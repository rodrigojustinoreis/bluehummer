# Anti-slop copy rules

Run on every copy change, then run the checker:

```bash
python3 ~/.claude/skills/slopmonster/tools/deslop.py blue_hammer_remodeling_site/<page>.html
```

Aim for 5/5. Lists of real place names (for example "Glenelg, Glenwood and West Friendship")
are allowed exceptions; note them. The optional rival-model `cleanse.sh` step is not required.

## Banned
- "not just X but Y", "more than just", "whether you're X or Y", self-answered questions.
- leverage, unparalleled, unmatched, seamless, elevate, world-class, top-notch, second to none,
  cutting-edge, state-of-the-art, bespoke, curated, nestled, journey, dream kitchen, transform
  your space, peace of mind, built to last, trusted and reliable, we pride ourselves, one-stop shop.
- Triple adjective or triple abstract-noun lists ("quality, integrity and excellence").
- Em-dash chains, semicolon-heavy paragraphs.

## Do
- Replace each abstract claim with what actually happens: "Drawings, selections and a written scope before we price" instead of "trusted, reliable craftsmanship".
- Active voice, plain verbs, sentence case. CTAs say exactly what happens: "Schedule a consultation".
- One idea per sentence. Cut any sentence that would fit on any contractor's site.

## Never invent
Facts, numbers, years in business, project counts, licenses, insurance, awards, reviews, ratings,
prices, guarantees or financing. If a sentence needs one of those and it is not in
`site-src/assets/site-config.js` (the file to edit; `python3 scripts/build.py` generates the published copy) or from Rodrigo, rewrite the sentence or list the gap in AGENT-LOG.md.
