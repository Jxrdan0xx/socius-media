# Runbook: schedule the next Socius Instagram post

Run this whenever the scheduled task fires. It is idempotent: safe to run daily.

1. `git pull` this repo. Read `BRAND.md`, `TESTIMONIALS.md`, `moments.json` and `calendar.json`.
2. Pick the first post in `calendar.json` with `status: "todo"` whose `date` is within the next 3 days (Europe/London). If none, stop: nothing to do.
   - If a `todo` post's date/time is already in the past, mark it `"status": "skipped"` with a `note`, commit, and move to the next one.
3. Double-check Metricool (`getScheduledPosts`, brand 7429706) that nothing is already scheduled at that date/time. If something is, set status to `scheduled` and stop.
4. Research if needed (WebSearch/WebFetch), following the hard rules in BRAND.md. For live-role posts, read sociustalent.com/jobs.
5. If the post already has a `folder` with spec.json and caption.md (pre-built), skip to step 6 using those. Otherwise write `posts/<date>_<slug>/spec.json` (one post, id = `<slug>`, `theme` from the calendar entry, and never the same theme as the previous scheduled post) and `posts/<date>_<slug>/caption.md`.
6. Render: `python3 engine/build.py posts/<date>_<slug>/spec.json posts/<date>_<slug>/`. Check every slide image visually. Fix and re-render if anything is clipped or wrong.
7. Commit and push (`git config user.name Claude; git config user.email noreply@anthropic.com`). Confirm one image URL returns 200: `curl -sI <raw_base>posts/<date>_<slug>/<slug>_01.jpg`.
8. Schedule in Metricool with `createScheduledPost`:
   - `blogId` 7429706, provider instagram, `instagramData.type` POST, date/time from the calendar, timezone Europe/London.
   - `media`: raw GitHub URLs of the slides in order.
   - `autoPublish`: `false` if the post date ≤ `config.approval_until`, else `true`.
   - `text`: the caption.
8b. LinkedIn: always also schedule a separate LinkedIn post (provider linkedin) following `config.linkedin` (times, PDF-document format, rewritten caption). Same autoPublish rule. Record it under the post's `linkedin` key.
   Budget: follow `config.monthly_post_budget` (count this month's Metricool posts first). If Metricool still returns a plan/quota error, keep Instagram, skip LinkedIn, and tell Jordan in the summary.
9. Set the post's `status` to `scheduled`, add `metricool_id` and `planner_url`, commit and push.
10. Final message: one short summary for Jordan: post title, date/time, slide count, caption hook, planner link, and whether he needs to tap publish.

When fewer than 5 `todo` posts remain, draft the next 15 using the content mix and theme rules in BRAND.md, slotting in every relevant date from `moments.json` (verify event dates online first; add new conferences you find). About 10 posts per calendar month (one every ~3 days, within `config.monthly_post_budget`), rotating Instagram times 18:00 / 12:00 / 20:00. Append them as `todo` with a `theme`, and list the new topics in the summary so Jordan can veto any.

Photos: if Jordan has added new images to `posts/photos/`, plan a `photo` theme post around them within the next week.
