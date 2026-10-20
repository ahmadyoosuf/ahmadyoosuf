"""The score for 77 MINUTES: an original solo-piano bed written to picture (DECISIONS
D015), rendered on Salamander Grand Piano V3 samples by Alexander Holm (CC BY 3.0).

The music is silent through section 2 (D028). It enters with section 3 on a descending
A-F-D figure (the "writing" motif) in D minor. In section 4 the bars shorten and the left
hand moves from quavers to semiquavers. It breaks off unresolved on A7 at "There's an
old Tamil saying." and lets the gourd be drawn in silence. Section 5 resolves into slow
F-major chords ("So, slowly, I started cooking."). Section 6 turns the motif upside down
(F-A-C-F) and lands it on "They say it.". Section 7 thins out, holds a chord on the end
card, and gives the dedication the motif once more, slowly, down to D.
"""
import functools
import pathlib
import subprocess

import numpy as np
from scipy.signal import fftconvolve

SR = 48000
ROOT = pathlib.Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "assets" / "audio" / "samples" / "salamander"

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SAMPLED = {"A": 9, "C": 0, "D#": 3, "F#": 6}
LAYERS = (6, 8, 10)


def sample_notes():
    out = []
    for octave in range(0, 9):
        for name, pc in SAMPLED.items():
            midi = 12 * (octave + 1) + pc
            if 21 <= midi <= 108:
                out.append((midi, f"{name}{octave}"))
    return out


@functools.lru_cache(maxsize=None)
def load(layer, name):
    path = SAMPLES / f"v{layer}" / f"{name}v{layer}.mp3"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype="<f4").reshape(-1, 2).astype(np.float64)


def voice(midi, vel, dur, release=0.45):
    """One note: nearest sample, pitch-shifted by resampling, velocity layer and gain,
    held for `dur` then released."""
    layer = 6 if vel < 0.36 else 8 if vel < 0.58 else 10
    best = min(sample_notes(), key=lambda s: (abs(s[0] - midi), s[0] - midi))
    src_midi, name = best
    x = load(layer, name)
    ratio = 2 ** ((midi - src_midi) / 12)
    need = int((dur + release + 0.05) * SR)
    pos = np.arange(min(need, int((len(x) - 2) / ratio))) * ratio
    y = np.stack([np.interp(pos, np.arange(len(x)), x[:, c]) for c in (0, 1)], axis=1)
    hold = int(dur * SR)
    if len(y) > hold:
        rel = len(y) - hold
        y[hold:] *= np.exp(-np.arange(rel) / (release / 5 * SR))[:, None]
    # within-layer gain: +-4 dB across the layer's span
    lo = {6: 0.0, 8: 0.36, 10: 0.58}[layer]
    hi = {6: 0.36, 8: 0.58, 10: 1.0}[layer]
    g = 10 ** ((-4 + 8 * (vel - lo) / max(1e-6, hi - lo)) / 20)
    return y * g


def chord(t, notes, vel, dur, roll=0.0, out=None):
    for k, n in enumerate(notes):
        out.append((t + k * roll, n, vel * (0.92 if k else 1.0), dur - k * roll))


def score(anchors):
    """anchors: dict of absolute times (s). Returns list of (t, midi, vel, dur)."""
    ev = []
    T3, T4, TB = anchors["s3"], anchors["s4"], anchors["break"]
    T5, T6, TSAY, T7 = anchors["cook"], anchors["s6"], anchors["say"], anchors["s7"]
    TEND, TFATHER, END = anchors["end_card"], anchors["father"], anchors["end"]

    # ---------------- section 3: Alone (14 bars across the section) ----------------
    bar = (T4 - T3) / 14
    prog3 = [
        ([38, 45, 53], [(2, 69)]),
        ([34, 41, 50], [(0, 65), (2, 62)]),
        ([41, 48, 57], [(0, 72), (2, 69)]),
        ([36, 43, 52], [(0, 67), (2, 64)]),
        ([38, 45, 53], [(0, 65), (1.5, 69), (2, 74)]),
        ([34, 41, 50], [(0, 74), (2, 72)]),
        ([31, 38, 46], [(0, 70), (2, 74)]),
        ([33, 40, 49], [(0, 73), (2, 76)]),
        ([38, 45, 53], [(0, 77), (1, 76), (2, 74)]),
        ([34, 41, 50], [(0, 74), (2, 65)]),
        ([33, 41, 48], [(0, 69), (2, 72)]),
        ([36, 43, 52], [(0, 67), (1, 64), (2, 72)]),
        ([38, 45, 52], [(0, 69)]),
        ([33, 40, 50], [(0, 64), (2, 73)]),
    ]
    beat = bar / 4
    for k, (lh, rh) in enumerate(prog3):
        t = T3 + k * bar
        v = 0.30 + 0.02 * min(k, 6)
        if k == 0:
            chord(t, lh[:2], v, bar * 1.05, roll=0.0, out=ev)  # the first sound: an open fifth
            chord(t + 1.5 * beat, lh[2:], v, bar * 0.7, out=ev)
        else:
            chord(t, lh, v, bar * 1.04, roll=0.05, out=ev)
        for b, n in rh:
            ev.append((t + b * beat, n, 0.40 + 0.01 * min(k, 6), beat * 2.2))
        if k == 13:
            ev.append((t + 2 * beat, 49, v, beat * 2.1))  # sus4 resolves to the major third

    # ---------------- section 4: Well said (accelerando to the break) ----------------
    prog4 = [
        ("Dm", [38, 45, 50, 53, 57]), ("Bb", [34, 41, 46, 50, 53]), ("F", [41, 48, 53, 57, 60]),
        ("C", [36, 43, 48, 52, 55]), ("Dm", [38, 45, 50, 53, 57]), ("Bb", [34, 41, 46, 50, 53]),
        ("Gm", [31, 38, 43, 46, 50]), ("A", [33, 40, 45, 49, 52]), ("Dm", [38, 45, 50, 53, 57]),
        ("Bb", [34, 41, 46, 50, 53]), ("Gm", [31, 38, 43, 46, 50]), ("A7", [33, 40, 43, 49, 52]),
    ]
    raw = np.linspace(4.0, 2.7, len(prog4))
    lens = raw * (TB - T4) / raw.sum()
    melody4 = {0: [(0, 69), (1, 65), (2, 62)], 1: [(0, 65), (2, 70)], 2: [(0, 72), (1, 69)], 3: [(0, 67), (2, 64)],
               4: [(0, 69), (1, 65), (2, 62)], 5: [(0, 74), (2, 70)], 6: [(0, 70), (1, 74)], 7: [(0, 73), (2, 76)],
               8: [(0, 69), (0.5, 65), (1, 62)], 9: [(0, 74), (1, 70), (2, 74)], 10: [(0, 77), (1, 74), (2, 70)],
               11: [(0, 73), (1, 76), (2, 79), (3, 76)]}
    t = T4
    for k, ((name, nts), L) in enumerate(zip(prog4, lens)):
        sub = 8 if k < 8 else 16
        pattern = [nts[0], nts[1], nts[2], nts[3], nts[4], nts[3], nts[2], nts[1]]
        if sub == 16:
            pattern = pattern + [nts[2], nts[3], nts[4], nts[4] + 5, nts[4], nts[3], nts[2], nts[1]]
        step = L / sub
        v = 0.32 + 0.022 * k
        for i in range(sub):
            n = pattern[i % len(pattern)]
            last = (k == len(prog4) - 1)
            d = step * (1.6 if not last else 1.2)
            if t + i * step + d > TB:
                d = max(0.04, TB - (t + i * step))
            ev.append((t + i * step, n, v * (1.0 if i % 4 == 0 else 0.86), d))
        for b, n in melody4.get(k, []):
            st = t + b * L / 4
            d = min(L / 4 * 1.6, TB - st)
            ev.append((st, n, v + 0.08, max(0.05, d)))
        t += L

    # ---------------- section 5: Well done (half speed, warm, resolves) ----------------
    prog5 = [
        ([41, 48, 57, 65], [(0.5, 69)]),
        ([40, 45, 52, 60], [(0.5, 76), (2.5, 72)]),
        ([34, 41, 50, 58], [(0.5, 74), (2.5, 77)]),
        ([33, 41, 48, 57], [(0.5, 72)]),
        ([31, 38, 46, 53], [(0.5, 70), (2.5, 74)]),
        ([36, 43, 52, 60], [(0.5, 76), (2.5, 79)]),
        ([41, 48, 57, 65], [(0.5, 77)]),
    ]
    L5 = (T6 - T5) / len(prog5)
    for k, (lh, rh) in enumerate(prog5):
        t = T5 + k * L5
        chord(t, lh, 0.34, L5 * 1.08, roll=0.07, out=ev)
        for b, n in rh:
            ev.append((t + b * L5 / 4, n, 0.42, L5 * 0.75))

    # ---------------- section 6: Just say it (the motif rises and lands on "They say it.") ---------
    prog6 = [([41, 48, 57], [(0, 65), (2, 69)]), ([34, 41, 50], [(0, 70), (2, 72)]),
             ([38, 45, 53], [(0, 74), (2, 72)]), ([36, 43, 52], [(0, 76), (3, 72)])]
    L6 = (TSAY - T6) / len(prog6)
    for k, (lh, rh) in enumerate(prog6):
        t = T6 + k * L6
        chord(t, lh, 0.34 + 0.02 * k, L6 * 1.05, roll=0.05, out=ev)
        for b, n in rh:
            ev.append((t + b * L6 / 4, n, 0.44 + 0.02 * k, L6 / 2 * 1.1))
    # arrival
    chord(TSAY, [29, 41, 48, 57, 65], 0.46, (T7 - TSAY) + 4.0, roll=0.06, out=ev)
    ev.append((TSAY + 0.02, 77, 0.52, 5.5))
    ev.append((TSAY + 0.55, 81, 0.40, 5.0))

    # ---------------- section 7: The ask (thin, a held chord, the motif for his father) ---------
    t = T7 + 2.6
    seven = [([34, 41, 50], 74), ([33, 41, 48], 72), ([31, 38, 46], 70), ([36, 43, 52], 76), ([38, 45, 53], 69)]
    gap = (TEND - 1.2 - t) / len(seven)
    for lh, top in seven:
        chord(t, lh, 0.28, gap * 1.15, roll=0.06, out=ev)
        ev.append((t + gap * 0.45, top, 0.36, gap * 0.9))
        t += gap
    chord(TEND, [29, 41, 48, 57, 65, 69], 0.40, TFATHER - TEND + 1.0, roll=0.09, out=ev)
    ev.append((TEND + 0.6, 72, 0.36, TFATHER - TEND))
    chord(TFATHER, [26, 38, 45], 0.26, END - TFATHER, roll=0.12, out=ev)
    step = min(1.6, (END - TFATHER - 2.0) / 3)
    for k, n in enumerate((69, 65, 62)):
        ev.append((TFATHER + 0.4 + k * step, n, 0.34 - 0.03 * k, END - (TFATHER + 0.4 + k * step)))
    return ev


def hall_ir(seconds=2.6, rt60=2.1, seed=9):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    decay = np.exp(-6.91 * t / rt60)
    chans = []
    for c in range(2):
        noise = r.standard_normal(n) * decay
        # darker as it decays: one-pole lowpass whose cutoff falls over time, done in blocks
        out = np.zeros(n)
        y = 0.0
        blk = 256
        for i in range(0, n, blk):
            fc = 9000 * np.exp(-t[i] / 0.9) + 1200
            a = np.exp(-2 * np.pi * fc / SR)
            seg = noise[i:i + blk]
            res = np.empty_like(seg)
            for j, s in enumerate(seg):
                y = (1 - a) * s + a * y
                res[j] = y
            out[i:i + blk] = res
        for d, g in ((0.013, 0.5), (0.021, 0.35), (0.029, 0.3), (0.037, 0.22)):
            out[int(d * SR) + c * 7] += g
        chans.append(out)
    ir = np.stack(chans, axis=1)
    return ir / np.sqrt(np.sum(ir ** 2, axis=0))[None, :] * 0.5


def render(ev, total, seed=12):
    r = np.random.default_rng(seed)
    n = int((total + 3) * SR)
    dry = np.zeros((n, 2))
    for (t, midi, vel, dur) in ev:
        t = t + r.uniform(-0.006, 0.006)
        vel = float(np.clip(vel + r.uniform(-0.025, 0.025), 0.05, 1.0))
        y = voice(midi, vel, max(0.05, dur))
        i = int(max(0, t) * SR)
        m = min(len(y), n - i)
        if m > 0:
            dry[i:i + m] += y[:m]
    ir = hall_ir()
    wet = np.stack([fftconvolve(dry[:, c], ir[:, c])[:n] for c in (0, 1)], axis=1)
    return 0.82 * dry + 0.30 * wet
