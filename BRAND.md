# Socius Talent: Instagram brand guide

## Who we are
Socius Talent (@sociustalent) is a specialist recruitment partner for Web3, blockchain, crypto and AI companies. Founder: Jordan. Tagline: **Partners in building the future.**
- Hiring teams → sociustalent.com/talent
- Candidates → sociustalent.com/jobs
- Instagram links are not clickable: always say "link in bio" and/or "DM us".

## Audience
Both, with emphasis on business growth: founders, CTOs, heads of engineering and talent leaders (primary), plus Web3/AI professionals.

## Voice
- UK English. Confident, direct, specialist. A peer to founders, not a salesman.
- Short sentences. No hype words ("revolutionary", "game-changing"), no engagement bait.
- Company voice on every channel ("we", never "I"). We post from business accounts only.
- Captions: hook line first, 3–6 short paragraphs, one clear CTA, 4–6 relevant hashtags at the end.
- Avoid em dashes in captions; use commas, colons or full stops.

## Hard rules (never break)
1. **Never invent facts**: no fake stats, placements, client names, salaries, testimonials or quotes. If a claim needs a number, either use a verifiable public source (and keep it general) or leave the number out.
2. **Live roles**: only roles currently listed at sociustalent.com/jobs, with title, sector, location and salary exactly as listed. If the jobs page can't be read, swap the post for an evergreen hiring-intelligence topic instead.
3. **Testimonials**: only from `TESTIMONIALS.md`, word for word (trim with "…", fix typos only). Use the `quote` slide type. Credit full name + role as listed. Never reuse one within 6 weeks.
4. **Never state how many roles we have** (no '25 live roles', 'six of 25', counts on slides or in captions). Showcase individual roles only. Socius is a boutique; totals look made up.
5. **No links in the body of LinkedIn or X posts** (they cut reach). LinkedIn: put the link in the first comment (Metricool `firstCommentText`). X: put the link in the final reply of the thread only, never in the first post. Instagram: 'link in bio'.
6. Holidays are welcome (Jordan's audience is global), but keep them on-brand and short. Never post generic stock-style holiday art.
7. Events/conferences: never claim Socius is attending, speaking or hosting unless Jordan has said so (see `config.confirmed_events` in calendar.json). Confirmed: Jordan is attending Solana Breakpoint 2026, London, 15–17 Nov.

## Content mix (rough targets)
- Hiring intelligence (founders/CTOs): 25%
- Culture & moments: 20%. Crypto history days, big industry news, conferences (who's going?), holidays. See `moments.json`.
- Candidate value: 15%
- Conversation: 10%. 'Settle this' polls, hot takes, questions that get comments.
- Live opportunities: 15%
- Proof (testimonials, Socius story, behind the scenes): 15%
Never two posts of the same pillar back to back. Testimonials at most 1 in 6 posts.

## Design: variety is a rule
Rendered by `engine/build.py` (1080×1350 JPEG). Write a spec JSON; don't hand-design. See `engine/showcase_spec.json`.
- **Themes (7)**: `midnight` (house navy glow), `light` (cream editorial + serif), `gradient` (bold brand gradient), `terminal` (black mono, crypto/tech), `white` (Swiss poster: white, huge black type, purple accent), `frame` (gradient border + white card), `photo` (Jordan's real photos from `posts/photos/`). Samples: `engine/showcase_spec.json`.
- **THE VARIETY RULE (Jordan's top priority, never break):** the feed must never look copy-and-pasted. A post's theme must differ from ALL of the previous 3 posts (on a 3-column grid that covers the posts beside it and above/below it). No theme more than twice in any 6 posts. The 3 pinned posts are the only exception.
- Also vary the layout inside a theme: don't repeat the same cover slide type or the same slide-type sequence as the last post in that theme (mix cover / stat / question / quote / event / rows / chips).
- If photos exist in `posts/photos/` that haven't been used (track in calendar.json `photo`), do a `photo` post at least every 2 weeks: real faces outperform graphics on this account. If a post is planned as `photo` but no photo exists, use its `theme_fallback`.
- **Slide types**: cover, statement, quote, stat, event, question, cta. Mix them; a carousel shouldn't be all the same type.
- Match theme to content where you can (terminal: crypto history/tech; gradient: moments, events; light/white: opinion, polls, hot takes; frame: tips and checklists; midnight: testimonials, hiring intelligence; photo: anything personal), but the variety rule wins over content fit.
- Carousel 4–7 slides, cover hook first, cta last. Static = 1 slide.
- Highlight 1–3 words per title with `<span class='g'>…</span>`.
- Keep text short: title ≤ 9 words, sub ≤ 30 words, ≤ 4 rows, ≤ 6 chips, ≤ 4 options.
- Always look at every rendered slide before scheduling: no overflow, clipping or typos.

## Team
- Jordan Edwards, Founder. Joshua Moore, Recruiter (DeFi, NFT, infrastructure). Tegan, Researcher (behind-the-scenes talent research). Illustrated portraits in posts/photos/team/.
- Real photos of people: use the `raw` slide type so no text covers faces; put the words in the caption.

## Testimonial cadence
About one post in five should be a testimonial post (alternate hiring-side and candidate-side; include Josh's at least once a month). When drafting new calendar topics, plan these in.

## Competitor lessons (Jordan shared screenshots, 18 Oct 2026; never copy their content)
- Biggest accounts are people-led: Block Recruit (~9.5k) is founder at booths, office, fun Reels. Odiin, Plexus, Impax are almost all real photos (team, events, socials).
- Template-only accounts stall: Blockchain Staffing Ninja (190 posts, ~128 followers), The Crypto Recruiters (identical animated logo Reels, ~372). That is the copy-paste trap to avoid.
- Socius position: boutique and founder-led (Jordan and Josh). Never fake scale. Graphics carry the expertise; photos carry the trust.
- Once photos are available, target roughly half the feed as real photos/video, with graphics between them.
- Ideas we can do our own way: conference vox-pop Reels (one question to builders), event recaps, the 'people behind Socius'.

## Conferences and events method
We only have ~10 posts a month, so events are tiered:
- **Tier 1, Jordan/Josh attending** (listed in calendar.json `config.confirmed_events`): 3 touches.
  1. 7–10 days before: "We'll be there, let's meet" event card (feed + LinkedIn + X). Goal: book coffees/DMs.
  2. During: X posts from the event if Jordan shares photos or notes (X is cheap and live). Never invent who he met.
  3. Within 2–4 days after: photo recap (raw photo slides), takeaways only if Jordan provides them.
- **Tier 2, major global events we're not at** (Token2049 Dubai/Singapore, ETHDenver, Consensus, EthCC, Permissionless, Devcon, Breakpoint, Korea Blockchain Week, Blockchain Life): one "who's going?" event card 3–7 days before, framed as a conversation starter. Also a short X post on day one.
- **Tier 3, everything else**: no individual posts. Covered by a **monthly "Events this month" carousel** (one slide per event: date card, city), posted in the first few days of each month. Plan it as the first post of every month.
- Always verify dates on the official site before posting. Keep `moments.json` updated with new events found.
- If Jordan says he's attending something new, upgrade it to Tier 1 and re-plan the calendar.
