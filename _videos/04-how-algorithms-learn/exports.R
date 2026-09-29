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
  # The three fitted lines over the stations, the worst 5%'s share of each total error,
  # and the slopes without the single largest catch.
  "loss-functions.qmd" = function(env, dir) {
    write(with(env, coefs), dir, "three-losses")
    write(with(env, dplyr::select(d, chlorophyll = chlorophyll_mg_m3, abundance)), dir, "stations")
    write(with(env, tibble::tibble(
      squared_share = sum(residuals[worst]^2) / sum(residuals^2),
      absolute_share = sum(abs(residuals[worst])) / sum(abs(residuals)),
      stations = length(y), worst_stations = length(worst))), dir, "error-share")
    write(with(env, tibble::tibble(
      loss = c("Squared error", "Absolute error"), largest_catch = max(y),
      all = c(coefs$slope[1], coefs$slope[2]),
      minus_one = c(fit_loss2(\(r) r^2)[2], fit_loss2(abs)[2]))), dir, "drop-one")
  },

  # The formula against lm(), the IRLS trace with its standing start, and the grid cost.
  "parameter-estimation.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      term = rownames(beta_hat), formula = drop(beta_hat),
      lm = coef(lm(abundance ~ chlorophyll_mg_m3 + depth_m + temperature_c, data = d3)))),
      dir, "closed-form")
    write(with(env, dplyr::bind_rows(
      tibble::tibble(iteration = 0, log_likelihood = log_likelihood(rep(0, ncol(Xb)))),
      dplyr::select(trace, iteration, log_likelihood))), dir, "irls")
  },

  # The objective's contours, the three walks, the stable limit, a divergent walk, the
  # conditioning, and the steps each walk needs. The page states the step counts in
  # prose; "arrived" is an MSE within 0.002 of the best, which gives all five of them.
  "gradient-descent.qmd" = function(env, dir) {
    write(with(env, contours(grid, "chlorophyll", "depth",
      min(grid$mse) + c(0.05, 0.2, 0.5, 1, 2, 3.5, 5.5, 8, 11, 15))), dir, "contours")
    write(with(env, dplyr::mutate(paths, learning_rate = as.numeric(as.character(`learning rate`))) |>
      dplyr::select(learning_rate, step, chlorophyll, depth)), dir, "paths")
    write(with(env, {
      mse <- \(M, b) mean((y - M %*% b)^2)
      best <- mse(X, optimum)
      limit <- \(M) 2 / max(eigen(2 / nrow(M) * t(M) %*% M)$values)
      steps <- function(M, rate) {
        b <- c(0, 0); k <- 0
        while (mse(M, b) - best > 0.002) {
          b <- b - rate * 2 / nrow(M) * drop(t(M) %*% (M %*% b - y)); k <- k + 1
        }
        k
      }
      diverged <- tail(gradient_descent(X, y, 0.80, 60), 1)
      tibble::tibble(
        optimum_chlorophyll = optimum[1], optimum_depth = optimum[2], best_mse = best,
        steps_002 = steps(X, 0.02), steps_03 = steps(X, 0.3), steps_072 = steps(X, 0.72),
        limit = limit(X), limit_unscaled = limit(centred_only),
        diverged_rate = 0.80, diverged_steps = 60,
        diverged_mse = mse(X, c(diverged$chlorophyll, diverged$depth)),
        condition = condition_number(X), condition_unscaled = condition_number(centred_only),
        steps_standardised = steps(X, 0.9 * limit(X)),
        steps_unscaled = steps(centred_only, 0.9 * limit(centred_only)),
        sd_depth = sd(d$depth_m), sd_chlorophyll = sd(d$chlorophyll_mg_m3))
    }), dir, "descent")
  },

  # Least squares as Gaussian maximum likelihood, and the three counts' joint likelihood.
  "maximum-likelihood.qmd" = function(env, dir) {
    write(with(env, {
      ls <- lm(abundance ~ chl_z, data = d)
      tibble::tibble(method = c("Maximum likelihood", "Least squares"),
                     intercept = c(mle$par[1], coef(ls)[1]), slope = c(mle$par[2], coef(ls)[2]),
                     sigma = c(exp(mle$par[3]), sqrt(mean(residuals(ls)^2))))
    }), dir, "normal-mle")
    write(with(env, tibble::tibble(count = counts)), dir, "counts")
  },

  # The forty-station fit: the coefficients three ways, the prior's figure values, the
  # error curves against λ, and the three test errors the page compares.
  "map-and-priors.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(term = colnames(X_train), mle = ridge_closed_form(0),
                                   map = map_fit$par, ridge = ridge_closed_form(sigma^2 / tau^2))),
          dir, "coefficients")
    write(with(env, dplyr::select(curve, lambda, train, test)), dir, "lambda-curve")
    write(with(env, tibble::tibble(
      training = nrow(X_train), testing = nrow(X_test), predictors = ncol(X_train),
      b_hat = b_hat, se = se, sigma = sigma, tau = tau, lambda = sigma^2 / tau^2,
      mean_rmse = sqrt(mean(y_test^2)), mle_rmse = rmse(ridge_closed_form(0), X_test, y_test),
      map_rmse = rmse(map_fit$par, X_test, y_test))), dir, "map-summary")
  },

  # The truncated fit, the separated fit, and the unseeded forests and k-means starts.
  "reading-a-fit.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      fit = c("maxit = 2", "run to convergence"),
      converged = c(stopped_early$converged, full_fit$converged),
      iterations = c(stopped_early$iter, full_fit$iter),
      chlorophyll = c(coef(stopped_early)[2], coef(full_fit)[2]))), dir, "truncated")
    write(with(env, tibble::tibble(
      estimate = summary(separated)$coefficients[2, 1], se = summary(separated)$coefficients[2, 2],
      p = summary(separated)$coefficients[2, 4], converged = separated$converged,
      iterations = separated$iter)), dir, "separation")
    write(with(env, tibble::tibble(run = seq_along(unseeded), rmse = unseeded)), dir, "forest-runs")
    write(with(env, tibble::tibble(start = seq_along(single_starts), withinss = single_starts)),
          dir, "kmeans-starts")
  }
)
