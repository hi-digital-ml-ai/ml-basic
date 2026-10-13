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

Rebuilt 2026-10-13 as an introduction, one new concept per part, each with one example
and one picture: test on what the model will face (folds of stations against blocks of
the map), measure what matters (sensitivity and specificity, on the Assumptions video's
rare species, which that video promised Validation would measure), and a score needs an
interval (resampling the sites). Cross-validation is known from the Generalisation
video and gets a clause, not a re-run. Nested cross-validation, RMSE against MAE,
shortlists, the cost threshold and the paired comparison stay on the pages; the end
card names some of them.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about
validation: how far to trust a model's score. It covers three things: why to test a
model on what it will face, why to measure what matters, and why a score needs an
interval.

# Test on what the model will face

## Scene 2
visual: manim Claim: a model, a score card, and an arrow to sites not yet surveyed (schematic)

First, why to test a model on what it will face. A model's score says how far its
predictions land from data it was not fitted to. It is a promise about new places: this
is how well the model will do where it has not been. So the test data should be as new
as those places.

## Scene 3
visual: manim Neighbours: sites as clusters of visits; single held-out stations, each next to visits to its own site that stay in the training data (schematic)

Say the test holds out single stations. Most sites in the survey were visited several
times, so a held-out station's own site, visited at other times, is usually still in the
training data. The model has, in effect, already seen that place.

## Scene 4
visual: manim Blocks: the survey's sites on the map, cut into squares; every site in one square held out (schematic)

Now hold out a whole block of the map instead: a square, with every site in it. The
model must predict an area it has never seen, which is what a map of new areas asks of
it.

## Scene 5
visual: manim BlockResult: the same random forest's error, held-out stations against held-out blocks (page results, spatial-and-temporal-cv.qmd)

Here is one random forest, scored both ways. Holding out single stations, its error is
4.23. Holding out blocks, it is 4.41. The model is the same; only the test is harder.
So test a model the way it will be used.

## Scene 6
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. Test a model on what it will face: to map new areas, hold out whole
areas.

# Measure what matters

## Scene 7
visual: manim Rare: the Assumptions video's grid of stations, the rare species lit, the model's calls as squares; its accuracy (page results, ../06-assumptions-limitations/class-imbalance.qmd)

Next, why to measure what matters. Remember the rare species from the Assumptions and
limitations video. A model was 92 per cent accurate, yet found only one presence in six.
Accuracy hid the misses. So what should we measure instead?

## Scene 8
visual: manim Rare: the presences ringed; sensitivity, one in six (page results)

The share of the presences a model finds is called its sensitivity. Here it is one in
six. Sensitivity counts the misses.

## Scene 9
visual: manim Rare: the absences picked out; specificity, 96 per cent; "accuracy is almost all specificity" (page results)

The share of the absences it calls absent is called its specificity. Here it is 96 per
cent. Specificity counts the false alarms. With so few presences, accuracy is almost all
specificity, which is why it looked so good.

## Scene 10
visual: manim Costs: a miss, a record lost, and a false alarm, a wasted dive, as squares sized by what they cost (schematic)

Which one matters more depends on what each mistake costs. For a protected species, a
miss means a record lost. For a survey with costly dives, a false alarm means a wasted
dive. So decide what the predictions are for, then choose the measure.

## Scene 11
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Measure what matters: report sensitivity and specificity, not accuracy
alone.

# A score needs an interval

## Scene 12
visual: manim OneSurvey: the survey's sites and the forest's score; other sites the survey might have drawn, the score moving with them (schematic)

Finally, why a score needs an interval. Scored by cross-validation by site, the random
forest's error is 4.32. But that number comes from one survey. With other sites, it
would have come out higher or lower.

## Scene 13
visual: manim Resample: the 160 sites drawn again with replacement, some twice, some not at all; each draw gives one error (schematic)

To see how far, draw the survey again from itself, which is called resampling. Draw 160
sites from its own 160, with replacement, so some come up twice and some not at all.
Work out the forest's error on them, and do it a thousand times.

## Scene 14
visual: manim Interval: the thousand errors as a histogram; the middle 95 per cent shaded, from 3.75 to 4.94 (page results, uncertainty-and-stability.qmd)

The middle 95 per cent of those thousand errors is a 95 per cent interval. For the
forest, it runs from 3.75 to 4.94. Its error on new sites could be anywhere in that
range, not exactly 4.32.

## Scene 15
visual: manim Intervals: the forest's interval, then linear regression's and predicting the average's, all overlapping (page results, uncertainty-and-stability.qmd)

Add linear regression and predicting the average, and all three intervals overlap. So a
small gap between two scores is not, on its own, a ranking: with other sites, the order
could change.

## Scene 16
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. A score needs an interval: resample the sites to see how far it could
move.

# Quiz

## Scene 17
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. You will use a model to map a stretch of coast that nobody has surveyed.
Which test gives the honest score: holding out single stations, or whole blocks of the
map?

## Scene 18
visual: manim QuizAnswer: "whole blocks"; the two scores again, the blocks' one picked out (page results)

Whole blocks. Holding out single stations leaves each station's neighbours in the
training data, so the score flatters the model. On the survey, that was 4.23 against
4.41.

# Key points

## Scene 19
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: test a model on what it will face.

## Scene 20
visual: manim KeyPoints: the second ticked

Two: measure what matters.

## Scene 21
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: a score needs an interval.

## Scene 22
visual: manim EndCard: the site's address and a thank-you

The pages go further: forecasts tested on later years, measures for counts, comparing
two models fairly, and choosing among many models without fooling yourself, with all the
code. They are linked below. Thanks for watching.
