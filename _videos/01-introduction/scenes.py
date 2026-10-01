"""Manim scenes for the introduction video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/01-introduction
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is an overview of the section: a short tour of its five pages. Scenes marked
"page results" read visuals/data/*.csv, which tools/figures-for-video.R writes from the
pages. The others are schematic: made-up shapes, never numbers that could pass for
survey results. The opening, key-point, recap, quiz and end-card scenes are shared
(mlbasic_video.py) and read PROMISES, ANSWERS and RECAP from here. Consecutive scenes
about one picture share a builder, so each starts where the previous one ended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mlbasic_video import *  # noqa: E402,F403


class Title(TitleScene):
    pass


PROMISES = ["The kinds of learning",
            "How machine learning relates to statistics",
            "Where it helps in marine science"]
ANSWERS = ["Answers or none:\nsupervised or\nunsupervised",
           "Same models, different\naims: decide first to\npredict or to explain",
           "Six tasks, each\nlimited by its labels"]
RECAP = ["Your data decide the kind of learning",
         "Decide first: predict or explain",
         "Six tasks, limited by their labels"]


class Scene01(LearnScene):
    number = 1
    times = (0.4, 0.55, 0.8)


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def polyline(axes, xs, ys, colour, width=6):
    return VMobject(color=colour, stroke_width=width).set_points_as_corners(
        [axes.c2p(x, y) for x, y in zip(xs, ys)])


def chart(x_range, y_range, x_length, y_length, x_ticks, y_ticks, x_name, y_name, size=24):
    """Axes with tick labels and names, in the series style; returns the axes and all of it."""
    axes = plain_axes(x_range, y_range, x_length, y_length)
    tx = VGroup(*[label(f"{v:g}", size, SUBDUED).next_to(axes.c2p(v, y_range[0]), DOWN, 0.15)
                  for v in x_ticks])
    ty = VGroup(*[label(f"{v:g}", size, SUBDUED).next_to(axes.c2p(x_range[0], v), LEFT, 0.15)
                  for v in y_ticks])
    xn = label(x_name, 26, SUBDUED).next_to(tx if len(tx) else axes, DOWN, 0.2)
    yn = label(y_name, 26, SUBDUED).rotate(PI / 2).next_to(ty if len(ty) else axes, LEFT, 0.2) \
        if y_name else VGroup()
    return axes, VGroup(axes, tx, ty, xn, yn)


def card(text, colour=PURPLE, size=40):
    words = label(text, size, colour, weight=BOLD)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def at(scene, fraction):
    """Wait until this fraction of the narration."""
    scene.wait(max(scene.share(fraction) - scene.time, 0.01))


# The survey data (scenes 2–6) -----------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        # Schematic: measurements in, a prediction out, for a case the model has not seen.
        inputs = VGroup(*[card(t, SKY, 30) for t in ["temperature", "salinity", "depth"]]
                        ).arrange(DOWN, buff=0.25).move_to([-4.6, -0.3, 0])
        unseen = label("a new case", 30, SUBDUED, weight=BOLD).next_to(inputs, UP, 0.35)
        box = RoundedRectangle(width=3.0, height=2.2, corner_radius=0.25, stroke_color=INK, stroke_width=5,
                               fill_color=GRID, fill_opacity=0.5).move_to([0, -0.3, 0])
        name = label("a model", 40, INK, weight=BOLD).move_to(box)
        fitted = label("fitted to examples", 28, SUBDUED).next_to(box, DOWN, 0.3)
        output = card("a prediction", GREEN, 38).move_to([4.6, -0.3, 0])
        arrow_in = Arrow(inputs.get_right(), box.get_left(), color=INK, stroke_width=5, buff=0.2)
        arrow_out = Arrow(box.get_right(), output.get_left(), color=INK, stroke_width=5, buff=0.2)
        # "Machine learning fits a model to examples,"
        self.play(FadeIn(box), FadeIn(name), FadeIn(fitted), run_time=self.share(0.2))
        # "so that it can make good predictions for cases it has not seen."
        at(self, 0.4)
        self.play(FadeIn(inputs), FadeIn(unseen), GrowArrow(arrow_in), run_time=self.share(0.2))
        self.play(GrowArrow(arrow_out), FadeIn(output, shift=0.2 * RIGHT), run_time=self.share(0.15))
        self.finish()


SURVEY_COLUMNS = [("temperature", "°C", "temperature_c", "{:.2f}"), ("salinity", "how salty", "salinity_psu", "{:.2f}"),
                  ("depth", "metres", "depth_m", "{:.1f}"), ("abundance", "animals counted", "abundance", "{:d}"),
                  ("present", "found or not", "present", "{}")]


def survey_layout(scene):
    """The first five stations, as the types-of-learning page prints them."""
    rows = scene.data("survey-head")
    n = len(scene.data("clusters"))
    xs = [-4.6, -2.2, 0.1, 2.4, 4.7]
    # Each column's name with a short gloss under it, so a column can appear as it is named.
    header = VGroup(*[VGroup(label(name, 30, INK, weight=BOLD).move_to([x, 1.75, 0]),
                             label(gloss, 22, SUBDUED).move_to([x, 1.3, 0]))
                      for (name, gloss, _, _), x in zip(SURVEY_COLUMNS, xs)])
    rule = Line([-5.9, 1.0, 0], [5.9, 1.0, 0], color=GRID, stroke_width=3)
    cells = VGroup()
    for i, row in rows.iterrows():
        y = 0.5 - 0.6 * i
        cells.add(VGroup(*[label(fmt.format(row[col]), 30, INK).move_to([x, y, 0])
                           for (_, _, col, fmt), x in zip(SURVEY_COLUMNS, xs)]))
    table = VGroup(header, rule, cells)
    head = label(f"{n} stations on a coastal shelf", 34, SUBDUED, weight=BOLD).to_edge(UP, buff=0.5)
    band = RoundedRectangle(width=2.1, height=4.3, corner_radius=0.12, stroke_width=0, fill_color=ORANGE,
                            fill_opacity=0.15).move_to([xs[4], -0.2, 0])
    return table, head, band


class Scene03(VideoScene):
    number = 3

    def construct(self):
        table, head, band = survey_layout(self)
        header, rule, cells = table
        course = VGroup(label("one simulated marine dataset,", 44, PURPLE, weight=BOLD),
                        label("used throughout the course", 44, PURPLE, weight=BOLD)).arrange(DOWN, buff=0.2)
        # "Throughout this course, we use one simulated marine dataset again and again."
        self.play(FadeIn(course, shift=0.2 * UP), run_time=self.share(0.08))
        # "It is a survey of 800 stations on a coastal shelf."
        at(self, 0.22)
        self.play(ReplacementTransform(course, head), Create(rule), run_time=self.share(0.08))
        # Each column appears as it is named: "temperature", "salinity, which is how salty
        # it is", "depth", then the species: "abundance, the number of animals counted",
        # "and whether it was present at all."
        for j, when in enumerate([0.46, 0.52, 0.66, 0.78, 0.92]):
            at(self, when)
            self.play(FadeIn(header[j]), LaggedStart(*[FadeIn(r[j]) for r in cells], lag_ratio=0.15),
                      run_time=self.share(0.05))
        self.finish()


class Scene04(VideoScene):
    number = 4

    def construct(self):
        table, head, band = survey_layout(self)
        self.add(table, head)
        known = card("simulated: the true answers are known", PURPLE, 36).to_edge(DOWN, buff=0.35)
        # "Because we wrote the simulation, we know the true answers,"
        self.play(FadeIn(known, shift=0.2 * UP), run_time=self.share(0.2))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        table, head, band = survey_layout(self)
        self.add(table, head)
        answer = label("the answer", 30, ORANGE, weight=BOLD).next_to(band, DOWN, 0.2)
        sup = label("supervised", 52, ORANGE, weight=BOLD).to_edge(DOWN, buff=0.45)
        # "If every example comes with an answer, such as whether the species was found,"
        self.play(FadeIn(band), FadeIn(answer), run_time=self.share(0.25))
        # "the learning is supervised."
        at(self, 0.7)
        self.play(FadeIn(sup, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene06(VideoScene):
    number = 6

    def construct(self):
        # Schematic: the answer is a quantity or a category.
        start = card("the answer", ORANGE, 40).move_to([-4.4, 0, 0])
        quantity = VGroup(label("a quantity", 40, INK, weight=BOLD), label("abundance", 30, SUBDUED)
                          ).arrange(DOWN, buff=0.12).move_to([0.4, 1.4, 0])
        category = VGroup(label("a category", 40, INK, weight=BOLD), label("present or absent", 30, SUBDUED)
                          ).arrange(DOWN, buff=0.12).move_to([0.4, -1.4, 0])
        reg = label("regression", 46, BLUE, weight=BOLD).move_to([4.5, 1.4, 0])
        cls = label("classification", 46, GREEN, weight=BOLD).move_to([4.5, -1.4, 0])
        arrows = [Arrow(start.get_right(), q.get_left(), color=INK, stroke_width=5, buff=0.3) for q in (quantity, category)]
        self.play(FadeIn(start), run_time=self.share(0.1))
        # "When the answer is a quantity, the task is regression."
        at(self, 0.15)
        self.play(GrowArrow(arrows[0]), FadeIn(quantity), run_time=self.share(0.15))
        self.play(FadeIn(reg, shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "When it is a category, such as present or absent, it is classification."
        at(self, 0.55)
        self.play(GrowArrow(arrows[1]), FadeIn(category), run_time=self.share(0.15))
        at(self, 0.85)
        self.play(FadeIn(cls, shift=0.2 * RIGHT), run_time=self.share(0.1))
        self.finish()


# Unsupervised, and what a model learns (scenes 7–9) ------------------------------------------

GROUP_COLOURS = {"Shallow": ORANGE, "Mid-depth": GREEN, "Deep": BLUE}


class Scene07(VideoScene):
    number = 7

    def construct(self):
        stations = self.data("clusters")
        axes, frame = chart([0, 200, 50], [2, 16, 2], 8.0, 5.0, [0, 50, 100, 150, 200], [4, 8, 12, 16],
                            "depth (m)", "temperature (°C)")
        frame.move_to([-1.6, -0.3, 0])
        grey = VGroup(*[Dot(axes.c2p(d, t), 0.04, color=GREY, fill_opacity=0.6)
                        for d, t in zip(stations["depth_m"], stations["temperature_c"])])
        coloured = VGroup(*[Dot(axes.c2p(d, t), 0.04, color=GROUP_COLOURS[g], fill_opacity=0.8)
                            for d, t, g in zip(stations["depth_m"], stations["temperature_c"], stations["group"])])
        names = VGroup()
        for g, colour in GROUP_COLOURS.items():
            names.add(label(g, 34, colour, weight=BOLD))
        names.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([4.8, -0.9, 0])
        note = VGroup(label("no answers:", 32, SUBDUED, weight=BOLD),
                      label("the water only", 32, SUBDUED, weight=BOLD)).arrange(DOWN, buff=0.12)
        note.move_to([4.8, 2.0, 0])
        head = label("unsupervised: k-means, three groups", 34, INK, weight=BOLD).to_edge(UP, buff=0.35)
        # "With no answers at all, the learning is unsupervised."
        self.play(FadeIn(frame), FadeIn(grey), FadeIn(note), run_time=self.share(0.25))
        # "Here k-means sorts the stations into three groups using only the water:"
        at(self, 0.35)
        self.play(FadeIn(head), Transform(grey, coloured), run_time=self.share(0.25))
        # "shallow, mid-depth and deep."
        at(self, 0.75)
        self.play(LaggedStart(*[FadeIn(n, shift=0.2 * RIGHT) for n in names], lag_ratio=0.4), run_time=self.share(0.2))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        # Schematic: a structureless cloud, cut into three groups and then into six.
        rng = np.random.default_rng(8)
        points = rng.normal(0, 1, (220, 2)) * [1.7, 0.9]
        palette = [ORANGE, BLUE, GREEN, VERMILION, PURPLE, SKY]

        def cut(k):
            centres = points[rng.choice(len(points), k, replace=False)]
            for _ in range(10):
                owner = np.argmin(((points[:, None, :] - centres[None]) ** 2).sum(-1), 1)
                centres = np.array([points[owner == j].mean(0) if (owner == j).any() else centres[j] for j in range(k)])
            return owner

        three, six = cut(3), cut(6)
        dots = VGroup(*[Dot([x, y - 0.1, 0], 0.07, color=palette[three[i]]) for i, (x, y) in enumerate(points)])
        head = label("ask for three: three groups", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        head6 = label("ask for six: six groups", 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
        check = card("groups appear whether or not they are real", PURPLE, 32).to_edge(DOWN, buff=0.4)
        # "It will return groups whether or not real ones exist,"
        self.play(FadeIn(head), FadeIn(dots), run_time=self.share(0.15))
        at(self, 0.2)
        self.play(ReplacementTransform(head, head6),
                  *[d.animate.set_color(palette[six[i]]) for i, d in enumerate(dots)], run_time=self.share(0.2))
        # "so its results need checking."
        at(self, 0.55)
        self.play(FadeIn(check, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def two_groups(rng, centre, spread, n):
    return centre + rng.normal(0, 1, (n, 2)) * spread


def triangle(point, colour=ORANGE, size=0.14):
    return Triangle(color=colour, fill_color=colour, fill_opacity=1, stroke_width=0).scale(size).move_to(point)


class Scene09(VideoScene):
    number = 9

    def construct(self):
        # Schematic: the same two groups seen by the two kinds of model.
        rng = np.random.default_rng(9)
        found = two_groups(rng, np.array([-0.7, -0.4]), [0.45, 0.4], 22)
        absent = two_groups(rng, np.array([0.9, 0.5]), [0.45, 0.4], 20)
        panels = VGroup()
        for cx, name, colour, note in [(-3.5, "Discriminative", GREEN, "learns the boundary"),
                                       (3.5, "Generative", PURPLE, "learns each group")]:
            box = RoundedRectangle(width=6.4, height=4.0, corner_radius=0.2, stroke_color=colour, stroke_width=4
                                   ).move_to([cx, -0.6, 0])
            heading = VGroup(label(name, 40, colour, weight=BOLD), label(note, 28, SUBDUED)
                             ).arrange(DOWN, buff=0.1).next_to(box, UP, 0.25)
            dots = VGroup(*[Dot([cx + x, -0.6 + y, 0], 0.08, color=BLUE) for x, y in found],
                          *[triangle([cx + x, -0.6 + y, 0]) for x, y in absent])
            panels.add(VGroup(box, heading, dots))
        boundary = DashedLine([-3.5 - 1.2, -0.6 + 1.8, 0], [-3.5 + 1.0, -0.6 - 1.9, 0], color=INK, stroke_width=5)
        blobs = VGroup(Ellipse(width=2.4, height=2.0, color=BLUE, fill_opacity=0.12, stroke_width=4).move_to([3.5 - 0.7, -1.0, 0]),
                       Ellipse(width=2.4, height=2.0, color=ORANGE, fill_opacity=0.15, stroke_width=4).move_to([3.5 + 0.9, -0.1, 0]))
        new = Circle(0.13, color=BLUE, stroke_width=5, fill_color=BACKGROUND, fill_opacity=1).move_to([3.5 - 1.1, -0.7, 0])
        new_name = label("a new example", 26, SUBDUED).move_to([3.5 - 1.1, 1.0, 0])
        new_arrow = Arrow(new_name.get_bottom(), new.get_top(), color=GREY, stroke_width=3, buff=0.08)
        tools = card("text and image generators are generative", PURPLE, 30).to_edge(DOWN, buff=0.1)
        # "Models also differ in what they learn."
        self.play(FadeIn(panels[0][2]), FadeIn(panels[1][2]), FadeIn(panels[0][0]), FadeIn(panels[1][0]),
                  run_time=self.share(0.12))
        # "A discriminative model learns only the line between outcomes."
        at(self, 0.18)
        self.play(FadeIn(panels[0][1]), Create(boundary), run_time=self.share(0.15))
        # "A generative model learns the data themselves, and can invent new examples."
        at(self, 0.42)
        self.play(FadeIn(panels[1][1]), FadeIn(blobs), run_time=self.share(0.15))
        at(self, 0.6)
        self.play(GrowFromCenter(new), FadeIn(new_name), GrowArrow(new_arrow), run_time=self.share(0.1))
        # "The tools that write text and draw pictures are generative."
        at(self, 0.78)
        self.play(FadeIn(tools, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene10(KeyPointScene):
    number, point = 10, 1


# Statistics and machine learning (scenes 11–19) --------------------------------------------

class Scene11(VideoScene):
    number = 11

    def construct(self):
        # Schematic: the statistics page's scale of methods.
        bar = Rectangle(width=11.6, height=0.22, stroke_width=0).set_fill([BLUE, ORANGE], opacity=1)
        bar.set_sheen_direction(RIGHT).move_to([0, 0.4, 0])
        methods = ["t-test", "ANOVA", "linear regression", "GLM", "GAM", "decision tree", "random forest", "neural network"]
        xs = np.linspace(-5.2, 5.2, len(methods))
        ticks, names = VGroup(), VGroup()
        for i, (x, m) in enumerate(zip(xs, methods)):
            ticks.add(Line([x, 0.1, 0], [x, 0.7, 0], color=INK, stroke_width=3))
            names.add(label(m, 28, INK).move_to([x, 1.15 if i % 2 == 0 else -0.35, 0]))
        both = RoundedRectangle(width=xs[4] - xs[2] + 2.3, height=2.2, corner_radius=0.15, stroke_width=0,
                                fill_color=PURPLE, fill_opacity=0.15).move_to([(xs[2] + xs[4]) / 2, 0.4, 0])
        both_name = label("used by both", 32, PURPLE, weight=BOLD).next_to(both, DOWN, 0.2)
        left = label("you write the shape down", 28, BLUE, weight=BOLD).move_to([-4.2, -1.9, 0])
        right = label("the algorithm finds it", 28, ORANGE, weight=BOLD).move_to([4.4, -1.9, 0])
        head = label("one toolbox", 44, INK, weight=BOLD).to_edge(UP, buff=0.7)
        # "Machine learning is not a separate subject from statistics."
        self.play(FadeIn(head), GrowFromCenter(bar), run_time=self.share(0.2))
        self.play(LaggedStart(*[AnimationGroup(Create(t), FadeIn(n)) for t, n in zip(ticks, names)], lag_ratio=0.15),
                  FadeIn(left), FadeIn(right), run_time=self.share(0.3))
        # "The two share their data and their models, and linear regression belongs to both."
        at(self, 0.65)
        self.play(FadeIn(both), FadeIn(both_name), run_time=self.share(0.15))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        # Schematic: the two aims side by side.
        cols = VGroup()
        for name, colour, lines in [("Statistical modelling", BLUE, ["estimates an effect"]),
                                    ("Machine learning", ORANGE, ["predicts new cases,", "checked on data held back"])]:
            box = RoundedRectangle(width=6.0, height=3.6, corner_radius=0.2, stroke_color=colour, stroke_width=5)
            strip = Rectangle(width=6.0, height=0.14, stroke_width=0, fill_color=colour, fill_opacity=1
                              ).align_to(box, UP)
            head = label(name, 40, INK, weight=BOLD)
            body = VGroup(*[label(t, 34, INK) for t in lines]).arrange(DOWN, buff=0.15)
            VGroup(head, body).arrange(DOWN, buff=0.5).move_to(box)
            cols.add(VGroup(box, strip, head, body))
        cols.arrange(RIGHT, buff=0.5).move_to([0, -0.3, 0])
        aim = label("the difference is the aim", 40, PURPLE, weight=BOLD).to_edge(UP, buff=0.7)
        # "The difference is mostly the aim."
        self.play(FadeIn(aim), FadeIn(cols[0][:3]), FadeIn(cols[1][:3]), run_time=self.share(0.2))
        # "A statistical model estimates an effect."
        at(self, 0.25)
        self.play(FadeIn(cols[0][3], shift=0.2 * UP), run_time=self.share(0.12))
        # "A machine-learning model predicts new cases, and is checked on data held back from fitting."
        at(self, 0.5)
        self.play(FadeIn(cols[1][3], shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


def hump_layout(scene):
    """@fig-shapes: the training stations, and each model's prediction across temperature."""
    points = scene.data("train-points")
    shapes = scene.data("shapes")
    top = 15   # the page's figure stops at 15, as does this one
    axes, frame = chart([1, 17, 1], [0, top, 5], 8.4, 5.2, [2, 5, 8, 11, 14], [0, 5, 10, 15],
                        "temperature (°C)", "abundance")
    frame.move_to([-1.9, -0.4, 0])
    shown = points[points["abundance"] <= top]
    dots = VGroup(*[Dot(axes.c2p(t, a), 0.045, color=GREY, fill_opacity=0.45)
                    for t, a in zip(shown["temperature_c"], shown["abundance"])])
    hidden = label(f"{len(points) - len(shown)} stations above {top} not shown", 22, SUBDUED)
    hidden.next_to(axes.c2p(17, top), DOWN + LEFT, 0.05).shift(0.1 * DOWN)
    line = shapes[shapes["model"] == "Linear regression"]
    tree = shapes[shapes["model"] == "Decision tree"]
    straight = polyline(axes, line["temperature_c"], line[".pred"], BLUE, 8)
    steps = polyline(axes, tree["temperature_c"], tree[".pred"], ORANGE, 8)
    tags = {"straight": VGroup(label("straight line:", 32, BLUE, weight=BOLD),
                               label("nearly flat", 32, BLUE, weight=BOLD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            "steps": VGroup(label("decision tree:", 32, ORANGE, weight=BOLD),
                            label("finds the hump", 32, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)}
    tags["straight"].next_to(axes.c2p(17, line[".pred"].iloc[-1]), RIGHT, 0.3)
    tags["steps"].next_to(axes.c2p(17, 9), RIGHT, 0.3)
    title_ = label(f"{len(points)} training stations", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.35)
    return frame, dots, hidden, straight, steps, tags, title_


class Scene13(VideoScene):
    number = 13

    def construct(self):
        frame, dots, hidden, straight, steps, tags, title_ = hump_layout(self)
        # "In the survey, the species does best in middling water."
        self.play(FadeIn(frame), FadeIn(title_), run_time=self.share(0.12))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003), FadeIn(hidden), run_time=self.share(0.3))
        # "A straight line through that hump is nearly flat, so the linear model reports no temperature effect."
        at(self, 0.45)
        self.play(Create(straight), FadeIn(tags["straight"]), run_time=self.share(0.25))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        frame, dots, hidden, straight, steps, tags, title_ = hump_layout(self)
        self.add(frame, dots, hidden, straight, tags["straight"], title_)
        # "A decision tree was never asked for a slope, and it finds the hump."
        self.play(Create(steps), run_time=self.share(0.5))
        self.play(FadeIn(tags["steps"]), run_time=self.share(0.15))
        self.finish()


class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Page results: the first five test stations as the page tabulates them, and the
        # RMSE built from all of them.
        misses = self.data("misses")
        steps = self.data("rmse-steps").iloc[0]
        widths = [2.0, 2.3, 2.0, 2.3]
        rows = [["observed", "predicted", "miss", "squared"]] + [
            [f"{r.observed:g}", f"{r.predicted:.2f}", f"{r.miss:.2f}".replace("-", "−"), f"{r.squared:.2f}"]
            for r in misses.itertuples()]
        cells = VGroup()
        for i, row in enumerate(rows):
            x = 0
            line = VGroup()
            for text, w in zip(row, widths):
                cell = label(text, 26 if i == 0 else 32, SUBDUED if i == 0 else INK, weight=BOLD if i == 0 else NORMAL)
                cell.move_to([x + w, -0.62 * i, 0], aligned_edge=RIGHT)
                line.add(cell)
                x += w
            cells.add(line)
        more = label(f"… and {steps.stations - len(misses):g} more stations", 26, SUBDUED).next_to(cells, DOWN, 0.35)
        grid_ = VGroup(cells, more).move_to([-2.6, -0.5, 0])
        columns = [VGroup(*[row[c] for row in cells]) for c in range(4)]
        columns[2][1:].set_color(VERMILION)
        columns[3][1:].set_color(PURPLE)
        mean_ = VGroup(label("mean of the squares", 30, SUBDUED),
                       label(f"{steps.mean_squared:.2f}", 44, PURPLE, weight=BOLD)).arrange(DOWN, buff=0.15)
        root = VGroup(label("square root", 30, SUBDUED),
                      label(f"{steps.rmse:.2f} animals", 44, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.15)
        VGroup(mean_, root).arrange(DOWN, buff=0.9).move_to([4.6, -0.3, 0])
        arrow = Arrow(mean_.get_bottom(), root.get_top(), color=GRID, stroke_width=5, buff=0.12)
        head = label("the tree on the held-back stations", 36, INK, weight=BOLD).to_edge(UP, buff=0.6)
        name = card("RMSE: a typical miss", ORANGE, 36).next_to(root, DOWN, 0.5)
        # "To compare the two, each one predicts the stations held back."
        self.play(FadeIn(head), FadeIn(columns[0]), FadeIn(columns[1]), FadeIn(more), run_time=self.share(0.14))
        # "At every station, take the miss: the observed count minus the predicted one."
        at(self, 0.18)
        self.play(LaggedStart(*[FadeIn(c, shift=0.15 * LEFT) for c in columns[2]], lag_ratio=0.12),
                  run_time=self.share(0.14))
        # "Square the misses, so that none cancel out,"
        at(self, 0.4)
        self.play(LaggedStart(*[FadeIn(c, shift=0.15 * LEFT) for c in columns[3]], lag_ratio=0.12),
                  run_time=self.share(0.12))
        # "average them,"
        at(self, 0.55)
        self.play(FadeIn(mean_, shift=0.2 * LEFT), run_time=self.share(0.06))
        # "and take the square root."
        at(self, 0.62)
        self.play(GrowArrow(arrow), FadeIn(root, shift=0.2 * DOWN), run_time=self.share(0.07))
        # "This is the root mean squared error, or RMSE: a typical miss, in animals."
        at(self, 0.72)
        self.play(FadeIn(name, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        # Page results: the test RMSE of each model, beside predicting the average.
        scores = self.data("test-rmse")
        colours = {"predicting the average": GREY, "straight line": BLUE, "decision tree": ORANGE}
        unit = 1.3   # scene units per animal
        left = -1.0
        bars = {}
        for i, r in enumerate(scores.itertuples()):
            y = 1.0 - 1.4 * i
            bar = Rectangle(width=r.rmse * unit, height=0.75, stroke_width=0, fill_color=colours[r.model],
                            fill_opacity=0.9).move_to([left, y, 0], aligned_edge=LEFT)
            name = label(r.model, 32, INK, weight=BOLD).next_to(bar, LEFT, 0.3)
            value = label(f"{r.rmse:.2f}", 36, colours[r.model], weight=BOLD)
            value.move_to([left + scores["rmse"].max() * unit + 0.3, y, 0], aligned_edge=LEFT)   # clear of the dashed line
            bars[r.model] = VGroup(bar, name, value)
        base = Line([left, 1.7, 0], [left, -3.2, 0], color=GRID, stroke_width=4)
        average = scores.loc[scores["model"] == "predicting the average", "rmse"].iloc[0]
        mark = DashedLine([left + average * unit, 1.75, 0], [left + average * unit, -2.4, 0],
                          color=SUBDUED, stroke_width=4)
        unit_ = label("test RMSE, animals per station", 26, SUBDUED).move_to([left + 3.0, -2.9, 0])
        head = label("lower is better", 44, INK, weight=BOLD).to_edge(UP, buff=0.6)
        learned = label("both beat the average, if not by much", 30, PURPLE, weight=BOLD)
        learned.next_to(mark, UP, 0.15).align_to(mark, RIGHT).shift(0.6 * RIGHT)
        # "Lower is better."
        self.play(FadeIn(head), Create(base), FadeIn(unit_), run_time=self.share(0.1))
        # "The tree's RMSE is 4.39 animals, the straight line's 4.59."
        at(self, 0.12)
        self.play(GrowFromEdge(bars["decision tree"][0], LEFT), FadeIn(bars["decision tree"][1:]),
                  run_time=self.share(0.12))
        at(self, 0.3)
        self.play(GrowFromEdge(bars["straight line"][0], LEFT), FadeIn(bars["straight line"][1:]),
                  run_time=self.share(0.1))
        # "Simply predicting the average count everywhere gives 4.72,"
        at(self, 0.45)
        self.play(GrowFromEdge(bars["predicting the average"][0], LEFT),
                  FadeIn(bars["predicting the average"][1:]), run_time=self.share(0.12))
        # "so both models have learned something, if not much."
        at(self, 0.66)
        self.play(Create(mark), FadeIn(learned), run_time=self.share(0.12))
        self.finish()


def cause_layout():
    """Schematic: depth drives both salinity and the species, as on the prediction and
    explanation page's diagram; salinity itself causes nothing."""
    depth = card("depth", GREEN, 38).move_to([0, 1.5, 0])
    salinity = card("salinity", SKY, 38).move_to([-4.2, -0.8, 0])
    species = card("the species", ORANGE, 38).move_to([4.2, -0.8, 0])
    drives = VGroup(Arrow(depth.get_bottom(), salinity.get_top(), color=INK, stroke_width=5, buff=0.15),
                    Arrow(depth.get_bottom(), species.get_top(), color=INK, stroke_width=5, buff=0.15))
    link = DashedLine(salinity.get_right(), species.get_left(), color=PURPLE, stroke_width=6, buff=0.2)
    predicts = label("helps predict", 30, PURPLE, weight=BOLD).next_to(link, UP, 0.35)
    cross = Cross(Square(0.4), stroke_color=VERMILION, stroke_width=8).move_to(link)
    nothing = label("but causes nothing", 30, VERMILION, weight=BOLD).next_to(link, DOWN, 0.3)
    title_ = label("predicting is not explaining", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
    return depth, salinity, species, drives, link, predicts, cross, nothing, title_


class Scene17(VideoScene):
    number = 17

    def construct(self):
        depth, salinity, species, drives, link, predicts, cross, nothing, title_ = cause_layout()
        # "Predicting and explaining are different jobs, too."
        self.play(FadeIn(title_), run_time=self.share(0.1))
        # "A variable can help predict without causing anything. In the survey, salinity
        # helps predict the species,"
        at(self, 0.3)
        self.play(FadeIn(salinity), FadeIn(species), run_time=self.share(0.08))
        self.play(Create(link), FadeIn(predicts), run_time=self.share(0.1))
        # "but only because it rises with depth,"
        at(self, 0.62)
        self.play(FadeIn(depth, shift=0.2 * DOWN), GrowArrow(drives[0]), run_time=self.share(0.1))
        # "and depth is what the species responds to."
        at(self, 0.8)
        self.play(GrowArrow(drives[1]), run_time=self.share(0.08))
        self.play(Create(cross), FadeIn(nothing), run_time=self.share(0.08))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        depth, salinity, species, drives, link, predicts, cross, nothing, title_ = cause_layout()
        self.add(depth, salinity, species, drives, link, predicts, cross, nothing, title_)
        warn = card("a good test error gives no warning", VERMILION, 34).to_edge(UP, buff=0.3)
        needs = VGroup(label("explaining needs a study design", 30, PURPLE, weight=BOLD),
                       label("and knowledge of the system", 30, PURPLE, weight=BOLD)).arrange(DOWN, buff=0.1)
        needs.move_to([0, -2.6, 0])
        later = label("more on this later in the course", 26, SUBDUED).move_to([0, -3.5, 0])
        # "A good test error gives no warning of this."
        self.play(FadeOut(title_), FadeIn(warn, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "Explaining needs a study design and knowledge of the system,"
        at(self, 0.3)
        self.play(FadeIn(needs, shift=0.2 * UP), run_time=self.share(0.12))
        # "and the course comes back to these ideas as it goes."
        at(self, 0.7)
        self.play(FadeIn(later), run_time=self.share(0.1))
        self.finish()


class Scene19(KeyPointScene):
    number, point = 19, 2


# Machine learning in marine science (scenes 20–24) ------------------------------------------

TASKS = [("Naming things", "classification", ORANGE), ("Mapping across space", "regression or classification", BLUE),
         ("Filling gaps", "regression", BLUE), ("Forecasting", "regression", BLUE),
         ("Finding groups", "unsupervised", GREEN), ("Standing in for a model", "regression", BLUE)]


def tasks_layout():
    cards = VGroup()
    for name, kind, colour in TASKS:
        box = RoundedRectangle(width=4.3, height=1.9, corner_radius=0.15, stroke_color="#1b6a87", stroke_width=3,
                               fill_color="#f4f8fa", fill_opacity=1)
        strip = Rectangle(width=4.3, height=0.12, stroke_width=0, fill_color=colour, fill_opacity=1).align_to(box, UP)
        words = VGroup(label(name, 30, INK, weight=BOLD), label(kind, 24, SUBDUED)).arrange(DOWN, buff=0.15)
        cards.add(VGroup(box, strip, words.move_to(box)))
    cards.arrange_in_grid(2, 3, buff=(0.3, 0.4)).move_to([0, -0.4, 0])
    head = label("six tasks cover most applications", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
    return head, cards


def warning_mark():
    tri = Triangle(color=VERMILION, fill_color=VERMILION, fill_opacity=1, stroke_width=0).scale(0.28)
    return VGroup(tri, label("!", 30, BACKGROUND, weight=BOLD).move_to(tri.get_center() + 0.05 * DOWN))


class Scene20(VideoScene):
    number = 20

    def construct(self):
        head, cards = tasks_layout()
        # "Most marine applications come down to six tasks: naming things, ... and standing in for a slow model."
        self.play(FadeIn(head), run_time=self.share(0.1))
        at(self, 0.25)
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cards], lag_ratio=0.6), run_time=self.share(0.65))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        head, cards = tasks_layout()
        self.add(head, cards)
        marks = VGroup(*[warning_mark().move_to(c[0].get_corner(UR) + [-0.1, 0.0, 0]) for c in cards])
        note = card("each has a typical way of going wrong", VERMILION, 32).to_edge(DOWN, buff=0.3)
        # "Each has a typical way of going wrong,"
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in marks], lag_ratio=0.15), run_time=self.share(0.3))
        self.play(FadeIn(note, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


def pipeline_layout():
    stages = [("data you have", "plentiful", BLUE),
              ("expert labels", "slow and costly", ORANGE),
              ("the model learns", "from the labelled few", PURPLE),
              ("used at scale", "on everything else", GREEN)]
    boxes = VGroup()
    for name, note, colour in stages:
        words = VGroup(label(name, 30, colour, weight=BOLD), label(note, 24, SUBDUED)).arrange(DOWN, buff=0.12)
        box = RoundedRectangle(width=max(words.width + 0.4, 2.6), height=1.5, corner_radius=0.2, stroke_color=colour, stroke_width=4)
        boxes.add(VGroup(box, words.move_to(box)))
    boxes.arrange(RIGHT, buff=0.5)
    if boxes.width > 13.4:
        boxes.scale_to_fit_width(13.4)
    boxes.move_to([0, 1.3, 0])
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), color=INK, stroke_width=4, buff=0.08)
                      for a, b in zip(boxes[:-1], boxes[1:])])
    return boxes, arrows


class Scene22(VideoScene):
    number = 22

    def construct(self):
        # Schematic: the applications page's pipeline.
        boxes, arrows = pipeline_layout()
        few = label("a few labels, predictions for everything else", 34, INK, weight=BOLD)
        few.move_to([0, -1.2, 0])
        # "Most of the six are supervised, and the answers usually come from a specialist: slow and costly."
        self.play(FadeIn(boxes[0]), run_time=self.share(0.12))
        at(self, 0.25)
        self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]), run_time=self.share(0.15))
        # "A model turns those few labels into predictions for everything else."
        at(self, 0.6)
        self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]), run_time=self.share(0.1))
        self.play(GrowArrow(arrows[2]), FadeIn(boxes[3]), run_time=self.share(0.1))
        self.play(FadeIn(few, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        # Schematic: a cloud of cases, and the labelled few bunched in one corner of it.
        boxes, arrows = pipeline_layout()
        self.add(boxes, arrows)
        rng = np.random.default_rng(21)
        cloud = rng.uniform([-3.2, -3.6], [3.2, -0.9], (160, 2))
        dots = VGroup(*[Dot([x, y, 0], 0.06, color=GREY, fill_opacity=0.6) for x, y in cloud])
        labelled = [i for i, (x, y) in enumerate(cloud) if x < -1.6 and y > -2.2][:14]
        warn = card("not a random sample", VERMILION, 28).move_to([-4.9, -1.0, 0])
        # "But the labelled examples are rarely a random sample,"
        self.play(Indicate(boxes[1], color=ORANGE, scale_factor=1.05), FadeIn(dots), run_time=self.share(0.25))
        self.play(*[dots[i].animate.set_color(ORANGE).scale(1.6) for i in labelled], run_time=self.share(0.15))
        self.play(FadeIn(warn), run_time=self.share(0.1))
        # "and the model inherits their gaps."
        at(self, 0.65)
        self.play(*[d.animate.set_color(GREEN) for i, d in enumerate(dots) if i not in labelled], run_time=self.share(0.2))
        self.finish()


class Scene24(KeyPointScene):
    number, point = 24, 3


# The quiz (scenes 25–26) ------------------------------------------------------------------

class Scene25(QuizScene):
    number = 25
    question = ("Seabed photographs, some named", "by a specialist.",
                "Supervised or unsupervised?", "Which of the six tasks?")


class Scene26(VideoScene):
    number = 26

    def construct(self):
        # Schematic: photos, some carrying a name; the naming-things card.
        rng = np.random.default_rng(24)
        photos = VGroup(*[RoundedRectangle(width=1.1, height=0.8, corner_radius=0.08, stroke_color=SUBDUED, stroke_width=3,
                                           fill_color=interpolate_color(ManimColor(SKY), ManimColor(BLUE), float(rng.uniform())),
                                           fill_opacity=0.7) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.15)
        photos.move_to([-3.8, -0.6, 0])
        named = VGroup(*[Dot(photos[i].get_corner(UR) + [-0.15, -0.15, 0], 0.1, color=ORANGE) for i in (0, 4, 7)])
        some = label("some named", 30, ORANGE, weight=BOLD).next_to(photos, UP, 0.3)
        answer = label("Supervised", 56, ORANGE, weight=BOLD).to_edge(UP, buff=0.5)
        head, cards = tasks_layout()
        task = cards[0].copy().scale(1.1).move_to([3.4, -0.6, 0])
        arrow = Arrow(photos.get_right(), task.get_left(), color=INK, stroke_width=5, buff=0.3)
        # "Supervised, because some photographs come with answers."
        self.play(FadeIn(answer), FadeIn(photos), run_time=self.share(0.2))
        self.play(FadeIn(named, scale=0.5), FadeIn(some), run_time=self.share(0.12))
        # "The task is naming things: a classification."
        at(self, 0.5)
        self.play(GrowArrow(arrow), FadeIn(task, shift=0.2 * LEFT), run_time=self.share(0.15))
        self.finish()


# The recap (scenes 27–29) and the end card (scene 30) --------------------------------------

class Scene27(RecapScene):
    number, point = 27, 1


class Scene28(RecapScene):
    number, point = 28, 2


class Scene29(RecapScene):
    number, point = 29, 3


class Scene30(EndCardScene):
    number = 30
