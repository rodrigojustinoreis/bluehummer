#!/usr/bin/env python3
"""Generate a photorealistic image with OpenAI's Images API (gpt-image-1).
Usage: python3 scripts/gen-image.py "prompt" out_name [--size 1536x1024] [--quality high]
Writes blue_hammer_remodeling_site/assets/<out_name>-1440.webp and -720.webp (needs Pillow; falls back to PNG).
Key: OPENAI_API_KEY env var, or macOS Keychain item 'OPENAI_API_KEY' (security add-generic-password -a "$USER" -s OPENAI_API_KEY -w 'sk-...').
"""
import os, sys, json, base64, subprocess, argparse, urllib.request, pathlib
ap = argparse.ArgumentParser(); ap.add_argument("prompt"); ap.add_argument("name")
ap.add_argument("--size", default="1536x1024"); ap.add_argument("--quality", default="high")
ap.add_argument("--model", default=os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1"))
a = ap.parse_args()
key = os.environ.get("OPENAI_API_KEY") or subprocess.run(["security","find-generic-password","-s","OPENAI_API_KEY","-w"],capture_output=True,text=True).stdout.strip()
if not key: sys.exit("No OPENAI_API_KEY found (env or Keychain).")
req = urllib.request.Request("https://api.openai.com/v1/images/generations",
    data=json.dumps({"model":a.model,"prompt":a.prompt,"size":a.size,"quality":a.quality,"n":1}).encode(),
    headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
data = json.load(urllib.request.urlopen(req, timeout=300))["data"][0]
raw = base64.b64decode(data["b64_json"]) if "b64_json" in data else urllib.request.urlopen(data["url"]).read()
out = pathlib.Path(__file__).resolve().parent.parent / "blue_hammer_remodeling_site" / "assets"
png = out / f"{a.name}.png"; png.write_bytes(raw)
try:
    from PIL import Image
    im = Image.open(png).convert("RGB")
    for w in (1440, 720):
        h = round(im.height * w / im.width); im.resize((w, h), Image.LANCZOS).save(out / f"{a.name}-{w}.webp", "WEBP", quality=80)
    png.unlink(); print(f"Saved {a.name}-1440.webp and {a.name}-720.webp in {out}")
except ImportError:
    print(f"Saved {png} (install Pillow for WebP: pip3 install pillow)")
