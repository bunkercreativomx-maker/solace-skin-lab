#!/usr/bin/env python3
# Genera calendar_v2_2026-09-01_to_2026-09-30.json desde el copy aprobado en la sala.
import json, datetime

# (day, type, title/hook, body, cta)
POSTS = [
 (1,"Promotion","TUESDAYS WERE MADE FOR TWO · 2×1 + wine","Two facials. One glass of wine. Zero excuses. Tuesdays at Solace are 2×1 facials — bring the person who keeps saying \"next time\" and get two free facials to share.","Tag your glow partner, then book before Tuesday fills."),
 (2,"Education","YOUR SKIN BARRIER IS YOUR BEST FRIEND","That tight, flaky, sensitive feeling is usually a barrier that's been stripped — not \"bad skin.\" Your barrier keeps moisture in and irritants out, and El Paso's dry air works against it every day. A gentle, barrier-first routine can help your skin feel calmer.","Save this for the next time it feels off."),
 (3,"Salmon DNA","SALMON DNA · SKIN-NOURISHING SCIENCE","Salmon DNA (PDRN) is the ingredient quietly taking over med-spa facials — molecules that may help support the skin's natural repair and hydration. No, it won't smell like fish. Yes, it's backed by growing aesthetic research.","Ask how a Salmon DNA treatment works."),
 (4,"LED","THE GLOW STARTS WITH LIGHT","LED light therapy is the calmest step in our room — warm, gentle, zero downtime. Different wavelengths target different concerns, and many clients pair it with their facial.","Book an LED session."),
 (5,"Education","EL PASO SUN: 365 DAYS A YEAR","El Paso sun doesn't take winter off. UV adds up on short drives, patio lunches, and school pickups — not just beach days. Daily SPF is the most consistent thing you can do for your skin.","Save this as your year-round reminder."),
 (6,"Microneedling","BREAKOUTS DON'T END AT 30","Adult acne isn't a teenage problem — plenty of men deal with breakouts and the scarring that follows well past 30. Microneedling may help improve the appearance of acne-scarred skin over a series of treatments. Individual results vary.","Book a consult and let's talk about what's realistic."),
 (7,"BOTOX","BOTOX® COSMETIC · YOU, REFRESHED","BOTOX® Cosmetic is about looking like you — refreshed, not frozen. A quick in-office treatment that temporarily improves the look of moderate frown lines and crow's feet. Real treatment, real care, results that still look like you.","Book a consultation to see if it fits your goals."),
 (8,"Promotion","GRAB YOUR GLOW PARTNER · 2×1 + wine","She keeps saying \"someday.\" Make it this Tuesday. 2×1 facials, a glass of wine, and two free facials to share — a whole girls' night, skincare edition.","Tag your glow partner and reserve before the week fills."),
 (9,"Education","THIRSTY SKIN ISN'T OILY SKIN","Shiny by noon doesn't always mean oily. Dehydrated skin can overproduce oil to compensate — which is why harsh, drying products make it worse. The fix often starts with hydration, not stripping.","Not sure which one you have? That's what a consult is for."),
 (10,"BOTOX","BEFORE YOU BOOK: ASK THIS","Good injectables start with good questions. Ask about your injector's training, how many units are typically used for your area, and what \"refreshed\" means for your face. We'd rather you ask first than guess.","Send us your question and we'll walk you through it."),
 (11,"Promotion","FREE FACIAL WITH LUXURY SKINCARE · $64.99","Get a free facial with the purchase of any luxury skincare product — only $64.99. Build a routine that actually fits your skin and leave with a professional facial on us.","Call (915) 995-9524 for eligible products and terms."),
 (12,"Facial","A FACIAL, TAILORED TO YOUR SKIN","Your skin isn't a template. The right facial starts with what your skin needs right now — not a one-size menu. Every Solace facial begins with a conversation, then gets tailored to your skin's current condition.","Book yours and we'll build it around you."),
 (13,"Salmon DNA","SALMON DNA · THE INGREDIENT EVERYONE ASKS ABOUT","It's the question we hear most right now: \"what's Salmon DNA?\" PDRN is a regenerative ingredient that may help support skin repair and deep hydration. No price games — just good science.","Ask how a Salmon DNA facial could fit your routine."),
 (14,"BOTOX","3 BOTOX® MYTHS, BROKEN","Myth 1: it'll make you look frozen. Myth 2: it's only for older skin. Myth 3: results are permanent. BOTOX® Cosmetic is about subtle refreshment, used by a wide range of ages, and results are temporary.","Want the real story? Send us your question."),
 (15,"Promotion","MID-MONTH GLOW, SHARED · 2×1 + wine","Halfway through September and your skin deserves the same energy. 2×1 facials, wine, and two free facials to share — grab a friend and make it a mid-month reset.","Reserve your Tuesday before it's gone."),
 (16,"Engagement","NAME YOUR SEPTEMBER SKIN GOAL","What's the one thing you want from your skin this month? Less redness? Fewer breakouts? A calmer barrier? Tell us in the comments — the most common goals become our next education posts.","Your skin goal beats any trend."),
 (17,"Microneedling","SCALP CARE ISN'T JUST FOR HAIR","Healthy-looking hair starts at the scalp. Microneedling on the scalp may help support the appearance of fuller, healthier hair for men, as part of a personalized approach. Individual results vary.","Book a private consult and we'll tell you honestly if you're a candidate."),
 (18,"LED","RED LIGHT. BLUE LIGHT. WHAT'S WHAT?","Red light is typically used for signs of aging; blue light is often chosen for acne-prone skin. Neither is magic — but both are gentle, non-invasive options many clients pair with facials.","Ask us which LED option matches your skin."),
 (19,"BOTOX","SEE A REAL BOTOX® SESSION","This is what a real BOTOX® Cosmetic appointment looks like — clean, quick, and guided by a conversation, not a sales pitch. We believe you should see the process before you book.","Book a consult and we'll walk you through every step."),
 (20,"Education","SMALL STEPS, REAL SKIN","Real skin progress isn't a 10-step overnight overhaul. It's SPF every morning, one product that fits, and consistency you can keep. Small steps, repeated, are what your skin actually responds to.","Save this for the weeks you're tempted to overdo it."),
 (21,"JUVÉDERM","JUVÉDERM® LIPS · BALANCED, NOT OVERDONE","Lip filler is about balance — proportion, shape, and a result that looks like you, just more defined. JUVÉDERM® is an FDA-approved family of fillers used to add subtle volume to the lips. Individual results vary.","Book a consult for a look that's yours."),
 (22,"Promotion","FALL GLOW, SHARED · 2×1 + wine","Fall in El Paso still calls for SPF — and this Tuesday, it calls for a friend. 2×1 facials, wine, and two free facials to share.","Tag your person and book while September Tuesdays still have room."),
 (23,"Microneedling","ACNE SCARS: THE GUY CONVERSATION","Guys, acne scars don't have to be a permanent reminder. Microneedling may help improve the appearance of acne scarring over a series of sessions. It's a real conversation worth having.","Book an evaluation for an honest read on your options."),
 (24,"Promotion","LUXURY + FREE FACIAL · $64.99","Your skincare should earn its place on your shelf — and right now it comes with a free facial. Purchase any luxury skincare product for just $64.99 and get a professional facial on us.","Call (915) 995-9524 to check eligible products and terms."),
 (25,"Education","EL PASO FALL = DRY AIR SEASON","As El Paso cools off, the air gets drier — and your skin feels it first. Fall is when barrier support and hydration matter most. A seasonal reset can help your skin adjust before winter.","Save this and come in when your skin starts feeling tight."),
 (26,"Trust","PREPPED. CLEAN. READY.","Every treatment starts the same way at Solace: a clean, prepared room and a clear plan. No surprises, no rushed steps — just calm, clinical care. That's the standard on every appointment.","Come see the process for yourself."),
 (27,"Microneedling","SCALP MICRONEEDLING FOR MEN","Thinning hair is a concern men don't always talk about. Scalp microneedling may help support a healthier-looking scalp as part of a broader approach. Individual results vary.","Book a private consult and let's have the conversation."),
 (28,"Facial","THE FULL GLOW: FACIAL + LED","The complete reset: a tailored facial finished with LED light therapy. Our favorite pairing for calm, hydrated, even-looking skin — without downtime.","Book your facial + LED combo and feel what a full treatment is like."),
 (29,"Promotion","LAST 2×1 TUESDAY OF SEPTEMBER","This is the last 2×1 Tuesday of September. After this, you wait for October. 2×1 facials, wine, and two free facials to share — one more chance to bring your person.","Call (915) 995-9524 now to lock your Tuesday."),
 (30,"Conversion","OCTOBER APPOINTMENTS ARE FILLING","September's almost gone and October appointments are already filling. If you've been meaning to book that facial, consult, or injectables visit — this is your sign.","Call (915) 995-9524 and lock in your October spot."),
]

DOW = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
HASHTAGS = "#SolaceSkinLab #ElPasoSkin #RealSkin #MedSpaElPaso #SkinGoals"

out = []
for day, typ, title, body, cta in POSTS:
    # Day 1 = Tue Sep 1, 2026
    d = datetime.date(2026, 9, 1) + datetime.timedelta(days=day-1)
    dow = DOW[d.weekday()]
    post = {
        "day": day,
        "date": f"{dow}, Sep {d.day}",
        "scheduledAt": f"2026-09-{d.day:02d}T15:00:00Z",
        "type": typ,
        "title": title,
        "hook": title,
        "body": body,
        "desire": "",
        "cta": cta,
        "hashtags": HASHTAGS,
        "imageTitle": title,
        "imageScript": "",
        "imageScene": "Dark-luxury editorial: gold serif dominant typography + white script, charcoal background, warm candlelight, real models filling the frame. GPT Image renders imageTitle as integrated typography; no AI logos; no price on Salmon DNA posts; phone (915) 995-9524 shown exactly.",
    }
    out.append(post)

with open("calendar_v2_2026-09-01_to_2026-09-30.json", "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"OK: {len(out)} posts -> calendar_v2_2026-09-01_to_2026-09-30.json")
print("types:", sorted(set(p["type"] for p in out)))