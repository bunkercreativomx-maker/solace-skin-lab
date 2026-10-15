"""v2 batch: designed typography (B = luxury promo poster for price posts, A = editorial magazine for the rest).
Usage: python3 gen_v2.py all | python3 gen_v2.py 3 7
"""
import sys, json, time, subprocess, shutil, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import gen, pilot_type as pt

ROOT = gen.ROOT; OUT = ROOT / "images"
# day: (style, headline, script accent, supporting line, price label, price)
C = {
 2: ("B", "Your skin deserves", "a little love", "PROFESSIONAL FACIAL · DEEP CLEANSE · GLOW", "FACIAL", "$64.99"),
 3: ("A", "Sunday", "reset", "HYDRATE · SKINCARE · REST", None, None),
 4: ("A", "Microneedling", "next level", "SMOOTHER-LOOKING TEXTURE STARTS HERE", None, None),
 6: ("B", "When was your", "last facial?", "TAKE AN HOUR FOR YOURSELF", "PROFESSIONAL FACIAL", "$64.99"),
 7: ("A", "More products ≠", "better skin", "KNOW WHAT YOUR SKIN ACTUALLY NEEDS", None, None),
 8: ("B", "An hour", "just for you", "NO WORK · NO STRESS · JUST YOU", "FACIAL", "$64.99"),
 9: ("A", "Be honest", "just one thing", "TEXTURE · LINES · SPOTS · SCARS · PORES", None, None),
 10: ("A", "Let's talk BOTOX®", "still you", "A REFRESHED LOOK — STILL LOOKING LIKE YOURSELF", None, None),
 11: ("A", "Okay…", "be honest", "HOW MANY PRODUCTS ARE IN YOUR ROUTINE?", None, None),
 12: ("B", "2 Facials", "for two", "TUESDAYS ONLY · BRING YOUR MOM", "BOTH FOR", "$64.99"),
 13: ("B", "Your skin", "called", "IT WANTS A FACIAL", "ONLY", "$64.99"),
 14: ("A", "Perfect skin isn't the goal.", "Confidence is.", "THAT'S SOLACE", None, None),
 15: ("B", "This is", "your sign", "STOP PUTTING IT OFF", "FACIAL", "$64.99"),
 16: ("A", "Happy", "Halloween", "DON'T SLEEP IN YOUR MAKEUP", None, None),
 17: ("A", "Why does everyone talk about", "microneedling?", "DISCOVER IT AT SOLACE", None, None),
 18: ("B", "Plans", "this week?", "WE'VE GOT A BETTER ONE", "FACIAL", "$64.99"),
 19: ("B", "2 Facials", "for two", "TUESDAYS ONLY · BRING YOUR SISTER", "BOTH FOR", "$64.99"),
 20: ("B", "Tag someone who", "needs a facial", "BESTIE · MOM · SISTER · BOYFRIEND", "FACIALS", "$64.99"),
 21: ("A", "The Solace", "experience", "WE LISTEN · WE PLAN WITH YOU", None, None),
 22: ("A", "This", "or that?", "MORNING SKINCARE OR NIGHT SKINCARE?", None, None),
 23: ("B", "Weekend glow", "activated", "FACIAL · SKINCARE · CONFIDENCE", "FACIAL", "$64.99"),
 24: ("A", "Sunday", "self-care", "REST · UNPLUG · GLOW", None, None),
 25: ("A", "How many units", "do I need?", "YOUR INJECTOR EVALUATES YOU", None, None),
 26: ("B", "2 Facials", "for two", "TUESDAYS ONLY · BRING YOUR PARTNER", "BOTH FOR", "$64.99"),
 27: ("A", "POV:", "you work at Solace", "SKINCARE-ADDICTED SINCE DAY ONE", None, None),
 28: ("A", "30 days from now will come", "either way", "OR YOU CAN SIMPLY START", None, None),
 29: ("A", "El Paso,", "thank you", "WE'RE JUST GETTING STARTED", None, None),
 30: ("B", "Stop thinking about it.", "Start.", "FACIALS · MICRONEEDLING · BOTOX® · SKINCARE", "FACIALS", "$64.99"),
}

EXTRA = {
 2: "CRITICAL SPELLING: the script reads 'a little love' — l-i-t-t-l-e, exactly TWO letter t.",
 24: "CRITICAL SPELLING: the headline reads 'Sunday' — S-u-n-d-a-y, six letters, including the letter a.",
 25: "CRITICAL: the script reads exactly 'do I need?' ending with ONLY a question mark, no period.",
 28: "CRITICAL: ALL text sits in an empty dark area of the frame and is NEVER covered by the person; every letter of 'from now' must be fully visible. This post has NO price: do NOT render any price, number other than 30, dollar sign or the word PRICE.",
 12: "Hands are not visible in the frame.", 19: "Hands are not visible in the frame.",
 20: "The client's hands are out of frame; the single gloved hand is anatomically correct with five fingers.",
}

def prompt(day):
    st, h, s, sup, lab, price = C[day]; p = gen.posts[day]
    lines = [f'HEADLINE (serif): "{h}"', f'SCRIPT ACCENT (champagne-gold handwritten script, layered with the headline): "{s}"',
             f'SUPPORTING LINE (small tracked caps): "{sup}"']
    if price:
        lines.append(f'PRICE LABEL (tiny tracked caps): "{lab}"   PRICE: "{price}"')
    lines.append('BRAND (small tracked caps, bottom): "SOLACE SKIN LAB"')
    crit = []
    if price:
        crit.append("CRITICAL: the price is SIXTY-FOUR dollars and ninety-nine cents, rendered exactly '$64.99'.")
    if "2 Facials" in h:
        crit.append("CRITICAL: the two people MUST be two clearly DIFFERENT individuals — different faces, hair, skin tone and age. Never twins or a duplicated/mirrored face.")
    if "®" in h + sup:
        crit.append("Render ® small and raised right after BOTOX.")
    if day in EXTRA: crit.append(EXTRA[day])
    if "≠" in h:
        crit.append("Render the not-equal sign ≠ correctly.")
    return "\n".join([pt.BASE, pt.STYLES[st], pt.RULES, "", "SCENE: " + p["imageScene"], "",
                      "EXACT TEXT IN IMAGE:", *lines, *crit, "No other text anywhere in the image."])

def run(day):
    f = OUT / f"day{day:02d}.png"
    for attempt in range(3):
        try:
            res = gen.call(prompt(day)); url = res["images"][0]["url"]; raw = str(f) + ".raw.png"
            urllib.request.urlretrieve(url, raw)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-vf", "scale=1080:1080:flags=lanczos",
                            "-frames:v", "1", str(f) + ".tmp.png"], check=True)
            shutil.move(str(f) + ".tmp.png", f); Path(raw).unlink()
            with open(gen.LOG, "a") as lg:
                lg.write(json.dumps({"day": day, "v": 2, "style": C[day][0], "model": "openai/gpt-image-2",
                                     "provider": "fal.run (own FAL_KEY)", "quality": "medium", "src": url, "ts": time.time()}) + "\n")
            print(f"day{day:02d} OK {C[day][0]}", flush=True); return True
        except Exception as e:
            print(f"day{day:02d} attempt {attempt+1}: {e}", flush=True); time.sleep(6)
    return False

if __name__ == "__main__":
    a = sys.argv[1:]; days = sorted(C) if a == ["all"] else [int(x) for x in a]
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(5) as ex: res = list(ex.map(run, days))
    print(f"RESUMEN: {sum(res)}/{len(days)}")
