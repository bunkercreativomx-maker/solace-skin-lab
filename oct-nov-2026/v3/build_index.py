"""Derive oct-nov-2026-v3/index.html from the Oct-Nov portal (same look + same PocketBase save path)."""
import re
from pathlib import Path
SRC = Path('/opt/data/solace-skin-lab/oct-nov-2026/index.html')
OUT = Path('/opt/data/solace-skin-lab/oct-nov-2026-v3/index.html')
s = SRC.read_text()

def sub(old, new, count=1):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, count)

sub("const BUNKER_CAMPAIGN='oct-nov-2026';", "const BUNKER_CAMPAIGN='oct-nov-2026-v3';")
s = s.replace("'solace_octnov_review'", "'solace_octnov_v3_review'")
sub("const DATA_URL='calendar_2026-10-16_to_2026-11-14.json';", "const DATA_URL='calendar_v3.json?v=1';")
sub("const ADS_URL='facebook_ads_2026-10-16_to_2026-11-14.json';", "const ADS_URL='../oct-nov-2026/facebook_ads_2026-10-16_to_2026-11-14.json';")

# media: client's own photo or video
old_img = re.search(r"`<img loading=\"lazy\" src=\"images/day\$\{String\(p\.day\)\.padStart\(2,'0'\)\}\.png\?v=2\" alt=\"Day \$\{p\.day\}: \$\{esc\(p\.title\)\}\" data-full=\"images/day\$\{String\(p\.day\)\.padStart\(2,'0'\)\}\.png\?v=2\">`", s).group(0)
sub(old_img, "mediaTag(p)")
# client request + what we did, above the copy
sub('<div class="content"><h3>${esc(p.title)}</h3>',
    '<div class="content"><h3>${esc(p.title)}</h3>${p.clientNote?`<div class="req"><b>YOUR REQUEST</b><p>${linkify(p.clientNote)}</p><b>WHAT WE DID</b><p>${esc(p.editNote||"")}</p></div>`:""}')
sub("function render(){", """function linkify(t){return esc(t).replace(/(https?:\\/\\/[^\\s<]+)/g,'<a href="$1" target="_blank" rel="noopener">reference link ↗</a>').replace(/\\n/g,'<br>')}
function mediaTag(p){const v=String(p.media||'')+'?v=1';if(p.mediaType==='video'){const poster=String(p.media).replace('.mp4','_poster.jpg');return `<video src="${v}" poster="${poster}" controls playsinline preload="none" style="width:100%;display:block;background:#000;aspect-ratio:9/16;object-fit:contain"></video>`}return `<img loading="lazy" src="${v}" alt="Day ${p.day}: ${esc(p.title)}" data-full="${v}" style="width:100%;display:block">`}
function render(){""")
# hero / notes copy
sub(re.search(r'<section class="hero">.*?</section>', s, re.S).group(0), """<section class="hero"><div><div class="eyebrow">VERSION 3 · DAYS 4–30 · YOUR PHOTOS &amp; VIDEOS</div><h1>Your references.<em>Your requests, post by post.</em></h1><p>We rebuilt every post with <strong>the photos and videos you chose</strong> — used as they are. We only removed what you asked (other brands' logos, websites and endings). Prices updated to <strong>$74.99</strong> and <strong>2 facials for $74.99 on Tuesdays</strong>. Under each post you'll see <strong>your request</strong> and <strong>what we did</strong>. Approve or request changes — everything saves automatically.</p></div><div class="hero-side"><div class="metric"><b>27</b><span>posts (days 4–30)</span></div><div class="metric"><b>$74.99</b><span>facial price</span></div><div class="metric"><b>4</b><span>2-for-$74.99 Tuesdays</span></div><div class="metric"><b>10</b><span>videos</span></div></div></section>""")
s = re.sub(r'<div class="promo-note"><strong>Offers in this campaign:</strong>.*?</div>',
           '<div class="promo-note"><strong>Offers:</strong> <strong>Facials $74.99</strong> · <strong>Tuesdays: 2 facials for $74.99 total</strong> (Oct 20, 27 · Nov 3, 10). Botox® Cosmetic &amp; Xeomin® · Juvéderm® &amp; Belotero® (0.55 ml / 1 ml) · GLP-1 &amp; peptides. Official phone <strong>(915) 209-2060</strong>.</div>', s, count=1, flags=re.S)
s = re.sub(r'<div class="promo-note"><strong>Please confirm before publishing:</strong>.*?</div>',
           '<div class="promo-note"><strong>Please confirm:</strong> GLP-1 / peptide posts (6, 13, 20, 27) are informational and always say a medical consultation comes first. Meta ads will be updated to the new prices once these posts are approved.</div>', s, count=1, flags=re.S)
# hide old ads section (prices/creatives belong to the previous version)
sub('<section class="ads-section" id="meta-ads">', '<section class="ads-section" id="meta-ads" style="display:none">')
sub('</style>', '.req{background:#fbf4ee;border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:8px 0 12px;font-size:12.5px;line-height:1.5}.req b{display:block;font-size:10px;letter-spacing:.14em;color:var(--rose);margin-top:4px}.req p{margin:2px 0 6px;color:var(--ink)}.req a{color:var(--rose)}</style>')
sub('<title>', '<title>V3 · ')
OUT.write_text(s)
print('ok', len(s))
