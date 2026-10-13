"""Manim scenes for the validation video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/07-validation
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

An introduction with one new concept per part, each on one example and one picture:
test on new places (folds of stations against blocks of the map), look beyond accuracy
(sensitivity and specificity on the Assumptions video's rare species, and the threshold
trading one for the other), and put an interval on a score (resampling the sites). Scenes marked "page
results" read visuals/data/*.csv, which tools/figures-for-video.R writes from the pages.
The others are schematic: made-up shapes, never numbers that could pass for survey
results; the maps use the survey's site positions, which are data, not results. The
opening, key-point, recap, quiz and end-card scenes are shared (mlbasic_video.py) and
read PROMISES, ANSWERS and RECAP from here. Consecutive scenes about one picture share a
builder, so each starts where the previous one ended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403
from mlbasic_data import load_coastal_survey_clean  # noqa: E402


class Title(TitleScene):
    pass


PROMISES = ["Test on new places",
            "Look beyond accuracy",
            "Put an interval on a score"]
ANSWERS = ["To map new areas,\nhold out whole areas",
           "Report sensitivity\nand specificity,\nnot accuracy alone",
           "Resample the sites\nto see how far\nit could move"]
RECAP = PROMISES

# The pages' colours: training data in blue, anything held out in orange, a flattering or
# misleading result in vermilion. Model names are the pages' own labels.
LIGHT = "#C9CED2"
FOREST, LINEAR, AVERAGE = "Random forest", "Linear regression", "Predicting the average"
MODEL_NAMES = {AVERAGE: "predicting the average", LINEAR: "linear regression", FOREST: "random forest"}


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


class Scene01(LearnScene):
    number = 1

    def setup(self):
        super().setup()
        self.times = tuple(position(self, p) for p in
                           ("testing a model", "looking beyond", "and putting an interval"))


# Test on new places (scenes 2–6) ---------------------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        model = card("a model", BLUE, 40).move_to([-5.4, 0.6, 0])
        score = VGroup(label("its score", 30, SUBDUED),
                       label("how far its predictions land", 30, INK),
                       label("from data it was not fitted to", 30, INK)).arrange(DOWN, buff=0.12)
        score_box = SurroundingRectangle(score, color=INK, buff=0.3, corner_radius=0.15)
        score_card = VGroup(score_box, score).move_to([-0.6, 0.6, 0])
        rng = np.random.default_rng(2)
        future = VGroup(*[Dot([4.9 + rng.uniform(-1.0, 1.0), 0.6 + rng.uniform(-1.3, 1.3), 0], radius=0.09,
                              color=LIGHT) for _ in range(24)])
        future_name = label("places not yet surveyed", 28, SUBDUED).next_to(future, DOWN, 0.35)
        arrow = Arrow(score_card.get_right(), future.get_left(), buff=0.25, color=ORANGE, stroke_width=6)
        promise = label("a promise about new places", 40, ORANGE, weight=BOLD).move_to([0, -2.3, 0])
        advice = label("so test on data as new as those places", 36, INK, weight=BOLD).next_to(promise, DOWN, 0.4)

        # "First, testing on new places."
        self.play(FadeIn(model, shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "A model's score says how far its predictions land from data it was not fitted to."
        cue(self, "A model's score")
        self.play(GrowArrow(Arrow(model.get_right(), score_card.get_left(), buff=0.15, color=INK,
                                  stroke_width=6)), FadeIn(score_card), run_time=self.share(0.12))
        # "It is a promise about new places: ..."
        cue(self, "It is a promise")
        self.play(FadeIn(future, lag_ratio=0.05), FadeIn(future_name), GrowArrow(arrow),
                  FadeIn(promise, shift=0.2 * UP), run_time=self.share(0.15))
        # "So the test data should be as new as those places."
        cue(self, "So the test data")
        self.play(FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        # Schematic: seven sites, each visited five times; four visits held out on their own.
        centres = [(-5.3, 1.7), (-2.9, 2.1), (-0.7, 1.5), (-4.5, -0.6), (-2.0, -0.2), (-3.4, -2.4), (-0.6, -2.0)]
        held_in = {0: 1, 2: 3, 4: 0, 5: 2}       # site: which of its visits is held out
        sites, held, kept, rings = VGroup(), VGroup(), VGroup(), VGroup()
        for s, (x, y) in enumerate(centres):
            visits = VGroup(*[Dot([x + 0.38 * np.cos(a), y + 0.38 * np.sin(a), 0], radius=0.11, color=LIGHT)
                              for a in np.linspace(0, 2 * PI, 5, endpoint=False) + PI / 2])
            sites.add(visits)
            rings.add(Circle(0.7, color=GRID, stroke_width=3).move_to([x, y, 0]))
            for k, d in enumerate(visits):
                (held if held_in.get(s) == k else kept).add(d)
        one_site = label("one site, visited five times", 26, SUBDUED).next_to(rings[1], UP, 0.12)
        key = VGroup(key_row(ORANGE, "a held-out station"), key_row(BLUE, "in the training data")
                     ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.6, 1.6, 0])
        seen = lines_of("its own site is still\nin the training data", 32, INK, BOLD, 0.08
                        ).next_to(key, DOWN, 0.8).align_to(key, LEFT)
        already = lines_of("the model has already\nseen that place", 34, VERMILION, BOLD, 0.08
                           ).next_to(seen, DOWN, 0.5).align_to(key, LEFT)

        # "Say the test holds out single stations."
        self.play(FadeIn(sites, lag_ratio=0.02), run_time=self.share(0.1))
        self.play(*[d.animate.set_color(ORANGE).scale(1.3) for d in held], FadeIn(key[0]), run_time=self.share(0.08))
        # "Most sites in the survey were visited several times, ..."
        cue(self, "Most sites")
        self.play(Create(rings), FadeIn(one_site), run_time=self.share(0.1))
        # "... so a held-out station's own site, visited at other times, is usually still in the
        # training data."
        cue(self, "so a held-out")
        self.play(*[d.animate.set_color(BLUE) for d in kept], FadeIn(key[1]), FadeIn(seen), run_time=self.share(0.12))
        # "The model has, in effect, already seen that place."
        cue(self, "The model has")
        self.play(FadeIn(already, shift=0.2 * UP), *[Indicate(rings[s], color=VERMILION) for s in held_in],
                  run_time=self.share(0.12))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        points, dots = site_map(width=6.0, height=5.6, centre=(-3.4, -0.2))
        for d in dots:
            d.set_color(LIGHT)
        lo, hi = points[:, :2].min(axis=0) - 0.25, points[:, :2].max(axis=0) + 0.25
        n = 4
        xs, ys = np.linspace(lo[0], hi[0], n + 1), np.linspace(lo[1], hi[1], n + 1)
        grid = VGroup(*[Line([x, lo[1], 0], [x, hi[1], 0], color=GRID, stroke_width=3) for x in xs],
                      *[Line([lo[0], y, 0], [hi[0], y, 0], color=GRID, stroke_width=3) for y in ys])
        cell = np.minimum(((points[:, :2] - lo) / (hi - lo) * n).astype(int), n - 1)
        ids = cell[:, 0] * n + cell[:, 1]
        block = np.bincount(ids, minlength=n * n).argmax()      # the square with the most sites
        bx, by = divmod(block, n)
        square = Rectangle(width=xs[1] - xs[0], height=ys[1] - ys[0], stroke_color=ORANGE, stroke_width=5,
                           fill_color=ORANGE, fill_opacity=0.15).move_to([(xs[bx] + xs[bx + 1]) / 2,
                                                                        (ys[by] + ys[by + 1]) / 2, 0])
        inside = VGroup(*[d for d, i in zip(dots, ids) if i == block])
        outside = VGroup(*[d for d, i in zip(dots, ids) if i != block])
        held = lines_of("a block held out:\nevery site in it", 34, ORANGE, BOLD, 0.08).move_to([3.4, 1.4, 0])
        never = lines_of("an area the model\nhas never seen", 34, INK, BOLD, 0.08
                         ).next_to(held, DOWN, 0.7).align_to(held, LEFT)
        like = lines_of("like a map of\nnew areas", 34, BLUE, BOLD, 0.08).next_to(never, DOWN, 0.7).align_to(held, LEFT)

        # "Now hold out a whole block of the map instead: ..."
        self.play(FadeIn(dots, lag_ratio=0.005), run_time=self.share(0.1))
        cue(self, "a whole block")
        self.play(Create(grid), run_time=self.share(0.1))
        # "... a square, with every site in it."
        cue(self, "a square, with")
        self.play(FadeIn(square), *[d.animate.set_color(ORANGE).scale(1.3) for d in inside],
                  *[d.animate.set_color(BLUE) for d in outside], FadeIn(held), run_time=self.share(0.12))
        # "The model must predict an area it has never seen, ..."
        cue(self, "The model must")
        self.play(FadeIn(never), run_time=self.share(0.1))
        # "... just as a map of new areas would ask of it."
        cue(self, "just as a map")
        self.play(FadeIn(like), run_time=self.share(0.1))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        km = self.data("distance").set_index("folds")["km"]
        to_w = lambda v: v / 14 * 8.0  # noqa: E731
        x0 = -3.0
        rows = {}
        for key, name, y, colour in (("Stations", "holding out\nsingle stations", 1.0, VERMILION),
                                     ("Half-degree blocks", "holding out\nblocks of the map", -0.8, ORANGE)):
            bar = Rectangle(width=to_w(km[key]), height=0.7, stroke_width=0, fill_color=colour, fill_opacity=0.85
                            ).move_to([x0, y, 0], aligned_edge=LEFT)
            value = label(f"{km[key]:.0f} km", 40, colour, weight=BOLD).next_to(bar, RIGHT, 0.25)
            words = lines_of(name, 30, INK, NORMAL, 0.06).move_to([x0 - 0.4, y, 0], aligned_edge=RIGHT)
            rows[key] = VGroup(words, bar, value)
        head = label("from a held-out station to the nearest training station", 34, SUBDUED).to_edge(UP, buff=0.6)
        times = plated(label(f"{km['Half-degree blocks'] / km['Stations']:.0f} times as far", 36, INK, weight=BOLD)
                       ).move_to([2.0, -2.6, 0])
        stations, blocks = rows["Stations"], rows["Half-degree blocks"]
        # "The difference shows in distance."
        self.play(FadeIn(head), run_time=self.share(0.1))
        # "Holding out single stations, the nearest station in the training data is typically about
        # 4 kilometres away."
        cue(self, "Holding out single")
        self.play(FadeIn(stations[0]), GrowFromEdge(stations[1], LEFT), run_time=self.share(0.12))
        cue(self, "about 4")
        self.play(FadeIn(stations[2]), run_time=self.share(0.06))
        # "Holding out blocks, it is about 13 kilometres."
        cue(self, "Holding out blocks")
        self.play(FadeIn(blocks[0]), GrowFromEdge(blocks[1], LEFT), run_time=self.share(0.12))
        self.play(FadeIn(blocks[2]), run_time=self.share(0.06))
        # "The model has to reach three times as far."
        cue(self, "The model has to")
        self.play(FadeIn(times, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def two_tests(scene):
    """The same random forest's pooled RMSE, held-out stations against held-out blocks."""
    means = scene.data("distance").set_index("folds")["rmse"]
    axis, to_x = number_line(4.1, 4.5, -2.0, 5.6, -1.6, [4.1, 4.2, 4.3, 4.4, 4.5], 1)
    axis_name = label("the forest's error on the held-out data", 26, SUBDUED).next_to(axis, DOWN, 0.6)
    rows = {}
    for key, name, y, colour in (("Stations", "holding out\nsingle stations", 1.4, VERMILION),
                                 ("Half-degree blocks", "holding out\nblocks of the map", 0.0, ORANGE)):
        dot = Dot([to_x(means[key]), y, 0], radius=0.17, color=colour)
        guide = DashedLine([to_x(means[key]), y, 0], [to_x(means[key]), -1.6, 0], color=GRID, stroke_width=2)
        value = label(f2(means[key]), 36, colour, weight=BOLD).next_to(dot, RIGHT, 0.25)
        words = lines_of(name, 30, INK, NORMAL, 0.06).move_to([-2.4, y, 0], aligned_edge=RIGHT)
        rows[key] = VGroup(words, guide, dot, value)
    head = label("One random forest, two tests", 36, SUBDUED).to_edge(UP, buff=0.5)
    return means, VGroup(axis, axis_name), rows, head, to_x


class Scene06(VideoScene):
    number = 6

    def construct(self):
        means, axis, rows, head, to_x = two_tests(self)
        stations, blocks = rows["Stations"], rows["Half-degree blocks"]
        arrow = Arrow(stations[2].get_center(), blocks[2].get_center(), buff=0.2, color=INK, stroke_width=5)
        same = plated(label("same model, harder test", 30, INK, weight=BOLD)).move_to([2.2, -0.8, 0])
        advice = label("test a model the way it will be used", 38, ORANGE, weight=BOLD).to_edge(DOWN, buff=0.35)
        # "Here is one random forest, scored both ways."
        self.play(FadeIn(head), FadeIn(axis), run_time=self.share(0.1))
        # "Holding out single stations, its error is 4.23."
        cue(self, "Holding out single")
        self.play(FadeIn(stations[0]), Create(stations[1]), FadeIn(stations[2], scale=1.5), FadeIn(stations[3]),
                  run_time=self.share(0.1))
        # "Holding out blocks, it is 4.41."
        cue(self, "Holding out blocks")
        self.play(FadeIn(blocks[0]), Create(blocks[1]), FadeIn(blocks[2], scale=1.5), FadeIn(blocks[3]),
                  run_time=self.share(0.1))
        # "The model is the same; only the test is harder."
        cue(self, "The model is the same")
        self.play(GrowArrow(arrow), FadeIn(same), run_time=self.share(0.1))
        # "So test a model the way it will be used."
        cue(self, "So test a model")
        self.play(FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene07(KeyPointScene):
    number = 7
    point = 1


# Look beyond accuracy (scenes 8–12) --------------------------------------------------------

def rare_grid(scene):
    """The Assumptions video's training stations as dots, the rare species picked out, laid
    out as that video lays them out, so the viewer sees the same picture again."""
    rare = scene.data("rare").iloc[0]
    n, present = int(rare["stations"]), int(rare["present"])
    dots = VGroup(*[Dot(radius=0.065, color=LIGHT) for _ in range(n)]).arrange_in_grid(cols=26, buff=0.09)
    dots.move_to(3.2 * LEFT + 0.3 * DOWN)
    picks = np.random.default_rng(3).choice(n, present, replace=False)
    lit = VGroup(*[dots[k] for k in picks])
    others = VGroup(*[d for k, d in enumerate(dots) if k not in set(picks)])
    for d in lit:
        d.set_color(VERMILION).scale(1.4)
    return dots, lit, others


def model_calls(scene, lit, others):
    """Squares on the stations the model called present, scaled from the page's five repeats
    to one grid, placed as in the Assumptions video: a few on presences, the rest on absences.
    Returns the squares on presences, the squares on absences, and the presences missed."""
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
    square = lambda d: Square(0.3, color=INK, stroke_width=4).move_to(d)  # noqa: E731
    missed = VGroup(*[d for d in lit if all(d is not h for h in hits)])
    return VGroup(*[square(d) for d in hits]), VGroup(*[square(d) for d in picked]), missed


def rare_layout(scene):
    matched = scene.data("matched").iloc[0]
    dots, lit, others = rare_grid(scene)
    on_presences, on_absences, missed = model_calls(scene, lit, others)
    called = VGroup(Square(0.3, color=INK, stroke_width=4), label("called present by the model", 28)
                    ).arrange(RIGHT, buff=0.2)
    key = VGroup(key_row(VERMILION, "species present"), called
                 ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(dots, UP, 0.45, aligned_edge=LEFT)

    def measure(name, meaning, value, colour, y):
        """The name and its meaning in one column, the value in a second, so the longest
        meaning never runs into its number."""
        names = VGroup(label(name, 34, colour, weight=BOLD), label(meaning, 26, SUBDUED)
                       ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([1.2, y, 0], aligned_edge=LEFT)
        number = label(value, 56, colour, weight=BOLD).move_to([4.9, y, 0], aligned_edge=LEFT)
        return VGroup(names, number)

    accuracy = measure("accuracy", "calls that are right", f"{100 * matched['accuracy']:.0f}%", GREEN, 2.2)
    sensitivity = measure("sensitivity", "presences found", f"1 in {round(1 / matched['sensitivity'])}",
                          VERMILION, 0.4)
    specificity = measure("specificity", "absences called absent", f"{100 * matched['specificity']:.0f}%",
                          BLUE, -1.4)
    return dict(dots=dots, lit=lit, others=others, key=key, on_presences=on_presences, on_absences=on_absences,
                missed=missed, accuracy=accuracy, sensitivity=sensitivity, specificity=specificity)


class Scene08(VideoScene):
    number = 8

    def construct(self):
        r = rare_layout(self)
        question = lines_of("we need measures\nthat see them", 36, INK, BOLD, 0.08).move_to([3.4, -0.6, 0])
        # "Next, looking beyond accuracy. Remember the rare species from the Assumptions and
        # limitations video."
        self.play(FadeIn(r["dots"], lag_ratio=0.001), FadeIn(r["key"][0]), run_time=self.share(0.12))
        # "A model was 92 per cent accurate, ..."
        cue(self, "A model was")
        self.play(FadeIn(r["key"][1]), LaggedStart(*[Create(c) for c in [*r["on_presences"], *r["on_absences"]]],
                                                  lag_ratio=0.05), run_time=self.share(0.1))
        cue(self, "92 per cent")
        self.play(FadeIn(r["accuracy"]), run_time=self.share(0.06))
        # "... yet found only one presence in six. Accuracy hid the misses."
        cue(self, "yet found only")
        self.play(Indicate(r["missed"], color=VERMILION, scale_factor=1.5), run_time=self.share(0.1))
        # "So we need measures that see them."
        cue(self, "So we need")
        self.play(FadeIn(question, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        r = rare_layout(self)
        self.add(r["dots"], r["key"], r["on_presences"], r["on_absences"], r["accuracy"])
        rings = VGroup(*[Circle(0.17, color=VERMILION, stroke_width=4).move_to(d) for d in r["lit"]])
        misses = label("counts the misses", 28, VERMILION, weight=BOLD).next_to(r["sensitivity"], DOWN, 0.2
                                                                             ).align_to(r["sensitivity"], LEFT)
        # "The share of the presences a model finds ..."
        self.play(Create(rings), run_time=self.share(0.15))
        # "... is called its sensitivity. Here it is one in six."
        cue(self, "is called its sensitivity")
        self.play(FadeIn(r["sensitivity"]), run_time=self.share(0.1))
        # "Sensitivity counts the misses."
        cue(self, "Sensitivity counts")
        self.play(FadeIn(misses), Indicate(r["missed"], color=VERMILION, scale_factor=1.5), run_time=self.share(0.12))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        r = rare_layout(self)
        self.add(r["dots"], r["key"], r["on_presences"], r["on_absences"], r["accuracy"], r["sensitivity"])
        alarms = label("counts the false alarms", 28, BLUE, weight=BOLD).next_to(r["specificity"], DOWN, 0.2
                                                                                 ).align_to(r["specificity"], LEFT)
        mostly = plated(lines_of("so few presences:\naccuracy is almost all specificity", 28, INK, BOLD, 0.06)
                        ).move_to([1.2, -3.2, 0], aligned_edge=LEFT)
        # "The share of the absences it calls absent ..."
        self.play(Indicate(r["others"], color=BLUE, scale_factor=1.0), run_time=self.share(0.12))
        # "... is called its specificity. Here it is 96 per cent."
        cue(self, "is called its specificity")
        self.play(FadeIn(r["specificity"]), run_time=self.share(0.1))
        # "Specificity counts the false alarms."
        cue(self, "Specificity counts")
        self.play(FadeIn(alarms), Indicate(r["on_absences"], color=BLUE), run_time=self.share(0.1))
        # "With so few presences, accuracy is almost all specificity, which is why it looked so good."
        cue(self, "With so few")
        self.play(FadeIn(mostly, shift=0.2 * UP), Indicate(r["accuracy"][1], color=GREEN),
                  Indicate(r["specificity"][1], color=BLUE), run_time=self.share(0.12))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        now, lower = self.data("matched").iloc[0], self.data("lower").iloc[0]
        rows = (("sensitivity", "sensitivity", VERMILION, 1.2), ("specificity", "specificity", BLUE, -0.3),
                ("accuracy", "accuracy", GREEN, -1.8))
        columns = ((now, -2.2), (lower, 2.6))
        names = VGroup(*[label(name, 34, colour, weight=BOLD).move_to([-2.7, y, 0], aligned_edge=RIGHT)
                         for _, name, colour, y in rows])
        heads, cells = VGroup(), []
        for at_threshold, x in columns:
            heads.add(label(f"threshold {at_threshold['threshold']:.2f}", 32, SUBDUED, weight=BOLD
                            ).move_to([x + 1.6, 2.6, 0]))
            column = VGroup()
            for key, _, colour, y in rows:
                v = at_threshold[key]
                bar = Rectangle(width=max(3.2 * v, 0.02), height=0.55, stroke_width=0, fill_color=colour,
                                fill_opacity=0.85).move_to([x, y, 0], aligned_edge=LEFT)
                text = f"1 in {round(1 / v)}" if key == "sensitivity" and v < 0.5 else pct(v)
                column.add(VGroup(bar, label(text, 32, colour, weight=BOLD).next_to(bar, RIGHT, 0.15)))
            cells.append(column)
        backdrop = Rectangle(width=4.6, height=4.6, stroke_width=0, fill_color=LIGHT, fill_opacity=0.25
                             ).move_to([2.6 + 2.0, -0.3, 0])
        lesson = label("finds far more, yet accuracy falls", 34, INK, weight=BOLD).to_edge(DOWN, buff=0.4)
        # "The model calls a station present when its probability passes a threshold."
        self.play(FadeIn(names), FadeIn(heads[0]), *[GrowFromEdge(c[0], LEFT) for c in cells[0]],
                  *[FadeIn(c[1]) for c in cells[0]], run_time=self.share(0.15))
        # "Lower that threshold, and it finds nearly three presences in four."
        cue(self, "Lower that")
        self.play(FadeIn(backdrop), FadeIn(heads[1]), run_time=self.share(0.06))
        cue(self, "and it finds")
        self.play(GrowFromEdge(cells[1][0][0], LEFT), FadeIn(cells[1][0][1]), run_time=self.share(0.1))
        # "But it raises more false alarms too: specificity falls to 71 per cent."
        cue(self, "specificity falls")
        self.play(GrowFromEdge(cells[1][1][0], LEFT), FadeIn(cells[1][1][1]), run_time=self.share(0.1))
        # "Accuracy falls with it, to 71 per cent, though the model now finds far more of the species."
        cue(self, "Accuracy falls")
        self.play(GrowFromEdge(cells[1][2][0], LEFT), FadeIn(cells[1][2][1]), run_time=self.share(0.1))
        cue(self, "though the model")
        self.play(FadeIn(lesson, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        heading = title("The cost of each mistake", 44).to_edge(UP, buff=0.5)

        def mistake(colour, name, counted, x):
            square = Square(1.6, stroke_width=0, fill_color=colour, fill_opacity=0.8).move_to([x, 0.9, 0])
            words = lines_of(name, 32, colour, BOLD, 0.06).next_to(square, DOWN, 0.3)
            by = label(counted, 26, SUBDUED).next_to(words, DOWN, 0.15)
            return VGroup(square, words, by)

        miss = mistake(ORANGE, "a miss:\na record lost", "counted by sensitivity", -3.2)
        alarm = mistake(VERMILION, "a false alarm:\na wasted dive", "counted by specificity", 3.2)
        species = label("a protected species", 28, INK, weight=BOLD).next_to(miss[0], UP, 0.2)
        dives = label("a survey with costly dives", 28, INK, weight=BOLD).next_to(alarm[0], UP, 0.2)
        advice = label("start from the use of the predictions, then choose the measure", 31, BLUE,
                       weight=BOLD).to_edge(DOWN, buff=0.5)
        # "So the threshold trades one kind of mistake for the other, and the right trade depends
        # on their costs."
        self.play(FadeIn(heading, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "For a protected species, a miss means a record lost."
        cue(self, "For a protected")
        self.play(FadeIn(species), FadeIn(miss[0], scale=0.6), FadeIn(miss[1]), FadeIn(miss[2]),
                  run_time=self.share(0.12))
        # "For a survey with costly dives, a false alarm means a wasted dive."
        cue(self, "For a survey")
        self.play(FadeIn(dives), FadeIn(alarm[0], scale=0.6), FadeIn(alarm[1]), FadeIn(alarm[2]),
                  run_time=self.share(0.12))
        # "So start from the use of the predictions, then choose the measure."
        cue(self, "So start from")
        self.play(FadeIn(advice, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene13(KeyPointScene):
    number = 13
    point = 2


# Put an interval on a score (scenes 14–17) -------------------------------------------------

class Scene14(VideoScene):
    number = 14

    def construct(self):
        forest = self.data("intervals").set_index("model").loc[FOREST, "RMSE"]
        others = self.data("bootstrap-scores")[FOREST].iloc[1:4].to_numpy()   # three resampled scores
        points, dots = site_map(width=6.0, height=5.4, centre=(-3.6, -0.3))
        head = label("the survey's sites", 30, BLUE, weight=BOLD).next_to(dots, UP, 0.2)
        lo, hi = points[:, :2].min(axis=0), points[:, :2].max(axis=0)
        score_name = label("the forest's error", 30, SUBDUED).move_to([3.6, 1.2, 0])
        score = label(f2(forest), 80, BLUE, weight=BOLD).next_to(score_name, DOWN, 0.3)
        rng = np.random.default_rng(22)

        def other_sites():
            return VGroup(*[Dot([rng.uniform(lo[0], hi[0]), rng.uniform(lo[1], hi[1]), 0], radius=0.07, color=GREY)
                            for _ in range(len(points))])

        # "Finally, putting an interval on a score. Scored by cross-validation by site, the random
        # forest's error is 4.32."
        self.play(FadeIn(dots, lag_ratio=0.005), FadeIn(head), run_time=self.share(0.12))
        cue(self, "the random")
        self.play(FadeIn(score_name), FadeIn(score, scale=1.2), run_time=self.share(0.1))
        # "But that number comes from one survey."
        cue(self, "But that number")
        self.play(Indicate(dots, color=BLUE, scale_factor=1.05), run_time=self.share(0.08))
        # "With other sites, it would have come out higher or lower."
        cue(self, "With other sites")
        other_head = label("other sites it might have drawn", 30, GREY, weight=BOLD).move_to(head)
        current = dots
        for k, value in enumerate(others):
            new = other_sites()
            moved = label(f2(value), 80, GREY, weight=BOLD).move_to(score)
            anims = [ReplacementTransform(current, new), Transform(score, moved)]
            if k == 0:
                anims.append(ReplacementTransform(head, other_head))
            self.play(*anims, run_time=self.share(0.12))
            current = new
        self.finish()


def site_squares():
    return VGroup(*[Square(0.26, stroke_width=0, fill_color=BLUE, fill_opacity=0.85) for _ in range(160)]
                  ).arrange_in_grid(10, 16, buff=0.06)


class Scene15(VideoScene):
    number = 15

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
        axis_name = label("the forest's error in each resample", 26, SUBDUED).next_to(axis, DOWN, 0.15)
        lo, hi = scores.min(), scores.max()
        to_x = lambda v: -3.0 + (v - lo) / (hi - lo) * 6.0  # noqa: E731
        bins = np.linspace(lo, hi, 31)
        counts, _ = np.histogram(scores, bins)
        hist = VGroup(*[Rectangle(width=6.0 / 30 * 0.9, height=max(c / counts.max() * 1.6, 0.001), stroke_width=0,
                                  fill_color=ORANGE, fill_opacity=0.7
                                  ).move_to([to_x((bins[i] + bins[i + 1]) / 2), -2.9, 0], aligned_edge=DOWN)
                        for i, c in enumerate(counts)])
        first = Dot([to_x(scores.iloc[0]), -2.75, 0], radius=0.1, color=ORANGE)
        # "To see by how much, draw the survey again from itself, which is called resampling."
        self.play(FadeIn(source), FadeIn(source_name), run_time=self.share(0.08))
        # "Draw 160 sites from its own 160, with replacement, so some come up twice and some not at all."
        cue(self, "Draw 160")
        self.play(FadeIn(target), FadeIn(target_name), run_time=self.share(0.06))
        self.play(LaggedStart(*[TransformFromCopy(source[i], p) for i, p in zip(drawn, picks)], lag_ratio=0.01),
                  run_time=self.share(0.2))
        self.play(FadeIn(twice), FadeIn(never), FadeIn(note), run_time=self.share(0.08))
        # "Work out the forest's error on them, ..."
        cue(self, "Work out the")
        self.play(Create(axis), FadeIn(axis_name), FadeIn(first, scale=2), run_time=self.share(0.1))
        # "... and do it a thousand times."
        cue(self, "do it a thousand")
        self.play(FadeOut(first), LaggedStart(*[GrowFromEdge(h, DOWN) for h in hist], lag_ratio=0.03),
                  run_time=self.share(0.15))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        scores = self.data("bootstrap-scores")[FOREST]
        iv = self.data("intervals").set_index("model").loc[FOREST]
        axis, to_x = number_line(3.25, 5.75, -5.5, 5.5, -2.2, [3.5, 4.0, 4.5, 5.0, 5.5], 1)
        axis_name = label("the forest's error in each resample", 26, SUBDUED).next_to(axis, DOWN, 0.5)
        bins = np.linspace(3.25, 5.75, 51)
        counts, _ = np.histogram(scores, bins)
        width = to_x(bins[1]) - to_x(bins[0])
        hist = VGroup(*[Rectangle(width=width * 0.9, height=max(c / counts.max() * 3.0, 0.001), stroke_width=0,
                                  fill_color=GREY, fill_opacity=0.5
                                  ).move_to([to_x((bins[i] + bins[i + 1]) / 2), -2.2, 0], aligned_edge=DOWN)
                        for i, c in enumerate(counts)])
        middle = [h for h, i in zip(hist, range(len(counts))) if iv["lower"] <= (bins[i] + bins[i + 1]) / 2 <= iv["upper"]]
        band = Line([to_x(iv["lower"]), 2.0, 0], [to_x(iv["upper"]), 2.0, 0], color=ORANGE, stroke_width=10)
        band_name = label("the middle 95%: an interval", 32, ORANGE, weight=BOLD).next_to(band, UP, 0.2)
        ends = VGroup(label(f2(iv["lower"]), 34, ORANGE, weight=BOLD).next_to(band.get_start(), DOWN, 0.2),
                      label(f2(iv["upper"]), 34, ORANGE, weight=BOLD).next_to(band.get_end(), DOWN, 0.2))
        point = DashedLine([to_x(iv["RMSE"]), -2.2, 0], [to_x(iv["RMSE"]), 1.05, 0], color=BLUE, stroke_width=4)
        point_name = label(f"the survey's own: {f2(iv['RMSE'])}", 28, BLUE, weight=BOLD
                           ).next_to(point.get_end(), RIGHT, 0.15)
        # "The middle 95 per cent of those thousand errors ..."
        self.play(FadeIn(axis), FadeIn(axis_name), FadeIn(hist), run_time=self.share(0.12))
        # "... is a 95 per cent interval."
        cue(self, "is a 95")
        self.play(*[h.animate.set_fill(ORANGE, opacity=0.75) for h in middle], Create(band), FadeIn(band_name),
                  run_time=self.share(0.12))
        # "For the forest, it runs from 3.75 to 4.94."
        cue(self, "it runs from")
        self.play(FadeIn(ends), run_time=self.share(0.1))
        # "Its error on new sites could be anywhere in that range, not exactly 4.32."
        cue(self, "not exactly")
        self.play(Create(point), FadeIn(point_name), run_time=self.share(0.1))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        iv = self.data("intervals").set_index("model")
        order = [FOREST, LINEAR, AVERAGE]
        axis, to_x = number_line(3.5, 5.75, -3.0, 6.2, -2.4, [3.5, 4.0, 4.5, 5.0, 5.5], 1)
        axis_name = label("error on new sites", 28, SUBDUED).next_to(axis, DOWN, 0.5)
        rows = VGroup()
        for i, m in enumerate(order):
            y = 1.3 - 1.1 * i
            colour = BLUE if m == FOREST else GREY
            bar = Line([to_x(iv.loc[m, "lower"]), y, 0], [to_x(iv.loc[m, "upper"]), y, 0], color=colour,
                       stroke_width=14, stroke_opacity=0.6)
            dot = Dot([to_x(iv.loc[m, "RMSE"]), y, 0], radius=0.15, color=colour)
            name = label(MODEL_NAMES[m], 28, INK).next_to([-3.2, y, 0], LEFT, 0.1)
            rows.add(VGroup(name, bar, dot))
        shared_lo = max(iv.loc[m, "lower"] for m in order)
        shared_hi = min(iv.loc[m, "upper"] for m in order)
        overlap = Rectangle(width=to_x(shared_hi) - to_x(shared_lo), height=3.6, stroke_width=0, fill_color=ORANGE,
                            fill_opacity=0.15).move_to([(to_x(shared_lo) + to_x(shared_hi)) / 2, 0.2, 0])
        overlap_name = label("all three overlap", 28, ORANGE, weight=BOLD).next_to(overlap, UP, 0.1)
        head = label("95% intervals", 32, SUBDUED).to_edge(UP, buff=0.4)
        lesson = label("a small gap between scores is not a ranking", 36, INK, weight=BOLD).to_edge(UP, buff=0.4)
        self.add(head, axis, axis_name, rows[0])
        # "Add linear regression and predicting the average, ..."
        self.play(*[AnimationGroup(FadeIn(r[0]), FadeIn(r[2]), GrowFromCenter(r[1])) for r in rows[1:]],
                  run_time=self.share(0.15))
        # "... and all three intervals overlap."
        cue(self, "and all three")
        self.play(FadeIn(overlap), FadeIn(overlap_name), run_time=self.share(0.1))
        # "So a small gap between two scores is not, on its own, a ranking: ..."
        cue(self, "So a small gap")
        self.play(FadeOut(head, shift=0.2 * UP), FadeIn(lesson, shift=0.2 * UP), run_time=self.share(0.1))
        # "... with other sites, the order could change."
        cue(self, "the order could")
        self.play(Indicate(VGroup(rows[0][2], rows[1][2]), color=ORANGE, scale_factor=1.4), run_time=self.share(0.1))
        self.finish()


class Scene18(KeyPointScene):
    number = 18
    point = 3


# Quiz (scenes 19–20) -----------------------------------------------------------------------

class Scene19(QuizScene):
    number = 19
    question = ("You will map coast nobody has surveyed.",
                "Hold out single stations, or whole blocks?",
                "Which test gives the honest score?")


class Scene20(VideoScene):
    number = 20

    def construct(self):
        means, axis, rows, head, to_x = two_tests(self)
        stations, blocks = rows["Stations"], rows["Half-degree blocks"]
        answer = label("whole blocks", 72, GREEN, weight=BOLD).to_edge(UP, buff=0.4)
        flatters = label("flatters the model", 30, VERMILION, weight=BOLD).next_to(stations[3], RIGHT, 0.4)
        honest = SurroundingRectangle(blocks, color=GREEN, buff=0.2, corner_radius=0.1)
        # "Whole blocks."
        self.play(FadeIn(answer, scale=1.3), run_time=self.share(0.1))
        # "Holding out single stations leaves each station's neighbours in the training data, ..."
        cue(self, "Holding out single")
        self.play(FadeIn(axis), FadeIn(stations), run_time=self.share(0.12))
        # "... so the score flatters the model."
        cue(self, "so the score")
        self.play(FadeIn(flatters), run_time=self.share(0.08))
        # "On the survey, that was 4.23 against 4.41."
        cue(self, "On the survey")
        self.play(FadeIn(blocks), Create(honest), run_time=self.share(0.12))
        self.finish()


# Key points and end card (scenes 21–24) ---------------------------------------------------

class Scene21(RecapScene):
    number = 21
    point = 1


class Scene22(RecapScene):
    number = 22
    point = 2


class Scene23(RecapScene):
    number = 23
    point = 3


class Scene24(EndCardScene):
    number = 24
