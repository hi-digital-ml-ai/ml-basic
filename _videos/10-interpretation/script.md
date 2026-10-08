---
title: "Interpretation: what a model can honestly tell you"
section: chapters/10-interpretation/index.qmd
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

This video is an overview built on three ideas, each with one example: test what a
model relies on against random numbers and on more than one split (feature importance,
with partial dependence and the GAM for the shape), name an interval and check its
coverage (the GAM's two intervals, then a conformal interval that lapses at new kinds
of station), and a score cannot check the records (the gear that misses animals on
rock). The quiz is the reproducibility page's seed against split. The depth curve that
follows position is left to the pages: the assumptions video already tells it. The
truth of the simulation is never shown; every check here is one a real study can make.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. Which inputs a model relies on, and how to
test the answer. Which interval to quote with a prediction. And what a good score
cannot check.

## Scene 2
visual: manim Questions: a score card, then three questions beside it: what did it find, how sure is it, can the records be trusted (schematic)

A score says how well a model predicts new sites. A study has to say more: what the
model found, how sure it is, and whether the records behind it can be trusted.

## Scene 3
visual: manim Survey: a map of stations, each with its depth, temperature, seabed and season appearing as named (schematic)

As throughout the course, the data are one simulated survey: counts of one species at
coastal stations, with the depth, the water temperature, the seabed and the season at
each.

# What a model relies on

## Scene 4
visual: manim Coefficients: a linear model's coefficients beside a forest of many trees with a question mark (schematic)

A linear model shows what it relies on through its coefficients. A random forest
averages hundreds of trees, and has no such numbers to read.

## Scene 5
visual: manim Shuffle: a small table scored, one column shuffled so its values change rows, scored again; the rise in error marked (schematic)

Permutation importance asks from outside. Score the model on test sites. Then shuffle
one input, so its values land on the wrong stations, and score again. The more the
error rises, the more the model relied on that input.

## Scene 6
visual: manim Shuffle: three columns of random numbers join the table as extra inputs (schematic)

But every input gets some score. To see what an unused input scores, add columns of
random numbers as extra inputs. An input that cannot beat them is used no more than
noise.

## Scene 7
visual: manim Impurity: the forest's own importance, thirteen bars, the three random columns in orange above salinity, the seabed and the season (page results, feature-importance.qmd#fig-impurity)

A forest also has a quicker score built in, from its own splits on the training data.
It ranked the three random columns above salinity, the seabed and the season. A
random column offers a tree hundreds of places to split, and some of them fit noise by
chance.

## Scene 8
visual: manim Permutation: permutation importance on one split's test sites, the best random column marked; only temperature and the seabed above it (page results, feature-importance.qmd#fig-permutation)

Permutation importance on test sites does better. But one split holds back only 39
sites, and on it, only temperature and the seabed beat the random columns.

## Scene 9
visual: manim TenSplits: for each input, ten dots, one per split, filled where it beat the random columns; the counts at the right (page results, feature-importance.qmd#fig-ten-splits)

So repeat it on ten splits. Temperature beats the random columns on all ten; depth,
chlorophyll and the seabed on most; salinity on one. That count is the number worth
reporting, not a rank from one split.

## Scene 10
visual: manim Sweep: one input set to each value in turn at every station, the predictions averaged into one curve (schematic)

Importance says how much, but not in which direction. A partial dependence plot shows
the shape: set temperature to one value at every station, predict, average, and repeat
along its range.

## Scene 11
visual: manim Hump: the forest's partial dependence on temperature, then thin curves for many stations behind it, each rising and falling (page results, partial-effects.qmd#fig-ice)

The forest predicts the most animals in cool water, near 7.7 degrees. Drawn station by
station, the curve rises and falls at nearly every one of the 598.

## Scene 12
visual: manim Readable: the GAM's temperature curve with its interval; then RMSE bars on the same folds, the GAM, the forest and the average (page results, black-box-or-not.qmd)

A GAM draws the same hump from its own parts, with an interval. Scored on the same
folds of sites, it predicted new sites as well as the forest: an RMSE of 4.34 against
4.43. On this survey, reading the model cost no accuracy.

## Scene 13
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. Test what a model relies on against random numbers, and on more than
one split.

# How sure a prediction is

## Scene 14
visual: manim TwoIntervals: one station's prediction; a narrow interval for the average and a wide one for a new catch (schematic)

A prediction needs a range, and there are two. They answer different questions.

## Scene 15
visual: manim TwoIntervals: the narrow one labelled "where the average lies", the wide one "where one new catch may land", catches scattering around (schematic)

A confidence interval says where the average catch lies, at stations like this one. A
prediction interval says where one new catch may land, so it adds the scatter of
single catches.

## Scene 16
visual: manim Coverage: catches at new sites dropping onto an interval, counted inside and outside (schematic)

To check an interval, count how many catches at new sites fall inside it. That share
is its coverage.

## Scene 17
visual: manim CoverageBars: the GAM's two intervals, width and coverage at the test sites (page results, communicating-uncertainty.qmd#fig-gam-intervals)

The GAM's interval for the average, 2.5 animals wide, held 20 per cent of the catches
at the test sites. Its interval for a new catch, 11.6 wide, held 96 per cent. Quote
the narrow one as a range for the next catch, and it is wrong four times in five.

## Scene 18
visual: manim Conformal: a forest's errors on calibration sites, sorted; the ninth in ten marked and turned into a half-width either side of a prediction (schematic)

A random forest gives no interval of its own. Conformal prediction makes one: measure
its errors on calibration sites, held back from fitting, and reach as far either side
as nine errors in ten.

## Scene 19
visual: manim Conformal: "held 90% at the test sites", 12.6 animals wide (page results, communicating-uncertainty.qmd)

At the test sites, the forest's interval held 90 per cent of the catches, just as
promised, from a model with no distribution at all.

## Scene 20
visual: manim Shift: calibrated on stations with little chlorophyll, used where it is highest; coverage 90% there, 73% here, the same label and width (page results, communicating-uncertainty.qmd#fig-shift)

Now calibrate it on stations with little chlorophyll, and use it where chlorophyll is
highest. It holds only 73 per cent, under the same label and at the same width.
Nothing in the interval says its promise has lapsed.

## Scene 21
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Name the interval you quote, and check its coverage at new sites.

# What a good score cannot check

## Scene 22
visual: manim Gear: a grab on sand and on rock; on rock, half the animals slip past it (schematic)

A model learns from the records, and the records come from a gear. Grabs and dredges
often catch fewer animals on hard ground.

## Scene 23
visual: manim Gear: the survey's records on rock halved, everything else unchanged; "the same analysis, the same folds" (schematic)

Suppose the survey's gear missed half the animals on rock, and run the whole analysis
again, on the same folds.

## Scene 24
visual: manim Multiplier: rock's multiplier against sand with its interval, as recorded across 1, then with the biased records well below it (page results, from-model-to-claim.qmd)

As recorded, the GAM could not tell rock from sand: its multiplier of 0.80 had an
interval from 0.59 to 1.09, which includes one. With the biased records it is 0.45,
from 0.32 to 0.63, and a study would report half as many animals on rock. The change
is the gear's, not the species'.

## Scene 25
visual: manim Multiplier: the cross-validated RMSE as recorded and with the biased records, the second lower (page results, from-model-to-claim.qmd)

The score did not warn. The cross-validated RMSE improved, from 4.34 to 4.27. Every
fold carries the same bias, so the model matches the records as well as ever.

## Scene 26
visual: manim Outside: three cards, two gears on the same ground, another way of counting (video, divers), the gear and effort reported (schematic)

Checks on the records come from outside the model: fishing the same ground with two
gears, counting the animals another way, with video or divers, and reporting the gear
and the effort.

## Scene 27
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. A score compares the model with the records, never the records with
the sea.

# Quiz

## Scene 28
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A random forest is scored on held-out sites. Which moves its score more:
the seed it is grown with, or which sites happen to be held out?

## Scene 29
visual: manim QuizAnswer: "The sites"; ten RMSEs from ten seeds in a tight cluster, ten from ten splits spread wide, each range marked (page results, reproducibility.qmd#fig-spread)

The sites. Ten seeds moved the forest's RMSE by 0.07; ten splits of the sites moved
it by 1.84, about 27 times as much. A seed makes a run repeat exactly, but it cannot
show how far the score would move with other sites. Cross-validation steadies it.

# Key points

## Scene 30
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: test what a model relies on
against random numbers.

## Scene 31
visual: manim KeyPoints: the second ticked

Two: name the interval, and check its coverage.

## Scene 32
visual: manim KeyPoints: the third ticked

Three: a good score cannot check the records.

## Scene 33
visual: manim EndCard: the site's address and a thank-you

This is the last section of the course. Its pages also cover reading a GAM in words,
making an analysis re-runnable, and writing up the findings, with all the code. They
are linked below. Thanks for watching.
