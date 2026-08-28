#!/usr/bin/env python3
import json

path='/opt/data/solace-skin-lab/september-2026/calendar_v2_2026-09-01_to_2026-09-30.json'
cal=json.load(open(path))

by_day={p['day']:p for p in cal}

# ---- Day 2: DpSCAN skin/scalp/hair scanner ----
d=by_day[2]
d['type']='Trust'
d['title']='YOUR SKIN, SCALP & HAIR. ANALYZED.'
d['hook']='YOUR SKIN, SCALP & HAIR. ANALYZED.'
d['body']='A free DpSCAN gives you an in-depth, data-driven look at the condition of your skin, scalp and hair — so we can recommend what actually fits you. No guesswork, just a clearer starting point.'
d['cta']='Book a free scan and see your skin differently.'
d['imageTitle']='YOUR SKIN, SCALP & HAIR. ANALYZED.'

# ---- Day 4: All the LED lights (face & body) from $79.99 ----
d=by_day[4]
d['type']='LED'
d['title']='ALL THE LIGHTS. FACE & BODY.'
d['hook']='ALL THE LIGHTS. FACE & BODY.'
d['body']='We have every light — for face and body. Multi-wavelength LED therapy in one place, from targeted facials to full-body sessions. Sessions start at $79.99.'
d['cta']='Book a session from $79.99 and glow all over.'
d['imageTitle']='ALL THE LIGHTS. FACE & BODY.'

# ---- Day 5: Neck & Decollete 24K ----
d=by_day[5]
d['type']='Education'
d['title']='NECK & DÉCOLLETÉ 24K'
d['hook']='NECK & DÉCOLLETÉ 24K'
d['body']='The neck and décolleté are the first to show age. Our 24K gold serum and cream help firm, smooth and reduce the appearance of expression lines — so your skin looks as cared-for as your face.'
d['cta']='Ask about our Neck & Décolleté 24K ritual.'
d['imageTitle']='NECK & DÉCOLLETÉ 24K'

# ---- Day 12: LED facial face & neck, $64.99 with luxury skincare ----
d=by_day[12]
d['type']='Facial'
d['title']='FACIAL + LED. FACE & NECK.'
d['hook']='FACIAL + LED. FACE & NECK.'
d['body']='A facial finished with LED light therapy, for both face and neck. Add any luxury skincare product and it is just $64.99 — with a free facial included.'
d['cta']='Book your facial + LED for $64.99.'
d['imageTitle']='FACIAL + LED. FACE & NECK.'

# ---- Day 26: Derma Jade Eye Solution ----
d=by_day[26]
d['type']='Trust'
d['title']='DERMA JADE EYE SOLUTION'
d['hook']='DERMA JADE EYE SOLUTION'
d['body']='Cooling jade, gentle sonic vibrations and LED — a luxury eye ritual that soothes puffiness and supports a refreshed, radiant look. The calmest few minutes of your day.'
d['cta']='Ask us about the Derma Jade Eye ritual.'
d['imageTitle']='DERMA JADE EYE SOLUTION'

json.dump(cal, open(path,'w'), ensure_ascii=False, indent=2)
print("Calendario actualizado OK")
for dd in [2,4,5,12,26]:
    p=by_day[dd]
    print(f"Day {dd}: {p['title']}")
