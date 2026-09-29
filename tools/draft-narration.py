#!/usr/bin/env python3
"""Narrate a video with a free offline voice, for drafts: no API key, no quota, no cost.

    python tools/draft-narration.py _videos/05-generalisation
    python tools/draft-narration.py _videos/05-generalisation --voice en_GB-northern_english_male-medium

Writes audio/draft/scene-NN.wav for every scene without a current Gemini take (one
whose text still matches the script), in the same format Gemini writes: 24 kHz, mono,
16-bit. The Manim scenes and tools/rough-cut.py use a current Gemini take when there
is one and the draft otherwise, so a whole video can be scripted, animated, timed and
watched before any speech is bought; tools/narrate.py then replaces the drafts scene
by scene. A draft is rewritten only when its text or voice changes.

The voice is Piper (https://github.com/OHF-Voice/piper1-gpl), run on this laptop. Its
voices are downloaded once into ~/.local/share/piper-voices/. The drafts are paced to
match Gemini's timing roughly, so the pictures need little retiming for the final voice.
"""

import argparse
import hashlib
import json
import re
import sys
import wave
from pathlib import Path

import numpy as np
from scipy.signal import resample_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from video_script import current_take, pronunciations, read_script, respell  # noqa: E402

VOICE = "en_GB-alan-medium"
VOICES = Path.home() / ".local" / "share" / "piper-voices"
RATE = 24000               # as Gemini TTS, so everything downstream is unchanged
LENGTH_SCALE = 1.0         # >1 is slower. With alan-medium the §5 drafts ran within
                           # 3% of the Gemini takes (297 s against 305 s, 2026-09-28)
SENTENCE_GAP = 0.35        # seconds of silence after each sentence
TAG_GAP = 0.5              # seconds for an inline tag such as <short pause>


def load_voice(name):
    from piper import PiperVoice
    from piper.download_voices import download_voice

    model = VOICES / f"{name}.onnx"
    if not model.exists():
        print(f"downloading the Piper voice {name} into {VOICES} …", flush=True)
        VOICES.mkdir(parents=True, exist_ok=True)
        download_voice(name, VOICES)
    return PiperVoice.load(str(model))


def speak(voice, text):
    """Text to 24 kHz floats. Inline tags such as <short pause> become silence."""
    from piper import SynthesisConfig

    config = SynthesisConfig(length_scale=LENGTH_SCALE)
    rate = voice.config.sample_rate
    pieces = []
    for i, part in enumerate(re.split(r"<[^>]+>", text)):
        if i:
            pieces.append(np.zeros(round(TAG_GAP * rate)))
        if not part.strip():
            continue
        for chunk in voice.synthesize(part.strip(), syn_config=config):
            pieces.append(chunk.audio_int16_array / 32768)
            pieces.append(np.zeros(round(SENTENCE_GAP * rate)))
    audio = np.concatenate(pieces[:-1] if len(pieces) > 1 else pieces)
    g = np.gcd(RATE, rate)
    return resample_poly(audio, RATE // g, rate // g)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("video", type=Path, help="the video folder, e.g. _videos/05-generalisation")
    parser.add_argument("--voice", default=VOICE, help=f"a Piper voice name (default {VOICE})")
    args = parser.parse_args()

    script = read_script(args.video / "script.md")
    table = pronunciations()
    drafts = args.video / "audio" / "draft"
    drafts.mkdir(parents=True, exist_ok=True)

    voice, written, current = None, 0, []
    for scene in script.scenes:
        wav, sidecar = drafts / f"{scene.stem}.wav", drafts / f"{scene.stem}.json"
        if current_take(args.video, script, scene, table):
            current.append(scene.number)
            continue

        spoken = respell(scene.narration, table)
        key = hashlib.sha256(json.dumps([spoken, args.voice, LENGTH_SCALE]).encode()).hexdigest()
        if wav.exists() and sidecar.exists() and json.loads(sidecar.read_text())["key"] == key:
            continue

        voice = voice or load_voice(args.voice)
        audio = speak(voice, spoken)
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())
        sidecar.write_text(json.dumps({"key": key, "spoken": spoken, "voice": args.voice,
                                       "seconds": round(len(audio) / RATE, 2)}, indent=1) + "\n")
        written += 1
        print(f"  scene {scene.number:2d}  {len(audio) / RATE:5.1f} s", flush=True)

    drafted = len(script.scenes) - len(current)
    print(f"{script.path}: {written} draft(s) written; {drafted} scene(s) on the draft voice, "
          f"{len(current)} with a current Gemini take")


if __name__ == "__main__":
    main()
