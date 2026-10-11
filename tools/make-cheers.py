#!/usr/bin/env python3
"""Make the three cheers that greet each key point: _videos/cheer-*.wav, 48 kHz stereo.

    python tools/make-cheers.py

    cheer-clap.wav       applause: a dozen pairs of hands, swelling then dying away
    cheer-hooray.wav     a small crowd shouting "Hooray!"
    cheer-fireworks.wav  a rocket's whistle, its bang, and the crackle after

The clapping and the fireworks are synthesised from noise here, and the crowd is the
offline Piper voice (as tools/draft-narration.py) at several pitches, so there is no
licence to track. To use recorded sounds instead (CC0, say), save them under the same
names, 48 kHz. tools/video_script.py pairs each sound with an animal per video, and
tools/rough-cut.py plays it as the animal appears.
"""

import importlib.util
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

RATE = 48000
OUT = Path(__file__).resolve().parent.parent / "_videos"
LEVEL = 0.1    # RMS of the loud part, as the jingle; the narration sits near 0.13
PEAK = 0.8
rng = np.random.default_rng(2026)


def band(x, low, high, order=2):
    return sosfilt(butter(order, [low, high], "bandpass", fs=RATE, output="sos"), x)


def room(stereo, length=0.35, wet=0.18):
    """A little reverberation, so the sounds sit in a space rather than in a box."""
    t = np.arange(int(length * RATE)) / RATE
    out = np.empty_like(stereo)
    for ch in range(2):
        tail = rng.standard_normal(len(t)) * np.exp(-t / (length / 5))
        tail /= np.sqrt(np.sum(tail ** 2))
        out[:, ch] = stereo[:, ch] + wet * fftconvolve(stereo[:, ch], tail)[: len(stereo)]
    return out


def place(out, mono, start, pan):
    """Add a mono sound into the stereo buffer at `start` seconds, panned -1 to 1."""
    i = int(start * RATE)
    n = min(len(mono), len(out) - i)
    if n <= 0:
        return
    out[i:i + n, 0] += mono[:n] * np.sqrt((1 - pan) / 2)
    out[i:i + n, 1] += mono[:n] * np.sqrt((1 + pan) / 2)


def finish(stereo, fade=0.3):
    stereo = room(stereo)
    n = int(fade * RATE)
    stereo[-n:] *= np.linspace(1, 0, n)[:, None]
    loud = stereo[: len(stereo) // 2]
    stereo = stereo * LEVEL / np.sqrt(np.mean(loud ** 2))
    return stereo * min(1, PEAK / np.abs(stereo).max())


def clap():
    length, hands = 2.4, 12
    out = np.zeros((int(length * RATE), 2))
    for _ in range(hands):
        centre = rng.uniform(900, 2200)            # each pair of hands has its own pitch
        rate = rng.uniform(4.2, 6.0)               # claps a second
        pan = rng.uniform(-0.8, 0.8)
        t = rng.uniform(0, 0.25)
        stop = rng.uniform(1.4, 2.0)
        while t < stop:
            n = int(0.06 * RATE)
            burst = band(rng.standard_normal(n), centre * 0.6, centre * 1.8)
            burst *= np.exp(-np.arange(n) / RATE / rng.uniform(0.008, 0.018))
            swell = min(t / 0.25, 1) * min((stop - t) / 0.6 + 0.3, 1)
            place(out, burst * swell * rng.uniform(0.6, 1.0), t, pan)
            t += (1 / rate) * rng.uniform(0.85, 1.15)
    return finish(out)


def fireworks():
    length = 2.8
    out = np.zeros((int(length * RATE), 2))
    # The rocket: a rising whistle that drifts left to right.
    rise = 0.7
    t = np.arange(int(rise * RATE)) / RATE
    freq = 900 + 1500 * (t / rise) ** 1.5 + 25 * np.sin(2 * np.pi * 9 * t)
    whistle = np.sin(2 * np.pi * np.cumsum(freq) / RATE) * (0.15 + 0.85 * t / rise) * 0.35
    whistle += band(rng.standard_normal(len(t)), 2000, 6000) * 0.05
    for i, pan in enumerate(np.linspace(-0.5, 0.2, 8)):
        piece = np.array_split(whistle, 8)[i]
        place(out, piece, i * rise / 8, pan)
    # The bang: a deep thump under a burst of noise.
    n = int(0.9 * RATE)
    tb = np.arange(n) / RATE
    thump = np.sin(2 * np.pi * (70 - 30 * tb) * tb) * np.exp(-tb / 0.18)
    burst = band(rng.standard_normal(n), 60, 1500) * np.exp(-tb / 0.25)
    place(out, 1.6 * (thump + burst), rise + 0.05, 0.2)
    # The crackle: sparks scattering, fewer as they fade.
    t = rise + 0.2
    while t < length - 0.2:
        m = int(rng.uniform(0.002, 0.006) * RATE)
        spark = band(rng.standard_normal(m), 2500, 9000) * np.hanning(m)
        fade = np.exp(-(t - rise) / 0.9)
        place(out, spark * rng.uniform(0.6, 1.4) * fade, t, rng.uniform(-0.9, 0.9))
        t += rng.exponential(0.012 + 0.03 * (1 - fade))
    return finish(out)


def hooray():
    spec = importlib.util.spec_from_file_location(
        "draft_narration", Path(__file__).with_name("draft-narration.py"))
    draft = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(draft)
    from piper import SynthesisConfig

    length = 2.2
    out = np.zeros((int(length * RATE), 2))
    voices = [draft.load_voice(n) for n in ("en_GB-alan-medium",
                                            "en_GB-northern_english_male-medium")]
    # Each shout at its own pitch: a resample raises the pitch and quickens the word,
    # so the higher voices sound like a younger crowd.
    for i, step in enumerate([0.95, 1.0, 1.12, 1.25, 1.4, 1.55, 1.7]):
        voice = voices[i % 2]
        config = SynthesisConfig(length_scale=1.15, noise_scale=0.9, noise_w_scale=1.0)
        audio = np.concatenate([c.audio_int16_array / 32768
                                for c in voice.synthesize("Hooray!", syn_config=config)])
        rate = voice.config.sample_rate
        up, down = 100, round(100 * step)
        shout = resample_poly(resample_poly(audio, RATE // np.gcd(RATE, rate), rate // np.gcd(RATE, rate)),
                              up, down)
        place(out, shout * rng.uniform(0.7, 1.0), rng.uniform(0.0, 0.15), rng.uniform(-0.8, 0.8))
    return finish(out, fade=0.5)


def main():
    for name, make in [("clap", clap), ("fireworks", fireworks), ("hooray", hooray)]:
        sound = np.clip(make(), -1, 1)
        path = OUT / f"cheer-{name}.wav"
        wavfile.write(path, RATE, (sound * 32767).astype(np.int16))
        print(f"{path.relative_to(OUT.parent)}: {len(sound) / RATE:.1f} s, "
              f"peak {np.abs(sound).max():.2f}")


if __name__ == "__main__":
    main()
