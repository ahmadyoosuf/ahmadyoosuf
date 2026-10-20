"""Write /out/STORYBOARD.md (HeyGen storyboard format) and /out/holds.json from the
same timeline the compositions are built from, so the plan cannot drift from the cut."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "timeline"))

import build as B  # noqa: E402

OUT = pathlib.Path("/out")

SECTION_SOUND = {
    "s0a": "Room tone only (about −46 LUFS) from frame 0. One typewriter strike per key at 24 keys/s through the letter "
           "line; the margin bell rings as the carriage nears the end of line one; the hold sits in room tone. "
           "The two narration cards are silent. The title is struck key by key (14 keys/s) in heavy strikes.",
    "s0b": "Room tone. Every card is typed: the letter at 24 keys/s, the 2022 line at 21/s, 'I was proud of that.' "
           "at 9/s, the title at 4/s in heavy strikes. A carriage return after each card.",
    "s1": "Room tone and a distant sea, low (the coast; D046). No music (D028). One page turn under the father's "
          "books.",
    "s2": "No music. A paper sheet is laid down as the section opens out of black. Typewriter strikes for every "
          "date (11 keys/s; 7 keys/s for 1 July 2019). Wind enters under 'Cyclone Gaja', peaks under the roof "
          "line and falls away by December. Two soft knocks under 'Around seven'. True silence for the two seconds "
          "of black. Room tone only after.",
    "s3": "The piano enters at the first frame of the section: the film's first music. Sparse single notes in "
          "D minor over room tone.",
    "s4": "The piano quickens into moving quavers as the cards accelerate. The journal is revealed word by word "
          "over it. The piano breaks off under 'There’s an old Tamil saying.', and the gourd is drawn to the sound "
          "of a pen nib on paper alone.",
    "s5": "The piano returns at half the speed, long warm chords, under 'So, slowly, I started cooking.'",
    "s6": "The melody opens upward and resolves under 'They say it.'",
    "s7": "A paper sheet is handled as the section opens. The piano thins to single notes, lands a held chord on "
          "the end card, and the last note decays under the dedication into silence.",
}

SECTION_VISUAL = {
    "s0a": "True black. The letter line in JetBrains Mono 60 px, paper colour, left-aligned at x 96, block centred "
           "at 47 % of frame height, with a 2 Hz caret; ‘77 minutes’ in accent. Narration cards in Fraunces 64 px.",
    "s0b": "True black. Everything typed in JetBrains Mono (60 px; title 72 px) with a caret: one sitting at the keys.",
    "s1": "Night ground: ink with a reading-lamp falloff from the top left and fine grain. Paper-coloured Fraunces "
          "64 px, left-aligned, two lines at most.",
    "s2": "A paper sheet (paper colour, fibres, lamp-lit edge). Ink type. Dates in JetBrains Mono with uneven "
          "typewriter strike density; statements in Fraunces. Enters and leaves through true black.",
    "s3": "Night ground. Quotes from 2022 (Discord) set in Fraunces italic; ‘half an hour’ in accent.",
    "s4": "Night ground, then the paper sheet for the gourd. The journal in Fraunces italic, word by word, "
          "‘well done’ in accent. The gourd: ink line on paper, never coloured, never food.",
    "s5": "Night ground. Domain cards (72 px) stand in for the blocked captures (D013); ‘cooking’ in accent.",
    "s6": "Night ground. ‘They say it.’ in accent.",
    "s7": "Paper only (as scripted). Ink type. End card 72 px; credits and the final small card 60 px.",
}

SECTION_WHY = {
    "s0a": "Opens on 77 minutes, the cost of writing, typed faster than it can be read, then re-framed by the "
           "narrator: the pride is the problem the film will solve.",
    "s0b": "Same lines, but the whole open happens at the typewriter, so the viewer sits through the act of "
           "writing before the film names it.",
    "s1": "Where the dream came from: a family that stops school early, a father with a third-grade education and "
          "two thousand books. Sets up who the slow writer is and why the stakes are personal.",
    "s2": "Nine months that took away the people the dream was for. The dates are typed on paper because these "
          "are facts, not story. The black is the loss.",
    "s3": "Alone, he did what the film says he was good at: he wrote. It cost him half an hour a statement, and "
          "it got him rejected. The music starts here, because this is where he starts.",
    "s4": "Well said: the habit of writing about the person he would become, in his own 2023 words, accelerating "
          "until the proverb stops it: a gourd drawn on paper won’t cook a curry.",
    "s5": "Well done: the turn from writing to building. Slow, because cooking is slow, and because these are "
          "the only true proofs in the film.",
    "s6": "The argument lands: children who think in Tamil and aren’t fast writers don’t have to write to build.",
    "s7": "The ask, on paper only: he is still slow and no longer needs to be fast. The film ends on his father.",
}


def fmt(t):
    m = int(t // 60)
    return f"{m}:{t - 60 * m:05.2f}"


def card_visual(c, sec_ground):
    g = c.get("ground", sec_ground)
    faces = []
    for p in c["parts"]:
        f = {"fraunces": "Fraunces", "italic": "Fraunces italic", "mono": "JetBrains Mono", "tamil": "Noto Serif Tamil"}[p["face"]]
        faces.append(f"{f} {p['size']} px")
    s = f"{g} ground; {', '.join(dict.fromkeys(faces))}; {c['lines']} line(s), widest {c['widest_px']} px of 1728"
    acc = [a for p in c["parts"] for a in p.get("accent", [])]
    if acc and g != "paper":
        s += f"; accent: {', '.join(repr(a) for a in acc)}"
    if c.get("gourd"):
        s += "; the gourd drawn in ink at the right of the sheet (7 strokes, 4.8 s)"
    if c.get("capture"):
        s += f"; capture slot: {c['capture']} (blocked in v1)"
    return s


def card_motion(c):
    bits = []
    for p, pt in zip(c["parts"], c["parts_t"]):
        if p["reveal"] == "type":
            if p.get("schedule") == "coldopen":
                bits.append(f"typed, 1 key per frame (24/s) with 2-frame breaths before ‘77’ and ‘Period.’, "
                            f"{len(p['text'])} chars in {pt['visible'] - pt['t0']:.2f} s, caret")
            else:
                bits.append(f"typed at {p.get('cps')} keys/s" + (", caret" if p.get("caret") else "")
                            + (", uneven strike density" if p.get("paper") else ""))
        elif p["reveal"] == "ink":
            bits.append(f"soft ink reveal (word wave {B.INK_CPS:.0f} chars/s, {B.INK_FADE} s fades, blur 5→0)")
        elif p["reveal"] == "words":
            bits.append(f"word by word, {p.get('words_from')}→{p.get('words_to')} s apart (accelerating)")
        if p.get("pause"):
            bits.append(f"{p['pause']} s still")
    exit_ = "8-frame dissolve out" if c["exit"] == "dissolve" else "cut out"
    if c.get("black"):
        exit_ += "; then exactly 2.00 s of true black (48 frames)"
    return "; ".join(bits) + f"; {exit_}. Text never moves after it lands."


def card_sound(c, cue_events):
    kinds = [e["kind"] for e in cue_events if e.get("card") == c["id"]]
    parts = []
    n_key = sum(1 for k in kinds if k in ("key", "heavy"))
    if n_key:
        parts.append(f"{n_key} typewriter strikes")
    if "space" in kinds:
        parts.append("space-bar thuds")
    if "return" in kinds:
        parts.append("carriage return")
    if "pen" in kinds:
        parts.append("pen nib on paper for each stroke")
    if "knock" in kinds:
        parts.append("two soft knocks on a wooden door")
    for k in kinds:
        if k.startswith("wind-"):
            parts.append(f"wind {k[5:]}")
    return ", ".join(parts) if parts else "(section bed only)"


def main():
    placed, total, issues = B.assemble("A", B.WIDE)
    placedB, totalB, _ = B.assemble("B", B.WIDE)
    cue = B.cues(placed, total)
    cueB = B.cues(placedB, totalB)
    holds = []
    lines = []
    lines.append("---")
    lines.append("format: 1920x1080")
    lines.append(f"duration: {total:.2f}s")
    lines.append('message: "A slow writer built a tool so children never have to write to build. Well done beats well said."')
    lines.append("arc: Cold open (77 minutes) → Library → Nine months → Alone → Well said → Well done → Just say it → The ask")
    lines.append("audience: teachers, school leaders and builders in Tamil Nadu; anyone who has been told to write it down first")
    lines.append("mode: autonomous")
    lines.append("fps: 24")
    lines.append("open: A (B rendered separately as /out/open_B.mp4)")
    lines.append("---")
    lines.append("")
    lines.append("# 77 MINUTES — Storyboard")
    lines.append("")
    lines.append("Text-led cut (no narration was supplied, D009). Every value below comes from `tools/build.py` on the "
                 "same timeline the compositions are generated from: starts and durations are frame-exact at 24 fps, "
                 "holds are measured from the frame the last glyph is fully visible (D024). Footage slots name what "
                 "v2 drops in once the blocked hosts are allowed (D011–D012); v1 renders the typographic layer alone.")
    lines.append("")
    lines.append("| § | Section | Script target | Actual start | Duration | Ground |")
    lines.append("|---|---------|---------------|--------------|----------|--------|")
    targets = {"s0a": "0:00", "s1": "0:18", "s2": "1:15", "s3": "2:00", "s4": "2:50", "s5": "3:40", "s6": "4:10", "s7": "4:30"}
    for i, pl in enumerate(placed):
        lines.append(f"| {i} | {pl['sec']['name']} | {targets.get(pl['sid'], '')} | {fmt(pl['start'])} | "
                     f"{pl['dur']:.2f} s | {pl['sec']['ground']} |")
    lines.append(f"| | **Total (open A)** | 4:00–6:15 | | **{fmt(total)}** | |")
    lines.append(f"| | Total with open B | | | {fmt(totalB)} | |")
    lines.append("")
    lines.append("Sections run later than the script's timestamps because measured holds cannot fit the 18 s cold "
                 "open (D025); the total stays inside 4:00–6:15.")
    lines.append("")
    n = 0
    for pl in placed:
        sid = pl["sid"]
        sec = pl["sec"]
        lines.append(f"## Section {placed.index(pl)} — {sec['name']} ({fmt(pl['start'])}–{fmt(pl['end'])})")
        lines.append("")
        lines.append(f"- visual: {SECTION_VISUAL[sid]}")
        lines.append(f"- sound: {SECTION_SOUND[sid]}")
        lines.append(f"- footage_slot (v2): {sec.get('footage', 'none — typographic by design')}")
        kind = "first section" if placed.index(pl) == 0 else B.TRANSITIONS[sid][0]
        lines.append(f"- enters: {kind}" + (f" (gap {B.TRANSITIONS[sid][1]} s of black, then an 8-frame fade in)" if kind == "black" else
                                              " (8-frame dissolve over the previous ground)" if kind == "dissolve" else
                                              " (same ground, invisible seam)" if kind == "cut" else ""))
        lines.append("")
        lines.append(SECTION_WHY[sid])
        lines.append("")
        for c in pl["cards"]:
            n += 1
            g0 = pl["start"]
            text = " / ".join(p["text"] for p in c["parts"])
            lines.append(f"### Frame {n} — {c['id']}")
            lines.append("")
            lines.append(f"- start: {fmt(g0 + c['start'])} ({g0 + c['start']:.3f} s)")
            lines.append(f"- duration: {c['end'] - c['start']:.2f}s")
            lines.append(f"- scene: {text}")
            ti = "cut from bare ground into a typed reveal" if c["parts"][0]["reveal"] == "type" else "cut from bare ground into a soft ink reveal"
            if c is pl["cards"][0] and placed.index(pl) > 0:
                ti = f"{B.TRANSITIONS[sid][0]} into the section, then " + ti.split("into ")[1]
            lines.append(f"- transition_in: {ti}")
            lines.append(f"- visual: {card_visual(c, sec['ground'])}")
            lines.append(f"- motion: {card_motion(c)}")
            lines.append(f"- sound: {card_sound(c, cue['events'])}")
            lines.append(f"- script_line: {c['script']}")
            lines.append(f"- hold: {c['hold']:.2f}s (minimum {c['hold_min']:.2f}s = max(2.5, 0.3 × {c['words']} + 1.2); "
                         f"last glyph visible at {fmt(g0 + c['last_visible'])})")
            lines.append(f"- src: compositions/{sid}.html")
            lines.append(f"- poster: {c['last_visible'] + 0.5:.2f}")
            lines.append("- status: outline")
            if c.get("note"):
                lines.append("")
                lines.append(c["note"])
            lines.append("")
            holds.append(dict(id=c["id"], section=sid, start=round(g0 + c["start"], 3), text=text, words=c["words"],
                              hold_min=c["hold_min"], hold=c["hold"], ok=c["hold"] + 1e-6 >= c["hold_min"],
                              lines=c["lines"]))
            if c.get("black"):
                n += 1
                a, b = c["black"]
                lines.append(f"### Frame {n} — two seconds of black")
                lines.append("")
                lines.append(f"- start: {fmt(g0 + a)} ({g0 + a:.3f} s)")
                lines.append(f"- duration: {b - a:.2f}s")
                lines.append("- scene: true black, 48 frames")
                lines.append("- transition_in: cut")
                lines.append("- visual: #000 over everything")
                lines.append("- motion: none")
                lines.append("- sound: silence — room tone ducks out on the cut and returns on the next card")
                lines.append("- script_line: two seconds of black")
                lines.append("- status: outline")
                lines.append("")
    # cold open B appendix
    lines.append("## Appendix — Cold open B (rendered as /out/open_B.mp4)")
    lines.append("")
    lines.append(f"- visual: {SECTION_VISUAL['s0b']}")
    lines.append(f"- sound: {SECTION_SOUND['s0b']}")
    lines.append(f"- duration: {placedB[0]['dur']:.2f}s (open A is {placed[0]['dur']:.2f}s)")
    lines.append("")
    lines.append(SECTION_WHY["s0b"])
    lines.append("")
    for c in placedB[0]["cards"]:
        text = " / ".join(p["text"] for p in c["parts"])
        lines.append(f"### B — {c['id']}")
        lines.append("")
        lines.append(f"- start: {fmt(c['start'])}")
        lines.append(f"- duration: {c['end'] - c['start']:.2f}s")
        lines.append(f"- scene: {text}")
        lines.append(f"- motion: {card_motion(c)}")
        lines.append(f"- sound: {card_sound(c, cueB['events'])}")
        lines.append(f"- hold: {c['hold']:.2f}s (minimum {c['hold_min']:.2f}s)")
        lines.append(f"- src: compositions/s0b.html")
        lines.append("- status: outline")
        lines.append("")
        holds.append(dict(id=c["id"], section="s0b", start=round(c["start"], 3), text=text, words=c["words"],
                          hold_min=c["hold_min"], hold=c["hold"], ok=c["hold"] + 1e-6 >= c["hold_min"], lines=c["lines"]))
    status = sys.argv[1] if len(sys.argv) > 1 else "outline"
    md = "\n".join(lines).replace("- status: outline", f"- status: {status}")
    (OUT / "STORYBOARD.md").write_text(md + "\n")
    (OUT / "holds.json").write_text(json.dumps(dict(rule="hold >= max(2.5, 0.3*words + 1.2) seconds, measured from the "
                                                          "frame the last glyph is fully visible to the first exit frame",
                                                    fps=24, total_open_A=total, total_open_B=totalB, cards=holds),
                                               ensure_ascii=False, indent=1))
    bad = [h for h in holds if not h["ok"] or h["lines"] > 2]
    print(f"STORYBOARD.md: {n} frames; holds.json: {len(holds)} cards; failing: {len(bad)}")
    for b in bad:
        print("  FAIL", b)


if __name__ == "__main__":
    main()
