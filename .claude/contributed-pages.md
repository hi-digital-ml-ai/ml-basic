# Contributed pages

Pages that course participants produce from their own data. The participants are
**researchers, not students** — domain experts in fisheries, oceanography, ecology,
genomics — who are new to ML but not to science. Treat a contribution as a colleague's
short paper, not as homework to be marked.

## Purpose

These pages are the payoff of the course: they show the same tidymodels patterns
applied to real, messy, domain-specific data. They are also the part readers arrive
at from outside, so they carry the site's credibility.

## Where they live

```
contributed/
  index.qmd                       listing page
  2026-<author-slug>-<topic>.qmd  e.g. 2026-nakamura-otolith-ageing.qmd
  img/                            figures, prefixed with the author slug
```

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
- **methodological traps the course itself warns about** — leakage, random CV on
  spatially autocorrelated data, accuracy reported on an imbalanced problem,
  extrapolation beyond the sampled range. Raise these with the author rather than
  silently rewriting the analysis; if they stand by it, publish with a note.
- consistency of headings, figure captions, alt text and categories.

Do not impose the chapter page skeleton on a contribution — its shape follows the
author's analysis. Do keep the "Key points" callout and figure alt text.

## Review flow

1. Author supplies a `.qmd` (or `.R` plus notes) and any shareable data.
2. Branch `feature/contrib-<author-slug>`, add the page, render locally, check it
   builds clean and the figures read well at page width.
3. Confirm data permissions and the points above with the author.
4. PR into `develop`; the author signs off on the rendered page before merge.

Never publish a contribution to `main` before the author has seen it rendered.
