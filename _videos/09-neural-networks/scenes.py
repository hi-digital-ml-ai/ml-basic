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


PROMISES = ["Build curves from simple bends",
            "Stop training at the right step",
            "Let a network find combinations"]
ANSWERS = ["Each neuron: a weighted sum\nwith a bend; the bends\nadd up to curves",
           "Watch the validation error;\nkeep the weights\nfrom its lowest point",
           "It pays off when the answer\nhangs on a combination\nnobody can name"]
RECAP = PROMISES


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("building curves", "stopping training", "and letting"))


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


def value(scene, page, name):
    """One number from a page's "<page>-numbers" table."""
    table = scene.data(f"{page}-numbers").set_index("name")["value"]
    return table[name]


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def polyline(axes, xs, ys, colour, width=6):
    points = [axes.c2p(x, y) for x, y in zip(xs, ys)]
    return VMobject(color=colour, stroke_width=width).set_points_as_corners(points)


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name,
          x_fmt="{:g}", y_fmt="{:g}", size=24, x_at=None):
    """Axes with tick labels and names, in the series style; returns the axes and all of it.

    `x_at` places the x tick labels at other positions than their values (a log axis).
    """
    axes = plain_axes(x_range, y_range, x_length, y_length)
    at_x = x_at if x_at is not None else x_ticks
    tx = VGroup(*[label(x_fmt.format(v), size, SUBDUED).next_to(axes.c2p(a, y_range[0]), DOWN, 0.15)
                  for v, a in zip(x_ticks, at_x)])
    ty = VGroup(*[label(y_fmt.format(v), size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15)
                  for v in y_ticks])
    xn = label(x_name, 26, SUBDUED).next_to(tx if len(tx) else axes, DOWN, 0.2)
    yn = label(y_name, 26, SUBDUED).rotate(PI / 2).next_to(ty if len(ty) else axes, LEFT, 0.2) \
        if y_name else VGroup()
    return axes, VGroup(axes, tx, ty, xn, yn)


def lines_of(text, size=32, colour=INK, weight=NORMAL, buff=0.12):
    return VGroup(*[label(t, size, colour, weight=weight) for t in text.split("\n")]
                  ).arrange(DOWN, buff=buff, aligned_edge=LEFT)


def s_curve(axes, colour=ORANGE, width=7):
    return axes.plot(lambda z: 1 / (1 + np.exp(-z)), x_range=[-5, 5], color=colour, stroke_width=width)


# Drawn networks ----------------------------------------------------------------------------

def bend_glyph(colour=ORANGE, width=0.5, straight=False):
    """A tiny activation drawn inside a neuron: an S-curve, or a straight line for none."""
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


# Build curves from simple bends (scenes 2–7) ------------------------------------------------

INPUT_NAMES = ["Depth", "Temperature", "Chlorophyll"]
NEURON_Y = -0.3


def neuron_layout():
    """Schematic: one neuron, its three inputs and weights, its constant and its output."""
    ys = [NEURON_Y + 1.7, NEURON_Y, NEURON_Y - 1.7]
    dots = VGroup(*[Circle(0.2, color=INK, stroke_width=3).move_to([-3.6, y, 0]) for y in ys])
    names = VGroup(*[label(n, 32).next_to(d, LEFT, 0.25) for n, d in zip(INPUT_NAMES, dots)])
    body = Circle(1.0, color=INK, stroke_width=5, fill_color=BACKGROUND, fill_opacity=1).move_to([1.2, NEURON_Y, 0])
    arrows = VGroup(*[Arrow(d.get_right(), body.get_center(), buff=1.0, color=BLUE, stroke_width=5)
                      for d in dots])
    weights = VGroup(*[label(f"× w{i}", 30, BLUE, weight=BOLD).move_to(a.point_from_proportion(0.45) + 0.35 * UP)
                       for i, a in enumerate(arrows, 1)])
    plus = label("add up", 30, BLUE, weight=BOLD).move_to(body)
    constant = label("+ a constant", 30, GREEN, weight=BOLD).next_to(body, DOWN, 0.3)
    out = Arrow(body.get_right(), body.get_right() + 2.0 * RIGHT, buff=0.1, color=INK, stroke_width=5)
    out_name = label("Output", 30).next_to(out, RIGHT, 0.2)
    head = label("A weighted sum", 40, BLUE, weight=BOLD).to_edge(UP, buff=0.6)
    return dict(dots=dots, names=names, body=body, arrows=arrows, weights=weights, plus=plus,
                constant=constant, out=out, out_name=out_name, head=head)


class Scene02(VideoScene):
    number = 2

    def construct(self):
        n = neuron_layout()
        cue(self, "called neurons")
        self.play(FadeIn(n["body"]), run_time=self.share(0.06))
        cue(self, "such as the depth")
        self.play(FadeIn(n["dots"]), LaggedStart(*[FadeIn(t, shift=0.2 * RIGHT) for t in n["names"]], lag_ratio=0.35),
                  run_time=self.share(0.14))
        cue(self, "It multiplies")
        self.play(LaggedStart(*[GrowArrow(a) for a in n["arrows"]], lag_ratio=0.3),
                  LaggedStart(*[FadeIn(w) for w in n["weights"]], lag_ratio=0.3), run_time=self.share(0.12))
        cue(self, "and adds them")
        self.play(FadeIn(n["plus"]), FadeIn(n["constant"], shift=0.2 * UP), run_time=self.share(0.08))
        cue(self, "That is a weighted")
        self.play(FadeIn(n["head"], shift=0.2 * DOWN), GrowArrow(n["out"]), FadeIn(n["out_name"]),
                  run_time=self.share(0.1))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        n = neuron_layout()
        self.add(*[n[k] for k in ("dots", "names", "body", "arrows", "weights", "plus", "constant",
                                  "out", "out_name", "head")])
        alone = label("On its own: linear regression, a straight line", 30, SUBDUED
                      ).next_to(n["head"], DOWN, 0.25)
        bend = bend_glyph(ORANGE, 1.2).move_to(n["body"])
        bend_name = label("The activation: a bend", 32, ORANGE, weight=BOLD).move_to([4.6, -1.3, 0])
        axes = plain_axes([-5, 5, 1], [-0.1, 1.1, 1], 3.0, 1.5).move_to([4.6, -2.7, 0])
        curve = s_curve(axes)
        curve_name = label("here, an S-curve", 28, ORANGE).next_to(bend_name, DOWN, 0.1)
        self.play(FadeIn(alone, shift=0.2 * DOWN), run_time=self.share(0.12))
        cue(self, "So the neuron")
        self.play(FadeOut(n["plus"]), Create(bend), FadeIn(bend_name), run_time=self.share(0.15))
        cue(self, "A common one")
        self.play(FadeIn(axes), FadeIn(curve_name), run_time=self.share(0.06))
        cue(self, "flat, then rising")
        self.play(Create(curve), run_time=self.share(0.22))
        self.finish()


def layer_layout():
    layers, edges = network([3, 4, 1], [-3.6, 0.4, 4.0], glyphs=[None, "bend", None], radius=0.32)
    names = VGroup(*[label(n, 30).next_to(u, LEFT, 0.25) for n, u in zip(INPUT_NAMES, layers[0])])
    hidden_name = label("Hidden layer", 32, BLUE, weight=BOLD).next_to(layers[1], UP, 0.3)
    hidden_note = label("its results are never seen directly", 26, SUBDUED).next_to(hidden_name, UP, 0.12)
    out_name = label("Prediction", 30).next_to(layers[2], RIGHT, 0.25)
    return layers, edges, names, VGroup(hidden_name, hidden_note), out_name


class Scene04(VideoScene):
    number = 4

    def construct(self):
        layers, edges, names, hidden_name, out_name = layer_layout()
        self.play(FadeIn(layers[0]), FadeIn(names), run_time=self.share(0.08))
        self.play(Create(edges[0]), FadeIn(layers[1], lag_ratio=0.3), run_time=self.share(0.25))
        cue(self, "Together they")
        self.play(FadeIn(hidden_name, shift=0.2 * DOWN), run_time=self.share(0.1))
        cue(self, "One more neuron")
        self.play(Create(edges[1]), FadeIn(layers[2]), FadeIn(out_name), run_time=self.share(0.2))
        self.finish()


HUMP_COLOURS = {0: VERMILION, 2: BLUE}
HUMP_NAMES = {0: "Straight line", 2: "Two neurons: a hump"}


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
    for i, units in enumerate([0, 2]):
        rows = hump[hump["units"] == units]
        curves[units] = polyline(axes, rows["temperature_c"], rows["y"], HUMP_COLOURS[units], 7)
        legend[units] = label(HUMP_NAMES[units], 30, HUMP_COLOURS[units], weight=BOLD
                              ).move_to([2.2, 2.6 - 0.6 * i, 0], aligned_edge=LEFT)
    return axes, VGroup(frame, points_name), points, curves, legend


def hump_parts(scene):
    """The two-neuron network's two bends, in a small panel of their own: one rising, one falling."""
    parts = scene.data("hump-parts")
    lo, hi = parts[["unit1", "unit2"]].min().min(), parts[["unit1", "unit2"]].max().max()
    axes = plain_axes([2, 16, 2], [lo * 1.1, hi * 1.1, 1], 3.6, 2.2).move_to([5.1, -1.2, 0])
    zero = DashedLine(axes.c2p(2, 0), axes.c2p(16, 0), color=GRID, stroke_width=2)
    rising, falling = sorted(("unit1", "unit2"), key=lambda c: parts[c].iloc[0] - parts[c].iloc[-1])
    ones = VGroup(*[polyline(axes, parts["temperature_c"], parts[c], col, 6)
                    for c, col in ((rising, PURPLE), (falling, SKY))])
    names = VGroup(label("rises", 26, PURPLE, weight=BOLD).next_to(axes, LEFT, 0.15).align_to(axes, DOWN),
                   label("falls", 26, SKY, weight=BOLD).next_to(axes, LEFT, 0.15).align_to(axes, UP))
    name = label("Its two bends", 28, SUBDUED, weight=BOLD).next_to(axes, UP, 0.2)
    return VGroup(axes, zero, name), ones, names


class Scene05(VideoScene):
    number = 5

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        cue(self, "In the survey")
        self.play(FadeIn(frame), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in points], lag_ratio=0.1), run_time=self.share(0.25))
        cue(self, "A straight line")
        self.play(Create(curves[0]), run_time=self.share(0.2))
        self.play(FadeIn(legend[0], shift=0.2 * LEFT), run_time=self.share(0.08))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        self.add(frame, points, curves[0], legend[0])
        panel, ones, names = hump_parts(self)
        self.play(curves[0].animate.set_stroke(opacity=0.3), FadeIn(panel), run_time=self.share(0.15))
        cue(self, "One bend rises")
        self.play(Create(ones[0]), FadeIn(names[0]), run_time=self.share(0.15))
        cue(self, "and the other falls")
        self.play(Create(ones[1]), FadeIn(names[1]), run_time=self.share(0.12))
        cue(self, "Added together")
        self.play(ReplacementTransform(ones.copy(), curves[2]), run_time=self.share(0.2))
        self.play(FadeIn(legend[2], shift=0.2 * LEFT), run_time=self.share(0.08))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        axes, frame, points, curves, legend = hump_layout(self)
        curves[0].set_stroke(opacity=0.3)
        panel, ones, names = hump_parts(self)
        self.add(frame, points, *curves.values(), *legend.values(), panel, ones, names)
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
        found = label("Shape not given", 32, INK, weight=BOLD).move_to([2.2, 1.0, 0], aligned_edge=LEFT)
        # The two-neuron network itself: its arrows are 4 weights, its neurons' constants 3 more.
        layers, edges = network([1, 2, 1], [0, 1.4, 2.8], glyphs=[None, "bend", None])
        small = VGroup(edges, layers).scale(1.15).move_to([4.5, -1.0, 0])
        input_name = label("Temperature", 24, SUBDUED).next_to(layers[0], DOWN, 0.15)
        arrows = VGroup(*[e for group in edges for e in group])
        arrow_count = len(arrows)
        constants = VGroup(*[label("+c", 24, GREEN, weight=BOLD).next_to(unit, UR, 0.0).shift(0.05 * LEFT)
                             for unit in (*layers[1], *layers[2])])
        assert arrow_count + len(constants) == n_weights
        tally_arrows = label(f"{arrow_count} arrows", 30, BLUE, weight=BOLD)
        tally_constants = label(f"+ {len(constants)} constants", 30, GREEN, weight=BOLD)
        tally_total = label(f"= {n_weights} weights", 30, INK, weight=BOLD)
        tally = VGroup(VGroup(tally_arrows, tally_constants).arrange(RIGHT, buff=0.2), tally_total
                       ).arrange(DOWN, buff=0.15).move_to([4.5, -2.9, 0])
        self.play(FadeOut(panel), FadeOut(ones), FadeOut(names), FadeIn(peak, scale=2), FadeIn(peak_name),
                  run_time=self.share(0.1))
        cue(self, "inside the one-degree")
        self.play(FadeIn(bin_band), FadeIn(bin_name), run_time=self.share(0.1))
        cue(self, "Nobody told")
        self.play(FadeIn(found, shift=0.2 * UP), run_time=self.share(0.08))
        cue(self, "with just seven")
        self.play(FadeIn(small), FadeIn(input_name), run_time=self.share(0.08))
        cue(self, "one on each")
        self.play(arrows.animate.set_stroke(BLUE, width=5), FadeIn(tally_arrows), run_time=self.share(0.08))
        cue(self, "and one constant")
        self.play(FadeIn(constants, lag_ratio=0.3), FadeIn(tally_constants), run_time=self.share(0.08))
        self.play(FadeIn(tally_total), run_time=self.share(0.05))
        self.finish()


class Scene08(KeyPointScene):
    number, point = 8, 1


# Stop training at the right step (scenes 9–12) ---------------------------------------------

class Scene09(VideoScene):
    number = 9

    def construct(self):
        small = int(value(self, "what-a-network-is", "small_net"))
        layers, edges = network([3, 4, 1], [-6.0, -3.8, -1.6], height=3.4, radius=0.28,
                                glyphs=[None, "bend", None], y=0.4)
        # As in scene 7: the arrows are weights, and so is each neuron's constant.
        n_arrows = sum(len(group) for group in edges)
        constants = VGroup(*[label("+c", 24, GREEN, weight=BOLD).next_to(unit, UR, 0.0).shift(0.05 * LEFT)
                             for unit in (*layers[1], *layers[2])])
        assert n_arrows + len(constants) == small
        name = label("3 inputs, 4 hidden neurons", 32, INK).move_to([3.7, 1.4, 0], aligned_edge=RIGHT)
        total = label(f"{small} weights", 36, ORANGE, weight=BOLD).move_to([4.0, 1.4, 0], aligned_edge=LEFT)
        parts = VGroup(label(f"{n_arrows} arrows", 30, ORANGE, weight=BOLD),
                       label(f"+ {len(constants)} constants", 30, GREEN, weight=BOLD)
                       ).arrange(RIGHT, buff=0.2).next_to(total, DOWN, 0.3).align_to(total, RIGHT)
        noise = lines_of("Many weights: room to fit\nthe noise as well as the pattern", 32, VERMILION, BOLD
                         ).move_to([0, -2.3, 0])
        overfit = label("Overfitting", 36, VERMILION, weight=BOLD).next_to(noise, DOWN, 0.3)
        self.add(layers, edges)
        cue(self, "Every arrow")
        self.play(edges.animate.set_color(ORANGE).set_stroke(width=4), run_time=self.share(0.08))
        cue(self, "and so is")
        self.play(FadeIn(constants, lag_ratio=0.2), run_time=self.share(0.08))
        cue(self, "Three inputs")
        self.play(FadeIn(name, shift=0.2 * LEFT), FadeIn(total, shift=0.2 * LEFT), run_time=self.share(0.08))
        cue(self, "16 arrows")
        self.play(FadeIn(parts, shift=0.2 * UP), run_time=self.share(0.08))
        cue(self, "With so many")
        self.play(FadeIn(noise, shift=0.2 * UP), run_time=self.share(0.1))
        cue(self, "That is overfitting")
        self.play(FadeIn(overfit, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


def stopping_layout(scene):
    runs = scene.data("early-stopping")
    top = np.log10(len(runs))
    axes, frame = chart([0, top, 1], [0.5, 1.1, 0.1], 8.6, 4.4, [1, 10, 100, "1,000", "8,000"],
                        [0.5, 0.7, 0.9, 1.1], "Step (log scale)", "Error",
                        x_at=[0, 1, 2, 3, top], x_fmt="{}", y_fmt="{:.1f}")
    frame.move_to([-1.6, -0.6, 0])
    # Every step would be 8,000 corners; a few hundred evenly spaced on the log axis suffice.
    keep = np.unique(np.round(np.logspace(0, top, 400)).astype(int)) - 1
    rows = runs.iloc[keep]
    xs = np.log10(rows["step"])
    training = polyline(axes, xs, rows["training"].clip(upper=1.1), BLUE, 6)
    validation = polyline(axes, xs, rows["validation"].clip(upper=1.1), ORANGE, 6)
    names = (label("Training", 30, BLUE, weight=BOLD).next_to(training.get_end(), RIGHT + DOWN, 0.1),
             label("Validation", 30, ORANGE, weight=BOLD).next_to(validation.get_end(), RIGHT + UP, 0.1))
    head = label("40 hidden neurons, 8,000 steps", 32, INK, weight=BOLD).to_edge(UP, buff=1.1)
    return axes, runs, frame, head, training, validation, names


def descent_line():
    return label("Gradient descent: each step changes every weight a little", 30, SUBDUED
                 ).to_edge(UP, buff=0.45)


class Scene10(VideoScene):
    number = 10

    def construct(self):
        axes, runs, frame, head, training, validation, names = stopping_layout(self)
        descent = descent_line()
        self.play(FadeIn(descent, shift=0.2 * DOWN), run_time=self.share(0.1))
        cue(self, "Here, a network")
        self.play(FadeIn(head), FadeIn(frame), run_time=self.share(0.12))
        cue(self, "and its training")
        self.play(Create(training), run_time=self.share(0.2))
        self.play(FadeIn(names[0]), run_time=self.share(0.06))
        self.finish()


def stopping_marks(scene, axes, runs, names):
    best_step = int(value(scene, "training-a-network", "best_step"))
    worse_pct = int(value(scene, "training-a-network", "worse_pct"))
    n_valid = int(value(scene, "training-a-network", "n_valid"))
    best = runs.iloc[best_step - 1]
    x = np.log10(best_step)
    marker = DashedLine(axes.c2p(x, 0.5), axes.c2p(x, 1.05), color=SUBDUED, stroke_width=3)
    dot = Dot(axes.c2p(x, best["validation"]), radius=0.11, color=ORANGE)
    held = label(f"{n_valid} stations held back", 28, ORANGE).next_to(names[1], UP, 0.12).align_to(names[1], LEFT)
    best_name = label(f"Lowest: step {best_step:,}", 30, ORANGE, weight=BOLD).next_to(axes.c2p(x, 1.0), LEFT, 0.15)
    worse_name = label(f"{worse_pct}% worse by the end", 30, ORANGE, weight=BOLD
                       ).next_to(held, UP, 0.25).align_to(names[1], LEFT)
    noise = lines_of("After this:\nlearning the noise", 30, VERMILION, BOLD
                     ).next_to(axes.c2p(x, 0.98), RIGHT, 0.2)
    return dict(x=x, marker=marker, dot=dot, held=held, best=best_name, worse=worse_name, noise=noise)


class Scene11(VideoScene):
    number = 11

    def construct(self):
        axes, runs, frame, head, training, validation, names = stopping_layout(self)
        self.add(descent_line(), head, frame, training, names[0])
        m = stopping_marks(self, axes, runs, names)
        self.play(FadeIn(names[1]), FadeIn(m["held"]), run_time=self.share(0.1))
        cue(self, "Their error")
        self.play(Create(validation), run_time=self.share(0.2))
        cue(self, "is lowest")
        self.play(Create(m["marker"]), FadeIn(m["dot"], scale=2), FadeIn(m["best"]), run_time=self.share(0.1))
        cue(self, "and then rises")
        self.play(FadeIn(m["worse"]), run_time=self.share(0.08))
        cue(self, "After that step")
        self.play(FadeIn(m["noise"], shift=0.2 * LEFT), run_time=self.share(0.1))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        axes, runs, frame, head, training, validation, names = stopping_layout(self)
        m = stopping_marks(self, axes, runs, names)
        self.add(descent_line(), head, frame, training, validation, *names,
                 *[m[k] for k in ("marker", "dot", "held", "best", "worse", "noise")])
        keep = lines_of("Early stopping:\nkeep these weights", 32, INK, BOLD
                        ).next_to(axes.c2p(m["x"], 0.98), RIGHT, 0.2)
        falls = lines_of("Training:\nkeeps falling", 30, BLUE, BOLD, buff=0.06).move_to(names[0], aligned_edge=UL).shift(0.45 * RIGHT)
        self.play(Indicate(m["dot"], color=ORANGE, scale_factor=2), run_time=self.share(0.15))
        cue(self, "This is called")
        self.play(FadeOut(m["noise"]), FadeIn(keep, shift=0.2 * DOWN), run_time=self.share(0.12))
        cue(self, "The training error")
        self.play(Indicate(training, color=BLUE, scale_factor=1.0), ReplacementTransform(names[0], falls),
                  run_time=self.share(0.2))
        self.finish()


class Scene13(KeyPointScene):
    number, point = 13, 2


# Let a network find combinations (scenes 14–20) ---------------------------------------------

class Scene14(VideoScene):
    number = 14

    def construct(self):
        scores = self.data("survey-scores").set_index("model")
        scale, x0 = 1.5, -2.6
        head = label("Error on the survey's counts at new sites (animals)", 30, SUBDUED).to_edge(UP, buff=0.8)
        rows = VGroup()
        for i, (model, name, colour) in enumerate([("Random forest", "Random forest", GREEN),
                                                   ("Neural network", "Network", VERMILION)]):
            y = 1.0 - 1.4 * i
            v = scores.loc[model, "counts"]
            bar = Rectangle(width=scale * v, height=0.8, stroke_width=0, fill_color=colour, fill_opacity=1
                            ).move_to([x0, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(label(name, 34).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT), bar,
                            label(f"{v:.2f}", 34, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)))
        noise = lines_of("Noisy counts: a network fits\nthe noise as readily as the pattern", 32, VERMILION, BOLD
                         ).move_to([0, -2.3, 0])
        self.play(FadeIn(head), run_time=self.share(0.08))
        cue(self, "On the survey")
        self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]), run_time=self.share(0.12))
        cue(self, "and the network")
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.1))
        cue(self, "With many weights")
        self.play(FadeIn(noise, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


PANEL_MODELS = ["Logistic regression", "Decision tree", "Random forest", "Neural network"]
PANEL_NAMES = {"Logistic regression": "Logistic regression", "Decision tree": "Decision tree",
               "Random forest": "Random forest", "Neural network": "Network, 2 neurons"}
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


class Scene15(VideoScene):
    number = 15

    def construct(self):
        axes, frame = water_axes(self, 8.0, 5.4, [-1.8, -0.1, 0])
        dots = stations(self, axes)
        core = VGroup(*[d for d in dots if isinstance(d, Dot)])
        core_name = label("Water-mass core", 32, ORANGE, weight=BOLD).move_to([2.9, 1.2, 0], aligned_edge=LEFT)
        legend = VGroup(VGroup(Dot(radius=0.08, color=ORANGE), label("Core", 26)).arrange(RIGHT, buff=0.15),
                        VGroup(Cross(scale_factor=0.06, stroke_color=GREY, stroke_width=2.5), label("Outside", 26)
                               ).arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.2, aligned_edge=LEFT
                                                                    ).move_to([2.9, 0.2, 0], aligned_edge=LEFT)
        n = len(self.data("water-train"))
        tag = lines_of(f"Simulated water mass\n{n} stations", 28, SUBDUED).move_to([2.9, 2.5, 0], aligned_edge=LEFT)
        neither = lines_of("Neither input alone:\ntheir combination", 32, INK, BOLD
                           ).move_to([2.9, -1.6, 0], aligned_edge=LEFT)
        cue(self, "Take a simulated")
        self.play(FadeIn(frame), FadeIn(tag), run_time=self.share(0.1))
        cue(self, "A station is")
        self.play(FadeIn(dots, lag_ratio=0.01), FadeIn(legend), run_time=self.share(0.15))
        cue(self, "inside a narrow")
        self.play(Indicate(core, color=ORANGE, scale_factor=1.3), FadeIn(core_name), run_time=self.share(0.12))
        cue(self, "Neither temperature")
        self.play(FadeIn(neither, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


PANEL_W, PANEL_H = 5.2, 2.7
PANEL_CENTRES = [[-3.2, 1.4, 0], [3.2, 1.4, 0], [-3.2, -2.3, 0], [3.2, -2.3, 0]]


def boundary_panels(scene):
    scores = scene.data("water-auc").set_index("model")
    panels = {}
    for model, centre in zip(PANEL_MODELS, PANEL_CENTRES):
        axes, frame = water_axes(scene, PANEL_W, PANEL_H, centre, ticks=False)
        image = class_image(scene, model, PANEL_W, PANEL_H).move_to(axes.get_center())
        dots = stations(scene, axes, radius=0.035)
        name = label(PANEL_NAMES[model], 26, INK, weight=BOLD).next_to(axes, UP, 0.12).align_to(axes, LEFT)
        score = label(f"{100 * scores.loc[model, 'accuracy']:.0f}% correct", 26, BLUE, weight=BOLD
                      ).next_to(axes, UP, 0.12).align_to(axes, RIGHT)
        panels[model] = (image, dots, name, score, axes)
    return panels


def show_panel(panel):
    image, dots, name, score, _ = panel
    return [FadeIn(image), FadeIn(dots), FadeIn(name)]


class Scene16(VideoScene):
    number = 16

    def construct(self):
        panels = boundary_panels(self)
        n_test = int(value(self, "when-a-network-pays-off", "n_test"))
        scored = label(f"Scored on {n_test:,} new stations", 28, SUBDUED).move_to([3.2, -2.3, 0])
        self.play(FadeIn(scored), run_time=self.share(0.1))
        cue(self, "Logistic regression")
        self.play(*show_panel(panels["Logistic regression"]), run_time=self.share(0.1))
        cue(self, "66%")
        self.play(FadeIn(panels["Logistic regression"][3]), run_time=self.share(0.06))
        cue(self, "A decision tree")
        self.play(*show_panel(panels["Decision tree"]), run_time=self.share(0.1))
        cue(self, "77%")
        self.play(FadeIn(panels["Decision tree"][3]), run_time=self.share(0.06))
        cue(self, "A random forest")
        self.play(*show_panel(panels["Random forest"]), run_time=self.share(0.1))
        cue(self, "86%")
        self.play(FadeIn(panels["Random forest"][3]), run_time=self.share(0.06))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        panels = boundary_panels(self)
        n_test = int(value(self, "when-a-network-pays-off", "n_test"))
        scored = label(f"Scored on {n_test:,} new stations", 28, SUBDUED).move_to([3.2, -2.3, 0])
        for model in PANEL_MODELS[:3]:
            self.add(*panels[model][:4])
        self.add(scored)
        net = panels["Neural network"]
        self.play(FadeOut(scored), *show_panel(net), run_time=self.share(0.3))
        cue(self, "and classifies")
        self.play(FadeIn(net[3], scale=1.3), run_time=self.share(0.15))
        self.play(Circumscribe(VGroup(net[4], net[2], net[3]), color=BLUE), run_time=self.share(0.2))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        axes, frame = water_axes(self, 7.8, 5.4, [-2.2, -0.1, 0])
        t_range, s_range = water_ranges(self)
        image = class_image(self, "Neural network", 7.8, 5.4).move_to(axes.get_center())
        dots = stations(self, axes, radius=0.04)
        units = self.data("water-units")
        # Each hidden neuron switches where its weighted sum is zero: a straight line on the
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
        name = lines_of("Each hidden neuron:\na bend along\na tilted line", 30, INK, BOLD
                        ).move_to([2.4, 1.6, 0], aligned_edge=LEFT)
        edges = lines_of("Two of them:\nthe band's edges", 30, BLUE, BOLD).move_to([2.4, -0.2, 0], aligned_edge=LEFT)
        found = lines_of("The combination,\nfound from the data", 30, GREEN, BOLD
                         ).move_to([2.4, -1.8, 0], aligned_edge=LEFT)
        self.add(frame, image, dots)
        self.play(FadeIn(name), LaggedStart(*[Create(line) for line in lines], lag_ratio=0.4), run_time=self.share(0.3))
        cue(self, "The two lines")
        self.play(FadeIn(edges), *[Indicate(line, color=BLUE, scale_factor=1.0) for line in lines],
                  run_time=self.share(0.2))
        cue(self, "Nobody told")
        self.play(FadeIn(found, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        # The combination the page names, added as a column.
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
        VGroup(t, s).arrange(RIGHT, buff=0.1).move_to([-3.4, 0.9, 0])
        combo.next_to(VGroup(t, s), RIGHT, 0.6)
        named = label("Named: logistic regression matches the network", 32, GREEN, weight=BOLD
                      ).move_to([0, -1.8, 0])
        unnamed = label("Nobody can name it: a network pays off", 32, BLUE, weight=BOLD).next_to(named, DOWN, 0.4)
        self.play(FadeIn(t), FadeIn(s), run_time=self.share(0.1))
        cue(self, "salinity minus")
        self.play(FadeIn(combo, shift=0.5 * LEFT), run_time=self.share(0.15))
        cue(self, "Then logistic")
        self.play(FadeIn(named), run_time=self.share(0.1))
        cue(self, "So a network")
        self.play(FadeIn(unnamed, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        # Schematic, two rows. Top: a grid of pixels, a 3x3 patch that is an edge, and edges
        # that make a fish. Bottom: a sound wave, the pitches in it, and the pitches joined
        # into a whale's call that rises and falls.
        top, low = 1.5, -1.7
        rng = np.random.default_rng(43)
        n = 9
        shade = rng.uniform(0.1, 0.35, (n, n))
        shade[:, 4:] += 0.5            # a vertical edge down the middle
        pixels = VGroup(*[Square(0.28, stroke_width=1, stroke_color=BACKGROUND, fill_color=INK,
                                 fill_opacity=float(np.clip(shade[i, j], 0, 1)))
                          for i in range(n) for j in range(n)]).arrange_in_grid(n, n, buff=0).move_to([-4.2, top, 0])
        patch = SurroundingRectangle(VGroup(*[pixels[i * n + j] for i in range(3, 6) for j in range(3, 6)]),
                                     color=ORANGE, buff=0.02, stroke_width=6)
        pixel_name = label("Pixels", 30, SUBDUED, weight=BOLD).next_to(pixels, UP, 0.2)
        arrow1 = Arrow([-2.4, top, 0], [-0.8, top, 0], color=INK, stroke_width=5)
        edge = Line([0.2, top - 0.75, 0], [0.2, top + 0.75, 0], color=ORANGE, stroke_width=10)
        edge_name = label("An edge", 30, ORANGE, weight=BOLD).next_to(edge, UP, 0.2)
        arrow2 = Arrow([1.0, top, 0], [2.6, top, 0], color=INK, stroke_width=5)
        body = Ellipse(width=2.2, height=1.1, color=BLUE, stroke_width=8).move_to([4.3, top, 0])
        tail = Polygon([5.4, top, 0], [6.2, top + 0.5, 0], [6.2, top - 0.5, 0], color=BLUE, stroke_width=8)
        shape_name = label("A fish", 30, BLUE, weight=BOLD).next_to(body, UP, 0.35)

        ts = np.linspace(0, 1, 400)
        wave = VMobject(color=SUBDUED, stroke_width=3).set_points_as_corners(
            [[-5.5 + 2.6 * t, low + 0.6 * np.sin(2 * np.pi * (6 + 10 * t) * t) * (0.5 + 0.5 * np.sin(np.pi * t)), 0]
             for t in ts])
        wave_name = label("A sound wave", 30, SUBDUED, weight=BOLD).next_to(wave, UP, 0.35)
        arrow3 = Arrow([-2.4, low, 0], [-0.8, low, 0], color=INK, stroke_width=5)
        heights = np.array([-0.5, -0.2, 0.2, 0.5, 0.3, -0.1, -0.4])
        steps = np.linspace(-0.4, 0.8, len(heights))
        pitches = VGroup(*[Line([x - 0.09, low + h, 0], [x + 0.09, low + h, 0], color=ORANGE, stroke_width=10)
                           for x, h in zip(steps, heights)])
        pitch_name = label("Pitches", 30, ORANGE, weight=BOLD).next_to(pitches, UP, 0.35)
        arrow4 = Arrow([1.0, low, 0], [2.6, low, 0], color=INK, stroke_width=5)
        call = VMobject(color=BLUE, stroke_width=8).set_points_smoothly(
            [[3.2 + 2.4 * (x + 0.4) / 1.2, low + h, 0] for x, h in zip(steps, heights)])
        call_name = label("A whale's call", 30, BLUE, weight=BOLD).next_to(call, UP, 0.35)
        nobody = label("Nobody can list them all", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(pixels, lag_ratio=0.01), FadeIn(pixel_name), run_time=self.share(0.08))
        cue(self, "an edge is")
        self.play(Create(patch), GrowArrow(arrow1), FadeIn(edge), FadeIn(edge_name), run_time=self.share(0.08))
        cue(self, "and a fish")
        self.play(GrowArrow(arrow2), Create(body), Create(tail), FadeIn(shape_name), run_time=self.share(0.08))
        cue(self, "In a recording")
        self.play(Create(wave), FadeIn(wave_name), run_time=self.share(0.08))
        cue(self, "combination of pitches")
        self.play(GrowArrow(arrow3), FadeIn(pitches, lag_ratio=0.2), FadeIn(pitch_name), run_time=self.share(0.08))
        cue(self, "rising and falling")
        self.play(GrowArrow(arrow4), Create(call), FadeIn(call_name), run_time=self.share(0.08))
        cue(self, "and nobody")
        self.play(FadeIn(nobody, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


class Scene21(KeyPointScene):
    number, point = 21, 3


# Quiz (scenes 22 and 23) -----------------------------------------------------------------

def deep_stack(hidden_layers=3, units=4, straight=True, width=9.0, height=4.4, radius=0.24):
    xs = np.linspace(-width / 2, width / 2, hidden_layers + 2)
    glyph = "straight" if straight else "bend"
    return network([3] + [units] * hidden_layers + [1], xs, height=height, radius=radius,
                   glyphs=[None] + [glyph] * hidden_layers + [None], y=-0.2)


def one_line(centre):
    axes = plain_axes([0, 1, 1], [0, 1, 1], 4.2, 2.8).move_to(centre)
    line = Line(axes.c2p(0.05, 0.12), axes.c2p(0.95, 0.88), color=BLUE, stroke_width=8)
    return VGroup(axes, line)


class Scene22(QuizScene):
    number = 22
    question = ("A network has ten hidden layers", "of a hundred neurons each, but no bends:",
                "every neuron passes on its weighted sum.", "What shapes can it fit?")


class Scene23(VideoScene):
    number = 23

    def construct(self):
        layers, edges = deep_stack(hidden_layers=10, units=5, width=11.0, height=3.8, radius=0.16)
        answer = label("Only a straight line", 52, BLUE, weight=BOLD).to_edge(UP, buff=0.6)
        result = one_line([0, -0.2, 0])
        why = lines_of("A weighted sum of weighted sums\nis still a weighted sum", 34, INK, BOLD
                       ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(answer), FadeIn(layers), Create(edges), run_time=self.share(0.15))
        cue(self, "Each layer")
        self.play(ReplacementTransform(VGroup(layers, edges), result), run_time=self.share(0.25))
        cue(self, "a weighted sum of")
        self.play(FadeIn(why, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


# Key points and end card (scenes 24–27) ----------------------------------------------------

class Scene24(RecapScene):
    number, point = 24, 1


class Scene25(RecapScene):
    number, point = 25, 2


class Scene26(RecapScene):
    number, point = 26, 3


class Scene27(EndCardScene):
    number = 27
