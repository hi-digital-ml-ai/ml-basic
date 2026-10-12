# Numbers for the assumptions video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 4–8: the training stations' catches, the forest's cross-validated errors and
  # their spread by fifth of the prediction, and the two forests' RMSEs and totals.
  "distributional-assumptions.qmd" = function(env, dir) {
    write(with(env, dplyr::count(train, abundance, name = "stations")), dir, "counts")
    write(with(env, dplyr::select(errors, caught, predicted, error, fifth)), dir, "errors")
    write(with(env, spread), dir, "spread")
    write(with(env, totals), dir, "totals")
  },

  # Scenes 12–16: the stations of the novelty scatter, the range check against the
  # distance, and the forest's error by distance from the survey.
  "sampling-and-extrapolation.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows(
      dplyr::transmute(surveyed, depth_m, temperature_c, season, status = "Surveyed"),
      dplyr::transmute(novelty, depth_m, temperature_c, season, status))), dir, "novelty")
    write(with(env, tibble::tibble(stations = nrow(asked), in_range = sum(asked$every_range),
                                   hidden = sum(asked$every_range & asked$far))), dir, "range-check")
    write(with(env, by_distance), dir, "by-distance")
  },

  # Scenes 18–24: the rare species' share, each recipe's calls at 0.5, every threshold
  # without rebalancing, the threshold at the prevalence, and each recipe's average
  # probability against the share of its predictions with the species.
  "class-imbalance.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(stations = nrow(train), present = n_present,
                                   prevalence = prevalence, top = top,
                                   copies = copies)), dir, "rare")
    write(with(env, at_default), dir, "at-default")
    write(with(env, curve), dir, "curve")
    write(with(env, same), dir, "same")
    write(with(env, dplyr::summarise(predictions, average = mean(.pred_yes),
                                     share = mean(rare_species == "yes"),
                                     .by = training)), dir, "chances")
  }
)
