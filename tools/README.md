# tools/

Build-time scripts. None is part of the course; they run when the site is built.

| File | What it does |
| --- | --- |
| `extract-code.py` | Pulls the R and Python out of every page into runnable scripts, and zips them with the data |
| `code-downloads.lua` | Puts the "Code from this page" line at the top of every page that has code |
| `slide-figures.py` | Copies the pages' plots that the slide decks show out of `_freeze/` into `slides/figures/` |

## The pages are the source of truth

The code readers download is *generated from the pages*, never maintained beside
them. That is the whole point of the arrangement: the R in
`code/07-validation/cross-validation.R` is literally the program Quarto ran to
produce that page's tables and figures, so it cannot show something the page does
not. The Python is byte-identical to what `python/check-snippets.py` already
executes, so it is known to run.

Do not edit a generated script. Edit the page.

## How it hangs together

`_quarto.yml` runs `extract-code.py` as a `pre-render` step, and lists `downloads/`
under `resources:` so Quarto copies the result into the site. Pre-render rather than
post-render because the pages link to these files: if they do not exist yet, Quarto
warns `Unable to resolve link target` once per page. It writes, into `downloads/`:

```
code/<section>/<page>.R     every {r} chunk of the page, in order, hidden ones included
code/<section>/<page>.py    every ```python block of the page, in order
ml-basic-code.zip           the above plus R/, python/, data/, a README and an .Rproj
```

`downloads/` is git-ignored. Nothing in it is authored, and nothing in it is
committed.

Every page lands exactly two levels under `code/`, which is what lets each Python
script find the bundle root with `parents[2]` and put `python/` on its import path.
The R scripts rely on `here::here()` instead, anchored by the `.here` file the zip
carries at its root, so they run from any working directory inside the bundle.

`code-downloads.lua` adds the download line. It decides what to link from the
document itself, an R link when the page has an R chunk and a Python link when it
has a Python block, so a page that gains or loses a language needs no edit. The
links are ordinary pandoc links, so Quarto resolves them: a download link that ever
breaks becomes a build warning instead of a reader's 404.

It skips `index.qmd` and `_`-prefixed files, which must stay in step with what
`extract-code.py` skips, or a page would link to a script that was never written.
One asymmetry is deliberate: the filter reads the rendered document, so a page
whose only R chunk is the hidden `setup` chunk shows no R link, even though the
extractor still writes the file. There is nothing on such a page worth downloading
as R.

## Running it by hand

```sh
tools/extract-code.py                     # refresh downloads/ without a build
tools/extract-code.py --out /tmp/check    # write somewhere else and look at it
```
