# Alpha v0.1 status

The public site is a foundation for TSP’s redevelopment. It is not a claim that events, a complete curriculum, partnerships, research findings, or national programming are already in place.

## Implemented

- Six principal sections, responsive editorial styling, neutral configurable wordmark, original community illustration, search, privacy and accessibility pages, and a useful 404 page.
- Automatic news and research archives with metadata, topic categories, filtering, and RSS; a homepage news listing and program resource archive.
- An explicitly labeled national service research agenda and proposed community model, with separate information for teens, facilitators, and host communities.
- Reusable draft-first templates, publication boundaries, approved public asset directories, browser editing instructions, contribution guidance, issue forms, and Pages automation.
- An R 4.5.0 workspace managed by renv, Quarto analytical template, empty source inventory and dictionary templates, source validation, and future program evaluation planning.

## Materials and decisions still needed

- Original TSP program materials, verified history, dates, and attribution.
- Youth and community review of the proposed model and resource priorities.
- Verified research sources, lawful datasets, a reviewed analysis plan, and subsequent evidence-based publications.
- Real contact and social channels; a suitable confidential feedback route before sensitive information is collected.
- Confirmed local responsibilities, safeguarding, access, consent, and practical support before events are offered.
- Separate intellectual property and licensing decisions for code, publications, and program resources.
- Owner publication steps, including the intended repository name and GitHub Pages settings; see DEPLOYMENT.md.

## What the local checks mean

Rendering and internal-link checks validate the public site. Temporary content integration checks exercise automatic archives, homepage updates, RSS, search inclusion, and exclusion of draft content. R checks validate the empty workspace’s schema and reporting environment; they do not validate any research finding. Browser and automated accessibility checks cover the tested pages and interactions, not every assistive technology or future resource.

The current installed library has been checked against the renv lock. A clean CRAN download on a separate machine and a remote GitHub Actions/Pages deployment remain distinct checks. Local tooling is obtained through HTTPS and Debian’s signed indexes with package checksum verification; the Quarto archive is checked against its official SHA-256 list.

Local alpha validation completed:

- Quarto render and source validation: 19 public HTML pages; 688 internal links and asset references checked.
- Real temporary content tests: new news and research entries appeared in archives, homepage news, RSS, and search; unpublished content remained excluded. Fixtures were removed and the real site rebuilt.
- Chromium: all 19 pages checked at desktop (1440 px) and mobile (390 px) widths; search, archive filtering, keyboard category selection, skip link, mobile navigation, and optional social configuration passed.
- axe-core 4.10.3: zero automated WCAG A/AA findings on the 19 pages at both tested sizes. This is not a complete accessibility audit.
- R: six inventory validation checks passed; the executable analytical template rendered; the 27-package project library synchronized with renv.lock for R 4.5.0.
- GitHub Actions: both workflows passed actionlint 1.7.7. Remote workflow execution and deployment were not performed.
- The reusable cloud setup script was executed successfully, and Quarto preview returned HTTP 200 with the expected homepage. Installation/startup instructions and the CRAN domain addition were saved as an environment draft; publication of that draft remains an owner step.
