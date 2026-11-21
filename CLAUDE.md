# @quotations_and_quotes — Instagram reels automation

This repo holds the reels for the Instagram account **@quotations_and_quotes** (owner: Sarmad, Pakistan, timezone **Asia/Karachi**). Talk to the owner in **Roman Urdu**, short and simple.

- `media/` — reels waiting to be posted (MP4, **1080x1920 (9:16), 12 s, silent** since 18 Oct 2026; older ones 1080x1350 with music). Deleted after they are posted.
- `schedule.json` — one entry per post: `slot` (Karachi time), `file`, `mood`, `sound`, `caption`, `approved`, `channel` (`gmail`, fallback `manual`; old entries `buffer_notify`/`metricool_notify`/`vidiq`/`metricool`/`buffer`), `gmail_id`, `buffer_id`, `sent_to_owner`, `ig_song`, `metricool_id`, `metricool_uuid`, `posted`, `permalink`.
- `songs_pool.json` — slow, relaxing Instagram-library songs per mood group, refreshed weekly (see "Song research").
- `sounds/` — our own original background tracks; `sounds/playlist.txt` lists the ones in use (1 lofi udaas piano, 3 bansuri cinematic, 4 romantic guitar, 5 slowed reverb sad). Made with `tools/sounds.py`.
- `weeks/` — the quote lists the reels were made from (daily files `<date>.json` since 18 Oct 2026).
- `tools/` — `make_reels.sh <posts.json> <out_dir> [seed]` renders silent reels in the house style (`reel916.py`; scenes come from `premium.py`). `add_music.py` (old, for the 15 s music reels) is **not used any more**: do not run it.

## How posting works (owner's decision, 21 Nov 2026: reels by Gmail)

Two reels a day, **10:00 and 18:00 Karachi**. Each reel is made shortly before its slot (~09:47 and ~17:47, see "Daily runs") and **emailed to the owner's Gmail**. **We never publish to Instagram ourselves.** He downloads the video, adds a song in the Instagram app and posts it.

- **Why Gmail** (owner, 21 Nov 2026): the Metricool free plan ran out (every reminder from 18 Nov 18:00 on shows "You have reached your Metricool account limit", so nothing reached his phone) and Buffer reminders did not reach his phone on 7–8 Nov. WhatsApp has no free connector; Telegram is blocked from this sandbox. He chose Gmail.
- **Email** (`channel: gmail`): Gmail `send_message` to the owner's own address (the session's user email). Subject exactly `[Reel] <D Mon> subah 10 baje - <Label>` or `[Reel] <D Mon> shaam 6 baje - <Label>`. Plain-text body: (1) the raw GitHub download link, (2) "Instagram par upload karein, slow song lagayein (mashwara: <song>)", (3) the exact caption, (4) "(Yeh email 5 din baad khud delete ho jayegi.)". **Never attach the MP4** (link only, so the mailbox never fills up). Save the message id as `gmail_id`, set `sent_to_owner: true`.
- **Cleanup every run**: `search_threads` with `subject:"[Reel]" older_than:5d` (from/to his own address) and `trash_thread` each result. Only threads with the `[Reel]` subject; never touch any other email.
- **No auto posting** (owner, 27 Oct 2026): Instagram does not let him add a song after a reel is posted. Never Buffer `schedulingType: automatic`, never Metricool `autoPublish: true`, never vidIQ publishing.
- Do not use Metricool or Buffer reminders any more (old entries keep their `metricool_*`/`buffer_id` fields as history).
- If Gmail fails: `channel: manual`, send the MP4 + exact caption with `SendUserFile` and a `PushNotification` "yeh reel manually Instagram par upload kar dein".
- Send each reel only at its own time (owner, 18 Oct: "kal ki video kal bhejna"): never email tomorrow's reel today.
- Reels are **silent** (owner, 18 Oct); he adds an Instagram song himself when posting.
- Note: Telegram works for the nf-updates repo through its GitHub Actions workflow `tg-notify.yml`; if the owner ever wants reels on Telegram, the same approach could be set up here.

Video URLs (all channels) are GitHub raw links: `https://raw.githubusercontent.com/Sarmads050/reels/main/<file>`.
Metricool brand id `7403821`. vidIQ account `quotations_and_quotes`.

## Rules that never change

- Never post the same entry twice. If anything fails, do not retry in a loop: record `"error"` on the entry, push, and tell the owner.
- Only post entries with `approved: true`. If the owner ever asks to check reels before posting, set new entries to `approved: false` until he says yes.
- Quotes are in Roman Urdu, our **own original simple lines** (see "Our own simple lines"); Allama Iqbal banned; no famous couplets unless the owner asks. Never song lyrics, never lines of modern copyrighted poets.
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

## Our own simple lines (owner's decision, 30 Oct 2026 — replaces "Famous lines first")

Owner, 30 Oct 2026: "Allama Iqbal ki banana ban karo, apni taraf se quotes banow jo asan ho or humans feel bhi kar pay" — Iqbal's (and other classical poets') couplets were too hard for normal people to understand.

- **Every reel uses our own original line.** No famous couplets from classical poets (Allama Iqbal, Mirza Ghalib, Mir Taqi Mir, Daagh, Momin, etc.) unless the owner asks for one again.
- **Allama Iqbal is banned completely** — never his lines, never "Iqbal ki shayari" in a caption.
- Still no Quran, no hadith, no sayings of religious figures, no modern poets, no song lyrics (owner, 25 Oct 2026).
- **Easy words:** everyday Roman Urdu that a normal person (school level, no Persian/Arabic heavy words) understands on first read. Avoid words like khudi, shaheen, kisht-e-veeran, mohkam, paiham, khugar, visal, mayassar, jahan-e-digar. Test: if a 15-year-old would need to ask "iska matlab kya hai?", rewrite it.
- **Feelable:** speak to the reader about something they live through (thakan, akelapan, intezaar, ghar, maa, dost, mehnat, dua), like a kind friend. Short: line1 max ~8 words, line2 max ~10 words. Concrete images (raat, chai, barish, safar, darwaza) are better than abstract ideas.
- Before writing, check `weeks/` and `schedule.json` so a line or idea is never repeated.
- No `author` on the reel (our lines carry only the `@quotations_and_quotes` watermark). Caption first line: "<Mood> | Roman Urdu shayari — ...".
- `famous_used.json` stays as history only; nothing new is added to it.

### Emotional connect first (owner, 14 Nov 2026)

Owner, 14 Nov 2026, about the 14 Nov 18:00 reel ("Phone mein koi message nahi aaya na? / Phir bhi kisi ki dua mein tumhara naam zaroor hai."): "yeh quote acha nahi, log isay connect nahi kar payenge… aesay quote banow jisay log emotionally connect kar payein." Reels are for common people.

- The line must make the reader think **"yeh to meri baat hai"** in the first second. Write about a hidden feeling many people carry but rarely say: smiling in front of everyone and crying alone, being the strong one at home, hiding tiredness from parents, nobody asking "tum theek ho?", overthinking at night, giving everything and not being valued, parents' quiet sacrifices, missing home, waiting for someone.
- **Line 1 names that real moment/feeling** (specific, true-to-life, not a random detail). **Line 2 gives the emotional turn**: recognition ("main samajhta hoon"), comfort or hope, said like a close friend. It must hit the heart, not just be "nice" or clever.
- Avoid: trivial or odd details (phone messages, notifications), vague/abstract comfort ("kisi ki dua mein naam", "kahani baaki hai", "mausam badal jata hai") and generic nature metaphors (suraj, beej, diya, mausam) unless the feeling itself is clear and personal.
- Self-test before rendering: would a normal person screenshot this and send it to someone saying "bilkul sach"? If not, rewrite.
- Examples of the target style: "Raat ko ro kar bhi, / subah phir uth jaate ho na? Yahi asli himmat hai." · "Ghar walon ke saamne theek rehte ho, / sirf tumhara takiya jaanta hai tum kitne thake ho."

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

## Daily runs (owner, 21 Nov 2026: Gmail delivery; each reel made just before its slot)

### Morning run (~09:47 Karachi): today's 10:00 reel

1. `git pull`. Drop entries from `schedule.json` whose slot is more than 14 days old (and `git rm` their media files). Trash `[Reel]` emails older than 5 days (see "How posting works").
2. Sundays only: results of the last 7 days with `vidiq_instagram_owner_insights` (and `vidiq_ig_profile_reels`); a short summary for the owner (moods, morning vs evening).
3. If today's 10:00 entry already has `gmail_id` (or `sent_to_owner: true`), stop. If it exists without one, skip to step 5. Otherwise take today's 10:00 topic from "Topics" (by weekday) and write the quote following "Our own simple lines". Never repeat a line (check `weeks/` and `schedule.json`). Fields: `id` (`<date>_am`), `scene` (sunset, mist, sunrise, road, city, rain; never the same as the previous reel), `label`, `line1`, `line2`, `mood`, `topic`. Save as `weeks/<date>.json` (a list).
4. Render with `tools/make_reels.sh <json with just this item> <tmp> <new seed>` (pip install numpy/pillow/fonttools/scipy with `--break-system-packages` if missing). Look at the `_preview.png`; fix anything hard to read. Copy to `media/<date>_am.mp4`; add the entry (caption per "Captions"; `approved: true`, `posted: false`, `channel: gmail`). Commit and push, and check the raw link returns 200.
5. Email it (see "How posting works"), save `gmail_id`, `sent_to_owner: true`, commit, push.
6. One short Roman Urdu line: "Subah 10 baje wali reel Gmail par bhej di" + the line and a suggested slow song (Sundays: add the weekly summary).

### Evening run (~17:47 Karachi): today's 18:00 reel

1. `git pull`. Trash `[Reel]` emails older than 5 days. If today's 18:00 entry already has `gmail_id` (or `sent_to_owner: true`), stop (say nothing).
2. If today's 10:00 reel was never sent (morning run failed): make/send it too, same way.
3. If today's 18:00 entry does not exist: take today's 18:00 topic from "Topics", write the line (never repeat; scene different from the 10:00 reel), append it (`id` `<date>_pm`) to `weeks/<date>.json`, render, check the preview, copy to `media/<date>_pm.mp4`, add the entry (`channel: gmail`), commit, push, check the raw link.
4. Email it, save `gmail_id`, commit, push. Gmail failing → `channel: manual` (see above).
5. One short Roman Urdu line: "Shaam 6 baje wali reel Gmail par bhej di" (+ the line and a suggested slow song).

## Scheduling in Metricool (not used since 21 Nov 2026; kept for reference)

`createScheduledPost` (blogId `7403821`, date = slot with +05:00): `autoPublish: false`, `draft: false`, `media` = [raw GitHub link], `text` = exact caption, `providers` [instagram], `publicationDate` {slot, `Asia/Karachi`}, `instagramData` {`type: REEL`, `showReelOnFeed: true`} (no audioConfiguration). Save `metricool_id`, `metricool_uuid`.

## Captions

```
<Mood> | Roman Urdu shayari — <one new line that adds to the quote, with searchable words>.
<share CTA, e.g. "Jise yaad karte ho, usay yeh reel bhej do 💌" / "Us dost ko bhejo jo yeh samjhega">

Roz aisi lines ke liye follow karein @quotations_and_quotes

<5 hashtags: niche Roman-Urdu tags first, e.g. #urdushayari #sadshayari #romanurdu + mood tag + #urduquotes>
```
The share CTA goes **only in the caption, never on the video** (owner, 18 Oct). Prefer "bhejo/share" CTAs over "save karo". Max 5 hashtags (Instagram limit since Dec 2025).

## Post checklist (owner's standard, design "E" approved 18 Oct 2026)

Powerful, short, heart-touching, original quote that people want to **send** to someone · **1080x1920 (9:16)**, 12 s, silent, loops (no fade-out) · **light background**, a **different scene every reel** (sunset, mist, sunrise, road, city, rain; avoid moon with short quotes — the moon sits behind the label) · line 1 visible from frame 0, line 2 rises in at ~2 s · fonts **Lora Bold** (line 1, ink #211A16) + **Lora Italic** (line 2, maroon #7A2228); label, quote mark and divider maroon; no script/stylish fonts · watermark: only `@quotations_and_quotes` (no "QUOTATIONS & QUOTES") · text **exactly centred** (centre x 540; owner, 19 Oct 2026) inside the safe zone (x 150–930, y 300–1250) · readable on mobile · caption per "Captions".
