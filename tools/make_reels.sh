#!/usr/bin/env bash
# Usage: tools/make_reels.sh <posts.json> <out_dir> [seed]
# Renders silent 1080x1350, 15s cinematic quote reels (one per entry) with the house style.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
JSON="$1"; OUT="$2"; SEED="${3:-100}"
TMP="$(mktemp -d)"
mkdir -p "$OUT"
SEED="$SEED" python3 "$HERE/premium.py" "$HERE/fonts" "$TMP" "$JSON" >/dev/null
for id in $(python3 -c "import json,sys;print(' '.join(p['id'] for p in json.load(open(sys.argv[1]))))" "$JSON"); do
  ffmpeg -y -loglevel error -loop 1 -i "$TMP/${id}_bg.png" -loop 1 -i "$TMP/${id}_text.png" \
    -filter_complex "[0:v]scale=2160:2700,zoompan=z='1+0.00013*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=450:s=1080x1350:fps=30,noise=alls=3:allf=t,fade=t=in:st=0:d=0.8[b];[1:v]format=rgba,fade=t=in:st=0.9:d=1.4:alpha=1[t];[b][t]overlay=0:0:shortest=1,fade=t=out:st=14.2:d=0.8,format=yuv420p[v]" \
    -map "[v]" -t 15 -r 30 -c:v libx264 -preset slow -crf 23 -maxrate 4500k -bufsize 9000k -movflags +faststart "$OUT/${id}.mp4"
  cp "$TMP/${id}.png" "$OUT/${id}_preview.png"
done
rm -rf "$TMP"
