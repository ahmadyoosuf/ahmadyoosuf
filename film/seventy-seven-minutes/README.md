# 77 MINUTES: the HyperFrames project

A text-led personal video essay, built as data. `timeline/script.py` holds every card,
in the script's fixed wording and order. Everything else is generated from it: the
compositions, the cue list the sound is mixed from, the storyboard, the holds table and
the animatic. So the plan, the picture and the sound can't drift apart.

The documents live in `../out/` (also reachable as `/out`): `STANDARD.md`, `facts.json`,
`DECISIONS.md` (every decision and its reason), `STORYBOARD.md`, `holds.json` and `QA.md`.
Asset licences are in `../assets/footage/SOURCES.csv`.

## Layout

| Path | What it is |
| --- | --- |
| `timeline/script.py` | The film as data: sections, cards, parts, accents, reveal modes, pauses |
| `timeline/script_source.txt` | The brief's script, verbatim. QA compares the screen text against it |
| `tools/build.py` | Timing (holds, reveal schedules, transitions) and the HTML for every section |
| `tools/measure.py` | HarfBuzz text measurement and shaping against the shipped font files |
| `tools/textures.py` | The night and paper grounds (procedural, palette colours only) |
| `tools/sfx.py`, `tools/music.py`, `tools/audio.py` | Synthesized foley, the piano score, mixing and mastering |
| `tools/mux.py` | Puts the mastered WAV on each rendered MP4 (AAC-LC 256 kbps, 48 kHz) |
| `tools/storyboard.py`, `tools/animatic.py` | STORYBOARD.md and holds.json, and the plain-card animatic |
| `tools/qc.py`, `tools/qa.py` | Contact sheets, card margin measurement, and the QA evidence |
| `compositions/`, `index.html` | Generated. The film with cold open A |
| `../variants/` | Generated alternate roots: `open-a`, `open-b`, `square`, `animatic` |

## Rebuild from scratch

Python 3.13 with `numpy scipy soundfile pyloudnorm fonttools uharfbuzz Pillow brotli`,
plus Node 22 and ffmpeg 6.

```bash
python tools/textures.py
python tools/build.py && python tools/build.py --square
python tools/audio.py film A          # sets the master gain the excerpts reuse
python tools/audio.py open A && python tools/audio.py open B && python tools/audio.py square
python tools/storyboard.py animated
npx hyperframes check

R="--fps 24 --quality high --video-bitrate 12M"
npx hyperframes render . $R --output /out/77minutes_1080p.mp4
npx hyperframes render ../variants/open-a $R --output /out/open_A.mp4
npx hyperframes render ../variants/open-b $R --output /out/open_B.mp4
npx hyperframes render ../variants/square $R --output /out/77minutes_square.mp4
python tools/mux.py

python tools/animatic.py
npx hyperframes render ../variants/animatic --fps 24 --quality draft --output renders/animatic_raw.mp4
python tools/animatic.py burn renders/animatic_raw.mp4

python tools/qc.py cards A /out/77minutes_1080p.mp4
python tools/qc.py cards square /out/77minutes_square.mp4
python tools/qa.py
```

The WAVs, stems and MP4s are kept out of git (see `../.gitignore`). Every one of them can be
rebuilt with the commands above.
