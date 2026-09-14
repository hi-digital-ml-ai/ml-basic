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

A deliberately messy version — sensor dropouts, transcription errors, a rarer
species — belongs with §2 when that section is written. Keep this one clean.
