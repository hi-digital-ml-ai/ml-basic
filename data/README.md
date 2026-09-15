# Example datasets

Small datasets used by the course pages. Rules:

- Under 5 MB each; CSV or RDS.
- Every dataset gets a loader in `R/data.R`, not an ad-hoc `read_csv()` in a page.
- Every dataset is documented below: what one row is, where it came from, the
  period it covers, its licence, and how to cite it.
- Nothing embargoed, and nothing that reveals precise locations of protected or
  commercially sensitive species. See `.claude/contributed-pages.md`.

| File | One row is | Source | Period | Licence |
| --- | --- | --- | --- | --- |
| `coastal-survey.csv` | One survey station: position, water properties, substrate, and catch of one benthic species | **Simulated** — `R/make-example-data.R` | Notional 2018–2023 | CC0 (no real data) |
| `coastal-survey-raw.csv` | The same 800 station visits as they came off the ship, plus 15 duplicated rows and extra columns | **Simulated** — `R/make-raw-data.R` | Notional 2018–2023 | CC0 (no real data) |

## About `coastal-survey.csv`

800 stations on a notional temperate shelf. It is **simulated**, and every page that
uses it says so in the text.

Simulation is deliberate rather than a fallback. Because the generating process is
written down in `R/make-example-data.R`, we know the true relationships, so pages can
show a model recovering them — or failing to — which no real dataset allows. It also
sidesteps embargoes and licensing entirely.

The truth built into it:

- abundance peaks around 80 m depth and falls away either side;
- abundance peaks around 9 °C and falls away either side;
- chlorophyll has a positive, saturating effect;
- substrate matters: mud > gravel > sand > rock;
- **salinity and `survey_year` have no effect** — they are there to be rejected;
- a smooth spatial field adds structure no covariate explains, so nearby stations
  are correlated. This is what makes the dataset useful for §6 and §7.

To regenerate (the seed is fixed, so the output is identical):

```bash
Rscript R/make-example-data.R
```

## About `coastal-survey-raw.csv`

The same survey before anyone tidied it, used throughout §2. It is *derived from*
`coastal-survey.csv` by `R/make-raw-data.R`, so the two are guaranteed to describe the
same station visits — which means a reader can clean the raw file and check their work
against the clean one.

What is deliberately wrong with it:

| Problem | Where |
| --- | --- |
| `-999` sentinel values | 25 in salinity, 8 in temperature |
| Missing values, **not at random** | chlorophyll, 6% overall but 19% in winter against 4% in summer |
| Inconsistent category labels | 14 spellings of 4 substrate types in the file (readr's default `trim_ws` silently collapses two, leaving 12) |
| Decimal-point errors | 12 depths ten times too deep (max 1581 m) — but 2 of them land inside the plausible range and cannot be spotted at all |
| Exact duplicate rows | 15, from double data entry |
| Text dates in two formats | ISO for one vessel, day/month/year for the other |
| Instrument bias | `RV Tsubasa` reads salinity about 0.4 PSU high |
| Target leakage | `catch_weight_kg` is computed from `abundance` |
| Class imbalance | `rare_species` present at 5% of stations |
| Non-independent rows | `site_id`: 160 monitoring sites, about 5 visits each |

The last two rows are the ones that matter most later. `site_id` is what makes a naive
random split dishonest, and it is what §7 needs for grouped resampling.

Keep `coastal-survey.csv` clean. New kinds of damage belong in the raw file.
