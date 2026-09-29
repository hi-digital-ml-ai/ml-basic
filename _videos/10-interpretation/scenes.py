"""Manim scenes for the interpretation video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/10-interpretation
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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["Which predictors a model relies on",
            "Why the right model can draw the wrong shape",
            "What no model can warn you about"]
ANSWERS = ["Add random columns,\nand count how often\neach variable beats them",
           "The data never\nseparated depth from\ntemperature: say so",
           "What its data do not\ncontain: a shift, or\na biased gear"]
RECAP = ["Importance needs a null",
         "The data must separate the effects",
         "A model cannot see what its data lack"]


class Scene01(LearnScene):
    number = 1


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def polyline(axes, xs, ys, colour, width=6, dashed=False):
    points = [axes.c2p(x, y) for x, y in zip(xs, ys)]
    line = VMobject(color=colour, stroke_width=width).set_points_as_corners(points)
    return DashedVMobject(line, num_dashes=60) if dashed else line


def ribbon(axes, xs, lower, upper, colour, opacity):
    points = [axes.c2p(x, y) for x, y in zip(xs, upper)] + \
             [axes.c2p(x, y) for x, y in zip(xs[::-1], lower[::-1])]
    return Polygon(*points, stroke_width=0, fill_color=colour, fill_opacity=opacity)


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name,
          x_fmt="{:g}", y_fmt="{:g}", size=24):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
    axes = plain_axes(x_range, y_range, x_length, y_length)
    tx = VGroup(*[label(x_fmt.format(v), size, SUBDUED).next_to(axes.c2p(v, y_range[0]), DOWN, 0.15)
                  for v in x_ticks])
    ty = VGroup(*[label(y_fmt.format(v), size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15)
                  for v in y_ticks])
    xn = label(x_name, 26, SUBDUED).next_to(tx if len(tx) else axes, DOWN, 0.2)
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


def hbar_rows(names, values, colours, scale, x0=-1.6, top=1.2, step=1.3, texts=None, size=32, height=0.7):
    """Horizontal bars, one row each: name at the left of x0, bar from x0, value after it."""
    rows = VGroup()
    for i, (name, value, colour) in enumerate(zip(names, values, colours)):
        y = top - step * i
        text = label(name, size).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=max(scale * value, 0.03), height=height, stroke_width=0, fill_color=colour,
                        fill_opacity=1).move_to([x0, y, 0], aligned_edge=LEFT)
        value_text = label(texts[i] if texts else f"{value:.3f}", size, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)
        rows.add(VGroup(text, bar, value_text))
    return rows


def at(scene, fraction):
    """Wait until this fraction of the narration."""
    scene.wait(max(scene.share(fraction) - scene.time, 0.01))


def percent(value, digits=0):
    return f"{100 * value:.{digits}f}%"


PRETTY = {"depth_m": "depth", "temperature_c": "temperature", "chlorophyll_mg_m3": "chlorophyll",
          "salinity_psu": "salinity", "survey_year": "survey year", "longitude": "longitude",
          "latitude": "latitude", "substrate": "substrate", "season": "season",
          "noise_1": "random 1", "noise_2": "random 2", "noise_3": "random 3"}


def pretty(term):
    if term in PRETTY:
        return PRETTY[term]
    head, _, level = term.partition("_")
    return f"{head}: {level}"


def is_noise(term):
    return term.startswith("noise_")


# The puzzle (scenes 2–5, page results) --------------------------------------------------------

CURVE_COLOURS = {"truth": GREEN, "forest": BLUE, "glm": VERMILION}


def depth_layout(scene):
    # The page quotes the curves at 10 m and 160 m; the chart stops there too.
    curves = scene.data("depth-curves")
    curves = curves[(curves["depth_m"] >= 10) & (curves["depth_m"] <= 160)]
    axes, frame = chart([0, 170, 20], [0, 9, 1], 8.6, 5.0, [10, 40, 80, 120, 160], [0, 2, 4, 6, 8],
                        "depth (m)", "partial dependence (count)")
    VGroup(frame).move_to([-1.2, -0.3, 0])
    lines = {k: polyline(axes, curves["depth_m"], curves[k], c, 7) for k, c in CURVE_COLOURS.items()}
    peak = curves.loc[curves["truth"].idxmax()]
    marker = DashedLine(axes.c2p(peak["depth_m"], 0), axes.c2p(peak["depth_m"], 8.8), color=GREEN,
                        stroke_width=3)
    peak_name = label(f"true peak: {peak['depth_m']:.0f} m", 30, GREEN, weight=BOLD).next_to(
        axes.c2p(peak["depth_m"], 0.5), RIGHT, 0.15)
    names = {"truth": "truth", "forest": "random forest", "glm": "the right formula"}
    tags = {k: label(names[k], 30, c, weight=BOLD).next_to(axes.c2p(160, curves[k].iloc[-1]), RIGHT, 0.2)
            for k, c in CURVE_COLOURS.items()}
    tags["truth"].shift(0.3 * UP)      # the truth and the GLM end 0.16 apart at 160 m
    tags["glm"].shift(0.3 * DOWN)
    ends = {k: VGroup(*[VGroup(Dot(axes.c2p(d, curves.loc[curves["depth_m"] == d, k].item()), 0.09, color=c),
                               label(f"{curves.loc[curves['depth_m'] == d, k].item():.2f}", 28, c, weight=BOLD)
                               .next_to(axes.c2p(d, curves.loc[curves["depth_m"] == d, k].item()),
                                        LEFT if (k == "glm" and d == 160) else UP, 0.15)
                               .shift(0.25 * DOWN if (k == "glm" and d == 160) else 0 * UP))
                        for d in (10, 160)])
            for k, c in CURVE_COLOURS.items()}
    return axes, frame, lines, marker, peak_name, tags, ends


class Scene02(VideoScene):
    number = 2

    def construct(self):
        axes, frame, lines, marker, peak_name, tags, ends = depth_layout(self)
        n = len(self.data("stations"))
        survey = label(f"{n} stations, simulated", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.4)
        # "Here is a survey of 720 stations."
        self.play(FadeIn(survey), FadeIn(frame), run_time=self.share(0.2))
        # "It is simulated, so we know the truth: abundance peaks at 80 metres depth."
        at(self, 0.4)
        self.play(Create(lines["truth"]), FadeIn(tags["truth"]), run_time=self.share(0.3))
        self.play(Create(marker), FadeIn(peak_name), run_time=self.share(0.15))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        axes, frame, lines, marker, peak_name, tags, ends = depth_layout(self)
        self.add(frame, lines["truth"], tags["truth"], marker, peak_name)
        # "Fit a random forest and ask it about depth."
        self.play(Create(lines["forest"]), FadeIn(tags["forest"]), run_time=self.share(0.35))
        # "It says abundance falls with depth, from 5.04 to 3.77."
        at(self, 0.5)
        self.play(LaggedStart(*[FadeIn(e) for e in ends["forest"]], lag_ratio=0.6), run_time=self.share(0.35))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        axes, frame, lines, marker, peak_name, tags, ends = depth_layout(self)
        self.add(frame, lines["truth"], tags["truth"], marker, peak_name, lines["forest"], tags["forest"],
                 ends["forest"])
        blame = card("blame the black box?", SUBDUED, 36).move_to([-1.2, 3.3, 0])
        formula = card("the formula that made the data", VERMILION, 40).move_to([-1.2, 2.3, 0])
        # "So blame the black box."
        self.play(FadeIn(blame, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "Fit the exactly right model instead: a regression given the formula that made the data."
        at(self, 0.35)
        self.play(FadeIn(formula, scale=0.9), run_time=self.share(0.2))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        axes, frame, lines, marker, peak_name, tags, ends = depth_layout(self)
        self.add(frame, lines["truth"], tags["truth"], marker, peak_name, lines["forest"], tags["forest"],
                 ends["forest"])
        why = card("two models, one wrong shape: why?", PURPLE, 38).to_edge(UP, buff=0.25)
        # "It tells the same story, only steeper: 8.19 falling to 1.80."
        self.play(Create(lines["glm"]), FadeIn(tags["glm"]), run_time=self.share(0.3))
        self.play(LaggedStart(*[FadeIn(e) for e in ends["glm"]], lag_ratio=0.6), run_time=self.share(0.25))
        # "Two models, one wrong shape. Why?"
        at(self, 0.65)
        self.play(FadeIn(why, scale=0.9), run_time=self.share(0.15))
        self.play(Wiggle(why[1]), run_time=self.share(0.15))
        self.finish()


# What the model relies on (scenes 6–15) -----------------------------------------------------

class Scene06(VideoScene):
    number = 6

    def construct(self):
        # Schematic: a generic importance plot, bars of made-up lengths and no values.
        head = title("So what drives it?", 56).to_edge(UP, buff=0.8)
        lengths = [5.2, 3.9, 3.1, 2.4, 1.8, 1.2, 0.7]
        bars = VGroup(*[Rectangle(width=w, height=0.45, stroke_width=0, fill_color=BLUE, fill_opacity=0.8)
                        for w in lengths]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([0.6, -0.6, 0])
        names = VGroup(*[RoundedRectangle(width=1.6, height=0.28, corner_radius=0.1, stroke_width=0,
                                          fill_color=GRID, fill_opacity=1).next_to(b, LEFT, 0.3) for b in bars])
        caption = label("an importance plot", 34, SUBDUED, weight=BOLD).to_edge(DOWN, buff=0.5)
        # "Start with the question everyone asks: so what drives it?"
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "The usual answer is an importance plot."
        at(self, 0.55)
        self.play(FadeIn(names), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.15),
                  run_time=self.share(0.3))
        self.play(FadeIn(caption), run_time=self.share(0.1))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        # Schematic: the table's columns, then three more of random shades.
        rng = np.random.default_rng(7)
        measured = ["depth", "temp.", "chl.", "salinity", "substrate", "season", "year", "lon.", "lat."]
        rows = 10

        def column(name, colour, width=0.95):
            cells = VGroup(*[Square(0.34, stroke_width=0, fill_color=colour,
                                    fill_opacity=float(rng.uniform(0.15, 0.9))) for _ in range(rows)]
                           ).arrange(DOWN, buff=0.05)
            head = label(name, 22, colour, weight=BOLD).rotate(PI / 4)
            head.next_to(cells, UP, 0.15)
            return VGroup(cells, head)

        table = VGroup(*[column(n, BLUE) for n in measured]).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        noise = VGroup(*[column(f"random {i}", VERMILION) for i in (1, 2, 3)]
                       ).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        VGroup(table, noise).arrange(RIGHT, buff=0.6, aligned_edge=DOWN).move_to([0, -0.2, 0])
        brace = Brace(noise, DOWN, color=VERMILION)
        cannot = label("cannot possibly matter", 32, VERMILION, weight=BOLD).next_to(brace, DOWN, 0.15)
        self.add(table)
        # "First, we add three columns of random numbers."
        self.play(LaggedStart(*[FadeIn(c, shift=0.3 * LEFT) for c in noise], lag_ratio=0.3),
                  run_time=self.share(0.4))
        # "They cannot possibly matter."
        at(self, 0.6)
        self.play(GrowFromCenter(brace), FadeIn(cannot), run_time=self.share(0.2))
        self.finish()


def impurity_layout(scene):
    table = scene.data("impurity").sort_values("importance", ascending=False).reset_index(drop=True)
    head = label("Default importance (impurity), 16 terms", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.25)
    colours = [VERMILION if is_noise(t) else BLUE for t in table["term"]]
    rows = hbar_rows([pretty(t) for t in table["term"]], table["importance"], colours, 6.0,
                     x0=-1.8, top=2.95, step=0.4, texts=[""] * len(table), size=22, height=0.3)
    ranks = VGroup(*[label(str(i + 1), 22, SUBDUED).move_to([-5.4, r[1].get_y(), 0])
                     for i, r in enumerate(rows)])
    return table, head, rows, ranks


class Scene08(VideoScene):
    number = 8

    def construct(self):
        table, head, rows, ranks = impurity_layout(self)
        noise_rows = [i for i, t in enumerate(table["term"]) if is_noise(t)]
        places = ", ".join(str(i + 1) for i in noise_rows)
        note = label(f"random columns: {places} of {len(table)}", 32, VERMILION, weight=BOLD
                     ).move_to([3.4, 0.6, 0])
        # "The default importance ranks them ..."
        self.play(FadeIn(head), FadeIn(ranks), FadeIn(VGroup(*[r[0] for r in rows])), run_time=self.share(0.15))
        self.play(LaggedStart(*[GrowFromEdge(r[1], LEFT) for r in rows], lag_ratio=0.05), run_time=self.share(0.3))
        # "... sixth, seventh and eighth of sixteen."
        self.play(*[Indicate(rows[i], color=VERMILION, scale_factor=1.08) for i in noise_rows],
                  FadeIn(note), run_time=self.share(0.3))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        table, head, rows, ranks = impurity_layout(self)
        noise_rows = [i for i, t in enumerate(table["term"]) if is_noise(t)]
        places = ", ".join(str(i + 1) for i in noise_rows)
        note = label(f"random columns: {places} of {len(table)}", 32, VERMILION, weight=BOLD
                     ).move_to([3.4, 0.6, 0])
        self.add(head, ranks, rows, note)
        salinity = [i for i, t in enumerate(table["term"]) if t == "salinity_psu"]
        substrate = [i for i, t in enumerate(table["term"]) if t.startswith("substrate")]
        real = label("substrate: a real effect", 32, ORANGE, weight=BOLD).move_to([3.4, -1.9, 0])
        # "Above salinity, ..."
        self.play(*[rows[i][1].animate.set_fill(ORANGE) for i in salinity], run_time=self.share(0.15))
        # "... and above every substrate term."
        at(self, 0.25)
        self.play(*[rows[i][1].animate.set_fill(ORANGE) for i in substrate],
                  *[Indicate(rows[i][0], color=ORANGE) for i in substrate], run_time=self.share(0.3))
        # "And substrate has a real effect."
        at(self, 0.62)
        self.play(FadeIn(real, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        # Schematic: split points on a measured column against a yes-or-no one.
        left_line = Line([-6.0, 0.6, 0], [-0.8, 0.6, 0], color=INK, stroke_width=4)
        cuts = VGroup(*[Line([x, 0.35, 0], [x, 0.85, 0], color=BLUE, stroke_width=2)
                        for x in np.linspace(-5.9, -0.9, 60)])
        left_name = label("a measured column", 34, INK, weight=BOLD).next_to(left_line, UP, 0.7)
        left_note = label("hundreds of places to split", 30, BLUE, weight=BOLD).next_to(left_line, DOWN, 0.5)
        boxes = VGroup(card("rock", SUBDUED, 34), card("not rock", SUBDUED, 34)).arrange(RIGHT, buff=0.9
                                                                                           ).move_to([3.6, 0.6, 0])
        cut = Line(boxes.get_center() + 0.6 * UP, boxes.get_center() + 0.6 * DOWN, color=BLUE, stroke_width=5)
        right_name = label("a yes-or-no column", 34, INK, weight=BOLD).next_to(boxes, UP, 0.5)
        right_note = label("one", 30, BLUE, weight=BOLD).next_to(boxes, DOWN, 0.5)
        chance = label("among hundreds, chance finds one that helps a little", 32, VERMILION, weight=BOLD
                       ).to_edge(DOWN, buff=0.7)
        # "A measured column offers hundreds of places to split."
        self.play(FadeIn(left_name), Create(left_line), run_time=self.share(0.1))
        self.play(LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.03), FadeIn(left_note),
                  run_time=self.share(0.2))
        # "A yes-or-no column offers one."
        at(self, 0.36)
        self.play(FadeIn(right_name), FadeIn(boxes), run_time=self.share(0.1))
        self.play(Create(cut), FadeIn(right_note), run_time=self.share(0.1))
        # "Among hundreds, chance alone finds one that helps a little."
        at(self, 0.6)
        self.play(Indicate(cuts[23], color=VERMILION, scale_factor=2), FadeIn(chance, shift=0.2 * UP),
                  run_time=self.share(0.2))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        # Schematic: one column's values shuffled; the error bar grows.
        shades = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 0.2, 0.5]
        cells = VGroup(*[Square(0.45, stroke_width=0, fill_color=BLUE, fill_opacity=s) for s in shades]
                       ).arrange(DOWN, buff=0.06).move_to([-3.2, -0.3, 0])
        name = label("one column", 32, BLUE, weight=BOLD).next_to(cells, UP, 0.3)
        question = label("how much worse does the model predict?", 34, INK, weight=BOLD).to_edge(UP, buff=0.6)
        base = Rectangle(width=2.4, height=0.55, stroke_width=0, fill_color=GREY, fill_opacity=1
                         ).move_to([0.8, 0.5, 0], aligned_edge=LEFT)
        base_name = label("error", 30).next_to(base, LEFT, 0.25)
        after = Rectangle(width=4.2, height=0.55, stroke_width=0, fill_color=VERMILION, fill_opacity=1
                          ).move_to([0.8, -0.6, 0], aligned_edge=LEFT)
        after_name = label("shuffled", 30, VERMILION, weight=BOLD).next_to(after, LEFT, 0.25)
        increase = label("the increase is the importance", 30, VERMILION, weight=BOLD).next_to(after, DOWN, 0.4)
        order = [3, 6, 0, 7, 2, 5, 1, 4]
        # "Permutation importance asks a better question."
        self.play(FadeIn(cells), FadeIn(name), FadeIn(base), FadeIn(base_name), run_time=self.share(0.15))
        self.play(FadeIn(question), run_time=self.share(0.1))
        # "Shuffle one column: ..."
        at(self, 0.45)
        targets = [cells[j].get_center() for j in range(len(cells))]
        self.play(*[cells[i].animate.move_to(targets[order[i]]) for i in range(len(cells))],
                  run_time=self.share(0.15))
        # "... how much worse does the model predict?"
        self.play(GrowFromEdge(after, LEFT), FadeIn(after_name), run_time=self.share(0.15))
        self.play(FadeIn(increase), run_time=self.share(0.1))
        self.finish()


def permutation_layout(scene):
    table = scene.data("permutation").sort_values("increase").reset_index(drop=True)
    noise = table[table["variable"].map(is_noise)]
    lo, hi = noise["increase"].min(), noise["increase"].max()
    axes, frame = chart([-0.05, 0.25, 0.05], [0, len(table) + 0.5, 1], 7.6, 5.4,
                        [0, 0.05, 0.1, 0.15, 0.2], [], "increase in test error when shuffled", "")
    frame.move_to([1.3, -0.45, 0])
    band = Rectangle(width=axes.c2p(hi, 0)[0] - axes.c2p(lo, 0)[0], height=axes.y_length, stroke_width=0,
                     fill_color=GREY, fill_opacity=0.25).move_to(axes.c2p((lo + hi) / 2, (len(table) + 0.5) / 2))
    band_name = label("random columns", 26, SUBDUED, weight=BOLD).next_to(band, UP, 0.1)
    rows = VGroup()
    for i, r in table.iterrows():
        colour = VERMILION if is_noise(r["variable"]) else (BLUE if r["increase"] - 2 * r["se"] > hi else GREY)
        y = i + 0.75
        bar = Line(axes.c2p(r["increase"] - 2 * r["se"], y), axes.c2p(r["increase"] + 2 * r["se"], y),
                   color=colour, stroke_width=4)
        dot = Dot(axes.c2p(r["increase"], y), 0.1, color=colour)
        name = label(pretty(r["variable"]), 24, colour if colour != GREY else SUBDUED,
                     weight=BOLD if colour == BLUE else NORMAL).next_to(axes.c2p(-0.05, y), LEFT, 0.2)
        rows.add(VGroup(name, bar, dot))
    clear = [i for i, r in table.iterrows() if not is_noise(r["variable"]) and r["increase"] - 2 * r["se"] > hi]
    return table, frame, band, band_name, rows, clear


class Scene12(VideoScene):
    number = 12

    def construct(self):
        table, frame, band, band_name, rows, clear = permutation_layout(self)
        noise_rows = [i for i, v in enumerate(table["variable"]) if is_noise(v)]
        n = len(self.data("halves"))
        test = self.data("halves")["test"].item()
        note = label(f"on {test} held-out stations", 26, SUBDUED).to_corner(UR, buff=0.4)
        self.play(FadeIn(frame), FadeIn(note), FadeIn(VGroup(*[r[0] for r in rows])), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(VGroup(r[1], r[2])) for r in rows], lag_ratio=0.05), run_time=self.share(0.15))
        # "Now the random columns mark a band: what nothing looks like."
        self.play(FadeIn(band), FadeIn(band_name),
                  *[Indicate(rows[i][2], color=VERMILION, scale_factor=1.6) for i in noise_rows],
                  run_time=self.share(0.2))
        # "Temperature, latitude, longitude, substrate and depth clear it."
        at(self, 0.5)
        self.play(LaggedStart(*[Indicate(rows[i][0], color=BLUE, scale_factor=1.15) for i in reversed(clear)],
                              lag_ratio=0.3), run_time=self.share(0.4))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        splits = self.data("splits")
        real = splits[~splits["variable"].map(is_noise)]
        summary = real.groupby("variable")["rank"].agg(["min", "max"]).sort_values("min").reset_index()
        n_splits = splits["split"].nunique()
        n_vars = splits.groupby("split")["variable"].count().max()
        head = label(f"Rank over {n_splits} splits (1 = most important)", 30, SUBDUED, weight=BOLD
                     ).to_edge(UP, buff=0.25)
        axes, frame = chart([0.5, n_vars + 0.5, 1], [0, len(summary) + 0.5, 1], 8.0, 5.4,
                            list(range(1, n_vars + 1)), [], "rank", "")
        frame.move_to([1.4, -0.3, 0])
        rows = VGroup()
        for i, r in summary.iterrows():
            y = len(summary) - i
            colour = VERMILION if r["variable"] == "chlorophyll_mg_m3" else BLUE
            span = Line(axes.c2p(r["min"], y), axes.c2p(r["max"], y), color=colour, stroke_width=10)
            ends = VGroup(Dot(axes.c2p(r["min"], y), 0.1, color=colour), Dot(axes.c2p(r["max"], y), 0.1, color=colour))
            name = label(pretty(r["variable"]), 26, colour if colour == VERMILION else INK,
                         weight=BOLD if colour == VERMILION else NORMAL).next_to(axes.c2p(0.5, y), LEFT, 0.25)
            rows.add(VGroup(name, span, ends))
        chl = summary.index[summary["variable"] == "chlorophyll_mg_m3"].item()
        chl_row = summary.loc[chl]
        chl_note = label(f"first in one split, {int(chl_row['max'])}th in another", 30, VERMILION, weight=BOLD
                         ).next_to(rows[chl][1], UP, 0.15)
        # "But one split is not a result."
        self.play(FadeIn(head), FadeIn(frame), FadeIn(VGroup(*[r[0] for r in rows])), run_time=self.share(0.2))
        # "Over eight splits, ..."
        self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(r[1]), FadeIn(r[2])) for r in rows], lag_ratio=0.1),
                  run_time=self.share(0.3))
        # "... chlorophyll ranked first in one and eleventh in another."
        at(self, 0.6)
        self.play(Indicate(rows[chl], color=VERMILION, scale_factor=1.05), FadeIn(chl_note), run_time=self.share(0.25))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        runs = self.data("seed-split")
        lo, hi = runs["rmse"].min(), runs["rmse"].max()
        axes, frame = chart([3.5, 5.5, 0.5], [0, 3, 1], 9.0, 3.6, [3.5, 4.0, 4.5, 5.0, 5.5], [],
                            "test error (RMSE), eight runs each", "", x_fmt="{:.1f}")
        frame.move_to([0.8, -0.4, 0])
        groups = {}
        for key, y, colour, name in (("seed", 2.1, BLUE, "the forest's seed"), ("split", 0.9, VERMILION, "the split")):
            values = runs[runs["varying"] == key]["rmse"]
            dots = VGroup(*[Dot(axes.c2p(v, y), 0.12, color=colour, fill_opacity=0.6) for v in values])
            text = label(name, 30, colour, weight=BOLD).next_to(axes.c2p(3.5, y), LEFT, 0.3)
            spread = values.max() - values.min()
            moved = label(f"moved by {spread:.3f}" if key == "seed" else f"moved by {spread:.2f}", 32, colour,
                          weight=BOLD).next_to(axes.c2p(values.max(), y), UP if key == "seed" else DOWN, 0.3)
            if key == "seed":
                moved.next_to(axes.c2p(values.mean(), y), UP, 0.35)
            groups[key] = (dots, text, moved)
        head = label("Changing only …", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.6)
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.1))
        # "Even the forest's random seed matters little next to the split. Changing the seed moved
        # the test error by 0.016."
        at(self, 0.3)
        self.play(FadeIn(groups["seed"][1]), LaggedStart(*[FadeIn(d, scale=0.5) for d in groups["seed"][0]],
                                                         lag_ratio=0.1), run_time=self.share(0.15))
        self.play(FadeIn(groups["seed"][2]), run_time=self.share(0.1))
        # "Changing the split moved it by 1.50."
        at(self, 0.7)
        self.play(FadeIn(groups["split"][1]), LaggedStart(*[FadeIn(d, scale=0.5) for d in groups["split"][0]],
                                                          lag_ratio=0.1), run_time=self.share(0.15))
        self.play(FadeIn(groups["split"][2]), run_time=self.share(0.1))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        splits = self.data("splits")
        n_splits = splits["split"].nunique()
        real = splits[~splits["variable"].map(is_noise)].copy()
        real["above"] = real["increase"] > real["noise_ceiling"]
        counts = real.groupby("variable")["above"].sum().sort_values(ascending=False)
        head = label(f"Splits (of {n_splits}) in which each beats every random column", 30, SUBDUED,
                     weight=BOLD).to_edge(UP, buff=0.35)
        colours = [VERMILION if c == 0 else BLUE for c in counts]
        rows = hbar_rows([pretty(v) for v in counts.index], counts.values.astype(float), colours, 0.75,
                         x0=-1.2, top=2.5, step=0.62, texts=[str(int(c)) for c in counts], size=28, height=0.42)
        zero = [i for i, c in enumerate(counts) if c == 0]
        note = label("the two with no effect", 32, VERMILION, weight=BOLD).next_to(rows[zero[-1]], DOWN, 0.3
                                                                                    ).set_x(rows[zero[-1]][0].get_x())
        # "What stays steady is a count."
        self.play(FadeIn(head), FadeIn(VGroup(*[r[0] for r in rows])), run_time=self.share(0.1))
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                              lag_ratio=0.1), run_time=self.share(0.25))
        # "Salinity and survey year beat the random columns in none of the eight splits."
        at(self, 0.4)
        self.play(*[Indicate(rows[i], color=VERMILION, scale_factor=1.08) for i in zero], run_time=self.share(0.25))
        # "They are the two with no effect."
        at(self, 0.78)
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene16(KeyPointScene):
    number, point = 16, 1


# The puzzle, solved (scenes 17–26) ----------------------------------------------------------

class Scene17(VideoScene):
    number = 17

    def construct(self):
        # Schematic: stations at their own depths, all moved to one depth, averaged, then the next.
        rng = np.random.default_rng(17)
        axis = Line([-5.5, -2.2, 0], [5.5, -2.2, 0], color=INK, stroke_width=3)
        axis_name = label("depth", 30, SUBDUED).next_to(axis, DOWN, 0.2)
        xs = rng.uniform(-5.2, 5.2, 12)
        ys = np.linspace(2.4, -1.6, 12)
        dots = VGroup(*[Dot([x, y, 0], 0.11, color=GREY) for x, y in zip(xs, ys)])
        name = label("every station", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.3)
        path = VGroup()
        self.play(Create(axis), FadeIn(axis_name), FadeIn(dots), FadeIn(name), run_time=self.share(0.15))
        # "A partial dependence plot sets every station to one depth, ..."
        for k, x in enumerate([-4.0, -1.5, 1.0, 3.5]):
            share = 0.14 if k == 0 else 0.1
            self.play(*[d.animate.set_x(x).set_color(BLUE) for d in dots], run_time=self.share(share))
            # "... averages the predictions, ..."
            mean = Dot([x, -2.2 + 0.9 + 0.3 * np.sin(k), 0], 0.15, color=VERMILION)
            self.play(FadeIn(mean, scale=0.5), run_time=self.share(0.05))
            if len(path):
                self.play(Create(Line(path[-1].get_center(), mean.get_center(), color=VERMILION, stroke_width=5)),
                          run_time=self.share(0.03))
            path.add(mean)
        # "... and moves along."
        self.play(FadeOut(dots), run_time=self.share(0.05))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        curves = self.data("temperature-curves")
        axes, frame = chart([2, 17, 1], [0, 6.5, 1], 7.4, 5.0, [3, 6, 9, 12, 15], [0, 2, 4, 6],
                            "temperature (°C)", "partial dependence (count)")
        frame.move_to([-1.9, -0.3, 0])
        truth = polyline(axes, curves["temperature_c"], curves["truth"], GREEN, 7)
        forest = polyline(axes, curves["temperature_c"], curves["forest"], BLUE, 7)
        peaks = {}
        for key, colour in (("truth", GREEN), ("forest", BLUE)):
            p = curves.loc[curves[key].idxmax()]
            line = DashedLine(axes.c2p(p["temperature_c"], 0), axes.c2p(p["temperature_c"], p[key]),
                              color=colour, stroke_width=3)
            peaks[key] = (p, line)
        t_name = label(f"truth: peak {peaks['truth'][0]['temperature_c']:g} °C", 28, GREEN, weight=BOLD
                       ).next_to(axes.c2p(15, curves["truth"].iloc[-1]), RIGHT, 0.2).shift(0.3 * DOWN)
        f_name = label(f"random forest: peak {peaks['forest'][0]['temperature_c']:g} °C", 28, BLUE, weight=BOLD
                       ).next_to(axes.c2p(16, curves["forest"].iloc[-1]), RIGHT, 0.2).shift(0.3 * UP)
        f_name.move_to([2.1, 1.2, 0], aligned_edge=LEFT)
        t_name.move_to([2.1, 0.5, 0], aligned_edge=LEFT)
        works = label("the shape comes back", 34, GREEN, weight=BOLD).to_edge(UP, buff=0.3)
        # "For temperature, it works."
        self.play(FadeIn(frame), run_time=self.share(0.1))
        self.play(Create(truth), Create(forest), FadeIn(works), run_time=self.share(0.25))
        # "The forest's peak is at 7.75 degrees, against a true 9."
        at(self, 0.4)
        self.play(Create(peaks["forest"][1]), FadeIn(f_name), run_time=self.share(0.15))
        at(self, 0.75)
        self.play(Create(peaks["truth"][1]), FadeIn(t_name), run_time=self.share(0.15))
        self.finish()


def stations_layout(scene):
    stations = scene.data("stations")
    axes, frame = chart([0, 200, 20], [0, 18, 2], 8.0, 5.4, [0, 50, 100, 150, 200], [0, 5, 10, 15],
                        "depth (m)", "temperature (°C)")
    frame.move_to([-1.6, -0.3, 0])
    dots = VGroup(*[Dot(axes.c2p(d, t), 0.045, color=BLUE, fill_opacity=0.55)
                    for d, t in zip(stations["depth_m"], stations["temperature_c"])])
    return stations, axes, frame, dots


class Scene19(VideoScene):
    number = 19

    def construct(self):
        stations, axes, frame, dots = stations_layout(self)
        cold_shallow = Ellipse(width=2.4, height=1.5, color=VERMILION, stroke_width=5).move_to(axes.c2p(25, 3.5))
        warm_deep = Ellipse(width=2.4, height=1.5, color=VERMILION, stroke_width=5).move_to(axes.c2p(170, 14))
        cs = label("cold and shallow:\nalmost none", 28, VERMILION, weight=BOLD).next_to(cold_shallow, UP, 0.1)
        wd = label("warm and deep:\nalmost none", 28, VERMILION, weight=BOLD).next_to(warm_deep, RIGHT, 0.15)
        cs.next_to(cold_shallow, RIGHT, 0.15).shift(0.2 * DOWN)
        for words in (cs, wd):
            words.add_background_rectangle(color=BACKGROUND, opacity=0.85)
        head = label(f"{len(stations)} stations", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.3)
        # "Depth fails because of how the survey was taken."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=self.share(0.3))
        # "There are almost no cold shallow stations, ..."
        at(self, 0.5)
        self.play(Create(cold_shallow), FadeIn(cs), run_time=self.share(0.15))
        # "... and almost no warm deep ones."
        at(self, 0.78)
        self.play(Create(warm_deep), FadeIn(wd), run_time=self.share(0.15))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        stations, axes, frame, dots = stations_layout(self)
        self.add(frame, dots)
        r = np.corrcoef(stations["depth_m"], stations["temperature_c"])[0, 1]
        corr = label(f"correlation {r:.2f}".replace("-", "−"), 30, SUBDUED, weight=BOLD).move_to([4.6, 2.4, 0])
        humps = VGroup(label("two humps,", 34, INK, weight=BOLD), label("one pattern", 34, INK, weight=BOLD)
                       ).arrange(DOWN, buff=0.12).move_to([4.6, 1.2, 0])
        takes = VGroup(label("temperature takes", 30, GREEN, weight=BOLD), label("the shared part", 30, GREEN, weight=BOLD)
                       ).arrange(DOWN, buff=0.1).move_to([4.6, -0.4, 0])
        left = VGroup(label("depth is left", 30, VERMILION, weight=BOLD), label("with a decline", 30, VERMILION, weight=BOLD)
                      ).arrange(DOWN, buff=0.1).move_to([4.6, -1.8, 0])
        # "So the data cannot separate the two humps."
        self.play(FadeIn(corr), FadeIn(humps), run_time=self.share(0.2))
        # "Temperature takes the shared part, ..."
        at(self, 0.4)
        self.play(FadeIn(takes, shift=0.2 * UP), run_time=self.share(0.15))
        # "... and depth is left with a decline."
        at(self, 0.72)
        self.play(FadeIn(left, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        terms = self.data("glm-terms")
        quad = terms[terms["term"] == "depth, quadratic"].iloc[0]
        ratio = quad["truth"] / quad["estimate"]
        head = label("The right formula's depth term (the curvature)", 30, SUBDUED, weight=BOLD
                     ).to_edge(UP, buff=0.8)
        scale = 7.0 / abs(quad["truth"])
        rows = hbar_rows(["true size", "estimated"], [abs(quad["truth"]), abs(quad["estimate"])], [GREEN, VERMILION],
                         scale, x0=-2.6, top=1.0, step=1.3, texts=["", f"about a {ratio:.0f}th of it"], size=34)
        p = label(f"p = {quad['p']:.2f}", 40, VERMILION, weight=BOLD).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(head), FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), run_time=self.share(0.2))
        # "Its depth term came back at a fourteenth of its true size, ..."
        at(self, 0.3)
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.25))
        # "... with a p value of 0.63."
        at(self, 0.72)
        self.play(FadeIn(p, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        plot = card("a different plot", SUBDUED, 48).move_to([0, 1.0, 0])
        survey = card("a different survey", GREEN, 52).move_to([0, -1.2, 0])
        box, mark = tick(0.8)
        box.next_to(survey, LEFT, 0.4)
        mark.move_to(box)
        # "No plot can fix that."
        self.play(FadeIn(plot), run_time=self.share(0.15))
        self.play(Create(strike(plot)), run_time=self.share(0.15))
        # "The fix is a different survey."
        at(self, 0.5)
        self.play(FadeIn(survey, scale=0.9), FadeIn(box), run_time=self.share(0.2))
        self.play(Create(mark), run_time=self.share(0.1))
        self.finish()


MODEL_NAMES = {"mean only": "predict the mean", "linear regression": "linear regression",
               "negative binomial GLM, linear terms": "GLM, straight terms",
               "negative binomial GLM, correct form": "GLM, the right formula",
               "GAM with smooth terms": "GAM, smooth curves",
               "random forest": "random forest", "boosted trees": "boosted trees"}


class Scene23(VideoScene):
    number = 23

    def construct(self):
        scores = self.data("model-scores").sort_values("rmse").reset_index(drop=True)
        head = label("Cross-validated error (RMSE), same folds (lower is better)", 30, SUBDUED, weight=BOLD
                     ).to_edge(UP, buff=0.5)
        colours = [GREEN if m.startswith("GAM") else (BLUE if m == "random forest" else GREY) for m in scores["model"]]
        # Bars start at 3.5 so the differences are visible; the axis says so.
        base = 3.5
        rows = hbar_rows([MODEL_NAMES[m] for m in scores["model"]], scores["rmse"] - base, colours, 3.6,
                         x0=-0.4, top=2.2, step=0.78, texts=[f"{v:.2f}" for v in scores["rmse"]], size=30, height=0.5)
        start = label(f"bars start at {base}", 24, SUBDUED).next_to(rows, DOWN, 0.4).set_x(-0.4)
        gam = [i for i, m in enumerate(scores["model"]) if m.startswith("GAM")][0]
        forest = [i for i, m in enumerate(scores["model"]) if m == "random forest"][0]
        # "Now try a GAM, a model of smooth curves you can read."
        self.play(FadeIn(head), FadeIn(VGroup(*[r[0] for r in rows])), FadeIn(start), run_time=self.share(0.2))
        # "On the same folds, it was the most accurate of seven: ..."
        at(self, 0.4)
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                              lag_ratio=0.1), run_time=self.share(0.25))
        # "... 4.08, against the forest's 4.28."
        at(self, 0.72)
        self.play(Indicate(rows[gam], color=GREEN, scale_factor=1.06), run_time=self.share(0.1))
        self.play(Indicate(rows[forest], color=BLUE, scale_factor=1.06), run_time=self.share(0.1))
        self.finish()


def gam_layout(scene):
    frame_data = scene.data("gam-depth")
    x, fit, se, truth = (frame_data[k].to_numpy() for k in ("x", "fit", "se", "truth"))
    lo, hi = fit - 1.96 * se, fit + 1.96 * se
    axes, frame = chart([0, 200, 20], [-2.5, 1, 0.5], 7.4, 5.0, [0, 50, 100, 150, 200], [-2, -1, 0, 1],
                        "depth (m)", "effect on log count")
    frame.move_to([-2.4, -0.3, 0])
    band = ribbon(axes, x, lo, hi, BLUE, 0.2)
    fitted = polyline(axes, x, fit, BLUE, 7)
    true = polyline(axes, x, truth, GREEN, 6, dashed=True)
    peak = x[np.argmax(fit)]
    peak_line = DashedLine(axes.c2p(peak, -2.5), axes.c2p(peak, fit.max()), color=BLUE, stroke_width=3)
    peak_name = label(f"GAM's peak: {peak:.0f} m", 28, BLUE, weight=BOLD).next_to(axes.c2p(peak, -2.3), RIGHT, 0.15)
    names = VGroup(label("GAM, with its 95% interval", 28, BLUE, weight=BOLD),
                   label("truth", 28, GREEN, weight=BOLD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT
                                                                   ).to_corner(UR, buff=0.4)
    covered = int(np.sum((truth >= lo) & (truth <= hi)))
    return axes, frame, band, fitted, true, peak_line, peak_name, names, covered, len(x)


class Scene24(VideoScene):
    number = 24

    def construct(self):
        axes, frame, band, fitted, true, peak_line, peak_name, names, covered, n = gam_layout(self)
        self.play(FadeIn(frame), Create(true), FadeIn(names[1]), run_time=self.share(0.15))
        # "Its depth curve is wrong too, peaking at 52 metres."
        self.play(Create(fitted), FadeIn(names[0]), run_time=self.share(0.2))
        self.play(Create(peak_line), FadeIn(peak_name), run_time=self.share(0.15))
        # "But it comes with an interval."
        at(self, 0.62)
        self.play(FadeIn(band), run_time=self.share(0.2))
        self.finish()


class Scene25(VideoScene):
    number = 25

    def construct(self):
        axes, frame, band, fitted, true, peak_line, peak_name, names, covered, n = gam_layout(self)
        self.add(frame, band, true, fitted, peak_line, peak_name, names)
        count = VGroup(label("covers the truth at", 32, GREEN, weight=BOLD),
                       label(f"{covered} of {n} points", 40, GREEN, weight=BOLD)).arrange(DOWN, buff=0.15
                                                                                         ).move_to([4.4, 0.9, 0])
        wide = VGroup(label("a wide answer,", 36, BLUE, weight=BOLD), label("not a wrong one", 36, BLUE, weight=BOLD)
                      ).arrange(DOWN, buff=0.15).move_to([4.4, -1.0, 0])
        # "That interval covers the true curve at 197 of 200 points."
        self.play(Indicate(true, color=GREEN), FadeIn(count), run_time=self.share(0.3))
        # "It is not a wrong answer. It is a wide one."
        at(self, 0.6)
        self.play(FadeIn(wide, scale=0.9), run_time=self.share(0.15))
        self.finish()


class Scene26(VideoScene):
    number = 26

    def construct(self):
        gam = card("GAM", BLUE, 44).move_to([-3.4, 1.2, 0])
        says = label("\"I don't know\"", 44, BLUE, weight=BOLD).next_to(gam, DOWN, 0.6)
        pdp = card("partial dependence plot", SUBDUED, 40).move_to([3.0, 1.2, 0])
        silent = label("no way to say it", 40, VERMILION, weight=BOLD).next_to(pdp, DOWN, 0.6)
        # "The GAM says it does not know."
        self.play(FadeIn(gam), run_time=self.share(0.1))
        self.play(FadeIn(says, shift=0.2 * UP), run_time=self.share(0.2))
        # "A partial dependence plot has no way to say that."
        at(self, 0.45)
        self.play(FadeIn(pdp), run_time=self.share(0.1))
        self.play(FadeIn(silent, shift=0.2 * UP), run_time=self.share(0.2))
        self.finish()


class Scene27(KeyPointScene):
    number, point = 27, 2


# What no model can warn you about (scenes 28–37) --------------------------------------------

def intervals_layout(scene):
    bands = scene.data("interval-bands").sort_values("expected").reset_index(drop=True)
    table = scene.data("intervals").set_index("interval")
    axes, frame = chart([0, 17, 1], [0, 50, 10], 8.0, 5.4, [0, 4, 8, 12, 16], [0, 10, 20, 30, 40, 50],
                        "expected count from the GAM", "observed count")
    frame.move_to([-1.8, -0.3, 0])
    x = bands["expected"].to_numpy()
    mean_band = ribbon(axes, x, bands["mean_lower"].to_numpy(), bands["mean_upper"].to_numpy(), BLUE, 0.75)
    new_band = ribbon(axes, x, bands["new_lower"].to_numpy(), np.minimum(bands["new_upper"].to_numpy(), 50),
                      SKY, 0.3)
    dots = VGroup(*[Dot(axes.c2p(e, min(o, 50)), 0.06, color=INK, fill_opacity=0.6)
                    for e, o in zip(bands["expected"], bands["observed"])])
    return table, axes, frame, mean_band, new_band, dots


def coverage_note(table, key, name, colour, y):
    row = table.loc[key]
    return VGroup(label(name, 30, colour, weight=BOLD),
                  label(f"covers {percent(row['covers the observed count'])}", 36, colour, weight=BOLD),
                  label(f"mean width {row['mean width']:.1f}", 26, SUBDUED)
                  ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([4.6, y, 0], aligned_edge=LEFT).set_x(3.0,
                                                                                                          LEFT)


class Scene28(VideoScene):
    number = 28

    def construct(self):
        table, axes, frame, mean_band, new_band, dots = intervals_layout(self)
        head = label(f"{int(table['test'].iloc[0])} test stations", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.3)
        question = VGroup(label("two kinds of interval,", 32, INK, weight=BOLD),
                          label("two questions", 32, INK, weight=BOLD)).arrange(DOWN, buff=0.12).move_to([4.6, 0.5, 0])
        # "Every prediction needs an interval."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), run_time=self.share(0.3))
        # "But there are two kinds, and they answer different questions."
        at(self, 0.5)
        self.play(FadeIn(question), run_time=self.share(0.15))
        self.finish()


class Scene29(VideoScene):
    number = 29

    def construct(self):
        table, axes, frame, mean_band, new_band, dots = intervals_layout(self)
        self.add(frame, dots)
        note = coverage_note(table, "mean", "for the average count", BLUE, 1.6)
        # "The band a GAM gives you is for the average count."
        self.play(FadeIn(mean_band), FadeIn(note[0]), run_time=self.share(0.3))
        # "It covers 29% of the observed counts."
        at(self, 0.55)
        self.play(FadeIn(note[1:], shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene30(VideoScene):
    number = 30

    def construct(self):
        table, axes, frame, mean_band, new_band, dots = intervals_layout(self)
        mean_note = coverage_note(table, "mean", "for the average count", BLUE, 1.6)
        self.add(frame, mean_band, dots, mean_note)
        note = coverage_note(table, "new count", "for a new count", "#3C8DBF", -1.0)
        # "The interval for a new count is three times wider, ..."
        self.play(FadeIn(new_band), FadeIn(note[0]), FadeIn(note[2]), run_time=self.share(0.35))
        # "... and covers 99%."
        at(self, 0.65)
        self.play(FadeIn(note[1], shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def forest_coverage_layout(scene):
    table = scene.data("intervals").set_index("interval")
    head = label("A 95% interval for the random forest: share of test counts it covers", 28, SUBDUED,
                 weight=BOLD).to_edge(UP, buff=0.6)
    keys = ["in-sample rmse", "conformal"]
    names = ["from its training error", "conformal"]
    values = [table.loc[k, "covers the observed count"] for k in keys]
    rows = hbar_rows(names, values, [VERMILION, GREEN], 6.0, x0=-1.6, top=1.3, step=1.6,
                     texts=[percent(values[0]), percent(values[1], 1)], size=34)
    nominal_x = -1.6 + 6.0 * 0.95
    nominal = DashedLine([nominal_x, 2.2, 0], [nominal_x, -1.6, 0], color=INK, stroke_width=3)
    nominal_name = label("95%", 28, INK, weight=BOLD).next_to(nominal, UP, 0.1)
    return table, head, rows, nominal, nominal_name


class Scene31(VideoScene):
    number = 31

    def construct(self):
        table, head, rows, nominal, nominal_name = forest_coverage_layout(self)
        in_sample, held_out = table["in_sample_rmse"].iloc[0], table["held_out_rmse"].iloc[0]
        errors = VGroup(label(f"training error {in_sample:.2f}", 30, VERMILION, weight=BOLD),
                        label(f"honest error {held_out:.2f}", 30, INK, weight=BOLD)
                        ).arrange(RIGHT, buff=0.8).next_to(rows[0], DOWN, 0.45).set_x(0)
        # "A forest has no distribution."
        self.play(FadeIn(head), Create(nominal), FadeIn(nominal_name), run_time=self.share(0.15))
        # "Build its interval from the training error, and it covers 77%: ..."
        at(self, 0.25)
        self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]), run_time=self.share(0.25))
        # "... that error is 2.11, against an honest 4.17."
        at(self, 0.68)
        self.play(FadeIn(errors, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene32(VideoScene):
    number = 32

    def construct(self):
        table, head, rows, nominal, nominal_name = forest_coverage_layout(self)
        self.add(head, nominal, nominal_name, rows[0])
        lowest = table["lowest"].iloc[0]
        sized = label("sized on stations the model never saw", 30, GREEN, weight=BOLD).next_to(rows[1], DOWN, 0.4
                                                                                                ).set_x(0)
        # "Conformal prediction sizes the interval on stations the model never saw."
        self.play(FadeIn(rows[1][0]), FadeIn(sized), run_time=self.share(0.25))
        # "It covers 96.5%, whatever the model."
        at(self, 0.55)
        self.play(GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.25))
        self.finish()


class Scene33(VideoScene):
    number = 33

    def construct(self):
        shift = self.data("shift")
        rows_data = shift[shift["experiment"] == "chlorophyll"].set_index("evaluated on")
        head = label("Conformal 95% interval, calibrated on low chlorophyll", 30, SUBDUED, weight=BOLD
                     ).to_edge(UP, buff=0.6)
        values = [rows_data.loc["same conditions", "coverage"], rows_data.loc["shifted", "coverage"]]
        rows = hbar_rows(["used on low chlorophyll", "used on high chlorophyll"], values, [GREEN, VERMILION], 6.0,
                         x0=-1.2, top=1.3, step=1.6, texts=[percent(v) for v in values], size=34)
        nominal_x = -1.2 + 6.0 * 0.95
        nominal = DashedLine([nominal_x, 2.2, 0], [nominal_x, -0.9, 0], color=INK, stroke_width=3)
        nominal_name = label("95%", 28, INK, weight=BOLD).next_to(nominal, UP, 0.1)
        widths = [rows_data.loc[k, "width"] for k in ("same conditions", "shifted")]
        width = label(f"width {widths[0]:.1f} both times", 32, SUBDUED, weight=BOLD).move_to([0, -1.6, 0])
        warning = label("no warning", 40, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.7)
        # "But only for stations like those."
        self.play(FadeIn(head), Create(nominal), FadeIn(nominal_name), run_time=self.share(0.1))
        self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]), run_time=self.share(0.15))
        # "Calibrate it on low chlorophyll, use it on high, and it covers 86%."
        at(self, 0.3)
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.2))
        # "Same width. No warning."
        at(self, 0.72)
        self.play(FadeIn(width), run_time=self.share(0.1))
        self.play(FadeIn(warning, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene34(VideoScene):
    number = 34

    def construct(self):
        # Schematic: a patch of rock with animals on it; the grab brings up half.
        rng = np.random.default_rng(34)
        rocks = VGroup(*[Ellipse(width=w, height=w * 0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.7)
                         .move_to([x, -2.2 + 0.2 * rng.uniform(), 0])
                         for x, w in zip(np.linspace(-5.5, 5.5, 12), rng.uniform(0.8, 1.4, 12))])
        rock_name = label("rock", 34, SUBDUED, weight=BOLD).next_to(rocks, DOWN, 0.2)
        animals = VGroup(*[Dot([x, y, 0], 0.13, color=ORANGE)
                           for x, y in zip(rng.uniform(-5, 5, 16), rng.uniform(-1.7, -1.3, 16))])
        grab = RoundedRectangle(width=2.2, height=1.4, corner_radius=0.2, stroke_color=INK, stroke_width=5
                                ).move_to([0, 2.2, 0])
        rope = Line([0, 3.6, 0], grab.get_top(), color=INK, stroke_width=3)
        half = label("only half come up", 36, VERMILION, weight=BOLD).next_to(grab, RIGHT, 0.5)
        # "One last error."
        self.play(FadeIn(rocks), FadeIn(rock_name), FadeIn(animals), run_time=self.share(0.2))
        # "Suppose the gear catches only half the animals on rock."
        at(self, 0.3)
        self.play(FadeIn(grab), Create(rope), run_time=self.share(0.15))
        kept = animals[::2]
        self.play(*[d.animate.move_to(grab.get_center() + [rng.uniform(-0.7, 0.7), rng.uniform(-0.4, 0.4), 0])
                    for d in kept], animals[1::2].animate.set_opacity(0.25), run_time=self.share(0.25))
        self.play(FadeIn(half), run_time=self.share(0.1))
        self.finish()


def rock_layout(scene):
    bias = scene.data("rock-bias").set_index("dataset")
    as_recorded, biased = bias.loc["as recorded"], bias.loc["gear halves the catch on rock"]
    return as_recorded, biased


class Scene35(VideoScene):
    number = 35

    def construct(self):
        as_recorded, biased = rock_layout(self)
        fewer = [1 - np.exp(as_recorded["rock effect"]), 1 - np.exp(biased["rock effect"])]
        head = label("Estimated animals on rock, compared with gravel", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.8)
        rows = hbar_rows(["as recorded", "gear halves the catch"], fewer, [BLUE, VERMILION], 7.0, x0=-1.8, top=1.0,
                         step=1.6, texts=[f"{percent(v)} fewer" for v in fewer], size=34)
        # "The estimated rock effect more than doubles: from 38% fewer animals than gravel ..."
        self.play(FadeIn(head), FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]),
                  run_time=self.share(0.3))
        # "... to 69% fewer."
        at(self, 0.65)
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.2))
        self.finish()


class Scene36(VideoScene):
    number = 36

    def construct(self):
        as_recorded, biased = rock_layout(self)
        values = [as_recorded["CV RMSE"], biased["CV RMSE"]]
        head = label("Cross-validated error (RMSE; lower is better)", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.8)
        base = 3.9
        rows = hbar_rows(["as recorded", "gear halves the catch"], [v - base for v in values], [BLUE, VERMILION],
                         30.0, x0=-1.8, top=1.0, step=1.6, texts=[f"{v:.3f}" for v in values], size=34)
        start = label(f"bars start at {base}", 24, SUBDUED).next_to(rows, DOWN, 0.3).set_x(-1.8, LEFT)
        better = label("the biased model scores better", 38, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(head), FadeIn(start), FadeIn(rows[0]), run_time=self.share(0.2))
        # "And the cross-validated error improves, from 4.079 to 4.008."
        at(self, 0.4)
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.25))
        self.play(FadeIn(better, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene37(VideoScene):
    number = 37

    def construct(self):
        checks = VGroup()
        for text in ("cross-validation", "every metric", "every plot"):
            box, mark = tick(0.5)
            words = label(text, 34).next_to(box, RIGHT, 0.3)
            checks.add(VGroup(box, mark, words))
        checks.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([-3.6, 0.3, 0])
        for c in checks:
            c[1].move_to(c[0])
        passes = label("every check passes", 36, VERMILION, weight=BOLD).next_to(checks, UP, 0.5)
        defences = VGroup(card("calibrate the gear", GREEN, 36), card("an independent method", GREEN, 36)
                          ).arrange(DOWN, buff=0.4).move_to([3.4, -0.3, 0])
        outside = label("outside the model", 34, GREEN, weight=BOLD).next_to(defences, UP, 0.5)
        # "Validation compares the model with the data. When the data are biased, every check passes."
        self.play(FadeIn(VGroup(*[VGroup(c[0], c[2]) for c in checks])), run_time=self.share(0.15))
        at(self, 0.25)
        self.play(LaggedStart(*[Create(c[1]) for c in checks], lag_ratio=0.3), FadeIn(passes), run_time=self.share(0.2))
        # "The defences are outside the model: calibrate the gear, and use an independent method."
        at(self, 0.52)
        self.play(FadeIn(outside), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(d, shift=0.2 * LEFT) for d in defences], lag_ratio=0.5), run_time=self.share(0.3))
        self.finish()


class Scene38(KeyPointScene):
    number, point = 38, 3


# Quiz (scenes 39–40) -------------------------------------------------------------------------

class Scene39(QuizScene):
    number = 39
    question = ("Two columns carry exactly the same information:", "depth, recorded twice.",
                "What does permutation importance", "say about each?")


class Scene40(VideoScene):
    number = 40

    def construct(self):
        # Schematic: two identical columns; shuffle one and the model reads the other.
        rng = np.random.default_rng(40)
        shades = rng.uniform(0.15, 0.9, 7)

        def column(name, x):
            cells = VGroup(*[Square(0.42, stroke_width=0, fill_color=BLUE, fill_opacity=float(s)) for s in shades]
                           ).arrange(DOWN, buff=0.05).move_to([x, -0.4, 0])
            return VGroup(cells, label(name, 30, BLUE, weight=BOLD).next_to(cells, UP, 0.25))

        first, second = column("depth", -4.6), column("depth, again", -2.6)
        answer = label("Both near zero", 52, BLUE, weight=BOLD).to_edge(UP, buff=0.5)
        reads = label("the model reads the other", 32, INK, weight=BOLD).move_to([2.6, 0.4, 0])
        arrow = Arrow(second.get_right(), reads.get_left(), color=INK, stroke_width=5, buff=0.3)
        redundant = VGroup(label("low importance means", 34, INK, weight=BOLD),
                           label("redundant, not unimportant", 34, VERMILION, weight=BOLD)
                           ).arrange(DOWN, buff=0.12).move_to([2.6, -1.6, 0])
        order = [4, 0, 6, 2, 5, 1, 3]
        # "Both near zero."
        self.play(FadeIn(answer), FadeIn(first), FadeIn(second), run_time=self.share(0.2))
        # "Shuffle one, and the model reads the other."
        cells = first[0]
        targets = [c.get_center() for c in cells]
        self.play(*[cells[i].animate.move_to(targets[order[i]]) for i in range(len(cells))], run_time=self.share(0.15))
        self.play(GrowArrow(arrow), FadeIn(reads), run_time=self.share(0.15))
        # "Low importance means redundant, not unimportant."
        at(self, 0.6)
        self.play(FadeIn(redundant, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


# The recap (scenes 41–43) and the end card (scene 44) --------------------------------------

class Scene41(RecapScene):
    number, point = 41, 1


class Scene42(RecapScene):
    number, point = 42, 2


class Scene43(RecapScene):
    number, point = 43, 3


class Scene44(EndCardScene):
    number = 44
