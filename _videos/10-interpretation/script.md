---
title: "Interpretation: reading a model after it is built"
section: chapters/10-interpretation/index.qmd
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

Rebuilt 2026-10-14 with the section's pages, as an introduction like the Assumptions,
Validation, Unsupervised learning and Neural networks videos: one new concept per
part, each with one example and one picture, and plain imperative key points used for
the opening, the cards and the recap (RECAP = PROMISES). The three parts are
permutation importance, partial dependence and SHAP values, all on the same random
forest and split. No cross-validation, splits, score ranges or intervals: the earlier
videos taught them. Inputs that share information get the quiz. The first draft's SHAP
part skipped the basics; it now says what the values do for one station, what the name
stands for, and how to use them, and leaves out the averaging over orders. ICE curves,
the GAM, the surrogate tree and the model card stay on the pages; the end card names
them.
The shuffle schematic names its columns and rows, and shuffles one input at a time.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about reading
a model once it is built, to see what it learned from the data. It covers three things:
shuffling each input in turn, drawing each input's effect, and splitting one
prediction into parts.

# Shuffle each input in turn

## Scene 2
visual: manim Forest: a linear model's coefficients, one bar per input, beside a random forest of many small trees with a question mark (schematic)

First, shuffling each input in turn. Linear regression shows what it learned through
its coefficients: one number for each input. A random forest averages hundreds of
trees, each asking its own questions, so it has no such numbers to read.

## Scene 3
visual: manim Shuffle: a table of the test stations, one row per station, with columns depth, temperature, salinity and count; the error on them; then the temperature column outlined and its values shuffled between rows, the other columns unmoved (schematic)

Yet any model can be read from outside. Take the test stations, which the model never
saw while learning. Each row is one station: its inputs, and the count recorded there.
Score the model's predictions against those counts. Then take one input, say
temperature, and shuffle its column, so each station gets another station's
temperature. The other columns stay as they were, so any change comes from temperature
alone.

## Scene 4
visual: manim Shuffle: the error after shuffling beside the error before, the rise marked "temperature's importance"; temperature put back, then depth's column shuffled, then salinity's; "each many times, the rises averaged" (schematic)

Score the model again. If it relied on temperature, its predictions get worse, and the
error rises. That rise is temperature's importance, called permutation importance. Then
put temperature back, and do the same with depth, then salinity: one input at a time.
Shuffling is random, so each input is shuffled many times and the rises are averaged.

## Scene 5
visual: manim Importance: "typical miss on the test stations: 3.93 animals"; then each input's rise as a bar, temperature first at 0.34, depth next at 0.10, chlorophyll and salinity near zero (page results, feature-importance.qmd)

On the survey, a random forest predicts the count of one species at each station. On
the test stations its typical miss, the RMSE, is 3.93 animals. Shuffle temperature, and
that miss grows by 0.34: more than three times as much as for depth, the next input.
Shuffle chlorophyll or salinity, and it hardly moves.

## Scene 6
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. Shuffle each input in turn: the more the error rises, the more the model
relies on that input.

# Draw each input's effect

## Scene 7
visual: manim Direction: temperature's importance bar; then "which way?" with a rising and a falling arrow (schematic)

Next, drawing each input's effect. Importance says how much the forest relies on
temperature, but not which way. Does the count rise in warmer water, or fall?

## Scene 8
visual: manim Sweep: every station given the same temperature, their predictions drawn as dots on a vertical line; the dots gather into their average, one point (schematic)

To find out, ask the forest a what-if question. Take every station it learned from,
and give them all the same temperature, keeping their other inputs as they were. The
forest predicts each station's count, and the predictions are averaged into one point.

## Scene 9
visual: manim Sweep: the line moves to warmer values, a point at each; the points joined into a curve, "partial dependence plot" (schematic)

Then do the same at a slightly warmer temperature, and again, across the whole range.
Joined up, the points draw a curve, called a partial dependence plot: the forest's
average prediction at each temperature.

## Scene 10
visual: manim Hump: the forest's partial dependence on temperature, rising to a peak at 7.7 °C and falling in warmer water (page results, partial-effects.qmd#fig-partial)

For the forest, the curve rises from the coldest water to a peak at 7.7 degrees, then
falls again in warmer water: a hump. The forest predicts the most animals in cool
water, and no single number could have described that shape.

## Scene 11
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Draw each input's effect: set it to each value in turn at every
station, and average the predictions.

# Split one prediction into parts

## Scene 12
visual: manim Average: the forest's predictions at the training stations as a strip of dots, their average 4.11 marked; one station's prediction, 6.53, picked out; "which inputs raised it?" (page results, explaining-one-prediction.qmd)

Finally, splitting one prediction into parts. Importance and the curve describe the
forest over all the stations, but often the question is about one station. Over the
stations it learned from, the forest predicts 4.11 animals on average. At this station
it predicts 6.53. Which inputs raised it?

## Scene 13
visual: manim Pushes: a line of predicted counts with the average marked; bars from it, two pushing up, one pushing down, ending at this station's prediction; "one SHAP value per input" (schematic)

SHAP values answer that. Each input gets one number for this station: the animals it
adds to the average, or takes away. A positive value pushes the prediction up, a
negative one pushes it down. Added together, they lead exactly from the average to
this station's prediction.

## Scene 14
visual: manim Name: "SHAP" spelled out as SHapley Additive exPlanations; then a quiz team sharing a prize, the best player's arrow widest and a player who cost points with a negative share; then the inputs sharing the gap, 6.53 − 4.11 = 2.42 animals, depth's share widest and the seabed's negative (schematic shares; the gap from explaining-one-prediction.qmd)

SHAP stands for SHapley Additive exPlanations. Additive, because the parts add up.
Shapley, after the mathematician Lloyd Shapley, who worked out a fair way to share a
team's prize among its players. Think of a quiz team that wins a prize. The player who
answered the most questions gets the biggest share, and a player who cost the team
points gets a negative one. Here the players are the inputs, and the prize is the gap
between the average and this station's prediction: 2.42 animals. The input that raised
the prediction most gets the biggest share, and an input that pulled it down gets a
negative one.

## Scene 15
visual: manim Waterfall: the station 44.9 m deep, from the average 4.11 to its prediction 6.53, a bar for each input: depth +0.95, chlorophyll +0.80, temperature +0.63, salinity +0.58, seabed (sand) −0.49, season −0.05 (page results, explaining-one-prediction.qmd#fig-waterfall)

At this station, 44.9 metres deep, depth adds 0.95 animals to the average. Chlorophyll
adds 0.8, temperature 0.63, and salinity 0.58. Its sandy seabed takes off 0.49, and the
season almost nothing. So each prediction comes with its reasons: check them against
what you know of the species, or show them to whoever acts on the prediction.

## Scene 16
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. Split one prediction into parts: each input's SHAP value is how far it
moves that prediction from the average.

# Quiz

## Scene 17
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Shuffling salinity barely changes the forest's error. Does that mean
salinity has no effect on the species?

## Scene 18
visual: manim QuizAnswer: "Not necessarily"; season's importance with temperature in the forest, then refitted without it, the bar growing from 0.04 to 0.15; "the same information, shared" (page results, feature-importance.qmd#fig-without)

Not necessarily. Importance says what this forest relies on, given its other inputs.
Two inputs that carry the same information share the work. Fitted again without
temperature, the forest leaned on season instead: its importance rose from 0.04 to
0.15, because summer water is warm and winter water cold. A low score can mean another
input already told the model the same thing.

# Key points

## Scene 19
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: shuffle each input in turn.

## Scene 20
visual: manim KeyPoints: the second ticked

Two: draw each input's effect.

## Scene 21
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: split one prediction into parts.

## Scene 22
visual: manim EndCard: the site's address and a thank-you

The pages go further: each station's own curve, models that can be read from their
parts, a small tree that copies the forest, and a model card to go with a model, with
all the code. They are linked below. Thanks for
watching.
