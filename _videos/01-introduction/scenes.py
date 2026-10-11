"""Manim scenes for the introduction video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/01-introduction
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is an overview of the section: a short tour of its four pages. Scenes marked
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
            "Predicting is not explaining",
            "Where it helps in marine science"]
ANSWERS = ["Answers or none:\nsupervised or\nunsupervised",
           "Different jobs, checked\ndifferently: decide first\nto predict or to explain",
           "Six tasks, each\nlimited by its labels"]
RECAP = ["Your data decide the kind of learning",
         "Decide first: predict or explain",
         "Six tasks, limited by their labels"]


class Scene01(LearnScene):
    number = 1
    times = (0.53, 0.62, 0.8)


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
        # Schematic: a trained model; new data in, a prediction out.
        inputs = VGroup(*[card(t, SKY, 30) for t in ["temperature", "salinity", "depth"]]
                        ).arrange(DOWN, buff=0.25).move_to([-4.6, 0.2, 0])
        unseen = label("new data", 30, SUBDUED, weight=BOLD).next_to(inputs, UP, 0.35)
        box = RoundedRectangle(width=3.4, height=2.2, corner_radius=0.25, stroke_color=INK, stroke_width=5,
                               fill_color=GRID, fill_opacity=0.5).move_to([0, 0.2, 0])
        name = VGroup(label("a trained", 40, INK, weight=BOLD), label("model", 40, INK, weight=BOLD)
                      ).arrange(DOWN, buff=0.1).move_to(box)
        fitted = label("trained on examples with answers", 28, SUBDUED).next_to(box, DOWN, 0.3)
        output = card("a prediction", GREEN, 38).move_to([4.6, 0.2, 0])
        arrow_in = Arrow(inputs.get_right(), box.get_left(), color=INK, stroke_width=5, buff=0.2)
        arrow_out = Arrow(box.get_right(), output.get_left(), color=INK, stroke_width=5, buff=0.2)
        course = card("this course: build models well, and avoid the pitfalls", PURPLE, 32).to_edge(DOWN, buff=0.5)
        # "Machine learning trains a model on examples whose answers we already know."
        at(self, 0.08)
        self.play(FadeIn(box), FadeIn(name), FadeIn(fitted), run_time=self.share(0.12))
        # "Once trained, the model takes new data as its input,"
        at(self, 0.27)
        self.play(FadeIn(inputs), FadeIn(unseen), GrowArrow(arrow_in), run_time=self.share(0.15))
        # "Its output is a prediction for that station."
        at(self, 0.56)
        self.play(GrowArrow(arrow_out), FadeIn(output, shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "In this course, we learn how to build these models well, ..."
        at(self, 0.68)
        self.play(FadeIn(course, shift=0.2 * UP), run_time=self.share(0.1))
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
        # "In supervised learning, when the answer is a quantity, ... the task is regression."
        at(self, 0.2)
        self.play(GrowArrow(arrows[0]), FadeIn(quantity), run_time=self.share(0.15))
        self.play(FadeIn(reg, shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "When it is a category, such as present or absent, it is classification."
        at(self, 0.62)
        self.play(GrowArrow(arrows[1]), FadeIn(category), run_time=self.share(0.15))
        at(self, 0.88)
        self.play(FadeIn(cls, shift=0.2 * RIGHT), run_time=self.share(0.08))
        self.finish()


# Supervised: k-nearest neighbours (scenes 7–8) ----------------------------------------------

FOUND, NOT_FOUND = BLUE, ORANGE


def neighbours_layout(scene):
    """The stations by depth and temperature, a new mid-depth station, and its 15 nearest
    stations, found on the classifier's scaled temperature, salinity and depth."""
    stations = scene.data("neighbours")
    new = scene.data("new-stations").set_index("station").loc["mid-depth"]
    axes, frame = chart([0, 200, 50], [2, 16, 2], 6.8, 5.0, [0, 50, 100, 150, 200], [4, 8, 12, 16],
                        "depth (m)", "temperature (°C)")
    frame.move_to([-3.0, -0.3, 0])
    grey = VGroup(*[Dot(axes.c2p(d, t), 0.035, color=GREY, fill_opacity=0.45)
                    for d, t in zip(stations["depth_m"], stations["temperature_c"])])
    near = stations[stations["neighbour"]]
    picked = VGroup(*[Dot(axes.c2p(d, t), 0.07, color=PURPLE)
                      for d, t in zip(near["depth_m"], near["temperature_c"])])
    star = Star(5, outer_radius=0.2, color=INK, fill_color=YELLOW, fill_opacity=1, stroke_width=3
                ).move_to(axes.c2p(new["depth_m"], new["temperature_c"])).set_z_index(10)   # always on top
    star_name = plated(label("a new station", 28, INK, weight=BOLD)).next_to(star, UP + RIGHT, 0.25)
    ring = Circle(radius=0.75, color=PURPLE, stroke_width=4).move_to(picked)
    found = [p == "yes" for p in near["present"]]
    return axes, frame, grey, picked, star, star_name, ring, found, new


class Scene07(VideoScene):
    number = 7

    def construct(self):
        axes, frame, grey, picked, star, star_name, ring, found, new = neighbours_layout(self)
        head = label("k-nearest neighbours", 40, INK, weight=BOLD).to_edge(UP, buff=0.35)
        aim = VGroup(label("aim: is the species", 30, INK, weight=BOLD),
                     label("present at the star?", 30, INK, weight=BOLD)).arrange(DOWN, buff=0.1)
        fifteen = label("the 15 most similar", 32, PURPLE, weight=BOLD)
        note = VGroup(label("in temperature, salinity", 28, SUBDUED),
                      label("and depth, not on a map", 28, SUBDUED)).arrange(DOWN, buff=0.1)
        answers = card("their answers are known", BLUE, 28)
        VGroup(aim, fifteen, note, answers).arrange(DOWN, buff=0.45).move_to([4.2, -0.2, 0])
        # "Let's look at one of the simplest supervised methods, k-nearest neighbours."
        self.play(FadeIn(head), FadeIn(frame), FadeIn(grey), run_time=self.share(0.14))
        # "Here, its aim is to predict whether the species is present at a new station, marked by the star,"
        at(self, 0.2)
        self.play(GrowFromCenter(star), FadeIn(star_name), FadeIn(aim), run_time=self.share(0.1))
        # "It does this from the neighbours: the fifteen survey stations most like the new one ..."
        at(self, 0.45)
        self.play(FadeIn(picked, scale=1.5), Create(ring), FadeIn(fifteen), run_time=self.share(0.12))
        # "Nearest means most similar in the water, not closest on a map."
        at(self, 0.69)
        self.play(FadeIn(note), run_time=self.share(0.08))
        # "The neighbours come with answers, ..."
        at(self, 0.82)
        self.play(FadeIn(answers, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene08(VideoScene):
    number = 8

    def construct(self):
        axes, frame, grey, picked, star, star_name, ring, found, new = neighbours_layout(self)
        head = label("k-nearest neighbours", 40, INK, weight=BOLD).to_edge(UP, buff=0.35)
        self.add(head, frame, grey, picked, ring, star, star_name)
        tokens = VGroup(*[Dot(radius=0.16, color=FOUND if f else NOT_FOUND) for f in found])
        tokens.arrange_in_grid(3, 5, buff=0.22).move_to([4.2, 2.7, 0])
        keys = VGroup(VGroup(Dot(radius=0.1, color=FOUND), label("found", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
                      VGroup(Dot(radius=0.1, color=NOT_FOUND), label("not found", 26, SUBDUED)).arrange(RIGHT, buff=0.15)
                      ).arrange(RIGHT, buff=0.5).next_to(tokens, DOWN, 0.3)
        share = label(f"{sum(found)} of {len(found)} found", 36, INK, weight=BOLD).next_to(keys, DOWN, 0.35)
        chance = card(f"{round(100 * new['.pred_yes'])}% chance of presence", GREEN, 28).next_to(share, DOWN, 0.3)
        confidence = label("a kind of confidence", 26, SUBDUED).next_to(chance, DOWN, 0.15)
        kind = VGroup(label("present or absent:", 28, INK, weight=BOLD),
                      label("a classification", 28, GREEN, weight=BOLD)).arrange(DOWN, buff=0.08)
        cutoff = label("above a cut-off: yes or no", 26, SUBDUED)
        counts = VGroup(label("abundance: their average count", 28, INK, weight=BOLD),
                        label("a regression", 28, BLUE, weight=BOLD)).arrange(DOWN, buff=0.08)
        VGroup(VGroup(kind, cutoff).arrange(DOWN, buff=0.12), counts).arrange(DOWN, buff=0.3
                                                                          ).next_to(confidence, DOWN, 0.3)
        # "Eleven of those fifteen neighbours had the species."
        self.play(ReplacementTransform(picked.copy(), tokens), FadeIn(keys), run_time=self.share(0.08))
        self.play(FadeIn(share), run_time=self.share(0.04))
        # "So the model predicts a seventy-three percent chance of presence: a kind of confidence ..."
        at(self, 0.14)
        self.play(FadeIn(chance, shift=0.2 * UP), run_time=self.share(0.06))
        at(self, 0.26)
        self.play(FadeIn(confidence), run_time=self.share(0.05))
        # "This is a classification, because the answer is a category: present or absent."
        at(self, 0.47)
        self.play(FadeIn(kind), run_time=self.share(0.05))
        # "To get a plain yes or no, choose a cut-off, and call the species present above it."
        at(self, 0.63)
        self.play(FadeIn(cutoff), run_time=self.share(0.04))
        # "The same method can also do regression: to predict abundance, it averages the neighbours' counts instead."
        at(self, 0.8)
        self.play(FadeIn(counts), run_time=self.share(0.06))
        self.finish()


# Unsupervised, and what a model learns (scenes 9–11) ------------------------------------------

GROUP_COLOURS = {"Shallow": ORANGE, "Mid-depth": GREEN, "Deep": BLUE}


class Scene09(VideoScene):
    number = 9

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
        names_alike = VGroup(
            VGroup(label("k-nearest neighbours:", 32, INK, weight=BOLD), label("supervised", 32, BLUE, weight=BOLD)
                   ).arrange(RIGHT, buff=0.2),
            VGroup(label("k-means:", 32, INK, weight=BOLD), label("unsupervised", 32, PURPLE, weight=BOLD)
                   ).arrange(RIGHT, buff=0.2)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.35)
        # "Now for unsupervised learning, where the examples have no answers at all."
        self.play(FadeIn(frame), FadeIn(grey), FadeIn(note), run_time=self.share(0.12))
        # "A common method is k-means. Its name sounds like k-nearest neighbours, but ..."
        at(self, 0.35)
        self.play(FadeIn(names_alike[0]), run_time=self.share(0.05))
        at(self, 0.5)
        self.play(FadeIn(names_alike[1]), run_time=self.share(0.05))
        # "In this example, k-means sorted all 800 stations into three groups, ..."
        at(self, 0.63)
        self.play(FadeOut(names_alike), FadeIn(head), Transform(grey, coloured), run_time=self.share(0.12))
        # "Looking at the groups afterwards, we named them shallow, mid-depth and deep."
        at(self, 0.85)
        self.play(LaggedStart(*[FadeIn(n, shift=0.2 * RIGHT) for n in names], lag_ratio=0.4), run_time=self.share(0.12))
        self.finish()


class Scene10(VideoScene):
    number = 10

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
        k_is = card("k: the number of groups, which we choose", INK, 32).to_edge(DOWN, buff=0.4)
        unknown = card("the best k is usually unknown", VERMILION, 32).to_edge(DOWN, buff=0.4)
        # "Unsupervised learning often needs extra information from us."
        self.play(FadeIn(head), FadeIn(dots), run_time=self.share(0.12))
        # "The k in k-means is the number of groups, and we chose three,"
        at(self, 0.2)
        self.play(FadeIn(k_is, shift=0.2 * UP), run_time=self.share(0.06))
        # "but the best number is usually unknown."
        at(self, 0.41)
        self.play(FadeOut(k_is), FadeIn(unknown, shift=0.2 * UP), run_time=self.share(0.06))
        # "k-means returns as many groups as we ask for, ...: ask for six, and six appear."
        at(self, 0.79)
        self.play(ReplacementTransform(head, head6),
                  *[d.animate.set_color(palette[six[i]]) for i, d in enumerate(dots)], run_time=self.share(0.15))
        # "So its results need checking."
        at(self, 0.9)
        self.play(FadeOut(unknown), FadeIn(check, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


def two_groups(rng, centre, spread, n):
    return centre + rng.normal(0, 1, (n, 2)) * spread


def triangle(point, colour=ORANGE, size=0.14):
    return Triangle(color=colour, fill_color=colour, fill_opacity=1, stroke_width=0).scale(size).move_to(point)


class Scene11(VideoScene):
    number = 11

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
        course = card("this course: mostly discriminative models", GREEN, 30).to_edge(DOWN, buff=0.1)
        what = label("not how a model learns, but what it produces", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.2)
        # "Models also differ in another way."
        self.play(FadeIn(panels[0][2]), FadeIn(panels[1][2]), FadeIn(panels[0][0]), FadeIn(panels[1][0]),
                  run_time=self.share(0.07))
        # "This is not about how a model learns, but about what it produces."
        at(self, 0.08)
        self.play(FadeIn(what), run_time=self.share(0.06))
        # "A discriminative model, such as k-nearest neighbours, learns only the answer: here, the boundary ..."
        at(self, 0.22)
        self.play(FadeIn(panels[0][1]), run_time=self.share(0.06))
        at(self, 0.38)
        self.play(Create(boundary), run_time=self.share(0.1))
        # "A generative model learns what the data themselves look like, so it can invent new examples."
        at(self, 0.54)
        self.play(FadeIn(panels[1][1]), FadeIn(blobs), run_time=self.share(0.1))
        at(self, 0.67)
        self.play(GrowFromCenter(new), FadeIn(new_name), GrowArrow(new_arrow), run_time=self.share(0.06))
        # "The tools that write text and draw pictures are generative."
        at(self, 0.75)
        self.play(FadeIn(tools, shift=0.2 * UP), run_time=self.share(0.06))
        # "This basic course focuses mostly on discriminative models."
        at(self, 0.87)
        self.play(FadeOut(tools), FadeIn(course, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


class Scene12(KeyPointScene):
    number, point = 12, 1


# Predicting and explaining (scenes 13–21) --------------------------------------------------

def aims_layout():
    """Schematic: the two aims side by side, coloured as on the prediction and explanation
    page's diagram."""
    cols = VGroup()
    for name, colour, lines in [("Prediction", ORANGE, ["the outcome at a new station,", "checked on stations held back"]),
                                ("Explanation", GREEN, ["what drives the outcome"])]:
        box = RoundedRectangle(width=6.0, height=3.4, corner_radius=0.2, stroke_color=colour, stroke_width=5)
        strip = Rectangle(width=6.0, height=0.14, stroke_width=0, fill_color=colour, fill_opacity=1).align_to(box, UP)
        head = label(name, 42, INK, weight=BOLD)
        body = VGroup(*[label(t, 30, INK) for t in lines]).arrange(DOWN, buff=0.15)
        VGroup(head, body).arrange(DOWN, buff=0.45).move_to(box)
        cols.add(VGroup(box, strip, head, body))
    cols.arrange(RIGHT, buff=0.5).move_to([0, 0.1, 0])
    title_ = label("one model, two aims", 42, PURPLE, weight=BOLD).to_edge(UP, buff=0.5)
    usual = VGroup(*[label(f"usual aim of {who}", 30, colour, weight=BOLD).next_to(col, DOWN, 0.3)
                     for who, colour, col in [("machine learning", ORANGE, cols[0]),
                                              ("statistical modelling", GREEN, cols[1])]])
    return title_, cols, usual


class Scene13(VideoScene):
    number = 13

    def construct(self):
        title_, cols, usual = aims_layout()
        predict_body = cols[0][3]
        # "A model can serve two aims."
        self.play(FadeIn(title_), run_time=self.share(0.1))
        # "Prediction asks what the outcome will be at a station nobody has measured,"
        at(self, 0.12)
        self.play(FadeIn(cols[0][:3]), FadeIn(predict_body[0], shift=0.2 * UP), run_time=self.share(0.12))
        # "and it can be checked on stations held back from fitting."
        at(self, 0.5)
        self.play(FadeIn(predict_body[1], shift=0.2 * UP), run_time=self.share(0.1))
        # "Explanation asks what drives the outcome."
        at(self, 0.78)
        self.play(FadeIn(cols[1], shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene14(VideoScene):
    number = 14

    def construct(self):
        title_, cols, usual = aims_layout()
        self.add(title_, cols)
        checked = card("the same model, checked in different ways", PURPLE, 30).to_edge(DOWN, buff=0.35)
        # "Machine learning usually aims at prediction,"
        self.play(FadeIn(usual[0], shift=0.2 * UP), run_time=self.share(0.12))
        # "and statistical modelling at explanation."
        at(self, 0.3)
        self.play(FadeIn(usual[1], shift=0.2 * UP), run_time=self.share(0.12))
        # "The same model can serve either, but it is checked in different ways."
        at(self, 0.6)
        self.play(FadeIn(checked, shift=0.2 * UP), run_time=self.share(0.12))
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
    hidden = plated(label(f"{len(points) - len(shown)} stations above {top} not shown", 24, SUBDUED))
    hidden.next_to(axes.c2p(17, top), DOWN + LEFT, 0.05)
    line = shapes[shapes["model"] == "Linear regression"]
    tree = shapes[shapes["model"] == "Decision tree"]
    straight = polyline(axes, line["temperature_c"], line[".pred"], BLUE, 8)
    steps = polyline(axes, tree["temperature_c"], tree[".pred"], ORANGE, 8)
    tags = {"straight": VGroup(label("linear regression:", 32, BLUE, weight=BOLD),
                               label("nearly flat", 32, BLUE, weight=BOLD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            "steps": VGroup(label("decision tree:", 32, ORANGE, weight=BOLD),
                            label("finds the hump", 32, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)}
    tags["straight"].next_to(axes.c2p(17, line[".pred"].iloc[-1]), RIGHT, 0.3)
    tags["steps"].next_to(axes.c2p(17, 9), RIGHT, 0.3)
    title_ = label(f"{len(points)} training stations", 30, SUBDUED, weight=BOLD).to_edge(UP, buff=0.35)
    return frame, dots, hidden, straight, steps, tags, title_


class Scene15(VideoScene):
    number = 15

    def construct(self):
        frame, dots, hidden, straight, steps, tags, title_ = hump_layout(self)
        # "Here is an example of how predictions are evaluated, using two models."
        self.play(FadeIn(frame), FadeIn(title_), run_time=self.share(0.1))
        # "In the survey, the species does best in middling water, neither too cold nor too warm."
        at(self, 0.23)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003), FadeIn(hidden), run_time=self.share(0.25))
        # "The first model, a linear regression, fits a straight line. Through that hump, the line is nearly flat, ..."
        at(self, 0.55)
        self.play(Create(straight), run_time=self.share(0.15))
        at(self, 0.72)
        self.play(FadeIn(tags["straight"]), run_time=self.share(0.08))
        self.finish()


class Scene16(VideoScene):
    number = 16

    def construct(self):
        frame, dots, hidden, straight, steps, tags, title_ = hump_layout(self)
        self.add(frame, dots, hidden, straight, tags["straight"], title_)
        kind = label("a supervised model", 28, PURPLE, weight=BOLD)
        later = VGroup(label("explained later", 26, SUBDUED),
                       label("in the course", 26, SUBDUED)).arrange(DOWN, buff=0.08)
        words = VGroup(kind, later).arrange(DOWN, buff=0.2)
        box = SurroundingRectangle(words, color=PURPLE, buff=0.25, corner_radius=0.15)
        VGroup(box, words).next_to(tags["steps"], UP, 0.6, aligned_edge=LEFT)
        # "The second model, a decision tree, works differently. It splits the stations in two, ..."
        at(self, 0.11)
        self.play(Create(steps), run_time=self.share(0.3))
        # "It was never asked for a straight line, and it finds the hump."
        at(self, 0.48)
        self.play(FadeIn(tags["steps"]), run_time=self.share(0.06))
        # "Like k-nearest neighbours, a decision tree is a supervised model: ..."
        at(self, 0.6)
        self.play(Create(box), FadeIn(kind), run_time=self.share(0.06))
        # "We learn how decision trees work later in the course, ..."
        at(self, 0.82)
        self.play(FadeIn(later), run_time=self.share(0.06))
        self.finish()


class Scene17(VideoScene):
    number = 17

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
        # "To compare the two, each one predicts stations that were held back, ..."
        self.play(FadeIn(head), FadeIn(columns[0]), FadeIn(columns[1]), FadeIn(more), run_time=self.share(0.14))
        # "At every station, take the miss: the observed count minus the predicted one."
        at(self, 0.34)
        self.play(LaggedStart(*[FadeIn(c, shift=0.15 * LEFT) for c in columns[2]], lag_ratio=0.12),
                  run_time=self.share(0.1))
        # "Square the misses, so that none cancel out,"
        at(self, 0.56)
        self.play(LaggedStart(*[FadeIn(c, shift=0.15 * LEFT) for c in columns[3]], lag_ratio=0.12),
                  run_time=self.share(0.1))
        # "average them,"
        at(self, 0.68)
        self.play(FadeIn(mean_, shift=0.2 * LEFT), run_time=self.share(0.06))
        # "and take the square root."
        at(self, 0.72)
        self.play(GrowArrow(arrow), FadeIn(root, shift=0.2 * DOWN), run_time=self.share(0.07))
        # "This is the root mean squared error, or RMSE: a typical miss, in animals."
        at(self, 0.79)
        self.play(FadeIn(name, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        # Page results: the test RMSE of each model, beside predicting the average.
        scores = self.data("test-rmse")
        colours = {"predicting the average": GREY, "linear regression": BLUE, "decision tree": ORANGE}
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
        # "The tree's RMSE is 4.39 animals, the linear regression's 4.59."
        at(self, 0.12)
        self.play(GrowFromEdge(bars["decision tree"][0], LEFT), FadeIn(bars["decision tree"][1:]),
                  run_time=self.share(0.12))
        at(self, 0.3)
        self.play(GrowFromEdge(bars["linear regression"][0], LEFT), FadeIn(bars["linear regression"][1:]),
                  run_time=self.share(0.1))
        # "Simply predicting the average count everywhere, the baseline, gives 4.72,"
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


class Scene19(VideoScene):
    number = 19

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


class Scene20(VideoScene):
    number = 20

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


class Scene21(KeyPointScene):
    number, point = 21, 2


# Machine learning in marine science (scenes 22–26) ------------------------------------------

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


class Scene22(VideoScene):
    number = 22

    def construct(self):
        head, cards = tasks_layout()
        # "Most marine applications come down to six tasks: naming things, ... and standing in for a slow model."
        self.play(FadeIn(head), run_time=self.share(0.08))
        at(self, 0.15)
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cards], lag_ratio=0.6), run_time=self.share(0.4))
        # "Each task tends to have its own suitable ways of building models, ..."
        ways = card("each task has its own suitable ways of building models", PURPLE, 30).to_edge(DOWN, buff=0.3)
        at(self, 0.57)
        self.play(FadeIn(ways, shift=0.2 * UP), run_time=self.share(0.08))
        at(self, 0.72)
        self.play(LaggedStart(*[Indicate(c[2][1], color=PURPLE, scale_factor=1.15) for c in cards], lag_ratio=0.15),
                  run_time=self.share(0.2))
        self.finish()


class Scene23(VideoScene):
    number = 23

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


class Scene24(VideoScene):
    number = 24

    def construct(self):
        # Schematic: the applications page's pipeline.
        boxes, arrows = pipeline_layout()
        few = label("a few labels, predictions for everything else", 34, INK, weight=BOLD)
        few.move_to([0, -1.2, 0])
        # "Most of the six are supervised, so they need answers, which machine learning calls labels."
        self.play(FadeIn(boxes[0]), run_time=self.share(0.1))
        # "The labels usually come from a specialist, which is slow and costly."
        at(self, 0.3)
        self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]), run_time=self.share(0.12))
        # "A model trained on those few labels can then predict for everything else."
        at(self, 0.69)
        self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]), run_time=self.share(0.08))
        self.play(GrowArrow(arrows[2]), FadeIn(boxes[3]), run_time=self.share(0.08))
        self.play(FadeIn(few, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene25(VideoScene):
    number = 25

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


class Scene26(KeyPointScene):
    number, point = 26, 3


# The quiz (scenes 27–28) ------------------------------------------------------------------

class Scene27(QuizScene):
    number = 27
    question = ("Seabed photographs, some named", "by a specialist.",
                "Supervised or unsupervised?", "Which of the six tasks?")


class Scene28(VideoScene):
    number = 28

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


# The recap (scenes 29–31) and the end card (scene 32) --------------------------------------

class Scene29(RecapScene):
    number, point = 29, 1


class Scene30(RecapScene):
    number, point = 30, 2


class Scene31(RecapScene):
    number, point = 31, 3


class Scene32(EndCardScene):
    number = 32
