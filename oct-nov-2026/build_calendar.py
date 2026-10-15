"""Solace Skin Lab — Oct 16 – Nov 14, 2026 calendar, built from the client's own 30-day idea list.
All public copy in ENGLISH (client's Spanish posts translated). Tuesdays = 2 FACIALS FOR $64.99 TOTAL.
Days 31-35 = posts that need REAL client material (team photo, results, staff reel, review, before/after).
"""
import json
from datetime import date

HT = "#SolaceSkinLab #ElPasoMedSpa #ElPasoTX #CieloVistaMall"
TUESDAY_BODY = ("👯‍♀️ TWO FACIALS. ONE PRICE.\n\n🔥 2 FACIALS FOR $64.99 TOTAL 🔥\n\nYes, you read that right…\n"
                "TWO FACIALS FOR ONLY $64.99.\n\nBring your:\n👯‍♀️ Bestie\n❤️ Partner\n👩‍👧 Mom\n👭 Sister\n\n"
                "Because self-care is better together. ✨\n\n📍 SOLACE — EL PASO, TEXAS\n\n"
                "⚠️ Tuesday appointments are limited.")
TUESDAY_CTA = "👇 TAG WHO YOU'RE BRINGING.\n📲 MESSAGE US TO BOOK."

P = []
def add(d, typ, title, hook, body, cta, img_title, img_sub, scene, tags="", src=None):
    P.append(dict(date=d, type=typ, title=title, hook=hook, body=body, desire="", cta=cta,
                  hashtags=(HT + " " + tags).strip(), imageTitle=img_title, imageSub=img_sub,
                  imageScene=scene, clientIdea=src))

add(date(2026,10,16), "Brand", "WELCOME TO SOLACE", "✨ Welcome to Solace Skin Lab ✨",
    "Where beauty, confidence and advanced skincare come together.\n\nYour skin is unique. Your treatment should be too.\n\n✨ Facials starting at $64.99\n\n📍 El Paso, Texas",
    "📲 Message us to schedule your appointment.",
    "Welcome to Solace", "Facials starting at $64.99",
    "Serene woman in her early 30s, light-medium olive skin, dark hair wrapped in a white towel, reclining on a treatment bed with eyes closed while gloved esthetician hands gently apply a cream mask with a soft brush; warm overhead treatment lamp pooling light on her face, deep dark background.",
    "#Facials #Skincare", 1)
add(date(2026,10,17), "Facial", "YOUR SKIN DESERVES A LITTLE LOVE", "✨ YOUR SKIN DESERVES A LITTLE LOVE ✨",
    "Give your skin the refresh it's been asking for.\n\n🧖‍♀️ Professional facial\n✨ Deep cleansing\n✨ Personalized care\n✨ That GLOW we love\n\n🔥 FACIAL $64.99\n\n📍 Solace — El Paso, Texas",
    "📲 Message us to book.",
    "Your skin deserves a little love", "Facial · $64.99",
    "Macro close-up of a Latina woman in her late 20s with a dewy, freshly cleansed cheek, glass dropper releasing a glistening drop of serum onto her skin, gloved hand steadying her jaw; dramatic warm overhead light, dark moody background, real pores visible.",
    "#Facial #GlowingSkin", 2)
add(date(2026,10,18), "Lifestyle", "SUNDAY RESET", "SUNDAY RESET ✨",
    "💧 Hydrate\n🧴 Skincare\n💤 Rest\n❤️ Take care of yourself\n\nAnd maybe…\n\n🧖‍♀️ Book that facial you've been putting off.\n\n✨ $64.99\n\n📍 El Paso, Texas",
    "📲 Message us to book.",
    "Sunday Reset", "Hydrate · Skincare · Rest",
    "Calm Sunday-morning still life and person: woman in her 40s with natural grey streaks, in a cream robe, sitting by a sunlit window holding a glass of water, a jar of moisturizer and a folded white towel on the table; soft warm morning light, muted cream and warm brown tones, quiet and real.",
    "#SundayReset #SelfCare", 7)
add(date(2026,10,19), "Microneedling", "MICRONEEDLING", "✨ MICRONEEDLING ✨",
    "Looking to improve the appearance of:\n\n✔️ Acne scars\n✔️ Uneven texture\n✔️ Enlarged-looking pores\n✔️ Fine lines\n✔️ Dull-looking skin\n\nReady to take your skincare to the next level?\n\n📍 Solace — El Paso, Texas",
    "📲 Message us to learn more.",
    "Microneedling", "Smoother-looking texture starts here",
    "Documentary close-up of a microneedling session: gloved hand holding a motorized microneedling pen with a clear sterile cartridge against the forehead of a man in his 30s with medium-brown skin, white disposable cap, skin slightly flushed and glossy with serum; bright focused clinical light, dark surroundings.",
    "#Microneedling #SkinTexture", 3)
add(date(2026,10,20), "2×1 Tuesday", "TUESDAY ONLY — 2 FOR 1", "🚨🚨 TUESDAY ONLY 🚨🚨", TUESDAY_BODY, TUESDAY_CTA,
    "2 Facials for $64.99", "Tuesdays only · Bring your bestie",
    "Two best friends side by side on two treatment beds wearing white headbands and white cream masks, laughing at each other: one Black woman in her late 20s with short natural curls, one Latina woman in her early 30s with long dark wavy hair; warm candle-like lighting, dark elegant room.",
    "#TwoForOne #FacialTuesday #BestieDay", "Tuesday")
add(date(2026,10,21), "Facial", "WHEN WAS YOUR LAST FACIAL?", "WHEN WAS YOUR LAST FACIAL? 👀",
    "If you had to think about it…\n\nIt's probably been too long. 😂\n\n✨ Professional Facial — $64.99\n\nTake an hour for yourself and give your skin some attention.\n\n📍 El Paso, Texas",
    "📲 Message us to book.",
    "When was your last facial?", "Professional Facial · $64.99",
    "Woman in her mid 30s, fair skin with freckles, auburn hair in a white towel, eyes closed under a warm steam vapor facial steamer, soft mist visible in the light beam, dark background, documentary realism.",
    "#Facial #TreatYourself", 5)
add(date(2026,10,22), "Education", "MORE PRODUCTS ≠ BETTER SKIN", "MORE PRODUCTS ≠ BETTER SKIN. 👀",
    "Sometimes you don't need another serum sitting in your bathroom.\n\nYou need to understand what your skin actually needs.\n\nThat's where professional skincare comes in.\n\n✨ Facial — $64.99",
    "📲 Schedule your appointment at Solace.",
    "More products ≠ better skin", "Know what your skin actually needs",
    "Overhead editorial still life: a crowded bathroom counter with many unbranded plain amber and white skincare bottles and jars (no labels, no text), one woman's hand reaching past them; moody warm side light, dark stone counter, shallow depth of field.",
    "#SkincareTips #LessIsMore", 8)
add(date(2026,10,23), "Self-care", "AN HOUR JUST FOR YOU?", "An hour just for YOU? ❤️",
    "No work.\nNo to-do list.\nNo stress.\n\nJust you and a little self-care. ✨\n\n🧖‍♀️ Facial $64.99\n\n📍 Solace — El Paso",
    "📲 Book by message.",
    "An hour just for you", "No work · No stress · Facial $64.99",
    "Woman in her early 50s, warm brown skin, silver short hair, wrapped in a plush white blanket on a treatment bed, completely relaxed with eyes closed, warm stones beside her, single warm lamp glow, dark tranquil room.",
    "#SelfCare #MeTime", 6)
add(date(2026,10,24), "Engagement", "BE HONEST", "BE HONEST 👀😂",
    "What's the ONE thing you'd improve about your skin?\n\nA) Texture\nB) Fine lines\nC) Dark spots\nD) Acne scars\nE) Pores",
    "👇 Drop your letter in the comments.",
    "Be honest 👀", "What's the ONE thing you'd improve?",
    "Woman in her late 20s, East Asian, examining her skin up close in a round vanity mirror with warm bulbs, playful raised eyebrow, dark bathroom background, natural skin texture.",
    "#SkinGoals #BeHonest", 4)
add(date(2026,10,25), "BOTOX®", "LET'S TALK BOTOX®", "LET'S TALK BOTOX®. 💉✨",
    "The goal doesn't always have to be looking dramatically different.\n\nFor many clients, it's about achieving a refreshed appearance while still looking like themselves.\n\nCurious? A consultation tells you if BOTOX® Cosmetic is right for you. Individual results vary.\n\n📍 El Paso, Texas",
    "📲 Message Solace to schedule an injector consultation.",
    "Let's talk BOTOX®", "Refreshed — still you",
    "Consultation moment, no needle: female injector in black scrubs and gloves gently pointing at a woman's forehead area with a fingertip while the client in her early 40s, light skin, blonde shoulder-length hair, sits upright smiling naturally; warm focused lamp, dark clinical-luxury room.",
    "#BotoxCosmetic #Consultation", 10)
add(date(2026,10,26), "Engagement", "OKAY… BE HONEST", "OKAY… BE HONEST. 😂👇",
    "How many products are in your skincare routine?\n\n😬 0–1\n😊 2–3\n✨ 4–5\n👑 6+\n\nThe 6+ crew… we need to talk. 😂",
    "👇 Comment your number.",
    "Okay… be honest", "How many products in your routine?",
    "Playful flat lay: a hand-held fan of six small plain unlabeled skincare bottles and droppers held by a woman's manicured hand in front of a dark velvet background, warm spotlight, no text or labels.",
    "#SkincareRoutine #Poll", 12)
add(date(2026,10,27), "2×1 Tuesday", "TWO FACIALS. ONE PRICE.", "🚨 IT'S TUESDAY 🚨", TUESDAY_BODY, TUESDAY_CTA,
    "2 Facials for $64.99", "Tuesdays only · Bring your mom",
    "Mother and adult daughter having facials together on adjacent treatment beds, relaxed and smiling, hands resting under the towels (no hands visible): mother in her late 50s, Latina, grey-streaked dark hair; daughter in her late 20s with a different face shape and lighter brown hair in a bun; warm lamp light, dark luxe spa room.",
    "#TwoForOne #FacialTuesday #MomAndMe", "Tuesday")
add(date(2026,10,28), "Facial", "YOUR SKIN CALLED", "YOUR SKIN CALLED. 📞",
    "It wants a facial. 😂\n\n🧖‍♀️ Professional Facial\n✨ Relax\n✨ Refresh\n✨ Glow\n\n🔥 ONLY $64.99\n\n📍 Solace — El Paso, Texas",
    "📲 Message us to book.",
    "Your skin called.", "It wants a facial · $64.99",
    "Humorous but elegant: woman in her early 30s, medium-dark skin, wearing a white headband and a green clay mask, holding a smartphone to her ear with a surprised smile, sitting on a treatment bed; warm overhead lamp, dark background. The phone screen is black and blank.",
    "#Facial #YourSkinCalled", 13)
add(date(2026,10,29), "Confidence", "PERFECT SKIN ISN'T THE GOAL", "PERFECT SKIN ISN'T THE GOAL. ❤️",
    "Confidence is.\n\nWe're not chasing perfection.\n\nWe want you to look in the mirror and feel amazing in YOUR skin.\n\n✨ That's Solace.\n\n📍 El Paso",
    "📲 Message us to start your skin journey.",
    "Perfect skin isn't the goal.", "Confidence is.",
    "Unretouched portrait of a confident woman in her mid 30s with visible natural texture, a few freckles and faint acne marks, warm tan skin, hair pulled back, soft genuine smile looking straight into camera; warm Rembrandt lighting, dark background, editorial and honest.",
    "#Confidence #RealSkin", 14)
add(date(2026,10,30), "Conversion", "THIS IS YOUR SIGN", "You've been saying it for weeks… 👀",
    "\"I'll book later…\"\n\"Maybe next week…\"\n\"Let me think about it…\" 👀\n\nTHIS IS YOUR SIGN. 😂🔥\n\n🧖‍♀️ Facial $64.99\n\nStop putting it off.",
    "📲 Message us and book.",
    "This is your sign.", "Facial · $64.99",
    "Woman in her late 20s, Middle Eastern features, lying on a treatment bed with eyes closed and a blissful smile while gloved hands massage her temples; golden warm light from above like a spotlight, dark surroundings.",
    "#ThisIsYourSign #Facial", 15)
add(date(2026,10,31), "Seasonal", "HAPPY HALLOWEEN", "HAPPY HALLOWEEN 🎃",
    "Had fun tonight? Don't sleep in your makeup.\n\nDouble cleanse: an oil or balm first to melt everything away, then a gentle cleanser. Finish with a hydrating serum and moisturizer.\n\nYour skin will thank you tomorrow. ✨\n\n📍 Solace — El Paso, Texas",
    "👇 Tell us your costume in the comments.",
    "Happy Halloween", "Don't sleep in your makeup",
    "Woman in her late 20s removing dramatic dark Halloween eye makeup with a cotton pad in a bathroom mirror, a small carved pumpkin with a candle on the counter, warm candlelight, moody and elegant, real skin texture.",
    "#HappyHalloween #DoubleCleanse", None)
add(date(2026,11,1), "Microneedling", "WHY DOES EVERYONE TALK ABOUT MICRONEEDLING?", "WHY DOES EVERYONE TALK ABOUT MICRONEEDLING? 👀",
    "Sometimes skincare alone isn't enough when you're concerned about the appearance of deeper texture or acne scarring.\n\nThat's when professional treatments can come in.\n\n✨ Discover microneedling at Solace.",
    "📲 Message us to learn more.",
    "Why does everyone talk about microneedling?", "Discover it at Solace",
    "Extreme close-up of a sterile microneedling cartridge tip gliding across a woman's cheek glossy with clear serum, gloved fingers stretching the skin, crisp focus on the cartridge and real pores, warm clinical light with deep dark falloff.",
    "#Microneedling #SkinCare", 16)
add(date(2026,11,2), "Facial", "PLANS THIS WEEK?", "PLANS THIS WEEK? 👀",
    "We've got a better one:\n\n🧖‍♀️ You\n✨ A facial\n📵 Your phone put away\n😌 One hour to relax\n\n🔥 FACIAL $64.99\n\nYou deserve it.\n\n📍 Solace — El Paso",
    "📲 Message us to book.",
    "Plans this week?", "We've got a better one · Facial $64.99",
    "Woman in her early 40s, light brown skin, curly hair tied up, lying relaxed on a treatment bed with cool gel eye pads, her smartphone face-down on a small tray next to her, esthetician's gloved hands applying a hydrating mask; warm lamp, dark room.",
    "#Facial #UnplugAndRelax", 18)
add(date(2026,11,3), "2×1 Tuesday", "2 FOR 1 TUESDAY", "👯‍♀️ BRING YOUR BESTIE — IT'S TUESDAY", TUESDAY_BODY, TUESDAY_CTA,
    "2 Facials for $64.99", "Tuesdays only · Bring your sister",
    "Two sisters with clearly different faces on two treatment beds in white robes and headbands, laughing toward each other with green clay masks on, hands resting under the robes (no hands visible): one in her mid 30s with straight black hair and fair skin, the other in her early 20s with honey-blonde hair and a tan; warm candle glow, dark luxe spa.",
    "#TwoForOne #FacialTuesday #SisterTime", "Tuesday")
add(date(2026,11,4), "Engagement", "TAG SOMEONE WHO NEEDS A FACIAL", "TAG SOMEONE WHO NEEDS A FACIAL. 👇😂",
    "Your best friend?\nYour mom?\nYour sister?\nYour boyfriend? 👀\n\nMaybe all of them. 😂\n\n✨ Facials $64.99\n\n📍 Solace — El Paso, Texas",
    "📲 Message us to book.",
    "Tag someone who needs a facial", "Facials · $64.99",
    "Man in his early 30s with a beard and medium-brown skin, white headband, lying on a treatment bed with a white cream mask, smiling amused at the camera with his hands out of frame, while one gloved esthetician hand brushes on the mask; warm overhead light, dark background, fun and real.",
    "#TagAFriend #Facial", 19)
add(date(2026,11,5), "Process", "THE SOLACE EXPERIENCE", "WHAT HAPPENS WHEN YOU COME TO SOLACE?",
    "1️⃣ We listen.\n2️⃣ We discuss your goals.\n3️⃣ We evaluate your options.\n4️⃣ We create a plan with you.\n\nNo two clients are exactly alike.\n\nYour skincare shouldn't be either.\n\n🧖‍♀️ Facials $64.99\n\n📍 El Paso, Texas",
    "📲 Message us to book your first visit.",
    "The Solace experience", "We listen · We plan with you",
    "Consultation scene: esthetician in black scrubs seated across from a client in her mid 40s with dark skin and braids, both smiling, the esthetician holding a tablet with a blank dark screen, warm lamp light, dark elegant consultation room, documentary feel.",
    "#Consultation #PersonalizedSkincare", 23)
add(date(2026,11,6), "Engagement", "THIS OR THAT", "THIS OR THAT? 👀",
    "💉 BOTOX® OR Facial\n✨ Microneedling OR Facial\n☀️ Morning skincare OR 🌙 Night skincare\n💄 Makeup OR ✨ Natural glow",
    "👇 Drop your answers in the comments.",
    "This or that?", "Morning or night skincare?",
    "Split-mood still life on a dark marble counter: left side a sunlit morning skincare setup with a plain sunscreen tube and a glass of water, right side a candlelit night setup with a plain glass serum dropper and a silk sleep mask; no labels, no text on products.",
    "#ThisOrThat #SkincareRoutine", 22)
add(date(2026,11,7), "Lifestyle", "WEEKEND GLOW ACTIVATED", "WEEKEND GLOW ACTIVATED. ✨🔥",
    "Facial ✔️\nSkincare ✔️\nConfidence ✔️\nWeekend ✔️\n\n🧖‍♀️ Facial $64.99\n\nThat fresh-after-a-facial feeling hits different. 😍\n\n📍 El Paso",
    "📲 Message us to book.",
    "Weekend glow activated", "Facial · $64.99",
    "Woman in her late 20s, glowing fresh skin, mixed race, natural curls loose, getting ready for a night out in front of a warm-lit mirror, touching her dewy cheek and smiling; dark moody background with soft bokeh lights.",
    "#WeekendGlow #FreshSkin", 20)
add(date(2026,11,8), "Lifestyle", "SUNDAY RESET", "SUNDAY RESET ✨",
    "💧 Drink water\n🧴 Do your skincare\n🛏️ Rest\n🧘‍♀️ Unplug\n🧖‍♀️ Book your facial\n\n✨ $64.99\n\nA new week starts tomorrow.\n\nStart it feeling good about yourself. ❤️",
    "📲 Message us to book.",
    "Sunday reset", "Rest · Unplug · Glow",
    "Woman in her mid 30s, East Asian, in cozy knit loungewear sitting cross-legged on a bed with crisp linen, applying a clear hydrating gel mask with her fingertips, a cup of tea beside her; soft warm late-afternoon light, cream and warm brown palette.",
    "#SundayReset #SelfCareSunday", 28)
add(date(2026,11,9), "BOTOX®", "HOW MANY UNITS OF BOTOX® DO I NEED?", "\"HOW MANY UNITS OF BOTOX® DO I NEED?\"",
    "There's no universal number.\n\nTreatment depends on the areas being addressed, your anatomy, muscle activity and your desired outcome.\n\nThat's why your injector evaluates YOU. Individual results vary.\n\n📍 El Paso, Texas",
    "📲 Schedule your consultation.",
    "How many units do I need?", "Your injector evaluates YOU",
    "Injector in black scrubs and gloves assessing the expression lines of a man in his late 40s with greying temples and light-medium skin, asking him to raise his eyebrows, her gloved fingertip near his forehead, no needle in frame; warm focused lamp, dark clinical-luxury room.",
    "#BotoxCosmetic #InjectorConsult", 25)
add(date(2026,11,10), "2×1 Tuesday", "TUESDAY — 2 FACIALS, ONE PRICE", "🚨 TUESDAY ONLY 🚨 BRING YOUR PARTNER", TUESDAY_BODY, TUESDAY_CTA,
    "2 Facials for $64.99", "Tuesdays only · Bring your partner",
    "Couple's facial: a woman in her early 30s with dark skin and long box braids and a man in his early 30s with light skin and short brown hair, on two treatment beds side by side, both with white cream masks, smiling at each other; warm candlelight, dark luxe spa room.",
    "#TwoForOne #FacialTuesday #DateNight", "Tuesday")
add(date(2026,11,11), "Brand", "POV: YOU WORK AT SOLACE", "POV:",
    "You work at Solace and little by little the whole team gets addicted to skincare. 😂😂\n\n⚠️ WARNING:\n\nAfter visiting us, you might want another facial too. 🤷‍♀️✨\n\nAnd for $64.99… we don't blame you. 😂",
    "📲 Message us to book.",
    "POV: you work at Solace", "Skincare-addicted since day one",
    "Behind-the-scenes candid: two estheticians in black scrubs laughing while testing a plain unlabeled serum on the backs of their hands at a dark treatment-room counter, warm lamp light, only hands and lower faces partially visible, documentary feel.",
    "#POV #SpaLife", 26)
add(date(2026,11,12), "Motivation", "30 DAYS FROM NOW WILL COME EITHER WAY", "30 DAYS FROM NOW WILL COME EITHER WAY.",
    "You can keep saying:\n\n\"Someday…\"\n\nOr you can simply start. ❤️\n\n🧖‍♀️ Facial $64.99",
    "📲 Message us to book.",
    "30 days from now will come either way.", "Or you can simply start.",
    "Woman in her early 40s, Latina, walking through a softly lit spa doorway in a white robe, glancing back over her shoulder with a confident smile; warm light spilling from the room, dark hallway, cinematic.",
    "#StartToday #SkinJourney", 27)
add(date(2026,11,13), "Community", "EL PASO ❤️ THANK YOU", "EL PASO ❤️ THANK YOU.",
    "Thank you for every appointment, referral, review, comment and share.\n\nThank you to everyone who recommends us, visits us and trusts us.\n\nSolace keeps growing because of you.\n\nAnd we're just getting started. ✨\n\n📍 El Paso, Texas",
    "👇 Tell us your favorite Solace moment.",
    "El Paso, thank you.", "We're just getting started",
    "Golden-hour landscape of the Franklin Mountains above El Paso, Texas, with warm desert light, a softly blurred white spa towel and a small candle on a ledge in the foreground; warm, grateful mood, no text on anything.",
    "#ElPaso #ThankYou", 29)
add(date(2026,11,14), "Conversion", "STOP THINKING ABOUT IT. START.", "🚨 STOP THINKING ABOUT IT. START. 🚨",
    "Stop saying \"Someday.\"\n\n✨ Facials\n✨ Microneedling\n✨ BOTOX® & Injectables\n✨ Advanced skincare\n\n🧖‍♀️ FACIALS $64.99\n\nYour skin journey can start TODAY.\n\nYour skin will thank you. ❤️\n\n📍 SOLACE — EL PASO, TEXAS",
    "📲 MESSAGE US TO BOOK.",
    "Stop thinking about it. Start.", "Facials · $64.99",
    "Bold editorial close-up of a woman in her early 30s, deep brown skin, glowing hydrated complexion, looking directly into the lens with quiet determination, a glass serum dropper held near her cheek; dramatic warm side light, black background.",
    "#StartToday #Facials", 30)

# Posts that require REAL client material — never generated with AI
NEED = [
    ("Team", "MEET THE TEAM", "Behind Solace is a team that loves what they do. ❤️",
     "We want every person who walks through our doors to feel:\n\n✨ Heard\n✨ Comfortable\n✨ Pampered\n✨ Safe\n\nCome meet us.\n\n🧖‍♀️ Facials $64.99\n\n📍 El Paso, Texas",
     "📲 Message us to book.", "a real team photo (group or individual)", 9),
    ("Results", "RESULTS SPEAK LOUDER THAN WORDS", "RESULTS SPEAK LOUDER THAN WORDS. 🔥",
     "Real treatments.\nReal clients.\nReal confidence.\n\n✨ YOUR SKIN. YOUR JOURNEY.",
     "📲 Ready to start? Message us.", "real client result photos with client consent", 11),
    ("Reel", "STAFF REEL", "WE ASKED THE SOLACE TEAM:",
     "\"What skincare product could you NEVER live without?\" 😂\n\nWatch until the end. 👀",
     "👇 Now tell us yours.", "a short vertical video of the team answering (9:16, 15–60 s)", 17),
    ("Testimonial", "CLIENT REVIEW", "⭐⭐⭐⭐⭐",
     "Nothing makes us happier than reading this:\n\n\"[REAL CLIENT REVIEW]\"\n\nThank you for trusting Solace. ❤️\n\nEvery client trusts us with something important: their skin.\n\nAnd we take that trust VERY seriously.\n\n📍 El Paso, Texas",
     "📲 Message us to book.", "a real Google/Facebook review (screenshot or text + first name)", 21),
    ("Transformation", "TRANSFORMATION", "THIS is what we love to see. 🔥",
     "Not just the change in the skin…\n\nThe change in CONFIDENCE. ❤️\n\n📸 [REAL BEFORE / AFTER]",
     "📲 Ready to start? Message us.", "a real before/after with written client consent", 24),
]

out = []
for i, p in enumerate(P, 1):
    p = dict(p); d = p.pop("date")
    p.update(day=i, date=d.strftime("%a, %b %-d"), isoDate=d.isoformat(),
             scheduledAt=f"{d.isoformat()}T15:00:00Z")
    out.append(p)
for j, (typ, title, hook, body, cta, need, src) in enumerate(NEED, len(out) + 1):
    out.append(dict(day=j, date="Date TBD — when material arrives", isoDate=None, scheduledAt=None,
                    type="Needs your material", title=title, hook=hook, body=body, desire="", cta=cta,
                    hashtags=HT, imageTitle="", imageSub="", imageScene="", clientIdea=src,
                    needsMaterial=need))
assert len(P) == 30 and len(out) == 35
json.dump(out, open("/opt/data/solace-skin-lab/oct-nov-2026/calendar_2026-10-16_to_2026-11-14.json", "w"),
          ensure_ascii=False, indent=1)
print("ok", len(out), [p["date"] for p in out[:30] if "Tue" in p["date"]])
