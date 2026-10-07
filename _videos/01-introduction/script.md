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

This video is a short tour of the introduction. It covers three things: the kinds of
learning, why predicting is not the same as explaining, and where machine learning
helps in marine science.

# The survey data

## Scene 2
visual: manim Idea: measurements go into a model, a prediction comes out, for a new case (schematic)

Machine learning fits a model to examples, so that it can make good predictions for
cases it has not seen.

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

When the answer is a quantity, the task is regression. When it is a category, such as
present or absent, it is classification.

## Scene 7
visual: manim Neighbours: the stations by depth and temperature; a new mid-depth station appears, and its 15 nearest stations light up (page results, types-of-learning.qmd)

The simplest supervised method is k-nearest neighbours. For a new station, it finds the
fifteen survey stations most like it in temperature, salinity and depth.

## Scene 8
visual: manim Neighbours: the 15 neighbours coloured found or not found; "11 of 15 found", then "73% chance of presence" (page results, types-of-learning.qmd)
pause-after: 0.5

Eleven of those fifteen had the species, so the model gives a seventy-three percent
chance of presence. To predict abundance, it averages their counts instead.

## Scene 9
visual: manim Clusters: the 800 stations by depth and temperature, sorted into three groups by k-means (page results, types-of-learning.qmd#fig-clusters)

With no answers at all, the learning is unsupervised. Here k-means sorts the stations
into three groups using only the water: shallow, mid-depth and deep.

## Scene 10
visual: manim Always: ask for six groups, and six appear (schematic)

It will return groups whether or not real ones exist, so its results need checking.

## Scene 11
visual: manim Models: a boundary between two groups, "discriminative", and an outline around each, "generative" (schematic)

Models also differ in what they learn. A discriminative model, such as k-nearest
neighbours, learns only the answer. A generative model learns the data themselves, and
can invent new examples. The tools that write text and draw pictures are generative.

## Scene 12
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

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

In the survey, the species does best in middling water. A straight line through that
hump is nearly flat, so a linear regression reports almost no temperature effect.

## Scene 16
visual: manim Hump: the decision tree's steps drawn over it, following the hump
pause-after: 0.5

A decision tree was never asked for a slope, and it finds the hump.

## Scene 17
visual: manim Rmse: the page's first five test stations, observed and the tree's predicted count; then the miss, then its square; "… and 195 more"; the mean of the squares 19.29; its square root 4.39 animals (page results, prediction-and-explanation.qmd)

To compare the two, each one predicts the stations held back. At every station, take
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

A good test error gives no warning of this. Explaining needs a study design and
knowledge of the system, and the course comes back to these ideas as it goes.

## Scene 21
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Predicting and explaining are different jobs. Decide first which one you
want, because they are checked in different ways.

# Machine learning in marine science

## Scene 22
visual: manim Tasks: six cards appear, naming things to standing in for a slow model (schematic)

Most marine applications come down to six tasks: naming things, mapping across space,
filling gaps, forecasting, finding groups, and standing in for a slow model.

## Scene 23
visual: manim Tasks: each card gains a warning mark, "a typical way of going wrong"

Each has a typical way of going wrong, and the course deals with each one later.

## Scene 24
visual: manim Pipeline: plentiful data, a specialist's scarce labels, a model, predictions at scale (schematic)

Most of the six are supervised, and the answers usually come from a specialist: slow
and costly. A model turns those few labels into predictions for everything else.

## Scene 25
visual: manim Pipeline: the labelled few bunched in one corner, "not a random sample"

But the labelled examples are rarely a random sample, and the model inherits their
gaps.

## Scene 26
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

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
visual: manim KeyPoints: the third ticked

Three: most applications are one of six tasks, limited by their labels.

## Scene 32
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
