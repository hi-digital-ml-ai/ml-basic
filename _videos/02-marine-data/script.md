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

Welcome back to Machine Learning Basics for Marine Science. This video is a short tour
of marine data. It covers three things: what the course's survey records, how to find
and fix the problems in a raw data file, and how to test a model without fooling
yourself.

# The survey

## Scene 2
visual: manim Table: a data table flows into a model; a bad value in the table flows straight through to the output (schematic)

Let's start with why the data come first. A model learns only from the table it is
given. If the table is wrong, the model learns that too, and nothing in its output says
so. So before any modelling, we need to know what is in the table.

## Scene 3
visual: manim Station: one station as a card, where and when, the water, the seabed, the count of one species, each part appearing as it is named (schematic, after the-coastal-survey.qmd img/survey-station.svg)

The course works on one simulated coastal survey, the one from the introduction. Each
row of its table is a station: one visit to one place. It records where and when, the
water's temperature and salinity, and its chlorophyll, a measure of the tiny plants
called phytoplankton. Then the type of seabed, and the count of one species.

## Scene 4
visual: manim Kinds: a quantity, depth; a category, the seabed; neither, the month; then months on a line with December and January far apart, bending into a circle where they meet (schematic)

The columns come in different kinds, and each kind is handled differently. Some are
quantities, measured on a scale, like depth. Some are categories, a label from a short
list, like the type of seabed. And some are neither, like the month, which goes round
in a cycle. As plain numbers, December and January are eleven months apart. In the sea
they are neighbours, so a model needs to see the months as a circle.

## Scene 5
visual: manim Counts: three bars, 815 rows, 800 unique rows, 160 sites, appearing as spoken (page results, the-coastal-survey.qmd)

Now, how many observations does the survey really hold? The raw file has 815 rows. Some
are the same station entered twice, called duplicates. Remove them, and 800 remain. But
those 800 come from only 160 sites, each visited several times.

## Scene 6
visual: manim Site: several visits to one site share the same water and seabed, "rows are not independent observations"; then the site's rows are kept together as one block (schematic)

Visits to the same site share their water and their seabed, so they are alike. A fifth
visit to a site tells the model much less that is new than a first visit to another
site. So the row count is not the number of independent observations, each bringing its
own information. Keep the rows, but keep each site's rows together. We will see why when
we test a model.

## Scene 7
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. Know what one row is, and how many of them are really independent.

# Cleaning the raw file

## Scene 8
visual: manim Ranges: salinity in the raw file, smallest −999, average 2.24, largest; "real sea water: about 34", "no sea is that fresh" (page results, exploring-and-cleaning.qmd)

Next, cleaning the raw file. Before modelling, look at the data. A simple first check is
the smallest, average and largest value of every column. Here is salinity. Its smallest
value is minus 999, and its average is 2.24. Real sea water here is about 34, so no sea
is that fresh.

## Scene 9
visual: manim Ranges: −999 marked missing, the mean becomes 33.9 (page results, exploring-and-cleaning.qmd)

Minus 999 is a code: some instrument or export wrote it to mean "missing". Mark those
values as missing instead, and the average becomes 33.9, as it should be.

## Scene 10
visual: manim Substrate: twelve spellings as labels, collapsing into four seabed types (page results, exploring-and-cleaning.qmd)

Count every category, too. The type of seabed was written in twelve different ways, such
as sand with a capital S, sand in capitals, and sandy. They are really four types: mud,
sand, gravel and rock. A model would treat each spelling as a different habitat, so the
spellings are merged.

## Scene 11
visual: manim Deletion: stations per season, then with incomplete rows dropped; winter shrinks most, 10% overall, 20% of winter (page results, exploring-and-cleaning.qmd#fig-deletion)

Some values are simply missing. Chlorophyll is missing most often in winter. Many
modelling functions quietly drop every incomplete row, that is, every station with any
value missing. Here, that loses 10% of the stations, but 20% of the winter ones. The
model then learns winter from fewer stations, which can bias its results.

## Scene 12
visual: manim Why: "why is this value missing, or strange?"; then three reasons a value is missing, each with its fix: by chance, little harm; depends on something recorded, fill in from it; depends on the missing value itself, no fix in the data (schematic, after missing-and-unusual.svg)
pause-after: 0.5

So every fix starts with one question: why is this value missing, or strange? The answer
decides the fix. A sample lost by pure chance costs only a little precision. Gaps that
depend on something recorded, such as the season, can be filled in from what was
recorded. But when a sensor fails in storms, the gaps are the stormy values themselves,
and no fix to the data can bring them back.

## Scene 13
visual: manim Recipe: three preparations, each with a short gloss: standardise, the same scale; log, pull in a long tail; columns of 0s and 1s, a category as numbers; then three cards, specify, estimate on the training data, apply to any data (schematic, after scaling-and-encoding.qmd img/recipe-steps.svg)

Many methods also need the columns prepared. Standardising puts every column on the same
scale: subtract its mean and divide by its standard deviation, so depth in metres cannot
outweigh temperature in degrees. A log pulls in a long tail, such as a few very high
chlorophyll values. And a category, such as the seabed, becomes columns of zeros and
ones, because models need numbers. A recipe holds these steps. It lists them, works out
the numbers they need, such as each mean, from the training data only, and then applies
those same numbers to any data. Why the training data only? We come to that next.

## Scene 14
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Look before you model. Each fix is a decision, and preparation belongs
in a recipe.

# Testing a model honestly

## Scene 15
visual: manim Roles: "tested on data it has not seen"; training, the model learns from it; validation, chooses between models; test, reports the result, once (schematic)

Now to testing a model. A model must be tested on data it has not seen, because it may
simply have memorised the data it learned from. So the data are split into parts with
different jobs. The model learns from the training data. Validation data choose between
models, or between settings of one model. And the test data report the result, once, at
the end.

## Scene 16
visual: manim Split: a random split, every test station marked at a site already in training, 100% (page results, splitting-data.qmd)

The simplest way is a random split: each station goes to training or test by chance,
here three quarters to training. Split this survey at random, and every test station
sits at a site the model trained on.

## Scene 17
visual: manim Questions: the goal, "predict places nobody has sampled"; the random split tests a site the model knows; the split by site holds back site D, new to the model; then "split along what you will predict for" (schematic, after splitting-data.qmd img/split-roles.svg)
pause-after: 0.5

But a survey model is usually wanted for places nobody has sampled. A random split only
tests another visit to a site the model already knows. Hold back whole sites instead, so
every visit to a test site stays out of training. Then the test sites are new to the
model, as they will be in use. So split along what you will predict for: by site for new
sites, by year for next year.

## Scene 18
visual: manim Leak: test data seeping into the model before the test, "information leakage", "every score looks better", "and leaves no trace" (schematic)

When information from the test data reaches the model before the test, that is called
information leakage, or leakage for short. It makes the score look better than the
model really is, and it leaves no trace: the results look just like honest ones, only
better.

## Scene 19
visual: manim Target: R squared, 0 "no better than the average", 1 "every prediction exact"; environment only 0.22, plus catch weight 0.98 (page results, information-leakage.qmd)

Here is an example. A linear regression, met in the introduction as a straight line,
predicts the count from the environment: the water, the seabed and the season. We score
it with R squared: the share of the variation in the test counts that the predictions
follow. One means every prediction is exact; zero means no better than predicting the
average. On the environment alone, R squared is 0.22. Add one more column, catch
weight, and it jumps to 0.98.

## Scene 20
visual: manim Target: catch weight and the count, the same animals; for each test station the model is handed its answer; the 0.98 bar crossed, "copying, not predicting" (schematic, page results as in scene 19)

Catch weight is the weight of the animals that were counted: the count again, in other
units. So for every test station, the model is handed the answer it should predict. The
0.98 measures copying, not predicting.

## Scene 21
visual: manim Group: R squared, random split 0.22, by site 0.04 (page results, information-leakage.qmd)

Leakage can also hide in the split. Keep each site whole, and the environment-only
model's R squared falls from 0.22 to 0.04. Predicting a new site is much harder than
predicting another visit to a familiar one, and the random split hid that.

## Scene 22
visual: manim Question: "does this line use any information from rows I intend to test on?"
pause-after: 0.5

Leakage is rarely cheating. It is usually one line of code in the wrong place. So one
question catches every kind of leakage. Does this line of code use information from the
rows I intend to test on?

## Scene 23
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

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
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: split along what you will predict for, and keep the test data untouched.

## Scene 29
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
