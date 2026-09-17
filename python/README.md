# Python tabs

The site is built with R. Every figure and every printed table on a chapter page
comes from the R chunk beside it, and Quarto never executes anything in this
folder. What lives here is the **Python half of the code tabsets**: the
scikit-learn translation of each tidymodels step, so a reader who works in Python
can follow the course without mentally porting every example.

```
mlbasic_data.py      loaders mirroring R/data.R, same files and cleaning
check-snippets.py    runs every Python snippet in the site
requirements.txt     what the snippets need (not needed to build the site)
```

## Why it is real code

Code that is displayed but never run rots quietly. So it is run:

```bash
python -m venv .venv && .venv/bin/pip install -r python/requirements.txt
.venv/bin/python python/check-snippets.py
```

The checker pulls the ```` ```python ```` blocks out of each page in order, joins
them into one program, since the snippets on a page are cumulative exactly as the R
chunks are, and executes it. A page that throws is a failure; a page that only
warns prints the warning, because a convergence warning means the snippet is
teaching something slightly wrong.

Run it after editing any Python tab, and after a scikit-learn upgrade.

## What the numbers do

They differ from the R output, and the note on each page says so. R and Python
draw their random splits from different generators, so `random_state=123` is not
`set.seed(123)` and the fold boundaries are not in the same places. Conclusions
match; third decimal places do not. Nothing here is presented as the result on
the page; the R tab produced those.

## Keeping the two halves honest

- Add a loader here whenever one is added to `R/data.R`, and keep the cleaning
  identical. `load_coastal_survey_clean()` is checked against the R version:
  800 rows, the same missing counts, the same four substrate levels.
- Where scikit-learn's default differs from R's, say so in a comment rather than
  silently matching it. `LogisticRegression` regularises and `glm()` does not;
  `PoissonRegressor` needs scaled inputs where `glm()` does not; `classes_` is
  sorted, so the coefficients describe the opposite class from `glm()`'s.
- Where Python has no equivalent, leave the block R-only rather than inventing
  one. There is no `mgcv`, so the GAM pages use a spline basis and say what that
  costs; `statsmodels` appears only where scikit-learn reports no standard
  errors.
