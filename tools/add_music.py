"""Give every reel in schedule.json that has no "sound" yet a random background track from sounds/playlist.txt.
Never the same track as the entry just before it. Run from the repo root: python3 tools/add_music.py"""
import json, random, subprocess, os

pl = [l.strip() for l in open("sounds/playlist.txt") if l.strip()]
sch = json.load(open("schedule.json"))
sch.sort(key=lambda e: e["slot"])
prev = None
for e in sch:
    if e.get("sound"):
        prev = e["sound"]; continue
    if not os.path.exists(e["file"]):
        continue
    s = random.choice([x for x in pl if x != prev] or pl); prev = s
    tmp = e["file"].replace(".mp4", ".tmp.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", e["file"], "-i", f"sounds/{s}", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", "afade=t=out:st=13.8:d=1.2", "-shortest",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, e["file"])
    e["sound"] = s
    print(e["slot"], s)
json.dump(sch, open("schedule.json", "w"), indent=1, ensure_ascii=False)
