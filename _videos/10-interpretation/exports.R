# Numbers for the interpretation video's Manim scenes, taken from the objects each
# page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().
# Two pages print a table without keeping it (the shift experiment, the gear
# bias); those calls are repeated here with the page's own functions and seeds.

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Impurity and permutation importance with the noise columns, and the eight splits.
  "feature-importance.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(term = names(impurity), importance = impurity / max(impurity))),
          dir, "impurity")
    write(with(env, importance), dir, "permutation")
    write(with(env, dplyr::select(repeated, variable, split, rank, increase, noise_ceiling)),
          dir, "splits")
    write(with(env, tibble::tibble(train = nrow(train_set), test = nrow(test_set))), dir, "halves")
  },

  # The true, forest and GLM partial dependence, the GLM's terms and the stations.
  "partial-effects.qmd" = function(env, dir) {
    write(with(env, depth_curves), dir, "depth-curves")
    write(with(env, temperature_curves), dir, "temperature-curves")
    write(with(env, tibble::tibble(term = c("depth, linear", "depth, quadratic",
                                            "temperature, linear", "temperature, quadratic"),
                                   estimate = coef(correct_form)[2:5],
                                   se = sqrt(diag(vcov(correct_form)))[2:5],
                                   truth = c(2 * 0.55 * 80 / 3600, -0.55 / 3600,
                                             2 * 0.60 * 9 / 9, -0.60 / 9),
                                   p = 2 * pnorm(-abs(estimate / se)))), dir, "glm-terms")
    write(with(env, dplyr::select(modelling, depth_m, temperature_c)), dir, "stations")
  },

  # The seven models on the same folds, and the GAM's depth smooth against the truth.
  "black-box-or-not.qmd" = function(env, dir) {
    write(with(env, purrr::imap_dfr(results, \(scored, name)
      tibble::tibble(model = name, rmse = rmse_vec(scored$truth, scored$prediction)))),
      dir, "model-scores")
    write(with(env, smooth_frame("depth_m", \(d) -0.55 * ((d - 80) / 60)^2)), dir, "gam-depth")
  },

  # Coverage of each interval, the bands behind the figure, and the two shifts.
  "communicating-uncertainty.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows(
      coverage(mean_lower, mean_upper, "mean"),
      coverage(new_lower, new_upper, "new count"),
      coverage(predicted - 1.96 * in_sample_rmse, predicted + 1.96 * in_sample_rmse, "in-sample rmse"),
      coverage(predicted - 1.96 * held_out_rmse, predicted + 1.96 * held_out_rmse, "held-out rmse"),
      coverage(intervals$.pred_lower, intervals$.pred_upper, "conformal")) |>
      dplyr::mutate(in_sample_rmse = in_sample_rmse, held_out_rmse = held_out_rmse,
                    lowest = min(intervals$.pred_lower), test = nrow(test))), dir, "intervals")
    write(with(env, tibble::tibble(expected = as.numeric(expected), observed = test$abundance,
                                   mean_lower = as.numeric(mean_lower), mean_upper = as.numeric(mean_upper),
                                   new_lower = as.numeric(new_lower), new_upper = as.numeric(new_upper),
                                   conformal_lower = gam_bands$.pred_lower,
                                   conformal_upper = gam_bands$.pred_upper)), dir, "interval-bands")
    write(with(env, dplyr::bind_rows(
      shift_experiment("depth", \(x) x$depth_m < 50 | x$depth_m > 120,
                       \(x) x$depth_m >= 60 & x$depth_m <= 100),
      shift_experiment("chlorophyll", \(x) x$chlorophyll_mg_m3 < 2,
                       \(x) x$chlorophyll_mg_m3 >= 3))), dir, "shift")
  },

  # The gear that halves the catch on rock, against the survey as recorded.
  "from-model-to-claim.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows(compare(modelling, "as recorded"),
                                     compare(biased, "gear halves the catch on rock"))),
          dir, "rock-bias")
  },

  # Sixteen runs: the forest's seed varied, then the split.
  "reproducibility.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows(
      dplyr::mutate(model_randomness, varying = "seed"),
      dplyr::mutate(split_randomness, varying = "split"))), dir, "seed-split")
  }
)
