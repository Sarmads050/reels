"""Make sure every reel in schedule.json that is not posted yet has background music.
A reel gets a random track from sounds/playlist.txt (never the same as the entry just before it) when it has
no "sound" yet OR when its file has no audio stream. Run from the repo root: python3 tools/add_music.py
Exit code 1 if any unposted reel still has no audio afterwards."""
import json, random, subprocess, os, sys

def has_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return "audio" in r.stdout

pl = [l.strip() for l in open("sounds/playlist.txt") if l.strip()]
sch = json.load(open("schedule.json"))
sch.sort(key=lambda e: e["slot"])
prev, bad = None, []
for e in sch:
    if e.get("posted") or not os.path.exists(e["file"]):
        prev = e.get("sound", prev); continue
    if e.get("sound") and has_audio(e["file"]):
        prev = e["sound"]; continue
    s = random.choice([x for x in pl if x != prev] or pl); prev = s
    tmp = e["file"].replace(".mp4", ".tmp.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", e["file"], "-i", f"sounds/{s}", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", "afade=t=out:st=13.8:d=1.2", "-shortest",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, e["file"])
    e["sound"] = s
    print(e["slot"], s)
for e in sch:
    if not e.get("posted") and os.path.exists(e["file"]) and not has_audio(e["file"]):
        bad.append(e["file"])
json.dump(sch, open("schedule.json", "w"), indent=1, ensure_ascii=False)
if bad:
    print("NO AUDIO:", *bad); sys.exit(1)
