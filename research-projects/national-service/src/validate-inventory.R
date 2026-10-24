# Run from the repository root. No packages or data downloads required.
validate_inventory <- function(path) {
  inventory <- read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
  required <- c("source_id", "title", "publisher", "publication_date", "url",
                "retrieved_date", "source_type", "population", "coverage", "method",
                "limitations", "access_conditions", "verification_status", "reviewed_by", "notes")
  if (!identical(names(inventory), required)) stop("Source inventory columns do not match the documented schema.")
  if (anyDuplicated(inventory$source_id)) stop("Source identifiers must be unique.")
  if (nrow(inventory) > 0L) {
    if (any(is.na(inventory$source_id) | !nzchar(inventory$source_id))) stop("Every source needs an identifier.")
    allowed <- c("candidate", "verified", "excluded")
    if (any(is.na(inventory$verification_status) | !inventory$verification_status %in% allowed)) {
      stop("Use candidate, verified, or excluded for verification_status.")
    }
    verified <- inventory$verification_status == "verified"
    for (field in c("title", "publisher", "url", "retrieved_date", "method", "limitations", "access_conditions", "reviewed_by")) {
      if (any(is.na(inventory[[field]][verified]) | !nzchar(inventory[[field]][verified]))) {
        stop(paste("Verified sources require", field))
      }
    }
  }
  message(nrow(inventory), " source(s); ", sum(inventory$verification_status == "verified"), " verified. An empty inventory contains no evidence.")
  invisible(inventory)
}

if (sys.nframe() == 0L) {
  validate_inventory("research-projects/national-service/source-inventory.csv")
}
