# Runbook: schedule the next Socius post (LinkedIn + Instagram/Facebook via Metricool, X via Typefully)

**Channel strategy (Jordan, 21 Oct 2026; details in `config.channel_strategy`):** business accounts only, never Jordan's personal profiles. Company voice ('we'), never 'I'. Priority: LinkedIn company page first, then X (use all 10 Typefully credits a month), then Instagram, with Facebook following Instagram.

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
8b. LinkedIn: always also schedule a separate LinkedIn post (provider linkedin) following `config.linkedin` (times, PDF-document format, rewritten caption). Same autoPublish rule. Record it under the post's `linkedin` key.
   Budget: follow `config.monthly_post_budget` (count this month's Metricool posts first). LinkedIn has priority: if the budget is tight or Metricool returns a plan/quota error, drop Facebook first, then Instagram, and keep LinkedIn. Tell Jordan in the summary.
   If LinkedIn scheduling fails because the network is disconnected or not on the plan, still schedule Instagram/Facebook and X, do NOT change config, and send Jordan a push notification straight away: LinkedIn is the top-priority channel and needs reconnecting.
8c. X: if `config.x.enabled`, schedule an X version in Typefully following `config.x` (thread for carousels, single post for statics; check publishing_quota first; if no quota left this month, skip X and say so). Record it under the post's `x` key. Never use publish_at="now". Goal is all 10 credits used every month: if remaining credits exceed the X posts still planned this month, add X-only entries to the calendar to use them.
9. Set the post's `status` to `scheduled`, add `metricool_id` and `planner_url`, commit and push.
10. Final message: one short summary for Jordan: post title, date/time, slide count, caption hook, planner link, and whether he needs to tap publish.

Events: follow 'Conferences and events method' in BRAND.md. When drafting a month, the first post is the 'Events this month' carousel, Tier 1 events get their 3 touches, Tier 2 events get one post.

When fewer than 5 `todo` posts remain, draft the next 15 using the content mix and theme rules in BRAND.md, slotting in every relevant date from `moments.json` (verify event dates online first; add new conferences you find). About 10 posts per calendar month (one every ~3 days, within `config.monthly_post_budget`), rotating Instagram times 18:00 / 12:00 / 20:00. Plan exactly 10 X posts per month (calendar X versions + X-only fill-ins), keeping room for live X posts during Tier 1 events. Avoid Friday LinkedIn live-roles posts (Jordan's personal Friday round-up covers roles). Append them as `todo` with a `theme`, and list the new topics in the summary so Jordan can veto any.

Photos: if Jordan has added new images to `posts/photos/`, plan a `photo` theme post around them within the next week.
