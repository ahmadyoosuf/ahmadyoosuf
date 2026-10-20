# STANDARD.md: what the HeyGen launch films actually do

Source: `heygen-com/hyperframes-launches` (cloned 2026-10-20, LFS skipped). I read every
`STORYBOARD.md` (cloud-render, claude-design-send, codex-five-hour-limit-replica, figma,
hyperframes-launch, inspector, sfx-music, timeline, website-to-hyperframes), the
variables-launch HTML boards (`storyboard.html`, `boards/storyboard.html`,
`STORYBOARD-SCENE-05.html`), frame-md's `HANDOFF.md` (its storyboard zip is an LFS pointer
and was not fetched) and each project's `index.html`.

Timestamps are film time. "SB" means the number comes from the storyboard; "IDX" means it
comes from the built `index.html`, which is what shipped.

---

## The ten decisions

### 1. The first event lands inside two seconds; a caret on black is a valid first frame
- website-to-hyperframes SB Beat 1.0, **0:00–0:01.66**: near-black, one mono caret
  blinking at **2 Hz**, room tone at **−40 dB**. The first musical hit and the first panel
  arrive at **0:01.66**.
- IDX: `vo-a1-01` and its caption both start at **1.66 s**. hyperframes-launch SB Beat 1:
  "Camera is already moving when the video starts. No fade in. No preamble."
- **77 MINUTES:** the first character strikes at 0.25 s (open A) and "77 minutes" is on
  screen before 1.0 s. No logo and no fade-up from black.

### 2. Typing has a measured rate, and the sound bed is chosen to fit that rate
- website-to-hyperframes SB Beat 1.1 (**0:01.66–0:04.16**): "~20 chars/s. Each keystroke
  triggers a faint keyboard-typing SFX". Beat 4.4 (**0:47.00–0:48.50**): the install
  command also types at **20 chars/s**, and "a tiny blinking cursor remains at the end".
- variables-launch Scene 05 (**1.5–3.5 s**): code types at **~40 chars/s**. The tagline
  fades in **0.3 s after** typing completes.
- claude-design IDX `sfx-keys` at **4.5913 s**, duration 3.00, volume 0.20: "110 chars
  over 3.0 s is ~37 cps … discrete ticks would read as a machine gun". Fast runs get a
  continuous bed, not a tick per key.
- **77 MINUTES:** each typed card has a declared rate. Slow runs (dates, ~9 cps) get one
  strike per key. The fast cold-open run (~25 cps) gets a continuous typing bed with
  accented strikes, and the caret stays after the last character.

### 3. Read-time holds are explicit and treated as minimums
- variables-launch board: "**0.3 s** hold without motion is enough to read any single
  line. **Minimum hold, not target.**" Scene 05 headline: **0.0–1.5 s** with "~1 s for
  reading". Scene 03: Line A holds ~0.5 s, Line B ~0.8 s.
- sfx-music SB: "**+0.5 s read hold**" after each terminal reply before it exits (Act 2
  ends **16.9**). claude-design S1d: "Stillness (~0.4 s) as the sentence completes".
- inspector IDX: three-to-five-word text scenes run **1.59–3.0 s** ("Close isn't final."
  **20.07–21.77**; "Change what you SEE." **38.38–40.16**).
- **77 MINUTES:** our hold rule (0.3 s per word + 1.2 s, never under 2.5 s, measured from
  the moment the last character is fully visible) is stricter than every launch.
  `holds.json` stores each card's computed and actual hold, and QA checks both.

### 4. Seams are short and asymmetric: exits use `.in`, entrances use `.out`
- cloud-render IDX: the opener exits over **0.22 s `power2.in`** from **5.80**; the cut is
  at **6.00**; "checks" enters over **0.32 s `power3.out`** at **6.00**.
- inspector IDX: exit **0.33 s `power3.in`**, entry **0.42 s `expo.out`**. The background
  leads the foreground by **0.1 s**.
- sfx-music IDX: every seam's exit starts **0.26 s** before its cut (4.64→4.90,
  10.14→10.40, 18.49→18.75, 25.73→25.99, 28.63→28.89).
- **77 MINUTES:** our only transition, the 8-frame dissolve (**0.333 s** at 24 fps), sits
  in the same 0.22–0.42 s band. The ink reveal on each card is a `power2.out` entrance;
  the dissolve is symmetric (`sine.inOut`) because both sides are still.

### 5. A hard cut is used when both sides of the seam share the same ground
- cloud-render IDX at **12.2, 26.2, 29.8**: "HARD CUT … at the identical full-screen dark
  … seamless, no bg flash".
- claude-design IDX seam 2 at **27.8413**: "match cut … S3's k0 is the same picture";
  seam 4 at **44.3763**: "match cut on a flat cream field (#EDECE2 both sides)".
- sfx-music: cream `#F0EEE6` sits behind every section "so exposed edges stay seamless".
- **77 MINUTES:** same-ground section seams (sections 3→4 and 5→6) are invisible hard
  cuts. Every change of ground (night↔paper) is the 8-frame dissolve. A card leaves its own
  ground by an 8-frame dissolve, except the hard-cut beats listed in DECISIONS D031.
  Section 2 (Nine months) enters and leaves through true black.

### 6. Acceleration comes from shrinking intervals, not faster motion
- figma SB Act 2 zoom ladder (**11.8–14.7 s**): nine cuts with cadence
  **0.8 / 0.5 / 0.4 / 0.3 / 0.2 / 0.15 / 0.12 / 0.1 s**.
- hyperframes-launch IDX flex run (**17.30–32.44**): shots of 1.71, 0.67, 1.20 and 1.21 s,
  then word-locked shots of 0.36, 0.58, 0.93, 0.83, 0.15 and 0.33 s, landing on a 2.22 s
  hold.
- timeline SB spiral (**0:06–0:10**): prompts flash for **0.4–0.6 s** each, "Pace
  accelerates."
- **77 MINUTES:** card holds can't drop below the minimum, so section 4 (Well said)
  accelerates through everything around the cards. Air between cards shrinks from 0.6 s
  to 0. Holds sit at exactly the minimum. Footage shots shorten from 7 s to 4 s. The
  journal line's word-by-word reveal speeds up across the sentence. Section 5 (Well done)
  reverses this, with long captures and extra air.

### 7. Silence and stillness are placed deliberately
- sfx-music SB **0.0–10.4**: "SILENCE (the joke; do not fill)".
- hyperframes-launch SB Beat 5 (**0:20–0:24**): "Held beat — one second of stillness"
  between the two lines, and "Silence under the first line".
- website-to-hyperframes SB Beat 4.5 (**0:48.50–0:50.00**): "The command holds. Nothing
  else moves." Then a hard cut to black at **0:50.00**.
- claude-design S6: "Stillness-before-climax: **0.5 s** hold on 'ready'".
- **77 MINUTES:** silence is part of the structure. The cold open has no music. Section 2
  has ambience only, plus a scripted 2.0 s of true black with the sound dipped. The music
  bed doesn't enter until section 3.

### 8. Sound lands on the frame, so lead-in silence is trimmed off every SFX
- claude-design IDX SFX block: click times are "lifted from the cursor PRESS tweens …
  on the press frame". "Zero-onset" sources were chosen because files with **158 ms** and
  **394 ms** of leading silence "fire **4–9 frames late**".
- timeline SB Act 1 (**0:00–0:04**): a sound **~250 ms** late is the intended joke, so
  250 ms is plainly visible as wrong.
- **77 MINUTES:** every typewriter strike is trimmed to its transient onset. Each strike is
  placed within one frame (≤42 ms) of its character appearing, verified by onset detection
  on the final mix.

### 9. Music is edited so its phrases land on structural moments, and sits well below dialogue
- website-to-hyperframes IDX: "Music trimmed **3 s** from start so its natural drop at
  file-time **15 s** lands at timeline **12 s** (matches new Act 3 start)". The bed runs at
  `data-volume 0.11` (≈ −19 dB) under VO. The SB audio map ducks it to **−20 dB** in Act 1.
- hyperframes-launch SB: the pad is "already playing … no silence-to-sound transition",
  "swells gently during the flex section (**0:24–0:38**)", "drops to near-nothing for the
  comparison beat, resolves on a final chord at close".
- **77 MINUTES:** the bed is offset with `data-media-start` so a phrase begins as
  section 3 opens. It is automated, not tweened: down under the gourd, up at "So, slowly,
  I started cooking", and out on the dedication card.

### 10. Ambient motion never stops mid-shot (no move-stop-move-stop)
- inspector IDX: "Master continuous motion tween … advance linearly across the entire
  timeline. **Never stops, never has zero-velocity boundaries** — this is what kills the
  move-stop-move-stop feel." Between cuts there is a `sine.inOut` drift.
- hyperframes-launch SB Beat 1 (**0:00–0:05**): drift of **2–3° over 5 s**, `power1.inOut`.
- figma IDX: each act's background video is "a single full pass at its own speed (no
  looping, no mid-act restarts)".
- **77 MINUTES:** every footage shot drifts 2–4% on a linear (`ease:"none"`) scale or
  translate tween that spans the whole shot, so motion never stops while a still is on
  screen. Text never moves after it lands.

---

## Also observed (not counted in the ten)

- **Plans drift; builds re-time.** Planned vs. built runtimes: hyperframes-launch 60 s →
  49.77 s, cloud-render ~30 s → 38.0 s, figma ~49 s → 64.05 s, timeline 15–20 s →
  33.53 s, variables ~35 s → 43.6 s, website-to-hyperframes ~61 s → 41.8 s.
  `storyboard-format.md` calls `duration` "advisory". We treat the script's section
  timestamps the same way: as targets, overridden by measured holds, with every
  difference logged in DECISIONS.md.
- **Captions are not duplicated on screen.** website-to-hyperframes IDX: "GIANT on-screen
  phrase; skip caption to avoid duplication". Not applicable here, because 77 MINUTES has
  no narration.
- **End on a hold, then a cut.** website-to-hyperframes: 1.5 s hold then a hard cut to
  black at 0:50.00. sfx-music outro "holds ~1 s". codex replica: final hold of
  9.00–10.13 s.

## What 77 MINUTES must meet (the storyboard is checked against this)

1. First character by 0.3 s; "77 minutes" readable by 1.0 s; full line by 3.0 s (open A).
2. Every typed run declares chars/s, plus a strike bed or per-key strikes to match.
3. Every hold is at or above `max(2.5, 0.3·words + 1.2)` s, computed by script, never by eye.
4. Transitions are cuts or 8-frame dissolves only, timed to the 24 fps frame grid.
5. A ground change is a dissolve; a same-ground seam is a cut; section 2 uses black.
6. Section 4 accelerates through air and shot length; section 5 decelerates.
7. Silences are placed in the storyboard, not left over from the edit.
8. SFX onsets are trimmed, and each one is within one frame of its event.
9. The music phrase is aligned with `data-media-start`, and its level is automated.
10. Footage drift is linear and continuous across the whole shot; type never moves after
    it lands.
