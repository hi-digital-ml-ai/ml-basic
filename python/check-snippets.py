#!/usr/bin/env python3
"""Run every Python snippet in the site, to stop the untested tabs from rotting.

The site's tables and figures come from R. Pages converted to ```{python} chunks
run their Python tabs in the render; the rest only display them. This script runs
all of them outside the render, which is quicker than a site build: it pulls the ```python blocks out of each page,
in order, joins them into one program (the snippets on a page are cumulative,
exactly as the R chunks beside them are) and runs it.

    python/check-snippets.py                     # every page
    python/check-snippets.py chapters/07-*/*.qmd  # just these

Needs scikit-learn and pandas; see python/requirements.txt. Exits non-zero on the
first page that fails, and prints the traceback with the page it came from.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Plain ```python blocks (displayed only) and ```{python} chunks (run by knitr
# through reticulate); their #| option lines are Python comments, so harmless.
BLOCK = re.compile(r'^```\{?python[^\n]*\n(.*?)^```', re.S | re.M)


def snippets(page):
    return BLOCK.findall(page.read_text())


def check(page):
    blocks = snippets(page)
    if not blocks:
        return None
    program = "\n".join(blocks)
    result = subprocess.run(
        [sys.executable, "-c", program],
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "python"), "PATH": "/usr/bin:/bin",
             "MPLBACKEND": "Agg"},
        capture_output=True,
        text=True,
    )
    return result


def main(argv):
    pages = ([Path(a) for a in argv] if argv
             else sorted(page
                         for folder in ("toolkit", "chapters")
                         for page in (ROOT / folder).rglob("*.qmd")))
    checked = failed = 0
    for page in pages:
        result = check(page)
        if result is None:
            continue
        checked += 1
        rel = page.relative_to(ROOT) if page.is_absolute() else page
        if result.returncode == 0:
            print(f"ok    {rel}  ({len(snippets(page))} snippets)")
            if result.stderr.strip():
                # Not a failure, but a convergence or deprecation warning here
                # means the snippet is teaching something slightly wrong.
                print(f"      warnings:\n{result.stderr.rstrip()}", file=sys.stderr)
        else:
            failed += 1
            print(f"FAIL  {rel}\n{result.stderr}", file=sys.stderr)
    print(f"\n{checked} page(s) checked, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
