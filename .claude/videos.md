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
  to the section page.
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
   - Series opening: `TitleScene` in `_videos/mlbasic_video.py` (series, section number,
     title from the front matter) over `_videos/intro-music.wav`, a 3.2 s jingle
     synthesised by `tools/make-intro-music.py` (no licence to track; replace the WAV
     with any 48 kHz track to change it). `rough-cut.py` puts it first.
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

### Still open

- Source Sans 3 or Inter for titles. The scenes use Source Sans 3 (installed on the
  laptop); `FONT` in `_videos/mlbasic_video.py` switches it.

Settled on 2026-09-28: billing (200 NOK of prepaid credit in AI Studio, about $18–20;
the paid tier hit no rate limits in the first runs), the voice and the style.
