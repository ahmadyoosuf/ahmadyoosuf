# DECISIONS.md: 77 MINUTES

Every decision is numbered, has a reason, and is appended in the order it was made. "You"
means Ahmad, the person who wrote the brief.

## Setup and process

**D001 Workspace.** The film lives in `film/` inside the `ahmadyoosuf/ahmadyoosuf` repo,
with `/assets → film/assets` and `/out → film/out` symlinked.
*Why:* this keeps the brief's absolute paths working, keeps every file openable in the
Claude app (which only opens files under the working directory), and lets the work be
committed to the session branch. The website is untouched.

**D002 Skills read.** `npx skills add heygen-com/hyperframes --all` installed 21 skills.
Two of the names in the brief no longer exist: `hyperframes-media` was retired into
`media-use` (its `references/meta.md` says "hyperframes-media retired"), and GSAP now lives
in `hyperframes-animation` (`adapters/gsap.md` plus `gsap-timeline-and-labels.md`,
`gsap-easing-and-stagger.md` and `gsap-transforms-and-perf.md`). I read all of these in
full, plus `hyperframes`, `hyperframes-cli` and `hyperframes-core` with their references.
*Why:* the brief asks for these skills by function, so I read the skills that now carry
that function.

**D003 Route: `/general-video`.** *Why:* the router sends pieces clearly longer than 3
minutes to general-video. This is not a product promo (products are one section of eight)
and not a faceless explainer (that route tops out around 90 s).

**D004 No intent interview; BRIEF.md written from your prompt.** *Why:* you said "Do not ask
me questions." Your prompt is a complete brief, so the interview's job is already done.

**D005 Renders proceed without the "final look" approval pause.** The skills say to pause
for approval before rendering, but your instruction "Do not stop until QA.md is written"
outranks that. The Studio preview can still be opened for you; nothing waits on it.

**D006 Telemetry disabled; no `hyperframes feedback` posts.** *Why:* the film covers your
father's death and family history. `feedback` posts to a public channel, so I don't send
anything about this project outward without your say-so.

**D007 Section numbering.** Cold open = section 0, The library = 1, Nine months = 2,
Alone = 3, Well said = 4, Well done = 5, Just say it = 6, The ask = 7.
*Why:* only this numbering makes "section 4 accelerates / section 5 decelerates" match the
script's "Well said. Accelerate." and "Well done. Slow down", and makes "section 2 enters
and leaves through black" plus "longer in section 2" match "Nine months. No music."

## Asset audit (Workflow 1)

**D008 `/assets` did not exist.** I found no `vo_master.wav`, no `screens/`, no
`footage/` and no `music/`. The consequences follow below.

**D009 Text-led film.** No narration was supplied, so every script line becomes a card. No
transcription and no captions (captions apply to narration-led films only). No TTS ever.

**D010 Discord, Keep, Day One and the 2022 letter are shown as typed text cards.**
*Why:* no screenshots were supplied, and the brief forbids fabricating a screenshot or chat
UI.

## Network (this blocked most sourcing)

**D011 The session's network policy denies these hosts** (each returned 403 from the
egress proxy, recorded in its status log): commons.wikimedia.org, upload.wikimedia.org,
archive.org, www.pexels.com, api.pexels.com, pixabay.com, images-api.nasa.gov, www.loc.gov,
api.openverse.org, freesound.org, cdn.jsdelivr.net, vaakku.org, statement2xl.com,
ayyayo.app and ayyayo.ai. All four `npx hyperframes capture` runs failed with
`net::ERR_TUNNEL_CONNECTION_FAILED`. Reachable: the npm and PyPI registries,
fonts.googleapis.com and raw.githubusercontent.com.
*Why this matters:* every footage source on the allow-list, and every product site, is
unreachable from this container. I did not route around the proxy (its rules forbid that).

**D012 No footage in v1, and nothing fabricated in its place.** No AI imagery, no mock
websites, no "stand-in" pictures of a library or a coast. v1 is typographic: ink "night"
grounds, physical paper sheets, typed dates, and the gourd as the single drawn visual.
STORYBOARD.md still names every footage slot (what, where, search terms, required
license), so v2 can drop footage in without re-cutting.

**D013 Product sections without captures.** Each product beat is preceded by a one-line
domain card (`vaakku.org`, `statement2xl.com`, `ayyayo.ai`, `ayyayo.app`), set as text.
*Why:* the script lines never name Vaakku or statement2xl; the captures would have shown
the names. A plain domain card restores the name without faking a UI. In v2 the captures
replace these cards.

**D014 GSAP and fonts are vendored locally.** GSAP 3.14.2 (the version the skills
document) comes from npm into `assets/vendor/`, because jsDelivr is blocked and renders
must not fetch anything at render time anyway. Fonts are the official Google Fonts builds,
taken from npm `@fontsource` packages (OFL-1.1), with the OFL texts in
`assets/fonts/licenses/`.

## Sound and music (sourcing blocked)

**D015 Music: an original solo-piano bed, played on Salamander Grand Piano V3 samples.**
The samples are by Alexander Holm under CC BY 3.0 (explicitly stated in the npm package
`@audio-samples/piano-mp3-velocity*` README, which mirrors archive.org/details/SalamanderGrandPianoV3);
the packaging code is MIT. The composition is written for this film to its exact timing,
contains no drums and no vocals, and is credited in the end credits.
*Why:* Pixabay, Internet Archive and Wikimedia are blocked, so a sourced bed was
impossible. CC BY samples are inside your licence rule ("anything explicitly … CC-BY"), and
composing to picture lets the music land on the film's structure. **v2 can swap in a
sourced or human-composed bed** without changing anything else.

**D016 Sound effects are synthesized in code, not sourced.** Typewriter strikes,
the margin bell, paper, the pen nib for the gourd, wind, distant sea and room tone are
procedural (seeded noise and resonators, written for this film), so their licence is
simply "original, CC0".
*Why:* every SFX source was blocked. I rejected the bundled `media-use` SFX for three
reasons: they're computer-keyboard sounds, not a typewriter; they have no per-file source
page or author (your rule rejects unclear licences); and half the set (whoosh, glitch,
riser) is banned by your prohibitions.

## Visual system

**D017 The three colours are the only designed colours.** Paper `#F2EBDD`, ink
`#1B1A17`, accent `#C8902E`. Two clarifications. **Black** (`#000`) appears only where the
script says black: the cold open, section 2's way in and out, and the two seconds of black.
That is absence of picture, not a fourth colour. **Textures** (paper fibre, the lamp
fall-off on the night ground) are built only from the paper and ink colours at low opacity,
so they're tints within the palette.

**D018 Accent only on dark grounds.** `#C8902E` on paper `#F2EBDD` is about 2.6:1 contrast,
below WCAG's 3:1 for large text, so accent words appear only on night or black grounds.
*Why:* it keeps the highlighted words legible.

**D019 Accent words trace the argument.** "77 minutes" (×2, section 0) → "half an hour"
(section 3) → "well done" (in the 2023 journal line, section 4) → "cooking" (section 5) →
"They say it." (section 6). That is all; nothing else is highlighted.
*Why:* the accent follows the cost of writing until the film says nobody needs to pay it.

**D020 Emoji.** The facts contain two emoji, 😅 (the letter) and 😢 ("Ok😢"), and both are
in your fixed script, so both appear and no others do. They are drawn as monochrome Noto
Emoji glyphs (OFL) in the line's own text colour.
*Why:* a colour emoji would bring yellow and blue into a three-colour film. None of the
three fonts contains emoji glyphs, so Noto Emoji is used for those two code points only
(via `unicode-range`). It is not a fourth text face.

**D021 Fonts in use.** Fraunces (variable: opsz auto, wght 400, SOFT 50, WONK 0) for every
card and quote. Quotes (other people's words, and your own past writing) are Fraunces
*italic*. Noto Serif Tamil 500 for the proverb. JetBrains Mono 400 for dates, the cold-open
letter line and the title.
*Why:* italic separates quoted voices from the narrator without breaking the three-font
rule. WONK 0 keeps Fraunces calm.

**D022 Type sizes and margins.** Cards are 64 px Fraunces, left-aligned at x = 96, with
the measure capped at the 5% safe width (96 to 1824 px). Mono is 60 px; the title and the
end card are 72 px; the proverb's English line and the final small card are 60 px. Text
never extends past 54 px from the top or bottom. Card splits are planned with HarfBuzz
against the shipped font files (`tools/measure.py`) and re-checked in the browser.

**D023 Apostrophes.** Narration cards use typographic ’ and ‘ ’. The two Discord quotes
keep the straight apostrophe exactly as typed ("no i'm busy", "No I'm busy").
*Why:* narration is typeset; the quotes are reproductions of real messages, so their
characters are preserved.

## Timing

**D024 The hold rule, as measured.** A card's hold starts on the frame its last glyph is
fully visible and ends on the first frame of its exit. The minimum is
`max(2.5 s, 0.3 s × words + 1.2 s)`, where words are whitespace-separated tokens across
everything visible on the card (date lines and Tamil included). The builder computes this,
`holds.json` records the computed and actual value for every card, and QA re-checks it.
All times snap to the 24 fps frame grid.

**D025 Script timestamps are targets, not walls.** With measured holds, the cold open alone
can't be shorter than about 21 s: 15.4 s of minimum holds plus typing, reveals and exits. So
sections run longer than the script's 0:18, 1:15 and so on. Every section's actual start is
logged in STORYBOARD.md, and the total is kept inside 4:00–6:15.

**D026 One script line = one card. A line only splits when it can't fit in two lines.**
Multi-sentence lines reveal sentence by sentence on the same card. Lines too long for two
lines at 64 px are split at sentence boundaries into consecutive cards, with wording and
order untouched: the family line (128 characters), the 2023 journal line (159) and the
classrooms/DMs line (131). Both cold opens fit.

**D027 Script-only details.** Three fixed script lines contain details that aren't in
FACTS: "five thirty", "Around seven" and "For three years". The script's wording is not
mine to change, so they appear verbatim. They are flagged in `facts.json`, QA.md and the v2
list.

**D028 Music is silent from 0:00 through the end of section 2; the bed enters at
section 3.** *Why:* "Silent through section 2" reads like "closed through Friday": silent
until and including section 2. That also matches the script's own "No music" in Nine
months. So the music's first appearance is the moment you start building.

## The two cold opens

**D029 Open A, "two voices"** (in the film, 23.9 s). The letter line is typed in JetBrains
Mono at one key per frame (24 keys/s), with two-frame breaths before "77" and before
"Period.". It completes at 2.83 s, then holds with a blinking caret. The narrator's two
cards are soft-inked Fraunces, and the title is struck in mono.
*Intended effect:* the 2022 voice (proud, mechanical, an emoji) is set against the quiet
serif voice of now, so the viewer hears the gap between who wrote that line and who is
telling the story.

**D030 Open B, "one sitting"** (`/out/open_B.mp4`, 28.2 s). Everything in the cold open is
typed on the same black page with a caret and a carriage return between cards. The letter
types as in A, the 2022 line at 21 keys/s, "I was proud of that." at 9 keys/s, and the title
at 4 keys/s in heavy strikes.
*Intended effect:* the whole opening is one long sitting at the keys, so the viewer feels
how slow writing is before the film says a word about it.

## Grammar and typography refinements (from scene inspection)

**D031 Transitions.** A card leaves by an 8-frame dissolve to its bare ground. Exceptions
are hard cuts: "I was proud of that.", the two "busy" replies, the late cards of section 4
(the acceleration), the 1 July cut into the two seconds of black, and the typed cards of
open B. Ground changes are 8-frame dissolves (paper↔night in sections 4/5 and 6/7).
Same-ground section seams (3→4, 5→6) are invisible cuts. Section 2 enters and leaves
through black.
*Why:* this matches STANDARD §4–5, and "Cut or 8-frame dissolve only" holds everywhere.

**D032 The soft ink reveal uses opacity plus a fading text-shadow halo, never CSS
`filter: blur()`.** *Why:* the CLI's lint warns that about 40 blurred elements in one
composition make captures go solid black for half the render.

**D033 One sentence per line when it fits.** If every sentence on a card fits on one line,
each starts its own line (still at most two lines). Otherwise the card is one balanced
paragraph.
*Why:* a sentence revealed after a pause at the end of a line reads as a mistake.

**D034 Accent phrases never break across lines.** They are joined with no-break spaces,
and the wrap planner treats each phrase as one token.

**D035 The Discord quote is staged as two sentences**, each on its own line, revealed in
turn. The wording is unchanged.

**D036 Typed dates on paper show typewriter character.** Strike density varies per key
(0.80–1.00) and there's a ±0.6 px baseline jitter, both seeded and static. The cold-open
letter stays clean because it was an email.

**D037 The gourd** is a bottle gourd (suraikkai): upper bulb, waist, belly, cut stem, leaf,
tendril, contour lines and hatching, drawn as an ink line in 10 strokes over 5.2 s. It then
holds still, uncoloured, for the rest of its card, which is the point: it never becomes
food. It is on screen 6.85 s, inside the 8 s cap.

**D038 Domain cards only for Vaakku and statement2xl.** The ayyayo lines already name
ayyayo, so `ayyayo.ai` and `ayyayo.app` cards were dropped to stay inside 6:15.

**D039 Credits come before the final card.** You called the dedication the "Final small
card", so it is the last thing on screen. The credits card ("Music and sound made for this
film. Piano samples: Salamander Grand Piano V3 by Alexander Holm, CC BY 3.0.") sits between
the end card and the dedication.

## Variants and the square

**D040 Each alternate root is its own project** (`film/variants/open-a`, `open-b`,
`animatic`, `square`), symlinked to the main `assets/` and `compositions/`.
*Why:* lint errors on more than one root composition per project, because the runtime
could treat them as entry points and double the audio.

**D041 The square is a re-split, not a crop.** At 1080 px wide (972 px measure), seven of
the first eleven cards need more than two lines. They are split at sentence boundaries
first, then at the nearest word boundary to the middle (after punctuation, before "(",
never inside an accent phrase). Holds are recomputed. The cut ends on the last complete
card ("My father studied until the third grade.") and fades to black at 60.00 s.

## Sound

**D042 Mastering.** Integrated −16.0 LUFS (BS.1770-4), then a 4×-oversampled look-ahead
true-peak limiter with a −2.0 dBTP ceiling.
*Why:* AAC encoding can lift true peak by about 0.5 dB, and the spec is "below −1 dBTP" in
the delivered MP4. QA measures the MP4 itself.

**D043 The opens and the square use the film's master gain, not their own normalisation.**
Neither contains music (D028), so their integrated loudness is lower than −16 LUFS by
design.
*Why:* this keeps the A/B comparison fair and makes them sound exactly as they do in the
film. Normalising them separately would have pushed the room tone and typewriter up by
about 10 dB.

**D044 Score structure (composed to picture, D015).** The score enters at section 3 on
the descending A–F–D "writing" motif in D minor. In section 4 it accelerates: bars shrink
from 4.0 s to 2.7 s, and the left hand moves from quavers to semiquavers. It breaks off
unresolved on A7 at "There's an old Tamil saying.", and the gourd is drawn under pen sound
alone. Section 5 resolves into slow F-major chords. In section 6 the motif rises (F–A–C–F)
onto "They say it.". Section 7 thins out, holds a chord on the end card, and plays the
descending motif once more, slowly, under the dedication.

**D045 Foley placement.** Two soft knocks under "Around seven, my brother knocked on my
door." The margin bell rings eight keys before the end of each long typed line. A sheet of
paper is laid down whenever a paper ground opens. The room tone ducks to silence for the
two seconds of black.

## Delivery (Workflow 5–7)

**D046 The quiet beds were raised, and the excerpts keep the film's gain.** Measuring the
first master section by section showed section 1 (the library, 55 s) at −41.5 LUFS and
the room tone at −53 LUFS: 25 LU below the music sections. On a laptop that minute
plays as dead air, and the room tone was too low for its drop into the scripted two
seconds of silence to be felt. The room tone is now 7 dB louder and the distant sea 8 dB
louder. I also tried mastering the opens and the square to −16 LUFS on their own, and it
doesn't work. Their sound is typewriter strikes over quiet ambience, so the limiter eats
the gain: the square took +16 dB and still only reached −22.3 LUFS, with about 12 dB of
limiting on every strike and the room tone pushed up into an audible hiss. So D043
stands. The opens and the square keep the film's master gain, sound exactly as they do
in the film, and meet the true-peak limit. Their integrated loudness is below −16 LUFS
because the brief keeps music out of sections 0–2. QA.md reports that as a fail, with
this reason, and the v2 list asks how you want it handled.

**D047 The mastered WAV is muxed onto each render.** HyperFrames renders the picture, and
`tools/mux.py` copies that H.264 stream untouched. It then encodes the mastered WAV once,
as AAC-LC 256 kbps, 48 kHz stereo, trimmed to the picture's exact length.
*Why:* the renderer's own track is AAC 192 kbps from the same WAV. Muxing gives a known,
higher audio bitrate, and lets a sound fix ship without a 15-minute re-render. QA measures
loudness and true peak on the muxed MP4.

**D048 "High bitrate" is a 12 Mbps x264 target, not padding.** Video is H.264 High
profile, yuv420p, 24 fps, single-pass ABR targeting 12 Mbps (1.5× YouTube's 8 Mbps
recommendation for 1080p24). Still type on still grounds needs far less, so the encoder
spends only what the picture needs: open A averages 0.27 Mbps. Held frames measure 50–65
dB PSNR against lossless snapshots of the same composition.
*Why:* the point of "high bitrate" is no visible compression. Forcing a constant 12 Mbps
(CBR with filler data) would only make the files bigger.

**D049 Rendered films stay out of git.** The source, tools and documents are committed
to the session branch. The MP4s and WAVs are delivered to you directly instead, and every
one can be rebuilt with the commands in `seventy-seven-minutes/README.md`.
*Why:* `ahmadyoosuf/ahmadyoosuf` is a public repository, and I shouldn't publish an
unapproved cut of a film about your father. The WAVs also exceed GitHub's 100 MB file
limit. Note that the script is part of the committed source, so the branch itself is
publicly readable.

**D050 STANDARD §9 is met by composing to picture, not by a `data-media-start` offset.**
The score is written against the timeline's own anchors (D044), so its phrases start on
section 3, break off at "There's an old Tamil saying.", resolve under "So, slowly, I
started cooking." and decay under the dedication. No offset is needed. The level automation
is part of the single mastered WAV, so the film carries one audio element.
*Why:* an offset aligns a found track to picture. A track written to the picture is aligned
by construction, and baking the mix into one file keeps the loudness measurable end to end.
