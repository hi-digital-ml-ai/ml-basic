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
- One idea per scene: one or two short sentences, at most one number.
- Directive lines, directly under the scene heading:
    visual: manim <SceneName>: <what>   an animation in scenes.py; "real data" means R
                                        writes the numbers to a CSV, "schematic" means
                                        made-up shapes that must not look like results
    visual: figure <page>.qmd#<label>   a chapter figure, re-exported by figures-for-video.R
    visual: card: <text>                a plain text card; "card: Heading | text" puts a
                                        small heading above the text
    pause-after: <seconds>              silence added after the narration
- gap in the front matter is the silence between scenes, in seconds.
- Every number spoken comes from the section's pages.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video: why a perfect fit is a warning sign, where the U-shaped error curve comes
from, and how to choose a model's complexity honestly.

# The puzzle

## Scene 2
visual: manim FiveModels: five bars grow, training error only (real data, training-versus-new-data.qmd)

Here are five models, fitted to the same coastal survey. The bars show their error on
the stations they learned from.

## Scene 3
visual: manim FiveModels: the zero bar is highlighted

One of them is perfect: an error of exactly zero.

## Scene 4
visual: manim FiveModels: a question mark appears in the hidden column
pause-after: 1.5

Which one would you trust with next year's survey?

## Scene 5
visual: manim Simulated: a "true process" box sends dots to a map of stations (schematic)

A note first: this survey is simulated. We wrote the process that made it, so we know
the true answer.

# Training error answers the wrong question

## Scene 6
visual: manim RankReversal: the slope chart's axes, training errors on the left (real data)

Now give the five models stations they have never seen.

## Scene 7
visual: manim RankReversal: the lines draw to the new-station errors

Every error goes up. New data is always harder. But look at the order.

## Scene 8
visual: manim Rankings: two ranked lists with arrows between them

Ranked by training error, and ranked on new stations, the order is exactly reversed.

## Scene 9
visual: manim Rankings: the grown-out tree circled at the top of one list and the bottom of the other

The model you would have picked is the worst of the five.

## Scene 10
visual: manim RankReversal: the grown-out tree highlighted, its error labelled

That perfect tree scores 6.9 on new stations.

## Scene 11
visual: manim RankReversal: the dashed "predict the mean" line appears

Just guessing the average scores 5.3. The tree has not learned. It has memorised.

## Scene 12
visual: manim SignalAndNoise: dots, then a smooth trend through them (schematic)

Every survey holds two things. Signal is the pattern that turns up again next year.

## Scene 13
visual: manim SignalAndNoise: the scatter around the trend is drawn

Noise is what belongs only to these stations, on these days, with this net.

## Scene 14
visual: manim SignalAndNoise: a wiggly curve chases the dots while a training-error bar falls to zero

Training error cannot tell them apart. Chasing the noise lowers it just as well.

# The U-shaped curve

## Scene 15
visual: manim ThreeFits: abundance against depth, a tree with one split (real data, underfitting-and-overfitting.qmd#fig-three-fits)

Here is a tree fitted to abundance and depth. With one split, it is too rigid. That is
underfitting.

## Scene 16
visual: manim ThreeFits: the tree grows to nine leaves

With nine leaves, it follows the decline with depth.

## Scene 17
visual: manim ThreeFits: the tree grows to one station per leaf

With one station per leaf, it chases every point. That is overfitting.

## Scene 18
visual: manim UCurve: the training curve draws down to zero (real data, underfitting-and-overfitting.qmd#fig-u-curve)

Now make a tree more and more flexible. Its training error falls, all the way to zero.

## Scene 19
visual: manim UCurve: the new-station curve draws, the best point marked

Its error on new stations falls, bottoms out at sixteen leaves, then climbs.

## Scene 20
visual: manim UCurve: the U is traced and highlighted

This U shape is the curve this whole section is about.

## Scene 21
visual: manim UCurve: the "predict the mean" line and the band where the curve crosses it

Between 62 and 85 leaves, the tree becomes worse than using no predictors at all.

## Scene 22
visual: manim UCurve: a flash runs down the training curve

And training error gives no warning. It keeps on falling.

## Scene 23
visual: manim Diagnosis: two bars, both poor and about equal (schematic)

So read both errors together. Both poor, and about equal: that is underfitting.

## Scene 24
visual: manim Diagnosis: a short bar and a tall one, the gap marked

Good on training data, much worse on new data: overfitting. The gap is the tell.

# Complexity is not a count of parameters

## Scene 25
visual: manim NoiseColumns: a data table grows columns of random numbers (schematic)

How flexible is too flexible? Take three real predictors, and add columns of pure
random numbers.

## Scene 26
visual: manim NoiseColumns: a training R² gauge steps up to 1.000 (real data, model-complexity.qmd#fig-noise)

With 539 noise columns on 540 stations, training R² is exactly one. A perfect fit.

## Scene 27
visual: manim NoiseColumns: the new-station error shoots past a bar for the largest catch

On new stations, its error is 185, in a survey whose largest catch is 40.

## Scene 28
visual: manim Balance: a see-saw with "flexibility" on one side and "data" on the other (schematic)

What matters is not the number of parameters. It is flexibility, compared with how much
data you have.

# Bias, variance and the noise floor

## Scene 29
visual: manim Targets: an empty target with the true value at the centre (schematic)

Why the U shape? Imagine repeating the survey many times, and fitting the same model to
each one.

## Scene 30
visual: manim Targets: a tight cluster of hits, off to one side

Bias is being wrong the same way every time, like a thermometer that always reads high.

## Scene 31
visual: manim Targets: a second target, hits centred but widely scattered

Variance is being right on average, but different every time. Deep trees are like this.

## Scene 32
visual: manim Decomposition: bias² falls and levels off, variance rises (real data, bias-variance.qmd#fig-decomposition)

More flexibility trades one for the other. Bias falls, then stops. Variance keeps
rising.

## Scene 33
visual: manim Decomposition: the sum of the two draws as a U

Add them together, and you get the U.

## Scene 34
visual: manim Decomposition: the irreducible-noise line drops in above everything

And underneath it all sits a floor: noise that no model can remove.

## Scene 35
visual: manim Decomposition: the floor compared with the smallest reachable error, as two bars

Here it is more than double everything a model can control. That is simply what counting
animals is like.

# Regularisation

## Scene 36
visual: manim RidgeShrink: coefficient bars shrink towards zero as a penalty slider rises (schematic)

Regularisation charges a model for large coefficients, so they shrink towards zero.

## Scene 37
visual: manim RidgeBars: least squares and predict-the-mean bars (real data, regularisation.qmd)

With 44 predictors on 120 stations, least squares did worse than guessing the mean.

## Scene 38
visual: manim RidgeBars: the ridge bar grows, lowest of the three

Ridge beat both.

## Scene 39
visual: manim LassoStability: one dot per term, placed by how often lasso kept it (real data, regularisation.qmd#fig-stability)

Lasso can also drop predictors. But which ones it keeps is not stable.

## Scene 40
visual: manim LassoStability: the real and noise dots separate into two rows, their averages marked

Over a hundred resamples, real predictors were kept only a little more often than pure
noise.

# The trap

## Scene 41
visual: manim PeekAtTest: a box labelled "test set" is opened again and again (schematic)

Now the trap. Every result so far chose its settings by looking at the test set.

## Scene 42
visual: manim PeekAtTest: the box's label changes to "training set, again"

Look, adjust, look again, and the test set quietly becomes a second training set.

## Scene 43
visual: manim CrossValidation: the training data splits into ten folds; the test box stays sealed (schematic)

The honest way is cross-validation. Split the training data into ten folds.

## Scene 44
visual: manim CrossValidation: the held-out fold rotates, then the test box opens once

Fit on nine, score on the tenth, and rotate. Open the test set once, at the very end.

## Scene 45
visual: manim Instability: forty validation splits drop their winners into the grid (real data, hyperparameter-selection.qmd#fig-instability)

Even then, be modest. Forty validation splits chose sixteen different winners.

## Scene 46
visual: manim Instability: an arrow points to the simpler corner of the grid

So when settings tie, prefer the simplest.

## Scene 47
visual: manim RepeatVisits: 160 sites, each with a stack of repeat visits (schematic apart from the 160)

One more catch. The stations come from 160 sites, visited again and again.

## Scene 48
visual: manim RepeatVisits: sites with visits on both sides of the split are circled

A random split puts the same site on both sides, and flatters every number here.
Section seven puts that right.

# Quiz

## Scene 49
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. You add a column of random numbers to a regression. Can its training R² go
down?

## Scene 50
visual: manim QuizAnswer: "No", with the R² steps from the noise experiment rising (real data)

No. It never falls, not even for random numbers.

# Key points

## Scene 51
visual: manim KeyPoints: the first point is ticked

To sum up. <short pause> Training error measures memory, not prediction.

## Scene 52
visual: manim KeyPoints: the second point is ticked

Error on new data is U-shaped in flexibility.

## Scene 53
visual: manim KeyPoints: the third point is ticked

Much of the error in marine counts is noise that no model can remove.

## Scene 54
visual: manim KeyPoints: the fourth point is ticked

Choose settings with cross-validation, and open the test set once.

## Scene 55
visual: manim EndCard: the section's web address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
