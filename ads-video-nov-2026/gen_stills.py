"""Solace Meta video ads Nov 2026 — vertical 9:16 stills (GPT Image 2 on FAL, quality medium, NO text).
Composition rule: subject/faces in the CENTRAL band (28%-62% of height) so 9:16 safe zones and a 4:5 center crop both work.
usage: python3 gen_stills.py all | python3 gen_stills.py a2 b3
"""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).parent; OUT = ROOT / "stills"; OUT.mkdir(exist_ok=True)
KEY = [l.split("=", 1)[1].strip().strip('"\'') for l in open("/opt/data/.env") if l.startswith("FAL_KEY=")][0]
SIZE = (1024, 1824)

MASTER = """Premium vertical 9:16 photograph for a paid social ad of Solace Skin Lab, a high-end med spa in El Paso, Texas.
LOOK: documentary editorial beauty photography that looks like a REAL photo shot on a full-frame camera with a fast prime lens inside a luxury treatment room — moody low-key lighting, warm focused lamp or candle-warm light pooling on the subject, deep espresso / near-black shadows, crisp white towels and linens, warm skin tones, subtle champagne-gold accents (brass, gold tray). Real people with natural skin texture and visible pores, restrained retouching, believable hands with correct anatomy (five fingers), never plastic or airbrushed skin, never uncanny or duplicated faces.
COMPOSITION: the subject and any faces sit in the CENTRAL band of the frame (between 28% and 62% of the height, horizontally centered); the top 22% and bottom 30% are calm, darker, low-detail areas (soft shadow, blurred background, towels) because ad text will sit there.
ABSOLUTELY NO TEXT: no words, letters, numbers, logos, watermarks, signage or labels anywhere; every bottle, jar, device and screen is plain and unlabeled."""

JOBS = {
 # META-01 / 05 Tuesday
 "a2": "Hero product shot, no people: a single elegant unlabeled frosted-glass skincare jar with a brushed gold lid and a matching slim unlabeled glass serum bottle with gold dropper, standing on a small round gold tray on dark marble, a white folded towel and a lit amber candle softly blurred behind, warm rim light glinting on the glass, luxurious and desirable.",
 "a3": "Close-up of two hands clinking two glasses of red wine in a dim luxury spa lounge, both women wearing plush white spa robes (only hands, wrists and robe sleeves visible), warm candlelight bokeh behind, the clink happening at the center of the frame.",
 "a4": "Two friends in white spa robes and white headbands sitting side by side on a velvet lounge bench after their facials, glowing skin, laughing together, each holding a glass of red wine; one Latina woman in her late 20s with long dark hair, one woman in her early 30s with light-brown skin and curly hair. Faces centered in the frame.",
 # META-02 any day
 "b1": "Luxury facial: woman in her early 30s, light-medium olive skin, hair wrapped in a white towel, eyes closed and serene, while gloved esthetician hands gently brush a creamy mask onto her cheek with a soft fan brush; overhead warm lamp light on her face; face centered in the frame, shot from above at a slight angle.",
 "b3": "Beauty portrait after a facial: a Latina woman in her mid 30s with dewy, healthy-looking glowing skin, hair pulled back, in a white spa robe, softly touching her cheek with her fingertips and smiling with closed lips, warm golden lamp light, dark background, face centered in the frame.",
 # META-03 microneedling
 "c1": "Microneedling close-up: gloved hand holding a plain unlabeled motorized microneedling pen with a clear sterile cartridge against the cheek of a man in his early 30s with light-medium skin, short dark hair and light stubble, eyes closed, skin glossy with serum, white disposable cap; crisp focus on the cartridge, the face centered in the frame.",
 "c2": "Microneedling on a woman: woman in her late 30s with medium skin and natural texture, eyes closed, white headband, gloved hand gliding a plain unlabeled microneedling pen along her forehead, skin glossy with clear serum, warm lamp light, face centered in the frame.",
 "c3": "Extreme close-up of healthy-looking smooth skin on a cheek catching warm golden light, a single glistening drop of clear serum, fine natural pores still visible, soft focus falloff; abstract, premium skincare macro, centered.",
 # META-04 injectables consultation (no needle, no syringe, no brand)
 "d1": "Injectable consultation: female injector in black scrubs and black gloves gently assessing the forehead of a seated woman in her early 40s with shoulder-length blonde hair, the injector's fingertip near the brow, the client smiling calmly; absolutely no needle or syringe in frame; both faces in the central band.",
 "d2": "Portrait of a confident woman in her mid 40s with natural fine lines, warm brown skin and short elegant hair, wearing a black satin top, smiling naturally, soft warm golden holiday bokeh lights in the dark background, refined and fresh-looking, face centered in the frame.",
 "d3": "Calm consultation: a woman in her late 30s sitting across a small marble table from a female provider in black scrubs who is listening and gesturing gently, a closed leather folder and a glass of water on the table, warm lamp light, both faces in the central band of the frame.",
 # META-05 retargeting
 "e1": "Woman in her early 30s in a white robe relaxing at home on a cream sofa in warm evening lamp light, looking at her phone with a soft smile (screen faces away and is not visible), cozy and aspirational, face centered in the frame.",
}

def call(prompt):
    body = json.dumps({"prompt": prompt, "image_size": {"width": SIZE[0], "height": SIZE[1]}, "quality": "medium",
                       "num_images": 1, "output_format": "png"}).encode()
    r = urllib.request.Request("https://fal.run/openai/gpt-image-2", data=body, method="POST",
                               headers={"Authorization": f"Key {KEY}", "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(r, timeout=400).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read()[:300]}")

def run(name):
    out = OUT / f"{name}.png"
    if out.exists(): print(name, "exists"); return True
    prompt = "\n".join([MASTER, "", "SCENE: " + JOBS[name], "Remember: absolutely no text or logos anywhere."])
    for attempt in range(2):
        try:
            url = call(prompt)["images"][0]["url"]
            urllib.request.urlretrieve(url, out); print(name, "OK", flush=True); return True
        except Exception as e:
            print(name, f"attempt {attempt+1}: {e}", flush=True); time.sleep(5)
    return False

if __name__ == "__main__":
    names = list(JOBS) if sys.argv[1:] == ["all"] else sys.argv[1:]
    with ThreadPoolExecutor(4) as ex: print(list(ex.map(run, names)))
