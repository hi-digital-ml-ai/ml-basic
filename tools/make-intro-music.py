#!/usr/bin/env python3
"""Synthesise the series jingle: _videos/intro-music.wav, about three seconds.

    python tools/make-intro-music.py

Made from sine tones here, so there is no licence to track. To use a recorded track
instead (for example a CC0 one), save it as _videos/intro-music.wav, 48 kHz; any
length works, but keep it short: tools/rough-cut.py shows the title for as long as
the music lasts.
"""

from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve

RATE = 48000
LENGTH = 3.2
OUT = Path(__file__).resolve().parent.parent / "_videos" / "intro-music.wav"


def hz(note):
    """MIDI note number to frequency."""
    return 440.0 * 2 ** ((note - 69) / 12)


def bell(freq, start, decay=0.7, level=1.0):
    """A soft mallet tone: a few partials, a 6 ms attack, an exponential decay."""
    t = np.arange(int((LENGTH - start) * RATE)) / RATE
    tone = sum(a * np.sin(2 * np.pi * freq * k * t)
               for k, a in [(1, 1.0), (2, 0.28), (3, 0.08), (4.2, 0.04)])
    envelope = np.minimum(t / 0.006, 1) * np.exp(-t / decay)
    out = np.zeros(int(LENGTH * RATE))
    out[int(start * RATE):] = level * tone * envelope
    return out


def pad(freqs, start, level=0.35):
    """A warm chord that swells in and fades out, slightly detuned for width."""
    t = np.arange(int((LENGTH - start) * RATE)) / RATE
    left, right = np.zeros_like(t), np.zeros_like(t)
    for f in freqs:
        left += np.sin(2 * np.pi * f * 0.998 * t)
        right += np.sin(2 * np.pi * f * 1.002 * t)
    envelope = np.minimum(t / 0.35, 1) * np.clip((LENGTH - start - t) / 1.6, 0, 1)
    out = np.zeros((int(LENGTH * RATE), 2))
    out[int(start * RATE):, 0] = level * left * envelope / len(freqs)
    out[int(start * RATE):, 1] = level * right * envelope / len(freqs)
    return out


def pluck(freq, start, decay=0.12, level=1.0):
    """A short plucked bass note: a bright attack that dies away quickly."""
    return bell(freq, start, decay=decay, level=level)


def shaker(start, level=0.08):
    """A soft tick of filtered noise, for a light off-beat lift."""
    rng = np.random.default_rng(int(start * 1000))
    t = np.arange(int(0.06 * RATE)) / RATE
    tick = np.diff(rng.normal(0, 1, t.size + 1)) * np.exp(-t / 0.012)
    out = np.zeros(int(LENGTH * RATE))
    out[int(start * RATE):int(start * RATE) + t.size] = level * tick
    return out


def main():
    # G major, bouncy: a skipping run up to a bright final chord with a high sparkle.
    # (note, start, decay, level); short notes skip, the last ones ring.
    tune = [(67, 0.00, 0.25, 0.7), (71, 0.12, 0.25, 0.7), (74, 0.24, 0.25, 0.75),
            (79, 0.42, 0.25, 0.8), (78, 0.54, 0.25, 0.7), (79, 0.66, 0.25, 0.75),
            (83, 0.84, 0.9, 0.85), (86, 0.84, 0.9, 0.6), (91, 1.02, 0.7, 0.35)]
    melody = sum(bell(hz(n), s, decay=d, level=v) for n, s, d, v in tune)
    bass = sum(pluck(hz(n), s, level=0.9) for n, s in [(43, 0.00), (50, 0.24), (43, 0.42), (50, 0.66), (43, 0.84)])
    ticks = sum(shaker(s) for s in (0.12, 0.30, 0.54, 0.72))
    music = pad([hz(n) for n in (55, 62, 67, 71, 74)], 0.84, level=0.3)
    music[:, 0] += melody * 0.9 + bass * 0.5 + ticks * 0.6     # mallet a little left of centre
    music[:, 1] += melody * 0.75 + bass * 0.5 + ticks * 0.9

    # A short, gentle room: decaying noise as the impulse response.
    rng = np.random.default_rng(5)
    t = np.arange(int(1.1 * RATE)) / RATE
    room = rng.normal(0, 1, (t.size, 2)) * np.exp(-t / 0.28)[:, None]
    wet = np.stack([fftconvolve(music[:, c], room[:, c])[: music.shape[0]] for c in (0, 1)], 1)
    music = music + 0.18 * wet / np.abs(wet).max() * np.abs(music).max()

    fade = np.clip((LENGTH - np.arange(music.shape[0]) / RATE) / 0.4, 0, 1)
    music *= fade[:, None]
    music *= 10 ** (-4 / 20) / np.abs(music).max()     # peak at -4 dBFS
    wavfile.write(OUT, RATE, (music * 32767).astype(np.int16))
    print(f"{OUT}: {LENGTH} s, {RATE} Hz stereo")


if __name__ == "__main__":
    main()
