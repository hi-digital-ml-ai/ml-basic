# Authoring guide

How a chapter page should read, compute, and look. Applies to everything under
`chapters/`; `contributed/` pages follow it loosely (see
`.claude/contributed-pages.md`).

## Voice

The reader is a working marine scientist who knows their own field well and ML not
at all. They are not a beginner in general — do not talk down — but every ML term is
new.

- **Concept → marine example → code → interpretation.** In that order. A page that
  opens with a code block has been written backwards.
- Define each jargon term the first time it appears, in one sentence, inline.
  "A *feature* is simply one of the measured variables you feed the model — depth,
  temperature, chlorophyll."
- Short sentences. Active voice. Say "we" for what the page does together with the
  reader.
- Equations are welcome but always follow a plain-English statement of the same
  idea, and every symbol gets named. Use a `::: {.callout-note collapse="true"}`
  block titled "The maths, if you want it" when the equation is optional depth.
- Avoid ML folklore and unexplained rules of thumb ("use 80/20"). If a number is
  conventional rather than principled, say so.
- British spelling: modelling, generalisation, centre, behaviour.

## Page skeleton

```markdown
---
title: ...
description: ...
categories: [...]
---

## Why this matters            <- 2–4 sentences, marine motivation
## The idea                    <- plain English, usually with a figure
## Worked example              <- tidymodels on a dataset from data/
## What the results mean       <- interpretation, and what would go wrong
## Where this breaks down      <- honest limitations; links to §6
## Key points                  <- callout-tip, 3–5 bullets
## Try it yourself             <- 1–2 small exercises (optional)
```

Aim for 1,000–1,800 words plus code. If a page runs longer, split it.

## Code

- tidymodels idiom throughout: `initial_split()` → `recipe()` → `*_spec()` →
  `workflow()` → `fit()` → `predict()` → `yardstick` metrics. Show the workflow even
  when a one-liner would do — the point is the pattern.
- `set.seed()` before anything random, in the same chunk.
- Chunks are labelled and echoed: `#| label: fit-forest`, `#| echo: true`.
  Setup chunks use `#| include: false`.
- Keep chunks short enough to explain in the prose that follows. One idea per chunk.
- Prose between chunks, never two code chunks back to back without explanation.
- No `install.packages()` in pages — dependencies go through `renv`
  (see `.claude/workflow.md`).
- Load shared helpers with `source(here::here("R/theme.R"))`; paths are always
  `here::here()`, never relative or absolute.
- Long-running fits: keep under ~30 s per page where possible and rely on
  `freeze: auto`. If a fit is genuinely slow, cache its result into `data/` with a
  script in `R/` rather than letting the page grind on every render.

### Python tabs

Pages in sections 2, 3, 5, 7, 8 and 10 show each modelling step twice, R and
scikit-learn, in a tabset. The R chunk is the one that runs, so its output
appears under the R tab; the Python block is displayed only.

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

- `group="language"` syncs every tabset on the page, so choosing Python once
  chooses it throughout.
- Wrap the modelling steps, not the figures. Figures stay R-only, and so does
  any step with no honest Python counterpart — `mgcv`'s smooth table, for one.
  A missing tab is information, not an omission to fill in.
- The Python is cumulative down the page, exactly as the R chunks are, and must
  run: `python/check-snippets.py` executes every snippet in the site. Do not add
  a tab you have not run.
- Load data through `python/mlbasic_data.py`, never by reading `data/*.csv`
  directly, so the two halves clean the survey the same way.
- Where a default differs between the two — regularisation, event level, the
  need for scaled inputs — say so in a comment in the Python block. That
  difference is usually the most useful thing on the page.
- Add `{{< include ../../_snippets/python-tabs.qmd >}}` under the data note, so
  the reader knows the Python is not what produced the numbers.

## Figures

Figures carry most of the teaching here, so they are worth real effort.

- Every page has at least one figure. Prefer a picture of the *concept*
  (overfitting as a wiggly line through noisy points) over a table of numbers.
- Generated with ggplot2 using `R/theme.R`, so the whole site shares one look.
- Every figure gets `#| fig-cap:` and `#| fig-alt:`. The alt text describes what the
  figure shows, for a reader who cannot see it — it is not a duplicate of the caption.
- Label directly on the plot where possible instead of relying on a legend.
- Colour must survive greyscale and colour-blind viewers: use viridis or Okabe–Ito,
  never red/green for a two-class contrast.
- Hand-drawn or diagrammatic figures (neural-network schematics, the train/test
  split) go in the section's `img/` folder as SVG.
- Figure dimensions set per chunk (`#| fig-width: 7`, `#| fig-height: 4.5`), not
  globally, so nothing is squashed.

## Callouts

| Callout | Use for |
| --- | --- |
| `callout-note` | Optional depth, maths, side remarks |
| `callout-tip` | "Key points" summary at the end of every page |
| `callout-warning` | Common mistakes, leakage traps, misuse of a metric |
| `callout-important` | Things that invalidate results if ignored |

## Cross-references

Link forward and back between sections by relative path — the threads listed at the
bottom of `.claude/curriculum.md` should be visibly linked, not just implied.
Use Quarto cross-refs (`@fig-...`, `@eq-...`) for figures and equations within a page.
