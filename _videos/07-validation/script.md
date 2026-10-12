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
is only as honest as its folds (the distance to the fitted data, then a search over
noise caught by nested cross-validation), the measure must follow the use (RMSE and MAE
pick different forests because counts are skewed, a shortlist uses only the order,
costs set the threshold), and a score needs an interval (a bootstrap of the sites, and a
paired comparison). The quiz applies the second idea to the cost rule on the
choosing-a-measure page. It does not tour every page: the number of folds, the
correlogram, forecasts, R² and the measures for presence are left to the pages, and the
end card names some of them.

Earlier videos already taught cross-validation and whole-site folds (Generalisation),
resampling with replacement (Assumptions and limitations), and thresholds, false alarms
and misses (Supervised learning). Here they get a one-line reminder, not a re-run; the
words go on why each effect happens.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about
validation: checking how far to trust a model's score. It covers three things: why a
score is only as honest as its folds, why the measure must follow the use of the
predictions, and why a score needs an interval.

## Scene 2
visual: manim Claim: a model, a score card, and an arrow to sites not yet surveyed (schematic)

Every model in this course has been given a score: roughly how far its predictions land
from what new sites caught. A score is a claim about the future: this is how well the
model will do where it has not been. This video asks when to believe it.

# A score is only as honest as its folds

## Scene 3
visual: manim Folds: sites dealt into five folds; each fold held out in turn, its stations predicted by a model fitted to the rest (schematic)

First, why a score is only as honest as its folds. You met cross-validation in the
Generalisation video: the sites are dealt into folds, and each fold takes a turn as new
data while a model is fitted to the others. So every station gets one out-of-fold
prediction, from a model that never saw its site, and the score is worked out from
those.

## Scene 4
visual: manim DistanceScore: the axes, then the ten runs of each scheme as small dots, named as they are spoken; the x-axis name highlighted (page results, spatial-and-temporal-cv.qmd#fig-distance)

What a score claims depends on what the folds hold out. Here a random forest, many
decision trees averaged, was scored three ways: with folds of single stations, folds of
whole sites, and folds of blocks, which are squares of the map. Along the bottom is how
far each held-out station lies from the nearest station the forest was fitted to.

## Scene 5
visual: manim DistanceScore: each scheme's average as a large dot, joined; their distances and errors; "hold out what the model will face" (page results)

With folds of stations, a held-out station's own site is often still in the fitted
data, so the forest can lean on what its neighbours caught. The further away its fitted
data, the larger its error: from 4.23 with folds of stations to 4.41 with blocks. So
choose folds that hold out what the model will face.

## Scene 6
visual: manim Search: eight measured columns and twenty columns of random numbers; a hundred candidates of five columns each; "keep the lowest cross-validated error" (schematic)

Folds can also flatter a model they helped to choose. Here is a test. Add twenty
columns of random numbers to the survey: inputs that carry no information about the
catch. Then try a hundred models, each a linear regression on five columns, score every
one by cross-validation, and keep the lowest error. This is called a search.

## Scene 7
visual: manim Search: the hundred candidates' RMSEs as dots; the lowest picked out, its five columns below it, two of them noise (page results, cross-validation.qmd)

The winner scores 4.51, the lowest of the hundred. Yet two of its five columns are
random numbers. They just happen to suit these folds.

## Scene 8
visual: manim Luck: each score drawn as what the model would really score plus a random nudge; the lowest of many has the biggest nudge (schematic)

Why? Every score is partly luck: which stations happened to land in which folds. Some
models get a lucky nudge down, others an unlucky one up. Keep the lowest of many
scores, and you keep the luckiest. So the more models a search tries, the more its
winner's score flatters it.

## Scene 9
visual: manim Nested: an outer fold of sites held out; the whole search runs on the rest, with folds of its own; its choice predicts the outer fold (schematic)

The cure is nested cross-validation: cross-validation inside cross-validation. First,
an outer fold of sites is held out. The whole search, with folds of its own, runs on
the other sites and makes its choice. That choice is then scored on the outer fold,
which played no part in choosing. Each outer fold takes its turn.

## Scene 10
visual: manim NestedResult: three points, the search's claim, its choices on the outer folds, and the eight measured inputs with no search (page results, cross-validation.qmd#fig-nested)

Inside each round, the search claimed an error of 4.43. On the outer folds, its choices
scored 4.46, a little worse: that gap is the flattery. Linear regression on the eight
measured inputs, with no search at all, scored 4.37, better than both. The gap is small
here; with fewer sites or more flexible models, it grows.

## Scene 11
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. A score is only as honest as its folds: hold out what the model will
face, and keep the search out of the score.

# The measure must follow the use

## Scene 12
visual: manim Misses: misses at a row of stations, turned into one number two ways, squared for the RMSE and as they are for MAE (schematic)

Next, why the measure must follow the use. A performance measure turns every miss into
one number. The RMSE squares each miss before averaging, so it minds large misses most.
The mean absolute error, or MAE, averages the misses as they are, so every animal missed
counts the same.

## Scene 13
visual: manim Skewed: a histogram of counts, tall at few animals with a long tail to the right; the median line, then the average line to its right; "RMSE: best at the average", "MAE: best at the median" (schematic)

That changes which prediction scores best. The RMSE is lowest when a model predicts the
average catch, and MAE when it predicts the median. Survey counts are skewed: most
stations catch a few animals, and a few catch a great many. Those big catches pull the
average up, so the median sits below it.

## Scene 14
visual: manim Picks: the four models' RMSE and MAE as two rows of dots; the RMSE's lowest is the random forest, MAE's the random forest on log counts (page results, regression-metrics.qmd)

So the two measures can pick different models. Here are four, scored both ways. The
last is a random forest fitted to log counts: taking the logarithm shrinks the big
catches, so this forest aims near the median. The RMSE picks the plain random forest.
MAE picks the forest on log counts.

## Scene 15
visual: manim Picks: a bar of the animals caught, and each model's predicted total; the forest on log counts at 69 per cent of it (page results)

Add up that forest's predictions, and they reach only 69 per cent of the animals
caught. For a stock estimate, which needs the total, MAE has picked a model that misses
almost a third of them.

## Scene 16
visual: manim Shortlist: stations ranked by a model's prediction; a ship visits the top hundred (schematic)

Other uses ask other things. Say a ship has time to revisit 100 stations, and goes where
a model predicts the most animals. Then only the order of the predictions matters, not
their size.

## Scene 17
visual: manim ShortlistResult: animals found by each model's shortlist, between a random hundred and a perfect hundred (page results, choosing-a-metric.qmd)

The forest on log counts finds 847 animals, about as many as the other models. Each
shortlist finds 2.1 times what a hundred random stations would. Predictions that run low
lose nothing here.

## Scene 18
visual: manim Costs: a false alarm, a wasted dive, as a large square; a miss, a lost record, as a small one; a threshold on the probability of presence slides up from 0.5 (schematic)

Calls of present or absent need something else again. As in the Supervised learning
video, a threshold turns a probability of presence into a call, and a call can be a
false alarm or a miss. If a false alarm wastes a dive, it may cost far more than a miss.
Then the threshold should come from those costs, not sit at 0.5: raise it, and the model
calls present only where it is surer.

## Scene 19
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. The measure must follow the use: decide what the predictions are for,
then choose the measure.

# A score needs an interval

## Scene 20
visual: manim OneSurvey: the survey's sites, then other sites the survey might have drawn, the score moving with them (schematic)

Finally, why a score needs an interval. A score comes from one survey. Had other sites
been sampled, it would have come out higher or lower, and two models might have swapped
places.

## Scene 21
visual: manim Resample: the 160 sites drawn again with replacement, some twice, some not at all; each draw gives one error (schematic)

To see how far, resample the sites, as in the Assumptions and limitations video. Draw
the 160 sites again, with replacement, so some come up twice and some not at all. Keep
their stations' out-of-fold predictions, and work out the error. Do it a thousand times.

## Scene 22
visual: manim Intervals: the three models' RMSEs with their 95% intervals, all overlapping (page results, uncertainty-and-stability.qmd)

The middle 95 per cent of those thousand errors is a 95 per cent interval: the range
the score could take with other sites. For the random forest it runs from 3.75 to 4.94,
and all three models' intervals overlap. Read alone, they cannot even say whether the
forest beats predicting the average.

## Scene 23
visual: manim Pairs: two models' errors over a few resamples, rising and falling together; their difference drawn beside, nearly constant (schematic)

But a hard sample is hard for every model: when one model's error rises, so do the
others'. So compare them in pairs: in each resample, take one model's error from the
other's. What they share cancels, and only the difference is left.

## Scene 24
visual: manim PairScatter: the forest's RMSE against predicting the average's, one dot per resample, nearly all below the diagonal (page results, uncertainty-and-stability.qmd#fig-pairs)

Each dot is one resample. Below the diagonal, the forest's error is the lower. In pairs,
the forest beats predicting the average in 99 per cent of the resamples.

## Scene 25
visual: manim PairScatter: the second panel, against linear regression, a narrow band along the diagonal; the paired interval across zero (page results)

Against linear regression, it wins in only 80 per cent, and the paired interval for the
difference reaches across zero: no difference at all is still possible. On this survey,
the RMSE cannot tell those two apart.

## Scene 26
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. A score needs an interval: resample the sites, and compare models in
pairs.

# Quiz

## Scene 27
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A false alarm wastes a dive, and costs three times as much as a missed
record. The model's probabilities can be read as chances. Above what probability should
a station be called present?

## Scene 28
visual: manim QuizAnswer: "0.75"; the two expected costs against the probability, crossing at 0.75; logistic regression's cost curve with its lowest point (page results, choosing-a-metric.qmd#fig-cost)

0.75. At probability p, calling a station present risks a false alarm, with chance one
minus p and a cost of three. Calling it absent risks a miss, with chance p and a cost of
one. The two match at 0.75, and that is where logistic regression's calls were cheapest
on the survey.

# Key points

## Scene 29
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: a score is only as honest as its folds.

## Scene 30
visual: manim KeyPoints: the second ticked

Two: the measure must follow the use.

## Scene 31
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: a score needs an interval.

## Scene 32
visual: manim EndCard: the site's address and a thank-you

The pages also cover how many folds to use, forecasts tested on later years, and the
measures for presence, with all the code. They are linked below. Thanks for watching.
