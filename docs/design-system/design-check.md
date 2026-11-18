# Five-agent design check (must pass before every commit that changes design or copy)

Run five independent reviewers (Task subagents, in parallel when possible). Each gets the changed
pages, `docs/brand.md`, `docs/design-system/design-brief.md` and its checklist below, and returns
PASS or FAIL with specific fixes. Fix every FAIL and re-run that check. Log the results in AGENT-LOG.md.

1. **Visual hierarchy and brand consistency**: one clear focal point per section; type, colors,
   radius, spacing and icons match brand.md; none of the "Do not" tells from the design brief.
2. **Accessibility and contrast**: text contrast at least 4.5:1 (large 3:1), visible focus, alt text
   descriptive and neutral, heading order, form labels, keyboard navigation, reduced motion respected.
3. **Mobile and responsive**: 390, 768, 1024, 1440 px widths. No horizontal scroll, tap targets
   at least 44 px, readable line lengths, first screen shows headline and CTA.
4. **Performance / Core Web Vitals**: hero image under ~200 KB with `fetchpriority="high"`, others
   lazy, width/height on every image, no new libraries, CSS/JS growth justified, fonts with
   `display=swap`. Use `npx unlighthouse` or PageSpeed Insights on the deployed URL when available.
5. **Conversion and CTA clarity**: glance test from `dont-make-me-think.md`, one primary CTA per
   section, consultation form reachable in one click, copy passes the anti-slop check, no invented claims.

Also always: `python3 scripts/build.py --check` must print OK.
