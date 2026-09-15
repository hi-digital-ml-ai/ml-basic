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
`chapters/07-validation/` · categories: `validation`

- Cross-validation
- Spatial and temporal cross-validation
- Regression performance measures
- Classification performance measures
- Confusion matrix, precision, recall, and related measures
- Uncertainty and stability of model results
- Selecting evaluation measures appropriate to the scientific objective

## 8. Unsupervised learning
`chapters/08-unsupervised-learning/` · categories: `unsupervised`

- Clustering
- Principal component analysis
- Dimensionality reduction
- Pattern detection in marine datasets
- Interpretation and limitations of unsupervised methods

## 9. Introduction to neural networks
`chapters/09-neural-networks/` · categories: `neural-networks`

- Neurons, layers, weights, and activation functions
- Forward propagation and backpropagation
- Loss functions and gradient descent
- Strengths, limitations, and data requirements
- When neural networks are — and are not — appropriate

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
- **Spatial/temporal dependence** (§6) drives the choice of resampling scheme (§7)
  and is the most common mistake in marine applications.
- **Gradient descent** (§4) is reused directly by neural networks (§9).
- **Extrapolation limits** (§6) frame the responsible-use discussion (§10).
