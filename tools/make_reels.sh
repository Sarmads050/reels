#!/usr/bin/env bash
# Usage: tools/make_reels.sh <posts.json> <out_dir> [seed]
# Renders SILENT 1080x1920 (9:16), 12 s quote reels in the house style (tools/reel916.py):
# light background with slow zoom + drifting dust, line 1 visible from frame 0, line 2 rises in at ~2 s,
# no fade-out (loops). The owner adds an Instagram song himself, so there is no audio track.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
JSON="$1"; OUT="$2"; SEED="${3:-100}"
TMP="$(mktemp -d)"
mkdir -p "$OUT"
PYTHONDONTWRITEBYTECODE=1 SEED="$SEED" python3 "$HERE/reel916.py" "$TMP" "$JSON" >/dev/null
for id in $(python3 -c "import json,sys;print(' '.join(p['id'] for p in json.load(open(sys.argv[1]))))" "$JSON"); do
  ffmpeg -y -loglevel error -loop 1 -i "$TMP/${id}_bg.png" -loop 1 -i "$TMP/${id}_dust.png" \
    -loop 1 -i "$TMP/${id}_l1.png" -loop 1 -i "$TMP/${id}_l2.png" -loop 1 -i "$TMP/${id}_brand.png" \
    -filter_complex "[0:v]scale=2160:3840,zoompan=z='1.0+0.0002*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=360:s=1080x1920:fps=30,noise=alls=2:allf=t[b];[1:v]format=rgba[du];[b][du]overlay=x=0:y='-mod(t*35\,1920)':shortest=1[b1];[b1][4:v]overlay=0:0[b2];[b2][2:v]overlay=0:0[b3];[3:v]format=rgba,fade=t=in:st=2.0:d=0.9:alpha=1[t2];[b3][t2]overlay=x=0:y='if(lt(t,2),20,if(lt(t,2.9),20-(t-2)*22,0))',format=yuv420p[v]" \
    -map "[v]" -an -t 12 -r 30 -c:v libx264 -preset slow -crf 21 -movflags +faststart "$OUT/${id}.mp4"
  cp "$TMP/${id}.png" "$OUT/${id}_preview.png"
done
rm -rf "$TMP"
