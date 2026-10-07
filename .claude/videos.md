# Videos

A short YouTube video for each of the ten course sections, narrated by an AI voice.
**Status (2026-09-28): planning done, laptop set up, voice chosen, nothing built yet.**
The next step is a pilot for §5 (Generalisation); see [Next step](#next-step-the-5-pilot).

The work moved from the desktop to a Linux laptop, because the desktop has no audio
output and the laptop has the better graphics card. The laptop is now set up (see
[Laptop setup](#laptop-setup-linux)).

## Decisions so far

| Topic | Decision |
| --- | --- |
| Scope | One overview video per section, 5–8 minutes (about 750–1,100 words of script). Shorts may come later. |
| Narration | One AI voice for the whole series. **No mascot, no two-voice dialogue.** |
| Keeping it fun | Through structure, not characters: a puzzle as the hook, the section's real trap as the climax, a 10-second quiz, then the page's *Key points*. |
| Text-to-speech | Gemini TTS, `gemini-3.8-flash-tts`, called with an API key from Google AI Studio. |
| Voice | Prebuilt voice **`Sadaltager`** ("knowledgeable"), British English, at a natural, conversational pace, for all ten videos. Chosen on 2026-09-28 over `Charon` and `Kore`, and over a slower "teaching pace". |
| Python env | The existing `claude` conda env (Python 3.11, manim 0.20.1, google-genai 2.25.0). No separate video env. |
| Pipeline | Hybrid: scripted steps (script → narration → visuals → rough cut) and polishing by hand in a video editor. |
| Animation | **Manim Community Edition** for every animated scene. Still ggplot figures, re-exported at video size, for real results. gganimate only if a scene truly needs a real fitted model to move. |
| Editor | **Kdenlive** (official AppImage). Not DaVinci Resolve: the free Linux version cannot import or export H.264 or AAC. |
| Pilot | §5 Generalisation, on the `feature/videos` branch. |

## Rules the videos inherit from the course

- **No invented numbers.** Every number spoken or shown comes from the page. When an
  animation needs real values, R writes them to a small CSV and Manim reads it. Concept
  animations (a loss surface, cross-validation folds) may use schematic data, but it
  must not look like survey results.
- **Same datasets.** Manim scenes load data with `python/mlbasic_data.py`.
- **Same look.** Okabe–Ito palette from `python/mlbasic_theme.py`. Font: Source Sans 3
  (the site's font, currently Source Sans Pro) if installed, otherwise Inter.
- **Scripts follow the authoring guide:** British spelling, no em dashes, plain English
  before equations. Scripts are drafted from the chapter's `.qmd` pages.
- **No section numbers in the video,** spoken or shown (decided 2026-09-29). Sections
  may be renumbered, and a number baked into a video cannot be changed. Numbers go in
  the YouTube title and description; other sections are named ("the validation
  section"). The end card shows only the site, `ml-basic.pages.dev` (Cloudflare Pages,
  the `SITE` constant), because page paths carry the section number too.

## Pipeline

```
_videos/05-generalisation/
  script.md      scenes: narration + what is on screen (drafted from the pages, edited by hand)
       │
       ▼  tools/draft-narration.py  free offline draft voice (Piper), no key or quota
  audio/draft/scene-01.wav …
       ▼  tools/narrate.py          Gemini TTS, one audio file per scene, when approved
  audio/scene-01.wav …
       │
       ▼  tools/figures-for-video.R  chapter figures re-exported at 1920×1080, larger text
       ▼  scenes.py (Manim)          each animation timed to its scene's audio length
  visuals/ …
       │
       ▼  tools/rough-cut.py        ffmpeg: pictures + audio → draft
  rough-cut.mp4, captions.srt, chapters.txt
       │
       ▼  Kdenlive, by hand         zooms, highlights, quiet music, intro/outro card
  final video → YouTube → embedded on chapters/NN-slug/index.qmd
```

### Drafts without the Google API

A whole video can be scripted, animated, cut and reviewed before any speech is bought:

```bash
python tools/draft-narration.py _videos/NN-slug   # offline, free, seconds per scene
cd _videos/NN-slug && manim -qh --frame_rate 30 scenes.py && cd ../..
python tools/rough-cut.py _videos/NN-slug
```

`draft-narration.py` writes `audio/draft/scene-NN.wav` (24 kHz mono, like Gemini) for
every scene that has no Gemini take of its current text. Manim and `rough-cut.py`
choose each scene's audio the same way (`narration_audio()` in `tools/video_script.py`):
a current Gemini take, else the draft, else an out-of-date take. `rough-cut.py` ends by
listing the scenes still on the draft voice. When the script is settled, run
`narrate.py` once, re-render the Manim scenes (the Gemini take is a little longer or
shorter), and cut again.

The voice is Piper's `en_GB-alan-medium` (`pip install piper-tts` in the `claude` env;
the voice, about 60 MB, downloads itself into `~/.local/share/piper-voices/` on first
use). It sounds synthetic but is paced within 3% of the Gemini takes, so timing and
layout reviewed on a draft hold for the final voice. `--voice` picks another Piper voice.

To plan the Gemini runs, `python tools/audio-list.py` lists every scene of every video
with the source of its audio (`gemini`, `reuse`, `draft`, `gemini-stale` or `none`),
writes it to `audio/audio-list.csv` in each video folder, and counts the requests a
`narrate.py` run would use against the 100 a day. `narrate.py --scenes 3,5-7` then
narrates just the chosen scenes.

- `_videos/` starts with an underscore so Quarto never renders it (like `_freeze/`).
  Scripts and code are committed; `audio/`, `visuals/` and the video outputs will be
  git-ignored.
- The scripts run in the `claude` conda env. `_videos/requirements.txt` will list the
  packages they use, kept separate from `python/requirements.txt` so the site and
  `check-snippets.py` are unaffected.

### Script format

One file per section, divided into scenes of 1–3 sentences with one visual each:

```markdown
## Scene 3
visual: chapters/05-generalisation/img/overfit-curve.png
The wiggly curve passes through every station perfectly.
Then we give it next year's survey, and it falls apart.
```

### Narration

- **Record the audio first, then animate to fit it.** Each Manim scene gets the exact
  length of its audio, read from the WAV header (Python's `wave` module). The
  `manim-voiceover` plugin is not used: recording first makes it unnecessary.
- **One request per scene**, cached by a hash of (text, voice, style, model). Only
  changed scenes are regenerated. This matters because TTS output varies slightly on
  every run, so approved scenes must not be regenerated.
- **Voice:** `Sadaltager` for every video, with `language: en-GB`. Auditioned against
  `Charon` and `Kore` on the same lines.
- **Style:** **"friendly British English, speaking at a natural, conversational pace"**
  for every video, set in each script's front matter and sent in `speech_metadata`.
  Chosen on 2026-09-28 by ear over "calm and friendly British English, speaking at a
  steady teaching pace", which sounded slower and more like a lecture. Inline tags such
  as `<short pause>` before a punchline. **Never put the style instruction in the text
  itself:** in the audition, a prefix such as "Read this as a calm, friendly narrator:
  …" was spoken aloud, doubling each sample from about 13 s to 25 s.
- **Pace:** with the chosen style, about 157 words per minute including pauses (§5
  scenes 1–3); the steady style gave about 126. A 1,000-word script is therefore about
  6.5 minutes of narration. Keep scripts to 1,000–1,100 words to stay under 8 minutes
  once the rough cut adds gaps between scenes. The natural style roughly halves the
  pauses, so a beat that needs room (after the hook question, before the quiz answer)
  needs a `<short pause>` tag or `pause-after:`.
- **API:** use the Interactions API. `generateContent` works (it was used for the
  test) but Google marks it as legacy, and the Interactions API is where custom voice IDs
  are configured. The request that works (google-genai 2.25.0), as used by
  `tools/narrate.py`: `client.interactions.create(model=…, input=[{"type": "text",
  "text": …, "annotations": [{"type": "speech_metadata", "style": …}]}],
  response_modalities=["audio"], generation_config={"speech_config": [{"voice":
  "Sadaltager", "language": "en-GB"}]}, response_format={"type": "audio", "mime_type":
  "audio/wav"})`. Modalities must be lowercase. The WAV is base64 in
  `response.output_audio.data`, and `response.usage.total_output_tokens` gives the cost.
- **The style changes the pace.** The same 20 words took 7.4 s without a style and
  9.4 s with the steady teaching-pace style: slower speech, not the style read aloud.
- **Pronunciation:** Google does not document a pronunciation dictionary. `narrate.py`
  applies a respelling list just before sending the text (e.g. `tidymodels → tidy
  models`, `RMSE → R M S E`, `ggplot → gee gee plot`). Captions keep the real spelling.
- **Paid tier daily limit: 100 requests per day** for `gemini-3.8-flash-tts`
  (`GenerateRequestsPerDayPerProjectPerModel`, found on 2026-09-28 after about 100
  requests, retries included). **When it runs out, the Interactions API hangs instead
  of returning 429**; the legacy `generateContent` endpoint returns the 429 at once,
  with the time until reset. So a narration run that hangs means the day's quota is
  gone: stop, and check with one `generateContent` call. Budget requests: a full video
  is 55–60, so re-narrate only changed scenes (`narrate.py` does) and never loop retries.
- **Limits:** up to 8,192 input tokens per request, far above one scene. The free tier
  allows **10 requests per day per model** (quota `GenerateRequestsPerDayPerProjectPerModel-FreeTier`,
  found on 2026-09-28), and failed retries count. It also hit a per-minute limit after
  about four requests. `narrate.py` must wait and retry on 429 errors, honour the
  `retryDelay` in the error, and stop (not keep retrying) when the daily quota is gone.

### Publishing checklist

- Upload `captions.srt` (more accurate than auto-captions).
- Paste `chapters.txt` (timestamps from scene lengths) into the description, with a link
  to the section page (e.g. `https://ml-basic.pages.dev/chapters/05-generalisation/`).
- Put the section number in the title and description only; the video has none.
- State in the description that the narration is AI-generated; check YouTube's current
  rules on labelling synthetic content.
- Embed the video on the section's `index.qmd`, thumbnail in `img/video/`.

## Gemini account, key and cost

- **Google AI Pro does not cover the API.** Its developer benefits apply only inside the
  AI Studio web interface. Use AI Studio (with or without Pro) to try and design voices;
  the pipeline needs its own API key.
- **Free-tier key tested on 2026-09-28 (desktop):** both `gemini-3.8-flash-tts` and
  `gemini-3.8-flash-lite-tts` are available to it, and a test sentence produced 8.2 s of
  WAV (24 kHz, mono, 16-bit) using 262 audio tokens (about 30 per second). No billing is
  set up. The response field `serviceTier: standard` is the speed tier, not the billing
  tier.
- **Free tier:** Google may use the text to improve its products, which is acceptable
  because the scripts will be published anyway.
- **The free tier is too small for production.** At 10 requests a day, one video of
  30–40 scenes plus retakes would take most of a week. Billing is needed before the
  narration starts in earnest.
- **Paid tier:** audio output is $9 per million tokens until 31 December 2026 and $18
  from 1 January 2027. At about 32 audio tokens per second, one 8-minute take is about
  15,000 tokens. With three takes per scene, the series of ten is about 460,000 tokens:
  **about $4 at the 2026 price, $8 at the 2027 price** (five takes: $7 / $14). The §5
  pilot alone is under $1. Input text tokens are negligible.
- **Key safety:** in the Google Cloud console, restrict the key to the *Generative
  Language API* and set a budget alert ($10 covers the series at the 2026 price; $20 if
  the work runs into 2027). Rotate it if it may have leaked.

### Storing the key

Never in `~/.bashrc`, the repo, or a Claude chat. Store it in the keyring and pass it
only to the command that needs it:

```bash
secret-tool store --label="Gemini API key" service gemini-api   # prompts for the key
GEMINI_API_KEY=$(secret-tool lookup service gemini-api) python tools/narrate.py _videos/05-generalisation
```

`narrate.py` will read `GEMINI_API_KEY` from the environment and nothing else. The
keyring is unlocked by a desktop login; over SSH use `pass` instead
(`pass insert gemini/api-key`, `pass show gemini/api-key`).

## Laptop setup (Linux)

**Done on 2026-09-28** (Ubuntu 24.04): steps 1–3, 5, 6 and 8.
Step 4 is replaced by the existing `claude` conda env, which already has manim 0.20.1,
google-genai 2.25.0, pandas, scipy, scikit-learn, pydub, PyYAML and ffmpeg 9 (libx264,
AAC). A test render with `Text` (Inter) and `MathTex` worked. Steps 7 (Source Sans 3) and 9 (renv, after the apt line in step 3 of the pilot) were
done later the same day.

The steps below are kept for setting up another machine. Commands assume Ubuntu or
Debian; adapt package names on another distribution.

1. **Get the branch.**

   ```bash
   git fetch && git switch feature/videos
   ```

2. **System packages.** ffmpeg is called directly by the scripts; `secret-tool` comes
   from `libsecret-tools`.

   ```bash
   sudo apt install ffmpeg libsecret-tools
   ```

3. **LaTeX, only if a scene uses equations** (`MathTex`). The desktop had TeX Live 2023
   with everything Manim's default template needs. On a fresh machine:

   ```bash
   sudo apt install texlive texlive-latex-extra texlive-fonts-extra texlive-science dvisvgm
   ```

   Check with `kpsewhich standalone.cls preview.sty dsfont.sty physics.sty calligra.sty`.
   Most scenes should use plain text and need none of this.

4. **Video environment.** conda-forge brings Manim's Cairo and Pango.

   ```bash
   conda create -n ml-basic-video -c conda-forge python=3.12 manim pandas scipy scikit-learn
   conda activate ml-basic-video
   pip install google-genai
   ```

5. **Store the API key on the laptop** (see [Storing the key](#storing-the-key)), then
   check it without printing it:

   ```bash
   secret-tool lookup service gemini-api | wc -c    # 39 characters for the current key
   curl -sS -o /dev/null -w '%{http_code}\n' \
     -H @<(printf 'x-goog-api-key: %s\n' "$(secret-tool lookup service gemini-api)") \
     https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash-tts   # expect 200
   ```

6. **Kdenlive:** download the AppImage from kdenlive.org, `chmod +x`, run.

7. **Optional: Source Sans 3**, so video titles match the site. It is the current name of
   Source Sans Pro (same design). Ubuntu 24.04 has no package for it, so install it for
   the user from Adobe's releases (3.052R at the time of writing):

   ```bash
   cd /tmp
   gh release download --repo adobe-fonts/source-sans --pattern 'OTF-*.zip'
   mkdir -p ~/.local/share/fonts/source-sans-3
   unzip -j OTF-source-sans-*.zip '*.otf' -d ~/.local/share/fonts/source-sans-3
   fc-cache -f
   fc-match "Source Sans 3"    # should name a Source Sans 3 file
   ```

   Without `gh`, download "Source Sans 3" from fonts.google.com and unzip the files in
   `static/` instead. Use the static OTFs rather than the variable font: Kdenlive and
   Pango handle separate weights more reliably. In Manim, `Text("…", font="Source Sans 3")`;
   Pango falls back to another font without warning if the name is wrong, so check the
   first render. The website does not need this; it gets the font from `styles.scss`.

8. **Optional: `mpv`** for quick checks of audio and drafts.

9. **R, only if figures are re-exported on the laptop.** `renv::restore()` and the
   system libraries listed in `workflow.md`. No new R packages are needed (`ragg` is
   already in `renv.lock`).

## Next step: the §5 pilot

On `feature/videos`, build the pilot for §5 (Generalisation), whose best moments suit
Manim: the curve that overfits, bias and variance shown as scatter around a target,
ridge shrinking the coefficients.

1. Draft `_videos/05-generalisation/script.md` from the six §5 pages, with a hook, the
   trap (choosing complexity by looking at the test set, which §5 does knowingly until
   `hyperparameter-selection.qmd`), a quiz and the *Key points*.
2. Write `tools/narrate.py` (Interactions API, caching, retry, respelling list).
   **Done 2026-09-28**, with `tools/video_script.py` (the script parser, shared with
   `rough-cut.py`) and `_videos/pronunciation.yml`. All 40 §5 scenes narrated on
   2026-09-28 (script trimmed to 1,069 words): 7.5 minutes including pauses, 14,000
   audio tokens, about $0.13.
3. Write the shared Manim style and the §5 scenes; `tools/figures-for-video.R`.
   **Done 2026-09-28**, rendered and checked at draft quality (`manim -ql`):
   - `_videos/mlbasic_video.py`: palette, Source Sans 3, and `VideoScene`, which reads
     each scene's WAV so the animation lasts exactly as long as its narration.
   - `_videos/05-generalisation/scenes.py`: 23 scenes. Schematic, tagged
     "illustration": 8, 9, 15, 16, 20–22, 26, 29–31, 33. Real data: 1, 2, 5–7, 12–14,
     17, 18, 27. `manim.cfg` sends them to `visuals/scenes/SceneNN.mp4`.
   - `tools/figures-for-video.R`: knits every page the script names, figures forced
     to 1920×1080 (8×4.5 in at 240 dpi), then runs the video's `exports.R` in the
     page's environment to write `visuals/data/*.csv`. About 75 s for §5. Every number
     the §5 script speaks matched the CSVs.
   - Known issue: `fig-stability` (scene 28) is a tall figure on the page; at 16:9 its
     44 term labels overlap. Replace with a Manim scene or crop in Kdenlive.
   - Manim pitfalls: never use `self.duration` in a scene (Manim overwrites it on
     every `play`); small `Text` loses its spaces, so `label()` sets text at 4× and
     scales down.
   - The laptop needed `sudo apt install cmake gdal-bin libabsl-dev libgdal-dev
     libnode-dev libudunits2-dev libx11-dev` before `renv::restore()` would finish.
4. Write `tools/rough-cut.py` (draft video, `captions.srt`, `chapters.txt`).
   **Done 2026-09-28.** `python tools/rough-cut.py _videos/05-generalisation` builds
   `rough-cut.mp4` (§5: 7:49, 1080p30), `captions.srt` and `chapters.txt` in about two
   minutes; unchanged scenes are cached in `visuals/segments/`. Each scene lasts its
   narration + `pause-after` + 0.5 s. Manim clips hold their last frame; figures and
   cards are stills. The sound is one WAV joined in Python and added once, so there are
   no seams. Cards are drawn with Pillow in Source Sans 3; `card: Heading | text` adds
   a small heading. Render the Manim scenes at 1080p first:
   `cd _videos/05-generalisation && manim -qh --frame_rate 30 -a scenes.py` (3 minutes).
5. Watch the rough cut, adjust, then polish in Kdenlive.
   **First review, 2026-09-28:** too much information per scene, too few animations,
   too little time between scenes; every video should open with a title and a short
   jingle, then say what the viewer will learn. Done the same day:
   - Script rewritten to one idea per scene: 55 scenes, 754 words (was 40 and 1,069),
     about 14 words each, at most one number. Chapter "In this video" first.
   - Every figure and card replaced by a Manim scene (new real-data scenes: the three
     trees, the bias–variance curves, lasso stability, forty validation splits; the quiz
     has a countdown bar through its pause; the key points tick off one by one).
     `exports.R` writes the extra CSVs. The chapter figures are still re-exported, but
     the §5 video no longer uses them.
   - Series opening: `TitleScene` in `_videos/mlbasic_video.py` (series and
     title from the front matter; the section number was dropped on 2026-09-29) over `_videos/intro-music.wav`, a 3.2 s jingle
     synthesised by `tools/make-intro-music.py` (no licence to track; replace the WAV
     with any 48 kHz track to change it). `rough-cut.py` puts it first. Made merrier on
     2026-09-29 at the user's request: a skipping G-major run over a plucked bass and
     light off-beat ticks, ending on a bright chord; still 3.2 s, so title timings hold.
   - `gap: 1.0` in the front matter (1 s between scenes, was 0.5); the soundtrack is now
     mixed at 48 kHz stereo.
   - Result: 6:35. Scene 55 reuses the approved take of the identical old closing line
     (its sidecar says so), because narration had started to hang; see the quota note
     below for why.
   **Second review, 2026-09-28:** name the "U-shaped error curve" explicitly, and make
   the three points promised in the opening unmistakable. Done:
   - Three "Key point one / two / three" scenes (15, 37, 51), each at the end of the
     chapter that delivers it, showing the opening's numbered promise and its answer;
     the recap (54–56) repeats exactly those three. The wording lives once, in
     `PROMISES`, `ANSWERS` and `RECAP` in `scenes.py`. 57 scenes, 823 words.
   - "U-shaped error curve" said and shown by name (scenes 21, 30, 34 and the points).
   - `narrate.py` reuses any take whose request is unchanged, even when its scene
     number moved, so inserting a scene costs only the new lines.
   - Captions: `captions.srt` is for uploading to YouTube (closed captions); preview
     with `mpv rough-cut.mp4 --sub-file=captions.srt`. Not burned into the picture,
     because they would cover axis labels.
   - No "illustration" corner tag (removed 2026-09-29). Every dataset in the course
     is simulated and scene 5 says so; the tag only told drawn scenes from page
     results, a difference viewers would not see. The no-invented-numbers rule is
     kept by the pipeline: numbers reach the scenes only through the CSVs.
   Only after that, decide on the
   other nine sections.

## Second video: §6 Assumptions (2026-09-29)

Built the same way as the §5 pilot, on `feature/videos`, up to a rough cut on the draft
voice: `_videos/06-assumptions-limitations/` (`script.md`, `exports.R`, `scenes.py`).

- 55 scenes, 840 words, 6:59. Hook: a model that is 95% accurate and never once finds
  the rare species, answered in "The puzzle, solved". The three key points: rows are
  worth less than they seem (independence, spatial dependence; the trap is random
  folds flattering position), a better fit can be more wrong (confounded depth curve,
  Poisson spread), a model answers where it knows nothing (extrapolation, rare classes).
- Every scene is Manim; `exports.R` writes 18 CSVs from the six pages (about 1 minute).
  Every spoken number was checked against them.
- The opening, key-point, recap, quiz and end-card scenes now live in
  `_videos/mlbasic_video.py` (`LearnScene`, `KeyPointScene`, `RecapScene`, `QuizScene`,
  `EndCardScene`); each video's `scenes.py` sets `PROMISES`, `ANSWERS` and `RECAP`.
  §5 uses them too; its re-rendered frames matched the old ones.
- Pango wraps long text on its own: keep a key-point answer line to about 30
  characters and a heading to about 50.
- Render with `manim -a` (one process). Rendering scenes in parallel processes
  corrupts Manim's shared text cache.
- Not yet narrated with Gemini: 55 requests, about $0.10.

## Third video: §7 Validation (2026-09-29)

Built like §6, to a rough cut on the draft voice: `_videos/07-validation/`.

- 53 scenes, 7:35. Hook: two models, one with the lower RMSE (forest, 4.36 against
  4.46), the other finding more animals at its top fifty stations (481 against 456),
  answered in "The puzzle, solved": the measure follows the sentence you will write.
  Key points: a single score is never enough (split spread, nested search, paired
  intervals), the way you split is a question (distance axis), measures disagree
  (RMSE/MAE, MAPE, confusion-matrix measures, cost-based threshold).
- `exports.R` writes 19 CSVs from the six pages (the cross-validation page is slow:
  allow about 5 minutes). Every spoken number was checked against them. The page
  uses two search numbers: 4.485 is the first search's winner, 4.472 the average
  the search reported inside the nested folds; the script keeps them apart.
- A shared base for several scenes must be a mixin, not a `Scene` subclass, or
  `manim -a` tries to render it (`ObjectiveRows` in `scenes.py`).
- Not yet narrated with Gemini.

## Fourth video: §8 Unsupervised learning (2026-09-29)

Built like §7, to a rough cut on the draft voice: `_videos/08-unsupervised-learning/`.

- 52 scenes, 8:21 on the draft voice (cut from 54 scenes and 8:58; a little over the 8-minute target). Hook: k-means splits the soft-bottom stations into a shallow
  and a deep group (medians 60 and 124 m) that come back in every resample (mean
  agreement 0.89, never below 0.71); answered in "The puzzle, solved": the taxa's
  depth optima are evenly spread, so the split is a stable cut through a gradient at
  about 92 m. Key points: every method finds something (units, noise, choosing k,
  the shuffled-data null, linkage), a component is not a gradient (29.4%, the 139°
  and 41° directions, 16/7/3 against two by cross-validation, the UMAP null), stable
  is not the same as real (bimodal bootstrap 53/7, the continuum, external checks).
- `exports.R` writes 19 CSVs from the six pages (under a minute). Every spoken number
  was checked against them. `beyond-k-means.qmd` must knit first: the pages attach
  `mclust` with `include.only`, and a later `library()` call cannot add
  `adjustedRandIndex` to a package already attached. `tools/figures-for-video.R` now
  knits with `error = FALSE`, so a failing chunk stops the export instead of leaving
  an object silently missing.
- The continuum curves (scene 39 on) are `geom_smooth()`'s loess, span 0.6, refitted
  in `exports.R` from the page's own data, as the page's figure draws them.
- Not yet narrated with Gemini.

## Fifth video: §9 Neural networks (2026-09-29)

Built like §8, to a rough cut on the draft voice: `_videos/09-neural-networks/`.

- 50 scenes, 868 words, 7:32 on the draft voice. Hook: a default eight-unit network
  trained on 480 stations scores a test error of 5.26, worse than predicting the
  average (4.402); "networks need a lot of data", so is 480 too few? Answered in "The
  puzzle, solved": everything learnable is a 0.70 window (baseline 4.402, oracle
  3.701), cross-validation picks one hidden unit, and on the noise-free target the
  same network beats linear regression by 24%: short of signal, not rows. Key points:
  a network is weighted sums with a bend (one neuron = lm() to eight decimals, the
  two-S-curve hump peaking at 8.7 °C against 9, 225 weights for 720 stations), it
  can fail without a warning (gradient check, learning rates, 0.763 unscaled against
  0.570 and 0.680, early stopping at step 1,937, seed spread), and it is the right
  tool for signal to spare and a combination you cannot name (the T–S band: 0.715,
  0.827, 0.926 against 0.998 with 17 weights; 0.994 on 100 stations). The autoencoder
  page is left out, for length. The quiz: ten identity layers fit only a straight line.
- `exports.R` writes 20 CSVs from five pages (about 3 minutes). The `sizes` chunk of
  `when-to-use-one.qmd` prints its table without keeping it, so `exports.R` re-runs
  it with the page's seeds (it reproduced 0.994, 1.000 and 0.996).
- **The seed spread does not reproduce on the laptop.** `training-a-network.qmd`
  says validation MSE spans 0.046 across ten seeds (its frozen output: best 0.5342);
  the laptop's knit gives 0.055 (seed 9 reaches 0.5256), while every other number on
  the page, training spread included, matches. Probably floating-point differences
  between machines amplified by one run. The video says "about 0.05", true of both.
  **Settled on 2026-10-05:** the page was re-rendered on the laptop and now gives
  0.055 (nine per cent), with the spread in inline R so its prose follows its own
  output; the section overview, `when-to-use-one.qmd` and `curriculum.md` say 0.055.
  The re-render also moved the learning-rate sweep's best at 0.5 from 0.5842 to 0.5844,
  now inline too.
- Not yet narrated with Gemini.

## Sixth video: §10 Interpretation (2026-09-29)

Built like §9, to a rough cut on the draft voice: `_videos/10-interpretation/`.

- 44 scenes, 807 words, 7:01 on the draft voice. Hook: the true depth effect peaks
  at 80 m, but a random forest's partial dependence falls from 5.04 to 3.77, and a
  GLM given the generator's own formula falls from 8.19 to 1.80: why? Answered in
  "The puzzle, solved": depth and temperature are confounded by the design (almost no
  cold shallow or warm deep stations, correlation −0.45); the GLM's depth quadratic
  comes back at about a fourteenth, p = 0.63; the GAM (best of seven on the same
  folds, 4.08 against the forest's 4.28) is wrong too but its interval covers the
  truth at 197 of 200 points. Key points: importance needs a null (three `rnorm()`
  columns rank 6, 7 and 8 of 16 on impurity; permutation band; chlorophyll's rank 1
  to 11 over eight splits; salinity and survey year beat the noise in 0 of 8; seed
  0.016 against split 1.50), no method recovers an effect the data cannot separate,
  and a model cannot see what its data lack (confidence band covers 29%, prediction
  interval 99%, in-sample RMSE 77%, conformal 96.5%, 86% under the chlorophyll shift;
  the rock gear bias takes the rock effect from 38% to 69% fewer and improves CV RMSE
  from 4.079 to 4.008). The quiz: two copies of depth both score near zero.
- `exports.R` writes 15 CSVs from six pages (about 6 minutes). Two tables are printed
  by their pages without being kept, the shift experiment and the gear-bias
  comparison, so `exports.R` repeats those calls with the pages' own functions and
  seeds. The GAM's coverage (197 of 200) and peak (52 m) are computed in scenes.py
  from the exported smooth, the way the page's figure draws it; they match the text.
- Every spoken number reproduced on the laptop.
- Not yet narrated with Gemini.

## Seventh video: §1 Introduction (2026-09-29)

Built like §10, to a rough cut on the draft voice: `_videos/01-introduction/`. Sections
1–4 were still without videos after §10; this starts them.

**Rebuilt later on 2026-09-29 as an overview** (`feature/improve-introduction`), after
the section's pages were rewritten. The user's brief: the video is not the place to
explain everything; it introduces the section briefly and says what its pages cover.

- 28 scenes, about 540 words, 5:09 on the draft voice. No puzzle hook: a short tour of
  the five pages under three promises. First the survey data, opening with "Throughout
  this course, we use one simulated marine dataset again and again"; the table's columns
  appear as they are named, each with a short gloss (salinity "how salty", abundance
  "animals counted"); the next section covers marine data in detail. Key point one,
  the kinds of learning (supervised, regression and classification; k-means into
  shallow, mid-depth and deep groups; discriminative and generative models,
  schematic). Key point two, statistics and machine learning (the scale of methods;
  the two aims; the flat straight line and the tree's hump from
  `what-is-machine-learning.qmd#fig-shapes`; predicting is not explaining, as a
  schematic where depth drives both salinity and the species, so salinity helps
  predict but causes nothing, with "more on this later in the course"). Key point
  three, the six tasks and the labelled-examples pipeline. The quiz: seabed
  photographs, some named by a specialist, are supervised, and the task is naming
  things.
- The user's feedback on the first cut: don't open the data with "every page uses one
  simulated survey"; say briefly what the variables are. And don't walk through the
  salinity slopes (−2.2 to −0.2) in 15 seconds: name the concept and say the course
  returns to it.
- `exports.R` writes 4 CSVs from two pages (under a minute); the applications,
  discriminative-generative and prediction-explanation pages appear as schematics.
  The one spoken number, 800 stations, reproduced on the laptop.
- Narrated with Gemini on 2026-09-29: 28 requests, all first time, no retries; 8,356
  audio tokens (about $0.08). Rough cut 5:04. Yesterday's failures were quota, not
  length: the free tier's 10 requests a day, then the paid tier's 100 a day (retries
  count), which made the Interactions API hang. The longest scene is 59 words, far
  under the 8,192-token input limit.

## Eighth video: §2 Marine data (2026-09-29)

Built like §1, to a rough cut on the draft voice: `_videos/02-marine-data/`.

**Rebuilt on 2026-09-30 as an overview** (`feature/improve-marine-data`), after the
section's pages were revised. The notes below describe the first version, which is
replaced; the lessons are in `section-revision.md`.

- 29 scenes, about 740 words, 5:41 with Gemini. A tour under three promises, with
  linear regression as the only model: the survey (a row is a station; 815 rows, 800
  unique, 160 sites), cleaning the raw file (salinity −999, mean 2.24 then 33.9; twelve
  spellings of four seabed types; dropping incomplete rows loses 10% of stations but
  20% of winter; the recipe), and testing a model honestly (a random split puts every
  test station at a trained site; catch weight lifts R² from 0.28 to 0.98, the answer
  in disguise; keeping sites whole drops the honest model from 0.28 to 0.08). Quiz:
  filling chlorophyll gaps with the whole survey's median before splitting is leakage.
- `exports.R` writes 9 CSVs from five pages. The user's feedback on the draft: space
  out the stacked seabed labels; a class assigned from the catch read as an unseen
  category rather than leakage, so catch weight replaced it in the video, the quiz and
  the leakage page; the split scene became four concrete sites.
- Narrated with Gemini on 2026-09-30: 29 requests, all first time, about $0.09.

The first version:

- 48 scenes, 8:11 on the draft voice. Hook: two random forests on the same survey, R² 0.87 and 0.13; which
  would you trust? Solved at the leakage climax: 0.87 is target leakage (catch weight,
  correlated 0.99 with the count; environment only scores 0.25), and 0.13 is the
  honest one (sites kept together; RMSE falls 4.82 to 3.76 on a different test set,
  so compare R²). Key points: the row count is not the sample size (815 rows, 800
  unique, 160 sites; most sites visited four to six times, one fifteen); look before
  you model (salinity −999 in 25 rows, mean 2.24 then 33.9; depth to 1581 m, ten
  stations divided by ten, two more undetectable; twelve spellings of four substrates;
  chlorophyll missing 19% in winter, 1% in autumn; dropping incomplete rows loses 80
  rows and 20.1% of winter; the vessel offset; months on a circle; the rare species
  at 5%, so "absent" scores 95%); and keep the test set untouched by every decision
  (a random split puts all 200 test stations at trained sites, 120 of 160 sites on
  both sides; `strata` silently pooled, 6.0% against 2.5%, fixed at 5.0% and 5.5%;
  selection from 200 noise columns, 0.03 against 0.0003; a recipe inside a workflow).
  Quiz: a habitat class assigned from the catch is target leakage.
- `exports.R` writes 19 CSVs from five pages; the types and scaling pages give no
  numbers (the months circle is schematic). The splitting and leakage pages print
  their tables without keeping them, so `exports.R` reruns them from the pages' own
  split objects and functions (the forest's seed is fixed): the values match.
- Three page discrepancies found, none spoken in the video, all fixed in the pages on
  2026-09-29: exploratory-analysis said the vessels differ by 0.42 PSU, where its own
  table gives 34.13 − 33.75 = 0.38; missing-values-and-outliers said 1581 m came "with
  6 °C water", where that station reads 3.11 °C (the 6 °C one is 1392 m, now named);
  and its deletion figure's alt text said winter drops "from just over 200 to around
  165", where the data give 199 to 159.
- The shelf depth (200 m) and the two undetectable depth errors are stated in the
  pages' prose, so `scenes.py` holds them as named constants, like §1's optimum.

## Ninth video: §3 Supervised learning (2026-09-29)

Built like §2, to a rough cut on the draft voice: `_videos/03-supervised-learning/`.

**Rebuilt on 2026-09-30 as an overview** (`feature/improve-supervised-learning`), after
the section's seven pages were revised. The notes below describe the first version,
which is replaced.

- 34 scenes, 845 words, 6:43 on the draft voice. A tour under three promises: models
  that add up their inputs (quantity or category; the count, 22.5% zeros, variance
  about six times the mean; linear regression's one slope; polynomial regression's
  peak at 7.5 °C and 12 of 202 test stations below zero; Poisson regression never
  below zero, mud 1.34 times sand; spread 3.7 times Poisson's, the negative binomial's
  wider intervals no longer tell rock from sand; logistic regression between 0 and 1,
  thresholds 0.5 and 0.9 giving 34/4 and 6/97 false alarms and misses), models made of
  questions (the depth-3 tree, the 6.4 to 10.4 °C band, steps level beyond the data,
  validation lowest at depth 5, resampled first thresholds 2.57 to 12.6, the forest's
  average, boosting best at 200 trees, test RMSE tree 4.48, boosting 4.35, forest 3.96,
  Poisson 3.55), and choosing (five questions; the seven models on test and validation
  sites; three models beyond the sampled temperatures). Quiz: clipping negative count
  predictions to zero hides the symptom, not the cause (the linear page's own point).
- `exports.R` writes 23 CSVs from all seven pages (under a minute). Every spoken
  number matched the frozen pages. The pages first labelled some models by shape
  ("Curve", "Poisson curve"); they were renamed by method on 2026-09-30, and
  `METHOD_NAMES` in `scenes.py` now only lower-cases the choosing page's labels.
- **Poisson** is respelled for the voice in `_videos/pronunciation.yml` (the voice
  otherwise risks "poison"); the entry also changes the §4 and §6 scenes that say it.
  `audio/poisson-audition.wav` (one Gemini request) reads four candidates: "Poisson",
  "Pwasson", "Pwah-son" and "Pwahsonn". The user chose "Pwah-son" on 2026-09-30.
- `Chart` in `scenes.py` places the axis names from the bottom and left edges: Manim
  draws the x axis at y = 0, mid-chart when the range goes below zero.
- Narrated with Gemini on 2026-09-30: 34 requests, all first time, 10,865 audio tokens
  (about $0.10). Rough cut 6:30.
- The user's review the same day, and the changes (9 more requests, $0.03; 35 scenes,
  7:00):
  - Gemini said "between 1 and 1" for "between 0 and 1", though the draft voice read it
    right. Numbers that stand for words are now written as words ("zero and one").
  - Overdispersion was shown but never named: scene 3 names it, and scene 9 keeps
    Poisson's intervals on screen beside the negative binomial's, "too narrow" against
    "wider".
  - False alarms and misses were used before they were explained: a new scene 11
    defines each (said present, truly absent; said absent, truly present), and the
    thresholds scene labels its bars the same way.
  - The tree scenes carry the heading "a decision tree", not only the narration. Their
    "yes" and "no" sit in small tags on the branches, as `rpart.plot` draws them: set
    beside the shallow branches, they collided with the question boxes.
  - Scene 26 names the tuning as overfitting: the tree's depth and boosting's number of
    trees were chosen on the validation sites, so both look better there than on the
    test sites (1 more request; 7:13).
  - "Held-back sites" became "the validation sites, which were held back from fitting",
    and the key point says "validation data".

- 50 scenes, 9:35 on the draft voice, the longest so far; the quiz and the multiplier
  scene (15) are the easiest cuts if it should come down. Hook: ten models on one
  survey, same predictors, same 200 test stations; boosting has the reputation, which
  would you bet on? Solved in "Ten models ranked": Poisson + polynomial first (4.54),
  default boosting last (5.41), four models predicting negative fish. Key points:
  match the model to the response (mean 3.9, variance 22.78; 180 zeros, 22.5%; 620
  present, 1 to 40; polynomial 6 negative predictions, lowest −2.06, linear 2; Poisson
  none, lowest 0.16, best RMSE; deviance ratio 3.95; AIC 3764 to 2839); a probability
  is not a decision (11 of 201 test stations; accuracy 0.9453 equals always "absent";
  never predicts presence; AUC 0.79; highest 0.274; thresholds 0.15 and 0.05; depth's
  odds ratio 0.971 describes absence, prevalence 0.7% to 19.4% by depth band); and
  flexibility costs data (the depth-3 tree's band, 1.4, 4.2 and 2.1; test RMSE 4.81,
  4.76, 4.84, 5.49, boosting's training 0.58; held-out error lowest at 50 trees;
  trees flat beyond the data). Quiz: a forest asked to predict warmer water.
- `exports.R` writes 15 CSVs from all five pages. Printed-but-not-kept tables (three
  models, four models, the rare-species scores) are rerun with the pages' own
  `evaluate()` and objects; all match the frozen outputs.
- RMSE values are rounded half up (`fixed()`): the default tree's 4.755 shows as 4.76,
  as the pages' prose says, where Python's `.2f` gives 4.75.
- Page discrepancies, none used in the video, both fixed in the pages on 2026-09-29:
  - linear-and-polynomial-regression: the substrate multipliers were relative to
    **gravel** (the clean loader's `factor()` sorts levels alphabetically), but the
    prose read them against sand. The recipe now has `step_relevel(substrate,
    ref_level = "sand")` (Python: `drop=["sand", "spring"]`), and the prose reads mud
    1.46 against a built-in 1.49 and rock 0.75 against 0.55. The old confounding
    explanation did not hold (rock stays near 0.8 even with the true curved depth and
    temperature terms), so the page now puts it down to rock being the rarest
    substrate, with the too-small Poisson standard errors hiding it. Key point: mud
    about 1.5 times sand. The fit and every prediction are unchanged.
  - trees-forests-boosting: the tree's upper split is at 10.57 °C; the page said 11
    (rpart.plot's two significant digits). It now says 10.6 and notes the plot's
    rounding.
- Not yet narrated with Gemini.

## Tenth video: §4 How algorithms learn (2026-09-29)

Built like §3, to a rough cut on the draft voice: `_videos/04-how-algorithms-learn/`.
Every section now has a video.

- 47 scenes, 9:29 on the draft voice. Hook: two fits of one model to the same 40
  stations (12 predictors); temperature gets 8.59 in one, 0.33 in the other, which had
  "one extra term, containing no data". Solved in "A penalty is a prior": on the other
  680 stations the mean scores 4.850, maximum likelihood 4.745 (about 2% better), the
  fit with the prior 4.495 (more than three times the improvement). Key points: the
  loss is an assumption (three losses, intercepts 2.36 and 1.13; the worst 37 stations
  of 749 supply 49.7% of the squared error, 21.0% of the absolute; dropping the largest
  catch, 40, moves the slopes 13.5% and 2.1%; likelihood for counts 3, 0 and 11 peaks
  at their mean; the loss menu as distributions; least squares is Normal maximum
  likelihood to four places); fitting is a search, check that it arrived (the formula
  against `lm()`; IRLS from −513.6 to −378.3, −373.3, flat by the fourth step; 10⁴,
  10⁸, 10²⁰ grid points; learning rates 0.3, 0.02 and 0.72 need 6, 106 and 161 steps;
  the limit 0.7282, 0.8 reaching an MSE of 7.3 billion; condition number 766 against
  2.2, 1,500 steps against 17; `maxit = 2` 9% out; separation −158, SE 13,515, p 0.99,
  cap 25; five forests spanning 0.037, k-means ten answers from twenty starts); and a
  penalty is a prior (SE 5.95; +8.59 and −6.20 fighting; MAP equals ridge; a flat prior
  finds 900 as plausible as 0.9; the λ curve). Quiz: ridge with depth in millimetres.
- `exports.R` writes 18 CSVs from all six pages. The step counts (6, 106, 161, 17 and
  1,500) are stated in gradient-descent's prose without code; "arrived" as an MSE within
  0.002 of the minimum reproduces all five, so `exports.R` computes them that way. The
  contours are `contourLines()` on the page's own grid.
- Two rounding notes: the forest span is taken from the page's four-place values
  (4.7568 − 4.7203 = 0.0365, so 0.037; unrounded it is 0.03646). The loss page's
  2.1% is 2.06% unrounded, so it holds.
- Pitfall met: `tibble()` evaluates columns in order, so a column named `worst` shadowed
  the page's `worst` index in the next column. Name export columns so they cannot
  collide with the page's objects.
- Page discrepancy, not used in the video, fixed on 2026-09-29: parameter-estimation
  said 10²⁰ evaluations "at a billion evaluations a second takes longer than the
  Holocene". It takes 10¹¹ seconds, about 3,200 years, against the Holocene's 11,700;
  the page now says "over 3,000 years".
- Not yet narrated with Gemini.

## §5 Generalisation rebuilt (2026-10-02)

Rebuilt from the revised pages on the same three points as the pilot (a perfect fit is a
warning sign; the U-shaped error curve comes from bias and variance; choose complexity
with cross-validation and open the test set once). 37 scenes, about 900 words, 7:22,
narrated with Gemini (34 requests; scenes 1, 10 and 37 reused their earlier takes).

- Examples, all through `exports.R` from the six pages: five models on their fitting
  stations and on new sites (the grown-out tree 0.00 and 6.21, the average 4.83); the
  three temperature trees (4, 20 and 414 leaves); the node-size sweep as the U-shaped
  curve; bias² and variance measured on the simulated truth, noise 72% of the best
  tree's error, a forest cutting a tree's variance about fifteen-fold; ridge regression
  and the lasso against 200 random columns (6.41 against 4.55, as good as the measured
  inputs alone at 4.56); one validation split against ten-fold cross-validation in 40
  repeats (3.52–6.36 against 4.45–4.70); the test sites scored once (0.29 against the
  0.26 cross-validation promised). Quiz: ten new columns raise R².
- Manim draws each axis through the other's zero, so a chart whose range excludes zero
  (the λ sweep from 0.001 to 1,000) shifts both ranges to start at 0 and translates the
  tick labels back (`Scene24`).
- A knob drawn with `always_redraw` does not follow a later `shift()` of its track until
  an animation starts, so the first frames showed it off the track: place the track
  before making the knob.

## §6 Assumptions rebuilt (2026-10-02, cut down 2026-10-03)

Rebuilt from the revised pages (`feature/improve-assumptions-limitations`) on three
points: a model can fit well and still be wrong, rows are worth less than they seem,
and a model never says when it is guessing. 29 scenes, about 860 words, 6:36 on the draft
voice. Narrated with Gemini on 2026-10-03 (29 requests, no retries, about $0.10): 6:28.

- Examples, all through `exports.R` from five pages: linear models assume straight
  lines, random forests and GAMs do not; caught ÷ predicted along each input shows
  temperature's hump; the forest and the GAM find it, but put depth's peak at 17 and
  31 m against the true 80, confounded with position; 598 training stations from 120
  sites, worth about 350 when whole sites are resampled (1.30 times wider); a forest on
  position alone scores R² 0.076 by site and 0.027 by block; ten shallow-survey forests
  run flat below 100 m (1.8–2.8 times the truth below 140 m); winter stations inside
  every range but far from the survey, and the forest's error growing with that
  distance. Quiz: two forests with almost the same RMSE (4.69, 4.78), the one on log
  counts predicting 1,699 animals against 2,421 caught, 30% short.
- The first rebuild (41 scenes, 958 words, 7:28) also had the models' scores on
  fitting and new sites, Poisson regression's simulated surveys and summer effect, the
  error map, the fitted neighbours within 30 km and four class-imbalance scenes with an
  upsampling quiz. After the pages were trimmed to one to three examples each, the user
  asked for the video to follow with less information: the scores, the Poisson spread
  and the neighbour count had left the pages, and the rest went to keep one example per
  idea. Class imbalance and prediction intervals are named on the end card only.
- The user then asked for one pronunciation of GAM and a little more explanation of each
  result. `pronunciation.yml` now says "G A M" (as RMSE is "R M S E"), for every video,
  and the result scenes each gained a sentence on what the number means: where a ratio of
  1 is right, why 1.3 times wider means about 350 stations, that the position-only score
  comes from the neighbours, why a forest runs flat past its data, and why log counts
  give a short total.
- First built around the GAM alone; the user pointed out that most machine-learning
  models handle curves, and that this is a machine-learning course, not a statistical
  one. The linearity page and the first chapter now lead with the random forest, and
  the GAM appears as the flexible model whose curves can be read.
- The spatial scenes draw a line from each held-out site to its nearest fitted site,
  computed from `sites.csv`, instead of counting neighbours: by block the lines cross
  out of the held-out squares.
- `exports.R` knits five pages. The independence page keeps only the bootstrap
  spreads, so `exports.R` averages the page's own `by_station` and `by_site` samples
  again.
- Delete the old video's CSVs from `visuals/data/` when `exports.R` is rewritten, and
  old `SceneNN.mp4` files past the new last scene: stale files stay there, and a scene
  could read one without error.
- pandas: `group.empty` is the DataFrame's emptiness flag, not a column called
  `empty`; use `group["empty"]`.
- Manim: `FadeIn(x)` and `Rotate(group_containing_x)` in one `play` leave `x`
  invisible; fade in first, then rotate.

## §8 Unsupervised learning rebuilt (2026-10-05)

Rebuilt from the revised pages (`feature/improve-unsupervised-learning`) on three points:
clustering finds groups nobody labelled, PCA turns many columns into one map, and a
pattern is checked before it is reported. 35 scenes, 7:48 on the draft voice; not yet
narrated. The old 52-scene puzzle (the soft-bottom split) became the quiz.

- Examples, all through `exports.R` from the six pages: k-means recovering the seabed
  (15 of 800 out of place); the silhouette's 0.179 against a shuffled baseline of about
  0.05 (3.5 times); a schematic dendrogram, then Ward against single linkage by the share
  of stations in the largest group (more than 99% for single); the ordination (29.4%),
  the taxa's loadings, depth and hard bottom 39° and 38° from the axes; 16 components by
  the 80% rule, 3 by parallel analysis, 2 by cross-validation for depth (PC3 is rock
  against gravel); 52 of 60 bootstrap samples giving the seabed split; 2% of stations
  near its boundary against 11% for the soft-bottom split; the recorded seabed at an
  ARI of 0.92; UMAP's observed map beside the shuffled one (scene 20). The other
  linkages, UMAP's settings and the horseshoe effect are on the end card.
- The first draft of the script ran about 9 minutes on the draft voice (38 scenes,
  1,146 words); merging four pairs of scenes and dropping UMAP brought it to 7:35. The
  user asked for UMAP back, as one scene: 7:48.
- The page names its linkages `Ward`, `single`, `average`, `complete` (`trees` in
  `beyond-k-means.qmd`), not R's `ward.D2`; `scenes.py` keys on those names.
- A chart whose x axis starts at k = 2 keeps Manim's zero-based axes and hides the
  empty stretch with a white strip (`axis_mask()`).
- A dot stack sizes its dots from its tallest bin (`dot_stack()`): 52 bootstrap
  agreements in one bin ran off the top of the frame at a fixed step.

### Still open

- Source Sans 3 or Inter for titles. The scenes use Source Sans 3 (installed on the
  laptop); `FONT` in `_videos/mlbasic_video.py` switches it.

Settled on 2026-09-28: billing (200 NOK of prepaid credit in AI Studio, about $18–20;
the paid tier hit no rate limits in the first runs), the voice and the style.

## §7 Validation rebuilt (2026-10-03; a short version tried 2026-10-04)

Rebuilt from the revised pages (`feature/improve-validation`) on three points: a score
is only as honest as its folds, the measure must follow the use, and a score needs an
interval. 34 scenes, about 980 words, 7:32 on the draft voice. Not yet narrated with
Gemini. **This is the current version**; the user will go through the section's pages
on 2026-10-05 and then decide how to improve the video.

- Examples, all through `exports.R` from five pages (the classification page is not
  knitted): the forest's pooled RMSE growing with the distance to the nearest fitted
  station (4.23 with folds of stations, 4.41 with half-degree blocks); a search over 100
  candidates with 20 noise columns, won at 4.50 by a model with two noise columns, and
  nested cross-validation (claimed 4.42, scored 4.86, the eight measured inputs with no
  search 4.37); RMSE and MAE picking different forests, the forest on log counts
  predicting 69% of the catch yet finding 847 animals on a shortlist of 100, 2.1 times
  random; false alarms and misses, and a threshold set by their costs; a bootstrap of
  the 160 sites giving overlapping intervals (the forest 3.75 to 4.94), and the paired
  comparison (the forest lower than predicting the average in 99% of resamples, than
  Poisson regression in 79%, its interval covering zero). Quiz: a false alarm costs
  three misses; the threshold is 0.75, where logistic regression's calls were cheapest.
- **A short version** is kept in `_videos/07-validation/short-version/` (`script.md`,
  `scenes.py`, `exports.R`, and `rough-cut-short.mp4`, which git ignores): 26 scenes,
  584 words, 4:19, for readers from any marine field, on what is new in the section
  (keep a score honest, choose a score that fits your goal, compare models in pairs),
  with no spatial folds and no RMSE against MAE. The user had said the 7:32 version
  leans on spatial cross-validation and skewed-count issues covered in earlier
  sections, holds too much, and that the videos dwell on limitations instead of giving
  a broad audience easy messages; the short version answered that but, in the user's
  words, "we have trimmed too much". To use it, copy its three files over the video's
  and run `figures-for-video.R` (or keep the CSVs), the drafts, Manim and the cut.
- Knitting the five pages takes 13 minutes, the cross-validation page most of it. To
  remake a few CSVs, a scratch folder with a `script.md` holding only the front matter
  and an `exports.R` naming only the pages needed can be knitted instead, and its
  `visuals/data/` copied across (three pages: under 3 minutes).
- The site maps are drawn from the survey's site positions (`load_coastal_survey_clean`),
  which are data rather than results, so the schematic scenes may use them.
- In a wait loop, `pgrep -f "manim -qh"` matches the loop's own command line and never
  ends; wait on the background task instead.
