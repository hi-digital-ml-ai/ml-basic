# Numbers for the validation video's Manim scenes, taken from the objects each page computed.
# Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 4–5: each fold scheme's pooled RMSE and median distance to the nearest
  # fitted station, run by run and averaged.
  "spatial-and-temporal-cv.qmd" = function(env, dir) {
    write(with(env, distance_runs), dir, "distance-runs")
    write(with(env, by_scheme), dir, "distance")
  },

  # Scenes 7–10: the hundred searched candidates with their noise columns, and the
  # nested scores.
  "cross-validation.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      candidate = seq_along(candidates), rmse = searched,
      noise = purrr::map_int(candidates, \(v) sum(startsWith(v, "noise"))),
      winner = seq_along(candidates) == which.min(searched))), dir, "search")
    write(with(env, tibble::tibble(claimed = claimed_mean, nested = nested_searched,
                                   eight_inputs = nested_eight)), dir, "nested")
  },

  # Scenes 14–15: the four models' measures.
  "regression-metrics.qmd" = function(env, dir) {
    write(with(env, scores), dir, "measures")
  },

  # Scene 17 and the quiz's answer: the shortlists and the cheapest thresholds.
  "choosing-a-metric.qmd" = function(env, dir) {
    write(with(env, dplyr::mutate(shortlists, perfect = perfect, at_random = at_random,
                                  budget = budget)), dir, "shortlists")
    write(with(env, cheapest), dir, "thresholds")
    write(with(env, dplyr::select(cost_curves, k, threshold, cost)), dir, "cost-curves")
  },

  # Scene 18: the Assumptions video's rare species and logistic regression at the
  # threshold that calls about as many stations present as hold it, as that video's
  # exports.R writes them, with the share of absences it calls absent.
  "../06-assumptions-limitations/class-imbalance.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(stations = nrow(train), present = n_present,
                                   prevalence = prevalence)), dir, "rare")
    write(with(env, {
      n <- nrow(plain_predictions)
      presences <- sum(plain_predictions$rare_species == "yes")
      dplyr::transmute(matched, threshold,
                       called_present = round(called * n),
                       false_alarms = round(false_alarms * (n - presences)),
                       sensitivity = found, specificity = 1 - false_alarms / (n - presences),
                       accuracy, presences, repeats = 5)
    }), dir, "matched")
  },

  # Scenes 22–26: each model's interval, the paired differences, and the thousand
  # bootstrap scores.
  "uncertainty-and-stability.qmd" = function(env, dir) {
    write(with(env, intervals), dir, "intervals")
    write(with(env, differences), dir, "paired")
    write(with(env, scores), dir, "bootstrap-scores")
  }
)
