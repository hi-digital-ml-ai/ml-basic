# Numbers for the §5 Manim scenes, taken from the objects each page computed.
# Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 1–2 and 5–7: the five models, training and test RMSE, and the
  # predict-the-mean line.
  "training-versus-new-data.qmd" = function(env, dir) {
    table <- with(env, dplyr::mutate(results[c("model", "training", "test")],
                                     baseline = baseline))
    write(table, dir, "five-models")
  },

  # Scenes 12–14: the U-shaped curve, with its baseline and best leaf count.
  "underfitting-and-overfitting.qmd" = function(env, dir) {
    table <- with(env, dplyr::mutate(sweep[c("leaves", "training", "test")],
                                     baseline = baseline, best_leaves = best$leaves))
    write(table, dir, "u-curve")
  },

  # Scenes 17–18: columns of noise, training R² and test RMSE, and the largest
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

  # Scene 27: least squares, predicting the mean and ridge, with the page's own
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
  }
)
