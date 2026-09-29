---
title: "Marine data: preparing a survey without fooling yourself"
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
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. How many observations you really have.
What to look for before you model. And how a test score gets inflated without anyone
noticing.

# The puzzle

## Scene 2
visual: manim Scores: two random forests on the same survey, R squared 0.87 and 0.13 (page results, information-leakage.qmd)

Here are two random forests, fitted to the same coastal survey. One has an R squared
of 0.87: it explains most of the variation in abundance. The other, 0.13.

## Scene 3
visual: manim Scores: "which would you trust?"
pause-after: 1.5

Same data, same kind of model. Which one would you trust? By the end of this video,
you will choose the lower one, and know why.

## Scene 4
visual: manim Raw: the file as it came off the ship, 815 rows and 17 columns (page results, observations-and-features.qmd)

It starts with the survey as it came off the ship: one file, 815 rows and 17 columns.

# Counting the observations

## Scene 5
visual: manim Counts: a bar of 815 rows, "so 815 observations?" (page results, observations-and-features.qmd#fig-what-is-n)

So you have 815 observations?

## Scene 6
visual: manim Counts: unique rows 800 added, "the same station entered twice"

Remove the exact duplicates, the same station entered twice, and you have 800.

## Scene 7
visual: manim Counts: distinct stations 800, distinct sites 160, the last bar far shorter

800 distinct stations, too. But only 160 distinct sites.

## Scene 8
visual: manim Visits: how many times each site was visited, most four to six, one fifteen (page results)

The survey returns to fixed sites. Most were visited four to six times; one, fifteen
times.

## Scene 9
visual: manim Site: five stations at one site, sharing water, seabed and day, "closer to one observation with replicates" (schematic)

Stations at one site share the same water, the same seabed, often the same day. They
are closer to one observation with replicates than to five observations.

## Scene 10
visual: manim Counts: "effective sample size nearer 160 than 815", "scores computed on 815 are optimistic"

So your effective sample size is nearer 160 than 815. Every score computed as though
it were 815 will be optimistic.

## Scene 11
visual: manim Site: the rows kept, each site's rows kept together when splitting (schematic)

The fix is not to delete rows. It is to keep each site's rows together when you split
the data.

## Scene 12
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. The row count is not the sample size. Deciding what one row is, is a
scientific decision.

# Looking before modelling

## Scene 13
visual: manim Ranges: the minimum, mean and maximum of every numeric column (page results, exploratory-analysis.qmd)

Now look before you model. Print the smallest and largest value of every numeric
column, and read them as a scientist.

## Scene 14
visual: manim Ranges: salinity highlighted, minimum −999, mean 2.24

Salinity has a minimum of minus 999, and a mean of 2.24. No ocean is 2 PSU.

## Scene 15
visual: manim Salinity: the histogram, a bar at −999 and the real ocean a sliver near 34 (page results, exploratory-analysis.qmd#fig-damage)

Minus 999 was written to mean "missing". Because it is a number, nothing complained.
Mark it missing, and the mean salinity is 33.9.

## Scene 16
visual: manim Ranges: depth highlighted, maximum 1581 m, "a shelf survey meant to stay under 200 m"

Depth reaches 1581 metres, on a shelf survey meant to stay under 200.

## Scene 17
visual: manim Depths: temperature against depth, ten stations far out, then divided by ten into the cloud (page results, missing-values-and-outliers.qmd)

Ten stations were recorded ten times too deep. Divide them by ten, and each one lands
where its temperature makes sense. That is evidence, not convenience.

## Scene 18
visual: manim Depths: two more hidden inside the cloud, "undetectable"

Two more were ten times too deep but landed inside the normal range. No amount of
looking will find them.

## Scene 19
visual: manim Substrate: twelve spellings as bars, collapsing into four substrate types (page results)

Count every level of every category. Here, four substrate types have twelve
spellings, and a model treats each spelling as a different habitat.

## Scene 20
visual: manim Missing: chlorophyll missing by season, 19% in winter, 1% in autumn (page results, exploratory-analysis.qmd#fig-damage)

Chlorophyll is missing at 19% of winter stations, and 1% in autumn. Missing, but not
at random.

## Scene 21
visual: manim Deletion: stations per season before and after dropping incomplete rows, winter loses a fifth (page results, missing-values-and-outliers.qmd#fig-deletion)

Most modelling functions quietly drop any row with a gap. Here that removes 80 rows,
and a fifth of winter.

## Scene 22
visual: manim Vessels: mean salinity by vessel, 33.75 and 34.13, temperatures alike (page results)

Now split by vessel. The two ships sampled the same shelf, and one reads higher
salinity than the other. That is an instrument offset, invisible in the pooled data.

## Scene 23
visual: manim Months: December and January eleven apart on a line, neighbours on a circle (schematic)

And ask what each column means. As numbers, December and January are eleven months
apart. In the ocean they are neighbours.

## Scene 24
visual: manim Rare: the rare species at 5% of stations, "always say absent" scores 95% (page results)

Last, the response. The rare species is present at 5% of stations, so answering
"absent" every time is 95% accurate.

## Scene 25
visual: manim Decisions: the six findings, each turned into a decision (page results)

Each finding is a decision, not a repair, and each one needs someone who knows how
the data were collected.

## Scene 26
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. Exploration is damage assessment. Its output is a list of decisions,
and none of them should be a default.

# Protecting the test set

## Scene 27
visual: manim Roles: training fits, validation chooses, test reports once (schematic)

Now the held-back data. Training data fit the model. Validation data choose between
models. The test set reports, once, at the end.

## Scene 28
visual: manim Split: a random split, 600 and 200, every test station at a site already in training (page results, splitting-data.qmd)

Split this survey at random, and every one of the 200 test stations sits at a site the
model has trained on.

## Scene 29
visual: manim Questions: "another station at a site I surveyed?" against "a site I never surveyed?" (schematic)

So the test asks how well it predicts another station at a surveyed site. A habitat
map is asked about sites nobody has surveyed.

## Scene 30
visual: manim Stratify: asked to stratify on the rare species, 6.0% in training against 2.5% in test (page results)

Or ask the split to stratify on the rare species. The code runs without complaint. Yet
training gets 6.0% of it, and the test set 2.5%.

## Scene 31
visual: manim Stratify: the rare class pooled away by a default, fixed at 5.0% and 5.5%, "check the result, not the code"

The rare class fell below a default threshold and was quietly pooled away. Lower the
threshold, and you get 5.0 and 5.5%. Check that a safeguard did what you asked.

## Scene 32
visual: manim Scores: back to the puzzle, "leakage: information from the test data reaching the model"

Back to the puzzle. Both scores were shaped by leakage: information about the test data
reaching the model before the test.

## Scene 33
visual: manim Target: environment only 0.25, plus catch weight 0.87 (page results, information-leakage.qmd)

The 0.87 came from adding one column, catch weight. The forest without it scored 0.25.

## Scene 34
visual: manim Target: catch weight and the count, "the same measurement in different units", no catch weight at a new station

But catch weight is the weight of the animals that were counted: the same measurement,
in different units. At a new station, nobody has counted anything, so there is no
catch weight.

## Scene 35
visual: manim Target: the test question, "would this value exist for a station I have not sampled?"

So ask of every feature: would this value exist for a station I have not yet sampled?

## Scene 36
visual: manim Group: random split 0.25, grouped by site 0.13 (page results)

The 0.13 is the forest without catch weight, tested on sites it never saw. Keeping
sites together halved its R squared.

## Scene 37
visual: manim Group: error falls from 4.82 to 3.76, struck out, "different test sets"
pause-after: 0.5

Its error falls, from 4.82 to 3.76, but that is not an improvement. The two were scored
on different test sets, so compare R squared, not the error.

## Scene 38
visual: manim Scores: 0.87 marked "leaked", 0.13 marked "honest"
pause-after: 1.0

So the lower score is the honest one. It says how well the model predicts a site nobody
has surveyed.

## Scene 39
visual: manim Noise: 200 columns of pure noise, the ten best chosen using all rows, test R squared 0.03 (page results)

One more leak. Take 200 columns of pure random noise. Choose the ten most correlated
with abundance using all the rows, and the test R squared is 0.03.

## Scene 40
visual: manim Noise: chosen using training rows only, 0.0003, near the truth of zero

Choose them from the training rows only, and it is 0.0003, near the truth of zero.

## Scene 41
visual: manim Recipe: specify the steps, estimate them on training data, apply them to test data (schematic)

The cure is order. Specify each step, estimate it on training data only, then apply it
to the test data. A recipe inside a workflow does exactly that.

## Scene 42
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. The test set must be untouched by every decision, not just by the
fitting.

# Quiz

## Scene 43
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A colleague's habitat model uses a habitat class that was assigned by
looking at what was caught. Its score is excellent. What is wrong?

## Scene 44
visual: manim QuizAnswer: "target leakage", the class cannot exist for a station nobody has sampled (schematic)

Target leakage. The class could not exist for a station nobody has sampled, so the
model cannot run in the field.

# Key points

## Scene 45
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: the row count is not the sample
size.

## Scene 46
visual: manim KeyPoints: the second ticked

Two: look before you model, and treat every fix as a decision.

## Scene 47
visual: manim KeyPoints: the third ticked

Three: keep the test set untouched by every decision.

## Scene 48
visual: manim EndCard: the site's address and a thanks

The pages for this section, with all the code, are linked below. Thanks for watching.
