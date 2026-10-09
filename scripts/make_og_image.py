#!/usr/bin/env python3
"""Generate the default 1200x630 Open Graph image (docs/og-image.png).

Usage: python3 scripts/make_og_image.py   (requires Pillow)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG, CORAL, WHITE, INK = "#ebe9e1", "#f76c6c", "#ffffff", "#24395e"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 400], fill=CORAL)

def centered(text, y, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)

centered("Weekend Code Adventures", 145, ImageFont.truetype(SERIF_BOLD, 76), WHITE)
centered("by Francesco Barbera", 255, ImageFont.truetype(SERIF, 40), WHITE)
centered("weekendcodeadventures.xyz", 485, ImageFont.truetype(SERIF, 36), INK)

out = Path(__file__).resolve().parent.parent / "docs" / "og-image.png"
img.save(out, optimize=True)
print(f"wrote {out}")
