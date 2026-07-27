#!/usr/bin/env python3
"""Composite an elegant on-brand $64.99 price badge onto selected Solace August V2 creatives.

Days: 5, 12, 19, 26 (Tuesday 2x1 promo) + 28 (Facial + LED).
Badge:
  $64.99            (rose #a76550, bold serif)
  [ Luxury skincare · FREE facial ]   (terracotta pill, white text -> high contrast)
Bottom-left, never overlapping phone/CTA. Ivory card + soft shadow.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "images", "august-2026-v2")
DAYS = [5, 12, 19, 26, 28]

IVORY = (248, 243, 237, 240)
CARD_LINE = (214, 200, 188, 255)
ROSE = (167, 101, 80, 255)
TERRA = (167, 101, 80, 255)      # pill fill
WHITE = (255, 255, 255, 255)
INK = (52, 46, 42, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def fit(draw, text, fnt, max_w):
    while draw.textlength(text, font=fnt) > max_w and fnt.size > 8:
        fnt = ImageFont.truetype(fnt.path, fnt.size - 1)
    return fnt


def add_badge(src):
    im = Image.open(src).convert("RGBA")
    W, H = im.size
    draw = ImageDraw.Draw(im, "RGBA")

    pad = int(W * 0.035)
    card_w = int(W * 0.42)
    card_h = int(H * 0.155)
    x0 = pad
    y0 = H - card_h - pad
    x1 = x0 + card_w
    y1 = y0 + card_h

    # shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([x0 + 6, y0 + 10, x1 + 6, y1 + 10], radius=20, fill=(60, 40, 30, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    im.alpha_composite(shadow)

    # ivory card
    draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=IVORY, outline=CARD_LINE, width=2)

    inner = int(card_w * 0.08)
    cx = x0 + inner
    price_f = fit(draw, "$64.99", ImageFont.truetype(SERIF_B, int(card_h * 0.42)), card_w - 2 * inner)
    price_y = y0 + int(card_h * 0.14)
    draw.text((cx, price_y), "$64.99", font=price_f, fill=ROSE)

    # terracotta pill with white sub-text (high contrast, on-brand)
    sub = "Luxury skincare · FREE facial"
    sub_f = fit(draw, sub, ImageFont.truetype(SERIF_B, int(card_h * 0.20)), card_w - 2 * inner)
    sub_bbox = draw.textbbox((0, 0), sub, font=sub_f)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_h = sub_bbox[3] - sub_bbox[1]
    pill_pad_x = int(sub_w * 0.10)
    pill_h = sub_h + int(sub_h * 0.7)
    pill_y = y1 - int(card_h * 0.18) - pill_h
    pill_x0 = cx
    pill_x1 = cx + sub_w + 2 * pill_pad_x
    draw.rounded_rectangle([pill_x0, pill_y, pill_x1, pill_y + pill_h], radius=pill_h // 2, fill=TERRA)
    draw.text((pill_x0 + pill_pad_x, pill_y + (pill_h - sub_h) // 2), sub, font=sub_f, fill=WHITE)

    im.convert("RGB").save(src, "PNG")
    print(f"updated {os.path.basename(src)} ({W}x{H})")


def main():
    for d in DAYS:
        add_badge(os.path.join(IMG_DIR, f"day{str(d).zfill(2)}.png"))
    print("done")


if __name__ == "__main__":
    main()
