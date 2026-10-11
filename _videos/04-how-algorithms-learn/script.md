---
title: "How algorithms learn: the loss, the search and its assumptions"
section: chapters/04-how-algorithms-learn/index.qmd
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

This video is an overview built on three ideas, each with the reason it matters: the
loss decides what a model pays attention to, a search can fail quietly so it must be
checked, and every loss assumes a distribution, as a prior adds a penalty. It does not
tour every page; the units of the inputs, separation, trees and the maths of likelihood
are left to the pages. It never says which variables truly drive the species.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video looks at what
happens when a model is fitted, that is, when it learns its numbers from the training
data. It covers three things: the one number every fit makes as small as it can, the
search that finds the best values, and the assumptions hidden inside that number.

# The number a fit makes small

## Scene 2
visual: manim Loop: "parameters: the numbers a model learns"; three cards in a circle, "guess the parameters", "score how wrong", "adjust and repeat" (schematic)

Let's start with what fitting means. A model has parameters: the numbers it learns from
the data, such as the coefficients of linear regression, which we met in supervised
learning. Most models find them in the same way. The algorithm guesses the parameters,
scores how wrong the predictions are, adjusts the parameters to do a little better, and
repeats. Fitting is a search for the best score.

## Scene 3
visual: manim Residual: a line through scattered points, one point's gap to the line drawn and labelled "residual = observed − predicted"; then "noise: what the conditions do not decide", with "patchy animals", "a net that fished badly", "chance"; a card "even the best fit leaves residuals" (schematic, after loss-functions.qmd)
pause-after: 0.5

The score is built from residuals. A residual is how far one prediction missed: the
observed count minus the predicted one. Part of every residual is noise, the part of a
count that the station's conditions do not decide, such as patchy animals, a net that
fished badly, or plain chance. No model can predict noise, so even the best fit leaves
residuals.

## Scene 4
visual: manim Losses: squared error as a steep U, "miss × miss", and absolute error as a shallow V, "the size of the miss", against the residual; a miss of 10 marked, costing 100 and 10 (schematic, the page's definitions)

A loss function turns each miss into a penalty, and the average penalty over all the
stations is the score. The two most common losses treat big misses very differently.
Squared error multiplies each miss by itself, so a miss of 10 costs 100, a hundred times
a miss of 1. Absolute error just takes the size of the miss, so a miss of 10 costs 10,
only ten times as much.

## Scene 5
visual: manim Lines: abundance against chlorophyll at 749 stations, "each dot: one station"; the squared-error line and the absolute-error line (page results, loss-functions.qmd#fig-two-lines)

Here is why that matters. This chart shows the count of one species against
chlorophyll, a sign of how much plankton is in the water, at the survey's 749 stations.
Each dot is a station. Fit a straight line with squared error, then fit it again with
absolute error. The two losses draw two different lines through exactly the same data.

## Scene 6
visual: manim Share: the worst 5% of stations, 37 of them, supplying 50% of the squared error; "the slope: how fast the line rises", the question "does the slope rest on a few stations?"; then the largest catch removed, the squared-error slope moving 13.5% and the absolute-error slope 2.1% (page results, loss-functions.qmd)
pause-after: 0.5

Why do they differ? Squared error listens hardest to the biggest misses. Just 37
stations, 5 per cent of the data, supply half of all the squared error. That matters if
the slope, how fast the line rises with chlorophyll, rests on those few stations. So
remove one large catch, a single haul a repeat survey could easily miss, and fit again.
The squared-error slope moves by 13.5 per cent; the absolute-error slope, by only 2.1.

## Scene 7
visual: manim Readings: two cards, "a real shoal: let squared error listen" and "a net that fished badly: absolute error is safer", under "the loss is a choice about the science" (schematic)
pause-after: 0.5

So which loss is right? If the big catches are real shoals, they are important, and
squared error should listen to them. If they come from a net that fished badly,
absolute error is safer. The data cannot tell you which. It is a choice about your
science, so always say which loss you used.

## Scene 8
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. A fit makes a loss small, and the loss decides what the model pays
attention to.

# The search that finds the parameters

## Scene 9
visual: manim Landscape: the score as a bowl over two parameters, "each spot: one choice of the two parameters", "height: the score", its lowest point marked "the best parameters"; "a formula for a straight line, a search for most models" (schematic)

Now, how does the algorithm find the best parameters? For a straight line fitted with
squared error, a formula gives them in one step. Most models have no formula, so the
algorithm has to search. Picture a map where each spot is one choice of two parameters,
and the height is the score for that choice. The score forms a landscape, and the best
parameters sit at its lowest point.

## Scene 10
visual: manim Downhill: a bowl, a dot feeling the slope and stepping down; "gradient: the slope of the ground"; "the learning rate: the size of each step, a hyperparameter" (schematic)

The simplest search is called gradient descent. The gradient is the slope of the ground
under your feet, and descent means walking down it. So the algorithm finds which way is
downhill, takes a step, and repeats until the ground is flat. The size of each step is
set by the learning rate. Like the number of neighbours in k-nearest neighbours, it is a
hyperparameter: a setting we choose before fitting.

## Scene 11
visual: manim Paths: the objective's contours for two slopes, "each ring: the same score", the lowest point marked; the walk at learning rate 0.3 arriving in 11 steps, then 0.02 creeping, needing 197 (page results, gradient-descent.qmd#fig-paths)

Here is gradient descent on the survey. It fits a straight line with two slopes, one
for chlorophyll and one for depth. A formula knows the answer, so we can check the walk
against it. Each ring joins the pairs of slopes with the same score, and the lowest
point is in the middle. At a learning rate of 0.3, the walk reaches the bottom in 11
steps. At 0.02, it creeps, and needs 197.

## Scene 12
visual: manim Overshoot: a bowl, each step crossing the valley and landing higher on the far side; "0.8: never arrives", "no warning" (schematic, the page's rate)
pause-after: 0.5

But make the steps too large, and each one overshoots the valley and lands higher on the
other side. At a learning rate of 0.8, the walk climbs out and never arrives, and nothing
on the way warns you.

## Scene 13
visual: manim Printout: a model's output, coefficients that look normal, and a line "converged: FALSE" highlighted; "converged: the steps stopped improving the score"; "check the flag first" (schematic)

That is why a fit needs checking. A search that went wrong still prints coefficients,
and they look perfectly normal. The software also records whether the search finished.
A search has converged when its steps stop improving the score, and a convergence flag
says whether that happened. Look at it before you read anything else.

## Scene 14
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Fitting is a search, and a search can fail quietly. Check that it
finished.

# The assumptions inside the loss

## Scene 15
visual: manim Distributions: "a distribution: how the values scatter around the prediction"; three cards, a bell curve "Normal: a measurement" giving "squared error", bars from zero "Poisson: a count" giving "Poisson deviance", two bars "present or absent" giving "log loss"; "name the distribution, and the loss follows" (schematic, after likelihood-and-priors.qmd)
pause-after: 0.5

So far, we have chosen a loss by what it pays attention to. But each loss also assumes
a distribution: a description of how the observed values scatter around the prediction.
Squared error assumes a bell-shaped curve, the Normal distribution, which suits
measurements. Assume a Poisson distribution, made for counts, and the loss becomes
Poisson deviance. For present or absent, it becomes log loss. Name the distribution, and
the loss follows. This is called maximum likelihood: the fit picks the parameters that
make the data you saw most likely.

## Scene 16
visual: manim Negative: a bell curve around a low prediction with the part below zero shaded, "squared error: below zero allowed"; beside it Poisson bars starting at zero, "Poisson: never below zero" (schematic)
pause-after: 0.5

That explains a puzzle from supervised learning: polynomial regression predicted fewer
than zero animals at some warm stations. It was fitted with squared error, which assumes
a Normal curve, and a Normal curve runs below zero, so the loss saw nothing wrong. A
Poisson distribution stops at zero, so Poisson regression never predicts fewer than zero
animals.

## Scene 17
visual: manim Forty: forty stations, twelve inputs; "each effect: animals per standard deviation of its input"; temperature +9.23 and its square −6.78, two bars cancelling (page results, likelihood-and-priors.qmd)

An assumption can also carry what you knew before the survey. Take a small survey:
forty stations and twelve inputs, such as depth, temperature and their squares. Each
effect is the change in animals for one standard deviation of its input. The fit gives
temperature an effect of 9.23 animals, and its square minus 6.78. Two large effects that
cancel each other out are a warning sign: with so few stations, the fit is chasing
chance patterns.

## Scene 18
visual: manim Prior: the heading "what you knew before can help"; a Normal curve centred on zero, "a prior: effects that large are rare"; the two bars shrinking to 0.26 and −0.18 (page results, likelihood-and-priors.qmd)

With so few stations, what you knew before the survey can help. And you did know
something: effects that large are rare. A prior writes that belief down, as a curve
centred on zero, so small effects are likely and large ones are not. Combined with the
data, it pulls the temperature effect from 9.23 to 0.26, and its square from minus 6.78
to minus 0.18.

## Scene 19
visual: manim Penalty: "loss + penalty on large parameters"; "a prior = a penalty", "this is ridge regression" (schematic)

In the fit, a prior works as a penalty added to the loss, one that grows as the
parameters grow. So the fit now balances two things: missing the data, and using large
parameters. This is ridge regression. The generalisation section uses it to stop models
overfitting, that is, learning the noise along with the pattern.

## Scene 20
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. Every loss assumes a distribution for the data, and a prior on the
parameters adds a penalty.

# Quiz

## Scene 21
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A colleague fits logistic regression, the model that predicts the
probability of presence, and every coefficient looks sensible. Can they trust them?

## Scene 22
visual: manim QuizAnswer: "not yet"; the fit stopped after two steps beside the finished one, chlorophyll 0.268 against 0.348, "converged: FALSE" highlighted (page results, parameter-estimation.qmd)

Not yet. On the survey, a fit stopped after two steps gave a chlorophyll coefficient 23
per cent out, and it looked entirely normal. Only the convergence flag showed the
problem. Check it first.

# Key points

## Scene 23
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: the loss decides what a model pays attention to.

## Scene 24
visual: manim KeyPoints: the second ticked

Two: a search can fail quietly, so check that it finished.

## Scene 25
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: every loss assumes a distribution, and a prior adds a penalty.

## Scene 26
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
