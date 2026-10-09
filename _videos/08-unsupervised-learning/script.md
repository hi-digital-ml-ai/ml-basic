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

This video is an overview built on three ideas, each with one or two examples:
clustering finds groups nobody labelled (k-means recovers the seabed from the counts;
a shuffled copy says how many groups stand out; a tree gives every number at once),
PCA turns many columns into a map (the ordination, its loadings, and choosing the
number of components by its use; UMAP briefly), and a pattern is checked before it is
reported (bootstrap samples, a gap, a recorded category). The quiz applies the second
check to the soft-bottom split on the checking page. The other linkage rules, UMAP's
settings and the horseshoe effect are left to the pages; the end card names them.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. How clustering finds groups nobody has
labelled. How principal component analysis turns many columns into one map. And how to
check a pattern before you report it.

## Scene 2
visual: manim NoLabels: a table of animal counts, its answer column empty (schematic)

Many marine datasets have no answer column. A benthic survey counts the animals at
every station, but nobody has said which habitat each station belongs to. Unsupervised
learning finds structure in the data itself.

## Scene 3
visual: manim Matrix: a table builds up, one row per station and one column per taxon, counts filling in (page results, clustering.qmd)

Here, each of the course's 800 simulated survey stations has counts of 24 taxa. One
row per station, one column per taxon: ecologists call this a community matrix.

# Clustering finds groups nobody labelled

## Scene 4
visual: manim KMeans: points in two dimensions; two centres placed, points coloured by nearest centre, centres move, repeat (schematic)

Clustering sorts stations into groups of similar stations. The most widely used
method is k-means. You choose the number of groups, k. Each station joins its nearest
centre, each centre moves to the average of its stations, and this repeats.

## Scene 5
visual: manim Seabed: 800 squares in two clusters, then each marked by its recorded seabed; the 15 out of place highlighted (page results, clustering.qmd)

k-means was given only the counts, logged and on a common scale, and asked for two
groups. One cluster is the hard bottom, rock and gravel; the other, the soft bottom.
Only 15 of the 800 stations sit in the other kind's cluster.

## Scene 6
visual: manim Random: points scattered at random, cut into four tidy groups (schematic)

But k-means returns as many groups as you ask for, even from random numbers. So how
many groups does the survey really hold?

## Scene 7
visual: manim Silhouette: one station, its average distance to its own cluster and to the nearest other cluster (schematic)

The silhouette width compares each station's distance to its own cluster with its
distance to the nearest other one. Averaged over the stations, higher means better
separated groups.

## Scene 8
visual: manim Sweep: the average silhouette for two to eight clusters, highest at two (page results, choosing-the-number-of-clusters.qmd#fig-k-sweep)

Across two to eight clusters, the silhouette is highest at two, at 0.179. That
sounds low: a popular rule of thumb calls it no real structure.

## Scene 9
visual: manim Shuffle: a small table, each column's values shuffled up and down on its own (schematic)

So run the same clustering on a shuffled copy. Shuffle each taxon's counts across
the stations: every column keeps its values, but any groups are gone.

## Scene 10
visual: manim Sweep: the shuffled baseline added near 0.05; the lead at two clusters marked "3.5 times" (page results)

On shuffled counts, the silhouette stays near 0.05 for every number of clusters. At
two, the survey scores three and a half times that, the clearest lead of any.

## Scene 11
visual: manim Tree: stations joined pair by pair into a dendrogram; a cut line drops to give two, then three groups (schematic)

Hierarchical clustering gives every number of groups at once. It joins the two
closest groups again and again, and records the joins as a tree, a dendrogram. Cut it
high for a few groups, lower for more.

## Scene 12
visual: manim Linkage: the share of stations in the largest group for Ward and single linkage at two to six groups (page results, hierarchical-clustering.qmd#fig-linkage)

How the tree measures the distance between groups, its linkage, decides what it
finds. Ward's linkage finds nearly the same two groups as k-means. Single linkage chains
more than 99 per cent of stations into one group.

## Scene 13
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. Clustering finds groups nobody labelled. Compare them with the same data,
shuffled, to see how many really stand out.

# PCA turns many columns into one map

## Scene 14
visual: manim Components: a cloud of points; the direction of most spread drawn as PC1, the next at right angles as PC2 (schematic)

Twenty-four columns cannot be drawn in one picture. Principal component analysis, or
PCA, finds the direction along which the stations spread out most: the first principal
component. The second is the next most, at right angles.

## Scene 15
visual: manim Ordination: the 800 stations on PC1 and PC2, coloured by depth, shaped by seabed (page results, principal-component-analysis.qmd#fig-ordination)

Plotted on those two, the stations form a map, an ordination, where similar
communities sit close together. The two components hold 29.4 per cent of the variance,
usual for species counts.

## Scene 16
visual: manim Loadings: each taxon as a point at its loadings on PC1 and PC2, coloured by its share on hard bottom (page results, principal-component-analysis.qmd#fig-loadings)

To read the axes, look at the loadings: the weight of each taxon in a component.
The hard-bottom taxa sit together, and the rest line up in order of depth.

## Scene 17
visual: manim Ordination: arrows for depth and hard bottom over the map, each about 39 degrees from an axis (page results)

So depth and seabed both run diagonally, about 39 degrees from the axes: each
component mixes the two. Read an axis from its loadings, not from its name.

## Scene 18
visual: manim Keep: 24 component bars by share of variance; the 80% line falls at 16; then the shuffled shares, three components above them (page results, dimensionality-reduction.qmd#fig-baseline)

Components can also be a model's inputs. How many to keep? Keeping 80 per cent of the
variance keeps 16 of the 24. Parallel analysis keeps only those that beat their
shuffled counterparts: three.

## Scene 19
visual: manim Depth: cross-validated error of predicting depth against the number of components, flat after two (page results, dimensionality-reduction.qmd#fig-components)

When the components feed a model, cross-validate the number. To predict depth, two
are enough. The third holds real structure, rock against gravel, that depth does not
need.

## Scene 20
visual: manim UMAP: the observed map, hard bottom apart and depth running smoothly, beside the shuffled single cloud (page results, dimensionality-reduction.qmd#fig-umap)

UMAP draws a map another way, keeping each station's nearest neighbours close. The
hard-bottom stations form their own group, with depth running smoothly through each.
Shuffled counts give one cloud.

## Scene 21
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. PCA turns many columns into one map. Read its axes from their loadings,
and keep as many components as the use needs.

# Check a pattern before reporting it

## Scene 22
visual: manim Checks: a supervised model checked against held-out answers; a clustering with none; three cards appear (schematic)

A supervised model can be checked against held-out answers. A clustering has none,
so three checks take their place.

## Scene 23
visual: manim Bootstrap: the survey's sites drawn again at random, some twice and some not at all, each with all its stations (schematic)

First, does the pattern come back? A bootstrap sample draws the survey's sites again
at random, with replacement, each with all its stations. k-means is refitted on sixty.

## Scene 24
visual: manim Agreement: pairs of stations, together or apart in two groupings; the adjusted Rand index from zero to one (schematic)

The adjusted Rand index compares each refit with the original. For every pair of
stations: together in both, or apart in both? One means identical, zero no better than
chance.

## Scene 25
visual: manim Replicates: sixty dots by agreement with the original, 52 near one, 8 near zero (page results, interpreting-patterns.qmd#fig-bootstrap)

In 52 of the 60 samples, the seabed split came back almost exactly. In the other 8,
a split into shallow and deep took its place. Report how often each came back.

## Scene 26
visual: manim Gap: stations placed on the line between two cluster centres; groups give two humps with a gap, a gradient gives a flat spread (schematic)

Second, is there a gap? Place each station on the line between the two cluster
centres. Real groups leave few stations near the boundary; a gradient leaves as many
there as anywhere.

## Scene 27
visual: manim Positions: the seabed split's histogram of positions, two humps, 2% within 0.1 of the boundary (page results, interpreting-patterns.qmd#fig-positions)

The seabed split has a clear gap: only 2 per cent of stations lie close to its boundary.

## Scene 28
visual: manim Record: the two clusters beside the recorded seabed; the adjusted Rand index 0.92 (page results, interpreting-patterns.qmd)

Third, does it match a record? The split matches the recorded seabed, which k-means
never saw, at an adjusted Rand index of 0.92: the strongest evidence there is.

## Scene 29
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. Check a pattern before reporting it: does it come back, is there a gap,
and does it match a record?

# Quiz

## Scene 30
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. Within the soft bottom, k-means splits the stations into shallow and
deep, and the split comes back in every bootstrap sample. Are they two groups?

## Scene 31
visual: manim QuizAnswer: "not yet"; the soft-bottom split's flat histogram beside the seabed split's two humps, 11% against 2% near the boundary (page results, interpreting-patterns.qmd#fig-positions)

Not yet. Eleven per cent of its stations sit near the boundary, against 2 per cent
for the seabed split. No gap: k-means cut a steady depth gradient in the same place every
time. And a gradient is a finding too.

# Key points

## Scene 32
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: clustering finds groups nobody
labelled; compare them with shuffled data.

## Scene 33
visual: manim KeyPoints: the second ticked

Two: PCA turns many columns into a map; read its axes from their loadings.

## Scene 34
visual: manim KeyPoints: the third ticked

Three: check a pattern before reporting it.

## Scene 35
visual: manim EndCard: the site's address and a thank-you

The pages also cover how to read a UMAP map, the other linkage rules and the
horseshoe effect in PCA, with all the code. They are linked below. Thanks for watching.
