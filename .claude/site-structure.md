# Site structure

## Two axes: sections navigate, categories cross-cut

The syllabus is a *course*, so the ten sections are the primary navigation: an
ordered sidebar, read front to back. Methods are the *secondary* axis: a reader who
wants "everything about random forests" should get chapter pages and participant
contributions together, which sections alone cannot give.

So we use both:

- **Sections → sidebar chapters.** Ordered, numbered, one folder each.
- **Methods/themes → `categories`.** Quarto listing metadata, rendered as clickable
  tags on `chapters/index.qmd` and `contributed/index.qmd`.

A page belongs to exactly one section but may carry 1–3 categories.

## Category vocabulary

Controlled list. Add a new one only by editing this file, so tags do not fragment
(`random-forest` vs `random-forests` vs `rf`).

| Category | Covers |
| --- | --- |
| `foundations` | What ML is, learning types, prediction vs explanation |
| `marine-data` | Data types specific to marine work: profiles, tracks, surveys, acoustics |
| `data-preparation` | Cleaning, recipes, encoding, scaling, splitting, leakage |
| `eda` | Exploratory analysis and visualisation before modelling |
| `supervised` | Any supervised-learning page (umbrella) |
| `regression` | Continuous responses, linear/polynomial regression |
| `classification` | Categorical responses, logistic regression |
| `trees-ensembles` | Decision trees, random forests, boosting |
| `optimisation` | Loss functions, gradient descent, MLE, MAP |
| `generalisation` | Over/underfitting, bias–variance, complexity, regularisation |
| `tuning` | Hyperparameter search, grids, `tune` |
| `assumptions` | Independence, linearity, distributions, extrapolation |
| `spatial-temporal` | Spatial/temporal dependence and blocked resampling |
| `class-imbalance` | Rare events, resampling, imbalance-aware metrics |
| `validation` | Cross-validation and resampling schemes |
| `metrics` | Performance measures, confusion matrix, ROC/PR |
| `uncertainty` | Intervals, stability, communicating uncertainty |
| `unsupervised` | Clustering, PCA, dimensionality reduction |
| `neural-networks` | Neurons, layers, backpropagation, deep learning |
| `interpretation` | Feature importance, explainability, black-box vs interpretable |
| `reproducibility` | Transparent reporting, seeds, environments, data provenance |
| `case-study` | Participant contributions using their own data |
| `toolkit` | Orientation in a language or library rather than in a method |

## Files and naming

```
_quarto.yml
index.qmd                          landing page: what the course is, how to use it
glossary.qmd                       every term, A to Z, generated from _glossary.yml
_glossary.yml                      one entry per term: definition, the page that introduces it
img/video/                         YouTube thumbnails for the further-resources lists,
                                   named <video-id>.jpg, fetched once and committed
toolkit/
  r-with-tidymodels.qmd            the pipeline shape, run once end to end
  python-with-scikit-learn.qmd     the same shape in scikit-learn, and where the two differ
  img/                             the two shape diagrams, shared by both pages
chapters/
  index.qmd                        listing of all chapter pages, filterable by category
  01-introduction/
    index.qmd                      section overview + its own listing
    prediction-and-explanation.qmd
    img/                           figures authored for this section
  02-marine-data/
  ... 10 sections, see .claude/curriculum.md
contributed/
  index.qmd                        listing of participant pages
  2026-<author-slug>-<topic>.qmd
data/                              small (<5 MB) example datasets, CSV or RDS
R/
  theme.R                          shared ggplot theme + palette
  data.R                           loaders for data/
tools/
  extract-code.py                  pre-render: pages -> downloads/code/<section>/<page>.{R,py}
  code-downloads.lua               filter: the "Code from this page" line
  glossary.lua                     shortcodes: the "New terms on this page" box, the Glossary
downloads/                         generated, git-ignored: the scripts and the zip
_freeze/                           committed render cache
```

Nothing in `downloads/` is authored or committed. It is generated from the pages on
every build and copied into the site through `resources:`; see `tools/README.md`.

- Folders and files: `kebab-case`; chapter folders prefixed `NN-`.
- Pages may be renamed, merged or removed without a redirect while the site is in
  development (user, 2026-10-07). Once it is shared publicly, add `aliases:` in the
  front matter of a page that replaces an old address.

## Page front matter

Every content page starts with:

```yaml
---
title: "Logistic regression"
description: "Predicting presence/absence from environmental covariates"
categories: [supervised, classification]
author: "..."          # chapter pages may omit; contributed pages must not
date: 2026-09-15
---
```

`description` is what shows on listing cards, so write it for a reader scanning the
index, not as a restatement of the title.

## Listings

Each `chapters/NN-slug/index.qmd` is kept short (since 2026-10-15): the title and
description, **one paragraph** on what the section covers, the section's video, a card
grid of its pages with **one sentence each**, then Further resources.

```yaml
listing:
  id: pages
  # Each card takes its title from the page and gives it one sentence here.
  contents:
    - path: underfitting-and-overfitting.qmd
      description: "A model that fits its training stations too loosely or too closely ..."
    - path: bias-variance.qmd
      description: "..."
  type: grid
  grid-columns: 3
  sort: "order"
  fields: [title, description]
toc: false
```

The card sentences live in the overview, not in a field on each page: the render
cache (`_freeze/`) is keyed on the whole page file, front matter included, so a new
field on a page would re-run all of its R code. A page's own `description` stays
longer; it sits under the page's title and in the course index. A new page needs a
line here as well as in the sidebar.

The `id:` matters. Without it Quarto appends the listing at the end of the
document; with it, the cards render where the matching div sits:

```markdown
## Pages in this section

::: {#pages}
:::
```

The video sits just above that heading, as `{{< video https://www.youtube.com/watch?v=<id> title="..." >}}`.

`chapters/index.qmd` and `contributed/index.qmd` use `type: table` with
`categories: true`, so the topic filter is the point of those pages.

## Code tabsets

Sections 2, 3, 4, 5, 7, 8 and 10, the pages that teach the modelling pipeline and
how its models are fitted, show each step as an R and a Python tab:

````markdown
::: {.panel-tabset group="language"}

## R

```{r}
#| label: fit
...
```

## Python

```python
...
```

:::
````

`group="language"` ties every tabset on the page together, so one click switches
all of them. Quarto keeps tabset headings out of the table of contents, so the
`##` levels here do not disturb `toc-depth: 3`.

**The R chunk is the only one that executes.** Its table therefore renders under
the R tab and not the Python one. That was the deliberate choice over splitting
each chunk in two and printing the output below the tabset: it leaves every
executing chunk exactly as it was, so `_freeze/` and the numbers on the page are
unaffected by the tabs.

**What gets a tab.** Modelling steps do. Figure chunks stay R-only, because the site's
figures are all ggplot2, which is the point of `R/theme.R`. Steps with no honest
Python counterpart also stay R-only: `summary(gam)$s.table` has no equivalent,
and inventing one would teach something false.

The Python is not decoration. `python/check-snippets.py` extracts every
```` ```python ```` block, concatenates each page's blocks in order, since they are
cumulative exactly as the R chunks are, and runs the result. It reports a
page that only warns as well as one that fails, because a convergence warning
means the snippet is subtly wrong. Data comes from `python/mlbasic_data.py`,
which mirrors `R/data.R` step for step; the cleaned survey was checked against
the R loader (800 rows, identical NA counts, identical substrate levels).

Each converted page carries `{{< include ../../_snippets/python-tabs.qmd >}}`
under the data note, saying that the numbers shown came from R and that Python's
own random streams put the splits elsewhere.

Dependencies are in `python/requirements.txt`: pandas and scikit-learn
throughout, `statsmodels` where scikit-learn reports no standard errors (GLM
inference, negative binomial), `scipy` for the optimiser and quasi-random
designs, `umap-learn` in section 8. None of them is needed to build the site.

## Page layout

The site is full-width: a docked sidebar on the left, wide body, margin TOC.

```yaml
format:
  html:
    page-layout: full
    grid:
      sidebar-width: 300px
      body-width: 1250px
      margin-width: 250px
      gutter-width: 1.6rem
```

`page-layout: full` on its own does **not** widen the body; it still honours the
grid's `body-width`, which defaults to 800px. Both are needed.

The width is for figures, tables and code, not for prose. `styles.scss` keeps
paragraphs, list items and the YAML `description` at a 42rem measure while
letting everything else use the column:

| Element | Width at a 1680px window |
| --- | --- |
| content column | 1116px |
| paragraphs, list items | 714px |
| figures | 1020px (capped at 60rem, centred with their caption) |
| `.diagram` figures | 1116px (full column; SVG diagrams are text, not plots) |
| tables, code blocks | 1116px (full column) |

The `description` is emitted as a `div`, not a `p`, so it needs its own rule or
it runs the whole column.

**Do not set `toc-depth: 2`.** In Quarto 1.9.38 it emits the table of contents as
`<ul class="collapse">` and nothing ever adds `show`, so the TOC renders as a
heading with no entries. `toc-expand` does not fix it. `toc-depth: 3` works, and
is shallow in practice, since pages average 7 `##` and 2 `###` headings, and Quarto
reveals the `###` entries contextually as you scroll.

## Sidebar

`_quarto.yml` lists the ten sections at the top level of `contents:`, each
expandable to its pages, with `style: docked` and `collapse-level: 1`. All ten
section titles stay visible; Quarto expands the one containing the current page.
Keep section labels short enough for one line in a 300px rail: "10 · Interpretation",
not "10 · Interpretation & responsible use".

`Toolkit` sits above section 1, holding the two language orientation pages. It is
outside the numbered sections on purpose: it teaches a library, not a concept, and the
curriculum is ten sections. It carries no `index.qmd`, so the sidebar label is a group
rather than a link, exactly as `More` is. Its pages therefore do not appear on
`chapters/index.qmd`, whose listing is `*/index.qmd` under `chapters/`.

`More` sits at the bottom with the course index and `contributed/`. The sidebar is
the table of contents for the course; do not hide chapter pages from it.
