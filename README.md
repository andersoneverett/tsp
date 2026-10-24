# Teen Service Project

**Advancing youth opportunity through research, advocacy, and civic engagement.**

An R and Quarto project: the public website, research workspace, and developing youth service resources live together here. The website is at **https://andersoneverett.github.io/tsp/**.

## Everyday editing

Open `teen-service-project.Rproj` in RStudio. Open a `.qmd` page, edit its text, and click **Render**. Use **Render Website** in the Build pane to render all pages. Quarto also supports `quarto preview` and `quarto render` from a terminal.

You can also edit directly on GitHub. Saving approved changes to `main` runs one GitHub Actions workflow that renders Quarto and publishes the site. See [EDITING-GUIDE.md](EDITING-GUIDE.md) for adding news, publications, and resources without using a terminal.

## Where things live

| What you want to change | File or folder |
| --- | --- |
| Homepage | `index.qmd` |
| Navigation, footer, public URL | `_quarto.yml` |
| Shared mission text | `_variables.yml` |
| Colors and typography | `assets/brand.scss` |
| Social and contact links | `get-involved.qmd` — ordinary Markdown links when verified |
| Program pages and resources | `programs/` |
| News articles | `news/posts/<slug>/index.qmd` |
| Research publications | `research/publications/<slug>/index.qmd` |
| Research code, source inventory, and local reports | `research-projects/` |
| Reusable documents and unpublished working text | `templates/` and `drafts/` |
| Approved public downloads | `downloads/` |

News and research archives, categories, search, and RSS are built by Quarto. Adding a properly formatted article updates its archive automatically. The design uses one SCSS theme and local SVG images. A small include in `includes/accessibility.html` corrects keyboard and navigation behavior in Quarto 1.8; there is no custom application or dynamic configuration service.

## R research

Use **R 4.5.0** and **Quarto 1.8.27**. In the R console at the project root:

```r
renv::restore()
source("research-projects/national-service/src/validate-inventory.R")
validate_inventory("research-projects/national-service/source-inventory.csv")
```

Open `research-projects/national-service/reports/report.qmd` and click **Render** to run the analytical template. Its separate Quarto configuration keeps analysis outside the public website. The equivalent terminal command is `quarto render research-projects/national-service/reports/report.qmd --execute`.

The lock contains the packages needed for reports. Add `ggplot2`, tidyverse packages, or other analytical dependencies with `renv::install()` when needed, then use `renv::snapshot()` to record them. Ordinary website updates do not run R analyses or need datasets.

The initial source inventory is intentionally empty. The report is a working template, not research findings. Original TSP materials, verified history, sources, and datasets remain to be supplied. The program pages distinguish proposed guidance from tested practice.

## Optional checks

After rendering the whole website, run this in the R console:

```r
source("scripts/check.R")
```

This checks rendered internal links, feeds, search, draft boundaries, image alternative text, and the research inventory. It uses base R and `yaml`, already included in the locked reporting environment. There is no Python, Node, or browser-testing toolchain to install or maintain for this project.

## Publishing

GitHub Pages is enabled for this repository. The single workflow in `.github/workflows/website.yml` builds pull requests and publishes successful `main` builds. For a fresh repository, choose **Settings → Pages → Source → GitHub Actions**. No personal access token or extra hosting service is needed.

If you rename the repository to `teen-service-project`, update `website.site-url` in `_quarto.yml` to match the new Pages URL. For an error, open **Actions → Publish website** and inspect the failed step; you can retry with **Run workflow**.

The public render explicitly excludes drafts, templates, and analytical projects. `_site/` is generated and not committed. A public Git repository still exposes committed drafts: never commit private participant information, confidential research records, or credentials.

See [CONTRIBUTING.md](CONTRIBUTING.md) for suggestions and corrections. Licensing choices remain open for code, publications, and program materials separately; see [docs/LICENSING.md](docs/LICENSING.md).
