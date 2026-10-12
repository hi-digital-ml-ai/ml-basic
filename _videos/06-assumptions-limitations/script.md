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

This video is an overview built on three ideas, each with one example and the reason
behind it: a model can fit well and still be wrong (the random forest's depth curve,
explained as confounding), rows are worth less than they seem (repeat visits and the
effective sample size), and a model never says when it is guessing (past the survey's
depths, and a new mix of conditions). The quiz applies the second idea. It does not
tour every page: the error check along each input, blocks of the map, what the forest's
inputs explain, polynomial regression past the data, what each loss aims at, samples
from one year and class imbalance are left to the pages, and the end card names some
of them. Each true curve is shown only after the model's own answer.

Earlier videos already taught linear regression and random forests (Supervised
learning), repeat visits that are not independent (Marine data), resamples (Supervised
learning), extrapolation and each method's own rule past the data (Supervised learning)
and whole-site folds (Generalisation). Here they get a one-line reminder, not a re-run;
the words go on confounding, the effective sample size and why a forest runs flat.
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
visual: manim Simulated: a "true process" box sends dots to a map of stations (schematic)

As in the other videos, the survey is simulated: we wrote the process that makes its
counts. So a model's answers can be checked against the truth, which no real study can
do.

# A model can fit well and still be wrong

## Scene 3
visual: manim Shapes: a straight line fails a hump; a random forest follows it in steps (schematic)

First, why a model can fit well and still be wrong. Few marine responses are straight
lines. A linear model, such as linear regression, assumes they are: each extra degree
or metre always adds the same amount. A random forest, many decision trees averaged,
does not. Its trees split the stations into groups, so it follows the data in steps,
with no shape chosen in advance.

## Scene 4
visual: manim Truth: the forest's temperature curve, then the simulation's curve dashed over it (page results, linearity-and-nonlinearity.qmd#fig-truth)

Fit a random forest to the survey, and draw how its prediction changes with
temperature, with the other inputs held fixed. It finds a hump, a temperature where the
species does best, without being told the shape. The dashed line is the true curve, the
one the simulation used, and the forest follows it closely.

## Scene 5
visual: manim Truth: the depth panel, the forest's peak in shallow water, the true peak at 80 m, the stretch between them shaded (page results)

For depth, it does not. The forest puts the most animals at 17 metres, and the truth is
80. Yet the forest fits the survey well, and nothing in its predictions warns of the
mistake. A map drawn from this curve would send the next survey to the wrong depth.

## Scene 6
visual: manim Shelf: a cross-section from the coast to open sea, the seabed deepening; along it, depth changes and so does something no input measures; the forest sees only depth, which takes the credit (schematic)

Why? The shelf deepens offshore. So moving away from the coast changes the depth, but
it can change other things too, things that no input measures. Both change together,
station by station, so the forest cannot tell them apart. It sees only depth, so depth
takes the credit for both.

## Scene 7
visual: manim Confounding: "confounding" and its meaning; position, depth and the count as three boxes; then fish, fishing boats and seabirds in the same three places; "a better fit cannot fix it: measure the hidden cause" (schematic)

This is called confounding. A confounder is a hidden cause linked to both an input and
the outcome: here, position sets the depth and also changes the catch. Think of
seabirds and fishing boats. They gather in the same places, but the boats do not draw
the birds: the fish draw both. A better-fitting curve cannot fix this, because the data
look the same either way. Only measuring the hidden cause can.

## Scene 8
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. A model can fit well and still be wrong: a curve that follows the data
can credit the wrong input.

# Rows are worth less than they seem

## Scene 9
visual: manim Visits: 800 stations as squares, which gather into 160 sites; one site's visits highlighted; "dependent data" (page results, dependent-data.qmd)

Next, why rows are worth less than they seem. The survey holds 800 stations, from only
160 sites visited again and again. As the Marine data video showed, visits to one site
share its depth, its seabed and its water, so they partly repeat each other. Ask one
person the same question twice, and you get two answers but only one opinion. Data like
these are called dependent: each visit says something about the others.

## Scene 10
visual: manim Resample: stations drawn at random, then whole sites drawn with all their visits; the average catch of each draw marked on a line (schematic)

How much less are they worth? A resample can tell. Draw stations at random, as many as
the survey holds, so some come up twice and some not at all: a survey that might have
been. Work out its average catch, and do it many times. The more the averages move, the
less sure the survey is of its average. Then draw whole sites instead, each with all
its visits, because a new survey would bring new sites, not just new visits.

## Scene 11
visual: manim Spreads: the 500 averages drawn by station, and the 500 by site, wider; "worth about 470 stations"; "the effective sample size" (page results, dependent-data.qmd)

Drawing whole sites spreads the averages 1.31 times wider. That is the spread an
average of only about 470 independent stations would have, so the 800 stations are
worth about 470. This is the survey's effective sample size: how many independent rows
the data are really worth. Count all 800, and the survey seems surer of its average
than it is.

## Scene 12
visual: manim Unseen: one site's visits, some fitted and some held out, "already seen"; then the whole site held out, "a new site" (schematic)

The same goes for a model's score. Hold out a few visits to a site whose other visits
were fitted, and the model has, in effect, seen that site already. Its score looks
better than it will be at a new site. That is why the Generalisation video held out
whole sites.

## Scene 13
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Rows are worth less than they seem: visits to one site repeat each
other, so score a model on sites it has never seen.

# A model never says when it is guessing

## Scene 14
visual: manim Beyond: the true mean count against depth, the survey's depths to 100 m unshaded, deeper water shaded; "extrapolation: predicting beyond the data" (page results, sampling-and-extrapolation.qmd#fig-beyond)

Finally, why a model never says when it is guessing. Survey effort is never even: it
follows ports, weather and ship time. Suppose the survey reached only sites shallower
than 100 metres, and a model must map the deeper ones. The line is the true average
count at each depth. As in the Supervised learning video, predicting beyond the data is
called extrapolation.

## Scene 15
visual: manim Beyond: ten random forests, one per survey, follow the truth to 100 m and run flat beyond it; "deeper than the deepest station: the same leaf" (page results)

Ten random forests, each fitted to a different part of the survey, follow the truth
within its depths. Beyond, they run flat, while the true count keeps falling. Why? A
tree only asks whether a station is deeper or shallower than depths it has seen. A
station far deeper gets the same answers as the deepest station it saw, so it lands in
the same leaf and gets the same prediction.

## Scene 16
visual: manim Beyond: "below 140 m: 1.8 to 2.8 times the truth" on screen only (page results)

Below 140 metres they are too high on all ten surveys, and nothing in their
predictions says so.

## Scene 17
visual: manim Novelty: temperature against depth for the summer and autumn survey, cold water only at depth (page results, sampling-and-extrapolation.qmd#fig-novelty)

A new mix of conditions is harder to spot. Here each dot is a station, placed by its
depth and its temperature. A survey that sailed only in summer and autumn met cold
water only at depth.

## Scene 18
visual: manim Novelty: winter stations appear, cold and shallow, inside both ranges (page results)

Winter brings cold water to the shallows. Its depth and its temperature each lie within
the survey's ranges, but never together. The forest has no stations like these to
learn from, so it is guessing here too.

## Scene 19
visual: manim Distance: a winter station and a line to its nearest surveyed station, across the inputs at once; "map the distance beside the predictions" (schematic)

A check on one input at a time misses it. A better check is the distance from each
station to the nearest surveyed station, across all the inputs at once. On the survey,
the forest's errors grew with that distance. So map the distance beside the
predictions, to show where the map is guessing.

## Scene 20
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. A model never says when it is guessing: measure how far each
prediction lies from the survey.

# Quiz

## Scene 21
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Two surveys each record 800 stations. One visits 800 different sites, once
each. The other visits 160 sites, five times each. Which gives the surer average
catch?

## Scene 22
visual: manim QuizAnswer: "The first"; 800 squares each on its own site, against 160 stacks of five; "worth about 470, like this video's survey" (schematic, with the page's 470)

The first. Each of its stations brings a new site. In the second, visits to one site
partly repeat each other, so its 800 stations are worth fewer: in this video's survey,
about 470.

# Key points

## Scene 23
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: a model can fit well and still be
wrong.

## Scene 24
visual: manim KeyPoints: the second ticked

Two: rows are worth less than they seem.

## Scene 25
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: a model never says when it is guessing.

## Scene 26
visual: manim EndCard: the site's address and a thank-you

The pages also cover blocks of the map, what a model assumes about counts, forecasts
and rare species, with all the code. They are linked below. Thanks for watching.
