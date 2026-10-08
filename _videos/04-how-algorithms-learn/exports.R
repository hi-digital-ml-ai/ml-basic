# Numbers for the how-algorithms-learn video's Manim scenes, taken from the objects
# each page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().
# Tables a page prints without keeping are rerun with the page's own functions and
# objects; nothing here fits a model the page does not.

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

# The page's grid of the objective as contour lines, for the scenes to draw.
contours <- function(grid, x, y, levels) {
  xs <- sort(unique(grid[[x]])); ys <- sort(unique(grid[[y]]))
  z <- matrix(grid$mse, nrow = length(xs), byrow = TRUE)   # expand_grid varies y fastest
  lines <- grDevices::contourLines(xs, ys, z, levels = levels)
  dplyr::bind_rows(lapply(seq_along(lines), \(i)
    tibble::tibble(line = i, level = lines[[i]]$level, x = lines[[i]]$x, y = lines[[i]]$y)))
}

exports <- list(
  # The stations and the two fitted lines, the worst 5%'s share of each total, and the
  # slopes without the largest catch.
  "loss-functions.qmd" = function(env, dir) {
    write(with(env, dplyr::select(d, chlorophyll = chlorophyll_mg_m3, abundance)), dir, "stations")
    write(with(env, coefs), dir, "two-losses")
    write(with(env, tibble::tibble(
      squared_share = share[["squared"]], absolute_share = share[["absolute"]],
      stations = nrow(d), worst_stations = length(worst))), dir, "error-share")
    write(with(env, dplyr::transmute(slopes, loss, all = `all stations`,
                                     minus_one = `largest catch removed`, change,
                                     largest_catch = max(d$abundance))), dir, "drop-one")
  },

  # The objective's contours, the walks drawn on the page, the steps each rate needs,
  # and the optimum.
  "gradient-descent.qmd" = function(env, dir) {
    write(with(env, contours(grid, "chlorophyll", "depth",
      best_mse + c(0.05, 0.2, 0.5, 1, 2, 3.5, 5.5, 8, 11, 15))), dir, "contours")
    write(with(env, dplyr::mutate(paths, learning_rate = as.numeric(as.character(`learning rate`)),
                                  step = dplyr::row_number() - 1, .by = `learning rate`) |>
      dplyr::select(learning_rate, step, chlorophyll, depth)), dir, "paths")
    write(with(env, dplyr::transmute(rates, learning_rate = `learning rate`,
                                     mse_40 = `MSE after 40 steps`, steps = `steps to arrive`)),
          dir, "rates")
    write(with(env, tibble::tibble(optimum_chlorophyll = optimum[1], optimum_depth = optimum[2])),
          dir, "descent")
  },

  # The forty-station fit, the prior's figure values, and the three test errors the
  # page compares.
  "map-and-priors.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(prior_sd = prior_sds, peak = peaks)), dir, "prior-peaks")
    write(with(env, tibble::tibble(
      training = nrow(X_train), testing = nrow(X_test), inputs = ncol(X_train),
      b_temp, se_temp, b_temp2,
      mean_rmse = mean_only, mle_rmse = curve$test[1], map_rmse = map_test)), dir, "map-summary")
  },

  # The fit stopped after two steps, against the finished one.
  "reading-a-fit.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      fit = c("two steps", "left to finish"),
      converged = c(stopped_early$converged, full_fit$converged),
      chlorophyll = c(coef(stopped_early)[2], coef(full_fit)[2]), off = chl_off)), dir, "truncated")
  }
)
