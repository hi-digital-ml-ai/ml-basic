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

This video is built from three pages of the section, each a case where a good score
hides a problem: the loss decides what a prediction means (distributional assumptions:
two forests with the same RMSE, one 30 per cent short of the animals caught), a model
never says when it is guessing (uneven sampling and extrapolation: a new mix of
conditions passes the range check), and a rare answer fools accuracy (class imbalance:
95 per cent accurate while finding nothing, and rebalancing that only moves the
threshold). The quiz applies the third idea to a made-up rare event. Linearity and
dependent data are left to their pages, and the end card names them.

Earlier videos already taught squared and absolute error (How algorithms learn),
extrapolation and each method's own rule past the data, k-nearest neighbours, and
thresholds with false alarms and misses (Supervised learning). Here they get a one-line
reminder; the words go on what is new: which middle a loss aims at, a new mix of
conditions, the distance to the survey, sensitivity, specificity and precision, and why
rebalancing is a threshold in disguise.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about
assumptions: what a model takes for granted about its data. It covers three things:
why the loss decides what a prediction means, why a model never says when it is
guessing, and why a rare answer fools accuracy.

## Scene 2
visual: manim Hidden: a score card with a big tick; a magnifying glass passes over it and finds a crack: "a good score can hide a problem" (schematic)

Each part shows a model with a good score that hides a problem. The score alone never
reveals it. Knowing what the model assumes does.

# The loss decides what a prediction means

## Scene 3
visual: manim Checks: two boxes, "errors bell-shaped" and "equal spread everywhere"; "taught in statistics courses" (schematic)

First, why the loss decides what a prediction means. Statistics courses teach two
checks before fitting a model. A model's errors should follow a bell curve, the Normal
distribution, and they should spread equally everywhere.

## Scene 4
visual: manim Counts: a histogram of the 598 training stations' catches; 129 at zero, the median 3, the largest 40, the average 4.0 to the right of the median; "skewed: a long tail" (page results, distributional-assumptions.qmd)

Counts of animals fail both. Of 598 stations, 129 caught nothing, the middle station
caught 3, and the largest 40. A long tail like this is called skew. The few big catches
pull the average up to 4.0, above the middle catch, the median.

## Scene 5
visual: manim Errors: the random forest's errors against its predictions, fanning out; "1.8" and "7.7" for the spread in the lowest and highest fifth, "4.3 times as wide"; "the forest predicts well anyway" (page results, distributional-assumptions.qmd#fig-errors)

A random forest's errors fail both checks too. They are lopsided, and they spread 4.3
times wider where it predicts the most. Yet the forest predicts well. A tree predicts
the average catch of similar stations, and an average needs no bell curve.

## Scene 6
visual: manim Middles: a schematic histogram with a long tail; the median, the average and a far point marked: "absolute error: the median", "squared error: the average", "a quantile loss: any point you choose" (schematic)

So what does the shape change? What a prediction means. A prediction is one number
standing for all the catches a station could give, and the loss picks which one.
Squared error aims at the average. Absolute error aims at the median. And a quantile
loss aims at any point you choose, such as the catch only 1 in 20 stations exceed.

## Scene 7
visual: manim Logs: the long tail squeezed by taking logs, the histogram turning more bell-shaped; "a common habit" (schematic)

Now a common habit. Skewed counts are often turned into their logarithm before
fitting, which squeezes the long tail into something more bell-shaped. Fit a second
forest to the log counts, and turn its predictions back into animals.

## Scene 8
visual: manim Totals: two RMSEs, almost the same; then bars for the animals caught, the forest on raw counts and the forest on log counts, "30% short" (page results, distributional-assumptions.qmd)

The two forests score almost the same RMSE, 4.69 and 4.78. Now add up their
predictions. The stations caught 2,421 animals. The forest on raw counts predicts 2,514.
The forest on log counts predicts 1,699: 30 per cent short.

## Scene 9
visual: manim Middles: the histogram again; the log-count forest's aim near the median, "a total needs the average"; "keep the counts, or use a loss made for counts" (schematic)

Why? On the log scale, squared error aims at the average log count, and turned back
into animals, that lands near the median, the typical catch. A stock estimate needs
the average. So when totals matter, keep the counts as they are, or use a loss made
for counts, such as Poisson deviance.

## Scene 10
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. The loss decides what a prediction means: for skewed counts, the
average and the typical catch differ, and a total needs the average.

# A model never says when it is guessing

## Scene 11
visual: manim Easy: one input as a line, the survey's range marked; a new station beyond it, flagged "outside the range: easy to spot"; then a question mark: "inside every range?" (schematic)

Next, why a model never says when it is guessing. Survey effort is uneven: it follows
ports, weather and ship time. As the Supervised learning video showed, past the data
each model follows its own rule. A station outside the survey's range is easy to spot.
The hard case is a station inside every range.

## Scene 12
visual: manim Novelty: temperature against depth for the summer and autumn survey, cold water only at depth (page results, sampling-and-extrapolation.qmd#fig-novelty)

Here is a survey that sailed only in summer and autumn. Each dot is a station, placed
by its depth and its temperature. In those seasons the shallows are warm, so the survey
met cold water only at depth.

## Scene 13
visual: manim Novelty: winter stations appear, cold and shallow, inside the dashed box of the survey's ranges; "each value seen, never together" (page results)

Then the model is asked about winter, when the shallows turn cold. Each winter station's
depth was seen, and so was its temperature, but never together. The forest has no
stations like these to learn from.

## Scene 14
visual: manim RangeCheck: 406 spring and winter stations; 279 pass the range check on every input; 132 of those far from every surveyed station, 47% (page results, sampling-and-extrapolation.qmd)

The usual check takes one input at a time. Of 406 spring and winter stations, 279 pass
it on every input. Yet 132 of those, almost half, lie far from every surveyed station.

## Scene 15
visual: manim Distance: a winter station and a line to its nearest surveyed station, across the inputs at once (schematic)

A better check looks at all the inputs at once: the distance from each station to the
nearest surveyed station, the same distance k-nearest neighbours uses to find its
neighbours. Far from every surveyed station means the model is on its own.

## Scene 16
visual: manim DistanceError: the forest's typical error in four groups, nearest to furthest from the survey, rising from 1.4 to 2.7; "off by a factor of 2: twice or half the truth"; "map the distance beside the predictions" (page results, sampling-and-extrapolation.qmd)

And it works. Because the survey is simulated, the forest can be checked against the
truth. Its error is the factor it is off by, so twice the truth or half of it is a
factor of 2. Nearest the survey, it was typically off by 1.4; furthest away, by 2.7.
So map the distance beside the predictions, to show where the model is guessing.

## Scene 17
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. A model never says when it is guessing: measure how far each station
lies from the survey, on all the inputs at once.

# A rare answer fools accuracy

## Scene 18
visual: manim Rare: 598 training stations as dots, the 29 with a rare species lit up; "4.8%"; "imbalanced classes" (page results, class-imbalance.qmd)

Finally, why a rare answer fools accuracy. Many things marine scientists most want to
predict are rare: a protected species, a harmful algal bloom. Here a second species
turns up at only 29 of 598 stations, 4.8 per cent. When one answer is much rarer than
the other, the classes are called imbalanced.

## Scene 19
visual: manim Trap: logistic regression's calls at the threshold of 0.5; "presences found: 0"; "accuracy: 95%" (page results, class-imbalance.qmd)

Logistic regression gives each station a probability of presence, and as in the
Supervised learning video, a threshold of 0.5 turns it into a call. Here it finds none
of the presences. Yet its accuracy, the share of calls that are right, is 95 per cent:
calling the species absent everywhere is right almost everywhere.

## Scene 20
visual: manim Measures: twenty cases, four truly present and sixteen absent, six called present; sensitivity, specificity and precision each lighting its group (schematic, after class-imbalance.qmd img/three-measures.svg)

So count the two kinds of mistake apart. Sensitivity: of the stations with the
species, the share called present; misses lower it. Specificity: of the stations
without it, the share called absent; false alarms lower it. Precision: of the stations
called present, the share that truly have it.

## Scene 21
visual: manim Rebalance: the training stations; upsampling copies each presence about 20 times; downsampling drops absences; "only the training data change" (schematic, with the page's 20)

The usual fix is rebalancing: change the training data so both answers are equally
common. Upsampling copies each presence, here about 20 times. Downsampling drops
absences until the two match. Only the data the model learns from change; it is still
scored on the real mix.

## Scene 22
visual: manim Rebalanced: sensitivity 0 rising to about 0.7; 31% of absences become false alarms; precision: about 1 in 9 called present holds the species (page results, class-imbalance.qmd)

Both raise the sensitivity from 0 to about 0.7: most presences are now found. The
price is false alarms, at about 31 per cent of the absences. And precision stays low:
only about 1 in 9 stations called present holds the species.

## Scene 23
visual: manim Curve: sensitivity against specificity for every threshold, no rebalancing; upsampling at 0.5 lands exactly on the point for a threshold of 0.048 (page results, class-imbalance.qmd#fig-curve)

Now leave the data alone and lower the threshold instead, to 0.048, the share of
stations with the species. The calls come out the same as upsampling: a sensitivity of
0.717 and a specificity of 0.712 both ways. Copying the presences raises every
station's probability but keeps their order, so a cut at 0.5 after copying falls in
the same place as a cut at 0.048 before.

## Scene 24
visual: manim Chances: the average probability against the share of stations with the species, without rebalancing (0.048 against 4.8%) and after upsampling (0.34, about 7 times too high); "choose the threshold from the costs" (page results, class-imbalance.qmd)

Rebalancing also does harm. After upsampling, the probabilities average 0.34, about 7
times the real share: they are no longer chances. So leave the data alone, and choose
the threshold from what a miss and a false alarm each cost.

## Scene 25
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. A rare answer fools accuracy: report sensitivity, specificity and
precision, and move the threshold rather than the data.

# Quiz

## Scene 26
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A harmful algal bloom occurs on 2 days in 100. A model that warns of blooms
is 98 per cent accurate. Is it a good model?

## Scene 27
visual: manim QuizAnswer: "Can't tell yet"; a model that never warns: 98% accurate, sensitivity 0; "ask for sensitivity and precision" (schematic)

You can't tell yet. A model that never warns is also 98 per cent accurate, and it
misses every bloom. Ask for its sensitivity, how many blooms it catches, and its
precision, how many of its warnings are real.

# Key points

## Scene 28
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: the loss decides what a prediction
means.

## Scene 29
visual: manim KeyPoints: the second ticked

Two: a model never says when it is guessing.

## Scene 30
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: a rare answer fools accuracy.

## Scene 31
visual: manim EndCard: the site's address and a thank-you

The pages also cover straight lines and curves, and repeat visits to the same sites,
with all the code. They are linked below. Thanks for watching.
