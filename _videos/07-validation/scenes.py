"""Manim scenes for the validation video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/07-validation
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is built on three ideas from the section, each with the reason it matters: a
score is only as honest as its folds, the measure must follow the use, and a score needs
an interval. Scenes marked "page results" read visuals/data/*.csv, which
tools/figures-for-video.R writes from the pages. The others are schematic: made-up
shapes, never numbers that could pass for survey results; the maps use the survey's
site positions, which are data, not results. The opening, key-point, recap, quiz and
end-card scenes are shared (mlbasic_video.py) and read PROMISES, ANSWERS and RECAP from
here. Consecutive scenes about one picture share a builder, so each starts where the
previous one ended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403
from mlbasic_data import load_coastal_survey_clean  # noqa: E402


class Title(TitleScene):
    pass


PROMISES = ["Why a score is only as honest as its folds",
            "Why the measure must follow the use",
            "Why a score needs an interval"]
ANSWERS = ["Hold out what the model\nwill face, and keep the\nsearch out of the score",
           "Decide what the\npredictions are for,\nthen choose the measure",
           "Resample the sites,\nand compare models\nin pairs"]
RECAP = ["A score is only as honest as its folds",
         "The measure must follow the use",
         "A score needs an interval"]

# The pages' colours: fitted data in blue, anything held out in orange, a flattering or
# misleading result in vermilion. Model names are the pages' own labels.
LIGHT = "#C9CED2"
FOREST, LOG_FOREST = "Random forest", "Random forest on log counts"
POISSON, AVERAGE = "Poisson regression", "Predicting the average"


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


def pct(value):
    return f"{100 * value:.0f}%"


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name, size=24,
          x_text=None, y_text=None):
    """Axes with tick labels and names, in the series style; returns the axes and all of it.

    Both ranges start at zero (Manim draws each axis through the other's zero); a chart
    whose values do not is drawn shifted, and x_text or y_text add the shift back.
    """
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


def number_line(lo, hi, x0, x1, y, ticks, digits=2, size=26):
    """A horizontal value axis from x0 to x1 at height y; returns it and a mapper."""
    to_x = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)  # noqa: E731
    line = Line([x0, y, 0], [x1, y, 0], color=GRID, stroke_width=3)
    marks = VGroup(*[VGroup(Line([to_x(t), y - 0.08, 0], [to_x(t), y + 0.08, 0], color=GRID,
                                 stroke_width=3),
                            label(f"{t:.{digits}f}", size, SUBDUED).move_to([to_x(t), y - 0.35, 0]))
                     for t in ticks])
    return VGroup(line, marks), to_x


def card(text, colour=PURPLE, size=40):
    words = VGroup(*[label(t, size, colour, weight=BOLD) for t in text.split("\n")]).arrange(DOWN, buff=0.15)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def key_row(colour, text, size=28):
    return VGroup(Dot(radius=0.13, color=colour), label(text, size)).arrange(RIGHT, buff=0.2)


def lines_of(text, size=32, colour=INK, weight=NORMAL, buff=0.12):
    return VGroup(*[label(t, size, colour, weight=weight) for t in text.split("\n")]
                  ).arrange(DOWN, buff=buff, aligned_edge=LEFT)


def site_map(width=6.4, height=5.6, centre=(-3.4, -0.2)):
    """The survey's 160 sites at the centre of their stations, east–west shrunk by
    cos(42°) as the pages measure distance. Returns the positions and a dot per site."""
    survey = load_coastal_survey_clean()
    sites = survey.groupby("site_id")[["longitude", "latitude"]].mean()
    x = sites["longitude"] * np.cos(np.radians(42))
    y = sites["latitude"]
    s = min(width / (x.max() - x.min()), height / (y.max() - y.min()))
    cx, cy = (x.max() + x.min()) / 2, (y.max() + y.min()) / 2
    points = np.column_stack([centre[0] + s * (x - cx), centre[1] + s * (y - cy),
                              np.zeros(len(x))])
    dots = VGroup(*[Dot(p, radius=0.07, color=BLUE) for p in points])
    return points, dots


def ship(colour=INK, scale=1.0):
    hull = Polygon([-0.6, 0, 0], [0.6, 0, 0], [0.45, -0.25, 0], [-0.45, -0.25, 0],
                   color=colour, fill_color=colour, fill_opacity=1, stroke_width=0)
    cabin = Rectangle(width=0.4, height=0.2, color=colour, fill_color=colour, fill_opacity=1,
                      stroke_width=0).next_to(hull, UP, 0).shift(0.1 * LEFT)
    mast = Line([0.15, 0, 0], [0.15, 0.55, 0], color=colour, stroke_width=4)
    return VGroup(hull, cabin, mast).scale(scale)


class Scene01(LearnScene):
    number = 1


# A score is a claim (scene 2, schematic) ---------------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        model = card("a model", BLUE, 40).move_to([-5.4, 0.6, 0])
        score = VGroup(label("its score", 30, SUBDUED),
                       label("how far its predictions land", 30, INK),
                       label("from what new sites caught", 30, INK)).arrange(DOWN, buff=0.12)
        score_box = SurroundingRectangle(score, color=INK, buff=0.3, corner_radius=0.15)
        score_card = VGroup(score_box, score).move_to([-0.6, 0.6, 0])
        rng = np.random.default_rng(2)
        future = VGroup(*[Dot([4.9 + rng.uniform(-1.0, 1.0), 0.6 + rng.uniform(-1.3, 1.3), 0], radius=0.09,
                              color=LIGHT) for _ in range(24)])
        future_name = label("sites not yet surveyed", 28, SUBDUED).next_to(future, DOWN, 0.35)
        arrow = Arrow(score_card.get_right(), future.get_left(), buff=0.25, color=ORANGE, stroke_width=6)
        claim = label("a claim about the future", 40, ORANGE, weight=BOLD).move_to([0, -2.3, 0])
        ask = label("when should you believe it?", 40, INK, weight=BOLD).next_to(claim, DOWN, 0.4)

        # "Every model in this course has been given a score: ..."
        self.play(FadeIn(model, shift=0.2 * RIGHT), run_time=self.share(0.1))
        self.play(GrowArrow(Arrow(model.get_right(), score_card.get_left(), buff=0.15, color=INK,
                                  stroke_width=6)), FadeIn(score_card), run_time=self.share(0.15))
        # "A score is a claim about the future."
        cue(self, "A score is a claim")
        self.play(FadeIn(future, lag_ratio=0.05), FadeIn(future_name), GrowArrow(arrow),
                  FadeIn(claim, shift=0.2 * UP), run_time=self.share(0.15))
        # "This video asks when to believe it."
        cue(self, "This video asks")
        self.play(FadeIn(ask, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


# Folds and their reach (scenes 3–6) --------------------------------------------------------

FOLD_COLOURS = [BLUE, ORANGE, GREEN, PURPLE, SKY]


class Scene03(VideoScene):
    number = 3

    def construct(self):
        points, dots = site_map()
        for d in dots:
            d.set_color(LIGHT)
        fold = np.random.default_rng(3).permutation(len(dots)) % 5
        head = label("Cross-validation by site", 40, INK, weight=BOLD).move_to([3.6, 2.6, 0])
        steps = VGroup(lines_of("1  deal the sites into folds", 32),
                       lines_of("2  hold out one fold;\n    fit to the others", 32),
                       lines_of("3  predict the held-out fold", 32)).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        steps.next_to(head, DOWN, 0.6).align_to(head, LEFT)
        result = lines_of("one out-of-fold prediction\nper station, from a model\nthat never saw its site",
                          32, ORANGE, BOLD).next_to(steps, DOWN, 0.6).align_to(head, LEFT)

        # "Cross-validation deals the sites into folds."
        self.play(FadeIn(dots, lag_ratio=0.005), FadeIn(head), run_time=self.share(0.1))
        self.play(*[d.animate.set_color(FOLD_COLOURS[f]) for d, f in zip(dots, fold)], FadeIn(steps[0]),
                  run_time=self.share(0.12))
        # "Each fold is held out in turn ..."
        cue(self, "Each fold is held out")
        self.play(FadeIn(steps[1]), FadeIn(steps[2]), run_time=self.share(0.08))
        for k in range(5):
            self.play(*[d.animate.set_color(ORANGE if f == k else LIGHT).scale(1.0) for d, f in zip(dots, fold)],
                      run_time=self.share(0.07))
        # "So every station gets one out-of-fold prediction, ..."
        self.play(*[d.animate.set_color(ORANGE) for d in dots], FadeIn(result, shift=0.2 * UP),
                  run_time=self.share(0.1))
        self.finish()


def reach_panel(kind, x):
    """One fold scheme, drawn as nine sites of five stations: which stations are held out,
    and the line from one held-out station to the nearest fitted one (schematic)."""
    rng = np.random.default_rng(4)
    box = RoundedRectangle(width=4.1, height=4.1, corner_radius=0.15, stroke_color=GRID,
                           stroke_width=3).move_to([x, -0.4, 0])
    centres = [np.array([x + 1.25 * (i - 1), -0.4 + 1.25 * (1 - j), 0]) for j in range(3) for i in range(3)]
    stations, held = VGroup(), []
    for s, c in enumerate(centres):
        for k in range(5):
            offset = np.array([rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), 0])
            if kind == "stations":
                out = s == 4 and k == 0
            elif kind == "sites":
                out = s == 4
            else:
                out = s in (0, 1, 3, 4)
            stations.add(Dot(c + offset, radius=0.08, color=ORANGE if out else BLUE))
            held.append(out)
    fitted = [i for i, h in enumerate(held) if not h]

    def nearest_to(i):
        here = stations[i].get_center()
        return min(fitted, key=lambda j: np.linalg.norm(stations[j].get_center() - here))

    def reach_of(i):
        return np.linalg.norm(stations[nearest_to(i)].get_center() - stations[i].get_center())

    # a station of the middle site; in a block, the held-out station furthest from any fitted one
    target = 20 if kind != "blocks" else max((i for i, h in enumerate(held) if h), key=reach_of)
    here = stations[target].get_center()
    nearest = nearest_to(target)
    reach = Line(here, stations[nearest].get_center(), color=INK, stroke_width=5)
    ring = Circle(0.17, color=INK, stroke_width=4).move_to(here)
    block = VGroup()
    if kind == "blocks":
        block = Square(2.55, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.08
                       ).move_to((centres[0] + centres[4]) / 2)
    name = label({"stations": "folds of stations", "sites": "folds of sites",
                  "blocks": "spatial blocks"}[kind], 32, INK, weight=BOLD).next_to(box, UP, 0.25)
    return VGroup(box, block, stations, name), VGroup(ring, reach)


class Scene04(VideoScene):
    number = 4

    def construct(self):
        panels = [reach_panel(k, x) for k, x in (("stations", -4.6), ("sites", 0), ("blocks", 4.6))]
        head = label("held out", 28, ORANGE, weight=BOLD)
        fitted = label("fitted", 28, BLUE, weight=BOLD)
        line_name = label("to the nearest fitted station", 28, INK)
        key = VGroup(VGroup(Dot(radius=0.1, color=ORANGE), head).arrange(RIGHT, buff=0.15),
                     VGroup(Dot(radius=0.1, color=BLUE), fitted).arrange(RIGHT, buff=0.15),
                     VGroup(Line(ORIGIN, 0.6 * RIGHT, color=INK, stroke_width=5), line_name
                            ).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.35)
        # "What a score claims depends on what the folds hold out."
        self.play(FadeIn(key), run_time=self.share(0.1))
        for (panel, reach), phrase in zip(panels, ("Folds of single stations", "Folds of sites",
                                                   "spatial blocks")):
            cue(self, phrase)
            self.play(FadeIn(panel), run_time=self.share(0.08))
            self.play(Create(reach[0]), Create(reach[1]), run_time=self.share(0.08))
        self.finish()


SCHEME_NAMES = {"Stations": "folds of stations", "Sites": "folds of sites",
                "Half-degree blocks": "half-degree blocks"}


class Scene05(VideoScene):
    number = 5

    def construct(self):
        runs, means = self.data("distance-runs"), self.data("distance")
        lo = 4.1
        top = np.ceil((runs["rmse"].max() - lo) * 10) / 10
        axes, frame = chart([0, 16, 4], [0, top, 0.1], 9.5, 5.0, [0, 4, 8, 12, 16],
                            np.arange(0, top + 1e-9, 0.1), "median distance to the nearest fitted station (km)",
                            "pooled RMSE (individuals)", y_text=lambda v: f"{v + lo:.1f}")
        frame.move_to([0.4, -0.2, 0])
        small = {s: VGroup(*[Dot(axes.c2p(r["nearest_km"], r["rmse"] - lo), radius=0.06, color=BLUE,
                                 fill_opacity=0.4) for _, r in runs[runs["folds"] == s].iterrows()])
                 for s in SCHEME_NAMES}
        big = {s: Dot(axes.c2p(r["km"], r["rmse"] - lo), radius=0.15, color=BLUE)
               for _, r in means.iterrows() for s in [r["folds"]]}
        names = {}
        for _, r in means.iterrows():
            s = r["folds"]
            names[s] = lines_of(f"{SCHEME_NAMES[s]}\n{r['km']:.0f} km, {f2(r['rmse'])}", 28, INK, BOLD, 0.06)
            names[s].next_to(big[s], UP + LEFT if s == "Half-degree blocks" else DOWN + RIGHT, 0.15)
        trend = VMobject(color=GREY, stroke_width=4).set_points_as_corners(
            [big[s].get_center() for s in SCHEME_NAMES])
        head = label("The same random forest, scored three ways", 34, SUBDUED).to_edge(UP, buff=0.35)

        # "A random forest was scored all three ways, ten times each."
        self.play(FadeIn(head), FadeIn(frame), run_time=self.share(0.12))
        self.play(*[FadeIn(small[s], lag_ratio=0.1) for s in SCHEME_NAMES], run_time=self.share(0.2))
        # "The further away its fitted data, the larger its error: ..."
        cue(self, "The further away")
        self.play(*[FadeIn(big[s], scale=1.6) for s in SCHEME_NAMES], Create(trend), run_time=self.share(0.15))
        # "... from 4.23 with folds of stations ..."
        cue(self, "from 4.23")
        self.play(FadeIn(names["Stations"]), FadeIn(names["Sites"]), run_time=self.share(0.1))
        # "... to 4.41 with blocks."
        cue(self, "to 4.41")
        self.play(FadeIn(names["Half-degree blocks"]), Indicate(big["Half-degree blocks"], color=ORANGE),
                  run_time=self.share(0.12))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        def panel(x, heading, answer, gap_side):
            box = RoundedRectangle(width=5.8, height=4.4, corner_radius=0.2, stroke_color=GRID,
                                   stroke_width=3).move_to([x, 0.1, 0])
            rng = np.random.default_rng(6 if gap_side else 7)
            dots, marks = VGroup(), VGroup()
            for _ in range(36):
                p = np.array([x + rng.uniform(-2.5, 2.5), rng.uniform(-1.4, 1.6), 0])
                if gap_side and p[0] > x + 0.2:
                    continue
                dots.add(Dot(p, radius=0.08, color=BLUE))
            if gap_side:
                area = Rectangle(width=2.5, height=3.3, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                                 fill_opacity=0.1).move_to([x + 1.4, 0.1, 0])
                marks.add(area, label("?", 60, ORANGE, weight=BOLD).move_to(area))
            else:
                for p in ([x - 1.1, 0.5, 0], [x + 0.9, -0.6, 0], [x + 0.3, 1.0, 0]):
                    marks.add(label("?", 40, ORANGE, weight=BOLD).move_to(p))
            title_ = lines_of(heading, 30, INK, BOLD, 0.06).next_to(box, UP, 0.25)
            use = label(answer, 34, ORANGE, weight=BOLD).next_to(box, DOWN, 0.3)
            return VGroup(box, dots, title_), marks, use

        gaps = panel(-3.3, "fill the gaps between\nmonitored sites", "use folds of sites", False)
        new = panel(3.3, "map an area\nnobody has surveyed", "use blocks", True)
        report = label("Report the distance with the score", 36, INK, weight=BOLD).to_edge(DOWN, buff=0.3)
        # "No distance is right in general."
        self.play(FadeIn(gaps[0]), FadeIn(new[0]), run_time=self.share(0.15))
        # "To fill the gaps between monitored sites, use folds of sites; ..."
        cue(self, "To fill the gaps")
        self.play(FadeIn(gaps[1]), run_time=self.share(0.1))
        self.play(FadeIn(gaps[2], shift=0.2 * UP), run_time=self.share(0.1))
        # "... to map an area nobody has surveyed, use blocks."
        cue(self, "to map an area")
        self.play(FadeIn(new[1]), run_time=self.share(0.1))
        self.play(FadeIn(new[2], shift=0.2 * UP), run_time=self.share(0.1))
        # "Report the distance with the score."
        cue(self, "Report the distance")
        self.play(FadeIn(report), run_time=self.share(0.1))
        self.finish()


# A search flatters its winner (scenes 7–11) ------------------------------------------------

def column_cells(n, colour, size=0.32):
    return VGroup(*[Square(size, stroke_width=0, fill_color=colour, fill_opacity=1) for _ in range(n)]
                  ).arrange(RIGHT, buff=0.06)


def search_layout(scene):
    search = scene.data("search")
    cards = VGroup()
    for _, r in search.iterrows():
        cells = VGroup(*[Square(0.13, stroke_width=0, fill_opacity=1,
                                fill_color=GREY if i < r["noise"] else BLUE) for i in range(5)])
        cards.add(cells.arrange(RIGHT, buff=0.03))
    cards.arrange_in_grid(10, 10, buff=(0.28, 0.2)).move_to([0, -1.0, 0])
    axis, to_x = number_line(4.45, 4.95, -5.5, 5.5, -1.9, [4.5, 4.6, 4.7, 4.8, 4.9], 1)
    axis_name = label("cross-validated RMSE of each model (individuals)", 28, SUBDUED
                      ).next_to(axis, DOWN, 0.1)
    rng = np.random.default_rng(8)
    dots = VGroup(*[Dot([to_x(v), -0.9 + rng.uniform(-0.5, 0.5), 0], radius=0.09,
                        color=VERMILION if w else GREY, fill_opacity=1 if w else 0.6)
                    for v, w in zip(search["rmse"], search["winner"])])
    winner = int(np.flatnonzero(search["winner"].to_numpy())[0])
    return search, cards, VGroup(axis, axis_name), dots, winner


class Scene07(VideoScene):
    number = 7

    def construct(self):
        search, cards, axis, dots, winner = search_layout(self)
        real = column_cells(8, BLUE)
        noise = column_cells(20, GREY)
        columns = VGroup(real, noise).arrange(RIGHT, buff=0.5).move_to([0, 2.6, 0])
        real_name = label("8 measured inputs", 28, BLUE, weight=BOLD).next_to(real, UP, 0.2)
        noise_name = label("20 columns of random numbers", 28, GREY, weight=BOLD).next_to(noise, UP, 0.2)
        model_name = label("100 models: Poisson regression on five columns each", 30, INK).move_to([0, 1.5, 0])
        keep = label("keep the lowest cross-validated error", 34, VERMILION, weight=BOLD).to_edge(DOWN, buff=0.4)
        # "Folds can also flatter a model they helped to choose."
        self.play(FadeIn(real), FadeIn(real_name), run_time=self.share(0.15))
        # "Add twenty columns of random numbers to the survey, ..."
        cue(self, "Add twenty columns")
        self.play(FadeIn(noise, lag_ratio=0.05), FadeIn(noise_name), run_time=self.share(0.12))
        # "... try a hundred models, each Poisson regression on five columns, ..."
        cue(self, "try a hundred")
        self.play(FadeIn(model_name), LaggedStart(*[FadeIn(c, scale=0.6) for c in cards], lag_ratio=0.02),
                  run_time=self.share(0.3))
        # "... and keep the lowest cross-validated error."
        cue(self, "and keep the lowest")
        self.play(FadeIn(keep), run_time=self.share(0.1))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        search, cards, axis, dots, winner = search_layout(self)
        self.add(cards)
        best = dots[winner]
        value = VGroup(label(f2(search["rmse"].min()), 48, VERMILION, weight=BOLD),
                       label("lowest of the 100", 28, VERMILION)).arrange(DOWN, buff=0.08
                                                                          ).next_to(best, UP, 0.7)
        noise = int(search.loc[winner, "noise"])
        cells = VGroup(*[Square(0.7, stroke_width=0, fill_opacity=1, fill_color=GREY if i < noise else BLUE)
                         for i in range(5)]).arrange(RIGHT, buff=0.85).move_to([1.6, 2.4, 0])
        names = VGroup(*[label("noise" if i < noise else "measured", 24, SUBDUED).next_to(c, DOWN, 0.12)
                         for i, c in enumerate(cells)])
        head = label("the winner's five columns", 30, VERMILION, weight=BOLD).next_to(cells, UP, 0.25)
        # "The winner scores 4.50, the lowest of the hundred."
        self.play(*[ReplacementTransform(c, d) for c, d in zip(cards, dots)], FadeIn(axis),
                  run_time=self.share(0.25))
        self.play(best.animate.scale(1.7), FadeIn(value, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "Two of its five columns are pure noise."
        cue(self, "Two of its five")
        self.play(TransformFromCopy(best, cells), FadeIn(head), run_time=self.share(0.15))
        self.play(FadeIn(names), *[Indicate(c, color=GREY) for c in cells[:noise]], run_time=self.share(0.12))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        axis = Line([-5.5, -1.6, 0], [5.5, -1.6, 0], color=GRID, stroke_width=3)
        axis_name = label("cross-validated error", 28, SUBDUED).next_to(axis, DOWN, 0.2)
        truth = DashedLine([1.0, 2.0, 0], [1.0, -1.6, 0], color=INK, stroke_width=4)
        truth_name = label("what each model would\nreally score on new sites", 26, INK).next_to(truth, UP, 0.15)
        rng = np.random.default_rng(9)

        def scores(n, seed):
            r = np.random.default_rng(seed)
            return VGroup(*[Dot([1.0 + r.normal(0, 0.9), -1.1 + r.uniform(-0.35, 0.35), 0], radius=0.11,
                                color=GREY, fill_opacity=0.7) for _ in range(n)])

        few = scores(10, 91)
        many = scores(60, 92)

        def lowest(group):
            return min(group, key=lambda d: d.get_x())

        def nudge(dot):
            arrow = Arrow([1.0, 0.3, 0], [dot.get_x(), 0.3, 0], buff=0, color=VERMILION, stroke_width=6,
                          max_tip_length_to_length_ratio=0.15)
            return VGroup(arrow, label("luck", 30, VERMILION, weight=BOLD).next_to(arrow, UP, 0.1))

        # "Every score is partly luck, ..."
        self.play(Create(axis), FadeIn(axis_name), Create(truth), FadeIn(truth_name), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d, shift=(d.get_x() - 1.0) * RIGHT) for d in few], lag_ratio=0.08),
                  run_time=self.share(0.2))
        # "... and the lowest of many scores has gathered the most."
        cue(self, "the lowest of many")
        first = lowest(few)
        n1 = nudge(first)
        self.play(first.animate.set_color(VERMILION).scale(1.5), GrowArrow(n1[0]), FadeIn(n1[1]),
                  run_time=self.share(0.12))
        # "So the more models a search tries, the more its winner's score flatters it."
        cue(self, "So the more models")
        self.play(FadeIn(many, lag_ratio=0.02), run_time=self.share(0.18))
        second = lowest(many)
        n2 = nudge(second)
        self.play(second.animate.set_color(VERMILION).scale(1.5), ReplacementTransform(n1, n2),
                  first.animate.set_color(GREY).scale(1 / 1.5), run_time=self.share(0.12))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        blocks = VGroup(*[Rectangle(width=2.2, height=0.9, stroke_color=BACKGROUND, stroke_width=4,
                                    fill_color=BLUE, fill_opacity=1) for _ in range(5)]
                        ).arrange(RIGHT, buff=0).move_to([0, 2.0, 0])
        fold_name = label("outer folds of sites", 28, SUBDUED).next_to(blocks, UP, 0.2)
        head = label("Nested cross-validation", 40, INK, weight=BOLD).to_edge(UP, buff=0.25)
        mini = VGroup(*[Square(0.12, stroke_width=0, fill_color=GREY, fill_opacity=1) for _ in range(100)]
                      ).arrange_in_grid(10, 10, buff=0.06).move_to([-1.6, -0.7, 0])
        inner = VGroup(*[Rectangle(width=0.4, height=0.25, stroke_color=BACKGROUND, stroke_width=2,
                                   fill_color=SKY, fill_opacity=1) for _ in range(4)]
                       ).arrange(RIGHT, buff=0).next_to(mini, DOWN, 0.25)
        search_name = lines_of("the whole search, on the\nother sites, with folds\nof its own", 28, SUBDUED
                               ).next_to(mini, LEFT, 0.5)
        held_name = lines_of("its choice is scored here:\nno part in choosing", 30, ORANGE, BOLD, 0.06
                             ).move_to([3.4, -1.0, 0])
        # "Nested cross-validation measures what the search is worth."
        self.play(FadeIn(head), FadeIn(blocks), FadeIn(fold_name), run_time=self.share(0.12))
        arrow = None
        for f in range(3):
            chosen = mini[(37 * f + 11) % 100]
            new_arrow = Arrow(mini.get_right(), blocks[f].get_bottom(), buff=0.15, color=ORANGE, stroke_width=5)
            anims = [blocks[f].animate.set_fill(ORANGE)] + ([blocks[f - 1].animate.set_fill(BLUE)] if f else [])
            if f == 0:
                # "An outer fold of sites is held out, the whole search runs on the other sites, ..."
                cue(self, "An outer fold")
                self.play(*anims, run_time=self.share(0.06))
                cue(self, "the whole search runs")
                self.play(FadeIn(mini), FadeIn(inner), FadeIn(search_name), run_time=self.share(0.08))
            else:
                self.play(*anims, mini.animate.set_fill(GREY), FadeOut(arrow), run_time=self.share(0.05))
            self.play(LaggedStart(*[Indicate(s, color=INK, scale_factor=1.6) for s in mini[::9]], lag_ratio=0.05),
                      Indicate(inner, color=SKY), run_time=self.share(0.07))
            if f == 0:
                # "... and its choice is scored on the outer fold, which played no part in choosing."
                cue(self, "and its choice")
            self.play(chosen.animate.set_fill(VERMILION), GrowArrow(new_arrow), run_time=self.share(0.05))
            if f == 0:
                self.play(FadeIn(held_name), run_time=self.share(0.06))
            arrow = new_arrow
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        n = self.data("nested").iloc[0]
        axis, to_x = number_line(4.2, 5.0, -5.0, 5.5, -2.2, [4.2, 4.4, 4.6, 4.8, 5.0], 1)
        axis_name = label("RMSE (individuals)", 28, SUBDUED).next_to(axis, DOWN, 0.15)
        head = label("Poisson regression, chosen by the search", 34, SUBDUED).to_edge(UP, buff=0.5)

        def mark(value, y, colour, text, hollow=False):
            dot = Circle(0.17, color=colour, stroke_width=5).move_to([to_x(value), y, 0]) if hollow else \
                Dot([to_x(value), y, 0], radius=0.17, color=colour)
            words = VGroup(label(text, 30, colour), label(f2(value), 44, colour, weight=BOLD)
                           ).arrange(RIGHT, buff=0.3).next_to(dot, RIGHT, 0.3)
            stem = DashedLine([to_x(value), y, 0], [to_x(value), -2.2, 0], color=GRID, stroke_width=2)
            return VGroup(stem, dot, words)

        claimed = mark(n["claimed"], 1.3, GREY, "the search claimed", hollow=True)
        honest = mark(n["nested"], 0.0, VERMILION, "its choices, outer folds")
        honest[2].next_to(honest[1], LEFT, 0.3)
        plain = mark(n["eight_inputs"], -1.3, BLUE, "eight measured inputs, no search")
        # "Inside each round, the search claimed an error of 4.42."
        self.play(FadeIn(head), FadeIn(axis), FadeIn(axis_name), run_time=self.share(0.12))
        self.play(FadeIn(claimed), run_time=self.share(0.12))
        # "On the outer folds, its choices scored 4.86."
        cue(self, "On the outer folds")
        self.play(TransformFromCopy(claimed[1], honest[1]), FadeIn(honest[0]), FadeIn(honest[2]),
                  run_time=self.share(0.15))
        # "Poisson regression on the eight measured inputs, with no search at all, scored 4.37."
        cue(self, "Poisson regression on")
        self.play(FadeIn(plain), run_time=self.share(0.15))
        self.finish()


class Scene12(KeyPointScene):
    number = 12
    point = 1


# The measure follows the use (scenes 13–20) ------------------------------------------------

class Scene13(VideoScene):
    number = 13

    def construct(self):
        misses = [0.5, -0.4, 0.8, -0.3, 2.4, 0.6]
        xs = np.linspace(-5.0, 0.0, len(misses))
        base = 1.4
        caught = VGroup(*[Dot([x, base + m * 0.55, 0], radius=0.12, color=INK) for x, m in zip(xs, misses)])
        predicted = VGroup(*[Line([x - 0.3, base, 0], [x + 0.3, base, 0], color=BLUE, stroke_width=6) for x in xs])
        gaps = VGroup(*[Line([x, base, 0], [x, base + m * 0.55, 0], color=VERMILION, stroke_width=5)
                        for x, m in zip(xs, misses)])
        key = VGroup(key_row(INK, "caught"), VGroup(Line(ORIGIN, 0.5 * RIGHT, color=BLUE, stroke_width=6),
                                                    label("predicted", 28)).arrange(RIGHT, buff=0.2),
                     VGroup(Line(ORIGIN, 0.5 * RIGHT, color=VERMILION, stroke_width=5), label("miss", 28)
                            ).arrange(RIGHT, buff=0.2)).arrange(RIGHT, buff=0.6).move_to([-2.5, 3.3, 0])
        squares = VGroup(*[Square(abs(m) * 0.55, stroke_width=0, fill_color=VERMILION, fill_opacity=0.6)
                           for m in misses]).arrange(RIGHT, buff=0.15, aligned_edge=DOWN).move_to([3.6, 1.6, 0])
        rmse_name = lines_of("RMSE: squares each miss,\nso a large one dominates", 30, INK, BOLD, 0.06
                             ).next_to(squares, DOWN, 0.3)
        bars = VGroup(*[Rectangle(width=abs(m) * 0.55, height=0.28, stroke_width=0, fill_color=VERMILION,
                                  fill_opacity=0.6) for m in misses]).arrange(RIGHT, buff=0.08).move_to([-2.5, -2.0, 0])
        mae_name = lines_of("MAE: adds the misses\nas they are", 30, INK, BOLD, 0.06).next_to(bars, DOWN, 0.3)
        # "A performance measure turns every miss into one number."
        self.play(FadeIn(key), FadeIn(caught), FadeIn(predicted), run_time=self.share(0.12))
        self.play(LaggedStart(*[Create(g) for g in gaps], lag_ratio=0.15), run_time=self.share(0.15))
        # "The RMSE minds large misses most."
        cue(self, "The RMSE minds")
        self.play(*[TransformFromCopy(g, s) for g, s in zip(gaps, squares)], run_time=self.share(0.15))
        self.play(FadeIn(rmse_name), Indicate(squares[4], color=VERMILION), run_time=self.share(0.1))
        # "The mean absolute error, or MAE, counts every animal missed the same."
        cue(self, "The mean absolute error")
        self.play(*[TransformFromCopy(g, b) for g, b in zip(gaps, bars)], run_time=self.share(0.15))
        self.play(FadeIn(mae_name), run_time=self.share(0.08))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        catch = self.data("catch").iloc[0]
        counts = load_coastal_survey_clean()["abundance"].clip(upper=25).value_counts().sort_index()
        counts = counts.reindex(range(26), fill_value=0)
        top = int(np.ceil(counts.max() / 50) * 50)
        axes, frame = chart([0, 26, 5], [0, top, 50], 11.0, 4.6, [0.5, 5.5, 10.5, 15.5, 20.5, 25.5],
                            range(0, top + 1, 50), "animals caught at a station", "stations",
                            x_text=lambda v: f"{v - 0.5:g}" if v < 25 else "25+")
        frame.move_to([0.3, -0.9, 0])
        bars = VGroup(*[Rectangle(width=axes.x_length / 26 * 0.85, height=max(c / top * axes.y_length, 0.001),
                                  stroke_width=0, fill_color=GREY, fill_opacity=0.7
                                  ).move_to(axes.c2p(k + 0.5, 0), aligned_edge=DOWN)
                        for k, c in counts.items()])

        def marker(value, colour, text, height, side):
            # the median's words stand above its line, clear of the y axis; the average's beside it
            line = DashedLine(axes.c2p(value + 0.5, 0), axes.c2p(value + 0.5, top * height), color=colour,
                              stroke_width=5)
            words = VGroup(label(text, 30, colour, weight=BOLD), label(f"{value:g}", 40, colour, weight=BOLD)
                           ).arrange(DOWN if side is RIGHT else RIGHT, buff=0.12).next_to(line.get_end(), side, 0.15)
            return VGroup(line, words)

        median = marker(catch["median"], GREEN, "median, for MAE", 1.2, UP)
        mean = marker(round(catch["average"], 1), BLUE, "average, for the RMSE", 1.0, RIGHT)
        # "On skewed counts, the two aim at different targets."
        self.play(FadeIn(frame), run_time=self.share(0.12))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=self.share(0.2))
        # "The RMSE is lowest when a model predicts the average catch, 3.9 animals."
        cue(self, "The RMSE is lowest")
        self.play(Create(mean[0]), FadeIn(mean[1]), run_time=self.share(0.15))
        # "MAE is lowest at the median, just 2."
        cue(self, "MAE is lowest")
        self.play(Create(median[0]), FadeIn(median[1]), run_time=self.share(0.15))
        self.finish()


MODEL_ORDER = [AVERAGE, POISSON, FOREST, LOG_FOREST]
MODEL_NAMES = {AVERAGE: "predicting the average", POISSON: "Poisson regression",
               FOREST: "random forest", LOG_FOREST: "random forest on log counts"}


def picks_layout(scene):
    measures = scene.data("measures").set_index("model").loc[MODEL_ORDER]
    ys = [1.2 - 1.0 * i for i in range(4)]
    names = VGroup(*[label(MODEL_NAMES[m], 28, INK).move_to([-1.8, y, 0], aligned_edge=RIGHT)
                     for m, y in zip(MODEL_ORDER, ys)])
    columns = {}
    for measure, x0 in (("RMSE", -1.2), ("MAE", 2.9)):
        values = measures[measure]
        lo, hi = values.min() * 0.97, values.max() * 1.01
        to_x = lambda v, lo=lo, hi=hi, x0=x0: x0 + (v - lo) / (hi - lo) * 2.8  # noqa: E731
        head = label(measure, 34, INK, weight=BOLD).move_to([x0 + 1.4, 2.3, 0])
        rows = VGroup()
        for m, y in zip(MODEL_ORDER, ys):
            dot = Dot([to_x(values[m]), y, 0], radius=0.13, color=GREY)
            value = label(f2(values[m]), 28, SUBDUED).next_to(dot, RIGHT, 0.2)
            rows.add(VGroup(Line([x0, y, 0], [x0 + 2.8, y, 0], color=GRID, stroke_width=2), dot, value))
        best = MODEL_ORDER.index(values.idxmin())
        columns[measure] = (head, rows, best)
    return measures, names, columns, ys


class Scene15(VideoScene):
    number = 15

    def construct(self):
        measures, names, columns, ys = picks_layout(self)
        lower = label("lower is better", 26, SUBDUED).to_edge(DOWN, buff=0.6)
        # "So the two measures pick different models."
        self.play(FadeIn(names), *[FadeIn(h) for h, r, b in columns.values()],
                  *[FadeIn(r) for h, r, b in columns.values()], FadeIn(lower), run_time=self.share(0.2))
        for measure, phrase, colour in (("RMSE", "The RMSE picks", BLUE), ("MAE", "MAE picks", VERMILION)):
            head, rows, best = columns[measure]
            cue(self, phrase)
            box = SurroundingRectangle(VGroup(names[best], rows[best]), color=colour, buff=0.12, corner_radius=0.1)
            self.play(rows[best][1].animate.set_color(colour).scale(1.4), rows[best][2].animate.set_color(colour),
                      Create(box), run_time=self.share(0.15))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        measures = self.data("measures").set_index("model").loc[MODEL_ORDER]
        share = measures["predicted / caught"]
        ys = [1.4 - 1.0 * i for i in range(4)]
        full = 7.0
        x0 = -1.6
        caught = DashedLine([x0 + full, 2.3, 0], [x0 + full, -2.2, 0], color=INK, stroke_width=4)
        caught_name = label("animals caught", 28, INK, weight=BOLD).next_to(caught, UP, 0.1)
        head = label("Each model's predictions, added up", 34, SUBDUED).to_edge(UP, buff=0.35)
        rows = VGroup()
        for m, y in zip(MODEL_ORDER, ys):
            colour = VERMILION if m == LOG_FOREST else GREY
            bar = Rectangle(width=full * share[m], height=0.5, stroke_width=0, fill_color=colour,
                            fill_opacity=0.85 if m == LOG_FOREST else 0.5).move_to([x0, y, 0], aligned_edge=LEFT)
            name = label(MODEL_NAMES[m], 28, INK).next_to([x0, y, 0], LEFT, 0.3)
            rows.add(VGroup(name, bar))
        log_row = rows[MODEL_ORDER.index(LOG_FOREST)]
        value = label(pct(share[LOG_FOREST]), 40, VERMILION, weight=BOLD).next_to(log_row[1], RIGHT, 0.2)
        missing = Brace(Line(log_row[1].get_right(), [x0 + full, log_row[1].get_y(), 0]), DOWN, color=VERMILION)
        missing_name = label("missed", 30, VERMILION, weight=BOLD).next_to(missing, DOWN, 0.1)
        # "Add up that forest's predictions, ..."
        self.play(FadeIn(head), Create(caught), FadeIn(caught_name), run_time=self.share(0.12))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT)) for r in rows],
                              lag_ratio=0.2), run_time=self.share(0.25))
        # "... and they reach only 69 per cent of the animals caught."
        cue(self, "and they reach only")
        self.play(FadeIn(value), run_time=self.share(0.1))
        # "For a stock estimate, MAE has picked a model that misses almost a third of them."
        cue(self, "For a stock estimate")
        self.play(GrowFromCenter(missing), FadeIn(missing_name), run_time=self.share(0.15))
        self.finish()


def ranked_bars(n=20, seed=17):
    rng = np.random.default_rng(seed)
    heights = np.sort(rng.gamma(1.6, 1.0, n))[::-1]
    heights = heights / heights.max() * 3.6
    bars = VGroup(*[Rectangle(width=0.4, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.6)
                    for h in heights]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    return bars


class Scene17(VideoScene):
    number = 17

    def construct(self):
        bars = ranked_bars().move_to([-0.6, -0.6, 0], aligned_edge=DOWN).shift(1.8 * DOWN)
        top = VGroup(*bars[:6])
        boat = ship(INK, 1.3).next_to(top, UP, 0.5)
        bracket = Brace(top, UP, color=ORANGE).next_to(top, UP, 0.1)
        x_name = label("stations, ranked by the model's prediction", 28, SUBDUED).next_to(bars, DOWN, 0.3)
        budget = label("the stations the ship has time for", 30, ORANGE, weight=BOLD).next_to(bracket, UP, 0.1
                                                                                             ).shift(2.0 * RIGHT)
        only = label("only the order matters", 40, INK, weight=BOLD).to_edge(UP, buff=0.4).shift(2.2 * RIGHT)
        # "Other uses ask other things."
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), FadeIn(x_name),
                  run_time=self.share(0.2))
        # "A ship has time to revisit 100 stations, and goes where a model predicts the most animals."
        cue(self, "A ship has time")
        self.play(*[b.animate.set_fill(ORANGE, opacity=0.9) for b in top], GrowFromCenter(bracket),
                  FadeIn(budget), run_time=self.share(0.15))
        boat.next_to(bracket, UP, 0.7).shift(1.2 * LEFT)
        self.play(FadeIn(boat, shift=0.5 * RIGHT), run_time=self.share(0.12))
        # "Only the order of the predictions matters."
        cue(self, "Only the order")
        drop = bars[0].height / 2
        self.play(FadeIn(only), *[b.animate.stretch(0.5, 1, about_edge=DOWN) for b in bars],
                  VGroup(bracket, budget, boat).animate.shift(drop * DOWN), run_time=self.share(0.15))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        lists = self.data("shortlists").set_index("model")
        r = lists.iloc[0]
        perfect, at_random, budget = r["perfect"], r["at_random"], int(r["budget"])
        axis, to_x = number_line(0, 1400, -5.8, 5.8, -2.3, [0, 200, 400, 600, 800, 1000, 1200, 1400], 0)
        axis_name = label(f"animals found at {budget} stations", 28, SUBDUED).next_to(axis, DOWN, 0.15)

        def bench(value, text, colour):
            line = Line([to_x(value), -2.3, 0], [to_x(value), -1.0, 0], color=colour, stroke_width=5)
            words = VGroup(label(text, 28, colour, weight=BOLD), label(f"{value:.0f}", 36, colour, weight=BOLD)
                           ).arrange(DOWN, buff=0.05).next_to(line, UP, 0.1)
            return VGroup(line, words)

        rand = bench(at_random, "random", GREY)
        best = bench(perfect, "perfect", INK)
        rows = VGroup()
        for i, m in enumerate([POISSON, FOREST, LOG_FOREST]):
            y = 2.2 - 0.85 * i
            colour = VERMILION if m == LOG_FOREST else BLUE
            dot = Dot([to_x(lists.loc[m, "animals found"]), y, 0], radius=0.15, color=colour)
            name = label(f"{MODEL_NAMES[m]}  {lists.loc[m, 'animals found']:.0f}", 28, colour, weight=BOLD
                         ).next_to(dot, LEFT, 0.25)
            rows.add(VGroup(dot, name))
        ratio = lists["animals found"].mean() / at_random
        times = label(f"{ratio:.1f} times random", 36, BLUE, weight=BOLD).move_to([to_x(at_random) + 0.3, -1.65, 0],
                                                                                  aligned_edge=LEFT)
        # "The forest on log counts finds 847 animals, as many as the other models."
        self.play(FadeIn(axis), FadeIn(axis_name), run_time=self.share(0.1))
        self.play(FadeIn(rows[2], scale=1.3), run_time=self.share(0.12))
        cue(self, "as many as")
        self.play(FadeIn(rows[0]), FadeIn(rows[1]), run_time=self.share(0.12))
        # "Each shortlist finds 2.1 times what a hundred random stations would."
        cue(self, "Each shortlist")
        self.play(FadeIn(rand), FadeIn(best), run_time=self.share(0.12))
        self.play(FadeIn(times, shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "Predictions that run low lose nothing here."
        cue(self, "Predictions that run low")
        self.play(Indicate(rows[2], color=VERMILION), run_time=self.share(0.12))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        size = 3.0
        cells = VGroup(*[Square(size, stroke_color=GRID, stroke_width=4) for _ in range(4)]
                       ).arrange_in_grid(2, 2, buff=0).move_to([1.2, -0.5, 0])
        truth = VGroup(label("species present", 28, SUBDUED).next_to(cells[0], UP, 0.2),
                       label("species absent", 28, SUBDUED).next_to(cells[1], UP, 0.2))
        calls = VGroup(label("called present", 30, SUBDUED).next_to(cells[0], LEFT, 0.25),
                       label("called absent", 30, SUBDUED).next_to(cells[2], LEFT, 0.25))
        right = VGroup(label("right", 32, GREEN, weight=BOLD).move_to(cells[0]),
                       label("right", 32, GREEN, weight=BOLD).move_to(cells[3]))
        alarm = label("false alarm", 36, VERMILION, weight=BOLD).move_to(cells[1])
        miss = label("miss", 36, ORANGE, weight=BOLD).move_to(cells[2])
        # "Calls of present or absent need something else."
        self.play(Create(cells), FadeIn(truth), FadeIn(calls), run_time=self.share(0.15))
        self.play(FadeIn(right), run_time=self.share(0.1))
        # "A false alarm is a station called present where the species is absent."
        cue(self, "A false alarm")
        self.play(cells[1].animate.set_fill(VERMILION, opacity=0.12), FadeIn(alarm, scale=0.8),
                  run_time=self.share(0.12))
        # "A miss is a station called absent where it is present."
        cue(self, "A miss is")
        self.play(cells[2].animate.set_fill(ORANGE, opacity=0.12), FadeIn(miss, scale=0.8), run_time=self.share(0.12))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        alarm = VGroup(Square(1.8, stroke_width=0, fill_color=VERMILION, fill_opacity=0.8),
                       ).move_to([-4.0, 1.0, 0])
        alarm_name = lines_of("a false alarm:\na wasted dive", 30, VERMILION, BOLD, 0.06).next_to(alarm, DOWN, 0.25)
        miss = Square(0.75, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8).move_to([-0.8, 0.55, 0])
        miss_name = lines_of("a miss:\na record lost", 30, ORANGE, BOLD, 0.06).next_to(miss, DOWN, 0.25)
        miss_name.align_to(alarm_name, UP)
        axis, to_x = number_line(0, 1, 1.0, 5.0, -2.4, [0, 0.5, 1], 1)
        axis_name = label("probability of presence", 28, SUBDUED).next_to(axis, DOWN, 0.45)
        threshold = ValueTracker(0.5)
        pointer = always_redraw(lambda: VGroup(
            Line([to_x(threshold.get_value()), -2.4, 0], [to_x(threshold.get_value()), -0.4, 0], color=INK,
                 stroke_width=6),
            label("threshold", 28, INK, weight=BOLD).move_to([to_x(threshold.get_value()), -0.15, 0]),
            label("called present", 26, BLUE).next_to([to_x(threshold.get_value()), -1.8, 0], RIGHT, 0.15)))
        # "If a false alarm wastes a dive, it may cost far more than a miss."
        self.play(FadeIn(alarm, scale=0.6), FadeIn(alarm_name), run_time=self.share(0.15))
        cue(self, "it may cost far more")
        self.play(FadeIn(miss, scale=0.6), FadeIn(miss_name), run_time=self.share(0.12))
        # "Then the threshold for calling a station present should come from those costs, ..."
        cue(self, "Then the threshold")
        self.play(FadeIn(axis), FadeIn(axis_name), FadeIn(pointer), run_time=self.share(0.12))
        # "... not sit at 0.5."
        cue(self, "not sit at")
        self.play(threshold.animate.set_value(0.7), run_time=self.share(0.15))
        self.finish()


class Scene21(KeyPointScene):
    number = 21
    point = 2


# A score needs an interval (scenes 22–27) --------------------------------------------------

class Scene22(VideoScene):
    number = 22

    def construct(self):
        points, dots = site_map(width=6.0, height=5.4, centre=(-3.6, -0.3))
        head = label("the survey's sites", 30, BLUE, weight=BOLD).next_to(dots, UP, 0.2)
        lo, hi = points[:, :2].min(axis=0), points[:, :2].max(axis=0)
        axis = Line([1.6, -2.4, 0], [6.4, -2.4, 0], color=GRID, stroke_width=3)
        axis_name = label("score", 28, SUBDUED).next_to(axis, DOWN, 0.2)
        a, b = ValueTracker(3.4), ValueTracker(4.4)
        mark_a = always_redraw(lambda: Dot([a.get_value(), -1.6, 0], radius=0.16, color=BLUE))
        mark_b = always_redraw(lambda: Dot([b.get_value(), -0.9, 0], radius=0.16, color=ORANGE))
        key = VGroup(key_row(BLUE, "model A"), key_row(ORANGE, "model B")).arrange(DOWN, buff=0.2,
                                                                                 aligned_edge=LEFT).move_to([4.0, 1.6, 0])
        rng = np.random.default_rng(22)

        def other_sites():
            return VGroup(*[Dot([rng.uniform(lo[0], hi[0]), rng.uniform(lo[1], hi[1]), 0], radius=0.07, color=GREY)
                            for _ in range(len(points))])

        # "A score comes from one survey."
        self.play(FadeIn(dots, lag_ratio=0.005), FadeIn(head), run_time=self.share(0.15))
        self.play(Create(axis), FadeIn(axis_name), FadeIn(mark_a), FadeIn(mark_b), FadeIn(key),
                  run_time=self.share(0.12))
        # "Had other sites been sampled, it would have come out higher or lower, ..."
        cue(self, "Had other sites")
        other_head = label("other sites it might have drawn", 30, GREY, weight=BOLD).move_to(head)
        current = dots
        for k, (va, vb) in enumerate(((2.4, 3.6), (4.6, 5.8), (3.8, 3.1))):
            new = other_sites()
            anims = [ReplacementTransform(current, new), a.animate.set_value(va), b.animate.set_value(vb)]
            if k == 0:
                anims.append(ReplacementTransform(head, other_head))
            # "... and two models might have swapped places."
            if k == 2:
                cue(self, "and two models")
            self.play(*anims, run_time=self.share(0.13))
            current = new
        self.finish()


def site_squares():
    return VGroup(*[Square(0.26, stroke_width=0, fill_color=BLUE, fill_opacity=0.85) for _ in range(160)]
                  ).arrange_in_grid(10, 16, buff=0.06)


class Scene23(VideoScene):
    number = 23

    def construct(self):
        scores = self.data("bootstrap-scores")[FOREST]
        source = site_squares().move_to([-3.6, 1.6, 0])
        source_name = label("the 160 sites", 28, BLUE, weight=BOLD).next_to(source, UP, 0.15)
        target = VGroup(*[Square(0.26, stroke_color=GRID, stroke_width=1.5) for _ in range(160)]
                        ).arrange_in_grid(10, 16, buff=0.06).move_to([3.6, 1.6, 0])
        target_name = label("one resample", 28, ORANGE, weight=BOLD).next_to(target, UP, 0.15)
        rng = np.random.default_rng(23)
        drawn = rng.integers(0, 160, 160)
        times = np.bincount(drawn, minlength=160)
        picks = VGroup(*[source[i].copy().move_to(t).set_fill(ORANGE) for i, t in zip(drawn, target)])
        twice = VGroup(*[s.copy().set_fill(VERMILION, opacity=1) for s, n in zip(source, times) if n > 1])
        never = VGroup(*[s.copy().set_fill(LIGHT, opacity=1) for s, n in zip(source, times) if n == 0])
        note = VGroup(key_row(VERMILION, "drawn twice or more", 26), key_row(LIGHT, "not drawn", 26)
                      ).arrange(RIGHT, buff=0.6).next_to(source, DOWN, 0.25)

        axis = Line([-3.0, -2.9, 0], [3.0, -2.9, 0], color=GRID, stroke_width=3)
        axis_name = label("the error in each resample", 26, SUBDUED).next_to(axis, DOWN, 0.15)
        lo, hi = scores.min(), scores.max()
        to_x = lambda v: -3.0 + (v - lo) / (hi - lo) * 6.0  # noqa: E731
        bins = np.linspace(lo, hi, 31)
        counts, _ = np.histogram(scores, bins)
        hist = VGroup(*[Rectangle(width=6.0 / 30 * 0.9, height=max(c / counts.max() * 1.6, 0.001), stroke_width=0,
                                  fill_color=ORANGE, fill_opacity=0.7
                                  ).move_to([to_x((bins[i] + bins[i + 1]) / 2), -2.9, 0], aligned_edge=DOWN)
                        for i, c in enumerate(counts)])
        first = Dot([to_x(scores.iloc[0]), -2.75, 0], radius=0.1, color=ORANGE)
        # "To see how far, resample the sites."
        self.play(FadeIn(source), FadeIn(source_name), run_time=self.share(0.1))
        # "Draw the 160 sites again, with replacement, ..."
        cue(self, "Draw the 160")
        self.play(FadeIn(target), FadeIn(target_name), run_time=self.share(0.06))
        self.play(LaggedStart(*[TransformFromCopy(source[i], p) for i, p in zip(drawn, picks)], lag_ratio=0.01),
                  run_time=self.share(0.2))
        self.play(FadeIn(twice), FadeIn(never), FadeIn(note), run_time=self.share(0.08))
        # "... keep their stations' out-of-fold predictions, and work out the error."
        cue(self, "and work out the error")
        self.play(Create(axis), FadeIn(axis_name), FadeIn(first, scale=2), run_time=self.share(0.1))
        # "Do it a thousand times."
        cue(self, "Do it a thousand")
        self.play(FadeOut(first), LaggedStart(*[GrowFromEdge(h, DOWN) for h in hist], lag_ratio=0.03),
                  run_time=self.share(0.15))
        self.finish()


class Scene24(VideoScene):
    number = 24

    def construct(self):
        iv = self.data("intervals").set_index("model")
        order = [FOREST, POISSON, AVERAGE]
        axis, to_x = number_line(3.5, 5.75, -3.0, 6.2, -2.4, [3.5, 4.0, 4.5, 5.0, 5.5], 1)
        axis_name = label("RMSE on new sites (individuals)", 28, SUBDUED).next_to(axis, DOWN, 0.15)
        rows = VGroup()
        for i, m in enumerate(order):
            y = 1.3 - 1.1 * i
            colour = BLUE if m == FOREST else GREY
            bar = Line([to_x(iv.loc[m, "lower"]), y, 0], [to_x(iv.loc[m, "upper"]), y, 0], color=colour,
                       stroke_width=14, stroke_opacity=0.6)
            dot = Dot([to_x(iv.loc[m, "RMSE"]), y, 0], radius=0.15, color=colour)
            name = label(MODEL_NAMES[m], 28, INK).next_to([-3.2, y, 0], LEFT, 0.1)
            rows.add(VGroup(name, bar, dot))
        ends = VGroup(label(f2(iv.loc[FOREST, "lower"]), 30, BLUE, weight=BOLD).next_to(rows[0][1], UP, 0.15
                                                                                         ).align_to(rows[0][1], LEFT),
                      label(f2(iv.loc[FOREST, "upper"]), 30, BLUE, weight=BOLD).next_to(rows[0][1], UP, 0.15
                                                                                         ).align_to(rows[0][1], RIGHT))
        shared_lo = max(iv.loc[m, "lower"] for m in order)
        shared_hi = min(iv.loc[m, "upper"] for m in order)
        overlap = Rectangle(width=to_x(shared_hi) - to_x(shared_lo), height=3.6, stroke_width=0, fill_color=ORANGE,
                            fill_opacity=0.15).move_to([(to_x(shared_lo) + to_x(shared_hi)) / 2, 0.2, 0])
        overlap_name = label("all three overlap", 28, ORANGE, weight=BOLD).next_to(overlap, UP, 0.1)
        head = label("95% intervals from the thousand resamples", 32, SUBDUED).to_edge(UP, buff=0.3)
        # "The middle 95 per cent of those errors is an interval."
        self.play(FadeIn(head), FadeIn(axis), FadeIn(axis_name), run_time=self.share(0.1))
        # "For the random forest it runs from 3.75 to 4.94, ..."
        cue(self, "For the random forest")
        self.play(FadeIn(rows[0][0]), FadeIn(rows[0][2]), GrowFromCenter(rows[0][1]), run_time=self.share(0.1))
        self.play(FadeIn(ends), run_time=self.share(0.08))
        # "... and all three models' intervals overlap."
        cue(self, "and all three")
        self.play(*[AnimationGroup(FadeIn(r[0]), FadeIn(r[2]), GrowFromCenter(r[1])) for r in rows[1:]],
                  run_time=self.share(0.12))
        self.play(FadeIn(overlap), FadeIn(overlap_name), run_time=self.share(0.08))
        # "Read alone, they cannot even say whether the forest beats predicting the average."
        cue(self, "Read alone")
        self.play(Indicate(rows[0][1], color=BLUE), Indicate(rows[2][1], color=GREY), run_time=self.share(0.15))
        self.finish()


class Scene25(VideoScene):
    number = 25

    def construct(self):
        a = np.array([4.6, 3.8, 5.3, 4.2, 4.9])
        b = a - np.array([0.30, 0.25, 0.35, 0.28, 0.32])
        to_y = lambda v: -2.0 + (v - 3.4) / (5.6 - 3.4) * 4.6  # noqa: E731
        xs = np.linspace(-6.0, -2.0, 5)
        head_l = label("each model's error, by resample", 28, SUBDUED).move_to([-4.0, 3.2, 0])
        dots_a = VGroup(*[Dot([x, to_y(v), 0], radius=0.12, color=BLUE) for x, v in zip(xs, a)])
        dots_b = VGroup(*[Dot([x, to_y(v), 0], radius=0.12, color=ORANGE) for x, v in zip(xs, b)])
        line_a = VMobject(color=BLUE, stroke_width=4).set_points_as_corners([d.get_center() for d in dots_a])
        line_b = VMobject(color=ORANGE, stroke_width=4).set_points_as_corners([d.get_center() for d in dots_b])
        key = VGroup(key_row(BLUE, "model A", 26), key_row(ORANGE, "model B", 26)).arrange(RIGHT, buff=0.5
                                                                                          ).move_to([-4.0, -2.8, 0])
        axis = Line([1.0, -1.6, 0], [6.4, -1.6, 0], color=GRID, stroke_width=3)
        zero = DashedLine([5.0, 2.2, 0], [5.0, -1.6, 0], color=GREY, stroke_width=3)
        zero_name = label("no difference", 26, SUBDUED).next_to(zero, DOWN, 0.15).shift(0.05 * DOWN)
        head_r = label("B minus A, in each resample", 28, SUBDUED).move_to([3.6, 3.2, 0])
        diffs = VGroup(*[Dot([5.0 - 6.0 * d, 1.6 - 0.75 * i, 0], radius=0.12, color=GREEN)
                         for i, d in enumerate(a - b)])
        links = VGroup(*[Line(p.get_center(), q.get_center(), color=GRID, stroke_width=3)
                         for p, q in zip(dots_a, dots_b)])
        # "But a hard sample is hard for every model, so their errors rise and fall together."
        self.play(FadeIn(head_l), FadeIn(key), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(VGroup(p, q)) for p, q in zip(dots_a, dots_b)], lag_ratio=0.2),
                  run_time=self.share(0.2))
        cue(self, "rise and fall together")
        self.play(Create(line_a), Create(line_b), run_time=self.share(0.12))
        # "Compare them in pairs: take the difference within each sample, and what they share cancels."
        cue(self, "Compare them in pairs")
        self.play(FadeIn(head_r), Create(axis), Create(zero), FadeIn(zero_name), FadeIn(links),
                  run_time=self.share(0.1))
        self.play(LaggedStart(*[TransformFromCopy(l, d) for l, d in zip(links, diffs)], lag_ratio=0.15),
                  run_time=self.share(0.2))
        self.finish()


def pair_panel(scores, other, x, paired):
    lo = min(scores[FOREST].min(), scores[other].min())
    hi = max(scores[FOREST].max(), scores[other].max())
    lo, hi = np.floor(lo * 2) / 2, np.ceil(hi * 2) / 2
    side = 4.0
    to = lambda u, v: np.array([x - side / 2 + (u - lo) / (hi - lo) * side,  # noqa: E731
                                -0.1 - side / 2 + (v - lo) / (hi - lo) * side, 0])
    box = Square(side, stroke_color=GRID, stroke_width=3).move_to(to((lo + hi) / 2, (lo + hi) / 2))
    diagonal = DashedLine(to(lo, lo), to(hi, hi), color=GREY, stroke_width=3)
    dots = VGroup(*[Dot(to(u, v), radius=0.035, color=BLUE if v < u else VERMILION, fill_opacity=0.6)
                    for u, v in zip(scores[other], scores[FOREST])])
    x_name = label(f"RMSE of {MODEL_NAMES[other]}", 26, SUBDUED).next_to(box, DOWN, 0.2)
    y_name = label("RMSE of the forest", 26, SUBDUED).rotate(PI / 2).next_to(box, LEFT, 0.2)
    share = paired.loc[other, "samples with the forest lower"]
    result = label(f"forest lower in {pct(share)}", 34, BLUE, weight=BOLD).next_to(box, UP, 0.25)
    return VGroup(box, diagonal, x_name, y_name), dots, result


class Scene26(VideoScene):
    number = 26

    def construct(self):
        scores = self.data("bootstrap-scores")
        paired = self.data("paired").set_index("forest minus")
        frame, dots, result = pair_panel(scores, AVERAGE, -3.4, paired)
        key = VGroup(key_row(BLUE, "forest lower", 26), key_row(VERMILION, "forest higher", 26)
                     ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([2.2, 0.5, 0])
        note = label("one dot per resample", 26, SUBDUED).next_to(key, DOWN, 0.4).align_to(key, LEFT)
        # "In pairs, the forest beats predicting the average in 99 per cent of the samples."
        self.play(FadeIn(frame), FadeIn(key), FadeIn(note), run_time=self.share(0.15))
        self.play(FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.3))
        cue(self, "in 99 per cent")
        self.play(FadeIn(result, shift=0.2 * DOWN), run_time=self.share(0.15))
        self.finish()


class Scene27(VideoScene):
    number = 27

    def construct(self):
        scores = self.data("bootstrap-scores")
        paired = self.data("paired").set_index("forest minus")
        left = pair_panel(scores, AVERAGE, -3.4, paired)
        frame, dots, result = pair_panel(scores, POISSON, 3.4, paired)
        self.add(*left)
        p = paired.loc[POISSON]
        axis, to_x = number_line(-0.4, 0.2, 1.4, 5.4, -3.3, [-0.4, -0.2, 0, 0.2], 1, 22)
        bar = Line([to_x(p["lower"]), -3.05, 0], [to_x(p["upper"]), -3.05, 0], color=VERMILION, stroke_width=12)
        zero = DashedLine([to_x(0), -2.8, 0], [to_x(0), -3.3, 0], color=INK, stroke_width=4)
        interval_name = label("paired interval, forest minus Poisson", 24, VERMILION, weight=BOLD
                              ).next_to(axis, LEFT, 0.2)
        # "Against Poisson regression, it wins in only 79 per cent, ..."
        self.play(FadeIn(frame), run_time=self.share(0.12))
        self.play(FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.2))
        cue(self, "in only 79")
        self.play(FadeIn(result, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "... and the paired interval covers zero."
        cue(self, "and the paired interval")
        self.play(FadeIn(axis), FadeIn(interval_name), GrowFromCenter(bar), Create(zero), run_time=self.share(0.12))
        # "On this survey, the RMSE cannot tell those two apart."
        cue(self, "On this survey")
        self.play(Indicate(zero, color=VERMILION), run_time=self.share(0.12))
        self.finish()


class Scene28(KeyPointScene):
    number = 28
    point = 3


# Quiz (scenes 29–30) ----------------------------------------------------------------------

class Scene29(QuizScene):
    number = 29
    question = ("A false alarm costs three misses.",
                "The probabilities can be trusted.",
                "Where should the threshold be?")


class Scene30(VideoScene):
    number = 30

    def construct(self):
        thresholds = self.data("thresholds").set_index("k")
        curve = self.data("cost-curves")
        curve = curve[curve["k"] == 3]
        cheapest = thresholds.loc[3, "cheapest threshold"]
        rule = thresholds.loc[3, "k / (1 + k)"]
        answer = label(f2(rule), 80, GREEN, weight=BOLD).move_to([0, 3.1, 0])

        # Left: the two expected costs for one station, worked from the quiz's ratio.
        axes, frame = chart([0, 1, 0.25], [0, 3, 1], 5.0, 3.6, [0, 0.5, 1], [0, 1, 2, 3],
                            "probability of presence, p", "expected cost (misses)")
        frame.move_to([-3.6, -0.6, 0])
        present = axes.plot(lambda p: 3 * (1 - p), color=VERMILION, stroke_width=6)  # k = 3, from the quiz
        absent = axes.plot(lambda p: p, color=ORANGE, stroke_width=6)
        present_name = label("call present: 3 × (1 − p)", 26, VERMILION, weight=BOLD
                             ).next_to(axes.c2p(0.12, 3), RIGHT, 0.1)
        absent_name = label("call absent: p", 26, ORANGE, weight=BOLD).next_to(axes.c2p(1, 1), UP, 0.15
                                                                                 ).shift(0.4 * LEFT)
        cross = Dot(axes.c2p(rule, rule), radius=0.13, color=GREEN)
        cross_line = DashedLine(axes.c2p(rule, rule), axes.c2p(rule, 0), color=GREEN, stroke_width=4)

        # Right: logistic regression's expected cost at every threshold, from the page.
        top = float(np.ceil(curve["cost"].max() * 2) / 2)
        axes2, frame2 = chart([0, 1, 0.25], [0, top, 0.5], 5.0, 3.6, [0, 0.5, 1], np.arange(0, top + 1e-9, 0.5),
                              "threshold", "expected cost per station", y_text=lambda v: f"{v:.1f}")
        frame2.move_to([3.8, -0.6, 0])
        line = axes2.plot_line_graph(curve["threshold"].to_numpy(), curve["cost"].to_numpy(), line_color=BLUE,
                                     stroke_width=5, add_vertex_dots=False)
        low = curve.loc[curve["cost"].idxmin()]
        low_dot = Dot(axes2.c2p(low["threshold"], low["cost"]), radius=0.13, color=GREEN)
        low_name = label(f"cheapest at {f2(cheapest)}", 28, GREEN, weight=BOLD).next_to(low_dot, DOWN, 0.3)
        head2 = label("logistic regression on the survey", 26, SUBDUED).next_to(frame2, UP, 0.2)

        # "0.75."
        self.play(FadeIn(answer, scale=1.3), run_time=self.share(0.08))
        # "At probability p, calling a station present risks a false alarm: three times one minus p."
        self.play(FadeIn(frame), run_time=self.share(0.08))
        cue(self, "calling a station present")
        self.play(Create(present), FadeIn(present_name), run_time=self.share(0.12))
        # "Calling it absent risks a miss: p."
        cue(self, "Calling it absent")
        self.play(Create(absent), FadeIn(absent_name), run_time=self.share(0.1))
        # "The two match at 0.75, ..."
        cue(self, "The two match")
        self.play(FadeIn(cross, scale=2), Create(cross_line), run_time=self.share(0.08))
        # "... where logistic regression's calls were cheapest on the survey."
        cue(self, "where logistic")
        self.play(FadeIn(frame2), FadeIn(head2), Create(line), run_time=self.share(0.12))
        self.play(FadeIn(low_dot, scale=2), FadeIn(low_name), run_time=self.share(0.08))
        self.finish()


# Key points and end card (scenes 31–34) ---------------------------------------------------

class Scene31(RecapScene):
    number = 31
    point = 1


class Scene32(RecapScene):
    number = 32
    point = 2


class Scene33(RecapScene):
    number = 33
    point = 3


class Scene34(EndCardScene):
    number = 34
