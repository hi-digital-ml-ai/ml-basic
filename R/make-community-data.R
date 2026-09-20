# Generates data/coastal-community.csv and data/coastal-community-taxa.csv,
# the multi-taxon community matrix used in §8 (unsupervised learning).
#
# Run with: Rscript R/make-community-data.R
#
# The data is SIMULATED, and every page using it says so. It is built on top of
# data/coastal-survey.csv, so it joins on station_id and describes the same 800
# stations: the same depths, the same substrates, the same shelf.
#
# The truth, for reference when writing pages:
#   - 24 taxa. Composition turns over CONTINUOUSLY along depth: each taxon has a
#     Gaussian depth optimum and the optima are spread evenly from 15 m to 165 m.
#     There are no depth-defined assemblages. Any depth "cluster" is a cut through
#     a gradient.
#   - Substrate structure IS discrete: 6 taxa occur essentially only on rock and
#     gravel, 8 essentially only on sand and mud, 7 are indifferent. So the one
#     real grouping of stations is hard-bottom versus soft-bottom, and it is
#     two groups, not three or five.
#   - 3 taxa (tax22-tax24) respond to NOTHING: constant mean, no depth, no
#     substrate. They are there to be rejected, like salinity in the survey.
#   - Counts are negative binomial, so the matrix is sparse and over-dispersed
#     the way real benthic grabs are.
#
# Consequence the §8 pages are built on: the hard/soft split replicates under
# resampling and matches an external variable; the depth split does neither.

set.seed(20260916)

survey <- read.csv("data/coastal-survey.csv", stringsAsFactors = FALSE)
survey <- survey[order(survey$station_id), ]
n <- nrow(survey)

# --- Taxon traits ------------------------------------------------------------
taxon <- sprintf("tax%02d", 1:24)

group <- c(rep("hard-substrate", 6), rep("soft-substrate", 8),
           rep("generalist", 7), rep("unrelated", 3))

# Depth optima spread evenly across the surveyed range: a continuum, by design.
depth_optimum <- c(seq(20, 160, length.out = 21), rep(NA, 3))
depth_optimum <- round(depth_optimum[c(seq(1, 21, by = 3.5)[1:6],   # hard
                                       seq(2, 21, by = 2.6)[1:8],   # soft
                                       seq(3, 21, by = 3)[1:7],     # generalist
                                       NA, NA, NA)])
niche_width <- c(rep(38, 6), rep(34, 8), rep(45, 7), rep(NA, 3))
peak_mean   <- round(exp(runif(24, log(1.5), log(9))), 2)

prefs <- list(
  `hard-substrate` = c(sand = 0.05, mud = 0.02, gravel = 0.85, rock = 1.00),
  `soft-substrate` = c(sand = 0.80, mud = 1.00, gravel = 0.12, rock = 0.03),
  `generalist`     = c(sand = 0.90, mud = 1.00, gravel = 0.95, rock = 0.85),
  `unrelated`      = c(sand = 1.00, mud = 1.00, gravel = 1.00, rock = 1.00)
)

# --- Expected counts ---------------------------------------------------------
counts <- matrix(0L, nrow = n, ncol = 24, dimnames = list(NULL, taxon))

for (j in seq_len(24)) {
  substrate_mult <- prefs[[group[j]]][survey$substrate]

  depth_mult <- if (is.na(depth_optimum[j])) {
    rep(1, n)
  } else {
    exp(-((survey$depth_m - depth_optimum[j])^2) / (2 * niche_width[j]^2))
  }

  mu <- peak_mean[j] * depth_mult * substrate_mult
  counts[, j] <- rnbinom(n, mu = mu, size = 1.2)
}

community <- data.frame(station_id = survey$station_id, counts,
                        stringsAsFactors = FALSE)

taxa <- data.frame(
  taxon            = taxon,
  group            = group,
  depth_optimum_m  = depth_optimum,
  niche_width_m    = niche_width,
  peak_mean        = peak_mean,
  stringsAsFactors = FALSE
)

write.csv(community, "data/coastal-community.csv", row.names = FALSE)
write.csv(taxa, "data/coastal-community-taxa.csv", row.names = FALSE)

cat("stations:", nrow(community), " taxa:", ncol(community) - 1, "\n")
cat("zeros:", round(mean(counts == 0), 3), "\n")
cat("taxa per station: median", median(rowSums(counts > 0)),
    " range", paste(range(rowSums(counts > 0)), collapse = "-"), "\n")
cat("total per station: median", median(rowSums(counts)),
    " max", max(rowSums(counts)), "\n")
print(table(rowSums(counts) == 0))
print(taxa)
