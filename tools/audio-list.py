#!/usr/bin/env python3
"""List every scene's narration audio and how it was made, to plan the Gemini TTS runs.

    python tools/audio-list.py                              # every video in _videos/
    python tools/audio-list.py _videos/05-generalisation    # one video

For each video, writes audio/audio-list.csv (one row per scene) and prints a summary.
A scene's audio is one of:

    gemini        a Gemini take of the scene's current text: nothing to do
    reuse         no take under this number, but a take of the same request exists
                  under another (the scene moved); tools/narrate.py copies it, no request
    draft         the offline draft voice (tools/draft-narration.py): needs a request
    gemini-stale  a Gemini take of text that has since changed, and no draft: needs a
                  request
    none          no audio at all: needs a request (or a draft first)

The "request" column is what tools/narrate.py would send, so the summary is the
number of requests a run would use against the paid tier's 100 a day. The cost is an
estimate: seconds of audio (the draft's length when there is no take) at the audio
token rate the §5 takes used.
"""

import argparse
import csv
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from video_script import current_take, pronunciations, read_script, scene_key  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DAILY_REQUESTS = 100           # paid tier, gemini-3.8-flash-tts (see .claude/videos.md)
PRICE = 9.0                    # US dollars per million audio output tokens, 2026
TOKENS_PER_SECOND = 32         # §5 takes: 273 tokens for 8.52 s, and so on


def seconds(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def audio_list(folder, table):
    script = read_script(folder / "script.md")
    audio = folder / "audio"
    takes = {}                 # request key -> scene number of a take on disk
    for sidecar in audio.glob("scene-*.json"):
        if sidecar.with_suffix(".wav").exists():
            takes.setdefault(json.loads(sidecar.read_text())["key"], sidecar.stem)

    rows = []
    for scene in script.scenes:
        take = audio / f"{scene.stem}.wav"
        draft = audio / "draft" / f"{scene.stem}.wav"
        key = scene_key(script, scene, table)
        if current_take(folder, script, scene, table):
            source, path = "gemini", take
        elif key in takes:
            source, path = "reuse", audio / f"{takes[key]}.wav"
        elif draft.exists():
            source, path = "draft", draft
        elif take.exists():
            source, path = "gemini-stale", take
        else:
            source, path = "none", None
        rows.append({
            "scene": scene.number,
            "chapter": scene.chapter,
            "source": source,
            "request": "no" if source in ("gemini", "reuse") else "yes",
            "file": path.relative_to(folder).as_posix() if path else "",
            "seconds": round(seconds(path), 1) if path else "",
            "words": len(scene.narration.split()),
            "narration": scene.narration,
        })
    return script, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("videos", nargs="*", type=Path,
                        help="video folders (default: every _videos/*/ with a script.md)")
    args = parser.parse_args()
    folders = args.videos or sorted(p.parent for p in (ROOT / "_videos").glob("*/script.md"))
    table = pronunciations()

    total_requests = 0
    for folder in folders:
        folder = folder.resolve()
        script, rows = audio_list(folder, table)
        out = folder / "audio" / "audio-list.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

        counts = {}
        for row in rows:
            counts[row["source"]] = counts.get(row["source"], 0) + 1
        needed = [r for r in rows if r["request"] == "yes"]
        # Without any audio, guess the length from the words, at the §5 pace.
        est = sum(r["seconds"] if r["seconds"] != "" else r["words"] / 2.7 for r in needed)
        total_requests += len(needed)

        print(f"\n{folder.name}: {len(rows)} scenes  "
              + "  ".join(f"{k} {v}" for k, v in sorted(counts.items())))
        print(f"  {'scene':>5}  {'source':<12} {'secs':>5}  narration")
        for r in rows:
            if r["request"] == "yes":
                text = r["narration"] if len(r["narration"]) <= 70 else r["narration"][:67] + "…"
                print(f"  {r['scene']:>5}  {r['source']:<12} {r['seconds']:>5}  {text}")
        if needed:
            print(f"  → {len(needed)} request(s), about {est:.0f} s of speech, "
                  f"about ${est * TOKENS_PER_SECOND * PRICE / 1e6:.2f}")
            print(f"    scenes to narrate: {','.join(str(r['scene']) for r in needed)}")
        else:
            print("  → nothing to narrate")
        print(f"  list: {out.relative_to(Path.cwd()) if out.is_relative_to(Path.cwd()) else out}")

    if len(folders) > 1:
        print(f"\nAll videos: {total_requests} request(s); the paid tier allows "
              f"{DAILY_REQUESTS} a day, retakes included.")


if __name__ == "__main__":
    main()
