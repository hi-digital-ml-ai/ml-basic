# Numbers for the interpretation video's Manim scenes, taken from the objects each
# page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().
# Single numbers the narration speaks go into a "<page>-numbers" table of name and
# value, so a scene can show the page's own value.

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))
numbers <- function(...) tibble::tibble(name = names(c(...)), value = unname(c(...)))

exports <- list(
  # Scene 5: each input's rise in test RMSE when shuffled, and the RMSE before.
  # Scene 18: the same with the forest fitted without temperature.
  "feature-importance.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows("all six" = all_six, "without temperature" = without,
                                     .id = "forest")), dir, "importance")
    write(with(env, numbers(rmse = before_all, rmse_without = errors$rmse[2])),
          dir, "feature-importance-numbers")
  },

  # Scene 10: the forest's partial dependence on temperature.
  "partial-effects.qmd" = function(env, dir) {
    write(with(env, partial$temperature_c), dir, "partial")
  },

  # Scenes 12 and 15: the forest's predictions at the training stations, whose average
  # starts every explanation, and the chosen station's inputs and SHAP values.
  "explaining-one-prediction.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(.pred = predict(forest, train)$.pred)), dir, "train-predictions")
    write(with(env, tibble::tibble(input = inputs, value = shown(chosen[1, ]),
                                   shap = explained$S[1, ])), dir, "shap")
    write(with(env, numbers(average = explained$baseline, prediction = chosen$.pred[1])),
          dir, "explaining-one-prediction-numbers")
  }
)
