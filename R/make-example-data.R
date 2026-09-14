# Generates data/coastal-survey.csv — the simulated dataset used across the course.
#
# Run with: Rscript R/make-example-data.R
#
# The data is SIMULATED, and every page using it says so. Simulation is a
# deliberate choice, not a fallback: because we wrote the generating process, we
# know the true relationships, so pages can show a model recovering them (or
# failing to). No real survey is misrepresented, and nothing is embargoed.
#
# The truth, for reference when writing pages:
#   - abundance peaks at about 80 m depth and falls away either side
#   - abundance peaks at about 9 °C and falls away either side
#   - chlorophyll has a positive, saturating effect
#   - substrate matters: mud > gravel > sand > rock
#   - salinity and survey_year have NO effect — they are there to be rejected
#   - a smooth spatial field adds structure that no covariate explains, so
#     observations near each other are correlated (§6, §7)

set.seed(20260915)

n <- 800

# --- Survey layout: a temperate shelf, deepening offshore -------------------
longitude <- runif(n, 140.0, 142.5)
latitude  <- runif(n, 41.0, 43.0)

depth_m <- 15 + 130 * (longitude - 140.0) / 2.5 +
  25 * sin((latitude - 41) * 2) + rnorm(n, 0, 12)
depth_m <- pmax(depth_m, 5)

# --- Smooth spatial field: structure the covariates do not explain ----------
n_bumps <- 6
bump_lon <- runif(n_bumps, 140.0, 142.5)
bump_lat <- runif(n_bumps, 41.0, 43.0)
bump_amp <- rnorm(n_bumps, 0, 1)
spatial_field <- rowSums(vapply(seq_len(n_bumps), function(k) {
  bump_amp[k] * exp(-((longitude - bump_lon[k])^2 + (latitude - bump_lat[k])^2) / (2 * 0.35^2))
}, numeric(n)))

# --- Environment ------------------------------------------------------------
survey_year <- sample(2018:2023, n, replace = TRUE)
season <- sample(c("spring", "summer", "autumn", "winter"), n, replace = TRUE)
season_temp <- c(spring = 0.5, summer = 4.5, autumn = 1.5, winter = -2.0)[season]

temperature_c <- 11.5 - 0.035 * depth_m - 0.8 * (latitude - 41) +
  season_temp + rnorm(n, 0, 0.7)

salinity_psu <- 33.2 + 0.006 * depth_m + rnorm(n, 0, 0.25)

season_chl <- c(spring = 1.5, summer = 0.3, autumn = 0.6, winter = -0.4)[season]
chlorophyll_mg_m3 <- exp(0.3 - 0.010 * depth_m + season_chl + rnorm(n, 0, 0.45))

substrate <- vapply(depth_m, function(d) {
  p <- c(sand = 0.45, mud = 0.10 + 0.004 * d, gravel = 0.25, rock = 0.35 - 0.003 * d)
  p <- pmax(p, 0.02)
  sample(names(p), 1, prob = p / sum(p))
}, character(1))

# --- Response: the truth ----------------------------------------------------
substrate_effect <- c(sand = 0, mud = 0.40, gravel = 0.20, rock = -0.60)[substrate]

log_mu <- 1.5 -
  0.55 * ((depth_m - 80) / 60)^2 -
  0.60 * ((temperature_c - 9) / 3)^2 +
  0.35 * log1p(chlorophyll_mg_m3) +
  substrate_effect +
  0.70 * spatial_field

abundance <- rnbinom(n, mu = exp(log_mu), size = 1.5)

survey <- data.frame(
  station_id        = sprintf("ST%04d", seq_len(n)),
  survey_year       = survey_year,
  season            = factor(season, levels = c("spring", "summer", "autumn", "winter")),
  longitude         = round(longitude, 4),
  latitude          = round(latitude, 4),
  depth_m           = round(depth_m, 1),
  temperature_c     = round(temperature_c, 2),
  salinity_psu      = round(salinity_psu, 2),
  chlorophyll_mg_m3 = round(chlorophyll_mg_m3, 3),
  substrate         = factor(substrate, levels = c("sand", "mud", "gravel", "rock")),
  abundance         = abundance,
  present           = factor(ifelse(abundance > 0, "yes", "no"), levels = c("yes", "no")),
  stringsAsFactors  = FALSE
)

survey <- survey[order(survey$station_id), ]

dir.create("data", showWarnings = FALSE)
write.csv(survey, "data/coastal-survey.csv", row.names = FALSE)

cat("rows:", nrow(survey), "\n")
cat("present rate:", round(mean(survey$present == "yes"), 3), "\n")
cat("abundance: median", median(survey$abundance), " mean", round(mean(survey$abundance), 2),
    " max", max(survey$abundance), "\n")
print(summary(survey[, c("depth_m", "temperature_c", "salinity_psu", "chlorophyll_mg_m3")]))
print(table(survey$substrate))
