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


def dashed(line, n=50):
    return DashedVMobject(line, num_dashes=n)


def key_row(colour, text, size=28, shape="dot"):
    mark = Dot(radius=0.13, color=colour) if shape == "dot" else \
        Line(ORIGIN, 0.5 * RIGHT, color=colour, stroke_width=6)
    return VGroup(mark, label(text, size)).arrange(RIGHT, buff=0.2)


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("why a model can", "why rows", "and why a model"))


# The survey is simulated (scene 2, schematic) -----------------------------------------------

class Scene02(VideoScene):
    number = 2

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
        # "As in the other videos, the survey is simulated: we wrote the process that makes its counts."
        self.play(FadeIn(source, scale=0.9), run_time=self.share(0.12))
        self.play(GrowArrow(arrow), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(d, shift=0.4 * RIGHT) for d in field], lag_ratio=0.04),
                  FadeIn(field_name), run_time=self.share(0.25))
        # "So a model's answers can be checked against the truth, ..."
        cue(self, "So a model's")
        self.play(FadeIn(known, shift=0.2 * UP), run_time=self.share(0.1))
        self.play(Indicate(known, color=GREEN), run_time=self.share(0.15))
        self.finish()


# A model can fit well and still be wrong (scenes 3–8) ---------------------------------------

class Scene03(VideoScene):
    """Schematic: a hump a straight line misses and a forest follows in steps."""

    number = 3

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
        steps_name = label("random forest: many trees, steps", 30, GREEN, weight=BOLD)

        names = VGroup(line_name, steps_name).arrange(RIGHT, buff=1.2)
        names.scale_to_fit_width(min(names.width, 12.6)).to_edge(UP, buff=0.5)

        # "First, why a model can fit well and still be wrong. Few marine responses are straight lines."
        self.play(FadeIn(axes), FadeIn(xl), FadeIn(yl), run_time=self.share(0.06))
        cue(self, "Few marine")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02), run_time=self.share(0.08))
        # "A linear model, such as linear regression, assumes they are: ..."
        cue(self, "A linear model")
        self.play(Create(line), FadeIn(line_name), run_time=self.share(0.08))
        # "... each extra degree or metre always adds the same amount."
        cue(self, "each extra")
        self.play(Create(cross), line.animate.fade(0.7), run_time=self.share(0.05))
        # "A random forest, many decision trees averaged, does not."
        cue(self, "A random forest")
        self.play(FadeIn(steps_name), run_time=self.share(0.06))
        # "Its trees split the stations into groups, so it follows the data in steps, ..."
        cue(self, "Its trees split")
        self.play(Create(steps), run_time=self.share(0.14))
        self.play(Indicate(steps, color=GREEN, scale_factor=1.03), run_time=self.share(0.06))
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


class Scene04(VideoScene):
    number = 4

    def construct(self):
        panels, key = truth_layout(self)
        axes, frame, model_lines, sim_line, _ = panels["temperature_c"]
        # "Fit a random forest to the survey, ..."
        self.play(FadeIn(panels["depth_m"][1]), FadeIn(frame), run_time=self.share(0.08))
        # "... and draw how its prediction changes with temperature, with the other inputs held fixed."
        cue(self, "and draw how")
        self.play(FadeIn(key[0]), Create(model_lines), run_time=self.share(0.2))
        # "It finds a hump, a temperature where the species does best, without being told the shape."
        cue(self, "It finds a hump")
        hump = label("a hump: found, not told", 26, GREEN, weight=BOLD).next_to(axes.c2p(9, 1.0), UP, 0.25)
        self.play(FadeIn(plated(hump), shift=0.2 * DOWN), run_time=self.share(0.1))
        # "The dashed line is the true curve, the one the simulation used, ..."
        cue(self, "The dashed line")
        self.play(FadeIn(key[1]), Create(sim_line), run_time=self.share(0.2))
        # "... and the forest follows it closely."
        cue(self, "and the forest follows")
        self.play(Indicate(model_lines, color=GREEN, scale_factor=1.02), run_time=self.share(0.1))
        self.finish()


class Scene05(VideoScene):
    number = 5

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
        # "Yet the forest fits the survey well, and nothing in its predictions warns of the mistake."
        cue(self, "Yet the forest")
        shade = Rectangle(width=axes.c2p(true_peak, 0)[0] - axes.c2p(forest_peak, 0)[0], height=axes.y_length,
                          stroke_width=0, fill_color=VERMILION, fill_opacity=0.15
                          ).move_to(axes.c2p(forest_peak, 0), aligned_edge=DL)
        self.play(FadeIn(shade), run_time=self.share(0.1))
        cue(self, "and nothing in")
        self.play(Indicate(model_lines, color=VERMILION, scale_factor=1.02), run_time=self.share(0.1))
        # "A map drawn from this curve would send the next survey to the wrong depth."
        cue(self, "A map drawn")
        wrong = label("the next survey, sent to the wrong depth", 28, VERMILION, weight=BOLD
                      ).next_to(axes, DOWN, 1.05)
        self.play(FadeIn(wrong, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene06(VideoScene):
    """Schematic: moving offshore changes the depth and something no input measures, together."""

    number = 6

    def construct(self):
        seabed_y = lambda x: 1.3 - (x + 6.0) * 2.4 / 12.2  # noqa: E731
        surface = Line([-6.0, 2.2, 0], [6.2, 2.2, 0], color=BLUE, stroke_width=4)
        bed = Line([-6.0, seabed_y(-6.0), 0], [6.2, seabed_y(6.2), 0], color=SUBDUED, stroke_width=6)
        water = Polygon([-6.0, 2.2, 0], [6.2, 2.2, 0], bed.get_end(), bed.get_start(), stroke_width=0,
                        fill_color="#EAF2F8", fill_opacity=1)
        coast = label("coast", 28, SUBDUED, weight=BOLD).next_to(surface.get_start(), UP, 0.15)
        sea = label("open sea", 28, SUBDUED, weight=BOLD).next_to(surface.get_end(), UP, 0.15, aligned_edge=RIGHT)
        offshore = Arrow([-3.4, 2.75, 0], [3.4, 2.75, 0], color=INK, stroke_width=5, buff=0)
        offshore_name = label("moving offshore", 28, INK, weight=BOLD).next_to(offshore, UP, 0.1)
        xs = [-1.9, -0.5, 0.9, 2.3, 3.7, 5.1]
        drops = VGroup(*[DashedLine([x, 2.2, 0], [x, seabed_y(x), 0], color=GREY, stroke_width=3) for x in xs])
        stations = VGroup(*[Dot([x, seabed_y(x), 0], radius=0.1, color=INK) for x in xs])

        def row(y, colour):
            return VGroup(*[Square(0.62, stroke_width=0, fill_color=colour,
                                   fill_opacity=0.15 + 0.75 * k / (len(xs) - 1)).move_to([x, y, 0])
                            for k, x in enumerate(xs)])

        depth_row = row(-1.85, BLUE)
        hidden_fill = row(-2.75, PURPLE)

        def name_of(lines, colour, row_):
            return VGroup(*[label(t, 26, colour, weight=BOLD) for t in lines]).arrange(
                DOWN, buff=0.06, aligned_edge=RIGHT).next_to(row_, LEFT, 0.4)

        depth_name = name_of(["depth,", "which an input measures"], BLUE, depth_row)
        hidden_name = name_of(["something", "no input measures"], PURPLE, hidden_fill)
        pairs = VGroup(*[SurroundingRectangle(VGroup(a, b), color=ORANGE, buff=0.06, stroke_width=4)
                         for a, b in zip(depth_row, hidden_fill)])
        credit = label("depth takes the credit", 30, VERMILION, weight=BOLD)
        # "Why? The shelf deepens offshore."
        self.play(FadeIn(water), Create(surface), Create(bed), FadeIn(coast), FadeIn(sea),
                  run_time=self.share(0.1))
        self.play(GrowArrow(offshore), FadeIn(offshore_name), run_time=self.share(0.06))
        # "So moving away from the coast changes the depth, ..."
        cue(self, "So moving")
        self.play(LaggedStart(*[AnimationGroup(Create(d), FadeIn(st)) for d, st in zip(drops, stations)],
                              lag_ratio=0.15), run_time=self.share(0.1))
        self.play(FadeIn(depth_name), LaggedStart(*[FadeIn(q, shift=0.2 * UP) for q in depth_row], lag_ratio=0.2),
                  run_time=self.share(0.1))
        # "... but it can change other things too, things that no input measures."
        cue(self, "but it can")
        self.play(FadeIn(hidden_name), LaggedStart(*[FadeIn(q, shift=0.2 * UP) for q in hidden_fill],
                                                   lag_ratio=0.2), run_time=self.share(0.12))
        # "Both change together, station by station, so the forest cannot tell them apart."
        cue(self, "Both change")
        self.play(LaggedStart(*[Create(r) for r in pairs], lag_ratio=0.3), run_time=self.share(0.14))
        # "It sees only depth, ..."
        cue(self, "It sees only")
        self.play(FadeOut(pairs), hidden_fill.animate.set_fill(GREY, 0.2), hidden_name.animate.set_color(GREY),
                  run_time=self.share(0.08))
        # "... so depth takes the credit for both."
        cue(self, "so depth takes")
        credit.next_to(hidden_fill, DOWN, 0.35)
        self.play(depth_row.animate.set_fill(VERMILION), FadeIn(credit, shift=0.2 * UP),
                  run_time=self.share(0.1))
        self.finish()


def node(text, colour, width=3.4):
    box = RoundedRectangle(width=width, height=1.0, corner_radius=0.2, stroke_color=colour, stroke_width=5,
                           fill_color=BACKGROUND, fill_opacity=1)
    return VGroup(box, label(text, 32, colour, weight=BOLD).move_to(box))


def triangle(top, left, right, top_says, credit_says):
    """A hidden cause above an input and an outcome: arrows down to both, and the arrow
    between them that the data seem to show."""
    top = node(*top).move_to(1.0 * UP)
    left = node(*left).move_to(4.0 * LEFT + 1.5 * DOWN)
    right = node(*right).move_to(4.0 * RIGHT + 1.5 * DOWN)
    down = VGroup(Arrow(top.get_bottom(), left.get_top(), color=PURPLE, stroke_width=6, buff=0.12),
                  Arrow(top.get_bottom(), right.get_top(), color=PURPLE, stroke_width=6, buff=0.12))
    says = VGroup(label(top_says[0], 28, PURPLE).next_to(down[0].get_center(), UL, 0.15),
                  label(top_says[1], 28, PURPLE).next_to(down[1].get_center(), UR, 0.15))
    across = Arrow(left.get_right(), right.get_left(), color=VERMILION, stroke_width=7, buff=0.15)
    across_says = label(credit_says, 28, VERMILION, weight=BOLD).next_to(across, DOWN, 0.15)
    return top, VGroup(left, right), VGroup(down, says), VGroup(across, across_says)


class Scene07(VideoScene):
    number = 7

    def construct(self):
        name = label("confounding", 52, VERMILION, weight=BOLD).to_edge(UP, buff=0.3)
        meaning = label("a hidden cause, linked to both an input and the outcome", 30, INK
                        ).next_to(name, DOWN, 0.15)
        place, ends, down, across = triangle(("position", PURPLE), ("depth", BLUE),
                                             ("the species' count", INK, 4.4), ("sets", "changes"),
                                             "gets the credit")
        fish, birds_boats, draws, not_drawn = triangle(("the fish", PURPLE), ("fishing boats", BLUE, 3.8),
                                                       ("seabirds", INK), ("draw", "draw"), "do not draw")
        cross = Cross(Square(0.5), stroke_color=VERMILION, stroke_width=8).move_to(not_drawn[0])
        not_drawn[0].set_color(GREY)
        together = DashedLine(birds_boats[0].get_right(), birds_boats[1].get_left(), color=GREY, stroke_width=4,
                              buff=0.15)
        together_says = label("seen together", 28, GREY).next_to(together, UP, 0.15)
        fix = VGroup(label("a better fit cannot fix it:", 32, INK),
                     label("measure the hidden cause", 32, VERMILION, weight=BOLD)
                     ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        # "This is called confounding."
        self.play(FadeIn(name, scale=1.2), run_time=self.share(0.05))
        # "A confounder is a hidden cause linked to both an input and the outcome: ..."
        cue(self, "A confounder")
        self.play(FadeIn(meaning, shift=0.2 * UP), run_time=self.share(0.07))
        # "... here, position sets the depth and also changes the catch."
        cue(self, "here, position")
        self.play(FadeIn(place), FadeIn(ends), run_time=self.share(0.05))
        self.play(*[GrowArrow(a) for a in down[0]], FadeIn(down[1]), run_time=self.share(0.07))
        self.play(GrowArrow(across[0]), FadeIn(across[1]), run_time=self.share(0.05))
        # "Think of seabirds and fishing boats. They gather in the same places, ..."
        cue(self, "Think of")
        self.play(FadeOut(VGroup(place, ends, down, across)), FadeIn(birds_boats), run_time=self.share(0.06))
        cue(self, "They gather")
        self.play(Create(together), FadeIn(together_says), run_time=self.share(0.05))
        # "... but the boats do not draw the birds: ..."
        cue(self, "but the boats")
        self.play(FadeOut(together), FadeOut(together_says), GrowArrow(not_drawn[0]), FadeIn(not_drawn[1]),
                  run_time=self.share(0.05))
        self.play(Create(cross), run_time=self.share(0.03))
        # "... the fish draw both."
        cue(self, "the fish draw")
        self.play(FadeIn(fish), *[GrowArrow(a) for a in draws[0]], FadeIn(draws[1]), run_time=self.share(0.07))
        # "A better-fitting curve cannot fix this, because the data look the same either way."
        cue(self, "A better-fitting")
        self.play(FadeIn(fix[0], shift=0.2 * UP), run_time=self.share(0.06))
        # "Only measuring the hidden cause can."
        cue(self, "Only measuring")
        self.play(FadeIn(fix[1], shift=0.2 * UP), run_time=self.share(0.05))
        self.finish()


class Scene08(KeyPointScene):
    number, point = 8, 1


# Rows are worth less than they seem (scenes 9–13) ------------------------------------------

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


class Scene09(VideoScene):
    number = 9

    def construct(self):
        total, grid, stacks = visit_squares(self.data("visits"))
        head = label(f"{total} stations", 48, INK, weight=BOLD).to_edge(UP, buff=0.5)
        sites = label(f"from {len(stacks)} sites", 48, BLUE, weight=BOLD).to_edge(UP, buff=0.5)
        # "Next, why rows are worth less than they seem. The survey holds 800 stations, ..."
        cue(self, "The survey holds")
        self.play(FadeIn(head), run_time=self.share(0.06))
        self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.002), run_time=self.share(0.15))
        # "... from only 160 sites visited again and again."
        cue(self, "from only")
        flat = VGroup(*[sq for stack in stacks for sq in stack])
        self.play(Transform(grid, flat), run_time=self.share(0.2))
        self.play(FadeOut(head, shift=0.3 * UP), FadeIn(sites, shift=0.3 * UP), run_time=self.share(0.08))
        # "As the Marine data video showed, visits to one site share its depth, its seabed and its water, ..."
        cue(self, "visits to one site")
        one = stacks[5]
        flat_one = VGroup(*grid[sum(len(s) for s in stacks[:5]):sum(len(s) for s in stacks[:6])])
        box = SurroundingRectangle(one, color=ORANGE, buff=0.08, stroke_width=4)
        name = label("one site: same depth, same seabed, same water", 30, ORANGE, weight=BOLD
                     ).next_to(stacks, UP, 0.3)
        self.play(flat_one.animate.set_fill(ORANGE), Create(box), run_time=self.share(0.12))
        self.play(FadeIn(name), run_time=self.share(0.08))
        # "Ask one person the same question twice, and you get two answers but only one opinion."
        cue(self, "Ask one person")
        opinion = label("ask one person twice: two answers, one opinion", 30, ORANGE, weight=BOLD).move_to(name)
        self.play(FadeOut(name, shift=0.2 * UP), FadeIn(opinion, shift=0.2 * UP), run_time=self.share(0.08))
        # "Data like these are called dependent: each visit says something about the others."
        cue(self, "Data like these")
        dependent = label("dependent data: each visit says something about the others", 32, INK, weight=BOLD
                          ).to_edge(UP, buff=0.5)
        self.play(FadeOut(sites, shift=0.3 * UP), FadeIn(dependent, shift=0.3 * UP), run_time=self.share(0.08))
        self.finish()


class Scene10(VideoScene):
    """Schematic: draw stations, then whole sites, and watch the average move."""

    number = 10

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
        # "Draw stations at random, as many as the survey holds, so some come up twice and some not at all, ..."
        cue(self, "Draw stations")
        self.play(FadeIn(mode), FadeIn(marker), run_time=self.share(0.05))

        def station_draw(seed):
            mean, picks = draw_stations(seed)
            chosen = VGroup(*[flat[k] for k in set(picks)])
            self.play(Indicate(chosen, color=INK, scale_factor=1.25),
                      marker.animate.set_x(to_x(mean)), run_time=self.share(0.05))
            trail.add(Dot([to_x(mean), scale.get_y() + 0.32, 0], radius=0.07, color=BLUE))
            self.add(trail[-1])

        station_draw(0)
        # "... a survey that might have been."
        cue(self, "a survey that")
        might = label("each draw: a survey that might have been", 28, INK, weight=BOLD).move_to(site_names)
        self.play(FadeOut(site_names), FadeIn(might), run_time=self.share(0.05))
        # "Work out its average catch, and do it many times."
        cue(self, "Work out")
        for seed in range(1, 4):
            station_draw(seed)
        # "The more the averages move, the less sure the survey is of its average."
        cue(self, "The more the")
        self.play(Indicate(trail, color=BLUE, scale_factor=1.6), run_time=self.share(0.06))
        # "Then draw whole sites instead, each with all its visits, ..."
        cue(self, "Then draw whole")
        self.play(FadeOut(mode), FadeIn(mode_sites), run_time=self.share(0.04))
        for seed in range(4):
            mean, picks = draw_sites(seed + 10)
            chosen = VGroup(*[columns[k] for k in set(picks)])
            self.play(Indicate(chosen, color=INK, scale_factor=1.15),
                      marker.animate.set_x(to_x(mean)), run_time=self.share(0.05))
            trail.add(Dot([to_x(mean), scale.get_y() + 0.62, 0], radius=0.07, color=VERMILION))
            self.add(trail[-1])
        # "... because a new survey would bring new sites, not just new visits."
        cue(self, "because a new")
        new_sites = label("a new survey brings new sites, not just new visits", 28, VERMILION, weight=BOLD
                          ).move_to(site_names)
        self.play(FadeOut(might), FadeIn(new_sites), run_time=self.share(0.06))
        self.finish()


DRAWN = {"Single stations": ("drawing stations", BLUE, 2.0),
         "Whole sites": ("drawing sites", VERMILION, 1.0)}


def spread_of(scene, estimate, resampled):
    spreads = scene.data("spreads")
    return spreads[(spreads["estimate"] == estimate) & (spreads["resampled"] == resampled)].iloc[0]


def averages_layout(scene):
    """The bootstrap averages, one strip per way of drawing."""
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


class Scene11(VideoScene):
    number = 11

    def construct(self):
        frame, strips, names = averages_layout(self)
        sites = spread_of(self, "Average catch", "Whole sites")
        ratio = label(f"{sites['wider']:.2f} times wider", 40, VERMILION, weight=BOLD).to_edge(UP, buff=0.4)
        worth = label(f"worth about {round(sites['worth'], -1):.0f} independent stations", 38, INK, weight=BOLD
                      ).next_to(ratio, DOWN, 0.25)
        sample = label("the effective sample size: what the rows are really worth", 30, SUBDUED
                       ).next_to(worth, DOWN, 0.12)
        # "Drawing whole sites spreads the averages 1.31 times wider."
        self.play(FadeIn(frame), FadeIn(names["Single stations"]), FadeIn(names["Whole sites"]),
                  run_time=self.share(0.08))
        self.play(FadeIn(strips["Single stations"], lag_ratio=0.002), run_time=self.share(0.12))
        self.play(FadeIn(strips["Whole sites"], lag_ratio=0.002), run_time=self.share(0.12))
        self.play(FadeIn(ratio), run_time=self.share(0.08))
        # "That is the spread an average of only about 470 independent stations would have, ..."
        cue(self, "That is the spread")
        self.play(FadeIn(worth, shift=0.2 * UP), run_time=self.share(0.1))
        # "This is the survey's effective sample size: how many independent rows the data are really worth."
        cue(self, "the survey's effective")
        self.play(FadeIn(sample), run_time=self.share(0.06))
        # "Count all 800, and the survey seems surer of its average than it is."
        cue(self, "Count all")
        stations = int(self.data("visits")["visits"].sum())
        narrow = label(f"count all {stations} as independent: too sure of the average", 30, VERMILION, weight=BOLD
                       ).to_edge(DOWN, buff=0.1)
        self.play(FadeIn(narrow, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene12(VideoScene):
    """Schematic: visits held out from a site the model was fitted on, then the whole site."""

    number = 12

    def construct(self):
        def bin_(name, colour, x):
            box = RoundedRectangle(width=5.4, height=3.8, corner_radius=0.2, stroke_color=colour, stroke_width=5
                                   ).move_to([x, -0.9, 0])
            return VGroup(box, label(name, 32, colour, weight=BOLD).next_to(box, UP, 0.2))

        fitted, held = bin_("fitted", BLUE, -3.5), bin_("held out, to score", VERMILION, 3.5)

        def stack(n, colour):
            return VGroup(*[Square(0.42, stroke_width=0, fill_color=colour, fill_opacity=1) for _ in range(n)]
                          ).arrange(UP, buff=0.06)

        others = VGroup(*[stack(n, BLUE) for n in (4, 6, 5)]).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        others.move_to(fitted[0].get_bottom() + 0.35 * UP + 1.1 * LEFT, aligned_edge=DOWN)
        site = stack(5, ORANGE).move_to(2.6 * UP)
        site_name = label("one site's visits", 28, ORANGE, weight=BOLD).next_to(site, RIGHT, 0.3)
        kept = VGroup(*site[:3]).copy().arrange(UP, buff=0.06).next_to(others, RIGHT, 0.3, aligned_edge=DOWN)
        out = VGroup(*site[3:]).copy().arrange(UP, buff=0.06).move_to(held[0].get_bottom() + 0.35 * UP,
                                                                      aligned_edge=DOWN)
        seen = CurvedArrow(kept.get_top() + 0.1 * UP, out.get_top() + 0.1 * UP, angle=-PI / 4, color=ORANGE,
                           stroke_width=5)
        seen_name = plated(label("already seen", 30, ORANGE, weight=BOLD)).next_to(seen, UP, 0.1)
        too_good = label("its score: better than at a new site", 28, VERMILION, weight=BOLD
                         ).next_to(held[0], DOWN, 0.2)
        whole = site.copy().arrange(UP, buff=0.06).move_to(held[0].get_bottom() + 0.35 * UP, aligned_edge=DOWN)
        new_site = label("the whole site held out: a new site", 30, GREEN, weight=BOLD).move_to(too_good)
        # "The same goes for a model's score."
        self.play(FadeIn(fitted), FadeIn(held), FadeIn(others), run_time=self.share(0.1))
        # "Hold out a few visits to a site whose other visits were fitted, ..."
        cue(self, "Hold out")
        self.play(FadeIn(site), FadeIn(site_name), run_time=self.share(0.06))
        self.play(*[Transform(site[k], kept[k]) for k in range(3)],
                  *[Transform(site[3 + k], out[k]) for k in range(2)], FadeOut(site_name), run_time=self.share(0.12))
        # "... and the model has, in effect, seen that site already."
        cue(self, "and the model")
        self.play(Create(seen), FadeIn(seen_name), run_time=self.share(0.1))
        # "Its score looks better than it will be at a new site."
        cue(self, "Its score")
        self.play(FadeIn(too_good, shift=0.2 * UP), run_time=self.share(0.08))
        # "That is why the Generalisation video held out whole sites."
        cue(self, "That is why")
        self.play(FadeOut(seen), FadeOut(seen_name), FadeOut(too_good),
                  *[Transform(site[k], whole[k]) for k in range(5)], run_time=self.share(0.12))
        self.play(FadeIn(new_site, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


class Scene13(KeyPointScene):
    number, point = 13, 2


# A model never says when it is guessing (scenes 14–20) -------------------------------------

BEYOND = {"Random forest": ("ten random forests, one per survey", BLUE)}


def beyond_layout(scene, model="Random forest"):
    """Depth against mean count: the surveyed depths, each fit of one method, and the truth."""
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
    key.move_to(axes.c2p(140, top * 0.85))
    return axes, frame, VGroup(surveyed, surveyed_name, beyond_area, beyond_name), fits, \
        (truth_within, truth_beyond, truth_line), key


def extrapolation_name(key):
    return plated(VGroup(label("extrapolation:", 30, ORANGE, weight=BOLD),
                         label("predicting beyond the data", 28, INK)).arrange(DOWN, buff=0.1)).move_to(key)


class Scene14(VideoScene):
    number = 14

    def construct(self):
        axes, frame, areas, fits, (_, _, truth_line), key = beyond_layout(self)
        surveyed, surveyed_name, beyond_area, beyond_name = areas
        # "Finally, why a model never says when it is guessing. Survey effort is never even: ..."
        self.play(FadeIn(frame), run_time=self.share(0.12))
        # "Suppose the survey reached only sites shallower than 100 metres, ..."
        cue(self, "Suppose")
        self.play(FadeIn(surveyed), FadeIn(surveyed_name), run_time=self.share(0.1))
        # "... and a model must map the deeper ones."
        cue(self, "and a model")
        self.play(FadeIn(beyond_area), FadeIn(beyond_name), run_time=self.share(0.08))
        # "The line is the true average count at each depth."
        cue(self, "The line is")
        self.play(Create(truth_line), run_time=self.share(0.12))
        # "As in the Supervised learning video, predicting beyond the data is called extrapolation."
        cue(self, "predicting beyond")
        self.play(FadeIn(extrapolation_name(key)), run_time=self.share(0.08))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        axes, frame, areas, fits, (truth_within, truth_beyond, _), key = beyond_layout(self)
        extrapolation = extrapolation_name(key)
        self.add(frame, areas, truth_within, truth_beyond, extrapolation)
        # "Ten random forests, each fitted to a different part of the survey, follow the truth within its depths."
        self.play(FadeOut(extrapolation), FadeIn(key), run_time=self.share(0.1))
        self.play(LaggedStart(*[Create(f[0]) for f in fits.values()], lag_ratio=0.1), run_time=self.share(0.2))
        # "Beyond, they run flat, while the true count keeps falling."
        cue(self, "Beyond, they")
        self.play(*[Create(f[1]) for f in fits.values()], run_time=self.share(0.2))
        cue(self, "while the true")
        self.play(Indicate(truth_beyond, color=INK, scale_factor=1.0), run_time=self.share(0.12))
        # "Why? A tree only asks whether a station is deeper or shallower than depths it has seen."
        cue(self, "A tree only")
        edge = label("a tree asks: is a station deeper or shallower than depths it has seen?", 28, BLUE,
                     weight=BOLD).to_edge(UP, buff=0.3)
        self.play(FadeIn(edge), run_time=self.share(0.08))
        # "A station far deeper gets the same answers as the deepest station it saw, ..."
        cue(self, "A station far")
        leaf = label("far deeper: the same answers, the same leaf, the same prediction", 28, INK,
                     weight=BOLD).next_to(edge, DOWN, 0.15)
        self.play(FadeIn(leaf, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "... so it lands in the same leaf and gets the same prediction."
        cue(self, "so it lands")
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


class Scene16(VideoScene):
    number = 16

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


class Scene17(VideoScene):
    number = 17

    def construct(self):
        frame, dots, box, winter, axes, surveyed = novelty_layout(self)
        head = label("A survey in summer and autumn", 28, SUBDUED, weight=BOLD).move_to([1.0, 2.9, 0], aligned_edge=LEFT)
        key = key_row(LIGHT, "surveyed station").next_to(head, DOWN, 0.4, aligned_edge=LEFT)
        # "A new mix of conditions is harder to spot."
        self.play(FadeIn(frame), run_time=self.share(0.12))
        # "Here each dot is a station, placed by its depth and its temperature."
        cue(self, "Here each dot")
        self.play(FadeIn(key), FadeIn(dots["Surveyed"], lag_ratio=0.001), run_time=self.share(0.2))
        # "A survey that sailed only in summer and autumn met cold water only at depth."
        cue(self, "A survey that")
        self.play(FadeIn(head), run_time=self.share(0.08))
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


class Scene18(VideoScene):
    number = 18

    def construct(self):
        frame, dots, box, winter, axes, surveyed = novelty_layout(self)
        head = label("A survey in summer and autumn", 28, SUBDUED, weight=BOLD).move_to([1.0, 2.9, 0], aligned_edge=LEFT)
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
        self.play(FadeIn(never), Indicate(winter, color=ORANGE, scale_factor=1.4), run_time=self.share(0.12))
        # "The forest has no stations like these to learn from, so it is guessing here too."
        cue(self, "The forest has")
        guess = label("no stations like these: guessing", 30, VERMILION, weight=BOLD
                      ).next_to(never, DOWN, 0.5, aligned_edge=LEFT)
        self.play(FadeIn(guess, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene19(VideoScene):
    """Schematic: distance to the nearest surveyed station across all the inputs at once."""

    number = 19

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
                       label("across all the inputs at once", 28, SUBDUED)
                       ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(3.6 * RIGHT + 1.4 * UP)
        grew = VGroup(label("the forest's errors", 28, INK),
                      label("grew with it", 28, INK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT
                                                              ).next_to(words, DOWN, 0.5, aligned_edge=LEFT)
        advice = VGroup(label("map the distance", 34, BLUE, weight=BOLD),
                        label("beside the predictions", 34, BLUE, weight=BOLD)
                        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(grew, DOWN, 0.5, aligned_edge=LEFT)
        # "A check on one input at a time misses it."
        self.play(FadeIn(axes), FadeIn(xl), FadeIn(yl), FadeIn(dots), run_time=self.share(0.1))
        self.play(FadeIn(station, scale=1.6), run_time=self.share(0.05))
        # "A better check is the distance from each station to the nearest surveyed station, ..."
        cue(self, "the distance")
        self.play(Create(link), FadeIn(near_dot), FadeIn(words[:2]), run_time=self.share(0.15))
        # "... across all the inputs at once."
        cue(self, "across all")
        self.play(FadeIn(words[2]), run_time=self.share(0.06))
        # "On the survey, the forest's errors grew with that distance."
        cue(self, "On the survey")
        self.play(FadeIn(grew, shift=0.2 * UP), run_time=self.share(0.08))
        # "So map the distance beside the predictions, to show where the map is guessing."
        cue(self, "So map")
        self.play(FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene20(KeyPointScene):
    number, point = 20, 3


# Quiz (scenes 21–22) -----------------------------------------------------------------------

class Scene21(QuizScene):
    number = 21
    question = ("Two surveys each record 800 stations.", "One visits 800 sites, once each;",
                "the other, 160 sites, five times each.", "Which gives the surer average catch?")


class Scene22(VideoScene):
    """Schematic: 800 stations at their own sites against 160 sites visited five times, with the
    page's effective sample size for this video's survey."""

    number = 22

    def construct(self):
        def survey(stacks, per, colour):
            return VGroup(*[VGroup(*[Square(0.075, stroke_width=0, fill_color=colour, fill_opacity=1)
                                     for _ in range(per)]).arrange(UP, buff=0.015) for _ in range(stacks)])

        first = survey(800, 1, GREEN).arrange_in_grid(rows=20, buff=0.05)
        second = survey(160, 5, BLUE).arrange_in_grid(rows=8, buff=(0.12, 0.14), cell_alignment=DOWN)
        for group in (first, second):
            group.scale_to_fit_width(5.6)
            if group.height > 3.6:
                group.scale_to_fit_height(3.6)
        first.move_to(3.4 * LEFT + 0.4 * DOWN)
        second.move_to(3.4 * RIGHT + 0.4 * DOWN)
        top = max(first.get_top()[1], second.get_top()[1]) + 0.45
        first_name = label("800 sites, once each", 30, GREEN, weight=BOLD).move_to([first.get_x(), top, 0])
        second_name = label("160 sites, five times each", 30, BLUE, weight=BOLD).move_to([second.get_x(), top, 0])
        answer = label("The first.", 64, GREEN, weight=BOLD).to_edge(UP, buff=0.3)
        new_site = label("each station: a new site", 28, GREEN, weight=BOLD).next_to(first, DOWN, 0.35)
        repeat = label("visits repeat each other", 28, BLUE, weight=BOLD).next_to(second, DOWN, 0.35)
        worth = spread_of(self, "Average catch", "Whole sites")["worth"]
        fewer = label(f"this video's survey: worth about {round(worth, -1):.0f}", 28, INK, weight=BOLD
                      ).next_to(repeat, DOWN, 0.15)
        # "The first."
        self.play(FadeIn(answer, scale=1.3), FadeIn(first), FadeIn(first_name), FadeIn(second),
                  FadeIn(second_name), run_time=self.share(0.12))
        # "Each of its stations brings a new site."
        cue(self, "Each of its")
        self.play(FadeIn(new_site, shift=0.2 * UP), Indicate(first, color=GREEN, scale_factor=1.03),
                  run_time=self.share(0.12))
        # "In the second, visits to one site partly repeat each other, ..."
        cue(self, "In the second")
        self.play(FadeIn(repeat, shift=0.2 * UP), Indicate(second, color=BLUE, scale_factor=1.03),
                  run_time=self.share(0.12))
        # "... so its 800 stations are worth fewer: in this video's survey, about 470."
        cue(self, "in this video")
        self.play(FadeIn(fewer, shift=0.2 * UP), run_time=self.share(0.1))
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
