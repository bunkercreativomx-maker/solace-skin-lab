"""Typography pilot: 2 richer type styles x 2 posts (day01, day05) -> pilot/ . Reuses gen.py scene data."""
import sys, json, subprocess, shutil, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import gen

BASE = gen.MASTER.split("TYPOGRAPHY")[0]
RULES = """TEXT RULE: render ONLY the exact wording listed below, spelled exactly. Do NOT invent logos, emblems, monograms, watermarks, URLs, phone numbers, hashtags or any other words. Products and devices are plain and unlabeled. The brand appears ONLY as the plain words "Solace Skin Lab"."""

STYLES = {
 "A": """TYPOGRAPHY — EDITORIAL MAGAZINE COVER (designed by a luxury beauty magazine art director, NOT a plain caption):
- The main headline is HUGE, in a high-contrast Didone serif (Vogue / Harper's Bazaar style), ivory, spanning most of the width; the key word of the headline is set in a flowing elegant handwritten script in warm champagne gold, overlapping the serif line for a layered, designed lockup.
- DEPTH EFFECT: part of the giant headline sits BEHIND the subject (the person's head or shoulder overlaps some letters), like a real magazine cover.
- Supporting line in small, widely letter-spaced uppercase sans-serif (tracking +300), with a thin champagne-gold hairline rule above it.
- Price set as a refined typographic element: tiny tracked caps label above a large elegant serif number in champagne gold.
- Brand "Solace Skin Lab" small, tracked caps, centered at the bottom. Strong hierarchy, intentional negative space, everything inside safe margins. No boxes, banners, stickers, splashes, glow or 3D type.""",
 "B": """TYPOGRAPHY — LUXURY PROMO POSTER (premium, bold, scroll-stopping, NOT a plain caption):
- Headline in a confident bold modern serif mixed with a refined script accent word in champagne gold; large, 2-3 stacked lines with tight leading, aligned left in the calm dark area of the photo.
- The PRICE is the hero graphic: very large elegant numerals in champagne-gold foil look (subtle metallic texture, not glowing), with a small tracked-caps label next to it.
- A slim translucent smoked-glass vertical panel or thin gold frame line partially behind the text block to anchor it (elegant, minimal), plus one thin gold hairline divider.
- Supporting line in small tracked uppercase sans-serif.
- Brand "Solace Skin Lab" small, tracked caps at the bottom. Polished like a high-end med-spa ad campaign. No stickers, starbursts, splashes, glow, clip-art or 3D letters.""",
}

COPY = {
 1: [('HEADLINE: "Welcome to Solace" (script accent word: "Solace")'),
     ('SUPPORTING LINE: "WHERE BEAUTY MEETS CONFIDENCE"'),
     ('PRICE LABEL: "FACIALS STARTING AT"  PRICE: "$64.99"')],
 5: [('HEADLINE: "2 Facials" (script accent: "for two")  — render exactly the words "2 Facials" and "for two"'),
     ('SUPPORTING LINE: "TUESDAYS ONLY · BRING YOUR BESTIE"'),
     ('PRICE LABEL: "BOTH FOR"  PRICE: "$64.99"')],
}

def prompt(day, st):
    p = gen.posts[day]
    crit = ["CRITICAL: the price is SIXTY-FOUR dollars and ninety-nine cents, rendered exactly '$64.99'."]
    if day == 5:
        crit.append("CRITICAL: the two women MUST be two clearly DIFFERENT people — different faces, hair, skin tone. Never twins or a duplicated face.")
    return "\n".join([BASE, STYLES[st], RULES, "", "SCENE: " + p["imageScene"], "", "EXACT TEXT IN IMAGE:", *COPY[day],
                      'BRAND: "Solace Skin Lab"', *crit, "No other text anywhere in the image."])

def run(job):
    day, st = job; out = Path(gen.ROOT / "pilot"); out.mkdir(exist_ok=True)
    f = out / f"day{day:02d}_{st}.png"
    res = gen.call(prompt(day, st)); raw = str(f) + ".raw.png"
    urllib.request.urlretrieve(res["images"][0]["url"], raw)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-vf", "scale=1080:1080:flags=lanczos", "-frames:v", "1", str(f)], check=True)
    Path(raw).unlink(); print("OK", f, flush=True)

if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex: list(ex.map(run, [(1, "A"), (1, "B"), (5, "A"), (5, "B")]))
