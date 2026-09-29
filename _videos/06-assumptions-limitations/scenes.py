"""Manim scenes for the assumptions video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/06-assumptions-limitations
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


PROMISES = ["Why rows are worth less than they seem",
            "Why a better fit can be more wrong",
            "Why a model answers where it knows nothing"]
ANSWERS = ["Repeat visits and neighbours\nmake results look more\ncertain than they are",
           "Flexibility and the wrong\ndistribution give confident\nanswers that are false",
           "Past the edge of its data,\nand on rare events, a model\nanswers anyway: check both"]
RECAP = ["Rows are worth less than they seem",
         "A better fit can be more wrong",
         "A model answers where it knows nothing"]


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


# The puzzle: 95% accurate, never once right (scenes 2–4, page results) -------------------

def accuracy_layout(scene):
    untouched = scene.data("imbalance-metrics").set_index("recipe").loc["Untouched"]
    flagged = int(scene.data("thresholds").query("threshold == 0.5")["flagged"].iloc[0])
    head = label("A model built to find a rare species", 36, SUBDUED).to_edge(UP, buff=0.8)

    track = RoundedRectangle(width=5.4, height=0.7, corner_radius=0.12, stroke_color=GRID,
                             stroke_width=3).move_to([-3.3, 0, 0])
    fill = Rectangle(width=5.4 * untouched["accuracy"], height=0.7, stroke_width=0,
                     fill_color=GREEN, fill_opacity=1).align_to(track, LEFT).set_y(0)
    value = label(f"{percent(untouched['accuracy'])} accurate", 56, GREEN, weight=BOLD
                  ).next_to(track, UP, 0.5)
    gauge = VGroup(track, fill, value)

    count = label(str(flagged), 150, VERMILION, weight=BOLD).move_to([3.3, 0.2, 0])
    count_name = VGroup(label("stations where it said", 30, SUBDUED),
                        label("\"the species is here\"", 30, SUBDUED)
                        ).arrange(DOWN, buff=0.12).next_to(count, DOWN, 0.4)
    counter = VGroup(count, count_name)
    return head, gauge, counter


class Scene02(VideoScene):
    number = 2

    def construct(self):
        head, gauge, counter = accuracy_layout(self)
        track, fill, value = gauge
        # "Here is a model built to find a rare species."
        self.play(FadeIn(head), FadeIn(track), run_time=self.share(0.2))
        self.wait(self.share(0.2))
        # "It is 95% accurate."
        self.play(GrowFromEdge(fill, LEFT), run_time=self.share(0.3))
        self.play(FadeIn(value, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        head, gauge, counter = accuracy_layout(self)
        self.add(head, gauge)
        self.play(FadeIn(counter[1]), run_time=self.share(0.2))
        # "... it never once said the species was there."
        self.play(FadeIn(counter[0], scale=1.6), run_time=self.share(0.2))
        self.play(Circumscribe(counter[0], color=VERMILION), run_time=self.share(0.3))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        head, gauge, counter = accuracy_layout(self)
        self.add(head, gauge, counter)
        mark = label("?", 110, PURPLE, weight=BOLD).move_to([0, 0.2, 0])
        self.play(FadeIn(mark, scale=2), run_time=self.share(0.3))
        self.play(Wiggle(mark), run_time=self.share(0.4))
        self.finish()


# Simulated survey (scene 5, schematic) ----------------------------------------------------

class Scene05(VideoScene):
    number = 5

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


# Every method assumes something (scenes 6–7, schematic) -----------------------------------

class Scene06(VideoScene):
    number = 6

    def construct(self):
        called = label("machine learning is", 40, SUBDUED).move_to(1.3 * UP)
        free = label("assumption-free", 80, INK, weight=BOLD).next_to(called, DOWN, 0.4)
        strike = Line(free.get_left() + 0.2 * LEFT, free.get_right() + 0.2 * RIGHT,
                      color=VERMILION, stroke_width=10)
        # "Machine learning is often called assumption-free."
        self.play(FadeIn(called), FadeIn(free, shift=0.2 * UP), run_time=self.share(0.25))
        self.wait(self.share(0.3))
        # "It is not."
        self.play(Create(strike), free.animate.set_color(GREY), run_time=self.share(0.15))
        self.finish()


def assumes_panels():
    def panel(heading, items, weight_colour, x):
        box = RoundedRectangle(width=5.6, height=4.8, corner_radius=0.2, stroke_color=weight_colour,
                               stroke_width=5).move_to([x, -0.3, 0])
        head = label(heading, 34, weight_colour, weight=BOLD).next_to(box.get_top(), DOWN, 0.4)
        rows = VGroup(*[label(t, 30) for t in items]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rows.next_to(head, DOWN, 0.5)
        return VGroup(box, head, rows)

    shape = panel("assumes less about", ["the shape of a relationship"], GREY, -3.3)
    collection = panel("assumes a lot about", ["how the data were collected:",
                                               "  every row independent",
                                               "  the right spread",
                                               "  new data like the old",
                                               "  enough of every class"], BLUE, 3.3)
    return shape, collection


class Scene07(VideoScene):
    number = 7

    def construct(self):
        shape, collection = assumes_panels()
        # "It assumes less about the shape of a relationship."
        self.play(FadeIn(shape[0]), FadeIn(shape[1]), run_time=self.share(0.12))
        self.play(FadeIn(shape[2]), run_time=self.share(0.15))
        self.wait(max(self.share(0.42) - self.time, 0.01))
        # "But it assumes a lot about how the data were collected."
        self.play(FadeIn(collection[0]), FadeIn(collection[1]), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in collection[2]], lag_ratio=0.35),
                  run_time=self.share(0.35))
        self.finish()


# Rows are not observations (scenes 8–11, page results) ------------------------------------

def visit_squares(visits):
    """One square per visit, as rows of a spreadsheet and as stacks by site."""
    counts = sorted(visits["visits"].astype(int), reverse=True)
    size = 0.1
    total = sum(counts)
    squares = VGroup(*[Square(size, stroke_width=0, fill_color=BLUE, fill_opacity=1)
                       for _ in range(total)])
    grid = squares.copy().arrange_in_grid(rows=20, buff=0.06).move_to(0.3 * DOWN)

    stacks, i = VGroup(), 0
    for n in counts:
        stacks.add(VGroup(*[squares[i + k].copy() for k in range(n)]).arrange(UP, buff=0.02))
        i += n
    stacks.arrange_in_grid(rows=4, buff=(0.06, 0.35), cell_alignment=DOWN)
    stacks.scale_to_fit_width(12.6)
    if stacks.height > 5.4:
        stacks.scale_to_fit_height(5.4)
    stacks.move_to(0.5 * DOWN)
    return total, grid, stacks


class Scene08(VideoScene):
    number = 8

    def construct(self):
        total, grid, stacks = visit_squares(self.data("visits"))
        head = label(f"{total} visits", 48, INK, weight=BOLD).to_edge(UP, buff=0.6)
        self.play(FadeIn(head), run_time=self.share(0.2))
        self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.002), run_time=self.share(0.6))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        total, grid, stacks = visit_squares(self.data("visits"))
        head = label(f"{total} visits", 48, INK, weight=BOLD).to_edge(UP, buff=0.6)
        sites = label(f"from {len(stacks)} sites", 48, BLUE, weight=BOLD).to_edge(UP, buff=0.6)
        self.add(head, grid)
        flat = VGroup(*[sq for stack in stacks for sq in stack])
        # "But they come from 158 sites, visited again and again."
        self.play(Transform(grid, flat), run_time=self.share(0.45))
        self.play(FadeOut(head, shift=0.3 * UP), FadeIn(sites, shift=0.3 * UP), run_time=self.share(0.15))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        total, grid, stacks = visit_squares(self.data("visits"))
        sites = label(f"from {len(stacks)} sites", 48, BLUE, weight=BOLD).to_edge(UP, buff=0.6)
        self.add(sites, stacks)
        one = stacks[3]
        others = [s for s in stacks if s is not one]
        box = SurroundingRectangle(one, color=ORANGE, buff=0.08, stroke_width=4)
        name = label("one site: same rock, same currents", 30, ORANGE, weight=BOLD
                     ).next_to(box, DOWN, 0.25).shift(1.8 * RIGHT)
        # "Two visits to one site share its rock, its currents and its patch of animals."
        self.play(*[s.animate.set_opacity(0.2) for s in others], run_time=self.share(0.15))
        self.play(one.animate.set_fill(ORANGE), Create(box), FadeIn(name), run_time=self.share(0.2))
        # "They are not two separate pieces of evidence."
        self.play(one.animate.arrange(UP, buff=0).move_to(one), run_time=self.share(0.25))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        total, grid, stacks = visit_squares(self.data("visits"))
        effective = self.data("effective").iloc[0]
        worth = round(effective["effective"], -1)       # "about 550"
        self.add(stacks.set_opacity(0.25))
        value = ValueTracker(total)
        card = BackgroundRectangle(VGroup(Rectangle(width=6.4, height=3.2)), color=BACKGROUND,
                                   fill_opacity=0.92, buff=0).move_to(0.2 * UP)
        counter = always_redraw(lambda: label(f"{value.get_value():.0f}", 130, INK, weight=BOLD
                                              ).move_to(0.6 * UP))
        name = label("independent visits", 40, SUBDUED, weight=BOLD).move_to(0.9 * DOWN)
        self.play(FadeIn(card), FadeIn(counter), FadeIn(name), run_time=self.share(0.15))
        # "... worth about 550 independent ones."
        self.play(value.animate.set_value(worth), run_time=self.share(0.45))
        counter.clear_updaters()
        final = label(f"about {worth:.0f}", 130, BLUE, weight=BOLD).move_to(0.6 * UP)
        self.play(Transform(counter, final), run_time=self.share(0.15))
        self.finish()


# The cost in certainty (scenes 12–13, page results) ---------------------------------------

SE_NAMES = {"depth_m": "depth", "temperature_c": "temperature",
            "chlorophyll_mg_m3": "chlorophyll", "site_noise": "random site column"}


def se_layout(table):
    rows = table[table["term"].isin(SE_NAMES)].copy()
    rows["inflation"] = rows["cluster_se"] / rows["naive_se"]
    axis_x = lambda v: -2.2 + 2.6 * (v - 0)  # noqa: E731
    one = axis_x(1)
    head = label("honest standard error ÷ naive one", 32, SUBDUED).to_edge(UP, buff=0.7)
    ref = DashedLine([one, 2.3, 0], [one, -2.6, 0], dash_length=0.08, color=GREY, stroke_width=3)
    ref_name = label("1 × (naive)", 26, SUBDUED).next_to(ref, DOWN, 0.15)
    bars = {}
    for i, (_, r) in enumerate(rows.iterrows()):
        y = 1.6 - 1.1 * i
        name = label(SE_NAMES[r["term"]], 32).move_to([-2.5, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=axis_x(r["inflation"]) - axis_x(0), height=0.5, stroke_width=0,
                        fill_color=VERMILION if r["term"] == "chlorophyll_mg_m3" else BLUE,
                        fill_opacity=1).move_to([axis_x(0), y, 0], aligned_edge=LEFT)
        start = bar.copy().stretch_to_fit_width(one - axis_x(0)).move_to([axis_x(0), y, 0],
                                                                         aligned_edge=LEFT)
        value = label(f"{r['inflation']:.2f} ×", 30, bar.get_fill_color())
        value.move_to([max(bar.get_right()[0], one) + 0.25, y, 0], aligned_edge=LEFT)
        bars[r["term"]] = VGroup(name, start, bar, value)
    return rows.set_index("term"), VGroup(head, ref, ref_name), bars


class Scene12(VideoScene):
    number = 12

    def construct(self):
        rows, frame, bars = se_layout(self.data("cluster-se"))
        # "The cost is in certainty."
        self.play(FadeIn(frame), *[FadeIn(b[0]) for b in bars.values()],
                  *[GrowFromEdge(b[1], LEFT) for b in bars.values()], run_time=self.share(0.25))
        # "Chlorophyll's honest standard error is 2.77 times the naive one."
        self.play(*[Transform(b[1], b[2]) for b in bars.values()], run_time=self.share(0.3))
        self.play(*[FadeIn(b[3]) for b in bars.values()], run_time=self.share(0.1))
        self.play(Indicate(bars["chlorophyll_mg_m3"][3], color=VERMILION, scale_factor=1.4),
                  run_time=self.share(0.2))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        row = self.data("cluster-se").set_index("term").loc["site_noise"]
        head = label("A random number, one per site", 36, SUBDUED).to_edge(UP, buff=0.8)
        line = NumberLine(x_range=[0, 0.25, 0.05], length=10, color=GRID, include_numbers=False,
                          stroke_width=4).shift(0.5 * DOWN)
        ticks = VGroup(*[label(f"{v:.2f}", 26, SUBDUED).next_to(line.n2p(v), DOWN, 0.25)
                         for v in (0, 0.05, 0.1, 0.15, 0.2, 0.25)])
        name = label("p-value", 28, SUBDUED).next_to(ticks, DOWN, 0.3)
        cut = DashedLine(line.n2p(0.05) + 1.8 * UP, line.n2p(0.05), dash_length=0.08,
                         color=VERMILION, stroke_width=3)
        cut_name = label("significant", 26, VERMILION).next_to(cut, UP, 0.15).shift(0.9 * LEFT)
        dot = Dot(line.n2p(row["naive_p"]), radius=0.18, color=ORANGE)
        tag = label(f"naive: p = {row['naive_p']:.2f}", 32, ORANGE, weight=BOLD).next_to(dot, UP, 0.35)
        honest = label(f"honest: p = {row['cluster_p']:.2f}", 32, BLUE, weight=BOLD)
        self.play(FadeIn(head), FadeIn(line), FadeIn(ticks), FadeIn(name), Create(cut), FadeIn(cut_name),
                  run_time=self.share(0.15))
        # "... looked close to significant."
        self.play(FadeIn(dot, scale=2), FadeIn(tag), run_time=self.share(0.2))
        self.wait(max(self.share(0.5) - self.time, 0.01))
        # "Counted honestly, it was nowhere near."
        target = line.n2p(row["cluster_p"])
        self.play(dot.animate.move_to(target).set_color(BLUE),
                  Transform(tag, honest.next_to(target, UP, 0.35)), run_time=self.share(0.3))
        self.finish()


# Neighbours in the test set (scenes 14–21, page results) ----------------------------------

def shelf_map(sites, height=6.0, centre=ORIGIN):
    """Site positions on a map with the page's aspect (coord_quickmap at this latitude)."""
    lon, lat = sites["longitude"], sites["latitude"]
    squash = np.cos(np.radians(lat.mean()))
    scale = height / (lat.max() - lat.min())
    x = (lon - lon.mean()) * squash * scale
    y = (lat - lat.mean()) * scale
    points = [np.array([a, b, 0]) + centre for a, b in zip(x, y)]
    frame = SurroundingRectangle(VGroup(*[Dot(p) for p in points]), color=GRID, buff=0.35,
                                 stroke_width=3, corner_radius=0.1)
    return points, frame


def residual_colour(r):
    t = float(np.clip(r / 1.5, -1, 1))
    return interpolate_color(ManimColor("#E3E6E8"), ManimColor(BLUE if t < 0 else ORANGE), abs(t))


class Scene14(VideoScene):
    number = 14

    def construct(self):
        sites = self.data("site-residuals")
        points, frame = shelf_map(sites, centre=1.4 * LEFT + 0.3 * DOWN)
        dots = VGroup(*[Dot(p, radius=0.05 + 0.018 * v, color=residual_colour(r))
                        for p, r, v in zip(points, sites["residual"], sites["visits"])])
        head = label("Leftover error at each site", 34, SUBDUED).to_edge(UP, buff=0.4)
        key = VGroup(VGroup(Dot(radius=0.14, color=ORANGE), label("more than predicted", 28)
                            ).arrange(RIGHT, buff=0.2),
                     VGroup(Dot(radius=0.14, color=BLUE), label("fewer than predicted", 28)
                            ).arrange(RIGHT, buff=0.2)
                     ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(frame, RIGHT, 0.6)
        self.play(FadeIn(head), Create(frame), run_time=self.share(0.12))
        # "Even different sites are not independent."
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.01),
                  FadeIn(key), run_time=self.share(0.35))
        # "Stations close together tend to be wrong in the same way."
        warm = VGroup(*[d for d, r in zip(dots, sites["residual"]) if r > 0.8])
        cold = VGroup(*[d for d, r in zip(dots, sites["residual"]) if r < -0.8])
        self.play(Indicate(warm, color=ORANGE, scale_factor=1.5), run_time=self.share(0.2))
        self.play(Indicate(cold, color=BLUE, scale_factor=1.5), run_time=self.share(0.2))
        self.finish()


def neighbour_layout(scene):
    sites = scene.data("site-residuals")
    points, frame = shelf_map(sites, centre=1.4 * LEFT + 0.3 * DOWN)
    dots = VGroup(*[Dot(p, radius=0.08, color=GREY) for p in points])
    arr = np.array(points)
    held = int(np.argmin(np.linalg.norm(arr - arr.mean(axis=0), axis=1)))
    near = np.argsort(np.linalg.norm(arr - arr[held], axis=1))[1:6]
    key = VGroup(VGroup(Dot(radius=0.14, color=ORANGE), label("held out", 28)).arrange(RIGHT, buff=0.2),
                 VGroup(Dot(radius=0.14, color=BLUE), label("its neighbours, in training", 28)
                        ).arrange(RIGHT, buff=0.2)
                 ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(frame, RIGHT, 0.5)
    head = label("Ordinary cross-validation", 34, SUBDUED).to_edge(UP, buff=0.4)
    return head, frame, dots, held, near, key


class Scene15(VideoScene):
    number = 15

    def construct(self):
        head, frame, dots, held, near, key = neighbour_layout(self)
        self.play(FadeIn(head), Create(frame), FadeIn(dots), run_time=self.share(0.2))
        # "... holds out a station, ..."
        self.play(dots[held].animate.scale(2).set_color(ORANGE), FadeIn(key[0]), run_time=self.share(0.2))
        # "... and trains on its neighbours."
        self.play(*[dots[i].animate.scale(1.5).set_color(BLUE) for i in near], FadeIn(key[1]),
                  run_time=self.share(0.25))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        head, frame, dots, held, near, key = neighbour_layout(self)
        dots[held].scale(2).set_color(ORANGE)
        for i in near:
            dots[i].scale(1.5).set_color(BLUE)
        self.add(head, frame, dots, key)
        links = VGroup(*[Line(dots[held].get_center(), dots[i].get_center(), color=BLUE, stroke_width=4)
                         for i in near])
        note = label("just look up the neighbourhood", 32, BLUE, weight=BOLD).next_to(frame, DOWN, 0.25)
        # "So a model can score well just by looking up the neighbourhood."
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.2), run_time=self.share(0.35))
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def r2_bar(value, colour, x, scale, base_y, name):
    bar = Rectangle(width=1.4, height=max(value * scale, 0.02), stroke_width=0, fill_color=colour,
                    fill_opacity=1).move_to([x, base_y, 0], aligned_edge=DOWN)
    number_ = label(f"{value:.3f}", 32, colour, weight=BOLD).next_to(bar, UP, 0.15)
    caption = label(name, 26, SUBDUED).move_to([x, base_y - 0.45, 0])
    return VGroup(bar, number_, caption)


def coords_only_layout(scene):
    r2 = scene.data("cv-r2")
    only = r2[r2["model"] == "Coordinates only"].set_index("scheme")["r2"]
    sites = scene.data("site-residuals")
    points, frame = shelf_map(sites, height=5.0, centre=3.4 * LEFT + 0.4 * DOWN)
    dots = VGroup(*[Dot(p, radius=0.06, color=GREY) for p in points])
    head = label("A forest given only longitude and latitude", 34, SUBDUED).to_edge(UP, buff=0.4)
    base_y, scale = -2.6, 45
    base = Line([1.2, base_y, 0], [6.2, base_y, 0], color=GRID, stroke_width=3)
    name = label("R² on held-out stations", 28, SUBDUED).move_to([3.7, 2.4, 0])
    random = r2_bar(only["Random 10-fold"], BLUE, 2.6, scale, base_y, "random folds")
    blocked = r2_bar(only["Spatial block"], ORANGE, 4.8, scale, base_y, "blocked folds")

    x0, y0, _ = frame.get_corner(DL)
    w, h = frame.width / 3, frame.height / 3
    cells = VGroup(*[Rectangle(width=w, height=h, stroke_color=ORANGE, stroke_width=3)
                     .move_to([x0 + w * (i + 0.5), y0 + h * (j + 0.5), 0])
                     for j in range(3) for i in range(3)])
    return head, VGroup(frame, dots), VGroup(base, name), random, blocked, cells


class Scene17(VideoScene):
    number = 17

    def construct(self):
        head, shelf, axis, random, blocked, cells = coords_only_layout(self)
        # "A forest given nothing but longitude and latitude ..."
        self.play(FadeIn(head), FadeIn(shelf), run_time=self.share(0.25))
        # "... scores an R² of 0.075."
        self.play(FadeIn(axis), GrowFromEdge(random[0], DOWN), FadeIn(random[2]), run_time=self.share(0.3))
        self.play(FadeIn(random[1], shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        head, shelf, axis, random, blocked, cells = coords_only_layout(self)
        self.add(head, shelf, axis, random)
        # "Hold out whole blocks of the shelf instead, ..."
        self.play(Create(cells), run_time=self.share(0.25))
        self.play(cells[4].animate.set_fill(ORANGE, 0.3), run_time=self.share(0.1))
        # "... and it falls to 0.011."
        self.play(GrowFromEdge(blocked[0], DOWN), FadeIn(blocked[2]), run_time=self.share(0.2))
        self.play(FadeIn(blocked[1], shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def coords_gain_layout(scene):
    r2 = scene.data("cv-r2").set_index(["model", "scheme"])["r2"]
    base_y, scale = -2.3, 16
    base = Line([-6, base_y, 0], [6, base_y, 0], color=GRID, stroke_width=3)
    head = label("Adding position to a model of the environment", 34, SUBDUED).to_edge(UP, buff=0.5)
    sub = label("R² on held-out stations", 28, SUBDUED).next_to(head, DOWN, 0.15)
    groups = {}
    for scheme, x, colour in (("Random 10-fold", -3.0, BLUE), ("Spatial block", 3.0, ORANGE)):
        env = r2_bar(r2[("Environment only", scheme)], GREY, x - 1.0, scale, base_y, "environment")
        both = r2_bar(r2[("Environment + coordinates", scheme)], colour, x + 1.0, scale, base_y,
                      "+ position")
        gain = r2[("Environment + coordinates", scheme)] / r2[("Environment only", scheme)] - 1
        tag = label(f"+{percent(gain)}", 44, colour, weight=BOLD).move_to([x, 1.9, 0])
        name = label("random folds" if scheme.startswith("Random") else "blocked folds", 32, colour,
                     weight=BOLD).move_to([x, base_y - 1.0, 0])
        groups[scheme] = VGroup(env, both, tag, name)
    return VGroup(base, head, sub), groups


class Scene19(VideoScene):
    number = 19

    def construct(self):
        frame, groups = coords_gain_layout(self)
        env, both, tag, name = groups["Random 10-fold"]
        # "Now add position to a model of the environment."
        self.play(FadeIn(frame), FadeIn(name), GrowFromEdge(env[0], DOWN), FadeIn(env[1:]),
                  run_time=self.share(0.25))
        self.play(GrowFromEdge(both[0], DOWN), FadeIn(both[1:]), run_time=self.share(0.2))
        # "Random folds say it helps by 29%."
        self.play(FadeIn(tag, scale=1.4), run_time=self.share(0.15))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        frame, groups = coords_gain_layout(self)
        self.add(frame, groups["Random 10-fold"])
        env, both, tag, name = groups["Spatial block"]
        # "Blocked folds say 11%."
        self.play(FadeIn(name), GrowFromEdge(env[0], DOWN), FadeIn(env[1:]),
                  GrowFromEdge(both[0], DOWN), FadeIn(both[1:]), run_time=self.share(0.2))
        self.play(FadeIn(tag, scale=1.4), run_time=self.share(0.1))
        # "Most of the gain was the validation scheme flattering itself."
        self.play(Indicate(groups["Random 10-fold"][2], color=BLUE, scale_factor=1.3),
                  run_time=self.share(0.25))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        frame, groups = coords_gain_layout(self)
        self.add(frame, *groups.values())
        trap = label("the trap", 64, VERMILION, weight=BOLD).move_to(0.4 * UP)
        later = label("→ model validation", 40, GREEN, weight=BOLD).next_to(trap, DOWN, 0.5)
        # "This is the trap in this section."
        self.play(*[g.animate.set_opacity(0.2) for g in groups.values()], frame[0].animate.set_opacity(0.2),
                  FadeIn(trap, scale=1.3), run_time=self.share(0.2))
        self.wait(self.share(0.2))
        # "The validation section shows how to test honestly."
        self.play(FadeIn(later, shift=0.2 * LEFT), run_time=self.share(0.15))
        self.finish()


class Scene22(KeyPointScene):
    number, point = 22, 1


# A better fit, a wrong answer (scenes 23–28) ----------------------------------------------

class Scene23(VideoScene):
    number = 23

    def construct(self):
        axes = plain_axes([0, 10, 1], [0, 1.2, 1], 9, 4.6).shift(0.4 * DOWN)
        xl = label("temperature or depth", 28, SUBDUED).next_to(axes, DOWN, 0.3)
        yl = label("how many", 28, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.3)
        hump = axes.plot(lambda x: np.exp(-((x - 5) / 2.0) ** 2), x_range=[0, 10], color=BLUE,
                         stroke_width=7)
        best = DashedLine(axes.c2p(5, 0), axes.c2p(5, 1.05), dash_length=0.08, color=INK)
        best_name = label("best", 30, INK, weight=BOLD).next_to(best, UP, 0.1)
        line = axes.plot(lambda x: 0.35 + 0.02 * x, x_range=[0, 10], color=GREY, stroke_width=5)
        line_name = label("a straight line", 28, GREY).next_to(axes.c2p(10, 0.55), LEFT, 0.1)
        # "Species have a best temperature and a best depth."
        self.play(FadeIn(axes), FadeIn(xl), FadeIn(yl), run_time=self.share(0.1))
        self.play(Create(hump), run_time=self.share(0.3))
        self.play(Create(best), FadeIn(best_name), run_time=self.share(0.12))
        # "The response is a hump, not a straight line."
        self.play(Create(line), FadeIn(line_name), run_time=self.share(0.15))
        cross = Cross(line_name, stroke_color=VERMILION, stroke_width=5)
        self.play(Create(cross), line.animate.set_opacity(0.3), run_time=self.share(0.1))
        self.finish()


def recovery_panel(table, column, x_name, unit, centre, truth_optimum):
    xs, fitted, truth = table[column], table["fitted"], table["truth"]
    lo = min(fitted.min(), truth.min())
    hi = max(fitted.max(), truth.max())
    axes = plain_axes([xs.min(), xs.max(), 1], [lo, hi, 1], 5.4, 3.6).move_to(centre)
    fit_line = polyline(axes, xs, fitted, BLUE, 6)
    true_line = polyline(axes, xs, truth, INK, 5, dashed=True)
    name = label(x_name, 30, SUBDUED).next_to(axes, DOWN, 0.3)
    best = xs[fitted.idxmax()]
    fit_mark = DashedLine(axes.c2p(best, lo), axes.c2p(best, hi), dash_length=0.06, color=BLUE)
    true_mark = DashedLine(axes.c2p(truth_optimum, lo), axes.c2p(truth_optimum, hi),
                           dash_length=0.06, color=INK)
    digits = 1 if unit == "°C" else 0
    fit_tag = label(f"fitted: {best:.{digits}f} {unit}", 28, BLUE, weight=BOLD)
    true_tag = label(f"truth: {truth_optimum} {unit}", 28, INK, weight=BOLD)
    tags = VGroup(fit_tag, true_tag).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(axes, UP, 0.3)
    return VGroup(axes, name), fit_line, true_line, VGroup(fit_mark, true_mark), tags


def recovery_layout(scene):
    temperature = recovery_panel(scene.data("temperature-curves"), "temperature_c", "temperature (°C)",
                                 "°C", 3.4 * LEFT + 0.7 * DOWN, 9)
    depth = recovery_panel(scene.data("depth-curves"), "depth_m", "depth (m)", "m",
                           3.4 * RIGHT + 0.7 * DOWN, 80)
    key = VGroup(VGroup(Line(ORIGIN, 0.6 * RIGHT, color=BLUE, stroke_width=6), label("fitted", 26)
                        ).arrange(RIGHT, buff=0.15),
                 VGroup(DashedLine(ORIGIN, 0.6 * RIGHT, color=INK, stroke_width=5), label("truth", 26)
                        ).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.3)
    return temperature, depth, key


class Scene24(VideoScene):
    number = 24

    def construct(self):
        temperature, depth, key = recovery_layout(self)
        frame, fit_line, true_line, marks, tags = temperature
        self.play(FadeIn(frame), FadeIn(key), run_time=self.share(0.1))
        self.play(Create(true_line), run_time=self.share(0.2))
        # "A flexible model finds the best temperature: ..."
        self.play(Create(fit_line), run_time=self.share(0.25))
        # "... 9.3 degrees, where the truth is 9."
        self.play(Create(marks), FadeIn(tags), run_time=self.share(0.2))
        self.finish()


class Scene25(VideoScene):
    number = 25

    def construct(self):
        temperature, depth, key = recovery_layout(self)
        self.add(*temperature, key)
        frame, fit_line, true_line, marks, tags = depth
        # "Same model, same data."
        self.play(FadeIn(frame), Create(true_line), run_time=self.share(0.2))
        self.play(Create(fit_line), run_time=self.share(0.2))
        # "It puts the best depth at 15 metres. The truth is 80."
        self.play(Create(marks[0]), FadeIn(tags[0]), run_time=self.share(0.15))
        self.play(Create(marks[1]), FadeIn(tags[1]), run_time=self.share(0.15))
        self.play(Indicate(tags[0], color=VERMILION), run_time=self.share(0.15))
        self.finish()


def tangle():
    depth = VGroup(Circle(0.9, color=VERMILION, stroke_width=5), label("depth", 36, VERMILION, weight=BOLD))
    others = []
    for text, position in (("temperature", [-4.2, 1.8, 0]), ("food", [4.2, 1.8, 0]),
                           ("position", [0, -2.6, 0])):
        others.append(VGroup(Circle(0.9, color=BLUE, stroke_width=4), label(text, 28, BLUE, weight=BOLD)
                             ).move_to(position))
    depth.move_to(0.1 * UP)
    links = VGroup(*[Line(depth[0].get_center(), o[0].get_center(), color=GRID, stroke_width=5,
                          buff=0.95) for o in others])
    return depth, VGroup(*others), links


class Scene26(VideoScene):
    number = 26

    def construct(self):
        depth, others, links = tangle()
        # "The difference is not the method."
        self.play(FadeIn(depth, scale=0.8), run_time=self.share(0.2))
        self.wait(max(self.share(0.35) - self.time, 0.01))
        # "Depth is tangled up with temperature, food and position."
        for link, other in zip(links, others):
            self.play(Create(link), FadeIn(other), run_time=self.share(0.14))
        self.finish()


class Scene27(VideoScene):
    number = 27

    def construct(self):
        depth, others, links = tangle()
        self.add(depth, others, links)
        curve = FunctionGraph(lambda x: 0.6 * np.sin(2.2 * x) * np.exp(-0.2 * x * x), x_range=[-2, 2],
                              color=INK, stroke_width=6).move_to(3.0 * UP)
        # "Flexibility lets a model draw any shape."
        self.play(Create(curve), run_time=self.share(0.25))
        # "It cannot tell which variable the shape belongs to."
        mark = label("?", 44, VERMILION, weight=BOLD)
        for node in [depth, *others]:
            arrow = Arrow(curve.get_bottom(), node.get_top(), color=VERMILION, stroke_width=4, buff=0.15)
            self.play(GrowArrow(arrow), FadeIn(mark.copy().next_to(arrow.get_center(), RIGHT, 0.1)),
                      run_time=self.share(0.1))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        aic = self.data("aic")
        head = label("How well each model fits the survey", 34, SUBDUED).to_edge(UP, buff=0.8)
        sub = label("AIC: lower is better", 28, SUBDUED).next_to(head, DOWN, 0.15)
        cards = VGroup()
        for _, r in aic.iterrows():
            best = r["aic"] == aic["aic"].min()
            colour = BLUE if best else GREY
            box = RoundedRectangle(width=3.6, height=2.2, corner_radius=0.15, stroke_color=colour,
                                   stroke_width=6 if best else 3)
            text = VGroup(label(r["model"], 30, colour, weight=BOLD), label(f"{r['aic']:.0f}", 44, colour)
                          ).arrange(DOWN, buff=0.3).move_to(box)
            cards.add(VGroup(box, text))
        cards.arrange(RIGHT, buff=0.6).shift(0.3 * DOWN)
        ribbon = label("best fit", 34, BLUE, weight=BOLD).next_to(cards[-1], DOWN, 0.35)
        wrong = label("and the most wrong depth curve", 30, VERMILION, weight=BOLD).next_to(ribbon, DOWN, 0.2)
        self.play(FadeIn(head), FadeIn(sub), run_time=self.share(0.12))
        # "And of three models, this one fitted the data best."
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cards], lag_ratio=0.3),
                  run_time=self.share(0.4))
        self.play(FadeIn(ribbon, scale=1.2), run_time=self.share(0.12))
        self.play(FadeIn(wrong), run_time=self.share(0.15))
        self.finish()


# Wrong about the spread (scenes 29–34) ----------------------------------------------------

def spread_layout(width_scale):
    # Schematic counts around one average; only the ratio shown in scene 30 is a result.
    rng = np.random.default_rng(29)
    centre_y = 0.0
    base = 0.55
    axis = Line(6 * LEFT, 6 * RIGHT, color=GRID, stroke_width=3).shift(centre_y * UP)
    mean_name = label("average", 26, SUBDUED).next_to(axis, RIGHT, 0.1).shift(0.3 * LEFT + 0.3 * UP)
    band = Rectangle(width=11.4, height=2 * base * width_scale, stroke_width=0, fill_color=BLUE,
                     fill_opacity=0.18).move_to(axis)
    xs = np.linspace(-5.5, 5.5, 44)
    dots = VGroup(*[Dot([x, centre_y + y, 0], radius=0.08, color=INK)
                    for x, y in zip(xs, rng.normal(0, base * width_scale * 0.9, len(xs)))])
    return axis, mean_name, band, dots


class Scene29(VideoScene):
    number = 29

    def construct(self):
        axis, mean_name, band, dots = spread_layout(1.0)
        head = label("A Poisson model's claim", 36, SUBDUED).to_edge(UP, buff=0.7)
        claim = label("variance = average", 44, BLUE, weight=BOLD).next_to(head, DOWN, 0.3)
        band_name = label("the spread Poisson allows", 28, BLUE).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(head), Create(axis), FadeIn(mean_name), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), run_time=self.share(0.3))
        # "... the variance of the counts equals their average."
        self.play(FadeIn(band), FadeIn(band_name), FadeIn(claim, shift=0.2 * DOWN), run_time=self.share(0.25))
        self.finish()


class Scene30(VideoScene):
    number = 30

    def construct(self):
        ratio = self.data("dispersion")["dispersion"].iloc[0]
        axis, mean_name, band, dots = spread_layout(1.0)
        wide_axis, _, wide_band, wide_dots = spread_layout(np.sqrt(ratio))
        head = label("A Poisson model's claim", 36, SUBDUED).to_edge(UP, buff=0.7)
        claim = label("variance = average", 44, BLUE, weight=BOLD).next_to(head, DOWN, 0.3)
        actual = label(f"variance = {ratio:.1f} × average", 44, VERMILION, weight=BOLD).move_to(claim)
        self.add(axis, mean_name, band, dots, head, claim)
        # "Here the variance is nearly four times larger."
        self.play(Transform(dots, wide_dots), run_time=self.share(0.3))
        self.play(Transform(claim, actual), run_time=self.share(0.15))
        # "Animals gather in groups."
        groups = label("animals gather in groups", 30, SUBDUED).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(groups), run_time=self.share(0.15))
        self.finish()


def zeros_layout(scene):
    sims = scene.data("simulated-zeros")
    poisson = sims[sims["model"] == "Poisson"]["zeros"]
    info = scene.data("dispersion").iloc[0]
    axes = plain_axes([40, 180, 20], [0, 1, 1], 11, 4.4).shift(0.5 * DOWN)
    ticks = VGroup(*[label(str(v), 26, SUBDUED).next_to(axes.c2p(v, 0), DOWN, 0.2)
                     for v in range(40, 181, 20)])
    name = label("empty stations in a survey", 28, SUBDUED).next_to(ticks, DOWN, 0.25)
    counts, edges = np.histogram(poisson, bins=np.arange(40, 181, 2))
    top = counts.max()
    bars = VGroup(*[Rectangle(width=axes.x_length * 2 / 140 * 0.9, height=max(c / top * 4.0, 0.001),
                              stroke_width=0, fill_color=BLUE, fill_opacity=1)
                    .move_to(axes.c2p(e + 1, 0), aligned_edge=DOWN)
                    for c, e in zip(counts, edges[:-1]) if c > 0])
    label_sim = label(f"{len(poisson)} surveys from the Poisson model: about {info['poisson_zeros']:.0f}",
                      30, BLUE, weight=BOLD).to_edge(UP, buff=0.6)
    real = DashedLine(axes.c2p(info["observed_zeros"], 0), axes.c2p(info["observed_zeros"], 1) + 0.4 * UP,
                      dash_length=0.1, color=VERMILION, stroke_width=5)
    real_name = label(f"real survey: {info['observed_zeros']:.0f}", 34, VERMILION, weight=BOLD
                      ).next_to(real, UP, 0.15)
    return VGroup(axes, ticks, name), bars, label_sim, VGroup(real, real_name)


class Scene31(VideoScene):
    number = 31

    def construct(self):
        frame, bars, label_sim, real = zeros_layout(self)
        self.play(FadeIn(frame), run_time=self.share(0.15))
        # "Simulate surveys from the Poisson model, ..."
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=self.share(0.4))
        # "... and they have about 68 empty stations."
        self.play(FadeIn(label_sim), run_time=self.share(0.15))
        self.finish()


class Scene32(VideoScene):
    number = 32

    def construct(self):
        frame, bars, label_sim, real = zeros_layout(self)
        self.add(frame, bars, label_sim)
        # "The real survey has 159."
        self.play(Create(real[0]), FadeIn(real[1]), run_time=self.share(0.25))
        # "That model could not have made these data."
        gap = DoubleArrow(bars.get_right() + 0.3 * RIGHT + 0.6 * UP, real[0].get_center() + 0.6 * UP + 0.1 * LEFT,
                          color=VERMILION, stroke_width=4, buff=0)
        self.play(GrowFromCenter(gap), run_time=self.share(0.2))
        self.finish()


def poisson_se_layout(scene):
    table = scene.data("poisson-se")
    ratio = (table["nb_se"] / table["poisson_se"]).mean()
    base_y = -2.4
    base = Line([-4.5, base_y, 0], [4.5, base_y, 0], color=GRID, stroke_width=3)
    head = label("Standard errors, on average across terms", 32, SUBDUED).to_edge(UP, buff=0.6)
    right = Rectangle(width=2.2, height=4.4, stroke_width=0, fill_color=GREEN, fill_opacity=1
                      ).move_to([1.8, base_y, 0], aligned_edge=DOWN)
    poisson = Rectangle(width=2.2, height=4.4 / ratio, stroke_width=0, fill_color=VERMILION, fill_opacity=1
                        ).move_to([-1.8, base_y, 0], aligned_edge=DOWN)
    names = VGroup(label("Poisson", 30, VERMILION, weight=BOLD).next_to(poisson, DOWN, 0.4),
                   label("the right model", 30, GREEN, weight=BOLD).next_to(right, DOWN, 0.4))
    names[1].align_to(names[0], DOWN)
    tag = label(f"{ratio:.1f} × larger", 36, GREEN, weight=BOLD).next_to(right, UP, 0.2)
    depth = table.iloc[1]          # the linear depth term
    return VGroup(base, head), poisson, right, names, tag, depth


class Scene33(VideoScene):
    number = 33

    def construct(self):
        frame, poisson, right, names, tag, depth = poisson_se_layout(self)
        self.play(FadeIn(frame), run_time=self.share(0.1))
        # "Its standard errors were about half the right size."
        self.play(GrowFromEdge(poisson, DOWN), FadeIn(names[0]), run_time=self.share(0.25))
        self.play(GrowFromEdge(right, DOWN), FadeIn(names[1]), run_time=self.share(0.25))
        self.play(FadeIn(tag), run_time=self.share(0.1))
        self.finish()


class Scene34(VideoScene):
    number = 34

    def construct(self):
        depth = self.data("poisson-se").iloc[1]
        head = label("Does depth matter?", 36, SUBDUED).to_edge(UP, buff=0.8)
        line = NumberLine(x_range=[-4, 0, 1], length=10, color=GRID, stroke_width=4).shift(0.5 * DOWN)
        ticks = VGroup(*[label(t, 26, SUBDUED).next_to(line.n2p(v), DOWN, 0.25)
                         for v, t in ((-4, "0.0001"), (-3, "0.001"), (-2, "0.01"), (-1, "0.1"), (0, "1"))])
        name = label("p-value (log scale)", 28, SUBDUED).next_to(ticks, DOWN, 0.3)
        cut = DashedLine(line.n2p(np.log10(0.05)) + 1.8 * UP, line.n2p(np.log10(0.05)),
                         dash_length=0.08, color=GREY, stroke_width=3)
        cut_name = label("0.05", 26, SUBDUED).next_to(cut, UP, 0.15)
        start = line.n2p(max(np.log10(depth["poisson_p"]), -4))
        end = line.n2p(np.log10(depth["nb_p"]))
        dot = Dot(start, radius=0.18, color=VERMILION)
        tag = label("Poisson: highly significant", 32, VERMILION, weight=BOLD).next_to(dot, UP, 0.35)
        tag.shift((1.2 - tag.get_left()[0] + start[0]) * RIGHT)
        honest = label(f"right model: p = {depth['nb_p']:.2f}", 32, GREEN, weight=BOLD).next_to(end, UP, 0.35)
        self.play(FadeIn(head), FadeIn(line), FadeIn(ticks), FadeIn(name), Create(cut), FadeIn(cut_name),
                  run_time=self.share(0.15))
        # "So depth looked highly significant."
        self.play(FadeIn(dot, scale=2), FadeIn(tag), run_time=self.share(0.2))
        self.wait(max(self.share(0.45) - self.time, 0.01))
        # "With the right model, it was not."
        self.play(dot.animate.move_to(end).set_color(GREEN), Transform(tag, honest), run_time=self.share(0.3))
        self.finish()


class Scene35(KeyPointScene):
    number, point = 35, 2


# Past the edge of the data (scenes 36–42) -------------------------------------------------

class Scene36(VideoScene):
    number = 36

    def construct(self):
        coast = VMobject(color=INK, stroke_width=6).set_points_smoothly(
            [[-6.2, 3.2, 0], [-5.2, 1.6, 0], [-5.6, 0.2, 0], [-4.8, -1.3, 0], [-5.3, -3.2, 0]])
        port = VGroup(Square(0.4, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([-4.9, 0.3, 0]),
                      label("port", 28, INK, weight=BOLD).move_to([-5.9, 0.9, 0]))
        rng = np.random.default_rng(36)
        near = VGroup(*[Dot([-4.3 + abs(rng.normal(0, 1.1)), rng.normal(0.3, 1.0), 0], radius=0.08,
                            color=BLUE) for _ in range(70)])
        empty = DashedVMobject(RoundedRectangle(width=4.6, height=5.2, corner_radius=0.3, color=GREY,
                                                stroke_width=3).move_to([3.4, -0.2, 0]), num_dashes=50)
        never = label("never sampled", 34, GREY, weight=BOLD).move_to(empty)
        # "Survey effort follows ports and weather."
        self.play(Create(coast), FadeIn(port), run_time=self.share(0.2))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in near], lag_ratio=0.02), run_time=self.share(0.3))
        # "Some water is never sampled at all."
        self.play(Create(empty), FadeIn(never), run_time=self.share(0.25))
        self.finish()


BAND_ORDER = ["[0,40]", "(40,70]", "(70,100]", "(100,120]", "(120,140]", "(140,160]", "(160,200]"]
BAND_NAMES = ["0–40", "40–70", "70–100", "100–120", "120–140", "140–160", "160–200"]


def depth_bands_layout(scene):
    bands = scene.data("depth-bands").pivot(index="band", columns="series", values="mean_count")
    bands = bands.loc[BAND_ORDER]
    axes = plain_axes([0, 6, 1], [0, 8, 2], 10.5, 4.6).shift(0.2 * DOWN + 0.4 * RIGHT)
    xs = np.arange(7)
    ticks = VGroup(*[label(n, 22, SUBDUED).next_to(axes.c2p(x, 0), DOWN, 0.2) for x, n in zip(xs, BAND_NAMES)])
    y_ticks = VGroup(*[label(str(v), 24, SUBDUED).next_to(axes.c2p(0, v), LEFT, 0.2) for v in (0, 2, 4, 6, 8)])
    x_name = label("depth band (m)", 28, SUBDUED).next_to(ticks, DOWN, 0.2)
    y_name = label("mean count", 28, SUBDUED).rotate(PI / 2).next_to(y_ticks, LEFT, 0.2)
    edge = axes.c2p(2.5, 0)[0]
    shade = Rectangle(width=edge - axes.c2p(-0.3, 0)[0], height=4.6, stroke_width=0, fill_color=BLUE,
                      fill_opacity=0.1).move_to(axes.c2p(-0.3, 0), aligned_edge=DL)
    shade_name = label("trained here", 28, BLUE, weight=BOLD).next_to(shade.get_top(), DOWN, 0.2)
    past_name = label("asked about here", 28, SUBDUED, weight=BOLD).move_to(
        [(edge + axes.c2p(6, 0)[0]) / 2, shade_name.get_y(), 0])

    def trace(column, colour, width):
        line = polyline(axes, xs, bands[column], colour, width)
        dots = VGroup(*[Dot(axes.c2p(x, v), radius=0.08, color=colour) for x, v in zip(xs, bands[column])])
        return VGroup(line, dots)

    truth = trace("Truth", INK, 8)
    forest = trace("Random forest", VERMILION, 6)
    truth_name = label("truth", 30, INK, weight=BOLD).next_to(truth[1][-1], DOWN, 0.2)
    forest_name = label("random forest", 30, VERMILION, weight=BOLD).next_to(forest[1][4], UP, 0.35)
    frame = VGroup(axes, ticks, y_ticks, x_name, y_name)
    return bands, frame, VGroup(shade, shade_name, past_name), truth, truth_name, forest, forest_name


class Scene37(VideoScene):
    number = 37

    def construct(self):
        bands, frame, shade, truth, truth_name, forest, forest_name = depth_bands_layout(self)
        self.play(FadeIn(frame), run_time=self.share(0.12))
        # "So train a model only on water shallower than 100 metres, ..."
        self.play(FadeIn(shade[0]), FadeIn(shade[1]), run_time=self.share(0.2))
        self.play(Create(truth[0]), FadeIn(truth[1]), FadeIn(truth_name), run_time=self.share(0.3))
        # "... and ask it about deeper water."
        self.play(FadeIn(shade[2]), run_time=self.share(0.12))
        self.finish()


class Scene38(VideoScene):
    number = 38

    def construct(self):
        bands, frame, shade, truth, truth_name, forest, forest_name = depth_bands_layout(self)
        self.add(frame, shade, truth, truth_name)
        # "A random forest cannot follow the decline."
        self.play(Create(forest[0]), FadeIn(forest[1]), run_time=self.share(0.4))
        self.play(FadeIn(forest_name), run_time=self.share(0.1))
        # "It repeats the last thing it saw."
        self.play(Indicate(VGroup(*forest[1][3:]), color=VERMILION, scale_factor=1.4), run_time=self.share(0.25))
        self.finish()


class Scene39(VideoScene):
    number = 39

    def construct(self):
        bands, frame, shade, truth, truth_name, forest, forest_name = depth_bands_layout(self)
        self.add(frame, shade, truth, truth_name, forest, forest_name)
        last = bands.iloc[-1]
        true_tag = label(f"{last['Truth']:.2f}", 34, INK, weight=BOLD).next_to(truth[1][-1], LEFT, 0.25)
        forest_tag = label(f"{last['Random forest']:.2f}", 34, VERMILION, weight=BOLD
                           ).next_to(forest[1][-1], DOWN, 0.25)
        # "In the deepest water, the truth is about one animal."
        self.play(FadeOut(truth_name), FadeIn(true_tag), Flash(truth[1][-1], color=INK), run_time=self.share(0.3))
        self.wait(max(self.share(0.55) - self.time, 0.01))
        # "The forest says nearly five."
        self.play(FadeIn(forest_tag), Flash(forest[1][-1], color=VERMILION), run_time=self.share(0.25))
        self.finish()


class Scene40(VideoScene):
    number = 40

    def construct(self):
        forest = self.data("bias").set_index("model").loc["Random forest"]
        base_y = -2.4
        base = Line([-4.5, base_y, 0], [4.5, base_y, 0], color=GRID, stroke_width=3)
        head = label("Random forest: how far too high, on average", 32, SUBDUED).to_edge(UP, buff=0.5)
        scale = 4.4 / forest["extrapolated"]
        bars = VGroup()
        for x, value, colour, name in ((-1.8, forest["in_range"], BLUE, "in range"),
                                       (1.8, forest["extrapolated"], VERMILION, "past the edge")):
            bar = Rectangle(width=2.2, height=value * scale, stroke_width=0, fill_color=colour,
                            fill_opacity=1).move_to([x, base_y, 0], aligned_edge=DOWN)
            tag = label(f"+{percent(value)}", 40, colour, weight=BOLD).next_to(bar, UP, 0.2)
            caption = label(name, 30, SUBDUED).move_to([x, base_y - 0.45, 0])
            bars.add(VGroup(bar, tag, caption))
        warning = label("no warning", 34, VERMILION, weight=BOLD).next_to(bars[1], LEFT, 0.4).shift(0.8 * UP)
        self.play(FadeIn(base), FadeIn(head), run_time=self.share(0.1))
        self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), run_time=self.share(0.15))
        # "Past the edge, its predictions are 73% too high on average, ..."
        self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), run_time=self.share(0.3))
        # "... with no warning at all."
        self.play(FadeIn(warning), run_time=self.share(0.12))
        self.finish()


NOVELTY_COLOURS = {"Surveyed": "#C9CED2", "Covered": SKY, "Outside a range": BLUE,
                   "Inside every range, but novel": ORANGE}


def novelty_layout(scene):
    stations = scene.data("novelty")
    temp = stations["temperature_c"]
    chl = np.log10(stations["chlorophyll_mg_m3"])
    axes = plain_axes([np.floor(temp.min()), np.ceil(temp.max()), 2], [chl.min(), chl.max(), 1], 8.0, 5.0
                      ).shift(0.3 * DOWN + 1.6 * LEFT)
    x_name = label("temperature (°C)", 28, SUBDUED).next_to(axes, DOWN, 0.25)
    y_name = label("chlorophyll (log scale)", 28, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.25)
    dots = {}
    for status in NOVELTY_COLOURS:
        rows = stations["status"] == status
        dots[status] = VGroup(*[Dot(axes.c2p(t, c), radius=0.05, color=NOVELTY_COLOURS[status])
                                for t, c in zip(temp[rows], chl[rows])])
    surveyed = stations["status"] == "Surveyed"
    corner = axes.c2p(temp[surveyed].min(), chl[surveyed].min())
    far = axes.c2p(temp[surveyed].max(), chl[surveyed].max())
    box = DashedVMobject(Rectangle(width=far[0] - corner[0], height=far[1] - corner[1], color=INK,
                                   stroke_width=3).move_to((corner + far) / 2), num_dashes=70)
    box_name = label("each variable's surveyed range", 26, INK).next_to(box, UP, 0.1)
    box_name.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.05)
    head = label("Cold water, high chlorophyll: never together", 34, SUBDUED).to_edge(UP, buff=0.3)
    to_predict = stations[~surveyed]
    share = (to_predict["status"] == "Inside every range, but novel").mean()
    return VGroup(axes, x_name, y_name), dots, VGroup(box, box_name), head, share


class Scene41(VideoScene):
    number = 41

    def construct(self):
        frame, dots, box, head, share = novelty_layout(self)
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.1))
        self.play(FadeIn(dots["Surveyed"]), run_time=self.share(0.2))
        # "Checking each variable's range is not enough."
        self.play(Create(box[0]), FadeIn(box[1]), run_time=self.share(0.2))
        # "The survey saw cold water, and it saw high chlorophyll, but never the two together."
        corner = Circle(0.9, color=ORANGE, stroke_width=5).move_to(box[0].get_corner(UL) + 0.8 * RIGHT + 0.6 * DOWN)
        self.play(Create(corner), run_time=self.share(0.2))
        self.finish()


class Scene42(VideoScene):
    number = 42

    def construct(self):
        frame, dots, box, head, share = novelty_layout(self)
        self.add(frame, dots["Surveyed"], box, head)
        tag = label(percent(share), 72, ORANGE, weight=BOLD)
        sub = VGroup(*[label(t, 28, ORANGE) for t in ("of the stations to predict:", "inside every range,",
                                                     "outside the survey")]).arrange(DOWN, buff=0.1)
        note = VGroup(tag, sub).arrange(DOWN, buff=0.2).move_to([4.7, 0, 0])
        # "40% of the stations to predict passed every single range check, ..."
        self.play(FadeIn(dots["Covered"]), FadeIn(dots["Outside a range"]), run_time=self.share(0.15))
        self.play(FadeIn(dots["Inside every range, but novel"], scale=1.5), run_time=self.share(0.25))
        # "... and still lay outside the survey."
        self.play(FadeIn(note), run_time=self.share(0.15))
        self.finish()


# The puzzle, solved (scenes 43–48, page results) ------------------------------------------

def prevalence_grid(scene):
    probabilities = scene.data("probabilities")
    prevalence = (probabilities["rare_species"] == "yes").mean()
    present = round(100 * prevalence)
    cells = VGroup(*[Square(0.46, stroke_width=0, fill_color="#D5DCE1", fill_opacity=1) for _ in range(100)])
    cells.arrange_in_grid(rows=10, buff=0.1).move_to(2.6 * LEFT + 0.3 * DOWN)
    rng = np.random.default_rng(43)
    chosen = sorted(rng.choice(100, present, replace=False))
    head = label(f"The rare species: at {percent(prevalence)} of stations", 34, SUBDUED).to_edge(UP, buff=0.35)
    return cells, chosen, head


class Scene43(VideoScene):
    number = 43

    def construct(self):
        cells, chosen, head = prevalence_grid(self)
        self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01),
                  run_time=self.share(0.35))
        # "It is found at 5% of stations."
        self.play(*[cells[i].animate.set_fill(ORANGE) for i in chosen], run_time=self.share(0.25))
        self.finish()


class Scene44(VideoScene):
    number = 44

    def construct(self):
        cells, chosen, head = prevalence_grid(self)
        for i in chosen:
            cells[i].set_fill(ORANGE)
        self.add(head, cells)
        accuracy = self.data("imbalance-metrics").set_index("recipe").loc["Untouched", "accuracy"]
        rule = label("Always say \"no\"", 44, INK, weight=BOLD).move_to([3.8, 1.3, 0])
        right = label(f"{percent(accuracy)} accurate", 48, GREEN, weight=BOLD).next_to(rule, DOWN, 0.6)
        missed = label("every species missed", 32, VERMILION, weight=BOLD).next_to(right, DOWN, 0.4)
        crosses = VGroup(*[Cross(cells[i], stroke_color=VERMILION, stroke_width=5, scale_factor=0.9)
                           for i in chosen])
        # "Say no every time, ..."
        self.play(FadeIn(rule), run_time=self.share(0.2))
        # "... and you are 95% accurate."
        self.play(*[c.animate.set_fill(GREEN, 0.6) for i, c in enumerate(cells) if i not in chosen],
                  FadeIn(right), run_time=self.share(0.3))
        self.play(Create(crosses), FadeIn(missed), run_time=self.share(0.2))
        self.finish()


class Scene45(VideoScene):
    number = 45

    def construct(self):
        probabilities = self.data("probabilities")
        axes = plain_axes([0, 0.6, 0.1], [0, 1, 1], 11, 3.8).shift(0.3 * DOWN)
        ticks = VGroup(*[label(f"{v:.1f}", 26, SUBDUED).next_to(axes.c2p(v, 0), DOWN, 0.2)
                         for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)])
        name = label("the model's probability that the species is present", 28, SUBDUED
                     ).next_to(ticks, DOWN, 0.25)
        rng = np.random.default_rng(45)
        present = probabilities["rare_species"] == "yes"
        dots = VGroup(*[Dot(axes.c2p(p, rng.uniform(0.08, 0.92)), radius=0.045 if not y else 0.08,
                            color=ORANGE if y else GREY).set_opacity(0.9 if y else 0.5)
                        for p, y in zip(probabilities[".pred_yes"], present)])
        cut = DashedLine(axes.c2p(0.5, 0), axes.c2p(0.5, 1.15), dash_length=0.1, color=VERMILION, stroke_width=5)
        cut_name = label("usual cut-off: 0.5", 30, VERMILION, weight=BOLD).next_to(cut, UP, 0.15)
        top = probabilities[".pred_yes"].max()
        top_mark = Arrow(axes.c2p(top, 1.35), axes.c2p(top, 1.0), color=INK, stroke_width=4, buff=0)
        top_name = label(f"highest: {top:.2f}", 30, INK, weight=BOLD).next_to(top_mark, UP, 0.1)
        self.play(FadeIn(axes), FadeIn(ticks), FadeIn(name), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=self.share(0.3))
        # "The model's highest probability anywhere was 0.37."
        self.play(GrowArrow(top_mark), FadeIn(top_name), run_time=self.share(0.15))
        # "The usual cut-off of one half never fires."
        self.play(Create(cut), FadeIn(cut_name), run_time=self.share(0.2))
        self.finish()


TRADEOFF_COLOURS = {"Downsample": ORANGE, "Upsample": BLUE, "SMOTE": PURPLE}


def tradeoff_layout(scene):
    sweep = scene.data("tradeoff")
    metrics = scene.data("imbalance-metrics").set_index("recipe")
    # Specificity runs from 1 on the left to 0 on the right, as on the page.
    axes = plain_axes([0, 1, 0.25], [0, 1, 0.25], 6.6, 5.4).shift(1.8 * LEFT + 0.3 * DOWN)
    to = lambda spec, sens: axes.c2p(1 - spec, sens)  # noqa: E731
    ticks_x = VGroup(*[label(f"{v:.1f}", 24, SUBDUED).next_to(to(v, 0), DOWN, 0.2) for v in (1, 0.5, 0)])
    ticks_y = VGroup(*[label(f"{v:.1f}", 24, SUBDUED).next_to(to(1, v), LEFT, 0.2) for v in (0, 0.5, 1)])
    x_name = label("specificity: non-events left alone", 26, SUBDUED).next_to(ticks_x, DOWN, 0.2)
    y_name = label("sensitivity: species found", 26, SUBDUED).rotate(PI / 2).next_to(ticks_y, LEFT, 0.2)
    order = sweep.sort_values("specificity", ascending=False)
    curve = VMobject(color=GREY, stroke_width=6).set_points_as_corners(
        [to(s, t) for s, t in zip(order["specificity"], order["sensitivity"])])
    curve_name = VGroup(label("untouched model,", 26, GREY), label("every cut-off", 26, GREY)
                        ).arrange(DOWN, buff=0.08).move_to(to(0.3, 0.3))
    points = VGroup()
    key = VGroup()
    for recipe, colour in TRADEOFF_COLOURS.items():
        r = metrics.loc[recipe]
        points.add(Dot(to(r["specificity"], r["sensitivity"]), radius=0.13, color=colour))
        key.add(VGroup(Dot(radius=0.12, color=colour), label(recipe.lower(), 28)).arrange(RIGHT, buff=0.2))
    key.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([2.3, 1.2, 0], aligned_edge=LEFT)
    head = label("Rebalancing: along the curve, not above it", 32, SUBDUED).to_edge(UP, buff=0.3)
    frame = VGroup(axes, ticks_x, ticks_y, x_name, y_name, head)
    return frame, curve, curve_name, points, key, to


class Scene46(VideoScene):
    number = 46

    def construct(self):
        frame, curve, curve_name, points, key, to = tradeoff_layout(self)
        self.play(FadeIn(frame), run_time=self.share(0.1))
        # "Rebalancing the training data is the usual fix."
        self.play(LaggedStart(*[AnimationGroup(FadeIn(p, scale=1.5), FadeIn(k)) for p, k in zip(points, key)],
                              lag_ratio=0.4), run_time=self.share(0.3))
        # "It moves along the trade-off, but does not lift it."
        self.play(Create(curve), FadeIn(curve_name), run_time=self.share(0.35))
        self.finish()


class Scene47(VideoScene):
    number = 47

    def construct(self):
        frame, curve, curve_name, points, key, to = tradeoff_layout(self)
        self.add(frame, curve, curve_name, points, key)
        at = self.data("thresholds").query("threshold == 0.05").iloc[0]
        start = self.data("thresholds").query("threshold == 0.5").iloc[0]
        cross = Cross(scale_factor=0.18, stroke_color=INK, stroke_width=6).move_to(
            to(start["specificity"], start["sensitivity"]))
        tag = label("untouched, cut-off 0.5", 26, INK).next_to(cross, RIGHT, 0.2)
        moved = VGroup(Cross(scale_factor=0.12, stroke_color=INK, stroke_width=5),
                       label(f"untouched, cut-off {at['threshold']:.2f}", 28, INK, weight=BOLD)
                       ).arrange(RIGHT, buff=0.2).next_to(key, DOWN, 0.5, aligned_edge=LEFT)
        self.play(FadeIn(cross), FadeIn(tag), run_time=self.share(0.15))
        # "Upsampling gave the same result as simply lowering the cut-off to 0.05."
        self.play(cross.animate.move_to(to(at["specificity"], at["sensitivity"])), FadeOut(tag),
                  run_time=self.share(0.35))
        self.play(FadeIn(moved), Indicate(points[1], color=BLUE, scale_factor=1.6), run_time=self.share(0.2))
        self.finish()


class Scene48(VideoScene):
    number = 48

    def construct(self):
        pivot = Triangle(color=INK, fill_opacity=1).scale(0.45).move_to(2.2 * DOWN)
        beam = Line(4.4 * LEFT, 4.4 * RIGHT, color=INK, stroke_width=8).next_to(pivot, UP, 0)
        missed = VGroup(Square(1.2, stroke_width=0, fill_color=VERMILION, fill_opacity=1),
                        label("a missed species", 32, VERMILION, weight=BOLD))
        wasted = VGroup(Square(1.2, stroke_width=0, fill_color=BLUE, fill_opacity=1),
                        label("a wasted inspection", 32, BLUE, weight=BOLD))
        missed[0].next_to(beam.get_left() + 1.0 * RIGHT, UP, 0)
        wasted[0].next_to(beam.get_right() + 1.0 * LEFT, UP, 0)
        missed[1].next_to(missed[0], UP, 0.25)
        wasted[1].next_to(wasted[0], UP, 0.25)
        saw = VGroup(beam, missed, wasted)
        head = label("Choose the cut-off from the costs", 40, INK, weight=BOLD).to_edge(UP, buff=0.8)
        # "So choose the cut-off from what each kind of mistake costs."
        self.play(FadeIn(head), FadeIn(pivot), FadeIn(saw), run_time=self.share(0.3))
        self.play(Rotate(saw, 0.12, about_point=beam.get_center()), run_time=self.share(0.2))
        self.play(Rotate(saw, -0.2, about_point=beam.get_center()), run_time=self.share(0.2))
        self.finish()


class Scene49(KeyPointScene):
    number, point = 49, 3


# Quiz (scenes 50–51) -----------------------------------------------------------------------

class Scene50(QuizScene):
    number = 50
    question = ("A forest was trained on water", "down to 100 metres.",
                "What does it predict at 190 metres?")


class Scene51(VideoScene):
    number = 51

    def construct(self):
        bands, frame, shade, truth, truth_name, forest, forest_name = depth_bands_layout(self)
        answer = label("Much the same as just past 100 metres", 40, VERMILION, weight=BOLD).to_edge(UP, buff=0.3)
        self.play(FadeIn(answer), FadeIn(frame), FadeIn(shade[0]), FadeIn(shade[1]), run_time=self.share(0.15))
        # "... about five animals."
        self.play(Create(forest[0]), FadeIn(forest[1]), FadeIn(forest_name), run_time=self.share(0.3))
        # "The truth is about one."
        self.play(Create(truth[0]), FadeIn(truth[1]), FadeIn(truth_name), run_time=self.share(0.3))
        self.finish()


# The recap (scenes 52–54) and the end card (scene 55) --------------------------------------

class Scene52(RecapScene):
    number, point = 52, 1


class Scene53(RecapScene):
    number, point = 53, 2


class Scene54(RecapScene):
    number, point = 54, 3


class Scene55(EndCardScene):
    number = 55
