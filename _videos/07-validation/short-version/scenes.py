"""Manim scenes for the validation video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/07-validation
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

A short, encouraging overview for readers from any marine field, on what is new in the
section: keep a score honest, choose a score that fits the goal, and compare models in
pairs. Scenes marked "page results" read visuals/data/*.csv, which
tools/figures-for-video.R writes from the pages. The others are schematic: made-up
shapes, never numbers that could pass for survey results; the site maps use the
survey's site positions, which are data, not results. The opening, key-point, recap,
quiz and end-card scenes are shared (mlbasic_video.py) and read PROMISES, ANSWERS and
RECAP from here.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403
from mlbasic_data import load_coastal_survey_clean  # noqa: E402


class Title(TitleScene):
    pass


PROMISES = ["How to keep a score honest",
            "How to choose a score that fits your goal",
            "How to tell whether one model is really better"]
ANSWERS = ["Score the whole search,\nnot just its winner",
           "Start from what the\npredictions are for",
           "Compare the two\nin pairs"]
RECAP = ["Keep the score honest",
         "Choose a score that fits your goal",
         "Compare models in pairs"]

# The pages' colours: blue for the models, orange for anything held out or chosen, vermilion
# for a flattering score. Model names are the pages' own labels, as in the CSVs.
FOREST, POISSON, AVERAGE = "Random forest", "Poisson regression", "Predicting the average"


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


class Scene02(VideoScene):
    number = 2

    def construct(self):
        model = card("a model", BLUE, 44).move_to([0, 0.9, 0])
        score = label("its score: how well it predicts\ndata it has never seen", 32, INK).next_to(model, DOWN, 0.45)
        fields = VGroup(*[card(t, c, 32) for t, c in (("seagrass maps", GREEN), ("fish stocks", ORANGE),
                                                       ("plankton counts", PURPLE))])
        for f, p in zip(fields, ([-4.6, 2.6, 0], [4.6, 2.6, 0], [0, -2.9, 0])):
            f.move_to(p)
        trust = label("worth trusting?", 44, BLUE, weight=BOLD).move_to([4.2, -1.6, 0])
        # "Whether you map seagrass, forecast a fish stock or count plankton, ..."
        for f, phrase in zip(fields, ("map seagrass", "forecast a fish stock", "count plankton")):
            cue(self, phrase)
            self.play(FadeIn(f, scale=0.8), run_time=self.share(0.07))
        # "... a model comes with a score: how well it predicts data it has never seen."
        cue(self, "a model comes")
        self.play(FadeIn(model), run_time=self.share(0.08))
        self.play(FadeIn(score, shift=0.2 * UP), run_time=self.share(0.1))
        # "This section is about making that score worth trusting."
        cue(self, "This section")
        self.play(FadeIn(trust, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


# Keep the score honest (scenes 3–7) -------------------------------------------------------

def search_cards(scene, coloured):
    """The hundred candidates of the page's search, five columns each; random columns in grey
    once `coloured`."""
    search = scene.data("search")
    cards = VGroup()
    for _, r in search.iterrows():
        cells = VGroup(*[Square(0.13, stroke_width=0, fill_opacity=1,
                                fill_color=GREY if coloured and i < r["noise"] else BLUE) for i in range(5)])
        cards.add(cells.arrange(RIGHT, buff=0.03))
    cards.arrange_in_grid(10, 10, buff=(0.28, 0.2)).move_to([0, -0.4, 0])
    winner = int(np.flatnonzero(search["winner"].to_numpy())[0])
    return search, cards, winner


class Scene03(VideoScene):
    number = 3

    def construct(self):
        search, cards, winner = search_cards(self, False)
        head = label("a hundred models", 34, SUBDUED).to_edge(UP, buff=0.6)
        box = SurroundingRectangle(cards[winner], color=VERMILION, buff=0.08, stroke_width=5)
        best = label("best score: keep it", 32, VERMILION, weight=BOLD).next_to(cards, DOWN, 0.4)
        # "Suppose you try a hundred models ..."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(c, scale=0.6) for c in cards], lag_ratio=0.02),
                  run_time=self.share(0.35))
        # "... and keep the one with the best score."
        cue(self, "and keep the one")
        self.play(Create(box), cards[winner].animate.scale(1.5), FadeIn(best), run_time=self.share(0.15))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        axis = Line([-5.5, -1.6, 0], [5.5, -1.6, 0], color=GRID, stroke_width=3)
        lower = label("← better score", 28, SUBDUED).next_to(axis, DOWN, 0.2).align_to(axis, LEFT)
        truth = DashedLine([1.0, 2.0, 0], [1.0, -1.6, 0], color=INK, stroke_width=4)
        truth_name = label("how good the models really are", 28, INK).next_to(truth, UP, 0.15)

        def scores(n, seed):
            r = np.random.default_rng(seed)
            return VGroup(*[Dot([1.0 + r.normal(0, 0.9), -1.1 + r.uniform(-0.35, 0.35), 0], radius=0.11,
                                color=GREY, fill_opacity=0.7) for _ in range(n)])

        few, many = scores(10, 91), scores(90, 92)
        # "But every score is partly luck."
        self.play(Create(axis), FadeIn(lower), Create(truth), FadeIn(truth_name), run_time=self.share(0.15))
        self.play(LaggedStart(*[FadeIn(d, shift=(d.get_x() - 1.0) * RIGHT) for d in few], lag_ratio=0.08),
                  run_time=self.share(0.2))
        # "The best of a hundred has had the most luck, ..."
        cue(self, "The best of a hundred")
        self.play(FadeIn(many, lag_ratio=0.01), run_time=self.share(0.15))
        best = min([*few, *many], key=lambda d: d.get_x())
        arrow = Arrow([1.0, 0.3, 0], [best.get_x(), 0.3, 0], buff=0, color=VERMILION, stroke_width=6,
                      max_tip_length_to_length_ratio=0.15)
        luck = label("luck", 32, VERMILION, weight=BOLD).next_to(arrow, UP, 0.1)
        self.play(best.animate.set_color(VERMILION).scale(1.6), GrowArrow(arrow), FadeIn(luck),
                  run_time=self.share(0.15))
        # "... so its score looks better than the model really is."
        cue(self, "so its score looks")
        self.play(Indicate(truth, color=INK), run_time=self.share(0.12))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        search, plain, winner = search_cards(self, False)
        search, cards, winner = search_cards(self, True)
        self.add(plain)
        real = VGroup(*[Square(0.32, stroke_width=0, fill_color=BLUE, fill_opacity=1) for _ in range(8)]
                      ).arrange(RIGHT, buff=0.06)
        noise = VGroup(*[Square(0.32, stroke_width=0, fill_color=GREY, fill_opacity=1) for _ in range(20)]
                       ).arrange(RIGHT, buff=0.06)
        columns = VGroup(real, noise).arrange(RIGHT, buff=0.5).move_to([0, 2.7, 0])
        names = VGroup(label("measured inputs", 28, BLUE, weight=BOLD).next_to(real, UP, 0.2),
                       label("random numbers", 28, GREY, weight=BOLD).next_to(noise, UP, 0.2))
        noise_count = int(search.loc[winner, "noise"])
        cells = VGroup(*[Square(0.8, stroke_width=0, fill_opacity=1, fill_color=GREY if i < noise_count else BLUE)
                         for i in range(5)]).arrange(RIGHT, buff=0.85).move_to([0, -0.2, 0])
        cell_names = VGroup(*[label("random" if i < noise_count else "measured", 26, SUBDUED).next_to(c, DOWN, 0.15)
                              for i, c in enumerate(cells)])
        head = label("the winning model's five inputs", 34, VERMILION, weight=BOLD).next_to(cells, UP, 0.5)
        # "To see it, we hid twenty columns of pure random numbers among the inputs."
        self.play(FadeIn(real), FadeIn(names[0]), run_time=self.share(0.1))
        cue(self, "we hid twenty")
        self.play(FadeIn(noise, lag_ratio=0.05), FadeIn(names[1]), run_time=self.share(0.15))
        self.play(*[ReplacementTransform(p, c) for p, c in zip(plain, cards)], run_time=self.share(0.12))
        # "The winning model used two of them."
        cue(self, "The winning model")
        self.play(*[FadeOut(c) for i, c in enumerate(cards) if i != winner], run_time=self.share(0.08))
        self.play(ReplacementTransform(cards[winner], cells), FadeIn(head), run_time=self.share(0.12))
        self.play(FadeIn(cell_names), *[Indicate(c, color=GREY) for c in cells[:noise_count]],
                  run_time=self.share(0.12))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        blocks = VGroup(*[Rectangle(width=2.2, height=0.9, stroke_color=BACKGROUND, stroke_width=4,
                                    fill_color=BLUE, fill_opacity=1) for _ in range(5)]
                        ).arrange(RIGHT, buff=0).move_to([0, 2.0, 0])
        fold_name = label("the survey's sites, in five groups", 28, SUBDUED).next_to(blocks, UP, 0.2)
        head = label("Nested cross-validation", 40, INK, weight=BOLD).to_edge(UP, buff=0.25)
        mini = VGroup(*[Square(0.12, stroke_width=0, fill_color=GREY, fill_opacity=1) for _ in range(100)]
                      ).arrange_in_grid(10, 10, buff=0.06).move_to([-1.6, -0.9, 0])
        search_name = lines_of("the whole search,\non the other sites", 30, SUBDUED).next_to(mini, LEFT, 0.5)
        held_name = lines_of("its winner is scored here,\non sites the search\nnever saw", 30, ORANGE, BOLD, 0.2
                             ).move_to([3.6, -0.9, 0])
        # "Nested cross-validation gives an honest score."
        self.play(FadeIn(head), FadeIn(blocks), FadeIn(fold_name), run_time=self.share(0.12))
        arrow = None
        for f in range(3):
            chosen = mini[(37 * f + 11) % 100]
            new_arrow = Arrow(mini.get_right(), blocks[f].get_bottom(), buff=0.15, color=ORANGE, stroke_width=5)
            anims = [blocks[f].animate.set_fill(ORANGE)] + ([blocks[f - 1].animate.set_fill(BLUE)] if f else [])
            if f == 0:
                # "It holds some sites back, ..."
                cue(self, "It holds some sites back")
                self.play(*anims, run_time=self.share(0.06))
                # "... runs the whole search on the rest, ..."
                cue(self, "runs the whole search")
                self.play(FadeIn(mini), FadeIn(search_name), run_time=self.share(0.08))
            else:
                self.play(*anims, mini.animate.set_fill(GREY), FadeOut(arrow), run_time=self.share(0.05))
            self.play(LaggedStart(*[Indicate(s, color=INK, scale_factor=1.6) for s in mini[::9]], lag_ratio=0.05),
                      run_time=self.share(0.06))
            if f == 0:
                # "... and only then scores the winner on the sites it held back."
                cue(self, "and only then")
            self.play(chosen.animate.set_fill(VERMILION), GrowArrow(new_arrow), run_time=self.share(0.05))
            if f == 0:
                self.play(FadeIn(held_name), run_time=self.share(0.06))
            arrow = new_arrow
        self.finish()


class Scene07(VideoScene):
    number = 7

    def construct(self):
        n = self.data("nested").iloc[0]
        axis, to_x = number_line(4.2, 5.0, -5.0, 5.5, -2.2, [4.2, 4.4, 4.6, 4.8, 5.0], 1)
        axis_name = label("error on new sites (lower is better)", 28, SUBDUED).next_to(axis, DOWN, 0.15)

        def mark(value, y, colour, text, side=RIGHT, hollow=False):
            dot = Circle(0.17, color=colour, stroke_width=5).move_to([to_x(value), y, 0]) if hollow else \
                Dot([to_x(value), y, 0], radius=0.17, color=colour)
            words = VGroup(label(text, 30, colour), label(f2(value), 44, colour, weight=BOLD)
                           ).arrange(RIGHT, buff=0.3).next_to(dot, side, 0.3)
            stem = DashedLine([to_x(value), y, 0], [to_x(value), -2.2, 0], color=GRID, stroke_width=2)
            return VGroup(stem, dot, words)

        claimed = mark(n["claimed"], 1.6, GREY, "the search claimed", hollow=True)
        honest = mark(n["nested"], 0.3, VERMILION, "scored honestly", LEFT)
        plain = mark(n["eight_inputs"], -1.0, BLUE, "a plain model, no search")
        # "The search claimed an error of 4.42."
        self.play(FadeIn(axis), FadeIn(axis_name), run_time=self.share(0.1))
        self.play(FadeIn(claimed), run_time=self.share(0.12))
        # "Scored honestly, its winners managed 4.86: ..."
        cue(self, "Scored honestly")
        self.play(TransformFromCopy(claimed[1], honest[1]), FadeIn(honest[0]), FadeIn(honest[2]),
                  run_time=self.share(0.15))
        # "... worse than a plain model that skipped the search altogether."
        cue(self, "worse than a plain")
        self.play(FadeIn(plain), run_time=self.share(0.15))
        self.finish()


class Scene08(KeyPointScene):
    number = 8
    point = 1


# Choose a score that fits your goal (scenes 9–13) -----------------------------------------

class Scene09(VideoScene):
    number = 9

    def construct(self):
        def use(heading, example, colour, x):
            box = RoundedRectangle(width=4.0, height=3.2, corner_radius=0.2, stroke_color=colour,
                                   stroke_width=5).move_to([x, 0.4, 0])
            head = label(heading, 40, colour, weight=BOLD).next_to(box.get_top(), DOWN, 0.4)
            body = lines_of(example, 28, INK).next_to(head, DOWN, 0.4)
            return VGroup(box, head, body)

        uses = [use("a total", "a stock\nestimate", BLUE, -4.4),
                use("a shortlist", "sites worth\nvisiting", ORANGE, 0),
                use("a yes or no", "is the species\nthere?", GREEN, 4.4)]
        own = label("each use needs its own score", 40, INK, weight=BOLD).to_edge(DOWN, buff=0.8)
        # "Predictions are put to different uses: a total ..., a shortlist ..., or a yes or no ..."
        for u, phrase in zip(uses, ("a total", "a shortlist", "a yes or no")):
            cue(self, phrase)
            self.play(FadeIn(u, shift=0.2 * UP), run_time=self.share(0.08))
        # "Each use needs its own score."
        cue(self, "Each use")
        self.play(FadeIn(own), run_time=self.share(0.1))
        self.finish()


def ranked_bars(n=20, seed=17):
    rng = np.random.default_rng(seed)
    heights = np.sort(rng.gamma(1.6, 1.0, n))[::-1]
    heights = heights / heights.max() * 3.6
    return VGroup(*[Rectangle(width=0.4, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.6)
                    for h in heights]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


class Scene10(VideoScene):
    number = 10

    def construct(self):
        bars = ranked_bars().move_to([-0.6, -2.4, 0], aligned_edge=DOWN)
        top = VGroup(*bars[:6])
        bracket = Brace(top, UP, color=ORANGE).next_to(top, UP, 0.1)
        x_name = label("stations, ranked by the model's prediction", 28, SUBDUED).next_to(bars, DOWN, 0.3)
        budget = label("the stations the ship has time for", 30, ORANGE, weight=BOLD).next_to(bracket, UP, 0.1
                                                                                             ).shift(2.0 * RIGHT)
        boat = ship(INK, 1.3).next_to(bracket, UP, 0.7).shift(1.2 * LEFT)
        # "Take the shortlist."
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), FadeIn(x_name),
                  run_time=self.share(0.25))
        # "A ship has time to revisit 100 stations, and goes where the model predicts the most animals."
        cue(self, "A ship has time")
        self.play(FadeIn(boat, shift=0.5 * RIGHT), run_time=self.share(0.12))
        cue(self, "and goes where")
        self.play(*[b.animate.set_fill(ORANGE, opacity=0.9) for b in top], GrowFromCenter(bracket),
                  FadeIn(budget), run_time=self.share(0.15))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        lists = self.data("shortlists")
        r = lists.iloc[0]
        perfect, at_random, budget = r["perfect"], r["at_random"], int(r["budget"])
        axis, to_x = number_line(0, 1400, -5.8, 5.8, -2.0, [0, 200, 400, 600, 800, 1000, 1200, 1400], 0)
        axis_name = label(f"animals found at {budget} stations", 28, SUBDUED).next_to(axis, DOWN, 0.45)

        def bench(value, text, colour, y):
            dot = Dot([to_x(value), y, 0], radius=0.17, color=colour)
            words = VGroup(label(text, 30, colour, weight=BOLD), label(f"{value:.0f}", 36, colour, weight=BOLD)
                           ).arrange(DOWN, buff=0.05).next_to(dot, UP, 0.2)
            return VGroup(dot, words)

        rand = bench(at_random, "chosen at random", GREY, -1.2)
        best = bench(perfect, "a perfect list", INK, -1.2)
        models = VGroup(*[Dot([to_x(v), 0.9 + 0.35 * i, 0], radius=0.15, color=BLUE)
                          for i, v in enumerate(lists["animals found"])])
        models_name = label("three models' shortlists", 30, BLUE, weight=BOLD).next_to(models, LEFT, 0.3)
        ratio = lists["animals found"].mean() / at_random
        times_name = label(f"{ratio:.1f} times as many", 40, BLUE, weight=BOLD).move_to([0.6, 2.8, 0])
        planner = label("a score a survey planner can act on", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.2)
        # "The models' shortlists find 2.1 times as many animals as 100 stations picked at random."
        self.play(FadeIn(axis), FadeIn(axis_name), FadeIn(rand), run_time=self.share(0.15))
        self.play(FadeIn(models, lag_ratio=0.2), FadeIn(models_name), run_time=self.share(0.12))
        cue(self, "2.1 times")
        self.play(FadeIn(times_name, shift=0.2 * DOWN), FadeIn(best), run_time=self.share(0.15))
        # "That is a score a survey planner can act on."
        cue(self, "That is a score")
        self.play(FadeIn(planner), run_time=self.share(0.12))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        size = 3.0
        cells = VGroup(*[Square(size, stroke_color=GRID, stroke_width=4) for _ in range(4)]
                       ).arrange_in_grid(2, 2, buff=0).move_to([1.2, -0.6, 0])
        truth = VGroup(label("species there", 30, SUBDUED).next_to(cells[0], UP, 0.2),
                       label("species not there", 30, SUBDUED).next_to(cells[1], UP, 0.2))
        calls = VGroup(label("model says yes", 30, SUBDUED).next_to(cells[0], LEFT, 0.25),
                       label("model says no", 30, SUBDUED).next_to(cells[2], LEFT, 0.25))
        right = VGroup(label("right", 32, GREEN, weight=BOLD).move_to(cells[0]),
                       label("right", 32, GREEN, weight=BOLD).move_to(cells[3]))
        alarm = label("false alarm", 36, VERMILION, weight=BOLD).move_to(cells[1])
        miss = label("miss", 36, ORANGE, weight=BOLD).move_to(cells[2])
        # "A yes or no at each site can go wrong in two ways."
        self.play(Create(cells), FadeIn(truth), FadeIn(calls), run_time=self.share(0.15))
        self.play(FadeIn(right), run_time=self.share(0.1))
        # "A false alarm says the species is there when it is not."
        cue(self, "A false alarm")
        self.play(cells[1].animate.set_fill(VERMILION, opacity=0.12), FadeIn(alarm, scale=0.8),
                  run_time=self.share(0.12))
        # "A miss says it is absent when it is there."
        cue(self, "A miss says")
        self.play(cells[2].animate.set_fill(ORANGE, opacity=0.12), FadeIn(miss, scale=0.8), run_time=self.share(0.12))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        alarm = Square(1.8, stroke_width=0, fill_color=VERMILION, fill_opacity=0.8).move_to([-4.0, 1.0, 0])
        alarm_name = lines_of("a false alarm:\na wasted dive", 30, VERMILION, BOLD, 0.06).next_to(alarm, DOWN, 0.25)
        miss = Square(0.75, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8).move_to([-0.8, 0.55, 0])
        miss_name = lines_of("a miss:\na record lost", 30, ORANGE, BOLD, 0.06).next_to(miss, DOWN, 0.25)
        miss_name.align_to(alarm_name, UP)
        axis, to_x = number_line(0, 1, 1.0, 5.0, -2.4, [0, 0.5, 1], 1)
        axis_name = label("how sure the model is that the species is there", 26, SUBDUED
                          ).next_to(axis, DOWN, 0.45)
        threshold = ValueTracker(0.5)
        pointer = always_redraw(lambda: VGroup(
            Line([to_x(threshold.get_value()), -2.4, 0], [to_x(threshold.get_value()), -0.4, 0], color=INK,
                 stroke_width=6),
            label("the bar for yes", 28, INK, weight=BOLD).move_to([to_x(threshold.get_value()), -0.15, 0])))
        # "The two rarely cost the same."
        self.play(FadeIn(alarm, scale=0.6), FadeIn(alarm_name), FadeIn(miss, scale=0.6), FadeIn(miss_name),
                  run_time=self.share(0.15))
        # "If a false alarm sends a dive team out for nothing, ..."
        cue(self, "If a false alarm")
        self.play(Indicate(alarm, color=VERMILION), FadeIn(axis), FadeIn(axis_name), FadeIn(pointer),
                  run_time=self.share(0.15))
        # "... raise the bar for saying yes."
        cue(self, "raise the bar")
        self.play(threshold.animate.set_value(0.75), run_time=self.share(0.2))
        self.finish()


class Scene14(KeyPointScene):
    number = 14
    point = 2


# Is one model really better? (scenes 15–19) -----------------------------------------------

class Scene15(VideoScene):
    number = 15

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
        # "With other sites, it would have come out a little different, ..."
        cue(self, "With other sites")
        other_head = label("other sites it might have drawn", 30, GREY, weight=BOLD).move_to(head)
        current = dots
        for k, (va, vb) in enumerate(((2.9, 3.9), (3.9, 4.9), (4.1, 3.6))):
            new = other_sites()
            anims = [ReplacementTransform(current, new), a.animate.set_value(va), b.animate.set_value(vb)]
            if k == 0:
                anims.append(ReplacementTransform(head, other_head))
            # "... and two models might swap places."
            if k == 2:
                cue(self, "and two models")
            self.play(*anims, run_time=self.share(0.13))
            current = new
        self.finish()


def site_squares():
    return VGroup(*[Square(0.26, stroke_width=0, fill_color=BLUE, fill_opacity=0.85) for _ in range(160)]
                  ).arrange_in_grid(10, 16, buff=0.06)


class Scene16(VideoScene):
    number = 16

    def construct(self):
        scores = self.data("bootstrap-scores")[FOREST]
        source = site_squares().move_to([-3.6, 1.4, 0])
        source_name = label("the survey's 160 sites", 28, BLUE, weight=BOLD).next_to(source, UP, 0.15)
        target = VGroup(*[Square(0.26, stroke_color=GRID, stroke_width=1.5) for _ in range(160)]
                        ).arrange_in_grid(10, 16, buff=0.06).move_to([3.6, 1.4, 0])
        target_name = label("drawn again, some twice", 28, ORANGE, weight=BOLD).next_to(target, UP, 0.15)
        rng = np.random.default_rng(23)
        drawn = rng.integers(0, 160, 160)
        picks = VGroup(*[source[i].copy().move_to(t).set_fill(ORANGE) for i, t in zip(drawn, target)])

        axis = Line([-3.0, -2.9, 0], [3.0, -2.9, 0], color=GRID, stroke_width=3)
        axis_name = label("a model's score on each of a thousand draws", 26, SUBDUED).next_to(axis, DOWN, 0.15)
        lo, hi = scores.min(), scores.max()
        to_x = lambda v: -3.0 + (v - lo) / (hi - lo) * 6.0  # noqa: E731
        bins = np.linspace(lo, hi, 31)
        counts, _ = np.histogram(scores, bins)
        hist = VGroup(*[Rectangle(width=6.0 / 30 * 0.9, height=max(c / counts.max() * 1.6, 0.001), stroke_width=0,
                                  fill_color=ORANGE, fill_opacity=0.7
                                  ).move_to([to_x((bins[i] + bins[i + 1]) / 2), -2.9, 0], aligned_edge=DOWN)
                        for i, c in enumerate(counts)])
        # "So draw the sites again, ..."
        self.play(FadeIn(source), FadeIn(source_name), FadeIn(target), FadeIn(target_name), run_time=self.share(0.12))
        self.play(LaggedStart(*[TransformFromCopy(source[i], p) for i, p in zip(drawn, picks)], lag_ratio=0.01),
                  run_time=self.share(0.3))
        # "... a thousand times, and score the models on each draw."
        cue(self, "a thousand times")
        self.play(Create(axis), FadeIn(axis_name), LaggedStart(*[GrowFromEdge(h, DOWN) for h in hist],
                                                                lag_ratio=0.03), run_time=self.share(0.3))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        a = np.array([4.6, 3.8, 5.3, 4.2, 4.9])
        b = a - np.array([0.30, 0.25, 0.35, 0.28, 0.32])
        to_y = lambda v: -2.0 + (v - 3.4) / (5.6 - 3.4) * 4.6  # noqa: E731
        xs = np.linspace(-6.0, -2.0, 5)
        head_l = label("each model's score, draw by draw", 28, SUBDUED).move_to([-4.0, 3.2, 0])
        dots_a = VGroup(*[Dot([x, to_y(v), 0], radius=0.12, color=BLUE) for x, v in zip(xs, a)])
        dots_b = VGroup(*[Dot([x, to_y(v), 0], radius=0.12, color=ORANGE) for x, v in zip(xs, b)])
        line_a = VMobject(color=BLUE, stroke_width=4).set_points_as_corners([d.get_center() for d in dots_a])
        line_b = VMobject(color=ORANGE, stroke_width=4).set_points_as_corners([d.get_center() for d in dots_b])
        hard = label("a hard draw", 26, SUBDUED).next_to(dots_a[2], UP, 0.2)
        key = VGroup(key_row(BLUE, "model A", 26), key_row(ORANGE, "model B", 26)).arrange(RIGHT, buff=0.5
                                                                                          ).move_to([-4.0, -2.8, 0])
        axis = Line([1.0, -1.6, 0], [6.4, -1.6, 0], color=GRID, stroke_width=3)
        zero = DashedLine([5.0, 2.2, 0], [5.0, -1.6, 0], color=GREY, stroke_width=3)
        zero_name = label("no difference", 26, SUBDUED).next_to(zero, DOWN, 0.2)
        head_r = label("the difference, draw by draw", 28, SUBDUED).move_to([3.6, 3.2, 0])
        diffs = VGroup(*[Dot([5.0 - 6.0 * d, 1.6 - 0.75 * i, 0], radius=0.12, color=GREEN)
                         for i, d in enumerate(a - b)])
        links = VGroup(*[Line(p.get_center(), q.get_center(), color=GRID, stroke_width=3)
                         for p, q in zip(dots_a, dots_b)])
        steady = label("far steadier", 32, GREEN, weight=BOLD).next_to(diffs, LEFT, 0.4)
        # "On a hard draw, every model does worse."
        self.play(FadeIn(head_l), FadeIn(key), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(VGroup(p, q)) for p, q in zip(dots_a, dots_b)], lag_ratio=0.2),
                  Create(line_a), Create(line_b), run_time=self.share(0.2))
        self.play(FadeIn(hard), Indicate(VGroup(dots_a[2], dots_b[2]), color=INK), run_time=self.share(0.1))
        # "So compare two models draw by draw: ..."
        cue(self, "So compare")
        self.play(FadeIn(head_r), Create(axis), Create(zero), FadeIn(zero_name), FadeIn(links),
                  run_time=self.share(0.1))
        self.play(LaggedStart(*[TransformFromCopy(l, d) for l, d in zip(links, diffs)], lag_ratio=0.15),
                  run_time=self.share(0.15))
        # "... the difference between them is far steadier than either score."
        cue(self, "far steadier")
        self.play(FadeIn(steady), run_time=self.share(0.1))
        self.finish()


def pair_panel(scores, other, x, paired):
    lo = min(scores[FOREST].min(), scores[other].min())
    hi = max(scores[FOREST].max(), scores[other].max())
    lo, hi = np.floor(lo * 2) / 2, np.ceil(hi * 2) / 2
    side = 4.4
    to = lambda u, v: np.array([x - side / 2 + (u - lo) / (hi - lo) * side,  # noqa: E731
                                -0.3 - side / 2 + (v - lo) / (hi - lo) * side, 0])
    box = Square(side, stroke_color=GRID, stroke_width=3).move_to(to((lo + hi) / 2, (lo + hi) / 2))
    diagonal = DashedLine(to(lo, lo), to(hi, hi), color=GREY, stroke_width=3)
    dots = VGroup(*[Dot(to(u, v), radius=0.035, color=BLUE if v < u else VERMILION, fill_opacity=0.6)
                    for u, v in zip(scores[other], scores[FOREST])])
    x_name = label(f"error of {MODEL_NAMES[other]}", 26, SUBDUED).next_to(box, DOWN, 0.2)
    y_name = label("error of the random forest", 26, SUBDUED).rotate(PI / 2).next_to(box, LEFT, 0.2)
    share = paired.loc[other, "samples with the forest lower"]
    result = label(f"forest better in {pct(share)}", 36, BLUE, weight=BOLD).next_to(box, UP, 0.25)
    return VGroup(box, diagonal, x_name, y_name), dots, result


MODEL_NAMES = {AVERAGE: "predicting the average", POISSON: "Poisson regression", FOREST: "random forest"}


class Scene18(VideoScene):
    number = 18

    def construct(self):
        scores = self.data("bootstrap-scores")
        paired = self.data("paired").set_index("forest minus")
        frame, dots, result = pair_panel(scores, AVERAGE, -3.4, paired)
        key = VGroup(key_row(BLUE, "forest better", 26), key_row(VERMILION, "forest worse", 26)
                     ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([2.4, 0.5, 0])
        note = label("one dot per draw", 26, SUBDUED).next_to(key, DOWN, 0.4).align_to(key, LEFT)
        # "A random forest beats simply predicting the average in 99 per cent of the draws: ..."
        self.play(FadeIn(frame), FadeIn(key), FadeIn(note), run_time=self.share(0.15))
        self.play(FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.3))
        cue(self, "in 99 per cent")
        self.play(FadeIn(result, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "... a real difference."
        cue(self, "a real difference")
        self.play(Indicate(result, color=BLUE), run_time=self.share(0.12))
        self.finish()


class Scene19(VideoScene):
    number = 19

    def construct(self):
        scores = self.data("bootstrap-scores")
        paired = self.data("paired").set_index("forest minus")
        left = pair_panel(scores, AVERAGE, -3.4, paired)
        frame, dots, result = pair_panel(scores, POISSON, 3.4, paired)
        self.add(*left)
        undecided = label("too close to call", 34, VERMILION, weight=BOLD).move_to(frame[2])
        # "Against Poisson regression, it wins only 79 per cent of the time."
        self.play(FadeIn(frame), run_time=self.share(0.12))
        self.play(FadeIn(dots, lag_ratio=0.001), run_time=self.share(0.25))
        cue(self, "only 79")
        self.play(FadeIn(result, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "On this survey, you cannot yet tell those two apart."
        cue(self, "On this survey")
        self.play(FadeOut(frame[2]), FadeIn(undecided), run_time=self.share(0.12))
        self.finish()


class Scene20(KeyPointScene):
    number = 20
    point = 3


# Quiz (scenes 21–22) ----------------------------------------------------------------------

class Scene21(QuizScene):
    number = 21
    question = ("A false alarm costs three misses.",
                "Should the bar for yes",
                "be above 0.5, or below?")


class Scene22(VideoScene):
    number = 22

    def construct(self):
        thresholds = self.data("thresholds").set_index("k")
        curve = self.data("cost-curves")
        curve = curve[curve["k"] == 3]
        cheapest = thresholds.loc[3, "cheapest threshold"]
        rule = thresholds.loc[3, "k / (1 + k)"]
        answer = label(f"Above: {f2(rule)}", 72, GREEN, weight=BOLD).move_to([0, 3.0, 0])
        odds = label("called present only when presence is\nthree times as likely as absence", 30, INK
                     ).next_to(answer, DOWN, 0.3)
        top = float(np.ceil(curve["cost"].max() * 2) / 2)
        axes, frame = chart([0, 1, 0.25], [0, top, 0.5], 8.0, 3.4, [0, 0.25, 0.5, 0.75, 1],
                            np.arange(0, top + 1e-9, 0.5), "the bar for yes", "cost of the calls",
                            y_text=lambda v: f"{v:.1f}")
        frame.move_to([0.3, -1.7, 0])
        line = axes.plot_line_graph(curve["threshold"].to_numpy(), curve["cost"].to_numpy(), line_color=BLUE,
                                    stroke_width=5, add_vertex_dots=False)
        half = DashedLine(axes.c2p(0.5, 0), axes.c2p(0.5, top), color=GREY, stroke_width=3)
        low = curve.loc[curve["cost"].idxmin()]
        low_dot = Dot(axes.c2p(low["threshold"], low["cost"]), radius=0.14, color=GREEN)
        low_name = label(f"cheapest at {f2(cheapest)}", 28, GREEN, weight=BOLD).next_to(low_dot, DOWN, 0.3)
        head = label("logistic regression on the survey", 26, SUBDUED).next_to(frame, UP, 0.1).shift(2.5 * RIGHT)
        # "Above."
        self.play(FadeIn(answer, scale=1.3), run_time=self.share(0.1))
        # "At 0.75, a station is called present only when presence is three times as likely as absence."
        cue(self, "At 0.75")
        self.play(FadeIn(odds), run_time=self.share(0.12))
        # "That is where logistic regression's calls cost least on the survey."
        cue(self, "That is where")
        self.play(FadeIn(frame), FadeIn(head), Create(half), Create(line), run_time=self.share(0.15))
        self.play(FadeIn(low_dot, scale=2), FadeIn(low_name), run_time=self.share(0.1))
        self.finish()


# Key points and end card (scenes 23–26) ---------------------------------------------------

class Scene23(RecapScene):
    number = 23
    point = 1


class Scene24(RecapScene):
    number = 24
    point = 2


class Scene25(RecapScene):
    number = 25
    point = 3


class Scene26(EndCardScene):
    number = 26
