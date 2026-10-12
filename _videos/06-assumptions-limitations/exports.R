# Numbers for the assumptions video's Manim scenes, taken from the objects each page computed.
# Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 4–5: the random forest's curves beside the simulation's, each divided by its
  # own peak.
  "linearity-and-nonlinearity.qmd" = function(env, dir) {
    write(with(env, shapes), dir, "shapes")
  },

  # Scenes 9–11 and the quiz's answer: visits per site, the average catch in each
  # bootstrap sample (the page keeps only their spreads, so its own samples are
  # averaged again), and how much wider the catch and the forest's errors spread.
  "dependent-data.qmd" = function(env, dir) {
    write(with(env, dplyr::count(survey, site_id, name = "visits")), dir, "visits")
    write(with(env, purrr::imap(resamples, \(r, drawn)
      tibble::tibble(drawn = drawn, average = purrr::map_dbl(r$splits, \(s)
        mean(survey$abundance[as.integer(s)])))) |>
      purrr::list_rbind()), dir, "averages")
    write(with(env, dplyr::bind_rows("Average catch" = catch_spread,
                                     "Average forest error" = error_spread,
                                     .id = "estimate")), dir, "spreads")
  },

  # Scenes 14–18: each method's mean prediction by depth band with the true mean
  # count, the ratios below 140 m, and the stations of the novelty scatter.
  "sampling-and-extrapolation.qmd" = function(env, dir) {
    write(with(env, dplyr::summarise(bands, predicted = mean(predicted),
                                     true_mean = mean(true_mean),
                                     .by = c(model, id, depth))), dir, "beyond")
    write(with(env, ratios), dir, "ratios")
    write(with(env, dplyr::bind_rows(
      dplyr::transmute(surveyed, depth_m, temperature_c, season, status = "Surveyed"),
      dplyr::transmute(novelty, depth_m, temperature_c, season, status))), dir, "novelty")
  }
)
