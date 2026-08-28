#!/usr/bin/env python3
"""Schedule Solace Skin Lab September 2026 calendar (30 posts) to Zernio.

Flow per post:
  1. POST /api/v1/media/presign  -> uploadUrl, publicUrl
  2. PUT image bytes to uploadUrl
  3. POST /api/v1/posts with content + mediaItems + platforms + scheduledFor

Account: Solace Skin Lab Facebook = 6a42e1c49d9472faae24d632
Day 1 -> START date (default today), day N -> START + (N-1) days @ 15:00 America/Denver.
"""
import os, sys, json, base64, urllib.request, urllib.error
from datetime import date, datetime, timedelta, timezone

API = "https://zernio.com/api/v1"
_CFG = "/opt/data/home/.zernio/config.json"
import re
_raw = open(_CFG, "rb").read().decode("utf-8", "replace")
_m = re.search(r'"apiKey"\s*:\s*"(sk_[A-Za-z0-9_]+)"', _raw)
KEY = _m.group(1) if _m else None
if not KEY:
    KEY = os.environ.get("ZERNIO_KEY")
assert KEY and KEY.startswith("sk_"), "could not load ZERNio key"

ACCOUNT = "6a42e1c49d9472faae24d632"  # Solace Skin Lab FB
IMG_DIR = "/opt/data/solace-skin-lab/september-2026/images"
CAL = "/opt/data/solace-skin-lab/september-2026/calendar_v2_2026-09-01_to_2026-09-30.json"
TZ = "America/Denver"
HOUR = 15  # 3pm El Paso/MT

def req(method, path, body=None, extra_headers=None, raw_url=None):
    url = raw_url or (API + path)
    h = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    if extra_headers:
        h.update(extra_headers)
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        resp = urllib.request.urlopen(r, timeout=60)
        return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def presign_and_upload(img_path):
    fn = os.path.basename(img_path)
    ct = "image/png"
    s, o = req("POST", "/media/presign", {"filename": fn, "contentType": ct})
    if s != 200:
        return None, f"presign {s}: {o[:200]}"
    d = json.loads(o)
    upload_url = d["uploadUrl"]
    public_url = d["publicUrl"]
    with open(img_path, "rb") as f:
        body = f.read()
    h = {"Content-Type": ct}
    r = urllib.request.Request(upload_url, data=body, headers=h, method="PUT")
    try:
        resp = urllib.request.urlopen(r, timeout=120)
        up = resp.status
    except urllib.error.HTTPError as e:
        return None, f"upload {e.code}: {e.read().decode()[:200]}"
    if up not in (200, 201):
        return None, f"upload bad status {up}"
    return public_url, None

def main():
    start = date.today()
    if len(sys.argv) > 1:
        start = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    days = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else None

    cal = json.load(open(CAL))
    by_day = {p["day"]: p for p in cal}
    results = []
    for day in sorted(by_day):
        if days and day not in days:
            continue
        p = by_day[day]
        sched = datetime.combine(start + timedelta(days=day - 1), datetime.min.time().replace(hour=HOUR))
        sched_iso = sched.strftime("%Y-%m-%dT%H:%M:%S")
        img = os.path.join(IMG_DIR, f"day{day:02d}.png")
        if not os.path.exists(img):
            results.append((day, "NO_IMAGE", img))
            continue
        pub, err = presign_and_upload(img)
        if err:
            results.append((day, f"UPLOAD_ERR:{err}", None))
            continue
        caption = "\n\n".join([
            p.get("hook", "").strip(),
            p.get("body", "").strip(),
            p.get("cta", "").strip(),
            (p.get("hashtags", "") or "").strip(),
        ]).strip()
        payload = {
            "content": caption,
            "mediaItems": [{"url": pub, "type": "image"}],
            "scheduledFor": sched_iso,
            "timezone": TZ,
            "platforms": [{"platform": "facebook", "accountId": ACCOUNT}],
        }
        s, o = req("POST", "/posts", payload)
        if s in (200, 201):
            try:
                pid = json.loads(o).get("data", {}).get("post", {}).get("_id") or json.loads(o).get("post", {}).get("_id")
            except Exception:
                pid = None
            results.append((day, f"OK {s} id={pid}", sched_iso))
        else:
            results.append((day, f"POST_ERR {s}: {o[:200]}", sched_iso))
    for r in results:
        print(r)
    with open("/opt/data/solace-skin-lab/zernio_september_schedule_report.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
