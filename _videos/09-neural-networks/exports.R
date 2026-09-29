# Numbers for the neural-networks video's Manim scenes, taken from the objects each
# page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # One neuron against lm(), the hidden-unit sweep, the fitted humps, and the two
  # S-curves the two-unit network adds up. nnet's hidden units are logistic.
  "what-a-network-is.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(term = names(coef(linear)), lm = unname(coef(linear)),
                                   neuron = as.numeric(coef(one_neuron)))), dir, "one-neuron")
    write(with(env, sweep), dir, "units-sweep")
    write(with(env, dplyr::select(curves, temperature_c, y, units = `hidden units`)), dir, "hump")
    write(with(env, dplyr::select(binned, temperature_c, y, n)), dir, "hump-binned")
    write(with(env, {
      w <- coef(fit_units(2))
      g <- grid$temp
      tibble::tibble(temperature_c = g * temp_sd + temp_mean, bias = w[["b->o"]],
                     unit1 = w[["h1->o"]] * plogis(w[["b->h1"]] + w[["i1->h1"]] * g),
                     unit2 = w[["h2->o"]] * plogis(w[["b->h2"]] + w[["i1->h2"]] * g))
    }), dir, "hump-parts")
  },

  # The largest disagreement between backpropagation and finite differences.
  "forward-and-backward.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      parameter = names(par),
      disagreement = purrr::map_dbl(names(par), \(nm)
        max(abs(as.numeric(gradients[[nm]]) - as.numeric(numeric[[nm]])))))), dir, "gradient-check")
  },

  # The learning-rate sweep, the unscaled run, the long run and the ten seeds.
  "training-a-network.qmd" = function(env, dir) {
    write(with(env, sweeps), dir, "rates")
    write(with(env, tibble::tibble(
      inputs = c("standardised", "measured units", "linear model"),
      mse = c(dplyr::last(standardised$training), dplyr::last(measured$training), linear_mse))),
      dir, "scaling")
    write(with(env, tibble::tibble(step = seq_along(big$training), training = big$training,
                                   validation = big$validation, best = step == best_step)),
          dir, "early-stopping")
    write(with(env, seed_runs), dir, "seeds")
  },

  # The baseline and the oracle, the learning curves, the tuned configuration and the
  # noise-free diagnostic.
  "how-much-data.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(baseline = baseline, oracle = oracle)), dir, "references")
    write(with(env, dplyr::summarise(curves, lower = quantile(rmse, 0.1), upper = quantile(rmse, 0.9),
                                     rmse = mean(rmse), sd = sd(rmse), .by = c(n, model))),
          dir, "learning-curves")
    write(with(env, dplyr::select(show_best(searched, metric = "rmse", n = 1),
                                  hidden_units, penalty, mean)), dir, "tuned")
    write(with(env, dplyr::summarise(noise_free, rmse = mean(rmse), .by = c(n, model))),
          dir, "noise-free")
  },

  # The water-mass band: training stations, scores, each model's probability over the
  # plane, the network's hidden units, and the sample sizes. The `sizes` chunk prints
  # its table without keeping it, so it is re-run here with the page's own seeds.
  "when-to-use-one.qmd" = function(env, dir) {
    write(with(env, train), dir, "water-train")
    write(with(env, purrr::imap_dfr(fits, \(fitted, nm) {
      scored <- augment(fitted, test)
      tibble::tibble(model = nm, auc = roc_auc_vec(test$water_mass, scored$.pred_core),
                     weights = if (nm == "neural network") length(coef(extract_fit_engine(fitted))) else NA)
    })), dir, "water-auc")
    write(with(env, purrr::imap_dfr(fits, \(fitted, nm)
      dplyr::mutate(plane, model = nm, p_core = predict(fitted, plane, type = "prob")$.pred_core))),
      dir, "water-plane")
    write(with(env, {
      p <- predict(fits$`neural network`, plane, type = "prob")$.pred_core
      tibble::tibble(low = min(p), high = max(p))
    }), dir, "water-range")
    write(with(env, {
      net <- extract_fit_engine(fits$`neural network`)
      steps <- extract_recipe(fits$`neural network`)$steps[[1]]
      w <- coef(net)
      units <- seq_len(net$n[2])
      tibble::tibble(unit = units,
                     bias = w[paste0("b->h", units)], t = w[paste0("i1->h", units)],
                     s = w[paste0("i2->h", units)], out = w[paste0("h", units, "->o")],
                     t_mean = steps$means[["temperature_c"]], t_sd = steps$sds[["temperature_c"]],
                     s_mean = steps$means[["salinity_psu"]], s_sd = steps$sds[["salinity_psu"]])
    }), dir, "water-units")
    write(with(env, purrr::map_dfr(c(100, 400, 1600), \(n) {
      training <- make_water_mass(n, seed = 10 + n)
      purrr::imap_dfr(specs, \(spec, nm) {
        set.seed(5)
        fitted <- fit(workflow() |> add_recipe(water_recipe) |> add_model(spec), training)
        tibble::tibble(n = n, model = nm,
                       auc = roc_auc_vec(test$water_mass, augment(fitted, test)$.pred_core))
      })
    })), dir, "water-sizes")
  }
)
