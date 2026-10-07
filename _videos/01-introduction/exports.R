# Numbers for the introduction video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # The first five stations as the page prints them; the 15 stations nearest the
  # mid-depth new station, found on the classifier's own scaled inputs, with the
  # classifier's chance of presence; and the clustered stations with the names the
  # page gives the groups.
  "types-of-learning.qmd" = function(env, dir) {
    write(with(env, head(dplyr::select(survey, temperature_c, salinity_psu, depth_m, abundance,
                                       present), 5)), dir, "survey-head")
    neighbours <- with(env, {
      rec    <- workflows::extract_recipe(classifier)
      inputs <- c("temperature_c", "salinity_psu", "depth_m")
      scaled <- as.matrix(recipes::bake(rec, survey)[inputs])
      target <- as.matrix(recipes::bake(rec, new_stations[2, ])[inputs])
      distance <- sqrt(colSums((t(scaled) - as.vector(target))^2))
      dplyr::mutate(dplyr::select(survey, depth_m, temperature_c, present),
                    neighbour = rank(distance, ties.method = "first") <= 15)
    })
    write(neighbours, dir, "neighbours")
    write(with(env, dplyr::bind_cols(
      dplyr::select(new_stations, station, depth_m, temperature_c),
      predict(classifier, new_stations, type = "prob")[".pred_yes"]
    )), dir, "new-stations")
    write(with(env, dplyr::select(clustered, depth_m, temperature_c, group)), dir, "clusters")
  },

  # The training stations and the two models' predictions across temperature, as
  # @fig-shapes draws them; the RMSE built by hand from the tree's misses; and the
  # test RMSE of each model beside the baseline, predicting the average.
  "prediction-and-explanation.qmd" = function(env, dir) {
    write(with(env, dplyr::select(train, temperature_c, abundance)), dir, "train-points")
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "shapes")
    write(with(env, head(misses, 5)), dir, "misses")
    write(with(env, tibble::tibble(stations = nrow(misses), mean_squared = mean(misses$squared),
                                   rmse = sqrt(mean(misses$squared)))), dir, "rmse-steps")
    write(with(env, tibble::tibble(
      model = c("predicting the average", "linear regression", "decision tree"),
      rmse  = test_rmse$test_rmse
    )), dir, "test-rmse")
  }
)
