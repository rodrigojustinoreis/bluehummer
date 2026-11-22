# Image and motion sources

Real photographs used on the site that were not made by or for Blue Hammer. **Used as illustrative imagery; not
Blue Hammer projects.** Captions and alt text only describe what is visible; they never say or imply that Blue
Hammer built these rooms or that they belong to Blue Hammer clients.

## Licenses relied on (read on 2026-11-20)

These are free licenses with conditions. They are **not** public domain.

- **Unsplash License**, https://unsplash.com/license. The page says all images "can be downloaded and used for
  free", for "commercial and non-commercial purposes", "No permission needed (though attribution is
  appreciated!)". Not allowed: "Images cannot be sold without significant modification" and "Compiling images from
  Unsplash to replicate a similar or competing service". Attribution is not required (suggested format: "Photo by
  NAME on Unsplash"). This covers free Unsplash photos only. Unsplash+ photos are under a separate paid license and
  are **not** used here: each photo page below was checked and says "Free to use under the Unsplash License".
- **Pexels License**, https://www.pexels.com/license/ (page title "Free Stock Photo & Video License"): free to
  use, may be modified, attribution "not necessary but always appreciated". Not allowed: showing identifiable people
  in a bad light, selling unaltered copies, implying endorsement by people or brands in the image, redistributing on
  other stock or wallpaper platforms, using the media in a trademark. The help article
  https://help.pexels.com/hc/en-us/articles/360042295214 returned HTTP 403 to the automated fetch and was not
  read. **No Pexels photo is used in the end** (see "Considered and not used").

All six photos come from **Unsplash**, as free photos. The home page credits the photographers by name in a small
line under the services ("Photographs: ..."); the site name is left out of page text because `scripts/build.py`
FORBIDDEN rejects the word "Unsplash" on public pages (an older rule against starter-site wording).

## Photos on the home page (2026-11-20)

Downloaded through each photo page's official download link (`/download?force=true&w=2560`, which redirects to
images.unsplash.com) on 2026-11-20 at 2560 px wide. Originals kept outside the repo. Published files are WebP
(JPEG for the social image), re-encoded with Pillow, with **no EXIF, GPS, XMP or ICC metadata** written.
Camera, as shown on the photo page (Unsplash shows the model, not settings or a date).

| # | Repo files (`blue_hammer_remodeling_site/assets/`) | Photographer | Photo page | Download URL used | Camera | Used where |
|---|---|---|---|---|---|---|
| 1 | `home-hero-kitchen-gudakov-{720,1440,1920}.webp`, `home-og-kitchen-gudakov-1200x630.jpg`; copy `tools/remotion/public/home-hero-kitchen-gudakov-1920.webp` | Zac Gudakov (@zacgudakov) | https://unsplash.com/photos/LC-6Dnwo6_g | https://unsplash.com/photos/LC-6Dnwo6_g/download?force=true&w=2560 | FUJIFILM X-T3 (location listed: South Carolina, USA; published 2023-04-30) | Hero carousel slide 1 and poster (fetchpriority high); og:image / twitter:image; schema primaryImageOfPage |
| 2 | `home-hero-bath-beach-{720,1440,1920}.webp`; copy in `tools/remotion/public/` | Taylor Beach (@taylor65s) | https://unsplash.com/photos/PR7h5QGXd8A | https://unsplash.com/photos/PR7h5QGXd8A/download?force=true&w=2560 | Canon EOS 6D Mark II (Seattle, United States; published 2020-11-07) | Hero carousel slide 2 |
| 3 | `home-hero-living-tosolini-{720,1440,1920}.webp`; copy in `tools/remotion/public/` | Francesca Tosolini (@fromitaly) | https://unsplash.com/photos/XyGvEj587Mc | https://unsplash.com/photos/XyGvEj587Mc/download?force=true&w=2560 | Canon EOS 6D (published 2019-06-10) | Hero carousel slide 3 |
| 4 | `home-kitchen-elliot-{720,1440}.webp` | Clay Elliot (@ibidsy) | https://unsplash.com/photos/1by_GbwEMwc | https://unsplash.com/photos/1by_GbwEMwc/download?force=true&w=2560 | Canon EOS 80D (published 2020-10-03) | Services card "Kitchen remodeling" |
| 5 | `home-bath-gudakov-{720,1440}.webp` | Zac Gudakov (@zacgudakov) | https://unsplash.com/photos/FPim6ZLM6fc | https://unsplash.com/photos/FPim6ZLM6fc/download?force=true&w=2560 | FUJIFILM X-T3 (South Carolina, USA; published 2023-04-30) | Services card "Bathroom remodeling" |
| 6 | `home-interior-george-{720,1440}.webp` | Ronnie George (@realestateron) | https://unsplash.com/photos/S0-e9aITeHc | https://unsplash.com/photos/S0-e9aITeHc/download?force=true&w=2560 | Canon EOS R (Baton Rouge, LA, USA; published 2026-02-10) | Services card "Basements and interiors" |

Date accessed for all rows: **2026-11-20**. License for all rows: **Unsplash License**, https://unsplash.com/license.

Checks done on each: the photo page states the free Unsplash License (not Unsplash+); the page lists a camera
model; the image was looked at in full: a real photograph (lens perspective, real light, normal real-estate
interior), no people, no readable text or visible brand after the edits below.

### Edits (allowed by the license: "modify")
- #2 (bathroom): a candle jar on the vanity tray had a small printed label with readable words; the label area is
  filled with the jar's own color so no text is readable.
- #4 (kitchen card): a small maker's badge on the refrigerator door is covered with the plain steel just below it.
- #6 (living room): cropped to 85.5% of the width from the left (removes a refrigerator with a visible maker logo
  and photo magnets) and to 3:2; the three small framed pictures on the mantel (family photographs) are blurred so
  no person is shown or identifiable.
- All: resized (never upscaled), WebP quality 64 to 78 (#1 to #3 at 1920 px stay under about 210 KB).

### Alt text and captions used
- #1 alt "Kitchen with white shaker cabinets, a farmhouse sink under a window and a white range with gold-toned
  handles"; caption "White shaker cabinets, a farmhouse sink and gold-toned hardware."
- #2 alt "Bathroom with a wood double vanity, two oval mirrors, a glass shower and a freestanding tub"; caption
  "A wood double vanity, oval mirrors and a glass shower."
- #3 alt "Living room with wood floors, plantation shutters and an open dining area"; caption "Wood floors,
  plantation shutters and an open dining area."
- #4 alt "U-shaped kitchen with white shaker cabinets, a farmhouse sink under a window and a tiled backsplash".
- #5 alt "Bathroom with a green painted double vanity, gold-toned faucets and two arched mirrors".
- #6 alt "Living room with a brick fireplace, crown molding and an open kitchen beyond".

## Hero carousel video (Remotion)

- Files: `assets/video/home-hero-1280.{webm,mp4}` (1280x800, photo column on desktop and tablet) and
  `assets/video/home-hero-720.{webm,mp4}` (720x944, portrait phone hero). Made only from photos #1 to #3 above.
  16.5 s loop, 30 fps, 5.5 s per photo, 0.6 s crossfade, scale 1.000 to 1.025 per slide, no text, no audio track.
- Composition `HomeHeroCarousel` / `HomeHeroCarouselMobile` in `tools/remotion/src/HomeHeroCarousel.tsx`.
  Reproduce with `cd tools/remotion && ./render.sh home-hero` (Remotion master in `out/`, then ffmpeg: H.264 CRF 29
  veryslow +faststart, VP9 CRF 41; a keyframe at every slide start).
- **Remotion license** (read 2026-11-20 at https://www.remotion.dev/pricing and in
  `tools/remotion/node_modules/remotion/LICENSE.md`, v4.0.545): the Free License covers "an individual" and "a
  for-profit organization with up to 3 employees", with "Unlimited commercial use"; a paid Company License is
  required only for organizations that do not qualify. Condition relied on: Blue Hammer Remodeling is a one-owner
  business (fewer than 4 employees). If the company grows past 3 employees, a Remotion Company License is needed
  before rendering again (videos already rendered stay usable as videos; check the terms then). No React or
  Remotion code ships to the site.

## Considered and not used (2026-11-20)
- Pexels 8089190 and 8089188 (Max Vakhtbovych, Nikon D800, real photographs): readable sign on the wall
  ("love rules"), European outlets, high-gloss cabinets that read as staged luxury.
- Pexels 8288957 (Allyson Salness, Sony ILCE-7RM3; the brief listed it under Vakhtbovych): readable appliance logo
  on the refrigerator; dated HDR look.
- Pexels 6782573 (Max Vakhtbovych, Nikon D810): real photo, acceptable; the two Unsplash bathrooms fitted the
  warm traditional direction better.
- Pexels 16113326 (Hongyue Stone-Jon Lee, Canon 5DS R): hotel-style luxury bath, lit magnifier mirror.
- Pexels 8583860 (Curtis Adams, Canon EOS R6): usable; not needed once the six were approved.
- Unsplash YBxrveqHAFU: photographer watermark/logo in the image and a readable poster.
- Unsplash 9OKuf13OidA, asgkXxIQrPU (Peter Muniz): readable cosmetics brand label on the vanity.
- Unsplash koLQ6-45B3k: furniture looks virtually staged.

## Homepage local section map (2026-11-21)
- `blue_hammer_remodeling_site/assets/home-map-maryland.svg`: decorative outline of Maryland (with county lines), DC and the neighbouring states, plus a soft marker at Olney (39.153 N, 77.067 W). Generated locally from `us-atlas@3.0.1` `counties-10m.json` (ISC license, Mike Bostock; derived from the U.S. Census Bureau cartographic boundary files, which are public domain U.S. government data) with `topojson-client@3.1.0` and `d3-geo@3.1.1` (Mercator fitted to Maryland). Generator script kept out of the repo (scratchpad); inputs and versions are listed here so it can be rebuilt. Shown at 40% opacity, `alt=""` and `aria-hidden`.
