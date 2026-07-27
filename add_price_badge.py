#!/usr/bin/env python3
"""Composite an elegant on-brand $64.99 price badge onto selected Solace August V2 creatives.

Target days: 5, 12, 19, 26 (Tuesday 2x1 promo) + 28 (Facial + LED).
Badge text:
  $64.99
  Luxury skincare · FREE facial
Placed bottom-left, ivory translucent card, rose (#a76550) accent rule, serif type.
Does NOT cover faces or top text. Preserves original pixels elsewhere.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "images", "august-2026-v2")
DAYS = [5, 12, 19, 26, 28]

# Brand palette
IVORY = (248, 243, 237, 242)       # card fill, slightly translucent
CARD_LINE = (230, 221, 213, 255)   # hairline border
ROSE = (167, 101, 80, 255)         # #a76550 text accent
INK = (52, 46, 42, 255)            # #342e2a dark text
MUTED = (117, 109, 103, 255)       # #756d67 sub text

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, fnt, max_w):
    # shrink to fit width
    while draw.textlength(text, font=fnt) > max_w and fnt.size > 8:
        fnt = ImageFont.truetype(fnt.path, fnt.size - 1)
    return fnt


def add_badge(src_path, dst_path):
    im = Image.open(src_path).convert("RGBA")
    W, H = im.size
    draw = ImageDraw.Draw(im, "RGBA")

    # Badge sizing relative to image
    pad = int(W * 0.035)
    card_w = int(W * 0.46)
    card_h = int(H * 0.135)
    x0 = pad
    y0 = H - card_h - pad
    x1 = x0 + card_w
    y1 = y0 + card_h

    # Soft shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([x0 + 6, y0 + 8, x1 + 6, y1 + 8], radius=18, fill=(60, 40, 30, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    im.alpha_composite(shadow)

    # Card
    draw.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=IVORY, outline=CARD_LINE, width=2)

    # Layout inside card
    inner_pad = int(card_w * 0.07)
    cx = x0 + inner_pad
    price_sz = int(card_h * 0.40)
    sub_sz = int(card_h * 0.20)
    price_f = fit(draw, "$64.99", font(SERIF_B, price_sz), card_w - 2 * inner_pad)
    sub_f = fit(draw, "Luxury skincare · FREE facial", font(SERIF, sub_sz), card_w - 2 * inner_pad)

    # accent rule between price and sub
    price_y = y0 + int(card_h * 0.16)
    draw.text((cx, price_y), "$64.99", font=price_f, fill=ROSE)
    pb = draw.textbbox((cx, price_y), "$64.99", font=price_f)
    sub_y = pb[3] + int(card_h * 0.06)
    # small rose rule
    rule_y = sub_y - int(card_h * 0.04)
    draw.line([(cx, rule_y), (cx + int(card_w * 0.30), rule_y)], fill=ROSE, width=2)
    draw.text((cx, sub_y), "Luxury skincare · FREE facial", font=sub_f, fill=MUTED)

    im.convert("RGB").save(dst_path, "PNG")
    print(f"wrote {os.path.basename(dst_path)} ({W}x{H})")


def main():
    for d in DAYS:
        name = f"day{str(d).zfill(2)}.png"
        src = os.path.join(IMG_DIR, name)
        add_badge(src, src)  # overwrite in place
    print("done")


if __name__ == "__main__":
    main()
