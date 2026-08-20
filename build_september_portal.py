#!/usr/bin/env python3
# Porta el portal de agosto -> septiembre-2026/ reconfigurado.
import os, shutil

SRC = "index.html"
DST = "september-2026/index.html"
os.makedirs("september-2026", exist_ok=True)
os.makedirs("september-2026/images", exist_ok=True)

html = open(SRC).read()

R = [
  # --- mecanicos (global) ---
  ("images/august-2026-v2/", "images/"),
  ("calendar_v2_2026-07-24_to_2026-08-22.json", "calendar_v2_2026-09-01_to_2026-09-30.json"),
  ("facebook_ads_v2_2026-07-24_to_2026-08-22.json", "facebook_ads_v2_2026-09-01_to_2026-09-30.json"),
  ("BUNKER_CAMPAIGN='august-2026'", "BUNKER_CAMPAIGN='september-2026'"),
  ("solace_august_v2_review", "solace_september_review"),
  # --- titulo / header ---
  ("Solace Skin Lab Med Spa — August 2026 Content Review", "Solace Skin Lab Med Spa — September 2026 Content Review"),
  ("July 24 – August 22, 2026 · Cielo Vista Mall, El Paso TX", "September 1 – 30, 2026 · Cielo Vista Mall, El Paso TX"),
  ("AUGUST 2026 · V2 · 30-DAY CAMPAIGN", "SEPTEMBER 2026 · DARK LUXURY · 30-DAY CAMPAIGN"),
  ("August Skin Reset<em>Real skin. Smart care.</em>", "The September Glow<em>Dark luxury. Real skin.</em>"),
  ("A brighter, more human campaign built around education, real Solace treatment photography, six promotional creatives, and personalized care. Review every GPT Image 2 visual and AIDA copy below.",
   "A dark-luxury September built around five 2×1 Tuesdays, a value-stack $64.99 offer, men's microneedling, Salmon DNA science, and El Paso desert-skin education. Review every GPT Image 2 visual and AIDA copy below."),
  ("<div class=\"metric\"><b>6</b><span>promotion creatives</span></div>", "<div class=\"metric\"><b>8</b><span>Meta ads</span></div>"),
  ("<div class=\"metric\"><b>4</b><span>microneedling concerns</span></div>", "<div class=\"metric\"><b>5</b><span>Tuesdays 2×1</span></div>"),
  # --- promos note 1 ---
  ("<strong>V2 campaign requirements included:</strong> daily promo “FREE facial with any luxury skincare product — only $64.99” on every pending post; <strong>Salmon DNA Collection</strong> facials (deep cleanse, acne, brightening, anti-aging, Salmon DNA) promoted by benefits only — <em>no prices shown</em>; four Tuesday 2×1 creatives with wine + two FREE facials; microneedling content for acne scars and scalp/hair (men); official phone <strong>(915) 995-9524</strong>. No numbered 01–04 labels or generated logos appear in final artwork.",
   "<strong>September campaign requirements:</strong> <strong>dark-luxury direction</strong> on every creative — gold serif dominant + white script on charcoal, warm candlelight, real models filling the frame; <strong>Tuesday 2×1 facials + wine + two FREE facials</strong> on 5 Tuesdays (1, 8, 15, 22, 29); <strong>$64.99 luxury skincare + FREE facial</strong> bundle (2 days, value-stack, never a discount); <strong>Salmon DNA</strong> promoted by benefits only — <em>no prices shown</em>; microneedling content for <strong>MEN</strong> (acne + scalp/hair); BOTOX® Cosmetic + JUVÉDERM® from real authorized photography; official phone <strong>(915) 995-9524</strong>. No AI-generated logos."),
  # --- export / whatsapp strings ---
  ("campaign:'August Skin Reset V2',period:'2026-07-24 to 2026-08-22'", "campaign:'September Dark Luxury',period:'2026-09-01 to 2026-09-30'"),
  ("solace-august-2026-v2-client-review.json", "solace-september-2026-client-review.json"),
  ("Solace Skin Lab — August Content Review", "Solace Skin Lab — September Content Review"),
  # --- enlace de descarga a la pagina de imagenes ---
  ('href="facebook_ads_v2_2026-09-01_to_2026-09-30.json" download', 'href="facebook_ads_v2_2026-09-01_to_2026-09-30.json" download'),
]

for old, new in R:
    n = html.count(old)
    html = html.replace(old, new)

open(DST, "w").write(html)
print("Portado:", DST, "|", os.path.getsize(DST), "bytes")

# Verificaciones de strings criticos
checks = [
  ("campaign septiembre", "BUNKER_CAMPAIGN='september-2026'" in html),
  ("calendar sept", "calendar_v2_2026-09-01_to_2026-09-30.json" in html),
  ("ads sept", "facebook_ads_v2_2026-09-01_to_2026-09-30.json" in html),
  ("img path rel", 'src="images/day' in html),
  ("localStorage", "solace_september_review" in html),
  ("no august img leftover", "august-2026-v2" not in html),
  ("no august campaign leftover", "BUNKER_CAMPAIGN='august-2026'" not in html),
  ("no old json leftover", "2026-07-24_to_2026-08-22" not in html),
]
for label, ok in checks:
    print(("  OK " if ok else "  FAIL ") + label)