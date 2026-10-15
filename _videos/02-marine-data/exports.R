# Numbers for the marine data video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # The file's rows, its rows once duplicates are removed, and its sites.
  "the-coastal-survey.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(rows = nrow(raw), unique = nrow(dplyr::distinct(raw)),
                                   sites = dplyr::n_distinct(raw$site_id))), dir, "counts")
  },

  # The raw file's range table as the page prints it, the substrate spellings,
  # salinity's mean before and after -999 is marked missing, rounded as the page
  # rounds them, and the stations per season before and after dropping incomplete rows.
  "exploring-and-cleaning.qmd" = function(env, dir) {
    write(with(env, raw |>
      dplyr::summarise(dplyr::across(dplyr::where(is.numeric),
                                     list(min = \(x) min(x, na.rm = TRUE),
                                          mean = \(x) mean(x, na.rm = TRUE),
                                          max = \(x) max(x, na.rm = TRUE)))) |>
      tidyr::pivot_longer(dplyr::everything(), names_to = c("variable", "stat"),
                          names_sep = "_(?=[^_]+$)") |>
      tidyr::pivot_wider(names_from = stat, values_from = value) |>
      dplyr::mutate(dplyr::across(dplyr::where(is.numeric), \(x) round(x, 2)))), dir, "ranges")
    write(with(env, dplyr::count(raw, substrate, sort = TRUE)), dir, "substrate-spellings")
    write(with(env, tibble::tibble(
      raw_mean = round(mean(raw$salinity_psu), 2),
      clean_mean = round(mean(clean$salinity_psu, na.rm = TRUE), 1))), dir, "salinity-means")
    write(with(env, comparison), dir, "deletion")
    write(with(env, tibble::tibble(lost_pct, winter_lost_pct)), dir, "deletion-cost")
  },

  # The share of the random split's test stations at a site the model trained on.
  "splitting-data.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(seen_pct)), dir, "seen")
  },

  # The two leakage tables as the page prints them: target leakage and group leakage.
  "information-leakage.qmd" = function(env, dir) {
    write(with(env, target), dir, "target")
    write(with(env, group), dir, "group")
  }
)
