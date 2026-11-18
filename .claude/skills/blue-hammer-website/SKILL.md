---
name: blue-hammer-website
description: Method for building, maintaining and reviewing the Blue Hammer Remodeling website (bluehammermd.com) and similar residential construction and remodeling sites. Use for any page, section, copy, SEO, image or design task on this repo, before editing site-src/ or the CSS, and when planning, reviewing or verifying a page. Coordinates the installed design, marketing, SEO, browser and docs tools with the bh-* agents.
---

# Blue Hammer website

Company: Blue Hammer Remodeling, based in Olney, MD 20832; serves Maryland, Washington, DC and
Virginia within about 40 miles (DC/VA licensing unconfirmed: never claim it).
Services: small repairs (entry service; specific repairs and minimum job unconfirmed), Kitchen
Remodeling, Bathroom Remodeling, Basements & Interiors.
Primary CTA: **Schedule a Consultation**. Public language: natural American English.
Goal: explain the services clearly, earn trust with real evidence, and generate qualified consultations.

This skill is the working method. It does not replace the agent system:
`bh-orchestrator` plans and gates, `bh-designer`, `bh-seo-content`, `bh-images` do the work,
`bh-qa` reviews. `.claude/agents/HARD-RULES.md` overrides everything here.

## Read first (single source of truth; do not copy their data here)
- `.claude/agents/HARD-RULES.md` - service area, honesty, images, git rules.
- `docs/brand.md` + `DESIGN.md` - visual identity (palette A, Gambetta/Switzer, logo).
- `docs/design-system/README.md` and its files - design loop, anti-slop copy, glance test.
- `.agents/product-marketing.md` - audience, positioning, CTA, confirmed facts.
- `blue_hammer_remodeling_site/assets/site-config.js` - the only source for phone, email, MHIC, review URL.
- `AUDIT-2026-11-18.md`, `AGENT-LOG.md` - backlog and history.

## The 10-step method
Full checklist with the tool for each step: [references/method.md](references/method.md).
1. Understand the page goal, the service and the audience.
2. Gather real company information and evidence (never invent; see [references/evidence.md](references/evidence.md)).
3. Define the page structure and the single primary action.
4. Write the content with the marketing skills.
5. Build the interface within the visual system.
6. Check technical documentation (Context7) when a library or API is involved.
7. Review accessibility, responsiveness, images and performance.
8. Check SEO settings and structured data.
9. Verify the experience in a real browser.
10. Record the result and the real open items.

## Remodeling page criteria
Every service, location or project page must pass [references/remodeling-criteria.md](references/remodeling-criteria.md):
scope, process, communication and next step explained; projects shown as starting point, goal,
execution, documented result (real projects only); only confirmed reviews, credentials, licenses,
insurance and warranties; image provenance tracked (real vs illustrative); local content only
when backed by specifics; keyword work based on real data; no promises of Google rankings or
AI-assistant recommendations.

## Local edits vs publishing
- Edit `site-src/pages/*.html`, `scripts/build.py`, and CSS/JS/assets in `blue_hammer_remodeling_site/assets/`.
  Never hand-edit generated HTML. Run `python3 scripts/build.py --check`.
- Local changes are not live. Publishing = commit + push to `main` (Netlify deploys). Only the
  orchestrator publishes, after `bh-qa` passes, and only in runs that allow publishing.
