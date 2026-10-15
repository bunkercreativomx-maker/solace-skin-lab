"""Generate Solace Oct16–Nov14 creatives with GPT Image 2 on FAL (own FAL_KEY, fal.run/openai/gpt-image-2, quality medium).
Usage: python3 gen.py 1 5   |  python3 gen.py all   (skips existing)  |  python3 gen.py --force 3
"""
import json, sys, time, subprocess, shutil, urllib.request, urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path("/opt/data/solace-skin-lab/oct-nov-2026")
OUT = ROOT / "images"; OUT.mkdir(exist_ok=True)
LOG = ROOT / "gen_log.jsonl"
KEY = [l.split("=", 1)[1].strip().strip('"\'') for l in open("/opt/data/.env") if l.startswith("FAL_KEY=")][0]
posts = {p["day"]: p for p in json.load(open(ROOT / "calendar_2026-10-16_to_2026-11-14.json")) if not p.get("needsMaterial")}

MASTER = """Square 1:1 Facebook feed post for Solace Skin Lab, a premium med spa in El Paso, Texas.
LOOK (inspired by top med-spa Pinterest content): documentary, editorial beauty photography that looks like a REAL photo taken inside a high-end treatment room — moody low-key lighting, a warm focused overhead treatment lamp or candle-warm light pooling on the subject, deep espresso / near-black shadows, crisp whites (towels, caps, linens), warm skin tones, subtle champagne-gold accents. Real people with natural skin texture, visible pores, freckles and fine lines, restrained retouching, believable gloved hands and anatomy. Photography fills the whole frame (full-bleed). Never plastic or airbrushed skin, never uncanny faces, never duplicated or twin faces.
TYPOGRAPHY (rendered natively, minimal like Pinterest med-spa posts): ONE short headline in an elegant high-contrast serif (Playfair/Cormorant style), white or soft ivory, title case, placed over a calm dark area of the photo with a very faint shadow for legibility; optional small refined sans-serif secondary line under it; tiny plain-text brand line. Generous margins, nothing near the edges, nothing cropped. No boxes, banners, badges, stickers, splashes, glow, 3D type, sparkles or clip-art.
TEXT RULE: render ONLY the exact wording listed below, spelled exactly. Do NOT invent logos, emblems, monograms, watermarks, URLs, phone numbers, hashtags or any other words. Products and devices are plain and unlabeled. The brand appears ONLY as the plain words "Solace Skin Lab" in small elegant serif."""

def prompt_for(p):
    lines = [f'HEADLINE: "{p["imageTitle"]}"']
    if p["imageSub"]:
        lines.append(f'SECONDARY LINE (smaller): "{p["imageSub"]}"')
    lines.append('TINY BRAND LINE near the bottom: "Solace Skin Lab"')
    crit = []
    if "$64.99" in p["imageTitle"] + p["imageSub"]:
        crit.append("CRITICAL: the price is SIXTY-FOUR dollars and ninety-nine cents, rendered exactly '$64.99' (dollar sign, 6, 4, decimal point, 9, 9).")
    if "2 Facials" in p["imageTitle"]:
        crit.append("CRITICAL: the headline reads exactly '2 Facials for $64.99' — the price is for BOTH facials together.")
        crit.append("CRITICAL: the two people MUST be two clearly DIFFERENT individuals — different facial features, hair, skin tone and age. Never twins, never the same face duplicated or mirrored.")
    if "®" in p["imageTitle"]:
        crit.append("Render the registered mark ® small and raised right after BOTOX.")
    if "≠" in p["imageTitle"]:
        crit.append("Render the not-equal sign ≠ correctly.")
    return "\n".join([MASTER, "", "SCENE: " + p["imageScene"], "", "EXACT TEXT IN IMAGE:", *lines, *crit,
                      "No other text anywhere in the image."])

def call(prompt):
    body = json.dumps({"prompt": prompt, "image_size": "square_hd", "quality": "medium",
                       "num_images": 1, "output_format": "png"}).encode()
    r = urllib.request.Request("https://fal.run/openai/gpt-image-2", data=body, method="POST",
                               headers={"Authorization": f"Key {KEY}", "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(r, timeout=300).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read()[:400]}")

def gen(day):
    p = posts[day]; out = OUT / f"day{day:02d}.png"
    for attempt in range(3):
        try:
            res = call(prompt_for(p)); url = res["images"][0]["url"]
            raw = OUT / f"day{day:02d}.raw.png"
            urllib.request.urlretrieve(url, raw)
            tmp = str(out) + ".tmp.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf",
                            "scale=1080:1080:flags=lanczos", "-frames:v", "1", tmp], check=True)
            shutil.move(tmp, out); raw.unlink()
            b = open(out, "rb").read(24)
            dims = (int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big"))
            with open(LOG, "a") as f:
                f.write(json.dumps({"day": day, "model": "openai/gpt-image-2", "provider": "fal.run (own FAL_KEY)",
                                    "quality": "medium", "src": url, "dims": dims, "ts": time.time()}) + "\n")
            print(f"day{day:02d} OK {dims}", flush=True); return True
        except Exception as e:
            print(f"day{day:02d} attempt {attempt+1} failed: {e}", flush=True); time.sleep(6)
    return False

if __name__ == "__main__":
    a = sys.argv[1:]; force = "--force" in a; a = [x for x in a if x != "--force"]
    days = sorted(posts) if a == ["all"] else [int(x) for x in a]
    if not force:
        days = [d for d in days if not (OUT / f"day{d:02d}.png").exists()] if a == ["all"] else days
    with ThreadPoolExecutor(5) as ex:
        res = list(ex.map(gen, days))
    print(f"RESUMEN: {sum(res)}/{len(days)}")
