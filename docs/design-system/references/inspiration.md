# Layout inspiration: "Forma Drylining" (owner reference, 2026-11-18)

Source page: https://lumith.studio/ideas/trades/forma-drylining (a Lumith "website idea" page
for UK trades; the business name is made up).
Files beside this doc (all git-ignored, reference only):
- `forma-drylining-inspiration.jpg` - Rodrigo's Pinterest screenshot (hero + top of page).
- `forma-drylining-concept.webp` - the full-length concept mock-up shown on that page
  (desktop only, hero to footer). **Best view of the whole layout.**
- `forma-drylining-fullpage.png` - full-page Playwright capture (1440 px) of the Lumith page
  itself; mostly Lumith's own sales/pricing content around the concept, not the concept. A Pinterest screenshot of a website
concept for a UK drylining trade, by Lumith. Sent by Rodrigo as the **primary layout inspiration
for the AUDIT item 15 chrome and home overhaul**.

**Reference only.** Never copy it, trace it, crop it, or ship it (or any part of it) as a site
image. It is third-party work: do not move it into `blue_hammer_remodeling_site/`, do not
commit it (it is git-ignored), and do not reuse its copy, logo, photos or prices.

## What to take from it (adapted to Blue Hammer)
1. **Mixed-type hero headline.** One huge, heavy, tight word in the sans plus an italic serif
   line, like "SHAPE / *better spaces.*". Ours: **Switzer 700, uppercase, tight tracking
   (about -0.02em), line-height about 0.9** for the big word + **Gambetta italic** for the
   second line. Write our own words (e.g. a room word + an italic promise); no copying.
2. **Section titles with the same pairing** (their "Selected WORK.", "Clean lines. STRONG
   FOUNDATIONS."): Gambetta italic phrase + Switzer bold uppercase word, with a **thin brass
   accent rule** (1-2 px, `--brass`) near the title.
3. **Giant faded watermark word** behind a section (e.g. REMODELING, KITCHENS): Switzer 700,
   very large, `--navy` or `--line` at low opacity, `aria-hidden="true"`, decorative only, never
   hurting text contrast, clipped on mobile.
4. **Full-bleed hero photo of a craftsperson at work** with a **compact single CTA**
   ("Schedule a Consultation"). Craft hands/tools on fine materials (cabinetry, stone, millwork),
   no identifiable faces. It is illustrative: never captioned or implied to be a Blue Hammer
   employee, client or project.
5. **Category cards, 3 across:** image, small uppercase label, arrow (Kitchen Remodeling,
   Bathroom Remodeling, Basements & Interiors). Hover: subtle image zoom + arrow nudge.
6. **Service grid of line icons in bordered tiles**, with **one highlighted tile in brass**
   (`--brass` fill or border, navy text for contrast; never brass text on ivory). Lucide-style
   icons per `docs/brand.md`.
7. **Generous ivory background** (`--ivory`) and a confident editorial type scale.

## Brand adaptation (non-negotiable)
- Accent is **brass `#A88B5A`**, not their yellow. Palette A and Gambetta/Switzer stay
  (`docs/brand.md`, `DESIGN.md`). Royal stays the button color.
- **No "From $" prices** or price badges unless Rodrigo confirms prices.
- Images: no AI labels anywhere; never presented as real Blue Hammer projects, clients or
  staff; "Selected work"-style sections must not imply completed Blue Hammer projects; use
  room categories or design gallery wording until real projects exist.
- Tone: upscale Maryland homeowner, **less industrial** than the reference: warmer photos,
  more air, finer rules, no hard-hat/site-construction mood, no heavy black blocks.
- Owner override (2026-11-18): this reference allows uppercase Switzer **display words** and
  the italic-serif/bold-sans headline pairing, which `docs/brand.md` Typography otherwise
  discourages. Limit it to hero and section titles; keep small all-caps eyebrows reduced (AUDIT
  15d). Update `docs/brand.md` Typography in the same commit that ships it, per brand.md's rule.

## Full concept, top to bottom (from `forma-drylining-concept.webp`)
Inspiration for structure and rhythm only; write our own copy, use our own images.
1. **Header** over the hero photo: logo left, 4 plain text links centered, one filled CTA
   button right. Ours: mark + nav + "Schedule a Consultation" (royal), header transparent over
   the hero, ivory once scrolled.
2. **Hero**: left half ivory fading into a full-bleed photo on the right; small uppercase
   location line ("Olney, Maryland" style), giant sans word, italic serif line, one short
   sentence, one button. Giant watermark word across the bottom of the hero.
3. **"Selected WORK."** title with a short accent rule and a 2-line note on the right; 3 image
   cards with uppercase label + arrow. Ours: the three services (or design gallery
   categories), not "projects", until real projects exist.
4. **Services grid** under a watermark word (theirs: SERVICES): title pairing + short note on
   the right; 4-column grid of bordered tiles, line icon, name, arrow; first tile filled in the
   accent. Theirs shows "From GBP/m2" prices + "illustrative guide prices" note: **we do not show
   prices** (no "From $") unless Rodrigo confirms them. Ours: fewer tiles (what each service
   includes, e.g. design and drawings, permits, cabinetry, tile and stone, lighting, project
   management), one brass tile.
5. **Full-bleed "about" band**: a wide photo (theirs: branded van in motion) with a big
   watermark phrase, and on the right a title pairing + short paragraph + one button. Ours: an
   upscale Maryland home exterior/interior or craft detail photo; the paragraph uses only
   confirmed facts (Olney-based, MD/DC/VA within ~40 miles, design-led process). No branded vehicle/staff
   imagery implying real Blue Hammer people.
6. **Testimonials**: title pairing + 4 cards with stars, quote, face photo, name, area.
   **Do not build this with placeholder or invented reviews.** Keep the slot hidden until
   real, verified reviews exist (HARD-RULES.md); meanwhile use this position for the process
   ("Consultation, Design and written scope, Build, Walkthrough") in the same card rhythm.
7. **Contact block**: big pairing headline ("LET'S BUILD / *your next space.*" pattern, our own
   words), short line on the right; simple form left (name, email, project), vertical hairline,
   contact methods right with line icons. Ours: the existing Netlify `consultation` form fields;
   phone/email only when confirmed in `site-config.js`.
8. **Footer**: logo, the same 4 links, social icons right; thin rule; copyright left, short
   accent dash + tagline right. Ours: on ivory or navy2, brass dash, no social icons until real
   profiles exist.

Recurring devices: thin accent dash next to every section title; italic-serif + bold-sans title
on every section; text block on the right of each title (2 short lines); square-ish cards with
hairline borders and almost no radius; lots of ivory; one accent color used sparingly.

## Mobile (not shown in the reference; our rules)
The concept is desktop-only. On mobile: stack the hero (photo first or behind text with a
strong ivory gradient for contrast), scale the giant word with `clamp()` so it never overflows,
hide or shrink watermark words, cards 1 per row (or a horizontal scroll with visible next card),
service tiles 2 per row, title side-notes move under the title, sticky header with the CTA as a
compact button. Test at 390 px and 768 px with playwright-cli.
