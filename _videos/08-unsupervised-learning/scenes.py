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


PROMISES = ["How clustering finds groups without labels",
            "How PCA turns many columns into one map",
            "How to check a pattern before reporting it"]
ANSWERS = ["Compare the groups\nwith the same data,\nshuffled",
           "Read the axes from\ntheir loadings; keep\nwhat the use needs",
           "Does it come back?\nIs there a gap?\nDoes it match a record?"]
RECAP = ["Clustering: compare with shuffled data",
         "PCA: read the axes from their loadings",
         "Check a pattern before reporting it"]

HARD, SOFT = ORANGE, BLUE     # hard and soft bottom, in every scene


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
    """Axes with tick labels and names, in the series style; returns the axes and all of it.

    Ranges must start at zero or the axes cross mid-chart (Manim draws each axis through
    the other's zero); every chart here does.
    """
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


def wait_until(scene, fraction):
    """Hold until this share of the narration, where the next words are spoken."""
    scene.wait(max(scene.share(fraction) - scene.time, 0.01))


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
    """A station: a dot for hard bottom, a small triangle for soft, as on the pages."""
    if hard:
        return Dot(point, radius=size, color=colour, fill_opacity=0.9)
    return Triangle(stroke_width=0, fill_color=colour, fill_opacity=0.9).scale(size * 1.5).move_to(point)


def kmeans(points, centres, steps=20):
    """Plain k-means on schematic points: returns each point's group."""
    for _ in range(steps):
        nearest = np.argmin(((points[:, None, :] - centres[None]) ** 2).sum(-1), axis=1)
        centres = np.array([points[nearest == j].mean(0) for j in range(len(centres))])
    return nearest


# Opening (scenes 2 and 3) -----------------------------------------------------------------

def cell_grid(rows, cols, size, seed, colour=BLUE):
    rng = np.random.default_rng(seed)
    cells = VGroup(*[Square(size, stroke_width=0, fill_color=colour,
                            fill_opacity=float(rng.choice([0.08, 0.3, 0.6, 0.9], p=[0.5, 0.2, 0.2, 0.1])))
                     for _ in range(rows * cols)])
    return cells.arrange_in_grid(rows, cols, buff=0.04)


class Scene02(VideoScene):
    number = 2

    def construct(self):
        # Schematic: a table of counts, shaded by size, and an answer column left empty.
        cells = cell_grid(14, 18, 0.22, 2).move_to([-1.2, -0.4, 0])
        top = label("animals counted at each station", 30, BLUE, weight=BOLD).next_to(cells, UP, 0.3).align_to(cells, LEFT)
        answer = DashedVMobject(Rectangle(width=1.3, height=cells.height, color=GREY, stroke_width=3),
                                num_dashes=50).next_to(cells, RIGHT, 0.4)
        answer_name = label("habitat", 30, VERMILION, weight=BOLD).next_to(answer, DOWN, 0.2)
        marks = VGroup(*[label("?", 30, VERMILION, weight=BOLD).move_to([answer.get_x(), y, 0])
                         for y in np.linspace(answer.get_top()[1] - 0.5, answer.get_bottom()[1] + 0.5, 6)])
        idea = label("structure from the data itself", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.35)
        # "Many marine datasets have no answer column. A benthic survey counts the animals ..."
        self.play(FadeIn(cells, lag_ratio=0.002), FadeIn(top), run_time=self.share(0.3))
        # "... but nobody has said which habitat each station belongs to."
        wait_until(self, 0.42)
        self.play(Create(answer), FadeIn(answer_name), run_time=self.share(0.12))
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2), run_time=self.share(0.15))
        # "Unsupervised learning finds structure in the data itself."
        wait_until(self, 0.75)
        self.play(FadeIn(idea, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        matrix = self.data("matrix")
        cols = list(matrix.columns)
        w, h = 1.05, 0.62
        x0, y0 = -3.7, 1.7
        heads = VGroup(*[label(c, 28, BLUE, weight=BOLD).move_to([x0 + i * w, y0, 0]) for i, c in enumerate(cols)])
        heads.add(label("…  tax24", 28, BLUE, weight=BOLD).move_to([x0 + len(cols) * w + 0.35, y0, 0]))
        rows = VGroup()
        for r, (_, row) in enumerate(matrix.iterrows()):
            y = y0 - (r + 1) * h
            cells = VGroup(*[label(f"{int(v)}", 30).move_to([x0 + i * w, y, 0]) for i, v in enumerate(row)])
            cells.add(label("…", 30, SUBDUED).move_to([x0 + len(cols) * w, y, 0]))
            rows.add(cells)
        more = label("⋮", 34, SUBDUED).move_to([x0 + 3 * w, y0 - (len(matrix) + 1) * h, 0])
        table = VGroup(heads, rows, more)
        brace = Brace(VGroup(rows, more), LEFT, color=SUBDUED)
        n_rows = label("800\nstations", 30, SUBDUED, weight=BOLD).next_to(brace, LEFT, 0.2)
        top = Brace(heads, UP, color=SUBDUED)
        n_cols = label("24 taxa", 30, SUBDUED, weight=BOLD).next_to(top, UP, 0.1)
        name = label("a community matrix", 40, INK, weight=BOLD).to_edge(DOWN, buff=0.4)
        # "Here, each of the course's 800 simulated survey stations ..."
        self.play(FadeIn(heads), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), FadeIn(more),
                  run_time=self.share(0.3))
        self.play(GrowFromCenter(brace), FadeIn(n_rows), run_time=self.share(0.1))
        # "... has counts of 24 taxa."
        self.play(GrowFromCenter(top), FadeIn(n_cols), run_time=self.share(0.12))
        # "One row per station, one column per taxon: ecologists call this a community matrix."
        wait_until(self, 0.72)
        self.play(FadeIn(name, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


# Clustering (scenes 4–12) ----------------------------------------------------------------

class Scene04(VideoScene):
    number = 4

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
        head = label("k-means, with k = 2", 34, SUBDUED).to_edge(UP, buff=0.3)
        # "Clustering sorts stations into groups of similar stations."
        self.play(FadeIn(dots, lag_ratio=0.02), run_time=self.share(0.15))
        # "The most widely used method is k-means. You choose the number of groups, k."
        wait_until(self, 0.25)
        self.play(FadeIn(head), run_time=self.share(0.08))
        wait_until(self, 0.4)
        self.play(FadeIn(stars, scale=2), run_time=self.share(0.08))
        # "Each station joins its nearest centre, each centre moves to the average ..."
        steps = 4
        for _ in range(steps):
            nearest = np.argmin(((points[:, None, :] - centres[None]) ** 2).sum(-1), axis=1)
            self.play(*[d.animate.set_color(colours[n]) for d, n in zip(dots, nearest)],
                      run_time=self.share(0.45 / (2 * steps)))
            centres = np.array([points[nearest == j].mean(0) for j in range(2)])
            self.play(*[s.animate.move_to([*p, 0]) for s, p in zip(stars, centres)],
                      run_time=self.share(0.45 / (2 * steps)))
        self.finish()


def waffle(n_first, n_second, colour_first, colour_second, cols, size=0.17, gap=0.045):
    """n_first + n_second squares in rows of `cols`: the second kind last, at the bottom."""
    squares = VGroup(*[Square(size, stroke_width=0, fill_color=colour_first, fill_opacity=1)
                       for _ in range(n_first)],
                     *[Square(size, stroke_width=0, fill_color=colour_second, fill_opacity=1)
                       for _ in range(n_second)])
    rows = int(np.ceil(len(squares) / cols))
    for i, s in enumerate(squares):
        s.move_to([(i % cols) * (size + gap), -(i // cols) * (size + gap), 0])
    return squares, rows


class Scene05(VideoScene):
    number = 5

    def construct(self):
        seabed = self.data("seabed").pivot(index="cluster", columns="bottom", values="n")
        hard_c = seabed["hard"].idxmax()
        soft_c = [c for c in seabed.index if c != hard_c][0]
        # Each cluster's own kind first, the stations of the other kind last.
        hard_sq, _ = waffle(seabed.loc[hard_c, "hard"], seabed.loc[hard_c, "soft"], HARD, SOFT, 12)
        soft_sq, _ = waffle(seabed.loc[soft_c, "soft"], seabed.loc[soft_c, "hard"], SOFT, HARD, 30)
        hard_sq.move_to([-4.3, -0.55, 0]).align_to(soft_sq, UP)
        soft_sq.move_to([1.9, -0.55, 0])
        hard_sq.align_to(soft_sq, UP)
        grey = VGroup(*[s.copy().set_fill(GREY) for s in [*hard_sq, *soft_sq]])
        names = VGroup(label(f"cluster 1: {seabed.loc[hard_c].sum()} stations", 30, INK, weight=BOLD
                             ).next_to(hard_sq, UP, 0.3),
                       label(f"cluster 2: {seabed.loc[soft_c].sum()} stations", 30, INK, weight=BOLD
                             ).next_to(soft_sq, UP, 0.3))
        key = VGroup(VGroup(Square(0.25, stroke_width=0, fill_color=HARD, fill_opacity=1),
                            label("hard bottom: rock, gravel", 28, SUBDUED)).arrange(RIGHT, buff=0.2),
                     VGroup(Square(0.25, stroke_width=0, fill_color=SOFT, fill_opacity=1),
                            label("soft bottom: sand, mud", 28, SUBDUED)).arrange(RIGHT, buff=0.2)
                     ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.3)
        out_hard = hard_sq[seabed.loc[hard_c, "hard"]:]
        out_soft = soft_sq[seabed.loc[soft_c, "soft"]:]
        out = VGroup(*out_hard, *out_soft)
        rings = VGroup(*[Circle(0.16, color=VERMILION, stroke_width=4).move_to(s) for s in out])
        n_out = len(out)
        note = label(f"{n_out} of {int(seabed.values.sum())} in the other kind's cluster", 32, VERMILION,
                     weight=BOLD).to_edge(UP, buff=0.25)
        # "k-means was given only the counts, logged and on a common scale, and asked for two groups."
        self.play(FadeIn(grey, lag_ratio=0.001), FadeIn(names), run_time=self.share(0.3))
        # "One cluster is the hard bottom, rock and gravel; the other, the soft bottom."
        wait_until(self, 0.4)
        self.play(*[Transform(g, s) for g, s in zip(grey, [*hard_sq, *soft_sq])], FadeIn(key),
                  run_time=self.share(0.2))
        # "Only 15 of the 800 stations sit in the other kind's cluster."
        wait_until(self, 0.72)
        self.play(Create(rings), FadeIn(note), run_time=self.share(0.15))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        # Schematic: random points in a square, cut into four groups by k-means.
        rng = np.random.default_rng(66)
        points = rng.uniform(-2.6, 2.6, (160, 2))
        groups = kmeans(points, points[:4].copy())
        colours = [BLUE, ORANGE, GREEN, PURPLE]
        centre = np.array([-2.6, -0.3, 0])
        frame = Square(5.6, color=GRID, stroke_width=3).move_to(centre)
        dots = VGroup(*[Dot(centre + np.array([x, y, 0]), radius=0.06, color=GREY) for x, y in points])
        name = label("random numbers", 30, SUBDUED).next_to(frame, UP, 0.25)
        ask = label("asked for four groups", 36, INK, weight=BOLD).move_to([3.6, 1.0, 0])
        get = label("four tidy groups", 36, BLUE, weight=BOLD).move_to([3.6, -0.2, 0])
        question = label("so how many are real?", 36, VERMILION, weight=BOLD).move_to([3.6, -1.6, 0])
        # "But k-means returns as many groups as you ask for, even from random numbers."
        self.play(Create(frame), FadeIn(dots, lag_ratio=0.005), FadeIn(name), FadeIn(ask),
                  run_time=self.share(0.3))
        self.play(*[d.animate.set_color(colours[g]) for d, g in zip(dots, groups)], FadeIn(get),
                  run_time=self.share(0.2))
        # "So how many groups does the survey really hold?"
        wait_until(self, 0.62)
        self.play(FadeIn(question, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        # Schematic: two groups, one station, and its distances to each.
        rng = np.random.default_rng(8)
        own = rng.normal([-2.0, -0.4], 0.55, (12, 2))
        other = rng.normal([2.4, -0.2], 0.55, (12, 2))
        station = np.array([-1.3, -0.1])
        own_dots = VGroup(*[Dot([x, y, 0], radius=0.09, color=BLUE) for x, y in own])
        other_dots = VGroup(*[Dot([x, y, 0], radius=0.09, color=ORANGE) for x, y in other])
        star = Dot([*station, 0], radius=0.15, color=INK)
        near = VGroup(*[Line([*station, 0], [x, y, 0], color=BLUE, stroke_width=2.5) for x, y in own])
        far = VGroup(*[Line([*station, 0], [x, y, 0], color=ORANGE, stroke_width=2.5) for x, y in other])
        a = label("own cluster: close", 32, BLUE, weight=BOLD).move_to([-2.0, 1.6, 0])
        b = label("nearest other cluster: far", 32, ORANGE, weight=BOLD).move_to([2.4, 1.6, 0])
        rule = label("silhouette width: near 1 when its own cluster is far closer", 28, INK, weight=BOLD
                     ).to_edge(DOWN, buff=0.6)
        average = label("averaged over every station: higher is better separated", 28, SUBDUED
                        ).next_to(rule, DOWN, 0.2)
        # "The silhouette width compares each station's distance to its own cluster ..."
        self.play(FadeIn(own_dots), FadeIn(other_dots), FadeIn(star, scale=2), run_time=self.share(0.15))
        self.play(Create(near), FadeIn(a), run_time=self.share(0.2))
        # "... with its distance to the nearest other one."
        self.play(Create(far), FadeIn(b), run_time=self.share(0.2))
        self.play(FadeIn(rule), run_time=self.share(0.1))
        # "Averaged over the stations, higher means better separated groups."
        wait_until(self, 0.68)
        self.play(FadeIn(average), run_time=self.share(0.12))
        self.finish()


def silhouette_layout(scene):
    sil = scene.data("silhouette").sort_values("k")
    axes, frame = chart([0, 8.5, 1], [0, 0.3, 0.05], 9.0, 4.8, range(2, 9), [0, 0.1, 0.2, 0.3],
                        "number of clusters (k)", "average silhouette width", y_fmt="{:.1f}")
    # The chart starts at zero (see chart()); hide the empty stretch below k = 2.
    VGroup(frame).move_to([0.4, -0.4, 0])

    def curve(column, colour):
        line = polyline(axes, sil["k"], sil[column], colour)
        dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.1, color=colour) for a, b in zip(sil["k"], sil[column])])
        return VGroup(line, dots)

    obs, base = curve("silhouette", BLUE), curve("silhouette_mean", GREY)
    band = Polygon(*[axes.c2p(k, v) for k, v in zip(sil["k"], sil["silhouette_high"])],
                   *[axes.c2p(k, v) for k, v in zip(sil["k"][::-1], sil["silhouette_low"][::-1])],
                   stroke_width=0, fill_color=GREY, fill_opacity=0.25)
    two = sil[sil["k"] == 2].iloc[0]
    peak_name = label(f"{two['silhouette']:.3f}", 32, BLUE, weight=BOLD).next_to(obs[1][0], UR, 0.15)
    rule = DashedLine(axes.c2p(2, 0.25), axes.c2p(8, 0.25), color=VERMILION, stroke_width=4)
    rule_name = label("rule of thumb: below 0.25, \"no substantial structure\"", 28, VERMILION
                      ).next_to(rule, UP, 0.12).align_to(rule, RIGHT)
    return sil, axes, frame, obs, base, band, peak_name, VGroup(rule, rule_name), two


def axis_mask(axes, frame, upto):
    """A white strip over the x axis from zero to `upto`, so a chart can start at k = 2."""
    left, right = axes.c2p(0, 0), axes.c2p(upto, 0)
    return Rectangle(width=right[0] - left[0] + 0.05, height=0.12, stroke_width=0, fill_color=BACKGROUND,
                     fill_opacity=1).move_to((left + right) / 2)


class Scene08(VideoScene):
    number = 8

    def construct(self):
        sil, axes, frame, obs, _, _, peak_name, rule, _ = silhouette_layout(self)
        mask = axis_mask(axes, frame, 1.6)
        # "Across two to eight clusters, the silhouette is highest at two, at 0.179."
        self.play(FadeIn(frame), FadeIn(mask), run_time=self.share(0.1))
        self.play(Create(obs[0]), FadeIn(obs[1], lag_ratio=0.2), run_time=self.share(0.3))
        self.play(FadeIn(peak_name), Indicate(obs[1][0], scale_factor=1.6), run_time=self.share(0.15))
        # "That sounds low: a popular rule of thumb calls it no real structure."
        wait_until(self, 0.6)
        self.play(Create(rule[0]), FadeIn(rule[1]), run_time=self.share(0.2))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        # Schematic: six rows and five columns; rows 1–3 hold the first three taxa
        # together, rows 4–6 the last two. Shuffling each column breaks that.
        rows, cols = 6, 5
        high = [[(r < 3) == (c < 3) for c in range(cols)] for r in range(rows)]
        size, gap = 0.8, 0.12
        x0, y0 = -((cols - 1) * (size + gap)) / 2 - 2.6, ((rows - 1) * (size + gap)) / 2 - 0.2
        cells = [[Square(size, stroke_width=0, fill_color=BLUE, fill_opacity=0.9 if high[r][c] else 0.15
                         ).move_to([x0 + c * (size + gap), y0 - r * (size + gap), 0])
                  for c in range(cols)] for r in range(rows)]
        grid = VGroup(*[s for row in cells for s in row])
        head = label("stations × taxa", 30, SUBDUED).next_to(grid, UP, 0.3)
        keeps = label("each column keeps its values", 32, INK, weight=BOLD).move_to([3.4, 0.6, 0])
        gone = label("any groups: gone", 32, VERMILION, weight=BOLD).move_to([3.4, -0.6, 0])
        # "So run the same clustering on a shuffled copy."
        self.play(FadeIn(grid, lag_ratio=0.02), FadeIn(head), run_time=self.share(0.2))
        # "Shuffle each taxon's counts across the stations: ..."
        wait_until(self, 0.3)
        rng = np.random.default_rng(18)
        moves = []
        for c in range(cols):
            order = rng.permutation(rows)
            while (order == np.arange(rows)).all():
                order = rng.permutation(rows)
            for r in range(rows):
                moves.append(cells[r][c].animate.move_to(cells[order[r]][c].get_center()))
        self.play(*moves, run_time=self.share(0.25))
        # "... every column keeps its values, but any groups are gone."
        wait_until(self, 0.62)
        self.play(FadeIn(keeps), run_time=self.share(0.1))
        self.play(FadeIn(gone), run_time=self.share(0.1))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        sil, axes, frame, obs, base, band, peak_name, rule, two = silhouette_layout(self)
        mask = axis_mask(axes, frame, 1.6)
        self.add(frame, mask, obs, peak_name, rule)
        base_name = label("shuffled counts: about 0.05", 30, SUBDUED, weight=BOLD
                          ).next_to(axes.c2p(5, 0.03), DOWN, 0.05)
        top, bottom = axes.c2p(2, two["silhouette"]), axes.c2p(2, two["silhouette_mean"])
        bracket = VGroup(Line(bottom + 0.35 * LEFT, top + 0.35 * LEFT, color=BLUE, stroke_width=5),
                         Line(bottom + 0.45 * LEFT, bottom + 0.25 * LEFT, color=BLUE, stroke_width=5),
                         Line(top + 0.45 * LEFT, top + 0.25 * LEFT, color=BLUE, stroke_width=5))
        times = label(f"{two['times']:.1f} times\nthe baseline", 32, BLUE, weight=BOLD
                      ).move_to(axes.c2p(4.6, 0.22), aligned_edge=LEFT)
        # "On shuffled counts, the silhouette stays near 0.05 for every number of clusters."
        self.play(FadeOut(rule), FadeIn(band), Create(base[0]), FadeIn(base[1], lag_ratio=0.2),
                  run_time=self.share(0.3))
        self.play(FadeIn(base_name), run_time=self.share(0.1))
        # "At two, the survey scores three and a half times that, the clearest lead of any."
        wait_until(self, 0.52)
        self.play(Create(bracket), FadeIn(times), run_time=self.share(0.2))
        self.finish()


# A schematic tree: ten leaves joined pair by pair. Each join is (left, right, height);
# nodes 10 onwards are the joins in order.
LEAVES = 10
JOINS = [(0, 1, 0.6), (5, 6, 0.5), (2, 3, 0.8), (7, 8, 0.7), (4, 11, 1.2), (13, 9, 1.4),
         (10, 12, 1.6), (14, 15, 2.4), (16, 17, 3.6)]


def tree_layout():
    base, unit = -2.3, 1.15
    x = {i: -4.5 + i for i in range(LEAVES)}
    y = {i: base for i in range(LEAVES)}
    links = []
    for n, (a, b, h) in enumerate(JOINS, start=LEAVES):
        x[n], y[n] = (x[a] + x[b]) / 2, base + h * unit
        links.append(VMobject(color=INK, stroke_width=5).set_points_as_corners(
            [[x[a], y[a], 0], [x[a], y[n], 0], [x[b], y[n], 0], [x[b], y[b], 0]]))
    leaves = VGroup(*[Dot([x[i], base, 0], radius=0.14, color=GREY) for i in range(LEAVES)])
    return leaves, links, (lambda h: base + h * unit)


def leaves_under(node):
    if node < LEAVES:
        return [node]
    a, b, _ = JOINS[node - LEAVES]
    return leaves_under(a) + leaves_under(b)


class Scene11(VideoScene):
    number = 11

    def construct(self):
        leaves, links, height = tree_layout()
        name = label("a dendrogram", 36, INK, weight=BOLD).to_edge(UP, buff=0.35)
        # "Hierarchical clustering gives every number of groups at once. It joins the two
        # closest groups again and again, ..."
        self.play(FadeIn(leaves, lag_ratio=0.1), run_time=self.share(0.1))
        for link in links:
            self.play(Create(link), run_time=self.share(0.4 / len(links)))
        # "... and records the joins as a tree, a dendrogram."
        self.play(FadeIn(name), run_time=self.share(0.08))
        # "Cut it high for a few groups, lower for more."
        wait_until(self, 0.66)
        cut = DashedLine([-5.2, height(3.0), 0], [5.2, height(3.0), 0], color=VERMILION, stroke_width=5)
        colours = [BLUE, ORANGE, GREEN]
        self.play(Create(cut), *[leaves[i].animate.set_color(colours[g])
                                 for g, node in enumerate((16, 17)) for i in leaves_under(node)],
                  run_time=self.share(0.12))
        self.play(cut.animate.set_y(height(2.0)),
                  *[leaves[i].animate.set_color(colours[g])
                    for g, node in enumerate((16, 14, 15)) for i in leaves_under(node)],
                  run_time=self.share(0.12))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        linkages = self.data("linkages")
        axes, frame = chart([0, 6.5, 1], [0, 1, 0.25], 8.4, 4.6, range(2, 7), [0, 0.25, 0.5, 0.75, 1],
                            "number of groups", "share of stations in the largest group", y_fmt="{:.0%}")
        VGroup(frame).move_to([-0.9, -0.5, 0])
        mask = axis_mask(axes, frame, 1.6)
        head = label("One table, two linkages", 32, SUBDUED).to_edge(UP, buff=0.3)
        lines = {}
        for key, name, colour in (("Ward", "Ward", BLUE), ("single", "single", VERMILION)):
            rows = linkages[linkages["linkage"] == key].sort_values("k")
            line = polyline(axes, rows["k"], rows["largest_share"], colour)
            dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.09, color=colour)
                            for a, b in zip(rows["k"], rows["largest_share"])])
            lines[key] = VGroup(line, dots)
        single = linkages[linkages["linkage"] == "single"]["largest_share"].min()
        ward_note = label("Ward: nearly k-means' two groups", 30, BLUE, weight=BOLD
                          ).move_to(axes.c2p(2.2, 0.1), aligned_edge=LEFT)
        chain_note = label(f"single: more than {np.floor(100 * single):.0f}% in one group", 30, VERMILION,
                           weight=BOLD).move_to(axes.c2p(2.2, 0.88), aligned_edge=LEFT)
        # "How the tree measures the distance between groups, its linkage, decides what it finds."
        self.play(FadeIn(head), FadeIn(frame), FadeIn(mask), run_time=self.share(0.2))
        # "Ward's linkage finds nearly the same two groups as k-means."
        wait_until(self, 0.4)
        self.play(Create(lines["Ward"][0]), FadeIn(lines["Ward"][1:]), FadeIn(ward_note),
                  run_time=self.share(0.2))
        # "Single linkage chains more than 99 per cent of stations into one group."
        wait_until(self, 0.7)
        self.play(Create(lines["single"][0]), FadeIn(lines["single"][1:]), FadeIn(chain_note),
                  run_time=self.share(0.2))
        self.finish()


class Scene13(KeyPointScene):
    number, point = 13, 1


# PCA (scenes 14–20) ----------------------------------------------------------------------

class Scene14(VideoScene):
    number = 14

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
        many = label("24 columns: no single picture", 34, SUBDUED).to_edge(UP, buff=0.3)
        head = label("Principal component analysis (PCA)", 34, INK, weight=BOLD).to_edge(UP, buff=0.3)
        names = VGroup(label("PC1: most spread", 30, BLUE, weight=BOLD),
                       label("PC2: next, at right angles", 30, BLUE, weight=BOLD))
        # "Twenty-four columns cannot be drawn in one picture."
        self.play(FadeIn(many), run_time=self.share(0.1))
        # "Principal component analysis, or PCA, finds the direction along which the stations
        # spread out most: ..."
        wait_until(self, 0.2)
        self.play(FadeIn(dots, lag_ratio=0.02), FadeIn(old), FadeOut(many), FadeIn(head), run_time=self.share(0.15))
        self.play(Rotate(new, angle, about_point=centre), run_time=self.share(0.25))
        names[0].next_to(new[0].get_end(), UP, 0.1).shift(1.2 * LEFT)
        self.play(FadeIn(names[0]), run_time=self.share(0.08))
        # "The second is the next most, at right angles."
        wait_until(self, 0.78)
        names[1].next_to(new[1].get_end(), LEFT, 0.15)
        self.play(FadeIn(names[1]), Indicate(new[1], color=BLUE), run_time=self.share(0.12))
        self.finish()


def ordination_layout(scene):
    stations = scene.data("ordination")
    hard = stations["hard_bottom"].astype(str).str.upper() == "TRUE"
    x_lo, x_hi = np.floor(stations["PC1"].min()), np.ceil(stations["PC1"].max())
    y_lo, y_hi = np.floor(stations["PC2"].min()), np.ceil(stations["PC2"].max())
    height = 6.0
    width = min(height * (x_hi - x_lo) / (y_hi - y_lo), 8.4)
    axes = plain_axes([x_lo, x_hi, 1], [y_lo, y_hi, 1], width, height).move_to([-1.6, -0.35, 0])
    axes.set_stroke(opacity=0.5, width=2)       # faint lines through zero; the box is the frame
    box = Rectangle(width=width, height=height, color=GRID, stroke_width=3).move_to(
        (axes.c2p(x_lo, y_lo) + axes.c2p(x_hi, y_hi)) / 2)
    lo, hi = stations["depth_m"].min(), stations["depth_m"].max()
    dots = VGroup(*[marker(axes.c2p(a, b), viridis((d - lo) / (hi - lo)), h, 0.06)
                    for a, b, d, h in zip(stations["PC1"], stations["PC2"], stations["depth_m"], hard)])
    x_name = label("PC1", 28, SUBDUED).next_to(box, DOWN, 0.15)
    y_name = label("PC2", 28, SUBDUED).rotate(PI / 2).next_to(box, LEFT, 0.15)
    key = VGroup(depth_key(2.2),
                 VGroup(marker(ORIGIN, INK, True, 0.1), label("hard bottom", 26, SUBDUED)).arrange(RIGHT, buff=0.2),
                 VGroup(marker(ORIGIN, INK, False, 0.1), label("soft bottom", 26, SUBDUED)).arrange(RIGHT, buff=0.2)
                 ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_corner(UR, buff=0.4)
    return axes, dots, VGroup(axes, box, x_name, y_name), key


SIDE_X = 4.7    # right of the map, under the key: where the map's notes go


class Scene15(VideoScene):
    number = 15

    def construct(self):
        axes, dots, frame, key = ordination_layout(self)
        variance = self.data("variance")
        two = variance["cumulative percent variance"].iloc[1]
        name = label("an ordination", 34, INK, weight=BOLD).move_to([SIDE_X, 0.2, 0])
        held = label(f"PC1 and PC2:\n{two:.1f}% of\nthe variance", 32, BLUE, weight=BOLD).move_to([SIDE_X, -1.6, 0])
        # "Plotted on those two, the stations form a map, an ordination, ..."
        self.play(FadeIn(frame), FadeIn(key), run_time=self.share(0.12))
        self.play(FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.3))
        self.play(FadeIn(name), run_time=self.share(0.08))
        # "The two components hold 29.4 per cent of the variance, usual for species counts."
        wait_until(self, 0.62)
        self.play(FadeIn(held), run_time=self.share(0.15))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        taxa = self.data("loadings")
        lim = np.ceil(10 * max(taxa["PC1"].abs().max(), taxa["PC2"].abs().max())) / 10
        size = 5.6
        axes = plain_axes([-lim, lim, 0.1], [-lim, lim, 0.1], size, size).move_to([-1.6, -0.4, 0])
        axes.set_stroke(opacity=0.6, width=2)
        box = Square(size, color=GRID, stroke_width=3).move_to(axes)
        names = VGroup(label("loading on PC1", 26, SUBDUED).next_to(box, DOWN, 0.15),
                       label("loading on PC2", 26, SUBDUED).rotate(PI / 2).next_to(box, LEFT, 0.15))
        hard = taxa[taxa["hard_share"] > 0.5]
        soft = taxa[taxa["hard_share"] <= 0.5].sort_values("mean_depth")
        lo, hi = soft["mean_depth"].min(), soft["mean_depth"].max()
        hard_dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.13, color=HARD) for a, b in zip(hard["PC1"], hard["PC2"])])
        soft_dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.13, color=viridis((d - lo) / (hi - lo)))
                             for a, b, d in zip(soft["PC1"], soft["PC2"], soft["mean_depth"])])
        head = label("Each taxon placed at its loadings", 32, SUBDUED).to_edge(UP, buff=0.3)
        hard_name = label("hard-bottom taxa", 32, HARD, weight=BOLD).move_to([SIDE_X, 1.2, 0])
        soft_name = label("the rest, in order\nof depth", 32, INK, weight=BOLD).move_to([SIDE_X, -0.6, 0])
        key = depth_key(2.0, "shallow", "deep").next_to(soft_name, DOWN, 0.3)
        # "To read the axes, look at the loadings: the weight of each taxon in a component."
        self.play(FadeIn(head), FadeIn(VGroup(axes, box, names)), run_time=self.share(0.15))
        self.play(FadeIn(VGroup(*[d.copy().set_color(GREY) for d in [*hard_dots, *soft_dots]]), lag_ratio=0.05),
                  run_time=self.share(0.25))
        # "The hard-bottom taxa sit together, ..."
        wait_until(self, 0.5)
        self.play(FadeIn(hard_dots, scale=1.4), FadeIn(hard_name), run_time=self.share(0.15))
        # "... and the rest line up in order of depth."
        wait_until(self, 0.7)
        self.play(FadeIn(soft_dots), FadeIn(soft_name), FadeIn(key), run_time=self.share(0.2))
        self.finish()


def direction_arrows(scene, axes):
    directions = scene.data("directions").set_index("variable")
    arrows = VGroup()
    origin = axes.c2p(0, 0)
    for name in ("depth", "hard bottom"):
        r = directions.loc[name]
        unit = np.array([r["PC1"], r["PC2"]]) / np.hypot(r["PC1"], r["PC2"])
        tip = axes.c2p(*(3.6 * unit))
        off = abs(r["angle_from_PC1"]) % 90
        off = min(off, 90 - off)
        arrow = Arrow(origin, tip, buff=0, color=VERMILION, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        text = label(f"{name}: {off:.0f}°", 32, VERMILION, weight=BOLD).next_to(tip, UP if unit[1] > 0 else DOWN, 0.12)
        arrows.add(VGroup(arrow, text))
    return arrows


class Scene17(VideoScene):
    number = 17

    def construct(self):
        axes, dots, frame, key = ordination_layout(self)
        self.add(frame, key, dots.set_opacity(0.35))
        arrows = direction_arrows(self, axes)
        note = label("degrees from\nthe nearest axis", 26, SUBDUED).move_to([SIDE_X, 0.0, 0])
        verdict = label("each component\nmixes the two", 34, INK, weight=BOLD).move_to([SIDE_X, -1.6, 0])
        # "So depth and seabed both run diagonally, about 39 degrees from the axes: ..."
        self.play(GrowArrow(arrows[0][0]), FadeIn(arrows[0][1]), run_time=self.share(0.2))
        self.play(GrowArrow(arrows[1][0]), FadeIn(arrows[1][1]), FadeIn(note), run_time=self.share(0.2))
        # "... each component mixes the two. Read an axis from its loadings, not from its name."
        wait_until(self, 0.5)
        self.play(FadeIn(verdict), run_time=self.share(0.15))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        shares = self.data("shares").sort_values("component")
        top = np.ceil(shares["observed"].max() / 5) * 5
        axes, frame = chart([0, 25, 1], [0, top, 5], 10.4, 4.4, [1, 4, 8, 12, 16, 20, 24],
                            list(range(0, int(top) + 1, 5)), "component", "share of the variance (%)")
        VGroup(frame).move_to([0.3, -0.7, 0])
        width = axes.x_axis.get_unit_size() * 0.7
        unit = axes.y_axis.get_unit_size()
        bars = VGroup(*[Rectangle(width=width, height=max(unit * p, 0.01), stroke_width=0, fill_color=GREY,
                                  fill_opacity=1).move_to(axes.c2p(c, 0), aligned_edge=DOWN)
                        for c, p in zip(shares["component"], shares["observed"])])
        n_80 = int(shares.loc[shares["cumulative"] >= 80, "component"].iloc[0])
        kept = int(np.cumprod(shares["above"].astype(str).str.upper() == "TRUE").sum())
        line80 = DashedLine(axes.c2p(n_80 + 0.5, 0), axes.c2p(n_80 + 0.5, top), color=SUBDUED, stroke_width=4)
        name80 = label(f"80% of the variance: {n_80} components", 30, SUBDUED, weight=BOLD
                       ).next_to(line80, UP, 0.1).align_to(line80, RIGHT)
        shuffled = polyline(axes, shares["component"], shares["shuffled"], VERMILION, width=5, dashed=True)
        shuffled_name = label("shuffled tables", 28, VERMILION, weight=BOLD).next_to(
            axes.c2p(14, shares["shuffled"].iloc[13]), UP, 0.45)
        pa_name = label(f"parallel analysis: {kept}", 34, BLUE, weight=BOLD).move_to(axes.c2p(5, top * 0.8),
                                                                                    aligned_edge=LEFT)
        # "Components can also be a model's inputs. How many to keep?"
        self.play(FadeIn(frame), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05),
                  run_time=self.share(0.25))
        # "Keeping 80 per cent of the variance keeps 16 of the 24."
        wait_until(self, 0.3)
        self.play(*[bars[i].animate.set_fill(SKY) for i in range(n_80)], Create(line80), FadeIn(name80),
                  run_time=self.share(0.2))
        # "Parallel analysis keeps only those that beat their shuffled counterparts: three."
        wait_until(self, 0.58)
        self.play(Create(shuffled), FadeIn(shuffled_name), *[bars[i].animate.set_fill(GREY) for i in range(n_80)],
                  FadeOut(line80), FadeOut(name80), run_time=self.share(0.2))
        self.play(*[bars[i].animate.set_fill(BLUE) for i in range(kept)], FadeIn(pa_name), run_time=self.share(0.12))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        cv = self.data("components-cv").sort_values("num_comp")
        y_top = np.ceil(cv["mean"].max() / 5) * 5 + 5
        y_ticks = list(range(0, int(y_top) + 1, 10))
        x_top = cv["num_comp"].max()
        axes, frame = chart([0, x_top + 0.5, 1], [0, y_top, 5], 9.6, 4.6, sorted(set([1, 2, 4, 8, x_top])), y_ticks,
                            "components kept", "error predicting depth (m)")
        VGroup(frame).move_to([-0.4, -0.5, 0])
        head = label("Predicting depth from the components", 32, SUBDUED).to_edge(UP, buff=0.3)
        line = polyline(axes, cv["num_comp"], cv["mean"], BLUE)
        dots = VGroup(*[Dot(axes.c2p(a, b), radius=0.09, color=BLUE) for a, b in zip(cv["num_comp"], cv["mean"])])
        two = cv[cv["num_comp"] == 2].iloc[0]
        pointer_text = label("two are enough", 32, BLUE, weight=BOLD).move_to(
            axes.c2p(3.5, two["mean"] + 0.35 * y_top), aligned_edge=LEFT)
        pointer = Arrow(pointer_text.get_left(), axes.c2p(2, two["mean"]), buff=0.15, color=BLUE, stroke_width=4)
        pc3 = label("PC3: rock against gravel,\nnot needed for depth", 28, INK, weight=BOLD).move_to(
            axes.c2p(10, 0.3 * y_top), aligned_edge=LEFT)
        # "When the components feed a model, cross-validate the number."
        self.play(FadeIn(head), FadeIn(frame), run_time=self.share(0.2))
        self.play(Create(line), FadeIn(dots, lag_ratio=0.05), run_time=self.share(0.25))
        # "To predict depth, two are enough."
        self.play(GrowArrow(pointer), FadeIn(pointer_text), run_time=self.share(0.12))
        # "The third holds real structure, rock against gravel, that depth does not need."
        wait_until(self, 0.62)
        self.play(FadeIn(pc3), run_time=self.share(0.15))
        self.finish()


def umap_panel(umap, data, centre, title_text, size=4.8):
    rows = umap[umap["data"] == data]
    xs, ys = rows["UMAP1"], rows["UMAP2"]
    span = max(xs.max() - xs.min(), ys.max() - ys.min())
    to = lambda x, y: np.array([centre[0] + (x - (xs.max() + xs.min()) / 2) / span * size,  # noqa: E731
                                centre[1] + (y - (ys.max() + ys.min()) / 2) / span * size, 0])
    lo, hi = umap["depth_m"].min(), umap["depth_m"].max()
    dots = VGroup(*[marker(to(x, y), viridis((d - lo) / (hi - lo)), s == "Hard bottom", 0.05)
                    for x, y, d, s in zip(xs, ys, rows["depth_m"], rows["seabed"])])
    frame = RoundedRectangle(width=size + 0.6, height=size + 0.6, corner_radius=0.15, stroke_color=GRID,
                             stroke_width=3).move_to([*centre, 0])
    name = label(title_text, 32, INK, weight=BOLD).next_to(frame, UP, 0.2)
    return rows, dots, VGroup(frame, name), to


class Scene20(VideoScene):
    number = 20

    def construct(self):
        umap = self.data("umap")
        rows, dots, frame, to = umap_panel(umap, "Observed", (-3.4, -0.3), "UMAP: observed")
        _, null_dots, null_frame, _ = umap_panel(umap, "Shuffled", (3.4, -0.3), "UMAP: shuffled")
        key = VGroup(depth_key(2.2),
                     VGroup(marker(ORIGIN, INK, True, 0.1), label("hard bottom", 24, SUBDUED)).arrange(RIGHT, buff=0.15),
                     VGroup(marker(ORIGIN, INK, False, 0.1), label("soft bottom", 24, SUBDUED)).arrange(RIGHT, buff=0.15)
                     ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.15)
        # The hard-bottom group: an outline around the middle 90% of its stations.
        hard = rows[rows["seabed"] == "Hard bottom"]
        lo_x, hi_x = (to(hard["UMAP1"].quantile(q), 0)[0] for q in (0.05, 0.95))
        lo_y, hi_y = (to(0, hard["UMAP2"].quantile(q))[1] for q in (0.05, 0.95))
        ring = Ellipse(width=hi_x - lo_x + 0.6, height=hi_y - lo_y + 0.6, color=VERMILION,
                       stroke_width=5).move_to([(lo_x + hi_x) / 2, (lo_y + hi_y) / 2, 0])
        group = label("hard bottom:\na group of its own", 28, VERMILION, weight=BOLD
                      ).next_to(ring, DOWN, 0.2).align_to(ring, LEFT)
        group.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.1)
        one = label("one cloud", 32, VERMILION, weight=BOLD).move_to([3.4, -0.3, 0])
        one.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.15)
        # "UMAP draws a map another way, keeping each station's nearest neighbours close."
        self.play(FadeIn(frame), FadeIn(key), FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.3))
        # "The hard-bottom stations form their own group, with depth running smoothly through each."
        wait_until(self, 0.38)
        self.play(Create(ring), FadeIn(group), run_time=self.share(0.12))
        self.play(Indicate(key[0], color=None), run_time=self.share(0.15))
        # "Shuffled counts give one cloud."
        wait_until(self, 0.78)
        self.play(FadeIn(null_frame), FadeIn(null_dots, lag_ratio=0.001), run_time=self.share(0.15))
        self.play(FadeIn(one), run_time=self.share(0.05))
        self.finish()


class Scene21(KeyPointScene):
    number, point = 21, 2


# Checking a pattern (scenes 22–28) -------------------------------------------------------

CHECKS = ["Does it come back?", "Is there a gap?", "Does it match a record?"]


class Scene22(VideoScene):
    number = 22

    def construct(self):
        sup = VGroup(label("supervised model", 32, INK, weight=BOLD),
                     label("checked against held-out answers", 28, GREEN)).arrange(DOWN, buff=0.15)
        uns = VGroup(label("clustering", 32, INK, weight=BOLD),
                     label("no answers to hold out", 28, VERMILION)).arrange(DOWN, buff=0.15)
        VGroup(sup, uns).arrange(RIGHT, buff=2.0).to_edge(UP, buff=0.8)
        cards = VGroup()
        for i, text in enumerate(CHECKS, 1):
            box = RoundedRectangle(width=4.1, height=1.9, corner_radius=0.15, stroke_color=BLUE, stroke_width=4)
            inner = VGroup(badge(i), label(text, 28, INK, weight=BOLD)).arrange(DOWN, buff=0.25).move_to(box)
            cards.add(VGroup(box, inner))
        cards.arrange(RIGHT, buff=0.35).move_to(1.2 * DOWN)
        # "A supervised model can be checked against held-out answers."
        self.play(FadeIn(sup), run_time=self.share(0.2))
        # "A clustering has none, ..."
        wait_until(self, 0.42)
        self.play(FadeIn(uns), run_time=self.share(0.15))
        # "... so three checks take their place."
        wait_until(self, 0.62)
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cards], lag_ratio=0.3), run_time=self.share(0.3))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        # Schematic: eight sites, each a box of stations, drawn again with replacement.
        letters = "ABCDEFGH"
        rng = np.random.default_rng(22)
        sizes = rng.integers(2, 5, len(letters))

        def site(i, colour=BLUE):
            box = RoundedRectangle(width=1.2, height=1.2, corner_radius=0.12, stroke_color=colour, stroke_width=4)
            dots = VGroup(*[Dot(radius=0.09, color=colour) for _ in range(sizes[i])]).arrange_in_grid(2, 2, buff=0.18)
            name = label(letters[i], 28, colour, weight=BOLD).next_to(box, UP, 0.1)
            return VGroup(box, dots.move_to(box), name)

        survey = VGroup(*[site(i) for i in range(len(letters))]).arrange(RIGHT, buff=0.3).move_to(1.6 * UP)
        survey_name = label("the survey's sites", 28, SUBDUED).next_to(survey, LEFT, 0.3)
        draw = [1, 1, 3, 0, 5, 5, 7, 2]
        sample = VGroup(*[site(i, ORANGE) for i in draw]).arrange(RIGHT, buff=0.3).move_to(1.2 * DOWN)
        sample_name = label("one bootstrap sample", 28, ORANGE, weight=BOLD).next_to(sample, DOWN, 0.3)
        note = label("some twice, some not at all", 30, INK, weight=BOLD).to_edge(DOWN, buff=0.35)
        sixty = label("k-means refitted on 60 samples", 32, BLUE, weight=BOLD).to_edge(DOWN, buff=0.35)
        # "First, does the pattern come back? A bootstrap sample draws the survey's sites again ..."
        self.play(FadeIn(survey, lag_ratio=0.1), run_time=self.share(0.2))
        wait_until(self, 0.3)
        # "... at random, with replacement, each with all its stations."
        self.play(LaggedStart(*[TransformFromCopy(survey[i], s) for i, s in zip(draw, sample)], lag_ratio=0.15),
                  FadeIn(sample_name), run_time=self.share(0.35))
        self.play(FadeIn(note), run_time=self.share(0.1))
        # "k-means is refitted on sixty."
        wait_until(self, 0.84)
        self.play(FadeOut(note), FadeIn(sixty), run_time=self.share(0.1))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        # Schematic: six stations under two groupings, and three pairs judged.
        first = [0, 0, 0, 1, 1, 1]
        second = [0, 0, 1, 1, 1, 1]
        colours = [BLUE, ORANGE]
        xs = np.linspace(-3.0, 3.0, 6)

        def row(groups, y, name):
            dots = VGroup(*[Dot([x, y, 0], radius=0.2, color=colours[g]) for x, g in zip(xs, groups)])
            return VGroup(dots, label(name, 28, SUBDUED).next_to(dots, LEFT, 0.5))

        top, bottom = row(first, 2.0, "original"), row(second, 0.9, "refit")
        head = label("adjusted Rand index", 34, INK, weight=BOLD).to_edge(UP, buff=0.3)
        pairs = [(0, 1), (0, 4), (1, 2)]
        texts = [label("together in both: agree", 28, GREEN, weight=BOLD),
                 label("apart in both: agree", 28, GREEN, weight=BOLD),
                 label("together, then apart: disagree", 28, VERMILION, weight=BOLD)]
        for t in texts:
            t.move_to([0, -0.3, 0])
        scale, to_x = number_line(0, 1, -3.5, 3.5, -2.2, [0, 1], 0)
        ends = VGroup(label("chance", 28, SUBDUED).move_to([to_x(0), -3.0, 0]),
                      label("identical", 28, SUBDUED).move_to([to_x(1), -3.0, 0]))
        # "The adjusted Rand index compares each refit with the original."
        self.play(FadeIn(head), FadeIn(top), FadeIn(bottom), run_time=self.share(0.2))
        # "For every pair of stations: together in both, or apart in both?"
        wait_until(self, 0.3)
        shown = None
        for (i, j), text in zip(pairs, texts):
            rings = VGroup(*[Circle(0.3, color=INK, stroke_width=4).move_to(r[0][k]) for r in (top, bottom) for k in (i, j)])
            anims = [Create(rings), FadeIn(text)]
            if shown is not None:
                anims += [FadeOut(shown[0]), FadeOut(shown[1])]
            self.play(*anims, run_time=self.share(0.1))
            shown = (rings, text)
        # "One means identical, zero no better than chance."
        wait_until(self, 0.68)
        self.play(FadeOut(shown[0]), FadeOut(shown[1]), FadeIn(scale), FadeIn(ends), run_time=self.share(0.15))
        self.finish()


BIN = 0.05


def dot_stack(values, to_x, base, colours, height=4.2):
    """A dot plot: each value a dot, stacked in bins of BIN, as the page's histogram."""
    bins = np.minimum((np.asarray(values) / BIN).astype(int), int(1 / BIN) - 1)
    step = min(0.13, height / np.bincount(bins).max())
    radius = min(0.06, 0.45 * step)
    counts = {}
    dots = VGroup()
    for v in sorted(values):
        b = min(int(v / BIN), int(1 / BIN) - 1)
        n = counts.get(b, 0)
        counts[b] = n + 1
        dots.add(Dot([to_x((b + 0.5) * BIN), base + radius + step * n, 0], radius=radius,
                     color=colours(v)))
    return dots


class Scene25(VideoScene):
    number = 25

    def construct(self):
        reps = self.data("replicates")["agreement"].to_numpy()
        axis, to_x = number_line(0, 1, -5.6, 5.6, -2.6, [0, 0.25, 0.5, 0.75, 1], 2)
        name = label("agreement with the original (adjusted Rand index)", 26, SUBDUED).next_to(axis, DOWN, 0.05)
        dots = dot_stack(reps, to_x, -2.6, lambda v: BLUE if v > 0.5 else ORANGE)
        same, other = int((reps > 0.5).sum()), int((reps <= 0.5).sum())
        top = max(d.get_y() for d in dots)
        same_name = label(f"{same}: the seabed split", 32, BLUE, weight=BOLD).move_to([to_x(0.97), top + 0.45, 0],
                                                                                    aligned_edge=RIGHT)
        low_top = max(d.get_y() for d in dots if d.get_x() < to_x(0.5))
        other_name = label(f"{other}: shallow against deep", 32, ORANGE, weight=BOLD).move_to(
            [to_x(0.02), low_top + 0.5, 0], aligned_edge=LEFT)
        report = label("report how often each came back", 34, INK, weight=BOLD).to_edge(UP, buff=0.4)
        head = label(f"{len(reps)} bootstrap samples, k-means refitted", 30, SUBDUED).to_edge(UP, buff=0.4)
        # "In 52 of the 60 samples, the seabed split came back almost exactly."
        self.play(FadeIn(head), FadeIn(VGroup(axis, name)), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(d, shift=0.4 * DOWN) for d in dots], lag_ratio=0.03), run_time=self.share(0.25))
        self.play(FadeIn(same_name), run_time=self.share(0.08))
        # "In the other 8, a split into shallow and deep took its place."
        wait_until(self, 0.45)
        self.play(FadeIn(other_name), run_time=self.share(0.12))
        # "Report how often each came back."
        wait_until(self, 0.78)
        self.play(FadeOut(head), FadeIn(report), run_time=self.share(0.12))
        self.finish()


def position_axis(x0, x1, y, size=24, names=("centre 1", "boundary", "centre 2")):
    """Where a station sits between the two centres: 0 at the first, 1 at the second."""
    lo, hi = -1.0, 2.0
    to_x = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)  # noqa: E731
    line = Line([x0, y, 0], [x1, y, 0], color=GRID, stroke_width=3)
    marks = VGroup(*[VGroup(Line([to_x(v), y - 0.08, 0], [to_x(v), y + 0.08, 0], color=GRID, stroke_width=3),
                            label(t, size, SUBDUED).move_to([to_x(v), y - 0.3, 0]))
                     for v, t in zip((0, 0.5, 1), names) if t])
    return VGroup(line, marks), to_x, (lo, hi)


def histogram(values, to_x, span, base, height, colour, width_bin=0.05):
    lo, hi = span
    edges = np.arange(lo, hi + 1e-9, width_bin)
    counts, _ = np.histogram(np.clip(values, lo, hi - 1e-9), bins=edges)
    share = counts / counts.sum()
    bars = VGroup()
    scale = height / share.max()
    for left, s in zip(edges[:-1], share):
        if s == 0:
            continue
        x0, x1 = to_x(left), to_x(left + width_bin)
        bars.add(Rectangle(width=(x1 - x0) * 0.92, height=s * scale, stroke_width=0, fill_color=colour,
                           fill_opacity=1).move_to([(x0 + x1) / 2, base, 0], aligned_edge=DOWN))
    return bars


def boundary_band(to_x, base, height):
    return Rectangle(width=to_x(0.6) - to_x(0.4), height=height, stroke_width=0, fill_color=VERMILION,
                     fill_opacity=0.12).move_to([(to_x(0.4) + to_x(0.6)) / 2, base, 0], aligned_edge=DOWN)


class Scene26(VideoScene):
    number = 26

    def construct(self):
        # Schematic: made-up positions, two humps against a flat spread.
        rng = np.random.default_rng(25)
        humps = np.concatenate([rng.normal(0, 0.12, 400), rng.normal(1, 0.12, 400)])
        flat = rng.uniform(-0.1, 1.1, 800)
        rows = VGroup()
        for values, y, colour, text in ((humps, 0.6, GREEN, "groups: a gap"), (flat, -2.5, ORANGE, "gradient: no gap")):
            axis, to_x, span = position_axis(-4.6, 4.6, y)
            bars = histogram(values, to_x, span, y, 1.7, colour)
            name = label(text, 32, colour, weight=BOLD).move_to([5.3, y + 0.8, 0])
            rows.add(VGroup(axis, bars, name, boundary_band(to_x, y, 1.9)))
        head = label("Where each station sits between the two centres", 30, SUBDUED).to_edge(UP, buff=0.3)
        # "Second, is there a gap? Place each station on the line between the two cluster centres."
        self.play(FadeIn(head), FadeIn(rows[0][0]), FadeIn(rows[1][0]), run_time=self.share(0.3))
        # "Real groups leave few stations near the boundary; ..."
        wait_until(self, 0.45)
        self.play(FadeIn(rows[0][3]), GrowFromEdge(rows[0][1], DOWN), FadeIn(rows[0][2]), run_time=self.share(0.2))
        # "... a gradient leaves as many there as anywhere."
        wait_until(self, 0.72)
        self.play(FadeIn(rows[1][3]), GrowFromEdge(rows[1][1], DOWN), FadeIn(rows[1][2]), run_time=self.share(0.2))
        self.finish()


def positions_panel(scene, split, x0, x1, y, height, colour, names=("centre 1", "boundary", "centre 2")):
    positions = scene.data("positions")
    values = positions.loc[positions["split"] == split, "position"].to_numpy()
    axis, to_x, span = position_axis(x0, x1, y, names=names)
    bars = histogram(values, to_x, span, y, height, colour)
    near = np.mean(np.abs(values - 0.5) < 0.1)
    return VGroup(axis, bars, boundary_band(to_x, y, height + 0.2)), near, to_x


SEABED_SPLIT, SOFT_SPLIT = "All stations, two clusters", "Soft bottom only, two clusters"


class Scene27(VideoScene):
    number = 27

    def construct(self):
        panel, near, to_x = positions_panel(self, SEABED_SPLIT, -5.0, 5.0, -2.2, 3.6, GREEN)
        head = label("The seabed split: where each station sits", 30, SUBDUED).to_edge(UP, buff=0.3)
        note = label(f"{percent(near)} of stations\nnear the boundary", 32, VERMILION, weight=BOLD
                     ).move_to([to_x(0.5), 2.0, 0])
        # "The seabed split has a clear gap: ..."
        self.play(FadeIn(head), FadeIn(panel[0]), run_time=self.share(0.15))
        self.play(GrowFromEdge(panel[1], DOWN), run_time=self.share(0.3))
        # "... only 2 per cent of stations lie close to its boundary."
        wait_until(self, 0.5)
        self.play(FadeIn(panel[2]), FadeIn(note), run_time=self.share(0.2))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        record = self.data("record").pivot(index="cluster", columns="bottom", values="n").fillna(0).astype(int)
        external = self.data("external")
        ari = external["ARI with recorded seabed"].iloc[0]
        hard_c = record["hard"].idxmax()
        order = [hard_c] + [c for c in record.index if c != hard_c]
        cols = {"hard": (0.6, HARD), "soft": (3.8, SOFT)}
        heads = VGroup(*[label(f"{b} bottom", 30, colour, weight=BOLD).move_to([x, 2.0, 0])
                         for b, (x, colour) in cols.items()])
        never = label("recorded seabed, never shown to k-means", 28, SUBDUED).next_to(heads, UP, 0.25)
        names = VGroup()
        cells = VGroup()
        for i, c in enumerate(order):
            y = 0.6 - 2.0 * i
            names.add(label(f"cluster {i + 1}", 32, INK, weight=BOLD).move_to([-2.0, y, 0], aligned_edge=RIGHT))
            for b, (x, colour) in cols.items():
                main = (i == 0) == (b == "hard")
                box = RoundedRectangle(width=2.8, height=1.6, corner_radius=0.12, stroke_width=4,
                                       stroke_color=colour if main else GRID,
                                       fill_color=colour, fill_opacity=0.12 if main else 0).move_to([x, y, 0])
                cells.add(VGroup(box, label(f"{record.loc[c, b]}", 56, INK, weight=BOLD).move_to(box)))
        score = label(f"adjusted Rand index: {ari:.2f}", 38, GREEN, weight=BOLD).to_edge(DOWN, buff=0.4)
        # "Third, does it match a record? The split matches the recorded seabed, which k-means never saw, ..."
        self.play(FadeIn(names), FadeIn(heads), run_time=self.share(0.2))
        self.play(FadeIn(never), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.2), run_time=self.share(0.3))
        # "... at an adjusted Rand index of 0.92: the strongest evidence there is."
        wait_until(self, 0.62)
        self.play(FadeIn(score, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene29(KeyPointScene):
    number, point = 29, 3


# Quiz (scenes 30 and 31) -----------------------------------------------------------------

class Scene30(QuizScene):
    number = 30
    question = ("Within the soft bottom, k-means splits", "the stations into shallow and deep.",
                "The split comes back in every sample.", "Are they two groups?")


class Scene31(VideoScene):
    number = 31

    def construct(self):
        seabed, seabed_near, seabed_x = positions_panel(self, SEABED_SPLIT, -6.4, -0.6, -1.4, 2.4, GREEN, ("", "boundary", ""))
        soft, soft_near, soft_x = positions_panel(self, SOFT_SPLIT, 0.6, 6.4, -1.4, 2.4, ORANGE, ("", "boundary", ""))
        names = VGroup(label("the seabed split", 30, GREEN, weight=BOLD).move_to([-3.5, 1.6, 0]),
                       label("the soft-bottom split", 30, ORANGE, weight=BOLD).move_to([3.5, 1.6, 0]))
        notes = VGroup(label(f"{percent(seabed_near)} near the boundary", 28, GREEN, weight=BOLD
                             ).next_to(names[0], DOWN, 0.15),
                       label(f"{percent(soft_near)} near the boundary", 28, ORANGE, weight=BOLD
                             ).next_to(names[1], DOWN, 0.15))
        answer = label("Not yet: no gap", 44, INK, weight=BOLD).to_edge(UP, buff=0.35)
        finding = label("a steady depth gradient, cut in the same place every time", 30, INK, weight=BOLD
                        ).to_edge(DOWN, buff=0.25)
        too = label("a gradient is a finding too", 34, GREEN, weight=BOLD).to_edge(DOWN, buff=0.25)
        # "Not yet."
        self.play(FadeIn(answer), run_time=self.share(0.08))
        # "Eleven per cent of its stations sit near the boundary, ..."
        self.play(FadeIn(soft), FadeIn(names[1]), FadeIn(notes[1]), run_time=self.share(0.2))
        # "... against 2 per cent for the seabed split."
        wait_until(self, 0.3)
        self.play(FadeIn(seabed), FadeIn(names[0]), FadeIn(notes[0]), run_time=self.share(0.15))
        # "No gap: k-means cut a steady depth gradient in the same place every time."
        wait_until(self, 0.5)
        self.play(FadeIn(finding), Indicate(soft[2], color=VERMILION), run_time=self.share(0.15))
        # "And a gradient is a finding too."
        wait_until(self, 0.84)
        self.play(FadeOut(finding), FadeIn(too), run_time=self.share(0.1))
        self.finish()


# Key points and end card (scenes 32–35) ----------------------------------------------------

class Scene32(RecapScene):
    number, point = 32, 1


class Scene33(RecapScene):
    number, point = 33, 2


class Scene34(RecapScene):
    number, point = 34, 3


class Scene35(EndCardScene):
    number = 35
