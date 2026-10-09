# Numbers for the unsupervised-learning video's Manim scenes, taken from the objects
# each page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scene 12: the share of stations in the largest group for every linkage and k.
  # Knitted first: it attaches mclust with adjustedRandIndex, and the pages after it
  # that attach mclust with fewer functions leave the attached package as it is.
  "hierarchical-clustering.qmd" = function(env, dir) {
    write(with(env, linkages), dir, "linkages")
  },

  # Scenes 3 and 5: a corner of the community matrix, and the clusters against the
  # recorded seabed.
  "clustering.qmd" = function(env, dir) {
    write(with(env, dplyr::slice_head(dplyr::select(taxa_only, 1:8), n = 6)), dir, "matrix")
    write(with(env, dplyr::select(seabed, cluster, bottom, n, majority)), dir, "seabed")
  },

  # Scenes 8 and 10: the average silhouette on the observed and shuffled counts.
  "choosing-the-number-of-clusters.qmd" = function(env, dir) {
    write(with(env, dplyr::select(lift, k, silhouette, silhouette_mean, silhouette_low,
                                  silhouette_high, times)), dir, "silhouette")
  },

  # Scenes 15–17: the variance table, the station map, the taxa's loadings, and the
  # directions in which depth and hard bottom increase.
  "principal-component-analysis.qmd" = function(env, dir) {
    write(with(env, variance), dir, "variance")
    write(with(env, dplyr::select(stations, PC1, PC2, depth_m, hard_bottom)), dir, "ordination")
    write(with(env, dplyr::select(taxon_habitat, taxon, PC1, PC2, hard_share, mean_depth)),
          dir, "loadings")
    write(with(env, directions), dir, "directions")
  },

  # Scenes 18–20: each component's share against the shuffled tables, the
  # cross-validated error of predicting depth, and the observed and shuffled UMAP maps.
  "dimensionality-reduction.qmd" = function(env, dir) {
    write(with(env, dplyr::select(shares, component, observed, cumulative, shuffled, above)),
          dir, "shares")
    write(with(env, dplyr::select(dplyr::filter(cv, .metric == "rmse"), num_comp, mean, std_err)),
          dir, "components-cv")
    write(with(env, dplyr::select(maps, data, UMAP1, UMAP2, depth_m, seabed)), dir, "umap")
  },

  # Scenes 25, 27, 28 and 31: the bootstrap refits, each station's position between
  # the centres, and the clusters against the recorded seabed.
  "interpreting-patterns.qmd" = function(env, dir) {
    write(with(env, replicates), dir, "replicates")
    write(with(env, dplyr::select(positions, split, position)), dir, "positions")
    write(with(env, external), dir, "external")
    write(with(env, dplyr::count(tibble::tibble(cluster = original, bottom = stations$bottom),
                                 cluster, bottom)), dir, "record")
  }
)
