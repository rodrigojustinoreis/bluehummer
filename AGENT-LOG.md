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
