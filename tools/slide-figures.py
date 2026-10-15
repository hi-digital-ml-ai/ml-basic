#!/usr/bin/env python3
"""Copy the course pages' plots that the slide decks show into slides/figures/.

A deck shows a page's plot as figures/<section>/<page>/<label>.png. The plot
itself is the one the page's R code drew, kept in the committed render cache at
_freeze/chapters/<section>/<page>/figure-html/<label>.png, so a deck always shows
the same plot as its page and the copies are never edited or committed.

It runs as a pre-render step, before the decks, and needs only the standard
library, so it also runs on the GitHub runner. A reference to a plot that is not
in the cache stops the build.

Run from the repo root, or anywhere: paths are resolved from this file.
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECKS = ROOT / "slides"
OUT = DECKS / "figures"
REF = re.compile(r"figures/([\w-]+)/([\w-]+)/([\w-]+\.png)")


def main():
    wanted = set()
    for deck in sorted(DECKS.glob("*.qmd")):
        wanted.update(REF.findall(deck.read_text(encoding="utf-8")))

    missing = []
    for section, page, name in sorted(wanted):
        src = ROOT / "_freeze" / "chapters" / section / page / "figure-html" / name
        dst = OUT / section / page / name
        if not src.exists():
            missing.append(f"{section}/{page}/{name}")
            continue
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    if missing:
        sys.exit("slide-figures: no plot in _freeze/ for " + ", ".join(missing))
    print(f"slide-figures: {len(wanted)} plots for the slide decks")


if __name__ == "__main__":
    main()
