# @quotations_and_quotes — Instagram reels automation

This repo holds the reels for the Instagram account **@quotations_and_quotes** (owner: Sarmad, Pakistan, timezone **Asia/Karachi**). Talk to the owner in **Roman Urdu**, short and simple.

- `media/` — reels waiting to be posted (MP4, 1080x1350, 15 s, with our own background music). Deleted after they are posted.
- `schedule.json` — one entry per post: `slot` (Karachi time), `file`, `mood`, `sound`, `caption`, `approved`, `channel` (`metricool_notify` or `manual`; old entries `vidiq`/`metricool`), `sent_to_owner`, `ig_song`, `metricool_id`, `metricool_uuid`, `posted`, `permalink`.
- `songs_pool.json` — slow, relaxing Instagram-library songs per mood group, refreshed weekly (see "Song research").
- `sounds/` — our own original background tracks; `sounds/playlist.txt` lists the ones in use (1 lofi udaas piano, 3 bansuri cinematic, 4 romantic guitar, 5 slowed reverb sad). Made with `tools/sounds.py`.
- `weeks/` — the quote lists the reels were made from (daily files `<date>.json` since 18 Oct 2026).
- `tools/` — `make_reels.sh <posts.json> <out_dir> [seed]` renders silent reels in the house style; `add_music.py` gives each unposted reel without audio a random playlist track.

## How posting works (owner's decision, 18 Oct 2026: "Metricool notification, song khud lagaunga")

Two reels a day, **10:00 and 18:00 Karachi**, made **daily** (the evening before). **We never publish to Instagram ourselves.** The owner adds a trending song in the Instagram app and posts each reel himself.

- Each reel is scheduled in Metricool with **`autoPublish: false`** (manual publishing via notification) and **no `audioConfiguration`**, `channel: metricool_notify`. At the slot time the Metricool phone app notifies him; tapping it saves the video to his gallery and copies the caption; he opens Instagram, picks the video, adds a song, pastes the caption and posts. (The Instagram API cannot create Instagram drafts, so this is the closest to "draft".)
- Do **not** send the reels to the owner in advance (owner, 18 Oct: "kal ki video kal bhejna"); the Metricool notification at the slot time is the delivery.
- If Metricool refuses a post (e.g. the free plan's 20-a-month limit or an error), the Claude copy is the only delivery: `channel: manual`, note the error, and send a `PushNotification` "yeh reel manually Instagram par upload kar dein".
- Never publish through vidIQ or with `autoPublish: true`. Our own music stays inside every MP4 so the video has sound until he picks a song.

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
- **Only `audioType: "music"`** (Instagram's licensed library). Never use `original_sound` (other users' clips of songs): on 16 Oct 2026 such a song did not play and the reel went out silent. Famous film songs mostly exist only as `original_sound`, so pick slow licensed tracks (piano, acoustic, flute, sufi/instrumental, soft Hindi/Urdu indie).
- Pick only slow versions: titles with slowed / reverb / acoustic / unplugged / lofi / flute / nazm, or the original song if it is itself a slow ballad. **Never** pick titles with remix, DJ, house, mashup, party, phonk, bass boosted or similar.
- Save to `songs_pool.json` under its group: `{title, artist, audioId, audioType, library_title, source, found}`. Keep at most 6 per group, drop songs older than 45 days. The group's **top 3** = the newest three (most recently confirmed as trending). Reuse is fine.
- Do not call `vidiq_instagram_tiktok_outlier_search` or `vidiq_watch_shortform_content` for songs.

Test draft for library lookups: Metricool post uuid `7689021596470561225` (a draft, date 2026-10-30, never published). Get its current id with `getScheduledPosts`; update it with `draft: true`, `autoPublish: false`, keeping it a draft. A successful update attaches that audio to the draft (harmless) and changes its id.

## Daily run (~20:55 Karachi): make tomorrow's 2 reels

1. `git pull`. Drop entries from `schedule.json` whose slot is more than 14 days old (and `git rm` their media files).
2. Sundays only: results of the last 7 days with `vidiq_instagram_owner_insights` (and `vidiq_ig_profile_reels`); a short summary for the owner (moods, morning vs evening).
3. If tomorrow already has entries in `schedule.json`, skip to step 5. Otherwise write 2 new original quotes for tomorrow (10:00 and 18:00), leaning toward what performed best. Never repeat a quote already used (check `weeks/`). Each: `id`, `scene` (road, rain, moon, mist, sunset, sunrise, city; vary), `label` (one or two words, CAPS), `line1`, `line2`, `mood`. Save as `weeks/<date>.json`.
4. Render with `tools/make_reels.sh weeks/<date>.json <tmp> <new seed>` (pip install numpy/pillow/fonttools/scipy with `--break-system-packages` if missing; ffmpeg needed). Look at each `_preview.png`; fix and re-render anything hard to read. Copy MP4s to `media/<date>_am.mp4` / `_pm.mp4`; add entries (`mood`; caption = engaging line + CTA, then `\n\nFollow @quotations_and_quotes for daily deep lines\n\n` + 5 hashtags; `approved: true`, `posted: false`, `channel: metricool_notify`). Run `python3 tools/add_music.py`. Commit and push (the raw link must exist before Metricool fetches it).
5. Schedule every `metricool_notify` entry without a `metricool_uuid` (see "Scheduling in Metricool"). Failure → `channel: manual`, note the error.
6. Only for `manual` entries (Metricool refused them): send the MP4 to the owner with `SendUserFile` plus time, exact caption and a suggested trending slow song, and a `PushNotification`; set `sent_to_owner: true`. Commit and push.
7. Message the owner in one or two short Roman Urdu lines: tomorrow's 2 reels are set in Metricool (times, mood, a suggested trending slow song each), or which reel must be uploaded from the Claude copy. Sundays: add the weekly summary.

## Scheduling in Metricool

`createScheduledPost` (blogId `7403821`, date = slot with +05:00): `autoPublish: false`, `draft: false`, `media` = [raw GitHub link], `text` = exact caption, `providers` [instagram], `publicationDate` {slot, `Asia/Karachi`}, `instagramData` {`type: REEL`, `showReelOnFeed: true`} (no audioConfiguration). Save `metricool_id`, `metricool_uuid`.

## Post checklist (owner's standard)

Powerful, short, heart-touching quote · premium aesthetic + cinematic background matched to mood · grain, shadows, contrast · consistent fonts (Cormorant Garamond + DM Sans) and palette (cream + gold #E6B25C) · "QUOTATIONS & QUOTES" + handle watermark · readable on mobile, good spacing · 1080x1350 · engaging caption with CTA · relevant hashtags · original and share-/save-worthy.
