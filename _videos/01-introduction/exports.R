# Numbers for the introduction video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # The stations, the split, the linear model's coefficients, the training data with
  # the figure's two lines (geom_smooth's lm and loess, span 0.6), and the error table.
  "what-is-machine-learning.qmd" = function(env, dir) {
    write(with(env, dplyr::select(survey, longitude, latitude)), dir, "stations")
    write(with(env, tibble::tibble(train = nrow(train), test = nrow(test))), dir, "split")
    write(with(env, dplyr::select(tidy(lm_fit, conf.int = TRUE), term, estimate, conf.low,
                                  conf.high, p.value)), dir, "coefficients")
    write(with(env, dplyr::select(train, temperature_c, abundance)), dir, "train-points")
    write(with(env, {
      grid <- data.frame(temperature_c = seq(min(train$temperature_c), max(train$temperature_c),
                                             length.out = 120))
      tibble::tibble(temperature_c = grid$temperature_c,
                     straight = predict(lm(abundance ~ temperature_c, train), grid),
                     smooth = predict(loess(abundance ~ temperature_c, train, span = 0.6), grid))
    }), dir, "temperature-lines")
    write(with(env, dplyr::bind_rows(
      dplyr::bind_cols(set = "training", performance(lm_fit, train, "linear")),
      dplyr::bind_cols(set = "training", performance(rf_fit, train, "forest")),
      dplyr::bind_cols(set = "test",     performance(lm_fit, test,  "linear")),
      dplyr::bind_cols(set = "test",     performance(rf_fit, test,  "forest")))), dir, "errors")
  },

  # The four models' test errors, the curved model's temperature terms, and its
  # temperature response with the fitted optimum. The `fit-four` chunk prints its table
  # without keeping it, so the scores are recomputed here from the page's own fits.
  "prediction-and-explanation.qmd" = function(env, dir) {
    write(with(env, purrr::list_rbind(purrr::imap(fits, \(fit, name)
      tibble::tibble(model = name, rmse = rmse_vec(test$abundance, predict(fit, test)$.pred))))),
      dir, "four-models")
    write(with(env, dplyr::filter(tidy(fits[["Linear model, with curves"]]), grepl("temperature", term))),
          dir, "temperature-terms")
    write(with(env, dplyr::mutate(dplyr::select(grid, temperature_c, predicted),
                                  optimum = fitted_optimum)), dir, "optimum")
  },

  # Presence: the confusion matrix (from which accuracy and the always-present baseline
  # follow), and the clustered stations with their habitat names.
  "types-of-learning.qmd" = function(env, dir) {
    write(with(env, dplyr::count(predictions, truth = present, prediction = .pred_class)), dir, "presence")
    write(with(env, dplyr::select(clustered, depth_m, temperature_c, chlorophyll_mg_m3, abundance, habitat)),
          dir, "clusters")
  }
)
