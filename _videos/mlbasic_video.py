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
from video_script import narration_audio, read_script  # noqa: E402

SERIES = "Machine Learning Basics for Marine Science"
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

    def share(self, fraction):
        """A run time as a fraction of this scene's narration."""
        return fraction * self.narration

    def finish(self):
        """Hold the last frame until the narration ends."""
        left = self.narration - self.time
        if left > 1 / config.frame_rate:
            self.wait(left)

    def data(self, name):
        """A CSV written by tools/figures-for-video.R, from the pages' own results."""
        path = self.folder / "visuals" / "data" / f"{name}.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"{path} is missing: run Rscript tools/figures-for-video.R {self.folder.name}")
        return pd.read_csv(path)


class TitleScene(Scene):
    """The opening every video shares: series name, section, title, over the jingle.

    Each scenes.py has `class Title(TitleScene): pass`; the text comes from the
    script's front matter and the length from _videos/intro-music.wav.
    """

    def construct(self):
        folder = Path(sys.modules[type(self).__module__].__file__).resolve().parent
        meta = read_script(folder / "script.md").meta
        with wave.open(str(MUSIC)) as w:
            length = w.getnframes() / w.getframerate()
        section = int(Path(meta["section"]).parent.name.split("-")[0])
        main, _, sub = meta["title"].partition(": ")

        rule = Line(3.2 * LEFT, 3.2 * RIGHT, color=BLUE, stroke_width=6)
        series = label(SERIES, 30, SUBDUED)
        number = label(f"Section {section}", 34, BLUE, weight=BOLD)
        head = title(main, 80)
        tagline = label(sub, 42, SUBDUED) if sub else VGroup()
        VGroup(series, number, head, rule, tagline).arrange(DOWN, buff=0.35)
        rule.shift(0.1 * DOWN)
        tagline.shift(0.15 * DOWN)

        # Timed to the jingle: the text arrives with the arpeggio, the rule with the chord.
        self.play(FadeIn(series, shift=0.2 * DOWN), FadeIn(number, shift=0.2 * DOWN),
                  run_time=0.4)
        self.play(FadeIn(head, shift=0.3 * UP), run_time=0.5)
        self.play(GrowFromCenter(rule), FadeIn(tagline), run_time=0.6)
        self.wait(max(length - self.time, 0.1))
