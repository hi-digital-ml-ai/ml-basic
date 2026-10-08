# Numbers for the interpretation video's Manim scenes, taken from the objects each
# page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 7-9: the forest's impurity importance, permutation importance on one
  # split's test sites, how many test sites that split held, and on how many of the
  # ten splits each input beat the random columns.
  "feature-importance.qmd" = function(env, dir) {
    write(with(env, impurity_table), dir, "impurity")
    write(with(env, one_split), dir, "permutation")
    write(with(env, tibble::tibble(test_sites = dplyr::n_distinct(test$site_id),
                                   splits = nrow(splits))), dir, "one-split")
    write(with(env, beats), dir, "beats")
  },

  # Scene 11: the forest's partial dependence on temperature, every station's ICE
  # curve, and how many stations rise to the peak and fall from it.
  "partial-effects.qmd" = function(env, dir) {
    write(with(env, partial$temperature_c), dir, "partial")
    write(with(env, ice$temperature_c), dir, "ice")
    write(with(env, tibble::tibble(stations = nrow(changes),
                                   rise = sum(changes$rise > 0),
                                   fall = sum(changes$fall > 0),
                                   peak = top)), dir, "ice-changes")
  },

  # Scene 12: the GAM's temperature curve with its interval, and the models' RMSEs
  # on the same folds.
  "black-box-or-not.qmd" = function(env, dir) {
    write(with(env, curves$temperature_c), dir, "gam-curve")
    write(with(env, comparison), dir, "comparison")
  },

  # Scenes 17-20: the GAM's two intervals, the forest's conformal interval at the
  # test sites, and the same forest calibrated on low chlorophyll.
  "communicating-uncertainty.qmd" = function(env, dir) {
    write(with(env, gam_summary), dir, "gam-intervals")
    write(with(env, tibble::tibble(coverage = mean(conformal$inside),
                                   width = 2 * half_width)), dir, "conformal")
    write(with(env, dplyr::summarise(shifted, coverage = mean(inside),
                                     width = mean(high - low),
                                     .by = c(stations, interval))), dir, "shift")
  },

  # Scene 29, the quiz's answer: the forest's RMSE across seeds, splits and folds.
  "reproducibility.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(run = 1:10, seed = by_seed, split = by_split,
                                   folds = by_folds)), dir, "spread")
  },

  # Scenes 24-25: rock's multiplier and the cross-validated RMSE, as recorded and
  # with half the animals on rock missed.
  "from-model-to-claim.qmd" = function(env, dir) {
    write(with(env, gear), dir, "gear")
  }
)
