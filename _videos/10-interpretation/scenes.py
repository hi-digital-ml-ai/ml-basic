"""Manim scenes for the interpretation video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/10-interpretation
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

Scenes marked "page results" read visuals/data/*.csv, which tools/figures-for-video.R
writes from the pages through exports.R. Single numbers come from the "<page>-numbers"
tables, so a scene shows the page's own value. The other scenes are schematic: made-up
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


PROMISES = ["Shuffle each input in turn",
            "Draw each input's effect",
            "Split one prediction into parts"]
ANSWERS = ["The more the error rises,\nthe more the model\nrelies on that input",
           "Set it to each value\nat every station, and\naverage the predictions",
           "Each input's SHAP value:\nhow far it moves the\nprediction from the average"]
RECAP = PROMISES

LIGHT = "#C9CED2"
PALE_BLUE = "#EAF2F8"

UNITS = {"depth_m": " m", "temperature_c": " °C", "chlorophyll_mg_m3": " mg/m³",
         "salinity_psu": "", "substrate": "", "season": ""}
INPUT_NAMES = {"depth_m": "depth", "temperature_c": "temperature",
               "chlorophyll_mg_m3": "chlorophyll", "salinity_psu": "salinity",
               "substrate": "seabed", "season": "season"}


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("shuffling each", "drawing each", "and splitting"))


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


def value(scene, page, name):
    """One number from a page's "<page>-numbers" table."""
    table = scene.data(f"{page}-numbers").set_index("name")["value"]
    return table[name]


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


def panel(width, height, colour, fill=BACKGROUND):
    return RoundedRectangle(width=width, height=height, corner_radius=0.2, stroke_color=colour,
                            stroke_width=5, fill_color=fill, fill_opacity=1)


def hbars(names, values, colours, top, length=6.4, height=0.34, step=0.46, size=26, digits=None,
          texts=None):
    """Horizontal bars from a common left edge, the names right-aligned beside it.

    `texts`, if given, label the bars in place of their lengths."""
    rows = VGroup()
    for i, (name, amount, colour) in enumerate(zip(names, values, colours)):
        y = -i * step
        bar = Rectangle(width=max(amount / top * length, 0.001), height=height, stroke_width=0,
                        fill_color=colour, fill_opacity=1).move_to([0, y, 0], aligned_edge=LEFT)
        words = label(name, size, colour if colour != LIGHT else SUBDUED).next_to([0, y, 0], LEFT, 0.25)
        if texts is not None:
            amount_text = label(texts[i], size - 2, SUBDUED).next_to(bar, RIGHT, 0.15)
        elif digits is not None:
            amount_text = label(f"{amount:.{digits}f}", size - 2, SUBDUED).next_to(bar, RIGHT, 0.15)
        else:
            amount_text = VGroup()
        rows.add(VGroup(words, bar, amount_text))
    return rows


def dots_table(rows, columns, colours, cell=0.42, gap=0.08, seed=1, width=None):
    """A small table drawn as shaded cells: one column per input, schematic."""
    rng = np.random.default_rng(seed)
    table = VGroup()
    for c, colour in zip(range(columns), colours):
        column = VGroup(*[Rectangle(width=width or cell, height=cell, stroke_width=0, fill_color=colour,
                                    fill_opacity=rng.uniform(0.25, 1.0)) for _ in range(rows)])
        column.arrange(DOWN, buff=gap)
        table.add(column)
    table.arrange(RIGHT, buff=gap)
    return table


def tree_icon(colour=GREEN, height=0.7):
    crown = Triangle(color=colour, fill_color=colour, fill_opacity=1, stroke_width=0).scale(height / 2)
    trunk = Rectangle(width=0.08, height=height * 0.25, stroke_width=0, fill_color=GREY, fill_opacity=1)
    trunk.next_to(crown, DOWN, 0)
    return VGroup(crown, trunk)


# Shuffle each input in turn (scenes 2–6) ---------------------------------------------------

class Scene02(VideoScene):
    """Schematic: linear regression's coefficients beside a forest with nothing to read."""

    number = 2

    def construct(self):
        left = panel(5.6, 4.6, BLUE).move_to(3.3 * LEFT + 0.2 * DOWN)
        left_head = label("linear regression", 34, BLUE, weight=BOLD).next_to(left.get_top(), DOWN, 0.3)
        coefficients = VGroup()
        for i, (name, size) in enumerate((("depth", -1.0), ("temperature", 1.4), ("salinity", 0.65),
                                          ("chlorophyll", 0.15))):
            words = label(name, 28).move_to([-3.6, 0.8 - 0.75 * i, 0], aligned_edge=RIGHT)
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
        # "Linear regression shows what it learned through its coefficients: ..."
        cue(self, "Linear regression")
        self.play(FadeIn(left), FadeIn(left_head), Create(zero), run_time=self.share(0.08))
        self.play(LaggedStart(*[FadeIn(c[0]) for c in coefficients], lag_ratio=0.2),
                  LaggedStart(*[GrowFromEdge(c[1], LEFT if c[1].get_left()[0] >= -2.21 else RIGHT)
                                for c in coefficients], lag_ratio=0.2),
                  FadeIn(coef_name), run_time=self.share(0.2))
        # "A random forest averages hundreds of trees, each asking its own questions, ..."
        cue(self, "A random forest")
        self.play(FadeIn(right), FadeIn(right_head), run_time=self.share(0.06))
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in trees], lag_ratio=0.04), run_time=self.share(0.18))
        # "... so it has no such numbers to read."
        cue(self, "so it has no")
        self.play(trees.animate.fade(0.7), FadeIn(question, scale=1.4), FadeIn(forest_name),
                  run_time=self.share(0.1))
        self.finish()


SHUFFLE_ROWS = 7
SHUFFLE_INPUTS = ("temperature", "depth", "salinity")
# the rise in the error when each input is shuffled, as heights: schematic
SHUFFLE_RISES = (1.6, 0.6, 0.08)


def shuffled_order(seed):
    return np.random.default_rng(seed).permutation(SHUFFLE_ROWS)


def shuffle_layout():
    """The schematic of scenes 3 and 4: the test stations' inputs and counts, one row each."""
    table = dots_table(SHUFFLE_ROWS, 3, [BLUE] * 3, seed=3, width=1.6, gap=0.14)
    outcome = dots_table(SHUFFLE_ROWS, 1, [INK], seed=9, width=1.0, gap=0.14)
    outcome.next_to(table, RIGHT, 0.3)
    VGroup(table, outcome).move_to(3.4 * LEFT + 0.5 * DOWN)
    heads = VGroup(*[label(t, 26, BLUE if t != "count" else INK, weight=BOLD).next_to(col, UP, 0.2)
                     for t, col in zip((*SHUFFLE_INPUTS, "count"), [*table, outcome[0]])])
    stations = label("test stations, one per row", 26, SUBDUED).next_to(VGroup(table, outcome), DOWN, 0.3)
    outlines = VGroup(*[SurroundingRectangle(column, color=ORANGE, buff=0.08, stroke_width=5)
                        for column in table])
    homes = [[cell.get_center() for cell in column] for column in table]
    return table, outcome, heads, stations, outlines, homes


def shuffle(scene, column, home, seed, run_time):
    order = shuffled_order(seed)
    scene.play(*[cell.animate.move_to(home[i]) for cell, i in zip(column, order)],
               run_time=run_time, rate_func=smooth)


def unshuffle(column, home):
    return [cell.animate.move_to(spot) for cell, spot in zip(column, home)]


def error_bars(before, after, x=1.6):
    base = -2.2
    first = Rectangle(width=1.1, height=before, stroke_width=0, fill_color=GREY, fill_opacity=1
                      ).move_to([x, base, 0], aligned_edge=DOWN)
    second = Rectangle(width=1.1, height=after, stroke_width=0, fill_color=GREY, fill_opacity=1
                       ).move_to([x + 2.0, base, 0], aligned_edge=DOWN)
    rise = Rectangle(width=1.1, height=after - before, stroke_width=0, fill_color=VERMILION, fill_opacity=1
                     ).move_to([x + 2.0, base + before, 0], aligned_edge=DOWN)
    floor = Line([x - 0.9, base, 0], [x + 2.9, base, 0], color=GRID, stroke_width=3)
    names = VGroup(label("before", 26, SUBDUED).next_to(first, DOWN, 0.2),
                   label("shuffled", 26, ORANGE).next_to(second, DOWN, 0.2))
    head = label("error on the test stations", 28, SUBDUED, weight=BOLD).move_to([x + 1.0, 2.4, 0])
    return first, second, rise, floor, names, head


BEFORE = 1.6


class Scene03(VideoScene):
    """Schematic: the test stations scored, then temperature's column shuffled between rows."""

    number = 3

    def construct(self):
        table, outcome, heads, stations, outlines, homes = shuffle_layout()
        first, second, rise, floor, names, head = error_bars(BEFORE, BEFORE + SHUFFLE_RISES[0])
        name = label("read it from outside", 40, BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        row = SurroundingRectangle(VGroup(*[column[2] for column in [*table, outcome[0]]]), color=INK,
                                   buff=0.06, stroke_width=4)
        row_name = label("one station", 26, INK, weight=BOLD).next_to(row, RIGHT, 0.2)
        # "Yet any model can be read from outside."
        self.play(FadeIn(name, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "Take the test stations, which the model never saw while learning."
        cue(self, "Take the test")
        self.play(FadeIn(table), FadeIn(outcome), FadeIn(heads), FadeIn(stations), run_time=self.share(0.07))
        # "Each row is one station: its inputs, and the count recorded there."
        cue(self, "Each row")
        self.play(Create(row), FadeIn(row_name), run_time=self.share(0.05))
        cue(self, "its inputs")
        self.play(Indicate(VGroup(*heads[:3]), color=BLUE), run_time=self.share(0.05))
        cue(self, "and the count")
        self.play(Indicate(heads[3], color=INK), run_time=self.share(0.05))
        # "Score the model's predictions against those counts."
        cue(self, "Score the model")
        self.play(FadeOut(row), FadeOut(row_name), FadeIn(head), Create(floor), GrowFromEdge(first, DOWN),
                  FadeIn(names[0]), run_time=self.share(0.07))
        # "Then take one input, say temperature, and shuffle its column, ..."
        cue(self, "say temperature")
        self.play(Create(outlines[0]), heads[0].animate.set_color(ORANGE), run_time=self.share(0.05))
        cue(self, "and shuffle its")
        shuffle(self, table[0], homes[0], 5, self.share(0.12))
        # "The other columns stay as they were, so any change comes from temperature alone."
        cue(self, "The other columns")
        self.play(Indicate(VGroup(table[1], table[2], outcome), color=SUBDUED, scale_factor=1.03),
                  run_time=self.share(0.1))
        self.finish()


class Scene04(VideoScene):
    """Schematic: score again; the rise is temperature's importance; then depth, then salinity."""

    number = 4

    def construct(self):
        table, outcome, heads, stations, outlines, homes = shuffle_layout()
        first, second, rise, floor, names, head = error_bars(BEFORE, BEFORE + SHUFFLE_RISES[0])
        order = shuffled_order(5)
        for cell, i in zip(table[0], order):
            cell.move_to(homes[0][i])
        heads[0].set_color(ORANGE)
        name = label("read it from outside", 40, BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(name, table, outcome, heads, stations, outlines[0], first, floor, names[0], head)
        shuffled_name = label("temperature\nshuffled", 26, ORANGE).next_to(second, DOWN, 0.2)
        rise_name = label("the rise:\nits importance", 28, VERMILION, weight=BOLD).next_to(rise, RIGHT, 0.3)
        new_name = label("permutation importance", 40, BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        repeat = label("each many times, the rises averaged", 28, INK, weight=BOLD).to_edge(DOWN, buff=0.3)

        def bars_for(k):
            """The second bar and its rise when input k is shuffled."""
            after = BEFORE + SHUFFLE_RISES[k]
            bar = second.copy().stretch_to_fit_height(after).align_to(first, DOWN)
            top = rise.copy().stretch_to_fit_height(SHUFFLE_RISES[k]).move_to(
                bar.get_top(), aligned_edge=UP)
            words = label(f"{SHUFFLE_INPUTS[k]}\nshuffled", 26, ORANGE).next_to(bar, DOWN, 0.2)
            return bar, top, words

        # "Score the model again."
        self.play(GrowFromEdge(second, DOWN), FadeIn(shuffled_name), run_time=self.share(0.07))
        # "If it relied on temperature, its predictions get worse, and the error rises."
        cue(self, "and the error rises")
        self.play(FadeIn(rise), run_time=self.share(0.05))
        # "That rise is temperature's importance, called permutation importance."
        cue(self, "That rise")
        self.play(FadeIn(rise_name, shift=0.2 * LEFT), run_time=self.share(0.05))
        cue(self, "called permutation")
        self.play(ReplacementTransform(name, new_name), run_time=self.share(0.05))
        # "Then put temperature back, and do the same with depth, then salinity: one input at a time."
        for k, phrase in ((1, "put temperature back"), (2, "then salinity")):
            cue(self, phrase)
            bar, top, words = bars_for(k)
            self.play(*unshuffle(table[k - 1], homes[k - 1]), heads[k - 1].animate.set_color(BLUE),
                      ReplacementTransform(outlines[k - 1], outlines[k]), heads[k].animate.set_color(ORANGE),
                      run_time=self.share(0.05))
            shuffle(self, table[k], homes[k], 5 + k, self.share(0.06))
            self.play(Transform(second, bar), Transform(rise, top), Transform(shuffled_name, words),
                      rise_name.animate.next_to(top, RIGHT, 0.3), run_time=self.share(0.05))
        # "Shuffling is random, so each input is shuffled many times and the rises are averaged."
        cue(self, "Shuffling is random")
        self.play(FadeIn(repeat, shift=0.2 * UP), run_time=self.share(0.05))
        for seed in (11, 13):
            shuffle(self, table[2], homes[2], seed, self.share(0.05))
        self.finish()


def importance_bars(scene, forest="all six", top=0.4, length=6.4, colour=BLUE):
    table = scene.data("importance")
    table = table[table["forest"] == forest].sort_values("rise", ascending=False)
    shown = table["rise"].clip(lower=0)
    rows = hbars([INPUT_NAMES[t] for t in table["input"]], shown, [colour] * len(table), top,
                 length=length, height=0.42, step=0.62, size=30,
                 texts=[f"{rise:.2f}" for rise in table["rise"]])
    return table, rows


class Scene05(VideoScene):
    """Page results: the forest's RMSE on the test stations, then each input's rise."""

    number = 5

    def construct(self):
        rmse = value(self, "feature-importance", "rmse")
        table, rows = importance_bars(self)
        rows.move_to(1.0 * RIGHT + 0.9 * DOWN)
        head = label("rise in the typical miss when shuffled (animals)", 30, SUBDUED, weight=BOLD
                     ).next_to(rows, UP, 0.5)
        miss = VGroup(label("the forest's typical miss on the test stations:", 32, INK),
                      label(f"{rmse:.2f} animals", 40, BLUE, weight=BOLD)).arrange(RIGHT, buff=0.25)
        miss.to_edge(UP, buff=0.5)
        order = list(table["input"])

        def row_of(term):
            return rows[order.index(term)]

        # "On the survey, a random forest predicts the count of one species at each station."
        # "On the test stations its typical miss, the RMSE, is 3.93 animals."
        cue(self, "On the test stations")
        self.play(FadeIn(miss[0]), run_time=self.share(0.06))
        cue(self, "is 3.93")
        self.play(FadeIn(miss[1], scale=1.2), run_time=self.share(0.05))
        self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows], run_time=self.share(0.06))
        # "Shuffle temperature, and that miss grows by 0.34: ..."
        cue(self, "Shuffle temperature")
        t = row_of("temperature_c")
        self.play(GrowFromEdge(t[1], LEFT), FadeIn(t[2]), run_time=self.share(0.08))
        # "... more than three times as much as for depth, the next input."
        cue(self, "more than three")
        d = row_of("depth_m")
        self.play(GrowFromEdge(d[1], LEFT), FadeIn(d[2]), run_time=self.share(0.06))
        rest = [row_of(x) for x in ("substrate", "season")]
        self.play(*[GrowFromEdge(r[1], LEFT) for r in rest], *[FadeIn(r[2]) for r in rest],
                  run_time=self.share(0.05))
        # "Shuffle chlorophyll or salinity, and it hardly moves."
        cue(self, "Shuffle chlorophyll")
        low = [row_of(x) for x in ("chlorophyll_mg_m3", "salinity_psu")]
        self.play(*[GrowFromEdge(r[1], LEFT) for r in low], *[FadeIn(r[2]) for r in low],
                  run_time=self.share(0.05))
        self.play(*[Indicate(r[0], color=SUBDUED) for r in low], run_time=self.share(0.08))
        self.finish()


class Scene06(KeyPointScene):
    number, point = 6, 1


# Draw each input's effect (scenes 7–11) ----------------------------------------------------

class Scene07(VideoScene):
    """Page results and schematic: temperature's importance, then which way?"""

    number = 7

    def construct(self):
        table, rows = importance_bars(self, length=5.0)
        t = rows[list(table["input"]).index("temperature_c")]
        t.move_to(1.0 * UP + 0.6 * RIGHT)
        how_much = label("how much", 34, BLUE, weight=BOLD).next_to(t, UP, 0.5)
        axes = plain_axes([0, 4, 1], [0, 3, 1], 4.4, 2.6).move_to(2.0 * DOWN + 0.4 * RIGHT)
        rising = Arrow(axes.c2p(0.3, 0.4), axes.c2p(1.7, 2.6), color=BLUE, stroke_width=8, buff=0)
        falling = Arrow(axes.c2p(2.3, 2.6), axes.c2p(3.7, 0.4), color=ORANGE, stroke_width=8, buff=0)
        x_name = label("temperature", 26, SUBDUED).next_to(axes, DOWN, 0.2)
        y_name = label("count", 26, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.2)
        which = label("which way?", 40, VERMILION, weight=BOLD).next_to(axes, RIGHT, 0.6)
        # "Importance says how much the forest relies on temperature, ..."
        cue(self, "Importance says")
        self.play(FadeIn(t[0]), GrowFromEdge(t[1], LEFT), FadeIn(t[2]), FadeIn(how_much),
                  run_time=self.share(0.12))
        # "... but not which way."
        cue(self, "but not which")
        self.play(FadeIn(axes), FadeIn(x_name), FadeIn(y_name), FadeIn(which), run_time=self.share(0.1))
        # "Does the count rise in warmer water, or fall?"
        cue(self, "Does the count rise")
        self.play(GrowArrow(rising), run_time=self.share(0.1))
        cue(self, "or fall")
        self.play(GrowArrow(falling), run_time=self.share(0.1))
        self.finish()


SWEEP_XS = np.linspace(0, 10, 41)


def sweep_layout():
    """The schematic of scenes 8 and 9: stations' prediction curves and their average."""
    axes, frame = chart([0, 10, 1], [0, 1.2, 0.5], 9.0, 4.0, [], [], "temperature", "prediction")
    VGroup(axes, frame).shift(0.7 * DOWN)
    rng = np.random.default_rng(2)
    scales = rng.uniform(0.3, 1.0, 8)
    shapes = [s * np.exp(-((SWEEP_XS - 4.0 - rng.normal(0, 0.3)) / 2.4) ** 2) + 0.1 for s in scales]
    average = np.mean(shapes, axis=0)
    return axes, frame, shapes, average


SWEEP_STEPS = (8, 12, 16, 20, 24, 28, 32, 36)


class Scene08(VideoScene):
    """Schematic: every station's prediction at one temperature, then their average."""

    number = 8

    def construct(self):
        axes, frame, shapes, average = sweep_layout()
        k = SWEEP_STEPS[0]
        line = DashedLine(axes.c2p(SWEEP_XS[k], 0), axes.c2p(SWEEP_XS[k], 1.15), color=ORANGE, stroke_width=4)
        one = label("one value", 26, ORANGE, weight=BOLD).next_to(line, UP, 0.1)
        marks = VGroup(*[Dot(axes.c2p(SWEEP_XS[k], ys[k]), radius=0.08, color=GREY) for ys in shapes])
        mean_dot = Dot(axes.c2p(SWEEP_XS[k], average[k]), radius=0.12, color=BLUE)
        step_text = VGroup(label("every station given the same temperature", 28, INK),
                           label("predict", 28, SUBDUED), label("average", 28, SUBDUED)
                           ).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.4)
        # "To find out, ask the forest a what-if question."
        self.play(FadeIn(frame), run_time=self.share(0.08))
        # "Take every station it learned from, and give them all the same temperature, ..."
        cue(self, "give them all")
        self.play(Create(line), FadeIn(one), FadeIn(step_text[0]), run_time=self.share(0.1))
        # "The forest predicts each station's count, ..."
        cue(self, "The forest predicts")
        self.play(step_text[1].animate.set_color(INK),
                  LaggedStart(*[FadeIn(m, scale=0.5) for m in marks], lag_ratio=0.1), run_time=self.share(0.12))
        # "... and the predictions are averaged into one point."
        cue(self, "and the predictions")
        self.play(step_text[2].animate.set_color(INK), *[m.animate.move_to(mean_dot) for m in marks],
                  FadeIn(mean_dot), run_time=self.share(0.1))
        self.remove(marks)
        self.finish()


class Scene09(VideoScene):
    """Schematic: the same at each warmer value; the averages joined into a curve."""

    number = 9

    def construct(self):
        axes, frame, shapes, average = sweep_layout()
        k0 = SWEEP_STEPS[0]
        line = DashedLine(axes.c2p(SWEEP_XS[k0], 0), axes.c2p(SWEEP_XS[k0], 1.15), color=ORANGE, stroke_width=4)
        dots = VGroup(Dot(axes.c2p(SWEEP_XS[k0], average[k0]), radius=0.12, color=BLUE))
        self.add(frame, line, dots)
        name = label("partial dependence plot", 44, BLUE, weight=BOLD).to_edge(UP, buff=0.4)
        # "Then do the same at a slightly warmer temperature, and again, across the whole range."
        each = self.share(0.45) / (len(SWEEP_STEPS) - 1)
        for k in SWEEP_STEPS[1:]:
            self.play(line.animate.move_to(axes.c2p(SWEEP_XS[k], 0.575)), run_time=each * 0.5)
            dot = Dot(axes.c2p(SWEEP_XS[k], average[k]), radius=0.12, color=BLUE)
            self.play(FadeIn(dot, scale=0.5), run_time=each * 0.5)
            dots.add(dot)
        # "Joined up, the points draw a curve, called a partial dependence plot: ..."
        cue(self, "Joined up")
        self.play(FadeOut(line), Create(polyline(axes, SWEEP_XS, average, BLUE, 8)), run_time=self.share(0.15))
        cue(self, "called a partial")
        self.play(FadeIn(name, shift=0.2 * DOWN), run_time=self.share(0.08))
        self.finish()


def hump_chart(scene, width=8.0, height=4.4, centre=0.5 * DOWN):
    partial = scene.data("partial").sort_values("value")
    lo, hi = partial["value"].min(), partial["value"].max()
    top = np.ceil(partial[".pred"].max() + 0.5)
    axes, frame = chart([np.floor(lo), np.ceil(hi), 1], [0, top, 1], width, height,
                        list(range(int(np.ceil(lo)), int(np.floor(hi)) + 1, 2)),
                        list(range(0, int(top) + 1, 2)), "temperature (°C)", "average prediction (animals)")
    VGroup(axes, frame).move_to(centre)
    curve = polyline(axes, partial["value"], partial[".pred"], BLUE, 8)
    return partial, axes, frame, curve


class Scene10(VideoScene):
    """Page results: the forest's partial dependence on temperature, a hump peaking at 7.7 °C."""

    number = 10

    def construct(self):
        partial, axes, frame, curve = hump_chart(self)
        top_row = partial.loc[partial[".pred"].idxmax()]
        peak = top_row["value"]
        head = label("the forest's partial dependence on temperature", 34, BLUE, weight=BOLD
                     ).to_edge(UP, buff=0.35)
        peak_line = DashedLine(axes.c2p(peak, 0), axes.c2p(peak, top_row[".pred"] + 0.6), color=BLUE,
                               stroke_width=4)
        peak_name = label(f"{peak:.1f} °C", 32, BLUE, weight=BOLD).next_to(peak_line, UP, 0.1)
        rising = partial[partial["value"] <= peak]
        falling = partial[partial["value"] >= peak]
        up = polyline(axes, rising["value"], rising[".pred"], BLUE, 8)
        down = polyline(axes, falling["value"], falling[".pred"], BLUE, 8)
        hump = label("a hump", 40, INK, weight=BOLD).move_to(axes.c2p(11.4, top_row[".pred"] + 0.4))
        # "For the forest, the curve rises from the coldest water to a peak at 7.7 degrees, ..."
        self.play(FadeIn(head), FadeIn(frame), run_time=self.share(0.08))
        cue(self, "the curve rises")
        self.play(Create(up), run_time=self.share(0.15))
        cue(self, "a peak at")
        self.play(Create(peak_line), FadeIn(peak_name), run_time=self.share(0.07))
        # "... then falls again in warmer water: a hump."
        cue(self, "falls again")
        self.play(Create(down), run_time=self.share(0.12))
        cue(self, "a hump")
        self.play(FadeIn(hump, scale=1.2), run_time=self.share(0.05))
        self.finish()


class Scene11(KeyPointScene):
    number, point = 11, 2


# Split one prediction into parts (scenes 12–16) --------------------------------------------

class Scene12(VideoScene):
    """Page results: the training stations' predictions, their average, and one station's."""

    number = 12

    def construct(self):
        predictions = self.data("train-predictions")[".pred"]
        average = value(self, "explaining-one-prediction", "average")
        prediction = value(self, "explaining-one-prediction", "prediction")
        top = np.ceil(predictions.max() / 2) * 2
        axes, frame = chart([0, top, 2], [0, 1, 1], 11.0, 2.6, list(range(0, int(top) + 1, 4)), [],
                            "predicted count (animals)", None)
        VGroup(axes, frame).move_to(0.9 * DOWN)
        rng = np.random.default_rng(4)
        dots = VGroup(*[Dot(axes.c2p(p, rng.uniform(0.1, 0.9)), radius=0.05, color=GREY, fill_opacity=0.5)
                        for p in predictions])
        head = label("the forest's predictions at the stations it learned from", 30, SUBDUED, weight=BOLD
                     ).to_edge(UP, buff=0.4)
        mean_line = Line(axes.c2p(average, 0), axes.c2p(average, 1.15), color=BLUE, stroke_width=7)
        mean_tag = VGroup(label("average", 30, BLUE, weight=BOLD),
                          label(f"{average:.2f}", 36, BLUE, weight=BOLD)).arrange(DOWN, buff=0.1)
        mean_tag.next_to(mean_line, UP, 0.15).align_to(mean_line, RIGHT)
        station = Dot(axes.c2p(prediction, 0.5), radius=0.16, color=VERMILION).set_z_index(10)
        station_line = DashedLine(axes.c2p(prediction, 0), axes.c2p(prediction, 1.15), color=VERMILION,
                                  stroke_width=5)
        station_tag = VGroup(label("this station", 30, VERMILION, weight=BOLD),
                             label(f"{prediction:.2f}", 36, VERMILION, weight=BOLD)).arrange(DOWN, buff=0.1)
        station_tag.next_to(station_line, UP, 0.15).align_to(station_line, LEFT)
        question = label("which inputs raised it?", 40, VERMILION, weight=BOLD).next_to(frame, DOWN, 0.4)
        # "Importance and the curve describe the forest over all the stations, ..."
        cue(self, "Importance and")
        self.play(FadeIn(head), FadeIn(frame), run_time=self.share(0.06))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=self.share(0.12))
        # "... but often the question is about one station."
        cue(self, "but often")
        self.play(FadeIn(station, scale=0.5), run_time=self.share(0.06))
        # "Over the stations it learned from, the forest predicts 4.11 animals on average."
        cue(self, "Over the stations")
        self.play(dots.animate.fade(0.5), Create(mean_line), run_time=self.share(0.06))
        cue(self, "4.11")
        self.play(FadeIn(mean_tag, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "At this station it predicts 6.53."
        cue(self, "At this station")
        self.play(Create(station_line), FadeIn(station_tag, shift=0.2 * DOWN), run_time=self.share(0.07))
        # "Which inputs raised it?"
        cue(self, "Which inputs")
        self.play(FadeIn(question, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


class Scene13(VideoScene):
    """Schematic: from the average, each input's bar pushes the prediction up or down."""

    number = 13

    def construct(self):
        axes, frame = chart([0, 10, 1], [0, 1, 1], 9.0, 0.01, [], [], "predicted count", None)
        VGroup(axes, frame).move_to(2.4 * DOWN + 0.6 * RIGHT)
        moves = (("depth", 2.2), ("temperature", 1.4), ("seabed", -1.0))
        start = 3.0
        rows, running = VGroup(), start
        for i, (name, move) in enumerate(moves):
            y = 1.0 - i * 0.95
            x0, x1 = axes.c2p(min(running, running + move), 0)[0], axes.c2p(max(running, running + move), 0)[0]
            running += move
            colour = BLUE if move > 0 else ORANGE
            bar = Rectangle(width=x1 - x0, height=0.5, stroke_width=0, fill_color=colour, fill_opacity=1
                            ).move_to([(x0 + x1) / 2, y, 0])
            words = label(name, 30, INK).move_to([axes.c2p(0, 0)[0] - 0.2, y, 0], aligned_edge=RIGHT)
            rows.add(VGroup(words, bar))
        top_y, bottom_y = 1.6, -1.95
        mean_line = DashedLine([axes.c2p(start, 0)[0], top_y, 0], [axes.c2p(start, 0)[0], bottom_y, 0],
                               color=GREY, stroke_width=4)
        end_line = DashedLine([axes.c2p(running, 0)[0], top_y, 0], [axes.c2p(running, 0)[0], bottom_y, 0],
                              color=INK, stroke_width=4)
        mean_tag = label("average", 28, SUBDUED, weight=BOLD).next_to(mean_line, UP, 0.1)
        mean_tag.align_to(mean_line, RIGHT)
        end_tag = label("this station's prediction", 28, INK, weight=BOLD).next_to(end_line, UP, 0.1)
        end_tag.align_to(end_line, LEFT)
        head = label("one SHAP value per input", 40, BLUE, weight=BOLD).to_edge(UP, buff=0.35)
        edge = max(r[1].get_right()[0] for r in rows) + 0.6
        up = label("+ adds animals", 28, BLUE, weight=BOLD).move_to([edge, rows[0].get_y(), 0], aligned_edge=LEFT)
        down = label("− takes some away", 28, ORANGE, weight=BOLD).move_to([edge, rows[2].get_y(), 0],
                                                                         aligned_edge=LEFT)
        # "SHAP values answer that."
        self.play(FadeIn(head), FadeIn(frame), Create(mean_line), FadeIn(mean_tag), run_time=self.share(0.08))
        # "Each input gets one number for this station: the animals it adds to the average, or takes away."
        cue(self, "Each input gets")
        for i in range(len(rows)):
            self.play(FadeIn(rows[i][0]), GrowFromEdge(rows[i][1], LEFT if moves[i][1] > 0 else RIGHT),
                      run_time=self.share(0.07))
        # "A positive value pushes the prediction up, ..."
        cue(self, "A positive value")
        self.play(Indicate(VGroup(rows[0][1], rows[1][1]), color=BLUE, scale_factor=1.05), FadeIn(up),
                  run_time=self.share(0.08))
        # "... a negative one pushes it down."
        cue(self, "a negative one")
        self.play(Indicate(rows[2][1], color=ORANGE, scale_factor=1.05), FadeIn(down), run_time=self.share(0.08))
        # "Added together, they lead exactly from the average to this station's prediction."
        cue(self, "Added together")
        self.play(Create(end_line), FadeIn(end_tag, scale=1.1), run_time=self.share(0.1))
        self.finish()


def player(colour, name, size=26):
    disc = Circle(0.38, color=colour, fill_color=colour, fill_opacity=0.25, stroke_width=4)
    return VGroup(disc, label(name, size, INK).next_to(disc, DOWN, 0.15))


SHARES = (8, 4, -4)   # arrow widths: the biggest share, a smaller one, a negative one


def sharing(head, prize, names, colour, note=None):
    """A prize box split by arrows among three players, the last share negative: schematic."""
    words = label(prize, 28, INK, weight=BOLD)
    if note:
        words = VGroup(words, label(note, 22, SUBDUED)).arrange(DOWN, buff=0.08)
    box = RoundedRectangle(width=max(3.2, words.width + 0.4), height=1.05, corner_radius=0.12,
                           stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.25)
    words.move_to(box)
    players = VGroup(*[player(colour, n) for n in names]).arrange(RIGHT, buff=0.55)
    players.next_to(box, DOWN, 1.0)
    arrows = VGroup()
    for p, width in zip(players, SHARES):
        ends = (box.get_bottom(), p[0].get_top())
        if width < 0:   # a negative share runs back to the prize
            ends = ends[::-1]
        arrows.add(Arrow(*ends, color=BLUE if width > 0 else ORANGE, stroke_width=abs(width) + 1, buff=0.1,
                         max_tip_length_to_length_ratio=0.2))
    signs = VGroup(*[label("+" if w > 0 else "−", 34, BLUE if w > 0 else ORANGE, weight=BOLD
                           ).next_to(a, LEFT if i == 0 else RIGHT, 0.08)
                     for i, (a, w) in enumerate(zip(arrows, SHARES))])
    name = label(head, 30, colour, weight=BOLD).next_to(box, UP, 0.3)
    return VGroup(name, VGroup(box, words), arrows, players, signs)


def show_share(scene, panel_, i, share=0.06):
    scene.play(GrowArrow(panel_[2][i]), FadeIn(panel_[4][i]), Indicate(panel_[3][i], color=panel_[2][i].get_color()),
               run_time=scene.share(share))


class Scene14(VideoScene):
    """Schematic: the name spelled out; a quiz team sharing a prize, then the inputs sharing the gap."""

    number = 14

    def construct(self):
        average = value(self, "explaining-one-prediction", "average")
        prediction = value(self, "explaining-one-prediction", "prediction")
        shap = label("SHAP", 72, BLUE, weight=BOLD).to_edge(UP, buff=0.3)
        full = label("SHapley Additive exPlanations", 44, INK, weight=BOLD,
                     t2c={"SH": BLUE, "A": BLUE, "P": BLUE}).next_to(shap, DOWN, 0.25)
        adds = label("average + the parts = the prediction", 30, SUBDUED).next_to(full, DOWN, 0.3)
        team = sharing("a quiz team shares its prize", "prize", ("most answers", "some", "cost points"), PURPLE)
        inputs = sharing("the inputs share the gap", "the gap",
                         ("depth", "temperature", "seabed"), BLUE,
                         note=f"{prediction:.2f} − {average:.2f} = {prediction - average:.2f} animals")
        VGroup(team, inputs).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.35)
        # "SHAP stands for SHapley Additive exPlanations."
        self.play(FadeIn(shap, scale=1.2), run_time=self.share(0.04))
        cue(self, "stands for")
        self.play(FadeIn(full, shift=0.2 * DOWN), run_time=self.share(0.05))
        # "Additive, because the parts add up."
        cue(self, "Additive, because")
        self.play(Indicate(full[7:15], color=BLUE, scale_factor=1.08), FadeIn(adds), run_time=self.share(0.05))
        # "Shapley, after the mathematician Lloyd Shapley, who worked out a fair way to share a
        # team's prize among its players."
        cue(self, "Shapley, after")
        self.play(Indicate(full[0:7], color=BLUE, scale_factor=1.08), run_time=self.share(0.04))
        # "Think of a quiz team that wins a prize."
        cue(self, "Think of")
        self.play(FadeIn(team[0]), FadeIn(team[1]), FadeIn(team[3]), run_time=self.share(0.05))
        # "The player who answered the most questions gets the biggest share, ..."
        cue(self, "The player who")
        show_share(self, team, 0)
        show_share(self, team, 1, 0.04)
        # "... and a player who cost the team points gets a negative one."
        cue(self, "cost the team")
        show_share(self, team, 2)
        # "Here the players are the inputs, ..."
        cue(self, "Here the players")
        self.play(FadeIn(inputs[0]), FadeIn(inputs[3]), run_time=self.share(0.05))
        # "... and the prize is the gap between the average and this station's prediction: 2.42 animals."
        cue(self, "and the prize")
        self.play(FadeIn(inputs[1]), run_time=self.share(0.05))
        # "The input that raised the prediction most gets the biggest share, ..."
        cue(self, "The input that raised")
        show_share(self, inputs, 0)
        show_share(self, inputs, 1, 0.04)
        # "... and an input that pulled it down gets a negative one."
        cue(self, "pulled it down")
        show_share(self, inputs, 2)
        self.finish()


WATERFALL_TOP = 1.9
WATERFALL_STEP = 0.66


def waterfall(scene, length=6.4, x=1.2):
    """Page results: the station's SHAP values as bars from the average to its prediction."""
    shap = scene.data("shap")
    shap = shap.reindex(shap["shap"].abs().sort_values(ascending=False).index)
    average = value(scene, "explaining-one-prediction", "average")
    prediction = value(scene, "explaining-one-prediction", "prediction")
    axes, frame = chart([0, 8, 1], [0, 1, 1], length, 0.01, [0, 2, 4, 6, 8], [], "predicted count (animals)", None)
    VGroup(axes, frame).shift([x - axes.get_x(), -2.6 - axes.get_y(), 0])
    rows = VGroup()
    running = average
    for i, (_, row) in enumerate(shap.iterrows()):
        y = WATERFALL_TOP - i * WATERFALL_STEP
        start, end = running, running + row["shap"]
        running = end
        colour = BLUE if row["shap"] > 0 else ORANGE
        x0, x1 = axes.c2p(min(start, end), 0)[0], axes.c2p(max(start, end), 0)[0]
        bar = Rectangle(width=max(x1 - x0, 0.02), height=0.44, stroke_width=0, fill_color=colour,
                        fill_opacity=1).move_to([(x0 + x1) / 2, y, 0])
        words = label(f"{INPUT_NAMES[row['input']]} = {row['value']}{UNITS[row['input']]}", 28, INK).move_to(
            [axes.c2p(0, 0)[0] - 0.2, y, 0], aligned_edge=RIGHT)
        amount = label(f"{row['shap']:+.2f}", 28, colour, weight=BOLD).move_to(
            [axes.c2p(8, 0)[0] + 0.9, y, 0])
        row_group = VGroup(words, bar, amount)
        row_group.lifts = row["shap"] > 0
        rows.add(row_group)
    top_y, bottom_y = WATERFALL_TOP + 0.5, WATERFALL_TOP - (len(shap) - 1) * WATERFALL_STEP - 0.5
    lines = VGroup(*[DashedLine([axes.c2p(v, 0)[0], top_y, 0], [axes.c2p(v, 0)[0], bottom_y, 0],
                                color=GREY, stroke_width=3) for v in (average, prediction)])
    # each tag above its line, on the side away from the other line
    start_tag = label(f"average {average:.2f}", 26, SUBDUED, weight=BOLD)
    end_tag = label(f"prediction {prediction:.2f}", 28, INK, weight=BOLD)
    for tag, line, outward in ((start_tag, lines[0], prediction > average),
                               (end_tag, lines[1], prediction < average)):
        tag.next_to(line, UP, 0.1)
        tag.align_to(line, RIGHT if outward else LEFT)
    return shap, rows, lines, start_tag, end_tag, frame


def reveal(scene, rows, i, share=0.07):
    scene.play(FadeIn(rows[i][0]), GrowFromEdge(rows[i][1], LEFT if rows[i].lifts else RIGHT),
               FadeIn(rows[i][2]), run_time=scene.share(share))


class Scene15(VideoScene):
    """Page results: the station's SHAP values, from the average 4.11 to its prediction 6.53."""

    number = 15

    def construct(self):
        shap, rows, lines, start_tag, end_tag, frame = waterfall(self)
        depth = shap.set_index("input").loc["depth_m", "value"]
        head = label(f"this station, {depth} m deep", 36, BLUE, weight=BOLD).to_edge(UP, buff=0.3)
        reasons = label("a prediction with its reasons", 36, BLUE, weight=BOLD).to_edge(UP, buff=0.3)
        order = list(shap["input"])
        # "At this station, 44.9 metres deep, depth adds 0.95 animals to the average."
        self.play(FadeIn(head), FadeIn(frame), Create(lines[0]), FadeIn(start_tag), run_time=self.share(0.06))
        cue(self, "depth adds")
        reveal(self, rows, order.index("depth_m"))
        # "Chlorophyll adds 0.8, temperature 0.63, and salinity 0.58."
        for term, phrase in (("chlorophyll_mg_m3", "Chlorophyll adds"), ("temperature_c", "temperature 0.63"),
                             ("salinity_psu", "and salinity")):
            cue(self, phrase)
            reveal(self, rows, order.index(term), 0.04)
        # "Its sandy seabed takes off 0.49, and the season almost nothing."
        cue(self, "Its sandy")
        reveal(self, rows, order.index("substrate"), 0.04)
        cue(self, "and the season")
        reveal(self, rows, order.index("season"), 0.04)
        self.play(Create(lines[1]), FadeIn(end_tag, scale=1.2), run_time=self.share(0.05))
        # "So each prediction comes with its reasons: check them against what you know of the
        # species, or show them to whoever acts on the prediction."
        cue(self, "So each prediction")
        self.play(ReplacementTransform(head, reasons), run_time=self.share(0.06))
        self.play(Indicate(VGroup(*[r[1] for r in rows]), color=INK, scale_factor=1.03), run_time=self.share(0.1))
        self.finish()


class Scene16(KeyPointScene):
    number, point = 16, 3


# The quiz (scenes 17–18) --------------------------------------------------------------------

class Scene17(QuizScene):
    number = 17
    question = ("Shuffling salinity barely changes", "the forest's error. Does that mean",
                "salinity has no effect on the species?")


class Scene18(VideoScene):
    """Page results: season's importance with temperature in the forest, and without it."""

    number = 18

    def construct(self):
        table = self.data("importance").set_index(["forest", "input"])["rise"]
        answer = label("Not necessarily", 56, VERMILION, weight=BOLD).to_edge(UP, buff=0.4)
        top = 0.4
        length = 6.0
        groups = VGroup()
        for i, term in enumerate(("temperature_c", "season")):
            y = 0.6 - i * 1.8
            name = label(INPUT_NAMES[term], 34, INK, weight=BOLD).move_to([-2.6, y - 0.3, 0], aligned_edge=RIGHT)
            bars = VGroup()
            for j, (forest, colour) in enumerate((("all six", BLUE), ("without temperature", ORANGE))):
                rise = table.get((forest, term), np.nan)
                yy = y - j * 0.6
                if np.isnan(rise):
                    bar = label("left out", 26, ORANGE).move_to([-2.2, yy, 0], aligned_edge=LEFT)
                    bars.add(VGroup(bar))
                    continue
                bar = Rectangle(width=rise / top * length, height=0.44, stroke_width=0, fill_color=colour,
                                fill_opacity=1).move_to([-2.2, yy, 0], aligned_edge=LEFT)
                amount = label(f"{rise:.2f}", 28, colour, weight=BOLD).next_to(bar, RIGHT, 0.15)
                bars.add(VGroup(bar, amount))
            groups.add(VGroup(name, bars))
        key = VGroup(VGroup(Square(0.3, fill_color=BLUE, fill_opacity=1, stroke_width=0),
                            label("all six inputs", 26, BLUE)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.3, fill_color=ORANGE, fill_opacity=1, stroke_width=0),
                            label("fitted without temperature", 26, ORANGE)).arrange(RIGHT, buff=0.15)
                     ).arrange(RIGHT, buff=0.6).next_to(answer, DOWN, 0.4)
        shared = label("the same information, shared", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.35)
        temperature, season = groups
        # "Not necessarily."
        self.play(FadeIn(answer, scale=1.2), run_time=self.share(0.05))
        # "Importance says what this forest relies on, given its other inputs."
        cue(self, "Importance says")
        self.play(FadeIn(key), FadeIn(temperature[0]), FadeIn(season[0]),
                  GrowFromEdge(temperature[1][0][0], LEFT), FadeIn(temperature[1][0][1]),
                  GrowFromEdge(season[1][0][0], LEFT), FadeIn(season[1][0][1]), run_time=self.share(0.1))
        # "Two inputs that carry the same information share the work."
        cue(self, "Two inputs")
        self.play(Indicate(VGroup(temperature[0], season[0]), color=BLUE), run_time=self.share(0.08))
        # "Fitted again without temperature, the forest leaned on season instead: ..."
        cue(self, "Fitted again")
        self.play(FadeIn(temperature[1][1]), run_time=self.share(0.06))
        # "... its importance rose from 0.04 to 0.15, ..."
        cue(self, "its importance rose")
        self.play(GrowFromEdge(season[1][1][0], LEFT), FadeIn(season[1][1][1]), run_time=self.share(0.08))
        # "... because summer water is warm and winter water cold."
        # "A low score can mean another input already told the model the same thing."
        cue(self, "A low score")
        self.play(FadeIn(shared, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


# Key points and end card (scenes 19–22) ----------------------------------------------------

class Scene19(RecapScene):
    number, point = 19, 1


class Scene20(RecapScene):
    number, point = 20, 2


class Scene21(RecapScene):
    number, point = 21, 3


class Scene22(EndCardScene):
    number = 22
