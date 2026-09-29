---
title: "Assumptions: when the ocean disagrees with your model"
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
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. Why your rows are worth less evidence than
they seem. Why a better fit can give a more wrong answer. And why a model answers
confidently where it knows nothing.

# The puzzle

## Scene 2
visual: manim Accuracy: an accuracy gauge fills to 95% (page results, class-imbalance.qmd)

Here is a model built to find a rare species. It is 95% accurate.

## Scene 3
visual: manim Accuracy: a "stations flagged" counter stays at zero

Yet at every station it was tested on, it never once said the species was there.

## Scene 4
visual: manim Accuracy: a question mark between the gauge and the counter
pause-after: 1.5

How can a model be so accurate, and so useless?

## Scene 5
visual: manim Simulated: a "true process" box sends dots to a map of stations (schematic)

A note first: this survey is simulated. We wrote the process that made it, so we can
check every answer against the truth.

# Every method assumes something

## Scene 6
visual: manim Assumes: the words "assumption-free" appear and are struck through (schematic)

Machine learning is often called assumption-free. It is not.

## Scene 7
visual: manim Assumes: two panels, "the shape of a relationship" light, "how the data were collected" heavy

It assumes less about the shape of a relationship. But it assumes a lot about how the
data were collected.

# Rows are not observations

## Scene 8
visual: manim Visits: a column of 720 rows fills the screen (page results, independence-of-observations.qmd)

Our survey has 720 visits.

## Scene 9
visual: manim Visits: the rows gather into stacks, one per site

But they come from 158 sites, visited again and again.

## Scene 10
visual: manim Visits: one site's stack highlighted, its visits sharing one colour

Two visits to one site share its rock, its currents and its patch of animals. They are
not two separate pieces of evidence.

## Scene 11
visual: manim Visits: a counter runs down from 720 to about 550

Allowing for that, the 720 visits are worth about 550 independent ones.

## Scene 12
visual: manim ClusterSE: naive and honest standard errors as bars, chlorophyll's grows 2.77 times (page results)

The cost is in certainty. Chlorophyll's honest standard error is 2.77 times the naive
one.

## Scene 13
visual: manim ClusterSE: a random site-level column's p-value moves away from significance

A column of random numbers, one per site, looked close to significant. Counted honestly,
it was nowhere near.

# Neighbours in the test set

## Scene 14
visual: manim ResidualMap: the shelf, each site coloured by the model's leftover error (page results, spatial-and-temporal-dependence.qmd#fig-map)

Even different sites are not independent. Stations close together tend to be wrong in
the same way.

## Scene 15
visual: manim RandomFolds: one held-out station, its training neighbours ringed (page results)

Ordinary cross-validation holds out a station, and trains on its neighbours.

## Scene 16
visual: manim RandomFolds: lines join the held-out station to its nearest neighbours

So a model can score well just by looking up the neighbourhood.

## Scene 17
visual: manim CoordsOnly: an R² bar for a model of position alone, random folds (page results)

A forest given nothing but longitude and latitude scores an R² of 0.075.

## Scene 18
visual: manim CoordsOnly: the shelf splits into blocks and the bar shrinks

Hold out whole blocks of the shelf instead, and it falls to 0.011.

## Scene 19
visual: manim CoordsGain: environment, then environment plus position, random folds (page results)

Now add position to a model of the environment. Random folds say it helps by 29%.

## Scene 20
visual: manim CoordsGain: the same pair under blocked folds

Blocked folds say 11%. Most of the gain was the validation scheme flattering itself.

## Scene 21
visual: manim CoordsGain: a pointer to the validation section

This is the trap in this section. The validation section shows how to test honestly.

## Scene 22
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. Your rows are worth less than they seem: repeat visits and near
neighbours make results look more certain than they are.

# A better fit, a wrong answer

## Scene 23
visual: manim Hump: a response curve rises and falls around an optimum (schematic)

Species have a best temperature and a best depth. The response is a hump, not a
straight line.

## Scene 24
visual: manim Recovery: temperature, the fitted curve drawn over the true one (page results, linearity-and-nonlinearity.qmd#fig-shapes)

A flexible model finds the best temperature: 9.3 degrees, where the truth is 9.

## Scene 25
visual: manim Recovery: depth, the fitted curve against the true one, the two optima marked

Same model, same data. It puts the best depth at 15 metres. The truth is 80.

## Scene 26
visual: manim Tangled: depth linked to temperature, food and position (schematic)

The difference is not the method. Depth is tangled up with temperature, food and
position.

## Scene 27
visual: manim Tangled: a curve is drawn, and arrows try each variable in turn

Flexibility lets a model draw any shape. It cannot tell which variable the shape
belongs to.

## Scene 28
visual: manim FitBars: how well three models fit, the flexible one best (page results)

And of three models, this one fitted the data best.

# Wrong about the spread

## Scene 29
visual: manim Spread: counts scattered around their average, a Poisson band drawn (schematic)

A Poisson model makes a claim: the variance of the counts equals their average.

## Scene 30
visual: manim Spread: the band widens to the observed spread (page results, distributional-assumptions.qmd)

Here the variance is nearly four times larger. Animals gather in groups.

## Scene 31
visual: manim EmptyStations: empty stations in 500 surveys simulated from the Poisson model (page results, distributional-assumptions.qmd#fig-ppc)

Simulate surveys from the Poisson model, and they have about 68 empty stations.

## Scene 32
visual: manim EmptyStations: the real survey's line lands far to the right

The real survey has 159. That model could not have made these data.

## Scene 33
visual: manim PoissonSE: standard-error bars, Poisson against the right model (page results)

Its standard errors were about half the right size.

## Scene 34
visual: manim PoissonSE: depth's p-value crosses the significance line

So depth looked highly significant. With the right model, it was not.

## Scene 35
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. A better fit can be more wrong: flexibility and the wrong distribution
both give confident answers that are false.

# Past the edge of the data

## Scene 36
visual: manim Effort: survey tracks cluster near a port, open water left empty (schematic)

Survey effort follows ports and weather. Some water is never sampled at all.

## Scene 37
visual: manim DepthBands: the true mean count by depth band, water shallower than 100 m shaded (page results, sampling-and-extrapolation.qmd#fig-extrapolation)

So train a model only on water shallower than 100 metres, and ask it about deeper water.

## Scene 38
visual: manim DepthBands: the forest's line runs flat past the edge

A random forest cannot follow the decline. It repeats the last thing it saw.

## Scene 39
visual: manim DepthBands: the deepest band, truth and forest labelled

In the deepest water, the truth is about one animal. The forest says nearly five.

## Scene 40
visual: manim BiasBars: the forest's bias in range and past the edge (page results)

Past the edge, its predictions are 73% too high on average, with no warning at all.

## Scene 41
visual: manim Novelty: temperature against chlorophyll, the survey grey, each variable's range boxed (page results, sampling-and-extrapolation.qmd#fig-novelty)

Checking each variable's range is not enough. The survey saw cold water, and it saw
high chlorophyll, but never the two together.

## Scene 42
visual: manim Novelty: the stations inside every range but outside the survey light up

40% of the stations to predict passed every single range check, and still lay outside
the survey.

# The puzzle, solved

## Scene 43
visual: manim Prevalence: a grid of 100 stations, 5 of them coloured (page results, class-imbalance.qmd)

Back to the rare species. It is found at 5% of stations.

## Scene 44
visual: manim Prevalence: every station stamped "no", 95 of them ticked

Say no every time, and you are 95% accurate.

## Scene 45
visual: manim Probabilities: every station's predicted probability, all short of the 0.5 line (page results)

The model's highest probability anywhere was 0.37. The usual cut-off of one half never
fires.

## Scene 46
visual: manim Tradeoff: the untouched model's curve, the rebalanced models landing on or below it (page results, class-imbalance.qmd#fig-tradeoff)

Rebalancing the training data is the usual fix. It moves along the trade-off, but does
not lift it.

## Scene 47
visual: manim Tradeoff: the untouched model at a cut-off of 0.05 lands on the upsampled point

Upsampling gave the same result as simply lowering the cut-off to 0.05.

## Scene 48
visual: manim Tradeoff: a balance of missed species against wasted inspections

So choose the cut-off from what each kind of mistake costs.

## Scene 49
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. A model answers where it knows nothing: past the edge of its data, and
on events it has barely seen. Check both.

# Quiz

## Scene 50
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A forest was trained on water down to 100 metres. What does it predict at
190?

## Scene 51
visual: manim QuizAnswer: the forest's predictions by depth band, flat past the edge (page results)

Much the same as just past 100 metres: about five animals. The truth is about one.

# Key points

## Scene 52
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: your rows are worth less than they
seem.

## Scene 53
visual: manim KeyPoints: the second ticked

Two: a better fit can be more wrong.

## Scene 54
visual: manim KeyPoints: the third ticked

Three: a model answers where it knows nothing, so check where it is being asked.

## Scene 55
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
