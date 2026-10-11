#!/usr/bin/env python3
"""Put a video's narration and pictures together into a draft, with captions and chapters.

    python tools/rough-cut.py _videos/05-generalisation

Writes, into the video folder:

    rough-cut.mp4   1920x1080, 30 fps, H.264 and AAC: the draft to watch and to polish
                    in Kdenlive
    captions.srt    for YouTube, from the narration as written (never the respelled
                    text sent for speech)
    chapters.txt    timestamps for the YouTube description, one per "# " heading

Every video opens with the series title (visuals/scenes/Title.mp4, from the Title
scene) over the jingle in _videos/intro-music.wav. Then each scene lasts its
narration, plus its pause-after, plus the gap between scenes (`gap:` in the script's
front matter, 1 s by default), rounded up to whole frames. What is on screen comes
from the scene's visual line:

    visual: manim SceneName ...        visuals/scenes/SceneNN.mp4, rendered by manim; the
                                        last frame is held to the end of the scene
    visual: figure page.qmd#label ...  visuals/figures/<page>/<label>-1.png, from
                                        tools/figures-for-video.R
    visual: card: [Heading |] text     a text card drawn here

A scene with a cheer line (cheer: 1, 2, 3 or all) has its animals' sounds
(_videos/cheer-*.wav, from tools/make-cheers.py) mixed in as the narration ends, at
the moments the Manim scene shows the animals, both read from cheer_plan.

Each scene's voice is its Gemini take (audio/scene-NN.wav) when the take's text is
current, and otherwise the offline draft voice (audio/draft/, tools/draft-narration.py),
so a video can be cut before any speech is bought. The summary says how many scenes
are still on the draft voice.

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

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
from scipy.signal import resample_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from video_script import (caption_text, cheer_plan, narration_audio,  # noqa: E402
                          pronunciations, read_script)

WIDTH, HEIGHT, FPS = 1920, 1080, 30
GAP = 1.0              # seconds between scenes, unless the script's front matter sets gap
RATE = 24000           # Gemini TTS: 24 kHz, mono, 16-bit
MIX_RATE = 48000       # the soundtrack: 48 kHz stereo, so the jingle keeps its top end
MUSIC = Path(__file__).resolve().parent.parent / "_videos" / "intro-music.wav"
CHEERS = MUSIC.parent    # cheer-clap.wav, cheer-hooray.wav, cheer-fireworks.wav
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


def speech_samples(path):
    """A narration WAV as 48 kHz stereo floats."""
    with wave.open(str(path)) as w:
        if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (RATE, 1, 2):
            sys.exit(f"{path}: expected 24 kHz mono 16-bit, as Gemini TTS and "
                     f"tools/draft-narration.py write")
        mono = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768
    mono = resample_poly(mono, MIX_RATE // RATE, 1)
    return np.stack([mono, mono], axis=1)


def music_samples(path=MUSIC):
    rate, music = wavfile.read(path)
    if rate != MIX_RATE:
        sys.exit(f"{path}: expected {MIX_RATE} Hz")
    music = music / 32768 if music.dtype == np.int16 else music.astype(float)
    return music if music.ndim == 2 else np.stack([music, music], axis=1)


def padded(samples, length):
    """Samples followed by silence, exactly `length` seconds in all."""
    out = np.zeros((round(length * MIX_RATE), 2))
    out[: min(len(samples), len(out))] = samples[: len(out)]
    return out


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

    gap = float(script.meta.get("gap", GAP))
    title = folder / "visuals" / "scenes" / "Title.mp4"
    missing = [] if title.exists() else ["visuals/scenes/Title.mp4 (manim ... scenes.py Title)"]
    table = pronunciations()
    plan, drafted = [], []
    for scene in script.scenes:
        wav, is_draft = narration_audio(folder, script, scene, table)
        if wav is None:
            missing.append(f"audio/{scene.stem}.wav (tools/draft-narration.py or tools/narrate.py)")
        if is_draft:
            drafted.append(scene.number)
        kind, source = source_for(scene, folder)
        if not source.exists():
            missing.append(f"{source.relative_to(folder)}")
        plan.append((scene, wav, kind, source))
    if missing:
        sys.exit("missing:\n  " + "\n  ".join(missing))

    captions, chapters, entries, sound = [], [], [], []
    list_file = segments / "list.txt"

    def add_segment(name, kind, source, frames):
        out = segments / f"{name}.mp4"
        stamp = [str(source), source.stat().st_mtime, frames]
        if cache.get(name) != stamp or not out.exists():
            print(f"  {name}: {kind} {source.name}, {frames / FPS:.2f} s", flush=True)
            render_segment(kind, source, frames, out)
            cache[name] = stamp
        entries.append(f"file '{out.name}'")

    # The series opening: the title over the jingle, then a beat of silence.
    music = music_samples()
    frames = math.ceil(round((len(music) / MIX_RATE + gap) * FPS, 6))
    add_segment("title", "clip", title, frames)
    sound.append(padded(music, frames / FPS))
    t = frames / FPS

    for scene, wav, kind, source in plan:
        speech = speech_samples(wav)
        spoken = len(speech) / MIX_RATE
        frames = math.ceil(round((spoken + scene.pause_after + gap) * FPS, 6))
        length = frames / FPS

        track = padded(speech, length)
        for animal, name, start in cheer_plan(folder, scene):
            cheer = music_samples(CHEERS / f"cheer-{name}.wav")
            at = round((spoken + start) * MIX_RATE)
            if at + len(cheer) > len(track):
                sys.exit(f"scene {scene.number}: the {name} cheer runs past the scene's end; "
                         f"lengthen its pause-after")
            track[at:at + len(cheer)] += cheer
        sound.append(track)
        captions += caption_cues(caption_text(scene.narration), t, spoken)
        if not chapters or chapters[-1][1] != scene.chapter:
            # YouTube wants the first chapter at 0:00, so it takes in the title.
            chapters.append((t if chapters else 0.0, scene.chapter))
        add_segment(scene.stem, kind, source, frames)
        t += length

    cache_file.write_text(json.dumps(cache, indent=1))
    list_file.write_text("\n".join(entries) + "\n")

    soundtrack = segments / "soundtrack.wav"
    mix = np.clip(np.concatenate(sound), -1, 1)
    wavfile.write(soundtrack, MIX_RATE, (mix * 32767).astype(np.int16))

    draft = folder / "rough-cut.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
                    "-i", str(soundtrack), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", str(draft)], check=True)

    (folder / "captions.srt").write_text("".join(
        f"{i}\n{timestamp(a, True)} --> {timestamp(b, True)}\n{text}\n\n"
        for i, (a, b, text) in enumerate(captions, 1)), encoding="utf-8")
    (folder / "chapters.txt").write_text(
        "".join(f"{timestamp(a)} {name}\n" for a, name in chapters), encoding="utf-8")

    short = [name for (a, name), (b, _) in zip(chapters, chapters[1:] + [(t, "")]) if b - a < 10]
    print(f"\n{draft.relative_to(Path.cwd()) if draft.is_relative_to(Path.cwd()) else draft}: "
          f"{timestamp(t)} ({len(script.scenes)} scenes), with captions.srt and chapters.txt")
    if drafted:
        print(f"Draft voice in {len(drafted)} of {len(script.scenes)} scenes: "
              f"{', '.join(map(str, drafted))}")
    if short:
        print(f"YouTube needs chapters of at least 10 s; too short: {', '.join(short)}")
    if shutil.which("mpv"):
        print(f"Watch: mpv {draft}")


if __name__ == "__main__":
    main()
