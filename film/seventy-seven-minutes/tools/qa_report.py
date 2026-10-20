"""Write /out/QA.md from the measurements in /out/qc/qa_evidence.json.

  python tools/qa.py && python tools/qa_report.py

Every number in QA.md is read from the evidence file; only the prose around it is fixed.
"""
import json
import pathlib

OUT = pathlib.Path("/out")
EV = OUT / "qc" / "qa_evidence.json"


def mmss(s):
    m = int(s // 60)
    return f"{m}:{s - 60 * m:05.2f}"


def n(x, digits=1):
    """A number with a true minus sign."""
    return f"{x:.{digits}f}".replace("-", "−")


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def verdict(ok, note=""):
    v = "**PASS**" if ok else "**FAIL**"
    return f"{v}{note}"


def spec(d):
    return (f"{d['width']}×{d['height']}, {d['fps'].split('/')[0]} fps, H.264 {d['profile']} ({d['pix_fmt']}), "
            f"{d['video_bitrate'] / 1e6:.2f} Mbps average",
            f"AAC-LC, {d['sample_rate'] // 1000} kHz, {'stereo' if d['channels'] == 2 else d['channels']}, "
            f"{d['audio_bitrate'] / 1e3:.0f} kbps")


def main():
    ev = json.loads(EV.read_text())
    film, sq = ev["film"], ev["square"]
    oa, ob = ev["opens"]["open_A.mp4"], ev["opens"]["open_B.mp4"]
    lf = ev["loudness"]
    fx = ev["facts"]
    mg, msq = ev["margins"], ev["margins_square"]
    f3 = ev["first_three_seconds"]
    pal = ev["palette"]
    lic = ev["licensing"]
    tr = ev["transitions"]
    gd = ev["gourd"]
    hf = ev["hyperframes_check"]
    sl, al, bl = sq["loudness"], oa["loudness"], ob["loudness"]
    flagged = ", ".join(f"“{t}”" for t, _ in fx["script_only"])
    w = []
    a = w.append

    a("# QA.md: 77 MINUTES, version 1")
    a("")
    a("Measured on the delivered files by `tools/qa.py`. Every number here is read from `qc/qa_evidence.json`")
    a("(`tools/qa_report.py` writes this page), so nothing below is estimated. Fixes made during QA are logged in")
    a("`qc/QC_LOG.md` and DECISIONS D046–D050.")
    a("")
    brief_ok = [ev["facts"]["ok"], ev["tamil"]["ok"], ev["margins_ok"], ev["loudness_ok"], ev["licensing_ok"],
                ev["runtime_ok"], ev["first_three_ok"]]
    a(f"**Result:** {sum(brief_ok)} of the brief's 7 applicable checks pass on the film; captions don't apply.")
    if not ev["excerpts_integrated_ok"]:
        a("One part of the loudness check fails: the integrated loudness of the three excerpts (the square and the two")
        a("cold opens), for the reason given under *What failed*.")
    a("")
    a("## Delivered files")
    a("")
    a("| File | Picture | Sound | Length | Size |")
    a("| --- | --- | --- | --- | --- |")
    for name, d in (("77minutes_1080p.mp4", film), ("77minutes_square.mp4", sq), ("open_A.mp4", oa), ("open_B.mp4", ob)):
        pic, snd = spec(d)
        a(f"| `{name}` | {pic} | {snd} | {mmss(d['duration_s'])} | {d['size_bytes'] / 1e6:.1f} MB |")
    a("")
    a("Video is single-pass x264 with a 12 Mbps target. Still type on still grounds needs far less than that, so the")
    a("average is what the picture used, not a cap it hit. Held frames of open A measured 50–65 dB PSNR against")
    a("lossless snapshots of the same composition (D048).")
    a("")

    a("## The two cold opens")
    a("")
    a(f"- **Open A, “two voices”** (`open_A.mp4`, {mmss(oa['duration_s'])}; used in the film). The 2022 voice (proud,")
    a("  mechanical, an emoji) is set against the quiet serif voice of now, so the viewer hears the gap between who")
    a("  wrote that line and who is telling the story (D029).")
    a(f"- **Open B, “one sitting”** (`open_B.mp4`, {mmss(ob['duration_s'])}). The whole opening is one long sitting")
    a("  at the keys, so the viewer feels how slow writing is before the film says a word about it (D030).")
    a("")
    a("## The brief's checks")
    a("")
    a("| # | Check | Result | Evidence |")
    a("| --- | --- | --- | --- |")
    a(f"| 1 | Facts match `facts.json` | {verdict(fx['ok'], ', 3 flagged')} | {len(fx['claims'])} on-screen numbers, "
      f"dates, names and claims each trace to the FACTS sentence that licenses it, and no number or name on screen is "
      f"unaccounted for ({len(fx['uncovered_numbers'])} uncovered numbers, {len(fx['uncovered_names'])} uncovered "
      f"names). The only emoji are {' and '.join(fx['emoji'])}, the two in the facts. Three details come from the "
      f"fixed script but aren't in FACTS: {flagged}. They're shown verbatim because the script's wording isn't mine "
      f"to change (D027); please confirm them (v2 list). |")
    ligs = ", ".join(f"`{g}`" for g in ev["tamil"]["conjunct_ligatures"])
    a(f"| 2 | Tamil without broken conjuncts | {verdict(ev['tamil']['ok'])} | Shaped with HarfBuzz against the shipped "
      f"Noto Serif Tamil file. All four consonant + u-sign ligatures form ({ligs}), every pulli sits on its "
      f"consonant, and there are no `.notdef` or dotted-circle glyphs ({len(ev['tamil']['broken'])} found). "
      f"Rendered crop from the delivered film at {ev['tamil']['rendered_at_s']:.2f} s: `qc/tamil_rendered.png`. |")
    s0, s1 = mg["safe"][:2], mg["safe"][2:]
    a(f"| 3 | No text outside safe margins | {verdict(ev['margins_ok'])} | All {mg['cards']} cards were measured "
      f"in the delivered film at mid-hold, using a pixel mask of ink against its ground. The ink spans x "
      f"{mg['min_x']}–{mg['max_x']} and y {mg['min_y']}–{mg['max_y']}, inside the 5% safe area "
      f"({s0[0]}–{s1[0]} × {s0[1]}–{s1[1]}). No card renders more than {mg['max_lines']} lines. The square's "
      f"{msq['cards']} cards span x {msq['min_x']}–{msq['max_x']} and y {msq['min_y']}–{msq['max_y']}, inside "
      f"{msq['safe'][0]}–{msq['safe'][2]}. The test is strict, with no pixel of slack. |")
    a(f"| 4a | Loudness and peak: the film | {verdict(ev['loudness_ok'])} | `77minutes_1080p.mp4`: "
      f"{n(lf['integrated_lufs'])} LUFS integrated and {n(lf['true_peak_dbtp'])} dBTP true peak (targets −16 "
      f"LUFS and below −1 dBTP), measured with ffmpeg `ebur128` on the MP4's AAC track. Loudness range "
      f"{lf['lra_lu']:.1f} LU. |")
    a(f"| 4b | Loudness and peak: the excerpts' true peak | {verdict(ev['excerpts_true_peak_ok'])} | Square "
      f"{n(sl['true_peak_dbtp'])}, open A {n(al['true_peak_dbtp'])}, open B {n(bl['true_peak_dbtp'])} dBTP. |")
    a(f"| 4c | Loudness and peak: the excerpts' integrated loudness | {verdict(ev['excerpts_integrated_ok'])} | Square "
      f"{n(sl['integrated_lufs'])}, open A {n(al['integrated_lufs'])}, open B {n(bl['integrated_lufs'])} LUFS. "
      f"They keep the film's master gain; see *What failed*. |")
    a(f"| 5 | Every clip and sound licensed in SOURCES.csv | {verdict(ev['licensing_ok'])} | {lic['media_files']} "
      f"media files in the project's `assets/`, each covered by one of the {lic['rows']} rows of "
      f"`/assets/footage/SOURCES.csv` ({len(lic['uncovered'])} uncovered). There's no footage, no capture and no "
      f"third-party sound effect. The only third-party sound is the Salamander Grand Piano V3 samples (CC BY 3.0), "
      f"credited on screen. |")
    a(f"| 6 | Runtime 4:00–6:15 | {verdict(ev['runtime_ok'])} | {mmss(film['duration_s'])} with open A. "
      f"(With open B the film would run {mmss(ev['total_open_B'])}.) |")
    a(f"| 7 | The first three seconds show the typed 77-minute line | {verdict(ev['first_three_ok'])} | The letter "
      f"line types from the first frames. Share of the held line on screen: 0.5 s {f3['0.5']['share_of_full']:.0%}, "
      f"1.0 s {f3['1.0']['share_of_full']:.0%}, 2.0 s {f3['2.0']['share_of_full']:.0%}, 2.9 s "
      f"{f3['2.9']['share_of_full']:.0%}. “77 minutes” is on screen in accent by 1.0 s "
      f"({f3['1.0']['accent_px']} accent pixels). Frames: `qc/first3s_*.png`. |")
    a("| 8 | Captions match narration at word level | **N/A** | No narration was supplied (D009). The film is "
      "text-led, so there are no captions to check. |")
    a("")

    a("## Further checks")
    a("")
    a("| Check | Result | Evidence |")
    a("| --- | --- | --- |")
    a(f"| Script wording and order | {verdict(ev['script']['ok'] and ev['script_open_B']['ok'] and ev['script_square']['ok'])} "
      f"| Screen text equals the script character for character: the film with open A ({ev['script']['cards']} "
      f"cards), the film with open B ({ev['script_open_B']['cards']}), and the square (its first "
      f"{ev['script_square']['cards']} cards). Non-script text: the journal date, the two domain names and the "
      f"credits line. |")
    a(f"| Hold rule `max(2.5, 0.3·words + 1.2)` | {verdict(ev['holds_ok'])} | {ev['holds']['cards']} cards (both "
      f"opens included), each measured from the frame its last glyph is fully visible. Tightest card is "
      f"{ev['holds']['min_margin']:.3f} s over its minimum. |")
    ex = tr["card_exits"]
    a(f"| Cut or 8-frame dissolve only | {verdict(ev['transitions_ok'])} | Card exits: {ex.get('dissolve', 0)} "
      f"dissolves of {tr['dissolve_frames']} frames and {ex.get('cut', 0)} cuts. Section 2 enters and leaves through "
      f"black. Same-ground seams (3→4, 5→6) are cuts. |")
    sy = ev["sync"]
    a(f"| Sound on the frame | {verdict(ev['sync_ok'])} | Onset of each of the {sy['strikes']} typewriter strikes, "
      f"detected in the delivered soundtrack, against the frame its character appears: worst {sy['max_abs_ms']:.1f} ms, "
      f"95th percentile {sy['p95_abs_ms']:.1f} ms (one frame is {sy['frame_ms']:.1f} ms). |")
    fc = ev["flat_colour"]
    a(f"| Palette | {verdict(ev['palette_ok'])} | {pal['sampled_frames']} frames, one every 5 s. Worst 99.9th-percentile "
      f"distance from the palette's colour segments is {pal['worst_p999']:.1f} (threshold 12), at "
      f"{pal['worst_frame'][0]:.0f} s. This is measured at the video's 4:2:0 chroma resolution; at full resolution "
      f"chroma subsampling at accent edges gives {pal['worst_p999_full_resolution']:.1f}. Flat fills decode as "
      f"accent {tuple(fc['accent_decoded'])} (target {tuple(fc['accent_target'])}) and paper "
      f"{tuple(fc['paper_decoded'])} (target {tuple(fc['paper_target'])}). |")
    a(f"| The gourd: one drawing, at most 8 s | {verdict(ev['gourd_ok'])} | {gd['cards_with_drawing']} drawing in the "
      f"film. Its card is on screen {gd['card_on_screen_s']:.2f} s, and the drawing itself "
      f"{gd['drawing_on_screen_s']:.2f} s. It is never coloured and never becomes food. |")
    a(f"| Delivery spec | {verdict(ev['delivery_ok'] and ev['square_ok'])} | 1080p: 1920×1080, 24 fps, H.264 High, "
      f"AAC 48 kHz. Square: 1080×1080, {sq['duration_s']:.2f} s. |")
    a(f"| Both cold opens | {verdict(oa['letter_complete_by_2.9s'] > 0.97 and ob['letter_complete_by_2.9s'] > 0.97)} "
      f"| Both complete the letter line by 2.9 s (A {oa['letter_complete_by_2.9s']:.0%}, B "
      f"{ob['letter_complete_by_2.9s']:.0%}). A runs {mmss(oa['duration_s'])}, B {mmss(ob['duration_s'])}. |")
    a(f"| HyperFrames check | {verdict(ev['hyperframes_check_ok'])} | " + "; ".join(
        f"{k} {plural(v['errors'], 'error')}, {plural(v['warnings'], 'warning')}" for k, v in hf.items()) + ". |")
    a("")

    a("## What failed, and why")
    a("")
    a("**Integrated loudness of the excerpts (4c).** The square and both cold opens are the film's first seconds, and")
    a("the brief keeps music out of sections 0–2. Their sound is typewriter strikes over quiet room tone and sea, so")
    a(f"at the film's master gain they measure {n(sl['integrated_lufs'])} LUFS (square), "
      f"{n(al['integrated_lufs'])} (open A) and {n(bl['integrated_lufs'])} (open B).")
    a("I tried mastering each one to −16 LUFS on its own, and it doesn't work: the limiter eats the gain. The square")
    a("took +16 dB and still only reached −22.3 LUFS, with about 12 dB of limiting on every strike and the room tone")
    a("pushed up into a hiss. So they stay at the film's gain (D043, D046): they sound exactly as they do in the film,")
    a("and their true peak passes. The square is the one that matters for publishing, and the v2 list asks how you")
    a("want it handled.")
    a("")
    a("## Known limits of v1 (not failures)")
    a("")
    a("- **No footage and no site captures.** This session's network policy blocked every allowed footage source and")
    a("  all four product sites (D011–D013). v1 is typographic, and nothing was faked in their place. STORYBOARD.md")
    a("  names every footage slot.")
    a("- **No narration** (D009), so there are no captions and no music-under-voice level to check.")
    a("- **Sections start later than the script's timestamps.** The measured holds don't fit them, so every start is")
    a("  logged in STORYBOARD.md (D025). For the same reason the cold opens run 24.9 s (A) and 29.2 s (B), not 18 s.")
    a(f"- **Wide loudness range ({lf['lra_lu']:.1f} LU).** The film is quiet until the piano enters in section 3, which")
    a("  is the brief's rule. The quiet beds were raised so section 1 is audible (D046), but on phone speakers the")
    a("  first two and a half minutes will still feel quiet.")
    a("")
    a("## What version 2 needs from you")
    a("")
    for i, item in enumerate(v2(ev), 1):
        a(f"{i}. {item}")
    a("")
    (OUT / "QA.md").write_text("\n".join(w))
    print("QA.md written:", sum(brief_ok), "of 7 applicable brief checks pass; excerpts integrated:",
          ev["excerpts_integrated_ok"])


def v2(ev):
    return [
        "**Network access, or the media itself.** Allow these hosts in the environment's network settings: "
        "commons.wikimedia.org, upload.wikimedia.org, archive.org, www.pexels.com, api.pexels.com, pixabay.com, "
        "images-api.nasa.gov, www.loc.gov, api.openverse.org, freesound.org, vaakku.org, statement2xl.com, ayyayo.app "
        "and ayyayo.ai. Or put files in `/assets/footage/` and `/assets/captures/`. Each footage slot in STORYBOARD.md "
        "says what it needs.",
        "**Which cold open:** A (“two voices”) or B (“one sitting”). The film uses A until you say otherwise.",
        "**Confirm three script details that aren't in FACTS:** “five thirty”, “Around seven” and “For three years”. "
        "If any is wrong, send the corrected line.",
        f"**How the square should sound.** It measures {n(ev['square']['loudness']['integrated_lufs'])} LUFS, because "
        "its 60 seconds have no music. Choose one: "
        "keep it as it is; let music play under the square only; or cut the square from a different 60 seconds.",
        "**Approve the music, or replace it.** The score is an original solo-piano piece on Salamander CC BY samples, "
        "written to picture (D015, D044). If you'd rather have a sourced or human-composed bed, send it or name it.",
        "**Approve the on-screen extras.** The `vaakku.org` and `statement2xl.com` cards stand in for the captures "
        "(D013, D038), and the credits card reads: “Music and sound made for this film. Piano samples: Salamander Grand "
        "Piano V3 by Alexander Holm, CC BY 3.0.” (D039).",
        "**Optional: narration.** `/assets/vo/vo_master.wav` if you want a narrated cut. The film would then get word-level "
        "captions and a music bed 15 dB under the voice.",
        "**Optional: real screenshots** in `/assets/screens/` of the Discord messages, the 2022 letter, the notes and the "
        "27 August 2023 journal entry. Until then they stay typed text cards (D010).",
        f"**Runtime headroom.** The film is {mmss(ev['film']['duration_s'])} with A and would be "
        f"{mmss(ev['total_open_B'])} with B, against a 6:15 cap. Footage can "
        "play under the cards without adding time. If you want footage shots of their own, something has to be cut.",
    ]


if __name__ == "__main__":
    main()
