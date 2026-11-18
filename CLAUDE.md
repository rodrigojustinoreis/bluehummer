# Blue Hammer Remodeling

Website and online presence for Blue Hammer Remodeling (Maryland remodeling company).

For any task about content, SEO, images, design, or online presence, and for every
headless or autonomous run, start the **`bh-orchestrator`** agent
(`.claude/agents/bh-orchestrator.md`). It reads the audit and `AGENT-LOG.md`,
picks the next stage, delegates to specialist subagents (`bh-designer`,
`bh-seo-content`, `bh-images`, `bh-qa`), runs the quality gate, and only then
commits and pushes to `main` (Netlify deploys). Headless entry point:
`scripts/run-orchestrator.sh`. The `bluehammer` agent is a compatibility alias
that follows the orchestrator. Never invent reviews, credentials, or contact details.
All agents follow `.claude/agents/HARD-RULES.md`.

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
