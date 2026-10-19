#!/usr/bin/env python3
"""Client approval portal for Solace November 2026 (based on oct-nov-2026-v3 portal)."""
import json, re, sys, datetime
sys.path.insert(0, '/opt/data/solace-skin-lab/november-2026')
from spec import POSTS
B = '/opt/data/solace-skin-lab'
OUT = f'{B}/november-2026/review'
V = sys.argv[1] if len(sys.argv) > 1 else '1'
cal = []
for p in POSTS:
    lines = p['caption'].split('\n')
    cal.append(dict(day=p['d'], date=datetime.date.fromisoformat(p['date']).strftime('%a, %b %d').replace(' 0', ' '), isoDate=p['date'],
        type=p['service'], title=p['title'] + ' ' + p['script'], hook=lines[0], body='\n'.join(lines[1:]).strip(), desire='', cta='',
        hashtags=p['tags'], media=f"media/day{p['d']:02d}.mp4", poster=f"media/day{p['d']:02d}.png", mediaType='video',
        aspect='4/5' if p['fmt'] == '4x5' else '1/1', format='4:5' if p['fmt'] == '4x5' else '1:1'))
json.dump(cal, open(f'{OUT}/calendar.json', 'w'), indent=1, ensure_ascii=False)

h = open(f'{B}/oct-nov-2026-v3/index.html').read()
def sub(old, new, count=1, regex=False):
    global h
    n = len(re.findall(old, h, flags=re.S)) if regex else h.count(old)
    assert n >= 1, old[:60]
    h = re.sub(old, new, h, count=count, flags=re.S) if regex else h.replace(old, new, count if count else -1)
sub(r'<title>.*?</title>', '<title>Solace Skin Lab — November 2026 Content Review</title>', regex=True)
sub('Oct 16 – Nov 14, 2026 · Cielo Vista Mall', 'Nov 2 – Dec 1, 2026 · Cielo Vista Mall')
sub(r'<section class="hero">.*?</section>', '<section class="hero"><div><div class="eyebrow">NOVEMBER 2026 · 30 ANIMATED POSTS</div><h1>Your November.<em>Every post, in motion.</em></h1>'
    '<p>30 Facebook posts for <strong>Nov 2 – Dec 1</strong>. Every post is a short <strong>animated video with English voice-over</strong> (press play to listen), and it can also be posted as a still image. '
    '15 posts are vertical <strong>4:5</strong> and 15 are square <strong>1:1</strong>. Approve or request changes on each post — everything saves automatically. When you finish, press <strong>“Enviar a Bunker”</strong>.</p></div>'
    '<div class="hero-side"><div class="metric"><b>30</b><span>animated posts</span></div><div class="metric"><b>$74.99</b><span>facial price</span></div><div class="metric"><b>5</b><span>2-for-$74.99 Tuesdays</span></div><div class="metric"><b>15 + 15</b><span>4:5 and 1:1</span></div></div></section>', regex=True)
notes = re.findall(r'<div class="promo-note".*?</div>', h, flags=re.S)
sub(notes[0], '<div class="promo-note"><strong>Offers used:</strong> Tuesdays: <strong>2 facials for $74.99 total + a glass of wine</strong> (Nov 3, 10, 17, 24 · Dec 1) · <strong>Luxury product $74.99 + FREE facial</strong> · <strong>Salmon DNA 2×1</strong> · <strong>LED face &amp; body from $79.99</strong> · Facial $74.99. Official phone <strong>(915) 209-2060</strong>.</div>')
sub(notes[1], '<div class="promo-note"><strong>Please confirm:</strong> Black Friday (Nov 27) uses the current offer <strong>luxury product $74.99 + FREE facial</strong>. If you want a different Black Friday promo, tell us in that post’s notes. Holidays included: Veterans Day, Thanksgiving and Small Business Saturday.</div>')
sub("const DATA_URL='calendar_v3.json?v=2';", f"const DATA_URL='calendar.json?v={V}';")
sub("Promise.all([DATA_URL,ADS_URL].map(", "Promise.all([DATA_URL].map(")
sub("const BUNKER_CAMPAIGN='oct-nov-2026-v3';", "const BUNKER_CAMPAIGN='nov-2026';")
sub("solace_octnov_v3_review", "solace_nov2026_review", count=0)
sub('<script src="../photo-uploads.js?v=1"></script>', '<script src="../../photo-uploads.js?v=1"></script>')
# media: video with its own aspect + poster, plus still-image link
sub(r"function mediaTag\(p\)\{.*?\n", "function mediaTag(p){const v=String(p.media)+'?v=" + V + "',po=String(p.poster)+'?v=" + V + "';return `<video src=\"${v}\" poster=\"${po}\" controls playsinline preload=\"none\" style=\"width:100%;display:block;background:#000;aspect-ratio:${p.aspect};object-fit:contain\"></video><div style=\"display:flex;justify-content:space-between;padding:6px 12px;font-size:12px;color:var(--muted)\"><span>Format ${p.format} · ▶ press play for sound</span><a href=\"${po}\" target=\"_blank\" style=\"color:var(--rose)\">Still image</a></div>`}\n", regex=True)
sub("function field(p,key,label){return ", "function field(p,key,label){if(!edited(p,key))return '';return ")
sub("Solace Skin Lab — Oct 16–Nov 14 Content Review", "Solace Skin Lab — November 2026 Content Review")
sub("campaign:'Client Ideas Oct-Nov',period:'2026-10-16 to 2026-11-14'", "campaign:'November 2026',period:'2026-11-02 to 2026-12-01'")
sub("image:`images/day${String(p.day).padStart(2,'0')}.png`", "image:p.poster")
sub("solace-oct-nov-2026-client-review.json", "solace-nov-2026-client-review.json")
sub('<span class="pill ok">${aa} ads approved</span><span class="pill skip">${as} ads changes</span><span class="pill">${an} ads pending</span>`', '`')
assert 'oct-nov-2026-v3' not in h
open(f'{OUT}/index.html', 'w').write(h)
print('ok', len(cal))
