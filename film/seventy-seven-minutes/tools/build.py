"""Build 77 MINUTES from timeline/script.py.

Writes (16:9 film):
  compositions/<section>.html     one sub-composition per section (s0a, s0b, s1 ... s7)
  index.html                      the film with cold open A
  index-open-a.html / -open-b.html the two cold opens alone
  build/timeline-<variant>.json   every card, part, word and character with frame-exact times
  build/cues-<variant>.json       audio cue list for tools/audio.py
  /out/holds.json, /out/STORYBOARD.md

Every time is snapped to the 24 fps grid. Holds are computed, never typed in:
hold >= max(2.5, 0.3 * words + 1.2) measured from the frame the last glyph is fully
visible to the first frame of the card's exit (DECISIONS D024).
"""
import argparse
import copy
import html
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "timeline"))
sys.path.insert(0, str(ROOT / "tools"))

import script as S  # noqa: E402
import measure as M  # noqa: E402

FPS = 24
F = 1.0 / FPS
DIS = 8 * F  # the only transition besides a cut
OUT = pathlib.Path("/out")

PAPER, INK, ACCENT = "#F2EBDD", "#1B1A17", "#C8902E"

INK_CPS = 110.0  # soft ink reveal: speed of the word wave across the line
INK_FADE = 0.34  # each word's own fade
WORD_FADE = 0.32  # word-by-word reveal fade (journal)

FACE_FONT = {"fraunces": "fraunces", "italic": "fraunces-italic", "mono": "mono", "tamil": "tamil"}


def fr(t):
    return round(t * FPS)


def snap(t):
    return fr(t) / FPS


def snap_up(t):
    return math.ceil(t * FPS - 1e-6) / FPS


def min_hold(words):
    return max(2.5, 0.3 * words + 1.2)


def words_of(text):
    return [w for w in text.split() if w]


# ------------------------------------------------------------------ layout
class Layout:
    def __init__(self, width, height, margin_x, margin_y):
        self.W, self.H, self.mx, self.my = width, height, margin_x, margin_y
        self.measure = width - 2 * margin_x


WIDE = Layout(1920, 1080, 96, 54)
SQUARE = Layout(1080, 1080, 54, 54)


def variations(face, size):
    if face in ("fraunces", "italic"):
        return {"opsz": min(144, size), "wght": 400, "SOFT": 50, "WONK": 0}
    if face == "mono":
        return {"wght": 400}
    return None


def token_width(tok, face, size, tracking=0.0):
    w = M.width(tok, FACE_FONT[face], size, variations(face, size))
    if tracking:
        w += tracking * size * len(tok)
    return w


def paragraphs(parts):
    """Group parts into paragraphs: a block part starts a new paragraph."""
    paras = []
    for p in parts:
        if p.get("block") or not paras:
            paras.append([p])
        else:
            paras[-1].append(p)
    return paras


def word_groups(p):
    """[(words, accented)] for a part; an accent phrase is one unbreakable group."""
    words = p["text"].split(" ")
    mask = accent_mask(p["text"], p.get("accent", [])) if p.get("accent") else [False] * len(p["text"])
    groups, pos, prev = [], 0, False
    for w in words:
        acc = any(mask[pos:pos + len(w)])
        if acc and prev and groups and p["reveal"] != "type":
            groups[-1][0].append(w)
        else:
            groups.append(([w], acc))
        prev = acc
        pos += len(w) + 1
    return groups


def wrap_para(para, measure):
    """Greedy wrap of a paragraph made of mixed-face parts. Returns list of lines (list of tokens)."""
    tokens = []
    for p in para:
        for g, _acc in word_groups(p):
            tokens.append((" ".join(g), p["face"], p["size"], p.get("tracking", 0.0)))
    lines, cur, cur_w = [], [], 0.0
    for tok in tokens:
        w = token_width(tok[0], tok[1], tok[2], tok[3])
        sp = token_width(" ", tok[1], tok[2], tok[3])
        add = w if not cur else sp + w
        if cur and cur_w + add > measure:
            lines.append(cur)
            cur, cur_w = [tok], w
        else:
            cur.append(tok)
            cur_w += add
    if cur:
        lines.append(cur)
    return lines


def card_lines(card, layout):
    total = 0
    widest = 0.0
    for para in paragraphs(card["parts"]):
        lines = wrap_para(para, layout.measure)
        total += len(lines)
        for ln in lines:
            w = sum(token_width(t[0], t[1], t[2], t[3]) for t in ln) + (len(ln) - 1) * token_width(" ", ln[0][1], ln[0][2])
            widest = max(widest, w)
    return total, widest


# ------------------------------------------------------------------ timing
def coldopen_schedule(text, start):
    """Frame list for the cold-open letter: one key per frame, a space shares the frame of
    the next character, a two-frame breath before "77" and before "Period."."""
    frames = []
    f = fr(start)
    first = True
    i = 0
    while i < len(text):
        ch = text[i]
        if first:
            frames.append(f)
            first = False
            i += 1
            continue
        if ch == " ":
            # the space bar lands with the next key
            nxt = text[i + 1:i + 3]
            f += 1
            if nxt.startswith("77") or text[i + 1:i + 7] == "Period":
                f += 2
            frames.append(f)
            frames.append(f)
            i += 2
            continue
        f += 1
        frames.append(f)
        i += 1
    return frames[:len(text)]


def schedule_part(p, t0, rng_seed=0):
    """Timing for one part starting at t0 (section-local seconds). Returns dict with
    units (words or chars) and the time the part is fully visible."""
    text = p["text"]
    out = {"t0": t0}
    if p["reveal"] == "type":
        chars = list(text)
        if p.get("schedule") == "coldopen":
            frames = coldopen_schedule(text, t0)
        else:
            cps = p.get("cps", 10.0)
            frames = [fr(t0 + i / cps) for i in range(len(chars))]
            # never two keys on one frame for a slow typist
            for i in range(1, len(frames)):
                if frames[i] <= frames[i - 1]:
                    frames[i] = frames[i - 1] + 1
        out["chars"] = [{"c": c, "t": fr_ / FPS} for c, fr_ in zip(chars, frames)]
        out["visible"] = frames[-1] / FPS + F  # glyph is on screen from its frame
    elif p["reveal"] in ("ink", "words"):
        ws = text.split(" ")
        units = []
        if p["reveal"] == "ink":
            cps = p.get("cps", INK_CPS)
            off = 0
            for w in ws:
                units.append({"w": w, "t": snap(t0 + off / cps)})
                off += len(w) + 1
            fade = INK_FADE
        else:
            a, b = p.get("words_from", 0.4), p.get("words_to", 0.2)
            t = t0
            n = len(ws)
            for k, w in enumerate(ws):
                units.append({"w": w, "t": snap(t)})
                frac = k / max(1, n - 2)
                t += a + (b - a) * min(1.0, frac)
            fade = WORD_FADE
        out["words"] = units
        out["fade"] = fade
        out["visible"] = snap_up(units[-1]["t"] + fade)
    elif p["reveal"] == "cut":
        out["visible"] = snap(t0)
    else:
        raise ValueError(p["reveal"])
    return out


def lerp_param(sec, key, idx, n):
    v = sec.get(key)
    if isinstance(v, tuple):
        a, b = v
        return a + (b - a) * (idx / max(1, n - 1))
    return v


def part_width(p):
    return sum(token_width(w, p["face"], p["size"], p.get("tracking", 0.0)) for w in p["text"].split(" ")) + \
        (len(p["text"].split(" ")) - 1) * token_width(" ", p["face"], p["size"])


def sentence_lines(card, layout):
    """When a card's sentences each fit on one line, start each sentence on its own line
    (max two lines). Otherwise they flow in one balanced paragraph. Explicit `block`
    and `inline` settings win."""
    parts = card["parts"]
    if len(parts) < 2 or any(p.get("block") for p in parts[1:]) or card.get("inline"):
        return
    m = layout.measure
    if part_width(parts[0]) > m:
        return
    rest = parts[1:]
    rest_w = sum(part_width(p) for p in rest) + (len(rest) - 1) * token_width(" ", rest[0]["face"], rest[0]["size"])
    if rest_w <= m:
        parts[1]["block"] = True


def time_section(sec, layout, check_lines=True):
    """Lay out cards in section-local time. Returns (cards, duration, issues)."""
    t = sec.get("lead", 0.0)
    n = len(sec["cards"])
    issues = []
    timed = []
    for idx, c in enumerate(sec["cards"]):
        c = copy.deepcopy(c)
        sentence_lines(c, layout)
        extra = c["extra"] if c["extra"] is not None else lerp_param(sec, "extra", idx, n)
        air = c["air"] if c["air"] is not None else lerp_param(sec, "air", idx, n)
        start = snap(t)
        cursor = start + c.get("lead", 0.0)
        parts_t = []
        for p in c["parts"]:
            pt = schedule_part(p, cursor)
            parts_t.append(pt)
            cursor = pt["visible"] + p.get("pause", 0.0)
        last_visible = parts_t[-1]["visible"]
        words = sum(len(words_of(p["text"])) for p in c["parts"])
        hmin = min_hold(words)
        exit_at = snap_up(last_visible + hmin + extra)
        exit_kind = c["exit"]
        end = exit_at + (DIS if exit_kind == "dissolve" else 0.0)
        lines, widest = card_lines(c, layout) if check_lines else (0, 0)
        if check_lines and lines > 2:
            issues.append(f"{c['id']}: {lines} lines at {layout.W}x{layout.H}")
        c.update(dict(start=start, end=snap(end), exit_at=exit_at, last_visible=last_visible, words=words,
                      hold_min=round(hmin, 3), hold=round(exit_at - last_visible, 3), extra_used=round(extra, 3),
                      parts_t=parts_t, lines=lines, widest_px=round(widest)))
        if c["hold"] + 1e-6 < hmin:
            issues.append(f"{c['id']}: hold {c['hold']} < min {hmin}")
        timed.append(c)
        t = end + air
        if c.get("black_after"):
            c["black"] = (snap(end), snap(end + c["black_after"]))
            t = end + c["black_after"] + air
    return timed, snap(t), issues


# ------------------------------------------------------------------ html helpers
FONT_FACES = """
@font-face { font-family: "Fraunces"; src: url("../assets/fonts/fraunces-latin-full-normal.woff2") format("woff2"); font-weight: 100 900; font-style: normal; font-display: block; }
@font-face { font-family: "Fraunces"; src: url("../assets/fonts/fraunces-latin-full-italic.woff2") format("woff2"); font-weight: 100 900; font-style: italic; font-display: block; }
@font-face { font-family: "JetBrains Mono"; src: url("../assets/fonts/jetbrains-mono-latin-wght-normal.woff2") format("woff2"); font-weight: 100 800; font-display: block; }
@font-face { font-family: "Noto Serif Tamil"; src: url("../assets/fonts/noto-serif-tamil-tamil-500-normal.woff2") format("woff2"); font-weight: 500; font-display: block; }
@font-face { font-family: "Noto Emoji"; src: url("../assets/fonts/noto-emoji-9-400-normal.woff2") format("woff2"); font-weight: 400; font-display: block; unicode-range: U+1F605, U+1F622; }
"""


def css(layout, prefix):
    W, H, mx, my = layout.W, layout.H, layout.mx, layout.my
    lift = round(H * 0.06)
    return f"""
{FONT_FACES}
#root {{ position: absolute; inset: 0; overflow: hidden; }}
.{prefix}ground {{ position: absolute; inset: 0; }}
.{prefix}black {{ background: #000; }}
.{prefix}night {{ background: {INK} url("../assets/textures/night-{W}x{H}.jpg") center / cover no-repeat; }}
.{prefix}paper {{ background: {PAPER} url("../assets/textures/paper-{W}x{H}.jpg") center / cover no-repeat; }}
.{prefix}card {{ position: absolute; inset: 0; display: flex; align-items: center;
  padding: {my}px {mx}px {my + lift}px {mx}px; box-sizing: border-box; }}
.{prefix}inner {{ position: relative; width: {layout.measure}px; }}
.{prefix}para {{ margin: 0; text-wrap: balance; font-kerning: normal; }}
.{prefix}para + .{prefix}para {{ margin-top: 0.42em; }}
.{prefix}fraunces, .{prefix}italic {{ font-family: "Fraunces", "Noto Emoji", serif; font-weight: 400;
  font-optical-sizing: auto; font-variation-settings: "SOFT" 50, "WONK" 0; line-height: 1.22; letter-spacing: -0.004em; }}
.{prefix}italic {{ font-style: italic; }}
.{prefix}mono {{ font-family: "JetBrains Mono", "Noto Emoji", monospace; font-weight: 400; line-height: 1.32;
  text-wrap: wrap; font-variant-ligatures: none; }}
.{prefix}tamil {{ font-family: "Noto Serif Tamil", serif; font-weight: 500; line-height: 1.5; padding-left: 0.06em; }}
.{prefix}on-dark {{ color: {PAPER}; }}
.{prefix}on-paper {{ color: {INK}; }}
.{prefix}acc {{ color: {ACCENT}; }}
.{prefix}w {{ display: inline; opacity: 0; }}
.{prefix}ch {{ position: relative; opacity: 0; --c: 0; }}
.{prefix}cs-start {{ position: relative; --c: 0; }}
.{prefix}caret::after, .{prefix}cs-start::after {{ content: ""; position: absolute; top: 0.12em; bottom: 0.06em;
  right: -0.08em; width: 0.08em; background: {PAPER}; opacity: var(--c); }}
.{prefix}cs-start::after {{ right: auto; left: 0; }}
.{prefix}blackout {{ position: absolute; inset: 0; background: #000; z-index: 50; }}
.{prefix}gourd {{ position: absolute; }}
"""


def esc(s):
    return html.escape(s, quote=False)


def accent_mask(text, accents):
    mask = [False] * len(text)
    for a in accents:
        i = text.find(a)
        if i < 0:
            raise ValueError(f"accent {a!r} not in {text!r}")
        for k in range(i, i + len(a)):
            mask[k] = True
    return mask


def render_part_html(p, pt, prefix, cid, pidx, on_paper, caret):
    mask = accent_mask(p["text"], p.get("accent", []))
    cls = f"{prefix}{p['face']}"
    pieces = []
    if p["reveal"] == "type":
        if caret:
            pieces.append(f'<span class="{prefix}cs-start" id="{cid}-p{pidx}-k"></span>')
        for i, ch in enumerate(p["text"]):
            ccls = [f"{prefix}ch"]
            if caret:
                ccls.append(f"{prefix}caret")
            if ch == " ":
                ccls.append(f"{prefix}cs")
            if mask[i]:
                ccls.append(f"{prefix}acc")
            jit = ""
            if p.get("paper") and ch != " ":
                h1 = ((i + 1) * 2246822519 + len(cid) * 3266489917) % 1000 / 1000.0
                h2 = ((i + 7) * 668265263 + len(cid) * 374761393) % 1000 / 1000.0
                jit = f' style="top: {(h1 - 0.5) * 1.3:.2f}px; left: {(h2 - 0.5) * 0.8:.2f}px"'
            pieces.append(f'<span class="{" ".join(ccls)}" id="{cid}-p{pidx}-c{i}"{jit}>{esc(ch)}</span>')
        body = "".join(pieces)
    else:
        out = []
        k = 0
        for g, acc in word_groups(p):
            spans = []
            for w in g:
                wc = f"{prefix}w" + (f" {prefix}acc" if acc and not on_paper else "")
                spans.append(f'<span class="{wc}" id="{cid}-p{pidx}-w{k}">{esc(w)}</span>')
                k += 1
            out.append("\u00a0".join(spans))
        body = " ".join(out)
    size = p["size"]
    style = f"font-size: {size}px;"
    if p.get("tracking"):
        style += f" letter-spacing: {p['tracking']}em;"
    return cls, style, body


def card_html(c, prefix, sec_ground, layout, k=0):
    cid = c["id"]
    ground = c.get("ground", sec_ground)
    on_paper = ground == "paper"
    tone = f"{prefix}on-paper" if on_paper else f"{prefix}on-dark"
    paras = []
    pidx = 0
    for para in paragraphs(c["parts"]):
        spans = []
        pcls, pstyle = None, None
        for p in para:
            pt = c["parts_t"][pidx]
            cls, style, body = render_part_html(p, pt, prefix, cid, pidx, on_paper, p.get("caret", False))
            if pcls is None:
                pcls, pstyle = cls, style
                spans.append(body)
            else:
                spans.append(f'<span class="{cls}" style="{style}">{body}</span>')
            pidx += 1
        lead = para[0]
        ov = M.left_overhang(lead["text"], FACE_FONT[lead["face"]], lead["size"], variations(lead["face"], lead["size"]))
        if ov > 0.5:
            # an italic capital (the gourd card's "A") inks left of its origin: keep it inside the safe margin
            pstyle += f" padding-left: {math.ceil(ov) + 1}px;"
        paras.append(f'<p class="{prefix}para {pcls} {tone}" style="{pstyle}">{" ".join(spans)}</p>')
    gourd = ""
    if c.get("gourd"):
        gourd = gourd_svg(prefix, cid, layout)
    dur = round(c["end"] - c["start"], 4)
    return (f'<div id="{cid}" class="{prefix}card clip" data-start="{c["start"]:.4f}" data-duration="{dur:.4f}" '
            f'data-track-index="{2 + k % 4}" data-layout-allow-overflow>\n'
            f'  <div class="{prefix}inner" id="{cid}-in">{"".join(paras)}</div>{gourd}\n</div>')


# ------------------------------------------------------------------ the gourd
# A bottle gourd (suraikkai, Lagenaria siceraria) in ink: long neck, swelling body,
# a short stem with a curl of tendril and three contour strokes that give it volume.
# Coordinates in a 420 x 860 box. Strokes are drawn in order; each entry is
# (path, duration_s, start_offset_s, width).
GOURD_STROKES = [
    # (path, duration_s, start_offset_s, width, opacity) -- drawn in this order
    # right outline: stem base, over the small upper bulb, in at the waist, round the big bulb
    ("M 212 96 C 250 110 286 150 286 205 C 286 255 256 290 252 330 C 248 372 300 420 340 480 "
     "C 384 546 392 640 366 712 C 338 790 280 832 210 834", 1.45, 0.00, 3.3, 1.0),
    # left outline: back up from the bottom to the stem base
    ("M 210 834 C 140 832 82 790 56 712 C 30 640 38 546 82 480 C 122 420 172 372 168 330 "
     "C 164 290 134 255 134 205 C 134 150 168 110 198 96", 1.35, 1.35, 3.3, 1.0),
    # a second, thinner pass of the pen along the shaded side (sketch weight)
    ("M 254 336 C 254 380 304 424 344 486 C 386 552 393 640 368 714", 0.55, 2.62, 1.3, 0.55),
    # the stem and its cut end
    ("M 198 96 C 197 74 195 50 194 30 M 212 96 C 212 74 211 50 210 30 "
     "M 194 30 C 197 25 207 25 210 30 C 207 34 197 34 194 30", 0.40, 3.05, 3.0, 1.0),
    # a leaf off the stem, and its midrib
    ("M 196 54 C 160 30 112 36 90 64 C 118 86 168 82 196 54 M 196 54 C 160 60 124 62 94 64",
     0.50, 3.40, 2.3, 1.0),
    # a curl of tendril
    ("M 211 60 C 240 46 270 54 276 78 C 282 102 262 116 246 108 C 232 100 238 82 252 84", 0.42, 3.86, 2.0, 1.0),
    # contour lines that give the body its weight
    ("M 266 360 C 276 392 294 420 318 452", 0.22, 4.24, 1.6, 0.9),
    ("M 304 474 C 334 522 352 582 350 650", 0.30, 4.42, 1.6, 0.9),
    ("M 320 566 C 334 614 336 672 322 722", 0.26, 4.68, 1.5, 0.9),
    # a few hatch strokes in the shadow under the belly
    ("M 332 690 L 352 676 M 324 712 L 346 700 M 312 734 L 336 724 M 298 754 L 322 746 M 282 772 L 304 766",
     0.34, 4.90, 1.3, 0.85),
]


def gourd_svg(prefix, cid, layout):
    if layout.W >= 1600:
        x, y, h = 1390, 108, 840
    else:
        x, y, h = 640, 380, 600
    w = round(h * 420 / 860)
    paths = []
    for i, (d, _dur, _off, sw, op) in enumerate(GOURD_STROKES):
        paths.append(f'<path id="{cid}-g{i}" d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" '
                     f'stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round" />')
    return (f'\n  <svg class="{prefix}gourd" id="{cid}-gourd" viewBox="0 0 420 860" width="{w}" height="{h}" '
            f'style="left:{x}px; top:{y}px;" aria-hidden="true">'
            f'<defs><filter id="{cid}-ink" x="-5%" y="-5%" width="110%" height="110%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="77" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter></defs>'
            f'<g filter="url(#{cid}-ink)">{"".join(paths)}</g></svg>')


# ------------------------------------------------------------------ section composition
def caret_spans(chars, start_t, exit_at):
    """Caret on/off windows. Characters that land on the same frame share one caret, which
    sits after the last of them; it stays solid while typing and blinks at 2 Hz after."""
    groups = []
    for i, ch in enumerate(chars):
        if groups and abs(groups[-1][1] - ch["t"]) < 1e-6:
            groups[-1][0] = i
        else:
            groups.append([i, ch["t"]])
    spans = []
    for g, (i, t) in enumerate(groups):
        t_off = groups[g + 1][1] if g + 1 < len(groups) else None
        spans.append((i, t, t_off))
    blink = []
    i_last, t_last, _ = spans[-1]
    t = t_last + 0.5
    on = True
    while t < exit_at - 0.01:
        blink.append((i_last, round(t, 4), 0 if on else 1))
        on = not on
        t += 0.25
    return spans, blink


def section_js(sid, cards, prefix, ground_events, sec_ground):
    O, CAR, BL, W, X = [], [], [], [], []
    starts = []
    for c in cards:
        cid = c["id"]
        on_paper = c.get("ground", sec_ground) == "paper"
        for pidx, (p, pt) in enumerate(zip(c["parts"], c["parts_t"])):
            if p["reveal"] == "type":
                chars = pt["chars"]
                for i, ch in enumerate(chars):
                    target = 1
                    if p.get("paper"):
                        # typewriter strike density varies key to key (seeded, deterministic)
                        h = (i * 2654435761 + len(cid) * 40503) % 1000 / 1000.0
                        target = round(0.80 + 0.20 * h, 3)
                    O.append([f"{cid}-p{pidx}-c{i}", round(ch["t"], 4), target])
                if p.get("caret"):
                    spans, blink = caret_spans(chars, c["start"], c["exit_at"])
                    starts.append([f"{cid}-p{pidx}-k", round(c["start"], 4), round(chars[0]["t"], 4)])
                    for i, t_on, t_off in spans:
                        CAR.append([f"{cid}-p{pidx}-c{i}", round(t_on, 4), None if t_off is None else round(t_off, 4)])
                    for i, t, v in blink:
                        BL.append([f"{cid}-p{pidx}-c{i}", t, v])
            else:
                for k, u in enumerate(pt["words"]):
                    W.append([f"{cid}-p{pidx}-w{k}", round(u["t"], 4), pt["fade"], 1 if (p.get("paper_text") or on_paper) else 0])
        if c["exit"] == "dissolve":
            X.append([f"{cid}-in", round(c["exit_at"], 4)])
            if c.get("gourd"):
                X.append([f"{cid}-gourd", round(c["exit_at"], 4)])
    G = []
    for c in cards:
        if c.get("gourd"):
            base = c["start"] + c.get("gourd_at", 0.32)
            for i, (_d, dur, off, _sw, _op) in enumerate(GOURD_STROKES):
                G.append([f"{c['id']}-g{i}", round(base + off, 4), dur])
    j = lambda v: json.dumps(v, separators=(",", ":"))
    return "\n".join([
        'const tl = gsap.timeline({ paused: true });',
        *ground_events,
        f'const D = {DIS:.4f};',
        '// typed characters: [id, time, strike density]',
        f'const O = {j(O)};',
        'for (const [id, t, o] of O) tl.set("#" + id, { opacity: o }, t);',
        '// the caret before the first key: [id, on, off]',
        f'const K = {j(starts)};',
        'for (const [id, a, b] of K) { tl.set("#" + id, { "--c": 1 }, a); tl.set("#" + id, { "--c": 0 }, b); }',
        '// caret after each key while typing: [id, on, off]',
        f'const CA = {j(CAR)};',
        'for (const [id, a, b] of CA) { tl.set("#" + id, { "--c": 1 }, a); if (b !== null) tl.set("#" + id, { "--c": 0 }, b); }',
        '// 2 Hz blink once typing stops: [id, time, value]',
        f'const BL = {j(BL)};',
        'for (const [id, t, v] of BL) tl.set("#" + id, { "--c": v }, t);',
        '// soft ink reveal, word by word: [id, time, fade, on paper]',
        f'const W = {j(W)};',
        'const glow = (p) => p ? "rgba(27,26,23," : "rgba(242,235,221,";',
        'for (const [id, t, f, p] of W) tl.fromTo("#" + id, { opacity: 0, textShadow: "0 0 14px " + glow(p) + "0.55)" },',
        '  { opacity: 1, textShadow: "0 0 0px " + glow(p) + "0)", duration: f, ease: "power2.out" }, t);',
        '// 8-frame dissolves out: [id, time]',
        f'const X = {j(X)};',
        'for (const [id, t] of X) tl.to("#" + id, { opacity: 0, duration: D, ease: "none" }, t);',
        '// the gourd, drawn stroke by stroke: [id, start, duration]',
        f'const G = {j(G)};',
        'for (const [id, t, d] of G) {',
        '  const el = document.getElementById(id); const len = el.getTotalLength();',
        '  el.style.strokeDasharray = len + " " + len;',
        '  // round caps would show a dot where an undrawn stroke starts: keep it hidden until its turn',
        '  tl.set(el, { opacity: 0 }, 0); tl.set(el, { opacity: 1 }, t);',
        '  tl.fromTo(el, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: d, ease: "sine.inOut" }, t);',
        '}',
        f'window.__timelines["{sid}"] = tl;',
    ])


def build_section_html(sec, cards, duration, layout, prefix, sid, title):
    ground = sec["ground"]
    body = [f'<div id="{sid}-ground" class="{prefix}ground {prefix}{ground}"></div>']
    ground_events = []
    # per-card grounds (the gourd's paper inside section 4)
    paper_from = None
    for c in cards:
        if c.get("ground") and c["ground"] != ground and paper_from is None:
            paper_from = c["start"]
    if paper_from is not None:
        dur = round(duration - paper_from, 4)
        body.append(f'<div id="{sid}-paperclip" class="{prefix}ground clip" data-start="{paper_from:.4f}" '
                    f'data-duration="{dur:.4f}" data-track-index="1"><div id="{sid}-paperin" '
                    f'class="{prefix}ground {prefix}paper"></div></div>')
        ground_events.append(f'tl.fromTo("#{sid}-paperin", {{ opacity: 0 }}, {{ opacity: 1, duration: {DIS:.4f}, '
                             f'ease: "none" }}, {paper_from:.4f});')
    for c in cards:
        body.append(card_html(c, prefix, ground, layout, k=cards.index(c)))
        if c.get("black"):
            a, b = c["black"]
            body.append(f'<div id="{c["id"]}-black" class="{prefix}blackout clip" data-start="{a:.4f}" '
                        f'data-duration="{b - a:.4f}" data-track-index="7"></div>')
    js = section_js(sid, cards, prefix, ground_events, ground)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>77 MINUTES · {esc(title)}</title>
</head>
<body>
<template id="{sid}-template">
<style>
{css(layout, prefix)}
</style>
<div id="root" data-composition-id="{sid}" data-width="{layout.W}" data-height="{layout.H}" data-duration="{duration:.4f}">
{chr(10).join(body)}
</div>
<script>
{js}
</script>
</template>
</body>
</html>
"""


# ------------------------------------------------------------------ assembly
TRANSITIONS = {
    # section id -> how it enters
    "s1": ("black", 0.4),
    "s2": ("black", 0.5),
    "s3": ("black", 0.6),
    "s4": ("cut", 0.0),
    "s5": ("dissolve", 0.0),
    "s6": ("cut", 0.0),
    "s7": ("dissolve", 0.0),
}
# sections whose host fades to black when they end (the card leaves with the ground)
FADE_OUT = {"s1", "s2", "s7"}
TAIL_BLACK = 1.5


def assemble(open_key, layout, prefix="", sections=None, tail=None):
    sections = sections or ([S.OPENS[open_key]] + S.SECTIONS)
    placed = []
    issues = []
    t = 0.0
    for i, sec in enumerate(sections):
        sid = sec["id"]
        cards, dur, iss = time_section(sec, layout)
        issues += iss
        if i == 0:
            start = 0.0
        else:
            kind, gap = TRANSITIONS[sid]
            if kind == "black":
                start = snap(t + gap)
            elif kind == "dissolve":
                start = snap(t - DIS)
            else:
                start = snap(t)
        # a section that fades out to black gets its own fade inside its window
        end = snap(start + dur)
        placed.append(dict(sec=sec, sid=sid, cards=cards, start=start, dur=dur, end=end))
        t = end
    total = snap(t + (TAIL_BLACK if tail is None else tail))
    return placed, total, issues


def root_html(placed, total, layout, audio_src, comp_dir="compositions", root_id="film", title="77 MINUTES"):
    hosts = []
    js = ['const tl = gsap.timeline({ paused: true });']
    for k, pl in enumerate(placed):
        sid = pl["sid"]
        hosts.append(f'  <div id="el-{sid}" data-composition-id="{sid}" data-composition-src="{comp_dir}/{sid}.html" '
                     f'data-start="{pl["start"]:.4f}" data-duration="{pl["dur"]:.4f}" data-track-index="{1 + k % 2}" '
                     f'data-width="{layout.W}" data-height="{layout.H}"></div>')
        if k > 0:
            kind, _gap = TRANSITIONS[sid]
            if kind in ("black", "dissolve"):
                js.append(f'tl.fromTo("#el-{sid}", {{ opacity: 0 }}, {{ opacity: 1, duration: {DIS:.4f}, ease: "none" }}, '
                          f'{pl["start"]:.4f});')
        if sid in FADE_OUT:
            js.append(f'tl.to("#el-{sid}", {{ opacity: 0, duration: {DIS:.4f}, ease: "none" }}, {pl["end"] - DIS:.4f});')
    js.append(f'window.__timelines["{root_id}"] = tl;')
    audio = ""
    if audio_src:
        audio = (f'  <audio id="{root_id}-mix" src="{audio_src}" data-start="0" data-duration="{total:.4f}" '
                 f'data-track-index="10" data-volume="1"></audio>\n')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={layout.W}, height={layout.H}" />
<title>{esc(title)}</title>
<script src="assets/vendor/gsap.min.js"></script>
<style>
html, body {{ margin: 0; width: {layout.W}px; height: {layout.H}px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
#root > div[data-composition-src] {{ position: absolute; inset: 0; }}
</style>
</head>
<body>
<div id="root" data-composition-id="{root_id}" data-start="0" data-width="{layout.W}" data-height="{layout.H}" data-fps="24" data-duration="{total:.4f}">
{chr(10).join(hosts)}
{audio}</div>
<script>
{chr(10).join(js)}
</script>
</body>
</html>
"""


# ------------------------------------------------------------------ cues for audio.py
def cues(placed, total):
    ev = []
    for pl in placed:
        g0 = pl["start"]
        sec = pl["sec"]
        for c in pl["cards"]:
            for p, pt in zip(c["parts"], c["parts_t"]):
                if p["reveal"] == "type":
                    for ch in pt["chars"]:
                        kind = "space" if ch["c"] == " " else ("heavy" if p.get("heavy") else "key")
                        ev.append(dict(t=round(g0 + ch["t"], 4), kind=kind, c=ch["c"], card=c["id"]))
            if c.get("return_after"):
                ev.append(dict(t=round(g0 + c["exit_at"] - 0.02, 4), kind="return", card=c["id"]))
            if c.get("gourd"):
                base = c["start"] + c.get("gourd_at", 0.32)
                for i, (_d, dur, off, sw, _op) in enumerate(GOURD_STROKES):
                    ev.append(dict(t=round(g0 + base + off, 4), kind="pen", dur=dur, width=sw, card=c["id"]))
            if c.get("knock"):
                ev.append(dict(t=round(g0 + c["start"] + 0.15, 4), kind="knock", card=c["id"]))
            if c.get("wind"):
                ev.append(dict(t=round(g0 + c["start"], 4), kind="wind-" + c["wind"], card=c["id"]))
            if c.get("black"):
                a, b = c["black"]
                ev.append(dict(t=round(g0 + a, 4), kind="black-in"))
                ev.append(dict(t=round(g0 + b, 4), kind="black-out"))
        ev.append(dict(t=round(pl["start"], 4), kind="section", sid=pl["sid"], ground=sec["ground"],
                       end=round(pl["end"], 4)))
    ev.sort(key=lambda e: e["t"])
    # the margin bell: a real typewriter rings a few keys before the right margin
    return dict(total=total, fps=FPS, events=ev,
                sections=[dict(sid=pl["sid"], start=pl["start"], end=pl["end"], ground=pl["sec"]["ground"])
                          for pl in placed])


# ------------------------------------------------------------------ outputs
def timeline_json(placed, total):
    return dict(total=total, fps=FPS, sections=[
        dict(sid=pl["sid"], name=pl["sec"]["name"], start=pl["start"], end=pl["end"], ground=pl["sec"]["ground"],
             cards=[{k: v for k, v in c.items() if k not in ("parts",)} | {"parts": c["parts"]} for c in pl["cards"]])
        for pl in placed])


def fmt(t):
    m = int(t // 60)
    s = t - 60 * m
    return f"{m}:{s:05.2f}"


VARIANTS = ROOT.parent / "variants"


def variant_dir(name, comp_dir="compositions"):
    """A sibling HyperFrames project for an alternate root (lint allows one root per project).
    It shares this project's assets and compositions through symlinks."""
    d = VARIANTS / name
    d.mkdir(parents=True, exist_ok=True)
    for link, target in (("assets", ROOT / "assets"), ("compositions", ROOT / comp_dir)):
        lp = d / link
        if lp.is_symlink() or lp.exists():
            lp.unlink()
        lp.symlink_to(pathlib.Path("../../seventy-seven-minutes") / target.relative_to(ROOT))
    (d / "meta.json").write_text(json.dumps({"id": f"77-{name}", "name": f"77 MINUTES {name}"}))
    (d / "hyperframes.json").write_text((ROOT / "hyperframes.json").read_text())
    (d / "package.json").write_text(json.dumps({"name": f"seventy-seven-minutes-{name}", "private": True,
                                                "type": "module"}, indent=2))
    return d


# ------------------------------------------------------------------ square (1080 x 1080, first 60 s)
def _lines(c, layout):
    c2 = copy.deepcopy(c)
    sentence_lines(c2, layout)
    return card_lines(c2, layout)[0]


def split_card(c, layout):
    """Split a card that needs more than two lines at this layout into consecutive cards:
    by sentence groups first, then at the best word boundary of a single long part
    (after punctuation if possible, never inside an accent phrase). Wording and order kept."""
    if _lines(c, layout) <= 2:
        return [c]
    parts = c["parts"]
    if len(parts) > 1:
        groups, cur = [], []
        for prt in parts:
            trial = cur + [prt]
            probe = dict(copy.deepcopy(c), parts=[dict(q, block=(q.get("block") if i else False))
                                                  for i, q in enumerate(copy.deepcopy(trial))])
            if cur and _lines(probe, layout) > 2:
                groups.append(cur)
                cur = [prt]
            else:
                cur = trial
        groups.append(cur)
    else:
        prt = parts[0]
        words = prt["text"].split(" ")
        mask = accent_mask(prt["text"], prt.get("accent", [])) if prt.get("accent") else [False] * len(prt["text"])
        best, best_score = None, None
        pos = 0
        starts = []
        for w in words:
            starts.append(pos)
            pos += len(w) + 1
        for i in range(1, len(words)):
            cut = starts[i] - 1  # the space between words[i-1] and words[i]
            if mask[cut - 1] and mask[cut + 1]:
                continue  # inside an accent phrase
            a, b = " ".join(words[:i]), " ".join(words[i:])
            pa = dict(prt, text=a, accent=[x for x in prt.get("accent", []) if x in a], pause=0.0)
            pb = dict(prt, text=b, accent=[x for x in prt.get("accent", []) if x in b])
            if _lines(dict(c, parts=[pa]), layout) > 2 or _lines(dict(c, parts=[pb]), layout) > 2:
                continue
            score = abs(len(a) - len(b)) - (30 if a.endswith((",", ".", ":", ";")) else 0) - (60 if b.startswith("(") else 0)
            if best_score is None or score < best_score:
                best, best_score = (pa, pb), score
        if best is None:
            raise ValueError(f"cannot split {c['id']} for {layout.W}x{layout.H}")
        groups = [[best[0]], [best[1]]]
    out = []
    for k, g in enumerate(groups):
        nc = copy.deepcopy(c)
        nc["id"] = f"{c['id']}-{k + 1}"
        nc["parts"] = copy.deepcopy(g)
        nc["parts"][0]["block"] = False
        nc["parts"][-1]["pause"] = 0.0
        if k < len(groups) - 1:
            nc["exit"] = "cut" if nc["parts"][0]["reveal"] == "type" else "dissolve"
            nc["air"] = 0.0 if nc["parts"][0]["reveal"] == "type" else 0.2
            nc["extra"] = None
            nc.pop("black_after", None)
        nc["script"] = (c.get("script") or "") + f" (square split {k + 1}/{len(groups)})"
        out += split_card(nc, layout)
    return out


def square_sections():
    secs = []
    for sec in (S.OPEN_A, S.LIBRARY):
        sq = copy.deepcopy(sec)
        sq["cards"] = [x for c in sec["cards"] for x in split_card(c, SQUARE)]
        secs.append(sq)
    return secs


def build_square(limit=60.0):
    secs = square_sections()
    placed, _total, issues = assemble("A", SQUARE, sections=secs, tail=0.0)
    # end on the last card that has finished by the limit, then fade the section to black
    s1 = placed[1]
    keep = [c for c in s1["cards"] if s1["start"] + c["end"] <= limit - DIS - 0.2]
    last = keep[-1]
    s1["cards"] = keep
    s1["dur"] = snap(last["end"] + 0.3)
    s1["end"] = snap(s1["start"] + s1["dur"])
    FADE_OUT.add("s1")
    total = limit
    comp = ROOT / "compositions-square"
    comp.mkdir(exist_ok=True)
    for pl in placed:
        (comp / f"{pl['sid']}.html").write_text(
            build_section_html(pl["sec"], pl["cards"], pl["dur"], SQUARE, "", pl["sid"], pl["sec"]["name"] + " (square)"))
    vdir = variant_dir("square", comp_dir="compositions-square")
    (vdir / "index.html").write_text(root_html(placed, total, SQUARE, "assets/audio/mix_square.wav",
                                               root_id="square", title="77 MINUTES · square, first 60 s"))
    (ROOT / "build" / "timeline-square.json").write_text(json.dumps(timeline_json(placed, total), ensure_ascii=False, indent=1))
    (ROOT / "build" / "cues-square.json").write_text(json.dumps(cues(placed, total), ensure_ascii=False, indent=1))
    for pl in placed:
        for c in pl["cards"]:
            print(f"  sq {c['id']:18s} {fmt(pl['start'] + c['start'])}  hold {c['hold']:5.2f} (min {c['hold_min']:4.2f})"
                  f"  lines {c['lines']}")
    if issues:
        print("SQUARE ISSUES:", issues)
    print("square total", fmt(total), "content ends", fmt(s1["end"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", default="A")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--square", action="store_true")
    args = ap.parse_args()
    if args.square:
        return build_square()

    layout = WIDE
    (ROOT / "compositions").mkdir(exist_ok=True)
    (ROOT / "build").mkdir(exist_ok=True)
    results = {}
    for key in ("A", "B"):
        placed, total, issues = assemble(key, layout)
        results[key] = (placed, total, issues)
    placed, total, issues = results[args.open]
    if issues:
        print("ISSUES:")
        for i in issues:
            print("  ", i)
    if args.report:
        for pl in placed:
            print(f"{pl['sid']:4s} {fmt(pl['start'])} -> {fmt(pl['end'])}  ({pl['dur']:.2f}s)  {pl['sec']['name']}")
            for c in pl["cards"]:
                print(f"     {c['id']:18s} {fmt(pl['start'] + c['start'])}  hold {c['hold']:5.2f} (min {c['hold_min']:4.2f})  "
                      f"lines {c['lines']}  w {c['widest_px']}")
        print("TOTAL", fmt(total), f"({total:.2f}s)")
        for key in ("A", "B"):
            p0 = results[key][0][0]
            print(f"open {key}: {p0['dur']:.2f}s; film total {fmt(results[key][1])}")
        return
    # write section compositions (s0a and s0b both exist; index uses the chosen one)
    written = set()
    for key in ("A", "B"):
        for pl in results[key][0]:
            if pl["sid"] in written:
                continue
            html_ = build_section_html(pl["sec"], pl["cards"], pl["dur"], layout, "", pl["sid"], pl["sec"]["name"])
            (ROOT / "compositions" / f"{pl['sid']}.html").write_text(html_)
            written.add(pl["sid"])
    for key in ("A", "B"):
        pk, tk, _ = results[key]
        (ROOT / "build" / f"timeline-{key}.json").write_text(json.dumps(timeline_json(pk, tk), ensure_ascii=False, indent=1))
        (ROOT / "build" / f"cues-{key}.json").write_text(json.dumps(cues(pk, tk), ensure_ascii=False, indent=1))
        # cold open alone: its own project (one root per project), 1 s of black after
        op = [dict(pk[0])]
        ot = snap(op[0]["end"] + 1.0)
        vdir = variant_dir(f"open-{key.lower()}")
        (vdir / "index.html").write_text(
            root_html(op, ot, layout, f"assets/audio/open_{key}.wav", root_id=f"open-{key.lower()}",
                      title=f"77 MINUTES · cold open {key}"))
        (ROOT / "build" / f"cues-open-{key}.json").write_text(json.dumps(cues(op, ot), ensure_ascii=False, indent=1))
    (ROOT / "index.html").write_text(root_html(placed, total, layout, f"assets/audio/mix_{args.open}.wav"))
    print("wrote", sorted(written), "total", fmt(total))


if __name__ == "__main__":
    main()
