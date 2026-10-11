---
title: "Generalisation: why a perfect fit is a bad sign"
section: chapters/05-generalisation/index.qmd
voice: Sadaltager
style: "friendly British English, speaking at a natural, conversational pace"
gap: 1.0
---

<!--
Script conventions (read by tools/narrate.py and tools/rough-cut.py):

- The video opens with the series title and jingle (the Title scene in scenes.py and
  _videos/intro-music.wav); the script starts after it.
- A level-1 heading starts a YouTube chapter; its text becomes the chapter title.
- A level-2 heading starts a scene. Everything after the directive lines is narration.
- One idea per scene: one or two short sentences, few numbers.
- Directive lines, directly under the scene heading:
    visual: manim <SceneName>: <what>   an animation in scenes.py; "page results" means
                                        R writes the numbers the page computed to a CSV,
                                        "schematic" means drawn shapes with no numbers
    visual: figure <page>.qmd#<label>   a chapter figure, re-exported by figures-for-video.R
    visual: card: <text>                a plain text card; "card: Heading | text" puts a
                                        small heading above the text
    pause-after: <seconds>              silence added after the narration
    cheer: 1 | 2 | 3 | all              after the narration, the key point's animal pops up
                                        with its sound; "all" brings all three, after the
                                        recap. Give it pause-after: 2.0 (all: 4.0)
- gap in the front matter is the silence between scenes, in seconds.
- Every number spoken comes from the section's pages.
- No section numbers anywhere in the video, spoken or shown: they can change, so they
  go only in the YouTube title and description. Refer to other sections by name.

This video is an overview built on three ideas, each with the reason it matters: a
perfect fit on the fitting stations is a warning sign, the U-shaped error curve comes
from bias and variance, and complexity is chosen by cross-validation with the test
sites opened once. It does not tour every page: the one-standard-error rule and the lasso's list of inputs are left to the
pages. It never says which inputs truly drive the species.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. Why a perfect fit is a warning sign.
Where the U-shaped error curve comes from. And how to choose a model's complexity
honestly.

# A perfect fit is a warning sign

## Scene 2
visual: manim FiveModels: five bars grow, each model's error on its fitting stations (page results, underfitting-and-overfitting.qmd#fig-crossing)

Here are five models from earlier in the course, fitted to the same simulated coastal
survey. The bars show each model's error on the stations it was fitted to.

## Scene 3
visual: manim FiveModels: the grown-out tree's empty bar is highlighted, "0.00"

One of them is perfect. A decision tree, grown until every leaf holds a single
station, has an error of exactly zero.

## Scene 4
visual: manim FiveModels: an empty column headed "new sites", a question mark in it
pause-after: 1.5

Which one would you trust at sites it has never seen?

## Scene 5
visual: manim FiveModels: the new-site bars grow beside the old ones; the dashed "predict the average" line (page results)

So score them on new sites, held back from fitting. The perfect tree comes last, at
6.21. That is worse than ignoring every input and predicting the average count, 4.83.

## Scene 6
visual: manim Crossing: each model a line from its error on the fitting stations to its error on new sites; the lines cross (page results, underfitting-and-overfitting.qmd#fig-crossing)

The order turns over. Linear regression, last on its own stations, is close to the
best on new ones.

## Scene 7
visual: manim SignalAndNoise: dots, a smooth trend through them labelled "pattern", then the scatter around it labelled "noise" (schematic)

Why? Data hold a pattern and noise. The pattern, such as warmer water holding more of a
species, turns up again at new sites. Noise, such as one lucky haul, does not.

## Scene 8
visual: manim SignalAndNoise: a zigzag chases every dot while a "fitting stations" error bar falls to zero and a "new sites" bar stays long (schematic)

A flexible model cannot tell the two apart. Fitting the noise lowers its error on its
own stations, but not on new ones. The perfect tree has memorised the noise.

## Scene 9
visual: manim SiteSplit: sites on a map split into fitting sites and new sites, whole sites on each side (schematic)

So a model is always judged on data it was not fitted to. And the split is made by
site, so that new sites really are new.

## Scene 10
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. A perfect fit is a warning sign: the model has memorised the noise, and
training error cannot tell.

# The U-shaped error curve

## Scene 11
visual: manim NodeSize: a group of stations that may split in two only if it holds enough of them; "minimum node size" (schematic)

How flexible should a model be? For a decision tree, one setting decides: the minimum
node size, the smallest group of stations the tree may split in two.

## Scene 12
visual: manim ThreeTrees: abundance against temperature, the trees with node sizes 300, 50 and 2 drawn in turn, with their leaf counts (page results, underfitting-and-overfitting.qmd#fig-one-input)

Here are three trees with temperature as their only input. A node size of 300 gives
four leaves. A size of 50 gives twenty. A size of 2 gives 414, jumping up to meet
nearly every large catch.

## Scene 13
visual: manim UCurve: the error on the fitting stations against leaves, drawn from rigid to flexible, falling to zero (page results, underfitting-and-overfitting.qmd#fig-sweep)

Now sweep the setting from rigid to flexible, with all six inputs. The error on the
fitting stations falls all the way to zero.

## Scene 14
visual: manim UCurve: the error on new sites drawn, falling a little and then rising; "the U-shaped error curve"
pause-after: 0.5

The error on new sites falls a little, then rises. This is the U-shaped error curve.

## Scene 15
visual: manim UCurve: "underfitting" over the left end, both errors high and close; "overfitting" over the right end, a wide gap

On the left, the tree underfits: both errors are high and close together. On the
right, it overfits: a low error on its own stations, and a high one on new sites.

## Scene 16
visual: manim Targets: the same model fitted to many surveys, its predictions as dots around a target; "bias" the miss of their centre (schematic)

Where does the U come from? Imagine surveying the shelf again and again, and fitting
the same model each time. Bias is how far the average of those models misses.

## Scene 17
visual: manim Targets: a second target, the dots spread wide around the centre; "variance" the spread (schematic)

Variance is how much the model changes from one survey to the next.

## Scene 18
visual: manim Parts: bias² and variance against leaves, then their sum, a U (page results, bias-variance.qmd#fig-parts)

Because the survey is simulated, the true expected counts are known, so both can be
measured. As the tree grows, bias falls and then stops. Variance keeps rising. Their
sum is the U.

## Scene 19
visual: manim Parts: the dashed noise line appears above the best tree's bias² and variance; "noise: 72% of the best tree's error"

Under it all lies noise: chance in the counts, which no model removes. For the best
tree, noise was 72 per cent of the error.

## Scene 20
visual: manim TreeAndForest: bias² and variance bars for a single tree and a random forest of the same trees; the forest's variance bar shrinks (page results, bias-variance.qmd)

This is why a random forest works. Averaging many trees keeps their bias, but cuts
their variance, here about thirteen-fold.

## Scene 21
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. The U-shaped error curve comes from bias falling and variance rising as
a model gets more flexible.

# Choosing complexity honestly

## Scene 22
visual: manim Penalty: a linear model's coefficients as bars; a slider for λ, the penalty's weight; as it rises, the bars shrink towards zero (schematic)

A linear model has its own dial: a penalty. The fit is charged for large coefficients,
so it keeps them small unless the data clearly need them. A weight called lambda sets how
hard the penalty pulls.

## Scene 23
visual: manim TwoPenalties: two panels; "ridge regression: charges the squared coefficients", every bar shrinks and none reaches zero; "the lasso: charges their absolute size", the small bars drop to exactly zero (schematic)

There are two common penalties. Ridge regression charges the squared coefficients, so it
shrinks every one but removes none. The lasso charges their absolute size, which makes a
small coefficient cheaper to drop than to keep. It sets those to exactly zero, and their
inputs leave the model.

## Scene 24
visual: manim LambdaCurve: error on new sites against λ for ridge regression and the lasso, with lines for linear regression on all inputs and on the measured inputs only (page results, regularisation.qmd#fig-sweep)

Give a regression 200 columns of random numbers, and its error on new sites is 6.41.
The lasso, at its best penalty, scores 4.55: as good as being told which inputs were
real.

## Scene 25
visual: manim Settings: "node size" and "penalty λ" as two dials; the training error always favours the most flexible end (schematic)

A node size, a penalty: every method has a setting like this, and it has to be chosen.
Not by training error, which always favours the most flexible.

## Scene 26
visual: manim Repeats: twenty runs of one validation split as dots, the error each claimed for its winner, spread wide (page results, hyperparameter-selection.qmd#fig-repeats)

The simplest way is one validation split: hold back some sites and compare settings on
them. But it depends on which sites were held back. In 20 repeats, the error it claimed
ranged from 3.72 to 5.37.

## Scene 27
visual: manim Folds: the training sites dealt into ten folds; each fold lights up in turn as new data while the rest are fitted (schematic)

Cross-validation does better. Deal the training sites into ten folds. Each fold takes a
turn as new data while the model is fitted to the rest, and the ten errors are averaged.

## Scene 28
visual: manim Repeats: the twenty cross-validation dots added below, in a narrow band (page results)

Every training site counts, so the verdict is steadier: in 20 repeats, from 4.45 to
4.64.

## Scene 29
visual: manim TestOnce: a sealed box of test sites opened once; the tree against predicting the average, 0.28 better, beside the 0.26 cross-validation promised (page results, hyperparameter-selection.qmd)

Last, the test sites, held back since the start, are scored once. The chosen tree beats
predicting the average by 0.28, close to the 0.26 that cross-validation promised.

## Scene 30
visual: manim TestOnce: the box marked "spent"; choosing again turns test sites into validation sites (schematic)

Then the test sites are spent. Choose again because the score disappointed, and they
can no longer give an honest one.

## Scene 31
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Choose complexity honestly: use cross-validation on the training data,
and open the test set only once.

# Quiz

## Scene 32
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A colleague adds ten new columns to a regression, and its R squared on the
fitting stations goes up. Does that show the new columns help?

## Scene 33
visual: manim QuizAnswer: "No"; R² on the fitting stations rising with columns of random numbers, the error on new sites rising too (page results, regularisation.qmd#fig-noise)

No. R squared on the fitting stations never falls when a column is added, even a column
of random numbers. On the survey, ten random columns raised it, and raised the error on
new sites from 4.56 to 4.66. Only new sites can tell.

# Key points

## Scene 34
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: a perfect fit is a warning sign.

## Scene 35
visual: manim KeyPoints: the second ticked

Two: the U-shaped error curve comes from bias and variance.

## Scene 36
visual: manim KeyPoints: the third ticked

Three: choose complexity with cross-validation, and open the test set once.

## Scene 37
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
