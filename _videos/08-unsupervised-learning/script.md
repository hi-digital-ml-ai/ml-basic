---
title: "Unsupervised learning: is that pattern real?"
section: chapters/08-unsupervised-learning/index.qmd
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

In this video, you will learn three things. Why every method always finds something.
Why a principal component is not a gradient. And how to tell a real group from a cut
through a gradient.

# The puzzle

## Scene 2
visual: manim Survey: a grid of 800 stations and a strip of 24 taxa, no label column (schematic)

Here is a survey of 800 seabed stations, with counts of 24 kinds of animal, and no
labels at all.

## Scene 3
visual: manim SoftSplit: the soft-bottom stations along a depth axis, coloured by the two clusters (page results, interpreting-patterns.qmd)

Take the soft-bottom stations, and ask for two groups. You get a shallow group, at a
median depth of 60 metres, and a deep one at 124.

## Scene 4
visual: manim SoftSplit: sixty resamples drop sixty agreement dots, all high

Resample the stations sixty times. The same split comes back every time: an agreement
of 0.89 on average, and never below 0.71.

## Scene 5
visual: manim SoftSplit: a question mark over the two groups
pause-after: 1.5

So are there two kinds of soft seabed community?

## Scene 6
visual: manim Simulated: a "true process" box sends dots to a map of stations (schematic)

A note first: this survey is simulated. We wrote the process that made it, so we can
check every answer against the truth.

# Groups from counts alone

## Scene 7
visual: manim KMeans: two centres move to the middle of the points nearest them, until nothing moves (schematic)

k-means places as many centres as you ask for, and moves each to the middle of the
stations nearest it, until nothing moves.

## Scene 8
visual: manim Units: each environmental variable's share of the variance, depth nearly all of it (page results, clustering.qmd)

Nearest means distance, in whatever units your columns happen to be in. In metres,
depth carries 99.4% of the variance.

## Scene 9
visual: manim Units: chlorophyll against depth, clustered raw into depth bands, then standardised
pause-after: 0.5

So clustering those columns as they stand is clustering depth. Standardise them first,
and a group of spring blooms appears.

## Scene 10
visual: manim Habitat: the two clusters against hard and soft seabed, 15 stations on the wrong side (page results)

On the counts, two groups find the hard and soft seabed, with 15 stations out of 800 on
the wrong side.

## Scene 11
visual: manim Habitat: the seabed column it never saw, crossed out

It was never told the seabed type. That is what clustering is for.

## Scene 12
visual: manim Noise: 800 points of uniform noise, cut into four tidy clusters, then "no structure found" struck through (page results, clustering.qmd#fig-noise)

But give it pure noise, and ask for four groups. You get four tidy groups, from
nothing. k-means never says it found nothing.

# How many groups?

## Scene 13
visual: manim Dial: the number of groups as a dial the analyst turns (schematic)

The number of groups is your choice. So how do you choose it?

## Scene 14
visual: manim Elbow: the within-group error against the number of groups, a smooth fall (page results, choosing-the-number-of-clusters.qmd)

The textbook looks for an elbow in the error. Here it falls smoothly, from 0.878 to
0.661: no elbow.

## Scene 15
visual: manim Silhouette: the silhouette curve, highest at two groups, under the rule-of-thumb line

The silhouette peaks at two groups, at 0.179. A common rule of thumb says anything under
0.25 means no structure.

## Scene 16
visual: manim Silhouette: the two-group point ticked, labelled "the seabed split"

Yet that split was the seabed, almost exactly.

## Scene 17
visual: manim Shuffle: each column of a small table shuffled on its own (schematic)

So shuffle each column on its own. Each animal keeps its counts, but who lives with
whom is gone.

## Scene 18
visual: manim Silhouette: the shuffled data's line along the floor

On shuffled data, the silhouette stays between 0.037 and 0.055. Against that floor,
0.179 is nearly five times as high.

## Scene 19
visual: manim Criteria: four criteria as cards, the elbow abstaining, then two, six and three (page results)

Other criteria disagree. The gap statistic, with its default reference, says six. A
mixture model says three. The truth is two.

## Scene 20
visual: manim Linkage: four linkage rules' agreement with the seabed, against the number of groups (page results, beyond-k-means.qmd#fig-linkage)

Settings decide too: four ways of building a cluster tree match the true split anywhere
from 0.005 to 0.889.

## Scene 21
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. Every method always finds something: compare what it found with the
same data, shuffled.

# A map of the stations

## Scene 22
visual: manim Rotate: a cloud of points and new axes turning to its longest spread (schematic)

Principal component analysis builds new axes from the columns, ordered by how much of
the spread they hold.

## Scene 23
visual: manim Variance: the share of variance of each component, the first two picked out (page results, principal-component-analysis.qmd)

The first two hold 29.4% of the variance. That sounds poor, but most of the rest is
sampling noise, and here we know it is.

## Scene 24
visual: manim Ordination: the 800 stations on the first two components, shaded by depth, shaped by seabed (page results, principal-component-analysis.qmd#fig-ordination)

The map shows both structures. The hard seabed sticks out as its own arm, and depth
runs smoothly up each arm, with no edge anywhere.

## Scene 25
visual: manim Ordination: the arm outlined as "boundary", the depth ramp as "gradient"

A separate arm is a boundary. A smooth ramp is a gradient.

## Scene 26
visual: manim Ordination: "first component = depth?" on the horizontal axis
pause-after: 0.5

Now name the axes. Is the first one depth?

## Scene 27
visual: manim Ordination: arrows for depth and hard bottom, at 139° and 41°

No. Depth increases at 139 degrees from the first axis, and hard bottom at 41. Both lie
at about 45 degrees to the axes.

## Scene 28
visual: manim Ordination: the axes turn freely in the plane, the arrows fixed

The two carry almost the same variance, so nothing tells PCA which way to turn its axes.
It finds the plane, not the gradients.

## Scene 29
visual: manim Rules: three rules for how many components to keep: 16, 7 and 3 (page results, dimensionality-reduction.qmd)

How many components should you keep? Three common rules say sixteen, seven, and three.

## Scene 30
visual: manim CvComponents: cross-validated depth error against the number of components (page results, dimensionality-reduction.qmd#fig-components)

Let the task decide. Predict depth from the components: one gives an error of 30.4
metres, two give 21.2, and all 24 do no better than two.

## Scene 31
visual: manim Umap: the UMAP picture of the survey, shaded by depth (page results, dimensionality-reduction.qmd#fig-umap)

UMAP draws a prettier map. The hard seabed pulls out as its own arm, and depth runs
smoothly along both.

## Scene 32
visual: manim Umap: the same settings on shuffled data, a shape with no colour pattern

But shuffled data, with nothing in it, still makes a shape. Only the colours give it
away.

## Scene 33
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. A component is a direction of large spread, not a gradient: check what
it lines up with, and let the task choose how many to keep.

# Is it real?

## Scene 34
visual: manim Questions: three questions to ask of any pattern (schematic)

With nothing held out to check against, ask three questions of any pattern.

## Scene 35
visual: manim Bootstrap: sixty resamples of the whole survey drop agreement dots, the mean marked (page results, interpreting-patterns.qmd#fig-bootstrap)

First, does it replicate? Cluster sixty resamples of the whole survey. Their average
agreement with the original split is 0.881.

## Scene 36
visual: manim Bootstrap: two heaps, 53 near one and 7 near zero, the mean in the empty gap

But fifty-three resamples found that split almost exactly, and seven found something
else entirely. The average describes no resample that happened.

## Scene 37
visual: manim Bootstrap: the seven labelled "a depth split"

The seven had cut the survey by depth. That is two answers, not one noisy one. Report
the spread, not its average.

## Scene 38
visual: manim Stability: the puzzle's soft-bottom dots beside the whole survey's

Second: is it a group, or a cut through a gradient? The puzzle's split was even more
stable than the seabed split: never below 0.71, where the seabed split fell to 0.095.

# The puzzle, solved

## Scene 39
visual: manim Continuum: eight soft-bottom taxa across depth, each curve peaking a little deeper (page results, interpreting-patterns.qmd#fig-continuum)

But every kind of animal here was given a favourite depth, spread evenly from 20 to 160
metres.

## Scene 40
visual: manim Continuum: the curves overlapping, no gap anywhere along the axis

Each peaks a little deeper than the last, and neighbours overlap: there is no depth
where one set hands over to another.

## Scene 41
visual: manim Continuum: the cut at about 92 metres drawn through the curves

k-means cut that slope at about 92 metres, in the same place every time. A stable method
cuts a stable gradient in a stable place.

## Scene 42
visual: manim Continuum: "two communities" crossed out, "one turnover with depth" ticked

So there are no two soft-bottom communities. Just one continuous turnover with depth.

## Scene 43
visual: manim External: agreement with the seabed type, the whole-survey split at 0.920 (page results)

Third: does it match something the method never saw? The whole-survey split matches
the seabed type at 0.920.

## Scene 44
visual: manim External: the soft-bottom split against depth bands, 0.40

The soft-bottom split matches depth bands at 0.40, as any cut through a slope would.
Matching a category is evidence of groups. Matching a measurement cut into bands is not.

## Scene 45
visual: manim Finding: "composition turns over with depth" as the sentence for the paper

And a gradient is a finding too. "Composition turns over with depth" is the honest
sentence here.

## Scene 46
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Stable is not the same as real: check against something the method
never saw, and report a gradient as a gradient.

# Quiz

## Scene 47
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. In a UMAP picture, two islands sit twice as far apart as two others. Are
they twice as different?

## Scene 48
visual: manim QuizAnswer: islands sliding apart while each keeps its neighbours (schematic)

No. UMAP keeps each station's nearest neighbours. The space between the islands means
nothing.

# Key points

## Scene 49
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: every method finds something.

## Scene 50
visual: manim KeyPoints: the second ticked

Two: a component is not a gradient.

## Scene 51
visual: manim KeyPoints: the third ticked

Three: stable is not the same as real.

## Scene 52
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
