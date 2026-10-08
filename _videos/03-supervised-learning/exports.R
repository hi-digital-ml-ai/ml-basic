# Numbers for the supervised learning video's Manim scenes, taken from the objects each
# page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

# The pages' grid for curves across temperature: the other inputs at typical values.
temperature_grid <- function(train, from, to, n = 200) {
  tibble::tibble(
    temperature_c     = seq(from, to, length.out = n),
    depth_m           = median(train$depth_m, na.rm = TRUE),
    chlorophyll_mg_m3 = median(train$chlorophyll_mg_m3, na.rm = TRUE),
    salinity_psu      = median(train$salinity_psu, na.rm = TRUE),
    substrate         = factor("sand", levels = levels(train$substrate)),
    season            = factor("summer", levels = levels(train$season))
  )
}

exports <- list(
  # The line and the curve across temperature, the curve's peak, and its negative
  # predictions on the test sites.
  "linear-and-polynomial-regression.qmd" = function(env, dir) {
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "line-curves")
    write(with(env, tibble::tibble(optimum, test_stations = nrow(test))), dir, "optimum")
    write(with(env, scores), dir, "line-curve-scores")
  },

  # The survey's counts, Poisson regression across temperature and its multipliers.
  "count-regression.qmd" = function(env, dir) {
    write(with(env, dplyr::count(survey, abundance)), dir, "histogram")
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "count-curves")
    write(with(env, multipliers), dir, "multipliers")
  },

  # The probability curve, the training stations it was fitted to, and the thresholds.
  "logistic-regression.qmd" = function(env, dir) {
    write(with(env, dplyr::select(augment(logistic_fit, grid), temperature_c, .pred_yes)),
          dir, "logistic-curve")
    write(with(env, dplyr::transmute(train, temperature_c,
                                     present = as.integer(present == "yes"))), dir, "logistic-points")
    write(with(env, thresholds), dir, "thresholds")
  },

  # The error against the number of neighbours.
  "nearest-neighbours.qmd" = function(env, dir) {
    write(with(env, neighbours), dir, "neighbours")
  },

  # The depth-3 tree's nodes and the error against depth.
  "decision-trees.qmd" = function(env, dir) {
    write(with(env, dplyr::select(nodes, node, var, n, yval, cut)), dir, "tree-nodes")
    write(with(env, depths), dir, "depths")
  },

  # The six first questions, the scores by number of trees, and thirty of the
  # page's 400-tree forest's trees with their average, across temperature.
  "forests-and-boosting.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(question = first_questions, threshold = thresholds)),
          dir, "first-questions")
    write(with(env, dplyr::bind_rows(forest = forest_scores, boosting = boost_scores,
                                     .id = "model")), dir, "tree-counts")
    # Outside with(): there, `grid` would find graphics::grid().
    grid <- temperature_grid(env$train, 0, 20)
    baked <- recipes::bake(workflows::extract_recipe(env$forest_fit), grid)
    every <- predict(workflows::extract_fit_engine(env$forest_fit), baked,
                     predict.all = TRUE)$predictions
    trees <- purrr::map(1:30, \(i) tibble::tibble(tree = i, temperature_c = grid$temperature_c,
                                                  .pred = every[, i])) |> purrr::list_rbind()
    write(trees, dir, "forest-trees")
    write(tibble::tibble(temperature_c = grid$temperature_c, .pred = rowMeans(every)),
          dir, "forest-average")
    write(with(env, tibble::tibble(low = min(train$temperature_c, na.rm = TRUE),
                                   high = max(train$temperature_c, na.rm = TRUE))), dir, "forest-range")
  },

  # The seven models on the validation and test sites, and the three curves beyond
  # the sampled temperatures.
  "choosing-a-method.qmd" = function(env, dir) {
    write(with(env, results), dir, "comparison")
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "extrapolate")
    write(with(env, tibble::tibble(low = temp_range[1], high = temp_range[2])), dir, "extrapolate-range")
  }
)
