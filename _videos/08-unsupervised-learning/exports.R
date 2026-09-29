# Numbers for the unsupervised-learning video's Manim scenes, taken from the objects
# each page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scene 20: agreement with the seabed for every linkage and k. Knitted first: it
  # attaches mclust with adjustedRandIndex, and the pages after it that attach mclust
  # with fewer functions leave the attached package as it is.
  "beyond-k-means.qmd" = function(env, dir) {
    write(with(env, linkages), dir, "linkages")
  },

  # Scenes 8–12: each variable's share of the raw variance, the raw and standardised
  # clusterings, the clusters against the seabed, and k-means on uniform noise.
  "clustering.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(variable = names(env),
                                   share = purrr::map_dbl(env, var) / sum(purrr::map_dbl(env, var)))),
          dir, "env-share")
    write(with(env, dplyr::mutate(dplyr::select(env, depth_m, chlorophyll_mg_m3),
                                  raw = raw_clusters$cluster, scaled = scaled_clusters$cluster)),
          dir, "env-clusters")
    write(with(env, dplyr::count(stations, cluster, bottom)), dir, "habitat")
    write(with(env, noise), dir, "noise")
  },

  # Scenes 14–19: the k sweep on the observed and shuffled matrices, and the number of
  # clusters each criterion chose.
  "choosing-the-number-of-clusters.qmd" = function(env, dir) {
    write(with(env, comparison), dir, "k-sweep")
    write(with(env, tibble::tibble(
      criterion = c("silhouette against shuffled", "gap statistic", "mixture BIC"),
      k = c(observed$k[which.max(observed$silhouette - reference$silhouette)],
            gap_table$k[maxSE(gap_table$gap, gap_table$SE.sim, method = "firstSEmax")],
            mixture$G))), dir, "criteria")
  },

  # Scenes 23–27: the variance table, the station map, and the directions in which
  # depth and hard bottom increase.
  "principal-component-analysis.qmd" = function(env, dir) {
    write(with(env, variance), dir, "variance")
    write(with(env, dplyr::select(stations, PC1, PC2, depth_m, bottom)), dir, "ordination")
    write(with(env, tibble::tibble(
      gradient = c("depth", "hard bottom"),
      x = c(depth_direction[1], bottom_direction[1]),
      y = c(depth_direction[2], bottom_direction[2]),
      angle = round(atan2(y, x) * 180 / pi))), dir, "directions")
  },

  # Scenes 28–31: the three rules, the cross-validated depth error, and the two UMAPs.
  "dimensionality-reduction.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(
      rule = c("80% of variance", "Kaiser", "parallel analysis"),
      components = c(which(cumsum(proportion) >= 0.8)[1], sum(eigenvalues > 1),
                     sum(proportion > null_threshold)))), dir, "rules")
    write(with(env, dplyr::filter(collect_metrics(tuned), .metric == "rmse") |>
                 dplyr::select(num_comp, mean, std_err)), dir, "components-cv")
    write(with(env, tibble::tibble(x = embedding[, 1], y = embedding[, 2],
                                   null_x = null_embedding[, 1], null_y = null_embedding[, 2],
                                   depth_m = stations$depth_m, bottom = stations$bottom)),
          dir, "umap")
  },

  # Scenes 3–5 and 35–43: the bootstrap replicates, the soft-bottom split and its
  # stability, the continuum of soft-substrate taxa, and the external checks.
  "interpreting-patterns.qmd" = function(env, dir) {
    write(with(env, replicates), dir, "replicates")
    write(with(env, tibble::tibble(agreement = soft_agreement)), dir, "soft-stability")
    write(with(env, tibble::tibble(depth_m = stations$depth_m[soft], cluster = soft_reference)),
          dir, "soft-stations")
    write(with(env, tibble::tibble(
      cluster = 1:2, median_depth = as.numeric(tapply(stations$depth_m[soft], soft_reference, median)),
      boundary = boundary)), dir, "soft-medians")
    # The curves of fig-continuum: geom_smooth's loess (span 0.6) for each taxon.
    write(with(env, {
      long <- community |>
        dplyr::inner_join(dplyr::select(stations, station_id, depth_m, bottom), by = "station_id") |>
        dplyr::filter(bottom == "soft") |>
        tidyr::pivot_longer(tidyselect::all_of(soft_taxa$taxon), names_to = "taxon",
                            values_to = "count")
      grid <- seq(min(long$depth_m), max(long$depth_m), length.out = 80)
      purrr::map_dfr(soft_taxa$taxon, \(t) {
        fit <- loess(count ~ depth_m, data = dplyr::filter(long, taxon == t), span = 0.6)
        tibble::tibble(taxon = t, depth_m = grid, count = predict(fit, data.frame(depth_m = grid)))
      }) |>
        dplyr::left_join(dplyr::select(soft_taxa, taxon, depth_optimum_m), by = "taxon")
    }), dir, "continuum")
    write(with(env, tibble::tibble(
      clustering = c("all stations", "soft stations only"),
      substrate = c(adjustedRandIndex(reference, stations$bottom),
                    adjustedRandIndex(soft_reference, stations$bottom[soft])),
      depth_band = c(adjustedRandIndex(reference, depth_band),
                     adjustedRandIndex(soft_reference, depth_band[soft])))), dir, "external")
  }
)
