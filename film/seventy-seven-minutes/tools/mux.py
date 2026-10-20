"""Put the mastered soundtrack on each rendered MP4 (DECISIONS D047).

  python tools/mux.py            -> every deliverable in /out that exists
  python tools/mux.py open_A     -> just /out/open_A.mp4

HyperFrames renders the picture. This step copies the H.264 stream untouched and encodes the mastered WAV once, as
AAC-LC 256 kbps, 48 kHz stereo, trimmed to the picture's exact length. Running it again gives the same result.
"""
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "out"
AUD = ROOT / "assets" / "audio"

DELIVERABLES = {
    "77minutes_1080p": AUD / "mix_A.wav",
    "77minutes_square": AUD / "mix_square.wav",
    "open_A": AUD / "open_A.wav",
    "open_B": AUD / "open_B.wav",
}


def video_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                          "-of", "json", str(path)], check=True, capture_output=True, text=True).stdout
    return float(json.loads(out)["streams"][0]["duration"])


def mux(name, wav):
    mp4 = OUT / f"{name}.mp4"
    tmp = OUT / f".{name}.mux.mp4"
    dur = video_duration(mp4)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-i", str(wav),
                    "-map", "0:v:0", "-map", "1:a:0", "-map_metadata", "0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                    "-t", f"{dur:.6f}", "-movflags", "+faststart", str(tmp)], check=True)
    os.replace(tmp, mp4)
    print(f"{mp4.name}: {wav.name} -> AAC 256k 48 kHz, {dur:.3f} s")


def main():
    names = sys.argv[1:] or [n for n in DELIVERABLES if (OUT / f"{n}.mp4").exists()]
    for n in names:
        mux(n, DELIVERABLES[n])


if __name__ == "__main__":
    main()
