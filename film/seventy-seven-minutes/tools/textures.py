"""Procedural grounds for 77 MINUTES, built only from the film's two neutral colours.

night: ink #1B1A17 with a reading-lamp falloff (paper at <= 7%) and fine grain that
       dithers the gradient so it does not band in 8-bit H.264.
paper: paper #F2EBDD with fibres, mottling and a soft lamp-lit edge (ink at <= 9%).

Every pixel is ink*(1-a) + paper*a, so no colour outside the palette is introduced
(DECISIONS D017). Seeded, so the textures are identical on every run.
"""
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "textures"

INK = np.array([0x1B, 0x1A, 0x17], dtype=np.float64)
PAPER = np.array([0xF2, 0xEB, 0xDD], dtype=np.float64)


def mottle(h, w, rng, scales=((180, 1.0), (60, 0.55), (14, 0.3))):
    acc = np.zeros((h, w))
    for s, amp in scales:
        n = rng.standard_normal((h, w))
        n = gaussian_filter(n, s, mode="wrap")
        n /= n.std() + 1e-9
        acc += amp * n
    acc /= np.abs(acc).max()
    return acc  # roughly -1..1


def fibres(h, w, rng, count, alpha_range):
    """Thin paper fibres drawn at 2x and downsampled for soft edges."""
    sc = 2
    img = Image.new("L", (w * sc, h * sc), 0)
    d = ImageDraw.Draw(img)
    for _ in range(count):
        x = rng.uniform(0, w * sc)
        y = rng.uniform(0, h * sc)
        ln = rng.uniform(18, 140) * sc
        ang = rng.normal(0.25, 0.9)  # loosely aligned, like a paper's grain direction
        bend = rng.normal(0, 0.35)
        pts = []
        for k in range(6):
            t = k / 5
            a = ang + bend * (t - 0.5)
            pts.append((x + np.cos(a) * ln * t, y + np.sin(a) * ln * t))
        v = int(255 * rng.uniform(*alpha_range))
        d.line(pts, fill=v, width=rng.choice([1, 1, 1, 2]))
    img = img.resize((w, h), Image.LANCZOS)
    return np.asarray(img, dtype=np.float64) / 255.0


def compose(a, w, h):
    rgb = INK[None, None, :] * (1 - a[..., None]) + PAPER[None, None, :] * a[..., None]
    return Image.fromarray(np.clip(np.round(rgb), 0, 255).astype(np.uint8), "RGB")


def night(w, h, seed=7):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    # lamp above the frame, left of centre: light falls across the top-left of the desk
    lx, ly = -0.18 * w, -0.32 * h
    dist = np.hypot((xx - lx) / w, (yy - ly) / h)
    lamp = np.clip(1.25 - dist, 0, None) ** 2.2
    lamp /= lamp.max()
    m = mottle(h, w, rng) * 0.5 + 0.5
    grain = rng.random((h, w))
    a = 0.062 * lamp + 0.006 * m + 0.010 * grain
    return compose(np.clip(a, 0, 0.09), w, h)


def paper(w, h, seed=11):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    m = mottle(h, w, rng) * 0.5 + 0.5
    fib = fibres(h, w, rng, count=int(5200 * w * h / (1920 * 1080)), alpha_range=(0.10, 0.34))
    grain = rng.random((h, w))
    # lamp-lit sheet: brightest top-left, a soft falloff to the far corner and the edges
    cx, cy = 0.30 * w, 0.22 * h
    fall = np.hypot((xx - cx) / w, (yy - cy) / h)
    fall = np.clip(fall - 0.25, 0, None) ** 1.6
    edge = np.minimum.reduce([xx, w - 1 - xx, yy, h - 1 - yy]) / (0.08 * min(w, h))
    edge = np.clip(1 - edge, 0, 1) ** 2
    b = 0.030 * m + 0.080 * fib + 0.012 * grain + 0.048 * fall + 0.024 * edge
    b = np.clip(b, 0, 0.13)
    return compose(1 - b, w, h)  # a = share of paper


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for w, h in ((1920, 1080), (1080, 1080)):
        night(w, h).save(OUT / f"night-{w}x{h}.jpg", quality=95, subsampling=0, optimize=True)
        paper(w, h).save(OUT / f"paper-{w}x{h}.jpg", quality=95, subsampling=0, optimize=True)
    print("textures ->", OUT)


if __name__ == "__main__":
    sys.exit(main())
