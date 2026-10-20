"""Procedural sound for 77 MINUTES (DECISIONS D016): every effect is synthesized here,
seeded, so the film's sound is original and reproducible. 48 kHz, float64, stereo.

Nothing here is a whoosh, riser, glitch or impact: the palette is a typewriter, paper,
a pen nib, a door, wind, a distant sea and the room.
"""
import numpy as np
from scipy.signal import butter, sosfilt, lfilter

SR = 48000


def _rng(seed):
    return np.random.default_rng(seed)


def bandpass(x, lo, hi, order=2):
    sos = butter(order, [lo / (SR / 2), hi / (SR / 2)], btype="band", output="sos")
    return sosfilt(sos, x)


def lowpass(x, f, order=2):
    sos = butter(order, f / (SR / 2), btype="low", output="sos")
    return sosfilt(sos, x)


def highpass(x, f, order=2):
    sos = butter(order, f / (SR / 2), btype="high", output="sos")
    return sosfilt(sos, x)


def damped(freq, tau, n, phase=0.0):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * t + phase) * np.exp(-t / tau)


def pan(mono, p):
    """p in [-1, 1]; equal-power."""
    a = (p + 1) * np.pi / 4
    return np.stack([mono * np.cos(a), mono * np.sin(a)], axis=1)


# ---------------------------------------------------------------- typewriter
def key_strike(seed, heavy=False, space=False):
    r = _rng(seed)
    n = int(0.16 * SR)
    out = np.zeros(n)
    if space:
        # space bar: a broad, low, wooden-plastic thud plus the escapement tick
        out += 0.55 * damped(r.uniform(85, 110), 0.022, n)
        out += 0.25 * damped(r.uniform(420, 520), 0.010, n)
        click = r.standard_normal(int(0.002 * SR)) * np.exp(-np.arange(int(0.002 * SR)) / (0.0006 * SR))
        out[:len(click)] += 0.18 * highpass(click, 2500)
    else:
        g = 1.6 if heavy else 1.0
        # typebar hits the platen: a hard broadband transient
        nc = int(0.003 * SR)
        click = r.standard_normal(nc) * np.exp(-np.arange(nc) / (0.0007 * SR))
        out[:nc] += g * 0.9 * highpass(click, 900)
        # metal ring of bar and frame
        for f0, tau, amp in ((r.uniform(1500, 1800), 0.020, 0.22), (r.uniform(2700, 3300), 0.012, 0.16),
                             (r.uniform(4300, 5200), 0.007, 0.10)):
            out += g * amp * damped(f0, tau * (1.5 if heavy else 1.0), n, r.uniform(0, 6.28))
        # body thump through the desk
        out += g * 0.5 * damped(r.uniform(135, 190), 0.020 * (1.4 if heavy else 1.0), n)
        out += g * 0.18 * damped(r.uniform(620, 820), 0.010, n)
        # escapement tick as the carriage steps, 9-16 ms later
        d = int(r.uniform(0.009, 0.016) * SR)
        ne = int(0.0015 * SR)
        esc = r.standard_normal(ne) * np.exp(-np.arange(ne) / (0.0004 * SR))
        out[d:d + ne] += 0.22 * highpass(esc, 3000)
        # key returning, 32-48 ms later, softer
        d2 = int(r.uniform(0.032, 0.048) * SR)
        nr = int(0.002 * SR)
        ret = r.standard_normal(nr) * np.exp(-np.arange(nr) / (0.0006 * SR))
        out[d2:d2 + nr] += 0.28 * bandpass(ret, 1200, 6000)
        out[d2:] += 0.08 * damped(r.uniform(900, 1300), 0.006, n - d2)
    env = np.ones(n)
    env[-int(0.02 * SR):] = np.linspace(1, 0, int(0.02 * SR))
    return out * env * (r.uniform(0.85, 1.05))


def margin_bell(seed=3):
    r = _rng(seed)
    n = int(1.6 * SR)
    f0 = 2350.0
    out = np.zeros(n)
    for ratio, tau, amp in ((1.0, 0.85, 0.5), (2.41, 0.42, 0.26), (3.83, 0.26, 0.16), (5.31, 0.16, 0.08)):
        out += amp * damped(f0 * ratio * r.uniform(0.995, 1.005), tau, n, r.uniform(0, 6.28))
    nc = int(0.002 * SR)
    out[:nc] += 0.3 * highpass(r.standard_normal(nc), 3000)
    # gentle beating between the two halves of the bell
    out *= 1 + 0.06 * np.sin(2 * np.pi * 5.5 * np.arange(n) / SR)
    return out


def carriage_return(seed=5):
    """Ratchet clicks of the line feed, a slide of the carriage, a stop."""
    r = _rng(seed)
    dur = 0.62
    n = int(dur * SR)
    out = np.zeros(n)
    # ratchet: 11 clicks, faster in the middle
    ts = np.cumsum(np.concatenate([[0.0], r.uniform(0.022, 0.034, 10)]))
    for k, t in enumerate(ts):
        i = int(t * SR)
        nc = int(0.004 * SR)
        c = r.standard_normal(nc) * np.exp(-np.arange(nc) / (0.0009 * SR))
        seg = bandpass(c, 1800, 7000) * (0.5 + 0.3 * np.sin(k / 10 * np.pi))
        out[i:i + nc] += seg[:max(0, min(nc, n - i))]
    # the carriage sliding back (filtered noise swell, short and papery-metal)
    t = np.arange(n) / SR
    slide = bandpass(r.standard_normal(n), 900, 4200) * np.clip((t - 0.10) / 0.12, 0, 1) * np.exp(-np.clip(t - 0.30, 0, None) / 0.06)
    out += 0.25 * slide
    # the stop: a low knock at the margin
    i = int(0.46 * SR)
    m = n - i
    out[i:] += 0.6 * damped(150, 0.030, m) + 0.2 * damped(700, 0.012, m)
    return out


# ---------------------------------------------------------------- paper, pen, door
def paper_handle(seed, dur=0.9, amount=1.0):
    r = _rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    # crinkle: a Poisson train of tiny impulses through a bright band
    rate = 120 + 300 * np.sin(np.pi * t / dur) ** 2
    imp = (r.random(n) < rate / SR) * r.standard_normal(n)
    crk = bandpass(imp, 2000, 9000) * 6.0
    # the sheet's body sliding: a soft low-mid rustle
    body = bandpass(r.standard_normal(n), 300, 1600) * 0.35
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return amount * (crk + body) * env


def page_turn(seed):
    r = _rng(seed)
    a = paper_handle(seed, 0.55, 0.9)
    n = len(a)
    t = np.arange(n) / SR
    flap = lowpass(r.standard_normal(n), 900) * np.exp(-np.abs(t - 0.38) / 0.05) * 0.5
    return a + flap


def pen_scratch(seed, dur, width):
    """A nib drawing one stroke: bright friction modulated by the hand's micro-jitter."""
    r = _rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = r.standard_normal(n)
    bright = bandpass(noise, 2600, 7500)
    mid = bandpass(r.standard_normal(n), 700, 1800) * 0.25
    # roughness: 40-70 Hz grain from paper fibres
    rough = 0.6 + 0.4 * np.abs(lowpass(r.standard_normal(n), 60) * 8).clip(0, 1)
    speed = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.6  # pressure eases in and out of the stroke
    return (bright + mid) * rough * speed * (0.6 + 0.12 * width)


def knock(seed):
    r = _rng(seed)
    n = int(0.9 * SR)
    out = np.zeros(n)
    for k, t in enumerate((0.0, 0.31)):
        i = int(t * SR)
        m = n - i
        g = 1.0 if k == 0 else 0.85
        out[i:] += g * (0.7 * damped(r.uniform(100, 120), 0.045, m) + 0.35 * damped(r.uniform(360, 400), 0.028, m)
                        + 0.15 * damped(r.uniform(900, 1000), 0.012, m))
        nc = int(0.003 * SR)
        out[i:i + nc] += g * 0.2 * bandpass(r.standard_normal(nc), 800, 4000)
    # heard through a door, from the next room: dull it
    return lowpass(out, 1400)


# ---------------------------------------------------------------- beds (stereo)
def _brown(n, r):
    w = r.standard_normal(n)
    b = lfilter([1.0], [1.0, -0.995], w)
    b -= np.mean(b)
    return b / (np.std(b) + 1e-9)


def room_tone(n, seed=21):
    r = _rng(seed)
    L = lowpass(_brown(n, r), 420) + 0.05 * highpass(r.standard_normal(n), 3000)
    R = lowpass(_brown(n, r), 420) + 0.05 * highpass(r.standard_normal(n), 3000)
    x = np.stack([L, R], axis=1)
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)


def sea(n, seed=31):
    """Distant surf: slow swells of low noise with a little foam on each break."""
    r = _rng(seed)
    t = np.arange(n) / SR
    env = np.zeros(n)
    tt = r.uniform(0, 3)
    while tt < n / SR:
        period = r.uniform(7.0, 10.5)
        rise, fall = r.uniform(2.2, 3.2), r.uniform(3.5, 5.0)
        a = r.uniform(0.6, 1.0)
        seg = np.where(t < tt, 0, np.where(t < tt + rise, ((t - tt) / rise) ** 2,
                                           np.exp(-(t - tt - rise) / fall * 2.2)))
        env += a * np.where(t >= tt, seg, 0)
        tt += period
    env = lowpass(env, 3)
    chans = []
    for _ in range(2):
        body = lowpass(_brown(n, r), 700)
        foam = highpass(r.standard_normal(n), 1800) * 0.18
        chans.append(body * (0.35 + env) + foam * env ** 2)
    x = np.stack(chans, axis=1)
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)


def wind(n, seed=41):
    """Gusting wind: resonant bands that wander, a faint high whistle."""
    r = _rng(seed)
    t = np.arange(n) / SR
    gust = (0.55 + 0.25 * np.sin(2 * np.pi * 0.071 * t + 1.3) + 0.15 * np.sin(2 * np.pi * 0.13 * t + 0.2)
            + 0.08 * np.sin(2 * np.pi * 0.29 * t + 2.0))
    chans = []
    for c in range(2):
        src = _brown(n, r) * 0.6 + r.standard_normal(n) * 0.4
        # time-varying resonance approximated by crossfading three fixed bands with the gust
        b1 = bandpass(src, 220, 520)
        b2 = bandpass(src, 480, 1000)
        b3 = bandpass(src, 1100, 2400) * 0.35
        g = np.clip(gust + 0.05 * c, 0, 1.2)
        mix = b1 * (1.2 - g) + b2 * g + b3 * g ** 2
        chans.append(mix * g)
    x = np.stack(chans, axis=1)
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)
