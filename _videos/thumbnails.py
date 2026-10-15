"""YouTube thumbnails, one per video, in the series style.

    cd _videos
    manim -s -r 1280,720 --disable_caching -a thumbnails.py   # into _videos/media/
    python thumbnails.py                                      # copy them out

renders a 1280 x 720 still for every video and copies it to
`_videos/NN-slug/thumbnail.png`, ready to upload (both are git-ignored outputs).
Each shows the section number (YouTube only: the videos themselves carry none), the
title from the script's front matter, and one of the animals that cheer in that video.
"""

import shutil
import sys
from pathlib import Path

from manim import (BOLD, DOWN, LEFT, ORIGIN, RIGHT, UP, Circle, Line, RoundedRectangle,
                   Scene, VGroup, config)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mlbasic_video import (BLUE, INK, SERIES, SUBDUED, label, sprite)  # noqa: E402
from video_script import cheer_cast, read_script  # noqa: E402

HERE = Path(__file__).resolve().parent
FOLDERS = sorted(p for p in HERE.iterdir() if p.is_dir() and p.name[:2].isdigit())
PALE = "#E8F1F8"   # a pale tint of the series blue, behind the animal


def fit(mob, width):
    """Shrink `mob` to `width` if it is wider; never enlarge it."""
    return mob.scale_to_fit_width(width) if mob.width > width else mob


def wrap(text, limit):
    """`text` on one line if it fits in `limit` characters, otherwise on two lines
    split at the space that makes them most nearly equal."""
    if len(text) <= limit:
        return [text]
    words = text.split()
    splits = [(" ".join(words[:i]), " ".join(words[i:])) for i in range(1, len(words))]
    return list(min(splits, key=lambda pair: max(len(pair[0]), len(pair[1]))))


TEXT_WIDTH = 7.7   # the text column, clear of the animal's disc


def parts(folder):
    meta = read_script(folder / "script.md").meta
    main, _, sub = meta["title"].partition(": ")
    head = VGroup(*[label(line, 120, INK, weight=BOLD) for line in wrap(main, 14)])
    head.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    sub = sub[0].upper() + sub[1:]
    tagline = VGroup(*[label(line, 60, SUBDUED) for line in wrap(sub, 26)])
    tagline.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    return head, tagline


def animals():
    """Each video's animal: of the three that cheer in it, the one the earlier
    thumbnails have used least, so the eight animals spread over the ten videos."""
    used, chosen = [], {}
    for folder in FOLDERS:
        cast = [a for a, _, _ in cheer_cast(folder)]
        chosen[folder] = min(cast, key=used.count)
        used.append(chosen[folder])
    return chosen


ANIMAL = animals()


def widest(groups):
    return max(line.width for group in groups for line in group)


# One size for every title and one for every subtitle, set by the widest line in the
# series, so the ten thumbnails match.
_ALL = [parts(f) for f in FOLDERS]
HEAD_SCALE = min(1.0, TEXT_WIDTH / widest(h for h, _ in _ALL))
SUB_SCALE = min(1.0, TEXT_WIDTH / widest(t for _, t in _ALL))


def thumbnail(folder):
    number = int(folder.name[:2])
    animal = ANIMAL[folder]

    # Right: the animal on a pale disc.
    disc = Circle(radius=2.45, stroke_width=0, fill_color=PALE, fill_opacity=1)
    friend = sprite(animal, 2.9)
    art = VGroup(disc, friend).move_to(4.45 * RIGHT + 0.3 * DOWN)

    # Top: the number and the series name.
    badge_disc = Circle(radius=0.55, stroke_width=0, fill_color=BLUE, fill_opacity=1)
    badge = VGroup(badge_disc, label(str(number), 60, "#FFFFFF", weight=BOLD).move_to(badge_disc))
    series = label(SERIES, 34, SUBDUED)
    top = VGroup(badge, series).arrange(RIGHT, buff=0.3)
    top.to_corner(UP + LEFT, buff=0.55).shift(0.15 * DOWN)

    # Below: the title, a rule and the subtitle, centred in the space that is left.
    head, tagline = parts(folder)
    head.scale(HEAD_SCALE)
    tagline.scale(SUB_SCALE)
    rule = Line(ORIGIN, 2.4 * RIGHT, color=BLUE, stroke_width=10)
    text = VGroup(head, rule, tagline).arrange(DOWN, aligned_edge=LEFT, buff=0.36)
    room_top, room_bottom = top.get_bottom()[1] - 0.3, -config.frame_height / 2 + 0.5
    if text.height > room_top - room_bottom:
        text.scale((room_top - room_bottom) / text.height)
    text.move_to([0, (room_top + room_bottom) / 2, 0]).align_to(top, LEFT)

    strip = RoundedRectangle(width=config.frame_width + 1, height=0.22, corner_radius=0,
                             stroke_width=0, fill_color=BLUE, fill_opacity=1).to_edge(UP, buff=0)
    return VGroup(art, top, text, strip)


def scene_for(folder):
    class Thumbnail(Scene):
        def construct(self):
            self.add(thumbnail(folder))

        def tear_down(self):
            super().tear_down()

    Thumbnail.__name__ = f"Thumbnail{folder.name[:2]}"
    return Thumbnail


for _folder in FOLDERS:
    globals()[f"Thumbnail{_folder.name[:2]}"] = scene_for(_folder)


def copy_out():
    """Copy each rendered still next to its video's script."""
    images = Path(config.media_dir) / "images" / "thumbnails"
    for folder in FOLDERS:
        found = sorted(images.glob(f"Thumbnail{folder.name[:2]}*.png"))
        if found:
            shutil.copy(found[-1], folder / "thumbnail.png")


if __name__ == "__main__":
    copy_out()
