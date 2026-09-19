#!/usr/bin/env python3
"""Pull the R and Python code out of every page into runnable scripts, and zip them.

The pages are the source of truth. This script is the only thing that writes the
downloadable code, so a script cannot drift from the page it came from: the R it
emits is literally the program Quarto ran to produce that page's tables and
figures, and the Python is what python/check-snippets.py already executes.

    tools/extract-code.py                 # write into downloads/ (what the build does)
    tools/extract-code.py --out /tmp/x    # write somewhere else, to inspect it

It runs as a pre-render step, so the files exist before the pages that link to
them are rendered and Quarto can resolve the links. downloads/ is git-ignored and
copied into the site by the `resources:` key in _quarto.yml.

It produces, under the output directory:

    code/<section>/<page>.R     every {r} chunk of that page, in order
    code/<section>/<page>.py    every ```python block of that page, in order
    ml-basic-code.zip           the above plus R/, python/, data/ and a README

Run from the repo root, or anywhere: paths are resolved from this file.
"""

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = "ml-basic-code"
SITE_URL = "https://hi-digital-ml-ai.github.io/ml-basic"
BUNDLE_URL = f"{SITE_URL}/downloads/{BUNDLE}.zip"

# Pages live in these folders. index.qmd is a listing, not a lesson, and files
# starting with _ are Quarto partials.
PAGE_DIRS = ["chapters", "toolkit", "contributed"]

FENCE = re.compile(r"^(`{3,})(.*)$")
R_INFO = re.compile(r"^\{r[\s,}]")
PY_INFO = re.compile(r"^python\s*$")
OPTION = re.compile(r"^#\|\s*(\S+):\s*(.*)$")
TITLE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.M)


def blocks(text):
    """Yield (language, label, body) for every top-level fenced block.

    Fences are tracked with a depth rule rather than by matching ``` naively,
    because the authoring guide quotes markdown inside longer ```` fences and
    those inner blocks are examples, not code to extract.
    """
    open_fence = None
    kind = None
    body = []
    label = None

    for line in text.split("\n"):
        m = FENCE.match(line)
        if open_fence is None:
            if m:
                open_fence = len(m.group(1))
                info = m.group(2).strip()
                kind = "r" if R_INFO.match(info) else "py" if PY_INFO.match(info) else None
                body, label = [], None
            continue

        # Inside a fence: only a bare run of at least as many backticks closes it.
        if m and len(m.group(1)) >= open_fence and not m.group(2).strip():
            if kind:
                yield kind, label, "\n".join(body).strip("\n")
            open_fence, kind = None, None
            continue

        if kind == "r":
            opt = OPTION.match(line)
            if opt:
                if opt.group(1) == "label":
                    label = opt.group(2).strip()
                continue          # every other #| is a Quarto directive, not R
        if kind:
            body.append(line)


def heading(label, width=74):
    """An RStudio/VS Code fold marker, so the script has the page's structure."""
    if not label:
        return ""
    return f"# {label} " + "-" * max(3, width - len(label) - 3)


def page_title(text, fallback):
    m = TITLE.search(text.split("---")[1]) if text.startswith("---") else None
    return m.group(1) if m else fallback


def header(title, rel, comment="#"):
    page_url = f"{SITE_URL}/{rel.with_suffix('.html').as_posix()}"
    lines = [
        title,
        "",
        f"From:   {page_url}",
        f"Source: {rel.as_posix()}",
        "",
        "Part of the ml-basic code bundle, which carries the data and the shared",
        "helpers this needs. If you took this file on its own, get the bundle:",
        f"  {BUNDLE_URL}",
        "",
        "Extracted from the page by tools/extract-code.py. Edit the page, not this.",
    ]
    return "\n".join(f"{comment} {l}".rstrip() for l in lines)


def r_script(title, rel, chunks):
    parts = [header(title, rel), ""]
    parts.append("# here::here() finds the bundle root from the .here file beside R/,")
    parts.append("# so this runs from any working directory inside the bundle.")
    parts.append("")
    for label, body in chunks:
        head = heading(label)
        if head:
            parts += [head, ""]
        parts += [body, ""]
    return "\n".join(parts).rstrip() + "\n"


def py_script(title, rel, chunks):
    parts = [header(title, rel), ""]
    parts += [
        "# Bundle path setup, not part of the page: put the bundle's python/ folder",
        "# on the import path so `from mlbasic_data import ...` resolves.",
        "import sys",
        "from pathlib import Path",
        'sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python"))',
        "",
    ]
    for label, body in chunks:
        head = heading(label)
        if head:
            parts += [head, ""]
        parts += [body, ""]
    return "\n".join(parts).rstrip() + "\n"


# Two things would silently lose code from a download, so say so loudly instead.
# A {python} chunk would execute and is not what python/check-snippets.py reads;
# a code fence inside an included snippet is invisible to the page-by-page scan.
EXEC_PY = re.compile(r"^`{3,}\{python[\s,}]", re.M)
INCLUDE = re.compile(r"\{\{<\s*include\s+(\S+?)\s*>\}\}")


def warn_unhandled(text, rel):
    if EXEC_PY.search(text):
        print(f"extract-code: {rel}: {{python}} chunk is not extracted; the Python "
              f"tabs are plain ```python blocks", file=sys.stderr)
    for inc in INCLUDE.findall(text):
        target = (ROOT / rel).parent / inc
        if target.exists() and re.search(r"^`{3,}[{a-zA-Z]", target.read_text(), re.M):
            print(f"extract-code: {rel}: included {inc} holds code, which the "
                  f"download will not carry", file=sys.stderr)


def pages():
    for d in PAGE_DIRS:
        for p in sorted((ROOT / d).rglob("*.qmd")):
            if p.name == "index.qmd" or p.name.startswith("_"):
                continue
            yield p


def target(rel):
    """chapters/07-validation/x.qmd -> code/07-validation/x; toolkit/x.qmd -> code/toolkit/x.

    Every page lands exactly two levels under code/, which is what lets the
    Python header find the bundle root with parents[2].
    """
    parts = list(rel.parts)
    if parts[0] == "chapters":
        parts = parts[1:]
    return Path("code", *parts).with_suffix("")


def extract(out):
    written = {}
    for page in pages():
        rel = page.relative_to(ROOT)
        text = page.read_text()
        warn_unhandled(text, rel)
        r, py = [], []
        for kind, label, body in blocks(text):
            (r if kind == "r" else py).append((label, body))
        if not r and not py:
            continue

        title = page_title(text, rel.stem)
        stem = target(rel)
        entry = {}
        for suffix, chunks, render in ((".R", r, r_script), (".py", py, py_script)):
            if not chunks:
                continue
            dest = out / stem.with_suffix(suffix)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(render(title, rel, chunks))
            entry[suffix.lstrip(".")] = stem.with_suffix(suffix).as_posix()
        written[rel.as_posix()] = entry
    return written


def readme(written):
    n_r = sum(1 for e in written.values() if "R" in e)
    n_py = sum(1 for e in written.values() if "py" in e)
    return f"""# ml-basic: the course code

Every code block from <{SITE_URL}>, pulled out of the pages into scripts you can
run. {n_r} R scripts and {n_py} Python scripts, one of each per page that has code.

```
code/<section>/<page>.R    the R from that page, in the order it appears
code/<section>/<page>.py   the scikit-learn translation from the same page
R/                         theme.R, data.R and the data-generating scripts
python/                    mlbasic_data.py and requirements.txt
data/                      the example datasets the scripts read
```

## Running the R

Open `{BUNDLE}.Rproj`, or set your working directory anywhere inside this folder,
then:

```r
install.packages(c("tidymodels", "tidyverse", "here", "ranger"))
source("code/07-validation/cross-validation.R")
```

`here::here()` finds this folder from the `.here` file, so the scripts load
`R/data.R` and the CSVs in `data/` wherever you run them from. A few pages need a
package beyond the four above; the `library()` calls at the top of each script say
which.

## Running the Python

```sh
pip install -r python/requirements.txt
python code/07-validation/cross-validation.py
```

Each script puts `python/` on its own import path, so it runs from any directory.

## Two things to know

**The data is simulated.** The coastal survey is generated by
`R/make-example-data.R`, not measured. That is deliberate: the true relationships
are known, so you can check whether a model recovers them. It is not a result
about any real species, and it must not be presented as one.

**R and Python will not print identical numbers.** The two languages draw random
splits from different generators, so a split is not the same split. The
conclusions match; the digits do not.

## Keeping it current

These scripts are generated from the pages by `tools/extract-code.py` on every
build, so they cannot drift from the site. Do not edit them expecting the change
to stick: edit the page.
"""


def bundle(out, written):
    """Zip the scripts together with everything they need to run."""
    staged = {
        "README.md": readme(written),
        ".here": "",                       # here::here() anchors on this
        f"{BUNDLE}.Rproj": "Version: 1.0\n\nRestoreWorkspace: No\nSaveWorkspace: No\n"
                           "AlwaysSaveHistory: No\nEnableCodeIndexing: Yes\n"
                           "UseSpacesForTab: Yes\nNumSpacesForTab: 2\nEncoding: UTF-8\n",
    }
    copied = ["R", "data", "python"]
    skip = {"__pycache__", "check-snippets.py"}

    zip_path = out / f"{BUNDLE}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, body in staged.items():
            z.writestr(f"{BUNDLE}/{name}", body)
        for f in sorted((out / "code").rglob("*")):
            if f.is_file():
                z.write(f, f"{BUNDLE}/{f.relative_to(out).as_posix()}")
        for d in copied:
            for f in sorted((ROOT / d).rglob("*")):
                if f.is_file() and not (set(f.parts) & skip):
                    z.write(f, f"{BUNDLE}/{f.relative_to(ROOT).as_posix()}")
    return zip_path


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(ROOT / "downloads"),
                    help="directory to write code/ and the zip into")
    args = ap.parse_args(argv)

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if (out / "code").exists():
        shutil.rmtree(out / "code")

    written = extract(out)
    if not written:
        print("extract-code: no pages with code found", file=sys.stderr)
        return 1
    zip_path = bundle(out, written)

    n_r = sum(1 for e in written.values() if "R" in e)
    n_py = sum(1 for e in written.values() if "py" in e)
    print(f"extract-code: {n_r} R and {n_py} Python scripts from {len(written)} pages, "
          f"{zip_path.name} {zip_path.stat().st_size // 1024} kB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
