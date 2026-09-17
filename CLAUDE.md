# ml-basic: Machine Learning Basics for Marine Science

Static course website built with **Quarto + R**, explaining core machine-learning
concepts in **plain English** with **tidymodels** examples and plenty of figures.

Audience: marine researchers with mixed backgrounds (ecology, oceanography,
fisheries, genomics) who are motivated and numerate, but not ML specialists. Pages that
participants produce from their own data are published under `contributed/`.

Repo: <https://github.com/hi-digital-ml-ai/ml-basic> (private; publishes to GitHub Pages).

## Layout

```
_quarto.yml          site config, sidebar, listing definitions
index.qmd            landing page
chapters/NN-slug/    one folder per course section (10 sections)
  index.qmd            section overview + listing of its pages
  *.qmd                one page per subtopic
  img/                 hand-made figures for that section
contributed/         participant pages (one .qmd per contribution)
data/                small example datasets committed to the repo
R/                   shared helpers: ggplot theme, data loaders, tidymodels utils
python/              the scikit-learn half of the code tabsets (never rendered)
_freeze/             committed render cache; CI renders without R
.claude/             detail docs (see below)
```

## Commands

```bash
quarto preview                 # local site with live reload
quarto render                  # full build into _site/
quarto render chapters/03-supervised-learning/logistic-regression.qmd
Rscript -e 'renv::restore()'   # sync R packages
Rscript -e 'renv::snapshot()'  # after adding a package
python python/check-snippets.py  # run every Python tab in the site
```

## Conventions

- **Plain English first.** Explain the idea and its marine-science meaning before any
  equation. Equations are optional depth, never the entry point.
- **British spelling** to match the syllabus: modelling, generalisation, centre.
- **No em dashes.** Use a comma, colon, semicolon, full stop or brackets, whichever
  the sentence actually needs. En dashes stay for numeric ranges and coupled-noun
  compounds only. See `.claude/authoring-guide.md`.
- **Headings are declarative and page-specific**, not "Why this matters" or "What the
  results mean" repeated on every page, and not phrased as questions.
- **tidymodels is the default toolkit** (`recipes` → `parsnip` → `workflows` →
  `rsample`/`tune` → `yardstick`). Show base-R or other packages only to contrast.
- **Modelling steps carry a Python tab.** In sections 2, 3, 5, 7, 8 and 10 each
  modelling chunk sits in a `panel-tabset` with its scikit-learn equivalent. The
  R tab is the one Quarto runs; the Python is displayed only, and is kept honest
  by `python/check-snippets.py`. See `.claude/authoring-guide.md`.
- **Every page** carries YAML `title`, `description`, `categories`, and ends with a
  *Key points* callout. Categories come from the controlled list in
  `.claude/site-structure.md`; do not invent new ones ad hoc.
- **Examples are marine examples.** Prefer the datasets in `data/`; never invent
  numbers that look like real survey results.
- Files and folders are `kebab-case`; chapter folders are `NN-slug`.

## Branching

gitflow: `main` (published site), `develop` (integration), `feature/*`, `release/*`,
`hotfix/*`. Never commit directly to `main`. Do not commit or push unless asked.

## Detail docs

| File | Contents |
| --- | --- |
| `.claude/curriculum.md` | The 10 sections and their subtopics (tentative, editable) |
| `.claude/site-structure.md` | File layout, navigation, category vocabulary, naming |
| `.claude/authoring-guide.md` | Writing, code, and figure style for chapter pages |
| `.claude/contributed-pages.md` | How participant pages are added and reviewed |
| `.claude/workflow.md` | Build, freeze, renv, gitflow, GitHub Pages deployment |
