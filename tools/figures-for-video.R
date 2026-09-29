#!/usr/bin/env Rscript
# Re-export a section's figures at video size, and write the numbers its Manim
# scenes animate.
#
#   Rscript tools/figures-for-video.R _videos/05-generalisation
#
# Every page named in the script's "visual: figure <page>.qmd#<label>" lines, or in
# the video's exports.R, is knitted exactly as Quarto runs it, but with every figure
# forced to 1920x1080. The pages stay the only source: nothing here refits a model.
#
#   visuals/figures/<page>/<label>-1.png   every figure of those pages
#   visuals/data/<name>.csv                 written by the video's exports.R
#
# exports.R defines `exports`, a list named by page file, each a function of the
# environment the page ran in and the output folder. It picks the page's own
# objects (a results table, a baseline) and writes them as CSV for scenes.py.

suppressPackageStartupMessages(library(knitr))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: Rscript tools/figures-for-video.R _videos/NN-slug")
video <- normalizePath(args[[1]], mustWork = TRUE)
root  <- here::here()   # the repo root, found the same way the pages find it

script <- readLines(file.path(video, "script.md"), warn = FALSE)
section <- sub("^section:\\s*", "", grep("^section:", script, value = TRUE))
chapter <- file.path(root, dirname(section))

figures <- regmatches(script, regexpr("(?<=^visual: figure )[^#\\s]+\\.qmd", script, perl = TRUE))

exports <- list()
if (file.exists(file.path(video, "exports.R"))) source(file.path(video, "exports.R"))
pages <- unique(c(figures, names(exports)))

# 8 x 4.5 inches at 240 dpi is 1920 x 1080. The site's 13-point text then stands
# 36 pixels tall, a thirtieth of the frame: readable on a phone.
width <- 8; height <- 4.5; dpi <- 240
data_dir <- file.path(video, "visuals", "data")
dir.create(data_dir, recursive = TRUE, showWarnings = FALSE)

for (page in pages) {
  message("knitting ", page)
  out <- file.path(video, "visuals", "figures", sub("\\.qmd$", "", page))
  unlink(out, recursive = TRUE)
  dir.create(out, recursive = TRUE)

  # knitr reads .Rmd, not .qmd; the chunks and their #| options are the same.
  input <- tempfile(fileext = ".Rmd")
  file.copy(file.path(chapter, page), input)

  opts_knit$set(root.dir = root)
  opts_chunk$set(fig.path = paste0(out, "/"), dev = "ragg_png", dpi = dpi,
                 fig.width = width, fig.height = height, fig.retina = 1,
                 message = FALSE, warning = FALSE, error = FALSE)  # stop on a failing chunk
  # A page's own fig-width or fig-height would win over the defaults above.
  opts_hooks$set(fig.width  = function(o) { o$fig.width  <- width;  o },
                 fig.height = function(o) { o$fig.height <- height; o })

  env <- new.env(parent = globalenv())
  knit(input, output = tempfile(fileext = ".md"), envir = env, quiet = TRUE)

  if (!is.null(exports[[page]])) exports[[page]](env, data_dir)
}

message("figures: ", file.path(video, "visuals", "figures"))
message("data:    ", data_dir, " (", paste(list.files(data_dir), collapse = ", "), ")")
