"""Manim scenes for the supervised learning video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/03-supervised-learning
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is an overview of the section: three points from its seven pages. Scenes marked
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
            "Models that learn their shape",
            "How to choose between them"]
ANSWERS = ["Match the model to the outcome:\na count is never negative,\na probability needs a threshold",
           "Flexible models learn the shape;\na hyperparameter, chosen on\nvalidation data, sets how closely",
           "Start from the question\nand the outcome, not the\nmost flexible method"]
RECAP = ["Match the model to the outcome",
         "Choose hyperparameters on validation data",
         "Start from the question"]


class Scene01(LearnScene):
    number = 1
    times = (0.64, 0.75, 0.9)


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


# Models that add up their inputs (scenes 2–12) ------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        # Schematic: a quantity on a number line, a category as two answers.
        head = label("the outcome: the answer the model predicts", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        decides = card("the kind of outcome decides which models fit", PURPLE, 34).move_to(head)
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
        # "Let's start with the outcome: the answer the model predicts."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "As we saw in the introduction, when the outcome is a quantity, such as a temperature
        # or a count, the task is regression."
        cue(self, "is a quantity")
        self.play(FadeIn(quantity), run_time=self.share(0.1))
        cue(self, "the task is regression")
        self.play(FadeIn(names[0], shift=0.2 * UP), run_time=self.share(0.06))
        # "When it is a category, such as present or absent, it is classification."
        cue(self, "When it is a category")
        self.play(FadeIn(category), run_time=self.share(0.1))
        cue(self, "it is classification")
        self.play(FadeIn(names[1], shift=0.2 * UP), run_time=self.share(0.06))
        # "The kind of outcome decides which models fit."
        cue(self, "The kind of outcome")
        self.play(ReplacementTransform(head, decides), run_time=self.share(0.08))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        # Page results: count-regression.qmd, the survey's counts.
        hist = self.data("histogram")
        chart = Chart([-0.5, 40.5, 5], [0, 200, 50], 10.5, 4.6, x_ticks=range(0, 41, 10), y_ticks=(0, 100, 200),
                      x_name="animals caught at a station", y_name="stations", centre=(0.5, -0.6, 0))
        base = chart.p(0, 0)[1]
        bars = VGroup()
        for _, row in hist.iterrows():
            x, n = row["abundance"], row["n"]
            height = max(chart.p(0, n)[1] - base, 0.02)
            bar = Rectangle(width=chart.p(0.9, 0)[0] - chart.p(0, 0)[0], height=height, stroke_width=0,
                            fill_color=BLUE, fill_opacity=0.85)
            bars.add(bar.move_to([chart.p(x, 0)[0], base + height / 2, 0]))
        head = label("the count of one species at each station", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        floor = Arrow(chart.p(6, 150), chart.p(0, 150), color=VERMILION, stroke_width=5, buff=0.1)
        never = label("never below zero", 32, VERMILION, weight=BOLD).next_to(floor, RIGHT, 0.15)
        few = card("most stations: only a few animals", PURPLE, 30).move_to(chart.p(24, 100))
        gloss = label("each bar: the number of stations that caught that many animals", 28, SUBDUED)
        gloss.next_to(head, DOWN, 0.3)
        tail = bars[-2:]
        large = plated(label("a few large catches", 26, BLUE, weight=BOLD)).next_to(chart.p(38.5, 4), UP, 0.4)
        # "In this section, the outcome is the count of one species at each station of the survey."
        self.play(FadeIn(head), FadeIn(chart.frame), run_time=self.share(0.1))
        # "This chart is a histogram: each bar shows how many stations caught that number of animals."
        cue(self, "This chart")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(gloss),
                  run_time=self.share(0.18))
        # "A count is a whole number, and it never falls below zero."
        cue(self, "it never falls")
        self.play(GrowArrow(floor), FadeIn(never), run_time=self.share(0.08))
        # "Most stations caught only a few animals, and a few made large catches."
        cue(self, "Most stations")
        self.play(Indicate(VGroup(*bars[:6]), color=PURPLE, scale_factor=1.05), FadeIn(few, shift=0.2 * UP),
                  run_time=self.share(0.1))
        cue(self, "and a few made")
        self.play(Indicate(tail, color=BLUE, scale_factor=1.3), FadeIn(large), run_time=self.share(0.08))
        self.finish()


def count_chart():
    return Chart([1.5, 16.5, 1], [-6, 7, 1], 10.5, 5.2, x_ticks=(2, 6, 10, 14), y_ticks=(-4, 0, 4),
                 x_name="temperature (°C)", y_name="predicted count", centre=(0.5, -0.45, 0))


def count_layout(scene):
    """Three models across the survey's temperatures: the line and the curve from the linear
    page, Poisson regression from the count page (same grid, same curve on both)."""
    line = scene.data("line-curves")
    counts = scene.data("count-curves")
    table = pd.concat([line, counts[counts["model"] == "Poisson regression"]])
    chart = count_chart()
    zero = chart.hline(0)
    zero_name = label("zero", 24, SUBDUED).next_to(chart.p(16.5, 0), RIGHT, 0.1)
    curves = {"line": model_curve(chart, table, "Linear regression", BLUE),
              "curve": model_curve(chart, table, "Polynomial regression", ORANGE),
              "poisson": model_curve(chart, table, "Poisson regression", VERMILION)}
    return table, chart, VGroup(zero, zero_name), curves


def curve_name(text, colour, point, direction=UP):
    return plated(label(text, 30, colour, weight=BOLD)).next_to(point, direction, 0.2)


class Scene04(VideoScene):
    number = 4

    def construct(self):
        # Page results: linear-and-polynomial-regression.qmd#fig-shapes, linear regression.
        table, chart, zero, curves = count_layout(self)
        name = curve_name("linear regression: one slope", BLUE, chart.p(10.5, 4.6))
        # Schematic first: the sum linear regression makes, before the page's line.
        head = label("linear regression adds up its inputs", 40, BLUE, weight=BOLD).to_edge(UP, buff=0.7)
        first = VGroup(label("predicted count  =", 32, INK), label("a starting value", 32, INK)).arrange(RIGHT, buff=0.25)
        terms = VGroup(first, label("+  so much per degree of temperature", 32, INK),
                       label("+  so much per metre of depth", 32, INK),
                       label("+  …", 32, INK)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        for t in terms[1:]:
            t.align_to(first[1], LEFT).shift(0.45 * LEFT)     # the "+" hangs left of the terms
        terms.move_to([-1.5, 0.0, 0])
        amounts = VGroup(terms[1], terms[2])
        brace = Brace(amounts, RIGHT, color=PURPLE)
        coefficients = VGroup(label("coefficients:", 28, PURPLE, weight=BOLD),
                              label("learned from the\ntraining data", 26, PURPLE)).arrange(DOWN, buff=0.1)
        coefficients.next_to(brace, RIGHT, 0.2)
        # "The first family of models adds up its inputs. Linear regression, met in the introduction
        # as a straight line, starts from a fixed value,"
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.06))
        cue(self, "starts from")
        self.play(FadeIn(terms[0]), run_time=self.share(0.05))
        # "then adds a fixed amount for each input: so much per degree of temperature, so much per metre of depth."
        cue(self, "so much per degree")
        self.play(FadeIn(terms[1], shift=0.2 * RIGHT), run_time=self.share(0.05))
        cue(self, "so much per metre")
        self.play(FadeIn(terms[2], shift=0.2 * RIGHT), FadeIn(terms[3]), run_time=self.share(0.05))
        # "These amounts are its coefficients, learned from the training data."
        cue(self, "These amounts")
        self.play(GrowFromCenter(brace), FadeIn(coefficients), run_time=self.share(0.06))
        # "Against temperature, that gives one slope, the same in cold water and warm."
        cue(self, "Against temperature")
        self.play(FadeOut(VGroup(head, terms, brace, coefficients)), FadeIn(chart.frame), FadeIn(zero),
                  run_time=self.share(0.06))
        self.play(Create(curves["line"]), run_time=self.share(0.1))
        self.play(FadeIn(name), run_time=self.share(0.06))
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
        square = square_card()
        # "But a straight line cannot rise and then fall."
        self.play(curves["line"].animate.set_stroke(opacity=0.5), run_time=self.share(0.06))
        # "Add the square of temperature as one more input,"
        cue(self, "Add the square")
        self.play(FadeIn(square, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "and the line can bend into a curve."
        cue(self, "and the line can bend")
        self.play(TransformFromCopy(curves["line"], curves["curve"]), run_time=self.share(0.15))
        # "This is polynomial regression. It still adds up its inputs, and here it finds a peak at 7.5 degrees."
        cue(self, "This is polynomial")
        self.play(FadeIn(name), run_time=self.share(0.06))
        cue(self, "and here it finds")
        self.play(FadeIn(peak, scale=0.8), run_time=self.share(0.08))
        self.finish()


def square_card():
    return card("+ temperature²: one more input", ORANGE, 30).move_to([-3.2, 2.9, 0])


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
        self.add(chart.frame, zero, curves["line"], curves["curve"], optimum_marker(self, chart, table), square_card())
        scores = self.data("line-curve-scores").set_index("model")
        stations = int(self.data("optimum").iloc[0]["test_stations"])
        area = below_zero(chart, table)
        words = plated(label("fewer than zero animals", 32, VERMILION, weight=BOLD)).next_to(chart.p(12.2, -2.2), LEFT, 0.3)
        count = card(f"at {int(scores.loc['Polynomial regression', 'below_zero'])} of the {stations} test stations", VERMILION, 30)
        count.move_to([3.4, 2.9, 0])
        # "But nothing in linear regression knows that a count stops at zero."
        self.play(Indicate(zero[0], color=INK), run_time=self.share(0.15))
        # "In warm water the curve falls below zero,"
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
        scores = self.data("line-curve-scores").set_index("model")
        stations = int(self.data("optimum").iloc[0]["test_stations"])
        count = card(f"at {int(scores.loc['Polynomial regression', 'below_zero'])} of the {stations} test stations",
                     VERMILION, 30).move_to([3.4, 2.9, 0])
        peak = optimum_marker(self, chart, table)
        earlier = VGroup(peak, square_card(), count, below_zero(chart, table))
        self.add(chart.frame, zero, curves["line"], curves["curve"], earlier)
        name = plated(label("Poisson regression", 30, VERMILION, weight=BOLD)).move_to(chart.p(8.5, -1.6))
        steps = [label("add up the inputs", 30, INK, weight=BOLD), label("the log of the count", 30, INK, weight=BOLD),
                 label("the count: above zero", 30, VERMILION, weight=BOLD)]
        arrows = [Arrow(LEFT, RIGHT, color=GREY, stroke_width=5).scale(0.4) for _ in range(2)]
        chain = VGroup(steps[0], arrows[0], steps[1], arrows[1], steps[2]).arrange(RIGHT, buff=0.2).move_to([0, 2.95, 0])
        # "Poisson regression is made for counts."
        self.play(FadeOut(earlier), curves["line"].animate.set_stroke(opacity=0.25),
                  curves["curve"].animate.set_stroke(opacity=0.35), run_time=self.share(0.06))
        self.play(Create(curves["poisson"]), FadeIn(name), run_time=self.share(0.12))
        # "It adds up its inputs in the same way, but the sum gives the logarithm of the count, not the count itself."
        cue(self, "It adds up")
        self.play(FadeIn(steps[0]), run_time=self.share(0.05))
        cue(self, "but the sum")
        self.play(GrowArrow(arrows[0]), FadeIn(steps[1], shift=0.2 * RIGHT), run_time=self.share(0.06))
        # "Turning a logarithm back into a count always gives a number above zero."
        cue(self, "Turning a logarithm")
        self.play(GrowArrow(arrows[1]), FadeIn(steps[2], shift=0.2 * RIGHT), run_time=self.share(0.06))
        # "So a prediction can come close to zero, but never cross it."
        cue(self, "So a prediction")
        self.play(Indicate(steps[2], color=VERMILION), Indicate(zero[0], color=INK), run_time=self.share(0.1))
        self.finish()


SUBSTRATE_ROWS = [("sand", None), ("mud", "substratemud"), ("rock", "substraterock")]


class Scene08(VideoScene):
    number = 8

    def construct(self):
        # Page results: count-regression.qmd#each-coefficient-is-a-multiplier.
        table = self.data("multipliers").set_index("term")
        chart = Chart([0.5, 2.0, 0.25], [0, 3, 1], 9.0, 3.6, x_ticks=(0.5, 1, 1.5, 2), x_name="multiplier on the count",
                      centre=(1.0, -0.2, 0))
        one = DashedLine(chart.p(1, 0), chart.p(1, 3), color=GREY, stroke_width=3)
        rows = {}
        for i, (name, term) in enumerate(SUBSTRATE_ROWS):
            y = 2.5 - i
            value = 1 if term is None else table.loc[term, "multiplier"]
            rows[name] = VGroup(label(name, 34, INK, weight=BOLD).next_to(chart.p(0.5, y), LEFT, 0.4),
                                Dot(chart.p(value, y), 0.14, color=GREY if term is None else VERMILION))
        head = label("each seabed type against sand", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        held = label("with the same water and the same season", 28, SUBDUED).next_to(head, DOWN, 0.25)
        times = label(f"× {table.loc['substratemud', 'multiplier']:.2f}", 34, VERMILION, weight=BOLD)
        times.next_to(rows["mud"][1], UP, 0.15)
        rock = label(f"× {table.loc['substraterock', 'multiplier']:.2f}", 34, VERMILION, weight=BOLD)
        rock.next_to(rows["rock"][1], UP, 0.15)
        base = label("baseline", 26, SUBDUED).next_to(rows["sand"][1], RIGHT, 0.25)
        # "Because of the logarithm, each coefficient becomes a multiplier."
        self.play(FadeIn(VGroup(chart.axes.x_axis, chart.ticks, chart.x_name)), Create(one), run_time=self.share(0.1))
        # "Take the seabed."
        cue(self, "Take the seabed")
        self.play(FadeIn(head), FadeIn(rows["sand"]), FadeIn(base), run_time=self.share(0.08))
        # "With everything else held fixed, the same water and the same season,"
        cue(self, "With everything")
        self.play(FadeIn(held), run_time=self.share(0.06))
        # "a muddy station is expected to hold 1.34 times the count of a sandy one."
        cue(self, "a muddy station")
        self.play(FadeIn(rows["mud"]), run_time=self.share(0.06))
        cue(self, "1.34")
        self.play(FadeIn(times, shift=0.1 * UP), run_time=self.share(0.06))
        # "A rocky station is expected to hold fewer, so its multiplier is below one."
        cue(self, "A rocky station")
        self.play(FadeIn(rows["rock"]), run_time=self.share(0.06))
        cue(self, "so its multiplier")
        self.play(FadeIn(rock, shift=0.1 * UP), Indicate(one, color=INK), run_time=self.share(0.06))
        self.finish()


class Scene09(VideoScene):
    number = 9

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
        found = plated(label("found", 26, INK, weight=BOLD)).next_to(chart.p(2.0, 1), DOWN, 0.2).align_to(chart.p(2.0, 0), LEFT)
        missing = plated(label("not found", 26, INK, weight=BOLD)).next_to(chart.p(9.0, 0), UP, 0.2)
        head = label("logistic regression", 40, VERMILION, weight=BOLD).to_edge(UP, buff=0.4)
        chance = label("the chance that the species is present", 28, SUBDUED).next_to(head, DOWN, 0.2)
        stays = card("always between 0 and 1", VERMILION, 30).move_to(chart.p(9, 0.45))
        # "For present or absent, logistic regression uses the same idea."
        self.play(FadeIn(chart.frame), FadeIn(edges), run_time=self.share(0.08))
        cue(self, "logistic regression")
        self.play(FadeIn(head), run_time=self.share(0.06))
        # "It adds up its inputs, then squeezes the sum into a probability, the chance that the
        # species is present,"
        cue(self, "then squeezes")
        self.play(Create(line), FadeIn(chance), run_time=self.share(0.18))
        # "which always stays between zero and one."
        cue(self, "which always")
        self.play(Indicate(edges, color=INK), FadeIn(stays, shift=0.2 * UP), run_time=self.share(0.08))
        # "The dots are the training stations: along the top where the species was found,
        # along the bottom where it was not."
        cue(self, "The dots")
        self.play(FadeOut(stays), FadeIn(dots), run_time=self.share(0.08))
        cue(self, "along the top")
        self.play(FadeIn(found), run_time=self.share(0.05))
        cue(self, "along the bottom")
        self.play(FadeIn(missing), run_time=self.share(0.05))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        # Schematic: the two ways a present-or-absent answer can be wrong.
        head = label("from a probability to present or absent", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        chips = VGroup(card("probability", GREY, 30), card("present", GREEN, 30), card("absent", GREY, 30))
        arrow = Arrow(LEFT, RIGHT, color=INK, stroke_width=5)
        threshold = label("threshold:\na cut-off", 26, SUBDUED)
        answers = VGroup(chips[1], chips[2]).arrange(DOWN, buff=0.25)
        flow = VGroup(chips[0], VGroup(arrow, threshold).arrange(DOWN, buff=0.1), answers).arrange(RIGHT, buff=0.4)
        flow.next_to(head, DOWN, 0.5)

        def mistake(name, said, truth, colour):
            return panel(name, [f"said: {said}", f"truly: {truth}"], colour, 4.6, 2.2, 30)

        alarm = mistake("a false alarm", "present", "absent", ORANGE)
        miss = mistake("a miss", "absent", "present", BLUE)
        VGroup(alarm, miss).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.6)
        two = label("two ways to be wrong", 30, SUBDUED, weight=BOLD).next_to(VGroup(alarm, miss), UP, 0.25)
        # "To get a plain answer, choose a threshold, a cut-off: above it, call the species present;
        # below it, absent."
        self.play(FadeIn(head), FadeIn(chips[0]), run_time=self.share(0.08))
        cue(self, "choose a threshold")
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


class Scene11(VideoScene):
    number = 11

    def construct(self):
        # Page results: logistic-regression.qmd, the thresholds table.
        table = self.data("thresholds").set_index("threshold")
        head = label("false alarms and misses on the test stations", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
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
        # "At a threshold of 0.5, the model gives 34 false alarms and 4 misses on the test stations."
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
        # "So the right threshold depends on what each mistake costs."
        cue(self, "So the right")
        self.play(ReplacementTransform(head, cost), run_time=self.share(0.08))
        self.finish()


class Scene12(KeyPointScene):
    number, point = 12, 1


# Models that learn their shape (scenes 13–23) -------------------------------------------

class Scene13(VideoScene):
    number = 13

    def construct(self):
        # Schematic: made-up points on two unnamed inputs, after the kNN page's diagram.
        rng = np.random.default_rng(13)
        chart = Chart([0, 10, 1], [0, 10, 1], 6.4, 5.0, x_name="input 1", y_name="input 2", centre=(-2.2, -0.3, 0))
        points = rng.uniform(0.5, 9.5, size=(40, 2))
        new = np.array([5.2, 4.8])
        order = np.argsort(np.hypot(*(points - new).T))
        near = order[:5]
        radius = np.hypot(*(points[near[-1]] - new)) + 0.35
        dots = VGroup(*[Dot(chart.p(*p), 0.09, color=GREY) for p in points])
        star = Star(5, outer_radius=0.2, color=VERMILION, fill_opacity=1).move_to(chart.p(*new))
        links = VGroup(*[Line(chart.p(*new), chart.p(*points[i]), color=BLUE, stroke_width=3) for i in near])
        ring = Circle(radius * (chart.p(1, 0)[0] - chart.p(0, 0)[0]), color=BLUE, stroke_width=4).move_to(star)
        head = label("k-nearest neighbours", 44, BLUE, weight=BOLD).to_corner(UL, buff=0.6)
        shape = label("every model so far assumes a shape", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        new_name = VGroup(Star(5, outer_radius=0.16, color=VERMILION, fill_opacity=1),
                          label("a new station", 30, VERMILION, weight=BOLD)).arrange(RIGHT, buff=0.2)
        notes = VGroup(card("k = 5", BLUE, 34),
                       card("prediction:\ntheir average count", PURPLE, 30)).arrange(DOWN, buff=0.5)
        VGroup(new_name, notes).arrange(DOWN, buff=0.5).move_to([4.3, -0.3, 0])
        # "Next, models that learn their shape. Every model so far assumes a shape, such as a line or a curve."
        self.play(FadeIn(chart.frame), FadeIn(dots), run_time=self.share(0.1))
        cue(self, "Every model")
        self.play(FadeIn(shape, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "k-nearest neighbours, met in the introduction, assumes none."
        cue(self, "k-nearest neighbours")
        self.play(ReplacementTransform(shape, head), run_time=self.share(0.08))
        # "For a new station, it finds the k most similar stations in the training data, here five,"
        cue(self, "For a new station")
        self.play(FadeIn(star, scale=0.5), FadeIn(new_name), run_time=self.share(0.07))
        cue(self, "it finds")
        self.play(*[Create(l) for l in links], *[dots[i].animate.set_color(BLUE).scale(1.4) for i in near],
                  Create(ring), run_time=self.share(0.12))
        cue(self, "here five")
        self.play(FadeIn(notes[0]), run_time=self.share(0.05))
        # "and predicts their average count."
        cue(self, "and predicts")
        self.play(FadeIn(notes[1], shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


def neighbours_layout(scene):
    """The kNN page's figure: the error against the number of neighbours, on a log scale."""
    table = scene.data("neighbours")
    chart = Chart([0, np.log10(300), 1], [0, 5.5, 1], 10.5, 5.0, x_ticks=np.log10([1, 3, 10, 30, 100, 300]),
                  y_ticks=(0, 2, 4), x_name="number of neighbours, k", y_name="error (RMSE)", centre=(0.5, -0.45, 0),
                  x_text=lambda v: f"{10 ** v:.0f}")
    xs = np.log10(table["k"])
    lines = {name: VGroup(chart.line(xs, table[name], colour),
                          *[Dot(chart.p(x, y), 0.07, color=colour) for x, y in zip(xs, table[name])])
             for name, colour in [("training", BLUE), ("validation", ORANGE)]}
    names = {"training": plated(label("training stations", 28, BLUE, weight=BOLD)).next_to(chart.p(0.25, 0.3), RIGHT, 0.1),
             "validation": plated(label("validation sites", 28, ORANGE, weight=BOLD)).next_to(chart.p(0.08, 5.2), RIGHT, 0.25)}
    return table, chart, lines, names


class Scene14(VideoScene):
    number = 14

    def construct(self):
        # Page results: nearest-neighbours.qmd#fig-neighbours.
        table, chart, lines, names = neighbours_layout(self)
        one = table.iloc[0]
        ring = Circle(0.25, color=ORANGE, stroke_width=5).move_to(chart.p(0, one["validation"]))
        head = neighbours_head()
        overfit = card("overfitting:\nlearning the noise", VERMILION, 30).move_to(chart.p(0.8, 2.2))
        blur = card("one average", GREY, 28).move_to(chart.p(2.25, 2.4))
        # "How many neighbours should it use? This chart shows the error, the typical miss from the
        # introduction, for each number of neighbours."
        self.play(FadeIn(chart.frame), run_time=self.share(0.06))
        cue(self, "This chart")
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "With one neighbour, the model copies every chance high and low in the training data.
        # Its error on the training stations is zero,"
        cue(self, "Its error on")
        self.play(Create(lines["training"]), FadeIn(names["training"]), run_time=self.share(0.1))
        # "but on the validation sites, held back to choose between settings, it is at its worst."
        cue(self, "but on the validation")
        self.play(Create(lines["validation"]), FadeIn(names["validation"]), run_time=self.share(0.1))
        cue(self, "it is at its worst")
        self.play(Create(ring), run_time=self.share(0.04))
        # "This is overfitting: learning the noise along with the pattern."
        cue(self, "This is overfitting")
        self.play(FadeIn(overfit, shift=0.2 * UP), run_time=self.share(0.06))
        # "With hundreds of neighbours, every prediction blurs into one average."
        cue(self, "With hundreds")
        self.play(FadeIn(blur, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


def neighbours_head():
    return label("the error, a typical miss, for each number of neighbours", 34, INK, weight=BOLD).to_edge(UP, buff=0.5)


class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Page results: nearest-neighbours.qmd#fig-neighbours, the best number of neighbours.
        table, chart, lines, names = neighbours_layout(self)
        self.add(chart.frame, *lines.values(), *names.values(), neighbours_head())
        best = table.loc[table["validation"].idxmin()]
        x = np.log10(best["k"])
        mark = DashedLine(chart.p(x, 0), chart.p(x, 5.5), color=GREY, stroke_width=4)
        lowest = plated(label(f"lowest at {int(best['k'])}", 30, ORANGE, weight=BOLD)).next_to(chart.p(x, 3.3), RIGHT, 0.2)
        rule = card("a hyperparameter: chosen on validation data", PURPLE, 28).move_to(chart.p(1.25, 1.6))
        # "In between, the validation error is lowest at 30 neighbours."
        cue(self, "is lowest")
        self.play(Create(mark), FadeIn(lowest), run_time=self.share(0.1))
        # "A setting like k, which we fix before the model is fitted, is called a hyperparameter."
        cue(self, "is called")
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=self.share(0.1))
        # "It is chosen on validation data, never on the training data, where one neighbour always looks perfect."
        cue(self, "never on")
        self.play(Indicate(lines["validation"], color=ORANGE, scale_factor=1.0), run_time=self.share(0.1))
        self.finish()


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
    return nodes, levels, (q1, q2, q3, cold, band, warm, rich)


class Scene16(VideoScene):
    number = 16

    def construct(self):
        # Page results: decision-trees.qmd#fig-tree, the top of the depth-3 tree.
        nodes, levels, (q1, q2, q3, cold, band, warm, rich) = tree_layout(self)
        name = label("a decision tree", 44, GREEN, weight=BOLD).to_corner(UL, buff=0.6)
        note = label("leaf: a final group, predicting the average count of its stations", 30, SUBDUED).to_edge(DOWN, buff=0.5)
        # "A decision tree, also met in the introduction, works differently."
        self.play(FadeIn(name, shift=0.2 * RIGHT), run_time=self.share(0.06))
        # "It asks yes-or-no questions about the inputs, one after another, like an identification key."
        cue(self, "It asks")
        self.play(FadeIn(levels[0], shift=0.2 * DOWN), run_time=self.share(0.06))
        for level in levels[1:]:
            self.play(FadeIn(level, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "Each final group, called a leaf, predicts the average count of the training stations that reach it."
        cue(self, "Each final group")
        self.play(*[Indicate(leaf[1], color=GREEN) for leaf in (cold, band, warm, rich)], FadeIn(note),
                  run_time=self.share(0.1))
        # "Here, the first question is about chlorophyll, and the next two are about temperature."
        cue(self, "Here, the first")
        self.play(Indicate(q1[2], color=BLUE), run_time=self.share(0.06))
        cue(self, "and the next two")
        self.play(Indicate(q2[2], color=BLUE), Indicate(q3[2], color=BLUE), run_time=self.share(0.06))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        # Page results: decision-trees.qmd, the temperature band.
        nodes, levels, (q1, q2, q3, cold, band, warm, rich) = tree_layout(self)
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
        # "For most stations, those two questions about temperature find a band, from 6.4 to 10.4 degrees,"
        cue(self, "two questions")
        self.play(Indicate(q2[2], color=BLUE), Indicate(q3[2], color=BLUE), run_time=self.share(0.15))
        cue(self, "find a band")
        self.play(FadeIn(chart.axes.x_axis), FadeIn(chart.ticks), Create(steps), run_time=self.share(0.15))
        # "with the most animals."
        cue(self, "with the most")
        self.play(Indicate(band[1], color=GREEN), Indicate(steps[1], color=GREEN), run_time=self.share(0.1))
        # "A peak takes one question for each side."
        cue(self, "A peak")
        self.play(Create(risers), FadeIn(peak), run_time=self.share(0.1))
        self.finish()


def step_chart(x_max=20, y_max=6.5, y_ticks=(0, 2, 4, 6)):
    return Chart([0, x_max, 1], [0, y_max, 1], 10.5, 5.0, x_ticks=range(0, x_max + 1, 5), y_ticks=y_ticks,
                 x_name="temperature (°C)", y_name="predicted count", centre=(0.5, -0.45, 0))


class Scene18(VideoScene):
    number = 18

    def construct(self):
        # Page results: decision-trees.qmd#fig-depth.
        depths = self.data("depths")
        best = int(depths.loc[depths["validation"].idxmin(), "depth"])
        chart = Chart([0.5, 15.5, 1], [0, 5.5, 1], 10.5, 5.0, x_ticks=(1, 5, 10, 15), y_ticks=(0, 2, 4),
                      x_name="tree depth", y_name="error (RMSE)", centre=(0.5, -0.45, 0))
        train = chart.line(depths["depth"], depths["training"], BLUE)
        valid = chart.line(depths["depth"], depths["validation"], ORANGE)
        names = VGroup(plated(label("training stations", 28, BLUE, weight=BOLD)).move_to(chart.p(13, 2.4)),
                       plated(label("validation sites", 28, ORANGE, weight=BOLD)).next_to(chart.p(13, 4.6), DOWN, 0.1))
        mark = DashedLine(chart.p(best, 0), chart.p(best, 5.5), color=GREY, stroke_width=4)
        lowest = plated(label(f"lowest at depth {best}", 30, ORANGE, weight=BOLD)).next_to(chart.p(best, 5.2), RIGHT, 0.2)
        head = label("depth: the number of questions in a row", 36, INK, weight=BOLD).to_edge(UP, buff=0.5)
        rule = card("depth:\na hyperparameter", PURPLE, 28).move_to(chart.p(8.4, 0.75))
        # "How deep should a tree grow?"
        self.play(FadeIn(chart.frame), run_time=self.share(0.06))
        # "Its depth, the number of questions in a row, is a hyperparameter too."
        cue(self, "Its depth")
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.06))
        cue(self, "is a hyperparameter")
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=self.share(0.06))
        # "A deeper tree fits the training stations ever more closely,"
        cue(self, "A deeper tree")
        self.play(Create(train), FadeIn(names[0]), run_time=self.share(0.14))
        # "but on the validation sites the error is lowest at depth 5, then climbs: overfitting again."
        cue(self, "but on the validation")
        self.play(Create(valid), FadeIn(names[1]), run_time=self.share(0.12))
        cue(self, "lowest at depth")
        self.play(Create(mark), FadeIn(lowest), run_time=self.share(0.06))
        self.finish()


# Schematic: which of eight made-up stations a resample draws, some twice, some not at all.
RESAMPLE = [0, 2, 2, 3, 5, 6, 6, 6]
STATION_COLOURS = [BLUE, ORANGE, GREEN, SKY, PURPLE, VERMILION, YELLOW, GREY]


class Scene19(VideoScene):
    number = 19

    def construct(self):
        # Page results: forests-and-boosting.qmd, the first question of six resampled trees.
        values = list(self.data("first-questions")["threshold"])
        head = label("one tree is unstable", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        first = label("the first question of six resampled trees", 40, INK, weight=BOLD).move_to(head)
        chips = VGroup(*[card(f"chlorophyll < {v:g}", BLUE, 26) for v in values]).arrange_in_grid(2, 3, buff=(0.4, 0.35))
        chips.next_to(head, DOWN, 0.5)

        def stations(indices):
            return VGroup(*[Square(0.42, stroke_width=0, fill_color=STATION_COLOURS[i], fill_opacity=0.9)
                            for i in indices]).arrange(RIGHT, buff=0.18)

        original, drawn = stations(range(8)), stations(RESAMPLE)
        rows = VGroup(VGroup(label("training stations", 26, SUBDUED), original).arrange(RIGHT, buff=0.4),
                      VGroup(label("a resample", 26, SUBDUED), drawn).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to([0, -1.6, 0])
        note = label("drawn at random: some twice, some not at all", 26, PURPLE, weight=BOLD).next_to(rows, DOWN, 0.3)
        resample = VGroup(rows, note)
        line = NumberLine(x_range=[0, 14, 2], length=11, color=GRID, include_numbers=False, stroke_width=4)
        line.move_to([0, -2.3, 0])
        ticks = VGroup(*[label(f"{v}", 24, SUBDUED).next_to(line.n2p(v), DOWN, 0.2) for v in range(0, 15, 2)])
        name = label("chlorophyll threshold", 26, SUBDUED).next_to(ticks, DOWN, 0.15)
        marks = VGroup(*[Triangle(color=BLUE, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI)
                         .next_to(line.n2p(v), UP, 0.05) for v in values])
        span = BraceBetweenPoints(line.n2p(min(values)) + 0.5 * UP, line.n2p(max(values)) + 0.5 * UP, UP, color=VERMILION)
        span_name = label(f"from {min(values):g} to {max(values):g}", 32, VERMILION, weight=BOLD).next_to(span, UP, 0.1)
        # "One tree is also unstable: a small change in the data can change it a lot."
        self.play(FadeIn(head), run_time=self.share(0.06))
        # "To see this, grow it on six resamples."
        cue(self, "grow it on six")
        self.play(ReplacementTransform(head, first), LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.2),
                  run_time=self.share(0.12))
        # "A resample draws the same number of stations at random from the training data,
        # so some come twice and some not at all."
        cue(self, "A resample")
        self.play(FadeIn(rows[0]), run_time=self.share(0.05))
        cue(self, "at random")
        self.play(FadeIn(rows[1][0]), *[TransformFromCopy(original[i], d) for i, d in zip(RESAMPLE, drawn)],
                  run_time=self.share(0.1))
        cue(self, "so some come")
        self.play(FadeIn(note, shift=0.1 * UP), run_time=self.share(0.05))
        # "The first question is always about chlorophyll,"
        cue(self, "The first question")
        self.play(FadeOut(resample), *[Indicate(c[1], color=VERMILION, scale_factor=1.1) for c in chips],
                  run_time=self.share(0.07))
        # "but its threshold moves from 2.57 to 12.6."
        cue(self, "but its threshold")
        self.play(FadeIn(line), FadeIn(ticks), FadeIn(name), *[TransformFromCopy(c, m) for c, m in zip(chips, marks)],
                  run_time=self.share(0.08))
        self.play(GrowFromCenter(span), FadeIn(span_name), run_time=self.share(0.06))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        # Page results: forests-and-boosting.qmd, thirty of the 400-tree forest's trees and their average.
        trees = self.data("forest-trees")
        forest = self.data("forest-average")
        span = self.data("forest-range").iloc[0]
        chart = step_chart(20, 18.5, (0, 5, 10, 15))
        shades = VGroup(chart.shade(0, span["low"]), chart.shade(span["high"], 20))
        thin = VGroup(*[chart.line(g["temperature_c"], g[".pred"], ORANGE, 2.5).set_stroke(opacity=0.35)
                        for _, g in trees.groupby("tree")])
        average = chart.line(forest["temperature_c"], forest[".pred"], VERMILION, 9)
        names = VGroup(plated(label("30 of its trees", 30, ORANGE, weight=BOLD)).next_to(chart.p(13, 16), RIGHT, 0.1),
                       card("the forest: their average", VERMILION, 28).move_to(chart.p(15.5, 9)))
        head = label("a random forest", 40, VERMILION, weight=BOLD).to_edge(UP, buff=0.4)
        gloss = label("hundreds of trees, each on its own resample, then averaged", 28, SUBDUED).next_to(head, DOWN, 0.2)
        # "A random forest puts this to use."
        self.play(FadeIn(chart.frame), FadeIn(shades), FadeIn(head), run_time=self.share(0.06))
        # "It grows hundreds of trees, each on its own resample, and each question chooses from a few
        # inputs picked at random, so the trees differ."
        cue(self, "It grows")
        self.play(LaggedStart(*[Create(t) for t in thin], lag_ratio=0.08), FadeIn(names[0]), FadeIn(gloss),
                  run_time=self.share(0.4))
        # "Then it averages their predictions."
        cue(self, "Then it averages")
        self.play(thin.animate.set_stroke(opacity=0.18), Create(average), FadeIn(names[1]), run_time=self.share(0.12))
        # "The big jumps of single trees shrink into small steps."
        cue(self, "The big jumps")
        self.play(Indicate(average, color=VERMILION, scale_factor=1.0), run_time=self.share(0.08))
        self.finish()


def small_tree(colour=GREEN, scale=1.0):
    top = Dot([0, 0.35, 0], 0.1, color=colour)
    left, right = Dot([-0.35, -0.25, 0], 0.1, color=colour), Dot([0.35, -0.25, 0], 0.1, color=colour)
    return VGroup(Line(top.get_center(), left.get_center(), color=colour, stroke_width=4),
                  Line(top.get_center(), right.get_center(), color=colour, stroke_width=4), top, left, right).scale(scale)


class Scene21(VideoScene):
    number = 21

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
        # "Boosting also combines many trees, but in a different way. It adds small trees one after another."
        self.play(FadeIn(start), run_time=self.share(0.06))
        cue(self, "It adds small")
        self.play(FadeIn(head), run_time=self.share(0.06))
        # "Each new tree is fitted to the errors left by the trees before it, so it corrects them
        # a little at a time."
        cue(self, "Each new tree")
        for arrow, words, box in zip(arrows, errors, boxes[1:]):
            self.play(GrowArrow(arrow), FadeIn(words), FadeIn(box, shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "The prediction is the sum of all the trees."
        cue(self, "The prediction is")
        self.play(FadeIn(total, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene22(VideoScene):
    number = 22

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
        names = VGroup(plated(label("random forest", 30, GREEN, weight=BOLD)).next_to(chart.p(2.3, 3.72), DOWN, 0.2),
                       plated(label("boosting", 30, PURPLE, weight=BOLD)).next_to(chart.p(3.05, 3.97), UP, 0.25))
        best_name = plated(label(f"best at {int(best['trees'])} trees", 30, PURPLE, weight=BOLD)).next_to(mark, UP, 0.5)
        noise = card("later trees fit the noise", PURPLE, 28).move_to(chart.p(2.6, 4.45))
        hyper = card("for boosting, the number of trees:\na hyperparameter", PURPLE, 28).move_to(noise)
        # "More trees never hurt a forest: its validation error stays flat."
        self.play(FadeIn(chart.frame), run_time=self.share(0.06))
        self.play(Create(lines["forest"]), FadeIn(dots["forest"]), FadeIn(names[0]), run_time=self.share(0.15))
        # "Boosting is different. On the validation sites, it does best at 200 trees,"
        cue(self, "Boosting is different")
        self.play(Create(lines["boosting"]), FadeIn(dots["boosting"]), FadeIn(names[1]), run_time=self.share(0.15))
        cue(self, "at 200")
        self.play(Create(mark), FadeIn(best_name), run_time=self.share(0.08))
        # "then gets worse, as the later trees fit the noise."
        cue(self, "then gets worse")
        self.play(FadeIn(noise, shift=0.2 * UP), run_time=self.share(0.06))
        # "So for boosting, the number of trees is a hyperparameter."
        cue(self, "So for boosting")
        self.play(ReplacementTransform(noise, hyper), run_time=self.share(0.06))
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
        # "Finally, how to choose between these methods. Five questions narrow the choice before any
        # model is fitted."
        cue(self, "Five questions")
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "What is the aim: to predict, or to explain? What kind of outcome is it? Must the model predict
        # beyond the range of the data? How much data is there? And who must accept the result?"
        for c, phrase in zip(cards, ["What is the aim", "What kind", "Must the model", "How much", "And who"]):
            cue(self, phrase)
            self.play(FadeIn(c, shift=0.2 * UP), run_time=self.share(0.05))
        self.finish()


# The choosing page's labels, as they read mid-sentence on screen.
METHOD_NAMES = {"k-nearest neighbours": "k-nearest neighbours", "Poisson regression": "Poisson regression",
                "Polynomial regression": "polynomial regression", "Linear regression": "linear regression",
                "Random forest": "random forest", "Boosting": "boosting", "Decision tree": "decision tree"}


def comparison_layout(scene):
    table = scene.data("comparison")          # already ordered by test RMSE
    chart = Chart([3.4, 4.6, 0.2], [0, len(table) + 2, 1], 7.6, 5.2, x_ticks=(3.5, 4.0, 4.5),
                  x_name="error on new sites: the typical miss (RMSE)", centre=(2.2, -0.2, 0))
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
        counts = SurroundingRectangle(rows[order[0]][1], color=GREEN, buff=0.12,
                                      corner_radius=0.1)
        trees = SurroundingRectangle(VGroup(*[rows[m][1] for m in order[-3:]]), color=ORANGE, buff=0.12,
                                     corner_radius=0.1)
        few = card("a few hundred noisy stations", PURPLE, 28).move_to(chart.p(4.15, 8.1))
        lower = card("lower is better", BLUE, 28).move_to(few)
        # "Here, all seven models were scored on the same test sites, with the typical miss: lower is better."
        self.play(FadeIn(VGroup(chart.axes.x_axis, chart.ticks, chart.x_name)), FadeIn(guides), FadeIn(key[0]),
                  FadeIn(VGroup(*[rows[m][1] for m in order])), run_time=self.share(0.12))
        self.play(LaggedStart(*[FadeIn(rows[m][2], scale=0.5) for m in order], lag_ratio=0.15),
                  run_time=self.share(0.15))
        cue(self, "lower is better")
        self.play(FadeIn(lower, shift=0.2 * UP), Indicate(chart.x_name, color=BLUE, scale_factor=1.05),
                  run_time=self.share(0.06))
        # "Poisson regression comes first, and the three tree models last."
        cue(self, "Poisson regression comes")
        self.play(Create(counts), run_time=self.share(0.08))
        cue(self, "and the three")
        self.play(Create(trees), run_time=self.share(0.08))
        # "A few hundred noisy stations are too few for the flexible methods to beat a simple curve."
        cue(self, "A few hundred")
        self.play(ReplacementTransform(lower, few), run_time=self.share(0.08))
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
        tuned = card("tuned on these sites: a kind of overfitting", VERMILION, 28).move_to(chart.p(4.0, 8.1))
        close = card("one split cannot separate close models", PURPLE, 28).move_to(tuned)
        # "On the validation sites, though, the single tree came first."
        self.play(FadeIn(key[1]), *[Create(rows[m][4]) for m in order], *[FadeIn(rows[m][3], scale=0.5) for m in order],
                  run_time=self.share(0.12))
        cue(self, "the single tree")
        self.play(Create(ring), FadeIn(first), run_time=self.share(0.06))
        # "Its depth, and boosting's number of trees, were chosen on those same sites, so they were
        # tuned to those sites' chance patterns: a kind of overfitting."
        cue(self, "Its depth")
        self.play(*[rows[m][4].animate.set_color(VERMILION) for m in ("Decision tree", "Boosting")],
                  *[Indicate(rows[m][1], color=VERMILION) for m in ("Decision tree", "Boosting")], run_time=self.share(0.08))
        cue(self, "so they were")
        self.play(FadeIn(tuned, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "The test sites, kept apart until the end, show the cost."
        cue(self, "The test sites")
        self.play(*[Indicate(rows[m][2], color=BLUE, scale_factor=1.6) for m in ("Decision tree", "Boosting")],
                  run_time=self.share(0.08))
        # "And one split cannot reliably tell apart models whose scores are close."
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
    head = label("extrapolation: predicting beyond the data", 36, INK, weight=BOLD).to_edge(UP, buff=0.5)
    return chart, VGroup(shades, zero, beyond), curves, names, head


class Scene27(VideoScene):
    number = 27

    def construct(self):
        # Page results: choosing-a-method.qmd#fig-extrapolate.
        chart, backdrop, curves, names, head = beyond_layout(self)
        # "The models also differ beyond the data."
        self.play(FadeIn(chart.frame), FadeIn(backdrop), run_time=self.share(0.06))
        # "Predicting outside the range of the data is called extrapolation."
        cue(self, "is called")
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "Beyond the sampled temperatures, each model follows its own rule."
        cue(self, "Beyond the sampled")
        self.play(*[Create(c) for c in curves.values()], run_time=self.share(0.14))
        # "The forest stays level, Poisson regression flattens towards zero, and linear regression falls below zero."
        for key, phrase in [("forest", "The forest"), ("poisson", "Poisson regression"), ("line", "and linear")]:
            cue(self, phrase)
            self.play(FadeIn(names[key]), Indicate(curves[key], color=curves[key].get_color(), scale_factor=1.0),
                      run_time=self.share(0.1))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        # Page results as in scene 27, with the page's conclusion over them.
        chart, backdrop, curves, names, head = beyond_layout(self)
        self.add(chart.frame, backdrop, *curves.values(), *names.values(), head)
        nothing = card("nothing in the data says which is right", VERMILION, 34).move_to([0, 0.8, 0])
        defend = card("choose an assumption you can defend, and say it", PURPLE, 34).move_to([0, -0.6, 0])
        dimmed = VGroup(chart.frame, backdrop, *curves.values(), *names.values(), head)
        # "Nothing in the data says which is right, because there are no data there."
        self.play(dimmed.animate.fade(0.75), FadeIn(nothing, shift=0.2 * DOWN), run_time=self.share(0.15))
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
        # Schematic: a line set to zero where it falls below, the model beneath unchanged, then a count model.
        answer = label("No", 64, VERMILION, weight=BOLD).to_edge(UP, buff=0.5)
        chart = Chart([0, 10, 1], [-2, 6, 1], 9.0, 4.2, x_name="an input", y_name="predicted count", centre=(0.4, -0.6, 0))
        zero = chart.hline(0)
        xs = np.linspace(0, 10, 50)
        line = chart.line(xs, 5 - 0.65 * xs, BLUE)
        below = chart.line(xs[xs > 7.6], (5 - 0.65 * xs)[xs > 7.6], BLUE).set_stroke(opacity=0.35)
        clipped = chart.line(xs[xs > 7.6], 0 * xs[xs > 7.6], BLUE, 8)
        hidden = label("set to zero: the symptom hidden", 28, BLUE, weight=BOLD).next_to(chart.p(7.4, 0), UP, 0.35)
        still = label("the model still allows it", 26, SUBDUED).next_to(chart.p(9.3, -1.5), LEFT, 0.2)
        count = chart.line(xs, 5 * np.exp(-0.32 * xs), GREEN)
        count_name = card("a count model: never below zero", GREEN, 30).move_to(chart.p(5.3, 4.9))
        # "No."
        self.play(FadeIn(answer, scale=0.9), FadeIn(chart.frame), FadeIn(zero), Create(line), run_time=self.share(0.12))
        # "Setting them to zero hides the symptom,"
        cue(self, "Setting them")
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
