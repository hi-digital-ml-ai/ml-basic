# Site structure

## Two axes: sections navigate, categories cross-cut

The syllabus is a *course*, so the ten sections are the primary navigation — an
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

## Files and naming

```
_quarto.yml
index.qmd                          landing page: what the course is, how to use it
chapters/
  index.qmd                        listing of all chapter pages, filterable by category
  01-introduction/
    index.qmd                      section overview + its own listing
    what-is-machine-learning.qmd
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
_freeze/                           committed render cache
```

- Folders and files: `kebab-case`; chapter folders prefixed `NN-`.
- Never rename a published page without adding a redirect in `_quarto.yml`
  (`aliases:` in the page front matter) — links get shared.

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

`chapters/index.qmd` and `contributed/index.qmd` use Quarto listings:

```yaml
listing:
  contents: "*/*.qmd"
  type: grid
  categories: true
  sort: "title"
  fields: [image, title, description, categories]
```

Give each page an `image:` when a representative figure exists — the grid looks
broken with a mixture of thumbnails and blanks, so within one listing either all
pages have images or none do.

## Sidebar

`_quarto.yml` lists the ten sections in order, each expandable to its pages.
`contributed/` sits at the bottom as its own section. The sidebar is the table of
contents for the course; do not hide chapter pages from it.
