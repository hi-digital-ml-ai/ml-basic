"""Manim scenes for the interpretation video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/10-interpretation
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is built on three ideas from the section, each with the reason it matters:
test what a model relies on against random numbers and on more than one split, name
the interval you quote and check its coverage, and a good score cannot check the
records. Scenes marked "page results" read visuals/data/*.csv, which
tools/figures-for-video.R writes from the pages. The others are schematic: made-up
shapes, never numbers that could pass for survey results. The opening, key-point,
recap, quiz and end-card scenes are shared (mlbasic_video.py) and read PROMISES,
ANSWERS and RECAP from here. Consecutive scenes about one picture share a builder, so
each starts where the previous one ended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["Which inputs a model relies on",
            "Which interval to quote",
            "What a good score cannot check"]
ANSWERS = ["Test it against random numbers,\non more than one split",
           "Name the interval,\nand check its coverage\nat new sites",
           "A score compares the model\nwith the records,\nnever the records with the sea"]
RECAP = ["Test importance against random numbers",
         "Name the interval and check its coverage",
         "A good score cannot check the records"]

# The pages' colours: real inputs and the models in blue, the random columns in orange,
# anything that fails a check in vermilion.
LIGHT = "#C9CED2"
PALE_BLUE = "#EAF2F8"

INPUT_NAMES = {"depth_m": "depth", "temperature_c": "temperature",
               "chlorophyll_mg_m3": "chlorophyll", "salinity_psu": "salinity",
               "substrate": "seabed", "season": "season"}


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


def input_name(term):
    """A page's input or level as the video says it: "substrate: mud" is "seabed: mud"."""
    if term.startswith("random_"):
        return "random " + term.split("_")[1]
    base, _, level = term.partition(": ")
    name = INPUT_NAMES.get(base, base)
    return f"{name}: {level}" if level else name


def is_random(term):
    return term.startswith("random")


def pct(value):
    return f"{100 * value:.0f}%"


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


def ribbon(axes, xs, lower, upper, colour, opacity=0.25):
    points = [axes.c2p(x, y) for x, y in zip(xs, upper)] + \
             [axes.c2p(x, y) for x, y in zip(list(xs)[::-1], list(lower)[::-1])]
    return Polygon(*points, stroke_width=0, fill_color=colour, fill_opacity=opacity)


def card(text, colour=PURPLE, size=40):
    words = VGroup(*[label(t, size, colour, weight=BOLD) for t in text.split("\n")]).arrange(DOWN, buff=0.15)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def panel(width, height, colour, fill=BACKGROUND):
    return RoundedRectangle(width=width, height=height, corner_radius=0.2, stroke_color=colour,
                            stroke_width=5, fill_color=fill, fill_opacity=1)


def hbars(names, values, colours, top, length=6.4, height=0.34, step=0.46, size=26, digits=None):
    """Horizontal bars from a common left edge, the names right-aligned beside it.

    Returns rows of (name, bar, value label) and the x of the zero line, so a reference
    line can be drawn at any value."""
    rows = VGroup()
    for i, (name, value, colour) in enumerate(zip(names, values, colours)):
        y = -i * step
        bar = Rectangle(width=max(value / top * length, 0.001), height=height, stroke_width=0,
                        fill_color=colour, fill_opacity=1).move_to([0, y, 0], aligned_edge=LEFT)
        words = label(name, size, colour if colour != LIGHT else SUBDUED).next_to([0, y, 0], LEFT, 0.25)
        value_text = label(f"{value:.{digits}f}", size - 2, SUBDUED).next_to(bar, RIGHT, 0.15) \
            if digits is not None else VGroup()
        rows.add(VGroup(words, bar, value_text))
    return rows


def dots_table(rows, columns, colours, cell=0.42, gap=0.08, seed=1):
    """A small table drawn as shaded cells: one column per input, schematic."""
    rng = np.random.default_rng(seed)
    table = VGroup()
    for c, colour in zip(range(columns), colours):
        column = VGroup(*[Square(cell, stroke_width=0, fill_color=colour,
                                 fill_opacity=rng.uniform(0.25, 1.0)) for _ in range(rows)])
        column.arrange(DOWN, buff=gap)
        table.add(column)
    table.arrange(RIGHT, buff=gap)
    return table


# The opening (scenes 1–3) ------------------------------------------------------------------

class Scene01(LearnScene):
    number = 1

    @property
    def times(self):
        return tuple(position(self, p) for p in ("Which inputs", "Which interval", "And what"))


class Scene02(VideoScene):
    """Schematic: a score card, then the three questions a study has to answer as well."""

    number = 2

    def construct(self):
        score = VGroup(panel(4.0, 2.6, BLUE, PALE_BLUE),
                       VGroup(label("a score", 40, BLUE, weight=BOLD),
                              label("how well it predicts", 28, INK),
                              label("new sites", 28, INK)).arrange(DOWN, buff=0.15))
        score[1].move_to(score[0])
        score.move_to(4.2 * LEFT)
        questions = VGroup(*[VGroup(badge(i + 1, 0.26), label(t, 34)).arrange(RIGHT, buff=0.3)
                             for i, t in enumerate(["What did the model find?", "How sure is it?",
                                                    "Can the records be trusted?"])])
        questions.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(2.6 * RIGHT)
        more = label("a study has to say more", 32, SUBDUED, weight=BOLD).next_to(questions, UP, 0.7)
        brace = Brace(questions, LEFT, color=GRID)
        # "A score says how well a model predicts new sites."
        self.play(FadeIn(score, scale=0.9), run_time=self.share(0.12))
        # "A study has to say more: ..."
        cue(self, "A study")
        self.play(FadeIn(more), GrowFromCenter(brace), run_time=self.share(0.08))
        for row, phrase in zip(questions, ("what the", "how sure", "whether the")):
            cue(self, phrase)
            self.play(FadeIn(row, shift=0.3 * RIGHT), run_time=self.share(0.08))
        self.finish()


class Scene03(VideoScene):
    """Schematic: stations along a coast, then one station's columns as they are named."""

    number = 3

    def construct(self):
        rng = np.random.default_rng(10)
        coast = VMobject(color=GREY, stroke_width=5).set_points_smoothly(
            [[-6.4, 2.6, 0], [-5.2, 1.4, 0], [-5.6, 0.0, 0], [-4.6, -1.2, 0], [-5.0, -2.8, 0]])
        land = label("coast", 26, SUBDUED).move_to([-6.1, -0.6, 0])
        xs, ys = rng.uniform(-4.2, -0.8, 40), rng.uniform(-2.6, 2.6, 40)
        stations = VGroup(*[Dot([x, y, 0], radius=0.08, color=BLUE) for x, y in zip(xs, ys)])
        chosen = stations[7]
        ring = Circle(0.22, color=ORANGE, stroke_width=5).move_to(chosen)
        sim = label("one simulated survey", 32, SUBDUED, weight=BOLD).to_edge(UP, buff=0.5).shift(2.6 * LEFT)

        box = panel(5.0, 4.6, ORANGE).move_to(3.6 * RIGHT)
        head = label("one station", 32, ORANGE, weight=BOLD).next_to(box.get_top(), DOWN, 0.3)
        fields = VGroup(*[label(t, 32) for t in ("count of the species", "depth", "water temperature",
                                                   "seabed", "season")])
        fields.arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(head, DOWN, 0.35)
        fields[0].set_color(BLUE)
        link = DashedLine(ring.get_right(), box.get_left(), color=ORANGE, stroke_width=3)
        # "As throughout the course, the data are one simulated survey: ..."
        self.play(Create(coast), FadeIn(land), FadeIn(sim), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in stations], lag_ratio=0.02),
                  run_time=self.share(0.15))
        # "... counts of one species at coastal stations, ..."
        cue(self, "counts of one")
        self.play(Create(ring), Create(link), FadeIn(box), FadeIn(head), run_time=self.share(0.08))
        self.play(FadeIn(fields[0], shift=0.2 * RIGHT), run_time=self.share(0.05))
        # "... with the depth, the water temperature, the seabed and the season at each."
        for row, phrase in zip(fields[1:], ("the depth", "the water", "the seabed", "the season")):
            cue(self, phrase)
            self.play(FadeIn(row, shift=0.2 * RIGHT), run_time=self.share(0.05))
        self.finish()


# What a model relies on (scenes 4–13) -----------------------------------------------------

def tree_icon(colour=GREEN, height=0.7):
    crown = Triangle(color=colour, fill_color=colour, fill_opacity=1, stroke_width=0).scale(height / 2)
    trunk = Rectangle(width=0.08, height=height * 0.25, stroke_width=0, fill_color=GREY, fill_opacity=1)
    trunk.next_to(crown, DOWN, 0)
    return VGroup(crown, trunk)


class Scene04(VideoScene):
    """Schematic: a linear model's coefficients beside a forest with nothing to read."""

    number = 4

    def construct(self):
        left = panel(5.6, 4.6, BLUE).move_to(3.3 * LEFT + 0.2 * DOWN)
        left_head = label("linear model", 34, BLUE, weight=BOLD).next_to(left.get_top(), DOWN, 0.3)
        coefficients = VGroup()
        for i, (name, size) in enumerate((("depth", -1.0), ("temperature", 1.4), ("chlorophyll", 0.65),
                                          ("salinity", 0.15))):
            words = label(name, 28).move_to([-3.5, 0.8 - 0.75 * i, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=abs(size), height=0.36, stroke_width=0, fill_color=BLUE, fill_opacity=1)
            bar.move_to([-2.2, 0.8 - 0.75 * i, 0], aligned_edge=LEFT if size > 0 else RIGHT)
            coefficients.add(VGroup(words, bar))
        zero = Line([-2.2, 1.2, 0], [-2.2, -1.8, 0], color=GRID, stroke_width=3)
        coef_name = label("one coefficient per input", 26, SUBDUED).next_to(left.get_bottom(), UP, 0.3)

        right = panel(5.6, 4.6, GREEN).move_to(3.3 * RIGHT + 0.2 * DOWN)
        right_head = label("random forest", 34, GREEN, weight=BOLD).next_to(right.get_top(), DOWN, 0.3)
        trees = VGroup(*[tree_icon(GREEN, 0.55) for _ in range(24)]).arrange_in_grid(rows=4, buff=(0.35, 0.18))
        trees.move_to(right.get_center() + 0.1 * DOWN)
        question = label("?", 120, VERMILION, weight=BOLD).move_to(trees)
        forest_name = label("no numbers to read", 26, VERMILION, weight=BOLD).next_to(right.get_bottom(), UP, 0.3)
        # "A linear model shows what it relies on through its coefficients."
        self.play(FadeIn(left), FadeIn(left_head), Create(zero), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(c[0]) for c in coefficients], lag_ratio=0.2),
                  LaggedStart(*[GrowFromEdge(c[1], LEFT if c[1].get_left()[0] >= -2.21 else RIGHT)
                                for c in coefficients], lag_ratio=0.2),
                  FadeIn(coef_name), run_time=self.share(0.25))
        # "A random forest averages hundreds of trees, ..."
        cue(self, "A random forest")
        self.play(FadeIn(right), FadeIn(right_head), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in trees], lag_ratio=0.04), run_time=self.share(0.2))
        # "... and has no such numbers to read."
        cue(self, "and has no")
        self.play(trees.animate.set_opacity(0.3), FadeIn(question, scale=1.4), FadeIn(forest_name),
                  run_time=self.share(0.1))
        self.finish()


def shuffle_layout():
    """The schematic table of scenes 5 and 6: three inputs, the outcome, an error bar."""
    colours = [BLUE, BLUE, BLUE]
    table = dots_table(7, 3, colours, seed=3)
    outcome = dots_table(7, 1, [INK], seed=9)
    outcome.next_to(table, RIGHT, 0.35)
    whole = VGroup(table, outcome).move_to(3.2 * LEFT + 0.4 * DOWN)
    heads = VGroup(*[label(t, 28, BLUE if t != "count" else INK, weight=BOLD).next_to(col, UP, 0.2)
                     for t, col in zip(("A", "B", "C", "count"), [*table, outcome[0]])])
    return table, outcome, heads


def error_bars(before, after, x=0.6):
    base = -2.0
    first = Rectangle(width=1.0, height=before, stroke_width=0, fill_color=GREY, fill_opacity=1
                      ).move_to([x, base, 0], aligned_edge=DOWN)
    second = Rectangle(width=1.0, height=after, stroke_width=0, fill_color=GREY, fill_opacity=1
                       ).move_to([x + 1.8, base, 0], aligned_edge=DOWN)
    rise = Rectangle(width=1.0, height=after - before, stroke_width=0, fill_color=VERMILION, fill_opacity=1
                     ).move_to([x + 1.8, base + before, 0], aligned_edge=DOWN)
    floor = Line([x - 0.8, base, 0], [x + 2.6, base, 0], color=GRID, stroke_width=3)
    names = VGroup(label("before", 26, SUBDUED).next_to(first, DOWN, 0.2),
                   label("after", 26, SUBDUED).next_to(second, DOWN, 0.2))
    head = label("error on test sites", 28, SUBDUED, weight=BOLD).move_to([x + 0.9, 2.6, 0])
    return first, second, rise, floor, names, head


class Scene05(VideoScene):
    """Schematic: score, shuffle one input so its values change rows, score again."""

    number = 5

    def construct(self):
        table, outcome, heads = shuffle_layout()
        first, second, rise, floor, names, head = error_bars(1.6, 3.2)
        name = label("permutation importance", 44, BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        rise_name = label("the rise:\nits importance", 28, VERMILION, weight=BOLD)
        rise_name.next_to(rise, RIGHT, 0.3)
        # "Permutation importance asks from outside."
        self.play(FadeIn(name, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "Score the model on test sites."
        cue(self, "Score the model")
        self.play(FadeIn(table), FadeIn(outcome), FadeIn(heads), run_time=self.share(0.08))
        self.play(FadeIn(head), Create(floor), GrowFromEdge(first, DOWN), FadeIn(names[0]),
                  run_time=self.share(0.08))
        # "Then shuffle one input, so its values land on the wrong stations, ..."
        cue(self, "Then shuffle")
        column = table[1]
        order = np.random.default_rng(5).permutation(len(column))
        targets = [column[i].get_center() for i in order]
        outline = SurroundingRectangle(column, color=ORANGE, buff=0.08, stroke_width=5)
        self.play(Create(outline), heads[1].animate.set_color(ORANGE), run_time=self.share(0.05))
        self.play(*[cell.animate.move_to(target) for cell, target in zip(column, targets)],
                  run_time=self.share(0.15), rate_func=smooth)
        # "... and score again."
        cue(self, "and score again")
        self.play(GrowFromEdge(VGroup(second), DOWN), FadeIn(names[1]), run_time=self.share(0.06))
        # "The more the error rises, the more the model relied on that input."
        cue(self, "The more the error")
        self.play(FadeIn(rise), FadeIn(rise_name, shift=0.2 * LEFT), run_time=self.share(0.1))
        self.finish()


class Scene06(VideoScene):
    """Schematic: random columns join the inputs; their best score is the line to beat."""

    number = 6

    def construct(self):
        table, outcome, heads = shuffle_layout()
        heads[1].set_color(ORANGE)
        name = label("permutation importance", 44, BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(name, table, outcome, heads)
        noise = dots_table(7, 3, [ORANGE] * 3, seed=11).next_to(table, RIGHT, 0.08)
        noise_head = label("random numbers", 26, ORANGE, weight=BOLD).next_to(noise, UP, 0.65)
        everything = VGroup(table, noise, outcome, heads, noise_head)

        # The schematic scores: three inputs, three random columns, the best random as a line.
        scores = [("A", 2.6, BLUE), ("B", 1.9, BLUE), ("C", 0.45, LIGHT), ("random", 0.7, ORANGE),
                  ("random", 0.5, ORANGE), ("random", 0.3, ORANGE)]
        rows = hbars([s[0] for s in scores], [s[1] for s in scores], [s[2] for s in scores], 3.0,
                     length=4.0, height=0.36, step=0.55, size=28)
        rows.move_to(3.3 * RIGHT + 0.4 * DOWN)
        zero_x = rows[0][1].get_left()[0]
        line_x = zero_x + 0.7 / 3.0 * 4.0
        line = DashedLine([line_x, rows.get_top()[1] + 0.3, 0], [line_x, rows.get_bottom()[1] - 0.3, 0],
                          color=ORANGE, stroke_width=4)
        bar_name = label("every input gets some score", 28, SUBDUED).next_to(rows, UP, 0.5)
        noise_name = label("no better than noise", 28, VERMILION, weight=BOLD).next_to(rows, DOWN, 0.45)
        # "But every input gets some score."
        self.play(FadeIn(bar_name), *[FadeIn(r[0]) for r in rows[:3]],
                  *[GrowFromEdge(r[1], LEFT) for r in rows[:3]], run_time=self.share(0.12))
        # "To see what an unused input scores, add columns of random numbers as extra inputs."
        cue(self, "add columns")
        self.play(outcome.animate.shift((noise.width + 0.08) * RIGHT),
                  heads[3].animate.shift((noise.width + 0.08) * RIGHT), run_time=self.share(0.06))
        self.play(FadeIn(noise, shift=0.2 * DOWN), FadeIn(noise_head), run_time=self.share(0.08))
        self.play(*[FadeIn(r[0]) for r in rows[3:]], *[GrowFromEdge(r[1], LEFT) for r in rows[3:]],
                  run_time=self.share(0.08))
        # "An input that cannot beat them is used no more than noise."
        cue(self, "An input that")
        self.play(Create(line), run_time=self.share(0.06))
        self.play(Indicate(rows[2], color=VERMILION, scale_factor=1.05), FadeIn(noise_name),
                  run_time=self.share(0.12))
        self.finish()


class Scene07(VideoScene):
    """Page results: the forest's impurity importance, the random columns among the inputs."""

    number = 7

    def construct(self):
        table = self.data("impurity").sort_values("importance", ascending=False)
        names = [input_name(t) for t in table["input"]]
        top_random = max(i for i, t in enumerate(table["input"]) if is_random(t))
        colours = [ORANGE if is_random(t) else (BLUE if i < top_random else VERMILION)
                   for i, t in enumerate(table["input"])]
        rows = hbars(names, table["importance"], colours, 1.0, length=5.6, height=0.27, step=0.38, size=24)
        rows.move_to(1.4 * RIGHT + 0.45 * DOWN)
        head = VGroup(label("impurity importance", 40, GREEN, weight=BOLD),
                      label("the forest's own score, from its splits on the training data", 26, SUBDUED)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        below = VGroup(*[rows[i] for i in range(top_random + 1, len(rows))])
        brace = Brace(below, LEFT, color=VERMILION).shift(0.1 * LEFT)
        brace.next_to(VGroup(*[r[0] for r in below]), LEFT, 0.15)
        below_name = label("below the\nrandom\ncolumns", 26, VERMILION, weight=BOLD).next_to(brace, LEFT, 0.15)
        why = label("a random column: hundreds of places to split", 26, ORANGE, weight=BOLD
                    ).to_edge(DOWN, buff=0.15)
        # "A forest also has a quicker score built in, from its own splits on the training data."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT)) for r in rows],
                              lag_ratio=0.08), run_time=self.share(0.22))
        # "It ranked the three random columns above the seabed and the season."
        cue(self, "It ranked")
        randoms = VGroup(*[r for r, t in zip(rows, table["input"]) if is_random(t)])
        self.play(Indicate(randoms, color=ORANGE, scale_factor=1.05), run_time=self.share(0.1))
        self.play(GrowFromCenter(brace), FadeIn(below_name), run_time=self.share(0.08))
        # "A random column offers a tree hundreds of places to split, ..."
        cue(self, "A random column")
        self.play(FadeIn(why, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


def rise_colours(table, best_random):
    return [ORANGE if is_random(t) else (BLUE if r > best_random else LIGHT)
            for t, r in zip(table["input"], table["rise"])]


class Scene08(VideoScene):
    """Page results: permutation importance on one split's test sites."""

    number = 8

    def construct(self):
        table = self.data("permutation").sort_values("rise", ascending=False)
        sites = int(self.data("one-split")["test_sites"].iloc[0])
        best_random = table.loc[table["input"].map(is_random), "rise"].max()
        shown = table["rise"].clip(lower=0)
        top = table["rise"].max() * 1.05
        rows = hbars([input_name(t) for t in table["input"]], shown, rise_colours(table, best_random), top,
                     length=6.0, height=0.34, step=0.5, size=28)
        rows.move_to(1.0 * RIGHT + 0.5 * DOWN)
        zero_x = rows[0][1].get_left()[0]
        line_x = zero_x + best_random / top * 6.0
        line = DashedLine([line_x, rows.get_top()[1] + 0.25, 0], [line_x, rows.get_bottom()[1] - 0.25, 0],
                          color=ORANGE, stroke_width=4)
        line_name = label("best random column", 24, ORANGE, weight=BOLD).next_to(line, DOWN, 0.1)
        head = VGroup(label("permutation importance", 40, BLUE, weight=BOLD),
                      label("rise in RMSE when shuffled, on one split's test sites", 26, SUBDUED)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        held = label(f"{sites} test sites", 32, VERMILION, weight=BOLD).to_corner(DR, buff=0.5)
        above = VGroup(*[r for r, t, v in zip(rows, table["input"], table["rise"])
                         if not is_random(t) and v > best_random])
        # "Permutation importance on test sites does better."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT)) for r in rows],
                              lag_ratio=0.08), run_time=self.share(0.2))
        # "But one split holds back only 39 sites, ..."
        cue(self, "But one split")
        self.play(FadeIn(held, scale=1.2), run_time=self.share(0.08))
        # "... and on it, only temperature and the seabed beat the random columns."
        cue(self, "and on it")
        self.play(Create(line), FadeIn(line_name), run_time=self.share(0.08))
        self.play(Indicate(above, color=BLUE, scale_factor=1.05), run_time=self.share(0.12))
        self.finish()


class Scene09(VideoScene):
    """Page results: on how many of the ten splits each input beat the random columns."""

    number = 9

    def construct(self):
        beats = self.data("beats").sort_values("splits_above_random", ascending=False)
        splits = int(self.data("one-split")["splits"].iloc[0])
        names = [input_name(t) for t in beats["input"]]
        counts = beats["splits_above_random"].astype(int)
        colours = [BLUE if c > splits / 2 else LIGHT for c in counts]
        bars = hbars(names, counts, colours, splits, length=6.4, height=0.42, step=0.66, size=32)
        bars.move_to(0.6 * DOWN)
        rows = VGroup(*[VGroup(b[0], b[1], label(f"{c} of {splits}", 30, INK, weight=BOLD).next_to(
            [b[1].get_right()[0], b[1].get_y(), 0], RIGHT, 0.2)) for b, c in zip(bars, counts)])
        head = VGroup(label(f"on {splits} splits of the sites", 40, BLUE, weight=BOLD),
                      label("how often each input beat all three random columns", 28, SUBDUED)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        report = label("report the count, not a rank from one split", 30, INK, weight=BOLD
                       ).to_edge(DOWN, buff=0.3)
        order = list(beats["input"])

        def row_of(term):
            return rows[order.index(term)]

        # "So repeat it on ten splits."
        self.play(FadeIn(head, shift=0.2 * DOWN), *[FadeIn(r[0]) for r in rows], run_time=self.share(0.1))
        # "Temperature beats the random columns on all ten; ..."
        cue(self, "Temperature beats")
        self.play(GrowFromEdge(row_of("temperature_c")[1], LEFT), FadeIn(row_of("temperature_c")[2]),
                  run_time=self.share(0.08))
        # "... depth, chlorophyll and the seabed on most; ..."
        cue(self, "depth, chlorophyll")
        most = [row_of(t) for t in ("depth_m", "chlorophyll_mg_m3", "substrate")]
        self.play(*[GrowFromEdge(r[1], LEFT) for r in most], *[FadeIn(r[2]) for r in most],
                  run_time=self.share(0.1))
        # "... salinity on one."
        cue(self, "salinity on one")
        rest = [row_of(t) for t in order if t not in ("temperature_c", "depth_m", "chlorophyll_mg_m3",
                                                      "substrate")]
        self.play(*[GrowFromEdge(r[1], LEFT) for r in rest], *[FadeIn(r[2]) for r in rest],
                  run_time=self.share(0.08))
        # "That count is the number worth reporting, not a rank from one split."
        cue(self, "That count")
        self.play(FadeIn(report, shift=0.2 * UP), *[Indicate(r[2], color=BLUE) for r in rows],
                  run_time=self.share(0.12))
        self.finish()


class Scene10(VideoScene):
    """Schematic: set one input to each value at every station, predict, average, repeat."""

    number = 10

    def construct(self):
        axes, frame = chart([0, 10, 1], [0, 1.2, 0.5], 9.0, 4.0, [], [], "temperature", "prediction")
        VGroup(axes, frame).shift(0.7 * DOWN)
        rng = np.random.default_rng(2)
        xs = np.linspace(0, 10, 41)
        scales = rng.uniform(0.3, 1.0, 8)
        shapes = [s * np.exp(-((xs - 4.0 - rng.normal(0, 0.3)) / 2.4) ** 2) + 0.1 for s in scales]
        stations = VGroup(*[polyline(axes, xs, ys, GREY, 3, 0.7) for ys in shapes])
        average = np.mean(shapes, axis=0)
        name = label("partial dependence", 44, BLUE, weight=BOLD).to_edge(UP, buff=0.35)
        how = label("importance says how much, not in which direction", 28, SUBDUED).next_to(name, DOWN, 0.15)
        steps = VGroup(*[label(t, 26, INK) for t in ("set temperature to one value at every station",
                                                     "predict", "average", "repeat along its range")])
        steps.arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.2)
        for i in range(1, len(steps)):
            steps[i].set_color(SUBDUED)
        if steps.width > 13:
            steps.scale_to_fit_width(13)

        # "Importance says how much, but not in which direction."
        self.play(FadeIn(how), FadeIn(frame), run_time=self.share(0.12))
        # "A partial dependence plot shows the shape: ..."
        cue(self, "A partial dependence")
        self.play(FadeIn(name, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "... set temperature to one value at every station, ..."
        cue(self, "set temperature")
        k = 12
        sweep = DashedLine(axes.c2p(xs[k], 0), axes.c2p(xs[k], 1.15), color=ORANGE, stroke_width=4)
        marks = VGroup(*[Dot(axes.c2p(xs[k], ys[k]), radius=0.07, color=GREY) for ys in shapes])
        self.play(FadeIn(steps[0]), Create(sweep), run_time=self.share(0.08))
        # "... predict, ..."
        cue(self, "predict,")
        self.play(steps[1].animate.set_color(INK), LaggedStart(*[FadeIn(m, scale=0.5) for m in marks],
                                                               lag_ratio=0.1), run_time=self.share(0.06))
        # "... average, ..."
        cue(self, "average,")
        mean_dot = Dot(axes.c2p(xs[k], average[k]), radius=0.11, color=BLUE)
        self.play(steps[2].animate.set_color(INK), *[m.animate.move_to(mean_dot) for m in marks],
                  FadeIn(mean_dot), run_time=self.share(0.06))
        self.remove(marks)
        # "... and repeat along its range."
        cue(self, "and repeat")
        curve = polyline(axes, xs, average, BLUE, 8)
        self.play(steps[3].animate.set_color(INK), Create(curve),
                  sweep.animate.move_to(axes.c2p(xs[-1], 0.575)), run_time=self.share(0.15))
        self.play(FadeOut(sweep), FadeIn(stations), run_time=self.share(0.06))
        self.finish()


class Scene11(VideoScene):
    """Page results: the forest's partial dependence on temperature, then each station's curve."""

    number = 11

    def construct(self):
        partial = self.data("partial").sort_values("value")
        ice = self.data("ice")
        changes = self.data("ice-changes").iloc[0]
        top = np.ceil(max(ice[".pred"].quantile(0.99), partial[".pred"].max()) * 1.05)
        lo, hi = partial["value"].min(), partial["value"].max()
        axes, frame = chart([np.floor(lo), np.ceil(hi), 1], [0, top, 2], 7.4, 4.4,
                            list(range(int(np.ceil(lo)), int(np.floor(hi)) + 1, 2)),
                            list(range(0, int(top) + 1, 4)), "temperature (°C)", "predicted count")
        VGroup(axes, frame).shift(0.4 * DOWN + 2.0 * LEFT)
        rng = np.random.default_rng(1)
        highest = ice.groupby("station")[".pred"].max()
        chosen = rng.choice(highest[highest <= top].index, 80, replace=False)
        curves = VGroup()
        for station in chosen:
            rows = ice[ice["station"] == station].sort_values("value")
            curves.add(polyline(axes, rows["value"], rows[".pred"], GREY, 2, 0.45))
        average = polyline(axes, partial["value"], partial[".pred"], BLUE, 9)
        peak = changes["peak"]
        peak_line = DashedLine(axes.c2p(peak, 0), axes.c2p(peak, top), color=BLUE, stroke_width=4)
        peak_name = label(f"{peak:.1f} °C", 30, BLUE, weight=BOLD).next_to(peak_line, UP, 0.1)
        head = label("the forest's partial dependence", 34, BLUE, weight=BOLD).to_edge(UP, buff=0.35)
        stations = int(changes["stations"])
        rows_text = VGroup(label(f"one curve per station: {stations}", 28, SUBDUED, weight=BOLD),
                           label(f"rise to the peak: all but {stations - int(changes['rise'])}", 26, INK),
                           label(f"fall after it: all but {stations - int(changes['fall'])}", 26, INK)
                           ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(4.6 * RIGHT + 0.4 * DOWN)
        # "The forest predicts the most animals in cool water, near 7.7 degrees."
        self.play(FadeIn(head), FadeIn(frame), run_time=self.share(0.1))
        self.play(Create(average), run_time=self.share(0.18))
        cue(self, "near")
        self.play(Create(peak_line), FadeIn(peak_name), run_time=self.share(0.08))
        # "Drawn station by station, the curve rises and falls at nearly every one of the 598."
        cue(self, "Drawn station")
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.02), run_time=self.share(0.25))
        self.add_foreground_mobjects(average)
        cue(self, "rises and falls")
        self.play(FadeIn(rows_text, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene12(VideoScene):
    """Page results: the GAM's temperature curve with its interval, then RMSE on the same folds."""

    number = 12

    def construct(self):
        curves = self.data("gam-curve")
        gam = curves[curves["model"] == "GAM"].sort_values("value")
        lo, hi = gam["value"].min(), gam["value"].max()
        axes, frame = chart([np.floor(lo), np.ceil(hi), 1], [0, 1.3, 0.5], 5.4, 3.6,
                            list(range(int(np.ceil(lo)), int(np.floor(hi)) + 1, 3)), [0, 0.5, 1],
                            "temperature (°C)", "relative to its peak")
        VGroup(axes, frame).move_to(3.4 * LEFT + 0.5 * DOWN)
        band = ribbon(axes, gam["value"], gam["lower"], gam["upper"].clip(upper=1.3), BLUE, 0.2)
        line = polyline(axes, gam["value"], gam[".pred"], BLUE, 8)
        left_head = label("a GAM, read from its parts", 30, BLUE, weight=BOLD).next_to(frame, UP, 0.35)
        band_name = label("with its interval", 26, BLUE).next_to(axes, DOWN, 1.0)

        comparison = self.data("comparison").set_index("Model")
        models = [("GAM", "GAM", BLUE), ("Random forest", "random forest", GREEN),
                  ("Predicting the average", "the average", GREY)]
        values = [comparison.loc[m, "RMSE"] for m, _, _ in models]
        top = np.ceil(max(values))
        rows = hbars([n for _, n, _ in models], values, [c for _, _, c in models], top,
                     length=3.6, height=0.5, step=0.85, size=30, digits=2)
        rows.move_to(3.6 * RIGHT + 0.3 * DOWN)
        right_head = label("RMSE on new sites (individuals)", 26, SUBDUED, weight=BOLD).next_to(rows, UP, 0.5)
        folds = label("the same folds of sites", 26, SUBDUED).next_to(right_head, UP, 0.12)
        cost = label("reading cost no accuracy", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.3)
        # "A GAM draws the same hump from its own parts, with an interval."
        self.play(FadeIn(left_head), FadeIn(frame), run_time=self.share(0.08))
        self.play(Create(line), run_time=self.share(0.12))
        cue(self, "with an interval")
        self.play(FadeIn(band), FadeIn(band_name), run_time=self.share(0.06))
        # "Scored on the same folds of sites, it predicted new sites as well as the forest: ..."
        cue(self, "Scored on")
        self.play(FadeIn(folds), FadeIn(right_head), *[FadeIn(r[0]) for r in rows], run_time=self.share(0.08))
        # "... an RMSE of 4.34 against 4.43."
        cue(self, "an RMSE")
        self.play(GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]), run_time=self.share(0.06))
        self.play(GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.06))
        self.play(GrowFromEdge(rows[2][1], LEFT), FadeIn(rows[2][2]), run_time=self.share(0.05))
        # "On this survey, reading the model cost no accuracy."
        cue(self, "On this survey")
        self.play(FadeIn(cost, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene13(KeyPointScene):
    number, point = 13, 1


# How sure a prediction is (scenes 14–21) ---------------------------------------------------

def interval_layout():
    """Schematic: one station's prediction with a narrow and a wide interval, on a count axis."""
    axis = NumberLine(x_range=[0, 10, 1], length=10, include_ticks=False, color=GRID, stroke_width=3)
    axis.move_to(1.6 * DOWN)
    axis_name = label("animals caught at one station", 26, SUBDUED).next_to(axis, DOWN, 0.75)
    centre = 3.4
    prediction = Dot(axis.n2p(centre), radius=0.14, color=INK)
    pred_name = label("prediction", 26, INK).next_to(prediction, DOWN, 0.2)

    def bar(low, high, y, colour):
        return VGroup(Line(axis.n2p(low) + y * UP, axis.n2p(high) + y * UP, color=colour, stroke_width=10),
                      Line(axis.n2p(low) + (y - 0.2) * UP, axis.n2p(low) + (y + 0.2) * UP, color=colour,
                           stroke_width=6),
                      Line(axis.n2p(high) + (y - 0.2) * UP, axis.n2p(high) + (y + 0.2) * UP, color=colour,
                           stroke_width=6))

    narrow = bar(2.9, 3.9, 1.6, BLUE)
    wide = bar(0.3, 8.3, 0.5, ORANGE)
    narrow_name = label("confidence interval", 30, BLUE, weight=BOLD).next_to(narrow, UP, 0.2)
    wide_name = label("prediction interval", 30, ORANGE, weight=BOLD).next_to(wide, UP, 0.2).shift(2.4 * RIGHT)
    return axis, axis_name, prediction, pred_name, narrow, wide, narrow_name, wide_name


class Scene14(VideoScene):
    number = 14

    def construct(self):
        axis, axis_name, prediction, pred_name, narrow, wide, _, _ = interval_layout()
        head = label("a prediction needs a range", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        two = label("two ranges, two questions", 32, SUBDUED).next_to(head, DOWN, 0.2)
        # "A prediction needs a range, ..."
        self.play(FadeIn(head), Create(axis), FadeIn(axis_name), run_time=self.share(0.15))
        self.play(FadeIn(prediction, scale=0.5), FadeIn(pred_name), run_time=self.share(0.1))
        # "... and there are two."
        cue(self, "and there are two")
        self.play(GrowFromCenter(narrow), run_time=self.share(0.12))
        self.play(GrowFromCenter(wide), run_time=self.share(0.12))
        # "They answer different questions."
        cue(self, "They answer")
        self.play(FadeIn(two), run_time=self.share(0.1))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        axis, axis_name, prediction, pred_name, narrow, wide, narrow_name, wide_name = interval_layout()
        self.add(axis, axis_name, prediction, pred_name, narrow, wide)
        narrow_q = label("where the average catch lies", 26, BLUE).next_to(narrow_name, UP, 0.1)
        wide_q = label("where one new catch may land", 26, ORANGE).next_to(wide_name, UP, 0.1)
        rng = np.random.default_rng(8)
        catches = np.clip(rng.gamma(2.0, 1.7, 26), 0.1, 9.6)
        dots = VGroup(*[Dot(axis.n2p(c) + (0.14 + 0.1 * (i % 3)) * UP, radius=0.07, color=GREY)
                        for i, c in enumerate(catches)])
        # "A confidence interval says where the average catch lies, at stations like this one."
        self.play(FadeIn(narrow_name), Indicate(narrow, color=BLUE, scale_factor=1.05), run_time=self.share(0.12))
        cue(self, "says where the average")
        self.play(FadeIn(narrow_q, shift=0.2 * UP), run_time=self.share(0.1))
        # "A prediction interval says where one new catch may land, ..."
        cue(self, "A prediction interval")
        self.play(FadeIn(wide_name), Indicate(wide, color=ORANGE, scale_factor=1.03), run_time=self.share(0.1))
        self.play(FadeIn(wide_q, shift=0.2 * UP), run_time=self.share(0.08))
        # "... so it adds the scatter of single catches."
        cue(self, "so it adds")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05), run_time=self.share(0.2))
        self.finish()


class Scene16(VideoScene):
    """Schematic: catches at new sites fall on an interval and are counted inside or outside."""

    number = 16

    def construct(self):
        axis = NumberLine(x_range=[0, 10, 1], length=10, include_ticks=False, color=GRID, stroke_width=3)
        axis.move_to(0.4 * DOWN)
        low, high = 1.0, 7.2
        band = Rectangle(width=axis.n2p(high)[0] - axis.n2p(low)[0], height=0.9, stroke_color=ORANGE,
                         stroke_width=5, fill_color=ORANGE, fill_opacity=0.12
                         ).move_to((axis.n2p(low) + axis.n2p(high)) / 2)
        head = label("checking an interval", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        sub = label("catches at new sites", 28, SUBDUED).next_to(head, DOWN, 0.15)
        rng = np.random.default_rng(12)
        values = np.concatenate([rng.uniform(low + 0.2, high - 0.2, 16), [0.4, 8.4, 9.3]])
        rng.shuffle(values)
        dots = VGroup(*[Dot(axis.n2p(v) + 2.4 * UP, radius=0.1, color=GREY) for v in values])
        inside, outside = VGroup(), VGroup()
        tally_in = label("inside", 30, GREEN, weight=BOLD).move_to(5.4 * LEFT + 2.2 * DOWN)
        tally_out = label("outside", 30, VERMILION, weight=BOLD).move_to(3.4 * RIGHT + 2.2 * DOWN)
        coverage = label("coverage: the share inside", 36, INK, weight=BOLD).to_edge(DOWN, buff=0.25)
        # "To check an interval, count how many catches at new sites fall inside it."
        self.play(FadeIn(head), FadeIn(sub), Create(axis), FadeIn(band), run_time=self.share(0.12))
        self.play(FadeIn(tally_in), FadeIn(tally_out), run_time=self.share(0.05))
        moves = []
        for i, (d, v) in enumerate(zip(dots, values)):
            ok = low <= v <= high
            colour = GREEN if ok else VERMILION
            target = (tally_in if ok else tally_out).get_right() + RIGHT * (0.35 + 0.28 * (len(inside) if ok
                                                                                           else len(outside)))
            (inside if ok else outside).add(d)
            moves.append(Succession(FadeIn(d, shift=0.3 * DOWN, run_time=0.3),
                                    d.animate(run_time=0.3).move_to(axis.n2p(v)).set_color(colour),
                                    d.animate(run_time=0.3).move_to(target).set_color(colour)))
        self.play(LaggedStart(*moves, lag_ratio=0.25), run_time=self.share(0.55))
        # "That share is its coverage."
        cue(self, "That share")
        self.play(FadeIn(coverage, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


def coverage_rows(items, promise=0.9, length=6.0, step=1.25):
    """Coverage bars from 0 to 100%, each with a name and a width, and a dashed line at the promise."""
    rows = VGroup()
    for i, (name, colour, coverage, width) in enumerate(items):
        y = -i * step
        track = Rectangle(width=length, height=0.55, stroke_color=GRID, stroke_width=2
                          ).move_to([0, y, 0], aligned_edge=LEFT)
        bar = Rectangle(width=max(coverage * length, 0.001), height=0.55, stroke_width=0, fill_color=colour,
                        fill_opacity=1).move_to([0, y, 0], aligned_edge=LEFT)
        value = label(pct(coverage), 34, colour, weight=BOLD).next_to(track, RIGHT, 0.25)
        words = VGroup(label(name, 28, colour, weight=BOLD),
                       label(f"{width:.1f} animals wide", 24, SUBDUED)).arrange(DOWN, buff=0.06, aligned_edge=RIGHT)
        words.next_to([0, y, 0], LEFT, 0.3)
        rows.add(VGroup(words, track, bar, value))
    x = promise * length
    line = DashedLine([x, 0.6, 0], [x, -(len(items) - 1) * step - 0.6, 0], color=INK, stroke_width=4)
    line_name = label(f"{pct(promise)} promised", 24, INK).next_to(line, UP, 0.1)
    return rows, VGroup(line, line_name)


class Scene17(VideoScene):
    """Page results: the GAM's two intervals, their widths and their coverage at the test sites."""

    number = 17

    def construct(self):
        table = self.data("gam-intervals").set_index("interval")
        average, catch = table.loc["For the average"], table.loc["For a new catch"]
        rows, promise = coverage_rows([("for the average", BLUE, average["coverage"], average["width"]),
                                       ("for a new catch", ORANGE, catch["coverage"], catch["width"])])
        VGroup(rows, promise).move_to(0.8 * RIGHT + 0.2 * DOWN)
        head = VGroup(label("the GAM's 90% intervals", 38, INK, weight=BOLD),
                      label("share of catches inside, at the test sites", 26, SUBDUED)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        wrong = label(f"as a range for the next catch: wrong at {pct(1 - average['coverage'])} of stations",
                      30, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.35)
        # "The GAM's interval for the average, 2.5 animals wide, ..."
        self.play(FadeIn(head), FadeIn(promise), *[FadeIn(r[1]) for r in rows], run_time=self.share(0.1))
        self.play(FadeIn(rows[0][0]), run_time=self.share(0.06))
        # "... held 20 per cent of the catches at the test sites."
        cue(self, "held 20")
        self.play(GrowFromEdge(rows[0][2], LEFT), FadeIn(rows[0][3]), run_time=self.share(0.08))
        # "Its interval for a new catch, 11.6 wide, held 96 per cent."
        cue(self, "Its interval")
        self.play(FadeIn(rows[1][0]), run_time=self.share(0.06))
        cue(self, "held 96")
        self.play(GrowFromEdge(rows[1][2], LEFT), FadeIn(rows[1][3]), run_time=self.share(0.08))
        # "Quote the narrow one as a range for the next catch, and it is wrong four times in five."
        cue(self, "Quote the narrow")
        self.play(Indicate(rows[0], color=VERMILION, scale_factor=1.03), FadeIn(wrong, shift=0.2 * UP),
                  run_time=self.share(0.12))
        self.finish()


class Scene18(VideoScene):
    """Schematic: errors on calibration sites, sorted; nine in ten become the half-width."""

    number = 18

    def construct(self):
        rng = np.random.default_rng(4)
        errors = np.sort(rng.gamma(1.6, 0.55, 20))
        errors = errors / errors.max() * 2.6
        bars = VGroup(*[Rectangle(width=0.26, height=e, stroke_width=0, fill_color=GREY, fill_opacity=1)
                        for e in errors]).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        bars.move_to(3.0 * LEFT + 0.6 * DOWN)
        head = label("conformal prediction", 44, BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        none = label("a random forest gives no interval of its own", 28, SUBDUED).next_to(head, DOWN, 0.15)
        bars_name = label("its errors on calibration sites, sorted", 26, SUBDUED).next_to(bars, DOWN, 0.3)
        held = label("held back from fitting", 24, SUBDUED).next_to(bars_name, DOWN, 0.1)
        k = int(np.ceil(0.9 * len(errors))) - 1
        mark = bars[k]
        nine = label("nine in ten are smaller", 26, BLUE, weight=BOLD)
        level = DashedLine([bars.get_left()[0], mark.get_top()[1], 0], mark.get_corner(UR), color=BLUE,
                           stroke_width=4)
        nine.next_to(level, UP, 0.15).align_to(level, LEFT)

        centre = np.array([3.6, -0.6, 0])
        half = errors[k]
        prediction = Dot(centre, radius=0.14, color=INK)
        pred_name = label("a prediction", 26, INK).next_to(prediction, LEFT, 0.3)
        up = Line(centre, centre + half * UP, color=BLUE, stroke_width=8)
        down = Line(centre, centre + half * DOWN, color=BLUE, stroke_width=8)
        caps = VGroup(Line(centre + half * UP + 0.25 * LEFT, centre + half * UP + 0.25 * RIGHT, color=BLUE,
                           stroke_width=6),
                      Line(centre + half * DOWN + 0.25 * LEFT, centre + half * DOWN + 0.25 * RIGHT, color=BLUE,
                           stroke_width=6))
        either = label("as far either side", 26, BLUE, weight=BOLD).next_to(up, RIGHT, 0.3)
        # "A random forest gives no interval of its own."
        self.play(FadeIn(none), run_time=self.share(0.1))
        # "Conformal prediction makes one: ..."
        cue(self, "Conformal")
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "... measure its errors on calibration sites, held back from fitting, ..."
        cue(self, "measure its errors")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(bars_name),
                  run_time=self.share(0.2))
        cue(self, "held back")
        self.play(FadeIn(held), run_time=self.share(0.05))
        # "... and reach as far either side as nine errors in ten."
        cue(self, "and reach")
        self.play(mark.animate.set_color(BLUE), Create(level), FadeIn(nine), run_time=self.share(0.1))
        self.play(FadeIn(prediction), FadeIn(pred_name), run_time=self.share(0.05))
        self.play(TransformFromCopy(mark, up), TransformFromCopy(mark, down), run_time=self.share(0.12))
        self.play(FadeIn(caps), FadeIn(either), run_time=self.share(0.06))
        self.finish()


class Scene19(VideoScene):
    """Page results: the forest's conformal interval at the test sites."""

    number = 19

    def construct(self):
        conformal = self.data("conformal").iloc[0]
        rows, promise = coverage_rows([("random forest", GREEN, conformal["coverage"], conformal["width"])])
        VGroup(rows, promise).move_to(0.6 * RIGHT + 0.2 * UP)
        head = VGroup(label("a conformal 90% interval", 38, INK, weight=BOLD),
                      label("share of catches inside, at the test sites", 26, SUBDUED)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.5)
        note = label("from a model with no distribution", 32, BLUE, weight=BOLD).to_edge(DOWN, buff=0.8)
        # "At the test sites, the forest's interval held 90 per cent of the catches, just as promised, ..."
        self.play(FadeIn(head), FadeIn(rows[0][0]), FadeIn(rows[0][1]), FadeIn(promise), run_time=self.share(0.15))
        cue(self, "held 90")
        self.play(GrowFromEdge(rows[0][2], LEFT), FadeIn(rows[0][3]), run_time=self.share(0.12))
        cue(self, "just as promised")
        self.play(Indicate(promise, color=GREEN), run_time=self.share(0.1))
        # "... from a model with no distribution at all."
        cue(self, "from a model")
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene20(VideoScene):
    """Page results: calibrated on little chlorophyll, used where chlorophyll is highest."""

    number = 20

    def construct(self):
        shift = self.data("shift")
        forest = shift[shift["interval"] == "Forest, conformal"].set_index("stations")
        same, rich = forest.loc["Like the calibration sites"], forest.loc["Most chlorophyll"]
        rows, promise = coverage_rows([("like the calibration sites", GREEN, same["coverage"], same["width"]),
                                       ("most chlorophyll", VERMILION, rich["coverage"], rich["width"])])
        VGroup(rows, promise).move_to(0.6 * RIGHT + 0.4 * DOWN)
        head = VGroup(label("calibrated on stations with little chlorophyll", 34, INK, weight=BOLD),
                      label("the forest's conformal 90% interval, share of catches inside", 26, SUBDUED)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        silent = label("same label, same width, no warning", 32, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.3)
        # "Now calibrate it on stations with little chlorophyll, ..."
        self.play(FadeIn(head), FadeIn(promise), *[FadeIn(r[1]) for r in rows], run_time=self.share(0.1))
        self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][2], LEFT), FadeIn(rows[0][3]), run_time=self.share(0.1))
        # "... and use it where chlorophyll is highest."
        cue(self, "and use it")
        self.play(FadeIn(rows[1][0]), run_time=self.share(0.06))
        # "It holds only 73 per cent, under the same label and at the same width."
        cue(self, "It holds only")
        self.play(GrowFromEdge(rows[1][2], LEFT), FadeIn(rows[1][3]), run_time=self.share(0.1))
        cue(self, "under the same")
        self.play(Indicate(VGroup(rows[0][0][1], rows[1][0][1]), color=INK), run_time=self.share(0.1))
        # "Nothing in the interval says its promise has lapsed."
        cue(self, "Nothing in")
        self.play(FadeIn(silent, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene21(KeyPointScene):
    number, point = 21, 2


# What a good score cannot check (scenes 22–27) ---------------------------------------------

def ground(kind, colour, centre, rng, kept=1.0):
    """Schematic: a patch of seabed with its animals; a share of them missed by the gear."""
    box = panel(5.2, 3.4, colour).move_to(centre)
    name = label(kind, 32, colour, weight=BOLD).next_to(box, UP, 0.2)
    xs, ys = rng.uniform(-2.2, 2.2, 16), rng.uniform(-1.2, 0.9, 16)
    animals = VGroup(*[Dot(centre + np.array([x, y, 0]), radius=0.13, color=INK) for x, y in zip(xs, ys)])
    missed = VGroup(*[a for i, a in enumerate(animals) if i % 2 == 1]) if kept < 1 else VGroup()
    return box, name, animals, missed


class Scene22(VideoScene):
    number = 22

    def construct(self):
        rng = np.random.default_rng(3)
        sand = ground("sand", ORANGE, 3.3 * LEFT + 0.4 * DOWN, rng)
        rock = ground("rock", GREY, 3.3 * RIGHT + 0.4 * DOWN, rng, kept=0.5)
        chain = VGroup(*[label(t, 30, INK, weight=BOLD) for t in ("the gear", "the records", "the model")])
        arrows = VGroup()
        chain.arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.4)
        for a, b in zip(chain[:-1], chain[1:]):
            arrows.add(Arrow(a.get_right(), b.get_left(), color=INK, stroke_width=4, buff=0.15))
        missed_name = label("missed", 28, VERMILION, weight=BOLD).next_to(rock[0], DOWN, 0.2)
        # "A model learns from the records, and the records come from a gear."
        self.play(FadeIn(chain[2]), FadeIn(chain[1]), GrowArrow(arrows[1]), run_time=self.share(0.15))
        cue(self, "and the records come")
        self.play(FadeIn(chain[0]), GrowArrow(arrows[0]), run_time=self.share(0.1))
        # "Grabs and dredges often catch fewer animals on hard ground."
        cue(self, "Grabs and dredges")
        self.play(*[FadeIn(VGroup(g[0], g[1])) for g in (sand, rock)], run_time=self.share(0.1))
        self.play(*[LaggedStart(*[FadeIn(a, scale=0.5) for a in g[2]], lag_ratio=0.05) for g in (sand, rock)],
                  run_time=self.share(0.15))
        cue(self, "fewer animals")
        self.play(rock[3].animate.set_color(LIGHT).shift(0.15 * DOWN), FadeIn(missed_name),
                  run_time=self.share(0.15))
        self.finish()


class Scene23(VideoScene):
    """Schematic: the records on rock halved, everything else unchanged."""

    number = 23

    def construct(self):
        rng = np.random.default_rng(14)
        kinds = ["sand", "mud", "rock", "sand", "rock", "mud", "sand", "rock"]
        counts = rng.uniform(0.6, 2.6, len(kinds))
        rows = VGroup()
        for i, (kind, count) in enumerate(zip(kinds, counts)):
            y = 1.6 - 0.5 * i
            words = label(kind, 26, GREY if kind == "rock" else SUBDUED,
                          weight=BOLD if kind == "rock" else NORMAL).move_to([-3.6, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=count * 1.6, height=0.34, stroke_width=0, fill_color=BLUE, fill_opacity=1
                            ).move_to([-3.3, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(words, bar))
        head = label("the survey's records", 32, SUBDUED, weight=BOLD).next_to(rows, UP, 0.4)
        name = VGroup(label("half the animals on rock missed", 27, VERMILION, weight=BOLD),
                      label("everything else unchanged", 26, SUBDUED)).arrange(DOWN, buff=0.1)
        name.move_to(3.7 * RIGHT + 1.0 * UP)
        again = card("the same analysis,\nthe same folds", BLUE, 32).move_to(3.9 * RIGHT + 1.4 * DOWN)
        # "Suppose the survey's gear missed half the animals on rock, ..."
        self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows], *[GrowFromEdge(r[1], LEFT) for r in rows],
                  run_time=self.share(0.15))
        cue(self, "missed half")
        halve = [r[1].animate.stretch(0.5, 0, about_edge=LEFT).set_color(VERMILION)
                 for r, k in zip(rows, kinds) if k == "rock"]
        self.play(*halve, FadeIn(name), run_time=self.share(0.2))
        # "... and run the whole analysis again, on the same folds."
        cue(self, "and run the whole")
        self.play(FadeIn(again, scale=0.9), run_time=self.share(0.12))
        self.finish()


def multiplier_layout(scene):
    gear = scene.data("gear").set_index("records")
    axes, frame = chart([0.2, 1.4, 0.2], [0, 3, 1], 8.0, 3.0, [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4], [],
                        "rock's multiplier against sand", None, x_text=lambda v: f"{v:.1f}")
    VGroup(axes, frame).move_to(1.2 * RIGHT + 0.3 * DOWN)
    one = DashedLine(axes.c2p(1, 0), axes.c2p(1, 3), color=INK, stroke_width=4)
    one_name = label("1: the same as sand", 24, INK).next_to(one, UP, 0.1)
    rows = {}
    for key, y, colour, name in (("As recorded", 2.1, BLUE, "as recorded"),
                                 ("Half missed on rock", 0.9, VERMILION, "half missed on rock")):
        g = gear.loc[key]
        line = Line(axes.c2p(g["rock_low"], y), axes.c2p(g["rock_high"], y), color=colour, stroke_width=8)
        dot = Dot(axes.c2p(g["rock"], y), radius=0.15, color=colour)
        value = label(f"{g['rock']:.2f}  ({g['rock_low']:.2f} to {g['rock_high']:.2f})", 26, colour, weight=BOLD
                      ).next_to(line, UP, 0.15)
        value.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.05)
        words = label(name, 28, colour, weight=BOLD).next_to(axes.c2p(0.2, y), LEFT, 0.3)
        rows[key] = VGroup(words, line, dot, value)
    return gear, axes, frame, one, one_name, rows


class Scene24(VideoScene):
    """Page results: rock's multiplier with its interval, as recorded and with the biased records."""

    number = 24

    def construct(self):
        _, axes, frame, one, one_name, rows = multiplier_layout(self)
        recorded, missed = rows["As recorded"], rows["Half missed on rock"]
        head = label("the GAM's multiplier for rock, with its 95% interval", 32, SUBDUED, weight=BOLD
                     ).to_edge(UP, buff=0.35)
        cannot = label("cannot tell", 28, BLUE, weight=BOLD).next_to(recorded[1], RIGHT, 0.3)
        half = label("half as many", 28, VERMILION, weight=BOLD).next_to(axes.c2p(1.0, 0.9), RIGHT, 0.3)
        gear_not = label("the change is the gear's, not the species'", 32, INK, weight=BOLD
                         ).to_edge(DOWN, buff=0.25)
        # "As recorded, the GAM could not tell rock from sand: ..."
        self.play(FadeIn(head), FadeIn(frame), Create(one), FadeIn(one_name), run_time=self.share(0.08))
        # "... its multiplier of 0.80 had an interval from 0.59 to 1.09, which includes one."
        cue(self, "its multiplier")
        self.play(FadeIn(recorded[0]), FadeIn(recorded[2], scale=0.5), FadeIn(recorded[3]), run_time=self.share(0.06))
        cue(self, "had an interval")
        self.play(GrowFromCenter(recorded[1]), run_time=self.share(0.06))
        cue(self, "which includes")
        self.play(Indicate(one, color=INK), FadeIn(cannot), run_time=self.share(0.06))
        # "With the biased records it is 0.45, from 0.32 to 0.63, ..."
        cue(self, "With the biased")
        self.play(FadeIn(missed[0]), FadeIn(missed[2], scale=0.5), FadeIn(missed[3]), run_time=self.share(0.06))
        cue(self, "from 0.32")
        self.play(GrowFromCenter(missed[1]), run_time=self.share(0.06))
        # "... and a study would report half as many animals on rock."
        cue(self, "and a study")
        self.play(FadeIn(half), run_time=self.share(0.06))
        # "The change is the gear's, not the species'."
        cue(self, "The change")
        self.play(FadeIn(gear_not, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene25(VideoScene):
    """Page results: the cross-validated RMSE as recorded and with the biased records."""

    number = 25

    def construct(self):
        gear, *_ = multiplier_layout(self)
        values = [gear.loc["As recorded", "gam_rmse"], gear.loc["Half missed on rock", "gam_rmse"]]
        top = np.ceil(max(values))
        rows = hbars(["as recorded", "half missed on rock"], values, [BLUE, VERMILION], top,
                     length=6.0, height=0.6, step=1.1, size=32, digits=2)
        rows.move_to(0.6 * LEFT + 0.2 * DOWN)
        head = VGroup(label("the GAM's cross-validated RMSE (individuals)", 32, SUBDUED, weight=BOLD),
                      label("lower is better", 26, SUBDUED)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.5)
        improved = label("improved", 34, VERMILION, weight=BOLD).next_to(rows[1][2], RIGHT, 0.4)
        why = label("every fold carries the same bias", 32, INK, weight=BOLD).to_edge(DOWN, buff=0.6)
        # "The score did not warn."
        self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows], run_time=self.share(0.12))
        # "The cross-validated RMSE improved, from 4.34 to 4.27."
        cue(self, "from 4.34")
        self.play(GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]), run_time=self.share(0.08))
        cue(self, "to 4.27")
        self.play(GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]), run_time=self.share(0.08))
        self.play(FadeIn(improved, shift=0.2 * LEFT), run_time=self.share(0.06))
        # "Every fold carries the same bias, so the model matches the records as well as ever."
        cue(self, "Every fold")
        self.play(FadeIn(why, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene26(VideoScene):
    """Schematic: three checks from outside the model."""

    number = 26

    def construct(self):
        head = label("checks on the records come from outside the model", 30, INK, weight=BOLD
                     ).to_edge(UP, buff=0.5)
        texts = [("two gears", "on the same ground"), ("another way of counting", "video or divers"),
                 ("the gear and the effort", "reported")]
        cards = VGroup()
        for main, sub in texts:
            box = panel(4.2, 2.4, BLUE, PALE_BLUE)
            words = VGroup(label(main, 27, BLUE, weight=BOLD), label(sub, 25, INK)).arrange(DOWN, buff=0.15)
            cards.add(VGroup(box, words.move_to(box)))
        cards.arrange(RIGHT, buff=0.35).move_to(0.4 * DOWN)
        # "Checks on the records come from outside the model: ..."
        self.play(FadeIn(head), run_time=self.share(0.12))
        # "... fishing the same ground with two gears, counting the animals another way, with video or
        # divers, and reporting the gear and the effort."
        for c, phrase in zip(cards, ("fishing", "counting", "and reporting")):
            cue(self, phrase)
            self.play(FadeIn(c, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene27(KeyPointScene):
    number, point = 27, 3


# The quiz (scenes 28–29) --------------------------------------------------------------------

class Scene28(QuizScene):
    number = 28
    question = ("A random forest is scored", "on held-out sites. Which moves",
                "its score more: the seed,", "or which sites are held out?")


class Scene29(VideoScene):
    """Page results: the forest's RMSE across ten seeds, ten splits and ten seeds for the folds."""

    number = 29

    def construct(self):
        spread = self.data("spread")
        lo = np.floor(min(spread[["seed", "split", "folds"]].min()) * 2) / 2
        hi = np.ceil(max(spread[["seed", "split", "folds"]].max()) * 2) / 2
        ticks = list(np.arange(lo, hi + 0.01, 0.5))
        axes, frame = chart([lo, hi, 0.5], [0, 3, 1], 8.4, 3.3, ticks, [], "RMSE on new sites (individuals)", None,
                            x_text=lambda v: f"{v:.1f}")
        VGroup(axes, frame).move_to(1.6 * RIGHT + 0.5 * DOWN)
        rows = {}
        for column, y, colour, name in (("seed", 2.6, BLUE, "ten seeds, one split"),
                                        ("split", 1.7, VERMILION, "ten splits, one seed"),
                                        ("folds", 0.8, GREEN, "cross-validation")):
            values = spread[column]
            dots = VGroup(*[Dot(axes.c2p(v, y), radius=0.1, color=colour, fill_opacity=0.8) for v in values])
            span = Line(axes.c2p(values.min(), y - 0.3), axes.c2p(values.max(), y - 0.3), color=colour,
                        stroke_width=4)
            width = values.max() - values.min()
            value = label(f"{width:.2f}", 26, colour, weight=BOLD).next_to(span, DOWN, 0.08)
            words = label(name, 26, colour, weight=BOLD).next_to(axes.c2p(lo, y), LEFT, 0.3)
            rows[column] = VGroup(words, dots, span, value)
        answer = label("The sites.", 64, VERMILION, weight=BOLD).to_edge(UP, buff=0.3)
        ratio = (spread["split"].max() - spread["split"].min()) / (spread["seed"].max() - spread["seed"].min())
        times = label(f"about {ratio:.0f} times as much", 30, VERMILION, weight=BOLD).next_to(answer, DOWN, 0.15)
        # "The sites."
        self.play(FadeIn(answer, scale=1.3), FadeIn(frame), run_time=self.share(0.06))
        # "Ten seeds moved the forest's RMSE by 0.07; ..."
        cue(self, "Ten seeds")
        r = rows["seed"]
        self.play(FadeIn(r[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in r[1]], lag_ratio=0.1),
                  run_time=self.share(0.08))
        self.play(Create(r[2]), FadeIn(r[3]), run_time=self.share(0.04))
        # "... ten splits of the sites moved it by 1.84, about 27 times as much."
        cue(self, "ten splits")
        r = rows["split"]
        self.play(FadeIn(r[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in r[1]], lag_ratio=0.1),
                  run_time=self.share(0.08))
        self.play(Create(r[2]), FadeIn(r[3]), run_time=self.share(0.04))
        cue(self, "about 27")
        self.play(FadeIn(times), run_time=self.share(0.05))
        # "A seed makes a run repeat exactly, but it cannot show how far the score would move with
        # other sites."
        cue(self, "A seed makes")
        self.play(Indicate(rows["seed"][1], color=BLUE), run_time=self.share(0.1))
        cue(self, "but it cannot")
        self.play(Indicate(rows["split"][1], color=VERMILION), run_time=self.share(0.1))
        # "Cross-validation steadies it."
        cue(self, "Cross-validation")
        r = rows["folds"]
        self.play(FadeIn(r[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in r[1]], lag_ratio=0.1),
                  Create(r[2]), FadeIn(r[3]), run_time=self.share(0.08))
        self.finish()


# The recap (scenes 30–32) and the end card (scene 33) --------------------------------------

class Scene30(RecapScene):
    number, point = 30, 1


class Scene31(RecapScene):
    number, point = 31, 2


class Scene32(RecapScene):
    number, point = 32, 3


class Scene33(EndCardScene):
    number = 33
