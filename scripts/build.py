#!/usr/bin/env python3
"""Blue Hammer Remodeling — static site builder.

Source of truth for page content:  site-src/pages/<slug>.html
    First line is an HTML comment with JSON metadata:  <!--meta {...} -->
    The rest is the <main> content fragment (without the shared consultation section).
    Placeholders available inside fragments:
        {{BREADCRUMBS}}     semantic breadcrumb nav built from meta.breadcrumb
        {{SERVICE_CARDS}}   the three service cards (kitchen / bath / basements)
        {{FORM:some-id}}    a lead form with the given id (contact page)
        {{ARROW}} {{CHECK}} inline SVG icons
Shared chrome (head, topline, header, consultation section, footer, mobile CTA, JSON-LD)
lives in this file so every page stays consistent.

Output: blue_hammer_remodeling_site/<slug>.html + sitemap.xml  (the folder Netlify publishes)

Usage:  python3 scripts/build.py            # build everything
        python3 scripts/build.py --check    # build, then validate links, alt text, schema, copy rules
"""
from __future__ import annotations
import html, json, pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "site-src" / "pages"
OUT = ROOT / "blue_hammer_remodeling_site"

SITE = "https://bluehammermd.com"
BRAND = "Blue Hammer Remodeling"
OG_IMAGE = "assets/og-blue-hammer.jpg"          # 1200x630
LOGO = "assets/blue-hammer-logo-512.png"        # 512x292
MARK = "assets/blue-hammer-mark-140.webp"       # 140x80 header/footer mark
TODAY = "2026-11-18"

# ---------------------------------------------------------------------------
# Service area (strict): Olney base, Maryland only, Tier 1 places.
# ---------------------------------------------------------------------------
MONTGOMERY = "Montgomery County, Maryland"
HOWARD = "Howard County, Maryland"
AREAS = [
    ("Olney", MONTGOMERY), ("Brookeville", MONTGOMERY), ("Brinklow", MONTGOMERY), ("Ashton", MONTGOMERY),
    ("Sandy Spring", MONTGOMERY), ("Laytonsville", MONTGOMERY),
    ("Potomac", MONTGOMERY), ("North Potomac", MONTGOMERY), ("Darnestown", MONTGOMERY),
    ("Bethesda", MONTGOMERY), ("North Bethesda", MONTGOMERY), ("Chevy Chase", MONTGOMERY),
    ("Kensington", MONTGOMERY), ("Garrett Park", MONTGOMERY), ("Cabin John", MONTGOMERY), ("Glen Echo", MONTGOMERY),
    ("Rockville", MONTGOMERY), ("Boyds", MONTGOMERY), ("Clarksburg", MONTGOMERY), ("Poolesville", MONTGOMERY),
    ("Clarksville", HOWARD), ("Highland", HOWARD), ("Dayton", HOWARD), ("Glenelg", HOWARD), ("Glenwood", HOWARD),
    ("Fulton", HOWARD), ("West Friendship", HOWARD), ("Ellicott City", HOWARD),
]
SERVICE_TYPES = ["Kitchen remodeling", "Bathroom remodeling", "Basement finishing", "Interior remodeling",
                 "Custom cabinetry and millwork", "Design-build remodeling"]
BUSINESS_DESCRIPTION = ("Design-led kitchen, bathroom, basement and interior remodeling for established homes "
                        "in Montgomery and Howard County, Maryland. Based in Olney, MD.")

# Text that must never appear in public pages (off-strategy places, other states, dev notes).
FORBIDDEN = [
    "Silver Spring", "Gaithersburg", "Germantown", "Aspen Hill", "Wheaton", "DMV", "Northern Virginia and", "serving DC", "Washington area",
    "starter website", "Unsplash", "before public launch", "Available when contact details are added",
    "Replace with approved", "pre-launch", "PRE-LAUNCH", "lorem",
    # Image labeling: imagery stays neutral (never "AI" labels, never claimed as Blue Hammer projects).
    "AI-generated", "AI generated", "AI-created", "design concept", "Design concept", "DESIGN INSPIRATION",
    # Anti-slop copy (see docs/design-system/anti-slop-copy.md)
    "built to last", "unparalleled", "leverage", "seamless", "world-class", "top-notch", "second to none", "elevate your",
]

# ---------------------------------------------------------------------------
# Icons / partials
# ---------------------------------------------------------------------------
def svg(path: str, cls: str = "") -> str:
    return (f'<svg aria-hidden="true" class="{cls}" fill="none" stroke="currentColor" stroke-linecap="round" '
            f'stroke-linejoin="round" stroke-width="1.8" viewbox="0 0 24 24">{path}</svg>')

ARROW = svg('<path d="M5 12h14m-6-6 6 6-6 6"></path>')
CHECK = svg('<path d="m5 12 4 4L19 6"></path>')
PIN = svg('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"></path><circle cx="12" cy="10" r="2.5"></circle>')
MENU = svg('<path d="M4 6h16M4 12h16M4 18h16"></path>')
PHONE = svg('<path d="M5 3h4l2 5-2.7 2a15 15 0 0 0 5.7 5.7l2-2.7 5 2v4a2 2 0 0 1-2.2 2A18 18 0 0 1 3 5.2 2 2 0 0 1 5 3Z"></path>')

def img(src_base: str, alt: str, *, w: int, h: int, cls: str = "", lazy: bool = True, sizes: str | None = None) -> str:
    sizes = sizes or "(max-width: 700px) 100vw, (max-width: 960px) 50vw, 48vw"
    load = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    return (f'<img alt="{html.escape(alt)}" class="{cls}" decoding="async" {load} height="{h}" sizes="{sizes}" '
            f'src="assets/{src_base}-720.webp" srcset="assets/{src_base}-720.webp 720w, assets/{src_base}-1440.webp 1440w" width="{w}"/>')

SERVICE_CARDS_DATA = [
    ("kitchen-remodeling.html", "Kitchen Remodeling", "kitchen-design", 1080,
     "Remodeled kitchen with navy cabinetry and a marble island",
     "Custom cabinetry, natural stone and layouts planned around how your family actually cooks and gathers."),
    ("bathroom-remodeling.html", "Bathroom Remodeling", "bathroom-design", 1080,
     "Bathroom with a walk-in shower and navy double vanity",
     "Primary suites, hall baths and powder rooms with curbless showers, heated floors and quiet, durable detailing."),
    ("basements-interiors.html", "Basements &amp; Interiors", "basement-design", 1080,
     "Finished basement with built-in shelving and a living area",
     "Lower levels, built-ins and whole-interior refreshes that make every square foot feel intentional."),
]

def service_cards() -> str:
    cards = []
    for href, name, base, h, alt, blurb in SERVICE_CARDS_DATA:
        cards.append(
            f'<article class="service-card"><a aria-label="Learn about {name}" href="{href}">'
            f'{img(base, alt, w=1440, h=h, cls="service-photo")}</a>'
            f'<div class="service-body"><h3>{name}</h3><p>{blurb}</p>'
            f'<a class="text-link" href="{href}">Explore Service {ARROW}</a></div></article>')
    return '<div class="cards-3">' + "".join(cards) + '</div>'

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
        f'<option value="Basements &amp; Interiors">Basements &amp; Interiors</option><option value="Multiple Spaces">Multiple spaces / whole home</option>'
        f'<option value="Not Sure Yet">Not sure yet</option></select></div>'
        f'<div class="field"><label for="{f}-timing">When are you hoping to start? *</label>'
        f'<select id="{f}-timing" name="timeline" required=""><option value="">Select a timeframe</option>'
        f'<option>As soon as practical</option><option>Within 1–3 months</option><option>Within 3–6 months</option><option>Just planning ahead</option></select></div>'
        f'<div class="field"><label for="{f}-zip">Project ZIP code *</label>'
        f'<input autocomplete="postal-code" id="{f}-zip" inputmode="numeric" maxlength="5" minlength="5" name="zip" pattern="[0-9]{{5}}" placeholder="e.g. 20832" required=""/>'
        f'<div class="field-hint">We use this to confirm your home is inside our Maryland service area.</div></div>'
        f'<div class="form-foot"><button class="btn btn--primary form-next" type="button">Continue {ARROW}</button></div></div>'
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
        f'<div class="form-foot"><button class="form-back" type="button">← Back</button>'
        f'<button class="btn btn--primary" type="submit">Send Consultation Request {ARROW}</button></div></div>'
        f'<div aria-live="polite" class="form-status" role="status"></div>'
        f'<div class="field-hint" style="margin-top:17px">No obligation. We review every request and follow up if the project and location are a fit.</div>'
        f'</form>')

def consultation_section() -> str:
    return (
        '<section aria-labelledby="consult-title" class="consultation" id="consultation"><div class="container consult-grid"><div>'
        '<span class="eyebrow">Start with a conversation</span><h2 id="consult-title">Let’s talk about what your home could become.</h2>'
        '<p>Whether you have drawings in hand or just a few ideas, tell us about your project. We review every request and reply with honest next steps.</p>'
        f'<div class="consult-benefits"><div>{CHECK} Start with your priorities, budget range and timing</div>'
        f'<div>{CHECK} Talk through scope, design direction and permits</div>'
        f'<div>{CHECK} Confirm your home is inside our Maryland service area</div></div>'
        '<div class="consult-contact"><p>Prefer to speak with us?</p><div class="phone-slot"></div><p class="email-slot"></p></div></div>'
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
    return (f'<div class="nav-dropdown"><button aria-controls="{panel_id}" aria-expanded="false" type="button"{cls}>{label}</button>'
            f'<div class="dropdown-panel" id="{panel_id}">{links}</div></div>')

def brand(aria: str = "Blue Hammer Remodeling homepage") -> str:
    return (f'<a aria-label="{aria}" class="brand" href="index.html">'
            f'<img alt="" height="57" src="{MARK}" width="70"/>'
            f'<span class="brand-copy">BLUE HAMMER<small>REMODELING</small></span></a>')

def topline() -> str:
    return (f'<div class="topline"><div class="container"><span>{PIN} Based in Olney, MD · Serving Montgomery &amp; Howard County, Maryland</span>'
            '<div class="topline-right"><span class="phone-slot"></span><span>Design-led kitchen, bath &amp; basement remodeling</span></div></div></div>')

def header(active: str) -> str:
    def a(href, label, key):
        return f'<a class="{"active" if active == key else ""}" href="{href}">{label}</a>'
    return (
        f'<header class="site-header"><div class="container nav-wrap">{brand()}'
        '<nav aria-label="Primary navigation" class="nav-links" id="main-navigation">'
        + a("index.html", "Home", "home")
        + nav_dropdown("Services", NAV_SERVICES, "services-dropdown", active == "services")
        + a("projects.html", "Gallery", "inspiration")
        + a("about.html", "About Us", "about")
        + nav_dropdown("Service Areas", NAV_AREAS, "areas-dropdown", active == "areas")
        + a("faq.html", "FAQ", "faq")
        + a("contact.html", "Contact", "contact")
        + '</nav>'
        f'<button aria-controls="main-navigation" aria-expanded="false" aria-label="Open menu" class="menu-toggle" type="button">{MENU}</button>'
        f'<a class="btn btn--primary header-cta" href="index.html#consultation">Schedule a Consultation {ARROW}</a></div></header>')

def footer() -> str:
    areas = "".join(f'<a href="{h}">{t.replace(" (home base)", "").replace(" (Clarksville)", "")}</a>' for h, t in NAV_AREAS[1:] if existing(h))
    return (
        f'<footer class="footer"><div class="container"><div class="footer-grid"><div>{brand()}'
        '<p>Design-led remodeling for established homes in Montgomery and Howard County, Maryland. Based in Olney and built on clear scopes, honest timelines and craftsmanship you can see up close.</p>'
        '<p class="phone-slot"></p><p class="email-slot"></p><span class="license-slot"></span>'
        '</div>'
        '<div><h4>Explore</h4><div class="footer-links"><a href="index.html">Home</a><a href="projects.html">Design Gallery</a><a href="about.html">About Blue Hammer</a><a href="process.html">Our Process</a><a href="reviews.html">Client Feedback</a></div></div>'
        '<div><h4>Remodeling</h4><div class="footer-links"><a href="kitchen-remodeling.html">Kitchen Remodeling</a><a href="bathroom-remodeling.html">Bathroom Remodeling</a><a href="basements-interiors.html">Basements &amp; Interiors</a><a href="services.html">All Services</a><a href="faq.html">Frequently Asked Questions</a></div></div>'
        f'<div><h4>Service Areas</h4><div class="footer-links">{areas}<a href="service-areas.html">All Maryland Service Areas</a></div></div>'
        '<div><h4>Let’s talk</h4><div class="footer-links"><a href="index.html#consultation">Schedule a Consultation</a><a href="contact.html">Contact Us</a><a href="privacy.html">Privacy Policy</a><a href="terms.html">Website Terms</a></div>'
        '<p>Scope, schedule and any required permits or licenses are confirmed in writing before work is accepted.</p></div></div>'
        '<div class="footer-bottom"><span>© 2026 Blue Hammer Remodeling. All rights reserved.</span>'
        '<span>Olney, Maryland · Remodeling Montgomery &amp; Howard County · <a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></span></div></div></footer>')

def mobile_cta() -> str:
    return (f'<div class="mobile-cta"><a aria-label="Call Blue Hammer" class="btn btn--outline mobile-phone phone-link" hidden="" href="#">{PHONE}</a>'
            f'<a class="btn btn--primary" href="index.html#consultation">Schedule a Consultation {ARROW}</a></div>')

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
    url = SITE + "/" + ("" if slug == "index.html" else slug)
    page_type = meta.get("type", "WebPage")
    hero = meta.get("image")
    business = {
        "@type": "HomeAndConstructionBusiness", "@id": SITE + "/#business", "name": BRAND, "url": SITE + "/",
        "description": BUSINESS_DESCRIPTION,
        "logo": {"@type": "ImageObject", "url": f"{SITE}/{LOGO}", "width": 512, "height": 292},
        "image": f"{SITE}/{OG_IMAGE}",
        "address": {"@type": "PostalAddress", "addressLocality": "Olney", "addressRegion": "MD", "postalCode": "20832", "addressCountry": "US"},
        "areaServed": area_served(),
        "serviceType": SERVICE_TYPES,
        "knowsAbout": ["Kitchen remodeling", "Bathroom remodeling", "Basement finishing", "Custom cabinetry",
                       "Montgomery County residential permits", "Howard County residential permits"],
    }
    graph = [business]
    if slug == "index.html":
        graph.append({"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND,
                      "publisher": {"@id": SITE + "/#business"}, "inLanguage": "en-US"})
    page = {"@type": page_type, "@id": url + "#webpage", "url": url, "name": meta["title"],
            "description": meta["description"], "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": SITE + "/#business"}, "inLanguage": "en-US", "dateModified": TODAY}
    if hero:
        page["primaryImageOfPage"] = {"@type": "ImageObject", "url": f"{SITE}/{hero}"}
    if len(crumb_items) > 1:
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label,
             **({"item": SITE + "/" + ("" if href == "index.html" else href)} if href else {})}
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
    faqs = extract_faqs(body)
    if faqs:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'

# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
def head(meta: dict, slug: str, body: str, crumb_items) -> str:
    url = SITE + "/" + ("" if slug == "index.html" else slug)
    title = html.escape(meta["title"])
    desc = html.escape(meta["description"])
    robots = meta.get("robots", "index,follow")
    og_img = meta.get("ogImage", OG_IMAGE)
    return (
        '<head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/>'
        f'<title>{title}</title><meta content="{desc}" name="description"/>'
        f'<link href="{url}" rel="canonical"/><meta content="#0b2347" name="theme-color"/><meta content="{robots}" name="robots"/>'
        '<link href="assets/favicon.png" rel="icon" type="image/png"/><link href="https://api.fontshare.com" rel="preconnect" crossorigin=""/><link href="https://api.fontshare.com/v2/css?f[]=gambetta@400,500,600&amp;f[]=switzer@400,500,600,700&amp;display=swap" rel="stylesheet"/><link href="assets/main.css" rel="stylesheet"/>'
        '<meta content="website" property="og:type"/><meta content="en_US" property="og:locale"/>'
        f'<meta content="{BRAND}" property="og:site_name"/><meta content="{url}" property="og:url"/>'
        f'<meta content="{title}" property="og:title"/><meta content="{desc}" property="og:description"/>'
        f'<meta content="{SITE}/{og_img}" property="og:image"/><meta content="1200" property="og:image:width"/><meta content="630" property="og:image:height"/>'
        f'<meta content="Blue Hammer Remodeling — design-led remodeling in Olney and Montgomery County, Maryland" property="og:image:alt"/>'
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
                .replace("{{SERVICE_CARDS}}", service_cards())
                .replace("{{ARROW}}", ARROW).replace("{{CHECK}}", CHECK))
    body = re.sub(r"\{\{FORM:([a-z0-9-]+)\}\}", lambda m: lead_form(m.group(1)), body)
    if meta.get("consult", True):
        body += consultation_section()
    return (
        '<!DOCTYPE html>\n<html lang="en">' + head(meta, slug, body, crumb_items)
        + '<body><a class="skip-link" href="#main">Skip to main content</a>\n'
        + topline() + header(meta.get("nav", "")) + f'<main id="main">{body}</main>' + footer() + mobile_cta()
        + '<script src="assets/site-config.js"></script><script defer="" src="assets/main.js"></script></body></html>\n')

def build():
    pages = {}
    for path in sorted(SRC.glob("*.html")):
        meta, body = parse_fragment(path)
        out_html = render(path.name, meta, body)
        (OUT / path.name).write_text(out_html, encoding="utf-8")
        pages[path.name] = (meta, out_html)
    write_sitemap(pages)
    return pages

def write_sitemap(pages):
    urls = []
    for slug, (meta, _) in pages.items():
        if "noindex" in meta.get("robots", "") or meta.get("sitemap") is False:
            continue
        loc = SITE + "/" + ("" if slug == "index.html" else slug)
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

def check(pages) -> int:
    errors = []
    for slug, (meta, out_html) in pages.items():
        c = Collector(); c.feed(out_html)
        if c.h1 != 1: errors.append(f"{slug}: {c.h1} <h1> tags")
        if len(meta["title"]) > 65: errors.append(f"{slug}: title {len(meta['title'])} chars")
        if not (70 <= len(meta["description"]) <= 160): errors.append(f"{slug}: description {len(meta['description'])} chars")
        for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out_html, re.S):
            try: json.loads(ld)
            except Exception as e: errors.append(f"{slug}: invalid JSON-LD ({e})")
        text = TAG_RE.sub(" ", out_html)
        for bad in FORBIDDEN:
            if bad in text: errors.append(f"{slug}: forbidden text '{bad}'")
        for href in c.links:
            if href.startswith(("http", "mailto:", "tel:")): continue
            target, _, frag = href.partition("#")
            if target and not (OUT / target).exists(): errors.append(f"{slug}: broken link {href}")
            if not target and frag and frag not in c.ids: errors.append(f"{slug}: missing anchor #{frag}")
        for tag, src, alt in c.imgs:
            if src.startswith("http"): continue
            if not (OUT / src).exists(): errors.append(f"{slug}: missing asset {src}")
            if tag == "img" and alt is None: errors.append(f"{slug}: <img> without alt ({src})")
            if alt and re.search(r"\bAI\b|AI-generated|concept|inspiration", alt, re.I): errors.append(f"{slug}: AI/concept label in alt text ({src})")
        if "{{" in out_html: errors.append(f"{slug}: unexpanded placeholder")
        if 'rel="canonical"' not in out_html: errors.append(f"{slug}: no canonical")
    for e in errors: print("  ✗", e)
    print(f"{'OK' if not errors else 'FAILED'}: {len(pages)} pages, {len(errors)} problems")
    return 1 if errors else 0

if __name__ == "__main__":
    pages = build()
    print(f"Built {len(pages)} pages → {OUT.relative_to(ROOT)}/ (+ sitemap.xml)")
    if "--check" in sys.argv:
        sys.exit(check(pages))
