import json
import sys
from pathlib import Path
from PIL import Image

ROOT = Path('/opt/data/solace-skin-lab')
DATA = ROOT / 'calendar_v2_2026-07-24_to_2026-08-22.json'
IMG_DIR = ROOT / 'images' / 'august-2026-v2'
REPORT = ROOT / 'generation-report-v2.json'
REQUIRED_FIELDS = {'day','date','scheduledAt','type','title','hook','body','desire','cta','hashtags','imageTitle','imageScript','imageScene'}
OFFICIAL_PHONE = '(915) 995-9524'
RETIRED = ['2060', '(915) 995-2060', '915-995-2060']
errors = []

posts = json.loads(DATA.read_text(encoding='utf-8'))
if len(posts) != 30:
    errors.append(f'Expected 30 posts, got {len(posts)}')
if [p.get('day') for p in posts] != list(range(1,31)):
    errors.append('Days are not consecutive 1-30')
for p in posts:
    missing = REQUIRED_FIELDS - set(p)
    if missing:
        errors.append(f"Day {p.get('day')}: missing {sorted(missing)}")
    for field in ('hook','body','desire','cta'):
        if not str(p.get(field,'')).strip():
            errors.append(f"Day {p.get('day')}: blank {field}")
    if any(old in json.dumps(p, ensure_ascii=False) for old in RETIRED):
        errors.append(f"Day {p.get('day')}: retired phone fragment found")

for day in (4,25):
    p = posts[day-1]
    if p.get('imageTitle') != 'GET A FREE FACIAL':
        errors.append(f'Day {day}: bad skincare headline')
    if p.get('imageOffer') != 'WITH THE PURCHASE OF ANY LUXURY SKINCARE PRODUCT • ONLY $64.99':
        errors.append(f'Day {day}: bad skincare offer')
for day in (5,12,19,26):
    p = posts[day-1]
    blob = ' '.join([p.get('imageTitle',''),p.get('imageOffer',''),p.get('body','')])
    if '2×1' not in blob or 'WINE + 2 FREE FACIALS' not in blob:
        errors.append(f'Day {day}: Tuesday offer mismatch')
    if 'TUESDAY 2×1 + WINE + 2 FREE FACIALS' not in p.get('body',''):
        errors.append(f'Day {day}: Tuesday body does not preserve literal offer')
    if 'Wine available only to guests age 21+.' not in p.get('body',''):
        errors.append(f'Day {day}: missing exact 21+ qualifier')
if posts[9].get('imageTitle') != 'BEFORE BOTOX® COSMETIC':
    errors.append('Day 10: incomplete BOTOX® Cosmetic image title')
public_blob = json.dumps(posts, ensure_ascii=False).lower()
for forbidden in ('trained provider', 'trained gloved provider', 'natural renewal response', 'natural renewal process'):
    if forbidden in public_blob:
        errors.append(f'Forbidden or unsupported wording remains: {forbidden}')
for day in (13,18,20,27):
    blob = json.dumps(posts[day-1], ensure_ascii=False).lower()
    required = {13:'acne',18:'fine lines',20:'scalp',27:'scar'}[day]
    if required not in blob:
        errors.append(f'Day {day}: missing microneedling concern {required}')

missing_images = []
for day in range(1,31):
    p = IMG_DIR / f'day{day:02d}.png'
    if not p.exists():
        missing_images.append(day)
        continue
    try:
        with Image.open(p) as im:
            if im.format != 'PNG' or im.size != (1024,1024):
                errors.append(f'Day {day}: {im.format} {im.size}, expected PNG 1024x1024')
    except Exception as exc:
        errors.append(f'Day {day}: unreadable image: {exc}')
if missing_images:
    errors.append(f'Missing images: {missing_images}')

if REPORT.exists():
    report = json.loads(REPORT.read_text(encoding='utf-8'))
    summary = report.get('summary', {})
    if summary.get('model') != 'gpt-image-2-high':
        errors.append(f"Wrong model: {summary.get('model')}")
    if summary.get('flux_used') is not False:
        errors.append('Report does not prove flux_used=false')
    for item in report.get('results', []):
        if item.get('provider') != 'openai-codex':
            errors.append(f"Day {item.get('day')}: provider is {item.get('provider')}")
        if item.get('model') != 'gpt-image-2-high':
            errors.append(f"Day {item.get('day')}: model is {item.get('model')}")
else:
    errors.append('Missing generation report')

result = {
    'ok': not errors,
    'posts': len(posts),
    'images': 30 - len(missing_images),
    'official_phone': OFFICIAL_PHONE,
    'errors': errors,
}
print(json.dumps(result, indent=2, ensure_ascii=False))
sys.exit(0 if not errors else 1)
