# Method: 10 steps, with the tool for each

Run the steps in order for a new or reworked page. For a small fix, run only the steps it touches,
but always run 7, 9 and 10.

| # | Step | Do | Tools |
|---|---|---|---|
| 1 | Understand | Write one sentence: who the page is for (homeowner, area, room), what they need to decide, and the one action we want. Check where the page sits in the nav and sitemap. | `product-marketing` (reads `.agents/product-marketing.md`), `site-architecture` |
| 2 | Gather evidence | List the facts the page will use and where each one is confirmed. Anything not confirmed stays out or goes to "Needs Rodrigo". | [evidence.md](evidence.md), `site-config.js`, `AGENT-LOG.md` |
| 3 | Structure | Outline sections top to bottom: promise, scope, process, proof (only real), cost/planning guidance (labeled as planning ranges), FAQ, CTA "Schedule a Consultation". One primary action per page. | `site-architecture`, `cro`, `docs/design-system/dont-make-me-think.md` |
| 4 | Write | American English, concrete and specific, brand Voice in `docs/brand.md`. Then the anti-slop pass. | `copywriting`, `cro`, `bh-anti-slop-copy` (slopmonster) |
| 5 | Build | Edit `site-src/pages/*.html`, shared chrome in `scripts/build.py`, styles in `assets/main.css`. Keep palette A, Gambetta/Switzer, existing components. No redesign unless the stage asks for it. | `anthropic-frontend-design`, `impeccable` (critique/polish/typeset/layout/harden only), `better-interface` family, `bh-design-loop`, `bh-section-references` |
| 6 | Docs | Before using an API, CSS feature, Playwright command or library option, check current docs for the version in use. | Context7 MCP (`resolve-library-id`, then `query-docs`) |
| 7 | Review | Accessibility (WCAG 2.2 AA: contrast, focus, labels, keyboard), responsive at 390, 768, 1280, 1440 px, image size/alt/width/height/lazy, performance (no new heavy JS). | `web-interface-guidelines` (local copy, preferred), `better-accessibility`, `impeccable` audit, Chrome DevTools MCP (`lighthouse_audit`, `performance_start_trace`, network, console) |
| 8 | SEO | Title <= 60, meta <= 155, one H1, canonical, OG, internal links, sitemap entry, JSON-LD (HomeAndConstructionBusiness, Service, FAQPage, BreadcrumbList) with only real data. | `marketing-seo-audit`, `schema`, existing `seo-*` personal skills |
| 9 | Browser | Serve locally and look at it: `cd blue_hammer_remodeling_site && python3 -m http.server 8765 --bind 127.0.0.1`, then `tools/node_modules/.bin/playwright-cli -s=bh open http://127.0.0.1:8765/<page>.html`, `screenshot`, `resize 390 844`, `screenshot`, `console`. Close the session and stop the server after. Never submit the real consultation form. | `playwright-cli` skill, `webapp-testing`, Chrome DevTools MCP |
| 10 | Record | `python3 scripts/build.py --check` passes. Add a dated entry to `AGENT-LOG.md`: what changed, checks run, and real open items under "Needs Rodrigo". | `bh-design-check`, `bh-qa` |

## Done means
- Build check passes, `bh-design-check` passes, `bh-qa` reports PASS.
- Screenshots at mobile and desktop were looked at, not just taken.
- No unconfirmed fact, no AI label on images, no illustrative image presented as a real project.
- Log updated. Publishing is a separate, orchestrator-only step.
