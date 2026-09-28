#!/usr/bin/env python3
"""Put a video's narration and pictures together into a draft, with captions and chapters.

    python tools/rough-cut.py _videos/05-generalisation

Writes, into the video folder:

    rough-cut.mp4   1920x1080, 30 fps, H.264 and AAC: the draft to watch and to polish
                    in Kdenlive
    captions.srt    for YouTube, from the narration as written (never the respelled
                    text sent for speech)
    chapters.txt    timestamps for the YouTube description, one per "# " heading

Each scene lasts its narration, plus its pause-after, plus a short gap, rounded up
to whole frames. What is on screen comes from the scene's visual line:

    visual: manim SceneName ...        visuals/scenes/SceneNN.mp4, rendered by manim; the
                                        last frame is held to the end of the scene
    visual: figure page.qmd#label ...  visuals/figures/<page>/<label>-1.png, from
                                        tools/figures-for-video.R
    visual: card: [Heading |] text     a text card drawn here

The sound is built as one WAV and added once, so there are no seams between scenes.
Scene pictures are cached in visuals/segments/ and redrawn only when their source
or length changes.
"""

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import textwrap
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from video_script import caption_text, read_script  # noqa: E402

WIDTH, HEIGHT, FPS = 1920, 1080, 30
GAP = 0.5              # seconds of silence between scenes
RATE = 24000           # Gemini TTS: 24 kHz, mono, 16-bit
CAPTION_CHARS = 84     # at most two lines of 42 characters per caption
CARD_TEXT_WIDTH = 1500  # pixels

BACKGROUND, INK, SUBDUED = "#FFFFFF", "#1F2A33", "#55606A"
FONT = "Source Sans 3"   # as in _videos/mlbasic_video.py


def font_file(style):
    out = subprocess.run(["fc-match", "-f", "%{file}", f"{FONT}:{style}"],
                         capture_output=True, text=True, check=True).stdout
    return out


def draw_card(text, path):
    """A white card: optional small heading, then the text, centred and wrapped."""
    heading, _, body = text.rpartition(" | ") if " | " in text else ("", "", text)
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    size = 84 if len(body) < 60 else 68
    head_font = ImageFont.truetype(font_file("bold"), 52)
    words = body.split()
    # Shrink until the longest word (a web address, say) fits on one line.
    while True:
        body_font = ImageFont.truetype(font_file("regular"), size)
        if max(draw.textlength(w, font=body_font) for w in words) <= CARD_TEXT_WIDTH:
            break
        size -= 4
    lines = [words[0]]
    for word in words[1:]:   # wrap by measured width, never inside a word
        if draw.textlength(f"{lines[-1]} {word}", font=body_font) <= CARD_TEXT_WIDTH:
            lines[-1] += f" {word}"
        else:
            lines.append(word)
    spacing = int(size * 1.3)
    block = spacing * len(lines) + (100 if heading else 0)
    y = (HEIGHT - block) // 2
    if heading:
        draw.text((WIDTH // 2, y), heading, font=head_font, fill=SUBDUED, anchor="mt")
        y += 100
    for line in lines:
        draw.text((WIDTH // 2, y), line, font=body_font, fill=INK, anchor="mt")
        y += spacing
    image.save(path)


def source_for(scene, folder):
    """(kind, path) of what the scene shows; cards are drawn into visuals/cards/."""
    visual = scene.visual
    if m := re.match(r"manim (\w+)", visual):
        return "clip", folder / "visuals" / "scenes" / f"Scene{scene.number:02d}.mp4"
    if m := re.match(r"figure ([\w-]+)\.qmd#([\w-]+)", visual):
        return "still", folder / "visuals" / "figures" / m.group(1) / f"{m.group(2)}-1.png"
    if visual.startswith("card:"):
        path = folder / "visuals" / "cards" / f"{scene.stem}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        draw_card(visual[len("card:"):].strip(), path)
        return "still", path
    sys.exit(f"scene {scene.number}: cannot read its visual line: {visual!r}")


def wav_frames(path):
    with wave.open(str(path)) as w:
        if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (RATE, 1, 2):
            sys.exit(f"{path}: expected 24 kHz mono 16-bit, as Gemini TTS writes")
        return w.readframes(w.getnframes())


def render_segment(kind, source, frames, out):
    """The scene's pictures only, exactly `frames` long."""
    fit = (f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease:flags=lanczos,"
           f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=white,setsar=1")
    if kind == "clip":
        inputs = ["-i", str(source)]
        video = f"{fit},fps={FPS},tpad=stop_mode=clone:stop_duration=3600"
    else:
        inputs = ["-loop", "1", "-framerate", str(FPS), "-i", str(source)]
        video = fit
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-vf", f"{video},format=yuv420p",
                    "-frames:v", str(frames), "-r", str(FPS), "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(out)],
                   check=True)


def timestamp(seconds, srt=False):
    ms = round(seconds * 1000)
    h, rest = divmod(ms, 3_600_000)
    m, rest = divmod(rest, 60_000)
    s, ms = divmod(rest, 1000)
    if srt:
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def caption_cues(text, start, length):
    """Split a scene's narration into short cues, timed by their share of characters."""
    sentences = re.split(r"(?<=[.?!:])\s+", text)
    cues = []
    for sentence in sentences:
        cues += textwrap.wrap(sentence, CAPTION_CHARS) if len(sentence) > CAPTION_CHARS else [sentence]
    total = sum(len(c) for c in cues)
    t, out = start, []
    for cue in cues:
        d = length * len(cue) / total
        out.append((t, t + d, "\n".join(textwrap.wrap(cue, CAPTION_CHARS // 2 + 4))))
        t += d
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("video", type=Path, help="the video folder, e.g. _videos/05-generalisation")
    args = parser.parse_args()

    folder = args.video.resolve()
    script = read_script(folder / "script.md")
    segments = folder / "visuals" / "segments"
    segments.mkdir(parents=True, exist_ok=True)
    cache_file = segments / "cache.json"
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}

    missing = []
    for scene in script.scenes:
        if not (folder / "audio" / f"{scene.stem}.wav").exists():
            missing.append(f"audio/{scene.stem}.wav (tools/narrate.py)")
    plan = []
    for scene in script.scenes:
        kind, source = source_for(scene, folder)
        if not source.exists():
            missing.append(f"{source.relative_to(folder)}")
        plan.append((scene, kind, source))
    if missing:
        sys.exit("missing:\n  " + "\n  ".join(missing))

    audio, captions, chapters = bytearray(), [], []
    list_file = segments / "list.txt"
    entries = []
    t = 0.0
    for scene, kind, source in plan:
        speech = wav_frames(folder / "audio" / f"{scene.stem}.wav")
        spoken = len(speech) / 2 / RATE
        frames = math.ceil(round((spoken + scene.pause_after + GAP) * FPS, 6))
        length = frames / FPS

        audio += speech + b"\0\0" * (round(length * RATE) - len(speech) // 2)
        captions += caption_cues(caption_text(scene.narration), t, spoken)
        if not chapters or chapters[-1][1] != scene.chapter:
            chapters.append((t, scene.chapter))

        out = segments / f"{scene.stem}.mp4"
        stamp = [str(source), source.stat().st_mtime, frames]
        if cache.get(scene.stem) != stamp or not out.exists():
            print(f"  scene {scene.number:2d}: {kind} {source.name}, {length:.2f} s", flush=True)
            render_segment(kind, source, frames, out)
            cache[scene.stem] = stamp
        entries.append(f"file '{out.name}'")
        t += length

    cache_file.write_text(json.dumps(cache, indent=1))
    list_file.write_text("\n".join(entries) + "\n")

    sound = segments / "narration.wav"
    with wave.open(str(sound), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(audio))

    draft = folder / "rough-cut.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
                    "-i", str(sound), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", "-shortest", str(draft)], check=True)

    (folder / "captions.srt").write_text("".join(
        f"{i}\n{timestamp(a, True)} --> {timestamp(b, True)}\n{text}\n\n"
        for i, (a, b, text) in enumerate(captions, 1)), encoding="utf-8")
    (folder / "chapters.txt").write_text(
        "".join(f"{timestamp(a)} {name}\n" for a, name in chapters), encoding="utf-8")

    short = [name for (a, name), (b, _) in zip(chapters, chapters[1:] + [(t, "")]) if b - a < 10]
    print(f"\n{draft.relative_to(Path.cwd()) if draft.is_relative_to(Path.cwd()) else draft}: "
          f"{timestamp(t)} ({len(script.scenes)} scenes), with captions.srt and chapters.txt")
    if short:
        print(f"YouTube needs chapters of at least 10 s; too short: {', '.join(short)}")
    if shutil.which("mpv"):
        print(f"Watch: mpv {draft}")


if __name__ == "__main__":
    main()
