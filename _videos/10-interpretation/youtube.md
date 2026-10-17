# YouTube upload: video 10, Interpretation

Generated 2026-10-15 from `script.md`, `chapters.txt` and the section page. If the
video is re-cut, update the chapters from the new `chapters.txt`. Shared settings for
all ten videos are in `_videos/youtube.md`.

| Field | Value |
| --- | --- |
| Video file | `_videos/10-interpretation/rough-cut.mp4` |
| Captions | `_videos/10-interpretation/captions.srt` (English, United Kingdom) |
| Thumbnail | `_videos/10-interpretation/thumbnail.png` (1280 × 720; made by `_videos/thumbnails.py`) |
| Playlist | Machine Learning Basics for Marine Science, position 10 |
| YouTube | <https://www.youtube.com/watch?v=zU2KrW-P6q8> (2026-10-18, with the GitHub Pages end card) |
| First upload | <https://www.youtube.com/watch?v=anfrxEKV4Xk> (2026-10-15, `ml-basic.pages.dev` on the end card; replaced, so delete it on YouTube) |
| Embed on | `chapters/10-interpretation/index.qmd` (the new upload) |

## Title

```
10 · Interpretation: reading a model after it is built | ML Basics for Marine Science
```

## Description

```
Reading a model once it is built: which inputs a random forest relies on, which way each one pushes its predictions, and why it made one particular prediction.

This is video 10 of 10 in Machine Learning Basics for Marine Science, a free introductory course for marine researchers. This video goes with section 10 · Interpretation and responsible application.

In this video:
1. Shuffle each input in turn (permutation importance): the more the error rises, the more the model relies on that input.
2. Draw each input's effect (partial dependence): set it to each value in turn at every station, and average the predictions.
3. Split one prediction into parts (SHAP values): each input's SHAP value is how far it moves that prediction from the average.

0:00 In this video
0:22 Shuffle each input in turn
2:11 Draw each input's effect
3:23 Split one prediction into parts
5:29 Quiz
6:15 Key points

The course pages for this section, with more examples and all the code in R (tidymodels) and Python (scikit-learn):
https://hi-digital-ml-ai.github.io/ml-basic/chapters/10-interpretation/

The whole course:
https://hi-digital-ml-ai.github.io/ml-basic/

About this video
- The coastal survey in the examples is simulated, not a real survey, so the numbers are not results about any real species.
- The narration is an AI-generated voice (Google Gemini text-to-speech) reading a script written for the course. Animations are made with Manim; the music and sound effects were made for the course.

#MachineLearning #MarineScience #DataScience
```

## Tags

```
interpretable machine learning, explainable AI, feature importance, partial dependence, SHAP, machine learning, marine science, machine learning for beginners, data science, ecology, oceanography, fisheries science, R, tidymodels, Python, scikit-learn
```
