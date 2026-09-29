---
title: "How algorithms learn: the loss, the search, and the prior"
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
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. Where a model's loss comes from. Why a fit
can fail without telling you. And why a term with no data in it can make predictions
better.

# The puzzle

## Scene 2
visual: manim Two fits: one model, the same forty stations, temperature 8.59 against 0.33 (page results, map-and-priors.qmd)

Here are two fits of the same model to the same forty stations, a pilot survey with
twelve predictors. In one, the temperature coefficient is 8.59. In the other, 0.33.

## Scene 3
visual: manim Two fits: the second "plus one term, containing no data", "which predicts new stations better?"
pause-after: 1.5

The second fit had one extra term, and that term contains no data at all. Which one
predicts new stations better? By the end of this video, you will know, and why.

## Scene 4
visual: manim Loop: score how wrong, change the numbers, repeat (schematic)

To see why, you need to know what fitting is. It is a search: score how wrong the model
is, change its numbers to be a little less wrong, and repeat.

# Every fit minimises a loss

## Scene 5
visual: manim Losses: squared error, absolute error and Huber against the residual (schematic, the page's definitions)

The score is the loss. Squared error makes a miss of 10 a hundred times worse than a miss
of 1. Absolute error makes it ten times worse. Huber is a compromise.

## Scene 6
visual: manim Lines: abundance against chlorophyll at 749 stations, three fitted lines (page results, loss-functions.qmd#fig-three-lines)

Fit abundance against chlorophyll three times, changing nothing but the loss, and you get
three answers. The squared-error line starts at 2.36 individuals, the absolute-error line
at 1.13.

## Scene 7
visual: manim Share: the worst 5% of stations, 49.7% of the squared error, 21.0% of the absolute error (page results)

Why? Thirty-seven stations, 5% of the data, supply half of the total squared error, but
only a fifth of the absolute error.

## Scene 8
visual: manim Drop one: the largest catch removed, the squared-error slope moves 13.5%, the absolute-error slope 2.1% (page results)

Delete the single largest catch, one station of 749, and the least-squares slope moves by
13.5%. The absolute-error slope moves by 2.1%.

## Scene 9
visual: manim Two readings: "a real aggregation" favours squared error, "a net that fished badly" absolute error (schematic)

Neither loss is wrong. If the big hauls are real aggregations, squared error is right. If
they are a net that fished badly, you have handed half the objective to your worst data.

## Scene 10
visual: manim Likelihood: the Poisson probability of counts 3, 0 and 11 against the expected count, their product peaking at the mean, 4.67 (page results, maximum-likelihood.qmd#fig-one-station)

So where do losses come from? Likelihood asks which values make the data you saw most
probable. For three stations that caught 3, 0 and 11, the answer is their mean.

## Scene 11
visual: manim Menu: the assumed distribution and the loss it becomes, Normal to squared error, Poisson to Poisson deviance, yes or no to log loss (schematic, the page's table)

Take the negative logarithm, and a likelihood becomes a loss. Assume Normal errors, and
you get squared error. Poisson gives Poisson deviance. Yes or no gives log loss.

## Scene 12
visual: manim Normal: maximum likelihood and least squares side by side, identical to four decimal places (page results)

It is not an analogy. Maximum likelihood under a Normal model returns exactly the
least-squares line.

## Scene 13
visual: manim Normal: the Normal curve around a small expected count, its tail running below zero, "negative fish" (schematic)

So least squares on counts silently assumes a distribution that runs to minus infinity.
That is why a linear model can predict negative fish.

## Scene 14
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. The loss is an assumption about your data. Choose it deliberately, and
report it.

# Fitting is a search

## Scene 15
visual: manim Formula: the normal equations against lm(), the same four coefficients (page results, parameter-estimation.qmd)

For a few models the best numbers can be calculated. Least squares has a formula: exact,
in one step, the same every time. Almost nothing else does.

## Scene 16
visual: manim IRLS: logistic regression's log-likelihood by step, −513.6, −378.3, −373.3, then flat (page results)

Logistic regression has to search. From a standing start, each step improves the
log-likelihood, and by the fourth it has stopped changing.

## Scene 17
visual: manim Grid: 100 values per parameter, two parameters 10⁴ evaluations, four 10⁸, ten 10²⁰ (page results)

Why not simply try every combination? At a hundred values each, two parameters is ten
thousand evaluations. Four is a hundred million. Ten is ten to the power twenty.

## Scene 18
visual: manim Downhill: a bowl, a dot feeling the slope and stepping down (schematic)

So the search has to be directed. Feel which way is downhill, take a step, and repeat.
That is gradient descent, and it trains every neural network you have heard of.

## Scene 19
visual: manim Paths: the objective's contours for two slopes, the walk at learning rate 0.3 reaching the minimum (page results, gradient-descent.qmd#fig-paths)

The size of each step is the learning rate. At 0.3, this walk reaches the bottom of the
bowl in six steps.

## Scene 20
visual: manim Paths: 0.02 still short after 40 steps, it needs 106; 0.72 zig-zagging, it needs 161

At 0.02 it is still short after forty steps, and needs 106. At 0.72 it zig-zags across
the valley, and needs 161.

## Scene 21
visual: manim Cliff: the stable limit 0.7282; at 0.80, sixty steps and an MSE of 7.3 billion (page results)

And there is a cliff edge. Above 0.7282 the walk does not arrive slowly; it diverges. At
0.8, sixty steps take the error to 7.3 billion.

## Scene 22
visual: manim Units: depth's standard deviation 40.6 m, chlorophyll's 1.58 mg m⁻³; the bowl stretched 766 to 1, standardised 2.2 (page results)

That limit is set by the shape of the bowl, and the shape by your units. Unscaled, this
bowl is 766 times more stretched one way than the other. Standardised, 2.2.

## Scene 23
visual: manim Steps: at the best rate each allows, 17 steps standardised, 1,500 unscaled (page results)

Give each its best learning rate. The standardised version arrives in 17 steps, the
unscaled one in 1,500. The same answer, with eighty-eight times the work.

## Scene 24
visual: manim Which: scaling matters for gradient descent, penalties, networks and k-means; not for lm, glm or trees (schematic, the page's list)

That is the real reason to scale your predictors. It matters for gradient descent,
penalised regression, networks and k-means, and not at all for trees. The rule follows the
algorithm.

## Scene 25
visual: manim Truncated: logistic regression stopped after 2 iterations, −0.312 against −0.344, converged FALSE (page results, reading-a-fit.qmd)

A search can also fail without saying so. Stop logistic regression after two iterations,
and the chlorophyll coefficient is 9% out, and perfectly plausible.

## Scene 26
visual: manim Truncated: the converged flag highlighted, "check the flag, not the coefficients"

The only difference is a flag, "converged", and you have to ask for it.

## Scene 27
visual: manim Separation: the leaked catch weight, coefficient −158, standard error 13,515, p 0.99 (page results)

Or give it the leaked catch weight. The coefficient is minus 158, with a standard error of
13,515, and a p-value of 0.99.

## Scene 28
visual: manim Separation: the likelihood rising forever, no maximum, the search stopped by its cap at 25 iterations (schematic, the page's cap)

That is not weak evidence. The predictor separates the classes, so there is no best
value, and the search walked on until its cap of 25 iterations stopped it.

## Scene 29
visual: manim Runs: five unseeded forests spanning 0.037 in RMSE; twenty k-means starts, ten different answers (page results, reading-a-fit.qmd#fig-instability)

Random algorithms land somewhere different each run. Five unseeded forests spanned 0.037
in error. Twenty k-means runs found ten different answers, and every one reported success.

## Scene 30
visual: manim Runs: "a seed gives reproducibility, not stability"

A seed makes a result reproducible, not stable. Remove it on purpose, and treat the spread
as the resolution of every comparison you make.

## Scene 31
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Fitting is a search. Check that it arrived, not just that it printed an
answer.

# A penalty is a prior

## Scene 32
visual: manim Wide: the likelihood for the temperature coefficient, peak 8.59, standard error 5.95 (page results, map-and-priors.qmd#fig-prior-likelihood)

Back to the forty stations. Maximum likelihood looks only at the data in front of it, and
gives temperature 8.59. But its standard error is 5.95: the data barely tell it from zero.

## Scene 33
visual: manim Fighting: temperature +8.59 and its square −6.20, "two collinear terms fighting, not biology" (page results)

Temperature and its square take huge opposite values that partly cancel. That is two
collinear terms fighting, not biology.

## Scene 34
visual: manim Wide: a prior centred on zero added, the posterior pulled almost to zero

You know effects that large do not occur. A prior says so: coefficients here are usually
within about plus or minus one. Combined with the likelihood, it pulls the estimate
almost to zero.

## Scene 35
visual: manim Ridge: the MAP and ridge coefficients, identical, "a Normal prior is ridge regression" (page results)

That is MAP estimation, and written out, it is exactly ridge regression. The penalty is
a Normal prior on the coefficients.

## Scene 36
visual: manim Flat: maximum likelihood as a flat prior, 900 as plausible as 0.9 (schematic, the page's example)

So maximum likelihood is not assumption-free. It is a prior that finds a coefficient of
900 exactly as plausible as 0.9.

## Scene 37
visual: manim Scores: test error on 680 stations, the mean 4.850, maximum likelihood 4.745 (page results)

Now, the puzzle. On the other 680 stations, predicting the mean everywhere gives an error
of 4.850. Maximum likelihood gives 4.745, about 2% better.

## Scene 38
visual: manim Scores: the fit with the prior, 4.495, three times the improvement
pause-after: 0.5

The fit with the prior gives 4.495: more than three times the improvement, from a term
with no data in it.

## Scene 39
visual: manim Curve: training and test error against the prior's strength, training rising, test falling then rising (page results, map-and-priors.qmd#fig-lambda)

As the prior tightens, training error only rises. Test error falls, then rises. The
training curve cannot choose the strength for you.

## Scene 40
visual: manim Curve: "a prior can be wrong", a tight one shrinks real effects too

And a prior can be wrong. A tight one shrinks real effects too. Like the loss, it is an
assumption, and it belongs in your methods.

## Scene 41
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. A penalty is a prior: what you knew before the survey. With few
stations, it can be worth more than the data.

# Quiz

## Scene 42
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A colleague fits ridge regression with depth in millimetres and temperature in
degrees, without standardising. What goes wrong?

## Scene 43
visual: manim QuizAnswer: "about plus or minus one" means nothing without a unit; depth in millimetres barely penalised (schematic)

The prior says coefficients are about plus or minus one, and that means nothing without a
unit. Depth in millimetres is barely penalised at all. Standardise first.

# Key points

## Scene 44
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: the loss is an assumption, so choose it
and report it.

## Scene 45
visual: manim KeyPoints: the second ticked

Two: fitting is a search, so check that it arrived.

## Scene 46
visual: manim KeyPoints: the third ticked

Three: a penalty is a prior, and with little data it can help.

## Scene 47
visual: manim EndCard: the site's address and a thanks

The pages for this section, with all the code, are linked below. Thanks for watching.
