# @quotations_and_quotes — Instagram reels automation

This repo holds the reels for the Instagram account **@quotations_and_quotes** (owner: Sarmad, Pakistan, timezone **Asia/Karachi**). Talk to the owner in **Roman Urdu**, short and simple.

- `media/` — reels waiting to be posted (MP4, 1080x1350, 15 s, **no audio**: the owner adds a song from Instagram's music library when he posts). Deleted 3 days after their slot.
- `schedule.json` — one entry per post: `slot` (Karachi time), `file`, `mood`, `caption`, `approved`, `notified`, `songs`.
- `weeks/` — the quote lists each week's reels were made from.
- `tools/` — `make_reels.sh <posts.json> <out_dir> [seed]` renders silent reels in the house style (`premium.py` designs, `fonts/`).

Video links for the owner are GitHub raw links: `https://raw.githubusercontent.com/Sarmads050/reels/main/<file>`.

## How posting works (owner's choice, 13 Oct 2026)

The owner posts every reel himself so he can pick the song. Two reels a day, 10:00 and 18:00 Karachi. About 10 minutes before each slot a reminder run sends him a notification with the video link, the ready caption and **3 song suggestions** that fit that reel right now; he picks one and posts from the Instagram app. **Never publish to Instagram yourself** (no vidiq_instagram_publish_reel, no Metricool posts) unless the owner asks for that again in chat.

## Rules that never change

- Quotes are original (no copied poetry or lyrics), Roman Urdu, mood: sad / deep / reality / loneliness / mohabbat / sabr / dua / himmat / umeed.
- Song suggestions name the song and artist only; never quote lyrics.
- If anything fails, do not retry in a loop: note it on the entry (`"error"`), push, and tell the owner.
- Commits end with:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

## Reminder run (09:50 and 17:50 Karachi)

1. `git pull`. Get the current time with the time tool and convert to Asia/Karachi.
2. Pick the entry in `schedule.json` whose `slot` is within the next 40 minutes (or up to 30 minutes past) and that has no `notified: true`. None → also check whether the next week is missing (no entries for tomorrow) and tell the owner if so; otherwise stop quietly.
3. Find 3 songs for this reel. Use web search for what is trending on Instagram Reels in Pakistan/India right now (search with the month and year, e.g. "trending Instagram reels songs Pakistan <Month YYYY>", plus the reel's mood such as sad, romantic, sufi/spiritual, motivational). Pick 3 real, well-known Pakistani/Indian songs (Urdu/Hindi/Punjabi; sufi or naat-style instrumental for dua/sabr) that are likely in Instagram's music library and match the quote's mood. Prefer songs that are trending now; vary them from the songs suggested in the last 6 entries (`songs` field). For each: "Song – Artist" and a few words on why it fits.
4. Final message (this is what reaches his phone), in Roman Urdu:
   - Line 1: "Reel ka waqt: <time> — <mood>" and the quote.
   - **Video:** the raw GitHub link (tap → three dots → Download).
   - **Caption:** the exact caption in a code block so he can copy it.
   - **Gaane (3):** numbered list, best first.
   - **Steps:** Instagram → + → Reel → video chunein → Audio/Music → gaane ka naam search karein → acha hissa chunein → Next → caption paste → Share.
5. Save `notified: true` and `songs` on the entry. Also `git rm` media files whose slot is more than 3 days old. Commit and push.

## Weekly run (Sunday evening Karachi)

1. `git pull`. Drop entries from `schedule.json` whose slot is more than 14 days old.
2. Results of the last 7 days: `vidiq_instagram_owner_insights` (and `vidiq_ig_profile_reels` for public numbers). Compare moods, morning vs evening, and which songs went with the best reels. Keep vidIQ credit use under 15 per week.
3. Write 14 new original quotes for the 7 days that start the day after the last slot already in `schedule.json` (7 morning 10:00, 7 evening 18:00), leaning toward what performed best. Never repeat a quote already used (check `weeks/`). Each entry: `id`, `scene` (one of road, rain, moon, mist, sunset, sunrise, city — vary them), `label` (one or two words, CAPS), `line1`, `line2` (short, the punch), `mood`. Save as `weeks/<first-date>_am.json` and `_pm.json`.
4. Render: `tools/make_reels.sh weeks/<first-date>_am.json <tmp> <new seed>` (and `_pm`). Look at every `_preview.png`; text must be easy to read on the background. Fix and re-render any that are not.
5. Copy MP4s to `media/w<week>_d<n>_am.mp4` / `_pm.mp4`, add 14 entries to `schedule.json` with `mood` and captions (engaging line + CTA to Save/Share/Comment, then `\n\nFollow @quotations_and_quotes for daily deep lines\n\n` + 5 relevant hashtags), `approved: true` (the owner checks each reel himself when he posts it). Commit and push.
6. Send the owner: a short summary of last week's results, a contact sheet of the 14 previews, and a table of quotes + captions. If he asks for changes, re-render those, update `schedule.json`, push and show them again.

## Post checklist (owner's standard)

Powerful, short, heart-touching quote · premium aesthetic + cinematic background matched to mood · grain, shadows, contrast · consistent fonts (Cormorant Garamond + DM Sans) and palette (cream + gold #E6B25C) · "QUOTATIONS & QUOTES" + handle watermark · readable on mobile, good spacing · 1080x1350 · engaging caption with CTA · relevant hashtags · original and share-/save-worthy.
