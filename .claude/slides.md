# Slide decks

One reveal.js deck per section, for teaching a section or reviewing it. Added
2026-10-15 at the user's request; the menu entry is **Slides**.

```
slides.qmd                    the Slides page: a listing of the ten decks, and the keys
slides/
  _metadata.yml               format: revealjs for every file here (1280 x 720, shared
                              theme, controls); this is why the listing page sits outside
  NN-slug.qmd                 one deck per section, named like its chapter folder
  assets/slides.scss          the five themes as CSS variables, the slide parts, the
                              classes the inline diagrams use
  assets/controls.html        signposts, contents tiles, plot crops, the control bar,
                              the theme menu, the laser pointer, the T and L keys
  assets/theme-init.html      applies the remembered theme before the first paint
  figures/                    generated, git-ignored: the plots the decks show
tools/slide-figures.py        pre-render: copies those plots out of _freeze/
```

## Rules from the user (2026-10-15)

- Each page of a section gets **two slides**: one for the idea, background and
  motivation, one for an example. Three when two are not enough, **never four**. A deck
  also has a title slide, an "In this section" contents slide and a closing "Key
  points" slide.
- **Visuals first.** Diagrams, illustrations and the pages' own plots over text. One
  main idea per slide, short plain sentences, nothing that needs every detail spelled
  out. The audience has a wide range of backgrounds.
- **No em or en dashes, and no semicolons or colons joining sentences or clauses**,
  on the slides, in the speaker notes and in the diagrams' text. Use two sentences or
  "and". (Ranges are written "5 to 195 m".) Course-wide rules still apply: British
  spelling, simulated data never presented as real, no invented numbers that look like
  results.
- One consistent visual style across all decks.
- Controls to switch theme and to turn the cursor into a laser pointer.

## Anatomy of a deck

```markdown
## The data decide the kind of learning {#types-of-learning .idea data-page="Types of learning" data-href="../chapters/01-introduction/types-of-learning.html"}

(an inline SVG in a ```{=html} block, inside <div class="visual">)

::: {.takeaway}
One sentence that carries the slide.
:::

::: notes
Speaker notes: what to say, a few plain sentences.
:::

## An example heading {.example}
```

- The first slide of a page is `.idea` with `data-page` (the page's title) and
  `data-href`; its id is the page's file name, which the contents tiles link to.
  Later slides of the same page are `.example` (or a second `.idea`) without
  `data-page`, and inherit it. controls.html turns these into the small label above
  each heading, tagged Idea or Example.
- A page's plot: `::: {.plot}` > `::: {.card}` > `![](figures/<section>/<page>/<label>.png){fig-alt="..."}`.
  The path is enough; `tools/slide-figures.py` copies the file from
  `_freeze/chapters/...` before every render. When the plot carries its own title
  (often with a semicolon or colon), add `data-crop="0.067"`: the share of the image's
  height, from the top, to hide. Measure it from the title's bottom edge; most
  single-line ggplot titles are 0.06 to 0.08. `.plot.short` for a plot that is tall,
  `::: {.panel-labels}` above the image to name panels whose titles were cropped.
- Inline diagrams take the theme colours through classes, never fixed colours:
  `card`, `panel`, `wire`, `axis`, `grid`, `f-blue`/`s-blue` (fill/stroke) and the
  other palette names, `t-blue` (tints), `sm`, `head`, `big`, `lab`, `mute`, `mid`,
  `end`; `arrow` and `arrow-accent` add arrowheads. Text is 21 to 40 px in a viewBox
  about 1200 wide. Do not use `<use>`: the theme classes do not reach into it.
- Plots stay PNGs on a white card in every theme.

## Checking a deck

```bash
quarto render slides/05-generalisation.qmd
```

Then look at every slide in a browser (or headless Chrome at 1280 x 720 with
`?theme=dark#/N`), in at least one light and one dark theme. A takeaway longer than
about 100 characters wraps onto the control bar. Search the visible text, the
`aria-label`s, the `fig-alt`s and the notes for `;`, `—`, `–` and clause-joining
colons before committing.

`quarto render` also leaves a copy of reveal.js in `_freeze/site_libs/revealjs/`.
It is git-ignored: the decks run no code, so the GitHub build renders them, and their
libraries, from scratch.
