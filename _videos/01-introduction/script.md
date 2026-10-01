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
learning, how machine learning relates to the statistics you already use, and where it
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
visual: manim Clusters: the 800 stations by depth and temperature, sorted into three groups by k-means (page results, types-of-learning.qmd#fig-clusters)

With no answers at all, the learning is unsupervised. Here k-means sorts the stations
into three groups using only the water: shallow, mid-depth and deep.

## Scene 8
visual: manim Always: ask for six groups, and six appear (schematic)

It will return groups whether or not real ones exist, so its results need checking.

## Scene 9
visual: manim Models: a boundary between two groups, "discriminative", and an outline around each, "generative" (schematic)

Models also differ in what they learn. A discriminative model learns only the line
between outcomes. A generative model learns the data themselves, and can invent new
examples. The tools that write text and draw pictures are generative.

## Scene 10
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. The data you hold decide the kind of learning: supervised with answers,
unsupervised without them.

# Statistics and machine learning

## Scene 11
visual: manim Scale: methods from "you write the shape down" to "the algorithm finds it", linear regression "used by both" (schematic)

Machine learning is not a separate subject from statistics. The two share their data
and their models, and linear regression belongs to both.

## Scene 12
visual: manim Aims: "estimate an effect" and "predict new cases, checked on data held back" (schematic)

The difference is mostly the aim. A statistical model estimates an effect. A
machine-learning model predicts new cases, and is checked on data held back from
fitting.

## Scene 13
visual: manim Hump: abundance against temperature, the straight line nearly flat (page results, what-is-machine-learning.qmd#fig-shapes)

In the survey, the species does best in middling water. A straight line through that
hump is nearly flat, so the linear model reports no temperature effect.

## Scene 14
visual: manim Hump: the decision tree's steps drawn over it, following the hump
pause-after: 0.5

A decision tree was never asked for a slope, and it finds the hump.

## Scene 15
visual: manim Rmse: the page's first five test stations, observed and the tree's predicted count; then the miss, then its square; "… and 195 more"; the mean of the squares 19.29; its square root 4.39 animals (page results, what-is-machine-learning.qmd)

To compare the two, each one predicts the stations held back. At every station, take
the miss: the observed count minus the predicted one. Square the misses, so that none
cancel out, average them, and take the square root. This is the root mean squared
error, or RMSE: a typical miss, in animals.

## Scene 16
visual: manim Scores: three bars, predicting the average 4.72, the straight line 4.59, the tree 4.39; "lower is better" (page results, what-is-machine-learning.qmd)
pause-after: 0.5

Lower is better. The tree's RMSE is 4.39 animals, the straight line's 4.59. Simply
predicting the average count everywhere gives 4.72, so both models have learned
something, if not much. The course scores predictions this way throughout.

## Scene 17
visual: manim Cause: depth drives both salinity and the species; a dashed line from salinity to the species, "helps predict", then "but causes nothing" (schematic)

Predicting and explaining are different jobs, too. A variable can help predict without
causing anything. In the survey, salinity helps predict the species, but only because
it rises with depth, and depth is what the species responds to.

## Scene 18
visual: manim Cause: "a good test error gives no warning", "explaining needs a study design and knowledge of the system", "more on this later in the course"
pause-after: 0.5

A good test error gives no warning of this. Explaining needs a study design and
knowledge of the system, and the course comes back to these ideas as it goes.

## Scene 19
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Statistics and machine learning share their models. Decide first
whether you want to predict or to explain.

# Machine learning in marine science

## Scene 20
visual: manim Tasks: six cards appear, naming things to standing in for a slow model (schematic)

Most marine applications come down to six tasks: naming things, mapping across space,
filling gaps, forecasting, finding groups, and standing in for a slow model.

## Scene 21
visual: manim Tasks: each card gains a warning mark, "a typical way of going wrong"

Each has a typical way of going wrong, and later sections deal with each one.

## Scene 22
visual: manim Pipeline: plentiful data, a specialist's scarce labels, a model, predictions at scale (schematic)

Most of the six are supervised, and the answers usually come from a specialist: slow
and costly. A model turns those few labels into predictions for everything else.

## Scene 23
visual: manim Pipeline: the labelled few bunched in one corner, "not a random sample"

But the labelled examples are rarely a random sample, and the model inherits their
gaps.

## Scene 24
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Place your problem among the six tasks, and look hard at where its
labels came from.

# Quiz

## Scene 25
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. You have a folder of seabed photographs, and a specialist has named the
species in some of them. Supervised or unsupervised? And which of the six tasks?

## Scene 26
visual: manim QuizAnswer: the named photos marked "supervised", and the "naming things" card (schematic)

Supervised, because some photographs come with answers. The task is naming things: a
classification.

# Key points

## Scene 27
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: your data decide the kind of learning.

## Scene 28
visual: manim KeyPoints: the second ticked

Two: decide whether you want to predict or to explain.

## Scene 29
visual: manim KeyPoints: the third ticked

Three: most applications are one of six tasks, limited by their labels.

## Scene 30
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
