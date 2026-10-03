# Revising a section

How to revise a course section's pages, diagrams and video. Written on 2026-09-29 from the
revision of section 1, Introduction (`feature/improve-introduction`, 11 commits), and
updated from section 2, Marine data (`feature/improve-marine-data`, 14 commits), section 3,
Supervised learning (`feature/improve-supervised-learning`), section 4, How algorithms
learn (`feature/improve-how-algorithms-learn`), and section 5, Generalisation
(`feature/improve-generalisation`, 2026-10-02). The general writing and figure rules are
in `authoring-guide.md` and the video pipeline in `videos.md`; this file collects what
the revisions added to them, as a checklist.

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
   merge, move or drop, whether a new page is needed (section 2 gained *The coastal
   survey* to open it), and the order in which methods are introduced. Splitting the
   whole section in two was considered for section 2 and rejected; ask before
   proposing it. **Revisit the titles and layout after the first page**, once its
   rewrite shows how much each topic needs: section 3's first page needed little
   change, but the user then asked to rethink the layout, and the section became
   seven pages, counts before logistic regression and a single tree before forests
   and boosting. Update `_quarto.yml` (sidebar), each page's `order:` and
   `curriculum.md` to match, and record the section's decisions in its
   `curriculum.md` entry.
3. **One page at a time.** Rewrite, render, screenshot, and let the user review it.
   Section 1 took several rounds per page; section 2, with the rules below already
   applied, mostly took one ("commit and move on to ..."). Commit only when the user
   says so; one commit per page keeps the history readable, with a body that says
   what went and what came in.
4. **Diagrams** with each page, in the house style below. When a new diagram lands,
   restyle the section's older diagrams so the section looks consistent.
5. **The section overview** (`index.qmd`) last among the pages: its summary must match
   the pages as they now are. If the section's title changes, change it everywhere it
   appears: the overview, the sidebar, the home page and `curriculum.md`.
6. **Check links from other sections.** Moving a topic between sections breaks their
   pointers to it: after section 2, a section 6 page still sent readers to "section 3"
   for RMSEs that cannot be compared across test sets, which section 2 now shows.
   `grep -rn "section N\|§N" chapters/` for the section's number and for every page
   it moved or renamed. Check what the other pages **claim** about the section, not
   only where they link: after section 5 was revised, two section 7 pages still said
   it had tuned on the test set, which it no longer did.
7. **A consistency pass across the section** before the video. The same model gets
   the same name on every page, in headings, plot legends, tables and the labels in
   code (see Wording). In section 3 the user found the old shape names ("The straight
   line", "The curve") and raw term labels only after the overview was done. Section
   5's pass also checked that legends and tables are in sentence case like the rest
   ("Ridge regression", not "ridge regression"), that every RMSE axis gives its unit
   the same way ("RMSE on new sites (individuals)"), that no two pages share a
   subheading, and that every mention of another section names a page.
8. **A headings pass.** Read the section's table of contents alone, page by page: can
   a reader say what each section shows? Rewrite the headings that fail (see Wording),
   as a before-and-after table the user approves before any page is edited. Check
   that every term the video will stress is named on a page, in bold and in a heading.
   `grep -rn "<page>.qmd#"` for links to the old heading anchors. Section 5 did this
   after its video's first cut, and the video had to wait for it: do it before.
9. **The video**, after the pages are settled, on the draft voice first (see below).
10. **Gemini narration** only when the user approves the script.
11. **Close:** full `quarto render`, then merge into `develop` when the user asks.

Checking a page: `quarto render <page>`, then a headless Chrome screenshot of
`_site/...` (a static server on port 4321 from `_site/` works). The user reviews
screenshots, so look at the rendered page yourself first.

Rendering: render a changed page **once**, check for "Output created", and check that
the `"hash"` at the top of its `_freeze/.../execute-results/html.json` equals
`md5sum` of the `.qmd`. Rendering a single page always runs every chunk, whatever
`_freeze/` holds, so a second render only repeats the work. Check that no
`chapters/*/*.rmarkdown` intermediate is left behind (stopping a render leaves one).
Any edit to a `.qmd`, even to a heading, changes its `_freeze` file, which is committed
with the page. Heavy pages take minutes, so render in the background.

Keep each page quick to run: a reader who copies the worked example should have its
results in about a minute per tab. Many repeats over many schemes belong in a
prototype, not on the page; the page shows the few that make its point. Section 7's
*Spatial and temporal cross-validation* first compared six fold schemes over 20 runs
(600 forests per tab, half an hour per render) and was cut to three schemes over 10
runs of 100-tree forests. If the Python tab is much slower than R, check that it fits
the same model: a `RandomForestRegressor` needs `max_features="sqrt"` and
`min_samples_leaf=5` to match ranger, as on *Forests and boosting*, and `n_jobs=-1`
costs more than it saves on the survey's 800 stations.

Committing: one commit per page, each with its own `_freeze/` and `img/` files. A
`git rm` of an old figure stays staged, so the first commit takes every staged deletion
with it, whichever page they belong to. Unstage first (`git reset`), then
`git add -A <page> <its _freeze folder> <its svg>` per commit, and check each commit's
`git show --stat`.

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
- **One diagram per page, in place of the longest passage.** In section 2 a diagram
  replaced each page's long idea section, numbered list or run of subsections (seven
  kinds of data, the order of checks, three reasons for a missing value, the recipe's
  stages, the three data roles, four kinds of leakage). The prose then keeps only what
  the diagram cannot show and the points readers get wrong.
- **Put a topic where it is used.** Class imbalance moved from *Missing values and
  outliers* to *Splitting the data*, where the stratified split needs it.
- **Cut the page's limits section and warning boxes** down to a sentence, or drop them;
  section 2 had one on nearly every page.
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
- **Never assign `_` in a Python tab** (`train_rows, _ = next(...)`). reticulate reads
  the chunk's last value from `_`, so every later table on the page prints as plain text
  instead of a table. Name the variable (`test_rows`).
- **Assign a fitted model, even inside a loop** (`fitted = model.fit(...)`, not a bare
  `model.fit(...)`). reticulate prints the last bare expression it ran, and a scikit-learn
  estimator prints as a long block of HTML and CSS.
- **Draw the resamples before building any recipe.** `recipe()` and each `step_*()`
  draw a random ID, so a recipe made between `set.seed()` and `group_mc_cv()` shifts
  the splits. Pages that claim to share splits must create them straight after
  `training(split)`. §5's first two pages had different splits until this was fixed.
- **Reset a sorted or filtered DataFrame's index** (`.reset_index(drop=True)`) before
  showing it. Any index other than 0, 1, 2 ... prints as an extra unnamed column.
- **Tab the R-only chunks too.** Once a page has R and Python tabs, a chunk with no
  Python equivalent still goes in a `panel-tabset` with a single *R* tab, so every
  chunk looks the same (`authoring-guide.md`, Code). Python equivalents may need a
  package R has built in: section 3 added statsmodels for the count models.
- **A section with no tabs may still need them.** Section 4 had none, as it fits
  models by hand rather than through the pipeline, yet every step had an honest
  numpy, scipy or statsmodels twin, and scikit-learn's defaults gave the tabs
  something to teach: `LogisticRegression` and `PoissonRegressor` carry a ridge
  penalty unless switched off, which hides separation. Three traps there: R's
  `glm()` models a factor's second level (`present` → "no"), so match it or the
  signs flip; scipy's BFGS stops on absolute error's corner (use Nelder-Mead); and
  Python warnings do not reach the rendered page, so say in a comment what warns.

### Wording

- **Titles and headings:** short and declarative, no commas, no "X, grouped by Y".
  Headings can be renamed whenever a better one exists; "Worked example" is fine as a
  section heading when its subsections carry the specific names.
- **A heading says what the section shows,** so the table of contents alone tells the
  story (section 5, 2026-10-02). Name the subject and the result; say what is compared,
  not how many ("Three trees on one input" became "Node size sets how closely a tree
  follows temperature"); no "the X" pointing back at something the heading has not named
  ("The ranking turns over" became "The best fits to their own stations do worst on new
  sites"); no teasers ("A model's report on itself") and no process words ("Reading the
  two ends"). A number is fine when a list of that length follows ("Four kinds of
  leakage"). The fixed labels stay.
- **A term the video stresses is named on a page, in bold and in a heading.** The
  section 5 video promised "the U-shaped error curve", which no page had named, and used
  the lasso, which only two sentences of section 4 had mentioned and no section 5
  heading showed. Underfitting and overfitting now names the curve, and Regularisation's
  headings name ridge regression and the lasso.
- **Say what a vague phrase means.** "The typical size of a prediction error" needed
  spelling out (the RMSE: roughly how far a prediction usually lands from the truth, in
  the outcome's units). "Without driving it" became plain words. If a reader could ask
  "what does that mean?", answer it in the sentence.
- **Use methods the reader already knows** before the course has introduced others:
  "you have fitted a linear regression", not "you have written a GLM". This covers the
  code too. Section 2's demonstrations used random forests, and its scaling page had a
  table of nine methods and a lasso exercise; they became linear regression, a plain
  paragraph ("methods that measure distance need a common scale"), and nothing.
- **Name a worked model by its method**, not its shape: *Linear regression*,
  *Polynomial regression*, *Poisson regression*, *Negative binomial model*, not "The
  straight line", "The curve" or "The Poisson curve". Use the same name in the
  heading, the prose, the plot legend and the model labels in code, on every page
  that fits the model.
- **Explain a metric before its first number.** RMSE and R squared are each given one
  plain sentence on the first page that quotes them. One sentence was not enough for
  RMSE, which every section uses: *Statistical modelling and machine learning* now
  builds it by hand (square, mean, root) from five test stations, compares it with
  predicting the average, and the introduction video gives it two scenes. Later pages
  link there rather than define it again.
- **Make an example show what its heading claims.** The salinity example was headed as
  prediction but was really about a confounder and causality; the page was rewritten
  around that, with *confounder* defined. In section 2, a habitat class assigned from
  the catch was meant to show target leakage, but the user read it as a category that
  did not exist at training time, a different problem. Catch weight, the count again
  in other units, shows target leakage directly: the model is handed the answer.
- **Explain any label the reader did not see being made.** "Shallow, mid-depth and
  deep" groups needed one sentence saying k-means found them and the page named them
  by their average depth.
- **Introduce a method in the section that needs it,** even when a later section
  covers it in full. Section 5 introduced cross-validation by site to choose a
  hyperparameter, and section 7's pages were adjusted to build on it rather than
  introduce it again.
- **Tables show readable term labels.** R's `tidy()` pastes a factor's name onto
  its level (`substrategravel`, `seasonsummer`); rewrite them as `substrate: gravel`
  (`str_replace(term, "^(substrate|season)", "\\1: ")`) and match the Python tab's
  labels to R's.
- **An overview's pointers must be traceable.** "Section 2 pointed here for a model
  that respects what a count is" named no page, and the user could not find it; it
  was cut. Name the page, or drop the sentence if it is not essential.
- **Plot titles must make sense on their own.** "Abundance, never shown to it" was
  unclear; say "k-means did not use abundance" in plain words.
- Few *who, why, how, what* (see `authoring-guide.md`, Voice).

### Data and numbers

- Section 1 uses only temperature, salinity and depth as inputs (abundance or presence
  as the outcome). Section 2 introduces the survey properly; from then on a page may
  use the other variables, but explains each the first time it appears.
- Every dataset is simulated. The `_snippets/simulated-data.qmd` note goes on each page
  that uses the survey; never write numbers that look like real survey results.
- **Never reveal the survey's true effects** (which variables really drive the
  species). Readers find them out by modelling; later pages reveal them when checking
  a model. Section 2 removed a line saying salinity has no real effect.
- **Compute every number in prose with inline R** (`` `r ...` ``) from the page's own
  objects, rather than typing it. Section 2 did this throughout and found three typed
  numbers that disagreed with the page's own tables.
- **Check every number quoted in prose against the rendered output** after each
  render (k-means group depths, percentages, slopes). A changed seed or split silently
  breaks them.
- Commit `_freeze/` with its page.

### Figures

- **Stacked panels need short axis titles.** In a patchwork stack each panel is short,
  so a long y-axis title ("RMSE on new sites (individuals)") runs up past the panel into
  its title. Break it onto two lines with `\n`.
- **Give every RMSE axis its unit**, worded the same on every page:
  "RMSE (individuals)", "RMSE on new sites (individuals)".

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
about 540 words, 5 minutes; section 2's is 29 scenes, about 740 words, 5:41; section 3's,
with seven pages to cover, is 35 scenes, about 950 words, 7:13; section 5's, three points
over six pages, is 37 scenes, about 900 words, 7:22. Use
`_videos/01-introduction/` or `_videos/02-marine-data/` as the template alongside
`videos.md`.

- **Three major points, each with its reason; not a tour of every page.** Section 4's
  first rebuild covered all six pages in 34 scenes and 8:19, and the user rejected it:
  it "touches all aspects without enough explanation of why we are checking and doing
  these things". The second kept three ideas (the loss decides what a model attends
  to; a search can fail quietly, so check it; a prior keeps a small survey sensible),
  one example each plus why it matters, and left the rest to the pages: 25 scenes,
  about 735 words, 5:43. Motivate first, then name the concept.
- **Rebuild the old video; don't patch it.** Every section already has a video, made
  before its pages were revised. Section 2's was 48 scenes and 8 minutes, a puzzle
  built on two random forests. Write a new script from the revised pages, one chapter
  per group of pages, and keep only the scene classes that still fit.
- **Use only the methods the course has introduced**, as on the pages: section 2's
  video uses linear regression only.
- **Keep a scene's words when its point is unchanged.** `narrate.py` reuses any
  approved take whose text is identical, even under a new scene number, so the opening,
  key-point and end-card lines carried over from the pilot cost nothing to narrate.

- **Shape:** title with the jingle; scene 1 promises three things (`PROMISES`); a
  chapter per promise, each ending on a key-point scene (`ANSWERS`); a quiz with a
  countdown and its answer; a recap of the three points (`RECAP`); the end card. The
  shared scene classes are in `_videos/mlbasic_video.py`.
- **One idea per scene, animated**, with pauses (`pause-after:`) where a viewer needs a
  moment. Don't crowd a scene with text.
- **Introduce the data plainly** where it first appears: "Throughout this course, we
  use one simulated marine dataset again and again", then what a row is and what each
  variable means, each column appearing as it is named.
- **Concrete, not abstract.** "A habitat map is asked about sites nobody has
  surveyed" lost the user. The scene became four sites, A to D: a random split tests
  another visit to a site the model knows, the split by site holds back site D, new to
  the model. Say what happens to what, in everyday words.
- **The quiz tests the video's main idea, with the page's example.** Section 2's quiz
  (filling gaps with the whole survey's median, then splitting) is the leakage page's
  own case. When the video finds a clearer example than the page, change the page too
  (the leakage page was reworded to match), so the two tell the same story.
- **Name a hard concept; don't walk through its numbers.** The salinity slopes (−2.2
  shrinking to −0.2) could not be followed in 15 seconds. A schematic (depth drives
  both salinity and the species; salinity helps predict but causes nothing) plus "the
  course comes back to these ideas" worked.
- **No section numbers** anywhere in the video, and no bare "the next section": say
  "the next section of the course" or "later in the course", or name the section.
- **Explain a method briefly before its result.** The section 5 video first showed the
  lasso's error curve with only a line on what the lasso is; the user asked for a short
  explanation. Two schematic scenes now come first: what a penalty does and what λ sets,
  then ridge regression against the lasso (squared against absolute size, shrinking
  against removing).
- **Define a term in its own scene before using it.** Section 3 used "false alarms"
  and "misses" straight away, and the user found them confusing; a schematic scene
  now defines each (said present, truly absent; said absent, truly present) before the
  thresholds scene counts them, and the bars carry the same words.
- **Name what the picture shows.** Overdispersion was drawn but never named, so the
  difference between the two models' intervals meant nothing; the scene now says the
  counts are overdispersed, so Poisson's intervals are too narrow, and keeps both
  sets on screen. Say it on screen as well as in the voice: the tree scenes gained the
  heading "a decision tree".
- **Say what a data role means in the scene.** "Held-back sites" became "the
  validation sites, which were held back from fitting".
- **Name the lesson a result teaches.** The single tree led on the validation sites
  but not on the test sites; the scene now says its depth, and boosting's number of
  trees, were tuned on those sites, "a kind of overfitting", and marks their gaps.
- Spoken numbers come only from the pages, via the video's `exports.R`; drop an export
  when the video stops using it. Schematic scenes use no numbers.
- **Read the page's own objects in `exports.R`, after checking their names.** A page
  may reuse a name: section 5's hyperparameter page sets `best` twice and its
  bias-variance page has a scalar `noise` where model complexity has a matrix. Knitting
  all six section 5 pages takes about 15 minutes, so start
  `tools/figures-for-video.R` first and write `scenes.py` while it runs; the CSVs
  appear page by page, so scenes can be checked as their data arrive.
- **Name models by method on screen**, as on the pages. The video reads the pages'
  model labels from the CSVs, so renaming a model on a page means updating the keys in
  `scenes.py` too, then re-running `exports.R`.
- **Long text wraps.** Manim's `Text` breaks a line it finds too wide, so a heading of
  about 40 characters at size 44 or more comes out on two lines. Keep characters × size
  under about 1,700, or split the text with `\n` yourself.
- **Check frames**, not just the last frame: `manim -ql -s` for last frames, and an
  ffmpeg `tile` contact sheet of the rough cut to check text arrives with the voice.
  Look hard at stacked labels: section 2's twelve seabed spellings touched each other
  vertically until the list was given more spacing. Section 3's charts put the axis
  names on the zero line when the range went below zero (Manim draws the x axis at
  y = 0), so its `Chart` places them from the chart's edges; and a tree's "yes" and
  "no" crossed the branches until they became small tags on them, as `rpart.plot`
  draws them.
- **Schematic layouts need fixed sizes.** Boxes drawn around random dots
  (`SurroundingRectangle`) came out at different heights, so two sibling nodes were not
  level, and a fixed box shorter than its tallest stack let dots spill over its edge.
  Give each box a fixed size and place its contents inside it. Keep labels a little
  clear of axis and divider lines, and check every scene that shares a layout after
  changing it (section 5 fixed scene 29 and left scene 30, built from the same
  layout, unrendered).
- **Manim draws each axis through the other's zero.** A chart whose range excludes
  zero (a λ sweep from 0.001 to 1,000) drew its y axis in the middle, at λ = 1. Shift
  both ranges to start at zero and translate the tick labels back.
- **Place a slider's track before making its knob.** A knob drawn with
  `always_redraw` ignores a later `shift()` of its track until an animation starts, so
  the first frames show it off the track.
- **Pages with Python tabs knit for the video** because `tools/figures-for-video.R`
  reads `_environment.local` (the Python reticulate uses). If it fails on a
  `{python}` chunk, check that file first.
- **Draft voice first** (`tools/draft-narration.py`, free, offline). Gemini only when
  the user approves the script, with the key passed as
  `GEMINI_API_KEY=$(secret-tool lookup service gemini-api)` and never printed or
  stored.
- **Gemini quota, not scene length, causes failures.** The paid tier allows 100
  requests a day and retries count; when it runs out the request hangs rather than
  erroring. A full video is 30–60 requests, so narrate at most one or two full videos
  a day, re-narrate only changed scenes (`narrate.py` does this), and wrap the run in
  `timeout`. Section 1's 28 scenes and section 2's 29 all succeeded first time (about
  $0.08 and $0.09). `python tools/audio-list.py <video>` confirms that no scene is
  left on the draft voice.
- **Write numbers that stand for words as words.** Gemini read "between 0 and 1" as
  "between 1 and 1", though the draft voice read it right; "between zero and one" fixed
  it. Listen to every Gemini take; the draft voice does not predict its mistakes. A
  quick first check: each take's length against its draft's (`wave`); a ratio outside
  about 0.8–1.25 suggests a misread or a skipped line. Section 5's 34 takes all fell
  within it.
- **Names the voice may misread** go in `_videos/pronunciation.yml` as respellings,
  which change only the speech; the captions keep the script's spelling. For a
  doubtful name, one Gemini request can read several candidates in turn for the user
  to choose from: section 3 chose "Pwah-son" for Poisson, which also applies to later
  videos that say it.
- Then re-render every scene (`manim -qh --frame_rate 30 -a scenes.py`, timing follows
  the new audio) and rebuild the rough cut. **The video changes only when the cut is
  rebuilt:** new takes are not in `rough-cut.mp4` until the re-render (about five
  minutes for section 5) and `rough-cut.py` have finished. The user watched the old cut
  once and heard the draft voice; say when the new file is written, and check its time.

## Status

| Section | Branch | Status |
| --- | --- | --- |
| 1 Introduction | `feature/improve-introduction` | Done; merged into `develop` 2026-09-29 |
| 2 Marine data | `feature/improve-marine-data` | Done; merged into `develop` 2026-09-30 |
| 3 Supervised learning | `feature/improve-supervised-learning` | Done; merged into `develop` 2026-09-30 (video narrated with Gemini, 44 requests, about $0.14) |
| 4 How algorithms learn | `feature/improve-how-algorithms-learn` | Done; merged into `develop` 2026-10-01 |
| 5 Generalisation | `feature/improve-generalisation` | Done; merged into `develop` 2026-10-02 (video narrated with Gemini, 34 requests, about $0.10) |
| 6 Assumptions and limitations | `feature/improve-assumptions-limitations` | Done; merged into `develop` 2026-10-03 (video narrated with Gemini, 29 requests, about $0.10) |
| 7 Validation | `feature/improve-validation` | Pages and overview revised; consistency and headings passes, video to come |
| 8–10 | | Not started |

Loose ends from section 7, for later sections' revisions: §7's *Uncertainty and
stability* bootstraps sites over the pooled out-of-fold predictions without refitting.
§9's `training-a-network.qmd` (about line 270) says that page means "fit it several
times and report the spread", and §8's `interpreting-patterns.qmd` (about line 91)
calls drawing 800 stations "the bootstrap from §7". Reword both to match.

Loose ends from section 1: the overview page says "the size of an effect" where the
other pages say "estimate an effect".
