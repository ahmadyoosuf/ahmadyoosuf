"""Mix and master the 77 MINUTES soundtrack from the timeline's cue list.

  python tools/audio.py film A          -> assets/audio/mix_A.wav (+ stems)
  python tools/audio.py open A|B        -> assets/audio/open_A.wav / open_B.wav (film's master gain)
  python tools/audio.py square          -> assets/audio/mix_square.wav (film's master gain)

Master: integrated loudness -16.0 LUFS (ITU-R BS.1770-4 via pyloudnorm), then a 4x
oversampled true-peak limiter at -2.0 dBTP (headroom for AAC encoding). The opens and the square are excerpts and
keep the film's master gain (DECISIONS D043, D046). Every strike lands on the frame its character appears (cue times
come from build.py, already on the 24 fps grid).
"""
import json
import pathlib
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.ndimage import minimum_filter1d
from scipy.signal import resample_poly

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import sfx  # noqa: E402
import music  # noqa: E402

SR = sfx.SR
AUD = ROOT / "assets" / "audio"
TARGET_LUFS = -16.0
CEILING_DBTP = -2.0


def db(x):
    return 10 ** (x / 20)


def place(buf, t, y, gain=1.0, p=0.0):
    i = int(round(t * SR))
    if y.ndim == 1:
        y = sfx.pan(y, p)
    m = min(len(y), len(buf) - i)
    if i < 0 or m <= 0:
        return
    buf[i:i + m] += gain * y[:m]


def env_points(n, points):
    """Piecewise-linear gain envelope from [(t, gain), ...]."""
    t = np.arange(n) / SR
    ts = [p[0] for p in points]
    gs = [p[1] for p in points]
    return np.interp(t, ts, gs)


def rms_norm(x):
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-12)


def build_layers(cue, timeline, with_music=True):
    total = cue["total"]
    n = int((total + 0.5) * SR)
    keys = np.zeros((n, 2))
    amb = np.zeros((n, 2))
    ev = cue["events"]
    secs = {s["sid"]: s for s in cue["sections"]}

    # ---- typewriter and foley
    typed_by_card = {}
    for e in ev:
        if e["kind"] in ("key", "space", "heavy"):
            typed_by_card.setdefault(e["card"], []).append(e)
    seed = 1000
    for card, strikes in typed_by_card.items():
        for k, e in enumerate(strikes):
            seed += 1
            if e["kind"] == "space":
                place(keys, e["t"], sfx.key_strike(seed, space=True), db(-17), p=-0.05)
            else:
                heavy = e["kind"] == "heavy"
                g = db(-7.5) if heavy else db(-11.5)
                # the carriage travels left to right: pan follows the column a little
                p = -0.25 + 0.5 * (k % 46) / 45
                place(keys, e["t"], sfx.key_strike(seed, heavy=heavy), g, p=p)
        if len(strikes) > 45 and not card.endswith("title"):
            # the margin bell, eight keys before the end of the first line
            place(keys, strikes[37]["t"] + 0.01, sfx.margin_bell(seed), db(-21), p=0.25)
    for e in ev:
        k = e["kind"]
        if k == "return":
            place(keys, e["t"], sfx.carriage_return(int(e["t"] * 100)), db(-14), p=0.15)
        elif k == "pen":
            place(keys, e["t"], sfx.pen_scratch(int(e["t"] * 1000), e["dur"], e["width"]), db(-31), p=0.35)
        elif k == "knock":
            place(keys, e["t"], sfx.knock(77), db(-23), p=-0.4)

    # paper: the sheet is laid down whenever a paper ground opens
    for s in cue["sections"]:
        if s["ground"] == "paper":
            place(keys, s["start"] + 0.12, sfx.paper_handle(int(s["start"] * 10), 0.9), db(-30), p=0.1)
    for e in ev:
        if e["kind"] == "pen" and e["card"] and e is next(x for x in ev if x["kind"] == "pen"):
            place(keys, e["t"] - 0.32, sfx.paper_handle(4242, 0.7), db(-31), p=0.1)
    # one page turn under the father's books
    for sec in timeline["sections"]:
        for c in sec["cards"]:
            if c["id"] == "s1-father":
                place(keys, sec["start"] + c["start"] + 2.2, sfx.page_turn(88), db(-31), p=0.2)

    # ---- beds
    room = sfx.room_tone(n) * db(-49)
    pts = [(0, 0.0), (0.15, 1.0)]
    for e in ev:
        if e["kind"] == "black-in":
            pts += [(e["t"] - 0.001, 1.0), (e["t"] + 0.03, 0.0)]
        if e["kind"] == "black-out":
            pts += [(e["t"], 0.0), (e["t"] + 0.25, 1.0)]
    pts += [(total - 1.2, 1.0), (total, 0.0)]
    pts.sort()
    amb += room * env_points(n, pts)[:, None]

    if "s1" in secs:
        s1 = secs["s1"]
        sea = sfx.sea(n) * db(-37)
        amb += sea * env_points(n, [(0, 0), (s1["start"], 0), (s1["start"] + 3.5, 1), (s1["end"] - 3.5, 1),
                                    (s1["end"], 0), (total, 0)])[:, None]
    wind_pts = None
    rise = next((e["t"] for e in ev if e["kind"] == "wind-rise"), None)
    if rise is not None:
        peak = next(e["t"] for e in ev if e["kind"] == "wind-peak")
        fall = next(e["t"] for e in ev if e["kind"] == "wind-fall")
        wind_pts = [(0, 0), (rise - 0.3, 0), (rise + 2.5, 0.55), (peak, 0.65), (peak + 2.0, 1.0),
                    (fall, 0.7), (fall + 5.0, 0.0), (total, 0)]
        w = sfx.wind(n) * db(-28)
        amb += w * env_points(n, wind_pts)[:, None]

    mus = np.zeros((n, 2))
    if with_music and "s3" in secs:
        anchors = music_anchors(timeline)
        ev_m = music.score(anchors)
        mus = music.render(ev_m, total)[:n]
        if len(mus) < n:
            mus = np.vstack([mus, np.zeros((n - len(mus), 2))])
        meter = pyln.Meter(SR)
        lufs = meter.integrated_loudness(mus)
        mus *= db(-20.0 - lufs)
    return keys, amb, mus


def music_anchors(tl):
    S = {s["sid"]: s for s in tl["sections"]}

    def card(sid, cid):
        sec = S[sid]
        for c in sec["cards"]:
            if c["id"] == cid:
                return sec, c
        raise KeyError(cid)

    sec, c = card("s4", "s4-saying")
    brk = sec["start"] + c["start"]
    sec, c = card("s5", "s5-cooking")
    cook = sec["start"] + c["start"]
    sec, c = card("s6", "s6-say")
    say = sec["start"] + c["parts_t"][1]["t0"]
    sec, c = card("s7", "s7-end")
    end_card = sec["start"] + c["start"]
    sec, c = card("s7", "s7-father")
    father = sec["start"] + c["start"]
    return dict(s3=S["s3"]["start"], s4=S["s4"]["start"], **{"break": brk}, cook=cook, s6=S["s6"]["start"], say=say,
                s7=S["s7"]["start"], end_card=end_card, father=father, end=tl["total"])


def _os_peaks(x, block=48):
    """Per-block (1 ms) maximum of the 4x-oversampled absolute signal, computed in chunks."""
    n = len(x)
    out = np.zeros(int(np.ceil(n / block)))
    chunk = SR * 10
    pad = 64
    for a in range(0, n, chunk):
        lo, hi = max(0, a - pad), min(n, a + chunk + pad)
        seg = x[lo:hi]
        os_ = np.max(np.abs(np.stack([resample_poly(seg[:, c], 4, 1) for c in range(seg.shape[1])], axis=1)), axis=1)
        os_ = os_[(a - lo) * 4:(a - lo) * 4 + (min(n, a + chunk) - a) * 4]
        m = len(os_) // 4
        per = os_[: m * 4].reshape(m, 4).max(axis=1)
        nb = int(np.ceil(m / block))
        padded = np.concatenate([per, np.zeros(nb * block - m)])
        out[a // block:a // block + nb] = np.maximum(out[a // block:a // block + nb], padded.reshape(nb, block).max(axis=1))
    return out


def true_peak_db(x):
    return 20 * np.log10(np.max(_os_peaks(x)) + 1e-12)


def limit(x, ceiling_db=CEILING_DBTP, release=0.08, block=48):
    """Look-ahead true-peak limiter working on a 1 ms gain grid."""
    thr = db(ceiling_db)
    for _ in range(4):
        peaks = _os_peaks(x, block)
        g = np.minimum(1.0, thr / np.maximum(peaks, 1e-12))
        if g.min() >= 0.9999:
            break
        g = minimum_filter1d(g, size=5)  # +-2 ms look-ahead/hold
        a = np.exp(-1.0 / (release * SR / block))
        sm = np.empty_like(g)
        cur = 1.0
        for i in range(len(g)):
            cur = g[i] if g[i] < cur else a * cur + (1 - a) * g[i]
            sm[i] = cur
        # back to samples: hold each block's gain, then a 1 ms linear blend
        gs = np.repeat(sm, block)[: len(x)]
        k = np.ones(block) / block
        gs = np.minimum(gs, np.convolve(gs, k, mode="same"))
        x = x * gs[:, None]
    return x


def master(mix):
    meter = pyln.Meter(SR)
    lufs = meter.integrated_loudness(mix)
    gain_db = TARGET_LUFS - lufs
    y = limit(mix * db(gain_db))
    # the limiter takes a hair off; re-trim once and re-limit
    lufs2 = meter.integrated_loudness(y)
    if abs(lufs2 - TARGET_LUFS) > 0.1:
        g2 = TARGET_LUFS - lufs2
        y = limit(y * db(g2))
        gain_db += g2
    return y, gain_db


def write(path, x, sub="PCM_24"):
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), np.clip(x, -1, 1), SR, subtype=sub)


def report(name, x):
    meter = pyln.Meter(SR)
    print(f"{name}: integrated {meter.integrated_loudness(x):.2f} LUFS, true peak {true_peak_db(x):.2f} dBTP, "
          f"{len(x) / SR:.2f} s")


def main():
    what = sys.argv[1]
    if what == "film":
        key = sys.argv[2] if len(sys.argv) > 2 else "A"
        cue = json.loads((ROOT / "build" / f"cues-{key}.json").read_text())
        tl = json.loads((ROOT / "build" / f"timeline-{key}.json").read_text())
        keys, amb, mus = build_layers(cue, tl)
        for nm, layer in (("keys", keys), ("amb", amb), ("music", mus)):
            write(AUD / "stems" / f"{nm}_{key}.wav", layer)
        y, gain = master(keys + amb + mus)
        write(AUD / f"mix_{key}.wav", y)
        (ROOT / "build" / f"master-{key}.json").write_text(json.dumps(dict(gain_db=gain)))
        report(f"mix_{key}", y)
        print(f"master gain {gain:+.2f} dB")
    elif what in ("open", "square"):
        key = sys.argv[2] if what == "open" else "square"
        cue = json.loads((ROOT / "build" / (f"cues-open-{key}.json" if what == "open" else "cues-square.json")).read_text())
        tl_name = "timeline-A.json" if what == "open" else "timeline-square.json"
        tl = json.loads((ROOT / "build" / tl_name).read_text())
        gain = json.loads((ROOT / "build" / "master-A.json").read_text())["gain_db"]
        keys, amb, mus = build_layers(cue, tl, with_music=False)
        y = limit((keys + amb + mus) * db(gain))
        out = AUD / (f"open_{key}.wav" if what == "open" else "mix_square.wav")
        write(out, y)
        report(out.name, y)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
