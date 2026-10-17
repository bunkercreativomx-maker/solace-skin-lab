"""Build Oct-Nov 2026 V3 review portal (days 4-30) from the client's own reference media + notes.
Media = client's reference photos/videos UNCHANGED except the removals the client asked for
(and third-party clinic names). Output: /opt/data/solace-skin-lab/oct-nov-2026-v3/"""
import json, os, re, shutil, subprocess
from pathlib import Path

V3 = Path(__file__).parent
SRC_PORTAL = V3.parent
OUT = SRC_PORTAL.parent / 'oct-nov-2026-v3'
MEDIA = OUT / 'media'
MEDIA.mkdir(parents=True, exist_ok=True)

cal = {p['day']: p for p in json.load(open(SRC_PORTAL / 'calendar_2026-10-16_to_2026-11-14.json'))}
appr = json.load(open('/opt/data/cache/scratch/solace_appr.json'))
rec = [x for x in appr['approvals'] if x['campaign'] == 'oct-nov-2026'][0]
notes = {p['id']: (p.get('notes') or '').strip() for p in rec['review']['posts']}

PHONE = '(915) 209-2060'
BASE_TAGS = '#SolaceSkinLab #ElPasoMedSpa #ElPasoTX #CieloVistaMall'
BOOK = f'📲 Call {PHONE} or message us to book.'

C = {
 4: ('Microneedling', 'MICRONEEDLING FOR ACNE', 'Acne is part of the journey. It doesn\'t have to define your story. 💛',
     'Breakouts, marks and uneven texture can take a toll on your confidence.\n\nMicroneedling works with your skin\'s own healing response to stimulate collagen and help improve acne marks, texture and overall skin quality — with a plan made for YOUR skin.\n\n📍 Inside Cielo Vista Mall, El Paso',
     f'📲 Book your microneedling consultation: {PHONE} or send us a message.', '#Microneedling #AcneSkin #AcneScars'),
 5: ('2×1 Tuesday', 'TUESDAY ONLY — 2 FACIALS $74.99', '🚨 TUESDAY ONLY: 2 FACIALS FOR $74.99 🚨',
     'This is your sign to disconnect from the world for an hour. ✨\n\nBring your bestie, mom, sister or partner and choose your facial:\n• Deep Cleansing\n• Brightening\n• Hydrating\n\n👯‍♀️ 2 facials · $74.99 total · Tuesdays only',
     f'📲 Book your Tuesday spot: {PHONE}. Spots are limited!', '#FacialTuesday #TwoForOne #BestieDay'),
 6: ('GLP-1 & Peptides', 'GLP-1 & PEPTIDES', 'Your wellness journey starts with a consultation. 🩺',
     'Now at Solace Skin Lab: GLP-1 & peptide programs.\n\n• Semaglutide\n• Tirzepatide\n• NAD+\n• GHK-Cu\n…and more.\n\nEvery program starts with a medical consultation to review your history, goals and options. Treatment is only prescribed when it\'s right for you.',
     f'📲 Ask us about GLP-1 & peptides: {PHONE} or send us a message.', '#GLP1 #Semaglutide #Tirzepatide #Peptides #NADplus'),
 7: ('BOTOX®', 'BOTOX® COSMETIC & XEOMIN®', 'Why Botox®? 🤔',
     'Smooth the lines caused by everyday expressions — forehead lines, crow\'s feet and frown lines.\n\nAt Solace we offer TWO trusted brands:\n• Botox® Cosmetic\n• Xeomin®\n\nQuick appointment, minimal downtime and natural-looking results.',
     f'📲 Book your Botox® or Xeomin® appointment: {PHONE}.', '#Botox #Xeomin #Neurotoxin #AntiAging'),
 8: ('Facial', 'A FACIAL FOR EVERY SKIN TYPE — $74.99', 'An hour just for you. ✨',
     'Acne, dark spots, expression lines or you just want that GLOW?\n\nWe have a facial for every skin type, customized to what your skin needs today.\n\n✨ Professional Facial — $74.99',
     BOOK, '#Facial #Skincare #GlowingSkin'),
 9: ('Lip Filler', 'LIP FILLER — JUVÉDERM® & BELOTERO®', 'Lips: off ➜ on 💋',
     'Soft, natural-looking volume and definition with two premium brands:\n• Juvéderm®\n• Belotero®\n\nEvery lip treatment starts with an evaluation so we design the result that fits YOUR face.',
     f'📲 Book your lip evaluation: {PHONE}.', '#LipFiller #Juvederm #Belotero #Lips'),
 10: ('24K Gold Facial', '24K GOLD EXPERIENCE — $74.99', 'The 24K Gold Experience ✨',
     'A detoxifying, hydrating facial with a magnetic mask that\'s lifted off with a magnet… leaving a layer of 24K gold on your skin. 🧲✨\n\n✨ $74.99 any day\n👯‍♀️ 2 for $74.99 on Tuesdays',
     f'📲 Book your 24K Gold Experience: {PHONE}.', '#24KGoldFacial #GoldFacial #Facial'),
 11: ('Microneedling', 'MICRONEEDLING — COLLAGEN INDUCTION', 'Give your skin a reason to rebuild. 🔁',
     'Your skin loses collagen as you age.\n\nMicroneedling (collagen induction therapy) stimulates new collagen + elastin:\n➜ smoother texture\n➜ softer-looking scars\n➜ firmer-looking skin\n\n📍 Inside Cielo Vista Mall, El Paso',
     f'📲 Book your microneedling appointment: {PHONE}.', '#Microneedling #Collagen #SkinTexture'),
 12: ('2×1 Tuesday', 'TWO FACIALS. ONE PRICE. $74.99', 'TWO FACIALS. ONE PRICE. 👯‍♀️',
     'Every Tuesday: 2 facials for $74.99 total. Choose:\n• Anti-Aging Lifting\n• Clear Skin Reset\n• Lift & Glow\n\nReveal your natural radiance — together. ✨',
     f'📲 Book your Tuesday spot: {PHONE}. Limited spots!', '#FacialTuesday #TwoForOne #AntiAging'),
 13: ('GLP-1', 'GLP-1 WEIGHT LOSS', 'Ready for a change? 💛',
     'Medical weight loss with GLP-1 medications — semaglutide or tirzepatide — guided by a licensed provider.\n\nAsk us how it works and whether it\'s right for you.',
     f'📲 Ask & book your consultation: {PHONE}.', '#GLP1 #Semaglutide #Tirzepatide #WeightLoss'),
 14: ('BOTOX®', 'BOTOX® COSMETIC OR XEOMIN®', 'Natural results start with precision. ✍️',
     'Every injectable treatment starts with careful facial mapping, so you look like YOU — just refreshed.\n\nChoose Botox® Cosmetic or Xeomin®.',
     f'📲 Book your appointment: {PHONE}.', '#Botox #Xeomin #NaturalResults'),
 15: ('Facial', 'THERMAL ANTI-AGING LIFTING — $74.99', 'Thermal Anti-Aging Lifting 🔥',
     'A warming thermal mask helps target dark spots and visibly firm the skin… followed by red light therapy to maximize your results. ❤️‍🔥\n\n✨ $74.99',
     f'📲 Book your lifting facial: {PHONE}.', '#AntiAging #RedLightTherapy #LiftingFacial'),
 16: ('Lip Filler', 'LIP FILLER — JUVÉDERM® OR BELOTERO®', 'No tricks. Just beautiful lips. 🎃💋',
     'Natural-looking lip filler with Juvéderm® or Belotero® — designed for your face and your style.',
     f'📲 Book your lip consultation: {PHONE}.', '#LipFiller #Juvederm #Belotero #Halloween'),
 17: ('Facial', 'BYE BYE BLACKHEADS — $74.99', 'Say goodbye to blackheads. ✨',
     'Our deep cleansing facial with extractions helps clear congested pores and reset oily, acne-prone skin — plus a recovery routine to keep results at home.\n\n✨ 1 facial $74.99\n👯‍♀️ 2 for $74.99 on Tuesdays',
     BOOK, '#Blackheads #DeepCleansing #AcneSkin'),
 18: ('Microneedling', 'MICRONEEDLING FOR HAIR GROWTH', 'Thinning hair? Let\'s talk. 💈',
     'Scalp microneedling stimulates the scalp to support healthier, fuller-looking hair. For men and women.\n\nWe evaluate your scalp first — results vary from person to person.',
     f'📲 Book your scalp consultation: {PHONE}.', '#HairGrowth #ScalpMicroneedling #HairLoss'),
 19: ('2×1 Tuesday', '2 FOR 1 TUESDAY — $74.99', '2 FOR 1 TUESDAY 👯‍♀️',
     '2 facials for $74.99 total — every Tuesday.\n\nBring your bestie and leave with smooth, fresh, glowing skin. ✨',
     f'📲 Book your Tuesday spot: {PHONE}.', '#FacialTuesday #TwoForOne'),
 20: ('GLP-1 & Peptides', 'GLP-1 & PEPTIDES', 'Are you ready for a change?',
     'Start your wellness journey at Solace:\n• GLP-1: semaglutide, tirzepatide\n• Peptides: NAD+, GHK-Cu and more\n\nAlways with a medical consultation first.',
     f'📲 Call {PHONE} or message us to get started.', '#GLP1 #Peptides #WeightLoss'),
 21: ('BOTOX®', 'MEET XEOMIN®', 'Meet Xeomin®. 💉',
     'Smooth expression lines with Xeomin® or Botox® Cosmetic — two trusted options, one natural-looking goal.\n\nNot sure which one is for you? Ask us!',
     f'📲 Book your appointment: {PHONE}.', '#Xeomin #Botox #Wrinkles'),
 22: ('Facial', 'FACIAL + DERMAPLANING — $74.99', 'Facial + Dermaplaning ✨ $74.99',
     'Dermaplaning gently removes dead skin and peach fuzz, so your skin renews and absorbs your facial better.\n\nThe result: smooth, bright, makeup-ready skin.',
     BOOK, '#Dermaplaning #Facial #SmoothSkin'),
 23: ('Lip Filler', 'LIP FILLER — 0.55 ML OR 1 ML', 'Your lips, just better. 💋',
     'Lip filler in two sizes:\n• 0.55 ml — a subtle refresh\n• 1 ml — more volume\n\nWith Juvéderm® or Belotero®.',
     f'📲 Book your lip consultation: {PHONE}.', '#LipFiller #Juvederm #Belotero'),
 24: ('Facial', 'SALMON PDRN FACIAL — $74.99', 'Salmon PDRN Facial 🐟✨',
     'A regenerating facial with salmon PDRN to support hydration, glow and skin repair.\n\n✨ 1 facial $74.99\n👯‍♀️ 2 for $74.99 on Tuesdays',
     BOOK, '#SalmonPDRN #PDRN #Facial #SundayReset'),
 25: ('Microneedling', 'MICRONEEDLING', 'Microneedling for real skin concerns. ✨',
     '• Acne\n• Pigmentation\n• Scars\n• Photoaging\n\nMicroneedling boosts collagen and elastin to improve tone and texture over a series of sessions.',
     f'📲 Book your microneedling: {PHONE}.', '#Microneedling #AcneScars #Pigmentation'),
 26: ('2×1 Tuesday', 'TUESDAY GLOW — 2 FOR $74.99', 'TUESDAY GLOW 👯‍♀️✨',
     'Glow Facial for two — $74.99 total, every Tuesday.\n\nBring someone who deserves a glow-up.',
     f'📲 Book your Tuesday spot: {PHONE}.', '#FacialTuesday #GlowFacial #TwoForOne'),
 27: ('Peptides', 'PEPTIDES — NAD+ & GHK-Cu', 'Aging is natural. How you age is up to you.',
     'Peptide therapy — NAD+, GHK-Cu and more — to support regeneration and rejuvenation from within.\n\nIt all starts with a consultation.',
     f'📲 Book your consultation: {PHONE}.', '#Peptides #NADplus #GHKCu #Longevity'),
 28: ('BOTOX®', 'BOTOX® EFFECTS', 'Botox® effects ✨',
     'Smoother lines • Lifted brows • Relaxed forehead\n\nNatural-looking results with Botox® Cosmetic or Xeomin®.',
     f'📲 Book your appointment: {PHONE}.', '#Botox #Xeomin #SmoothSkin'),
 29: ('Facial', 'GLASS SKIN — FACIAL + DERMAPLANING $74.99', 'Glass skin starts at Solace Skin Lab. ✨',
     'Facial + Dermaplaning — $74.99\n\nSmooth, bright, glass-like skin. 🪞',
     BOOK, '#GlassSkin #Dermaplaning #Facial'),
 30: ('Conversion', 'REFINE YOUR JAWLINE', 'Refine your jawline. ✨',
     'Non-surgical options to help define your jawline and lower face:\n• Botox® Cosmetic / Xeomin®\n• Microneedling to firm and improve skin quality\n\nWe\'ll recommend the right plan for you.',
     f'📲 Book your consultation: {PHONE}.', '#Jawline #Botox #Microneedling'),
}

# media: (file, what we changed)
CLEAN = {6: 'work/day06_clean.png', 7: 'work/day07_clean.png', 18: 'work/day18_clean.png',
         20: 'work/day20_clean.png', 30: 'work/day30_clean.png'}
VIDEO_OUT = {11: 'out/day11.mp4', 12: 'out/day12.mp4', 28: 'out/day28.mp4'}
EDIT_NOTE = {
 4: 'Your photo, unedited.', 6: 'Removed the "kin meds" logo and website.', 7: 'Removed the other clinic\'s name at the bottom.',
 11: 'Removed the other clinic\'s ending and added our location.', 12: 'Removed the last part (other spa\'s logo).',
 18: 'Removed the watermark.', 20: 'Removed the "kin MEDS" logo, website and icons.', 21: 'Second photo of the pin (Xeomin).',
 28: 'Removed the other clinic\'s website.', 30: 'Removed the other clinic\'s logo.',
}

def norm_image(src, dst):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(src), '-vf', "scale='min(1080,iw)':-2", '-q:v', '2', str(dst)], check=True)

posts = []
for d in range(4, 31):
    t, title, hook, body, cta, tags = C[d]
    vid = V3 / VIDEO_OUT[d] if (d in VIDEO_OUT and (V3 / VIDEO_OUT[d]).exists()) else (V3 / f'src/day{d:02d}.mp4')
    if vid.exists():
        dst = MEDIA / f'day{d:02d}.mp4'; shutil.copy(vid, dst); kind = 'video'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', '0.5', '-i', str(dst), '-frames:v', '1', '-vf', "scale='min(720,iw)':-2", '-q:v', '3', str(MEDIA / f'day{d:02d}_poster.jpg')], check=True)
    else:
        src = V3 / CLEAN[d] if d in CLEAN else next((V3 / 'src').glob(f'day{d:02d}.*'))
        dst = MEDIA / f'day{d:02d}.jpg'; norm_image(src, dst); kind = 'image'
    p = dict(cal[d])
    p.update(type=t, title=title, hook=hook, body=body, desire='', cta=cta, hashtags=f'{BASE_TAGS} {tags}',
             media=f'media/{dst.name}', mediaType=kind, clientNote=notes.get(d, ''),
             editNote=EDIT_NOTE.get(d, 'Your reference, unedited.'))
    for k in ('imageTitle', 'imageSub', 'imageScene'): p.pop(k, None)
    posts.append(p)

json.dump(posts, open(OUT / 'calendar_v3.json', 'w'), ensure_ascii=False, indent=1)
print('posts', len(posts), 'media', len(list(MEDIA.iterdir())))
