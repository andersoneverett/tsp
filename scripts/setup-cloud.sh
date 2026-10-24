#!/usr/bin/env bash
# Debian 13 x86_64 cloud setup; no system writes or tracked-file changes.
set -euo pipefail
cd /workspace/tsp
tool_root=/workspace/.tools
mkdir -p "$tool_root"/{downloads,bin,cache,apt/etc/apt,apt/lists/partial,apt/cache/archives/partial}
test "$(uname -m)" = x86_64 || { echo 'This helper requires x86_64; install Quarto and R normally on other platforms.' >&2; exit 1; }

quarto_version=1.8.27
release_url="https://github.com/quarto-dev/quarto-cli/releases/download/v${quarto_version}"
archive="quarto-${quarto_version}-linux-amd64.tar.gz"
curl --fail --silent --show-error --location --retry 2 "$release_url/quarto-${quarto_version}-checksums.txt" -o "$tool_root/downloads/quarto-checksums.txt"
if [ ! -f "$tool_root/downloads/$archive" ]; then
  curl --fail --silent --show-error --location --retry 2 "$release_url/$archive" -o "$tool_root/downloads/$archive"
fi
(
  cd "$tool_root/downloads"
  python3 - <<'PY'
import hashlib
from pathlib import Path
name = 'quarto-1.8.27-linux-amd64.tar.gz'
expected = next(line.split()[0] for line in Path('quarto-checksums.txt').read_text().splitlines() if line.split()[-1] == name)
actual = hashlib.file_digest(open(name, 'rb'), 'sha256').hexdigest()
if actual != expected:
    raise SystemExit('Quarto checksum mismatch. Remove the download and retry; do not bypass verification.')
print('Quarto archive SHA-256 verified.')
PY
)
if [ ! -x "$tool_root/quarto-$quarto_version/bin/quarto" ]; then
  tar -xzf "$tool_root/downloads/$archive" -C "$tool_root"
fi

# APT verifies Debian's signed package indexes and package hashes. Download and
# extract under /workspace because this machine does not provide root or sudo.
mkdir -p "$tool_root/apt/empty"
cat > "$tool_root/apt/apt.conf" <<'EOF'
Dir::Etc::main "/dev/null";
Dir::Etc::parts "/workspace/.tools/apt/empty";
Dir::Etc::sourcelist "/workspace/.tools/apt/etc/apt/sources.list";
Dir::Etc::sourceparts "/workspace/.tools/apt/empty";
Dir::State::lists "/workspace/.tools/apt/lists";
Dir::Cache "/workspace/.tools/apt/cache";
Dir::State::status "/var/lib/dpkg/status";
APT::Get::List-Cleanup "0";
EOF
cat > "$tool_root/apt/etc/apt/sources.list" <<'EOF'
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main
EOF
export APT_CONFIG="$tool_root/apt/apt.conf"
apt-get update
apt-get --download-only --no-install-recommends -o Debug::NoLocking=true -y install r-base-core r-cran-renv r-cran-knitr r-cran-rmarkdown
mkdir -p "$tool_root/r"
for package in "$tool_root"/apt/cache/archives/*.deb; do
  dpkg-deb -x "$package" "$tool_root/r"
done

python3 - <<'PY'
import os
from pathlib import Path
root = Path('/workspace/.tools/r')
# Relocate Debian configuration links and shared resource links. Some shared
# JavaScript dependencies already exist in the base image and are not downloaded.
for p in root.rglob('*'):
    if not p.is_symlink():
        continue
    target = p.readlink()
    if target.is_absolute() and (root / str(target).lstrip('/')).exists():
        p.unlink()
        p.symlink_to(root / str(target).lstrip('/'))
    elif not p.exists():
        resolved = Path(os.path.normpath(p.parent / target))
        try:
            system = Path('/') / resolved.relative_to(root)
        except ValueError:
            system = resolved
        if system.exists():
            p.unlink()
            p.symlink_to(system)
etc = root / 'usr/lib/R/etc'
renviron = etc / 'Renviron'
if renviron.is_symlink() or renviron.exists():
    renviron.unlink()
renviron.write_text((etc / 'Renviron.ucf').read_text())
for p in (root / 'usr/bin/R', root / 'usr/lib/R/bin/R'):
    p.write_text(p.read_text().replace('/usr/lib/R', str(root / 'usr/lib/R')).replace('/usr/share/R', str(root / 'usr/share/R')))
for name in ('R', 'Rscript'):
    p = Path('/workspace/.tools/bin') / name
    p.write_text('''#!/bin/sh
export RHOME=/workspace/.tools/r/usr/lib/R
export R_HOME=/workspace/.tools/r/usr/lib/R
export R_LIBS_SITE=/workspace/.tools/r/usr/lib/R/site-library
export LD_LIBRARY_PATH="/workspace/.tools/r/usr/lib/R/lib:/workspace/.tools/r/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec /workspace/.tools/r/usr/bin/''' + name + ''' "$@"
''')
    p.chmod(0o755)
PY
source scripts/cloud-env.sh

# Seed exact locked versions from the verified Debian packages when available.
# Never update a lockfile or overwrite an existing project package here.
Rscript --vanilla -e '
  library(renv)
  lock <- renv::lockfile_read("renv.lock")
  lib <- renv::paths$library(project = getwd())
  dir.create(lib, recursive = TRUE, showWarnings = FALSE)
  available <- installed.packages(lib.loc = "/workspace/.tools/r/usr/lib/R/site-library")
  for (p in names(lock$Packages)) {
    if (!dir.exists(file.path(lib, p)) && p %in% rownames(available) &&
        identical(available[p, "Version"], lock$Packages[[p]]$Version)) {
      stopifnot(file.copy(file.path("/workspace/.tools/r/usr/lib/R/site-library", p), lib, recursive = TRUE))
    }
  }
'
Rscript -e 'renv::restore(prompt = FALSE); renv::status()'
if ! python3 -c 'import yaml' 2>/dev/null; then
  python3 -m venv /workspace/.tools/validation-venv
  /workspace/.tools/validation-venv/bin/python -m pip install PyYAML==6.0.3
fi
quarto --version
Rscript scripts/test-research.R
quarto render research-projects/national-service/reports/report.qmd --execute
quarto render
if python3 -c 'import yaml' 2>/dev/null; then
  python3 scripts/validate.py
else
  /workspace/.tools/validation-venv/bin/python scripts/validate.py
fi
