---
title: "Neural networks: short of data, or short of signal?"
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
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. What a neural network actually computes.
Why one can fail without a single warning. And when a network is the right tool.

# The puzzle

## Scene 2
visual: manim Survey: a table of 720 stations, eight predictor columns and a count column (schematic)

Here is a survey of 720 stations, with eight measurements at each, and a count of
animals to predict.

## Scene 3
visual: manim Network: a network with eight inputs and eight hidden units, trained on 480 stations (schematic)

Fit a neural network with eight hidden units, the kind you would write without
thinking. Train it on 480 stations.

## Scene 4
visual: manim Puzzle: the network's test error beside predicting the average (page results, how-much-data.qmd)

Its test error is 5.26. Simply predicting the average scores 4.402. The network is
worse than knowing nothing.

## Scene 5
visual: manim Puzzle: "networks need a lot of data" and a question mark over 480
pause-after: 1.5

Neural networks need a lot of data, they say. So are 480 stations too few?

## Scene 6
visual: manim Simulated: a "true process" box sends dots to a map of stations (schematic)

A note first: this survey is simulated. We wrote the process that made it, so we can
check every answer against the truth.

# Weighted sums with a bend

## Scene 7
visual: manim Neuron: three inputs, each arrow a weight, into a circle with a bend (schematic)

A neuron multiplies each input by a weight, adds a constant, and passes the total
through a bend, called the activation.

## Scene 8
visual: manim OneNeuron: the neuron's weights beside lm()'s coefficients, identical (page results, what-a-network-is.qmd)

Without the bend, that is linear regression. One neuron and an ordinary regression
agreed to eight decimal places.

## Scene 9
visual: manim Activations: identity, logistic, tanh and ReLU drawn one by one (schematic)

The bends are simple: an S-curve, or ReLU, flat and then straight.

## Scene 10
visual: manim Layer: the neuron becomes a hidden layer of four, then an output (schematic)

A hidden layer is several neurons reading the same inputs. Their outputs feed the
prediction.

## Scene 11
visual: manim Collapse: without a bend, the layers fold into one straight line
pause-after: 0.5

And here is the whole trick. Without a bend, any number of layers is still one
straight line.

## Scene 12
visual: manim Hump: binned mean abundance against temperature, and the best straight line, rising (page results, what-a-network-is.qmd#fig-hump)

Abundance peaks at a middle temperature. The best straight line through it rises: it
gets even the direction wrong.

## Scene 13
visual: manim Hump: the one-unit curve, a single S-curve that only falls

One hidden unit is one S-curve. It can rise or fall, but not both.

## Scene 14
visual: manim Hump: the two-unit network's two S-curves, then their sum, a hump

Two can. Two opposing S-curves add up to a hump.

## Scene 15
visual: manim Hump: the hump's peak at 8.7 °C, the true optimum at 9 °C, five units on top

Its peak is at 8.7 degrees. The truth is 9. Five units add nothing more.

## Scene 16
visual: manim Weights: weights against hidden units, 225 at sixteen units, against 720 stations (page results)

But every arrow is a weight to estimate. Sixteen hidden units on this survey is 225
weights, for 720 stations.

## Scene 17
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. A network is weighted sums with a bend between them, and the bend is
the whole trick.

# Training it

## Scene 18
visual: manim Descent: a ball stepping down a loss curve (schematic)

Training is gradient descent: find how the error changes with every weight, and step
downhill.

## Scene 19
visual: manim Backprop: the network, with the slopes passed back from the output, layer by layer (schematic)

A first-layer weight acts through everything after it. Backpropagation passes the
slopes back from the output, one layer at a time.

## Scene 20
visual: manim Check: the hand-written gradients against a brute-force check, disagreement about 1e-11 (page results, forward-and-backward.qmd)

Our hand-written gradients matched a brute-force check to about eleven decimal places.

## Scene 21
visual: manim Rates: training error under five learning rates, 0.01 crawling (page results, training-a-network.qmd#fig-rates)

The size of each step is the learning rate. At 0.01, the network has barely beaten a
straight line after 1,500 steps.

## Scene 22
visual: manim Rates: 0.2 the lowest, 0.5 bouncing, 2 gone off the chart, "overflowed by step 147"

At 0.2 it descends cleanly. At 0.5 it bounces around. At 2, the error explodes, and by
step 147 it has overflowed.

## Scene 23
visual: manim Scaling: the same network on measured units and on standardised inputs, against a straight line (page results)

Now leave the inputs in metres and degrees. Same network, same learning rate, same
start.

## Scene 24
visual: manim Scaling: bars 0.570, 0.680 and 0.763, the unscaled one worst

It scores 0.763. Standardised, 0.570. A straight line, 0.680. It loses to a straight
line, and nothing warns you.

## Scene 25
visual: manim Stopping: a 40-unit network's training and validation error over 8,000 steps (page results, training-a-network.qmd#fig-early-stopping)

Train a big network, forty units, for 8,000 steps. Its training error falls the whole
way.

## Scene 26
visual: manim Stopping: the validation minimum at step 1,937, then 4% worse by the end

Validation error is lowest at step 1,937, and 4% worse by the end. Keep the weights
from the best step: that is early stopping.

## Scene 27
visual: manim Seeds: ten runs, identical but for the seed, as dots on a validation-error axis (page results)

Now train the same network ten times, changing only the random seed.

## Scene 28
visual: manim Seeds: the spread, about 0.05, marked

Validation error varies by about 0.05. Two models closer than that have not been told
apart.

## Scene 29
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. A network can fail without a warning: standardise, watch the validation
error, and report the spread over seeds.

# The puzzle, solved

## Scene 30
visual: manim Window: the mean-only baseline at 4.402 and the oracle at 3.701 (page results, how-much-data.qmd)

Back to the puzzle. Predicting the average scores 4.402. A model that knew the true
expected count at every station would score 3.701.

## Scene 31
visual: manim Window: the band between them shaded, "0.70: all there is to learn"

Everything any method can learn lives in that window of 0.70. The rest is noise.

## Scene 32
visual: manim Curves: test error against training stations for four models, the band shaded (page results, how-much-data.qmd#fig-learning-curves)

The forest wins at every size. The eight-unit network never even reaches the window.

## Scene 33
visual: manim Curves: the tuned network's line, labelled "one hidden unit, penalty 1"

Cross-validation, allowed to choose, cut the network down to one hidden unit, with the
heaviest penalty: almost a straight line.

## Scene 34
visual: manim NoiseFree: the target switched from the counts to the true expected count (schematic)

Now take the noise away. Train on the true expected count instead of the counts.

## Scene 35
visual: manim NoiseFree: bars at 480 stations, network 1.88 against linear 2.47, "24% better" (page results)

The eight-unit network now beats linear regression by 24%. It had learned the true
shape all along.

## Scene 36
visual: manim Signal: "short of rows" struck out, "short of signal" ticked
pause-after: 0.5

So it was not short of rows. It was short of signal.

# When a network wins

## Scene 37
visual: manim Band: 200 stations on a temperature–salinity diagram, the core stations in a diagonal band (page results, when-to-use-one.qmd)

Now a constructed case. A water mass is a diagonal band on a temperature–salinity
diagram.

## Scene 38
visual: manim Boundaries: logistic regression's single line, the tree's blocks, the forest's staircase, with their AUCs (page results, when-to-use-one.qmd#fig-boundaries)

Logistic regression can draw one straight line: 0.715. Trees cut along one axis at a
time. A forest of 500 reaches 0.926.

## Scene 39
visual: manim Boundaries: the network's clean diagonal stripe, 17 weights, 0.998

A network with seventeen weights reaches 0.998.

## Scene 40
visual: manim Units: each hidden unit's line drawn on the plane, two along the band's edges

Each hidden unit is a weighted sum: a new axis, at any angle. Two of them, one at each
edge, make the stripe.

## Scene 41
visual: manim Sizes: AUC at 100, 400 and 1,600 stations, network and forest (page results)

On just 100 stations, the network reaches 0.994. The forest needs 1,600 to reach
0.996.

## Scene 42
visual: manim Combination: "salinity − 0.16 × temperature" as a column (schematic)

If you can name the combination, add it as a column and use a simpler model. A network
searches for the ones you cannot name.

## Scene 43
visual: manim Images: pixels into an edge, edges into a shape (schematic)

That is images and sound: an edge is a combination of pixels, and nobody can write
them all down.

## Scene 44
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. A network is the right tool when there is signal to spare, and a
combination you cannot name.

# Quiz

## Scene 45
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A network has ten hidden layers of a hundred units, and every activation
is the identity. What shapes can it fit?

## Scene 46
visual: manim QuizAnswer: the ten layers fold into one straight line (schematic)

Only a straight line. A weighted sum of weighted sums is still a weighted sum.

# Key points

## Scene 47
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: a network is sums with a bend.

## Scene 48
visual: manim KeyPoints: the second ticked

Two: it can fail without a warning.

## Scene 49
visual: manim KeyPoints: the third ticked

Three: it needs signal, not just rows.

## Scene 50
visual: manim EndCard: the site's address and a thank-you

The pages for this section, with all the code, are linked below. Thanks for watching.
