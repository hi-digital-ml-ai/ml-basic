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
frees a model from straight lines, but not from the way the data were collected. Three
ideas, one example and one picture each, and few numbers: what an assumption is (a
straight line against a forest's steps), a model guessing where its survey never went
(cold, shallow winter water), and a rare answer that fools accuracy (95 per cent
accurate, finding nothing). Every term is introduced before it is used. The spread of
counts, repeat visits, the distance check and rebalancing are left to the pages; the
end card names some of them.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about
assumptions and their limits. It covers three things: what machine learning frees a
model from, what it does not free it from, and why a rare answer fools accuracy.

# Machine learning frees a model from straight lines

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
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. Machine learning frees a model from straight lines: it can find the
shape in the data on its own.

# But not from how the data were collected

## Scene 6
visual: manim Learns: a model and the stations it was given, "it can only learn from these"; then ports, weather and ship time pulling the stations together (schematic)

Next, what it does not free a model from. However flexible, a model can only learn
from the stations it was given. And survey effort is never even: it follows ports,
weather and ship time.

## Scene 7
visual: manim Novelty: temperature against depth for the summer and autumn survey, cold water only at depth (page results, sampling-and-extrapolation.qmd#fig-novelty)

Here is a survey that sailed only in summer and autumn. Each dot is a station, placed
by its depth and its temperature. In those seasons the shallows are warm, so the survey
met cold water only at depth.

## Scene 8
visual: manim Novelty: winter stations appear, cold and shallow; "depth: seen", "temperature: seen", "together: never" (page results)

In winter, the shallows turn cold. Each winter station's depth was seen in the survey,
and so was its temperature, but never the two together. The model has no stations like
these to learn from.

## Scene 9
visual: manim Novelty: the winter stations ringed, "the model still answers, just as sure"; "extrapolation: predicting beyond the data" (page results)

It still gives an answer, and the answer looks just as sure as any other. As in the
Supervised learning video, predicting beyond the data is called extrapolation. On the
page, the forest's errors grew the further a station lay from the survey.

## Scene 10
visual: manim Novelty: "before trusting a prediction, ask: did the survey see conditions like these?" (page results)

So before trusting a prediction, ask one question: did the survey see conditions like
these? The page shows a simple way to measure it.

## Scene 11
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Machine learning does not free a model from how the data were
collected: where the survey never went, the model is guessing.

# A rare answer fools accuracy

## Scene 12
visual: manim Rare: 598 training stations as dots, the 29 with a rare species lit up; "4.8%" (page results, class-imbalance.qmd)

Finally, why a rare answer fools accuracy. Many things marine scientists most want to
predict are rare: a protected species, a harmful algal bloom. Here a second species
turns up at only 29 of 598 stations, about 5 per cent.

## Scene 13
visual: manim Trap: logistic regression, threshold 0.5; "presences found: 0"; "accuracy: 95%", "the share of calls that are right" (page results, class-imbalance.qmd)

Logistic regression gives each station a probability of presence, and, as in the
Supervised learning video, a threshold of 0.5 turns it into a call. Here it finds none
of the presences. Yet its accuracy, the share of its calls that are right, is 95 per
cent. Calling the species absent everywhere is right almost everywhere.

## Scene 14
visual: manim Sensitivity: "sensitivity: of the stations with the species, the share called present"; 0 at the threshold of 0.5 (page results)

So count what the model finds. Sensitivity is the share of the stations with the
species that the model calls present. Here it is 0: the 95 per cent hid a model that
finds nothing.

## Scene 15
visual: manim Sensitivity: the threshold lowered; sensitivity about 0.7; more false alarms; "the threshold: set by what each mistake costs" (page results)

Lower the threshold, and the model finds about 7 in 10 of them. The price is more false
alarms: stations without the species called present. Where to set the threshold depends
on what each mistake costs.

## Scene 16
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. A rare answer fools accuracy: count what the model finds, not just
how often it is right.

# Quiz

## Scene 17
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A harmful algal bloom occurs on 2 days in 100. A model that warns of blooms
is 98 per cent accurate. Is it a good model?

## Scene 18
visual: manim QuizAnswer: "You can't tell yet"; a hundred days, two with a bloom; a model that never warns: 98% accurate, blooms caught: 0; "ask for its sensitivity" (schematic)

You can't tell yet. A model that never warns is also 98 per cent accurate, and it
misses every bloom. Ask for its sensitivity: how many of the blooms it catches.

# Key points

## Scene 19
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: machine learning frees a model from
straight lines.

## Scene 20
visual: manim KeyPoints: the second ticked

Two: it does not free a model from how the data were collected.

## Scene 21
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: a rare answer fools accuracy.

## Scene 22
visual: manim EndCard: the site's address and a thank-you

The pages go further: repeat visits to the same sites, what a model assumes about the
spread of counts, how to measure how far a station lies from the survey, and how to
handle a rare answer, with all the code. They are linked below. Thanks for watching.
