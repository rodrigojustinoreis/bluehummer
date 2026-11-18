# Design system and workflow

Read in this order for any design, layout or copy change:

1. `docs/brand.md`: tokens, type, photo style, voice (source of truth).
2. `design-brief.md`: what "premium" means for this site and the look to avoid.
3. `anti-slop-copy.md`: copy rules and the SlopMonster check.
4. `dont-make-me-think.md`: glance test, one message and one CTA per section.
5. `section-references.md`: where to look for navbar, footer, CTA, 404 and bento references.
6. `design-check.md`: the five checks that must pass before a commit.

Project skills that run this workflow (in `.claude/skills/`): `bh-design-loop`,
`bh-design-check`, `bh-anti-slop-copy`, `bh-section-references`. Personal skills used:
`anthropic-frontend-design` (official Anthropic frontend-design skill), `slopmonster`
(github.com/ItsssssJack/SlopMonster, MIT), `web-design-guidelines`, `design-review`.
All tools are free. Do not sign up for or pay for any design tool.
