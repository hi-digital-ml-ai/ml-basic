---
title: "Introduction: what is machine learning for?"
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
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. What machine learning is actually for.
Why the best predictor can be the worst explanation. And how your data decide which
questions you can ask.

# The puzzle

## Scene 2
visual: manim Survey: a map of 800 simulated coastal stations, "how does temperature affect abundance?" (page results, what-is-machine-learning.qmd)

Here is a survey of 800 coastal stations, and one question: how does temperature
affect the abundance of a seabed species?

## Scene 3
visual: manim Coefficients: the linear model's estimates and intervals, chlorophyll clear, depth weak (page results)

Fit a linear model, as you normally would. Chlorophyll has a clear positive association.
Depth declines, weakly.

## Scene 4
visual: manim Coefficients: temperature highlighted, −0.074 per degree, p = 0.31, its interval spanning zero, "no effect"

And temperature? About minus 0.07 per degree, with a p value of 0.31. You would report
no temperature effect.

## Scene 5
visual: manim Coefficients: "the species peaks at 9 °C" over the table, and a question mark
pause-after: 1.5

But this survey is simulated, and we wrote the species to peak at 9 degrees. So what
went wrong?

# Two ways to fit the same data

## Scene 6
visual: manim Split: 600 training stations and 200 held back, the held-back part locked (page results)

Start by splitting the data: 600 stations to train on, and 200 held back, not looked
at until the end.

## Scene 7
visual: manim Statement: "you choose the form", a straight line, a coefficient with its interval (schematic)

A statistical model estimates something about the world. You choose the form, and it
returns a number with an interval: a statement you can put in a paper.

## Scene 8
visual: manim Machine: a station's measurements go into a box, a prediction comes out (schematic)

A machine-learning model is built to predict cases it has not seen. It searches for
whatever shape fits, and returns a machine.

## Scene 9
visual: manim Forest: 500 small trees, "no coefficients to print" (schematic)

Here, a random forest of 500 trees. There are no coefficients to print, only
predictions.

## Scene 10
visual: manim Hump: abundance against temperature in the 600 training stations (page results, what-is-machine-learning.qmd#fig-temperature)

So look at the data. Abundance rises to a peak around 9 degrees, then falls away.

## Scene 11
visual: manim Hump: the best straight line through it, nearly flat, "its line is wrong"

The linear model had to answer with a single slope. The best straight line through a
hump is flat.

## Scene 12
visual: manim Hump: the flexible curve drawn over it, following the hump
pause-after: 0.5

The forest was never asked for a slope, so the hump costs it nothing.

## Scene 13
visual: manim Errors: typical error on the training stations, forest 2.09 against linear 4.35 (page results)

So does it predict better? On the training stations, the forest's typical error is
2.09. The linear model's is 4.35.

## Scene 14
visual: manim Errors: the 200 held-back stations added, 4.13 against 4.22

On the 200 held-back stations, the gap almost vanishes: 4.13 against 4.22.

## Scene 15
visual: manim Errors: the forest's training bar marked "memorised", the test set "the honesty check"

Most of the forest's advantage was memory of the stations it trained on. That is
overfitting, and only the held-back data caught it.

## Scene 16
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. A statistical model estimates something about the world. A
machine-learning model builds something that predicts, and only data it never saw can
check it.

# The puzzle, solved

## Scene 17
visual: manim Goals: "prediction: what will the value be?" and "explanation: how much does this driver matter?" (schematic)

That comparison hides a choice. Prediction asks what the value will be. Explanation
asks how a driver affects it, and by how much.

## Scene 18
visual: manim Four: four models' test errors as bars, the linear model at 4.22, the forest at 4.13 (page results, prediction-and-explanation.qmd)

So fit four models on the same data, and score each on the held-back stations.

## Scene 19
visual: manim Four: the linear model with curves at 4.01, better than the forest

A linear model allowed to curve scores 4.01, better than the forest. It took one piece
of ecology: species have optima, so let the line bend.

## Scene 20
visual: manim Optimum: the curved model's temperature response, fitted peak 8.6 °C, true 9 °C (page results, prediction-and-explanation.qmd#fig-optimum)

Its temperature curve peaks at 8.6 degrees. The truth is 9.

## Scene 21
visual: manim Optimum: "no effect" struck out, "an effect the model could not draw" ticked
pause-after: 0.5

So "no temperature effect" was never a fact about the species. It was a fact about a
model that could only draw straight lines.

## Scene 22
visual: manim Optimum: the curve's ends, below zero, marked "impossible"

Even so, look at its ends. Below zero: fewer than no animals. Sound in the centre,
nonsense at the edges.

## Scene 23
visual: manim Four: the forest with longitude and latitude, the best at 3.98

And the best predictor? The forest, with longitude and latitude added: 3.98.

## Scene 24
visual: manim Proxy: "no fish responds to longitude", the coordinates standing in for "where the good patches were" (schematic)

No fish responds to longitude. The coordinates are a proxy: the model learned where
the good patches were during this survey.

## Scene 25
visual: manim Table: the four models, "predicts" and "explains" marked for each (page results)

The best predictor explains nothing. The best explanation is nearly the best predictor.

## Scene 26
visual: manim Check: prediction checked against held-back data; explanation with no such check (schematic)

And only prediction can be checked by holding data back. A good test score is not
evidence that the effects are real.

## Scene 27
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Decide whether you want prediction or explanation before choosing a
method. They pull a model in different directions.

# What your data let you ask

## Scene 28
visual: manim Types: a table with an answer column, "supervised", and one without, "unsupervised" (schematic)

The next question is forced by your data. If each row has a known answer, the learning
is supervised. If not, it is unsupervised.

## Scene 29
visual: manim Types: the answer a number, "regression", or a category, "classification" (schematic)

Supervised learning splits by the answer. A quantity is regression. A category, like
present or absent, is classification.

## Scene 30
visual: manim Accuracy: a forest classifying presence, 79% accurate (page results, types-of-learning.qmd)

So classify whether the species is present. The forest is 79% accurate. That sounds
respectable.

## Scene 31
visual: manim Accuracy: "always say present" beside it, 78%

Now always answer "present", ignoring every measurement. That scores 78%.

## Scene 32
visual: manim Absent: the 45 absent stations, the 11 the forest caught (page results)

Of 45 stations where it was absent, the forest caught 11. As a map of where the
species is not, it is close to useless.

## Scene 33
visual: manim Absent: "compare with always guessing the common answer"
pause-after: 0.5

So always compare accuracy with always guessing the common answer.

## Scene 34
visual: manim Clusters: 800 stations with no answer column, sorted into three groups by k-means (page results, types-of-learning.qmd#fig-clusters)

Now remove the answer entirely. Ask k-means, an unsupervised method, to sort the 800
stations into three groups, using only the water.

## Scene 35
visual: manim Clusters: the three groups named deep and cold, shallow and warm, shallow and productive

It finds three recognisable habitats: deep and cold, shallow and warm, and shallow and
productive.

## Scene 36
visual: manim Clusters: mean abundance per group, 7.94 in the productive group against 4.25 and 2.86

It never saw abundance. Yet the productive group averages 7.94 animals, against 4.25
and 2.86.

## Scene 37
visual: manim Always: ask for six groups, and six appear (schematic)

But ask for six groups and you get six, just as confident. Unsupervised methods always
return groups.

## Scene 38
visual: manim Machines: supervised and unsupervised as the question, a forest and a network as interchangeable machines (schematic)

And neural networks? They are not a third kind of learning. They are a machine, one
choice among many, for either kind.

## Scene 39
visual: manim Pipeline: abundant data, a specialist's scarce labels, a model that scales them up (schematic)

In marine science the answers are usually a specialist's labels: slow and costly. A
model spends that judgement once and applies it a million times.

## Scene 40
visual: manim Pipeline: the labelled subset, "not a random sample"

But the labelled part is rarely a random sample. Whatever it over-represents, the
model applies everywhere.

## Scene 41
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Your data decide the question. Labelled or not comes first; the
machine comes second.

# Quiz

## Scene 42
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. You have a folder of seabed photographs, and none is labelled. Supervised
or unsupervised? And does choosing a neural network change that?

## Scene 43
visual: manim QuizAnswer: unlabelled photos, "unsupervised", a network swapped in without changing it (schematic)

Unsupervised, because nothing is labelled. A network is only a machine: it cannot
change what your data let you ask.

# Key points

## Scene 44
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: machine learning is built to
predict.

## Scene 45
visual: manim KeyPoints: the second ticked

Two: the best predictor is not the best explanation.

## Scene 46
visual: manim KeyPoints: the third ticked

Three: your data decide the question.

## Scene 47
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
