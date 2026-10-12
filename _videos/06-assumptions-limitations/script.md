---
title: "Assumptions: what a good score cannot show"
section: chapters/06-assumptions-limitations/index.qmd
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

A gentle introduction to the section, following its overview page: machine learning
frees a model from straight lines and bell curves, but not from the way the data were
collected. Three ideas, a simple picture for each concept, and few numbers: what an
assumption is (a straight line against a forest's steps, then skewed counts and a
forest's lopsided errors), how the data were collected (repeat visits worth fewer
stations, and cold, shallow winter water a summer survey never met), and a rare answer
that fools accuracy (95 per cent accurate, finding nothing). Every term is introduced
before it is used. Performance measures such as sensitivity belong to the Validation
section and are not named here. Log counts, resampling, the distance check and
rebalancing are left to the pages; the end card names some of them.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about
assumptions and their limits. It covers three things: what machine learning frees a
model from, what it does not free it from, and why a rare answer fools accuracy.

# Machine learning frees a model from straight lines and bell curves

## Scene 2
visual: manim Assumption: "an assumption: something a method takes for granted about its data"; a model still answers when it is wrong (schematic)

First, what machine learning frees a model from. Every method takes something for
granted about its data. That is called an assumption. When an assumption is wrong, the
model still gives an answer, but the answer can be wrong.

## Scene 3
visual: manim Shapes: animals against temperature with a hump; a straight line through it, crossed out (schematic)

Take linear regression. It assumes a straight line: each extra degree of temperature
always adds the same number of animals. But a species often has a temperature it
prefers, with fewer animals in colder and in warmer water. A straight line cannot draw
that hump.

## Scene 4
visual: manim Shapes: a random forest follows the hump in steps; "no shape chosen in advance" (schematic)

A random forest does not assume a shape. Its trees split the stations into groups by
temperature, so it follows the data in steps, and finds the hump on its own. This is
what people mean when they call machine learning flexible.

## Scene 5
visual: manim Checks: two boxes, "errors: a bell curve" and "equal spread everywhere"; "taught in statistics courses" (schematic)

Statistics courses teach another assumption, about a model's errors: the gaps between
what was caught and what was predicted. The errors should follow a bell curve, the
Normal distribution, and spread evenly everywhere.

## Scene 6
visual: manim Counts: a histogram of the 598 training stations' catches; 129 at zero, the median 3, the largest 40; "a long tail of big catches" (page results, distributional-assumptions.qmd)

Survey counts do not behave like that. Of 598 stations, 129 caught nothing, the middle
station caught 3, and the largest 40. Most catches are small, with a long tail of big
ones.

## Scene 7
visual: manim Errors: the random forest's errors against its predictions, lopsided and fanning out; "the forest predicts well anyway" (page results, distributional-assumptions.qmd#fig-errors)

So a random forest's errors are lopsided, and they spread wider where it predicts more.
Yet the forest predicts well. A tree predicts the average catch of similar stations,
and an average needs no bell curve.

## Scene 8
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. Machine learning frees a model from straight lines and bell curves: it
can find the shape in the data on its own.

# But not from how the data were collected

## Scene 9
visual: manim Learns: a model and the stations it was given, "it can only learn from these" (schematic)

Next, what it does not free a model from: how the data were collected. However
flexible, a model can only learn from the stations it was given, so how they were
gathered matters.

## Scene 10
visual: manim Visits: 800 stations as squares, which gather into 160 sites; one site's visits highlighted, "same depth, same seabed, same water" (page results, dependent-data.qmd)

This survey's 800 stations come from only 160 sites, visited again and again. As the
Marine data video showed, visits to one site share its depth, its seabed and its water,
so they partly repeat each other.

## Scene 11
visual: manim Worth: the 800 squares, about 470 of them kept bright: "worth about 470 independent stations"; "counted as 800: looks surer than it is" (page results, dependent-data.qmd)

The page measures how much. The 800 stations carry about as much information as 470
independent ones. Count them as 800, and a model's results look surer than they are.

## Scene 12
visual: manim Novelty: temperature against depth for the summer and autumn survey, cold water only at depth (page results, sampling-and-extrapolation.qmd#fig-novelty)

Survey effort is uneven too: it follows ports, weather and ship time. Here is a survey
that sailed only in summer and autumn. Each dot is a station, placed by its depth and
its temperature. In those seasons the shallows are warm, so the survey
met cold water only at depth.

## Scene 13
visual: manim Novelty: winter stations appear, cold and shallow; "depth: seen", "temperature: seen", "together: never" (page results)

In winter, the shallows turn cold. Each winter station's depth was seen in the survey,
and so was its temperature, but never the two together. The model has no stations like
these to learn from.

## Scene 14
visual: manim Novelty: the winter stations ringed, "the model still answers, just as sure"; "extrapolation: predicting beyond the data" (page results)

It still gives an answer, and the answer looks just as sure as any other. As in the
Supervised learning video, predicting beyond the data is called extrapolation. On the
page, the forest's errors grew the further a station lay from the survey.

## Scene 15
visual: manim Novelty: "before trusting a prediction, ask: did the survey see conditions like these?" (page results)

So before trusting a prediction, ask one question: did the survey see conditions like
these? The page shows a simple way to measure it.

## Scene 16
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Machine learning does not free a model from how the data were
collected: repeat visits count for less, and where the survey never went, the model is
guessing.

# A rare answer fools accuracy

## Scene 17
visual: manim Rare: 598 training stations as dots, the 29 with a rare species lit up; "4.8%" (page results, class-imbalance.qmd)

Finally, why a rare answer fools accuracy. Many things marine scientists most want to
predict are rare: a protected species, a harmful algal bloom. Here a second species
turns up at only 29 of 598 stations, about 5 per cent.

## Scene 18
visual: manim Trap: logistic regression, threshold 0.5; "presences found: 0"; "accuracy: 95%", "the share of calls that are right" (page results, class-imbalance.qmd)

Logistic regression gives each station a probability of presence, and, as in the
Supervised learning video, a threshold of 0.5 turns it into a call. Here it finds none
of the presences. Yet its accuracy, the share of its calls that are right, is 95 per
cent. Calling the species absent everywhere is right almost everywhere.

## Scene 19
visual: manim Check: the 29 presences ringed, "how many of these does it find?"; "measuring it: the Validation section" (page results)

So check how many of the rare cases a model finds, not just how often it is right. The
Validation section shows how to measure that.

## Scene 20
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. A rare answer fools accuracy: check how many of the rare cases the
model finds, not just how often it is right.

# Quiz

## Scene 21
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A harmful algal bloom occurs on 2 days in 100. A model that warns of blooms
is 98 per cent accurate. Is it a good model?

## Scene 22
visual: manim QuizAnswer: "You can't tell yet"; a hundred days, two with a bloom; a model that never warns: 98% accurate, blooms caught: 0; "ask how many blooms it catches" (schematic)

You can't tell yet. A model that never warns is also 98 per cent accurate, and it
misses every bloom. Ask how many of the blooms it catches.

# Key points

## Scene 23
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: machine learning frees a model from
straight lines and bell curves.

## Scene 24
visual: manim KeyPoints: the second ticked

Two: it does not free a model from how the data were collected.

## Scene 25
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: a rare answer fools accuracy.

## Scene 26
visual: manim EndCard: the site's address and a thank-you

The pages go further: how to measure what repeat visits are worth, how far a station
lies from the survey, and what to do about a rare answer, with all the code. They are linked below. Thanks for watching.
