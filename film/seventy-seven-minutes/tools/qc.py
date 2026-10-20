"""Scene QC for 77 MINUTES (Workflow step 4).

  python tools/qc.py sheet <sid>   1 fps contact sheet of a section + 3 full-res keyframes
  python tools/qc.py cards         every card at mid-hold: measured text box vs. the 5% safe
                                   area and the number of rendered lines (pixel analysis)
  python tools/qc.py cards A /out/77minutes_1080p.mp4      the same, measured on a delivered file
  python tools/qc.py cards square /out/77minutes_square.mp4

Frames come from `npx hyperframes snapshot`, i.e. the same seek path the renderer uses, or
from the delivered MP4 itself.
"""
import json
import pathlib
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path("/out/qc")
TMP = ROOT / "build" / "qc"
FONT = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"


def snapshot(times, outdir, project=ROOT):
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    frames = []
    # the CLI takes a comma list; chunk to keep each browser session short
    for k in range(0, len(times), 40):
        chunk = times[k:k + 40]
        sub = outdir / f"chunk{k:03d}"
        at = ",".join(f"{t:.3f}" for t in chunk)
        subprocess.run(["npx", "hyperframes", "snapshot", str(project), "--at", at, "--no-end", "--output", str(sub)],
                       check=True, capture_output=True, text=True, timeout=1800)
        got = sorted(sub.glob("frame-*.png"), key=lambda p: int(p.name.split("-")[1]))
        if len(got) != len(chunk):
            raise RuntimeError(f"expected {len(chunk)} frames, got {len(got)} in {sub}")
        frames += list(zip(chunk, got))
    return frames


def mp4_frames(mp4, times, outdir):
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    frames = []
    for i, t in enumerate(times):
        path = outdir / f"frame-{i:03d}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        str(path)], check=True)
        frames.append((t, path))
    return frames


def timeline(key="A"):
    return json.loads((ROOT / "build" / f"timeline-{key}.json").read_text())


def section(tl, sid):
    for s in tl["sections"]:
        if s["sid"] == sid:
            return s
    raise KeyError(sid)


def contact(frames, path, cols=10, thumb=(320, 180), title=""):
    rows = (len(frames) + cols - 1) // cols
    pad, head = 6, 34
    W = cols * thumb[0] + (cols + 1) * pad
    H = rows * (thumb[1] + 22) + (rows + 1) * pad + head
    sheet = Image.new("RGB", (W, H), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 15)
    ft = ImageFont.truetype(FONT, 20)
    d.text((pad, 7), title, fill=(230, 230, 230), font=ft)
    for i, (t, p) in enumerate(frames):
        im = Image.open(p).convert("RGB").resize(thumb, Image.LANCZOS)
        r, c = divmod(i, cols)
        x = pad + c * (thumb[0] + pad)
        y = head + pad + r * (thumb[1] + 22 + pad)
        sheet.paste(im, (x, y))
        m = int(t // 60)
        d.text((x + 2, y + thumb[1] + 3), f"{m}:{t - 60 * m:05.2f}", fill=(200, 200, 200), font=f)
    sheet.save(path, quality=88)


def cmd_sheet(sid, key="A"):
    tl = timeline(key)
    s = section(tl, sid)
    a, b = s["start"], s["end"]
    times = list(np.arange(np.ceil(a) + 0.0, b, 1.0))
    frames = snapshot(times, TMP / f"sheet-{sid}")
    OUT.mkdir(parents=True, exist_ok=True)
    contact(frames, OUT / f"{sid}_sheet.jpg", title=f"{sid} · {s['name']} · {a:.2f}–{b:.2f} s · 1 frame per second")
    # three keyframes: first card mid-reveal, the densest card at hold, the section's last card at hold
    cards = s["cards"]
    first = cards[0]
    dense = max(cards, key=lambda c: c["words"])
    last = cards[-1]
    picks = [
        ("reveal", a + first["start"] + (first["last_visible"] - first["start"]) * 0.55),
        ("hold", a + dense["last_visible"] + 0.6),
        ("last", a + last["last_visible"] + 0.4),
    ]
    kf = snapshot([t for _, t in picks], TMP / f"key-{sid}")
    for (label, t), (_, p) in zip(picks, kf):
        shutil.copy(p, OUT / f"{sid}_key_{label}_{t:.2f}s.png")
    print(f"{sid}: {len(frames)} frames -> {OUT / (sid + '_sheet.jpg')}; keyframes at " +
          ", ".join(f"{t:.2f}" for _, t in picks))


def text_mask(im, ground):
    a = np.asarray(im.convert("L")).astype(np.int16)
    if ground == "paper":
        return a < 165
    return a > 95


def lines_in(mask, min_gap=3):
    rows = mask.any(axis=1)
    runs = []
    y = 0
    n = len(rows)
    while y < n:
        if rows[y]:
            y0 = y
            while y < n and rows[y]:
                y += 1
            runs.append([y0, y])
        y += 1
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= min_gap:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    # ignore specks (a caret, a stray dot) shorter than 12 px
    return [r for r in merged if r[1] - r[0] >= 12]


def cmd_cards(key="A", mp4=None):
    tl = timeline(key)
    probes = []
    for s in tl["sections"]:
        for c in s["cards"]:
            ground = c.get("ground", s["ground"])
            t = s["start"] + c["last_visible"] + min(1.0, c["hold"] / 2)
            probes.append((s, c, ground, t))
    times = [p[3] for p in probes]
    if mp4:
        frames = mp4_frames(mp4, times, TMP / f"cards-mp4-{key}")
    else:
        frames = snapshot(times, TMP / "cards")
    W, H = (1080, 1080) if key == "square" else (1920, 1080)
    mx, my = round(W * 0.05), round(H * 0.05)
    safe = (mx, my, W - mx, H - my)
    results = []
    for (s, c, ground, t), (_, path) in zip(probes, frames):
        im = Image.open(path)
        m = text_mask(im, ground)
        if c.get("gourd"):
            m[:, 1380:] = False  # the drawing is not text
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            results.append(dict(id=c["id"], t=round(t, 3), ok=False, error="no text pixels found"))
            continue
        box = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        inside = box[0] >= safe[0] and box[1] >= safe[1] and box[2] <= safe[2] and box[3] <= safe[3]
        ln = lines_in(m)
        expected_paras = len([p for i, p in enumerate(c["parts"]) if i == 0 or p.get("block")])
        results.append(dict(id=c["id"], section=s["sid"], t=round(t, 3), box=box, inside_safe=inside,
                            rendered_lines=len(ln), predicted_lines=c["lines"], ok=inside and len(ln) <= 2,
                            safe=list(safe), source=str(mp4) if mp4 else "snapshot", frame=str(path)))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"cards_{key}.json").write_text(json.dumps(results, indent=1))
    bad = [r for r in results if not r["ok"]]
    print(f"cards: {len(results)} measured; {len(bad)} failing")
    for r in results:
        flag = "OK " if r["ok"] else "BAD"
        print(f"  {flag} {r['id']:18s} t={r['t']:8.2f} lines {r.get('rendered_lines')} (pred {r.get('predicted_lines')}) "
              f"box {r.get('box')}")


if __name__ == "__main__":
    if sys.argv[1] == "sheet":
        cmd_sheet(sys.argv[2])
    elif sys.argv[1] == "cards":
        cmd_cards(*(sys.argv[2:4] or ["A"]))
    else:
        raise SystemExit(__doc__)
