# Numbers for the validation video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 7–17: forty single splits against forty cross-validations, the hundred
  # searched candidates, and the nested comparison.
  "cross-validation.qmd" = function(env, dir) {
    write(with(env, estimates), dir, "split-estimates")
    write(with(env, tibble::tibble(
      candidate = seq_along(candidates), rmse = searched,
      noise = purrr::map_int(candidates, \(v) sum(grepl("noise", v))),
      winner = seq_along(candidates) == which.min(searched))), dir, "search")
    write(with(env, nested), dir, "nested")
  },

  # Scenes 23–30: the stations, every scheme's pooled score and separation, and the
  # forecasting check.
  "spatial-and-temporal-cv.qmd" = function(env, dir) {
    write(with(env, dplyr::select(d, site_id, survey_year, longitude, latitude)),
          dir, "stations")
    write(with(env, comparison), dir, "schemes")
    write(with(env, forecast_check), dir, "forecast")
  },

  # Scenes 2–3 and 33–35: the five models' scores, the negative binomial's
  # out-of-fold errors, and the three measures under rescaled predictions.
  "regression-metrics.qmd" = function(env, dir) {
    write(with(env, scores), dir, "regression-scores")
    write(with(env, nb), dir, "nb-errors")
    write(with(env, dplyr::select(curves, scale, measure, value, relative)), dir, "scaling")
  },

  # Scenes 36–39: the confusion matrix at 0.5, the ten measures, and the rule that
  # flags every station.
  "classification-metrics.qmd" = function(env, dir) {
    write(with(env, tibble::as_tibble(conf_mat(at_threshold(logistic, 0.5), truth, estimate)$table)),
          dir, "confusion")
    write(with(env, dplyr::select(class_measures(at_threshold(logistic, 0.5),
                                                 truth = truth, estimate = estimate),
                                  measure = .metric, value = .estimate)),
          dir, "class-measures")
    write(with(env, tibble::tibble(
      rule = c("flag every station", "logistic model"),
      f1 = c(f_meas_vec(always_present$truth, always_present$estimate),
             f_meas_vec(logistic$truth, at_threshold(logistic, 0.5)$estimate)))),
      dir, "flag-all")
  },

  # Scenes 18–21: the bootstrap interval, the per-fold scores, and the unpaired and
  # paired intervals on the difference.
  "uncertainty-and-stability.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      estimate = rmse_vec(pooled_glm$obs, pooled_glm$pred),
      lower = quantile(boot$rmse, 0.025), upper = quantile(boot$rmse, 0.975))),
      dir, "interval")
    write(with(env, per_fold), dir, "per-fold")
    write(with(env, tibble::tibble(
      comparison = c("unpaired", "paired"),
      difference = c(diff(rev(unpaired$estimate)), paired$estimate),
      lower = c(unpaired$conf.int[1], paired$conf.int[1]),
      upper = c(unpaired$conf.int[2], paired$conf.int[2]))), dir, "paired")
  },

  # Scenes 2–4, 41–46 and 49: the three objectives, the shortlist benchmarks, and the
  # expected cost of each threshold.
  "choosing-a-metric.qmd" = function(env, dir) {
    write(with(env, dplyr::rename(objectives, rmse = `mapping: RMSE`,
                                  total_ratio = `stock total: pred / obs`,
                                  caught = `targeting: caught in 50`,
                                  share = `share of a perfect shortlist`)),
          dir, "objectives")
    write(with(env, tibble::tibble(total = sum(observed), perfect = perfect,
                                   random = budget * mean(observed))),
          dir, "benchmarks")
    write(with(env, dplyr::select(cost_table, k = `a wasted dive costs`,
                                  cheapest = `cheapest threshold`, cost_there = `cost there`,
                                  cost_half = `cost at 0.5`)),
          dir, "cost-table")
    write(with(env, cost_curves), dir, "cost-curves")
  }
)
