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

## 5. Generalisation and model complexity
`chapters/05-generalisation/` · categories: `generalisation`

- Training performance versus performance on new data
- Underfitting and overfitting
- Bias–variance trade-off
- Model complexity
- Regularisation
- Hyperparameter selection

## 6. Model assumptions and limitations
`chapters/06-assumptions-limitations/` · categories: `assumptions`

- Independence of observations
- Linearity and nonlinearity
- Distributional assumptions
- Spatial and temporal dependence
- Uneven sampling and extrapolation
- Class imbalance
- When standard validation methods are inappropriate
- Limitations of predictions outside the observed data range

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
