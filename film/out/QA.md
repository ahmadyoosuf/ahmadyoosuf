# QA.md: 77 MINUTES, version 1

Measured on the delivered files by `tools/qa.py`. Every number here is read from `qc/qa_evidence.json`
(`tools/qa_report.py` writes this page), so nothing below is estimated. Fixes made during QA are logged in
`qc/QC_LOG.md` and DECISIONS D046–D050.

**Result:** 7 of the brief's 7 applicable checks pass on the film; captions don't apply.
One part of the loudness check fails: the integrated loudness of the three excerpts (the square and the two
cold opens), for the reason given under *What failed*.

## Delivered files

| File | Picture | Sound | Length | Size |
| --- | --- | --- | --- | --- |
| `77minutes_1080p.mp4` | 1920×1080, 24 fps, H.264 High (yuv420p), 1.34 Mbps average | AAC-LC, 48 kHz, stereo, 252 kbps | 6:10.58 | 73.9 MB |
| `77minutes_square.mp4` | 1080×1080, 24 fps, H.264 High (yuv420p), 0.73 Mbps average | AAC-LC, 48 kHz, stereo, 246 kbps | 1:00.00 | 7.4 MB |
| `open_A.mp4` | 1920×1080, 24 fps, H.264 High (yuv420p), 0.27 Mbps average | AAC-LC, 48 kHz, stereo, 244 kbps | 0:24.88 | 1.6 MB |
| `open_B.mp4` | 1920×1080, 24 fps, H.264 High (yuv420p), 0.09 Mbps average | AAC-LC, 48 kHz, stereo, 260 kbps | 0:29.21 | 1.3 MB |

Video is single-pass x264 with a 12 Mbps target. Still type on still grounds needs far less than that, so the
average is what the picture used, not a cap it hit. Held frames of open A measured 50–65 dB PSNR against
lossless snapshots of the same composition (D048).

## The two cold opens

- **Open A, “two voices”** (`open_A.mp4`, 0:24.88; used in the film). The 2022 voice (proud,
  mechanical, an emoji) is set against the quiet serif voice of now, so the viewer hears the gap between who
  wrote that line and who is telling the story (D029).
- **Open B, “one sitting”** (`open_B.mp4`, 0:29.21). The whole opening is one long sitting
  at the keys, so the viewer feels how slow writing is before the film says a word about it (D030).

## The brief's checks

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Facts match `facts.json` | **PASS**, 3 flagged | 40 on-screen numbers, dates, names and claims each trace to the FACTS sentence that licenses it, and no number or name on screen is unaccounted for (0 uncovered numbers, 0 uncovered names). The only emoji are 😅 and 😢, the two in the facts. Three details come from the fixed script but aren't in FACTS: “five thirty”, “Around seven”, “For three years”. They're shown verbatim because the script's wording isn't mine to change (D027); please confirm them (v2 list). |
| 2 | Tamil without broken conjuncts | **PASS** | Shaped with HarfBuzz against the shipped Noto Serif Tamil file. All four consonant + u-sign ligatures form (`ttutamil`, `cutamil`, `kutamil`, `tutamil`), every pulli sits on its consonant, and there are no `.notdef` or dotted-circle glyphs (0 found). Rendered crop from the delivered film at 252.42 s: `qc/tamil_rendered.png`. |
| 3 | No text outside safe margins | **PASS** | All 55 cards were measured in the delivered film at mid-hold, using a pixel mask of ink against its ground. The ink spans x 96–1804 and y 421–603, inside the 5% safe area (96–1824 × 54–1026). No card renders more than 2 lines. The square's 12 cards span x 55–1020 and y 442–584, inside 54–1026. The test is strict, with no pixel of slack. |
| 4a | Loudness and peak: the film | **PASS** | `77minutes_1080p.mp4`: −16.0 LUFS integrated and −2.0 dBTP true peak (targets −16 LUFS and below −1 dBTP), measured with ffmpeg `ebur128` on the MP4's AAC track. Loudness range 21.7 LU. |
| 4b | Loudness and peak: the excerpts' true peak | **PASS** | Square −2.0, open A −1.3, open B −1.9 dBTP. |
| 4c | Loudness and peak: the excerpts' integrated loudness | **FAIL** | Square −28.1, open A −20.2, open B −21.9 LUFS. They keep the film's master gain; see *What failed*. |
| 5 | Every clip and sound licensed in SOURCES.csv | **PASS** | 108 media files in the project's `assets/`, each covered by one of the 16 rows of `/assets/footage/SOURCES.csv` (0 uncovered). There's no footage, no capture and no third-party sound effect. The only third-party sound is the Salamander Grand Piano V3 samples (CC BY 3.0), credited on screen. |
| 6 | Runtime 4:00–6:15 | **PASS** | 6:10.58 with open A. (With open B the film would run 6:14.92.) |
| 7 | The first three seconds show the typed 77-minute line | **PASS** | The letter line types from the first frames. Share of the held line on screen: 0.5 s 11%, 1.0 s 30%, 2.0 s 72%, 2.9 s 100%. “77 minutes” is on screen in accent by 1.0 s (2878 accent pixels). Frames: `qc/first3s_*.png`. |
| 8 | Captions match narration at word level | **N/A** | No narration was supplied (D009). The film is text-led, so there are no captions to check. |

## Further checks

| Check | Result | Evidence |
| --- | --- | --- |
| Script wording and order | **PASS** | Screen text equals the script character for character: the film with open A (55 cards), the film with open B (55), and the square (its first 12 cards). Non-script text: the journal date, the two domain names and the credits line. |
| Hold rule `max(2.5, 0.3·words + 1.2)` | **PASS** | 59 cards (both opens included), each measured from the frame its last glyph is fully visible. Tightest card is 0.017 s over its minimum. |
| Cut or 8-frame dissolve only | **PASS** | Card exits: 48 dissolves of 8 frames and 7 cuts. Section 2 enters and leaves through black. Same-ground seams (3→4, 5→6) are cuts. |
| Sound on the frame | **PASS** | Onset of each of the 131 typewriter strikes, detected in the delivered soundtrack, against the frame its character appears: worst 12.4 ms, 95th percentile 0.4 ms (one frame is 41.7 ms). |
| Palette | **PASS** | 74 frames, one every 5 s. Worst 99.9th-percentile distance from the palette's colour segments is 7.3 (threshold 12), at 6 s. This is measured at the video's 4:2:0 chroma resolution; at full resolution chroma subsampling at accent edges gives 14.9. Flat fills decode as accent (200, 143, 47) (target (200, 144, 46)) and paper (242, 233, 220) (target (242, 235, 221)). |
| The gourd: one drawing, at most 8 s | **PASS** | 1 drawing in the film. Its card is on screen 7.17 s, and the drawing itself 6.85 s. It is never coloured and never becomes food. |
| Delivery spec | **PASS** | 1080p: 1920×1080, 24 fps, H.264 High, AAC 48 kHz. Square: 1080×1080, 60.00 s. |
| Both cold opens | **PASS** | Both complete the letter line by 2.9 s (A 100%, B 100%). A runs 0:24.88, B 0:29.21. |
| HyperFrames check | **PASS** | lint 0 errors, 0 warnings; runtime 0 errors, 0 warnings; layout 0 errors, 0 warnings; motion 0 errors, 0 warnings; contrast 0 errors, 0 warnings. |

## What failed, and why

**Integrated loudness of the excerpts (4c).** The square and both cold opens are the film's first seconds, and
the brief keeps music out of sections 0–2. Their sound is typewriter strikes over quiet room tone and sea, so
at the film's master gain they measure −28.1 LUFS (square), −20.2 (open A) and −21.9 (open B).
I tried mastering each one to −16 LUFS on its own, and it doesn't work: the limiter eats the gain. The square
took +16 dB and still only reached −22.3 LUFS, with about 12 dB of limiting on every strike and the room tone
pushed up into a hiss. So they stay at the film's gain (D043, D046): they sound exactly as they do in the film,
and their true peak passes. The square is the one that matters for publishing, and the v2 list asks how you
want it handled.

## Known limits of v1 (not failures)

- **No footage and no site captures.** This session's network policy blocked every allowed footage source and
  all four product sites (D011–D013). v1 is typographic, and nothing was faked in their place. STORYBOARD.md
  names every footage slot.
- **No narration** (D009), so there are no captions and no music-under-voice level to check.
- **Sections start later than the script's timestamps.** The measured holds don't fit them, so every start is
  logged in STORYBOARD.md (D025). For the same reason the cold opens run 24.9 s (A) and 29.2 s (B), not 18 s.
- **Wide loudness range (21.7 LU).** The film is quiet until the piano enters in section 3, which
  is the brief's rule. The quiet beds were raised so section 1 is audible (D046), but on phone speakers the
  first two and a half minutes will still feel quiet.

## What version 2 needs from you

1. **Network access, or the media itself.** Allow these hosts in the environment's network settings: commons.wikimedia.org, upload.wikimedia.org, archive.org, www.pexels.com, api.pexels.com, pixabay.com, images-api.nasa.gov, www.loc.gov, api.openverse.org, freesound.org, vaakku.org, statement2xl.com, ayyayo.app and ayyayo.ai. Or put files in `/assets/footage/` and `/assets/captures/`. Each footage slot in STORYBOARD.md says what it needs.
2. **Which cold open:** A (“two voices”) or B (“one sitting”). The film uses A until you say otherwise.
3. **Confirm three script details that aren't in FACTS:** “five thirty”, “Around seven” and “For three years”. If any is wrong, send the corrected line.
4. **How the square should sound.** It measures −28.1 LUFS, because its 60 seconds have no music. Choose one: keep it as it is; let music play under the square only; or cut the square from a different 60 seconds.
5. **Approve the music, or replace it.** The score is an original solo-piano piece on Salamander CC BY samples, written to picture (D015, D044). If you'd rather have a sourced or human-composed bed, send it or name it.
6. **Approve the on-screen extras.** The `vaakku.org` and `statement2xl.com` cards stand in for the captures (D013, D038), and the credits card reads: “Music and sound made for this film. Piano samples: Salamander Grand Piano V3 by Alexander Holm, CC BY 3.0.” (D039).
7. **Optional: narration.** `/assets/vo/vo_master.wav` if you want a narrated cut. The film would then get word-level captions and a music bed 15 dB under the voice.
8. **Optional: real screenshots** in `/assets/screens/` of the Discord messages, the 2022 letter, the notes and the 27 August 2023 journal entry. Until then they stay typed text cards (D010).
9. **Runtime headroom.** The film is 6:10.58 with A and would be 6:14.92 with B, against a 6:15 cap. Footage can play under the cards without adding time. If you want footage shots of their own, something has to be cut.
