#!/usr/bin/env python3
"""Solace Skin Lab · Meta video ads Nov 2026 (HyperFrames).
Multi-scene 15-18 s ads: Kling hook clip + GPT-Image stills, kinetic luxury type, CloneVoice EN VO, deep-house bed + SFX.
usage: gen.py <ad> <fmt>   fmt = 9x16 | 4x5     -> /opt/data/hyperframes/solace-ads/ad0N_<fmt>/
"""
import json, os, re, shutil, subprocess, sys, difflib, html

SRC = '/opt/data/solace-skin-lab/ads-video-nov-2026'
NOV = '/opt/data/solace-skin-lab/november-2026'
ROOT = '/opt/data/hyperframes/solace-ads'
TPL = '/opt/data/hyperframes/dp-fb-d01-45'
PHONE = '(915) 209-2060'
VO = json.load(open(f'{SRC}/vo.json'))['ads']

def norm(w): return re.sub(r'[^a-z0-9]', '', w.lower())

def line_times(lines, words):
    script, owner = [], []
    for i, l in enumerate(lines):
        for w in l.split():
            n = norm(w)
            if n: script.append(n); owner.append(i)
    tw = [norm(w['text']) for w in words]
    m = {}
    for a, b, size in difflib.SequenceMatcher(None, script, tw, autojunk=False).get_matching_blocks():
        for k in range(size): m[a + k] = b + k
    st, en = [], []
    for i in range(len(lines)):
        hit = [m[j] for j, o in enumerate(owner) if o == i and j in m]
        st.append(words[min(hit)]['start'] if hit else None); en.append(words[max(hit)]['end'] if hit else None)
    total = words[-1]['end']
    for i in range(len(lines)):
        if st[i] is None:
            prev = en[i-1] if i and en[i-1] else 0
            nxt = next((st[j] for j in range(i+1, len(lines)) if st[j]), total)
            st[i] = prev + 0.1; en[i] = nxt - 0.1
    return st, en

# ---------------------------------------------------------------- ad specs
# media: 'clip:a4' (Kling mp4) | 'still:a2' | 'nov:d01v3' | 'web:clinic-01'
# text types: hook(words, script, script_at) | price(label, num, sub) | free(lead, sub) | offer(label,num,stamp) | line(eyebrow,title,script,support) | chips(items)
ADS = {
 1: dict(name='META-01 · Tuesday: product $74.99 + 2 FREE facials + wine', cta='MESSAGE US TO BOOK', note='TUESDAYS ONLY · SPOTS GO FAST', fine=None,
   recap=['Luxury product $74.99', '2 facials FREE', 'Glass of wine'],
   scenes=[('clip:a4', dict(t='hook', words='Tuesday plans?', script='Sorted.', script_word='sorted')),
           ('still:a2', dict(t='price', label='LUXURY SKINCARE PRODUCT', num='$74.99')),
           ('still:a1', dict(t='free', lead='+ 2 FACIALS', sub='YOU + YOUR BESTIE')),
           ('still:a3', dict(t='line', eyebrow='AND', title='A glass of wine.', script='cheers to you')),
           ('still:b3', dict(t='line', eyebrow='LIMITED SPOTS', title='Tuesdays only.', script='every week')),
           ('still:a4', dict(t='end'))]),
 2: dict(name='META-02 · Any day: product $74.99 + FREE facial', cta='MESSAGE US TO BOOK', note='ANY DAY OF THE WEEK', fine=None,
   recap=['Luxury product $74.99', 'Your facial FREE'],
   scenes=[('clip:b1', dict(t='hook', words='When was your last facial?', script=None)),
           ('still:c3', dict(t='line', eyebrow='BE HONEST', title='Been too long?', script='treat your skin')),
           ('still:a2', dict(t='price', label='TAKE HOME A LUXURY PRODUCT', num='$74.99')),
           ('still:b3', dict(t='free', lead='+ YOUR FACIAL', sub='ANY DAY · NO CATCH', stamp_sub='ON US')),
           ('web:clinic-01', dict(t='line', eyebrow='MON — SUN', title='Any day of the week.', support='SOLACE SKIN LAB · EL PASO')),
           ('still:b1', dict(t='end'))]),
 3: dict(name='META-03 · Microneedling', cta='MESSAGE US TO LEARN MORE', note='CONSULTATION FIRST', fine='Individual results vary. Consultation required.',
   recap=['Texture', 'Pores', 'Fine lines'],
   scenes=[('clip:c1', dict(t='chips', items=['Texture.', 'Pores.', 'Fine lines.'], words_at=['texture', 'pores', 'fine'])),
           ('still:c2', dict(t='line', eyebrow='AT SOLACE SKIN LAB', title='Meet microneedling.')),
           ('still:c3', dict(t='line', eyebrow='COLLAGEN INDUCTION', title="Your skin's own renewal.", support='WORKS WITH YOUR NATURAL PROCESS')),
           ('nov:d01', dict(t='line', eyebrow='OVER A SERIES OF SESSIONS', title='Smoother-looking texture.', script='step by step')),
           ('still:d3', dict(t='line', eyebrow='EVERY PLAN STARTS WITH', title='An honest consultation.')),
           ('still:c2', dict(t='end'))]),
 4: dict(name='META-04 · Wrinkle relaxer consultation (no brand names)', cta='BOOK A CONSULTATION', note='ONE-ON-ONE WITH OUR INJECTOR', fine='Individual results vary. Medical consultation required.',
   recap=['Softer-looking lines', 'Still you'],
   scenes=[('clip:d2', dict(t='hook', words='Holiday photos', script='are coming.', script_word='coming')),
           ('still:d1', dict(t='line', eyebrow='SOFTEN THE LOOK OF FINE LINES', title='Softer lines.', script='still you')),
           ('nov:d14', dict(t='line', eyebrow='AT SOLACE SKIN LAB', title='Wrinkle relaxers.', support='SUBTLE · REFRESHED · NATURAL-LOOKING')),
           ('still:d3', dict(t='line', eyebrow='IT STARTS WITH', title='A 1-on-1 consultation.', support='WITH OUR INJECTOR')),
           ('still:d2', dict(t='line', eyebrow='YOUR FACE, YOUR GOALS', title='A plan made for you.')),
           ('still:d1', dict(t='end'))]),
 5: dict(name='META-05 · Retargeting "This is your sign"', cta='MESSAGE US TO BOOK', note='BEFORE THE SPOTS FILL UP', fine=None,
   recap=['Any day: product $74.99 + FREE facial', 'Tuesdays: 2 FREE facials + wine'],
   scenes=[('clip:e1', dict(t='hook', words='This is your sign.', script=None)),
           ('still:b1', dict(t='line', eyebrow='FINALLY', title='Book the facial', script="you've been putting off")),
           ('still:a2', dict(t='offer', label='ANY DAY · LUXURY PRODUCT', num='$74.99', stamp='FACIAL FREE')),
           ('still:a1', dict(t='free', eyebrow='TUESDAYS', lead='+ 2 FACIALS', sub='BRING A FRIEND · + WINE')),
           ('still:a4', dict(t='line', eyebrow='CIELO VISTA MALL · EL PASO', title='Solace Skin Lab.')),
           ('still:b3', dict(t='end'))]),
}

LAY = {
 '9x16': dict(W=1080, H=1920, BRAND_T=292, BAND_T=372, BAND_B=None, HOOK=150, TITLE=112, SCRIPT=104, PRICE=230, EYE=24, LEAD=96, STAMP=210,
              END_T=330, END_B=700, LOGO=150, FINE_B=700, SHADE='top'),
 '4x5':  dict(W=1080, H=1350, BRAND_T=54, BAND_T=None, BAND_B=150, HOOK=128, TITLE=98, SCRIPT=92, PRICE=200, EYE=22, LEAD=84, STAMP=184,
              END_T=150, END_B=110, LOGO=136, FINE_B=34, SHADE='bottom'),
}

def media_src(m):
    kind, key = m.split(':')
    if kind == 'clip': return f'{SRC}/clips/{key}.mp4', 'video'
    if kind == 'still': return f'{SRC}/stills/{key}.png', 'img'
    if kind == 'web': return f'/opt/data/solace-skin-lab/website-imagery/v2/raw/{key}.png', 'img'
    if kind == 'nov':
        d = int(key[1:]); pick = json.load(open(f'{NOV}/picks.json')).get(str(d), 1)
        return f'{NOV}/photos/d{d:02d}/v{pick}.png', 'img'

def esc(s): return html.escape(s or '')

def text_block(i, s, c):
    t = s['t']; P = f's{i}'
    if t == 'hook':
        words = ''.join(f'<span class="w">{esc(w)}</span> ' for w in s['words'].split())
        scr = f'<div class="script" id="{P}scr">{esc(s["script"])}</div>' if s.get('script') else ''
        return f'<div class="hook" id="{P}h">{words}</div>{scr}'
    if t == 'chips':
        return ''.join(f'<div class="chip" id="{P}c{k}">{esc(x)}</div>' for k, x in enumerate(s['items']))
    if t == 'price':
        return (f'<div class="eyebrow" id="{P}e"><i></i><span>{esc(s["label"])}</span><i></i></div>'
                f'<div class="price" id="{P}p"><span class="cur">$</span>{esc(s["num"][1:])}</div>')
    if t == 'offer':
        return (f'<div class="eyebrow" id="{P}e"><i></i><span>{esc(s["label"])}</span><i></i></div>'
                f'<div class="offerrow"><div class="price sm" id="{P}p"><span class="cur">$</span>{esc(s["num"][1:])}</div>'
                f'<div class="plus" id="{P}pl">+</div><div class="stamp" id="{P}st"><b>FREE</b><small>FACIAL</small></div></div>')
    if t == 'free':
        eb = f'<div class="eyebrow" id="{P}e"><i></i><span>{esc(s["eyebrow"])}</span><i></i></div>' if s.get('eyebrow') else ''
        return (eb + f'<div class="freerow"><div class="lead" id="{P}l">{esc(s["lead"])}</div>'
                f'<div class="stamp" id="{P}st"><b>FREE</b><small>{s.get("stamp_sub","FOR TWO")}</small></div></div>'
                f'<div class="support" id="{P}u">{esc(s["sub"])}</div>')
    if t == 'line':
        out = f'<div class="eyebrow" id="{P}e"><i></i><span>{esc(s.get("eyebrow"))}</span><i></i></div>' if s.get('eyebrow') else ''
        out += '<div class="title" id="%st">%s</div>' % (P, ''.join(f'<span class="w">{esc(w)}</span> ' for w in s['title'].split()))
        if s.get('script'): out += f'<div class="script" id="{P}scr">{esc(s["script"])}</div>'
        if s.get('support'): out += f'<div class="support" id="{P}u">{esc(s["support"])}</div>'
        return out
    return ''

def word_time(words, w, after):
    for x in words:
        if x['start'] >= after - 0.05 and norm(x['text']).startswith(norm(w)): return x['start']
    return None

def build(ad, fmt):
    A = ADS[ad]; c = LAY[fmt]; W, H = c['W'], c['H']
    proj = f'{ROOT}/ad{ad:02d}_{fmt}'
    if os.path.exists(proj): shutil.rmtree(proj)
    os.makedirs(f'{proj}/assets')
    for f in ('hyperframes.json', 'meta.json', 'package.json'): shutil.copy(f'{TPL}/{f}', proj)
    shutil.copy(f'{SRC}/audio/ad{ad:02d}.wav', f'{proj}/assets/vo.wav')
    words = json.load(open(f'{SRC}/audio/tr_ad{ad:02d}/transcript.json'))
    st, en = line_times(VO[str(ad)], words)
    vo_end = words[-1]['end']
    DUR = round(vo_end + 2.4, 2)
    starts = [0.0] + st[1:]
    ends = starts[1:] + [DUR]
    # media
    media_html, js = [], []
    for i, (m, s) in enumerate(A['scenes']):
        path, kind = media_src(m)
        ext = 'mp4' if kind == 'video' else 'png'
        shutil.copy(path, f'{proj}/assets/m{i}.{ext}')
        a, b = starts[i], ends[i]
        if kind == 'video':
            vd = round(min(5.0, b - a + 0.3), 2)
            inner = f'<video id="v{i}" src="assets/m{i}.mp4" muted playsinline data-start="{a:.2f}" data-duration="{vd}" data-track-index="{10+i}"></video>'
        else:
            inner = f'<img src="assets/m{i}.png" alt="" />'
        media_html.append(f'<div class="media" id="m{i}" data-layout-allow-overflow>{inner}</div>')
        js.append(f'tl.set("#m{i}",{{opacity:1}},{a:.2f});')
        if i: js.append(f'tl.set("#m{i-1}",{{opacity:0}},{a+0.02:.2f});')
        endcard = s['t'] == 'end'
        js.append(f'tl.fromTo("#m{i}",{{scale:{1.22 if i else 1.12}}},{{scale:1.0,duration:{b-a+0.1:.2f},ease:"power2.out",immediateRender:false}},{a:.2f});')
        if i:
            js.append(f'tl.fromTo("#flash",{{opacity:0.4}},{{opacity:0,duration:0.32,ease:"power2.out",immediateRender:false}},{a:.2f});')
    # text blocks
    text_html = []
    for i, (m, s) in enumerate(A['scenes']):
        if s['t'] == 'end': continue
        P = f's{i}'; a, b = starts[i], ends[i]
        text_html.append(f'<div class="band" id="{P}">{text_block(i, s, c)}</div>')
        js.append(f'tl.set("#{P}",{{opacity:1}},{a:.2f});')
        js.append(f'tl.to("#{P}",{{opacity:0,y:-20,duration:0.18,ease:"power1.in"}},{b-0.18:.2f});')
        t = s['t']; t0 = a + (0.12 if i else 0.15)
        if t == 'hook':
            js.append(f'tl.fromTo("#{P}h .w",{{opacity:0,scale:1.7,y:30}},{{opacity:1,scale:1,y:0,duration:0.45,ease:"back.out(1.6)",stagger:0.16,immediateRender:false}},{t0:.2f});')
            if s.get('script'):
                ts = word_time(words, s['script_word'], a) or (a + 0.6 * (en[0] - a))
                js.append(f'tl.fromTo("#{P}scr",{{opacity:0,x:-40,rotation:-3}},{{opacity:1,x:0,rotation:-3,duration:0.7,ease:"power3.out",immediateRender:false}},{ts:.2f});')
        elif t == 'chips':
            for k, w in enumerate(s['words_at']):
                tk = word_time(words, w, a) or (t0 + k * 0.6)
                js.append(f'tl.fromTo("#{P}c{k}",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:0.35,ease:"power4.out",immediateRender:false}},{tk:.2f});')
        elif t in ('price', 'offer'):
            js.append(f'tl.fromTo("#{P}e",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.5,ease:"expo.out",immediateRender:false}},{t0:.2f});')
            js.append(f'tl.fromTo("#{P}e i",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out",immediateRender:false}},{t0+0.1:.2f});')
            tp = word_time(words, 'seventyfour', a) or word_time(words, '74', a) or (t0 + 0.5)
            tp = max(t0 + 0.25, tp - 0.1)
            js.append(f'tl.fromTo("#{P}p",{{opacity:0,scale:1.7}},{{opacity:1,scale:1,duration:0.42,ease:"power4.out",immediateRender:false}},{tp:.2f});')
            js.append(f'tl.fromTo("#{P}p",{{y:0}},{{y:-6,duration:0.12,yoyo:true,repeat:1,ease:"sine.inOut",immediateRender:false}},{tp+0.42:.2f});')
            if t == 'offer':
                tf = word_time(words, 'free', tp) or (tp + 1.2)
                js.append(f'tl.fromTo("#{P}pl",{{opacity:0}},{{opacity:1,duration:0.3,immediateRender:false}},{tf-0.3:.2f});')
                js.append(f'tl.fromTo("#{P}st",{{opacity:0,scale:3,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(1.8)",immediateRender:false}},{tf-0.05:.2f});')
        elif t == 'free':
            if s.get('eyebrow'):
                js.append(f'tl.fromTo("#{P}e",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.5,ease:"expo.out",immediateRender:false}},{t0:.2f});')
                js.append(f'tl.fromTo("#{P}e i",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out",immediateRender:false}},{t0+0.1:.2f});')
            js.append(f'tl.fromTo("#{P}l",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.55,ease:"expo.out",immediateRender:false}},{t0:.2f});')
            tf = word_time(words, 'free', a) or word_time(words, 'facial', a) or (t0 + 0.7)
            tf = max(t0 + 0.35, tf - 0.05)
            js.append(f'tl.fromTo("#{P}st",{{opacity:0,scale:3,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(1.8)",immediateRender:false}},{tf:.2f});')
            js.append(f'tl.fromTo("#{P}u",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.5,ease:"expo.out",immediateRender:false}},{t0+0.35:.2f});')
        elif t == 'line':
            k = t0
            if s.get('eyebrow'):
                js.append(f'tl.fromTo("#{P}e",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.5,ease:"expo.out",immediateRender:false}},{k:.2f});')
                js.append(f'tl.fromTo("#{P}e i",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.out",immediateRender:false}},{k+0.1:.2f});'); k += 0.18
            js.append(f'tl.fromTo("#{P}t .w",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.6,ease:"expo.out",stagger:0.09,immediateRender:false}},{k:.2f});')
            nw = len(s['title'].split())
            if s.get('script'):
                js.append(f'tl.fromTo("#{P}scr",{{opacity:0,x:-40,rotation:-3}},{{opacity:1,x:0,rotation:-3,duration:0.8,ease:"power3.out",immediateRender:false}},{k+0.25+0.09*nw:.2f});')
            if s.get('support'):
                js.append(f'tl.fromTo("#{P}u",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.5,ease:"expo.out",immediateRender:false}},{k+0.35+0.09*nw:.2f});')
    # end card
    ia = len(A['scenes']) - 1; ea = starts[ia]
    recap = ''.join(f'<li id="r{k}">{esc(x)}</li>' for k, x in enumerate(A['recap']))
    end_html = f"""<div class="endcard" id="end">
      <div class="logo" id="elogo"><span class="sl">Solace</span><span class="sk">SKIN LAB</span></div>
      <ul class="recap">{recap}</ul>
      <div class="cta" id="ecta"><span>{esc(A['cta'])}</span><b>→</b></div>
      <div class="note" id="enote">{esc(A['note'])}</div>
      <div class="phone" id="ephone">{PHONE} · CIELO VISTA MALL · EL PASO</div>
    </div>"""
    js.append(f'tl.fromTo("#endshade",{{opacity:0}},{{opacity:1,duration:0.4,ease:"power2.out",immediateRender:false}},{ea:.2f});')
    js.append(f'tl.set("#end",{{opacity:1}},{ea:.2f});')
    js.append(f'tl.fromTo("#elogo",{{opacity:0,scale:0.86}},{{opacity:1,scale:1,duration:0.8,ease:"expo.out",immediateRender:false}},{ea+0.1:.2f});')
    for k in range(len(A['recap'])):
        js.append(f'tl.fromTo("#r{k}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.45,ease:"expo.out",immediateRender:false}},{ea+0.35+0.14*k:.2f});')
    tc = ea + 0.5 + 0.14 * len(A['recap'])
    js.append(f'tl.fromTo("#ecta",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.6,ease:"back.out(1.6)",immediateRender:false}},{tc:.2f});')
    js.append(f'tl.fromTo("#enote",{{opacity:0}},{{opacity:1,duration:0.5,immediateRender:false}},{tc+0.25:.2f});')
    js.append(f'tl.fromTo("#ephone",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.5,ease:"expo.out",immediateRender:false}},{tc+0.35:.2f});')
    js.append(f'tl.fromTo("#ecta",{{scale:1}},{{scale:1.06,duration:0.45,yoyo:true,repeat:3,ease:"sine.inOut",immediateRender:false}},{tc+0.8:.2f});')
    js.append(f'tl.fromTo("#ecta b",{{x:0}},{{x:10,duration:0.45,yoyo:true,repeat:3,ease:"sine.inOut",immediateRender:false}},{tc+0.8:.2f});')
    fine = f'<div class="fine" id="fine">{esc(A["fine"])}</div>' if A['fine'] else ''
    if fine: js.append('tl.fromTo("#fine",{opacity:0},{opacity:1,duration:0.6,immediateRender:false},0.5);')
    js.insert(0, 'tl.fromTo("#brand",{opacity:0,y:-10},{opacity:1,y:0,duration:0.8,ease:"expo.out",immediateRender:false},0.2);')
    js.insert(0, 'tl.fromTo("#frame",{opacity:0,scale:1.03},{opacity:1,scale:1,duration:1.0,ease:"expo.out",immediateRender:false},0.1);')
    js.append(f'tl.to("#brand",{{opacity:0,duration:0.3}},{ea:.2f});')
    # ---- css
    band_pos = f'top:{c["BAND_T"]}px;' if c['BAND_T'] else f'bottom:{c["BAND_B"]}px;'
    shade = ('linear-gradient(180deg, rgba(10,7,5,.88) 0%, rgba(10,7,5,.72) 30%, rgba(10,7,5,.15) 48%, rgba(10,7,5,0) 60%), linear-gradient(0deg, rgba(10,7,5,.55) 0%, rgba(10,7,5,0) 30%)'
             if c['SHADE'] == 'top' else
             'linear-gradient(0deg, rgba(10,7,5,.92) 0%, rgba(10,7,5,.78) 30%, rgba(10,7,5,.2) 52%, rgba(10,7,5,0) 64%), linear-gradient(180deg, rgba(10,7,5,.6) 0%, rgba(10,7,5,0) 14%)')
    end_justify = (f'justify-content:flex-start; padding-top:{c["END_T"]}px;' if fmt == '9x16' else f'justify-content:center; padding-top:{c["END_T"]}px; padding-bottom:{c["END_B"]}px;')
    css = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0b0806; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; color:#F6EFE4; font-family:Jost,sans-serif; }}
.media {{ position:absolute; inset:0; overflow:hidden; opacity:0; }}
.media img, .media video {{ width:100%; height:100%; object-fit:cover; object-position:50% 46%; display:block; }}
.shade {{ position:absolute; inset:0; background:{shade}; }}
.grain {{ position:absolute; inset:0; opacity:.07; background-image:radial-gradient(rgba(255,255,255,.5) 1px, transparent 1px); background-size:3px 3px; mix-blend-mode:overlay; }}
#flash {{ position:absolute; inset:0; background:#FFF4DE; opacity:0; }}
.frame {{ position:absolute; inset:24px; border:1px solid rgba(216,190,138,.35); opacity:0; }}
.brand {{ position:absolute; top:{c['BRAND_T']}px; left:0; right:0; text-align:center; font:500 20px/1 Jost,sans-serif; letter-spacing:.44em; color:rgba(246,239,228,.85); opacity:0; }}
.brand b {{ color:#D8BE8A; font-weight:500; }}
.band {{ position:absolute; left:64px; right:64px; {band_pos} display:flex; flex-direction:column; align-items:center; text-align:center; opacity:0; }}
.hook {{ font:600 {c['HOOK']}px/0.98 "Cormorant Garamond",serif; letter-spacing:-.015em; text-shadow:0 4px 30px rgba(0,0,0,.6); }}
.hook .w, .title .w {{ display:inline-block; opacity:0; }}
.title {{ margin-top:16px; font:500 {c['TITLE']}px/1.0 "Cormorant Garamond",serif; letter-spacing:-.01em; text-shadow:0 4px 26px rgba(0,0,0,.55); }}
.script {{ margin-top:2px; font:400 {c['SCRIPT']}px/1.15 "Pinyon Script",cursive; color:#EBD39E; opacity:0; text-shadow:0 2px 18px rgba(0,0,0,.6); }}
.eyebrow {{ display:flex; align-items:center; gap:18px; font:500 {c['EYE']}px/1.2 Jost,sans-serif; letter-spacing:.32em; color:#D8BE8A; opacity:0; text-shadow:0 2px 10px rgba(0,0,0,.8); }}
.eyebrow i {{ display:block; width:56px; height:1px; background:#D8BE8A; transform:scaleX(0); }}
.support {{ margin-top:18px; font:500 {c['EYE']}px/1.35 Jost,sans-serif; letter-spacing:.24em; color:rgba(246,239,228,.92); opacity:0; text-shadow:0 2px 10px rgba(0,0,0,.85); }}
.price {{ margin-top:40px; font:600 {c['PRICE']}px/1 "Cormorant Garamond",serif; color:#E8CF95; letter-spacing:-.02em; opacity:0; text-shadow:0 0 40px rgba(232,207,149,.35), 0 6px 30px rgba(0,0,0,.7); }}
.price.sm {{ font-size:{int(c['PRICE']*0.72)}px; margin-top:0; }}
.price .cur {{ font-size:.5em; position:relative; top:-.72em; margin-right:4px; }}
.offerrow, .freerow {{ display:flex; align-items:center; justify-content:center; gap:26px; margin-top:12px; }}
.plus {{ font:500 {int(c['LEAD']*0.9)}px/1 "Cormorant Garamond",serif; color:#F6EFE4; opacity:0; }}
.lead {{ font:600 {c['LEAD']}px/1 "Cormorant Garamond",serif; letter-spacing:-.01em; opacity:0; text-shadow:0 4px 24px rgba(0,0,0,.6); white-space:nowrap; }}
.stamp {{ flex:none; width:{c['STAMP']}px; height:{c['STAMP']}px; border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center; opacity:0;
  background:radial-gradient(circle at 35% 30%, #F4E3B8, #D3B06E 55%, #A9844A); color:#1a120b; box-shadow:0 0 0 6px rgba(216,190,138,.25), 0 10px 40px rgba(0,0,0,.55); }}
.stamp b {{ font:700 {int(c['STAMP']*0.34)}px/1 "Cormorant Garamond",serif; letter-spacing:.02em; }}
.stamp small {{ font:600 {int(c['STAMP']*0.085)}px/1 Jost,sans-serif; letter-spacing:.3em; margin-top:6px; }}
.chip {{ font:600 {c['HOOK']}px/1.02 "Cormorant Garamond",serif; letter-spacing:-.015em; opacity:0; text-shadow:0 4px 30px rgba(0,0,0,.6); }}
.chip:nth-child(2) {{ color:#EBD39E; }}
#endshade {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 45%, rgba(12,8,6,.72) 0%, rgba(12,8,6,.9) 70%); opacity:0; }}
.endcard {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; {end_justify} opacity:0; }}
.logo {{ display:flex; flex-direction:column; align-items:center; }}
.logo .sl {{ font:500 {c['LOGO']}px/0.9 "Cormorant Garamond",serif; letter-spacing:.01em; }}
.logo .sk {{ margin-top:10px; font:500 22px/1 Jost,sans-serif; letter-spacing:.6em; color:#D8BE8A; padding-left:.6em; }}
.recap {{ list-style:none; margin-top:36px; display:flex; flex-direction:column; align-items:center; gap:12px; }}
.recap li {{ font:500 {int(c['EYE']*1.45)}px/1.2 Jost,sans-serif; letter-spacing:.06em; color:#F6EFE4; opacity:0; }}
.recap li::before {{ content:"✦"; color:#D8BE8A; margin-right:14px; font-size:.8em; }}
.cta {{ margin-top:40px; display:flex; align-items:center; gap:18px; font:600 {int(c['EYE']*1.1)}px/1 Jost,sans-serif; letter-spacing:.2em; color:#1a120c;
  background:linear-gradient(90deg,#CFAF74,#EFDDAF,#CFAF74); padding:24px 40px; border-radius:999px; opacity:0; box-shadow:0 10px 40px rgba(207,175,116,.35); }}
.cta b {{ display:inline-block; font-size:1.2em; }}
.note {{ margin-top:22px; font:500 {c['EYE']}px/1 Jost,sans-serif; letter-spacing:.3em; color:#EBD39E; opacity:0; }}
.phone {{ margin-top:16px; font:400 {int(c['EYE']*0.95)}px/1 Jost,sans-serif; letter-spacing:.16em; color:rgba(246,239,228,.85); opacity:0; }}
.fine {{ position:absolute; left:0; right:0; bottom:{c['FINE_B']}px; text-align:center; font:400 17px/1 Jost,sans-serif; letter-spacing:.1em; color:rgba(246,239,228,.92); text-shadow:0 0 6px rgba(0,0,0,.95), 0 1px 3px rgba(0,0,0,.95); opacity:0; }}
"""
    body = f"""
  <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
    {''.join(media_html)}
    <div class="shade"></div>
    <div class="grain"></div>
    <div id="endshade"></div>
    <div id="flash"></div>
    <div class="frame" id="frame"></div>
    <div class="brand" id="brand">SOLACE <b>·</b> SKIN LAB</div>
    {''.join(text_html)}
    {end_html}
    {fine}
    <audio id="vo" src="assets/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="1"></audio>
    <audio id="music" src="assets/music.wav" data-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
  </div>"""
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Pinyon+Script&family=Jost:wght@400;500;600&display=block" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{css}</style></head>
<body>{body}
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
    open(f'{proj}/index.html', 'w').write(page)
    # music bed + SFX (cuts = whoosh, price/stamp = boom)
    cuts = starts[1:]
    make_music(proj, DUR, ad, cuts)
    json.dump(dict(ad=ad, fmt=fmt, dur=DUR, starts=starts, vo_end=vo_end), open(f'{proj}/build.json', 'w'))
    return proj, DUR, starts

def make_music(proj, DUR, ad, cuts):
    M = f'{NOV}/music/cv_B.mp3'
    sfx = f'{ROOT}/sfx'
    os.makedirs(sfx, exist_ok=True)
    if not os.path.exists(f'{sfx}/whoosh.wav'):
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'anoisesrc=d=0.5:c=pink:a=0.6:r=48000',
                        '-af', 'highpass=f=500,lowpass=f=7000,afade=t=in:d=0.32:curve=exp,afade=t=out:st=0.32:d=0.18,volume=0.5', '-ac', '2', f'{sfx}/whoosh.wav'], check=True)
    off = {1: 8, 2: 20, 3: 34, 4: 48, 5: 62}[ad]
    fo = max(0, DUR - 1.6)
    inputs = ['-ss', str(off), '-i', M]
    fc = [f'[0:a]aresample=48000,loudnorm=I=-23:TP=-3,volume=0.62,afade=t=in:d=0.4,afade=t=out:st={fo:.2f}:d=1.6,atrim=0:{DUR}[m]']
    labels = ['[m]']
    for k, t in enumerate(cuts):
        inputs += ['-i', f'{sfx}/whoosh.wav']
        d = max(0, int((t - 0.3) * 1000))
        fc.append(f'[{k+1}:a]adelay={d}|{d}[w{k}]'); labels.append(f'[w{k}]')
    fc.append(f'{"".join(labels)}amix=inputs={len(labels)}:duration=first:normalize=0,atrim=0:{DUR}[a]')
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', '[a]', '-ac', '2', '-ar', '48000', f'{proj}/assets/music.wav'], check=True)

if __name__ == '__main__':
    ad, fmt = int(sys.argv[1]), sys.argv[2]
    proj, dur, st = build(ad, fmt)
    print(proj, dur, [round(x, 2) for x in st])
