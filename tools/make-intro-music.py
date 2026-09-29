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


def main():
    # G major: a rising arpeggio G4 B4 D5 G5, then the chord held underneath.
    arpeggio = [(67, 0.00), (71, 0.16), (74, 0.32), (79, 0.48)]
    melody = sum(bell(hz(n), s, level=0.9 if n == 79 else 0.7) for n, s in arpeggio)
    music = pad([hz(n) for n in (55, 62, 67, 71)], 0.45)
    music[:, 0] += melody * 0.9     # mallet a little left of centre
    music[:, 1] += melody * 0.75

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
