# Numbers for the assumptions video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 6–7: the training stations' catches, and the forest's cross-validated errors
  # with their spread by fifth of the prediction.
  "distributional-assumptions.qmd" = function(env, dir) {
    write(with(env, dplyr::count(train, abundance, name = "stations")), dir, "counts")
    write(with(env, dplyr::select(errors, caught, predicted, error, fifth)), dir, "errors")
    write(with(env, spread), dir, "spread")
  },

  # Scenes 10–11: visits per site, and how many independent stations the survey is worth.
  "dependent-data.qmd" = function(env, dir) {
    write(with(env, dplyr::count(survey, site_id, name = "visits")), dir, "visits")
    write(with(env, dplyr::bind_rows("Average catch" = catch_spread,
                                     "Average forest error" = error_spread,
                                     .id = "estimate")), dir, "spreads")
  },

  # Scenes 12–15: the stations of the depth and temperature scatter.
  "sampling-and-extrapolation.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows(
      dplyr::transmute(surveyed, depth_m, temperature_c, season, status = "Surveyed"),
      dplyr::transmute(novelty, depth_m, temperature_c, season, status))), dir, "novelty")
  },

  # Scenes 17–19: the rare species' share and the calls at 0.5.
  "class-imbalance.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(stations = nrow(train), present = n_present,
                                   prevalence = prevalence, top = top,
                                   copies = copies)), dir, "rare")
    write(with(env, at_default), dir, "at-default")
  }
)
