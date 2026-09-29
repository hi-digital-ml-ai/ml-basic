"""Manim scenes for the marine data video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/02-marine-data
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

Scenes marked "page results" read visuals/data/*.csv, which tools/figures-for-video.R
writes from the pages. The others are schematic: made-up shapes, never numbers that
could pass for survey results. The opening, key-point, recap, quiz and end-card scenes
are shared (mlbasic_video.py) and read PROMISES, ANSWERS and RECAP from here.
Consecutive scenes about one picture share a builder, so each starts where the
previous one ended.
"""

import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["How many observations you really have",
            "What to look for before you model",
            "How a test score gets inflated, silently"]
ANSWERS = ["Fewer than the rows:\nrepeat visits are\nnot independent",
           "A list of decisions,\nand none of them\na default",
           "Keep the test set\nuntouched by every\ndecision, not just the fit"]
RECAP = ["The row count is not the sample size",
         "Look before you model: every fix is a decision",
         "Keep the test set untouched by every decision"]

# Stated in the pages' prose rather than computed: the shelf the stations were meant to
# stay on (exploratory-analysis.qmd), and the depth errors that landed inside the
# normal range (the same page, and missing-values-and-outliers.qmd).
SHELF_DEPTH = 200
HIDDEN_DEPTH_ERRORS = 2

SUBSTRATE_COLOURS = {"sand": ORANGE, "mud": VERMILION, "gravel": GREY, "rock": PURPLE}


class Scene01(LearnScene):
    number = 1


# Helpers ----------------------------------------------------------------------------------

def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name, size=24):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
    axes = plain_axes(x_range, y_range, x_length, y_length)
    tx = VGroup(*[label(f"{v:g}", size, SUBDUED).next_to(axes.c2p(v, y_range[0]), DOWN, 0.15)
                  for v in x_ticks])
    ty = VGroup(*[label(f"{v:g}", size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15)
                  for v in y_ticks])
    xn = label(x_name, 26, SUBDUED).next_to(tx if len(tx) else axes, DOWN, 0.2) if x_name else VGroup()
    yn = label(y_name, 26, SUBDUED).rotate(PI / 2).next_to(ty if len(ty) else axes, LEFT, 0.2) \
        if y_name else VGroup()
    return axes, VGroup(axes, tx, ty, xn, yn)


def strike(mobject, colour=VERMILION):
    return Line(mobject.get_left() + 0.1 * LEFT, mobject.get_right() + 0.1 * RIGHT, color=colour,
                stroke_width=6)


def card(text, colour=PURPLE, size=40):
    words = label(text, size, colour, weight=BOLD)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def cross(size=0.4, colour=VERMILION):
    return VGroup(Line(size * UL, size * DR, color=colour, stroke_width=8),
                  Line(size * UR, size * DL, color=colour, stroke_width=8)).scale(0.5)


def at(scene, fraction):
    """Wait until this fraction of the narration."""
    scene.wait(max(scene.share(fraction) - scene.time, 0.01))


def whole_percent(value):
    """A proportion as the pages speak it: 0.785 is 79%, rounded half up as R's round() would not."""
    return f"{Decimal(str(100 * value)).quantize(Decimal('1'), ROUND_HALF_UP)}%"


def band(mobject, colour, width=None, opacity=0.15):
    b = SurroundingRectangle(mobject, color=colour, buff=0.12, corner_radius=0.1, stroke_width=0,
                             fill_color=colour, fill_opacity=opacity)
    if width:
        b.stretch_to_fit_width(width)
    return b


def vbar(axes, x, value, colour, width=0.9):
    bottom, top = axes.c2p(x, 0), axes.c2p(x, value)
    return Rectangle(width=width, height=max(top[1] - bottom[1], 0.001), stroke_width=0, fill_color=colour,
                     fill_opacity=1).move_to(bottom, aligned_edge=DOWN)


def hbar(axes, y, value, colour, height=0.5):
    left, right = axes.c2p(0, y), axes.c2p(value, y)
    return Rectangle(width=max(right[0] - left[0], 0.001), height=height, stroke_width=0, fill_color=colour,
                     fill_opacity=1).move_to(left, aligned_edge=LEFT)


def rsq(scene, model):
    return scene.data("leakage").set_index("model").loc[model, "rsq"]


# The puzzle (scenes 2–4) ------------------------------------------------------------------

def scores_layout(scene):
    """Two forests' R squared, as two cards: the catch-weight forest and the grouped one."""
    heading = title("Two random forests, one survey", 46).to_edge(UP, buff=0.5)
    cards = VGroup()
    for name, model, colour in [("forest A", "catch weight", BLUE), ("forest B", "grouped", BLUE)]:
        box = RoundedRectangle(width=4.6, height=3.4, corner_radius=0.25, stroke_color=colour, stroke_width=5)
        who = label(name, 34, SUBDUED, weight=BOLD).next_to(box.get_top(), DOWN, 0.35)
        what = label("R squared", 30, SUBDUED).next_to(who, DOWN, 0.25)
        value = label(f"{rsq(scene, model):.2f}", 110, colour, weight=BOLD).next_to(what, DOWN, 0.2)
        cards.add(VGroup(box, who, what, value))
    cards.arrange(RIGHT, buff=1.6).move_to([0, -0.2, 0])
    note = label("of the variation in abundance, explained on held-back stations", 28, SUBDUED
                 ).next_to(cards, DOWN, 0.45)
    return heading, cards, note


class Scene02(VideoScene):
    number = 2

    def construct(self):
        heading, cards, note = scores_layout(self)
        # "Here are two random forests, fitted to the same coastal survey."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(cards[0][0]), FadeIn(cards[1][0]),
                  FadeIn(cards[0][1]), FadeIn(cards[1][1]), run_time=self.share(0.2))
        # "One has an R squared of 0.87: it explains most of the variation in abundance."
        at(self, 0.3)
        self.play(FadeIn(cards[0][2]), FadeIn(cards[0][3], scale=0.8), FadeIn(note), run_time=self.share(0.15))
        # "The other, 0.13."
        at(self, 0.82)
        self.play(FadeIn(cards[1][2]), FadeIn(cards[1][3], scale=0.8), run_time=self.share(0.12))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        heading, cards, note = scores_layout(self)
        self.add(heading, cards, note)
        same = label("same data, same kind of model", 34, SUBDUED, weight=BOLD).next_to(heading, DOWN, 0.3)
        ask = card("Which would you trust?", PURPLE, 48).move_to([0, -3.1, 0])
        marks = VGroup(*[label("?", 90, PURPLE, weight=BOLD).next_to(c, UP, -0.2).shift(1.9 * RIGHT + 0.1 * DOWN)
                         for c in cards])
        # "Same data, same kind of model."
        self.play(FadeIn(same), run_time=self.share(0.15))
        # "Which one would you trust?"
        at(self, 0.3)
        self.play(FadeOut(note), FadeIn(ask, shift=0.2 * UP), FadeIn(marks, scale=0.6), run_time=self.share(0.15))
        # "By the end of this video, you will choose the lower one, and know why."
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        columns = self.data("columns")
        heading = title("As it came off the ship", 46).to_edge(UP, buff=0.5)
        chips = VGroup(*[VGroup(RoundedRectangle(width=3.05, height=0.62, corner_radius=0.1, stroke_color=GRID,
                                                 stroke_width=2, fill_color=BLUE, fill_opacity=0.08),
                                label(c, 24, INK)) for c in columns["column"]])
        for chip in chips:
            chip[1].move_to(chip[0])
        chips.arrange_in_grid(rows=5, cols=4, buff=(0.2, 0.18)).move_to([0, -0.2, 0])
        n_rows, n_cols = columns["rows"].iloc[0], len(columns)
        size = label(f"{n_rows} rows, {n_cols} columns", 40, BLUE, weight=BOLD).to_edge(DOWN, buff=0.6)
        # "It starts with the survey as it came off the ship:"
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "one file, 815 rows and 17 columns."
        self.play(LaggedStart(*[FadeIn(c, shift=0.1 * DOWN) for c in chips], lag_ratio=0.08),
                  run_time=self.share(0.45))
        self.play(FadeIn(size, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


# Counting the observations (scenes 5–11) ------------------------------------------------------

def counts_layout(scene):
    """The page's four answers to "how many observations?", as horizontal bars."""
    counts = scene.data("row-counts")
    axes = plain_axes([0, 900, 100], [0, 4, 1], 7.6, 4.4).move_to([1.4, -0.4, 0])
    rows = []
    for i, r in counts.iterrows():
        y = 3.5 - i
        colour = VERMILION if r["what"] == "Distinct sites" else BLUE
        bar = hbar(axes, y, r["n"], colour, 0.62)
        name = label(r["what"], 32).next_to(axes.c2p(0, y), LEFT, 0.3)
        value = label(str(r["n"]), 34, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)
        rows.append(VGroup(name, bar, value))
    heading = title("How many observations is this?", 46).to_edge(UP, buff=0.5)
    return heading, axes, rows, counts


def grow_row(row):
    return [FadeIn(row[0]), GrowFromEdge(row[1], LEFT), FadeIn(row[2])]


class Scene05(VideoScene):
    number = 5

    def construct(self):
        heading, axes, rows, _ = counts_layout(self)
        # "So you have 815 observations?"
        self.play(FadeIn(heading, shift=0.2 * DOWN), *grow_row(rows[0]), run_time=self.share(0.5))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        heading, axes, rows, counts = counts_layout(self)
        self.add(heading, rows[0])
        twice = card(f"{counts['n'][0] - counts['n'][1]} rows: the same station entered twice", ORANGE, 30
                     ).to_edge(DOWN, buff=0.4)
        # "Remove the exact duplicates, the same station entered twice,"
        self.play(FadeIn(twice, shift=0.2 * UP), run_time=self.share(0.2))
        # "and you have 800."
        at(self, 0.6)
        self.play(*grow_row(rows[1]), run_time=self.share(0.25))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        heading, axes, rows, _ = counts_layout(self)
        self.add(heading, rows[0], rows[1])
        # "800 distinct stations, too."
        self.play(*grow_row(rows[2]), run_time=self.share(0.25))
        # "But only 160 distinct sites."
        at(self, 0.5)
        self.play(*grow_row(rows[3]), run_time=self.share(0.25))
        self.play(Indicate(rows[3][2], color=VERMILION), run_time=self.share(0.15))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        visits = self.data("site-visits")
        axes, frame = chart([0, 16, 1], [0, 40, 10], 10.4, 4.6, [1, 5, 10, 15], [0, 10, 20, 30],
                            "visits to the site", "number of sites")
        frame.move_to([0.4, -0.5, 0])
        heading = title("The survey returns to fixed sites", 46).to_edge(UP, buff=0.5)
        bars = {}
        for _, r in visits.iterrows():
            bars[r["visits"]] = vbar(axes, r["visits"], r["number_of_sites"], BLUE, 0.55)
        common = VGroup(*[bars[v] for v in (4, 5, 6)])
        most = label("most: four to six visits", 30, GREEN, weight=BOLD).next_to(common, UP, 0.3)
        top = max(visits["visits"])
        once = label(f"one site: {top} visits", 30, VERMILION, weight=BOLD).next_to(bars[top], UP, 0.3
                                                                                      ).shift(0.9 * LEFT)
        # "The survey returns to fixed sites."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.2))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars.values()], lag_ratio=0.1),
                  run_time=self.share(0.2))
        # "Most were visited four to six times;"
        at(self, 0.45)
        self.play(*[b.animate.set_color(GREEN) for b in common], FadeIn(most), run_time=self.share(0.15))
        # "one, fifteen times."
        at(self, 0.75)
        self.play(bars[top].animate.set_color(VERMILION), FadeIn(once), run_time=self.share(0.15))
        self.finish()


def site_patch():
    """Schematic: one monitoring site as a patch of sea, with five stations in it."""
    patch = Ellipse(width=5.4, height=3.4, stroke_color=SKY, stroke_width=4, fill_color=SKY, fill_opacity=0.15)
    spots = [(-1.5, 0.6), (-0.3, 1.0), (1.2, 0.5), (-0.8, -0.7), (0.9, -0.8)]
    dots = VGroup(*[Dot([x, y, 0], 0.16, color=BLUE) for x, y in spots])
    return VGroup(patch, dots)


class Scene09(VideoScene):
    number = 9

    def construct(self):
        site = site_patch().move_to([-2.8, -0.2, 0])
        name = label("one site, five stations", 32, SUBDUED, weight=BOLD).next_to(site, UP, 0.3)
        shared = VGroup(*[label(t, 36, BLUE, weight=BOLD) for t in
                          ["the same water", "the same seabed", "often the same day"]]
                        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([3.6, 0.3, 0])
        verdict = card("closer to one observation with replicates", PURPLE, 34).to_edge(DOWN, buff=0.5)
        # "Stations at one site share the same water, the same seabed, often the same day."
        self.play(FadeIn(site[0]), FadeIn(name), LaggedStart(*[FadeIn(d, scale=0.5) for d in site[1]], lag_ratio=0.2),
                  run_time=self.share(0.15))
        for i, line in enumerate(shared):
            at(self, 0.12 + 0.13 * i)
            self.play(FadeIn(line, shift=0.2 * RIGHT), run_time=self.share(0.08))
        # "They are closer to one observation with replicates than to five observations."
        at(self, 0.58)
        self.play(site[1].animate.arrange(RIGHT, buff=0.08).move_to(site[0]), run_time=self.share(0.15))
        self.play(FadeIn(verdict, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        heading, axes, rows, counts = counts_layout(self)
        self.add(heading, *rows)
        effective = card(f"effective sample size:\nnearer {counts['n'].iloc[-1]} than {counts['n'].iloc[0]}",
                         VERMILION, 30).next_to(rows[3][2], RIGHT, 0.4)
        # "So your effective sample size is nearer 160 than 815."
        self.play(FadeIn(effective, shift=0.2 * UP), Indicate(rows[3][1], color=VERMILION, scale_factor=1.03),
                  run_time=self.share(0.25))
        # "Every score computed as though it were 815 will be optimistic."
        at(self, 0.55)
        tag = label(f"scores computed on {counts['n'].iloc[0]} rows are optimistic", 30, VERMILION, weight=BOLD
                    ).to_edge(DOWN, buff=0.45)
        self.play(rows[0][1].animate.set_color(ORANGE), FadeIn(tag), run_time=self.share(0.15))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        # Schematic: six sites, three to five rows each. First split at random, then by site.
        rng = np.random.default_rng(11)
        colours = [BLUE, ORANGE, GREEN, PURPLE, SKY, VERMILION]
        sizes = [4, 5, 3, 5, 4, 3]
        rows = VGroup(*[Square(0.42, stroke_width=0, fill_color=c, fill_opacity=1)
                        for c, n in zip(colours, sizes) for _ in range(n)])
        site_of = [s for s, n in enumerate(sizes) for _ in range(n)]
        train_box = RoundedRectangle(width=7.2, height=3.4, corner_radius=0.2, stroke_color=INK, stroke_width=3
                                     ).move_to([-2.4, -0.6, 0])
        test_box = RoundedRectangle(width=3.8, height=3.4, corner_radius=0.2, stroke_color=INK, stroke_width=3
                                    ).move_to([4.2, -0.6, 0])
        names = VGroup(label("training", 32, INK, weight=BOLD).next_to(train_box, UP, 0.2),
                       label("test", 32, INK, weight=BOLD).next_to(test_box, UP, 0.2))
        heading = label("every row kept", 36, GREEN, weight=BOLD).to_edge(UP, buff=0.5)

        def fill(indices, box, cols):
            group = VGroup(*[rows[i] for i in indices])
            targets = [box.get_corner(UL) + np.array([0.55 + 0.55 * (k % cols), -0.55 - 0.55 * (k // cols), 0])
                       for k in range(len(indices))]
            return [rows[i].animate.move_to(t) for i, t in zip(indices, targets)], group

        rows.arrange_in_grid(rows=3, buff=0.13).move_to([0, 2.2, 0])
        order = rng.permutation(len(rows))
        random_test = sorted(order[:6])
        random_train = sorted(order[6:])
        by_site_test = [i for i, s in enumerate(site_of) if s in (1, 4)]
        by_site_train = [i for i, s in enumerate(site_of) if s not in (1, 4)]

        # "The fix is not to delete rows."
        self.play(FadeIn(heading), FadeIn(rows), run_time=self.share(0.15))
        self.play(FadeIn(train_box), FadeIn(test_box), FadeIn(names), run_time=self.share(0.1))
        moves_a, _ = fill(random_train, train_box, 12)
        moves_b, _ = fill(random_test, test_box, 6)
        self.play(*moves_a, *moves_b, run_time=self.share(0.15))
        split_site = cross(0.9).move_to(test_box.get_corner(DR) + np.array([-0.5, 0.5, 0]))
        self.play(FadeIn(split_site), run_time=self.share(0.05))
        # "It is to keep each site's rows together when you split the data."
        at(self, 0.5)
        moves_a, _ = fill(by_site_train, train_box, 12)
        moves_b, _ = fill(by_site_test, test_box, 6)
        box, mark = tick(0.7)
        box.move_to(split_site)
        mark.move_to(box)
        self.play(*moves_a, *moves_b, FadeOut(split_site), run_time=self.share(0.25))
        together = label("each site on one side", 32, GREEN, weight=BOLD).next_to(train_box, DOWN, 0.3
                                                                                  ).set_x(0)
        self.play(FadeIn(box), Create(mark), FadeIn(together), run_time=self.share(0.1))
        self.finish()


class Scene12(KeyPointScene):
    number, point = 12, 1


# Looking before modelling (scenes 13–25) ---------------------------------------------------

def ranges_layout(scene):
    """The page's range table: minimum, mean and maximum of every numeric column, raw file."""
    table = scene.data("ranges")
    xs = [-4.0, 0.6, 3.1, 5.6]
    head = VGroup(*[label(t, 28, SUBDUED, weight=BOLD).move_to([x, 2.5, 0])
                    for t, x in zip(["", "min", "mean", "max"], xs)])
    rows = {}
    for i, r in table.iterrows():
        y = 1.9 - 0.52 * i
        rows[r["variable"]] = VGroup(
            label(r["variable"], 30).move_to([xs[0] + 2.6, y, 0], aligned_edge=RIGHT),
            *[label(f"{r[k]:.2f}", 30).move_to([x, y, 0]) for k, x in zip(["min", "mean", "max"], xs[1:])])
    rule = Line([-6.6, 2.2, 0], [6.6, 2.2, 0], stroke_width=3)
    heading = title("Every numeric column, smallest to largest", 44).to_edge(UP, buff=0.35)
    return VGroup(heading, head, rule), rows, table


class Scene13(VideoScene):
    number = 13

    def construct(self):
        frame, rows, _ = ranges_layout(self)
        # "Now look before you model. Print the smallest and largest value of every numeric column,"
        self.play(FadeIn(frame), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(r, shift=0.1 * DOWN) for r in rows.values()], lag_ratio=0.12),
                  run_time=self.share(0.4))
        # "and read them as a scientist."
        self.finish()


def ranges_salinity(frame, rows, table):
    row = rows["salinity_psu"]
    b = band(row, VERMILION, 13.2).set_x(0)
    r = table.set_index("variable").loc["salinity_psu"]
    return row, b, r


class Scene14(VideoScene):
    number = 14

    def construct(self):
        frame, rows, table = ranges_layout(self)
        self.add(frame, *rows.values())
        row, b, r = ranges_salinity(frame, rows, table)
        verdict = card("no ocean is 2 PSU", VERMILION, 34).to_edge(DOWN, buff=0.25).shift(3.4 * RIGHT)
        # "Salinity has a minimum of minus 999,"
        self.play(FadeIn(b), row[1].animate.set_color(VERMILION), run_time=self.share(0.2))
        # "and a mean of 2.24."
        at(self, 0.4)
        self.play(row[2].animate.set_color(VERMILION), Indicate(row[2], color=VERMILION), run_time=self.share(0.15))
        # "No ocean is 2 PSU."
        at(self, 0.7)
        self.play(FadeIn(verdict, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        values = self.data("salinity")["salinity_psu"]
        clean_mean = self.data("salinity-means")["clean_mean"].iloc[0]
        # The page's histogram: 60 bins over the whole range, so the real ocean is one sliver.
        counts, edges = np.histogram(values, bins=60)
        axes, frame = chart([-1050, 50, 100], [0, 800, 100], 10.4, 4.6, [-1000, -500, 0], [0, 200, 400, 600, 800],
                            "salinity (PSU)", "stations")
        frame.move_to([0.4, -0.5, 0])
        width = axes.c2p(edges[1], 0)[0] - axes.c2p(edges[0], 0)[0]
        bars = VGroup(*[vbar(axes, (lo + hi) / 2, n, BLUE, width * 0.95)
                        for n, lo, hi in zip(counts, edges[:-1], edges[1:]) if n > 0])
        sentinel = bars[0]
        n_sentinel = int((values == -999).sum())
        sentinel_name = label(f"−999 ({n_sentinel} rows)", 30, VERMILION, weight=BOLD).next_to(sentinel, UP, 0.2
                                                                                               ).shift(1.0 * RIGHT)
        ocean = label("the real ocean", 30, BLUE, weight=BOLD).next_to(bars[-1], LEFT, 0.3).shift(0.8 * UP)
        heading = title("A number that is not a measurement", 46).to_edge(UP, buff=0.5)
        fixed = card(f"marked missing: mean {clean_mean:.1f}", GREEN, 34).move_to([-0.6, 1.2, 0])
        # "Minus 999 was written to mean "missing"."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame),
                  LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=self.share(0.25))
        self.play(sentinel.animate.set_color(VERMILION), FadeIn(sentinel_name), FadeIn(ocean), run_time=self.share(0.1))
        # "Because it is a number, nothing complained."
        # "Mark it missing, and the mean salinity is 33.9."
        at(self, 0.62)
        self.play(FadeOut(sentinel), sentinel_name.animate.set_opacity(0.3), run_time=self.share(0.12))
        self.play(FadeIn(fixed, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        frame, rows, table = ranges_layout(self)
        self.add(frame, *rows.values())
        row = rows["depth_m"]
        b = band(row, VERMILION, 13.2).set_x(0)
        shelf = card(f"a shelf survey meant to stay under {SHELF_DEPTH} m", VERMILION, 30
                     ).to_edge(DOWN, buff=0.25).shift(2.0 * RIGHT)
        # "Depth reaches 1581 metres,"
        self.play(FadeIn(b), row[3].animate.set_color(VERMILION), Indicate(row[3], color=VERMILION),
                  run_time=self.share(0.3))
        # "on a shelf survey meant to stay under 200."
        at(self, 0.45)
        self.play(FadeIn(shelf, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def depths_layout(scene, top):
    depths = scene.data("depths")
    step = 400 if top > 400 else 50
    axes, frame = chart([0, top, step], [0, 18, 2], 10.4, 4.8, list(range(0, int(top) + 1, step)), [0, 5, 10, 15],
                        "depth (m)", "temperature (°C)")
    frame.move_to([0.4, -0.6, 0])
    return depths, axes, frame


class Scene17(VideoScene):
    number = 17

    def construct(self):
        depths, wide, wide_frame = depths_layout(self, 1600)
        _, near, near_frame = depths_layout(self, 200)
        ok = depths[~depths["corrected"]]
        bad = depths[depths["corrected"]]
        heading = title(f"{len(bad)} stations, ten times too deep", 46).to_edge(UP, buff=0.5)
        cloud = VGroup(*[Dot(wide.c2p(d, t), 0.045, color=BLUE, fill_opacity=0.6)
                         for d, t in zip(ok["depth_m"], ok["temperature_c"])])
        wrong = VGroup(*[Dot(wide.c2p(d, t), 0.1, color=VERMILION)
                         for d, t in zip(bad["recorded"], bad["temperature_c"])])
        # "Ten stations were recorded ten times too deep."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(wide_frame), FadeIn(cloud), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in wrong], lag_ratio=0.1), run_time=self.share(0.15))
        # "Divide them by ten, and each one lands where its temperature makes sense."
        at(self, 0.35)
        self.play(*[d.animate.move_to(wide.c2p(x, t)) for d, x, t in zip(wrong, bad["depth_m"], bad["temperature_c"])],
                  run_time=self.share(0.15))
        # Zoom to the shelf, so the corrected stations can be seen sitting in the cloud.
        self.play(ReplacementTransform(wide_frame, near_frame),
                  *[d.animate.move_to(near.c2p(x, t)) for d, x, t in zip(cloud, ok["depth_m"], ok["temperature_c"])],
                  *[d.animate.move_to(near.c2p(x, t)) for d, x, t in zip(wrong, bad["depth_m"], bad["temperature_c"])],
                  run_time=self.share(0.2))
        # "That is evidence, not convenience."
        at(self, 0.8)
        self.play(Indicate(wrong, color=VERMILION, scale_factor=1.3), run_time=self.share(0.12))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        depths, near, near_frame = depths_layout(self, 200)
        ok = depths[~depths["corrected"]]
        bad = depths[depths["corrected"]]
        heading = title(f"{len(bad)} stations, ten times too deep", 46).to_edge(UP, buff=0.5)
        cloud = VGroup(*[Dot(near.c2p(d, t), 0.045, color=BLUE, fill_opacity=0.6)
                         for d, t in zip(ok["depth_m"], ok["temperature_c"])])
        fixed = VGroup(*[Dot(near.c2p(d, t), 0.1, color=VERMILION)
                         for d, t in zip(bad["depth_m"], bad["temperature_c"])])
        self.add(heading, near_frame, cloud, fixed)
        hidden = card(f"{HIDDEN_DEPTH_ERRORS} more are in here, and look normal", PURPLE, 32)
        # "Two more were ten times too deep but landed inside the normal range."
        self.play(fixed.animate.set_color(BLUE).set_opacity(0.6).scale(0.5), run_time=self.share(0.15))
        undetectable = label("undetectable", 40, VERMILION, weight=BOLD)
        VGroup(hidden, undetectable).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.35)
        self.play(FadeOut(heading), FadeIn(hidden, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "No amount of looking will find them."
        at(self, 0.62)
        self.play(Wiggle(cloud, scale_value=1.02), FadeIn(undetectable), run_time=self.share(0.25))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        spellings = self.data("substrate-spellings")
        heading = title("Four substrate types, twelve spellings", 46).to_edge(UP, buff=0.4)
        axes = plain_axes([0, 180, 20], [0, 12, 1], 6.4, 6.0).move_to([0.4, -0.6, 0])
        rows = VGroup()
        for i, r in spellings.iterrows():
            y = 11.5 - i
            bar = hbar(axes, y, r["n"], GREY, 0.36)
            name = label(r["substrate"], 28).next_to(axes.c2p(0, y), LEFT, 0.25)
            value = label(str(r["n"]), 24, SUBDUED).next_to(bar, RIGHT, 0.12)
            rows.add(VGroup(name, bar, value))
        kinds = [str(s).strip().lower().replace("sandy", "sand").replace("muddy", "mud").replace("rocky", "rock")
                 for s in spellings["substrate"]]
        key = VGroup(*[VGroup(Square(0.34, stroke_width=0, fill_color=c, fill_opacity=1),
                              label(k, 32, c, weight=BOLD)).arrange(RIGHT, buff=0.2)
                       for k, c in SUBSTRATE_COLOURS.items()]
                     ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.8, 0.2, 0])
        # "Count every level of every category."
        self.play(FadeIn(heading, shift=0.2 * DOWN), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08),
                  run_time=self.share(0.3))
        # "Here, four substrate types have twelve spellings,"
        at(self, 0.35)
        self.play(*[r[1].animate.set_color(SUBSTRATE_COLOURS[k]) for r, k in zip(rows, kinds)], FadeIn(key),
                  run_time=self.share(0.2))
        # "and a model treats each spelling as a different habitat."
        at(self, 0.7)
        twelve = label("to a model:\ntwelve habitats", 30, VERMILION, weight=BOLD).next_to(key, DOWN, 0.5)
        self.play(FadeIn(twelve), run_time=self.share(0.12))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        missing = self.data("chlorophyll-missing").sort_values("missing").reset_index(drop=True)
        heading = title("Missing, but not at random", 46).to_edge(UP, buff=0.5)
        axes, frame = chart([0, 25, 5], [0, 4, 1], 8.0, 4.0, [0, 5, 10, 15, 20], [], "chlorophyll missing (%)", "")
        frame.move_to([0.8, -0.4, 0])
        rows = []
        for i, r in missing.iterrows():
            y = 0.5 + i
            colour = VERMILION if r["season"] == "winter" else ORANGE
            bar = hbar(axes, y, r["missing"], colour, 0.62)
            name = label(r["season"], 32).next_to(axes.c2p(0, y), LEFT, 0.3)
            value = label(whole_percent(r["missing"] / 100), 32, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)
            rows.append(VGroup(name, bar, value))
        by = {r["season"]: rows[i] for i, r in missing.iterrows()}
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), *[FadeIn(r[0]) for r in rows],
                  run_time=self.share(0.12))
        # "Chlorophyll is missing at 19% of winter stations,"
        self.play(GrowFromEdge(by["winter"][1], LEFT), FadeIn(by["winter"][2]), run_time=self.share(0.2))
        # "and 1% in autumn."
        at(self, 0.4)
        self.play(GrowFromEdge(by["autumn"][1], LEFT), FadeIn(by["autumn"][2]), run_time=self.share(0.12))
        # "Missing, but not at random."
        at(self, 0.6)
        rest = [by[s] for s in ("spring", "summer")]
        self.play(*[GrowFromEdge(r[1], LEFT) for r in rest], *[FadeIn(r[2]) for r in rest], run_time=self.share(0.15))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        deletion = self.data("deletion")
        cost = self.data("deletion-cost").iloc[0]
        seasons = ["spring", "summer", "autumn", "winter"]
        heading = title("Dropping every row with a gap", 46).to_edge(UP, buff=0.5)
        axes, frame = chart([0, 4, 1], [0, 250, 50], 9.4, 4.4, [], [0, 100, 200], "", "stations")
        frame.move_to([-1.4, -0.5, 0])
        colours = {"All rows": BLUE, "Complete cases only": ORANGE}
        groups = {}
        for d, colour in colours.items():
            part = VGroup()
            for s, season in enumerate(seasons):
                n = deletion[(deletion["dataset"] == d) & (deletion["season"] == season)]["n"].item()
                x = s + 0.5 + (-0.21 if d == "All rows" else 0.21)
                bar = vbar(axes, x, n, colour, 0.4)
                part.add(VGroup(bar, label(str(n), 24, INK).next_to(bar, UP, 0.1)))
            groups[d] = part
        names = VGroup(*[label(s, 30).next_to(axes.c2p(i + 0.5, 0), DOWN, 0.25) for i, s in enumerate(seasons)])
        key = VGroup(*[VGroup(Square(0.3, stroke_width=0, fill_color=c, fill_opacity=1),
                              label(n.lower(), 28, c, weight=BOLD)).arrange(RIGHT, buff=0.2)
                       for n, c in colours.items()]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4).set_y(1.8)
        lost = card(f"{int(cost['rows_before'] - cost['rows_after'])} rows lost;\nwinter loses {cost['winter_lost_pct']:.1f}%",
                    VERMILION, 30).to_edge(RIGHT, buff=0.4).set_y(-0.6)
        # "Most modelling functions quietly drop any row with a gap."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), FadeIn(names), FadeIn(key),
                  *[GrowFromEdge(g[0], DOWN) for g in groups["All rows"]], *[FadeIn(g[1]) for g in groups["All rows"]],
                  run_time=self.share(0.25))
        self.play(*[GrowFromEdge(g[0], DOWN) for g in groups["Complete cases only"]],
                  *[FadeIn(g[1]) for g in groups["Complete cases only"]], run_time=self.share(0.15))
        # "Here that removes 80 rows, and a fifth of winter."
        at(self, 0.55)
        winter = VGroup(groups["All rows"][3], groups["Complete cases only"][3])
        self.play(FadeIn(band(winter, VERMILION, opacity=0.12)), FadeIn(lost, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        vessels = self.data("vessels")
        heading = title("Split by vessel", 46).to_edge(UP, buff=0.5)
        xs = [-4.2, -1.3, 1.6, 4.9]
        head = VGroup(*[label(t, 28, SUBDUED, weight=BOLD).move_to([x, 1.7, 0]) for t, x in
                        zip(["", "stations", "mean salinity", "mean temperature"], xs)])
        rows = VGroup()
        for i, r in vessels.iterrows():
            y = 0.8 - 1.0 * i
            rows.add(VGroup(label(r["vessel"], 36, INK, weight=BOLD).move_to([xs[0], y, 0]),
                            label(str(r["stations"]), 36).move_to([xs[1], y, 0]),
                            label(f"{r['mean_salinity']:.2f}", 40, VERMILION, weight=BOLD).move_to([xs[2], y, 0]),
                            label(f"{r['mean_temperature']:.2f}", 36).move_to([xs[3], y, 0])))
        rule = Line([-5.6, 1.3, 0], [6.6, 1.3, 0], stroke_width=3)
        salinity = VGroup(head[2], *[r[2] for r in rows])
        verdict = card("an instrument offset, hidden when the fleet is pooled", PURPLE, 32).to_edge(DOWN, buff=0.7)
        # "Now split by vessel. The two ships sampled the same shelf,"
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(head), FadeIn(rule),
                  LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=self.share(0.3))
        # "and one reads higher salinity than the other."
        at(self, 0.38)
        self.play(FadeIn(band(salinity, VERMILION)), run_time=self.share(0.12))
        # "That is an instrument offset, invisible in the pooled data."
        at(self, 0.62)
        self.play(FadeIn(verdict, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        # Schematic: the twelve months, on a line and on a circle.
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        line = NumberLine(x_range=[1, 12, 1], length=5.8, color=GRID, include_ticks=False, stroke_width=3
                          ).move_to([-3.6, 0.2, 0])
        line_dots = VGroup(*[Dot(line.n2p(m), 0.1, color=BLUE) for m in range(1, 13)])
        line_names = VGroup(*[label(months[m - 1], 22, SUBDUED).next_to(line.n2p(m), UP, 0.2)
                              for m in (1, 12)])
        apart = DoubleArrow(line.n2p(1) + 0.5 * DOWN, line.n2p(12) + 0.5 * DOWN, color=VERMILION, buff=0,
                            stroke_width=5, tip_length=0.2)
        apart_name = label("eleven apart", 30, VERMILION, weight=BOLD).next_to(apart, DOWN, 0.2)
        centre = np.array([3.6, -0.7, 0])
        ring = Circle(1.9, color=GRID, stroke_width=3).move_to(centre)
        ring_dots = VGroup(*[Dot(centre + 1.9 * np.array([np.sin(2 * PI * m / 12), np.cos(2 * PI * m / 12), 0]),
                                 0.1, color=BLUE) for m in range(1, 13)])
        ring_names = VGroup(*[label(months[m - 1], 26, INK, weight=BOLD).move_to(
            centre + 2.4 * np.array([np.sin(2 * PI * m / 12), np.cos(2 * PI * m / 12), 0])) for m in (1, 12)])
        close = label("neighbours", 30, GREEN, weight=BOLD).move_to(centre + 0.4 * DOWN)
        titles = VGroup(label("as a number", 34, SUBDUED, weight=BOLD).next_to(line, UP, 1.3),
                        label("as sine and cosine", 34, SUBDUED, weight=BOLD).next_to(ring, UP, 0.8))
        titles[0].set_y(titles[1].get_y())
        heading = title("What does each column mean?", 46).to_edge(UP, buff=0.5)
        # "And ask what each column means."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "As numbers, December and January are eleven months apart."
        at(self, 0.25)
        self.play(FadeIn(titles[0]), FadeIn(line), FadeIn(line_dots), FadeIn(line_names), run_time=self.share(0.12))
        self.play(GrowFromCenter(apart), FadeIn(apart_name), run_time=self.share(0.15))
        # "In the ocean they are neighbours."
        at(self, 0.68)
        self.play(FadeIn(titles[1]), Create(ring), FadeIn(ring_dots), FadeIn(ring_names), FadeIn(close),
                  run_time=self.share(0.2))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        rare = self.data("rare-species").set_index("rare_species")
        present, absent = int(rare.loc["yes", "n"]), int(rare.loc["no", "n"])
        total = present + absent
        heading = title("The rare species", 46).to_edge(UP, buff=0.5)
        cells = VGroup(*[Square(0.17, stroke_width=0, fill_color=GRID, fill_opacity=1) for _ in range(total)])
        cells.arrange_in_grid(cols=33, buff=0.05).move_to([-3.2, -0.5, 0])
        rng = np.random.default_rng(24)   # where the present stations sit in the grid is arbitrary
        yes = rng.choice(total, present, replace=False)
        found = label(f"present at {whole_percent(present / total)} of stations", 34, ORANGE, weight=BOLD
                      ).move_to([3.7, 1.0, 0])
        baseline = card(f"always say \"absent\":\n{whole_percent(absent / total)} accurate", VERMILION, 34
                        ).move_to([3.7, -1.2, 0])
        # "Last, the response. The rare species is present at 5% of stations,"
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(cells), run_time=self.share(0.2))
        at(self, 0.25)
        self.play(*[cells[i].animate.set_fill(ORANGE) for i in yes], FadeIn(found), run_time=self.share(0.2))
        # "so answering "absent" every time is 95% accurate."
        at(self, 0.62)
        self.play(FadeIn(baseline, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene25(VideoScene):
    number = 25

    def construct(self):
        ranges = self.data("ranges").set_index("variable")
        spellings = self.data("substrate-spellings")
        winter = self.data("chlorophyll-missing").set_index("season").loc["winter", "missing"]
        rare = self.data("rare-species").set_index("rare_species")
        share = rare.loc["yes", "n"] / rare["n"].sum()
        kinds = {str(s).strip().lower().replace("sandy", "sand").replace("muddy", "mud").replace("rocky", "rock")
                 for s in spellings["substrate"]}
        findings = [
            ("−999 in salinity and temperature", "mark it missing, then decide"),
            (f"depths up to {ranges.loc['depth_m', 'max']:.0f} m", "correct, drop or flag"),
            (f"{len(spellings)} spellings of {len(kinds)} substrates", "merge, and lose nothing real"),
            (f"chlorophyll missing {whole_percent(winter / 100)} in winter", "dropping rows deletes winter"),
            (f"rare species at {whole_percent(share)}", "accuracy is the wrong measure"),
            ("one vessel reads salinity high", "correct it, model it, or drop it"),
        ]
        heading = title("Six findings, six decisions", 46).to_edge(UP, buff=0.45)
        rows = VGroup()
        for i, (finding, decision) in enumerate(findings):
            y = 2.0 - 0.9 * i
            left = label(finding, 32).move_to([-0.5, y, 0], aligned_edge=RIGHT)
            arrow = Arrow([-0.3, y, 0], [0.6, y, 0], color=SUBDUED, stroke_width=4, buff=0, tip_length=0.18)
            right = label(decision, 32, PURPLE, weight=BOLD).move_to([0.8, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(left, arrow, right))
        rows.set_x(0)
        # "Each finding is a decision, not a repair,"
        self.play(FadeIn(heading, shift=0.2 * DOWN), LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.15),
                  run_time=self.share(0.25))
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(r[1]), FadeIn(r[2])) for r in rows], lag_ratio=0.15),
                  run_time=self.share(0.3))
        # "and each one needs someone who knows how the data were collected."
        self.finish()


class Scene26(KeyPointScene):
    number, point = 26, 2


# Protecting the test set (scenes 27–41) ----------------------------------------------------

class Scene27(VideoScene):
    number = 27

    def construct(self):
        # Schematic: the three roles of held-back data.
        roles = [("training", "fits the model", BLUE), ("validation", "chooses between\nmodels", ORANGE),
                 ("test", "reports once,\nat the end", GREEN)]
        boxes = VGroup()
        for name, job, colour in roles:
            box = RoundedRectangle(width=4.1, height=2.4, corner_radius=0.2, stroke_color=colour, stroke_width=5,
                                   fill_color=colour, fill_opacity=0.08)
            words = VGroup(label(name, 40, colour, weight=BOLD), label(job, 28, INK)).arrange(DOWN, buff=0.3)
            boxes.add(VGroup(box, words.move_to(box)))
        boxes.arrange(RIGHT, buff=0.4).move_to([0, -0.2, 0])
        lock = VGroup(RoundedRectangle(width=0.6, height=0.45, corner_radius=0.06, stroke_width=0, fill_color=GREEN,
                                       fill_opacity=1),
                      Arc(0.2, 0, PI, color=GREEN, stroke_width=6).shift(0.3 * UP)).next_to(boxes[2], UP, 0.25)
        heading = title("Three roles for your data", 46).to_edge(UP, buff=0.5)
        # "Now the held-back data."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "Training data fit the model. Validation data choose between models. The test set reports, once, at the end."
        for box, when in zip(boxes, (0.22, 0.45, 0.68)):
            at(self, when)
            self.play(FadeIn(box, shift=0.2 * UP), run_time=self.share(0.1))
        self.play(FadeIn(lock, shift=0.1 * DOWN), run_time=self.share(0.08))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        shared = self.data("shared-sites").iloc[0]
        heading = title("A random split", 46).to_edge(UP, buff=0.4)
        total = shared["training"] + shared["testing"]
        train = Rectangle(width=11 * shared["training"] / total, height=0.9, stroke_width=0, fill_color=BLUE,
                          fill_opacity=1)
        test = Rectangle(width=11 * shared["testing"] / total, height=0.9, stroke_width=0, fill_color=GREEN,
                         fill_opacity=1)
        strip = VGroup(train, test).arrange(RIGHT, buff=0.1).move_to([0, 2.0, 0])
        names = VGroup(label(f"{shared['training']} training", 32, BACKGROUND, weight=BOLD).move_to(train),
                       label(f"{shared['testing']} test", 32, BACKGROUND, weight=BOLD).move_to(test))
        seen = card(f"all {shared['test_rows_seen']} of {shared['testing']} test stations: at a site already in training",
                    VERMILION, 30).to_edge(DOWN, buff=0.35)
        # The sites: those with stations on both sides, and those only in training.
        both, only = int(shared["sites_in_both"]), int(shared["sites"] - shared["sites_in_both"])
        sites = VGroup(*[Square(0.26, stroke_width=0, fill_color=BLUE, fill_opacity=1) for _ in range(both + only)])
        sites.arrange_in_grid(rows=8, buff=0.07).move_to([-1.6, -0.6, 0])
        key = VGroup(label(f"{both} sites on both sides", 30, PURPLE, weight=BOLD),
                     label(f"{only} only in training", 30, BLUE, weight=BOLD)).arrange(DOWN, buff=0.3, aligned_edge=LEFT
                                                                                       ).next_to(sites, RIGHT, 0.6)
        # "Split this survey at random,"
        self.play(FadeIn(heading, shift=0.2 * DOWN), GrowFromEdge(train, LEFT), GrowFromEdge(test, LEFT),
                  FadeIn(names), run_time=self.share(0.25))
        # "and every one of the 200 test stations sits at a site the model has trained on."
        at(self, 0.35)
        self.play(FadeIn(sites), run_time=self.share(0.1))
        self.play(*[s.animate.set_fill(PURPLE) for s in sites[:both]], FadeIn(key), run_time=self.share(0.15))
        self.play(FadeIn(seen, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene29(VideoScene):
    number = 29

    def construct(self):
        # Schematic: the question each split answers.
        left = VGroup(label("a random split tests", 30, SUBDUED, weight=BOLD),
                      card("another station at a\nsite I have surveyed?", BLUE, 34)).arrange(DOWN, buff=0.35)
        right = VGroup(label("a habitat map is asked", 30, SUBDUED, weight=BOLD),
                       card("a site nobody\nhas surveyed?", GREEN, 34)).arrange(DOWN, buff=0.35)
        VGroup(left, right).arrange(RIGHT, buff=1.6).move_to([0, 0, 0])
        differs = MathTex(r"\neq", color=VERMILION).scale(2.2).move_to((left[1].get_right() + right[1].get_left()) / 2)
        heading = title("Two questions", 46).to_edge(UP, buff=0.5)
        # "So the test asks how well it predicts another station at a surveyed site."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(left, shift=0.2 * RIGHT), run_time=self.share(0.25))
        # "A habitat map is asked about sites nobody has surveyed."
        at(self, 0.55)
        self.play(FadeIn(right, shift=0.2 * LEFT), run_time=self.share(0.15))
        self.play(FadeIn(differs, scale=0.5), run_time=self.share(0.1))
        self.finish()


def stratify_layout(scene):
    table = scene.data("stratify").set_index("split")
    overall = table.loc["all", "train_pct"]
    heading = title("Asking for a stratified split", 46).to_edge(UP, buff=0.4)
    code = label("strata = rare_species", 34, INK)
    code_box = SurroundingRectangle(code, color=GRID, buff=0.25, corner_radius=0.1, fill_color=GRID, fill_opacity=0.3)
    ran = label("ran without complaint", 30, GREEN, weight=BOLD)
    request = VGroup(VGroup(code_box, code), ran).arrange(RIGHT, buff=0.5).move_to([0, 2.2, 0])
    axes, frame = chart([0, 8, 1], [0, 2, 1], 8.0, 2.6, [0, 2, 4, 6, 8], [], "rare species present (%)", "")
    frame.move_to([1.0, -1.0, 0])
    line = DashedLine(axes.c2p(overall, 0), axes.c2p(overall, 2.1), color=INK, stroke_width=4)
    line_name = label(f"all stations: {overall:.1f}%", 28, INK, weight=BOLD).next_to(line, UP, 0.12)
    return table, heading, request, axes, frame, VGroup(line, line_name)


def stratify_bars(axes, train_pct, test_pct):
    bars = VGroup()
    for y, name, value, colour in [(1.5, "training", train_pct, BLUE), (0.5, "test", test_pct, GREEN)]:
        bar = hbar(axes, y, value, colour, 0.62)
        bars.add(VGroup(label(name, 32).next_to(axes.c2p(0, y), LEFT, 0.3), bar,
                        label(f"{value:.1f}%", 32, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)))
    return bars


class Scene30(VideoScene):
    number = 30

    def construct(self):
        table, heading, request, axes, frame, overall = stratify_layout(self)
        asked = stratify_bars(axes, table.loc["stratified", "train_pct"], table.loc["stratified", "test_pct"])
        # "Or ask the split to stratify on the rare species."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(request[0]), run_time=self.share(0.2))
        # "The code runs without complaint."
        at(self, 0.35)
        self.play(FadeIn(request[1]), run_time=self.share(0.1))
        # "Yet training gets 6.0% of it, and the test set 2.5%."
        at(self, 0.55)
        self.play(FadeIn(frame), FadeIn(overall), *[FadeIn(b[0]) for b in asked], run_time=self.share(0.1))
        self.play(*[GrowFromEdge(b[1], LEFT) for b in asked], *[FadeIn(b[2]) for b in asked], run_time=self.share(0.2))
        self.finish()


class Scene31(VideoScene):
    number = 31

    def construct(self):
        table, heading, request, axes, frame, overall = stratify_layout(self)
        asked = stratify_bars(axes, table.loc["stratified", "train_pct"], table.loc["stratified", "test_pct"])
        fixed = stratify_bars(axes, table.loc["properly", "train_pct"], table.loc["properly", "test_pct"])
        self.add(heading, request, frame, overall, asked)
        pooled = label("pooled away, below\na default threshold", 28, VERMILION, weight=BOLD
                       ).next_to(request[0], RIGHT, 0.5)
        check = card("check the result, not the code", PURPLE, 32).to_edge(DOWN, buff=0.3).shift(0.3 * UP)
        # "The rare class fell below a default threshold and was quietly pooled away."
        self.play(FadeOut(request[1]), FadeIn(pooled), run_time=self.share(0.15))
        # "Lower the threshold, and you get 5.0 and 5.5%."
        at(self, 0.45)
        self.play(*[Transform(a[1], f[1]) for a, f in zip(asked, fixed)],
                  *[Transform(a[2], f[2]) for a, f in zip(asked, fixed)], run_time=self.share(0.2))
        # "Check that a safeguard did what you asked."
        at(self, 0.75)
        self.play(FadeIn(check, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene32(VideoScene):
    number = 32

    def construct(self):
        heading, cards, note = scores_layout(self)
        self.add(heading, cards)
        leak = card("leakage: information about the test data\nreaching the model before the test", VERMILION, 32
                    ).to_edge(DOWN, buff=0.3)
        # "Back to the puzzle."
        self.play(Indicate(cards, color=BLUE, scale_factor=1.03), run_time=self.share(0.2))
        # "Both scores were shaped by leakage: information about the test data reaching the model before the test."
        at(self, 0.3)
        self.play(FadeIn(leak, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def rsq_bars(scene, models, names, colours, heading_text):
    axes, frame = chart([0, 2, 1], [0, 1, 0.25], 6.0, 4.4, [], [0, 0.25, 0.5, 0.75, 1], "", "R squared on the test set")
    frame.move_to([-0.6, -0.5, 0])
    bars = VGroup()
    for i, (model, name, colour) in enumerate(zip(models, names, colours)):
        value = rsq(scene, model)
        bar = vbar(axes, i + 0.5, value, colour, 1.6)
        bars.add(VGroup(bar, label(f"{value:.2f}", 40, INK, weight=BOLD).next_to(bar, UP, 0.15),
                        label(name, 28, SUBDUED, weight=BOLD).next_to(axes.c2p(i + 0.5, 0), DOWN, 0.25)))
    heading = title(heading_text, 46).to_edge(UP, buff=0.4)
    return heading, frame, bars


class Scene33(VideoScene):
    number = 33

    def construct(self):
        heading, frame, bars = rsq_bars(self, ["random", "catch weight"], ["environment\nonly", "plus catch\nweight"],
                                        [BLUE, VERMILION], "Target leakage")
        # "The 0.87 came from adding one column, catch weight."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), FadeIn(bars[1][2]), run_time=self.share(0.15))
        self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), run_time=self.share(0.2))
        # "The forest without it scored 0.25."
        at(self, 0.62)
        self.play(FadeIn(bars[0][2]), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), run_time=self.share(0.2))
        self.finish()


class Scene34(VideoScene):
    number = 34

    def construct(self):
        correlation = self.data("catch-weight")["correlation"].iloc[0]
        heading = title("The same measurement, in different units", 46).to_edge(UP, buff=0.5)
        count = card("animals counted", BLUE, 36)
        weight = card("their weight (kg)", VERMILION, 36)
        pair = VGroup(count, weight).arrange(RIGHT, buff=3.0).move_to([0, 1.2, 0])
        link = DoubleArrow(count.get_right(), weight.get_left(), color=INK, buff=0.15, stroke_width=5, tip_length=0.2)
        corr = label(f"correlation {correlation:.2f}", 28, SUBDUED, weight=BOLD).next_to(link, DOWN, 0.2)
        station = label("a new station, not yet sampled", 34, INK, weight=BOLD).move_to([0, -1.0, 0])
        blanks = VGroup(label("count: ?", 36, BLUE, weight=BOLD), label("catch weight: ?", 36, VERMILION, weight=BOLD)
                        ).arrange(RIGHT, buff=1.8).next_to(station, DOWN, 0.5)
        x = cross(0.9).next_to(blanks[1], RIGHT, 0.3)
        # "But catch weight is the weight of the animals that were counted: the same measurement, in different units."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(count), run_time=self.share(0.15))
        self.play(FadeIn(weight), GrowFromCenter(link), FadeIn(corr), run_time=self.share(0.2))
        # "At a new station, nobody has counted anything, so there is no catch weight."
        at(self, 0.55)
        self.play(FadeIn(station), FadeIn(blanks), run_time=self.share(0.15))
        at(self, 0.82)
        self.play(FadeIn(x, scale=0.5), run_time=self.share(0.08))
        self.finish()


class Scene35(VideoScene):
    number = 35

    def construct(self):
        ask = label("Ask of every feature", 40, SUBDUED, weight=BOLD).move_to([0, 1.8, 0])
        question = VGroup(label("Would this value exist", 60, PURPLE, weight=BOLD),
                          label("for a station I have not", 60, PURPLE, weight=BOLD),
                          label("yet sampled?", 60, PURPLE, weight=BOLD)).arrange(DOWN, buff=0.3).next_to(ask, DOWN, 0.6)
        self.play(FadeIn(ask), run_time=self.share(0.12))
        self.play(LaggedStart(*[FadeIn(q, shift=0.2 * UP) for q in question], lag_ratio=0.4), run_time=self.share(0.45))
        self.finish()


class Scene36(VideoScene):
    number = 36

    def construct(self):
        heading, frame, bars = rsq_bars(self, ["random", "grouped"], ["random\nsplit", "sites kept\ntogether"],
                                        [BLUE, GREEN], "Group leakage")
        # "The 0.13 is the forest without catch weight, tested on sites it never saw."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), *[FadeIn(b[2]) for b in bars],
                  run_time=self.share(0.15))
        self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), run_time=self.share(0.2))
        # "Keeping sites together halved its R squared."
        at(self, 0.6)
        self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), run_time=self.share(0.2))
        self.finish()


class Scene37(VideoScene):
    number = 37

    def construct(self):
        heading, frame, bars = rsq_bars(self, ["random", "grouped"], ["random\nsplit", "sites kept\ntogether"],
                                        [BLUE, GREEN], "Group leakage")
        self.add(heading, frame, bars)
        errors = self.data("leakage").set_index("model")["rmse"]
        head = label("typical error (RMSE)", 30, SUBDUED, weight=BOLD).move_to([4.6, 1.6, 0])
        a = label(f"{errors['random']:.2f}", 44, BLUE, weight=BOLD)
        b = label(f"{errors['grouped']:.2f}", 44, GREEN, weight=BOLD)
        arrow = Arrow(LEFT, RIGHT, color=INK, stroke_width=5, buff=0).scale(0.5)
        pair = VGroup(a, arrow, b).arrange(RIGHT, buff=0.3).next_to(head, DOWN, 0.4)
        better = label("better?", 34, SUBDUED, weight=BOLD).next_to(pair, DOWN, 0.3)
        warn = card("different test sets:\ncompare R squared", VERMILION, 30).next_to(better, DOWN, 0.4)
        # "Its error falls, from 4.82 to 3.76,"
        self.play(FadeIn(head), FadeIn(pair), run_time=self.share(0.2))
        self.play(FadeIn(better), run_time=self.share(0.08))
        # "but that is not an improvement."
        at(self, 0.35)
        self.play(Create(strike(better)), run_time=self.share(0.08))
        # "The two were scored on different test sets, so compare R squared, not the error."
        at(self, 0.5)
        self.play(FadeIn(warn, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene38(VideoScene):
    number = 38

    def construct(self):
        heading, cards, note = scores_layout(self)
        self.add(heading, cards)
        stamps = VGroup(card("leaked: catch weight", VERMILION, 30).next_to(cards[0], DOWN, 0.35),
                        card("honest: a new site", GREEN, 30).next_to(cards[1], DOWN, 0.35))
        # "So the lower score is the honest one."
        self.play(FadeIn(stamps[0], shift=0.2 * UP), cards[0].animate.set_opacity(0.35), run_time=self.share(0.2))
        self.play(FadeIn(stamps[1], shift=0.2 * UP), cards[1][0].animate.set_stroke(GREEN), run_time=self.share(0.15))
        # "It says how well the model predicts a site nobody has surveyed."
        at(self, 0.5)
        self.play(Indicate(cards[1][3], color=GREEN), run_time=self.share(0.25))
        self.finish()


def noise_layout(scene):
    selection = scene.data("selection").set_index("selection")["test_rsq"]
    rng = np.random.default_rng(39)   # schematic noise: the picture, not the page's values
    cells = VGroup(*[Square(0.2, stroke_width=0, fill_color=interpolate_color(ManimColor(GRID), ManimColor(SUBDUED),
                                                                               float(rng.uniform())), fill_opacity=1)
                     for _ in range(200)]).arrange_in_grid(rows=10, buff=0.05).move_to([-4.3, -0.3, 0])
    name = label("200 columns of pure noise", 30, SUBDUED, weight=BOLD).next_to(cells, UP, 0.3)
    chosen = rng.choice(200, 10, replace=False)
    heading = title("Selection leakage", 46).to_edge(UP, buff=0.4)
    rows = VGroup()
    for i, (key, text, colour, digits) in enumerate([("all rows", "chosen using all rows", VERMILION, 2),
                                                     ("training rows", "chosen using training rows only", GREEN, 4)]):
        rows.add(VGroup(label(text, 30, SUBDUED, weight=BOLD),
                        label(f"test R squared {selection[key]:.{digits}f}", 44, colour, weight=BOLD)
                        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-1.0, 1.0 - 2.2 * i, 0], aligned_edge=LEFT))
    return heading, cells, name, chosen, rows


class Scene39(VideoScene):
    number = 39

    def construct(self):
        heading, cells, name, chosen, rows = noise_layout(self)
        # "One more leak. Take 200 columns of pure random noise."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(cells), FadeIn(name), run_time=self.share(0.3))
        # "Choose the ten most correlated with abundance using all the rows,"
        at(self, 0.4)
        self.play(*[cells[i].animate.set_fill(VERMILION).scale(1.2) for i in chosen], run_time=self.share(0.15))
        # "and the test R squared is 0.03."
        at(self, 0.75)
        self.play(FadeIn(rows[0], shift=0.2 * LEFT), run_time=self.share(0.12))
        self.finish()


class Scene40(VideoScene):
    number = 40

    def construct(self):
        heading, cells, name, chosen, rows = noise_layout(self)
        for i in chosen:
            cells[i].set_fill(VERMILION).scale(1.2)
        self.add(heading, cells, name, rows[0])
        truth = label("the truth is zero", 30, INK, weight=BOLD).next_to(rows[1], DOWN, 0.4).align_to(rows[1], LEFT)
        # "Choose them from the training rows only,"
        self.play(*[cells[i].animate.set_fill(GREEN) for i in chosen], run_time=self.share(0.2))
        # "and it is 0.0003, near the truth of zero."
        at(self, 0.4)
        self.play(FadeIn(rows[1], shift=0.2 * LEFT), run_time=self.share(0.15))
        at(self, 0.75)
        self.play(FadeIn(truth), run_time=self.share(0.1))
        self.finish()


class Scene41(VideoScene):
    number = 41

    def construct(self):
        # Schematic: a recipe, specified once, estimated on training data, applied to test data.
        steps = VGroup(*[label(s, 30, INK) for s in ["impute", "log", "dummy", "normalise"]]
                       ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        recipe_box = SurroundingRectangle(steps, color=PURPLE, buff=0.35, corner_radius=0.15)
        recipe = VGroup(recipe_box, steps, label("1 · specify", 32, PURPLE, weight=BOLD).next_to(recipe_box, UP, 0.2)
                        ).move_to([-4.6, -0.4, 0])
        train = card("training data", BLUE, 34).move_to([0.2, 1.2, 0])
        test = card("test data", GREEN, 34).move_to([0.2, -2.0, 0])
        estimate = label("2 · estimate", 32, BLUE, weight=BOLD).next_to(train, RIGHT, 0.4)
        apply = label("3 · apply", 32, GREEN, weight=BOLD).next_to(test, RIGHT, 0.4)
        a1 = Arrow(recipe_box.get_right(), train.get_left(), color=BLUE, stroke_width=5, buff=0.2)
        a2 = Arrow(train.get_bottom(), test.get_top(), color=GREEN, stroke_width=5, buff=0.2)
        stored = label("medians, means, levels", 26, SUBDUED).next_to(a2, RIGHT, 0.2)
        workflow = card("a recipe inside a workflow", PURPLE, 32).to_edge(DOWN, buff=0.3).shift(3.6 * RIGHT)
        heading = title("The cure is order", 46).to_edge(UP, buff=0.4)
        # "The cure is order. Specify each step,"
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(recipe), run_time=self.share(0.2))
        # "estimate it on training data only,"
        at(self, 0.25)
        self.play(GrowArrow(a1), FadeIn(train), FadeIn(estimate), run_time=self.share(0.12))
        # "then apply it to the test data."
        at(self, 0.45)
        self.play(GrowArrow(a2), FadeIn(stored), FadeIn(test), FadeIn(apply), run_time=self.share(0.12))
        # "A recipe inside a workflow does exactly that."
        at(self, 0.72)
        self.play(FadeIn(workflow, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene42(KeyPointScene):
    number, point = 42, 3


# The quiz (scenes 43–44) ------------------------------------------------------------------

class Scene43(QuizScene):
    number = 43
    question = ("A habitat model uses a habitat class", "assigned by looking at what was caught.",
                "Its score is excellent.", "What is wrong?")


class Scene44(VideoScene):
    number = 44

    def construct(self):
        # Schematic: the class comes from the catch, and a new station has no catch.
        answer = label("Target leakage", 56, VERMILION, weight=BOLD).to_edge(UP, buff=0.5)
        catch = card("what was caught", BLUE, 34).move_to([-3.6, 0.8, 0])
        habitat = card("habitat class", ORANGE, 34).move_to([3.0, 0.8, 0])
        arrow = Arrow(catch.get_right(), habitat.get_left(), color=INK, stroke_width=5, buff=0.2)
        new = label("a new station: nothing caught yet", 34, INK, weight=BOLD).move_to([0, -1.2, 0])
        missing = label("habitat class: ?", 36, ORANGE, weight=BOLD).next_to(new, DOWN, 0.5)
        x = cross(0.9).next_to(missing, RIGHT, 0.3)
        field = label("the model cannot run in the field", 32, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.5)
        # "Target leakage."
        self.play(FadeIn(answer), run_time=self.share(0.1))
        # "The class could not exist for a station nobody has sampled,"
        self.play(FadeIn(catch), GrowArrow(arrow), FadeIn(habitat), run_time=self.share(0.15))
        at(self, 0.3)
        self.play(FadeIn(new), FadeIn(missing), run_time=self.share(0.12))
        self.play(FadeIn(x, scale=0.5), run_time=self.share(0.06))
        # "so the model cannot run in the field."
        at(self, 0.7)
        self.play(FadeIn(field, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


# The recap (scenes 45–47) and the end card (scene 48) --------------------------------------

class Scene45(RecapScene):
    number, point = 45, 1


class Scene46(RecapScene):
    number, point = 46, 2


class Scene47(RecapScene):
    number, point = 47, 3


class Scene48(EndCardScene):
    number = 48
