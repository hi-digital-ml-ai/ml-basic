# Curriculum

The ten course sections and their subtopics. **Tentative**: content, ordering and
page splits can change; update this file when they do, and keep
`_quarto.yml` and `.claude/site-structure.md` in step.

Each section is one folder under `chapters/`. Each subtopic is normally one `.qmd`
page; short subtopics may be merged into a sibling page rather than left thin.

Two pages sit **outside** the ten sections, in `toolkit/`: a short orientation in R
with tidymodels and the same one in Python with scikit-learn. They teach a library
rather than a concept, so numbering them would have implied they are part of the
argument the course makes. They exist so that the modelling pages can use the pipeline
idiom without stopping to explain it, and so the Python tabs have somewhere to point.

---

## Site-wide revision (from 2026-10-07)

A second pass over every page, after all ten sections had been revised once. The aim
(user, 2026-10-07): give readers a good understanding of general machine-learning
knowledge, clearly and readably, for participants of mixed backgrounds. Three problems
drive it:

- **Redundancy.** Most later pages re-taught an idea an earlier page owned (RMSE, the
  split roles, the bootstrap, why to standardise, the learning rate, ridge, site against
  block cross-validation, the cost threshold) and then added their own part. Pages grew
  from about 1,500 words in §1 to 2,500–3,500 in §6, §7 and §10.
- **A lean towards statistical modelling.** §3, §4, §6 and §10 spent much of their length
  on coefficient intervals, standard errors, p-values, log-likelihoods, overdispersion
  checks and posteriors, and Poisson, negative binomial and GAM models were the default
  models through §6, §7 and §10.
- **Terms used before they were explained**, and R² defined as a share of the variation
  while the code computed `rsq()`, the squared correlation.

Pages may be merged, removed and renamed freely; URLs need no redirects (the user is the
only one working on the site). Every syllabus subtopic keeps a heading somewhere.

### Target pages

| Section | Pages, in order | Change |
| --- | --- | --- |
| 1 Introduction | Types of learning; Prediction and explanation; Applications in marine science; Discriminative and generative models | *Statistical modelling and machine learning* and *Prediction and explanation* merge: the two aims, the line and the tree, the RMSE built by hand, the confounder |
| 2 Marine data | The coastal survey; Kinds of marine data; Exploring and cleaning the data; Scaling and encoding; Splitting the data; Avoiding information leakage | *Observations and features* merges into *The coastal survey*; *Exploring the data first* and *Missing values and outliers* merge (one finds the six problems, the other fixes them); *Splitting* drops its rebalancing section for a link to *Class imbalance* |
| 3 Supervised learning | Linear and polynomial regression; Regression for counts; Logistic regression; k-nearest neighbours; Decision trees; Random forests and boosting; Choosing a method | *Regression and classification* folds into the overview and the linear regression page; **k-nearest neighbours is new** (user, 2026-10-07): the simplest machine-learning method, predicting from the most similar stations, which ties together distance, scaling, k-means and the distance-to-the-survey check |
| 4 How algorithms learn | Loss functions; Finding the parameters; Gradient descent; Likelihood and priors | *Maximum likelihood* and *Priors and ridge regression* merge into one page on where losses and penalties come from, statistics in the maths callouts; *Checking a fit* folds into *Finding the parameters* (did the search work), its seeds part into *Reproducibility* |
| 5 Generalisation | Underfitting and overfitting; The bias–variance trade-off; Regularisation; Hyperparameter selection | *Training error and new data* merges into *Underfitting and overfitting* (same splits, same curve); *Model complexity* folds into *Regularisation* (same random columns); ridge is taught here, §4 only says a penalty is a prior |
| 6 Assumptions | Linearity and nonlinearity; Distributional assumptions; Dependent data; Uneven sampling and extrapolation; Class imbalance | *Independence of observations* and *Spatial and temporal dependence* merge into one page on repeat visits, neighbours and time (the why; the folds go to §7); *Distributional assumptions* becomes what a loss aims at, its prediction intervals moving to *Communicating uncertainty* |
| 7 Validation | Cross-validation; Spatial and temporal cross-validation; Regression performance measures; Classification performance measures; Uncertainty and stability; Choosing measures that match the objective | Same pages; *Spatial and temporal CV* takes the site-against-block comparison from §6; *Classification measures* starts from *Class imbalance* |
| 8 Unsupervised learning | Clustering with k-means; Choosing the number of clusters; Hierarchical clustering; Principal component analysis; How many components to keep; Checking a pattern before reporting it | Same pages |
| 9 Neural networks | Neurons, layers and activations; Forward propagation and backpropagation; Training a network; When a network pays off; Autoencoders | *How much data a network needs* and *When a network is the right tool* merge; *Training a network* drops its repeat of §4's learning-rate lesson |
| 10 Interpretation | Feature importance; Partial effects; Black boxes and interpretable models; Communicating uncertainty; Reproducibility and transparent reporting; From a model to a claim | Same pages; fewer coefficient intervals; the claim is written as a machine-learning report (a score against a baseline, shapes, prediction intervals) |

Fifty-three pages, against sixty-two before. File names may change with the titles.

### One page teaches each idea; the others link to it

| Idea | Taught on | Other pages |
| --- | --- | --- |
| The coastal survey | *The coastal survey* | §1 gives two sentences and a link |
| RMSE | *Prediction and explanation* (built by hand) | Link; *Regression performance measures* compares it with the others |
| R² | The first page that quotes it, as the textbook R² (`rsq_trad()`, `r2_score()`) everywhere | Link |
| Training, validation and test data | *Splitting the data* | Link |
| Parameters and hyperparameters | The term *hyperparameter* on *k-nearest neighbours* (the number of neighbours); the contrast with parameters on *Finding the parameters* | Link |
| Cross-validation | *Hyperparameter selection* | §7's *Cross-validation* starts where it stops; §6 pages link |
| The bootstrap | *Random forests and boosting* | Link |
| Why standardise | *Scaling and encoding* | One line and a link |
| Learning rate, divergence, mini-batches | *Gradient descent* | *Training a network* keeps early stopping, seeds and mini-batches for networks |
| Ridge and the lasso | *Regularisation* | *Likelihood and priors*: a penalty is a prior, nothing more |
| Seeds and run-to-run spread | *Reproducibility and transparent reporting* | Link |
| What a loss aims at (average, median), log counts falling short | *Distributional assumptions* | The measures pages link instead of rebuilding |
| Overdispersion and the negative binomial | *Regression for counts* | Link |
| Rebalancing; sensitivity, specificity, precision | *Class imbalance* | Link |
| False alarms and misses; a threshold from their costs | Named on *Logistic regression*; the rule on *Choosing measures* | Link |
| Site against block cross-validation | *Spatial and temporal cross-validation* | *Dependent data* shows why (the patches in the errors) |
| Extrapolation | *Uneven sampling and extrapolation* | One line each on the method pages |
| Depth confounded with position | Confounding on *Prediction and explanation*; resolved on *Partial effects* | Name it and link |
| The simulated truth as a check | *The coastal survey* | One sentence and a link |

Section overviews keep the thread paragraph ("The section picks up threads ...") to one or
two sentences.

### Decisions (user, 2026-10-07)

- The default models of §6, §7 and §10 move from Poisson, negative binomial and the GAM
  to a random forest and one simple baseline.
- A **glossary**: `glossary.qmd` (sidebar, More) lists every term, and each page opens
  with a collapsed "New terms on this page" box. Both come from one file,
  `_glossary.yml`, through the `{{< new-terms >}}` and `{{< glossary >}}` shortcodes in
  `tools/glossary.lua`. Add a page's terms to the file as the page is revised.

---

## 1. Introduction to machine learning in marine science
`chapters/01-introduction/` · categories: `foundations`

- Types of learning: supervised and unsupervised learning (reinforcement learning
  named, not covered)
- What machine learning is, and how it differs from traditional statistical modelling
- Prediction versus explanation and scientific inference
- Examples of machine-learning applications in marine science
- Discriminative and generative models

**Being revised (from 2026-09-29, `feature/improve-introduction`).** Types of learning
comes first; discriminative and generative models have their own page, last. Examples
use only temperature, salinity and depth, and each method is explained before it is used.

## 2. Understanding and preparing marine data
`chapters/02-marine-data/` · categories: `data-preparation`, `marine-data`

- The coastal survey: the simulated dataset the course uses, its columns and files,
  observations and features (with outcomes and labels)
- Kinds of marine data: continuous, categorical, circular, temporal, spatial, profile
  and compositional
- Exploring and cleaning the data: exploratory analysis, missing values and outliers
  (with measurement errors)
- Scaling and encoding
- Splitting the data: training, validation and test data; class imbalance is a link to
  *Class imbalance* in §6
- Avoiding information leakage

**Revised 2026-09-30** (`feature/improve-marine-data`). A first page introduces the
survey formally; every page is shorter and has one diagram. The pages use only linear
regression as a model, since later sections introduce the others. The survey's true
effects are deliberately not listed; later pages reveal them when checking a model.

**Second pass 2026-10-08** (`feature/revise-marine-data`): six pages, as in the target
table above. *Observations and features* merged into *The coastal survey*; *Exploring
the data first* and *Missing values and outliers* merged into *Exploring and cleaning
the data*, which still finds the problems by looking before it fixes them; *Splitting
the data* links to *Class imbalance* instead of teaching rebalancing. Every term is
defined at first use, with glossary entries. *Avoiding information leakage* names the
term in the overview, since every later section depends on it.

## 3. Supervised learning
`chapters/03-supervised-learning/` · categories: `supervised`, `regression`,
`classification`, `trees-ensembles`

- Regression and classification
- Linear and polynomial regression
- Regression for counts: Poisson and negative binomial
- Logistic regression
- Decision trees
- Random forests and boosting
- Choosing a method according to the scientific question and dataset

**Revision started 2026-09-30** (`feature/improve-supervised-learning`). Seven pages,
one new method each: the old linear, polynomial and count page split into two, and the
old trees, forests and boosting page split into two. Counts come before logistic
regression, so the log scale is introduced on counts and reused for probabilities. The
single tree gets its own page before the ensembles, which build on it. Titles carry no
commas.

**Second pass 2026-10-08** (`feature/revise-supervised-learning`): seven pages, as in
the target table. *Regression and classification* is gone: Types of learning already
names the two tasks and keeps the subtopic's headings (*Presence is a classification*,
*Abundance is a regression*), its marine-outcomes table moved to the overview, overdispersion
lives on *Regression for counts*, and what a count loses as present or absent opens
*Logistic regression*. *k-nearest neighbours* is new, between logistic regression and
the trees, and owns overfitting and the term hyperparameter; *Decision trees* links to
it for the fitting and validation sites, overfitting and flat predictions beyond the
data. *Random forests and boosting* owns the bootstrap. *Choosing a method* compares
seven models (k-nearest neighbours in, the negative binomial out). Every page uses the
textbook R², links RMSE and R² to where they are taught, and says one line on
extrapolation with a link. The video was rebuilt from these pages the same day (see
`videos.md`).

Found during this pass, to fix when those sections are revised:

- **Poisson intervals called too narrow.** Pages still say Poisson regression's
  intervals are too narrow for the survey's counts, a statistical-modelling point the
  revised §3 no longer makes (the §4 and §6 cases went with their pages):
  `black-box-or-not.qmd:66`.
- **Squared-correlation R².** These still compute `rsq()` or a squared correlation:
  §9 `autoencoders.qmd`, §7 `regression-metrics.qmd:67`.

## 4. How machine-learning algorithms learn
`chapters/04-how-algorithms-learn/` · categories: `optimisation`

- Loss and objective functions
- Parameter estimation
- Gradient descent
- Maximum likelihood estimation (MLE)
- Maximum a posteriori estimation (MAP)
- Basic interpretation of model optimisation

**Written, one page per subtopic, in the order listed.** The last subtopic became
`reading-a-fit.qmd`, framed as a diagnostic page rather than a conceptual one, because
"interpreting optimisation" is only useful as a set of things to check.

**Revised 2026-09-30** (`feature/improve-how-algorithms-learn`): the same six pages in the
same order, retitled *Loss functions*, *Finding the parameters*, *Gradient descent*,
*Maximum likelihood*, *Priors and ridge regression* and *Checking a fit*. The file names
are unchanged, since sections 5, 6 and 9 link to them.

**Second pass 2026-10-08** (`feature/revise-how-algorithms-learn`): four pages, in order
*Loss functions*, *Finding the parameters*, *Gradient descent*, *Likelihood and priors*.
*Checking a fit* (`reading-a-fit.qmd`) folded into *Finding the parameters* (separation and
a table of failure signs and fixes); its seeds part went to §10 *Reproducibility*.
*Maximum likelihood* and *Priors and ridge regression* merged into
`likelihood-and-priors.qmd`, statistics kept to the maths callouts; the negative binomial,
standard errors and posterior figure were cut.

Spillovers outside the section's own subject:

- *Gradient descent* carries the real justification for §2's scaling advice: the same
  model takes many times more steps in raw units. §2 could only assert it. Its learning
  rate is tied to boosting's.
- *Likelihood and priors* derives ridge from a Normal prior, which §5 then presents as a
  technique. The two pages must stay consistent: §5 refers back rather than re-deriving.
- *Finding the parameters* uses separation in logistic regression to show a search with
  no lowest point.

## 5. Generalisation and model complexity
`chapters/05-generalisation/` · categories: `generalisation`, `tuning`

- Training performance versus performance on new data
- Underfitting and overfitting
- Bias–variance trade-off
- Model complexity
- Regularisation
- Hyperparameter selection

**Written, one page per subtopic, in the order listed** (complexity before bias–variance,
so the axis is defined before it is decomposed).

**Revision decisions, 2026-10-01** (`feature/improve-generalisation`): the same six pages
in the same order. They replace the old test-set framing ("every page before the last
deliberately chooses its complexity by looking at the test set"):

- Every page uses §2's split by site into fitting, validation and test sites, as §3 does,
  not a random split of stations. Earlier pages choose a setting on the validation sites;
  the test sites are scored once.
- *Underfitting and overfitting* builds on §3's training-versus-validation curve for tree
  depth rather than re-teaching it.
- *Hyperparameter selection* introduces k-fold cross-validation (folds of sites) and shows
  that one validation split picks unstable winners. §2's pointer to cross-validation points
  here; §7's *Cross-validation* page builds on it with spatial and temporal versions.

*Regularisation* teaches ridge regression, the lasso and λ as tools for prediction. §4's
[Likelihood and priors](../chapters/04-how-algorithms-learn/likelihood-and-priors.qmd) only
shows that each penalty is a prior's negative log, and *Regularisation* links there rather
than repeating it. The same applies in reverse if §4 is edited.

### New dataset: `data/coastal-survey-truth.csv`

`bias-variance.qmd` needs the true expected count per station, which observed counts cannot
supply. `R/make-example-data.R` now also writes `data/coastal-survey-truth.csv`
(`station_id`, `true_mean`), loaded by `load_coastal_survey_truth()`. The addition does not
change `coastal-survey.csv`: same seed, same bytes, verified.

Rules for using it are in `data/README.md`: join on `station_id`, never pass it to a model,
never quote a score against it without saying no real study could compute one.

## 6. Model assumptions and limitations
`chapters/06-assumptions-limitations/` · categories: `assumptions`, `spatial-temporal`,
`class-imbalance`

- Linearity and nonlinearity
- Distributional assumptions
- Independence of observations
- Spatial and temporal dependence
- Uneven sampling and extrapolation
- Class imbalance
- When standard validation methods are inappropriate
- Limitations of predictions outside the observed data range

**Written as six pages, merging two pairs of subtopics:**

- "When standard validation methods are inappropriate" is folded into
  `spatial-and-temporal-dependence.qmd`, which is where the demonstration lives, with the
  remedy pointed forward to §7.
- "Limitations of predictions outside the observed data range" is folded into
  `sampling-and-extrapolation.qmd`, because uneven coverage and extrapolation are the same problem
  at two severities and read badly when separated.

**Revision decisions, 2026-10-02** (`feature/improve-assumptions-limitations`): the same
six pages, reordered. The first two cover what a model assumes about shape and spread,
which machine learning relaxes; the next three cover how the data were collected, which
it does not.

- Every page uses §2's split by site and §5's cross-validation by site, not AIC or a
  random split.
- Material earlier sections now teach is cut, not repeated: pseudo-replication and the
  split by site (§2), overdispersion and the negative binomial (§3), Poisson standard
  errors that are too small (§4), random against grouped cross-validation (§5).
- *Linearity and nonlinearity* is framed for a machine-learning course: linearity is an
  assumption of linear models, which trees and forests drop. It checks the assumption by
  dividing caught by predicted along each input (temperature shows a hump), then
  draws the curves of a random forest and a GAM, which drops the straight lines but keeps one
  readable curve per input (smooth bumps with a penalty on bending, tied to §5's
  penalty; no effective degrees of freedom), against the simulation's curves. §10's revision dropped
  effective degrees of freedom too. *Distributional
  assumptions* is framed the same way: most machine-learning models predict without
  Normal errors or equal spread, but the distribution decides what a prediction means
  and how sure it can be. One random forest throughout: its cross-validated errors fail
  both checks; trained on log counts it scores the same RMSE but predicts about 30% too
  few animals (it aims at the median, not the average); a Normal interval reaches below
  zero, while a quantile forest's intervals widen where the catches do. Generative
  models get one sentence (§1 covers them). Simulating from Poisson and negative
  binomial models was cut (2026-10-02); the negative binomial model is now credited to
  §3's *Count regression* on the pages that reuse it.
  *Independence* shrinks to effective sample size and its cost to standard errors.
  *Spatial and temporal dependence* compares cross-validation by site against spatial
  blocks and diagnoses with a residual map, not Moran's I. *Extrapolation* replaces
  Mahalanobis distance with the distance to the nearest surveyed station. *Class
  imbalance* introduces sensitivity, specificity and precision; ROC AUC and PR AUC stay
  in §7.
- **One to three worked-example parts per page, each on the page's topic** (user,
  2026-10-02: four was too many; give good, easy examples and leave the rest for
  learners to pursue). Cut that day: linearity's scores of four models on their own
  stations and new sites (a §5 lesson) and its Poisson model with squared terms (left
  as an exercise); spatial's count of fitted sites within 30 km (the diagram makes the
  point); extrapolation's ratio table (two sentences under the depth figure keep its
  numbers). Extrapolation then dropped the negative binomial model, which behaved like
  polynomial regression past the data, leaving two methods.
- Running Python tabs on every page. scikit-learn has no GAM: its tab uses
  `SplineTransformer` with a ridge-penalised `PoissonRegressor`.

**Second pass 2026-10-09** (`feature/revise-assumptions`): five pages, as in the target
table. The default models are a random forest and one simple baseline; statistics stay
out unless the lesson needs them.

- *Linearity and nonlinearity*: linear regression's errors averaged along each input
  show where a straight line fails, and a random forest finds the temperature curve.
  The GAM moved to §10 *Black boxes and interpretable models* (with `gam.svg`). The
  linear model scored no worse than the forest on the test sites (RMSE 3.75 against
  3.98), so the page claims no win for the forest.
- *Distributional assumptions*: two parts, the forest's errors skewed and widening, and
  log counts aiming at the median (about 30% too few animals in total). The quantile
  forest's intervals moved to §10 *Communicating uncertainty*.
- *Dependent data* merges *Independence of observations* and *Spatial and temporal
  dependence*: resampling stations, whole sites and half-degree spatial blocks measures
  the effective sample size of the average catch and of the forest's errors. Cut: the
  negative binomial, the patches map and a position-only forest (a permutation check
  found no clustering of errors beyond chance). The spatial-blocks diagram moved to §7
  *Spatial and temporal cross-validation*, which now owns the folds.
- *Uneven sampling and extrapolation*: how each method carries on past the data is §3's
  (*Choosing a method* draws it), so the page links there and gives its own diagram to
  the range check against the distance to the nearest surveyed station, which it ties
  to k-nearest neighbours.
- *Class imbalance*: false alarm and miss are §3's terms and are linked, not bolded.

Every page has glossary entries and a new-terms box.

### Two threads that must be kept if these pages are edited

**RMSE is not comparable across resampling schemes.** Different folds or splits hold
different distributions of the response, so a "harder" scheme can report a *lower* RMSE.
Use R², or the same test set for both. §2's leakage page found it first. No §6 page
compares schemes any more; §7's `spatial-and-temporal-cv.qmd` does, and must keep it.

**A curve that fits the data can still be wrong.** The forest recovers the temperature hump
but puts depth's peak in shallow water, because depth is confounded with position, which
carries an unmodelled spatial field. Since the 2026-10 beginners' pass this lives only in
§10's `partial-effects.qmd` (with §1 teaching confounding); `linearity-and-nonlinearity.qmd`
stays on the straight line against the forest's temperature hump.

### Uses of `coastal-survey-truth.csv`

`partial-effects.qmd` compares the forest's curves against the true generating curves,
and `sampling-and-extrapolation.qmd` measures extrapolation bias against `true_mean` rather
than observed counts. Both say in the text that no real study could do this.

## 7. Model validation and performance assessment
`chapters/07-validation/` · categories: `validation`, `metrics`, `uncertainty`

- Cross-validation
- Spatial and temporal cross-validation
- Regression performance measures
- Classification performance measures
- Confusion matrix, precision, recall, and related measures
- Uncertainty and stability of model results
- Selecting evaluation measures appropriate to the scientific objective

**Written as six pages, merging one pair of subtopics:** "classification performance measures"
and "confusion matrix, precision, recall" are the same material and read badly apart, so they
are one page, `classification-metrics.qmd`, organised around the matrix as the object and every
threshold-dependent measure as a ratio of its four cells.

**Revision decisions, 2026-10-03** (`feature/improve-validation`): the same six pages,
in three pairs: the folds (cross-validation, spatial and temporal), the measures
(regression, classification), and what to report (uncertainty, choosing a measure).

- Every page uses the same ten folds of sites (`set.seed(61)`, `group_vfold_cv(survey,
  group = site_id, v = 10)`; Python `GroupKFold(n_splits=10, shuffle=True,
  random_state=61)`) and scores the pooled out-of-fold predictions. Pages 3 to 6 share
  their models: predicting the average, Poisson regression, a random forest and the
  forest on log counts for counts; logistic regression and the forest for presence.
- Each worked example runs in about a minute per tab, with no caching (user, 2026-10-03:
  a Python tab that took 30 minutes was an analysis, not an example). Repeated schemes
  and large grids were cut to fit.
- *Cross-validation*: five or ten folds are enough; the pooled score, not the average of
  the folds'; selection optimism from a search over 100 sets of inputs with noise
  columns, and nested cross-validation to score the search.
- *Spatial and temporal cross-validation*: the score depends on the distance to the
  nearest fitted station; a correlogram of the errors sets the block width (half-degree
  blocks); an expanding window for forecasts. Schemes are compared over ten runs, since
  single runs overlap.
- *Regression performance measures*: RMSE, MAE, Poisson deviance and R², what each is
  lowest at; the squared correlation (`rsq()`) against the textbook R² (`rsq_trad()`);
  MAE would scale the forest's predictions down. MAPE is dismissed for counts.
- *Classification performance measures*: calls at one threshold, the ranking (ROC AUC)
  and the probabilities (log loss, with a calibration plot). F1 cannot tell the models
  from calling every station present. Sensitivity, specificity and precision come from
  §6's *Class imbalance* and are not taught again.
- *Uncertainty and stability*: a bootstrap of the sites over the pooled out-of-fold
  predictions, without refitting, and a paired comparison on the same draws.
- *Choosing measures that match the objective*: a table of uses and their measures; a
  shortlist scored on the animals it finds against a perfect and a random one (the
  forest on log counts predicts 69% of the catch yet finds as many as the others); the
  expected cost of the calls, with the cheapest threshold at k/(1+k) for calibrated
  probabilities. The mean-only total argument is on page 3 and is not repeated.

**Second pass from 2026-10-09** (`feature/revise-validation`): the same six pages.
Decisions agreed with the user:

- Poisson regression leaves the section. Counts use predicting the average (no skill),
  linear regression (the simple baseline) and the random forest, with the forest on log
  counts only where a measure's point needs it (*Regression performance measures*,
  *Choosing measures*). Presence keeps the share present, logistic regression and the
  forest.
- *Cross-validation*: the search and nested cross-validation use linear regression. Its
  selection optimism on the full survey is small (nested 4.46 against a claim of 4.43),
  and the page says so: the search still keeps noise columns and loses to the eight
  inputs, and optimism grows with more candidates, flexible models and fewer sites
  (user, 2026-10-09: show the honest small effect, not a 40-site subset or Poisson).
- *Regression performance measures*: two parts; the Poisson deviance leaves the table
  (linear regression can predict below zero) and the scaling curves go (they restate
  *Distributional assumptions*). The R² section says other software often reports the
  squared correlation; the course uses the textbook R² throughout.
- *Spatial and temporal cross-validation* keeps the correlogram but drops "patches": the
  errors' correlations are weak (about 0.04 up to 40 km).
- *Choosing measures*' table is the one place that matches a use to a measure; pages 3
  and 4 link to it. False alarm and miss link to *Logistic regression*.

### Two conventions that hold the section together

**Pool the out-of-fold predictions before computing a metric.** Every v-fold scheme holds out
each row exactly once, so pooling gives one metric over identical rows for every scheme. This is
the proper answer to §6's "RMSE is not comparable across resampling schemes" thread, and
`spatial-and-temporal-cv.qmd` depends on it.

**Use the same folds for every model compared.** `uncertainty-and-stability.qmd` shows why:
paired on the same draws, the difference between two models has a much narrower interval than
either model's own score.

### Aimed at §10

`choosing-a-metric.qmd` ends on observation bias: a model that reproduces biased survey data
reproduces the bias, and no validation scheme detects it. That is the handover to §10.

## 8. Unsupervised learning
`chapters/08-unsupervised-learning/` · categories: `unsupervised`, `interpretation`

- Clustering
- Principal component analysis
- Dimensionality reduction
- Pattern detection in marine datasets
- Interpretation and limitations of unsupervised methods

**Written as six pages, splitting one subtopic and merging two.** "Clustering" became three
pages: k-means (`clustering.qmd`), the number of clusters (`choosing-the-number-of-clusters.qmd`)
and hierarchical clustering (`hierarchical-clustering.qmd`, which also introduces the adjusted Rand
index the later pages use). PCA is `principal-component-analysis.qmd`; "dimensionality
reduction" is `dimensionality-reduction.qmd`, on how many components to keep, ending with
UMAP briefly. "Pattern detection in marine datasets" and "interpretation and limitations"
became one page, `interpreting-patterns.qmd` ("Checking a pattern before reporting it"),
because a pattern is best taught by detecting one and then checking it. Gaussian mixtures
were dropped in the 2026 revision: they added a method without adding a lesson.

### A second dataset

§8 needs many correlated columns, which the single-species survey does not have, so
`R/make-community-data.R` generates `data/coastal-community.csv`: the same 800 stations with
counts of 24 benthic taxa. It joins on `station_id`, so the environment is the survey's.

Two things are built into it and every page depends on the contrast:

- **Depth is a continuum.** Taxon depth optima are spread evenly from 20 m to 160 m, so
  composition turns over smoothly and there are no depth-defined assemblages.
- **Substrate is a genuine split.** Six taxa are effectively hard-bottom only, eight
  soft-bottom only. The one real grouping of stations is hard versus soft: two groups.

Three taxa (`tax22`–`tax24`) respond to nothing, like salinity in the survey. They sit at the
centre of the loadings plot in `principal-component-analysis.qmd`, which is how that page shows
PCA giving noise columns almost no weight unprompted. The pages never state these facts as
given; they find them, and refer to the simulation only to check a result.

### Two conventions that hold the section together

**Run the same steps on a shuffled copy of the data.** Shuffle each column on its own: every
column keeps its values, and which values occur together is lost. Silhouette widths and shares
of the variance have no fixed scale, and this supplies one. It is used for the number of
clusters (silhouette 0.179 at *k* = 2, 3.5 times the shuffled value), for parallel analysis
(three components) and for UMAP.

**Check against a variable the method never saw, and mind its type.** Agreement with a
recorded *category* is evidence of groups; agreement with a continuous variable cut into bands
shows only a gradient. `interpreting-patterns.qmd` makes this its third check.

### Three findings the pages are built on

- **Coming back is not enough.** Splitting the soft-bottom stations comes back in every
  site bootstrap (lowest ARI 0.69), yet the generator has no soft-bottom assemblages.
  `interpreting-patterns.qmd` tells it apart from the seabed split without revealing the
  truth: projected onto the line between the two centres, 11% of soft-bottom stations sit
  within 0.1 of the boundary against 2% for the seabed split, and the position correlates
  0.87 with depth.
- **Two answers, not one average.** The bootstrap by site (`group_bootstraps()`, as in §6)
  at *k* = 2 gives 52 refits with the seabed split and 8 with a depth split; the average ARI
  of 0.87 describes neither. Keep the histogram: it is the argument for reporting how often
  each answer came back.
- **Settings decide the answer.** The linkage rule alone moves agreement with the seabed from
  0.005 (single) to 0.89 (Ward), and tidyclust and scikit-learn have different defaults; the
  80% rule keeps 16 components, the shuffled baseline 3, cross-validation for depth 2.

## 9. Introduction to neural networks
`chapters/09-neural-networks/` · categories: `neural-networks`

- Neurons, layers, weights, and activation functions
- Forward propagation and backpropagation
- Loss functions and gradient descent
- Strengths, limitations, and data requirements
- When neural networks are, and are not, appropriate

**Written as six pages, reframing one subtopic and splitting another.** "Loss functions and
gradient descent" is §4's material, so §9's version is `training-a-network.qmd`: the
settings (learning rate, when to stop, which seed) that §4 did not have to face because its
loss surfaces were convex. "Strengths, limitations, and data requirements" and "when
appropriate" became `how-much-data.qmd` and `when-to-use-one.qmd`, the first measuring a
case where the network does not lead and the second one where it does. The added page is
`autoencoders.qmd`, which follows on from §8's `principal-component-analysis.qmd`: the
only unsupervised network, and the easiest to check, because a linear one gives PCA's
answer.

Revised in October 2026 (`feature/improve-neural-networks`). Page order and titles:
Neurons, layers and activations; Forward propagation and backpropagation; Training a
network; How much data a network needs; When a network is the right tool; Autoencoders.
The section is R-only: no Python tabs.

**Second pass 2026-10-10** (`feature/revise-neural-networks`): five pages, as in the
target table. Decisions agreed with the user:

- *How much data a network needs* and *When a network is the right tool* merge into
  `when-a-network-pays-off.qmd`. The learning curves, the cross-validated tuning and
  `learning-curves.svg` go, so the page runs in about half a minute: linear regression,
  the forest and the network are fitted once, scored on the counts, then trained again
  on the true mean counts (§6's term, replacing "expected counts"). The water-mass band
  keeps its 100/400/1,600-station table, and the closing checklist covers both signal
  against noise and combinations nobody can name.
- *Training a network* drops its learning-rate sweep, §4's lesson, for one paragraph
  linking to *Gradient descent* and *Scaling and encoding*; early stopping and the seeds
  stay as the worked parts, mini-batches and epochs as prose, with a redrawn diagram.
- Every page gets a new-terms box. *Autoencoders* computes R² with `rsq_trad_vec()`.

### The engine decision

**No `torch`, `brulee` or `keras`.** Everything runs on `nnet` (already installed for §3),
parsnip's `mlp()`, and short base-R networks. That was a deliberate choice, not a
constraint: a hand-written forward and backward pass whose slopes are checked against
small nudges of each weight teaches backpropagation better than a framework call, and it
costs no system dependency. `forward-and-backward.qmd`, `training-a-network.qmd` and
`autoencoders.qmd` each write their own gradient descent. If §9 is ever extended to
convolutional or recurrent architectures, that decision has to be revisited; see
`.claude/workflow.md`.

Two consequences must be kept if these pages are edited:

- `nnet` optimises with **BFGS, not gradient descent**, and parsnip maps `epochs` to
  `maxit`. `forward-and-backward.qmd` and `training-a-network.qmd` both say so. Do not let
  a later edit imply that `mlp(engine = "nnet")` takes a learning rate.
- **parsnip squeezes two-class `nnet` probabilities into 0.269–0.731**, that is
  1/(1 + e) to e/(1 + e): `parsnip:::nnet_softmax()` turns nnet's single output p into
  the pair (1 − p, p) and then applies a softmax to it, as if they were scores. The ranking is untouched, so ROC AUC and predicted classes are right,
  but the probabilities are not. `when-a-network-pays-off.qmd` therefore reports AUC and draws
  predicted classes, never probability maps or calibration. The old page's "a good score
  and an uncalibrated model" lesson was this artefact, not a property of networks.

### Three findings the pages are built on

- **The network was short of signal, not of rows.** `when-a-network-pays-off.qmd` fits
  linear regression, a random forest and an eight-unit network once on the survey's 539
  training stations. On the counts the forest leads (4.20) and the network is last
  (4.52, against 4.72 for predicting the mean). Trained on the true mean counts of the
  same stations and scored against them, the network comes first (1.43, forest 1.62,
  linear regression 2.12; 33% better than linear regression): the count noise buried the
  gain. This is the section's headline; the page says the true mean counts are available
  only because the survey is simulated.
- **A hidden unit bends along a tilted line.** The same page simulates a water-mass
  band in T–S space, the one place this section steps outside the course datasets. A
  two-unit network (9 weights) reaches ROC AUC 0.999 from 200 stations where a 500-tree
  forest reaches 0.926 and logistic regression stays near 0.72 at every size; the forest
  needs about 1,600 stations to come close. Adding the named combination as a column
  (feature engineering) lets logistic regression match the network. Combinations of
  inputs nobody has named is the section's answer to "when is a network the right tool",
  and what carries over to images, spectra and sound.
- **A linear autoencoder is PCA.** Same reconstruction error to four decimals, and its
  code predicts both principal components with R² 1.000 (regression R², not canonical
  correlation, which the course has not introduced). The tanh version predicts depth only
  slightly better than PCA's two components (0.743 against 0.727), because the community
  changes almost in straight lines. Every seed finds the same plane with different axes in
  it, which is §8's interpretation lesson with PCA's ordering and determinism removed.

### Measured on the pages, kept positive

- `what-a-network-is.qmd`: two hidden units (7 weights) find the temperature optimum
  without being told its shape; one is not enough and more add little.
- `forward-and-backward.qmd`: all 21 hand-written slopes agree with the nudged ones to 10
  decimal places, and a run can pause on a plateau before it beats a straight line.
- `training-a-network.qmd`: early stopping keeps step 1,937 of 8,000, and the last step's
  validation error is 4% worse; ten seeds vary by 0.055 in validation MSE, and
  their average beats seven of them. The learning rate and standardising are prose with
  links, since *Gradient descent* and *Scaling and encoding* teach them.

### Aimed at §10

Network weights are not reportable quantities, so §10's importance and partial-effect
tools are the route to an effect. Ten identical runs varying by 0.055 in validation MSE is
§10's reproducibility case in numbers.

## 10. Interpretation and responsible application
`chapters/10-interpretation/` · categories: `interpretation`, `reproducibility`

- Feature importance and model interpretation
- Black-box models versus interpretable models
- Reproducibility and transparent reporting
- Communicating uncertainty and limitations
- Practical marine-science examples and exercises

**Written as six pages, splitting the first subtopic and turning the last into a capstone.**
"Feature importance and model interpretation" became two pages, because a ranking and a shape
are different objects with different failure modes and one page could only do the ranking.
"Practical marine-science examples and exercises" became `from-model-to-claim.qmd`, which
takes the survey through the whole course and ends in the two paragraphs you would actually
write, so the exercises are then attached to something concrete rather than free-floating.

**Revision decisions, 2026-10-07** (`feature/improve-interpretation`): the same six pages,
with *Communicating uncertainty* moved before *Reproducibility*. The first two read a black
box from outside, the next two read a model from its parts and say how sure its predictions
are, and the last two turn the analysis into a report.

- **One method per page, introduced before it is used.** *Feature importance* introduces
  permutation importance on test sites against the forest's impurity importance;
  *Partial effects* introduces partial dependence and ICE curves; *Black boxes and
  interpretable models* reads a GAM from its parts; *Communicating uncertainty* introduces
  confidence and prediction intervals, coverage and conformal prediction; *Reproducibility*
  measures what a seed, a split and cross-validation each move.
- **Every page uses the course's own methods:** the split by site (§2), cross-validation by
  site (§5), the random forest and boosting (§3), the negative binomial model (§3), the GAM
  and the quantile forest (§6). ALE plots, effective degrees of freedom and p-values were cut,
  and the old GLM given the generator's exact form went with them.
- **The truth is revealed only to check a model**, never as a page's starting point.
  *Partial effects* and *From a model to a claim* compare the curves with
  `R/make-example-data.R`; the other pages read the model alone. The old spatial-term
  recovery by subtraction was cut.
- **One to three worked-example parts per page,** each running in about a minute per tab.
  Feature importance keeps three random columns and ten splits; *Black boxes* scores the
  average, boosting, the forest and the GAM on the same ten folds; *From a model to a claim*
  writes its Methods and Results paragraphs entirely in inline R.
- **The overview has no numbers.** Its "Findings from this section" list (GAM 4.08, 29%
  coverage, rock 38% → 69%) was cut with the pages that computed them.
- Running Python tabs on every page. scikit-learn has no GAM or intervals: the tabs use
  `SplineTransformer` with a ridge penalty, statsmodels' negative binomial for intervals,
  and boosting with a quantile loss for the quantile forest.

**Second pass 2026-10-10** (`feature/revise-interpretation`): the same six pages, each
with a new-terms box. Decisions agreed with the user:

- *Black boxes and interpretable models* is trimmed to one interpretable model, the GAM,
  scored against the forest and boosting on the same folds. Poisson regression and the
  multiplier table go; mud and summer are one sentence, and paired comparison is linked.
- *Communicating uncertainty* is rebuilt on the random forest: bootstrap refits of the
  sites give the interval for the average, the quantile forest the interval for a new
  catch, and conformal prediction any model's interval. The GAM, the negative binomial
  and statsmodels leave the page.
- *From a model to a claim* is a random forest report: the cross-validated score against
  predicting the average, the inputs that beat three random columns on most folds,
  partial-dependence shapes, and a 90% quantile-forest interval with its held-out
  coverage, all in inline R. The gear bias moves from rock to **mud**, half the animals
  missed; the rock version (55 stations) is the first Try it yourself exercise. The
  Python tab uses `GradientBoostingRegressor(loss="quantile")` for the interval ends,
  since `HistGradientBoostingRegressor` spent about 5 s per fit on threads with data
  this small.

### Three findings the pages are built on

- **No curve separates what the design confounds.** The simulation's depth peak is at 80 m;
  the forest's partial dependence and the GAM's curve both stay highest in shallow water,
  even with position as an input, because depth follows distance offshore. The temperature
  hump is recovered at nearly every station. *From a model to a claim* turns this into the
  sentence a study can write: the temperature curve is supported, a depth peak is not.
- **Reading cost no accuracy on the survey.** On the same folds of sites the GAM predicted
  new sites as well as the random forest and better than untuned boosting, and its curves
  match the forest's. A black box earns its place where inputs work in combination, inputs
  are raw, or prediction is the whole job.
- **Observation bias defeats validation.** A gear that misses half the animals on mud
  turns the forest's "mud holds 1.10–1.16 times as many as sand" into 0.90–0.95 on every
  fold model, while the cross-validated RMSE falls from 4.41 to 3.86 and the intervals
  still hold 95%.
  This is §7's `choosing-a-metric.qmd` handover landing, and it is the last thing the
  course says: checks on the records come from outside the model.

### Two conventions that hold the section together

**Every importance score needs a null and a repeat.** Three columns of random numbers show
what an unused input scores (impurity importance ranks them above the seabed); ten splits
show which inputs beat them again and again. Report how often an input beats the random
columns, not its rank.

**Name which interval you are quoting and measure its coverage.** An interval for the
average holds few catches at new sites, an interval for a new catch about nine in ten, and
conformal prediction holds its promise only at stations like the calibration sites (the
stations with the most chlorophyll fall short at the same width). Coverage on held-out
sites is the evidence an interval works.

### A trap that caught this section twice

`summarise()` and `tibble()` evaluate arguments in order, so
`summarise(rmse = mean(rmse), lower = quantile(rmse, 0.1))` computes the quantile of the
*new scalar*, silently collapsing every ribbon to its line. The same shadowing bit §7 and §8.
Put derived columns before the column they are derived from, or rename. The revision
met it again in `from-model-to-claim.qmd`, where a column `rock` shadowed a local `rock`.
The rebuilt page computes `folds_better` before `forest_rmse = mean(forest_rmse)` for the
same reason.

---

## Threads that run across sections

Repeat these deliberately rather than treating them as one section's property:

- **Leakage** (§2) reappears in every resampling example (§7).
- **Calibration** (§7) is what makes the cost-based threshold rule $k/(1+k)$ valid, and is the
  property §6's rebalancing destroys.
- **Spatial/temporal dependence** (§6) drives the choice of resampling scheme (§7)
  and is the most common mistake in marine applications.
- **Gradient descent** (§4) is reused directly by neural networks (§9).
- **Extrapolation limits** (§6) frame the responsible-use discussion (§10).
- **Comparing against a structure-free null** (§8) is the same move as §7's baseline models:
  neither a silhouette width nor an R² means anything until you know what no-skill looks like.
- **Groups versus gradients** (§8) is why §6's spatial dependence matters: a smooth field has
  no edges, and every method in the course will invent one if asked.
- **The baseline and the ceiling** (§9) generalise §7's baseline models and §8's
  structure-free null: before fitting anything, find out what no skill scores and what
  perfect skill would score. If they are close, flexibility has nothing to buy.
- **Axis-aligned splitting** is the limitation trees and forests share (§3, §9) and the one
  thing a single hidden unit fixes. It is also why the tree in §9 extrapolates "high
  salinity means core" sideways into empty space, which is §6's extrapolation thread again.
- **Identifiability** (§10) is the limit on everything §6 to §10 do. A confounded design
  cannot be rescued by a better model, a better plot or a bigger sample; the honest output is
  the sentence naming the confounding.
- **Simulation with a known truth** is what makes §5's bias/variance, §8's cluster validity
  and §10's interpretation checks possible at all. Any new dataset added to `data/` should
  come with its generator and, where useful, its truth file.
