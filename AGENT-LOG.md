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
