"""Manim scenes for the marine data video. One class per script scene: Scene08 is "## Scene 8".

    cd _videos/02-marine-data
    manim -ql scenes.py Scene08                      # draft
    manim -qh --frame_rate 30 -a scenes.py           # all, 1080p, for the rough cut

The video is an overview of the section: a short tour of its pages. Scenes marked
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


PROMISES = ["What the survey records",
            "Finding the problems in a raw file",
            "Testing a model honestly"]
ANSWERS = ["Know what one row is,\nand how many are\nreally independent",
           "Look before you model:\neach fix is a decision,\nkept in a recipe",
           "Split along what you\nwill predict for, and keep\nthe test data untouched"]
RECAP = ["Rows are not all independent",
         "Look first; every fix is a decision",
         "Split along what you will predict for"]


class Scene01(LearnScene):
    number = 1
    times = (0.48, 0.61, 0.81)


def plain_axes(x_range, y_range, x_length, y_length):
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
                tips=False, axis_config={"color": GRID, "include_ticks": False, "stroke_width": 3})


def card(text, colour=PURPLE, size=40):
    words = label(text, size, colour, weight=BOLD)
    box = SurroundingRectangle(words, color=colour, buff=0.3, corner_radius=0.15, fill_color=BACKGROUND,
                               fill_opacity=0.95)
    return VGroup(box, words)


def panel(heading, lines, colour, width=3.0, height=2.4, size=26):
    """A card in the diagrams' house style: pale fill, a coloured strip along the top."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color="#1b6a87",
                           stroke_width=3, fill_color="#f4f8fa", fill_opacity=1)
    strip = Rectangle(width=width, height=0.12, stroke_width=0, fill_color=colour, fill_opacity=1).align_to(box, UP)
    words = VGroup(label(heading, size + 6, INK, weight=BOLD),
                   *[label(t, size, SUBDUED) for t in lines]).arrange(DOWN, buff=0.15)
    return VGroup(box, strip, words.move_to(box))


def at(scene, fraction):
    """Wait until this fraction of the narration."""
    scene.wait(max(scene.share(fraction) - scene.time, 0.01))


# The survey (scenes 2–7) ----------------------------------------------------------------

class Scene02(VideoScene):
    number = 2

    def construct(self):
        # Schematic: a table flows into a model; one bad cell flows straight through.
        cells = VGroup(*[Rectangle(width=0.7, height=0.42, stroke_color=GRID, stroke_width=3,
                                   fill_color=SKY, fill_opacity=0.18) for _ in range(20)])
        cells.arrange_in_grid(5, 4, buff=0).move_to([-4.6, -0.3, 0])
        table_name = label("the table", 32, SUBDUED, weight=BOLD).next_to(cells, UP, 0.3)
        box = RoundedRectangle(width=3.0, height=2.2, corner_radius=0.25, stroke_color=INK, stroke_width=5,
                               fill_color=GRID, fill_opacity=0.5).move_to([0, -0.3, 0])
        name = label("a model", 40, INK, weight=BOLD).move_to(box)
        output = card("a prediction", GREEN, 38).move_to([4.6, -0.3, 0])
        arrow_in = Arrow(cells.get_right(), box.get_left(), color=INK, stroke_width=5, buff=0.25)
        arrow_out = Arrow(box.get_right(), output.get_left(), color=INK, stroke_width=5, buff=0.2)
        bad = cells[9]
        fault = Dot(bad.get_center(), 0.13, color=VERMILION)
        quiet = label("no warning", 32, VERMILION, weight=BOLD).next_to(output, DOWN, 0.4)
        first = card("first, know what is in the table", GREEN, 34).to_edge(DOWN, buff=0.5)
        # "Let's start with why the data come first."
        self.play(FadeIn(cells), FadeIn(table_name), run_time=self.share(0.1))
        # "A model learns only from the table it is given."
        at(self, 0.18)
        self.play(GrowArrow(arrow_in), FadeIn(box), FadeIn(name), run_time=self.share(0.08))
        self.play(GrowArrow(arrow_out), FadeIn(output, shift=0.2 * RIGHT), run_time=self.share(0.08))
        # "If the table is wrong,"
        at(self, 0.38)
        self.play(bad.animate.set_fill(VERMILION, 0.8), run_time=self.share(0.06))
        # "the model learns that too,"
        at(self, 0.48)
        self.add(fault)
        self.play(fault.animate.move_to(box.get_center()), run_time=self.share(0.08))
        # "and nothing in its output says so."
        at(self, 0.59)
        self.play(fault.animate.move_to(output.get_center()).set_opacity(0), run_time=self.share(0.07))
        self.play(FadeIn(quiet, shift=0.2 * UP), run_time=self.share(0.06))
        # "So before any modelling, we need to know what is in the table."
        at(self, 0.74)
        self.play(FadeIn(first, shift=0.2 * UP), run_time=self.share(0.07))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        # Schematic: one station as a card, after the survey page's diagram.
        head = label("one simulated coastal survey", 44, PURPLE, weight=BOLD).to_edge(UP, buff=0.7)
        row = label("each row is a station: one visit to one place", 34, INK, weight=BOLD).next_to(head, DOWN, 0.4)
        parts = VGroup(panel("where and when", ["site", "date, season"], BLUE, 3.6),
                       panel("the water", ["temperature", "salinity", "chlorophyll:", "phytoplankton"], SKY, 3.0, 2.8),
                       panel("the seabed", ["mud, sand,", "gravel or rock"], ORANGE, 3.0),
                       panel("the species", ["how many", "were counted"], VERMILION, 3.0)
                       ).arrange(RIGHT, buff=0.25).move_to([0, -1.2, 0])
        # "The course works on one simulated coastal survey, the one from the introduction."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "Each row of its table is a station: one visit to one place."
        at(self, 0.24)
        self.play(FadeIn(row), run_time=self.share(0.08))
        # "It records where and when, the water's temperature and salinity, and its
        # chlorophyll, ... Then the type of seabed, and the count of one species."
        for part, when in zip(parts, [0.42, 0.51, 0.84, 0.91]):
            at(self, when)
            self.play(FadeIn(part, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class Scene04(VideoScene):
    number = 4

    def construct(self):
        # Schematic: three kinds of column, then the months on a line and on a circle.
        kinds = VGroup(panel("a quantity", ["depth"], BLUE, 3.2, 1.5),
                       panel("a category", ["seabed"], ORANGE, 3.2, 1.5),
                       panel("neither", ["month"], PURPLE, 3.2, 1.5)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.5)
        xs = np.linspace(-5.5, 5.5, 12)
        dots = VGroup(*[Dot([x, -0.6, 0], 0.11, color=ORANGE if i in (0, 11) else INK) for i, x in enumerate(xs)])
        names = VGroup(*[label(m, 24, ORANGE if i in (0, 11) else SUBDUED, weight=BOLD if i in (0, 11) else NORMAL)
                         .next_to(d, DOWN, 0.2) for i, (m, d) in enumerate(zip(MONTHS, dots))])
        line = Line([-5.8, -0.6, 0], [5.8, -0.6, 0], color=GRID, stroke_width=4)
        apart = BraceBetweenPoints(dots[0].get_center() + 0.2 * UP, dots[11].get_center() + 0.2 * UP, UP, color=VERMILION)
        apart_name = label("eleven months apart", 30, VERMILION, weight=BOLD).next_to(apart, UP, 0.1)
        centre, radius = np.array([0, -1.3, 0]), 1.55
        ring = Circle(radius, color=GRID, stroke_width=4).move_to(centre)
        angles = [PI / 2 - (i + 0.5) * TAU / 12 for i in range(12)]
        spots = [centre + radius * np.array([np.cos(a), np.sin(a), 0]) for a in angles]
        near = label("neighbours", 32, GREEN, weight=BOLD).move_to(centre + [0, radius + 0.75, 0])
        # "Some are quantities, measured on a scale, like depth. Some are categories, a label
        # from a short list, like the type of seabed. And some are neither, like the month,"
        at(self, 0.18)
        self.play(FadeIn(kinds[0], shift=0.2 * DOWN), run_time=self.share(0.05))
        at(self, 0.31)
        self.play(FadeIn(kinds[1], shift=0.2 * DOWN), run_time=self.share(0.05))
        at(self, 0.49)
        self.play(FadeIn(kinds[2], shift=0.2 * DOWN), run_time=self.share(0.05))
        # "As plain numbers, December and January are eleven months apart."
        at(self, 0.65)
        self.play(Create(line), FadeIn(dots), FadeIn(names), run_time=self.share(0.07))
        self.play(GrowFromCenter(apart), FadeIn(apart_name), run_time=self.share(0.06))
        # "In the sea they are neighbours, so a model needs to see the months as a circle."
        at(self, 0.81)
        moves = [d.animate.move_to(s) for d, s in zip(dots, spots)]
        moves += [n.animate.move_to(centre + (radius + 0.4) * (s - centre) / radius) for n, s in zip(names, spots)]
        self.play(FadeOut(apart), FadeOut(apart_name), ReplacementTransform(line, ring), *moves,
                  run_time=self.share(0.1))
        self.play(FadeIn(near, scale=0.8), run_time=self.share(0.05))
        self.finish()


class Scene05(VideoScene):
    number = 5

    def construct(self):
        # Page results: the-coastal-survey.qmd.
        counts = self.data("counts").iloc[0]
        rows = [("rows in the file", int(counts["rows"]), GREY),
                ("once duplicates are removed", int(counts["unique"]), BLUE),
                ("sites", int(counts["sites"]), ORANGE)]
        scale = 9.0 / rows[0][1]
        bars = VGroup()
        for i, (name, n, colour) in enumerate(rows):
            y = 1.4 - 1.5 * i
            bar = Rectangle(width=n * scale, height=0.7, stroke_width=0, fill_color=colour, fill_opacity=0.85)
            bar.move_to([-5.2 + n * scale / 2, y, 0])
            value = label(str(n), 44, INK, weight=BOLD).next_to(bar, RIGHT, 0.25)
            what = label(name, 30, SUBDUED).next_to(bar, UP, 0.12).align_to(bar, LEFT)
            bars.add(VGroup(bar, value, what))
        # "The raw file has 815 rows. Some are the same station entered twice, called
        # duplicates. Remove them, and 800 remain. But those 800 come from only 160 sites,"
        for group, when in zip(bars, [0.23, 0.6, 0.72]):
            at(self, when)
            self.play(GrowFromEdge(group[0], LEFT), FadeIn(group[1]), FadeIn(group[2]), run_time=self.share(0.1))
        self.finish()


# Four schematic sites with their visits, used again in the split scenes.
SITE_VISITS = [3, 5, 4, 4]
SITE_COLOURS = [BLUE, ORANGE, GREEN, PURPLE]


class Scene06(VideoScene):
    number = 6

    def construct(self):
        # Schematic: visits to a site are alike, so a site's rows are kept together.
        rng = np.random.default_rng(6)
        owners = [s for s, n in enumerate(SITE_VISITS) for _ in range(n)]
        order = rng.permutation(len(owners))
        squares = VGroup(*[RoundedRectangle(width=0.8, height=0.8, corner_radius=0.1, stroke_width=0,
                                            fill_color=GREY, fill_opacity=0.5) for _ in owners])
        slots = VGroup(*[Square(0.8) for _ in owners]).arrange_in_grid(4, 4, buff=0.25).move_to([0, 0.3, 0])
        for k, i in enumerate(order):
            squares[i].move_to(slots[k])
        head = label("16 rows", 40, INK, weight=BOLD).to_edge(UP, buff=0.5)
        warn = card("rows are not independent observations", VERMILION, 32).to_edge(DOWN, buff=0.3)
        blocks, frames = [], VGroup()
        x = -5.0
        for s, n in enumerate(SITE_VISITS):
            column = VGroup(*[Square(0.8) for _ in range(n)]).arrange(DOWN, buff=0.12)
            column.move_to([x + 0.4 + s * 0.4, 0.4, 0]).align_to([0, 2.3, 0], UP)
            blocks.append(column)
            frames.add(SurroundingRectangle(column, color=SITE_COLOURS[s], buff=0.15, corner_radius=0.15, stroke_width=4))
            x += 2.4
        names = VGroup(*[label(f"site {c}", 30, SITE_COLOURS[s], weight=BOLD).next_to(frames[s], UP, 0.15)
                         for s, c in enumerate("ABCD")])
        together = VGroup(frames, names).move_to([0, 0.5, 0])
        for s, column in enumerate(blocks):
            column.move_to(frames[s])
        self.play(FadeIn(head), FadeIn(squares), run_time=self.share(0.1))
        # "Visits to the same site share their water and their seabed, so they are alike."
        at(self, 0.06)
        self.play(*[sq.animate.set_fill(SITE_COLOURS[o], 0.8) for sq, o in zip(squares, owners)],
                  run_time=self.share(0.15))
        # "So the row count is not the number of independent observations,"
        at(self, 0.49)
        self.play(FadeIn(warn, shift=0.2 * UP), run_time=self.share(0.08))
        # "Keep the rows, but keep each site's rows together."
        at(self, 0.76)
        seen = [0] * len(SITE_VISITS)
        moves = []
        for sq, o in zip(squares, owners):
            moves.append(sq.animate.move_to(blocks[o][seen[o]]))
            seen[o] += 1
        self.play(FadeOut(head), *moves, run_time=self.share(0.12))
        self.play(FadeIn(together), run_time=self.share(0.08))
        self.finish()


class Scene07(KeyPointScene):
    number, point = 7, 1


# Cleaning the raw file (scenes 8–14) ----------------------------------------------------

def salinity_layout(scene):
    """The raw file's salinity as the exploring page's range table gives it."""
    salinity = scene.data("ranges").set_index("variable").loc["salinity_psu"]
    head = label("salinity in the raw file", 44, INK, weight=BOLD).to_edge(UP, buff=0.8)
    cols = VGroup()
    for name, value in [("smallest", salinity["min"]), ("average", salinity["mean"]), ("largest", salinity["max"])]:
        text = f"{value:.0f}".replace("-", "−") if value == int(value) else f"{value:.2f}"
        cols.add(VGroup(label(name, 32, SUBDUED), label(text, 72, INK, weight=BOLD)).arrange(DOWN, buff=0.35))
    cols.arrange(RIGHT, buff=1.8).move_to([0, 0.1, 0])
    for c in cols:
        c[1].set_y(cols[0][1].get_y())
    return head, cols


class Scene08(VideoScene):
    number = 8

    def construct(self):
        # Page results: exploring-and-cleaning.qmd, the range table.
        head, cols = salinity_layout(self)
        fresh = card("no sea is that fresh", VERMILION, 38).to_edge(DOWN, buff=0.9)
        # The page's prose: the real ocean is the narrow cluster near 34.
        real = label("real sea water here: about 34", 34, GREEN, weight=BOLD).next_to(fresh, UP, 0.35)
        look = label("before modelling, look", 44, INK, weight=BOLD).move_to(head)
        # "Next, cleaning the raw file. Before modelling, look at the data."
        at(self, 0.1)
        self.play(FadeIn(look, shift=0.2 * DOWN), run_time=self.share(0.06))
        # "A simple first check is the smallest, average and largest value of every column."
        at(self, 0.23)
        self.play(LaggedStart(*[FadeIn(c[0]) for c in cols], lag_ratio=0.5), run_time=self.share(0.12))
        # "Here is salinity."
        at(self, 0.52)
        self.play(ReplacementTransform(look, head), run_time=self.share(0.05))
        # "Its smallest value is minus 999,"
        at(self, 0.59)
        cols[0][1].set_color(VERMILION)
        self.play(FadeIn(cols[0][1]), FadeIn(cols[2][1]), run_time=self.share(0.05))
        # "and its average is 2.24."
        at(self, 0.71)
        cols[1][1].set_color(VERMILION)
        self.play(FadeIn(cols[1][1]), run_time=self.share(0.05))
        # "Real sea water here is about 34, so no sea is that fresh."
        at(self, 0.8)
        self.play(FadeIn(real), run_time=self.share(0.05))
        at(self, 0.91)
        self.play(FadeIn(fresh, shift=0.2 * UP), run_time=self.share(0.06))
        self.finish()


class Scene09(VideoScene):
    number = 9

    def construct(self):
        # Page results: exploring-and-cleaning.qmd, the mean once −999 is missing.
        head, cols = salinity_layout(self)
        cols[0][1].set_color(VERMILION)
        cols[1][1].set_color(VERMILION)
        self.add(head, cols)
        means = self.data("salinity-means").iloc[0]
        meaning = card("−999 means \"missing\"", PURPLE, 38).to_edge(DOWN, buff=0.9)
        missing = label("missing", 56, SUBDUED, weight=BOLD).move_to(cols[0][1])
        smallest = label("smallest real", 32, SUBDUED).move_to(cols[0][0])
        mean = label(f"{means['clean_mean']:.1f}", 72, GREEN, weight=BOLD).move_to(cols[1][1])
        # "Minus 999 is a code: some instrument or export wrote it to mean "missing"."
        self.play(FadeIn(meaning, shift=0.2 * UP), run_time=self.share(0.12))
        # "Mark those values as missing instead,"
        at(self, 0.47)
        self.play(FadeOut(cols[0]), FadeIn(missing), run_time=self.share(0.1))
        # "and the average becomes 33.9, as it should be."
        at(self, 0.71)
        self.play(ReplacementTransform(cols[1][1], mean), run_time=self.share(0.12))
        self.finish()


SUBSTRATE_TYPES = ["mud", "sand", "gravel", "rock"]


class Scene10(VideoScene):
    number = 10

    def construct(self):
        # Page results: exploring-and-cleaning.qmd, the substrate spellings.
        spellings = list(self.data("substrate-spellings")["substrate"])
        kind = {s: next(t for t in SUBSTRATE_TYPES if s.lower().startswith(t)) for s in spellings}
        colour = dict(zip(SUBSTRATE_TYPES, [PURPLE, ORANGE, BLUE, GREEN]))
        chips = VGroup(*[card(s, colour[kind[s]], 26) for s in spellings])
        chips.arrange_in_grid(3, 4, buff=(0.5, 0.45)).move_to([0, -0.5, 0])
        head = label(f"{len(spellings)} spellings", 44, INK, weight=BOLD).to_edge(UP, buff=0.6)
        xs = [-4.8, -1.6, 1.6, 4.8]
        headings = VGroup(*[label(t, 40, colour[t], weight=BOLD).move_to([x, 2.15, 0])
                            for t, x in zip(SUBSTRATE_TYPES, xs)])
        head4 = label(f"{len(SUBSTRATE_TYPES)} seabed types", 44, INK, weight=BOLD).to_edge(UP, buff=0.6)
        seen = {t: 0 for t in SUBSTRATE_TYPES}
        step = max(c.height for c in chips) + 0.2   # a gap between the chips in each column
        moves = []
        for chip, s in zip(chips, spellings):
            t = kind[s]
            moves.append(chip.animate.move_to([xs[SUBSTRATE_TYPES.index(t)], 1.15 - step * seen[t], 0]))
            seen[t] += 1
        warn = card("a model sees twelve different habitats", VERMILION, 32).to_edge(DOWN, buff=0.3)
        # "Count every category, too. The type of seabed was written in twelve different ways,"
        self.play(FadeIn(head), LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.1),
                  run_time=self.share(0.2))
        # "such as sand with a capital S, sand in capitals, and sandy."
        for name, when in [("Sand", 0.29), ("SAND", 0.4), ("sandy", 0.47)]:
            at(self, when)
            self.play(Indicate(chips[spellings.index(name)], color=ORANGE, scale_factor=1.15),
                      run_time=self.share(0.06))
        # "They are really four types: mud, sand, gravel and rock."
        at(self, 0.5)
        self.play(ReplacementTransform(head, head4), FadeIn(headings), run_time=self.share(0.1))
        # "A model would treat each spelling as a different habitat,"
        at(self, 0.7)
        self.play(FadeIn(warn, shift=0.2 * UP), run_time=self.share(0.08))
        # "so the spellings are merged."
        at(self, 0.9)
        self.play(*moves, run_time=self.share(0.1))
        self.finish()


class Scene11(VideoScene):
    number = 11

    def construct(self):
        # Page results: exploring-and-cleaning.qmd#fig-deletion.
        table = self.data("deletion")
        cost = self.data("deletion-cost").iloc[0]
        seasons = ["spring", "summer", "autumn", "winter"]
        top = 250
        axes = plain_axes([0, 4, 1], [0, top, 50], 10.0, 4.2).move_to([0, -0.9, 0])
        base = axes.c2p(0, 0)[1]
        all_rows, complete, values = VGroup(), VGroup(), VGroup()
        for i, season in enumerate(seasons):
            for dataset, group, dx, colour in [("All rows", all_rows, -0.32, GREY),
                                               ("Complete rows only", complete, 0.32, BLUE)]:
                n = int(table[(table["season"] == season) & (table["dataset"] == dataset)]["n"].iloc[0])
                x = axes.c2p(i + 0.5, 0)[0] + dx
                height = axes.c2p(0, n)[1] - base
                bar = Rectangle(width=0.6, height=height, stroke_width=0, fill_color=colour, fill_opacity=0.85)
                bar.move_to([x, base + height / 2, 0])
                group.add(bar)
                if dataset == "Complete rows only":
                    values.add(label(str(n), 24, SUBDUED).next_to(bar, UP, 0.1))
        names = VGroup(*[label(s, 30, INK).move_to(axes.c2p(i + 0.5, 0) + 0.4 * DOWN) for i, s in enumerate(seasons)])
        key = VGroup(VGroup(Square(0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.85), label("all rows", 28, SUBDUED)
                            ).arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.3, stroke_width=0, fill_color=BLUE, fill_opacity=0.85),
                            label("incomplete rows dropped", 28, SUBDUED)).arrange(RIGHT, buff=0.15)
                     ).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.4)
        overall = label(f"{cost['lost_pct']:.0f}% of the stations lost", 34, INK, weight=BOLD).to_edge(UP, buff=1.1)
        winter = label(f"{cost['winter_lost_pct']:.0f}% of winter", 36, VERMILION, weight=BOLD)
        ring = SurroundingRectangle(VGroup(all_rows[3], complete[3], values[3]), color=VERMILION, buff=0.15, corner_radius=0.1)
        winter.next_to(ring, UP, 0.15)
        # "Some values are simply missing. Chlorophyll is missing most often in winter."
        self.play(Create(axes.x_axis), FadeIn(names), FadeIn(key[0]), GrowFromEdge(all_rows, DOWN), run_time=self.share(0.15))
        # "Many modelling functions quietly drop every incomplete row,"
        at(self, 0.24)
        self.play(FadeIn(key[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in complete], lag_ratio=0.2),
                  FadeIn(values), run_time=self.share(0.2))
        # "Here, that loses 10% of the stations,"
        at(self, 0.56)
        self.play(FadeIn(overall), run_time=self.share(0.08))
        # "but 20% of the winter ones."
        at(self, 0.68)
        self.play(Create(ring), FadeIn(winter), run_time=self.share(0.08))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        # Schematic: the question every fix starts from, and the three reasons a value is
        # missing, after the exploring page's missing-and-unusual diagram.
        question = label("Why is this value missing, or strange?", 44, INK, weight=BOLD).to_edge(UP, buff=0.7)
        decides = label("the answer decides the fix", 40, GREEN, weight=BOLD).next_to(question, DOWN, 0.4)
        reasons = VGroup(panel("by chance", ["a sample lost:", "little harm"], GREEN, 3.9, 2.6, 28),
                         panel("with the season", ["follows something", "recorded: fill in", "from it"],
                               ORANGE, 3.9, 2.6, 28),
                         panel("in storms", ["the gaps are the", "stormy values:", "no fix in the data"],
                               VERMILION, 3.9, 2.6, 28)).arrange(RIGHT, buff=0.35).move_to([0, -1.4, 0])
        no_fix = reasons[2][2][-1]
        # "So every fix starts with one question: why is this value missing, or strange?"
        self.play(FadeIn(question, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "The answer decides the fix."
        at(self, 0.2)
        self.play(FadeIn(decides, shift=0.2 * UP), run_time=self.share(0.06))
        # "A sample lost by pure chance costs only a little precision. Gaps that depend on
        # something recorded, such as the season, can be filled in from what was recorded.
        # But when a sensor fails in storms,"
        for reason, when in zip(reasons, [0.27, 0.43, 0.69]):
            at(self, when)
            self.play(FadeIn(reason, shift=0.2 * UP), run_time=self.share(0.06))
        # "and no fix to the data can bring them back."
        at(self, 0.89)
        self.play(no_fix.animate.set_color(VERMILION), run_time=self.share(0.05))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        # Schematic: the recipe's three stages, after the scaling-and-encoding page's diagram.
        chips = VGroup(*[VGroup(card(name, SKY, 30), label(gloss, 26, SUBDUED)).arrange(DOWN, buff=0.15)
                         for name, gloss in [("standardise", "every column on one scale"),
                                             ("log", "pulls in a long tail"),
                                             ("columns of 0s and 1s", "a category as numbers")]]
                       ).arrange(RIGHT, buff=0.5, aligned_edge=UP).to_edge(UP, buff=0.5)
        stages = VGroup(panel("1 specify", ["list the steps"], BLUE, 3.3, 2.2, 28),
                        panel("2 estimate", ["the numbers they need,", "from training data only"], ORANGE, 4.5, 2.2, 28),
                        panel("3 apply", ["the same numbers,", "to any data"], GREEN, 3.7, 2.2, 28)
                        ).arrange(RIGHT, buff=0.5).move_to([0, -0.9, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), color=INK, stroke_width=4, buff=0.08)
                          for a, b in zip(stages[:-1], stages[1:])])
        name = label("a recipe", 40, INK, weight=BOLD).next_to(stages, UP, 0.4)
        # "Standardising puts every column on the same scale: ... A log pulls in a long tail,
        # ... And a category, such as the seabed, becomes columns of zeros and ones,"
        for chip, when in zip(chips, [0.07, 0.35, 0.47]):
            at(self, when)
            self.play(FadeIn(chip, shift=0.2 * DOWN), run_time=self.share(0.04))
        # "A recipe holds these steps. It lists them,"
        at(self, 0.63)
        self.play(FadeIn(name), FadeIn(stages[0], shift=0.2 * UP), run_time=self.share(0.04))
        # "works out the numbers they need, such as each mean, from the training data only,"
        at(self, 0.7)
        self.play(GrowArrow(arrows[0]), FadeIn(stages[1], shift=0.2 * UP), run_time=self.share(0.04))
        # "and then applies those same numbers to any data."
        at(self, 0.84)
        self.play(GrowArrow(arrows[1]), FadeIn(stages[2], shift=0.2 * UP), run_time=self.share(0.04))
        # "Why the training data only? We come to that next."
        at(self, 0.92)
        self.play(stages[1][2][2].animate.set_color(VERMILION), run_time=self.share(0.04))
        self.finish()


class Scene14(KeyPointScene):
    number, point = 14, 2


# Testing a model honestly (scenes 15–24) ------------------------------------------------

class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Schematic: the three roles of the data.
        head = label("tested on data it has not seen", 44, INK, weight=BOLD).to_edge(UP, buff=0.8)
        roles = VGroup(panel("training", ["the model", "learns from it"], BLUE, 3.6, 2.0, 30),
                       panel("validation", ["chooses between", "models"], ORANGE, 3.6, 2.0, 30),
                       panel("test", ["reports the result,", "once"], GREEN, 3.6, 2.0, 30)
                       ).arrange(RIGHT, buff=0.5).move_to([0, -0.4, 0])
        # "Now to testing a model. A model must be tested on data it has not seen,"
        at(self, 0.07)
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.08))
        # "The model learns from the training data. Validation data choose between models,
        # or between settings of one model. And the test data report the result, once,"
        for role, when in zip(roles, [0.53, 0.64, 0.85]):
            at(self, when)
            self.play(FadeIn(role, shift=0.2 * UP), run_time=self.share(0.05))
        self.finish()


def sites_grid(test_of):
    """Schematic: the four sites' visits as squares, test visits marked by test_of(site, visit)."""
    columns = VGroup()
    for s, n in enumerate(SITE_VISITS):
        squares = VGroup()
        for v in range(n):
            test = test_of(s, v)
            squares.add(RoundedRectangle(width=0.6, height=0.6, corner_radius=0.08, stroke_width=4,
                                         stroke_color=VERMILION if test else SITE_COLOURS[s],
                                         fill_color=VERMILION if test else SITE_COLOURS[s],
                                         fill_opacity=0.85 if test else 0.35))
        squares.arrange(DOWN, buff=0.12)
        name = label(f"site {'ABCD'[s]}", 26, SITE_COLOURS[s], weight=BOLD)
        columns.add(VGroup(name, squares).arrange(DOWN, buff=0.2))
    columns.arrange(RIGHT, buff=0.45, aligned_edge=UP)
    return columns


def split_key():
    return VGroup(VGroup(RoundedRectangle(width=0.35, height=0.35, corner_radius=0.05, stroke_width=0, fill_color=GREY,
                                          fill_opacity=0.5), label("training", 26, SUBDUED)).arrange(RIGHT, buff=0.15),
                  VGroup(RoundedRectangle(width=0.35, height=0.35, corner_radius=0.05, stroke_width=0,
                                          fill_color=VERMILION, fill_opacity=0.85), label("test", 26, SUBDUED)
                         ).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.5)


def random_grid():
    return sites_grid(lambda s, v: v == (s + 1) % SITE_VISITS[s])


def grouped_grid():
    return sites_grid(lambda s, v: s == 3)


class Scene16(VideoScene):
    number = 16

    def construct(self):
        # Page results: splitting-data.qmd, the share of test stations at a trained site.
        seen = int(self.data("seen")["seen_pct"].iloc[0])
        before = sites_grid(lambda s, v: False).scale(0.85).move_to([0, 0.1, 0])
        after = random_grid().scale(0.85).move_to(before)
        head = label("a random split", 44, INK, weight=BOLD).to_edge(UP, buff=0.3)
        how = label("each station by chance: three quarters to training", 30, SUBDUED).next_to(head, DOWN, 0.15)
        key = split_key().next_to(after, DOWN, 0.3)
        share = card(f"{seen}% of test stations sit at a site in training", VERMILION, 32).to_edge(DOWN, buff=0.3)
        # "The simplest way is a random split: each station goes to training or test by chance,"
        self.play(FadeIn(head), FadeIn(before), run_time=self.share(0.1))
        at(self, 0.15)
        self.play(FadeIn(how), ReplacementTransform(before, after), FadeIn(key), run_time=self.share(0.2))
        # "Split this survey at random, and every test station sits at a site the model trained on."
        at(self, 0.71)
        self.play(FadeIn(share, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene17(VideoScene):
    number = 17

    def construct(self):
        # Schematic: the two splits answer two questions; only one is the model's job.
        goal = card("the goal: predict places nobody has sampled", PURPLE, 34).to_edge(UP, buff=0.3)
        rand = random_grid().scale(0.7).move_to([-3.6, 0.15, 0])
        grouped = grouped_grid().scale(0.7).move_to([3.6, 0.15, 0])
        heads = [label(t, 34, INK, weight=BOLD).next_to(g, UP, 0.25) for t, g in
                 [("random split", rand), ("split by site", grouped)]]
        asks = [label(t, 30, c, weight=BOLD).next_to(g, DOWN, 0.35)
                for t, c, g in [("tests a site it knows", SUBDUED, rand),
                                ("tests a site it has never seen", GREEN, grouped)]]
        new = SurroundingRectangle(grouped[3], color=GREEN, buff=0.12, corner_radius=0.1, stroke_width=5)
        rule = card("split along what you will predict for", PURPLE, 36).to_edge(DOWN, buff=0.3)
        full = random_grid().move_to([0, 0.3, 0])
        self.add(full)
        # "But a survey model is usually wanted for places nobody has sampled."
        self.play(ReplacementTransform(full, rand), FadeIn(heads[0]), FadeIn(goal, shift=0.2 * DOWN),
                  run_time=self.share(0.1))
        # "A random split only tests another visit to a site the model already knows."
        at(self, 0.18)
        self.play(FadeIn(asks[0]), run_time=self.share(0.08))
        # "Hold back whole sites instead, so every visit to a test site stays out of training."
        at(self, 0.38)
        self.play(FadeIn(grouped), FadeIn(heads[1]), run_time=self.share(0.08))
        # "Then the test sites are new to the model, as they will be in use."
        at(self, 0.6)
        self.play(Create(new), FadeIn(asks[1]), run_time=self.share(0.06))
        # "So split along what you will predict for: by site for new sites, by year for next year."
        at(self, 0.77)
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene18(VideoScene):
    number = 18

    def construct(self):
        # Schematic: test data seeping into the model before the test.
        train = panel("training data", [], BLUE, 3.4, 1.4, 30).move_to([-4.5, 0.6, 0])
        model = panel("the model", [], INK, 3.0, 1.4, 30).move_to([0, 0.6, 0])
        test = panel("test data", [], GREEN, 3.0, 1.4, 30).move_to([4.5, 0.6, 0])
        fit = Arrow(train.get_right(), model.get_left(), color=INK, stroke_width=5, buff=0.15)
        wall = DashedLine([2.55, 2.0, 0], [2.55, -0.8, 0], color=GREY, stroke_width=5)
        leak = CurvedArrow(test.get_bottom() + 0.1 * DOWN, model.get_bottom() + 0.1 * DOWN, color=VERMILION,
                           stroke_width=6, angle=-PI / 2.2)
        name = label("information leakage", 46, VERMILION, weight=BOLD).move_to([1.6, -1.9, 0])
        better = label("the score looks better than the model is", 36, INK, weight=BOLD).move_to([0, -2.9, 0])
        trace = label("and leaves no trace", 36, SUBDUED, weight=BOLD).next_to(better, DOWN, 0.2)
        self.play(FadeIn(train), FadeIn(model), GrowArrow(fit), FadeIn(test), Create(wall), run_time=self.share(0.12))
        # "When information from the test data reaches the model before the test,"
        at(self, 0.08)
        self.play(Create(leak), run_time=self.share(0.17))
        # "that is called information leakage, or leakage for short."
        at(self, 0.27)
        self.play(FadeIn(name, scale=0.8), run_time=self.share(0.06))
        # "It makes the score look better than the model really is,"
        at(self, 0.49)
        self.play(FadeIn(better, shift=0.2 * UP), run_time=self.share(0.06))
        # "and it leaves no trace: the results look just like honest ones, only better."
        at(self, 0.71)
        self.play(FadeIn(trace, shift=0.2 * UP), run_time=self.share(0.07))
        self.finish()


def rsq_bars(rows, colours, head_text):
    """Horizontal R² bars on a 0 to 1 scale, with each bar's value as the page prints it.
    The axis group ends with what 0 and 1 mean, as the leakage page defines R²."""
    head = label(head_text, 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
    axis = plain_axes([0, 1, 0.25], [0, 1, 1], 8.0, 0.01).move_to([1.2, -1.9, 0])
    ticks = VGroup(*[label(f"{v:g}", 24, SUBDUED).next_to(axis.c2p(v, 0), DOWN, 0.15) for v in (0, 0.5, 1)])
    means = VGroup(label("no better than the average", 24, SUBDUED).next_to(ticks[0], DOWN, 0.12)
                   .align_to(ticks[0], LEFT).shift(0.3 * LEFT),
                   label("every prediction exact", 24, SUBDUED).next_to(ticks[2], DOWN, 0.12)
                   .align_to(ticks[2], RIGHT).shift(0.3 * RIGHT))
    axis_name = label("R² on the test data", 26, SUBDUED, weight=BOLD).next_to(means, DOWN, 0.2)
    bars = VGroup()
    for i, ((name, value), colour) in enumerate(zip(rows, colours)):
        y = 0.9 - 1.6 * i
        width = max(value * 8.0, 0.02)
        bar = Rectangle(width=width, height=0.9, stroke_width=0, fill_color=colour, fill_opacity=0.85)
        bar.move_to([axis.c2p(0, 0)[0] + width / 2, y + 0.2, 0])
        what = label(name, 30, INK, weight=BOLD).next_to([axis.c2p(0, 0)[0], y + 0.2, 0], LEFT, 0.3)
        amount = label(f"{value:.2f}", 40, INK, weight=BOLD).next_to(bar, RIGHT, 0.25)
        bars.add(VGroup(bar, what, amount))
    return head, VGroup(axis, ticks, axis_name, means), bars


def target_layout(scene):
    table = scene.data("target").set_index("model")["rsq"]
    return rsq_bars([("environment only", table["Environment only"]),
                     ("plus catch weight", table["Plus catch weight"])], [BLUE, VERMILION],
                    "a linear regression of the count")


# Made-up counts at ten test stations, and predictions that follow about half their
# swings: a picture of what R² measures, not survey numbers.
RSQ_COUNTS = [3.0, 7.5, 4.5, 9.0, 5.5, 2.0, 8.0, 6.5, 3.5, 7.0]
RSQ_SWAY = [0.4, -0.3, 0.5, -0.6, 0.2, 0.5, -0.4, 0.3, 0.6, -0.2]


class Scene19(VideoScene):
    number = 19

    def construct(self):
        # Schematic: the counts vary about their average; the predictions follow part of it.
        model = label("a linear regression: the count from the environment", 36, INK, weight=BOLD)
        model.to_edge(UP, buff=0.45)
        head = label("R squared: how well a model fits the data", 40, PURPLE, weight=BOLD).move_to(model)
        axes = plain_axes([0, 11, 1], [0, 10, 2], 7.0, 4.4).move_to([-2.9, -0.7, 0])
        axis_name = label("the count at each test station", 26, SUBDUED).next_to(axes, UP, 0.15).align_to(axes, LEFT)
        mean = np.mean(RSQ_COUNTS)
        xs = range(1, len(RSQ_COUNTS) + 1)
        dots = VGroup(*[Dot(axes.c2p(x, y), 0.1, color=INK) for x, y in zip(xs, RSQ_COUNTS)])
        average = DashedLine(axes.c2p(0.4, mean), axes.c2p(10.6, mean), color=GREY, stroke_width=4)
        average_name = label("average", 26, GREY, weight=BOLD).next_to(average, RIGHT, 0.15)
        spread = VGroup(*[Line(axes.c2p(x, mean) + 0.07 * LEFT, axes.c2p(x, y) + 0.07 * LEFT,
                               color=SKY, stroke_width=6) for x, y in zip(xs, RSQ_COUNTS)])
        vary = label("how much the counts vary", 28, SKY, weight=BOLD).next_to(axes, DOWN, 0.3)
        guesses = [mean + 0.5 * (y - mean) + d for y, d in zip(RSQ_COUNTS, RSQ_SWAY)]
        predictions = VGroup(*[Line(axes.c2p(x - 0.3, g), axes.c2p(x + 0.3, g), color=ORANGE, stroke_width=7)
                               for x, g in zip(xs, guesses)])
        predicted = label("predictions", 28, ORANGE, weight=BOLD).next_to(vary, RIGHT, 0.6)
        misses = VGroup(*[Line(axes.c2p(x, g) + 0.07 * RIGHT, axes.c2p(x, y) + 0.07 * RIGHT,
                               color=VERMILION, stroke_width=6) for x, y, g in zip(xs, RSQ_COUNTS, guesses)])
        missed = label("missed", 28, VERMILION, weight=BOLD).next_to(predicted, RIGHT, 0.6)
        share = VGroup(label("R² = the share of", 34, INK, weight=BOLD),
                       label("the variation the", 34, INK, weight=BOLD),
                       label("predictions follow", 34, INK, weight=BOLD)).arrange(DOWN, buff=0.12)
        share.move_to([4.1, 1.2, 0])
        scale = Line([2.6, -0.6, 0], [5.6, -0.6, 0], color=INK, stroke_width=5)
        ends = VGroup(*[Line(scale.get_start() + 0.15 * UP, scale.get_start() + 0.15 * DOWN, color=INK, stroke_width=5),
                        Line(scale.get_end() + 0.15 * UP, scale.get_end() + 0.15 * DOWN, color=INK, stroke_width=5)])
        one = VGroup(label("1", 36, GREEN, weight=BOLD), label("every prediction", 24, SUBDUED),
                     label("exact", 24, SUBDUED)).arrange(DOWN, buff=0.08).next_to(scale.get_end(), DOWN, 0.25)
        zero = VGroup(label("0", 36, VERMILION, weight=BOLD), label("no better than", 24, SUBDUED),
                      label("the average", 24, SUBDUED)).arrange(DOWN, buff=0.08).next_to(scale.get_start(), DOWN, 0.25)
        # "Here is an example. A linear regression, ... predicts the count from the environment:"
        at(self, 0.04)
        self.play(FadeIn(model, shift=0.2 * DOWN), run_time=self.share(0.05))
        # "To check how well a model fits the data, we use R squared."
        at(self, 0.31)
        self.play(ReplacementTransform(model, head), run_time=self.share(0.04))
        # "The counts at the test stations vary: some are high, some are low."
        at(self, 0.42)
        self.play(Create(axes), FadeIn(axis_name), FadeIn(dots), Create(average), FadeIn(average_name),
                  run_time=self.share(0.05))
        at(self, 0.49)
        self.play(Create(spread), FadeIn(vary), run_time=self.share(0.04))
        # "The model's predictions follow part of that variation, and miss the rest."
        at(self, 0.54)
        self.play(FadeIn(predictions), FadeIn(predicted), run_time=self.share(0.04))
        at(self, 0.63)
        self.play(Create(misses), FadeIn(missed), run_time=self.share(0.04))
        # "R squared is the share they follow."
        at(self, 0.68)
        self.play(FadeIn(share, shift=0.2 * UP), run_time=self.share(0.04))
        # "If every prediction is exact, R squared is one."
        at(self, 0.75)
        self.play(Create(scale), FadeIn(ends), FadeIn(one), run_time=self.share(0.04))
        # "If the model does no better than predicting the average count everywhere, it is zero."
        at(self, 0.86)
        self.play(FadeIn(zero), run_time=self.share(0.04))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        # Page results: information-leakage.qmd, target leakage.
        head, axis, bars = target_layout(self)
        fifth = label("about a fifth of the variation", 28, SUBDUED).next_to(bars[0][2], RIGHT, 0.4)
        self.add(head, axis)
        # "On the environment alone, R squared is 0.22:"
        at(self, 0.02)
        self.play(GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]), run_time=self.share(0.1))
        # "the predictions follow only about a fifth of the variation."
        at(self, 0.28)
        self.play(FadeIn(fifth), run_time=self.share(0.08))
        # "Add one more column, catch weight, and it jumps to 0.98."
        at(self, 0.87)
        self.play(GrowFromEdge(bars[1][0], LEFT), FadeIn(bars[1][1:]), run_time=self.share(0.08))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        # Page results as in scene 20; the rest schematic.
        head, axis, bars = target_layout(self)
        fifth = label("about a fifth of the variation", 28, SUBDUED).next_to(bars[0][2], RIGHT, 0.4)
        self.add(head, axis, bars, fifth)
        same = card("catch weight is the count, in other units", PURPLE, 34).to_edge(UP, buff=0.5)
        handed = card("each test station's answer, handed to the model", VERMILION, 32).move_to([0, -3.3, 0])
        copying = card("copying, not predicting", VERMILION, 36).move_to(handed)
        cross = Cross(bars[1][0], stroke_color=VERMILION, stroke_width=8)
        # "Catch weight is the weight of the animals that were counted: the count again, in other units."
        self.play(FadeOut(head), FadeIn(same, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "So for every test station, the model is handed the answer it should predict."
        at(self, 0.44)
        self.play(FadeOut(axis), FadeOut(fifth), FadeIn(handed, shift=0.2 * UP), run_time=self.share(0.08))
        # "The 0.98 measures copying, not predicting."
        at(self, 0.8)
        self.play(Create(cross), bars[1].animate.set_opacity(0.35), ReplacementTransform(handed, copying),
                  run_time=self.share(0.1))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        # Page results: information-leakage.qmd, group leakage.
        table = self.data("group").set_index("split")["rsq"]
        head, axis, bars = rsq_bars([("random split", table["Random"]), ("split by site", table["By site"])],
                                    [BLUE, GREEN], "environment only, split two ways")
        harder = card("a new site is much harder to predict", PURPLE, 32).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(head), FadeIn(axis), GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]), run_time=self.share(0.15))
        # "Leakage can also hide in the split. Keep each site whole, and the environment-only
        # model's R squared falls from 0.22 to 0.04."
        at(self, 0.3)
        self.play(GrowFromEdge(bars[1][0], LEFT), FadeIn(bars[1][1:]), run_time=self.share(0.1))
        # "Predicting a new site is much harder than predicting another visit to a familiar one,"
        at(self, 0.52)
        self.play(FadeOut(axis), FadeIn(harder, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene23(VideoScene):
    number = 23

    def construct(self):
        # Schematic: the page's one question.
        head = label("one question catches every kind of leakage", 38, SUBDUED, weight=BOLD).to_edge(UP, buff=1.0)
        code = VGroup(*[RoundedRectangle(width=w, height=0.28, corner_radius=0.08, stroke_width=0, fill_color=GRID,
                                         fill_opacity=1) for w in (5.0, 3.6, 6.2, 4.4)]).arrange(DOWN, buff=0.18,
                                                                                                aligned_edge=LEFT)
        code.move_to([0, 0.5, 0])
        line = code[2]
        mark = Arrow(line.get_left() + 1.2 * LEFT, line.get_left(), color=VERMILION, stroke_width=6, buff=0.1)
        question = VGroup(label("Does this line of code use information", 44, INK, weight=BOLD),
                          label("from the rows I intend to test on?", 44, INK, weight=BOLD)).arrange(DOWN, buff=0.2)
        question.move_to([0, -2.0, 0])
        # "Leakage is rarely cheating."
        self.play(FadeIn(code), run_time=self.share(0.1))
        # "It is usually one line of code in the wrong place."
        at(self, 0.14)
        self.play(line.animate.set_fill(VERMILION, 0.6), GrowArrow(mark), run_time=self.share(0.1))
        # "So one question catches every kind of leakage."
        at(self, 0.4)
        self.play(FadeIn(head), run_time=self.share(0.08))
        # "Does this line of code use information from the rows I intend to test on?"
        at(self, 0.63)
        self.play(FadeIn(question, shift=0.2 * UP), run_time=self.share(0.12))
        self.finish()


class Scene24(KeyPointScene):
    number, point = 24, 3


# The quiz (scenes 25–26) ----------------------------------------------------------------

class Scene25(QuizScene):
    number = 25
    question = ("Gaps in chlorophyll are filled with", "the median of the whole survey,",
                "then it is split into training and test.", "What is wrong?")


class Scene26(VideoScene):
    number = 26

    def construct(self):
        # Schematic: every row, test rows included, sets the median; a recipe uses training rows only.
        answer = label("Leakage", 64, VERMILION, weight=BOLD).to_edge(UP, buff=0.5)

        def rows(n, colour):
            return VGroup(*[Rectangle(width=2.4, height=0.36, stroke_color=GRID, stroke_width=3, fill_color=colour,
                                      fill_opacity=0.35) for _ in range(n)]).arrange(DOWN, buff=0)

        train = rows(6, BLUE).move_to([-3.4, 0.55, 0])
        test = rows(2, GREEN).next_to(train, DOWN, 0.55)
        names = VGroup(label("training", 30, BLUE, weight=BOLD).next_to(train, LEFT, 0.6),
                       label("test", 30, GREEN, weight=BOLD).next_to(test, LEFT, 0.6))
        median = panel("median", ["of chlorophyll"], ORANGE, 3.0, 1.5, 28).move_to([1.8, train.get_center()[1], 0])
        feeds = VGroup(*[Line(r.get_right(), median.get_left(), color=GRID, stroke_width=3) for r in train])
        leaks = VGroup(*[Line(r.get_right(), median.get_left(), color=VERMILION, stroke_width=5) for r in test])
        shaped = card("the test rows shaped it", VERMILION, 32).next_to(median, DOWN, 0.9)
        recipe = SurroundingRectangle(VGroup(train, median), color=PURPLE, buff=0.3, corner_radius=0.2, stroke_width=5)
        recipe_name = label("recipe", 34, PURPLE, weight=BOLD).next_to(recipe, UP, 0.12).align_to(recipe, RIGHT)
        fix = card("the median from the training rows only", PURPLE, 32).to_edge(DOWN, buff=0.4).shift(1.8 * RIGHT)
        # "Leakage."
        self.play(FadeIn(answer, scale=0.9), run_time=self.share(0.08))
        # "The test rows helped set that median,"
        at(self, 0.1)
        self.play(FadeIn(train), FadeIn(test), FadeIn(names), FadeIn(median), Create(feeds), run_time=self.share(0.1))
        self.play(Create(leaks), run_time=self.share(0.08))
        # "so the test data reached the model before the test."
        at(self, 0.34)
        self.play(FadeIn(shaped, shift=0.2 * UP), run_time=self.share(0.08))
        # "Put the step in a recipe, and the median comes from the training data only."
        at(self, 0.6)
        self.play(FadeOut(leaks), FadeOut(shaped), Create(recipe), FadeIn(recipe_name), run_time=self.share(0.1))
        at(self, 0.8)
        self.play(FadeIn(fix, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


# The recap (scenes 27–29) and the end card (scene 30) -----------------------------------

class Scene27(RecapScene):
    number, point = 27, 1


class Scene28(RecapScene):
    number, point = 28, 2


class Scene29(RecapScene):
    number, point = 29, 3


class Scene30(EndCardScene):
    number = 30
