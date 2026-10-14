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
- Captions: hook line first, 3–6 short paragraphs, one clear CTA, 4–6 relevant hashtags at the end.
- Avoid em dashes in captions; use commas, colons or full stops.

## Hard rules (never break)
1. **Never invent facts**: no fake stats, placements, client names, salaries, testimonials or quotes. If a claim needs a number, either use a verifiable public source (and keep it general) or leave the number out.
2. **Live roles**: only roles currently listed at sociustalent.com/jobs, with title, sector, location and salary exactly as listed. If the jobs page can't be read, swap the post for an evergreen hiring-intelligence topic instead.
3. **Testimonials**: only from `TESTIMONIALS.md`, word for word (trim with "…", fix typos only). Use the `quote` slide type. Credit full name + role as listed. Never reuse one within 6 weeks.
4. Holidays are welcome (Jordan's audience is global), but keep them on-brand and short. Never post generic stock-style holiday art.
5. Events/conferences: never claim Socius is attending, speaking or hosting unless Jordan has said so in calendar.json or BRAND.md.

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
- **Themes**: `midnight` (house navy), `light` (editorial paper + serif), `gradient` (bold brand gradient), `terminal` (mono, crypto/tech), `photo` (Jordan's real photos from `posts/photos/`).
- **Never use the same theme as the previous post.** Over any 6 posts use at least 4 themes. If photos exist in `posts/photos/` that haven't been used (track in calendar.json `photo`), prefer a `photo` post at least every 2 weeks: real faces outperform graphics on this account.
- **Slide types**: cover, statement, quote, stat, event, question, cta. Mix them; a carousel shouldn't be all the same type.
- Match theme to content: terminal for crypto history/tech; gradient for moments, events, announcements; light for opinion, advice and polls; midnight for hiring intelligence and testimonials; photo for anything personal.
- Carousel 4–7 slides, cover hook first, cta last. Static = 1 slide.
- Highlight 1–3 words per title with `<span class='g'>…</span>`.
- Keep text short: title ≤ 9 words, sub ≤ 30 words, ≤ 4 rows, ≤ 6 chips, ≤ 4 options.
- Always look at every rendered slide before scheduling: no overflow, clipping or typos.

## Testimonial cadence
About one post in five should be a testimonial post (alternate hiring-side and candidate-side; include Josh's at least once a month). When drafting new calendar topics, plan these in.
