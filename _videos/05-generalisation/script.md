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
perfect fit on the training stations is a warning sign, the U-shaped error curve comes
from bias and variance, and complexity is chosen by cross-validation with the test
sites opened once. It does not tour every page: the one-standard-error rule and the lasso's list of inputs are left to the
pages. It never says which inputs truly drive the species.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about
generalisation: how well a model does on data it has never seen, which is the reason for
fitting it at all. It covers three things: why a perfect fit is a warning sign, where the
U-shaped error curve comes from, and how to choose a model's complexity honestly.
Complexity is how freely a model can bend to the data.

# A perfect fit is a warning sign

## Scene 2
visual: manim FiveModels: five bars grow, each model's error on its training stations, "error (RMSE): the typical miss, in animals" (page results, underfitting-and-overfitting.qmd#fig-crossing)

Let's start with five models from supervised learning, all fitted to the same simulated
coastal survey: linear regression, two decision trees, a random forest and boosting. The
bars show each model's error on its training stations, the stations it was fitted to.
The error is the typical miss, in animals, from the introduction, so shorter is better.

## Scene 3
visual: manim FiveModels: the grown-out tree's empty bar is highlighted, "0.00"

One of them is perfect. This decision tree kept splitting until every leaf, every final
group, held a single station. So it predicts each training station as that station's own
count, and its error is exactly zero.

## Scene 4
visual: manim FiveModels: an empty column headed "new sites", a question mark in it
pause-after: 1.5

Which one would you trust at sites it has never seen?

## Scene 5
visual: manim FiveModels: the new-site bars grow beside the old ones; the dashed "predict the average" line (page results)

To find out, score them on new sites, held back from fitting, as a stand-in for the
places where the model will be used. The perfect tree comes last, at 6.21 animals. That
is worse than ignoring every input and predicting the average count everywhere, which
misses by 4.83.

## Scene 6
visual: manim Crossing: each model a line from its error on the training stations to its error on new sites; the lines cross (page results, underfitting-and-overfitting.qmd#fig-crossing)

Here, each line joins a model's two errors. The order turns over. Linear regression,
last on its own stations, is close to the best on new ones, behind only the random
forest.

## Scene 7
visual: manim SignalAndNoise: dots, a smooth trend through them labelled "pattern", then the scatter around it labelled "noise" (schematic)

Why? Data hold two things: a pattern and noise. The pattern, such as warmer water
holding more of a species, turns up again at new sites. Noise, the part of a count that
the conditions do not decide, such as one lucky haul, does not.

## Scene 8
visual: manim SignalAndNoise: a fitted straight line through the dots; at one station, "noise" from the pattern to the dot and "residual" from the line to the dot; then every residual drawn; three definitions build up on the right: noise, residual, error (schematic, after loss-functions.qmd)

Three words are easy to mix up here. Noise belongs to the data: how far a count falls from
the pattern, which we never get to see. A residual belongs to a fitted model: how far a
count falls from the model's prediction. Part of it is noise, and the rest is the model's
own mistake. The error rolls many misses into one number, the typical miss, on the
training stations or on new sites.

## Scene 9
visual: manim SignalAndNoise: a zigzag chases every dot while a "training stations" error bar falls to zero and a "new sites" bar stays long (schematic)

A flexible model, one that can bend freely, cannot tell the pattern from the noise.
Fitting the noise lowers its error on its own stations, but not on new ones. The perfect
tree has memorised the noise. This is overfitting.

## Scene 10
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. A perfect fit is a warning sign: the model has memorised the noise, and
its training error cannot tell.

# The U-shaped error curve

## Scene 11
visual: manim UCurve: "minimum node size: the smallest group the tree may split"; the error on the training stations against leaves, falling to zero, then the error on new sites, falling a little and rising; "the U-shaped error curve"; the best tree marked (page results, underfitting-and-overfitting.qmd#fig-sweep)
pause-after: 0.5

Now for the U-shaped error curve. A decision tree's flexibility is set by its minimum
node size: the smallest group of stations it may still split. Sweep it from large to
small, and the tree grows from a few leaves to many. Its error on the training stations
falls all the way to zero. Its error on new sites falls a little, then rises. That is the
U-shaped error curve, and the best tree sits at its lowest point.

## Scene 12
visual: manim UCurve: "underfitting" over the left end, both errors high and close; "overfitting" over the right end, a wide gap

On the left, the tree underfits: it is too rigid to follow the pattern, so both errors
are high and close together. On the right, it overfits: a low error on its own stations,
and a high one on new sites.

## Scene 13
visual: manim Targets: the same model fitted to many surveys, its predictions as dots around a target, "the centre: the expected count"; "bias" the miss of their centre (schematic)

Where does the U come from? Imagine surveying the shelf again and again, and fitting the
same model each time. Each survey gives a slightly different model, and so a slightly
different prediction at one station: the dots on this target. The centre is the
station's expected count, the average it would give if it could be sampled again and
again. Bias is how far the average of the predictions misses the centre.

## Scene 14
visual: manim Targets: a second target, the dots spread wide around the centre; "variance" the spread (schematic)

Variance is how much the predictions change from one survey to the next. A flexible
model follows whichever stations it happened to get, so its predictions spread widely.

## Scene 15
visual: manim Parts: bias² against leaves, "bias²: bias × bias"; the line falls, "few leaves: very different stations share one prediction", then levels off, "a shape trees cannot reach" (page results, bias-variance.qmd#fig-parts)

Because the survey is simulated, every station's expected count is known, so both can be
measured. Bias is squared here, multiplied by itself, so that it can be added to the
variance. A tree with few leaves gives very different stations the same prediction, so
it misses the pattern. More leaves let it follow the pattern, so bias falls. But part of
the pattern has a shape that trees cannot reach on these inputs, however finely they
split, so bias stops falling.

## Scene 16
visual: manim Parts: variance against leaves, rising, "more leaves: fewer stations in each"; then their sum, a U (page results, bias-variance.qmd#fig-parts)

Variance works the other way. A leaf predicts the average count of its stations. More
leaves mean fewer stations in each, and an average of a few counts depends on which
stations a survey happened to catch. So variance keeps rising. Their sum is the U.

## Scene 17
visual: manim Parts: the dashed noise line appears above the best tree's bias² and variance; "noise: 72% of the best tree's error"

Under it all lies noise: chance in the counts, which no model removes. For the best
tree, noise was 72 per cent of the error. That is why even the best tree beat predicting
the average by so little.

## Scene 18
visual: manim TreeAndForest: bias² and variance bars for a single tree and a random forest of the same trees; the forest's variance bar shrinks (page results, bias-variance.qmd)

This is also why a random forest works. Averaging many trees keeps their bias, but cuts
their variance, here about thirteen-fold. Each tree follows its own stations, and their
mistakes partly cancel in the average.

## Scene 19
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. The U-shaped error curve comes from bias falling and variance rising as
a model gets more flexible.

# Choosing complexity honestly

## Scene 20
visual: manim Penalty: a linear model's coefficients as bars; a slider for λ, the penalty's weight; as it rises, the bars shrink towards zero; "λ = 0: no penalty", "larger λ: more rigid"; a brace under "λ × (size of the coefficients)", "the regularisation term: controls complexity" (schematic)

Finally, how to choose complexity honestly. A linear model has its own dial: a penalty,
which we met in the last video. The fit is charged for large coefficients, so it keeps
them small unless the data clearly need them. A weight called lambda sets how hard the
penalty pulls. At zero there is no penalty, and the larger it is, the more rigid the
model. Lambda times the size of the coefficients is called the regularisation term: it
is what controls the model's complexity.

## Scene 21
visual: manim TwoPenalties: two panels; "ridge regression: charges the squared coefficients", every bar shrinks and none reaches zero; "the lasso: charges their absolute size", the small bars drop to exactly zero (schematic)

There are two common penalties. Ridge regression charges the squared coefficients, so it
shrinks every one but removes none. The lasso charges their absolute size, the size
without its sign, which makes a small coefficient cheaper to drop than to keep. It sets
those to exactly zero, and their inputs leave the model.

## Scene 22
visual: manim LambdaCurve: "a regression with 200 random columns"; error on new sites against λ for ridge regression and the lasso, with lines for linear regression on all inputs and on the measured inputs only (page results, regularisation.qmd#fig-sweep)

Here is a test. Give a linear regression 200 extra columns of random numbers: inputs that
carry no information at all. Its error on new sites rises to 6.41, worse than predicting
the average. This chart follows the error as lambda grows. The lasso, at its best lambda,
scores 4.55: as good as a regression told which inputs were measured.

## Scene 23
visual: manim Settings: "node size" and "penalty λ" as two dials, "hyperparameters: fixed before fitting"; the training error always favours the most flexible end (schematic)

A node size, a penalty: every method has a setting like this, a hyperparameter, fixed
before fitting. It has to be chosen, and not by the training error, which always favours
the most flexible setting.

## Scene 24
visual: manim Folds: the training sites dealt into ten folds, "a fold: a group of whole sites"; each fold lights up in turn as new data while the rest are fitted; the ten errors averaged; "for each setting: keep the lowest average" (schematic)

Instead, it is chosen by cross-validation. Deal the training sites into ten groups,
called folds. Each fold holds whole sites, because visits to one site resemble each
other. Each fold takes a turn as new data while the model is fitted to the other nine,
and the ten errors are averaged. Do this for every setting, and keep the one with the
lowest average.

## Scene 25
visual: manim Repeats: twenty runs of cross-validation as dots, the error each claimed for its winner, in a narrow band; then twenty runs of one held-back group, spread wide (page results, hyperparameter-selection.qmd#fig-repeats)

Because every training site takes a turn, the verdict is steady. Run 20 times with
different folds, the error it claimed for its winning setting stayed between 4.45 and
4.64. Holding back a single group of sites instead gave anything from 3.72 to 5.37.

## Scene 26
visual: manim TestOnce: a sealed box of test sites opened once; the tree against predicting the average, 0.28 better, beside the 0.26 cross-validation promised (page results, hyperparameter-selection.qmd)

Last, the test sites, held back since the very start, score the chosen tree once. It
beats predicting the average by 0.28, close to the 0.26 that cross-validation promised.

## Scene 27
visual: manim TestOnce: the box marked "spent"; choosing again turns test sites into validation sites (schematic)

Then the test sites are spent. Choose again because the score disappointed, and they
become validation sites, which can no longer give an honest score.

## Scene 28
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. Choose complexity honestly: use cross-validation on the training data,
and open the test set only once.

# Quiz

## Scene 29
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. R squared is the share of the variation in the counts that a model
explains. A colleague adds ten new columns to a linear regression, and its R squared on
the training stations goes up. Does that show the new columns help?

## Scene 30
visual: manim QuizAnswer: "No"; R² on the training stations rising with columns of random numbers, the error on new sites rising too (page results, regularisation.qmd#fig-noise)

No. R squared on the training stations never falls when a column is added, even a column
of random numbers. On the survey, ten random columns raised it, and raised the error on
new sites from 4.56 to 4.66. Only new sites can tell.

# Key points

## Scene 31
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: a perfect fit is a warning sign.

## Scene 32
visual: manim KeyPoints: the second ticked

Two: the U-shaped error curve comes from bias and variance.

## Scene 33
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: choose complexity with cross-validation, and open the test set once.

## Scene 34
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
