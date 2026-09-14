# Loaders for the example datasets in data/.
# Pages load this with: source(here::here("R/data.R"))
#
# Every loader returns a tibble and documents, in a comment, where the data came
# from and what one row means. Add a loader here rather than reading files
# directly in a page, so a dataset used by several pages stays consistent.

# Example shape (delete once a real dataset lands in data/):
#
# #' Coastal CTD casts, one row per depth bin per cast.
# #' Source: <survey name, years, licence>
# load_ctd <- function() {
#   readr::read_csv(here::here("data", "ctd-casts.csv"), show_col_types = FALSE)
# }
