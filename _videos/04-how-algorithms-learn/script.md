---
title: "How algorithms learn: the loss, the search and the prior"
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
checked, and a prior keeps a small survey sensible. It does not tour every page;
maximum likelihood, the units of the inputs, separation and random runs are left to
the pages. It never says which variables truly drive the species.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

This video looks at what happens when a model is fitted. It covers three ideas: the one
number every fit makes small, the search that finds the best parameters, and how
knowing something before the survey helps a small one.

# The number a fit makes small

## Scene 2
visual: manim Loop: three cards in a circle, "guess the parameters", "score how wrong", "adjust and repeat" (schematic)

Every model in this course was fitted the same way. The algorithm guesses its
parameters, the numbers it learns from the data. It scores how wrong that guess is,
adjusts the parameters to do better, and repeats. Fitting is a search for the best
score.

## Scene 3
visual: manim Residual: a line through scattered points, one point's gap to the line drawn and labelled "residual = observed − predicted"; then a dashed curve, "the true average: unknown", and the same point's gap to it labelled "error"; a card "the residual is the fit's estimate of the error" (schematic, after loss-functions.qmd)
pause-after: 0.5

The score is built from residuals. A residual is how far one prediction missed: the
observed count minus the predicted one. It is not quite an error. The error is the miss
against the true average for those conditions, the count you would get on average if
you sampled there again and again. Nobody knows that average, so the residual is the
fit's estimate of the error.

## Scene 4
visual: manim Losses: squared error as a steep U and absolute error as a shallow V against the residual; a miss of 10 marked, costing 100 and 10 (schematic, the page's definitions)

A loss function turns each miss into a penalty, and the average penalty is the score.
The two common losses treat big misses very differently. Under squared error, a miss of
10 costs a hundred times a miss of 1. Under absolute error, only ten times.

## Scene 5
visual: manim Lines: abundance against chlorophyll at 749 stations, the squared-error line and the absolute-error line (page results, loss-functions.qmd#fig-two-lines)

That difference changes the answer. On the survey's 749 stations, the two losses draw
two different lines through exactly the same data.

## Scene 6
visual: manim Share: the worst 5% of stations, 37 of them, supplying 50% of the squared error; the question "does the slope rest on a few stations?"; then the largest catch removed, the squared-error slope moving 13.5% and the absolute-error slope 2.1% (page results, loss-functions.qmd)
pause-after: 0.5

Squared error listens hardest to the biggest misses. Just 37 stations, 5 per cent of
the data, supply half of it. That matters if the slope we would report rests on those
few stations. So remove one large catch, a single haul a repeat survey could easily
miss, and refit. The squared-error slope moves by 13.5 per cent; the absolute-error
slope, by 2.1.

## Scene 7
visual: manim Readings: two cards, "a real shoal: let squared error listen" and "a net that fished badly: absolute error is safer", under "the loss is a choice about the science" (schematic)
pause-after: 0.5

So which loss is right? If the big catches are real shoals, they matter, and squared
error should listen to them. If they come from a net that fished badly, absolute error
is safer. The data cannot tell you which. It is a choice about your science, so say
which loss you used.

## Scene 8
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. A fit makes a loss small, and the loss decides what the model pays
attention to.

# The search that finds the parameters

## Scene 9
visual: manim Landscape: the score as a bowl over two parameters, its lowest point marked "the best parameters"; "a formula for a straight line, a search for most models" (schematic)

For a straight line, a formula gives the best parameters in one step. Most models have
no formula, so the algorithm has to search. Picture the score as a landscape. The best
parameters sit at its lowest point.

## Scene 10
visual: manim Downhill: a bowl, a dot feeling the slope and stepping down; "the learning rate: the size of each step" (schematic)

Gradient descent is the simplest search. Find which way is downhill, take a step, and
repeat until the ground is flat. The size of each step is called the learning rate.

## Scene 11
visual: manim Paths: the objective's contours for two slopes; the walk at learning rate 0.3 arriving in 11 steps, then 0.02 creeping, needing 197 (page results, gradient-descent.qmd#fig-paths)

The step size matters. At a learning rate of 0.3, this walk reaches the bottom in 11
steps. At 0.02, it creeps, and needs 197.

## Scene 12
visual: manim Overshoot: a bowl, each step crossing the valley and landing higher on the far side; "0.8: never arrives", "no warning" (schematic, the page's rate)
pause-after: 0.5

Too large, and each step overshoots the valley and lands higher on the other side. At
0.8, the walk climbs out and never arrives, and nothing on the way warns you.

## Scene 13
visual: manim Printout: a model's output, coefficients that look normal, and a line "converged: FALSE" highlighted; "check the flag first" (schematic)

That is why a fit needs checking. A search that went wrong still prints coefficients,
and they look perfectly normal. The software records whether the search finished, in a
convergence flag. Look at it before you read anything else.

## Scene 14
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Fitting is a search, and a search can fail quietly. Check that it
finished.

# Knowing something before the survey

## Scene 15
visual: manim Forty: forty stations, twelve inputs; temperature +9.23 animals per standard deviation and its square −6.78, two bars cancelling (page results, map-and-priors.qmd)

Now a small survey: forty stations and twelve inputs. The fit gives temperature an
effect of 9.23 animals, and its square minus 6.78. Two large effects that cancel out
are a warning sign: with so few stations, the fit is chasing chance patterns.

## Scene 16
visual: manim Prior: the heading "what you knew before can help"; the likelihood for the temperature coefficient, wide, peaking at 9.23; the heading turns into "a prior: effects that large are rare" as a prior centred on zero is added; the combined estimate at 0.22 (page results, map-and-priors.qmd#fig-prior-likelihood)

With so few stations, what you knew before the survey can help the model predict
better. And you did know something: effects that large are rare. A prior writes that
down, as a curve centred on zero. Combined with the data, it pulls the temperature
effect to 0.22.

## Scene 17
visual: manim Penalty: "loss + penalty on large parameters"; "a prior = a penalty", "this is ridge regression" (schematic)

In the fit, a prior works as a penalty added to the loss, one that grows as the
parameters grow. This is ridge regression, and the next section of the course uses it
to stop models overfitting.

## Scene 18
visual: manim Scores: test RMSE on the 680 stations held back, predicting the average 4.85, without the prior 4.76, with the prior 4.45 (page results, map-and-priors.qmd)
pause-after: 0.5

Does it help? On the 680 stations held back, predicting the average gives an error of
4.85. The fit without a prior gives 4.76; with the prior, 4.45. The prior fits the
forty stations a little worse, and predicts new ones better.

## Scene 19
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. With little data, what you knew before the survey keeps a model
sensible.

# Quiz

## Scene 20
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A colleague fits logistic regression, and every coefficient looks
sensible. Can they trust them?

## Scene 21
visual: manim QuizAnswer: "not yet"; the fit stopped after two steps beside the finished one, chlorophyll −0.312 against −0.344, "converged: FALSE" highlighted (page results, reading-a-fit.qmd)

Not yet. On the survey, a fit stopped after two steps gave a chlorophyll coefficient 9
per cent out, and it looked entirely normal. Only the convergence flag showed the
problem. Check it first.

# Key points

## Scene 22
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: the loss decides what a model pays attention to.

## Scene 23
visual: manim KeyPoints: the second ticked

Two: a search can fail quietly, so check that it finished.

## Scene 24
visual: manim KeyPoints: the third ticked

Three: with little data, a prior keeps a model sensible.

## Scene 25
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
