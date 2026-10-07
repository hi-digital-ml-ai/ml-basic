"""Manim scenes for the neural-networks video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/09-neural-networks
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

Scenes marked "page results" read visuals/data/*.csv, which tools/figures-for-video.R
writes from the pages through exports.R. Single numbers come from the "<page>-numbers"
tables, so a scene shows the page's own value. The other scenes are schematic: made-up
shapes, never numbers that could pass for survey results. The opening, key-point,
recap, quiz and end-card scenes are shared (mlbasic_video.py) and read PROMISES,
ANSWERS and RECAP from here. Consecutive scenes about one picture share a builder, so
each starts where the previous one ended.
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
ANSWERS = ["Weighted sums with a\nbend between them;\nthe bend does the work",
           "Set it up on validation\ndata, and report the\nspread over seeds",
           "Signal to spare, and\na combination nobody\nhas named"]
RECAP = ["A network is sums with a bend",
         "It can fail without a warning",
         "It needs signal, not just rows"]

WORDS = {7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


class Scene01(LearnScene):
    number = 1


def value(scene, page, name):
    """One number from a page's "<page>-numbers" table."""
    table = scene.data(f"{page}-numbers").set_index("name")["value"]
    return table[name]


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


def hbar_rows(names, values, colours, scale, x0=-1.6, top=1.2, step=1.3, digits=3, size=32):
    """Horizontal bars, one row each: name at the left of x0, bar from x0, value after it."""
    rows = VGroup()
    for i, (name, v, colour) in enumerate(zip(names, values, colours)):
        y = top - step * i
        text = label(name, size).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=max(scale * v, 0.03), height=0.7, stroke_width=0, fill_color=colour,
                        fill_opacity=1).move_to([x0, y, 0], aligned_edge=LEFT)
        number_text = label(f"{v:.{digits}f}", size, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)
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


# Opening (scenes 2–3, schematic) -------------------------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        layers, edges = network([3, 4, 1], [-5.0, -2.4, 0.2], height=3.6, radius=0.28,
                                glyphs=[None, "bend", None], y=-0.2)
        sums = label("Weighted sums", 34, BLUE, weight=BOLD).move_to([3.6, 1.6, 0], aligned_edge=LEFT)
        bend = label("A bend", 34, ORANGE, weight=BOLD).move_to([3.6, 0.0, 0], aligned_edge=LEFT)
        walk = label("A walk downhill", 34, GREEN, weight=BOLD).move_to([3.6, -1.6, 0], aligned_edge=LEFT)
        valley = plain_axes([-2, 2, 1], [0, 4, 1], 1.6, 0.9)
        curve = valley.plot(lambda x: x ** 2, x_range=[-1.9, 1.9], color=GREEN, stroke_width=4)
        ball = Dot(valley.c2p(-1.4, 1.96), radius=0.08, color=GREEN)
        downhill = VGroup(curve, ball).next_to(walk, LEFT, 0.35)
        # "Neural networks are behind much of the artificial intelligence in the news."
        self.play(FadeIn(layers[0]), FadeIn(layers[2]), run_time=self.share(0.1))
        self.play(Create(edges, lag_ratio=0.02), FadeIn(layers[1], lag_ratio=0.2), run_time=self.share(0.25))
        # "Yet every part of one is something this course has already met: weighted sums, ..."
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(FadeIn(sums, shift=0.2 * LEFT), edges.animate.set_color(BLUE), run_time=self.share(0.1))
        # "... a bend, ..."
        self.play(FadeIn(bend, shift=0.2 * LEFT),
                  *[Indicate(u[1], color=ORANGE, scale_factor=1.6) for u in layers[1]], run_time=self.share(0.1))
        # "... and a walk downhill."
        self.play(FadeIn(walk, shift=0.2 * LEFT), FadeIn(downhill), run_time=self.share(0.08))
        self.play(ball.animate.move_to(valley.c2p(0, 0) + 0.06 * UP), run_time=self.share(0.08))
        self.finish()


class Scene03(VideoScene):
    number = 3

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
        measured_name = label("Depth, temperature and more", 32, BLUE, weight=BOLD).next_to(measured, UP, 0.3)
        count_name = VGroup(label("Count of", 32, ORANGE, weight=BOLD), label("one species", 32, ORANGE, weight=BOLD)
                            ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(counts, RIGHT, 0.3)
        brace = Brace(measured, LEFT, color=SUBDUED)
        stations = label("Coastal stations", 32, SUBDUED, weight=BOLD).next_to(brace, LEFT, 0.2)
        tag = label("Simulated survey", 28, SUBDUED).to_corner(UR, buff=0.4)
        # "As throughout the course, the examples use one simulated survey: ..."
        self.play(FadeIn(tag), FadeIn(measured, lag_ratio=0.005), run_time=self.share(0.3))
        # "... counts of one species at coastal stations, ..."
        self.play(FadeIn(counts, lag_ratio=0.05), FadeIn(count_name), run_time=self.share(0.15))
        self.play(GrowFromCenter(brace), FadeIn(stations), run_time=self.share(0.12))
        # "... with the depth, the water temperature and more at each."
        self.wait(max(self.share(0.65) - self.time, 0.01))
        self.play(FadeIn(measured_name, shift=0.2 * DOWN), run_time=self.share(0.15))
        self.finish()


# Weighted sums with a bend (scenes 4–13) --------------------------------------------------

INPUT_NAMES = ["Depth", "Temperature", "Chlorophyll"]


class Scene04(VideoScene):
    number = 4

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
        bend_name = label("Activation: the bend", 32, ORANGE, weight=BOLD).next_to(body, UP, 0.3)
        out = Arrow(body.get_right(), body.get_right() + 2.2 * RIGHT, buff=0.1, color=INK, stroke_width=5)
        out_name = label("Output", 30).next_to(out, RIGHT, 0.2)
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


TERM_NAMES = {"(Intercept)": "Constant", "depth": "Depth", "temperature": "Temperature",
              "chlorophyll": "Chlorophyll"}


class Scene05(VideoScene):
    number = 5

    def construct(self):
        table = self.data("one-neuron")
        places = int(value(self, "what-a-network-is", "places"))
        cols = {"lm": -0.2, "neuron": 4.0}
        heads = VGroup(label("Linear regression", 32, SUBDUED, weight=BOLD).move_to([cols["lm"], 2.4, 0]),
                       label("One neuron, no bend", 32, BLUE, weight=BOLD).move_to([cols["neuron"], 2.4, 0]))
        names, lm_values, neuron_values = VGroup(), VGroup(), VGroup()
        for i, r in table.iterrows():
            y = 1.3 - 1.0 * i
            names.add(label(TERM_NAMES[r["term"]], 32).move_to([-2.2, y, 0], aligned_edge=RIGHT))
            # One decimal fewer than the agreement, so rounding cannot split the last digit.
            lm_values.add(label(f"{r['lm']:.{places - 1}f}", 34).move_to([cols["lm"], y, 0]))
            neuron_values.add(label(f"{r['neuron']:.{places - 1}f}", 34, BLUE).move_to([cols["neuron"], y, 0]))
        same = label(f"The same, to {WORDS[places]} decimal places", 36, GREEN, weight=BOLD
                     ).to_edge(DOWN, buff=0.7)
        # "Without the bend, that is linear regression."
        self.play(FadeIn(heads[0]), FadeIn(names), FadeIn(lm_values), run_time=self.share(0.3))
        # "One neuron and an ordinary regression agreed to nine decimal places."
        self.wait(max(self.share(0.4) - self.time, 0.01))
        self.play(FadeIn(heads[1]), LaggedStart(*[FadeIn(v, shift=0.3 * LEFT) for v in neuron_values],
                                                lag_ratio=0.2), run_time=self.share(0.3))
        self.play(FadeIn(same, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        # The functions themselves, drawn exactly: no data.
        z = np.linspace(-4, 4, 200)
        specs = [("Logistic", 1 / (1 + np.exp(-z)), (-0.1, 1.1), "An S-curve"),
                 ("tanh", np.tanh(z), (-1.1, 1.1), "An S-curve"),
                 ("ReLU", np.maximum(z, 0), (-0.4, 4.2), "Flat, then straight")]
        panels = VGroup()
        for name, values, (lo, hi), note in specs:
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
    hidden_name = label("Hidden layer", 32, BLUE, weight=BOLD).next_to(layers[1], UP, 0.3)
    out_name = label("Prediction", 30).next_to(layers[2], RIGHT, 0.25)
    return layers, edges, names, hidden_name, out_name


class Scene07(VideoScene):
    number = 7

    def construct(self):
        layers, edges, names, hidden_name, out_name = layer_layout()
        # "A hidden layer is several neurons reading the same inputs."
        self.play(FadeIn(layers[0]), FadeIn(names), run_time=self.share(0.1))
        self.play(Create(edges[0]), FadeIn(layers[1], lag_ratio=0.3), run_time=self.share(0.3))
        self.play(FadeIn(hidden_name, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "An output neuron adds up their results into the prediction."
        self.wait(max(self.share(0.55) - self.time, 0.01))
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


class Scene08(VideoScene):
    number = 8

    def construct(self):
        layers, edges = deep_stack()
        note = label("No bend: every activation a straight line", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.6)
        result = one_line([0, -0.4, 0])
        result_name = label("Still one straight line", 40, BLUE, weight=BOLD).next_to(result, DOWN, 0.4)
        # "And here is the whole trick."
        self.play(FadeIn(layers), Create(edges), run_time=self.share(0.25))
        # "Without a bend, any number of layers ..."
        self.play(FadeIn(note), *[Indicate(u[1], color=VERMILION, scale_factor=1.6)
                                  for layer in layers[1:-1] for u in layer], run_time=self.share(0.3))
        # "... adds up to one straight line."
        self.play(ReplacementTransform(VGroup(layers, edges), result), run_time=self.share(0.2))
        self.play(FadeIn(result_name), run_time=self.share(0.1))
        self.finish()


HUMP_COLOURS = {0: VERMILION, 1: ORANGE, 2: BLUE}
HUMP_NAMES = {0: "Straight line", 1: "One unit: one bend", 2: "Two units: a hump"}


def hump_layout(scene):
    axes, frame = chart([2, 16, 2], [0, 1.8, 0.5], 7.6, 4.8, [4, 8, 12, 16], [0, 0.5, 1.0, 1.5],
                        "Temperature (°C)", "log(1 + abundance)")
    frame.move_to([-2.4, -0.2, 0])
    binned = scene.data("hump-binned")
    points = VGroup(*[Dot(axes.c2p(t, y), radius=0.1, color=GREY) for t, y in
                      zip(binned["temperature_c"], binned["y"])])
    points_name = label("Station means, one-degree bins", 26, SUBDUED).next_to(frame, UP, 0.15
                                                                              ).align_to(frame, LEFT)
    hump = scene.data("hump")
    curves, legend = {}, {}
    for i, units in enumerate([0, 1, 2]):
        rows = hump[hump["units"] == units]
        curves[units] = polyline(axes, rows["temperature_c"], rows["y"], HUMP_COLOURS[units], 7)
        legend[units] = label(HUMP_NAMES[units], 30, HUMP_COLOURS[units], weight=BOLD
                              ).move_to([2.6, 2.6 - 0.6 * i, 0], aligned_edge=LEFT)
    return axes, VGroup(frame, points_name), points, curves, legend


def hump_parts(scene):
    """The two-unit network's two bends, in a small panel of their own."""
    parts = scene.data("hump-parts")
    lo, hi = parts[["unit1", "unit2"]].min().min(), parts[["unit1", "unit2"]].max().max()
    axes = plain_axes([2, 16, 2], [lo * 1.1, hi * 1.1, 1], 3.6, 2.2).move_to([4.6, -1.4, 0])
    zero = DashedLine(axes.c2p(2, 0), axes.c2p(16, 0), color=GRID, stroke_width=2)
    ones = VGroup(*[polyline(axes, parts["temperature_c"], parts[c], col, 6)
                    for c, col in (("unit1", PURPLE), ("unit2", SKY))])
    name = label("Its two bends", 28, SUBDUED, weight=BOLD).next_to(axes, UP, 0.2)
    return VGroup(axes, zero, name), ones


class Scene09(VideoScene):
    number = 9

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        # "Abundance peaks at a middle temperature."
        self.play(FadeIn(frame), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in points], lag_ratio=0.1), run_time=self.share(0.25))
        # "A straight line cannot turn over: the best one rises gently and misses the peak."
        self.wait(max(self.share(0.4) - self.time, 0.01))
        self.play(Create(curves[0]), run_time=self.share(0.25))
        self.play(FadeIn(legend[0], shift=0.2 * LEFT), run_time=self.share(0.1))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        self.add(frame, points, curves[0], legend[0])
        # "One hidden unit adds a single bend. It can fall, but it cannot rise first."
        self.play(curves[0].animate.set_stroke(opacity=0.3), run_time=self.share(0.1))
        self.play(Create(curves[1]), FadeIn(legend[1], shift=0.2 * LEFT), run_time=self.share(0.45))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        curves[0].set_stroke(opacity=0.3)
        self.add(frame, points, curves[0], curves[1], legend[0], legend[1])
        panel, ones = hump_parts(self)
        # "Two can. A rising bend and a falling one ..."
        self.play(curves[1].animate.set_stroke(opacity=0.3), FadeIn(panel), run_time=self.share(0.15))
        self.play(Create(ones[0]), Create(ones[1]), run_time=self.share(0.3))
        # "... add up to a hump."
        self.play(ReplacementTransform(ones.copy(), curves[2]), run_time=self.share(0.3))
        self.play(FadeIn(legend[2], shift=0.2 * LEFT), run_time=self.share(0.1))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        for units in (0, 1):
            curves[units].set_stroke(opacity=0.3)
        panel, ones = hump_parts(self)
        self.add(frame, points, *curves.values(), *legend.values(), panel, ones)
        peak_c = value(self, "what-a-network-is", "peak_c")
        top_low = int(value(self, "what-a-network-is", "top_low"))
        n_weights = int(value(self, "what-a-network-is", "two_unit_weights"))
        hump = self.data("hump")
        two = hump[hump["units"] == 2]
        peak_y = two.loc[(two["temperature_c"] - peak_c).abs().idxmin(), "y"]
        peak = Dot(axes.c2p(peak_c, peak_y), radius=0.12, color=BLUE)
        peak_name = label(f"Peak {peak_c:.1f} °C", 30, BLUE, weight=BOLD).move_to(axes.c2p(5.0, peak_y))
        bin_band = Rectangle(width=axes.c2p(top_low + 1, 0)[0] - axes.c2p(top_low, 0)[0],
                             height=axes.c2p(0, 1.8)[1] - axes.c2p(0, 0)[1], stroke_width=0,
                             fill_color=GREEN, fill_opacity=0.15).move_to(axes.c2p(top_low + 0.5, 0.9))
        bin_name = VGroup(label("Most animals:", 26, GREEN, weight=BOLD),
                          label(f"{top_low}–{top_low + 1} °C", 26, GREEN, weight=BOLD)
                          ).arrange(DOWN, buff=0.06).next_to(axes.c2p(top_low + 1, 0.3), RIGHT, 0.15)
        weights = VGroup(label("Shape not given,", 32, INK, weight=BOLD),
                         label(f"found with {n_weights} weights", 32, INK, weight=BOLD)
                         ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([2.6, -1.4, 0], aligned_edge=LEFT)
        # "Its peak is at 8.7 degrees, ..."
        self.play(FadeOut(panel), FadeOut(ones), FadeIn(peak, scale=2), FadeIn(peak_name),
                  run_time=self.share(0.15))
        # "... inside the one-degree band where the stations hold the most animals."
        self.wait(max(self.share(0.22) - self.time, 0.01))
        self.play(FadeIn(bin_band), FadeIn(bin_name), run_time=self.share(0.15))
        # "Nobody told the network that shape. It found it with seven weights."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeIn(weights, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        small = int(value(self, "what-a-network-is", "small_net"))
        small_linear = int(value(self, "what-a-network-is", "small_linear"))
        large = int(value(self, "what-a-network-is", "large_net"))
        layers, edges = network([3, 4, 1], [-6.0, -4.0, -2.0], height=3.4, radius=0.26,
                                glyphs=[None, "bend", None], y=0.0)
        rows = [("3 inputs, 4 hidden units", f"{small} weights", ORANGE),
                ("Linear regression", f"{small_linear} weights", SUBDUED),
                ("10 inputs, 20 hidden units", f"{large} weights", VERMILION)]
        counts = VGroup(*[VGroup(label(name, 32, INK).move_to([3.3, 1.0 - 1.0 * i, 0], aligned_edge=RIGHT),
                                 label(count, 36, colour, weight=BOLD).move_to([3.6, 1.0 - 1.0 * i, 0], aligned_edge=LEFT))
                          for i, (name, count, colour) in enumerate(rows)])
        self.add(layers, edges)
        # "But every arrow is a weight to estimate."
        self.play(edges.animate.set_color(ORANGE).set_stroke(width=4), run_time=self.share(0.15))
        self.play(*[Indicate(u[0], color=ORANGE) for layer in layers[1:] for u in layer], run_time=self.share(0.1))
        # "Three inputs and four hidden units make 21 weights, where linear regression has 4."
        self.wait(max(self.share(0.25) - self.time, 0.01))
        self.play(FadeIn(counts[0], shift=0.2 * LEFT), run_time=self.share(0.12))
        self.wait(max(self.share(0.48) - self.time, 0.01))
        self.play(FadeIn(counts[1], shift=0.2 * LEFT), run_time=self.share(0.1))
        # "Ten inputs and twenty units make 241."
        self.wait(max(self.share(0.68) - self.time, 0.01))
        self.play(FadeIn(counts[2], shift=0.2 * LEFT), run_time=self.share(0.12))
        self.finish()


class Scene14(KeyPointScene):
    number, point = 14, 1


# Training it (scenes 15–23) -----------------------------------------------------------------

class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Schematic: a smooth error curve and a ball stepping down it.
        f = lambda x: 0.22 * (x - 1.2) ** 2 + 0.5  # noqa: E731
        df = lambda x: 0.44 * (x - 1.2)  # noqa: E731
        axes, frame = chart([-5, 5, 1], [0, 8, 1], 9, 5, [], [], "A weight", "Error")
        frame.move_to([0, -0.3, 0])
        curve = axes.plot(f, x_range=[-4.6, 5], color=INK, stroke_width=5)
        xs = [-4.2, -2.3, -0.9, 0.1, 0.7]
        ball = Dot(axes.c2p(xs[0], f(xs[0])), radius=0.18, color=ORANGE).shift(0.18 * UP)

        def tangent(x):
            return Line(axes.c2p(x - 0.9, f(x) - 0.9 * df(x)), axes.c2p(x + 0.9, f(x) + 0.9 * df(x)),
                        color=BLUE, stroke_width=5)
        slope_name = label("Which way is downhill", 30, BLUE, weight=BOLD).next_to(axes.c2p(xs[0], f(xs[0])), RIGHT, 0.9)
        step_name = label("A small step", 30, ORANGE, weight=BOLD).move_to(axes.c2p(2.8, 6.5))
        # "A network learns its weights by gradient descent: find which way is downhill for every weight, ..."
        self.play(FadeIn(frame), Create(curve), FadeIn(ball), run_time=self.share(0.25))
        line = tangent(xs[0])
        self.play(Create(line), FadeIn(slope_name), run_time=self.share(0.2))
        # "... and take a small step."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeOut(slope_name), FadeIn(step_name), run_time=self.share(0.06))
        for x in xs[1:]:
            self.play(ball.animate.move_to(axes.c2p(x, f(x)) + 0.18 * UP), Transform(line, tangent(x)),
                      run_time=self.share(0.07))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        layers, edges, names, hidden_name, out_name = layer_layout()
        self.add(layers, edges, names, out_name)
        # The weight from temperature into the first hidden unit, as on the page's schematic.
        weight = [e for e in edges[0] if np.allclose(e.get_start(), layers[0][1][0].get_center(), atol=0.4)
                  and np.allclose(e.get_end(), layers[1][0][0].get_center(), atol=0.4)][0]
        path = VGroup(weight.copy(), edges[1][0].copy()).set_color(ORANGE).set_stroke(width=7)
        weight_name = label("A first-layer weight", 30, ORANGE, weight=BOLD).next_to(weight, UP, 0.5).shift(0.4 * LEFT)
        back_name = label("The error, passed back one layer at a time", 32, VERMILION, weight=BOLD
                          ).to_edge(DOWN, buff=0.4)
        slopes = label("Every weight gets its slope", 32, BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        # "A first-layer weight acts through everything after it."
        self.play(Create(path[0]), FadeIn(weight_name), run_time=self.share(0.12))
        self.play(Create(path[1]), Indicate(layers[2], color=ORANGE), run_time=self.share(0.15))
        # "Backpropagation passes the error back from the output, one layer at a time, ..."
        self.wait(max(self.share(0.3) - self.time, 0.01))
        back = [VGroup(*[Line(e.get_end(), e.get_start(), color=VERMILION, stroke_width=7) for e in group])
                for group in (edges[1], edges[0])]
        self.play(FadeIn(back_name), run_time=self.share(0.08))
        for group in back:
            self.play(ShowPassingFlash(group, time_width=0.6), run_time=self.share(0.14))
        # "... and gives every weight its slope."
        self.wait(max(self.share(0.75) - self.time, 0.01))
        self.play(FadeIn(slopes), edges.animate.set_color(BLUE), run_time=self.share(0.12))
        self.finish()


GRADIENT_NAMES = {"W1": "Weights into the hidden layer", "b1": "Hidden-layer constants",
                  "w2": "Weights into the output", "b2": "Output constant"}


class Scene17(VideoScene):
    number = 17

    def construct(self):
        check = self.data("gradient-check")
        n_weights = int(value(self, "forward-and-backward", "n_weights"))
        places = int(value(self, "forward-and-backward", "places"))
        head = label("Largest difference between backpropagation and nudging", 32, SUBDUED
                     ).to_edge(UP, buff=0.7)
        rows = VGroup()
        for i, r in check.iterrows():
            y = 1.5 - 0.95 * i
            rows.add(VGroup(label(GRADIENT_NAMES[r["group"]], 32).move_to([0.6, y, 0], aligned_edge=RIGHT),
                            label(f"{r['difference']:.1e}", 36, INK, weight=BOLD
                                  ).move_to([1.3, y, 0], aligned_edge=LEFT)))
        same = label(f"All {n_weights} slopes agree to {WORDS[places]} decimal places", 36, GREEN, weight=BOLD
                     ).to_edge(DOWN, buff=0.8)
        # "Nudging each weight by a tiny amount checks those slopes."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=self.share(0.45))
        # "All 21 agreed to ten decimal places."
        self.wait(max(self.share(0.55) - self.time, 0.01))
        self.play(FadeIn(same, shift=0.2 * UP), run_time=self.share(0.2))
        self.finish()


RATE_COLOURS = {0.01: SKY, 0.05: GREEN, 0.2: BLUE, 0.5: ORANGE, 2.0: VERMILION}


def rates_layout(scene):
    rates = scene.data("rates")
    linear = value(scene, "training-a-network", "linear_mse")
    names = {0.01: "0.01: crawls", 0.05: "0.05", 0.2: "0.2: goes lowest", 0.5: "0.5: bounces",
             2.0: "2: not a number"}
    top = np.log10(rates["step"].max())
    axes, frame = chart([0, top, 1], [0.5, 0.9, 0.1], 7.8, 4.8, [1, 10, 100, "1,000"],
                        [0.5, 0.6, 0.7, 0.8, 0.9], "Gradient-descent step (log scale)", "Training MSE",
                        x_at=[0, 1, 2, 3], x_fmt="{}", y_fmt="{:.1f}")
    frame.move_to([-2.4, -0.2, 0])
    line = DashedLine(axes.c2p(0, linear), axes.c2p(top, linear), color=GREY, stroke_width=3)
    line_name = label("Straight line", 26, SUBDUED).next_to(axes.c2p(0.05, linear), DOWN + RIGHT, 0.1)
    curves, legend = {}, {}
    head = label("Learning rate", 30, SUBDUED, weight=BOLD).move_to([2.2, 2.8, 0], aligned_edge=LEFT)
    for i, (rate, rows) in enumerate(rates.groupby("rate")):
        values = rows["mse"].to_numpy()
        keep = np.isfinite(values) & (values <= 0.9)
        steps = rows["step"].to_numpy()
        # The page clips its panel at 0.9; the 0.5 run's spikes and the 2 run leave it.
        curves[rate] = polyline(axes, np.log10(steps[keep]), np.clip(values[keep], 0.5, 0.9),
                                RATE_COLOURS[rate], 5) if keep.sum() > 1 else VGroup()
        legend[rate] = label(names[rate], 30, RATE_COLOURS[rate], weight=BOLD
                             ).move_to([2.2, 2.1 - 0.6 * i, 0], aligned_edge=LEFT)
    return axes, VGroup(frame, line, line_name), curves, legend, head


class Scene18(VideoScene):
    number = 18

    def construct(self):
        axes, frame, curves, legend, head = rates_layout(self)
        passes = int(value(self, "training-a-network", "passes_001"))
        linear = value(self, "training-a-network", "linear_mse")
        x = np.log10(passes)
        mark = DashedLine(axes.c2p(x, 0.5), axes.c2p(x, linear), color=SKY, stroke_width=3)
        mark_name = label(f"Step {passes:,}", 26, SKY, weight=BOLD).next_to(axes.c2p(x, 0.5), UP + LEFT, 0.12)
        # "The length of each step is the learning rate."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.25))
        # "At 0.01, the network takes 1,122 steps to beat a straight line."
        self.wait(max(self.share(0.35) - self.time, 0.01))
        self.play(Create(curves[0.01]), FadeIn(legend[0.01]), run_time=self.share(0.4))
        self.play(Create(mark), FadeIn(mark_name), run_time=self.share(0.12))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        axes, frame, curves, legend, head = rates_layout(self)
        self.add(frame, head, curves[0.01], legend[0.01])
        up = Arrow(axes.c2p(0.05, 0.62), axes.c2p(0.05, 0.93), buff=0, color=VERMILION, stroke_width=6)
        nan_at = int(value(self, "training-a-network", "nan_at"))
        warn = VGroup(label(f"At step {nan_at},", 30, VERMILION, weight=BOLD),
                      label("and no warning", 30, VERMILION, weight=BOLD)
                      ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(legend[2.0], DOWN, 0.35
                                                                             ).align_to(legend[2.0], LEFT)
        # "At 0.2 it goes lowest."
        self.play(Create(curves[0.05]), Create(curves[0.2]), FadeIn(legend[0.05]), FadeIn(legend[0.2]),
                  run_time=self.share(0.14))
        # "At 0.5 it is quicker, but bounces around the valley floor."
        self.play(Create(curves[0.5]), FadeIn(legend[0.5]), run_time=self.share(0.22))
        # "At 2, the error passes 1,000 by step 6, and becomes "not a number" at step 147, ..."
        self.wait(max(self.share(0.42) - self.time, 0.01))
        self.play(GrowArrow(up), FadeIn(legend[2.0]), run_time=self.share(0.15))
        # "... with no warning at all."
        self.wait(max(self.share(0.82) - self.time, 0.01))
        self.play(FadeIn(warn, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def stopping_layout(scene):
    runs = scene.data("early-stopping")
    top = np.log10(len(runs))
    axes, frame = chart([0, top, 1], [0.5, 1.1, 0.1], 8.6, 4.8, [1, 10, 100, "1,000", "8,000"],
                        [0.5, 0.7, 0.9, 1.1], "Gradient-descent step (log scale)", "MSE",
                        x_at=[0, 1, 2, 3, top], x_fmt="{}", y_fmt="{:.1f}")
    frame.move_to([-1.6, -0.2, 0])
    # Every step would be 8,000 corners; a few hundred evenly spaced on the log axis suffice.
    keep = np.unique(np.round(np.logspace(0, top, 400)).astype(int)) - 1
    rows = runs.iloc[keep]
    xs = np.log10(rows["step"])
    training = polyline(axes, xs, rows["training"].clip(upper=1.1), BLUE, 6)
    validation = polyline(axes, xs, rows["validation"].clip(upper=1.1), ORANGE, 6)
    names = (label("Training", 30, BLUE, weight=BOLD).next_to(training.get_end(), RIGHT + DOWN, 0.1),
             label("Validation", 30, ORANGE, weight=BOLD).next_to(validation.get_end(), RIGHT + UP, 0.1))
    head = label("A 40-unit network, 8,000 steps", 32, SUBDUED).to_edge(UP, buff=0.4)
    return axes, runs, VGroup(frame, head), training, validation, names


class Scene20(VideoScene):
    number = 20

    def construct(self):
        axes, runs, frame, training, validation, names = stopping_layout(self)
        # "Now give a network forty hidden units and 8,000 steps."
        self.play(FadeIn(frame), run_time=self.share(0.3))
        # "Its training error falls the whole way."
        self.wait(max(self.share(0.45) - self.time, 0.01))
        self.play(Create(training), run_time=self.share(0.4))
        self.play(FadeIn(names[0]), run_time=self.share(0.1))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        axes, runs, frame, training, validation, names = stopping_layout(self)
        self.add(frame, training, names[0])
        best_step = int(value(self, "training-a-network", "best_step"))
        worse_pct = int(value(self, "training-a-network", "worse_pct"))
        n_valid = int(value(self, "training-a-network", "n_valid"))
        best = runs.iloc[best_step - 1]
        x = np.log10(best_step)
        marker = DashedLine(axes.c2p(x, 0.5), axes.c2p(x, 1.05), color=SUBDUED, stroke_width=3)
        dot = Dot(axes.c2p(x, best["validation"]), radius=0.11, color=ORANGE)
        held = label(f"{n_valid} stations held back", 28, ORANGE).next_to(names[1], UP, 0.12
                                                                       ).align_to(names[1], LEFT)
        best_name = label(f"Lowest: step {best_step:,}", 30, ORANGE, weight=BOLD
                          ).next_to(axes.c2p(x, 1.0), LEFT, 0.15)
        worse_name = label(f"{worse_pct}% worse by the end", 30, ORANGE, weight=BOLD
                           ).next_to(held, UP, 0.25).align_to(names[1], LEFT)
        keep = VGroup(label("Early stopping:", 32, INK, weight=BOLD), label("keep these weights", 32, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(axes.c2p(x, 0.98), RIGHT, 0.2)
        # "On 200 stations held back for validation, ..."
        self.play(Create(validation), FadeIn(names[1]), FadeIn(held), run_time=self.share(0.2))
        # "... the error is lowest at step 1,937, ..."
        self.play(Create(marker), FadeIn(dot, scale=2), FadeIn(best_name), run_time=self.share(0.12))
        # "... and 4% worse by the end."
        self.wait(max(self.share(0.42) - self.time, 0.01))
        self.play(FadeIn(worse_name), run_time=self.share(0.1))
        # "Keeping the weights from that step is early stopping."
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(FadeIn(keep, shift=0.2 * DOWN), Indicate(dot, color=ORANGE, scale_factor=2), run_time=self.share(0.2))
        self.finish()


def seeds_layout(scene):
    seeds = scene.data("seeds")
    values = seeds["validation"].to_numpy()
    averaged = value(scene, "training-a-network", "averaged_mse")
    lo = np.floor(min(values.min(), averaged) * 100 - 1) / 100
    hi = np.ceil(values.max() * 100 + 1) / 100
    ticks = np.round(np.arange(lo, hi + 1e-9, 0.02), 2)
    axis, to_x = number_line(lo, hi, -5.2, 5.2, -0.8, ticks, 2)
    name = label("Validation MSE, one dot per seed", 28, SUBDUED).next_to(axis, DOWN, 0.15).align_to(axis, RIGHT)
    dots = VGroup(*[Dot([to_x(v), -0.8 + 0.3, 0], radius=0.16, color=BLUE, fill_opacity=0.85) for v in values])
    head = label("The same network ten times: only the seed differs", 32, SUBDUED).to_edge(UP, buff=0.8)
    return values, averaged, VGroup(axis, name), to_x, dots, head


class Scene22(VideoScene):
    number = 22

    def construct(self):
        values, averaged, axis, to_x, dots, head = seeds_layout(self)
        # "Then train ten networks that differ only in their random starting weights."
        self.play(FadeIn(head), FadeIn(axis), run_time=self.share(0.2))
        self.play(LaggedStart(*[FadeIn(d, shift=1.5 * DOWN) for d in dots], lag_ratio=0.3), run_time=self.share(0.6))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        values, averaged, axis, to_x, dots, head = seeds_layout(self)
        self.add(head, axis, dots)
        n_beaten = int(value(self, "training-a-network", "n_beaten"))
        span = Line([to_x(values.min()), 0.2, 0], [to_x(values.max()), 0.2, 0], color=BLUE, stroke_width=5)
        ends = VGroup(*[Line([x, 0.05, 0], [x, 0.35, 0], color=BLUE, stroke_width=5)
                        for x in (to_x(values.min()), to_x(values.max()))])
        spread = values.max() - values.min()
        span_name = label(f"Spread: {spread:.3f}", 34, BLUE, weight=BOLD).next_to(span, UP, 0.2)
        mean_dot = Dot([to_x(averaged), -0.8 + 0.3, 0], radius=0.2, color=GREEN)
        mean_name = VGroup(label("Average of all ten:", 30, GREEN, weight=BOLD),
                           label(f"better than {WORDS.get(n_beaten, n_beaten)} of them", 30, GREEN, weight=BOLD)
                           ).arrange(DOWN, buff=0.08).move_to([to_x(averaged), -2.6, 0])
        mean_line = Line(mean_dot.get_bottom(), mean_name.get_top() + 0.1 * UP, color=GREEN, stroke_width=3)
        # "Their validation error spans 0.055, from the seed alone."
        self.play(Create(span), FadeIn(ends), FadeIn(span_name), run_time=self.share(0.3))
        # "Averaging all ten does better than seven of them."
        self.wait(max(self.share(0.5) - self.time, 0.01))
        self.play(FadeIn(mean_dot, scale=2), Create(mean_line), FadeIn(mean_name), run_time=self.share(0.2))
        self.finish()


class Scene24(KeyPointScene):
    number, point = 24, 2


# When a network pays off (scenes 25–37) ------------------------------------------------------

CURVE_COLOURS = {"Random forest": GREEN, "Linear regression": SUBDUED, "Neural network": VERMILION}
CURVE_NAMES = {"Random forest": "Random forest", "Linear regression": "Linear regression",
               "Neural network": "Network, 8 hidden units"}
Y_TOP = 9.0


def curves_layout(scene):
    curves = scene.data("learning-curves")
    baseline = value(scene, "how-much-data", "baseline")
    sizes = sorted(curves["n"].unique())
    lo, hi = np.log10(sizes[0]), np.log10(sizes[-1])
    axes, frame = chart([lo, hi, 0.5], [3.5, Y_TOP, 1], 7.0, 5.0, sizes, [4, 5, 6, 7, 8, 9],
                        "Training stations (log scale)", "RMSE on test sites (individuals)",
                        x_at=np.log10(sizes))
    frame.move_to([-2.6, -0.2, 0])
    base = DashedLine(axes.c2p(lo, baseline), axes.c2p(hi, baseline), color=GREY, stroke_width=4)
    right = axes.c2p(hi, 0)[0] + 0.3
    base_name = label(f"Predict the mean: {baseline:.2f}", 26, SUBDUED, weight=BOLD
                      ).move_to([right, base.get_y(), 0], aligned_edge=LEFT)
    lines, ribbons, legend = {}, {}, {}
    for i, model in enumerate(["Random forest", "Linear regression", "Neural network"]):
        rows = curves[curves["model"] == model].sort_values("n")
        xs = np.log10(rows["n"]).to_numpy()
        colour = CURVE_COLOURS[model]
        lines[model] = VGroup(polyline(axes, xs, rows["rmse"].clip(upper=Y_TOP), colour, 6),
                              *[Dot(axes.c2p(x, min(y, Y_TOP)), radius=0.07, color=colour)
                                for x, y in zip(xs, rows["rmse"])])
        upper = rows["upper"].clip(upper=Y_TOP).to_numpy()
        lower = rows["lower"].clip(upper=Y_TOP).to_numpy()
        ribbons[model] = Polygon(*[axes.c2p(x, y) for x, y in zip(xs, upper)],
                                 *[axes.c2p(x, y) for x, y in zip(xs[::-1], lower[::-1])],
                                 stroke_width=0, fill_color=colour, fill_opacity=0.15)
        legend[model] = label(CURVE_NAMES[model], 28, colour, weight=BOLD
                              ).move_to([right, 2.6 - 0.5 * i, 0], aligned_edge=LEFT)
    return dict(axes=axes, frame=frame, base=VGroup(base, base_name), lines=lines, ribbons=ribbons,
                legend=legend, curves=curves, right=right)


class Scene25(VideoScene):
    number = 25

    def construct(self):
        c = curves_layout(self)
        # "Back to the survey. Linear regression, a random forest and a network with eight hidden units ..."
        self.play(FadeIn(c["frame"]), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(c["legend"][m]) for m in c["legend"]], lag_ratio=0.4), run_time=self.share(0.3))
        # "Predicting the mean scores 4.72."
        self.wait(max(self.share(0.78) - self.time, 0.01))
        self.play(Create(c["base"][0]), FadeIn(c["base"][1]), run_time=self.share(0.15))
        self.finish()


def end_values(c):
    curves = c["curves"]
    at = curves[curves["n"] == curves["n"].max()].set_index("model")["rmse"]
    return {"Random forest": label(f"{at['Random forest']:.2f}", 26, GREEN, weight=BOLD
                                   ).next_to(c["lines"]["Random forest"][-1], DOWN + LEFT, 0.1),
            "Neural network": label(f"{at['Neural network']:.2f}", 26, VERMILION, weight=BOLD
                                    ).next_to(c["lines"]["Neural network"][-1], UP, 0.15)}


class Scene26(VideoScene):
    number = 26

    def construct(self):
        c = curves_layout(self)
        self.add(c["frame"], c["base"], *c["legend"].values())
        ends = end_values(c)
        # "The forest leads at every size, ending at 4.20."
        self.play(FadeIn(c["ribbons"]["Random forest"]), Create(c["lines"]["Random forest"]), run_time=self.share(0.2))
        self.play(FadeIn(ends["Random forest"]), FadeIn(c["ribbons"]["Linear regression"]),
                  Create(c["lines"]["Linear regression"]), run_time=self.share(0.15))
        # "The network varies most from draw to draw, and ends at 4.94."
        self.wait(max(self.share(0.42) - self.time, 0.01))
        self.play(FadeIn(c["ribbons"]["Neural network"]), Create(c["lines"]["Neural network"]), run_time=self.share(0.3))
        self.play(FadeIn(ends["Neural network"]), run_time=self.share(0.1))
        self.finish()


class Scene27(VideoScene):
    number = 27

    def construct(self):
        c = curves_layout(self)
        self.add(c["frame"], c["base"], *c["legend"].values(), *c["ribbons"].values(), *c["lines"].values(),
                 *end_values(c).values())
        units = int(value(self, "how-much-data", "hidden_units"))
        penalty = value(self, "how-much-data", "penalty")
        note = VGroup(label("Cross-validation chooses:", 28, BLUE, weight=BOLD),
                      label(f"{units} hidden unit, penalty {penalty:g}", 28, BLUE, weight=BOLD),
                      label("almost a straight line", 28, BLUE, weight=BOLD)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([c["right"], 0.4, 0], aligned_edge=LEFT)
        # "Allowed to choose, cross-validation shrinks the network to one hidden unit with the largest penalty: ..."
        self.play(FadeIn(note[:2], shift=0.2 * LEFT), run_time=self.share(0.25))
        # "... almost a straight line."
        self.wait(max(self.share(0.75) - self.time, 0.01))
        self.play(FadeIn(note[2]), Indicate(c["lines"]["Linear regression"], color=SUBDUED, scale_factor=1.0),
                  run_time=self.share(0.2))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        # Schematic: a smooth average, noisy counts scattered around it, then the counts removed.
        axes, frame = chart([0, 10, 1], [0, 10, 1], 8, 4.6, [], [], "An input", "")
        frame.move_to([0, -0.4, 0])
        f = lambda x: 2 + 6 * np.exp(-((x - 5) ** 2) / 6)  # noqa: E731
        expected = axes.plot(f, x_range=[0, 10], color=BLUE, stroke_width=7)
        rng = np.random.default_rng(34)
        xs = rng.uniform(0.3, 9.7, 60)
        counts = VGroup(*[Dot(axes.c2p(x, np.clip(f(x) + rng.normal(0, 1.6), 0.2, 9.8)), radius=0.08, color=GREY)
                          for x in xs])
        counts_name = label("Observed counts", 30, SUBDUED, weight=BOLD).move_to(axes.c2p(8.6, 9.2))
        expected_name = label("Expected counts", 30, BLUE, weight=BOLD).move_to(axes.c2p(1.6, 8.6))
        check = label("A check, not data", 36, VERMILION, weight=BOLD).to_edge(UP, buff=0.5)
        # "But this survey is simulated, so each station's expected count is known: ..."
        self.play(FadeIn(frame), FadeIn(counts, lag_ratio=0.02), FadeIn(counts_name), run_time=self.share(0.2))
        # "... the average its count was drawn from."
        self.wait(max(self.share(0.3) - self.time, 0.01))
        self.play(Create(expected), FadeIn(expected_name), run_time=self.share(0.2))
        # "A real survey has no such column. Here it is only a check."
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(counts.animate.set_opacity(0.25), FadeIn(check, shift=0.2 * DOWN), run_time=self.share(0.15))
        self.finish()


class Scene29(VideoScene):
    number = 29

    def construct(self):
        expected = self.data("expected-curves")
        full = int(value(self, "how-much-data", "n_train"))
        at = expected[expected["n"] == full].set_index("model")["rmse"]
        order = ["Neural network", "Random forest", "Linear regression"]
        head = label(f"RMSE against the expected counts, {full} stations (individuals)", 30, SUBDUED
                     ).to_edge(UP, buff=0.8)
        rows = hbar_rows(["Network", "Random forest", "Linear regression"], [at[m] for m in order],
                         [BLUE, GREEN, GREY], 2.6, x0=-0.6, top=1.2, step=1.3, digits=2)
        best = label("Learned the response best", 36, BLUE, weight=BOLD).to_edge(DOWN, buff=0.7)
        # "Scored against the expected counts, the order turns round."
        self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows], run_time=self.share(0.15))
        # "The network scores 1.54, the forest 1.63, and linear regression 2.12."
        self.wait(max(self.share(0.22) - self.time, 0.01))
        for r in rows:
            self.play(GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=self.share(0.1))
        # "The network had learned the response best; the noise in the counts hid it."
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(FadeIn(best, shift=0.2 * UP), Indicate(rows[0][1], color=BLUE, scale_factor=1.05),
                  run_time=self.share(0.2))
        self.finish()


class Scene30(VideoScene):
    number = 30

    def construct(self):
        rows = label("Short of rows", 60, INK, weight=BOLD)
        signal = label("Short of signal", 60, INK, weight=BOLD)
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


PANEL_MODELS = ["Logistic regression", "Decision tree", "Random forest", "Neural network"]
PANEL_NAMES = {"Logistic regression": "Logistic regression", "Decision tree": "Decision tree",
               "Random forest": "Random forest", "Neural network": "Network"}
CORE_RGB, OUTSIDE_RGB = (0xF6, 0xD2, 0xA8), (0xEE, 0xF1, 0xF3)


def water_ranges(scene):
    train = scene.data("water-train")
    return (2, 16), (train["salinity_psu"].min(), train["salinity_psu"].max())


def water_axes(scene, width, height, centre, ticks=True):
    t_range, s_range = water_ranges(scene)
    if ticks:
        s_ticks = list(range(int(np.ceil(s_range[0])), int(np.floor(s_range[1])) + 1))
        axes, frame = chart([*t_range, 2], [*s_range, 0.5], width, height, [4, 8, 12, 16], s_ticks,
                            "Temperature (°C)", "Salinity (PSU)")
    else:
        axes = plain_axes([*t_range, 2], [*s_range, 0.5], width, height)
        frame = VGroup(axes)
    frame.move_to(centre)
    return axes, frame


def class_image(scene, model, width, height):
    """A model's predicted class over the plane: core shaded orange, outside pale grey."""
    plane = scene.data("water-plane")
    rows = plane[plane["model"] == model]
    grid = rows.pivot(index="salinity_psu", columns="temperature_c", values="core").sort_index(ascending=False)
    core = grid.to_numpy().astype(bool)
    rgb = np.where(core[..., None], np.array(CORE_RGB, dtype=np.uint8), np.array(OUTSIDE_RGB, dtype=np.uint8))
    image = ImageMobject(rgb.astype(np.uint8))
    image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    image.stretch_to_fit_width(width).stretch_to_fit_height(height)
    return image


def stations(scene, axes, radius=0.07):
    train = scene.data("water-train")
    dots = VGroup()
    for t, s, mass in zip(train["temperature_c"], train["salinity_psu"], train["water_mass"]):
        if mass == "core":
            dots.add(Dot(axes.c2p(t, s), radius=radius, color=ORANGE if radius > 0.05 else INK))
        else:
            dots.add(Cross(scale_factor=radius * 0.9, stroke_color=GREY, stroke_width=2.5).move_to(axes.c2p(t, s)))
    return dots


class Scene31(VideoScene):
    number = 31

    def construct(self):
        axes, frame = water_axes(self, 8.0, 5.4, [-1.8, -0.1, 0])
        dots = stations(self, axes)
        core = VGroup(*[d for d in dots if isinstance(d, Dot)])
        core_name = label("Water-mass core", 32, ORANGE, weight=BOLD).move_to([3.4, 1.4, 0], aligned_edge=LEFT)
        legend = VGroup(VGroup(Dot(radius=0.08, color=ORANGE), label("Core", 26)).arrange(RIGHT, buff=0.15),
                        VGroup(Cross(scale_factor=0.06, stroke_color=GREY, stroke_width=2.5), label("Outside", 26)
                               ).arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.2, aligned_edge=LEFT
                                                                    ).move_to([3.4, 0.4, 0], aligned_edge=LEFT)
        n = len(self.data("water-train"))
        tag = VGroup(label("Simulated water mass", 28, SUBDUED), label(f"{n} stations", 28, SUBDUED)
                     ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([3.4, 2.5, 0], aligned_edge=LEFT)
        # "Now a simulated water mass."
        self.play(FadeIn(frame), FadeIn(tag), run_time=self.share(0.2))
        # "Its core is a diagonal band on a temperature–salinity diagram, ..."
        self.play(FadeIn(dots, lag_ratio=0.01), FadeIn(legend), run_time=self.share(0.3))
        self.play(Indicate(core, color=ORANGE, scale_factor=1.3), FadeIn(core_name), run_time=self.share(0.2))
        # "... and 200 stations train the models."
        self.finish()


PANEL_W, PANEL_H = 5.2, 2.7
PANEL_CENTRES = [[-3.2, 1.4, 0], [3.2, 1.4, 0], [-3.2, -2.3, 0], [3.2, -2.3, 0]]


def boundary_panels(scene):
    scores = scene.data("water-auc").set_index("model")
    n_weights = int(value(scene, "when-to-use-one", "n_weights"))
    names = dict(PANEL_NAMES, **{"Neural network": f"Network, {n_weights} weights"})
    panels = {}
    for model, centre in zip(PANEL_MODELS, PANEL_CENTRES):
        axes, frame = water_axes(scene, PANEL_W, PANEL_H, centre, ticks=False)
        image = class_image(scene, model, PANEL_W, PANEL_H).move_to(axes.get_center())
        dots = stations(scene, axes, radius=0.035)
        name = label(names[model], 26, INK, weight=BOLD).next_to(axes, UP, 0.12).align_to(axes, LEFT)
        auc = label(f"ROC AUC {scores.loc[model, 'auc']:.3f}", 26, BLUE, weight=BOLD
                    ).next_to(name, RIGHT, 0.4)
        panels[model] = (image, dots, name, auc, axes)
    return panels


def show_panel(panel):
    image, dots, name, auc, _ = panel
    return [FadeIn(image), FadeIn(dots), FadeIn(name)]


class Scene32(VideoScene):
    number = 32

    def construct(self):
        panels = boundary_panels(self)
        # "Scored by ROC AUC, where one is a perfect ranking, logistic regression draws one straight line and reaches 0.715."
        self.play(*show_panel(panels["Logistic regression"]), run_time=self.share(0.15))
        self.wait(max(self.share(0.3) - self.time, 0.01))
        self.play(FadeIn(panels["Logistic regression"][3]), run_time=self.share(0.1))
        # "A tree cuts one input at a time: 0.827."
        self.wait(max(self.share(0.48) - self.time, 0.01))
        self.play(*show_panel(panels["Decision tree"]), FadeIn(panels["Decision tree"][3]), run_time=self.share(0.18))
        # "A forest of 500 trees: 0.926."
        self.wait(max(self.share(0.75) - self.time, 0.01))
        self.play(*show_panel(panels["Random forest"]), FadeIn(panels["Random forest"][3]), run_time=self.share(0.18))
        self.finish()


class Scene33(VideoScene):
    number = 33

    def construct(self):
        panels = boundary_panels(self)
        for model in PANEL_MODELS[:3]:
            self.add(*panels[model][:4])
        net = panels["Neural network"]
        # "A network with two hidden units, nine weights in all, ..."
        self.play(*show_panel(net), run_time=self.share(0.4))
        # "... reaches 0.999."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeIn(net[3], scale=1.3), run_time=self.share(0.2))
        self.finish()


class Scene34(VideoScene):
    number = 34

    def construct(self):
        axes, frame = water_axes(self, 7.8, 5.4, [-2.2, -0.1, 0])
        t_range, s_range = water_ranges(self)
        image = class_image(self, "Neural network", 7.8, 5.4).move_to(axes.get_center())
        dots = stations(self, axes, radius=0.04)
        units = self.data("water-units")
        # Each hidden unit switches where its weighted sum is zero: a straight line on the
        # temperature–salinity plane, drawn back in measured units.
        lines = VGroup()
        for _, u in units.iterrows():
            def salinity(t):
                z_t = (t - u["t_mean"]) / u["t_sd"]
                return u["s_mean"] + u["s_sd"] * (-(u["bias"] + u["t"] * z_t) / u["s"])
            ts = np.linspace(*t_range, 200)
            ss = np.array([salinity(t) for t in ts])
            keep = (ss >= s_range[0]) & (ss <= s_range[1])
            if keep.sum() >= 2:
                lines.add(polyline(axes, ts[keep], ss[keep], BLUE, 7))
        name = VGroup(label("Each hidden unit:", 30, INK, weight=BOLD),
                      label("a bend along", 30, INK, weight=BOLD), label("a tilted line", 30, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([2.4, 1.2, 0], aligned_edge=LEFT)
        edges = VGroup(label("Two of them:", 30, BLUE, weight=BOLD), label("the band's edges", 30, BLUE, weight=BOLD)
                       ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([2.4, -0.8, 0], aligned_edge=LEFT)
        self.add(frame, image, dots)
        # "Each hidden unit bends along a tilted line."
        self.play(FadeIn(name), LaggedStart(*[Create(line) for line in lines], lag_ratio=0.4), run_time=self.share(0.4))
        # "Two of them, one at each edge, fence in the band."
        self.wait(max(self.share(0.5) - self.time, 0.01))
        self.play(FadeIn(edges), *[Indicate(line, color=BLUE, scale_factor=1.0) for line in lines],
                  run_time=self.share(0.3))
        self.finish()


class Scene35(VideoScene):
    number = 35

    def construct(self):
        sizes = self.data("water-sizes")
        n_test = int(value(self, "when-to-use-one", "n_test"))
        cols = {"Neural network": (-1.8, "Network", BLUE), "Random forest": (1.4, "Random forest", GREEN),
                "Logistic regression": (5.0, "Logistic regression", SUBDUED)}
        head = label(f"ROC AUC on the {n_test:,} test stations", 32, SUBDUED).to_edge(UP, buff=0.8)
        heads = VGroup(*[label(name, 30, colour, weight=BOLD).move_to([x, 2.0, 0])
                         for x, name, colour in cols.values()])
        cells, names = {}, VGroup()
        ns = sorted(sizes["n"].unique())
        for i, n in enumerate(ns):
            y = 0.9 - 1.1 * i
            names.add(label(f"{n:,} stations", 32).move_to([-3.3, y, 0], aligned_edge=RIGHT))
            for m, (x, _, _) in cols.items():
                v = sizes[(sizes["n"] == n) & (sizes["model"] == m)]["auc"].item()
                cells[(n, m)] = label(f"{v:.3f}", 40, INK, weight=BOLD).move_to([x, y, 0])
        # "With only 100 stations, the network reaches 0.997."
        self.play(FadeIn(head), FadeIn(heads), FadeIn(names), run_time=self.share(0.12))
        self.play(*[FadeIn(cells[(n, "Neural network")]) for n in ns], run_time=self.share(0.12))
        self.play(Circumscribe(cells[(ns[0], "Neural network")], color=BLUE), run_time=self.share(0.15))
        # "The forest needs 1,600 to come close, ..."
        self.play(*[FadeIn(cells[(n, "Random forest")]) for n in ns], run_time=self.share(0.12))
        self.play(Circumscribe(cells[(ns[-1], "Random forest")], color=GREEN), run_time=self.share(0.15))
        # "... and logistic regression stays near 0.72."
        self.wait(max(self.share(0.75) - self.time, 0.01))
        self.play(*[FadeIn(cells[(n, "Logistic regression")]) for n in ns], run_time=self.share(0.15))
        self.finish()


class Scene36(VideoScene):
    number = 36

    def construct(self):
        # The combination the page names, added as a column; the score is the page's.
        named_auc = value(self, "when-to-use-one", "named_auc")
        rng = np.random.default_rng(42)

        def column(name, colour, n=6):
            cells = VGroup(*[Rectangle(width=2.6, height=0.45, stroke_color=GRID, stroke_width=2, fill_color=colour,
                                       fill_opacity=float(rng.uniform(0.1, 0.5))) for _ in range(n)]
                           ).arrange(DOWN, buff=0)
            return VGroup(label(name, 28, INK, weight=BOLD).next_to(cells, UP, 0.2), cells)
        t = column("Temperature", BLUE)
        s = column("Salinity", BLUE)
        combo = column("Salinity − 0.16 × temperature", GREEN)
        combo[0].scale(0.9)
        VGroup(t, s).arrange(RIGHT, buff=0.1).move_to([-3.4, 0.8, 0])
        combo.next_to(VGroup(t, s), RIGHT, 0.6)
        named = label(f"Named: logistic regression reaches {named_auc:.3f}", 32, GREEN, weight=BOLD
                      ).move_to([0, -1.9, 0])
        unnamed = label("Not named: a network finds it", 32, BLUE, weight=BOLD).next_to(named, DOWN, 0.4)
        # "If you can name the combination, add it as a column: ..."
        self.play(FadeIn(t), FadeIn(s), run_time=self.share(0.12))
        self.play(FadeIn(combo, shift=0.5 * LEFT), run_time=self.share(0.2))
        # "... logistic regression then reaches 1.000."
        self.wait(max(self.share(0.36) - self.time, 0.01))
        self.play(FadeIn(named), run_time=self.share(0.12))
        # "A network finds the combinations nobody has named."
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(FadeIn(unnamed, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene37(VideoScene):
    number = 37

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
        pixel_name = label("Pixels", 32, SUBDUED, weight=BOLD).next_to(pixels, UP, 0.3)
        arrow1 = Arrow([-2.2, -0.3, 0], [-0.6, -0.3, 0], color=INK, stroke_width=5)
        edge = Line([0.2, -1.1, 0], [0.2, 0.5, 0], color=ORANGE, stroke_width=10)
        edge_name = label("An edge", 32, ORANGE, weight=BOLD).next_to(edge, UP, 0.3)
        arrow2 = Arrow([1.0, -0.3, 0], [2.6, -0.3, 0], color=INK, stroke_width=5)
        body = Ellipse(width=2.4, height=1.2, color=BLUE, stroke_width=8).move_to([4.4, -0.3, 0])
        tail = Polygon([5.6, -0.3, 0], [6.4, 0.2, 0], [6.4, -0.8, 0], color=BLUE, stroke_width=8)
        shape_name = label("A shape", 32, BLUE, weight=BOLD).next_to(body, UP, 0.5)
        nobody = label("Nobody can list them all", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.7)
        # "That is why networks lead on images and sound."
        self.play(FadeIn(pixels, lag_ratio=0.01), FadeIn(pixel_name), run_time=self.share(0.2))
        # "An edge is a combination of pixels, ..."
        self.play(Create(patch), GrowArrow(arrow1), FadeIn(edge), FadeIn(edge_name), run_time=self.share(0.2))
        self.play(GrowArrow(arrow2), Create(body), Create(tail), FadeIn(shape_name), run_time=self.share(0.2))
        # "... and nobody can list them all."
        self.wait(max(self.share(0.75) - self.time, 0.01))
        self.play(FadeIn(nobody, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene38(KeyPointScene):
    number, point = 38, 3


# Quiz (scenes 39–40) -------------------------------------------------------------------------

class Scene39(QuizScene):
    number = 39
    question = ("A network has ten hidden layers,", "each of a hundred units,", "and every activation is the identity.",
                "What shapes can it fit?")


class Scene40(VideoScene):
    number = 40

    def construct(self):
        layers, edges = deep_stack(hidden_layers=10, units=5, width=11.0, height=3.8, radius=0.16)
        answer = label("Only a straight line", 52, BLUE, weight=BOLD).to_edge(UP, buff=0.6)
        result = one_line([0, -0.4, 0])
        why = VGroup(label("A weighted sum of weighted sums", 34, INK, weight=BOLD),
                     label("is still a weighted sum", 34, INK, weight=BOLD)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        # "Only a straight line."
        self.play(FadeIn(answer), FadeIn(layers), Create(edges), run_time=self.share(0.25))
        self.play(ReplacementTransform(VGroup(layers, edges), result), run_time=self.share(0.25))
        # "A weighted sum of weighted sums is still a weighted sum."
        self.play(FadeIn(why, shift=0.2 * UP), run_time=self.share(0.15))
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
