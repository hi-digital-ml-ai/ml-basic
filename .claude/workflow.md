# Workflow

## Local development

```bash
quarto preview                 # live-reloading site at localhost:4200-ish
quarto render                  # full build into _site/
quarto render chapters/05-generalisation/overfitting.qmd   # one page
```

The site is developed entirely locally. `_site/` is build output and is **not**
committed.

`quarto render` runs `tools/extract-code.py` first, which pulls the R and Python out
of every page into `downloads/` as runnable scripts plus `ml-basic-code.zip`, and
`tools/code-downloads.lua` puts the download links on each page. `downloads/` is
generated and git-ignored; see `tools/README.md`. To refresh it without a full
build:

```bash
tools/extract-code.py
```

### Python for the tabs

Converted pages run their Python tabs as `{python}` chunks, through `reticulate`, so
rendering such a page needs a Python with `python/requirements.txt` installed. Tell
Quarto which one in `_environment.local` at the project root (git-ignored, one per
machine), and put `python/` on the import path so `mlbasic_data` loads:

```bash
RETICULATE_PYTHON=/path/to/env/bin/python
PYTHONPATH=/path/to/ml-basic/python
```

`R/python-tabs.R` shows a chunk's final pandas DataFrame as a table, through
`to_markdown()` (so `tabulate` must be installed). It wraps reticulate's internal
`eng_python_autoprint()`, so after upgrading reticulate render a page with a Python
table and check it still shows as a table.

CI and anyone rendering only other pages need nothing: the Python output is stored in
`_freeze/` like the R output, so commit the freeze with the page.

## R environment

`renv` pins package versions so every author renders the same results. The project
library lives in `renv/library/` (git-ignored); `renv.lock` is the record and **is**
committed.

```bash
Rscript -e 'renv::restore()'    # after cloning, or when renv.lock changes
Rscript -e 'renv::status()'     # is the library in sync with the lockfile?
Rscript -e 'renv::install("pkg")' && Rscript -e 'renv::snapshot()'
```

Commit `renv.lock` in the same commit as the page that needs the new package.

`snapshot.type` is set to `"all"`, so the lockfile records the whole project library
rather than only packages renv can find `library()` calls for. Packages here are
installed ahead of the pages that use them, and the default implicit snapshotter
would drop almost all of them.

`.Rprofile` points R at Posit Package Manager's prebuilt binaries on Ubuntu and at
CRAN everywhere else. That is an install-speed choice only, since the lockfile pins
versions either way, but it is the difference between a two-minute install and an
hour of compilation. On a non-Ubuntu Linux machine it falls back to CRAN source
packages, so expect a slow first `renv::restore()`.

### System dependencies

`sf` needs GDAL, GEOS and PROJ, which are present on this machine (`gdal-config`,
`geos-config`, `proj`). A new machine needs them installed at the OS level first.

`kknn` (k-nearest neighbours) is deliberately **not** installed: it pulls in `igraph`,
whose binary needs `libglpk.so.40`, a system library that is not present and needs
root to install. k-NN is not in the curriculum, so dropping it was cheaper than
taking on a system dependency. If a page ever wants k-NN, `libglpk40` has to be
installed first.

### vip is archived on CRAN

`vip` was removed from CRAN on 2026-07-08 ("issues were not corrected despite
reminder"), so `available.packages()` no longer lists it and a plain
`renv::install("vip")` fails. We pin `vip@0.4.6`, which Posit Package Manager still
serves as a binary, and the lockfile records it that way, so `renv::restore()`
works without reaching into the CRAN archive.

It works fine today, but it is unmaintained. `DALEXtra::explain_tidymodels()` with
`DALEX::model_parts()` gives model-agnostic permutation importance from maintained
packages, so §10 should show that route as well as `vip::vi()` rather than resting
the whole section on an archived package.

### renv rolls back everything on one failure

renv installs transactionally. One package failing at the end, such as `vip` failing to
download after 205 others had installed, discards the entire batch and leaves the
library as it was. The log reads "Successfully installed 205 packages" immediately
before the rollback, which is misleading: check the library, not the log.

When a large install fails on one package, install the troublesome package
separately first, then re-run the batch. The renv cache makes the second run take
seconds.

### Known install failure: gridExtra and rlang

A fresh install of the full set can die with:

```
Error: error testing if 'gridExtra' can be loaded
  there is no package called 'rlang'
```

`gridExtra` 2.3.1 declares `Imports: gtable, grid, grDevices, graphics, utils` in the
repository metadata, but at load time it needs `rlang` (through `gtable`). renv builds
its install order from that metadata, so it can load-test `gridExtra` before `rlang`
exists, and the whole transaction rolls back, leaving an empty library, which makes
it look worse than it is. Serialising installs does not help; the ordering is wrong,
not raced.

Fix: install the infrastructure first, then everything else.

```r
renv::install(c("rlang", "cli", "glue", "lifecycle", "vctrs", "gtable"))
renv::restore()   # or renv::install(<the rest>)
```

### What is installed, and for which section

| Packages | Used by |
| --- | --- |
| `tidyverse`, `tidymodels`, `here`, `knitr`, `rmarkdown` | everywhere |
| `skimr`, `naniar` | §2 EDA and missing-data patterns |
| `glmnet`, `rpart`, `rpart.plot`, `ranger`, `xgboost`, `nnet` | §3 model engines, §5 regularisation |
| `themis` | §2, §6 class imbalance |
| `sf`, `spatialsample` | §6, §7 spatial dependence and blocked resampling |
| `probably` | §7 thresholds and calibration |
| `tidyclust`, `embed` | §8 clustering and dimensionality reduction |
| `vip`, `DALEX`, `DALEXtra`, `pdp` | §10 feature importance and interpretation |
| `patchwork`, `ggrepel`, `gt` | figures and tables throughout |
| `reticulate` | running the Python tabs (see Python for the tabs) |

**Not installed: `torch` / `brulee` / `keras3`. Settled when §9 was written: not needed.**
Section 9 teaches neurons, layers, forward propagation and backpropagation with about
forty lines of base R, including a finite-difference gradient check, and uses `nnet`
through the parsnip `mlp` engine for everything else. Nothing in the section needs a
second layer, a GPU, or an autodiff framework.

Two consequences to keep in mind before adding one:

- `nnet` optimises with **BFGS**, not gradient descent, and parsnip maps `epochs` to
  `maxit`. There is no learning rate to tune. §9 says so explicitly in two places; a
  `torch`- or `keras`-backed engine would change that and those passages would need
  editing.
- A real deep-learning demonstration (convolutional or recurrent architectures on imagery
  or acoustics) needs libtorch, a ~2 GB runtime download beyond the R package, or a
  Python/TensorFlow stack, and would make CI restores heavy. §9's
  `when-a-network-pays-off.qmd` explains why those architectures matter and deliberately stops
  short of running one.

## Freeze

`_quarto.yml` sets:

```yaml
execute:
  freeze: auto
```

Rendered R results are cached in `_freeze/`, **which is committed**. Consequences:

- A page re-executes only when its source changes, so full builds stay fast.
- CI can render the site with Quarto alone: no R, no package installs, no
  multi-minute model fits on every push.
- If a page's output looks stale after changing a helper in `R/`, delete that page's
  folder under `_freeze/` and re-render.
- Commit `_freeze/` changes together with the page that produced them.

## Branching (gitflow)

| Branch | Role |
| --- | --- |
| `main` | What is published. Only receives merges from `release/*` and `hotfix/*`. |
| `develop` | Integration branch; day-to-day work merges here. |
| `feature/*` | One section, page, or contribution. Branch from `develop`. |
| `release/*` | Stabilise a batch of sections before publishing. |
| `hotfix/*` | Fix on top of `main` (broken build, wrong result, data permission problem). |

Naming: `feature/ch03-logistic-regression`, `feature/contrib-<author-slug>`,
`release/v0.2.0`, `hotfix/broken-freeze`.

Never commit directly to `main`. Commit and push only when asked.

## Publishing to GitHub Pages

The site is published at <https://hi-digital-ml-ai.github.io/ml-basic/> by `.github/workflows/publish.yml` (since
2026-10-15). It runs on every push to `main`, which only receives release and hotfix
merges, so a push to `main` is a release; it can also be run by hand from the Actions
tab. Watch a run with `gh run watch`.

- The workflow installs Quarto only (the same version as the laptop) and runs
  `quarto render`, then uploads `_site/` to Pages. The repo setting is Pages, source
  "GitHub Actions".
- It installs no R or Python packages, which works *because* `_freeze/` is committed:
  a page whose cache is missing or out of date fails in the workflow. Render it
  locally and commit its `_freeze/` folder with it. If that ever stops being
  practical, add `r-lib/actions/setup-r` and `setup-renv` and expect slow builds.
- The repo is public, so everything in its history is public too: never commit
  embargoed participant data (see `.claude/contributed-pages.md`).
- `site-url` in `_quarto.yml` and `SITE_URL` in `tools/extract-code.py` carry the
  address; the videos' end cards carry it as `SITE` in `_videos/mlbasic_video.py`.

Until 2026-10-15 the site's only home was Cloudflare Pages at `ml-basic.pages.dev`. GitHub
Pages became the main address because institutional networks, the institute's among
them, block all of `*.pages.dev`. The Cloudflare copy is kept as a second address; every
public link (descriptions, end cards, `site-url`) points to GitHub Pages.

## Before pushing

```bash
quarto render          # must complete with no errors
```

Check: no broken internal links, every new page appears in the sidebar and its
listing, every figure has a caption and alt text.

A page's downloadable scripts come from the same render, so a new page needs no
extra step. `WARN: Unable to resolve link target: downloads/...` means the
pre-render step did not run or the filter and `tools/extract-code.py` disagree about
which pages have code.
