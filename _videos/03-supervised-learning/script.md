---
title: "Supervised learning: choosing a model by the question, not the reputation"
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
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. Why the response decides the model. Why a
probability is not a decision. And why the most powerful method can come last.

# The puzzle

## Scene 2
visual: manim Ten: ten model names, from a straight line to boosted trees (page results, choosing-a-method.qmd)

Here are ten models, from a straight line to boosted trees. All ten were fitted to the
same survey, with the same predictors, and scored on the same 200 held-back stations.

## Scene 3
visual: manim Ten: boosting highlighted, "wins competitions", "which would you bet on?"
pause-after: 1.5

Boosting has the best reputation: it wins competitions. Which would you bet on? By the
end of this video, you will see the winner, and why it won.

## Scene 4
visual: manim Fork: "what kind of thing is your response?" (schematic)

Every choice follows from one question. What kind of thing is your response?

# Counts need a count model

## Scene 5
visual: manim Fork: regression predicts a quantity, close counts; classification predicts a category, close does not (schematic)

Regression predicts a quantity, and being close counts: predicting 11 when the truth is
12 is nearly right. Classification predicts a category, and close does not count.

## Scene 6
visual: manim Histogram: individuals caught at each of 800 stations (page results, regression-and-classification.qmd#fig-two-framings)

Our survey counted one species at 800 stations. That is a number, so it is regression.
Right in outline, and wrong in the details that matter.

## Scene 7
visual: manim Histogram: mean 3.9, variance 22.78, "for a Poisson process they would be equal"

The mean catch is 3.9 individuals. The variance is about 23, nearly six times the mean.
Individuals cluster, so counts vary far more than chance alone predicts.

## Scene 8
visual: manim Histogram: the bar at zero highlighted, 180 stations, 22.5%

And nearly a quarter of the stations caught nothing. A smooth model will never
reproduce that spike at zero.

## Scene 9
visual: manim Present: the same data as absent and present, 180 and 620, a catch of 1 and of 40 both "present" (page results)

You could turn the count into presence and absence. Then a station with one individual
and a station with forty are both simply "present".

## Scene 10
visual: manim Present: "dichotomise only when the decision is binary"

If your question is where the species is abundant, you have just deleted the answer.
Dichotomise only when the decision really is binary.

## Scene 11
visual: manim Curves: the polynomial's temperature curve, rising to an optimum and diving below zero (page results, linear-and-polynomial-regression.qmd#fig-shapes)

So keep the count, and fit ordinary regression with a curve for the thermal optimum. It
finds the optimum, then dives below zero in warm water.

## Scene 12
visual: manim Three: linear and polynomial, 2 and 6 negative predictions on 200 test stations, the lowest −2.06 (page results)

On 200 test stations, it predicts a negative number of fish six times, the lowest about
minus 2. Even the straight line manages two.

## Scene 13
visual: manim Curves: the Poisson curve added, flattening towards zero and never crossing it

Poisson regression models the logarithm of the expected count. An exponential cannot
be negative, so impossible predictions become impossible to make.

## Scene 14
visual: manim Three: Poisson plus polynomial added, no negative predictions, lowest 0.16, the smallest error of the three

On the same test stations it makes none, its lowest prediction is 0.16, and it is also
the most accurate of the three.

## Scene 15
visual: manim Multiplier: an effect of 0.35 on the log scale multiplies the count by 1.42, at two fish or two hundred (schematic, the page's example)

And its effects become multipliers. A coefficient of 0.35 multiplies the expected count
by 1.42, whether a station holds two fish or two hundred.

## Scene 16
visual: manim Dispersion: the deviance ratio, 3.95 against 1 (page results)

Poisson assumes the variance equals the mean. Check it: the ratio should be near one,
and here it is almost four. The predictions survive, but the p-values are too small.

## Scene 17
visual: manim Dispersion: the negative binomial, AIC from 3764 to 2839

The negative binomial adds a parameter for exactly this clustering, and the AIC falls
by over 900. On real data, that is the model you would report.

## Scene 18
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. Match the model to what the response actually is. The version built for
it is usually both more plausible and more accurate.

# A probability is not a decision

## Scene 19
visual: manim Rare: a species present at 5% of stations, 11 present among 201 test stations (page results, logistic-regression.qmd)

Now a presence and absence response: a species present at 5% of stations. The test
set holds 201 stations, and only 11 of them have it.

## Scene 20
visual: manim Logistic: the S-shaped curve, the probability between 0 and 1 (schematic)

Logistic regression models the log-odds, so its output is always a probability between
0 and 1. It is a probability, not a class.

## Scene 21
visual: manim Accuracy: the model's accuracy 0.9453, always answering "absent" 0.9453

Its accuracy is 94.5%. Answering "absent" every time is also 94.5%, identical to four
decimal places.

## Scene 22
visual: manim Confusion: the confusion matrix, no station ever predicted present

Print the confusion matrix and you see why. It never once predicts presence. It is the
do-nothing baseline.

## Scene 23
visual: manim Probabilities: every test station's predicted probability, by what was there, the 0.5 line far to the right (page results, logistic-regression.qmd#fig-threshold)

Yet it has learned something. Its ROC AUC is 0.79: given one station with the species
and one without, it ranks the right one higher 79% of the time.

## Scene 24
visual: manim Probabilities: the highest probability, 0.274, nothing reaching 0.5

The trouble is the default rule, which calls a station present above 0.5. The highest
probability it gives any station is 0.27, so nothing is ever called present.

## Scene 25
visual: manim Thresholds: 0.15 catches 2 of 11 with 11 false alarms; 0.05 catches 8 with 68 (page results)

Lower the threshold. At 0.15 it catches two of the eleven, with eleven false alarms. At
0.05 it catches eight, with sixty-eight.

## Scene 26
visual: manim Thresholds: "the model is identical in every row", "only the decision changes"

There is no best row. If each flag sends a vessel out, you want few; if a miss costs a
protected species, you want many. The model is the same in every row.

## Scene 27
visual: manim Odds: depth's odds ratio 0.971, "less likely deeper?", the levels yes and no (page results)

One more trap. Depth has an odds ratio of 0.971, as if the species avoided deep water.
But the underlying model describes the odds of the last level: absence.

## Scene 28
visual: manim Odds: prevalence by depth band, 0.7%, 1.9%, 8.1% and 19.4% (page results)

A simple table settles it: prevalence rises with depth. Check the sign of one
coefficient against a cross-tabulation before you publish a direction.

## Scene 29
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. The model ranks; the threshold is a decision about consequences, and it
is yours, not the model's.

# Flexibility costs data

## Scene 30
visual: manim Tree: a depth-three tree, the root split on chlorophyll, the temperature band (page results, trees-forests-boosting.qmd#fig-tree)

Now the tree-based methods. A decision tree asks yes or no questions. This one splits
first on chlorophyll, then on temperature.

## Scene 31
visual: manim Tree: the band from 6.4 to 10.6 °C predicting 4.2, against 1.4 and 2.1 either side

Below 6.4 degrees it expects 1.4 individuals, above 10.6 it expects 2.1, and in between,
4.2. Two splits, to carve out one optimum.

## Scene 32
visual: manim Tree: "depth never appears", a hump costs two splits, a monotonic effect one

Depth, one of the strongest drivers, never appears. A hump costs a tree two splits, so a
greedy algorithm favours effects that only rise.

## Scene 33
visual: manim Ensembles: a forest of trees on bootstrap samples, averaged; boosting, trees in sequence, each fixing the last (schematic)

A random forest averages hundreds of deliberately varied trees. Boosting builds trees
in sequence, each one fitting what the last ones got wrong.

## Scene 34
visual: manim Four: test error, trees 4.81 and 4.76, forest 4.84, boosting 5.49 (page results)

Here are all three, on the same test stations. Both single trees beat the forest, and the
boosted model, with 500 trees, is worst by a wide margin.

## Scene 35
visual: manim Four: training error added, boosting 0.58 against 5.49 on test

Now its training error: 0.58, roughly seven times better than a tree. It predicts new
stations worst of all. That pair of numbers is the whole story.

## Scene 36
visual: manim Capacity: boosting's training and held-out error against the number of trees (page results, trees-forests-boosting.qmd#fig-capacity)

As trees are added, the training error falls towards zero. The held-out error is lowest
at 50 trees, then rises. That widening gap is overfitting.

## Scene 37
visual: manim Capacity: "about 600 noisy training stations", only so much signal

With about 600 training stations and noisy counts, there is only so much signal. Past
that, extra flexibility learns these particular stations.

## Scene 38
visual: manim Flat: a tree's prediction flat beyond the sampled range (schematic)

And trees cannot extrapolate. Beyond the training data a tree's prediction is flat,
constant forever, and a forest of trees is still flat.

# Ten models ranked

## Scene 39
visual: manim Ranking: the ten models by test error, best at the top (page results, choosing-a-method.qmd#fig-comparison)

Back to the ten models. Boosting at its defaults comes last. The winner is Poisson
regression with two quadratic terms.

## Scene 40
visual: manim Ranking: crosses on the four models that predicted negative fish

Four models predicted negative fish. The winner cannot, because it matches the
response: counts, with optima.

## Scene 41
visual: manim Ranking: the spread within the trees, three times the gap between families; gentle against default boosting, 0.46

The spread among the tree-based models is three times the gap between the best of each
family. How you configure a method matters more than which family it belongs to.

## Scene 42
visual: manim Ranking: "one test set of 200 stations", the top five hard to separate

This is one test set of 200 stations. The top five are hard to separate, and with far
more data the order could reverse. Treat it as a hypothesis, not a ranking.

## Scene 43
visual: manim Habit: fit a simple model and a flexible one, the gap measures missing structure (schematic)

The practical habit: fit a simple model and a flexible one. The gap between them tells
you how much structure you have not specified.

## Scene 44
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Flexibility has to be paid for with data and signal. Choose by the
question, not by the reputation.

# Quiz

## Scene 45
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Your random forest scores best on the test set. Now you need predictions
for water warmer than any you sampled. Should you use it?

## Scene 46
visual: manim QuizAnswer: "no", the forest flat beyond the sampled range, a parametric model with its assumption stated (schematic)

No. Beyond the sampled range, the forest predicts no change, with complete confidence.
Use a parametric model, and state its assumption loudly.

# Key points

## Scene 47
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: match the model to what the response
is.

## Scene 48
visual: manim KeyPoints: the second ticked

Two: a probability is not a decision, so choose the threshold.

## Scene 49
visual: manim KeyPoints: the third ticked

Three: flexibility costs data, so choose by the question.

## Scene 50
visual: manim EndCard: the site's address and a thanks

The pages for this section, with all the code, are linked below. Thanks for watching.
