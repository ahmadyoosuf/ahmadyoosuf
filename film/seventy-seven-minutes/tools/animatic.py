"""Timing animatic: plain cards at the exact times of the real cut.

Writes variants/animatic/index.html (one flat composition; no reveals, no textures) and a
tick track (high tick = card on, low tick = hold starts, i.e. last glyph visible) so the
rhythm can be judged by ear.

  python tools/animatic.py               -> variants/animatic + assets/audio/animatic_ticks.wav
  python tools/animatic.py burn RAW.mp4  -> /out/animatic.mp4: timecode burned in, the film mix under the ticks
"""
import html
import pathlib
import subprocess
import sys
import wave

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "timeline"))

import build as B  # noqa: E402


def main():
    placed, total, _ = B.assemble("A", B.WIDE)
    clips = []
    ticks = []
    for pl in placed:
        g0 = pl["start"]
        for c in pl["cards"]:
            a, b = g0 + c["start"], g0 + c["end"]
            text = " ".join(p["text"] for p in c["parts"])
            label = (f"{pl['sid']} · {c['id']} · on {B.fmt(a)} · "
                     f"hold {c['hold']:.2f}s (min {c['hold_min']:.2f}) · {c['exit']}")
            bg = "#E9E4D8" if c.get("ground", pl["sec"]["ground"]) == "paper" else "#141413"
            fg = "#141413" if bg == "#E9E4D8" else "#EDEDED"
            clips.append(
                f'<div id="an-{c["id"]}" class="clip an" data-start="{a:.4f}" data-duration="{b - a:.4f}" '
                f'data-track-index="1" style="background:{bg};color:{fg}">'
                f'<p class="t">{html.escape(text)}</p><p class="l">{html.escape(label)}</p></div>')
            ticks.append((a, 1400.0))
            ticks.append((g0 + c["last_visible"], 700.0))
            if c.get("black"):
                ba, bb = c["black"]
                clips.append(f'<div id="an-{c["id"]}-black" class="clip an" data-start="{g0 + ba:.4f}" '
                             f'data-duration="{bb - ba:.4f}" data-track-index="2" style="background:#000;color:#666">'
                             f'<p class="l">two seconds of black</p></div>')
        clips.append(f'<div id="an-{pl["sid"]}-lab" class="clip sec" data-start="{pl["start"]:.4f}" '
                     f'data-duration="{pl["dur"]:.4f}" data-track-index="3">§ {placed.index(pl)} {html.escape(pl["sec"]["name"])}</div>')
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>77 MINUTES · timing animatic</title>
<script src="assets/vendor/gsap.min.js"></script>
<style>
@font-face {{ font-family: "Fraunces"; src: url("assets/fonts/fraunces-latin-full-normal.woff2") format("woff2"); font-weight: 100 900; font-display: block; }}
@font-face {{ font-family: "JetBrains Mono"; src: url("assets/fonts/jetbrains-mono-latin-wght-normal.woff2") format("woff2"); font-weight: 100 800; font-display: block; }}
@font-face {{ font-family: "Noto Serif Tamil"; src: url("assets/fonts/noto-serif-tamil-tamil-500-normal.woff2") format("woff2"); font-weight: 500; font-display: block; }}
@font-face {{ font-family: "Noto Emoji"; src: url("assets/fonts/noto-emoji-9-400-normal.woff2") format("woff2"); font-weight: 400; font-display: block; unicode-range: U+1F605, U+1F622; }}
html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
.an {{ position: absolute; inset: 0; }}
.t {{ position: absolute; left: 96px; right: 96px; top: 380px; margin: 0; font: 400 56px/1.25 "Fraunces", "Noto Serif Tamil", "Noto Emoji", serif; }}
.l {{ position: absolute; left: 96px; bottom: 70px; margin: 0; font: 400 24px/1 "JetBrains Mono", monospace; opacity: .55; }}
.sec {{ position: absolute; left: 96px; top: 70px; font: 400 24px/1 "JetBrains Mono", monospace; color: #8a8a8a; z-index: 5; }}
</style>
</head>
<body>
<div id="root" data-composition-id="animatic" data-start="0" data-width="1920" data-height="1080" data-fps="24" data-duration="{total:.4f}">
{chr(10).join(clips)}
<audio id="animatic-ticks" src="assets/audio/animatic_ticks.wav" data-start="0" data-duration="{total:.4f}" data-track-index="10" data-volume="1"></audio>
</div>
<script>
window.__timelines["animatic"] = gsap.timeline({{ paused: true }});
</script>
</body>
</html>
"""
    vdir = B.variant_dir("animatic")
    (vdir / "index.html").write_text(doc)
    sr = 48000
    n = int(total * sr) + sr
    y = np.zeros(n)
    for t, f in ticks:
        i = int(t * sr)
        k = np.arange(int(0.035 * sr))
        y[i:i + len(k)] += 0.25 * np.sin(2 * np.pi * f * k / sr) * np.exp(-k / (0.008 * sr))
    y = np.clip(y, -1, 1)
    out = ROOT / "assets" / "audio"
    out.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out / "animatic_ticks.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((y * 32767).astype("<i2").tobytes())
    print("animatic:", len(clips), "clips;", f"{total:.2f}s")


def burn(raw):
    font = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
    graph = (f"[0:v]drawtext=fontfile={font}:timecode='00\\:00\\:00\\:00':rate=24:fontsize=30:"
             "fontcolor=0xEDEDED@0.9:box=1:boxcolor=0x000000@0.6:boxborderw=10:x=w-tw-96:y=64[v];[1:a]volume=0.6[m];"
             "[0:a][m]amix=inputs=2:normalize=0:duration=first[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-i", str(ROOT / "assets" / "audio" / "mix_A.wav"),
                    "-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "/out/animatic.mp4"], check=True)
    print("animatic: /out/animatic.mp4")


if __name__ == "__main__":
    if sys.argv[1:2] == ["burn"]:
        burn(sys.argv[2])
    else:
        main()
