# Blue Hammer keyword -> URL map (implemented)

Date: 2026-11-19. Source: Semrush export `Blue_Hammer_SEO_Keywords_2026-11-19.csv` (65 terms, US database).
Status: **published.** Committed as 0a9e24f, pushed to main and live on https://bluehammermd.com on 2026-11-19. Titles, H1s and robots values below were
read from the built output in `blue_hammer_remodeling_site/` after `python3 scripts/build.py --check` (OK, 24 pages).
Volumes, KD and intent are the CSV values, unchanged from the plan.

## How to read the numbers

- **Volume is US national monthly volume, not city volume.** Semrush reports the whole country for the phrase.
  It is a national estimate for the phrase and carries no information about where the searchers are, for
  town terms ("kitchen remodeling bethesda md") as much as for generic ones ("kitchen remodeling", 33,100).
- **KD "no data"** means Semrush has no difficulty score (volume 0 or missing, or KD 0 with no intent and no
  SERP data). It does **not** mean the term is easy.
- Low KD numbers on town terms (KD 1-15) are real Semrush values. Where the export's "SERP Features" column
  lists Local Pack for a term, part of that result page is a map pack, which depends on a Google Business
  Profile, proximity and reviews rather than on the page alone. The SERPs were not inspected individually, so
  this is per-term export data, not a statement about every result. Nothing here is a ranking promise.
- URLs are in the canonical form (no `.html`).

## One primary keyword per URL (as built)

| URL | Primary keyword | Volume (US national) | KD | Final title | Final H1 | Status |
|---|---|---|---|---|---|---|
| `/` | home remodeling maryland | 320 | 36 | Home Remodeling in Maryland \| Blue Hammer Remodeling | Home remodeling. In Maryland. | Implemented (batch A; H1 by owner decision) |
| `/kitchen-remodeling` | kitchen remodeling maryland | 320 | 9 | Kitchen Remodeling in Maryland \| Blue Hammer Remodeling | Kitchen remodeling in Maryland. | Implemented (batch A) |
| `/bathroom-remodeling` | bathroom remodeling maryland | 320 | 21 | Bathroom Remodeling in Maryland \| Blue Hammer Remodeling | Bathroom remodeling in Maryland. | Implemented (batch A) |
| `/basements-interiors` | basement remodeling maryland | 210 | 10 | Basement Remodeling & Finishing in Maryland \| Blue Hammer | Basement remodeling in Maryland. | Implemented (batch A) |
| `/olney-md` | home remodeling olney md | 50 | 3 | Home Remodeling in Olney, MD \| Blue Hammer Remodeling | Home remodeling in Olney, MD. | Implemented (batch B) |
| `/bethesda-md` | home remodeling bethesda md | 320 | 5 | Home Remodeling in Bethesda, MD \| Blue Hammer Remodeling | Home remodeling in Bethesda, MD. | Implemented (batch B) |
| `/potomac-md` | home remodeling potomac md | 110 | 4 | Home Remodeling in Potomac, MD \| Blue Hammer Remodeling | Home remodeling in Potomac, MD. | Implemented (batch B) |
| `/rockville-md` | home remodeling rockville md | 170 | 4 | Home Remodeling in Rockville, MD \| Blue Hammer Remodeling | Home remodeling in Rockville, MD. | Implemented (batch B) |
| `/chevy-chase-md` | home remodeling chevy chase md | 110 | 3 | Home Remodeling in Chevy Chase, MD \| Blue Hammer Remodeling | Home remodeling in Chevy Chase, MD. | Implemented (batch C) |
| `/howard-county-md` | home remodeling howard county md | no data | no data | Home Remodeling in Howard County, MD \| Blue Hammer Remodeling | Home remodeling in Howard County, MD. | Implemented (batch C); kitchen term worked into hero, first topic, FAQ, description |
| `/kensington-garrett-park-md` | bathroom remodeling kensington md | 90 | 5 | Kensington & Garrett Park, MD Home Remodeling \| Blue Hammer | Home remodeling in Kensington and Garrett Park, MD. | Implemented (batch C); general two-town page, bathroom first |
| `/silver-spring-md` | home remodeling silver spring md | 140 | 11 | Home Remodeling in Silver Spring, MD \| Blue Hammer Remodeling | Home remodeling in Silver Spring, MD. | Implemented (batch C); page restored at the owner's request |
| `/service-areas` | home remodeling montgomery county md | 20 | no data | Home Remodeling in Montgomery County, MD \| Blue Hammer | Home remodeling in Montgomery County, MD. | Implemented (batch C) |

Notes on the primaries:

- Town pages take the general "home remodeling + town" term, because each town has one page that covers all
  three services. The service + town terms ("kitchen remodeling bethesda md") sit on the same town page as
  secondaries, so two pages never compete for one term.
- `/howard-county-md`: "home remodeling howard county md" has **no data** in the export. The strongest term
  with data for that page is "kitchen remodeling howard county md" (140, KD 3); it is worked into the page.
- `/kensington-garrett-park-md`: the export has only one Kensington term ("bathroom remodeling kensington md",
  90, KD 5) and none for Garrett Park. It is the primary by default; the page stays a general town page.
- `/silver-spring-md`: the page was retired in an earlier pass and restored on 2026-11-19 at the owner's request.
  The retirement redirects were removed from `netlify.toml` and `_redirects`; the name is no longer blocked by the
  build; the page is in the nav, the footer, the hub, the sitemap and the business `areaServed`. No ZIP or
  neighborhood lists (owner: not needed).
- `/service-areas`: "home remodeling montgomery county md" (20, no KD data) fits the hub. County service
  terms go to the service pages.

## Supporting pages (no primary keyword from this export)

| URL | Final title | Final H1 | Robots | Status |
|---|---|---|---|---|
| `/services` | Remodeling Services: Kitchens, Baths & Basements \| Blue Hammer | Remodeling services, room by room. | index,follow | Implemented (batch A): hub, routes each project type to its service page |
| `/process` | Our Remodeling Process, Step by Step \| Blue Hammer Remodeling | Our process, step by step. | index,follow | Implemented (final batch): six steps, conditional planning, no durations |
| `/faq` | Remodeling FAQ: Budget, Schedule & Permits \| Blue Hammer | Remodeling questions, answered directly. | index,follow | Implemented (final batch): budget factors, schedule factors, permits by address, credential check, areas incl. Silver Spring (17 questions) |
| `/projects` | Kitchen, Bath & Basement Design Gallery \| Blue Hammer | Kitchen, bath and basement design gallery. | index,follow | Implemented (final batch): neutral captions, no towns / decades / house types |
| `/about` | About Blue Hammer Remodeling \| Based in Olney, Maryland | About Blue Hammer Remodeling. | index,follow | Implemented (final batch, owner notes): company, approach, what to expect |
| `/contact` | Contact Blue Hammer Remodeling \| Olney, MD | Contact Blue Hammer Remodeling. | index,follow | Implemented (final batch): area list incl. Silver Spring |
| `/reviews` | Client Feedback \| Blue Hammer Remodeling | Client feedback for Blue Hammer. | noindex,follow | Implemented (final batch): **noindex,follow, not in sitemap** while there are no reviews; URL and footer link kept |
| `/privacy` | Privacy Policy \| Blue Hammer Remodeling | Privacy policy | index,follow | Unchanged (reviewed, nothing to remove) |
| `/terms` | Website Terms \| Blue Hammer Remodeling | Website terms | index,follow | Implemented (final batch): "cost ranges" section is now "Budget information" |

`/404` and `/thank-you` are noindex and out of the sitemap, as before. The sitemap lists 21 URLs: every page above
except `/reviews`.

## Full map by URL (all 65 terms)

### `/`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling maryland | PRIMARY | 320 | 36 | Commercial |  |
| home remodeling | secondary | 27,100 | 45 | Commercial | National head term; supporting wording only, not a realistic target. |
| remodeling contractor | secondary | 6,600 | 41 | Commercial | National head term; supporting wording only, not a realistic target. |
| blue hammer remodeling | brand | 20 | no data | no data | Brand term. |

### `/kitchen-remodeling`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| kitchen remodeling maryland | PRIMARY | 320 | 9 | Commercial |  |
| kitchen remodeling | secondary | 33,100 | 49 | Commercial | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| kitchen remodeling near me | secondary | 14,800 | 49 | Transactional | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| kitchen renovation | secondary | 14,800 | 66 | Commercial | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| kitchen remodeling montgomery county md | secondary | 50 | 6 | Commercial | Regional variant of the page primary. |

### `/bathroom-remodeling`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| bathroom remodeling maryland | PRIMARY | 320 | 21 | Commercial |  |
| bathroom remodeling | secondary | 74,000 | 70 | Commercial | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| bathroom remodeling near me | secondary | 49,500 | 56 | Transactional | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| bathroom renovation | secondary | 27,100 | 54 | Commercial | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| bathroom remodeling montgomery county md | secondary | 40 | 25 | Commercial | Regional variant of the page primary. |

### `/basements-interiors`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| basement remodeling maryland | PRIMARY | 210 | 10 | Informational |  |
| basement finishing | secondary | 14,800 | 40 | Informational | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| basement remodeling | secondary | 9,900 | 49 | Commercial | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| basement finishing near me | secondary | 2,400 | 20 | Transactional | National head term or "near me" (decided by Google Business Profile and proximity); supporting wording only. |
| basement finishing montgomery county md | secondary | 30 | no data | no data | Regional variant of the page primary. |
| basement finishing maryland | secondary | 20 | no data | no data | Regional variant of the page primary. |
| basement remodeling montgomery county md | secondary | no data | no data | no data | Regional variant of the page primary. |

### `/olney-md`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling olney md | PRIMARY | 50 | 3 | Commercial |  |
| kitchen remodeling olney md | secondary | 110 | 5 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| bathroom remodeling olney md | secondary | 90 | 1 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement remodeling olney md | secondary | 70 | 3 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement finishing olney md | secondary | 10 | no data | no data | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| kitchen remodeling brookeville md | secondary | no data | no data | no data | Brookeville is covered on the Olney page. Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |

### `/bethesda-md`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling bethesda md | PRIMARY | 320 | 5 | Commercial |  |
| kitchen remodeling bethesda md | secondary | 390 | 15 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement remodeling bethesda md | secondary | 320 | 0 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| bathroom remodeling bethesda md | secondary | 260 | 4 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement finishing bethesda md | secondary | 20 | no data | no data | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |

### `/potomac-md`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling potomac md | PRIMARY | 110 | 4 | Commercial |  |
| bathroom remodeling potomac md | secondary | 260 | 5 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| kitchen remodeling potomac md | secondary | 210 | 5 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement remodeling potomac md | secondary | 70 | 6 | Navigational | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement finishing potomac md | secondary | 20 | no data | no data | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |

### `/rockville-md`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling rockville md | PRIMARY | 170 | 4 | Commercial |  |
| kitchen remodeling rockville md | secondary | 260 | 4 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| bathroom remodeling rockville md | secondary | 210 | 5 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement remodeling rockville md | secondary | 140 | 3 | Informational | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement finishing rockville md | secondary | 20 | no data | no data | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |

### `/chevy-chase-md`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling chevy chase md | PRIMARY | 110 | 3 | Commercial |  |
| kitchen remodeling chevy chase md | secondary | 170 | 5 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement remodeling chevy chase md | secondary | 170 | 2 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| bathroom remodeling chevy chase md | secondary | 70 | 6 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement finishing chevy chase md | secondary | 20 | no data | no data | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |

### `/howard-county-md`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling howard county md | PRIMARY | no data | no data | no data |  |
| kitchen remodeling howard county md | secondary | 140 | 3 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| bathroom remodeling howard county md | secondary | 50 | 2 | Commercial | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement remodeling howard county md | secondary | no data | no data | no data | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |
| basement finishing howard county md | secondary | no data | no data | no data | Service + town term; served by the town page (no service-by-city pages, owner 2026-11-19). |

### `/kensington-garrett-park-md`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| bathroom remodeling kensington md | PRIMARY | 90 | 5 | Commercial |  |

### `/service-areas`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling montgomery county md | PRIMARY | 20 | no data | no data |  |

### `/silver-spring-md`

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| home remodeling silver spring md | PRIMARY | 140 | 11 | Commercial |  |
| kitchen remodeling silver spring md | secondary | 210 | 10 | Commercial,Informational | Service + town term; served by the town page. |
| bathroom remodeling silver spring md | secondary | 170 | 6 | Informational | Service + town term; served by the town page. |
| basement remodeling silver spring md | secondary | 140 | 3 | Commercial | Service + town term; served by the town page. |
| basement finishing silver spring md | secondary | 20 | no data | no data | Service + town term; served by the town page. |

### /faq, /basements-interiors

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| basement finishing cost | FUTURE | 880 | 30 | Informational | Informational. Answered with budget factors (no dollar figures) on /faq and the service page. Not a ranking target as written. |
| basement finishing cost maryland | FUTURE | 10 | no data | no data | Informational. Answered with budget factors (no dollar figures) on /faq and the service page. Not a ranking target as written. |

### /faq, /bathroom-remodeling

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| bathroom remodel cost | FUTURE | 14,800 | 41 | Informational | Informational. Answered with budget factors (no dollar figures) on /faq and the service page. Not a ranking target as written. |
| bathroom remodel cost maryland | FUTURE | 40 | no data | no data | Informational. Answered with budget factors (no dollar figures) on /faq and the service page. Not a ranking target as written. |

### /faq, /kitchen-remodeling

| Keyword | Role | Volume (US national) | KD | Intent | Note |
|---|---|---|---|---|---|
| kitchen remodel cost | FUTURE | 12,100 | 46 | Informational | Informational. Answered with budget factors (no dollar figures) on /faq and the service page. Not a ranking target as written. |
| kitchen remodel cost maryland | FUTURE | 20 | no data | no data | Informational. Answered with budget factors (no dollar figures) on /faq and the service page. Not a ranking target as written. |

## Terms without a dedicated page (6 terms)

1. **Cost terms (6 terms).** "bathroom remodel cost" (14,800), "kitchen remodel cost" (12,100) and
   "basement finishing cost" (880) are national and informational. The Maryland variants (40, 20, 10) have no
   KD data. No page carries dollar figures: `/faq` and the three service pages answer these questions with the
   factors that make up a budget. A cost guide with figures would need the owner to confirm real prices first.
2. **Service + town terms** are secondaries on the town pages. Owner decision 2026-11-19: no service-by-city
   pages.
3. **Brookeville** ("kitchen remodeling brookeville md", no data) stays on the Olney page.

## Cannibalization check (as built)

- "kitchen / bathroom / basement remodeling maryland" are in the titles and H1s of the three service pages only.
  The home page takes "home remodeling maryland".
- `/services` is a hub with a general title; it does not repeat a service page title.
- Each town term appears on exactly one URL above. No two pages share a title or a meta description
  (`build.py --check` fails on duplicates).
- `/faq` answers budget, schedule and permit questions in general terms and links to the service and town pages
  for the detail; its title carries no town or service primary.

## What is verified and what is not

- Verified locally: titles, H1s, canonicals, robots and sitemap membership above (read from the built files).
- Not verified: rankings, impressions, indexing, or any effect on the Semrush site audit. Those depend on a
  deploy and a re-crawl. Nothing in this file is a ranking promise.
