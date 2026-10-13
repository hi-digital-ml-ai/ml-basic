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
map (PCA makes no groups, but colours and shapes on its map show how well known groups
fit: here the recorded seabed, or else the k-means groups), and check that groups come
back (refitting k-means on resampled sites, which the Validation video introduced, to
judge whether the chosen k is reasonable). The key points avoid why and what. The
silhouette and the shuffled baseline, hierarchical clustering and linkage, loadings, the
share of variance, the number of components, UMAP, the adjusted Rand index by name, the
gap between clusters and the soft-bottom split stay on the pages; the end card names
some of them.
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

First, finding groups without labels. In supervised learning, a model learns from
examples that come with answers, such as the habitat at each station. But often nobody
has recorded the answer. A benthic survey counts the animals at every station, and
nobody has said which habitat each station belongs to. Can the counts alone sort the
stations into groups?

## Scene 3
visual: manim Matrix: a table builds up, one row per station and one column per taxon, counts filling in; "same habitat: similar counts" (page results, clustering.qmd)

This survey has 800 stations, each with counts of 24 kinds of animal, or taxa. One row
per station, one column per taxon. Stations in the same habitat should have similar
counts: the same animals, in similar numbers.

## Scene 4
visual: manim Points: stations as points placed by two taxa's counts, two clouds; "similar counts: close together" (schematic)

Clustering sorts the stations into groups of similar ones. Picture each station as a
point, placed by its counts. Stations with similar counts lie close together, so the
distance between two points says how different they are. Here there are only two taxa,
so the picture is flat; with 24, the idea is the same, but it cannot be drawn.

## Scene 5
visual: manim KMeans: two centres placed; points coloured by nearest centre, centres move, repeat; "a group for every station" (schematic)

The most widely used method is k-means. Before it starts, you choose the number of
groups, k: here, two. It places two centres, and each station joins its nearest centre.
Each centre then moves to the middle of its stations, and the two steps repeat until
nothing changes. The result is a group for every station.

## Scene 6
visual: manim Seabed: 800 squares in two groups, then each marked by its recorded seabed; the 15 out of place ringed (page results, clustering.qmd)

k-means gives the groups numbers, not names. To see what they mean, compare them with
something recorded. Here, the seabed was recorded at each station, though k-means never
saw it. Asked for two groups, k-means put the hard bottom, rock and gravel, in one group,
and the soft bottom, sand and mud, in the other. Only 15 of the 800 stations sit in the
other kind's group.

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
which the stations spread out most: the first principal component, or PC1.

## Scene 9
visual: manim Spread: "PC2: next most, at right angles"; then "each one: a mix of all 24 taxa" (schematic)

The second, PC2, is the direction of next most spread, at right angles to the first.
Each one is a mix of all 24 taxa, chosen so that the stations spread out as far as they
can. Spread matters because it is where the stations differ.

## Scene 10
visual: manim Ordination: the 800 stations drawn on PC1 and PC2 in grey; "similar counts sit close" (page results, principal-component-analysis.qmd#fig-ordination)

Draw each station at its place on PC1 and PC2, and 24 columns become one map. Stations
with similar counts sit close together, and stations with different counts sit far
apart.

## Scene 11
visual: manim Ordination: "PCA: a place for each station", "no groups"; "check groups by eye: colour or shape" (page results)

Note that PCA does not split the stations into groups. It only gives each station a
place on the map. But the map is a good way to check groups by eye: mark each station's
group with a colour or a shape, and see whether the groups sit apart.

## Scene 12
visual: manim Ordination: the stations marked by recorded seabed, circles and triangles; "two arms, a narrow band between"; "no record? mark the k-means groups" (page results)

Here the groups are known beforehand, because the seabed was recorded. Mark hard bottom
with circles and soft bottom with triangles, and the two form separate arms of the map,
meeting only in a narrow band. If no groups had been recorded, you could mark the groups
k-means found instead.

## Scene 13
visual: manim Ordination: the stations coloured by depth, "depth changes smoothly: a gradient"; "PCA saw neither" (page results)

Now colour the map by depth. It changes smoothly along each arm, with no edge: a
gradient, not groups. PCA never saw the seabed or the depth: the counts alone put the
stations there.

## Scene 14
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 2
pause-after: 2.0

Key point two. Draw many columns as one map: PCA places the stations, and colours and
shapes show how well groups fit.

# Check that groups come back

## Scene 15
visual: manim Random: points scattered at random, cut into four tidy groups; "the groups alone cannot judge k" (schematic)

Finally, checking that groups come back. Remember that you choose k. k-means always
returns that many groups, even from random numbers. Asked for four groups here, it finds
four tidy ones. So the groups alone cannot tell you whether k is a reasonable choice.

## Scene 16
visual: manim Idea: two rows of three small samples; real groups split the same way each time, random points split a different way each time (schematic)

Here is the idea. Real groups should not depend on exactly which stations were
surveyed. If the groups are real and k fits them, a slightly different sample gives the
same groups. If not, the groups shift from one sample to the next.

## Scene 17
visual: manim Bootstrap: the survey's sites drawn again at random, some twice and some not at all, each with all its stations; "fit k-means again, same k: the same groups?" (schematic)

To get slightly different samples, resample the survey's sites, as in the Validation
video: draw 160 sites from its own 160, with replacement, each with all its stations.
Fit k-means again on each new sample, with the same k, and compare its groups with the
first ones.

## Scene 18
visual: manim Replicates: sixty dots by agreement with the first grouping, 52 near one, 8 near zero (page results, interpreting-patterns.qmd#fig-bootstrap)

Here, with k equal to two, this was done 60 times. Each dot is one refit, placed by how
closely its groups match the first ones: one means the same groups. In 52 of the 60
refits, the hard and soft groups came back almost exactly. In the other 8, the stations
split into shallow and deep instead.

## Scene 19
visual: manim Replicates: "k = 2: a reasonable choice"; "report how often each came back"; "another k? repeat the check" (page results)

So two groups is a reasonable choice here, and the hard and soft groups are the stronger
answer. Report how often each came back. To judge another k, say five, repeat the check
with five, and see how often the same five groups come back.

## Scene 20
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked; then an animal cheers
cheer: 3
pause-after: 2.0

Key point three. Check that groups come back: refit on resampled sites, and see whether
k gives the same groups each time.

# Quiz

## Scene 21
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Asked for five groups of plankton samples, k-means returns five groups. Is
five a good choice?

## Scene 22
visual: manim QuizAnswer: "You can't tell yet"; random dots cut into five groups; "resample, refit with five: do the same five come back?" (schematic)

You can't tell yet. k-means returns five groups whenever it is asked for five, even from
random numbers. Resample, refit with k equal to five, and count how often the same five
groups come back. If they rarely do, five is not a good choice.

# Key points

## Scene 23
visual: manim KeyPoints: the three key points, the first ticked

To sum up. <short pause> One: find groups without labels.

## Scene 24
visual: manim KeyPoints: the second ticked

Two: draw many columns as one map.

## Scene 25
visual: manim KeyPoints: the third ticked; then all three animals cheer
cheer: all
pause-after: 4.0

Three: check that groups come back.

## Scene 26
visual: manim EndCard: the site's address and a thank-you

The pages go further: choosing the number of groups, clustering as a tree, how much of
the counts a map can show, and other kinds of map, with all the code. They are linked
below. Thanks for watching.
