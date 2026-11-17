"""After you own/verify your business domain: python configure-domain.py https://yourdomain.com"""
from pathlib import Path
from urllib.parse import urlsplit
import sys, re, html
if len(sys.argv)!=2:
 raise SystemExit('Usage: python configure-domain.py https://your-verified-domain.com')
url=sys.argv[1].strip().rstrip('/')
parsed=urlsplit(url)
if parsed.scheme!='https' or not parsed.netloc or parsed.username or parsed.query or parsed.fragment or parsed.path:
 raise SystemExit('Use an HTTPS domain only, for example https://yourdomain.com')
root=Path(__file__).resolve().parent
pages=sorted(p for p in root.glob('*.html') if p.name!='thank-you.html')
for page in pages:
 s=page.read_text()
 path='/' if page.name=='index.html' else '/'+page.name
 canonical=url+path
 s=re.sub(r'<link rel="canonical"[^>]*>','',s)
 s=re.sub(r'<meta property="og:url"[^>]*>','',s)
 s=re.sub(r'<meta property="og:image"[^>]*>','',s)
 tag=f'<link rel="canonical" href="{html.escape(canonical,quote=True)}"><meta property="og:url" content="{html.escape(canonical,quote=True)}"><meta property="og:image" content="{html.escape(url+"/assets/blue-hammer-mark.png",quote=True)}">'
 s=s.replace('</head>',tag+'</head>')
 page.write_text(s)
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in pages:
 loc=url+('/' if p.name=='index.html' else '/'+p.name)
 xml+=f'  <url><loc>{html.escape(loc)}</loc></url>\n'
xml+='</urlset>\n'
(root/'sitemap.xml').write_text(xml)
(root/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {url}/sitemap.xml\n')
print(f'Configured {len(pages)} pages for {url}. Confirm the domain belongs to you before publishing.')
