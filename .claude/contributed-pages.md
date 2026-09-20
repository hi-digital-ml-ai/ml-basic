# Contributed pages

Pages that course participants produce from their own data. The participants are
**researchers, not students**: domain experts in fisheries, oceanography, ecology and
genomics who are new to ML but not to science. Treat a contribution as a colleague's
short paper, not as homework to be marked.

## Purpose

These pages are the payoff of the course: they show the same tidymodels patterns
applied to real, messy, domain-specific data. They are also the part readers arrive
at from outside, so they carry the site's credibility.

Contributed pages are **R-only**. The site's build executes R and nothing else,
and the Python tabs in sections 2, 3, 5, 7, 8 and 10 are displayed, never run, so a
page whose results come from Python has no way to produce them here. If a
contributor works in Python, that is a conversation to have before the page is
written, not a tab to bolt on afterwards.

## Where they live

```
contributed/
  index.qmd                       listing page
  writing-a-contributed-page.qmd  the reader-facing version of this doc
  _template.qmd                   starting point for a new contribution
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
