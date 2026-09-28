# Videos

A short YouTube video for each of the ten course sections, narrated by an AI voice.
**Status (2026-09-28): planning done, nothing built yet.** The next step is a pilot for
§5 (Generalisation); see [Next step](#next-step-the-5-pilot).

The work moved from the desktop to a Linux laptop, because the desktop has no audio
output and the laptop has the better graphics card. Everything below is written so a new
session on the laptop can pick it up from here.

## Decisions so far

| Topic | Decision |
| --- | --- |
| Scope | One overview video per section, 5–8 minutes (about 750–1,100 words of script). Shorts may come later. |
| Narration | One AI voice for the whole series. **No mascot, no two-voice dialogue.** |
| Keeping it fun | Through structure, not characters: a puzzle as the hook, the section's real trap as the climax, a 10-second quiz, then the page's *Key points*. |
| Text-to-speech | Gemini TTS, `gemini-3.8-flash-tts`, called with an API key from Google AI Studio. |
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
       ▼  tools/narrate.py          Gemini TTS, one audio file per scene
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

All file and folder names above are planned, not yet created.

- `_videos/` starts with an underscore so Quarto never renders it (like `_freeze/`).
  Scripts and code are committed; `audio/`, `visuals/` and the video outputs will be
  git-ignored.
- `_videos/requirements.txt` will record the video environment, kept separate from
  `python/requirements.txt` so the site and `check-snippets.py` are unaffected.

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
  length of its audio. The `manim-voiceover` plugin does this; check it is still
  maintained, otherwise read the WAV length ourselves.
- **One request per scene**, cached by a hash of (text, voice, style, model). Only
  changed scenes are regenerated. This matters because TTS output varies slightly on
  every run, so approved scenes must not be regenerated.
- **Voice:** not chosen yet. Choose or design it in AI Studio (a prebuilt voice, the
  Extended Voice Library, or Voice Design with something like "warm, clear British
  English narrator, unhurried"), then use that one voice ID for all ten videos.
  Until then use the prebuilt voice `Kore`.
- **Style:** a fixed `style` in `speech_metadata`, e.g. "calm and friendly, speaking at
  a steady teaching pace". Inline tags such as `<short pause>` before a punchline.
- **API:** use the Interactions API. `generateContent` works (it was used for the
  test) but Google marks it as legacy, and the Interactions API is where custom voice IDs
  are configured.
- **Pronunciation:** Google does not document a pronunciation dictionary. `narrate.py`
  applies a respelling list just before sending the text (e.g. `tidymodels → tidy
  models`, `RMSE → R M S E`, `ggplot → gee gee plot`). Captions keep the real spelling.
- **Limits:** up to 8,192 input tokens per request, far above one scene. Free-tier rate
  limits are not published, so `narrate.py` must wait and retry on rate-limit errors.

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
- **Paid tier, if the free limits get in the way:** audio output is $9 per million tokens
  until 31 December 2026 and $18 from 1 January 2027. With three takes per scene, the
  whole series of ten is about 360,000 output tokens, so roughly **$3–7 in total**.
- **Key safety:** in the Google Cloud console, restrict the key to the *Generative
  Language API* and set a budget alert (e.g. $10). Rotate it if it may have leaked.

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

Commands assume Ubuntu or Debian; adapt package names on another distribution.

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

7. **Optional.** Source Sans 3 from Google Fonts, so video titles match the site.
   `mpv` for quick checks of audio and drafts.

8. **R, only if figures are re-exported on the laptop.** `renv::restore()` and the
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
3. Write the shared Manim style and the §5 scenes; `tools/figures-for-video.R`.
4. Write `tools/rough-cut.py` (draft video, `captions.srt`, `chapters.txt`).
5. Watch the rough cut, adjust, then polish in Kdenlive. Only after that, decide on the
   other nine sections.

### Still open

- The narrator voice (name or Voice Design ID).
- Whether to install Source Sans 3 or use Inter.
- Whether to add billing to the key (only if the free limits slow the work).
- Whether `manim-voiceover` is still maintained.
