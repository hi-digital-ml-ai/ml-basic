# Numbers for the §5 Manim scenes, taken from the objects each page computed.
# Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 2–4 and 6–11: the five models, training and test RMSE, and the
  # predict-the-mean line.
  "training-versus-new-data.qmd" = function(env, dir) {
    table <- with(env, dplyr::mutate(results[c("model", "training", "test")],
                                     baseline = baseline))
    write(table, dir, "five-models")
  },

  # Scenes 18–22: the U-shaped curve, with its baseline and best leaf count.
  "underfitting-and-overfitting.qmd" = function(env, dir) {
    table <- with(env, dplyr::mutate(sweep[c("leaves", "training", "test")],
                                     baseline = baseline, best_leaves = best$leaves))
    write(table, dir, "u-curve")

    # Scenes 15–17: the three one-predictor trees, taken from the page's own plots.
    fits <- list(under = list(maxdepth = 1), right = list(minbucket = 45),
                 over = list(minbucket = 1))
    for (name in names(fits)) {
      plot <- do.call(env$step_plot, c(list(name), fits[[name]]))
      leaves <- as.integer(sub(" .*", "", plot$labels$subtitle))
      write(dplyr::mutate(plot$layers[[2]]$data, leaves = leaves), dir, paste0("fit-", name))
    }
    write(env$one_d_train[c("depth_m", "abundance")], dir, "fit-points")
  },

  # Scenes 32–35: bias², variance and the irreducible noise, by minbucket.
  "bias-variance.qmd" = function(env, dir) {
    table <- with(env, dplyr::mutate(decomposition, irreducible = irreducible))
    write(dplyr::rename(table, bias2 = `bias²`, total = `bias² + variance`), dir, "decomposition")
  },

  # Scenes 45–46: which grid cell each of the forty validation splits chose.
  "hyperparameter-selection.qmd" = function(env, dir) {
    write(with(env, winners[c("replicate", "tree_depth", "min_n", "winning_rmse")]),
          dir, "winners")
  },

  # Scenes 26, 27 and 50: columns of noise, training R² and test RMSE, and the largest
  # observed catch, which the page's figure caption compares the RMSE with.
  "model-complexity.qmd" = function(env, dir) {
    table <- with(env, dplyr::transmute(noise_results,
                                        noise_columns = `noise columns`,
                                        training_r2   = `training R²`,
                                        test_rmse     = `test RMSE`,
                                        stations      = nrow(train),
                                        largest_catch = max(d$abundance)))
    write(table, dir, "noise-columns")
  },

  # Scenes 37–38: least squares, predicting the mean and ridge, with the page's own
  # functions on the page's own split.
  "regularisation.qmd" = function(env, dir) {
    table <- with(env, tibble::tibble(
      method     = c("Least squares", "Predict the mean", "Ridge"),
      rmse       = c(rmse_of(y_test, cbind(1, X_test) %*% coef(ols)),
                     rmse_of(y_test, mean(y_train)),
                     best_glmnet(0)$`test RMSE`),
      predictors = ncol(X),
      stations   = length(y_train)))
    write(table, dir, "ridge-bars")

    # Scenes 39–40: how often lasso kept each term over 100 resampled fits.
    write(with(env, frequency), dir, "lasso-stability")
  }
)
