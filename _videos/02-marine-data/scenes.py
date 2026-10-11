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
    times = (0.36, 0.52, 0.78)


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
        # "A model learns only from the table it is given."
        self.play(FadeIn(cells), FadeIn(table_name), run_time=self.share(0.12))
        self.play(GrowArrow(arrow_in), FadeIn(box), FadeIn(name), run_time=self.share(0.12))
        self.play(GrowArrow(arrow_out), FadeIn(output, shift=0.2 * RIGHT), run_time=self.share(0.1))
        # "If the table is wrong,"
        at(self, 0.4)
        self.play(bad.animate.set_fill(VERMILION, 0.8), run_time=self.share(0.08))
        # "the model learns that too,"
        at(self, 0.55)
        self.add(fault)
        self.play(fault.animate.move_to(box.get_center()), run_time=self.share(0.12))
        # "and nothing in its output says so."
        at(self, 0.75)
        self.play(fault.animate.move_to(output.get_center()).set_opacity(0), run_time=self.share(0.1))
        self.play(FadeIn(quiet, shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene03(VideoScene):
    number = 3

    def construct(self):
        # Schematic: one station as a card, after the survey page's diagram.
        head = label("one simulated coastal survey", 44, PURPLE, weight=BOLD).to_edge(UP, buff=0.7)
        row = label("each row is a station: one visit to one place", 34, INK, weight=BOLD).next_to(head, DOWN, 0.4)
        parts = VGroup(panel("where and when", ["site", "date, season"], BLUE, 3.6),
                       panel("the water", ["temperature", "salinity", "chlorophyll"], SKY, 3.0),
                       panel("the seabed", ["mud, sand,", "gravel or rock"], ORANGE, 3.0),
                       panel("the species", ["how many", "were counted"], VERMILION, 3.0)
                       ).arrange(RIGHT, buff=0.25).move_to([0, -1.2, 0])
        # "The course works on one simulated coastal survey."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "Each row is a station: one visit to one place."
        at(self, 0.2)
        self.play(FadeIn(row), run_time=self.share(0.08))
        # "It records where and when, the water's temperature, salinity and chlorophyll,
        # the type of seabed, and the count of one species."
        for part, when in zip(parts, [0.45, 0.55, 0.78, 0.88]):
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
        # "Columns come in different kinds. Some are quantities, some are categories, and some are neither."
        self.play(FadeIn(kinds[0], shift=0.2 * DOWN), run_time=self.share(0.06))
        at(self, 0.22)
        self.play(FadeIn(kinds[1], shift=0.2 * DOWN), run_time=self.share(0.06))
        at(self, 0.34)
        self.play(FadeIn(kinds[2], shift=0.2 * DOWN), run_time=self.share(0.06))
        # "As numbers, December and January are eleven months apart;"
        at(self, 0.45)
        self.play(Create(line), FadeIn(dots), FadeIn(names), run_time=self.share(0.1))
        self.play(GrowFromCenter(apart), FadeIn(apart_name), run_time=self.share(0.08))
        # "in the sea they are neighbours."
        at(self, 0.76)
        moves = [d.animate.move_to(s) for d, s in zip(dots, spots)]
        moves += [n.animate.move_to(centre + (radius + 0.4) * (s - centre) / radius) for n, s in zip(names, spots)]
        self.play(FadeOut(apart), FadeOut(apart_name), ReplacementTransform(line, ring), *moves,
                  run_time=self.share(0.14))
        self.play(FadeIn(near, scale=0.8), run_time=self.share(0.06))
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
        # "The raw file has 815 rows. Remove the duplicates and 800 remain.
        # But they come from only 160 sites, each visited several times."
        for group, when in zip(bars, [0.05, 0.35, 0.62]):
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
        warn = card("rows are not independent observations", VERMILION, 32).to_edge(DOWN, buff=0.45)
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
        together = VGroup(frames, names).move_to([0, 0.25, 0])
        for s, column in enumerate(blocks):
            column.move_to(frames[s])
        self.play(FadeIn(head), FadeIn(squares), run_time=self.share(0.1))
        # "Visits to the same site share their water and their seabed, so they are alike."
        at(self, 0.12)
        self.play(*[sq.animate.set_fill(SITE_COLOURS[o], 0.8) for sq, o in zip(squares, owners)],
                  run_time=self.share(0.15))
        # "The row count is not the number of independent observations."
        at(self, 0.44)
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
        # "Before modelling, look."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "The smallest value of salinity is minus 999,"
        at(self, 0.2)
        self.play(FadeIn(cols), run_time=self.share(0.1))
        at(self, 0.3)
        self.play(cols[0][1].animate.set_color(VERMILION), run_time=self.share(0.06))
        # "and its average is 2.24."
        at(self, 0.58)
        self.play(cols[1][1].animate.set_color(VERMILION), run_time=self.share(0.06))
        # "No sea is that fresh."
        at(self, 0.82)
        self.play(FadeIn(fresh, shift=0.2 * UP), run_time=self.share(0.08))
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
        # "Minus 999 was written to mean "missing"."
        self.play(FadeIn(meaning, shift=0.2 * UP), run_time=self.share(0.12))
        # "Mark it missing,"
        at(self, 0.45)
        self.play(FadeOut(cols[0]), FadeIn(missing), run_time=self.share(0.1))
        # "and the average is 33.9."
        at(self, 0.72)
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
        chips.arrange_in_grid(3, 4, buff=(0.5, 0.45)).move_to([0, 0.2, 0])
        head = label(f"{len(spellings)} spellings", 44, INK, weight=BOLD).to_edge(UP, buff=0.6)
        xs = [-4.8, -1.6, 1.6, 4.8]
        headings = VGroup(*[label(t, 40, colour[t], weight=BOLD).move_to([x, 2.3, 0])
                            for t, x in zip(SUBSTRATE_TYPES, xs)])
        head4 = label(f"{len(SUBSTRATE_TYPES)} seabed types", 44, INK, weight=BOLD).to_edge(UP, buff=0.6)
        seen = {t: 0 for t in SUBSTRATE_TYPES}
        step = max(c.height for c in chips) + 0.2   # a gap between the chips in each column
        moves = []
        for chip, s in zip(chips, spellings):
            t = kind[s]
            moves.append(chip.animate.move_to([xs[SUBSTRATE_TYPES.index(t)], 1.3 - step * seen[t], 0]))
            seen[t] += 1
        warn = card("a model sees twelve different habitats", VERMILION, 32).to_edge(DOWN, buff=0.3)
        # "Count every category, too."
        self.play(FadeIn(head), LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.1),
                  run_time=self.share(0.2))
        # "Four seabed types were written twelve different ways,"
        at(self, 0.25)
        self.play(ReplacementTransform(head, head4), FadeIn(headings), *moves, run_time=self.share(0.18))
        # "and a model would treat each spelling as a different habitat."
        at(self, 0.62)
        self.play(FadeIn(warn, shift=0.2 * UP), run_time=self.share(0.1))
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
        # "Chlorophyll is missing most often in winter."
        self.play(Create(axes.x_axis), FadeIn(names), FadeIn(key[0]), GrowFromEdge(all_rows, DOWN), run_time=self.share(0.15))
        # "Drop every incomplete row, as most modelling functions do by default,"
        at(self, 0.25)
        self.play(FadeIn(key[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in complete], lag_ratio=0.2),
                  FadeIn(values), run_time=self.share(0.2))
        # "and you lose 10% of the stations,"
        at(self, 0.66)
        self.play(FadeIn(overall), run_time=self.share(0.08))
        # "but 20% of winter."
        at(self, 0.86)
        self.play(Create(ring), FadeIn(winter), run_time=self.share(0.08))
        self.finish()


class Scene12(VideoScene):
    number = 12

    def construct(self):
        # Schematic: the question every fix starts from.
        question = VGroup(label("Why is this value", 60, INK, weight=BOLD),
                          label("missing, or strange?", 60, INK, weight=BOLD)).arrange(DOWN, buff=0.2)
        question.move_to([0, 1.2, 0])
        decides = label("the answer decides the fix", 40, GREEN, weight=BOLD).move_to([0, -0.9, 0])
        some = label("and some gaps cannot be fixed at all", 36, VERMILION, weight=BOLD).move_to([0, -2.0, 0])
        # "So every fix starts with one question: why is this value missing, or strange?"
        self.play(FadeIn(question, shift=0.2 * DOWN), run_time=self.share(0.2))
        # "The answer decides the fix,"
        at(self, 0.6)
        self.play(FadeIn(decides, shift=0.2 * UP), run_time=self.share(0.1))
        # "and some gaps cannot be fixed at all."
        at(self, 0.8)
        self.play(FadeIn(some, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene13(VideoScene):
    number = 13

    def construct(self):
        # Schematic: the recipe's three stages, after the scaling-and-encoding page's diagram.
        chips = VGroup(card("standardise", SKY, 30), card("log", SKY, 30), card("columns of 0s and 1s", SKY, 30)
                       ).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.6)
        stages = VGroup(panel("1 specify", ["list the steps"], BLUE, 3.3, 2.2, 28),
                        panel("2 estimate", ["the numbers they need,", "from training data only"], ORANGE, 4.5, 2.2, 28),
                        panel("3 apply", ["the same numbers,", "to any data"], GREEN, 3.7, 2.2, 28)
                        ).arrange(RIGHT, buff=0.5).move_to([0, -0.9, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), color=INK, stroke_width=4, buff=0.08)
                          for a, b in zip(stages[:-1], stages[1:])])
        name = label("a recipe", 40, INK, weight=BOLD).next_to(stages, UP, 0.4)
        # "Columns then need preparing: standardised, logged, or turned into columns of zeros and ones."
        for chip, when in zip(chips, [0.1, 0.2, 0.3]):
            at(self, when)
            self.play(FadeIn(chip, shift=0.2 * DOWN), run_time=self.share(0.05))
        # "A recipe lists these steps,"
        at(self, 0.46)
        self.play(FadeIn(name), FadeIn(stages[0], shift=0.2 * UP), run_time=self.share(0.08))
        # "works out the numbers they need from the training data only,"
        at(self, 0.6)
        self.play(GrowArrow(arrows[0]), FadeIn(stages[1], shift=0.2 * UP), run_time=self.share(0.08))
        # "and applies them to any data."
        at(self, 0.86)
        self.play(GrowArrow(arrows[1]), FadeIn(stages[2], shift=0.2 * UP), run_time=self.share(0.08))
        self.finish()


class Scene14(KeyPointScene):
    number, point = 14, 2


# Testing a model honestly (scenes 15–23) ------------------------------------------------

class Scene15(VideoScene):
    number = 15

    def construct(self):
        # Schematic: the three roles of the data.
        head = label("tested on data it has not seen", 44, INK, weight=BOLD).to_edge(UP, buff=0.8)
        roles = VGroup(panel("training", ["fits the model"], BLUE, 3.6, 2.0, 30),
                       panel("validation", ["chooses between", "models"], ORANGE, 3.6, 2.0, 30),
                       panel("test", ["reports the result,", "once"], GREEN, 3.6, 2.0, 30)
                       ).arrange(RIGHT, buff=0.5).move_to([0, -0.4, 0])
        # "A model must be tested on data it has not seen."
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.12))
        # "Training data fits the model, validation data chooses between models,
        # and test data reports the result, once."
        for role, when in zip(roles, [0.36, 0.56, 0.76]):
            at(self, when)
            self.play(FadeIn(role, shift=0.2 * UP), run_time=self.share(0.07))
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
        before = sites_grid(lambda s, v: False).move_to([0, 0.3, 0])
        after = random_grid().move_to(before)
        head = label("a random split", 44, INK, weight=BOLD).to_edge(UP, buff=0.4)
        key = split_key().next_to(after, DOWN, 0.45)
        share = card(f"{seen}% of test stations sit at a site in training", VERMILION, 32).to_edge(DOWN, buff=0.35)
        # "Split this survey at random,"
        self.play(FadeIn(head), FadeIn(before), run_time=self.share(0.15))
        at(self, 0.2)
        self.play(ReplacementTransform(before, after), FadeIn(key), run_time=self.share(0.2))
        # "and every test station sits at a site the model trained on."
        at(self, 0.55)
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
        at(self, 0.3)
        self.play(FadeIn(asks[0]), run_time=self.share(0.08))
        # "Hold back whole sites instead, and the test sites are new to the model, as they will be in use."
        at(self, 0.52)
        self.play(FadeIn(grouped), FadeIn(heads[1]), run_time=self.share(0.1))
        self.play(Create(new), FadeIn(asks[1]), run_time=self.share(0.08))
        # "So split along what you will predict for."
        at(self, 0.86)
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
        name = label("leakage", 52, VERMILION, weight=BOLD).move_to([2.3, -1.9, 0])
        better = label("every score looks better", 36, INK, weight=BOLD).move_to([0, -2.9, 0])
        trace = label("and leaves no trace", 36, SUBDUED, weight=BOLD).next_to(better, DOWN, 0.2)
        self.play(FadeIn(train), FadeIn(model), GrowArrow(fit), FadeIn(test), Create(wall), run_time=self.share(0.12))
        # "When information from the test data reaches the model before the test,"
        at(self, 0.15)
        self.play(Create(leak), run_time=self.share(0.25))
        # "that is leakage."
        at(self, 0.45)
        self.play(FadeIn(name, scale=0.8), run_time=self.share(0.06))
        # "It makes every score look better, and it leaves no trace."
        at(self, 0.62)
        self.play(FadeIn(better, shift=0.2 * UP), run_time=self.share(0.07))
        at(self, 0.82)
        self.play(FadeIn(trace, shift=0.2 * UP), run_time=self.share(0.07))
        self.finish()


def rsq_bars(rows, colours, head_text):
    """Horizontal R² bars on a 0 to 1 scale, with each bar's value as the page prints it."""
    head = label(head_text, 40, INK, weight=BOLD).to_edge(UP, buff=0.6)
    axis = plain_axes([0, 1, 0.25], [0, 1, 1], 8.0, 0.01).move_to([1.2, -2.2, 0])
    ticks = VGroup(*[label(f"{v:g}", 24, SUBDUED).next_to(axis.c2p(v, 0), DOWN, 0.15) for v in (0, 0.5, 1)])
    axis_name = label("R² on the test data", 26, SUBDUED).next_to(ticks, DOWN, 0.15)
    bars = VGroup()
    for i, ((name, value), colour) in enumerate(zip(rows, colours)):
        y = 0.9 - 1.6 * i
        width = max(value * 8.0, 0.02)
        bar = Rectangle(width=width, height=0.9, stroke_width=0, fill_color=colour, fill_opacity=0.85)
        bar.move_to([axis.c2p(0, 0)[0] + width / 2, y, 0])
        what = label(name, 30, INK, weight=BOLD).next_to([axis.c2p(0, 0)[0], y, 0], LEFT, 0.3)
        amount = label(f"{value:.2f}", 40, INK, weight=BOLD).next_to(bar, RIGHT, 0.25)
        bars.add(VGroup(bar, what, amount))
    return head, VGroup(axis, ticks, axis_name), bars


def target_layout(scene):
    table = scene.data("target").set_index("model")["rsq"]
    return rsq_bars([("environment only", table["Environment only"]),
                     ("plus catch weight", table["Plus catch weight"])], [BLUE, VERMILION],
                    "a linear regression of the count")


class Scene19(VideoScene):
    number = 19

    def construct(self):
        # Page results: information-leakage.qmd, target leakage.
        head, axis, bars = target_layout(self)
        # "Add catch weight to a linear regression of the count,"
        self.play(FadeIn(head), FadeIn(axis), run_time=self.share(0.12))
        # "and R squared jumps from 0.28"
        at(self, 0.5)
        self.play(GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]), run_time=self.share(0.12))
        # "to 0.98."
        at(self, 0.8)
        self.play(GrowFromEdge(bars[1][0], LEFT), FadeIn(bars[1][1:]), run_time=self.share(0.12))
        self.finish()


class Scene20(VideoScene):
    number = 20

    def construct(self):
        # Page results as in scene 19; the rest schematic.
        head, axis, bars = target_layout(self)
        self.add(head, axis, bars)
        same = card("catch weight is the count, in other units", PURPLE, 34).to_edge(UP, buff=0.5)
        handed = card("each test station's answer, handed to the model", VERMILION, 32).move_to([0, -3.3, 0])
        copying = card("copying, not predicting", VERMILION, 36).move_to(handed)
        cross = Cross(bars[1][0], stroke_color=VERMILION, stroke_width=8)
        # "Catch weight is the weight of the animals that were counted: the count again, in other units."
        self.play(FadeOut(head), FadeIn(same, shift=0.2 * DOWN), run_time=self.share(0.1))
        # "So for every test station, the model is handed the answer it should predict."
        at(self, 0.45)
        self.play(FadeOut(axis), FadeIn(handed, shift=0.2 * UP), run_time=self.share(0.08))
        # "The 0.98 measures copying, not predicting."
        at(self, 0.8)
        self.play(Create(cross), bars[1].animate.set_opacity(0.35), ReplacementTransform(handed, copying),
                  run_time=self.share(0.1))
        self.finish()


class Scene21(VideoScene):
    number = 21

    def construct(self):
        # Page results: information-leakage.qmd, group leakage.
        table = self.data("group").set_index("split")["rsq"]
        head, axis, bars = rsq_bars([("random split", table["Random"]), ("grouped by site", table["Grouped by site"])],
                                    [BLUE, GREEN], "the honest model, split two ways")
        harder = card("a new site is much harder to predict", PURPLE, 32).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(head), FadeIn(axis), GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]), run_time=self.share(0.15))
        # "Keep each site whole, and the honest model's R squared falls from 0.28 to 0.08."
        at(self, 0.4)
        self.play(GrowFromEdge(bars[1][0], LEFT), FadeIn(bars[1][1:]), run_time=self.share(0.12))
        # "Predicting a new site is much harder than predicting a familiar one."
        at(self, 0.62)
        self.play(FadeOut(axis), FadeIn(harder, shift=0.2 * UP), run_time=self.share(0.1))
        self.finish()


class Scene22(VideoScene):
    number = 22

    def construct(self):
        # Schematic: the page's one question.
        head = label("one question catches every kind of leakage", 38, SUBDUED, weight=BOLD).to_edge(UP, buff=1.0)
        code = VGroup(*[RoundedRectangle(width=w, height=0.28, corner_radius=0.08, stroke_width=0, fill_color=GRID,
                                         fill_opacity=1) for w in (5.0, 3.6, 6.2, 4.4)]).arrange(DOWN, buff=0.18,
                                                                                                aligned_edge=LEFT)
        code.move_to([0, 0.5, 0])
        line = code[2]
        mark = Arrow(line.get_left() + 1.2 * LEFT, line.get_left(), color=PURPLE, stroke_width=6, buff=0.1)
        question = VGroup(label("Does this line of code use information", 44, INK, weight=BOLD),
                          label("from the rows I intend to test on?", 44, INK, weight=BOLD)).arrange(DOWN, buff=0.2)
        question.move_to([0, -2.0, 0])
        self.play(FadeIn(head), FadeIn(code), run_time=self.share(0.15))
        # "Does this line of code use information from the rows I intend to test on?"
        at(self, 0.42)
        self.play(line.animate.set_fill(PURPLE, 0.6), GrowArrow(mark), run_time=self.share(0.1))
        self.play(FadeIn(question, shift=0.2 * UP), run_time=self.share(0.15))
        self.finish()


class Scene23(KeyPointScene):
    number, point = 23, 3


# The quiz (scenes 24–25) ----------------------------------------------------------------

class Scene24(QuizScene):
    number = 24
    question = ("Gaps in chlorophyll are filled with", "the median of the whole survey,",
                "then it is split into training and test.", "What is wrong?")


class Scene25(VideoScene):
    number = 25

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


# The recap (scenes 26–28) and the end card (scene 29) -----------------------------------

class Scene26(RecapScene):
    number, point = 26, 1


class Scene27(RecapScene):
    number, point = 27, 2


class Scene28(RecapScene):
    number, point = 28, 3


class Scene29(EndCardScene):
    number = 29
