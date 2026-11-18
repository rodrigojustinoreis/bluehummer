---
name: bh-design-check
description: Five-agent design check for bluehammermd.com. Use before every commit that changes layout, styles, images or copy. Runs five independent reviewers (hierarchy/brand, accessibility/contrast, mobile, performance, conversion/CTA) and blocks the commit until all pass.
---

# Five-agent design check

Follow `docs/design-system/design-check.md` exactly.

- Launch five Task subagents (in parallel when possible), one per check, each with the changed
  pages, `docs/brand.md`, the design brief and its checklist. Each returns PASS/FAIL plus fixes.
- Fix every FAIL, re-run only the failed checks, repeat until all five pass.
- Also run `python3 scripts/build.py --check` (must print OK) and the anti-slop checker on changed pages.
- Write a one-line result per check in AGENT-LOG.md. Do not commit while any check fails.
