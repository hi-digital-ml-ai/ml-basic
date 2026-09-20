# Authoring guide

How a chapter page should read, compute, and look. Applies to everything under
`chapters/`; `contributed/` pages follow it loosely (see
`.claude/contributed-pages.md`).

## Voice

The reader is a working marine scientist who knows their own field well and ML not
at all. They are not a beginner in general, so do not talk down, but every ML term is
new.

- **Concept → marine example → code → interpretation.** In that order. A page that
  opens with a code block has been written backwards.
- Define each jargon term the first time it appears, in one sentence, inline.
  "A *feature* is simply one of the measured variables you feed the model: depth,
  temperature, chlorophyll."
- Short sentences. Active voice. Say "we" for what the page does together with the
  reader.
- Equations are welcome but always follow a plain-English statement of the same
  idea, and every symbol gets named. Use a `::: {.callout-note collapse="true"}`
  block titled "The maths, if you want it" when the equation is optional depth.
- Avoid ML folklore and unexplained rules of thumb ("use 80/20"). If a number is
  conventional rather than principled, say so.
- British spelling: modelling, generalisation, centre, behaviour.
- **No em dashes (—) anywhere.** An em dash is always standing in for a comma, a
  colon, a semicolon, a full stop or a pair of brackets, and naming which one makes
  the sentence say what it means. A parenthetical pair becomes commas or brackets; an
  elaboration becomes a colon; two independent clauses become two sentences. This
  applies to prose, YAML `description:` fields, figure captions, alt text, table cells
  and code comments alike.
- En dashes stay where they are typographically right: numeric ranges (`2–16 °C`) and
  coupled-noun compounds (bias–variance, Bray–Curtis, temperature–salinity). Do not
  use one as punctuation in a sentence.

## Page skeleton

```markdown
---
title: ...
description: ...
categories: [...]
---

## <the motivation, named>     <- 2–4 sentences, marine motivation
## The idea                    <- plain English, usually with a figure
## Worked example              <- tidymodels on a dataset from data/
## <what the results say>      <- interpretation, and what would go wrong
## Limits of <this thing>      <- honest limitations; links to §6
## Key points                  <- callout-tip, 3–5 bullets
## Try it yourself             <- 1–2 small exercises (optional)
```

**Headings are declarative, and named for the page.** The first, fourth and fifth
slots used to read "Why this matters", "What the results mean" and "Where this breaks
down" on every page, which told a reader scanning the sidebar nothing and made
seventy pages look like one. Write what the section actually says instead: "A debt
from two earlier pages", "Two measures, two winners", "Limits of a single split".
Avoid opening a heading with Why, What, Where, How, Which, When or Does; a question
as a heading postpones the answer that the section is about to give. `The idea`,
`Worked example`, `Key points` and `Try it yourself` stay fixed, because they are
labels rather than claims.

Aim for 1,000–1,800 words plus code. If a page runs longer, split it.

### Further resources

Section index pages and the two `toolkit/` pages end with a `## Further resources`
block, after everything else. Individual chapter pages do not: seventy link lists
would repeat the same handful of sources and rot at seventy separate rates.

The block is two labelled lists, **Documentation** then **Video**, each entry a link
followed by the source and one clause saying why it earns its place. A link with no
reason attached is a bookmark, not a resource.

The video list carries thumbnails. Wrap it in a `::: {.video-list}` div and give each
entry a linked thumbnail of its own, on the line above the text:

```markdown
::: {.video-list}
- [![](../../img/video/4jRBRDbJemM.jpg){.video-thumb fig-alt="ROC and AUC, Clearly Explained, on YouTube" loading="lazy"}](https://www.youtube.com/watch?v=4jRBRDbJemM)

  [ROC and AUC, Clearly Explained](https://www.youtube.com/watch?v=4jRBRDbJemM), StatQuest with Josh Starmer. Builds the curve one threshold at a time.
:::
```

The blank line inside the bullet is load-bearing: it makes the item two paragraphs,
which is what `.video-list li` lays out side by side. One video per bullet, so every
entry has one thumbnail; pair two related videos as two bullets, not one.

Thumbnails live in `img/video/<video-id>.jpg`, one shared folder at the repo root
rather than the per-section `img/` folders, which hold figures made for this site.
Fetch each one once, at render-independent size, and commit it:

```bash
curl -o img/video/<video-id>.jpg https://i.ytimg.com/vi/<video-id>/mqdefault.jpg
```

Committing them rather than hotlinking `i.ytimg.com` keeps the build offline, keeps
the images stable when a channel changes its artwork, and means a reader's browser
never calls Google to read a page. A thumbnail that comes back at about 1 kB is the
grey placeholder for a video that no longer exists, which is a second check on the
link. The alt text is the video title followed by `, on YouTube`, because the
thumbnail is a link and a link needs a name. It goes in `fig-alt`, not in the `![...]`
brackets: an image alone in a paragraph with bracket alt text is an implicit figure to
Quarto, which renders the alt text a second time as a visible caption.

Rules for what goes in it:

- **Check every URL before committing it.** A documentation page must return 200; a
  video must resolve through `https://www.youtube.com/oembed?url=...&format=json`,
  which also returns the real channel name. Search-result summaries misattribute
  videos, so the channel a search claims is not evidence.
- **Video comes from channels with a teaching record**: StatQuest, 3Blue1Brown,
  Julia Silge, Posit PBC, PyData, Data School. English only.
- **Documentation is upstream documentation**, tidymodels and scikit-learn, not blog
  posts about them. `tmwr.org` and Molnar's *Interpretable Machine Learning* are the
  exceptions, both being free books by the people who wrote the tools.
- Prefer a page that covers what the section actually argues. The scikit-learn
  leakage section belongs with §2, its grouped-data section with §6 and §7.
- Nobody here has watched every linked video end to end. Treat the list as reviewed
  for source and topic, not for content, and check it before publishing to `main`.

## Code

- tidymodels idiom throughout: `initial_split()` → `recipe()` → `*_spec()` →
  `workflow()` → `fit()` → `predict()` → `yardstick` metrics. Show the workflow even
  when a one-liner would do; the point is the pattern.
- `set.seed()` before anything random, in the same chunk.
- Chunks are labelled and echoed: `#| label: fit-forest`, `#| echo: true`.
  Setup chunks use `#| include: false`.
- Keep chunks short enough to explain in the prose that follows. One idea per chunk.
- Prose between chunks, never two code chunks back to back without explanation.
- No `install.packages()` in pages; dependencies go through `renv`
  (see `.claude/workflow.md`).
- Load shared helpers with `source(here::here("R/theme.R"))`; paths are always
  `here::here()`, never relative or absolute.
- Long-running fits: keep under ~30 s per page where possible and rely on
  `freeze: auto`. If a fit is genuinely slow, cache its result into `data/` with a
  script in `R/` rather than letting the page grind on every render.

### Python tabs

Pages in sections 2, 3, 5, 7, 8 and 10 show each modelling step twice, R and
scikit-learn, in a tabset. The two `toolkit/` pages are the exception: they are
single-language orientation pages, one per library, and carry no tabsets. The R chunk is the one that runs, so its output
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
  any step with no honest Python counterpart, such as `mgcv`'s smooth table.
  A missing tab is information, not an omission to fill in.
- The Python is cumulative down the page, exactly as the R chunks are, and must
  run: `python/check-snippets.py` executes every snippet in the site. Do not add
  a tab you have not run.
- Load data through `python/mlbasic_data.py`, never by reading `data/*.csv`
  directly, so the two halves clean the survey the same way.
- Where a default differs between the two, whether regularisation, event level or the
  need for scaled inputs, say so in a comment in the Python block. That
  difference is usually the most useful thing on the page.
- Add `{{< include ../../_snippets/python-tabs.qmd >}}` under the data note, so
  the reader knows the Python is not what produced the numbers.

## Figures

Figures carry most of the teaching here, so they are worth real effort.

- Every page has at least one figure. Prefer a picture of the *concept*
  (overfitting as a wiggly line through noisy points) over a table of numbers.
- Generated with ggplot2 using `R/theme.R`, so the whole site shares one look.
- Every figure gets `#| fig-cap:` and `#| fig-alt:`. The alt text describes what the
  figure shows, for a reader who cannot see it; it is not a duplicate of the caption.
- Label directly on the plot where possible instead of relying on a legend.
- Colour must survive greyscale and colour-blind viewers: use viridis or Okabe–Ito,
  never red/green for a two-class contrast.
- Hand-drawn or diagrammatic figures (neural-network schematics, the train/test
  split) go in the section's `img/` folder as SVG.
- A box-and-arrow diagram goes in `::: {.diagram}`, which lifts the 60rem figure cap
  and lets it use the whole content column:

  ````markdown
  ::: {.diagram}
  ![The caption.](img/ml-pipeline.svg){fig-alt="..."}
  :::
  ````

  A plot stays legible as it shrinks because its axes shrink with it. A diagram is
  text at a fixed size inside boxes, so it needs the room. The wrapper also works for
  a diagram with no caption, which would otherwise sit at the 42rem prose measure
  because a bare image is a paragraph. Give the SVG `width="100%"` and a `viewBox`, so
  it scales, and check that every text line still sits inside its box after an edit:
  the `y` of the last line plus a few pixels for descenders must clear the rectangle.
- Figure dimensions set per chunk (`#| fig-width: 7`, `#| fig-height: 4.5`), not
  globally, so nothing is squashed.

## Code readers can download

Every page's code is pulled out into a runnable script on each build, and offered
at the top of the page as `<page>.R`, `<page>.py` and a whole-course zip. Nothing
is maintained by hand, so there is nothing extra to write. Two habits keep the
scripts working:

- **A page's chunks are one cumulative program, in the order they appear.** That is
  already how the site renders, so the constraint is not new; it does mean not
  relying on a variable defined on a different page.
- **Libraries and `source()` calls go in the hidden `setup` chunk**, which is
  extracted like any other. A chunk that quietly depends on a package loaded
  nowhere on the page will render fine here and fail for a reader.

Give every chunk a `#| label:`, which is a rule anyway: the label becomes the
section heading in the downloaded script, so `#| label: fit-forest` is worth more
than `#| label: chunk-6`. See `tools/README.md` for how the extraction works.

## Callouts

| Callout | Use for |
| --- | --- |
| `callout-note` | Optional depth, maths, side remarks |
| `callout-tip` | "Key points" summary at the end of every page |
| `callout-warning` | Common mistakes, leakage traps, misuse of a metric |
| `callout-important` | Things that invalidate results if ignored |

## Cross-references

Link forward and back between sections by relative path; the threads listed at the
bottom of `.claude/curriculum.md` should be visibly linked, not just implied.
Use Quarto cross-refs (`@fig-...`, `@eq-...`) for figures and equations within a page.
