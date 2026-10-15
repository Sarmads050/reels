# @quotations_and_quotes — Instagram reels automation

This repo holds the reels for the Instagram account **@quotations_and_quotes** (owner: Sarmad, Pakistan, timezone **Asia/Karachi**). Talk to the owner in **Roman Urdu**, short and simple.

- `media/` — reels waiting to be posted (MP4, 1080x1350, 15 s, with our own background music). Deleted after they are posted.
- `schedule.json` — one entry per post: `slot` (Karachi time), `file`, `mood`, `sound`, `caption`, `approved`, `channel` (`vidiq` or `metricool`), `ig_song`, `metricool_id`, `metricool_uuid`, `posted`, `permalink`.
- `songs_pool.json` — slow, relaxing Instagram-library songs per mood group, refreshed weekly (see "Song research").
- `sounds/` — our own original background tracks; `sounds/playlist.txt` lists the ones in use (1 lofi udaas piano, 3 bansuri cinematic, 4 romantic guitar, 5 slowed reverb sad). Made with `tools/sounds.py`.
- `weeks/` — the quote lists each week's reels were made from.
- `tools/` — `make_reels.sh <posts.json> <out_dir> [seed]` renders silent reels in the house style; `add_music.py` gives each unposted reel without audio a random playlist track.

## How posting works (owner's decision, 15 Oct 2026: "Mix")

Two reels a day, **10:00 and 18:00 Karachi**, fully automatic, owner's standing approval (`approved: true`).

- **Metricool reels (`channel: metricool`)**: the **Monday–Friday 10:00** reels (5 a week). Posted through Metricool with a **slow Instagram-library song** that is trending for that mood, with the reel's own sound muted (`videoVolume: 0`). Metricool's free plan publishes at most **20 posts per calendar month**: count Metricool entries already scheduled or posted in that month; if a new one would be the 21st, make it `vidiq` instead.
- **vidIQ reels (`channel: vidiq`)**: every other slot. Posted through vidIQ with our own background music.
- Any Metricool reel that cannot get a song, cannot be scheduled, or did not publish falls back to vidIQ with our own music. **No reel is ever posted without music.**

Video URLs (both channels) are GitHub raw links: `https://raw.githubusercontent.com/Sarmads050/reels/main/<file>`.
Metricool brand id `7403821`. vidIQ account `quotations_and_quotes`.

## Rules that never change

- Never post the same entry twice. If anything fails, do not retry in a loop: record `"error"` on the entry, push, and tell the owner.
- Only post entries with `approved: true`. If the owner ever asks to check reels before posting, set new entries to `approved: false` until he says yes.
- Quotes are original (no copied poetry or lyrics), Roman Urdu, mood: sad / deep / reality / loneliness / mohabbat / sabr / dua / himmat / umeed.
- Our video files only ever contain the tracks in `sounds/`. Instagram songs are attached only through Instagram's own music library (Metricool `audioConfiguration`); never download a song or put it into a file.
- **Never post a reel without music** (owner's rule). Tracks may repeat freely.
- vidIQ credits are limited (150 a month). Song research uses **no** vidIQ credits (owner's rule).
- Instagram songs must be **slow and relaxing** (owner's rule).
- Commits end with:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

## Mood groups

- `sad`: reality, deep, zindagi, tanhai, dil ki baat, yaadein, sad lines
- `romantic`: mohabbat, love, yaadein (romantic)
- `spiritual`: sabr, dua, Juma, Allah, faith
- `hope`: himmat, umeed, safar, motivation

## Song research (no vidIQ credits)

Owner's rules (15 Oct 2026): songs must be **slow and relaxing** (no fast music), and finding them must not use vidIQ credits.

- Sources, all free: (1) web search for songs trending on Instagram Reels in Pakistan/India this month for the mood (e.g. "trending slow sad songs Instagram reels Pakistan <Month YYYY>", "sufi/naat slow reels trending", "slowed reverb Hindi Urdu songs reels"); (2) well-known slow songs that are always used on Urdu quote reels (sad/romantic ballads, sufi, naat, nazm, flute instrumentals).
- Look each song up in Instagram's library through the Metricool test draft (below) with search terms like "<song> slowed", "<song> acoustic", "<song> unplugged", "<song> flute", or just "<song>". Multiple-match errors list candidates; that is the search.
- Pick only slow versions: titles with slowed / reverb / acoustic / unplugged / lofi / flute / nazm, or the original song if it is itself a slow ballad. **Never** pick titles with remix, DJ, house, mashup, party, phonk, bass boosted or similar.
- Save to `songs_pool.json` under its group: `{title, artist, audioId, audioType, library_title, source, found}`. Keep at most 6 per group, drop songs older than 45 days. The group's **top 3** = the newest three (most recently confirmed as trending). Reuse is fine.
- Do not call `vidiq_instagram_tiktok_outlier_search` or `vidiq_watch_shortform_content` for songs.

Test draft for library lookups: Metricool post uuid `7689021596470561225` (a draft, date 2026-10-30, never published). Get its current id with `getScheduledPosts`; update it with `draft: true`, `autoPublish: false`, keeping it a draft. A successful update attaches that audio to the draft (harmless) and changes its id.

## Posting run (starts ~09:50 and ~17:50 Karachi)

1. `git pull`. Get the current time with the time tool and convert to Asia/Karachi.
2. **Check earlier Metricool reels.** For each entry with `channel: metricool`, `posted: false`, a `metricool_uuid`, and a slot already more than 10 minutes past: `getScheduledPosts` for that day. If the post is no longer listed as pending (or shows published), set `posted: true` (permalink: find it with `vidiq_ig_profile_reels` if cheap, else leave null) and `git rm` its media file. If it is still pending/failed and the slot is less than 6 hours ago, post it now through vidIQ with our music (steps 6–8) and tell the owner; otherwise mark `"error": "missed"` and tell the owner.
3. **Prepare Metricool reels for the next 36 hours.** For each entry with `channel: metricool`, `posted: false`, no `metricool_uuid`, slot within the next 36 hours (and at least 20 minutes away):
   - Monthly limit check (see above). Over the limit → set `channel: vidiq`.
   - Pick its song: from `songs_pool.json`, the top 3 of its mood group; use the one used least recently (rotate, avoid the song of the previous Metricool reel). Pool empty for the group → do "Song research" for it.
   - `createScheduledPost` (blogId `7403821`, date = slot with +05:00): `autoPublish: true`, `draft: false`, `media` = [raw GitHub link], `text` = the exact caption, `providers` [instagram], `publicationDate` {slot, `Asia/Karachi`}, `instagramData` {`type: REEL`, `showReelOnFeed: true`, `audioConfiguration` {`audioId`: the numeric id, `videoVolume`: 0}}.
   - Success → save `metricool_id`, `metricool_uuid`, `ig_song` {title, artist, audioId}. Failure → set `channel: vidiq`, note the error.
   - Commit and push.
4. **Due vidIQ reel.** Pick the earliest entry with `channel: vidiq` (or no channel), `approved: true`, `posted: false`, slot not more than 15 minutes in the future and not more than 6 hours in the past. One per run. If the slot is still more than 4 minutes away, wait (sleep) until about 3 minutes before it. An entry more than 6 hours late: mark `"error": "missed"`, tell the owner, do not post.
5. Music check: run `python3 tools/add_music.py`. If it exits with an error, do not post that entry: record `"error": "no audio"`, push, tell the owner. If it changed a file, commit and push.
6. `vidiq_instagram_connected_accounts` → the account `quotations_and_quotes` with `publishingAvailable: true` (its `platformAccountId`).
7. `vidiq_video_upload` with `url` = the raw GitHub link of `file` and a short `title`. If still processing, call again with `uploadId`.
8. `vidiq_instagram_publish_reel` with `videoUrl` from step 7, the entry's exact `caption`, and the `platformAccountId`. Continue with `containerId` (wait ~5 s between calls) until `PUBLISHED`.
9. Success: `posted: true`, `permalink`, `git rm` the media file, commit ("Posted <slot>"), push.
10. Final message to the owner, one or two short Roman Urdu lines: what was posted (permalink) and, if a Metricool reel was prepared, its time and song. Nothing happened → one short line.

## Weekly run (Sunday evening Karachi)

1. `git pull`. Drop entries from `schedule.json` whose slot is more than 14 days old.
2. Results of the last 7 days: `vidiq_instagram_owner_insights` (and `vidiq_ig_profile_reels` for public numbers). Compare moods, morning vs evening, Instagram songs vs our own music.
3. Write 14 new original quotes for the 7 days that start the day after the last slot already in `schedule.json` (7 morning 10:00, 7 evening 18:00), leaning toward what performed best. Never repeat a quote already used (check `weeks/`). Each entry: `id`, `scene` (one of road, rain, moon, mist, sunset, sunrise, city — vary them), `label` (one or two words, CAPS), `line1`, `line2` (short, the punch), `mood`. Save as `weeks/<first-date>_am.json` and `_pm.json`.
4. Render: `tools/make_reels.sh weeks/<first-date>_am.json <tmp> <new seed>` (and `_pm`). Look at every `_preview.png`; text must be easy to read on the background. Fix and re-render any that are not.
5. Copy MP4s to `media/w<week>_d<n>_am.mp4` / `_pm.mp4`, add 14 entries to `schedule.json` with `mood`, captions (engaging line + CTA to Save/Share/Comment, then `\n\nFollow @quotations_and_quotes for daily deep lines\n\n` + 5 relevant hashtags), `approved: true`, `posted: false`, `channel` (`metricool` for Monday–Friday 10:00, else `vidiq`, applying the monthly limit). Run `python3 tools/add_music.py`. Commit and push.
6. Song research (free, slow songs only) to refresh the pool for next week's Metricool mood groups. Commit and push `songs_pool.json`.
7. Send the owner: a short summary of last week's results, a contact sheet of the 14 previews, and a table of quotes + captions + music (Instagram song for Metricool reels, our track for the others) + where the songs came from. If he asks for changes, re-render those, update `schedule.json`, push and show them again.

## Post checklist (owner's standard)

Powerful, short, heart-touching quote · premium aesthetic + cinematic background matched to mood · grain, shadows, contrast · consistent fonts (Cormorant Garamond + DM Sans) and palette (cream + gold #E6B25C) · "QUOTATIONS & QUOTES" + handle watermark · readable on mobile, good spacing · 1080x1350 · engaging caption with CTA · relevant hashtags · original and share-/save-worthy.
