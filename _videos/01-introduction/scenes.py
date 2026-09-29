"""Manim scenes for the introduction video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/01-introduction
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


PROMISES = ["What machine learning is for",
            "Why the best predictor can be the worst explanation",
            "What your data let you ask"]
ANSWERS = ["Predicting cases it has\nnot seen, checked on\ndata held back",
           "Decide first: prediction\nor explanation; they pull\nin different directions",
           "Labelled or not\ncomes first; the\nmachine comes second"]
RECAP = ["Machine learning is built to predict",
         "The best predictor is not the best explanation",
         "Your data decide the question"]

# The simulation's thermal optimum, stated on the prediction-and-explanation page.
TRUE_OPTIMUM = 9


class Scene01(LearnScene):
    number = 1


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def polyline(axes, xs, ys, colour, width=6):
    return VMobject(color=colour, stroke_width=width).set_points_as_corners(
        [axes.c2p(x, y) for x, y in zip(xs, ys)])


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name, size=24):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
    axes = plain_axes(x_range, y_range, x_length, y_length)
    tx = VGroup(*[label(f"{v:g}", size, SUBDUED).next_to(axes.c2p(v, y_range[0]), DOWN, 0.15)
                  for v in x_ticks])
    ty = VGroup(*[label(f"{v:g}", size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15)
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


def cross(size=0.4, colour=VERMILION):
    return VGroup(Line(size * (UL), size * DR, color=colour, stroke_width=8),
                  Line(size * UR, size * DL, color=colour, stroke_width=8)).scale(0.5)


def at(scene, fraction):
    """Wait until this fraction of the narration."""
    scene.wait(max(scene.share(fraction) - scene.time, 0.01))


def whole_percent(value):
    """A proportion as the pages speak it: 0.785 is 79%, rounded half up as R's round() would not."""
    return f"{Decimal(str(100 * value)).quantize(Decimal('1'), ROUND_HALF_UP)}%"


def station_map(scene, width=6.2, height=4.6):
    """The surveyed stations by position. No axis values: the coordinates are simulated."""
    stations = scene.data("stations")
    axes = plain_axes([stations["longitude"].min() - 0.05, stations["longitude"].max() + 0.05, 1],
                      [stations["latitude"].min() - 0.05, stations["latitude"].max() + 0.05, 1],
                      width, height)
    frame = SurroundingRectangle(axes, color=GRID, buff=0.1, stroke_width=3)
    dots = VGroup(*[Dot(axes.c2p(lon, lat), 0.045, color=BLUE)
                    for lon, lat in zip(stations["longitude"], stations["latitude"])])
    axes.set_opacity(0)
    return VGroup(axes, frame, dots), len(stations)


# The puzzle (scenes 2–5, page results) --------------------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        chart_, n = station_map(self)
        chart_.move_to([0, -0.5, 0])
        count = label(f"{n} stations, simulated", 30, SUBDUED, weight=BOLD).next_to(chart_, DOWN, 0.25)
        question = card("how does temperature affect abundance?", PURPLE, 40).to_edge(UP, buff=0.35)
        # "Here is a survey of 800 coastal stations,"
        self.play(FadeIn(chart_[1]), LaggedStart(*[FadeIn(d) for d in chart_[2]], lag_ratio=0.002),
                  run_time=self.share(0.35))
        self.play(FadeIn(count), run_time=self.share(0.08))
        # "and one question: how does temperature affect the abundance of a seabed species?"
        at(self, 0.45)
        self.play(FadeIn(question, shift=0.2 * DOWN), run_time=self.share(0.15))
        self.finish()


COEFFICIENT_NAMES = {"depth_m": "depth (per m)", "temperature_c": "temperature (per °C)",
                     "chlorophyll_mg_m3": "chlorophyll", "salinity_psu": "salinity",
                     "substratemud": "mud (vs sand)", "substrategravel": "gravel (vs sand)",
                     "substraterock": "rock (vs sand)"}


def p_text(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def coefficient_layout(scene):
    """The linear model's table as the page prints it, rounded to three places."""
    table = scene.data("coefficients")
    table = table[table["term"] != "(Intercept)"].reset_index(drop=True)
    xs = [-3.2, 0.2, 3.1, 5.4]
    head = VGroup(*[label(t, 28, SUBDUED, weight=BOLD).move_to([x, 2.35, 0])
                    for t, x in zip(["", "estimate", "95% interval", "p"], xs)])
    rows = VGroup()
    for i, r in table.iterrows():
        y = 1.6 - 0.62 * i
        rows.add(VGroup(
            label(COEFFICIENT_NAMES[r["term"]], 32).move_to([xs[0] + 1.9, y, 0], aligned_edge=RIGHT),
            label(f"{r['estimate']:.3f}", 32).move_to([xs[1], y, 0]),
            label(f"{r['conf.low']:.3f} to {r['conf.high']:.3f}", 32).move_to([xs[2], y, 0]),
            label(p_text(r["p.value"]), 32).move_to([xs[3], y, 0])))
    rule = Line([-5.8, 2.0, 0], [6.3, 2.0, 0], stroke_width=3)
    heading = title("A linear model", 46).to_edge(UP, buff=0.4)
    terms = list(table["term"])
    return VGroup(heading, head, rule), rows, terms, table


def row_band(row, colour):
    return SurroundingRectangle(row, color=colour, buff=0.12, corner_radius=0.1, stroke_width=0,
                                fill_color=colour, fill_opacity=0.15).stretch_to_fit_width(12.4).set_x(0.25)


class Scene03(VideoScene):
    number = 3

    def construct(self):
        frame, rows, terms, table = coefficient_layout(self)
        chl, depth = rows[terms.index("chlorophyll_mg_m3")], rows[terms.index("depth_m")]
        # "Fit a linear model, as you normally would."
        self.play(FadeIn(frame), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.1), run_time=self.share(0.35))
        # "Chlorophyll has a clear positive association."
        at(self, 0.4)
        chl_band = row_band(chl, GREEN)
        self.play(FadeIn(chl_band), chl.animate.set_color(GREEN), run_time=self.share(0.15))
        # "Depth declines, weakly."
        at(self, 0.75)
        depth_band = row_band(depth, SKY)
        self.play(FadeIn(depth_band), run_time=self.share(0.12))
        self.finish()


def temperature_highlight(frame, rows, terms, table):
    row = rows[terms.index("temperature_c")]
    band = row_band(row, VERMILION)
    r = table[table["term"] == "temperature_c"].iloc[0]
    # A small interval, drawn to scale, under the table: it spans zero.
    axis = NumberLine(x_range=[-0.25, 0.1, 0.05], length=6, color=GRID, include_ticks=False, stroke_width=3)
    axis.move_to([-2.2, -3.0, 0])
    zero = DashedLine(axis.n2p(0) + 0.45 * UP, axis.n2p(0) + 0.45 * DOWN, color=INK, stroke_width=3)
    zero_name = label("0", 26, INK, weight=BOLD).next_to(zero, DOWN, 0.1)
    span = Line(axis.n2p(r["conf.low"]), axis.n2p(r["conf.high"]), color=VERMILION, stroke_width=10)
    dot = Dot(axis.n2p(r["estimate"]), 0.13, color=VERMILION)
    verdict = card("no temperature effect", VERMILION, 34).next_to(axis, RIGHT, 0.4).shift(0.05 * UP)
    return row, band, VGroup(axis, zero, zero_name), VGroup(span, dot), verdict


class Scene04(VideoScene):
    number = 4

    def construct(self):
        frame, rows, terms, table = coefficient_layout(self)
        self.add(frame, rows)
        row, band, scale, interval, verdict = temperature_highlight(frame, rows, terms, table)
        # "And temperature? About minus 0.07 per degree, with a p value of 0.31."
        self.play(FadeIn(band), row.animate.set_color(VERMILION), run_time=self.share(0.15))
        at(self, 0.25)
        self.play(FadeIn(scale), GrowFromCenter(interval[0]), FadeIn(interval[1]), run_time=self.share(0.25))
        # "You would report no temperature effect."
        at(self, 0.72)
        self.play(FadeIn(verdict, scale=0.9), run_time=self.share(0.15))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        frame, rows, terms, table = coefficient_layout(self)
        row, band, scale, interval, verdict = temperature_highlight(frame, rows, terms, table)
        row.set_color(VERMILION)
        self.add(frame, rows, band, scale, interval, verdict)
        truth = card(f"written to peak at {TRUE_OPTIMUM} °C", GREEN, 44).move_to([0, 0.3, 0])
        what = label("so what went wrong?", 44, PURPLE, weight=BOLD).next_to(truth, DOWN, 0.4)
        shade = Rectangle(width=15, height=9, stroke_width=0, fill_color=BACKGROUND, fill_opacity=0.92)
        # "But this survey is simulated, and we wrote the species to peak at 9 degrees."
        self.play(FadeIn(shade), FadeIn(truth, scale=0.9), run_time=self.share(0.25))
        # "So what went wrong?"
        at(self, 0.7)
        self.play(FadeIn(what, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


# Two ways to fit the same data (scenes 6–16) ------------------------------------------------

class Scene06(VideoScene):
    number = 6

    def construct(self):
        split = self.data("split").iloc[0]
        total = int(split["train"] + split["test"])
        columns = 40
        rows = total // columns
        cells = VGroup(*[Square(0.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.85)
                         for _ in range(total)]).arrange_in_grid(rows, columns, buff=0.07, flow_order="dr")
        cells.move_to([0, -0.2, 0])
        held = cells[int(split["train"]):]          # the last columns: 200 of 800
        train_name = label(f"{int(split['train'])} to train on", 36, BLUE, weight=BOLD)
        train_name.next_to(cells[:int(split["train"])], UP, 0.35)
        held_name = label(f"{int(split['test'])} held back", 36, SUBDUED, weight=BOLD).next_to(held, UP, 0.35)
        lock = SurroundingRectangle(held, color=SUBDUED, buff=0.12, corner_radius=0.1, stroke_width=4)
        until = label("not looked at until the end", 30, SUBDUED).next_to(lock, DOWN, 0.3)
        # "Start by splitting the data: 600 stations to train on,"
        self.play(FadeIn(cells), run_time=self.share(0.15))
        self.play(FadeIn(train_name), run_time=self.share(0.12))
        # "and 200 held back, not looked at until the end."
        at(self, 0.45)
        self.play(held.animate.set_fill(GREY, 0.45).shift(0.35 * RIGHT), run_time=self.share(0.15))
        lock.move_to(held)
        self.play(FadeIn(held_name), Create(lock), run_time=self.share(0.12))
        self.play(FadeIn(until), run_time=self.share(0.1))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        # Schematic: made-up points, a line through them, and a coefficient with no value.
        rng = np.random.default_rng(7)
        axes = plain_axes([0, 10, 1], [0, 10, 1], 5.5, 4.2).move_to([-3.4, -0.5, 0])
        xs = rng.uniform(0.5, 9.5, 30)
        dots = VGroup(*[Dot(axes.c2p(x, 1.5 + 0.7 * x + rng.normal(0, 1.1)), 0.07, color=GREY) for x in xs])
        line = Line(axes.c2p(0, 1.5), axes.c2p(10, 8.5), color=VERMILION, stroke_width=7)
        head = title("A statistical model", 50).to_edge(UP, buff=0.5)
        chose = label("you choose the form", 34, VERMILION, weight=BOLD).next_to(axes, UP, 0.25)
        slope = VGroup(label("a number", 40, INK, weight=BOLD), label("with an interval", 40, INK, weight=BOLD))
        slope.arrange(DOWN, buff=0.15).move_to([3.3, 0.8, 0])
        bar = VGroup(Line([1.9, -0.6, 0], [4.7, -0.6, 0], color=BLUE, stroke_width=10),
                     Dot([3.3, -0.6, 0], 0.16, color=BLUE))
        statement = card("a statement for a paper", GREEN, 34).move_to([3.3, -2.0, 0])
        # "A statistical model estimates something about the world."
        self.play(FadeIn(head), FadeIn(axes), FadeIn(dots), run_time=self.share(0.2))
        # "You choose the form,"
        at(self, 0.3)
        self.play(Create(line), FadeIn(chose), run_time=self.share(0.15))
        # "and it returns a number with an interval:"
        at(self, 0.5)
        self.play(FadeIn(slope), GrowFromCenter(bar[0]), FadeIn(bar[1]), run_time=self.share(0.15))
        # "a statement you can put in a paper."
        at(self, 0.75)
        self.play(FadeIn(statement, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        # Schematic: measurements in, a prediction out, and no number either side.
        head = title("A machine-learning model", 50).to_edge(UP, buff=0.5)
        inputs = VGroup(*[card(t, SKY, 28) for t in ["depth", "temperature", "chlorophyll", "salinity", "substrate"]]
                        ).arrange(DOWN, buff=0.2).move_to([-4.6, -0.5, 0])
        box = RoundedRectangle(width=3.2, height=2.4, corner_radius=0.25, stroke_color=INK, stroke_width=5,
                               fill_color=GRID, fill_opacity=0.5).move_to([0, -0.5, 0])
        shape = VMobject(color=BLUE, stroke_width=6).set_points_smoothly(
            [box.get_center() + p for p in [[-1.1, -0.6, 0], [-0.5, 0.5, 0], [0.1, -0.2, 0], [0.6, 0.6, 0], [1.1, -0.4, 0]]])
        searches = label("searches for the shape", 30, BLUE, weight=BOLD).next_to(box, DOWN, 0.3)
        output = card("a prediction", GREEN, 36).move_to([4.6, -0.5, 0])
        arrow_in = Arrow(inputs.get_right(), box.get_left(), color=INK, stroke_width=5, buff=0.2)
        arrow_out = Arrow(box.get_right(), output.get_left(), color=INK, stroke_width=5, buff=0.2)
        machine = label("a machine", 40, INK, weight=BOLD).next_to(box, UP, 0.3)
        unseen = label("for a station it has not seen", 28, SUBDUED).next_to(inputs, UP, 0.25)
        # "A machine-learning model is built to predict cases it has not seen."
        self.play(FadeIn(head), FadeIn(inputs), FadeIn(unseen), run_time=self.share(0.2))
        self.play(FadeIn(box), GrowArrow(arrow_in), GrowArrow(arrow_out), FadeIn(output), run_time=self.share(0.2))
        # "It searches for whatever shape fits, and returns a machine."
        at(self, 0.5)
        self.play(Create(shape), FadeIn(searches), run_time=self.share(0.2))
        at(self, 0.8)
        self.play(FadeIn(machine, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.finish()


def tree_icon(size=0.5, colour=GREEN):
    crown = Triangle(color=colour, fill_color=colour, fill_opacity=0.85, stroke_width=0).scale(size / 2)
    trunk = Rectangle(width=size * 0.14, height=size * 0.3, stroke_width=0, fill_color=SUBDUED,
                      fill_opacity=1).next_to(crown, DOWN, 0)
    return VGroup(crown, trunk)


class Scene09(VideoScene):
    number = 9

    def construct(self):
        # Schematic: a field of trees standing for the forest (the page grows 500).
        head = title("A random forest of 500 trees", 50).to_edge(UP, buff=0.5)
        trees = VGroup(*[tree_icon(0.5) for _ in range(60)]).arrange_in_grid(5, 12, buff=0.3).move_to([0, 0.1, 0])
        none = card("no coefficients to print", VERMILION, 38).to_edge(DOWN, buff=0.6)
        # "Here, a random forest of 500 trees."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(t, scale=0.5) for t in trees], lag_ratio=0.02),
                  run_time=self.share(0.4))
        # "There are no coefficients to print, only predictions."
        at(self, 0.5)
        self.play(FadeIn(none, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def hump_layout(scene):
    points = scene.data("train-points")
    lines = scene.data("temperature-lines")
    top = 20   # the few counts above 20 are left off, as noted on screen
    axes, frame = chart([1, 17, 1], [0, top, 5], 9.2, 5.2, [2, 5, 8, 11, 14], [0, 5, 10, 15, 20],
                        "temperature (°C)", "abundance")
    frame.move_to([-0.9, -0.4, 0])
    shown = points[points["abundance"] <= top]
    dots = VGroup(*[Dot(axes.c2p(t, a), 0.045, color=GREY, fill_opacity=0.45)
                    for t, a in zip(shown["temperature_c"], shown["abundance"])])
    hidden = label(f"{len(points) - len(shown)} stations above {top} not shown", 22, SUBDUED)
    hidden.next_to(axes.c2p(17, top), DOWN + LEFT, 0.05).shift(0.1 * DOWN)
    straight = polyline(axes, lines["temperature_c"], lines["straight"], VERMILION, 8)
    smooth = polyline(axes, lines["temperature_c"], lines["smooth"], BLUE, 8)
    tags = {"straight": label("what the linear model sees", 30, VERMILION, weight=BOLD),
            "smooth": label("what is actually there", 30, BLUE, weight=BOLD)}
    tags["straight"].next_to(axes.c2p(16, lines["straight"].iloc[-1]), UP, 0.15).shift(1.0 * LEFT + 0.15 * UP)
    peak = lines.loc[lines["smooth"].idxmax()]
    tags["smooth"].next_to(axes.c2p(peak["temperature_c"], peak["smooth"]), UP, 1.1)
    title_ = label(f"{len(points)} training stations", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.35)
    return frame, dots, hidden, straight, smooth, tags, title_


class Scene10(VideoScene):
    number = 10

    def construct(self):
        frame, dots, hidden, straight, smooth, tags, title_ = hump_layout(self)
        # "So look at the data. Abundance rises to a peak around 9 degrees, then falls away."
        self.play(FadeIn(frame), FadeIn(title_), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003), FadeIn(hidden), run_time=self.share(0.5))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        frame, dots, hidden, straight, smooth, tags, title_ = hump_layout(self)
        self.add(frame, dots, hidden, title_)
        wrong = card("not wrong about its line: its line is wrong", VERMILION, 32).to_edge(UP, buff=0.3)
        # "The linear model had to answer with a single slope."
        self.play(Create(straight), FadeIn(tags["straight"]), run_time=self.share(0.35))
        # "The best straight line through a hump is flat."
        at(self, 0.6)
        self.play(FadeOut(title_), FadeIn(wrong, shift=0.2 * DOWN), run_time=self.share(0.15))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        frame, dots, hidden, straight, smooth, tags, title_ = hump_layout(self)
        wrong = card("not wrong about its line: its line is wrong", VERMILION, 32).to_edge(UP, buff=0.3)
        self.add(frame, dots, hidden, straight, tags["straight"], wrong)
        # "The forest was never asked for a slope, so the hump costs it nothing."
        self.play(Create(smooth), FadeIn(tags["smooth"]), run_time=self.share(0.55))
        self.finish()


def errors_layout(scene):
    errors = scene.data("errors")
    axes, frame = chart([0, 5, 1], [0, 5, 1], 7.4, 4.6, [], [0, 1, 2, 3, 4, 5], "", "typical error (RMSE)")
    frame.move_to([-0.6, -0.4, 0])
    colours = {"linear": VERMILION, "forest": BLUE}
    groups = {}
    for g, (setname, centre) in enumerate([("training", 1.25), ("test", 3.75)]):
        bars = VGroup()
        for k, model in enumerate(["linear", "forest"]):
            value = errors[(errors["set"] == setname) & (errors["model"] == model)]["rmse"].item()
            x = centre + (k - 0.5) * 1.05
            bottom, top = axes.c2p(x, 0), axes.c2p(x, value)
            bar = Rectangle(width=1.0, height=top[1] - bottom[1], stroke_width=0, fill_color=colours[model],
                            fill_opacity=1).move_to(bottom, aligned_edge=DOWN)
            text = label(f"{value:.2f}", 32, INK, weight=BOLD).next_to(bar, UP, 0.12)
            bars.add(VGroup(bar, text))
        name = label({"training": "the 600 it trained on", "test": "the 200 held back"}[setname], 28, SUBDUED,
                     weight=BOLD).next_to(axes.c2p(centre, 0), DOWN, 0.25)
        groups[setname] = VGroup(bars, name)
    key = VGroup(*[VGroup(Square(0.3, stroke_width=0, fill_color=c, fill_opacity=1),
                          label(n, 30, c, weight=BOLD)).arrange(RIGHT, buff=0.2)
                   for n, c in [("linear model", VERMILION), ("random forest", BLUE)]]
                 ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([5.0, -0.3, 0])
    return frame, groups, key


class Scene13(VideoScene):
    number = 13

    def construct(self):
        frame, groups, key = errors_layout(self)
        bars = groups["training"][0]
        # "So does it predict better? On the training stations,"
        self.play(FadeIn(frame), FadeIn(key), FadeIn(groups["training"][1]), run_time=self.share(0.25))
        # "the forest's typical error is 2.09."
        at(self, 0.4)
        self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), run_time=self.share(0.2))
        # "The linear model's is 4.35."
        at(self, 0.72)
        self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), run_time=self.share(0.2))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        frame, groups, key = errors_layout(self)
        self.add(frame, key, groups["training"])
        bars = groups["test"][0]
        # "On the 200 held-back stations, the gap almost vanishes: 4.13 against 4.22."
        self.play(FadeIn(groups["test"][1]), run_time=self.share(0.15))
        at(self, 0.4)
        self.play(*[GrowFromEdge(b[0], DOWN) for b in bars], run_time=self.share(0.25))
        self.play(FadeIn(bars[1][1]), FadeIn(bars[0][1]), run_time=self.share(0.15))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        frame, groups, key = errors_layout(self)
        self.add(frame, key, groups["training"], groups["test"])
        forest_train = groups["training"][0][1][0]
        memory = label("memorised", 32, BLUE, weight=BOLD).next_to(groups["training"][0], UP, 0.3)
        arrow = Arrow(memory.get_bottom(), forest_train.get_top() + 0.5 * UP, color=BLUE, stroke_width=5, buff=0.1)
        honest = card("the honesty check", GREEN, 32).next_to(groups["test"][0], UP, 0.35)
        # "Most of the forest's advantage was memory of the stations it trained on."
        self.play(FadeIn(memory), GrowArrow(arrow), run_time=self.share(0.2))
        # "That is overfitting, and only the held-back data caught it."
        at(self, 0.6)
        self.play(FadeIn(honest, shift=0.2 * DOWN), Indicate(groups["test"][1], color=GREEN), run_time=self.share(0.2))
        self.finish()


class Scene16(KeyPointScene):
    number, point = 16, 1


# The puzzle, solved (scenes 17–27) ---------------------------------------------------------

class Scene17(VideoScene):
    number = 17

    def construct(self):
        head = title("Two goals", 52).to_edge(UP, buff=0.7)
        predict = VGroup(label("Prediction", 46, BLUE, weight=BOLD),
                         label("what will the value be?", 36)).arrange(DOWN, buff=0.3)
        explain = VGroup(label("Explanation", 46, ORANGE, weight=BOLD),
                         label("how does a driver affect it,", 36),
                         label("and by how much?", 36)).arrange(DOWN, buff=0.3)
        VGroup(predict, explain).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to([0, -0.3, 0])
        # "That comparison hides a choice."
        self.play(FadeIn(head), run_time=self.share(0.12))
        # "Prediction asks what the value will be."
        at(self, 0.25)
        self.play(FadeIn(predict, shift=0.2 * UP), run_time=self.share(0.15))
        # "Explanation asks how a driver affects it, and by how much."
        at(self, 0.55)
        self.play(FadeIn(explain, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


FOUR = [("Linear model", "linear model", VERMILION),
        ("Random forest", "random forest", BLUE),
        ("Linear model, with curves", "linear model, with curves", GREEN),
        ("Random forest + coordinates", "forest + coordinates", ORANGE)]


def four_layout(scene):
    """Test error per model on a narrow axis: the differences are small, and so is the axis."""
    scores = scene.data("four-models").set_index("model")["rmse"]
    axis = NumberLine(x_range=[3.9, 4.3, 0.1], length=7.2, color=GRID, include_ticks=True, tick_size=0.08,
                      stroke_width=3).move_to([2.6, -2.6, 0])
    ticks = VGroup(*[label(f"{v:.1f}", 24, SUBDUED).next_to(axis.n2p(v), DOWN, 0.2) for v in [3.9, 4.0, 4.1, 4.2, 4.3]])
    name = label("test error, on the 200 held back (lower is better)", 26, SUBDUED).next_to(ticks, DOWN, 0.2)
    rows = {}
    for i, (key, text, colour) in enumerate(FOUR):
        y = 1.6 - 1.0 * i
        guide = DashedLine(axis.n2p(3.9) + (y + 2.6) * UP, axis.n2p(4.3) + (y + 2.6) * UP, color=GRID,
                           stroke_width=2)
        dot = Dot(axis.n2p(scores[key]) + (y + 2.6) * UP, 0.17, color=colour)
        rows[key] = VGroup(label(text, 32, colour, weight=BOLD).move_to([-1.3, y, 0], aligned_edge=RIGHT),
                           guide, dot, label(f"{scores[key]:.2f}", 30, INK, weight=BOLD).next_to(dot, UP, 0.12))
    head = title("Four models, the same data", 46).to_edge(UP, buff=0.4)
    return VGroup(head, axis, ticks, name), rows, scores


class Scene18(VideoScene):
    number = 18

    def construct(self):
        frame, rows, scores = four_layout(self)
        # "So fit four models on the same data, and score each on the held-back stations."
        self.play(FadeIn(frame), run_time=self.share(0.25))
        self.play(FadeIn(rows["Linear model"]), run_time=self.share(0.2))
        self.play(FadeIn(rows["Random forest"]), run_time=self.share(0.2))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        frame, rows, scores = four_layout(self)
        self.add(frame, rows["Linear model"], rows["Random forest"])
        bend = card("species have optima: let it bend", GREEN, 32).move_to([0.6, -1.4, 0])
        # "A linear model allowed to curve scores 4.01, better than the forest."
        self.play(FadeIn(rows["Linear model, with curves"]), run_time=self.share(0.3))
        # "It took one piece of ecology: species have optima, so let the line bend."
        at(self, 0.5)
        self.play(FadeIn(bend, shift=0.2 * DOWN), run_time=self.share(0.15))
        self.finish()


def optimum_layout(scene):
    curve = scene.data("optimum")
    fitted = curve["optimum"].iloc[0]
    axes, frame = chart([3, 16, 1], [-4, 4.5, 1], 9.6, 5.0, [3, 6, 9, 12, 15], [-4, -2, 0, 2, 4],
                        "temperature (°C)", "predicted abundance")
    frame.move_to([-0.6, -0.5, 0])
    line = polyline(axes, curve["temperature_c"], curve["predicted"], BLUE, 8)
    truth = Line(axes.c2p(TRUE_OPTIMUM, -4), axes.c2p(TRUE_OPTIMUM, 4.5), color=GREY, stroke_width=4)
    fit = DashedLine(axes.c2p(fitted, -4), axes.c2p(fitted, 4.5), color=VERMILION, stroke_width=4)
    truth_name = label(f"true, {TRUE_OPTIMUM} °C", 30, SUBDUED, weight=BOLD).next_to(axes.c2p(TRUE_OPTIMUM, -3.4), RIGHT, 0.15)
    fit_name = label(f"fitted, {fitted:.1f} °C", 30, VERMILION, weight=BOLD).next_to(axes.c2p(fitted, 4.2), LEFT, 0.15)
    zero = DashedLine(axes.c2p(3, 0), axes.c2p(16, 0), color=INK, stroke_width=2)
    below = curve["predicted"] < 0
    low = curve[below & (curve["temperature_c"] < fitted)]
    high = curve[below & (curve["temperature_c"] > fitted)]
    negatives = VGroup(*[polyline(axes, part["temperature_c"], part["predicted"], VERMILION, 11)
                         for part in (low, high) if len(part) > 1])
    shade = Polygon(axes.c2p(3, 0), axes.c2p(16, 0), axes.c2p(16, -4), axes.c2p(3, -4), stroke_width=0,
                    fill_color=VERMILION, fill_opacity=0.08)
    return frame, line, VGroup(truth, truth_name), VGroup(fit, fit_name), VGroup(shade, zero), negatives


class Scene20(VideoScene):
    number = 20

    def construct(self):
        frame, line, truth, fit, below, negatives = optimum_layout(self)
        head = label("the curved model's temperature response", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.35)
        # "Its temperature curve peaks at 8.6 degrees."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.12))
        self.play(Create(line), run_time=self.share(0.3))
        self.play(Create(fit[0]), FadeIn(fit[1]), run_time=self.share(0.12))
        # "The truth is 9."
        at(self, 0.72)
        self.play(Create(truth[0]), FadeIn(truth[1]), run_time=self.share(0.15))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        frame, line, truth, fit, below, negatives = optimum_layout(self)
        self.add(frame, line, truth, fit)
        shade = Rectangle(width=15, height=9, stroke_width=0, fill_color=BACKGROUND, fill_opacity=0.8)
        old = label("no temperature effect", 44, SUBDUED, weight=BOLD).move_to([0, 1.0, 0])
        line_ = strike(old)
        new = VGroup(label("an effect the model", 44, GREEN, weight=BOLD),
                     label("could not draw", 44, GREEN, weight=BOLD)).arrange(DOWN, buff=0.15).move_to([0.4, -0.8, 0])
        box, mark = tick(0.7)
        box.next_to(new, LEFT, 0.45)
        mark.move_to(box)
        # "So 'no temperature effect' was never a fact about the species."
        self.play(FadeIn(shade), FadeIn(old), run_time=self.share(0.2))
        self.play(Create(line_), run_time=self.share(0.12))
        # "It was a fact about a model that could only draw straight lines."
        at(self, 0.5)
        self.play(FadeIn(new, shift=0.2 * UP), FadeIn(box), run_time=self.share(0.15))
        self.play(Create(mark), run_time=self.share(0.08))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        frame, line, truth, fit, below, negatives = optimum_layout(self)
        self.add(frame, line, truth, fit)
        name = VGroup(label("fewer than", 32, VERMILION, weight=BOLD), label("no animals", 32, VERMILION, weight=BOLD)
                     ).arrange(DOWN, buff=0.1).move_to([-3.4, -1.6, 0])
        verdict = card("sound in the centre, nonsense at the edges", PURPLE, 32).to_edge(UP, buff=0.3)
        # "Even so, look at its ends. Below zero: fewer than no animals."
        self.play(FadeIn(below), run_time=self.share(0.15))
        at(self, 0.25)
        self.play(Create(negatives), FadeIn(name), run_time=self.share(0.2))
        # "Sound in the centre, nonsense at the edges."
        at(self, 0.65)
        self.play(FadeIn(verdict, shift=0.2 * DOWN), run_time=self.share(0.15))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        frame, rows, scores = four_layout(self)
        self.add(frame, *[rows[k] for k, _, _ in FOUR[:3]])
        # "And the best predictor? The forest, with longitude and latitude added: 3.98."
        at(self, 0.3)
        self.play(FadeIn(rows["Random forest + coordinates"]), run_time=self.share(0.3))
        self.play(Indicate(rows["Random forest + coordinates"][2], color=ORANGE, scale_factor=1.6),
                  run_time=self.share(0.2))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        # The survey's stations by position: the two columns the best predictor added.
        chart_, n = station_map(self, 5.6, 4.2)
        chart_.move_to([-3.3, -0.6, 0])
        box = chart_[1]
        lon = Arrow(box.get_corner(DL) + 0.3 * DOWN, box.get_corner(DR) + 0.3 * DOWN, color=INK, stroke_width=5, buff=0)
        lat = Arrow(box.get_corner(DL) + 0.3 * LEFT, box.get_corner(UL) + 0.3 * LEFT, color=INK, stroke_width=5, buff=0)
        lon_name = label("longitude", 28, INK, weight=BOLD).next_to(lon, DOWN, 0.12)
        lat_name = label("latitude", 28, INK, weight=BOLD).rotate(PI / 2).next_to(lat, LEFT, 0.12)
        head = card("no fish responds to longitude", VERMILION, 36).to_edge(UP, buff=0.4)
        proxy = VGroup(label("a proxy for", 34, SUBDUED),
                       label("where the good patches", 34, ORANGE, weight=BOLD),
                       label("were during this survey", 34, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.18)
        proxy.move_to([3.6, -0.3, 0])
        # "No fish responds to longitude."
        self.play(FadeIn(head, shift=0.2 * DOWN), FadeIn(chart_[1:]), run_time=self.share(0.2))
        self.play(GrowArrow(lon), GrowArrow(lat), FadeIn(lon_name), FadeIn(lat_name), run_time=self.share(0.12))
        # "The coordinates are a proxy: the model learned where the good patches were during this survey."
        at(self, 0.4)
        self.play(LaggedStart(*[FadeIn(p) for p in proxy], lag_ratio=0.4), run_time=self.share(0.35))
        self.finish()


class Scene25(VideoScene):
    number = 25

    def construct(self):
        # The page's table of the four models: how well each predicts, and whether it explains.
        scores = self.data("four-models").set_index("model")["rmse"]
        explains = {"Linear model": False, "Random forest": False,
                    "Linear model, with curves": True, "Random forest + coordinates": False}
        notes = {"Linear model": "reports no temperature effect", "Random forest": "no coefficients to read",
                 "Linear model, with curves": "recovers the optimum", "Random forest + coordinates": "position is a proxy"}
        order = sorted(scores.index, key=lambda k: scores[k])
        xs = [-3.1, -0.5, 3.2]
        head = VGroup(*[label(t, 30, SUBDUED, weight=BOLD).move_to([x, 2.1, 0])
                        for t, x in zip(["", "test error", "explains?"], xs)])
        rows = VGroup()
        for i, key in enumerate(order):
            text, colour = next((t, c) for k, t, c in FOUR if k == key)
            y = 1.2 - 1.0 * i
            mark = tick(0.5) if explains[key] else (cross(0.9),)
            mark = VGroup(*mark).move_to([xs[2] - 1.5, y, 0])
            rows.add(VGroup(label(text, 32, colour, weight=BOLD).move_to([xs[0] + 1.3, y, 0], aligned_edge=RIGHT),
                            label(f"{scores[key]:.2f}", 32, INK, weight=BOLD).move_to([xs[1], y, 0]),
                            mark, label(notes[key], 24, SUBDUED).next_to(mark, RIGHT, 0.3)))
        best = SurroundingRectangle(rows[0], color=ORANGE, buff=0.15, corner_radius=0.1, stroke_width=4)
        good = SurroundingRectangle(rows[1], color=GREEN, buff=0.15, corner_radius=0.1, stroke_width=4)
        # "The best predictor explains nothing."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=self.share(0.3))
        self.play(Create(best), run_time=self.share(0.12))
        # "The best explanation is nearly the best predictor."
        at(self, 0.55)
        self.play(Create(good), run_time=self.share(0.12))
        self.finish()


class Scene26(VideoScene):
    number = 26

    def construct(self):
        # Schematic: a held-back set checks a prediction; nothing checks an effect size.
        predict = VGroup(label("Prediction", 42, BLUE, weight=BOLD), Arrow(LEFT, RIGHT, color=INK, stroke_width=5),
                         card("held-back data", SUBDUED, 32)).arrange(RIGHT, buff=0.4)
        box, mark = tick(0.6)
        predict.add(VGroup(box, mark).next_to(predict, RIGHT, 0.4))
        explain = VGroup(label("Explanation", 42, ORANGE, weight=BOLD), Arrow(LEFT, RIGHT, color=INK, stroke_width=5),
                         card("no data hold the true effect", SUBDUED, 32)).arrange(RIGHT, buff=0.4)
        explain.add(label("?", 60, VERMILION, weight=BOLD).next_to(explain, RIGHT, 0.4))
        VGroup(predict, explain).arrange(DOWN, buff=1.0, aligned_edge=LEFT).move_to([0, 0.4, 0])
        note = label("a good test score is not evidence the effects are real", 32, PURPLE, weight=BOLD)
        note.to_edge(DOWN, buff=0.8)
        # "And only prediction can be checked by holding data back."
        self.play(FadeIn(predict[:3]), run_time=self.share(0.2))
        self.play(FadeIn(box), Create(mark), run_time=self.share(0.1))
        self.play(FadeIn(explain), run_time=self.share(0.15))
        # "A good test score is not evidence that the effects are real."
        at(self, 0.55)
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene27(KeyPointScene):
    number, point = 27, 2


# What your data let you ask (scenes 28–41) ------------------------------------------------

def data_table(rng, answer=True, n_rows=7, n_cols=4, size=0.4):
    columns = VGroup()
    for j in range(n_cols + (1 if answer else 0)):
        colour = ORANGE if (answer and j == n_cols) else BLUE
        columns.add(VGroup(*[Square(size, stroke_width=0, fill_color=colour, fill_opacity=float(rng.uniform(0.2, 0.9)))
                             for _ in range(n_rows)]).arrange(DOWN, buff=0.05))
    columns.arrange(RIGHT, buff=0.05)
    if answer:
        columns[-1].shift(0.2 * RIGHT)
    return columns


class Scene28(VideoScene):
    number = 28

    def construct(self):
        # Schematic: two tables, one with an answer column and one without.
        rng = np.random.default_rng(28)
        head = title("Your data decide", 52).to_edge(UP, buff=0.6)
        with_answer = data_table(rng, True).move_to([-3.4, -0.2, 0])
        without = data_table(rng, False).move_to([3.4, -0.2, 0])
        answer_name = label("known answer", 28, ORANGE, weight=BOLD).next_to(with_answer[-1], UP, 0.25)
        sup = label("supervised", 44, ORANGE, weight=BOLD).next_to(with_answer, DOWN, 0.5)
        uns = label("unsupervised", 44, BLUE, weight=BOLD).next_to(without, DOWN, 0.5)
        # "The next question is forced by your data."
        self.play(FadeIn(head), run_time=self.share(0.15))
        # "If each row has a known answer, the learning is supervised."
        at(self, 0.3)
        self.play(FadeIn(with_answer), FadeIn(answer_name), run_time=self.share(0.15))
        self.play(FadeIn(sup, shift=0.2 * UP), run_time=self.share(0.1))
        # "If not, it is unsupervised."
        at(self, 0.75)
        self.play(FadeIn(without), FadeIn(uns, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene29(VideoScene):
    number = 29

    def construct(self):
        # Schematic: the answer column is a number, or a category.
        rng = np.random.default_rng(29)
        table = data_table(rng, True).move_to([-4.2, -0.2, 0])
        head = label("supervised", 44, ORANGE, weight=BOLD).next_to(table, UP, 0.5)
        quantity = VGroup(label("a quantity", 38, INK, weight=BOLD), label("abundance", 30, SUBDUED)).arrange(DOWN, buff=0.12)
        category = VGroup(label("a category", 38, INK, weight=BOLD), label("present or absent", 30, SUBDUED)).arrange(DOWN, buff=0.12)
        quantity.move_to([0.6, 1.2, 0])
        category.move_to([0.6, -1.6, 0])
        reg = label("regression", 44, BLUE, weight=BOLD).next_to(quantity, RIGHT, 1.0)
        cls = label("classification", 44, GREEN, weight=BOLD).next_to(category, RIGHT, 1.0)
        arrows = [Arrow(table[-1].get_right(), q.get_left(), color=INK, stroke_width=5, buff=0.3) for q in (quantity, category)]
        # "Supervised learning splits by the answer."
        self.play(FadeIn(table), FadeIn(head), run_time=self.share(0.2))
        # "A quantity is regression."
        at(self, 0.35)
        self.play(GrowArrow(arrows[0]), FadeIn(quantity), FadeIn(reg), run_time=self.share(0.15))
        # "A category, like present or absent, is classification."
        at(self, 0.6)
        self.play(GrowArrow(arrows[1]), FadeIn(category), FadeIn(cls), run_time=self.share(0.15))
        self.finish()


def presence_counts(scene):
    table = scene.data("presence")
    n = lambda truth, pred: table[(table["truth"] == truth) & (table["prediction"] == pred)]["n"].item()
    total = table["n"].sum()
    accuracy = (n("yes", "yes") + n("no", "no")) / total
    baseline = (n("yes", "yes") + n("yes", "no")) / total      # always answer "present"
    return n, accuracy, baseline


def accuracy_layout(scene):
    n, accuracy, baseline = presence_counts(scene)
    rows = VGroup()
    for i, (name, value, colour) in enumerate([("random forest", accuracy, BLUE),
                                               ("always \"present\"", baseline, GREY)]):
        y = 0.6 - 1.6 * i
        rows.add(VGroup(label(name, 38, colour, weight=BOLD).move_to([-2.2, y, 0], aligned_edge=RIGHT),
                        Rectangle(width=7.0 * value, height=0.9, stroke_width=0, fill_color=colour, fill_opacity=1)
                        .move_to([-1.8, y, 0], aligned_edge=LEFT),
                        ))
        rows[-1].add(label(whole_percent(value), 44, INK, weight=BOLD).next_to(rows[-1][1], RIGHT, 0.25))
    head = label("accuracy on the held-back stations", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.6)
    return head, rows


class Scene30(VideoScene):
    number = 30

    def construct(self):
        head, rows = accuracy_layout(self)
        question = card("is the species present?", GREEN, 36).next_to(head, DOWN, 0.4)
        # "So classify whether the species is present."
        self.play(FadeIn(head), FadeIn(question), run_time=self.share(0.2))
        # "The forest is 79% accurate. That sounds respectable."
        at(self, 0.35)
        self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), run_time=self.share(0.2))
        self.play(FadeIn(rows[0][2]), run_time=self.share(0.1))
        self.finish()


class Scene31(VideoScene):
    number = 31

    def construct(self):
        head, rows = accuracy_layout(self)
        self.add(head, rows[0])
        ignoring = label("ignoring every measurement", 28, SUBDUED).next_to(rows[1][0], DOWN, 0.15)
        ignoring.align_to(rows[1][0], RIGHT)
        # "Now always answer 'present', ignoring every measurement."
        self.play(FadeIn(rows[1][0]), FadeIn(ignoring), run_time=self.share(0.2))
        # "That scores 78%."
        at(self, 0.65)
        self.play(GrowFromEdge(rows[1][1], LEFT), run_time=self.share(0.15))
        self.play(FadeIn(rows[1][2]), run_time=self.share(0.1))
        self.finish()


def absent_layout(scene):
    n, _, _ = presence_counts(scene)
    absent = n("no", "yes") + n("no", "no")
    caught = n("no", "no")
    dots = VGroup(*[Circle(0.26, stroke_width=4, stroke_color=SUBDUED, fill_color=GRID, fill_opacity=0.6)
                    for _ in range(absent)]).arrange_in_grid(5, (absent + 4) // 5, buff=0.2).move_to([0, -0.2, 0])
    head = label(f"the {absent} stations where it was absent", 36, INK, weight=BOLD).to_edge(UP, buff=0.7)
    caught_name = label(f"caught: {caught}", 36, GREEN, weight=BOLD)
    missed_name = label(f"missed: {absent - caught}", 36, VERMILION, weight=BOLD)
    VGroup(caught_name, missed_name).arrange(RIGHT, buff=1.2).next_to(dots, DOWN, 0.5)
    return head, dots, caught, caught_name, missed_name


class Scene32(VideoScene):
    number = 32

    def construct(self):
        head, dots, caught, caught_name, missed_name = absent_layout(self)
        # "Of 45 stations where it was absent,"
        self.play(FadeIn(head), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03),
                  run_time=self.share(0.25))
        # "the forest caught 11."
        at(self, 0.3)
        self.play(*[d.animate.set_fill(GREEN, 1).set_stroke(GREEN) for d in dots[:caught]],
                  *[d.animate.set_fill(VERMILION, 0.25).set_stroke(VERMILION) for d in dots[caught:]],
                  FadeIn(caught_name), FadeIn(missed_name), run_time=self.share(0.2))
        # "As a map of where the species is not, it is close to useless."
        self.finish()


class Scene33(VideoScene):
    number = 33

    def construct(self):
        head, dots, caught, caught_name, missed_name = absent_layout(self)
        for d in dots[:caught]:
            d.set_fill(GREEN, 1).set_stroke(GREEN)
        for d in dots[caught:]:
            d.set_fill(VERMILION, 0.25).set_stroke(VERMILION)
        self.add(head, dots, caught_name, missed_name)
        shade = Rectangle(width=15, height=9, stroke_width=0, fill_color=BACKGROUND, fill_opacity=0.93)
        rule = VGroup(label("always compare accuracy", 48, PURPLE, weight=BOLD),
                      label("with always guessing", 48, PURPLE, weight=BOLD),
                      label("the common answer", 48, PURPLE, weight=BOLD)).arrange(DOWN, buff=0.2)
        # "So always compare accuracy with always guessing the common answer."
        self.play(FadeIn(shade), LaggedStart(*[FadeIn(r, shift=0.2 * UP) for r in rule], lag_ratio=0.4),
                  run_time=self.share(0.5))
        self.finish()


HABITAT_COLOURS = {"Shallow, warm": ORANGE, "Deep, cold": BLUE, "Shallow, productive": GREEN}


def clusters_layout(scene):
    stations = scene.data("clusters")
    axes, frame = chart([0, 200, 20], [np.log10(0.05), np.log10(20), 1], 6.8, 4.8, [0, 50, 100, 150, 200], [],
                        "depth (m)", "chlorophyll (log scale)")
    frame.move_to([-2.9, -0.5, 0])
    grey = VGroup()
    coloured = VGroup()
    for d, c, h in zip(stations["depth_m"], stations["chlorophyll_mg_m3"], stations["habitat"]):
        p = axes.c2p(d, np.log10(c))
        grey.add(Dot(p, 0.05, color=GREY, fill_opacity=0.6))
        coloured.add(Dot(p, 0.05, color=HABITAT_COLOURS[h], fill_opacity=0.8))
    means = stations.groupby("habitat").agg(n=("abundance", "size"), abundance=("abundance", "mean"),
                                            depth=("depth_m", "mean"),
                                            chl=("chlorophyll_mg_m3", lambda x: np.mean(np.log10(x))))
    names = {}
    for h, r in means.iterrows():
        text = label(h.lower().replace(", ", " and "), 28, HABITAT_COLOURS[h], weight=BOLD)
        text.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.08)
        names[h] = text.move_to(axes.c2p(r["depth"], r["chl"]))
    names["Shallow, productive"].shift(0.75 * UP)
    names["Shallow, warm"].shift(0.9 * DOWN)
    names["Deep, cold"].shift(0.2 * UP)
    return frame, grey, coloured, names, means, len(stations)


class Scene34(VideoScene):
    number = 34

    def construct(self):
        frame, grey, coloured, names, means, n = clusters_layout(self)
        note = VGroup(label("no answer column:", 32, SUBDUED, weight=BOLD),
                      label("water properties only", 32, SUBDUED, weight=BOLD)).arrange(DOWN, buff=0.12)
        note.move_to([4.2, 1.2, 0])
        three = label("k-means: three groups", 34, INK, weight=BOLD).move_to([4.2, -0.6, 0])
        head = label(f"all {n} stations", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.35)
        # "Now remove the answer entirely."
        self.play(FadeIn(frame), FadeIn(head), FadeIn(grey), run_time=self.share(0.2))
        self.play(FadeIn(note), run_time=self.share(0.1))
        # "Ask k-means, an unsupervised method, to sort the 800 stations into three groups, using only the water."
        at(self, 0.45)
        self.play(FadeIn(three), run_time=self.share(0.1))
        self.play(Transform(grey, coloured), run_time=self.share(0.25))
        self.finish()


class Scene35(VideoScene):
    number = 35

    def construct(self):
        frame, grey, coloured, names, means, n = clusters_layout(self)
        self.add(frame, coloured)
        found = label("three recognisable habitats", 34, INK, weight=BOLD).move_to([4.2, 1.8, 0])
        # "It finds three recognisable habitats: deep and cold, shallow and warm, and shallow and productive."
        self.play(FadeIn(found), run_time=self.share(0.15))
        for h in ["Deep, cold", "Shallow, warm", "Shallow, productive"]:
            self.play(FadeIn(names[h], scale=0.9), run_time=self.share(0.15))
        self.finish()


class Scene36(VideoScene):
    number = 36

    def construct(self):
        frame, grey, coloured, names, means, n = clusters_layout(self)
        self.add(frame, coloured, *names.values())
        never = card("it never saw abundance", PURPLE, 32).move_to([4.3, 2.6, 0])
        head = label("mean abundance", 30, SUBDUED, weight=BOLD).move_to([4.3, 1.5, 0])
        order = ["Shallow, productive", "Shallow, warm", "Deep, cold"]
        top = means["abundance"].max()
        bars = VGroup()
        for i, h in enumerate(order):
            y = 0.7 - 1.05 * i
            bar = Rectangle(width=2.6 * means.loc[h, "abundance"] / top, height=0.6, stroke_width=0,
                            fill_color=HABITAT_COLOURS[h], fill_opacity=1).move_to([2.9, y, 0], aligned_edge=LEFT)
            bars.add(VGroup(bar, label(f"{means.loc[h, 'abundance']:.2f}", 32, INK, weight=BOLD).next_to(bar, RIGHT, 0.15)))
        # "It never saw abundance."
        self.play(FadeIn(never, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "Yet the productive group averages 7.94 animals, against 4.25 and 2.86."
        at(self, 0.3)
        self.play(FadeIn(head), GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1]), run_time=self.share(0.2))
        at(self, 0.7)
        self.play(*[GrowFromEdge(b[0], LEFT) for b in bars[1:]], *[FadeIn(b[1]) for b in bars[1:]],
                  run_time=self.share(0.2))
        self.finish()


class Scene37(VideoScene):
    number = 37

    def construct(self):
        # Schematic: a structureless cloud, cut into three groups and then into six.
        rng = np.random.default_rng(37)
        points = rng.normal(0, 1, (220, 2)) * [1.9, 1.3]
        palette = [ORANGE, BLUE, GREEN, VERMILION, PURPLE, SKY]

        def cut(k):
            centres = points[rng.choice(len(points), k, replace=False)]
            for _ in range(10):
                owner = np.argmin(((points[:, None, :] - centres[None]) ** 2).sum(-1), 1)
                centres = np.array([points[owner == j].mean(0) if (owner == j).any() else centres[j] for j in range(k)])
            return owner

        three, six = cut(3), cut(6)
        dots = VGroup(*[Dot([x, y - 0.4, 0], 0.07, color=palette[three[i]]) for i, (x, y) in enumerate(points)])
        head = label("ask for three: three groups", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        head6 = label("ask for six: six groups, just as confident", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        always = card("unsupervised methods always return groups", PURPLE, 34).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(head), FadeIn(dots), run_time=self.share(0.15))
        # "But ask for six groups and you get six, just as confident."
        at(self, 0.15)
        self.play(ReplacementTransform(head, head6),
                  *[d.animate.set_color(palette[six[i]]) for i, d in enumerate(dots)], run_time=self.share(0.2))
        # "Unsupervised methods always return groups."
        at(self, 0.6)
        self.play(FadeIn(always, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene38(VideoScene):
    number = 38

    def construct(self):
        # Schematic: the question is fixed by the data; the machine is a slot anything can fill.
        question = VGroup(label("the question", 32, SUBDUED, weight=BOLD),
                          VGroup(card("supervised", ORANGE, 36), card("unsupervised", BLUE, 36)).arrange(RIGHT, buff=0.5)
                          ).arrange(DOWN, buff=0.3).move_to([0, 2.0, 0])
        slot = RoundedRectangle(width=5.2, height=1.3, corner_radius=0.2, stroke_color=INK, stroke_width=4)
        slot.move_to([0, -0.6, 0])
        slot_name = label("the machine", 32, SUBDUED, weight=BOLD).next_to(slot, UP, 0.25)
        machines = [label(t, 40, INK, weight=BOLD).move_to(slot) for t in
                    ["linear model", "random forest", "neural network"]]
        note = label("a neural network is one choice among many, for either", 32, PURPLE, weight=BOLD).to_edge(DOWN, buff=0.5)
        not_third = card("not a third kind of learning", VERMILION, 30).next_to(slot, DOWN, 0.35)
        # "And neural networks? They are not a third kind of learning."
        self.play(FadeIn(question), FadeIn(slot), FadeIn(slot_name), FadeIn(machines[0]), run_time=self.share(0.2))
        self.play(ReplacementTransform(machines[0], machines[1]), run_time=self.share(0.1))
        self.play(ReplacementTransform(machines[1], machines[2]), run_time=self.share(0.1))
        self.play(FadeIn(not_third), run_time=self.share(0.1))
        # "They are a machine, one choice among many, for either kind."
        at(self, 0.6)
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def pipeline_layout():
    stages = [("abundant data", "images, recordings, casts", BLUE),
              ("a specialist's labels", "slow, costly, never complete", ORANGE),
              ("the model learns", "the mapping", PURPLE),
              ("applied at scale", "to everything unlabelled", GREEN)]
    boxes = VGroup()
    for name, note, colour in stages:
        words = VGroup(label(name, 28, colour, weight=BOLD), label(note, 20, SUBDUED)).arrange(DOWN, buff=0.12)
        box = RoundedRectangle(width=max(words.width + 0.35, 2.4), height=1.5, corner_radius=0.2, stroke_color=colour, stroke_width=4)
        boxes.add(VGroup(box, words.move_to(box)))
    boxes.arrange(RIGHT, buff=0.5)
    if boxes.width > 13.4:
        boxes.scale_to_fit_width(13.4)
    boxes.move_to([0, 1.3, 0])
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), color=INK, stroke_width=4, buff=0.08)
                      for a, b in zip(boxes[:-1], boxes[1:])])
    return boxes, arrows


class Scene39(VideoScene):
    number = 39

    def construct(self):
        # Schematic: the applications page's pipeline.
        boxes, arrows = pipeline_layout()
        once = label("a specialist's judgement, spent once, applied a million times", 32, INK, weight=BOLD)
        once.move_to([0, -1.2, 0])
        # "In marine science the answers are usually a specialist's labels: slow and costly."
        self.play(FadeIn(boxes[0]), run_time=self.share(0.1))
        self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]), run_time=self.share(0.15))
        # "A model spends that judgement once and applies it a million times."
        at(self, 0.45)
        self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]), run_time=self.share(0.12))
        self.play(GrowArrow(arrows[2]), FadeIn(boxes[3]), run_time=self.share(0.12))
        self.play(FadeIn(once, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene40(VideoScene):
    number = 40

    def construct(self):
        # Schematic: a cloud of cases, and the labelled few bunched in one corner of it.
        boxes, arrows = pipeline_layout()
        self.add(boxes, arrows)
        rng = np.random.default_rng(40)
        cloud = rng.uniform([-3.2, -3.6], [3.2, -0.9], (160, 2))
        dots = VGroup(*[Dot([x, y, 0], 0.06, color=GREY, fill_opacity=0.6) for x, y in cloud])
        labelled = [i for i, (x, y) in enumerate(cloud) if x < -1.6 and y > -2.2][:14]
        warn = card("not a random sample", VERMILION, 32).move_to([4.6, -2.2, 0])
        # "But the labelled part is rarely a random sample."
        self.play(Indicate(boxes[1], color=ORANGE, scale_factor=1.05), FadeIn(dots), run_time=self.share(0.25))
        self.play(*[dots[i].animate.set_color(ORANGE).scale(1.6) for i in labelled], run_time=self.share(0.15))
        self.play(FadeIn(warn), run_time=self.share(0.1))
        # "Whatever it over-represents, the model applies everywhere."
        at(self, 0.6)
        self.play(*[d.animate.set_color(GREEN) for i, d in enumerate(dots) if i not in labelled], run_time=self.share(0.25))
        self.finish()


class Scene41(KeyPointScene):
    number, point = 41, 3


# The quiz (scenes 42–43) ------------------------------------------------------------------

class Scene42(QuizScene):
    number = 42
    question = ("A folder of seabed photographs,", "and none is labelled.", "Supervised or unsupervised?",
                "Does a neural network change that?")


class Scene43(VideoScene):
    number = 43

    def construct(self):
        # Schematic: unlabelled photos; swapping in a network leaves the question where it was.
        rng = np.random.default_rng(43)
        photos = VGroup(*[RoundedRectangle(width=1.1, height=0.8, corner_radius=0.08, stroke_color=SUBDUED, stroke_width=3,
                                           fill_color=interpolate_color(ManimColor(SKY), ManimColor(BLUE), float(rng.uniform())),
                                           fill_opacity=0.7) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.15)
        photos.move_to([-4.3, -0.4, 0])
        none = label("no labels", 30, SUBDUED, weight=BOLD).next_to(photos, UP, 0.3)
        answer = label("Unsupervised", 56, BLUE, weight=BOLD).to_edge(UP, buff=0.5)
        slot = RoundedRectangle(width=4.4, height=1.2, corner_radius=0.2, stroke_color=INK, stroke_width=4).move_to([2.6, 0.4, 0])
        machine = label("k-means", 38, INK, weight=BOLD).move_to(slot)
        network = label("neural network", 38, INK, weight=BOLD).move_to(slot)
        arrow = Arrow(photos.get_right(), slot.get_left(), color=INK, stroke_width=5, buff=0.3)
        same = label("the same question: only a machine", 32, PURPLE, weight=BOLD).next_to(slot, DOWN, 0.6)
        # "Unsupervised, because nothing is labelled."
        self.play(FadeIn(answer), FadeIn(photos), FadeIn(none), run_time=self.share(0.25))
        # "A network is only a machine: it cannot change what your data let you ask."
        at(self, 0.35)
        self.play(GrowArrow(arrow), FadeIn(slot), FadeIn(machine), run_time=self.share(0.12))
        self.play(ReplacementTransform(machine, network), run_time=self.share(0.12))
        self.play(FadeIn(same, shift=0.2 * UP), run_time=self.share(0.12))
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
