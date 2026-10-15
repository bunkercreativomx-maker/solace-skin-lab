"""Solace website imagery v2 — same visual system as the Oct-Nov social batch (GPT Image 2 on FAL, own FAL_KEY,
quality medium), but NO TEXT. Outputs to ./out/ as webp/jpg at the exact sizes the site uses.
Usage: python3 gen_site.py all | python3 gen_site.py hero botox
"""
import json, sys, time, subprocess, urllib.request, urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).parent; OUT = ROOT / "out"; RAW = ROOT / "raw"; OUT.mkdir(exist_ok=True); RAW.mkdir(exist_ok=True)
KEY = [l.split("=", 1)[1].strip().strip('"\'') for l in open("/opt/data/.env") if l.startswith("FAL_KEY=")][0]

MASTER = """Premium editorial photograph for the website of Solace Skin Lab, a high-end med spa in El Paso, Texas.
LOOK: documentary editorial beauty photography that looks like a REAL photo shot on a full-frame camera with a fast prime lens inside a luxury treatment room — moody low-key lighting, a warm focused overhead treatment lamp or candle-warm light pooling on the subject, deep espresso / near-black shadows, crisp white towels, caps and linens, warm skin tones, subtle champagne-gold accents (brass lamp, gold tray). Real people with natural skin texture, visible pores, freckles and fine lines, restrained retouching, believable gloved hands with correct anatomy (five fingers), calm expressions. Never plastic or airbrushed skin, never uncanny faces, never duplicated faces.
ABSOLUTELY NO TEXT: no words, letters, numbers, logos, watermarks, signage or labels anywhere; every bottle, jar, device and screen is plain and unlabeled (screens dark or not visible)."""

# key: (size requested, final WxH, output file, scene, extra)
L = (1600, 1200); FINAL_L = (1200, 900)
JOBS = {
 "hero": ((2560, 1440), (2560, 1440), "hero-spa-friends-wine-2026.webp",
   "Two best friends enjoying a facial day together, lying on two treatment beds side by side under warm lamp light, white headbands and towels, light cream masks, laughing toward each other; one Black woman in her early 30s with natural curls, one Latina woman in her late 20s with long dark wavy hair. A glass of red wine rests on a small brass side table between them.",
   "COMPOSITION FOR A WEBSITE HERO: the two women occupy the RIGHT 55% of the frame; the LEFT 45% is calm, dark, nearly empty negative space (deep shadow, soft blur) where the site will place its headline. Wide cinematic 16:9."),
 "hero-mobile": ((1440, 2560), (1440, 2560), "hero-spa-friends-wine-2026-mobile.webp",
   "Same concept: two best friends on side-by-side treatment beds, white headbands and towels, light cream masks, laughing toward each other; one Black woman in her early 30s with natural curls, one Latina woman in her late 20s with long dark wavy hair; a glass of red wine on a brass side table.",
   "COMPOSITION FOR A MOBILE HERO (vertical 9:16): the two women and their faces sit in the TOP 45% of the frame, shot from slightly above; the BOTTOM 55% falls off into calm dark shadow (dark towels/floor) with no important detail, where the site places its headline."),
 "clinic-01": ((1024, 1280), (896, 1088), "clinic-room-01.jpg",
   "Empty private treatment room, no people: a treatment bed dressed in crisp white linens and a folded towel, a brass overhead treatment lamp casting a warm pool of light, a small marble side table with a lit amber candle and a plain glass serum bottle, dark espresso walls, quiet and inviting.", "Vertical 4:5."),
 "clinic-02": ((1920, 1088), (1200, 675), "clinic-room-02.jpg",
   "Close detail of a treatment trolley: neatly rolled white towels in a brass bowl, a plain glass dropper bottle, a ceramic dish with cream, a lit candle, soft bokeh of the dark treatment room behind, warm lamp light.", "Wide 16:9."),
 "facials": (L, FINAL_L, "services/luxury-facial-landscape.webp",
   "Luxury facial: woman in her early 30s, light-medium olive skin, hair wrapped in a white towel, eyes closed, while gloved esthetician hands brush a creamy mask onto her cheek; warm overhead lamp, candles softly blurred.", ""),
 "facial": (L, FINAL_L, "services/facials-landscape.webp",
   "Classic facial: woman in her mid 30s with freckles and auburn hair in a white towel, eyes closed under a gentle facial steamer, soft mist in the light beam, esthetician's gloved hand resting at her temple.", ""),
 "microneedling": (L, FINAL_L, "services/microneedling-landscape.webp",
   "Microneedling: gloved hand holding a plain motorized microneedling pen with a clear sterile cartridge against the cheek of a man in his early 30s with light-medium skin, short dark hair and light stubble, eyes closed, skin glossy with serum, white disposable cap, other gloved hand gently stretching the skin; crisp focus on the cartridge.", ""),
 "botox": (L, FINAL_L, "services/botox-landscape.webp",
   "Injectable consultation: female injector in black scrubs and black gloves gently assessing the forehead of a seated woman in her early 40s with shoulder-length blonde hair, fingertip near the brow, client smiling calmly; no needle in frame.", ""),
 "lip-fillers": (L, FINAL_L, "services/lip-fillers-juvederm-landscape.webp",
   "Lip consultation: close-up of a woman in her early 30s, medium-brown skin, natural lips, while a gloved injector's fingertip softly touches near the corner of her mouth to assess balance; a closed plain treatment tray in soft focus; no needle in frame.", ""),
 "dermaplaning": (L, FINAL_L, "services/dermaplaning-landscape.webp",
   "Dermaplaning: gloved esthetician hand gliding a plain dermaplaning blade at a shallow angle along the smooth cheek of a woman in her late 20s, other hand stretching the skin, white headband, very fine peach fuzz visible in the light.", ""),
 "salmon-dna": (L, FINAL_L, "services/salmon-dna-landscape.webp",
   "Regenerative serum facial: glass dropper releasing a glistening drop of a soft rose-coral tinted serum onto the cheek of a woman in her 40s with natural fine lines, eyes closed, gloved hand at her jaw; a small plain glass ampoule on a gold tray in soft focus.", ""),
 "dpscan": (L, FINAL_L, "services/dpscan-landscape.webp",
   "Skin and scalp analysis: esthetician in black scrubs holding a small plain handheld skin-analysis magnifier camera (a compact cylindrical lens with a ring of tiny LEDs at the tip) lightly against the cheek of a seated woman in her 30s; the device screen is not visible; calm, clinical-luxury mood.", ""),
 "24k-neck": (L, FINAL_L, "services/24k-neck-decollete-landscape.webp",
   "Neck and décolleté treatment: woman in her late 40s reclining, towel folded low, a translucent gel mask with fine 24k gold flakes being brushed onto her neck and décolleté by gloved hands; warm golden light.", ""),
 "derma-jade": (L, FINAL_L, "services/derma-jade-landscape.webp",
   "Eye treatment: close-up of a woman in her mid 30s with eyes closed, translucent under-eye gel patches, a gloved hand gently gliding a cool polished green jade roller beside the eye area; delicate, soothing.", ""),
 "acne-men": (L, FINAL_L, "services/acne-scar-evaluation-men-landscape.webp",
   "Men's skin consultation: man in his early 30s with medium-brown skin, short beard and clearly visible mild rolling acne scars and uneven texture on his cheek (realistic, not exaggerated), seated, while an esthetician in black scrubs examines that cheek closely under a brass magnifying lamp, the light grazing the textured skin; respectful, calm, honest.", ""),
 "scalp-men": (L, FINAL_L, "services/scalp-care-men-landscape.webp",
   "Men's scalp care: man in his late 30s seated in a treatment chair with a white towel on his shoulders while a gloved specialist parts his short dark hair and applies a drop of clear serum to the scalp with a glass dropper; close, warm light.", ""),
}

def call(prompt, size):
    body = json.dumps({"prompt": prompt, "image_size": {"width": size[0], "height": size[1]}, "quality": "medium",
                       "num_images": 1, "output_format": "png"}).encode()
    r = urllib.request.Request("https://fal.run/openai/gpt-image-2", data=body, method="POST",
                               headers={"Authorization": f"Key {KEY}", "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(r, timeout=400).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read()[:300]}")

def run(name):
    size, final, fname, scene, extra = JOBS[name]
    prompt = "\n".join([MASTER, "", "SCENE: " + scene, extra, "Remember: absolutely no text or logos anywhere."])
    for attempt in range(3):
        try:
            url = call(prompt, size)["images"][0]["url"]
            raw = RAW / f"{name}.png"; urllib.request.urlretrieve(url, raw)
            out = OUT / fname; out.parent.mkdir(parents=True, exist_ok=True)
            vf = f"scale={final[0]}:{final[1]}:force_original_aspect_ratio=increase:flags=lanczos,crop={final[0]}:{final[1]}"
            args = ["-quality", "82"] if fname.endswith(".webp") else ["-q:v", "3"]
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", vf, *args, "-frames:v", "1", str(out)], check=True)
            print(f"{name} OK -> {fname} {final} ({out.stat().st_size//1024} KB)", flush=True); return True
        except Exception as e:
            print(f"{name} attempt {attempt+1}: {e}", flush=True); time.sleep(6)
    return False

if __name__ == "__main__":
    a = sys.argv[1:]; names = list(JOBS) if a == ["all"] else a
    with ThreadPoolExecutor(5) as ex: res = list(ex.map(run, names))
    print(f"RESUMEN {sum(res)}/{len(names)}")
