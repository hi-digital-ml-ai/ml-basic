"""Read a video script (_videos/NN-slug/script.md) into chapters and scenes.

Shared by tools/narrate.py and tools/rough-cut.py, so both read the script the same
way. The format is described in the comment at the top of each script.md and in
.claude/videos.md.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DIRECTIVE = re.compile(r"^(visual|pause-after):\s*(.*)$")


@dataclass
class Scene:
    number: int
    chapter: str
    narration: str
    visual: str = ""
    pause_after: float = 0.0
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


def caption_text(narration):
    """The narration as it should appear in captions: inline speech tags removed."""
    return " ".join(re.sub(r"<[^>]+>", "", narration).split())
