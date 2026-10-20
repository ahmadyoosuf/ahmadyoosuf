"""Shape text with HarfBuzz against the shipped font files and report widths.

Used to plan card splits (max two lines) before anything is built, and later by
build.py to wrap lines exactly the way the cards will.
"""
import functools
import pathlib

import uharfbuzz as hb
from fontTools.ttLib import TTFont

FONTS = pathlib.Path(__file__).resolve().parent.parent / "assets" / "fonts"

FACES = {
    "fraunces": FONTS / "fraunces-latin-full-normal.woff2",
    "fraunces-italic": FONTS / "fraunces-latin-full-italic.woff2",
    "mono": FONTS / "jetbrains-mono-latin-wght-normal.woff2",
    "tamil": FONTS / "noto-serif-tamil-tamil-500-normal.woff2",
    "emoji": FONTS / "noto-emoji-9-400-normal.woff2",
}


@functools.lru_cache(maxsize=None)
def _face(name):
    # woff2 must be decompressed to sfnt bytes for HarfBuzz.
    import io

    tt = TTFont(str(FACES[name]))
    buf = io.BytesIO()
    tt.flavor = None
    tt.save(buf)
    blob = hb.Blob(buf.getvalue())
    face = hb.Face(blob)
    upem = face.upem
    return face, upem, tt


def shape(text, face_name, size_px, variations=None, features=None):
    """Return (advance_px, glyph_names) for one run of text."""
    face, upem, tt = _face(face_name)
    font = hb.Font(face)
    if variations:
        font.set_variations(variations)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    order = tt.getGlyphOrder()
    names = [order[i.codepoint] for i in buf.glyph_infos]
    adv = sum(p.x_advance for p in buf.glyph_positions)
    return adv * size_px / upem, names


EMOJI = {"\U0001F605", "\U0001F622"}


def width(text, face_name, size_px, variations=None):
    """Width of a mixed run, sending emoji codepoints to the emoji face."""
    total = 0.0
    run = ""
    for ch in text:
        if ch in EMOJI:
            if run:
                total += shape(run, face_name, size_px, variations)[0]
                run = ""
            total += shape(ch, "emoji", size_px)[0]
        else:
            run += ch
    if run:
        total += shape(run, face_name, size_px, variations)[0]
    return total


def wrap(text, face_name, size_px, measure_px, variations=None):
    """Greedy word wrap identical in spirit to the browser's (spaces collapse)."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w) if cur else w
        if width(trial, face_name, size_px, variations) <= measure_px or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


if __name__ == "__main__":
    import sys

    fv = {"opsz": 64, "wght": 400, "SOFT": 50, "WONK": 0}
    for line in sys.stdin.read().splitlines():
        if not line.strip():
            continue
        w = width(line, "fraunces", 64, fv)
        print(f"{w:7.0f}px {len(line):3d}ch  {line}")


def left_overhang(text, face_name, size_px, variations=None):
    """How far (px) the first glyph's ink reaches left of the pen origin; 0 when it doesn't."""
    if text[:1] in EMOJI:
        return 0.0
    face, upem, tt = _face(face_name)
    font = hb.Font(face)
    if variations:
        font.set_variations(variations)
    buf = hb.Buffer()
    buf.add_str(text[:8])
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    info, pos = buf.glyph_infos[0], buf.glyph_positions[0]
    ext = font.get_glyph_extents(info.codepoint)
    left = pos.x_offset + (ext.x_bearing if ext else 0)
    return max(0.0, -left * size_px / upem)
