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

In this video, you will learn three things. Why a model can fit well and still be
wrong. Why rows are worth less than they seem. And why a model never says when it is
guessing.

## Scene 2
visual: manim Assumes: "assumption-free" struck through; two panels, "freed from" straight lines, "not freed from" how the data were collected (schematic)

Machine learning is often called assumption-free. It frees a model from straight
lines, but not from the way its data were collected.

## Scene 3
visual: manim Simulated: a "true process" box sends dots to a map of stations (schematic)

The survey in this course is simulated, so a model's answers can be checked against
the truth, which no real study can do.

# A model can fit well and still be wrong

## Scene 4
visual: manim Shapes: a straight line fails a hump; a random forest follows it in steps (schematic)

Few marine responses are straight lines. Linear models assume them; random forests do
not. They follow the data in steps, with no shape chosen in advance.

## Scene 5
visual: manim ErrorCheck: linear regression's average error, caught − predicted, in ten groups along each input; temperature's hump stands out (page results, linearity-and-nonlinearity.qmd#fig-errors)

To check the straight-line assumption, fit a linear regression and average its errors,
the animals caught minus the number predicted, in ten groups along each input. Where
the line is right, the average stays near zero. For temperature it rises and falls: the
line predicts too many animals in the coldest and warmest water, and too few in
between, where the species does best.

## Scene 6
visual: manim Truth: the forest's temperature curve, then the simulation's curve dashed over it (page results, linearity-and-nonlinearity.qmd#fig-truth)

A random forest can bend, so it finds that hump without being told its shape, close to
the true curve.

## Scene 7
visual: manim Truth: the depth panel, the forest's peak in shallow water, the true peak at 80 m, the stretch between them shaded (page results)

For depth, it does not. The forest puts the most animals at 17 metres, and the truth is
80. Nothing warned of it: the error check showed no pattern along depth. A map drawn
from this curve would send the next survey to the wrong depth.

## Scene 8
visual: manim Confounding: depth and the species both linked to position, with an unmeasured patch behind position (schematic)

Depth follows position, because the shelf deepens offshore. So something about
position that no input measures ends up in depth's curve. This is confounding, and no
choice of shape removes it.

## Scene 9
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. A model can fit well and still be wrong: a curve that follows the data
can credit the wrong input.

# Rows are worth less than they seem

## Scene 10
visual: manim Visits: 800 stations as squares, which gather into 160 sites; one site's visits highlighted (page results, dependent-data.qmd)

The survey holds 800 stations, from only 160 sites visited again and again. Visits to
one site share its depth, its seabed and its water, so they partly repeat each other.

## Scene 11
visual: manim Resample: stations drawn at random, then whole sites drawn with all their visits (schematic)

To measure by how much, resample: draw stations at random, many times, and watch the
average catch move. Then draw whole sites instead.

## Scene 12
visual: manim Spreads: the 500 averages drawn by station, and the 500 by site, wider; "worth about 470 stations" (page results, dependent-data.qmd)

Drawing whole sites spreads the average 1.31 times wider. The spread shrinks with the
square root of the number of independent rows, so the 800 stations are worth only about
470 independent ones: the survey's effective sample size. Count all 800, and an
interval for the average comes out too narrow.

## Scene 13
visual: manim Blocks: the sites on the map, then the squares of the map; the 500 averages drawn by block spread wider still; "worth about 150" (page results, dependent-data.qmd)

Neighbouring sites share their water too. Draw whole squares of the map, each with
every site in it, and the average spreads 2.34 times wider. Then the 800 stations are
worth only about 150.

## Scene 14
visual: manim Errors: how much wider each way of drawing spreads, for the catch (by site, by block), then for the forest's errors by site (page results, dependent-data.qmd#fig-spread)

A model's inputs can explain some of this. Resample a random forest's errors on sites
it never saw, instead of the catch. By site, they still spread 1.25 times wider, almost
as much as the catch: what a site's visits share, the inputs miss. So the forest must be
scored on sites it has never seen.

## Scene 15
visual: manim Errors: the forest's errors by block join the chart, far below the catch's (page results)

By block, the errors spread only 1.36 times wider, against 2.34 for the catch. Most of
what neighbours share is their depth and water, and the forest already knows those.
Some may remain, so a map of areas nobody has surveyed is scored on held-out areas.

## Scene 16
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Rows are worth less than they seem: visits to one site repeat each
other, so score a model on sites it has never seen.

# A model never says when it is guessing

## Scene 17
visual: manim Beyond: the true mean count against depth, the survey's depths to 100 m unshaded, deeper water shaded (page results, sampling-and-extrapolation.qmd#fig-beyond)

Survey effort is never even. Suppose the survey reached only sites shallower than 100
metres, and a model must map the deeper ones.

## Scene 18
visual: manim Beyond: ten random forests, one per survey, follow the truth to 100 m and run flat beyond it (page results)

Within the survey's depths, ten random forests follow the truth. Below, they run flat,
while the true count keeps falling. A tree sends every deeper station to the leaf of the
deepest stations it saw, so the forest repeats its value at the edge.

## Scene 19
visual: manim Beyond: "below 140 m: 1.8 to 2.8 times the truth" on screen only (page results)

Below 140 metres they are too high on all ten surveys, and nothing in their
predictions says so.

## Scene 20
visual: manim Beyond: the forests fade; ten polynomial regressions follow the truth to 100 m and fan out beyond it; "0.7 to 3.7 times the truth" (page results, sampling-and-extrapolation.qmd#fig-beyond)

A polynomial regression fans out instead. Fits that agree within the survey bend in
different directions below it, from 0.7 to 3.7 times the truth. Each method follows its
own rule past the data.

## Scene 21
visual: manim Novelty: temperature against depth for the summer and autumn survey, cold water only at depth (page results, sampling-and-extrapolation.qmd#fig-novelty)

A new mix of conditions is harder to spot. A survey in summer and autumn met cold
water only at depth.

## Scene 22
visual: manim Novelty: winter stations appear, cold and shallow, inside both ranges (page results)

Winter brings cold water to the shallows. Its depth and its temperature each lie within
the survey's ranges, but never together.

## Scene 23
visual: manim Distance: a winter station and a line to its nearest surveyed station, across the inputs at once (schematic)

One check catches it: the distance from each station to the nearest surveyed station,
across all the inputs at once.

## Scene 24
visual: manim DistanceError: the forest's typical error in four groups, nearest to furthest from the survey, rising (page results, sampling-and-extrapolation.qmd)

The forest's error grew with that distance. At the nearest quarter of stations it was
typically off by a factor of 1.4; at the furthest, by 2.7. So map the distance beside
the predictions, to show where the map is guessing.

## Scene 25
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. A model never says when it is guessing: measure how far each
prediction lies from the survey.

# Quiz

## Scene 26
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Two random forests score almost the same error on new sites. One learnt
from the log of the counts, a common step for skewed data. Do they predict about the
same number of animals in total?

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
visual: manim KeyPoints: the third ticked

Three: a model never says when it is guessing.

## Scene 31
visual: manim EndCard: the site's address and a thank-you

The pages also cover forecasts and rare species, with all the code. They are linked
below. Thanks for watching.
