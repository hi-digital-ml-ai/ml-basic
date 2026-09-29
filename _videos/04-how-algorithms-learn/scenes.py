"""Manim scenes for the how-algorithms-learn video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/04-how-algorithms-learn
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

Scenes marked "page results" read visuals/data/*.csv, which tools/figures-for-video.R
writes from the pages. The others are schematic: made-up shapes, never numbers that
could pass for survey results. The opening, key-point, recap, quiz and end-card scenes
are shared (mlbasic_video.py) and read PROMISES, ANSWERS and RECAP from here.
Consecutive scenes about one picture share a builder, so each starts where the
previous one ended.
"""

import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["Where a model's loss comes from",
            "Why a fit can fail without telling you",
            "Why a term with no data can help"]
ANSWERS = ["The loss is an\nassumption about\nyour data",
           "Fitting is a search:\ncheck that\nit arrived",
           "A penalty is a prior:\nwhat you knew\nbefore the survey"]
RECAP = ["The loss is an assumption: choose it and report it",
         "Fitting is a search: check that it arrived",
         "A penalty is a prior, and with little data it can help"]

# Stated in the pages' prose rather than computed: Huber's threshold and the misses the
# loss page prices, the grid's hundred values per parameter, and the prior's "about ±1"
# and its 0.9 against 900 on the MAP page.
HUBER_DELTA = 2
MISSES = (1, 10)
GRID_VALUES = 100
PRIOR_SCALE = 1
FLAT_PRIOR = (0.9, 900)

LOSS_COLOURS = {"Squared error": BLUE, "Absolute error": ORANGE, "Huber (δ = 2)": GREEN}
RATE_COLOURS = {0.02: ORANGE, 0.3: BLUE, 0.72: VERMILION}


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


def fixed(value, digits=2):
    """A number to `digits` places, rounded half up as the pages' prose rounds."""
    text = f"{Decimal(str(value)).quantize(Decimal(1).scaleb(-digits), ROUND_HALF_UP)}"
    return text.replace("-", "−")


def percent(value, digits=1):
    return f"{Decimal(str(100 * value)).quantize(Decimal(1).scaleb(-digits), ROUND_HALF_UP)}%"


def grouped(value):
    """A whole number with a thousands separator, as the pages print 13,515."""
    return f"{int(Decimal(str(value)).quantize(Decimal(1), ROUND_HALF_UP)):,}"


def band(mobject, colour, opacity=0.15, buff=0.12):
    return SurroundingRectangle(mobject, color=colour, buff=buff, corner_radius=0.1, stroke_width=0,
                                fill_color=colour, fill_opacity=opacity)


def hbar(axes, y, value, colour, height=0.5, start=0):
    left, right = axes.c2p(start, y), axes.c2p(value, y)
    return Rectangle(width=max(right[0] - left[0], 0.001), height=height, stroke_width=0, fill_color=colour,
                     fill_opacity=1).move_to(left, aligned_edge=LEFT)


def table(rows, widths, size=30, colours=None, header_colour=SUBDUED, row_gap=0.62):
    """Rows of text cells: the first row is the header. Columns after the first are right-aligned."""
    out = VGroup()
    for r, row in enumerate(rows):
        cells = VGroup()
        x = 0
        for c, (text, width) in enumerate(zip(row, widths)):
            colour = header_colour if r == 0 else (colours[r - 1] if colours else INK)
            cell = label(text, size - (4 if r == 0 else 0), colour, weight=BOLD if r == 0 or c == 0 else NORMAL)
            if c == 0:
                cell.move_to([x, -r * row_gap, 0], aligned_edge=LEFT)
            else:
                cell.move_to([x + width, -r * row_gap, 0], aligned_edge=RIGHT)
            cells.add(cell)
            x += width
        out.add(cells)
    return out


def normal_pdf(x, mean, sd):
    return math.exp(-0.5 * ((x - mean) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))


def poisson(k, mu):
    return math.exp(k * math.log(mu) - mu - math.lgamma(k + 1))


# The puzzle (scenes 2–4) ------------------------------------------------------------------

def two_fits_layout(scene):
    """The forty-station fit twice: maximum likelihood and MAP, named only as fits 1 and 2."""
    summary = scene.data("map-summary").iloc[0]
    temperature = scene.data("coefficients").set_index("term").loc["temperature_c"]
    heading = title(f"One model, the same {int(summary['training'])} stations", 46).to_edge(UP, buff=0.5)
    sub = label(f"a pilot survey with {int(summary['predictors'])} predictors", 32, SUBDUED
                ).next_to(heading, DOWN, 0.25)
    cards = VGroup()
    for name, value, colour in (("Fit 1", temperature["mle"], ORANGE), ("Fit 2", temperature["map"], BLUE)):
        head = label(name, 36, colour, weight=BOLD)
        what = label("temperature coefficient", 28, SUBDUED)
        big = label(fixed(value), 84, colour, weight=BOLD)
        inner = VGroup(head, what, big).arrange(DOWN, buff=0.3)
        box = RoundedRectangle(width=4.8, height=3.4, corner_radius=0.2, stroke_color=colour, stroke_width=4,
                               fill_color=colour, fill_opacity=0.06)
        inner.move_to(box)
        cards.add(VGroup(box, inner))
    cards.arrange(RIGHT, buff=1.4).move_to([0, -0.4, 0])
    return heading, sub, cards


class Scene02(VideoScene):
    number = 2

    def construct(self):
        heading, sub, cards = two_fits_layout(self)
        # "Here are two fits of the same model to the same forty stations, a pilot survey with twelve predictors."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.play(FadeIn(sub), run_time=self.share(0.1))
        self.play(FadeIn(cards[0][0]), FadeIn(cards[1][0]), FadeIn(cards[0][1][:2]), FadeIn(cards[1][1][:2]),
                  run_time=self.share(0.12))
        # "In one, the temperature coefficient is 8.59. In the other, 0.33."
        at(self, 0.62)
        self.play(FadeIn(cards[0][1][2], scale=0.8), run_time=self.share(0.1))
        at(self, 0.85)
        self.play(FadeIn(cards[1][1][2], scale=0.8), run_time=self.share(0.1))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        heading, sub, cards = two_fits_layout(self)
        self.add(heading, sub, cards)
        extra = label("+ one term, containing no data", 30, PURPLE, weight=BOLD).next_to(cards[1], DOWN, 0.3)
        question = label("Which predicts new stations better?", 44, INK, weight=BOLD).to_edge(DOWN, buff=0.55)
        # "The second fit had one extra term, and that term contains no data at all."
        self.play(FadeIn(extra, shift=0.2 * UP), run_time=self.share(0.15))
        # "Which one predicts new stations better?"
        at(self, 0.42)
        self.play(FadeIn(question, shift=0.2 * UP), run_time=self.share(0.12))
        # "By the end of this video, you will know, and why."
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        # Schematic: the fitting loop.
        heading = title("Fitting is a search", 50).to_edge(UP, buff=0.6)
        steps = ["score how wrong\nthe model is", "change its numbers\nto be less wrong", "repeat"]
        colours = [VERMILION, BLUE, GREEN]
        points = [[-4.2, -1.6, 0], [0, 1.0, 0], [4.2, -1.6, 0]]
        boxes = VGroup()
        for text, colour, point in zip(steps, colours, points):
            words = VGroup(*[label(t, 34, colour, weight=BOLD) for t in text.split("\n")]).arrange(DOWN, buff=0.1)
            box = RoundedRectangle(width=4.0, height=1.6, corner_radius=0.2, stroke_color=colour, stroke_width=4,
                                   fill_color=colour, fill_opacity=0.07).move_to(point)
            boxes.add(VGroup(box, words.move_to(box)))
        arrows = VGroup(
            CurvedArrow(boxes[0].get_top() + 0.1 * UP, boxes[1].get_left() + 0.1 * LEFT, angle=-PI / 4, color=INK),
            CurvedArrow(boxes[1].get_right() + 0.1 * RIGHT, boxes[2].get_top() + 0.1 * UP, angle=-PI / 4,
                        color=INK),
            CurvedArrow(boxes[2].get_bottom() + 0.1 * DOWN, boxes[0].get_bottom() + 0.1 * DOWN, angle=-PI / 3,
                        color=INK))
        # "To see why, you need to know what fitting is."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "It is a search: score how wrong the model is, change its numbers ..., and repeat."
        at(self, 0.35)
        self.play(FadeIn(boxes[0]), run_time=self.share(0.1))
        at(self, 0.55)
        self.play(Create(arrows[0]), FadeIn(boxes[1]), run_time=self.share(0.12))
        at(self, 0.82)
        self.play(Create(arrows[1]), FadeIn(boxes[2]), Create(arrows[2]), run_time=self.share(0.12))
        self.finish()


# Every fit minimises a loss (scenes 5–14) --------------------------------------------------

class Scene05(VideoScene):
    number = 5

    def construct(self):
        # The three losses as the page defines them; a schematic of the definitions, not results.
        heading = title("The loss scores one prediction", 46).to_edge(UP, buff=0.45)
        axes, frame = chart([-10, 10, 1], [0, 50, 10], 7.6, 4.8, [-10, -5, 0, 5, 10], [0, 25, 50],
                            "residual: observed − predicted", "penalty")
        frame.move_to([-2.4, -0.55, 0])

        def huber(r):
            return 0.5 * r * r if abs(r) <= HUBER_DELTA else HUBER_DELTA * (abs(r) - 0.5 * HUBER_DELTA)

        shapes = {"Squared error": lambda r: r * r, "Absolute error": abs, "Huber (δ = 2)": huber}
        curves, names = VGroup(), VGroup()
        for name, f in shapes.items():
            limit = math.sqrt(50) if name == "Squared error" else 10
            curves.add(axes.plot(f, x_range=[-limit, limit, 0.05], color=LOSS_COLOURS[name], stroke_width=6))
            names.add(label(name, 30, LOSS_COLOURS[name], weight=BOLD))
        names.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([2.9, 1.6, 0], aligned_edge=LEFT)
        small, big = MISSES
        prices = VGroup(label(f"a miss of {big} costs", 28, SUBDUED),
                        label(f"{big * big // small} × a miss of {small}", 32, BLUE, weight=BOLD),
                        label(f"{big // small} × a miss of {small}", 32, ORANGE, weight=BOLD)
                        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(names, DOWN, 0.7, aligned_edge=LEFT)
        compromise = label("squared near zero,\nstraight beyond", 26, GREEN).next_to(prices, DOWN, 0.45,
                                                                                  aligned_edge=LEFT)
        # "The score is the loss."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.12))
        # "Squared error makes a miss of 10 a hundred times worse than a miss of 1."
        at(self, 0.15)
        self.play(Create(curves[0]), FadeIn(names[0]), run_time=self.share(0.15))
        self.play(FadeIn(prices[0]), FadeIn(prices[1]), run_time=self.share(0.1))
        # "Absolute error makes it ten times worse."
        at(self, 0.58)
        self.play(Create(curves[1]), FadeIn(names[1]), FadeIn(prices[2]), run_time=self.share(0.14))
        # "Huber is a compromise."
        at(self, 0.82)
        self.play(Create(curves[2]), FadeIn(names[2]), FadeIn(compromise), run_time=self.share(0.14))
        self.finish()


def lines_layout(scene):
    """Abundance against chlorophyll at every station, and the axes for the fitted lines."""
    stations = scene.data("stations")
    axes, frame = chart([0, 14, 1], [0, 40, 5], 8.6, 5.2, [0, 2, 4, 6, 8, 10, 12, 14], [0, 10, 20, 30, 40],
                        "chlorophyll (mg m⁻³)", "abundance (individuals)")
    frame.move_to([-1.6, -0.5, 0])
    dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.035, color=GREY, fill_opacity=0.45)
                    for x, y in zip(stations["chlorophyll"], stations["abundance"])])
    return axes, frame, dots, stations


def fitted_line(axes, intercept, slope, colour):
    return Line(axes.c2p(0, intercept), axes.c2p(14, intercept + 14 * slope), color=colour, stroke_width=6)


class Scene06(VideoScene):
    number = 6

    def construct(self):
        axes, frame, dots, stations = lines_layout(self)
        losses = self.data("three-losses").set_index("loss")
        heading = title("One dataset, three losses, three answers", 44).to_edge(UP, buff=0.4)
        count = label(f"{len(stations)} stations", 28, SUBDUED).next_to(heading, DOWN, 0.2)
        lines, names = VGroup(), VGroup()
        for name, row in losses.iterrows():
            lines.add(fitted_line(axes, row["intercept"], row["slope"], LOSS_COLOURS[name]))
            names.add(label(name, 28, LOSS_COLOURS[name], weight=BOLD))
        names.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([5.0, 1.2, 0])
        starts = VGroup()
        for i, name in enumerate(("Squared error", "Absolute error")):
            value = losses.loc[name, "intercept"]
            dot = Dot(axes.c2p(0, value), radius=0.1, color=LOSS_COLOURS[name])
            text = label(f"{name.split()[0].lower()} starts at {fixed(value)}", 28, LOSS_COLOURS[name],
                         weight=BOLD).move_to([5.0, -0.9 - 0.55 * i, 0])
            starts.add(VGroup(dot, text))
        # "Fit abundance against chlorophyll three times, changing nothing but the loss, ..."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.1))
        self.play(FadeIn(dots, lag_ratio=0.002), FadeIn(count), run_time=self.share(0.15))
        # "... and you get three answers."
        at(self, 0.4)
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.4), FadeIn(names),
                  run_time=self.share(0.18))
        # "The squared-error line starts at 2.36 individuals, the absolute-error line at 1.13."
        at(self, 0.65)
        self.play(FadeIn(starts[0]), run_time=self.share(0.1))
        at(self, 0.85)
        self.play(FadeIn(starts[1]), run_time=self.share(0.1))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        share = self.data("error-share").iloc[0]
        heading = title(f"{int(share['worst_stations'])} stations, 5% of {int(share['stations'])}", 46
                        ).to_edge(UP, buff=0.6)
        sub = label("their share of the total error", 32, SUBDUED).next_to(heading, DOWN, 0.25)
        axes = plain_axes([0, 1, 0.1], [0, 2, 1], 9.0, 3.0).move_to([0.9, -0.9, 0])
        rows = VGroup()
        for y, name, value, colour in ((1.4, "squared error", share["squared_share"], BLUE),
                                       (0.5, "absolute error", share["absolute_share"], ORANGE)):
            whole = hbar(axes, y, 1, colour, 0.7).set_fill(opacity=0.15)
            worst = hbar(axes, y, value, colour, 0.7)
            name_text = label(name, 30, colour, weight=BOLD).next_to(whole, LEFT, 0.3)
            value_text = label(percent(value), 36, BACKGROUND, weight=BOLD).move_to(worst)
            rows.add(VGroup(whole, name_text, worst, value_text))
        half = DashedLine(axes.c2p(0.5, 0.0), axes.c2p(0.5, 1.95), color=GREY)
        half_text = label("half", 26, SUBDUED).next_to(half, UP, 0.1)
        # "Why? Thirty-seven stations, 5% of the data, ..."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        self.play(FadeIn(sub), FadeIn(rows[0][:2]), FadeIn(rows[1][:2]), run_time=self.share(0.12))
        # "... supply half of the total squared error, ..."
        at(self, 0.45)
        self.play(GrowFromEdge(rows[0][2], LEFT), FadeIn(rows[0][3]), Create(half), FadeIn(half_text),
                  run_time=self.share(0.15))
        # "... but only a fifth of the absolute error."
        at(self, 0.75)
        self.play(GrowFromEdge(rows[1][2], LEFT), FadeIn(rows[1][3]), run_time=self.share(0.12))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        axes, frame, dots, stations = lines_layout(self)
        drop = self.data("drop-one").set_index("loss")
        share = self.data("error-share").iloc[0]
        heading = title(f"Delete one station of {int(share['stations'])}", 46).to_edge(UP, buff=0.4)
        largest = drop["largest_catch"].iloc[0]
        top = stations.loc[stations["abundance"].idxmax()]
        target = Circle(radius=0.22, color=VERMILION, stroke_width=5).move_to(axes.c2p(top["chlorophyll"], largest))
        tag = label(f"the largest catch, {largest:.0f}", 28, VERMILION, weight=BOLD
                    ).next_to(target, RIGHT, 0.2)
        rows = [["slope", "all", "minus one", "moves"]]
        for name in ("Squared error", "Absolute error"):
            r = drop.loc[name]
            rows.append([name, fixed(r["all"], 3), fixed(r["minus_one"], 3),
                         percent((r["all"] - r["minus_one"]) / r["all"])])
        numbers = table(rows, [3.0, 1.2, 1.9, 1.5], 28, colours=[BLUE, ORANGE])
        box = SurroundingRectangle(numbers, color=GRID, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                                   fill_opacity=0.95)
        panel = VGroup(box, numbers).move_to([2.9, -0.9, 0])
        self.add(frame, dots)
        # "Delete the single largest catch, one station of 749, ..."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(target), FadeIn(tag), run_time=self.share(0.15))
        at(self, 0.3)
        self.play(FadeOut(target), FadeOut(tag), dots[int(top.name)].animate.set_opacity(0),
                  run_time=self.share(0.08))
        # "... and the least-squares slope moves by 13.5%."
        self.play(FadeIn(panel[0]), FadeIn(numbers[0]), FadeIn(numbers[1]), run_time=self.share(0.12))
        self.play(Indicate(numbers[1][3], color=BLUE, scale_factor=1.3), run_time=self.share(0.1))
        # "The absolute-error slope moves by 2.1%."
        at(self, 0.72)
        self.play(FadeIn(numbers[2]), run_time=self.share(0.1))
        self.play(Indicate(numbers[2][3], color=ORANGE, scale_factor=1.3), run_time=self.share(0.1))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        # Schematic: the same large hauls, read two ways.
        heading = title("Neither loss is wrong", 50).to_edge(UP, buff=0.6)
        sub = label("it depends on what the big hauls are", 32, SUBDUED).next_to(heading, DOWN, 0.25)
        cards = VGroup()
        for what, then, colour in (("real aggregations", "squared error", BLUE),
                                   ("a net that fished badly", "absolute error or Huber", ORANGE)):
            head = label("if they are", 28, SUBDUED)
            what_text = label(what, 36, INK, weight=BOLD)
            arrow = Arrow(UP, DOWN, color=colour, buff=0).scale(0.4)
            then_text = label(then, 36, colour, weight=BOLD)
            inner = VGroup(head, what_text, arrow, then_text).arrange(DOWN, buff=0.25)
            box = RoundedRectangle(width=5.8, height=3.3, corner_radius=0.2, stroke_color=colour, stroke_width=4,
                                   fill_color=colour, fill_opacity=0.05)
            cards.add(VGroup(box, inner.move_to(box)))
        cards.arrange(RIGHT, buff=0.7).move_to([0, -0.6, 0])
        warning = label("otherwise half the objective comes from your worst data", 30, VERMILION
                        ).to_edge(DOWN, buff=0.45)
        # "Neither loss is wrong."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(sub), run_time=self.share(0.12))
        # "If the big hauls are real aggregations, squared error is right."
        at(self, 0.18)
        self.play(FadeIn(cards[0], shift=0.2 * RIGHT), run_time=self.share(0.14))
        # "If they are a net that fished badly, you have handed half the objective to your worst data."
        at(self, 0.52)
        self.play(FadeIn(cards[1], shift=0.2 * LEFT), run_time=self.share(0.14))
        at(self, 0.75)
        self.play(FadeIn(warning), run_time=self.share(0.1))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        counts = [int(c) for c in self.data("counts")["count"]]
        mean = sum(counts) / len(counts)
        heading = title("Likelihood: what makes the data most probable?", 42).to_edge(UP, buff=0.4)
        axes, frame = chart([0, 15, 1], [0, 1, 0.2], 9.0, 4.8, [0, 3, 6, 9, 12, 15], [],
                            "expected count μ", "likelihood")
        frame.move_to([-1.2, -0.6, 0])
        singles, names = VGroup(), VGroup()
        for k in counts:
            curve = axes.plot(lambda m, k=k: poisson(k, m), x_range=[0.05, 15, 0.05], color=GREY, stroke_width=4)
            singles.add(curve)
            peak = max(k, 0.05)
            names.add(label(f"caught {k}", 26, SUBDUED, weight=BOLD).next_to(
                axes.c2p(peak, poisson(k, peak)), UP, 0.12))
        names[1].next_to(axes.c2p(0.4, poisson(0, 0.4)), RIGHT, 0.2)

        def joint(m):
            return math.prod(poisson(k, m) for k in counts)

        top = joint(mean)
        together = axes.plot(lambda m: 0.8 * joint(m) / top, x_range=[0.05, 15, 0.05], color=VERMILION,
                             stroke_width=7)
        peak_line = DashedLine(axes.c2p(mean, 0), axes.c2p(mean, 0.85), color=VERMILION)
        peak_text = label(f"all three together: peak at the mean, {fixed(mean)}", 28, VERMILION, weight=BOLD
                          ).next_to(axes.c2p(mean, 0.85), RIGHT, 0.2)
        # "So where do losses come from?"
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.12))
        # "Likelihood asks which values make the data you saw most probable."
        at(self, 0.2)
        self.play(Create(singles[0]), FadeIn(names[0]), run_time=self.share(0.15))
        # "For three stations that caught 3, 0 and 11, ..."
        at(self, 0.55)
        self.play(Create(singles[1]), FadeIn(names[1]), Create(singles[2]), FadeIn(names[2]),
                  run_time=self.share(0.15))
        # "... the answer is their mean."
        at(self, 0.8)
        self.play(Create(together), Create(peak_line), FadeIn(peak_text), run_time=self.share(0.15))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        # The page's table of assumptions and the losses they become.
        heading = title("Each loss is an assumption", 48).to_edge(UP, buff=0.5)
        rule = label("loss = − log likelihood", 36, PURPLE, weight=BOLD).next_to(heading, DOWN, 0.4)
        rows = [["if you assume the data are", "the loss is"],
                ["Normal", "squared error"],
                ["Poisson counts", "Poisson deviance"],
                ["yes or no", "log loss"]]
        grid = table(rows, [6.2, 4.6], 36, colours=[BLUE, GREEN, ORANGE], row_gap=0.95).move_to([0, -1.2, 0])
        arrows = VGroup(*[Arrow(grid[r][0].get_right() + 0.2 * RIGHT, grid[r][1].get_left() + 0.2 * LEFT,
                                color=GREY, buff=0.1, stroke_width=4) for r in (1, 2, 3)])
        # "Take the negative logarithm, and a likelihood becomes a loss."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.play(FadeIn(rule), run_time=self.share(0.1))
        # "Assume Normal errors, and you get squared error."
        at(self, 0.4)
        self.play(FadeIn(grid[0]), FadeIn(grid[1]), GrowArrow(arrows[0]), run_time=self.share(0.12))
        # "Poisson gives Poisson deviance."
        at(self, 0.68)
        self.play(FadeIn(grid[2]), GrowArrow(arrows[1]), run_time=self.share(0.1))
        # "Yes or no gives log loss."
        at(self, 0.85)
        self.play(FadeIn(grid[3]), GrowArrow(arrows[2]), run_time=self.share(0.1))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        fits = self.data("normal-mle")
        heading = title("Least squares is Normal maximum likelihood", 44).to_edge(UP, buff=0.6)
        rows = [["", "intercept", "slope", "sigma"]]
        for _, r in fits.iterrows():
            rows.append([r["method"], fixed(r["intercept"], 4), fixed(r["slope"], 4), fixed(r["sigma"], 4)])
        grid = table(rows, [4.6, 2.2, 2.0, 2.0], 34, colours=[PURPLE, BLUE], row_gap=0.85).move_to([0, 0.2, 0])
        same = card("identical", GREEN, 40).next_to(grid, DOWN, 0.8)
        # "It is not an analogy."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "Maximum likelihood under a Normal model returns exactly the least-squares line."
        at(self, 0.3)
        self.play(FadeIn(grid[0]), FadeIn(grid[1]), run_time=self.share(0.12))
        at(self, 0.6)
        self.play(FadeIn(grid[2]), run_time=self.share(0.12))
        self.play(FadeIn(same, scale=0.8), run_time=self.share(0.1))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        # Schematic: a Normal distribution around a small expected count.
        heading = title("Least squares on counts", 48).to_edge(UP, buff=0.6)
        axes = plain_axes([-8, 12, 1], [0, 0.16, 0.04], 10.5, 4.2).move_to([0, -0.6, 0])
        zero = Line(axes.c2p(0, 0), axes.c2p(0, 0.16), color=INK, stroke_width=3)
        zero_text = label("0", 30, INK, weight=BOLD).next_to(axes.c2p(0, 0), DOWN, 0.15)
        name = label("count", 28, SUBDUED).next_to(axes, DOWN, 0.55)
        bell = axes.plot(lambda x: normal_pdf(x, 2.5, 3), x_range=[-8, 12, 0.05], color=BLUE, stroke_width=6)
        tail = axes.get_area(bell, x_range=[-8, 0], color=VERMILION, opacity=0.5)
        tail_text = label("negative fish", 36, VERMILION, weight=BOLD).move_to(axes.c2p(-5, 0.1))
        assumes = label("assumes a Normal distribution, running to minus infinity", 32, BLUE
                        ).next_to(heading, DOWN, 0.35)
        # "So least squares on counts silently assumes a distribution that runs to minus infinity."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(axes), FadeIn(zero), FadeIn(zero_text), FadeIn(name),
                  run_time=self.share(0.12))
        self.play(Create(bell), FadeIn(assumes), run_time=self.share(0.25))
        # "That is why a linear model can predict negative fish."
        at(self, 0.62)
        self.play(FadeIn(tail), FadeIn(tail_text), run_time=self.share(0.15))
        self.finish()


class Scene14(KeyPointScene):
    number, point = 14, 1


# Fitting is a search (scenes 15–31) --------------------------------------------------------

class Scene15(VideoScene):
    number = 15

    def construct(self):
        closed = self.data("closed-form")
        heading = title("Least squares has a formula", 48).to_edge(UP, buff=0.5)
        names = {"(Intercept)": "intercept", "chlorophyll_mg_m3": "chlorophyll", "depth_m": "depth",
                 "temperature_c": "temperature"}
        rows = [["", "by formula", "by lm()"]]
        for _, r in closed.iterrows():
            rows.append([names[r["term"]], fixed(r["formula"], 4), fixed(r["lm"], 4)])
        grid = table(rows, [3.0, 2.6, 2.4], 34, row_gap=0.7).move_to([-2.4, -0.3, 0])
        traits = VGroup(*[label(t, 32, GREEN, weight=BOLD) for t in ("exact", "one step", "the same every time")]
                        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        traits.move_to([2.6, -0.1, 0], aligned_edge=LEFT)
        rare = label("almost nothing else has one", 34, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.55)
        # "For a few models the best numbers can be calculated."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "Least squares has a formula: exact, in one step, the same every time."
        at(self, 0.3)
        self.play(FadeIn(grid, lag_ratio=0.1), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(t, shift=0.2 * LEFT) for t in traits], lag_ratio=0.5),
                  run_time=self.share(0.2))
        # "Almost nothing else does."
        at(self, 0.82)
        self.play(FadeIn(rare), run_time=self.share(0.1))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        trace = self.data("irls")
        heading = title("Logistic regression has to search", 46).to_edge(UP, buff=0.45)
        axes, frame = chart([0, 6, 1], [-520, -360, 40], 8.4, 4.6, range(7), [-520, -480, -440, -400, -360],
                            "step", "log-likelihood", y_format="{:.0f}")
        frame.move_to([-0.8, -0.6, 0])
        for t in frame[2]:
            t.become(label(t.text.replace("-", "−"), 24, SUBDUED).move_to(t))
        points = [axes.c2p(r["iteration"], r["log_likelihood"]) for _, r in trace.iterrows()]
        dots = VGroup(*[Dot(p, radius=0.09, color=BLUE) for p in points])
        values = VGroup()
        for i, side in ((0, RIGHT), (1, UP), (2, DOWN)):
            values.add(label(fixed(trace["log_likelihood"][i], 1), 28, BLUE, weight=BOLD
                             ).next_to(dots[i], side + (RIGHT if side is not RIGHT else ORIGIN), 0.15))
        start = label("(a standing start)", 26, SUBDUED).next_to(values[0], RIGHT, 0.2)
        flat = label("stopped changing", 30, GREEN, weight=BOLD).next_to(axes.c2p(4.5, trace["log_likelihood"][4]),
                                                                         DOWN, 0.5)
        # "Logistic regression has to search."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.12))
        # "From a standing start, each step improves the log-likelihood, ..."
        at(self, 0.2)
        self.play(FadeIn(dots[0], scale=0.5), FadeIn(values[0]), FadeIn(start), run_time=self.share(0.1))
        for i in range(1, len(dots)):
            self.play(Create(VMobject(color=BLUE, stroke_width=5).set_points_as_corners(points[i - 1:i + 1])),
                      FadeIn(dots[i]), *([FadeIn(values[i])] if i < 3 else []), run_time=self.share(0.07))
        # "... and by the fourth it has stopped changing."
        at(self, 0.82)
        self.play(FadeIn(flat), Indicate(dots[4], color=GREEN, scale_factor=1.8), run_time=self.share(0.12))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        # The page's grid-cost table: GRID_VALUES candidate values per parameter, all combinations.
        heading = title("Try every combination?", 48).to_edge(UP, buff=0.5)
        sub = label(f"{GRID_VALUES} values for each parameter", 32, SUBDUED).next_to(heading, DOWN, 0.25)
        powers = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        words = {2: "ten thousand", 4: "a hundred million", 10: ""}
        axes = plain_axes([0, 20, 1], [0, 3, 1], 8.0, 3.6).move_to([1.4, -1.2, 0])
        rows = VGroup()
        for y, p in ((2.5, 2), (1.5, 4), (0.5, 10)):
            exponent = round(math.log10(GRID_VALUES ** p))
            bar = hbar(axes, y, exponent, VERMILION if p == 10 else BLUE, 0.6)
            name = label(f"{p} parameters", 30, INK, weight=BOLD).next_to(axes.c2p(0, y), LEFT, 0.3)
            value = label(f"10{str(exponent).translate(powers)}  {words[p]}".strip(), 30,
                          VERMILION if p == 10 else BLUE, weight=BOLD).next_to(bar, RIGHT, 0.2)
            rows.add(VGroup(name, bar, value))
        # "Why not simply try every combination?"
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "At a hundred values each, two parameters is ten thousand evaluations."
        at(self, 0.22)
        self.play(FadeIn(sub), FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]),
                  run_time=self.share(0.14))
        # "Four is a hundred million."
        at(self, 0.62)
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.1))
        # "Ten is ten to the power twenty."
        at(self, 0.8)
        self.play(FadeIn(rows[2][0]), GrowFromEdge(rows[2][1], LEFT), FadeIn(rows[2][2]), run_time=self.share(0.12))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        # Schematic: a walk down a bowl.
        heading = title("Gradient descent", 50).to_edge(UP, buff=0.6)
        axes = plain_axes([-4, 4, 1], [0, 16, 4], 8.0, 4.2).move_to([-1.2, -0.4, 0])
        bowl = axes.plot(lambda x: x * x, x_range=[-4, 4, 0.05], color=GREY, stroke_width=6)
        xs = [-3.6, -2.2, -1.2, -0.55, -0.2]
        dots = [Dot(axes.c2p(x, x * x), radius=0.13, color=BLUE) for x in xs]
        steps = ["feel which way\nis downhill", "take a step", "repeat"]
        notes = VGroup(*[VGroup(*[label(t, 34, c, weight=BOLD) for t in s.split("\n")]).arrange(DOWN, buff=0.08)
                         for s, c in zip(steps, (VERMILION, BLUE, GREEN))]
                       ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([4.6, -0.4, 0])
        slope = Line(axes.c2p(-4.3, 4.3 * 7.2 - 12.96), axes.c2p(-2.9, 2.9 * 7.2 - 12.96), color=VERMILION,
                     stroke_width=6)
        networks = label("how every neural network is trained", 30, SUBDUED).to_edge(DOWN, buff=0.45)
        # "So the search has to be directed."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(bowl), FadeIn(dots[0]), run_time=self.share(0.15))
        # "Feel which way is downhill, take a step, and repeat."
        at(self, 0.2)
        self.play(Create(slope), FadeIn(notes[0]), run_time=self.share(0.1))
        self.play(FadeOut(slope), ReplacementTransform(dots[0].copy(), dots[1]), FadeIn(notes[1]),
                  run_time=self.share(0.1))
        self.play(FadeIn(notes[2]), *[ReplacementTransform(dots[i].copy(), dots[i + 1]) for i in (1, 2, 3)],
                  run_time=self.share(0.15), lag_ratio=0.5)
        # "That is gradient descent, and it trains every neural network you have heard of."
        at(self, 0.7)
        self.play(FadeIn(networks), run_time=self.share(0.1))
        self.finish()


def paths_layout(scene):
    """The objective's contours for the two slopes, from the page's own grid, and its minimum."""
    contours = scene.data("contours")
    descent = scene.data("descent").iloc[0]
    axes, frame = chart([-0.3, 2.9, 0.5], [-1.8, 0.7, 0.5], 6.9, 5.4, [0, 1, 2], [-1.5, -1, -0.5, 0, 0.5],
                        "chlorophyll slope", "depth slope", y_format="{:g}")
    for t in frame[2]:
        t.become(label(t.text.replace("-", "−"), 24, SUBDUED).move_to(t))
    frame.move_to([-2.4, -0.45, 0])
    lines = VGroup()
    for _, line in contours.groupby("line"):
        lines.add(VMobject(color=GRID, stroke_width=3).set_points_as_corners(
            [axes.c2p(x, y) for x, y in zip(line["x"], line["y"])]))
    best = cross(0.5, INK).move_to(axes.c2p(descent["optimum_chlorophyll"], descent["optimum_depth"]))
    heading = title("A walk down the bowl", 46).to_edge(UP, buff=0.35)
    return heading, axes, frame, lines, best, descent


def walk(scene, axes, rate, steps):
    paths = scene.data("paths")
    walk = paths[(paths["learning_rate"] - rate).abs() < 1e-9].sort_values("step").head(steps + 1)
    points = [axes.c2p(x, y) for x, y in zip(walk["chlorophyll"], walk["depth"])]
    colour = RATE_COLOURS[rate]
    return (VMobject(color=colour, stroke_width=4).set_points_as_corners(points),
            VGroup(*[Dot(p, radius=0.06, color=colour) for p in points]))


class Scene19(VideoScene):
    number = 19

    def construct(self):
        heading, axes, frame, lines, best, descent = paths_layout(self)
        line, dots = walk(self, axes, 0.3, 40)
        start = label("start", 26, SUBDUED).next_to(dots[0], UP, 0.15)
        rate = label("learning rate: the size of each step", 30, INK, weight=BOLD).move_to([3.7, 2.4, 0])
        tag = VGroup(label("0.3", 40, BLUE, weight=BOLD),
                     label(f"the bottom in {int(descent['steps_03'])} steps", 30, BLUE)
                     ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([2.3, 1.3, 0], aligned_edge=LEFT)
        # "The size of each step is the learning rate."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), Create(lines), FadeIn(best),
                  run_time=self.share(0.15))
        self.play(FadeIn(rate), FadeIn(dots[0]), FadeIn(start), run_time=self.share(0.12))
        # "At 0.3, this walk reaches the bottom of the bowl in six steps."
        at(self, 0.45)
        self.play(Create(line), LaggedStart(*[FadeIn(d) for d in dots[1:8]], lag_ratio=0.5), FadeIn(tag),
                  run_time=self.share(0.3))
        self.add(dots)
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        heading, axes, frame, lines, best, descent = paths_layout(self)
        line, dots = walk(self, axes, 0.3, 40)
        rate = label("learning rate: the size of each step", 30, INK, weight=BOLD).move_to([3.7, 2.4, 0])
        tag = VGroup(label("0.3", 40, BLUE, weight=BOLD),
                     label(f"the bottom in {int(descent['steps_03'])} steps", 30, BLUE)
                     ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        tag.move_to([2.3, 1.3, 0], aligned_edge=LEFT)
        self.add(heading, frame, lines, best, line, dots, rate, tag)
        slow_line, slow_dots = walk(self, axes, 0.02, 40)
        fast_line, fast_dots = walk(self, axes, 0.72, 40)
        slow = VGroup(label("0.02", 40, ORANGE, weight=BOLD),
                      label("still short after 40 steps;", 30, ORANGE),
                      label(f"needs {int(descent['steps_002'])}", 30, ORANGE)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(tag, DOWN, 0.5, aligned_edge=LEFT)
        fast = VGroup(label("0.72", 40, VERMILION, weight=BOLD),
                      label("zig-zags across the valley;", 30, VERMILION),
                      label(f"needs {int(descent['steps_072'])}", 30, VERMILION)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(slow, DOWN, 0.5, aligned_edge=LEFT)
        # "At 0.02 it is still short after forty steps, and needs 106."
        self.play(FadeOut(rate), Create(slow_line), FadeIn(slow_dots, lag_ratio=0.1), run_time=self.share(0.25))
        self.play(FadeIn(slow), run_time=self.share(0.1))
        # "At 0.72 it zig-zags across the valley, and needs 161."
        at(self, 0.5)
        self.play(Create(fast_line), FadeIn(fast_dots, lag_ratio=0.1), run_time=self.share(0.3))
        self.play(FadeIn(fast), run_time=self.share(0.1))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        descent = self.data("descent").iloc[0]
        limit = descent["limit"]
        heading = title("The cliff edge", 50).to_edge(UP, buff=0.5)
        axes, frame = chart([0, 1, 0.1], [0, 1, 1], 11.0, 0.01, [0, 0.2, 0.4, 0.6, 0.8, 1.0], [],
                            "learning rate", "")
        frame.move_to([0, -0.2, 0])
        safe = Rectangle(width=axes.c2p(limit, 0)[0] - axes.c2p(0, 0)[0], height=1.2, stroke_width=0,
                         fill_color=GREEN, fill_opacity=0.15).move_to(axes.c2p(0, 0), aligned_edge=DL)
        danger = Rectangle(width=axes.c2p(1, 0)[0] - axes.c2p(limit, 0)[0], height=1.2, stroke_width=0,
                           fill_color=VERMILION, fill_opacity=0.18).move_to(axes.c2p(limit, 0), aligned_edge=DL)
        safe_text = label("arrives", 32, GREEN, weight=BOLD).move_to(safe).shift(0.3 * UP)
        danger_text = label("diverges", 32, VERMILION, weight=BOLD).move_to(danger).shift(0.3 * UP)
        edge = Line(axes.c2p(limit, 0), axes.c2p(limit, 0) + 1.7 * UP, color=INK, stroke_width=5)
        edge_text = label(f"limit {fixed(limit, 4)}", 32, INK, weight=BOLD).next_to(edge, UP, 0.1)
        marks = VGroup()
        for rate in (0.02, 0.3, 0.72):
            marks.add(Dot(axes.c2p(rate, 0) + 0.3 * UP, radius=0.1, color=RATE_COLOURS[rate]))
        over = Dot(axes.c2p(descent["diverged_rate"], 0) + 0.3 * UP, radius=0.12, color=VERMILION)
        billions = descent["diverged_mse"] / 1e9
        blowup = card(f"at {fixed(descent['diverged_rate'], 1)}, after {int(descent['diverged_steps'])} steps:\n"
                      f"MSE {fixed(billions, 1)} billion", VERMILION, 36).move_to([0, -2.4, 0])
        # "And there is a cliff edge."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), FadeIn(safe), FadeIn(marks),
                  run_time=self.share(0.15))
        # "Above 0.7282 the walk does not arrive slowly; it diverges."
        at(self, 0.2)
        self.play(Create(edge), FadeIn(edge_text), FadeIn(safe_text), run_time=self.share(0.12))
        at(self, 0.4)
        self.play(FadeIn(danger), FadeIn(danger_text), run_time=self.share(0.1))
        # "At 0.8, sixty steps take the error to 7.3 billion."
        at(self, 0.6)
        self.play(FadeIn(over, scale=0.5), run_time=self.share(0.08))
        self.play(FadeIn(blowup, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        descent = self.data("descent").iloc[0]
        heading = title("The bowl's shape comes from your units", 44).to_edge(UP, buff=0.45)
        units = VGroup(label(f"depth: standard deviation {fixed(descent['sd_depth'], 1)} m", 30, SUBDUED),
                       label(f"chlorophyll: standard deviation {fixed(descent['sd_chlorophyll'])} mg m⁻³", 30,
                             SUBDUED)).arrange(DOWN, buff=0.15).next_to(heading, DOWN, 0.35)
        # An ellipse's axes stand in the ratio √κ: the bowl drawn to its true proportions.
        width = 8.0
        raw = Ellipse(width=width, height=width / math.sqrt(descent["condition_unscaled"]), color=VERMILION,
                      stroke_width=5).move_to([1.8, -0.9, 0])
        raw_text = VGroup(label("unscaled", 30, VERMILION, weight=BOLD),
                          label(f"stretched {fixed(descent['condition_unscaled'], 0)} to 1", 30, VERMILION)
                          ).arrange(DOWN, buff=0.08).next_to(raw, LEFT, 0.3)
        std_width = 3.2
        standard = Ellipse(width=std_width, height=std_width / math.sqrt(descent["condition"]), color=GREEN,
                           stroke_width=5).move_to([1.8, -2.55, 0])
        std_text = VGroup(label("standardised", 30, GREEN, weight=BOLD),
                          label(f"{fixed(descent['condition'], 1)} to 1", 30, GREEN)
                          ).arrange(DOWN, buff=0.08).next_to(standard, LEFT, 0.4)
        for text in (raw_text, std_text):
            text.set_x(-2.6 - text.width / 2)
        # "That limit is set by the shape of the bowl, and the shape by your units."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        self.play(FadeIn(units), run_time=self.share(0.12))
        # "Unscaled, this bowl is 766 times more stretched one way than the other."
        at(self, 0.45)
        self.play(Create(raw), FadeIn(raw_text), run_time=self.share(0.15))
        # "Standardised, 2.2."
        at(self, 0.82)
        self.play(Create(standard), FadeIn(std_text), run_time=self.share(0.12))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        descent = self.data("descent").iloc[0]
        std_steps, raw_steps = int(descent["steps_standardised"]), int(descent["steps_unscaled"])
        heading = title("The same answer, at different cost", 46).to_edge(UP, buff=0.55)
        sub = label("each at its best learning rate", 32, SUBDUED).next_to(heading, DOWN, 0.25)
        axes = plain_axes([0, raw_steps, 100], [0, 2, 1], 8.2, 2.8).move_to([1.6, -0.6, 0])
        rows = VGroup()
        for y, name, steps, colour in ((1.4, "standardised", std_steps, GREEN), (0.5, "unscaled", raw_steps, VERMILION)):
            bar = hbar(axes, y, steps, colour, 0.7)
            name_text = label(name, 32, colour, weight=BOLD).next_to(axes.c2p(0, y), LEFT, 0.3)
            value = label(f"{steps:,} steps", 34, colour, weight=BOLD)
            if steps < raw_steps / 2:
                value.next_to(bar, RIGHT, 0.25)
            else:
                value.set_color(BACKGROUND).move_to(bar)
            rows.add(VGroup(name_text, bar, value))
        times = card(f"{round(raw_steps / std_steps)} × the work", VERMILION, 40).to_edge(DOWN, buff=0.55)
        # "Give each its best learning rate."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(sub), run_time=self.share(0.15))
        # "The standardised version arrives in 17 steps, the unscaled one in 1,500."
        at(self, 0.25)
        self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]), run_time=self.share(0.1))
        at(self, 0.45)
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), run_time=self.share(0.15))
        self.play(FadeIn(rows[1][2]), run_time=self.share(0.05))
        # "The same answer, with eighty-eight times the work."
        at(self, 0.75)
        self.play(FadeIn(times, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        # The page's list of where scaling matters.
        heading = title("The real reason to scale", 48).to_edge(UP, buff=0.55)
        columns = VGroup()
        for head, items, colour in (("scaling matters for", ["gradient descent", "ridge and lasso", "neural networks",
                                                             "PCA and k-means"], GREEN),
                                    ("scaling does nothing for", ["lm() and glm()", "trees and forests"], GREY)):
            words = VGroup(label(head, 32, colour, weight=BOLD),
                           *[label(i, 34, INK) for i in items]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            columns.add(words)
        columns.arrange(RIGHT, buff=2.0, aligned_edge=UP).move_to([0, -0.3, 0])
        rule = label("the rule follows the algorithm, not the data", 34, PURPLE, weight=BOLD
                     ).to_edge(DOWN, buff=0.55)
        # "That is the real reason to scale your predictors."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "It matters for gradient descent, penalised regression, networks and k-means, ..."
        at(self, 0.25)
        self.play(FadeIn(columns[0][0]), LaggedStart(*[FadeIn(i, shift=0.2 * RIGHT) for i in columns[0][1:]],
                                                     lag_ratio=0.5), run_time=self.share(0.3))
        # "... and not at all for trees."
        at(self, 0.65)
        self.play(FadeIn(columns[1]), run_time=self.share(0.12))
        # "The rule follows the algorithm."
        at(self, 0.85)
        self.play(FadeIn(rule), run_time=self.share(0.1))
        self.finish()


def truncated_layout(scene):
    fits = scene.data("truncated")
    heading = title("Stopped after two iterations", 46).to_edge(UP, buff=0.6)
    rows = [["", "converged", "iterations", "chlorophyll"]]
    for _, r in fits.iterrows():
        rows.append([r["fit"], "TRUE" if r["converged"] else "FALSE", str(int(r["iterations"])),
                     fixed(r["chlorophyll"], 3)])
    grid = table(rows, [4.6, 2.4, 2.4, 2.6], 34, row_gap=0.9).move_to([0, 0.2, 0])
    out = abs((fits["chlorophyll"][0] - fits["chlorophyll"][1]) / fits["chlorophyll"][1])
    return heading, grid, out


class Scene25(VideoScene):
    number = 25

    def construct(self):
        heading, grid, out = truncated_layout(self)
        tag = label(f"{percent(out, 0)} out, and perfectly plausible", 34, VERMILION, weight=BOLD
                    ).next_to(grid, DOWN, 0.8)
        # "A search can also fail without saying so."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "Stop logistic regression after two iterations, ..."
        at(self, 0.3)
        self.play(FadeIn(grid[0]), FadeIn(grid[1]), run_time=self.share(0.12))
        self.play(FadeIn(grid[2]), run_time=self.share(0.1))
        # "... and the chlorophyll coefficient is 9% out, and perfectly plausible."
        at(self, 0.7)
        self.play(Indicate(VGroup(grid[1][3], grid[2][3]), color=VERMILION, scale_factor=1.15), FadeIn(tag),
                  run_time=self.share(0.15))
        self.finish()


class Scene26(VideoScene):
    number = 26

    def construct(self):
        heading, grid, out = truncated_layout(self)
        tag = label(f"{percent(out, 0)} out, and perfectly plausible", 34, VERMILION, weight=BOLD
                    ).next_to(grid, DOWN, 0.8)
        self.add(heading, grid, tag)
        flag = band(VGroup(grid[0][1], grid[1][1], grid[2][1]), PURPLE, 0.18)
        advice = card("check the flag,\nnot the coefficients", PURPLE, 36).next_to(grid, DOWN, 0.6)
        # "The only difference is a flag, 'converged', ..."
        self.play(FadeIn(flag), grid[1][1].animate.set_color(VERMILION), run_time=self.share(0.2))
        # "... and you have to ask for it."
        at(self, 0.5)
        self.play(FadeOut(tag), FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene27(VideoScene):
    number = 27

    def construct(self):
        sep = self.data("separation").iloc[0]
        heading = title("Give it the leaked catch weight", 46).to_edge(UP, buff=0.6)
        blocks = VGroup()
        for name, value, colour in (("coefficient", fixed(sep["estimate"], 0), BLUE),
                                    ("standard error", grouped(sep["se"]), ORANGE),
                                    ("p-value", fixed(sep["p"], 2), VERMILION)):
            blocks.add(VGroup(label(name, 30, SUBDUED), label(value, 72, colour, weight=BOLD)
                              ).arrange(DOWN, buff=0.25))
        blocks.arrange(RIGHT, buff=1.2).move_to([0, -0.4, 0])
        # "Or give it the leaked catch weight."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "The coefficient is minus 158, with a standard error of 13,515, and a p-value of 0.99."
        at(self, 0.3)
        self.play(FadeIn(blocks[0], shift=0.2 * UP), run_time=self.share(0.1))
        at(self, 0.52)
        self.play(FadeIn(blocks[1], shift=0.2 * UP), run_time=self.share(0.1))
        at(self, 0.8)
        self.play(FadeIn(blocks[2], shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        # Schematic: a likelihood that rises forever; only the cap (from the page's fit) is a number.
        cap = int(self.data("separation").iloc[0]["iterations"])
        heading = title("Not weak evidence: no best value", 46).to_edge(UP, buff=0.55)
        axes = plain_axes([0, 10, 1], [0, 4, 1], 9.5, 4.2).move_to([-0.3, -0.6, 0])
        ceiling = DashedLine(axes.c2p(0, 3.6), axes.c2p(10, 3.6), color=GREY)
        curve = axes.plot(lambda x: 3.6 * (1 - math.exp(-0.55 * x)), x_range=[0, 10, 0.05], color=BLUE,
                          stroke_width=6)
        x_name = label("size of the coefficient", 28, SUBDUED).next_to(axes, DOWN, 0.2)
        y_name = label("likelihood", 28, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.2)
        xs = [1, 2.5, 4, 5.5, 7, 8.5, 9.7]
        dots = VGroup(*[Dot(axes.c2p(x, 3.6 * (1 - math.exp(-0.55 * x))), radius=0.1, color=BLUE) for x in xs])
        never = label("always a little higher further on", 30, BLUE, weight=BOLD).move_to(axes.c2p(6.2, 2.4))
        stop = label(f"stopped by its cap: {cap} iterations", 30, VERMILION, weight=BOLD
                     ).move_to(axes.c2p(6.8, 1.2))
        separates = label("the predictor separates the classes", 32, INK).next_to(heading, DOWN, 0.3)
        # "That is not weak evidence."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(axes), FadeIn(x_name), FadeIn(y_name),
                  run_time=self.share(0.12))
        # "The predictor separates the classes, so there is no best value, ..."
        at(self, 0.2)
        self.play(FadeIn(separates), Create(curve), Create(ceiling), run_time=self.share(0.2))
        self.play(FadeIn(never), run_time=self.share(0.08))
        # "... and the search walked on until its cap of 25 iterations stopped it."
        at(self, 0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.4), run_time=self.share(0.2))
        self.play(FadeIn(stop), run_time=self.share(0.08))
        self.finish()


def runs_layout(scene):
    forests = scene.data("forest-runs")["rmse"]
    # The page prints each RMSE to four places and quotes the span of those: 0.0365, so 0.037.
    span = forests.round(4).max() - forests.round(4).min()
    starts = scene.data("kmeans-starts")["withinss"]
    heading = title("Different answers from each run", 46).to_edge(UP, buff=0.45)
    top, top_frame = chart([4.70, 4.78, 0.01], [0, 1, 1], 8.2, 0.01, [4.70, 4.72, 4.74, 4.76, 4.78], [],
                           "test RMSE", "", x_format="{:.2f}")
    top_frame.move_to([1.7, 0.9, 0])
    bottom, bottom_frame = chart([1080, 1160, 10], [0, 1, 1], 8.2, 0.01, [1080, 1100, 1120, 1140, 1160], [],
                                 "within-cluster sum of squares", "")
    bottom_frame.move_to([1.7, -2.0, 0])
    forest_dots = VGroup(*[Dot(top.c2p(v, 0) + 0.35 * UP, radius=0.11, color=BLUE, fill_opacity=0.7) for v in forests])
    # Equal values stack, so twenty starts show as ten piles.
    seen = {}
    kmeans_dots = VGroup()
    for v in starts:
        key = round(v, 3)
        seen[key] = seen.get(key, 0) + 1
        kmeans_dots.add(Dot(bottom.c2p(v, 0) + (0.12 + 0.24 * seen[key]) * UP, radius=0.1, color=VERMILION,
                            fill_opacity=0.8))
    forest_name = VGroup(label(f"{len(forests)} random forests", 30, BLUE, weight=BOLD),
                         label(f"span {fixed(span, 3)}", 30, BLUE)
                         ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(top_frame, LEFT, 0.4)
    kmeans_name = VGroup(label(f"{len(starts)} k-means runs", 30, VERMILION, weight=BOLD),
                         label(f"{starts.round(3).nunique()} different answers", 30, VERMILION)
                         ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(bottom_frame, LEFT, 0.4)
    return (heading, VGroup(top_frame, forest_dots, forest_name), VGroup(bottom_frame, kmeans_dots, kmeans_name))


class Scene29(VideoScene):
    number = 29

    def construct(self):
        heading, forests, kmeans = runs_layout(self)
        success = label("every one reported success", 32, GREEN, weight=BOLD).to_edge(DOWN, buff=0.35)
        # "Random algorithms land somewhere different each run."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "Five unseeded forests spanned 0.037 in error."
        at(self, 0.22)
        self.play(FadeIn(forests[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in forests[1]], lag_ratio=0.3),
                  FadeIn(forests[2]), run_time=self.share(0.18))
        # "Twenty k-means runs found ten different answers, and every one reported success."
        at(self, 0.5)
        self.play(FadeIn(kmeans[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in kmeans[1]], lag_ratio=0.1),
                  FadeIn(kmeans[2]), run_time=self.share(0.25))
        at(self, 0.85)
        self.play(FadeIn(success), run_time=self.share(0.08))
        self.finish()


class Scene30(VideoScene):
    number = 30

    def construct(self):
        heading, forests, kmeans = runs_layout(self)
        self.add(heading, forests, kmeans)
        seed = card("a seed gives reproducibility,\nnot stability", PURPLE, 44).move_to([0, 0.2, 0])
        spread = label("the spread is the resolution of your comparisons", 32, INK, weight=BOLD
                       ).to_edge(DOWN, buff=0.35)
        # "A seed makes a result reproducible, not stable."
        self.play(forests.animate.set_opacity(0.12), kmeans.animate.set_opacity(0.12), run_time=self.share(0.1))
        self.play(FadeIn(seed, scale=0.9), run_time=self.share(0.15))
        # "Remove it on purpose, and treat the spread as the resolution of every comparison you make."
        at(self, 0.55)
        self.play(FadeIn(spread), run_time=self.share(0.12))
        self.finish()


class Scene31(KeyPointScene):
    number, point = 31, 2


# A penalty is a prior (scenes 32–41) -------------------------------------------------------

def prior_layout(scene):
    """The temperature coefficient's likelihood, as the MAP page's figure draws it."""
    summary = scene.data("map-summary").iloc[0]
    b_hat, se, tau = summary["b_hat"], summary["se"], summary["tau"]
    heading = title(f"{int(summary['training'])} stations: the temperature coefficient", 44).to_edge(UP, buff=0.4)
    axes, frame = chart([-5, 15, 1], [0, 0.4, 0.1], 10.5, 4.6, [-5, 0, 5, 10, 15], [], "coefficient", "")
    for t in frame[1]:
        t.become(label(t.text.replace("-", "−"), 24, SUBDUED).move_to(t))
    frame.move_to([0, -0.7, 0])
    zero = DashedLine(axes.c2p(0, 0), axes.c2p(0, 0.4), color=GREY)
    likelihood = axes.plot(lambda b: normal_pdf(b, b_hat, se), x_range=[-5, 15, 0.05], color=GREY, stroke_width=6)
    return heading, axes, frame, zero, likelihood, summary


class Scene32(VideoScene):
    number = 32

    def construct(self):
        heading, axes, frame, zero, likelihood, summary = prior_layout(self)
        b_hat, se = summary["b_hat"], summary["se"]
        peak = axes.c2p(b_hat, normal_pdf(b_hat, b_hat, se))
        peak_text = label(f"maximum likelihood: {fixed(b_hat)}", 30, INK, weight=BOLD
                          ).move_to(axes.c2p(b_hat, 0.2))
        peak_line = DashedLine(peak, axes.c2p(b_hat, 0.18), color=GREY)
        spread = DoubleArrow(axes.c2p(b_hat, 0.1), axes.c2p(b_hat + se, 0.1), color=ORANGE, buff=0,
                             stroke_width=5, tip_length=0.2)
        spread_text = label(f"standard error {fixed(se)}", 30, ORANGE, weight=BOLD).next_to(spread, UP, 0.12)
        spread_text.align_to(spread, LEFT).shift(0.2 * RIGHT)
        zero_text = label("zero", 26, SUBDUED).next_to(zero, UP, 0.1)
        # "Back to the forty stations. Maximum likelihood looks only at the data in front of it, ..."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.12))
        # "... and gives temperature 8.59."
        at(self, 0.3)
        self.play(Create(likelihood), Create(peak_line), FadeIn(peak_text), run_time=self.share(0.18))
        # "But its standard error is 5.95: the data barely tell it from zero."
        at(self, 0.6)
        self.play(GrowFromCenter(spread), FadeIn(spread_text), run_time=self.share(0.12))
        at(self, 0.82)
        self.play(Create(zero), FadeIn(zero_text), run_time=self.share(0.1))
        self.finish()


class Scene33(VideoScene):
    number = 33

    def construct(self):
        coefficients = self.data("coefficients").set_index("term")
        heading = title("Two terms fighting", 48).to_edge(UP, buff=0.55)
        axes = plain_axes([0, 3, 1], [-8, 10, 2], 6.0, 5.2).move_to([-2.2, -0.6, 0])
        zero = Line(axes.c2p(0, 0), axes.c2p(3, 0), color=INK, stroke_width=3)
        bars = VGroup()
        for x, term, name, colour in ((1, "temperature_c", "temperature", BLUE),
                                      (2, "I(temperature_c^2)", "its square", ORANGE)):
            value = coefficients.loc[term, "mle"]
            base, top = axes.c2p(x, 0), axes.c2p(x, value)
            bar = Rectangle(width=1.2, height=abs(top[1] - base[1]), stroke_width=0, fill_color=colour,
                            fill_opacity=1).move_to(base, aligned_edge=DOWN if value > 0 else UP)
            text = label(("+" if value > 0 else "") + fixed(value), 38, colour, weight=BOLD
                         ).next_to(bar, UP if value > 0 else DOWN, 0.15)
            name_text = label(name, 28, colour, weight=BOLD).next_to(base, DOWN if value > 0 else UP, 0.2)
            bars.add(VGroup(bar, text, name_text))
        verdict = card("two collinear\nterms fighting,\nnot biology", VERMILION, 38).move_to([3.6, -0.4, 0])
        cancel = label("huge, opposite, partly cancelling", 30, SUBDUED).move_to([3.6, 1.6, 0])
        # "Temperature and its square take huge opposite values that partly cancel."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(zero), run_time=self.share(0.1))
        self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), run_time=self.share(0.15))
        self.play(GrowFromEdge(bars[1][0], UP), FadeIn(bars[1][1:]), run_time=self.share(0.15))
        self.play(FadeIn(cancel), run_time=self.share(0.1))
        # "That is two collinear terms fighting, not biology."
        at(self, 0.62)
        self.play(FadeIn(verdict, scale=0.9), run_time=self.share(0.12))
        self.finish()


class Scene34(VideoScene):
    number = 34

    def construct(self):
        heading, axes, frame, zero, likelihood, summary = prior_layout(self)
        b_hat, se, tau = summary["b_hat"], summary["se"], summary["tau"]
        names = VGroup(label("likelihood: what the data say", 28, GREY, weight=BOLD))
        self.add(heading, frame, zero, likelihood)
        prior = axes.plot(lambda b: normal_pdf(b, 0, tau), x_range=[-5, 15, 0.02], color=ORANGE, stroke_width=6)
        # The page's single-coefficient posterior: the figure's own formula.
        mode = b_hat * tau ** 2 / (tau ** 2 + se ** 2)
        sd = math.sqrt(1 / (1 / se ** 2 + 1 / tau ** 2))
        posterior = axes.plot(lambda b: normal_pdf(b, mode, sd), x_range=[-5, 15, 0.02], color=BLUE, stroke_width=7)
        names.add(label(f"prior: usually within ±{PRIOR_SCALE}", 28, ORANGE, weight=BOLD),
                  label("combined: pulled almost to zero", 28, BLUE, weight=BOLD))
        names.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(axes.c2p(9.5, 0.3))
        # "You know effects that large do not occur."
        self.play(FadeIn(names[0]), run_time=self.share(0.1))
        # "A prior says so: coefficients here are usually within about plus or minus one."
        at(self, 0.25)
        self.play(Create(prior), FadeIn(names[1]), run_time=self.share(0.2))
        # "Combined with the likelihood, it pulls the estimate almost to zero."
        at(self, 0.68)
        self.play(Create(posterior), FadeIn(names[2]), run_time=self.share(0.18))
        self.finish()


class Scene35(VideoScene):
    number = 35

    def construct(self):
        coefficients = self.data("coefficients")
        heading = title("MAP estimation is ridge regression", 46).to_edge(UP, buff=0.35)
        names = {"depth_m": "depth", "I(depth_m^2)": "depth²", "temperature_c": "temperature",
                 "I(temperature_c^2)": "temperature²", "chlorophyll_mg_m3": "chlorophyll",
                 "salinity_psu": "salinity", "substratemud": "mud", "substraterock": "rock",
                 "substratesand": "sand", "seasonsummer": "summer", "seasonautumn": "autumn",
                 "seasonwinter": "winter"}
        rows = [["", "MAP", "ridge"]]
        for _, r in coefficients.iterrows():
            rows.append([names[r["term"]], fixed(r["map"], 4), fixed(r["ridge"], 4)])
        grid = table(rows, [2.6, 1.8, 1.8], 26, row_gap=0.44).move_to([-3.2, -0.5, 0])
        same = label("identical", 32, GREEN, weight=BOLD).next_to(grid, RIGHT, 0.4).align_to(grid, UP)
        point = VGroup(label("the penalty is", 34, SUBDUED),
                       label("a Normal prior", 44, PURPLE, weight=BOLD),
                       label("on the coefficients", 34, SUBDUED)).arrange(DOWN, buff=0.2).move_to([3.6, -0.4, 0])
        # "That is MAP estimation, and written out, it is exactly ridge regression."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.12))
        self.play(FadeIn(grid, lag_ratio=0.05), run_time=self.share(0.25))
        self.play(FadeIn(same), run_time=self.share(0.08))
        # "The penalty is a Normal prior on the coefficients."
        at(self, 0.65)
        self.play(FadeIn(point, shift=0.2 * LEFT), run_time=self.share(0.15))
        self.finish()


class Scene36(VideoScene):
    number = 36

    def construct(self):
        # The MAP page's example of what a flat prior allows.
        small, big = FLAT_PRIOR
        heading = title("Maximum likelihood is a flat prior", 46).to_edge(UP, buff=0.6)
        sub = label("not assumption-free", 34, VERMILION, weight=BOLD).next_to(heading, DOWN, 0.3)
        axes = plain_axes([0, 3, 1], [0, 2, 1], 9.0, 3.0).move_to([0, -1.1, 0])
        flat = Line(axes.c2p(0, 1.2), axes.c2p(3, 1.2), color=GREY, stroke_width=6)
        marks = VGroup()
        for x, value in ((0.5, small), (2.5, big)):
            stem = Line(axes.c2p(x, 0), axes.c2p(x, 1.2), color=BLUE, stroke_width=6)
            text = label(f"a coefficient of {value:g}", 30, BLUE, weight=BOLD).next_to(axes.c2p(x, 0), DOWN, 0.2)
            marks.add(VGroup(stem, Dot(axes.c2p(x, 1.2), radius=0.1, color=BLUE), text))
        equal = label("exactly as plausible", 32, INK, weight=BOLD).next_to(flat, UP, 0.3)
        # "So maximum likelihood is not assumption-free."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.15))
        self.play(FadeIn(sub), Create(flat), run_time=self.share(0.15))
        # "It is a prior that finds a coefficient of 900 exactly as plausible as 0.9."
        at(self, 0.5)
        self.play(FadeIn(marks[1]), run_time=self.share(0.1))
        self.play(FadeIn(marks[0]), FadeIn(equal), run_time=self.share(0.12))
        self.finish()


def scores_layout(scene):
    summary = scene.data("map-summary").iloc[0]
    heading = title(f"The puzzle: error on the other {int(summary['testing'])} stations", 42).to_edge(UP, buff=0.5)
    axes, frame = chart([4.45, 4.9, 0.05], [0, 1, 1], 11.6, 0.01, [4.5, 4.6, 4.7, 4.8, 4.9], [],
                        "test RMSE (individuals)", "", x_format="{:.1f}")
    frame.move_to([-0.3, -2.1, 0])
    marks = VGroup()
    for value, name, colour in ((summary["mean_rmse"], "the mean,\neverywhere", GREY),
                                (summary["mle_rmse"], "Fit 1:\nmaximum likelihood", ORANGE),
                                (summary["map_rmse"], "Fit 2:\nwith the prior", BLUE)):
        stem = Line(axes.c2p(value, 0), axes.c2p(value, 0) + 1.7 * UP, color=colour, stroke_width=5)
        dot = Dot(axes.c2p(value, 0), radius=0.12, color=colour)
        text = VGroup(label(fixed(value, 3), 36, colour, weight=BOLD),
                      *[label(t, 26, colour) for t in name.split("\n")]).arrange(DOWN, buff=0.06)
        if colour == GREY:   # beside its stem, clear of the gain between the two
            text.next_to(stem.get_end(), RIGHT, 0.15, aligned_edge=UP)
        else:
            text.next_to(stem, UP, 0.12)
        marks.add(VGroup(stem, dot, text))
    return heading, axes, frame, marks, summary


def gain_arrow(axes, summary):
    """Maximum likelihood's gain over the mean: an arrow between the two, its size beneath."""
    arrow = Arrow(axes.c2p(summary["mean_rmse"], 0) + 0.8 * UP, axes.c2p(summary["mle_rmse"], 0) + 0.8 * UP,
                  color=ORANGE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.35)
    better = (summary["mean_rmse"] - summary["mle_rmse"]) / summary["mean_rmse"]
    gain = label(f"about {percent(better, 0)} better", 22, ORANGE, weight=BOLD).next_to(arrow, DOWN, 0.1)
    return arrow, gain


class Scene37(VideoScene):
    number = 37

    def construct(self):
        heading, axes, frame, marks, summary = scores_layout(self)
        arrow, gain = gain_arrow(axes, summary)
        # "Now, the puzzle. On the other 680 stations, ..."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.15))
        # "... predicting the mean everywhere gives an error of 4.850."
        at(self, 0.35)
        self.play(FadeIn(marks[0]), run_time=self.share(0.12))
        # "Maximum likelihood gives 4.745, about 2% better."
        at(self, 0.68)
        self.play(FadeIn(marks[1]), GrowArrow(arrow), FadeIn(gain), run_time=self.share(0.15))
        self.finish()


class Scene38(VideoScene):
    number = 38

    def construct(self):
        heading, axes, frame, marks, summary = scores_layout(self)
        arrow, gain = gain_arrow(axes, summary)
        self.add(heading, frame, marks[0], marks[1], arrow, gain)
        times = (summary["mean_rmse"] - summary["map_rmse"]) / (summary["mean_rmse"] - summary["mle_rmse"])
        big = Arrow(axes.c2p(summary["mean_rmse"], 0) + 0.25 * UP, axes.c2p(summary["map_rmse"], 0) + 0.25 * UP,
                    color=BLUE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.1)
        verdict = card(f"more than {int(times)} × the improvement, from a term with no data", BLUE, 30
                       ).move_to([0, 2.2, 0])
        # "The fit with the prior gives 4.495: ..."
        self.play(FadeIn(marks[2]), GrowArrow(big), run_time=self.share(0.2))
        # "... more than three times the improvement, from a term with no data in it."
        at(self, 0.35)
        self.play(FadeIn(verdict, scale=0.9), run_time=self.share(0.15))
        self.finish()


def curve_layout(scene):
    curve = scene.data("lambda-curve")
    summary = scene.data("map-summary").iloc[0]
    heading = title("Tightening the prior", 46).to_edge(UP, buff=0.4)
    logs = np.log10(curve["lambda"])
    axes, frame = chart([-2, math.log10(500), 1], [3.2, 5.0, 0.4], 8.6, 5.0, [-2, -1, 0, 1, 2],
                        [3.2, 3.6, 4.0, 4.4, 4.8], "λ, the prior's strength (log scale)", "RMSE (individuals)",
                        x_format="{:g}", y_format="{:.1f}")
    for t, v in zip(frame[1], [-2, -1, 0, 1, 2]):
        t.become(label(f"{10 ** v:g}", 24, SUBDUED).move_to(t))
    frame.move_to([-2.0, -0.5, 0])
    lines = VGroup()
    for column, colour in (("train", GREEN), ("test", BLUE)):
        lines.add(VMobject(color=colour, stroke_width=6).set_points_smoothly(
            [axes.c2p(x, y) for x, y in zip(logs, curve[column])]))
    mean = DashedLine(axes.c2p(-2, summary["mean_rmse"]), axes.c2p(math.log10(500), summary["mean_rmse"]),
                      color=GREY)
    mean_text = label("the mean, everywhere", 24, SUBDUED).next_to(mean, UP, 0.08).align_to(mean, RIGHT)
    names = VGroup(label("training: only rises", 30, GREEN, weight=BOLD),
                   label("test: falls, then rises", 30, BLUE, weight=BOLD))
    names[0].move_to(axes.c2p(-0.8, 3.7))
    names[1].move_to(axes.c2p(-0.8, 4.3))
    return heading, axes, frame, lines, mean, mean_text, names, curve, summary


class Scene39(VideoScene):
    number = 39

    def construct(self):
        heading, axes, frame, lines, mean, mean_text, names, curve, summary = curve_layout(self)
        pick = label("the training curve\ncannot choose λ", 32, PURPLE, weight=BOLD).move_to([4.8, 0.9, 0])
        # "As the prior tightens, training error only rises."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), Create(mean), FadeIn(mean_text),
                  run_time=self.share(0.12))
        self.play(Create(lines[0]), FadeIn(names[0]), run_time=self.share(0.2))
        # "Test error falls, then rises."
        at(self, 0.4)
        self.play(Create(lines[1]), FadeIn(names[1]), run_time=self.share(0.2))
        # "The training curve cannot choose the strength for you."
        at(self, 0.72)
        self.play(FadeIn(pick), run_time=self.share(0.1))
        self.finish()


class Scene40(VideoScene):
    number = 40

    def construct(self):
        heading, axes, frame, lines, mean, mean_text, names, curve, summary = curve_layout(self)
        self.add(heading, frame, mean, mean_text, lines, names)
        tight = axes.c2p(math.log10(500), curve["test"].iloc[-1])
        zone = Rectangle(width=axes.c2p(math.log10(500), 0)[0] - axes.c2p(1.6, 0)[0], height=5.0, stroke_width=0,
                         fill_color=VERMILION, fill_opacity=0.1).move_to(axes.c2p(1.6, 3.2), aligned_edge=DL)
        wrong = card("a prior can be wrong:\na tight one shrinks\nreal effects too", VERMILION, 28
                     ).move_to([5.0, 0.8, 0])
        methods = label("an assumption,\nlike the loss", 30, PURPLE, weight=BOLD).next_to(wrong, DOWN, 0.5)
        # "And a prior can be wrong. A tight one shrinks real effects too."
        self.play(FadeIn(zone), Indicate(Dot(tight, color=BLUE), scale_factor=2), run_time=self.share(0.15))
        self.play(FadeIn(wrong, scale=0.9), run_time=self.share(0.15))
        # "Like the loss, it is an assumption, and it belongs in your methods."
        at(self, 0.6)
        self.play(FadeIn(methods), run_time=self.share(0.12))
        self.finish()


class Scene41(KeyPointScene):
    number, point = 41, 3


# The quiz (scenes 42–43) ------------------------------------------------------------------

class Scene42(QuizScene):
    number = 42
    question = ("A colleague fits ridge regression", "with depth in millimetres", "and temperature in degrees,",
                "without standardising. What goes wrong?")


class Scene43(VideoScene):
    number = 43

    def construct(self):
        # Schematic: one prior scale, two units for depth.
        answer = label("The prior needs a unit", 52, VERMILION, weight=BOLD).to_edge(UP, buff=0.6)
        prior = label(f"\"coefficients are about ±{PRIOR_SCALE}\"", 38, ORANGE, weight=BOLD).next_to(answer, DOWN, 0.5)
        rows = VGroup(
            VGroup(label("depth in metres", 34, INK, weight=BOLD), label("a coefficient per metre", 30, SUBDUED),
                   label("penalised as intended", 32, GREEN, weight=BOLD)),
            VGroup(label("depth in millimetres", 34, INK, weight=BOLD),
                   label("a coefficient a thousand times smaller", 30, SUBDUED),
                   label("barely penalised at all", 32, VERMILION, weight=BOLD)))
        for row in rows:
            row.arrange(DOWN, buff=0.15)
        rows.arrange(RIGHT, buff=1.2).move_to([0, -0.8, 0])
        fix = card("standardise first", GREEN, 38).to_edge(DOWN, buff=0.45)
        # "The prior says coefficients are about plus or minus one, and that means nothing without a unit."
        self.play(FadeIn(answer), FadeIn(prior), run_time=self.share(0.2))
        # "Depth in millimetres is barely penalised at all."
        at(self, 0.5)
        self.play(FadeIn(rows[0]), run_time=self.share(0.1))
        self.play(FadeIn(rows[1]), run_time=self.share(0.12))
        # "Standardise first."
        at(self, 0.85)
        self.play(FadeIn(fix, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


# The recap (scenes 44–46) and the end card (scene 47) --------------------------------------

class Scene44(RecapScene):
    number, point = 44, 1


class Scene45(RecapScene):
    number, point = 45, 2


class Scene46(RecapScene):
    number, point = 46, 3


class Scene47(EndCardScene):
    number = 47
