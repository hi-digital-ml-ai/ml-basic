# Numbers for the §6 Manim scenes, taken from the objects each page computed.
# Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 5–7: the straight-line model's caught ÷ predicted along each input, and
  # the curves of the random forest and the GAM beside the simulation's, each divided
  # by its own peak.
  "linearity-and-nonlinearity.qmd" = function(env, dir) {
    write(with(env, checks), dir, "error-check")
    write(with(env, shapes), dir, "shapes")
  },

  # Scene 25, the quiz's answer: the two forests' RMSEs and totals against the catch.
  "distributional-assumptions.qmd" = function(env, dir) {
    write(with(env, totals), dir, "totals")
  },

  # Scenes 10–12: visits per site, and the average catch in each bootstrap sample
  # drawn by station and by site (the page keeps only their spreads, so the same
  # samples are averaged again).
  "independence-of-observations.qmd" = function(env, dir) {
    write(with(env, dplyr::count(prepared, site_id, name = "visits")), dir, "visits")
    write(with(env, dplyr::bind_rows(
      tibble::tibble(drawn = "By station", average = average_catch(by_station)),
      tibble::tibble(drawn = "By site", average = average_catch(by_site)))),
      dir, "averages")
    write(with(env, average_spread), dir, "average-spread")
  },

  # Scenes 13–14: the sites with their block and their fold in the first round of
  # each scheme, and the forests' R².
  "spatial-and-temporal-dependence.qmd" = function(env, dir) {
    fold_of <- function(folds) {
      first <- dplyr::filter(folds, id == "Repeat1")
      purrr::map2(first$splits, first$id2, \(s, fold)
        tibble::tibble(site_id = unique(rsample::assessment(s)$site_id), fold = fold)) |>
        purrr::list_rbind()
    }
    centres <- with(env, dplyr::summarise(train, x = mean(longitude) * 83,
                                          y = mean(latitude) * 111, .by = site_id))
    sites <- with(env, dplyr::distinct(train, site_id, block)) |>
      dplyr::left_join(centres, by = "site_id") |>
      dplyr::left_join(dplyr::rename(fold_of(env$by_site), site_fold = fold), by = "site_id") |>
      dplyr::left_join(dplyr::rename(fold_of(env$by_block), block_fold = fold), by = "site_id")
    write(sites, dir, "sites")
    write(with(env, tidyr::pivot_longer(r2, -inputs, names_to = "scheme", values_to = "r2")),
          dir, "position-r2")
  },

  # Scenes 16–22: each forest's mean prediction by depth band with the true mean
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
