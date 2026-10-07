---
title: "Validation: when to believe a score"
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

This video is an overview built on three ideas, each with one or two examples: a score
is only as honest as its folds (the distance to the fitted data, and a search over
noise caught by nested cross-validation), the measure must follow the use (RMSE and MAE
pick different forests, a shortlist uses only the order, costs set the threshold), and
a score needs an interval (a bootstrap of the sites, and a paired comparison). The quiz
applies the second idea to the cost rule on the choosing-a-measure page. It does not
tour every page: the number of folds, the correlogram, forecasts, R² and the measures
for presence are left to the pages, and the end card names some of them.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. Why a score is only as honest as its
folds. Why the measure must follow the use of the predictions. And why a score needs an
interval.

## Scene 2
visual: manim Claim: a model, a score card, and an arrow to sites not yet surveyed (schematic)

Every model in this course has been given a score: roughly how far its predictions land
from what new sites caught. A score is a claim about the future. This video asks when to
believe it.

# A score is only as honest as its folds

## Scene 3
visual: manim Folds: sites dealt into five folds; each fold held out in turn, its stations predicted by a model fitted to the rest (schematic)

Cross-validation deals the sites into folds. Each fold is held out in turn and predicted
by a model fitted to the others. So every station gets one out-of-fold prediction, from a
model that never saw its site.

## Scene 4
visual: manim Reach: one held-out station and a line to the nearest fitted station, short for folds of stations, longer for folds of sites, longest for blocks (schematic)

What a score claims depends on what the folds hold out. Folds of single stations often
leave a station's own site in the fitted data. Folds of sites push the nearest fitted
station out to the next site, and spatial blocks push it across the block.

## Scene 5
visual: manim DistanceScore: pooled RMSE against the distance to the nearest fitted station, ten runs per scheme and their averages (page results, spatial-and-temporal-cv.qmd#fig-distance)

A random forest was scored all three ways, ten times each. The further away its fitted
data, the larger its error: from 4.23 with folds of stations to 4.41 with blocks.

## Scene 6
visual: manim Use: two uses side by side, gaps between monitored sites with folds of sites, an unsurveyed area with blocks (schematic)

No distance is right in general. To fill the gaps between monitored sites, use folds of
sites; to map an area nobody has surveyed, use blocks. Report the distance with the
score.

## Scene 7
visual: manim Search: eight measured columns and twenty columns of random numbers; a hundred candidates of five columns each (schematic)

Folds can also flatter a model they helped to choose. Add twenty columns of random
numbers to the survey, try a hundred models, each Poisson regression on five columns,
and keep the lowest cross-validated error.

## Scene 8
visual: manim Search: the hundred candidates' RMSEs as dots; the lowest picked out, its five columns below it, two of them noise (page results, cross-validation.qmd)

The winner scores 4.50, the lowest of the hundred. Two of its five columns are pure
noise. They just happen to suit these folds.

## Scene 9
visual: manim Luck: each score drawn as skill plus a random nudge; the lowest of many has the biggest nudge (schematic)

Every score is partly luck, and the lowest of many scores has gathered the most. So the
more models a search tries, the more its winner's score flatters it.

## Scene 10
visual: manim Nested: an outer fold of sites held out; the whole search runs on the rest, with folds of its own; its choice predicts the outer fold (schematic)

Nested cross-validation measures what the search is worth. An outer fold of sites is
held out, the whole search runs on the other sites, and its choice is scored on the
outer fold, which played no part in choosing.

## Scene 11
visual: manim NestedResult: three bars, the search's claim, its choices on the outer folds, and the eight measured inputs with no search (page results, cross-validation.qmd#fig-nested)

Inside each round, the search claimed an error of 4.42. On the outer folds, its choices
scored 4.86. Poisson regression on the eight measured inputs, with no search at all,
scored 4.37.

## Scene 12
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. A score is only as honest as its folds: hold out what the model will
face, and keep the search out of the score.

# The measure must follow the use

## Scene 13
visual: manim Misses: misses at a row of stations, turned into one number two ways, squared for the RMSE and as they are for MAE (schematic)

A performance measure turns every miss into one number. The RMSE minds large misses
most. The mean absolute error, or MAE, counts every animal missed the same.

## Scene 14
visual: manim Middle: the skewed catch per station, with the average and the median marked (page results, regression-metrics.qmd)

On skewed counts, the two aim at different targets. The RMSE is lowest when a model
predicts the average catch, 3.9 animals. MAE is lowest at the median, just 2.

## Scene 15
visual: manim Picks: the four models' RMSE and MAE as two rows of bars; the RMSE's lowest is the random forest, MAE's the random forest on log counts (page results, regression-metrics.qmd)

So the two measures pick different models. The RMSE picks the random forest. MAE picks
the same forest fitted to log counts, which aims at the median.

## Scene 16
visual: manim Picks: a bar of the animals caught, and the forest on log counts' predicted total, 69 per cent of it (page results)

Add up that forest's predictions, and they reach only 69 per cent of the animals caught.
For a stock estimate, MAE has picked a model that misses almost a third of them.

## Scene 17
visual: manim Shortlist: stations ranked by a model's prediction; a ship visits the top hundred (schematic)

Other uses ask other things. A ship has time to revisit 100 stations, and goes where a
model predicts the most animals. Only the order of the predictions matters.

## Scene 18
visual: manim ShortlistResult: animals found by each model's shortlist, between a random hundred and a perfect hundred (page results, choosing-a-metric.qmd)

The forest on log counts finds 847 animals, as many as the other models. Each shortlist
finds 2.1 times what a hundred random stations would. Predictions that run low lose
nothing here.

## Scene 19
visual: manim Mistakes: a two-by-two table of called and true presence; "false alarm" and "miss" placed in their cells (schematic)

Calls of present or absent need something else. A false alarm is a station called
present where the species is absent. A miss is a station called absent where it is
present.

## Scene 20
visual: manim Costs: a dive boat for a false alarm, a blank record for a miss, on a balance that tips; the threshold slides away from 0.5 (schematic)

If a false alarm wastes a dive, it may cost far more than a miss. Then the threshold for
calling a station present should come from those costs, not sit at 0.5.

## Scene 21
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. The measure must follow the use: decide what the predictions are for,
then choose the measure.

# A score needs an interval

## Scene 22
visual: manim OneSurvey: the survey's sites, then other sites the survey might have drawn, the score moving with them (schematic)

A score comes from one survey. Had other sites been sampled, it would have come out
higher or lower, and two models might have swapped places.

## Scene 23
visual: manim Resample: the 160 sites drawn again with replacement, some twice, some not at all; each draw gives one error (schematic)

To see how far, resample the sites. Draw the 160 sites again, with replacement, keep
their stations' out-of-fold predictions, and work out the error. Do it a thousand times.

## Scene 24
visual: manim Intervals: the three models' RMSEs with their 95% intervals, all overlapping (page results, uncertainty-and-stability.qmd)

The middle 95 per cent of those errors is an interval. For the random forest it runs
from 3.75 to 4.94, and all three models' intervals overlap. Read alone, they cannot even
say whether the forest beats predicting the average.

## Scene 25
visual: manim Pairs: two models' errors over a few resamples, rising and falling together; their difference drawn below, nearly constant (schematic)

But a hard sample is hard for every model, so their errors rise and fall together.
Compare them in pairs: take the difference within each sample, and what they share
cancels.

## Scene 26
visual: manim PairScatter: the forest's RMSE against predicting the average's, one dot per sample, nearly all below the diagonal (page results, uncertainty-and-stability.qmd#fig-pairs)

In pairs, the forest beats predicting the average in 99 per cent of the samples.

## Scene 27
visual: manim PairScatter: the second panel, against Poisson regression, a narrow band along the diagonal (page results)

Against Poisson regression, it wins in only 79 per cent, and the paired interval covers
zero. On this survey, the RMSE cannot tell those two apart.

## Scene 28
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. A score needs an interval: resample the sites, and compare models in
pairs.

# Quiz

## Scene 29
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A false alarm wastes a dive, and costs three times as much as a missed
record. The model's probabilities can be read as chances. Above what probability should
a station be called present?

## Scene 30
visual: manim QuizAnswer: "0.75"; the two expected costs against the probability, crossing at 0.75; logistic regression's cost curve with its lowest point (page results, choosing-a-metric.qmd#fig-cost)

0.75. At probability p, calling a station present risks a false alarm: three times one
minus p. Calling it absent risks a miss: p. The two match at 0.75, where logistic
regression's calls were cheapest on the survey.

# Key points

## Scene 31
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: a score is only as honest as its
folds.

## Scene 32
visual: manim KeyPoints: the second ticked

Two: the measure must follow the use.

## Scene 33
visual: manim KeyPoints: the third ticked

Three: a score needs an interval.

## Scene 34
visual: manim EndCard: the site's address and a thank-you

The pages also cover how many folds to use, forecasts tested on later years, and the
measures for presence, with all the code. They are linked below. Thanks for watching.
