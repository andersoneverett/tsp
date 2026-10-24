# Dependency-free behavioral checks of the real source inventory validator.
source("research-projects/national-service/src/validate-inventory.R")
inventory <- validate_inventory("research-projects/national-service/source-inventory.csv")
stopifnot(nrow(inventory) == 0L)
temporary <- tempfile(fileext = ".csv")
expect_failure <- function(data) {
  write.csv(data, temporary, row.names = FALSE, na = "")
  result <- tryCatch({validate_inventory(temporary); FALSE}, error = function(e) TRUE)
  stopifnot(result)
}
expect_failure(data.frame(wrong_column = "test"))
candidate <- as.data.frame(setNames(rep(list(""), ncol(inventory)), names(inventory)))
candidate$source_id <- "test-only-not-a-source"
candidate$verification_status <- "candidate"
write.csv(candidate, temporary, row.names = FALSE)
stopifnot(nrow(validate_inventory(temporary)) == 1L)
expect_failure(rbind(candidate, candidate))
candidate$verification_status <- "verified"
expect_failure(candidate)
candidate$verification_status <- "unknown"
expect_failure(candidate)
unlink(temporary)
message("Passed 6 checks: empty inventory, schema rejection, candidate accepted, duplicate rejection, unverified claim rejection, invalid status rejection.")
