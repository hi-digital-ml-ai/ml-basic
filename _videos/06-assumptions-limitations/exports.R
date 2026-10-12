# Numbers for the assumptions video's Manim scenes, taken from the objects each page
# computed. Sourced by tools/figures-for-video.R; see the comment at its top.
#
# Each table is built with with(env, ...), which looks names up in the page's
# environment, and written outside it: inside, `dir` would find base R's dir().

write <- function(x, dir, name) readr::write_csv(x, file.path(dir, paste0(name, ".csv")))

exports <- list(
  # Scenes 7–10: the stations of the depth and temperature scatter.
  "sampling-and-extrapolation.qmd" = function(env, dir) {
    write(with(env, dplyr::bind_rows(
      dplyr::transmute(surveyed, depth_m, temperature_c, season, status = "Surveyed"),
      dplyr::transmute(novelty, depth_m, temperature_c, season, status))), dir, "novelty")
  },

  # Scenes 12–15: the rare species' share, the calls at 0.5, and the calls at a
  # threshold lowered to the prevalence.
  "class-imbalance.qmd" = function(env, dir) {
    write(with(env, tibble::tibble(stations = nrow(train), present = n_present,
                                   prevalence = prevalence, top = top,
                                   copies = copies)), dir, "rare")
    write(with(env, at_default), dir, "at-default")
    write(with(env, same), dir, "same")
  }
)
