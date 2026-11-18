"""Composite the real Blue Hammer mark (assets/blue-hammer-mark.png) as a one-colour shirt print
onto a generated hero photo. The model is asked for a plain shirt; the logo is never AI-drawn.
Usage: python3 tools/image/shirt_print.py RAW.png OUT.png --cx 1763 --cy 590 --width 270 [--rotate -3] [--skew 0.08]
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "blue_hammer_remodeling_site" / "assets"
INK = (238, 233, 222)  # warm off-white screen-print ink

def build_print(width: int) -> Image.Image:
    mark = Image.open(ASSETS / "blue-hammer-mark.png").convert("RGBA")
    a = mark.split()[3]
    mw = width; mh = round(mark.height * mw / mark.width)
    a = a.resize((mw, mh), Image.LANCZOS)
    big = ImageFont.truetype(str(ASSETS / "fonts" / "switzer-700.woff2"), round(width * 0.155))
    small = ImageFont.truetype(str(ASSETS / "fonts" / "switzer-600.woff2"), round(width * 0.068))
    def text_mask(txt, font, track):
        widths = [font.getbbox(c)[2] - font.getbbox(c)[0] if c != " " else font.size * 0.3 for c in txt]
        tw = int(sum(widths) + track * (len(txt) - 1)) + 4
        th = int(font.size * 1.25)
        m = Image.new("L", (tw, th), 0); d = ImageDraw.Draw(m); x = 0
        for c, w in zip(txt, widths):
            d.text((x - font.getbbox(c)[0] if c != " " else x, 0), c, font=font, fill=255); x += w + track
        return m.crop(m.getbbox())
    t1 = text_mask("BLUE HAMMER", big, width * 0.012)
    t2 = text_mask("REMODELING", small, width * 0.05)
    scale = min(1, width / t1.width); t1 = t1.resize((round(t1.width * scale), round(t1.height * scale)), Image.LANCZOS)
    gap = round(width * 0.06)
    H = mh + gap + t1.height + round(gap * 0.6) + t2.height
    m = Image.new("L", (width, H), 0)
    m.paste(a, (0, 0))
    m.paste(t1, ((width - t1.width) // 2, mh + gap))
    m.paste(t2, ((width - t2.width) // 2, mh + gap + t1.height + round(gap * 0.6)))
    return m

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("raw"); ap.add_argument("out")
    ap.add_argument("--cx", type=int, required=True); ap.add_argument("--cy", type=int, required=True)
    ap.add_argument("--width", type=int, default=260); ap.add_argument("--rotate", type=float, default=0)
    ap.add_argument("--skew", type=float, default=0.0); ap.add_argument("--opacity", type=float, default=0.86)
    a = ap.parse_args()
    base = Image.open(a.raw).convert("RGB")
    m = build_print(a.width * 2).resize((a.width, None or round(build_print(a.width * 2).height / 2)), Image.LANCZOS)
    if a.skew:
        m = m.transform((m.width, m.height), Image.AFFINE, (1, a.skew, -a.skew * m.height / 2, 0, 1, 0), Image.BICUBIC)
    if a.rotate:
        m = m.rotate(a.rotate, Image.BICUBIC, expand=True)
    m = m.filter(ImageFilter.GaussianBlur(0.6))
    x0 = a.cx - m.width // 2; y0 = a.cy - m.height // 2
    region = base.crop((x0, y0, x0 + m.width, y0 + m.height))
    # Follow the fabric: modulate the ink by the shirt's local shading (folds, light falloff).
    lum = ImageOps.grayscale(region).filter(ImageFilter.GaussianBlur(2))
    mean = sum(lum.getdata()) / (lum.width * lum.height) or 1
    shade = lum.point(lambda v: max(0, min(255, int(255 * min(1.25, max(0.55, v / mean)) / 1.25))))
    ink = Image.new("RGB", m.size, INK)
    ink = ImageChops.multiply(ink, Image.merge("RGB", [shade.point(lambda v: min(255, int(v * 1.25)))] * 3))
    alpha = m.point(lambda v: int(v * a.opacity))
    region.paste(ink, (0, 0), alpha)
    base.paste(region, (x0, y0))
    base.save(a.out)
    print("saved", a.out, base.size, "print box", (x0, y0, m.width, m.height))

if __name__ == "__main__":
    main()
