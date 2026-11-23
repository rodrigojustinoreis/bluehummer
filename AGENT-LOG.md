# Blue Hammer agent log

Dated entries, newest at the bottom. Each entry: what changed, why, commits, verification,
what's next, and a "Needs Rodrigo" list containing only things the agent cannot do itself.

---

## 2026-11-18 — Run 1: audit revision, repo hygiene

### Batch 1: audit realignment + repo hygiene
- **What changed**
  - `AUDIT-2026-11-18.md` revised in place: new section "0. Service-area alignment", rewritten 4.3/4.4,
    5.x, prioritized list and "Needs Rodrigo" to match the agent definition (Olney 20832 base, Maryland
    only, premium positioning, Tier 1 areas). Withdrew the earlier Gaithersburg / Germantown / Wheaton /
    Aspen Hill recommendations; Silver Spring scheduled for retirement with a 301.
  - Added `.gitignore` (`.claude/bluehammer-run.log`, `.netlify/`, `data/`, `.DS_Store`, `.env*`).
  - Committed agent config (`CLAUDE.md`, `.claude/agents/bluehammer.md`, `.claude/settings.json`),
    `scripts/gen-image.py`, and the new brand assets created earlier today:
    `blue-hammer-mark-140.webp` (140×80, 5.6 KB), `blue-hammer-mark-140.png`, `blue-hammer-logo-512.png`
    (512×292), `og-blue-hammer.jpg` (1200×630, 52 KB), and the re-encoded `basement-design-1440.webp`
    (252 KB → 187 KB).
- **Why**: the audit's framing was off-strategy; the working tree had valuable uncommitted assets; the
  215 KB session log must never reach GitHub.
- **Verification**: `git status` clean of the log file after `.gitignore`; asset dimensions checked
  with `sips`.
- **Image generation**: `python3 scripts/gen-image.py` reports `No OPENAI_API_KEY found (env or
  Keychain)` — image generation skipped this run (see Needs Rodrigo).

---

## 2026-11-18 — Owner-requested design pass and image-label removal (done by Grok Bot for Rodrigo)

- **What changed**
  - Committed the agent's pending run-2 work (five new Tier 1 town pages, page rewrites, new images) after a clean build.
  - Removed every AI label on images: 21 visible tags/badges ("AI-generated design concept", "DESIGN INSPIRATION"),
    8 notices, 12 gallery eyebrows, the footer disclaimer, the projects info panel; 44 alt texts rewritten to neutral
    descriptions (plus 3 in `scripts/build.py`). Gallery renamed "Design Gallery". Terms/FAQ keep an honest, neutral
    statement that images are not finished Blue Hammer projects. `project-concept.svg` renamed `project-detail.svg` (unreferenced).
  - `build.py --check` now fails on AI-label wording in text or alt, and on banned slop phrases.
  - Design system: `docs/brand.md`, `docs/design-system/*`, project skills `bh-design-loop`, `bh-design-check`,
    `bh-anti-slop-copy`, `bh-section-references`; personal skills `anthropic-frontend-design` (official Anthropic) and
    `slopmonster` (MIT) installed in `~/.claude/skills/`.
  - Type: Gambetta + Switzer (Fontshare, ITF Free Font License). Micro-interactions: button press, image zoom on hover,
    scroll reveal, counters for `data-count` only; all disabled under `prefers-reduced-motion`. New 404 layout.
  - Copy: hero H1 no longer says "built to last"; generic triple lists on service pages rewritten concretely.
- **Next**: AUDIT fix list item 15 (page-by-page design overhaul with the design loop and five-agent check).

## 2026-11-18 — Palette A (Heritage Navy & Brass) and design-review skills

- **What changed**
  - Applied palette A, approved by Rodrigo: ivory page background `#FBF8F2`, navy `#0B2347`,
    royal `#1E4FA3`, brass `#A88B5A`, warm limestone `#F3EEE3`, ink `#14243D`, muted `#525D6B`,
    borders `#E4DCCB`. Tokens and the matching chrome (header, eyebrows, buttons, topline,
    focus ring, dark-section accents) were ported into `blue_hammer_remodeling_site/assets/main.css`.
    `docs/brand.md` and `docs/design-system/design-brief.md` now document this palette.
  - Installed into `~/.claude/skills/` (skill files only, no install scripts, no npx):
    `better-interface` plus domain skills `better-accessibility`, `better-layout`,
    `better-writing`, `better-typography`, `better-colors`, `better-ui` (MIT, jakubkrehel/skills),
    and a local `web-interface-guidelines` skill that vendors `command.md` from
    vercel-labs/web-interface-guidelines (MIT) with no network step.
  - `.claude/agents/bluehammer.md` and `bh-design-loop` now tell the agent to use those skills
    on the AUDIT item 15 page-by-page overhaul.
- **Why**: Rodrigo chose palette A so the site can feel traditional and modern at once;
  the new skills add typography, layout, accessibility and interface-guideline review
  beyond the already installed frontend-design and slopmonster skills.
- **Verification**: `python3 scripts/build.py --check` — OK, 23 pages, 0 problems.
  Live CSS on bluehammermd.com to be confirmed after the Netlify deploy.
- **Next**: AUDIT item 15 page-by-page overhaul with `bh-design-loop`, `better-interface`
  and `web-interface-guidelines`.

## 2026-11-18 — Orchestrator and specialist subagents

- **What changed**
  - Added `.claude/agents/bh-orchestrator.md` as the entry point for every
    headless or autonomous run. It reads the audit and this log, picks the next
    stage, delegates, runs a quality gate, and only then commits and pushes.
  - Added specialists: `bh-designer`, `bh-seo-content`, `bh-images`, and
    read-only `bh-qa`. Shared rules live in `.claude/agents/HARD-RULES.md` and
    are repeated in each agent.
  - `bluehammer` is now a compatibility alias that follows the orchestrator.
  - `CLAUDE.md` and new `scripts/run-orchestrator.sh` start the orchestrator
    (`claude -p --agent bh-orchestrator --permission-mode bypassPermissions`).
- **Why**: Rodrigo asked for an agent that orchestrates each stage of the
  project instead of one generalist doing all the work.
- **Verification**: `python3 scripts/build.py --check` after this change.
- **Next**: AUDIT item 15 page-by-page design overhaul, via the orchestrator
  (not started in this commit).

---

## 2026-11-18 — AUDIT item 15, pass 1: site chrome + home page overhaul (orchestrator)

- **Stage:** 2, design system and page overhaul (AUDIT 15 a-g). Specialists: `bh-designer` (build), `bh-qa` (gate).
- **Picked up from the stopped run:** kept the one-rule-per-line `main.css`, the six downloaded woff2 files
  (verified byte-identical to Fontshare's CDN) and the `/assets/fonts/*` immutable cache header in `netlify.toml`.
- **What changed**
  - **Fonts (15g):** self-hosted Gambetta 400/400 italic/500/600 and Switzer 400-700 (`assets/fonts/`,
    `font-display:swap`, 2 preloads per page). Removed the `api.fontshare.com` link and the legacy Inter stack.
  - **Base styles (15d, 15e):** radius by hierarchy (2-6 px). Removed the tinted button shadow and card shadows.
    Eyebrows are sentence case and mostly removed. Limestone alternate sections with brass hairlines. Off-palette
    blue tints replaced with palette A tokens. Dark areas get an on-dark focus ring for contrast.
  - **Chrome (15c):** one-line topline. Solid ivory header with a short nav (Services, Service areas, Process,
    Gallery, About, Contact) and a compact royal CTA. Accessible mobile menu (`aria-expanded`, Escape returns
    focus). Editorial navy2 footer with all previous links; phone/email/license slots stay hidden while empty.
  - **Home (15a, 15b, 15f):** follows the owner's layout reference (adapted, nothing copied). Full-bleed craft
    photo with a solid ivory text panel and a mixed-type H1 ("REMODELING / *planned before the first wall comes
    down.*"). Services bento with a large kitchen tile. Eight-tile "What goes into the work" icon grid with one
    brass tile. Numbered process, Olney areas split, short FAQ, restyled consultation. Trust strip and gallery
    band cut to reduce text. Netlify form `consultation` unchanged in function.
  - **Copy honesty:** removed promises not in the evidence register ("weekly updates", "one team", "reply with
    honest next steps" → "follow up if the project is in our area").
  - **Docs:** `docs/brand.md` Typography now records the owner override (uppercase Switzer display word +
    Gambetta italic, H1/section titles only) and self-hosted fonts. `DESIGN.md` (setup file, left uncommitted)
    is updated to match.
- **Why:** AUDIT item 15. The owner said the site looks generic/AI-made.
- **Verification:** `python3 scripts/build.py --check` printed OK (23 pages, 0 problems). Screenshots of home,
  services, kitchen, Olney, contact and 404 at 1440/390 were reviewed. `bh-qa` gate **PASS** on all 8 checks
  (build, design, a11y, image/AI labels, facts, anti-slop, form, SEO): no console errors, no outside font
  requests, no overflow, contrast at least 4.5:1 (brass tile 5.5:1). The desktop dropdown no longer opens on
  `:focus-within`; Escape closing it was re-verified in the browser.
- **Commit:** this entry ships in the same commit as the work. Setup files were left uncommitted on purpose.
- **Next:** AUDIT 15, pass 2: interior page heroes and templates (service pages, then location pages). Remove
  the uppercase "BLUE HAMMER APPROACH" / "STEP 01" strings and leftover button arrows. Change the mobile menu
  label to "Close" when open. Move or soften the DETAIL watermark behind the side note. Neutral hero alt text
  ("Painted inset cabinet door with a brass hinge and a spirit level on a stone counter"). Make footer link
  casing consistent. Decide on `primaryImageOfPage` (now `cabinetry-detail`, was `kitchen-potomac-estate`).
  Review the Olney page alt text that ties a generated image to "a wooded Olney, Maryland lot".
- **Needs Rodrigo**
  - Confirm or reject these service facts before they go back into copy: in-house design, permit handling,
    weekly progress updates, replying to every request.
  - Confirm the FAQ planning ranges ($85k-$175k, $175k-$300k+); they are not in the evidence register.
  - Optional: an `OPENAI_API_KEY` in the Keychain (or real photos) for a wide hero image of hands at work on
    cabinetry or stone (no faces, about 2400 px). The current close-up is soft at full width on large screens.
  - Still open from earlier: Netlify form detection, phone/email/MHIC in `site-config.js`, GBP/Search Console access.

---

## 2026-11-18 — Scope change (MD/DC/VA + small repairs), brand motion, hero, three layout fixes

Run by the Grok Bot executor on Rodrigo's Mac. The orchestrator wasn't running.

- **Scope (owner decision, 2026-11-18).** The service area is now about 40 miles of Olney across Maryland, Washington, DC
  and Virginia, and small repairs are the entry service. Updated in:
  - HARD-RULES and every `.claude/agents` file;
  - CLAUDE.md, DESIGN.md, docs/brand.md and the design brief;
  - the blue-hammer-website skill and its references;
  - `.agents/product-marketing.md` (v1.1);
  - AUDIT item 0.8 (now superseded) and the new item 16.

  Site copy changes:
  - home: the hero sub-line, the areas section, the FAQ, and a new "Starting smaller?" repairs note;
  - faq, service-areas, about, contact and terms;
  - the top bar.

  In `build.py`: the business description, "Small home repairs" added to the schema `serviceType`, and the
  Northern Virginia/DC phrases removed from FORBIDDEN. No DC/VA license is claimed anywhere.
- **Hero.** A new generated image of a generic craftsperson with a drill at cream inset cabinets
  (`assets/hero-craftsman-{720..2400}.webp`), made with `scripts/gen-image.py`. The real Blue Hammer mark was
  composited as a one-colour shirt print with `tools/image/shirt_print.py`; it sits on the back because the
  figure faces away. Alt text is neutral. No AI label, and it isn't presented as an employee or a project.

  The photo now covers the full hero, so the plate and CTA sit inside it on desktop.
- **Brand motion.** A Remotion 4 project in `tools/remotion/` (outside the build; licence notes below) renders:
  - `hero-loop`: a slow 12 s push on the hero photo. MP4 1.58 MB, WebM 0.65 MB.
  - `process-steps`: a brass line and four line icons above the 4-step list. About 30–50 KB; desktop only.

  Both are muted, loop and playsinline, with posters. Sources attach only when the video is near the viewport,
  motion is allowed and Save-Data is off. Under reduced motion only the photo or poster shows.

  `render.sh` re-renders both. The official `remotion-*` skills were added under `.claude/skills/`.
- **Fixes.**
  - The DETAIL watermark has its own band, so it no longer overlaps the side note.
  - The mobile sticky CTA detects Netlify's injected badge iframe (`#nl-badge-frame`) and pads itself, so the
    badge sits under the button instead of on it.
- **Verification.**
  - `python3 scripts/build.py --check`: OK, 23 pages.
  - Local Playwright at 1440 and 390: videos play, nothing loads under reduced motion, the watermark and side
    note don't overlap, and the plate sits inside the hero photo. With a simulated badge, the badge sits
    below the CTA button.
  - The bh-qa gate ran read-only. It passed licences, honesty, AI labels, the video embeds and file sizes. It FAILED one item: the
    branded shirt reads as a Blue Hammer employee. That was shipped as an explicit owner request (Needs Rodrigo 5).
    Its non-blocking notes were fixed: the "Maryland service area" strings were removed and "Small repair" was added
    to the form's project types. Page titles and meta still name Montgomery and Howard County; that waits for AUDIT 16.
- **Needs Rodrigo**
  1. Confirm DC and Virginia contractor licensing before any license is claimed for those jurisdictions (DC DLCP
     home improvement licence; Virginia DPOR Class A/B/C). DC/VA area pages (AUDIT 16b) wait on this.
  2. Confirm the small-repairs scope: which repairs, any minimum job size or trip fee, and how they're priced.
     The site only says "small repairs and fixes"; a repairs page (16a) waits on this.
  3. Remotion licence. It's free for individuals and for-profit companies with **3 or fewer people** (total
     headcount). From 4 people up, a Company License is required: "Creators" is $25 per seat per month, or
     "Automators" is $0.01 per render with a $100/month minimum. Confirm Blue Hammer's headcount.
  4. Netlify's "Powered by Netlify" badge is injected by Netlify and can't be removed in code. To remove it, go
     to Netlify > Project configuration > General > "Powered by Netlify" badge (it may be locked on the Free
     plan). The code fix only keeps it off the CTA.
  5. The hero craftsperson wears a Blue Hammer-branded shirt, as you asked. He's a generated, generic person:
     the alt text is neutral and he isn't named or presented as staff. Swap in a real photo of your crew when
     you have one.
  6. Still open from before: the business phone, the MHIC number, and real reviews and project photos.

---

## 2026-11-18 — AUDIT item 15, pass 2: interior hero template + service pages (orchestrator)

- **Stage:** 2, page-by-page design overhaul. Specialists: `bh-designer` (build), `bh-qa` (gate).
- **What changed**
  - **Shared interior hero** (`assets/main.css`, used by about 17 pages): ivory background, text column low under a
    brass rule, photo bleeding to the right edge; on mobile, text and CTA first, then a full-width photo. Pages with
    no photo (contact, privacy, terms) keep a plain text hero.
  - **Service pages** (kitchen, bathroom, basements, services): paired H1 (Gambetta italic + Switzer uppercase); the
    four identical "BLUE HAMMER APPROACH" boxes became a two-column topic list with no kicker labels; the repeated
    checklist block became one photo-and-text section; FAQ laid out like the home page; services.html gets the home
    bento, the "Starting smaller?" repairs note and the numbered process (no more "STEP 01"). Images are no longer
    repeated on one page (bath uses `bath-bethesda-hall`, basement uses `basement-lower-level`, neutral alt text).
  - **Leftovers from pass 1:** 30 button arrows removed site-wide (text links keep theirs); footer links in sentence
    case; the mobile menu button shows an X and "Close" when open (`aria-expanded` kept); Olney/service-areas hero alt
    no longer ties a generated image to Olney.
  - **Copy honesty:** removed "weekly updates" (unconfirmed) and the line saying each service page lists timelines and
    permits (untrue). Process step 4 now reads "Floor protection during the work and a final punch-list
    walk-through". The orchestrator cut the designer's "a shared schedule" because it is an unconfirmed promise.
    Copy is more concrete (e.g. "Quartzite, marble or quartz, compared for how each one stains, etches and wears").
  - **Orchestrator tweak after the gate:** interior hero photo height `clamp(420px,38vw,560px)` (was up to 640 px),
    which closes the gap QA found above short headlines at 1440. A stale "sticky" CSS comment was removed.
- **Why:** AUDIT 15. Interior pages still looked like a contractor template after pass 1.
- **Verification:** `python3 scripts/build.py --check` OK (23 pages, 0 problems). `bh-qa` **GATE: PASS** on all 7
  checks: build; design (bh-design-check + better-interface + web-interface-guidelines); accessibility (one H1,
  landmarks, contrast, focus, menu label + Escape); images/AI labels; facts; anti-slop (deslop 5/5 on kitchen, bath
  and basements, 4/5 on services for the literal service list in the H1, accepted); browser at 390/768/1024/1440
  with no console errors and no horizontal overflow. The orchestrator re-checked the kitchen hero at 1440 after the
  tweak: no console errors.
- **Commit:** this entry ships in the same commit as the work. Setup files (`.claude/skills/*`, `.mcp.json`,
  `tools/package*.json`) were left uncommitted on purpose.
- **Next:** AUDIT 15, pass 3. Location pages (olney, potomac, bethesda, chevy-chase, kensington-garrett-park,
  howard-county, rockville, service-areas) and about.html need the following:
  - Remove the "KITCHENS / BATHS / BASEMENTS" kicker labels and the middot eyebrows.
  - Use sentence-case buttons and breadcrumbs, to match the footer.
  - Give location pages the paired H1 and the topic-list pattern.
  - Make the button text "See the Design Gallery" consistent.
  - Remove the repeated "before anything is ordered" on the kitchen page.

  After that, SEO work (`bh-seo-content`):
  - Service-page titles and meta still say "Serving Montgomery County, Maryland". Update them for the MD/DC/VA area
    and repairs (AUDIT 2.5 / 16d).
  - The about hero says only "Montgomery and Howard County".

  Low priority:
  - Re-encode `olney-colonial-exterior-1440.webp` (229 KB) to under 200 KB.
  - Rename the `bath-bethesda-hall-*` and `kitchen-howard-county-*` image files to neutral names, with redirects.
- **Needs Rodrigo**
  1. These claims were already live before this run and are still there. Confirm or reject them:
     - The services cost table says the ranges include "design, permits, labor and materials".
     - Process step 3 says "the permit application for your jurisdiction".
     - service-areas mentions "our team, our trade partners".
  2. Confirm the services planning ranges ($35k–$300k+), as well as the FAQ ranges already listed. Neither is in the
     evidence register.
  3. Still open from earlier runs:
     - DC and Virginia licensing.
     - The small-repairs scope and any minimum job.
     - Remotion headcount licence.
     - The Netlify badge and the Netlify form detection setting.
     - Phone, email and MHIC number in `site-config.js`.
     - Real photos and reviews.
     - GBP and Search Console access.

---

## 2026-11-18 — AUDIT item 15, pass 3: location pages, about, service-areas + area-aligned titles/meta (orchestrator)

- **Stage:** 2, page-by-page overhaul, plus a small content/SEO follow-up (AUDIT 2.5 / 16d). Specialists:
  `bh-designer` (design), `bh-seo-content` (titles, meta, claims, permit facts), `bh-qa` (gate).
- **Design (bh-designer)**
  - Rebuilt olney, potomac, bethesda, chevy-chase, kensington-garrett-park, howard-county, rockville,
    service-areas and about on the pass-2 patterns. Each now has:
    - paired H1 and paired section titles;
    - a housing section, a topic list of what homeowners ask for, the services bento, permits + planning
      ranges, and the home-style FAQ.
  - Removed the KITCHENS/BATHS/BASEMENTS kicker labels and middot eyebrows; ZIPs moved into the hero text.
  - `{{SERVICE_CARDS}}` in `build.py` now emits the bento plus the "Starting smaller?" repairs note.
  - Sentence-case buttons and breadcrumbs everywhere: "See the design gallery" and "Schedule a consultation"
    (the header CTA included).
  - The kitchen page's repeated "before anything is ordered" is cut to one.
  - Copy tightened on every page (old → new quoted in the designer report). One unverifiable line was cut:
    "The single most requested project in Olney."
- **Content/SEO (bh-seo-content)**
  - Titles (≤60) and metas (≤155) on kitchen, bath, basements, services, service-areas, process, faq,
    about, index and contact now say Olney base + MD/DC/VA within about 40 miles + small repairs. No license
    claim anywhere.
  - The About hero, footer blurb and `og:image:alt` are aligned with the same area.
  - Unconfirmed operational promises were made neutral:
    - crew on site daily or the same crew every day;
    - daily clean-up;
    - the last "weekly update";
    - showroom and slab-yard trips;
    - "We do this regularly";
    - the process FAQ's "lead carpenter … licensed trades";
    - "Inspectors we see often".
  - **Permit fact fix.** Five pages said Montgomery County DPS permits plumbing. Plumbing and gas permits
    actually come from **WSSC Water**; DPS covers structural and electrical. Corrected on olney, potomac,
    bethesda, chevy-chase, kensington and service-areas.
  - Laytonsville was taken out of the "unincorporated" list (it is an incorporated town).
  - Bethesda housing copy was corrected: "Tudors", "compact lots" and Glen Echo Heights as mid-century were
    removed.
- **Why:** AUDIT 15. The location pages and About still had the contractor-template look. Titles and meta
  still said Montgomery County only, after the owner's MD/DC/VA + repairs scope decision.
- **Verification**
  - `python3 scripts/build.py --check` OK (23 pages, 0 problems).
  - `bh-qa` **GATE: PASS** on all 8 checks: build, design (bh-design-check five checks + better-interface +
    web-interface-guidelines), accessibility, images/AI labels, facts, anti-slop, SEO lengths/canonicals/
    JSON-LD, and the browser at 390/1440 on six pages (no console errors, no overflow).
  - QA's non-blocking notes applied afterwards (text only; build re-run OK): footer blurb, WSSC on the
    service-areas DPS bullet, the process "lead carpenter" FAQ, the Bethesda section title, the FAQ hero
    area wording, and the Bethesda and Rockville metas.
  - Caveat: the design-check reviewers ran inline, not as five separate subagents (no subagent tool inside the
    specialists).
- **Commit:** ships in the same commit as this entry.
- **Next**
  1. AUDIT 15 pass 4: process, faq, projects, reviews and contact still have eyebrows and plain H1s. Also split
     the FAQ's 8 semicolon sentences.
  2. Real local depth for Bethesda and Rockville (AUDIT 4.3): replace their two generic FAQs.
  3. Rename the town-tied image files (`kitchen-potomac-estate-*`, `kitchen-chevy-chase-1920s-*`,
     `bath-bethesda-hall-*`, `kitchen-howard-county-*`) to neutral names, with redirects. They now sit as heroes
     on same-town pages, so this is more urgent.
  4. Re-export `olney-colonial-exterior-1440.webp` (223 KB) from the source image. Re-encoding the WebP to under
     200 KB visibly softens it.
  5. Projects and terms pages still use Montgomery and Howard County framing. The service-areas title could read
     better. "Closer means better" heading is vague.
- **Needs Rodrigo**
  1. Approve or correct the local facts now on the Bethesda and Rockville pages:
     - neighborhoods: West End, Fallsgrove, King Farm, Woodley Gardens;
     - City of Rockville Inspection Services Division;
     - Bethesda 1930s–60s colonials and Capes, Carderock Springs mid-century.

     They are public facts but not yet in the evidence register.
  2. Confirm or reject the claims still live:
     - "trade partners";
     - "decisions are logged in writing" (about, process);
     - "we prepare and file residential permits … and schedule the inspections";
     - the per-town planning ranges, the $55k–$95k Howard County FAQ range and the services ranges;
     - the 20/25/30-minute drive times.
  3. Whether Sandy Spring 20860 belongs on the service-areas list (it is not in Tier 1).
  4. Still open from earlier runs:
     - DC and Virginia licensing;
     - the small-repairs scope and any minimum job;
     - Remotion headcount licence;
     - the Netlify badge and form-detection setting;
     - phone, email and MHIC number in `site-config.js`;
     - real photos and reviews;
     - GBP and Search Console access.

---

## 2026-11-19 — Visual audit + AUDIT 15 pass 4; owner package ported into the build (orchestrator)
- **Critical first: the owner package (commit e455100) is preserved.** That commit was a hand-delivered
  build that edited generated HTML directly. Its changes were the v2 identity, the new home page with the
  hero video, the new nav, the consultation copy, the hammer mark and favicon, the Barlow preload and the
  `?v=` cache-busters. None of this was in `site-src/` or `scripts/build.py`, so running the build would
  have reverted all 23 pages. Ported:
  - `scripts/build.py` now emits the owner's chrome exactly:
    - theme-color `#142131`;
    - `bh-hammer-v2.png` as favicon and as the 62×68 header/footer mark;
    - Barlow Condensed 800 + Switzer 400 preloads;
    - sha256[:12] `?v=` hashes on CSS/JS/config/favicon;
    - nav Services / Our Process / Service Areas / About;
    - title-case "Schedule a Consultation";
    - the consultation eyebrow, title and lede;
    - schema logo `bh-logo-v2.png`.
  - `site-src/pages/index.html` holds the owner's home `<main>` and the owner's title and meta.
  - **Proof:** after porting, the build output was byte-identical to HEAD (empty `git diff` on every
    page). The owner's CSS/JS blocks are untouched; this run only appended to `main.css`.
- **Visual audit (1440 + 390, all 23 pages, Playwright).** No overflow, console errors or broken images
  before or after. Problems ranked by visual impact:
  1. Process, FAQ, gallery, reviews, contact, thank-you, privacy, terms and 404 still had brown eyebrow
     labels and plain mixed-case H1/H2s. They clashed with the uppercase paired titles everywhere else.
  2. Interior hero H1s used two sizes inside the paired title (pass-2 rule over the owner's Barlow rule).
  3. Barlow Condensed has only one upright face, so step numbers, timeline counters and "Starting
     smaller?" rendered as synthetic (fake) italics.
  4. h3s and FAQ questions on interior pages were in condensed caps type. The owner's home uses Switzer
     for both.
  5. Paired titles had no bottom margin in split layouts, so headings touched their paragraphs.
  6. CTA casing was mixed: "Schedule a Consultation" in the header and home, "Schedule a consultation"
     on buttons and the mobile bar, sometimes on one screen.
  7. The fixed mobile CTA sent visitors off the page (to `index.html#consultation`), even on the contact
     page with its own form. It also stayed over the open mobile menu.
  8. QA found inline body links (FAQ, about, privacy, terms) that were indistinguishable from text
     (WCAG 1.4.1).
- **Fixes**
  - Pass-4 pages use `.title-pair` H1/H2s; eyebrows removed. The FAQ "The practical questions." now reads
    "Permits, licensing and service area." (restates the old label; no new claim).
  - `main.css` (appended block "Pass 4 alignment"):
    - no italics on Barlow;
    - h3, FAQ summaries and prose h2 in Switzer;
    - interior hero H1 as two equal lines with the second in royal, mirroring the home hero;
    - title-pair spacing;
    - form scroll margin;
    - mobile bar hidden while the menu is open;
    - inline body links royal and underlined.
  - All primary buttons read "Schedule a Consultation".
  - `mobile_cta()` targets the form on the same page (`#consultation`, or `#contact-form` on contact).
- **Verification**
  - `python3 scripts/build.py --check`: OK (23 pages, 0 problems).
  - Playwright at 390/1440 on 23 pages: no overflow, no console errors, one H1 each.
  - bh-qa (independent subagent, with the five bh-design-check reviewers):
    - hierarchy/brand PASS;
    - mobile PASS;
    - performance PASS;
    - conversion PASS;
    - build/images/copy PASS;
    - accessibility first FAILed on the inline-link issue. Fixed and re-verified by computed style
      (royal + underline on every affected link; area lists and breadcrumbs unchanged).
  - Contrast measured by QA: royal 5.3:1 on white, navy on orange 7.5:1, `#9D4000` about 7:1.
- **Left on purpose**
  - The header CTA still links to `index.html#consultation`. It is the owner's chrome, kept as delivered.
  - The home H1 `<br>` (text reads "A better home.Starts here.") is the owner's markup.
  - `olney-colonial-exterior-1440.webp` is still 229 KB; it needs a re-export from source.
  - Splitting the FAQ's semicolon sentences is copy work, not visual.
  - `docs/brand.md` still specifies palette A. Rewriting the spec needs the owner's sign-off.
- **Next**
  1. Update `docs/brand.md` and the design-check checklist to the v2 identity once approved.
  2. Re-export the Olney hero image.
  3. Consider pointing the header CTA in-page on pages that have a form.
- **Needs Rodrigo**
  1. Approve rewriting `docs/brand.md` to the v2 identity:
     - navy `#142131`, orange `#FF7A24`, royal `#0864D8`;
     - Barlow Condensed 800 + Switzer;
     - title-case primary CTA.
  2. Still open from earlier runs:
     - phone, email and MHIC number for `site-config.js`;
     - DC/VA licensing;
     - real project photos and reviews.

---

## 2026-11-19 — Step 1: technical SEO base + keyword map (not committed, not pushed)
- **Scope:** head tags, JSON-LD, internal links, sitemap, robots and redirect config only. No CSS, layout or
  copy restyling. Built on top of the uncommitted visual-audit pass; nothing was restored or reset.
- **Build safety proof:** before any change, every page was rendered in memory and compared with the
  generated folder: 23 pages, 0 differing. After the change, a second dry run into a temp folder showed only
  these diff kinds: internal `<a href>` (1,068), form `action` (19), canonical (22), `og:url` (22), JSON-LD (23).
  Assets and every other non-HTML file are byte-identical (checksums compared).
- **Finding 1, duplicates (46 URLs). Real cause, confirmed live:** the live HTML is post-processed by Netlify
  (Pretty URLs is on): every internal link is rewritten to `/name`, while canonical and sitemap said
  `/name.html`. Both forms return 200 with the same ETag, and `/index.html` duplicates `/`. 23 pages x 2 = 46.
  - **Fix:** one URL form, extensionless (`/`, `/kitchen-remodeling`). `scripts/build.py` now emits canonical,
    `og:url`, JSON-LD URLs, sitemap and all internal links in that form (`page_url()`, `pretty_links()`).
    Fragments in `site-src/` still write `name.html`; the build converts them.
  - Retired Silver Spring redirects now point at `/service-areas` (in both `netlify.toml` and `_redirects`).
  - **Not added on purpose:** `name.html -> /name` 301 rules. Netlify resolves `/name` from `name.html`
    internally and a forced rule can loop; this cannot be tested without a deploy. The `.html` URLs keep
    answering 200 but are no longer linked, listed or canonical.
- **Finding 2, structured data (LocalBusiness on 42 URLs + FAQ on 2).**
  - Business node: `serviceType` is not a property of `HomeAndConstructionBusiness` (schema.org validator:
    UNKNOWN_FIELD, 7 values, every page). 21 indexable pages x 2 URL forms = 42. Removed. The type stays
    `HomeAndConstructionBusiness` with name, logo, image, areaServed and the truthful address (Olney, MD,
    20832, US; no street, no phone, no empty properties). Description is now the footer sentence verbatim.
  - FAQ page: two `FAQPage` nodes in the JSON-LD (the page node, with no `mainEntity`, plus `#faq`). No
    microdata was involved. Now exactly one FAQPage with one `mainEntity`, built from the visible questions.
    1 page x 2 URL forms = 2.
  - `WebSite` node is now on every page, so `isPartOf` always resolves.
- **Finding 3, 19 pages with 1 incoming link.** Every page already has 22 sitewide inbound links (nav and
  footer). The count is a side effect of finding 1: the `.html` twins were only reachable through the
  canonical tag. Also added in-body links by wrapping town names that were already in the text (no new copy)
  on services, about, process, projects and FAQ. In-body inbound links: Olney 2 -> 5, Potomac 2 -> 6,
  Bethesda 2 -> 6, Chevy Chase 2 -> 6, Kensington/Garrett Park 1 -> 6, Rockville 2 -> 4, Howard County 2 -> 6.
- **Finding 4, 1 broken URL: not reproduced in this crawl.** All 98 internal references and 98 absolute URLs
  on the live pages returned 200.
- **Finding 5, 84 JS/CSS warnings: not reproduced as a list** (no Semrush detail available). Observed:
  `main.css` (59.6 KB) and `main.js` (16.9 KB) are not minified; `site-config.js` (757 bytes) is served
  uncompressed; Netlify injects its own script `/.netlify/scripts/hud` (36 KB, 60 s cache) on every page.
  Nothing changed: the repo has no minifier, and the injected script is a Netlify setting.
- **Also:** `robots.txt` disallow is now `/thank-you` (covers both forms). Sitemap has 21 canonical,
  indexable URLs (no thank-you, 404 or `__forms`). `scripts/preview.py` added: local preview that resolves
  `/name` the way Netlify does (plain `python3 -m http.server` cannot follow the new links).
- **New build checks (`--check`):** links in canonical form and resolving, canonical and `og:url` equal to the
  page URL, sitemap equal to the canonical indexable set, one JSON-LD block, no empty values, references
  resolve, no `.html` URLs in schema, at most one FAQPage and equal to the visible FAQ, no unconfirmed or
  invalid business properties, no duplicate titles or descriptions.
- **Verification:** `python3 scripts/build.py --check` OK (23 pages, 0 problems). Local crawl through
  `scripts/preview.py`: 23 pages, 43 assets, 0 problems, canonical equals URL on all 23. schema.org validator
  on the new faq, home, Olney and kitchen pages: 0 errors, 0 warnings (was 7 warnings per page).
- **Not verified:** the Semrush counts themselves (needs a re-crawl after deploy); the exact Semrush rule
  behind the LocalBusiness errors; Netlify behaviour after deploy; no browser or visual check was run.
- **Keyword map:** `docs/seo-keyword-map-2026-11-19.md` (65 terms, 12 primaries, 11 terms with no page).
- **Next:** page-by-page content steps in the order listed in the keyword map, starting with
  `/kitchen-remodeling`.
- **Needs Rodrigo**
  1. Publish when ready (nothing is committed). After the deploy, check `/kitchen-remodeling` and
     `/kitchen-remodeling.html` and re-run the Semrush audit.
  2. Decide whether to test `name.html -> /name` 301 rules on a Netlify deploy preview.
  3. Netlify UI: the injected Netlify script/badge can only be turned off there (or by plan).
  4. If Semrush still flags LocalBusiness after the re-crawl, it wants a street address or phone. Either
     provide a phone for `site-config.js`, or approve switching `BUSINESS_TYPE` in `scripts/build.py` to
     `Organization`.
  5. `CLAUDE.md` still documents `python3 -m http.server` for preview; update it to `python3 scripts/preview.py`.
  6. Keyword decisions: Silver Spring page, Maryland cost guides, service + town pages.
  7. `reviews` is an indexable page with no reviews yet; decide whether to noindex it until there are some.

---

## 2026-11-19 — Page-content pass, batch A (not committed, not pushed)
Service pages, home and services hub. One page at a time: source edit, `build.py --check`, copy check
(deslop + facts grep), screenshots at 390 and 1440, then the next page.
- **Shared change:** `main.css` gained `.range-table--scope` (same table component; last column is prose
  instead of a price, rows stack under 700 px). No other styling changed.
- **Sources opened 2026-11-19** (recorded in `.claude/skills/blue-hammer-website/references/evidence.md`):
  Montgomery County DPS "Home Improvements: Permits Required / No Permits Required" flyer, WSSC Water
  "Information for Homeowners", Howard County DILP Licenses & Permits Division, City of Rockville
  "Apply for a Building or Trade Permit".
- **`/kitchen-remodeling`** (primary: kitchen remodeling maryland). Title "Kitchen Remodeling in Maryland |
  Blue Hammer Remodeling"; H1 "Kitchen remodeling in Maryland." Added: scope/cost-factor table (no prices),
  permits-by-address section (DPS, WSSC, Rockville, Howard DILP), six FAQs answered directly, Service
  schema node, links to process, bathroom, service areas, Rockville and Howard County. Check: OK, deslop 5/5.
- **Owner editorial note applied to all batch A pages:** no "we do not publish prices" policy wording and no
  talk about missing prices. Budget sections explain what a budget is made of (scope, layout changes,
  cabinetry, surfaces, mechanicals, permits, existing conditions).
- **`/bathroom-remodeling`** (primary: bathroom remodeling maryland). Title "Bathroom Remodeling in Maryland |
  Blue Hammer Remodeling"; H1 "Bathroom remodeling in Maryland." Added: five planning decisions (waterproofing
  and ventilation are new), scope/cost-factor table, plumbing-permit section led by WSSC Water, six FAQs,
  Service schema node. Check: OK, deslop 5/5.
- **`/basements-interiors`** (primary: basement remodeling maryland). Title "Basement Remodeling & Finishing in
  Maryland | Blue Hammer"; H1 "Basement remodeling in Maryland." Added: five site conditions to check first,
  four-row scope/cost-factor table (interior rooms included), permit section (DPS, WSSC, well and septic,
  Rockville, Howard DILP), six FAQs, Service schema node. Bedroom question points to an on-site assessment and
  the permit office; no egress or septic workaround advice. Check: OK, deslop 5/5.
- **`/` home** (primary: home remodeling maryland). Owner package kept: hero, video, header, layout and the H1
  "A better home. Starts here." are unchanged. Title now "Home Remodeling in Maryland | Blue Hammer
  Remodeling"; hero lede leads with "Home remodeling in Maryland"; the three service cards say what each
  page covers; the cost FAQ lists the budget factors. No prices or durations on the page. Check: OK;
  deslop 4/5 (the flagged list is the services list in the hero lede, accepted).
- **`/services`** (hub, no primary keyword). Title "Remodeling Services: Kitchens, Baths & Basements | Blue
  Hammer"; H1 "Remodeling services, room by room." The price table (six dollar ranges) is now a project
  table that routes each row to its service page. Removed "Planning cost ranges are listed below", the
  "ranges reflect typical total project cost" note, and the step promises about filing the permit
  application and floor protection. Check: OK, deslop 5/5.
- **Verification:** `python3 scripts/build.py --check` OK (23 pages, 0 problems) after every page. Playwright at
  390 and 1440 on the five pages: no horizontal overflow, one H1, no broken images, no console errors.
  Screenshots looked at. Facts grep (`$`, month, week, minute, licensed, insured, years) on the five sources:
  no hits. The shared consultation form still offers "Within 1–3 months" as a homeowner choice.
- **Not verified:** bh-qa was not run as a separate agent. DPS pages on residential alterations and basement
  finishing could not be opened (old URLs redirect), so egress and septic rules are not stated.
- **Left for later batches:** town pages, service-areas, about, process and FAQ still carry dollar ranges,
  timelines and travel times. `.agents/product-marketing.md` still says the site shows planning ranges.
- **Needs Rodrigo**
  1. RESOLVED 2026-11-19 (owner decision): home H1 is now "Home remodeling." / "In Maryland." (same element, br and span); the brand phrase moved into the hero lede. Line 524 above predates this.
  2. Service page titles and H1s now say "in Maryland" (keyword map primaries). DC and Virginia stay in the
     hero text and the footer only.
- **Also:** `404.html` kitchen link label said "planning ranges"; now "budget factors" (the kitchen page has no ranges). `about` and `terms` still mention planning ranges (later batch).

---

## 2026-11-19 — Page-content pass, batch B: town pages (not committed, not pushed)
Bethesda, Rockville, Potomac, Olney, one page at a time: source edit, `build.py --check`, deslop + facts grep,
screenshots at 390 and 1440. Owner note applied mid-batch: commercial content first (what can be remodeled,
layout / storage / comfort choices, scope differences, how to start), local permit facts in ONE short block with
links to the official source, one local permit question per FAQ, house situations written as conditionals.
- **Shared pattern, different content per town:** rooms block (`topic-list`), choices / cost-factor table
  (`range-table--scope`), services bento (shared fragment, unchanged), "how to start" (`media-split`), local
  block (`detail-list` with outbound links to DPS, WSSC, City of Rockville, Montgomery Planning), six FAQs equal
  to JSON-LD. No CSS change. `Service` schema node with town `areaServed` added to Bethesda and Rockville.
- **`/bethesda-md`** (primary: home remodeling bethesda md). Title "Home Remodeling in Bethesda, MD | Blue Hammer
  Remodeling"; H1 "Home remodeling in Bethesda, MD." Angle: more from the rooms the house already has. Table by
  service (choices / cost drivers). Local: County DPS + WSSC, historic status per property (Greenwich Forest as
  the example), Glen Echo town approval. Removed: "colonials and Cape Cods built between the 1930s and the
  1960s", Carderock Springs claims, "several municipalities and historic districts add their own review".
- **`/rockville-md`** (primary: home remodeling rockville md). Title "Home Remodeling in Rockville, MD | Blue
  Hammer Remodeling"; H1 "Home remodeling in Rockville, MD." Angle: smaller vs larger scope per room (table).
  Local: City vs County by address, with the City's own sentence about mailing addresses and its address finder;
  Historic District Commission. Removed: neighborhood list (West End, Fallsgrove, King Farm, Woodley Gardens),
  "We confirm the jurisdiction from your address first, so the schedule includes the right review".
- **`/potomac-md`** (primary: home remodeling potomac md). Title "Home Remodeling in Potomac, MD | Blue Hammer
  Remodeling"; H1 "Home remodeling in Potomac, MD." Angle: kitchen with pantry or scullery, primary suite, lower
  level; well and septic. Price table (four dollar ranges) is now a cost-factor table in the same grid. Removed:
  "twenty-five minutes away" and the travel FAQ, the den-without-closet septic suggestion, RE-2 "two-acre lots",
  named-community descriptions and HOA review claims, "we prepare the submission", "from the same team", the
  architect/designer FAQ that implied past Potomac projects. Septic FAQ now states the County's criteria only.
- **`/olney-md`** (primary: home remodeling olney md). Title "Home Remodeling in Olney, MD | Blue Hammer
  Remodeling"; H1 "Home remodeling in Olney, MD." Angle: home base; kitchen opened to the family room, primary
  bath, lower level. Price table (four dollar ranges) is now a cost-factor table in the same grid. Removed: the
  "five to seven months" FAQ, "in most Olney colonials that wall is load-bearing", "minutes from our base",
  "the kitchens ... we work on in Norbeck Grove, Hallowell ...", build decades, the egress and septic statements
  that had no source, "Brookeville is a designated historic district" (not verified; the page now says historic
  status is checked per property and that Brookeville and Laytonsville require town approval before the County
  application, per the DPS municipalities page).
- **Sources opened 2026-11-19** (all in `evidence.md`): DPS Home Improvements, Residential Alterations,
  Homeowners Permits, Municipalities, Historic Area Permit pages (new `department-permitting-services/` URLs);
  DPS Well and Septic guideline for additions/improvements (rev. Dec. 2025); Montgomery Planning HAWP page;
  Greenwich Forest HD amendment (2011); City of Rockville services, permit and historic-alteration pages; County
  DEP Glen Hills study page and the Potomac Subregion Master Plan excerpt; Olney Master Plan (2005).
- **Verification:** `python3 scripts/build.py --check` OK (23 pages, 0 problems) after every page. deslop 5/5 on
  all four. Facts grep (`$`, month, week, minute, licensed, insured, years) on the four sources: no hits.
  Playwright at 390 and 1440: no horizontal overflow, one H1, no broken images, no console errors; screenshots
  looked at. The 11 outbound source links return 200. Shared fragments in `build.py` were read and not changed.
- **Not verified / not done:** bh-qa not run as a separate agent. The old DPS `municipalities.html` URL redirects
  to the department home page (the new URL was used). No official text on basement egress or ceiling height.
- **Left for later batches (contradict the new town pages until fixed):** `service-areas` still names the
  Rockville neighborhoods, "two-acre estate lots" in Potomac, "many on well and septic" for Olney, and says
  "We prepare and file residential permits"; `faq` and `about` say "We prepare and file" / "We file them".
- **Needs Rodrigo**
  1. Subdivision and neighborhood names were taken off these four pages because nothing official ties them to a
     claim. If you want named neighborhoods back as plain service-area lists, say which ones.
  2. `olney-colonial-exterior-1440.webp` is still the 1200-px, 229 KB file (srcset says 1200w); re-export pending.

---

## 2026-11-19 — Page-content pass, batch C: Chevy Chase, Howard County, Kensington & Garrett Park, service areas, Silver Spring (not committed, not pushed)
One page at a time, same loop as batch B: source edit, `build.py --check`, deslop + facts grep, screenshots at
390 and 1440. Town pattern from Potomac / Olney: rooms as conditionals, services bento, ONE local block with
official links beside a choices / cost-factor table, how to start, six FAQs (house assessment, kitchen, bathroom,
basement, consultation, one local permit question). No CSS change.
- **`/chevy-chase-md`** (primary: home remodeling chevy chase md). Title "Home Remodeling in Chevy Chase, MD | Blue
  Hammer Remodeling"; H1 "Home remodeling in Chevy Chase, MD." Angle: more room inside the same walls (kitchen
  combined with the next room, added or rebuilt bathroom, basement with a low ceiling). Removed: the five dollar
  ranges, "We handle the paperwork and the neighbor notices", "We prepare both applications", the "30 minutes" FAQ,
  house decades and styles by village, "kitchens were built for staff", "seven-foot ceilings", construction-hour /
  parking / dumpster rules, "Parts of Chevy Chase sit in County historic districts", inspection-hole promise. Local
  block states only what the DPS municipalities list and the Town of Chevy Chase page say. Check OK, deslop 5/5.
- **`/howard-county-md`** (primary: home remodeling howard county md; "kitchen remodeling" worked into hero, first
  topic, FAQ and description). Title "Home Remodeling in Howard County, MD | Blue Hammer Remodeling"; H1 "Home
  remodeling in Howard County, MD." Angle: the rooms a household uses hardest; table of choices that move the budget.
  Removed: all dollar figures (incl. the $55k-$95k FAQ), "twenty minutes up Route 108" and the 20/25-minute FAQ, "We
  file and manage them", "Who pulls the permit? We do", River Hill / Maple Lawn / Columbia Association / HOA claims,
  house decades, "Most River Hill homes are on public sewer", the egress-bedroom answer. WSSC is not mentioned (its
  page names only Montgomery and Prince George's counties); gas is not mentioned (no Howard source). Check OK,
  deslop 4/5 (flagged lists are the department's name and the four permit types).
- **`/kensington-garrett-park-md`** (primary: bathroom remodeling kensington md; still a general two-town page).
  Title "Kensington & Garrett Park, MD Home Remodeling | Blue Hammer"; H1 "Home remodeling in Kensington and Garrett
  Park, MD." Angle: bathroom first (three bathroom scopes in the table), compact kitchen, basement. The two towns
  have separate items in the local block. Removed: five dollar ranges, "twenty minutes from our base" (twice),
  "Garrett Park's entire town" / "The whole town is a historic district", house decades and styles, the neighborhood
  list (Parkwood, Rock Creek Hills, Kensington Heights, Homewood), "We check early and prepare the application",
  "We coordinate them with the County permit", "We measure to the quarter inch". Check OK, deslop 5/5.
- **`/service-areas`** (primary: home remodeling montgomery county md). Title "Home Remodeling in Montgomery County,
  MD | Blue Hammer"; H1 "Home remodeling in Montgomery County, MD." Each area group now routes to its town page in a
  sentence that matches that page. Removed: Rockville neighborhood names, "Two-acre estate lots", "many on well and
  septic", "Town of Brookeville adds its own historic review", "Twenty to thirty minutes up Route 108", "We handle the
  paperwork", "We prepare and file residential permits", and the whole "Closer means better" block (trade partners
  "who have worked in 1930s Chevy Chase colonials", vendor claims), replaced by "What to send with your address".
  Hero CTA is "Schedule a Consultation". The Howard pill now reads "Howard County"; Clarksville is a ZIP pill.
  Check OK, deslop 4/5 (place-name lists and the DILP name).
- **`/silver-spring-md`** (new, owner request; primary: home remodeling silver spring md). Title "Home Remodeling in
  Silver Spring, MD | Blue Hammer Remodeling"; H1 "Home remodeling in Silver Spring, MD." Angle: room by room or in
  phases (what to prepare for the next phase; table "How phasing shapes the budget"). Local block: Silver Spring is
  not on the County's municipalities list, so County DPS + WSSC; the County's Silver Spring regional office area
  includes all of the City of Takoma Park, which is on the list; historic status per property; private covenants.
  Images are existing ones with neutral alt text (`hero-kitchen`, `basement-lower-level`). No ZIP codes or
  neighborhood names (none verified). Check OK, deslop 5/5.
  - `scripts/build.py`: "Silver Spring" removed from `FORBIDDEN`; added to `NAV_AREAS` (header dropdown and footer,
    after Rockville) and to `AREAS` (business `areaServed`). In the sitemap (priority 0.9) and on the hub.
  - Retirement redirects `/silver-spring-md(.html) -> /service-areas` removed from BOTH `netlify.toml` and
    `blue_hammer_remodeling_site/_redirects` (they agree). The URL was a page before, so no new redirect is needed.
- **Sources opened 2026-11-19** (all in `evidence.md`): DPS municipalities page (re-read), Town of Chevy Chase
  Building & Permitting, WSSC homeowner page (re-read for jurisdiction), Howard County DILP sample-descriptions
  handout (11.05.2025), Howard County Health Department floor-plan memo (2017), Howard County Historic Planning,
  Town of Garrett Park Permits and Historic Preservation pages, Town of Kensington resident FAQs, Silver Spring
  Regional Services Center "About us", Montgomery Planning "About Silver Spring" and Woodside Locational Atlas page
  (the last two opened, not cited).
- **Verification:** `python3 scripts/build.py --check` OK after every page (24 pages, 0 problems at the end). Facts
  grep (`$`, month, week, minute, licensed, insured, years) on the five sources: no hits. Playwright at 390 and
  1440 on the five pages: no horizontal overflow, one H1, no broken images, no console errors; screenshots looked
  at. The 13 outbound links return 200. Every built page links to `/silver-spring-md` through the nav.
- **Not verified:** Chevy Chase Village's own permit page (site not reached through search or guessed URLs); the Town
  of Kensington permit page (404 on two URLs; the resident FAQ was used); whether interior work needs a town permit
  in Kensington or Garrett Park; an official sentence calling Silver Spring "unincorporated" (the page says "not on
  the County's list of municipalities" instead). bh-qa not run as a separate agent.
- **Still contradicting these pages (final batch):** `faq` (dollar ranges, "We prepare and file the application",
  "Howard corridor", "Chevy Chase, Kensington, Garrett Park and Brookeville add their own review for exterior or
  historic work", Rockville "West End, Fallsgrove and King Farm"; its area answer omits Silver Spring); `about`
  ("We file them", "Carderock Springs beam ceiling", "heart pine in Kensington"); `process` ("We file with ...");
  `projects` (captions tying images to Kensington / Garrett Park "tall-ceilinged Victorians" and house decades; meta
  lists towns); `contact` (area list omits Silver Spring); `terms` and `.agents/product-marketing.md` (planning
  ranges). `services` says "the Howard County corridor" (harmless). `.claude/agents/bh-seo-content.md` and the agent
  brief still call Silver Spring a non-priority market; `AUDIT-2026-11-18.md` items 0.3 / 4.4 predate the owner's
  request.
- **Needs Rodrigo**
  1. Silver Spring ZIP codes / neighborhoods to name on the page and the hub, if wanted (none were verified).
  2. Agent definitions still say "Silver Spring is not a priority market"; update them if the page stays.

---

## 2026-11-19 — Page-content pass, final batch + gate (not committed, not pushed)
Process, FAQ, about, projects, contact, reviews, legal pages, shared fragments, docs. Same loop per page: source edit,
`build.py --check`, deslop + facts grep, screenshots at 390 and 1440 looked at. Copy only; no restyle, no CSS change.
- **`/process`** Title "Our Remodeling Process, Step by Step | Blue Hammer Remodeling"; H1 "Our process, step by step."
  Removed: the timelines panel ("3–4 months", "5–7 months", "5–8 months"), "In 1920s–1990s homes we often find...",
  "We file with Montgomery County DPS, the City of Rockville or Howard County DILP", the temporary-kitchen and
  always-one-working-bathroom promises, "3D views", "ordered and checked on arrival", "Dust barriers and floor protection
  go up first", warranty documentation, "we check in once you have lived with it", the Kensington / Clarksville job
  examples. Added: "What sets the schedule" (four factors, no durations), "What is behind the walls", permit office by
  address with "who applies for each is written into the agreement", conditional answers (if the kitchen / the only
  bathroom / a second bathroom is involved, the plan needs to cover...).
- **`/faq`** Title "Remodeling FAQ: Budget, Schedule & Permits | Blue Hammer"; H1 "Remodeling questions, answered
  directly." 17 questions in three groups; one FAQPage node equal to the visible text. Removed: every dollar range,
  every duration, "Do you give free estimates?", "We prepare and file the application", "the rest of the Howard
  corridor", "Chevy Chase, Kensington, Garrett Park and Brookeville add their own review...", Rockville's "West End,
  Fallsgrove and King Farm", "Many clients come to us", "vendors across Montgomery and Howard County", "Is Blue Hammer
  licensed and insured?" with "as soon as it is confirmed for display", and the photos question. Added: budget factors
  per service, schedule factors, permits by address (links to DPS, WSSC, the County municipalities list), the areas
  answer with Silver Spring (same list as `/service-areas`), "How do I check a remodeling contractor's credentials in
  Maryland?" (MHIC, its public license search, confirm with the person responsible before signing; nothing says Blue
  Hammer holds a license).
- **`/about`** (owner notes applied) Title unchanged; H1 "About Blue Hammer Remodeling." Removed: the roofline sentence
  (the mark has none), the founding story, "trade partners who know 1930s plaster", the material specifications and "what
  we would put in our own homes", "heart pine in Kensington", "Carderock Springs beam ceiling", "We file them and schedule
  the inspections", "We would rather do fewer projects well...", and the whole "What you will and won't find on this
  site" block (no invented reviews / no borrowed photos / planning ranges / licensing). New last section "What to expect
  when you work with us": written scope, choices explained, clear communication, next step. Olney base kept in the hero.
- **`/projects`** Title unchanged; H1 "Kitchen, bath and basement design gallery." All twelve captions and the hero now
  describe room, layout and materials only. Removed: every town link and name, "1920s–40s", "1950s Bethesda Cape Cod",
  "tall-ceilinged Victorians and kit houses", "King Farm, Fallsgrove and North Potomac", "pre-war colonials, mid-century
  Capes, 1990s customs and new estates", "a real egress window". Meta description no longer lists towns.
- **Alt text, site-wide:** "Renovated 1920s colonial kitchen", "Renovated 1950s hall bathroom", "Luxury estate kitchen",
  "Victorian kitchen", "Remodeled kitchen", "freshly installed", "egress window", "Brick center-hall colonial" replaced by
  plain descriptions (sources and the shared services block in `build.py`).
- **`/contact`** H1 "Contact Blue Hammer Remodeling." Area list now includes Silver Spring and says other addresses are
  confirmed by ZIP code; removed "meet clients", "the right team", "we will tell you straight away"; DC / Virginia answer
  matches `/service-areas`.
- **`/reviews`** `noindex,follow` and `"sitemap": false`; URL, footer link and breadcrumb kept; no review content. H1
  "Client feedback for Blue Hammer." Checklist now links the MHIC license search; removed "Permits in their name",
  "workers' compensation certificates naming you", "warranty", "References". `build.py --check` now fails if a page with
  the empty-reviews block is indexable. Sitemap: 21 URLs.
- **`/terms`** "Cost ranges on this site" is now "Budget information on this site"; "Consultations and estimates" is
  "Consultation requests"; removed "licensing and insurance documentation ... and warranty". **`/404`**: one sentence.
  **`/privacy`, `/thank-you`**: read, nothing to remove, unchanged.
- **Shared (`scripts/build.py`)**: repair note reworded (no "often", no "same standard"); services-block kitchen alt;
  business `knowsAbout` reduced to the three services; `FORBIDDEN` gained "planning range" / "cost ranges". Header,
  footer, form and consultation section were read and left as they are (Silver Spring was already in both nav lists).
- **Other pages touched for consistency:** home area list (+ Kensington & Garrett Park, Silver Spring); `/services`
  (names Silver Spring, "Typical scope" -> "Scope", one intro sentence); Kensington (second-bathroom sentence is now
  conditional); Howard County ("rarely"), Chevy Chase (engineer / permit statement), Potomac (heated floor), basements
  ("work that needs a permit").
- **Docs:** `docs/seo-keyword-map-2026-11-19.md` rewritten as the implemented map (titles, H1s and robots read from the
  built files; CSV numbers and the caveats section unchanged). `DESIGN.md`, `docs/brand.md`,
  `docs/design-system/design-brief.md`: note that the live identity is v2 (navy / orange / royal, Barlow Condensed +
  Switzer) and the palette A / Gambetta text is history. `.agents/product-marketing.md` v1.2: no planning ranges.
  `README-START-HERE.md`: Silver Spring is a live page. `.claude/agents/*`, `CLAUDE.md` and settings were not edited.
- **Source opened 2026-11-19** (in `evidence.md`): Maryland Home Improvement Commission page (Maryland Department of
  Labor) and its Home Improvement Public Query (license search), both HTTP 200.
- **Site-wide sweep (24 pages, source and output)** for `$` amounts, durations, travel minutes, "planning range",
  "we file / handle / prepare / often", "licensed", "insured", "years", "our clients", "completed", "award", "best",
  "team", "estimate", "warranty": none left in page copy. Kept, with reason: form options "Within 1–3 months" /
  "Within 3–6 months" (the homeowner's own choice); "© 2026" and "Last updated" dates; footer link "Client feedback";
  footer line "...any required permits or licenses are confirmed in writing..."; "Department of Inspections, Licenses and
  Permits" (official name); "a plumber who holds a WSSC Water license" (WSSC source); MHIC guidance on `/faq` and
  `/reviews`; `/terms` "Maryland home improvement contractors must hold ... (MHIC) license" (MHIC source) and its Design
  images paragraph; `/privacy` "No system can guarantee absolute security"; "day to day" / "every day" as plain words;
  "often" / "usually" in scope descriptions on the service pages (batch A).
- **Gate:** `python3 scripts/build.py --check` OK, 24 pages, 0 problems. deslop 5/5 on process, about, contact, reviews,
  terms; 4/5 on faq and projects (flagged lists are the literal "Permits, credentials and service area" and "Kitchen,
  bath and basement"). **bh-qa (independent, read-only), run 1: FAIL** on three items: Kensington "the two are remodeled
  one after the other"; terms "licensing and insurance documentation ... warranty"; alt "Brick center-hall colonial" on
  the Olney and service-areas hero. All three fixed, plus its minor notes. **bh-qa run 2: PASS**, no blocking failure;
  its three wording advisories were applied afterwards (services intro, "crew", "inspiration images") and the build
  check re-run. **Design check** (one independent reviewer covering the five checklists at 390 / 768 / 1024 / 1440,
  measured): 5 of 5 PASS. Its copy-fit notes were fixed (process and reviews H1 no longer leave a word alone on a line;
  short gallery caption lengthened).
  Redirects: `netlify.toml` and `_redirects` carry the same 3 host rules and 5 internal-file rules; no silver-spring rule.
- **Not verified / depends on a deploy:** nothing is deployed, so the Semrush audit numbers (including the schema
  errors reported there) are unchanged until a deploy and a re-crawl. Rankings and indexing were not measured. Netlify's
  handling of the `noindex` page and the extensionless URLs was checked only on the local preview. The Potomac septic
  sentence "requires a septic permit record on file" follows the County guideline but the guideline also describes a
  path when no record exists.
- **Design-check notes left as they are (shared components, not copy):** header and mobile-bar CTA point to the home
  page form on every page, including `/contact`; the fixed CTA bar shows on `/thank-you`; `bh-hammer-v2.png` is 73 KB for
  a 62 px mark; unused Gambetta `@font-face` rules remain in `main.css`; the consultation section keeps its eyebrow;
  some `/process` and `/faq` paragraphs run past 60 words.
- **Needs Rodrigo**
  1. Phone, public email, MHIC number and review profile are still empty in `site-config.js` (hidden on the site).
     Maryland requires an MHIC license to contract home improvement work with homeowners.
  2. Image files still carry town / decade names (`kitchen-chevy-chase-1920s`, `kitchen-kensington-victorian`,
     `kitchen-potomac-estate`, `kitchen-rockville-contemporary`, `bath-bethesda-hall`, `kitchen-howard-county`,
     `olney-colonial-exterior`). The visible text and alt text are neutral; renaming needs redirects or a cache check.
  3. The Olney and service-areas heroes show a house exterior. The alt is neutral now; an interior image would remove
     any reading of it as a local house.
  4. `CLAUDE.md` and `.claude/agents/bluehammer.md` may still describe the old identity and scope; not edited here.
  5. Sandy Spring 20860 is on `/service-areas`, `/olney-md` and in `areaServed` but not in the HARD-RULES tier list.
  6. Review, then commit and deploy; re-crawl in Semrush afterwards.

## 2026-11-19 — Published: SEO content pass (commit 0a9e24f)
- Commit 0a9e24f pushed to main (fast-forward from e455100, no force). Owner authorized after his own review.
- Live check on https://bluehammermd.com after the Netlify deploy (curl, no form submitted): `/`, `/kitchen-remodeling`,
  `/bathroom-remodeling`, `/basements-interiors`, `/silver-spring-md` return 200 with the new H1s and extensionless
  canonicals; `/reviews` is `noindex,follow`; `sitemap.xml` has 21 URLs, includes silver-spring-md, no reviews, no `.html`.
- Not measured: Semrush audit counts (need a re-crawl), rankings, indexing.

## 2026-11-19 — Post-publication: Semrush re-run (observed by the owner) and two final corrections
- Owner re-ran the Semrush site audit after the deploy and reported: 27 URLs crawled; Site Health 99% (was 95);
  AI Search Health 89% (was 88); Errors filter = 0 / nothing found; Markup 100% (was 60); Internal Linking 100%
  (was 96). The old `serviceType` detail was confirmed as the schema cause.
- Still listed by Semrush: 44 unminified JS/CSS warnings, 1 missing llms.txt, 1 blocked, 4 external resources 403.
  Not addressed (no minifier in the repo; llms.txt is not a Google requirement).
- Potomac septic FAQ: the absolute "requires a septic permit record on file" now follows the County guideline and
  covers the no-record case (tests to establish a reserve area + new system). Source re-read and evidence.md updated.
- docs/seo-keyword-map-2026-11-19.md status set to published.

## 2026-11-20 — Technical step 2: minified CSS/JS, llms.txt, CTA targets, unused font rules (not committed, not pushed)
Technical only: no copy, no keyword work, no new pages, no contact details, no redesign. Commit hash and live check: to be added by the owner.
- **Asset pipeline.** Readable sources moved with `git mv` to `site-src/assets/main.css`, `main.js`, `site-config.js`.
  `scripts/build.py` minifies each with **esbuild 0.28.2** (exact pin in `tools/package.json` + lockfile; the only new
  dependency) into `blue_hammer_remodeling_site/assets/` under the same names, so URLs and the `?v=<sha256[:12]>` cache
  buster are unchanged. Flags: `--minify --legal-comments=none --log-level=warning --loader=css|js --sourcefile=<src>`,
  stdin to stdout; CSS `--target=chrome108,edge108,firefox121,safari15.4` (the floor the stylesheet already needs:
  `:has()`, `dvh`); JS `--target=es2020` (newest syntax in `main.js` is `?.`). No `--bundle`, no `--format`, no
  source map, ASCII-only output. `main.js` is still a classic deferred script; `window.BLUE_HAMMER_CONFIG` is still a
  global. Netlify still runs no build: the minified files are committed.
- **Bytes (raw / gzip -9).** `main.css` 60,726 / 13,168 -> 57,019 / 11,837. `main.js` 16,856 / 5,523 -> 11,885 / 4,368.
  `site-config.js` 757 / 484 -> 192 / 199. Total 78,339 / 19,175 -> 69,096 / 16,404. (Minify alone, before the font
  rules were removed, gave `main.css` 57,326 / 11,844.)
- **`--check` now also fails** when a published asset differs from a fresh minify of its source (it never rewrites
  the assets; the message names the `site-src/assets/` file to edit and says to run `python3 scripts/build.py`), when
  a `.map` is published, and on `llms.txt` problems. Both `build.py` and `build.py --check` stop with
  "Install the pinned dev tools first: npm --prefix tools ci" when esbuild is missing or is not the pinned version.
  Workflow change: after editing a file in `site-src/assets/`, run `python3 scripts/build.py`, then `--check`.
- **Unused font CSS.** The four `@font-face` "Gambetta" rules were removed from `site-src/assets/main.css`. Proof in
  Chrome on the built site, all 24 pages x 390 and 1440 x reduced motion and motion allowed (96 loads): no element
  or pseudo-element with a computed `font-family` starting with Gambetta, no rule naming Gambetta except the four
  `@font-face` rules and the overridden `:root{--font-display}`, every Gambetta face `unloaded`, no
  `gambetta-*.woff2` request; `--font-display` resolves to Barlow Condensed. Re-run after the removal: 0 violations.
  The variable cascade was left as it is. The four `assets/fonts/gambetta-*.woff2` files were NOT deleted; nothing
  on the site references them any more.
- **`llms.txt`** generated by `build.py` at `blue_hammer_remodeling_site/llms.txt`: H1, one blockquote summary, H2
  Services / Service areas / Company, 21 `- [Title](URL): description` lines = the sitemap set. Titles and
  descriptions are each page's existing `<title>` (brand suffix dropped) and meta description. Not in the sitemap, no
  `llms-full.txt`, `robots.txt` byte-identical.
- **CTA targets.** Header button, in-menu button, footer "Schedule a consultation" and the fixed mobile bar now share
  one target per page: `#consultation` on the 20 pages with the shared consultation section, `#contact-form` on
  `/contact`, `/#consultation` on `/privacy`, `/terms`, `/404`, `/thank-you`. `/thank-you` renders no fixed mobile
  bar (`"mobileCta": false` in its meta, `body.no-mobile-cta`, one appended CSS rule that drops the 96px reserved
  under the footer; `.footer-bottom` padding-bottom is 14px there at 390). `main.js` logic was not changed.
- **Files.** Moved: the three asset sources. New: published `assets/main.css`, `main.js`, `site-config.js`
  (generated), `llms.txt`. Changed: `scripts/build.py`, `site-src/pages/thank-you.html`, all 24 generated HTML pages
  (CTA hrefs and `?v=` hashes; thank-you also loses the bar), `tools/package.json`, `tools/package-lock.json`,
  `README-START-HERE.md`, `DESIGN.md`, `docs/brand.md`, `docs/design-system/design-brief.md`,
  `docs/design-system/anti-slop-copy.md`, `docs/design-system/references/inspiration.md`,
  `.agents/product-marketing.md`, `tools/remotion/src/brand.ts` (comment).
- **Checks.** `python3 scripts/build.py --check`: OK, 24 pages, 0 problems, run twice with no further change in
  `git status`; build output byte-identical across runs. Stale-asset test and missing-esbuild test: both fail with
  the messages above. CSS equivalence in Chrome's CSSOM: source and minified stylesheet give the same 5,081
  selector/declaration pairs in the same order (`translateX(n)` vs `translate(n)` and whitespace normalised).
  Minified `main.js` at `es2020` is byte-identical to the `esnext` output, so nothing was lowered. Browser
  (Chrome via Playwright, preview on 8770): 0 console errors or warnings, failed requests or 4xx on the 17 listed
  pages at 390 and 1440; desktop Services / Service Areas dropdowns (click, arrow keys, Escape + focus return);
  390 menu toggle, dropdowns, link click closes the menu; header / menu / bar CTAs on `/`, `/kitchen-remodeling`,
  `/contact`, `/faq` keep the pathname and show the form below the sticky header, `/privacy` goes to
  `/#consultation`; `/contact` CTA also works with JavaScript off; FAQ details on `/faq` and `/bethesda-md`, one
  FAQPage node each; gallery filters (12 / 6 / 3 / 3 cards); home video attaches and plays with motion allowed,
  the motion toggle pauses and resumes, nothing loads with reduced motion; phone / email / license slots empty and
  hidden, honeypot 0x0. The form was never submitted (POST blocked in the test contexts). 41 of 42 scripted checks
  pass; the one failure is the existing behaviour listed below.
- **Before / after screenshots** (17 pages x 390 and 1440, reduced motion): 31 of 34 pairs pixel-identical with
  identical computed styles and `scrollHeight`. `/thank-you` 390: expected (bar gone, height 2262 -> 2180);
  `/thank-you` 1440: 0 pixels, only the `.mobile-cta` style entry is now absent. `/about` 390 (164 px) and
  `/bethesda-md` 390 (556 px): same size, same computed styles, differences of at most 20/255 scattered inside
  photographs and on anti-aliased corners. This is raster noise: `/about` and `/projects` 390 flip between two
  such states on the unchanged tree, and a copy of the HEAD site served separately produced a `/bethesda-md` 390
  screenshot byte-identical to the one from the final build. Pixel equality of photographs is not guaranteed by
  this method.
- **bh-qa (independent, read-only), one run: PASS** on build, diff review, hard rules and browser spot check; no
  failure. Its advisories, left as they are: `--font-display` still lists Gambetta first in the overridden
  declaration; the "llms.txt differs from generated" check cannot fire because the file is rewritten first; with a
  stale asset `--check` rewrites the pages with the stale hash before failing.
- **Existing behaviour found, not changed (out of scope):** at 390, tapping "Service Areas" while "Services" is
  open closes both instead of opening the second (the first panel collapses on focus-out and the tap lands
  elsewhere). Same on the live site before this step.
- **Not verified:** nothing is deployed, so Netlify's serving of `llms.txt` and of the minified files was checked
  only on the local preview. Site-audit tools: not measured until a re-crawl (the last recorded result is the
  2026-11-19 entry above). Safari and Firefox were not run (Chrome only); the only CSS addition esbuild makes for
  the chosen targets is `-webkit-user-select:none` next to `user-select:none` on `.watermark`. No Lighthouse run.
- **Operational references (done after the agent run, on the owner's instruction to update every reference):**
  `CLAUDE.md`, `.claude/agents/HARD-RULES.md`, `bh-orchestrator.md`, `bh-designer.md`, the `bh-design-loop` and
  `blue-hammer-website` skill files and `~/.claude/agents/bluehammer.md` now name `site-src/assets/` as the place to
  edit and say the published copies are generated. Path and build-command lines only.
- **Needs Rodrigo**
  1. Phone and public email stay empty until he provides them; when he does, edit `site-src/assets/site-config.js`
     and run `python3 scripts/build.py`.
  2. Anyone building on another machine runs `npm --prefix tools ci` once.
  3. Re-crawl in the site-audit tool when access is available; nothing was measured after this step.

- **Published:** commit 03f00f6 pushed to main (fast-forward from 81bcea4, no force). Live check on https://bluehammermd.com
  after the Netlify deploy (curl only, no form submitted): `/llms.txt` returns 200 `text/plain` and is byte-identical to
  the repo file; `assets/main.css` (57,019 bytes), `main.js` (11,885) and `site-config.js` (192) are byte-identical to
  the repo and served with new `?v=` hashes; no Gambetta `@font-face` in the live CSS; header, menu and footer CTAs are
  `#consultation` on `/`, `/kitchen-remodeling`, `/faq`, `#contact-form` on `/contact`, `/#consultation` on `/privacy`
  and `/thank-you`; `/thank-you` has no mobile bar; `robots.txt` unchanged; sitemap has 21 URLs. Site-audit result:
  not measured.

## 2026-11-20 — Redesign phase 1: homepage + shared components (not committed, not pushed)
Owner brief: "focus on design, remove everything that looks made by AI. I need a designer", then "trust, modern and
traditional at the same time" (traditional in the identity, modern in the presentation). Direction, references and
the rules for the next phases: `docs/design-system/design-brief.md` > "2026-11-20 direction".
- **References studied (layout only, nothing copied):** casedesign.com, anthonywilder.com, bowa.com (as the pattern
  to avoid); gibsonbuilders.com did not respond.
- **CSS.** `site-src/assets/main.css` rewritten as ONE layer (the v1 layer, the v2 override layer and the "pass 4"
  block are gone; 47 unused classes deleted: `.hero*`, `.tiles`, `.watermark`, `.cards-3`, `.pill`, `.areas-*`,
  `.feature-*`, `.steps-motion`, `.bh-*` and others). Published size 57,019 -> 34,426 bytes. Tokens: one `:root`
  (navy / royal / orange / ink / muted / line / soft, type sizes, `--sec`, `--sec-tight`, `--gap`, `--gutter`,
  `--max` 1240). Headings: Switzer 600 sentence case; Barlow Condensed 800 only in the logo wordmark and the H1
  (sentence case). No uppercase heading, no eyebrow, no orange rules or dots. `--field-line` darkened to `#74859A`
  (input borders now 3:1 on white).
- **Chrome (`scripts/build.py`).** Topline strip removed (phone slot moved into the header, hidden while empty).
  Header 76 px. Consultation section: grey, H2 "Schedule a consultation", one sentence, three plain lines, the
  same two-step form (`lead_form` untouched: name `consultation`, honeypot `companyWebsite`, all field names).
  Footer: three wrapped link rows with the same links, one bottom line; 397 px tall at 1440 (was about 840).
- **Home (`site-src/pages/index.html`).** H1 "Home remodeling. / In Maryland." (same words, sentence-case Barlow,
  no blue second line) and one button on white above one wide static photograph with a caption; the hero video,
  its pause button and the eyebrow are gone (video files kept). Services: mosaic of three photographs of different
  sizes with captions below, each article one link. Process: three numbered text rows on grey. Areas: town index
  and one house photograph. Four questions (same `<details>`, FAQ JSON-LD unchanged). No image is used twice.
  Images: hero `bh-kitchen-v2`, kitchen `kitchen-kensington-victorian`, bath `bh-bathroom-v2`, basement
  `bh-basement-v2`, areas `olney-colonial-exterior`. Captions name only what the picture shows.
- **Copy replaced on the home page (old -> new).** Eyebrows "Blue Hammer Remodeling · Olney, Maryland", "What we
  do", "How it works", "Close to home", "Before we begin", "Let's talk about your home" -> removed. "Make room for
  what's next." -> "What we remodel". "A clear path from idea to home." -> "How a project is planned". "Based in
  Olney. Built around your home." -> "Where we work". "A few things you may be wondering." -> "Questions before a
  remodel". "Ready to make your space work better?" -> "Schedule a consultation". "Your priorities. A written
  scope. A clear next step." and "Thoughtful spaces for everyday living." -> removed (photo caption instead).
  Step titles "Tell us your vision / Plan the details / Bring it to life" -> "First conversation / Layout,
  materials and a written scope / Construction and walk-through". Service summaries now say one specific thing
  per room, taken from the service pages. No fact, permit statement, price, duration or credential was added.
- **`main.js`.** (1) Mobile menu bug fixed: `focusout` no longer collapses a dropdown below 1061 px (the panel is
  in the page flow there, so collapsing it on pointer-down moved the rows under the finger and the tap missed);
  a tap on a plain row inside the open menu no longer closes the open dropdown. Desktop behaviour unchanged.
  (2) ArrowDown / ArrowUp on a dropdown button skipped one item (the key event was handled twice): fixed.
  (3) The fixed mobile bar hides while a primary button or the form is on screen (`.is-idle`).
- **Checks.** `python3 scripts/build.py --check`: OK, 24 pages, 0 problems (21 indexable; sitemap, llms.txt,
  robots.txt and `__forms.html` unchanged). Chrome via Playwright on the 8770 preview, reduced motion: all 24
  pages at 320, 390, 768 and 1440 (96 loads): `scrollWidth` equals the viewport everywhere, no element outside
  the viewport, no heading with `text-transform: uppercase`, 0 console errors, failed requests or 4xx. 31 scripted
  checks pass: 390 touch menu (Services <-> Service Areas switching, own-button close, Escape + focus return,
  link under an open dropdown navigates, tap outside closes), mobile bar idle / shown / target, form step 1 -> 2
  with the field names, honeypot and empty contact slots, desktop click / outside click / ArrowDown / ArrowUp /
  Home / End / Escape / Tab-out, one CTA in the header, every caption below its photo at 768 / 1024 / 1440. No
  POST was sent (blocked in the test contexts). Contrast: muted text 6.5:1 on white and 6.0:1 on grey, royal
  links 5.5:1 / 5.1:1, button text 6.5:1, footer text 11:1. Anti-slop checker on the home page: 4/5, the one
  flag is the list of the four real services ("Kitchens, bathrooms, basements and interior rooms"), accepted.
- **Screenshots.** `scratchpad/redesign/phase1/<page>-<width>.png` for home, kitchen-remodeling, bethesda-md,
  contact, faq at 390 / 768 / 1440, plus `home-320.png`.
- **Not done / not verified.** Chrome only (no Safari or Firefox run). No Lighthouse run. The project's five-agent
  design check and critic loop were not launched from this run; the coordinator's independent reviewers looked at
  the homepage instead and their findings were applied (useful service copy, unverifiable material names removed
  from captions, captions below photos, 320 px overflow, mobile H1 size). Nothing is deployed.
- **What the other 23 pages still need (later phases, one page at a time).** They share the new type, color,
  header, consultation and footer, but keep the previous layouts: the same two-column hero with a photo bleeding
  right on 18 pages, the same split / table / photo-split / FAQ sequence on the three service pages and the nine
  town pages, the `.bento` services block on nine pages, slogan-style H2s ("Planned first. Built to the plan.",
  "Your next space starts with a direction.", "From first idea to finished room."), no captions on any
  photograph, one repeated image on `/projects`, bordered boxes on `/reviews`, inline styles on `/thank-you`.
  Old agent files (`bh-designer.md`, `bh-orchestrator.md`, `bh-design-loop`) still name Gambetta / palette A.
- **Needs Rodrigo.** Phone, public email and MHIC number stay empty (unchanged). The hero photograph is 1402 px
  wide; a larger original would hold up better on very large screens.

## 2026-11-20 — Redesign phase 2: the 23 interior pages (not committed, not pushed)
Same owner brief and direction as phase 1 (`docs/design-system/design-brief.md` > "2026-11-20 direction"). Every interior
page was recomposed from its own content; none keeps the old two-column hero, `.split`, `.media-split` or `.bento`.
- **Shared components (neutral names, `site-src/assets/main.css` section 5).** The home patterns were generalised and the
  homepage re-rendered identically at 1440 (pixel-equal) before any other change: `.home-head` -> `.sec-head`,
  `.home-steps` -> `.steps`, `.home-area-list` -> `.link-index`, `.home-areas-grid` / `.home-faq-grid` -> `.cols-5-7`.
  New: `.page-head` (H1 + introduction on white, `--stack`, `--plain`), `figure.photo` (frames `--wide`, `--band`, `--43`,
  `--tall`, `--fill`; focal point `.at-low`, `.at-right`), `.photo-pair`, `.cols-7-5`, `.rows` / `ol.rows--num`, `.trio`,
  `.notes`, `.feature` (`--flip`, `--index`), `.callout`, `.aside-note`, `.town-links`, a 12-column `.gallery-grid`.
- **Templates.** Service page, town page, hub (services, service-areas), editorial (about, process), FAQ, gallery,
  utility (contact, reviews, thank-you, legal, 404). Pages of one type share components but not the order or the
  composition. Section order by page (T topics, B budget table, P permits, C how to start, F questions):
  kitchen T(numbered) / photo pair / B / C+photo / P / F; bathroom photo-pair lead / C / T / photo+B / P / F; basement
  photo+T(notes) / B / C+photo / P / F; Olney T / photo pair / P / B / C / F; Bethesda B / T / C+photo / P / F; Potomac
  T as three photo rows / C / P / B / F; Chevy Chase P / T / B+photo / C / F; Rockville P / B / T+photo / C / F; Silver
  Spring T / B / C+photo / P / F; Kensington and Garrett Park T / P / B / C / F; Howard County T / C+photo / B / P / F.
- **Images.** Every content photograph is a `<figure>` with a caption below that names only what the picture shows. No
  image twice on a page; the eight town pages no longer share one trio (the `.bento` block and `{{SERVICE_CARDS}}` are
  gone; the three service links stay in each page's topic headings or table, the small-repair link as one sentence).
  `consultation-scene`, `hero-craftsman` and `design-gallery-collage` are not used. No image was generated or added.
- **Headings.** Sentence case, no trailing period on H2/H3, no slogans. H1 wording of service and town pages
  unchanged. Only H1 changed: `/faq` "Remodeling questions, answered directly." -> "Remodeling questions and answers."
  Titles, meta descriptions, canonicals, routes: unchanged (the 24 meta lines are byte-identical). FAQ questions and
  answers: byte-identical. No internal link was lost (checked per page against the phase 1 sources).
- **Home.** One fix requested during the run: the "We also take on small repairs" line now sits directly under the
  "Basements and interiors" summary (it was pinned to the bottom of the column, leaving a gap). Mosaic unchanged.
- **Removed.** CSS: `.interior-hero`, `.interior-grid`, `.illustration-frame`, `.grid-2`, `.split`, `.faq-split`,
  `.media-split*`, `.topic-list`, `.bento`, `.room*`, `.repairs-note`, old `.steps` / `.step*`, `.timeline*`,
  `.info-panel`, `.area-group`, `.city-pills`, `.gallery-card-body`, `.contact-grid`, `.review-empty` box,
  `.section-head`, `.section-heading`, `.title-pair`, `.form-status.success`. JS (`main.js`): `initMotion`,
  `initMedia` (hero video and scroll reveal, referenced by nothing) and `svgCheck`; video files stay on disk.
  `scripts/build.py`: the unused `service_cards()` helper and its placeholder. No inline `style` is left in any page
  source. Published sizes: `main.css` 34,426 -> 34,574 bytes, `main.js` 12,395 -> 8,465 bytes.
- **Checks (run once at the end).** `python3 scripts/build.py --check`: OK, 24 pages, 0 problems; sitemap 21 URLs,
  llms.txt 21 URLs. Chrome (cached Playwright Chromium build, 8770 preview, reduced motion), all 24 pages at 320, 390,
  768 and 1440 (96 loads): `scrollWidth` equals the viewport, nothing outside the viewport, no uppercase heading, no
  H2/H3 ending in a period, every content image inside a figure with a caption below it, no repeated image on a page,
  no inline style, 0 console errors, failed requests or 4xx. 35 interaction checks pass: desktop dropdowns, 390 touch
  switching Services <-> Service Areas, FAQ details, gallery filter 12 / 6 / 3 / 3 / 12 with full rows under every
  filter, form step 1 -> 2 -> Back with field names, form name and honeypot on `/kitchen-remodeling`, `/olney-md` and
  `/contact`, CTA targets, empty phone / email / license slots. 0 POST requests. No new color pair was introduced
  (text uses the phase 1 tokens measured then: muted 6.5:1 on white / 6.0:1 on grey, royal 5.5:1 / 5.1:1).
- **Screenshots.** `scratchpad/redesign/phase2/<page>-390.png` and `-1440.png` for all 24 pages.
- **Not done / not verified.** Chrome only; no Safari or Firefox run (the gallery pattern uses `:nth-child(n of S)`;
  browsers without it fall back to two equal columns). No Lighthouse run. The anti-slop checker and the five-agent
  design check were not run. The page generators used for the conversion are one-off scripts in the scratchpad; the
  page sources in `site-src/pages/` are plain HTML as before. Nothing is committed or deployed.
- **Weak spots left.** `/service-areas`: the Silver Spring and Howard County rows repeat the group name as the link.
  `/faq`: the second and third groups have no note under their heading, so the left column is short. `cabinetry-detail`
  is half out of focus and is used at a large size on `/chevy-chase-md`. Photographs repeat across pages (17 usable
  files for 24 pages). The old agent files still describe Gambetta / palette A.
- **Needs Rodrigo.** Phone, public email and MHIC number stay empty (unchanged). Real project photographs would
  replace the repeated ones.

## 2026-11-20 — Redesign: final independent gate and fixes
- One independent read-only critic/QA pass over the 24 pages (design by eye, copy against HARD-RULES, keyboard,
  contrast, tap targets, images, CTA targets, internal links). Verdict: one blocking item, fixed: `/projects` lede
  named a wood species and a cabinet construction about the gallery images ("painted inset cabinetry to flat-panel
  oak" -> "painted cabinets to flat-panel wood").
- Also fixed from its list and from the owner's reviewer: `/services` intro and three summaries no longer describe
  how the site is organized ("Each service has its own page...", "The page covers..."); `/process` head is
  top-aligned; the "404" label above the 404 H1 is gone; `/service-areas` Silver Spring and Howard County rows no
  longer repeat the group name as a link (the paragraph link stays); `/about` list lead-ins are concrete;
  breadcrumb and table links have a taller tap area; `#main` takes focus from the skip link.
- Passed in that gate: keyboard navigation and focus rings, contrast AA on all visible text, image dimensions and
  alt, reduced motion, CTA targets, 65 internal hrefs (all 200), tables stacking on phones.
- Left as they are (not blocking): the three "If ..." sentences in area-page room paragraphs (conditionals are the
  owner's rule for house situations); counted table headings on the three service pages; three same-size rows on
  `/services`; photographs repeat across pages (17 usable files for 24 pages); `/privacy` and `/terms` narrow column.
- After the fixes: `python3 scripts/build.py --check` OK, 24 pages, 0 problems; the six touched pages have no
  overflow at 320 / 390 / 1440 and no console errors. Chrome only; no Safari / Firefox / Lighthouse run.
- **Needs Rodrigo:** (1) image filenames still carry town / style names (`kitchen-kensington-victorian`,
  `olney-colonial-exterior`, ...); renaming needs redirects. (2) The footer links "Client feedback" to a page with
  no feedback yet. (3) `/contact` shows only the form until a phone / email is provided. (4) A lighter Barlow
  Condensed weight for the H1 would need a new font file. (5) The hero photo source is 1402px wide.

- **Published:** commit 0b88a13 pushed to main (fast-forward from 00d51d0, no force). Live check on
  https://bluehammermd.com after the Netlify deploy (curl only, no form submitted): `main.css` (34,605 bytes),
  `main.js` (8,465) and `site-config.js` (192) byte-identical to the repo; `/`, `/services`, `/kitchen-remodeling`,
  `/potomac-md`, `/process`, `/projects`, `/contact`, `/reviews`, `/thank-you` return 200 with the expected H1, one
  canonical each and no `<video>`; `/reviews` and `/thank-you` still noindex; sitemap 21 URLs; `/llms.txt` 200;
  `robots.txt` unchanged; video files still served. The live pages were not viewed in a browser after the deploy.

## 2026-11-20: design refinement (serif H1, warm surfaces, blue actions). Not committed

Owner: "I need a designer who brings trust, modern and traditional at the same time." The Barlow Condensed 800 H1
read as heavy. Shared style only: `site-src/assets/main.css`, `scripts/build.py` (`preload_fonts()`), docs. No page
source, copy, route, metadata, schema, sitemap, llms.txt, robots or form markup changed.

- **Font license checked first.** Gambetta (Indian Type Foundry, designer Paul Troppmar) is under the ITF Free
  Font License; text read on 2026-11-20 at https://www.fontshare.com/licenses/itf-ffl (shown there as "Version 2.0 -
  17 Aug 2026"). It allows free commercial use and self-hosting with `@font-face`; it forbids modifying, subsetting,
  converting or redistributing the files. `gambetta-500.woff2` in the repo is byte-identical to the Fontshare file.
  Note file added: `blue_hammer_remodeling_site/assets/fonts/FONT-LICENSES.txt`.
- **Type.** H1 on all 24 pages: Gambetta 500 upright (was Barlow Condensed 800). 68 px at 1440, 40.6 px at 390,
  line-height 1.06 / 1.08, tracking -0.018em. Home H1: 76 px at 1440, 41 px at 390, 35 px at 320 (the fixed line
  "Home remodeling." does not fit at 38 px on a 320 px screen). Switzer for everything else; Barlow Condensed only
  in the wordmark. End-aligned page heads: the last H1 baseline now sits on the bottom edge of the intro column.
- **Color.** `--white` page -> `--paper #FDFCFA`; `--soft #F4F6F8 -> #F6F3EE`; `--line #DFE5EB -> #E7E2D9`;
  `--line-strong #B9C4D0 -> #C8C0B3`; `--field-line #74859A -> #857C70`; `--muted #51606F -> #55606B`;
  `--focus-on-dark #FFAB70 -> #9AC6FF`; new `--action #0B57C0`, `--action-hover #0A4596`, `--on-navy-hover #DCE8F7`;
  `--orange-hover` removed. Primary buttons (hero, mobile bar, form Continue and Send): blue with white text
  (6.69:1). Header button and the button in the open mobile menu: white with navy text (16.26:1). Orange is left
  only in the two hairlines of the logo wordmark.
- **Preload.** `gambetta-500`, `switzer-400`, `barlow-condensed-800` (was Barlow + Switzer). Barlow stays because
  the wordmark is live text in the header.
- **Checks.** `python3 scripts/build.py --check`: OK, 24 pages, 0 problems. Chromium, 24 pages at 390 and 1440 plus
  the home page at 320: no horizontal overflow, every H1 inside its container and the gutter, H1 family Gambetta
  with the face loaded, no failed requests or console errors. Menus, the mobile menu and form steps 1 -> 2 -> Back
  work; no POST was sent. Published `main.css`: 35,163 bytes. No photograph or crop was changed.
- **Not done / next.** Not committed or pushed. Chrome only (no Safari or Firefox). Three fonts are preloaded
  (about 76 KB); if that weighs on the first paint, the wordmark could become part of the logo image.
  `gambetta-400`, `gambetta-400-italic` and `gambetta-600` are still in `assets/fonts/` but not loaded.
- **Needs Rodrigo:** nothing new. Still open from before: phone, email and license number (hidden while empty).

- **Published:** commit 7546ce7 pushed to main (fast-forward from f1284e0, no force). Live on https://bluehammermd.com
  after the Netlify deploy: `main.css` (35,163 bytes) byte-identical to the repo; `gambetta-500.woff2` served 200
  `font/woff2`, immutable cache, SHA-256 matches FONT-LICENSES.txt; preloads gambetta-500 / switzer-400 /
  barlow-condensed-800. In Chrome on the live site, `/`, `/kitchen-remodeling` and `/contact` render the H1 in Gambetta
  500 with the face loaded, page background rgb(253,252,250) and blue primary buttons. No form submitted.

## 2026-11-20: home page, real photographs, Remotion hero carousel, Re-Bath-style composition. Not committed

Owner requests (same day, in order): replace the home photographs with real, freely licensed stock photos and add
a Remotion hero carousel; then "rebath.com style: fonts, motion, everything except our colors and brand"; then his
own notes (photo column + consultation panel with the existing form, light serif H1, blue pill CTA, three equal
service cards, centered serif H2s, discreet numbered steps, fade-up on entry). Home page only.

- **Photos.** Six free Unsplash photos (Unsplash License; not Unsplash+, not public domain), owner-approved:
  Zac Gudakov LC-6Dnwo6_g (hero slide 1, poster, og:image), Taylor Beach PR7h5QGXd8A (slide 2), Francesca Tosolini
  XyGvEj587Mc (slide 3), Clay Elliot 1by_GbwEMwc (kitchen card), Zac Gudakov FPim6ZLM6fc (bath card), Ronnie George
  S0-e9aITeHc (interiors card). Small edits: a candle label and a refrigerator badge made unreadable, a refrigerator
  logo and photo magnets cropped off, framed family pictures on a mantel blurred. All new filenames (`home-*`); no
  existing image file changed. WebP 720/1440 (+1920 for hero slides), no EXIF/GPS. Full manifest, licenses,
  cameras and rejected candidates: `docs/image-sources.md`. Credit line on the page: "Photographs: ..." (names only;
  the build's FORBIDDEN list rejects the word "Unsplash" in page text).
- **Remotion.** Free License condition relied on: individual or for-profit with up to 3 employees (read on
  remotion.dev/pricing and in node_modules/remotion/LICENSE.md v4.0.545). New composition `HomeHeroCarousel`
  (1280x800) / `HomeHeroCarouselMobile` (720x944) in `tools/remotion/src/HomeHeroCarousel.tsx`: 3 photos, 5.5 s
  each, 0.6 s crossfade, scale 1.000 to 1.025, no text, no audio, seamless 16.5 s loop. `./render.sh home-hero`
  renders a Remotion master into out/ (gitignored) and encodes H.264 CRF 29 (+faststart) and VP9 CRF 41 with a
  keyframe at each slide start. Files: `assets/video/home-hero-1280.mp4` 1,401,967 B, `.webm` 1,153,813 B;
  `home-hero-720.mp4` 980,907 B, `.webm` 802,443 B. No React or player ships to the site.
- **Carousel behaviour** (`site-src/assets/main.js` initHeroCarousel). Poster `<img>` = slide 1, fetchpriority high,
  same box as the video (no layout shift). Video sources are attached only after load + idle and when the hero is
  near the viewport; never with prefers-reduced-motion or Save-Data. Prev / Next / Pause-Play (44 px, white focus
  ring), "1 / 3" counter, caption per slide, polite live region on manual changes only. Prev/Next seek the video to
  `index * 5.5 + 0.05 s` (a clean frame); if `video.seekable` does not cover the target or the seek does not land
  (a server without HTTP Range, such as scripts/preview.py), the carousel switches to still mode (video paused and
  hidden, WebP still for that slide loaded on demand) until Play. Pauses on hover, keyboard focus on the controls,
  tab hidden, off-screen; stays paused after Pause. No JS: poster + caption, controls hidden.
- **Re-Bath analysis** (rebath.com read in Chrome at 1440 and 390 on 2026-11-20, cookie dialog hidden with CSS,
  nothing accepted or submitted). Adopted: full-height photo hero with a dark scrim, centered white light serif H1
  (theirs: Freight Display Pro 300, 81 px / 1.0; ours: Gambetta 400, 81 px / 1.0 at 1440, 42 px at 320, 51 px at
  390, three lines on phones), white lead and pill CTA; a consultation panel beside the photo (about 28%) holding the
  existing 2-step form (stacked under the hero at 1060 px and below); a light band of four short items (only facts
  already on the site); centered serif H2s (54 px at 1440); three equal cards, photo on top, light strip with a bold
  sans title; numbered steps on one line; pill buttons in the home's main content; fade-up on entry (18 px, 0.6 s,
  transform/opacity only). Not adopted: their typefaces (Freight Display is commercial; Open Sans and Montserrat
  would add files, so Switzer keeps the text role), their colors, photos, copy, reviews, logos of review sites,
  stats, offers, phone number, "Free" wording, button "shine" animation, image parallax, and animation of the H1 or
  CTA (kept static for LCP and the earlier owner rule).
- **Form.** The home page meta is now `"consult": false` and the form is placed with `{{FORM:consult-form-consultation}}`
  inside `#consultation` in the hero panel: one form on the page, same id and field names as before. The hero CTA
  targets `#consultation`; the header, menu, footer and mobile-bar CTAs target `#consult-form-consultation` (the
  build's rule for pages without the shared section). Both land on the panel. The bottom consultation section is no
  longer on the home page.
- **Other.** og:image / twitter:image: new `assets/home-og-kitchen-gudakov-1200x630.jpg` (106,280 B); schema
  primaryImageOfPage: `home-hero-kitchen-gudakov-1440.webp`. Gambetta 400 declared in main.css (used on the home
  page only; FONT-LICENSES.txt updated). Title, meta description, canonical, H1 words, FAQ and schema rules are
  unchanged. The "Where we work" house photo is unchanged (same files, markup, CSS, caption); SHA-256 identical:
  1440 `4ed5ee56...f1c629`, 720 `b486578f...f52e3`.
- **Checks.** `python3 scripts/build.py --check`: OK, 24 pages, 0 problems. The other 23 generated pages differ
  only in `?v=` hashes; CSS changes are home-only selectors (plus the unused-elsewhere Gambetta 400 face). Chrome:
  no horizontal overflow at 320 / 390 / 1440; CLS 0 / 0.0007 / 0.0035; 0 console errors, 0 failed requests,
  0 POST; all 7 images load; seek path and still fallback both tested; reduced motion and Save-Data load no video;
  form step 1 -> 2 -> Back in the panel works. First load of / at 1440 (to the load event, local server): before
  732,284 B, after 470,467 B; after 6 s including the idle video: before 805,119 B, after 1,697,115 B (WebM
  1,153,813 B). Screenshots in the session scratchpad (home-photos/).
- **Not done / next.** Not committed or pushed. Chrome only. `preload_fonts()` in build.py still preloads
  gambetta-500 on the home page, which now uses 400 (one wasted 20 KB preload and a font swap on the H1); a
  slug-aware preload is a small build.py change, not made here. The Remotion master renders are in
  tools/remotion/out (gitignored).
- **Needs Rodrigo:** nothing new. If the company grows past 3 employees, Remotion needs a Company License before
  any new render. Still open: phone, email, license number (hidden while empty).
- Follow-up before commit: the homepage now preloads `gambetta-400` (the weight its H1/H2 use) instead of `gambetta-500`; interior pages keep 500. Build check OK, 24 pages, 0 problems.

- **Published:** commit 21c9a17 pushed to main (fast-forward from bb930a9, no force). Live on https://bluehammermd.com:
  `main.css`, `main.js`, the six new photos, the og image, the four hero videos, `gambetta-400.woff2` and the house
  photo are byte-identical to the repo; Netlify answers Range requests (206); og:image is
  `home-og-kitchen-gudakov-1200x630.jpg`; the home preloads gambetta-400, switzer-400, barlow-condensed-800. Chrome on
  the live home: the WebM autoplays (readyState 4, seekable 0-16.5 s), Pause stops it, Next seeks to 11.05 s (3 / 3)
  and wraps to 0.05 s (1 / 3); H1 Gambetta 400 "Home remodeling. In Maryland."; 0 console errors, 0 POST.

## 2026-11-21 — Homepage trust band (honest version of the Re-Bath "confidence" section)
- Added `section.home-trust` to `site-src/pages/index.html` between `.home-facts` and `.home-services`; CSS block in `site-src/assets/main.css` (home-only classes). Hero, carousel, photos, house photo, SEO metadata untouched.
- Content: small original house/speech line mark (royal blue), H2 Gambetta 400 "Confidence starts with a clear plan", one factual paragraph drawn from /about and /process, four line icons (muted) labelled Written scope / Choices explained / Clear communication / Final walk-through, blue pill CTA "Explore our process" -> /process. No cards or boxes. Mobile: 2x2 icons, CTA full width (max 360px).
- Deliberately NOT included: star ratings, review counts, job counts, Google/Facebook/HomeAdvisor/Houzz logos, review placeholders, AggregateRating/Review schema. `site-config.reviewProfileUrl` is empty, /reviews has no reviews, and no verifiable public profile for this Maryland business was found (a same-name Florida business exists and must not be used). Ratings or platform logos require real, verified profiles first; revisit then.
- Checks: `build.py --check` OK 24/0. Chrome at 320/390/1440: no horizontal overflow, H2 Gambetta 400 (36px mobile, 50px desktop), icons 2 rows on mobile / 1 row desktop, CTA 50px tall, link opens /process, 0 console errors, 0 POST. Fixed "walk-through" breaking at the hyphen at 320px.
- Owner review (1280, internal browser): composition approved; H2 max-width changed from 20ch to min(1000px,100%) so it sits on one wide line on desktop (50px kept, no nowrap; mobile wraps naturally). Rechecked: check OK 24/0, 320/390/1440 no overflow, one line at 1440, CTA -> /process, 0 errors, 0 POST.

## 2026-11-21 — Trust band: icon row replaced by illustrative platform logos (owner decision)
- Owner instruction (explicit, supersedes the earlier "no logos without verified profiles" note for this section): show Google, Facebook, HomeAdvisor and Houzz logos as illustration only, images WITHOUT links, no profiles, no reviews.
- Replaced the four icons/labels in `section.home-trust` with four `<img>` (alt = platform name, width/height set, lazy), no `<a>`/href. Added neutral caption "Platforms homeowners use to research remodeling companies." Title, paragraph and "Explore our process" CTA unchanged. No stars, ratings, counts, seals, endorsements or Review/AggregateRating schema.
- Assets hosted locally, unmodified gray (#6d6e71) SVGs, checked for scripts/external refs (none):
  - assets/platform-logo-google.svg <- https://www.rebath.com/uploads/2024/03/logo-google.svg
  - assets/platform-logo-facebook.svg <- https://www.rebath.com/uploads/2024/03/logo-facebook.svg
  - assets/platform-logo-homeadvisor.svg <- https://www.rebath.com/uploads/2024/03/logo-homeadvisor.svg
  - assets/platform-logo-houzz.svg <- https://www.rebath.com/uploads/2024/03/logo-houzz.svg
  (downloaded 2026-11-21; trademarks belong to their owners; no Re-Bath branding or text reused.)
- Sizing: desktop 4-up (Google 190x63, Facebook 64x64, HomeAdvisor 245x38, Houzz 205x47, max-width 100%); mobile 2x2 capped at 44px height (Facebook 52px). No cards or boxes.
- Checks: build --check OK 24/0; Chrome 320/390/1440 no horizontal overflow, CTA -> /process, 0 console errors, 0 POST.
- Open risk for the owner: platform brand guidelines generally restrict logo use that could suggest a presence or endorsement; replace with real profile links (or remove) once profiles exist.

## 2026-11-21 — Site-wide harmonization with the Re-Bath reference + local section (owner direction)
- Tokens and chrome (shared, so interior pages follow without content/SEO changes): white header, navy wordmark, blue-grey headings/nav #465B6B, grey body text, #F7F7F7 bands, light grey lines, icon blue #8AB8C8, wine pill buttons and links #A51F3D (hover #871831), dark slate footer #2E3B46 with white wordmark. Details in docs/design-system/design-brief.md (2026-11-21 section).
- Fonts: Gambetta 400 for every H1/H2; Open Sans (text) and Montserrat (nav, buttons, labels, H3, hero panel title) self-hosted from the official Google Fonts distribution, OFL, recorded in assets/fonts/FONT-LICENSES.txt. Preloads: gambetta-400, open-sans-var-latin, montserrat-var-latin, barlow-condensed-800. Switzer no longer referenced (files kept).
- Home: hero compacted (1440: 634px tall; the form panel sets that height), slate scrim, H1 70px desktop / 40-43px mobile, H2 50px / 32px, section rhythm 52-84px. Trust band: the house/dialogue mark replaced by five decorative grey stars (aria-hidden; no rating, count or Review schema); logos still unlinked images.
- New section "Remodeling near you" between the trust band and services: Maryland outline map (us-atlas / Census, see docs/image-sources.md) at 40% opacity, area select limited to the eight existing town pages, "View area" navigates to the page (no-JS fallback GET /service-areas), wine "Explore service areas" -> /service-areas, outline "Schedule a Consultation" -> #consultation.
- Owner preview review applied: map opacity 0.4, header focus wine (the old light ring was winning), hero panel title Montserrat 600 21px.
- QA (Chrome, preview 8770): build --check OK 24/0; 320/390/1440 no horizontal overflow; fonts loaded (Gambetta 400, Open Sans, Montserrat, Barlow); header white with navy wordmark; mobile menu white, dropdown works; focus rings visible (Tab through header: wine 3px); area select Rockville -> /rockville-md; form step 1 -> 2 with 0 POST; carousel playing, Pause + Next -> 3/3; logos 0 links; 5 stars aria-hidden; 0 console errors. Fixed during QA: the mobile hero caption overlapped the CTA at 320px. House photo SHA unchanged (4ed5ee56 / b486578f).
- Not run: Safari, Firefox, Lighthouse.

## 2026-11-22 — Hammer orange instead of wine + mobile pass (owner direction)
- Owner: "coloque a cor que esta no martelo ... nesse que esta vermelho" and "crie a versao otimizada para celular". Then: keep mobile simple — poster + MANUAL WebP carousel with the existing showStill/go fallback, no autoplay, no video, Pause hidden; desktop Remotion unchanged.
- Color (tokens, site-wide): buttons `--action #FF7A24` (hammer orange) with navy text `--on-action #142131` (6.24:1); hover #F06A10 (5.2:1), active #E35F0A (4.6:1). Text links, focus rings, form progress and checkbox accent on light surfaces: `--royal #A64000` (6.26:1 on white, 5.8:1 on #F7F7F7). Footer focus ring and the old pink tints moved to light orange (#FFC59E / #FFEADB). Every rule that put white text on the button fill now uses --on-action; the hero :active rule that would have put navy on navy now uses the active orange. Hammer blue, grey stars, slate headings/body unchanged.
- Hero carousel (main.js, +5/-2 lines): the Remotion video runs only at >=768px (motion allowed, no Save-Data). Below 768px the carousel is manual: poster image, prev/next load only the chosen WebP still (showStill), no Pause button, no video request.
- Performance (no new dependencies): header/footer hammer mark now a 160px WebP made from the owner PNG (73 KB -> 3 KB); favicon a 64px PNG (2.6 KB); Barlow wordmark font subset to ASCII (39 KB -> 12 KB, see FONT-LICENSES). The original PNG and full Barlow file stay in place.
- Layout: 701-900px service cards are horizontal (photo left, same 4:3 crop) instead of three ~640px stacked cards; on phones "View area" sits on the select's row.
- Mobile bytes (Chrome, preview, after 9 s idle) 390@3x: 1,263,625 -> 364,447 B (video 802,443 -> 0; logo PNG 145,670 -> WebP; fonts 138,012 -> 110,856). 360@2x: 1,212,827 -> 313,649 B.
- QA (Chrome, preview 8770) 320/390/430/768/1440: no horizontal overflow; 0 elements with wine; all orange fills carry navy text >= 4.5:1; video requested only at 768/1440; next on phone swaps the still (720 at 320@2x, 1440 at 390@2x) and counter 2/3; menu dropdown opens on tap, Escape closes dropdown then menu; form step 1 -> 2 with 0 POST; area select -> /bethesda-md; text inputs 16px; 0 console errors.
- Lighthouse mobile (12.6.0, live domain BEFORE this change): Performance 79, Accessibility 99, LCP 2.8 s, FCP 1.1 s, TBT 660 ms (one 705 ms unattributed long task while the mobile video loaded), CLS 0, 1,392 KiB.
- Published e619fda. Live domain: main.css/main.js, logo WebP, favicon, Barlow subset and hero stills MATCH the repo. Live QA 320/390/430/768/1440 same results as preview (no video request below 768; at 768/1440 the video seeks to 2/3 on Next).
- Lighthouse mobile (12.6.0, live domain AFTER): Performance 100, Accessibility 99, LCP 1.9 s, FCP 0.9 s, TBT 0 ms, CLS 0, Speed Index 0.9 s, 444 KiB (was 79 / 2.8 s / 660 ms / 1,392 KiB). One run each, simulated throttling; not run: Safari, Firefox, real devices.

## 2026-11-22 — Regional expansion: 25 new area pages, regional hub (owner direction)
- Owner request (Rodrigo): "adicione todas as cidades referencia da regiao no website adicione as regioes que mais tem procura por remodelation." Implementation selection based on the owner request and the Semrush research (assisted run, not a city list dictated by Rodrigo): 25 new pages + 8 existing = 33 area pages; 49 pages total, 46 indexable. One general page per city (kitchen / bath / basement + jurisdiction + FAQ), no service x city pages. This broad request applies to this task and is recorded here; HARD-RULES.md and other instruction files were not changed. Note for future runs: HARD-RULES still lists the Tier 1 places and says not to create pages for lower-income areas, and AUDIT item 0.4 had flagged Gaithersburg/Germantown; this task follows the owner's later request. scripts/build.py FORBIDDEN no longer lists Gaithersburg and Germantown for the same reason.
- New pages: Montgomery: gaithersburg-md, germantown-md, north-bethesda-md, north-potomac-md, darnestown-md, clarksburg-md. Howard: columbia-md, ellicott-city-md, clarksville-md, fulton-md (howard-county-md stays the county hub and links them). Nearby Maryland: frederick-md, laurel-md, owings-mills-md. DC: washington-dc. Northern Virginia: mclean-va, great-falls-va, vienna-va, arlington-va, falls-church-va, alexandria-va, fairfax-va, reston-va, herndon-va, ashburn-va, leesburg-va.
- Demand data: owner's Semrush Keyword Overview (UI, US database, 120 unique terms, 2026-11-22; API error 132 that day) saved in docs/seo-regions-research-2026-11-22.md with the keyword -> URL map. No volumes, counts, ranks or "high demand" wording in site copy; North Bethesda, North Potomac, Fulton and Clarksburg are coverage pages.
- Radius: Census Gazetteer 2024 internal points, straight line from Olney (docs/regions-distances-2026-11-22.csv): all 33 places within about 27 miles (Frederick 27.2, Leesburg ~26.5 approx., Owings Mills 23.8, Fairfax city 23.5, Ashburn ~23.3 approx., Alexandria 22.5). Farther addresses are confirmed one by one; no page promises a whole county or state.
- Jurisdiction blocks: official sources only, docs/regions-official-sources-2026-11-22.md (accessed 2026-11-22; items marked Excerpt should be rechecked in a browser over time). Key distinctions used: City of Gaithersburg / Rockville own permits; Germantown and Clarksburg County historic districts (HAWP); Howard DILP, Columbia village covenants, Ellicott City HPC; DC DOB + HPO; Fairfax County LDS (McLean, Great Falls, Reston, Vienna with Town zoning review); Town of Herndon own permits; City of Fairfax, Falls Church, Alexandria independent cities (Alexandria BAR for qualifying exterior work); Loudoun County (Ashburn; Leesburg Town zoning first + H-1 district); City of Frederick vs County; Laurel City vs Prince George's / Howard / Anne Arundel; Baltimore County PAI. No contractor license is claimed for DC or Virginia; DC/VA pages say eligibility and jurisdiction requirements are confirmed before any agreement.
- Photos: only the six licensed real photographs from the home page (Unsplash License, attribution not required; docs/image-sources.md), neutral captions, never attributed to a city or a project.
- Hub /service-areas: H1 "Where we remodel.", region jump links, all 33 pages grouped (13/5/3/1/11) with the smaller Tier 1 places named in their group, short "address decides the permit office" block, new FAQ; the house photo is unchanged. Title changed from the Montgomery County keyword (volume 20) to "Remodeling Service Areas: MD, DC and Northern VA | Blue Hammer"; Montgomery County is the first H2 group.
- Home: area select has optgroups with all 33 pages; local paragraph and "Where we work" now summarize the five regions with a button to the hub. Header dropdown and footer link regions only (7 links), not 27 names. FAQ, contact and services area sentences harmonized. areaServed adds the new places; llms.txt lists all area pages by region.
- Independent QA corrections applied: removed "short drive" / drive-time and frequency wording ("often", "frequent request", "most addresses"), egress wording made conditional ("code-compliant emergency escape and rescue access ... confirmed during design and permit review"), Columbia covenants made conditional with the official CA village list link, Alexandria BAR qualified to qualifying exterior work.
- Route QA (preview, Chrome): build --check OK 49/0; sitemap 46 URLs; 190 internal links + anchors OK; 0 duplicate titles/descriptions; one H1 and correct canonical on every page; 0 overflow at 390 and 1440 on home, hub and all 25 new pages; home select 13/5/3/1/11 options, /leesburg-va navigation; 0 console errors; 0 POST.
- bh-design-check (five independent reviewers, read-only, preview 8770) + bh-qa gate:
  - 1 hierarchy/brand: PASS (nit applied: hub region chips centered on mobile).
  - 2 accessibility/contrast: PASS (one H1, no skipped levels; 44px jump/town links; focus #A64000; buttons 6.24:1, links 6.26:1 / 5.84:1 on #F7F7F7).
  - 3 mobile 390/768/1024/1440: PASS (no horizontal scroll on 11 pages x 4 widths, H1 + CTA in the first screen, anchors land below the sticky header).
  - 4 performance: PASS (one fetchpriority hero per page, other images lazy with width/height, CLS 0, no new libraries, CSS +0.6 KB; new pages 393-590 KB at 390, same range as existing area pages).
  - 5 conversion/copy: FAIL on six frequency phrases and one unsourced county in the Laurel intro; all fixed (North Bethesda x2, Darnestown, Clarksburg, Clarksville, North Potomac, Laurel).
  - bh-qa: PASS (build --check OK 49/0 without changing files; image/AI-label rules; no invented facts; links and titles).
  - 5 conversion/copy re-run after the fixes: PASS (7 fixes confirmed; scan of the 25 new pages + hub finds no frequency, drive-time, client/project, DC/VA license or absolute code claims).
