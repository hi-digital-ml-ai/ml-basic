# Numbers for the supervised learning video's Manim scenes, taken from the objects each
# page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # The count's shape: stations per count, and the summary the prose quotes.
  "regression-and-classification.qmd" = function(env, dir) {
    write(with(env, dplyr::count(survey, abundance)), dir, "histogram")
    write(with(env, tibble::tibble(count_mean, count_var, zero_pct)), dir, "count-shape")
  },

  # The curve's temperature optimum, and its negative predictions on the test sites.
  "linear-and-polynomial-regression.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(optimum, test_stations = nrow(test))), dir, "optimum")
    write(with(env, scores), dir, "line-curve-scores")
  },

  # The three curves across temperature, the multipliers of both count models, and
  # the spread ratio.
  "count-regression.qmd" = function(env, dir) {
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "count-curves")
    write(with(env, dplyr::bind_rows(poisson = poisson_table, negbin = nb_table, .id = "fit")),
          dir, "multipliers")
    write(with(env, tibble::tibble(spread_ratio, theta = nb_fit$theta, wider)), dir, "spread")
    write(with(env, scores), dir, "count-scores")
  },

  # The probability curve, the training stations it was fitted to, and the thresholds.
  "logistic-regression.qmd" = function(env, dir) {
    write(with(env, dplyr::select(augment(logistic_fit, grid), temperature_c, .pred_yes)),
          dir, "logistic-curve")
    write(with(env, dplyr::transmute(train, temperature_c,
                                     present = as.integer(present == "yes"))), dir, "logistic-points")
    write(with(env, thresholds), dir, "thresholds")
  },

  # The depth-3 tree's nodes, its steps against the Poisson curve, and the depths.
  "decision-trees.qmd" = function(env, dir) {
    write(with(env, dplyr::select(nodes, node, var, n, yval, cut)), dir, "tree-nodes")
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "tree-steps")
    write(with(env, tibble::tibble(low = temp_range[1], high = temp_range[2])), dir, "tree-range")
    write(with(env, depths), dir, "depths")
  },

  # The six first questions, the scores by number of trees, thirty of the forest's
  # trees with their average, and the four models on the test sites.
  "forests-and-boosting.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(question = first_questions, threshold = thresholds)),
          dir, "first-questions")
    write(with(env, dplyr::bind_rows(forest = forest_scores, boosting = boost_scores,
                                     .id = "model")), dir, "tree-counts")
    write(with(env, trees_long), dir, "forest-trees")
    write(with(env, dplyr::select(augment(forest_fit, grid), temperature_c, .pred)),
          dir, "forest-average")
    write(with(env, tibble::tibble(model = names(test_rmse), rmse = unname(test_rmse),
                                   depth = best_depth, trees = best_boost)), dir, "ensembles-test")
  },

  # The seven models on the validation and test sites, and the three curves beyond
  # the sampled temperatures.
  "choosing-a-method.qmd" = function(env, dir) {
    write(with(env, results), dir, "comparison")
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "extrapolate")
    write(with(env, tibble::tibble(low = temp_range[1], high = temp_range[2])), dir, "extrapolate-range")
  }
)
