# @quotations_and_quotes — Instagram reels automation

This repo holds the reels for the Instagram account **@quotations_and_quotes** (owner: Sarmad, Pakistan, timezone **Asia/Karachi**). Talk to the owner in **Roman Urdu**, short and simple.

- `media/` — reels waiting to be posted (MP4, 1080x1350, 15 s, with our own background music). Deleted after they are posted.
- `schedule.json` — one entry per post: `slot` (Karachi time), `file`, `mood`, `sound`, `caption`, `approved`, `channel` (`metricool` or `manual`; old entries `vidiq`), `manual_sent`, `ig_song`, `metricool_id`, `metricool_uuid`, `posted`, `permalink`.
- `songs_pool.json` — slow, relaxing Instagram-library songs per mood group, refreshed weekly (see "Song research").
- `sounds/` — our own original background tracks; `sounds/playlist.txt` lists the ones in use (1 lofi udaas piano, 3 bansuri cinematic, 4 romantic guitar, 5 slowed reverb sad). Made with `tools/sounds.py`.
- `weeks/` — the quote lists the reels were made from (daily files `<date>.json` since 18 Oct 2026).
- `tools/` — `make_reels.sh <posts.json> <out_dir> [seed]` renders silent reels in the house style; `add_music.py` gives each unposted reel without audio a random playlist track.

## How posting works (owner's decision, 18 Oct 2026: "song ya manual")

Two reels a day, **10:00 and 18:00 Karachi**, owner's standing approval (`approved: true`). Reels are made **daily** (the evening before), not 14 at once.

- **Every reel goes through Metricool with a slow Instagram-library song** (`audioType: "music"`), own sound muted (`videoVolume: 0`), `channel: metricool`. The owner says reels with Instagram songs get much more reach than reels with our own music, so **vidIQ is no longer used for posting.**
- Metricool's free plan publishes at most **20 posts per calendar month**: count Metricool entries already scheduled or posted in that month; a 21st becomes `channel: manual`.
- **`channel: manual`**: when a reel cannot get a song in Metricool (over the limit, no song found, scheduling error, or Metricool did not publish it), do NOT post it anywhere. Send the owner the MP4 with `SendUserFile` (original quality), plus its time, exact caption and a suggested trending slow song for the mood (he adds the song in the Instagram app and uploads it himself), and a `PushNotification` saying "yeh reel manually Instagram par upload kar dein". Set `manual_sent: true` on the entry. Never post a manual entry ourselves.
- Our own music stays inside every MP4 (muted on Metricool), so the manual copies have sound until he picks a song.

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

1. `git pull`. Drop entries from `schedule.json` whose slot is more than 14 days old.
2. Sundays only: results of the last 7 days with `vidiq_instagram_owner_insights` (and `vidiq_ig_profile_reels`); a short summary for the owner (moods, morning vs evening, which songs).
3. If tomorrow already has entries in `schedule.json`, skip to step 5. Otherwise write 2 new original quotes for tomorrow (10:00 and 18:00), leaning toward what performed best. Never repeat a quote already used (check `weeks/`). Each: `id`, `scene` (road, rain, moon, mist, sunset, sunrise, city; vary), `label` (one or two words, CAPS), `line1`, `line2`, `mood`. Save as `weeks/<date>.json`.
4. Render with `tools/make_reels.sh weeks/<date>.json <tmp> <new seed>` (pip install numpy/pillow/fonttools/scipy with `--break-system-packages` if missing; ffmpeg needed). Look at each `_preview.png`; fix and re-render anything hard to read. Copy MP4s to `media/<date>_am.mp4` / `_pm.mp4`; add entries (`mood`; caption = engaging line + CTA, then `\n\nFollow @quotations_and_quotes for daily deep lines\n\n` + 5 hashtags; `approved: true`, `posted: false`, `channel: metricool`, or `manual` over the limit). Run `python3 tools/add_music.py`. Commit and push (the raw link must exist before Metricool fetches it).
5. Song research when the pool needs it (see "Song research").
6. Schedule each new `metricool` entry (see "Scheduling in Metricool"). Failure → `channel: manual`, note the error.
7. Deliver every `manual` entry not yet sent (see "How posting works"). Commit and push.
8. Message the owner in short Roman Urdu: the 2 quotes, their times, and each song (or that it was sent for manual upload). Sundays: add the weekly summary.

## Scheduling in Metricool

Song: from `songs_pool.json`, top 3 of the mood group, used least recently, not the same as the previous reel. `createScheduledPost` (blogId `7403821`, date = slot with +05:00): `autoPublish: true`, `draft: false`, `media` = [raw GitHub link], `text` = exact caption, `providers` [instagram], `publicationDate` {slot, `Asia/Karachi`}, `instagramData` {`type: REEL`, `showReelOnFeed: true`, `audioConfiguration` {`audioId`: numeric id, `videoVolume`: 0}}. The response must show `audioType: "music"`. Save `metricool_id`, `metricool_uuid`, `ig_song` {title, artist, audioId}.

## Check run (~10:20 and ~18:20 Karachi)

1. `git pull`; current time in Asia/Karachi.
2. Each `metricool` entry with `posted: false`, a `metricool_uuid`, slot more than 10 minutes past: `getScheduledPosts` for that day. Published → `posted: true`, `permalink` (publicUrl), `git rm` its media file. Still pending/failed → `channel: manual`, note the error, deliver it for manual upload.
3. Each `metricool` entry without a `metricool_uuid` (e.g. the daily run failed): slot more than 20 minutes away → schedule it now; otherwise, or if scheduling fails → `manual` and deliver it.
4. Commit and push. Message the owner only when a reel was published (permalink) or sent for manual upload; nothing to report → one short line.

## Post checklist (owner's standard)

Powerful, short, heart-touching quote · premium aesthetic + cinematic background matched to mood · grain, shadows, contrast · consistent fonts (Cormorant Garamond + DM Sans) and palette (cream + gold #E6B25C) · "QUOTATIONS & QUOTES" + handle watermark · readable on mobile, good spacing · 1080x1350 · engaging caption with CTA · relevant hashtags · original and share-/save-worthy.
