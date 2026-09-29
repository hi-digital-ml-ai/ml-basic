# Numbers for the introduction video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # The first five stations as the page prints them, and the clustered stations with
  # the names the page gives the groups.
  "types-of-learning.qmd" = function(env, dir) {
    write(with(env, head(dplyr::select(survey, temperature_c, salinity_psu, depth_m, abundance,
                                       present), 5)), dir, "survey-head")
    write(with(env, dplyr::select(clustered, depth_m, temperature_c, group)), dir, "clusters")
  },

  # The training stations and the two models' predictions across temperature, as
  # @fig-shapes draws them.
  "what-is-machine-learning.qmd" = function(env, dir) {
    write(with(env, dplyr::select(train, temperature_c, abundance)), dir, "train-points")
    write(with(env, dplyr::select(curves, model, temperature_c, .pred)), dir, "shapes")
  }
)
