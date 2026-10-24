# Optional checks: run from the project root after rendering the whole website.
# Uses base R and yaml, already included in the locked reporting environment.
stopifnot(file.exists("_quarto.yml"), dir.exists("_site"))
config <- yaml::read_yaml("_quarto.yml")
stopifnot(identical(config$execute$enabled, FALSE),
          identical(config$website$`draft-mode`, "gone"))
site <- normalizePath("_site", winslash = "/")
pages <- list.files(site, "\\.html$", recursive = TRUE, full.names = TRUE)
pages <- pages[!grepl("/site_libs/", pages, fixed = TRUE)]
read_text <- function(path) paste(readLines(path, warn = FALSE), collapse = "\n")
matches <- function(pattern, text) regmatches(text, gregexpr(pattern, text, perl = TRUE))[[1]]
ids <- lapply(pages, function(p) {
  sub('"$', '', sub('^id="', '', matches('id="[^"]+"', read_text(p))))
})
names(ids) <- pages
prefix <- sub("/$", "", sub("^https?://[^/]+", "", config$website$`site-url`))
checked <- 0L
for (page in pages) {
  text <- read_text(page)
  stopifnot(length(matches("<h1\\b", text)) == 1L)
  if (grepl(":::", text, fixed = TRUE)) stop("Unparsed layout markup: ", page)
  images <- matches("<img\\b[^>]*>", text)
  if (any(!grepl('\\balt="', images))) stop("Image without alternative text: ", page)
  links <- sub('"$', '', sub('^(href|src)="', '', matches('(?:href|src)="[^"]+"', text)))
  for (link in links) {
    if (link == "#" || grepl("^([A-Za-z][A-Za-z0-9+.-]*:|//)", link)) next
    pieces <- strsplit(link, "#", fixed = TRUE)[[1]]
    path <- utils::URLdecode(sub("\\?.*$", "", pieces[1]))
    if (!nzchar(path)) {
      target <- page
    } else if (startsWith(path, "/")) {
      if (nzchar(prefix) && (path == prefix || startsWith(path, paste0(prefix, "/")))) {
        path <- substring(path, nchar(prefix) + 1L)
      }
      target <- file.path(site, sub("^/", "", path))
    } else {
      target <- file.path(dirname(page), path)
    }
    if (dir.exists(target)) target <- file.path(target, "index.html")
    if (!file.exists(target)) stop("Missing target in ", page, ": ", link)
    target <- normalizePath(target, winslash = "/")
    if (!startsWith(target, paste0(site, "/"))) stop("Link leaves public output: ", link)
    if (length(pieces) > 1L && nzchar(pieces[2]) && target %in% pages &&
        !utils::URLdecode(pieces[2]) %in% ids[[target]]) stop("Missing anchor: ", link)
    checked <- checked + 1L
  }
}
for (private in c("drafts", "templates", "research-projects", "renv", "scripts", ".github")) {
  if (file.exists(file.path(site, private))) stop("Nonpublic directory in site: ", private)
}
stopifnot(all(file.exists(file.path(site, c("news/index.xml", "research/index.xml", "search.json")))))
for (template in list.files("templates", "\\.qmd$", full.names = TRUE)) {
  if (!grepl("draft: true", read_text(template), fixed = TRUE)) stop("Template must default to draft: ", template)
}
source("research-projects/national-service/src/validate-inventory.R")
validate_inventory("research-projects/national-service/source-inventory.csv")
message("Passed: ", length(pages), " pages, ", checked,
        " internal links/assets, feeds, search, publication boundaries, and research inventory.")
