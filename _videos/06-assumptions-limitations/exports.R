# Numbers for the §6 Manim scenes, taken from the objects each page computed.
# Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 8–13: visits per site, the effective sample size, and the naive and
  # cluster-robust standard errors and p-values.
  "independence-of-observations.qmd" = function(env, dir) {
    write(with(env, visits), dir, "visits")
    write(with(env, tibble::tibble(rows = nrow(d), sites = nrow(visits), icc = icc,
                                   design_effect = design_effect,
                                   effective = nrow(d) / design_effect)),
          dir, "effective")
    write(with(env, tibble::tibble(term = rownames(naive), naive_se = naive[, 2],
                                   cluster_se = cluster_se,
                                   naive_p = naive[, 4],
                                   cluster_p = 2 * pnorm(-abs(naive[, 1] / cluster_se)))),
          dir, "cluster-se")
  },

  # Scenes 14–21: the site residual map, and cross-validated R² under random and
  # spatially blocked folds.
  "spatial-and-temporal-dependence.qmd" = function(env, dir) {
    write(with(env, site_residuals), dir, "site-residuals")
    write(with(env, dplyr::select(dplyr::filter(comparison, .metric == "rsq"),
                                  model, scheme, r2 = mean)),
          dir, "cv-r2")
  },

  # Scenes 24–28: the fitted and true curves for temperature and depth, and the
  # three models' AIC.
  "linearity-and-nonlinearity.qmd" = function(env, dir) {
    write(with(env, dplyr::select(depth_curves, depth_m, fitted = Fitted, truth = Truth)),
          dir, "depth-curves")
    write(with(env, dplyr::select(temp_curves, temperature_c, fitted = Fitted, truth = Truth)),
          dir, "temperature-curves")
    write(with(env, tibble::tibble(
      model = c("Straight lines", "Quadratic terms", "Flexible curves"),
      aic   = c(AIC(linear), AIC(quadratic), AIC(smooth)))), dir, "aic")
  },

  # Scenes 30–34: the dispersion ratio, the simulated empty stations, and the
  # Poisson and negative-binomial standard errors and p-values.
  "distributional-assumptions.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      dispersion = sum(residuals(poisson_fit, "pearson")^2) / poisson_fit$df.residual,
      observed_zeros = sum(d$abundance == 0),
      poisson_zeros = mean(poisson_sims$zeros))), dir, "dispersion")
    write(with(env, dplyr::bind_rows(
      dplyr::mutate(poisson_sims, model = "Poisson"),
      dplyr::mutate(nb_sims, model = "Negative binomial"))), dir, "simulated-zeros")
    write(with(env, tibble::tibble(term = rownames(poisson_coefs),
                                   poisson_se = poisson_coefs[, 2], nb_se = nb_coefs[, 2],
                                   poisson_p = poisson_coefs[, 4], nb_p = nb_coefs[, 4])),
          dir, "poisson-se")
  },

  # Scenes 37–42 and 51: mean counts by depth band, each model's bias in range and
  # past the edge, and the stations for the novelty scatter.
  "sampling-and-extrapolation.qmd" = function(env, dir) {
    write(with(env, dplyr::mutate(both, band = as.character(band))), dir, "depth-bands")
    write(with(env, tibble::tibble(
      model = names(extrapolated),
      in_range = purrr::map_dbl(in_range, \(p) mean(p) / mean(shallow$true_mean[-inner]) - 1),
      extrapolated = purrr::map_dbl(extrapolated, \(p) mean(p) / mean(deep$true_mean) - 1))),
      dir, "bias")
    write(with(env, dplyr::bind_rows(
      dplyr::mutate(sampled, status = "Surveyed"),
      dplyr::mutate(unsampled, status = dplyr::case_when(
        univariate_ok & jointly_novel ~ "Inside every range, but novel",
        jointly_novel                 ~ "Outside a range",
        TRUE                          ~ "Covered")))), dir, "novelty")
  },

  # Scenes 2–4 and 43–48: the four recipes' metrics, the untouched model's
  # probabilities, its thresholds and its sensitivity-specificity curve.
  "class-imbalance.qmd" = function(env, dir) {
    write(with(env, tidyr::pivot_wider(dplyr::select(results, recipe, .metric, mean),
                                       names_from = .metric, values_from = mean)),
          dir, "imbalance-metrics")
    write(with(env, dplyr::select(untouched, .pred_yes, rare_species)), dir, "probabilities")
    write(with(env, threshold_table), dir, "thresholds")
    write(with(env, sweep), dir, "tradeoff")
  }
)
