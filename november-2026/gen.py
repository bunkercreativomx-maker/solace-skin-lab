#!/usr/bin/env python3
"""Solace Skin Lab · November 2026 — 30 HyperFrames projects (Artistly photo + CloneVoice EN + motion type).
usage: gen.py [day ...]"""
import json, os, re, shutil, subprocess, sys, difflib, html
SRC = '/opt/data/solace-skin-lab/november-2026'
sys.path.insert(0, SRC)
from spec import POSTS, PHONE
ROOT = '/opt/data/hyperframes/solace-nov'
TPL = '/opt/data/hyperframes/dp-fb-d01-45'
PICK = json.load(open(f'{SRC}/picks.json')) if os.path.exists(f'{SRC}/picks.json') else {}
OVR = json.load(open(f'{SRC}/overrides.json')) if os.path.exists(f'{SRC}/overrides.json') else {}
FINE = {'Microneedling', 'BOTOX®', 'Lip filler', 'Myth: BOTOX®', 'Peptides', 'Men: acne scars', 'BOTOX® timing', 'LED face & body',
        'Derma Jade Eye Solution', 'Salmon DNA 2×1', 'Thermal Anti-Aging Lifting', 'GLP-1', 'Microneedling (hair)', 'Jawline', 'Salmon PDRN Facial'}

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

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:%(W)dpx; height:%(H)dpx; overflow:hidden; background:#0d0907; }
#root { position:relative; width:%(W)dpx; height:%(H)dpx; overflow:hidden; color:#F6EFE4; font-family:Jost,sans-serif; }
.bg { position:absolute; inset:0; overflow:hidden; }
.bg img { width:100%%; height:100%%; object-fit:cover; object-position:%(OBJPOS)s; transform-origin:50%% 70%%; }
.shade { position:absolute; inset:0; background:
  linear-gradient(180deg, rgba(12,8,6,.92) 0%%, rgba(12,8,6,.78) %(S1)d%%, rgba(12,8,6,.25) %(S2)d%%, rgba(12,8,6,0) %(S3)d%%),
  linear-gradient(0deg, rgba(12,8,6,.92) 0%%, rgba(12,8,6,.6) 14%%, rgba(12,8,6,0) 30%%); }
.frame { position:absolute; inset:26px; border:1px solid rgba(216,190,138,.38); opacity:0; }
.brand { position:absolute; top:58px; left:0; right:0; text-align:center; font:500 19px/1 Jost,sans-serif; letter-spacing:.42em; color:rgba(246,239,228,.82); opacity:0; }
.brand b { color:#D8BE8A; font-weight:500; }
.copy { position:absolute; left:70px; right:70px; top:%(TOP)dpx; display:flex; flex-direction:column; align-items:center; text-align:center; }
.eyebrow { display:flex; align-items:center; gap:18px; font:500 %(EYE)dpx/1.2 Jost,sans-serif; letter-spacing:.32em; color:#D8BE8A; opacity:0; }
.eyebrow i { display:block; width:54px; height:1px; background:#D8BE8A; transform:scaleX(0); }
.title { margin-top:%(TGAP)dpx; font:500 %(TS)dpx/1.0 "Cormorant Garamond",serif; letter-spacing:-.01em; }
.title .w { display:inline-block; opacity:0; }
.script { margin-top:%(SGAP)dpx; font:400 %(SS)dpx/1.1 "Pinyon Script",cursive; color:#EBD39E; opacity:0; transform:rotate(-3deg); text-shadow:0 2px 18px rgba(0,0,0,.55); }
.support { margin-top:%(UGAP)dpx; font:400 %(US)dpx/1.35 Jost,sans-serif; letter-spacing:.14em; text-transform:uppercase; color:rgba(246,239,228,.9); opacity:0; max-width:%(UW)dpx; }
.price { margin-top:%(PGAP)dpx; display:flex; align-items:center; gap:16px; opacity:0; padding:10px 26px; border-radius:16px; background:radial-gradient(ellipse at center, rgba(12,8,6,.78) 0%%, rgba(12,8,6,.55) 60%%, rgba(12,8,6,0) 100%%); }
.price .lbl, .price .num { text-shadow:0 0 12px rgba(0,0,0,.95), 0 0 3px rgba(0,0,0,.9); }
.price .lbl { font:500 %(PL)dpx/1.35 Jost,sans-serif; letter-spacing:.3em; color:rgba(246,239,228,.8); text-align:right; }
.price .num { font:600 %(PS)dpx/1 "Cormorant Garamond",serif; color:#E2C88F; letter-spacing:-.01em; }
.foot { position:absolute; left:0; right:0; bottom:%(FB)dpx; display:flex; flex-direction:column; align-items:center; gap:22px; }
.cta { font:500 %(CS)dpx/1 Jost,sans-serif; letter-spacing:.24em; text-transform:uppercase; color:#1a120c; background:linear-gradient(90deg,#CFAF74,#E8D3A2,#CFAF74); padding:18px 34px; border-radius:999px; opacity:0; }
.phone { font:400 %(PH)dpx/1 Jost,sans-serif; letter-spacing:.18em; color:#F6EFE4; opacity:0; }
.offer { display:flex; align-items:center; gap:14px; padding:8px 30px; border-radius:30px; background:radial-gradient(ellipse at center, rgba(12,8,6,.85) 0%%, rgba(12,8,6,.6) 65%%, rgba(12,8,6,0) 100%%); font:500 %(OF)dpx/1.2 Jost,sans-serif; letter-spacing:.2em; color:#EBD39E; opacity:0; text-shadow:0 2px 12px rgba(0,0,0,.6); }
.offer i { display:block; width:36px; height:1px; background:#D8BE8A; }
.fine { position:absolute; left:0; right:0; bottom:%(FINEB)dpx; text-align:center; font:400 15px/1 Jost,sans-serif; letter-spacing:.12em; color:rgba(246,239,228,.6); opacity:0; }
"""
LAY = {
 '4x5': dict(W=1080, H=1350, OBJPOS='50% 60%', S1=24, S2=46, S3=60, TOP=140, EYE=21, TGAP=26, TS=112, SGAP=-2, SS=100, UGAP=18, US=22, UW=820, PGAP=14, PS=118, PL=17, FB=74, CS=22, PH=26, FINEB=40, OF=19),
 '1x1': dict(W=1080, H=1080, OBJPOS='50% 62%', S1=22, S2=44, S3=58, TOP=118, EYE=19, TGAP=20, TS=92, SGAP=-2, SS=84, UGAP=12, US=19, UW=780, PGAP=8, PS=96, PL=15, FB=58, CS=19, PH=22, FINEB=30, OF=16),
}

def build(p):
    d, fmt = p['d'], p['fmt']
    proj = f'{ROOT}/d{d:02d}'
    os.makedirs(f'{proj}/assets', exist_ok=True)
    for f in ('hyperframes.json', 'meta.json', 'package.json'): shutil.copy(f'{TPL}/{f}', proj)
    v = PICK.get(str(d), 1)
    shutil.copy(f'{SRC}/photos/d{d:02d}/v{v}.png', f'{proj}/assets/photo.png')
    shutil.copy(f'{SRC}/audio/d{d:02d}.wav', f'{proj}/assets/vo.wav')
    words = json.load(open(f'{SRC}/audio/tr_d{d:02d}/transcript.json'))
    dur_audio = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{proj}/assets/vo.wav']).decode())
    DUR = round(dur_audio + 1.6, 2)
    subprocess.run(['/opt/data/hyperframes/.venv-tts/bin/python', f'{ROOT}/ambient.py', str(DUR), f'{proj}/assets/music.wav', str(d)], check=True, capture_output=True)
    st, en = line_times(p['vo'], words)
    c = dict(LAY[fmt]); c.update({k.upper(): v for k, v in OVR.get(str(d), {}).items() if k.upper() in c})
    n = len(p['title'])
    if n > 16: c['TS'] = int(c['TS'] * (0.86 if n <= 22 else 0.74))
    css = CSS % c
    price = p.get('price')
    lbl, num = ('FROM', price.replace('from ', '')) if price and price.startswith('from') else ('ONLY', price)
    if p['service'].startswith('2×1'): lbl = 'BOTH<br>FOR'
    if p.get('plabel'): lbl = p['plabel']
    title = ' '.join(f'<span class="w">{html.escape(w)}</span>' for w in p['title'].split())
    fine = ('<div class="fine" id="fine">' + ('Prescription & medical consultation required. Results vary.' if p['service']=='GLP-1' else 'Individual results vary. Consultation required.') + '</div>') if p['service'] in FINE else ''
    pblock = f'<div class="price" id="price"><div class="lbl">{lbl}</div><div class="num">{html.escape(num)}</div></div>' if price else ''
    endnote = f'<div class="offer" id="offer"><i></i><span>{html.escape(p["endnote"])}</span><i></i></div>' if p.get('endnote') else ''
    body = f"""
  <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{c['W']}" data-height="{c['H']}">
    <div class="bg" data-layout-allow-overflow><img id="photo" src="assets/photo.png" alt="" /></div>
    <div class="shade"></div>
    <div class="frame" id="frame"></div>
    <div class="brand" id="brand">SOLACE <b>·</b> SKIN LAB</div>
    <div class="copy">
      <div class="eyebrow" id="eyebrow"><i></i><span>{html.escape(p['eyebrow'])}</span><i></i></div>
      <div class="title" id="title">{title}</div>
      <div class="script" id="script">{html.escape(p['script'])}</div>
      <div class="support" id="support">{html.escape(p['support'])}</div>
      {pblock}
    </div>
    <div class="foot">{endnote}<div class="cta" id="cta">{html.escape(p['cta'])}</div><div class="phone" id="phone">{PHONE} · CIELO VISTA MALL</div></div>
    {fine}
    <audio id="vo" src="assets/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="1"></audio>
    <audio id="music" src="assets/music.wav" data-start="0" data-duration="{DUR}" data-track-index="2" data-volume="0.16"></audio>
  </div>"""
    t0, t1, t2, t3, t4 = st
    l1 = max(0.5, en[1] - st[1])
    js = [f'tl.fromTo("#photo",{{scale:1.12}},{{scale:1.0,duration:{DUR},ease:"none"}},0);',
          'IN("#frame",0.05,{opacity:0,scale:1.02},1.2);',
          'IN("#brand",0.15,{opacity:0,y:-12},0.9);',
          f'IN("#eyebrow",{max(0.3, t0):.2f});',
          f'tl.fromTo("#eyebrow i",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"power2.out",immediateRender:false}},{max(0.3, t0)+0.15:.2f});',
          f'tl.fromTo("#title .w",{{opacity:0,y:34}},{{opacity:1,y:0,duration:0.8,ease:E,stagger:0.12,immediateRender:false}},{t1:.2f});',
          f'tl.fromTo("#script",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:1.0,ease:"power2.out",immediateRender:false}},{t1 + l1*0.7:.2f});',
          f'IN("#support",{t2:.2f},{{opacity:0,y:16}},0.8);']
    if price:
        js.append(f'tl.fromTo("#price",{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:0.8,ease:"power3.out",immediateRender:false}},{t3:.2f});')
    if fine: js.append(f'IN("#fine",{t2:.2f},{{opacity:0}},0.8);')
    if p.get('endnote'): js.append(f'IN("#offer",{t4:.2f},{{opacity:0,y:14}},0.8);')
    js.append(f'IN("#cta",{t4 + (0.5 if p.get("endnote") else 0):.2f},{{opacity:0,y:18}},0.7);')
    js.append(f'IN("#phone",{t4 + 0.25:.2f},{{opacity:0,y:12}},0.7);')
    js.append(f'tl.fromTo("#cta",{{scale:1}},{{scale:1.04,duration:0.6,yoyo:true,repeat:1,ease:"sine.inOut",immediateRender:false}},{t4 + 1.0:.2f});')
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={c['W']}, height={c['H']}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Pinyon+Script&family=Jost:wght@400;500&display=block" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{css}</style>
</head>
<body>{body}
<script>
const tl = gsap.timeline({{ paused: true }});
const E = "expo.out";
const IN = (sel, t, from = {{ opacity: 0, y: 18 }}, d = 0.7) => tl.fromTo(sel, from, {{ opacity: 1, y: 0, x: 0, scale: 1, duration: d, ease: E, immediateRender: false }}, t);
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>"""
    open(f'{proj}/index.html', 'w').write(page)
    json.dump(dict(d=d, fmt=fmt, dur=DUR, starts=st, ends=en, pick=v), open(f'{proj}/build.json', 'w'))
    return proj, DUR, st

if __name__ == '__main__':
    days = [int(x) for x in sys.argv[1:]] or [p['d'] for p in POSTS]
    for p in POSTS:
        if p['d'] in days:
            proj, dur, st = build(p); print(p['d'], p['fmt'], dur, [round(x, 2) for x in st])
