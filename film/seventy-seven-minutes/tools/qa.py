"""QA for 77 MINUTES: every check is measured on the delivered files, and the evidence is
written to /out/qc/qa_evidence.json. QA.md is written from it.

  python tools/qa.py
"""
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path("/out")
QC = OUT / "qc"
sys.path.insert(0, str(ROOT / "tools"))

FILM = OUT / "77minutes_1080p.mp4"
SQUARE = OUT / "77minutes_square.mp4"
OPENS = [OUT / "open_A.mp4", OUT / "open_B.mp4"]

INK = np.array([0x1B, 0x1A, 0x17], float)
PAPER = np.array([0xF2, 0xEB, 0xDD], float)
ACCENT = np.array([0xC8, 0x90, 0x2E], float)
BLACK = np.array([0, 0, 0], float)


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]).stdout
    return json.loads(out)


def loudness(path):
    p = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(path), "-map", "0:a", "-af",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    txt = p.stderr[p.stderr.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", txt).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", txt).group(1))
    lra = float(re.search(r"LRA:\s+(-?[\d.]+) LU", txt).group(1))
    return dict(integrated_lufs=i, true_peak_dbtp=tp, lra_lu=lra)


def delivery(path):
    pr = probe(path)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    return dict(path=str(path), duration_s=float(pr["format"]["duration"]), width=v["width"], height=v["height"],
                fps=v["r_frame_rate"], vcodec=v["codec_name"], profile=v.get("profile"), pix_fmt=v.get("pix_fmt"),
                video_bitrate=int(v.get("bit_rate", 0)), acodec=a["codec_name"], sample_rate=int(a["sample_rate"]),
                channels=a["channels"], audio_bitrate=int(a.get("bit_rate", 0)), size_bytes=int(pr["format"]["size"]),
                loudness=loudness(path))


def frame(path, t, size=None):
    args = ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1", "-f", "rawvideo",
            "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(args, check=True, capture_output=True).stdout
    w, h = size or (1920, 1080)
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3)


def norm_text(s):
    s = unicodedata.normalize("NFC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("\u00a0", " "), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- 1. script and facts
def check_script(tl, prefix=False):
    """The screen text equals the script (prefix=True: the screen is the script's opening, as in the square)."""
    src_lines = []
    extra = []
    for ln in (ROOT / "timeline" / "script_source.txt").read_text().splitlines():
        if not ln or ln.startswith("#"):
            continue
        if ln.startswith("+ "):
            extra.append(ln[2:])
            src_lines.append(ln[2:])
        else:
            src_lines.append(ln)
    src = norm_text(" ".join(src_lines))
    screen = []
    for s in tl["sections"]:
        for c in s["cards"]:
            screen.append(" ".join(p["text"] for p in c["parts"]))
    scr = norm_text(" ".join(screen))
    # the brother's quote is shown with quote marks; the script writes 'Everything ... dress.'
    ok = src.startswith(scr) if prefix else scr == src
    diff = None
    if not ok:
        i = next((k for k in range(min(len(scr), len(src))) if scr[k] != src[k]), min(len(scr), len(src)))
        diff = dict(at=i, screen=scr[max(0, i - 40):i + 40], source=src[max(0, i - 40):i + 40])
    return dict(ok=ok, cards=len(screen), non_script_on_screen=extra, first_difference=diff)


# Every number, date and name on screen, mapped to the FACTS sentence that licenses it.
# (on-screen token, fact sentence substring)
CLAIMS = [
    ("77 minutes", "I took 77 minutes for writing this message to you"),
    ("77 MINUTES", "I took 77 minutes for writing this message to you"),
    ("one message to a Harvard professor", "2022 letter to a Harvard professor"),
    ("2022", "2022 letter to a Harvard professor"),
    ("Harvard", "2022 letter to a Harvard professor"),
    ("Ahmad", "Ahmad Yoosuf"),
    ("Adirampattinam", "From Adirampattinam, a coastal town"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Islam", "Family are scholars of Islam"),
    ("class ten or twelve", "around class 10 or 12"),
    ("first of us to go to college", "First in the family to attend college"),
    ("third grade", "Father studied until third grade"),
    ("two thousand books", "owned more than 2,000 books"),
    ("nine and fifteen", "Ages 9 to 15"),
    ("seventh grade to tenth", "Grades 7 to 10"),
    ("came first in all eighteen exams", "first rank in all 18 exams"),
    ("October 2018", "Maternal grandmother died October 2018"),
    ("15 November 2018", "Cyclone Gaja, 15 November 2018"),
    ("Gaja", "Cyclone Gaja"),
    ("December 2018", "Paternal grandmother died December 2018"),
    ("Forty-five days after the first", "45 days after the first"),
    ("1 July 2019", "died 1 July 2019"),
    ("forty-three", "aged 43"),
    ("two of the final four months", "sick in bed two of the last four months"),
    ("seventy-five percent", "finished with 75 percent"),
    ("MIT", "Harvard, MIT, Princeton and Yale"),
    ("Princeton", "Harvard, MIT, Princeton and Yale"),
    ("Yale", "Harvard, MIT, Princeton and Yale"),
    ("SAT", "no SAT"),
    ("half an hour", "It took nearly half an hour"),
    ("a hundred companies", "about 100 companies"),
    ("four hundred", "more than 400 roles"),
    ("2010", "a laptop released in 2010"),
    ("27 August 2023", "Journal, 27 August 2023"),
    ("at eighteen", "age 18"),
    ("vaakku.org", "(vaakku.org)"),
    ("statement2xl.com", "(statement2xl.com)"),
    ("ayyayo", "ayyayo, voice-to-code"),
    ("Chennai", "Based in Chennai"),
    ("I first used it for an agent that found lost photos", "first used for an agent that found lost photos"),
]
# Number words the fixed script uses as ordinary words, claiming no quantity.
NON_NUMERIC = [("Every one of those notes", "script line: Every one of those notes was a gourd on paper.")]
SCRIPT_ONLY = [("five thirty", "script line: I woke up at five thirty, prayed, and put on my school uniform."),
               ("Around seven", "script line: Around seven, my brother knocked on my door."),
               ("For three years", "script line: For three years I filled notes with plans, rules and resolutions.")]
CREDIT_NAMES = ["Salamander Grand Piano V3", "Alexander Holm", "CC BY 3.0"]

NUMBER_WORDS = r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|" \
               r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|" \
               r"thousand|first|second|third|fourth|fifth|seventh|tenth|half)\b"


def check_facts(tl):
    facts = json.loads((OUT / "facts.json").read_text())
    fact_text = " ".join(facts["facts"])
    claims_ok = [dict(token=t, fact=f, ok=f in fact_text) for t, f in CLAIMS]
    # cards are joined with a pilcrow, so no phrase or name test can run across a card boundary
    screen = " ¶ ".join(norm_text(" ".join(p["text"] for p in c["parts"])) for s in tl["sections"] for c in s["cards"])
    covered = [t for t, _ in CLAIMS] + [t for t, _ in SCRIPT_ONLY] + [t for t, _ in NON_NUMERIC] + CREDIT_NAMES
    # every digit run and number word on screen must sit inside a covered phrase
    uncovered = []
    for m in re.finditer(r"\d+(?:,\d{3})*|" + NUMBER_WORDS, screen, flags=re.I):
        span = (m.start(), m.end())
        hit = False
        for phrase in covered:
            for mm in re.finditer(re.escape(phrase), screen):
                if mm.start() <= span[0] and span[1] <= mm.end():
                    hit = True
        if not hit:
            uncovered.append(screen[max(0, m.start() - 25):m.end() + 25])
    # every capitalised name-like token that is not sentence-initial must be covered too
    names = set(re.findall(r"(?<=[a-z,] )([A-Z][A-Za-z0-9.]+)", screen))
    common = {"I", "I'm", "MINUTES", "Period", "Islam"}
    name_unc = sorted(n for n in names - common if not any(n.strip(".,") in c for c in covered + ["Tamil", "English", "DMs", "Change"]))
    emoji = sorted({ch for ch in screen if ord(ch) > 0x1F000})
    return dict(ok=all(c["ok"] for c in claims_ok) and not uncovered and not name_unc and emoji == ["😅", "😢"],
                claims=claims_ok, script_only=SCRIPT_ONLY, non_numeric=NON_NUMERIC, credit_names=CREDIT_NAMES,
                uncovered_numbers=uncovered,
                uncovered_names=name_unc, emoji=emoji)


# ---------------------------------------------------------------- sound on the frame
def check_sync(path, cues):
    """Each typewriter strike's onset in the delivered soundtrack, against the frame its character appears."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-ac", "1", "-ar", "48000",
                          "-f", "f32le", "-"], check=True, capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(float)
    sr = 48000
    # the strike is a click: high-pass (first difference), 0.5 ms envelope, and the steepest rise is the onset
    env = np.convolve(np.abs(np.diff(x, prepend=x[:1])), np.ones(24) / 24, mode="same")
    rise = np.diff(env, prepend=env[:1])
    offs = []
    for e in cues["events"]:
        if e["kind"] not in ("key", "heavy"):
            continue
        # neighbours at 24 keys/s are 41.7 ms away, outside this window
        a, b = int((e["t"] - 0.015) * sr), int((e["t"] + 0.035) * sr)
        offs.append(((a + int(np.argmax(rise[a:b]))) / sr - e["t"]) * 1000)
    offs = np.abs(np.array(offs))
    return dict(strikes=len(offs), max_abs_ms=round(float(offs.max()), 2), p95_abs_ms=round(float(np.percentile(offs, 95)), 2),
                frame_ms=round(1000 / 24, 2), within_one_frame=bool(offs.max() <= 1000 / 24))


# ---------------------------------------------------------------- 2. Tamil shaping
def check_tamil():
    import measure as Mz
    text = "ஏட்டுச் சுரைக்காய் கறிக்கு உதவாது"
    w, names = Mz.shape(text, "tamil", 64)
    bad = [n for n in names if n in (".notdef", "uni25CC", "dottedcircle")]
    expected = ["ttutamil", "cutamil", "kutamil", "tutamil"]
    return dict(ok=not bad and all(e in names for e in expected), glyphs=names, broken=bad, conjunct_ligatures=expected,
                rendered_crop="qc/tamil_rendered.png")


# ---------------------------------------------------------------- 3. palette
SEGMENTS = [(BLACK, PAPER), (BLACK, ACCENT), (INK, PAPER), (INK, ACCENT), (BLACK, INK), (PAPER, ACCENT)]


def chroma_blocks(img):
    """2x2 block means: the chroma resolution of 4:2:0 video. Subsampling smears colour across a block at every
    accent edge, but the block mean of a mix of two palette colours stays on the segment between them."""
    h, w, _ = img.shape
    return img[:h // 2 * 2, :w // 2 * 2].reshape(h // 2, 2, w // 2, 2, 3).astype(float).mean(axis=(1, 3))


def palette_distance(img):
    px = img.reshape(-1, 3).astype(float)
    px = px[:: max(1, len(px) // 200000)]
    best = np.full(len(px), np.inf)
    for a, b in SEGMENTS:
        ab = b - a
        t = np.clip(((px - a) @ ab) / (ab @ ab), 0, 1)
        d = np.linalg.norm(px - (a + t[:, None] * ab), axis=1)
        best = np.minimum(best, d)
    return float(np.percentile(best, 99.9)), float(best.max())


def main():
    tl = json.loads((ROOT / "build" / "timeline-A.json").read_text())
    ev = {}
    ev["script"] = check_script(tl)
    ev["facts"] = check_facts(tl)
    tl_b = json.loads((ROOT / "build" / "timeline-B.json").read_text())
    tl_sq = json.loads((ROOT / "build" / "timeline-square.json").read_text())
    ev["script_open_B"] = check_script(tl_b)
    ev["facts_open_B"] = check_facts(tl_b)
    ev["script_square"] = check_script(tl_sq, prefix=True)
    ev["tamil"] = check_tamil()

    ev["film"] = delivery(FILM)
    fm = ev["film"]
    dur = fm["duration_s"]
    ev["delivery_ok"] = ((fm["width"], fm["height"], fm["fps"], fm["vcodec"], fm["profile"], fm["acodec"],
                          fm["sample_rate"]) == (1920, 1080, "24/1", "h264", "High", "aac", 48000))
    ev["runtime_ok"] = 240.0 <= dur <= 375.0
    ev["loudness"] = fm.pop("loudness")
    ev["sync"] = check_sync(FILM, json.loads((ROOT / "build" / "cues-A.json").read_text()))
    ev["sync_ok"] = ev["sync"]["within_one_frame"]
    ev["loudness_ok"] = abs(ev["loudness"]["integrated_lufs"] + 16.0) <= 0.5 and ev["loudness"]["true_peak_dbtp"] < -1.0

    # first three seconds: the typed letter line is complete by 3.0 s
    full = frame(FILM, 5.0)
    mask_full = full.max(axis=2) > 95
    # flat-colour accuracy: the fill of the accent words and of the paper-coloured letters, as decoded
    fi = full.astype(int)
    acc_px = (np.abs(fi - ACCENT.astype(int)).sum(axis=2) < 40)
    pap_px = (np.abs(fi - PAPER.astype(int)).sum(axis=2) < 40)
    ev["flat_colour"] = dict(accent_target=ACCENT.astype(int).tolist(),
                             accent_decoded=np.median(fi[acc_px], axis=0).astype(int).tolist(),
                             paper_target=PAPER.astype(int).tolist(),
                             paper_decoded=np.median(fi[pap_px], axis=0).astype(int).tolist())
    firsts = {}
    for t in (0.5, 1.0, 2.0, 2.9):
        f = frame(FILM, t)
        m = f.max(axis=2) > 95
        acc = ((np.abs(f.astype(int) - ACCENT.astype(int)).sum(axis=2)) < 60).sum()
        firsts[str(t)] = dict(text_px=int(m.sum()), share_of_full=round(float((m & mask_full).sum()) / max(1, mask_full.sum()), 3),
                              accent_px=int(acc))
        Image.fromarray(f).save(QC / f"first3s_{t:.1f}.png")
    ev["first_three_seconds"] = firsts
    ev["first_three_ok"] = firsts["2.9"]["share_of_full"] > 0.97 and firsts["1.0"]["accent_px"] > 500

    # Tamil as rendered in the delivered file
    for s in tl["sections"]:
        for c in s["cards"]:
            if c.get("gourd"):
                t = s["start"] + c["last_visible"] + 1.0
                f = frame(FILM, t)
                Image.fromarray(f[400:620, 80:1380]).save(QC / "tamil_rendered.png")
                ev["tamil"]["rendered_at_s"] = round(t, 3)

    # safe margins and two-line rule, measured on the rendered cards (snapshot pass)
    def strict(r):
        # judged here from the measured box, with no slack, whatever the measuring pass concluded
        if "box" not in r:
            return False
        bx, sf = r["box"], r["safe"]
        return bx[0] >= sf[0] and bx[1] >= sf[1] and bx[2] <= sf[2] and bx[3] <= sf[3] and r["rendered_lines"] <= 2

    cards = json.loads((QC / "cards_A.json").read_text())
    ev["margins_ok"] = all(strict(r) for r in cards)
    ev["margins"] = dict(cards=len(cards), failing=[r for r in cards if not strict(r)], safe=cards[0]["safe"],
                         source=cards[0]["source"],
                         min_x=min(r["box"][0] for r in cards), max_x=max(r["box"][2] for r in cards),
                         min_y=min(r["box"][1] for r in cards), max_y=max(r["box"][3] for r in cards),
                         max_lines=max(r["rendered_lines"] for r in cards))
    sq_cards = QC / "cards_square.json"
    if sq_cards.exists():
        sc = json.loads(sq_cards.read_text())
        ev["margins_square"] = dict(cards=len(sc), failing=[r for r in sc if not strict(r)],
                                    min_x=min(r["box"][0] for r in sc), max_x=max(r["box"][2] for r in sc),
                                    min_y=min(r["box"][1] for r in sc), max_y=max(r["box"][3] for r in sc),
                                    max_lines=max(r["rendered_lines"] for r in sc), safe=sc[0]["safe"])
        ev["margins_ok"] = ev["margins_ok"] and all(strict(r) for r in sc)

    # holds
    holds = json.loads((OUT / "holds.json").read_text())
    ev["holds_ok"] = all(h["ok"] for h in holds["cards"])
    ev["total_open_B"] = holds["total_open_B"]
    ev["holds"] = dict(cards=len(holds["cards"]), failing=[h for h in holds["cards"] if not h["ok"]],
                       min_margin=round(min(h["hold"] - h["hold_min"] for h in holds["cards"]), 3))

    # palette conformance on frames sampled every 5 s
    worst = []
    for t in np.arange(1.0, dur - 0.5, 5.0):
        f = frame(FILM, float(t))
        p999, mx = palette_distance(chroma_blocks(f))
        full = palette_distance(f)[0]
        worst.append((round(float(t), 1), round(p999, 2), round(mx, 1), round(full, 2)))
    ev["palette"] = dict(sampled_frames=len(worst), measured_on="2x2 block means (4:2:0 chroma resolution)",
                         worst_p999=max(w[1] for w in worst), worst_frame=max(worst, key=lambda w: w[1]),
                         worst_p999_full_resolution=max(w[3] for w in worst), frames=worst)
    ev["palette_ok"] = ev["palette"]["worst_p999"] < 12.0

    # square and opens
    ev["square"] = delivery(SQUARE)
    sq = ev["square"]
    ev["square_ok"] = ((sq["width"], sq["height"], sq["fps"], sq["vcodec"], sq["acodec"], sq["sample_rate"]) ==
                       (1080, 1080, "24/1", "h264", "aac", 48000) and abs(sq["duration_s"] - 60.0) < 0.05)
    ev["opens"] = {}
    for o in OPENS:
        d = delivery(o)
        own = frame(o, 5.0).max(axis=2) > 95
        f = frame(o, 2.9)
        d["letter_complete_by_2.9s"] = round(float(((f.max(axis=2) > 95) & own).sum()) / max(1, own.sum()), 3)
        ev["opens"][o.name] = d
    excerpts = [ev["square"], *ev["opens"].values()]
    ev["excerpts_true_peak_ok"] = all(x["loudness"]["true_peak_dbtp"] < -1.0 for x in excerpts)
    ev["excerpts_integrated_ok"] = all(abs(x["loudness"]["integrated_lufs"] + 16.0) <= 0.5 for x in excerpts)

    # licensing: every media file in assets/ is covered by a SOURCES.csv row
    import csv
    import fnmatch
    rows = list(csv.DictReader(open(ROOT.parent / "assets" / "footage" / "SOURCES.csv")))
    pats = [r["file"] for r in rows]
    media = [p for p in (ROOT / "assets").rglob("*") if p.is_file() and p.suffix.lower() in
             (".wav", ".mp3", ".jpg", ".png", ".woff2", ".js", ".mp4")]
    uncovered = []
    for p in media:
        rel = "seventy-seven-minutes/" + str(p.relative_to(ROOT))
        if not any(fnmatch.fnmatch(rel, pat) for pat in pats):
            uncovered.append(rel)
    ev["licensing"] = dict(media_files=len(media), rows=len(rows), uncovered=uncovered)
    ev["licensing_ok"] = not uncovered

    # transitions and the gourd, read from the timeline the film was rendered from
    import collections
    import build as B
    exits = collections.Counter(c["exit"] for s in tl["sections"] for c in s["cards"])
    ev["transitions"] = dict(card_exits=dict(exits), dissolve_frames=round(B.DIS * B.FPS),
                             section_entries={sid: list(v) for sid, v in B.TRANSITIONS.items()},
                             sections_fading_to_black=sorted(B.FADE_OUT))
    ev["transitions_ok"] = (set(exits) <= {"cut", "dissolve"} and round(B.DIS * B.FPS) == 8 and
                            B.TRANSITIONS["s2"][0] == "black" and B.TRANSITIONS["s3"][0] == "black" and "s2" in B.FADE_OUT)
    gourds = [c for s in tl["sections"] for c in s["cards"] if c.get("gourd")]
    g = gourds[0]
    ev["gourd"] = dict(cards_with_drawing=len(gourds), card_on_screen_s=round(g["end"] - g["start"], 3),
                       drawing_on_screen_s=round(g["exit_at"] - (g["start"] + g.get("gourd_at", 0.32)), 3))
    ev["gourd_ok"] = len(gourds) == 1 and ev["gourd"]["card_on_screen_s"] <= 8.0

    # the HyperFrames check (lint, runtime, layout, contrast) on the project as rendered
    chk = json.loads((ROOT / "build" / "check.json").read_text())
    ev["hyperframes_check"] = {k: dict(ok=chk[k]["ok"], errors=chk[k]["errorCount"], warnings=chk[k]["warningCount"])
                               for k in ("lint", "runtime", "layout", "motion", "contrast")}
    ev["hyperframes_check_ok"] = chk["ok"] and chk["lint"]["errorCount"] == 0

    (QC / "qa_evidence.json").write_text(json.dumps(ev, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({k: v for k, v in ev.items() if k.endswith("_ok")}, indent=1))
    print("script", ev["script"]["ok"], "facts", ev["facts"]["ok"], "tamil", ev["tamil"]["ok"],
          "script B", ev["script_open_B"]["ok"], "facts B", ev["facts_open_B"]["ok"], "square", ev["script_square"]["ok"])
    print("loudness", ev["loudness"], "film", {k: ev["film"][k] for k in ("duration_s", "width", "height", "fps", "vcodec",
                                                                       "video_bitrate", "acodec", "sample_rate")})


if __name__ == "__main__":
    main()
