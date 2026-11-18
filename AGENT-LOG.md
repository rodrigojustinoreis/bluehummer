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
