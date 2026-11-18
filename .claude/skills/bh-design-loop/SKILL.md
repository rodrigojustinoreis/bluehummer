---
name: bh-design-loop
description: Blue Hammer design loop. Use before shipping any new or redesigned page or section of bluehammermd.com. Plans against the brand file, builds, then has a critic subagent compare the result with premium reference sites and iterate until it meets the brief.
---

# Blue Hammer design loop

1. Read `docs/brand.md`, `docs/design-system/design-brief.md` and `docs/design-system/dont-make-me-think.md`.
2. Load the `anthropic-frontend-design` skill and follow its plan → review-the-plan → build process.
   Write the short plan (palette from brand.md, type roles, ASCII wireframe, the one memorable element) in your notes first.
   Also load `better-interface` (and its domain skills `better-typography`, `better-layout`,
   `better-accessibility`, `better-writing`, `better-colors`, `better-ui`) and the vendored
   `web-interface-guidelines` skill. Read its local `command.md`; do not fetch the guidelines
   and do not run install scripts. Use these for the AUDIT item 15 page-by-page overhaul.
3. For each section type, look at references from `docs/design-system/section-references.md`.
4. Edit `site-src/pages/*.html`, shared chrome in `scripts/build.py`, styles in `blue_hammer_remodeling_site/assets/main.css`. Run `python3 scripts/build.py --check`.
5. **Critic pass**: launch a Task subagent as an independent art director. Give it the built page
   (screenshots if you can take them, for example with `npx playwright screenshot` at 390 and 1440 px,
   otherwise the HTML/CSS), the brief and two or three gold-standard references from the brief.
   Ask it to score 1 to 10 on: premium feel, distinctiveness (does it look AI-template?), hierarchy,
   imagery, copy specificity, and to list the top five concrete fixes.
6. Apply the fixes and repeat the critic pass until every score is 8 or more, at most three rounds.
   Record the final scores in AGENT-LOG.md.
7. Run the `bh-design-check` skill before committing.
