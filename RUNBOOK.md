# Runbook: schedule the next Socius post (LinkedIn via Buffer, Instagram/Facebook via Metricool, X via Typefully)

**Channel strategy (Jordan, 21 Oct 2026, updated 4 Nov; details in `config.channel_strategy`):** this runbook covers business accounts only. Jordan's personal LinkedIn and personal X get only the Wednesday candidate spotlight and Friday roles round-up, which have their own scheduled tasks. Company voice ('we'), never 'I'. Priority: LinkedIn company page first, then X (use all 10 Typefully credits a month), then Instagram, with Facebook following Instagram.

Run this whenever the scheduled task fires. It is idempotent: safe to run daily.

1. `git pull` this repo. Read `BRAND.md`, `TESTIMONIALS.md`, `moments.json` and `calendar.json`.
2. Pick the first post in `calendar.json` with `status: "todo"` whose `date` is within the next 3 days (Europe/London). If none, stop: nothing to do.
   - Entries with `channels: ["x"]` are X-only: skip slides/Metricool, write the post(s) in the folder's caption.md (or straight from the topic), schedule in Typefully per step 8c, record under `x`, set status `scheduled`.
   - If a `todo` post's date/time is already in the past, mark it `"status": "skipped"` with a `note`, commit, and move to the next one.
3. Double-check Metricool (`getScheduledPosts`, brand 7429706) that nothing is already scheduled at that date/time. If something is, set status to `scheduled` and stop.
4. Research if needed (WebSearch/WebFetch), following the hard rules in BRAND.md. For live-role posts, read sociustalent.com/jobs.
5. If the post already has a `folder` with spec.json and caption.md (pre-built), skip to step 6 using those. Otherwise write `posts/<date>_<slug>/spec.json` (one post, id = `<slug>`, `theme` from the calendar entry; before rendering, re-check THE VARIETY RULE in BRAND.md against the last 3 scheduled/published posts and change the theme if it would clash) and `posts/<date>_<slug>/caption.md`.
6. Render: `python3 engine/build.py posts/<date>_<slug>/spec.json posts/<date>_<slug>/`. Check every slide image visually. Fix and re-render if anything is clipped or wrong.
7. Commit and push (`git config user.name Claude; git config user.email noreply@anthropic.com`). Confirm one image URL returns 200: `curl -sI <raw_base>posts/<date>_<slug>/<slug>_01.jpg`.
8. Schedule in Metricool with `createScheduledPost`. Do the LinkedIn post (8b) FIRST, then Instagram/Facebook:
   - `blogId` 7429706, providers instagram + facebook (if `config.facebook.enabled`, same post; add `facebookData: {type: POST}`), `instagramData.type` POST, date/time from the calendar, timezone Europe/London.
   - `media`: raw GitHub URLs of the slides in order.
   - `autoPublish`: always `true` (see config.approval_note; false means manual posting by Jordan).
   - `text`: the caption.
8b. **LinkedIn company page goes via Buffer (since 4 Nov 2026)**, following `config.linkedin` and `config.buffer`. Do it FIRST, before Instagram/Facebook.
   - Build `linkedin.pdf` from the slide JPGs (PIL) if missing, push it, then run (BUFFER_API_KEY comes from the scheduled-task prompt; never write it to the repo):
     `python3 engine/buffer_post.py create --channel socius_li --text-file <linkedin caption file> --due "YYYY-MM-DD HH:MM" --document <raw>/linkedin.pdf --doc-title "<title>" --thumb <raw>/<slug>_01.jpg`
     (single image: `--image <raw>/<slug>_01.jpg` instead of the document flags).
   - The caption must contain NO URL and no 'link in the comments' (Buffer free has no first comment). End with a soft CTA ('Send us a message', 'DM us').
   - Record under the post's `linkedin` key: status scheduled, buffer_id, date. Before creating, `list --channel socius_li` to make sure the slot isn't already taken.
   - If Buffer errors (limit reached, channel disconnected), still schedule Instagram/Facebook and X, and tell Jordan in a push notification straight away.
   Metricool budget: follow `config.monthly_post_budget` (count this month's Metricool posts first; LinkedIn no longer uses it). If tight, drop Facebook first. Never schedule LinkedIn in Metricool.
8c. X: if `config.x.enabled`, schedule an X version in Typefully following `config.x` (thread for carousels, single post for statics; check publishing_quota first; if no quota left this month, skip X and say so). Record it under the post's `x` key. Never use publish_at="now". Goal is all 10 credits used every month: if remaining credits exceed the X posts still planned this month, add X-only entries to the calendar to use them.
9. Set the post's `status` to `scheduled`, add `metricool_id` and `planner_url`, commit and push.
9b. When using `updateScheduledPost` (clean-up fixes), always send `providers` exactly as they were (a LinkedIn post stays `[linkedin]` only) and `publicationDate.dateTime` in Europe/London local time. Re-read with `getScheduledPosts` afterwards and confirm providers and time are unchanged. (27 Oct update added an Instagram provider and shifted the time by an hour.)
10. Final message: one short summary for Jordan: post title, date/time, slide count, caption hook, planner link, and whether he needs to tap publish.

Events: follow 'Conferences and events method' in BRAND.md. When drafting a month, the first post is the 'Events this month' carousel, Tier 1 events get their 3 touches, Tier 2 events get one post.

When fewer than 5 `todo` posts remain, draft the next 15 using the content mix and theme rules in BRAND.md, slotting in every relevant date from `moments.json` (verify event dates online first; add new conferences you find). About 10 posts per calendar month (one every ~3 days, within `config.monthly_post_budget`), rotating Instagram times 18:00 / 20:00 (12:00 dropped after the Oct 2026 review: noon posts had the lowest reach; revisit monthly). Plan exactly 10 X posts per month (calendar X versions + X-only fill-ins), keeping room for live X posts during Tier 1 events. Avoid Friday LinkedIn live-roles posts (Jordan's personal Friday round-up covers roles). Append them as `todo` with a `theme`, and list the new topics in the summary so Jordan can veto any.

Photos: if Jordan has added new images to `posts/photos/`, plan a `photo` theme post around them within the next week.
