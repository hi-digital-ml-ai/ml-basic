"""Manim scenes for the §5 video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/05-generalisation
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

Scenes marked "real data" read visuals/data/*.csv, which tools/figures-for-video.R
writes from the pages. The others are schematic: made-up shapes, tagged
"illustration" in the corner, never numbers that could pass for survey results.
Consecutive scenes about one picture share a builder, so each starts where the
previous one ended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


# In this video (scene 1) ------------------------------------------------------------

class Scene01(VideoScene):
    number = 1

    def construct(self):
        head = title("In this video", 56).to_edge(UP, buff=1.0)
        points = ["Why a perfect fit is a warning sign",
                  "Where the U-shaped error curve comes from",
                  "How to choose complexity honestly"]
        rows = VGroup()
        for i, text in enumerate(points, 1):
            badge = VGroup(Circle(0.33, color=BLUE, fill_opacity=1, stroke_width=0),
                           label(str(i), 32, BACKGROUND, weight=BOLD))
            rows.add(VGroup(badge, label(text, 40)).arrange(RIGHT, buff=0.45))
        rows.arrange(DOWN, buff=0.7, aligned_edge=LEFT).next_to(head, DOWN, 0.9)

        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "In this video: [1] ..., [2] ..., and [3] ..."
        for row, at in zip(rows, (0.12, 0.42, 0.7)):
            self.wait(max(self.share(at) - self.time, 0.01))
            self.play(FadeIn(row[0], scale=0.6), FadeIn(row[1], shift=0.3 * RIGHT),
                      run_time=self.share(0.08))
        self.finish()


# Five models, training error only (scenes 2–4, real data) -----------------------------

# The colours ggplot gives the five models on the page (levels in alphabetical
# order), so the video and fig-crossing agree.
MODEL_COLOURS = {
    "Boosted trees": BLUE, "Linear regression": ORANGE, "Random forest": GREEN,
    "Tree, depth 3": VERMILION, "Tree, grown out": PURPLE,
}


def rmse_text(value, digits=2, size=30, color=INK):
    """An RMSE as printed: an exact zero is written 0, not 0.00."""
    return label("0" if value == 0 else f"{value:.{digits}f}", size, color)


def five_models_table(models):
    heading = label("Error on the training stations (RMSE)", 34, SUBDUED)
    hidden = label("on new stations", 34, GRID)
    scale = 5.2 / models["training"].max()
    rows = VGroup()
    for i, (_, m) in enumerate(models.iterrows()):
        y = 1.6 - 0.95 * i
        name = label(m["model"], 32).move_to([-3.6, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=max(m["training"] * scale, 0.02), height=0.42, stroke_width=0,
                        fill_color=MODEL_COLOURS[m["model"]], fill_opacity=1)
        bar.move_to([-3.3, y, 0], aligned_edge=LEFT)
        value = rmse_text(m["training"]).next_to(bar, RIGHT, 0.2)
        blank = RoundedRectangle(width=1.2, height=0.5, corner_radius=0.08,
                                 stroke_color=GRID, stroke_width=2).move_to([5.4, y, 0])
        rows.add(VGroup(name, bar, value, blank))
    heading.move_to([-0.7, 2.7, 0])
    hidden.move_to([5.4, 2.7, 0])
    perfect = next(r for r, (_, m) in zip(rows, models.iterrows()) if m["training"] == 0)
    return heading, hidden, rows, perfect


class Scene02(VideoScene):
    number = 2

    def construct(self):
        heading, hidden, rows, perfect = five_models_table(self.data("five-models"))
        self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.15),
                  run_time=self.share(0.25))
        self.play(FadeIn(heading), FadeIn(hidden), *[FadeIn(r[3]) for r in rows],
                  run_time=self.share(0.1))
        # "The bars show their error on the stations they learned from."
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                for r in rows], lag_ratio=0.2), run_time=self.share(0.4))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        heading, hidden, rows, perfect = five_models_table(self.data("five-models"))
        self.add(heading, hidden, rows)
        others = [r for r in rows if r is not perfect]
        self.play(*[r.animate.set_opacity(0.3) for r in others], run_time=self.share(0.15))
        self.play(perfect[2].animate.scale(1.8).set_color(PURPLE), run_time=self.share(0.2))
        self.play(Circumscribe(VGroup(perfect[0], perfect[2]), color=PURPLE),
                  run_time=self.share(0.35))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        heading, hidden, rows, perfect = five_models_table(self.data("five-models"))
        perfect[2].scale(1.8).set_color(PURPLE)
        for r in rows:
            if r is not perfect:
                r.set_opacity(0.3)
        self.add(heading, hidden, rows)
        mark = label("?", 44, PURPLE, weight=BOLD).move_to(perfect[3])
        self.play(hidden.animate.set_color(INK), perfect[3].animate.set_stroke(PURPLE, 3),
                  run_time=self.share(0.25))
        self.play(FadeIn(mark, scale=2), run_time=self.share(0.25))
        self.play(Wiggle(mark), run_time=self.share(0.35))
        self.finish()


# Simulated survey (scene 5, schematic) ------------------------------------------------

class Scene05(VideoScene):
    number = 5

    def construct(self):
        box = RoundedRectangle(width=4.2, height=2.2, corner_radius=0.2, stroke_color=BLUE,
                               stroke_width=5, fill_color="#EAF2F8", fill_opacity=1)
        box_text = VGroup(label("the process", 36, BLUE, weight=BOLD),
                          label("we wrote", 36, BLUE, weight=BOLD)).arrange(DOWN, buff=0.15)
        source = VGroup(box, box_text.move_to(box)).move_to(3.8 * LEFT)
        rng = np.random.default_rng(5)
        field = VGroup(*[Dot([x, y, 0], radius=0.08, color=GREY)
                         for x, y in zip(rng.uniform(1.6, 5.8, 36), rng.uniform(-1.8, 1.8, 36))])
        field_name = label("simulated survey", 32, SUBDUED).next_to(field, DOWN, 0.4)
        arrow = Arrow(source.get_right(), [1.3, 0, 0], color=INK, stroke_width=5, buff=0.2)
        known = label("true answer known", 32, GREEN, weight=BOLD).next_to(source, DOWN, 0.4)

        self.add(schematic_note())
        # "A note first: this survey is simulated."
        self.play(FadeIn(source, scale=0.9), run_time=self.share(0.15))
        self.play(GrowArrow(arrow), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(d, shift=0.4 * RIGHT) for d in field], lag_ratio=0.04),
                  FadeIn(field_name), run_time=self.share(0.3))
        # "... so we know the true answer."
        self.play(FadeIn(known, shift=0.2 * UP), run_time=self.share(0.1))
        self.play(Indicate(known, color=GREEN), run_time=self.share(0.15))
        self.finish()


# The ranking reverses (scenes 6, 7, 10, 11; real data) ---------------------------------

def slope_axes(models):
    top = float(np.ceil(models["test"].max()))
    axes = Axes(x_range=[0, 1, 1], y_range=[0, top, 1], x_length=6, y_length=5.6,
                tips=False, axis_config={"color": GRID, "include_ticks": False}
                ).shift(1.4 * LEFT + 0.1 * DOWN)
    ticks = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(0, v), LEFT, 0.2)
                     for v in range(0, int(top) + 1)])
    ylab = label("RMSE (individuals)", 26, SUBDUED).rotate(PI / 2).next_to(ticks, LEFT, 0.3)
    sides = VGroup(label("Training", 30, SUBDUED).next_to(axes.c2p(0, 0), DOWN, 0.3),
                   label("New stations", 30, SUBDUED).next_to(axes.c2p(1, 0), DOWN, 0.3))
    frame = VGroup(axes, ticks, ylab, sides)

    lines, left_dots, right_dots, names = VGroup(), VGroup(), VGroup(), VGroup()
    for _, m in models.iterrows():
        c = MODEL_COLOURS[m["model"]]
        a, b = axes.c2p(0, m["training"]), axes.c2p(1, m["test"])
        left_dots.add(Dot(a, radius=0.1, color=c))
        right_dots.add(Dot(b, radius=0.1, color=c))
        lines.add(Line(a, b, color=c, stroke_width=5))
        names.add(label(m["model"], 26, c).next_to(b, RIGHT, 0.25))
    # keep the right-hand names from overlapping where test errors are close
    order = np.argsort(-models["test"].to_numpy())
    for k in range(1, len(order)):
        above, here = names[order[k - 1]], names[order[k]]
        if here.get_top()[1] > above.get_bottom()[1] - 0.14:
            here.shift((here.get_top()[1] - above.get_bottom()[1] + 0.14) * DOWN)
    return axes, frame, lines, left_dots, right_dots, names


class Scene06(VideoScene):
    number = 6

    def construct(self):
        axes, frame, lines, left_dots, right_dots, names = slope_axes(self.data("five-models"))
        self.play(FadeIn(frame[0]), FadeIn(frame[1]), FadeIn(frame[2]), FadeIn(frame[3][0]),
                  LaggedStart(*[FadeIn(d, scale=1.5) for d in left_dots], lag_ratio=0.2),
                  run_time=self.share(0.35))
        # "... stations they have never seen."
        self.play(FadeIn(frame[3][1], shift=0.3 * LEFT), run_time=self.share(0.25))
        self.play(Indicate(frame[3][1], color=INK), run_time=self.share(0.25))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        models = self.data("five-models")
        axes, frame, lines, left_dots, right_dots, names = slope_axes(models)
        self.add(frame, left_dots)
        order = np.argsort(models["training"].to_numpy())   # from the best-trained up
        # "Every error goes up. New data is always harder."
        self.play(LaggedStart(*[AnimationGroup(Create(lines[i]), FadeIn(right_dots[i]),
                                               FadeIn(names[i]))
                                for i in order], lag_ratio=0.35),
                  run_time=self.share(0.55))
        # "But look at the order."
        self.play(Indicate(names, scale_factor=1.08, color=INK), run_time=self.share(0.25))
        self.finish()


def dim_all_but_tree(models, parts):
    lines, left_dots, right_dots, names = parts
    tree = models.index[models["model"] == "Tree, grown out"][0]
    others = [m for i in range(len(models)) if i != tree
              for m in (lines[i], left_dots[i], right_dots[i], names[i])]
    return tree, others


class Scene10(VideoScene):
    number = 10

    def construct(self):
        models = self.data("five-models")
        axes, frame, *parts = slope_axes(models)
        self.add(frame, *parts)
        tree, others = dim_all_but_tree(models, parts)
        right_dots = parts[2]
        value = label(f"{models['test'].iloc[tree]:.1f}", 40, PURPLE, weight=BOLD)
        value.next_to(right_dots[tree], LEFT, 0.25)
        self.play(*[m.animate.set_opacity(0.15) for m in others], run_time=self.share(0.2))
        self.play(parts[0][tree].animate.set_stroke(width=9), run_time=self.share(0.15))
        self.play(FadeIn(value, scale=1.5), Flash(right_dots[tree], color=PURPLE),
                  run_time=self.share(0.3))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        models = self.data("five-models")
        axes, frame, *parts = slope_axes(models)
        tree, others = dim_all_but_tree(models, parts)
        for m in others:
            m.set_opacity(0.15)
        parts[0][tree].set_stroke(width=9)
        value = label(f"{models['test'].iloc[tree]:.1f}", 40, PURPLE, weight=BOLD)
        value.next_to(parts[2][tree], LEFT, 0.25)
        self.add(frame, *parts, value)

        baseline = models["baseline"].iloc[0]
        mean_line = DashedLine(axes.c2p(0, baseline), axes.c2p(1.25, baseline), color=GREY,
                               stroke_width=5)
        mean_name = label(f"just guess the average: {baseline:.1f}", 30, GREY).next_to(
            axes.c2p(0, baseline), UR, 0.15)
        # "Just guessing the average scores 5.3."
        self.play(Create(mean_line), FadeIn(mean_name), run_time=self.share(0.25))
        # "The tree has not learned. It has memorised."
        self.wait(self.share(0.25))
        memorised = label("memorised", 40, PURPLE, weight=BOLD).next_to(axes.c2p(1, 2.5), RIGHT, 0.3)
        self.play(FadeIn(memorised, scale=1.3), run_time=self.share(0.15))
        self.finish()


# Rankings (scenes 8–9, real data) ---------------------------------------------------

def ranking_lists(models):
    """The five models ranked by training error and by test error, 1 = best."""
    by_train = list(models.sort_values("training")["model"])
    by_test = list(models.sort_values("test")["model"])

    def column(heading, names):
        items = VGroup(*[
            VGroup(label(f"{i}", 32, SUBDUED), label(n, 32, MODEL_COLOURS[n])).arrange(RIGHT, buff=0.3)
            for i, n in enumerate(names, 1)])
        items.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        return VGroup(label(heading, 32, weight=BOLD), items).arrange(DOWN, buff=0.55)

    left = column("ranked by training error", by_train).move_to(3.6 * LEFT)
    right = column("ranked on new stations", by_test).move_to(3.6 * RIGHT)
    arrows = VGroup()
    for i, n in enumerate(by_train):
        j = by_test.index(n)
        arrows.add(Arrow(left[1][i].get_right(), right[1][j][0].get_left(),
                         buff=0.25, color=MODEL_COLOURS[n], stroke_width=4,
                         max_tip_length_to_length_ratio=0.05))
    return left, right, arrows


class Scene08(VideoScene):
    number = 8

    def construct(self):
        left, right, arrows = ranking_lists(self.data("five-models"))
        self.play(FadeIn(left), run_time=self.share(0.15))
        self.play(FadeIn(right), run_time=self.share(0.15))
        # "... the order is exactly reversed."
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25),
                  run_time=self.share(0.45))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        left, right, arrows = ranking_lists(self.data("five-models"))
        self.add(left, right, arrows)
        # arrows[0] is the model ranked first on training error: the grown-out tree
        self.play(*[a.animate.set_opacity(0.2) for a in arrows[1:]], run_time=self.share(0.15))
        self.play(Circumscribe(left[1][0], color=PURPLE), run_time=self.share(0.3))
        self.play(Circumscribe(right[1][-1], color=PURPLE), run_time=self.share(0.3))
        self.finish()


# Signal and noise (scenes 12–14, schematic) ---------------------------------------------

def signal_and_noise():
    rng = np.random.default_rng(8)
    x = np.linspace(0.04, 0.96, 26) + rng.uniform(-0.012, 0.012, 26)
    signal = lambda v: 0.25 + 1.05 * np.exp(-2.6 * v)  # noqa: E731
    y = signal(x) + rng.normal(0, 0.13, x.size)

    axes = Axes(x_range=[0, 1, 1], y_range=[0, 1.6, 1], x_length=10, y_length=5.2,
                tips=False, axis_config={"color": GRID, "include_ticks": False})
    names = VGroup(label("depth", 30, SUBDUED).next_to(axes.x_axis, DOWN, 0.25),
                   label("abundance", 30, SUBDUED).rotate(PI / 2).next_to(axes.y_axis, LEFT, 0.25))
    dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.07, color=GREY) for a, b in zip(x, y)])
    trend = axes.plot(signal, x_range=[0.02, 0.98], color=BLUE, stroke_width=6)
    residuals = VGroup(*[
        Line(axes.c2p(a, signal(a)), axes.c2p(a, b), color=ORANGE, stroke_width=4)
        for a, b in zip(x, y)])

    from scipy.interpolate import CubicSpline
    spline = CubicSpline(x, y)
    wiggle = axes.plot(lambda v: float(np.clip(spline(v), 0.02, 1.58)),
                       x_range=[x[0], x[-1], 0.002], color=VERMILION, stroke_width=5)

    signal_tag = label("signal", 36, BLUE, weight=BOLD).next_to(axes.c2p(0.3, signal(0.3)), UR, 0.3)
    noise_tag = label("noise", 36, ORANGE, weight=BOLD).next_to(axes.c2p(0.72, 1.0), UP, 0.1)
    return dict(axes=axes, names=names, dots=dots, trend=trend, residuals=residuals,
                wiggle=wiggle, signal_tag=signal_tag, noise_tag=noise_tag)


class Scene12(VideoScene):
    number = 12

    def construct(self):
        p = signal_and_noise()
        self.add(schematic_note())
        self.play(Create(p["axes"]), FadeIn(p["names"]), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in p["dots"]], lag_ratio=0.05),
                  run_time=self.share(0.25))
        # "Signal is the pattern that turns up again next year."
        self.play(Create(p["trend"]), run_time=self.share(0.3))
        self.play(FadeIn(p["signal_tag"], shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        p = signal_and_noise()
        self.add(schematic_note(), p["axes"], p["names"], p["dots"], p["trend"], p["signal_tag"])
        self.play(LaggedStart(*[Create(r) for r in p["residuals"]], lag_ratio=0.05),
                  run_time=self.share(0.55))
        self.play(FadeIn(p["noise_tag"], shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        p = signal_and_noise()
        self.add(schematic_note(), p["axes"], p["names"], p["dots"], p["trend"],
                 p["residuals"], p["signal_tag"], p["noise_tag"])

        # A training-error gauge with no scale: only its fall to zero matters.
        error = ValueTracker(1.0)
        gauge_label = label("training error", 30, SUBDUED)
        gauge_label.to_corner(UR, buff=0.6).shift(0.9 * LEFT)
        track = Rectangle(width=3.2, height=0.32, stroke_color=GRID, stroke_width=2)
        track.next_to(gauge_label, DOWN, 0.2, aligned_edge=LEFT)
        bar = always_redraw(lambda: Rectangle(
            width=max(3.2 * error.get_value(), 0.001), height=0.32, stroke_width=0,
            fill_color=VERMILION, fill_opacity=1).align_to(track, LEFT).align_to(track, DOWN))
        zero = label("0", 30, VERMILION, weight=BOLD).next_to(track, LEFT, 0.2)

        self.play(FadeOut(p["residuals"]), FadeOut(p["noise_tag"]),
                  p["trend"].animate.set_stroke(opacity=0.35),
                  p["signal_tag"].animate.set_opacity(0.35),
                  FadeIn(gauge_label), FadeIn(track), FadeIn(bar), run_time=self.share(0.12))
        self.play(Create(p["wiggle"]), error.animate.set_value(0),
                  run_time=self.share(0.55), rate_func=linear)
        self.play(FadeIn(zero, scale=1.4), run_time=self.share(0.08))
        self.finish()


# Three trees on one predictor (scenes 15–17, real data) ---------------------------------

def three_fits_axes(points):
    axes = Axes(x_range=[0, 200, 50], y_range=[0, 42, 10], x_length=10.5, y_length=5.2,
                tips=False, axis_config={"color": GRID, "include_ticks": False}
                ).shift(0.1 * DOWN + 0.4 * RIGHT)
    xt = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(v, 0), DOWN, 0.2)
                  for v in (0, 50, 100, 150, 200)])
    yt = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(0, v), LEFT, 0.2)
                  for v in (0, 10, 20, 30, 40)])
    names = VGroup(label("depth (m)", 28, SUBDUED).next_to(xt, DOWN, 0.2),
                   label("abundance", 28, SUBDUED).rotate(PI / 2).next_to(yt, LEFT, 0.25))
    dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.045, color=GREY, fill_opacity=0.35)
                    for x, y in zip(points["depth_m"], points["abundance"])])
    return axes, VGroup(axes, xt, yt, names), dots


def fit_line(axes, fit):
    return VMobject(color=VERMILION, stroke_width=5).set_points_as_corners(
        [axes.c2p(x, y) for x, y in zip(fit["depth_m"], fit["abundance"])])


def fit_caption(fit, word):
    leaves = int(fit["leaves"].iloc[0])
    text = f"{leaves} leaves" + (f": {word}" if word else "")
    return label(text, 38, VERMILION if word else INK, weight=BOLD).to_corner(UR, buff=0.7)


class Scene15(VideoScene):
    number = 15

    def construct(self):
        axes, frame, dots = three_fits_axes(self.data("fit-points"))
        fit = self.data("fit-under")
        line, caption = fit_line(axes, fit), fit_caption(fit, "")
        self.play(FadeIn(frame), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=self.share(0.2))
        # "With one split, it is too rigid."
        self.play(Create(line), FadeIn(caption), run_time=self.share(0.2))
        self.wait(self.share(0.2))
        # "That is underfitting."
        self.play(Transform(caption, fit_caption(fit, "underfitting")), run_time=self.share(0.1))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        axes, frame, dots = three_fits_axes(self.data("fit-points"))
        under, right = self.data("fit-under"), self.data("fit-right")
        line, caption = fit_line(axes, under), fit_caption(under, "underfitting")
        self.add(frame, dots, line, caption)
        self.play(Transform(line, fit_line(axes, right)),
                  Transform(caption, fit_caption(right, "")), run_time=self.share(0.4))
        self.play(Indicate(line, color=BLUE, scale_factor=1.0), run_time=self.share(0.3))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        axes, frame, dots = three_fits_axes(self.data("fit-points"))
        right, over = self.data("fit-right"), self.data("fit-over")
        line, caption = fit_line(axes, right), fit_caption(right, "")
        self.add(frame, dots, line, caption)
        # "With one station per leaf, it chases every point."
        self.play(Transform(line, fit_line(axes, over).set_stroke(width=3)),
                  Transform(caption, fit_caption(over, "")), run_time=self.share(0.4))
        self.wait(self.share(0.15))
        # "That is overfitting."
        self.play(Transform(caption, fit_caption(over, "overfitting")), run_time=self.share(0.1))
        self.finish()


# The U-shaped curve (scenes 18–22, real data) --------------------------------------------

def u_curve_axes(curve):
    lo, hi = np.log10(5), np.log10(500)
    axes = Axes(x_range=[lo, hi, 1], y_range=[0, 6, 1], x_length=10, y_length=5.2,
                tips=False, axis_config={"color": GRID, "include_ticks": False}
                ).shift(0.3 * DOWN + 0.3 * RIGHT)
    xt = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(np.log10(v), 0), DOWN, 0.2)
                  for v in (10, 30, 100, 300)])
    yt = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(lo, v), LEFT, 0.2)
                  for v in range(0, 7)])
    xl = label("leaves in the tree (log scale)", 28, SUBDUED).next_to(xt, DOWN, 0.25)
    yl = label("RMSE (individuals)", 28, SUBDUED).rotate(PI / 2).next_to(yt, LEFT, 0.25)

    def trace(column, colour):
        points = [axes.c2p(np.log10(n), v) for n, v in zip(curve["leaves"], curve[column])]
        line = VMobject(color=colour, stroke_width=6).set_points_as_corners(points)
        dots = VGroup(*[Dot(p, radius=0.07, color=colour) for p in points])
        return line, dots

    training = trace("training", BLUE)
    test = trace("test", ORANGE)
    names = VGroup(label("training", 30, BLUE, weight=BOLD).next_to(training[1][-1], LEFT, 0.3),
                   label("new stations", 30, ORANGE, weight=BOLD).next_to(test[1][-1], UP, 0.2))
    return axes, VGroup(axes, xt, yt, xl, yl), training, test, names


def best_marker(axes, curve):
    best = int(curve["best_leaves"].iloc[0])
    x = np.log10(best)
    dotted = DashedLine(axes.c2p(x, 0), axes.c2p(x, 6), dash_length=0.06, color=INK, stroke_width=3)
    tag = label(f"best: {best} leaves", 28, INK).next_to(axes.c2p(x, 5.8), RIGHT, 0.2)
    return dotted, tag


class Scene18(VideoScene):
    number = 18

    def construct(self):
        axes, frame, training, test, names = u_curve_axes(self.data("u-curve"))
        self.play(FadeIn(frame), run_time=self.share(0.1))
        # "Its training error falls, all the way to zero."
        self.wait(self.share(0.25))
        self.play(Create(training[0]), LaggedStart(*[FadeIn(d) for d in training[1]]),
                  run_time=self.share(0.45), rate_func=linear)
        self.play(FadeIn(names[0]), run_time=self.share(0.08))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        curve = self.data("u-curve")
        axes, frame, training, test, names = u_curve_axes(curve)
        self.add(frame, *training, names[0])
        dotted, tag = best_marker(axes, curve)
        best = int(np.argmin(curve["test"].to_numpy()))
        # "falls, bottoms out at sixteen leaves, then climbs."
        self.play(Create(test[0]), LaggedStart(*[FadeIn(d) for d in test[1]]),
                  FadeIn(names[1]), run_time=self.share(0.7), rate_func=linear)
        self.play(Create(dotted), FadeIn(tag), Flash(test[1][best], color=ORANGE),
                  run_time=self.share(0.15))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        curve = self.data("u-curve")
        axes, frame, training, test, names = u_curve_axes(curve)
        dotted, tag = best_marker(axes, curve)
        self.add(frame, *training, *test, names, dotted, tag)
        self.play(training[0].animate.set_stroke(opacity=0.25),
                  training[1].animate.set_opacity(0.25), names[0].animate.set_opacity(0.25),
                  run_time=self.share(0.15))
        glow = test[0].copy().set_stroke(ORANGE, width=16, opacity=0.5)
        self.play(ShowPassingFlash(glow, time_width=0.5), run_time=self.share(0.4))
        self.play(test[0].animate.set_stroke(width=10), run_time=self.share(0.15))
        self.finish()


def full_u(scene, curve):
    axes, frame, training, test, names = u_curve_axes(curve)
    dotted, tag = best_marker(axes, curve)
    scene.add(frame, *training, *test, names, dotted, tag)
    return axes, training, test


class Scene21(VideoScene):
    number = 21

    def construct(self):
        curve = self.data("u-curve")
        axes, training, test = full_u(self, curve)
        baseline = curve["baseline"].iloc[0]
        lo, hi = np.log10(5), np.log10(500)
        mean_line = DashedLine(axes.c2p(lo, baseline), axes.c2p(hi, baseline), color=GREY,
                               stroke_width=4)
        mean_name = label("no predictors", 26, GREY).next_to(axes.c2p(lo, baseline), UR, 0.1)
        # The crossing lies between the last sweep point below the baseline and the
        # first above it (62 and 85 leaves on the page).
        above = curve[(curve["test"] > baseline) & (curve["leaves"] > curve["best_leaves"])]
        first = above.index[0]
        a, b = curve["leaves"].iloc[first - 1], curve["leaves"].iloc[first]
        band = Rectangle(width=axes.c2p(np.log10(b), 0)[0] - axes.c2p(np.log10(a), 0)[0],
                         height=5.2, stroke_width=0, fill_color=VERMILION, fill_opacity=0.15)
        band.move_to(axes.c2p((np.log10(a) + np.log10(b)) / 2, 3))
        band_tag = label(f"{a}–{b} leaves", 28, VERMILION, weight=BOLD).next_to(band, UP, 0.1)

        self.play(FadeIn(band), FadeIn(band_tag), run_time=self.share(0.2))
        # "... worse than using no predictors at all."
        self.wait(self.share(0.2))
        self.play(Create(mean_line), FadeIn(mean_name), run_time=self.share(0.25))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        curve = self.data("u-curve")
        axes, training, test = full_u(self, curve)
        self.play(test[0].animate.set_stroke(opacity=0.3), test[1].animate.set_opacity(0.3),
                  run_time=self.share(0.15))
        glow = training[0].copy().set_stroke(SKY, width=16)
        self.play(ShowPassingFlash(glow, time_width=0.4), run_time=self.share(0.4))
        self.play(Flash(training[1][-1], color=BLUE), run_time=self.share(0.15))
        self.finish()


# Diagnosis (scenes 23–24, schematic) ---------------------------------------------------

def bar_pair(heading, training, new):
    """Two unlabelled bars, training and new data; heights are relative, not results."""
    base = Line(LEFT * 1.7, RIGHT * 1.7, color=GRID, stroke_width=3)
    bars = VGroup()
    for i, (h, colour) in enumerate([(training, BLUE), (new, VERMILION)]):
        bar = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=colour, fill_opacity=1)
        bar.next_to(base, UP, 0).shift((i - 0.5) * 1.6 * RIGHT)
        bars.add(bar)
    names = VGroup(*[label(t, 26, SUBDUED).move_to([b.get_x(), base.get_y() - 0.3, 0])
                     for t, b in zip(["training", "new data"], bars)])
    head = label(heading, 34, weight=BOLD).next_to(base, UP, 3.4)
    return VGroup(base, bars, names, head), bars


def diagnosis():
    under, under_bars = bar_pair("both poor, about equal", 2.3, 2.5)
    over, over_bars = bar_pair("good, then much worse", 0.5, 2.9)
    VGroup(under, over).arrange(RIGHT, buff=2.2).shift(0.2 * DOWN + 0.7 * LEFT)
    under_name = label("underfitting", 42, ORANGE, weight=BOLD).next_to(under, DOWN, 0.5)
    over_name = label("overfitting", 42, PURPLE, weight=BOLD).next_to(over, DOWN, 0.5)
    return under, under_bars, under_name, over, over_bars, over_name


class Scene23(VideoScene):
    number = 23

    def construct(self):
        under, under_bars, under_name, *_ = diagnosis()
        self.add(schematic_note())
        # "So read both errors together."
        self.play(FadeIn(under[3]), FadeIn(under[0]), FadeIn(under[2]),
                  GrowFromEdge(under_bars[0], DOWN), GrowFromEdge(under_bars[1], DOWN),
                  run_time=self.share(0.25))
        self.wait(self.share(0.25))
        # "Both poor, and about equal: that is underfitting."
        self.play(FadeIn(under_name, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        under, under_bars, under_name, over, over_bars, over_name = diagnosis()
        self.add(schematic_note(), under, under_name)
        x = over_bars[1].get_right()[0] + 0.25
        span = Line([x, over_bars[0].get_top()[1], 0], [x, over_bars[1].get_top()[1], 0])
        brace = Brace(span, RIGHT, color=INK)
        gap = label("the gap", 34, INK, weight=BOLD).next_to(brace, RIGHT, 0.15)

        self.play(FadeIn(over[3]), FadeIn(over[0]), FadeIn(over[2]),
                  GrowFromEdge(over_bars[0], DOWN), run_time=self.share(0.12))
        self.play(GrowFromEdge(over_bars[1], DOWN), run_time=self.share(0.15))
        self.play(FadeIn(over_name, shift=0.2 * UP), run_time=self.share(0.1))
        # "The gap is the tell."
        self.wait(self.share(0.25))
        self.play(GrowFromCenter(brace), FadeIn(gap), run_time=self.share(0.12))
        self.finish()


# Noise columns (scene 25 schematic; 26–27 real data) --------------------------------------

def survey_table(noise_columns):
    """A small table: three real predictor columns, then columns of random digits."""
    rng = np.random.default_rng(16)
    headers = ["depth", "temp.", "chl."] + [f"noise {i}" for i in range(1, noise_columns + 1)]
    columns = VGroup()
    for j, name in enumerate(headers):
        noise = j >= 3
        colour = VERMILION if noise else INK
        cells = [label(name, 22, colour, weight=BOLD)]
        for _ in range(6):
            value = rng.normal() if noise else rng.uniform(1, 9)
            cells.append(label(f"{value:.2f}" if noise else "· · ·", 22,
                               colour if noise else SUBDUED))
        for row, cell in enumerate(cells):
            cell.move_to(0.62 * row * DOWN)
        columns.add(VGroup(*cells))
    columns.arrange(RIGHT, buff=0.45, aligned_edge=UP)
    return columns.scale_to_fit_width(min(columns.width * 1.5, 12.5))


class Scene25(VideoScene):
    number = 25

    def construct(self):
        full = survey_table(5).move_to(ORIGIN)
        real, noise = full[:3], full[3:]
        start = real.copy().move_to(ORIGIN)
        rule = Line(LEFT, RIGHT, color=GRID).set_width(full.width + 0.4)
        rule.next_to(full[0][0], DOWN, 0.16).set_x(0)

        self.add(schematic_note())
        self.wait(self.share(0.2))
        # "Take three real predictors, ..."
        self.play(FadeIn(start), run_time=self.share(0.12))
        self.play(ReplacementTransform(start, real), FadeIn(rule), run_time=self.share(0.08))
        # "... and add columns of pure random numbers."
        self.play(LaggedStart(*[FadeIn(c, shift=0.3 * LEFT) for c in noise], lag_ratio=0.35),
                  run_time=self.share(0.4))
        self.finish()


class Scene26(VideoScene):
    number = 26

    def construct(self):
        rows = self.data("noise-columns")
        stations = int(rows["stations"].iloc[0])
        head = label("training R²", 40, weight=BOLD)
        track = Rectangle(width=9.0, height=0.6, stroke_color=GRID, stroke_width=2)
        VGroup(head, track).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(0.8 * UP + 0.6 * LEFT)
        counter_name = label("noise columns", 32, SUBDUED).next_to(track, DOWN, 0.9, aligned_edge=LEFT)
        station_note = label(f"on {stations} stations", 32, SUBDUED)
        station_note.next_to(counter_name, DOWN, 0.3, aligned_edge=LEFT)

        def bar(r2):
            return Rectangle(width=max(track.width * r2, 0.01), height=track.height,
                             stroke_width=0, fill_color=ORANGE, fill_opacity=1
                             ).align_to(track, LEFT).align_to(track, DOWN)

        def readouts(row):
            value = label(f"{row['training_r2']:.3f}", 44, ORANGE, weight=BOLD).next_to(track, RIGHT, 0.3)
            count = label(str(int(row["noise_columns"])), 32, INK, weight=BOLD).next_to(counter_name, RIGHT, 0.3)
            return value, count

        fill = bar(rows.iloc[0]["training_r2"])
        value, count = readouts(rows.iloc[0])
        self.play(FadeIn(head), FadeIn(track), FadeIn(fill), FadeIn(value),
                  FadeIn(counter_name), FadeIn(count), FadeIn(station_note),
                  run_time=self.share(0.1))
        # Step through the page's own rows only: no value between them is shown.
        step = self.share(0.55) / (len(rows) - 1)
        for _, row in rows.iloc[1:].iterrows():
            new_value, new_count = readouts(row)
            self.play(Transform(fill, bar(row["training_r2"])),
                      Transform(value, new_value), Transform(count, new_count), run_time=step)
        perfect = label("a perfect fit", 36, ORANGE, weight=BOLD).next_to(track, UP, 0.3, aligned_edge=RIGHT)
        self.play(FadeIn(perfect, shift=0.2 * UP), Indicate(value, color=ORANGE),
                  run_time=self.share(0.12))
        self.finish()


class Scene27(VideoScene):
    number = 27

    def construct(self):
        rows = self.data("noise-columns")
        last = rows.iloc[-1]
        largest = int(last["largest_catch"])
        width = 11.0
        scale = width / last["test_rmse"]

        head = label("error on new stations", 36, weight=BOLD).to_edge(UP, buff=1.2).to_edge(LEFT, buff=1.2)
        catch = Rectangle(width=largest * scale, height=0.6, stroke_width=0,
                          fill_color=GREY, fill_opacity=1).next_to(head, DOWN, 0.7, aligned_edge=LEFT)
        catch_tag = label(f"largest catch: {largest}", 30, GREY).next_to(catch, RIGHT, 0.25)
        error = Rectangle(width=rows["test_rmse"].iloc[0] * scale, height=0.6, stroke_width=0,
                          fill_color=VERMILION, fill_opacity=1).next_to(catch, DOWN, 0.9, aligned_edge=LEFT)
        value = label(f"{last['test_rmse']:.0f}", 64, VERMILION, weight=BOLD)

        self.play(FadeIn(head), FadeIn(error), run_time=self.share(0.1))
        # "On new stations, its error is 185, ..."
        self.play(error.animate.stretch_to_fit_width(width, about_edge=LEFT),
                  run_time=self.share(0.25), rate_func=rush_into)
        value.next_to(error, DOWN, 0.3).align_to(error, RIGHT)
        self.play(FadeIn(value, scale=1.5), run_time=self.share(0.1))
        # "... in a survey whose largest catch is 40."
        self.wait(self.share(0.1))
        self.play(GrowFromEdge(catch, LEFT), FadeIn(catch_tag), run_time=self.share(0.15))
        self.finish()


# Flexibility against data (scene 28, schematic) --------------------------------------------

class Scene28(VideoScene):
    number = 28

    def construct(self):
        count = label("number of parameters", 44, SUBDUED).move_to(1.6 * UP)
        strike = Line(count.get_left(), count.get_right(), color=VERMILION, stroke_width=6)

        pivot = Triangle(color=INK, fill_opacity=1).scale(0.45).move_to(2.2 * DOWN)
        beam = Line(4.2 * LEFT, 4.2 * RIGHT, color=INK, stroke_width=8).next_to(pivot, UP, 0)
        flex = Square(1.3, stroke_width=0, fill_color=VERMILION, fill_opacity=1)
        data = Square(0.7, stroke_width=0, fill_color=BLUE, fill_opacity=1)
        flex.next_to(beam.get_left() + 0.9 * RIGHT, UP, 0)
        data.next_to(beam.get_right() + 0.9 * LEFT, UP, 0)
        flex_name = label("flexibility", 32, VERMILION, weight=BOLD).next_to(flex, UP, 0.2)
        data_name = label("data", 32, BLUE, weight=BOLD).next_to(data, UP, 0.2)
        saw = VGroup(beam, flex, data, flex_name, data_name)
        tilt = 0.18

        self.add(schematic_note())
        # "What matters is not the number of parameters."
        self.play(FadeIn(count), run_time=self.share(0.12))
        self.play(Create(strike), run_time=self.share(0.12))
        self.play(FadeOut(count), FadeOut(strike), FadeIn(pivot), FadeIn(saw), run_time=self.share(0.1))
        # "It is flexibility, ..."
        self.play(Rotate(saw, tilt, about_point=beam.get_center()), run_time=self.share(0.15))
        # "... compared with how much data you have."
        big = Square(1.3, stroke_width=0, fill_color=BLUE, fill_opacity=1)
        big.rotate(tilt).move_to(data.get_center() + 0.3 * rotate_vector(UP, tilt))
        self.play(Transform(data, big), data_name.animate.shift(0.7 * UP), run_time=self.share(0.15))
        self.play(Rotate(saw, -tilt, about_point=beam.get_center()), run_time=self.share(0.15))
        self.finish()


# Bias and variance targets (scenes 29–31, schematic) -----------------------------------------

def target(centre=ORIGIN, radius=1.9):
    rings = VGroup(*[Circle(radius=radius * k / 4, color=GRID, stroke_width=3)
                     for k in range(1, 5)]).move_to(centre)
    bull = Dot(centre, radius=0.09, color=INK)
    tag = label("true value", 24, SUBDUED).next_to(bull, DOWN, 0.15)
    return VGroup(rings, bull, tag)


def hits(centre, offset, spread, seed, colour, n=14):
    rng = np.random.default_rng(seed)
    points = rng.normal(0, spread, (n, 2)) + np.array(offset)
    return VGroup(*[Dot(centre + np.array([a, b, 0]), radius=0.08, color=colour)
                    for a, b in points])


class Scene29(VideoScene):
    number = 29

    def construct(self):
        board = target()
        surveys = VGroup(*[label(f"survey {i}", 26, SUBDUED) for i in range(1, 5)]
                         ).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=1.2)
        self.add(schematic_note())
        self.play(FadeIn(board, scale=0.9), run_time=self.share(0.12))
        # "Imagine repeating the survey many times, ..."
        self.play(LaggedStart(*[FadeIn(s, shift=0.2 * RIGHT) for s in surveys], lag_ratio=0.4),
                  run_time=self.share(0.35))
        self.play(*[Indicate(s, color=BLUE) for s in surveys], run_time=self.share(0.2))
        self.finish()


LEFT_BOARD, RIGHT_BOARD = 3.4 * LEFT + 0.3 * DOWN, 3.4 * RIGHT + 0.3 * DOWN


def bias_board():
    board = target(LEFT_BOARD)
    shots = hits(LEFT_BOARD, [0.95, 0.75], 0.14, 21, ORANGE)
    name = label("bias", 46, ORANGE, weight=BOLD).next_to(board, UP, 0.35)
    return board, shots, name


class Scene30(VideoScene):
    number = 30

    def construct(self):
        board, shots, name = bias_board()
        centre = target()
        self.add(schematic_note(), centre)
        self.play(ReplacementTransform(centre, board), FadeIn(name), run_time=self.share(0.12))
        self.play(LaggedStart(*[FadeIn(s, scale=2) for s in shots], lag_ratio=0.2),
                  run_time=self.share(0.3))
        # "... like a thermometer that always reads high."
        arrow = Arrow(board[1].get_center(), shots.get_center(), buff=0.12,
                      color=INK, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(arrow), run_time=self.share(0.12))
        self.finish()


class Scene31(VideoScene):
    number = 31

    def construct(self):
        board, shots, name = bias_board()
        self.add(schematic_note(), board, shots, name)
        right = target(RIGHT_BOARD)
        scatter = hits(RIGHT_BOARD, [0, 0], 0.72, 22, SKY)
        right_name = label("variance", 46, BLUE, weight=BOLD).next_to(right, UP, 0.35)
        self.play(FadeIn(right), FadeIn(right_name), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(s, scale=2) for s in scatter], lag_ratio=0.2),
                  run_time=self.share(0.4))
        self.play(Indicate(scatter, color=BLUE, scale_factor=1.08), run_time=self.share(0.15))
        self.finish()


# Bias², variance and the noise floor (scenes 32–35, real data) ----------------------------------

def decomposition_axes(table):
    knobs = table["minbucket"].to_numpy()
    xs = -np.log10(knobs)
    top = float(np.ceil(max(table["total"].max(), table["irreducible"].iloc[0]) / 5) * 5)
    axes = Axes(x_range=[xs.min(), xs.max(), 1], y_range=[0, top, 5], x_length=10, y_length=5.2,
                tips=False, axis_config={"color": GRID, "include_ticks": False}
                ).shift(0.3 * DOWN + 0.2 * LEFT)
    xt = VGroup(*[label(str(k), 24, SUBDUED).next_to(axes.c2p(x, 0), DOWN, 0.2)
                  for k, x in zip(knobs, xs)])
    yt = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(xs.min(), v), LEFT, 0.2)
                  for v in range(0, int(top) + 1, 5)])
    xl = label("stations per leaf: more flexible to the right", 28, SUBDUED).next_to(xt, DOWN, 0.25)
    yl = label("squared error", 28, SUBDUED).rotate(PI / 2).next_to(yt, LEFT, 0.25)

    def trace(column, colour):
        return VMobject(color=colour, stroke_width=6).set_points_as_corners(
            [axes.c2p(x, v) for x, v in zip(xs, table[column])])

    lines = dict(bias2=trace("bias2", BLUE), variance=trace("variance", GREEN),
                 total=trace("total", ORANGE))
    names = dict(
        bias2=label("bias²", 30, BLUE, weight=BOLD).next_to(lines["bias2"].get_end(), RIGHT, 0.2),
        variance=label("variance", 30, GREEN, weight=BOLD).next_to(lines["variance"].get_end(), RIGHT, 0.2),
        total=label("sum", 30, ORANGE, weight=BOLD).next_to(lines["total"].get_end(), RIGHT, 0.2))
    floor_y = table["irreducible"].iloc[0]
    floor = DashedLine(axes.c2p(xs.min(), floor_y), axes.c2p(xs.max(), floor_y), color=GREY,
                       stroke_width=5)
    floor_name = label("noise no model can remove", 28, GREY).next_to(floor, UP, 0.12)
    return VGroup(axes, xt, yt, xl, yl), lines, names, floor, floor_name


class Scene32(VideoScene):
    number = 32

    def construct(self):
        frame, lines, names, *_ = decomposition_axes(self.data("decomposition"))
        self.play(FadeIn(frame), run_time=self.share(0.1))
        # "Bias falls, then stops."
        self.wait(self.share(0.25))
        self.play(Create(lines["bias2"]), FadeIn(names["bias2"]), run_time=self.share(0.25))
        # "Variance keeps rising."
        self.play(Create(lines["variance"]), FadeIn(names["variance"]), run_time=self.share(0.25))
        self.finish()


class Scene33(VideoScene):
    number = 33

    def construct(self):
        frame, lines, names, *_ = decomposition_axes(self.data("decomposition"))
        self.add(frame, lines["bias2"], lines["variance"], names["bias2"], names["variance"])
        self.play(TransformFromCopy(VGroup(lines["bias2"], lines["variance"]), lines["total"]),
                  run_time=self.share(0.4))
        self.play(FadeIn(names["total"]), run_time=self.share(0.15))
        self.play(lines["total"].animate.set_stroke(width=10), run_time=self.share(0.15))
        self.finish()


class Scene34(VideoScene):
    number = 34

    def construct(self):
        frame, lines, names, floor, floor_name = decomposition_axes(self.data("decomposition"))
        self.add(frame, *lines.values(), *names.values())
        self.wait(self.share(0.2))
        # "... a floor: noise that no model can remove."
        self.play(FadeIn(floor, shift=0.6 * DOWN), run_time=self.share(0.25))
        self.play(FadeIn(floor_name), run_time=self.share(0.15))
        self.finish()


class Scene35(VideoScene):
    number = 35

    def construct(self):
        table = self.data("decomposition")
        floor_value = table["irreducible"].iloc[0]
        reachable = table["total"].min()
        base = Line(5 * LEFT, 5 * RIGHT, color=GRID, stroke_width=3).shift(2.3 * DOWN)
        scale = 4.6 / floor_value
        bars = VGroup()
        for i, (value, colour, text) in enumerate(
                [(reachable, ORANGE, "what a model can control"),
                 (floor_value, GREY, "noise no model removes")]):
            bar = Rectangle(width=2.2, height=value * scale, stroke_width=0, fill_color=colour,
                            fill_opacity=1).next_to(base, UP, 0).set_x((i - 0.5) * 5.2)
            number = label(f"{value:.1f}", 40, colour, weight=BOLD).next_to(bar, UP, 0.2)
            name = label(text, 28, SUBDUED).next_to(base, DOWN, 0.3).set_x(bar.get_x())
            bars.add(VGroup(bar, number, name))
        self.play(FadeIn(base), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]),
                  run_time=self.share(0.15))
        # "Here it is more than double everything a model can control."
        self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), run_time=self.share(0.25))
        self.play(Indicate(bars[1][1], color=GREY), run_time=self.share(0.15))
        self.finish()


# Ridge (scene 36 schematic; 37–38 real data) -------------------------------------------------

class Scene36(VideoScene):
    number = 36

    def construct(self):
        start = np.array([1.9, -1.4, 1.1, 0.6, -2.1, 0.35, -0.8, 1.5])
        penalty = ValueTracker(0)
        baseline = Line(5 * LEFT, 5 * RIGHT, color=GRID, stroke_width=3).shift(0.4 * DOWN)
        xs = np.linspace(-4.2, 4.2, start.size)

        def bars():
            shrink = 1 / (1 + 4 * penalty.get_value())
            group = VGroup()
            for x, c in zip(xs, start * shrink):
                height = max(abs(c), 0.001)
                bar = Rectangle(width=0.62, height=height, stroke_width=0,
                                fill_color=BLUE if c > 0 else VERMILION, fill_opacity=1)
                bar.move_to(baseline.get_center() + np.array([x, np.sign(c) * height / 2, 0]))
                group.add(bar)
            return group

        coefficients = always_redraw(bars)
        caption = label("coefficients", 30, SUBDUED).to_corner(UL, buff=0.8)
        slider = Line(3 * LEFT, 3 * RIGHT, color=GRID, stroke_width=6).to_edge(DOWN, buff=0.9)
        knob = always_redraw(lambda: Dot(slider.point_from_proportion(penalty.get_value()),
                                         radius=0.16, color=INK))
        slider_name = label("penalty", 32, INK).next_to(slider, LEFT, 0.4)

        self.add(schematic_note())
        self.play(FadeIn(baseline), FadeIn(coefficients), FadeIn(caption), run_time=self.share(0.12))
        self.play(FadeIn(slider), FadeIn(knob), FadeIn(slider_name), run_time=self.share(0.12))
        # "... so they shrink towards zero."
        self.play(penalty.animate.set_value(1), run_time=self.share(0.55), rate_func=smooth)
        self.finish()


RIDGE_COLOURS = {"Least squares": VERMILION, "Predict the mean": GREY, "Ridge": BLUE}


def ridge_bars(rows):
    base = Line(5 * LEFT, 5 * RIGHT, color=GRID, stroke_width=3).shift(2.3 * DOWN)
    scale = 4.2 / rows["rmse"].max()
    bars = VGroup()
    for i, (_, r) in enumerate(rows.iterrows()):
        colour = RIDGE_COLOURS[r["method"]]
        bar = Rectangle(width=2.0, height=r["rmse"] * scale, stroke_width=0,
                        fill_color=colour, fill_opacity=1)
        bar.next_to(base, UP, 0).set_x((i - 1) * 3.2)
        value = label(f"{r['rmse']:.2f}", 36, colour, weight=BOLD).next_to(bar, UP, 0.2)
        name = label(r["method"], 28, SUBDUED).next_to(base, DOWN, 0.3).set_x(bar.get_x())
        bars.add(VGroup(bar, value, name))
    head = label(f"{int(rows['predictors'].iloc[0])} predictors, "
                 f"{int(rows['stations'].iloc[0])} training stations", 32, SUBDUED).to_edge(UP, buff=0.6)
    sub = label("error on new stations", 28, SUBDUED).next_to(head, DOWN, 0.15)
    return VGroup(head, sub), base, bars


class Scene37(VideoScene):
    number = 37

    def construct(self):
        head, base, bars = ridge_bars(self.data("ridge-bars"))
        self.play(FadeIn(head), FadeIn(base), run_time=self.share(0.15))
        # "... least squares did worse than guessing the mean."
        for group in bars[:2]:
            self.play(GrowFromEdge(group[0], DOWN), FadeIn(group[1]), FadeIn(group[2]),
                      run_time=self.share(0.18))
            self.wait(self.share(0.1))
        self.finish()


class Scene38(VideoScene):
    number = 38

    def construct(self):
        head, base, bars = ridge_bars(self.data("ridge-bars"))
        self.add(head, base, bars[:2])
        self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]), FadeIn(bars[2][2]),
                  run_time=self.share(0.4))
        self.play(Indicate(bars[2][1], color=BLUE), run_time=self.share(0.3))
        self.finish()


# Lasso's unstable choices (scenes 39–40, real data) ------------------------------------------

def stability_dots(table):
    axis = NumberLine(x_range=[0, 0.6, 0.1], length=11, color=GRID, include_ticks=False)
    axis.shift(2.4 * DOWN)
    ticks = VGroup(*[label(f"{int(round(v * 100))}%", 24, SUBDUED).next_to(axis.n2p(v), DOWN, 0.2)
                     for v in (0, 0.2, 0.4, 0.6)])
    name = label("share of 100 resampled fits that kept the predictor", 28, SUBDUED).next_to(ticks, DOWN, 0.2)

    def stacked(values, base_y, colour):
        dots, seen = VGroup(), {}
        for v in values:
            k = round(v, 2)
            level = seen.get(k, 0)
            seen[k] = level + 1
            dots.add(Dot([axis.n2p(v)[0], base_y + 0.24 * level, 0], radius=0.1, color=colour))
        return dots

    real = table["kind"].to_numpy() == "real term"
    mixed = stacked(table["selected_in"], -1.9, BLUE)
    rows = {True: iter(stacked(table["selected_in"][real], 0.9, ORANGE)),
            False: iter(stacked(table["selected_in"][~real], -1.3, GREY))}
    # Each term's place in its own row, in the table's order, so every dot can move there.
    split = VGroup(*[next(rows[r]) for r in real])
    return VGroup(axis, ticks, name), mixed, split, axis


class Scene39(VideoScene):
    number = 39

    def construct(self):
        frame, mixed, *_ = stability_dots(self.data("lasso-stability"))
        head = label("one dot per predictor", 32, SUBDUED).to_edge(UP, buff=0.8)
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d, shift=0.3 * DOWN) for d in mixed], lag_ratio=0.03),
                  run_time=self.share(0.45))
        self.finish()


class Scene40(VideoScene):
    number = 40

    def construct(self):
        table = self.data("lasso-stability")
        frame, mixed, split, axis = stability_dots(table)
        self.add(frame, mixed)
        self.play(*[Transform(m, s) for m, s in zip(mixed, split)], run_time=self.share(0.3))
        names = VGroup(label("real predictors", 30, ORANGE, weight=BOLD).move_to([-4.6, 2.3, 0]),
                       label("pure noise", 30, GREY, weight=BOLD).move_to([-4.6, -0.2, 0]))
        self.play(FadeIn(names), run_time=self.share(0.1))
        # Their averages, from the page's own table.
        marks = VGroup()
        for kind, y, colour in (("real term", 2.1, ORANGE), ("noise column", -0.4, GREY)):
            mean = table.loc[table["kind"] == kind, "selected_in"].mean()
            x = axis.n2p(mean)[0]
            line = DashedLine([x, y + 0.15, 0], [x, y - 1.6, 0], color=colour, stroke_width=4)
            tag = label(f"average {mean * 100:.0f}%", 26, colour, weight=BOLD).next_to(line, UP, 0.05)
            marks.add(VGroup(line, tag))
        self.play(*[Create(m[0]) for m in marks], *[FadeIn(m[1]) for m in marks],
                  run_time=self.share(0.2))
        self.finish()


# Peeking at the test set (scenes 41–42, schematic) ------------------------------------------

def test_box():
    body = RoundedRectangle(width=3.6, height=2.3, corner_radius=0.15,
                            stroke_color=INK, stroke_width=4, fill_color="#F2F5F7", fill_opacity=1)
    lid = RoundedRectangle(width=3.9, height=0.45, corner_radius=0.1,
                           stroke_color=INK, stroke_width=4, fill_color="#E3E9ED", fill_opacity=1)
    lid.next_to(body, UP, 0)
    name = label("test set", 40, weight=BOLD).move_to(body)
    return body, lid, name


def peek(scene, lid, run_time, mark=None):
    """Lift the lid (adding a mark to the tally of looks, if given) and close it again."""
    hinge = lid.get_corner(DL)
    extra = [FadeIn(mark, scale=1.6)] if mark is not None else []
    scene.play(Rotate(lid, angle=0.55, about_point=hinge), *extra, run_time=run_time / 2)
    scene.play(Rotate(lid, angle=-0.55, about_point=hinge), run_time=run_time / 2)


def peek_layout():
    body, lid, name = test_box()
    box = VGroup(body, lid, name).shift(0.4 * UP)
    marks = VGroup(*[Circle(radius=0.16, color=VERMILION, fill_opacity=1, stroke_width=0)
                     for _ in range(5)]).arrange(RIGHT, buff=0.3).next_to(box, DOWN, 0.8)
    looks = label("looks at the test set", 28, SUBDUED).next_to(marks, DOWN, 0.25)
    return body, lid, name, box, marks, looks


class Scene41(VideoScene):
    number = 41

    def construct(self):
        body, lid, name, box, marks, looks = peek_layout()
        self.add(schematic_note())
        self.play(FadeIn(box), run_time=self.share(0.1))
        self.wait(self.share(0.1))
        self.play(FadeIn(looks), run_time=self.share(0.05))
        for mark in marks:
            peek(self, lid, self.share(0.11), mark)
        self.finish()


class Scene42(VideoScene):
    number = 42

    def construct(self):
        body, lid, name, box, marks, looks = peek_layout()
        self.add(schematic_note(), box, marks, looks)
        again = label("training set, again", 30, VERMILION, weight=BOLD).move_to(body)
        # "Look, adjust, look again, ..."
        peek(self, lid, self.share(0.25))
        self.play(body.animate.set_stroke(VERMILION), lid.animate.set_stroke(VERMILION),
                  run_time=self.share(0.1))
        self.play(ReplacementTransform(name, again), run_time=self.share(0.2))
        self.finish()


# Cross-validation (scenes 43–44, schematic) --------------------------------------------------

def cv_layout():
    folds = VGroup(*[Rectangle(width=0.95, height=0.8, stroke_color=BACKGROUND,
                               stroke_width=4, fill_color=BLUE, fill_opacity=1)
                     for _ in range(10)]).arrange(RIGHT, buff=0)
    training = label("training data", 30, SUBDUED).next_to(folds, UP, 0.3)
    body, lid, name = test_box()
    box = VGroup(body, lid, name).scale(0.6)
    VGroup(VGroup(training, folds), box).arrange(RIGHT, buff=0.9).shift(0.3 * UP)
    split = folds.copy().arrange(RIGHT, buff=0.1).move_to(folds)
    legend = VGroup(
        VGroup(Square(0.3, fill_color=BLUE, fill_opacity=1, stroke_width=0),
               label("fit on these", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
        VGroup(Square(0.3, fill_color=ORANGE, fill_opacity=1, stroke_width=0),
               label("scored on this", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
    ).arrange(RIGHT, buff=0.6).next_to(folds, DOWN, 0.6)
    seal = label("sealed", 26, VERMILION, weight=BOLD).next_to(box, DOWN, 0.2)
    return folds, split, training, box, lid, legend, seal


class Scene43(VideoScene):
    number = 43

    def construct(self):
        folds, split, training, box, lid, legend, seal = cv_layout()
        self.add(schematic_note())
        self.play(FadeIn(training), FadeIn(folds), FadeIn(box), FadeIn(seal),
                  run_time=self.share(0.15))
        # "Split the training data into ten folds."
        self.wait(self.share(0.3))
        self.play(Transform(folds, split), run_time=self.share(0.25))
        self.finish()


class Scene44(VideoScene):
    number = 44

    def construct(self):
        folds, split, training, box, lid, legend, seal = cv_layout()
        self.add(schematic_note(), training, split, box, seal)
        self.play(FadeIn(legend), run_time=self.share(0.06))
        # "Fit on nine, score on the tenth, and rotate."
        step = self.share(0.045)
        for i in range(10):
            self.play(split[i].animate.set_fill(ORANGE),
                      *[split[j].animate.set_fill(BLUE) for j in range(10) if j != i],
                      run_time=step)
        self.play(*[f.animate.set_fill(BLUE) for f in split], run_time=self.share(0.04))
        # "Open the test set once, at the very end."
        hinge = lid.get_corner(DL)
        self.play(Rotate(lid, angle=0.6, about_point=hinge), FadeOut(seal), run_time=self.share(0.08))
        once = label("once", 32, GREEN, weight=BOLD).next_to(box, DOWN, 0.2)
        self.play(FadeIn(once, scale=1.3), run_time=self.share(0.06))
        self.finish()


# Forty validation splits, sixteen winners (scenes 45–46, real data) ----------------------------

DEPTHS = [2, 3, 4, 6, 8, 12]
MIN_NS = [2, 5, 10, 20, 40, 80]
CHOSEN = "#FBE3D6"


def instability_grid():
    cells = VGroup(*[Square(0.9, stroke_color=GRID, stroke_width=2, fill_color="#F7F9FA",
                            fill_opacity=1) for _ in range(36)])
    cells.arrange_in_grid(rows=6, cols=6, buff=0.06)
    cells.shift(1.8 * LEFT + 0.1 * DOWN)

    def cell(depth, min_n):   # depth rises upwards, min_n to the right
        return cells[(5 - DEPTHS.index(depth)) * 6 + MIN_NS.index(min_n)]

    xt = VGroup(*[label(str(m), 24, SUBDUED).next_to(cell(2, m), DOWN, 0.2) for m in MIN_NS])
    yt = VGroup(*[label(str(d), 24, SUBDUED).next_to(cell(d, 2), LEFT, 0.2) for d in DEPTHS])
    xl = label("stations needed to split", 26, SUBDUED).next_to(xt, DOWN, 0.2)
    yl = label("tree depth", 26, SUBDUED).rotate(PI / 2).next_to(yt, LEFT, 0.25)
    return VGroup(cells, xt, yt, xl, yl), cell


def winner_dots(winners, cell):
    """One dot per validation split, stacked in the cell it chose."""
    placed, dots = {}, []
    for _, w in winners.iterrows():
        key = (int(w["tree_depth"]), int(w["min_n"]))
        k = placed.get(key, 0)
        placed[key] = k + 1
        corner = cell(*key).get_corner(UL)
        dots.append((key, Dot(corner + np.array([0.16 + 0.19 * (k % 4), -0.16 - 0.19 * (k // 4), 0]),
                              radius=0.07, color=VERMILION)))
    return dots


class Scene45(VideoScene):
    number = 45

    def construct(self):
        winners = self.data("winners")
        frame, cell = instability_grid()
        counter_name = label("different winners", 30, SUBDUED).move_to([4.6, 1.2, 0])
        splits_name = label("validation splits", 30, SUBDUED).move_to([4.6, -0.8, 0])

        def count_text(n, y, colour):
            return label(str(n), 60, colour, weight=BOLD).move_to([4.6, y, 0])

        distinct = count_text(0, 0.4, VERMILION)
        splits = count_text(0, -1.6, INK)
        self.play(FadeIn(frame), FadeIn(counter_name), FadeIn(splits_name), FadeIn(distinct),
                  FadeIn(splits), run_time=self.share(0.1))
        # "Forty validation splits chose sixteen different winners."
        seen = set()
        step = self.share(0.6) / len(winners)
        for n, (key, dot) in enumerate(winner_dots(winners, cell), 1):
            seen.add(key)
            self.play(FadeIn(dot, shift=0.3 * DOWN), cell(*key).animate.set_fill(CHOSEN),
                      Transform(distinct, count_text(len(seen), 0.4, VERMILION)),
                      Transform(splits, count_text(n, -1.6, INK)), run_time=step)
        self.finish()


class Scene46(VideoScene):
    number = 46

    def construct(self):
        winners = self.data("winners")
        frame, cell = instability_grid()
        dots = winner_dots(winners, cell)
        for key, _ in dots:
            cell(*key).set_fill(CHOSEN)
        self.add(frame, *[d for _, d in dots])
        simple = cell(2, 80)
        arrow = Arrow(cell(8, 10).get_center(), simple.get_center(), color=GREEN,
                      stroke_width=8, buff=0.4)
        tag = label("simpler", 34, GREEN, weight=BOLD).next_to(simple, RIGHT, 0.3)
        self.play(GrowArrow(arrow), run_time=self.share(0.3))
        self.play(FadeIn(tag, shift=0.2 * RIGHT), Indicate(simple, color=GREEN), run_time=self.share(0.25))
        self.finish()


# Repeat visits (scenes 47–48, schematic apart from the 160 sites) ------------------------------

def repeat_visits():
    # 160 sites is from the page; how visits split between the sets is illustrative.
    rng = np.random.default_rng(33)
    sites = VGroup()
    for _ in range(160):
        visits = rng.integers(2, 6)
        stack = VGroup(*[Square(0.14, stroke_width=0, fill_opacity=1,
                                fill_color=BLUE if rng.random() < 0.75 else ORANGE)
                         for _ in range(visits)]).arrange(UP, buff=0.03)
        sites.add(stack)
    sites.arrange_in_grid(rows=8, cols=20, buff=(0.8, 0.18), aligned_edge=DOWN)
    heading = label("160 sites, each visited again and again", 34).to_edge(UP, buff=0.5)
    sites.scale_to_fit_height(5.2).next_to(heading, DOWN, 0.4)
    legend = VGroup(
        VGroup(Square(0.26, fill_color=BLUE, fill_opacity=1, stroke_width=0),
               label("training", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
        VGroup(Square(0.26, fill_color=ORANGE, fill_opacity=1, stroke_width=0),
               label("test", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
    ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.35)
    both = [s for s in sites if len({sq.get_fill_color().to_hex() for sq in s}) > 1]
    return heading, sites, legend, both


class Scene47(VideoScene):
    number = 47

    def construct(self):
        heading, sites, legend, both = repeat_visits()
        grey = sites.copy().set_fill(GREY)
        self.add(schematic_note())
        self.play(FadeIn(heading), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(s) for s in grey], lag_ratio=0.01), run_time=self.share(0.5))
        self.finish()


class Scene48(VideoScene):
    number = 48

    def construct(self):
        heading, sites, legend, both = repeat_visits()
        grey = sites.copy().set_fill(GREY)
        self.add(schematic_note(), heading, grey)
        # "A random split puts the same site on both sides, ..."
        self.play(Transform(grey, sites), FadeIn(legend), run_time=self.share(0.2))
        self.play(*[Circumscribe(s, color=VERMILION, buff=0.04, stroke_width=3)
                    for s in both[:24]], run_time=self.share(0.25))
        # "Section seven puts that right."
        seven = label("→ section 7", 34, GREEN, weight=BOLD).to_corner(DR, buff=0.9)
        self.play(FadeIn(seven, shift=0.2 * LEFT), run_time=self.share(0.1))
        self.finish()


# Quiz (scenes 49–50) ---------------------------------------------------------------------------

class Scene49(VideoScene):
    number = 49

    def construct(self):
        head = label("Quick quiz", 40, BLUE, weight=BOLD).to_edge(UP, buff=1.0)
        question = VGroup(label("You add a column of random numbers", 48),
                          label("to a regression.", 48),
                          label("Can its training R² go down?", 48, weight=BOLD)
                          ).arrange(DOWN, buff=0.3).next_to(head, DOWN, 0.8)
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(q) for q in question], lag_ratio=0.8), run_time=self.share(0.55))
        self.finish()
        # The pause after the question: a bar that empties, so viewers know to think.
        track = Rectangle(width=8, height=0.3, stroke_color=GRID, stroke_width=2).to_edge(DOWN, buff=1.2)
        left = ValueTracker(1.0)
        bar = always_redraw(lambda: Rectangle(width=max(8 * left.get_value(), 0.001), height=0.3,
                                              stroke_width=0, fill_color=BLUE, fill_opacity=1
                                              ).align_to(track, LEFT).align_to(track, DOWN))
        think = label("think about it", 28, SUBDUED).next_to(track, UP, 0.2)
        self.play(FadeIn(track), FadeIn(bar), FadeIn(think), run_time=0.3)
        self.play(left.animate.set_value(0), run_time=max(self.pause - 0.6, 0.5), rate_func=linear)


class Scene50(VideoScene):
    number = 50

    def construct(self):
        rows = self.data("noise-columns")
        no = label("No.", 80, VERMILION, weight=BOLD).to_edge(UP, buff=0.7)
        base = Line(5.5 * LEFT, 5.5 * RIGHT, color=GRID, stroke_width=3).shift(2.2 * DOWN)
        width = 11 / len(rows)
        bars = VGroup()
        for i, (_, r) in enumerate(rows.iterrows()):
            bar = Rectangle(width=width * 0.7, height=max(r["training_r2"] * 3.6, 0.01), stroke_width=0,
                            fill_color=ORANGE, fill_opacity=1).next_to(base, UP, 0)
            bar.set_x(-5.5 + width * (i + 0.5))
            count = label(str(int(r["noise_columns"])), 22, SUBDUED).next_to(base, DOWN, 0.2).set_x(bar.get_x())
            bars.add(VGroup(bar, count))
        name = label("training R² as noise columns are added", 28, SUBDUED).next_to(base, DOWN, 0.7)
        self.play(FadeIn(no, scale=1.4), run_time=self.share(0.15))
        self.play(FadeIn(base), FadeIn(name), run_time=self.share(0.05))
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in bars],
                              lag_ratio=0.3), run_time=self.share(0.55))
        self.finish()


# Key points (scenes 51–54) and the end card (scene 55) --------------------------------------------

KEY_POINTS = [
    "Training error measures memory, not prediction",
    "Error on new data is U-shaped in flexibility",
    "Much of the error is noise no model can remove",
    "Choose settings with cross-validation; open the test set once",
]


def key_points():
    head = title("Key points", 56).to_edge(UP, buff=0.8)
    rows = VGroup()
    for text in KEY_POINTS:
        box = RoundedRectangle(width=0.55, height=0.55, corner_radius=0.08, stroke_color=GREEN,
                               stroke_width=4)
        tick = VMobject(color=GREEN, stroke_width=8).set_points_as_corners(
            [[-0.16, 0.0, 0], [-0.04, -0.14, 0], [0.2, 0.16, 0]]).move_to(box)
        rows.add(VGroup(box, tick, label(text, 38).next_to(box, RIGHT, 0.4)))
    rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
    if rows.width > 12.4:
        rows.scale_to_fit_width(12.4)
    rows.next_to(head, DOWN, 0.8)
    return head, rows


class KeyPointScene(VideoScene):
    """Scene 51 shows point 1; each later scene adds the next."""

    def construct(self):
        index = self.number - 51
        head, rows = key_points()
        self.add(*rows[:index])
        if index == 0:
            self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.12))
        else:
            self.add(head)
        row = rows[index]
        self.play(FadeIn(row[0]), FadeIn(row[2], shift=0.3 * RIGHT), run_time=self.share(0.2))
        self.play(Create(row[1]), run_time=self.share(0.15))
        self.finish()


class Scene51(KeyPointScene):
    number = 51


class Scene52(KeyPointScene):
    number = 52


class Scene53(KeyPointScene):
    number = 53


class Scene54(KeyPointScene):
    number = 54


class Scene55(VideoScene):
    number = 55

    def construct(self):
        section = Path(self.script.meta["section"]).parent.as_posix()
        pages = label("Pages and code", 36, SUBDUED, weight=BOLD)
        address = label(f"hi-digital-ml-ai.github.io/ml-basic/{section}", 40, BLUE)
        thanks = title("Thanks for watching", 64)
        series = label(SERIES, 28, SUBDUED)
        VGroup(pages, address, thanks, series).arrange(DOWN, buff=0.5)
        thanks.shift(0.5 * DOWN)
        series.shift(0.5 * DOWN)
        self.play(FadeIn(pages), FadeIn(address, shift=0.2 * UP), run_time=self.share(0.2))
        self.wait(self.share(0.35))
        self.play(FadeIn(thanks, scale=0.9), FadeIn(series), run_time=self.share(0.2))
        self.finish()
