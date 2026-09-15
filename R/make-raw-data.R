# Generates data/coastal-survey-raw.csv — the "as collected" version of the survey
# used throughout section 2.
#
# Run with: Rscript R/make-raw-data.R   (after R/make-example-data.R)
#
# This script takes data/coastal-survey.csv and puts back the damage that a real
# field dataset arrives with. Deriving it from the clean extract rather than
# generating it separately means the two files are guaranteed to describe the same
# 800 station visits: section 2 can clean the raw file and check its work.
#
# What is wrong with it, deliberately:
#
#  1. -999 sentinel values in salinity and temperature (the classic missing-data
#     landmine: numeric, so nothing complains, and it destroys any mean)
#  2. missing chlorophyll, MORE OFTEN IN WINTER AND AT HIGH LATITUDE — missingness
#     that is not random, which is the case that matters
#  3. substrate typed inconsistently by different observers
#  4. decimal-point errors in depth (a handful of stations ten times too deep)
#  5. exact duplicate rows, from a double data entry
#  6. sample_date as text in two different formats
#  7. two vessels, one with a miscalibrated salinity sensor
#  8. catch_weight_kg, computed from the catch — a target-leakage trap
#  9. rare_species, present at about 6% of stations — class imbalance
# 10. site_id: stations belong to 160 monitoring sites, so rows are NOT independent.
#     This is the group-leakage trap, and it sets up grouped resampling in §7.

set.seed(4242)

clean <- read.csv("data/coastal-survey.csv", stringsAsFactors = FALSE)
n <- nrow(clean)

raw <- clean

# --- 10. Monitoring sites: nearby stations are revisits of the same site --------
sites <- kmeans(scale(clean[, c("longitude", "latitude")]), centers = 160, iter.max = 50)
raw$site_id <- sprintf("SITE-%03d", sites$cluster)

# --- 7. Vessels, one with a salinity calibration offset -------------------------
raw$vessel <- sample(c("RV Kaiyo", "RV Tsubasa"), n, replace = TRUE, prob = c(0.55, 0.45))
raw$salinity_psu <- raw$salinity_psu + ifelse(raw$vessel == "RV Tsubasa", 0.42, 0)

# --- 6. Dates as text, in two formats -------------------------------------------
month_of <- c(spring = 4, summer = 7, autumn = 10, winter = 1)[raw$season]
day <- sample(1:28, n, replace = TRUE)
iso <- sprintf("%d-%02d-%02d", raw$survey_year, month_of, day)
dmy <- sprintf("%02d/%02d/%d", day, month_of, raw$survey_year)
raw$sample_date <- ifelse(raw$vessel == "RV Kaiyo", iso, dmy)

# --- 8. A column computed from the response (target leakage) --------------------
raw$catch_weight_kg <- round(raw$abundance * runif(n, 0.28, 0.42) + runif(n, 0, 0.05), 3)

# --- 9. A rare species, present at about 6% of stations -------------------------
rare_p <- plogis(-6.2 + 0.030 * raw$depth_m + 0.9 * (raw$substrate == "rock"))
raw$rare_species <- ifelse(rbinom(n, 1, rare_p) == 1, "yes", "no")

# --- 3. Substrate typed by several observers ------------------------------------
variants <- list(
  sand   = c("sand", "Sand", "SAND", "sandy"),
  mud    = c("mud", "Mud", "mud ", "muddy"),
  gravel = c("gravel", "Gravel", "gravel "),
  rock   = c("rock", "Rock", "rocky")
)
raw$substrate <- vapply(raw$substrate, function(s) sample(variants[[s]], 1), character(1))

# --- 2. Chlorophyll missing, and not at random ----------------------------------
p_missing <- plogis(-3.4 + 1.9 * (raw$season == "winter") + 0.8 * (raw$latitude - 42))
raw$chlorophyll_mg_m3[rbinom(n, 1, p_missing) == 1] <- NA

# --- 1. Sentinel values ---------------------------------------------------------
raw$salinity_psu[sample(n, round(0.03 * n))]  <- -999
raw$temperature_c[sample(n, round(0.01 * n))] <- -999

# --- 4. Decimal-point errors in depth -------------------------------------------
slipped <- sample(n, 12)
raw$depth_m[slipped] <- raw$depth_m[slipped] * 10

# --- Column order as a field export would have it -------------------------------
raw <- raw[, c("station_id", "site_id", "vessel", "sample_date", "survey_year", "season",
               "longitude", "latitude", "depth_m", "temperature_c", "salinity_psu",
               "chlorophyll_mg_m3", "substrate", "abundance", "catch_weight_kg",
               "present", "rare_species")]

# --- 5. Duplicate rows from double data entry -----------------------------------
raw <- rbind(raw, raw[sample(n, 15), ])
raw <- raw[sample(nrow(raw)), ]

write.csv(raw, "data/coastal-survey-raw.csv", row.names = FALSE)

cat("rows:", nrow(raw), "(", nrow(raw) - n, "duplicates )\n")
cat("chlorophyll missing:", round(mean(is.na(raw$chlorophyll_mg_m3)), 3), "\n")
cat("  in winter:", round(mean(is.na(raw$chlorophyll_mg_m3[raw$season == "winter"])), 3),
    " in summer:", round(mean(is.na(raw$chlorophyll_mg_m3[raw$season == "summer"])), 3), "\n")
cat("salinity -999:", sum(raw$salinity_psu == -999), "  temperature -999:", sum(raw$temperature_c == -999), "\n")
cat("rare_species yes:", round(mean(raw$rare_species == "yes"), 3), "\n")
cat("sites:", length(unique(raw$site_id)), " stations per site:",
    round(mean(table(raw$site_id)), 1), "\n")
cat("substrate labels:", length(unique(raw$substrate)), "\n")
cat("depth max:", max(raw$depth_m), "\n")
