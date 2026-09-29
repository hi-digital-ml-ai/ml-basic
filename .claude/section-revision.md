# Revising a section

How to revise a course section's pages, diagrams and video. Written on 2026-09-29 from the
revision of section 1, Introduction (`feature/improve-introduction`, 11 commits). The
general writing and figure rules are in `authoring-guide.md` and the video pipeline in
`videos.md`; this file collects what the section 1 revision added to them, as a
checklist.

## The aim

The pages and videos used to name methods (random forest, boosting, k-means, neural
networks) without saying what they are, and spent most of their length on selecting and
evaluating models. The revision makes each section **introduce its concepts and methods
step by step**: a method is explained in plain English before it is used, and each
section adds something new instead of re-evaluating the same models.

The Welcome page and the two Toolkit pages are out of scope for now.

## Order of work

1. **Branch.** One feature branch per section from `develop`:
   `feature/improve-<slug>`, e.g. `feature/improve-marine-data`.
2. **Plan the pages.** Read the section's pages and its entry in `curriculum.md`. Agree
   the page list and order with the user before rewriting: which pages to split,
   merge, move or drop, and the order in which methods are introduced. Update
   `_quarto.yml` (sidebar), each page's `order:` and `curriculum.md` to match.
3. **One page at a time.** Rewrite, render, screenshot, and let the user review it.
   Expect several rounds per page. Commit only when the user says so; one commit per
   approved change keeps the history readable.
4. **Diagrams** with each page, in the house style below. When a new diagram lands,
   restyle the section's older diagrams so the section looks consistent.
5. **The section overview** (`index.qmd`) last among the pages: its summary must match
   the pages as they now are.
6. **The video**, after the pages are settled, on the draft voice first (see below).
7. **Gemini narration** only when the user approves the script.
8. **Close:** full `quarto render`, then merge into `develop` when the user asks.

Checking a page: `quarto render <page>`, then a headless Chrome screenshot of
`_site/...` (a static server on port 4321 from `_site/` works). The user reviews
screenshots, so look at the rendered page yourself first.

## Pages

### Structure

- **The opening says what the reader will learn and why it is worth it**, in a sentence
  or two of real prose. Not a list of the page's ingredients ("X and Y, then Z, with
  one survey and three variables"): the user called that opening boring.
- **General terms first, in general words; the marine example second.** Define a term
  (prediction, supervised learning, a generative model) without stations, abundance or
  any other survey detail. Simple physical variables such as temperature and salinity
  are fine in a definition; survey specifics are not. Then show it on the data.
- **Split a long worked example into headed subsections**, one per term, then one for
  the comparison: *Discriminative model*, *Generative model*, *The two compared*;
  *Classification*, *Regression*. Use `###` headings, not bold run-in paragraphs.
- **One idea per page.** If a page carries two ideas that each need a worked example,
  split it (Types of learning, and Discriminative and generative models, became two
  pages). Order pages so each method is introduced before a later page uses it.
- **Short and concise.** Cut any example or block that does not clearly teach the
  page's point. Removed in section 1: a "simulated coastal survey used throughout this
  section" aside, a "good fit can still predict impossible counts" section, a warning
  box about neural networks, and inference as a third aim (it confused more than it
  helped at that level).
- **Link backwards only to something that is really there.** "The previous page set
  prediction against explanation" failed because the previous page did not visibly do
  so. Name the page and point to the exact idea.
- **Key points is its own section, not a callout.** Inside a callout the heading
  becomes the box's title, so the summary looked like part of the section above it and
  was missing from the table of contents. Every page ends with a real heading and the
  list in a `.key-points` box (styled in `styles.scss`), then optionally *Try it
  yourself*:

  ```markdown
  ## Key points

  ::: {.key-points}
  - ...
  :::
  ```

  Section 1 is converted; convert each later section's pages as part of its revision
  (`perl -0pi -e 's/::: \{\.callout-tip\}\n## Key points\n/## Key points\n\n::: {.key-points}\n/'`
  does it), and commit the changed `_freeze/` files, which store the page text.

- **Run the Python tabs.** Change each ` ```python ` tab to ` ```{python} `, so its
  output shows as the R's does, add `source(here::here("R/python-tabs.R"))` to the
  setup chunk so a DataFrame shows as a table, and include `python-tabs-run.qmd` in
  place of `python-tabs.qmd`. Fix any tab that fails first (`python/check-snippets.py
  <page>`); a failing `{python}` chunk fails the render. The survey page was the
  first converted; setup is in `workflow.md`, Python for the tabs.

### Wording

- **Titles and headings:** short and declarative, no commas, no "X, grouped by Y".
  Headings can be renamed whenever a better one exists; "Worked example" is fine as a
  section heading when its subsections carry the specific names.
- **Say what a vague phrase means.** "The typical size of a prediction error" needed
  spelling out (the RMSE: roughly how far a prediction usually lands from the truth, in
  the outcome's units). "Without driving it" became plain words. If a reader could ask
  "what does that mean?", answer it in the sentence.
- **Use methods the reader already knows** before the course has introduced others:
  "you have fitted a linear regression", not "you have written a GLM".
- **Make an example show what its heading claims.** The salinity example was headed as
  prediction but was really about a confounder and causality; the page was rewritten
  around that, with *confounder* defined.
- **Explain any label the reader did not see being made.** "Shallow, mid-depth and
  deep" groups needed one sentence saying k-means found them and the page named them
  by their average depth.
- **Plot titles must make sense on their own.** "Abundance, never shown to it" was
  unclear; say "k-means did not use abundance" in plain words.
- Few *who, why, how, what* (see `authoring-guide.md`, Voice).

### Data and numbers

- Section 1 uses only temperature, salinity and depth as inputs (abundance or presence
  as the outcome). Section 2 introduces the survey properly; from then on a page may
  use the other variables, but explains each the first time it appears.
- Every dataset is simulated. The `_snippets/simulated-data.qmd` note goes on each page
  that uses the survey; never write numbers that look like real survey results.
- **Check every number quoted in prose against the rendered output** after each
  render (k-means group depths, percentages, slopes). A changed seed or split silently
  breaks them.
- Commit `_freeze/` with its page.

## Diagrams

Hand-drawn SVG in the section's `img/`, inside `::: {.diagram}` so it uses the full
content width (see `authoring-guide.md`, Figures). The house style, from the section 1
diagrams (`chapters/01-introduction/img/six-tasks.svg` is a good template to copy):

| Element | Style |
| --- | --- |
| Canvas | `viewBox="-40 -24 1020 H"` (content about 940 wide, a margin on every side), `width="100%"`, `role="img"`, an `aria-label` |
| Text | Source Sans Pro. Title bold 22, card heading bold 22, body 18, small label bold 14 (letter-spaced), note italic 17 |
| Cards | fill `#f4f8fa`, stroke `#1b6a87` 1.6 px, rounded, a 6 px coloured strip along the top |
| Colours | Okabe–Ito: blue `#0072B2`, orange `#E69F00`, green `#009E73`, vermilion `#D55E00`, purple `#CC79A7`; ink `#1f2933`, body `#3d4852`, notes `#55606a`, lines `#8a949c` |

- Leave buffer space around and inside the diagram; the user asked for more than
  once.
- General terms in general words, as for prose: no stations or abundance in a diagram
  that defines a term.
- Render and look: labels must not overlap each other or the axes, and every text line
  must sit inside its card. Convert with `rsvg-convert` for a quick check.
- A good diagram can replace a long comparison in prose (the statistics-and-ML page got
  much shorter around one).

## The video

A section video is a **short overview**, not a place to teach everything: it
introduces the section and says what its pages cover. Section 1's video is 28 scenes,
about 540 words, 5 minutes. Use `_videos/01-introduction/` as the template alongside
`videos.md`.

- **Shape:** title with the jingle; scene 1 promises three things (`PROMISES`); a
  chapter per promise, each ending on a key-point scene (`ANSWERS`); a quiz with a
  countdown and its answer; a recap of the three points (`RECAP`); the end card. The
  shared scene classes are in `_videos/mlbasic_video.py`.
- **One idea per scene, animated**, with pauses (`pause-after:`) where a viewer needs a
  moment. Don't crowd a scene with text.
- **Introduce the data plainly** where it first appears: "Throughout this course, we
  use one simulated marine dataset again and again", then what a row is and what each
  variable means, each column appearing as it is named.
- **Name a hard concept; don't walk through its numbers.** The salinity slopes (−2.2
  shrinking to −0.2) could not be followed in 15 seconds. A schematic (depth drives
  both salinity and the species; salinity helps predict but causes nothing) plus "the
  course comes back to these ideas" worked.
- **No section numbers** anywhere in the video, and no bare "the next section": say
  "the next section of the course" or "later in the course", or name the section.
- Spoken numbers come only from the pages, via the video's `exports.R`; drop an export
  when the video stops using it. Schematic scenes use no numbers.
- **Check frames**, not just the last frame: `manim -ql -s` for last frames, and an
  ffmpeg `tile` contact sheet of the rough cut to check text arrives with the voice.
- **Draft voice first** (`tools/draft-narration.py`, free, offline). Gemini only when
  the user approves the script, with the key passed as
  `GEMINI_API_KEY=$(secret-tool lookup service gemini-api)` and never printed or
  stored.
- **Gemini quota, not scene length, causes failures.** The paid tier allows 100
  requests a day and retries count; when it runs out the request hangs rather than
  erroring. A full video is 30–60 requests, so narrate at most one or two full videos
  a day, re-narrate only changed scenes (`narrate.py` does this), and wrap the run in
  `timeout`. Section 1's 28 scenes all succeeded first time (about $0.08).
- Then re-render every scene (`manim -qh --frame_rate 30 -a scenes.py`, timing follows
  the new audio) and rebuild the rough cut.

## Status

| Section | Branch | Status |
| --- | --- | --- |
| 1 Introduction | `feature/improve-introduction` | Done; merged into `develop` 2026-09-29 |
| 2 Marine data | | Next. Must introduce the survey formally: the section 1 video tells viewers "the next section of the course looks at marine data more closely" |
| 3–10 | | Not started |

Loose ends from section 1: the overview page says "the size of an effect" where the
other pages say "estimate an effect".
