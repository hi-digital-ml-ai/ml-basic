"""Manim scenes for the neural-networks video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/09-neural-networks
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


PROMISES = ["What a neural network actually computes",
            "Why a network can fail without a warning",
            "When a network is the right tool"]
ANSWERS = ["Weighted sums with a\nbend between them;\nthe bend is the trick",
           "Standardise, watch the\nvalidation error, report\nthe spread over seeds",
           "Signal to spare, and\na combination you\ncannot name"]
RECAP = ["A network is sums with a bend",
         "It can fail without a warning",
         "It needs signal, not just rows"]


class Scene01(LearnScene):
    number = 1


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def polyline(axes, xs, ys, colour, width=6, dashed=False):
    points = [axes.c2p(x, y) for x, y in zip(xs, ys)]
    line = VMobject(color=colour, stroke_width=width).set_points_as_corners(points)
    return DashedVMobject(line, num_dashes=60) if dashed else line


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name,
          x_fmt="{:g}", y_fmt="{:g}", size=24, x_at=None):
    """Axes with tick labels and names, in the series style; returns the axes and all of it.

    `x_at` places the x tick labels at other positions than their values (a log axis).
    """
    axes = plain_axes(x_range, y_range, x_length, y_length)
    at = x_at if x_at is not None else x_ticks
    tx = VGroup(*[label(x_fmt.format(v), size, SUBDUED).next_to(axes.c2p(a, y_range[0]), DOWN, 0.15)
                  for v, a in zip(x_ticks, at)])
    ty = VGroup(*[label(y_fmt.format(v), size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15)
                  for v in y_ticks])
    xn = label(x_name, 26, SUBDUED).next_to(tx if len(tx) else axes, DOWN, 0.2)
    yn = label(y_name, 26, SUBDUED).rotate(PI / 2).next_to(ty if len(ty) else axes, LEFT, 0.2) \
        if y_name else VGroup()
    return axes, VGroup(axes, tx, ty, xn, yn)


def number_line(lo, hi, x0, x1, y, ticks, digits=2, size=26):
    """A horizontal value axis from x0 to x1 at height y; returns it and a mapper."""
    to_x = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)  # noqa: E731
    line = Line([x0, y, 0], [x1, y, 0], color=GRID, stroke_width=3)
    marks = VGroup(*[VGroup(Line([to_x(t), y - 0.08, 0], [to_x(t), y + 0.08, 0], color=GRID,
                                 stroke_width=3),
                            label(f"{t:.{digits}f}", size, SUBDUED).move_to([to_x(t), y - 0.35, 0]))
                     for t in ticks])
    return VGroup(line, marks), to_x


def strike(mobject, colour=VERMILION):
    return Line(mobject.get_left() + 0.1 * LEFT, mobject.get_right() + 0.1 * RIGHT, color=colour,
                stroke_width=6)


def card(text, colour=PURPLE, size=40):
    words = label(text, size, colour, weight=BOLD)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def hbar_rows(names, values, colours, scale, x0=-1.6, top=1.2, step=1.3, digits=3, size=32):
    """Horizontal bars, one row each: name at the left of x0, bar from x0, value after it."""
    rows = VGroup()
    for i, (name, value, colour) in enumerate(zip(names, values, colours)):
        y = top - step * i
        text = label(name, size).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=max(scale * value, 0.03), height=0.7, stroke_width=0, fill_color=colour,
                        fill_opacity=1).move_to([x0, y, 0], aligned_edge=LEFT)
        number_text = label(f"{value:.{digits}f}", size, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)
        rows.add(VGroup(text, bar, number_text))
    return rows


# Drawn networks ----------------------------------------------------------------------------

def bend_glyph(colour=ORANGE, width=0.5, straight=False):
    """A tiny activation drawn inside a unit: an S-curve, or a straight line for the identity."""
    xs = np.linspace(-1, 1, 30)
    ys = xs * 0.8 if straight else np.tanh(3 * xs) * 0.8
    points = [[x * width / 2, y * width / 2, 0] for x, y in zip(xs, ys)]
    return VMobject(color=colour, stroke_width=4).set_points_as_corners(points)


def network(sizes, xs, height=5.0, radius=0.26, glyphs=None, y=0.0):
    """Layers of circles joined by every edge. `glyphs` says which layers draw a bend:
    "bend", "straight" or None for each layer. Returns the layers and the edge groups."""
    glyphs = glyphs or [None] * len(sizes)
    layers = VGroup()
    for size, x, glyph in zip(sizes, xs, glyphs):
        spread = min(height, (size - 1) * 0.9) if size > 1 else 0
        units = VGroup()
        for yy in (np.linspace(spread / 2, -spread / 2, size) if size > 1 else [0.0]):
            circle = Circle(radius, color=INK, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1
                            ).move_to([x, yy + y, 0])
            unit = VGroup(circle)
            if glyph:
                unit.add(bend_glyph(ORANGE if glyph == "bend" else GREY, radius * 1.6,
                                    straight=glyph == "straight").move_to(circle))
            units.add(unit)
        layers.add(units)
    edges = VGroup()
    for left, right in zip(layers[:-1], layers[1:]):
        edges.add(VGroup(*[Line(a[0].get_center(), b[0].get_center(), buff=radius, color=GRID,
                                stroke_width=2.5) for a in left for b in right]))
    return layers, edges


# The puzzle (scenes 2–5, page results) --------------------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        rng = np.random.default_rng(2)
        rows = 14
        measured = VGroup(*[Square(0.3, stroke_width=0, fill_color=BLUE,
                                   fill_opacity=float(rng.choice([0.15, 0.35, 0.6, 0.85])))
                            for _ in range(rows * 8)]).arrange_in_grid(rows, 8, buff=0.05)
        counts = VGroup(*[Square(0.3, stroke_width=0, fill_color=ORANGE,
                                 fill_opacity=float(rng.choice([0.1, 0.3, 0.6, 0.9], p=[0.4, 0.3, 0.2, 0.1])))
                          for _ in range(rows)]).arrange(DOWN, buff=0.05)
        VGroup(measured, counts).arrange(RIGHT, buff=0.5).move_to([-0.4, -0.4, 0])
        measured_name = label("8 measurements", 32, BLUE, weight=BOLD).next_to(measured, UP, 0.3)
        count_name = VGroup(label("count", 32, ORANGE, weight=BOLD), label("to predict", 28, ORANGE)
                            ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(counts, RIGHT, 0.3)
        brace = Brace(measured, LEFT, color=SUBDUED)
        stations = label("720 stations", 32, SUBDUED, weight=BOLD).next_to(brace, LEFT, 0.2)
        # "Here is a survey of 720 stations, ..."
        self.play(FadeIn(measured, lag_ratio=0.005), GrowFromCenter(brace), FadeIn(stations),
                  run_time=self.share(0.3))
        # "... with eight measurements at each, ..."
        self.play(FadeIn(measured_name, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "... and a count of animals to predict."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeIn(counts, lag_ratio=0.05), FadeIn(count_name), run_time=self.share(0.25))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        # The page's network reads 12 columns: the eight measurements, with substrate and
        # season as dummy columns. 113 weights is the page's count for it.
        layers, edges = network([12, 8, 1], [-3.2, 0.4, 3.6], height=5.4, radius=0.2,
                                glyphs=[None, "bend", None], y=-0.1)
        hidden_name = label("8 hidden units", 32, BLUE, weight=BOLD).next_to(layers[1], UP, 0.25)
        weights = label("113 weights", 28, SUBDUED).next_to(layers[2], DOWN, 0.4)
        trained = label("trained on 480 stations", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.35)
        # "Fit a neural network with eight hidden units, ..."
        self.play(FadeIn(layers[0]), FadeIn(layers[2]), run_time=self.share(0.1))
        self.play(Create(edges, lag_ratio=0.01), FadeIn(layers[1]), run_time=self.share(0.3))
        self.play(FadeIn(hidden_name), FadeIn(weights), run_time=self.share(0.1))
        # "... the kind you would write without thinking. Train it on 480 stations."
        self.wait(max(self.share(0.7) - self.time, 0.01))
        self.play(FadeIn(trained, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def puzzle_layout(scene):
    curves = scene.data("learning-curves")
    network_error = curves[(curves["n"] == 480) & (curves["model"] == "neural network (8 units)")]["rmse"].item()
    baseline = scene.data("references")["baseline"].item()
    head = label("Test error at 480 training stations (lower is better)", 32, SUBDUED).to_edge(UP, buff=0.8)
    rows = hbar_rows(["network, 8 hidden units", "predict the average"], [network_error, baseline],
                     [VERMILION, GREY], 1.2, x0=-0.6, top=0.9, step=1.5)
    rows[0][2].become(label(f"{network_error:.2f}", 32, INK, weight=BOLD).next_to(rows[0][1], RIGHT, 0.2))
    return head, rows


class Scene04(VideoScene):
    number = 4

    def construct(self):
        head, rows = puzzle_layout(self)
        worse = label("worse than knowing nothing", 36, VERMILION, weight=BOLD).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(head), FadeIn(rows[0][0]), FadeIn(rows[1][0]), run_time=self.share(0.1))
        # "Its test error is 5.26."
        self.play(GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]), run_time=self.share(0.2))
        # "Simply predicting the average scores 4.402."
        self.wait(max(self.share(0.35) - self.time, 0.01))
        self.play(GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.2))
        # "The network is worse than knowing nothing."
        self.wait(max(self.share(0.72) - self.time, 0.01))
        self.play(FadeIn(worse, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        head, rows = puzzle_layout(self)
        self.add(head, rows)
        saying = card("\"Networks need a lot of data\"", SUBDUED, 38).move_to([0, -1.6, 0])
        question = card("are 480 stations too few?", PURPLE, 42).move_to([0, -2.9, 0])
        # "Neural networks need a lot of data, they say."
        self.play(FadeIn(saying, shift=0.2 * UP), run_time=self.share(0.2))
        # "So are 480 stations too few?"
        self.wait(max(self.share(0.55) - self.time, 0.01))
        self.play(FadeIn(question, scale=0.9), run_time=self.share(0.2))
        self.play(Wiggle(question[1]), run_time=self.share(0.2))
        self.finish()


# Simulated survey (scene 6, schematic) ----------------------------------------------------

class Scene06(VideoScene):
    number = 6

    def construct(self):
        box = RoundedRectangle(width=4.2, height=2.2, corner_radius=0.2, stroke_color=BLUE,
                               stroke_width=5, fill_color="#EAF2F8", fill_opacity=1)
        box_text = VGroup(label("the process", 36, BLUE, weight=BOLD),
                          label("we wrote", 36, BLUE, weight=BOLD)).arrange(DOWN, buff=0.15)
        source = VGroup(box, box_text.move_to(box)).move_to(3.8 * LEFT)
        rng = np.random.default_rng(6)
        field = VGroup(*[Dot([x, y, 0], radius=0.08, color=GREY)
                         for x, y in zip(rng.uniform(1.6, 5.8, 36), rng.uniform(-1.8, 1.8, 36))])
        field_name = label("simulated survey", 32, SUBDUED).next_to(field, DOWN, 0.4)
        arrow = Arrow(source.get_right(), [1.3, 0, 0], color=INK, stroke_width=5, buff=0.2)
        known = label("every answer checkable", 32, GREEN, weight=BOLD).next_to(source, DOWN, 0.4)

        # "A note first: this survey is simulated."
        self.play(FadeIn(source, scale=0.9), run_time=self.share(0.12))
        self.play(GrowArrow(arrow), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(d, shift=0.4 * RIGHT) for d in field], lag_ratio=0.04),
                  FadeIn(field_name), run_time=self.share(0.25))
        # "... so we can check every answer against the truth."
        self.play(FadeIn(known, shift=0.2 * UP), run_time=self.share(0.1))
        self.play(Indicate(known, color=GREEN), run_time=self.share(0.15))
        self.finish()


# Weighted sums with a bend (scenes 7–16) --------------------------------------------------

INPUT_NAMES = ["depth", "temperature", "chlorophyll"]


class Scene07(VideoScene):
    number = 7

    def construct(self):
        # Schematic: one neuron, its three inputs, weights, constant and bend.
        ys = [1.8, 0, -1.8]
        dots = VGroup(*[Circle(0.2, color=INK, stroke_width=3).move_to([-3.4, y, 0]) for y in ys])
        names = VGroup(*[label(n, 32).next_to(d, LEFT, 0.25) for n, d in zip(INPUT_NAMES, dots)])
        body = Circle(1.0, color=INK, stroke_width=5, fill_color=BACKGROUND, fill_opacity=1).move_to([1.4, 0, 0])
        arrows = VGroup(*[Arrow(d.get_right(), body.get_center(), buff=1.0, color=BLUE, stroke_width=5)
                          for d in dots])
        weights = VGroup(*[label(f"× w{i}", 30, BLUE, weight=BOLD).move_to(a.point_from_proportion(0.45) + 0.35 * UP)
                           for i, a in enumerate(arrows, 1)])
        constant = label("+ constant", 30, GREEN, weight=BOLD).next_to(body, DOWN, 0.3)
        bend = bend_glyph(ORANGE, 1.2).move_to(body)
        bend_name = label("activation: the bend", 32, ORANGE, weight=BOLD).next_to(body, UP, 0.3)
        out = Arrow(body.get_right(), body.get_right() + 2.2 * RIGHT, buff=0.1, color=INK, stroke_width=5)
        out_name = label("output", 30).next_to(out, RIGHT, 0.2)
        # "A neuron multiplies each input by a weight, ..."
        self.play(FadeIn(dots), FadeIn(names), FadeIn(body), run_time=self.share(0.12))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3),
                  LaggedStart(*[FadeIn(w) for w in weights], lag_ratio=0.3), run_time=self.share(0.25))
        # "... adds a constant, ..."
        self.wait(max(self.share(0.42) - self.time, 0.01))
        self.play(FadeIn(constant, shift=0.2 * UP), run_time=self.share(0.1))
        # "... and passes the total through a bend, called the activation."
        self.wait(max(self.share(0.58) - self.time, 0.01))
        self.play(Create(bend), FadeIn(bend_name), run_time=self.share(0.2))
        self.play(GrowArrow(out), FadeIn(out_name), run_time=self.share(0.1))
        self.finish()


TERM_NAMES = {"(Intercept)": "constant", "depth": "depth", "temp": "temperature", "chl": "chlorophyll"}


class Scene08(VideoScene):
    number = 8

    def construct(self):
        table = self.data("one-neuron")
        cols = {"lm": -0.2, "neuron": 4.0}
        heads = VGroup(label("linear regression", 32, SUBDUED, weight=BOLD).move_to([cols["lm"], 2.4, 0]),
                       label("one neuron, no bend", 32, BLUE, weight=BOLD).move_to([cols["neuron"], 2.4, 0]))
        names, lm_values, neuron_values = VGroup(), VGroup(), VGroup()
        for i, r in table.iterrows():
            y = 1.3 - 1.0 * i
            names.add(label(TERM_NAMES[r["term"]], 32).move_to([-2.0, y, 0], aligned_edge=RIGHT))
            lm_values.add(label(f"{r['lm']:.8f}", 34).move_to([cols["lm"], y, 0]))
            neuron_values.add(label(f"{r['neuron']:.8f}", 34, BLUE).move_to([cols["neuron"], y, 0]))
        same = label("the same, to eight decimal places", 36, GREEN, weight=BOLD).to_edge(DOWN, buff=0.7)
        # "Without the bend, that is linear regression."
        self.play(FadeIn(heads[0]), FadeIn(names), FadeIn(lm_values), run_time=self.share(0.3))
        # "One neuron and an ordinary regression agreed to eight decimal places."
        self.wait(max(self.share(0.4) - self.time, 0.01))
        self.play(FadeIn(heads[1]), LaggedStart(*[FadeIn(v, shift=0.3 * LEFT) for v in neuron_values],
                                                lag_ratio=0.2), run_time=self.share(0.3))
        self.play(FadeIn(same, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        # The functions themselves, drawn exactly: no data.
        z = np.linspace(-4, 4, 200)
        specs = [("logistic", 1 / (1 + np.exp(-z)), (-0.1, 1.1), "an S-curve"),
                 ("tanh", np.tanh(z), (-1.1, 1.1), "an S-curve"),
                 ("ReLU", np.maximum(z, 0), (-0.4, 4.2), "flat, then straight")]
        panels = VGroup()
        for i, (name, values, (lo, hi), note) in enumerate(specs):
            axes = plain_axes([-4, 4, 1], [lo, hi, 1], 3.4, 2.6)
            zero = DashedLine(axes.c2p(-4, 0), axes.c2p(4, 0), color=GRID, stroke_width=2)
            curve = polyline(axes, z, values, BLUE, 7)
            head = label(name, 36, INK, weight=BOLD).next_to(axes, UP, 0.3)
            sub = label(note, 30, ORANGE, weight=BOLD).next_to(axes, DOWN, 0.3)
            panels.add(VGroup(axes, zero, curve, head, sub))
        panels.arrange(RIGHT, buff=0.8).move_to([0, -0.2, 0])
        # "The bends are simple: an S-curve, ..."
        for panel in panels[:2]:
            self.play(FadeIn(panel[0]), FadeIn(panel[1]), FadeIn(panel[3]), run_time=self.share(0.06))
            self.play(Create(panel[2]), FadeIn(panel[4]), run_time=self.share(0.14))
        # "... or ReLU, flat and then straight."
        self.wait(max(self.share(0.5) - self.time, 0.01))
        self.play(FadeIn(panels[2][0]), FadeIn(panels[2][1]), FadeIn(panels[2][3]), run_time=self.share(0.08))
        self.play(Create(panels[2][2]), FadeIn(panels[2][4]), run_time=self.share(0.25))
        self.finish()


def layer_layout():
    layers, edges = network([3, 4, 1], [-3.6, 0.4, 4.0], glyphs=[None, "bend", None], radius=0.32)
    names = VGroup(*[label(n, 30).next_to(u, LEFT, 0.25) for n, u in zip(INPUT_NAMES, layers[0])])
    brace = Brace(layers[1], RIGHT, color=BLUE, buff=0.15).shift(0.0 * RIGHT)
    hidden_name = label("hidden layer", 32, BLUE, weight=BOLD).next_to(layers[1], UP, 0.3)
    out_name = label("prediction", 30).next_to(layers[2], RIGHT, 0.25)
    return layers, edges, names, hidden_name, out_name


class Scene10(VideoScene):
    number = 10

    def construct(self):
        layers, edges, names, hidden_name, out_name = layer_layout()
        first = VGroup(*[e for e in edges[0] if np.allclose(e.get_end()[1], layers[1][0].get_y(), atol=0.4)])
        # "A hidden layer is several neurons reading the same inputs."
        self.play(FadeIn(layers[0]), FadeIn(names), run_time=self.share(0.1))
        self.play(Create(edges[0]), FadeIn(layers[1], lag_ratio=0.3), run_time=self.share(0.3))
        self.play(FadeIn(hidden_name, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "Their outputs feed the prediction."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(Create(edges[1]), FadeIn(layers[2]), FadeIn(out_name), run_time=self.share(0.25))
        self.finish()


def deep_stack(hidden_layers=3, units=4, straight=True, width=9.0, height=4.4, radius=0.24):
    xs = np.linspace(-width / 2, width / 2, hidden_layers + 2)
    glyph = "straight" if straight else "bend"
    return network([3] + [units] * hidden_layers + [1], xs, height=height, radius=radius,
                   glyphs=[None] + [glyph] * hidden_layers + [None], y=-0.2)


def one_line(centre):
    axes = plain_axes([0, 1, 1], [0, 1, 1], 4.2, 2.8).move_to(centre)
    line = Line(axes.c2p(0.05, 0.12), axes.c2p(0.95, 0.88), color=BLUE, stroke_width=8)
    return VGroup(axes, line)


class Scene11(VideoScene):
    number = 11

    def construct(self):
        layers, edges = deep_stack()
        note = label("no bend: every activation a straight line", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.6)
        result = one_line([0, -0.4, 0])
        result_name = label("still one straight line", 40, BLUE, weight=BOLD).next_to(result, DOWN, 0.4)
        # "And here is the whole trick."
        self.play(FadeIn(layers), Create(edges), run_time=self.share(0.25))
        # "Without a bend, any number of layers ..."
        self.play(FadeIn(note), *[Indicate(u[1], color=VERMILION, scale_factor=1.6)
                                  for layer in layers[1:-1] for u in layer], run_time=self.share(0.3))
        # "... is still one straight line."
        self.play(ReplacementTransform(VGroup(layers, edges), result), run_time=self.share(0.2))
        self.play(FadeIn(result_name), run_time=self.share(0.1))
        self.finish()


HUMP_COLOURS = {0: VERMILION, 1: ORANGE, 2: BLUE, 5: GREEN}
HUMP_NAMES = {0: "straight line: rises", 1: "one unit: one S-curve", 2: "two units: a hump",
              5: "five units: the same"}


def hump_layout(scene):
    axes, frame = chart([2, 16, 2], [0, 1.8, 0.5], 7.6, 4.8, [4, 8, 12, 16], [0, 0.5, 1.0, 1.5],
                        "temperature (°C)", "abundance (mean, log scale)")
    frame.move_to([-2.4, -0.2, 0])
    binned = scene.data("hump-binned")
    points = VGroup(*[Dot(axes.c2p(t, y), radius=0.1, color=GREY) for t, y in
                      zip(binned["temperature_c"], binned["y"])])
    hump = scene.data("hump")
    curves, legend = {}, {}
    for i, units in enumerate([0, 1, 2, 5]):
        rows = hump[hump["units"] == units]
        curves[units] = polyline(axes, rows["temperature_c"], rows["y"], HUMP_COLOURS[units], 7,
                                 dashed=units == 5)
        legend[units] = label(HUMP_NAMES[units], 30, HUMP_COLOURS[units], weight=BOLD
                              ).move_to([2.6, 2.6 - 0.6 * i, 0], aligned_edge=LEFT)
    return axes, frame, points, curves, legend


def hump_parts(scene):
    """The two-unit network's two S-curves, in a small panel of their own."""
    parts = scene.data("hump-parts")
    lo, hi = parts[["unit1", "unit2"]].min().min(), parts[["unit1", "unit2"]].max().max()
    axes = plain_axes([2, 16, 2], [lo * 1.1, hi * 1.1, 1], 3.6, 2.2).move_to([4.6, -1.4, 0])
    zero = DashedLine(axes.c2p(2, 0), axes.c2p(16, 0), color=GRID, stroke_width=2)
    ones = VGroup(*[polyline(axes, parts["temperature_c"], parts[c], col, 6)
                    for c, col in (("unit1", PURPLE), ("unit2", SKY))])
    name = label("its two S-curves", 28, SUBDUED, weight=BOLD).next_to(axes, UP, 0.2)
    return VGroup(axes, zero, name), ones


class Scene12(VideoScene):
    number = 12

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        # "Abundance peaks at a middle temperature."
        self.play(FadeIn(frame), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in points], lag_ratio=0.1), run_time=self.share(0.25))
        # "The best straight line through it rises: it gets even the direction wrong."
        self.wait(max(self.share(0.4) - self.time, 0.01))
        self.play(Create(curves[0]), run_time=self.share(0.25))
        self.play(FadeIn(legend[0], shift=0.2 * LEFT), run_time=self.share(0.1))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        self.add(frame, points, curves[0], legend[0])
        # "One hidden unit is one S-curve. It can rise or fall, but not both."
        self.play(curves[0].animate.set_stroke(opacity=0.3), run_time=self.share(0.1))
        self.play(Create(curves[1]), FadeIn(legend[1], shift=0.2 * LEFT), run_time=self.share(0.4))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        curves[0].set_stroke(opacity=0.3)
        self.add(frame, points, curves[0], curves[1], legend[0], legend[1])
        panel, ones = hump_parts(self)
        # "Two can. Two opposing S-curves ..."
        self.play(curves[1].animate.set_stroke(opacity=0.3), FadeIn(panel), run_time=self.share(0.15))
        self.play(Create(ones[0]), Create(ones[1]), run_time=self.share(0.3))
        # "... add up to a hump."
        self.play(ReplacementTransform(ones.copy(), curves[2]), run_time=self.share(0.3))
        self.play(FadeIn(legend[2], shift=0.2 * LEFT), run_time=self.share(0.1))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        for units in (0, 1):
            curves[units].set_stroke(opacity=0.3)
        panel, ones = hump_parts(self)
        self.add(frame, points, *[curves[u] for u in (0, 1, 2)], *[legend[u] for u in (0, 1, 2)], panel, ones)
        hump = self.data("hump")
        two = hump[hump["units"] == 2]
        peak_t, peak_y = two.loc[two["y"].idxmax(), ["temperature_c", "y"]]
        peak = Dot(axes.c2p(peak_t, peak_y), radius=0.12, color=BLUE)
        peak_name = label(f"peak {peak_t:.1f} °C", 30, BLUE, weight=BOLD).next_to(peak, UP + LEFT, 0.15)
        truth = DashedLine(axes.c2p(9, 0), axes.c2p(9, 1.75), color=SUBDUED, stroke_width=3)
        truth_name = label("true optimum 9 °C", 28, SUBDUED, weight=BOLD).next_to(axes.c2p(9, 0.12), RIGHT, 0.15)
        # "Its peak is at 8.7 degrees."
        self.play(FadeOut(panel), FadeOut(ones), FadeIn(peak, scale=2), FadeIn(peak_name),
                  run_time=self.share(0.2))
        # "The truth is 9."
        self.wait(max(self.share(0.3) - self.time, 0.01))
        self.play(Create(truth), FadeIn(truth_name), run_time=self.share(0.15))
        # "Five units add nothing more."
        self.wait(max(self.share(0.58) - self.time, 0.01))
        self.play(Create(curves[5]), FadeIn(legend[5], shift=0.2 * LEFT), run_time=self.share(0.3))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        # The page's own formula, (p + 1)H + H + 1, for its 12 input columns, and its 720
        # stations (what-a-network-is.qmd, "Counting the parameters").
        inputs, stations = 12, 720
        units = [1, 2, 4, 8, 16]
        weights = [(inputs + 1) * h + h + 1 for h in units]
        axes, frame = chart([0, 5, 1], [0, 800, 200], 7.0, 4.6, [], [0, 200, 400, 600, 800], "", "weights to estimate")
        frame.move_to([-0.8, -0.1, 0])
        bars = VGroup()
        for i, (h, w) in enumerate(zip(units, weights)):
            bottom = axes.c2p(i + 0.5, 0)
            bar = Rectangle(width=0.8, height=axes.c2p(0, w)[1] - axes.c2p(0, 0)[1], stroke_width=0,
                            fill_color=ORANGE if h == 16 else BLUE, fill_opacity=1).move_to(bottom, aligned_edge=DOWN)
            name = label(str(h), 28, SUBDUED).next_to(bottom, DOWN, 0.2)
            value = label(str(w), 28, INK, weight=BOLD).next_to(bar, UP, 0.12)
            bars.add(VGroup(bar, name, value))
        units_name = label("hidden units", 26, SUBDUED).next_to(bars, DOWN, 0.7)
        line = DashedLine(axes.c2p(0, stations), axes.c2p(5, stations), color=VERMILION, stroke_width=4)
        line_name = label(f"{stations} stations", 30, VERMILION, weight=BOLD).next_to(line, RIGHT, 0.2)
        ratio = label(f"about {stations / weights[-1]:.0f} stations per weight", 30, ORANGE, weight=BOLD
                      ).move_to(axes.c2p(0.2, 560), aligned_edge=LEFT)
        # "But every arrow is a weight to estimate."
        self.play(FadeIn(frame), FadeIn(units_name), run_time=self.share(0.1))
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]))
                                for b in bars], lag_ratio=0.3), run_time=self.share(0.35))
        # "Sixteen hidden units on this survey is 225 weights, for 720 stations."
        self.play(Indicate(bars[-1][2], color=ORANGE, scale_factor=1.4), run_time=self.share(0.15))
        self.play(Create(line), FadeIn(line_name), run_time=self.share(0.15))
        self.play(FadeIn(ratio), run_time=self.share(0.1))
        self.finish()


class Scene17(KeyPointScene):
    number, point = 17, 1


# Training it (scenes 18–28) -----------------------------------------------------------------

class Scene18(VideoScene):
    number = 18

    def construct(self):
        # Schematic: a smooth error curve and a ball stepping down it.
        f = lambda x: 0.22 * (x - 1.2) ** 2 + 0.5  # noqa: E731
        df = lambda x: 0.44 * (x - 1.2)  # noqa: E731
        axes, frame = chart([-5, 5, 1], [0, 8, 1], 9, 5, [], [], "a weight", "error")
        frame.move_to([0, -0.3, 0])
        curve = axes.plot(f, x_range=[-4.6, 5], color=INK, stroke_width=5)
        xs = [-4.2, -2.3, -0.9, 0.1, 0.7]
        ball = Dot(axes.c2p(xs[0], f(xs[0])), radius=0.18, color=ORANGE).shift(0.18 * UP)

        def tangent(x):
            return Line(axes.c2p(x - 0.9, f(x) - 0.9 * df(x)), axes.c2p(x + 0.9, f(x) + 0.9 * df(x)),
                        color=BLUE, stroke_width=5)
        slope_name = label("the slope", 30, BLUE, weight=BOLD).next_to(axes.c2p(xs[0], f(xs[0])), RIGHT, 0.9)
        step_name = label("step downhill", 30, ORANGE, weight=BOLD).move_to(axes.c2p(2.8, 6.5))
        # "Training is gradient descent: find how the error changes with every weight, ..."
        self.play(FadeIn(frame), Create(curve), FadeIn(ball), run_time=self.share(0.2))
        line = tangent(xs[0])
        self.play(Create(line), FadeIn(slope_name), run_time=self.share(0.2))
        # "... and step downhill."
        self.play(FadeOut(slope_name), FadeIn(step_name), run_time=self.share(0.08))
        for x in xs[1:]:
            self.play(ball.animate.move_to(axes.c2p(x, f(x)) + 0.18 * UP), Transform(line, tangent(x)),
                      run_time=self.share(0.1))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        layers, edges, names, hidden_name, out_name = layer_layout()
        self.add(layers, edges, names, out_name)
        # The weight from temperature into the first hidden unit, as on the page's schematic.
        weight = [e for e in edges[0] if np.allclose(e.get_start(), layers[0][1][0].get_center(), atol=0.4)
                  and np.allclose(e.get_end(), layers[1][0][0].get_center(), atol=0.4)][0]
        path = VGroup(weight.copy(), edges[1][0].copy()).set_color(ORANGE).set_stroke(width=7)
        weight_name = label("a first-layer weight", 30, ORANGE, weight=BOLD).next_to(weight, UP, 0.5).shift(0.4 * LEFT)
        back_name = label("slopes, passed back one layer at a time", 32, VERMILION, weight=BOLD
                          ).to_edge(DOWN, buff=0.4)
        # "A first-layer weight acts through everything after it."
        self.play(Create(path[0]), FadeIn(weight_name), run_time=self.share(0.15))
        self.play(Create(path[1]), Indicate(layers[2], color=ORANGE), run_time=self.share(0.2))
        # "Backpropagation passes the slopes back from the output, one layer at a time."
        self.wait(max(self.share(0.4) - self.time, 0.01))
        back = [VGroup(*[Line(e.get_end(), e.get_start(), color=VERMILION, stroke_width=7) for e in group])
                for group in (edges[1], edges[0])]
        self.play(FadeIn(back_name), run_time=self.share(0.1))
        for group in back:
            self.play(ShowPassingFlash(group, time_width=0.6), run_time=self.share(0.18))
        self.finish()


GRADIENT_NAMES = {"W1": "weights into the hidden layer", "b1": "hidden-layer constants",
                  "w2": "weights into the output", "b2": "output constant"}


class Scene20(VideoScene):
    number = 20

    def construct(self):
        check = self.data("gradient-check")
        head = label("Largest disagreement with a brute-force check", 32, SUBDUED
                     ).to_edge(UP, buff=0.7)
        rows = VGroup()
        for i, r in check.iterrows():
            y = 1.5 - 0.95 * i
            rows.add(VGroup(label(GRADIENT_NAMES[r["parameter"]], 32).move_to([0.3, y, 0], aligned_edge=RIGHT),
                            label(f"{r['disagreement']:.11f}", 36, INK, weight=BOLD
                                  ).move_to([1.0, y, 0], aligned_edge=LEFT)))
        same = label("the same to about eleven decimal places", 36, GREEN, weight=BOLD).to_edge(DOWN, buff=0.8)
        # "Our hand-written gradients matched a brute-force check ..."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=self.share(0.45))
        # "... to about eleven decimal places."
        self.play(FadeIn(same, shift=0.2 * UP), run_time=self.share(0.2))
        self.finish()


RATE_COLOURS = {0.01: SKY, 0.05: GREEN, 0.2: BLUE, 0.5: ORANGE, 2.0: VERMILION}
RATE_NAMES = {0.01: "0.01: crawls", 0.05: "0.05", 0.2: "0.2: descends cleanly", 0.5: "0.5: bounces",
              2.0: "2: overflowed by step 147"}


def rates_layout(scene):
    rates = scene.data("rates")
    linear = scene.data("scaling").set_index("inputs")["mse"]["linear model"]
    top = np.log10(1500)
    axes, frame = chart([0, top, 1], [0.5, 0.9, 0.1], 7.8, 4.8, [1, 10, 100, "1,000"],
                        [0.5, 0.6, 0.7, 0.8, 0.9], "gradient-descent step (log scale)", "training error",
                        x_at=[0, 1, 2, 3], x_fmt="{}", y_fmt="{:.1f}")
    frame.move_to([-2.3, -0.2, 0])
    line = DashedLine(axes.c2p(0, linear), axes.c2p(top, linear), color=GREY, stroke_width=3)
    line_name = label("straight line", 26, SUBDUED).next_to(axes.c2p(0.05, linear), DOWN + RIGHT, 0.1)
    curves, legend = {}, {}
    head = label("learning rate", 30, SUBDUED, weight=BOLD).move_to([2.4, 2.8, 0], aligned_edge=LEFT)
    for i, (rate, rows) in enumerate(rates.groupby("learning_rate")):
        values = rows["mse"].to_numpy()
        keep = np.isfinite(values) & (values <= 0.9)
        steps = rows["step"].to_numpy()
        # The page clips the panel at 0.9; the 0.5 run's spikes and the 2 run leave it.
        curves[rate] = polyline(axes, np.log10(steps[keep]), np.clip(values[keep], 0.5, 0.9),
                                RATE_COLOURS[rate], 5) if keep.sum() > 1 else VGroup()
        legend[rate] = label(RATE_NAMES[rate], 30, RATE_COLOURS[rate], weight=BOLD
                             ).move_to([2.4, 2.1 - 0.6 * i, 0], aligned_edge=LEFT)
    return axes, VGroup(frame, line, line_name), curves, legend, head


class Scene21(VideoScene):
    number = 21

    def construct(self):
        axes, frame, curves, legend, head = rates_layout(self)
        # "The size of each step is the learning rate."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.25))
        # "At 0.01, the network has barely beaten a straight line after 1,500 steps."
        self.wait(max(self.share(0.35) - self.time, 0.01))
        self.play(Create(curves[0.01]), FadeIn(legend[0.01]), run_time=self.share(0.45))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        axes, frame, curves, legend, head = rates_layout(self)
        self.add(frame, head, curves[0.01], legend[0.01])
        up = Arrow(axes.c2p(0.05, 0.62), axes.c2p(0.05, 0.93), buff=0, color=VERMILION, stroke_width=6)
        # "At 0.2 it descends cleanly."
        self.play(Create(curves[0.05]), Create(curves[0.2]), FadeIn(legend[0.05]), FadeIn(legend[0.2]),
                  run_time=self.share(0.22))
        # "At 0.5 it bounces around."
        self.play(Create(curves[0.5]), FadeIn(legend[0.5]), run_time=self.share(0.25))
        # "At 2, the error explodes, and by step 147 it has overflowed."
        self.play(GrowArrow(up), FadeIn(legend[2.0]), run_time=self.share(0.15))
        self.play(Indicate(legend[2.0], color=VERMILION), run_time=self.share(0.2))
        self.finish()


SCALING_NAMES = {"measured units": "metres and degrees", "standardised": "standardised",
                 "linear model": "a straight line"}
SCALING_COLOURS = {"measured units": VERMILION, "standardised": BLUE, "linear model": GREY}


def scaling_layout(scene):
    scaling = scene.data("scaling").set_index("inputs")["mse"]
    order = ["measured units", "standardised", "linear model"]
    head = label("Training error after 3,000 steps", 32, SUBDUED).to_edge(UP, buff=0.6)
    rows = hbar_rows([SCALING_NAMES[k] for k in order], [scaling[k] for k in order],
                     [SCALING_COLOURS[k] for k in order], 8.0, x0=-2.0, top=1.4, step=1.2)
    return head, dict(zip(order, rows))


class Scene23(VideoScene):
    number = 23

    def construct(self):
        head, rows = scaling_layout(self)
        chips = VGroup(*[label(t, 30, INK, weight=BOLD) for t in
                         ("same network", "same learning rate", "same start")]).arrange(RIGHT, buff=0.8)
        chips.to_edge(DOWN, buff=0.7)
        # "Now leave the inputs in metres and degrees."
        self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows.values()], run_time=self.share(0.2))
        self.play(Indicate(rows["measured units"][0], color=VERMILION), run_time=self.share(0.2))
        # "Same network, same learning rate, same start."
        self.wait(max(self.share(0.45) - self.time, 0.01))
        for chip in chips:
            self.play(FadeIn(chip, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        head, rows = scaling_layout(self)
        self.add(head, *[r[0] for r in rows.values()])
        warn = label("no error, no warning", 36, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.7)
        # "It scores 0.763. Standardised, 0.570. A straight line, 0.680."
        for key, at in (("measured units", 0.0), ("standardised", 0.2), ("linear model", 0.38)):
            self.wait(max(self.share(at) - self.time, 0.01))
            self.play(GrowFromEdge(rows[key][1], LEFT), FadeIn(rows[key][2]), run_time=self.share(0.12))
        # "It loses to a straight line, and nothing warns you."
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(Indicate(rows["measured units"][2], color=VERMILION), run_time=self.share(0.15))
        self.play(FadeIn(warn, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


def stopping_layout(scene):
    runs = scene.data("early-stopping")
    top = np.log10(len(runs))
    axes, frame = chart([0, top, 1], [0.5, 1.1, 0.1], 8.6, 4.8, [1, 10, 100, "1,000", "8,000"],
                        [0.5, 0.7, 0.9, 1.1], "gradient-descent step (log scale)", "error",
                        x_at=[0, 1, 2, 3, top], x_fmt="{}", y_fmt="{:.1f}")
    frame.move_to([-1.6, -0.2, 0])
    # Every step would be 8,000 corners; a few hundred evenly spaced on the log axis suffice.
    keep = np.unique(np.round(np.logspace(0, top, 400)).astype(int)) - 1
    rows = runs.iloc[keep]
    xs = np.log10(rows["step"])
    training = polyline(axes, xs, rows["training"], BLUE, 6)
    validation = polyline(axes, xs, rows["validation"], ORANGE, 6)
    names = (label("training", 30, BLUE, weight=BOLD).next_to(training.get_end(), RIGHT, 0.2),
             label("validation", 30, ORANGE, weight=BOLD).next_to(validation.get_end(), RIGHT, 0.2))
    return axes, runs, frame, training, validation, names


class Scene25(VideoScene):
    number = 25

    def construct(self):
        axes, runs, frame, training, validation, names = stopping_layout(self)
        head = label("A 40-unit network, 8,000 steps", 32, SUBDUED).to_edge(UP, buff=0.4)
        # "Train a big network, forty units, for 8,000 steps."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.3))
        # "Its training error falls the whole way."
        self.play(Create(training), run_time=self.share(0.45))
        self.play(FadeIn(names[0]), run_time=self.share(0.1))
        self.finish()


class Scene26(VideoScene):
    number = 26

    def construct(self):
        axes, runs, frame, training, validation, names = stopping_layout(self)
        head = label("A 40-unit network, 8,000 steps", 32, SUBDUED).to_edge(UP, buff=0.4)
        self.add(frame, head, training, names[0])
        best = runs[runs["best"]].iloc[0]
        last = runs.iloc[-1]
        x = np.log10(best["step"])
        marker = DashedLine(axes.c2p(x, 0.5), axes.c2p(x, 1.05), color=SUBDUED, stroke_width=3)
        dot = Dot(axes.c2p(x, best["validation"]), radius=0.11, color=ORANGE)
        best_name = label(f"lowest: step {int(best['step']):,}", 30, ORANGE, weight=BOLD
                          ).next_to(axes.c2p(x, 1.0), LEFT, 0.15)
        worse = last["validation"] / best["validation"] - 1
        worse_name = label(f"{100 * worse:.0f}% worse by the end", 30, ORANGE, weight=BOLD
                           ).next_to(names[1], UP, 0.3).align_to(names[1], LEFT)
        keep = VGroup(label("early stopping:", 32, INK, weight=BOLD), label("keep these weights", 32, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(axes.c2p(x, 0.98), RIGHT, 0.2)
        # "Validation error is lowest at step 1,937, ..."
        self.play(Create(validation), FadeIn(names[1]), run_time=self.share(0.2))
        self.play(Create(marker), FadeIn(dot, scale=2), FadeIn(best_name), run_time=self.share(0.12))
        # "... and 4% worse by the end."
        self.wait(max(self.share(0.35) - self.time, 0.01))
        self.play(FadeIn(worse_name), run_time=self.share(0.12))
        # "Keep the weights from the best step: that is early stopping."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeIn(keep, shift=0.2 * DOWN), Indicate(dot, color=ORANGE, scale_factor=2), run_time=self.share(0.2))
        self.finish()


def seeds_layout(scene):
    seeds = scene.data("seeds")
    values = seeds["validation"].to_numpy()
    axis, to_x = number_line(0.52, 0.59, -5.2, 5.2, -0.8, [0.52, 0.54, 0.56, 0.58], 2)
    name = label("validation error, one dot per seed", 28, SUBDUED).next_to(axis, DOWN, 0.15)
    dots = VGroup(*[Dot([to_x(v), -0.8 + 0.3, 0], radius=0.16, color=BLUE, fill_opacity=0.85) for v in values])
    head = label("The same network ten times: only the seed differs", 32, SUBDUED).to_edge(UP, buff=0.8)
    return values, VGroup(axis, name), to_x, dots, head


class Scene27(VideoScene):
    number = 27

    def construct(self):
        values, axis, to_x, dots, head = seeds_layout(self)
        # "Now train the same network ten times, changing only the random seed."
        self.play(FadeIn(head), FadeIn(axis), run_time=self.share(0.2))
        self.play(LaggedStart(*[FadeIn(d, shift=1.5 * DOWN) for d in dots], lag_ratio=0.3), run_time=self.share(0.6))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        values, axis, to_x, dots, head = seeds_layout(self)
        self.add(head, axis, dots)
        span = Line([to_x(values.min()), 0.2, 0], [to_x(values.max()), 0.2, 0], color=BLUE, stroke_width=5)
        ends = VGroup(*[Line([x, 0.05, 0], [x, 0.35, 0], color=BLUE, stroke_width=5)
                        for x in (to_x(values.min()), to_x(values.max()))])
        spread = values.max() - values.min()
        span_name = label(f"spread: about {spread:.2f}", 34, BLUE, weight=BOLD).next_to(span, UP, 0.2)
        apart = label("two models closer than this: not told apart", 34, VERMILION, weight=BOLD
                      ).to_edge(DOWN, buff=0.6)
        # "Validation error varies by about 0.05."
        self.play(Create(span), FadeIn(ends), FadeIn(span_name), run_time=self.share(0.3))
        # "Two models closer than that have not been told apart."
        self.wait(max(self.share(0.45) - self.time, 0.01))
        self.play(FadeIn(apart, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene29(KeyPointScene):
    number, point = 29, 2


# The puzzle, solved (scenes 30–36) ------------------------------------------------------------

CURVE_COLOURS = {"random forest": GREEN, "linear regression": SUBDUED,
                 "neural network (8 units)": VERMILION, "neural network (tuned)": BLUE}
CURVE_NAMES = {"random forest": "random forest", "linear regression": "linear regression",
               "neural network (8 units)": "network, 8 units", "neural network (tuned)": "network, tuned"}


def curves_layout(scene):
    curves = scene.data("learning-curves")
    refs = scene.data("references").iloc[0]
    sizes = sorted(curves["n"].unique())
    lo, hi = np.log10(sizes[0]), np.log10(sizes[-1])
    axes, frame = chart([lo, hi, 0.5], [3.5, 8.2, 1], 6.6, 5.0, sizes, [4, 5, 6, 7, 8],
                        "training stations (log scale)", "test error", x_at=np.log10(sizes))
    frame.move_to([-3.0, -0.2, 0])
    baseline = DashedLine(axes.c2p(lo, refs["baseline"]), axes.c2p(hi, refs["baseline"]), color=GREY, stroke_width=4)
    oracle = DashedLine(axes.c2p(lo, refs["oracle"]), axes.c2p(hi, refs["oracle"]), color=GREY, stroke_width=4)
    right = axes.c2p(hi, 0)[0] + 0.3
    baseline_name = label(f"predict the average: {refs['baseline']:.3f}", 26, SUBDUED, weight=BOLD
                          ).move_to([right, baseline.get_y() + 0.22, 0], aligned_edge=LEFT)
    oracle_name = label(f"knows the true expected count: {refs['oracle']:.3f}", 26, SUBDUED, weight=BOLD
                        ).move_to([right, oracle.get_y() - 0.22, 0], aligned_edge=LEFT)
    band = Polygon(baseline.get_start(), baseline.get_end(), oracle.get_end(), oracle.get_start(),
                   stroke_width=0, fill_color=BLUE, fill_opacity=0.14)
    brace = Brace(Line(oracle.get_end(), baseline.get_end()), RIGHT, color=BLUE, buff=0.1)
    brace_name = label(f"{refs['baseline'] - refs['oracle']:.2f}: all there is to learn", 28, BLUE, weight=BOLD
                       ).next_to(brace, RIGHT, 0.15)
    lines, legend = {}, {}
    order = ["random forest", "linear regression", "neural network (8 units)", "neural network (tuned)"]
    for i, model in enumerate(order):
        rows = curves[curves["model"] == model].sort_values("n")
        xs, ys = np.log10(rows["n"]), rows["rmse"]
        lines[model] = VGroup(polyline(axes, xs, ys, CURVE_COLOURS[model], 6),
                              *[Dot(axes.c2p(x, y), radius=0.07, color=CURVE_COLOURS[model]) for x, y in zip(xs, ys)])
        legend[model] = label(CURVE_NAMES[model], 28, CURVE_COLOURS[model], weight=BOLD
                              ).move_to([right, 2.4 - 0.5 * i, 0], aligned_edge=LEFT)
    return dict(axes=axes, frame=frame, baseline=VGroup(baseline, baseline_name),
                oracle=VGroup(oracle, oracle_name), band=band, brace=VGroup(brace, brace_name),
                lines=lines, legend=legend, curves=curves)


class Scene30(VideoScene):
    number = 30

    def construct(self):
        c = curves_layout(self)
        # "Back to the puzzle. Predicting the average scores 4.402."
        self.play(FadeIn(c["frame"]), run_time=self.share(0.15))
        self.play(Create(c["baseline"][0]), FadeIn(c["baseline"][1]), run_time=self.share(0.2))
        # "A model that knew the true expected count at every station would score 3.701."
        self.wait(max(self.share(0.45) - self.time, 0.01))
        self.play(Create(c["oracle"][0]), FadeIn(c["oracle"][1]), run_time=self.share(0.2))
        self.finish()


class Scene31(VideoScene):
    number = 31

    def construct(self):
        c = curves_layout(self)
        self.add(c["frame"], c["baseline"], c["oracle"])
        noise = label("the rest: noise", 26, GREY, weight=BOLD).next_to(c["oracle"][1], DOWN, 0.1).shift(0.15 * DOWN
                                                                                                       ).align_to(c["oracle"][1], LEFT)
        # "Everything any method can learn lives in that window of 0.70."
        self.play(FadeIn(c["band"]), GrowFromCenter(c["brace"][0]), run_time=self.share(0.25))
        self.play(FadeIn(c["brace"][1]), c["baseline"][1].animate.shift(0.15 * UP),
                  c["oracle"][1].animate.shift(0.15 * DOWN), run_time=self.share(0.2))
        # "The rest is noise."
        self.wait(max(self.share(0.7) - self.time, 0.01))
        self.play(FadeIn(noise), run_time=self.share(0.15))
        self.finish()


def curves_base(scene, c):
    c["baseline"][1].shift(0.15 * UP)
    c["oracle"][1].shift(0.15 * DOWN)
    scene.add(c["frame"], c["band"], c["baseline"], c["oracle"], c["brace"])


class Scene32(VideoScene):
    number = 32

    def construct(self):
        c = curves_layout(self)
        curves_base(self, c)
        # "The forest wins at every size."
        for model in ("random forest", "linear regression"):
            self.play(Create(c["lines"][model]), FadeIn(c["legend"][model]), run_time=self.share(0.18))
        # "The eight-unit network never even reaches the window."
        self.wait(max(self.share(0.45) - self.time, 0.01))
        net = "neural network (8 units)"
        self.play(Create(c["lines"][net]), FadeIn(c["legend"][net]), run_time=self.share(0.3))
        self.finish()


class Scene33(VideoScene):
    number = 33

    def construct(self):
        c = curves_layout(self)
        curves_base(self, c)
        for model in ("random forest", "linear regression", "neural network (8 units)"):
            self.add(c["lines"][model], c["legend"][model])
        tuned = self.data("tuned").iloc[0]
        units = int(tuned["hidden_units"])
        note = label(f"{units} hidden unit, penalty {tuned['penalty']:g}", 28, BLUE, weight=BOLD
                     ).next_to(c["legend"]["neural network (tuned)"], DOWN, 0.15).align_to(
            c["legend"]["neural network (tuned)"], LEFT)
        model = "neural network (tuned)"
        # "Cross-validation, allowed to choose, cut the network down to one hidden unit, ..."
        self.play(Create(c["lines"][model]), FadeIn(c["legend"][model]), run_time=self.share(0.35))
        # "... with the heaviest penalty: almost a straight line."
        self.play(FadeIn(note), run_time=self.share(0.15))
        self.play(Indicate(c["lines"]["linear regression"], color=SUBDUED, scale_factor=1.0),
                  Indicate(c["lines"][model], color=BLUE, scale_factor=1.0), run_time=self.share(0.3))
        self.finish()


class Scene34(VideoScene):
    number = 34

    def construct(self):
        # Schematic: a smooth truth, noisy counts scattered around it, then the counts removed.
        axes, frame = chart([0, 10, 1], [0, 10, 1], 8, 4.6, [], [], "a predictor", "")
        frame.move_to([0, -0.4, 0])
        f = lambda x: 2 + 6 * np.exp(-((x - 5) ** 2) / 6)  # noqa: E731
        truth = axes.plot(f, x_range=[0, 10], color=BLUE, stroke_width=7)
        rng = np.random.default_rng(34)
        xs = rng.uniform(0.3, 9.7, 60)
        counts = VGroup(*[Dot(axes.c2p(x, np.clip(f(x) + rng.normal(0, 1.6), 0.2, 9.8)), radius=0.08, color=GREY)
                          for x in xs])
        before = label("target: the observed counts", 34, SUBDUED, weight=BOLD).to_edge(UP, buff=0.6)
        after = label("target: the true expected count", 34, BLUE, weight=BOLD).to_edge(UP, buff=0.6)
        # "Now take the noise away."
        self.play(FadeIn(frame), FadeIn(counts, lag_ratio=0.02), FadeIn(before), run_time=self.share(0.25))
        self.play(Create(truth), run_time=self.share(0.15))
        # "Train on the true expected count instead of the counts."
        self.play(FadeOut(counts, lag_ratio=0.02), ReplacementTransform(before, after), run_time=self.share(0.3))
        self.finish()


class Scene35(VideoScene):
    number = 35

    def construct(self):
        free = self.data("noise-free")
        n = free["n"].max()
        at = free[free["n"] == n].set_index("model")["rmse"]
        linear, net = at["linear regression"], at["neural network (8 units)"]
        head = label(f"Error against the true expected count, {n} stations", 32, SUBDUED).to_edge(UP, buff=0.8)
        rows = hbar_rows(["linear regression", "network, 8 units"], [linear, net], [GREY, BLUE], 2.4,
                         x0=-1.0, top=0.9, step=1.5, digits=2)
        better = label(f"{100 * (1 - net / linear):.0f}% better", 40, GREEN, weight=BOLD).to_edge(DOWN, buff=1.0)
        # "The eight-unit network now beats linear regression by 24%."
        self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows], run_time=self.share(0.1))
        for r in rows:
            self.play(GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=self.share(0.14))
        self.play(FadeIn(better, scale=0.9), run_time=self.share(0.12))
        # "It had learned the true shape all along."
        self.wait(max(self.share(0.65) - self.time, 0.01))
        self.play(Indicate(rows[1][1], color=BLUE, scale_factor=1.05), run_time=self.share(0.2))
        self.finish()


class Scene36(VideoScene):
    number = 36

    def construct(self):
        rows = label("short of rows", 60, INK, weight=BOLD)
        signal = label("short of signal", 60, INK, weight=BOLD)
        VGroup(rows, signal).arrange(DOWN, buff=1.0).move_to([0.5, 0, 0])
        box, mark = tick(0.9)
        box.next_to(signal, LEFT, 0.5)
        mark.move_to(box)
        # "So it was not short of rows."
        self.play(FadeIn(rows), run_time=self.share(0.15))
        self.play(Create(strike(rows)), rows.animate.set_color(GREY), run_time=self.share(0.2))
        # "It was short of signal."
        self.wait(max(self.share(0.5) - self.time, 0.01))
        self.play(FadeIn(signal), FadeIn(box), run_time=self.share(0.15))
        self.play(Create(mark), run_time=self.share(0.12))
        self.finish()


# When a network wins (scenes 37–43) ------------------------------------------------------------

T_RANGE, S_RANGE = (2, 16), (32.6, 35.6)
PANEL_MODELS = ["logistic regression", "decision tree", "random forest", "neural network"]


def viridis_rgb(p):
    stops = np.array([[0x44, 0x01, 0x54], [0x3B, 0x52, 0x8B], [0x21, 0x90, 0x8C], [0x5D, 0xC8, 0x63],
                      [0xFD, 0xE7, 0x25]], dtype=float)
    t = np.clip(p, 0, 1) * (len(stops) - 1)
    i = np.minimum(t.astype(int), len(stops) - 2)
    f = (t - i)[..., None]
    return (stops[i] * (1 - f) + stops[i + 1] * f).astype(np.uint8)


def probability_image(plane, model, width, height):
    """A model's P(core) over the plane, as the page's viridis raster."""
    rows = plane[plane["model"] == model]
    grid = rows.pivot(index="salinity_psu", columns="temperature_c", values="p_core").sort_index(ascending=False)
    image = ImageMobject(viridis_rgb(grid.to_numpy()))
    image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    image.stretch_to_fit_width(width).stretch_to_fit_height(height)
    return image


def water_axes(width, height, centre, ticks=True):
    if ticks:
        axes, frame = chart([*T_RANGE, 2], [*S_RANGE, 0.5], width, height, [4, 8, 12, 16], [33, 34, 35],
                            "temperature (°C)", "salinity")
    else:
        axes = plain_axes([*T_RANGE, 2], [*S_RANGE, 0.5], width, height)
        frame = VGroup(axes)
    frame.move_to(centre)
    return axes, frame


def stations(scene, axes, white=False, radius=0.07):
    train = scene.data("water-train")
    dots = VGroup()
    for t, s, mass in zip(train["temperature_c"], train["salinity_psu"], train["water_mass"]):
        if not (S_RANGE[0] <= s <= S_RANGE[1]):   # the page's plane crops a few stations too
            continue
        core = mass == "core"
        colour = WHITE if white else (ORANGE if core else GREY)
        if core:
            dots.add(Dot(axes.c2p(t, s), radius=radius, color=colour))
        else:
            dots.add(Cross(scale_factor=radius * 0.9, stroke_color=colour, stroke_width=2.5).move_to(axes.c2p(t, s)))
    return dots


class Scene37(VideoScene):
    number = 37

    def construct(self):
        axes, frame = water_axes(8.4, 5.4, [-0.8, -0.1, 0])
        dots = stations(self, axes)
        # The band's edges from the page's make_water_mass(): salinity 32.68 + 0.16 T, plus or minus 0.3.
        edge = lambda t, side: 33.0 + 0.16 * t - 0.32 + side * 0.30  # noqa: E731
        band = Polygon(axes.c2p(2, edge(2, -1)), axes.c2p(16, edge(16, -1)), axes.c2p(16, edge(16, 1)),
                       axes.c2p(2, edge(2, 1)), stroke_width=0, fill_color=ORANGE, fill_opacity=0.15)
        core_name = label("water-mass core", 32, ORANGE, weight=BOLD).next_to(axes.c2p(13.5, edge(13.5, 1)), UP, 0.5)
        tag = label("constructed example", 28, SUBDUED).to_corner(UR, buff=0.4)
        # "Now a constructed case."
        self.play(FadeIn(frame), FadeIn(tag), run_time=self.share(0.2))
        # "A water mass is a diagonal band on a temperature–salinity diagram."
        self.play(FadeIn(dots, lag_ratio=0.01), run_time=self.share(0.3))
        self.play(FadeIn(band), FadeIn(core_name), run_time=self.share(0.2))
        self.finish()


PANEL_W, PANEL_H = 5.2, 2.7
PANEL_CENTRES = [[-3.2, 1.4, 0], [3.2, 1.4, 0], [-3.2, -2.3, 0], [3.2, -2.3, 0]]


def boundary_panels(scene):
    plane = scene.data("water-plane")
    scores = scene.data("water-auc").set_index("model")
    panels = {}
    for model, centre in zip(PANEL_MODELS, PANEL_CENTRES):
        axes, frame = water_axes(PANEL_W, PANEL_H, centre, ticks=False)
        image = probability_image(plane, model, PANEL_W, PANEL_H).move_to(axes.get_center())
        dots = stations(scene, axes, white=True, radius=0.035)
        name = label("network" if model == "neural network" else model, 28, INK, weight=BOLD
                     ).next_to(axes, UP, 0.12).align_to(axes, LEFT)
        auc = label(f"AUC {scores.loc[model, 'auc']:.3f}", 28, BLUE, weight=BOLD).next_to(axes, UP, 0.12
                                                                                          ).align_to(axes, RIGHT)
        panels[model] = (image, dots, name, auc, axes)
    return panels, scores


def show_panel(panel):
    image, dots, name, auc, _ = panel
    return [FadeIn(image), FadeIn(dots), FadeIn(name)]


class Scene38(VideoScene):
    number = 38

    def construct(self):
        panels, _ = boundary_panels(self)
        # "Logistic regression can draw one straight line: 0.715."
        self.play(*show_panel(panels["logistic regression"]), run_time=self.share(0.15))
        self.play(FadeIn(panels["logistic regression"][3]), run_time=self.share(0.1))
        # "Trees cut along one axis at a time."
        self.wait(max(self.share(0.38) - self.time, 0.01))
        self.play(*show_panel(panels["decision tree"]), FadeIn(panels["decision tree"][3]), run_time=self.share(0.2))
        # "A forest of 500 reaches 0.926."
        self.wait(max(self.share(0.7) - self.time, 0.01))
        self.play(*show_panel(panels["random forest"]), FadeIn(panels["random forest"][3]), run_time=self.share(0.2))
        self.finish()


class Scene39(VideoScene):
    number = 39

    def construct(self):
        panels, scores = boundary_panels(self)
        for model in PANEL_MODELS[:3]:
            self.add(*panels[model][:4])
        net = panels["neural network"]
        weights = int(scores.loc["neural network", "weights"])
        weights_name = label(f"{weights} weights", 26, ORANGE, weight=BOLD).next_to(net[2], RIGHT, 0.2)
        # "A network with seventeen weights reaches 0.998."
        self.play(*show_panel(net), FadeIn(weights_name), run_time=self.share(0.4))
        self.play(FadeIn(net[3], scale=1.3), run_time=self.share(0.2))
        self.finish()


class Scene40(VideoScene):
    number = 40

    def construct(self):
        axes, frame = water_axes(7.8, 5.4, [-2.2, -0.1, 0])
        plane = self.data("water-plane")
        image = probability_image(plane, "neural network", 7.8, 5.4).move_to(axes.get_center())
        dots = stations(self, axes, white=True, radius=0.05)
        units = self.data("water-units")
        # Each hidden unit switches at the line where its weighted sum is zero; the two with
        # the largest weights into the output are the band's edges.
        strongest = units["out"].abs().nlargest(2).index
        lines = VGroup()
        for i, u in units.iterrows():
            def salinity(t):
                z_t = (t - u["t_mean"]) / u["t_sd"]
                return u["s_mean"] + u["s_sd"] * (-(u["bias"] + u["t"] * z_t) / u["s"])
            ts = np.linspace(*T_RANGE, 200)
            ss = np.array([salinity(t) for t in ts])
            keep = (ss >= S_RANGE[0]) & (ss <= S_RANGE[1])
            if keep.sum() < 2:
                continue
            strong = i in strongest
            lines.add(polyline(axes, ts[keep], ss[keep], ORANGE if strong else WHITE, 7 if strong else 3))
        name = VGroup(label("each hidden unit:", 32, INK, weight=BOLD), label("a line at any angle", 32, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([2.9, 1.2, 0], aligned_edge=LEFT)
        edges = VGroup(label("two of them:", 32, ORANGE, weight=BOLD), label("the band's edges", 32, ORANGE, weight=BOLD)
                       ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([2.9, -0.6, 0], aligned_edge=LEFT)
        self.add(frame, image, dots)
        # "Each hidden unit is a weighted sum: a new axis, at any angle."
        self.play(FadeIn(name), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3), run_time=self.share(0.4))
        # "Two of them, one at each edge, make the stripe."
        self.wait(max(self.share(0.5) - self.time, 0.01))
        strong = [l for l in lines if l.get_color() == ManimColor(ORANGE)]
        self.play(FadeIn(edges), *[Indicate(l, color=ORANGE, scale_factor=1.0) for l in strong],
                  run_time=self.share(0.3))
        self.finish()


class Scene41(VideoScene):
    number = 41

    def construct(self):
        sizes = self.data("water-sizes")
        cols = {"neural network": 1.2, "random forest": 4.4}
        head = label("AUC on the 2,000 test stations", 32, SUBDUED).to_edge(UP, buff=0.8)
        heads = VGroup(*[label(m, 32, BLUE if m == "neural network" else GREEN, weight=BOLD).move_to([x, 2.0, 0])
                         for m, x in cols.items()])
        cells = {}
        names = VGroup()
        for i, n in enumerate(sorted(sizes["n"].unique())):
            y = 0.9 - 1.1 * i
            names.add(label(f"{n:,} stations", 32).move_to([-1.2, y, 0], aligned_edge=RIGHT))
            for m, x in cols.items():
                v = sizes[(sizes["n"] == n) & (sizes["model"] == m)]["auc"].item()
                cells[(n, m)] = label(f"{v:.3f}", 40, INK, weight=BOLD).move_to([x, y, 0])
        first, last = min(sizes["n"]), max(sizes["n"])
        # "On just 100 stations, the network reaches 0.994."
        self.play(FadeIn(head), FadeIn(heads), FadeIn(names), run_time=self.share(0.15))
        self.play(*[FadeIn(cells[(n, "neural network")]) for n in sorted(sizes["n"].unique())], run_time=self.share(0.15))
        self.play(Circumscribe(cells[(first, "neural network")], color=BLUE), run_time=self.share(0.2))
        # "The forest needs 1,600 to reach 0.996."
        self.play(*[FadeIn(cells[(n, "random forest")]) for n in sorted(sizes["n"].unique())], run_time=self.share(0.15))
        self.play(Circumscribe(cells[(last, "random forest")], color=GREEN), run_time=self.share(0.2))
        self.finish()


class Scene42(VideoScene):
    number = 42

    def construct(self):
        # Schematic: the combination the page names, added as a column.
        rng = np.random.default_rng(42)
        def column(name, colour, n=6):
            cells = VGroup(*[Rectangle(width=2.6, height=0.45, stroke_color=GRID, stroke_width=2, fill_color=colour,
                                       fill_opacity=float(rng.uniform(0.1, 0.5))) for _ in range(n)]
                           ).arrange(DOWN, buff=0)
            return VGroup(label(name, 28, INK, weight=BOLD).next_to(cells, UP, 0.2), cells)
        t = column("temperature", BLUE)
        s = column("salinity", BLUE)
        combo = column("salinity − 0.16 × temperature", GREEN)
        combo[0].scale(0.9)
        VGroup(t, s).arrange(RIGHT, buff=0.1).move_to([-3.4, 0.6, 0])
        combo.next_to(VGroup(t, s), RIGHT, 0.6).shift(0.0 * UP)
        named = label("named: add a column, use a simpler model", 32, GREEN, weight=BOLD).move_to([0, -2.3, 0])
        unnamed = label("not named: a network searches for it", 32, BLUE, weight=BOLD).next_to(named, DOWN, 0.4)
        # "If you can name the combination, add it as a column and use a simpler model."
        self.play(FadeIn(t), FadeIn(s), run_time=self.share(0.12))
        self.play(FadeIn(combo, shift=0.5 * LEFT), run_time=self.share(0.2))
        self.play(FadeIn(named), run_time=self.share(0.12))
        # "A network searches for the ones you cannot name."
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(FadeIn(unnamed, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene43(VideoScene):
    number = 43

    def construct(self):
        # Schematic: a grid of pixels, a 3x3 patch that is an edge, and edges that make a shape.
        rng = np.random.default_rng(43)
        n = 9
        shade = rng.uniform(0.1, 0.35, (n, n))
        shade[:, 4:] += 0.5            # a vertical edge down the middle
        pixels = VGroup(*[Square(0.4, stroke_width=1, stroke_color=BACKGROUND, fill_color=INK,
                                 fill_opacity=float(np.clip(shade[i, j], 0, 1)))
                          for i in range(n) for j in range(n)]).arrange_in_grid(n, n, buff=0).move_to([-4.2, -0.3, 0])
        patch = SurroundingRectangle(VGroup(*[pixels[i * n + j] for i in range(3, 6) for j in range(3, 6)]),
                                     color=ORANGE, buff=0.02, stroke_width=6)
        pixel_name = label("pixels", 32, SUBDUED, weight=BOLD).next_to(pixels, UP, 0.3)
        arrow1 = Arrow([-2.2, -0.3, 0], [-0.6, -0.3, 0], color=INK, stroke_width=5)
        edge = Line([0.2, -1.1, 0], [0.2, 0.5, 0], color=ORANGE, stroke_width=10)
        edge_name = label("an edge", 32, ORANGE, weight=BOLD).next_to(edge, UP, 0.3)
        arrow2 = Arrow([1.0, -0.3, 0], [2.6, -0.3, 0], color=INK, stroke_width=5)
        body = Ellipse(width=2.4, height=1.2, color=BLUE, stroke_width=8).move_to([4.4, -0.3, 0])
        tail = Polygon([5.6, -0.3, 0], [6.4, 0.2, 0], [6.4, -0.8, 0], color=BLUE, stroke_width=8)
        shape_name = label("a shape", 32, BLUE, weight=BOLD).next_to(body, UP, 0.5)
        nobody = label("nobody can write them all down", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.7)
        # "That is images and sound: an edge is a combination of pixels, ..."
        self.play(FadeIn(pixels, lag_ratio=0.01), FadeIn(pixel_name), run_time=self.share(0.2))
        self.play(Create(patch), GrowArrow(arrow1), FadeIn(edge), FadeIn(edge_name), run_time=self.share(0.2))
        self.play(GrowArrow(arrow2), Create(body), Create(tail), FadeIn(shape_name), run_time=self.share(0.2))
        # "... and nobody can write them all down."
        self.wait(max(self.share(0.72) - self.time, 0.01))
        self.play(FadeIn(nobody, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene44(KeyPointScene):
    number, point = 44, 3


# Quiz (scenes 45–46) -------------------------------------------------------------------------

class Scene45(QuizScene):
    number = 45
    question = ("A network has ten hidden layers,", "each of a hundred units,", "and every activation is the identity.",
                "What shapes can it fit?")


class Scene46(VideoScene):
    number = 46

    def construct(self):
        layers, edges = deep_stack(hidden_layers=10, units=5, width=11.0, height=3.8, radius=0.16)
        answer = label("Only a straight line", 52, BLUE, weight=BOLD).to_edge(UP, buff=0.6)
        result = one_line([0, -0.4, 0])
        why = VGroup(label("a weighted sum of weighted sums", 34, INK, weight=BOLD),
                     label("is still a weighted sum", 34, INK, weight=BOLD)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        # "Only a straight line."
        self.play(FadeIn(answer), FadeIn(layers), Create(edges), run_time=self.share(0.25))
        self.play(ReplacementTransform(VGroup(layers, edges), result), run_time=self.share(0.25))
        # "A weighted sum of weighted sums is still a weighted sum."
        self.play(FadeIn(why, shift=0.2 * UP), run_time=self.share(0.15))
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
