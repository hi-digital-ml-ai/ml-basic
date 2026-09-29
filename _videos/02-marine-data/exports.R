# Numbers for the marine data video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # The file's columns and rows, the four answers to "how many observations?", and how
  # often each site was visited.
  "observations-and-features.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(column = names(raw), rows = nrow(raw))), dir, "columns")
    write(with(env, dplyr::mutate(counts, what = as.character(what))), dir, "row-counts")
    write(with(env, dplyr::count(dplyr::count(raw, site_id, name = "visits"), visits,
                                 name = "number_of_sites")), dir, "site-visits")
  },

  # The raw file: the range table as the page prints it, every salinity value, missing
  # chlorophyll by season, the substrate spellings, the rare species and the vessels.
  "exploratory-analysis.qmd" = function(env, dir) {
    write(with(env, raw |>
      dplyr::summarise(dplyr::across(dplyr::where(is.numeric),
                                     list(min = \(x) min(x, na.rm = TRUE),
                                          mean = \(x) mean(x, na.rm = TRUE),
                                          max = \(x) max(x, na.rm = TRUE)))) |>
      tidyr::pivot_longer(dplyr::everything(), names_to = c("variable", "stat"),
                          names_sep = "_(?=[^_]+$)") |>
      tidyr::pivot_wider(names_from = stat, values_from = value) |>
      dplyr::mutate(dplyr::across(dplyr::where(is.numeric), \(x) round(x, 2)))), dir, "ranges")
    write(with(env, dplyr::select(raw, salinity_psu)), dir, "salinity")
    write(with(env, raw |> dplyr::group_by(season) |>
      dplyr::summarise(missing = 100 * mean(is.na(chlorophyll_mg_m3)))), dir, "chlorophyll-missing")
    write(with(env, dplyr::count(raw, substrate, sort = TRUE)), dir, "substrate-spellings")
    write(with(env, raw |> dplyr::count(rare_species) |>
      dplyr::mutate(percent = round(100 * n / sum(n), 1))), dir, "rare-species")
    write(with(env, raw |>
      dplyr::filter(salinity_psu != -999) |>
      dplyr::group_by(vessel) |>
      dplyr::summarise(stations = dplyr::n(),
                       mean_salinity = round(mean(salinity_psu), 2),
                       mean_temperature = round(mean(temperature_c[temperature_c != -999]), 2))),
      dir, "vessels")
  },

  # After the page's repairs: the substrates, the salinity mean, the depths before and
  # after dividing by ten (with temperature, the page's evidence), and the cost of
  # dropping incomplete rows.
  "missing-values-and-outliers.qmd" = function(env, dir) {
    write(with(env, dplyr::count(clean, substrate)), dir, "substrates")
    write(with(env, tibble::tibble(
      raw_mean = mean(raw$salinity_psu, na.rm = TRUE),
      clean_mean = mean(clean$salinity_psu, na.rm = TRUE))), dir, "salinity-means")
    write(with(env, raw |> dplyr::distinct() |>
      dplyr::filter(temperature_c != -999) |>
      dplyr::transmute(recorded = depth_m, temperature_c, corrected = depth_m > 250,
                       depth_m = dplyr::if_else(depth_m > 250, depth_m / 10, depth_m))),
      dir, "depths")
    write(with(env, comparison), dir, "deletion")
    write(with(env, tibble::tibble(
      rows_before = nrow(clean),
      rows_after = nrow(tidyr::drop_na(clean)),
      winter_lost_pct = round(100 * (1 - sum(tidyr::drop_na(clean)$season == "winter") /
                                         sum(clean$season == "winter")), 1))), dir, "deletion-cost")
  },

  # The random split's sites shared with training, and the rare species under the three
  # ways of asking for a stratified split. The page prints these without keeping them,
  # so they are recomputed from its own split objects.
  "splitting-data.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      training = nrow(training(plain)), testing = nrow(testing(plain)),
      sites = dplyr::n_distinct(survey$site_id),
      sites_in_both = length(intersect(training(plain)$site_id, testing(plain)$site_id)),
      test_rows_seen = sum(testing(plain)$site_id %in% training(plain)$site_id))), dir, "shared-sites")
    write(with(env, {
      pct <- \(x) 100 * mean(x$rare_species == "yes")
      tibble::tibble(
        split = c("all", "unstratified", "stratified", "properly"),
        train_pct = c(pct(survey), pct(training(unstratified)), pct(training(stratified)),
                      pct(training(properly))),
        test_pct = c(NA, pct(testing(unstratified)), pct(testing(stratified)),
                     pct(testing(properly))),
        positives = sum(survey$rare_species == "yes"))
    }), dir, "stratify")
  },

  # The three demonstrated leaks, rerun with the page's own functions and splits (the
  # forest's seed is fixed, so the scores are the page's), and catch weight's
  # correlation with the count.
  "information-leakage.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows(
      dplyr::mutate(fit_forest(honest, train, test), model = "random"),
      dplyr::mutate(fit_forest(update(honest, ~ . + catch_weight_kg), train, test),
                    model = "catch weight"),
      dplyr::mutate(fit_forest(honest, training(grouped), testing(grouped)),
                    model = "grouped")) |>
      tidyr::pivot_wider(names_from = .metric, values_from = .estimate)), dir, "leakage")
    write(with(env, tibble::tibble(
      correlation = cor(survey$abundance, survey$catch_weight_kg))), dir, "catch-weight")
    write(with(env, dplyr::bind_rows(
      evaluate(best_ten(fake), "all rows"),
      evaluate(best_ten(ftrain), "training rows"))), dir, "selection")
  }
)
