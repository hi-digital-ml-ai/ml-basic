"""Manim scenes for the unsupervised-learning video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/08-unsupervised-learning
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


PROMISES = ["Why every method always finds something",
            "Why a principal component is not a gradient",
            "How to tell a group from a gradient"]
ANSWERS = ["Compare what it found\nwith the same data,\nshuffled",
           "Check what it lines\nup with; let the task\nchoose how many",
           "Check against what\nit never saw; a slope\nis not a set of groups"]
RECAP = ["Every method finds something",
         "A component is not a gradient",
         "Stable is not the same as real"]


class Scene01(LearnScene):
    number = 1


def percent(x, digits=0):
    return f"{100 * x:.{digits}f}%"


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def polyline(axes, xs, ys, colour, width=6, dashed=False):
    points = [axes.c2p(x, y) for x, y in zip(xs, ys)]
    line = VMobject(color=colour, stroke_width=width).set_points_as_corners(points)
    return DashedVMobject(line, num_dashes=60) if dashed else line


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name,
          x_fmt="{:g}", y_fmt="{:g}", size=24):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
    axes = plain_axes(x_range, y_range, x_length, y_length)
    tx = VGroup(*[label(x_fmt.format(v), size, SUBDUED).next_to(axes.c2p(v, y_range[0]), DOWN, 0.15)
                  for v in x_ticks])
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


# Viridis, as the pages shade depth: dark purple for shallow, yellow for deep.
VIRIDIS = ["#440154", "#3B528B", "#21908C", "#5DC863", "#FDE725"]


def viridis(t):
    t = min(max(t, 0.0), 1.0) * (len(VIRIDIS) - 1)
    i = min(int(t), len(VIRIDIS) - 2)
    return interpolate_color(ManimColor(VIRIDIS[i]), ManimColor(VIRIDIS[i + 1]), t - i)


def depth_key(width=2.6, lo="shallow", hi="deep"):
    """A colour bar for depth, from 40 thin slices."""
    n = 40
    bar = VGroup(*[Rectangle(width=width / n, height=0.22, stroke_width=0, fill_color=viridis(i / (n - 1)),
                             fill_opacity=1) for i in range(n)]).arrange(RIGHT, buff=0)
    return VGroup(label(lo, 24, SUBDUED), bar, label(hi, 24, SUBDUED)).arrange(RIGHT, buff=0.15)


def marker(point, colour, hard, size=0.075):
    """A station: a dot for hard seabed, a small triangle for soft, as on the pages."""
    if hard:
        return Dot(point, radius=size, color=colour, fill_opacity=0.9)
    return Triangle(stroke_width=0, fill_color=colour, fill_opacity=0.9).scale(size * 1.5).move_to(point)


def strike(mobject, colour=VERMILION):
    return Line(mobject.get_left() + 0.1 * LEFT, mobject.get_right() + 0.1 * RIGHT, color=colour,
                stroke_width=6)


# The puzzle: a split of the soft bottom that always comes back (scenes 2–5, page results) --

class Scene02(VideoScene):
    number = 2

    def construct(self):
        rng = np.random.default_rng(2)
        rows, cols = 16, 24
        cells = VGroup(*[Square(0.2, stroke_width=0, fill_color=BLUE,
                                fill_opacity=float(rng.choice([0.08, 0.3, 0.6, 0.9], p=[0.5, 0.2, 0.2, 0.1])))
                         for _ in range(rows * cols)])
        cells.arrange_in_grid(rows, cols, buff=0.04).move_to([-0.8, -0.3, 0])
        taxa = label("24 kinds of animal: counts", 30, BLUE, weight=BOLD).next_to(cells, UP, 0.3)
        brace = Brace(cells, LEFT, color=SUBDUED)
        stations = label("800 stations", 30, SUBDUED, weight=BOLD).next_to(brace, LEFT, 0.2)
        missing = DashedVMobject(Rectangle(width=0.9, height=cells.height, color=GREY, stroke_width=3),
                                 num_dashes=40).next_to(cells, RIGHT, 0.4)
        missing_name = VGroup(label("labels", 30, VERMILION, weight=BOLD), label("none", 30, VERMILION)
                              ).arrange(DOWN, buff=0.1).next_to(missing, RIGHT, 0.3)
        # "Here is a survey of 800 seabed stations, ..."
        self.play(FadeIn(cells, lag_ratio=0.002), GrowFromCenter(brace), FadeIn(stations),
                  run_time=self.share(0.35))
        # "... with counts of 24 kinds of animal, ..."
        self.play(FadeIn(taxa, shift=0.2 * DOWN), run_time=self.share(0.2))
        # "... and no labels at all."
        self.wait(max(self.share(0.65) - self.time, 0.01))
        self.play(Create(missing), FadeIn(missing_name), run_time=self.share(0.2))
        self.finish()


def soft_layout(scene):
    stations = scene.data("soft-stations")
    medians = scene.data("soft-medians").set_index("cluster")
    deep = medians["median_depth"].idxmax()
    axis, to_x = number_line(0, 200, -5.6, 5.6, 0.3, [0, 50, 100, 150, 200], 0)
    axis_name = label("depth (m)", 26, SUBDUED).next_to(axis, DOWN, 0.05).shift(4.6 * RIGHT)
    rng = np.random.default_rng(3)
    colours = {c: (BLUE if c == deep else ORANGE) for c in medians.index}
    dots = VGroup(*[Dot([to_x(d), 1.55 + rng.uniform(-0.8, 0.8), 0], radius=0.05,
                        color=colours[c], fill_opacity=0.8)
                    for d, c in zip(stations["depth_m"], stations["cluster"])])
    head = label(f"The {len(stations)} soft-bottom stations, asked for two groups", 32, SUBDUED
                 ).to_edge(UP, buff=0.3)
    notes = VGroup()
    for c, m in medians["median_depth"].items():
        tag = "deep" if c == deep else "shallow"
        mark = Line([to_x(m), 0.6, 0], [to_x(m), 2.5, 0], color=colours[c], stroke_width=5)
        text = label(f"{tag}: median {m:.0f} m", 30, colours[c], weight=BOLD).next_to(mark, UP, 0.1)
        # The two medians are close: set each label off to its own side of its line.
        text.align_to(mark, LEFT if c == deep else RIGHT)
        notes.add(VGroup(mark, text))
    return head, VGroup(axis, axis_name), dots, notes


def stability_axis(y=-2.6):
    axis, to_x = number_line(0, 1, -4.8, 5.6, y, [0, 0.25, 0.5, 0.75, 1], 2)
    name = label("agreement with the original split (1 = identical)", 26, SUBDUED
                 ).next_to(axis, DOWN, 0.05).set_x(0.4)
    return VGroup(axis, name), to_x


class Scene03(VideoScene):
    number = 3

    def construct(self):
        head, axis, dots, notes = soft_layout(self)
        # "Take the soft-bottom stations, and ask for two groups."
        self.play(FadeIn(head), FadeIn(axis), run_time=self.share(0.15))
        self.play(FadeIn(dots, lag_ratio=0.002), run_time=self.share(0.3))
        # "You get a shallow group, at a median depth of 60 metres, and a deep one at 124."
        shallow, deep = sorted(notes, key=lambda n: n[0].get_x())
        self.play(Create(shallow[0]), FadeIn(shallow[1]), run_time=self.share(0.2))
        self.wait(max(self.share(0.75) - self.time, 0.01))
        self.play(Create(deep[0]), FadeIn(deep[1]), run_time=self.share(0.15))
        self.finish()


def soft_stability_dots(scene, to_x, y):
    values = scene.data("soft-stability")["agreement"].to_numpy()
    rng = np.random.default_rng(4)
    dots = VGroup(*[Dot([to_x(v), y + rng.uniform(-0.3, 0.3), 0], radius=0.08, color=BLUE, fill_opacity=0.8)
                    for v in values])
    return values, dots


class Scene04(VideoScene):
    number = 4

    def construct(self):
        head, axis, dots, notes = soft_layout(self)
        self.add(head, axis, dots, notes)
        stab, to_x = stability_axis()
        values, drops = soft_stability_dots(self, to_x, -1.7)
        # "Resample the stations sixty times. The same split comes back every time: ..."
        self.play(FadeIn(stab), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(d, shift=0.6 * DOWN) for d in drops], lag_ratio=0.05),
                  run_time=self.share(0.4))
        # "... an agreement of 0.89 on average, and never below 0.71."
        span = Line([to_x(values.min()), -1.1, 0], [to_x(1), -1.1, 0], color=BLUE, stroke_width=4)
        text = label(f"average {values.mean():.2f}, never below {values.min():.2f}", 30, BLUE, weight=BOLD
                     ).next_to(span, LEFT, 0.3)
        self.play(Create(span), FadeIn(text), run_time=self.share(0.25))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        head, axis, dots, notes = soft_layout(self)
        stab, to_x = stability_axis()
        values, drops = soft_stability_dots(self, to_x, -1.7)
        span = Line([to_x(values.min()), -1.1, 0], [to_x(1), -1.1, 0], color=BLUE, stroke_width=4)
        text = label(f"average {values.mean():.2f}, never below {values.min():.2f}", 30, BLUE, weight=BOLD
                     ).next_to(span, LEFT, 0.3)
        self.add(head, axis, dots, notes, stab, drops, span, text)
        question = label("two kinds of soft seabed community?", 40, PURPLE, weight=BOLD)
        box = SurroundingRectangle(question, color=PURPLE, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                                   fill_opacity=0.95)
        card = VGroup(box, question).move_to([0, 1.55, 0])
        # "So are there two kinds of soft seabed community?"
        self.play(FadeIn(card, scale=0.9), run_time=self.share(0.4))
        self.play(Wiggle(question), run_time=self.share(0.45))
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


# Groups from counts alone (scenes 7–12) ----------------------------------------------------

class Scene07(VideoScene):
    number = 7

    def construct(self):
        # Schematic: two made-up blobs, and k-means run on them step by step.
        rng = np.random.default_rng(7)
        points = np.vstack([rng.normal([-2.2, 0.6], 0.9, (40, 2)), rng.normal([2.4, -0.8], 0.9, (40, 2))])
        points[:, 1] -= 0.3
        dots = VGroup(*[Dot([x, y, 0], radius=0.09, color=GREY) for x, y in points])
        centres = np.array([[-0.6, 2.2], [0.8, 1.6]])
        colours = [ORANGE, BLUE]
        stars = VGroup(*[Star(5, outer_radius=0.28, color=c, fill_opacity=1, stroke_width=0).move_to([*p, 0])
                         for c, p in zip(colours, centres)])
        head = label("k-means, asked for two groups", 34, SUBDUED).to_edge(UP, buff=0.3)
        # "k-means places as many centres as you ask for, ..."
        self.play(FadeIn(head), FadeIn(dots, lag_ratio=0.02), run_time=self.share(0.2))
        self.play(FadeIn(stars, scale=2), run_time=self.share(0.1))
        # "... and moves each to the middle of the stations nearest it, until nothing moves."
        steps = 4
        for _ in range(steps):
            nearest = np.argmin(((points[:, None, :] - centres[None]) ** 2).sum(-1), axis=1)
            self.play(*[d.animate.set_color(colours[n]) for d, n in zip(dots, nearest)],
                      run_time=self.share(0.55 / (2 * steps)))
            centres = np.array([points[nearest == j].mean(0) for j in range(2)])
            self.play(*[s.animate.move_to([*p, 0]) for s, p in zip(stars, centres)],
                      run_time=self.share(0.55 / (2 * steps)))
        self.finish()


VARIABLE_NAMES = {"depth_m": "depth (m)", "temperature_c": "temperature (°C)",
                  "salinity_psu": "salinity", "chlorophyll_mg_m3": "chlorophyll"}


class Scene08(VideoScene):
    number = 8

    def construct(self):
        share = self.data("env-share").sort_values("share", ascending=False).reset_index(drop=True)
        head = label("Share of the variance, in measured units", 34, SUBDUED).to_edge(UP, buff=0.6)
        rows = VGroup()
        for i, r in share.iterrows():
            y = 1.6 - 1.2 * i
            name = label(VARIABLE_NAMES[r["variable"]], 32).move_to([-2.4, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=max(7.0 * r["share"], 0.03), height=0.6, stroke_width=0,
                            fill_color=BLUE if i == 0 else GREY, fill_opacity=1).move_to([-2.1, y, 0],
                                                                                       aligned_edge=LEFT)
            value = label(percent(r["share"], 1), 32, INK, weight=BOLD).next_to(bar, RIGHT, 0.2)
            rows.add(VGroup(name, bar, value))
        # "Nearest means distance, in whatever units your columns happen to be in."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.2),
                  run_time=self.share(0.35))
        # "In metres, depth carries 99.4% of the variance."
        self.wait(max(self.share(0.5) - self.time, 0.01))
        self.play(*[GrowFromEdge(r[1], LEFT) for r in rows], run_time=self.share(0.25))
        self.play(*[FadeIn(r[2]) for r in rows], run_time=self.share(0.1))
        self.finish()


def env_panel(env, column, x, title_text, bloom=None):
    axes, frame = chart([0, 200, 50], [0, env["chlorophyll_mg_m3"].max() * 1.05, 2], 5.6, 4.2,
                        [0, 50, 100, 150, 200], [], "depth (m)", "chlorophyll")
    group = VGroup(frame)
    # Colour the clusters by their mean depth, so the colours read shallow to deep.
    order = env.groupby(column)["depth_m"].mean().sort_values().index
    colours = dict(zip(order, [ORANGE, GREEN, BLUE]))
    if bloom is not None:   # the bloom group in a colour of its own, the others shallow to deep
        colours = dict(zip([k for k in order if k != bloom], [GREEN, BLUE]))
        colours[bloom] = PURPLE
    dots = VGroup(*[Dot(axes.c2p(d, c), radius=0.045, color=colours[k], fill_opacity=0.75)
                    for d, c, k in zip(env["depth_m"], env["chlorophyll_mg_m3"], env[column])])
    group.add(dots)
    group.move_to([x, -0.5, 0])
    name = label(title_text, 32, INK, weight=BOLD).next_to(group, UP, 0.35)
    return axes, frame, dots, name, colours


class Scene09(VideoScene):
    number = 9

    def construct(self):
        env = self.data("env-clusters")
        _, raw_frame, raw_dots, raw_name, _ = env_panel(env, "raw", -3.5, "measured units: depth bands")
        # The bloom group: the standardised cluster with the highest chlorophyll.
        bloom = env.groupby("scaled")["chlorophyll_mg_m3"].mean().idxmax()
        axes, scaled_frame, scaled_dots, scaled_name, colours = env_panel(env, "scaled", 3.6, "standardised",
                                                                          bloom)
        members = env[env["scaled"] == bloom]
        bloom_name = label("spring blooms", 32, colours[bloom], weight=BOLD).move_to(
            axes.c2p(members["depth_m"].median() + 45, members["chlorophyll_mg_m3"].quantile(0.9)))
        # "So clustering those columns as they stand is clustering depth."
        self.play(FadeIn(raw_frame), FadeIn(raw_name), run_time=self.share(0.1))
        self.play(FadeIn(raw_dots, lag_ratio=0.002), run_time=self.share(0.3))
        # "Standardise them first, and a group of spring blooms appears."
        self.play(FadeIn(scaled_frame), FadeIn(scaled_name), run_time=self.share(0.1))
        self.play(FadeIn(scaled_dots, lag_ratio=0.002), run_time=self.share(0.25))
        self.play(FadeIn(bloom_name, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.finish()


def habitat_layout(scene):
    table = scene.data("habitat").pivot(index="cluster", columns="bottom", values="n")
    # Name each cluster after the seabed most of its stations are on.
    hard_cluster = table["hard"].idxmax()
    order = [hard_cluster] + [c for c in table.index if c != hard_cluster]
    cols = {"hard": 0.4, "soft": 3.6}
    rows_y = [0.6, -1.4]
    heads = VGroup(label("hard seabed", 32, SUBDUED, weight=BOLD).move_to([cols["hard"], 2.1, 0]),
                   label("soft seabed", 32, SUBDUED, weight=BOLD).move_to([cols["soft"], 2.1, 0]))
    cells, names = VGroup(), VGroup()
    wrong = VGroup()
    for i, c in enumerate(order):
        y = rows_y[i]
        names.add(label(f"group {i + 1}: {table.loc[c].sum()} stations", 32, INK, weight=BOLD
                        ).move_to([-2.0, y, 0], aligned_edge=RIGHT))
        for bottom, x in cols.items():
            right = (i == 0) == (bottom == "hard")
            box = RoundedRectangle(width=2.8, height=1.6, corner_radius=0.12, stroke_width=4,
                                   stroke_color=GREEN if right else VERMILION,
                                   fill_color=GREEN if right else VERMILION, fill_opacity=0.08).move_to([x, y, 0])
            value = label(f"{table.loc[c, bottom]}", 60, INK, weight=BOLD).move_to(box)
            cells.add(VGroup(box, value))
            if not right:
                wrong.add(value)
    total = int(table.loc[order[0], "soft"] + table.loc[order[1], "hard"])
    wrong_name = label(f"{total} of {int(table.values.sum())} on the wrong side", 34, VERMILION, weight=BOLD
                       ).to_edge(DOWN, buff=0.5)
    return heads, names, cells, wrong, wrong_name


class Scene10(VideoScene):
    number = 10

    def construct(self):
        heads, names, cells, wrong, wrong_name = habitat_layout(self)
        head = label("k-means on the counts, two groups", 32, SUBDUED).to_edge(UP, buff=0.3)
        # "On the counts, two groups find the hard and soft seabed, ..."
        self.play(FadeIn(head), FadeIn(names), run_time=self.share(0.25))
        self.play(FadeIn(heads), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.2),
                  run_time=self.share(0.3))
        # "... with 15 stations out of 800 on the wrong side."
        self.play(*[Indicate(w, color=VERMILION, scale_factor=1.3) for w in wrong], FadeIn(wrong_name),
                  run_time=self.share(0.25))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        heads, names, cells, wrong, wrong_name = habitat_layout(self)
        head = label("k-means on the counts, two groups", 32, SUBDUED).to_edge(UP, buff=0.3)
        self.add(head, heads, names, cells, wrong_name)
        never = label("never shown to k-means", 30, VERMILION, weight=BOLD).next_to(heads, UP, 0.25)
        box, mark = tick(0.7)
        found = label("found from counts alone", 34, GREEN, weight=BOLD)
        row = VGroup(box, found).arrange(RIGHT, buff=0.3).move_to(wrong_name)
        mark.move_to(box)
        # "It was never told the seabed type."
        self.play(Indicate(heads, color=VERMILION), FadeIn(never), run_time=self.share(0.4))
        # "That is what clustering is for."
        self.play(FadeOut(wrong_name), FadeIn(row), Create(mark), run_time=self.share(0.3))
        self.finish()


def noise_layout(scene):
    noise = scene.data("noise")
    side = 5.6
    frame = Square(side, color=GRID, stroke_width=3).move_to([-2.6, -0.3, 0])
    corner = frame.get_corner(DL)
    colours = [BLUE, ORANGE, GREEN, PURPLE]
    dots = VGroup(*[Dot(corner + np.array([x * side, y * side, 0]), radius=0.045,
                        color=colours[int(c) - 1], fill_opacity=0.85)
                    for x, y, c in zip(noise["x"], noise["y"], noise["cluster"])])
    grey = VGroup(*[d.copy().set_color(GREY) for d in dots])
    name = label(f"{len(noise)} points of uniform noise", 30, SUBDUED).next_to(frame, UP, 0.25)
    return frame, dots, grey, name


class Scene12(VideoScene):
    number = 12

    def construct(self):
        frame, dots, grey, name = noise_layout(self)
        ask = label("asked for four groups", 36, INK, weight=BOLD).move_to([3.6, 1.0, 0])
        get = label("four tidy groups", 36, BLUE, weight=BOLD).move_to([3.6, -0.2, 0])
        # "But give it pure noise, ..."
        self.play(Create(frame), FadeIn(grey, lag_ratio=0.002), FadeIn(name), run_time=self.share(0.3))
        # "... and ask for four groups."
        self.play(FadeIn(ask), run_time=self.share(0.15))
        # "You get four tidy groups, from nothing."
        self.play(Transform(grey, dots), FadeIn(get), run_time=self.share(0.2))
        # "k-means never says it found nothing."
        never = label("\"no structure found\"", 36, SUBDUED).move_to([3.6, -1.6, 0])
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(FadeIn(never), run_time=self.share(0.12))
        self.play(Create(strike(never)), run_time=self.share(0.15))
        self.finish()


# How many groups? (scenes 13–20) -----------------------------------------------------------

class Scene13(VideoScene):
    number = 13

    def construct(self):
        options = VGroup(*[VGroup(RoundedRectangle(width=1.1, height=1.1, corner_radius=0.15, stroke_color=GRID,
                                                   stroke_width=4),
                                  label(str(k), 44, INK, weight=BOLD)) for k in range(2, 9)])
        for o in options:
            o[1].move_to(o[0])
        options.arrange(RIGHT, buff=0.3).move_to(0.4 * UP)
        head = label("How many groups?", 44, INK, weight=BOLD).to_edge(UP, buff=1.0)
        yours = label("you choose it; k-means obeys", 34, BLUE, weight=BOLD).next_to(options, DOWN, 0.8)
        pick = SurroundingRectangle(options[0], color=BLUE, stroke_width=6, buff=0.08, corner_radius=0.15)
        # "The number of groups is your choice."
        self.play(FadeIn(head), FadeIn(options, lag_ratio=0.1), run_time=self.share(0.25))
        self.play(Create(pick), run_time=self.share(0.1))
        for i in (3, 1, 5, 0):
            self.play(pick.animate.move_to(options[i]), run_time=self.share(0.06))
        self.play(FadeIn(yours), run_time=self.share(0.1))
        # "So how do you choose it?"
        self.play(Wiggle(head), run_time=self.share(0.2))
        self.finish()


def sweep(scene):
    k = scene.data("k-sweep")
    return k[k["data"] == "observed"].sort_values("k"), k[k["data"] == "shuffled"].sort_values("k")


class Scene14(VideoScene):
    number = 14

    def construct(self):
        observed, _ = sweep(self)
        axes, frame = chart([2, 8, 1], [0.6, 1.0, 0.1], 9.0, 4.6, range(2, 9), [0.6, 0.7, 0.8, 0.9, 1.0],
                            "number of groups", "error left within groups", y_fmt="{:.1f}")
        VGroup(frame).move_to([0.4, -0.4, 0])
        line = polyline(axes, observed["k"], observed["sse_ratio"], BLUE)
        points = VGroup(*[Dot(axes.c2p(a, b), radius=0.1, color=BLUE) for a, b in zip(observed["k"], observed["sse_ratio"])])
        first, last = observed.iloc[0], observed.iloc[-1]
        ends = VGroup(label(f"{first['sse_ratio']:.3f}", 30, BLUE, weight=BOLD).next_to(points[0], RIGHT, 0.25),
                      label(f"{last['sse_ratio']:.3f}", 30, BLUE, weight=BOLD).next_to(points[-1], UP, 0.2))
        verdict = label("no elbow", 44, VERMILION, weight=BOLD).move_to(axes.c2p(6.2, 0.93))
        # "The textbook looks for an elbow in the error."
        self.play(FadeIn(frame), run_time=self.share(0.2))
        self.wait(max(self.share(0.4) - self.time, 0.01))
        # "Here it falls smoothly, from 0.878 to 0.661: ..."
        self.play(Create(line), FadeIn(points, lag_ratio=0.2), FadeIn(ends[0]), run_time=self.share(0.3))
        self.play(FadeIn(ends[1]), run_time=self.share(0.05))
        # "... no elbow."
        self.play(FadeIn(verdict, scale=1.3), run_time=self.share(0.1))
        self.finish()


def silhouette_layout(scene):
    observed, shuffled = sweep(scene)
    axes, frame = chart([2, 8, 1], [0, 0.3, 0.05], 9.0, 4.8, range(2, 9), [0, 0.1, 0.2, 0.3],
                        "number of groups", "average silhouette width", y_fmt="{:.1f}")
    VGroup(frame).move_to([0.4, -0.4, 0])

    def curve(table, colour):
        line = polyline(axes, table["k"], table["silhouette"], colour)
        dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.1, color=colour) for a, b in zip(table["k"], table["silhouette"])])
        return VGroup(line, dots)

    obs, shuf = curve(observed, BLUE), curve(shuffled, GREY)
    peak = observed.iloc[0]
    peak_name = label(f"{peak['silhouette']:.3f}", 32, BLUE, weight=BOLD).next_to(obs[1][0], UR, 0.15)
    rule = DashedLine(axes.c2p(2, 0.25), axes.c2p(8, 0.25), color=VERMILION, stroke_width=4)
    rule_name = label("rule of thumb: below 0.25, \"no structure\"", 28, VERMILION
                      ).next_to(rule, UP, 0.12).align_to(rule, RIGHT)
    floor_name = label(f"shuffled: {shuffled['silhouette'].min():.3f} to {shuffled['silhouette'].max():.3f}",
                       30, SUBDUED, weight=BOLD).next_to(axes.c2p(5, 0.035), DOWN, 0.1)
    return axes, frame, obs, shuf, peak_name, VGroup(rule, rule_name), floor_name, observed, shuffled


class Scene15(VideoScene):
    number = 15

    def construct(self):
        axes, frame, obs, _, peak_name, rule, *_ = silhouette_layout(self)
        # "The silhouette peaks at two groups, at 0.179."
        self.play(FadeIn(frame), run_time=self.share(0.1))
        self.play(Create(obs[0]), FadeIn(obs[1], lag_ratio=0.2), run_time=self.share(0.3))
        self.play(FadeIn(peak_name), Indicate(obs[1][0], scale_factor=1.6), run_time=self.share(0.15))
        # "A common rule of thumb says anything under 0.25 means no structure."
        self.play(Create(rule[0]), FadeIn(rule[1]), run_time=self.share(0.25))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        axes, frame, obs, _, peak_name, rule, *_ = silhouette_layout(self)
        self.add(frame, obs, peak_name, rule)
        box, mark = tick(0.6)
        seabed = label("the seabed split", 32, GREEN, weight=BOLD)
        note = VGroup(box, seabed).arrange(RIGHT, buff=0.25).move_to(axes.c2p(4.6, 0.205))
        mark.move_to(box)
        # "Yet that split was the seabed, almost exactly."
        self.play(FadeIn(note, shift=0.2 * RIGHT), run_time=self.share(0.35))
        self.play(Create(mark), run_time=self.share(0.2))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        # Schematic: six rows and five columns; rows 1–3 hold the first three kinds of
        # animal together, rows 4–6 the last two. Shuffling each column breaks that.
        rows, cols = 6, 5
        high = [[(r < 3) == (c < 3) for c in range(cols)] for r in range(rows)]
        size, gap = 0.8, 0.12
        x0, y0 = -((cols - 1) * (size + gap)) / 2 - 2.6, ((rows - 1) * (size + gap)) / 2 - 0.2
        cells = [[Square(size, stroke_width=0, fill_color=BLUE, fill_opacity=0.9 if high[r][c] else 0.15
                         ).move_to([x0 + c * (size + gap), y0 - r * (size + gap), 0])
                  for c in range(cols)] for r in range(rows)]
        grid = VGroup(*[s for row in cells for s in row])
        head = label("stations × kinds of animal", 30, SUBDUED).next_to(grid, UP, 0.3)
        keeps = label("each column keeps its counts", 32, INK, weight=BOLD).move_to([3.4, 0.9, 0])
        gone = label("who lives with whom: gone", 32, VERMILION, weight=BOLD).move_to([3.4, -0.3, 0])
        none = label("no groups left to find", 32, SUBDUED, weight=BOLD).move_to([3.4, -1.5, 0])
        # "So shuffle each column on its own."
        self.play(FadeIn(grid, lag_ratio=0.02), FadeIn(head), run_time=self.share(0.15))
        rng = np.random.default_rng(18)
        moves = []
        for c in range(cols):
            order = rng.permutation(rows)
            while (order == np.arange(rows)).all():
                order = rng.permutation(rows)
            for r in range(rows):
                moves.append(cells[r][c].animate.move_to(cells[order[r]][c].get_center()))
        self.play(*moves, run_time=self.share(0.25))
        # "Each animal keeps its counts, ..."
        self.play(FadeIn(keeps), run_time=self.share(0.12))
        # "... but who lives with whom is gone."
        self.play(FadeIn(gone), run_time=self.share(0.12))
        self.play(FadeIn(none), run_time=self.share(0.1))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        axes, frame, obs, shuf, peak_name, rule, floor_name, observed, shuffled = silhouette_layout(self)
        self.add(frame, obs, peak_name, rule)
        times = observed["silhouette"].iloc[0] / shuffled["silhouette"].iloc[0]
        ratio = label(f"{times:.1f} × the floor", 32, BLUE, weight=BOLD).next_to(peak_name, RIGHT, 0.4)
        # "On shuffled data, the silhouette stays between 0.037 and 0.055."
        self.play(FadeOut(rule), Create(shuf[0]), FadeIn(shuf[1], lag_ratio=0.2), run_time=self.share(0.35))
        self.play(FadeIn(floor_name), run_time=self.share(0.15))
        # "Against that floor, 0.179 is nearly five times as high."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeIn(ratio), Indicate(peak_name), run_time=self.share(0.25))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        criteria = self.data("criteria").set_index("criterion")["k"]
        cards = [("the elbow", "no answer", SUBDUED),
                 ("silhouette, against shuffled", f"{criteria['silhouette against shuffled']}", INK),
                 ("gap statistic, default reference", f"{criteria['gap statistic']}", INK),
                 ("mixture model, by BIC", f"{criteria['mixture BIC']}", INK)]
        group = VGroup()
        for name, answer, colour in cards:
            box = RoundedRectangle(width=3.1, height=2.6, corner_radius=0.15, stroke_color=GRID, stroke_width=4)
            text = VGroup(*[label(t, 26, SUBDUED) for t in name.split(", ")]).arrange(DOWN, buff=0.08)
            value = label(answer, 72 if answer.isdigit() else 36, colour, weight=BOLD)
            inner = VGroup(text, value).arrange(DOWN, buff=0.3).move_to(box)
            group.add(VGroup(box, inner))
        group.arrange(RIGHT, buff=0.3).move_to(0.6 * UP)
        truth = label("the truth built into the data: 2", 40, GREEN, weight=BOLD).next_to(group, DOWN, 0.8)
        # "Other criteria disagree."
        self.play(FadeIn(group[0]), FadeIn(group[1]), run_time=self.share(0.2))
        # "The gap statistic, with its default reference, says six."
        self.play(FadeIn(group[2], shift=0.2 * UP), run_time=self.share(0.2))
        # "A mixture model says three."
        self.wait(max(self.share(0.55) - self.time, 0.01))
        self.play(FadeIn(group[3], shift=0.2 * UP), run_time=self.share(0.15))
        # "The truth is two."
        self.wait(max(self.share(0.8) - self.time, 0.01))
        self.play(FadeIn(truth), group[1][0].animate.set_stroke(GREEN, 6), run_time=self.share(0.12))
        self.finish()


LINKAGE_NAMES = {"single": ("single", VERMILION), "average": ("average", ORANGE),
                 "complete": ("complete", PURPLE), "ward.D2": ("Ward", BLUE)}


class Scene20(VideoScene):
    number = 20

    def construct(self):
        linkages = self.data("linkages")
        axes, frame = chart([2, 6, 1], [0, 1, 0.25], 8.4, 4.8, range(2, 7), [0, 0.25, 0.5, 0.75, 1],
                            "number of groups", "agreement with the true split", y_fmt="{:.2f}")
        VGroup(frame).move_to([-0.6, -0.5, 0])
        head = label("One distance matrix, four ways to build the tree", 32, SUBDUED).to_edge(UP, buff=0.3)
        lines = VGroup()
        for key, (name, colour) in LINKAGE_NAMES.items():
            rows = linkages[linkages["linkage"] == key].sort_values("k")
            line = polyline(axes, rows["k"], rows["agreement_with_substrate"], colour)
            dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.08, color=colour)
                            for a, b in zip(rows["k"], rows["agreement_with_substrate"])])
            tag = label(name, 30, colour, weight=BOLD).next_to(dots[-1], RIGHT, 0.25)
            lines.add(VGroup(line, dots, tag))
        # Keep the end labels apart where lines end close together.
        tags = sorted([l[2] for l in lines], key=lambda t: t.get_y())
        for below, above in zip(tags, tags[1:]):
            if above.get_y() - below.get_y() < 0.45:
                above.set_y(below.get_y() + 0.45)
        lo = linkages.loc[linkages["agreement_with_substrate"].idxmin()]
        hi = linkages.loc[linkages["agreement_with_substrate"].idxmax()]
        # In the clear space between the single and average lines, pointing at its point.
        lo_name = label(f"{lo['agreement_with_substrate']:.3f}", 32, VERMILION, weight=BOLD
                        ).move_to(axes.c2p(3.5, 0.13))
        lo_name = VGroup(lo_name, Arrow(lo_name.get_left(), axes.c2p(lo["k"], lo["agreement_with_substrate"]),
                                        buff=0.15, color=VERMILION, stroke_width=4))
        hi_name = label(f"{hi['agreement_with_substrate']:.3f}", 32, BLUE, weight=BOLD
                        ).next_to(axes.c2p(hi["k"], hi["agreement_with_substrate"]), RIGHT, 0.25)
        # "Settings decide too: ..."
        self.play(FadeIn(head), FadeIn(frame), run_time=self.share(0.15))
        # "... four ways of building a cluster tree match the true split ..."
        self.play(LaggedStart(*[AnimationGroup(Create(l[0]), FadeIn(l[1]), FadeIn(l[2])) for l in lines],
                              lag_ratio=0.3), run_time=self.share(0.45))
        # "... anywhere from 0.005 to 0.889."
        self.play(FadeIn(lo_name), run_time=self.share(0.1))
        self.play(FadeIn(hi_name), run_time=self.share(0.1))
        self.finish()


class Scene21(KeyPointScene):
    number, point = 21, 1


# A map of the stations (scenes 22–32) ------------------------------------------------------

class Scene22(VideoScene):
    number = 22

    def construct(self):
        # Schematic: a tilted cloud, and new axes turning to its longest spread.
        rng = np.random.default_rng(24)
        raw = rng.normal(0, 1, (80, 2)) * [2.2, 0.6]
        angle = 0.5
        rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        points = raw @ rot.T + [0, -0.4]
        dots = VGroup(*[Dot([x, y, 0], radius=0.08, color=GREY) for x, y in points])
        centre = np.array([0, -0.4, 0])
        old = VGroup(Line(centre + 5 * LEFT, centre + 5 * RIGHT, color=GRID, stroke_width=4),
                     Line(centre + 3 * DOWN, centre + 3 * UP, color=GRID, stroke_width=4))
        new = old.copy().set_color(BLUE)
        names = VGroup(label("first component", 30, BLUE, weight=BOLD), label("second", 30, BLUE, weight=BOLD))
        head = label("New axes: weighted sums of the columns", 34, SUBDUED).to_edge(UP, buff=0.3)
        # "Principal component analysis ..."
        self.play(FadeIn(dots, lag_ratio=0.02), FadeIn(old), run_time=self.share(0.2))
        # "... builds new axes from the columns, ..."
        self.play(FadeIn(head), run_time=self.share(0.1))
        self.play(Rotate(new, angle, about_point=centre), run_time=self.share(0.3))
        # "... ordered by how much of the spread they hold."
        names[0].next_to(new[0].get_end(), UP, 0.1).shift(0.6 * LEFT)
        names[1].next_to(new[1].get_end(), LEFT, 0.15)
        self.play(FadeIn(names), run_time=self.share(0.15))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        variance = self.data("variance").sort_values("component")
        axes, frame = chart([0, len(variance) + 1, 1], [0, 0.2, 0.05], 10.0, 4.4, [1, 2, 6, 12, 18, 24],
                            [0, 0.05, 0.1, 0.15, 0.2], "component", "share of the variance",
                            y_fmt="{:.0%}")
        VGroup(frame).move_to([0.2, -0.6, 0])
        width = axes.x_axis.get_unit_size() * 0.7
        bars = VGroup()
        for c, p in zip(variance["component"], variance["proportion"]):
            base = axes.c2p(c, 0)
            bars.add(Rectangle(width=width, height=axes.y_axis.get_unit_size() * p, stroke_width=0,
                               fill_color=BLUE if c <= 2 else GREY, fill_opacity=1).move_to(base, aligned_edge=DOWN))
        two = variance["proportion"].iloc[:2]
        tags = VGroup()
        together = label(f"the first two: {percent(two.iloc[0], 1)} + {percent(two.iloc[1], 1)} = "
                         f"{percent(two.sum(), 1)}", 34, BLUE, weight=BOLD).move_to(axes.c2p(5, 0.17), aligned_edge=LEFT)
        rest = label("the rest: mostly sampling noise", 32, SUBDUED, weight=BOLD
                     ).move_to(axes.c2p(5, 0.1), aligned_edge=LEFT)
        # "The first two hold 29.4% of the variance."
        self.play(FadeIn(frame), GrowFromEdge(bars[:2], DOWN), run_time=self.share(0.2))
        self.play(FadeIn(tags), FadeIn(together), run_time=self.share(0.15))
        # "That sounds poor, but most of the rest is sampling noise, and here we know it is."
        self.wait(max(self.share(0.45) - self.time, 0.01))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[2:]], lag_ratio=0.05), FadeIn(rest),
                  run_time=self.share(0.3))
        self.finish()


def ordination_layout(scene):
    stations = scene.data("ordination")
    x_lo, x_hi = np.floor(stations["PC1"].min()), np.ceil(stations["PC1"].max())
    y_lo, y_hi = np.floor(stations["PC2"].min()), np.ceil(stations["PC2"].max())
    height = 6.0
    width = height * (x_hi - x_lo) / (y_hi - y_lo)
    axes = plain_axes([x_lo, x_hi, 1], [y_lo, y_hi, 1], width, height).move_to([-1.6, -0.35, 0])
    axes.set_stroke(opacity=0.5, width=2)       # faint lines through zero; the box is the frame
    box = Rectangle(width=width, height=height, color=GRID, stroke_width=3).move_to(
        (axes.c2p(x_lo, y_lo) + axes.c2p(x_hi, y_hi)) / 2)
    lo, hi = stations["depth_m"].min(), stations["depth_m"].max()
    dots = VGroup(*[marker(axes.c2p(a, b), viridis((d - lo) / (hi - lo)), bottom == "hard", 0.06)
                    for a, b, d, bottom in zip(stations["PC1"], stations["PC2"], stations["depth_m"],
                                               stations["bottom"])])
    x_name = label("first component", 28, SUBDUED).next_to(box, DOWN, 0.15)
    y_name = label("second component", 28, SUBDUED).next_to(box, UP, 0.15)
    key = VGroup(depth_key(2.2),
                 VGroup(marker(ORIGIN, INK, True, 0.1), label("hard seabed", 26, SUBDUED)).arrange(RIGHT, buff=0.2),
                 VGroup(marker(ORIGIN, INK, False, 0.1), label("soft seabed", 26, SUBDUED)).arrange(RIGHT, buff=0.2)
                 ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_corner(UR, buff=0.4)
    return stations, axes, dots, VGroup(axes, box, x_name, y_name), key, x_name


SIDE_X = 4.7    # right of the map, under the key: where the map's notes go


class Scene24(VideoScene):
    number = 24

    def construct(self):
        stations, axes, dots, frame, key, _ = ordination_layout(self)
        # "The map shows both structures."
        self.play(FadeIn(frame), FadeIn(key), run_time=self.share(0.15))
        self.play(FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.3))
        # "The hard seabed sticks out as its own arm, and depth runs smoothly up each arm, ..."
        hard = VGroup(*[d for d, b in zip(dots, stations["bottom"]) if b == "hard"])
        self.play(Indicate(hard, color=None, scale_factor=1.3), run_time=self.share(0.25))
        self.play(Indicate(key[0], color=None), run_time=self.share(0.15))
        self.finish()


def ordination_notes(stations, axes):
    hard = stations[stations["bottom"] == "hard"]
    soft = stations[stations["bottom"] == "soft"]
    arm = axes.c2p(hard["PC1"].quantile(0.8), hard["PC2"].quantile(0.8))
    ramp = axes.c2p(soft["PC1"].quantile(0.15), soft["PC2"].median())
    arm_note = label("a separate arm:\na boundary", 30, VERMILION, weight=BOLD).move_to([SIDE_X, 0.6, 0])
    ramp_note = label("a smooth ramp:\na gradient", 28, VERMILION, weight=BOLD).move_to([-5.75, -2.2, 0])
    return VGroup(Arrow(arm_note.get_left(), arm, color=VERMILION, buff=0.15, stroke_width=4), arm_note), \
        VGroup(Arrow(ramp_note.get_top(), ramp, color=VERMILION, buff=0.15, stroke_width=4), ramp_note)


class Scene25(VideoScene):
    number = 25

    def construct(self):
        stations, axes, dots, frame, key, _ = ordination_layout(self)
        self.add(frame, key, dots)
        arm, ramp = ordination_notes(stations, axes)
        # "A separate arm is a boundary."
        self.play(FadeIn(arm[1]), GrowArrow(arm[0]), run_time=self.share(0.3))
        # "A smooth ramp is a gradient."
        self.wait(max(self.share(0.5) - self.time, 0.01))
        self.play(FadeIn(ramp[1]), GrowArrow(ramp[0]), run_time=self.share(0.3))
        self.finish()


class Scene26(VideoScene):
    number = 26

    def construct(self):
        stations, axes, dots, frame, key, x_name = ordination_layout(self)
        self.add(frame, key, dots)
        guess = label("= depth?", 36, VERMILION, weight=BOLD).next_to(x_name, LEFT, 0.25)
        # "Now name the axes. Is the first one depth?"
        self.play(Indicate(axes.x_axis, color=VERMILION), run_time=self.share(0.3))
        self.play(FadeIn(guess, shift=0.2 * LEFT), run_time=self.share(0.3))
        self.finish()


def direction_arrows(scene, axes):
    directions = scene.data("directions").set_index("gradient")
    arrows = VGroup()
    origin = axes.c2p(0, 0)
    for name, colour in (("depth", VERMILION), ("hard bottom", VERMILION)):
        r = directions.loc[name]
        unit = np.array([r["x"], r["y"]]) / np.hypot(r["x"], r["y"])
        tip = axes.c2p(*(4.2 * unit))
        arrow = Arrow(origin, tip, buff=0, color=colour, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        text = label(f"{name}: {r['angle']:.0f}°", 32, colour, weight=BOLD).next_to(tip, UP, 0.12)
        arrows.add(VGroup(arrow, text))
    return arrows


class Scene27(VideoScene):
    number = 27

    def construct(self):
        stations, axes, dots, frame, key, x_name = ordination_layout(self)
        self.add(frame, key, dots.set_opacity(0.35))
        guess = label("= depth?", 36, VERMILION, weight=BOLD).next_to(x_name, LEFT, 0.25)
        self.add(guess)
        arrows = direction_arrows(self, axes)
        verdict = label("both at about 45°\nto the axes", 34, INK, weight=BOLD).move_to([SIDE_X, -0.6, 0])
        # "No. Depth increases at 139 degrees from the first axis, ..."
        self.play(Create(strike(guess)), run_time=self.share(0.1))
        self.play(GrowArrow(arrows[0][0]), FadeIn(arrows[0][1]), run_time=self.share(0.25))
        # "... and hard bottom at 41."
        self.play(GrowArrow(arrows[1][0]), FadeIn(arrows[1][1]), run_time=self.share(0.2))
        # "Both lie at about 45 degrees to the axes."
        self.play(FadeIn(verdict), run_time=self.share(0.15))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        stations, axes, dots, frame, key, _ = ordination_layout(self)
        arrows = direction_arrows(self, axes)
        self.add(frame, key, dots.set_opacity(0.35), arrows)
        origin = axes.c2p(0, 0)
        cross = VGroup(DashedLine(origin + 2.3 * LEFT, origin + 2.3 * RIGHT, color=BLUE, stroke_width=5),
                       DashedLine(origin + 2.3 * DOWN, origin + 2.3 * UP, color=BLUE, stroke_width=5))
        note = label("any turn fits\nalmost as well", 32, BLUE, weight=BOLD).move_to([SIDE_X, -0.2, 0])
        verdict = label("PCA finds the plane,\nnot the gradients", 34, INK, weight=BOLD).move_to([SIDE_X, -2.0, 0])
        # "The two carry almost the same variance, so nothing tells PCA which way to turn its axes."
        self.play(Create(cross), FadeIn(note), run_time=self.share(0.15))
        self.play(Rotate(cross, PI / 4, about_point=origin), run_time=self.share(0.2))
        self.play(Rotate(cross, -PI / 3, about_point=origin), run_time=self.share(0.2))
        self.play(Rotate(cross, PI / 12, about_point=origin), run_time=self.share(0.1))
        # "It finds the plane, not the gradients."
        self.play(FadeIn(verdict), run_time=self.share(0.15))
        self.finish()


class Scene29(VideoScene):
    number = 29

    def construct(self):
        rules = self.data("rules").set_index("rule")["components"]
        names = [("80% of the variance", "80% of variance"), ("eigenvalue above 1", "Kaiser"),
                 ("beat shuffled data", "parallel analysis")]
        group = VGroup()
        for text, key in names:
            box = RoundedRectangle(width=3.8, height=2.8, corner_radius=0.15, stroke_color=GRID, stroke_width=4)
            inner = VGroup(label(text, 30, SUBDUED), label(f"{rules[key]}", 90, INK, weight=BOLD),
                           label("components", 26, SUBDUED)).arrange(DOWN, buff=0.2).move_to(box)
            group.add(VGroup(box, inner))
        group.arrange(RIGHT, buff=0.4).move_to(0.2 * DOWN)
        head = label("How many of the 24 components to keep?", 36, INK, weight=BOLD).to_edge(UP, buff=0.9)
        # "How many components should you keep?"
        self.play(FadeIn(head), run_time=self.share(0.3))
        # "Three common rules say sixteen, seven, and three."
        self.play(LaggedStart(*[FadeIn(g, shift=0.2 * UP) for g in group], lag_ratio=0.5), run_time=self.share(0.5))
        self.finish()


class Scene30(VideoScene):
    number = 30

    def construct(self):
        cv = self.data("components-cv").sort_values("num_comp")
        axes, frame = chart([0, 25, 1], [18, 32, 2], 9.6, 4.6, [1, 2, 4, 8, 14, 18, 24], [20, 24, 28, 32],
                            "components kept", "error predicting depth (m)")
        VGroup(frame).move_to([0.3, -0.5, 0])
        head = label("Predicting depth from the components", 32, SUBDUED).to_edge(UP, buff=0.3)
        line = polyline(axes, cv["num_comp"], cv["mean"], BLUE)
        dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.09, color=BLUE) for a, b in zip(cv["num_comp"], cv["mean"])])
        one, two, last = cv.iloc[0], cv.iloc[1], cv.iloc[-1]
        tags = [label(f"one: {one['mean']:.1f} m", 30, INK, weight=BOLD).next_to(dots[0], RIGHT, 0.3),
                label(f"two: {two['mean']:.1f} m", 32, BLUE, weight=BOLD).move_to(axes.c2p(6, 25), aligned_edge=LEFT),
                label(f"all {last['num_comp']:.0f}: {last['mean']:.1f} m", 30, INK, weight=BOLD
                      ).next_to(dots[-1], UP, 0.35).shift(0.5 * LEFT)]
        mark = Arrow(tags[1].get_left(), dots[1].get_center(), buff=0.15, color=BLUE, stroke_width=4)
        # "Let the task decide. Predict depth from the components: ..."
        self.play(FadeIn(head), FadeIn(frame), run_time=self.share(0.2))
        # "... one gives an error of 30.4 metres, ..."
        self.wait(max(self.share(0.35) - self.time, 0.01))
        self.play(FadeIn(dots[0], scale=2), FadeIn(tags[0]), run_time=self.share(0.1))
        # "... two give 21.2, ..."
        self.play(Create(line), FadeIn(dots[1:], lag_ratio=0.1), GrowArrow(mark), FadeIn(tags[1]),
                  run_time=self.share(0.2))
        # "... and all 24 do no better than two."
        self.play(FadeIn(tags[2]), Indicate(dots[-1], scale_factor=1.8), run_time=self.share(0.15))
        self.finish()


def umap_panel(umap, xcol, ycol, centre, title_text):
    xs, ys = umap[xcol], umap[ycol]
    size = 5.0
    span = max(xs.max() - xs.min(), ys.max() - ys.min())
    to = lambda x, y: np.array([centre[0] + (x - (xs.max() + xs.min()) / 2) / span * size,  # noqa: E731
                                centre[1] + (y - (ys.max() + ys.min()) / 2) / span * size, 0])
    lo, hi = umap["depth_m"].min(), umap["depth_m"].max()
    dots = VGroup(*[Dot(to(x, y), radius=0.045, color=viridis((d - lo) / (hi - lo)), fill_opacity=0.9)
                    for x, y, d in zip(xs, ys, umap["depth_m"])])
    frame = RoundedRectangle(width=size + 0.6, height=size + 0.6, corner_radius=0.15, stroke_color=GRID,
                             stroke_width=3).move_to([*centre, 0])
    name = label(title_text, 32, INK, weight=BOLD).next_to(frame, UP, 0.2)
    return dots, VGroup(frame, name), to


class Scene31(VideoScene):
    number = 31

    def construct(self):
        umap = self.data("umap")
        dots, frame, to = umap_panel(umap, "x", "y", (-3.4, -0.5), "the survey")
        key = depth_key(2.2).to_edge(DOWN, buff=0.2).set_x(-3.4)
        hard = umap[umap["bottom"] == "hard"]
        arm = to(hard["x"].median(), hard["y"].median())
        note = label("hard seabed", 30, VERMILION, weight=BOLD).move_to(arm + np.array([0.1, 1.9, 0]))
        pointer = Arrow(note.get_bottom(), arm, buff=0.15, color=VERMILION, stroke_width=4)
        # "UMAP draws a prettier map."
        self.play(FadeIn(frame), FadeIn(key), FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.3))
        # "The hard seabed pulls out as its own arm, ..."
        self.play(FadeIn(note), GrowArrow(pointer), run_time=self.share(0.2))
        # "... and depth runs smoothly along both."
        self.play(Indicate(key, color=None), run_time=self.share(0.25))
        self.finish()


class Scene32(VideoScene):
    number = 32

    def construct(self):
        umap = self.data("umap")
        dots, frame, to = umap_panel(umap, "x", "y", (-3.4, -0.5), "the survey")
        key = depth_key(2.2).to_edge(DOWN, buff=0.2).set_x(-3.4)
        hard = umap[umap["bottom"] == "hard"]
        arm = to(hard["x"].median(), hard["y"].median())
        note = label("hard seabed", 30, VERMILION, weight=BOLD).move_to(arm + np.array([0.1, 1.9, 0]))
        pointer = Arrow(note.get_bottom(), arm, buff=0.15, color=VERMILION, stroke_width=4)
        self.add(frame, key, dots, note, pointer)
        null_dots, null_frame, _ = umap_panel(umap, "null_x", "null_y", (3.4, -0.5), "shuffled: nothing in it")
        verdict = label("a shape, but no colour pattern", 30, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.2).set_x(3.4)
        # "But shuffled data, with nothing in it, still makes a shape."
        self.play(FadeIn(null_frame), FadeIn(null_dots, lag_ratio=0.001), run_time=self.share(0.4))
        # "Only the colours give it away."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeIn(verdict), run_time=self.share(0.2))
        self.finish()


class Scene33(KeyPointScene):
    number, point = 33, 2


# Is it real? (scenes 34–38) ----------------------------------------------------------------

QUESTIONS = ["Does it replicate?", "Is it a group, or a cut through a gradient?",
             "Does it match something it never saw?"]


class Scene34(VideoScene):
    number = 34

    def construct(self):
        head = title("Three questions for any pattern", 52).to_edge(UP, buff=1.0)
        rows = VGroup(*[VGroup(badge(i), label(q, 40)).arrange(RIGHT, buff=0.45) for i, q in enumerate(QUESTIONS, 1)])
        rows.arrange(DOWN, buff=0.7, aligned_edge=LEFT).next_to(head, DOWN, 0.9).set_x(0)
        # "With nothing held out to check against, ..."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.2))
        # "... ask three questions of any pattern."
        self.wait(max(self.share(0.45) - self.time, 0.01))
        self.play(LaggedStart(*[FadeIn(r, shift=0.3 * RIGHT) for r in rows], lag_ratio=0.4), run_time=self.share(0.4))
        self.finish()


BIN = 0.05


def dot_stack(values, to_x, base, colour=BLUE, radius=0.05, step=0.105):
    """A dot plot: each value a dot, stacked in bins of BIN, as the page's histogram."""
    counts = {}
    dots = VGroup()
    for v in sorted(values):
        b = min(int(v / BIN), int(1 / BIN) - 1)
        n = counts.get(b, 0)
        counts[b] = n + 1
        dots.add(Dot([to_x((b + 0.5) * BIN), base + radius + step * n, 0], radius=radius, color=colour))
    return dots


def bootstrap_layout(scene):
    reps = scene.data("replicates")
    axis, to_x = number_line(0, 1, -5.6, 5.6, -2.9, [0, 0.25, 0.5, 0.75, 1], 2)
    name = label("agreement with the original split", 26, SUBDUED).next_to(axis, DOWN, 0.05)
    values = reps["agreement"].to_numpy()
    dots = dot_stack(values, to_x, -2.9)
    mean = values.mean()
    mean_line = DashedLine([to_x(mean), -2.9, 0], [to_x(mean), 2.4, 0], color=VERMILION, stroke_width=4)
    mean_name = label(f"average {mean:.3f}", 32, VERMILION, weight=BOLD).next_to(mean_line, LEFT, 0.2).shift(1.8 * UP)
    head = label(f"{len(reps)} resamples of the whole survey, clustered again", 32, SUBDUED).to_edge(UP, buff=0.3)
    return reps, to_x, VGroup(axis, name), dots, VGroup(mean_line, mean_name), head


class Scene35(VideoScene):
    number = 35

    def construct(self):
        reps, to_x, axis, dots, mean, head = bootstrap_layout(self)
        # "First, does it replicate? Cluster sixty resamples of the whole survey."
        self.play(FadeIn(head), FadeIn(axis), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d, shift=0.5 * DOWN) for d in dots], lag_ratio=0.05),
                  run_time=self.share(0.4))
        # "Their average agreement with the original split is 0.881."
        self.play(Create(mean[0]), FadeIn(mean[1]), run_time=self.share(0.2))
        self.finish()


class Scene36(VideoScene):
    number = 36

    def construct(self):
        reps, to_x, axis, dots, mean, head = bootstrap_layout(self)
        self.add(head, axis, dots, mean)
        same = (reps["agreement"] > 0.5).sum()
        other = len(reps) - same
        top = max(d.get_y() for d in dots)
        same_name = label(f"{same}: the same split", 32, BLUE, weight=BOLD).move_to([to_x(0.97), top + 0.4, 0],
                                                                                   aligned_edge=RIGHT)
        other_name = label(f"{other}: something else", 32, ORANGE, weight=BOLD).move_to([to_x(0.02), -1.6, 0],
                                                                                        aligned_edge=LEFT)
        low = VGroup(*[d for d in dots if d.get_x() < to_x(0.5)])
        gap = Rectangle(width=to_x(0.88) - to_x(0.18), height=0.9, stroke_width=0, fill_color=GREY, fill_opacity=0.15
                        ).move_to([(to_x(0.18) + to_x(0.88)) / 2, -2.4, 0])
        gap_name = label("no resample here", 28, SUBDUED).move_to(gap)
        # "But fifty-three resamples found that split almost exactly, ..."
        self.play(FadeIn(same_name), run_time=self.share(0.2))
        # "... and seven found something else entirely."
        self.play(low.animate.set_color(ORANGE), FadeIn(other_name), run_time=self.share(0.2))
        # "The average describes no resample that happened."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeIn(gap), FadeIn(gap_name), Indicate(mean[1], color=VERMILION), run_time=self.share(0.25))
        self.finish()


class Scene37(VideoScene):
    number = 37

    def construct(self):
        reps, to_x, axis, dots, mean, head = bootstrap_layout(self)
        top = max(d.get_y() for d in dots)
        low = VGroup(*[d for d in dots if d.get_x() < to_x(0.5)]).set_color(ORANGE)
        self.add(head, axis, dots, mean)
        minority = reps[reps["agreement"] <= 0.5]
        depth_name = VGroup(label("a depth split", 34, ORANGE, weight=BOLD),
                            label(f"correlation with depth {minority['depth_correlation'].mean():.2f}", 26, ORANGE)
                            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([to_x(0.02), -1.3, 0], aligned_edge=LEFT)
        seabed_name = label("the seabed split", 34, BLUE, weight=BOLD).move_to([to_x(0.97), top + 0.4, 0],
                                                                              aligned_edge=RIGHT)
        report = label("two answers: report the spread, not its average", 34, INK, weight=BOLD
                       ).move_to([-0.8, 0.1, 0])
        # "The seven had cut the survey by depth."
        self.play(FadeIn(depth_name), Indicate(low, color=ORANGE), run_time=self.share(0.3))
        self.play(FadeIn(seabed_name), run_time=self.share(0.1))
        # "That is two answers, not one noisy one. Report the spread, not its average."
        self.play(FadeIn(report, shift=0.2 * UP), mean.animate.set_opacity(0.3), run_time=self.share(0.3))
        self.finish()


class Scene38(VideoScene):
    number = 38

    def construct(self):
        reps = self.data("replicates")["agreement"].to_numpy()
        soft = self.data("soft-stability")["agreement"].to_numpy()
        axis, to_x = number_line(0, 1, -3.6, 6.0, -2.6, [0, 0.25, 0.5, 0.75, 1], 2)
        name = label("agreement across 60 resamples", 26, SUBDUED).next_to(axis, DOWN, 0.05).set_x(1.2)
        rng = np.random.default_rng(40)
        rows = {}
        for key, values, y, colour, text in (("whole", reps, 0.9, ORANGE, "the seabed split"),
                                             ("soft", soft, -1.1, BLUE, "the puzzle's split")):
            dots = VGroup(*[Dot([to_x(v), y + rng.uniform(-0.35, 0.35), 0], radius=0.08, color=colour,
                                fill_opacity=0.8) for v in values])
            tag = label(text, 30, colour, weight=BOLD).move_to([-6.8, y, 0], aligned_edge=LEFT)
            low = label(f"lowest {values.min():.3f}" if values.min() < 0.5 else f"never below {values.min():.2f}",
                        28, colour, weight=BOLD).next_to([to_x(values.min()), y + 0.4, 0], UP, 0.1)
            rows[key] = VGroup(tag, dots, low)
        head = label("Is it a group, or a cut through a gradient?", 38, INK, weight=BOLD).to_edge(UP, buff=0.4)
        # "Second: is it a group, or a cut through a gradient?"
        self.play(FadeIn(head), FadeIn(VGroup(axis, name)), run_time=self.share(0.2))
        # "The puzzle's split was even more stable than the seabed split: ..."
        self.play(FadeIn(rows["whole"][0]), FadeIn(rows["whole"][1]), run_time=self.share(0.15))
        self.play(FadeIn(rows["soft"][0]), FadeIn(rows["soft"][1]), run_time=self.share(0.15))
        # "... never below 0.71, where the seabed split fell to 0.095."
        self.wait(max(self.share(0.6) - self.time, 0.01))
        self.play(FadeIn(rows["soft"][2]), run_time=self.share(0.12))
        self.play(FadeIn(rows["whole"][2]), run_time=self.share(0.12))
        self.finish()


# The puzzle, solved (scenes 39–45) ---------------------------------------------------------

def continuum_layout(scene):
    curves = scene.data("continuum")
    curves["count"] = curves["count"].clip(lower=0)
    medians = scene.data("soft-medians")
    top = np.ceil(curves["count"].max())
    axes, frame = chart([0, 200, 20], [0, top, 1], 10.0, 4.6, [0, 50, 100, 150, 200], [], "depth (m)",
                        "animals per station")
    VGroup(frame).move_to([-0.2, -0.6, 0])
    lo, hi = curves["depth_optimum_m"].min(), curves["depth_optimum_m"].max()
    lines = VGroup()
    for _, c in curves.groupby("depth_optimum_m"):
        c = c.sort_values("depth_m")
        colour = viridis((c["depth_optimum_m"].iloc[0] - lo) / (hi - lo))
        lines.add(polyline(axes, c["depth_m"], c["count"], colour, width=6))
    boundary = medians["boundary"].iloc[0]
    cut = DashedLine(axes.c2p(boundary, 0), axes.c2p(boundary, top), color=VERMILION, stroke_width=5)
    cut_name = label(f"k-means' cut: about {boundary:.0f} m", 32, VERMILION, weight=BOLD
                     ).next_to(cut, UP, 0.1)
    head = label("Eight soft-bottom animals along depth", 32, SUBDUED).to_edge(UP, buff=0.3)
    return axes, frame, lines, VGroup(cut, cut_name), head


class Scene39(VideoScene):
    number = 39

    def construct(self):
        axes, frame, lines, cut, head = continuum_layout(self)
        note = label("favourite depths spread evenly, 20 to 160 m", 30, INK, weight=BOLD
                     ).next_to(frame, UP, 0.25)
        # "But every kind of animal here was given a favourite depth, ..."
        self.play(FadeIn(frame), run_time=self.share(0.15))
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3), run_time=self.share(0.5))
        # "... spread evenly from 20 to 160 metres."
        self.play(FadeIn(note), run_time=self.share(0.15))
        self.finish()


def continuum_note(frame):
    return label("favourite depths spread evenly, 20 to 160 m", 30, INK, weight=BOLD).next_to(frame, UP, 0.25)


class Scene40(VideoScene):
    number = 40

    def construct(self):
        axes, frame, lines, cut, head = continuum_layout(self)
        note = continuum_note(frame)
        self.add(frame, lines, note)
        overlap = label("no gap anywhere", 34, BLUE, weight=BOLD).move_to(axes.c2p(100, axes.y_range[1] * 0.97))
        # "Each peaks a little deeper than the last, and neighbours overlap: ..."
        for l in lines:
            self.play(l.animate.set_stroke(width=12), run_time=self.share(0.06))
            self.play(l.animate.set_stroke(width=6), run_time=self.share(0.02))
        # "... there is no depth where one set hands over to another."
        self.play(FadeIn(overlap), run_time=self.share(0.15))
        self.finish()


class Scene41(VideoScene):
    number = 41

    def construct(self):
        axes, frame, lines, cut, head = continuum_layout(self)
        self.add(frame, lines)
        y = cut[0].get_top()[1] - 0.25
        sides = VGroup(label("shallow group", 30, ORANGE, weight=BOLD).move_to([cut[0].get_x() - 0.2, y, 0],
                                                                                aligned_edge=RIGHT),
                       label("deep group", 30, BLUE, weight=BOLD).move_to([cut[0].get_x() + 0.2, y, 0],
                                                                          aligned_edge=LEFT))
        stable = label("a stable cut through a stable gradient", 32, INK, weight=BOLD).to_edge(DOWN, buff=0.15)
        # "k-means cut that slope at about 92 metres, in the same place every time."
        self.play(Create(cut[0]), FadeIn(cut[1]), run_time=self.share(0.3))
        self.play(FadeIn(sides), run_time=self.share(0.15))
        # "A stable method cuts a stable gradient in a stable place."
        self.wait(max(self.share(0.55) - self.time, 0.01))
        self.play(FadeIn(stable), run_time=self.share(0.2))
        self.finish()


class Scene42(VideoScene):
    number = 42

    def construct(self):
        wrong = label("two soft-bottom communities", 44, SUBDUED, weight=BOLD).move_to(1.2 * UP)
        right = label("one continuous turnover with depth", 44, GREEN, weight=BOLD).move_to(0.8 * DOWN)
        box, mark = tick(0.8)
        box.next_to(right, LEFT, 0.4)
        mark.move_to(box)
        # "So there are no two soft-bottom communities."
        self.play(FadeIn(wrong), run_time=self.share(0.2))
        self.play(Create(strike(wrong)), run_time=self.share(0.2))
        # "Just one continuous turnover with depth."
        self.play(FadeIn(right, shift=0.2 * UP), FadeIn(box), run_time=self.share(0.25))
        self.play(Create(mark), run_time=self.share(0.1))
        self.finish()


def external_layout(scene):
    external = scene.data("external").set_index("clustering")
    cols = {"substrate": (0.6, "seabed type", "a category"), "depth_band": (4.4, "depth bands", "a measurement, cut")}
    rows = {"all stations": (0.8, "whole-survey split"), "soft stations only": (-1.4, "soft-bottom split")}
    heads = VGroup(*[VGroup(label(name, 32, INK, weight=BOLD), label(kind, 26, SUBDUED)).arrange(DOWN, buff=0.1
                                                                                                  ).move_to([x, 2.5, 0])
                     for x, name, kind in cols.values()])
    names = VGroup(*[label(name, 32, INK, weight=BOLD).move_to([-2.2, y, 0], aligned_edge=RIGHT)
                     for y, name in rows.values()])
    cells = {}
    for r, (y, _) in rows.items():
        for c, (x, _, _) in cols.items():
            v = external.loc[r, c]
            box = RoundedRectangle(width=3.2, height=1.6, corner_radius=0.12, stroke_color=GRID, stroke_width=4
                                   ).move_to([x, y, 0])
            text = label(f"{v:.3f}" if c == "substrate" or v < 0.1 else f"{v:.2f}", 56, INK, weight=BOLD).move_to(box)
            cells[(r, c)] = VGroup(box, text)
    head = label("agreement with something the clustering never saw", 30, SUBDUED).to_edge(UP, buff=0.2)
    return heads, names, cells, head


class Scene43(VideoScene):
    number = 43

    def construct(self):
        heads, names, cells, head = external_layout(self)
        key = cells[("all stations", "substrate")]
        # "Third: does it match something the method never saw?"
        self.play(FadeIn(head), FadeIn(heads), run_time=self.share(0.3))
        # "The whole-survey split matches the seabed type at 0.920."
        self.wait(max(self.share(0.45) - self.time, 0.01))
        self.play(FadeIn(names[0]), FadeIn(cells[("all stations", "substrate")]),
                  FadeIn(cells[("all stations", "depth_band")]), run_time=self.share(0.2))
        self.play(key[0].animate.set_stroke(GREEN, 6), key[1].animate.set_color(GREEN), run_time=self.share(0.15))
        self.finish()


class Scene44(VideoScene):
    number = 44

    def construct(self):
        heads, names, cells, head = external_layout(self)
        key = cells[("all stations", "substrate")]
        key[0].set_stroke(GREEN, 6)
        key[1].set_color(GREEN)
        self.add(head, heads, names[0], cells[("all stations", "substrate")], cells[("all stations", "depth_band")])
        soft = cells[("soft stations only", "depth_band")]
        groups = label("evidence of groups", 30, GREEN, weight=BOLD).next_to(soft, DOWN, 0.35).set_x(heads[0].get_x())
        gradient = label("only ever a gradient", 30, ORANGE, weight=BOLD).next_to(soft, DOWN, 0.35)
        # "The soft-bottom split matches depth bands at 0.40, as any cut through a slope would."
        self.play(FadeIn(names[1]), FadeIn(soft), FadeIn(cells[("soft stations only", "substrate")]),
                  run_time=self.share(0.2))
        self.play(soft[0].animate.set_stroke(ORANGE, 6), soft[1].animate.set_color(ORANGE), run_time=self.share(0.15))
        # "Matching a category is evidence of groups."
        self.wait(max(self.share(0.5) - self.time, 0.01))
        self.play(FadeIn(groups), run_time=self.share(0.15))
        # "Matching a measurement cut into bands is not."
        self.wait(max(self.share(0.75) - self.time, 0.01))
        self.play(FadeIn(gradient), run_time=self.share(0.15))
        self.finish()


class Scene45(VideoScene):
    number = 45

    def construct(self):
        head = label("A gradient is a finding too", 44, INK, weight=BOLD).to_edge(UP, buff=1.2)
        quote = label("\"Composition turns over\ncontinuously with depth.\"", 48, BLUE, weight=BOLD)
        card = VGroup(SurroundingRectangle(quote, color=BLUE, buff=0.5, corner_radius=0.2), quote).move_to(0.3 * DOWN)
        honest = label("the honest sentence for this survey", 30, SUBDUED).next_to(card, DOWN, 0.4)
        # "And a gradient is a finding too."
        self.play(FadeIn(head), run_time=self.share(0.25))
        # "\"Composition turns over with depth\" is the honest sentence here."
        self.play(FadeIn(card, scale=0.95), run_time=self.share(0.3))
        self.play(FadeIn(honest), run_time=self.share(0.15))
        self.finish()


class Scene46(KeyPointScene):
    number, point = 46, 3


# Quiz (scenes 47–48) -----------------------------------------------------------------------

class Scene47(QuizScene):
    number = 47
    question = ("In a UMAP picture, two islands sit", "twice as far apart as two others.",
                "Are they twice as different?")


class Scene48(VideoScene):
    number = 48

    def construct(self):
        # Schematic: three islands, each point joined to its nearest neighbours. Moving the
        # islands apart changes nothing UMAP was asked to keep.
        rng = np.random.default_rng(50)
        centres = [np.array([-4.0, -0.6]), np.array([-1.6, -0.6]), np.array([3.6, -0.6])]
        islands = VGroup()
        for c, colour in zip(centres, (BLUE, ORANGE, GREEN)):
            pts = c + rng.normal(0, 0.45, (14, 2))
            dots = VGroup(*[Dot([x, y, 0], radius=0.08, color=colour) for x, y in pts])
            links = VGroup()
            for i, p in enumerate(pts):
                d = ((pts - p) ** 2).sum(1)
                for j in np.argsort(d)[1:3]:
                    links.add(Line([*p, 0], [*pts[j], 0], color=colour, stroke_width=2, stroke_opacity=0.6))
            islands.add(VGroup(links, dots))
        answer = label("No", 56, VERMILION, weight=BOLD).to_edge(UP, buff=0.6)
        kept = label("kept: each station's nearest neighbours", 32, INK, weight=BOLD).next_to(answer, DOWN, 0.3)
        free = label("the space between islands means nothing", 32, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.6)
        # "No. UMAP keeps each station's nearest neighbours."
        self.play(FadeIn(answer), FadeIn(islands), run_time=self.share(0.25))
        self.play(FadeIn(kept), *[Indicate(i[0], color=None) for i in islands], run_time=self.share(0.2))
        # "The space between the islands means nothing."
        self.play(islands[0].animate.shift(1.2 * RIGHT), islands[1].animate.shift(2.8 * RIGHT),
                  islands[2].animate.shift(1.8 * RIGHT), FadeIn(free),
                  run_time=self.share(0.3))
        self.finish()


# The recap (scenes 49–51) and the end card (scene 52) --------------------------------------

class Scene49(RecapScene):
    number, point = 49, 1


class Scene50(RecapScene):
    number, point = 50, 2


class Scene51(RecapScene):
    number, point = 51, 3


class Scene52(EndCardScene):
    number = 52
