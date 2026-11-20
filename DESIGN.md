# DESIGN.md - Blue Hammer Remodeling

> **Current state (2026-11-20, redesign phase 1).** Identity v2 (navy `#142131`, royal `#0864D8`, orange `#FF7A24`
> on the primary button only, hammer logo, Barlow Condensed + Switzer). Headings are **Switzer, sentence case**;
> Barlow Condensed 800 is only the logo wordmark and the page H1 (sentence case). No eyebrows, no all-caps
> headings, no orange rules. `site-src/assets/main.css` is one layer (the v1 layer and the v2 override layer were
> merged and the unused rules deleted). Rules: `docs/design-system/design-brief.md` > "2026-11-20 direction" and
> `docs/brand.md` > "Typography (current)". Everything below this note that mentions palette A, brass, Gambetta,
> paired italic titles, uppercase display type, the topline, watermark words, icon tiles or the hero video is
> history.

## Redesign phase 1 (2026-11-20): what is live in the source
- **Shared chrome (`scripts/build.py`).** Header 76 px, navy, logo + Services / Our Process / Service Areas / About +
  one orange "Schedule a Consultation"; the topline strip was removed and the phone slot moved into the header
  (hidden while empty). Consultation section: grey, H2 "Schedule a consultation", one sentence, three plain lines,
  the unchanged two-step Netlify form. Footer: navy, three wrapped link rows (same links as before), one bottom line.
  Mobile bar: white, one button, hidden by `main.js` while a primary button or the form is on screen.
- **Home (`site-src/pages/index.html`).** H1 and one button above one wide static photograph with a caption; a
  three-photograph services mosaic; a text-only process band; areas with a town index and one photograph; four
  questions; the shared consultation. Classes are `home-*`.
- **Other 23 pages.** Same markup as before; they take the new type, color, header, consultation and footer.
  Their layouts are redesigned one page at a time in later phases.

Summary of the approved visual identity as observed on 2026-11-18 (repo `main`, CSS source
`site-src/assets/main.css`, published minified as `blue_hammer_remodeling_site/assets/main.css` by `scripts/build.py`). **`docs/brand.md` is the authoritative spec**
(tokens, scale, spacing, photography, motion, voice). This file records what is live, where it
lives, and where the live site still differs from the spec. Do not duplicate values elsewhere.

## Identity
- Position: design-led kitchen, bath and lower-level remodeling, with small repairs as the entry
  service; Olney-based, serving Maryland, DC and Virginia within about 40 miles (2026-11-18).
  Editorial, calm, specific; "high-end Maryland remodeler", not a contractor template.
- Logo: `assets/blue-hammer-logo-512.png` (full lockup), `assets/blue-hammer-mark-140.webp`
  (header/footer mark), `assets/favicon.png`, social card `assets/og-blue-hammer.jpg`.
  Usage rules: `docs/brand.md` > Logo.

## Color - palette A "Heritage Navy & Brass" (approved and live 2026-11-18)
Live `:root` tokens: ivory `#FBF8F2` (page), navy `#0B2347` (headings, dark sections),
navy2 `#071830` (topline, footer), royal `#1E4FA3` (primary buttons/links, the only bright
accent), hover `#163C80`, limestone/soft `#F3EEE3`, line `#E4DCCB`, ink `#14243D`, muted
`#525D6B`, accent-text `#7A6232`, on-dark-accent `#D9C08F`, on-dark-muted `#C9D2DE`.
Brass `#A88B5A` is used for rules and borders (topline border, ghost button border).
Full table and usage rules: `docs/brand.md` > Color tokens.

## Typography
Display **Gambetta**, text/UI **Switzer**, both from Fontshare (ITF Free Font License), **self-hosted** in
`assets/fonts/` with `@font-face` in `site-src/assets/main.css` (the Gambetta `@font-face` rules were removed
on 2026-11-20: no page uses the face; the woff2 files remain in `assets/fonts/`); two faces preloaded per page by `scripts/build.py`
`preload_fonts()`. Hero and section titles use the owner-approved pairing (Gambetta italic + Switzer 700 uppercase
word + brass rule). Scale, line length, casing and the override: `docs/brand.md` > Typography.

## Components (live, in main.css)
Topline (navy2, one sentence, phone slot), sticky solid-ivory header (logo, Services and Service areas dropdowns,
Process, Gallery, About, Contact, compact royal "Schedule a Consultation"), accessible mobile menu (`aria-expanded`,
Escape returns focus, closes on link and outside click, CTA inside), buttons (`btn--primary` royal, `--dark`,
`--outline`, `--light`, `--ghostlight`, `--link`, `--sm`), paired titles (`.title-pair`, `.section-head` with brass
rule), home hero (full-bleed photo + solid ivory plate), services bento (`.bento`, `.room`), icon tiles (`.tiles`,
one `.tile--accent` in brass), numbered process row (`.steps`), areas split (`.areas-grid`, `.area-links`), FAQ
`<details>` list, consultation (navy2 + Netlify Forms `consultation`), editorial footer on navy2 (three link columns,
NAP slots, legal nav), ivory mobile CTA bar, 404 page. Section patterns: `docs/design-system/section-references.md`.

## Presentation patterns
Asymmetric editorial layouts, large photographic imagery, generous whitespace, one primary CTA
"Schedule a Consultation". Images are illustrative unless recorded as real in
`.claude/skills/blue-hammer-website/references/evidence.md`; never labeled as AI and never
presented as Blue Hammer projects (owner rule 2026-11-18).

## Owner v2 identity (live since commit e455100, 2026-11-19)
The owner's package replaced palette A on the live site: navy `#142131` header/footer, orange `#FF7A24` primary
buttons with navy text, royal `#0864D8` links and second lines of H1s, Barlow Condensed 800 uppercase display type +
Switzer text, `bh-hammer-v2.png` mark, nav Services / Our Process / Service Areas / About, primary CTA
"Schedule a Consultation" (title case). Rules: owner block at the end of `site-src/assets/main.css`, plus the appended
"Pass 4 alignment" block (no Barlow italics; h3/FAQ questions in Switzer). `docs/brand.md` still describes palette A
and is pending the owner's approval to be rewritten. AUDIT 15 pass 4 (process, faq, projects, reviews, contact,
legal, 404, thank-you) is done: paired titles, no eyebrows.
Content pass 2026-11-19 (batches A-C and final): copy only, no restyle. Pages carry no dollar figures, durations or
travel times; price tables became scope / cost-factor tables (`.range-table--scope`, the one CSS addition). Image alt
text and gallery captions describe the room and materials only (no towns, decades or house types). `/reviews` is
`noindex,follow` and out of the sitemap while it has no reviews (`build.py --check` enforces it).

## Live site vs spec (updated 2026-11-18, AUDIT 15 first page-by-page pass: chrome + home)
Fixed in this pass:
- Corner radius now follows hierarchy (2 / 3 / 4 / 6 px tokens); the 18 px radius is gone.
- Eyebrows: no uppercase, no tracking, no rule; removed from the home page and the shared consultation section.
- Shadows: royal-tinted button shadow removed; cards have no shadow; only dropdown and mobile menu keep a soft navy shadow.
- Legacy `Inter` stack removed; fonts self-hosted (no `api.fontshare.com` request).
- Off-palette blue tints (`#eaf2fd`, `#edf4fc`, `#f5f8fb`, `#f2f6fc`, `#6bacff`, etc.) replaced with palette A tokens;
  limestone alternate sections carry a brass hairline; colored `border-left` callouts replaced.
- Home: three identical service cards replaced with a bento; trust strip and gallery band cut (15f); gradient overlay
  cards and the decorative circle in the consultation section removed; the scroll reveal no longer hides content.
Pass 3 (2026-11-18): location pages, service-areas and about use the paired H1, split + detail/topic lists,
section-head + bento (via `{{SERVICE_CARDS}}`, which now renders the bento, not three identical cards) and the
FAQ split; kicker labels and middot eyebrows removed; buttons and breadcrumbs in sentence case site-wide
(including "Schedule a consultation" and "See the design gallery").
Still open (later runs):
- `olney-colonial-exterior-1440.webp` is 223 KB (over the ~200 KB hero budget); re-encoding from the WebP visibly
  softens detail, so it needs the original source or a re-export.
- Hero photo is the best existing asset (cabinetry close-up); a dedicated craft-at-work photo would be stronger.

## Not confirmed yet
- Real project photography (none recorded yet).
- Final logo source files (vector) - only PNG/WebP exports are in the repo.
