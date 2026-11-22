#!/usr/bin/env python3
"""Blue Hammer Remodeling — static site builder.

Source of truth for page content:  site-src/pages/<slug>.html
    First line is an HTML comment with JSON metadata:  <!--meta {...} -->
    The rest is the <main> content fragment (without the shared consultation section).
    Placeholders available inside fragments:
        {{BREADCRUMBS}}     semantic breadcrumb nav built from meta.breadcrumb
        {{FORM:some-id}}    a lead form with the given id (contact page)
        {{ARROW}} {{CHECK}} {{ICON:name}} inline SVG icons (one Lucide-style set, see ICONS)
Shared chrome (head, header, consultation section, footer, mobile CTA, JSON-LD)
lives in this file so every page stays consistent.

Source of truth for CSS / JS:  site-src/assets/main.css, main.js, site-config.js  (readable, commented)
    The build minifies each one with esbuild (pinned in tools/package.json; install with
    `npm --prefix tools ci`) into blue_hammer_remodeling_site/assets/ under the SAME file name, so URLs
    do not change and the ?v=<content hash> cache buster keeps working. No bundling, no source maps.
    The published copies are generated: never edit them, edit site-src/assets/ and run this script.
    site-config.js (phone, email, MHIC number, review profile) is the owner-edited data file:
    edit site-src/assets/site-config.js, then run `python3 scripts/build.py`.

Output (the folder Netlify publishes as-is, no build command there, so the output is committed):
    blue_hammer_remodeling_site/<slug>.html, sitemap.xml, llms.txt, assets/main.css, assets/main.js,
    assets/site-config.js

Usage:  python3 scripts/build.py            # minify assets, build every page, sitemap.xml and llms.txt
        python3 scripts/build.py --check    # build the pages, then validate links, alt text, schema, copy
                                            # rules, llms.txt, and that every published asset equals a fresh
                                            # minify of its source. --check never rewrites the assets: when
                                            # one is stale or hand-edited it fails and names the source file.
Both commands stop with a clear message when esbuild is missing or is not the pinned version.
"""
from __future__ import annotations
import hashlib, html, json, pathlib, re, subprocess, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "site-src" / "pages"
OUT = ROOT / "blue_hammer_remodeling_site"

SITE = "https://bluehammermd.com"
BRAND = "Blue Hammer Remodeling"
OG_IMAGE = "assets/og-blue-hammer.jpg"          # 1200x630
LOGO = "assets/bh-logo-v2.png"                  # schema logo (owner package 2026-11-18 22:30)
MARK = "assets/bh-hammer-v2-160.webp"          # header/footer hammer mark: the owner package PNG resized to 160px WebP (2026-11-22, 73 KB -> 3 KB)
FAVICON = "assets/bh-hammer-v2-64.png"          # owner package PNG resized to 64px (2026-11-22); served with a content-hash ?v= query
THEME_COLOR = "#142131"                         # owner package
TODAY = "2026-11-19"

# ---------------------------------------------------------------------------
# Service area: Olney base, about 40 miles across Maryland, DC and Virginia (owner, 2026-11-18).
# AREAS lists the places that have pages / areaServed today (Maryland Tier 1); DC/VA come with AUDIT item 16.
# ---------------------------------------------------------------------------
MONTGOMERY = "Montgomery County, Maryland"
HOWARD = "Howard County, Maryland"
AREAS = [
    ("Olney", MONTGOMERY), ("Brookeville", MONTGOMERY), ("Brinklow", MONTGOMERY), ("Ashton", MONTGOMERY),
    ("Sandy Spring", MONTGOMERY), ("Laytonsville", MONTGOMERY),
    ("Potomac", MONTGOMERY), ("North Potomac", MONTGOMERY), ("Darnestown", MONTGOMERY),
    ("Bethesda", MONTGOMERY), ("North Bethesda", MONTGOMERY), ("Chevy Chase", MONTGOMERY),
    ("Kensington", MONTGOMERY), ("Garrett Park", MONTGOMERY), ("Cabin John", MONTGOMERY), ("Glen Echo", MONTGOMERY),
    ("Rockville", MONTGOMERY), ("Silver Spring", MONTGOMERY), ("Boyds", MONTGOMERY), ("Clarksburg", MONTGOMERY), ("Poolesville", MONTGOMERY),
    ("Clarksville", HOWARD), ("Highland", HOWARD), ("Dayton", HOWARD), ("Glenelg", HOWARD), ("Glenwood", HOWARD),
    ("Fulton", HOWARD), ("West Friendship", HOWARD), ("Ellicott City", HOWARD),
]
# Sitewide footer sentence. Also used verbatim as the business description in JSON-LD, so the
# structured data says exactly what every page shows.
FOOTER_BLURB = ("Repairs and design-led remodeling for established homes within about 40 miles of Olney, "
                "in Maryland, DC and Virginia.")
# Schema type of the business node. It is a service-area business: the address carries only the real
# locality / region / ZIP (no street address, no phone until the owner confirms them in site-src/assets/site-config.js).
# Never add empty properties. `serviceType` is NOT valid on this type (it belongs to Service) and was the
# property the validators rejected on every page (2026-11-19).
BUSINESS_TYPE = "HomeAndConstructionBusiness"

# ---------------------------------------------------------------------------
# URL form (2026-11-19): ONE public form per page, extensionless, no trailing slash:
#   index.html -> /        kitchen-remodeling.html -> /kitchen-remodeling
# Netlify serves /name from name.html natively. Canonical, og:url, JSON-LD, sitemap and every internal
# link use this form. Fragments in site-src/ keep writing links as "name.html"; render() converts them.
# ---------------------------------------------------------------------------
def page_path(slug: str) -> str:
    return "/" if slug == "index.html" else "/" + slug[:-len(".html")]

def page_url(slug: str) -> str:
    return SITE + page_path(slug)

_LINK_RE = re.compile(r'\b(href|action)="/?([a-z0-9-]+\.html)([?#][^"]*)?"')

def pretty_links(out_html: str) -> str:
    """Rewrite internal page links (href/action) from name.html to the canonical extensionless form."""
    def sub(m):
        if not (SRC / m.group(2)).exists():
            return m.group(0)
        return f'{m.group(1)}="{page_path(m.group(2))}{m.group(3) or ""}"'
    return _LINK_RE.sub(sub, out_html)

# Text that must never appear in public pages (off-strategy places, other states, dev notes).
FORBIDDEN = [
    "Gaithersburg", "Germantown", "Aspen Hill", "Wheaton", "DMV", "Washington area",  # vague regional phrasing; name real places
    "starter website", "Unsplash", "before public launch", "Available when contact details are added",
    "Replace with approved", "pre-launch", "PRE-LAUNCH", "lorem",
    # Unproven price wording removed in the 2026-11-19 content pass (budget factors only, no ranges).
    "planning range", "Planning range", "cost ranges",
    # Image labeling: imagery stays neutral (never "AI" labels, never claimed as Blue Hammer projects).
    "AI-generated", "AI generated", "AI-created", "design concept", "Design concept", "DESIGN INSPIRATION",
    # Anti-slop copy (see docs/design-system/anti-slop-copy.md)
    "built to last", "unparalleled", "leverage", "seamless", "world-class", "top-notch", "second to none", "elevate your",
]

# ---------------------------------------------------------------------------
# CSS / JS assets (2026-11-20): readable sources in site-src/assets/, minified copies published.
# Tool: esbuild, exact version pinned in tools/package.json (+ package-lock.json). Each file is minified
# on its own (stdin -> stdout): no --bundle, so url(fonts/...) and image paths are left exactly as written
# (they are relative to the PUBLISHED assets folder), no --format, so nothing is wrapped or converted:
# main.js stays a classic script (loaded with defer), site-config.js stays a plain script that sets the
# global window.BLUE_HAMMER_CONFIG, and top-level names are not renamed. No source maps.
#
# Targets are explicit and conservative, so the minifier may shorten syntax but never emits anything
# newer than the sources already use, and never has to lower anything:
#   JS  es2020  - the newest syntax in main.js is optional chaining (?.), ES2020. An ES level is used
#                 instead of browser versions on purpose: with browser versions esbuild 0.28 refuses the
#                 file ("Transforming destructuring ... is not supported yet") because of old engine bugs
#                 in its compatibility table.
#   CSS chrome108 / edge108 / firefox121 / safari15.4 - the floor main.css already needs (:has(), dvh,
#                 inset, aspect-ratio). With this floor esbuild keeps every declaration as written; the
#                 only addition is -webkit-user-select next to user-select (Safari needs the prefix).
# Output is ASCII-only (esbuild default; non-ASCII characters in strings become \u escapes), so the
# files do not depend on the charset the server declares. Legal comments are dropped: the sources have
# only our own comments, which stay in site-src/.
# ---------------------------------------------------------------------------
SRC_ASSETS = ROOT / "site-src" / "assets"
TOOLS = ROOT / "tools"
ESBUILD = TOOLS / "node_modules" / ".bin" / "esbuild"
_ESBUILD_COMMON = ["--minify", "--legal-comments=none", "--log-level=warning"]
ASSETS = {  # published name -> esbuild flags
    "main.css": ["--loader=css", "--target=chrome108,edge108,firefox121,safari15.4"],
    "main.js": ["--loader=js", "--target=es2020"],
    "site-config.js": ["--loader=js", "--target=es2020"],
}
INSTALL_HINT = "Install the pinned dev tools first:  npm --prefix tools ci"

def esbuild_ready() -> None:
    """Stop (never publish unminified files) unless the pinned esbuild is installed."""
    pinned = json.loads((TOOLS / "package.json").read_text(encoding="utf-8"))["devDependencies"]["esbuild"]
    if not ESBUILD.exists():
        sys.exit(f"build.py: esbuild is not installed ({ESBUILD.relative_to(ROOT)} is missing), so the CSS/JS "
                 f"cannot be minified and nothing was built.\n{INSTALL_HINT}")
    try:
        found = subprocess.run([str(ESBUILD), "--version"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as e:
        sys.exit(f"build.py: esbuild could not be run ({e}); nothing was built.\n{INSTALL_HINT}")
    if found != pinned:
        sys.exit(f"build.py: esbuild {found} is installed but tools/package.json pins {pinned}; the output would "
                 f"not be reproducible, so nothing was built.\n{INSTALL_HINT}")

def minify(name: str) -> bytes:
    src = SRC_ASSETS / name
    run = subprocess.run([str(ESBUILD), *_ESBUILD_COMMON, *ASSETS[name], f"--sourcefile={src.relative_to(ROOT)}"],
                         input=src.read_bytes(), capture_output=True)
    if run.returncode != 0 or not run.stdout.strip():
        sys.exit(f"build.py: esbuild failed on {src.relative_to(ROOT)}; nothing was built.\n{run.stderr.decode('utf-8', 'replace')}")
    if run.stderr.strip():  # warnings (log level "warning"): show them, they usually mean a typo in the source
        print(run.stderr.decode("utf-8", "replace").rstrip(), file=sys.stderr)
    return run.stdout

def publish_assets(write: bool) -> list[str]:
    """Minify site-src/assets/* into the published folder. With write=False (--check) nothing is written:
    a published file that differs from a fresh minify of its source is reported instead."""
    esbuild_ready()
    stale = []
    for name in ASSETS:
        fresh, published = minify(name), OUT / "assets" / name
        if published.exists() and published.read_bytes() == fresh:
            continue
        if write:
            published.write_bytes(fresh)
        else:
            stale.append(f"assets/{name}: the published file {'differs from' if published.exists() else 'is missing; expected'} "
                         f"a fresh minify of site-src/assets/{name} (stale or hand-edited output). The file to edit is "
                         f"site-src/assets/{name}; then run: python3 scripts/build.py")
    return stale

def asset_v(path: str) -> str:
    """Content-hash cache buster (sha256, first 12 hex), as in the owner's 2026-11-18 22:30 package."""
    digest = hashlib.sha256((OUT / path).read_bytes()).hexdigest()[:12]
    return f"{path}?v={digest}"

# ---------------------------------------------------------------------------
# Icons / partials
# ---------------------------------------------------------------------------
def svg(path: str, cls: str = "") -> str:
    return (f'<svg aria-hidden="true" class="{cls}" fill="none" stroke="currentColor" stroke-linecap="round" '
            f'stroke-linejoin="round" stroke-width="1.8" viewbox="0 0 24 24">{path}</svg>')

ARROW = svg('<path d="M5 12h14m-6-6 6 6-6 6"></path>')
CHECK = svg('<path d="m5 12 4 4L19 6"></path>')
PIN = svg('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"></path><circle cx="12" cy="10" r="2.5"></circle>')
MENU = svg('<path d="M4 6h16M4 12h16M4 18h16"></path>', "icon-menu")
CLOSE = svg('<path d="M6 6l12 12M18 6 6 18"></path>', "icon-close")
PHONE = svg('<path d="M5 3h4l2 5-2.7 2a15 15 0 0 0 5.7 5.7l2-2.7 5 2v4a2 2 0 0 1-2.2 2A18 18 0 0 1 3 5.2 2 2 0 0 1 5 3Z"></path>')
CHEVRON = svg('<path d="m6 9 6 6 6-6"></path>')

# One Lucide-style set (24 px, 1.8 stroke, currentColor, aria-hidden). Used in fragments as {{ICON:name}}.
ICONS = {
    "pencil-ruler": '<path d="M4 20l1-4L16.5 4.5a2.1 2.1 0 0 1 3 3L8 19z"></path><path d="m14.5 6.5 3 3"></path><path d="M13 20h7"></path>',
    "cabinet": '<rect x="4" y="3" width="16" height="18" rx="1"></rect><path d="M12 3v18"></path><path d="M9.5 10v3M14.5 10v3"></path>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"></path><path d="m3 13 9 5 9-5"></path>',
    "grid": '<rect x="3" y="3" width="18" height="18" rx="1"></rect><path d="M3 9h18M3 15h18M9 3v18M15 3v18"></path>',
    "lamp": '<path d="M12 3v4"></path><path d="M5 15a7 7 0 0 1 14 0z"></path><path d="M10 19a2 2 0 0 0 4 0"></path>',
    "heat": '<path d="M3 21h18"></path><path d="M7 17c-1.5-2 1.5-4 0-6s1.5-4 0-6"></path><path d="M12 17c-1.5-2 1.5-4 0-6s1.5-4 0-6"></path><path d="M17 17c-1.5-2 1.5-4 0-6s1.5-4 0-6"></path>',
    "shelves": '<path d="M4 4v16M9 4v16"></path><path d="m13.5 4.8 4.4 14.6"></path><path d="M3 20h18"></path>',
    "clipboard": '<rect x="5" y="4" width="14" height="18" rx="2"></rect><rect x="9" y="2" width="6" height="4" rx="1"></rect><path d="m9 14 2 2 4-4"></path>',
}

def img(src_base: str, alt: str, *, w: int, h: int, cls: str = "", lazy: bool = True, sizes: str | None = None) -> str:
    sizes = sizes or "(max-width: 700px) 100vw, (max-width: 960px) 50vw, 48vw"
    load = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    return (f'<img alt="{html.escape(alt)}" class="{cls}" decoding="async" {load} height="{h}" sizes="{sizes}" '
            f'src="assets/{src_base}-720.webp" srcset="assets/{src_base}-720.webp 720w, assets/{src_base}-1440.webp 1440w" width="{w}"/>')

def lead_form(form_id: str) -> str:
    f = form_id
    return (
        f'<form class="lead-form" id="{f}" name="consultation" method="post" action="/thank-you.html" '
        f'data-netlify="true" netlify-honeypot="companyWebsite" novalidate="">'
        f'<input type="hidden" name="form-name" value="consultation"/>'
        f'<div class="form-head"><h3>Tell us about your project</h3><span aria-live="polite" class="form-progress">Step 1 of 2</span></div>'
        f'<div aria-hidden="true" class="form-progress-track"><i></i></div>'
        f'<div class="form-step active" data-step="1">'
        f'<div class="field"><label for="{f}-type">What would you like to remodel? *</label>'
        f'<select id="{f}-type" name="projectType" required=""><option value="">Select a service</option>'
        f'<option value="Kitchen Remodeling">Kitchen Remodeling</option><option value="Bathroom Remodeling">Bathroom Remodeling</option>'
        f'<option value="Basements &amp; Interiors">Basements &amp; Interiors</option><option value="Multiple Spaces">Multiple spaces / whole home</option><option value="Small Repair">Small repair</option>'
        f'<option value="Not Sure Yet">Not sure yet</option></select></div>'
        f'<div class="field"><label for="{f}-timing">When are you hoping to start? *</label>'
        f'<select id="{f}-timing" name="timeline" required=""><option value="">Select a timeframe</option>'
        f'<option>As soon as practical</option><option>Within 1–3 months</option><option>Within 3–6 months</option><option>Just planning ahead</option></select></div>'
        f'<div class="field"><label for="{f}-zip">Project ZIP code *</label>'
        f'<input autocomplete="postal-code" id="{f}-zip" inputmode="numeric" maxlength="5" minlength="5" name="zip" pattern="[0-9]{{5}}" placeholder="e.g. 20832" required=""/>'
        f'<div class="field-hint">We use this to confirm your home is inside our service area.</div></div>'
        f'<div class="form-foot"><button class="btn btn--primary form-next" type="button">Continue</button></div></div>'
        f'<div class="form-step" data-step="2">'
        f'<div class="field-row"><div class="field"><label for="{f}-first">First name *</label>'
        f'<input autocomplete="given-name" id="{f}-first" maxlength="80" minlength="2" name="firstName" placeholder="First name" required=""/></div>'
        f'<div class="field"><label for="{f}-last">Last name *</label>'
        f'<input autocomplete="family-name" id="{f}-last" maxlength="80" name="lastName" placeholder="Last name" required=""/></div></div>'
        f'<div class="field-row"><div class="field"><label for="{f}-email">Email address *</label>'
        f'<input autocomplete="email" id="{f}-email" maxlength="180" name="email" placeholder="you@example.com" required="" type="email"/></div>'
        f'<div class="field"><label for="{f}-phone">Phone number *</label>'
        f'<input autocomplete="tel" id="{f}-phone" maxlength="25" minlength="7" name="phone" placeholder="(301) 000-0000" required="" type="tel"/></div></div>'
        f'<div class="field"><label for="{f}-message">A little about your project (optional)</label>'
        f'<textarea id="{f}-message" maxlength="3000" name="message" placeholder="Tell us what you’d like to change, your goals or any questions."></textarea></div>'
        f'<div aria-hidden="true" class="hp-field"><label for="{f}-website">Leave this blank</label>'
        f'<input autocomplete="off" id="{f}-website" name="companyWebsite" tabindex="-1" type="text"/></div>'
        f'<input name="utm_source" type="hidden"/><input name="utm_campaign" type="hidden"/>'
        f'<label class="form-consent"><input name="consent" required="" type="checkbox"/>'
        f'<span>I agree to be contacted about my project. My information will be used according to the <a href="privacy.html">Privacy Policy</a>. *</span></label>'
        f'<div class="form-foot"><button class="form-back" type="button">Back</button>'
        f'<button class="btn btn--primary" type="submit">Send consultation request</button></div></div>'
        f'<div aria-live="polite" class="form-status" role="status"></div>'
        f'<div class="field-hint form-note">No obligation. We review every request and follow up if the project and location are a fit.</div>'
        f'</form>')

def consultation_section() -> str:
    """Shared consultation section (redesign phase 1, 2026-11-20): light background, one plain heading that
    matches the button label, no eyebrow, no check icons. The form markup (lead_form) is unchanged."""
    return (
        '<section aria-labelledby="consult-title" class="consultation" id="consultation"><div class="container consult-grid"><div class="consult-intro">'
        '<h2 id="consult-title">Schedule a consultation</h2>'
        '<p class="consult-lede">Tell us the room, your timing and your ZIP code. We review each request and reply about the next step.</p>'
        '<ul class="consult-benefits"><li>Start with your priorities, budget range and timing</li>'
        '<li>Talk through scope, design direction and permits</li>'
        '<li>Confirm your home is inside our service area</li></ul>'
        '<div class="consult-contact"><div class="phone-slot"></div><p class="email-slot"></p></div></div>'
        f'<div class="consult-form">{lead_form("consult-form-consultation")}</div></div></section>')

# Navigation ---------------------------------------------------------------
NAV_AREAS = [
    ("service-areas.html", "All Service Areas"),
    ("olney-md.html", "Olney (home base)"),
    ("potomac-md.html", "Potomac"),
    ("bethesda-md.html", "Bethesda"),
    ("chevy-chase-md.html", "Chevy Chase"),
    ("kensington-garrett-park-md.html", "Kensington &amp; Garrett Park"),
    ("rockville-md.html", "Rockville"),
    ("silver-spring-md.html", "Silver Spring"),
    ("howard-county-md.html", "Howard County (Clarksville)"),
]
NAV_SERVICES = [
    ("services.html", "All Remodeling Services"),
    ("kitchen-remodeling.html", "Kitchen Remodeling"),
    ("bathroom-remodeling.html", "Bathroom Remodeling"),
    ("basements-interiors.html", "Basements &amp; Interiors"),
]

def existing(href: str) -> bool:
    return (SRC / href).exists()

def nav_dropdown(label: str, items, panel_id: str, active: bool) -> str:
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in items if existing(h))
    cls = ' class="active"' if active else ""
    return (f'<div class="nav-dropdown"><button aria-controls="{panel_id}" aria-expanded="false" type="button"{cls}>{label}{CHEVRON}</button>'
            f'<div class="dropdown-panel" id="{panel_id}">{links}</div></div>')

def brand(aria: str = "Blue Hammer Remodeling homepage") -> str:
    return (f'<a aria-label="{aria}" class="brand" href="index.html">'
            f'<img alt="" height="68" src="{MARK}" width="62"/>'
            f'<span class="brand-copy">BLUE HAMMER<small>REMODELING</small></span></a>')

def header(active: str, cta: str = "index.html#consultation") -> str:
    """`cta` is the page's own form when it has one (see cta_target), otherwise the home form."""
    def a(href, label, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<a class="{"active" if active == key else ""}" href="{href}"{cur}>{label}</a>'
    return (
        f'<header class="site-header"><div class="container nav-wrap">{brand()}'
        f'<button aria-controls="main-navigation" aria-expanded="false" class="menu-toggle" type="button">{MENU}{CLOSE}<span class="menu-label">Menu</span></button>'
        '<nav aria-label="Primary" class="nav-links" id="main-navigation">'
        + nav_dropdown("Services", NAV_SERVICES, "services-dropdown", active == "services")
        + a("process.html", "Our Process", "process")
        + nav_dropdown("Service Areas", NAV_AREAS, "areas-dropdown", active == "areas")
        + a("about.html", "About", "about")
        # Owner package 2026-11-18 22:30: Gallery and Contact left the header (still in the footer); title-case CTA.
        + f'<a class="btn btn--primary nav-cta-mobile" href="{cta}">Schedule a Consultation</a>'
        + '</nav>'
        # Redesign phase 1 (2026-11-20): the topline strip is gone; the phone slot (empty and hidden until the
        # owner confirms a number in site-config.js) sits beside the header button.
        f'<span class="phone-slot header-phone"></span>'
        f'<a class="btn btn--primary btn--sm header-cta" href="{cta}">Schedule a Consultation</a></div></header>')

def footer(cta: str = "index.html#consultation") -> str:
    def links(items):
        return '<ul class="footer-links">' + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in items) + '</ul>'
    areas = [(h, t.replace(" (home base)", "").replace(" (Clarksville)", "")) for h, t in NAV_AREAS[1:] if existing(h)]
    areas.append(("service-areas.html", "All service areas"))
    remodeling = [("kitchen-remodeling.html", "Kitchen remodeling"), ("bathroom-remodeling.html", "Bathroom remodeling"),
                  ("basements-interiors.html", "Basements &amp; interiors"), ("services.html", "All services"),
                  ("faq.html", "Frequently asked questions")]
    company = [("index.html", "Home"), ("projects.html", "Design gallery"), ("about.html", "About Blue Hammer"),
               ("process.html", "Our process"), ("reviews.html", "Client feedback"), ("contact.html", "Contact us"),
               (cta, "Schedule a consultation")]
    def group(title, items):
        return f'<div class="footer-group"><h2 class="footer-h">{title}</h2>{links(items)}</div>'
    # Redesign phase 1 (2026-11-20): compact footer. Same links as before (services, areas, company, legal);
    # the three groups are short wrapped rows instead of tall columns, and the written-scope sentence shares
    # the bottom line with the copyright.
    return (
        '<footer class="footer"><div class="container"><div class="footer-top">'
        f'<div class="footer-about">{brand()}'
        f'<p>{FOOTER_BLURB}</p>'
        '<p class="phone-slot"></p><p class="email-slot"></p><span class="license-slot"></span></div>'
        '<div class="footer-nav">'
        + group("Remodeling", remodeling) + group("Service areas", areas) + group("Company", company) + '</div></div>'
        '<div class="footer-bottom"><p>© 2026 Blue Hammer Remodeling. Olney, Maryland. '
        'Scope, schedule and any required permits or licenses are confirmed in writing before work is accepted.</p>'
        '<nav aria-label="Legal"><a href="privacy.html">Privacy policy</a><a href="terms.html">Website terms</a></nav></div></div></footer>')

def mobile_cta(target: str = "index.html#consultation") -> str:
    """Fixed mobile bar. Points at the form on the same page when there is one, so it never sends people away."""
    return (f'<div class="mobile-cta"><a aria-label="Call Blue Hammer" class="btn btn--outline mobile-phone phone-link" hidden="" href="#">{PHONE}</a>'
            f'<a class="btn btn--primary" href="{target}">Schedule a Consultation</a></div>')

def cta_target(meta: dict, body: str) -> str:
    """One target for every "Schedule a consultation" link on a page (header button, in-menu button, footer
    link, fixed mobile bar): #consultation on pages with the shared consultation section, the page's own
    form otherwise (/contact -> #contact-form), and the home form when the page has no form at all."""
    form = re.search(r'<form class="lead-form" id="([a-z0-9-]+)"', body)
    if meta.get("consult", True):
        return "#consultation"
    return f"#{form.group(1)}" if form else "index.html#consultation"

# ---------------------------------------------------------------------------
# Breadcrumbs, FAQ extraction, schema
# ---------------------------------------------------------------------------
def crumbs(meta: dict, slug: str):
    bc = meta.get("breadcrumb")
    if not bc:
        return []
    items = [("Home", "index.html")]
    if isinstance(bc, str):
        items.append((bc, slug))
    else:
        for i, it in enumerate(bc):
            it = it if isinstance(it, list) else [it]
            label, href = it[0], (it[1] if len(it) > 1 else None)
            items.append((label, href or (slug if i == len(bc) - 1 else None)))
    return items

def breadcrumb_html(items) -> str:
    if not items:
        return ""
    lis = []
    for i, (label, href) in enumerate(items):
        last = i == len(items) - 1
        if last:
            lis.append(f'<li aria-current="page">{html.escape(label)}</li>')
        else:
            lis.append(f'<li><a href="{href}">{html.escape(label)}</a></li>')
    return f'<nav aria-label="Breadcrumb" class="breadcrumbs"><ol>{"".join(lis)}</ol></nav>'

FAQ_RE = re.compile(r'<details class="faq-item"><summary>(.*?)</summary>(.*?)</details>', re.S)
TAG_RE = re.compile(r"<[^>]+>")

def text_only(fragment: str) -> str:
    return html.unescape(TAG_RE.sub("", fragment)).replace("’", "’").strip()

def extract_faqs(body: str):
    return [(text_only(q), text_only(a)) for q, a in FAQ_RE.findall(body)]

def area_served():
    return [{"@type": "City", "name": n, "containedInPlace": {"@type": "AdministrativeArea", "name": c}} for n, c in AREAS]

def schema_graph(meta: dict, slug: str, body: str, crumb_items) -> str:
    url = page_url(slug)
    page_type = meta.get("type", "WebPage")
    hero = meta.get("image")
    business = {
        "@type": BUSINESS_TYPE, "@id": SITE + "/#business", "name": BRAND, "url": SITE + "/",
        "description": FOOTER_BLURB,
        "logo": {"@type": "ImageObject", "url": f"{SITE}/{LOGO}"},
        "image": f"{SITE}/{OG_IMAGE}",
        "address": {"@type": "PostalAddress", "addressLocality": "Olney", "addressRegion": "MD", "postalCode": "20832", "addressCountry": "US"},
        "areaServed": area_served(),
        "knowsAbout": ["Kitchen remodeling", "Bathroom remodeling", "Basement finishing"],
    }
    # WebSite is on every page so the page node's isPartOf reference always resolves inside the graph.
    graph = [business, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND,
                        "publisher": {"@id": SITE + "/#business"}, "inLanguage": "en-US"}]
    page = {"@type": page_type, "@id": url + "#webpage", "url": url, "name": meta["title"],
            "description": meta["description"], "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": SITE + "/#business"}, "inLanguage": "en-US", "dateModified": TODAY}
    if hero:
        page["primaryImageOfPage"] = {"@type": "ImageObject", "url": f"{SITE}/{hero}"}
    if len(crumb_items) > 1:
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label,
             **({"item": page_url(href)} if href else {})}
            for i, (label, href) in enumerate(crumb_items)]})
    graph.append(page)
    svc = meta.get("service")
    if svc:
        service = {"@type": "Service", "@id": url + "#service", "name": svc["name"], "serviceType": svc.get("serviceType", svc["name"]),
                   "description": svc.get("description", meta["description"]), "provider": {"@id": SITE + "/#business"},
                   "url": url, "areaServed": area_served()}
        area = meta.get("area")
        if area:
            service["areaServed"] = [{"@type": "City", "name": n, "containedInPlace": {"@type": "AdministrativeArea", "name": area["county"]}}
                                     for n in area["places"]]
        graph.append(service)
    # FAQ markup is built from the visible <details class="faq-item"> blocks, so it always matches the page.
    # Exactly one FAQPage node per page: on the FAQ page itself the page node IS the FAQPage (a second,
    # empty FAQPage node there was the "missing mainEntity" error); elsewhere it is a separate #faq node.
    faqs = extract_faqs(body)
    if faqs:
        main_entity = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
        if page_type == "FAQPage":
            page["mainEntity"] = main_entity
        else:
            graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": main_entity})
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'

# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
def preload_fonts(slug: str):
    """Only the faces visible above the fold (Gambetta: Fontshare, ITF Free Font License; Open Sans, Montserrat and
    Barlow Condensed: SIL OFL 1.1). 2026-11-21: Gambetta 400 for every H1/H2, Open Sans text, Montserrat for the
    navigation and buttons (both variable woff2 files, latin subset from Google Fonts), Barlow for the wordmark."""
    return ["gambetta-400", "open-sans-var-latin", "montserrat-var-latin", "barlow-condensed-800-ascii"]

def head(meta: dict, slug: str, body: str, crumb_items) -> str:
    url = page_url(slug)
    title = html.escape(meta["title"])
    desc = html.escape(meta["description"])
    robots = meta.get("robots", "index,follow")
    og_img = meta.get("ogImage", OG_IMAGE)
    return (
        '<head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/>'
        f'<title>{title}</title><meta content="{desc}" name="description"/>'
        f'<link href="{url}" rel="canonical"/><meta content="{THEME_COLOR}" name="theme-color"/><meta content="{robots}" name="robots"/>'
         f'<link href="{asset_v(FAVICON)}" rel="icon" type="image/png"/>'
        + "".join(f'<link as="font" crossorigin="" href="assets/fonts/{f}.woff2" rel="preload" type="font/woff2"/>' for f in preload_fonts(slug))
        + f'<link href="{asset_v("assets/main.css")}" rel="stylesheet"/>'
        '<meta content="website" property="og:type"/><meta content="en_US" property="og:locale"/>'
        f'<meta content="{BRAND}" property="og:site_name"/><meta content="{url}" property="og:url"/>'
        f'<meta content="{title}" property="og:title"/><meta content="{desc}" property="og:description"/>'
        f'<meta content="{SITE}/{og_img}" property="og:image"/><meta content="1200" property="og:image:width"/><meta content="630" property="og:image:height"/>'
        f'<meta content="Blue Hammer Remodeling — repairs and design-led remodeling based in Olney, Maryland" property="og:image:alt"/>'
        f'<meta content="summary_large_image" name="twitter:card"/><meta content="{title}" name="twitter:title"/>'
        f'<meta content="{desc}" name="twitter:description"/><meta content="{SITE}/{og_img}" name="twitter:image"/>'
        + schema_graph(meta, slug, body, crumb_items)
        + '<noscript><style>.form-step{display:block}.form-next,.form-back,.form-progress,.form-progress-track{display:none}</style></noscript>'
        '</head>')

def parse_fragment(path: pathlib.Path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--meta\s+(\{.*?\})\s*-->\s*", raw, re.S)
    if not m:
        sys.exit(f"{path}: missing <!--meta {{...}} --> header")
    meta = json.loads(m.group(1))
    body = raw[m.end():].strip()
    return meta, body

def render(slug: str, meta: dict, body: str) -> str:
    crumb_items = crumbs(meta, slug)
    body = (body.replace("{{BREADCRUMBS}}", breadcrumb_html(crumb_items))
                .replace("{{ARROW}}", ARROW).replace("{{CHECK}}", CHECK))
    body = re.sub(r"\{\{ICON:([a-z-]+)\}\}", lambda m: svg(ICONS[m.group(1)]), body)
    body = re.sub(r"\{\{FORM:([a-z0-9-]+)\}\}", lambda m: lead_form(m.group(1)), body)
    if meta.get("consult", True):
        body += consultation_section()
    cta = cta_target(meta, body)
    # "mobileCta": false in the page meta (thank-you): no fixed conversion bar, and the body class lets the
    # CSS drop the bottom padding that is otherwise reserved for the bar on small screens.
    bar = meta.get("mobileCta", True)
    return pretty_links(
        '<!DOCTYPE html>\n<html lang="en">' + head(meta, slug, body, crumb_items)
        + ('<body>' if bar else '<body class="no-mobile-cta">') + '<a class="skip-link" href="#main">Skip to main content</a>\n'
        + header(meta.get("nav", ""), cta) + f'<main id="main" tabindex="-1">{body}</main>' + footer(cta)
        + (mobile_cta(cta) if bar else "")
        + f'<script src="{asset_v("assets/site-config.js")}"></script><script defer="" src="{asset_v("assets/main.js")}"></script></body></html>\n')

def build(check_only: bool = False):
    """Returns (pages, stale_assets). Assets go first: the pages carry a content hash of the published files."""
    stale_assets = publish_assets(write=not check_only)
    missing = [n for n in ASSETS if not (OUT / "assets" / n).exists()]
    if missing:
        sys.exit("build.py: " + "\n".join(stale_assets) if stale_assets else f"build.py: missing published assets {missing}")
    pages = {}
    for path in sorted(SRC.glob("*.html")):
        meta, body = parse_fragment(path)
        out_html = render(path.name, meta, body)
        (OUT / path.name).write_text(out_html, encoding="utf-8")
        pages[path.name] = (meta, out_html)
    write_sitemap(pages)
    (OUT / "llms.txt").write_text(llms_txt(pages), encoding="utf-8")
    return pages, stale_assets

def indexable(pages):
    """Slugs of the public indexable pages: the sitemap set (no noindex pages, none with "sitemap": false)."""
    return [s for s, (m, _) in pages.items() if "noindex" not in m.get("robots", "") and m.get("sitemap") is not False]

# ---------------------------------------------------------------------------
# llms.txt (2026-11-20): plain Markdown in the llmstxt.org layout (H1, blockquote summary, H2 sections of
# "- [Title](URL): description"). It lists exactly the sitemap URLs. Every title and description is the
# page's own approved <title> (without the brand suffix) and meta description, so no new copy lives here.
# The summary states only facts the pages already show. Not in the sitemap; no llms-full.txt.
# ---------------------------------------------------------------------------
LLMS_COMPANY_ORDER = ["index.html", "about.html", "process.html", "projects.html", "faq.html", "contact.html",
                      "privacy.html", "terms.html"]

def llms_txt(pages) -> str:
    public = indexable(pages)
    def ordered(wanted, pool):
        first = [s for s in wanted if s in pool]
        return first + sorted(s for s in pool if s not in first)
    services = ordered([h for h, _ in NAV_SERVICES], [s for s in public if pages[s][0].get("nav") == "services"])
    areas = ordered([h for h, _ in NAV_AREAS], [s for s in public if pages[s][0].get("nav") == "areas"])
    company = ordered(LLMS_COMPANY_ORDER, [s for s in public if s not in services and s not in areas])
    def line(slug):
        meta = pages[slug][0]
        return f"- [{meta['title'].split(' | ')[0]}]({page_url(slug)}): {meta['description']}"
    towns = [html.unescape(re.sub(r"\s*\(.*?\)", "", t)) for h, t in NAV_AREAS[1:] if h in areas]
    summary = (f"{BRAND} is a remodeling company based in Olney, Maryland 20832. It remodels kitchens, bathrooms, "
               f"basements and interior rooms. The site has service-area pages for {', '.join(towns[:-1])} and {towns[-1]}, "
               "all in Maryland. A consultation is requested through the form on the site.")
    out = [f"# {BRAND}", "", f"> {summary}", ""]
    for title, slugs in (("Services", services), ("Service areas", areas), ("Company", company)):
        out += [f"## {title}", ""] + [line(s) for s in slugs] + [""]
    return "\n".join(out)

def write_sitemap(pages):
    urls = []
    for slug in indexable(pages):
        meta = pages[slug][0]
        loc = page_url(slug)
        pr = meta.get("priority", 0.7)
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{meta.get('lastmod', TODAY)}</lastmod><changefreq>{meta.get('changefreq', 'monthly')}</changefreq><priority>{pr:.1f}</priority></url>")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
class Collector(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1 = 0; self.links = []; self.imgs = []; self.title = ""; self._in_title = False; self.ids = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "title": self._in_title = True
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag in ("img", "script", "link") and (a.get("src") or a.get("href")):
            if tag == "link" and a.get("rel") not in ("stylesheet", "icon"): return
            self.imgs.append((tag, a.get("src") or a.get("href"), a.get("alt")))
        if tag == "img" and "srcset" in a:
            for part in a["srcset"].split(","):
                self.imgs.append(("img", part.strip().split(" ")[0], a.get("alt", "")))
        if a.get("id"): self.ids.append(a["id"])
    def handle_data(self, data):
        if self._in_title: self.title += data
    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False

def schema_problems(slug: str, out_html: str):
    """JSON-LD rules: valid JSON, no empty values, internal @id references resolve, URLs in canonical form,
    one FAQPage at most and its questions/answers equal to the visible FAQ, no invalid business properties."""
    probs = []
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', out_html, re.S)
    if len(blocks) != 1: return [f"{len(blocks)} JSON-LD blocks (expected 1)"]
    try: data = json.loads(blocks[0])
    except Exception as e: return [f"invalid JSON-LD ({e})"]
    graph = data.get("@graph", [])
    ids = {n.get("@id") for n in graph}
    def walk(node, path):
        if isinstance(node, dict):
            if set(node) == {"@id"} and node["@id"] not in ids: probs.append(f"JSON-LD reference {node['@id']} not in graph")
            for k, v in node.items(): walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            if not node: probs.append(f"JSON-LD empty list at {path}")
            for v in node: walk(v, path)
        elif node is None or (isinstance(node, str) and not node.strip()):
            probs.append(f"JSON-LD empty value at {path}")
        elif isinstance(node, str) and node.startswith(SITE) and re.search(r"\.html(#|$)", node):
            probs.append(f"JSON-LD URL not in canonical form: {node}")
    walk(graph, "@graph")
    biz = [n for n in graph if n.get("@id") == SITE + "/#business"]
    if len(biz) != 1: probs.append("JSON-LD needs exactly one business node")
    else:
        b = biz[0]
        for bad in ("serviceType", "streetAddress", "telephone", "email", "aggregateRating", "review", "priceRange"):
            if bad in b or bad in b.get("address", {}): probs.append(f"business node must not carry '{bad}' (invalid or unconfirmed)")
        if not b.get("name") or not b.get("address", {}).get("addressLocality"): probs.append("business node missing name/address")
    faq_nodes = [n for n in graph if n.get("@type") == "FAQPage"]
    visible = extract_faqs(out_html)
    if len(faq_nodes) > 1: probs.append(f"{len(faq_nodes)} FAQPage nodes (max 1)")
    if bool(faq_nodes) != bool(visible): probs.append("FAQPage node and visible FAQ do not both exist")
    for n in faq_nodes:
        marked = [(q.get("name"), q.get("acceptedAnswer", {}).get("text")) for q in n.get("mainEntity", [])]
        if marked != visible: probs.append("FAQPage mainEntity differs from the visible questions/answers")
    return probs

# Extra wording rules for llms.txt only (whole words): no superlatives, credentials, prices or promises,
# and nothing addressed to AI systems.
LLMS_BANNED = re.compile(r"\b(best|top|leading|premier|licensed|insured|award\w*|guarantee\w*|years|reviews?|rated|"
                         r"rank\w*|cite|citation\w*|AI|LLMs?|assistants?|chatbots?|crawlers?|instructions?|phone)\b|[$★]|#1", re.I)

def llms_problems(pages):
    path = OUT / "llms.txt"
    if not path.exists(): return ["llms.txt: missing"]
    text = path.read_text(encoding="utf-8")
    probs = []
    if text != llms_txt(pages): probs.append("llms.txt: differs from the generated content (it is generated; do not edit it)")
    lines = text.split("\n")
    if lines[0] != f"# {BRAND}" or not lines[2].startswith("> "): probs.append("llms.txt: must start with the H1 and a blockquote summary")
    if [l for l in lines if l.startswith("## ")] != ["## Services", "## Service areas", "## Company"]: probs.append("llms.txt: unexpected H2 sections")
    links = re.findall(r"^- \[[^\]]+\]\(([^)]+)\): \S", text, re.M)
    if len(links) != len([l for l in lines if l.startswith("- ")]): probs.append("llms.txt: a list line is not '- [Title](URL): description'")
    expected = sorted(page_url(s) for s in indexable(pages))
    if sorted(links) != expected: probs.append(f"llms.txt: URLs differ from the sitemap set ({set(links) ^ set(expected)})")
    if sorted(links) != sorted(re.findall(r"<loc>(.*?)</loc>", (OUT / "sitemap.xml").read_text(encoding="utf-8"))): probs.append("llms.txt: URLs differ from sitemap.xml")
    probs += [f"llms.txt: forbidden text '{bad}'" for bad in FORBIDDEN if bad in text]
    prose = re.sub(r"\]\([^)]+\)", "]", text)  # wording rules apply to the text, not to the URLs
    probs += [f"llms.txt: wording not allowed here: '{m.group(0)}'" for m in LLMS_BANNED.finditer(prose)]
    return probs

def check(pages, stale_assets=()) -> int:
    errors = list(stale_assets)
    for name in ASSETS:  # the published copies must be the minified ones, and no source map may be published
        if (OUT / "assets" / (name + ".map")).exists(): errors.append(f"assets/{name}.map: source maps are not published")
    errors += llms_problems(pages)
    for slug, (meta, out_html) in pages.items():
        c = Collector(); c.feed(out_html)
        if c.h1 != 1: errors.append(f"{slug}: {c.h1} <h1> tags")
        if len(meta["title"]) > 65: errors.append(f"{slug}: title {len(meta['title'])} chars")
        if not (70 <= len(meta["description"]) <= 160): errors.append(f"{slug}: description {len(meta['description'])} chars")
        text = TAG_RE.sub(" ", out_html)
        for bad in FORBIDDEN:
            if bad in text: errors.append(f"{slug}: forbidden text '{bad}'")
        for href in c.links:
            if href.startswith(("http", "mailto:", "tel:")): continue
            target, _, frag = href.partition("#")
            target = target.partition("?")[0]  # query strings (e.g. ?service=) point at the same file
            if target.endswith(".html"): errors.append(f"{slug}: internal link not in canonical form {href}")
            if target.startswith("/"):  # canonical extensionless form: / -> index.html, /name -> name.html
                target = "index.html" if target == "/" else target[1:] + ".html"
            if target and not (OUT / target).exists(): errors.append(f"{slug}: broken link {href}")
            if not target and frag and frag not in c.ids: errors.append(f"{slug}: missing anchor #{frag}")
        for tag, src, alt in c.imgs:
            if src.startswith("http"): continue
            src = src.partition("?")[0]  # cache-busting ?v= queries
            if not (OUT / src).exists(): errors.append(f"{slug}: missing asset {src}")
            if tag == "img" and alt is None: errors.append(f"{slug}: <img> without alt ({src})")
            if alt and re.search(r"\bAI\b|AI-generated|concept|inspiration", alt, re.I): errors.append(f"{slug}: AI/concept label in alt text ({src})")
        if "{{" in out_html: errors.append(f"{slug}: unexpanded placeholder")
        # A reviews page with no real reviews (the empty-state block) stays out of the index and the sitemap.
        if 'class="review-empty"' in out_html and "noindex" not in meta.get("robots", ""):
            errors.append(f"{slug}: empty reviews page must be noindex (owner rule 2026-11-19)")
        canon = re.findall(r'<link href="([^"]+)" rel="canonical"/>', out_html)
        if canon != [page_url(slug)]: errors.append(f"{slug}: canonical {canon} != {page_url(slug)}")
        if f'<meta content="{page_url(slug)}" property="og:url"/>' not in out_html: errors.append(f"{slug}: og:url != canonical")
        errors += [f"{slug}: {e}" for e in schema_problems(slug, out_html)]
    # Sitemap: exactly the canonical URLs of the indexable pages, nothing else.
    expected = sorted(page_url(s) for s in indexable(pages))
    locs = sorted(re.findall(r"<loc>(.*?)</loc>", (OUT / "sitemap.xml").read_text(encoding="utf-8")))
    if locs != expected: errors.append(f"sitemap.xml: URLs differ from canonical indexable pages ({set(locs) ^ set(expected)})")
    titles, descs = {}, {}
    for slug, (meta, _) in pages.items():
        if meta["title"] in titles: errors.append(f"{slug}: duplicate title with {titles[meta['title']]}")
        if meta["description"] in descs: errors.append(f"{slug}: duplicate description with {descs[meta['description']]}")
        titles[meta["title"]] = slug; descs[meta["description"]] = slug
    for e in errors: print("  ✗", e)
    print(f"{'OK' if not errors else 'FAILED'}: {len(pages)} pages, {len(errors)} problems")
    return 1 if errors else 0

if __name__ == "__main__":
    checking = "--check" in sys.argv
    pages, stale_assets = build(check_only=checking)
    print(f"Built {len(pages)} pages → {OUT.relative_to(ROOT)}/ (+ sitemap.xml, llms.txt"
          + (")" if checking else f", {len(ASSETS)} minified assets)"))
    if checking:
        sys.exit(check(pages, stale_assets))
