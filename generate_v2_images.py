import importlib.util
import json
import os
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image

ROOT = Path('/opt/data/solace-skin-lab')
DATA = ROOT / 'calendar_v2_2026-07-24_to_2026-08-22.json'
OUT = ROOT / 'images' / 'august-2026-v2'
REPORT = ROOT / 'generation-report-v2.json'
PILOT = ROOT / 'images' / 'pilot-v2-free-facial.png'
OUT.mkdir(parents=True, exist_ok=True)

# Use only GPT Image 2 High through the migrated creative-profile Codex OAuth.
os.environ['HERMES_HOME'] = '/opt/data/profiles/creative'
os.environ['OPENAI_IMAGE_MODEL'] = 'gpt-image-2-high'

module_path = '/opt/data/hermes-agent/plugins/image_gen/openai-codex/__init__.py'
spec = importlib.util.spec_from_file_location('openai_codex_image_backend_solace_v2', module_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f'Could not load {module_path}')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
thread_local = threading.local()

PALETTES = [
    'warm ivory, rose clay, soft espresso and restrained sage',
    'soft cream, powder blue, muted terracotta and espresso',
    'warm white, pale peach, refined sage and soft espresso',
    'ivory, dusty rose, muted sky blue and warm brown',
]
LAYOUTS = [
    'full-bleed editorial photography with the headline integrated into open tonal space',
    'organic magazine-cover composition with curved text flow around the subject, never crossing the face',
    'close documentary treatment crop with compact editorial typography in one safe corner',
    'premium product-and-person composition with layered depth and a subtle translucent tonal falloff for text',
    'asymmetrical beauty-editorial composition with generous breathing room but no rigid split panel',
    'centered photographic hero with restrained top-and-bottom typographic hierarchy',
]

IMAGE_CTAS = {
    1: 'COMMENT YOUR SKIN PRIORITY', 2: 'ASK US ABOUT LED', 3: 'SAVE THIS GUIDE',
    4: 'BOOK YOUR CONSULTATION', 5: 'CALL TO RESERVE', 6: 'BOOK A CONSULTATION',
    7: 'SAVE THIS SPF REMINDER', 8: 'BOOK YOUR FACIAL', 9: 'COMMENT YOUR AUGUST GOAL',
    10: 'BRING YOUR QUESTIONS', 11: 'ASK IF IT FITS YOUR SKIN', 12: 'CALL TO RESERVE',
    13: 'REQUEST AN EVALUATION', 14: 'BOOK A BOTOX® CONSULTATION', 15: 'SHARE YOUR SKIN PRIORITY',
    16: 'ASK US ABOUT LED', 17: 'SAVE THIS REMINDER', 18: 'BOOK A CONSULTATION',
    19: 'CALL TO RESERVE', 20: 'ASK ABOUT ELIGIBILITY', 21: 'BOOK A CONSULTATION',
    22: 'SEND US YOUR QUESTION', 23: 'SAVE FOR DRY DAYS', 24: 'LEARN ABOUT THE PROCESS',
    25: 'CALL TO CONFIRM TERMS', 26: 'CALL TO RESERVE', 27: 'SCHEDULE AN EVALUATION',
    28: 'ASK ABOUT AVAILABILITY', 29: 'COMMENT YOUR SMALL WIN', 30: 'CALL TO GET STARTED',
}
PHONE_DAYS = {4, 5, 6, 8, 10, 11, 12, 13, 14, 18, 19, 20, 21, 24, 25, 26, 27, 28, 30}


def provider():
    if not hasattr(thread_local, 'provider'):
        thread_local.provider = module.OpenAICodexImageGenProvider()
    return thread_local.provider


def exact_text(post):
    texts = [post['imageTitle']]
    if post.get('imageScript'):
        texts.append(post['imageScript'])
    if post.get('imageOffer'):
        texts.append(post['imageOffer'])
    texts.append(IMAGE_CTAS[post['day']])
    if post['day'] in PHONE_DAYS:
        texts.append('(915) 995-9524')
    texts.append('Solace Skin Lab Med Spa')
    return texts


def prompt_for(post):
    day = post['day']
    texts = exact_text(post)
    text_block = '\n'.join(f'{i + 1}. “{value}”' for i, value in enumerate(texts))
    source_note = ''
    if post.get('sourceAsset'):
        source_note = '''\nSOURCE IMAGE EDITING RULES\nUse the supplied Solace Skin Lab client image as the authentic photographic foundation. Preserve the real people, treatment, equipment, and recognizable documentary character. Recompose, crop, extend, clean up, and add the approved editorial typography, but do not replace the real client/provider with generated people. Remove or fully replace any pre-existing promotional text, prices, logos, neon graphic treatment, or reference-layout artifacts that conflict with the exact allowed text below. Never copy old prices or claims from the source.\n'''
    return f'''Create one finished premium square social-media advertisement for Solace Skin Lab Med Spa, 1024 × 1024, 1:1. This is campaign day {day}: {post['title']}.

MODEL AND OUTPUT AUTHORITY
Generate the photography/edit, composition, and all typography together inside this image. Do not leave placeholder text. Do not create a mockup, frame, carousel, collage, logo, emblem, lotus, monogram, seal, watermark, product brand, or fabricated credential.
{source_note}
ART DIRECTION
High-end but approachable skincare editorial, luminous and realistic rather than generic Canva. Use {PALETTES[(day - 1) % len(PALETTES)]}. Use {LAYOUTS[(day - 1) % len(LAYOUTS)]}. Photography must dominate roughly 80–90% of the canvas. No dominant black/charcoal, metallic gold, neon, cheap coupon style, starburst, oversized badge, rigid half-page panel, or repeated template look.

SCENE
{post['imageScene']}
Natural adult Latina features when people appear, authentic pores and age texture, restrained retouching, correct anatomy and hands, believable professional environment and equipment. For medical-looking procedures: correct gloves, tool, angle and treatment location; no blood, exaggerated redness, fake before/after, unsafe technique, impossible anatomy, or treatment too near the eyes. For BOTOX® Cosmetic and JUVÉDERM® consultation images, do not imply guaranteed outcomes.

TYPOGRAPHY
Render every letter accurately and dynamically inside the artwork. Main headline: refined high-contrast editorial serif, largest element, mobile-legible. Supporting line: elegant italic serif or restrained handwritten style. Offer/CTA/phone/business name: clean premium sans serif. Use safe margins of at least 70 px, strong contrast, balanced spacing, and never place text across a face, hand, treatment tool, or important product.

EXACT ALLOWED TEXT — CRITICAL
The image must contain these exact text elements and no other words or numbers:
{text_block}

Do not paraphrase, duplicate, omit, misspell, translate, or invent text. Preserve capitalization, punctuation, symbols, registered marks, multiplication signs, dollar signs, decimal points, parentheses, and hyphens exactly. “Solace Skin Lab Med Spa” is plain text only, never a generated logo.

FINAL QA TARGET
One polished 1024 × 1024 feed-ready advertisement with realistic photography, premium integrated typography, no extra text, no invented marks, no cropped words, no malformed hands/tools, and no dark charcoal campaign styling.'''


def normalize_png(source, target):
    with Image.open(source) as im:
        im = im.convert('RGB')
        if im.size != (1024, 1024):
            im = im.resize((1024, 1024), Image.Resampling.LANCZOS)
        im.save(target, format='PNG', optimize=True)
    with Image.open(target) as check:
        check.verify()
    with Image.open(target) as check:
        if check.size != (1024, 1024):
            raise RuntimeError(f'Bad final dimensions for {target}: {check.size}')


def valid_existing(path):
    try:
        with Image.open(path) as im:
            return im.format == 'PNG' and im.size == (1024, 1024) and path.stat().st_size > 100_000
    except Exception:
        return False


def generate_one(post):
    day = post['day']
    final = OUT / f'day{day:02d}.png'
    if valid_existing(final):
        return {'day': day, 'status': 'existing', 'provider': 'openai-codex', 'model': 'gpt-image-2-high', 'size': '1024x1024', 'quality': 'high', 'path': str(final)}
    if day == 4:
        normalize_png(PILOT, final)
        return {'day': day, 'status': 'pilot-approved', 'provider': 'openai-codex', 'model': 'gpt-image-2-high', 'size': '1024x1024', 'quality': 'high', 'path': str(final)}

    last = None
    prompt = prompt_for(post)
    image_url = post.get('sourceAsset')
    for attempt in range(1, 4):
        try:
            result = provider().generate(prompt=prompt, aspect_ratio='square', image_url=image_url)
        except Exception as exc:
            result = {'success': False, 'error': str(exc), 'error_type': type(exc).__name__}
        if result.get('success'):
            normalize_png(result['image'], final)
            return {
                'day': day,
                'status': 'generated',
                'attempt': attempt,
                'provider': result.get('provider', 'openai-codex'),
                'model': result.get('model'),
                'size_reported': result.get('size'),
                'size': '1024x1024',
                'quality': result.get('quality', 'high'),
                'sourceAsset': image_url,
                'path': str(final),
            }
        last = result
        time.sleep(8 * attempt)
    return {'day': day, 'status': 'failed', 'error': last}


if not DATA.exists():
    raise SystemExit(f'Missing V2 data: {DATA}')
posts = json.loads(DATA.read_text(encoding='utf-8'))
if len(posts) != 30 or [p['day'] for p in posts] != list(range(1, 31)):
    raise SystemExit('V2 data must contain consecutive days 1–30')

results = []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(generate_one, post): post['day'] for post in posts}
    for future in as_completed(futures):
        result = future.result()
        results.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        REPORT.write_text(json.dumps({'results': sorted(results, key=lambda r: r['day'])}, indent=2, ensure_ascii=False), encoding='utf-8')

results.sort(key=lambda r: r['day'])
failed = [r for r in results if r['status'] == 'failed']
summary = {
    'total': len(results),
    'successful': len(results) - len(failed),
    'failed': failed,
    'provider': 'openai-codex',
    'model': 'gpt-image-2-high',
    'quality': 'high',
    'physical_size': '1024x1024',
    'flux_used': False,
}
REPORT.write_text(json.dumps({'summary': summary, 'results': results}, indent=2, ensure_ascii=False), encoding='utf-8')
print('FINAL_SUMMARY ' + json.dumps(summary, ensure_ascii=False), flush=True)
if failed:
    raise SystemExit(1)
