# Editing TSP in your browser

You can make routine website changes on GitHub without installing anything. The website is built from `.qmd` files: ordinary text with a short metadata block between `---` lines at the top. Keep that block intact. Use `#` for a main heading, `##` for a section, `**bold text**`, and `[link text](relative/path.qmd)` for a link.

## Save an edit

1. Open the repository on GitHub and choose the file.
2. Select the pencil icon (**Edit this file**). Change the text; do not edit `_site`, which is generated automatically.
3. Use **Preview** to check basic formatting. GitHub’s preview is not the final website layout.
4. Select **Commit changes** and describe the edit. Prefer a new branch and pull request so the website build can check the change before it reaches `main`.
5. In the pull request, open **Checks**. The website check must pass. Merge when the content is ready for public release. After changes reach `main`, the **Publish website** workflow deploys automatically if GitHub Pages has been enabled.

If you directly commit to `main`, the same build runs and publishes on success. A failed build does not deploy new content. Open the failed Actions run and its step log; errors include the file or missing target where possible.

## Change homepage text

Edit `index.qmd`. Leave lines beginning with `:::` in place; they control layout. Edit text between them. The shared mission is in `_variables.yml`; changing its `mission` value updates places using `{{< var mission >}}`. The footer’s mission and website description are in `_quarto.yml` and should be updated consistently if the mission changes.

## Create a news post

1. Open `templates/news.qmd`, select the copy icon, and copy the contents.
2. Choose **Add file → Create new file**. Name the file `news/posts/your-short-title/index.qmd`. Typing `/` creates folders.
3. Paste the template. Replace the title, description, summary, author, categories, **and date** (`YYYY-MM-DD`). Write the article.
4. Keep `draft: true` while it is unfinished, or put the working copy under `drafts/` instead. Committed drafts are still visible in the GitHub repository; they are not private.
5. When approved, remove `draft: true`, check links, and save through a pull request. Do not use future dates to schedule publication; a ready post publishes as soon as it reaches `main`.

The news archive, homepage’s latest updates, search index, and news RSS feed update automatically. You do not need to change navigation or listing files. Articles should describe actual developments, not invented organizational activity.

## Publish a policy brief or analytical report

Copy `templates/policy-brief.qmd` or `templates/analytical-report.qmd` into `research/publications/your-short-title/index.qmd`. Replace every prompt and metadata field. Specify an accurate `publication-type`, `research-status`, topic categories, date, and author. Remove `draft: true` only after evidence, methods, limitations, permissions, and claims have been reviewed.

The research archive, categories, search, and research RSS feed update automatically. Never publish unfinished templates as findings. A research agenda can be published as an agenda, explicitly stating that findings are not available.

Ordinary publication pages do not execute R. A researcher runs analysis separately in `research-projects/`, reviews the outputs, and supplies approved figures and narrative. Do not copy raw participant data or confidential records into the site.

## Add a downloadable resource

1. Confirm the material is reviewed, has publication permission, is accessible, and contains no confidential information.
2. Use **Add file → Upload files** in `downloads/` to upload a clearly named file, such as `tsp-example-v1.pdf`. Do not upload a placeholder or an unfinished guide as a completed resource.
3. Copy `templates/program-resource.qmd` to `programs/resources/your-short-title.qmd`. Fill in the audience, status, version, date, limitations, and description.
4. Add a link such as `[Download the guide (PDF, 240 KB)](../../downloads/actual-file-name.pdf)`. Use the file’s real size and format. Include accessible alternatives when needed.
5. Remove `draft: true` only after review. Add a link from the relevant audience page; the program resource archive also updates automatically. Keep version and revision notes visible.

## Keep work unpublished

Use `drafts/` for ordinary, nonconfidential working material. The website only renders explicitly selected public paths, so templates, research projects, and drafts are excluded. An article left in a public content directory with `draft: true` is also excluded. Never put drafts in `assets/` or `downloads/`; those are copied to the public site. Never store secrets or private information anywhere in the repository, including drafts or issues.

## Change social links and branding

Edit the **Follow TSP** section of `get-involved.qmd`. Add ordinary Markdown links to verified accounts, just as you would add any other link in a Quarto document. Leave the explanatory text until Facebook, Instagram, or Action Network addresses are confirmed. There is no separate social configuration file.

The neutral wordmark is `assets/wordmark.svg`; the favicon is `assets/favicon.svg`. Colors and typography are at the top of `assets/brand.scss`. The mission is in `_variables.yml`. The website title, navigation, footer, and public base URL are in `_quarto.yml`.

## Change navigation

Edit the `website.navbar` section of `_quarto.yml`, retaining spaces and indentation. Use an existing `.qmd` path for each `href`. The six principal sections are Home, About, Programs, Research & Policy, News & Updates, and Get Involved. A new article does not need a navigation item.

If you add a wholly new section outside those paths, a maintainer must also update `project.render` so it is included intentionally. This safeguard keeps research source and unpublished materials out of the site.

## Correct published information

Edit the original page. For a meaningful factual correction, retain its original publication date and add a dated correction note explaining what changed and why. Add `date-modified: YYYY-MM-DD` if useful. Correct the source analysis too when relevant, then replace reviewed outputs. Do not silently erase a material error or imply a level of evidence the source does not support.

For typos and formatting, a clear commit message is enough. To withdraw an unsafe or substantially incorrect article, set `draft: true`, explain the withdrawal in a public update where appropriate, and check for links that need updating. A maintainer should remove obsolete deployed artifacts through the next clean build.

## Before publishing

- Does the page distinguish plans, established practice, and findings?
- Have dates, authors, links, citations, permissions, and claims been checked?
- Are all template prompts replaced and unpublished material excluded?
- Do meaningful images have helpful alternative text?
- Is personal, confidential, or sensitive information absent?
- Did the GitHub Actions checks pass?
