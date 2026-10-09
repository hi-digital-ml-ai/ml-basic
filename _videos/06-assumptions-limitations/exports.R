# Numbers for the §6 Manim scenes, taken from the objects each page computed.
# Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 5–7: linear regression's average error along each input, and the random
  # forest's curves beside the simulation's, each divided by its own peak.
  "linearity-and-nonlinearity.qmd" = function(env, dir) {
    write(with(env, checks), dir, "error-check")
    write(with(env, shapes), dir, "shapes")
  },

  # Scene 27, the quiz's answer: the two forests' RMSEs and totals against the catch.
  "distributional-assumptions.qmd" = function(env, dir) {
    write(with(env, totals), dir, "totals")
  },

  # Scenes 10–15: visits per site, each site's block and centre, the average catch in
  # each bootstrap sample (the page keeps only their spreads, so its own samples are
  # averaged again), and how much wider the catch and the forest's errors spread.
  "dependent-data.qmd" = function(env, dir) {
    write(with(env, dplyr::count(survey, site_id, name = "visits")), dir, "visits")
    write(with(env, dplyr::summarise(survey, block = dplyr::first(block),
                                     x = mean(longitude) * 83, y = mean(latitude) * 111,
                                     .by = site_id)), dir, "sites")
    write(with(env, purrr::imap(resamples, \(r, drawn)
      tibble::tibble(drawn = drawn, average = purrr::map_dbl(r$splits, \(s)
        mean(survey$abundance[as.integer(s)])))) |>
      purrr::list_rbind()), dir, "averages")
    write(with(env, dplyr::bind_rows("Average catch" = catch_spread,
                                     "Average forest error" = error_spread,
                                     .id = "estimate")), dir, "spreads")
  },

  # Scenes 17–24: each method's mean prediction by depth band with the true mean
  # count, the ratios below 140 m, the stations of the novelty scatter, and the
  # forest's error by distance from the survey.
  "sampling-and-extrapolation.qmd" = function(env, dir) {
    write(with(env, dplyr::summarise(bands, predicted = mean(predicted),
                                     true_mean = mean(true_mean),
                                     .by = c(model, id, depth))), dir, "beyond")
    write(with(env, ratios), dir, "ratios")
    write(with(env, dplyr::bind_rows(
      dplyr::transmute(surveyed, depth_m, temperature_c, season, status = "Surveyed"),
      dplyr::transmute(novelty, depth_m, temperature_c, season, status))), dir, "novelty")
    write(with(env, by_distance), dir, "by-distance")
  }
)
