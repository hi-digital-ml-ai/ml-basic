"""Manim scenes for the assumptions video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/06-assumptions-limitations
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is built on three pages of the section, each a model whose good score hides a
problem: the loss decides what a prediction means, a model never says when it is
guessing, and a rare answer fools accuracy. Scenes marked "page results" read
visuals/data/*.csv, which tools/figures-for-video.R writes from the pages. The others
are schematic: made-up shapes, never numbers that could pass for survey results. The
opening, key-point, recap, quiz and end-card scenes are shared (mlbasic_video.py) and
read PROMISES, ANSWERS and RECAP from here. Consecutive scenes about one picture share
a builder, so each starts where the previous one ended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["Why the loss decides what a prediction means",
            "Why a model never says when it is guessing",
            "Why a rare answer fools accuracy"]
ANSWERS = ["For skewed counts, the average\nand the typical catch differ:\na total needs the average",
           "Measure how far each station\nlies from the survey,\non all the inputs at once",
           "Report sensitivity, specificity\nand precision; move the\nthreshold, not the data"]
RECAP = ["The loss decides what a prediction means",
         "A model never says when it is guessing",
         "A rare answer fools accuracy"]

# The pages' colours: the forest on raw counts in blue and on log counts in vermilion,
# anything far from the survey in orange, the rare species in vermilion.
LIGHT = "#C9CED2"


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
          x_text=None, y_text=None):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
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


def polyline(axes, xs, ys, colour, width=6, opacity=1.0):
    return VMobject(color=colour, stroke_width=width, stroke_opacity=opacity).set_points_as_corners(
        [axes.c2p(x, y) for x, y in zip(xs, ys)])


def key_row(colour, text, size=28, shape="dot"):
    mark = Dot(radius=0.13, color=colour) if shape == "dot" else \
        Line(ORIGIN, 0.5 * RIGHT, color=colour, stroke_width=6)
    return VGroup(mark, label(text, size)).arrange(RIGHT, buff=0.2)


def marker(axes, x, top, colour, dash=True):
    """A vertical line at x, from the axis to `top`."""
    start, end = axes.c2p(x, 0), axes.c2p(x, top)
    if dash:
        return DashedLine(start, end, color=colour, stroke_width=5)
    return Line(start, end, color=colour, stroke_width=5)


def percent(x):
    return f"{100 * x:.0f}%"


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("why the loss", "why a model never", "and why a rare"))


class Scene02(VideoScene):
    """Schematic: a good score card, and a magnifying glass that finds a crack behind it."""

    number = 2

    def construct(self):
        box = RoundedRectangle(width=5.0, height=3.2, corner_radius=0.25, stroke_color=GREEN, stroke_width=6,
                               fill_color=BACKGROUND, fill_opacity=1).move_to(0.9 * UP)
        tick = VMobject(color=GREEN, stroke_width=16).set_points_as_corners(
            [[-0.9, 0.0, 0], [-0.25, -0.65, 0], [1.0, 0.75, 0]]).move_to(box).shift(0.3 * UP)
        word = label("a good score", 40, GREEN, weight=BOLD).next_to(tick, DOWN, 0.35)
        card_ = VGroup(box, tick, word)
        crack = VMobject(color=VERMILION, stroke_width=8).set_points_as_corners(
            [[1.6, 2.5, 0], [1.2, 1.8, 0], [1.8, 1.3, 0], [1.3, 0.6, 0], [1.9, 0.0, 0], [1.5, -0.7, 0]])
        glass = VGroup(Circle(0.85, color=INK, stroke_width=8),
                       Line([0.6, -0.6, 0], [1.4, -1.4, 0], color=INK, stroke_width=14)).move_to(5.0 * LEFT + 0.9 * UP)
        hides = label("a good score can hide a problem", 40, VERMILION, weight=BOLD).to_edge(DOWN, buff=1.3)
        assumes = label("knowing what the model assumes reveals it", 34, INK).next_to(hides, DOWN, 0.3)
        # "Each part shows a model with a good score ..."
        self.play(FadeIn(card_, scale=0.9), run_time=self.share(0.15))
        # "... that hides a problem."
        cue(self, "that hides")
        self.play(FadeIn(glass), run_time=self.share(0.05))
        self.play(glass.animate.move_to([1.9, 1.0, 0]), run_time=self.share(0.15))
        self.play(Create(crack), run_time=self.share(0.1))
        # "The score alone never reveals it."
        cue(self, "The score alone")
        self.play(FadeIn(hides, shift=0.2 * UP), run_time=self.share(0.1))
        # "Knowing what the model assumes does."
        cue(self, "Knowing what")
        self.play(FadeIn(assumes, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


# The loss decides what a prediction means (scenes 3–10) -------------------------------------

class Scene03(VideoScene):
    """Schematic: the two checks of a statistics course."""

    number = 3

    def construct(self):
        head = label("Two checks taught in statistics courses", 38, SUBDUED, weight=BOLD).to_edge(UP, buff=0.6)

        def panel(x, heading, picture):
            box = RoundedRectangle(width=5.6, height=4.4, corner_radius=0.2, stroke_color=BLUE, stroke_width=5
                                   ).move_to([x, -0.6, 0])
            words = label(heading, 32, BLUE, weight=BOLD).next_to(box.get_top(), DOWN, 0.35)
            picture.move_to(box.get_center() + 0.4 * DOWN)
            return VGroup(box, words)

        bell_axes = plain_axes([-3, 3, 1], [0, 1.1, 1], 4.2, 2.2)
        bell_line = bell_axes.plot(lambda x: np.exp(-x * x / 2), x_range=[-3, 3], color=INK, stroke_width=6)
        bell = VGroup(bell_axes, bell_line)
        rng = np.random.default_rng(5)
        band_axes = plain_axes([0, 10, 1], [-3, 3, 1], 4.2, 2.2)
        points = VGroup(*[Dot(band_axes.c2p(x, y), radius=0.06, color=INK)
                          for x, y in zip(rng.uniform(0.3, 9.7, 60), rng.normal(0, 0.8, 60))])
        edges = VGroup(DashedLine(band_axes.c2p(0, 1.8), band_axes.c2p(10, 1.8), color=GREY, stroke_width=3),
                       DashedLine(band_axes.c2p(0, -1.8), band_axes.c2p(10, -1.8), color=GREY, stroke_width=3))
        band = VGroup(band_axes, points, edges)
        left = panel(-3.2, "errors: a bell curve", bell)
        right = panel(3.2, "equal spread everywhere", band)
        # "Statistics courses teach two checks before fitting a model."
        cue(self, "Statistics courses")
        self.play(FadeIn(head), run_time=self.share(0.1))
        # "A model's errors should follow a bell curve, the Normal distribution, ..."
        cue(self, "A model's errors")
        self.play(FadeIn(left), FadeIn(bell_axes), run_time=self.share(0.08))
        self.play(Create(bell_line), run_time=self.share(0.12))
        # "... and they should spread equally everywhere."
        cue(self, "and they should")
        self.play(FadeIn(right), FadeIn(band_axes), run_time=self.share(0.06))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in points], lag_ratio=0.02), Create(edges),
                  run_time=self.share(0.14))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        counts = self.data("counts").sort_values("abundance")
        values, stations = counts["abundance"].to_numpy(), counts["stations"].to_numpy()
        total = stations.sum()
        median = values[np.searchsorted(np.cumsum(stations), total / 2)]
        average = (values * stations).sum() / total
        top = np.ceil(stations.max() / 50) * 50
        axes, frame = chart([-1, 41, 10], [0, top, 50], 11.4, 4.6, [0, 10, 20, 30, 40],
                            list(range(0, int(top) + 1, 50)), "animals caught at a station", "stations")
        VGroup(axes, frame).shift(0.2 * RIGHT + 0.6 * DOWN)
        unit = axes.x_length / 42
        bars = VGroup(*[Rectangle(width=unit * 0.85, height=max(n / top * axes.y_length, 0.001), stroke_width=0,
                                  fill_color=BLUE, fill_opacity=0.85).move_to(axes.c2p(v, 0), aligned_edge=DOWN)
                        for v, n in zip(values, stations)])
        empty = label(f"{stations[values == 0][0]} caught nothing", 28, INK, weight=BOLD
                      ).next_to(bars[0], RIGHT, 0.25).align_to(bars[0], UP)
        mid = marker(axes, median, top * 0.7, INK)
        mid_name = VGroup(Line(mid.get_end(), axes.c2p(6.5, top * 0.7), color=INK, stroke_width=3),
                          label(f"median {median:g}", 28, INK, weight=BOLD).next_to(axes.c2p(6.5, top * 0.7), RIGHT, 0.1))
        avg = marker(axes, average, top * 0.55, VERMILION, dash=False)
        avg_name = VGroup(Line(avg.get_end(), axes.c2p(6.5, top * 0.55), color=VERMILION, stroke_width=3),
                          label(f"average {average:.1f}", 28, VERMILION, weight=BOLD
                                ).next_to(axes.c2p(6.5, top * 0.55), RIGHT, 0.1))
        largest = label(f"largest {values.max():g}", 28, INK, weight=BOLD).next_to(axes.c2p(values.max(), 0), UP, 0.35)
        tail = Arrow(axes.c2p(12, top * 0.3), axes.c2p(36, top * 0.3), color=ORANGE, stroke_width=6, buff=0)
        tail_name = label("skew: a long tail of big catches", 30, ORANGE, weight=BOLD).next_to(tail, UP, 0.15)
        head = label(f"The {total} training stations", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.35)
        # "Counts of animals fail both. Of 598 stations, 129 caught nothing, ..."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.06))
        cue(self, "Of 598")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=self.share(0.12))
        cue(self, "129 caught")
        self.play(FadeIn(empty, shift=0.2 * LEFT), Indicate(bars[0], color=BLUE), run_time=self.share(0.06))
        # "... the middle station caught 3, ..."
        cue(self, "the middle station")
        self.play(Create(mid), FadeIn(mid_name), run_time=self.share(0.06))
        # "... and the largest 40."
        cue(self, "and the largest")
        self.play(FadeIn(largest, shift=0.2 * DOWN), run_time=self.share(0.05))
        # "A long tail like this is called skew."
        cue(self, "A long tail")
        self.play(GrowArrow(tail), FadeIn(tail_name), run_time=self.share(0.08))
        # "The few big catches pull the average up to 4.0, above the middle catch, the median."
        cue(self, "The few big")
        self.play(Create(avg), FadeIn(avg_name), run_time=self.share(0.08))
        self.play(Indicate(avg_name, color=VERMILION), run_time=self.share(0.06))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        errors = self.data("errors")
        spread = self.data("spread").sort_values("fifth")
        x_top = np.ceil(errors["predicted"].max() / 4) * 4
        y_lo, y_hi = np.floor(errors["error"].min() / 10) * 10, np.ceil(errors["error"].max() / 10) * 10
        axes, frame = chart([0, x_top, 4], [y_lo, y_hi, 10], 8.2, 4.8, list(range(0, int(x_top) + 1, 4)),
                            list(range(int(y_lo), int(y_hi) + 1, 10)), "the forest's prediction",
                            "error: caught − predicted")
        VGroup(axes, frame).shift(1.9 * LEFT + 0.4 * DOWN)
        zero = Line(axes.c2p(0, 0), axes.c2p(x_top, 0), color=GREY, stroke_width=3)
        dots = VGroup(*[Dot(axes.c2p(p, e), radius=0.035, color=INK).set_opacity(0.45)
                        for p, e in zip(errors["predicted"], errors["error"])])
        above = VGroup(*[d for d, e in zip(dots, errors["error"]) if e > 8])
        bands = VGroup()
        for side_, (_, row) in zip((DOWN, UP), spread.iloc[[0, -1]].iterrows()):
            lo, hi = row["predicted_from"], min(row["predicted_to"], x_top)
            rect = Rectangle(width=axes.c2p(hi, 0)[0] - axes.c2p(lo, 0)[0],
                             height=axes.c2p(0, row["error_sd"])[1] - axes.c2p(0, -row["error_sd"])[1],
                             stroke_width=0, fill_color=BLUE, fill_opacity=0.25
                             ).move_to(axes.c2p(lo, -row["error_sd"]), aligned_edge=DL)
            bands.add(VGroup(rect, plated(label(f"spread {row['error_sd']:.1f}", 26, BLUE, weight=BOLD)
                                          ).next_to(rect, side_, 0.1).shift((0.5 if side_ is DOWN else 0) * RIGHT)))
        ratio = spread["error_sd"].iloc[-1] / spread["error_sd"].iloc[0]
        notes = VGroup(label("lopsided: a few", 28, INK, weight=BOLD),
                       label("far above", 28, INK, weight=BOLD)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        wider = label(f"{ratio:.1f} times as wide", 30, BLUE, weight=BOLD)
        fine = VGroup(label("the forest", 30, GREEN, weight=BOLD),
                      label("predicts well anyway", 30, GREEN, weight=BOLD)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        why = VGroup(label("a tree predicts the", 26, INK), label("average catch of", 26, INK),
                     label("similar stations:", 26, INK), label("no bell curve needed", 26, INK, weight=BOLD)
                     ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        side = VGroup(notes, wider, fine, why).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        side.move_to(5.1 * RIGHT + 0.2 * DOWN)
        head = label("The random forest's errors, on sites it never saw", 30, SUBDUED, weight=BOLD
                     ).to_edge(UP, buff=0.3)
        # "A random forest's errors fail both checks too."
        self.play(FadeIn(frame), FadeIn(head), Create(zero), run_time=self.share(0.08))
        self.play(FadeIn(dots, lag_ratio=0.002), run_time=self.share(0.12))
        # "They are lopsided, ..."
        cue(self, "They are lopsided")
        self.play(Indicate(above, color=VERMILION, scale_factor=1.5), FadeIn(notes), run_time=self.share(0.08))
        # "... and they spread 4.3 times wider where it predicts the most."
        cue(self, "and they spread")
        self.play(FadeIn(bands[0]), run_time=self.share(0.06))
        self.play(FadeIn(bands[1]), FadeIn(wider), run_time=self.share(0.08))
        # "Yet the forest predicts well."
        cue(self, "Yet the forest")
        self.play(FadeIn(fine, shift=0.2 * UP), run_time=self.share(0.06))
        # "A tree predicts the average catch of similar stations, and an average needs no bell curve."
        cue(self, "A tree predicts")
        self.play(FadeIn(why, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


def middles_layout(scene):
    """A schematic skewed histogram, with its median, average and 95% point, for scenes 6, 7 and 9."""
    ks = np.arange(0, 31)
    weights = np.exp(-(np.log(ks + 0.5) - 1.0) ** 2 / 2) / (ks + 0.5)
    weights /= weights.sum()
    cumulative = np.cumsum(weights)
    median = ks[np.searchsorted(cumulative, 0.5)] + 0.5
    average = (weights * (ks + 0.5)).sum()
    q95 = ks[np.searchsorted(cumulative, 0.95)] + 0.5
    top = weights.max() * 1.15
    axes = plain_axes([0, 31, 1], [0, top, top], 10.0, 3.8).shift(1.0 * RIGHT + 0.9 * DOWN)
    x_name = label("animals a station could catch", 26, SUBDUED).next_to(axes, DOWN, 0.2)
    unit = axes.x_length / 31
    bars = VGroup(*[Rectangle(width=unit * 0.9, height=w / top * axes.y_length, stroke_width=0, fill_color=BLUE,
                              fill_opacity=0.8).move_to(axes.c2p(k + 0.5, 0), aligned_edge=DOWN)
                    for k, w in zip(ks, weights)])
    lines = {"median": marker(axes, median, top * 0.95, INK),
             "average": marker(axes, average, top * 0.95, VERMILION, dash=False),
             "q95": marker(axes, q95, top * 0.6, PURPLE)}
    return axes, VGroup(axes, x_name), bars, lines, weights


class Scene06(VideoScene):
    number = 6

    def construct(self):
        axes, frame, bars, lines, _ = middles_layout(self)
        head = VGroup(label("a prediction: one number for all", 32, SUBDUED, weight=BOLD),
                      label("the catches a station could give", 32, SUBDUED, weight=BOLD)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.35)
        squared = plated(VGroup(label("squared error:", 26, VERMILION, weight=BOLD),
                                label("the average", 26, VERMILION, weight=BOLD)).arrange(DOWN, buff=0.05)
                         ).next_to(lines["average"], UP, 0.1).shift(1.0 * RIGHT)
        absolute = plated(VGroup(label("absolute error:", 26, INK, weight=BOLD),
                                 label("the median", 26, INK, weight=BOLD)).arrange(DOWN, buff=0.05)
                          ).next_to(lines["median"], UP, 0.1).shift(1.1 * LEFT)
        quantile = plated(VGroup(label("a quantile loss:", 26, PURPLE, weight=BOLD),
                                 label("any point you choose", 26, PURPLE, weight=BOLD)).arrange(DOWN, buff=0.05)
                          ).next_to(lines["q95"], UP, 0.1)
        cut = lines["q95"].get_center()[0]
        tail = VGroup(*[b for b in bars if b.get_center()[0] > cut])
        exceed = label("only 1 in 20 beyond", 26, PURPLE).next_to(quantile, RIGHT, 0.3).shift(0.3 * DOWN)
        # "So what does the shape change? What a prediction means."
        self.play(FadeIn(frame), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03),
                  run_time=self.share(0.12))
        # "A prediction is one number standing for all the catches a station could give, ..."
        cue(self, "A prediction is")
        self.play(FadeIn(head), run_time=self.share(0.08))
        # "Squared error aims at the average."
        cue(self, "Squared error aims")
        self.play(Create(lines["average"]), FadeIn(squared), run_time=self.share(0.08))
        # "Absolute error aims at the median."
        cue(self, "Absolute error aims")
        self.play(Create(lines["median"]), FadeIn(absolute), run_time=self.share(0.08))
        # "And a quantile loss aims at any point you choose, ..."
        cue(self, "And a quantile")
        self.play(Create(lines["q95"]), FadeIn(quantile), run_time=self.share(0.08))
        # "... such as the catch only 1 in 20 stations exceed."
        cue(self, "such as the")
        self.play(tail.animate.set_fill(PURPLE), FadeIn(exceed), run_time=self.share(0.08))
        self.finish()


class Scene07(VideoScene):
    """Schematic: taking logs squeezes the long tail into something more bell-shaped."""

    number = 7

    def construct(self):
        axes, frame, bars, _, weights = middles_layout(self)
        name = label("the counts", 30, BLUE, weight=BOLD).to_edge(UP, buff=0.5)
        log_name = label("the log of the counts", 30, BLUE, weight=BOLD).move_to(name)
        # On the log scale the same stations make a rough bell: each bar keeps its place in
        # the order and takes the bell's height there (schematic).
        bell = np.exp(-((np.arange(len(weights)) - 13) / 5.5) ** 2 / 2)
        bell *= weights.max() * 0.75 / bell.max()
        scale_top = weights.max() * 1.15
        targets = VGroup(*[b.copy().stretch_to_fit_height(max(h / scale_top * axes.y_length, 0.01)
                                                          ).align_to(axes.c2p(0, 0), DOWN)
                           for b, h in zip(bars, bell)])
        habit = label("a common habit for skewed counts", 30, SUBDUED).next_to(name, DOWN, 0.2)
        second = VGroup(label("forest 2: fitted to log counts,", 30, VERMILION, weight=BOLD),
                        label("its predictions turned back into animals", 30, VERMILION, weight=BOLD)
                        ).arrange(DOWN, buff=0.08).next_to(name, DOWN, 0.3)
        # "Now a common habit. Skewed counts are often turned into their logarithm before fitting, ..."
        self.play(FadeIn(axes), FadeIn(bars), FadeIn(name), run_time=self.share(0.08))
        cue(self, "Skewed counts")
        self.play(FadeIn(habit), run_time=self.share(0.06))
        # "... which squeezes the long tail into something more bell-shaped."
        cue(self, "which squeezes")
        self.play(Transform(bars, targets), FadeOut(name), FadeIn(log_name), run_time=self.share(0.25))
        # "Fit a second forest to the log counts, and turn its predictions back into animals."
        cue(self, "Fit a second")
        self.play(FadeOut(habit), FadeIn(second, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        totals = self.data("totals").set_index("model")
        raw, logged = totals.loc["Random forest"], totals.loc["Random forest on log counts"]
        caught = raw["caught_total"]
        top = np.ceil(max(caught, raw["predicted_total"]) / 500) * 500
        axes, frame = chart([0, top, 500], [0, 3, 1], 7.4, 3.4, list(range(0, int(top) + 1, 500)), [],
                            None, None, x_text=lambda v: f"{v:,.0f}")
        VGroup(axes, frame).shift(2.2 * RIGHT + 1.0 * DOWN)

        def row(value, y, colour, name):
            bar = Rectangle(width=value / top * axes.x_length, height=0.6, stroke_width=0, fill_color=colour,
                            fill_opacity=1).move_to(axes.c2p(0, y), aligned_edge=LEFT)
            number = label(f"{value:,.0f}", 30, colour, weight=BOLD).next_to(bar, RIGHT, 0.2)
            words = label(name, 30, colour, weight=BOLD).next_to(axes.c2p(0, y), LEFT, 0.3)
            return VGroup(bar, number, words)

        rows = [row(caught, 2.5, INK, "caught"),
                row(raw["predicted_total"], 1.5, BLUE, "forest on raw counts"),
                row(logged["predicted_total"], 0.5, VERMILION, "forest on log counts")]
        scores = VGroup(*[VGroup(label(name, 28, colour, weight=BOLD),
                                 label(f"RMSE {r['rmse']:.2f}", 40, colour, weight=BOLD)).arrange(DOWN, buff=0.1)
                          for name, colour, r in (("forest on raw counts", BLUE, raw),
                                                  ("forest on log counts", VERMILION, logged))]
                        ).arrange(RIGHT, buff=1.6).to_edge(UP, buff=0.4)
        same = label("almost the same", 30, SUBDUED).next_to(scores, DOWN, 0.2)
        short = 1 - logged["predicted_total"] / caught
        gap = label(f"{100 * short:.0f}% short", 34, VERMILION, weight=BOLD).next_to(rows[2][1], RIGHT, 0.35)
        added = label("animals, added up over the stations", 28, SUBDUED).next_to(frame, DOWN, 0.2)
        # "The two forests score almost the same RMSE, 4.69 and 4.78."
        self.play(FadeIn(scores[0]), run_time=self.share(0.08))
        self.play(FadeIn(scores[1]), run_time=self.share(0.08))
        cue(self, "4.69")
        self.play(FadeIn(same), run_time=self.share(0.05))
        # "Now add up their predictions. The stations caught 2,421 animals."
        cue(self, "Now add up")
        self.play(FadeIn(frame), FadeIn(added), run_time=self.share(0.06))
        cue(self, "The stations caught")
        self.play(FadeIn(rows[0][2]), GrowFromEdge(rows[0][0], LEFT), FadeIn(rows[0][1]), run_time=self.share(0.08))
        # "The forest on raw counts predicts 2,514."
        cue(self, "The forest on raw")
        self.play(FadeIn(rows[1][2]), GrowFromEdge(rows[1][0], LEFT), FadeIn(rows[1][1]), run_time=self.share(0.08))
        # "The forest on log counts predicts 1,699: 30 per cent short."
        cue(self, "The forest on log")
        self.play(FadeIn(rows[2][2]), GrowFromEdge(rows[2][0], LEFT), FadeIn(rows[2][1]), run_time=self.share(0.08))
        cue(self, "per cent short")
        self.play(FadeIn(gap, shift=0.2 * LEFT), run_time=self.share(0.06))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        axes, frame, bars, lines, _ = middles_layout(self)
        self.add(frame, bars)
        aims = plated(VGroup(label("forest on log counts:", 26, INK, weight=BOLD),
                             label("near the median", 26, INK, weight=BOLD)).arrange(DOWN, buff=0.05)
                      ).next_to(lines["median"], UP, 0.1).shift(1.6 * LEFT)
        needs = plated(VGroup(label("a total", 26, VERMILION, weight=BOLD),
                              label("needs the average", 26, VERMILION, weight=BOLD)).arrange(DOWN, buff=0.05)
                       ).next_to(lines["average"], UP, 0.1).shift(1.3 * RIGHT)
        log_scale = label("on the log scale: the average log count", 30, SUBDUED).to_edge(UP, buff=0.5)
        back = label("turned back into animals: near the typical catch", 30, INK, weight=BOLD
                     ).next_to(log_scale, DOWN, 0.2)
        advice = VGroup(label("when totals matter:", 30, INK),
                        label("keep the counts, or use a loss for counts (Poisson deviance)", 30, GREEN,
                              weight=BOLD)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.5)
        # "Why? On the log scale, squared error aims at the average log count, ..."
        cue(self, "On the log")
        self.play(FadeIn(log_scale), run_time=self.share(0.08))
        # "... and turned back into animals, that lands near the median, the typical catch."
        cue(self, "and turned back")
        self.play(FadeIn(back), Create(lines["median"]), FadeIn(aims), run_time=self.share(0.1))
        # "A stock estimate needs the average."
        cue(self, "A stock estimate")
        self.play(Create(lines["average"]), FadeIn(needs), run_time=self.share(0.08))
        # "So when totals matter, keep the counts as they are, or use a loss made for counts, ..."
        cue(self, "So when totals")
        self.play(FadeOut(VGroup(log_scale, back)), FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene10(KeyPointScene):
    number, point = 10, 1


# A model never says when it is guessing (scenes 11–17) --------------------------------------

class Scene11(VideoScene):
    """Schematic: a station outside the survey's range is easy to spot; one inside is not."""

    number = 11

    def construct(self):
        line = NumberLine(x_range=[0, 10, 1], length=11, color=GRID, stroke_width=4, include_ticks=False
                          ).shift(0.4 * DOWN)
        name = label("one input, such as depth", 28, SUBDUED).next_to(line, DOWN, 0.3)
        lo, hi = line.n2p(1.0), line.n2p(6.0)
        survey = Rectangle(width=hi[0] - lo[0], height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.25
                           ).move_to((lo + hi) / 2)
        survey_name = label("the survey's range", 28, BLUE, weight=BOLD).next_to(survey, DOWN, 0.6)
        rng = np.random.default_rng(9)
        stations = VGroup(*[Dot(line.n2p(v), radius=0.08, color=BLUE) for v in rng.uniform(1.0, 6.0, 25)])
        outside = Dot(line.n2p(8.6), radius=0.15, color=ORANGE)
        outside_name = VGroup(label("outside the range:", 28, ORANGE, weight=BOLD),
                              label("easy to spot", 28, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.06
                                                                                     ).next_to(outside, UP, 0.4)
        inside = Dot(line.n2p(3.3), radius=0.15, color=PURPLE)
        inside_name = label("inside every range: is it safe?", 32, PURPLE, weight=BOLD).move_to(1.9 * UP + 2.0 * LEFT)
        pointer = Arrow(inside_name.get_bottom(), inside.get_top() + 0.1 * UP, color=PURPLE, stroke_width=5, buff=0.15)
        rule = label("past the data, each model follows its own rule", 28, SUBDUED).to_edge(DOWN, buff=0.6)
        # "Survey effort is uneven: it follows ports, weather and ship time."
        cue(self, "Survey effort")
        self.play(Create(line), FadeIn(name), run_time=self.share(0.06))
        self.play(FadeIn(survey), FadeIn(survey_name), LaggedStart(*[FadeIn(s) for s in stations], lag_ratio=0.05),
                  run_time=self.share(0.1))
        # "As the Supervised learning video showed, past the data each model follows its own rule."
        cue(self, "As the Supervised")
        self.play(FadeIn(rule), run_time=self.share(0.06))
        # "A station outside the survey's range is easy to spot."
        cue(self, "A station outside")
        self.play(FadeIn(outside, scale=1.6), FadeIn(outside_name), run_time=self.share(0.08))
        # "The hard case is a station inside every range."
        cue(self, "The hard case")
        self.play(FadeIn(inside, scale=1.6), FadeIn(inside_name), GrowArrow(pointer), run_time=self.share(0.1))
        self.finish()


NOVELTY_COLOURS = {"Surveyed": LIGHT, "Close to surveyed stations": SKY, "Outside a range": BLUE,
                   "Inside every range, far from the survey": ORANGE}


def novelty_layout(scene):
    """The summer and autumn survey by depth and temperature, and the winter stations, for scenes 12–13."""
    stations = scene.data("novelty")
    depth, temp = stations["depth_m"], stations["temperature_c"]
    axes, frame = chart([0, 200, 50], [0, 20, 5], 7.0, 4.8, [0, 50, 100, 150, 200], [0, 5, 10, 15, 20],
                        "depth (m)", "temperature (°C)")
    VGroup(axes, frame).shift(2.6 * LEFT + 0.4 * DOWN)
    rows = (stations["status"] == "Surveyed") & depth.notna() & temp.notna()
    surveyed_dots = VGroup(*[Dot(axes.c2p(d, t), radius=0.045, color=LIGHT) for d, t in zip(depth[rows], temp[rows])])
    surveyed = stations[stations["status"] == "Surveyed"]
    corner = axes.c2p(surveyed["depth_m"].min(), surveyed["temperature_c"].min())
    far = axes.c2p(surveyed["depth_m"].max(), surveyed["temperature_c"].max())
    box = DashedVMobject(Rectangle(width=far[0] - corner[0], height=far[1] - corner[1], color=INK,
                                   stroke_width=3).move_to((corner + far) / 2), num_dashes=70)
    box_name = label("the survey's range of each", 24, INK).next_to(box, UP, 0.08)
    winter = stations[(stations["status"] == "Inside every range, far from the survey")
                      & (stations["season"] == "winter")]
    winter_dots = VGroup(*[Dot(axes.c2p(d, t), radius=0.07, color=ORANGE)
                           for d, t in zip(winter["depth_m"], winter["temperature_c"])])
    head = label("A survey in summer and autumn", 28, SUBDUED, weight=BOLD).move_to([1.0, 2.9, 0], aligned_edge=LEFT)
    return frame, surveyed_dots, VGroup(box, box_name), winter_dots, axes, surveyed, head


class Scene12(VideoScene):
    number = 12

    def construct(self):
        frame, dots, box, winter, axes, surveyed, head = novelty_layout(self)
        key = key_row(LIGHT, "surveyed station").next_to(head, DOWN, 0.4, aligned_edge=LEFT)
        # "Here is a survey that sailed only in summer and autumn."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.12))
        # "Each dot is a station, placed by its depth and its temperature."
        cue(self, "Each dot is")
        self.play(FadeIn(key), FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.2))
        # "In those seasons the shallows are warm, so the survey met cold water only at depth."
        cue(self, "so the survey met")
        cold = surveyed["temperature_c"] < 8
        cold_zone = Rectangle(width=axes.c2p(200, 0)[0] - axes.c2p(surveyed["depth_m"][cold].min(), 0)[0],
                              height=axes.c2p(0, 8)[1] - axes.c2p(0, 0)[1], stroke_color=BLUE, stroke_width=4,
                              fill_color=BLUE, fill_opacity=0.08
                              ).move_to(axes.c2p(surveyed["depth_m"][cold].min(), 0), aligned_edge=DL)
        cold_name = label("cold water: only at depth", 28, BLUE, weight=BOLD).next_to(key, DOWN, 0.4,
                                                                                       aligned_edge=LEFT)
        self.play(Create(cold_zone), FadeIn(cold_name), run_time=self.share(0.2))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        frame, dots, box, winter, axes, surveyed, head = novelty_layout(self)
        key = VGroup(key_row(LIGHT, "surveyed station"), key_row(ORANGE, "winter station")
                     ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(head, DOWN, 0.4, aligned_edge=LEFT)
        self.add(frame, dots, head, key[0])
        seen = VGroup(label("its depth: seen", 30, INK, weight=BOLD),
                      label("its temperature: seen", 30, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(key, DOWN, 0.6, aligned_edge=LEFT)
        never = label("but never together", 30, ORANGE, weight=BOLD).next_to(seen, DOWN, 0.15, aligned_edge=LEFT)
        alone = label("nothing like it to learn from", 30, VERMILION, weight=BOLD
                      ).next_to(never, DOWN, 0.5, aligned_edge=LEFT)
        # "Then the model is asked about winter, when the shallows turn cold."
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in winter], lag_ratio=0.01), FadeIn(key[1]),
                  run_time=self.share(0.25))
        # "Each winter station's depth was seen, and so was its temperature, ..."
        cue(self, "Each winter")
        self.play(Create(box[0]), FadeIn(box[1]), FadeIn(seen[0]), run_time=self.share(0.12))
        cue(self, "and so was")
        self.play(FadeIn(seen[1]), run_time=self.share(0.06))
        # "... but never together."
        cue(self, "but never")
        self.play(FadeIn(never), Indicate(winter, color=ORANGE, scale_factor=1.4), run_time=self.share(0.1))
        # "The forest has no stations like these to learn from."
        cue(self, "The forest has")
        self.play(FadeIn(alone, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        check = self.data("range-check").iloc[0]
        n, passed, hidden = int(check["stations"]), int(check["in_range"]), int(check["hidden"])
        squares = VGroup(*[Square(0.17, stroke_width=0, fill_color=LIGHT, fill_opacity=1) for _ in range(n)]
                         ).arrange_in_grid(cols=29, buff=0.05).move_to(2.8 * LEFT + 0.3 * DOWN)
        head = label("The range check: one input at a time", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.5)
        rows = VGroup(key_row(LIGHT, f"{n} spring and winter stations", 30),
                      key_row(BLUE, f"{passed} pass on every input", 30),
                      key_row(ORANGE, f"{hidden} of those: far from", 30)
                      ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(4.0 * RIGHT + 0.6 * UP)
        more = label("every surveyed station", 30).next_to(rows[2][1], DOWN, 0.08, aligned_edge=LEFT)
        share = label(f"{percent(hidden / passed)} of those that pass", 34, ORANGE, weight=BOLD
                      ).next_to(more, DOWN, 0.5).align_to(rows, LEFT)
        # "The usual check takes one input at a time."
        self.play(FadeIn(head), run_time=self.share(0.1))
        # "Of 406 spring and winter stations, 279 pass it on every input."
        cue(self, "Of 406")
        self.play(FadeIn(squares, lag_ratio=0.002), FadeIn(rows[0]), run_time=self.share(0.12))
        cue(self, "279 pass")
        self.play(*[squares[k].animate.set_fill(BLUE) for k in range(passed)], FadeIn(rows[1]),
                  run_time=self.share(0.12))
        # "Yet 132 of those, almost half, lie far from every surveyed station."
        cue(self, "Yet 132")
        self.play(*[squares[k].animate.set_fill(ORANGE) for k in range(hidden)], FadeIn(rows[2]), FadeIn(more),
                  run_time=self.share(0.14))
        cue(self, "almost half")
        self.play(FadeIn(share, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene15(VideoScene):
    """Schematic: distance to the nearest surveyed station across all the inputs at once."""

    number = 15

    def construct(self):
        rng = np.random.default_rng(28)
        axes = plain_axes([-3, 3, 1], [-3, 3, 1], 5.6, 5.0).shift(2.6 * LEFT + 0.4 * DOWN)
        xl = label("depth", 26, SUBDUED).next_to(axes, DOWN, 0.2)
        yl = label("temperature", 26, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.2)
        cloud = rng.multivariate_normal([0, 0], [[1.4, -1.1], [-1.1, 1.2]], 70)
        cloud = cloud[(np.abs(cloud) < 2.7).all(axis=1)]
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.07, color=LIGHT) for x, y in cloud])
        new = np.array([-1.6, -1.6])
        nearest = cloud[np.argmin(np.hypot(*(cloud - new).T))]
        station = Dot(axes.c2p(*new), radius=0.13, color=ORANGE)
        link = Line(axes.c2p(*new), axes.c2p(*nearest), color=ORANGE, stroke_width=6)
        near_dot = Dot(axes.c2p(*nearest), radius=0.1, color=INK)
        words = VGroup(label("distance to the nearest", 34, ORANGE, weight=BOLD),
                       label("surveyed station", 34, ORANGE, weight=BOLD),
                       label("on all the inputs at once", 28, SUBDUED)
                       ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(3.6 * RIGHT + 1.4 * UP)
        knn = VGroup(label("as k-nearest neighbours", 28, INK),
                     label("finds its neighbours", 28, INK)).arrange(DOWN, buff=0.08, aligned_edge=LEFT
                                                                     ).next_to(words, DOWN, 0.45, aligned_edge=LEFT)
        alone = VGroup(label("far from every one:", 30, VERMILION, weight=BOLD),
                       label("the model is on its own", 30, VERMILION, weight=BOLD)
                       ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(knn, DOWN, 0.5, aligned_edge=LEFT)
        # "A better check looks at all the inputs at once: ..."
        self.play(FadeIn(axes), FadeIn(xl), FadeIn(yl), FadeIn(dots), run_time=self.share(0.1))
        self.play(FadeIn(station, scale=1.6), run_time=self.share(0.05))
        # "... the distance from each station to the nearest surveyed station, ..."
        cue(self, "the distance from")
        self.play(Create(link), FadeIn(near_dot), FadeIn(words), run_time=self.share(0.15))
        # "... the same distance k-nearest neighbours uses to find its neighbours."
        cue(self, "the same distance")
        self.play(FadeIn(knn), run_time=self.share(0.08))
        # "Far from every surveyed station means the model is on its own."
        cue(self, "Far from every")
        self.play(FadeIn(alone, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        quarters = self.data("by-distance").sort_values("quarter")
        off = quarters["typical factor off"]
        top = np.ceil(off.max())
        axes, frame = chart([0, 4, 1], [0, top, 1], 8, 4.0, [], list(range(0, int(top) + 1)),
                            None, "typical factor off")
        VGroup(axes, frame).shift(1.6 * LEFT + 0.6 * DOWN)
        names = ["nearest", "second", "third", "furthest"]
        bars = VGroup()
        for k, (value, name) in enumerate(zip(off, names)):
            bar = Rectangle(width=1.2, height=value / top * axes.y_length, stroke_width=0,
                            fill_color=interpolate_color(ManimColor(SKY), ManimColor(ORANGE), k / 3), fill_opacity=1
                            ).move_to(axes.c2p(k + 0.5, 0), aligned_edge=DOWN)
            bars.add(VGroup(bar, label(f"{value:.1f}", 30, INK, weight=BOLD).next_to(bar, UP, 0.1),
                            label(name, 26, SUBDUED).next_to(axes.c2p(k + 0.5, 0), DOWN, 0.2)))
        x_name = label("quarter of stations, by distance from the survey", 26, SUBDUED).next_to(bars, DOWN, 0.3)
        head = label("The random forest's error, against the truth", 34, SUBDUED).to_edge(UP, buff=0.5)
        factor = VGroup(label("off by a factor of 2:", 28, INK, weight=BOLD),
                        label("twice the truth, or half", 28, SUBDUED)
                        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(4.6 * RIGHT + 2.0 * UP)
        advice = VGroup(label("map the distance", 32, BLUE, weight=BOLD),
                        label("beside the predictions", 32, BLUE, weight=BOLD)
                        ).arrange(DOWN, buff=0.12).move_to(4.6 * RIGHT + 0.2 * DOWN)
        # "And it works. Because the survey is simulated, the forest can be checked against the truth."
        self.play(FadeIn(head), FadeIn(frame), FadeIn(x_name), run_time=self.share(0.1))
        # "Its error is the factor it is off by, so twice the truth or half of it is a factor of 2."
        cue(self, "Its error is")
        self.play(FadeIn(factor, shift=0.2 * LEFT), run_time=self.share(0.08))
        # "Nearest the survey, it was typically off by 1.4; ..."
        cue(self, "Nearest the survey")
        self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), run_time=self.share(0.06))
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1:])) for b in bars[1:3]],
                              lag_ratio=0.4), run_time=self.share(0.08))
        # "... furthest away, by 2.7."
        cue(self, "furthest away")
        self.play(GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1:]), run_time=self.share(0.06))
        # "So map the distance beside the predictions, to show where the model is guessing."
        cue(self, "So map")
        self.play(FadeIn(advice, shift=0.2 * LEFT), run_time=self.share(0.12))
        self.finish()


class Scene17(KeyPointScene):
    number, point = 17, 2


# A rare answer fools accuracy (scenes 18–25) ------------------------------------------------

def rare_grid(scene):
    """The training stations as dots, the ones with the rare species picked out, for scenes 18–19."""
    rare = scene.data("rare").iloc[0]
    n, present = int(rare["stations"]), int(rare["present"])
    dots = VGroup(*[Dot(radius=0.065, color=LIGHT) for _ in range(n)]).arrange_in_grid(cols=26, buff=0.09)
    dots.move_to(3.2 * LEFT + 0.3 * DOWN)
    picks = np.random.default_rng(3).choice(n, present, replace=False)
    lit = VGroup(*[dots[k] for k in picks])
    return rare, dots, lit


class Scene18(VideoScene):
    number = 18

    def construct(self):
        rare, dots, lit = rare_grid(self)
        examples = VGroup(label("a protected species", 34, INK, weight=BOLD),
                          label("a harmful algal bloom", 34, INK, weight=BOLD)
                          ).arrange(DOWN, buff=0.2).move_to(0.5 * UP)
        found = VGroup(label(f"{int(rare['present'])} of {int(rare['stations'])} stations", 38, VERMILION, weight=BOLD),
                       label(f"{100 * rare['prevalence']:.1f}%", 52, VERMILION, weight=BOLD)
                       ).arrange(DOWN, buff=0.15).move_to(3.9 * RIGHT + 0.6 * UP)
        imbalanced = VGroup(label("imbalanced classes:", 30, INK, weight=BOLD),
                            label("one answer much rarer", 30, INK)).arrange(DOWN, buff=0.08
                                                                            ).move_to(3.9 * RIGHT + 1.6 * DOWN)
        # "Many things marine scientists most want to predict are rare: ..."
        cue(self, "Many things")
        self.play(FadeIn(examples, shift=0.2 * UP), run_time=self.share(0.1))
        # "Here a second species turns up at only 29 of 598 stations, 4.8 per cent."
        cue(self, "Here a second")
        self.play(FadeOut(examples), FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.12))
        cue(self, "29 of")
        self.play(*[d.animate.set_color(VERMILION).scale(1.4) for d in lit], FadeIn(found), run_time=self.share(0.12))
        # "When one answer is much rarer than the other, the classes are called imbalanced."
        cue(self, "When one answer")
        self.play(FadeIn(imbalanced, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        rare, dots, lit = rare_grid(self)
        for d in lit:
            d.set_color(VERMILION).scale(1.4)
        self.add(dots)
        plain = self.data("at-default").set_index("training").loc["No rebalancing"]
        head = VGroup(label("logistic regression", 32, INK, weight=BOLD),
                      label("threshold 0.5", 28, SUBDUED)).arrange(DOWN, buff=0.08).move_to(3.9 * RIGHT + 2.6 * UP)
        found = VGroup(label("presences found", 30, VERMILION),
                       label(f"{plain['sensitivity']:.0f}", 64, VERMILION, weight=BOLD)
                       ).arrange(DOWN, buff=0.1).move_to(3.9 * RIGHT + 0.7 * UP)
        accuracy = VGroup(label("accuracy", 30, GREEN),
                          label(percent(plain["accuracy"]), 64, GREEN, weight=BOLD)
                          ).arrange(DOWN, buff=0.1).move_to(3.9 * RIGHT + 1.5 * DOWN)
        same = label("as if it said absent everywhere", 28, INK).next_to(accuracy, DOWN, 0.25)
        rings = VGroup(*[Circle(0.13, color=VERMILION, stroke_width=3).move_to(d) for d in lit])
        # "Logistic regression gives each station a probability of presence, ..."
        self.play(FadeIn(head), run_time=self.share(0.1))
        # "Here it finds none of the presences."
        cue(self, "Here it finds")
        self.play(FadeIn(found), Create(rings), run_time=self.share(0.1))
        # "Yet its accuracy, the share of calls that are right, is 95 per cent: ..."
        cue(self, "Yet its accuracy")
        self.play(FadeIn(accuracy), run_time=self.share(0.1))
        # "... calling the species absent everywhere is right almost everywhere."
        cue(self, "calling the species")
        self.play(FadeIn(same, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene20(VideoScene):
    """Schematic: twenty cases and the three measures that count their mistakes apart."""

    number = 20

    def construct(self):
        present = VGroup(*[Dot(radius=0.2, color=VERMILION) for _ in range(4)]).arrange(RIGHT, buff=0.3)
        absent = VGroup(*[Circle(0.2, color=GREY, stroke_width=4) for _ in range(16)]
                        ).arrange_in_grid(rows=2, buff=0.3)
        present.move_to(3.4 * LEFT + 1.6 * UP)
        absent.move_to(3.4 * LEFT + 0.6 * DOWN)
        present_name = label("truly present", 28, VERMILION, weight=BOLD).next_to(present, UP, 0.25)
        absent_name = label("truly absent", 28, GREY, weight=BOLD).next_to(absent, DOWN, 0.25)
        called = [present[0], present[1], present[2], absent[0], absent[1], absent[9]]
        rings = VGroup(*[Circle(0.32, color=ORANGE, stroke_width=5).move_to(c) for c in called])
        called_name = key_row(ORANGE, "called present", 28).next_to(absent_name, DOWN, 0.3)
        measures = VGroup(
            VGroup(label("sensitivity", 34, VERMILION, weight=BOLD),
                   label("of the truly present: share called present", 26, INK),
                   label("misses lower it", 26, SUBDUED)),
            VGroup(label("specificity", 34, GREY, weight=BOLD),
                   label("of the truly absent: share called absent", 26, INK),
                   label("false alarms lower it", 26, SUBDUED)),
            VGroup(label("precision", 34, ORANGE, weight=BOLD),
                   label("of those called present: share truly present", 26, INK)))
        for m in measures:
            m.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        measures.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(3.5 * RIGHT + 0.2 * DOWN)
        boxes = [SurroundingRectangle(present, color=VERMILION, buff=0.2, stroke_width=4),
                 SurroundingRectangle(absent, color=GREY, buff=0.2, stroke_width=4)]
        # "So count the two kinds of mistake apart."
        self.play(FadeIn(present), FadeIn(present_name), FadeIn(absent), FadeIn(absent_name), run_time=self.share(0.08))
        self.play(Create(rings), FadeIn(called_name), run_time=self.share(0.08))
        # "Sensitivity: of the stations with the species, the share called present; misses lower it."
        cue(self, "Sensitivity")
        self.play(Create(boxes[0]), FadeIn(measures[0]), run_time=self.share(0.12))
        # "Specificity: of the stations without it, the share called absent; false alarms lower it."
        cue(self, "Specificity")
        self.play(ReplacementTransform(boxes[0], boxes[1]), FadeIn(measures[1]), run_time=self.share(0.12))
        # "Precision: of the stations called present, the share that truly have it."
        cue(self, "Precision")
        self.play(FadeOut(boxes[1]), Indicate(rings, color=ORANGE, scale_factor=1.2), FadeIn(measures[2]),
                  run_time=self.share(0.12))
        self.finish()


class Scene21(VideoScene):
    """Schematic: upsampling copies the presences, downsampling drops absences."""

    number = 21

    def construct(self):
        copies = round(self.data("rare").iloc[0]["copies"])

        def crowd(n_absent, n_present):
            return VGroup(*[Circle(0.1, color=GREY, stroke_width=3) for _ in range(n_absent)],
                          *[Dot(radius=0.1, color=VERMILION) for _ in range(n_present)]
                          ).arrange_in_grid(cols=10, buff=0.1)

        data = crowd(copies, 1).move_to(4.4 * LEFT + 0.3 * DOWN)
        data_name = label("training data", 30, INK, weight=BOLD).next_to(data, UP, 0.3)
        up = crowd(copies, copies).move_to(3.0 * RIGHT + 1.0 * UP)
        down = crowd(1, 1).move_to(3.0 * RIGHT + 1.5 * DOWN)
        up_name = VGroup(label("upsampling:", 28, VERMILION, weight=BOLD),
                         label(f"copy each presence, here about {copies} times", 26, INK)
                         ).arrange(DOWN, buff=0.06).next_to(up, UP, 0.2)
        down_name = VGroup(label("downsampling:", 28, BLUE, weight=BOLD),
                           label("drop absences until they match", 26, INK)).arrange(DOWN, buff=0.06
                                                                                     ).next_to(down, DOWN, 0.25)
        arrows = VGroup(Arrow(data.get_right(), up.get_left(), color=INK, stroke_width=5, buff=0.4),
                        Arrow(data.get_right(), down.get_left(), color=INK, stroke_width=5, buff=0.4))
        head = label("Rebalancing: make both answers equally common", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.3)
        scored = label("only the training data change: it is scored on the real mix", 28, GREEN, weight=BOLD
                       ).to_edge(DOWN, buff=0.35)
        # "The usual fix is rebalancing: change the training data so both answers are equally common."
        self.play(FadeIn(head), FadeIn(data), FadeIn(data_name), run_time=self.share(0.12))
        # "Upsampling copies each presence, here about 20 times."
        cue(self, "Upsampling")
        self.play(GrowArrow(arrows[0]), FadeIn(up_name), FadeIn(up, lag_ratio=0.02), run_time=self.share(0.14))
        # "Downsampling drops absences until the two match."
        cue(self, "Downsampling")
        self.play(GrowArrow(arrows[1]), FadeIn(down_name), FadeIn(down), run_time=self.share(0.12))
        # "Only the data the model learns from change; it is still scored on the real mix."
        cue(self, "Only the data")
        self.play(FadeIn(scored, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        calls = self.data("at-default").set_index("training")
        plain = calls.loc["No rebalancing"]
        both = calls.loc[["Upsampling", "Downsampling"]]
        sensitivity = both["sensitivity"].mean()
        alarms = 1 - both["specificity"].mean()
        one_in = round(1 / calls.loc["Upsampling", "precision"])

        def row(name, before, after, colour, y):
            words = label(name, 32, INK, weight=BOLD).move_to([-5.0, y, 0], aligned_edge=LEFT)
            was = label(before, 40, SUBDUED, weight=BOLD).move_to([-0.6, y, 0])
            arrow = Arrow([0.4, y, 0], [1.6, y, 0], color=GREY, stroke_width=5, buff=0)
            now = label(after, 40, colour, weight=BOLD).next_to(arrow, RIGHT, 0.3)
            return VGroup(words, was, arrow, now)

        rows = VGroup(row("sensitivity", f"{plain['sensitivity']:.0f}", f"about {sensitivity:.1f}", GREEN, 1.4),
                      row("false alarms", percent(1 - plain["specificity"]), f"{percent(alarms)} of absences",
                          VERMILION, 0.0),
                      row("precision", "", f"about 1 in {one_in}", VERMILION, -1.4))
        head = VGroup(label("without rebalancing", 26, SUBDUED).next_to(rows[0][1], UP, 0.6),
                      label("rebalanced", 26, SUBDUED).next_to(rows[0][3], UP, 0.6))
        precision_note = label("called present, and right", 26, SUBDUED
                               ).next_to(rows[2][3], DOWN, 0.15, aligned_edge=LEFT)
        # "Both raise the sensitivity from 0 to about 0.7: most presences are now found."
        self.play(FadeIn(head), FadeIn(rows[0][:2]), run_time=self.share(0.1))
        self.play(GrowArrow(rows[0][2]), FadeIn(rows[0][3]), run_time=self.share(0.1))
        # "The price is false alarms, at about 31 per cent of the absences."
        cue(self, "The price")
        self.play(FadeIn(rows[1][:2]), GrowArrow(rows[1][2]), FadeIn(rows[1][3]), run_time=self.share(0.12))
        # "And precision stays low: only about 1 in 9 stations called present holds the species."
        cue(self, "And precision")
        self.play(FadeIn(rows[2][0]), GrowArrow(rows[2][2]), FadeIn(rows[2][3]), FadeIn(precision_note),
                  run_time=self.share(0.12))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        curve = self.data("curve").sort_values("threshold")
        same = self.data("same").iloc[0]
        up = self.data("at-default").set_index("training").loc["Upsampling"]
        # Across: specificity from 1 at the left to 0 at the right, so x = 1 − specificity.
        axes, frame = chart([0, 1, 0.25], [0, 1, 0.25], 6.0, 5.0, [0, 0.25, 0.5, 0.75, 1], [0, 0.5, 1],
                            "specificity", "sensitivity", x_text=lambda v: f"{1 - v:g}")
        VGroup(axes, frame).shift(3.0 * LEFT + 0.3 * DOWN)
        path = polyline(axes, 1 - curve["specificity"], curve["sensitivity"], GREY, 6)
        path_name = VGroup(label("every threshold,", 26, GREY, weight=BOLD),
                           label("data left alone", 26, GREY, weight=BOLD)
                           ).arrange(DOWN, buff=0.05, aligned_edge=LEFT).next_to(axes.c2p(0.55, 0.45), RIGHT, 0.1)
        point = axes.c2p(1 - same["specificity"], same["sensitivity"])
        circle = Circle(0.3, color=INK, stroke_width=5).move_to(point)
        up_dot = Dot(axes.c2p(0.02, 0.02), radius=0.13, color=ORANGE).set_z_index(10)
        lower = VGroup(label(f"threshold {same['threshold']:.3f},", 30, INK, weight=BOLD),
                       label("data left alone", 30, INK, weight=BOLD)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        upsampled = VGroup(label("upsampling,", 30, ORANGE, weight=BOLD),
                           label("threshold 0.5", 30, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        values = VGroup(label(f"sensitivity {up['sensitivity']:.3f}", 30, INK),
                        label(f"specificity {up['specificity']:.3f}", 30, INK),
                        label("both ways", 30, INK, weight=BOLD)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        why = VGroup(label("copying raises every", 28, BLUE, weight=BOLD),
                     label("probability, but keeps", 28, BLUE, weight=BOLD),
                     label("the stations' order", 28, BLUE, weight=BOLD)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        side = VGroup(lower, upsampled, values, why).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.move_to(3.8 * RIGHT)
        # "Now leave the data alone and lower the threshold instead, ..."
        self.play(FadeIn(frame), run_time=self.share(0.06))
        self.play(Create(path), FadeIn(path_name), run_time=self.share(0.14))
        # "... to 0.048, the share of stations with the species."
        cue(self, "to 0.048")
        self.play(Create(circle), FadeIn(lower), run_time=self.share(0.08))
        # "The calls come out the same as upsampling: ..."
        cue(self, "The calls come")
        self.play(FadeIn(up_dot), FadeIn(upsampled), run_time=self.share(0.04))
        self.play(up_dot.animate.move_to(point), run_time=self.share(0.08))
        # "... a sensitivity of 0.717 and a specificity of 0.712 both ways."
        cue(self, "a sensitivity of")
        self.play(FadeIn(values), run_time=self.share(0.08))
        # "Copying the presences raises every station's probability but keeps their order, ..."
        cue(self, "Copying the")
        self.play(FadeIn(why, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        chances = self.data("chances").set_index("training")
        share = chances.loc["No rebalancing", "share"]
        plain, up = chances.loc["No rebalancing", "average"], chances.loc["Upsampling", "average"]
        top = 0.4
        axes, frame = chart([0, 2, 1], [0, top, 0.1], 7.0, 4.2, [], [0, 0.1, 0.2, 0.3, 0.4], None,
                            "average probability")
        VGroup(axes, frame).shift(1.8 * LEFT + 0.3 * DOWN)
        truth = DashedLine(axes.c2p(0, share), axes.c2p(2, share), color=VERMILION, stroke_width=4)
        truth_name = plated(label(f"the real share: {100 * share:.1f}%", 26, VERMILION, weight=BOLD)
                            ).next_to(axes.c2p(2, share), RIGHT, 0.2)

        def bar(k, value, colour, name):
            rect = Rectangle(width=1.6, height=max(value / top * axes.y_length, 0.01), stroke_width=0,
                             fill_color=colour, fill_opacity=0.9).move_to(axes.c2p(k + 0.5, 0), aligned_edge=DOWN)
            text = f"{value:.3f}" if value < 0.1 else f"{value:.2f}"
            return VGroup(rect, label(text, 30, colour, weight=BOLD).next_to(rect, UP, 0.12),
                          label(name, 26, SUBDUED).next_to(axes.c2p(k + 0.5, 0), DOWN, 0.2))

        bars = VGroup(bar(0, plain, BLUE, "data left alone"), bar(1, up, ORANGE, "upsampled"))
        times = label(f"about {up / share:.0f} times too high", 32, ORANGE, weight=BOLD
                      ).next_to(bars[1][0], RIGHT, 0.4).align_to(bars[1][1], UP)
        not_chances = label("no longer chances", 32, INK, weight=BOLD).next_to(times, DOWN, 0.2, aligned_edge=LEFT)
        advice = label("leave the data alone; set the threshold from what each mistake costs", 30, GREEN,
                       weight=BOLD).to_edge(DOWN, buff=0.3)
        # "Rebalancing also does harm."
        self.play(FadeIn(frame), Create(truth), FadeIn(truth_name), run_time=self.share(0.08))
        self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), run_time=self.share(0.08))
        # "After upsampling, the probabilities average 0.34, about 7 times the real share: ..."
        cue(self, "After upsampling")
        self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), run_time=self.share(0.1))
        cue(self, "about 7")
        self.play(FadeIn(times), run_time=self.share(0.06))
        # "... they are no longer chances."
        cue(self, "they are no")
        self.play(FadeIn(not_chances), run_time=self.share(0.06))
        # "So leave the data alone, and choose the threshold from what a miss and a false alarm each cost."
        cue(self, "So leave")
        self.play(FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene25(KeyPointScene):
    number, point = 25, 3


# Quiz (scenes 26–27) -----------------------------------------------------------------------

class Scene26(QuizScene):
    number = 26
    question = ("A harmful algal bloom occurs", "on 2 days in 100.",
                "A model that warns of blooms is 98% accurate.", "Is it a good model?")


class Scene27(VideoScene):
    """Schematic: a hundred days, two with a bloom, and a model that never warns."""

    number = 27

    def construct(self):
        days = VGroup(*[Square(0.36, stroke_width=0, fill_color=LIGHT, fill_opacity=1) for _ in range(100)]
                      ).arrange_in_grid(rows=10, buff=0.08).move_to(3.8 * LEFT + 0.4 * DOWN)
        blooms = VGroup(days[23], days[67])
        blooms.set_fill(VERMILION)
        answer = label("You can't tell yet.", 56, BLUE, weight=BOLD).to_edge(UP, buff=0.3)
        never = VGroup(label("a model that never warns:", 30, INK, weight=BOLD),
                       label("98% accurate", 40, GREEN, weight=BOLD),
                       label("blooms caught: 0", 40, VERMILION, weight=BOLD)
                       ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(3.0 * RIGHT + 1.0 * UP)
        ask = VGroup(label("ask for", 30, INK),
                     label("sensitivity: blooms caught", 30, VERMILION, weight=BOLD),
                     label("precision: warnings that are real", 30, ORANGE, weight=BOLD)
                     ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(never, DOWN, 0.7, aligned_edge=LEFT)
        rings = VGroup(*[Circle(0.3, color=VERMILION, stroke_width=4).move_to(b) for b in blooms])
        key = key_row(VERMILION, "a day with a bloom", 26).next_to(days, DOWN, 0.3)
        # "You can't tell yet."
        self.play(FadeIn(answer, scale=1.2), FadeIn(days, lag_ratio=0.005), FadeIn(key), run_time=self.share(0.12))
        # "A model that never warns is also 98 per cent accurate, ..."
        cue(self, "A model that")
        self.play(FadeIn(never[:2]), run_time=self.share(0.1))
        # "... and it misses every bloom."
        cue(self, "and it misses")
        self.play(FadeIn(never[2]), Create(rings), run_time=self.share(0.08))
        # "Ask for its sensitivity, how many blooms it catches, and its precision, ..."
        cue(self, "Ask for")
        self.play(FadeIn(ask[:2]), run_time=self.share(0.1))
        cue(self, "and its precision")
        self.play(FadeIn(ask[2]), run_time=self.share(0.08))
        self.finish()


# The recap (scenes 28–30) and the end card (scene 31) --------------------------------------

class Scene28(RecapScene):
    number, point = 28, 1


class Scene29(RecapScene):
    number, point = 29, 2


class Scene30(RecapScene):
    number, point = 30, 3


class Scene31(EndCardScene):
    number = 31
