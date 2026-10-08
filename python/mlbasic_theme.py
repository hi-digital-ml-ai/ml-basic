"""Shared plotting style for Python pages, the counterpart of R/theme.R.

Pages load it with:

    from mlbasic_theme import ML_PALETTE, apply_ml_style
    apply_ml_style()

The two halves of the site should look like one site, so the palette, the grid
and the type sizes here are the same values R/theme.R sets for ggplot2. Keep the
two in step: a change to one is a change to both.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

# Okabe-Ito: distinguishable for the common forms of colour blindness and in
# greyscale. Used for categorical colours site-wide, in the same order as R.
ML_PALETTE = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "vermilion": "#D55E00",
    "purple": "#CC79A7",
    "sky": "#56B4E9",
    "yellow": "#F0E442",
    "grey": "#5A5A5A",
}

# Continuous scales are viridis, again matching the R side.
ML_CONTINUOUS = "viridis"

_GRID = "#e6eaed"
_AXIS_TEXT = "#3d4852"
_SUBDUED = "#55606a"


def apply_ml_style(base_size=13):
    """Set the site style on the global matplotlib rcParams.

    base_size is the body font size in points; everything else is scaled from it,
    so a figure stays readable when a listing card shrinks it.
    """
    mpl.rcParams.update({
        "figure.figsize": (7, 4.5),
        "figure.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": base_size,
        "axes.titlesize": base_size * 1.05,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelsize": base_size * 0.95,
        "axes.labelcolor": _AXIS_TEXT,
        "axes.edgecolor": _GRID,
        "axes.facecolor": "white",
        "axes.grid": True,
        "axes.grid.which": "major",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": cycler(color=list(ML_PALETTE.values())),
        "grid.color": _GRID,
        "grid.linewidth": 0.4,
        "xtick.color": _SUBDUED,
        "ytick.color": _SUBDUED,
        "xtick.labelsize": base_size * 0.85,
        "ytick.labelsize": base_size * 0.85,
        "legend.frameon": False,
        "legend.fontsize": base_size * 0.9,
        "image.cmap": ML_CONTINUOUS,
    })


def palette(n=None):
    """The categorical colours as a list, optionally the first n of them."""
    colours = list(ML_PALETTE.values())
    return colours if n is None else colours[:n]


# Applied on import, so that `import mlbasic_theme` is enough, exactly as
# source(here::here("R/theme.R")) is enough on the R side.
apply_ml_style()
