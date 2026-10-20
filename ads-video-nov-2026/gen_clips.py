"""Kling 2.5 Turbo Pro image-to-video hook clips (5 s, 9:16) for the Solace ads.
usage: python3 gen_clips.py a4 b1 ..."""
import json, sys, time, base64, subprocess, urllib.request, urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT = Path(__file__).parent; OUT = ROOT / "clips"; OUT.mkdir(exist_ok=True)
KEY = [l.split("=", 1)[1].strip().strip('"\'') for l in open("/opt/data/.env") if l.startswith("FAL_KEY=")][0]
EP = "fal-ai/kling-video/v2.5-turbo/pro/image-to-video"
BASE = " Cinematic, realistic, subtle natural motion, slow gentle camera push-in, warm moody spa lighting, no text, no new objects, faces stay consistent."
P = {
 "a4": "The two friends laugh together and gently clink their wine glasses, then smile at each other.",
 "b1": "The esthetician's gloved hand slowly brushes the creamy mask across the woman's cheek; she breathes calmly with eyes closed.",
 "c1": "The gloved hand glides the microneedling pen slowly across the man's cheek; he stays relaxed with eyes closed.",
 "d2": "The woman turns slightly toward the camera and her smile grows naturally, golden bokeh lights twinkle softly behind her.",
 "e1": "The woman looks at her phone, smiles, then glances up as if she just decided something; candle flames flicker softly.",
 "a2": "Very slow orbiting camera move around the jar and bottle, candle flame flickering, light glinting on the glass.",
}
def req(url, data=None, method="GET"):
    r = urllib.request.Request(url, data=data, method=method, headers={"Authorization": f"Key {KEY}", "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r, timeout=120).read())
def run(name):
    out = OUT / f"{name}.mp4"
    if out.exists(): return f"{name} exists"
    jpg = ROOT / f"stills/{name}_k.jpg"
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", str(ROOT / f"stills/{name}.png"), "-q:v", "3", str(jpg)], check=True)
    uri = "data:image/jpeg;base64," + base64.b64encode(jpg.read_bytes()).decode()
    body = json.dumps({"prompt": P[name] + BASE, "image_url": uri, "duration": "5", "negative_prompt": "blur, distort, low quality, text, watermark, extra fingers, morphing face", "cfg_scale": 0.5}).encode()
    sub = req(f"https://queue.fal.run/{EP}", body, "POST")
    for _ in range(120):
        time.sleep(10)
        st = req(sub["status_url"])
        if st.get("status") == "COMPLETED": break
    res = req(sub["response_url"])
    urllib.request.urlretrieve(res["video"]["url"], out)
    return f"{name} OK"
if __name__ == "__main__":
    with ThreadPoolExecutor(5) as ex:
        for r in ex.map(lambda n: (lambda: run(n))() if True else None, sys.argv[1:]): print(r, flush=True)
