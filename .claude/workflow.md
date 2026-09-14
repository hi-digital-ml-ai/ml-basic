# Workflow

## Local development

```bash
quarto preview                 # live-reloading site at localhost:4200-ish
quarto render                  # full build into _site/
quarto render chapters/05-generalisation/overfitting.qmd   # one page
```

The site is developed entirely locally. `_site/` is build output and is **not**
committed.

## R environment

`renv` pins package versions so every author renders the same results.

```bash
Rscript -e 'renv::restore()'    # after cloning, or when renv.lock changes
Rscript -e 'renv::snapshot()'   # after adding a package to a page
```

Commit `renv.lock` in the same commit as the page that needs the new package.

Packages beyond tidymodels that the curriculum implies: `ranger`, `xgboost`,
`glmnet`, `vip`, `DALEX`, `themis` (class imbalance), `spatialsample` (spatial CV),
`sf` (spatial data), and `torch` or `keras3` for §9. Install them as sections need
them, not up front.

## Freeze

`_quarto.yml` sets:

```yaml
execute:
  freeze: auto
```

Rendered R results are cached in `_freeze/`, **which is committed**. Consequences:

- A page re-executes only when its source changes, so full builds stay fast.
- CI can render the site with Quarto alone — no R, no package installs, no
  multi-minute model fits on every push.
- If a page's output looks stale after changing a helper in `R/`, delete that page's
  folder under `_freeze/` and re-render.
- Commit `_freeze/` changes together with the page that produced them.

## Branching (gitflow)

| Branch | Role |
| --- | --- |
| `main` | What is published. Only receives merges from `release/*` and `hotfix/*`. |
| `develop` | Integration branch; day-to-day work merges here. |
| `feature/*` | One section, page, or contribution. Branch from `develop`. |
| `release/*` | Stabilise a batch of sections before publishing. |
| `hotfix/*` | Fix on top of `main` (broken build, wrong result, data permission problem). |

Naming: `feature/ch03-logistic-regression`, `feature/contrib-<author-slug>`,
`release/v0.2.0`, `hotfix/broken-freeze`.

Never commit directly to `main`. Commit and push only when asked.

## Publishing to GitHub Pages

Target: GitHub Action that renders on push to `main` and deploys to Pages.

```yaml
# .github/workflows/publish.yml — sketch
on:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    permissions: { contents: read, pages: write, id-token: write }
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - uses: quarto-dev/quarto-actions/render@v2
      - uses: actions/upload-pages-artifact@v3
        with: { path: _site }
      - uses: actions/deploy-pages@v4
```

This works without an R setup step *because* `_freeze/` is committed. If that ever
stops being true, add `r-lib/actions/setup-r` and `setup-renv` and expect slow builds.

Simpler interim route, run locally: `quarto publish gh-pages`.

**Two things to settle before the first publish:**

1. The repo is private. GitHub Pages from a private repo needs a paid plan
   (Pro / Team / Enterprise); on a free org the repo must be made public. Decide
   which before wiring the Action.
2. Making the repo public publishes everything in its history — check no embargoed
   participant data was ever committed (see `.claude/contributed-pages.md`).

`_quarto.yml` needs `site-url: https://hi-digital-ml-ai.github.io/ml-basic/` for
correct absolute links, and a `.nojekyll` file at the site root.

## Before pushing

```bash
quarto render          # must complete with no errors
```

Check: no broken internal links, every new page appears in the sidebar and its
listing, every figure has a caption and alt text.
