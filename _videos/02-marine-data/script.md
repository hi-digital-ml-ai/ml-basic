---
title: "Marine data: understanding and preparing a survey"
section: chapters/02-marine-data/index.qmd
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
without teaching each page in full. It uses only linear regression, the one model the
course has introduced so far, and never says which variables truly drive the species.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

This video is a short tour of marine data. It covers three things: what the course's
survey records, how to find and fix the problems in a raw data file, and how to test a
model without fooling yourself.

# The survey

## Scene 2
visual: manim Table: a data table flows into a model; a bad value in the table flows straight through to the output (schematic)

A model learns only from the table it is given. If the table is wrong, the model
learns that too, and nothing in its output says so.

## Scene 3
visual: manim Station: one station as a card, where and when, the water, the seabed, the count of one species, each part appearing as it is named (schematic, after the-coastal-survey.qmd img/survey-station.svg)

The course works on one simulated coastal survey. Each row is a station: one visit to
one place. It records where and when, the water's temperature, salinity and
chlorophyll, the type of seabed, and the count of one species.

## Scene 4
visual: manim Kinds: a number column, a category column, then months on a line with December and January far apart, bending into a circle where they meet (schematic)

Columns come in different kinds. Some are quantities, some are categories, and some
are neither. As numbers, December and January are eleven months apart; in the sea they
are neighbours.

## Scene 5
visual: manim Counts: three bars, 815 rows, 800 unique rows, 160 sites, appearing as spoken (page results, observations-and-features.qmd)

The raw file has 815 rows. Remove the duplicates and 800 remain. But they come from
only 160 sites, each visited several times.

## Scene 6
visual: manim Site: several visits to one site share the same water and seabed, then the site's rows are kept together as one block (schematic)

Visits to the same site share their water and their seabed, so they are alike. The
row count is not the number of independent observations. Keep the rows, but keep each
site's rows together.

## Scene 7
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. Know what one row is, and how many of them are really independent.

# Cleaning the raw file

## Scene 8
visual: manim Ranges: the smallest and largest value of every numeric column, salinity highlighted, minimum −999, mean 2.24 (page results, exploratory-analysis.qmd)

Before modelling, look. The smallest value of salinity is minus 999, and its average
is 2.24. No sea is that fresh.

## Scene 9
visual: manim Ranges: −999 marked missing, the mean becomes 33.9 (page results, missing-values-and-outliers.qmd)

Minus 999 was written to mean "missing". Mark it missing, and the average is 33.9.

## Scene 10
visual: manim Substrate: twelve spellings as labels, collapsing into four seabed types (page results, exploratory-analysis.qmd)

Count every category, too. Four seabed types were written twelve different ways, and a
model would treat each spelling as a different habitat.

## Scene 11
visual: manim Deletion: stations per season, then with incomplete rows dropped; winter shrinks most, 10% overall, 20% of winter (page results, missing-values-and-outliers.qmd#fig-deletion)

Chlorophyll is missing most often in winter. Drop every incomplete row, as most
modelling functions do by default, and you lose 10% of the stations, but 20% of
winter.

## Scene 12
visual: manim Why: "why is it missing?" and "why is it unusual?", each with its three reasons (schematic, after missing-and-unusual.svg)
pause-after: 0.5

So every fix starts with one question: why is this value missing, or strange? The
answer decides the fix, and some gaps cannot be fixed at all.

## Scene 13
visual: manim Recipe: three cards, specify, estimate on the training data, apply to any data (schematic, after scaling-and-encoding.qmd img/recipe-steps.svg)

Columns then need preparing: standardised, logged, or turned into columns of zeros and
ones. A recipe lists these steps, works out the numbers they need from the training
data only, and applies them to any data.

## Scene 14
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Look before you model. Each fix is a decision, and preparation belongs
in a recipe.

# Testing a model honestly

## Scene 15
visual: manim Roles: training fits, validation chooses, test reports once (schematic)

A model must be tested on data it has not seen. Training data fits the model,
validation data chooses between models, and test data reports the result, once.

## Scene 16
visual: manim Split: a random split, every test station marked at a site already in training, 100% (page results, splitting-data.qmd)

Split this survey at random, and every test station sits at a site the model trained
on.

## Scene 17
visual: manim Questions: the goal, "predict places nobody has sampled"; the random split tests a site the model knows; the split by site holds back site D, new to the model; then "split along what you will predict for" (schematic, after splitting-data.qmd img/split-roles.svg)
pause-after: 0.5

But a survey model is usually wanted for places nobody has sampled. A random split
only tests another visit to a site the model already knows. Hold back whole sites
instead, and the test sites are new to the model, as they will be in use. So split
along what you will predict for.

## Scene 18
visual: manim Leak: test data seeping into the model before the test, "leaves no trace" (schematic)

When information from the test data reaches the model before the test, that is
leakage. It makes every score look better, and it leaves no trace.

## Scene 19
visual: manim Target: R squared, environment only 0.28, plus catch weight 0.98 (page results, information-leakage.qmd)

Add catch weight to a linear regression of the count, and R squared jumps from 0.28
to 0.98.

## Scene 20
visual: manim Target: catch weight and the count, the same animals; for each test station the model is handed its answer; the 0.98 bar crossed, "copying, not predicting" (schematic, page results as in scene 19)

Catch weight is the weight of the animals that were counted: the count again, in other
units. So for every test station, the model is handed the answer it should predict.
The 0.98 measures copying, not predicting.

## Scene 21
visual: manim Group: R squared, random split 0.28, grouped by site 0.08 (page results, information-leakage.qmd)

Keep each site whole, and the honest model's R squared falls from 0.28 to 0.08.
Predicting a new site is much harder than predicting a familiar one.

## Scene 22
visual: manim Question: "does this line use any information from rows I intend to test on?"
pause-after: 0.5

One question catches every kind of leakage. Does this line of code use information
from the rows I intend to test on?

## Scene 23
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Split along what you will predict for, and keep the test data
untouched by every decision.

# Quiz

## Scene 24
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A colleague fills the gaps in chlorophyll with the median of the whole
survey, then splits it into training and test data. What is wrong?

## Scene 25
visual: manim QuizAnswer: "leakage"; every row, test rows included, feeds the median; then a recipe takes the median from the training rows only (schematic, after information-leakage.qmd img/leakage-kinds.svg)

Leakage. The test rows helped set that median, so the test data reached the model
before the test. Put the step in a recipe, and the median comes from the training
data only.

# Key points

## Scene 26
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: the row count is not the number of independent
observations.

## Scene 27
visual: manim KeyPoints: the second ticked

Two: look before you model, and treat every fix as a decision.

## Scene 28
visual: manim KeyPoints: the third ticked

Three: split along what you will predict for, and keep the test data untouched.

## Scene 29
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
