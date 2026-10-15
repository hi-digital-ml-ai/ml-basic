---
title: "Introduction: a map of machine learning"
section: chapters/01-introduction/index.qmd
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

This video is an overview: it introduces the section and says what its pages cover,
without teaching each page in full.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome to Machine Learning Basics for Marine Science. This first video is a short
tour of the introduction. It covers three things: the kinds of learning, why predicting
is not the same as explaining, and where machine learning helps in marine science.

# The survey data

## Scene 2
visual: manim Idea: a model trained on examples; new data go in, a prediction comes out; then "this course: build models well, avoid the pitfalls" (schematic)

Let's start with the basic idea. Machine learning trains a model on examples whose
answers we already know. Once trained, the model takes new data as its input, such as
the temperature, salinity and depth at a new station. Its output is a prediction for
that station. In this course, we learn how to build these models well, and in the right
way, so that we avoid the many pitfalls along the way.

## Scene 3
visual: manim Survey: "one simulated marine dataset, used throughout the course", then the first five stations of the survey, each column appearing with a short gloss as it is named (page results, types-of-learning.qmd)

Throughout this course, we use one simulated marine dataset again and again. It is a
survey of 800 stations on a coastal shelf. Each station records
the water's temperature, its salinity, which is how salty it is, and its depth. Then
comes one seabed species: its abundance, the number of animals counted, and whether it
was present at all.

## Scene 4
visual: manim Survey: "simulated: the true relationships are known"
pause-after: 0.5

Because we wrote the simulation, we know the true answers,
and can check whether a model finds them. The next section of the course looks at marine
data more closely.

# Kinds of learning

## Scene 5
visual: manim Supervised: the table with its answer column highlighted, "supervised" (page results)

If every example comes with an answer, such as whether the species was found, the
learning is supervised.

## Scene 6
visual: manim Supervised: the answer a quantity, "regression", or a category, "classification" (schematic)

In supervised learning, when the answer is a quantity, such as the number of animals
counted, the task is regression. When it is a category, such as present or absent, it is
classification.

## Scene 7
visual: manim Neighbours: the stations by depth and temperature; a new mid-depth station appears, always drawn on top, and its 15 nearest stations light up (page results, types-of-learning.qmd)

Let's look at one of the simplest supervised methods, k-nearest neighbours. Here, its
aim is to predict whether the species is present at a new station, marked by the star,
where nobody has looked yet. It does this from the neighbours: the fifteen survey
stations most like the new one in temperature, salinity and depth. Nearest means most
similar in the water, not closest on a map. The neighbours come with answers, so they
tell us what to expect at the new station.

## Scene 8
visual: manim Neighbours: the 15 neighbours coloured found or not found; "11 of 15 found", then "73% chance of presence"; "present or absent: a classification", then "above a cut-off: yes or no"; "abundance: their average count, a regression" (page results, types-of-learning.qmd)
pause-after: 0.5

Eleven of those fifteen neighbours had the species. So the model predicts a seventy-three
percent chance of presence: a kind of confidence that the species is there. The more
neighbours with the species, the higher the value. This is a classification, because
the answer is a category: present or absent. To get a plain yes or no, choose a cut-off,
and call the species present above it. The same method can also do regression: to
predict abundance, it averages the neighbours' counts instead.

## Scene 9
visual: manim Clusters: "k-nearest neighbours: supervised", "k-means: unsupervised"; then the 800 stations by depth and temperature, sorted into three groups by k-means (page results, types-of-learning.qmd#fig-clusters)

Now for unsupervised learning, where the examples have no answers at all. Instead of
predicting an answer, the aim is to find groups of similar examples. A common method is
k-means. Its name sounds like k-nearest neighbours, but they do different jobs:
k-nearest neighbours is supervised, while k-means is unsupervised. In this example,
k-means sorted all 800 stations into three groups, using only the water's temperature,
salinity and depth. Looking at the groups afterwards, we named them shallow, mid-depth
and deep.

## Scene 10
visual: manim Always: "k = the number of groups: we choose it"; ask for three, then for six, and six appear (schematic)

Unsupervised learning often needs extra information from us. The k in k-means is the
number of groups, and we chose three, but the best number is usually unknown. k-means
returns as many groups as we ask for, whether or not real ones exist: ask for six, and
six appear. So its results need checking.

## Scene 11
visual: manim Models: "not how a model learns, but what it produces"; a boundary between two groups, "discriminative", and an outline around each, "generative"; "this course: mostly discriminative" (schematic)

Models also differ in another way. This is not about how a model learns, but about what
it produces. A discriminative model, such as k-nearest neighbours, learns only the
answer: here, the boundary between stations with and without the species. A generative
model learns what the data themselves look like, so it can invent new examples. The
tools that write text and draw pictures are generative. This basic course focuses mostly
on discriminative models.

## Scene 12
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. The data you hold decide the kind of learning: supervised with answers,
unsupervised without them.

# Predicting and explaining

## Scene 13
visual: manim Aims: "prediction: the outcome at a new station, checked on stations held back" and "explanation: what drives the outcome" (schematic)

A model can serve two aims. Prediction asks what the outcome will be at a station
nobody has measured, and it can be checked on stations held back from fitting.
Explanation asks what drives the outcome.

## Scene 14
visual: manim Aims: "machine learning" under prediction, "statistical modelling" under explanation (schematic)

Machine learning usually aims at prediction, and statistical modelling at explanation.
The same model can serve either, but it is checked in different ways.

## Scene 15
visual: manim Hump: abundance against temperature, the straight line nearly flat (page results, prediction-and-explanation.qmd#fig-shapes)

Here is an example of how predictions are evaluated, using two models. In the survey,
the species does best in middling water, neither too cold nor too warm. The first model,
a linear regression, fits a straight line. Through that hump, the line is nearly flat,
so it reports almost no temperature effect.

## Scene 16
visual: manim Hump: the decision tree's steps drawn over it, following the hump; then "decision tree: a supervised model, explained later in the course"
pause-after: 0.5

The second model, a decision tree, works differently. It splits the stations in two, at
the value that best separates high counts from low ones, then splits each part again.
Each final part predicts its average count. It was never asked for a straight line, and
it finds the hump. Like k-nearest neighbours, a decision tree is a supervised model: it
learns from stations whose counts are known. We learn how decision trees work later in
the course, in the section on supervised learning.

## Scene 17
visual: manim Rmse: the page's first five test stations, observed and the tree's predicted count; then the miss, then its square; "… and 195 more"; the mean of the squares 19.29; its square root 4.39 animals (page results, prediction-and-explanation.qmd)

To compare the two, each one predicts stations that were held back, so the models never
saw them while they were trained. At every station, take
the miss: the observed count minus the predicted one. Square the misses, so that none
cancel out, average them, and take the square root. This is the root mean squared
error, or RMSE: a typical miss, in animals.

## Scene 18
visual: manim Scores: three bars, the baseline of predicting the average 4.72, linear regression 4.59, the decision tree 4.39; "lower is better" (page results, prediction-and-explanation.qmd)
pause-after: 0.5

Lower is better. The tree's RMSE is 4.39 animals, the linear regression's 4.59. Simply
predicting the average count everywhere, the baseline, gives 4.72, so both models have
learned something, if not much. The course scores predictions this way throughout.

## Scene 19
visual: manim Cause: depth drives both salinity and the species; a dashed line from salinity to the species, "helps predict", then "but causes nothing" (schematic)

Predicting and explaining are different jobs, too. A variable can help predict without
causing anything. In the survey, salinity helps predict the species, but only because
it rises with depth, and depth is what the species responds to.

## Scene 20
visual: manim Cause: "a good test error gives no warning", "explaining needs a study design and knowledge of the system", "more on this later in the course"
pause-after: 0.5

A good score on held-back stations gives no warning of this. Explaining needs a study design and
knowledge of the system, and the course comes back to these ideas as it goes.

## Scene 21
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Predicting and explaining are different jobs. Decide first which one you
want, because they are checked in different ways.

# Machine learning in marine science

## Scene 22
visual: manim Tasks: six cards appear, naming things to standing in for a slow model (schematic)

Most marine applications come down to six tasks: naming things, mapping across space,
filling gaps, forecasting, finding groups, and standing in for a slow model. Each task
tends to have its own suitable ways of building models, using supervised learning,
unsupervised learning, or both.

## Scene 23
visual: manim Tasks: each card gains a warning mark, "a typical way of going wrong"

Each has a typical way of going wrong, and the course deals with each one later.

## Scene 24
visual: manim Pipeline: plentiful data, a specialist's scarce labels, a model, predictions at scale (schematic)

Most of the six are supervised, so they need answers, which machine learning calls
labels. The labels usually come from a specialist, which is slow and costly. A model
trained on those few labels can then predict for everything else.

## Scene 25
visual: manim Pipeline: the labelled few bunched in one corner, "not a random sample"

But the labelled examples are rarely a random sample, and the model inherits their
gaps.

## Scene 26
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. Place your problem among the six tasks, and look hard at where its
labels came from.

# Quiz

## Scene 27
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. You have a folder of seabed photographs, and a specialist has named the
species in some of them. Supervised or unsupervised? And which of the six tasks?

## Scene 28
visual: manim QuizAnswer: the named photos marked "supervised", and the "naming things" card (schematic)

Supervised, because some photographs come with answers. The task is naming things: a
classification.

# Key points

## Scene 29
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: your data decide the kind of learning.

## Scene 30
visual: manim KeyPoints: the second ticked

Two: decide whether you want to predict or to explain.

## Scene 31
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: most applications are one of six tasks, limited by their labels.

## Scene 32
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
