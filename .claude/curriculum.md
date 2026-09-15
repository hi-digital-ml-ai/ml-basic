# Curriculum

The ten course sections and their subtopics. **Tentative** — content, ordering and
page splits can change; update this file when they do, and keep
`_quarto.yml` and `.claude/site-structure.md` in step.

Each section is one folder under `chapters/`. Each subtopic is normally one `.qmd`
page; short subtopics may be merged into a sibling page rather than left thin.

---

## 1. Introduction to machine learning in marine science
`chapters/01-introduction/` · categories: `foundations`

- What machine learning is, and how it differs from traditional statistical modelling
- Examples of machine-learning applications in marine science
- Main types of learning: supervised, unsupervised, neural-network-based
- Prediction versus explanation and scientific inference

## 2. Understanding and preparing marine datasets
`chapters/02-marine-data/` · categories: `data-preparation`, `marine-data`

- Observations, features, responses, and labels
- Continuous, categorical, spatial, temporal, and profile data
- Exploratory data analysis before modelling
- Missing values, outliers, measurement errors, and class imbalance
- Feature scaling, transformation, and encoding
- Training, validation, and test datasets
- Avoiding information leakage

**Written, with one change from the original outline:** exploratory analysis moved
*ahead* of missing values and outliers. You find the sentinel values and the impossible
depths by looking, so the looking has to come first; the cleaning page then acts on what
the EDA page found. The subtopics are otherwise as listed.

Circular data (month, day of year, bearing, tidal phase) was added to the data-types
page. It is not in the original outline and it is a genuine marine trap.

## 3. Supervised learning
`chapters/03-supervised-learning/` · categories: `supervised`, `regression`,
`classification`, `trees-ensembles`

- Regression and classification problems
- Linear and polynomial regression
- Logistic regression
- Decision trees, random forests, and boosting
- Choosing a method according to the scientific question and dataset

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

Three deliberate spillovers outside the section's own subject:

- Gradient descent carries the *real* justification for §2's scaling advice (a factor of
  about ninety in iterations on this data). §2 could only assert it.
- MAP derives ridge regression, which §5 will then present as a technique. The two pages
  must stay consistent: §5 should refer back rather than re-deriving.
- `reading-a-fit.qmd` uses §2's leaked `catch_weight_kg` column to produce separation, and
  measures random-forest run-to-run noise (0.037 RMSE) as the resolution limit for §3's
  ten-model comparison.

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

Every page before the last deliberately chooses its complexity by looking at the test set,
and says so each time; `hyperparameter-selection.qmd` is where that is done properly. Keep
that framing if these pages are edited — it is what makes §7 feel necessary rather than
pedantic.

`regularisation.qmd` must not re-derive ridge and lasso from scratch: §4's
[MAP page](../chapters/04-how-algorithms-learn/map-and-priors.qmd) derives them from priors,
and §5 refers back. The same applies in reverse if §4 is edited.

### New dataset: `data/coastal-survey-truth.csv`

`bias-variance.qmd` needs the true expected count per station, which observed counts cannot
supply. `R/make-example-data.R` now also writes `data/coastal-survey-truth.csv`
(`station_id`, `true_mean`), loaded by `load_coastal_survey_truth()`. The addition does not
change `coastal-survey.csv` — same seed, same bytes, verified.

Rules for using it are in `data/README.md`: join on `station_id`, never pass it to a model,
never quote a score against it without saying no real study could compute one.

## 6. Model assumptions and limitations
`chapters/06-assumptions-limitations/` · categories: `assumptions`, `spatial-temporal`,
`class-imbalance`

- Independence of observations
- Linearity and nonlinearity
- Distributional assumptions
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
  `sampling-and-extrapolation.qmd` — uneven coverage and extrapolation are the same problem
  at two severities and read badly when separated.

### Two threads that must be kept if these pages are edited

**RMSE is not comparable across resampling schemes.** Three pages hit this and each says so.
Different folds or splits hold different distributions of the response, so a "harder" scheme
can report a *lower* RMSE. Use R², or the same test set for both. §3's leakage page found it
first; §6 repeats it deliberately.

**A better fit is not a more correct model.** `linearity-and-nonlinearity.qmd` turns on this:
the GAM has the best AIC of three models by a wide margin and the most wrong depth response,
because depth is confounded with temperature, chlorophyll and an unmodelled spatial field.
Flexibility buys shape, not identifiability.

### Uses of `coastal-survey-truth.csv`

`linearity-and-nonlinearity.qmd` compares fitted smooths against the true generating curves,
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

### Two conventions that hold the section together

Both were adopted to fix problems §6 ran into, and editing either page must keep them.

**Pool the out-of-fold predictions before computing a metric.** Every v-fold scheme holds out
each row exactly once, so pooling gives one metric over identical rows for every scheme. This is
the proper answer to §6's "RMSE is not comparable across resampling schemes" thread, and
`spatial-and-temporal-cv.qmd` depends on it — without pooling, its five-scheme table would not
be a comparison.

**Use the same resamples object for every model compared.** `uncertainty-and-stability.qmd`
quantifies why: unpaired, the GLM-versus-forest interval is 1.54 wide and covers zero; paired on
identical folds it is 0.33 wide.

### Three findings the pages are built on

- **Selection optimism.** `cross-validation.qmd` searches 100 candidate predictor sets drawn
  from 8 real and 20 pure-noise columns. The winner contains three noise columns; nested CV puts
  the honest RMSE 0.38 above what the search reported, and a fixed no-search model beats the
  searched one on all five outer folds. About 0.04 of that gap is bookkeeping (five large folds
  rather than ten small ones), and the page says so.
- **The score is a function of fold separation.** `spatial-and-temporal-cv.qmd` measures the
  median distance from each held-out station to its nearest training station and plots R²
  against it. Blocked CV is not "more correct" — it is a harder question, chosen deliberately.
  Leave-one-year-out sits off the trend because it separates in time, and `survey_year` has no
  effect in the generator, so the diagnostic correctly reports nothing there.
- **Measures disagree, informatively.** `regression-metrics.qmd` and `choosing-a-metric.qmd` are
  a pair: the first shows MAE and RMSE picking different winners because the log-transformed
  model under-predicts the survey total by 31%, the second shows that same model *winning* the
  fifty-station shortlist. Keep both, and keep the mean-only row — it scores a perfect 1.000 on
  the total and has no skill, which is the argument against aggregate-only validation.

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
pages, because the method, the choice of *k* and the choice of algorithm are three separate
decisions and a single page could only gesture at two of them. "Pattern detection in marine
datasets" and "interpretation and limitations" became one page, `interpreting-patterns.qmd`,
because the honest way to teach pattern detection is to detect a pattern and then interrogate
it — separating them would have produced one credulous page and one abstract one.

### A second dataset

§8 needs many correlated columns, which the single-species survey does not have, so
`R/make-community-data.R` generates `data/coastal-community.csv`: the same 800 stations with
counts of 24 benthic taxa. It joins on `station_id`, so the environment is the survey's.

Two things are built into it and every page depends on the contrast:

- **Depth is a continuum.** Taxon depth optima are spread evenly from 20 m to 160 m, so
  composition turns over smoothly and there are no depth-defined assemblages.
- **Substrate is a genuine split.** Six taxa are effectively hard-bottom only, eight
  soft-bottom only. The one real grouping of stations is hard versus soft — two groups.

Three taxa (`tax22`–`tax24`) respond to nothing, like salinity in the survey. They load at
zero on both principal components, which is how `principal-component-analysis.qmd` shows PCA
ignoring noise columns unprompted.

### Two conventions that hold the section together

**Run the identical pipeline on a structure-free null.** Shuffle each column independently:
every variable keeps its own distribution, all co-occurrence is destroyed. Almost no
unsupervised statistic can be read on an absolute scale, and this is what supplies the scale.
It is used for cluster-count selection, for parallel analysis, and for UMAP. `clusGap()`'s
default uniform-bounding-box reference chose six clusters against the permutation null's two —
keep that example, it is the argument for choosing your own null.

**Validate against a variable the method never saw, and mind its type.** Agreement with a
*categorical* external variable is evidence of groups; agreement with a *binned continuous* one
is evidence only of a gradient. This asymmetry is the whole of `interpreting-patterns.qmd`.

### Three findings the pages are built on

- **Stability is necessary, not sufficient.** The most stable result in the section
  corresponds to nothing: splitting the soft-bottom stations by depth reproduces at ARI 0.890,
  never below 0.71, and the generator contains no soft-sediment assemblages. A stable algorithm
  cuts a stable gradient in a stable place. This is the section's headline and the reason the
  community data was built with a continuum in it.
- **Bimodal stability.** The whole-survey bootstrap at *k* = 2 returns 53 replicates recovering
  the substrate split (ARI > 0.9) and 7 recovering a depth split (ARI < 0.15), with nothing in
  between; the mean of 0.881 describes neither. Keep the histogram — it is the argument for
  reporting distributions rather than averages, and it echoes §7's stability page.
- **Defaults decide the answer.** Depth is 99.4% of the raw environmental table's variance;
  `hclust()`'s default complete linkage scores 0.332 at *k* = 2 where Ward scores 0.889; the
  "80% of variance" rule keeps 16 of 24 components where cross-validated prediction needs 2.
  Every page names a default and shows what it costs.

### Aimed at §9 and §10

`interpreting-patterns.qmd` hands two things forward. To §9: an autoencoder is PCA without the
linearity and inherits every interpretation problem on that page. To §10: a single number from
a single run, reported without its distribution, is how a plausible result becomes a wrong one.

## 9. Introduction to neural networks
`chapters/09-neural-networks/` · categories: `neural-networks`

- Neurons, layers, weights, and activation functions
- Forward propagation and backpropagation
- Loss functions and gradient descent
- Strengths, limitations, and data requirements
- When neural networks are — and are not — appropriate

**Written as six pages, reframing one subtopic and adding one.** "Loss functions and
gradient descent" is §4's material, so §9's version is `training-a-network.qmd`: the four
decisions (learning rate, input scale, when to stop, which seed) that §4 did not have to
face because its loss surfaces were convex. The added page is `autoencoders.qmd`, which
§8's `interpreting-patterns.qmd` explicitly promised — it is also the only unsupervised
network, and the easiest network to check, because a linear one has a closed-form answer.

### The engine decision

**No `torch`, `brulee` or `keras`.** Everything here runs on `nnet` (already installed for
§3) plus about forty lines of base R. That was a deliberate choice, not a constraint: a
hand-written forward/backward pass whose gradients are checked against finite differences
teaches backpropagation far better than a framework call, and it costs no system
dependency. If §9 is ever extended to convolutional or recurrent architectures, that
decision has to be revisited — see `.claude/workflow.md`.

One consequence must be kept if these pages are edited: `nnet` optimises with **BFGS, not
gradient descent**, and parsnip maps `epochs` to `maxit` (quasi-Newton iterations). Both
`forward-and-backward.qmd` and `training-a-network.qmd` say so explicitly. Do not let a
later edit imply that `mlp(engine = "nnet")` takes a learning rate.

### Three findings the pages are built on

- **The network was short of signal, not of rows.** `how-much-data.qmd` computes the
  mean-only baseline (4.402) and an oracle that knows every true expected count (3.701), so
  the whole learnable window is 0.70 RMSE. A default eight-unit network never enters it at
  any training-set size — and on the *noise-free* target the same network beats linear
  regression by 24%. It had learned the response surface; negative-binomial noise buried the
  advantage. This is the section's headline and it is why the `coastal-survey-truth.csv`
  diagnostic is worth the page space.
- **A hidden unit is a rotated coordinate.** `when-to-use-one.qmd` builds a water-mass band
  in T–S space — the one place this section steps outside `data/coastal-survey.csv`, and it
  says so in a callout. A four-unit network (17 weights) reaches AUC 0.998 where a 500-tree
  forest reaches 0.926 and logistic regression is capped at 0.72 at every sample size. That
  single property — combinations of inputs, not inputs — is the section's answer to "when
  is a network the right tool", and it is what generalises to images and audio.
- **A linear autoencoder is PCA, exactly.** Same reconstruction error to four decimals,
  canonical correlation 1.000. The nonlinear version reconstructs slightly *worse* and gains
  0.016 in depth R² — the mild arch §8 measured and declined to overstate. Every seed finds
  the same plane and a different basis in it, which is §8's interpretation lesson with PCA's
  guardrails (canonical rotation, variance ordering, determinism) removed.

### Two things that were measured rather than asserted

Both cost a rewrite and both should survive editing.

- **The best straight line through a hump can have the wrong sign.** `what-a-network-is.qmd`
  originally described the zero-unit fit as descending; it ascends, because the cold tail of
  this survey is lower than the warm one. That is now the page's argument, not an erratum.
- **Unscaled inputs make the network lose to a straight line.** 0.763 against 0.680, with no
  warning of any kind. `training-a-network.qmd` measures it with plain gradient descent;
  `nnet`'s BFGS suffers less (0.811 against 0.744) because it estimates curvature, which is
  why the demonstration is hand-written.

### Aimed at §10

Three handovers. Network weights are not reportable quantities, so §10's importance and
partial-effect tools are the *only* route to an effect. Ten identical runs varied by 0.046
in validation MSE, which is §10's reproducibility case made in numbers. And
`when-to-use-one.qmd` ends on a network that ranks almost perfectly (AUC 0.998) while never
predicting a probability outside 0.27–0.73 — a good score and an uncalibrated model, which
is §10's "what can you honestly claim" in miniature.

## 10. Interpretation and responsible application
`chapters/10-interpretation/` · categories: `interpretation`, `reproducibility`

- Feature importance and model interpretation
- Black-box models versus interpretable models
- Reproducibility and transparent reporting
- Communicating uncertainty and limitations
- Practical marine-science examples and exercises

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
- **Groups versus gradients** (§8) is why §6's spatial dependence matters — a smooth field has
  no edges, and every method in the course will invent one if asked.
- **The baseline and the ceiling** (§9) generalise §7's baseline models and §8's
  structure-free null: before fitting anything, find out what no skill scores and what
  perfect skill would score. If they are close, flexibility has nothing to buy.
- **Axis-aligned splitting** is the limitation trees and forests share (§3, §9) and the one
  thing a single hidden unit fixes. It is also why the tree in §9 extrapolates "high
  salinity means core" sideways into empty space — §6's extrapolation thread again.
