"""Manim scenes for the generalisation video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/05-generalisation
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is built on three ideas from the section, each with the reason it matters: a
perfect fit is a warning sign, the U-shaped error curve comes from bias and variance,
and complexity is chosen by cross-validation with the test sites opened once. Scenes
marked "page results" read visuals/data/*.csv, which tools/figures-for-video.R writes
from the pages. The others are schematic: made-up shapes, never numbers that could
pass for survey results. The opening, key-point, recap, quiz and end-card scenes are
shared (mlbasic_video.py) and read PROMISES, ANSWERS and RECAP from here. Consecutive
scenes about one picture share a builder, so each starts where the previous one ended.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["Why a perfect fit is a warning sign",
            "Where the U-shaped error curve comes from",
            "How to choose complexity honestly"]
ANSWERS = ["A perfect fit is a warning sign:\nthe model has memorised the noise",
           "The U-shaped error curve comes from\nbias falling and variance rising",
           "Choose complexity with cross-validation;\nopen the test set only once"]
RECAP = ["A perfect fit is a warning sign",
         "The U-shaped error curve comes from bias and variance",
         "Choose complexity with cross-validation; open the test set once"]

# The two errors in the colours of the pages' figures: ggplot's first two palette colours.
FITTING, NEW = BLUE, ORANGE

# The five models in the colours fig-crossing gives them (ggplot orders them alphabetically).
MODEL_COLOURS = {"Boosting": BLUE, "Decision tree, depth 3": ORANGE,
                 "Decision tree, grown out": GREEN, "Linear regression": VERMILION,
                 "Random forest": PURPLE}
GROWN_OUT = "Decision tree, grown out"


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


def f2(value):
    """Two decimal places, as the pages' sprintf("%.2f") prints them."""
    return f"{value:.2f}"


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name, size=24,
          x_text=None, y_text=None):
    """Axes with tick labels and names, in the series style; returns the axes and all of it.

    `x_text` and `y_text` turn a tick's position into its label, for log scales.
    """
    axes = plain_axes(x_range, y_range, x_length, y_length)
    x_text = x_text or (lambda v: f"{v:g}")
    y_text = y_text or (lambda v: f"{v:g}")
    tx = VGroup(*[label(x_text(v), size, SUBDUED).next_to(axes.c2p(v, y_range[0]), DOWN, 0.15)
                  for v in x_ticks])
    ty = VGroup(*[label(y_text(v), size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15)
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


def polyline(axes, xs, ys, colour, width=6):
    return VMobject(color=colour, stroke_width=width).set_points_as_corners(
        [axes.c2p(x, y) for x, y in zip(xs, ys)])


def hline(axes, y, x0, x1, colour=GREY, width=4):
    return DashedLine(axes.c2p(x0, y), axes.c2p(x1, y), color=colour, stroke_width=width, dash_length=0.12)


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("why a perfect", "where the U", "and how to choose"))


# A perfect fit is a warning sign (scenes 2–10) ---------------------------------------------

BAR_LEFT = -1.9           # where the bars start
BAR_SCALE = 1.05          # units of width per unit of RMSE


def five_models_layout(scene):
    """The five models, best on their training stations first, each with two bars."""
    models = scene.data("five-models").sort_values("training").reset_index(drop=True)
    heading = title("Five models, one survey", 46).to_edge(UP, buff=0.45)
    rows = VGroup()
    for i, m in models.iterrows():
        y = 1.75 - 1.0 * i
        name = label(m["model"], 30).move_to([BAR_LEFT - 0.3, y, 0], aligned_edge=RIGHT)
        fit_bar = Rectangle(width=max(m["training"] * BAR_SCALE, 0.02), height=0.34, stroke_width=0,
                            fill_color=FITTING, fill_opacity=1).move_to([BAR_LEFT, y + 0.19, 0], aligned_edge=LEFT)
        fit_value = plated(label(f2(m["training"]), 26, FITTING), buff=0.06).next_to(fit_bar, RIGHT, 0.15)
        new_bar = Rectangle(width=m["new"] * BAR_SCALE, height=0.34, stroke_width=0,
                            fill_color=NEW, fill_opacity=1).move_to([BAR_LEFT, y - 0.19, 0], aligned_edge=LEFT)
        new_value = plated(label(f2(m["new"]), 26, NEW), buff=0.06).next_to(new_bar, RIGHT, 0.15)
        mark = label("?", 34, NEW, weight=BOLD).move_to([BAR_LEFT + 0.35, y - 0.19, 0])
        for value in (fit_value, new_value):     # solid, so the faded values hide the average line
            value[0].set_fill(opacity=1)
        rows.add(VGroup(name, fit_bar, fit_value, new_bar, new_value, mark))
    key = VGroup(
        VGroup(Square(0.3, fill_color=FITTING, fill_opacity=1, stroke_width=0),
               label("error on the training stations", 28, SUBDUED)).arrange(RIGHT, buff=0.15),
        VGroup(Square(0.3, fill_color=NEW, fill_opacity=1, stroke_width=0),
               label("error on new sites", 28, SUBDUED)).arrange(RIGHT, buff=0.15),
    ).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.45)
    unit = label("error (RMSE, animals)", 24, SUBDUED).move_to([BAR_LEFT, 2.45, 0], aligned_edge=LEFT)
    baseline = models["baseline"].iloc[0]
    x = BAR_LEFT + baseline * BAR_SCALE
    average = DashedLine([x, 2.35, 0], [x, -2.6, 0], color=GREY, stroke_width=4, dash_length=0.12)
    average_name = label(f"predict the average: {f2(baseline)}", 26, GREY).next_to(average, UP, 0.1)
    perfect = rows[int(models.index[models["model"] == GROWN_OUT][0])]
    return models, heading, rows, key, unit, average, average_name, perfect


class Scene02(VideoScene):
    number = 2

    def construct(self):
        models, heading, rows, key, unit, *_ = five_models_layout(self)
        # "Let's start with five models from supervised learning, all fitted to the same simulated
        # coastal survey: linear regression, two decision trees, a random forest and boosting."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.06))
        cue(self, "linear regression, two")
        self.play(LaggedStart(*[FadeIn(r[0], shift=0.2 * RIGHT) for r in rows], lag_ratio=0.15),
                  run_time=self.share(0.15))
        # "The bars show each model's error on its training stations, the stations it was fitted to."
        cue(self, "The bars show")
        self.play(FadeIn(key[0]), run_time=self.share(0.05))
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                              lag_ratio=0.2), run_time=self.share(0.2))
        # "The error is the typical miss, in animals, from the introduction, so shorter is better."
        cue(self, "The error is")
        self.play(FadeIn(unit), Indicate(unit, color=INK), run_time=self.share(0.1))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        models, heading, rows, key, unit, *_, perfect = five_models_layout(self)
        self.add(heading, *[VGroup(r[0], r[1], r[2]) for r in rows], key[0], unit)
        others = [VGroup(r[0], r[1], r[2][1]) for r in rows if r is not perfect]   # plates stay solid
        one_each = plated(label("every leaf: one station", 28, FITTING, weight=BOLD)).next_to(perfect[2], RIGHT, 0.8)
        # "One of them is perfect."
        self.play(*[o.animate.fade(0.7) for o in others], run_time=self.share(0.08))
        # "This decision tree kept splitting until every leaf, every final group, held a single station."
        cue(self, "held a single")
        self.play(FadeIn(one_each), run_time=self.share(0.08))
        # "So it predicts each training station as that station's own count, and its error is exactly zero."
        cue(self, "and its error")
        self.play(perfect[2].animate.scale(1.6, about_edge=LEFT), run_time=self.share(0.08))
        self.play(Circumscribe(VGroup(perfect[0], perfect[2]), color=FITTING), run_time=self.share(0.25))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        models, heading, rows, key, unit, *_, perfect = five_models_layout(self)
        self.add(heading, *[VGroup(r[0], r[1], r[2]) for r in rows], key[0], unit)
        # "Which one would you trust at sites it has never seen?"
        self.play(FadeIn(key[1]), LaggedStart(*[FadeIn(r[5], scale=1.6) for r in rows], lag_ratio=0.15),
                  run_time=self.share(0.5))
        self.play(Wiggle(VGroup(*[r[5] for r in rows])), run_time=self.share(0.4))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        models, heading, rows, key, unit, average, average_name, perfect = five_models_layout(self)
        self.add(heading, *[VGroup(r[0], r[1], r[2], r[5]) for r in rows], key, unit)
        # "To find out, score them on new sites, held back from fitting, as a stand-in for the places ..."
        self.play(*[FadeOut(r[5]) for r in rows], run_time=self.share(0.05))
        for r in rows:
            r.remove(r[5])
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[3], LEFT), FadeIn(r[4])) for r in rows],
                              lag_ratio=0.15), run_time=self.share(0.3))
        # "The perfect tree comes last, at 6.21."
        cue(self, "The perfect tree")
        others = [VGroup(r[0], r[1], r[2][1], r[3], r[4][1]) for r in rows if r is not perfect]
        self.play(*[o.animate.fade(0.7) for o in others],
                  perfect[4].animate.scale(1.5, about_edge=LEFT), run_time=self.share(0.1))
        # "That is worse than ignoring every input and predicting the average count everywhere, which
        # misses by 4.83."
        cue(self, "That is worse")
        self.play(Create(average), FadeIn(average_name), run_time=self.share(0.15))
        self.finish()


def crossing_layout(scene):
    """Each model as a line from its error on the training stations to its error on new sites."""
    models = scene.data("five-models")
    top = math.ceil(models["new"].max())
    axes, frame = chart([0, 1, 1], [0, top, 1], 5.2, 5.4, [], range(0, top + 1),
                        None, "error (RMSE, animals)")
    frame.move_to([-1.6, -0.3, 0])
    sides = VGroup(label("training stations", 30, FITTING, weight=BOLD).next_to(axes.c2p(0, 0), DOWN, 0.3),
                   label("new sites", 30, NEW, weight=BOLD).next_to(axes.c2p(1, 0), DOWN, 0.3))
    lines, names = VGroup(), VGroup()
    for _, m in models.iterrows():
        colour = MODEL_COLOURS[m["model"]]
        a, b = axes.c2p(0, m["training"]), axes.c2p(1, m["new"])
        lines.add(VGroup(Line(a, b, color=colour, stroke_width=6), Dot(a, radius=0.1, color=colour),
                         Dot(b, radius=0.1, color=colour)))
        names.add(label(m["model"], 26, colour, weight=BOLD).next_to(b, RIGHT, 0.25))
    # Keep the names apart where errors on new sites are close.
    order = list(models["new"].sort_values(ascending=False).index)
    for k in range(1, len(order)):
        above, here = names[order[k - 1]], names[order[k]]
        if here.get_top()[1] > above.get_bottom()[1] - 0.08:
            here.shift((here.get_top()[1] - above.get_bottom()[1] + 0.08) * DOWN)
    heading = title("The order turns over", 46).to_edge(UP, buff=0.45)
    linear = list(models["model"]).index("Linear regression")
    return frame, sides, lines, names, heading, linear


class Scene06(VideoScene):
    number = 6

    def construct(self):
        frame, sides, lines, names, heading, linear = crossing_layout(self)
        forest = list(self.data("five-models")["model"]).index("Random forest")
        # "Here, each line joins a model's two errors."
        self.play(FadeIn(frame), FadeIn(sides), run_time=self.share(0.08))
        self.play(LaggedStart(*[AnimationGroup(Create(l), FadeIn(n)) for l, n in zip(lines, names)],
                              lag_ratio=0.2), run_time=self.share(0.25))
        # "The order turns over."
        cue(self, "The order turns")
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "Linear regression, last on its own stations, is close to the best on new ones, ..."
        cue(self, "Linear regression")
        self.play(*[VGroup(l, n).animate.fade(0.75) for i, (l, n) in enumerate(zip(lines, names))
                    if i not in (linear, forest)], lines[linear][0].animate.set_stroke(width=10),
                  run_time=self.share(0.1))
        self.play(Indicate(names[linear], color=MODEL_COLOURS["Linear regression"]), run_time=self.share(0.15))
        # "... behind only the random forest."
        cue(self, "behind only")
        self.play(Indicate(names[forest], color=MODEL_COLOURS["Random forest"]), run_time=self.share(0.12))
        self.finish()


# Made-up stations for the signal-and-noise scenes: a schematic, not the survey.
def signal_and_noise():
    rng = np.random.default_rng(8)
    x = np.linspace(0.04, 0.96, 24) + rng.uniform(-0.012, 0.012, 24)
    signal = lambda v: 0.3 + 0.95 * v ** 1.4  # noqa: E731
    y = signal(x) + rng.normal(0, 0.14, x.size)
    axes = plain_axes([0, 1, 1], [0, 1.6, 1], 8.6, 4.8).move_to([-1.9, -0.5, 0])
    names = VGroup(label("water temperature", 28, SUBDUED).next_to(axes.x_axis, DOWN, 0.25),
                   label("catch", 28, SUBDUED).rotate(PI / 2).next_to(axes.y_axis, LEFT, 0.25))
    dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.08, color=GREY) for a, b in zip(x, y)])
    trend = axes.plot(signal, x_range=[0.02, 0.98], color=GREEN, stroke_width=6)
    noise = VGroup(*[Line(axes.c2p(a, signal(a)), axes.c2p(a, b), color=PURPLE, stroke_width=4)
                     for a, b in zip(x, y)])
    rigid = lambda v: 0.42 + 0.75 * v  # noqa: E731   a straight line, too rigid for the curve
    model = axes.plot(rigid, x_range=[0.02, 0.98], color=FITTING, stroke_width=6)
    model_name = plated(label("a model", 28, FITTING, weight=BOLD)).move_to(axes.c2p(0.88, 1.5))
    misses = VGroup(*[Line(axes.c2p(a, rigid(a)), axes.c2p(a, b), color=FITTING, stroke_width=4)
                      for a, b in zip(x, y)])
    # One station below the pattern, where the model is above it: its residual is its noise
    # plus the model's own mistake.
    k = 14
    close = (x[k], y[k], signal(x[k]), rigid(x[k]))
    zigzag = VMobject(color=VERMILION, stroke_width=5).set_points_as_corners(
        [axes.c2p(a, b) for a, b in zip(x, y)])
    signal_tag = label("pattern: turns up again", 30, GREEN, weight=BOLD).next_to(axes.c2p(0.05, 1.3), RIGHT, 0)
    noise_tag = label("noise: these stations only", 30, PURPLE, weight=BOLD).next_to(signal_tag, DOWN, 0.2,
                                                                                      aligned_edge=LEFT)
    return dict(axes=axes, names=names, dots=dots, trend=trend, noise=noise, zigzag=zigzag,
                signal_tag=signal_tag, noise_tag=noise_tag, model=model, model_name=model_name,
                misses=misses, k=k, close=close)


def definitions():
    """The three words, built up on the right of the signal-and-noise chart."""
    rows = VGroup()
    for term, lines, colour in (("noise", ["a count's gap from the pattern", "belongs to the data"], PURPLE),
                                ("residual", ["a count's gap from the model", "noise + the model's mistake"], FITTING),
                                ("error", ["one number:", "the typical miss"], INK)):
        rows.add(VGroup(label(term, 32, colour, weight=BOLD), *[label(s, 24, SUBDUED) for s in lines]
                        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT))
    return rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.85, -0.3, 0])


class Scene07(VideoScene):
    number = 7

    def construct(self):
        p = signal_and_noise()
        # "Why? Data hold two things: a pattern and noise."
        self.play(FadeIn(p["axes"]), FadeIn(p["names"]), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in p["dots"]], lag_ratio=0.05),
                  run_time=self.share(0.15))
        # "The pattern, such as warmer water holding more of a species, turns up again at new sites."
        cue(self, "The pattern")
        self.play(Create(p["trend"]), FadeIn(p["signal_tag"]), run_time=self.share(0.25))
        # "Noise, the part of a count that the conditions do not decide, such as one lucky haul, does not."
        cue(self, "Noise")
        self.play(LaggedStart(*[Create(r) for r in p["noise"]], lag_ratio=0.04),
                  FadeIn(p["noise_tag"]), run_time=self.share(0.25))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        p = signal_and_noise()
        self.add(p["axes"], p["names"], p["dots"], p["trend"], p["noise"], p["signal_tag"], p["noise_tag"])
        axes, k, rows = p["axes"], p["k"], definitions()
        a, count, pattern, predicted = p["close"]
        nudge = 0.12 * RIGHT       # the three gaps side by side at the one station
        noise = Line(axes.c2p(a, pattern), axes.c2p(a, count), color=PURPLE, stroke_width=8).shift(-nudge)
        residual = Line(axes.c2p(a, predicted), axes.c2p(a, count), color=FITTING, stroke_width=8).shift(nudge)
        mistake = Line(axes.c2p(a, pattern), axes.c2p(a, predicted), color=VERMILION, stroke_width=8).shift(3 * nudge)
        noise_name = plated(label("noise", 28, PURPLE, weight=BOLD)).next_to(noise, LEFT, 0.15)
        residual_name = plated(label("residual", 28, FITTING, weight=BOLD)).next_to(
            residual.point_from_proportion(0.75), RIGHT, 0.15)
        mistake_name = plated(label("model's mistake", 24, VERMILION, weight=BOLD)).next_to(mistake, RIGHT, 0.12)
        others = VGroup(*[r for i, r in enumerate(p["noise"]) if i != k])
        # "Three words are easy to mix up here."
        self.play(others.animate.set_stroke(opacity=0.2), run_time=self.share(0.05))
        # "Noise belongs to the data: how far a count falls from the pattern, which we never get to see."
        cue(self, "Noise belongs")
        self.play(ReplacementTransform(p["noise"][k], noise), FadeIn(noise_name), FadeIn(rows[0]),
                  run_time=self.share(0.08))
        # "A residual belongs to a fitted model: how far a count falls from the model's prediction."
        cue(self, "A residual belongs")
        self.play(Create(p["model"]), FadeIn(p["model_name"]), run_time=self.share(0.08))
        cue(self, "from the model's")
        self.play(Create(residual), FadeIn(residual_name), FadeIn(rows[1][:2]), run_time=self.share(0.08))
        # "Part of it is noise, and the rest is the model's own mistake."
        cue(self, "Part of it")
        self.play(Indicate(noise_name, color=PURPLE), FadeIn(rows[1][2]), run_time=self.share(0.06))
        cue(self, "and the rest")
        self.play(Create(mistake), FadeIn(mistake_name), run_time=self.share(0.06))
        # "The error rolls many misses into one number, the typical miss, on the training stations or on new sites."
        cue(self, "The error rolls")
        self.play(FadeOut(VGroup(others, noise, noise_name, residual, residual_name, mistake, mistake_name)),
                  run_time=self.share(0.05))
        self.play(LaggedStart(*[Create(m) for m in p["misses"]], lag_ratio=0.04), FadeIn(rows[2]),
                  run_time=self.share(0.15))
        self.finish()


def error_gauges():
    """Two unlabelled error bars with no scale: only their movement matters (schematic)."""
    gauges = VGroup()
    for name, colour in (("on its own stations", FITTING), ("on new sites", NEW)):
        head = label(f"error {name}", 28, colour, weight=BOLD)
        track = Rectangle(width=3.4, height=0.34, stroke_color=GRID, stroke_width=2)
        gauges.add(VGroup(head, track).arrange(DOWN, buff=0.15, aligned_edge=LEFT))
    gauges.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([4.7, 0.4, 0])
    return gauges


class Scene09(VideoScene):
    number = 9

    def construct(self):
        p = signal_and_noise()
        made = VGroup(p["model"], p["model_name"], p["misses"], definitions())
        self.add(p["axes"], p["names"], p["dots"], p["trend"], p["signal_tag"], p["noise_tag"], made)
        gauges = error_gauges()
        own, new = ValueTracker(0.75), ValueTracker(0.75)

        def bar(tracker, gauge, colour):
            return always_redraw(lambda: Rectangle(
                width=max(3.4 * tracker.get_value(), 0.001), height=0.34, stroke_width=0, fill_color=colour,
                fill_opacity=1).align_to(gauge[1], LEFT).align_to(gauge[1], DOWN))

        bars = VGroup(bar(own, gauges[0], FITTING), bar(new, gauges[1], NEW))
        # "A flexible model, one that can bend freely, cannot tell the pattern from the noise."
        self.play(FadeOut(made), p["trend"].animate.set_stroke(opacity=0.3), run_time=self.share(0.05))
        self.play(FadeIn(gauges), FadeIn(bars), run_time=self.share(0.05))
        # "Fitting the noise lowers its error on its own stations, but not on new ones."
        cue(self, "Fitting the noise")
        self.play(Create(p["zigzag"]), own.animate.set_value(0), new.animate.set_value(0.95),
                  run_time=self.share(0.35), rate_func=linear)
        # "The perfect tree has memorised the noise."
        cue(self, "The perfect tree")
        memorised = card("memorised\nthe noise", VERMILION, 32).move_to([4.7, -1.9, 0])
        self.play(FadeIn(memorised, scale=0.9), run_time=self.share(0.08))
        # "This is overfitting."
        cue(self, "This is overfitting")
        named = card("overfitting:\nmemorised\nthe noise", VERMILION, 32).move_to([4.7, -2.1, 0])
        self.play(ReplacementTransform(memorised, named), run_time=self.share(0.08))
        self.finish()


class Scene10(KeyPointScene):
    number, point = 10, 1


# The U-shaped error curve (scenes 11–19) ---------------------------------------------------

def u_curve_layout(scene):
    curve = scene.data("u-curve").sort_values("leaves")
    lo, hi = 0.4, math.log10(500)
    top = math.ceil(curve["new"].max())
    axes, frame = chart([lo, hi, 1], [0, top, 1], 9.6, 4.9, [math.log10(v) for v in (3, 10, 30, 100, 300)],
                        range(0, top + 1), "leaves in the tree (log scale): more leaves, more flexible",
                        "error (RMSE, animals)",
                        x_text=lambda v: f"{10 ** v:.0f}")
    frame.move_to([-0.6, -0.7, 0])
    xs = [math.log10(v) for v in curve["leaves"]]

    def trace(column, colour):
        line = polyline(axes, xs, curve[column], colour)
        dots = VGroup(*[Dot(axes.c2p(x, v), radius=0.07, color=colour) for x, v in zip(xs, curve[column])])
        return VGroup(line, dots)

    fitting, new = trace("training", FITTING), trace("new", NEW)
    names = VGroup(label("training stations", 30, FITTING, weight=BOLD).next_to(fitting[1][-3], LEFT, 0.3),
                   label("new sites", 30, NEW, weight=BOLD).next_to(new[1][-1], RIGHT, 0.2))
    baseline = curve["baseline"].iloc[0]
    average = hline(axes, baseline, lo, hi)
    average_name = VGroup(label("predict", 24, GREY), label("the average", 24, GREY)).arrange(
        DOWN, buff=0.06, aligned_edge=LEFT).next_to(axes.c2p(hi, baseline), RIGHT, 0.15)
    return curve, axes, frame, xs, fitting, new, names, VGroup(average, average_name)


class Scene11(VideoScene):
    number = 11

    def construct(self):
        curve, axes, frame, xs, fitting, new, names, average = u_curve_layout(self)
        heading = title("A tree swept from rigid to flexible", 44).to_edge(UP, buff=0.45)
        rule = label("minimum node size: the smallest group of stations the tree may split", 28,
                     SUBDUED).next_to(heading, DOWN, 0.2)
        # "Now for the U-shaped error curve."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.05))
        # "A decision tree's flexibility is set by its minimum node size: the smallest group of stations it
        # may still split."
        cue(self, "A decision tree's")
        self.play(FadeIn(rule), run_time=self.share(0.05))
        # "Sweep it from large to small, and the tree grows from a few leaves to many."
        cue(self, "Sweep it")
        self.play(Indicate(frame[3], color=INK, scale_factor=1.1), run_time=self.share(0.1))
        # "Its error on the training stations falls all the way to zero."
        cue(self, "Its error on the training")
        self.play(Create(fitting[0]), LaggedStart(*[FadeIn(d) for d in fitting[1]]), FadeIn(names[0]),
                  run_time=self.share(0.1), rate_func=linear)
        self.play(Flash(fitting[1][-1], color=FITTING), run_time=self.share(0.03))
        # "Its error on new sites falls a little, then rises."
        cue(self, "Its error on new")
        self.play(FadeIn(average), run_time=self.share(0.03))
        self.play(Create(new[0]), LaggedStart(*[FadeIn(d) for d in new[1]]), FadeIn(names[1]),
                  run_time=self.share(0.1), rate_func=linear)
        # "That is the U-shaped error curve, ..."
        cue(self, "That is the U")
        name = title("the U-shaped error curve", 44).set_color(NEW).move_to(heading)
        glow = new[0].copy().set_stroke(NEW, width=16, opacity=0.5)
        self.play(ReplacementTransform(heading, name), FadeOut(rule), ShowPassingFlash(glow, time_width=0.5),
                  run_time=self.share(0.1))
        # "... and the best tree sits at its lowest point."
        cue(self, "and the best tree")
        low = int(np.argmin(curve["new"].to_numpy()))
        best = Dot(new[1][low].get_center(), radius=0.13, color=NEW).set_z_index(10)
        best_name = plated(label("the best tree", 28, NEW, weight=BOLD)).next_to(best, UP, 0.35, aligned_edge=LEFT)
        self.play(FadeIn(best, scale=1.6), FadeIn(best_name), run_time=self.share(0.06))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        curve, axes, frame, xs, fitting, new, names, average = u_curve_layout(self)
        heading = title("the U-shaped error curve", 44).set_color(NEW).to_edge(UP, buff=0.45)
        self.add(heading, frame, fitting, new, names, average)
        rigid, loose = curve.iloc[0], curve.iloc[-1]
        x_rigid, x_loose = xs[0], xs[-1]
        # Underfitting: both errors high and close together.
        under_box = SurroundingRectangle(VGroup(fitting[1][0], new[1][0]), color=PURPLE, buff=0.2, corner_radius=0.1)
        under = label("underfitting", 34, PURPLE, weight=BOLD).move_to(axes.c2p(x_rigid, 6.6), aligned_edge=LEFT)
        under_note = label("both high, close together", 26, PURPLE).next_to(under, DOWN, 0.08, aligned_edge=LEFT)
        # Overfitting: a wide gap between them.
        gap = Line(axes.c2p(x_loose, loose["training"]), axes.c2p(x_loose, loose["new"]))
        brace = Brace(gap, LEFT, color=VERMILION)
        over = label("overfitting", 34, VERMILION, weight=BOLD).next_to(brace, LEFT, 0.2).shift(0.5 * UP)
        over_note = label("a wide gap", 26, VERMILION).next_to(over, DOWN, 0.08)
        # "On the left, the tree underfits: it is too rigid to follow the pattern, so both errors are high
        # and close together."
        self.play(Create(under_box), FadeIn(under), run_time=self.share(0.15))
        cue(self, "both errors")
        self.play(FadeIn(under_note), run_time=self.share(0.08))
        # "On the right, it overfits: a low error on its own stations, and a high one on new sites."
        cue(self, "On the right")
        self.play(GrowFromCenter(brace), FadeIn(over), run_time=self.share(0.15))
        cue(self, "a low error")
        self.play(FadeIn(over_note), run_time=self.share(0.08))
        self.finish()


# Schematic targets: the bullseye is the expected count; each dot, one survey's model.
def target(centre, radius=1.75):
    rings = VGroup(*[Circle(radius=radius * k / 4, color=GRID, stroke_width=3) for k in range(1, 5)]).move_to(centre)
    bull = Dot(centre, radius=0.09, color=INK)
    tag = label("the expected count", 24, SUBDUED).next_to(rings, DOWN, 0.2)
    return VGroup(rings, bull, tag)


def hits(centre, offset, spread, seed, colour, n=14):
    rng = np.random.default_rng(seed)
    points = rng.normal(0, spread, (n, 2)) + np.array(offset)
    return VGroup(*[Dot(centre + np.array([a, b, 0]), radius=0.08, color=colour) for a, b in points])


LEFT_BOARD, RIGHT_BOARD = np.array([-3.4, -0.4, 0]), np.array([3.4, -0.4, 0])


def bias_board():
    board = target(LEFT_BOARD)
    shots = hits(LEFT_BOARD, [0.8, 0.65], 0.16, 21, BLUE)
    centre = Dot(LEFT_BOARD + np.array([0.8, 0.65, 0]), radius=0.12, color=INK)
    arrow = Arrow(LEFT_BOARD, centre.get_center(), buff=0.05, color=INK, stroke_width=5,
                  max_tip_length_to_length_ratio=0.25)
    name = label("bias", 46, BLUE, weight=BOLD).next_to(board, UP, 0.75)
    note = label("how far their average misses", 28, SUBDUED).next_to(name, DOWN, 0.1)
    each = label("each dot: one survey's prediction", 26, SUBDUED).next_to(board[2], DOWN, 0.15)
    board.add(each)
    return board, shots, arrow, VGroup(name, note)


class Scene13(VideoScene):
    number = 13

    def construct(self):
        board, shots, arrow, name = bias_board()
        heading = label("the same model, fitted to survey after survey", 32, SUBDUED).to_edge(UP, buff=0.4)
        # "Where does the U come from?"
        # "Imagine surveying the shelf again and again, and fitting the same model each time."
        cue(self, "Imagine")
        self.play(FadeIn(heading), FadeIn(board[0]), run_time=self.share(0.08))
        # "Each survey gives a slightly different model, and so a slightly different prediction at one
        # station: the dots on this target."
        cue(self, "Each survey gives")
        self.play(LaggedStart(*[FadeIn(s, scale=2) for s in shots], lag_ratio=0.2), run_time=self.share(0.2))
        cue(self, "the dots on")
        self.play(FadeIn(board[3]), run_time=self.share(0.05))
        # "The centre is the station's expected count, the average it would give if it could be sampled
        # again and again."
        cue(self, "The centre is")
        self.play(FadeIn(board[1], scale=2), FadeIn(board[2]), run_time=self.share(0.06))
        self.play(Flash(board[1], color=INK), run_time=self.share(0.06))
        # "Bias is how far the average of the predictions misses the centre."
        cue(self, "Bias is")
        self.play(GrowArrow(arrow), FadeIn(name), run_time=self.share(0.1))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        board, shots, arrow, name = bias_board()
        heading = label("the same model, fitted to survey after survey", 32, SUBDUED).to_edge(UP, buff=0.4)
        self.add(heading, board, shots, arrow, name)
        right = target(RIGHT_BOARD)
        scatter = hits(RIGHT_BOARD, [0, 0], 0.65, 22, VERMILION)
        right_name = VGroup(label("variance", 46, VERMILION, weight=BOLD),
                            label("how much the predictions spread", 28, SUBDUED)).arrange(DOWN, buff=0.1).next_to(right, UP, 0.3).align_to(name, UP)
        flexible = label("a flexible model", 28, VERMILION, weight=BOLD).next_to(right[2], DOWN, 0.15)
        # "Variance is how much the predictions change from one survey to the next."
        self.play(FadeIn(right), FadeIn(right_name), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(s, scale=2) for s in scatter], lag_ratio=0.15), run_time=self.share(0.3))
        # "A flexible model follows whichever stations it happened to get, so its predictions spread widely."
        cue(self, "A flexible model")
        self.play(FadeIn(flexible), run_time=self.share(0.08))
        self.finish()


PART_COLOURS = {"bias_squared": BLUE, "variance": VERMILION, "sum": GREEN}


def parts_layout(scene):
    parts = scene.data("parts").sort_values("leaves")
    lo, hi = 0.2, math.log10(300)
    top = 5 * math.ceil(max(parts["noise"].max(), (parts["bias_squared"] + parts["variance"]).max()) / 5)
    axes, frame = chart([lo, hi, 1], [0, top, 5], 9.0, 4.9, [math.log10(v) for v in (3, 10, 30, 100)],
                        range(0, top + 1, 5), "leaves in the tree (log scale)", "squared error (animals²)",
                        x_text=lambda v: f"{10 ** v:.0f}")
    frame.move_to([-0.9, -0.7, 0])
    xs = [math.log10(v) for v in parts["leaves"]]
    total = parts["bias_squared"] + parts["variance"]
    lines = {"bias_squared": polyline(axes, xs, parts["bias_squared"], BLUE),
             "variance": polyline(axes, xs, parts["variance"], VERMILION),
             "sum": polyline(axes, xs, total, GREEN)}
    ends = {"bias_squared": parts["bias_squared"].iloc[-1], "variance": parts["variance"].iloc[-1],
            "sum": total.iloc[-1]}
    names = {k: label(t, 30, PART_COLOURS[k], weight=BOLD).next_to(axes.c2p(xs[-1], ends[k]), RIGHT, 0.2)
             for k, t in (("bias_squared", "bias²"), ("variance", "variance"), ("sum", "bias² + variance"))}
    if names["sum"].get_bottom()[1] < names["variance"].get_top()[1] + 0.08:
        names["sum"].shift((names["variance"].get_top()[1] + 0.08 - names["sum"].get_bottom()[1]) * UP)
    noise = parts["noise"].iloc[0]
    noise_line = hline(axes, noise, lo, math.log10(60), GREY, 5)   # stops short of the curves' names
    noise_name = label("noise", 30, GREY, weight=BOLD).next_to(axes.c2p(lo, noise), UR, 0.1)
    best = parts[parts["min_n"] == parts["best_min_n"].iloc[0]].iloc[0]
    best_x = math.log10(best["leaves"])
    return parts, axes, frame, lines, names, noise_line, noise_name, best, best_x


def squared_note(heading):
    return label("bias²: bias × bias, so it adds to the variance", 28, BLUE).next_to(heading, DOWN, 0.2)


def bias_notes(axes, parts):
    """Why bias falls, and why it stops: two notes pointing at the bias² line."""
    first = parts.iloc[0]
    lowest = parts.loc[parts["bias_squared"].idxmin()]
    few = plated(VGroup(label("few leaves: very different stations", 26, BLUE, weight=BOLD),
                        label("share one prediction", 26, BLUE, weight=BOLD)).arrange(DOWN, buff=0.08,
                                                                                   aligned_edge=LEFT))
    few.next_to(axes.c2p(math.log10(first["leaves"]), 17), RIGHT, 0).shift(0.1 * LEFT)
    few_arrow = Arrow(few.get_bottom() + (few.get_left()[0] - few.get_x() + 0.3) * RIGHT,
                      axes.c2p(math.log10(first["leaves"]), first["bias_squared"]), buff=0.12, color=BLUE,
                      stroke_width=4, max_tip_length_to_length_ratio=0.1)
    floor = plated(VGroup(label("a shape trees cannot reach", 26, BLUE, weight=BOLD),
                          label("on these inputs", 26, BLUE, weight=BOLD)).arrange(DOWN, buff=0.08))
    floor.move_to(axes.c2p(math.log10(lowest["leaves"]), 9.5))
    floor_arrow = Arrow(floor.get_bottom(), axes.c2p(math.log10(lowest["leaves"]), lowest["bias_squared"]),
                        buff=0.12, color=BLUE, stroke_width=4, max_tip_length_to_length_ratio=0.15)
    return VGroup(few, few_arrow), VGroup(floor, floor_arrow)


class Scene15(VideoScene):
    number = 15

    def construct(self):
        parts, axes, frame, lines, names, *_ = parts_layout(self)
        heading = title("Bias and variance, measured", 44).to_edge(UP, buff=0.45)
        squared = squared_note(heading)
        few, floor = bias_notes(axes, parts)
        # "Because the survey is simulated, every station's expected count is known, so both can be measured."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.06))
        # "Bias is squared here, multiplied by itself, so that it can be added to the variance."
        cue(self, "Bias is squared")
        self.play(FadeIn(squared), run_time=self.share(0.06))
        # "A tree with few leaves gives very different stations the same prediction, so it misses the pattern."
        cue(self, "A tree with few")
        self.play(FadeIn(few[0]), GrowArrow(few[1]), run_time=self.share(0.07))
        # "More leaves let it follow the pattern, so bias falls."
        cue(self, "More leaves let")
        self.play(Create(lines["bias_squared"]), FadeIn(names["bias_squared"]), run_time=self.share(0.12))
        # "But part of the pattern has a shape that trees cannot reach on these inputs, however finely they
        # split, so bias stops falling."
        cue(self, "But part of")
        self.play(FadeIn(floor[0]), GrowArrow(floor[1]), run_time=self.share(0.07))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        parts, axes, frame, lines, names, *_ = parts_layout(self)
        heading = title("Bias and variance, measured", 44).to_edge(UP, buff=0.45)
        squared = squared_note(heading)
        notes = VGroup(*bias_notes(axes, parts))
        self.add(heading, squared, frame, lines["bias_squared"], names["bias_squared"], notes)
        fewer = plated(VGroup(label("more leaves: fewer stations in each,", 26, VERMILION, weight=BOLD),
                              label("so each leaf's average rests on a few counts", 26, VERMILION, weight=BOLD)
                              ).arrange(DOWN, buff=0.08, aligned_edge=LEFT))
        fewer.next_to(axes.c2p(0.25, 17.5), RIGHT, 0)
        # "Variance works the other way."
        self.play(FadeOut(notes), run_time=self.share(0.06))
        # "A leaf predicts the average count of its stations. More leaves mean fewer stations in each, and an
        # average of a few counts depends on which stations a survey happened to catch."
        cue(self, "More leaves mean")
        self.play(FadeIn(fewer), Create(lines["variance"]), FadeIn(names["variance"]), run_time=self.share(0.2))
        # "So variance keeps rising."
        cue(self, "So variance")
        self.play(Indicate(names["variance"], color=VERMILION), run_time=self.share(0.08))
        # "Their sum is the U."
        cue(self, "Their sum")
        self.play(FadeOut(fewer), TransformFromCopy(VGroup(lines["bias_squared"], lines["variance"]), lines["sum"]),
                  FadeIn(names["sum"]), run_time=self.share(0.1))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        parts, axes, frame, lines, names, noise_line, noise_name, best, best_x = parts_layout(self)
        heading = title("Bias and variance, measured", 44).to_edge(UP, buff=0.45)
        self.add(heading, squared_note(heading), frame, *lines.values(), *names.values())
        # "Under it all lies noise: chance in the counts, which no model removes."
        self.play(FadeIn(noise_line, shift=0.5 * DOWN), FadeIn(noise_name), run_time=self.share(0.15))
        # "For the best tree, noise was 72 per cent of the error."
        cue(self, "For the best tree")
        share = int(parts["noise_share"].iloc[0])
        note = card(f"noise: {share}% of\nthe best tree's error", GREY, 30).move_to(axes.c2p(math.log10(12), 18))
        best_dot = Dot(axes.c2p(best_x, best["bias_squared"] + best["variance"]), radius=0.12, color=GREEN)
        best_name = label("the best tree", 26, GREEN, weight=BOLD).next_to(best_dot, UP, 0.25)
        self.play(FadeIn(best_dot, scale=1.6), FadeIn(best_name), run_time=self.share(0.1))
        self.play(FadeIn(note, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "That is why even the best tree beat predicting the average by so little."
        cue(self, "That is why")
        self.play(Indicate(note, color=GREY), run_time=self.share(0.1))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        both = self.data("tree-and-forest").set_index("model")
        tree, forest = both.loc["single tree"], both.loc["random forest"]
        top = max(tree["variance"], tree["bias_squared"])
        scale = 3.6 / top
        base = Line(5.4 * LEFT, 5.4 * RIGHT, color=GRID, stroke_width=3).shift(2.3 * DOWN)
        heading = title("Averaging trees cuts the variance", 44).to_edge(UP, buff=0.45)

        def bar(value, colour, x):
            rect = Rectangle(width=1.5, height=max(value * scale, 0.01), stroke_width=0, fill_color=colour,
                             fill_opacity=1).next_to(base, UP, 0).set_x(x)
            return VGroup(rect, label(f2(value), 30, colour, weight=BOLD).next_to(rect, UP, 0.15))

        groups = VGroup()
        for name, row, centre in (("one tree", tree, -2.8), ("a random forest of them", forest, 2.8)):
            groups.add(VGroup(bar(row["bias_squared"], BLUE, centre - 0.9), bar(row["variance"], VERMILION, centre + 0.9),
                              label(name, 32, INK, weight=BOLD).next_to(base, DOWN, 0.35).set_x(centre)))
        key = VGroup(
            VGroup(Square(0.3, fill_color=BLUE, fill_opacity=1, stroke_width=0), label("bias²", 28, SUBDUED)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.3, fill_color=VERMILION, fill_opacity=1, stroke_width=0), label("variance", 28, SUBDUED)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6).next_to(heading, DOWN, 0.3)
        # The forest's variance bar starts at the single tree's height and shrinks.
        start = groups[0][1].copy().set_x(groups[1][1].get_x())
        # "This is also why a random forest works."
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(key), FadeIn(base), run_time=self.share(0.1))
        self.play(GrowFromEdge(groups[0][0][0], DOWN), GrowFromEdge(groups[0][1][0], DOWN),
                  FadeIn(groups[0][0][1]), FadeIn(groups[0][1][1]), FadeIn(groups[0][2]), run_time=self.share(0.15))
        # "Averaging many trees keeps their bias, ..."
        cue(self, "Averaging many")
        self.play(FadeIn(groups[1][2]), GrowFromEdge(groups[1][0][0], DOWN), FadeIn(groups[1][0][1]),
                  FadeIn(start), run_time=self.share(0.15))
        # "... but cuts their variance, here about thirteen-fold."
        cue(self, "but cuts")
        self.play(ReplacementTransform(start, groups[1][1]), run_time=self.share(0.15))
        # "Each tree follows its own stations, and their mistakes partly cancel in the average."
        cue(self, "and their mistakes")
        cancel = card("the trees' mistakes\npartly cancel", GREEN, 30).move_to([2.8, 0.6, 0])
        self.play(FadeIn(cancel, scale=0.9), run_time=self.share(0.08))
        self.finish()


class Scene19(KeyPointScene):
    number, point = 19, 2


# Choosing complexity honestly (scenes 20–28) --------------------------------------------------

COEFFICIENTS = np.array([1.9, -1.3, 0.9, 0.35, -1.7, 0.25, -0.5, 1.4])   # made up: a schematic


def coefficient_bars(centre, shrink, weight, width=2.6):
    """The made-up coefficients as bars about a zero line, redrawn as the penalty's weight moves."""
    base = Line(width * LEFT, width * RIGHT, color=GRID, stroke_width=3).move_to(centre)
    xs = np.linspace(-(width - 0.4), width - 0.4, COEFFICIENTS.size)

    def bars():
        group = VGroup()
        for x, c in zip(xs, COEFFICIENTS):
            v = shrink(c, weight.get_value())
            if v == 0:      # a coefficient at exactly zero: an open circle, as in the page's diagram
                group.add(Circle(radius=0.1, color=SUBDUED, stroke_width=3).move_to(base.get_center() + x * RIGHT))
                continue
            group.add(Rectangle(width=0.42, height=abs(v), stroke_width=0, fill_color=BLUE if c > 0 else VERMILION,
                                fill_opacity=1).move_to(base.get_center() + np.array([x, v / 2, 0])))
        return group

    return base, always_redraw(bars)


def ridge(c, w):
    return c / (1 + 3 * w)


def lasso(c, w):
    return float(np.sign(c) * max(abs(c) - 1.1 * w, 0))


def slider_for(weight, width=2.6):
    track = Line(width * LEFT, width * RIGHT, color=GRID, stroke_width=6).to_edge(DOWN, buff=0.8)
    knob = always_redraw(lambda: Dot(track.point_from_proportion(weight.get_value()), radius=0.16, color=INK))
    name = label("the penalty's weight, λ (lambda)", 30, INK).next_to(track, UP, 0.25)
    return VGroup(track, name), knob


class Scene20(VideoScene):
    number = 20

    def construct(self):
        # Schematic: one set of coefficients shrinking as the penalty's weight rises.
        weight = ValueTracker(0)
        base, bars = coefficient_bars(np.array([0, 0.7, 0]), ridge, weight, width=4.0)
        slider, knob = slider_for(weight, 3.0)
        slider.shift(0.3 * DOWN)            # room for the regularisation term above it
        heading = title("A penalty on large coefficients", 46).to_edge(UP, buff=0.5)
        name = label("a linear model's coefficients", 28, SUBDUED).next_to(heading, DOWN, 0.2)
        rule = VGroup(label("loss +", 34, PURPLE, weight=BOLD),
                      label("λ × (size of the coefficients)", 34, PURPLE, weight=BOLD)).arrange(RIGHT, buff=0.18)
        rule.next_to(base, DOWN, 1.95)
        brace = Brace(rule[1], DOWN, buff=0.08, color=PURPLE)
        term = label("the regularisation term: it controls complexity", 26, PURPLE, weight=BOLD).next_to(brace, DOWN, 0.08)
        track = slider[0]
        ends = VGroup(label("λ = 0: no penalty", 26, SUBDUED).next_to(track.get_start(), LEFT, 0.3),
                      label("larger λ: more rigid", 26, SUBDUED).next_to(track.get_end(), RIGHT, 0.3))
        # "Finally, how to choose complexity honestly."
        # "A linear model has its own dial: a penalty, which we met in the last video."
        cue(self, "A linear model")
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(name), FadeIn(base), FadeIn(bars), run_time=self.share(0.1))
        # "The fit is charged for large coefficients, so it keeps them small unless the data clearly need them."
        cue(self, "The fit is charged")
        self.play(FadeIn(rule), run_time=self.share(0.1))
        # "A weight called lambda sets how hard the penalty pulls."
        cue(self, "A weight called")
        self.play(FadeIn(slider), FadeIn(knob), run_time=self.share(0.06))
        # "At zero there is no penalty, and the larger it is, the more rigid the model."
        cue(self, "At zero")
        self.play(FadeIn(ends[0]), run_time=self.share(0.05))
        cue(self, "and the larger")
        self.play(FadeIn(ends[1]), weight.animate.set_value(1), run_time=self.share(0.12), rate_func=smooth)
        # "Lambda times the size of the coefficients is called the regularisation term: it is what controls
        # the model's complexity."
        cue(self, "Lambda times")
        self.play(GrowFromCenter(brace), FadeIn(term), run_time=self.share(0.08))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        # Schematic: the same coefficients under each penalty as its weight rises.
        weight = ValueTracker(0)
        left_base, left_bars = coefficient_bars(np.array([-3.5, -0.5, 0]), ridge, weight)
        right_base, right_bars = coefficient_bars(np.array([3.5, -0.5, 0]), lasso, weight)

        def penalty_shape(f, colour, centre):
            axes = plain_axes([-1, 1, 1], [0, 1, 1], 1.4, 0.8).move_to(centre)
            return VGroup(axes, axes.plot(f, x_range=[-1, 1, 0.02], color=colour, stroke_width=5))

        names = VGroup(
            VGroup(label("ridge regression", 36, INK, weight=BOLD),
                   label("charges the squared coefficients", 26, SUBDUED),
                   penalty_shape(lambda c: c * c, PURPLE, ORIGIN)).arrange(DOWN, buff=0.15).move_to([-3.5, 2.2, 0]),
            VGroup(label("the lasso", 36, INK, weight=BOLD),
                   label("charges their absolute size", 26, SUBDUED),
                   label("(the size without its sign)", 26, SUBDUED),
                   penalty_shape(abs, PURPLE, ORIGIN)).arrange(DOWN, buff=0.15).move_to([3.5, 2.2, 0]))
        names[1].align_to(names[0], DOWN)
        verdicts = VGroup(label("shrinks every one, removes none", 28, BLUE, weight=BOLD).next_to(left_base, DOWN, 1.4),
                          label("sets the small ones to exactly zero", 28, VERMILION, weight=BOLD).next_to(right_base, DOWN, 1.4))
        slider, knob = slider_for(weight, 2.2)
        # "There are two common penalties."
        self.play(FadeIn(left_base), FadeIn(left_bars), FadeIn(right_base), FadeIn(right_bars), FadeIn(slider),
                  FadeIn(knob), run_time=self.share(0.08))
        # "Ridge regression charges the squared coefficients, so it shrinks every one but removes none."
        cue(self, "Ridge regression")
        self.play(FadeIn(names[0]), run_time=self.share(0.08))
        cue(self, "so it shrinks")
        self.play(weight.animate.set_value(0.5), FadeIn(verdicts[0]), run_time=self.share(0.12))
        # "The lasso charges their absolute size, the size without its sign, which makes a small coefficient
        # cheaper to drop than to keep."
        cue(self, "The lasso charges")
        self.play(FadeIn(names[1]), run_time=self.share(0.08))
        # "It sets those to exactly zero, and their inputs leave the model."
        cue(self, "It sets those")
        self.play(weight.animate.set_value(1), FadeIn(verdicts[1]), run_time=self.share(0.15))
        self.finish()


LAMBDA_COLOURS = {"Ridge regression": BLUE, "Lasso": VERMILION}


class Scene22(VideoScene):
    number = 22

    def construct(self):
        curves = self.data("lambda-curves")
        best = self.data("lambda-best").set_index("model")
        all_inputs = best.loc["Linear regression, all inputs", "new"]
        measured = best.loc["Linear regression, measured only", "new"]
        lasso = best.loc["Lasso"]
        lo, hi = -3, 3
        y0 = math.floor(min(curves["new"].min(), measured) * 2) / 2 - 0.5
        y1 = math.ceil(max(curves["new"].max(), all_inputs) * 2) / 2
        # Manim draws each axis through the other's zero, so both run from 0: x is log10(λ) − lo
        # and y is the RMSE − y0, and the tick labels translate back.
        axes, frame = chart([0, hi - lo, 1], [0, y1 - y0, 0.5], 9.0, 4.8, range(0, hi - lo + 1),
                            [v / 2 - y0 for v in range(math.ceil(2 * y0), math.floor(2 * y1) + 1)],
                            "the penalty's weight, λ (log scale)", "error on new sites (RMSE, animals)",
                            x_text=lambda v: f"{10 ** (v + lo):g}", y_text=lambda v: f"{v + y0:.1f}")
        frame.move_to([-0.9, -0.75, 0])

        def at_point(log_lambda, value):
            return axes.c2p(log_lambda - lo, value - y0)

        lines = VGroup()
        for model in ("Ridge regression", "Lasso"):
            c = curves[curves["model"] == model].sort_values("lambda")
            lines.add(VMobject(color=LAMBDA_COLOURS[model], stroke_width=6).set_points_as_corners(
                [at_point(math.log10(l), v) for l, v in zip(c["lambda"], c["new"])]))

        def on_curve(model, log_lambda):
            c = curves[curves["model"] == model]
            row = c.iloc[(np.log10(c["lambda"]) - log_lambda).abs().argmin()]
            return at_point(log_lambda, row["new"])

        names = VGroup(label("ridge regression", 28, BLUE, weight=BOLD).next_to(on_curve("Ridge regression", 0), RIGHT, 0.2),
                       label("lasso", 28, VERMILION, weight=BOLD).next_to(on_curve("Lasso", -1.4), LEFT, 0.2))
        top_line = DashedLine(at_point(lo, all_inputs), at_point(hi, all_inputs), color=INK, stroke_width=4,
                              dash_length=0.12)
        top_name = label(f"linear regression, 200 random columns: {f2(all_inputs)}", 26, INK).next_to(
            at_point(lo, all_inputs), UR, 0.08)
        low_line = DashedLine(at_point(lo, measured), at_point(hi, measured), color=GREEN, stroke_width=4,
                              dash_length=0.12)
        low_name = label(f"told which inputs were measured: {f2(measured)}", 26, GREEN, weight=BOLD).next_to(
            at_point(lo, measured), DR, 0.1)
        best_dot = Dot(at_point(math.log10(lasso["lambda"]), lasso["new"]), radius=0.12, color=VERMILION)
        best_name = label(f"lasso at its best: {f2(lasso['new'])}", 28, VERMILION, weight=BOLD).next_to(
            at_point(hi, measured), DL, 0.1).shift(0.42 * DOWN)
        heading = title("A penalty against 200 random columns", 44).to_edge(UP, buff=0.45)
        # "Here is a test. Give a linear regression 200 extra columns of random numbers: inputs that carry
        # no information at all."
        cue(self, "Give a linear")
        self.play(FadeIn(heading, shift=0.2 * DOWN), FadeIn(frame), run_time=self.share(0.06))
        # "Its error on new sites rises to 6.41, worse than predicting the average."
        cue(self, "Its error on")
        self.play(Create(top_line), FadeIn(top_name), run_time=self.share(0.08))
        # "This chart follows the error as lambda grows."
        cue(self, "This chart")
        self.play(Create(lines[0]), Create(lines[1]), FadeIn(names), run_time=self.share(0.15))
        # "The lasso, at its best lambda, scores 4.55: ..."
        cue(self, "The lasso")
        self.play(FadeIn(best_dot, scale=1.6), FadeIn(best_name), run_time=self.share(0.08))
        # "... as good as a regression told which inputs were measured."
        cue(self, "as good as")
        self.play(Create(low_line), FadeIn(low_name), run_time=self.share(0.12))
        self.finish()


def dial(name, centre):
    track = Line(2.4 * LEFT, 2.4 * RIGHT, color=GRID, stroke_width=8).move_to(centre)
    ends = VGroup(label("simpler", 26, SUBDUED).next_to(track, DOWN, 0.2, aligned_edge=LEFT),
                  label("more flexible", 26, SUBDUED).next_to(track, DOWN, 0.2, aligned_edge=RIGHT))
    knob = Dot(track.get_center(), radius=0.18, color=INK)
    head = label(name, 34, INK, weight=BOLD).next_to(track, UP, 0.3)
    return VGroup(track, ends, head), knob, track


class Scene23(VideoScene):
    number = 23

    def construct(self):
        # Schematic: two settings, and the end training error always picks.
        node, node_knob, node_track = dial("a tree's node size", [-3.4, 0.8, 0])
        penalty, penalty_knob, penalty_track = dial("a regression's penalty, λ", [3.4, 0.8, 0])
        chosen = label("it has to be chosen", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        trap = card("training error always\nfavours the most flexible", VERMILION, 32).move_to([0, -2.2, 0])
        hyper = label("hyperparameters: fixed before fitting", 32, PURPLE, weight=BOLD).move_to([0, -0.55, 0])
        # "A node size, a penalty: every method has a setting like this, a hyperparameter, fixed before fitting."
        self.play(FadeIn(node), FadeIn(node_knob), run_time=self.share(0.08))
        cue(self, "a penalty")
        self.play(FadeIn(penalty), FadeIn(penalty_knob), run_time=self.share(0.08))
        cue(self, "a hyperparameter")
        self.play(FadeIn(hyper), run_time=self.share(0.08))
        # "It has to be chosen, ..."
        cue(self, "It has to")
        self.play(FadeIn(chosen, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "... and not by the training error, which always favours the most flexible setting."
        cue(self, "and not by")
        self.play(node_knob.animate.move_to(node_track.get_end()), penalty_knob.animate.move_to(penalty_track.get_end()),
                  FadeIn(trap, shift=0.2 * UP), run_time=self.share(0.2))
        self.finish()


METHOD_COLOURS = {"One validation split": ORANGE, "Ten-fold cross-validation": BLUE}
METHOD_NAMES = {"One validation split": "one held-back group", "Ten-fold cross-validation": "ten-fold cross-validation"}


def repeats_layout(scene):
    runs = scene.data("repeats")
    lo = math.floor(runs["claimed"].min() * 2) / 2
    hi = math.ceil(runs["claimed"].max() * 2) / 2
    axis = NumberLine(x_range=[lo, hi, 0.5], length=11, color=GRID, include_ticks=False).shift(2.5 * DOWN)
    ticks = VGroup(*[label(f"{v:.1f}", 24, SUBDUED).next_to(axis.n2p(v), DOWN, 0.15)
                     for v in np.arange(lo, hi + 0.01, 0.5)])
    name = label("error claimed for the winner (RMSE, animals)", 26, SUBDUED).next_to(ticks, DOWN, 0.2)
    rows = {}
    for method, y in (("One validation split", 1.5), ("Ten-fold cross-validation", -1.0)):
        claimed = runs.loc[runs["method"] == method, "claimed"].to_numpy()
        dots, seen = VGroup(), {}
        for v in sorted(claimed):
            k = round(v / 0.04)
            level = seen.get(k, 0)
            seen[k] = level + 1
            dots.add(Dot([axis.n2p(k * 0.04)[0], y - 0.45 + 0.15 * level, 0], radius=0.07,
                         color=METHOD_COLOURS[method]))
        low, high = claimed.min(), claimed.max()
        span = Line([axis.n2p(low)[0], y - 0.75, 0], [axis.n2p(high)[0], y - 0.75, 0],
                    color=METHOD_COLOURS[method], stroke_width=5)
        ends = VGroup(label(f2(low), 26, METHOD_COLOURS[method], weight=BOLD).next_to(span, LEFT, 0.15),
                      label(f2(high), 26, METHOD_COLOURS[method], weight=BOLD).next_to(span, RIGHT, 0.15))
        # The cross-validation dots sit left of centre, so its name goes on the right.
        x = -5.6 if method.startswith("One") else 1.4
        head = label(METHOD_NAMES[method], 30, METHOD_COLOURS[method], weight=BOLD).move_to([x, y + 0.3, 0],
                                                                                   aligned_edge=LEFT)
        rows[method] = VGroup(head, dots, span, ends)
    runs_each = int((runs["method"] == "One validation split").sum())
    caption = label(f"{runs_each} repeats, each with different sites held back", 28, SUBDUED).to_edge(UP, buff=0.3)
    return VGroup(axis, ticks, name), rows, caption


class Scene24(VideoScene):
    number = 24

    def construct(self):
        # Schematic: ten folds of sites, each held out in turn.
        rng = np.random.default_rng(26)
        folds = VGroup()
        for _ in range(10):
            sites = VGroup(*[Square(0.22, stroke_width=0, fill_color=FITTING, fill_opacity=1)
                             for _ in range(rng.integers(3, 5))]).arrange(DOWN, buff=0.08)
            box = SurroundingRectangle(sites, color=GRID, buff=0.12, corner_radius=0.08, stroke_width=3)
            folds.add(VGroup(box, sites))
        folds.arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to([0, 0.3, 0])
        names = VGroup(*[label(str(i), 26, SUBDUED).next_to(f, UP, 0.15) for i, f in enumerate(folds, 1)])
        heading = title("Ten-fold cross-validation", 46).to_edge(UP, buff=0.45)
        key = VGroup(
            VGroup(Square(0.3, fill_color=FITTING, fill_opacity=1, stroke_width=0), label("fitted to", 28, SUBDUED)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.3, fill_color=NEW, fill_opacity=1, stroke_width=0), label("new data", 28, SUBDUED)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.7).next_to(folds, DOWN, 0.7)
        errors = VGroup(*[Dot(radius=0.1, color=NEW) for _ in range(10)])
        for d, f in zip(errors, folds):
            d.next_to(f, DOWN, 1.7).set_x(f.get_x())
        average = label("average the ten errors", 32, INK, weight=BOLD).next_to(errors, DOWN, 0.35)
        whole = label("a fold: a group of whole sites", 28, SUBDUED).next_to(heading, DOWN, 0.2)
        keep = label("for every setting; keep the lowest average", 30, PURPLE, weight=BOLD)
        # "Instead, it is chosen by cross-validation."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.05))
        # "Deal the training sites into ten groups, called folds."
        cue(self, "Deal the")
        self.play(LaggedStart(*[FadeIn(f, shift=0.2 * DOWN) for f in folds], lag_ratio=0.1), FadeIn(names),
                  run_time=self.share(0.1))
        # "Each fold holds whole sites, because visits to one site resemble each other."
        cue(self, "Each fold holds")
        self.play(FadeIn(whole), run_time=self.share(0.05))
        # "Each fold takes a turn as new data while the model is fitted to the other nine, ..."
        cue(self, "Each fold takes")
        self.play(FadeIn(key), run_time=self.share(0.03))
        step = self.share(0.02)
        for i, f in enumerate(folds):
            self.play(f[1].animate.set_fill(NEW), *[g[1].animate.set_fill(FITTING) for j, g in enumerate(folds) if j != i],
                      FadeIn(errors[i], shift=0.3 * DOWN), run_time=step)
        self.play(folds[-1][1].animate.set_fill(FITTING), run_time=self.share(0.03))
        # "... and the ten errors are averaged."
        cue(self, "and the ten")
        self.play(FadeIn(average), errors.animate.arrange(RIGHT, buff=0.1).next_to(average, UP, 0.2),
                  run_time=self.share(0.07))
        # "Do this for every setting, and keep the one with the lowest average."
        cue(self, "Do this for")
        keep.next_to(average, DOWN, 0.3)
        self.play(FadeIn(keep, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


class Scene25(VideoScene):
    number = 25

    def construct(self):
        frame, rows, caption = repeats_layout(self)
        one, cv = rows["One validation split"], rows["Ten-fold cross-validation"]
        # "Because every training site takes a turn, the verdict is steady."
        self.play(FadeIn(frame), FadeIn(caption), FadeIn(cv[0]), run_time=self.share(0.08))
        # "Run 20 times with different folds, the error it claimed for its winning setting stayed between
        # 4.45 and 4.64."
        cue(self, "Run 20 times")
        self.play(LaggedStart(*[FadeIn(d, shift=0.3 * DOWN) for d in cv[1]], lag_ratio=0.03),
                  run_time=self.share(0.15))
        cue(self, "stayed between")
        self.play(Create(cv[2]), FadeIn(cv[3]), run_time=self.share(0.08))
        # "Holding back a single group of sites instead gave anything from 3.72 to 5.37."
        cue(self, "Holding back")
        self.play(FadeIn(one[0]), LaggedStart(*[FadeIn(d, shift=0.3 * DOWN) for d in one[1]], lag_ratio=0.03),
                  run_time=self.share(0.12))
        cue(self, "gave anything")
        self.play(Create(one[2]), FadeIn(one[3]), run_time=self.share(0.08))
        self.finish()


def test_box(name="test sites"):
    body = RoundedRectangle(width=3.6, height=2.1, corner_radius=0.15, stroke_color=INK, stroke_width=4,
                            fill_color="#F2F5F7", fill_opacity=1)
    lid = RoundedRectangle(width=3.9, height=0.42, corner_radius=0.1, stroke_color=INK, stroke_width=4,
                           fill_color="#E3E9ED", fill_opacity=1).next_to(body, UP, 0)
    text = label(name, 36, weight=BOLD).move_to(body)
    return VGroup(body, lid, text)


def test_once_layout(scene):
    scores = scene.data("test-once").iloc[0]
    box = test_box().move_to([-4.2, -0.5, 0])
    base = Line([-0.6, -1.9, 0], [-0.6, 1.9, 0], color=GRID, stroke_width=3)
    scale = 6.0 / max(scores["test_lead"], scores["cv_lead"])
    rows = VGroup()
    for i, (text, value, colour) in enumerate((("cross-validation promised", scores["cv_lead"], FITTING),
                                               ("the test sites gave", scores["test_lead"], NEW))):
        y = 0.8 - 1.7 * i
        bar = Rectangle(width=value * scale, height=0.55, stroke_width=0, fill_color=colour, fill_opacity=1
                        ).move_to([-0.6, y, 0], aligned_edge=LEFT)
        rows.add(VGroup(label(text, 28, SUBDUED).next_to(bar, UP, 0.12, aligned_edge=LEFT).shift(0.25 * RIGHT), bar,
                        label(f2(value), 32, colour, weight=BOLD).next_to(bar, RIGHT, 0.15)))
    head = VGroup(label("the chosen tree's lead", 32, INK, weight=BOLD),
                  label("over predicting the average", 32, INK, weight=BOLD)).arrange(DOWN, buff=0.1
                  ).move_to([2.4, 2.9, 0])
    return box, base, rows, head


class Scene26(VideoScene):
    number = 26

    def construct(self):
        box, base, rows, head = test_once_layout(self)
        sealed = label("held back since the start", 26, VERMILION, weight=BOLD).next_to(box, DOWN, 0.25)
        # "Last, the test sites, held back since the very start, score the chosen tree once."
        self.play(FadeIn(box), FadeIn(sealed), run_time=self.share(0.12))
        cue(self, "score the chosen")
        hinge = box[1].get_corner(DL)
        self.play(Rotate(box[1], angle=0.4, about_point=hinge), run_time=self.share(0.08))
        # "It beats predicting the average by 0.28, ..."
        cue(self, "It beats")
        self.play(FadeIn(head), FadeIn(base), run_time=self.share(0.06))
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.1))
        # "... close to the 0.26 that cross-validation promised."
        cue(self, "close to")
        self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]), run_time=self.share(0.1))
        self.finish()


class Scene27(VideoScene):
    number = 27

    def construct(self):
        box, base, rows, head = test_once_layout(self)
        hinge = box[1].get_corner(DL)
        box[1].rotate(0.4, about_point=hinge)
        self.add(box, base, rows, head)
        spent = label("spent", 44, VERMILION, weight=BOLD).rotate(0.25).move_to(box[0])
        again = label("validation sites", 30, VERMILION, weight=BOLD).move_to(box[0])
        warning = card("choose again, and the score\nis no longer honest", VERMILION, 30).move_to([2.6, -2.9, 0])
        # "Then the test sites are spent."
        self.play(FadeOut(box[2]), FadeIn(spent, scale=1.4), run_time=self.share(0.15))
        # "Choose again because the score disappointed, and they become validation sites, ..."
        cue(self, "and they become")
        self.play(ReplacementTransform(spent, again), box[0].animate.set_stroke(VERMILION), run_time=self.share(0.12))
        # "... which can no longer give an honest score."
        cue(self, "which can no")
        self.play(FadeIn(warning, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene28(KeyPointScene):
    number, point = 28, 3


# Quiz (scenes 29–30) ---------------------------------------------------------------------------

class Scene29(QuizScene):
    number = 29
    question = ("A colleague adds ten new columns,",
                "and R² on the training stations goes up.",
                "(R²: the share of the variation explained)",
                "Do the new columns help?")


class Scene30(VideoScene):
    number = 30

    def construct(self):
        rows = self.data("random-columns")
        shown = rows[rows["noise"].round().isin([0, 10, 50, 100, 200])].reset_index(drop=True)
        no = label("No.", 72, VERMILION, weight=BOLD).to_edge(UP, buff=0.5)
        header = ["random columns added", "R² on the training stations", "error on new sites (RMSE)"]
        xs = [-4.5, 0.2, 4.5]
        head = VGroup(*[label(t, 26, SUBDUED, weight=BOLD).move_to([x, 1.6, 0]) for t, x in zip(header, xs)])
        table_rows = VGroup()
        for i, r in shown.iterrows():
            y = 0.9 - 0.68 * i
            table_rows.add(VGroup(label(f"{r['noise']:.0f}", 32).move_to([xs[0], y, 0]),
                                  label(f"{r['r_squared']:.3f}", 32, FITTING).move_to([xs[1], y, 0]),
                                  label(f2(r["new"]), 32, NEW).move_to([xs[2], y, 0])))
        rule = Line([-6, 1.25, 0], [6, 1.25, 0], color=GRID, stroke_width=2)
        ten = SurroundingRectangle(table_rows[:2], color=INK, buff=0.12, corner_radius=0.1)
        ups = VGroup(label("rises", 28, FITTING, weight=BOLD).next_to(table_rows[-1][1], DOWN, 0.3),
                     label("rises", 28, NEW, weight=BOLD).next_to(table_rows[-1][2], DOWN, 0.3))
        tell = label("only new sites can tell", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.4)
        # "No. R squared on the training stations never falls when a column is added, even a column of random numbers."
        self.play(FadeIn(no, scale=1.4), run_time=self.share(0.08))
        self.play(FadeIn(head), Create(rule), run_time=self.share(0.08))
        # "On the survey, ten random columns raised it, ..."
        cue(self, "On the survey")
        self.play(FadeIn(table_rows[:2]), Create(ten), run_time=self.share(0.1))
        # "... and raised the error on new sites from 4.56 to 4.66."
        cue(self, "and raised the error")
        self.play(Indicate(VGroup(table_rows[0][2], table_rows[1][2]), color=NEW), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(r) for r in table_rows[2:]], lag_ratio=0.3), FadeIn(ups),
                  run_time=self.share(0.12))
        # "Only new sites can tell."
        cue(self, "Only new sites")
        self.play(FadeIn(tell, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


# The recap (scenes 31–33) and the end card (scene 34) -------------------------------------

class Scene31(RecapScene):
    number, point = 31, 1


class Scene32(RecapScene):
    number, point = 32, 2


class Scene33(RecapScene):
    number, point = 33, 3


class Scene34(EndCardScene):
    number = 34
