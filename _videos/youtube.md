# Uploading the course videos to YouTube

Prepared 2026-10-15. Each video has its own sheet with its title, description (with
chapters) and tags: `_videos/NN-slug/youtube.md`. This file holds what is the same for
all ten, and the order of work.

## Before uploading

- **The site is public** on GitHub Pages, at `hi-digital-ml-ai.github.io/ml-basic`.
  Every description, and every end card ("linked below"), sends viewers there, so the
  videos can be **Public**.
- **The files are the rough cuts** (`rough-cut.mp4`, 1080p, 30 fps), all on the Gemini
  voice. The planned Kdenlive pass (zooms, quiet music) has not been done; upload them as
  they are, or polish them first.
- **Custom thumbnails** are ready, `_videos/NN-slug/thumbnail.png` (1280 × 720 PNG): the
  section number, the title and one of the sea animals that cheer in that video. Uploading
  them needs a verified channel (YouTube asks for a phone number once). To redraw them,
  see the top of `_videos/thumbnails.py`.

## Settings for every video

| Setting | Value |
| --- | --- |
| Playlist | Machine Learning Basics for Marine Science, <https://www.youtube.com/playlist?list=PLNam3PcMB508> (linked from the home page and every section overview) |
| Audience | No, it's not made for kids |
| Altered or synthetic content | No: the voice is synthetic but does not imitate a real person, and nothing shows real people or events. Check the current wording of the question in YouTube Studio; the AI voice is stated in every description either way |
| Category | Education |
| Video language | English (United Kingdom) |
| Caption certification | This content has never aired on television in the U.S. |
| Subtitles | Upload `captions.srt` as English (United Kingdom), "With timing" |
| Licence | Standard YouTube Licence (or Creative Commons, if you want reuse allowed) |
| Chapters | Automatic from the description: each list starts at 0:00 and every chapter is longer than 10 seconds |
| End screen | Optional: "Next video" or the playlist over the last 5–20 seconds, which show the end card |

## Playlist

**Title**

```
Machine Learning Basics for Marine Science
```

**Description**

```
A free introductory course in machine learning for marine researchers: ten short videos, one for each section of the course, from the kinds of learning to reading a model once it is built. Every example uses the same simulated coastal survey. Each video goes with a section of the course website, which has more examples and all the code in R (tidymodels) and Python (scikit-learn).

https://hi-digital-ml-ai.github.io/ml-basic/

The narration is an AI-generated voice reading scripts written for the course.
```

## Order of work for each video

1. Upload `rough-cut.mp4`, paste the title, description and tags from the sheet, and
   apply the settings above.
2. Upload `thumbnail.png` as the thumbnail, and add `captions.srt` under Subtitles.
3. Add the video to the playlist, in course order (1 to 10).
4. Note the video ID (the `v=` part of the link) in the sheet.
5. Once all ten are up, they go on the site: each embedded on its section's
   `index.qmd`, above *Pages in this section*, with Quarto's `video` shortcode.

All ten were first uploaded on 2026-10-15, with `ml-basic.pages.dev` on the end card.
The site then moved to GitHub Pages, so all ten were uploaded again with the new end
card, embedded on 2026-10-18, and the first uploads deleted.

## The ten videos

| # | Video | Length |
| --- | --- | --- |
| 1 | Introduction: a map of machine learning | 9:27 |
| 2 | Marine data: understanding and preparing a survey | 9:35 |
| 3 | Supervised learning: from a straight line to boosting | 10:03 |
| 4 | How algorithms learn: the loss, the search and its assumptions | 9:44 |
| 5 | Generalisation: why a perfect fit is a bad sign | 10:29 |
| 6 | Assumptions: what a good score cannot show | 6:40 |
| 7 | Validation: when to believe a score | 6:22 |
| 8 | Unsupervised learning: finding structure without labels | 7:22 |
| 9 | Neural networks: sums with a bend, and when they pay off | 7:27 |
| 10 | Interpretation: reading a model after it is built | 6:50 |
