# GitHub Pages publication

## One-time owner setup

1. Keep this as one repository. The existing selected remote is `everettsaccount/tsp`. If the final name should be `teen-service-project`, rename it in **Repository Settings → General → Repository name**. No remote rename has been attempted because GitHub API access is unavailable in the build environment.
2. Set `website.site-url` in `_quarto.yml` to the real project Pages URL. It currently uses `https://everettsaccount.github.io/tsp/`. After the rename, use `https://everettsaccount.github.io/teen-service-project/`. Keep the trailing slash. This controls canonical URLs, sitemap, RSS, and project-path behavior.
3. Push/merge the reviewed project onto `main`. This empty starting repository did not originally have a `main` branch. Set `main` as the default branch in GitHub when it exists.
4. Open **Settings → Pages → Build and deployment → Source → GitHub Actions**. Confirm Pages is available for the repository’s visibility and account plan.
5. Open **Actions → Publish website**. The workflow runs after changes to `main`; it can also be started with **Run workflow** on `main`. Review the build and deployment jobs. The deployment job requires Pages permission and the `github-pages` environment; organization rules may require an owner to authorize it.
6. After a successful deployment, use GitHub’s reported Pages address. Confirm Home, a nested news article, a nested publication, search, RSS, and the mobile menu on the deployed site.

No custom domain, DNS change, external hosting, or secret token is required for the standard project Pages workflow. Do not add placeholder contact or social URLs. Local render success does not prove remote Actions or Pages settings work.

## What automation does

`.github/workflows/website.yml` validates source metadata, renders with Quarto 1.8.27, validates generated internal links and exclusions, and exercises the publication-listing workflow. Pull requests build and check but do not deploy. Successful `main` builds upload `_site` and deploy using GitHub’s official Pages actions. Concurrency prevents overlapping deployments. Each CI checkout starts without stale generated artifacts.

R is deliberately absent from website CI. The website has `execute.enabled: false` and a render allowlist excluding `research-projects/`, `drafts/`, and `templates/`. Analytical work has its own optional/research-change CI in `research.yml` using the `renv.lock` environment. Routine content updates do not run research.

## Troubleshooting

- **Build fails before rendering:** open the source validation step; correct the named metadata, JSON, or workflow issue.
- **Broken link:** use the generated-link check’s file and target. Paths in articles are relative to the article’s directory.
- **Nothing deploys:** confirm the successful run is on `main`, Pages source is GitHub Actions, Actions are enabled, and the repository owner permits Pages deployment.
- **Wrong links or RSS address after renaming:** update `website.site-url` and rerun the workflow. Update the local Git remote separately.
- **An article is missing:** check its directory, `index.qmd` filename, metadata, and `draft: true` flag. Future dates do not schedule content.
- **Unexpected research execution:** check the allowlist and any page-specific `execute` overrides; public publication pages should contain reviewed static outputs.
