# @quotations_and_quotes — Instagram reels automation

This repo holds the reels for the Instagram account **@quotations_and_quotes** (owner: Sarmad, Pakistan, timezone **Asia/Karachi**). Talk to the owner in **Roman Urdu**, short and simple.

- `media/` — reels waiting to be posted (MP4, 1080x1350, 15 s). Deleted after they are posted.
- `schedule.json` — one entry per post: `slot` (Karachi time), `file`, `caption`, `approved`, `posted`, `permalink`.
- `weeks/` — the quote lists each week's reels were made from.
- `tools/` — `make_reels.sh <posts.json> <out_dir> [seed]` renders reels in the house style (`premium.py` designs, `raag.py` music, `fonts/`, `music/raag.wav`).

Publishing goes through the **vidIQ** connector (`vidiq_instagram_publish_reel`); the account is connected there with publishing access. Media URLs for vidIQ are GitHub raw links: `https://raw.githubusercontent.com/Sarmads050/reels/main/<file>`.

## Rules that never change

- Only post entries with `"approved": true`. The owner approves the exact video and caption; `approved: true` is that approval. Never set `approved` yourself unless the owner says yes in chat.
- Never post the same entry twice. If anything fails, do not retry in a loop: record `"error"` on the entry, push, and tell the owner.
- Quotes are original (no copied poetry or lyrics), Roman Urdu, mood: sad / deep / reality / loneliness / sabr / dua / himmat.
- Commits end with:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

## Posting run (10:00 and 18:00 Karachi)

1. `git pull`. Get the current time with the time tool and convert to Asia/Karachi.
2. In `schedule.json`, pick the earliest entry with `approved: true`, `posted: false`, whose `slot` is not more than 20 minutes in the future and not more than 6 hours in the past. Post only that one entry per run. Nothing due → stop quietly.
   - An approved entry more than 6 hours late: mark `"error": "missed"` and tell the owner; do not post it late.
   - A due entry with `approved: false`: do not post; tell the owner it is waiting for approval.
3. `vidiq_instagram_connected_accounts` → the account `quotations_and_quotes` with `publishingAvailable: true` (its `platformAccountId`).
4. `vidiq_video_upload` with `url` = the raw GitHub link of `file` and a short `title`. If it is still processing, call again with `uploadId`.
5. `vidiq_instagram_publish_reel` with `videoUrl` from step 4, the entry's exact `caption`, and the `platformAccountId`. Then continue with `containerId` (wait ~5 s between calls) until `PUBLISHED`.
6. Success: set `posted: true` and `permalink`, `git rm` the media file, commit ("Posted <slot>"), push. Send the owner one short line with the permalink.

## Weekly run (Sunday evening Karachi)

1. `git pull`. Clean `schedule.json`: drop entries posted more than 14 days ago.
2. Results of the last 7 days: `vidiq_instagram_owner_insights` (and `vidiq_ig_profile_reels` for public numbers). Compare moods / quote styles / morning vs evening. Keep vidIQ credit use under 15 per week.
3. Write 14 new original quotes for next Monday–Sunday (7 morning 10:00, 7 evening 18:00), leaning toward what performed best. Each entry: `id`, `scene` (one of road, rain, moon, mist, sunset, sunrise, city — vary them), `label` (one or two words, CAPS), `line1`, `line2` (short, the punch). Save as `weeks/<monday-date>_am.json` and `_pm.json`.
4. Render: `tools/make_reels.sh weeks/<date>_am.json <tmp> <new seed>` (and `_pm`). Look at every `_preview.png`; text must be easy to read on the background. Fix and re-render any that are not.
5. Copy MP4s to `media/w<week>_d<n>_am.mp4` / `_pm.mp4`, add 14 entries to `schedule.json` with captions (engaging line + CTA to Save/Share/Comment, then `\n\nFollow @quotations_and_quotes for daily deep lines\n\n` + 5 relevant hashtags), `approved: false`. Commit and push.
6. Send the owner: a summary of last week's results, a contact sheet of the 14 previews, and a table of quotes + captions. Ask for approval ("Haan" approves all; or name what to change). When they approve, set `approved: true` for those entries and push.

## Post checklist (owner's standard)

Powerful, short, heart-touching quote · premium aesthetic + cinematic background matched to mood · grain, shadows, contrast · consistent fonts (Cormorant Garamond + DM Sans) and palette (cream + gold #E6B25C) · "QUOTATIONS & QUOTES" + handle watermark · readable on mobile, good spacing · 1080x1350 · engaging caption with CTA · relevant hashtags · original and share-/save-worthy.
