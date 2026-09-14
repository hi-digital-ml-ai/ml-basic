# Shared plotting style for the whole site.
# Pages load this with: source(here::here("R/theme.R"))

suppressPackageStartupMessages({
  library(ggplot2)
})

# Okabe-Ito: distinguishable for the common forms of colour blindness and in
# greyscale. Used for categorical fills and colours site-wide.
ml_palette <- c(
  blue      = "#0072B2",
  orange    = "#E69F00",
  green     = "#009E73",
  vermilion = "#D55E00",
  purple    = "#CC79A7",
  sky       = "#56B4E9",
  yellow    = "#F0E442",
  grey      = "#5A5A5A"
)

#' Site ggplot theme: light, uncluttered, readable when scaled down in a listing card.
theme_ml <- function(base_size = 13) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.title       = element_text(face = "bold", size = rel(1.05), hjust = 0),
      plot.subtitle    = element_text(colour = "#55606a", size = rel(0.92)),
      plot.caption     = element_text(colour = "#77818a", size = rel(0.8), hjust = 0),
      plot.title.position = "plot",
      axis.title       = element_text(colour = "#3d4852"),
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(colour = "#e6eaed", linewidth = 0.4),
      strip.text       = element_text(face = "bold", size = rel(0.92)),
      legend.position  = "bottom",
      legend.title     = element_text(size = rel(0.9))
    )
}

theme_set(theme_ml())

# Categorical scales default to the palette above; continuous scales to viridis.
scale_colour_ml <- function(...) scale_colour_manual(values = unname(ml_palette), ...)
scale_fill_ml   <- function(...) scale_fill_manual(values = unname(ml_palette), ...)

options(
  ggplot2.discrete.colour = function(...) scale_colour_ml(...),
  ggplot2.discrete.fill   = function(...) scale_fill_ml(...),
  ggplot2.continuous.colour = function(...) scale_colour_viridis_c(...),
  ggplot2.continuous.fill   = function(...) scale_fill_viridis_c(...)
)
