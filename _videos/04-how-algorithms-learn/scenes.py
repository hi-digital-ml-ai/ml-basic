"""Manim scenes for the how-algorithms-learn video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/04-how-algorithms-learn
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is built on three ideas from the section, each with the reason it matters:
the loss, the search and the assumptions inside the loss. Scenes marked "page results" read
visuals/data/*.csv, which tools/figures-for-video.R writes from the pages. The others
are schematic: made-up shapes, never numbers that could pass for survey results. The
opening, key-point, recap, quiz and end-card scenes are shared (mlbasic_video.py) and
read PROMISES, ANSWERS and RECAP from here.
"""

import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["The number every fit makes small",
            "The search that finds the parameters",
            "The assumptions inside the loss"]
ANSWERS = ["The loss decides\nwhat the model\npays attention to",
           "A search can fail quietly:\ncheck that it finished",
           "Every loss assumes\na distribution;\na prior adds a penalty"]
RECAP = ["The loss decides what a model attends to",
         "Check that the search finished",
         "A loss assumes a distribution; a prior, a penalty"]

# Stated in the pages' prose rather than computed: the misses the loss page prices and
# the rate at which the walk never arrives.
MISSES = (1, 10)
DIVERGING_RATE = 0.8

LOSS_COLOURS = {"Squared error": BLUE, "Absolute error": ORANGE}
RATE_COLOURS = {0.02: ORANGE, 0.3: BLUE}


# Helpers ----------------------------------------------------------------------------------

def narration_text(scene):
    return " ".join(scene.script.scenes[scene.number - 1].narration.split())


def position(scene, phrase):
    """Where a phrase starts in the narration, as a fraction of it."""
    text = narration_text(scene)
    start = text.find(phrase)
    if start < 0:
        raise ValueError(f"scene {scene.number}: {phrase!r} is not in the narration")
    return start / len(text)


def at(scene, fraction):
    """Wait until this fraction of the narration."""
    scene.wait(max(scene.share(fraction) - scene.time, 0.01))


def cue(scene, phrase):
    """Wait until the narration reaches this phrase, judged by its place in the text."""
    at(scene, position(scene, phrase))


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name, size=24,
          x_format="{:g}", y_format="{:g}"):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
    axes = plain_axes(x_range, y_range, x_length, y_length)
    tx = VGroup(*[label(x_format.format(v).replace("-", "−"), size, SUBDUED).next_to(
        axes.c2p(v, y_range[0]), DOWN, 0.15) for v in x_ticks])
    ty = VGroup(*[label(y_format.format(v).replace("-", "−"), size, SUBDUED).next_to(
        axes.c2p(x_range[0], v), LEFT, 0.15) for v in y_ticks])
    xn = label(x_name, 26, SUBDUED).next_to(tx if len(tx) else axes, DOWN, 0.2) if x_name else VGroup()
    yn = label(y_name, 26, SUBDUED).rotate(PI / 2).next_to(ty if len(ty) else axes, LEFT, 0.2) \
        if y_name else VGroup()
    return axes, VGroup(axes, tx, ty, xn, yn)


def card(text, colour=PURPLE, size=40):
    words = VGroup(*[label(t, size, colour, weight=BOLD) for t in text.split("\n")]).arrange(DOWN, buff=0.15)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def panel(heading, lines, colour, width=3.6, height=2.4, size=28):
    """A card in the diagrams' house style: pale fill, a coloured strip along the top."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color="#1b6a87",
                           stroke_width=3, fill_color="#f4f8fa", fill_opacity=1)
    strip = Rectangle(width=width, height=0.12, stroke_width=0, fill_color=colour, fill_opacity=1).align_to(box, UP)
    words = VGroup(label(heading, size + 6, INK, weight=BOLD),
                   *[label(t, size, SUBDUED) for t in lines]).arrange(DOWN, buff=0.15)
    return VGroup(box, strip, words.move_to(box))


def cross(size=0.4, colour=VERMILION):
    return VGroup(Line(size * UL, size * DR, color=colour, stroke_width=8),
                  Line(size * UR, size * DL, color=colour, stroke_width=8)).scale(0.5)


def fixed(value, digits=2):
    """A number to `digits` places, rounded half up as the pages' prose rounds."""
    text = f"{Decimal(str(value)).quantize(Decimal(1).scaleb(-digits), ROUND_HALF_UP)}"
    return text.replace("-", "−")


def percent(value, digits=1):
    return f"{Decimal(str(100 * value)).quantize(Decimal(1).scaleb(-digits), ROUND_HALF_UP)}%"


def grouped(value):
    """A whole number with a thousands separator, as the pages print 13,515."""
    text = f"{int(Decimal(str(value)).quantize(Decimal(1), ROUND_HALF_UP)):,}"
    return text.replace("-", "−")


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




def bell(x, mean, sd):
    """A Normal curve scaled to a peak of 1: the shape, for figures without a y axis."""
    return math.exp(-0.5 * ((x - mean) / sd) ** 2)


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("the one number", "the search that", "and the assumptions"))


# The number a fit makes small (scenes 2–8) -------------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        # Schematic: the fitting loop.
        heading = title("Fitting is a search", 50).to_edge(UP, buff=0.6)
        steps = ["guess the\nparameters", "score how wrong\nthe guess is", "adjust and repeat"]
        colours = [BLUE, VERMILION, GREEN]
        points = [[-4.2, -1.6, 0], [0, 0.7, 0], [4.2, -1.6, 0]]
        boxes = VGroup()
        for text, colour, point in zip(steps, colours, points):
            words = VGroup(*[label(t, 34, colour, weight=BOLD) for t in text.split("\n")]).arrange(DOWN, buff=0.1)
            box = RoundedRectangle(width=4.6, height=1.6, corner_radius=0.2, stroke_color=colour, stroke_width=4,
                                   fill_color=colour, fill_opacity=0.07).move_to(point)
            boxes.add(VGroup(box, words.move_to(box)))
        arrows = VGroup(
            CurvedArrow(boxes[0].get_top() + 0.1 * UP, boxes[1].get_left() + 0.1 * LEFT, angle=-PI / 4, color=INK),
            CurvedArrow(boxes[1].get_right() + 0.1 * RIGHT, boxes[2].get_top() + 0.1 * UP, angle=-PI / 4,
                        color=INK),
            CurvedArrow(boxes[2].get_bottom() + 0.1 * DOWN, boxes[0].get_bottom() + 0.1 * DOWN, angle=-PI / 3,
                        color=INK))
        learned = label("parameters: the numbers it learns from the data", 30, SUBDUED).next_to(heading, DOWN, 0.3)
        # "Every model in this course was fitted the same way."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "The algorithm guesses its parameters, the numbers it learns from the data."
        cue(self, "The algorithm guesses")
        self.play(FadeIn(boxes[0]), run_time=self.share(0.06))
        cue(self, "the numbers it learns")
        self.play(FadeIn(learned), run_time=self.share(0.06))
        # "It scores how wrong that guess is,"
        cue(self, "It scores")
        self.play(Create(arrows[0]), FadeIn(boxes[1]), run_time=self.share(0.07))
        # "adjusts the parameters to do better, and repeats."
        cue(self, "adjusts the parameters")
        self.play(Create(arrows[1]), FadeIn(boxes[2]), Create(arrows[2]), run_time=self.share(0.08))
        # "Fitting is a search for the best score."
        cue(self, "Fitting is a search")
        self.play(Indicate(heading, color=INK, scale_factor=1.06), run_time=self.share(0.08))
        self.finish()


# Made-up stations for the residual scene: a schematic, not the survey.
SKETCH_X = [0.8, 1.6, 2.3, 3.1, 3.9, 4.6, 5.4, 6.2, 7.0, 7.7, 8.5, 9.2]
SKETCH_Y = [1.6, 1.2, 2.6, 2.1, 3.8, 2.9, 4.6, 3.7, 7.0, 4.4, 5.2, 6.4]
SKETCH_POINT = 8          # the station whose miss is drawn


class Scene03(VideoScene):
    number = 3

    def construct(self):
        # Schematic: one residual.
        axes = plain_axes([0, 10, 1], [0, 8, 1], 9.0, 4.8).move_to([-0.6, -0.6, 0])
        x_name = label("an input", 26, SUBDUED).next_to(axes, DOWN, 0.2)
        y_name = label("the count", 26, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.2)
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.08, color=GREY) for x, y in zip(SKETCH_X, SKETCH_Y)])
        fitted = lambda x: 1.0 + 0.55 * x        # noqa: E731
        line = axes.plot(fitted, x_range=[0, 10], color=BLUE, stroke_width=6)
        line_name = label("the model's prediction", 26, BLUE, weight=BOLD).move_to(axes.c2p(7.6, 1.6))
        x, y = SKETCH_X[SKETCH_POINT], SKETCH_Y[SKETCH_POINT]
        dots[SKETCH_POINT].set_color(INK).scale(1.4)
        gap = Line(axes.c2p(x, y), axes.c2p(x, fitted(x)), color=VERMILION, stroke_width=6)
        gap_name = label("residual", 30, VERMILION, weight=BOLD).next_to(gap, RIGHT, 0.15).shift(0.3 * UP)
        formula = label("residual = observed − predicted", 36, VERMILION, weight=BOLD).to_edge(UP, buff=0.5)
        noise = VGroup(label("noise: what the station's", 28, GREEN, weight=BOLD),
                       label("conditions do not decide", 28, GREEN, weight=BOLD),
                       *[label(t, 26, GREEN) for t in ("patchy animals", "a net that fished badly", "chance")]
                       ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        noise.align_to(axes, LEFT).align_to(axes, UP).shift(0.4 * RIGHT + 0.1 * DOWN)
        # The other stations' misses, faint, once noise is named: every station has one.
        others = VGroup(*[Line(axes.c2p(px, py), axes.c2p(px, fitted(px)), color=GREEN, stroke_width=3,
                               stroke_opacity=0.6)
                          for i, (px, py) in enumerate(zip(SKETCH_X, SKETCH_Y)) if i != SKETCH_POINT])
        note = card("even the best fit\nleaves residuals", PURPLE, 28).to_edge(RIGHT, buff=0.3).shift(0.3 * DOWN)
        # "The score is built from residuals."
        self.play(FadeIn(VGroup(axes, x_name, y_name)), FadeIn(dots), run_time=self.share(0.05))
        self.play(Create(line), FadeIn(line_name), run_time=self.share(0.06))
        # "A residual is how far one prediction missed: the observed count minus the predicted one."
        cue(self, "A residual is")
        self.play(Create(gap), FadeIn(gap_name), run_time=self.share(0.05))
        cue(self, "the observed count")
        self.play(FadeIn(formula, shift=0.2 * DOWN), run_time=self.share(0.05))
        # "Part of every residual is noise, the part of a count that the station's conditions do not decide,"
        cue(self, "Part of every")
        self.play(FadeIn(noise[:2]), Create(others), run_time=self.share(0.06))
        # "such as patchy animals, a net that fished badly, or chance."
        cue(self, "such as patchy")
        self.play(FadeIn(noise[2]), run_time=self.share(0.03))
        cue(self, "a net that")
        self.play(FadeIn(noise[3]), run_time=self.share(0.03))
        cue(self, "or chance")
        self.play(FadeIn(noise[4]), run_time=self.share(0.03))
        # "No model can predict it, so even the best fit leaves residuals."
        cue(self, "so even the best")
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.05))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        # The two losses as the page defines them; a schematic of the definitions, not results.
        heading = title("A loss turns each miss into a penalty", 44).to_edge(UP, buff=0.45)
        score = label("the score = the average penalty", 30, PURPLE, weight=BOLD).next_to(heading, DOWN, 0.2)
        axes, frame = chart([-10, 10, 1], [0, 100, 10], 7.2, 4.4, [-10, -5, 0, 5, 10], [0, 50, 100],
                            "residual", "penalty")
        frame.move_to([-2.6, -0.9, 0])
        small, big = MISSES
        curves = VGroup(axes.plot(lambda r: r * r, x_range=[-10, 10, 0.05], color=BLUE, stroke_width=6),
                        axes.plot(abs, x_range=[-10, 10, 0.05], color=ORANGE, stroke_width=6))
        marks = VGroup(Dot(axes.c2p(big, big * big), radius=0.1, color=BLUE),
                       Dot(axes.c2p(big, big), radius=0.1, color=ORANGE))
        rows = VGroup()
        for name, times, colour in (("squared error", big * big // small, BLUE),
                                    ("absolute error", big // small, ORANGE)):
            rows.add(VGroup(label(name, 34, colour, weight=BOLD),
                            label(f"a miss of {big} costs {times} ×", 30, colour),
                            label(f"a miss of {small}", 30, colour)).arrange(DOWN, buff=0.1, aligned_edge=LEFT))
        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([3.9, -0.6, 0])
        # "A loss function turns each miss into a penalty, and the average penalty is the score."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.1))
        cue(self, "and the average penalty")
        self.play(FadeIn(score), run_time=self.share(0.06))
        # "The two common losses treat big misses very differently."
        # "Under squared error, a miss of 10 costs a hundred times a miss of 1."
        cue(self, "Under squared error")
        self.play(Create(curves[0]), FadeIn(rows[0]), FadeIn(marks[0], scale=0.5), run_time=self.share(0.12))
        # "Under absolute error, only ten times."
        cue(self, "Under absolute error")
        self.play(Create(curves[1]), FadeIn(rows[1]), FadeIn(marks[1], scale=0.5), run_time=self.share(0.1))
        self.finish()


def lines_layout(scene):
    """Abundance against chlorophyll at every station, with the two fitted lines."""
    stations = scene.data("stations")
    axes, frame = chart([0, 14, 1], [0, 40, 5], 8.6, 5.0, [0, 2, 4, 6, 8, 10, 12, 14], [0, 10, 20, 30, 40],
                        "chlorophyll (mg m⁻³)", "abundance (animals)")
    frame.move_to([-1.6, -0.6, 0])
    dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.035, color=GREY, fill_opacity=0.45)
                    for x, y in zip(stations["chlorophyll"], stations["abundance"])])
    losses = scene.data("two-losses").set_index("loss")
    lines, names = VGroup(), VGroup()
    for name, row in losses.iterrows():
        lines.add(Line(axes.c2p(0, row["intercept"]), axes.c2p(14, row["intercept"] + 14 * row["slope"]),
                       color=LOSS_COLOURS[name], stroke_width=6))
        names.add(label(name.lower(), 30, LOSS_COLOURS[name], weight=BOLD))
    names.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.9, 1.0, 0])
    return axes, frame, dots, lines, names, stations


class Scene05(VideoScene):
    number = 5

    def construct(self):
        # Page results: loss-functions.qmd#fig-two-lines.
        axes, frame, dots, lines, names, stations = lines_layout(self)
        heading = title("Same data, two losses, two lines", 44).to_edge(UP, buff=0.4)
        count = label(f"{len(stations)} stations", 30, SUBDUED).next_to(names, DOWN, 0.5, aligned_edge=LEFT)
        # "That difference changes the answer."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.12))
        # "On the survey's 749 stations,"
        cue(self, "On the survey")
        self.play(FadeIn(dots, lag_ratio=0.002), FadeIn(count), run_time=self.share(0.15))
        # "the two losses draw two different lines through exactly the same data."
        cue(self, "the two losses draw")
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.4), FadeIn(names), run_time=self.share(0.25))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        # Page results: loss-functions.qmd, the worst 5% and the largest catch removed.
        share = self.data("error-share").iloc[0]
        drop = self.data("drop-one").set_index("loss")
        heading = title("Squared error listens to big misses", 44).to_edge(UP, buff=0.5)
        axes = plain_axes([0, 1, 0.1], [0, 1, 1], 8.0, 1.0).move_to([1.6, 1.4, 0])
        whole = hbar(axes, 0.5, 1, BLUE, 0.7).set_fill(opacity=0.15)
        worst = hbar(axes, 0.5, share["squared_share"], BLUE, 0.7)
        value = label(percent(share["squared_share"], 0), 36, BACKGROUND, weight=BOLD).move_to(worst)
        who = VGroup(label(f"{int(share['worst_stations'])} stations", 34, INK, weight=BOLD),
                     label(f"5% of {int(share['stations'])}", 28, SUBDUED)).arrange(DOWN, buff=0.08)
        who.next_to(whole, LEFT, 0.4)
        of = label("of the total squared error", 28, BLUE).next_to(whole, DOWN, 0.2)
        question = label("does the slope we report rest on a few stations?", 32, PURPLE, weight=BOLD
                         ).move_to([0, -0.4, 0])
        catch = int(drop.loc["Squared error", "largest_catch"])
        removed = label(f"remove one large catch ({catch} animals) and refit", 32, INK).move_to([0, -1.3, 0])
        moves = VGroup(*[
            VGroup(label(f"{loss.lower()} slope moves", 34, colour),
                   label(percent(abs(drop.loc[loss, "change"])), 40, colour, weight=BOLD)).arrange(RIGHT, buff=0.25)
            for loss, colour in LOSS_COLOURS.items()
        ]).arrange(DOWN, buff=0.3).next_to(removed, DOWN, 0.4)
        # "Squared error listens hardest to the biggest misses."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "Just 37 stations, 5 per cent of the data, supply half of it."
        cue(self, "Just 37")
        self.play(FadeIn(who), FadeIn(whole), run_time=self.share(0.06))
        cue(self, "supply half")
        self.play(GrowFromEdge(worst, LEFT), FadeIn(value), FadeIn(of), run_time=self.share(0.07))
        # "That matters if the slope we would report rests on those few stations."
        cue(self, "That matters")
        self.play(FadeIn(question), run_time=self.share(0.06))
        # "So remove one large catch, a single haul a repeat survey could easily miss, and refit."
        cue(self, "So remove one")
        self.play(FadeIn(removed), run_time=self.share(0.06))
        # "The squared-error slope moves by 13.5 per cent; the absolute-error slope, by 2.1."
        cue(self, "The squared-error slope")
        self.play(FadeIn(moves[0], shift=0.2 * UP), run_time=self.share(0.06))
        cue(self, "the absolute-error slope")
        self.play(FadeIn(moves[1], shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        # Schematic: the same large catches, read two ways.
        heading = title("Which loss is right?", 50).to_edge(UP, buff=0.6)
        cards = VGroup()
        for what, then, colour in (("a real shoal", "let squared error\nlisten to it", BLUE),
                                   ("a net that fished badly", "absolute error\nis safer", ORANGE)):
            head = label("if a big catch is", 28, SUBDUED)
            what_text = label(what, 36, INK, weight=BOLD)
            arrow = Arrow(UP, DOWN, color=colour, buff=0).scale(0.4)
            then_text = VGroup(*[label(t, 34, colour, weight=BOLD) for t in then.split("\n")]).arrange(DOWN, buff=0.08)
            inner = VGroup(head, what_text, arrow, then_text).arrange(DOWN, buff=0.25)
            box = RoundedRectangle(width=5.8, height=3.6, corner_radius=0.2, stroke_color=colour, stroke_width=4,
                                   fill_color=colour, fill_opacity=0.05)
            cards.add(VGroup(box, inner.move_to(box)))
        cards.arrange(RIGHT, buff=0.7).move_to([0, 0.0, 0])
        choice = label("the data cannot tell you:\nit is a choice about your science", 32, PURPLE, weight=BOLD
                       ).to_edge(DOWN, buff=0.4)
        # "So which loss is right?"
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "If the big catches are real shoals, they matter, and squared error should listen to them."
        cue(self, "If the big catches")
        self.play(FadeIn(cards[0], shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "If they come from a net that fished badly, absolute error is safer."
        cue(self, "If they come")
        self.play(FadeIn(cards[1], shift=0.2 * LEFT), run_time=self.share(0.1))
        # "The data cannot tell you which. It is a choice about your science, so say which loss you used."
        cue(self, "The data cannot")
        self.play(FadeIn(choice), run_time=self.share(0.1))
        self.finish()


class Scene08(KeyPointScene):
    number, point = 8, 1


# The search that finds the parameters (scenes 9–14) ----------------------------------------

class Scene09(VideoScene):
    number = 9

    def construct(self):
        # Schematic: the score as a landscape over two parameters.
        cards = VGroup(card("a straight line: a formula, one step", GREEN, 30),
                       card("most models: a search", BLUE, 30)).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.4)
        axes = plain_axes([-4, 4, 1], [-3, 3, 1], 7.0, 4.8).move_to([-1.2, -1.1, 0])
        x_name = label("one parameter", 26, SUBDUED).next_to(axes, DOWN, 0.2)
        y_name = label("another", 26, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.2)
        rings = VGroup(*[Ellipse(width=1.3 * k, height=0.75 * k, color=GRID, stroke_width=4).rotate(-0.4)
                         .move_to(axes.c2p(0.6, -0.4)) for k in (1, 2, 3, 4, 5)])
        best = cross(0.5, INK).move_to(axes.c2p(0.6, -0.4))
        best_name = label("the best parameters:\nthe lowest point", 30, INK, weight=BOLD).move_to([5.0, -0.2, 0])
        pointer = Arrow(best_name.get_left() + 0.1 * LEFT, best.get_right() + 0.15 * RIGHT, color=INK, buff=0.1,
                        stroke_width=4)
        score = label("rings: equal score", 26, SUBDUED).move_to([5.0, -2.4, 0])
        # "For a straight line, a formula gives the best parameters in one step."
        self.play(FadeIn(cards[0], shift=0.2 * DOWN), run_time=self.share(0.1))
        # "Most models have no formula, so the algorithm has to search."
        cue(self, "Most models")
        self.play(FadeIn(cards[1], shift=0.2 * DOWN), run_time=self.share(0.08))
        # "Picture the score as a landscape."
        cue(self, "Picture the score")
        self.play(FadeIn(VGroup(axes, x_name, y_name)), LaggedStart(*[Create(r) for r in rings[::-1]], lag_ratio=0.2),
                  FadeIn(score), run_time=self.share(0.15))
        # "The best parameters sit at its lowest point."
        cue(self, "The best parameters")
        self.play(FadeIn(best, scale=0.5), GrowArrow(pointer), FadeIn(best_name), run_time=self.share(0.1))
        self.finish()


def bowl_axes():
    return plain_axes([-4, 4, 1], [0, 16, 4], 6.8, 4.2).move_to([-3.4, -0.6, 0])


class Scene10(VideoScene):
    number = 10

    def construct(self):
        # Schematic: a walk down a bowl.
        heading = title("Gradient descent", 50).to_edge(UP, buff=0.6)
        axes = bowl_axes()
        curve = axes.plot(lambda x: x * x, x_range=[-4, 4, 0.05], color=GREY, stroke_width=6)
        xs = [-3.6, -2.2, -1.2, -0.55, -0.2]
        dots = [Dot(axes.c2p(x, x * x), radius=0.13, color=BLUE) for x in xs]
        slope = Line(axes.c2p(-4.3, 4.3 * 7.2 - 12.96), axes.c2p(-2.9, 2.9 * 7.2 - 12.96), color=VERMILION,
                     stroke_width=6)
        notes = VGroup(label("find which way is downhill", 34, VERMILION, weight=BOLD),
                       label("take a step", 34, BLUE, weight=BOLD),
                       label("repeat until it is flat", 34, GREEN, weight=BOLD)).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        notes.move_to([3.4, 0.9, 0])
        rule = card("learning rate:\nthe size of each step", PURPLE, 32).next_to(notes, DOWN, 0.7)
        # "Gradient descent is the simplest search."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(curve), FadeIn(dots[0]), run_time=self.share(0.12))
        # "Find which way is downhill, take a step, and repeat until the ground is flat."
        cue(self, "Find which way")
        self.play(Create(slope), FadeIn(notes[0]), run_time=self.share(0.08))
        cue(self, "take a step")
        self.play(FadeOut(slope), ReplacementTransform(dots[0].copy(), dots[1]), FadeIn(notes[1]),
                  run_time=self.share(0.08))
        cue(self, "and repeat")
        self.play(*[ReplacementTransform(dots[i].copy(), dots[i + 1]) for i in (1, 2, 3)], FadeIn(notes[2]),
                  run_time=self.share(0.15), lag_ratio=0.5)
        # "The size of each step is called the learning rate."
        cue(self, "The size of each step")
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        # Page results: gradient-descent.qmd#fig-paths, the walks at 0.3 and 0.02.
        contours = self.data("contours")
        paths = self.data("paths")
        rates = self.data("rates").set_index("learning_rate")
        descent = self.data("descent").iloc[0]
        heading = title("The step size matters", 46).to_edge(UP, buff=0.35)
        axes, frame = chart([-0.3, 2.9, 0.5], [-1.8, 0.7, 0.5], 6.9, 5.4, [0, 1, 2], [-1.5, -1, -0.5, 0, 0.5],
                            "chlorophyll slope", "depth slope")
        frame.move_to([-2.6, -0.45, 0])
        lines = VGroup()
        for _, line in contours.groupby("line"):
            lines.add(VMobject(color=GRID, stroke_width=3).set_points_as_corners(
                [axes.c2p(x, y) for x, y in zip(line["x"], line["y"])]))
        best = cross(0.5, INK).move_to(axes.c2p(descent["optimum_chlorophyll"], descent["optimum_depth"]))
        start = label("start", 26, SUBDUED).next_to(axes.c2p(0, 0), UP, 0.2)
        bottom = label("the bottom", 26, INK).next_to(best, DOWN, 0.2)

        def walk(rate):
            rows = paths[(paths["learning_rate"] - rate).abs() < 1e-9].sort_values("step")
            points = [axes.c2p(x, y) for x, y in zip(rows["chlorophyll"], rows["depth"])]
            return (VMobject(color=RATE_COLOURS[rate], stroke_width=4).set_points_as_corners(points),
                    VGroup(*[Dot(p, radius=0.06, color=RATE_COLOURS[rate]) for p in points]))

        def row(rate, text):
            return VGroup(label(f"learning rate {rate:g}", 34, RATE_COLOURS[rate], weight=BOLD),
                          label(text, 32, RATE_COLOURS[rate])).arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        legend = VGroup(row(0.3, f"the bottom in {int(rates.loc[0.3, 'steps'])} steps"),
                        row(0.02, f"creeps: needs {int(rates.loc[0.02, 'steps'])}"))
        legend.arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([4.0, 0.3, 0])
        fast, slow = walk(0.3), walk(0.02)
        # "The step size matters."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), Create(lines), FadeIn(best), FadeIn(bottom),
                  FadeIn(start), run_time=self.share(0.15))
        # "At a learning rate of 0.3, this walk reaches the bottom in 11 steps."
        cue(self, "At a learning rate")
        self.play(Create(fast[0]), FadeIn(fast[1], lag_ratio=0.1), FadeIn(legend[0]), run_time=self.share(0.2))
        # "At 0.02, it creeps, and needs 197."
        cue(self, "At 0.02")
        self.play(Create(slow[0]), FadeIn(slow[1], lag_ratio=0.1), FadeIn(legend[1]), run_time=self.share(0.2))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        # Schematic: steps too large, each landing higher on the far side; only the rate is the page's.
        heading = title("Too large a step", 50).to_edge(UP, buff=0.6)
        axes = bowl_axes()
        curve = axes.plot(lambda x: x * x, x_range=[-4, 4, 0.05], color=GREY, stroke_width=6)
        xs = [-1.1, 1.4, -1.8, 2.4, -3.2]
        points = [axes.c2p(x, x * x) for x in xs]
        dots = [Dot(p, radius=0.13, color=VERMILION) for p in points]
        hops = [Arrow(points[i], points[i + 1], color=VERMILION, stroke_width=4, buff=0.15,
                      max_tip_length_to_length_ratio=0.08) for i in range(len(points) - 1)]
        notes = VGroup(label("each step overshoots", 34, VERMILION, weight=BOLD),
                       label("and lands higher", 34, VERMILION, weight=BOLD)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        notes.move_to([3.4, 1.2, 0])
        never = card(f"learning rate {DIVERGING_RATE:g}:\nnever arrives", VERMILION, 34).next_to(notes, DOWN, 0.6)
        warn = label("and nothing warns you", 34, INK, weight=BOLD).next_to(never, DOWN, 0.5)
        # "Too large, and each step overshoots the valley and lands higher on the other side."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(curve), FadeIn(dots[0]), run_time=self.share(0.1))
        for i, hop in enumerate(hops):
            self.play(Create(hop), FadeIn(dots[i + 1]), *([FadeIn(notes)] if i == 0 else []),
                      run_time=self.share(0.07))
        # "At 0.8, the walk climbs out and never arrives,"
        cue(self, "At 0.8")
        self.play(FadeIn(never, shift=0.2 * UP), run_time=self.share(0.08))
        # "and nothing on the way warns you."
        cue(self, "and nothing")
        self.play(FadeIn(warn), run_time=self.share(0.08))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        # Schematic: a model's printout, the coefficients as grey bars, never numbers.
        heading = title("Why a fit needs checking", 48).to_edge(UP, buff=0.5)
        box = RoundedRectangle(width=6.4, height=4.2, corner_radius=0.15, stroke_color=GRID, stroke_width=3,
                               fill_color="#f4f8fa", fill_opacity=1).move_to([-2.6, -0.7, 0])
        rows = VGroup(label("coefficients", 30, SUBDUED, weight=BOLD))
        for name, width in (("intercept", 1.4), ("chlorophyll", 1.1), ("depth", 1.6)):
            rows.add(VGroup(label(name, 30, INK), Rectangle(width=width, height=0.22, stroke_width=0,
                                                            fill_color=GREY, fill_opacity=0.6)
                            ).arrange(RIGHT, buff=0.5))
        for r in rows[1:]:
            r[1].move_to([0, r[1].get_y(), 0])
        flag = label("converged: FALSE", 32, VERMILION, weight=BOLD)
        rows.add(flag)
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(box)
        for r in rows[1:4]:
            r[1].set_x(box.get_right()[0] - 0.4 - r[1].width / 2)
        looks = label("looks normal", 30, GREEN, weight=BOLD).move_to([2.2, rows[2].get_y(), 0])
        brace = Brace(VGroup(*rows[1:4]), RIGHT, color=GREEN).next_to(box, RIGHT, 0.1).match_y(VGroup(*rows[1:4]))
        looks.next_to(brace, RIGHT, 0.2)
        ring = SurroundingRectangle(flag, color=VERMILION, buff=0.15, corner_radius=0.1)
        advice = card("look at the flag first", PURPLE, 36).move_to([3.8, -2.3, 0])
        # "That is why a fit needs checking."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "A search that went wrong still prints coefficients, and they look perfectly normal."
        cue(self, "A search that")
        self.play(FadeIn(box), FadeIn(VGroup(*rows[:4])), run_time=self.share(0.1))
        cue(self, "and they look")
        self.play(GrowFromCenter(brace), FadeIn(looks), run_time=self.share(0.08))
        # "The software records whether the search finished, in a convergence flag."
        cue(self, "The software records")
        self.play(FadeIn(flag), Create(ring), run_time=self.share(0.1))
        # "Look at it before you read anything else."
        cue(self, "Look at it")
        self.play(FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene14(KeyPointScene):
    number, point = 14, 2


# The assumptions inside the loss (scenes 15–20) ---------------------------------------------

def poisson_pmf(k, mean):
    return math.exp(-mean) * mean ** k / math.factorial(k)


def effect_bars(axes, values, names, colours, size=38):
    """Bars from zero on a vertical axis, each with its value and name; one VGroup per bar."""
    bars = VGroup()
    for x, value, name, colour in zip((1, 2), values, names, colours):
        base, top = axes.c2p(x, 0), axes.c2p(x, value)
        bar = Rectangle(width=1.2, height=max(abs(top[1] - base[1]), 0.02), stroke_width=0, fill_color=colour,
                        fill_opacity=1).move_to(base, aligned_edge=DOWN if value > 0 else UP)
        text = label(("+" if value > 0 else "") + fixed(value), size, colour, weight=BOLD
                     ).next_to(bar, UP if value > 0 else DOWN, 0.15)
        name_text = label(name, 28, colour, weight=BOLD).next_to(base, DOWN if value > 0 else UP, 0.2)
        bars.add(VGroup(bar, text, name_text))
    return bars


class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Schematic, after likelihood-and-priors.qmd's diagram: three distributions, three losses.
        heading = title("Where a loss comes from", 50).to_edge(UP, buff=0.5)
        specs = [("Normal", "a measurement", "squared error", BLUE),
                 ("Poisson", "a count", "Poisson deviance", ORANGE),
                 ("Bernoulli", "present or absent", "log loss", GREEN)]
        panels, losses, arrows = VGroup(), VGroup(), VGroup()
        for i, (name, kind, loss, colour) in enumerate(specs):
            box = RoundedRectangle(width=4.0, height=3.4, corner_radius=0.15, stroke_color="#1b6a87",
                                   stroke_width=3, fill_color="#f4f8fa", fill_opacity=1)
            strip = Rectangle(width=4.0, height=0.12, stroke_width=0, fill_color=colour, fill_opacity=1
                              ).align_to(box, UP)
            words = VGroup(label(name, 34, INK, weight=BOLD), label(kind, 26, SUBDUED)).arrange(DOWN, buff=0.08)
            words.next_to(strip, DOWN, 0.2)
            axes = plain_axes([0, 10, 1], [0, 1.1, 1], 3.2, 1.4).next_to(words, DOWN, 0.25)
            if i == 0:
                sketch = axes.plot(lambda x: bell(x, 5, 1.6), x_range=[0, 10, 0.05], color=colour, stroke_width=6)
            elif i == 1:
                peak = poisson_pmf(3, 3)
                sketch = VGroup(*[Rectangle(width=0.22, height=max(1.4 * poisson_pmf(k, 3) / peak / 1.1, 0.01),
                                            stroke_width=0, fill_color=colour, fill_opacity=1
                                            ).move_to(axes.c2p(0.5 + k, 0), aligned_edge=DOWN)
                                  for k in range(10)])
            else:
                sketch = VGroup(*[Rectangle(width=0.7, height=1.4 * h / 1.1, stroke_width=0, fill_color=colour,
                                            fill_opacity=1).move_to(axes.c2p(x, 0), aligned_edge=DOWN)
                                  for x, h in ((3, 0.35), (7, 0.65))])
                sketch.add(label("absent", 22, SUBDUED).next_to(axes.c2p(3, 0), DOWN, 0.08),
                           label("present", 22, SUBDUED).next_to(axes.c2p(7, 0), DOWN, 0.08))
            panel_ = VGroup(box, strip, words, axes, sketch).move_to([-4.6 + 4.6 * i, 0.9, 0])
            panels.add(panel_)
            arrow = Arrow(box.get_bottom(), box.get_bottom() + 0.8 * DOWN, buff=0.05, color=INK, stroke_width=5)
            arrows.add(arrow)
            losses.add(label(loss, 34, colour, weight=BOLD).next_to(arrow, DOWN, 0.15))
        rule = card("name the distribution, and the loss follows", PURPLE, 32).to_edge(DOWN, buff=0.4)
        # "Where does a loss come from?"
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "Squared error assumes each value is scattered around the prediction in a bell-shaped curve,
        # a Normal distribution."
        cue(self, "Squared error assumes")
        self.play(FadeIn(panels[0]), run_time=self.share(0.06))
        cue(self, "a Normal distribution")
        self.play(GrowArrow(arrows[0]), FadeIn(losses[0]), run_time=self.share(0.05))
        # "Assume a Poisson distribution, made for counts, and the loss becomes Poisson deviance."
        cue(self, "Assume a Poisson")
        self.play(FadeIn(panels[1]), run_time=self.share(0.06))
        cue(self, "and the loss becomes")
        self.play(GrowArrow(arrows[1]), FadeIn(losses[1]), run_time=self.share(0.05))
        # "For present or absent, it becomes log loss."
        cue(self, "For present")
        self.play(FadeIn(panels[2]), run_time=self.share(0.05))
        cue(self, "it becomes log")
        self.play(GrowArrow(arrows[2]), FadeIn(losses[2]), run_time=self.share(0.04))
        # "Name the distribution, and the loss follows."
        cue(self, "Name the distribution")
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=self.share(0.05))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        # Schematic: a Normal curve around a low prediction runs below zero; Poisson stops at zero.
        heading = title("A negative number of animals", 50).to_edge(UP, buff=0.5)
        left, left_frame = chart([-4, 6, 1], [0, 1.15, 0.5], 5.2, 3.4, [0], [], "animals", "")
        left_frame.move_to([-3.4, -0.6, 0])
        curve = left.plot(lambda x: bell(x, 1, 1.6), x_range=[-4, 6, 0.02], color=BLUE, stroke_width=6)
        below = left.get_area(curve, x_range=[-4, 0], color=VERMILION, opacity=0.45)
        zero = DashedLine(left.c2p(0, 0), left.c2p(0, 1.12), color=INK, stroke_width=3)
        left_name = VGroup(label("Normal: squared error", 30, BLUE, weight=BOLD),
                           label("below zero allowed", 28, VERMILION, weight=BOLD)).arrange(DOWN, buff=0.1)
        left_name.next_to(left_frame, UP, 0.25)
        right, right_frame = chart([-4, 6, 1], [0, 1.15, 0.5], 5.2, 3.4, [0], [], "animals", "")
        right_frame.move_to([3.4, -0.6, 0])
        peak = poisson_pmf(0, 1)
        bars = VGroup(*[Rectangle(width=0.36, height=max(3.4 / 1.15 * poisson_pmf(k, 1) / peak, 0.01),
                                  stroke_width=0, fill_color=ORANGE, fill_opacity=1
                                  ).move_to(right.c2p(k, 0), aligned_edge=DOWN) for k in range(6)])
        right_zero = DashedLine(right.c2p(0, 0), right.c2p(0, 1.12), color=INK, stroke_width=3).shift(0.2 * LEFT)
        right_name = VGroup(label("Poisson: Poisson deviance", 30, ORANGE, weight=BOLD),
                            label("never below zero", 28, GREEN, weight=BOLD)).arrange(DOWN, buff=0.1)
        right_name.next_to(right_frame, UP, 0.25)
        # "That explains a puzzle from earlier in the course: a polynomial regression predicted a negative
        # number of animals."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "A Normal curve runs below zero, so squared error saw nothing wrong."
        cue(self, "A Normal curve")
        self.play(FadeIn(left_frame), Create(zero), Create(curve), FadeIn(left_name[0]), run_time=self.share(0.1))
        cue(self, "runs below zero")
        self.play(FadeIn(below), FadeIn(left_name[1]), run_time=self.share(0.08))
        # "A Poisson distribution stops at zero, so Poisson regression never predicts fewer than zero animals."
        cue(self, "A Poisson distribution")
        self.play(FadeIn(right_frame), Create(right_zero), FadeIn(bars, lag_ratio=0.2), FadeIn(right_name[0]),
                  run_time=self.share(0.1))
        cue(self, "so Poisson regression")
        self.play(FadeIn(right_name[1]), run_time=self.share(0.08))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        # Page results: likelihood-and-priors.qmd, maximum likelihood on forty stations.
        forty = self.data("forty")
        heading = title(f"A small survey: {int(forty['stations'][0])} stations, {int(forty['inputs'][0])} inputs",
                        44).to_edge(UP, buff=0.4)
        axes = plain_axes([0, 3, 1], [-8, 10, 2], 6.0, 5.0).move_to([-2.6, -0.8, 0])
        zero = Line(axes.c2p(0, 0), axes.c2p(3, 0), color=INK, stroke_width=3)
        bars = effect_bars(axes, forty["ml"], ["temperature", "its square"], [BLUE, ORANGE])
        unit = label("animals per standard deviation of each input", 28, SUBDUED)
        unit.next_to(heading, DOWN, 0.2)
        cancel = label("two large effects\nthat cancel out", 34, INK, weight=BOLD).move_to([3.6, 0.8, 0])
        chasing = card("a warning sign:\nchasing chance patterns", VERMILION, 30).next_to(cancel, DOWN, 0.6)
        # "Now a small survey: forty stations and twelve inputs."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(zero), FadeIn(unit), run_time=self.share(0.1))
        # "The fit gives temperature an effect of 9.23 animals,"
        cue(self, "The fit gives")
        self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), run_time=self.share(0.08))
        # "and its square minus 6.78."
        cue(self, "and its square")
        self.play(GrowFromEdge(bars[1][0], UP), FadeIn(bars[1][1:]), run_time=self.share(0.08))
        # "Two large effects that cancel out are a warning sign:"
        cue(self, "Two large effects")
        self.play(FadeIn(cancel), run_time=self.share(0.08))
        # "with so few stations, the fit is chasing chance patterns."
        cue(self, "are a warning")
        self.play(FadeIn(chasing, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        # Page results: likelihood-and-priors.qmd, the same two effects with a Normal prior (ridge).
        forty = self.data("forty")
        heading = title("What you knew before can help", 46).to_edge(UP, buff=0.4)
        prior_heading = title("A prior: effects that large are rare", 46).to_edge(UP, buff=0.4)
        axes = plain_axes([0, 3, 1], [-8, 10, 2], 6.0, 5.0).move_to([2.6, -0.8, 0])
        zero = Line(axes.c2p(0, 0), axes.c2p(3, 0), color=INK, stroke_width=3)
        names = ["temperature", "its square"]
        before = effect_bars(axes, forty["ml"], names, [BLUE, ORANGE])
        after = effect_bars(axes, forty["map"], names, [BLUE, ORANGE])
        ghosts = VGroup(*[VGroup(b[0].copy().set_fill(opacity=0).set_stroke(GREY, 3),
                                 b[1].copy().set_color(GREY)) for b in before])
        unit = label("animals per standard deviation of each input", 28, SUBDUED).next_to(heading, DOWN, 0.2)
        pa, prior_frame = chart([-4, 4, 1], [0, 1.15, 0.5], 4.6, 2.6, [-3, 0, 3], [], "an effect", "")
        prior_frame.move_to([-4.0, -0.4, 0])
        prior = pa.plot(lambda b: bell(b, 0, 1), x_range=[-4, 4, 0.02], color=PURPLE, stroke_width=6)
        prior_name = label("the prior,\ncentred on zero", 28, PURPLE, weight=BOLD).next_to(prior_frame, UP, 0.2)
        # "With so few stations, what you knew before the survey can help."
        self.play(FadeIn(heading, shift=0.2 * DOWN), Create(zero), FadeIn(unit), FadeIn(before),
                  run_time=self.share(0.08))
        # "And you did know something: effects that large are rare."
        cue(self, "effects that large")
        self.play(Indicate(VGroup(before[0][1], before[1][1]), color=INK), run_time=self.share(0.06))
        # "A prior writes that down, as a curve centred on zero."
        cue(self, "A prior writes")
        self.play(ReplacementTransform(heading, prior_heading), FadeIn(prior_frame), Create(prior),
                  FadeIn(prior_name), run_time=self.share(0.1))
        # "Combined with the data, it pulls the temperature effect from 9.23 to 0.26,"
        cue(self, "it pulls")
        self.add(ghosts[0])
        self.play(ReplacementTransform(before[0][0], after[0][0]), FadeOut(before[0][1]), FadeIn(after[0][1]),
                  run_time=self.share(0.1))
        # "and its square from minus 6.78 to minus 0.18."
        cue(self, "and its square from")
        self.add(ghosts[1])
        self.play(ReplacementTransform(before[1][0], after[1][0]), FadeOut(before[1][1]), FadeIn(after[1][1]),
                  run_time=self.share(0.1))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        # Schematic: the prior as a penalty in the loss.
        heading = title("A prior is a penalty", 50).to_edge(UP, buff=0.6)
        parts = VGroup(label("score", 44, INK, weight=BOLD), label("=", 44, INK),
                       label("loss", 44, BLUE, weight=BOLD), label("+", 44, INK),
                       label("penalty", 44, ORANGE, weight=BOLD)).arrange(RIGHT, buff=0.9).move_to([0, 1.0, 0])
        under = VGroup(label("how well it fits", 28, BLUE).next_to(parts[2], DOWN, 0.3),
                       label("grows as the\nparameters grow", 28, ORANGE).next_to(parts[4], DOWN, 0.3))
        ridge = card("this is ridge regression", PURPLE, 38).move_to([0, -1.6, 0])
        later = label("the next section of the course uses it\nto stop models overfitting", 30, SUBDUED
                      ).to_edge(DOWN, buff=0.5)
        # "In the fit, a prior works as a penalty added to the loss,"
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.08))
        self.play(FadeIn(parts[:3]), FadeIn(under[0]), run_time=self.share(0.1))
        cue(self, "a penalty added")
        self.play(FadeIn(parts[3:]), run_time=self.share(0.08))
        # "one that grows as the parameters grow."
        cue(self, "one that grows")
        self.play(FadeIn(under[1]), run_time=self.share(0.08))
        # "This is ridge regression, and the next section of the course uses it to stop models overfitting."
        cue(self, "This is ridge")
        self.play(FadeIn(ridge, scale=0.9), run_time=self.share(0.08))
        cue(self, "and the next")
        self.play(FadeIn(later), run_time=self.share(0.08))
        self.finish()


class Scene20(KeyPointScene):
    number, point = 20, 3


# The quiz (scenes 21–22) ------------------------------------------------------------------

class Scene21(QuizScene):
    number = 21
    question = ("A colleague fits logistic regression,", "and every coefficient looks sensible.",
                "Can they trust them?")


class Scene22(VideoScene):
    number = 22

    def construct(self):
        # Page results: parameter-estimation.qmd, logistic regression stopped after two steps.
        fits = self.data("truncated")
        answer = title("Not yet", 56).to_edge(UP, buff=0.5)
        rows = [["logistic regression", "chlorophyll", "converged"]]
        for _, r in fits.iterrows():
            rows.append([r["fit"], fixed(r["chlorophyll"], 3), "TRUE" if r["converged"] else "FALSE"])
        grid = table(rows, [4.8, 3.0, 3.0], 36, row_gap=0.9).move_to([0, 0.5, 0])
        grid[1][2].set_color(VERMILION)
        flag = SurroundingRectangle(VGroup(grid[0][2], grid[1][2], grid[2][2]), color=PURPLE, buff=0.2,
                                    corner_radius=0.1, stroke_width=0, fill_color=PURPLE, fill_opacity=0.15)
        off = label(f"{percent(fits['off'].iloc[0], 0)} out, and it looks normal", 32, VERMILION, weight=BOLD
                    ).next_to(grid, DOWN, 0.6)
        advice = card("check the flag first", PURPLE, 36).to_edge(DOWN, buff=0.5)
        # "Not yet."
        self.play(FadeIn(answer, scale=0.9), run_time=self.share(0.06))
        # "On the survey, a fit stopped after two steps gave a chlorophyll coefficient 23 per cent out,"
        cue(self, "On the survey")
        self.play(FadeIn(grid[0]), FadeIn(VGroup(grid[1][:2], grid[2][:2])), run_time=self.share(0.1))
        cue(self, "23 per cent")
        self.play(FadeIn(off), run_time=self.share(0.08))
        # "and it looked entirely normal. Only the convergence flag showed the problem."
        cue(self, "Only the convergence")
        self.play(FadeIn(flag), FadeIn(grid[1][2]), FadeIn(grid[2][2]), run_time=self.share(0.1))
        # "Check it first."
        cue(self, "Check it first")
        self.play(FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


# The recap (scenes 23–25) and the end card (scene 26) --------------------------------------

class Scene23(RecapScene):
    number, point = 23, 1


class Scene24(RecapScene):
    number, point = 24, 2


class Scene25(RecapScene):
    number, point = 25, 3


class Scene26(EndCardScene):
    number = 26
