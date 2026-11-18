# Blue Hammer Remodeling: brand guideline

Every design or copy task reads this file first. If a change conflicts with it, update this
file in the same commit and say why in AGENT-LOG.md.

## Position
Design-led kitchen, bath and lower-level remodeling for established homes in Montgomery and
Howard County, Maryland. Based in Olney. The site should feel like a high-end Maryland remodeler
or small architecture practice: editorial, calm, specific. Not a contractor template.

## Logo
- Files: `assets/blue-hammer-logo-512.png` (full lockup), `assets/blue-hammer-mark-140.webp` (header/footer mark).
- Clear space: at least the height of the hammer head on every side. Minimum mark height 32 px.
- Only on ivory, white, limestone or navy backgrounds. Never stretch, recolor, outline, shadow or put it on a photo.

## Color tokens (palette A: Heritage Navy & Brass)
Approved 2026-11-18. Traditional and modern: logo navy and royal on warm ivory, with brass as a craft accent.

| Token | Hex | Use |
|---|---|---|
| `--ivory` | `#FBF8F2` | Page background |
| `--white` | `#FFFFFF` | Cards, raised surfaces |
| `--ink` / `--graphite` | `#14243D` | Body text on light backgrounds |
| `--muted` | `#525D6B` | Secondary text |
| `--navy` | `#0B2347` | Headings, footer, dark sections |
| `--navy2` | `#071830` | Topline and consultation background |
| `--royal` | `#1E4FA3` | Primary buttons and links. One bright accent; do not add another |
| `--hover` | `#163C80` | Primary button hover |
| `--limestone` / `--soft` | `#F3EEE3` | Alternate section background, pills, table headers |
| `--line` | `#E4DCCB` | Borders and hairline rules |
| `--brass` | `#A88B5A` | Hairline details, dots, focus ring, topline rule. Do not use as text on ivory (fails contrast) |
| `--accent-text` | `#7A6232` | Eyebrows and table headers on light backgrounds (brass at text contrast) |
| `--on-dark-accent` | `#D9C08F` | Eyebrows and small brand labels on navy |
| `--on-dark-muted` | `#C9D2DE` | Secondary text on navy |

Rules: no gradient washes or blobs, no glassmorphism, no colored drop shadows. Text contrast at
least 4.5:1 (3:1 for 24 px+ headings).

## Typography
- Display: **Gambetta** (Fontshare, ITF Free Font License, free for commercial web use). Weights 400, 400 italic, 500, 600.
- Text and UI: **Switzer** (Fontshare, ITF Free Font License). Weights 400 to 700.
- **Self-hosted** (2026-11-18): woff2 files in `assets/fonts/` (`gambetta-400`, `gambetta-400-italic`, `gambetta-500`,
  `gambetta-600`, `switzer-400` to `switzer-700`), declared with `@font-face` + `font-display: swap` at the top of
  `assets/main.css`. No request to `api.fontshare.com`. `scripts/build.py` `preload_fonts()` preloads only the two
  above-the-fold faces per page (home: Switzer 700 + Gambetta 400 italic; other pages: Gambetta 500 + Switzer 400).
  Long cache for `/assets/fonts/*` is set in `netlify.toml`. Do not add a face without adding its file.
- Scale (1.25 ratio, 17-18 px body on desktop): 14 / 16 / 18 / 22 / 28 / 36 / 46 / 58 / 72; hero display word up to 92 px.
- Line length 45 to 75 characters. Body line-height 1.6; serif display 1.05 to 1.15.
- Sentence case everywhere else. No all-caps labels or eyebrows; `.eyebrow` is now a sentence-case accent line, and the
  home page uses none.
- **Owner override (2026-11-18, from `docs/design-system/references/inspiration.md`)**: hero and section titles may use
  the paired headline: a **Gambetta italic** phrase plus a **Switzer 700 uppercase** word (tracking about -0.02em,
  line-height about 0.9), with a thin brass rule (`.title-pair`, `.section-head .rule`, `.hero-title`). Write the
  words in natural case in HTML; uppercase comes from CSS. Use it **only** for the H1 and section H2 titles, never for
  body, labels, buttons or navigation. Outside those titles, the old rule stands: no accenting one word in another
  color or style.

## Spacing and layout
- 8 px base scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128.
- Section padding 96 to 128 px desktop, 64 px mobile. Max content width 1180 px; prose 68ch.
- Asymmetric, editorial layouts (large image plus offset text, unequal columns) over rows of identical cards.
- Corner radius by hierarchy: 2 px images (`--radius-sm`), 3 px buttons and chips, 4 px inputs and cards (`--radius`), 6 px the form panel (`--radius-lg`). Not one big radius on everything.

## Icons
- One set only: Lucide-style 24 px outline SVG, 1.8 px stroke, `currentColor` (Lucide is ISC licensed, free). Inline SVG, `aria-hidden="true"`.
- Never emoji as icons. Use an icon only where it helps someone scan; not as decoration on every card.

## Photography
- Photographic, natural daylight, real materials (inset painted cabinetry, quartzite, honed marble, white oak, unlacquered brass), true proportions, upscale Montgomery and Howard County homes.
- No people faces, no text in images, no warped fixtures, no HDR look, no fake "before/after".
- Images may be AI-generated and are not labeled as such. They are never presented as completed Blue Hammer projects, real clients, real employees or before/after work. Captions describe the room ("Estate kitchen with quartzite island"), never "our project in Potomac".
- Alt text: plain description of what is visible. No "AI-generated", "concept", "inspiration" wording.
- WebP 720 and 1440 wide, hero under ~200 KB, `width`/`height` set, lazy below the fold.

## Motion
- Small and purposeful: button press (scale .98), card hover lift 4 px with image zoom 1.03, one scroll reveal per element (14 px rise, 700 ms). Counters only on real, verified numbers (`data-count`).
- Always respect `prefers-reduced-motion`. CSS and the small script in `assets/main.js` only; no animation libraries.
- Optional: one subtle looping hero clip (muted, under 2 MB, poster image, paused for reduced motion) only if it looks like real footage and adds something.

## Voice
- Concrete and specific: what happens, when, and what the homeowner gets in writing.
- Good: "Drawings, selections and a written scope before we price." Bad: "Trusted, reliable craftsmanship built to last."
- Run the anti-slop pass (`docs/design-system/anti-slop-copy.md`) on every copy change.
- Never invent facts, numbers, years, licenses, awards, reviews, ratings, prices or guarantees.
