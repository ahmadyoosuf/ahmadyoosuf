# QC_LOG.md: scene-by-scene inspection (Workflow step 4)

Every section was inspected the same way. I made a 1 fps contact sheet (`<sid>_sheet.jpg`)
and three full-resolution keyframes (`<sid>_key_*.png`) from `npx hyperframes snapshot`,
which is the renderer's own seek path. I then checked every card at mid-hold by pixel
analysis (`cards_A.json`): the measured text box against the 5% safe area and the number
of rendered lines. Defects were fixed before moving on, and the affected frames were
re-captured.

| Section | Sheet | Finding | Fix | Re-checked |
|---|---|---|---|---|
| global (lint) | — | `multiple_root_compositions`: alternate roots (cold opens, animatic) in the project root could double the audio | Moved each alternate root into its own project under `film/variants/*`, which symlink `assets/` and `compositions/` | lint: 0 errors |
| global (lint) | — | `composition_heavy_overlay_count_high`: every word carried `filter: blur()`. The CLI reports that about 40 of these make captures go solid black for half the render | Ink reveal rebuilt as opacity plus a fading `text-shadow` halo; no CSS filters on text | lint: warning gone; close-up `ink/strip.png` |
| s0a | `s0a_sheet.jpg` | The typed letter line did not wrap. It ran off the right edge, because the space spans had `white-space: pre` | Removed the rule, so spaces are break opportunities again | key at 5.0 s: 2 lines, inside the safe area |
| s0a | `s0a_sheet.jpg` | Caret follows the keys; the full line is visible at 2.83 s; blinks at 2 Hz during the hold | — | `crop_typing.png` |
| s1 | `s1_sheet.jpg` | Balanced wrapping started a second sentence at the end of line one ("…grade. He / owned…"), and it then revealed awkwardly after the pause | New rule: if every sentence fits on one line, each starts its own line (still at most two) | `cards_A.json` |
| s2 | `s2_sheet.jpg` | Typed dates on paper read as too clean | Seeded per-key strike density (0.80–1.00) plus ±0.6 px baseline jitter | `s2_date_crop.png` |
| s3 | `s3_sheet.jpg` | The accent phrase "half an hour" broke across lines | Accent phrases are joined with no-break spaces, and the wrap planner treats each as one token | key 162.6 s |
| s3 | `s3_sheet.jpg` | The Discord quote ran its two sentences together | Split into two parts, so each sentence starts its own line, revealed one after the other | key 162.6 s |
| s4 | `s4_sheet.jpg` | The gourd read as a teardrop: no stem, no plant | Redrawn as a bottle gourd (upper bulb, waist, lower bulb) with stem, leaf, tendril, contour and hatching, plus a thinner second pen pass; ends 1.6 s before the cut so it holds still, never becoming food | `gourd/frame-03-at-255.6s.png` |
| s4 | `s4_sheet.jpg` | Round line caps on undrawn strokes showed as dots above the stem | Each stroke is hidden until its own start time | `gourd2/crop_*.png` |
| s4 | `s4_sheet.jpg` | The Tamil first glyph overhung the safe margin by 2 px (x = 94) | Tamil indented 0.06 em | `cards_A.json` (x ≥ 96) |
| s5–s7 | `s5_sheet.jpg`, `s6_sheet.jpg`, `s7_sheet.jpg` | Paper→night dissolve, domain cards, accent on "cooking" and "They say it.", paper-only ask, end card, credits, dedication, fade to black, all as designed | — | — |
| delivery | `cards_A.json` (measured on `77minutes_1080p.mp4`) | The leftmost ink on the gourd card was still at x = 94. It is the foot of the italic "A" in "A gourd drawn on paper…" (HarfBuzz: 1.98 px left of its origin), not the Tamil, and the earlier re-check passed it only because the margin test allowed 2 px of slack | Any paragraph whose first glyph inks more than 0.5 px left of its origin is padded by the measured overhang, rounded up, plus 1 px (here 3 px). The margin test is now strict (no slack). The film was re-rendered | `cards_A.json` on the re-rendered MP4 |
| delivery (sound) | section loudness of `mix_A.wav` | Section 1 (the library, 55 s) measured −41.5 LUFS and the room tone −53 LUFS, 25 LU under the music sections: dead air on a laptop, and the scripted two seconds of silence could not be felt | Room tone +7 dB, distant sea +8 dB; film re-mastered to −16 LUFS (D046) | Section 1 −33.6 LUFS, room tone −46 LUFS |
| delivery (sound) | own-loudness master of the opens and the square | Normalising the excerpts to −16 LUFS on their own: the limiter ate the gain (square +16 dB → −22.3 LUFS, about 12 dB of limiting on every strike, audible room-tone hiss) | Reverted: the excerpts keep the film's gain (D043, D046) | QA.md |
| delivery (picture) | palette check on `77minutes_1080p.mp4` | Full-resolution frames put accent-text edges up to 44 RGB units off the palette segments, because 4:2:0 chroma subsampling smears colour across 2×2 blocks | Palette measured on 2×2 block means (the video's chroma resolution); flat-colour accuracy checked separately: accent decodes as (200,143,47) against (200,144,46) | `qa_evidence.json` |

Sheets were captured on the timeline as it stood when each section was inspected. The
final `cards_A.json` is re-run on the final build (see QA.md).
