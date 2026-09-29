"""Manim scenes for the supervised learning video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/03-supervised-learning
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


PROMISES = ["Why the response decides the model",
            "Why a probability is not a decision",
            "Why the most powerful method can come last"]
ANSWERS = ["Match the model\nto what the\nresponse is",
           "The model ranks;\nthe threshold is\nyour decision",
           "Flexibility is paid\nfor with data\nand signal"]
RECAP = ["Match the model to what the response is",
         "A probability is not a decision: choose the threshold",
         "Flexibility costs data: choose by the question"]

# Stated in the pages' prose rather than computed: the example coefficient that
# linear-and-polynomial-regression.qmd turns into a multiplier, and the example of a
# near miss on regression-and-classification.qmd.
EXAMPLE_COEFFICIENT, EXAMPLE_MULTIPLIER = 0.35, 1.42
NEAR_MISS = (11, 12)

FAMILY_COLOURS = {"Parametric": BLUE, "Tree-based": GREEN}
MODEL_COLOURS = {"Linear": GREY, "Polynomial": ORANGE, "Poisson + polynomial": BLUE}


class Scene01(LearnScene):
    number = 1


# Helpers ----------------------------------------------------------------------------------

def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name, size=24,
          x_format="{:g}", y_format="{:g}"):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
    axes = plain_axes(x_range, y_range, x_length, y_length)
    tx = VGroup(*[label(x_format.format(v), size, SUBDUED).next_to(axes.c2p(v, y_range[0]), DOWN, 0.15)
                  for v in x_ticks])
    ty = VGroup(*[label(y_format.format(v), size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15)
                  for v in y_ticks])
    xn = label(x_name, 26, SUBDUED).next_to(tx if len(tx) else axes, DOWN, 0.2) if x_name else VGroup()
    yn = label(y_name, 26, SUBDUED).rotate(PI / 2).next_to(ty if len(ty) else axes, LEFT, 0.2) \
        if y_name else VGroup()
    return axes, VGroup(axes, tx, ty, xn, yn)


def strike(mobject, colour=VERMILION):
    return Line(mobject.get_left() + 0.1 * LEFT, mobject.get_right() + 0.1 * RIGHT, color=colour,
                stroke_width=6)


def card(text, colour=PURPLE, size=40):
    words = VGroup(*[label(t, size, colour, weight=BOLD) for t in text.split("\n")]).arrange(DOWN, buff=0.15)
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


def fixed(value, digits=2):
    """A number to `digits` places, rounded half up as the pages' prose rounds 4.755 to 4.76."""
    return f"{Decimal(str(value)).quantize(Decimal(1).scaleb(-digits), ROUND_HALF_UP)}"


def percent(value, digits=1):
    return f"{Decimal(str(100 * value)).quantize(Decimal(1).scaleb(-digits), ROUND_HALF_UP)}%"


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


def hbar(axes, y, value, colour, height=0.5, start=0):
    left, right = axes.c2p(start, y), axes.c2p(value, y)
    return Rectangle(width=max(right[0] - left[0], 0.001), height=height, stroke_width=0, fill_color=colour,
                     fill_opacity=1).move_to(left, aligned_edge=LEFT)


def mini_tree(colour=GREEN, scale=1.0):
    """Schematic: a small tree, a root and four leaves."""
    root = Dot([0, 0.45, 0], radius=0.09, color=colour)
    mids = [Dot([x, 0, 0], radius=0.08, color=colour) for x in (-0.3, 0.3)]
    leaves = [Dot([x, -0.45, 0], radius=0.07, color=colour) for x in (-0.45, -0.15, 0.15, 0.45)]
    lines = [Line(root.get_center(), m.get_center(), color=colour, stroke_width=3) for m in mids]
    lines += [Line(mids[i // 2].get_center(), leaf.get_center(), color=colour, stroke_width=3)
              for i, leaf in enumerate(leaves)]
    return VGroup(*lines, root, *mids, *leaves).scale(scale)


def flat_layout(position=ORIGIN, width=8.0):
    """Schematic: stations inside a sampled range, a tree's steps through them, flat beyond."""
    axes = plain_axes([0, 10, 1], [0, 6, 1], width, 3.6).move_to(position)
    rng = np.random.default_rng(3)
    xs = rng.uniform(0.3, 6.3, 40)
    ys = 1 + 0.55 * xs + rng.normal(0, 0.45, 40)
    dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.05, color=SUBDUED) for x, y in zip(xs, ys)])
    sampled = Rectangle(width=axes.c2p(6.5, 0)[0] - axes.c2p(0, 0)[0], height=3.6, stroke_width=0,
                        fill_color=BLUE, fill_opacity=0.07).move_to(axes.c2p(0, 0), aligned_edge=DL)
    steps = [(0, 1.7), (1.6, 2.4), (3.1, 3.1), (4.6, 3.9), (6.5, 4.3)]
    points = []
    for (x0, y0), (x1, _) in zip(steps, steps[1:] + [(10, 0)]):
        points += [axes.c2p(x0, y0), axes.c2p(min(x1, 6.5), y0)]
    inside = VMobject(color=GREEN, stroke_width=6).set_points_as_corners(points[:-2] + [points[-2]])
    beyond = Line(axes.c2p(6.5, 4.3), axes.c2p(10, 4.3), color=VERMILION, stroke_width=6)
    trend = DashedLine(axes.c2p(6.5, 4.6), axes.c2p(9.8, 6.4), color=GREY, stroke_width=4)
    x_name = label("temperature", 26, SUBDUED).next_to(axes, DOWN, 0.2)
    y_name = label("abundance", 26, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.2)
    in_tag = label("sampled range", 26, BLUE, weight=BOLD).next_to(sampled, UP, 0.1)
    out_tag = label("beyond: flat, forever", 28, VERMILION, weight=BOLD).next_to(beyond, DOWN, 0.25)
    return VGroup(sampled, axes, x_name, y_name, dots, inside, in_tag), beyond, out_tag, trend


# The puzzle (scenes 2–4) ------------------------------------------------------------------

PAGE_ORDER = ["Linear regression", "Polynomial regression", "Poisson regression", "Poisson + polynomial",
              "Lasso + polynomial", "Decision tree (depth 3)", "Decision tree (defaults)", "Random forest",
              "Boosting (gentle)", "Boosting (defaults)"]


def ten_layout(scene):
    """The ten models as chips, in the order the page fits them, coloured by family."""
    models = scene.data("ten-models").set_index("model")
    heading = title("Ten models, one survey", 46).to_edge(UP, buff=0.5)
    chips = VGroup()
    for name in PAGE_ORDER:
        colour = FAMILY_COLOURS[models.loc[name, "family"]]
        box = RoundedRectangle(width=5.2, height=0.72, corner_radius=0.12, stroke_color=colour, stroke_width=3,
                               fill_color=colour, fill_opacity=0.08)
        chips.add(VGroup(box, label(name, 30, INK).move_to(box)))
    chips.arrange_in_grid(rows=5, cols=2, flow_order="dr", buff=(0.9, 0.25)).move_to([0, 0.1, 0])
    return heading, chips


class Scene02(VideoScene):
    number = 2

    def construct(self):
        heading, chips = ten_layout(self)
        test = self.data("three-models")["test_stations"].iloc[0]
        note = label(f"same predictors, same {test} held-back stations", 32, SUBDUED
                     ).to_edge(DOWN, buff=0.6)
        # "Here are ten models, from a straight line to boosted trees."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(c, shift=0.15 * RIGHT) for c in chips], lag_ratio=0.2),
                  run_time=self.share(0.35))
        # "All ten were fitted to the same survey, ... scored on the same 200 held-back stations."
        at(self, 0.55)
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        heading, chips = ten_layout(self)
        self.add(heading, chips)
        boosting = VGroup(chips[8], chips[9])
        ring = SurroundingRectangle(boosting, color=ORANGE, buff=0.15, corner_radius=0.15, stroke_width=5)
        fame = label("wins competitions", 32, ORANGE, weight=BOLD).next_to(ring, DOWN, 0.2).align_to(ring, RIGHT)
        ask = card("Which would you bet on?", PURPLE, 44).to_edge(DOWN, buff=0.25).shift(3.0 * LEFT)
        # "Boosting has the best reputation: it wins competitions."
        self.play(Create(ring), FadeIn(fame), run_time=self.share(0.2))
        # "Which would you bet on?"
        at(self, 0.4)
        self.play(FadeIn(ask, shift=0.2 * UP), run_time=self.share(0.12))
        # "By the end of this video, you will see the winner, and why it won."
        self.finish()


def fork_question():
    return card("What kind of thing is your response?", PURPLE, 44)


class Scene04(VideoScene):
    number = 4

    def construct(self):
        # Schematic.
        heading = title("One question first", 46).to_edge(UP, buff=0.5)
        ask = fork_question()
        # "Every choice follows from one question."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.2))
        # "What kind of thing is your response?"
        at(self, 0.45)
        self.play(FadeIn(ask, scale=0.9), run_time=self.share(0.15))
        self.finish()


# Counts need a count model (scenes 5–17) ---------------------------------------------------

class Scene05(VideoScene):
    number = 5

    def construct(self):
        # Schematic: the two boxes, with the page's example of a near miss.
        ask = fork_question().to_edge(UP, buff=0.5)
        self.add(ask)
        boxes = VGroup()
        for name, what, colour in [("Regression", "predicts a quantity", BLUE),
                                   ("Classification", "predicts a category", ORANGE)]:
            box = RoundedRectangle(width=5.6, height=3.6, corner_radius=0.2, stroke_color=colour, stroke_width=5)
            head = label(name, 40, colour, weight=BOLD).next_to(box.get_top(), DOWN, 0.35)
            sub = label(what, 30, SUBDUED).next_to(head, DOWN, 0.2)
            boxes.add(VGroup(box, head, sub))
        boxes.arrange(RIGHT, buff=1.2).move_to([0, -1.1, 0])
        arrows = VGroup(*[Arrow(ask.get_bottom(), b.get_top(), color=GRID, stroke_width=5, buff=0.15)
                          for b in boxes])
        guess, truth = NEAR_MISS
        near = VGroup(label(f"predict {guess}, truth {truth}", 30, INK),
                      label("nearly right", 32, GREEN, weight=BOLD)).arrange(DOWN, buff=0.2
                                                                            ).next_to(boxes[0][2], DOWN, 0.4)
        right = VGroup(label("right or wrong:", 30, INK),
                       label("close does not count", 32, VERMILION, weight=BOLD)).arrange(DOWN, buff=0.2
                                                                                        ).next_to(boxes[1][2], DOWN, 0.4)
        # "Regression predicts a quantity, and being close counts:"
        self.play(GrowArrow(arrows[0]), FadeIn(boxes[0]), run_time=self.share(0.15))
        # "predicting 11 when the truth is 12 is nearly right."
        at(self, 0.3)
        self.play(FadeIn(near, shift=0.1 * UP), run_time=self.share(0.12))
        # "Classification predicts a category, and close does not count."
        at(self, 0.62)
        self.play(GrowArrow(arrows[1]), FadeIn(boxes[1]), run_time=self.share(0.12))
        at(self, 0.82)
        self.play(FadeIn(right, shift=0.1 * UP), run_time=self.share(0.1))
        self.finish()


def histogram_layout(scene):
    """Individuals caught at each station, as the page's left panel."""
    counts = scene.data("count-histogram")
    top = int(np.ceil(counts["stations"].max() / 50) * 50)
    axes, frame = chart([-0.5, 41, 10], [0, top, 50], 8.4, 4.6, [0, 10, 20, 30, 40], list(range(0, top + 1, 50)),
                        "individuals caught", "stations")
    frame.move_to([-2.2, -0.4, 0])
    step = axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0]
    bars = VGroup(*[vbar(axes, a, n, BLUE, 0.85 * step) for a, n in zip(counts["abundance"], counts["stations"])])
    heading = title("One count per station", 46).to_edge(UP, buff=0.4)
    return heading, frame, axes, bars, counts


def summary(scene):
    return {k: int(v) if float(v).is_integer() else v for k, v in scene.data("count-summary").iloc[0].items()}


class Scene06(VideoScene):
    number = 6

    def construct(self):
        heading, frame, axes, bars, _ = histogram_layout(self)
        stations = summary(self)["stations"]
        n = label(f"{stations} stations", 40, BLUE, weight=BOLD).move_to([4.6, 1.6, 0])
        verdict = card("a number,\nso regression?", PURPLE, 36).move_to([4.6, -0.3, 0])
        # "Our survey counted one species at 800 stations."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.15))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(n),
                  run_time=self.share(0.3))
        # "That is a number, so it is regression. Right in outline, and wrong in the details that matter."
        at(self, 0.5)
        self.play(FadeIn(verdict, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


def stats_panel(scene):
    s = summary(scene)
    rows = VGroup(
        VGroup(label("mean", 32, SUBDUED), label(f"{s['mean_count']:g}", 56, BLUE, weight=BOLD)).arrange(DOWN, buff=0.1),
        VGroup(label("variance", 32, SUBDUED), label(f"{s['variance']:.2f}", 56, VERMILION, weight=BOLD)
               ).arrange(DOWN, buff=0.1))
    rows.arrange(DOWN, buff=0.45).move_to([4.8, 0.9, 0])
    note = VGroup(label("for a Poisson process", 26, SUBDUED), label("they would be equal", 26, SUBDUED)
                  ).arrange(DOWN, buff=0.1).next_to(rows, DOWN, 0.35)
    return rows, note


class Scene07(VideoScene):
    number = 7

    def construct(self):
        heading, frame, axes, bars, _ = histogram_layout(self)
        self.add(heading, frame, bars)
        rows, note = stats_panel(self)
        s = summary(self)
        times = label(f"nearly {s['variance'] / s['mean_count']:.0f} × the mean", 32, VERMILION, weight=BOLD
                      ).next_to(note, DOWN, 0.35)
        # "The mean catch is 3.9 individuals."
        self.play(FadeIn(rows[0], shift=0.2 * LEFT), run_time=self.share(0.12))
        # "The variance is about 23, nearly six times the mean."
        at(self, 0.25)
        self.play(FadeIn(rows[1], shift=0.2 * LEFT), run_time=self.share(0.12))
        self.play(FadeIn(times), run_time=self.share(0.1))
        # "Individuals cluster, so counts vary far more than chance alone predicts."
        at(self, 0.62)
        self.play(FadeIn(note), run_time=self.share(0.12))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        heading, frame, axes, bars, counts = histogram_layout(self)
        rows, note = stats_panel(self)
        self.add(heading, frame, bars, rows)
        s = summary(self)
        zero = bars[0]
        tag = VGroup(label(f"{s['zeros']} stations", 36, VERMILION, weight=BOLD),
                     label(f"{s['zero_pct']:g}% caught nothing", 30, VERMILION)).arrange(DOWN, buff=0.12)
        tag.move_to([4.8, -2.1, 0])
        arrow = Arrow(tag.get_left(), zero.get_right() + 0.3 * RIGHT + 0.3 * DOWN, color=VERMILION,
                      stroke_width=5, buff=0.15)
        # "And nearly a quarter of the stations caught nothing."
        self.play(bars[1:].animate.set_opacity(0.35), zero.animate.set_fill(VERMILION), run_time=self.share(0.15))
        self.play(FadeIn(tag), GrowArrow(arrow), run_time=self.share(0.15))
        # "A smooth model will never reproduce that spike at zero."
        self.finish()


def present_layout(scene):
    s, p = summary(scene), scene.data("present").iloc[0].astype(int)
    axes, frame = chart([0, 2, 1], [0, 700, 100], 4.2, 4.4, [], [0, 200, 400, 600], None, "stations")
    frame.move_to([-3.9, -0.5, 0])
    bars = VGroup(vbar(axes, 0.5, s["zeros"], ORANGE, 1.3), vbar(axes, 1.5, p["present"], ORANGE, 1.3))
    names = VGroup(*[label(t, 32, INK).next_to(axes.c2p(x, 0), DOWN, 0.2) for t, x in [("absent", 0.5),
                                                                                       ("present", 1.5)]])
    values = VGroup(*[label(f"{v}", 30, INK, weight=BOLD).next_to(b, UP, 0.12)
                      for v, b in zip([s["zeros"], p["present"]], bars)])
    heading = title("The same count, as present or absent", 46).to_edge(UP, buff=0.4)
    examples = VGroup()
    for n in [p["smallest"], p["largest"]]:
        word = "individual" if n == 1 else "individuals"
        examples.add(VGroup(label(f"{n} {word}", 36, INK, weight=BOLD), Arrow(ORIGIN, 1.2 * RIGHT, color=GRID,
                                                                             stroke_width=5),
                            label('"present"', 36, ORANGE, weight=BOLD)).arrange(RIGHT, buff=0.3))
    examples.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([3.0, 0.8, 0])
    return heading, VGroup(frame, names), bars, values, examples


class Scene09(VideoScene):
    number = 9

    def construct(self):
        heading, frame, bars, values, examples = present_layout(self)
        # "You could turn the count into presence and absence."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.15))
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], FadeIn(values), run_time=self.share(0.2))
        # "Then a station with one individual and a station with forty are both simply "present"."
        at(self, 0.45)
        self.play(FadeIn(examples[0], shift=0.2 * RIGHT), run_time=self.share(0.12))
        at(self, 0.65)
        self.play(FadeIn(examples[1], shift=0.2 * RIGHT), run_time=self.share(0.12))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        heading, frame, bars, values, examples = present_layout(self)
        self.add(heading, frame, bars, values, examples)
        deleted = label("where is it abundant? deleted", 32, VERMILION, weight=BOLD).next_to(examples, DOWN, 0.5)
        rule = card("Dichotomise only when\nthe decision is binary", PURPLE, 36).move_to([3.0, -2.4, 0])
        # "If your question is where the species is abundant, you have just deleted the answer."
        self.play(FadeIn(deleted), run_time=self.share(0.15))
        # "Dichotomise only when the decision really is binary."
        at(self, 0.6)
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


# The temperature curves (scenes 11–14) and the three models' test results.

def curves_layout(scene):
    curves = scene.data("curves")
    low = np.floor(curves[".pred"].min())
    high = np.ceil(curves[".pred"].max())
    axes, frame = chart([2, 17, 1], [low, high, 1], 6.2, 4.8, [2, 5, 8, 11, 14, 17],
                        [v for v in range(int(low), int(high) + 1) if v % 2 == 0],
                        "temperature (°C)", "predicted abundance")
    frame.move_to([-3.4, -0.4, 0])
    below = Polygon(axes.c2p(2, 0), axes.c2p(17, 0), axes.c2p(17, low), axes.c2p(2, low), stroke_width=0,
                    fill_color=VERMILION, fill_opacity=0.08)
    zero = Line(axes.c2p(2, 0), axes.c2p(17, 0), color=SUBDUED, stroke_width=3)
    impossible = label("impossible below zero", 24, VERMILION).next_to(axes.c2p(2.2, low), UR, 0.1)
    lines = {}
    for model, rows in curves.groupby("model"):
        lines[model] = VMobject(color=MODEL_COLOURS[model], stroke_width=6).set_points_smoothly(
            [axes.c2p(t, p) for t, p in zip(rows["temperature_c"], rows[".pred"])])
    heading = title("Three models, one relationship", 46).to_edge(UP, buff=0.4)
    return heading, VGroup(frame, below, zero, impossible), axes, lines


def three_table(scene):
    """The three models' results, one row each: below zero, lowest prediction, error."""
    models = scene.data("three-models").set_index("model")
    header = VGroup(*[label(t, 24, SUBDUED, weight=BOLD) for t in ["", "below\nzero", "lowest", "RMSE"]])
    xs = [1.9, 4.3, 5.4, 6.5]
    rows = VGroup()
    for i, name in enumerate(["Linear", "Polynomial", "Poisson + polynomial"]):
        r = models.loc[name]
        cells = VGroup(label(name if name != "Poisson + polynomial" else "Poisson +\npolynomial", 26,
                             MODEL_COLOURS[name], weight=BOLD),
                       label(f"{r['impossible_predictions']:.0f}", 30, VERMILION if r["impossible_predictions"] else GREEN,
                             weight=BOLD),
                       label(f"{r['lowest_prediction']:.2f}".replace("-", "−"), 30, INK),
                       label(fixed(r["rmse"]), 30, INK))
        for c, x in zip(cells, xs):
            c.move_to([x, 1.2 - 1.0 * i, 0])
        cells[0].align_to([0.4, 0, 0], LEFT)
        rows.add(cells)
    for c, x in zip(header, xs):
        c.move_to([x, 2.1, 0])
    test = models["test_stations"].iloc[0]
    note = label(f"on {test} test stations", 26, SUBDUED).move_to([3.6, -1.9, 0])
    return header, rows, note, models


class Scene11(VideoScene):
    number = 11

    def construct(self):
        heading, frame, axes, lines = curves_layout(self)
        poly = lines["Polynomial"]
        name = label("ordinary regression,\nwith a curve", 30, ORANGE, weight=BOLD).move_to([3.4, 1.0, 0])
        dive = label("dives below zero", 32, VERMILION, weight=BOLD).move_to([3.4, -1.5, 0])
        # "So keep the count, and fit ordinary regression with a curve for the thermal optimum."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.15))
        self.play(FadeIn(name), run_time=self.share(0.1))
        # "It finds the optimum, then dives below zero in warm water."
        at(self, 0.5)
        self.play(Create(poly), run_time=self.share(0.3), rate_func=linear)
        self.play(FadeIn(dive), run_time=self.share(0.08))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        heading, frame, axes, lines = curves_layout(self)
        self.add(heading, frame, lines["Polynomial"])
        header, rows, note, _ = three_table(self)
        # "On 200 test stations, it predicts a negative number of fish six times, the lowest about minus 2."
        self.play(FadeIn(header), FadeIn(note), FadeIn(rows[1][0]), run_time=self.share(0.12))
        at(self, 0.3)
        self.play(FadeIn(rows[1][1], scale=0.7), run_time=self.share(0.08))
        at(self, 0.5)
        self.play(FadeIn(rows[1][2]), run_time=self.share(0.08))
        # "Even the straight line manages two."
        at(self, 0.72)
        self.play(Create(lines["Linear"]), FadeIn(rows[0][:3]), run_time=self.share(0.18))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        heading, frame, axes, lines = curves_layout(self)
        header, rows, note, _ = three_table(self)
        self.add(heading, frame, lines["Polynomial"], lines["Linear"], header, note, rows[1][:3], rows[0][:3])
        log = MathTex(r"\log(\hat\mu) = \beta_0 + \beta_1 x + \dots", font_size=40).move_to([3.6, -2.7, 0])
        # "Poisson regression models the logarithm of the expected count."
        self.play(FadeIn(rows[2][0]), FadeIn(log), run_time=self.share(0.15))
        # "An exponential cannot be negative, so impossible predictions become impossible to make."
        at(self, 0.4)
        self.play(Create(lines["Poisson + polynomial"]), run_time=self.share(0.35), rate_func=linear)
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        heading, frame, axes, lines = curves_layout(self)
        header, rows, note, models = three_table(self)
        self.add(heading, frame, *lines.values(), header, note, rows[1][:3], rows[0][:3], rows[2][0])
        best = band(rows[2][3], GREEN, opacity=0.2)
        # "On the same test stations it makes none, its lowest prediction is 0.16,"
        self.play(FadeIn(rows[2][1], scale=0.7), run_time=self.share(0.1))
        at(self, 0.3)
        self.play(FadeIn(rows[2][2]), run_time=self.share(0.1))
        # "and it is also the most accurate of the three."
        at(self, 0.6)
        self.play(*[FadeIn(r[3]) for r in rows], run_time=self.share(0.12))
        self.play(FadeIn(best), Indicate(rows[2][3], color=GREEN), run_time=self.share(0.15))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Schematic, with the page's worked example of a coefficient.
        heading = title("Effects become multipliers", 46).to_edge(UP, buff=0.5)
        log = VGroup(label("log scale", 30, SUBDUED), label(f"+ {EXAMPLE_COEFFICIENT}", 64, BLUE, weight=BOLD)
                     ).arrange(DOWN, buff=0.15).move_to([-3.6, 1.0, 0])
        count = VGroup(label("count scale", 30, SUBDUED), label(f"× {EXAMPLE_MULTIPLIER}", 64, GREEN, weight=BOLD)
                       ).arrange(DOWN, buff=0.15).move_to([3.6, 1.0, 0])
        arrow = Arrow(log.get_right(), count.get_left(), color=INK, stroke_width=5, buff=0.4)
        exp = MathTex(rf"e^{{{EXAMPLE_COEFFICIENT}}}", font_size=48).next_to(arrow, UP, 0.15)
        examples = VGroup(*[label(f"{t}  × {EXAMPLE_MULTIPLIER}", 38, INK) for t in ["two fish", "two hundred fish"]]
                          ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, -1.9, 0])
        # "And its effects become multipliers."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "A coefficient of 0.35 multiplies the expected count by 1.42,"
        at(self, 0.22)
        self.play(FadeIn(log), run_time=self.share(0.1))
        at(self, 0.42)
        self.play(GrowArrow(arrow), FadeIn(exp), FadeIn(count), run_time=self.share(0.12))
        # "whether a station holds two fish or two hundred."
        at(self, 0.7)
        self.play(LaggedStart(*[FadeIn(e, shift=0.2 * RIGHT) for e in examples], lag_ratio=0.5),
                  run_time=self.share(0.2))
        self.finish()


def dispersion_layout(scene):
    d = scene.data("dispersion").iloc[0]
    heading = title("Poisson assumes variance equals mean", 46).to_edge(UP, buff=0.5)
    axes = plain_axes([0, 5, 1], [0, 1, 1], 10, 0.01).move_to([0, 1.1, 0])
    ticks = VGroup(*[label(str(v), 26, SUBDUED).next_to(axes.c2p(v, 0), DOWN, 0.25) for v in range(6)])
    name = label("residual deviance ÷ degrees of freedom", 28, SUBDUED).next_to(ticks, DOWN, 0.25)
    expect = VGroup(Triangle(color=GREEN, fill_opacity=1).scale(0.16).rotate(PI), label("Poisson: near 1", 28, GREEN,
                                                                                       weight=BOLD))
    expect[0].move_to(axes.c2p(1, 0) + 0.3 * UP)
    expect[1].next_to(expect[0], UP, 0.15)
    here = VGroup(Triangle(color=VERMILION, fill_opacity=1).scale(0.16).rotate(PI),
                  label(f"here: {d['ratio']:.2f}", 36, VERMILION, weight=BOLD))
    here[0].move_to(axes.c2p(d["ratio"], 0) + 0.3 * UP)
    here[1].next_to(here[0], UP, 0.15)
    return heading, VGroup(axes, ticks, name), expect, here, d


class Scene16(VideoScene):
    number = 16

    def construct(self):
        heading, scale, expect, here, _ = dispersion_layout(self)
        verdicts = VGroup(label("predictions: fine", 34, GREEN, weight=BOLD),
                          label("p-values: too small", 34, VERMILION, weight=BOLD)).arrange(RIGHT, buff=1.2
                                                                                           ).move_to([0, -2.6, 0])
        # "Poisson assumes the variance equals the mean. Check it: the ratio should be near one,"
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(scale), run_time=self.share(0.15))
        at(self, 0.28)
        self.play(FadeIn(expect, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "and here it is almost four."
        at(self, 0.5)
        self.play(FadeIn(here, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "The predictions survive, but the p-values are too small."
        at(self, 0.68)
        self.play(FadeIn(verdicts[0]), run_time=self.share(0.08))
        at(self, 0.82)
        self.play(FadeIn(verdicts[1]), run_time=self.share(0.08))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        _, _, _, _, d = dispersion_layout(self)
        heading = title("The negative binomial allows for clustering", 46).to_edge(UP, buff=0.5)
        axes, frame = chart([0, 4000, 1000], [0, 2, 1], 8, 2.4, [0, 1000, 2000, 3000, 4000], [], "AIC (lower is better)",
                            None)
        frame.move_to([0.8, -0.3, 0])
        rows = VGroup()
        for i, (name, value, colour) in enumerate([("Poisson", d["aic_poisson"], GREY),
                                                   ("negative binomial", d["aic_negbin"], BLUE)]):
            bar = hbar(axes, 1.5 - i, value, colour, 0.7)
            rows.add(VGroup(bar, label(name, 30, INK, weight=BOLD).next_to(bar, LEFT, 0.25),
                            label(f"{value:.0f}", 30, INK).next_to(bar, RIGHT, 0.2)))
        drop = label(f"{d['aic_poisson'] - d['aic_negbin']:.0f} lower", 36, BLUE, weight=BOLD).to_edge(DOWN, buff=0.8)
        # "The negative binomial adds a parameter for exactly this clustering,"
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), FadeIn(rows[0]), run_time=self.share(0.2))
        # "and the AIC falls by over 900."
        at(self, 0.42)
        self.play(GrowFromEdge(rows[1][0], LEFT), FadeIn(rows[1][1:]), run_time=self.share(0.15))
        self.play(FadeIn(drop), run_time=self.share(0.1))
        # "On real data, that is the model you would report."
        self.finish()


class Scene18(KeyPointScene):
    number, point = 18, 1


# A probability is not a decision (scenes 19–28) --------------------------------------------

def rare(scene):
    return scene.data("rare-scores").iloc[0]


class Scene19(VideoScene):
    number = 19

    def construct(self):
        r = rare(self)
        bands = self.data("depth-bands")
        prevalence = whole_percent(bands["present"].sum() / bands["stations"].sum())
        heading = title(f"A species present at {prevalence} of stations", 46).to_edge(UP, buff=0.5)
        n = int(r["testing"])
        dots = VGroup(*[Dot(radius=0.11, color=GRID) for _ in range(n)]).arrange_in_grid(cols=21, buff=0.2)
        dots.move_to([0, -0.3, 0])
        positives = np.random.default_rng(7).choice(n, int(r["present_in_test"]), replace=False)
        tag = label(f"{int(r['present_in_test'])} of {n} test stations", 38, ORANGE, weight=BOLD
                    ).to_edge(DOWN, buff=0.5)
        # "Now a presence and absence response: a species present at 5% of stations."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "The test set holds 201 stations,"
        at(self, 0.45)
        self.play(FadeIn(dots, lag_ratio=0.005), run_time=self.share(0.2))
        # "and only 11 of them have it."
        at(self, 0.75)
        self.play(*[dots[i].animate.set_color(ORANGE).scale(1.4) for i in positives], FadeIn(tag),
                  run_time=self.share(0.12))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        # Schematic: the logistic curve.
        heading = title("Logistic regression", 46).to_edge(UP, buff=0.5)
        axes, frame = chart([-6, 6, 1], [0, 1, 0.5], 8.5, 4.2, [], [0, 0.5, 1], "the linear predictor (log-odds)",
                            "probability", x_format="{:g}", y_format="{:g}")
        frame.move_to([-0.8, -0.5, 0])
        curve = axes.plot(lambda x: 1 / (1 + np.exp(-x)), color=BLUE, stroke_width=6)
        floor = DashedLine(axes.c2p(-6, 0), axes.c2p(6, 0), stroke_width=3)
        ceiling = DashedLine(axes.c2p(-6, 1), axes.c2p(6, 1), stroke_width=3)
        verdict = card("a probability,\nnot a class", PURPLE, 34).move_to([4.9, -1.6, 0])
        # "Logistic regression models the log-odds, so its output is always a probability between 0 and 1."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), FadeIn(floor), FadeIn(ceiling),
                  run_time=self.share(0.15))
        self.play(Create(curve), run_time=self.share(0.35), rate_func=linear)
        # "It is a probability, not a class."
        at(self, 0.75)
        self.play(FadeIn(verdict, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        r = rare(self)
        heading = title("Accuracy", 46).to_edge(UP, buff=0.5)
        cards = VGroup()
        for name, value, colour in [("the model", r["accuracy"], BLUE), ('always answer "absent"', r["always_absent"],
                                                                         GREY)]:
            box = RoundedRectangle(width=5.4, height=3.0, corner_radius=0.25, stroke_color=colour, stroke_width=5)
            who = label(name, 32, SUBDUED, weight=BOLD).next_to(box.get_top(), DOWN, 0.4)
            val = label(f"{value:.4f}", 90, colour, weight=BOLD).next_to(who, DOWN, 0.3)
            cards.add(VGroup(box, who, val))
        cards.arrange(RIGHT, buff=1.0).move_to([0, 0, 0])
        same = label("identical to four decimal places", 36, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.8)
        # "Its accuracy is 94.5%."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(cards[0]), run_time=self.share(0.2))
        # "Answering "absent" every time is also 94.5%, identical to four decimal places."
        at(self, 0.35)
        self.play(FadeIn(cards[1]), run_time=self.share(0.15))
        at(self, 0.72)
        self.play(FadeIn(same), run_time=self.share(0.1))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        r = rare(self)
        heading = title("The confusion matrix", 46).to_edge(UP, buff=0.5)
        present, n = int(r["present_in_test"]), int(r["testing"])
        predicted_yes = int(r["predicted_present"])
        cells = [[0, predicted_yes - 0], [present, n - present - predicted_yes]]   # rows: predicted yes, no
        grid = VGroup()
        for i in range(2):
            for j in range(2):
                box = Square(1.8, stroke_color=GRID, stroke_width=3).move_to([-0.2 + 1.8 * j, 0.5 - 1.8 * i, 0])
                grid.add(VGroup(box, label(str(cells[i][j]), 54, INK, weight=BOLD).move_to(box)))
        cols = VGroup(*[label(t, 30, SUBDUED, weight=BOLD).next_to(grid[j], UP, 0.2) for j, t in
                        [(0, "present"), (1, "absent")]])
        truth = label("actually", 28, SUBDUED).next_to(cols, UP, 0.15)
        rows = VGroup(*[label(t, 30, SUBDUED, weight=BOLD).next_to(grid[2 * i], LEFT, 0.3) for i, t in
                        [(0, "present"), (1, "absent")]])
        predicted = label("predicted", 28, SUBDUED).rotate(PI / 2).next_to(rows, LEFT, 0.3)
        never = band(VGroup(grid[0], grid[1]), VERMILION, opacity=0.18)
        note = label("never once predicts presence", 36, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.4)
        # "Print the confusion matrix and you see why."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(grid), FadeIn(cols), FadeIn(truth), FadeIn(rows),
                  FadeIn(predicted), run_time=self.share(0.25))
        # "It never once predicts presence. It is the do-nothing baseline."
        at(self, 0.4)
        self.play(FadeIn(never), FadeIn(note), run_time=self.share(0.15))
        self.finish()


def probabilities_layout(scene):
    predictions = scene.data("rare-predictions")
    axes, frame = chart([0, 0.62, 0.1], [0, 2, 1], 10, 3.6, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [],
                        "predicted probability of presence", None)
    frame.move_to([0.6, -0.3, 0])
    rng = np.random.default_rng(11)
    dots = VGroup()
    for p, truth in zip(predictions[".pred_yes"], predictions["rare_species"]):
        y = (1.5 if truth == "yes" else 0.5) + rng.uniform(-0.3, 0.3)
        dots.add(Dot(axes.c2p(p, y), radius=0.06, color=ORANGE if truth == "yes" else BLUE, fill_opacity=0.7))
    names = VGroup(label("present", 28, ORANGE, weight=BOLD).next_to(axes.c2p(0, 1.5), LEFT, 0.25),
                   label("absent", 28, BLUE, weight=BOLD).next_to(axes.c2p(0, 0.5), LEFT, 0.25))
    cut = DashedLine(axes.c2p(0.5, 0), axes.c2p(0.5, 2), color=VERMILION, stroke_width=5)
    cut_tag = label("default threshold", 26, VERMILION, weight=BOLD).next_to(cut, UP, 0.1)
    heading = title("Every test station's probability", 46).to_edge(UP, buff=0.4)
    return heading, VGroup(frame, names), axes, dots, VGroup(cut, cut_tag), predictions


class Scene23(VideoScene):
    number = 23

    def construct(self):
        heading, frame, axes, dots, cut, _ = probabilities_layout(self)
        r = rare(self)
        auc = card(f"ROC AUC {r['roc_auc']:.2f}", GREEN, 38).to_edge(DOWN, buff=0.25).shift(3.5 * RIGHT)
        meaning = label(f"ranks the right station higher {whole_percent(r['roc_auc'])} of the time", 28, GREEN
                        ).next_to(auc, LEFT, 0.4)
        # "Yet it has learned something."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.12))
        self.play(FadeIn(dots, lag_ratio=0.01), run_time=self.share(0.2))
        # "Its ROC AUC is 0.79: given one station with the species and one without, ... 79% of the time."
        at(self, 0.35)
        self.play(FadeIn(auc, shift=0.2 * UP), run_time=self.share(0.1))
        at(self, 0.6)
        self.play(FadeIn(meaning), run_time=self.share(0.1))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        heading, frame, axes, dots, cut, predictions = probabilities_layout(self)
        self.add(heading, frame, dots)
        r = rare(self)
        top = int(predictions[".pred_yes"].idxmax())
        highest = VGroup(label(f"highest: {r['highest']:.3f}", 30, INK, weight=BOLD))
        highest.next_to(dots[top], UP, 0.3)
        gap = DoubleArrow(dots[top].get_center() + 0.15 * RIGHT, [cut[0].get_x(), dots[top].get_y(), 0],
                          color=VERMILION, stroke_width=4, buff=0.05, tip_length=0.2)
        nothing = label("nothing reaches 0.5: nothing called present", 32, VERMILION, weight=BOLD
                        ).to_edge(DOWN, buff=0.4)
        # "The trouble is the default rule, which calls a station present above 0.5."
        self.play(Create(cut[0]), FadeIn(cut[1]), run_time=self.share(0.15))
        # "The highest probability it gives any station is 0.27,"
        at(self, 0.45)
        self.play(Indicate(dots[top], scale_factor=2.5, color=INK), FadeIn(highest), run_time=self.share(0.15))
        # "so nothing is ever called present."
        at(self, 0.75)
        self.play(GrowFromCenter(gap), FadeIn(nothing), run_time=self.share(0.12))
        self.finish()


def thresholds_layout(scene):
    t = scene.data("thresholds")
    present = int(rare(scene)["present_in_test"])
    heading = title("Choosing a threshold", 46).to_edge(UP, buff=0.4)
    xs = [-4.2, -1.6, 1.0, 3.8]
    header = VGroup(*[label(h, 28, SUBDUED, weight=BOLD).move_to([x, 2.2, 0]) for h, x in
                      zip(["threshold", "flagged", f"caught (of {present})", "false alarms"], xs)])
    rows = VGroup()
    for i, r in t.iterrows():
        cells = VGroup(label(f"{r['threshold']:.2f}", 34, INK, weight=BOLD),
                       label(f"{r['stations_flagged']:.0f}", 34, INK),
                       label(f"{r['caught']:.0f}", 34, GREEN, weight=BOLD),
                       label(f"{r['false_alarms']:.0f}", 34, VERMILION))
        for c, x in zip(cells, xs):
            c.move_to([x, 1.4 - 0.75 * i, 0])
        rows.add(cells)
    return heading, header, rows, t


class Scene25(VideoScene):
    number = 25

    def construct(self):
        heading, header, rows, t = thresholds_layout(self)
        index = {round(v, 2): i for i, v in enumerate(t["threshold"])}
        a, b = rows[index[0.15]], rows[index[0.05]]
        # "Lower the threshold."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(header), FadeIn(rows[0]), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(r[0]) for r in rows[1:]], lag_ratio=0.3), run_time=self.share(0.1))
        # "At 0.15 it catches two of the eleven, with eleven false alarms."
        at(self, 0.25)
        self.play(FadeIn(band(a, BLUE, width=9.2)), FadeIn(a[1:]), run_time=self.share(0.12))
        # "At 0.05 it catches eight, with sixty-eight."
        at(self, 0.65)
        self.play(FadeIn(band(b, BLUE, width=9.2)), FadeIn(b[1:]), run_time=self.share(0.12))
        others = [r[1:] for i, r in enumerate(rows) if i not in (index[0.15], index[0.05])]
        self.play(*[FadeIn(o) for o in others], run_time=self.share(0.1))
        self.finish()


class Scene26(VideoScene):
    number = 26

    def construct(self):
        heading, header, rows, t = thresholds_layout(self)
        index = {round(v, 2): i for i, v in enumerate(t["threshold"])}
        a, b = rows[index[0.15]], rows[index[0.05]]
        bands = VGroup(band(a, BLUE, width=9.2), band(b, BLUE, width=9.2))
        self.add(heading, header, rows, bands)
        same = card("The model is the same in every row", PURPLE, 34).to_edge(DOWN, buff=0.25)
        # "There is no best row."
        self.play(VGroup(header, rows, bands).animate.shift(1.6 * LEFT), run_time=self.share(0.1))
        few = label("each flag sends\na vessel: few", 26, BLUE, weight=BOLD).next_to(a, RIGHT, 0.5)
        many = label("a miss costs a protected\nspecies: many", 26, BLUE, weight=BOLD).next_to(b, RIGHT, 0.5)
        # "If each flag sends a vessel out, you want few;"
        at(self, 0.2)
        self.play(FadeIn(few), run_time=self.share(0.1))
        # "if a miss costs a protected species, you want many."
        at(self, 0.45)
        self.play(FadeIn(many), run_time=self.share(0.1))
        # "The model is the same in every row."
        at(self, 0.75)
        self.play(FadeIn(same, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene27(VideoScene):
    number = 27

    def construct(self):
        odds = self.data("depth-odds").iloc[0]["odds_ratio"]
        heading = title("Reading the coefficients", 46).to_edge(UP, buff=0.5)
        value = VGroup(label("depth: odds ratio", 36, SUBDUED), label(f"{odds:.3f}", 80, INK, weight=BOLD)
                       ).arrange(DOWN, buff=0.2).move_to([-3.4, 1.0, 0])
        seems = label("less likely deeper?", 36, VERMILION, weight=BOLD).next_to(value, DOWN, 0.4)
        levels = VGroup(label("levels:", 32, SUBDUED), label("yes, no", 36, INK, weight=BOLD)
                        ).arrange(RIGHT, buff=0.3).move_to([3.4, 1.3, 0])
        last = VGroup(label("the model describes the last level", 30, INK),
                      label("the odds of absence", 36, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.2
                                                                                  ).next_to(levels, DOWN, 0.5)
        flip = MathTex(rf"1 \div {odds:.3f} = {1 / odds:.3f}", font_size=42).next_to(last, DOWN, 0.5)
        flip_tag = label("per metre, for presence", 26, SUBDUED).next_to(flip, DOWN, 0.15)
        # "One more trap. Depth has an odds ratio of 0.971, as if the species avoided deep water."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(value), run_time=self.share(0.25))
        at(self, 0.35)
        self.play(FadeIn(seems), run_time=self.share(0.1))
        # "But the underlying model describes the odds of the last level: absence."
        at(self, 0.58)
        self.play(FadeIn(levels), FadeIn(last), run_time=self.share(0.15))
        at(self, 0.85)
        self.play(FadeIn(flip), FadeIn(flip_tag), run_time=self.share(0.1))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        bands = self.data("depth-bands")
        heading = title("Prevalence rises with depth", 46).to_edge(UP, buff=0.5)
        top = np.ceil(bands["prevalence"].max() * 10) / 10
        axes, frame = chart([0, 4, 1], [0, top, 0.05], 9, 3.9, [], [], None, "stations with the species")
        frame.move_to([0, -0.1, 0])
        bars, names, values = VGroup(), VGroup(), VGroup()
        for i, r in bands.iterrows():
            bar = vbar(axes, i + 0.5, r["prevalence"], ORANGE, 1.4)
            bars.add(bar)
            low, high = r["depth_band"].strip("(]").split(",")
            names.add(label(f"{low}–{high}", 28, INK).next_to(axes.c2p(i + 0.5, 0), DOWN, 0.2))
            values.add(label(percent(r["prevalence"]), 30, INK, weight=BOLD).next_to(bar, UP, 0.12))
        names.add(label("depth band (m)", 26, SUBDUED).next_to(names, DOWN, 0.2))
        check = label("check one sign against a simple table", 32, PURPLE, weight=BOLD).to_edge(DOWN, buff=0.3)
        # "A simple table settles it: prevalence rises with depth."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), FadeIn(names), run_time=self.share(0.15))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(values),
                  run_time=self.share(0.3))
        # "Check the sign of one coefficient against a cross-tabulation before you publish a direction."
        at(self, 0.55)
        self.play(FadeIn(check, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene29(KeyPointScene):
    number, point = 29, 2


# Flexibility costs data (scenes 30–38) ----------------------------------------------------

def threshold_of(rule):
    """rpart's split label, such as "temperature_c< 6.355", as the value to one decimal."""
    return f"{float(rule.split('<')[-1].split('=')[-1]):.1f}"


def tree_layout(scene):
    """The depth-3 tree's left branch in full, and the high-chlorophyll branch folded."""
    tree = scene.data("tree").set_index("node")

    def node(text, colour, width=3.6):
        words = VGroup(*[label(t, 26, colour, weight=BOLD) for t in text.split("\n")]).arrange(DOWN, buff=0.08)
        box = RoundedRectangle(width=max(width, words.width + 0.4), height=words.height + 0.4, corner_radius=0.15,
                               stroke_color=colour, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1)
        return VGroup(box, words.move_to(box))

    def leaf(n, colour):
        r = tree.loc[n]
        return node(f"expects {r['prediction']:.1f}\n{r['n']} stations", colour, 2.6)

    chl = threshold_of(tree.loc[2, "rule"])
    cold = threshold_of(tree.loc[4, "rule"])
    warm = threshold_of(tree.loc[10, "rule"])
    root = node(f"chlorophyll < {chl}?", INK).move_to([0, 2.5, 0])
    temp = node(f"temperature < {cold} °C?", INK).move_to([-3.2, 0.9, 0])
    high = node(f"higher chlorophyll\n{tree.loc[3, 'n']} stations", GREY).move_to([3.6, 0.9, 0])
    warm_node = node(f"temperature ≥ {warm} °C?", INK).move_to([-0.6, -0.8, 0])
    cold_leaf = leaf(4, BLUE).move_to([-5.2, -0.8, 0])
    warm_leaf = leaf(10, ORANGE).move_to([-2.4, -2.7, 0])
    band_leaf = leaf(11, GREEN).move_to([1.4, -2.7, 0])

    def edge(a, b, word):
        line = Line(a.get_bottom(), b.get_top(), color=GRID, stroke_width=4)
        tag = label(word, 22, SUBDUED).move_to(line.get_center() + 0.3 * (LEFT if b.get_x() < a.get_x() else RIGHT))
        return VGroup(line, tag)

    edges = VGroup(edge(root, temp, "yes"), edge(root, high, "no"), edge(temp, cold_leaf, "yes"),
                   edge(temp, warm_node, "no"), edge(warm_node, warm_leaf, "yes"), edge(warm_node, band_leaf, "no"))
    heading = title("A tree you can read", 46).to_edge(UP, buff=0.3)
    parts = dict(root=root, temp=temp, high=high, warm=warm_node, cold_leaf=cold_leaf, warm_leaf=warm_leaf,
                 band_leaf=band_leaf)
    return heading, parts, edges, (cold, warm)


class Scene30(VideoScene):
    number = 30

    def construct(self):
        heading, p, edges, _ = tree_layout(self)
        # "Now the tree-based methods. A decision tree asks yes or no questions."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.15))
        at(self, 0.25)
        self.play(FadeIn(p["root"]), run_time=self.share(0.1))
        # "This one splits first on chlorophyll, then on temperature."
        at(self, 0.5)
        self.play(Indicate(p["root"], color=INK, scale_factor=1.08), run_time=self.share(0.12))
        self.play(FadeIn(edges[0]), FadeIn(edges[1]), FadeIn(p["temp"]), FadeIn(p["high"]), run_time=self.share(0.12))
        self.play(FadeIn(edges[3]), FadeIn(p["warm"]), run_time=self.share(0.1))
        self.finish()


class Scene31(VideoScene):
    number = 31

    def construct(self):
        heading, p, edges, _ = tree_layout(self)
        self.add(heading, p["root"], p["temp"], p["high"], p["warm"], edges[0], edges[1], edges[3])
        optimum = label("one optimum,\ntwo splits", 32, GREEN, weight=BOLD).move_to([4.8, -2.7, 0])
        # "Below 6.4 degrees it expects 1.4 individuals,"
        self.play(FadeIn(edges[2]), FadeIn(p["cold_leaf"]), run_time=self.share(0.12))
        # "above 10.6 it expects 2.1,"
        at(self, 0.3)
        self.play(FadeIn(edges[4]), FadeIn(p["warm_leaf"]), run_time=self.share(0.12))
        # "and in between, 4.2."
        at(self, 0.55)
        self.play(FadeIn(edges[5]), FadeIn(p["band_leaf"]), run_time=self.share(0.12))
        # "Two splits, to carve out one optimum."
        at(self, 0.72)
        self.play(Indicate(p["band_leaf"], color=GREEN), FadeIn(optimum), run_time=self.share(0.15))
        self.finish()


def sketch(shape, colour):
    """Schematic: a small response curve, a hump or a rise, with the splits a tree needs."""
    axes = plain_axes([0, 4, 1], [0, 3, 1], 3.0, 1.8)
    if shape == "hump":
        curve = axes.plot(lambda x: 0.4 + 2.2 * np.exp(-((x - 2) ** 2) / 0.8), color=colour, stroke_width=5)
        cuts = [1.2, 2.8]
    else:
        curve = axes.plot(lambda x: 0.4 + 2.2 / (1 + np.exp(-2.5 * (x - 2))), color=colour, stroke_width=5)
        cuts = [2.0]
    lines = VGroup(*[DashedLine(axes.c2p(c, 0), axes.c2p(c, 3), color=VERMILION, stroke_width=4) for c in cuts])
    return VGroup(axes, curve), lines


class Scene32(VideoScene):
    number = 32

    def construct(self):
        heading = title("Depth never appears", 46).to_edge(UP, buff=0.5)
        note = label("one of the two strongest drivers, by construction", 30, SUBDUED).next_to(heading, DOWN, 0.3)
        hump, hump_cuts = sketch("hump", ORANGE)
        rise, rise_cuts = sketch("rise", BLUE)
        VGroup(hump, rise).arrange(RIGHT, buff=2.4).move_to([0, -0.5, 0])
        hump_cuts.move_to(hump[0])
        rise_cuts.move_to(rise[0]).align_to(rise[0], DOWN)
        hump_cuts.align_to(hump[0], DOWN)
        tags = VGroup(label("a hump: two splits", 32, ORANGE, weight=BOLD).next_to(hump, DOWN, 0.4),
                      label("a rise: one split", 32, BLUE, weight=BOLD).next_to(rise, DOWN, 0.4))
        greedy = label("a greedy algorithm favours effects that only rise", 32, PURPLE, weight=BOLD
                       ).to_edge(DOWN, buff=0.5)
        # "Depth, one of the strongest drivers, never appears."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(note), run_time=self.share(0.2))
        # "A hump costs a tree two splits,"
        at(self, 0.3)
        self.play(FadeIn(hump), run_time=self.share(0.1))
        self.play(Create(hump_cuts), FadeIn(tags[0]), run_time=self.share(0.1))
        # "so a greedy algorithm favours effects that only rise."
        at(self, 0.6)
        self.play(FadeIn(rise), Create(rise_cuts), FadeIn(tags[1]), run_time=self.share(0.12))
        self.play(FadeIn(greedy), run_time=self.share(0.1))
        self.finish()


class Scene33(VideoScene):
    number = 33

    def construct(self):
        # Schematic: a forest averages varied trees; boosting chains them.
        heading = title("Many trees, two ways", 46).to_edge(UP, buff=0.5)
        forest_trees = VGroup(*[mini_tree(GREEN) for _ in range(5)]).arrange(RIGHT, buff=0.35)
        forest_trees.move_to([-3.6, 0.8, 0])
        mean = card("average", GREEN, 30).move_to([-3.6, -1.4, 0])
        arrows = VGroup(*[Arrow(t.get_bottom(), mean.get_top(), color=GRID, stroke_width=3, buff=0.1,
                                max_tip_length_to_length_ratio=0.1) for t in forest_trees])
        forest_tag = label("random forest", 36, GREEN, weight=BOLD).next_to(forest_trees, UP, 0.5)
        forest_note = label("varied trees, averaged", 28, SUBDUED).next_to(mean, DOWN, 0.3)
        chain = VGroup()
        for i in range(4):
            chain.add(mini_tree(ORANGE, 0.9))
            if i < 3:
                chain.add(Arrow(ORIGIN, 0.6 * RIGHT, color=ORANGE, stroke_width=4, buff=0))
        chain.arrange(RIGHT, buff=0.15).move_to([3.6, 0.8, 0])
        boost_tag = label("boosting", 36, ORANGE, weight=BOLD).next_to(chain, UP, 0.5)
        boost_note = label("each tree fits\nthe last ones' errors", 28, SUBDUED).move_to([3.6, -1.4, 0])
        divider = DashedLine([0, 2.6, 0], [0, -2.6, 0], color=GRID)
        # "A random forest averages hundreds of deliberately varied trees."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(forest_tag), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(t, shift=0.1 * UP) for t in forest_trees], lag_ratio=0.2),
                  run_time=self.share(0.15))
        self.play(*[GrowArrow(a) for a in arrows], FadeIn(mean), FadeIn(forest_note), run_time=self.share(0.12))
        # "Boosting builds trees in sequence, each one fitting what the last ones got wrong."
        at(self, 0.5)
        self.play(Create(divider), FadeIn(boost_tag), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(c, shift=0.1 * RIGHT) for c in chain], lag_ratio=0.3),
                  run_time=self.share(0.2))
        self.play(FadeIn(boost_note), run_time=self.share(0.08))
        self.finish()


FOUR = [("Tree (depth 3)", "tree, depth 3"), ("Tree (defaults)", "tree, defaults"),
        ("Random forest (500)", "random forest"), ("Boosting (500 trees)", "boosting, 500 trees")]


def four_layout(scene):
    models = scene.data("four-models").set_index("model")
    heading = title("Three methods, the same test stations", 46).to_edge(UP, buff=0.4)
    axes, frame = chart([0, 6, 1], [0, 4, 1], 7.8, 5.0, [0, 1, 2, 3, 4, 5, 6], [], "error (RMSE), lower is better",
                        None)
    frame.move_to([1.6, -0.5, 0])
    test_bars, train_bars, names, test_values, train_values = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
    for i, (key, name) in enumerate(FOUR):
        y = 3.5 - i
        r = models.loc[key]
        colour = ORANGE if key.startswith("Boosting") else GREEN
        test_bars.add(hbar(axes, y + 0.14, r["test_rmse"], colour, 0.34))
        train_bars.add(hbar(axes, y - 0.24, r["train_rmse"], colour, 0.34).set_fill(opacity=0.35))
        names.add(label(name, 28, INK, weight=BOLD).next_to(axes.c2p(0, y), LEFT, 0.3))
        test_values.add(label(f"{r['test_rmse']:.2f}", 26, INK, weight=BOLD).next_to(test_bars[-1], RIGHT, 0.12))
        train_values.add(label(f"{r['train_rmse']:.2f}", 24, SUBDUED).next_to(train_bars[-1], RIGHT, 0.12))
    key = VGroup(VGroup(Square(0.25, fill_color=INK, fill_opacity=1, stroke_width=0), label("test", 26, INK)
                        ).arrange(RIGHT, buff=0.15),
                 VGroup(Square(0.25, fill_color=INK, fill_opacity=0.35, stroke_width=0), label("training", 26, INK)
                        ).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.5).next_to(heading, DOWN, 0.25)
    return heading, frame, names, (test_bars, test_values), (train_bars, train_values), key, models


class Scene34(VideoScene):
    number = 34

    def construct(self):
        heading, frame, names, (bars, values), _, key, _ = four_layout(self)
        worst = label("worst by a wide margin", 30, ORANGE, weight=BOLD).next_to(values[3], RIGHT, 0.3)
        if worst.get_right()[0] > 6.9:
            worst.next_to(bars[3], DOWN, 0.1).align_to(bars[3], RIGHT)
        # "Here are all three, on the same test stations."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), FadeIn(names), run_time=self.share(0.15))
        # "Both single trees beat the forest,"
        at(self, 0.3)
        self.play(*[GrowFromEdge(b, LEFT) for b in bars[:3]], FadeIn(values[:3]), run_time=self.share(0.2))
        # "and the boosted model, with 500 trees, is worst by a wide margin."
        at(self, 0.62)
        self.play(GrowFromEdge(bars[3], LEFT), FadeIn(values[3]), run_time=self.share(0.12))
        self.play(FadeIn(worst), run_time=self.share(0.08))
        self.finish()


class Scene35(VideoScene):
    number = 35

    def construct(self):
        heading, frame, names, (bars, values), (train, train_values), key, models = four_layout(self)
        self.add(heading, frame, names, bars, values)
        pair = VGroup(train_values[3], values[3])
        ring = SurroundingRectangle(pair, color=VERMILION, buff=0.12, corner_radius=0.1)
        boosting = models.loc["Boosting (500 trees)"]
        story = card(f"{boosting['train_rmse']:.2f} against {boosting['test_rmse']:.2f}", VERMILION, 34)
        story.to_corner(DL, buff=0.3)
        # "Now its training error: 0.58, roughly seven times better than a tree."
        self.play(FadeIn(key), *[GrowFromEdge(b, LEFT) for b in train], FadeIn(train_values), run_time=self.share(0.25))
        # "It predicts new stations worst of all. That pair of numbers is the whole story."
        at(self, 0.6)
        self.play(Create(ring), run_time=self.share(0.1))
        self.play(FadeIn(story, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def capacity_layout(scene):
    curve = scene.data("capacity")
    curve = curve[curve["method"] == "boosting"]
    heading = title("Boosting, tree by tree", 46).to_edge(UP, buff=0.4)
    trees = sorted(curve["capacity"].unique())
    axes, frame = chart([np.log10(4), np.log10(1000), 1], [0, 6, 1], 9.0, 4.8, [], [0, 2, 4, 6], None, "RMSE")
    frame.move_to([-0.8, -0.3, 0])
    ticks = VGroup(*[label(f"{t}", 24, SUBDUED).next_to(axes.c2p(np.log10(t), 0), DOWN, 0.15) for t in trees])
    frame[1].become(ticks)
    frame[3].become(label("number of trees (log scale)", 26, SUBDUED).next_to(ticks, DOWN, 0.2))
    lines, dots = {}, {}
    for name, colour in [("Training", BLUE), ("Held-out", VERMILION)]:
        rows = curve[curve["data"] == name].sort_values("capacity")
        pts = [axes.c2p(np.log10(c), r) for c, r in zip(rows["capacity"], rows["rmse"])]
        lines[name] = VMobject(color=colour, stroke_width=6).set_points_as_corners(pts)
        dots[name] = VGroup(*[Dot(p, radius=0.07, color=colour) for p in pts])
    tags = VGroup(label("training", 30, BLUE, weight=BOLD).next_to(lines["Training"].get_end(), RIGHT, 0.2),
                  label("held-out", 30, VERMILION, weight=BOLD).next_to(lines["Held-out"].get_end(), RIGHT, 0.2))
    held = curve[curve["data"] == "Held-out"]
    best = held.loc[held["rmse"].idxmin()]
    return heading, frame, axes, lines, dots, tags, best, curve


class Scene36(VideoScene):
    number = 36

    def construct(self):
        heading, frame, axes, lines, dots, tags, best, _ = capacity_layout(self)
        marker = Circle(0.2, color=GREEN, stroke_width=5).move_to(axes.c2p(np.log10(best["capacity"]), best["rmse"]))
        best_tag = label(f"lowest at {best['capacity']:.0f} trees", 28, GREEN, weight=BOLD).next_to(marker, DOWN, 0.3)
        gap = label("the gap: overfitting", 32, PURPLE, weight=BOLD).move_to(axes.c2p(np.log10(300), 3.3))
        # "As trees are added, the training error falls towards zero."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.12))
        self.play(Create(lines["Training"]), FadeIn(dots["Training"]), FadeIn(tags[0]), run_time=self.share(0.2),
                  rate_func=linear)
        # "The held-out error is lowest at 50 trees, then rises."
        at(self, 0.38)
        self.play(Create(lines["Held-out"]), FadeIn(dots["Held-out"]), FadeIn(tags[1]), run_time=self.share(0.2),
                  rate_func=linear)
        self.play(Create(marker), FadeIn(best_tag), run_time=self.share(0.08))
        # "That widening gap is overfitting."
        at(self, 0.8)
        self.play(FadeIn(gap), run_time=self.share(0.08))
        self.finish()


class Scene37(VideoScene):
    number = 37

    def construct(self):
        heading, frame, axes, lines, dots, tags, best, _ = capacity_layout(self)
        self.add(heading, frame, *lines.values(), *dots.values(), tags)
        n = self.data("four-models")["training_stations"].iloc[0]
        note = card(f"about {n} training stations,\nnoisy counts", PURPLE, 30).move_to(axes.c2p(np.log10(25), 1.1))
        learns = label("past that: learning these\nparticular stations", 28, VERMILION, weight=BOLD
                       ).move_to(axes.c2p(np.log10(330), 3.3))
        # "With about 600 training stations and noisy counts, there is only so much signal."
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.15))
        # "Past that, extra flexibility learns these particular stations."
        at(self, 0.55)
        self.play(FadeIn(learns), run_time=self.share(0.12))
        self.finish()


class Scene38(VideoScene):
    number = 38

    def construct(self):
        # Schematic.
        heading = title("Trees cannot extrapolate", 46).to_edge(UP, buff=0.5)
        inside, beyond, out_tag, _ = flat_layout([0, -0.4, 0], 10.0)
        forest = label("a forest of trees is still flat", 30, SUBDUED).to_edge(DOWN, buff=0.35)
        # "And trees cannot extrapolate."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(inside), run_time=self.share(0.2))
        # "Beyond the training data a tree's prediction is flat, constant forever,"
        at(self, 0.3)
        self.play(Create(beyond), run_time=self.share(0.2), rate_func=linear)
        self.play(FadeIn(out_tag), run_time=self.share(0.08))
        # "and a forest of trees is still flat."
        at(self, 0.75)
        self.play(FadeIn(forest), run_time=self.share(0.08))
        self.finish()


# Ten models ranked (scenes 39–43) -------------------------------------------------------

def ranking_layout(scene):
    """The page's dot chart: the ten models by test RMSE, best at the top."""
    results = scene.data("ten-models")
    heading = title("Ten models, ranked", 46).to_edge(UP, buff=0.25)
    axes, frame = chart([4.4, 5.5, 0.2], [0, 10, 1], 7.2, 5.6, [4.4, 4.6, 4.8, 5.0, 5.2, 5.4], [],
                        "test error (RMSE), lower is better", None, x_format="{:.1f}")
    frame.move_to([2.2, -0.35, 0])
    rows = VGroup()
    for i, r in results.iterrows():
        y = 9.5 - i
        colour = FAMILY_COLOURS[r["family"]]
        track = Line(axes.c2p(4.4, y), axes.c2p(r["rmse"], y), color=GRID, stroke_width=10)
        dot = Dot(axes.c2p(r["rmse"], y), radius=0.13, color=colour)
        name = label(r["model"], 26, INK, weight=BOLD if i == 0 else NORMAL).next_to(axes.c2p(4.4, y), LEFT, 0.3)
        value = label(fixed(r["rmse"]), 24, SUBDUED).next_to(dot, RIGHT, 0.15)
        rows.add(VGroup(track, dot, name, value))
    key = VGroup(*[VGroup(Dot(radius=0.1, color=c), label(f.lower(), 26, c, weight=BOLD)).arrange(RIGHT, buff=0.15)
                   for f, c in FAMILY_COLOURS.items()]).arrange(RIGHT, buff=0.5).to_corner(DL, buff=0.45)
    return heading, frame, axes, rows, key, results


class Scene39(VideoScene):
    number = 39

    def construct(self):
        heading, frame, axes, rows, key, results = ranking_layout(self)
        last = band(rows[-1], ORANGE, opacity=0.2)
        first = band(rows[0], BLUE, opacity=0.2)
        # "Back to the ten models."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), FadeIn(key), run_time=self.share(0.12))
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in reversed(rows)], lag_ratio=0.15),
                  run_time=self.share(0.3))
        # "Boosting at its defaults comes last."
        at(self, 0.35)
        self.play(FadeIn(last), run_time=self.share(0.1))
        # "The winner is Poisson regression with two quadratic terms."
        at(self, 0.62)
        self.play(FadeIn(first), Indicate(rows[0][2], color=BLUE), run_time=self.share(0.15))
        self.finish()


class Scene40(VideoScene):
    number = 40

    def construct(self):
        heading, frame, axes, rows, key, results = ranking_layout(self)
        self.add(heading, frame, rows, key)
        negative = [i for i, v in enumerate(results["impossible"]) if v > 0]
        crosses = VGroup(*[cross(0.5, BACKGROUND).set_stroke(width=5).move_to(rows[i][1]) for i in negative])
        tag = VGroup(cross(0.45, VERMILION), label(f"{len(negative)} predicted negative fish", 28, VERMILION,
                                                   weight=BOLD)).arrange(RIGHT, buff=0.2)
        tag.move_to(axes.c2p(5.2, 6.5))
        winner = label("counts, with optima", 28, BLUE, weight=BOLD).next_to(rows[0][3], RIGHT, 0.4)
        # "Four models predicted negative fish."
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in crosses], lag_ratio=0.3), FadeIn(tag),
                  run_time=self.share(0.25))
        # "The winner cannot, because it matches the response: counts, with optima."
        at(self, 0.5)
        self.play(Indicate(rows[0], color=BLUE, scale_factor=1.04), run_time=self.share(0.12))
        at(self, 0.72)
        self.play(FadeIn(winner), run_time=self.share(0.1))
        self.finish()


class Scene41(VideoScene):
    number = 41

    def construct(self):
        heading, frame, axes, rows, key, results = ranking_layout(self)
        self.add(heading, frame, rows, key)
        trees = results[results["family"] == "Tree-based"]["rmse"]
        best_parametric = results[results["family"] == "Parametric"]["rmse"].min()
        spread = VGroup(label("spread within the trees", 26, GREEN, weight=BOLD),
                        label(f"{fixed(trees.min())} to {fixed(trees.max())}", 30, GREEN)).arrange(DOWN, buff=0.08)
        gap = VGroup(label("gap between the best of each", 26, BLUE, weight=BOLD),
                     label(f"{fixed(best_parametric)} to {fixed(trees.min())}", 30, BLUE)).arrange(DOWN, buff=0.08)
        times = (trees.max() - trees.min()) / (trees.min() - best_parametric)
        ratio = card(f"about {times:.0f} ×", PURPLE, 36)
        VGroup(spread, gap, ratio).arrange(DOWN, buff=0.3).move_to(axes.c2p(5.3, 6.4))
        tree_dots = VGroup(*[rows[i][1] for i in results.index[results["family"] == "Tree-based"]])
        # "The spread among the tree-based models is three times the gap between the best of each family."
        self.play(FadeIn(spread), Indicate(tree_dots, color=GREEN, scale_factor=1.6), run_time=self.share(0.15))
        at(self, 0.25)
        self.play(FadeIn(gap), run_time=self.share(0.12))
        self.play(FadeIn(ratio, scale=0.8), run_time=self.share(0.1))
        # "How you configure a method matters more than which family it belongs to."
        self.finish()


class Scene42(VideoScene):
    number = 42

    def construct(self):
        heading, frame, axes, rows, key, results = ranking_layout(self)
        self.add(heading, frame, rows, key)
        test = self.data("three-models")["test_stations"].iloc[0]
        top = SurroundingRectangle(rows[:5], color=PURPLE, buff=0.08, corner_radius=0.12, stroke_width=4)
        hard = label("hard to\nseparate", 28, PURPLE, weight=BOLD).next_to(top, RIGHT, 0.2).align_to(top, UP)
        if hard.get_right()[0] > 6.9:
            hard.shift((hard.get_right()[0] - 6.9) * LEFT)
        once = label(f"one test set\nof {test} stations", 30, SUBDUED, weight=BOLD)
        hypothesis = card("a hypothesis,\nnot a ranking", PURPLE, 32)
        VGroup(once, hypothesis).arrange(DOWN, buff=0.3).move_to(axes.c2p(5.27, 4.0))
        # "This is one test set of 200 stations."
        self.play(FadeIn(once), run_time=self.share(0.12))
        # "The top five are hard to separate, and with far more data the order could reverse."
        at(self, 0.25)
        self.play(Create(top), FadeIn(hard), run_time=self.share(0.12))
        # "Treat it as a hypothesis, not a ranking."
        at(self, 0.75)
        self.play(FadeIn(hypothesis, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene43(VideoScene):
    number = 43

    def construct(self):
        # Schematic: two error bars and the gap between them.
        heading = title("Fit a simple model and a flexible one", 46).to_edge(UP, buff=0.5)
        simple = VGroup(Rectangle(width=1.6, height=3.2, stroke_width=0, fill_color=BLUE, fill_opacity=1),
                        label("simple", 32, BLUE, weight=BOLD))
        flexible = VGroup(Rectangle(width=1.6, height=2.0, stroke_width=0, fill_color=GREEN, fill_opacity=1),
                          label("flexible", 32, GREEN, weight=BOLD))
        for g in (simple, flexible):
            g[1].next_to(g[0], DOWN, 0.25)
        simple[0].move_to([-4.2, -1.8, 0], aligned_edge=DOWN)
        flexible[0].move_to([-1.8, -1.8, 0], aligned_edge=DOWN)
        simple[1].next_to(simple[0], DOWN, 0.25)
        flexible[1].next_to(flexible[0], DOWN, 0.25)
        y_name = label("error", 28, SUBDUED).rotate(PI / 2).next_to(simple[0], LEFT, 0.4)
        brace = BraceBetweenPoints([-0.8, simple[0].get_top()[1], 0], [-0.8, flexible[0].get_top()[1], 0],
                                   direction=RIGHT, color=PURPLE)
        gap = label("the gap", 32, PURPLE, weight=BOLD).next_to(brace, RIGHT, 0.2)
        guide = DashedLine(simple[0].get_corner(UR), [-0.8, simple[0].get_top()[1], 0], color=GREY)
        readings = VGroup(label("large: structure you have not specified", 30, INK),
                          label("small: prefer the interpretable one", 30, INK)
                          ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.6, -0.6, 0])
        # "The practical habit: fit a simple model and a flexible one."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        self.play(GrowFromEdge(simple[0], DOWN), FadeIn(simple[1]), GrowFromEdge(flexible[0], DOWN),
                  FadeIn(flexible[1]), FadeIn(y_name), run_time=self.share(0.2))
        # "The gap between them tells you how much structure you have not specified."
        at(self, 0.45)
        self.play(Create(guide), GrowFromCenter(brace), FadeIn(gap), run_time=self.share(0.12))
        at(self, 0.65)
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * LEFT) for r in readings], lag_ratio=0.5),
                  run_time=self.share(0.2))
        self.finish()


class Scene44(KeyPointScene):
    number, point = 44, 3


# The quiz (scenes 45–46) ------------------------------------------------------------------

class Scene45(QuizScene):
    number = 45
    question = ("Your random forest scores best on the test set.", "Now you need predictions for water",
                "warmer than any you sampled.", "Should you use it?")


class Scene46(VideoScene):
    number = 46

    def construct(self):
        # Schematic: the forest flat beyond the sampled range, a stated shape instead.
        answer = label("No", 60, VERMILION, weight=BOLD).to_edge(UP, buff=0.4)
        inside, beyond, out_tag, trend = flat_layout([-1.6, -0.2, 0], 8.0)
        trend_tag = label("a parametric model:\nits assumption, stated", 28, INK, weight=BOLD
                          ).next_to(trend.get_end(), RIGHT, 0.2)
        confident = label("no change, with complete confidence", 30, VERMILION).to_edge(DOWN, buff=0.4)
        # "No."
        self.play(FadeIn(answer), FadeIn(inside), run_time=self.share(0.12))
        # "Beyond the sampled range, the forest predicts no change, with complete confidence."
        at(self, 0.15)
        self.play(Create(beyond), FadeIn(out_tag), run_time=self.share(0.15))
        at(self, 0.35)
        self.play(FadeIn(confident), run_time=self.share(0.1))
        # "Use a parametric model, and state its assumption loudly."
        at(self, 0.6)
        self.play(Create(trend), FadeIn(trend_tag), run_time=self.share(0.15))
        self.finish()


# The recap (scenes 47–49) and the end card (scene 50) --------------------------------------

class Scene47(RecapScene):
    number, point = 47, 1


class Scene48(RecapScene):
    number, point = 48, 2


class Scene49(RecapScene):
    number, point = 49, 3


class Scene50(EndCardScene):
    number = 50
