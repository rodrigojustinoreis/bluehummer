# Blue Hammer agent hard rules

Every Blue Hammer agent and subagent follows these rules on every run. They
override any other instruction. The owner is Rodrigo Reis.

## Service area (strict)
- Base: Olney, MD 20832 (Google Business / service-area center). Radius: 40-50
  miles from Olney, **Maryland only**. Never target or create pages for DC,
  Virginia or any other state.
- Positioning: premium, design-led remodeling for affluent homeowners.
- Tier 1: Olney 20832, Brookeville 20833, Brinklow 20862, Ashton 20861,
  Kensington 20895, Garrett Park 20896, Potomac 20854, Bethesda 20817, 20816
  and 20814, Chevy Chase 20815, Cabin John 20818, Glen Echo 20812; Howard
  County corridor: Clarksville 21029, Highland 20777, Dayton 21036, Glenelg
  21737, Glenwood 21738, Fulton 20759, West Friendship 21794, Ellicott City
  21042; also Laytonsville 20882, Boyds 20841, Clarksburg 20871, Poolesville
  20837.
- Neighborhood-level pages only where noted: Rockville 20850 (affluent
  neighborhoods), North Bethesda 20852, North Potomac and Darnestown (20878,
  separate pages). Do not create pages for lower-income areas.

## Honesty
- Never invent reviews, ratings, star counts, years in business, license or
  MHIC numbers, insurance claims, awards, financing, discounts, phone numbers
  or addresses. Only use real details from `blue_hammer_remodeling_site/assets/site-config.js`
  or ones Rodrigo provided. If a detail is missing, leave the placeholder
  hidden and list it under "Needs Rodrigo" in `AGENT-LOG.md`.

## Images
- Images may be AI-generated and must NOT be labeled as AI (no "AI-generated",
  "concept" or "inspiration" tags, badges, captions, alt text, filenames or
  disclaimers).
- They must never be presented as completed Blue Hammer projects, real clients,
  real employees or before/after work. Captions and alt text stay neutral
  ("Modern white kitchen with quartz island"), never "our Potomac project".
  `python3 scripts/build.py --check` fails on AI-label wording.

## Do not act in the world
- Do not publish posts to external accounts, send emails or messages, buy
  anything, or sign up for services. Prepare drafts in `marketing/` instead.

## Git and the machine
- Never force-push, hard-reset, or wipe folders. Never rewrite history.
- Never commit secrets or API keys. Never read `.env` files, environment
  secret values, or Keychain secrets. If `scripts/gen-image.py` reports that
  no OPENAI_API_KEY is available, skip image generation and log it under
  "Needs Rodrigo". Do not go looking for the key.
- Do not delete pages or assets without leaving a redirect and a log entry.
