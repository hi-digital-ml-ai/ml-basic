"""Manim scenes for the assumptions video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/06-assumptions-limitations
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

A gentle introduction to the section, built on three ideas with a simple picture for
each concept: machine learning frees a model from straight lines and bell curves, but
not from how the data were collected, and a rare answer fools accuracy. Scenes marked "page results" read
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


PROMISES = ["What machine learning frees a model from",
            "What it does not free a model from",
            "Why a rare answer fools accuracy"]
ANSWERS = ["From straight lines and bell curves:\nit can find the shape\nin the data on its own",
           "Not from how the data were collected:\nrepeat visits count for less, and\noff the survey, it is guessing",
           "Check how many rare cases\nthe model finds, not just\nhow often it is right"]
RECAP = ["Machine learning frees a model from straight lines and bell curves",
         "Not from how the data were collected",
         "A rare answer fools accuracy"]

# The pages' colours: the forest in green, anything far from the survey in orange, the
# rare species in vermilion.
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


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name, size=24):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
    axes = plain_axes(x_range, y_range, x_length, y_length)
    tx = VGroup(*[label(f"{v:g}", size, SUBDUED).next_to(axes.c2p(v, y_range[0]), DOWN, 0.15) for v in x_ticks])
    ty = VGroup(*[label(f"{v:g}", size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15) for v in y_ticks])
    xn = label(x_name, 26, SUBDUED).next_to(tx, DOWN, 0.2)
    yn = label(y_name, 26, SUBDUED).rotate(PI / 2).next_to(ty, LEFT, 0.2)
    return axes, VGroup(axes, tx, ty, xn, yn)


def key_row(colour, text, size=28):
    return VGroup(Dot(radius=0.13, color=colour), label(text, size)).arrange(RIGHT, buff=0.2)


def lines(*rows, size=30, colour=INK, bold=True, buff=0.1):
    """Left-aligned lines of text, one style."""
    return VGroup(*[label(t, size, colour, weight=BOLD if bold else NORMAL) for t in rows]
                  ).arrange(DOWN, buff=buff, aligned_edge=LEFT)


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("what machine learning frees", "what it does not", "and why a rare"))


# Frees a model from straight lines and bell curves (scenes 2–8) ----------------------------

class Scene02(VideoScene):
    """Schematic: what an assumption is, and what happens when it is wrong."""

    number = 2

    def construct(self):
        word = label("an assumption", 64, BLUE, weight=BOLD).move_to(1.9 * UP)
        meaning = label("something a method takes for granted about its data", 34, INK).next_to(word, DOWN, 0.35)

        def card(heading, outcome, colour, x):
            box = RoundedRectangle(width=5.4, height=2.4, corner_radius=0.2, stroke_color=colour, stroke_width=5
                                   ).move_to([x, -1.6, 0])
            text = VGroup(label(heading, 30, colour, weight=BOLD), label(outcome, 30, INK)
                          ).arrange(DOWN, buff=0.25).move_to(box)
            return VGroup(box, text)

        right = card("assumption right", "the answer can be trusted", GREEN, -3.1)
        wrong = card("assumption wrong", "still an answer, maybe wrong", VERMILION, 3.1)
        # "Every method takes something for granted about its data."
        cue(self, "Every method")
        self.play(FadeIn(meaning, shift=0.2 * UP), run_time=self.share(0.12))
        # "That is called an assumption."
        cue(self, "That is called")
        self.play(FadeIn(word, scale=1.2), run_time=self.share(0.08))
        # "When an assumption is wrong, the model still gives an answer, but the answer can be wrong."
        cue(self, "When an assumption")
        self.play(FadeIn(right), run_time=self.share(0.08))
        self.play(FadeIn(wrong), run_time=self.share(0.1))
        self.finish()


def shapes_layout():
    """Schematic: animals against temperature with a hump, a straight line and a forest's steps."""
    axes = plain_axes([0, 10, 1], [-0.3, 1.3, 1], 10, 4.6).shift(0.7 * DOWN)
    xl = label("temperature", 28, SUBDUED).next_to(axes, DOWN, 0.25)
    yl = label("animals", 28, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.25)
    rng = np.random.default_rng(4)
    truth = lambda x: np.exp(-((x - 4.2) / 2.0) ** 2)  # noqa: E731
    xs = np.sort(rng.uniform(0.3, 9.7, 40))
    ys = truth(xs) + rng.normal(0, 0.12, len(xs))
    dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.07, color=GREY) for x, y in zip(xs, ys)])
    slope, intercept = np.polyfit(xs, ys, 1)
    line = axes.plot(lambda x: intercept + slope * x, x_range=[0, 10], color=GREY, stroke_width=5)
    cross = Cross(Square(0.5), stroke_color=VERMILION, stroke_width=8).move_to(axes.c2p(8.6, intercept + slope * 8.6))
    line_name = label("linear regression: a straight line", 30, GREY, weight=BOLD)
    # The forest: the mean of the dots in each slice of the input, as a tree's leaves give.
    edges = np.linspace(0, 10, 9)
    levels = [ys[(xs >= a) & (xs < b)].mean() for a, b in zip(edges[:-1], edges[1:])]
    corners = []
    for a, b, level in zip(edges[:-1], edges[1:], levels):
        corners += [axes.c2p(a, level), axes.c2p(b, level)]
    steps = VMobject(color=GREEN, stroke_width=7).set_points_as_corners(corners)
    steps_name = label("random forest: steps", 30, GREEN, weight=BOLD)
    names = VGroup(line_name, steps_name).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.5)
    hump = axes.c2p(4.2, 1.15)
    return VGroup(axes, xl, yl), dots, line, cross, steps, names, hump


class Scene03(VideoScene):
    number = 3

    def construct(self):
        frame, dots, line, cross, steps, names, hump = shapes_layout()
        prefers = label("a temperature it prefers", 28, INK, weight=BOLD).move_to(hump + 0.75 * UP)
        # "Take linear regression."
        self.play(FadeIn(frame), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02),
                  run_time=self.share(0.12))
        # "It assumes a straight line: each extra degree of temperature always adds the same number of animals."
        cue(self, "It assumes")
        self.play(Create(line), FadeIn(names[0]), run_time=self.share(0.14))
        # "But a species often has a temperature it prefers, with fewer animals in colder and in warmer water."
        cue(self, "But a species")
        self.play(FadeIn(prefers, shift=0.2 * DOWN), Indicate(dots, color=INK, scale_factor=1.15),
                  run_time=self.share(0.14))
        # "A straight line cannot draw that hump."
        cue(self, "A straight line cannot")
        self.play(Create(cross), line.animate.fade(0.6), run_time=self.share(0.1))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        frame, dots, line, cross, steps, names, hump = shapes_layout()
        prefers = label("a temperature it prefers", 28, INK, weight=BOLD).move_to(hump + 0.75 * UP)
        line.fade(0.6)
        self.add(frame, dots, line, cross, names[0], prefers)
        flexible = label("flexible", 40, GREEN, weight=BOLD).move_to([3.6, 1.4, 0])
        no_shape = lines("no shape chosen", "in advance", size=28, colour=GREEN).next_to(flexible, DOWN, 0.3)
        # "A random forest does not assume a shape."
        self.play(FadeIn(names[1]), run_time=self.share(0.1))
        # "Its trees split the stations into groups by temperature, so it follows the data in steps, ..."
        cue(self, "Its trees split")
        self.play(Create(steps), run_time=self.share(0.2))
        # "... and finds the hump on its own."
        cue(self, "and finds the hump")
        self.play(Indicate(steps, color=GREEN, scale_factor=1.03), FadeIn(no_shape), run_time=self.share(0.1))
        # "This is what people mean when they call machine learning flexible."
        cue(self, "This is what")
        self.play(FadeIn(flexible, scale=1.2), run_time=self.share(0.08))
        self.finish()


class Scene05(VideoScene):
    """Schematic: the second assumption of a statistics course, about the errors."""

    number = 5

    def construct(self):
        head = label("Taught in statistics courses: the errors", 38, SUBDUED, weight=BOLD).to_edge(UP, buff=0.6)
        gap = label("error: what was caught − what was predicted", 30, INK).next_to(head, DOWN, 0.3)

        def panel(x, heading):
            box = RoundedRectangle(width=5.6, height=4.0, corner_radius=0.2, stroke_color=BLUE, stroke_width=5
                                   ).move_to([x, -1.1, 0])
            return VGroup(box, label(heading, 32, BLUE, weight=BOLD).next_to(box.get_top(), DOWN, 0.35))

        bell_axes = plain_axes([-3, 3, 1], [0, 1.1, 1], 4.2, 2.0).move_to([-3.2, -1.5, 0])
        bell_line = bell_axes.plot(lambda x: np.exp(-x * x / 2), x_range=[-3, 3], color=INK, stroke_width=6)
        rng = np.random.default_rng(5)
        band_axes = plain_axes([0, 10, 1], [-3, 3, 1], 4.2, 2.0).move_to([3.2, -1.5, 0])
        points = VGroup(*[Dot(band_axes.c2p(x, y), radius=0.06, color=INK)
                          for x, y in zip(rng.uniform(0.3, 9.7, 60), rng.normal(0, 0.8, 60))])
        edges = VGroup(DashedLine(band_axes.c2p(0, 1.8), band_axes.c2p(10, 1.8), color=GREY, stroke_width=3),
                       DashedLine(band_axes.c2p(0, -1.8), band_axes.c2p(10, -1.8), color=GREY, stroke_width=3))
        left, right = panel(-3.2, "a bell curve"), panel(3.2, "even spread everywhere")
        # "Statistics courses teach another assumption, about a model's errors: ..."
        self.play(FadeIn(head), run_time=self.share(0.08))
        # "... the gaps between what was caught and what was predicted."
        cue(self, "the gaps")
        self.play(FadeIn(gap, shift=0.2 * UP), run_time=self.share(0.1))
        # "The errors should follow a bell curve, the Normal distribution, ..."
        cue(self, "The errors should")
        self.play(FadeIn(left), FadeIn(bell_axes), run_time=self.share(0.06))
        self.play(Create(bell_line), run_time=self.share(0.1))
        # "... and spread evenly everywhere."
        cue(self, "and spread evenly")
        self.play(FadeIn(right), FadeIn(band_axes), LaggedStart(*[FadeIn(d, scale=0.5) for d in points],
                                                                 lag_ratio=0.02), Create(edges), run_time=self.share(0.14))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        counts = self.data("counts").sort_values("abundance")
        values, stations = counts["abundance"].to_numpy(), counts["stations"].to_numpy()
        total = stations.sum()
        median = values[np.searchsorted(np.cumsum(stations), total / 2)]
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
        mid = DashedLine(axes.c2p(median, 0), axes.c2p(median, top * 0.7), color=INK, stroke_width=5)
        mid_name = VGroup(Line(mid.get_end(), axes.c2p(6.5, top * 0.7), color=INK, stroke_width=3),
                          label(f"the middle station: {median:g}", 28, INK, weight=BOLD
                                ).next_to(axes.c2p(6.5, top * 0.7), RIGHT, 0.1))
        largest = label(f"largest {values.max():g}", 28, INK, weight=BOLD).next_to(axes.c2p(values.max(), 0), UP, 0.35)
        tail = Arrow(axes.c2p(12, top * 0.3), axes.c2p(36, top * 0.3), color=ORANGE, stroke_width=6, buff=0)
        tail_name = label("a long tail of big catches", 30, ORANGE, weight=BOLD).next_to(tail, UP, 0.15)
        head = label(f"The survey's catches, {total} stations", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.35)
        # "Survey counts do not behave like that. Of 598 stations, 129 caught nothing, ..."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.06))
        cue(self, "Of 598")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=self.share(0.12))
        cue(self, "129 caught")
        self.play(FadeIn(empty, shift=0.2 * LEFT), run_time=self.share(0.06))
        # "... the middle station caught 3, ..."
        cue(self, "the middle station")
        self.play(Create(mid), FadeIn(mid_name), run_time=self.share(0.08))
        # "... and the largest 40."
        cue(self, "and the largest")
        self.play(FadeIn(largest, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "Most catches are small, with a long tail of big ones."
        cue(self, "Most catches")
        self.play(GrowArrow(tail), FadeIn(tail_name), run_time=self.share(0.1))
        self.finish()


class Scene07(VideoScene):
    number = 7

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
        dots = VGroup(*[Dot(axes.c2p(q, e), radius=0.035, color=INK).set_opacity(0.45)
                        for q, e in zip(errors["predicted"], errors["error"])])
        above = VGroup(*[d for d, e in zip(dots, errors["error"]) if e > 8])
        bands = VGroup()
        for _, row in spread.iloc[[0, -1]].iterrows():
            lo, hi = row["predicted_from"], min(row["predicted_to"], x_top)
            bands.add(Rectangle(width=axes.c2p(hi, 0)[0] - axes.c2p(lo, 0)[0],
                                height=axes.c2p(0, row["error_sd"])[1] - axes.c2p(0, -row["error_sd"])[1],
                                stroke_width=0, fill_color=BLUE, fill_opacity=0.25
                                ).move_to(axes.c2p(lo, -row["error_sd"]), aligned_edge=DL))
        lopsided = lines("lopsided: most a little", "below, a few far above", size=28)
        wider = lines("wider where it", "predicts more", size=28, colour=BLUE)
        fine = lines("the forest", "predicts well anyway", size=30, colour=GREEN)
        why = lines("a tree predicts the", "average catch of", "similar stations:", size=26, bold=False, buff=0.06)
        why.add(label("no bell curve needed", 26, INK, weight=BOLD).next_to(why, DOWN, 0.06, aligned_edge=LEFT))
        VGroup(lopsided, wider, fine, why).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(5.1 * RIGHT + 0.2 * DOWN)
        head = label("The random forest's errors, on sites it never saw", 30, SUBDUED, weight=BOLD
                     ).to_edge(UP, buff=0.3)
        # "So a random forest's errors are lopsided, ..."
        self.play(FadeIn(frame), FadeIn(head), Create(zero), run_time=self.share(0.06))
        self.play(FadeIn(dots, lag_ratio=0.002), run_time=self.share(0.1))
        cue(self, "are lopsided")
        self.play(Indicate(above, color=VERMILION, scale_factor=1.5), FadeIn(lopsided), run_time=self.share(0.08))
        # "... and they spread wider where it predicts more."
        cue(self, "and they spread")
        self.play(FadeIn(bands), FadeIn(wider), run_time=self.share(0.1))
        # "Yet the forest predicts well."
        cue(self, "Yet the forest")
        self.play(FadeIn(fine, shift=0.2 * UP), run_time=self.share(0.06))
        # "A tree predicts the average catch of similar stations, and an average needs no bell curve."
        cue(self, "A tree predicts")
        self.play(FadeIn(why, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene08(KeyPointScene):
    number, point = 8, 1


# But not from how the data were collected (scenes 9–16) ------------------------------------

class Scene09(VideoScene):
    """Schematic: a model learns only from its stations, and survey effort gathers near a port."""

    number = 9

    def construct(self):
        sea = Rectangle(width=7.0, height=5.0, stroke_width=0, fill_color="#EAF2F8", fill_opacity=1
                        ).move_to(2.6 * LEFT + 0.3 * DOWN)
        land = Rectangle(width=0.8, height=5.0, stroke_width=0, fill_color="#E8E0D0", fill_opacity=1
                         ).next_to(sea, LEFT, 0)
        port = VGroup(Square(0.3, stroke_width=0, fill_color=INK, fill_opacity=1),
                      label("port", 26, INK, weight=BOLD)).arrange(RIGHT, buff=0.15)
        port.move_to(sea.get_left() + 0.45 * RIGHT + 1.2 * UP, aligned_edge=LEFT)
        rng = np.random.default_rng(12)
        near = sea.get_left() + 2.0 * RIGHT + 1.0 * UP
        points = [near + np.array([abs(dx), dy, 0]) for dx, dy in rng.normal(0, [1.0, 0.8], (30, 2))]
        stations = VGroup(*[Dot(p, radius=0.08, color=BLUE) for p in points
                            if abs(p[0] - sea.get_x()) < 3.3 and abs(p[1] - sea.get_y()) < 2.3])
        model = RoundedRectangle(width=2.6, height=1.4, corner_radius=0.2, stroke_color=GREEN, stroke_width=6
                                 ).move_to(4.8 * RIGHT + 0.6 * UP)
        model_name = label("the model", 32, GREEN, weight=BOLD).move_to(model)
        arrow = Arrow(stations.get_right(), model.get_left(), color=INK, stroke_width=6, buff=0.3)
        only = lines("it can only learn", "from these stations", size=28).next_to(model, DOWN, 0.4)
        matters = label("so how they were gathered matters", 30, INK, weight=BOLD).to_edge(DOWN, buff=0.4)
        # "Next, what it does not free a model from: how the data were collected."
        self.play(FadeIn(sea), FadeIn(land), FadeIn(port), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in stations], lag_ratio=0.03), run_time=self.share(0.1))
        # "However flexible, a model can only learn from the stations it was given."
        cue(self, "a model can only")
        self.play(FadeIn(model), FadeIn(model_name), GrowArrow(arrow), FadeIn(only), run_time=self.share(0.14))
        # "... so how they were gathered matters."
        cue(self, "so how they")
        self.play(FadeIn(matters, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def visit_squares(visits):
    """One square per station, in rows like a spreadsheet and in stacks by site."""
    counts = sorted(visits["visits"].astype(int), reverse=True)
    total = sum(counts)
    squares = VGroup(*[Square(0.1, stroke_width=0, fill_color=BLUE, fill_opacity=1) for _ in range(total)])
    grid = squares.copy().arrange_in_grid(rows=20, buff=0.06).move_to(0.3 * DOWN)
    stacks, i = VGroup(), 0
    for n in counts:
        stacks.add(VGroup(*[squares[i + k].copy() for k in range(n)]).arrange(UP, buff=0.02))
        i += n
    stacks.arrange_in_grid(rows=4, buff=(0.06, 0.35), cell_alignment=DOWN)
    stacks.scale_to_fit_width(12.6)
    if stacks.height > 4.4:
        stacks.scale_to_fit_height(4.4)
    stacks.move_to(1.2 * DOWN)
    return total, grid, stacks


class Scene10(VideoScene):
    number = 10

    def construct(self):
        total, grid, stacks = visit_squares(self.data("visits"))
        head = label(f"{total} stations", 48, INK, weight=BOLD).to_edge(UP, buff=0.5)
        sites = label(f"from only {len(stacks)} sites", 48, BLUE, weight=BOLD).to_edge(UP, buff=0.5)
        # "This survey's 800 stations come from only 160 sites, visited again and again."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(q) for q in grid], lag_ratio=0.002), run_time=self.share(0.14))
        cue(self, "come from only")
        flat = VGroup(*[q for stack in stacks for q in stack])
        self.play(Transform(grid, flat), run_time=self.share(0.18))
        self.play(FadeOut(head, shift=0.3 * UP), FadeIn(sites, shift=0.3 * UP), run_time=self.share(0.06))
        # "As the Marine data video showed, visits to one site share its depth, its seabed and its water, ..."
        cue(self, "visits to one site")
        start = sum(len(q) for q in stacks[:5])
        one = VGroup(*grid[start:start + len(stacks[5])])
        box = SurroundingRectangle(stacks[5], color=ORANGE, buff=0.08, stroke_width=4)
        name = label("one site: same depth, same seabed, same water", 30, ORANGE, weight=BOLD
                     ).next_to(stacks, UP, 0.3)
        self.play(one.animate.set_fill(ORANGE), Create(box), FadeIn(name), run_time=self.share(0.12))
        # "... so they partly repeat each other."
        cue(self, "so they partly")
        repeat = label("so its visits partly repeat each other", 30, INK, weight=BOLD).move_to(name)
        self.play(FadeOut(name, shift=0.2 * UP), FadeIn(repeat, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        spreads = self.data("spreads")
        worth = spreads[(spreads["estimate"] == "Average catch") & (spreads["resampled"] == "Whole sites")]["worth"].iloc[0]
        worth = int(round(worth, -1))
        n = int(self.data("visits")["visits"].sum())
        squares = VGroup(*[Square(0.16, stroke_width=0, fill_color=BLUE, fill_opacity=1) for _ in range(n)]
                         ).arrange_in_grid(rows=20, buff=0.05).move_to(2.6 * LEFT + 0.3 * DOWN)
        head = label("How much the stations are worth", 34, SUBDUED, weight=BOLD).to_edge(UP, buff=0.4)
        counted = lines(f"{n} stations,", f"worth about {worth}", "independent ones", size=34, colour=BLUE
                        ).move_to(4.6 * RIGHT + 0.9 * UP)
        surer = lines(f"counted as {n}:", "results look surer", "than they are", size=30, colour=VERMILION
                      ).next_to(counted, DOWN, 0.6, aligned_edge=LEFT)
        # "How much do they repeat?"
        self.play(FadeIn(head), FadeIn(squares, lag_ratio=0.001), run_time=self.share(0.14))
        # "The 800 stations carry about as much information as 470 independent ones."
        cue(self, "The 800")
        self.play(*[q.animate.set_fill(LIGHT) for q in squares[worth:]], FadeIn(counted), run_time=self.share(0.2))
        # "Count them as 800, and a model's results look surer than they are."
        cue(self, "Count them")
        self.play(FadeIn(surer, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def novelty_layout(scene):
    """The summer and autumn survey by depth and temperature, and the winter stations, for scenes 12–15."""
    stations = scene.data("novelty")
    depth, temp = stations["depth_m"], stations["temperature_c"]
    axes, frame = chart([0, 200, 50], [0, 20, 5], 7.0, 4.8, [0, 50, 100, 150, 200], [0, 5, 10, 15, 20],
                        "depth (m)", "temperature (°C)")
    VGroup(axes, frame).shift(2.6 * LEFT + 0.4 * DOWN)
    rows = (stations["status"] == "Surveyed") & depth.notna() & temp.notna()
    surveyed_dots = VGroup(*[Dot(axes.c2p(d, t), radius=0.045, color=LIGHT) for d, t in zip(depth[rows], temp[rows])])
    surveyed = stations[rows]
    winter = stations[(stations["status"] == "Inside every range, far from the survey")
                      & (stations["season"] == "winter")]
    winter_dots = VGroup(*[Dot(axes.c2p(d, t), radius=0.07, color=ORANGE)
                           for d, t in zip(winter["depth_m"], winter["temperature_c"])])
    head = label("A survey in summer and autumn", 28, SUBDUED, weight=BOLD).move_to([1.0, 2.9, 0], aligned_edge=LEFT)
    key = VGroup(key_row(LIGHT, "surveyed station"), key_row(ORANGE, "winter station")
                 ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(head, DOWN, 0.4, aligned_edge=LEFT)
    cold = surveyed[surveyed["temperature_c"] < 8]
    low, high = axes.c2p(cold["depth_m"].min() - 4, cold["temperature_c"].min() - 0.6), axes.c2p(cold["depth_m"].max() + 4, 8)
    cold_zone = Rectangle(width=high[0] - low[0], height=high[1] - low[1], stroke_color=BLUE, stroke_width=4,
                          fill_color=BLUE, fill_opacity=0.08).move_to(low, aligned_edge=DL)
    cold_name = label("cold water: only at depth", 28, BLUE, weight=BOLD)
    return frame, surveyed_dots, winter_dots, head, key, cold_zone, cold_name


class Scene12(VideoScene):
    number = 12

    def construct(self):
        frame, dots, winter, head, key, cold_zone, cold_name = novelty_layout(self)
        cold_name.next_to(key[0], DOWN, 0.4, aligned_edge=LEFT)
        effort = lines("survey effort follows", "ports, weather and ship time", size=30).move_to(head, aligned_edge=UL)
        # "Survey effort is uneven too: it follows ports, weather and ship time."
        self.play(FadeIn(effort), run_time=self.share(0.08))
        # "Here is a survey that sailed only in summer and autumn."
        cue(self, "Here is a survey")
        self.play(FadeOut(effort), FadeIn(frame), FadeIn(head), run_time=self.share(0.1))
        # "Each dot is a station, placed by its depth and its temperature."
        cue(self, "Each dot is")
        self.play(FadeIn(key[0]), FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.2))
        # "In those seasons the shallows are warm, so the survey met cold water only at depth."
        cue(self, "so the survey met")
        self.play(Create(cold_zone), FadeIn(cold_name), run_time=self.share(0.2))
        self.finish()


def winter_notes(key):
    seen = VGroup(label("depth: seen", 30, INK, weight=BOLD),
                  label("temperature: seen", 30, INK, weight=BOLD),
                  label("the two together: never", 30, ORANGE, weight=BOLD)
                  ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(key, DOWN, 0.6, aligned_edge=LEFT)
    return seen


class Scene13(VideoScene):
    number = 13

    def construct(self):
        frame, dots, winter, head, key, cold_zone, cold_name = novelty_layout(self)
        self.add(frame, dots, head, key[0])
        seen = winter_notes(key)
        alone = label("nothing like them to learn from", 28, VERMILION, weight=BOLD
                      ).next_to(seen, DOWN, 0.5, aligned_edge=LEFT)
        # "In winter, the shallows turn cold."
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in winter], lag_ratio=0.01), FadeIn(key[1]),
                  run_time=self.share(0.2))
        # "Each winter station's depth was seen in the survey, and so was its temperature, ..."
        cue(self, "Each winter")
        self.play(FadeIn(seen[0]), run_time=self.share(0.08))
        cue(self, "and so was")
        self.play(FadeIn(seen[1]), run_time=self.share(0.08))
        # "... but never the two together."
        cue(self, "but never")
        self.play(FadeIn(seen[2]), Indicate(winter, color=ORANGE, scale_factor=1.4), run_time=self.share(0.1))
        # "The model has no stations like these to learn from."
        cue(self, "The model has")
        self.play(FadeIn(alone, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        frame, dots, winter, head, key, cold_zone, cold_name = novelty_layout(self)
        seen = winter_notes(key)
        self.add(frame, dots, head, key, winter, seen)
        ring = SurroundingRectangle(winter, color=ORANGE, buff=0.15, corner_radius=0.2, stroke_width=5)
        answers = lines("the model still answers,", "just as sure", size=30, colour=VERMILION
                        ).next_to(ring, UP, 0.2).set_x(ring.get_x())
        answers = plated(answers)
        extrapolation = VGroup(label("extrapolation:", 30, ORANGE, weight=BOLD),
                               label("predicting beyond the data", 30, INK)
                               ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        grew = lines("its errors grew the further", "a station lay from the survey", size=26, bold=False)
        side = VGroup(extrapolation, grew).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(seen, DOWN, 0.35,
                                                                                            aligned_edge=LEFT)
        grew.shift(0.35 * RIGHT)
        # "It still gives an answer, and the answer looks just as sure as any other."
        self.play(Create(ring), run_time=self.share(0.1))
        self.play(FadeIn(answers, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "As in the Supervised learning video, predicting beyond the data is called extrapolation."
        cue(self, "predicting beyond")
        self.play(FadeIn(extrapolation, shift=0.2 * UP), run_time=self.share(0.1))
        # "Tested on stations like these, the forest's errors grew the further a station lay from the survey."
        cue(self, "Tested on")
        self.play(FadeIn(grew, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        frame, dots, winter, head, key, cold_zone, cold_name = novelty_layout(self)
        seen = winter_notes(key)
        self.add(frame, dots, head, key, winter, seen)
        question = VGroup(label("before trusting a prediction, ask:", 34, INK, weight=BOLD),
                          label("did the survey see conditions like these?", 40, BLUE, weight=BOLD)
                          ).arrange(DOWN, buff=0.2).move_to(0.2 * DOWN)
        box = SurroundingRectangle(question, color=BLUE, buff=0.45, corner_radius=0.2, stroke_width=5,
                                   fill_color=BACKGROUND, fill_opacity=0.97)
        VGroup(box, question).set_z_index(5)
        # "So before trusting a prediction, ask one question: did the survey see conditions like these?"
        self.play(FadeOut(seen), dots.animate.set_opacity(0.4), winter.animate.set_opacity(0.4),
                  run_time=self.share(0.06))
        self.play(FadeIn(box), FadeIn(question[0]), run_time=self.share(0.1))
        cue(self, "did the survey")
        self.play(FadeIn(question[1], shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene16(KeyPointScene):
    number, point = 16, 2


# A rare answer fools accuracy (scenes 17–20) ------------------------------------------------

def rare_grid(scene):
    """The training stations as dots, the ones with the rare species picked out, for scenes 17–19."""
    rare = scene.data("rare").iloc[0]
    n, present = int(rare["stations"]), int(rare["present"])
    dots = VGroup(*[Dot(radius=0.065, color=LIGHT) for _ in range(n)]).arrange_in_grid(cols=26, buff=0.09)
    dots.move_to(3.2 * LEFT + 0.3 * DOWN)
    picks = np.random.default_rng(3).choice(n, present, replace=False)
    lit = VGroup(*[dots[k] for k in picks])
    others = VGroup(*[d for k, d in enumerate(dots) if k not in set(picks)])
    return rare, dots, lit, others


def rare_key(dots):
    """Above the grid: what the survey recorded, and what the model called."""
    called = VGroup(Square(0.3, color=INK, stroke_width=4), label("called present by the model", 28)
                    ).arrange(RIGHT, buff=0.2)
    key = VGroup(key_row(VERMILION, "species present (the survey's record)"), called
                 ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(dots, UP, 0.45, aligned_edge=LEFT)
    return key


def model_calls(scene, lit, others):
    """Squares on the stations the model called present, scaled from the page's five repeats
    to one grid: a few on presences (found), the rest on absences (false alarms). False
    alarms keep clear of the presences and of each other, so no square looks shared."""
    matched = scene.data("matched").iloc[0]
    repeats = int(matched["repeats"])
    found = round((matched["called_present"] - matched["false_alarms"]) / repeats)
    alarms = round(matched["false_alarms"] / repeats)
    rng = np.random.default_rng(5)
    hits = []
    for k in rng.permutation(len(lit)):
        if len(hits) < found and all(np.linalg.norm(lit[k].get_center() - q.get_center()) > 0.45 for q in hits):
            hits.append(lit[k])
    picked = []
    for k in rng.permutation(len(others)):
        d = others[k].get_center()
        if (all(np.linalg.norm(d - q.get_center()) > 0.4 for q in lit)
                and all(np.linalg.norm(d - q.get_center()) > 0.45 for q in hits + picked)):
            picked.append(others[k])
        if len(picked) == alarms:
            break
    return VGroup(*[Square(0.3, color=INK, stroke_width=4).move_to(d) for d in hits + picked])


def lit_up(lit):
    for d in lit:
        d.set_color(VERMILION).scale(1.4)


class Scene17(VideoScene):
    number = 17

    def construct(self):
        rare, dots, lit, _ = rare_grid(self)
        key = rare_key(dots)
        examples = VGroup(label("rare", 48, VERMILION, weight=BOLD),
                          label("a protected species", 36, INK, weight=BOLD),
                          label("a harmful algal bloom", 36, INK, weight=BOLD)).arrange(DOWN, buff=0.3).move_to(0.4 * UP)
        found = VGroup(label(f"{int(rare['present'])} of {int(rare['stations'])} stations", 38, VERMILION, weight=BOLD),
                       label(f"{100 * rare['prevalence']:.1f}%", 52, VERMILION, weight=BOLD)
                       ).arrange(DOWN, buff=0.15).move_to(3.9 * RIGHT + 0.3 * UP)
        # "Many things marine scientists most want to predict are rare: ..."
        cue(self, "Many things")
        self.play(FadeIn(examples, shift=0.2 * UP), run_time=self.share(0.14))
        # "Here a second species turns up at only 29 of 598 stations, about 5 per cent."
        cue(self, "Here a second")
        self.play(FadeOut(examples), FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.12))
        cue(self, "29 of")
        self.play(*[d.animate.set_color(VERMILION).scale(1.4) for d in lit], FadeIn(found), FadeIn(key[0]),
                  run_time=self.share(0.12))
        self.finish()


def trap_panel(scene):
    matched = scene.data("matched").iloc[0]
    one_in = round(1 / matched["sensitivity"])
    head = VGroup(label("logistic regression", 32, INK, weight=BOLD),
                  label(f"threshold {matched['threshold']:.2f}", 28, SUBDUED)
                  ).arrange(DOWN, buff=0.08).move_to(3.9 * RIGHT + 2.7 * UP)
    found = VGroup(label("presences found", 30, VERMILION),
                   label(f"1 in {one_in}", 64, VERMILION, weight=BOLD)
                   ).arrange(DOWN, buff=0.1).move_to(3.9 * RIGHT + 0.9 * UP)
    accuracy = VGroup(label("accuracy", 30, GREEN), label(f"{100 * matched['accuracy']:.0f}%", 64, GREEN, weight=BOLD)
                      ).arrange(DOWN, buff=0.1).move_to(3.9 * RIGHT + 1.3 * DOWN)
    meaning = label("the share of its calls that are right", 26, SUBDUED).next_to(accuracy, DOWN, 0.15)
    return matched, head, found, accuracy, meaning


class Scene18(VideoScene):
    number = 18

    def construct(self):
        rare, dots, lit, others = rare_grid(self)
        lit_up(lit)
        key = rare_key(dots)
        self.add(dots, key[0])
        matched, head, found, accuracy, meaning = trap_panel(self)
        hides = label("accuracy hides the misses", 28, INK, weight=BOLD).next_to(meaning, DOWN, 0.3)
        calls = model_calls(self, lit, others)
        # "Logistic regression gives each station a probability of presence, ..."
        self.play(FadeIn(head[0]), run_time=self.share(0.08))
        # "Here the threshold is set so that it calls about as many stations present ..."
        cue(self, "Here the threshold")
        self.play(FadeIn(head[1]), FadeIn(key[1]), LaggedStart(*[Create(c) for c in calls], lag_ratio=0.1),
                  run_time=self.share(0.14))
        # "It finds only one presence in six."
        cue(self, "It finds only")
        self.play(FadeIn(found), Indicate(lit, color=VERMILION, scale_factor=1.3), run_time=self.share(0.08))
        # "Yet its accuracy, the share of its calls that are right, is 92 per cent."
        cue(self, "Yet its accuracy")
        self.play(FadeIn(accuracy), FadeIn(meaning), run_time=self.share(0.08))
        # "... calling a station absent is nearly always right, so accuracy hides the misses."
        cue(self, "so accuracy hides")
        self.play(FadeIn(hides, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        rare, dots, lit, others = rare_grid(self)
        lit_up(lit)
        key = rare_key(dots)
        calls = model_calls(self, lit, others)
        matched, head, found, accuracy, meaning = trap_panel(self)
        self.add(dots, key, calls, head, found, accuracy, meaning)
        rings = VGroup(*[Circle(0.15, color=BLUE, stroke_width=4).move_to(d) for d in lit])
        ask = lines("how many of these", "does it find?", size=40, colour=BLUE).move_to(3.9 * RIGHT + 1.0 * UP)
        not_only = lines("not just how often", "it is right", size=30, colour=SUBDUED).next_to(ask, DOWN, 0.3)
        later = lines("measuring it:", "the Validation section", size=30, colour=INK).next_to(not_only, DOWN, 0.7)
        for g in (not_only, later):
            g.align_to(ask, LEFT)
        # "So check how many of the rare cases a model finds, ..."
        self.play(FadeOut(VGroup(head, found, accuracy, meaning)), Create(rings), run_time=self.share(0.12))
        self.play(FadeIn(ask), run_time=self.share(0.1))
        # "... not just how often it is right."
        cue(self, "not just")
        self.play(FadeIn(not_only), run_time=self.share(0.08))
        # "The Validation section shows how to measure that."
        cue(self, "The Validation")
        self.play(FadeIn(later, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene20(KeyPointScene):
    number, point = 20, 3


# Quiz (scenes 21–22) -----------------------------------------------------------------------

class Scene21(QuizScene):
    number = 21
    question = ("A harmful algal bloom occurs", "on 2 days in 100.",
                "A model that warns of blooms is 98% accurate.", "Is it a good model?")


class Scene22(VideoScene):
    """Schematic: a hundred days, two with a bloom, and a model that never warns."""

    number = 22

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
        ask = VGroup(label("ask:", 30, BLUE, weight=BOLD),
                     label("how many blooms does it catch?", 30, BLUE, weight=BOLD)
                     ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(never, DOWN, 0.7, aligned_edge=LEFT)
        rings = VGroup(*[Circle(0.3, color=VERMILION, stroke_width=4).move_to(b) for b in blooms])
        key = key_row(VERMILION, "a day with a bloom", 26).next_to(days, DOWN, 0.3)
        # "You can't tell yet."
        self.play(FadeIn(answer, scale=1.2), FadeIn(days, lag_ratio=0.005), FadeIn(key), run_time=self.share(0.14))
        # "A model that never warns is also 98 per cent accurate, ..."
        cue(self, "A model that")
        self.play(FadeIn(never[:2]), run_time=self.share(0.1))
        # "... and it misses every bloom."
        cue(self, "and it misses")
        self.play(FadeIn(never[2]), Create(rings), run_time=self.share(0.1))
        # "Ask how many of the blooms it catches."
        cue(self, "Ask how")
        self.play(FadeIn(ask, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


# The recap (scenes 23–25) and the end card (scene 26) --------------------------------------

class Scene23(RecapScene):
    number, point = 23, 1


class Scene24(RecapScene):
    number, point = 24, 2


class Scene25(RecapScene):
    number, point = 25, 3


class Scene26(EndCardScene):
    number = 26
