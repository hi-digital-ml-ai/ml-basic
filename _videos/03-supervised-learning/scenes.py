"""Manim scenes for the supervised learning video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/03-supervised-learning
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is an overview of the section: a short tour of its seven pages. Scenes marked
"page results" read visuals/data/*.csv, which tools/figures-for-video.R writes from the
pages. The others are schematic: made-up shapes, never numbers that could pass for
survey results. The opening, key-point, recap, quiz and end-card scenes are shared
(mlbasic_video.py) and read PROMISES, ANSWERS and RECAP from here. Consecutive scenes
about one picture share a builder, so each starts where the previous one ended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["Models that add up their inputs",
            "Models made of yes-or-no questions",
            "How to choose between them"]
ANSWERS = ["Match the model to the outcome:\na count is never negative,\na probability needs a threshold",
           "Trees find shapes on their own;\ntheir size is chosen\non validation data",
           "Start from the question\nand the outcome, not the\nmost flexible method"]
RECAP = ["Match the model to the outcome",
         "Choose a tree's size on validation data",
         "Start from the question"]


class Scene01(LearnScene):
    number = 1
    times = (0.43, 0.62, 0.8)


def card(text, colour=PURPLE, size=40):
    words = label(text, size, colour, weight=BOLD)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def panel(heading, lines, colour, width=3.0, height=2.4, size=26):
    """A card in the diagrams' house style: pale fill, a coloured strip along the top."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color="#1b6a87",
                           stroke_width=3, fill_color="#f4f8fa", fill_opacity=1)
    strip = Rectangle(width=width, height=0.12, stroke_width=0, fill_color=colour, fill_opacity=1).align_to(box, UP)
    words = VGroup(label(heading, size + 6, INK, weight=BOLD),
                   *[label(t, size, SUBDUED) for t in lines]).arrange(DOWN, buff=0.15)
    return VGroup(box, strip, words.move_to(box))


def at(scene, fraction):
    """Wait until this fraction of the narration."""
    scene.wait(max(scene.share(fraction) - scene.time, 0.01))


def cue(scene, phrase):
    """Wait until the narration reaches this phrase, judged by its place in the text."""
    text = " ".join(scene.script.scenes[scene.number - 1].narration.split())
    start = text.find(phrase)
    if start < 0:
        raise ValueError(f"scene {scene.number}: {phrase!r} is not in the narration")
    at(scene, start / len(text))


class Chart:
    """Plain axes with their own tick labels and axis names, in the series style."""

    def __init__(self, x_range, y_range, x_length=10.5, y_length=5.0, x_ticks=(), y_ticks=(),
                 x_name="", y_name="", centre=(0.4, -0.5, 0), x_text=None, y_text=None):
        self.axes = Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                         tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})
        self.axes.move_to(centre)
        x_text = x_text or (lambda v: f"{v:g}")
        y_text = y_text or (lambda v: f"{v:g}")
        x0, y0 = x_range[0], y_range[0]
        self.ticks = VGroup(*[label(x_text(v), 24, SUBDUED).next_to(self.axes.c2p(v, y0), DOWN, 0.15)
                              for v in x_ticks],
                            *[label(y_text(v).replace("-", "−"), 24, SUBDUED).next_to(self.axes.c2p(x0, v), LEFT, 0.15)
                              for v in y_ticks])
        # Placed from the bottom and left edges, not the axis lines: the x axis sits at
        # y = 0, which is mid-chart when the range goes below zero.
        x_mid = (x_range[0] + x_range[1]) / 2
        self.x_name = label(x_name, 26, SUBDUED).next_to(self.axes.c2p(x_mid, y0), DOWN, 0.65)
        left_edge = min([t.get_left()[0] for t in self.ticks[len(x_ticks):]] + [self.axes.c2p(x0, y0)[0]])
        self.y_name = label(y_name, 26, SUBDUED).rotate(PI / 2)
        self.y_name.move_to([left_edge - 0.4, self.axes.get_center()[1], 0])
        self.frame = VGroup(self.axes, self.ticks, self.x_name, self.y_name)

    def p(self, x, y):
        return self.axes.c2p(x, y)

    def line(self, xs, ys, colour, width=6):
        return VMobject(color=colour, stroke_width=width).set_points_as_corners(
            [self.p(x, y) for x, y in zip(xs, ys)])

    def hline(self, y, colour=GREY, width=3):
        (x0, x1) = self.axes.x_range[:2]
        return Line(self.p(x0, y), self.p(x1, y), color=colour, stroke_width=width)

    def shade(self, x0, x1, colour=GREY, opacity=0.15):
        (y0, y1) = self.axes.y_range[:2]
        return Polygon(self.p(x0, y0), self.p(x1, y0), self.p(x1, y1), self.p(x0, y1),
                       stroke_width=0, fill_color=colour, fill_opacity=opacity)


def model_curve(chart, table, model, colour, width=6):
    rows = table[table["model"] == model]
    return chart.line(rows["temperature_c"], rows[".pred"], colour, width)


# Models that add up their inputs (scenes 2–13) ------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        # Schematic: a quantity on a number line, a category as two answers.
        head = label("start from the outcome", 44, INK, weight=BOLD).to_edge(UP, buff=0.6)
        line = NumberLine(x_range=[0, 10, 1], length=5.0, color=GRID, include_ticks=False, stroke_width=4)
        truth = Dot(line.n2p(6), 0.14, color=INK)
        near = Dot(line.n2p(5.4), 0.12, color=GREEN)
        far = Dot(line.n2p(9.2), 0.12, color=VERMILION)
        gap = DoubleArrow(truth.get_center() + 0.35 * DOWN, far.get_center() + 0.35 * DOWN, color=VERMILION,
                          stroke_width=4, buff=0, tip_length=0.18)
        quantity = VGroup(label("a quantity", 36, INK, weight=BOLD), VGroup(line, truth, near, far, gap),
                          label("a temperature, a count", 28, SUBDUED)).arrange(DOWN, buff=0.5)
        chips = VGroup(card("present", GREEN, 32), card("absent", GREY, 32)).arrange(RIGHT, buff=0.5)
        category = VGroup(label("a category", 36, INK, weight=BOLD), chips,
                          label("present or absent", 28, SUBDUED)).arrange(DOWN, buff=0.5)
        VGroup(quantity, category).arrange(RIGHT, buff=2.0).move_to([0, 0.1, 0])
        chips.set_y(quantity[1].get_y())
        category[2].set_y(quantity[2].get_y())
        names = [card("regression", BLUE, 38).next_to(quantity, DOWN, 0.6),
                 card("classification", ORANGE, 38).next_to(category, DOWN, 0.6)]
        names[1].set_y(names[0].get_y())
        # "Supervised learning starts from the outcome."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "A quantity, such as a temperature or a count, calls for regression."
        cue(self, "A quantity")
        self.play(FadeIn(quantity), run_time=self.share(0.12))
        cue(self, "calls for regression")
        self.play(FadeIn(names[0], shift=0.2 * UP), run_time=self.share(0.07))
        # "A category, such as present or absent, calls for classification."
        cue(self, "A category")
        self.play(FadeIn(category), run_time=self.share(0.12))
        cue(self, "calls for classification")
        self.play(FadeIn(names[1], shift=0.2 * UP), run_time=self.share(0.07))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        # Page results: regression-and-classification.qmd, the count's shape.
        hist = self.data("histogram")
        shape = self.data("count-shape").iloc[0]
        chart = Chart([-0.5, 40.5, 5], [0, 200, 50], 10.5, 4.6, x_ticks=range(0, 41, 10), y_ticks=(0, 100, 200),
                      x_name="animals caught at a station", y_name="stations", centre=(0.5, -0.6, 0))
        base = chart.p(0, 0)[1]
        bars = VGroup()
        for _, row in hist.iterrows():
            x, n = row["abundance"], row["n"]
            height = chart.p(0, n)[1] - base
            bar = Rectangle(width=chart.p(0.9, 0)[0] - chart.p(0, 0)[0], height=height, stroke_width=0,
                            fill_color=VERMILION if x == 0 else BLUE, fill_opacity=0.85)
            bars.add(bar.move_to([chart.p(x, 0)[0], base + height / 2, 0]))
        head = label("the count of one species at each station", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        zeros = label(f"{shape['zero_pct']:.1f}% caught nothing", 34, VERMILION, weight=BOLD)
        zeros.next_to(chart.p(1.5, 170), RIGHT, 0.1)
        spread = card(f"overdispersed: variance about {round(shape['count_var'] / shape['count_mean'])} times the mean", PURPLE, 28)
        spread.move_to(chart.p(24, 100))
        # "The survey's outcome is the count of one species at each station."
        self.play(FadeIn(head), FadeIn(chart.frame), run_time=self.share(0.12))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=self.share(0.2))
        # "22.5% of the stations caught nothing,"
        cue(self, "22.5%")
        self.play(Indicate(bars[0], color=VERMILION), FadeIn(zeros, shift=0.2 * RIGHT), run_time=self.share(0.12))
        # "and the counts vary about six times as much as their average."
        cue(self, "and the counts vary")
        self.play(FadeIn(spread, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def count_chart():
    return Chart([1.5, 16.5, 1], [-6, 7, 1], 10.5, 5.2, x_ticks=(2, 6, 10, 14), y_ticks=(-4, 0, 4),
                 x_name="temperature (°C)", y_name="predicted count", centre=(0.5, -0.45, 0))


def count_layout(scene):
    """The count-regression page's figure: three models across the survey's temperatures."""
    table = scene.data("count-curves")
    chart = count_chart()
    zero = chart.hline(0)
    zero_name = label("zero", 24, SUBDUED).next_to(chart.p(16.5, 0), RIGHT, 0.1)
    curves = {"line": model_curve(chart, table, "Linear regression", BLUE),
              "curve": model_curve(chart, table, "Polynomial regression", ORANGE),
              "poisson": model_curve(chart, table, "Poisson regression", VERMILION)}
    return table, chart, VGroup(zero, zero_name), curves


def curve_name(text, colour, point, direction=UP):
    return label(text, 30, colour, weight=BOLD).next_to(point, direction, 0.2)


class Scene04(VideoScene):
    number = 4

    def construct(self):
        # Page results: count-regression.qmd#fig-shapes, linear regression.
        table, chart, zero, curves = count_layout(self)
        name = curve_name("linear regression: one slope", BLUE, chart.p(10.5, 4.6))
        # "Linear regression predicts a starting value plus a fixed amount for each input."
        self.play(FadeIn(chart.frame), FadeIn(zero), run_time=self.share(0.15))
        # "Against temperature, that is one slope, the same in cold water and warm."
        cue(self, "Against temperature")
        self.play(Create(curves["line"]), run_time=self.share(0.2))
        self.play(FadeIn(name), run_time=self.share(0.1))
        self.finish()


def optimum_marker(scene, chart, table):
    optimum = scene.data("optimum").iloc[0]["optimum"]
    rows = table[table["model"] == "Polynomial regression"]
    peak = rows[".pred"].max()
    dot = Dot(chart.p(optimum, peak), 0.12, color=ORANGE)
    words = label(f"peak at {optimum:.1f} °C", 30, ORANGE, weight=BOLD).next_to(dot, UP, 0.25)
    return VGroup(dot, words)


class Scene05(VideoScene):
    number = 5

    def construct(self):
        # Page results: linear-and-polynomial-regression.qmd, the curve and its peak.
        table, chart, zero, curves = count_layout(self)
        self.add(chart.frame, zero, curves["line"])
        name = curve_name("polynomial regression", ORANGE, chart.p(3.4, -3.0), RIGHT)
        peak = optimum_marker(self, chart, table)
        # "Add the square of temperature as one more column, and the line bends into a curve."
        self.play(curves["line"].animate.set_stroke(opacity=0.5), run_time=self.share(0.05))
        cue(self, "and the line bends")
        self.play(TransformFromCopy(curves["line"], curves["curve"]), run_time=self.share(0.2))
        # "This is polynomial regression, and it finds a peak at 7.5 degrees."
        cue(self, "This is polynomial")
        self.play(FadeIn(name), run_time=self.share(0.08))
        cue(self, "and it finds a peak")
        self.play(FadeIn(peak, scale=0.8), run_time=self.share(0.1))
        self.finish()


def below_zero(chart, table):
    rows = table[(table["model"] == "Polynomial regression") & (table["temperature_c"] > 8)]
    rows = rows[rows[".pred"] < 0]
    xs, ys = list(rows["temperature_c"]), list(rows[".pred"])
    return Polygon(*[chart.p(x, y) for x, y in zip(xs, ys)], chart.p(xs[-1], 0), chart.p(xs[0], 0),
                   stroke_width=0, fill_color=VERMILION, fill_opacity=0.35)


class Scene06(VideoScene):
    number = 6

    def construct(self):
        # Page results: linear-and-polynomial-regression.qmd, negative predictions.
        table, chart, zero, curves = count_layout(self)
        curves["line"].set_stroke(opacity=0.5)
        self.add(chart.frame, zero, curves["line"], curves["curve"], optimum_marker(self, chart, table))
        scores = self.data("line-curve-scores").set_index("model")
        stations = int(self.data("optimum").iloc[0]["test_stations"])
        area = below_zero(chart, table)
        words = label("fewer than zero animals", 32, VERMILION, weight=BOLD).next_to(chart.p(12.2, -2.2), LEFT, 0.3)
        count = card(f"at {int(scores.loc['Polynomial regression', 'below_zero'])} of the {stations} test stations", VERMILION, 30)
        count.move_to([3.4, 2.9, 0])
        # "But nothing in linear regression knows that a count stops at zero."
        self.play(Indicate(zero[0], color=INK), run_time=self.share(0.15))
        # "In warm water the curve falls below it,"
        cue(self, "In warm water")
        self.play(FadeIn(area), FadeIn(words), run_time=self.share(0.12))
        # "and it predicts fewer than zero animals at 12 of the 202 test stations."
        cue(self, "at 12")
        self.play(FadeIn(count, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        # Page results: count-regression.qmd#fig-shapes, Poisson regression added.
        table, chart, zero, curves = count_layout(self)
        curves["line"].set_stroke(opacity=0.5)
        self.add(chart.frame, zero, curves["line"], curves["curve"])
        name = curve_name("Poisson regression", VERMILION, chart.p(12.8, 1.9), UP)
        never = card("close to zero, never below", VERMILION, 30).move_to([3.4, 2.9, 0])
        # "Poisson regression predicts the logarithm of the count instead."
        self.play(curves["line"].animate.set_stroke(opacity=0.25), curves["curve"].animate.set_stroke(opacity=0.35),
                  run_time=self.share(0.08))
        self.play(Create(curves["poisson"]), run_time=self.share(0.25))
        self.play(FadeIn(name), run_time=self.share(0.08))
        # "Turned back into a count, a prediction can come close to zero, but never cross it."
        cue(self, "a prediction can come")
        self.play(FadeIn(never, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


SUBSTRATE_ROWS = [("sand", None), ("mud", "substrate: mud"), ("rock", "substrate: rock")]


def multiplier_layout(scene):
    table = scene.data("multipliers")
    chart = Chart([0.5, 2.0, 0.25], [0, 3, 1], 9.0, 3.6, x_ticks=(0.5, 1, 1.5, 2), x_name="multiplier on the count",
                  centre=(1.0, -0.2, 0))
    one = DashedLine(chart.p(1, 0), chart.p(1, 3), color=GREY, stroke_width=3)
    rows = {}
    for i, (name, term) in enumerate(SUBSTRATE_ROWS):
        y = 2.5 - i
        words = label(name, 34, INK, weight=BOLD).next_to(chart.p(0.5, y), LEFT, 0.4)
        marks = {}
        for fit, colour in [("poisson", VERMILION), ("negbin", PURPLE)]:
            if term is None:
                marks[fit] = VGroup(Dot(chart.p(1, y), 0.12, color=GREY))
                continue
            r = table[(table["fit"] == fit) & (table["term"] == term)].iloc[0]
            marks[fit] = VGroup(Line(chart.p(r["conf_low"], y), chart.p(r["conf_high"], y), color=colour,
                                     stroke_width=7),
                                Dot(chart.p(r["multiplier"], y), 0.13, color=colour))
        rows[name] = (words, marks)
    return table, chart, one, rows


class Scene08(VideoScene):
    number = 8

    def construct(self):
        # Page results: count-regression.qmd, the Poisson multipliers.
        table, chart, one, rows = multiplier_layout(self)
        head = label("each seabed type against sand", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        mud = table[(table["fit"] == "poisson") & (table["term"] == "substrate: mud")].iloc[0]
        times = label(f"× {mud['multiplier']:.2f}", 34, VERMILION, weight=BOLD)
        times.next_to(rows["mud"][1]["poisson"], UP, 0.15)
        base = label("baseline", 26, SUBDUED).next_to(rows["sand"][1]["poisson"], RIGHT, 0.25)
        # "Its coefficients become multipliers."
        self.play(FadeIn(head), FadeIn(VGroup(chart.axes.x_axis, chart.ticks, chart.x_name)), Create(one),
                  run_time=self.share(0.15))
        self.play(FadeIn(rows["sand"][0]), FadeIn(rows["sand"][1]["poisson"]), FadeIn(base), run_time=self.share(0.1))
        # "With everything else held fixed, a muddy station is expected to hold 1.34 times the count of a sandy one."
        cue(self, "a muddy station")
        self.play(FadeIn(rows["mud"][0]), FadeIn(rows["mud"][1]["poisson"]), run_time=self.share(0.1))
        cue(self, "1.34")
        self.play(FadeIn(times, shift=0.1 * UP), run_time=self.share(0.08))
        self.play(FadeIn(rows["rock"][0]), FadeIn(rows["rock"][1]["poisson"]), run_time=self.share(0.1))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        # Page results: count-regression.qmd, the spread ratio and the negative binomial's intervals.
        table, chart, one, rows = multiplier_layout(self)
        head = label("each seabed type against sand", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        base = label("baseline", 26, SUBDUED).next_to(rows["sand"][1]["poisson"], RIGHT, 0.25)
        self.add(head, chart.axes.x_axis, chart.ticks, chart.x_name, one, base,
                 *[VGroup(w, m["poisson"]) for w, m in rows.values()])
        ratio = self.data("spread").iloc[0]["spread_ratio"]
        spread = card(f"overdispersed: {ratio:.1f} times the spread Poisson expects", VERMILION, 30)
        spread.move_to(head)
        # The negative binomial's intervals sit just below Poisson's, so the two can be compared.
        for name in ("mud", "rock"):
            rows[name][1]["negbin"].shift(0.3 * DOWN)
        narrow = label("Poisson: too narrow", 28, VERMILION, weight=BOLD)
        wide = label("negative binomial: wider", 28, PURPLE, weight=BOLD)
        key = VGroup(narrow, wide).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.35)
        ring = SurroundingRectangle(VGroup(rows["rock"][1]["negbin"], one), color=PURPLE, buff=0.12, corner_radius=0.1)
        rock = label("rock: no longer told apart from sand", 28, PURPLE, weight=BOLD).next_to(ring, UP, 0.12)
        rock.set_x(ring.get_x())
        # "But Poisson assumes the counts vary only as much as their average. Even after the inputs
        # are taken into account, they vary 3.7 times as much: the counts are overdispersed,"
        cue(self, "Even after")
        self.play(ReplacementTransform(head, spread), run_time=self.share(0.08))
        # "so Poisson's intervals are too narrow."
        cue(self, "so Poisson's")
        self.play(FadeIn(narrow), *[Indicate(rows[n][1]["poisson"][0], color=VERMILION) for n in ("mud", "rock")],
                  run_time=self.share(0.08))
        # "The negative binomial model allows for the extra spread. Its intervals are wider,"
        cue(self, "The negative binomial")
        self.play(FadeIn(wide), run_time=self.share(0.06))
        cue(self, "Its intervals are wider")
        self.play(*[TransformFromCopy(rows[n][1]["poisson"], rows[n][1]["negbin"]) for n in ("mud", "rock")],
                  run_time=self.share(0.1))
        # "and rock can no longer be told apart from sand."
        cue(self, "and rock")
        self.play(Create(ring), FadeIn(rock), run_time=self.share(0.08))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        # Page results: logistic-regression.qmd#fig-curve.
        curve = self.data("logistic-curve")
        points = self.data("logistic-points").dropna()
        chart = Chart([1.5, 16.5, 1], [-0.08, 1.08, 0.5], 10.5, 5.0, x_ticks=(2, 6, 10, 14), y_ticks=(0, 0.5, 1),
                      x_name="temperature (°C)", y_name="probability of presence", centre=(0.5, -0.45, 0))
        rng = np.random.default_rng(10)
        dots = VGroup(*[Dot(chart.p(t, p + rng.uniform(-0.03, 0.03)), 0.045, color=GREY, fill_opacity=0.45)
                        for t, p in zip(points["temperature_c"], points["present"])])
        edges = VGroup(DashedLine(chart.p(1.5, 0), chart.p(16.5, 0), color=GREY),
                       DashedLine(chart.p(1.5, 1), chart.p(16.5, 1), color=GREY))
        line = chart.line(curve["temperature_c"], curve[".pred_yes"], VERMILION)
        present = label("present", 24, SUBDUED).next_to(chart.p(16.5, 1), RIGHT, 0.15)
        absent = label("absent", 24, SUBDUED).next_to(chart.p(16.5, 0), RIGHT, 0.15)
        head = label("logistic regression", 40, VERMILION, weight=BOLD).to_edge(UP, buff=0.4)
        stays = card("always between 0 and 1", VERMILION, 30).move_to(chart.p(9, 0.3))
        # "For present or absent, logistic regression uses the same design to predict a probability,"
        self.play(FadeIn(chart.frame), FadeIn(edges), FadeIn(dots), FadeIn(present), FadeIn(absent),
                  run_time=self.share(0.15))
        cue(self, "logistic regression")
        self.play(FadeIn(head), Create(line), run_time=self.share(0.3))
        # "which always stays between zero and one."
        cue(self, "which always")
        self.play(Indicate(edges, color=INK), FadeIn(stays, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        # Schematic: the two ways a present-or-absent answer can be wrong.
        head = label("from a probability to present or absent", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        chips = VGroup(card("probability", GREY, 30), card("present", GREEN, 30), card("absent", GREY, 30))
        arrow = Arrow(LEFT, RIGHT, color=INK, stroke_width=5)
        threshold = label("threshold", 26, SUBDUED)
        answers = VGroup(chips[1], chips[2]).arrange(DOWN, buff=0.25)
        flow = VGroup(chips[0], VGroup(arrow, threshold).arrange(DOWN, buff=0.1), answers).arrange(RIGHT, buff=0.4)
        flow.next_to(head, DOWN, 0.5)

        def mistake(name, said, truth, colour):
            return panel(name, [f"said: {said}", f"truly: {truth}"], colour, 4.6, 2.2, 30)

        alarm = mistake("a false alarm", "present", "absent", ORANGE)
        miss = mistake("a miss", "absent", "present", BLUE)
        VGroup(alarm, miss).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.6)
        two = label("two ways to be wrong", 30, SUBDUED, weight=BOLD).next_to(VGroup(alarm, miss), UP, 0.25)
        # "A threshold turns the probability into an answer: present or absent."
        self.play(FadeIn(head), FadeIn(chips[0]), run_time=self.share(0.1))
        cue(self, "into an answer")
        self.play(GrowArrow(arrow), FadeIn(threshold), FadeIn(answers, shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "The answer can be wrong in two ways."
        cue(self, "The answer can")
        self.play(FadeIn(two), run_time=self.share(0.06))
        # "A false alarm says present where the species was absent."
        cue(self, "A false alarm")
        self.play(FadeIn(alarm, shift=0.2 * UP), run_time=self.share(0.1))
        # "A miss says absent where it was present."
        cue(self, "A miss")
        self.play(FadeIn(miss, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        # Page results: logistic-regression.qmd, the thresholds table.
        table = self.data("thresholds").set_index("threshold")
        head = label("false alarms and misses on the test sites", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        top = 100
        chart = Chart([0, 2, 1], [0, top, 50], 8.0, 3.8, centre=(0, -0.6, 0))
        base = chart.p(0, 0)[1]
        groups = VGroup()
        for i, cut in enumerate([0.5, 0.9]):
            bars = VGroup()
            for dx, column, colour in [(-0.45, "false_alarms", ORANGE), (0.45, "misses", BLUE)]:
                n = int(table.loc[cut, column])
                height = max(chart.p(0, n)[1] - base, 0.02)
                bar = Rectangle(width=0.8, height=height, stroke_width=0, fill_color=colour, fill_opacity=0.85)
                bar.move_to([chart.p(i + 0.5, 0)[0] + dx, base + height / 2, 0])
                bars.add(VGroup(bar, label(str(n), 34, INK, weight=BOLD).next_to(bar, UP, 0.12)))
            name = label(f"threshold {cut:g}", 32, INK, weight=BOLD).next_to(chart.p(i + 0.5, 0), DOWN, 0.3)
            groups.add(VGroup(bars, name))
        key = VGroup(VGroup(Square(0.3, stroke_width=0, fill_color=ORANGE, fill_opacity=0.85),
                            label("false alarms: said present, truly absent", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.3, stroke_width=0, fill_color=BLUE, fill_opacity=0.85),
                            label("misses: said absent, truly present", 26, SUBDUED)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6)
        key.next_to(head, DOWN, 0.35)
        cost = card("what does each mistake cost?", PURPLE, 36).move_to(head)
        self.play(FadeIn(head), Create(chart.axes.x_axis), FadeIn(key), run_time=self.share(0.06))
        # "At a threshold of 0.5, the model gives 34 false alarms and 4 misses."
        self.play(FadeIn(groups[0][1]), GrowFromEdge(groups[0][0][0][0], DOWN), FadeIn(groups[0][0][0][1]),
                  run_time=self.share(0.08))
        cue(self, "and 4 misses")
        self.play(GrowFromEdge(groups[0][0][1][0], DOWN), FadeIn(groups[0][0][1][1]), run_time=self.share(0.06))
        # "Raise it to 0.9, and the false alarms fall to 6,"
        cue(self, "Raise it")
        self.play(FadeIn(groups[1][1]), GrowFromEdge(groups[1][0][0][0], DOWN), FadeIn(groups[1][0][0][1]),
                  run_time=self.share(0.06))
        # "but the misses rise to 97."
        cue(self, "but the misses")
        self.play(GrowFromEdge(groups[1][0][1][0], DOWN), FadeIn(groups[1][0][1][1]), run_time=self.share(0.06))
        # "The right threshold depends on what each mistake costs."
        cue(self, "The right threshold")
        self.play(ReplacementTransform(head, cost), run_time=self.share(0.08))
        self.finish()


class Scene13(KeyPointScene):
    number, point = 13, 1


# Models made of questions (scenes 14–23) ------------------------------------------------

def tree_layout(scene):
    """The decision-trees page's depth-3 tree, its top questions drawn as boxes.

    The two grey boxes, above 5.7 chlorophyll and below 6.4 °C, each ask one more
    question on the page; the video shows their averages and marks them "…".
    """
    nodes = scene.data("tree-nodes").set_index("node")

    def question(text):
        return panel(text, [], BLUE, 4.0, 0.8, 26)

    def leaf(n, colour=GREY, more=False):
        box = RoundedRectangle(width=1.9, height=0.8, corner_radius=0.12, stroke_width=0, fill_color=colour,
                               fill_opacity=0.3)
        words = label(f"{nodes.loc[n, 'yval']:.1f}", 32, INK, weight=BOLD).move_to(box)
        group = VGroup(box, words)
        if more:
            group.add(label("…", 30, SUBDUED).next_to(box, DOWN, 0.05))
        return group

    q1 = question(f"chlorophyll < {nodes.loc[2, 'cut']:.1f}?").move_to([0, 2.7, 0])
    q2 = question(f"temperature < {nodes.loc[4, 'cut']:.1f}?").move_to([-2.4, 1.3, 0])
    rich = leaf(3, more=True).move_to([3.6, 1.3, 0])
    cold = leaf(4, more=True).move_to([-4.8, -0.1, 0])
    q3 = question(f"temperature ≥ {nodes.loc[10, 'cut']:.1f}?").move_to([0.0, -0.1, 0])
    warm = leaf(10, GREEN).move_to([1.4, -1.5, 0])
    band = leaf(11, GREEN).move_to([-1.4, -1.5, 0])
    edges = VGroup()
    names = VGroup()
    for parent, child, word in [(q1, q2, "yes"), (q1, rich, "no"), (q2, cold, "yes"), (q2, q3, "no"),
                                (q3, warm, "yes"), (q3, band, "no")]:
        edge = Line(parent.get_bottom(), child.get_top(), color=GREY, stroke_width=3)
        edges.add(edge)
        # A small tag on the branch, as rpart.plot draws them: the line meets the tag and
        # never crosses the word.
        word_mob = label(word, 24, SUBDUED)
        tag = RoundedRectangle(width=word_mob.width + 0.24, height=word_mob.height + 0.16, corner_radius=0.08,
                               stroke_color=GREY, stroke_width=2, fill_color=BACKGROUND, fill_opacity=1)
        names.add(VGroup(tag, word_mob).move_to(edge.point_from_proportion(0.5)))
    stations = label(f"{int(nodes.loc[3, 'n'])} stations", 22, SUBDUED).next_to(rich, RIGHT, 0.15)
    levels = [VGroup(q1), VGroup(edges[0:2], names[0:2], q2, rich, stations),
              VGroup(edges[2:4], names[2:4], cold, q3), VGroup(edges[4:6], names[4:6], warm, band)]
    return nodes, levels, (q2, q3, cold, band, warm)


class Scene14(VideoScene):
    number = 14

    def construct(self):
        # Page results: decision-trees.qmd#fig-tree, the top of the depth-3 tree.
        nodes, levels, _ = tree_layout(self)
        name = label("a decision tree", 44, GREEN, weight=BOLD).to_corner(UL, buff=0.6)
        note = label("each leaf: the average count of its stations", 30, SUBDUED).to_edge(DOWN, buff=0.5)
        # "A decision tree works differently. It asks yes-or-no questions about the inputs,"
        self.play(FadeIn(name, shift=0.2 * RIGHT), FadeIn(levels[0], shift=0.2 * DOWN), run_time=self.share(0.1))
        cue(self, "It asks")
        for level in levels[1:]:
            self.play(FadeIn(level, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "and each leaf predicts the average of the stations that reach it."
        cue(self, "and each leaf")
        self.play(FadeIn(note), run_time=self.share(0.1))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Page results: decision-trees.qmd, the temperature band.
        nodes, levels, (q2, q3, cold, band, warm) = tree_layout(self)
        self.add(label("a decision tree", 44, GREEN, weight=BOLD).to_corner(UL, buff=0.6), *levels)
        low, high = nodes.loc[4, "cut"], nodes.loc[10, "cut"]
        chart = Chart([1.5, 16.5, 1], [0, 6, 1], 9.0, 1.3, x_ticks=(low, high), centre=(0.8, -2.8, 0),
                      x_text=lambda v: f"{v:.1f} °C")
        steps = VGroup()
        for x0, x1, n, colour in [(1.5, low, 4, GREY), (low, high, 11, GREEN), (high, 16.5, 10, GREY)]:
            y = nodes.loc[n, "yval"]
            steps.add(Line(chart.p(x0, y), chart.p(x1, y), color=colour, stroke_width=8))
        risers = VGroup(DashedLine(chart.p(low, 0), chart.p(low, 6), color=BLUE),
                        DashedLine(chart.p(high, 0), chart.p(high, 6), color=BLUE))
        peak = label("one question for each side", 28, BLUE, weight=BOLD).move_to([-4.7, -1.95, 0])
        # "On the survey, two questions about temperature find a band, from 6.4 to 10.4 degrees,"
        cue(self, "two questions")
        self.play(Indicate(q2, color=BLUE), Indicate(q3, color=BLUE), run_time=self.share(0.15))
        cue(self, "find a band")
        self.play(FadeIn(chart.axes.x_axis), FadeIn(chart.ticks), Create(steps), run_time=self.share(0.15))
        # "with the most animals."
        cue(self, "with the most")
        self.play(Indicate(band, color=GREEN), Indicate(steps[1], color=GREEN), run_time=self.share(0.1))
        # "A peak takes one question for each side."
        cue(self, "A peak")
        self.play(Create(risers), FadeIn(peak), run_time=self.share(0.1))
        self.finish()


def step_chart(x_max=20, y_max=6.5, y_ticks=(0, 2, 4, 6)):
    return Chart([0, x_max, 1], [0, y_max, 1], 10.5, 5.0, x_ticks=range(0, x_max + 1, 5), y_ticks=y_ticks,
                 x_name="temperature (°C)", y_name="predicted count", centre=(0.5, -0.45, 0))


class Scene16(VideoScene):
    number = 16

    def construct(self):
        # Page results: decision-trees.qmd#fig-steps.
        table = self.data("tree-steps")
        span = self.data("tree-range").iloc[0]
        chart = step_chart()
        shades = VGroup(chart.shade(0, span["low"]), chart.shade(span["high"], 20))
        beyond = label("beyond the data", 24, SUBDUED).move_to(chart.p(18, 6.1))
        poisson = model_curve(chart, table, "Poisson regression", VERMILION, 5).set_stroke(opacity=0.6)
        tree = model_curve(chart, table, "Decision tree", GREEN, 7)
        names = VGroup(label("decision tree", 30, GREEN, weight=BOLD).next_to(chart.p(9, 5.3), UP, 0.15),
                       label("Poisson regression", 26, VERMILION).next_to(chart.p(0.3, 5.9), RIGHT, 0))
        level = card("stays level", GREEN, 30).next_to(chart.p(18, 2.6), UP, 0.3)
        # "Its predictions come in steps."
        self.play(FadeIn(chart.frame), FadeIn(shades), FadeIn(beyond), FadeIn(poisson), FadeIn(names[1]),
                  run_time=self.share(0.12))
        self.play(Create(tree), FadeIn(names[0]), run_time=self.share(0.25))
        # "And beyond the warmest station it has seen, a tree stays level: it has no rule for going further."
        cue(self, "a tree stays level")
        self.play(Indicate(shades[1], color=GREEN), FadeIn(level, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        # Page results: decision-trees.qmd#fig-depth.
        depths = self.data("depths")
        best = int(depths.loc[depths["validation"].idxmin(), "depth"])
        chart = Chart([0.5, 15.5, 1], [0, 5.5, 1], 10.5, 5.0, x_ticks=(1, 5, 10, 15), y_ticks=(0, 2, 4),
                      x_name="tree depth", y_name="error (RMSE)", centre=(0.5, -0.45, 0))
        train = chart.line(depths["depth"], depths["training"], BLUE)
        valid = chart.line(depths["depth"], depths["validation"], ORANGE)
        names = VGroup(label("stations it was fitted to", 28, BLUE, weight=BOLD).move_to(chart.p(13, 2.9)),
                       label("validation sites", 28, ORANGE, weight=BOLD).next_to(chart.p(13, 4.6), DOWN, 0.1))
        mark = DashedLine(chart.p(best, 0), chart.p(best, 5.5), color=GREY, stroke_width=4)
        lowest = label(f"lowest at depth {best}", 30, ORANGE, weight=BOLD).next_to(chart.p(best, 5.2), RIGHT, 0.2)
        rule = card("choose the depth on the validation sites", PURPLE, 26).move_to(chart.p(4.3, 0.7))
        # "A deeper tree fits the stations it learned from ever more closely."
        self.play(FadeIn(chart.frame), run_time=self.share(0.1))
        self.play(Create(train), FadeIn(names[0]), run_time=self.share(0.18))
        # "On the validation sites, which were held back from fitting, the error is lowest at depth 5, then climbs."
        cue(self, "On the validation")
        self.play(Create(valid), FadeIn(names[1]), run_time=self.share(0.18))
        cue(self, "lowest at depth")
        self.play(Create(mark), FadeIn(lowest), run_time=self.share(0.08))
        # "So the depth is chosen on the validation sites."
        cue(self, "So the depth")
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        # Page results: forests-and-boosting.qmd, the first question of six resampled trees.
        values = list(self.data("first-questions")["threshold"])
        head = label("the first question of six resampled trees", 40, INK, weight=BOLD)
        head.to_edge(UP, buff=0.6)
        chips = VGroup(*[card(f"chlorophyll < {v:g}", BLUE, 26) for v in values]).arrange_in_grid(2, 3, buff=(0.4, 0.35))
        chips.next_to(head, DOWN, 0.5)
        line = NumberLine(x_range=[0, 14, 2], length=11, color=GRID, include_numbers=False, stroke_width=4)
        line.move_to([0, -2.3, 0])
        ticks = VGroup(*[label(f"{v}", 24, SUBDUED).next_to(line.n2p(v), DOWN, 0.2) for v in range(0, 15, 2)])
        name = label("chlorophyll threshold", 26, SUBDUED).next_to(ticks, DOWN, 0.15)
        marks = VGroup(*[Triangle(color=BLUE, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI)
                         .next_to(line.n2p(v), UP, 0.05) for v in values])
        span = BraceBetweenPoints(line.n2p(min(values)) + 0.5 * UP, line.n2p(max(values)) + 0.5 * UP, UP, color=VERMILION)
        span_name = label(f"from {min(values):g} to {max(values):g}", 32, VERMILION, weight=BOLD).next_to(span, UP, 0.1)
        # "One tree is also unstable. Grow it on six resamples of the same stations,"
        self.play(FadeIn(head), run_time=self.share(0.1))
        cue(self, "Grow it")
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.2), run_time=self.share(0.2))
        # "and the first question is always about chlorophyll, but its threshold moves from 2.57 to 12.6."
        cue(self, "but its threshold")
        self.play(FadeIn(line), FadeIn(ticks), FadeIn(name), *[TransformFromCopy(c, m) for c, m in zip(chips, marks)],
                  run_time=self.share(0.12))
        self.play(GrowFromCenter(span), FadeIn(span_name), run_time=self.share(0.1))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        # Page results: forests-and-boosting.qmd#fig-average, thirty trees and the forest.
        trees = self.data("forest-trees")
        forest = self.data("forest-average")
        span = self.data("tree-range").iloc[0]
        chart = step_chart(20, 18.5, (0, 5, 10, 15))
        shades = VGroup(chart.shade(0, span["low"]), chart.shade(span["high"], 20))
        thin = VGroup(*[chart.line(g["temperature_c"], g[".pred"], ORANGE, 2.5).set_stroke(opacity=0.35)
                        for _, g in trees.groupby("tree")])
        average = chart.line(forest["temperature_c"], forest[".pred"], VERMILION, 9)
        names = VGroup(label("30 of its trees", 30, ORANGE, weight=BOLD).next_to(chart.p(13, 16), RIGHT, 0.1),
                       card("the forest: their average", VERMILION, 28).move_to(chart.p(15.5, 9)))
        # "A random forest grows hundreds of trees, each on a resampled copy of the data,"
        self.play(FadeIn(chart.frame), FadeIn(shades), run_time=self.share(0.08))
        self.play(LaggedStart(*[Create(t) for t in thin], lag_ratio=0.08), FadeIn(names[0]), run_time=self.share(0.35))
        # "and averages them. The big jumps shrink into small steps."
        cue(self, "and averages")
        self.play(thin.animate.set_stroke(opacity=0.18), Create(average), FadeIn(names[1]), run_time=self.share(0.2))
        self.finish()


def small_tree(colour=GREEN, scale=1.0):
    top = Dot([0, 0.35, 0], 0.1, color=colour)
    left, right = Dot([-0.35, -0.25, 0], 0.1, color=colour), Dot([0.35, -0.25, 0], 0.1, color=colour)
    return VGroup(Line(top.get_center(), left.get_center(), color=colour, stroke_width=4),
                  Line(top.get_center(), right.get_center(), color=colour, stroke_width=4), top, left, right).scale(scale)


class Scene20(VideoScene):
    number = 20

    def construct(self):
        # Schematic: small trees in sequence, each fitted to the errors left before it.
        head = label("boosting: small trees, one after another", 40, INK, weight=BOLD).to_edge(UP, buff=0.7)
        start = panel("start", ["the average"], GREY, 2.4, 1.4, 24)
        boxes = [start] + [VGroup(RoundedRectangle(width=1.6, height=1.4, corner_radius=0.15, stroke_color="#1b6a87",
                                                   stroke_width=3, fill_color="#f4f8fa", fill_opacity=1),
                                  small_tree(GREEN, 1.3)) for _ in range(3)]
        row = VGroup(*boxes).arrange(RIGHT, buff=1.4).move_to([0, 0.3, 0])
        for b in boxes[1:]:
            b[1].move_to(b[0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), color=VERMILION, stroke_width=5, buff=0.1)
                          for a, b in zip(boxes[:-1], boxes[1:])])
        errors = VGroup(*[label("errors", 24, VERMILION, weight=BOLD).next_to(a, UP, 0.1) for a in arrows])
        total = card("prediction = the sum of all the trees", PURPLE, 32).to_edge(DOWN, buff=0.9)
        # "Boosting adds small trees one after another."
        self.play(FadeIn(head), FadeIn(start), run_time=self.share(0.12))
        # "Each new tree is fitted to the errors left by the trees before it."
        cue(self, "Each new tree")
        for arrow, words, box in zip(arrows, errors, boxes[1:]):
            self.play(GrowArrow(arrow), FadeIn(words), FadeIn(box, shift=0.2 * RIGHT), run_time=self.share(0.12))
        self.play(FadeIn(total, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        # Page results: forests-and-boosting.qmd#fig-trees, validation error by number of trees.
        scores = self.data("tree-counts")
        chart = Chart([0, np.log10(1600), 1], [3.5, 4.7, 0.5], 10.5, 5.0, x_ticks=(0, 1, 2, 3), y_ticks=(3.5, 4, 4.5),
                      x_name="number of trees", y_name="error on validation sites (RMSE)", centre=(0.5, -0.45, 0),
                      x_text=lambda v: f"{10 ** v:,.0f}")
        lines, dots = {}, {}
        for model, colour in [("forest", GREEN), ("boosting", PURPLE)]:
            rows = scores[scores["model"] == model]
            xs = np.log10(rows["trees"])
            lines[model] = chart.line(xs, rows["validation"], colour)
            dots[model] = VGroup(*[Dot(chart.p(x, y), 0.08, color=colour) for x, y in zip(xs, rows["validation"])])
        boost = scores[scores["model"] == "boosting"]
        best = boost.loc[boost["validation"].idxmin()]
        mark = Circle(0.22, color=PURPLE, stroke_width=5).move_to(chart.p(np.log10(best["trees"]), best["validation"]))
        names = VGroup(label("random forest", 30, GREEN, weight=BOLD).next_to(chart.p(2.3, 3.72), DOWN, 0.2),
                       label("boosting", 30, PURPLE, weight=BOLD).next_to(chart.p(3.05, 3.97), UP, 0.25))
        best_name = label(f"best at {int(best['trees'])} trees", 30, PURPLE, weight=BOLD).next_to(mark, UP, 0.5)
        noise = card("later trees fit the noise", PURPLE, 28).move_to(chart.p(2.6, 4.45))
        # "More trees never hurt a forest."
        self.play(FadeIn(chart.frame), run_time=self.share(0.08))
        self.play(Create(lines["forest"]), FadeIn(dots["forest"]), FadeIn(names[0]), run_time=self.share(0.15))
        # "Boosting is different: on the validation sites it does best at 200 trees,"
        cue(self, "Boosting is different")
        self.play(Create(lines["boosting"]), FadeIn(dots["boosting"]), FadeIn(names[1]), run_time=self.share(0.15))
        cue(self, "at 200")
        self.play(Create(mark), FadeIn(best_name), run_time=self.share(0.08))
        # "then gets worse, as the later trees fit the noise."
        cue(self, "then gets worse")
        self.play(FadeIn(noise, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


def rmse_bars(rows, head_text, top=5.0, width=8.0):
    """Horizontal RMSE bars, each with its value as the pages round it."""
    head = label(head_text, 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
    left = -2.2
    bars = VGroup()
    for i, (name, value, colour) in enumerate(rows):
        y = 1.6 - 1.15 * i
        length = value / top * width
        bar = Rectangle(width=length, height=0.75, stroke_width=0, fill_color=colour, fill_opacity=0.85)
        bar.move_to([left + length / 2, y, 0])
        what = label(name, 30, INK, weight=BOLD).next_to([left, y, 0], LEFT, 0.3)
        amount = label(f"{value:.2f}", 34, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)
        bars.add(VGroup(bar, what, amount))
    axis_name = label("error on the test sites (RMSE, lower is better)", 26, SUBDUED)
    axis_name.next_to(bars, DOWN, 0.4).set_x(left + width / 2)
    return head, bars, axis_name


class Scene22(VideoScene):
    number = 22

    def construct(self):
        # Page results: forests-and-boosting.qmd#tbl-test.
        table = self.data("ensembles-test").set_index("model")
        head, bars, axis_name = rmse_bars([("single tree", table.loc["tree", "rmse"], GREY),
                                           ("boosting", table.loc["boost", "rmse"], PURPLE),
                                           ("random forest", table.loc["forest", "rmse"], GREEN),
                                           ("Poisson regression", table.loc["poisson", "rmse"], VERMILION)],
                                          "four models on new sites")
        # "On new sites, both ensembles beat the single tree."
        self.play(FadeIn(head), FadeIn(axis_name), run_time=self.share(0.1))
        self.play(GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]), run_time=self.share(0.1))
        cue(self, "both ensembles")
        self.play(*[GrowFromEdge(b[0], LEFT) for b in bars[1:3]], *[FadeIn(b[1:]) for b in bars[1:3]],
                  run_time=self.share(0.15))
        # "But neither beats Poisson regression."
        cue(self, "But neither")
        self.play(GrowFromEdge(bars[3][0], LEFT), FadeIn(bars[3][1:]), run_time=self.share(0.12))
        self.play(Indicate(bars[3], color=VERMILION, scale_factor=1.04), run_time=self.share(0.12))
        self.finish()


class Scene23(KeyPointScene):
    number, point = 23, 2


# Choosing between them (scenes 24–29) ---------------------------------------------------

class Scene24(VideoScene):
    number = 24

    def construct(self):
        # Schematic: the five questions, after the choosing page's diagram.
        head = label("five questions narrow the choice", 44, INK, weight=BOLD).to_edge(UP, buff=0.8)
        cards = VGroup(panel("the aim", ["predict or", "explain?"], BLUE, 2.6, 2.2, 22),
                       panel("the outcome", ["quantity, count", "or yes/no?"], ORANGE, 2.6, 2.2, 22),
                       panel("the range", ["beyond the", "sampled range?"], GREEN, 2.6, 2.2, 22),
                       panel("the data", ["hundreds or", "thousands?"], SKY, 2.6, 2.2, 22),
                       panel("the audience", ["who must", "accept it?"], PURPLE, 2.6, 2.2, 22)
                       ).arrange(RIGHT, buff=0.12).move_to([0, -0.3, 0])
        # "So which method should you use? Five questions narrow the choice:"
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "the aim, the kind of outcome, the range you must predict over, how much data you have,
        # and who must accept the result."
        for c, phrase in zip(cards, ["the aim", "the kind", "the range", "how much", "and who"]):
            cue(self, phrase)
            self.play(FadeIn(c, shift=0.2 * UP), run_time=self.share(0.05))
        self.finish()


# The choosing page's labels, as they read mid-sentence on screen.
METHOD_NAMES = {"Negative binomial model": "negative binomial", "Poisson regression": "Poisson regression",
                "Polynomial regression": "polynomial regression", "Linear regression": "linear regression",
                "Random forest": "random forest", "Boosting": "boosting", "Decision tree": "decision tree"}


def comparison_layout(scene):
    table = scene.data("comparison")          # already ordered by test RMSE
    chart = Chart([3.4, 4.6, 0.2], [0, len(table) + 1, 1], 7.6, 4.9, x_ticks=(3.5, 4.0, 4.5),
                  x_name="error on new sites (RMSE, lower is better)", centre=(2.2, -0.2, 0))
    rows = {}
    for i, (_, r) in enumerate(table.iterrows()):
        y = len(table) - i
        name = label(METHOD_NAMES[r["model"]], 28, INK, weight=BOLD).next_to(chart.p(3.4, y), LEFT, 0.3)
        test = Dot(chart.p(r["test_rmse"], y), 0.13, color=BLUE)
        valid = Dot(chart.p(r["validation_rmse"], y), 0.13, color=ORANGE)
        link = Line(test.get_center(), valid.get_center(), color=GRID, stroke_width=6)
        rows[r["model"]] = (y, name, test, valid, link)
    guides = VGroup(*[DashedLine(chart.p(3.4, y), chart.p(4.6, y), color=GRID, stroke_width=1.5)
                      for (y, *_) in rows.values()])
    key = VGroup(VGroup(Dot(color=BLUE, radius=0.12), label("test sites", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
                 VGroup(Dot(color=ORANGE, radius=0.12), label("validation sites", 26, SUBDUED)).arrange(RIGHT, buff=0.15)
                 ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.4)
    return table, chart, rows, guides, key


class Scene25(VideoScene):
    number = 25

    def construct(self):
        # Page results: choosing-a-method.qmd#fig-comparison, the test sites.
        table, chart, rows, guides, key = comparison_layout(self)
        order = list(table["model"])
        counts = SurroundingRectangle(VGroup(*[rows[m][1] for m in order[:2]]), color=GREEN, buff=0.12,
                                      corner_radius=0.1)
        trees = SurroundingRectangle(VGroup(*[rows[m][1] for m in order[-3:]]), color=ORANGE, buff=0.12,
                                     corner_radius=0.1)
        few = card("a few hundred noisy stations", PURPLE, 28).move_to(chart.p(4.25, 7.4))
        # "Scored on the same new sites,"
        self.play(FadeIn(VGroup(chart.axes.x_axis, chart.ticks, chart.x_name)), FadeIn(guides), FadeIn(key[0]),
                  FadeIn(VGroup(*[rows[m][1] for m in order])), run_time=self.share(0.12))
        self.play(LaggedStart(*[FadeIn(rows[m][2], scale=0.5) for m in order], lag_ratio=0.15),
                  run_time=self.share(0.15))
        # "the two count models come first, and the three tree-based models last."
        cue(self, "the two count")
        self.play(Create(counts), run_time=self.share(0.08))
        cue(self, "and the three")
        self.play(Create(trees), run_time=self.share(0.08))
        # "A few hundred noisy stations are too few for many trees to beat a simple curve."
        cue(self, "A few hundred")
        self.play(FadeIn(few, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene26(VideoScene):
    number = 26

    def construct(self):
        # Page results: choosing-a-method.qmd#fig-comparison, the validation sites added.
        table, chart, rows, guides, key = comparison_layout(self)
        order = list(table["model"])
        self.add(chart.axes.x_axis, chart.ticks, chart.x_name, guides, key[0],
                 *[rows[m][1] for m in order], *[rows[m][2] for m in order])
        best = table.loc[table["validation_rmse"].idxmin(), "model"]
        ring = Circle(0.25, color=ORANGE, stroke_width=5).move_to(rows[best][3])
        first = card("first on validation", ORANGE, 24).next_to(ring, RIGHT, 0.2)
        tuned = card("tuned on these sites: a kind of overfitting", VERMILION, 28).move_to(chart.p(4.0, 7.4))
        close = card("one split cannot separate close models", PURPLE, 28).move_to(tuned)
        # "On the validation sites, though, the single tree came first."
        self.play(FadeIn(key[1]), *[Create(rows[m][4]) for m in order], *[FadeIn(rows[m][3], scale=0.5) for m in order],
                  run_time=self.share(0.12))
        cue(self, "the single tree")
        self.play(Create(ring), FadeIn(first), run_time=self.share(0.06))
        # "Its depth, and boosting's number of trees, were chosen on those same sites, so both were
        # tuned to their chance patterns: a kind of overfitting."
        cue(self, "Its depth")
        self.play(*[rows[m][4].animate.set_color(VERMILION) for m in ("Decision tree", "Boosting")],
                  *[Indicate(rows[m][1], color=VERMILION) for m in ("Decision tree", "Boosting")], run_time=self.share(0.08))
        cue(self, "so both were")
        self.play(FadeIn(tuned, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "The test sites, kept apart, show the cost."
        cue(self, "The test sites")
        self.play(*[Indicate(rows[m][2], color=BLUE, scale_factor=1.6) for m in ("Decision tree", "Boosting")],
                  run_time=self.share(0.08))
        # "And one split cannot tell apart models that are close."
        cue(self, "And one split")
        self.play(ReplacementTransform(tuned, close), run_time=self.share(0.06))
        self.finish()


def beyond_layout(scene):
    table = scene.data("extrapolate")
    span = scene.data("extrapolate-range").iloc[0]
    chart = Chart([0, 22, 1], [-1.5, 6.5, 1], 9.8, 5.0, x_ticks=range(0, 21, 5), y_ticks=(0, 2, 4, 6),
                  x_name="temperature (°C)", y_name="predicted count", centre=(-1.3, -0.45, 0))
    shades = VGroup(chart.shade(0, span["low"]), chart.shade(span["high"], 22))
    zero = chart.hline(0)
    beyond = label("beyond the data", 24, SUBDUED).move_to(chart.p(19.1, 6.1))
    curves = {"forest": model_curve(chart, table, "Random forest", ORANGE),
              "poisson": model_curve(chart, table, "Poisson regression", GREEN),
              "line": model_curve(chart, table, "Linear regression", BLUE)}
    ends = {m: table[table["model"] == name].iloc[-1][".pred"]
            for m, name in [("forest", "Random forest"), ("poisson", "Poisson regression"), ("line", "Linear regression")]}
    names = {"forest": label("random forest", 26, ORANGE, weight=BOLD).next_to(chart.p(22, ends["forest"]), RIGHT, 0.1),
             "poisson": label("Poisson regression", 26, GREEN, weight=BOLD).next_to(chart.p(22, ends["poisson"]), RIGHT, 0.1)
             .shift(0.15 * UP),
             "line": label("linear regression", 26, BLUE, weight=BOLD).next_to(chart.p(22, ends["line"]), RIGHT, 0.1)
             .shift(0.15 * DOWN)}
    return chart, VGroup(shades, zero, beyond), curves, names


class Scene27(VideoScene):
    number = 27

    def construct(self):
        # Page results: choosing-a-method.qmd#fig-extrapolate.
        chart, backdrop, curves, names = beyond_layout(self)
        # "Beyond the sampled temperatures, each model follows its own rule."
        self.play(FadeIn(chart.frame), FadeIn(backdrop), run_time=self.share(0.1))
        self.play(*[Create(c) for c in curves.values()], run_time=self.share(0.2))
        # "The forest stays level, Poisson regression flattens towards zero, and the straight line falls below it."
        for key, phrase in [("forest", "The forest"), ("poisson", "Poisson regression"), ("line", "and the straight")]:
            cue(self, phrase)
            self.play(FadeIn(names[key]), Indicate(curves[key], color=curves[key].get_color(), scale_factor=1.0),
                      run_time=self.share(0.1))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        # Page results as in scene 27, with the page's conclusion over them.
        chart, backdrop, curves, names = beyond_layout(self)
        self.add(chart.frame, backdrop, *curves.values(), *names.values())
        nothing = card("nothing in the data says which is right", VERMILION, 34).move_to([0, 0.8, 0])
        defend = card("choose an assumption you can defend, and say it", PURPLE, 34).move_to([0, -0.6, 0])
        dimmed = VGroup(chart.frame, backdrop, *curves.values(), *names.values())
        # "Nothing in the data says which is right."
        self.play(dimmed.animate.set_opacity(0.25), FadeIn(nothing, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "So choose a model whose assumption you can defend, and say what it is."
        cue(self, "So choose")
        self.play(FadeIn(defend, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene29(KeyPointScene):
    number, point = 29, 3


# The quiz (scenes 30–31) ----------------------------------------------------------------

class Scene30(QuizScene):
    number = 30
    question = ("A linear regression of counts", "gives a few predictions below zero.",
                "They are set to zero.", "Is the problem solved?")


class Scene31(VideoScene):
    number = 31

    def construct(self):
        # Schematic: a line clipped at zero, the model beneath unchanged, then a count model.
        answer = label("No", 64, VERMILION, weight=BOLD).to_edge(UP, buff=0.5)
        chart = Chart([0, 10, 1], [-2, 6, 1], 9.0, 4.2, x_name="an input", y_name="predicted count", centre=(0.4, -0.6, 0))
        zero = chart.hline(0)
        xs = np.linspace(0, 10, 50)
        line = chart.line(xs, 5 - 0.65 * xs, BLUE)
        below = chart.line(xs[xs > 7.6], (5 - 0.65 * xs)[xs > 7.6], BLUE).set_stroke(opacity=0.35)
        clipped = chart.line(xs[xs > 7.6], 0 * xs[xs > 7.6], BLUE, 8)
        hidden = label("clipped: the symptom hidden", 28, BLUE, weight=BOLD).next_to(chart.p(7.4, 0), UP, 0.35)
        still = label("the model still allows it", 26, SUBDUED).next_to(chart.p(9.3, -1.5), LEFT, 0.2)
        count = chart.line(xs, 5 * np.exp(-0.32 * xs), GREEN)
        count_name = card("a count model: never below zero", GREEN, 30).move_to(chart.p(5.3, 4.9))
        # "No."
        self.play(FadeIn(answer, scale=0.9), FadeIn(chart.frame), FadeIn(zero), Create(line), run_time=self.share(0.12))
        # "Clipping hides the symptom,"
        cue(self, "Clipping")
        self.play(ReplacementTransform(line.copy(), clipped), line.animate.set_stroke(opacity=0.35),
                  FadeIn(hidden), run_time=self.share(0.12))
        # "but the model still assumes a count can fall below zero."
        cue(self, "but the model")
        self.play(Indicate(below, color=VERMILION), FadeIn(still), run_time=self.share(0.12))
        # "A count model, such as Poisson regression, cannot make that mistake."
        cue(self, "A count model")
        self.play(FadeOut(hidden), FadeOut(still), FadeOut(clipped), line.animate.set_stroke(opacity=0.15),
                  Create(count), FadeIn(count_name), run_time=self.share(0.2))
        self.finish()


# The recap (scenes 32–34) and the end card (scene 35) -----------------------------------

class Scene32(RecapScene):
    number, point = 32, 1


class Scene33(RecapScene):
    number, point = 33, 2


class Scene34(RecapScene):
    number, point = 34, 3


class Scene35(EndCardScene):
    number = 35
