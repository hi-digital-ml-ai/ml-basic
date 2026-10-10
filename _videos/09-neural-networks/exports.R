# Numbers for the neural-networks video's Manim scenes, taken from the objects each
# page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().
# Single numbers the narration speaks go into a "<page>-numbers" table of name and
# value, so a scene can show the page's own value.

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))
numbers <- function(...) tibble::tibble(name = names(c(...)), value = unname(c(...)))

exports <- list(
  # One neuron against lm(), the fitted humps over the binned means, the two bends the
  # two-unit network adds up, and the weight counts. nnet's hidden units are logistic.
  "what-a-network-is.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(term = names(coef(linear)), lm = unname(coef(linear)),
                                   neuron = as.numeric(coef(one_neuron)))), dir, "one-neuron")
    write(with(env, dplyr::transmute(curves, temperature_c, y, units = as.integer(as.character(units)))),
          dir, "hump")
    write(with(env, dplyr::select(binned, temperature_c, y, n)), dir, "hump-binned")
    write(with(env, dplyr::select(parts, temperature_c, unit1 = `Unit 1`, unit2 = `Unit 2`,
                                  prediction = Prediction)), dir, "hump-parts")
    write(with(env, numbers(places = floor(-log10(largest_gap)), peak_c = peak_c,
                            top_low = top_low, two_unit_weights = length(coef(fit_units(2))),
                            small_net = n_weights(3, 4), small_linear = 3 + 1,
                            large_net = n_weights(10, 20))),
          dir, "what-a-network-is-numbers")
  },

  # The largest difference between backpropagation and nudging, per group of weights.
  "forward-and-backward.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(group = names(par), difference = check$`Largest difference`)),
          dir, "gradient-check")
    write(with(env, numbers(n_weights = n_weights, places = check_places)),
          dir, "forward-and-backward-numbers")
  },

  # The long run and the ten seeds.
  "training-a-network.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(step = seq_along(big$training), training = big$training,
                                   validation = big$validation)), dir, "early-stopping")
    write(with(env, tibble::tibble(seed = seq_along(seed_mse), validation = seed_mse)), dir, "seeds")
    write(with(env, numbers(
      n_train = nrow(X_train), n_valid = nrow(X_valid),
      best_step = best_step, last_step = last_step, worse_pct = worse_pct,
      seed_spread = max(seed_mse) - min(seed_mse), averaged_mse = averaged_mse,
      n_beaten = n_beaten)),
      dir, "training-a-network-numbers")
  },

  # The survey's counts: each model's test RMSE on the counts, and against the true mean
  # counts when trained on them. Then the water-mass band: training stations, scores,
  # each model's predicted class over the plane (a coarser grid than the page's figure),
  # the network's hidden units, the three sample sizes and the named combination.
  "when-a-network-pays-off.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(model = scores$Model, counts = scores$`Test RMSE`,
                                   true_means = checked$`Trained on true means`)),
          dir, "survey-scores")
    write(with(env, water_train), dir, "water-train")
    write(with(env, dplyr::transmute(water_scores, model = Model, auc = `Test ROC AUC`)), dir, "water-auc")
    write(with(env, {
      grid <- tidyr::expand_grid(
        temperature_c = seq(2, 16, length.out = 120),
        salinity_psu = seq(min(water_train$salinity_psu), max(water_train$salinity_psu), length.out = 120))
      purrr::imap_dfr(water_fits, \(fitted, nm)
        dplyr::mutate(grid, model = nm, core = predict(fitted, grid)$.pred_class == "core"))
    }), dir, "water-plane")
    write(with(env, {
      net <- extract_fit_engine(water_fits$`Neural network`)
      steps <- extract_recipe(water_fits$`Neural network`)$steps[[1]]
      w <- coef(net)
      units <- seq_len(net$n[2])
      tibble::tibble(unit = units,
                     bias = w[paste0("b->h", units)], t = w[paste0("i1->h", units)],
                     s = w[paste0("i2->h", units)], out = w[paste0("h", units, "->o")],
                     t_mean = steps$means[["temperature_c"]], t_sd = steps$sds[["temperature_c"]],
                     s_mean = steps$means[["salinity_psu"]], s_sd = steps$sds[["salinity_psu"]])
    }), dir, "water-units")
    write(with(env, dplyr::rename(by_size, n = `Training stations`)), dir, "water-sizes")
    write(with(env, numbers(baseline = baseline, n_train = nrow(train),
                            n_weights = band_weights, n_test = nrow(water_test), named_auc = named_auc,
                            n_coefficients = nrow(tidy(named_fit)))),
          dir, "when-a-network-pays-off-numbers")
  }
)
