# Teen Service Project · Alpha v0.1

**Advancing youth opportunity through research, advocacy, and civic engagement.**

Teen Service Project (TSP) is an independent grassroots initiative being redeveloped around community programming, applied research, and public policy advocacy. This repository contains the public Quarto website, reproducible R research workspace, publication templates, and a starting point for developing youth service materials.

This alpha does not claim active events, partnerships, completed research, participant outcomes, or a finished curriculum. Original TSP materials and a verified history remain to be supplied. No blanket software or content license has been selected; see [licensing decisions](docs/LICENSING.md).

## For routine content editing

Start with [EDITING-GUIDE.md](EDITING-GUIDE.md). You can edit pages and publish news or research through GitHub’s browser interface; RStudio, a terminal, and local deployment tools are not needed. GitHub Actions builds and deploys approved changes on `main` after Pages is enabled.

## Repository layout

| Path | Purpose |
| --- | --- |
| `index.qmd`, `about.qmd`, `get-involved.qmd` | Principal public pages |
| `programs/` | Model, audience pages, feedback, and future resource pages |
| `news/posts/<slug>/index.qmd` | Automatically listed updates |
| `research/publications/<slug>/index.qmd` | Automatically listed agendas, briefs, and reports |
| `research-projects/` | Analytical source, data documentation, and local reports; excluded from site |
| `assets/`, `downloads/` | Approved public assets and downloads |
| `templates/`, `drafts/` | Unpublished templates and working text; excluded from site |
| `renv/`, `renv.lock`, `.Rprofile` | Reproducible R environment |
| `scripts/`, `.github/` | Validation and publishing automation |

## Website development

Install [Quarto 1.8.27](https://quarto.org/docs/get-started/) and Python 3.12 or later. Python validation requires `PyYAML==6.0.3` (`python -m pip install PyYAML==6.0.3`). Website rendering needs **no R packages or datasets**.

```sh
quarto render
python3 scripts/validate.py
quarto preview --no-browser
```

The generated website is in `_site/` and is ignored by Git. Public rendering uses an explicit allowlist. `draft: true` adds a second safeguard for unfinished content, but a public Git repository still exposes committed drafts. Never commit confidential information.

Run `python3 scripts/test-listings.py` to test adding and removing a temporary news article, research publication, and unpublished draft. It rebuilds the site and checks listing, RSS, search, and draft behavior, then removes only its own temporary files and rebuilds the final site.

Optional browser validation uses `python3 scripts/test-browser.py` with Playwright and Chromium installed. Pass `--axe /path/to/axe.min.js` for automated WCAG A/AA checks. This starts a temporary internal server at the configured project URL path and tests all public pages at desktop and mobile widths, navigation, search, archive filtering, draft-safe public configuration, and keyboard access. It does not establish a complete accessibility audit. The cloud validation used Playwright’s installed Python package, system Chromium, and axe-core 4.10.3.

## R research

Use R 4.5.0 and restore the project’s package lock:

```sh
Rscript -e 'renv::restore(prompt = FALSE)'
Rscript research-projects/national-service/src/validate-inventory.R
quarto render research-projects/national-service/reports/report.qmd --execute
```

The initial lock contains `renv`, `knitr`, `rmarkdown`, and the dependencies required for analytical reports. Data manipulation and plotting packages such as `dplyr`, `readr`, `ggplot2`, or the full `tidyverse` can be installed with `renv::install()` when actual analysis requires them, followed by a reviewed `renv::snapshot()`. See the [research workspace instructions](research-projects/national-service/README.md).

No sources or datasets have been fabricated. The executable report validates an intentionally empty inventory and records session information; it is a template, not evidence of program effects. Publish only reviewed, approved artifacts to the website. Ordinary publishing never reruns the analytical projects.

## Cloud environment

In this Debian 13 environment, `bash scripts/setup-cloud.sh` installs verified tooling under `/workspace/.tools` without system administration. Then use `source scripts/cloud-env.sh`. The install script leaves content and lockfiles unchanged. Reuse the existing checkout; each cloud task is already isolated and needs no extra Git worktree.

Allow `cloud.r-project.org` in environment settings for new CRAN packages or a fresh source restore. The prepared locked library and report template work in the current instance; a clean CRAN download on another machine has not been tested. Reusable installation and startup instructions and this CRAN domain requirement are saved in the environment configuration draft; review and save the settings, then publish the environment to retain them.

## Publish on GitHub Pages

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). The selected remote is currently `everettsaccount/tsp`; the intended repository name is `teen-service-project`. The project and R project already use that name. A maintainer can rename the existing repository in GitHub Settings without creating a second copy, then update `website.site-url` in `_quarto.yml` and the checkout remote. Until then the configuration targets the current `tsp` project path. Neither a rename nor a live deployment has been performed by the local build.

## Contribute and correct

See [CONTRIBUTING.md](CONTRIBUTING.md). Research suggestions, resource feedback, and technical problem issue templates are included. Do not post personal or confidential information about young people. Report limitations and contradictory evidence as carefully as positive results.
