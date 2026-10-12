"""Manim scenes for the assumptions video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/06-assumptions-limitations
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

A gentle introduction to the section, built on three ideas with one picture each:
machine learning frees a model from straight lines, but not from how the data were
collected, and a rare answer fools accuracy. Scenes marked "page results" read
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
ANSWERS = ["From straight lines:\nit can find the shape\nin the data on its own",
           "Not from how the data\nwere collected: where the survey\nnever went, it is guessing",
           "Count what the model finds,\nnot just how often\nit is right"]
RECAP = ["Machine learning frees a model from straight lines",
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


# Machine learning frees a model from straight lines (scenes 2–5) ----------------------------

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
        prefers = label("a temperature it prefers", 28, INK, weight=BOLD).move_to(hump + 0.35 * UP)
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
        prefers = label("a temperature it prefers", 28, INK, weight=BOLD).move_to(hump + 0.35 * UP)
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


class Scene05(KeyPointScene):
    number, point = 5, 1


# But not from how the data were collected (scenes 6–11) -------------------------------------

class Scene06(VideoScene):
    """Schematic: a model learns only from its stations, and survey effort gathers near a port."""

    number = 6

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
        unsurveyed = label("never surveyed", 28, SUBDUED, weight=BOLD).move_to(sea.get_right() + 1.7 * LEFT + 1.5 * DOWN)
        model = RoundedRectangle(width=2.6, height=1.4, corner_radius=0.2, stroke_color=GREEN, stroke_width=6
                                 ).move_to(4.8 * RIGHT + 0.6 * UP)
        model_name = label("the model", 32, GREEN, weight=BOLD).move_to(model)
        arrow = Arrow(stations.get_right(), model.get_left(), color=INK, stroke_width=6, buff=0.3)
        only = lines("it can only learn", "from these stations", size=28).next_to(model, DOWN, 0.4)
        effort = label("survey effort follows ports, weather and ship time", 30, INK, weight=BOLD
                       ).to_edge(DOWN, buff=0.3)
        # "Next, what it does not free a model from."
        self.play(FadeIn(sea), FadeIn(land), FadeIn(port), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in stations], lag_ratio=0.03), run_time=self.share(0.1))
        # "However flexible, a model can only learn from the stations it was given."
        cue(self, "a model can only")
        self.play(FadeIn(model), FadeIn(model_name), GrowArrow(arrow), FadeIn(only), run_time=self.share(0.14))
        # "And survey effort is never even: it follows ports, weather and ship time."
        cue(self, "And survey effort")
        self.play(FadeIn(unsurveyed), Indicate(port, color=INK), run_time=self.share(0.1))
        cue(self, "it follows ports")
        self.play(FadeIn(effort, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def novelty_layout(scene):
    """The summer and autumn survey by depth and temperature, and the winter stations, for scenes 7–10."""
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
    cold = surveyed["temperature_c"] < 8
    left = surveyed["depth_m"][cold].min()
    cold_zone = Rectangle(width=axes.c2p(200, 0)[0] - axes.c2p(left, 0)[0],
                          height=axes.c2p(0, 8)[1] - axes.c2p(0, 0)[1], stroke_color=BLUE, stroke_width=4,
                          fill_color=BLUE, fill_opacity=0.08).move_to(axes.c2p(left, 0), aligned_edge=DL)
    cold_name = label("cold water: only at depth", 28, BLUE, weight=BOLD)
    return frame, surveyed_dots, winter_dots, head, key, cold_zone, cold_name


class Scene07(VideoScene):
    number = 7

    def construct(self):
        frame, dots, winter, head, key, cold_zone, cold_name = novelty_layout(self)
        cold_name.next_to(key[0], DOWN, 0.4, aligned_edge=LEFT)
        # "Here is a survey that sailed only in summer and autumn."
        self.play(FadeIn(frame), FadeIn(head), run_time=self.share(0.12))
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


class Scene08(VideoScene):
    number = 8

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


class Scene09(VideoScene):
    number = 9

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
        # "On the page, the forest's errors grew the further a station lay from the survey."
        cue(self, "On the page")
        self.play(FadeIn(grew, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene10(VideoScene):
    number = 10

    def construct(self):
        frame, dots, winter, head, key, cold_zone, cold_name = novelty_layout(self)
        seen = winter_notes(key)
        self.add(frame, dots, head, key, winter, seen)
        question = VGroup(label("before trusting a prediction, ask:", 34, INK, weight=BOLD),
                          label("did the survey see conditions like these?", 40, BLUE, weight=BOLD)
                          ).arrange(DOWN, buff=0.2)
        page = label("the page shows a simple way to measure it", 28, SUBDUED).next_to(question, DOWN, 0.45)
        words = VGroup(question, page).move_to(0.2 * DOWN)
        box = SurroundingRectangle(words, color=BLUE, buff=0.45, corner_radius=0.2, stroke_width=5,
                                   fill_color=BACKGROUND, fill_opacity=0.97)
        VGroup(box, words).set_z_index(5)
        # "So before trusting a prediction, ask one question: did the survey see conditions like these?"
        self.play(FadeOut(seen), dots.animate.set_opacity(0.4), winter.animate.set_opacity(0.4),
                  run_time=self.share(0.06))
        self.play(FadeIn(box), FadeIn(question[0]), run_time=self.share(0.1))
        cue(self, "did the survey")
        self.play(FadeIn(question[1], shift=0.2 * UP), run_time=self.share(0.12))
        # "The page shows a simple way to measure it."
        cue(self, "The page shows")
        self.play(FadeIn(page), run_time=self.share(0.1))
        self.finish()


class Scene11(KeyPointScene):
    number, point = 11, 2


# A rare answer fools accuracy (scenes 12–16) ------------------------------------------------

def rare_grid(scene):
    """The training stations as dots, the ones with the rare species picked out, for scenes 12–15."""
    rare = scene.data("rare").iloc[0]
    n, present = int(rare["stations"]), int(rare["present"])
    dots = VGroup(*[Dot(radius=0.065, color=LIGHT) for _ in range(n)]).arrange_in_grid(cols=26, buff=0.09)
    dots.move_to(3.2 * LEFT + 0.3 * DOWN)
    picks = np.random.default_rng(3).choice(n, present, replace=False)
    lit = VGroup(*[dots[k] for k in picks])
    others = VGroup(*[d for k, d in enumerate(dots) if k not in set(picks)])
    return rare, dots, lit, others


def lit_up(lit):
    for d in lit:
        d.set_color(VERMILION).scale(1.4)


class Scene12(VideoScene):
    number = 12

    def construct(self):
        rare, dots, lit, _ = rare_grid(self)
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
        self.play(*[d.animate.set_color(VERMILION).scale(1.4) for d in lit], FadeIn(found), run_time=self.share(0.12))
        self.finish()


def trap_panel(scene):
    plain = scene.data("at-default").set_index("training").loc["No rebalancing"]
    head = VGroup(label("logistic regression", 32, INK, weight=BOLD),
                  label("threshold 0.5", 28, SUBDUED)).arrange(DOWN, buff=0.08).move_to(3.9 * RIGHT + 2.7 * UP)
    found = VGroup(label("presences found", 30, VERMILION),
                   label(f"{plain['called_present'] - plain['false_alarms']:.0f}", 64, VERMILION, weight=BOLD)
                   ).arrange(DOWN, buff=0.1).move_to(3.9 * RIGHT + 0.9 * UP)
    accuracy = VGroup(label("accuracy", 30, GREEN), label(f"{100 * plain['accuracy']:.0f}%", 64, GREEN, weight=BOLD)
                      ).arrange(DOWN, buff=0.1).move_to(3.9 * RIGHT + 1.3 * DOWN)
    meaning = label("the share of its calls that are right", 26, SUBDUED).next_to(accuracy, DOWN, 0.15)
    return plain, head, found, accuracy, meaning


class Scene13(VideoScene):
    number = 13

    def construct(self):
        rare, dots, lit, _ = rare_grid(self)
        lit_up(lit)
        self.add(dots)
        plain, head, found, accuracy, meaning = trap_panel(self)
        everywhere = label("as if it said absent everywhere", 28, INK, weight=BOLD).next_to(meaning, DOWN, 0.3)
        rings = VGroup(*[Circle(0.13, color=VERMILION, stroke_width=3).move_to(d) for d in lit])
        # "Logistic regression gives each station a probability of presence, ..."
        self.play(FadeIn(head), run_time=self.share(0.1))
        # "Here it finds none of the presences."
        cue(self, "Here it finds")
        self.play(FadeIn(found), Create(rings), run_time=self.share(0.1))
        # "Yet its accuracy, the share of its calls that are right, is 95 per cent."
        cue(self, "Yet its accuracy")
        self.play(FadeIn(accuracy), FadeIn(meaning), run_time=self.share(0.1))
        # "Calling the species absent everywhere is right almost everywhere."
        cue(self, "Calling the species")
        self.play(FadeIn(everywhere, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


def sensitivity_name():
    return VGroup(label("sensitivity", 40, BLUE, weight=BOLD),
                  label("of the stations with the species,", 26, INK),
                  label("the share called present", 26, INK)
                  ).arrange(DOWN, buff=0.08).move_to(3.9 * RIGHT + 2.2 * UP)


class Scene14(VideoScene):
    number = 14

    def construct(self):
        rare, dots, lit, _ = rare_grid(self)
        lit_up(lit)
        plain, head, found, accuracy, meaning = trap_panel(self)
        self.add(dots, head, found, accuracy, meaning)
        name = sensitivity_name()
        value = label(f"{plain['sensitivity']:.0f}", 72, BLUE, weight=BOLD).move_to(3.9 * RIGHT + 0.2 * DOWN)
        hid = lines("the 95% hid a model", "that finds nothing", size=30, colour=VERMILION
                    ).next_to(value, DOWN, 0.5)
        hid.set_x(value.get_x())
        # "So count what the model finds."
        self.play(FadeOut(VGroup(head, found, accuracy, meaning)), run_time=self.share(0.08))
        # "Sensitivity is the share of the stations with the species that the model calls present."
        cue(self, "Sensitivity is")
        self.play(FadeIn(name), Indicate(lit, color=BLUE, scale_factor=1.6), run_time=self.share(0.14))
        # "Here it is 0: ..."
        cue(self, "Here it is")
        self.play(FadeIn(value, scale=1.3), run_time=self.share(0.08))
        # "... the 95 per cent hid a model that finds nothing."
        cue(self, "the 95 per cent")
        self.play(FadeIn(hid, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        rare, dots, lit, others = rare_grid(self)
        lit_up(lit)
        lower = self.data("same").iloc[0]
        self.add(dots)
        name = sensitivity_name()
        self.add(name)
        # Drawn at the page's rates: the share of presences found, and of absences called present.
        rng = np.random.default_rng(8)
        found = [lit[k] for k in rng.choice(len(lit), round(lower["sensitivity"] * len(lit)), replace=False)]
        alarms = [others[k] for k in rng.choice(len(others), round((1 - lower["specificity"]) * len(others)),
                                               replace=False)]
        rings = VGroup(*[Circle(0.14, color=GREEN, stroke_width=4).move_to(d) for d in found])
        threshold = label("threshold lowered", 30, INK, weight=BOLD).move_to(3.9 * RIGHT + 0.5 * UP)
        value = label(f"about {lower['sensitivity']:.1f}", 56, GREEN, weight=BOLD).next_to(threshold, DOWN, 0.25)
        seven = label("7 in 10 found", 28, GREEN).next_to(value, DOWN, 0.1)
        price = VGroup(key_row(PURPLE, "false alarms:", 28), label("without the species, called present", 24, INK)
                       ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(seven, DOWN, 0.45)
        price.set_x(threshold.get_x())
        costs = lines("where to set it:", "what each mistake costs", size=28, colour=BLUE
                      ).next_to(price, DOWN, 0.45)
        costs.set_x(threshold.get_x())
        # "Lower the threshold, and the model finds about 7 in 10 of them."
        self.play(FadeIn(threshold), run_time=self.share(0.08))
        cue(self, "the model finds")
        self.play(Create(rings), FadeIn(value), FadeIn(seven), run_time=self.share(0.14))
        # "The price is more false alarms: stations without the species called present."
        cue(self, "The price")
        self.play(*[d.animate.set_color(PURPLE) for d in alarms], FadeIn(price), run_time=self.share(0.14))
        # "Where to set the threshold depends on what each mistake costs."
        cue(self, "Where to set")
        self.play(FadeIn(costs, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene16(KeyPointScene):
    number, point = 16, 3


# Quiz (scenes 17–18) -----------------------------------------------------------------------

class Scene17(QuizScene):
    number = 17
    question = ("A harmful algal bloom occurs", "on 2 days in 100.",
                "A model that warns of blooms is 98% accurate.", "Is it a good model?")


class Scene18(VideoScene):
    """Schematic: a hundred days, two with a bloom, and a model that never warns."""

    number = 18

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
        ask = VGroup(label("ask for its sensitivity:", 30, BLUE, weight=BOLD),
                     label("how many blooms it catches", 30, INK)
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
        # "Ask for its sensitivity: how many of the blooms it catches."
        cue(self, "Ask for")
        self.play(FadeIn(ask, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


# The recap (scenes 19–21) and the end card (scene 22) --------------------------------------

class Scene19(RecapScene):
    number, point = 19, 1


class Scene20(RecapScene):
    number, point = 20, 2


class Scene21(RecapScene):
    number, point = 21, 3


class Scene22(EndCardScene):
    number = 22
