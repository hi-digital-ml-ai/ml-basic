"""Manim scenes for the assumptions video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/06-assumptions-limitations
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is built on three ideas from the section, each with the reason it matters: a
model can fit well and still be wrong, rows are worth less than they seem, and a model
never says when it is guessing. Scenes marked "page results" read visuals/data/*.csv,
which tools/figures-for-video.R writes from the pages. The others are schematic:
made-up shapes, never numbers that could pass for survey results. The opening,
key-point, recap, quiz and end-card scenes are shared (mlbasic_video.py) and read
PROMISES, ANSWERS and RECAP from here. Consecutive scenes about one picture share a
builder, so each starts where the previous one ended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["Why a model can fit well and still be wrong",
            "Why rows are worth less than they seem",
            "Why a model never says when it is guessing"]
ANSWERS = ["A curve that follows the data\ncan credit the wrong input",
           "Visits repeat each other:\nscore a model on sites\nit has never seen",
           "Measure how far each\nprediction lies\nfrom the survey"]
RECAP = ["A model can fit well and still be wrong",
         "Rows are worth less than they seem",
         "A model never says when it is guessing"]

# The pages' colours: the random forest in green on its curves and blue elsewhere, the
# truth in ink, anything far from the survey in orange.
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


def f2(value):
    return f"{value:.2f}"


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


def card(text, colour=PURPLE, size=40):
    words = VGroup(*[label(t, size, colour, weight=BOLD) for t in text.split("\n")]).arrange(DOWN, buff=0.15)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def polyline(axes, xs, ys, colour, width=6, opacity=1.0):
    return VMobject(color=colour, stroke_width=width, stroke_opacity=opacity).set_points_as_corners(
        [axes.c2p(x, y) for x, y in zip(xs, ys)])


def dashed(line, n=50):
    return DashedVMobject(line, num_dashes=n)


def key_row(colour, text, size=28, shape="dot"):
    mark = Dot(radius=0.13, color=colour) if shape == "dot" else \
        Line(ORIGIN, 0.5 * RIGHT, color=colour, stroke_width=6)
    return VGroup(mark, label(text, size)).arrange(RIGHT, buff=0.2)


class Scene01(LearnScene):
    number = 1


# Machine learning still assumes (scenes 2–3, schematic) ------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        called = label("machine learning is often called", 36, SUBDUED).move_to(1.2 * UP)
        free = label("assumption-free", 76, INK, weight=BOLD).next_to(called, DOWN, 0.35)
        strike = Line(free.get_left() + 0.2 * LEFT, free.get_right() + 0.2 * RIGHT,
                      color=VERMILION, stroke_width=10)
        claim = VGroup(called, free, strike)

        def panel(heading, rows, colour, x):
            box = RoundedRectangle(width=5.6, height=3.6, corner_radius=0.2, stroke_color=colour,
                                   stroke_width=5).move_to([x, -1.2, 0])
            head = label(heading, 32, colour, weight=BOLD).next_to(box.get_top(), DOWN, 0.35)
            items = VGroup(*[label(t, 30) for t in rows]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            items.next_to(head, DOWN, 0.4)
            return VGroup(box, head, items)

        shape = panel("freed from", ["straight lines"], GREEN, -3.2)
        data = panel("not freed from", ["repeat visits", "neighbouring sites",
                                        "uneven survey effort"], VERMILION, 3.2)
        # "Machine learning is often called assumption-free."
        self.play(FadeIn(called), FadeIn(free, shift=0.2 * UP), run_time=self.share(0.18))
        cue(self, "It frees")
        self.play(Create(strike), free.animate.set_color(GREY), run_time=self.share(0.1))
        self.play(claim.animate.scale(0.6).to_edge(UP, buff=0.5), run_time=self.share(0.1))
        # "It frees a model from straight lines, ..."
        self.play(FadeIn(shape), run_time=self.share(0.12))
        # "... but not from the way its data were collected."
        cue(self, "but not from")
        self.play(FadeIn(data[0]), FadeIn(data[1]), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in data[2]], lag_ratio=0.3),
                  run_time=self.share(0.2))
        self.finish()


class Scene03(VideoScene):
    number = 3

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
        known = label("answers checked against the truth", 32, GREEN, weight=BOLD).to_edge(DOWN, buff=0.4)
        # "The survey in this course is simulated, ..."
        self.play(FadeIn(source, scale=0.9), run_time=self.share(0.12))
        self.play(GrowArrow(arrow), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(d, shift=0.4 * RIGHT) for d in field], lag_ratio=0.04),
                  FadeIn(field_name), run_time=self.share(0.25))
        # "... so a model's answers can be checked against the truth, ..."
        cue(self, "so a model's")
        self.play(FadeIn(known, shift=0.2 * UP), run_time=self.share(0.1))
        self.play(Indicate(known, color=GREEN), run_time=self.share(0.15))
        self.finish()


# A model can fit well and still be wrong (scenes 4–9) ---------------------------------------

class Scene04(VideoScene):
    """Schematic: a hump a straight line misses and a forest follows in steps."""

    number = 4

    def construct(self):
        axes = plain_axes([0, 10, 1], [-0.3, 1.3, 1], 10, 4.6).shift(0.6 * DOWN)
        xl = label("an input, such as temperature", 28, SUBDUED).next_to(axes, DOWN, 0.25)
        yl = label("how many", 28, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.25)
        rng = np.random.default_rng(4)
        truth = lambda x: np.exp(-((x - 4.2) / 2.0) ** 2)  # noqa: E731
        xs = np.sort(rng.uniform(0.3, 9.7, 40))
        ys = truth(xs) + rng.normal(0, 0.12, len(xs))
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.07, color=GREY) for x, y in zip(xs, ys)])
        slope, intercept = np.polyfit(xs, ys, 1)
        line = axes.plot(lambda x: intercept + slope * x, x_range=[0, 10], color=GREY, stroke_width=5)
        cross = Cross(line, stroke_color=VERMILION, stroke_width=5, scale_factor=0.25).move_to(axes.c2p(8.5, 0.15))
        line_name = label("linear model: a straight line", 30, GREY, weight=BOLD)

        # The forest: the mean of the dots in each slice of the input, as a tree's leaves give.
        edges = np.linspace(0, 10, 9)
        levels = [ys[(xs >= a) & (xs < b)].mean() for a, b in zip(edges[:-1], edges[1:])]
        corners = []
        for a, b, level in zip(edges[:-1], edges[1:], levels):
            corners += [axes.c2p(a, level), axes.c2p(b, level)]
        steps = VMobject(color=GREEN, stroke_width=7).set_points_as_corners(corners)
        steps_name = label("random forest: steps", 30, GREEN, weight=BOLD)

        names = VGroup(line_name, steps_name).arrange(RIGHT, buff=1.2)
        names.scale_to_fit_width(min(names.width, 12.6)).to_edge(UP, buff=0.5)

        # "Few marine responses are straight lines."
        self.play(FadeIn(axes), FadeIn(xl), FadeIn(yl), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02), run_time=self.share(0.12))
        # "Linear models assume them; ..."
        cue(self, "Linear models")
        self.play(Create(line), FadeIn(line_name), run_time=self.share(0.1))
        self.play(Create(cross), line.animate.set_opacity(0.3), run_time=self.share(0.05))
        # "... random forests do not."
        cue(self, "random forests")
        self.play(FadeIn(steps_name), run_time=self.share(0.08))
        # "They follow the data in steps, with no shape chosen in advance."
        cue(self, "They follow")
        self.play(Create(steps), run_time=self.share(0.2))
        self.play(Indicate(steps, color=GREEN, scale_factor=1.03), run_time=self.share(0.1))
        self.finish()


ERROR_INPUTS = {"depth_m": "depth (m)", "temperature_c": "temperature (°C)",
                "chlorophyll_mg_m3": "chlorophyll (mg/m³)", "salinity_psu": "salinity (PSU)"}


class Scene05(VideoScene):
    number = 5

    def construct(self):
        checks = self.data("error-check")
        reach = np.ceil(checks["error"].abs().max())
        panels = VGroup()
        for k, (input_, name) in enumerate(ERROR_INPUTS.items()):
            rows = checks[checks["input"] == input_].sort_values("group")
            lo, hi = rows["value"].min(), rows["value"].max()
            axes = plain_axes([lo, hi, (hi - lo) / 4], [-reach, reach, reach / 2], 5.0, 2.0)
            one = DashedLine(axes.c2p(lo, 0), axes.c2p(hi, 0), color=GREY, stroke_width=3)
            colour = VERMILION if input_ == "temperature_c" else BLUE
            line = polyline(axes, rows["value"], rows["error"], colour, 6)
            dots = VGroup(*[Dot(axes.c2p(v, r), radius=0.07, color=colour)
                            for v, r in zip(rows["value"], rows["error"])])
            title_ = label(name, 28, colour if input_ == "temperature_c" else SUBDUED, weight=BOLD
                           ).next_to(axes, UP, 0.15)
            panels.add(VGroup(axes, one, line, dots, title_))
        panels.arrange_in_grid(rows=2, buff=(1.0, 0.8)).shift(0.5 * DOWN)
        head = label("Linear regression's average error: caught − predicted", 32, SUBDUED
                     ).to_edge(UP, buff=0.4)
        temperature = panels[1]
        hump = label("too many at both ends, too few between", 26, VERMILION, weight=BOLD
                     ).next_to(temperature, DOWN, 0.15)
        right = VGroup(DashedLine(ORIGIN, 0.6 * RIGHT, color=GREY, stroke_width=3),
                       label("0: the line is right on average", 26, SUBDUED)).arrange(RIGHT, buff=0.2
                                                                                     ).to_edge(DOWN, buff=0.2)
        # "To check the straight-line assumption, fit a linear regression and average its errors, ..."
        self.play(FadeIn(head), *[FadeIn(VGroup(p[0], p[1], p[4])) for p in panels], run_time=self.share(0.15))
        # "... in ten groups along each input."
        cue(self, "in ten groups")
        self.play(*[AnimationGroup(Create(p[2]), FadeIn(p[3])) for p in panels], run_time=self.share(0.2))
        # "Where the line is right, the average stays near zero."
        cue(self, "Where the line")
        self.play(*[Indicate(p[1], color=INK, scale_factor=1.0) for p in panels], FadeIn(right),
                  run_time=self.share(0.1))
        # "For temperature it rises and falls: ..."
        cue(self, "For temperature")
        self.play(Indicate(temperature[2:4], color=VERMILION, scale_factor=1.08), run_time=self.share(0.1))
        # "... the line predicts too many animals in the coldest and warmest water, and too few in between, ..."
        cue(self, "the line predicts")
        self.play(FadeIn(hump, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def truth_layout(scene):
    shapes = scene.data("shapes")
    panels = {}
    for input_, x_name, x_range, ticks, centre in (
            ("depth_m", "depth (m)", [0, 200, 50], [0, 50, 100, 150, 200], 3.4 * LEFT),
            ("temperature_c", "temperature (°C)", [0, 18, 3], [0, 3, 6, 9, 12, 15, 18], 3.4 * RIGHT)):
        axes, frame = chart(x_range, [0, 1.1, 0.5], 5.6, 3.8, ticks, [0, 0.5, 1], x_name,
                            "relative to its peak" if input_ == "depth_m" else None)
        VGroup(axes, frame).move_to(centre + 0.5 * DOWN)
        rows = shapes[shapes["input"] == input_]
        forest = rows[rows["curve"] == "Random forest"]
        sim = rows[rows["curve"] == "Simulation"]
        model_lines = polyline(axes, forest["value"], forest["relative"], GREEN, 7)
        sim_line = dashed(polyline(axes, sim["value"], sim["relative"], INK, 5), 45)
        peaks = (forest.loc[forest["relative"].idxmax(), "value"], sim.loc[sim["relative"].idxmax(), "value"])
        panels[input_] = (axes, frame, model_lines, sim_line, peaks)
    key = VGroup(key_row(GREEN, "random forest", shape="line"),
                 key_row(INK, "the true curve, dashed", shape="line")).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.5)
    return panels, key


class Scene06(VideoScene):
    number = 6

    def construct(self):
        panels, key = truth_layout(self)
        axes, frame, model_lines, sim_line, _ = panels["temperature_c"]
        # "A random forest can bend, so it finds that hump without being told its shape, ..."
        self.play(FadeIn(panels["depth_m"][1]), FadeIn(frame), run_time=self.share(0.12))
        self.play(FadeIn(key[0]), Create(model_lines), run_time=self.share(0.3))
        # "... close to the true curve."
        cue(self, "close to the true")
        self.play(FadeIn(key[1]), Create(sim_line), run_time=self.share(0.25))
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        panels, key = truth_layout(self)
        t = panels["temperature_c"]
        self.add(key, panels["depth_m"][1], t[1], t[2], t[3])
        axes, frame, model_lines, sim_line, (forest_peak, true_peak) = panels["depth_m"]
        # "For depth, it does not. The forest puts the most animals at 17 metres, ..."
        self.play(Create(model_lines), run_time=self.share(0.18))
        cue(self, "The forest puts")
        line = DashedLine(axes.c2p(forest_peak, 0), axes.c2p(forest_peak, 1.05), color=GREEN, stroke_width=4)
        name = label(f"{forest_peak:.0f} m", 26, GREEN, weight=BOLD).next_to(line, UP, 0.1)
        self.play(FadeIn(VGroup(line, name)), run_time=self.share(0.12))
        # "... and the truth is 80."
        cue(self, "and the truth")
        mark_true = DashedLine(axes.c2p(true_peak, 0), axes.c2p(true_peak, 1.05), color=INK, stroke_width=4)
        true_name = label(f"{true_peak:.0f} m", 26, INK, weight=BOLD).next_to(mark_true, UP, 0.1)
        self.play(Create(sim_line), Create(mark_true), FadeIn(true_name), run_time=self.share(0.15))
        # "Nothing warned of it: the error check showed no pattern along depth."
        cue(self, "Nothing warned")
        shade = Rectangle(width=axes.c2p(true_peak, 0)[0] - axes.c2p(forest_peak, 0)[0], height=axes.y_length,
                          stroke_width=0, fill_color=VERMILION, fill_opacity=0.15
                          ).move_to(axes.c2p(forest_peak, 0), aligned_edge=DL)
        self.play(FadeIn(shade), run_time=self.share(0.1))
        self.play(Indicate(model_lines, color=VERMILION, scale_factor=1.02), run_time=self.share(0.1))
        # "A map drawn from this curve would send the next survey to the wrong depth."
        cue(self, "A map drawn")
        wrong = label("the next survey, sent to the wrong depth", 28, VERMILION, weight=BOLD
                      ).next_to(axes, DOWN, 0.9)
        self.play(FadeIn(wrong, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def node(text, colour, width=3.4):
    box = RoundedRectangle(width=width, height=1.2, corner_radius=0.2, stroke_color=colour, stroke_width=5,
                           fill_color=BACKGROUND, fill_opacity=1)
    return VGroup(box, label(text, 34, colour, weight=BOLD).move_to(box))


class Scene08(VideoScene):
    number = 8

    def construct(self):
        place = node("position", PURPLE).move_to(2.0 * UP)
        depth = node("depth", BLUE).move_to(4.0 * LEFT + 1.4 * DOWN)
        count = node("the species' count", INK, 4.4).move_to(3.8 * RIGHT + 1.4 * DOWN)
        follows = Arrow(place.get_bottom(), depth.get_top(), color=PURPLE, stroke_width=6, buff=0.15)
        follows_name = label("the shelf deepens offshore", 26, PURPLE).next_to(follows.get_center(), LEFT, 0.3)
        hidden = DashedLine(place.get_bottom(), count.get_top(), color=GREY, stroke_width=5, buff=0.15)
        hidden_tip = Arrow(hidden.get_end() + 0.5 * normalize(hidden.get_end() - hidden.get_start()) * -1,
                           hidden.get_end(), color=GREY, stroke_width=5, buff=0)
        hidden_name = label("something no input measures", 26, GREY).next_to(hidden.get_center(), RIGHT, 0.3)
        credited = Arrow(depth.get_right(), count.get_left(), color=VERMILION, stroke_width=7, buff=0.15)
        credited_name = label("ends up in depth's curve", 28, VERMILION, weight=BOLD).next_to(credited, DOWN, 0.75)
        name = VGroup(label("confounding", 56, VERMILION, weight=BOLD),
                      label("no choice of shape removes it", 30, INK)).arrange(RIGHT, buff=0.5
                                                                           ).to_edge(DOWN, buff=0.35)
        # "Depth follows position, because the shelf deepens offshore."
        self.play(FadeIn(place), FadeIn(depth), run_time=self.share(0.12))
        self.play(GrowArrow(follows), FadeIn(follows_name), run_time=self.share(0.15))
        # "So something about position that no input measures ..."
        cue(self, "So something")
        self.play(FadeIn(count), Create(hidden), FadeIn(hidden_tip), FadeIn(hidden_name), run_time=self.share(0.18))
        # "... ends up in depth's curve."
        cue(self, "ends up")
        self.play(GrowArrow(credited), FadeIn(credited_name), run_time=self.share(0.12))
        # "This is confounding."
        cue(self, "This is confounding")
        self.play(FadeIn(name[0], scale=1.2), run_time=self.share(0.08))
        cue(self, "and no choice")
        self.play(FadeIn(name[1], shift=0.2 * LEFT), run_time=self.share(0.08))
        self.finish()


class Scene09(KeyPointScene):
    number, point = 9, 1


# Rows are worth less than they seem (scenes 10–16) ------------------------------------------

def visit_squares(visits):
    """One square per station, in rows like a spreadsheet and in stacks by site."""
    counts = sorted(visits["visits"].astype(int), reverse=True)
    size = 0.1
    total = sum(counts)
    squares = VGroup(*[Square(size, stroke_width=0, fill_color=BLUE, fill_opacity=1) for _ in range(total)])
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
        sites = label(f"from {len(stacks)} sites", 48, BLUE, weight=BOLD).to_edge(UP, buff=0.5)
        # "The survey holds 800 stations, ..."
        self.play(FadeIn(head), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.002), run_time=self.share(0.15))
        # "... from only 160 sites visited again and again."
        cue(self, "from only")
        flat = VGroup(*[sq for stack in stacks for sq in stack])
        self.play(Transform(grid, flat), run_time=self.share(0.2))
        self.play(FadeOut(head, shift=0.3 * UP), FadeIn(sites, shift=0.3 * UP), run_time=self.share(0.08))
        # "Visits to one site share its depth, its seabed and its water, ..."
        cue(self, "Visits to one site")
        one = stacks[5]
        flat_one = VGroup(*grid[sum(len(s) for s in stacks[:5]):sum(len(s) for s in stacks[:6])])
        box = SurroundingRectangle(one, color=ORANGE, buff=0.08, stroke_width=4)
        name = label("one site: same depth, same seabed, same water", 30, ORANGE, weight=BOLD
                     ).next_to(stacks, UP, 0.3)
        self.play(flat_one.animate.set_fill(ORANGE), Create(box), run_time=self.share(0.12))
        self.play(FadeIn(name), run_time=self.share(0.1))
        self.finish()


class Scene11(VideoScene):
    """Schematic: draw stations, then whole sites, and watch the average move."""

    number = 11

    def construct(self):
        rng = np.random.default_rng(16)
        # Eight sites, each with its own level; a site's visits sit close to it.
        levels = np.array([0.6, 2.4, 1.0, 3.2, 1.6, 0.4, 2.8, 1.2])
        visits = [rng.integers(3, 7) for _ in levels]
        site_colours = [BLUE, ORANGE, GREEN, VERMILION, PURPLE, SKY, YELLOW, GREY]
        columns = VGroup()
        values = []
        for j, (level, n) in enumerate(zip(levels, visits)):
            v = np.clip(level + rng.normal(0, 0.25, n), 0.1, None)
            values.append(v)
            columns.add(VGroup(*[Dot(radius=0.13, color=site_colours[j]) for _ in range(n)]
                               ).arrange(UP, buff=0.12))
        columns.arrange(RIGHT, buff=0.75, aligned_edge=DOWN).move_to(1.2 * UP)
        site_names = label("eight sites, each visited several times", 28, SUBDUED).next_to(columns, UP, 0.3)
        everything = np.concatenate(values)

        scale = Line(4.5 * LEFT, 4.5 * RIGHT, color=GRID, stroke_width=4).move_to(2.2 * DOWN)
        scale_name = label("the average catch, one resample at a time", 26, SUBDUED).next_to(scale, DOWN, 0.25)
        centre = everything.mean()
        to_x = lambda v: (v - centre) * 5.5  # noqa: E731
        marker = Triangle(color=INK, fill_opacity=1).scale(0.18).rotate(PI).next_to(scale, UP, 0.05)
        trail = VGroup()
        mode = label("drawing stations", 32, BLUE, weight=BOLD).next_to(scale, UP, 0.9)
        mode_sites = label("drawing whole sites", 32, VERMILION, weight=BOLD).move_to(mode)

        def draw_stations(seed):
            r = np.random.default_rng(seed)
            picks = r.integers(0, len(everything), len(everything))
            return everything[picks].mean(), picks

        def draw_sites(seed):
            r = np.random.default_rng(seed)
            picks = r.integers(0, len(values), len(values))
            return np.concatenate([values[k] for k in picks]).mean(), picks

        flat = [d for c in columns for d in c]
        self.play(FadeIn(site_names), LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in columns], lag_ratio=0.1),
                  Create(scale), FadeIn(scale_name), run_time=self.share(0.14))
        # "To measure by how much, resample: draw stations at random, many times, ..."
        cue(self, "draw stations")
        self.play(FadeIn(mode), FadeIn(marker), run_time=self.share(0.05))
        for seed in range(4):
            mean, picks = draw_stations(seed)
            chosen = VGroup(*[flat[k] for k in set(picks)])
            self.play(Indicate(chosen, color=INK, scale_factor=1.25),
                      marker.animate.set_x(to_x(mean)), run_time=self.share(0.06))
            trail.add(Dot([to_x(mean), scale.get_y() + 0.32, 0], radius=0.07, color=BLUE))
            self.add(trail[-1])
        # "Then draw whole sites instead."
        cue(self, "Then draw")
        self.play(FadeOut(mode), FadeIn(mode_sites), run_time=self.share(0.04))
        for seed in range(4):
            mean, picks = draw_sites(seed + 10)
            chosen = VGroup(*[columns[k] for k in set(picks)])
            self.play(Indicate(chosen, color=INK, scale_factor=1.15),
                      marker.animate.set_x(to_x(mean)), run_time=self.share(0.05))
            trail.add(Dot([to_x(mean), scale.get_y() + 0.62, 0], radius=0.07, color=VERMILION))
            self.add(trail[-1])
        self.finish()


DRAWN = {"Single stations": ("drawing stations", BLUE, 2.5),
         "Whole sites": ("drawing sites", VERMILION, 1.5),
         "Whole blocks": ("drawing blocks", PURPLE, 0.5)}


def spread_of(scene, estimate, resampled):
    spreads = scene.data("spreads")
    return spreads[(spreads["estimate"] == estimate) & (spreads["resampled"] == resampled)].iloc[0]


def averages_layout(scene):
    """The bootstrap averages, one strip per way of drawing, for scenes 12–13."""
    averages = scene.data("averages")
    values = averages["average"]
    lo, hi = np.floor(values.min() * 2) / 2, np.ceil(values.max() * 2) / 2
    axes, frame = chart([lo, hi, 0.5], [0, 3, 1], 9.0, 3.3, list(np.arange(lo, hi + 0.01, 0.5)), [],
                        "average catch in a resample", None)
    VGroup(axes, frame).shift(1.6 * RIGHT + 0.55 * DOWN)
    rng = np.random.default_rng(17)
    strips, names = {}, {}
    for drawn, (name, colour, y) in DRAWN.items():
        v = averages[averages["drawn"] == drawn]["average"]
        strips[drawn] = VGroup(*[Dot(axes.c2p(a, y + rng.uniform(-0.3, 0.3)), radius=0.035, color=colour)
                                 .set_opacity(0.6) for a in v])
        names[drawn] = label(name, 28, colour, weight=BOLD).next_to(axes.c2p(lo, y), LEFT, 0.3)
    return frame, strips, names


class Scene12(VideoScene):
    number = 12

    def construct(self):
        frame, strips, names = averages_layout(self)
        sites = spread_of(self, "Average catch", "Whole sites")
        ratio = label(f"{sites['wider']:.2f} times wider", 40, VERMILION, weight=BOLD).to_edge(UP, buff=0.4)
        worth = label(f"worth about {round(sites['worth'], -1):.0f} independent stations", 38, INK, weight=BOLD
                      ).next_to(ratio, DOWN, 0.25)
        sample = label("the effective sample size", 30, SUBDUED).next_to(worth, DOWN, 0.12)
        # "Drawing whole sites spreads the average 1.31 times wider."
        self.play(FadeIn(frame), FadeIn(names["Single stations"]), FadeIn(names["Whole sites"]),
                  run_time=self.share(0.08))
        self.play(FadeIn(strips["Single stations"], lag_ratio=0.002), run_time=self.share(0.12))
        self.play(FadeIn(strips["Whole sites"], lag_ratio=0.002), run_time=self.share(0.12))
        self.play(FadeIn(ratio), run_time=self.share(0.08))
        # "The spread shrinks with the square root of the number of independent rows, so the
        # 800 stations are worth only about 470 independent ones: ..."
        cue(self, "stations are worth")
        self.play(FadeIn(worth, shift=0.2 * UP), run_time=self.share(0.1))
        # "... the survey's effective sample size."
        cue(self, "the survey's effective")
        self.play(FadeIn(sample), run_time=self.share(0.06))
        # "Count all 800, and an interval for the average comes out too narrow."
        cue(self, "Count all")
        stations = int(self.data("visits")["visits"].sum())
        narrow = label(f"count all {stations}: intervals too narrow", 30, VERMILION, weight=BOLD
                       ).to_edge(DOWN, buff=0.1)
        self.play(FadeIn(narrow, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


# The sites on a map in km, and the half-degree squares the page calls blocks.
KM_PER_DEGREE = (83, 111)
BLOCK_COLOURS = [BLUE, ORANGE, GREEN, VERMILION, PURPLE, SKY]


def block_map(scene, height=5.0, width=8.0, centre=0.4 * DOWN):
    sites = scene.data("sites")
    span_x = sites["x"].max() - sites["x"].min()
    span_y = sites["y"].max() - sites["y"].min()
    scale = min(height / span_y, width / span_x)
    mid = np.array([(sites["x"].max() + sites["x"].min()) / 2, (sites["y"].max() + sites["y"].min()) / 2])

    def to(x, y):
        return np.array([(x - mid[0]) * scale, (y - mid[1]) * scale, 0]) + centre

    dots = VGroup(*[Dot(to(x, y), radius=0.09, color=GREY) for x, y in zip(sites["x"], sites["y"])])
    blocks = list(dict.fromkeys(sites["block"]))
    squares = VGroup()
    for block in blocks:
        i, j = (int(v) for v in block.split())
        x0, y0 = i * 0.5 * KM_PER_DEGREE[0], j * 0.5 * KM_PER_DEGREE[1]
        corner, far = to(x0, y0), to(x0 + 0.5 * KM_PER_DEGREE[0], y0 + 0.5 * KM_PER_DEGREE[1])
        squares.add(Rectangle(width=far[0] - corner[0], height=far[1] - corner[1], stroke_color=GRID,
                              stroke_width=3).move_to((corner + far) / 2))
    colours = [BLOCK_COLOURS[(blocks.index(b) + int(b.split()[1])) % len(BLOCK_COLOURS)] for b in sites["block"]]
    return dots, squares, colours


class Scene13(VideoScene):
    number = 13

    def construct(self):
        dots, squares, colours = block_map(self)
        map_name = label("the sites on the map", 30, SUBDUED).to_edge(UP, buff=0.4)
        frame, strips, names = averages_layout(self)
        blocks = spread_of(self, "Average catch", "Whole blocks")
        ratio = label(f"{blocks['wider']:.2f} times wider", 40, PURPLE, weight=BOLD).to_edge(UP, buff=0.4)
        worth = label(f"worth only about {round(blocks['worth'], -1):.0f}", 38, INK, weight=BOLD
                      ).next_to(ratio, DOWN, 0.25)
        # "Neighbouring sites share their water too."
        self.play(FadeIn(map_name), FadeIn(dots), run_time=self.share(0.1))
        # "Draw whole squares of the map, each with every site in it, ..."
        cue(self, "Draw whole squares")
        self.play(Create(squares), run_time=self.share(0.12))
        self.play(*[d.animate.set_color(c) for d, c in zip(dots, colours)], run_time=self.share(0.1))
        # "... and the average spreads 2.34 times wider."
        cue(self, "and the average")
        self.play(FadeOut(VGroup(map_name, dots, squares)), FadeIn(frame), FadeIn(VGroup(*names.values())),
                  FadeIn(strips["Single stations"]), FadeIn(strips["Whole sites"]), run_time=self.share(0.1))
        self.play(FadeIn(strips["Whole blocks"], lag_ratio=0.002), FadeIn(ratio), run_time=self.share(0.12))
        # "Then the 800 stations are worth only about 150."
        cue(self, "Then the")
        self.play(FadeIn(worth, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def errors_layout(scene):
    """How many times wider each way of drawing spreads the average, as on the page, for scenes 14–15."""
    spreads = scene.data("spreads")
    order = list(DRAWN)
    axes, frame = chart([0, 3, 1], [0, 2.5, 0.5], 7.0, 4.4, [], [0, 1, 2], None, "times wider")
    VGroup(axes, frame).shift(2.4 * LEFT + 0.6 * DOWN)
    ticks = VGroup(*[label(DRAWN[d][0].replace("drawing ", "by "), 26, SUBDUED).next_to(axes.c2p(k + 0.5, 0), DOWN, 0.2)
                     for k, d in enumerate(order)])
    one = DashedLine(axes.c2p(0, 1), axes.c2p(3, 1), color=GREY, stroke_width=3)
    series = {}
    for estimate, colour in (("Average catch", VERMILION), ("Average forest error", BLUE)):
        rows = spreads[spreads["estimate"] == estimate].set_index("resampled").loc[order]
        points = [axes.c2p(k + 0.5, w) for k, w in enumerate(rows["wider"])]
        dots = VGroup(*[Dot(p, radius=0.12, color=colour) for p in points])
        lines = VGroup(*[Line(a, b, color=colour, stroke_width=6) for a, b in zip(points[:-1], points[1:])])
        values = VGroup(*[label(f"{w:.2f}", 28, colour, weight=BOLD).next_to(p, UP if colour == VERMILION else DOWN, 0.18)
                          for w, p in zip(rows["wider"], points)])
        series[estimate] = (dots, lines, values, rows["wider"].to_numpy(), points)
    key = VGroup(key_row(VERMILION, "the catch"), key_row(BLUE, "the forest's errors")
                 ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(4.4 * RIGHT + 2.3 * UP)
    return axes, VGroup(frame, ticks, one), series, key


class Scene14(VideoScene):
    number = 14

    def construct(self):
        axes, base, series, key = errors_layout(self)
        c_dots, c_lines, c_values, _, _ = series["Average catch"]
        e_dots, e_lines, e_values, _, _ = series["Average forest error"]
        verdict = VGroup(label("score the forest", 32, BLUE, weight=BOLD),
                         label("on sites it has never seen", 32, BLUE, weight=BOLD)
                         ).arrange(DOWN, buff=0.1).move_to(4.4 * RIGHT + 0.2 * DOWN)
        # "A model's inputs can explain some of this."
        self.play(FadeIn(base), FadeIn(key[0]), FadeIn(c_dots), Create(c_lines), FadeIn(c_values),
                  run_time=self.share(0.15))
        # "Resample a random forest's errors on sites it never saw, instead of the catch."
        cue(self, "Resample a random")
        self.play(FadeIn(key[1]), FadeIn(e_dots[0]), run_time=self.share(0.12))
        # "By site, they still spread 1.25 times wider, ..."
        cue(self, "By site")
        self.play(Create(e_lines[0]), FadeIn(e_dots[1]), FadeIn(e_values[1]), run_time=self.share(0.1))
        # "... almost as much as the catch: what a site's visits share, the inputs miss."
        cue(self, "almost as much")
        self.play(Indicate(VGroup(c_dots[1], e_dots[1]), scale_factor=1.3), run_time=self.share(0.1))
        # "So the forest must be scored on sites it has never seen."
        cue(self, "So the forest")
        self.play(FadeIn(verdict, shift=0.2 * LEFT), run_time=self.share(0.1))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        axes, base, series, key = errors_layout(self)
        c_dots, c_lines, c_values, catch, c_points = series["Average catch"]
        e_dots, e_lines, e_values, error, e_points = series["Average forest error"]
        self.add(base, key, c_dots, c_lines, c_values, e_dots[:2], e_lines[0], e_values[1])
        gap = Line(e_points[2], c_points[2], color=GREEN, stroke_width=10).shift(0.35 * RIGHT)
        explained = VGroup(label("explained by", 28, GREEN, weight=BOLD),
                           label("the forest's inputs", 28, GREEN, weight=BOLD),
                           label("depth, water", 26, SUBDUED)
                           ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(gap, RIGHT, 0.25)
        areas = VGroup(label("a map of unsurveyed areas:", 28, INK),
                       label("score on held-out areas", 32, VERMILION, weight=BOLD)
                       ).arrange(DOWN, buff=0.1).move_to(4.4 * RIGHT + 1.6 * DOWN)
        # "By block, the errors spread only 1.36 times wider, ..."
        self.play(Create(e_lines[1]), FadeIn(e_dots[2]), FadeIn(e_values[2]), run_time=self.share(0.15))
        # "... against 2.34 for the catch."
        cue(self, "against")
        self.play(Indicate(VGroup(c_dots[2], c_values[2]), color=VERMILION, scale_factor=1.3), run_time=self.share(0.1))
        # "Most of what neighbours share is their depth and water, and the forest already knows those."
        cue(self, "Most of what")
        self.play(Create(gap), FadeIn(explained), run_time=self.share(0.15))
        # "Some may remain, so a map of areas nobody has surveyed is scored on held-out areas."
        cue(self, "Some may remain")
        self.play(FadeIn(areas, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene16(KeyPointScene):
    number, point = 16, 2


# A model never says when it is guessing (scenes 17–25) -------------------------------------

BEYOND = {"Random forest": ("ten random forests, one per survey", BLUE),
          "Polynomial regression": ("ten polynomial regressions", PURPLE)}


def beyond_layout(scene, model="Random forest"):
    """Depth against mean count: the surveyed depths, each fit of one method, and the truth.
    Both methods share the axes, so scene 20 can swap one for the other."""
    beyond = scene.data("beyond")
    forest = beyond[beyond["model"] == model]
    truth = forest.groupby("depth")["true_mean"].mean()
    top = np.ceil(max(beyond["predicted"].max(), truth.max()) / 2) * 2
    axes, frame = chart([20, 180, 20], [0, top, 2], 10, 4.4, [20, 60, 100, 140, 180],
                        list(range(0, int(top) + 1, 2)), "depth (m)", "mean count")
    VGroup(axes, frame).shift(0.4 * RIGHT + 0.5 * DOWN)
    surveyed = Rectangle(width=axes.c2p(100, 0)[0] - axes.c2p(20, 0)[0], height=axes.y_length, stroke_width=0,
                         fill_color=BLUE, fill_opacity=0.08).move_to(axes.c2p(20, 0), aligned_edge=DL)
    beyond_area = Rectangle(width=axes.c2p(180, 0)[0] - axes.c2p(100, 0)[0], height=axes.y_length,
                            stroke_width=0, fill_color=GREY, fill_opacity=0.15).move_to(axes.c2p(100, 0),
                                                                                       aligned_edge=DL)
    surveyed_name = label("the survey: sites shallower than 100 m", 26, BLUE, weight=BOLD
                          ).next_to(surveyed, UP, 0.15)
    beyond_name = label("to map", 26, SUBDUED, weight=BOLD).next_to(beyond_area, UP, 0.15)
    truth_line = polyline(axes, truth.index, truth.values, INK, 9)
    name, colour = BEYOND[model]
    fits = {}
    for run, rows in forest.groupby("id"):
        rows = rows.sort_values("depth")
        within = rows[rows["depth"] <= 90]
        fits[run] = (polyline(axes, within["depth"], within["predicted"], colour, 4, 0.6),
                     polyline(axes, rows["depth"][rows["depth"] >= 90], rows["predicted"][rows["depth"] >= 90],
                              colour, 4, 0.6))
    truth_within = polyline(axes, truth.index[truth.index <= 90], truth.values[truth.index <= 90], INK, 9)
    truth_beyond = polyline(axes, truth.index[truth.index >= 90], truth.values[truth.index >= 90], INK, 9)
    key = VGroup(key_row(colour, name, shape="line"),
                 key_row(INK, "the true mean count", shape="line")).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    key.move_to(axes.c2p(140, top * 0.85) if model == "Random forest" else axes.c2p(120, top * 0.95))
    return axes, frame, VGroup(surveyed, surveyed_name, beyond_area, beyond_name), fits, \
        (truth_within, truth_beyond, truth_line), key


class Scene17(VideoScene):
    number = 17

    def construct(self):
        axes, frame, areas, fits, truth, key = beyond_layout(self)
        surveyed, surveyed_name, beyond_area, beyond_name = areas
        # "Survey effort is never even."
        self.play(FadeIn(frame), run_time=self.share(0.15))
        # "Suppose the survey reached only sites shallower than 100 metres, ..."
        cue(self, "Suppose")
        self.play(FadeIn(surveyed), FadeIn(surveyed_name), run_time=self.share(0.2))
        # "... and a model must map the deeper ones."
        cue(self, "and a model")
        self.play(FadeIn(beyond_area), FadeIn(beyond_name), run_time=self.share(0.15))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        axes, frame, areas, fits, (truth_within, truth_beyond, _), key = beyond_layout(self)
        self.add(frame, areas)
        # "Within the survey's depths, ten random forests follow the truth."
        self.play(Create(truth_within), FadeIn(key[1]), run_time=self.share(0.15))
        self.play(LaggedStart(*[Create(f[0]) for f in fits.values()], lag_ratio=0.1), FadeIn(key[0]),
                  run_time=self.share(0.2))
        # "Below, they run flat, while the true count keeps falling."
        cue(self, "Below")
        self.play(*[Create(f[1]) for f in fits.values()], run_time=self.share(0.2))
        cue(self, "while the true")
        self.play(Create(truth_beyond), run_time=self.share(0.12))
        # "A tree sends every deeper station to the leaf of the deepest stations it saw, ..."
        cue(self, "A tree sends")
        edge = VGroup(label("each tree repeats", 28, BLUE, weight=BOLD),
                      label("its value at the edge", 28, BLUE, weight=BOLD)
                      ).arrange(DOWN, buff=0.08).move_to(key)
        self.play(FadeOut(key), FadeIn(edge), run_time=self.share(0.08))
        self.play(*[Indicate(f[1], color=BLUE, scale_factor=1.0) for f in fits.values()],
                  run_time=self.share(0.12))
        self.finish()


def below_140(scene, axes, model):
    ratios = scene.data("ratios")
    below = ratios[(ratios["model"] == model) & (ratios["where"] == "below")]["ratio"]
    deep = Rectangle(width=axes.c2p(180, 0)[0] - axes.c2p(140, 0)[0], height=axes.y_length,
                     stroke_color=VERMILION, stroke_width=4, fill_color=VERMILION, fill_opacity=0.08
                     ).move_to(axes.c2p(140, 0), aligned_edge=DL)
    verdict = VGroup(label("below 140 m, on all ten surveys:", 30, VERMILION, weight=BOLD),
                     label(f"{below.min():.1f} to {below.max():.1f} times the truth", 36, VERMILION,
                           weight=BOLD)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
    return deep, verdict


class Scene19(VideoScene):
    number = 19

    def construct(self):
        axes, frame, areas, fits, (truth_within, truth_beyond, _), key = beyond_layout(self)
        self.add(frame, areas, truth_within, truth_beyond, key, *[f[0] for f in fits.values()],
                 *[f[1] for f in fits.values()])
        deep, verdict = below_140(self, axes, "Random forest")
        warning = label("no sign of it in the predictions", 30, INK).next_to(verdict, DOWN, 0.15)
        # "Below 140 metres they are too high on all ten surveys, ..."
        self.play(FadeOut(key), FadeOut(areas[1]), FadeOut(areas[3]), FadeIn(deep), run_time=self.share(0.15))
        self.play(FadeIn(verdict, shift=0.2 * DOWN), run_time=self.share(0.15))
        # "... and nothing in their predictions says so."
        cue(self, "and nothing")
        self.play(FadeIn(warning), run_time=self.share(0.12))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        axes, frame, areas, forests, (truth_within, truth_beyond, _), _ = beyond_layout(self)
        _, _, _, fits, _, key = beyond_layout(self, "Polynomial regression")
        deep, old_verdict = below_140(self, axes, "Random forest")
        old_warning = label("no sign of it in the predictions", 30, INK).next_to(old_verdict, DOWN, 0.15)
        lines = VGroup(*[f[0] for f in forests.values()], *[f[1] for f in forests.values()])
        self.add(frame, areas[0], areas[2], truth_within, truth_beyond, lines, deep, old_verdict, old_warning)
        _, verdict = below_140(self, axes, "Polynomial regression")
        rule = label("each method follows its own rule past the data", 30, INK).next_to(verdict, DOWN, 0.15)
        # "A polynomial regression fans out instead."
        self.play(FadeOut(lines), FadeOut(old_verdict), FadeOut(old_warning), FadeIn(key[0]),
                  run_time=self.share(0.1))
        self.play(LaggedStart(*[Create(f[0]) for f in fits.values()], lag_ratio=0.1), run_time=self.share(0.12))
        self.play(*[Create(f[1]) for f in fits.values()], run_time=self.share(0.12))
        # "Fits that agree within the survey bend in different directions below it, ..."
        cue(self, "Fits that agree")
        self.play(*[Indicate(f[0], color=PURPLE, scale_factor=1.0) for f in fits.values()], run_time=self.share(0.1))
        cue(self, "bend in different")
        self.play(*[Indicate(f[1], color=PURPLE, scale_factor=1.0) for f in fits.values()], run_time=self.share(0.1))
        # "... from 0.7 to 3.7 times the truth."
        cue(self, "from 0.7")
        self.play(FadeIn(verdict, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "Each method follows its own rule past the data."
        cue(self, "Each method")
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


NOVELTY_COLOURS = {"Surveyed": LIGHT, "Close to surveyed stations": SKY, "Outside a range": BLUE,
                   "Inside every range, far from the survey": ORANGE}


def novelty_layout(scene):
    stations = scene.data("novelty")
    depth, temp = stations["depth_m"], stations["temperature_c"]
    axes, frame = chart([0, 200, 50], [0, 20, 5], 7.0, 4.8, [0, 50, 100, 150, 200], [0, 5, 10, 15, 20],
                        "depth (m)", "temperature (°C)")
    VGroup(axes, frame).shift(2.6 * LEFT + 0.4 * DOWN)
    dots = {}
    for status, colour in NOVELTY_COLOURS.items():
        rows = (stations["status"] == status) & depth.notna() & temp.notna()
        dots[status] = VGroup(*[Dot(axes.c2p(d, t), radius=0.045 if status == "Surveyed" else 0.06,
                                    color=colour) for d, t in zip(depth[rows], temp[rows])])
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
    return frame, dots, VGroup(box, box_name), winter_dots, axes, surveyed


class Scene21(VideoScene):
    number = 21

    def construct(self):
        frame, dots, box, winter, axes, surveyed = novelty_layout(self)
        head = label("A survey in summer and autumn", 28, SUBDUED, weight=BOLD).move_to([1.5, 2.9, 0], aligned_edge=LEFT)
        key = key_row(LIGHT, "surveyed station").next_to(head, DOWN, 0.4, aligned_edge=LEFT)
        # "A new mix of conditions is harder to spot."
        self.play(FadeIn(frame), run_time=self.share(0.15))
        # "A survey in summer and autumn met cold water only at depth."
        cue(self, "A survey in")
        self.play(FadeIn(head), FadeIn(key), FadeIn(dots["Surveyed"], lag_ratio=0.001), run_time=self.share(0.25))
        cue(self, "cold water")
        cold = surveyed["temperature_c"] < 8
        cold_zone = Rectangle(width=axes.c2p(200, 0)[0] - axes.c2p(surveyed["depth_m"][cold].min(), 0)[0],
                              height=axes.c2p(0, 8)[1] - axes.c2p(0, 0)[1], stroke_color=BLUE, stroke_width=4,
                              fill_color=BLUE, fill_opacity=0.08
                              ).move_to(axes.c2p(surveyed["depth_m"][cold].min(), 0), aligned_edge=DL)
        cold_name = label("cold water: only at depth", 28, BLUE, weight=BOLD).next_to(key, DOWN, 0.4,
                                                                                       aligned_edge=LEFT)
        self.play(Create(cold_zone), FadeIn(cold_name), run_time=self.share(0.2))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        frame, dots, box, winter, axes, surveyed = novelty_layout(self)
        head = label("A survey in summer and autumn", 28, SUBDUED, weight=BOLD).move_to([1.5, 2.9, 0], aligned_edge=LEFT)
        key = VGroup(key_row(LIGHT, "surveyed station"), key_row(ORANGE, "winter station, far from")
                     ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(head, DOWN, 0.4, aligned_edge=LEFT)
        key_more = label("every surveyed station", 28).next_to(key[1], DOWN, 0.08, aligned_edge=LEFT).shift(
            0.46 * RIGHT)
        self.add(frame, dots["Surveyed"], head, key[0])
        inside = label("inside both ranges", 30, INK, weight=BOLD).next_to(key_more, DOWN, 0.6).align_to(key, LEFT)
        never = label("but never together", 30, ORANGE, weight=BOLD).next_to(inside, DOWN, 0.15, aligned_edge=LEFT)
        # "Winter brings cold water to the shallows."
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in winter], lag_ratio=0.01), FadeIn(key[1]),
                  FadeIn(key_more), run_time=self.share(0.3))
        # "Its depth and its temperature each lie within the survey's ranges, ..."
        cue(self, "Its depth")
        self.play(Create(box[0]), FadeIn(box[1]), FadeIn(inside), run_time=self.share(0.25))
        # "... but never together."
        cue(self, "but never")
        self.play(FadeIn(never), Indicate(winter, color=ORANGE, scale_factor=1.4), run_time=self.share(0.15))
        self.finish()


class Scene23(VideoScene):
    """Schematic: distance to the nearest surveyed station across all the inputs at once."""

    number = 23

    def construct(self):
        rng = np.random.default_rng(28)
        axes = plain_axes([-3, 3, 1], [-3, 3, 1], 5.6, 5.0).shift(2.6 * LEFT + 0.4 * DOWN)
        xl = label("depth, standardised", 26, SUBDUED).next_to(axes, DOWN, 0.2)
        yl = label("temperature, standardised", 26, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.2)
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
                       label("across depth, temperature,", 28, SUBDUED),
                       label("chlorophyll and salinity at once", 28, SUBDUED)
                       ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(3.6 * RIGHT + 0.6 * UP)
        far = VGroup(label("far from every surveyed station:", 28, INK),
                     label("flag it", 34, VERMILION, weight=BOLD)).arrange(DOWN, buff=0.12, aligned_edge=LEFT
                                                                           ).next_to(words, DOWN, 0.6, aligned_edge=LEFT)
        # "One check catches it: ..."
        self.play(FadeIn(axes), FadeIn(xl), FadeIn(yl), FadeIn(dots), run_time=self.share(0.15))
        self.play(FadeIn(station, scale=1.6), run_time=self.share(0.08))
        # "... the distance from each station to the nearest surveyed station, ..."
        cue(self, "the distance")
        self.play(Create(link), FadeIn(near_dot), FadeIn(words[:2]), run_time=self.share(0.2))
        # "... across all the inputs at once."
        cue(self, "across all")
        self.play(FadeIn(words[2:]), run_time=self.share(0.12))
        self.play(FadeIn(far), run_time=self.share(0.1))
        self.finish()


class Scene24(VideoScene):
    number = 24

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
        x_name = label("quarter of stations, by distance from the survey", 26, SUBDUED
                       ).next_to(bars, DOWN, 0.3).shift(0.0 * DOWN)
        head = label("The random forest's error", 34, SUBDUED).to_edge(UP, buff=0.5)
        advice = VGroup(label("map the distance", 34, BLUE, weight=BOLD),
                        label("beside the predictions", 34, BLUE, weight=BOLD)
                        ).arrange(DOWN, buff=0.12).move_to(4.6 * RIGHT + 0.6 * UP)
        # "The forest's error grew with that distance."
        self.play(FadeIn(head), FadeIn(frame), FadeIn(x_name), run_time=self.share(0.1))
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]))
                                for b in bars], lag_ratio=0.3), run_time=self.share(0.18))
        # "At the nearest quarter of stations it was typically off by a factor of 1.4; ..."
        cue(self, "At the nearest")
        self.play(Indicate(bars[0][:2], color=SKY), run_time=self.share(0.1))
        # "... at the furthest, by 2.7."
        cue(self, "at the furthest")
        self.play(Indicate(bars[3][:2], color=ORANGE), run_time=self.share(0.08))
        # "So map the distance beside the predictions, to show where the map is guessing."
        cue(self, "So map")
        self.play(FadeIn(advice, shift=0.2 * LEFT), run_time=self.share(0.15))
        self.finish()


class Scene25(KeyPointScene):
    number, point = 25, 3


# Quiz (scenes 26–27) -----------------------------------------------------------------------

class Scene26(QuizScene):
    number = 26
    question = ("Two random forests score", "almost the same error on new sites.",
                "One learnt from log counts.", "Do they predict the same total?")


class Scene27(VideoScene):
    number = 27

    def construct(self):
        totals = self.data("totals").set_index("model")
        raw, logged = totals.loc["Random forest"], totals.loc["Random forest on log counts"]
        caught = raw["caught_total"]
        top = np.ceil(max(caught, raw["predicted_total"]) / 500) * 500
        axes, frame = chart([0, top, 500], [0, 3, 1], 7.4, 3.6, list(range(0, int(top) + 1, 500)), [],
                            None, None, x_text=lambda v: f"{v:,.0f}")
        VGroup(axes, frame).shift(2.2 * RIGHT + 0.1 * UP)

        def row(value, y, colour, name, rmse=None):
            bar = Rectangle(width=value / top * axes.x_length, height=0.6, stroke_width=0, fill_color=colour,
                            fill_opacity=1).move_to(axes.c2p(0, y), aligned_edge=LEFT)
            number = label(f"{value:,.0f}", 30, colour, weight=BOLD).next_to(bar, RIGHT, 0.2)
            words = VGroup(label(name, 30, colour, weight=BOLD))
            if rmse is not None:
                words.add(label(f"RMSE {rmse:.2f}", 26, SUBDUED))
            words.arrange(DOWN, buff=0.08, aligned_edge=RIGHT).next_to(axes.c2p(0, y), LEFT, 0.3)
            return VGroup(bar, number, words)

        rows = [row(caught, 2.5, INK, "caught"),
                row(raw["predicted_total"], 1.5, BLUE, "forest on raw counts", raw["rmse"]),
                row(logged["predicted_total"], 0.5, VERMILION, "forest on log counts", logged["rmse"])]
        no = label("No.", 72, VERMILION, weight=BOLD).to_edge(UP, buff=0.3)
        short = 1 - logged["predicted_total"] / caught
        gap_name = label(f"{100 * short:.0f}% short", 32, VERMILION, weight=BOLD).next_to(rows[2][1], RIGHT, 0.35)
        reason = VGroup(label("a few large catches pull the average above the typical catch", 28, SUBDUED),
                        label("on log counts: the typical catch; a total needs the average", 30, INK,
                              weight=BOLD)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        # "No."
        self.play(FadeIn(no, scale=1.4), FadeIn(frame), run_time=self.share(0.06))
        # "The stations caught 2,421 animals."
        cue(self, "The stations caught")
        self.play(FadeIn(rows[0][2]), GrowFromEdge(rows[0][0], LEFT), FadeIn(rows[0][1]), run_time=self.share(0.1))
        # "The forest on raw counts predicts 2,514, ..."
        cue(self, "The forest on raw")
        self.play(FadeIn(rows[1][2]), GrowFromEdge(rows[1][0], LEFT), FadeIn(rows[1][1]), run_time=self.share(0.1))
        # "... and the forest on log counts 1,699, ..."
        cue(self, "and the forest on log")
        self.play(FadeIn(rows[2][2]), GrowFromEdge(rows[2][0], LEFT), FadeIn(rows[2][1]), run_time=self.share(0.1))
        # "... 30 per cent short."
        cue(self, "per cent short")
        self.play(FadeIn(gap_name, shift=0.2 * LEFT), run_time=self.share(0.08))
        # "A few large catches pull the average above the typical catch."
        cue(self, "A few large")
        self.play(FadeIn(reason[0], shift=0.2 * UP), run_time=self.share(0.08))
        # "On log counts the forest aims at the typical catch, but a total needs the average."
        cue(self, "On log counts")
        self.play(FadeIn(reason[1], shift=0.2 * UP), run_time=self.share(0.08))
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
