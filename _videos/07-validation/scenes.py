"""Manim scenes for the validation video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/07-validation
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


PROMISES = ["Why a single score is never enough",
            "Why the way you split is a question",
            "Why performance measures disagree"]
ANSWERS = ["Use folds, nest any\nsearch, and give\nan interval",
           "Hold out what you\nwill actually be\nasked to predict",
           "Each minds different\nmistakes: choose from the\nsentence you will write"]
RECAP = ["A single score is never enough",
         "The way you split is a question",
         "Choose the measure from your sentence"]


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


def number_line(lo, hi, x0, x1, y, ticks, digits=2, size=26):
    """A horizontal value axis from x0 to x1 at height y; returns it and a mapper."""
    to_x = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)  # noqa: E731
    line = Line([x0, y, 0], [x1, y, 0], color=GRID, stroke_width=3)
    marks = VGroup(*[VGroup(Line([to_x(t), y - 0.08, 0], [to_x(t), y + 0.08, 0], color=GRID,
                                 stroke_width=3),
                            label(f"{t:.{digits}f}", size, SUBDUED).move_to([to_x(t), y - 0.35, 0]))
                     for t in ticks])
    return VGroup(line, marks), to_x


def counter(value, x, y, size=72, colour=INK):
    """A whole number that counts up from zero: a tracker and the label it draws."""
    tracker = ValueTracker(0)
    shown = always_redraw(lambda: label(f"{tracker.get_value():.0f}", size, colour, weight=BOLD
                                        ).move_to([x, y, 0]))
    return tracker, shown


# The puzzle: two models, two winners (scenes 2–5 and 41–43, page results) ----------------

FOREST_X, LOG_X = 0.9, 4.6


def puzzle_layout(scene):
    objectives = scene.data("objectives").set_index("model")
    forest, log = objectives.loc["random forest"], objectives.loc["log-transformed lm"]
    cards = VGroup()
    for x, name, sub, colour in ((FOREST_X, "random forest", "many trees", BLUE),
                                 (LOG_X, "log model", "a line through the log", ORANGE)):
        box = RoundedRectangle(width=3.6, height=1.4, corner_radius=0.15, stroke_color=colour,
                               stroke_width=5).move_to([x, 2.3, 0])
        text = VGroup(label(name, 36, colour, weight=BOLD), label(sub, 24, SUBDUED)
                      ).arrange(DOWN, buff=0.12).move_to(box)
        cards.add(VGroup(box, text))

    def row(y, name, values, fmt, best):
        """A row of two results: its name on the left, each model's value under its card."""
        head = VGroup(*[label(t, 30, SUBDUED) for t in name.split("\n")]
                      ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([-6.6, y, 0], aligned_edge=LEFT)
        shown = VGroup(*[label(fmt(v), 60, INK, weight=BOLD).move_to([x, y, 0])
                         for x, v in zip((FOREST_X, LOG_X), values)])
        box, mark = tick(0.6)
        box.next_to(shown[best], RIGHT, 0.3)
        mark.move_to(box)
        return VGroup(head, shown, VGroup(box, mark))

    rmse = row(0.6, "error at each station\n(RMSE, lower is better)",
               (forest["rmse"], log["rmse"]), lambda v: f"{v:.2f}",
               int(log["rmse"] < forest["rmse"]))
    caught = row(-1.2, "animals at its top\nfifty stations",
                 (forest["caught"], log["caught"]), lambda v: f"{v:.0f}",
                 int(log["caught"] > forest["caught"]))
    total = row(-3.0, "share of all animals\nits predictions add up to",
                (forest["total_ratio"], log["total_ratio"]), percent,
                int(abs(log["total_ratio"] - 1) < abs(forest["total_ratio"] - 1)))
    return cards, rmse, caught, total, (forest, log)


class Scene02(VideoScene):
    number = 2

    def construct(self):
        cards, *_ = puzzle_layout(self)
        head = label("Two models of the same survey", 34, SUBDUED).to_edge(UP, buff=0.25)
        # "Here are two models of the same survey: a random forest, ..."
        self.play(FadeIn(head), FadeIn(cards[0], shift=0.3 * DOWN), run_time=self.share(0.3))
        self.wait(max(self.share(0.45) - self.time, 0.01))
        # "... and a simpler model of the log of the counts."
        self.play(FadeIn(cards[1], shift=0.3 * DOWN), run_time=self.share(0.25))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        cards, rmse, *_ = puzzle_layout(self)
        head = label("Two models of the same survey", 34, SUBDUED).to_edge(UP, buff=0.25)
        self.add(head, cards)
        # "By the usual error measure, the forest wins: 4.36 against 4.46."
        self.play(FadeIn(rmse[0]), run_time=self.share(0.2))
        self.play(LaggedStart(*[FadeIn(v, shift=0.2 * UP) for v in rmse[1]], lag_ratio=0.5),
                  run_time=self.share(0.35))
        self.play(FadeIn(rmse[2][0]), Create(rmse[2][1]), run_time=self.share(0.15))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        cards, rmse, caught, _, (forest, log) = puzzle_layout(self)
        head = label("Two models of the same survey", 34, SUBDUED).to_edge(UP, buff=0.25)
        self.add(head, cards, rmse)
        trackers = [counter(v, x, -1.2, 60) for v, x in ((forest["caught"], FOREST_X),
                                                          (log["caught"], LOG_X))]
        # "Now send a ship to the fifty stations each model ranks highest."
        self.play(FadeIn(caught[0]), *[FadeIn(s) for _, s in trackers], run_time=self.share(0.2))
        self.wait(max(self.share(0.4) - self.time, 0.01))
        # "The log model's stations hold 481 animals. The forest's hold 456."
        self.play(trackers[1][0].animate.set_value(log["caught"]), run_time=self.share(0.2),
                  rate_func=linear)
        self.play(trackers[0][0].animate.set_value(forest["caught"]), run_time=self.share(0.2),
                  rate_func=linear)
        self.remove(*[s for _, s in trackers])
        self.add(caught[1])
        self.play(FadeIn(caught[2][0]), Create(caught[2][1]), run_time=self.share(0.1))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        cards, rmse, caught, *_ = puzzle_layout(self)
        head = label("Two models of the same survey", 34, SUBDUED).to_edge(UP, buff=0.25)
        self.add(head, cards, rmse, caught)
        mark = label("?", 120, PURPLE, weight=BOLD).move_to([(FOREST_X + LOG_X) / 2, 0, 0])
        # "So which model is better?"
        self.play(FadeIn(mark, scale=2), run_time=self.share(0.3))
        self.play(Wiggle(mark), run_time=self.share(0.5))
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


# One split is a noisy ruler (scenes 7–11, page results) -----------------------------------

GRID_COLS, GRID_ROWS = 40, 18   # 720 stations


def station_grid(y=1.65):
    squares = VGroup(*[Square(0.13, stroke_width=0, fill_color=BLUE, fill_opacity=1)
                       for _ in range(GRID_COLS * GRID_ROWS)])
    squares.arrange_in_grid(GRID_ROWS, GRID_COLS, buff=0.04).move_to([0.6, y, 0])
    return squares


def held_back(squares, seed, share=0.25):
    rng = np.random.default_rng(seed)
    chosen = rng.choice(len(squares), int(share * len(squares)), replace=False)
    return VGroup(*[squares[i].copy().set_fill(ORANGE) for i in chosen])


def split_layout(scene):
    estimates = scene.data("split-estimates")
    single = estimates[estimates["scheme"] == "single 75/25 split"]["rsq"].to_numpy()
    crossval = estimates[estimates["scheme"] == "10-fold cross-validation"]["rsq"].to_numpy()
    squares = station_grid()
    grid_name = label(f"the same {len(squares)} stations, the same model", 28, SUBDUED
                      ).next_to(squares, UP, 0.2)
    key = VGroup(Square(0.22, stroke_width=0, fill_color=ORANGE, fill_opacity=1),
                 label("held back for scoring", 26, SUBDUED)).arrange(RIGHT, buff=0.15
                                                                     ).next_to(squares, DOWN, 0.2)
    axis, to_x = number_line(0.05, 0.37, -3.6, 6.4, -3.0, [0.1, 0.2, 0.3], 1)
    axis_name = label("R² on held-out stations", 26, SUBDUED).next_to(axis, DOWN, 0.05).set_x(1.4)
    rows_y = {"single": -1.3, "cv": -2.3}
    names = VGroup(label("one split", 30, ORANGE, weight=BOLD).move_to([-6.8, rows_y["single"], 0], aligned_edge=LEFT),
                   label("cross-", 30, BLUE, weight=BOLD).move_to([-6.8, rows_y["cv"] + 0.2, 0], aligned_edge=LEFT),
                   label("validation", 30, BLUE, weight=BOLD).move_to([-6.8, rows_y["cv"] - 0.2, 0], aligned_edge=LEFT))
    rng = np.random.default_rng(3)
    dots = {kind: VGroup(*[Dot([to_x(v), rows_y[kind] + rng.uniform(-0.3, 0.3), 0], radius=0.09,
                               color=colour, fill_opacity=0.8)
                           for v in values])
            for kind, values, colour in (("single", single, ORANGE), ("cv", crossval, BLUE))}

    def range_label(values, kind, colour):
        lo, hi = values.min(), values.max()
        if kind == "cv":   # no room above: the single-split dots are there
            y = rows_y[kind]
            brace = Line([to_x(lo), y + 0.4, 0], [to_x(hi), y + 0.4, 0], color=colour, stroke_width=4)
            ends = label(f"{lo:.3f} to {hi:.3f}", 30, colour, weight=BOLD).move_to(
                [to_x(hi) + 0.4, y, 0], aligned_edge=LEFT)
            return VGroup(brace, ends)
        y = rows_y[kind] + 0.5
        brace = Line([to_x(lo), y, 0], [to_x(hi), y, 0], color=colour, stroke_width=4)
        ends = VGroup(label(f"{lo:.3f}", 28, colour, weight=BOLD).next_to(brace.get_start(), UP, 0.1),
                      label(f"{hi:.3f}", 28, colour, weight=BOLD).next_to(brace.get_end(), UP, 0.1))
        return VGroup(brace, ends)

    ranges = {"single": range_label(single, "single", ORANGE), "cv": range_label(crossval, "cv", BLUE)}
    return squares, grid_name, key, VGroup(axis, axis_name), names, dots, ranges


class Scene07(VideoScene):
    number = 7

    def construct(self):
        squares, grid_name, key, axis, names, dots, _ = split_layout(self)
        held = held_back(squares, 1)
        # "The simplest test holds back a quarter of the stations, ..."
        self.play(FadeIn(squares, lag_ratio=0.002), FadeIn(grid_name), run_time=self.share(0.25))
        self.play(FadeIn(held), FadeIn(key), run_time=self.share(0.2))
        # "... and scores the model on them."
        self.play(FadeIn(axis), FadeIn(names[0]), run_time=self.share(0.15))
        first = dots["single"][0]
        self.play(FadeIn(first, shift=0.8 * DOWN, scale=2), run_time=self.share(0.2))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        squares, grid_name, key, axis, names, dots, ranges = split_layout(self)
        held = held_back(squares, 1)
        self.add(squares, grid_name, key, axis, names[0], held, dots["single"][0])
        # "Do that forty times, with forty different splits."
        swaps = 6
        for i in range(swaps):
            new = held_back(squares, 10 + i)
            batch = dots["single"][1 + i * 6: 1 + (i + 1) * 6] if i < swaps - 1 else dots["single"][1 + i * 6:]
            self.play(FadeOut(held), FadeIn(new),
                      LaggedStart(*[FadeIn(d, shift=0.5 * DOWN) for d in batch], lag_ratio=0.2),
                      run_time=self.share(0.55 / swaps))
            held = new
        # "The same model scores an R² anywhere from 0.079 to 0.346."
        self.play(Create(ranges["single"][0]), FadeIn(ranges["single"][1]), run_time=self.share(0.25))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        squares, grid_name, key, axis, names, dots, ranges = split_layout(self)
        held = held_back(squares, 15)
        self.add(squares, grid_name, key, axis, names[0], held, dots["single"], ranges["single"])
        # "Nothing changed but where the line was drawn."
        self.play(Indicate(grid_name, color=INK, scale_factor=1.1), run_time=self.share(0.3))
        for i in range(3):
            new = held_back(squares, 30 + i)
            self.play(FadeOut(held), FadeIn(new), run_time=self.share(0.15))
            held = new
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        squares = station_grid(0.6)
        folds = VGroup(*[VGroup(*[squares[r * GRID_COLS + c] for r in range(GRID_ROWS)
                                  for c in range(4 * f, 4 * f + 4)]) for f in range(10)])
        cuts = VGroup(*[DashedLine(squares[4 * f].get_corner(UL) + [-0.025, 0.1, 0],
                                   squares[(GRID_ROWS - 1) * GRID_COLS + 4 * f].get_corner(DL) + [-0.025, -0.1, 0],
                                   color=INK, stroke_width=3, dash_length=0.08)
                        for f in range(1, 10)])
        head = label("Ten folds: each held out once", 36, INK, weight=BOLD).to_edge(UP, buff=0.8)
        note = label("scored by a model that never saw it", 30, ORANGE).next_to(squares, DOWN, 0.5)
        # "Cross-validation cuts the data into ten folds."
        self.play(FadeIn(squares), FadeIn(head), run_time=self.share(0.15))
        self.play(LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.15), run_time=self.share(0.2))
        # "Each is held out once, and scored by a model that never saw it."
        self.play(FadeIn(note), run_time=self.share(0.08))
        step = self.share(0.5) / 10
        for f in range(10):
            self.play(folds[f].animate.set_fill(ORANGE),
                      *([folds[f - 1].animate.set_fill(BLUE)] if f else []), run_time=step)
        self.play(folds[9].animate.set_fill(BLUE), run_time=min(step, 0.3))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        squares, grid_name, key, axis, names, dots, ranges = split_layout(self)
        held = held_back(squares, 15)
        self.add(squares, grid_name, key, axis, names[0], held, dots["single"], ranges["single"])
        # "Forty cross-validations agree far more closely: ..."
        self.play(FadeIn(names[1:]), FadeOut(held), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d, shift=0.5 * DOWN) for d in dots["cv"]], lag_ratio=0.05),
                  run_time=self.share(0.4))
        # "... from 0.195 to 0.239."
        self.play(Create(ranges["cv"][0]), FadeIn(ranges["cv"][1]), run_time=self.share(0.25))
        self.finish()


# The winner's score flatters (scenes 12–17, page results) ---------------------------------

def search_layout(scene):
    search = scene.data("search")
    cards = VGroup()
    for _, r in search.iterrows():
        cells = VGroup(*[Square(0.13, stroke_width=0, fill_opacity=1,
                                fill_color=GREY if i < r["noise"] else BLUE) for i in range(5)])
        cards.add(cells.arrange(RIGHT, buff=0.03))
    cards.arrange_in_grid(10, 10, buff=(0.28, 0.24)).move_to([0, -0.1, 0])
    head = label("A hundred candidate models, five columns each", 34, SUBDUED).to_edge(UP, buff=0.4)
    key = VGroup(
        VGroup(Square(0.25, stroke_width=0, fill_color=BLUE, fill_opacity=1), label("real predictor", 28)),
        VGroup(Square(0.25, stroke_width=0, fill_color=GREY, fill_opacity=1), label("random noise", 28)))
    for k in key:
        k.arrange(RIGHT, buff=0.15)
    key.arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.4)

    lo, hi = search["rmse"].min(), search["rmse"].max()
    axis, to_x = number_line(4.45, 4.85, -5.5, 5.5, -1.6, [4.5, 4.6, 4.7, 4.8], 1)
    axis_name = label("cross-validated error (RMSE) of each candidate", 28, SUBDUED
                      ).next_to(axis, DOWN, 0.1)
    rng = np.random.default_rng(12)
    dots = VGroup(*[Dot([to_x(v), -0.8 + rng.uniform(-0.45, 0.45), 0], radius=0.09,
                        color=VERMILION if w else GREY, fill_opacity=1 if w else 0.7)
                    for v, w in zip(search["rmse"], search["winner"])])
    winner = int(np.flatnonzero(search["winner"].to_numpy())[0])
    return search, head, cards, key, VGroup(axis, axis_name), dots, winner, to_x


class Scene12(VideoScene):
    number = 12

    def construct(self):
        search, head, cards, key, axis, dots, winner, to_x = search_layout(self)
        # "Now search for the best predictors. Add twenty columns of random noise, ..."
        self.play(FadeIn(head), FadeIn(key), run_time=self.share(0.2))
        self.wait(max(self.share(0.4) - self.time, 0.01))
        # "... and try a hundred models of five columns each."
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cards], lag_ratio=0.02),
                  run_time=self.share(0.45))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        search, head, cards, key, axis, dots, winner, to_x = search_layout(self)
        self.add(head, cards, key)
        best = dots[winner]
        value = VGroup(label(f"{search['rmse'].min():.3f}", 44, VERMILION, weight=BOLD),
                       label("best of the hundred", 28, VERMILION)).arrange(DOWN, buff=0.1
                                                                           ).next_to(best, UP, 0.9)
        pointer = Arrow(value.get_bottom(), best.get_top(), buff=0.1, color=VERMILION, stroke_width=5)
        # "The winner's cross-validated error is 4.472, ..."
        self.play(FadeOut(key), FadeOut(head), FadeIn(axis),
                  *[ReplacementTransform(c, d) for c, d in zip(cards, dots)], run_time=self.share(0.4))
        # "... the best of the hundred."
        self.play(GrowArrow(pointer), FadeIn(value), best.animate.scale(1.6), run_time=self.share(0.25))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        search, head, cards, key, axis, dots, winner, to_x = search_layout(self)
        dots[winner].scale(1.6)
        self.add(axis, dots)
        noise = int(search.loc[winner, "noise"])
        cells = VGroup(*[Square(0.7, stroke_width=0, fill_opacity=1,
                                fill_color=GREY if i < noise else BLUE) for i in range(5)]
                       ).arrange(RIGHT, buff=0.4).move_to([0, 2.4, 0])
        names = VGroup(*[label("noise" if i < noise else "real", 24, SUBDUED).next_to(c, DOWN, 0.15)
                         for i, c in enumerate(cells)])
        head = label("the winner's five columns", 30, VERMILION, weight=BOLD).next_to(cells, UP, 0.3)
        luck = label("lowest of a hundred noisy scores: partly luck", 32, INK
                     ).move_to([0, 0.35, 0])
        # "Three of its five columns are pure noise."
        self.play(TransformFromCopy(dots[winner], cells), FadeIn(head), run_time=self.share(0.25))
        self.play(FadeIn(names), *[Indicate(c, color=GREY) for c in cells[:noise]], run_time=self.share(0.2))
        # "The best of a hundred noisy scores is low partly by luck."
        self.play(FadeIn(luck), run_time=self.share(0.15))
        self.play(Wiggle(dots[winner], scale_value=1.8), run_time=self.share(0.2))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        blocks = VGroup(*[Rectangle(width=2.2, height=0.9, stroke_color=BACKGROUND, stroke_width=4,
                                    fill_color=BLUE, fill_opacity=1) for _ in range(5)]
                        ).arrange(RIGHT, buff=0).move_to([0, 1.8, 0])
        head = label("Nested cross-validation", 38, INK, weight=BOLD).to_edge(UP, buff=0.25)
        mini = VGroup(*[Square(0.12, stroke_width=0, fill_color=GREY, fill_opacity=1) for _ in range(100)]
                      ).arrange_in_grid(10, 10, buff=0.06).move_to([-2.5, -0.9, 0])
        search_name = label("the whole search, again,", 28, SUBDUED).next_to(mini, DOWN, 0.25)
        search_name2 = label("on the other four folds", 28, SUBDUED).next_to(search_name, DOWN, 0.1)
        held_name = label("scored here, where the search never looked", 28, ORANGE)
        # "Nested cross-validation repeats the whole search inside each fold, ..."
        self.play(FadeIn(head), FadeIn(blocks), run_time=self.share(0.12))
        rounds = 3
        arrow = None
        for f in range(rounds):
            chosen = mini[(37 * f + 11) % 100]
            target = blocks[f].get_bottom()
            new_arrow = Arrow(mini.get_top() + [0.8, 0, 0], target, buff=0.15, color=ORANGE, stroke_width=5)
            anims = [blocks[f].animate.set_fill(ORANGE)] + ([blocks[f - 1].animate.set_fill(BLUE)] if f else [])
            if f == 0:
                anims += [FadeIn(mini), FadeIn(search_name), FadeIn(search_name2)]
            else:
                anims += [mini.animate.set_fill(GREY), FadeOut(arrow)]
            self.play(*anims, run_time=self.share(0.08))
            self.play(LaggedStart(*[Indicate(s, color=INK, scale_factor=1.5) for s in mini[::7]], lag_ratio=0.05),
                      run_time=self.share(0.1))
            self.play(chosen.animate.set_fill(VERMILION), GrowArrow(new_arrow), run_time=self.share(0.06))
            if f == 0:
                # "... and scores its choice on data the search never saw."
                held_name.next_to(blocks, UP, 0.2)
                self.play(FadeIn(held_name), run_time=self.share(0.05))
            arrow = new_arrow
        self.finish()


def nested_layout(scene):
    nested = scene.data("nested")
    reported = nested["search reported"].mean()
    honest = nested["search's model, honestly"].mean()
    axis, to_x = number_line(4.3, 5.0, -4.5, 5.5, -1.1, [4.4, 4.6, 4.8, 5.0], 1)
    axis_name = label("error (RMSE), lower is better", 28, SUBDUED).next_to(axis, DOWN, 0.1)
    dot_rep = Dot([to_x(reported), 0, 0], radius=0.16, color=GREY)
    rep_name = VGroup(label("what the search reported", 28, SUBDUED),
                      label(f"{reported:.3f}", 44, INK, weight=BOLD)).arrange(DOWN, buff=0.1
                                                                         ).next_to(dot_rep, UP, 0.3)
    dot_hon = Dot([to_x(honest), 0, 0], radius=0.16, color=VERMILION)
    hon_name = VGroup(label("its model, honestly", 28, VERMILION),
                      label(f"{honest:.3f}", 44, VERMILION, weight=BOLD)).arrange(DOWN, buff=0.1
                                                                            ).next_to(dot_hon, UP, 0.3)
    gap = Arrow(dot_rep.get_right(), dot_hon.get_left(), buff=0.1, color=VERMILION, stroke_width=5)
    gap_name = label(f"about {100 * (honest / reported - 1):.0f}% worse", 30, VERMILION
                     ).next_to(gap, DOWN, 0.2)
    return nested, VGroup(axis, axis_name), VGroup(dot_rep, rep_name), VGroup(dot_hon, hon_name), VGroup(gap, gap_name)


class Scene16(VideoScene):
    number = 16

    def construct(self):
        nested, axis, rep, hon, gap = nested_layout(self)
        head = label("The search, measured honestly", 36, INK, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(FadeIn(head), FadeIn(axis), FadeIn(rep), run_time=self.share(0.2))
        # "Inside the folds, the search reported 4.472. Its choice actually scored 4.851: ..."
        self.play(TransformFromCopy(rep[0], hon[0]), run_time=self.share(0.2))
        self.play(FadeIn(hon[1]), run_time=self.share(0.15))
        # "... about 8% worse."
        self.play(GrowArrow(gap[0]), FadeIn(gap[1]), run_time=self.share(0.2))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        nested = self.data("nested")
        axis, to_x = number_line(3.8, 5.4, -2.5, 5.5, -2.55, [4.0, 4.5, 5.0], 1)
        axis_name = label("error (RMSE) on each outer fold", 26, SUBDUED).next_to(axis, DOWN, 0.05)
        head = label("Five outer folds", 36, INK, weight=BOLD).to_edge(UP, buff=0.3)
        key = VGroup(VGroup(Dot(radius=0.12, color=VERMILION), label("searched model", 28)).arrange(RIGHT, buff=0.15),
                     VGroup(Dot(radius=0.12, color=GREEN), label("no search at all", 28)).arrange(RIGHT, buff=0.15)
                     ).arrange(RIGHT, buff=0.8).next_to(head, DOWN, 0.3)
        rows = VGroup()
        wins = 0
        for i, (_, r) in enumerate(nested.iterrows()):
            y = 1.5 - 0.85 * i
            name = label(f"fold {int(r['fold'])}", 30, SUBDUED).move_to([-4.3, y, 0])
            s, n = r["search's model, honestly"], r["no search at all"]
            link = Line([to_x(s), y, 0], [to_x(n), y, 0], color=GRID, stroke_width=4)
            ds = Dot([to_x(s), y, 0], radius=0.13, color=VERMILION)
            dn = Dot([to_x(n), y, 0], radius=0.13, color=GREEN)
            box, mark = tick(0.45)
            box.move_to([6.4, y, 0])
            mark.move_to(box)
            wins += n < s
            rows.add(VGroup(name, link, ds, dn, VGroup(box, mark) if n < s else VGroup()))
        total = label(f"no search wins {wins} of {len(nested)}", 32, GREEN, weight=BOLD).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(head), FadeIn(key), FadeIn(axis), FadeIn(axis_name),
                  *[FadeIn(VGroup(r[0], r[2])) for r in rows], run_time=self.share(0.25))
        # "And a model with no search at all beat the searched one on all five folds."
        self.play(LaggedStart(*[AnimationGroup(Create(r[1]), FadeIn(r[3], scale=1.5), FadeIn(r[4]))
                                for r in rows], lag_ratio=0.3), run_time=self.share(0.5))
        self.play(FadeIn(total), run_time=self.share(0.1))
        self.finish()


# A score needs an interval (scenes 18–21, page results) -----------------------------------

class Scene18(VideoScene):
    number = 18

    def construct(self):
        r = self.data("interval").iloc[0]
        axis, to_x = number_line(3.4, 4.9, -5.5, 5.5, -1.0, [3.5, 4.0, 4.5], 1)
        axis_name = label("error (RMSE) of the Poisson model", 28, SUBDUED).next_to(axis, DOWN, 0.1)
        point = Dot([to_x(r["estimate"]), 0.2, 0], radius=0.18, color=BLUE)
        value = label(f"{r['estimate']:.2f}", 56, BLUE, weight=BOLD).next_to(point, UP, 0.35)
        band = Line([to_x(r["lower"]), 0.2, 0], [to_x(r["upper"]), 0.2, 0], color=BLUE, stroke_width=14,
                    stroke_opacity=0.5)
        ends = VGroup(label(f"{r['lower']:.2f}", 40, BLUE).next_to(band.get_start(), DOWN, 0.3),
                      label(f"{r['upper']:.2f}", 40, BLUE).next_to(band.get_end(), DOWN, 0.3))
        name = label("95% interval: a different 720 stations could give any of these", 30, SUBDUED
                     ).move_to([0, 2.6, 0])
        # "A score is an estimate, like an average catch."
        self.play(FadeIn(axis), FadeIn(axis_name), FadeIn(point, scale=2), run_time=self.share(0.2))
        # "Resample the stations, and an error of 4.14 ..."
        self.wait(max(self.share(0.4) - self.time, 0.01))
        self.play(FadeIn(value, shift=0.2 * UP), run_time=self.share(0.12))
        # "... could be anywhere from 3.70 to 4.58."
        self.play(GrowFromCenter(band), run_time=self.share(0.2))
        self.play(FadeIn(ends), FadeIn(name), run_time=self.share(0.12))
        self.finish()


def paired_layout(scene):
    per_fold = scene.data("per-fold")
    paired = scene.data("paired").set_index("comparison")
    to_y = lambda v: -2.6 + (v - 3.0) / (6.2 - 3.0) * 5.0  # noqa: E731
    xs = {"glm": -5.5, "forest": -2.7}
    col_names = VGroup(label("Poisson GLM", 26, BLUE, weight=BOLD).move_to([xs["glm"], 3.0, 0]),
                       label("random forest", 26, ORANGE, weight=BOLD).move_to([xs["forest"], 3.0, 0]))
    y_ticks = VGroup(*[label(f"{v:.0f}", 24, SUBDUED).move_to([-6.6, to_y(v), 0]) for v in (3, 4, 5, 6)])
    y_name = label("RMSE on each fold", 24, SUBDUED).rotate(PI / 2).move_to([-7.0 + 0.05, 0.1, 0])
    dots = {m: VGroup(*[Dot([x, to_y(v), 0], radius=0.11, color=BLUE if m == "glm" else ORANGE)
                        for v in per_fold[m]]) for m, x in xs.items()}
    links = VGroup(*[Line([xs["glm"], to_y(g), 0], [xs["forest"], to_y(f), 0], color=GREY, stroke_width=3)
                     for g, f in zip(per_fold["glm"], per_fold["forest"])])

    axis, to_x = number_line(-0.8, 1.2, 0.0, 6.4, -2.9, [-0.5, 0, 0.5, 1.0], 1, 24)
    axis_name = label("forest minus GLM", 26, SUBDUED).next_to(axis, DOWN, 0.05)
    zero = DashedLine([to_x(0), 2.4, 0], [to_x(0), -2.9, 0], color=GREY, stroke_width=3)
    head = label("The difference between the two models", 28, SUBDUED).move_to([3.2, 3.0, 0])

    def interval(name, y, colour):
        r = paired.loc[name]
        bar = Line([to_x(r["lower"]), y, 0], [to_x(r["upper"]), y, 0], color=colour, stroke_width=16)
        text = label(f"{name}: {r['upper'] - r['lower']:.2f} wide", 30, colour, weight=BOLD
                     ).next_to(bar, UP, 0.2).set_x(3.2)
        return VGroup(bar, text)

    unpaired = interval("unpaired", 1.3, GREY)
    paired_bar = interval("paired", -0.3, VERMILION)
    rng = np.random.default_rng(20)
    diffs = VGroup(*[Dot([to_x(f - g), -1.9 + rng.uniform(-0.3, 0.3), 0], radius=0.1, color=VERMILION)
                     for g, f in zip(per_fold["glm"], per_fold["forest"])])
    left = VGroup(col_names, y_ticks, y_name, dots["glm"], dots["forest"])
    right = VGroup(axis, axis_name, zero, head)
    return left, links, right, unpaired, paired_bar, diffs, dots


class Scene19(VideoScene):
    number = 19

    def construct(self):
        left, links, right, unpaired, paired_bar, diffs, dots = paired_layout(self)
        # "Compare two models on ten folds, and their scores overlap almost completely."
        self.play(FadeIn(left[:3]), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in [*dots["glm"], *dots["forest"]]], lag_ratio=0.04),
                  run_time=self.share(0.3))
        # "The interval on the difference is 1.54 wide, and covers zero."
        self.play(FadeIn(right), run_time=self.share(0.12))
        self.play(GrowFromCenter(unpaired[0]), FadeIn(unpaired[1]), run_time=self.share(0.2))
        self.play(Indicate(right[2], color=INK), run_time=self.share(0.12))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        left, links, right, unpaired, paired_bar, diffs, dots = paired_layout(self)
        self.add(left, right, unpaired)
        # "Pair the scores fold by fold, ..."
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.1), run_time=self.share(0.3))
        self.play(LaggedStart(*[TransformFromCopy(l, d) for l, d in zip(links, diffs)], lag_ratio=0.05),
                  run_time=self.share(0.2))
        # "... and it is 0.33 wide: nearly five times sharper, from the same numbers."
        self.play(TransformFromCopy(unpaired[0], paired_bar[0]), FadeIn(paired_bar[1]), run_time=self.share(0.25))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        left, links, right, unpaired, paired_bar, diffs, dots = paired_layout(self)
        self.add(left, links, right, unpaired, paired_bar, diffs)
        note = VGroup(label("high or low:", 30, INK), label("the fold, more than the model", 30, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.1).move_to([-4.1, -3.45, 0])
        # "Most of what makes a score high or low is the fold."
        self.play(LaggedStart(*[Indicate(l, color=INK, scale_factor=1.05) for l in links], lag_ratio=0.1),
                  FadeIn(note), run_time=self.share(0.45))
        # "So always compare models on the same folds."
        self.play(Circumscribe(paired_bar, color=VERMILION), run_time=self.share(0.3))
        self.finish()


class Scene22(KeyPointScene):
    number, point = 22, 1


# The split is a question (scenes 23–30, page results) -------------------------------------

def shelf(stations, width=6.4, height=6.4, centre=(-3.2, -0.2)):
    """Map positions for the stations: longitude shrunk by cos(42°), as the page does."""
    x = stations["longitude"] * np.cos(np.radians(42))
    y = stations["latitude"]
    s = min(width / (x.max() - x.min()), height / (y.max() - y.min()))
    cx, cy = (x.max() + x.min()) / 2, (y.max() + y.min()) / 2
    to = lambda lon, lat: np.array([centre[0] + s * (lon * np.cos(np.radians(42)) - cx),  # noqa: E731
                                    centre[1] + s * (lat - cy), 0])
    return to


def schemes_layout(scene):
    stations = scene.data("stations")
    to = shelf(stations)
    dots = VGroup(*[Dot(to(lon, lat), radius=0.05, color=BLUE, fill_opacity=0.8)
                    for lon, lat in zip(stations["longitude"], stations["latitude"])])
    return stations, to, dots


def scheme_text(heading, question, colour=ORANGE):
    return VGroup(label(heading, 40, colour, weight=BOLD),
                  *[label(t, 32, INK) for t in question]).arrange(DOWN, buff=0.2, aligned_edge=LEFT
                                                                 ).move_to([1.2, 0, 0], aligned_edge=LEFT)


def held_dots(dots, mask):
    return VGroup(*[d.copy().set_color(ORANGE).scale(1.5) for d, m in zip(dots, mask) if m])


class Scene23(VideoScene):
    number = 23

    def construct(self):
        stations, to, dots = schemes_layout(self)
        rng = np.random.default_rng(23)
        held = held_dots(dots, rng.random(len(dots)) < 0.1)
        text = scheme_text("Random folds", ["how well does it fill", "the gaps between", "stations it has seen?"])
        head = label("Every split asks a question", 36, SUBDUED).to_edge(UP, buff=0.4)
        # "Every way of splitting the data asks a question."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.001), run_time=self.share(0.3))
        # "Random folds ask how well a model fills the gaps between stations it has seen."
        self.play(FadeIn(held), run_time=self.share(0.2))
        self.play(FadeIn(text, shift=0.2 * LEFT), run_time=self.share(0.2))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        stations, to, dots = schemes_layout(self)
        head = label("Every split asks a question", 36, SUBDUED).to_edge(UP, buff=0.4)
        self.add(head, dots)
        size = 0.5
        bx = np.floor(stations["longitude"] / size)
        by = np.floor(stations["latitude"] / size)
        block = bx.astype(int).astype(str) + "_" + by.astype(int).astype(str)
        blocks = block.unique()
        fold = dict(zip(blocks, np.random.default_rng(24).permutation(len(blocks)) % 10))
        held_blocks = [b for b in blocks if fold[b] in (0, 1)]
        cells = VGroup()
        for b in held_blocks:
            i, j = (int(v) for v in b.split("_"))
            lo, hi = to(i * size, j * size), to((i + 1) * size, (j + 1) * size)
            cells.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_color=ORANGE,
                                stroke_width=3, fill_color=ORANGE, fill_opacity=0.15
                                ).move_to((lo + hi) / 2))
        held = held_dots(dots, block.isin(held_blocks))
        text = scheme_text("Blocks of the shelf", ["how well does it map", "ground never surveyed?"])
        # "Hold out whole blocks of the shelf, ..."
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.1), run_time=self.share(0.3))
        self.play(FadeIn(held), run_time=self.share(0.15))
        # "... and you ask how well it maps ground never surveyed."
        self.play(FadeIn(text, shift=0.2 * LEFT), run_time=self.share(0.2))
        self.finish()


class Scene25(VideoScene):
    number = 25

    def construct(self):
        stations, to, dots = schemes_layout(self)
        head = label("Every split asks a question", 36, SUBDUED).to_edge(UP, buff=0.4)
        self.add(head, dots)
        year = sorted(stations["survey_year"].unique())[-1]
        held = held_dots(dots, stations["survey_year"] == year)
        text = scheme_text("A whole year", ["how well does it", "forecast?"])
        # "Hold out a whole year, ..."
        self.play(FadeIn(held), run_time=self.share(0.3))
        # "... and you ask how well it forecasts."
        self.play(FadeIn(text, shift=0.2 * LEFT), run_time=self.share(0.25))
        self.finish()


SCHEME_NAMES = {"random 10-fold": "random folds", "grouped by site": "grouped by site",
                "spatial blocks, 1.20°": "largest blocks", "leave-one-year-out": "one year out"}


def distance_layout(scene):
    schemes = scene.data("schemes")
    axes = plain_axes([0, 28, 5], [0.10, 0.24, 0.05], 10.0, 5.2).shift(0.6 * RIGHT + 0.3 * DOWN)
    ticks_x = VGroup(*[label(f"{v}", 24, SUBDUED).next_to(axes.c2p(v, 0.10), DOWN, 0.15) for v in (5, 10, 15, 20, 25)])
    ticks_y = VGroup(*[label(f"{v:.2f}", 24, SUBDUED).next_to(axes.c2p(0, v), LEFT, 0.15) for v in (0.10, 0.15, 0.20)])
    x_name = label("distance to the nearest training station (km)", 26, SUBDUED).next_to(ticks_x, DOWN, 0.15)
    y_name = label("R²", 28, SUBDUED).next_to(ticks_y, UP, 0.2)
    head = label("The same forest, the same 720 stations", 32, SUBDUED).to_edge(UP, buff=0.3)
    temporal = schemes["scheme"] == "leave-one-year-out"
    points = VGroup()
    for _, r in schemes.iterrows():
        if r["scheme"] == "leave-one-year-out":
            p = Circle(0.12, color=VERMILION, stroke_width=4).move_to(axes.c2p(r["nearest_km"], r["R2"]))
        else:
            p = Dot(axes.c2p(r["nearest_km"], r["R2"]), radius=0.12, color=BLUE)
        points.add(p)
    space = schemes[~temporal]
    slope, intercept = np.polyfit(space["nearest_km"], space["R2"], 1)
    x0, x1 = space["nearest_km"].min() - 1, space["nearest_km"].max() + 1
    trend = DashedLine(axes.c2p(x0, intercept + slope * x0), axes.c2p(x1, intercept + slope * x1),
                       color=GREY, stroke_width=4, dash_length=0.12)
    return schemes, VGroup(axes, ticks_x, ticks_y, x_name, y_name, head), points, trend, axes


class Scene26(VideoScene):
    number = 26

    def construct(self):
        schemes, frame, points, trend, axes = distance_layout(self)
        year = int(np.flatnonzero((schemes["scheme"] == "leave-one-year-out").to_numpy())[0])
        year_name = label("one year out", 24, VERMILION).next_to(points[year], UP, 0.15)
        # "Now line the schemes up by how far each held-out station is from its nearest
        # training station."
        self.play(FadeIn(frame), run_time=self.share(0.25))
        self.play(LaggedStart(*[FadeIn(p, scale=2) for p in points], lag_ratio=0.15), FadeIn(year_name),
                  run_time=self.share(0.5))
        self.finish()


def distance_labels(schemes, points):
    out = VGroup()
    for name, direction in (("random 10-fold", RIGHT), ("spatial blocks, 1.20°", UP)):
        i = int(np.flatnonzero((schemes["scheme"] == name).to_numpy())[0])
        r = schemes.iloc[i]
        text = VGroup(label(SCHEME_NAMES[name], 26, BLUE, weight=BOLD),
                      label(f"{r['nearest_km']:.0f} km: R² {r['R2']:.3f}", 30, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        text.next_to(points[i], direction, 0.3)
        out.add(text)
    return out


class Scene27(VideoScene):
    number = 27

    def construct(self):
        schemes, frame, points, trend, axes = distance_layout(self)
        self.add(frame, points)
        near, far = distance_labels(schemes, points)
        i_near = int(np.flatnonzero((schemes["scheme"] == "random 10-fold").to_numpy())[0])
        i_far = int(np.flatnonzero((schemes["scheme"] == "spatial blocks, 1.20°").to_numpy())[0])
        # "About four kilometres away, the forest scores an R² of 0.200."
        self.play(points[i_near].animate.scale(1.6), FadeIn(near), run_time=self.share(0.2))
        self.wait(max(self.share(0.5) - self.time, 0.01))
        # "Twenty-five kilometres away, 0.114."
        self.play(points[i_far].animate.scale(1.6), FadeIn(far), run_time=self.share(0.2))
        self.finish()


class Scene28(VideoScene):
    number = 28

    def construct(self):
        schemes, frame, points, trend, axes = distance_layout(self)
        labels = distance_labels(schemes, points)
        self.add(frame, points, labels)
        note = VGroup(label("no single true score:", 30, INK, weight=BOLD),
                      label("only the question you chose", 30, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.1).move_to(axes.c2p(20, 0.228))
        # "There is no single true score. Only the question you chose."
        self.play(Create(trend), run_time=self.share(0.35))
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.25))
        self.finish()


class Scene29(VideoScene):
    number = 29

    def construct(self):
        # A made-up smooth pattern of leftover error: warm and cool patches, no data.
        rng = np.random.default_rng(29)
        centres = rng.uniform([-5.5, -2.8], [0.5, 2.8], (9, 2))
        signs = rng.choice([-1, 1], 9)
        patches = VGroup()
        for i, x in enumerate(np.linspace(-6.0, 1.0, 26)):
            for y in np.linspace(-3.0, 3.0, 22):
                v = sum(s * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 1.6) for s, (cx, cy) in zip(signs, centres))
                colour = interpolate_color(ManimColor(BACKGROUND), ManimColor(VERMILION if v > 0 else BLUE),
                                           min(abs(v), 1) * 0.8)
                patches.add(Square(0.27, stroke_width=0, fill_color=colour, fill_opacity=1).move_to([x, y, 0]))
        reach = DoubleArrow([-4.3, -3.4, 0], [-2.3, -3.4, 0], buff=0, color=INK, stroke_width=4, tip_length=0.2)
        reach_name = label("how far the pattern reaches", 26, INK).next_to(reach, RIGHT, 0.2)
        small = Square(0.9, color=ORANGE, stroke_width=6).move_to([-2.5, 0.5, 0])
        big = Square(2.2, color=ORANGE, stroke_width=6).move_to([-2.5, 0.5, 0])
        text = VGroup(label("block at least", 36, INK, weight=BOLD), label("that wide", 36, INK, weight=BOLD),
                      label("chosen before you", 30, SUBDUED), label("look at the score", 30, SUBDUED)
                      ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([2.2, 0.3, 0], aligned_edge=LEFT)
        text[2].shift(0.25 * DOWN)
        text[3].shift(0.25 * DOWN)
        # "So set the block size from how far the spatial pattern reaches, ..."
        self.play(FadeIn(patches), run_time=self.share(0.2))
        self.play(GrowFromCenter(reach), FadeIn(reach_name), Create(small), run_time=self.share(0.2))
        self.play(Transform(small, big), FadeIn(text[:2]), run_time=self.share(0.25))
        # "... before you look at the score."
        self.play(FadeIn(text[2:]), run_time=self.share(0.15))
        self.finish()


class Scene30(VideoScene):
    number = 30

    def construct(self):
        forecast = self.data("forecast")
        values = [("trained on earlier years", "earlier years", VERMILION),
                  ("trained on random years, same size", "random years, same size", BLUE)]
        head = label("Predicting a year from the years before it", 34, SUBDUED).to_edge(UP, buff=0.5)
        scale = 12.0
        bars = VGroup()
        for i, (column, name, colour) in enumerate(values):
            v = forecast[column].mean()
            y = 1.0 - 1.4 * i
            bar = Rectangle(width=scale * v, height=0.8, stroke_width=0, fill_color=colour, fill_opacity=1
                            ).move_to([-3.0, y, 0], aligned_edge=LEFT)
            bars.add(VGroup(label(f"trained on {name}", 30).next_to(bar, UP, 0.12, aligned_edge=LEFT), bar,
                            label(f"R² {v:.2f}", 30, colour, weight=BOLD).next_to(bar, RIGHT, 0.25)))
        note = VGroup(label("here the simulation gave the year no effect;", 30, SUBDUED),
                      label("real seas shift, and gear changes", 30, SUBDUED)).arrange(DOWN, buff=0.1
                                                                                 ).to_edge(DOWN, buff=0.7)
        # "Here, forecasting cost nothing: the simulation gave the year no effect."
        self.play(FadeIn(head), run_time=self.share(0.1))
        self.play(*[GrowFromEdge(b[1], LEFT) for b in bars], *[FadeIn(b[0]) for b in bars], run_time=self.share(0.25))
        self.play(*[FadeIn(b[2]) for b in bars], run_time=self.share(0.1))
        self.play(FadeIn(note[0]), run_time=self.share(0.1))
        # "Real surveys, with shifting seas and changing gear, are rarely so kind."
        self.wait(max(self.share(0.55) - self.time, 0.01))
        self.play(FadeIn(note[1]), run_time=self.share(0.1))
        self.finish()


class Scene31(KeyPointScene):
    number, point = 31, 2


# Measures disagree (scenes 32–39) ----------------------------------------------------------

class Scene32(VideoScene):
    number = 32

    def construct(self):
        # Schematic: each miss drawn as a length (MAE) and as a square (RMSE).
        unit = 0.3
        head = label("A measure says which mistakes you mind", 36, INK, weight=BOLD).to_edge(UP, buff=0.3)
        one_line = Line([0, 0, 0], [10 * unit, 0, 0], color=VERMILION, stroke_width=10)
        ten_lines = VGroup(*[Line([0, 0, 0], [unit, 0, 0], color=BLUE, stroke_width=10) for _ in range(10)]
                           ).arrange(RIGHT, buff=0)
        one_name = label("one big miss", 30, VERMILION, weight=BOLD)
        ten_name = label("ten small misses", 30, BLUE, weight=BOLD)
        VGroup(one_name, one_line).arrange(DOWN, buff=0.2).move_to([-3.8, 2.3, 0])
        VGroup(ten_name, ten_lines).arrange(DOWN, buff=0.2).move_to([2.8, 2.3, 0])
        mae = label("MAE: the same total length", 30, SUBDUED).move_to([-0.5, 1.45, 0])
        big = Square(10 * unit, stroke_width=0, fill_color=VERMILION, fill_opacity=0.8
                     ).next_to(one_line, DOWN, 1.3, aligned_edge=LEFT)
        smalls = VGroup(*[Square(unit, stroke_width=0, fill_color=BLUE, fill_opacity=0.8) for _ in range(10)]
                        ).arrange(RIGHT, buff=0).next_to(ten_lines, DOWN, 1.3, aligned_edge=LEFT)
        rmse = label("RMSE: squares, so one big miss counts far more", 30, SUBDUED).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(head), run_time=self.share(0.1))
        self.play(FadeIn(one_name), Create(one_line), FadeIn(ten_name), Create(ten_lines), run_time=self.share(0.15))
        # "RMSE minds one big miss more than many small ones."
        self.play(TransformFromCopy(one_line, big), TransformFromCopy(ten_lines, smalls), run_time=self.share(0.25))
        self.play(FadeIn(rmse), run_time=self.share(0.1))
        # "MAE minds them all the same."
        self.wait(max(self.share(0.75) - self.time, 0.01))
        self.play(FadeIn(mae), Indicate(one_line), Indicate(ten_lines), run_time=self.share(0.15))
        self.finish()


class Scene33(VideoScene):
    number = 33

    def construct(self):
        errors = self.data("nb-errors")
        squared = np.sort(((errors["obs"] - errors["pred"]) ** 2).to_numpy())[::-1]
        n_worst = round(0.05 * len(squared))
        share = squared[:n_worst].sum() / squared.sum()
        width = 12.0 / len(squared)
        top = squared.max()
        bars = VGroup(*[Rectangle(width=width, height=max(4.6 * v / top, 0.005), stroke_width=0,
                                  fill_color=VERMILION if i < n_worst else BLUE, fill_opacity=1)
                        for i, v in enumerate(squared)]).arrange(RIGHT, buff=0, aligned_edge=DOWN
                                                                ).move_to([0, -1.0, 0], aligned_edge=DOWN)
        bars.move_to([0, -1.2, 0], aligned_edge=DOWN)
        base = Line(bars.get_corner(DL), bars.get_corner(DR), color=GRID, stroke_width=3)
        head = label(f"Squared error at each of {len(squared)} stations, largest first", 32, SUBDUED
                     ).to_edge(UP, buff=0.3)
        worst_name = label("the worst 5%: the tall bars at the left", 30, VERMILION, weight=BOLD
                           ).next_to(bars[0], RIGHT, 0.5).align_to(bars, UP).shift(0.4 * DOWN)
        whole = Rectangle(width=12, height=0.6, stroke_width=0).move_to([0, -2.4, 0])
        part = Rectangle(width=12 * share, height=0.6, stroke_width=0, fill_color=VERMILION, fill_opacity=1
                         ).align_to(whole, LEFT).set_y(-2.4)
        rest = Rectangle(width=12 * (1 - share), height=0.6, stroke_width=0, fill_color=BLUE, fill_opacity=1
                         ).align_to(whole, RIGHT).set_y(-2.4)
        total_name = label("all the squared error", 28, SUBDUED).next_to(whole, DOWN, 0.15)
        share_name = label(f"{percent(share)} of it", 32, BACKGROUND, weight=BOLD).move_to(part)
        self.play(FadeIn(head), Create(base), run_time=self.share(0.1))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.002), run_time=self.share(0.3))
        # "On these counts, the worst 5% of stations carry half of all the squared error."
        self.play(FadeIn(worst_name), run_time=self.share(0.1))
        self.play(GrowFromEdge(rest, RIGHT), GrowFromEdge(part, LEFT), FadeIn(total_name), run_time=self.share(0.2))
        self.play(FadeIn(share_name), run_time=self.share(0.1))
        self.finish()


class Scene34(VideoScene):
    number = 34

    def construct(self):
        errors = self.data("nb-errors")
        zero = (errors["obs"] == 0).to_numpy()
        formula = VGroup(label("percentage error", 36, INK, weight=BOLD),
                         label("=  miss  ÷  count caught", 36, INK)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        squares = VGroup(*[Square(0.15, stroke_width=0, fill_color=BLUE, fill_opacity=1) for _ in zero]
                         ).arrange_in_grid(GRID_ROWS, GRID_COLS, buff=0.05).move_to([0, 0.2, 0])
        empty = VGroup(*[s for s, z in zip(squares, zero) if z])
        empty_name = label(f"{zero.sum()} stations caught nothing: ÷ 0", 34, VERMILION, weight=BOLD
                           ).next_to(squares, DOWN, 0.5)
        self.play(FadeIn(formula), run_time=self.share(0.2))
        self.play(FadeIn(squares), run_time=self.share(0.15))
        # "... and 157 stations caught nothing."
        self.play(empty.animate.set_fill(VERMILION), FadeIn(empty_name), run_time=self.share(0.2))
        self.play(LaggedStart(*[FadeOut(s, shift=0.8 * DOWN) for s in empty], lag_ratio=0.004),
                  run_time=self.share(0.3))
        self.finish()


class Scene35(VideoScene):
    number = 35

    def construct(self):
        scaling = self.data("scaling")
        mape = scaling[scaling["measure"] == "MAPE"].sort_values("scale")
        rmse = scaling[scaling["measure"] == "RMSE"].sort_values("scale")
        top = 3.0
        axes = plain_axes([0.3, 1.6, 0.1], [1, top, 0.5], 10.0, 5.0).shift(0.4 * RIGHT + 0.2 * DOWN)
        ticks_x = VGroup(*[label(f"{v:.1f}", 24, SUBDUED).next_to(axes.c2p(v, 1), DOWN, 0.15)
                           for v in (0.4, 0.6, 0.8, 1.0, 1.2, 1.4)])
        x_name = label("multiply every prediction by", 26, SUBDUED).next_to(ticks_x, DOWN, 0.15)
        y_name = label("error, relative to its best", 26, SUBDUED).rotate(PI / 2).next_to(axes, LEFT, 0.3)
        keep = mape["relative"] <= top
        curve = polyline(axes, mape["scale"][keep], mape["relative"][keep], VERMILION, 7)
        rcurve = polyline(axes, rmse["scale"], rmse["relative"].clip(upper=top), GREY, 4)
        rname = label("RMSE", 26, GREY).next_to(axes.c2p(1.55, rmse["relative"].iloc[-1]), UP, 0.1)
        best = mape.loc[mape["relative"].idxmin()]
        dot = Dot(axes.c2p(best["scale"], 1), radius=0.14, color=VERMILION)
        best_name = label(f"lowest at {best['scale']:.2f}", 34, VERMILION, weight=BOLD).next_to(dot, UP, 0.8)
        believed = DashedLine(axes.c2p(1, 1), axes.c2p(1, top), color=INK, stroke_width=3)
        believed_name = label("what the model believes", 26, INK).next_to(believed, UP, 0.1)
        name = label("percentage error", 30, VERMILION, weight=BOLD).move_to(axes.c2p(0.6, 2.6))
        head = label("Shrink every prediction, and see what each measure prefers", 30, SUBDUED
                     ).to_edge(UP, buff=0.2)
        self.play(FadeIn(VGroup(axes, ticks_x, x_name, y_name, head)), Create(believed), FadeIn(believed_name),
                  run_time=self.share(0.15))
        self.play(Create(rcurve), FadeIn(rname), run_time=self.share(0.15))
        # "On the rest, it is lowest if you shrink every prediction to 47% ..."
        self.play(Create(curve), FadeIn(name), run_time=self.share(0.3))
        self.play(FadeIn(dot, scale=2), FadeIn(best_name), run_time=self.share(0.15))
        self.finish()


CELL_WORDS = {("yes", "yes"): "found", ("yes", "no"): "wasted dive",
              ("no", "yes"): "missed", ("no", "no"): "rightly empty"}


def confusion_layout(scene):
    table = scene.data("confusion")
    cells = {}
    for _, r in table.iterrows():
        col = 0 if r["Truth"] == "yes" else 1
        row = 0 if r["Prediction"] == "yes" else 1
        centre = np.array([-0.2 + 3.4 * col, 0.7 - 2.1 * row, 0])
        box = Rectangle(width=3.2, height=1.9, stroke_color=GRID, stroke_width=4).move_to(centre)
        text = VGroup(label(f"{r['n']}", 60, INK, weight=BOLD),
                      label(CELL_WORDS[(r["Prediction"], r["Truth"])], 28, SUBDUED)).arrange(DOWN, buff=0.1
                                                                                      ).move_to(centre)
        cells[(r["Prediction"], r["Truth"])] = VGroup(box, text)
    cols = VGroup(label("truly present", 30, SUBDUED).move_to([-0.2, 2.1, 0]),
                  label("truly absent", 30, SUBDUED).move_to([3.2, 2.1, 0]))
    rows = VGroup(label("flagged present", 30, SUBDUED).move_to([-2.0, 0.7, 0], aligned_edge=RIGHT),
                  label("flagged absent", 30, SUBDUED).move_to([-2.0, -1.4, 0], aligned_edge=RIGHT))
    return cells, VGroup(cols, rows)


class Scene36(VideoScene):
    number = 36

    def construct(self):
        cells, frame = confusion_layout(self)
        head = label("Presence or absence, at a cut-off of one half", 32, SUBDUED).to_edge(UP, buff=0.4)
        order = [("yes", "yes"), ("yes", "no"), ("no", "yes"), ("no", "no")]
        # "For presence or absence, every prediction lands in one of four boxes."
        self.play(FadeIn(head), FadeIn(frame), *[Create(cells[k][0]) for k in order], run_time=self.share(0.35))
        self.play(LaggedStart(*[FadeIn(cells[k][1], scale=0.7) for k in order], lag_ratio=0.3),
                  run_time=self.share(0.45))
        self.finish()


MEASURE_NAMES = {"accuracy": "accuracy", "sensitivity": "sensitivity", "specificity": "specificity",
                 "ppv": "precision", "npv": "negative predictive value", "f_meas": "F1",
                 "bal_accuracy": "balanced accuracy", "j_index": "Youden's J", "kap": "kappa", "mcc": "MCC"}


class Scene37(VideoScene):
    number = 37

    def construct(self):
        measures = self.data("class-measures").sort_values("value", ascending=False).reset_index(drop=True)
        head = label("Ten measures, one table of four numbers", 32, SUBDUED).to_edge(UP, buff=0.3)
        scale = 7.0
        rows = VGroup()
        for i, r in measures.iterrows():
            y = 2.75 - 0.62 * i
            name = label(MEASURE_NAMES[r["measure"]], 28).move_to([-1.6, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=max(scale * r["value"], 0.02), height=0.42, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1).move_to([-1.3, y, 0], aligned_edge=LEFT)
            value = label(f"{r['value']:.3f}", 28, INK).next_to(bar, RIGHT, 0.15)
            rows.add(VGroup(name, bar, value))
        self.play(FadeIn(head), run_time=self.share(0.1))
        # "Ten measures from those four numbers ..."
        self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT)) for r in rows],
                              lag_ratio=0.12), run_time=self.share(0.4))
        self.play(*[FadeIn(r[2]) for r in rows], run_time=self.share(0.1))
        # "... run from 0.058 to 0.995."
        for r in (rows[0], rows[-1]):
            r[2].set_color(VERMILION)
        self.play(Indicate(rows[0][2], color=VERMILION, scale_factor=1.4),
                  Indicate(rows[-1][2], color=VERMILION, scale_factor=1.4), run_time=self.share(0.2))
        self.finish()


class Scene38(VideoScene):
    number = 38

    def construct(self):
        f1 = self.data("flag-all").set_index("rule")["f1"]
        head = label("F1", 44, INK, weight=BOLD).to_edge(UP, buff=0.6)
        scale = 9.0
        rows = VGroup()
        for i, (rule, name, colour) in enumerate((("flag every station", "a rule: \"present\" everywhere", GREY),
                                                  ("logistic model", "the fitted model", BLUE))):
            y = 0.9 - 1.8 * i
            bar = Rectangle(width=scale * f1[rule], height=0.8, stroke_width=0, fill_color=colour, fill_opacity=1
                            ).move_to([-5.5, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(label(name, 30).next_to(bar, UP, 0.12, aligned_edge=LEFT), bar,
                            label(f"{f1[rule]:.3f}", 40, INK, weight=BOLD).next_to(bar, RIGHT, 0.25)))
        # "A rule that says "present" at every station scores an F1 of 0.878."
        self.play(FadeIn(head), FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), run_time=self.share(0.3))
        self.play(FadeIn(rows[0][2]), run_time=self.share(0.1))
        # "The model scores 0.882."
        self.wait(max(self.share(0.62) - self.time, 0.01))
        self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), run_time=self.share(0.2))
        self.play(FadeIn(rows[1][2]), run_time=self.share(0.1))
        self.finish()


class Scene39(VideoScene):
    number = 39

    def construct(self):
        cells, frame = confusion_layout(self)
        self.add(frame, *cells.values())
        tn = cells[("no", "no")]
        cover = Rectangle(width=3.2, height=1.9, stroke_width=0, fill_color=GREY, fill_opacity=0.75).move_to(tn)
        note = label("F1 never looks here", 34, VERMILION, weight=BOLD).next_to(tn, DOWN, 0.35)
        used = VGroup(*[cells[k][0] for k in (("yes", "yes"), ("yes", "no"), ("no", "yes"))])
        # "A measure that ignores the empty stations ..."
        self.play(Indicate(tn[1], color=VERMILION), run_time=self.share(0.25))
        self.play(FadeIn(cover), FadeIn(note), run_time=self.share(0.2))
        # "... cannot tell a model from a rule with no model in it."
        self.play(*[b.animate.set_stroke(BLUE, 6) for b in used], run_time=self.share(0.25))
        self.finish()


# The puzzle, solved (scenes 40–46) ---------------------------------------------------------

class Scene40(VideoScene):
    number = 40

    def construct(self):
        pairs = [("\"We mapped abundance across the shelf\"", "error at each station"),
                 ("\"Total abundance is about N\"", "the total, predicted against observed"),
                 ("\"These fifty stations hold the most\"", "what a shortlist of fifty finds")]
        head = VGroup(label("the sentence you want to write", 30, SUBDUED, weight=BOLD),
                      label("the measure that could prove it false", 30, SUBDUED, weight=BOLD))
        head[0].move_to([-3.6, 2.8, 0])
        head[1].move_to([3.6, 2.8, 0])
        rows = VGroup()
        for i, (sentence, measure) in enumerate(pairs):
            y = 1.4 - 1.5 * i
            left = label(sentence, 30, INK).move_to([-3.6, y, 0])
            right = label(measure, 30, BLUE, weight=BOLD).move_to([3.6, y, 0])
            arrow = Arrow(left.get_right(), right.get_left(), buff=0.2, color=GREY, stroke_width=4)
            rows.add(VGroup(left, arrow, right))
        for r in rows:
            if r.width > 13.6:
                r.scale_to_fit_width(13.6)
            r.set_x(0)
        # "So write the sentence you want to publish first."
        self.play(FadeIn(head[0]), LaggedStart(*[FadeIn(r[0], shift=0.2 * RIGHT) for r in rows], lag_ratio=0.3),
                  run_time=self.share(0.4))
        # "Then pick the measure that would prove it false."
        self.play(FadeIn(head[1]), LaggedStart(*[AnimationGroup(GrowArrow(r[1]), FadeIn(r[2])) for r in rows],
                                               lag_ratio=0.3), run_time=self.share(0.4))
        self.finish()


def objective_heads():
    return {"rmse": label("mapping every station?", 32, INK, weight=BOLD),
            "caught": label("fifty stations to revisit?", 32, INK, weight=BOLD),
            "total": label("the total stock?", 32, INK, weight=BOLD)}


class ObjectiveRows:
    """Scenes 41–43: the puzzle's layout, relabelled by objective, one row at a time.

    A mixin, not a Scene, so that `manim -a` does not try to render it on its own.
    """

    row = None

    def construct(self):
        cards, rmse, caught, total, _ = puzzle_layout(self)
        rows = {"rmse": rmse, "caught": caught, "total": total}
        heads = objective_heads()
        for key, r in rows.items():
            heads[key].move_to(r[0], aligned_edge=LEFT).shift(0.35 * UP)
            r[0].scale(0.8).next_to(heads[key], DOWN, 0.1, aligned_edge=LEFT)
        order = list(rows)
        done = order[:order.index(self.row)]
        self.add(cards, *[VGroup(heads[k], *rows[k]) for k in done])
        r = rows[self.row]
        self.play(FadeIn(heads[self.row], shift=0.2 * RIGHT), FadeIn(r[0]), run_time=self.share(0.3))
        self.play(FadeIn(r[1]), run_time=self.share(0.2))
        if self.row == "total":
            cross = Cross(r[1][1], stroke_color=VERMILION, stroke_width=6)
            self.play(Create(cross), run_time=self.share(0.2))
        else:
            self.play(FadeIn(r[2][0]), Create(r[2][1]), run_time=self.share(0.2))
        self.finish()


class Scene41(ObjectiveRows, VideoScene):
    number, row = 41, "rmse"


class Scene42(ObjectiveRows, VideoScene):
    number, row = 42, "caught"


class Scene43(ObjectiveRows, VideoScene):
    number, row = 43, "total"


class Scene44(VideoScene):
    number = 44

    def construct(self):
        pivot = Triangle(color=INK, fill_opacity=1).scale(0.45).move_to(1.6 * DOWN)
        beam = Line(4.4 * LEFT, 4.4 * RIGHT, color=INK, stroke_width=8).next_to(pivot, UP, 0)
        pans = VGroup()
        for side, text, colour in ((-1, "a wasted dive", ORANGE), (1, "a missed station", VERMILION)):
            end = beam.get_center() + side * 4.2 * RIGHT
            pan = VGroup(Line(end, end + 1.0 * DOWN, color=INK, stroke_width=4),
                         RoundedRectangle(width=3.4, height=1.0, corner_radius=0.15, stroke_color=colour,
                                          stroke_width=5).move_to(end + 1.5 * DOWN))
            pan.add(label(text, 32, colour, weight=BOLD).move_to(pan[1]))
            pans.add(pan)
        head = label("A cut-off of one half assumes", 36, INK, weight=BOLD).to_edge(UP, buff=0.8)
        equal = label("they cost the same", 40, INK, weight=BOLD).next_to(head, DOWN, 0.3)
        # "Cut-offs work the same way."
        self.play(FadeIn(pivot), Create(beam), FadeIn(pans), run_time=self.share(0.3))
        # "Using one half assumes a wasted dive costs the same as a missed station."
        self.play(FadeIn(head), run_time=self.share(0.15))
        self.play(FadeIn(equal, shift=0.2 * UP), run_time=self.share(0.2))
        self.finish()


def cost_layout(scene, top=9.0, ticks=(1, 2, 4, 8)):
    curves = scene.data("cost-curves")
    table = scene.data("cost-table").set_index("k")
    axes = plain_axes([0, 1, 0.25], [0, np.log10(top), 0.25], 10.0, 5.2).shift(0.4 * RIGHT + 0.2 * DOWN)
    to = lambda c, rel: axes.c2p(c, np.log10(rel))  # noqa: E731
    ticks_x = VGroup(*[label(f"{v:.2f}", 24, SUBDUED).next_to(axes.c2p(v, 0), DOWN, 0.15) for v in (0, 0.25, 0.5, 0.75, 1)])
    ticks_y = VGroup(*[label(f"{v}×", 24, SUBDUED).next_to(to(0, v), LEFT, 0.15) for v in ticks])
    x_name = label("cut-off: flag the station above this probability", 26, SUBDUED).next_to(ticks_x, DOWN, 0.15)
    y_name = label("cost, against the cheapest", 26, SUBDUED).rotate(PI / 2).next_to(ticks_y, LEFT, 0.2)
    half = DashedLine(to(0.5, 1), to(0.5, top), color=GREY, stroke_width=3)
    half_name = label("one half", 24, SUBDUED).next_to(half, UP, 0.1)

    def curve(k, colour):
        c = curves[curves["k"] == k].sort_values("cut_off").copy()
        c["relative"] = (c["cost"] / c["cost"].min()).clip(upper=top)
        line = VMobject(color=colour, stroke_width=7).set_points_as_corners(
            [to(x, r) for x, r in zip(c["cut_off"], c["relative"])])
        best = table.loc[k]
        dot = Dot(to(best["cheapest"], 1), radius=0.14, color=colour)
        return line, dot, best

    frame = VGroup(axes, ticks_x, ticks_y, x_name, y_name, half, half_name)
    return frame, curve, to


class Scene45(VideoScene):
    number = 45

    def construct(self):
        frame, curve, to = cost_layout(self, 2.0, (1, 1.5, 2))
        line, dot, best = curve(3, BLUE)
        head = label("A wasted dive costs three missed stations", 32, BLUE, weight=BOLD).to_edge(UP, buff=0.25)
        best_name = label(f"cheapest: {best['cheapest']:.2f}", 34, BLUE, weight=BOLD).move_to(to(best["cheapest"], 1.85))
        self.play(FadeIn(frame), run_time=self.share(0.15))
        # "If a wasted dive costs three times as much, ..."
        self.play(FadeIn(head), Create(line), run_time=self.share(0.35))
        # "... the cheapest cut-off is 0.75."
        self.play(FadeIn(dot, scale=2), FadeIn(best_name), run_time=self.share(0.2))
        self.finish()


class Scene46(VideoScene):
    number = 46

    def construct(self):
        frame, curve, to = cost_layout(self)
        line3, dot3, _ = curve(3, BLUE)
        self.add(frame, line3.set_stroke(opacity=0.3), dot3.set_opacity(0.3))
        line, dot, best = curve(30, VERMILION)
        ratio = best["cost_half"] / best["cost_there"]
        head = label("A wasted dive costs thirty missed stations", 32, VERMILION, weight=BOLD).to_edge(UP, buff=0.25)
        at_half = Dot(to(0.5, ratio), radius=0.14, color=VERMILION)
        drop = DashedLine(to(0.5, ratio), to(best["cheapest"], ratio), color=VERMILION, stroke_width=3)
        ratio_name = label(f"at one half: {ratio:.1f} × the cheapest", 34, VERMILION, weight=BOLD
                           ).move_to(to(0.03, 3.2), aligned_edge=LEFT)
        # "At thirty times, ..."
        self.play(FadeIn(head), Create(line), FadeIn(dot), run_time=self.share(0.3))
        # "... leaving it at one half costs nearly eight times as much."
        self.play(FadeIn(at_half, scale=2), Create(drop), run_time=self.share(0.2))
        self.play(FadeIn(ratio_name), run_time=self.share(0.2))
        self.finish()


class Scene47(KeyPointScene):
    number, point = 47, 3


# Quiz (scenes 48–49) -----------------------------------------------------------------------

class Scene48(QuizScene):
    number = 48
    question = ("A model predicts the same average", "at every station. Its survey total",
                "is exactly right. Is it a good model?")


class Scene49(VideoScene):
    number = 49

    def construct(self):
        objectives = self.data("objectives").set_index("model")
        bench = self.data("benchmarks").iloc[0]
        mean_only = objectives.loc["mean only"]
        answer = label("No: it has no skill at all", 44, VERMILION, weight=BOLD).to_edge(UP, buff=0.5)
        total = label(f"its survey total: {percent(mean_only['total_ratio'])} of the real one", 32, SUBDUED
                      ).next_to(answer, DOWN, 0.4)
        scale = 9.0 / max(mean_only["caught"], bench["random"]) * 0.8
        rows = VGroup()
        for i, (name, value, colour) in enumerate((("its top fifty stations", mean_only["caught"], GREY),
                                                   ("fifty stations chosen at random", bench["random"], BLUE))):
            y = -0.2 - 1.7 * i
            bar = Rectangle(width=scale * value, height=0.8, stroke_width=0, fill_color=colour, fill_opacity=1
                            ).move_to([-5.0, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(label(name, 30).next_to(bar, UP, 0.12, aligned_edge=LEFT), bar,
                            label(f"{value:.0f} animals", 36, INK, weight=BOLD).next_to(bar, RIGHT, 0.25)))
        # "No. It has no skill at all."
        self.play(FadeIn(answer), FadeIn(total), run_time=self.share(0.25))
        # "Its fifty stations hold 183 animals, about what fifty random stations would."
        for r in rows:
            self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=self.share(0.25))
        self.finish()


# The recap (scenes 50–52) and the end card (scene 53) --------------------------------------

class Scene50(RecapScene):
    number, point = 50, 1


class Scene51(RecapScene):
    number, point = 51, 2


class Scene52(RecapScene):
    number, point = 52, 3


class Scene53(EndCardScene):
    number = 53
