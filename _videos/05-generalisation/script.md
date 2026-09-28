---
title: "Generalisation: why a perfect fit is a bad sign"
section: chapters/05-generalisation/index.qmd
voice: Sadaltager
style: "friendly British English, speaking at a natural, conversational pace"
---

<!--
Script conventions (read by tools/narrate.py and tools/rough-cut.py):

- A level-1 heading starts a YouTube chapter; its text becomes the chapter title.
- A level-2 heading starts a scene. Everything after the directive lines is narration.
- Directive lines, directly under the scene heading:
    visual: figure <page>.qmd#<label>   a chapter figure, re-exported by figures-for-video.R
    visual: manim <SceneName>: <what>   an animation in scenes.py; "real data" means R
                                        writes the numbers to a CSV, "schematic" means
                                        made-up shapes that must not look like results
    visual: card: <text>                a plain text card; "card: Heading | text" puts a
                                        small heading above the text
    pause-after: <seconds>              silence added after the narration
- Every number spoken comes from the section's pages. The page is named in a
  comment where a number is not obvious from the visual.
-->

# The puzzle

## Scene 1
visual: manim FiveModelsTraining: five horizontal bars, training RMSE only, test column hidden (real data, training-versus-new-data.qmd)

Here are five models, all fitted to the same coastal survey. This is the error each one
makes on the stations it was trained on. And one of them is perfect: an error of exactly
zero.

## Scene 2
visual: manim FiveModelsTraining: the zero bar pulses, a question mark appears
pause-after: 1.5

Which one would you trust with next year's survey? <short pause> Hold on to your
answer.

## Scene 3
visual: card: 5 · Generalisation and model complexity

This is section five of Machine Learning Basics for Marine Science. It is about
generalisation: how well a model does on data it has never seen.

## Scene 4
visual: card: The coastal survey is simulated, so we know the true answer.

One thing first. The survey in this course is simulated, not real. That is deliberate:
because we wrote the process that made it, we know the true answer, and we can check
whether a model finds it.

# Training error answers the wrong question

## Scene 5
visual: manim RankReversal: slope chart, the test side draws in line by line (real data, training-versus-new-data.qmd#fig-crossing)

Now let's give the five models stations they have never seen. Every line goes up,
because new data is always harder. But look at the order.

## Scene 6
visual: manim RankReversal: the two rankings side by side, arrows showing the exact reversal

Ranked by training error and ranked by error on new stations, the list is exactly
reversed. The model you would have picked is the worst of the five.

## Scene 7
visual: manim RankReversal: the fully grown tree highlighted against the dashed "predict the mean" line

That perfect tree scores 6.9 on new stations. Ignoring every predictor and just guessing
the average scores 5.3. It has not learned a relationship. It has memorised the survey.

## Scene 8
visual: manim SignalAndNoise: a scatter separates into a smooth trend and the scatter around it (schematic)

Every survey holds two things. Signal is the structure that will turn up again next
year. Noise is what belongs only to these stations, on these days, with this net.

## Scene 9
visual: manim SignalAndNoise: a wiggly curve chases the noise while a training-error counter falls

Training error cannot tell them apart: fitting the noise lowers it just as well as
fitting the signal. So it is not an estimate of anything you care about.

# The U-shaped curve

## Scene 10
visual: figure underfitting-and-overfitting.qmd#fig-three-fits (left panel first)

Here is abundance against depth, with a regression tree of growing flexibility. With a
single split, it can only say shallow or deep. That is underfitting: too rigid to hold
the pattern.

## Scene 11
visual: figure underfitting-and-overfitting.qmd#fig-three-fits (centre, then right panel)

With nine leaves, it follows the decline with depth. With one station per leaf, it
passes through almost every point. That is overfitting: it has recorded the survey
instead of learning from it.

## Scene 12
visual: manim UCurve: training curve draws from left to right down to zero (real data, underfitting-and-overfitting.qmd#fig-u-curve)

Now sweep the flexibility of a tree on all the predictors. As it grows, training error
falls, smoothly, all the way to zero.

## Scene 13
visual: manim UCurve: test curve draws, dotted line drops at 16 leaves

Error on new stations does something else. It falls, bottoms out at sixteen leaves, and
climbs again. This U shape is the single most important picture in this course.

## Scene 14
visual: manim UCurve: the test curve crosses the dashed baseline, the training curve keeps falling

Somewhere between 62 and 85 leaves, the tree becomes worse than using no predictors at
all. And training error gives no warning: it keeps falling straight through.

## Scene 15
visual: manim Diagnosis: two small bar pairs, "both poor, about equal" and "good, then much worse"

So you diagnose a model from both errors together. Both poor and about equal is
underfitting. Good on training data and much worse on new data is overfitting. The gap
is the tell.

# Complexity is not a count of parameters

## Scene 16
visual: manim NoiseColumns: a data table grows columns of random digits to the right (schematic)

How flexible is too flexible? Here is an experiment. Take three real predictors, and
add columns of pure random numbers, known to contain nothing at all.

## Scene 17
visual: manim NoiseColumns: training R² gauge climbs to 1.000 as columns are added (real data, model-complexity.qmd#fig-noise)

With 539 columns of noise on 540 stations, the model reports a perfect fit. Training R²
is exactly one.

## Scene 18
visual: manim NoiseColumns: test RMSE shoots up to 185, next to a marker at 40 for the largest catch

On new stations, its error is 185, for a survey whose largest catch is 40. The fit was
perfect because the model ran out of data to be wrong about.

## Scene 19
visual: card: R² never falls when you add a predictor.

R² never falls when you add a predictor, however useless. What matters is how flexible
the model is compared with how much data you have.

# Bias, variance and the noise floor

## Scene 20
visual: manim Targets: a target with a true value at the centre, empty (schematic)

Why is the curve U-shaped? Imagine repeating the survey many times and fitting the same
kind of model to each one. Two different things can go wrong.

## Scene 21
visual: manim Targets: a tight cluster of hits, all off to one side (schematic)

Bias is being wrong in the same direction every time, like a thermometer that always
reads high. A thousand casts will not find it.

## Scene 22
visual: manim Targets: hits centred on the truth but widely scattered (schematic)

Variance is being unstable: right on average, but different every time. A deep tree is
like this. Two surveys of the same shelf give two quite different trees.

## Scene 23
visual: figure bias-variance.qmd#fig-decomposition (bias² and variance lines first)

More flexibility trades one for the other. On our survey, bias fell by 42 per cent and
then stopped. Variance rose by a factor of nearly four hundred. Their sum is the U.

## Scene 24
visual: figure bias-variance.qmd#fig-decomposition (the dashed irreducible line highlighted)

And underneath sits a floor. Part of every count was never a function of the
environment. Here that irreducible noise is more than double everything a model could
control.

## Scene 25
visual: card: Most of the error in marine count data is not model error.

That is why marine habitat models so often have unimpressive R² values. It is a
property of counting animals, not a failure of the analysis.

# Regularisation

## Scene 26
visual: manim RidgeShrink: coefficient bars shrink towards zero as a λ slider rises (schematic)

Regularisation accepts a slightly worse fit for a steadier model. The model pays a
price for large coefficients, so they shrink towards zero.

## Scene 27
visual: manim RidgeBars: three bars, least squares 7.41, predict the mean 4.80, ridge 4.64 (real data, regularisation.qmd)

With 44 predictors on 120 stations, ordinary least squares scored 7.41, worse than
guessing the mean. Ridge scored 4.64.

## Scene 28
visual: figure regularisation.qmd#fig-stability

Lasso also drops variables, but not reliably. Over a hundred resamples, real predictors
survived about 25 per cent of the time, and pure noise about 18.

# The trap

## Scene 29
visual: manim PeekAtTest: a sealed box labelled "test set" is opened again and again (schematic)

Now the trap. Every result so far chose its setting, the number of leaves or the size of
the penalty, by looking at the test set. The pages say so each time.

## Scene 30
visual: manim PeekAtTest: the box's label changes from "test set" to "training set, again"

That is cheating. Look at the test set, pick the winner, adjust, and look again, and it
has quietly become a second training set. Its score is no longer honest.

## Scene 31
visual: manim CrossValidation: ten folds, the held-out fold rotating; the test box stays sealed until the end (schematic)

The honest way is cross-validation. Split the training data into ten folds. Fit on
nine, score on the tenth, and rotate, so every station is scored by a model that never
saw it. The test set is used once, at the very end.

## Scene 32
visual: figure hyperparameter-selection.qmd#fig-instability

Even then, be modest. Forty single validation splits of the same data chose sixteen
different winners. When settings tie, prefer the simplest one within one standard error
of the best.

## Scene 33
visual: manim RepeatVisits: 160 site markers, each with a stack of repeat visits split between training and test (schematic)

One more catch. These stations come from 160 sites visited again and again, so a random
split puts the same site on both sides, and flatters every number here. Section seven
puts that right.

# Quiz

## Scene 34
visual: card: Quiz | You add a column of random numbers to a regression. Can its training R² go down?
pause-after: 10

Quick quiz. You add a column of random numbers to a regression. Can its training R² go
down?

## Scene 35
visual: card: Answer | No. R² never falls when a predictor is added.

No. It rises every time, even with random numbers, so it cannot tell you whether a
variable matters.

# Key points

## Scene 36
visual: card: Key points | Training error measures memory, not how a model does on new data.

To sum up. Training error tells you how well a model remembers its data, not how it
will do on new data.

## Scene 37
visual: card: Key points | Error on new data is U-shaped in flexibility. The gap between the two errors tells underfitting from overfitting.

Error on new data against flexibility is U-shaped. Too rigid underfits, too flexible
overfits, and the gap between the two errors tells them apart.

## Scene 38
visual: card: Key points | Much of the error in marine counts is noise. Regularisation trades a little bias for a lot of stability.

Much of the error in marine count data is noise no model can remove. Regularisation
trades a little bias for a lot of stability.

## Scene 39
visual: card: Key points | Choose settings with cross-validation. Spend the test set once.

Choose settings with cross-validation, and spend the test set once.

## Scene 40
visual: card: Pages and code | hi-digital-ml-ai.github.io/ml-basic/chapters/05-generalisation

The pages for this section, with all the R and Python code, are linked below. Thanks
for watching.
