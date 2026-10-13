# @quotations_and_quotes — Instagram reels automation

This repo holds the reels for the Instagram account **@quotations_and_quotes** (owner: Sarmad, Pakistan, timezone **Asia/Karachi**). Talk to the owner in **Roman Urdu**, short and simple.

- `media/` — reels waiting to be posted (MP4, 1080x1350, 15 s, with background music). Deleted after they are posted.
- `schedule.json` — one entry per post: `slot` (Karachi time), `file`, `mood`, `sound`, `caption`, `approved`, `posted`, `permalink`.
- `sounds/` — the owner's chosen background tracks; `sounds/playlist.txt` lists the ones in use (1 lofi udaas piano, 3 bansuri cinematic, 4 romantic guitar, 5 slowed reverb sad). All are original, made with `tools/sounds.py`.
- `weeks/` — the quote lists each week's reels were made from.
- `tools/` — `make_reels.sh <posts.json> <out_dir> [seed]` renders silent reels in the house style; `add_music.py` gives each new reel a random track from the playlist (never the same as the reel before it).

## How posting works (owner's decision, 13 Oct 2026)

Fully automatic. Two reels a day, **10:00 and 18:00 Karachi**, published through the **vidIQ** connector (`vidiq_instagram_publish_reel`) to the connected account quotations_and_quotes. The owner gave standing approval on 13 Oct 2026 for every reel this system makes to be posted automatically with its caption and background music; `approved: true` records that. He plans to connect a Facebook Page within about a week and then switch to Instagram-library songs via Metricool; until he says so, keep this system.

Video URLs for vidIQ are GitHub raw links: `https://raw.githubusercontent.com/Sarmads050/reels/main/<file>`.

## Rules that never change

- Never post the same entry twice. If anything fails, do not retry in a loop: record `"error"` on the entry, push, and tell the owner.
- Only post entries with `approved: true`. If the owner ever asks to check reels before posting, set new entries to `approved: false` until he says yes.
- Quotes are original (no copied poetry or lyrics), Roman Urdu, mood: sad / deep / reality / loneliness / mohabbat / sabr / dua / himmat / umeed.
- Only the tracks in `sounds/` are used as music. Never download or add copyrighted songs.
- Commits end with:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

## Posting run (starts ~09:56 and ~17:56 Karachi)

1. `git pull`. Get the current time with the time tool and convert to Asia/Karachi.
2. In `schedule.json`, pick the earliest entry with `approved: true`, `posted: false`, whose `slot` is not more than 15 minutes in the future and not more than 6 hours in the past. Post only that one entry per run. Nothing due → check that tomorrow has entries (tell the owner if not), otherwise stop quietly.
   - An entry more than 6 hours late: mark `"error": "missed"` and tell the owner; do not post it late.
3. `vidiq_instagram_connected_accounts` → the account `quotations_and_quotes` with `publishingAvailable: true` (its `platformAccountId`).
4. `vidiq_video_upload` with `url` = the raw GitHub link of `file` and a short `title`. If it is still processing, call again with `uploadId`.
5. `vidiq_instagram_publish_reel` with `videoUrl` from step 4, the entry's exact `caption`, and the `platformAccountId`. Then continue with `containerId` (wait ~5 s between calls) until `PUBLISHED`.
6. Success: set `posted: true` and `permalink`, `git rm` the media file, commit ("Posted <slot>"), push. Final message to the owner: one short Roman Urdu line with the permalink.

## Weekly run (Sunday evening Karachi)

1. `git pull`. Drop entries from `schedule.json` whose slot is more than 14 days old.
2. Results of the last 7 days: `vidiq_instagram_owner_insights` (and `vidiq_ig_profile_reels` for public numbers). Compare moods, morning vs evening, and background tracks. Keep vidIQ credit use under 15 per week.
3. Write 14 new original quotes for the 7 days that start the day after the last slot already in `schedule.json` (7 morning 10:00, 7 evening 18:00), leaning toward what performed best. Never repeat a quote already used (check `weeks/`). Each entry: `id`, `scene` (one of road, rain, moon, mist, sunset, sunrise, city — vary them), `label` (one or two words, CAPS), `line1`, `line2` (short, the punch), `mood`. Save as `weeks/<first-date>_am.json` and `_pm.json`.
4. Render: `tools/make_reels.sh weeks/<first-date>_am.json <tmp> <new seed>` (and `_pm`). Look at every `_preview.png`; text must be easy to read on the background. Fix and re-render any that are not.
5. Copy MP4s to `media/w<week>_d<n>_am.mp4` / `_pm.mp4`, add 14 entries to `schedule.json` with `mood`, captions (engaging line + CTA to Save/Share/Comment, then `\n\nFollow @quotations_and_quotes for daily deep lines\n\n` + 5 relevant hashtags), `approved: true`, `posted: false`. Run `python3 tools/add_music.py`. Commit and push.
6. Send the owner: a short summary of last week's results, a contact sheet of the 14 previews, and a table of quotes + captions + music. If he asks for changes, re-render those, update `schedule.json`, push and show them again.

## Post checklist (owner's standard)

Powerful, short, heart-touching quote · premium aesthetic + cinematic background matched to mood · grain, shadows, contrast · consistent fonts (Cormorant Garamond + DM Sans) and palette (cream + gold #E6B25C) · "QUOTATIONS & QUOTES" + handle watermark · readable on mobile, good spacing · 1080x1350 · engaging caption with CTA · relevant hashtags · original and share-/save-worthy.
