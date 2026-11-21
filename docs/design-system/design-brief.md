# Design brief: bluehammermd.com

> **AUTHORITATIVE (2026-11-20 refinement): see "2026-11-20 refinement: serif H1, warm surfaces, blue actions" at
> the end of this file.** It supersedes the Barlow Condensed H1, the orange primary button, the white / cool grey
> surfaces and the "No Gambetta, no ivory" line wherever they appear below.

> **Documentation note (2026-11-19): the live identity is the owner v2 package.** Navy `#142131`, orange `#FF7A24`
> (primary buttons), royal `#0864D8`, Barlow Condensed + Switzer. Since 2026-11-20 the type and layout rules are the
> "2026-11-20 direction" section at the end of this file (sentence case, Switzer headings, Barlow only in the logo and the H1). Where this file
> says palette A, "Heritage Navy & Brass", ivory, brass, Gambetta or Gambetta italics, it describes the superseded
> identity and is kept for history only. Do not restyle pages toward it. The live rules are the owner block at the
> end of `site-src/assets/main.css` (the source; `python3 scripts/build.py` minifies it into
> `blue_hammer_remodeling_site/assets/main.css`, which is generated and never edited); summary in `DESIGN.md` > "Owner v2 identity".

**Client**: Blue Hammer Remodeling, Olney, Maryland. Small repairs up to kitchens, baths and lower
levels for affluent homeowners in Potomac, Bethesda, Chevy Chase, Kensington, Olney and western Howard
County, plus DC and Virginia within about 40 miles of Olney (2026-11-18).
**Job of the site**: get a qualified homeowner to request a consultation, and make Blue Hammer
feel like the careful, design-led choice.
**Feel**: premium, editorial, high-end Maryland remodeler. Think architecture-practice portfolio
and shelter magazine, not contractor template. Quiet confidence, large photography, generous
whitespace, precise typography.

## Do
- Distinctive type pairing (Gambetta + Switzer, see brand.md) used with a clear scale.
- Restrained palette (Heritage Navy & Brass): navy, royal blue, ivory, warm limestone, brass hairlines.
- Large, photographic imagery that carries the page; asymmetric editorial layouts.
- One memorable element per page (for example an oversized serif headline over a full-bleed kitchen photo). Everything around it stays quiet.
- Concrete copy: process, permits, timelines, written scope.

## Do not (generic AI-template tells)
- Gradient blobs, glows, glassmorphism, purple/teal gradients, decorative noise.
- Emoji icons, icons on every card, generic "sparkle" icons.
- The stock "hero + three identical cards + testimonial slider + CTA band" sequence.
- Same radius and same soft shadow on every box; content chopped into identical cards.
- All-caps tracked eyebrow above every heading, "01 / 02 / 03" markers on non-sequences, "→" on every link, "A · B · C" meta strings.
- Warm cream (#F4F1EA) background with terracotta accent; near-black with acid-green accent.
- Fake stats, fake logos ("as seen in"), fake reviews, badges, or "AI-generated" labels on images.

## Gold-standard references (for the design loop critic)
Use the public sites of well-regarded design-build and architecture firms in the region and
nationally as references for tone and layout quality (for example: Anthony Wilder Design/Build,
BOWA, Case Architects & Remodelers, Gibson Builders, Jenkins Baer, and editorial shelter sites
such as Remodelista). Study layout, rhythm and type; never copy text, images or claims.

## 2026-11-20 direction (site-wide redesign; phase 1 = homepage and shared components)

This section is the rule for every later phase. Where an older part of this file, `docs/brand.md` or `DESIGN.md`
says otherwise (all-caps Barlow headings, paired italic titles, eyebrows, brass rules, watermark words, bento,
icon tiles), this section wins.

**Owner brief.** "Remove everything that looks made by AI. I need a designer." And: "a designer who brings trust,
modern and traditional at the same time." Rule: **traditional in the identity, modern in the presentation.** The
trust of an American remodeling company; not a digital agency, not ostentatious luxury.
- Traditional side: the hammer and wordmark, navy and royal as anchors, balanced proportions, precise alignment,
  contained color, photographs of wood, stone and sober finishes, type that is comfortable to read.
- Modern side: breathing room, a clean hierarchy, simple navigation, well-framed images, a mobile page that works.
- Trust comes from clarity about services, location, scope and process, and how to get in touch. Never from seals,
  years, reviews, ratings or credentials that are not real.
- Avoid: sterile empty-gallery minimalism, heavy all caps, vintage decoration (ornaments, faux-heritage badges,
  serif nostalgia), SaaS layouts. Do not change typefaces to "look traditional". No Gambetta, no ivory/brass.
  (Last sentence superseded on 2026-11-20 by the refinement section at the end: a restrained upright serif H1 and
  a warm near-white surface are now the rule. Brass, italics and ornament stay out.)

**References studied on 2026-11-20** (layout and rhythm only; no text, image, code or claim was copied):
- https://www.casedesign.com/ : one photograph leads the page; headings are medium-weight sentence case around
  40 px; a heading on the left with its paragraph on the right; room categories as a plain row of links; one
  consultation band; a footer of a logo, one row of links and addresses. Taken: sentence-case headings at a modest
  size, the "title left, note right" section head, one consultation section per page, a short footer.
- https://www.anthonywilder.com/ : very little type, the photographs carry the page, a small photo mosaic next to
  a text column, a full-width photograph between text sections, a footer about 140 px tall. Taken: photographs of
  different sizes set in a mosaic instead of a card row, text-only sections between image sections, a calm footer.
- https://bowa.com/ : a hero photograph with the headline over it and three photo tiles with labels directly
  below. Taken as the thing to avoid: text over a darkened photograph and the three-tile row are exactly the
  "hero + three cards" sequence the owner rejected; our H1 sits on white above the photograph.
  (https://www.gibsonbuilders.com/ did not respond and was not studied.)

**Decisions**
1. **Type.** Switzer carries the hierarchy, in sentence case. H2 600, `clamp(1.75rem, 1.2rem + 1.6vw, 2.5rem)`,
   tracking -0.022em. H3 600, 1.1875rem. Body 1.0625rem / 1.62, lede 1.1875rem, small 0.875rem. **Barlow Condensed
   800 appears in two places only: the logo wordmark and the page H1** (sentence case, never all caps; the logo is
   the only uppercase Barlow). No heading has one word in another color, weight or style. Titles written as
   `<em>..</em> <strong>..</strong>` in older page sources render as one plain sentence.
2. **No eyebrows.** No label above a heading. A section heading says what the section contains ("What we remodel",
   "How a project is planned", "Where we work", "Questions before a remodel", "Schedule a consultation").
3. **Color.** White page, cool grey `#F4F6F8` for dense text bands, navy `#142131` for the header and footer, royal
   `#0864D8` for links. **Orange `#FF7A24` only on the primary button** (and the two hairlines inside the logo).
   Rules are grey (`--line`) or navy; no orange rules, dots or borders.
4. **Composition.** A 12-column grid, 1240 px wide, 32 px gap, one side margin (`--gutter`) used by the container
   and by anything that bleeds. Asymmetric but aligned: column splits are 7/5 or 5/7, never 6/6. The home hero is
   the H1 and one button on white above one wide photograph. Services are a mosaic of three photographs of
   different sizes, not a row of cards. No card with border and shadow around content; no bento; no icon tiles; no
   counters; no badges; no watermark words; no glow; numbers only on a real sequence.
5. **Images.** Large, one subject each, warm familiar materials first. Every photograph has a caption **below** it
   that says what is in the picture and names only what the picture shows (no stone or wood species, no town, no
   architecture style, nothing that reads as "our project"). No image twice on a page. Home: hero
   `bh-kitchen-v2`, kitchen `kitchen-kensington-victorian`, bathroom `bh-bathroom-v2`, basement `bh-basement-v2`,
   areas `olney-colonial-exterior`. The hero video is no longer used (files kept in `assets/video/`).
6. **Density.** Sections alternate: image-led sections take `--sec` (72 to 120 px) and text-only sections take
   `--sec-tight` (48 to 72 px) on a grey band. Home order: hero (photo), services (photos), process (dense text on
   grey), areas (text and one photo), questions (text), consultation (form on grey), footer.
7. **Header.** Navy, 76 px (68 px on phones), the logo, four items, one orange button. The topline strip is gone;
   the phone slot sits beside the button and stays hidden until a number exists.
8. **Consultation.** One per page, grey background, heading "Schedule a consultation" (the same words as the
   button), one sentence, three plain lines (hidden on phones), the two-step form without a card.
9. **Footer.** Navy, about 400 px on desktop: logo and one sentence on the left; Remodeling, Service areas and
   Company as three short wrapped rows; copyright, the written-scope sentence and the legal links on one line.
10. **Mobile bar.** White, one button. It hides while a "Schedule a Consultation" button or the form is on screen.
11. **Motion.** None on load or scroll. Only state changes (menu, FAQ, form step, the mobile bar).

**For the next phases (one page at a time).** The other 23 pages already take the shared type, color, header,
consultation and footer. Their own layouts (`.interior-hero`, `.split`, `.media-split`, `.bento`, `.section-head`,
tables) are the previous structure restyled; each is to be recomposed with the rules above, its images re-chosen
with captions, and its headings rewritten where they still read as slogans.

**Phase 2 (2026-11-20): done for the 23 interior pages.** The layouts named above (`.interior-hero`, `.split`,
`.media-split`, `.bento`, `.section-head`) no longer exist. Interior pages are built from `.page-head`, `figure.photo`,
`.photo-pair`, `.sec-head`, `.cols-5-7` / `.cols-7-5`, `.rows`, `.trio`, `.notes`, `.feature`, `.callout` (see section 5 of
`site-src/assets/main.css`). Pages of one type do not share one section order; see the AGENT-LOG phase 2 entry.

## 2026-11-20 refinement: serif H1, warm surfaces, blue actions (authoritative)

**Owner.** "I need a designer who brings trust, modern and traditional at the same time." The Barlow Condensed 800
H1 read as heavy and aggressive; the traditional half of the brief was not visible. This section changes shared
type and color only. Layouts, photographs, copy, routes and the form are as in phases 1 and 2.

1. **Type roles.** Gambetta 500, upright, for the page H1 only (68 px at 1440, 38 to 41 px on phones, line-height
   1.06 to 1.08, tracking -0.018em, balanced lines; home H1 76 px at 1440, 35 px at 320, 41 px at 390). Switzer for
   everything else, H2 and H3 included. Barlow Condensed 800 for the logo wordmark only. No italics, no small caps,
   no ornament, no second serif use (not in H2, quotes, numerals or captions).
2. **Color.** Page `#FDFCFA`, soft bands `#F6F3EE`, rules `#E7E2D9` / `#C8C0B3`, field borders `#857C70`, secondary
   text `#55606B`. Navy `#142131` and royal `#0864D8` stay the anchors. The page stays close to white; the
   photographs carry the warmth. No beige or yellow fills.
3. **Primary action.** Blue `#0B57C0`, white text, hover `#0A4596`. On the navy header and in the open mobile menu:
   white fill, navy text. Same rule for the mobile bar and the form's Continue and Send buttons. Orange `#FF7A24`
   is only the two hairlines in the logo.
4. **Supersedes** decision 1 ("Barlow Condensed 800 ... the page H1"), decision 3 ("White page, cool grey `#F4F6F8`
   ... Orange `#FF7A24` only on the primary button"), decision 7 ("one orange button") and decision 10 ("White" bar:
   now the page surface color) of the "2026-11-20 direction" above. Its other decisions stand.
5. **License.** Gambetta is an Indian Type Foundry family under the ITF Free Font License, read on 2026-11-20 at
   https://www.fontshare.com/licenses/itf-ffl (commercial use and `@font-face` self-hosting allowed; no modifying,
   subsetting or redistributing the files). Token table and details: `docs/brand.md`, first block.
