# Numbers for the unsupervised-learning video's Manim scenes, taken from the objects
# each page computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 3 and 6: a corner of the counts table, and the clusters against the
  # recorded seabed.
  "clustering.qmd" = function(env, dir) {
    write(with(env, dplyr::slice_head(dplyr::select(taxa_only, 1:8), n = 6)), dir, "matrix")
    write(with(env, dplyr::select(seabed, cluster, bottom, n, majority)), dir, "seabed")
  },

  # Scenes 10–13: the station map.
  "principal-component-analysis.qmd" = function(env, dir) {
    write(with(env, dplyr::select(stations, PC1, PC2, depth_m, hard_bottom)), dir, "ordination")
  },

  # Scenes 18 and 19: each bootstrap refit's agreement with the original grouping.
  "interpreting-patterns.qmd" = function(env, dir) {
    write(with(env, replicates), dir, "replicates")
  }
)
