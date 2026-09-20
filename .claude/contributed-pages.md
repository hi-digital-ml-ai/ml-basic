# Contributed pages

Pages that course participants produce from their own data. The participants are
**researchers, not students**: domain experts in fisheries, oceanography, ecology and
genomics who are new to ML but not to science. Treat a contribution as a colleague's
short paper, not as homework to be marked.

## Purpose

These pages are the payoff of the course: they show the same patterns the course
teaches applied to real, messy, domain-specific data. They are also the part readers
arrive at from outside, so they carry the site's credibility.

A contributed page runs in **R or in Python, one language per page**. R is the site
default and needs nothing declared. A Python page sets `engine: jupyter` in its front
matter, which makes Quarto execute its ```` ```{python} ```` chunks through the
jupyter engine, and uses `python/mlbasic_theme.py` for the house plotting style, as
an R page uses `R/theme.R`.

This is the one place on the site where Python executes. The Python tabs in sections
2, 3, 5, 7, 8 and 10 are still displayed and never run, and a contributed page does
not carry tabsets at all: it is one analysis in one language, not the same step shown
twice.

Rendering a Python page locally needs `jupyter` and `matplotlib` on top of
`python/requirements.txt`. Nothing changes for CI, because `_freeze/` is committed,
so the author must commit the freeze their render produces. A page whose freeze is
missing forces a Python environment onto every later build.

## Where they live

```
contributed/
  index.qmd                       listing page
  writing-a-contributed-page.qmd  the reader-facing version of this doc
  _template-r.qmd                 starting point, analysis in R
  _template-python.qmd            starting point, analysis in Python
  2026-<author-slug>-<topic>.qmd  e.g. 2026-nakamura-otolith-ageing.qmd
  img/                            figures, prefixed with the author slug
```

`writing-a-contributed-page.qmd` says all of this to the contributor in the site's
own voice, so the two move together: change a rule here and change it there. The
index listing globs `20*.qmd`, which is what keeps the guide page off the cards, so
a contribution whose filename lacks the year prefix will not appear.

Front matter is mandatory and complete:

```yaml
---
title: "Predicting otolith age class from shape descriptors"
description: "A random forest applied to 1,240 otolith images from coastal surveys"
author: "Name, Institution"
date: 2026-09-15
categories: [case-study, classification, trees-ensembles]
---
```

`case-study` plus the method categories that actually apply, from the vocabulary in
`.claude/site-structure.md`.

## Data handling

Before publishing anything, confirm with the author:

- **Is the data shareable?** Much marine data is embargoed, licensed, or covered by
  a data-sharing agreement. Default to *not* committing it.
- If not shareable: publish the page with a small synthetic or aggregated stand-in in
  `data/`, and state plainly at the top of the page that the figures use stand-in data.
  Never present synthetic results as if they were the real survey results.
- If shareable: file under `data/`, keep it under 5 MB, and record source,
  collection period, licence and citation at the top of the page.
- Strip anything sensitive: precise locations of protected or commercially valuable
  species, vessel identifiers, personal data.

## Editing contributions

Preserve the author's voice and their scientific judgement. Edit for:

- broken or non-reproducing code, missing seeds, missing `renv` dependencies;
- **methodological traps the course itself warns about**: leakage, random CV on
  spatially autocorrelated data, accuracy reported on an imbalanced problem,
  extrapolation beyond the sampled range. Raise these with the author rather than
  silently rewriting the analysis; if they stand by it, publish with a note.
- consistency of headings, figure captions, alt text and categories.

Do not impose the chapter page skeleton on a contribution; its shape follows the
author's analysis. Do keep the "Key points" callout and figure alt text.

## Review flow

1. Author supplies a `.qmd` (or `.R` plus notes) and any shareable data.
2. Branch `feature/contrib-<author-slug>`, add the page, render locally, check it
   builds clean and the figures read well at page width.
3. Confirm data permissions and the points above with the author.
4. PR into `develop`; the author signs off on the rendered page before merge.

Never publish a contribution to `main` before the author has seen it rendered.
