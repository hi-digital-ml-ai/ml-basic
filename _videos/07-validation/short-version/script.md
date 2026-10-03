---
title: "Validation: scores you can trust"
section: chapters/07-validation/index.qmd
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

This video is a short, encouraging overview for readers from any marine field. It keeps
to what is new in the section, three things a careful reader asks of a score: is it
honest (a search over many models flatters its winner; nested cross-validation scores
the search), does it fit the goal (a shortlist scored by the animals it finds; the
costs of a false alarm and a miss set the threshold), and is one model really better
(compare models in pairs on the same resamples). It leaves out what earlier videos
covered: spatial folds, and totals that fall short on skewed counts.
-->

# In this video

## Scene 1
visual: manim Learn: three points appear one by one as they are spoken
pause-after: 0.5

In this video, you will learn three things. How to keep a score honest. How to choose a
score that fits your goal. And how to tell whether one model is really better.

## Scene 2
visual: manim Fields: a model with its score, surrounded by uses from different marine fields (schematic)

Whether you map seagrass, forecast a fish stock or count plankton, a model comes with a
score: how well it predicts data it has never seen. This section is about making that
score worth trusting.

# Keep the score honest

## Scene 3
visual: manim Search: a hundred candidate models appear, each built from five columns (page results, cross-validation.qmd)

Suppose you try a hundred models and keep the one with the best score. It is a natural
thing to do.

## Scene 4
visual: manim Luck: each score drawn as the model's true skill plus a random nudge; the best of many has the biggest nudge (schematic)

But every score is partly luck. The best of a hundred has had the most luck, so its
score looks better than the model really is.

## Scene 5
visual: manim Search: twenty columns of random numbers among the inputs; the winner picked out, two of its five columns random (page results, cross-validation.qmd)

To see it, we hid twenty columns of pure random numbers among the inputs. The winning
model used two of them.

## Scene 6
visual: manim Nested: an outer fold of sites held out; the whole search runs on the rest; its winner predicts the held-out fold (schematic)

Nested cross-validation gives an honest score. It holds some sites back, runs the whole
search on the rest, and only then scores the winner on the sites it held back.

## Scene 7
visual: manim NestedResult: the score the search claimed, its honest score, and a plain model with no search (page results, cross-validation.qmd#fig-nested)

The search claimed an error of 4.42. Scored honestly, its winners managed 4.86: worse
than a plain model that skipped the search altogether.

## Scene 8
visual: manim KeyPoint: badge 1, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point one. To keep a score honest, score the whole search, not just its winner.

# Choose a score that fits your goal

## Scene 9
visual: manim Uses: three cards, a total, a shortlist, a yes or no (schematic)

Predictions are put to different uses: a total for a stock estimate, a shortlist of
sites to visit, or a yes or no at each site. Each use needs its own score.

## Scene 10
visual: manim Shortlist: stations ranked by a model's prediction; a ship visits the top ones (schematic)

Take the shortlist. A ship has time to revisit 100 stations, and goes where the model
predicts the most animals.

## Scene 11
visual: manim ShortlistResult: animals found by the models' shortlists, between a random hundred and a perfect hundred (page results, choosing-a-metric.qmd)

The models' shortlists find 2.1 times as many animals as 100 stations picked at random.
That is a score a survey planner can act on.

## Scene 12
visual: manim Mistakes: a two-by-two table of called and true presence; "false alarm" and "miss" placed in their cells (schematic)

A yes or no at each site can go wrong in two ways. A false alarm says the species is
there when it is not. A miss says it is absent when it is there.

## Scene 13
visual: manim Costs: a large block for a false alarm, a small one for a miss; the threshold slides up from 0.5 (schematic)

The two rarely cost the same. If a false alarm sends a dive team out for nothing, raise
the bar for saying yes.

## Scene 14
visual: manim KeyPoint: badge 2, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point two. To choose a score, start from what the predictions are for.

# Is one model really better?

## Scene 15
visual: manim OneSurvey: the survey's sites, then other sites it might have drawn, two models' scores moving and swapping (schematic)

A score comes from one survey. With other sites, it would have come out a little
different, and two models might swap places.

## Scene 16
visual: manim Resample: the 160 sites drawn again with replacement; each draw gives one score, a thousand times (page results, uncertainty-and-stability.qmd)

So draw the sites again, a thousand times, and score the models on each draw.

## Scene 17
visual: manim Pairs: two models' scores over a few draws, rising and falling together; their difference below, nearly constant (schematic)

On a hard draw, every model does worse. So compare two models draw by draw: the
difference between them is far steadier than either score.

## Scene 18
visual: manim PairScatter: the forest's score against predicting the average's, one dot per draw, nearly all below the diagonal (page results, uncertainty-and-stability.qmd#fig-pairs)

A random forest beats simply predicting the average in 99 per cent of the draws: a real
difference.

## Scene 19
visual: manim PairScatter: the second panel, against Poisson regression, a narrow band along the diagonal (page results)

Against Poisson regression, it wins only 79 per cent of the time. On this survey, you
cannot yet tell those two apart.

## Scene 20
visual: manim KeyPoint: badge 3, the promise from the opening, and its answer, ticked
pause-after: 0.5

Key point three. To tell whether one model is really better, compare the two in pairs.

# Quiz

## Scene 21
visual: manim Quiz: the question, then a countdown bar through the pause
pause-after: 8

Quick quiz. A false alarm costs three times as much as a miss. Should a station need a
probability above 0.5 to be called present, or below?

## Scene 22
visual: manim QuizAnswer: "Above: 0.75"; logistic regression's cost at every threshold, cheapest at 0.75, with 0.5 marked (page results, choosing-a-metric.qmd#fig-cost)

Above. At 0.75, a station is called present only when presence is three times as likely
as absence. That is where logistic regression's calls cost least on the survey.

# Key points

## Scene 23
visual: manim KeyPoints: the three key points, the first ticked

To sum up the three key points. <short pause> One: keep the score honest.

## Scene 24
visual: manim KeyPoints: the second ticked

Two: choose a score that fits your goal.

## Scene 25
visual: manim KeyPoints: the third ticked

Three: compare models in pairs.

## Scene 26
visual: manim EndCard: the site's address and a thank-you

The pages show how to do all of this in R and Python, with code to try on your own
data. They are linked below. Thanks for watching.
