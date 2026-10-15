"""Shared look and timing for the Manim scenes of every video.

Each video's scenes.py starts with

    from mlbasic_video import *

and defines one class per script scene, named after it (Scene05 for "## Scene 5").
The class declares its number, and VideoScene gives it the length of that scene's
narration, so the animation is timed to the voice. The narration is the Gemini take
in audio/scene-NN.wav when its text is current, and otherwise the draft voice in
audio/draft/ (tools/draft-narration.py), exactly as tools/rough-cut.py chooses:

    class Scene05(VideoScene):
        number = 5

        def construct(self):
            self.play(Create(line), run_time=self.share(0.3))  # 30% of the narration
            self.finish()                                        # hold to the end

Render from the video folder, where manim.cfg sends the output to visuals/scenes/:

    cd _videos/05-generalisation
    manim -ql scenes.py Scene05     # quick draft, 480p
    manim -qh scenes.py             # every scene, 1080p

Every number comes from visuals/data/*.csv, written by tools/figures-for-video.R from
the pages' own results (on the course's simulated survey). Anything drawn without a
CSV is schematic: shapes only, no numbers that could be read as results.
"""

import sys
import wave
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *  # noqa: F401,F403  (re-exported for the scene files)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "tools"))
from mlbasic_theme import ML_PALETTE  # noqa: E402  the site's Okabe-Ito palette
from video_script import SHOUTS, cheer_plan, narration_audio, read_script  # noqa: E402
sys.path.insert(0, str(ROOT / "_videos"))
from sea_friends import grid  # noqa: E402

SERIES = "Machine Learning Basics for Marine Science"
SITE = "hi-digital-ml-ai.github.io/ml-basic"   # GitHub Pages. The end cards show only
                                              # this: page paths carry section numbers,
                                              # which go in the description
MUSIC = ROOT / "_videos" / "intro-music.wav"

# The site's font. Pango silently substitutes another font if this name is wrong,
# so check the first render; "Inter" is the fallback named in .claude/videos.md.
FONT = "Source Sans 3"

BACKGROUND = "#FFFFFF"   # the same white as the re-exported ggplot figures
INK = "#1F2A33"          # body text
SUBDUED = "#55606A"      # secondary text, as in R/theme.R
GRID = "#D5DCE1"         # axes and guides, a little darker than the site grid for video

BLUE, ORANGE, GREEN = ML_PALETTE["blue"], ML_PALETTE["orange"], ML_PALETTE["green"]
VERMILION, PURPLE, SKY = ML_PALETTE["vermilion"], ML_PALETTE["purple"], ML_PALETTE["sky"]
YELLOW, GREY = ML_PALETTE["yellow"], ML_PALETTE["grey"]

config.background_color = BACKGROUND
Text.set_default(font=FONT, color=INK)
MathTex.set_default(color=INK)
Line.set_default(color=GRID)
DashedLine.set_default(color=GREY)


def label(text, size=36, color=INK, weight=NORMAL, **kwargs):
    """Text in the series style. Sizes are Manim font sizes; 36 is body text.

    Set large and scaled down: Pango drops the spaces between words when Manim asks
    it for small sizes directly ("true value" came out as "truevalue").
    """
    return Text(text, font_size=4 * size, color=color, weight=weight, **kwargs).scale(0.25)


def title(text, size=52):
    return label(text, size=size, weight=BOLD)


def number(value, digits=1, size=36, color=INK):
    """A number exactly as the pages round it: never re-rounded differently."""
    return label(f"{value:.{digits}f}", size=size, color=color)


def plated(text, buff=0.1):
    """Text on a plate of the background colour, so it reads over a chart's dots and
    lines. The plate sits above the chart (z-index 5), below a marker kept on top (10)."""
    plate = SurroundingRectangle(text, buff=buff, corner_radius=0.08, stroke_width=0,
                                 fill_color=BACKGROUND, fill_opacity=0.88)
    return VGroup(plate, text).set_z_index(5)


class VideoScene(Scene):
    """A scene whose length is its narration. Subclasses set `number`."""

    number = None

    def setup(self):
        folder = Path(sys.modules[type(self).__module__].__file__).resolve().parent
        self.folder = folder
        self.script = read_script(folder / "script.md")
        scene = self.script.scenes[self.number - 1]
        wav, _ = narration_audio(folder, self.script, scene)
        if wav is None:
            raise FileNotFoundError(f"scene {self.number} has no narration: run "
                                    f"tools/draft-narration.py or tools/narrate.py")
        with wave.open(str(wav)) as w:
            self.narration = w.getnframes() / w.getframerate()
        self.pause = self.script.scenes[self.number - 1].pause_after
        self.cheers = cheer_plan(folder, scene)
        # Room at the foot of the frame for the animals, in every scene that has them.
        self.lift = 0.6 if any(s.cheer for s in self.script.scenes) else 0.0

    def share(self, fraction):
        """A run time as a fraction of this scene's narration."""
        return fraction * self.narration

    def finish(self):
        """Hold the last frame until the narration ends."""
        left = self.narration - self.time
        if left > 1 / config.frame_rate:
            self.wait(left)

    def celebrate(self):
        """After the narration, the scene's animals pop up with their sounds.

        tools/rough-cut.py starts each sound at the same moment, from the same plan.
        """
        if not self.cheers:
            return
        one = len(self.cheers) == 1
        spots = ([np.array([0.0, -2.95, 0])] if one else
                 [np.array([x, -3.2, 0]) for x in (-4.6, 0.0, 4.6)])
        clock = ValueTracker(0.0)
        for (animal, sound, move, start), spot in zip(self.cheers, spots):
            figure, aside = sprite(animal, 1.6 if one else 1.4), 3.8 if one else 0
            if sound in SHOUTS:
                parts, update = shout_cheer(figure, spot, aside, SHOUTS[sound], move)
            elif sound == "fireworks":
                parts, update = fireworks_cheer(figure, spot, aside, move)
            else:
                parts, update = CHEERS[sound](figure, spot, aside)
            group = VGroup(*parts)
            group.add_updater(lambda m, u=update, s=start: u(clock.get_value() - s))
            update(-1.0)
            self.add(group)
        length = max(c[-1] for c in self.cheers) + CHEER_LENGTH
        self.play(clock.animate.set_value(length), run_time=length, rate_func=linear)

    def data(self, name):
        """A CSV written by tools/figures-for-video.R, from the pages' own results."""
        path = self.folder / "visuals" / "data" / f"{name}.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"{path} is missing: run Rscript tools/figures-for-video.R {self.folder.name}")
        return pd.read_csv(path)


class TitleScene(Scene):
    """The opening every video shares: series name and title, over the jingle.

    Each scenes.py has `class Title(TitleScene): pass`; the text comes from the
    script's front matter and the length from _videos/intro-music.wav. No section
    number: numbers can change, so they belong in the YouTube title and description.
    """

    def construct(self):
        folder = Path(sys.modules[type(self).__module__].__file__).resolve().parent
        meta = read_script(folder / "script.md").meta
        with wave.open(str(MUSIC)) as w:
            length = w.getnframes() / w.getframerate()
        main, _, sub = meta["title"].partition(": ")

        rule = Line(3.2 * LEFT, 3.2 * RIGHT, color=BLUE, stroke_width=6)
        series = label(SERIES, 30, SUBDUED)
        head = title(main, 80)
        tagline = label(sub, 42, SUBDUED) if sub else VGroup()
        VGroup(series, head, rule, tagline).arrange(DOWN, buff=0.35)
        rule.shift(0.1 * DOWN)
        tagline.shift(0.15 * DOWN)

        # Timed to the jingle: the text arrives with the skipping run, the rule with the final chord.
        self.play(FadeIn(series, shift=0.2 * DOWN), run_time=0.4)
        self.play(FadeIn(head, shift=0.3 * UP), run_time=0.5)
        self.play(GrowFromCenter(rule), FadeIn(tagline), run_time=0.6)
        self.wait(max(length - self.time, 0.1))


# The cheers ---------------------------------------------------------------------------
#
# At each key point an animal pops up with a sound (tools/make-cheers.py), and after
# the recap all three do. Which animals, which sounds and when come from
# tools/video_script.py (cheer_plan), which tools/rough-cut.py reads too, so the
# sound always lands on its animal. Each cheer is drawn as a function of the time
# since it began, so three can overlap.

CHEER_LENGTH = 2.4    # seconds each cheer moves for; the sounds last 2.2 to 2.8 s
SPARKS = [ORANGE, VERMILION, YELLOW, SKY, PURPLE, GREEN, BLUE]


def sprite(name, height=1.5):
    """A pixel-art animal from _videos/sea_friends.py, `height` units tall."""
    rows, colours = grid(name)
    size = height / len(rows)
    pixels = VGroup()
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != ".":
                # A hair larger than the grid, so no seams show between pixels.
                pixels.add(Square(size * 1.04, stroke_width=0, fill_color=colours[c],
                                  fill_opacity=1).move_to([x * size, -y * size, 0]))
    return pixels.move_to(ORIGIN)


def resting(mob):
    """Keep `mob`'s shape as drawn, for popped() and bubble_pop() to start from each frame."""
    mob.rest = mob.copy()
    return mob


def popped(animal, spot, t, hop=0.0, turn=0.0, squash=1.0):
    """The animal grown in over 0.3 s with a little overshoot, `hop` units up, tilted by
    `turn` radians and squashed sideways by `squash` (below 0 shows it mirrored, as it
    turns round in a spin)."""
    grow = rate_functions.ease_out_back(min(max(t / 0.3, 0), 1)) if t >= 0 else 0
    animal.become(animal.rest)
    animal.set_opacity(1 if t >= 0 else 0)
    animal.scale(max(grow, 0.001))
    if squash != 1.0:
        animal.stretch(np.sign(squash) * max(abs(squash), 0.03), 0)
    if turn:
        animal.rotate(turn)
    animal.move_to(spot + hop * UP)


def clap_cheer(animal, spot, aside):
    """The animal bounces with the applause, a star flashing on either side."""
    resting(animal)
    reach = animal.width / 2 + 0.45
    stars = VGroup(*[Star(4, outer_radius=0.3, inner_radius=0.09, color=ORANGE,
                          fill_opacity=1, stroke_width=0) for _ in (-1, 1)])

    def update(t):
        beat = abs(np.sin(np.pi * 4.6 * (t - 0.35))) if 0.35 <= t <= 1.95 else 0
        popped(animal, spot, t, 0.25 * beat)
        stars.set_opacity(min(1, 1.5 * beat) if t >= 0.35 else 0)
        for s, d in zip(stars, (-1, 1)):
            s.scale_to_fit_height(0.2 + 0.4 * beat).move_to(spot + d * reach * RIGHT + 0.45 * UP)

    return [animal, stars], update


def speech_bubble(words, size, tail, reach=0.45):
    """`words` in a white speech bubble, its tail pointing along `tail` (DOWN, or DOWN
    and to one side) from the bubble's lower edge."""
    text = label(words, size, VERMILION, weight=BOLD)
    box = SurroundingRectangle(text, buff=0.22, corner_radius=0.22, color=INK, stroke_width=3,
                               fill_color=WHITE, fill_opacity=1)
    root = box.get_bottom() + 0.3 * tail[0] * box.width * RIGHT
    tip = root + reach * normalize(tail)
    left, right = root + 0.18 * LEFT + 0.02 * UP, root + 0.18 * RIGHT + 0.02 * UP
    # The tail's fill covers the box's outline where they meet; its two sides are lines.
    fill = Polygon(left, right, tip, stroke_width=0, fill_color=WHITE, fill_opacity=1)
    sides = VGroup(Line(left + 0.02 * DOWN, tip, color=INK, stroke_width=3),
                   Line(right + 0.02 * DOWN, tip, color=INK, stroke_width=3))
    return VGroup(box, fill, sides, text)


def shout_cheer(animal, spot, aside, words, move):
    """The animal calls out `words` in a speech bubble beside it, or above it when
    `aside` is 0 (the recap, where the animals stand close together), and moves:
    "jump" jumps for joy, "spin" turns round twice, "wiggle" rocks from side to side."""
    resting(animal)
    side = 1 if spot[0] <= 0 else -1
    # Both places keep the bubble below the key point's answer and the recap's last line.
    if aside:
        bubble = speech_bubble(words, 40, DOWN + 0.8 * -side * RIGHT)
        place = spot + side * (animal.width / 2 + 0.5 + bubble.width / 2) * RIGHT + 0.45 * UP
    else:
        bubble = speech_bubble(words, 30, DOWN, reach=0.3)
        place = spot + (animal.height / 2 + 0.75) * UP
    resting(bubble)
    lift = 1.0 if aside else 0.45    # in the recap, the jumps stay under the bubble

    def update(t):
        hop = turn = 0.0
        squash = 1.0
        if move == "jump":
            if 0.3 <= t <= 0.9:
                hop = 0.7 * np.sin(np.pi * (t - 0.3) / 0.6)
            elif 1.0 <= t <= 1.4:
                hop = 0.3 * np.sin(np.pi * (t - 1.0) / 0.4)
        elif move == "spin":
            u = min(max((t - 0.3) / 1.2, 0), 1)
            squash = np.cos(2 * TAU * rate_functions.smooth(u))
            hop = 0.35 * np.sin(np.pi * u)
        elif move == "wiggle":
            if 0.3 <= t <= 1.9:
                turn = 0.32 * np.sin(TAU * 3 * (t - 0.3)) * (1 - (t - 0.3) / 1.6)
        popped(animal, spot, t, lift * hop, turn, squash)
        grow = rate_functions.ease_out_back(min(max((t - 0.15) / 0.3, 0), 1))
        bubble.become(bubble.rest)
        bubble.set_opacity(1 if t >= 0.15 else 0)
        bubble.scale(max(grow, 0.001)).move_to(place)

    return [animal, bubble], update


def bubbles_cheer(animal, spot, aside):
    """Bubbles stream up on either side of the animal, wobbling as they rise, and pop
    before they reach the text above: wider beside a lone animal than in the recap."""
    resting(animal)
    rng = np.random.default_rng(11)
    rise, spread = (1.5, (0.55, 1.5)) if aside else (1.1, (0.5, 0.85))
    stream = []
    for k in range(16):
        r = rng.uniform(0.07, 0.16)
        bubble = VGroup(Circle(r, color=SKY, stroke_width=3, fill_color=SKY, fill_opacity=0.18),
                        Dot([-0.35 * r, 0.35 * r, 0], radius=0.25 * r, color=WHITE))
        stream.append((bubble, 0.1 + 1.6 * k / 16 + rng.uniform(0, 0.08),
                       (-1) ** k * rng.uniform(*spread) * animal.width, rng.uniform(0, TAU),
                       rng.uniform(0.9, 1.3)))

    def update(t):
        hop = 0.12 * abs(np.sin(np.pi * 3 * (t - 0.3))) if 0.3 <= t <= 1.9 else 0
        popped(animal, spot, t, hop)
        for bubble, born, x, phase, pace in stream:
            age = (t - born) * pace
            seen = 0.0 if age < 0 or age > 1 else min(1.0, (1 - age) / 0.15)
            bubble[0].set_stroke(opacity=seen).set_fill(opacity=0.18 * seen)
            bubble[1].set_fill(opacity=seen)
            if seen:
                bubble.scale_to_fit_height(bubble[0].radius * 2 * (1 + 0.4 * age))
                bubble.move_to(spot + (x + 0.12 * np.sin(phase + 9 * age)) * RIGHT
                               + (rise * age - 0.45) * UP)

    return [animal, *[b for b, *_ in stream]], update


def flown(after, pace):
    """How far a spark has flown, from 0 to 1, `after` seconds after it set off."""
    return 1 - np.exp(-after / pace)


def fading(after, last):
    """A spark's opacity: full, then fading over the last half second of `last`."""
    return min(1.0, max(0.0, 2 * (last - after)))


# Each burst style returns its sparks and how they move, `after` seconds after the bang
# at `burst` (before the bang, `after` is negative and they are hidden). `size` is 1
# beside a lone animal and 0.5 in the recap, where the burst must stay small.

def peony_burst(size):
    """Two rings of coloured stars."""
    sparks = VGroup()
    for ring, (n, reach) in enumerate([(18, 1.0), (10, 0.55)]):
        for k in range(n):
            angle = TAU * (k + 0.5 * ring) / n
            sparks.add(Dot(radius=0.085 - 0.02 * ring, color=SPARKS[(k + ring) % len(SPARKS)]))
            sparks[-1].way = size * reach * np.array([np.cos(angle), np.sin(angle), 0])

    def move(after, burst):
        for s in sparks:
            s.move_to(burst + flown(max(after, 0), 0.22) * s.way + 0.35 * max(after, 0) ** 2 * DOWN)
            s.set_opacity(fading(after, 1.6) if after >= 0 else 0)

    return sparks, move


def willow_burst(size):
    """Golden stars that trail behind them and droop like a willow's branches."""
    rng = np.random.default_rng(5)
    heads, trails = VGroup(), VGroup()
    for k in range(24):
        angle = TAU * k / 24 + rng.uniform(-0.1, 0.1)
        heads.add(Dot(radius=0.06, color=ORANGE))
        heads[-1].way = size * rng.uniform(0.75, 1.0) * np.array([np.cos(angle), np.sin(angle), 0])
        trails.add(Line(LEFT, RIGHT, color=ORANGE, stroke_width=4 * max(size, 0.6)))

    def at(way, after, burst):
        return burst + flown(after, 0.3) * way + 0.45 * size * after ** 2 * DOWN

    def move(after, burst):
        for head, trail in zip(heads, trails):
            if after < 0:
                head.set_opacity(0).move_to(burst)
                trail.set_stroke(opacity=0)
                continue
            tip = at(head.way, after, burst)
            head.move_to(tip).set_opacity(fading(after, 1.9))
            trail.put_start_and_end_on(at(head.way, max(after - 0.5, 0), burst), tip + 1e-4 * UP)
            trail.set_stroke(opacity=0.55 * fading(after, 1.9))

    return VGroup(trails, heads), move


def crossette_burst(size):
    """Six stars fly out, then each splits into four smaller ones in a cross."""
    split = 0.45
    colours = [VERMILION, BLUE, GREEN, PURPLE, ORANGE, SKY]
    mains, children = VGroup(), VGroup()
    for k, colour in enumerate(colours):
        angle = TAU * (k + 0.5) / 6
        mains.add(Dot(radius=0.1, color=colour))
        mains[-1].way = 0.6 * size * np.array([np.cos(angle), np.sin(angle), 0])
        for j in range(4):
            turn = angle + TAU * (j + 0.5) / 4
            children.add(Dot(radius=0.065, color=colour))
            children[-1].parent = mains[-1]
            children[-1].way = 0.42 * size * np.array([np.cos(turn), np.sin(turn), 0])

    def main_at(main, after, burst):
        return burst + flown(after, 0.2) * main.way + 0.3 * after ** 2 * DOWN

    def move(after, burst):
        for main in mains:
            main.move_to(main_at(main, max(after, 0), burst))
            main.set_opacity(1 if 0 <= after < split else 0)
        for child in children:
            later = after - split
            start = main_at(child.parent, split, burst)
            child.move_to(start + flown(max(later, 0), 0.18) * child.way
                          + 0.35 * max(later, 0) ** 2 * DOWN)
            child.set_opacity(fading(later, 1.4) if later >= 0 else 0)

    return VGroup(mains, children), move


def heart_burst(size):
    """Stars that spread into a heart, which holds its shape as it fades."""
    sparks = VGroup()
    for k in range(30):
        a = TAU * k / 30
        x = 16 * np.sin(a) ** 3
        y = 13 * np.cos(a) - 5 * np.cos(2 * a) - 2 * np.cos(3 * a) - np.cos(4 * a)
        sparks.add(Dot(radius=0.075, color=VERMILION if k % 2 else PURPLE))
        # Smaller than a peony and set low, as it holds its shape near the text above.
        sparks[-1].way = size * 0.055 * np.array([x, y, 0])

    def move(after, burst):
        for s in sparks:
            s.move_to(burst + flown(max(after, 0), 0.25) * s.way + 0.12 * max(after, 0) ** 2 * DOWN)
            s.set_opacity(fading(after, 1.7) if after >= 0 else 0)

    return sparks, move


def glitter_burst(size):
    """Little four-pointed stars that twinkle as they drift down, with the crackle."""
    rng = np.random.default_rng(7)
    sparks = VGroup()
    for k in range(26):
        angle = TAU * k / 26 + rng.uniform(-0.12, 0.12)
        star = Star(4, outer_radius=0.13, inner_radius=0.04, stroke_width=0, fill_opacity=1,
                    color=[ORANGE, SKY, BLUE, VERMILION, GREEN][k % 5])
        star.way = size * rng.uniform(0.55, 1.0) * np.array([np.cos(angle), np.sin(angle), 0])
        star.phase, star.rate = rng.uniform(0, TAU), rng.uniform(9, 15)
        sparks.add(resting(star))

    def move(after, burst):
        for s in sparks:
            twinkle = abs(np.sin(s.rate * after + s.phase)) if after > 0.25 else 1.0
            s.become(s.rest).scale(max(0.45 + 0.75 * twinkle, 0.01))
            s.move_to(burst + flown(max(after, 0), 0.22) * s.way + 0.3 * max(after, 0) ** 2 * DOWN)
            s.set_opacity((0.3 + 0.7 * twinkle) * fading(after, 1.9) if after >= 0 else 0)

    return sparks, move


BURSTS = {"peony": peony_burst, "willow": willow_burst, "crossette": crossette_burst,
          "heart": heart_burst, "glitter": glitter_burst}


def fireworks_cheer(animal, spot, aside, style="peony"):
    """A rocket rises and bursts `aside` units to the animal's side, or above it when
    `aside` is 0, in one of the styles in video_script.FIREWORKS. The bang comes 0.75 s
    in, with the sound's."""
    resting(animal)
    side = 1 if spot[0] <= 0 else -1
    launch = spot + 0.6 * UP
    # Above, it leans outwards, clear of the recap's badges.
    burst = spot + (side * aside * RIGHT + 0.7 * UP if aside
                    else np.sign(spot[0]) * 0.8 * RIGHT + 1.55 * UP)
    size = 1.0 if aside else 0.5
    rocket = Dot(radius=0.07, color=ORANGE)
    trail = Line(launch, launch, color=ORANGE, stroke_width=4)
    sparks, move = BURSTS[style](size)

    def update(t):
        hop = 0.3 * np.sin(np.pi * (t - 0.75) / 0.35) if 0.75 <= t <= 1.1 else 0
        popped(animal, spot, t, hop)
        flying = 0.05 <= t < 0.75
        u = rate_functions.ease_out_sine(min(max((t - 0.05) / 0.7, 0), 1))
        head = launch + u * (burst - launch)
        rocket.move_to(head).set_opacity(1 if flying else 0)
        trail.put_start_and_end_on(launch + max(u - 0.25, 0) * (burst - launch) + 1e-4 * UP, head)
        trail.set_stroke(opacity=0.8 if flying else 0)
        move(t - 0.75, burst)

    return [trail, rocket, sparks, animal], update


# The effects; a shout (video_script.SHOUTS) is drawn by shout_cheer with its move,
# and a firework by fireworks_cheer with its style.
CHEERS = {"clap": clap_cheer, "fireworks": fireworks_cheer, "bubbles": bubbles_cheer}


# Scenes every video shares ------------------------------------------------------------
#
# The opening promises three things and each is kept by a key-point scene, then all
# three are recapped. The wording lives once, in the video's scenes.py, as
#
#     PROMISES = [...]   # scene 1: what the viewer will learn
#     ANSWERS = [...]    # the key-point scenes: the answer, "\n" between lines
#     RECAP = [...]      # the recap: one short line each
#
# and these classes read it from there.

def video_constant(scene, name):
    """A constant from the scenes.py that defined this scene, such as PROMISES."""
    return getattr(sys.modules[type(scene).__module__], name)


def badge(n, radius=0.33):
    return VGroup(Circle(radius, color=BLUE, fill_opacity=1, stroke_width=0),
                  label(str(n), int(radius * 97), BACKGROUND, weight=BOLD))


def tick(size=0.55):
    box = RoundedRectangle(width=size, height=size, corner_radius=0.08, stroke_color=GREEN,
                           stroke_width=4)
    mark = VMobject(color=GREEN, stroke_width=8).set_points_as_corners(
        [[-0.16, 0.0, 0], [-0.04, -0.14, 0], [0.2, 0.16, 0]]).scale(size / 0.55).move_to(box)
    return box, mark


class LearnScene(VideoScene):
    """Scene 1: "In this video", then the three promises as the narration names them.

    `times` are the fractions of the narration at which each promise is spoken.
    """

    times = (0.2, 0.45, 0.68)

    def construct(self):
        head = title("In this video", 56).to_edge(UP, buff=1.0)
        rows = VGroup()
        for i, text in enumerate(video_constant(self, "PROMISES"), 1):
            rows.add(VGroup(badge(i), label(text, 40)).arrange(RIGHT, buff=0.45))
        rows.arrange(DOWN, buff=0.7, aligned_edge=LEFT).next_to(head, DOWN, 0.9)
        if rows.width > 12.4:
            rows.scale_to_fit_width(12.4)
        rows.set_x(0)

        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.08))
        for row, at in zip(rows, self.times):
            self.wait(max(self.share(at) - self.time, 0.01))
            self.play(FadeIn(row[0], scale=0.6), FadeIn(row[1], shift=0.3 * RIGHT),
                      run_time=self.share(0.08))
        self.finish()


class KeyPointScene(VideoScene):
    """One promise from the opening, kept: its badge and question, then the answer."""

    point = None

    def construct(self):
        tag = label(f"Key point {self.point} of 3", 34, BLUE, weight=BOLD).to_edge(
            UP, buff=1.1 - self.lift)
        promise = VGroup(badge(self.point),
                         label(video_constant(self, "PROMISES")[self.point - 1], 38, SUBDUED)
                         ).arrange(RIGHT, buff=0.4).next_to(tag, DOWN, 0.7)
        answer_text = video_constant(self, "ANSWERS")[self.point - 1]
        lines = [label(t, 50, INK, weight=BOLD) for t in answer_text.split("\n")]
        answer = VGroup(*lines).arrange(DOWN, buff=0.25).next_to(promise, DOWN, 0.9)
        box, mark = tick(0.8)
        box.next_to(answer, LEFT, 0.5)
        mark.move_to(box)
        group = VGroup(answer, box, mark)
        if group.width > 12.4:           # keep the tick clear of the frame's edge
            group.scale_to_fit_width(12.4)
        group.set_x(0)

        # "Key point one."
        self.play(FadeIn(tag, shift=0.2 * DOWN), FadeIn(promise), run_time=self.share(0.12))
        # The answer, as the narration says it.
        self.play(LaggedStart(*[FadeIn(l, shift=0.2 * UP) for l in lines], lag_ratio=0.5),
                  FadeIn(box), run_time=self.share(0.4))
        self.play(Create(mark), run_time=self.share(0.1))
        self.finish()
        self.celebrate()


def recap_rows(recap, lift=0.0):
    head = title("The three key points", 56).to_edge(UP, buff=0.9 - lift)
    rows = VGroup()
    for i, text in enumerate(recap, 1):
        box, mark = tick()
        rows.add(VGroup(badge(i, 0.28), box, mark, label(text, 38)))
        rows[-1][1].next_to(rows[-1][0], RIGHT, 0.3)
        rows[-1][2].move_to(rows[-1][1])
        rows[-1][3].next_to(rows[-1][1], RIGHT, 0.35)
    rows.arrange(DOWN, buff=0.75, aligned_edge=LEFT)
    if rows.width > 12.4:
        rows.scale_to_fit_width(12.4)
    rows.next_to(head, DOWN, 0.9)
    return head, rows


class RecapScene(VideoScene):
    """The recap: point 1 shows all three and ticks the first; 2 and 3 tick the next."""

    point = None

    def construct(self):
        index = self.point - 1
        head, rows = recap_rows(video_constant(self, "RECAP"), self.lift)
        if index == 0:
            self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
            self.play(*[FadeIn(VGroup(r[0], r[1], r[3])) for r in rows], run_time=self.share(0.12))
        else:
            self.add(head, *[VGroup(r[0], r[1], r[3]) for r in rows], *[r[2] for r in rows[:index]])
        row = rows[index]
        self.play(Indicate(row[3], color=INK, scale_factor=1.06), run_time=self.share(0.3))
        self.play(Create(row[2]), run_time=self.share(0.12))
        self.finish()
        self.celebrate()


class QuizScene(VideoScene):
    """The question, then a bar that empties through the pause, so viewers know to think.

    `question` is its lines; the last is set in bold.
    """

    question = ()

    def construct(self):
        head = label("Quick quiz", 40, BLUE, weight=BOLD).to_edge(UP, buff=1.0)
        lines = [label(t, 48) for t in self.question[:-1]]
        lines.append(label(self.question[-1], 48, weight=BOLD))
        question = VGroup(*lines).arrange(DOWN, buff=0.3).next_to(head, DOWN, 0.8)
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=self.share(0.1))
        self.play(LaggedStart(*[FadeIn(q) for q in question], lag_ratio=0.8), run_time=self.share(0.55))
        self.finish()
        track = Rectangle(width=8, height=0.3, stroke_color=GRID, stroke_width=2).to_edge(DOWN, buff=1.2)
        left = ValueTracker(1.0)
        bar = always_redraw(lambda: Rectangle(width=max(8 * left.get_value(), 0.001), height=0.3,
                                              stroke_width=0, fill_color=BLUE, fill_opacity=1
                                              ).align_to(track, LEFT).align_to(track, DOWN))
        think = label("think about it", 28, SUBDUED).next_to(track, UP, 0.2)
        self.play(FadeIn(track), FadeIn(bar), FadeIn(think), run_time=0.3)
        self.play(left.animate.set_value(0), run_time=max(self.pause - 0.6, 0.5), rate_func=linear)


class EndCardScene(VideoScene):
    """The last scene: the site's address (never a page path, see SITE) and thanks."""

    def construct(self):
        pages = label("Pages and code", 36, SUBDUED, weight=BOLD)
        address = label(SITE, 44, BLUE)
        thanks = title("Thanks for watching", 64)
        series = label(SERIES, 28, SUBDUED)
        VGroup(pages, address, thanks, series).arrange(DOWN, buff=0.5)
        thanks.shift(0.5 * DOWN)
        series.shift(0.5 * DOWN)
        self.play(FadeIn(pages), FadeIn(address, shift=0.2 * UP), run_time=self.share(0.2))
        self.wait(self.share(0.35))
        self.play(FadeIn(thanks, scale=0.9), FadeIn(series), run_time=self.share(0.2))
        self.finish()
