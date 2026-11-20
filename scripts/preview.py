#!/usr/bin/env python3
"""Local preview that resolves URLs the way Netlify does: /name -> name.html, / -> index.html.

The site's canonical URLs and internal links are extensionless (see scripts/build.py), which a plain
`python3 -m http.server` cannot follow. Usage:  python3 scripts/preview.py [port]   (default 8765)
"""
import http.server, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "blue_hammer_remodeling_site"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)
    def translate_path(self, path):
        local = pathlib.Path(super().translate_path(path))
        if not local.exists() and not local.suffix and local.with_suffix(".html").exists():
            return str(local.with_suffix(".html"))
        return str(local)
    def send_error(self, code, message=None, explain=None):
        if code == 404 and (ROOT / "404.html").exists():
            body = (ROOT / "404.html").read_bytes()
            self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers()
            if self.command != "HEAD": self.wfile.write(body)
            return
        super().send_error(code, message, explain)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"Blue Hammer preview: http://127.0.0.1:{port}/")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
