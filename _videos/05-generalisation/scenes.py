"""Manim scenes for the §5 video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/05-generalisation
    manim -ql scenes.py Scene08     # draft
    manim -qh scenes.py             # all, 1080p

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


# Signal and noise (scenes 8–9, schematic) ---------------------------------------

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

    signal_tag = label("signal", 34, BLUE, weight=BOLD).next_to(axes.c2p(0.3, signal(0.3)), UR, 0.3)
    noise_tag = label("noise", 34, ORANGE, weight=BOLD).next_to(axes.c2p(0.72, 1.0), UP, 0.1)
    return dict(axes=axes, names=names, dots=dots, trend=trend, residuals=residuals,
                wiggle=wiggle, signal_tag=signal_tag, noise_tag=noise_tag)


class Scene08(VideoScene):
    number = 8

    def construct(self):
        p = signal_and_noise()
        self.add(schematic_note())
        self.play(Create(p["axes"]), FadeIn(p["names"]), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in p["dots"]], lag_ratio=0.05),
                  run_time=self.share(0.15))
        self.wait(self.share(0.05))
        self.play(Create(p["trend"]), run_time=self.share(0.2))
        self.play(FadeIn(p["signal_tag"], shift=0.2 * UP), run_time=self.share(0.06))
        self.wait(self.share(0.08))
        self.play(LaggedStart(*[Create(r) for r in p["residuals"]], lag_ratio=0.04),
                  FadeIn(p["noise_tag"], shift=0.2 * UP), run_time=self.share(0.2))
        self.finish()


class Scene09(VideoScene):
    number = 9

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
                  FadeIn(gauge_label), FadeIn(track), FadeIn(bar), run_time=self.share(0.08))
        self.play(Create(p["wiggle"]), error.animate.set_value(0),
                  run_time=self.share(0.42), rate_func=linear)
        self.play(FadeIn(zero, scale=1.4), run_time=self.share(0.06))
        self.finish()


# Diagnosis (scene 15, schematic) --------------------------------------------------

def bar_pair(heading, training, new, gap_note=None):
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
    group = VGroup(base, bars, names, head)
    return group, bars


class Scene15(VideoScene):
    number = 15

    def construct(self):
        under, under_bars = bar_pair("both poor, about equal", 2.3, 2.5)
        over, over_bars = bar_pair("good, then much worse", 0.5, 2.9)
        VGroup(under, over).arrange(RIGHT, buff=2.6).shift(0.2 * DOWN)
        under_name = label("underfitting", 40, ORANGE, weight=BOLD).next_to(under, DOWN, 0.5)
        over_name = label("overfitting", 40, PURPLE, weight=BOLD).next_to(over, DOWN, 0.5)
        brace = Brace(VGroup(Line(over_bars[0].get_corner(UR), over_bars[0].get_corner(UR)),
                             Line(over_bars[1].get_corner(UL), over_bars[1].get_corner(UL))),
                      direction=RIGHT, color=INK)
        brace.next_to(over_bars[1], RIGHT, 0.2).stretch_to_fit_height(
            over_bars[1].get_top()[1] - over_bars[0].get_top()[1])
        brace.align_to(over_bars[1], UP)
        gap = label("the gap", 32, INK, weight=BOLD).next_to(brace, RIGHT, 0.15)

        self.add(schematic_note())
        self.wait(self.share(0.12))
        self.play(FadeIn(under[3]), FadeIn(under[0]), FadeIn(under[2]),
                  GrowFromEdge(under_bars[0], DOWN), GrowFromEdge(under_bars[1], DOWN),
                  run_time=self.share(0.1))
        self.play(FadeIn(under_name, shift=0.2 * UP), run_time=self.share(0.06))
        self.wait(self.share(0.12))
        self.play(FadeIn(over[3]), FadeIn(over[0]), FadeIn(over[2]),
                  GrowFromEdge(over_bars[0], DOWN), run_time=self.share(0.08))
        self.play(GrowFromEdge(over_bars[1], DOWN), run_time=self.share(0.08))
        self.play(FadeIn(over_name, shift=0.2 * UP), run_time=self.share(0.06))
        self.wait(self.share(0.1))
        self.play(GrowFromCenter(brace), FadeIn(gap), run_time=self.share(0.08))
        self.play(Indicate(gap, color=VERMILION, scale_factor=1.15), run_time=self.share(0.08))
        self.finish()


# Noise columns (scene 16, schematic; 17–18 are real data) ------------------------

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


class Scene16(VideoScene):
    number = 16

    def construct(self):
        full = survey_table(5).move_to(ORIGIN)
        real, noise = full[:3], full[3:]
        start = real.copy().move_to(ORIGIN)
        rule = Line(LEFT, RIGHT, color=GRID).set_width(full.width + 0.4)
        rule.next_to(full[0][0], DOWN, 0.16).set_x(0)

        self.add(schematic_note())
        self.wait(self.share(0.15))
        self.play(FadeIn(start), run_time=self.share(0.1))
        self.wait(self.share(0.15))
        self.play(ReplacementTransform(start, real), FadeIn(rule), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(c, shift=0.3 * LEFT) for c in noise], lag_ratio=0.35),
                  run_time=self.share(0.35))
        self.finish()


# Bias and variance (scenes 20–22, schematic) -------------------------------------

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


class Scene20(VideoScene):
    number = 20

    def construct(self):
        board = target()
        self.add(schematic_note())
        self.play(FadeIn(board, scale=0.9), run_time=self.share(0.1))
        self.wait(self.share(0.35))
        # "repeating the survey many times": a few faint sweeps round the rings
        self.play(Circumscribe(board[0], shape=Circle, color=BLUE, fade_out=True),
                  run_time=self.share(0.25))
        self.finish()


LEFT_BOARD, RIGHT_BOARD = 3.4 * LEFT + 0.3 * DOWN, 3.4 * RIGHT + 0.3 * DOWN


def bias_board():
    board = target(LEFT_BOARD)
    shots = hits(LEFT_BOARD, [0.95, 0.75], 0.14, 21, ORANGE)
    name = label("bias", 44, ORANGE, weight=BOLD).next_to(board, UP, 0.35)
    return board, shots, name


class Scene21(VideoScene):
    number = 21

    def construct(self):
        board, shots, name = bias_board()
        self.add(schematic_note(), target())
        self.play(ReplacementTransform(self.mobjects[-1], board), run_time=self.share(0.08))
        self.play(FadeIn(name), LaggedStart(*[FadeIn(s, scale=2) for s in shots], lag_ratio=0.2),
                  run_time=self.share(0.3))
        self.wait(self.share(0.25))
        arrow = Arrow(board[1].get_center(), shots.get_center(), buff=0.12,
                      color=INK, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(arrow), run_time=self.share(0.1))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        board, shots, name = bias_board()
        self.add(schematic_note(), board, shots, name)
        right = target(RIGHT_BOARD)
        scatter = hits(RIGHT_BOARD, [0, 0], 0.72, 22, SKY)
        right_name = label("variance", 44, BLUE, weight=BOLD).next_to(right, UP, 0.35)
        self.play(FadeIn(right), FadeIn(right_name), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(s, scale=2) for s in scatter], lag_ratio=0.2),
                  run_time=self.share(0.35))
        self.wait(self.share(0.15))
        self.play(Indicate(scatter, color=BLUE, scale_factor=1.08), run_time=self.share(0.12))
        self.finish()


# Ridge shrinking the coefficients (scene 26, schematic) --------------------------

class Scene26(VideoScene):
    number = 26

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
        caption = label("coefficients", 30, SUBDUED).next_to(baseline, LEFT, 0.3).shift(2.6 * UP + 1.2 * RIGHT)

        slider = Line(3 * LEFT, 3 * RIGHT, color=GRID, stroke_width=6).to_edge(DOWN, buff=0.9)
        knob = always_redraw(lambda: Dot(slider.point_from_proportion(penalty.get_value()),
                                         radius=0.16, color=INK))
        slider_name = label("penalty  λ", 32, INK).next_to(slider, LEFT, 0.4)

        self.add(schematic_note())
        self.play(FadeIn(baseline), FadeIn(coefficients), FadeIn(caption), run_time=self.share(0.12))
        self.play(FadeIn(slider), FadeIn(knob), FadeIn(slider_name), run_time=self.share(0.1))
        self.wait(self.share(0.18))
        self.play(penalty.animate.set_value(1), run_time=self.share(0.45), rate_func=smooth)
        self.finish()


# Peeking at the test set (scenes 29–30, schematic) -------------------------------

def test_box():
    body = RoundedRectangle(width=3.6, height=2.3, corner_radius=0.15,
                            stroke_color=INK, stroke_width=4, fill_color="#F2F5F7", fill_opacity=1)
    lid = RoundedRectangle(width=3.9, height=0.45, corner_radius=0.1,
                           stroke_color=INK, stroke_width=4, fill_color="#E3E9ED", fill_opacity=1)
    lid.next_to(body, UP, 0)
    name = label("test set", 40, weight=BOLD).move_to(body)
    return body, lid, name


def peek(scene, lid, marks, i, run_time):
    """Lift the lid, add one mark to the tally of looks, close it again."""
    hinge = lid.get_corner(DL)
    scene.play(Rotate(lid, angle=0.55, about_point=hinge), FadeIn(marks[i], scale=1.6),
               run_time=run_time / 2)
    scene.play(Rotate(lid, angle=-0.55, about_point=hinge), run_time=run_time / 2)


def peek_marks():
    return VGroup(*[Circle(radius=0.16, color=VERMILION, fill_opacity=1, stroke_width=0)
                    for _ in range(5)]).arrange(RIGHT, buff=0.3)


class Scene29(VideoScene):
    number = 29

    def construct(self):
        body, lid, name = test_box()
        box = VGroup(body, lid, name).shift(0.4 * UP)
        marks = peek_marks().next_to(box, DOWN, 0.8)
        looks = label("looks at the test set", 28, SUBDUED).next_to(marks, DOWN, 0.25)
        self.add(schematic_note())
        self.play(FadeIn(box), run_time=self.share(0.08))
        self.wait(self.share(0.12))
        self.play(FadeIn(looks), run_time=self.share(0.05))
        for i in range(5):
            peek(self, lid, marks, i, self.share(0.1))
        self.finish()


class Scene30(VideoScene):
    number = 30

    def construct(self):
        body, lid, name = test_box()
        box = VGroup(body, lid, name).shift(0.4 * UP)
        marks = peek_marks().next_to(box, DOWN, 0.8)
        looks = label("looks at the test set", 28, SUBDUED).next_to(marks, DOWN, 0.25)
        self.add(schematic_note(), box, marks, looks)
        again = label("training set, again", 30, VERMILION, weight=BOLD).move_to(body)
        self.wait(self.share(0.35))
        self.play(body.animate.set_stroke(VERMILION), lid.animate.set_stroke(VERMILION),
                  run_time=self.share(0.08))
        self.play(ReplacementTransform(name, again), run_time=self.share(0.12))
        self.finish()


# Cross-validation (scene 31, schematic) ------------------------------------------

class Scene31(VideoScene):
    number = 31

    def construct(self):
        folds = VGroup(*[Rectangle(width=0.95, height=0.8, stroke_color=BACKGROUND,
                                   stroke_width=4, fill_color=BLUE, fill_opacity=1)
                         for _ in range(10)]).arrange(RIGHT, buff=0)
        training = label("training data", 30, SUBDUED).next_to(folds, UP, 0.3)
        body, lid, name = test_box()
        box = VGroup(body, lid, name).scale(0.6)
        VGroup(VGroup(training, folds), box).arrange(RIGHT, buff=0.9).shift(0.3 * UP)
        legend = VGroup(
            VGroup(Square(0.3, fill_color=BLUE, fill_opacity=1, stroke_width=0),
                   label("fit on these", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.3, fill_color=ORANGE, fill_opacity=1, stroke_width=0),
                   label("scored on this", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6).next_to(folds, DOWN, 0.6)
        seal = label("sealed", 26, VERMILION, weight=BOLD).next_to(box, DOWN, 0.2)

        self.add(schematic_note())
        self.play(FadeIn(training), FadeIn(folds), FadeIn(box), FadeIn(seal),
                  run_time=self.share(0.08))
        # "Split the training data into ten folds"
        self.play(folds.animate.arrange(RIGHT, buff=0.1).move_to(folds), run_time=self.share(0.08))
        self.play(FadeIn(legend), run_time=self.share(0.05))
        # "Fit on nine, score on the tenth, and rotate"
        step = self.share(0.055)
        for i in range(10):
            self.play(folds[i].animate.set_fill(ORANGE),
                      *[folds[j].animate.set_fill(BLUE) for j in range(10) if j != i],
                      run_time=step)
        self.play(*[f.animate.set_fill(BLUE) for f in folds], run_time=self.share(0.04))
        # "The test set is used once, at the very end"
        hinge = lid.get_corner(DL)
        self.play(Rotate(lid, angle=0.6, about_point=hinge), FadeOut(seal),
                  run_time=self.share(0.07))
        once = label("once", 30, GREEN, weight=BOLD).next_to(box, DOWN, 0.2)
        self.play(FadeIn(once, scale=1.3), run_time=self.share(0.05))
        self.finish()


# Repeat visits (scene 33, schematic apart from the 160 sites) ---------------------

class Scene33(VideoScene):
    number = 33

    def construct(self):
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

        self.add(schematic_note())
        self.play(FadeIn(heading), run_time=self.share(0.06))
        self.play(LaggedStart(*[FadeIn(s) for s in sites], lag_ratio=0.01),
                  run_time=self.share(0.2))
        self.play(FadeIn(legend), run_time=self.share(0.05))
        self.wait(self.share(0.08))
        # "a random split puts the same site on both sides"
        self.play(*[Circumscribe(s, color=VERMILION, buff=0.04, stroke_width=3)
                    for s in both[:24]], run_time=self.share(0.18))
        self.finish()


# ---------------------------------------------------------------------------------
# Real-data scenes. Every number drawn or printed comes from visuals/data/*.csv.
# ---------------------------------------------------------------------------------

# The colours ggplot gives the five models on the page (levels in alphabetical
# order), so the video and fig-crossing agree.
MODEL_COLOURS = {
    "Boosted trees": BLUE, "Linear regression": ORANGE, "Random forest": GREEN,
    "Tree, depth 3": VERMILION, "Tree, grown out": PURPLE,
}


def rmse_text(value, digits=2, size=30, color=INK):
    """An RMSE as printed: an exact zero is written 0, not 0.00."""
    return label("0" if value == 0 else f"{value:.{digits}f}", size, color)


# Five models, training error only (scenes 1–2) ------------------------------------

def five_models_table(models):
    heading = label("Error on the training stations (RMSE)", 34, SUBDUED)
    hidden = label("on new stations", 34, GRID)
    scale = 5.2 / models["training"].max()
    rows = VGroup()
    for _, m in models.iterrows():
        name = label(m["model"], 32).set_width(label(m["model"], 32).width)
        bar = Rectangle(width=max(m["training"] * scale, 0.02), height=0.42, stroke_width=0,
                        fill_color=MODEL_COLOURS[m["model"]], fill_opacity=1)
        value = rmse_text(m["training"])
        blank = RoundedRectangle(width=1.2, height=0.5, corner_radius=0.08,
                                 stroke_color=GRID, stroke_width=2)
        rows.add(VGroup(name, bar, value, blank))
    # columns: names right-aligned, bars from a common origin
    for i, (name, bar, value, blank) in enumerate(rows):
        y = 1.6 - 0.95 * i
        name.move_to([-3.6, y, 0], aligned_edge=RIGHT)
        bar.move_to([-3.3, y, 0], aligned_edge=LEFT)
        value.next_to(bar, RIGHT, 0.2)
        blank.move_to([5.4, y, 0])
    heading.move_to([-0.7, 2.7, 0])
    hidden.move_to([5.4, 2.7, 0])
    return heading, hidden, rows


class Scene01(VideoScene):
    number = 1

    def construct(self):
        models = self.data("five-models")
        heading, hidden, rows = five_models_table(models)
        self.play(FadeIn(heading), FadeIn(hidden), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.15),
                  *[FadeIn(r[3]) for r in rows], run_time=self.share(0.15))
        # "This is the error each one makes on the stations it was trained on."
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                for r in rows], lag_ratio=0.2), run_time=self.share(0.35))
        # "And one of them is perfect: an error of exactly zero."
        perfect = next(r for r, (_, m) in zip(rows, models.iterrows()) if m["training"] == 0)
        self.wait(self.share(0.15))
        self.play(perfect[2].animate.scale(1.6).set_color(PURPLE), run_time=self.share(0.08))
        self.finish()


class Scene02(VideoScene):
    number = 2

    def construct(self):
        models = self.data("five-models")
        heading, hidden, rows = five_models_table(models)
        perfect = next(r for r, (_, m) in zip(rows, models.iterrows()) if m["training"] == 0)
        perfect[2].scale(1.6).set_color(PURPLE)
        self.add(heading, hidden, rows)
        mark = label("?", 44, PURPLE, weight=BOLD).move_to(perfect[3])
        self.play(Indicate(VGroup(perfect[0], perfect[2]), color=PURPLE, scale_factor=1.15),
                  run_time=self.share(0.3))
        self.play(FadeIn(mark, scale=0.5), run_time=self.share(0.15))
        self.finish()


# The ranking reverses (scenes 5–7) ---------------------------------------------------

def slope_axes(models):
    top = float(np.ceil(models["test"].max()))
    axes = Axes(x_range=[0, 1, 1], y_range=[0, top, 1], x_length=6, y_length=5.6,
                tips=False, axis_config={"color": GRID, "include_ticks": False},
                y_axis_config={"include_numbers": False}).shift(1.4 * LEFT + 0.1 * DOWN)
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


class Scene05(VideoScene):
    number = 5

    def construct(self):
        models = self.data("five-models")
        axes, frame, lines, left_dots, right_dots, names = slope_axes(models)
        self.play(FadeIn(frame), LaggedStart(*[FadeIn(d, scale=1.5) for d in left_dots]),
                  run_time=self.share(0.15))
        # "Now let's give the five models stations they have never seen."
        self.wait(self.share(0.1))
        order = np.argsort(models["training"].to_numpy())   # from the best-trained up
        self.play(LaggedStart(*[AnimationGroup(Create(lines[i]), FadeIn(right_dots[i]),
                                               FadeIn(names[i]))
                                for i in order], lag_ratio=0.45),
                  run_time=self.share(0.55))
        self.finish()


def ranking_lists(models):
    """The five models ranked by training error and by test error, 1 = best."""
    by_train = list(models.sort_values("training")["model"])
    by_test = list(models.sort_values("test")["model"])

    def column(heading, names):
        items = VGroup(*[
            VGroup(label(f"{i}", 30, SUBDUED), label(n, 30, MODEL_COLOURS[n])).arrange(RIGHT, buff=0.3)
            for i, n in enumerate(names, 1)])
        items.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        return VGroup(label(heading, 30, weight=BOLD), items).arrange(DOWN, buff=0.5)

    left = column("ranked by training error", by_train).move_to(3.6 * LEFT)
    right = column("ranked on new stations", by_test).move_to(3.6 * RIGHT)
    arrows = VGroup()
    for i, n in enumerate(by_train):
        j = by_test.index(n)
        arrows.add(Arrow(left[1][i].get_right(), right[1][j][0].get_left(),
                         buff=0.25, color=MODEL_COLOURS[n], stroke_width=4,
                         max_tip_length_to_length_ratio=0.05))
    return left, right, arrows


class Scene06(VideoScene):
    number = 6

    def construct(self):
        left, right, arrows = ranking_lists(self.data("five-models"))
        self.play(FadeIn(left), run_time=self.share(0.12))
        self.play(FadeIn(right), run_time=self.share(0.12))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25),
                  run_time=self.share(0.3))
        # "The model you would have picked is the worst of the five."
        self.play(Circumscribe(left[1][0], color=PURPLE), Circumscribe(right[1][-1], color=PURPLE),
                  run_time=self.share(0.2))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        models = self.data("five-models")
        axes, frame, lines, left_dots, right_dots, names = slope_axes(models)
        self.add(frame, lines, left_dots, right_dots, names)
        tree = models.index[models["model"] == "Tree, grown out"][0]
        others = [i for i in range(len(models)) if i != tree]
        baseline = models["baseline"].iloc[0]

        tree_value = label(f"{models['test'].iloc[tree]:.1f}", 34, PURPLE, weight=BOLD)
        tree_value.next_to(right_dots[tree], LEFT, 0.25)
        self.play(*[m.animate.set_opacity(0.15) for i in others
                    for m in (lines[i], left_dots[i], right_dots[i], names[i])],
                  run_time=self.share(0.08))
        self.play(FadeIn(tree_value), Indicate(right_dots[tree], color=PURPLE),
                  run_time=self.share(0.12))
        # "Ignoring every predictor and just guessing the average scores 5.3."
        self.wait(self.share(0.08))
        mean_line = DashedLine(axes.c2p(0, baseline), axes.c2p(1.25, baseline), color=GREY,
                               stroke_width=4)
        mean_name = label(f"predict the mean: {baseline:.1f}", 28, GREY).next_to(
            axes.c2p(0, baseline), UR, 0.15)
        self.play(Create(mean_line), FadeIn(mean_name), run_time=self.share(0.15))
        # "It has not learned a relationship. It has memorised the survey."
        self.finish()


# The U-shaped curve (scenes 12–14) ---------------------------------------------------

def u_curve_axes(curve):
    lo, hi = np.log10(5), np.log10(500)
    axes = Axes(x_range=[lo, hi, 1], y_range=[0, 6, 1], x_length=10, y_length=5.2,
                tips=False, axis_config={"color": GRID, "include_ticks": False}).shift(0.3 * DOWN + 0.3 * RIGHT)
    xt = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(np.log10(v), 0), DOWN, 0.2)
                  for v in (10, 30, 100, 300)])
    yt = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(lo, v), LEFT, 0.2)
                  for v in range(0, 7)])
    xl = label("leaves in the tree (log scale)", 28, SUBDUED).next_to(xt, DOWN, 0.25)
    yl = label("RMSE (individuals)", 28, SUBDUED).rotate(PI / 2).next_to(yt, LEFT, 0.25)

    def trace(column, colour):
        points = [axes.c2p(np.log10(l), v) for l, v in zip(curve["leaves"], curve[column])]
        line = VMobject(color=colour, stroke_width=6).set_points_as_corners(points)
        dots = VGroup(*[Dot(p, radius=0.07, color=colour) for p in points])
        return line, dots

    training = trace("training", BLUE)
    test = trace("test", ORANGE)
    names = VGroup(label("training", 30, BLUE, weight=BOLD).next_to(training[1][-1], LEFT, 0.3),
                   label("new stations", 30, ORANGE, weight=BOLD).next_to(test[1][-1], UP, 0.2))
    return axes, VGroup(axes, xt, yt, xl, yl), training, test, names


class Scene12(VideoScene):
    number = 12

    def construct(self):
        axes, frame, training, test, names = u_curve_axes(self.data("u-curve"))
        self.play(FadeIn(frame), run_time=self.share(0.12))
        self.play(Create(training[0]), LaggedStart(*[FadeIn(d) for d in training[1]]),
                  run_time=self.share(0.55), rate_func=linear)
        self.play(FadeIn(names[0]), run_time=self.share(0.08))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        curve = self.data("u-curve")
        axes, frame, training, test, names = u_curve_axes(curve)
        self.add(frame, *training, names[0])
        self.play(Create(test[0]), LaggedStart(*[FadeIn(d) for d in test[1]]),
                  FadeIn(names[1]), run_time=self.share(0.4), rate_func=linear)
        best = int(curve["best_leaves"].iloc[0])
        x = np.log10(best)
        dotted = DashedLine(axes.c2p(x, 0), axes.c2p(x, 6), dash_length=0.06,
                            color=INK, stroke_width=3)
        tag = label(f"best: {best} leaves", 28, INK).next_to(axes.c2p(x, 5.8), RIGHT, 0.2)
        self.play(Create(dotted), FadeIn(tag), run_time=self.share(0.12))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        curve = self.data("u-curve")
        axes, frame, training, test, names = u_curve_axes(curve)
        self.add(frame, *training, *test, names)
        baseline = curve["baseline"].iloc[0]
        lo, hi = np.log10(5), np.log10(500)
        mean_line = DashedLine(axes.c2p(lo, baseline), axes.c2p(hi, baseline), color=GREY,
                               stroke_width=4)
        mean_name = label("predict the mean", 26, GREY).next_to(axes.c2p(lo, baseline), UR, 0.1)
        # The crossing lies between the last sweep point below the baseline and the
        # first above it (62 and 85 leaves on the page).
        above = curve[(curve["test"] > baseline) & (curve["leaves"] > curve["best_leaves"])]
        first = above.index[0]
        a, b = curve["leaves"].iloc[first - 1], curve["leaves"].iloc[first]
        band = Rectangle(width=axes.c2p(np.log10(b), 0)[0] - axes.c2p(np.log10(a), 0)[0],
                         height=5.2, stroke_width=0, fill_color=VERMILION, fill_opacity=0.15)
        band.move_to(axes.c2p((np.log10(a) + np.log10(b)) / 2, 3))
        band_tag = label(f"{a}–{b} leaves", 26, VERMILION).next_to(band, UP, 0.1)

        self.play(Create(mean_line), FadeIn(mean_name), run_time=self.share(0.15))
        self.play(FadeIn(band), FadeIn(band_tag), run_time=self.share(0.12))
        # "And training error gives no warning: it keeps falling straight through."
        self.wait(self.share(0.25))
        self.play(ShowPassingFlash(training[0].copy().set_stroke(width=12, color=SKY),
                                   time_width=0.4), run_time=self.share(0.25))
        self.finish()


# Noise columns: training R² and test RMSE (scenes 17–18) -----------------------------

def stepped_gauge(heading, width=9.0):
    head = label(heading, 34, weight=BOLD)
    track = Rectangle(width=width, height=0.55, stroke_color=GRID, stroke_width=2)
    VGroup(head, track).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    return head, track


class Scene17(VideoScene):
    number = 17

    def construct(self):
        rows = self.data("noise-columns")
        stations = int(rows["stations"].iloc[0])
        head, track = stepped_gauge("training R²")
        VGroup(head, track).move_to(0.6 * UP)
        counter_name = label("noise columns added", 30, SUBDUED)
        counter_name.next_to(track, DOWN, 0.9, aligned_edge=LEFT)
        station_note = label(f"{stations} training stations", 30, SUBDUED)
        station_note.next_to(counter_name, DOWN, 0.3, aligned_edge=LEFT)

        def bar(r2):
            return Rectangle(width=max(track.width * r2, 0.01), height=track.height,
                             stroke_width=0, fill_color=ORANGE, fill_opacity=1
                             ).align_to(track, LEFT).align_to(track, DOWN)

        def readouts(row):
            value = label(f"{row['training_r2']:.3f}", 40, ORANGE, weight=BOLD).next_to(track, RIGHT, 0.3)
            count = label(str(int(row["noise_columns"])), 30, INK, weight=BOLD).next_to(counter_name, RIGHT, 0.3)
            return value, count

        first = rows.iloc[0]
        fill = bar(first["training_r2"])
        value, count = readouts(first)
        self.play(FadeIn(head), FadeIn(track), FadeIn(fill), FadeIn(value),
                  FadeIn(counter_name), FadeIn(count), FadeIn(station_note),
                  run_time=self.share(0.1))
        # Step through the page's own rows only: no value between them is shown.
        step = self.share(0.55) / (len(rows) - 1)
        for _, row in rows.iloc[1:].iterrows():
            new_value, new_count = readouts(row)
            self.play(Transform(fill, bar(row["training_r2"])),
                      Transform(value, new_value), Transform(count, new_count), run_time=step)
        self.play(Indicate(value, color=ORANGE, scale_factor=1.2), run_time=self.share(0.1))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        rows = self.data("noise-columns")
        last = rows.iloc[-1]
        largest = int(last["largest_catch"])
        width = 11.0
        scale = width / last["test_rmse"]

        head = label("error on new stations (RMSE)", 34, weight=BOLD).to_edge(UP, buff=1.2).to_edge(LEFT, buff=1.2)
        catch = Rectangle(width=largest * scale, height=0.55, stroke_width=0,
                          fill_color=GREY, fill_opacity=1).next_to(head, DOWN, 0.6, aligned_edge=LEFT)
        catch_tag = label(f"largest catch in the survey: {largest}", 28, GREY).next_to(catch, RIGHT, 0.25)
        error = Rectangle(width=rows["test_rmse"].iloc[0] * scale, height=0.55, stroke_width=0,
                          fill_color=VERMILION, fill_opacity=1).next_to(catch, DOWN, 0.9, aligned_edge=LEFT)
        count_tag = label(f"with {int(last['noise_columns'])} noise columns", 28, SUBDUED).next_to(
            error, DOWN, 0.3, aligned_edge=LEFT)
        value = label(f"{last['test_rmse']:.0f}", 60, VERMILION, weight=BOLD)

        self.play(FadeIn(head), FadeIn(catch), FadeIn(catch_tag), FadeIn(error),
                  run_time=self.share(0.1))
        self.play(error.animate.stretch_to_fit_width(width, about_edge=LEFT),
                  run_time=self.share(0.2), rate_func=rush_into)
        value.next_to(error, DOWN, 0.3).align_to(error, RIGHT)
        self.play(FadeIn(value, scale=1.5), FadeIn(count_tag), run_time=self.share(0.1))
        self.finish()


# Least squares, the mean and ridge (scene 27) ----------------------------------------

class Scene27(VideoScene):
    number = 27

    def construct(self):
        rows = self.data("ridge-bars")
        colours = {"Least squares": VERMILION, "Predict the mean": GREY, "Ridge": BLUE}
        base = Line(5 * LEFT, 5 * RIGHT, color=GRID, stroke_width=3).shift(2.3 * DOWN)
        scale = 4.2 / rows["rmse"].max()
        bars = VGroup()
        for i, (_, r) in enumerate(rows.iterrows()):
            bar = Rectangle(width=2.0, height=r["rmse"] * scale, stroke_width=0,
                            fill_color=colours[r["method"]], fill_opacity=1)
            bar.next_to(base, UP, 0).set_x((i - 1) * 3.2)
            value = label(f"{r['rmse']:.2f}", 36, colours[r["method"]], weight=BOLD).next_to(bar, UP, 0.2)
            name = label(r["method"], 28, SUBDUED).next_to(base, DOWN, 0.3).set_x(bar.get_x())
            bars.add(VGroup(bar, value, name))
        head = label(f"{int(rows['predictors'].iloc[0])} predictors, "
                     f"{int(rows['stations'].iloc[0])} training stations: error on new stations",
                     30, SUBDUED).to_edge(UP, buff=0.6)

        self.play(FadeIn(head), FadeIn(base), run_time=self.share(0.1))
        for group, share in zip(bars, (0.2, 0.2, 0.2)):
            self.play(GrowFromEdge(group[0], DOWN), FadeIn(group[1]), FadeIn(group[2]),
                      run_time=self.share(share * 0.6))
            self.wait(self.share(share * 0.4))
        self.finish()
