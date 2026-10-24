# National service research workspace

Status: **in development; no evidence synthesis or findings yet**.

Question: How can paid national service expand youth opportunity, workforce development, and civic participation, and what does existing evidence suggest about program effectiveness and equitable access?

- `research-plan.md`: questions, methods, review criteria, ethics, and publication gates.
- `source-inventory.csv`: intentionally header-only pending verification; not a bibliography of verified evidence.
- `data-dictionary.csv`: header-only template for dataset and variable definitions.
- `data/raw/`: immutable source files, locally stored and ignored by Git.
- `data/processed/`: derived, documented outputs; locally stored and ignored.
- `src/validate-inventory.R`: checks inventory structure and verification requirements.
- `figures/`: generated figures, separate from approved public assets.
- `reports/report.qmd`: executable analytical report template, outside the website render scope.

From the repository root:

```sh
Rscript -e 'renv::restore(prompt = FALSE)'
Rscript research-projects/national-service/src/validate-inventory.R
quarto render research-projects/national-service/reports/report.qmd --execute
```

The template can render without datasets. It reports an empty inventory explicitly and contains no analysis or synthetic results. `execute: enabled: true` in this report overrides the website’s disabled execution. It writes a local report here, never under `_site`. An empty inventory is a scaffolding check, not a research result.

Install analytical dependencies when needed, for example `renv::install(c("dplyr", "readr", "ggplot2"))`, and run `renv::snapshot()` after reviewing the dependency changes. The full tidyverse is supported but is not preinstalled without a research need. Record scripts and decisions; do not run substantive analyses as part of routine website publication.

After review, export **only cleared public figures** to `assets/research/` and write a publication in `research/publications/<slug>/index.qmd`. Record source provenance, methods, limitations, code revision, and run date. Keep raw or personal data out of public artifacts and Git history.
