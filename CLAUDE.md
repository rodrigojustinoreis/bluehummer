# Blue Hammer Remodeling

Website and online presence for Blue Hammer Remodeling (Maryland remodeling company).
For any task about content, SEO, images, or online presence, delegate to the
`bluehammer` subagent (`.claude/agents/bluehammer.md`). It works autonomously,
commits and pushes to `main` (Netlify deploys), and logs its work in `AGENT-LOG.md`.
Never invent reviews, credentials, or contact details.

## Design and images (owner rules, 2026-11-18)
- Every design, image or copy task reads `docs/brand.md` and `docs/design-system/README.md`
  first and uses the `anthropic-frontend-design` skill plus the project skills in
  `.claude/skills/` (`bh-design-loop`, `bh-design-check`, `bh-anti-slop-copy`,
  `bh-section-references`). Goal: premium, editorial, high-end Maryland remodeler; no
  generic AI-template look.
- Images may be AI-generated and are never labeled as AI (no tags, badges, captions, alt
  text, filenames or disclaimers saying AI/concept/inspiration). They must never be
  presented as completed Blue Hammer projects, real clients, employees or before/after work.
- No invented facts, numbers, licenses, reviews or contact details in copy. Free tools only.
