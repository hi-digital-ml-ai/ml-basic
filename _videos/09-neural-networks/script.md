---
title: "Neural networks: sums with a bend, and when they pay off"
section: chapters/09-neural-networks/index.qmd
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

This video is an overview built on three ideas, each with its examples from the pages:
a network is weighted sums with a bend (one neuron is linear regression, two bends make
the temperature hump), training can go wrong without a warning (learning rate, early
stopping, the seed), and a network pays off with signal to spare and a combination
nobody has named (the learning curves, the expected counts, the water-mass band). The
expected counts are shown only as a check on the models, as on the page, and the video
says a real survey has no such column. Autoencoders are left to the pages, for length.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. What a neural network actually computes.
Why one can fail without a single warning. And when a network is the right tool.

## Scene 2
visual: manim Parts: a small network drawn, then its three parts named: weighted sums, a bend, a walk downhill (schematic)

Neural networks are behind much of the artificial intelligence in the news. Yet every
part of one is something this course has already met: weighted sums, a bend, and a
walk downhill.

## Scene 3
visual: manim Survey: a table of stations, measurement columns and a count column (schematic)

As throughout the course, the examples use one simulated survey: counts of one species
at coastal stations, with the depth, the water temperature and more at each.

# Weighted sums with a bend

## Scene 4
visual: manim Neuron: three inputs, each arrow a weight, into a circle with a bend (schematic)

A neuron multiplies each input by a weight, adds a constant, and passes the total
through a bend, called the activation.

## Scene 5
visual: manim OneNeuron: the neuron's weights beside lm()'s coefficients, identical (page results, what-a-network-is.qmd)

Without the bend, that is linear regression. One neuron and an ordinary regression
agreed to nine decimal places.

## Scene 6
visual: manim Activations: logistic, tanh and ReLU drawn one by one (schematic)

The bends are simple: an S-curve, or ReLU, flat and then straight.

## Scene 7
visual: manim Layer: the neuron becomes a hidden layer of four, then an output (schematic)

A hidden layer is several neurons reading the same inputs. An output neuron adds up
their results into the prediction.

## Scene 8
visual: manim Collapse: without a bend, the layers fold into one straight line
pause-after: 0.5

And here is the whole trick. Without a bend, any number of layers adds up to one
straight line.

## Scene 9
visual: manim Hump: mean abundance in one-degree bins of temperature, and the fitted straight line, rising gently (page results, what-a-network-is.qmd#fig-hump)

Abundance peaks at a middle temperature. A straight line cannot turn over: the best one
rises gently and misses the peak.

## Scene 10
visual: manim Hump: the one-unit curve, flat and then falling

One hidden unit adds a single bend. It can fall, but it cannot rise first.

## Scene 11
visual: manim Hump: the two-unit network's two bends, then their sum, a hump (page results, what-a-network-is.qmd#fig-bends)

Two can. A rising bend and a falling one add up to a hump.

## Scene 12
visual: manim Hump: the hump's peak at 8.7 °C, inside the 8–9 °C bin marked as the highest, "7 weights"

Its peak is at 8.7 degrees, inside the one-degree band where the stations hold the most
animals. Nobody told the network that shape. It found it with seven weights.

## Scene 13
visual: manim Weights: three inputs and four hidden units, every arrow lit, 21 weights against 4; then 241 for ten inputs and twenty units (page results, what-a-network-is.qmd)

But every arrow is a weight to estimate. Three inputs and four hidden units make 21
weights, where linear regression has 4. Ten inputs and twenty units make 241.

## Scene 14
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. A network is weighted sums with a bend between them, and the bend does
the work.

# Training it

## Scene 15
visual: manim Descent: a ball stepping down a loss curve (schematic)

A network learns its weights by gradient descent: find which way is downhill for every
weight, and take a small step.

## Scene 16
visual: manim Backprop: the network, with the error passed back from the output, layer by layer (schematic)

A first-layer weight acts through everything after it. Backpropagation passes the
error back from the output, one layer at a time, and gives every weight its slope.

## Scene 17
visual: manim Check: the largest difference between backpropagation and nudging, for each group of weights (page results, forward-and-backward.qmd)

Nudging each weight by a tiny amount checks those slopes. All 21 agreed to ten decimal
places.

## Scene 18
visual: manim Rates: training error under four learning rates, 0.01 crawling (page results, training-a-network.qmd#fig-rates)

The length of each step is the learning rate. At 0.01, the network takes 1,122 steps to
beat a straight line.

## Scene 19
visual: manim Rates: 0.2 the lowest, 0.5 bouncing, 2 gone off the chart, "not a number at step 147"

At 0.2 it goes lowest. At 0.5 it is quicker, but bounces around the valley floor. At 2,
the error passes 1,000 by step 6, and becomes "not a number" at step 147, with no
warning at all.

## Scene 20
visual: manim Stopping: a 40-unit network's training error over 8,000 steps (page results, training-a-network.qmd#fig-early-stopping)

Now give a network forty hidden units and 8,000 steps. Its training error falls the
whole way.

## Scene 21
visual: manim Stopping: the validation error, lowest at step 1,937, then 4% worse by the end

On 200 stations held back for validation, the error is lowest at step 1,937, and 4% worse
by the end. Keeping the weights from that step is early stopping.

## Scene 22
visual: manim Seeds: ten runs, identical but for the seed, as dots on a validation-error axis (page results, training-a-network.qmd)

Then train ten networks that differ only in their random starting weights.

## Scene 23
visual: manim Seeds: the spread, 0.055, marked; the average of the ten, better than seven of them

Their validation error spans 0.055, from the seed alone. Averaging all ten does better
than seven of them.

## Scene 24
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. A network can fail without a warning: set it up on validation data, and
report the spread over seeds.

# When a network pays off

## Scene 25
visual: manim Curves: an empty chart of test RMSE against training stations, the line for predicting the mean at 4.72 (page results, how-much-data.qmd#fig-learning-curves)

Back to the survey. Linear regression, a random forest and a network with eight hidden
units predict the counts from 40 training stations up to all 539. Predicting the mean
scores 4.72.

## Scene 26
visual: manim Curves: the three learning curves with their ranges, the forest lowest, the network's range widest

The forest leads at every size, ending at 4.20. The network varies most from draw to
draw, and ends at 4.94.

## Scene 27
visual: manim Curves: "cross-validation chooses one hidden unit, penalty 1", beside the linear regression line

Allowed to choose, cross-validation shrinks the network to one hidden unit with the
largest penalty: almost a straight line.

## Scene 28
visual: manim Expected: noisy counts scattered around a smooth curve; the counts fade, "a check, not data" (schematic)

But this survey is simulated, so each station's expected count is known: the average its
count was drawn from. A real survey has no such column. Here it is only a check.

## Scene 29
visual: manim Expected: RMSE against the expected counts with all 539 stations, network 1.54, forest 1.63, linear regression 2.12 (page results, how-much-data.qmd)

Scored against the expected counts, the order turns round. The network scores 1.54, the
forest 1.63, and linear regression 2.12. The network had learned the response best; the
noise in the counts hid it.

## Scene 30
visual: manim Signal: "short of rows" struck out, "short of signal" ticked
pause-after: 0.5

So it was not short of rows. It was short of signal.

## Scene 31
visual: manim Band: 200 simulated stations on a temperature–salinity diagram, the core stations in a diagonal band (page results, when-to-use-one.qmd)

Now a simulated water mass. Its core is a diagonal band on a temperature–salinity
diagram, and 200 stations train the models.

## Scene 32
visual: manim Boundaries: logistic regression's single line, the tree's blocks, the forest's staircase, each with its ROC AUC (page results, when-to-use-one.qmd#fig-boundaries)

Scored by ROC AUC, where one is a perfect ranking, logistic regression draws one
straight line and reaches 0.715. A tree cuts one input at a time: 0.827. A forest of 500
trees: 0.926.

## Scene 33
visual: manim Boundaries: the network's clean diagonal band, 9 weights, 0.999

A network with two hidden units, nine weights in all, reaches 0.999.

## Scene 34
visual: manim Units: each hidden unit's line drawn on the plane, one along each edge of the band (page results)

Each hidden unit bends along a tilted line. Two of them, one at each edge, fence in the
band.

## Scene 35
visual: manim Sizes: ROC AUC at 100, 400 and 1,600 training stations, network, forest and logistic regression (page results, when-to-use-one.qmd)

With only 100 stations, the network reaches 0.997. The forest needs 1,600 to come
close, and logistic regression stays near 0.72.

## Scene 36
visual: manim Combination: "salinity − 0.16 × temperature" added as a column; logistic regression 1.000 (page results, when-to-use-one.qmd)

If you can name the combination, add it as a column: logistic regression then reaches
1.000. A network finds the combinations nobody has named.

## Scene 37
visual: manim Images: pixels into an edge, edges into a shape (schematic)

That is why networks lead on images and sound. An edge is a combination of pixels, and
nobody can list them all.

## Scene 38
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. A network pays off when the data carry signal to spare, and what
matters is a combination nobody has named.

# Quiz

## Scene 39
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A network has ten hidden layers of a hundred units, and every activation
is the identity. What shapes can it fit?

## Scene 40
visual: manim QuizAnswer: the ten layers fold into one straight line (schematic)

Only a straight line. A weighted sum of weighted sums is still a weighted sum.

# Key points

## Scene 41
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: a network is sums with a bend.

## Scene 42
visual: manim KeyPoints: the second ticked

Two: it can fail without a warning.

## Scene 43
visual: manim KeyPoints: the third ticked

Three: it needs signal, not just rows.

## Scene 44
visual: manim EndCard: the site's address and a thank-you

The pages also cover autoencoders, a network that maps the stations with no response to
predict, with all the code. They are linked below. Thanks for watching.
