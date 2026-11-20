# Remodeling page criteria (pass/fail)

1. **Scope, process, communication, next step.** The page says what is included in the room
   type, how the work runs (consultation, design and selections, written scope and price,
   permits, build, walkthrough), how and how often the homeowner hears from us, and what
   happens after "Schedule a Consultation".
2. **Projects as stories, real only.** A project is shown as: starting point, homeowner goal,
   what was done, documented result (photos, dates, scope). Only real Blue Hammer projects with
   the homeowner's permission. Until one exists, show none; never fill the slot with
   illustrative images.
3. **Confirmed proof only.** Reviews, ratings, awards, years in business, MHIC license,
   insurance, warranties, financing and prices appear only when confirmed in `site-src/assets/site-config.js`
   or by Rodrigo (see [evidence.md](evidence.md)). Missing items stay hidden and are logged.
4. **Image provenance.** Every image has a known origin recorded in
   [evidence.md](evidence.md#image-provenance): real project photo or illustrative image.
   Owner rule (2026-11-18): illustrative images are not labeled as AI on the site, and are never
   captioned or described as Blue Hammer work, clients, staff or before/after.
5. **Local content needs local specifics.** A town or neighborhood page needs real, specific
   material (housing stock, permit office, typical layouts, distances from Olney). No city-swap
   pages. Maryland, DC and Virginia within about 40 miles of Olney, per HARD-RULES.md; never claim
   a DC or Virginia license until Rodrigo confirms it.
6. **Keyword work uses real data.** Choose terms from real sources (Search Console, Semrush or
   other connected data, Google autocomplete/People Also Ask observed that day), and note the
   source and date in the log. No made-up volumes.
7. **Lead delivery.** The form posts to Netlify Forms (`consultation`). Only when a task
   explicitly authorizes an end-to-end test, submit one clearly marked test lead and confirm it
   arrives at the configured destination. Never submit during routine checks.
8. **No promises.** Never promise Google rankings, "page one", or being recommended by AI
   assistants.
