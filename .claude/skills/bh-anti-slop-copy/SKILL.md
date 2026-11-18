---
name: bh-anti-slop-copy
description: Anti-slop copy pass for Blue Hammer pages. Use whenever writing or editing any site copy, headings, CTAs, meta descriptions or marketing drafts. Applies the project copy rules and the SlopMonster checker; never invents facts.
---

# Anti-slop copy pass

1. Read `docs/design-system/anti-slop-copy.md` and the Voice section of `docs/brand.md`.
2. Load the `slopmonster` skill for its editorial checklist.
3. Rewrite vague claims into concrete, verifiable statements about process, scope, permits and
   timelines. Never invent facts, numbers, licenses, reviews, prices or guarantees.
4. Build, then check every changed page:
   `python3 ~/.claude/skills/slopmonster/tools/deslop.py blue_hammer_remodeling_site/<page>.html`
   Target 5/5; real place-name lists are accepted exceptions (note them).
5. The rival-model `cleanse.sh` step is optional. Skip it if no other CLI is set up.
