---
title: "Validation: which score should you believe?"
section: chapters/07-validation/index.qmd
voice: Sadaltager
style: "friendly British English, speaking at a natural, conversational pace"
gap: 1.0
---

<!--
Script conventions: as in _videos/05-generalisation/script.md, whose header comment
lists the directive lines. In short: "# " starts a YouTube chapter, "## Scene N" a
scene; "page results" means R writes the numbers the page computed to a CSV;
"schematic" means drawn shapes with no numbers. Every number spoken comes from the
section's pages. No section numbers anywhere in the video: other sections are named.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. Why a single score is never enough. Why the
way you split your data is a question. And why performance measures disagree.

# The puzzle

## Scene 2
visual: manim Puzzle: two model cards, a random forest and a log model (page results, choosing-a-metric.qmd)

Here are two models of the same survey: a random forest, and a simpler model of the log
of the counts.

## Scene 3
visual: manim Puzzle: their RMSE as two bars, the forest's lower

By the usual error measure, the forest wins: 4.36 against 4.46.

## Scene 4
visual: manim Puzzle: fifty ranked stations each, and the animals they hold

Now send a ship to the fifty stations each model ranks highest. The log model's
stations hold 481 animals. The forest's hold 456.

## Scene 5
visual: manim Puzzle: a question mark between the two results
pause-after: 1.5

So which model is better?

## Scene 6
visual: manim Simulated: a "true process" box sends dots to a map of stations (schematic)

A note first: this survey is simulated. We wrote the process that made it, so we can
check every answer against the truth.

# One split is a noisy ruler

## Scene 7
visual: manim OneSplit: 720 stations, a quarter held back, one R² dot (page results, cross-validation.qmd)

The simplest test holds back a quarter of the stations, and scores the model on them.

## Scene 8
visual: manim OneSplit: forty splits drop forty dots along the R² axis

Do that forty times, with forty different splits. The same model scores an R² anywhere
from 0.079 to 0.346.

## Scene 9
visual: manim OneSplit: the stations reshuffle while the model card stays fixed

Nothing changed but where the line was drawn.

## Scene 10
visual: manim Folds: the stations cut into ten folds, each held out in turn (schematic)

Cross-validation cuts the data into ten folds. Each is held out once, and scored by a
model that never saw it.

## Scene 11
visual: manim OneSplit: forty cross-validations drop a tight row of dots under the first

Forty cross-validations agree far more closely: from 0.195 to 0.239.

# The winner's score flatters

## Scene 12
visual: manim Search: a hundred candidate models, five columns each, some columns noise (page results)

Now search for the best predictors. Add twenty columns of random noise, and try a
hundred models of five columns each.

## Scene 13
visual: manim Search: the hundred scores as dots, the lowest one picked out

The winner's cross-validated error is 4.485, the best of the hundred.

## Scene 14
visual: manim Search: the winner's five columns, three of them noise

Three of its five columns are pure noise. The best of a hundred noisy scores is low
partly by luck.

## Scene 15
visual: manim Nested: outer folds, each with the whole search running inside it (schematic)

Nested cross-validation repeats the whole search inside each fold, and scores its choice
on data the search never saw.

## Scene 16
visual: manim NestedBars: the reported error, then the honest one (page results)

Inside the folds, the search reported 4.472. Its choice actually scored 4.851: about 8%
worse.

## Scene 17
visual: manim NestedBars: five folds, the no-search model winning each one

And a model with no search at all beat the searched one on all five folds.

# A score needs an interval

## Scene 18
visual: manim Interval: the RMSE as a point, then its bootstrap interval (page results, uncertainty-and-stability.qmd)

A score is an estimate, like an average catch. Resample the stations, and an error of
4.14 could be anywhere from 3.70 to 4.58.

## Scene 19
visual: manim Paired: two models' scores on ten folds, overlapping, the unpaired interval across zero (page results, uncertainty-and-stability.qmd#fig-paired)

Compare two models on ten folds, and their scores overlap almost completely. The
interval on the difference is 1.54 wide, and covers zero.

## Scene 20
visual: manim Paired: lines join each fold's two scores, the paired interval shrinks

Pair the scores fold by fold, and it is 0.33 wide: nearly five times sharper, from the
same numbers.

## Scene 21
visual: manim Paired: the fold labels light up
pause-after: 0.5

Most of what makes a score high or low is the fold. So always compare models on the
same folds.

## Scene 22
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. A single score is never enough: use folds, nest any search, and give an
interval.

# The split is a question

## Scene 23
visual: manim Schemes: the survey's stations, a random fold held out (page results, spatial-and-temporal-cv.qmd)

Every way of splitting the data asks a question. Random folds ask how well a model fills
the gaps between stations it has seen.

## Scene 24
visual: manim Schemes: whole blocks of the shelf held out

Hold out whole blocks of the shelf, and you ask how well it maps ground never surveyed.

## Scene 25
visual: manim Schemes: a whole year held out

Hold out a whole year, and you ask how well it forecasts.

## Scene 26
visual: manim Distance: each scheme as a point, R² against distance to the nearest training station (page results, spatial-and-temporal-cv.qmd#fig-distance)

Now line the schemes up by how far each held-out station is from its nearest training
station.

## Scene 27
visual: manim Distance: random folds and the largest blocks picked out

About four kilometres away, the forest scores an R² of 0.200. Twenty-five kilometres
away, 0.114.

## Scene 28
visual: manim Distance: the trend line draws through the spatial schemes

There is no single true score. Only the question you chose.

## Scene 29
visual: manim BlockSize: a block grows until it covers the reach of the residual pattern (schematic)

So set the block size from how far the spatial pattern reaches, before you look at the
score.

## Scene 30
visual: manim Forecast: forecasting R² against random years of the same size, about equal (page results)

Here, forecasting cost nothing: the simulation gave the year no effect. Real surveys,
with shifting seas and changing gear, are rarely so kind.

## Scene 31
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. The way you split is a question: hold out what you will actually be asked
to predict.

# Measures disagree

## Scene 32
visual: manim Mistakes: one big miss against ten small ones, weighed by RMSE and by MAE (schematic)

A performance measure says which mistakes you mind. RMSE minds one big miss more than
many small ones. MAE minds them all the same.

## Scene 33
visual: manim WorstShare: every station's squared error, largest first, the worst 5% shaded (page results, regression-metrics.qmd)

On these counts, the worst 5% of stations carry half of all the squared error.

## Scene 34
visual: manim Mape: percentage error divides by the count; the empty stations fall out (page results)

Percentage error divides by the count, and 157 stations caught nothing.

## Scene 35
visual: manim Mape: its curve as every prediction is scaled, lowest at 0.47 (page results, regression-metrics.qmd#fig-scaling)

On the rest, it is lowest if you shrink every prediction to 47% of what the model
believes.

## Scene 36
visual: manim Confusion: the four boxes of the confusion matrix fill with counts (page results, classification-metrics.qmd)

For presence or absence, every prediction lands in one of four boxes.

## Scene 37
visual: manim Measures: ten measures from the same four numbers, as bars (page results)

Ten measures from those four numbers run from 0.058 to 0.995.

## Scene 38
visual: manim FlagAll: F1 for a rule that flags every station, against the model

A rule that says "present" at every station scores an F1 of 0.878. The model scores
0.882.

## Scene 39
visual: manim FlagAll: the empty-station box, which F1 never looks at

A measure that ignores the empty stations cannot tell a model from a rule with no model
in it.

# The puzzle, solved

## Scene 40
visual: manim Sentence: a sentence for the paper, then the measure that could prove it false (schematic)

So write the sentence you want to publish first. Then pick the measure that would prove
it false.

## Scene 41
visual: manim Objectives: "mapping every station", the RMSE bars, the forest ticked (page results, choosing-a-metric.qmd)

Mapping abundance at every station? That is per-station error, and the forest wins.

## Scene 42
visual: manim Objectives: "fifty stations to revisit", the shortlist bars, the log model ticked

Choosing fifty stations to revisit? Only the order matters, and the log model wins.

## Scene 43
visual: manim Objectives: "the stock total", the log model at 69% of the animals, crossed

Estimating the total stock? The log model predicts only 69% of the animals that are
there.

## Scene 44
visual: manim Threshold: a cut-off of one half as a balance, a wasted dive against a missed station (schematic)

Cut-offs work the same way. Using one half assumes a wasted dive costs the same as a
missed station.

## Scene 45
visual: manim CostCurves: expected cost against the cut-off when a wasted dive costs three (page results, choosing-a-metric.qmd#fig-cost)

If a wasted dive costs three times as much, the cheapest cut-off is 0.75.

## Scene 46
visual: manim CostCurves: the thirty-times curve, its value at one half against its minimum

At thirty times, leaving it at one half costs nearly eight times as much.

## Scene 47
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Measures disagree because each minds different mistakes: choose one
from the sentence you will write.

# Quiz

## Scene 48
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A model predicts the same average at every station. Its survey total is
exactly right. Is it a good model?

## Scene 49
visual: manim QuizAnswer: its shortlist against fifty random stations, about equal (page results)

No. It has no skill at all. Its fifty stations hold 183 animals, about what fifty
random stations would.

# Key points

## Scene 50
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: a single score is never enough.

## Scene 51
visual: manim KeyPoints: the second ticked

Two: the way you split the data is a question.

## Scene 52
visual: manim KeyPoints: the third ticked

Three: choose the measure from the sentence you will write.

## Scene 53
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
