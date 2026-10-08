---
title: "Supervised learning: from a straight line to boosting"
section: chapters/03-supervised-learning/index.qmd
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

This video is an overview: it introduces the section and says what its seven pages
cover, without teaching each page in full. It uses only the methods the section
introduces, and never says which variables truly drive the species. "Poisson" is
respelled for the voice in _videos/pronunciation.yml; the captions keep the spelling.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

This video is a short tour of supervised learning. It covers three things: models
that add up their inputs, models that learn their shape from the data, and how to
choose between them.

# Models that add up their inputs

## Scene 2
visual: manim Outcome: a quantity on a number line, "regression"; a category as present and absent, "classification" (schematic)

Supervised learning starts from the outcome. A quantity, such as a temperature or a
count, calls for regression. A category, such as present or absent, calls for
classification.

## Scene 3
visual: manim Histogram: stations by the number of animals caught, "never below zero" at the left edge, "a few large catches" at the right (page results, count-regression.qmd)

In this section, the outcome is the count of one species at each station of the
survey. A count is a whole number, it never falls below zero, and most stations
caught only a few animals.

## Scene 4
visual: manim Curves: predicted count against temperature, the straight line of linear regression (page results, linear-and-polynomial-regression.qmd#fig-shapes)

Linear regression predicts a starting value plus a fixed amount for each input. Against
temperature, that is one slope, the same in cold water and warm.

## Scene 5
visual: manim Curves: polynomial regression added, rising to a peak marked at 7.5 °C (page results, linear-and-polynomial-regression.qmd#fig-shapes)

Add the square of temperature as one more column, and the line bends into a curve.
This is polynomial regression, and it finds a peak at 7.5 degrees.

## Scene 6
visual: manim Curves: the part of the curve below zero shaded, "fewer than zero animals", 12 of 202 test stations (page results, linear-and-polynomial-regression.qmd)

But nothing in linear regression knows that a count stops at zero. In warm water the
curve falls below it, and it predicts fewer than zero animals at 12 of the 202 test
stations.

## Scene 7
visual: manim Curves: Poisson regression added, levelling off just above zero (page results, count-regression.qmd#fig-shapes)

Poisson regression predicts the logarithm of the count instead. Turned back into a
count, a prediction can come close to zero, but never cross it.

## Scene 8
visual: manim Multipliers: sand as 1, mud as 1.34 times sand, rock below 1 (page results, count-regression.qmd#each-coefficient-is-a-multiplier)

Its coefficients become multipliers. With everything else held fixed, a muddy station
is expected to hold 1.34 times the count of a sandy one.

## Scene 9
visual: manim Logistic: the probability of presence against temperature, between 0 and 1, the training stations as dots along the top and bottom (page results, logistic-regression.qmd#fig-curve)

For present or absent, logistic regression uses the same design to predict a
probability, which always stays between zero and one.

## Scene 10
visual: manim Mistakes: a threshold turns the probability into present or absent; two cards, a false alarm (said present, was absent) and a miss (said absent, was present) (schematic)

A threshold turns the probability into an answer: present or absent. The answer can be
wrong in two ways. A false alarm says present where the species was absent. A miss
says absent where it was present.

## Scene 11
visual: manim Thresholds: false alarms and misses on the test sites at thresholds 0.5 and 0.9, 34 and 4, then 6 and 97; "what does each mistake cost?" (page results, logistic-regression.qmd)
pause-after: 0.5

At a threshold of 0.5, the model gives 34 false alarms and 4 misses. Raise it to 0.9,
and the false alarms fall to 6, but the misses rise to 97. The right threshold depends
on what each mistake costs.

## Scene 12
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. Match the model to the outcome: a count is never negative, and a
probability needs a threshold you choose.

# Models that learn their shape

## Scene 13
visual: manim Neighbours: "k-nearest neighbours" as the heading; stations as grey dots on two inputs, a new station, its five nearest joined to it and ringed, "k = 5", "prediction: their average count" (schematic, after nearest-neighbours.qmd img/nearest-neighbours.svg)

Each of these models assumes a shape, such as a line or a curve. k-nearest neighbours
assumes none. For a new station, it finds the k most similar stations in
the training data and averages their counts.

## Scene 14
visual: manim Neighbours: the error against the number of neighbours, on the fitting stations and on the validation sites; the first at zero for one neighbour, the second at its worst there; both rising towards 300 (page results, nearest-neighbours.qmd#fig-neighbours)

With one neighbour, it copies every chance high and low: perfect on the stations it
learned from, and worst of all on the validation sites, which were held back from
fitting. This is overfitting. With hundreds of neighbours, every prediction blurs into
one average.

## Scene 15
visual: manim Neighbours: the validation error lowest at 30 neighbours, marked; "a hyperparameter: chosen on validation data" (page results, nearest-neighbours.qmd#fig-neighbours)
pause-after: 0.5

In between, the validation error is lowest at 30 neighbours. A setting like k, fixed
before the model is fitted, is called a hyperparameter. It is chosen on validation
data, never on the data the model learned from.

## Scene 16
visual: manim Tree: "a decision tree" as the heading; the depth-3 tree for the count grows question by question, chlorophyll first, then two questions on temperature (page results, decision-trees.qmd#fig-tree)

A decision tree works differently. It asks yes-or-no questions about the inputs, and
each leaf predicts the average of the stations that reach it.

## Scene 17
visual: manim Tree: the band between 6.4 and 10.4 °C highlighted, average 5.2 animals, against 1.5 below and 2.6 above (page results, decision-trees.qmd)

On the survey, two questions about temperature find a band, from 6.4 to 10.4 degrees,
with the most animals. A peak takes one question for each side.

## Scene 18
visual: manim Depth: the error on the fitting stations and on the validation sites against depth; the first falling towards zero, the second lowest at depth 5 (page results, decision-trees.qmd#fig-depth)
pause-after: 0.5

The tree's depth is a hyperparameter too. A deeper tree fits the stations it learned
from ever more closely, but on the validation sites the error is lowest at depth 5,
then climbs.

## Scene 19
visual: manim Resamples: six trees from resampled stations, each opening on chlorophyll, their thresholds marked on one line from 2.57 to 12.6 (page results, forests-and-boosting.qmd)

One tree is also unstable. Grow it on six resamples of the same stations, and the first
question is always about chlorophyll, but its threshold moves from 2.57 to 12.6.

## Scene 20
visual: manim Forest: thirty of the page's forest's trees as thin staircases across temperature, then the average of all its trees as a thick line in small steps (page results, forests-and-boosting.qmd)

A random forest grows hundreds of trees, each on a resampled copy of the data, and
averages them. The big jumps shrink into small steps.

## Scene 21
visual: manim Boosting: small trees in a row, each arrow labelled "errors", their sum the prediction (schematic, after forests-and-boosting.qmd img/forest-and-boosting.svg)

Boosting adds small trees one after another. Each new tree is fitted to the errors
left by the trees before it.

## Scene 22
visual: manim Counts: error on the validation sites against the number of trees, the forest flat, boosting lowest at 200 and rising (page results, forests-and-boosting.qmd#fig-trees)
pause-after: 0.5

More trees never hurt a forest. Boosting is different: on the validation sites it does
best at 200 trees, then gets worse, as the later trees fit the noise.

## Scene 23
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Flexible models learn the shape themselves, but a hyperparameter sets
how closely they fit, and it is chosen on validation data.

# Choosing between them

## Scene 24
visual: manim Questions: five cards, the aim, the outcome, the range, the data, the audience (schematic, after choosing-a-method.qmd img/choosing-a-method.svg)

So which method should you use? Five questions narrow the choice: the aim, the kind of
outcome, the range you must predict over, how much data you have, and who must accept
the result.

## Scene 25
visual: manim Comparison: the seven models' test RMSE as dots, ordered, Poisson regression first and the three tree models last (page results, choosing-a-method.qmd#fig-comparison)

Scored on the same new sites, Poisson regression comes first, and the three tree
models last. A few hundred noisy stations are too few for the flexible methods to beat
a simple curve.

## Scene 26
visual: manim Comparison: the validation dots added, the tree first there; the tree's and boosting's gaps from validation to test marked "tuned on these sites"; "one split cannot separate close models" (page results, choosing-a-method.qmd#fig-comparison)
pause-after: 0.5

On the validation sites, though, the single tree came first. Its depth, and boosting's
number of trees, were chosen on those same sites, so both were tuned to their chance
patterns: a kind of overfitting. The test sites, kept apart, show the cost. And one
split cannot tell apart models that are close.

## Scene 27
visual: manim Beyond: three models from 0 to 22 °C, the shaded ends beyond the data; the forest level, Poisson regression flattening to zero, linear regression falling below it (page results, choosing-a-method.qmd#fig-extrapolate)

Beyond the sampled temperatures, each model follows its own rule. The forest stays
level, Poisson regression flattens towards zero, and linear regression falls below
zero.

## Scene 28
visual: manim Beyond: "nothing in the data says which is right", "choose an assumption you can defend"
pause-after: 0.5

Nothing in the data says which is right. So choose a model whose assumption you can
defend, and say what it is.

## Scene 29
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Start from the question and the outcome, not from the most flexible
method.

# Quiz

## Scene 30
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A colleague models counts of a species with linear regression, and a few
predictions come out below zero. They set those to zero. Is the problem solved?

## Scene 31
visual: manim QuizAnswer: "no"; the negative predictions clipped to zero, the model beneath unchanged; then Poisson regression, never below zero (schematic)

No. Clipping hides the symptom, but the model still assumes a count can fall below
zero. A count model, such as Poisson regression, cannot make that mistake.

# Key points

## Scene 32
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: match the model to the outcome.

## Scene 33
visual: manim KeyPoints: the second ticked

Two: flexible models learn the shape, but a hyperparameter, chosen on validation data,
sets how closely.

## Scene 34
visual: manim KeyPoints: the third ticked

Three: start from the question, not the most flexible method.

## Scene 35
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
