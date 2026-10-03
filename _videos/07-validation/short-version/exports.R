# Numbers for the §7 Manim scenes, taken from the objects each page computed.
# Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 3–7: the hundred searched candidates with their noise columns, and the
  # nested scores.
  "cross-validation.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      candidate = seq_along(candidates), rmse = searched,
      noise = purrr::map_int(candidates, \(v) sum(startsWith(v, "noise"))),
      winner = seq_along(candidates) == which.min(searched))), dir, "search")
    write(with(env, tibble::tibble(claimed = claimed_mean, nested = nested_searched,
                                   eight_inputs = nested_eight)), dir, "nested")
  },

  # Scene 11 and the quiz's answer: the shortlists and the cheapest thresholds.
  "choosing-a-metric.qmd" = function(env, dir) {
    write(with(env, dplyr::mutate(shortlists, perfect = perfect, at_random = at_random,
                                  budget = budget)), dir, "shortlists")
    write(with(env, cheapest), dir, "thresholds")
    write(with(env, dplyr::select(cost_curves, k, threshold, cost)), dir, "cost-curves")
  },

  # Scenes 16–19: the paired differences and the thousand bootstrap scores.
  "uncertainty-and-stability.qmd" = function(env, dir) {
    write(with(env, differences), dir, "paired")
    write(with(env, scores), dir, "bootstrap-scores")
  }
)
