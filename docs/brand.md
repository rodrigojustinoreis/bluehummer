# Blue Hammer Remodeling: brand guideline

> **AUTHORITATIVE: refinement of 2026-11-20 (owner: "a designer who brings trust, modern and traditional at the
> same time").** This block wins over every other statement in this file, including the "Current rules" note
> below where it says Barlow Condensed for the H1, orange for the primary button, a white page or cool grey.
> - **Type roles.** **Gambetta 500** (upright serif, never italic, no small caps): the page H1 only.
>   **Switzer** (400 to 700): everything else (H2, H3, body, navigation, buttons, forms, captions).
>   **Barlow Condensed 800**: the logo wordmark only.
> - **H1 settings.** `clamp(2.5rem, 1.5rem + 3.2vw, 4.25rem)` = 68 px at 1440; line-height 1.06; tracking
>   -0.018em; `text-wrap: balance`. Phones (700 px and under): `clamp(2.375rem, 10.4vw, 3rem)` = 38 px at 320,
>   40.6 px at 390; line-height 1.08. Home H1 ("Home remodeling." / "In Maryland.", two fixed lines):
>   `clamp(3.5rem, 1.5rem + 3.6vw, 4.75rem)` = 76 px at 1440, line-height 1.03, tracking -0.022em; phones
>   `clamp(2.1875rem, 10.6vw, 4rem)` = 35 px at 320 (so the fixed first line fits), 41 px at 390, line-height 1.05.
>   H2 is unchanged (Switzer 600, 28 to 40 px, 1.14, -0.022em).
> - **Color tokens** (`:root` in `site-src/assets/main.css`):
>
>   | Token | Hex | Role |
>   |---|---|---|
>   | `--navy` | `#142131` | Header, footer, headings, rules |
>   | `--royal` / `--royal-hover` | `#0864D8` / `#074EAE` | Links, focus ring on light surfaces |
>   | `--action` / `--action-hover` | `#0B57C0` / `#0A4596` | Primary button fill (white text) and its hover |
>   | `--paper` | `#FDFCFA` | Page surface (warm near-white) |
>   | `--soft` | `#F6F3EE` | Dense text bands, consultation section, image placeholders |
>   | `--white` | `#FFFFFF` | Form fields, dropdown menu, header button |
>   | `--ink` / `--muted` | `#172638` / `#55606B` | Body text / secondary text and captions |
>   | `--line` / `--line-strong` | `#E7E2D9` / `#C8C0B3` | Warm hairlines |
>   | `--field-line` | `#857C70` | Field and outline-button borders (4.1:1 on white) |
>   | `--on-dark` / `--focus-on-dark` / `--on-navy-hover` | `#CBD6E3` / `#9AC6FF` / `#DCE8F7` | Text, focus ring and button hover on navy |
>   | `--orange` | `#FF7A24` | The two hairlines inside the logo wordmark. Nothing else. |
> - **Primary button rule.** `.btn--primary` is `--action` with white text (6.69:1), hover `--action-hover`,
>   pressed navy, focus a 2 px royal outline offset 3 px. Inside the navy header and the open mobile menu the same
>   button is white with navy text (16.26:1 for the text and for the shape against the header), hover `#DCE8F7`.
>   The mobile bar and the form's Continue and Send buttons use the blue primary. Orange is never a button, bar,
>   rule or text color.
> - **Font license.** Gambetta and Switzer: Indian Type Foundry, ITF Free Font License, read at
>   https://www.fontshare.com/licenses/itf-ffl on 2026-11-20: free commercial use and self-hosting with
>   `@font-face` are allowed; the files may not be modified, subset, converted or redistributed. Note file:
>   `blue_hammer_remodeling_site/assets/fonts/FONT-LICENSES.txt`. Barlow Condensed: SIL OFL 1.1.
> - **Superseded by this block:** "Barlow Condensed 800 for the page H1", "orange `#FF7A24` on the primary
>   button", "white page, cool grey `#F4F6F8`", "No Gambetta, no ivory" and "do not change typefaces to look
>   traditional". Still in force: sentence case, no eyebrows, no italics, no ornament, no brass, the layouts.

> **Current rules (2026-11-20, redesign phase 1).** Identity v2: navy `#142131`, royal `#0864D8`, orange `#FF7A24`
> (primary button only), white and cool grey `#F4F6F8`, the hammer logo, Barlow Condensed + Switzer. Type and
> layout follow `docs/design-system/design-brief.md` > "2026-11-20 direction" and the "Typography (current)"
> block below. Sections of this file that mention palette A, "Heritage Navy & Brass", ivory, brass, Gambetta,
> italic paired titles, uppercase display words or brass rules describe superseded identities and are kept for
> history only. Do not restyle pages toward them. Source of the live rules: `site-src/assets/main.css` (one layer
> since 2026-11-20; `python3 scripts/build.py` minifies it into the published copy, which is never edited).

Every design or copy task reads this file first. If a change conflicts with it, update this
file in the same commit and say why in AGENT-LOG.md.

## Position
Design-led kitchen, bath and lower-level remodeling for established homes, with small repairs as the
easy first job. Based in Olney, MD; serving Maryland, Washington, DC and Virginia within about 40 miles
(updated 2026-11-18; core market remains Montgomery and Howard County). The site should feel like a high-end Maryland remodeler
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

## Typography (current, 2026-11-20)
- **Switzer** (400, 500, 600, 700) carries the hierarchy: H2, H3, body, labels, buttons, navigation. Sentence case.
- **Gambetta 500** (upright) is the page H1, in sentence case, and nothing else. **Barlow Condensed 800** is the
  logo wordmark only (uppercase, as drawn). (Superseded the same day: Barlow Condensed 800 as the H1 face.)
- No all-caps headings. No eyebrow label above headings. No word in a heading set in another color or style.
- Scale: H1 `clamp(2.5rem, 1.5rem + 3.2vw, 4.25rem)`, line-height 1.06 (home H1 up to 4.75rem); H2 `clamp(1.75rem, 1.2rem + 1.6vw,
  2.5rem)` weight 600; H3 1.1875rem weight 600; body 1.0625rem / 1.62; lede 1.1875rem; captions and small text
  0.875rem. Line length 45 to 75 characters.
- Spacing: 12 columns, 1240 px, 32 px gap; section padding `--sec` (72 to 120 px) for image-led sections and
  `--sec-tight` (48 to 72 px) for dense text bands; radius 2 px on images, 3 px on buttons and inputs.
- The primary button is blue `#0B57C0` with white text (superseded: orange). Rules and dividers are warm grey or navy.
- Preloaded faces (`preload_fonts()` in `scripts/build.py`): `gambetta-500`, `switzer-400`, `barlow-condensed-800` (the wordmark is live text in the header).

## Typography (history: palette A and the first v2 pass, superseded)
- Display: **Gambetta** (Fontshare, ITF Free Font License, free for commercial web use). Weights 400, 400 italic, 500, 600.
- Text and UI: **Switzer** (Fontshare, ITF Free Font License). Weights 400 to 700.
- **Self-hosted** (2026-11-18): woff2 files in `assets/fonts/` (`gambetta-400`, `gambetta-400-italic`, `gambetta-500`,
  `gambetta-600`, `switzer-400` to `switzer-700`), declared with `@font-face` + `font-display: swap` at the top of
  `site-src/assets/main.css` (source; the published `assets/main.css` is the minified copy written by
  `python3 scripts/build.py`). Since 2026-11-20 the Gambetta files are no longer declared or loaded (unused by the
  v2 identity); the files stay in `assets/fonts/`. No request to `api.fontshare.com`. `scripts/build.py` `preload_fonts()` preloads only the two
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
- Always respect `prefers-reduced-motion`. CSS and the small script in `site-src/assets/main.js` (published minified as `assets/main.js`) only; no animation libraries.
- Optional: one subtle looping hero clip (muted, under 2 MB, poster image, paused for reduced motion) only if it looks like real footage and adds something.

## Voice
- Concrete and specific: what happens, when, and what the homeowner gets in writing.
- Good: "Drawings, selections and a written scope before we price." Bad: "Trusted, reliable craftsmanship built to last."
- Run the anti-slop pass (`docs/design-system/anti-slop-copy.md`) on every copy change.
- Never invent facts, numbers, years, licenses, awards, reviews, ratings, prices or guarantees.
