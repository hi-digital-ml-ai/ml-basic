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


PROMISES = ["Find groups without labels",
            "Draw many columns as one map",
            "Check that groups come back"]
ANSWERS = ["k-means sorts\nthe stations into groups\nof similar ones",
           "PCA places the stations\nalong their directions\nof most spread",
           "Refit on resampled sites,\nand report how often\nthey return"]
RECAP = PROMISES


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("finding groups", "drawing many", "and checking"))


HARD, SOFT = ORANGE, BLUE     # hard and soft bottom, in every scene


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


def number_line(lo, hi, x0, x1, y, ticks, digits=2, size=26):
    """A horizontal value axis from x0 to x1 at height y; returns it and a mapper."""
    to_x = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)  # noqa: E731
    line = Line([x0, y, 0], [x1, y, 0], color=GRID, stroke_width=3)
    marks = VGroup(*[VGroup(Line([to_x(t), y - 0.08, 0], [to_x(t), y + 0.08, 0], color=GRID,
                                 stroke_width=3),
                            label(f"{t:.{digits}f}", size, SUBDUED).move_to([to_x(t), y - 0.35, 0]))
                     for t in ticks])
    return VGroup(line, marks), to_x


def lines_of(text, size=32, colour=INK, weight=NORMAL, buff=0.12):
    return VGroup(*[label(t, size, colour, weight=weight) for t in text.split("\n")]
                  ).arrange(DOWN, buff=buff, aligned_edge=LEFT)


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


def random_groups(k, seed, centre, size=5.2, n=160):
    """Schematic: random points in a square, and the k groups k-means cuts them into."""
    rng = np.random.default_rng(seed)
    half = size / 2
    points = rng.uniform(-half + 0.1, half - 0.1, (n, 2))
    groups = kmeans(points, points[:k].copy())
    frame = Square(size, color=GRID, stroke_width=3).move_to(centre)
    dots = VGroup(*[Dot(centre + np.array([x, y, 0]), radius=0.06, color=GREY) for x, y in points])
    return frame, dots, groups


# Find groups without labels (scenes 2–6) ---------------------------------------------------

def cell_grid(rows, cols, size, seed, colour=BLUE):
    rng = np.random.default_rng(seed)
    cells = VGroup(*[Square(size, stroke_width=0, fill_color=colour,
                            fill_opacity=float(rng.choice([0.08, 0.3, 0.6, 0.9], p=[0.5, 0.2, 0.2, 0.1])))
                     for _ in range(rows * cols)])
    return cells.arrange_in_grid(rows, cols, buff=0.04)


class Scene02(VideoScene):
    number = 2

    def construct(self):
        # Schematic: a table of counts, shaded by size, and a habitat column left empty.
        cells = cell_grid(14, 18, 0.22, 2).move_to([-1.2, -0.3, 0])
        top = label("animals counted at each station", 30, BLUE, weight=BOLD).next_to(cells, UP, 0.3).align_to(cells, LEFT)
        answer = DashedVMobject(Rectangle(width=1.3, height=cells.height, color=GREY, stroke_width=3),
                                num_dashes=50).next_to(cells, RIGHT, 0.4)
        answer_name = label("habitat", 30, VERMILION, weight=BOLD).next_to(answer, DOWN, 0.2)
        marks = VGroup(*[label("?", 30, VERMILION, weight=BOLD).move_to([answer.get_x(), y, 0])
                         for y in np.linspace(answer.get_top()[1] - 0.5, answer.get_bottom()[1] + 0.5, 6)])
        idea = label("can the counts alone sort the stations into groups?", 32, INK, weight=BOLD
                     ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(cells, lag_ratio=0.002), FadeIn(top), run_time=self.share(0.2))
        cue(self, "but nobody has said")
        self.play(Create(answer), FadeIn(answer_name), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2), run_time=self.share(0.12))
        cue(self, "Can the counts")
        self.play(FadeIn(idea, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        matrix = self.data("matrix")
        cols = list(matrix.columns)
        w, h = 1.05, 0.62
        x0, y0 = -3.7, 1.9
        heads = VGroup(*[label(c, 28, BLUE, weight=BOLD).move_to([x0 + i * w, y0, 0]) for i, c in enumerate(cols)])
        heads.add(label("…  tax24", 28, BLUE, weight=BOLD).move_to([x0 + len(cols) * w + 0.35, y0, 0]))
        rows = VGroup()
        for r, (_, row) in enumerate(matrix.iterrows()):
            y = y0 - (r + 1) * h
            cells = VGroup(*[label(f"{int(v)}", 30).move_to([x0 + i * w, y, 0]) for i, v in enumerate(row)])
            cells.add(label("…", 30, SUBDUED).move_to([x0 + len(cols) * w, y, 0]))
            rows.add(cells)
        more = label("⋮", 34, SUBDUED).move_to([x0 + 3 * w, y0 - (len(matrix) + 1) * h, 0])
        brace = Brace(VGroup(rows, more), LEFT, color=SUBDUED)
        n_rows = label("800\nstations", 30, SUBDUED, weight=BOLD).next_to(brace, LEFT, 0.2)
        top = Brace(heads, UP, color=SUBDUED)
        n_cols = label("24 taxa", 30, SUBDUED, weight=BOLD).next_to(top, UP, 0.1)
        name = label("one row per station, one column per taxon", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(heads), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), FadeIn(more),
                  run_time=self.share(0.25))
        self.play(GrowFromCenter(brace), FadeIn(n_rows), run_time=self.share(0.1))
        cue(self, "each with counts")
        self.play(GrowFromCenter(top), FadeIn(n_cols), run_time=self.share(0.1))
        cue(self, "One row per")
        self.play(FadeIn(name, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


TWO_TAXA_SIDE = 4.4     # x of the notes beside the two-taxa picture


def two_taxa_layout():
    """Schematic: stations placed by two made-up taxa's counts, in two clouds."""
    rng = np.random.default_rng(7)
    points = np.vstack([rng.normal([2.6, 6.8], 1.0, (40, 2)), rng.normal([7.2, 2.6], 1.0, (40, 2))])
    points = np.clip(points, 0.4, 9.6)
    axes = plain_axes([0, 10, 1], [0, 10, 1], 6.6, 5.6).move_to([-2.6, -0.3, 0])
    names = VGroup(label("count of taxon A", 26, SUBDUED).next_to(axes, DOWN, 0.15),
                   label("count of taxon B", 26, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.15))
    dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.09, color=GREY) for x, y in points])
    return axes, VGroup(axes, names), dots, points


class Scene04(VideoScene):
    number = 4

    def construct(self):
        axes, frame, dots, points = two_taxa_layout()
        head = label("Clustering: groups of similar stations", 34, INK, weight=BOLD).to_edge(UP, buff=0.3)
        point = lines_of("each station:\na point, placed\nby its counts", 30, BLUE, BOLD).move_to([TWO_TAXA_SIDE, 1.3, 0])
        close = lines_of("similar counts:\nclose together", 30, INK, BOLD).move_to([TWO_TAXA_SIDE, -0.5, 0])
        same = lines_of("two taxa here;\nwith 24, the same idea", 28, SUBDUED).move_to([TWO_TAXA_SIDE, -2.1, 0])
        near = np.argsort(((points - [2.6, 6.8]) ** 2).sum(1))[:3]
        rings = VGroup(*[Circle(0.2, color=INK, stroke_width=4).move_to(dots[i]) for i in near])
        self.play(FadeIn(head), run_time=self.share(0.1))
        cue(self, "Picture each")
        self.play(FadeIn(frame), FadeIn(dots, lag_ratio=0.02), FadeIn(point), run_time=self.share(0.18))
        cue(self, "so that stations")
        self.play(Create(rings), FadeIn(close), run_time=self.share(0.12))
        cue(self, "Here there are")
        self.play(FadeOut(rings), FadeIn(same), run_time=self.share(0.12))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        axes, frame, dots, points = two_taxa_layout()
        self.add(frame, dots)
        head = label("k-means, with k = 2", 34, INK, weight=BOLD).to_edge(UP, buff=0.3)
        colours = [ORANGE, BLUE]
        centres = np.array([[4.2, 9.0], [5.6, 8.2]])
        stars = VGroup(*[Star(5, outer_radius=0.28, color=c, fill_opacity=1, stroke_width=0).move_to(axes.c2p(*p))
                         for c, p in zip(colours, centres)])
        steps = VGroup(lines_of("1. each station joins\n    its nearest centre", 28, INK, BOLD),
                       lines_of("2. each centre moves to\n    the middle of its stations", 28, INK, BOLD),
                       lines_of("repeat until\nnothing changes", 28, BLUE, BOLD)
                       ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([TWO_TAXA_SIDE, -0.3, 0])

        def assign():
            nearest = np.argmin(((points[:, None, :] - centres[None]) ** 2).sum(-1), axis=1)
            return nearest, [d.animate.set_color(colours[n]) for d, n in zip(dots, nearest)]

        def move(nearest):
            new = np.array([points[nearest == j].mean(0) for j in range(2)])
            return new, [s.animate.move_to(axes.c2p(*p)) for s, p in zip(stars, new)]

        self.play(FadeIn(head), run_time=self.share(0.08))
        cue(self, "It places two")
        self.play(FadeIn(stars, scale=2), run_time=self.share(0.06))
        cue(self, "and each station joins")
        nearest, anims = assign()
        self.play(*anims, FadeIn(steps[0]), run_time=self.share(0.08))
        cue(self, "Each centre then")
        centres, anims = move(nearest)
        self.play(*anims, FadeIn(steps[1]), run_time=self.share(0.08))
        cue(self, "and the two steps")
        self.play(FadeIn(steps[2]), run_time=self.share(0.06))
        for _ in range(3):
            nearest, anims = assign()
            self.play(*anims, run_time=self.share(0.035))
            centres, anims = move(nearest)
            self.play(*anims, run_time=self.share(0.035))
        self.finish()


def waffle(n_first, n_second, colour_first, colour_second, cols, size=0.17, gap=0.045):
    """n_first + n_second squares in rows of `cols`: the second kind last, at the bottom."""
    squares = VGroup(*[Square(size, stroke_width=0, fill_color=colour_first, fill_opacity=1)
                       for _ in range(n_first)],
                     *[Square(size, stroke_width=0, fill_color=colour_second, fill_opacity=1)
                       for _ in range(n_second)])
    for i, s in enumerate(squares):
        s.move_to([(i % cols) * (size + gap), -(i // cols) * (size + gap), 0])
    return squares


class Scene06(VideoScene):
    number = 6

    def construct(self):
        seabed = self.data("seabed").pivot(index="cluster", columns="bottom", values="n")
        hard_c = seabed["hard"].idxmax()
        soft_c = [c for c in seabed.index if c != hard_c][0]
        # Each group's own kind first, the stations of the other kind last.
        hard_sq = waffle(seabed.loc[hard_c, "hard"], seabed.loc[hard_c, "soft"], HARD, SOFT, 12)
        soft_sq = waffle(seabed.loc[soft_c, "soft"], seabed.loc[soft_c, "hard"], SOFT, HARD, 30)
        hard_sq.move_to([-4.3, -0.55, 0])
        soft_sq.move_to([1.9, -0.55, 0])
        hard_sq.align_to(soft_sq, UP)
        grey = VGroup(*[s.copy().set_fill(GREY) for s in [*hard_sq, *soft_sq]])
        names = VGroup(label(f"group 1: {seabed.loc[hard_c].sum()} stations", 30, INK, weight=BOLD
                             ).next_to(hard_sq, UP, 0.3),
                       label(f"group 2: {seabed.loc[soft_c].sum()} stations", 30, INK, weight=BOLD
                             ).next_to(soft_sq, UP, 0.3))
        key = VGroup(VGroup(Square(0.25, stroke_width=0, fill_color=HARD, fill_opacity=1),
                            label("hard bottom: rock, gravel", 28, SUBDUED)).arrange(RIGHT, buff=0.2),
                     VGroup(Square(0.25, stroke_width=0, fill_color=SOFT, fill_opacity=1),
                            label("soft bottom: sand, mud", 28, SUBDUED)).arrange(RIGHT, buff=0.2)
                     ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.3)
        head = label("k-means, given only the counts", 32, SUBDUED).to_edge(UP, buff=0.25)
        out = VGroup(*hard_sq[seabed.loc[hard_c, "hard"]:], *soft_sq[seabed.loc[soft_c, "soft"]:])
        rings = VGroup(*[Circle(0.16, color=VERMILION, stroke_width=4).move_to(s) for s in out])
        note = label(f"{len(out)} of {int(seabed.values.sum())} in the other kind's group", 32, VERMILION,
                     weight=BOLD).to_edge(UP, buff=0.25)
        self.play(FadeIn(head), FadeIn(grey, lag_ratio=0.001), FadeIn(names), run_time=self.share(0.2))
        cue(self, "Now compare")
        self.play(*[Transform(g, s) for g, s in zip(grey, [*hard_sq, *soft_sq])], FadeIn(key),
                  run_time=self.share(0.15))
        cue(self, "Only 15")
        self.play(Create(rings), FadeOut(head), FadeIn(note), run_time=self.share(0.12))
        self.finish()


class Scene07(KeyPointScene):
    number, point = 7, 1


# Draw many columns as one map (scenes 8–12) -----------------------------------------------

SPREAD_ANGLE = 0.5


def spread_layout():
    """Schematic: a tilted cloud, its usual axes, and a copy of them to turn."""
    rng = np.random.default_rng(24)
    raw = rng.normal(0, 1, (80, 2)) * [2.2, 0.6]
    rot = np.array([[np.cos(SPREAD_ANGLE), -np.sin(SPREAD_ANGLE)],
                    [np.sin(SPREAD_ANGLE), np.cos(SPREAD_ANGLE)]])
    centre = np.array([0, -0.4, 0])
    points = raw @ rot.T + centre[:2]
    dots = VGroup(*[Dot([x, y, 0], radius=0.08, color=GREY) for x, y in points])
    old = VGroup(Line(centre + 5 * LEFT, centre + 5 * RIGHT, color=GRID, stroke_width=4),
                 Line(centre + 3 * DOWN, centre + 3 * UP, color=GRID, stroke_width=4))
    new = old.copy().set_color(BLUE)
    head = label("Principal component analysis (PCA)", 34, INK, weight=BOLD).to_edge(UP, buff=0.3)
    return centre, dots, old, new, head


def pc_names(new):
    first = label("PC1: most spread", 30, BLUE, weight=BOLD)
    first.next_to(new[0].get_end(), UP, 0.1).shift(1.2 * LEFT)
    second = label("PC2: next most,\nat right angles", 30, BLUE, weight=BOLD)
    second.next_to(new[1].get_end(), LEFT, 0.3).shift(0.5 * DOWN + 0.4 * LEFT)
    return first, second


class Scene08(VideoScene):
    number = 8

    def construct(self):
        centre, dots, old, new, head = spread_layout()
        many = label("24 columns: no single picture", 34, SUBDUED).to_edge(UP, buff=0.3)
        flat = label("two columns: a flat picture", 34, SUBDUED).to_edge(UP, buff=0.3)
        self.play(FadeIn(old), FadeIn(dots, lag_ratio=0.02), FadeIn(flat), run_time=self.share(0.15))
        cue(self, "but 24")
        self.play(FadeOut(flat), FadeIn(many), run_time=self.share(0.08))
        cue(self, "Principal component")
        self.play(FadeOut(many), FadeIn(head), run_time=self.share(0.08))
        cue(self, "It finds the direction")
        self.add(new)
        self.play(Rotate(new, SPREAD_ANGLE, about_point=centre), run_time=self.share(0.2))
        first, _ = pc_names(new)
        cue(self, "the first principal")
        self.play(FadeIn(first), run_time=self.share(0.08))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        centre, dots, old, new, head = spread_layout()
        new.rotate(SPREAD_ANGLE, about_point=centre)
        first, second = pc_names(new)
        self.add(old, dots, new, head, first)
        mix = label("each one: a mix of all 24 taxa", 32, INK, weight=BOLD).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(second), Indicate(new[1], color=BLUE), run_time=self.share(0.15))
        cue(self, "Each component")
        self.play(FadeIn(mix, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


SIDE_X = 4.7    # right of the map: where the map's notes and keys go


def ordination_layout(scene):
    stations = scene.data("ordination")
    hard = (stations["hard_bottom"].astype(str).str.upper() == "TRUE").to_numpy()
    x_lo, x_hi = np.floor(stations["PC1"].min()), np.ceil(stations["PC1"].max())
    y_lo, y_hi = np.floor(stations["PC2"].min()), np.ceil(stations["PC2"].max())
    height = 6.0
    width = min(height * (x_hi - x_lo) / (y_hi - y_lo), 8.4)
    axes = plain_axes([x_lo, x_hi, 1], [y_lo, y_hi, 1], width, height).move_to([-1.6, -0.35, 0])
    axes.set_stroke(opacity=0.5, width=2)       # faint lines through zero; the box is the frame
    box = Rectangle(width=width, height=height, color=GRID, stroke_width=3).move_to(
        (axes.c2p(x_lo, y_lo) + axes.c2p(x_hi, y_hi)) / 2)
    places = [axes.c2p(a, b) for a, b in zip(stations["PC1"], stations["PC2"])]
    lo, hi = stations["depth_m"].min(), stations["depth_m"].max()
    shade = [(d - lo) / (hi - lo) for d in stations["depth_m"]]
    grey = VGroup(*[Dot(p, radius=0.055, color=GREY, fill_opacity=0.9) for p in places])
    seabed = VGroup(*[marker(p, HARD if h else SOFT, h, 0.06) for p, h in zip(places, hard)])
    depth = VGroup(*[marker(p, viridis(t), h, 0.06) for p, h, t in zip(places, hard, shade)])
    x_name = label("PC1", 28, SUBDUED).next_to(box, DOWN, 0.15)
    y_name = label("PC2", 28, SUBDUED).rotate(PI / 2).next_to(box, LEFT, 0.15)
    return VGroup(axes, box, x_name, y_name), grey, seabed, depth


def seabed_key(hard_colour=HARD, soft_colour=SOFT):
    return VGroup(VGroup(marker(ORIGIN, hard_colour, True, 0.1), label("hard bottom", 26, SUBDUED)).arrange(RIGHT, buff=0.2),
                  VGroup(marker(ORIGIN, soft_colour, False, 0.1), label("soft bottom", 26, SUBDUED)).arrange(RIGHT, buff=0.2)
                  ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([SIDE_X, 2.7, 0])


def map_keys():
    """The keys once the map is coloured by depth: seabed by shape, depth by colour."""
    return VGroup(seabed_key(INK, INK), depth_key(2.0).move_to([SIDE_X, 1.55, 0]))


class Scene10(VideoScene):
    number = 10

    def construct(self):
        frame, grey, _, _ = ordination_layout(self)
        dot = lines_of("each dot:\na station", 30, SUBDUED).move_to([SIDE_X, 0.9, 0])
        close = lines_of("similar counts\nsit close", 32, BLUE, BOLD).move_to([SIDE_X, -0.6, 0])
        self.play(FadeIn(frame), run_time=self.share(0.1))
        self.play(FadeIn(grey, lag_ratio=0.001), FadeIn(dot), run_time=self.share(0.25))
        cue(self, "Stations with similar")
        self.play(FadeIn(close), run_time=self.share(0.12))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        frame, grey, seabed, depth = ordination_layout(self)
        self.add(frame, grey)
        arms = lines_of("two arms:\nhard and soft", 32, INK, BOLD).move_to([SIDE_X, 0.2, 0])
        smooth = lines_of("depth changes\nsmoothly", 32, INK, BOLD).move_to([SIDE_X, -1.2, 0])
        never = lines_of("PCA saw\nneither", 32, VERMILION, BOLD).move_to([SIDE_X, -2.6, 0])
        key = seabed_key()
        keys = map_keys()
        cue(self, "The hard-bottom")
        self.play(*[Transform(g, s) for g, s in zip(grey, seabed)], FadeIn(key), run_time=self.share(0.15))
        self.play(FadeIn(arms), run_time=self.share(0.08))
        cue(self, "and depth changes")
        self.play(*[Transform(g, d) for g, d in zip(grey, depth)], Transform(key, keys[0]), FadeIn(keys[1]),
                  run_time=self.share(0.15))
        self.play(FadeIn(smooth), run_time=self.share(0.08))
        cue(self, "PCA never saw")
        self.play(FadeIn(never), run_time=self.share(0.1))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        frame, _, _, depth = ordination_layout(self)
        self.add(frame, depth, map_keys())
        variance = self.data("variance")
        two = variance["cumulative percent variance"].iloc[1]
        held = lines_of(f"PC1 and PC2:\n{two:.1f}% of\nthe variance", 32, BLUE, BOLD).move_to([SIDE_X, 0.0, 0])
        enough = lines_of("a summary:\nenough to show\nthe main structure", 28, INK, BOLD).move_to([SIDE_X, -2.0, 0])
        self.play(Indicate(frame[1], color=BLUE, scale_factor=1.0), run_time=self.share(0.15))
        cue(self, "Here it holds")
        self.play(FadeIn(held), run_time=self.share(0.12))
        cue(self, "That is usual")
        self.play(FadeIn(enough), run_time=self.share(0.12))
        self.finish()


class Scene13(KeyPointScene):
    number, point = 13, 2


# Check that groups come back (scenes 14–17) ------------------------------------------------

class Scene14(VideoScene):
    number = 14

    def construct(self):
        frame, dots, groups = random_groups(4, 66, np.array([-2.8, -0.3, 0]), 5.6)
        colours = [BLUE, ORANGE, GREEN, PURPLE]
        name = label("random numbers", 30, SUBDUED).next_to(frame, UP, 0.25)
        ask = label("asked for four groups", 34, INK, weight=BOLD).move_to([3.6, 1.2, 0])
        get = label("four tidy groups", 34, BLUE, weight=BOLD).move_to([3.6, 0.1, 0])
        nothing = lines_of("so groups alone\nprove nothing", 36, VERMILION, BOLD).move_to([3.6, -1.6, 0])
        cue(self, "k-means always")
        self.play(Create(frame), FadeIn(dots, lag_ratio=0.005), FadeIn(name), run_time=self.share(0.15))
        cue(self, "Asked for four")
        self.play(FadeIn(ask), run_time=self.share(0.06))
        self.play(*[d.animate.set_color(colours[g]) for d, g in zip(dots, groups)], FadeIn(get),
                  run_time=self.share(0.15))
        cue(self, "So a set")
        self.play(FadeIn(nothing, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Schematic: eight sites, each a box of stations, drawn again with replacement.
        letters = "ABCDEFGH"
        rng = np.random.default_rng(22)
        sizes = rng.integers(2, 5, len(letters))

        def site(i, colour=BLUE):
            box = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.1, stroke_color=colour, stroke_width=4)
            dots = VGroup(*[Dot(radius=0.08, color=colour) for _ in range(sizes[i])]).arrange_in_grid(2, 2, buff=0.14)
            name = label(letters[i], 26, colour, weight=BOLD).next_to(box, UP, 0.1)
            return VGroup(box, dots.move_to(box), name)

        head = label("real groups come back when the data change a little", 32, INK, weight=BOLD
                     ).to_edge(UP, buff=0.3)
        survey = VGroup(*[site(i) for i in range(len(letters))]).arrange(RIGHT, buff=0.22).move_to([1.8, 1.2, 0])
        survey_name = lines_of("the survey's\nsites", 28, SUBDUED).next_to(survey, LEFT, 0.5)
        draw = [1, 1, 3, 0, 5, 5, 7, 2]
        sample = VGroup(*[site(i, ORANGE) for i in draw]).arrange(RIGHT, buff=0.22).move_to([1.8, -1.2, 0])
        sample_name = lines_of("a resample:\nsome twice,\nsome not at all", 28, ORANGE, BOLD
                               ).next_to(sample, LEFT, 0.4)
        refit = label("fit k-means again: the same groups?", 34, BLUE, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(head), run_time=self.share(0.1))
        cue(self, "resample the survey")
        self.play(FadeIn(survey, lag_ratio=0.1), FadeIn(survey_name), run_time=self.share(0.12))
        cue(self, "draw 160")
        self.play(LaggedStart(*[TransformFromCopy(survey[i], s) for i, s in zip(draw, sample)], lag_ratio=0.15),
                  run_time=self.share(0.2))
        self.play(FadeIn(sample_name), run_time=self.share(0.06))
        cue(self, "Fit k-means again")
        self.play(FadeIn(refit, shift=0.2 * UP), run_time=self.share(0.1))
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


def replicates_layout(scene):
    reps = scene.data("replicates")["agreement"].to_numpy()
    axis, to_x = number_line(0, 1, -5.6, 5.6, -2.6, [0, 0.25, 0.5, 0.75, 1], 2)
    name = label("how closely each refit's groups match the first ones (1: the same)", 26, SUBDUED
                 ).next_to(axis, DOWN, 0.05)
    dots = dot_stack(reps, to_x, -2.6, lambda v: BLUE if v > 0.5 else ORANGE)
    same, other = int((reps > 0.5).sum()), int((reps <= 0.5).sum())
    top = max(d.get_y() for d in dots)
    same_name = label(f"{same}: the hard and soft groups", 32, BLUE, weight=BOLD).move_to(
        [to_x(0.97), top + 0.45, 0], aligned_edge=RIGHT)
    low_top = max(d.get_y() for d in dots if d.get_x() < to_x(0.5))
    other_name = label(f"{other}: shallow against deep", 32, ORANGE, weight=BOLD).move_to(
        [to_x(0.02), low_top + 0.5, 0], aligned_edge=LEFT)
    head = label(f"{len(reps)} refits, each on resampled sites", 30, SUBDUED).to_edge(UP, buff=0.4)
    return VGroup(axis, name), dots, same_name, other_name, head


class Scene16(VideoScene):
    number = 16

    def construct(self):
        axis, dots, same_name, other_name, head = replicates_layout(self)
        self.play(FadeIn(head), FadeIn(axis), run_time=self.share(0.1))
        cue(self, "Each dot")
        self.play(LaggedStart(*[FadeIn(d, shift=0.4 * DOWN) for d in dots], lag_ratio=0.03), run_time=self.share(0.2))
        cue(self, "In 52")
        self.play(FadeIn(same_name), run_time=self.share(0.08))
        cue(self, "In the other")
        self.play(FadeIn(other_name), run_time=self.share(0.08))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        axis, dots, same_name, other_name, head = replicates_layout(self)
        self.add(axis, dots, same_name, other_name, head)
        two = label("two competing answers", 36, INK, weight=BOLD).to_edge(UP, buff=0.4)
        report = lines_of("report how often\neach one came back", 34, INK, BOLD).move_to([-1.8, 0.6, 0])
        self.play(FadeOut(head), FadeIn(two), run_time=self.share(0.12))
        cue(self, "Report how often")
        self.play(FadeIn(report, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene18(KeyPointScene):
    number, point = 18, 3


# Quiz (scenes 19 and 20) -----------------------------------------------------------------

class Scene19(QuizScene):
    number = 19
    question = ("Asked for five groups of plankton samples,", "k-means returns five groups.",
                "Do the samples fall into five groups?")


class Scene20(VideoScene):
    number = 20

    def construct(self):
        frame, dots, groups = random_groups(5, 55, np.array([-3.0, -0.6, 0]), 5.2)
        colours = [BLUE, ORANGE, GREEN, PURPLE, VERMILION]
        answer = label("Not yet", 48, INK, weight=BOLD).to_edge(UP, buff=0.35)
        name = label("random numbers", 28, SUBDUED).next_to(frame, UP, 0.2)
        five = lines_of("five groups, because\nfive were asked for", 32, INK, BOLD).move_to([3.4, 0.7, 0])
        check = lines_of("resample, refit:\ndo the same five\ncome back?", 34, BLUE, BOLD).move_to([3.4, -1.6, 0])
        self.play(FadeIn(answer), run_time=self.share(0.08))
        cue(self, "k-means returns")
        self.play(Create(frame), FadeIn(dots, lag_ratio=0.005), FadeIn(name), run_time=self.share(0.12))
        self.play(*[d.animate.set_color(colours[g]) for d, g in zip(dots, groups)], FadeIn(five),
                  run_time=self.share(0.15))
        cue(self, "Resample, refit")
        self.play(FadeIn(check, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


# Key points and end card (scenes 21–24) ----------------------------------------------------

class Scene21(RecapScene):
    number, point = 21, 1


class Scene22(RecapScene):
    number, point = 22, 2


class Scene23(RecapScene):
    number, point = 23, 3


class Scene24(EndCardScene):
    number = 24
