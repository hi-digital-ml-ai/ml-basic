---
title: "Unsupervised learning: finding structure without labels"
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

Rebuilt 2026-10-14 as an introduction, one new concept per part, each with one example
and one picture, as the Assumptions and Validation videos were: find groups without
labels (k-means, which recovers the seabed from the counts), draw many columns as one
map (PCA and the ordination), and check that groups come back (refitting k-means on
resampled sites, which the Validation video introduced). The key points avoid why and
what. The silhouette and the shuffled baseline, hierarchical clustering and linkage,
loadings, the number of components, UMAP, the adjusted Rand index by name, the gap
between clusters and the soft-bottom split stay on the pages; the end card names some
of them.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

Welcome back to Machine Learning Basics for Marine Science. This video is about
unsupervised learning: finding structure in data that has no answers. It covers three
things: finding groups without labels, drawing many columns as one map, and checking
that groups come back.

# Find groups without labels

## Scene 2
visual: manim NoLabels: a table of animal counts, its habitat column empty (schematic)

First, finding groups without labels. A benthic survey counts the animals at every
station, but nobody has said which habitat each station belongs to. There is no answer
for a model to learn from. Can the counts alone sort the stations into groups?

## Scene 3
visual: manim Matrix: a table builds up, one row per station and one column per taxon, counts filling in (page results, clustering.qmd)

This survey has 800 stations, each with counts of 24 kinds of animal, or taxa. One row
per station, one column per taxon.

## Scene 4
visual: manim Points: stations as points placed by two taxa's counts, two clouds; "similar counts: close together" (schematic)

Clustering sorts the stations into groups of similar ones. Picture each station as a
point, placed by its counts, so that stations with similar counts lie close together.
Here there are only two taxa, so the picture is flat; with 24, the idea is the same.

## Scene 5
visual: manim KMeans: two centres placed; points coloured by nearest centre, centres move, repeat (schematic)

The most widely used method is k-means. You choose the number of groups, k: here, two.
It places two centres, and each station joins its nearest centre. Each centre then moves
to the middle of its stations, and the two steps repeat until nothing changes.

## Scene 6
visual: manim Seabed: 800 squares in two clusters, then each marked by its recorded seabed; the 15 out of place ringed (page results, clustering.qmd)

Given only the counts of the 800 stations, k-means was asked for two groups. Now compare
them with the seabed, recorded at each station but never shown to k-means. One group is
the hard bottom, rock and gravel; the other, the soft bottom, sand and mud. Only 15 of
the 800 stations sit in the other kind's group.

## Scene 7
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 1
pause-after: 2.0

Key point one. Find groups without labels: k-means sorts the stations into groups of
similar ones.

# Draw many columns as one map

## Scene 8
visual: manim Spread: a tilted cloud of points; new axes turn to its longest spread, "PC1: most spread" (schematic)

Next, drawing many columns as one map. Two columns make a flat picture, but 24 cannot
be drawn at all. Principal component analysis, or PCA, helps. It finds the direction in
which the stations spread out most: the first principal component.

## Scene 9
visual: manim Spread: "PC2: next, at right angles"; then "each a mix of all 24 taxa" (schematic)

The second principal component is the direction of next most spread, at right angles
to the first. Each component is a mix of all 24 taxa, weighted so that the stations
spread out as far as they can.

## Scene 10
visual: manim Ordination: the 800 stations drawn on PC1 and PC2 in grey; "similar counts sit close" (page results, principal-component-analysis.qmd#fig-ordination)

Draw each station at its place on the first two components, and 24 columns become one
map. Stations with similar counts sit close together, and stations with different
counts sit far apart.

## Scene 11
visual: manim Ordination: the stations shaped by seabed, then coloured by depth; "one arm: hard bottom", "depth changes smoothly"; "PCA never saw either" (page results)

Now mark what was recorded at each station. The hard-bottom stations form one arm of the
map and the soft-bottom stations another, and depth changes smoothly from shallow to
deep. PCA never saw the seabed or the depth: the counts alone put them there.

## Scene 12
visual: manim Ordination: "PC1 and PC2: 29.4% of the variance"; "a summary: enough to see the main structure" (page results)

A map of two components is a summary. Here it holds 29.4 per cent of the variance in
the counts. That is usual for species counts, and enough to show the main structure.

## Scene 13
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Draw many columns as one map: PCA places the stations along their
directions of most spread.

# Check that groups come back

## Scene 14
visual: manim Random: points scattered at random, cut into four tidy groups; "groups alone prove nothing" (schematic)

Finally, checking that groups come back. k-means always returns the number of groups
you ask for, even from random numbers. Asked for four groups here, it finds four tidy
ones. So a set of groups, on its own, proves nothing.

## Scene 15
visual: manim Bootstrap: the survey's sites drawn again at random, some twice and some not at all, each with all its stations; "fit k-means again: same groups?" (schematic)

Real groups should come back when the data change a little. So, as in the Validation
video, resample the survey's sites: draw 160 sites from its own 160, with replacement,
each with all its stations. Fit k-means again on the new sample, and see whether the
same groups come back.

## Scene 16
visual: manim Replicates: sixty dots by agreement with the first grouping, 52 near one, 8 near zero (page results, interpreting-patterns.qmd#fig-bootstrap)

Do this 60 times. Each dot is one refit, placed by how closely its groups match the
first ones: one means the same groups. In 52 of the 60 refits, the hard and soft groups
came back almost exactly. In the other 8, the stations split into shallow and deep
instead.

## Scene 17
visual: manim Replicates: "two competing answers"; "report how often each came back: 52 and 8 of 60" (page results)

So the data hold two competing answers, and the seabed groups are the stronger. Report
how often each one came back, not just the groups.

## Scene 18
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. Check that groups come back: refit on resampled sites, and report how
often they return.

# Quiz

## Scene 19
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Asked for five groups of plankton samples, k-means returns five groups. Does
that show the samples fall into five groups?

## Scene 20
visual: manim QuizAnswer: "Not yet"; random dots cut into five groups; "resample, refit: do the five come back?" (schematic)

Not yet. k-means returns five groups whenever it is asked for five, even from random
numbers. Resample, refit, and see whether the same five groups come back.

# Key points

## Scene 21
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: find groups without labels.

## Scene 22
visual: manim KeyPoints: the second ticked

Two: draw many columns as one map.

## Scene 23
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: check that groups come back.

## Scene 24
visual: manim EndCard: the site's address and a thank-you

The pages go further: choosing the number of groups, clustering as a tree, how many
components to keep, and other kinds of map, with all the code. They are linked below.
Thanks for watching.
