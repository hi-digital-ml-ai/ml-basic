---
title: "Assumptions: what a good score cannot show"
section: chapters/06-assumptions-limitations/index.qmd
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

This video is an overview built on three ideas, each with one example: a model can fit
well and still be wrong (the random forest's depth curve), rows are worth less than they
seem (repeat visits, neighbouring sites, and what the forest's inputs explain), and a
model never says when it is guessing (past the survey's depths, a new mix of
conditions). The quiz applies the first idea to the distributional page's forest on log
counts. It does not tour every page: what each loss aims at, samples from one year and
class imbalance are left to the pages, and the end card names the last two. Each true
curve is shown only after the model's own answer.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about
assumptions: what a method takes for granted about its data. It covers three things:
why a model can fit well and still be wrong, why rows are worth less than they seem,
and why a model never says when it is guessing.

## Scene 2
visual: manim Assumes: "assumption-free" struck through; two panels, "freed from" straight lines, "not freed from" how the data were collected (schematic)

Machine learning is often called assumption-free. It frees a model from straight
lines, but not from the way its data were collected.

## Scene 3
visual: manim Simulated: a "true process" box sends dots to a map of stations (schematic)

As in the other videos, the survey is simulated: we wrote the process that makes its
counts. So a model's answers can be checked against the truth, which no real study can
do.

# A model can fit well and still be wrong

## Scene 4
visual: manim Shapes: a straight line fails a hump; a random forest follows it in steps (schematic)

First, why a model can fit well and still be wrong. Few marine responses are straight
lines. A linear model, such as linear regression, assumes they are: each extra degree
or metre always adds the same amount. A random forest, many decision trees averaged,
does not. Its trees split the stations into groups, so it follows the data in steps,
with no shape chosen in advance.

## Scene 5
visual: manim ErrorCheck: linear regression's average error, caught − predicted, in ten groups along each input; temperature's hump stands out (page results, linearity-and-nonlinearity.qmd#fig-errors)

To check the straight-line assumption, fit a linear regression and look at its errors:
the animals caught minus the number predicted. Sort the stations into ten groups along
each input, and average the errors in each group. Where the line is right, the average
stays near zero. For temperature it rises and falls: the line predicts too many animals
in the coldest and warmest water, and too few in between, where the species does best.

## Scene 6
visual: manim Truth: the forest's temperature curve, then the simulation's curve dashed over it (page results, linearity-and-nonlinearity.qmd#fig-truth)

Now fit a random forest. Its curve across temperature finds the hump without being
told its shape. The dashed line is the true curve, the one the simulation used, and the
forest follows it closely.

## Scene 7
visual: manim Truth: the depth panel, the forest's peak in shallow water, the true peak at 80 m, the stretch between them shaded (page results)

For depth, it does not. The forest puts the most animals at 17 metres, and the truth is
80. Nothing warned of it: the error check showed no pattern along depth. A map drawn
from this curve would send the next survey to the wrong depth.

## Scene 8
visual: manim Confounding: depth and the species both linked to position, with an unmeasured patch behind position (schematic)

Why? Depth follows position, because the shelf deepens offshore. So something about
position that no input measures ends up in depth's curve. This is confounding: a
hidden cause, linked to both an input and the outcome, makes the input look as if it
acts. No choice of shape removes it.

## Scene 9
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. A model can fit well and still be wrong: a curve that follows the data
can credit the wrong input.

# Rows are worth less than they seem

## Scene 10
visual: manim Visits: 800 stations as squares, which gather into 160 sites; one site's visits highlighted; "dependent data" (page results, dependent-data.qmd)

Next, why rows are worth less than they seem. The survey holds 800 stations, from only
160 sites visited again and again. Visits to one site share its depth, its seabed and
its water, so they partly repeat each other. Data like these are called dependent:
each visit says something about the others.

## Scene 11
visual: manim Resample: stations drawn at random, then whole sites drawn with all their visits (schematic)

To measure how much less they are worth, resample. Draw stations at random, as many as
the survey holds, so some come up twice and some not at all, and work out the average
catch. Do it many times, and watch the average move. Then draw whole sites instead,
each with all its visits.

## Scene 12
visual: manim Spreads: the 500 averages drawn by station, and the 500 by site, wider; "worth about 470 stations" (page results, dependent-data.qmd)

Drawing whole sites spreads the average 1.31 times wider. An average's spread shrinks
with the square root of the number of independent rows, so the 800 stations are worth
only about 470 independent ones. This is the survey's effective sample size. Count all
800 as independent, and the survey seems surer of its average than it is.

## Scene 13
visual: manim Blocks: the sites on the map, then the squares of the map; the 500 averages drawn by block spread wider still; "worth about 150" (page results, dependent-data.qmd)

Neighbouring sites share their water too. Draw whole squares of the map, called
blocks, each with every site in it, and the average spreads 2.34 times wider. Then the
800 stations are worth only about 150.

## Scene 14
visual: manim Errors: how much wider each way of drawing spreads, for the catch (by site, by block), then for the forest's errors by site (page results, dependent-data.qmd#fig-spread)

Can a model's inputs explain some of this? A random forest knows each station's depth,
temperature and seabed. Resample its errors, on sites it never saw, instead of the
catch. By site, they still spread 1.25 times wider, almost as much as the catch: what a
site's visits share, the inputs miss. So the forest must be scored on sites it has
never seen.

## Scene 15
visual: manim Errors: the forest's errors by block join the chart, far below the catch's (page results)

By block, the errors spread only 1.36 times wider, against 2.34 for the catch. Most of
what neighbours share is their depth and water, and the forest already knows those.
Some may remain, so a map of areas nobody has surveyed is scored on held-out areas,
whole areas kept back from fitting.

## Scene 16
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Rows are worth less than they seem: visits to one site repeat each
other, so score a model on sites it has never seen.

# A model never says when it is guessing

## Scene 17
visual: manim Beyond: the true mean count against depth, the survey's depths to 100 m unshaded, deeper water shaded; "extrapolation: predicting beyond the data" (page results, sampling-and-extrapolation.qmd#fig-beyond)

Finally, why a model never says when it is guessing. Survey effort is never even: it
follows ports, weather and ship time. Suppose the survey reached only sites shallower
than 100 metres, and a model must map the deeper ones. The line is the true average
count at each depth. Predicting beyond the data like this is called extrapolation.

## Scene 18
visual: manim Beyond: ten random forests, one per survey, follow the truth to 100 m and run flat beyond it (page results)

Ten random forests, each fitted to a different part of the survey, follow the truth
within its depths. Below, they run flat, while the true count keeps falling. A tree
sends every deeper station to the leaf of the deepest stations it saw, so the forest
repeats its value at the edge.

## Scene 19
visual: manim Beyond: "below 140 m: 1.8 to 2.8 times the truth" on screen only (page results)

Below 140 metres they are too high on all ten surveys, and nothing in their
predictions says so.

## Scene 20
visual: manim Beyond: the forests fade; ten polynomial regressions follow the truth to 100 m and fan out beyond it; "0.7 to 3.7 times the truth" (page results, sampling-and-extrapolation.qmd#fig-beyond)

A polynomial regression, a linear regression given squared terms so that its line can
bend, fans out instead. Fits that agree within the survey bend in different directions
below it, from 0.7 to 3.7 times the truth. Each method follows its own rule past the
data.

## Scene 21
visual: manim Novelty: temperature against depth for the summer and autumn survey, cold water only at depth (page results, sampling-and-extrapolation.qmd#fig-novelty)

A new mix of conditions is harder to spot. Here each dot is a station, placed by its
depth and its temperature. A survey that sailed only in summer and autumn met cold
water only at depth.

## Scene 22
visual: manim Novelty: winter stations appear, cold and shallow, inside both ranges (page results)

Winter brings cold water to the shallows. Its depth and its temperature each lie within
the survey's ranges, but never together.

## Scene 23
visual: manim Distance: a winter station and a line to its nearest surveyed station, across the inputs at once (schematic)

A check on one input at a time misses it. This one catches it: the distance from each
station to the nearest surveyed station, across all the inputs at once, with each input
scaled so that they count alike.

## Scene 24
visual: manim DistanceError: the forest's typical error in four groups, nearest to furthest from the survey, rising; "off by a factor of 2: twice or half the truth" (page results, sampling-and-extrapolation.qmd)

The forest's error grew with that distance. Here the error is the factor a prediction
is off by: twice the truth, or half of it, is off by a factor of 2. At the nearest
quarter of stations the forest was typically off by a factor of 1.4; at the furthest,
by 2.7. So map the distance beside the predictions, to show where the map is guessing.

## Scene 25
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. A model never says when it is guessing: measure how far each
prediction lies from the survey.

# Quiz

## Scene 26
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Two random forests score almost the same error on new sites. One learnt
from the log of the counts, a common step that squeezes the long tail of large catches.
Do they predict about the same number of animals in total?

## Scene 27
visual: manim QuizAnswer: "No"; bars for the animals caught, the forest on raw counts and the forest on log counts, each forest with its RMSE (page results, distributional-assumptions.qmd)

No. The stations caught 2,421 animals. The forest on raw counts predicts 2,514, and the
forest on log counts 1,699, 30 per cent short. A few large catches pull the average
above the typical catch. On log counts the forest aims at the typical catch, but a total
needs the average.

# Key points

## Scene 28
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: a model can fit well and still be
wrong.

## Scene 29
visual: manim KeyPoints: the second ticked

Two: rows are worth less than they seem.

## Scene 30
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: a model never says when it is guessing.

## Scene 31
visual: manim EndCard: the site's address and a thank-you

The pages also cover forecasts and rare species, with all the code. They are linked
below. Thanks for watching.
