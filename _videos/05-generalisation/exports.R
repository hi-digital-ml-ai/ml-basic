# Numbers for the generalisation video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().
# Nothing here fits a model the page does not.

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 2–6: the five models on their fitting stations and on new sites, and the
  # error of predicting the average.
  "training-versus-new-data.qmd" = function(env, dir) {
    write(with(env, dplyr::filter(results, model != "Predict the average") |>
                      dplyr::transmute(model, training, new, baseline = baseline)),
          dir, "five-models")
  },

  # Scenes 12–15: the three one-input trees with the stations they were fitted to, and
  # the sweep from rigid to flexible.
  "underfitting-and-overfitting.qmd" = function(env, dir) {
    write(with(env, dplyr::select(train, temperature = temperature_c, abundance) |>
                      tidyr::drop_na()), dir, "temperature-points")
    write(with(env, dplyr::transmute(lines, min_n, temperature = temperature_c, prediction = .pred,
                                     leaves = one_leaves[match(min_n, three_sizes)])),
          dir, "three-trees")
    write(with(env, dplyr::transmute(sweep, min_n, leaves, training, new,
                                     baseline = baseline, best_leaves = best$leaves)),
          dir, "u-curve")
  },

  # Scenes 18–20: bias², variance and noise by tree size, the noise's share of the best
  # tree's error, and a single tree against a forest of the same trees.
  "bias-variance.qmd" = function(env, dir) {
    write(with(env, dplyr::transmute(parts, min_n, leaves, bias_squared, variance, noise,
                                     total, best_min_n = best$min_n, noise_share = noise_share)),
          dir, "parts")
    write(with(env, dplyr::select(tree_and_forest, model, bias_squared, variance)), dir, "tree-and-forest")
  },

  # Scene 24: error on new sites against λ, and the models without a penalty.
  "regularisation.qmd" = function(env, dir) {
    write(with(env, dplyr::filter(sweep, model %in% c("Ridge regression", "Lasso"))),
          dir, "lambda-curves")
    write(with(env, dplyr::select(best, model, lambda, new)), dir, "lambda-best")
  },

  # Scenes 26, 28 and 29: forty runs of each way of choosing, and the test sites' score.
  "hyperparameter-selection.qmd" = function(env, dir) {
    write(with(env, dplyr::select(repeats, method, min_n, claimed)), dir, "repeats")
    write(with(env, tibble::tibble(test_tree, test_average, test_lead = test_average - test_tree,
                                   cv_lead = lead)), dir, "test-once")
  },

  # Scene 33: R² on the fitting stations and the error on new sites, as random columns
  # are added.
  "model-complexity.qmd" = function(env, dir) {
    write(with(env, dplyr::transmute(noise_sweep, noise, r_squared, new, baseline = baseline)),
          dir, "random-columns")
  }
)
