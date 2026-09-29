---
title: "Interpretation: what can a model honestly tell you?"
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
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. How to tell which predictors a model
really relies on. Why even the right model can draw the wrong shape. And what no model
can warn you about.

# The puzzle

## Scene 2
visual: manim Truth: the true depth effect, a hump peaking at 80 m (page results, partial-effects.qmd)

Here is a survey of 720 stations. It is simulated, so we know the truth: abundance
peaks at 80 metres depth.

## Scene 3
visual: manim Truth: the random forest's partial dependence added, falling from 5.04 to 3.77

Fit a random forest and ask it about depth. It says abundance falls with depth, from
5.04 to 3.77.

## Scene 4
visual: manim Truth: "the generator's own formula" card over the chart (schematic)

So blame the black box. Fit the exactly right model instead: a regression given the
formula that made the data.

## Scene 5
visual: manim Truth: the GLM's curve added, falling from 8.19 to 1.80, and a question mark
pause-after: 1.5

It tells the same story, only steeper: 8.19 falling to 1.80. Two models, one wrong
shape. Why?

# What the model relies on

## Scene 6
visual: manim Importance: a schematic bar chart titled "so what drives it?" (schematic)

Start with the question everyone asks: so what drives it? The usual answer is an
importance plot.

## Scene 7
visual: manim Noise: three columns of random numbers added to the table (schematic)

First, we add three columns of random numbers. They cannot possibly matter.

## Scene 8
visual: manim Impurity: the default importance for sixteen terms, the three noise columns at six, seven and eight (page results, feature-importance.qmd)

The default importance ranks them sixth, seventh and eighth of sixteen.

## Scene 9
visual: manim Impurity: salinity and every substrate term highlighted below them

Above salinity, and above every substrate term. And substrate has a real effect.

## Scene 10
visual: manim Splits: a measured column with hundreds of split points, a yes-or-no column with one (schematic)

A measured column offers hundreds of places to split. A yes-or-no column offers one.
Among hundreds, chance alone finds one that helps a little.

## Scene 11
visual: manim Shuffle: one column shuffled, the error rising (schematic)

Permutation importance asks a better question. Shuffle one column: how much worse does
the model predict?

## Scene 12
visual: manim Permutation: the increase in error for each variable, the noise columns' band shaded (page results, feature-importance.qmd#fig-importance)

Now the random columns mark a band: what nothing looks like. Temperature, latitude,
longitude, substrate and depth clear it.

## Scene 13
visual: manim Ranks: each variable's best and worst rank over eight splits, chlorophyll from 1 to 11 (page results)

But one split is not a result. Over eight splits, chlorophyll ranked first in one and
eleventh in another.

## Scene 14
visual: manim Seeds: test error over eight forest seeds, piled together, and over eight splits, spread out (page results, reproducibility.qmd#fig-seeds)

Even the forest's random seed matters little next to the split. Changing the seed moved
the test error by 0.016. Changing the split moved it by 1.50.

## Scene 15
visual: manim Counts: how many of eight splits each variable beats the random columns, salinity and survey year at zero

What stays steady is a count. Salinity and survey year beat the random columns in none
of the eight splits. They are the two with no effect.

## Scene 16
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. Always add a null. Report how often each variable beats random numbers,
not its rank.

# The puzzle, solved

## Scene 17
visual: manim Sweep: every station set to one depth, the predictions averaged, then the next depth (schematic)

Back to depth. A partial dependence plot sets every station to one depth, averages the
predictions, and moves along.

## Scene 18
visual: manim Temperature: the true curve and the forest's, peaks at 9 and 7.75 °C (page results, partial-effects.qmd)

For temperature, it works. The forest's peak is at 7.75 degrees, against a true 9.

## Scene 19
visual: manim Stations: every station's depth against temperature, the empty corners marked (page results)

Depth fails because of how the survey was taken. There are almost no cold shallow
stations, and almost no warm deep ones.

## Scene 20
visual: manim Stations: "depth" and "temperature" arrows pointing the same way, "cannot be separated"

So the data cannot separate the two humps. Temperature takes the shared part, and depth
is left with a decline.

## Scene 21
visual: manim Terms: the GLM's depth term against its true size, a fourteenth, p = 0.63 (page results)

The right formula cannot help. Its depth term came back at a fourteenth of its true
size, with a p value of 0.63.

## Scene 22
visual: manim Fix: "a different plot" struck out, "a different survey" ticked
pause-after: 0.5

No plot can fix that. The fix is a different survey.

## Scene 23
visual: manim Scores: seven models' cross-validated error on the same folds, the GAM best (page results, black-box-or-not.qmd)

Now try a GAM, a model of smooth curves you can read. On the same folds, it was the
most accurate of seven: 4.08, against the forest's 4.28.

## Scene 24
visual: manim GAM: its depth curve, peaking at 52 m, with its interval, against the truth (page results, black-box-or-not.qmd#fig-smooths)

Its depth curve is wrong too, peaking at 52 metres. But it comes with an interval.

## Scene 25
visual: manim GAM: "covers the truth at 197 of 200 points", "a wide answer, not a wrong one"

That interval covers the true curve at 197 of 200 points. It is not a wrong answer. It
is a wide one.

## Scene 26
visual: manim GAM: "I don't know" beside the GAM, nothing beside the partial dependence plot
pause-after: 0.5

The GAM says it does not know. A partial dependence plot has no way to say that.

## Scene 27
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. No method recovers an effect the data cannot separate. Report the
confounding instead.

# What no model can warn you about

## Scene 28
visual: manim Intervals: observed counts against the GAM's expected count (page results, communicating-uncertainty.qmd#fig-intervals)

Every prediction needs an interval. But there are two kinds, and they answer different
questions.

## Scene 29
visual: manim Intervals: the confidence band on the mean, covering 29%

The band a GAM gives you is for the average count. It covers 29% of the observed
counts.

## Scene 30
visual: manim Intervals: the prediction interval for a new count, covering 99%

The interval for a new count is three times wider, and covers 99%.

## Scene 31
visual: manim Coverage: the forest's interval from its training error, 77%, and the two errors, 2.11 and 4.17 (page results)

A forest has no distribution. Build its interval from the training error, and it covers
77%: that error is 2.11, against an honest 4.17.

## Scene 32
visual: manim Coverage: conformal prediction, 96.5%, the nominal 95% line

Conformal prediction sizes the interval on stations the model never saw. It covers
96.5%, whatever the model.

## Scene 33
visual: manim Shift: calibrated on low chlorophyll, used on high, coverage 86%, the same width (page results)

But only for stations like those. Calibrate it on low chlorophyll, use it on high, and
it covers 86%. Same width. No warning.

## Scene 34
visual: manim Gear: a grab on rock bringing up half the animals (schematic)

One last error. Suppose the gear catches only half the animals on rock.

## Scene 35
visual: manim Rock: the estimated rock effect, 38% fewer than gravel, then 69% fewer (page results, from-model-to-claim.qmd)

The estimated rock effect more than doubles: from 38% fewer animals than gravel to 69%
fewer.

## Scene 36
visual: manim Rock: cross-validated error, 4.079 as recorded, 4.008 with the biased gear

And the cross-validated error improves, from 4.079 to 4.008.

## Scene 37
visual: manim Defences: "every check passes", then the defences outside the model
pause-after: 0.5

Validation compares the model with the data. When the data are biased, every check
passes. The defences are outside the model: calibrate the gear, and use an independent
method.

## Scene 38
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. A model cannot see what its data do not contain. Measure each
interval's coverage, and know how your data were collected.

# Quiz

## Scene 39
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Two columns carry exactly the same information: depth, recorded twice.
What does permutation importance say about each?

## Scene 40
visual: manim QuizAnswer: two depth columns, each shuffled while the other stands in (schematic)

Both near zero. Shuffle one, and the model reads the other. Low importance means
redundant, not unimportant.

# Key points

## Scene 41
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: importance needs a null.

## Scene 42
visual: manim KeyPoints: the second ticked

Two: the data must separate the effects.

## Scene 43
visual: manim KeyPoints: the third ticked

Three: a model cannot see what its data lack.

## Scene 44
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
