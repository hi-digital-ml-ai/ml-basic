# Numbers for the supervised learning video's Manim scenes, taken from the objects each
# page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().
# Tables a page prints without keeping are rerun with the page's own functions and
# objects; nothing here fits a model the page does not.

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # The count as the page summarises it, its histogram, and what "present" hides.
  "regression-and-classification.qmd" = function(env, dir) {
    write(with(env, dplyr::summarise(survey,
      stations = dplyr::n(), mean_count = round(mean(abundance), 2),
      variance = round(var(abundance), 2), zeros = sum(abundance == 0),
      zero_pct = round(100 * mean(abundance == 0), 1))), dir, "count-summary")
    write(with(env, dplyr::count(survey, abundance, name = "stations")), dir, "count-histogram")
    write(with(env, survey |> dplyr::filter(abundance > 0) |>
      dplyr::summarise(present = dplyr::n(), smallest = min(abundance),
                       largest = max(abundance), median = median(abundance))), dir, "present")
  },

  # The three models on 200 test stations, their temperature curves (the figure's own
  # `curves`), the deviance ratio and the negative binomial's AIC.
  "linear-and-polynomial-regression.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows(
      evaluate(linear_reg(), base_recipe, "Linear"),
      evaluate(linear_reg(), curved_recipe, "Polynomial"),
      evaluate(poisson_reg() |> set_engine("glm"), curved_recipe, "Poisson + polynomial")) |>
      dplyr::mutate(test_stations = nrow(test))), dir, "three-models")
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "curves")
    write(with(env, tibble::tibble(
      ratio = round(fitted_glm$deviance / fitted_glm$df.residual, 2),
      theta = round(nb_fit$theta, 3),
      aic_poisson = round(AIC(fitted_glm)), aic_negbin = round(AIC(nb_fit)))), dir, "dispersion")
  },

  # The rare species: the split, every test prediction, the page's scores and threshold
  # table, the depth odds ratio, and prevalence by depth band.
  "logistic-regression.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      training = nrow(train), testing = nrow(test),
      present_in_test = sum(test$rare_species == "yes"),
      accuracy = round(accuracy(predictions, truth = rare_species, estimate = .pred_class)$.estimate, 4),
      always_absent = round(mean(test$rare_species == "no"), 4),
      predicted_present = sum(predictions$.pred_class == "yes"),
      roc_auc = round(roc_auc(predictions, truth = rare_species, .pred_yes)$.estimate, 3),
      highest = round(max(predictions$.pred_yes), 3))), dir, "rare-scores")
    write(with(env, dplyr::select(predictions, .pred_yes, rare_species)), dir, "rare-predictions")
    write(with(env, thresholds), dir, "thresholds")
    write(with(env, tidy(logistic_fit, exponentiate = TRUE) |>
      dplyr::filter(term == "depth_m") |>
      dplyr::transmute(term, odds_ratio = round(estimate, 3))), dir, "depth-odds")
    write(with(env, survey |>
      dplyr::mutate(depth_band = cut(depth_m, breaks = c(0, 50, 100, 150, 200))) |>
      dplyr::group_by(depth_band) |>
      dplyr::summarise(stations = dplyr::n(), present = sum(rare_species == "yes"),
                       prevalence = round(mean(rare_species == "yes"), 3))), dir, "depth-bands")
  },

  # The depth-3 tree's nodes (rpart's own split labels), the four models' training and
  # test error, and the two capacity curves the figure draws.
  "trees-forests-boosting.qmd" = function(env, dir) {
    write(with(env, {
      engine <- extract_fit_engine(tree_fit)
      tibble::tibble(node = as.integer(rownames(engine$frame)), var = as.character(engine$frame$var),
                     n = engine$frame$n, prediction = round(engine$frame$yval, 1),
                     rule = labels(engine))
    }), dir, "tree")
    write(with(env, dplyr::bind_rows(
      evaluate(decision_tree(tree_depth = 3, min_n = 5) |> set_engine("rpart") |>
                 set_mode("regression"), base_recipe, "Tree (depth 3)"),
      evaluate(decision_tree() |> set_engine("rpart") |> set_mode("regression"),
               base_recipe, "Tree (defaults)"),
      evaluate(rand_forest(trees = 500) |> set_engine("ranger", seed = 9) |>
                 set_mode("regression"), base_recipe, "Random forest (500)"),
      evaluate(boost_tree(trees = 500, learn_rate = 0.1, tree_depth = 4) |>
                 set_engine("xgboost") |> set_mode("regression"),
               dummied_recipe, "Boosting (500 trees)")) |>
      dplyr::mutate(training_stations = nrow(train))), dir, "four-models")
    write(with(env, dplyr::bind_rows(dplyr::mutate(boosting_curve, method = "boosting"),
                                     dplyr::mutate(depth_curve, method = "tree"))), dir, "capacity")
  },

  # The ten models, as the page ranks them.
  "choosing-a-method.qmd" = function(env, dir) {
    write(with(env, results), dir, "ten-models")
  }
)
