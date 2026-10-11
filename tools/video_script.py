"""Read a video script (_videos/NN-slug/script.md) into chapters and scenes.

Shared by tools/narrate.py, tools/draft-narration.py, tools/rough-cut.py and the Manim
scenes, so all of them read the script, and find each scene's narration, the same
way. The format is described in the comment at the top of each script.md and in
.claude/videos.md.
"""

import hashlib
import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

MODEL = "gemini-3.8-flash-tts"
LANGUAGE = "en-GB"
PRONUNCIATION = Path(__file__).resolve().parent.parent / "_videos" / "pronunciation.yml"

DIRECTIVE = re.compile(r"^(visual|pause-after|cheer):\s*(.*)$")

# The cheers: an animal pops up with a sound when each key point is made ("cheer: 1",
# "cheer: 2", "cheer: 3"), and all three together after the recap ("cheer: all"). The
# animals are drawn in _videos/sea_friends.py, the sounds made by tools/make-cheers.py.
ANIMALS = ["crab", "octopus", "clownfish", "turtle", "whale", "pufferfish", "jellyfish",
           "starfish"]
SOUNDS = ["clap", "hooray", "fireworks"]
CHEER_STAGGER = 0.9    # seconds between the three cheers in "cheer: all"


@dataclass
class Scene:
    number: int
    chapter: str
    narration: str
    visual: str = ""
    pause_after: float = 0.0
    cheer: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def stem(self):
        return f"scene-{self.number:02d}"


@dataclass
class Script:
    path: Path
    meta: dict
    scenes: list


def read_script(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8")

    meta = {}
    if text.startswith("---\n"):
        _, front, text = text.split("---\n", 2)
        meta = yaml.safe_load(front) or {}

    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)

    scenes, chapter, current, lines = [], "", None, []

    def close():
        if current is None:
            return
        body = []
        for line in lines:
            m = DIRECTIVE.match(line) if not body else None
            if m:
                key, value = m.groups()
                if key == "visual":
                    current.visual = value.strip()
                elif key == "cheer":
                    current.cheer = value.strip()
                else:
                    current.pause_after = float(value)
            elif line.strip() or body:
                body.append(line.strip())
        current.narration = " ".join(" ".join(body).split())
        if not current.narration:
            raise ValueError(f"{path}: scene {current.number} has no narration")
        scenes.append(current)

    for line in text.splitlines():
        if line.startswith("# "):
            close()
            current, lines = None, []
            chapter = line[2:].strip()
        elif line.startswith("## "):
            close()
            m = re.fullmatch(r"## Scene (\d+)", line.strip())
            if not m:
                raise ValueError(f"{path}: expected '## Scene N', got {line!r}")
            current, lines = Scene(int(m.group(1)), chapter, ""), []
        elif current is not None:
            lines.append(line)
    close()

    numbers = [s.number for s in scenes]
    if numbers != list(range(1, len(scenes) + 1)):
        raise ValueError(f"{path}: scenes must be numbered 1, 2, 3 … in order, got {numbers}")

    return Script(path, meta, scenes)


def cheer_cast(folder):
    """The video's three (animal, sound) pairs, one per key point, in order.

    Drawn at random, but seeded by the folder's name, so every render and every rough
    cut of a video picks the same three.
    """
    pick = random.Random(Path(folder).resolve().name)
    return list(zip(pick.sample(ANIMALS, 3), pick.sample(SOUNDS, 3)))


def cheer_plan(folder, scene):
    """[(animal, sound, seconds after the narration ends)] for a scene's cheer line."""
    cast = cheer_cast(folder)
    if not scene.cheer:
        return []
    if scene.cheer == "all":
        return [(a, s, i * CHEER_STAGGER) for i, (a, s) in enumerate(cast)]
    if scene.cheer in ("1", "2", "3"):
        return [(*cast[int(scene.cheer) - 1], 0.0)]
    raise ValueError(f"scene {scene.number}: cheer must be 1, 2, 3 or all, not {scene.cheer!r}")


def caption_text(narration):
    """The narration as it should appear in captions: inline speech tags removed."""
    return " ".join(re.sub(r"<[^>]+>", "", narration).split())


def respell(text, table):
    for word in sorted(table, key=len, reverse=True):
        text = re.sub(rf"(?<!\w){re.escape(word)}(?!\w)", table[word], text)
    return text


def request_key(spoken, voice, style, language, model):
    blob = json.dumps([spoken, voice, style, language, model], ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def pronunciations():
    return yaml.safe_load(PRONUNCIATION.read_text(encoding="utf-8")) or {}


def scene_key(script, scene, table):
    """The key tools/narrate.py files a scene's take under: what it would send."""
    meta = script.meta
    return request_key(respell(scene.narration, table), meta.get("voice"),
                       meta.get("style", ""), meta.get("language", LANGUAGE),
                       meta.get("model", MODEL))


def current_take(folder, script, scene, table=None):
    """True when audio/scene-NN.wav is a Gemini take of the scene's text as it is now."""
    take = Path(folder) / "audio" / f"{scene.stem}.wav"
    sidecar = take.with_suffix(".json")
    if not (take.exists() and sidecar.exists()):
        return False
    key = scene_key(script, scene, pronunciations() if table is None else table)
    return json.loads(sidecar.read_text())["key"] == key


def narration_audio(folder, script, scene, table=None):
    """The WAV to use for a scene, and whether it is a draft.

    A Gemini take (audio/scene-NN.wav) whose text is current comes first. Otherwise
    the draft voice (audio/draft/scene-NN.wav, from tools/draft-narration.py), then
    an out-of-date take. None when the scene has no audio at all.
    """
    folder = Path(folder)
    take = folder / "audio" / f"{scene.stem}.wav"
    draft = folder / "audio" / "draft" / f"{scene.stem}.wav"
    if current_take(folder, script, scene, table):
        return take, False
    if draft.exists():
        return draft, True
    if take.exists():
        return take, False
    return None, False
