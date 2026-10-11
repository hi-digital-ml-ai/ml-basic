---
title: "Supervised learning: from a straight line to boosting"
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

This video is an overview: it introduces the section and says what its seven pages
cover, without teaching each page in full. It uses only the methods the section
introduces, and never says which variables truly drive the species. "Poisson" is
respelled for the voice in _videos/pronunciation.yml; the captions keep the spelling.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is a short tour
of supervised learning, where a model learns from examples whose answers are known. It
covers three things: models that add up their inputs, models that learn their shape
from the data, and how to choose between them.

# Models that add up their inputs

## Scene 2
visual: manim Outcome: "the outcome: the answer the model predicts"; a quantity on a number line, "regression"; a category as present and absent, "classification" (schematic)

Let's start with the outcome: the answer the model predicts. As we saw in the
introduction, when the outcome is a quantity, such as a temperature or a count, the
task is regression. When it is a category, such as present or absent, it is
classification. The kind of outcome decides which models fit.

## Scene 3
visual: manim Histogram: "each bar: the stations with that count"; stations by the number of animals caught, "never below zero" at the left edge, "a few large catches" at the right (page results, count-regression.qmd)

In this section, the outcome is the count of one species at each station of the
survey. This chart is a histogram: each bar shows how many stations caught that number
of animals. A count is a whole number, and it never falls below zero. Most stations
caught only a few animals, and a few made large catches.

## Scene 4
visual: manim Curves: "a starting value + so much per degree + so much per metre …", "coefficients: learned from the training data"; then predicted count against temperature, the straight line of linear regression (page results, linear-and-polynomial-regression.qmd#fig-shapes)

The first family of models adds up its inputs. Linear regression, met in the
introduction as a straight line, starts from a fixed value, then adds a fixed amount
for each input: so much per degree of temperature, so much per metre of depth. These
amounts are its coefficients, learned from the training data. Against temperature,
that gives one slope, the same in cold water and warm.

## Scene 5
visual: manim Curves: "+ temperature²" as one more input; polynomial regression added, rising to a peak marked at 7.5 °C (page results, linear-and-polynomial-regression.qmd#fig-shapes)

But a straight line cannot rise and then fall. Add the square of temperature as one
more input, and the line can bend into a curve. This is polynomial regression. It still
adds up its inputs, and here it finds a peak at 7.5 degrees.

## Scene 6
visual: manim Curves: the part of the curve below zero shaded, "fewer than zero animals", 12 of 202 test stations (page results, linear-and-polynomial-regression.qmd)

But nothing in linear regression knows that a count stops at zero. In warm water the
curve falls below zero, and it predicts fewer than zero animals at 12 of the 202 test
stations.

## Scene 7
visual: manim Curves: "add up the inputs → the log of the count → the count, always above zero"; Poisson regression added, levelling off just above zero (page results, count-regression.qmd#fig-shapes)

Poisson regression is made for counts. It adds up its inputs in the same way, but the
sum gives the logarithm of the count, not the count itself. Turning a logarithm back
into a count always gives a number above zero. So a prediction can come close to zero,
but never cross it.

## Scene 8
visual: manim Logistic: "the chance that the species is present"; the probability of presence against temperature, between 0 and 1; the training stations as dots, found along the top, not found along the bottom (page results, logistic-regression.qmd#fig-curve)

For present or absent, logistic regression uses the same idea. It adds up its inputs,
then squeezes the sum into a probability, the chance that the species is present,
which always stays between zero and one. The dots are the training stations: along the
top where the species was found, along the bottom where it was not.

## Scene 9
visual: manim Mistakes: a threshold, a cut-off, turns the probability into present or absent; two cards, a false alarm (said present, was absent) and a miss (said absent, was present) (schematic)

To get a plain answer, choose a threshold, a cut-off: above it, call the species
present; below it, absent. The answer can be wrong in two ways. A false alarm says
present where the species was absent. A miss says absent where it was present.

## Scene 10
visual: manim Thresholds: false alarms and misses on the test stations at thresholds 0.5 and 0.9, 34 and 4, then 6 and 97; "what does each mistake cost?" (page results, logistic-regression.qmd)
pause-after: 0.5

At a threshold of 0.5, the model gives 34 false alarms and 4 misses on the test
stations. Raise it to 0.9, and the false alarms fall to 6, but the misses rise to 97.
So the right threshold depends on what each mistake costs.

## Scene 11
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. Match the model to the outcome: a count is never negative, and a
probability needs a threshold you choose.

# Models that learn their shape

## Scene 12
visual: manim Neighbours: "every model so far assumes a shape"; then "k-nearest neighbours" as the heading; stations as grey dots on two inputs, a new station, its five nearest joined to it and ringed, "k = 5", "prediction: their average count" (schematic, after nearest-neighbours.qmd img/nearest-neighbours.svg)

Next, models that learn their shape. Every model so far assumes a shape, such as a
line or a curve. k-nearest neighbours, met in the introduction, assumes none. For a new
station, it finds the k most similar stations in the training data, here five, and
predicts their average count.

## Scene 13
visual: manim Neighbours: "the error: a typical miss (RMSE)"; the error against the number of neighbours, on the training stations and on the validation sites; the first at zero for one neighbour, the second at its worst there, "overfitting: learning the noise"; both rising towards 300 (page results, nearest-neighbours.qmd#fig-neighbours)

How many neighbours should it use? This chart shows the error, the typical miss from
the introduction, for each number of neighbours. With one neighbour, the model copies
every chance high and low in the training data. Its error on the training stations is
zero, but on the validation sites, held back to choose between settings, it is at its
worst. This is overfitting: learning the noise along with the pattern. With hundreds of
neighbours, every prediction blurs into one average.

## Scene 14
visual: manim Neighbours: the validation error lowest at 30 neighbours, marked; "a hyperparameter: chosen on validation data" (page results, nearest-neighbours.qmd#fig-neighbours)
pause-after: 0.5

In between, the validation error is lowest at 30 neighbours. A setting like k, which we
fix before the model is fitted, is called a hyperparameter. It is chosen on validation
data, never on the training data, where one neighbour always looks perfect.

## Scene 15
visual: manim Tree: "a decision tree" as the heading; the depth-3 tree for the count grows question by question, chlorophyll first, then two questions on temperature; "leaf: the average count of its stations" (page results, decision-trees.qmd#fig-tree)

A decision tree, also met in the introduction, works differently. It asks yes-or-no
questions about the inputs, one after another, like an identification key. Each final
group, called a leaf, predicts the average count of the training stations that reach
it. Here, the first question is about chlorophyll, and the next two are about
temperature.

## Scene 16
visual: manim Tree: the band between 6.4 and 10.4 °C highlighted, average 5.2 animals, against 1.5 below and 2.6 above (page results, decision-trees.qmd)

For most stations, those two questions about temperature find a band, from 6.4 to
10.4 degrees, with the most animals. A peak takes one question for each side.

## Scene 17
visual: manim Depth: "depth: the number of questions in a row"; the error on the training stations and on the validation sites against depth; the first falling towards zero, the second lowest at depth 5 (page results, decision-trees.qmd#fig-depth)
pause-after: 0.5

How deep should a tree grow? Its depth, the number of questions in a row, is a
hyperparameter too. A deeper tree fits the training stations ever more closely, but on
the validation sites the error is lowest at depth 5, then climbs: overfitting again.

## Scene 18
visual: manim Resamples: "a resample: stations drawn at random, some twice, some not at all"; six trees from resampled stations, each opening on chlorophyll, their thresholds marked on one line from 2.57 to 12.6 (page results, forests-and-boosting.qmd)

One tree is also unstable: a small change in the data can change it a lot. To see
this, grow it on six resamples. A resample draws the same number of stations at random
from the training data, so some come twice and some not at all. The first question is
always about chlorophyll, but its threshold moves from 2.57 to 12.6.

## Scene 19
visual: manim Forest: "a random forest: hundreds of trees, each on its own resample, averaged"; thirty of the page's forest's trees as thin staircases across temperature, then the average of all its trees as a thick line in small steps (page results, forests-and-boosting.qmd)

A random forest puts this to use. It grows hundreds of trees, each on its own
resample, and each question chooses from a few inputs picked at random, so the trees
differ. Then it averages their predictions. The big jumps of single trees shrink into
small steps.

## Scene 20
visual: manim Boosting: "boosting" as the heading; small trees in a row, each arrow labelled "errors", their sum the prediction (schematic, after forests-and-boosting.qmd img/forest-and-boosting.svg)

Boosting also combines many trees, but in a different way. It adds small trees one
after another. Each new tree is fitted to the errors left by the trees before it, so it
corrects them a little at a time. The prediction is the sum of all the trees.

## Scene 21
visual: manim Counts: error on the validation sites against the number of trees, the forest flat, boosting lowest at 200 and rising; "the number of trees: a hyperparameter for boosting" (page results, forests-and-boosting.qmd#fig-trees)
pause-after: 0.5

More trees never hurt a forest: its validation error stays flat. Boosting is different.
On the validation sites, it does best at 200 trees, then gets worse, as the later trees
fit the noise. So for boosting, the number of trees is a hyperparameter.

## Scene 22
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Flexible models learn the shape themselves, but a hyperparameter sets
how closely they fit, and it is chosen on validation data.

# Choosing between them

## Scene 23
visual: manim Questions: five cards, each with its question as it is asked: the aim, predict or explain; the outcome, what kind; the range, beyond the data; the data, how much; the audience, who must accept it (schematic, after choosing-a-method.qmd img/choosing-a-method.svg)

Finally, how to choose between these methods. Five questions narrow the choice before
any model is fitted. What is the aim: to predict, or to explain? What kind of outcome
is it? Must the model predict beyond the range of the data? How much data is there? And
who must accept the result?

## Scene 24
visual: manim Comparison: "RMSE on the test sites: lower is better"; the seven models' test RMSE as dots, ordered, Poisson regression first and the three tree models last (page results, choosing-a-method.qmd#fig-comparison)

Here, all seven models were scored on the same test sites, with the typical miss:
lower is better. Poisson regression comes first, and the three tree models last. A few
hundred noisy stations are too few for the flexible methods to beat a simple curve.

## Scene 25
visual: manim Comparison: the validation dots added, the tree first there; the tree's and boosting's gaps from validation to test marked "tuned on these sites"; "one split cannot separate close models" (page results, choosing-a-method.qmd#fig-comparison)
pause-after: 0.5

On the validation sites, though, the single tree came first. Its depth, and boosting's
number of trees, were chosen on those same sites, so they were tuned to those sites'
chance patterns: a kind of overfitting. The test sites, kept apart until the end, show
the cost. And one split cannot reliably tell apart models whose scores are close.

## Scene 26
visual: manim Beyond: "extrapolation: predicting beyond the data"; three models from 0 to 22 °C, the shaded ends beyond the data; the forest level, Poisson regression flattening to zero, linear regression falling below it (page results, choosing-a-method.qmd#fig-extrapolate)

The models also differ beyond the data. Predicting outside the range of the data is
called extrapolation. Beyond the sampled temperatures, each model follows its own rule.
The forest stays level, Poisson regression flattens towards zero, and linear regression
falls below zero.

## Scene 27
visual: manim Beyond: "nothing in the data says which is right", "choose an assumption you can defend"
pause-after: 0.5

Nothing in the data says which is right, because there are no data there. So choose a
model whose assumption you can defend, and say what it is.

## Scene 28
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. Start from the question and the outcome, not from the most flexible
method.

# Quiz

## Scene 29
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A colleague models counts of a species with linear regression, and a few
predictions come out below zero. They set those to zero. Is the problem solved?

## Scene 30
visual: manim QuizAnswer: "no"; the negative predictions set to zero, the model beneath unchanged; then Poisson regression, never below zero (schematic)

No. Setting them to zero hides the symptom, but the model still assumes a count can
fall below zero. A count model, such as Poisson regression, cannot make that mistake.

# Key points

## Scene 31
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: match the model to the outcome.

## Scene 32
visual: manim KeyPoints: the second ticked

Two: flexible models learn the shape, but a hyperparameter, chosen on validation data,
sets how closely.

## Scene 33
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: start from the question, not the most flexible method.

## Scene 34
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
