# @quotations_and_quotes — Instagram reels automation

This repo holds the reels for the Instagram account **@quotations_and_quotes** (owner: Sarmad, Pakistan, timezone **Asia/Karachi**). Talk to the owner in **Roman Urdu**, short and simple.

- `media/` — reels waiting to be posted (MP4, **1080x1920 (9:16), 12 s, silent** since 18 Oct 2026; older ones 1080x1350 with music). Deleted after they are posted.
- `schedule.json` — one entry per post: `slot` (Karachi time), `file`, `mood`, `sound`, `caption`, `approved`, `channel` (`buffer_notify`, fallback `metricool_notify` or `manual`; old entries `vidiq`/`metricool`/`buffer`), `buffer_id`, `sent_to_owner`, `ig_song`, `metricool_id`, `metricool_uuid`, `posted`, `permalink`.
- `songs_pool.json` — slow, relaxing Instagram-library songs per mood group, refreshed weekly (see "Song research").
- `sounds/` — our own original background tracks; `sounds/playlist.txt` lists the ones in use (1 lofi udaas piano, 3 bansuri cinematic, 4 romantic guitar, 5 slowed reverb sad). Made with `tools/sounds.py`.
- `weeks/` — the quote lists the reels were made from (daily files `<date>.json` since 18 Oct 2026).
- `tools/` — `make_reels.sh <posts.json> <out_dir> [seed]` renders silent reels in the house style (`reel916.py`; scenes come from `premium.py`). `add_music.py` (old, for the 15 s music reels) is **not used any more**: do not run it.

## How posting works (owner's decision, 27 Oct 2026: "buffer se mujhy notifications bhej dia karein")

Two reels a day, **10:00 and 18:00 Karachi**, made **daily** (the evening before). **We never publish to Instagram ourselves.** The owner adds a song in the Instagram app and posts each reel himself.

- **No auto posting** (owner, 27 Oct 2026): a Buffer auto-post test on 27 Oct showed Instagram does not let him add a song after a reel is posted. Never Buffer `schedulingType: automatic`, never Metricool `autoPublish: true`, never vidIQ publishing. (Instagram API cannot create Instagram drafts either.)
- **Delivery = Buffer reminder** (`channel: buffer_notify`): Buffer org `6ae0788be586811d71fdec73`, Instagram channel `6ae07a3a2f1f5ed648e8755e`. Each reel: `create_post` with **`schedulingType: notification`**, `mode: customScheduled`, `dueAt` = slot with +05:00, `text` = exact caption, `assets` [{video: {url: raw GitHub link}}], `metadata.instagram` {`type: reel`, `shouldShareToFeed: true`}. Save the id as `buffer_id`. At the slot the Buffer phone app notifies him; tapping it saves the video and copies the caption; he adds a song in Instagram and posts. Free plan: max 10 scheduled posts at a time (no monthly cap); we only schedule tomorrow's 2.
- Fallback if Buffer refuses: Metricool notification (`autoPublish: false`, see "Scheduling in Metricool", `channel: metricool_notify`; 20 a month, renews on the 1st). Never schedule the same reel in both.
- If both refuse: `channel: manual`, send the MP4 + exact caption with `SendUserFile` and a `PushNotification` "yeh reel manually Instagram par upload kar dein".
- Do **not** send reels to the owner in advance when Buffer/Metricool accepted them (owner, 18 Oct: "kal ki video kal bhejna").
- Reels are **silent** (owner, 18 Oct); he adds an Instagram song himself when posting.

Video URLs (all channels) are GitHub raw links: `https://raw.githubusercontent.com/Sarmads050/reels/main/<file>`.
Metricool brand id `7403821`. vidIQ account `quotations_and_quotes`.

## Rules that never change

- Never post the same entry twice. If anything fails, do not retry in a loop: record `"error"` on the entry, push, and tell the owner.
- Only post entries with `approved: true`. If the owner ever asks to check reels before posting, set new entries to `approved: false` until he says yes.
- Quotes are in Roman Urdu and follow "Topics" and "Famous lines first" below: famous lines only from **public-domain** classical poets or verified sayings, always credited; otherwise our own original lines. Never song lyrics, never lines of modern copyrighted poets.
- Our video files are silent (older ones contain only tracks from `sounds/`). Songs are added only through Instagram's own music library; never download a song or put it into a file.
- **No reel goes out without music**: the owner adds the Instagram song himself when he posts.
- vidIQ credits are limited (150 a month). Song research uses **no** vidIQ credits (owner's rule).
- Instagram songs must be **slow and relaxing** (owner's rule).
- Commits end with:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

## Topics (owner's decision, 18 Oct 2026, from the topic research)

Weekly mix of 14 reels (`topic` field). **Owner's decision, 25 Oct 2026: "sab se ziyada umeed, hosla, acha time aayega, na-umeed nahi karo, sab ke saath acha karo… aaj kal log bohat depression ke shikar hain."** So most reels lift people up. Weekday → 10:00 / 18:00:

| Day | 10:00 | 18:00 |
|---|---|---|
| Saturday | umeed (acha waqt aayega) | tanhai / deep (ending with hope) |
| Sunday | hosla / himmat | sab ke saath acha karo (kindness, naiki) |
| Monday | umeed (mushkil guzar jayegi) | mohabbat |
| Tuesday | hosla / khud par yaqeen | reality / self-respect (positive turn) |
| Wednesday | sabr (achha waqt aayega) | sab ke saath acha karo |
| Thursday | umeed / na-umeed mat ho | maa / family (odd ISO weeks), dosti (even ISO weeks) |
| Friday | Juma dua (our own original dua lines) | hosla / himmat |

- 10 of 14 reels are hope / courage / kindness. The others (tanhai, mohabbat, reality, family) must also **end with hope or warmth**: never hopeless, never "zindagi bekaar hai", nothing about giving up, death wishes or self-harm.
- Tone: like a kind friend telling someone who is sad or depressed "ruk jao, acha waqt aayega, tum akele nahi ho". Simple words, warm, sendable.

Write lines that speak **to someone** (so people send them). Seasonal: December → keep the same hopeful mix (winter loneliness: "tum akele nahi ho"); Ramadan 2027 (about 8 Feb–9 Mar, confirm moon sighting) → more dua/sabr/shukr reels (our own lines, no Quran/hadith), plus Eid reels; 14 August → one Pakistan reel. Every 4 weeks, check Insights (sends, saves, likes per 1,000 reach by topic) and tell the owner which topic to give one more slot.

## Famous lines first (owner's decision, 18 Oct 2026)

For every topic, first use **famous lines by well-known people** on that topic; only when no new verified famous line fits, write our own original line (researching the topic first).
- Allowed: classical poets who died more than 50 years ago (public domain in Pakistan), e.g. Mirza Ghalib, Mir Taqi Mir, Allama Iqbal, Daagh Dehlvi, Momin, Zauq, Akbar Allahabadi, Bulleh Shah, Sultan Bahu, Khwaja Ghulam Farid, Hali, Nazeer Akbarabadi.
- **No Quran reels** (owner, 25 Oct 2026: "Quran ki reel nhi banow"): never use Quran ayaat or their translation/meaning on a reel, also not for spiritual/Juma/sabr topics or in Ramadan; use poets or our own original lines instead.
- **No hadith and no sayings of religious figures** (owner, 25 Oct 2026: "koi hadees na rakho, maloom nahi wo original hai ya nahi"): no hadith, no "Hazrat Ali ne farmaya", no saying of any sahabi, imam or saint. Only classical poets' verified couplets or our own original lines.
- **Not allowed** (copyright): modern poets, e.g. Faiz Ahmed Faiz, Jaun Elia, Ahmad Faraz, Parveen Shakir, Mohsin Naqvi, Wasi Shah, Tehzeeb Hafi, Ali Zaryoun, Gulzar, Javed Akhtar, and any song lyrics. If unsure whether a poet died 50+ years ago, do not use them.
- **Verify every famous line** before using it: exact wording and poet on rekhta.org . Many lines shared online are misattributed: if the line or the attribution cannot be confirmed, do not use it. Save the link as `source`.
- Show the poet/source on the reel (`author`, e.g. "Mirza Ghalib", "Allama Iqbal") and in the caption's first line. Use the couplet in Roman Urdu exactly as verified (line1 = first misra, line2 = second misra).
- Keep a list of famous lines already used in `famous_used.json` ({text, author, source, date}) and never repeat one.

## Mood groups

- `sad`: reality, deep, zindagi, tanhai, dil ki baat, yaadein, sad lines
- `romantic`: mohabbat, love, yaadein (romantic)
- `spiritual`: sabr, dua, Juma, Allah, faith
- `hope`: himmat, umeed, hosla, acha waqt aayega, sab ke saath acha karo (kindness), safar, motivation

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
3. If tomorrow already has entries in `schedule.json`, skip to step 5. Otherwise pick tomorrow's 2 topics from "Topics" (by weekday) and write the 2 quotes following "Famous lines first". Never repeat a quote already used (check `weeks/` and `schedule.json`). Each: `id`, `scene` (sunset, mist, sunrise, road, city, rain; vary, never the same as the previous reel), `label` (one or two words, CAPS), `line1`, `line2`, `mood`, `topic`, and for famous lines `author` (shown on the reel as "— <author>") and `source` (the verification link). Save as `weeks/<date>.json`.
4. Render with `tools/make_reels.sh weeks/<date>.json <tmp> <new seed>` (pip install numpy/pillow/fonttools/scipy with `--break-system-packages` if missing; ffmpeg needed). Look at each `_preview.png`; fix and re-render anything hard to read. Copy MP4s to `media/<date>_am.mp4` / `_pm.mp4`; add entries (`mood`, `scene`, caption in the format under "Captions"; `approved: true`, `posted: false`, `channel: buffer_notify`). Do not run `add_music.py`. Commit and push (the raw link must exist before Buffer fetches it).
5. Schedule every `buffer_notify` entry without a `buffer_id` as a Buffer reminder (see "How posting works"). Buffer failure → Metricool notification (`channel: metricool_notify`); that failing too → `channel: manual`, note the errors.
6. Only for `manual` entries (Buffer and Metricool refused them): send the MP4 to the owner with `SendUserFile` plus time, exact caption and a suggested trending slow song, and a `PushNotification`; set `sent_to_owner: true`. Commit and push.
7. Message the owner in one or two short Roman Urdu lines: tomorrow's 2 reels are set as Buffer reminders (times, mood, a suggested slow song each), or which reels he must upload from the Claude copy. Sundays: add the weekly summary.

## Scheduling in Metricool (fallback)

`createScheduledPost` (blogId `7403821`, date = slot with +05:00): `autoPublish: false`, `draft: false`, `media` = [raw GitHub link], `text` = exact caption, `providers` [instagram], `publicationDate` {slot, `Asia/Karachi`}, `instagramData` {`type: REEL`, `showReelOnFeed: true`} (no audioConfiguration). Save `metricool_id`, `metricool_uuid`.

## Captions

```
<Mood> | Roman Urdu shayari — <one new line that adds to the quote, with searchable words>. (Famous line: "<Mood> | <Author> ki shayari — ...")
<share CTA, e.g. "Jise yaad karte ho, usay yeh reel bhej do 💌" / "Us dost ko bhejo jo yeh samjhega">

Roz aisi lines ke liye follow karein @quotations_and_quotes

<5 hashtags: niche Roman-Urdu tags first, e.g. #urdushayari #sadshayari #romanurdu + mood tag + #urduquotes>
```
The share CTA goes **only in the caption, never on the video** (owner, 18 Oct). Prefer "bhejo/share" CTAs over "save karo". Max 5 hashtags (Instagram limit since Dec 2025).

## Post checklist (owner's standard, design "E" approved 18 Oct 2026)

Powerful, short, heart-touching, original quote that people want to **send** to someone · **1080x1920 (9:16)**, 12 s, silent, loops (no fade-out) · **light background**, a **different scene every reel** (sunset, mist, sunrise, road, city, rain; avoid moon with short quotes — the moon sits behind the label) · line 1 visible from frame 0, line 2 rises in at ~2 s · fonts **Lora Bold** (line 1, ink #211A16) + **Lora Italic** (line 2, maroon #7A2228); label, quote mark and divider maroon; no script/stylish fonts · watermark: only `@quotations_and_quotes` (no "QUOTATIONS & QUOTES") · text **exactly centred** (centre x 540; owner, 19 Oct 2026) inside the safe zone (x 150–930, y 300–1250) · readable on mobile · caption per "Captions".
