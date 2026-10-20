#!/usr/bin/env python3
"""Build GH Pages review/download page for the Solace video ads -> <repo>/ads-video-nov-2026/index.html"""
import json, html, shutil, os
SRC = '/opt/data/solace-skin-lab/ads-video-nov-2026'
OUT = '/opt/data/hyperframes/solace-ads/final'
C = json.load(open(f'{SRC}/ads_copy.json'))
os.makedirs(f'{SRC}/videos', exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.mp4'): shutil.copy(f'{OUT}/{f}', f'{SRC}/videos/{f}')
e = html.escape
files, secs = [], []
for i, a in enumerate(C['ads'], 1):
    vids = ''
    for fmt, lab in (('9x16', '9:16 · Reels / Stories'), ('4x5', '4:5 · Feed')):
        fn = f"{a['file']}_{fmt}.mp4"; zipn = f"{i:02d}_{a['id']}_{fmt}.mp4"
        files.append([f'videos/{fn}', zipn])
        vids += f'<figure><video src="videos/{fn}?v=1" controls playsinline preload="metadata"></video><figcaption>{lab} · <a href="videos/{fn}" download="{zipn}">Descargar</a></figcaption></figure>'
    def fld(k, lab):
        return f'<div class="f"><b>{lab}</b><button onclick="cp(this)">Copiar</button><pre>{e(a[k])}</pre></div>'
    secs.append(f"""<section><h2>{e(a['id'])} · {e(a['name'])}</h2>
<p class="m">{e(a['objective'])} · CTA: {e(a['cta'])} · {e(a['schedule'])}<br>Público: {e(a['audience'])}</p>
<div class="vids">{vids}</div>
{fld('primaryTextA','Texto principal A')}{fld('primaryTextB','Texto principal B')}{fld('headlineA','Título A')}{fld('headlineB','Título B')}{fld('description','Descripción')}
</section>""")
copytxt = '\n\n'.join(f"{a['id']} — {a['name']}\nPrimary A: {a['primaryTextA']}\nPrimary B: {a['primaryTextB']}\nHeadline A: {a['headlineA']}\nHeadline B: {a['headlineB']}\nDescription: {a['description']}\nCTA: {a['cta']}\nAudience: {a['audience']}\nSchedule: {a['schedule']}" for a in C['ads'])
notes = ''.join(f'<li>{e(n)}</li>' for n in C['notes'])
page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Solace · Video Ads Nov 2026</title>
<style>body{{font-family:system-ui,sans-serif;background:#141210;color:#eee;margin:0 auto;padding:20px;max-width:1100px}}h1{{font-weight:600}}a{{color:#e2c88f}}
button{{background:#c9a86a;border:0;color:#111;padding:6px 12px;border-radius:6px;cursor:pointer;font-weight:600}}#zip{{font-size:1.1rem;padding:12px 20px}}
section{{border:1px solid #333;border-radius:12px;padding:16px;margin:18px 0}}.vids{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}}
figure{{margin:0}}figure video{{border-radius:10px;background:#000;display:block}}.vids figure:first-child video{{width:270px;height:480px}}.vids figure:last-child video{{width:384px;height:480px}}
figcaption{{font-size:.8rem;color:#aaa;margin-top:6px}}.f{{margin:10px 0}}.f b{{margin-right:8px}}pre{{white-space:pre-wrap;background:#1e1b18;padding:10px;border-radius:8px;margin:6px 0 0}}.m{{color:#bbb;font-size:.9rem}}
.n{{background:#1e1b18;border-radius:10px;padding:10px 14px 10px 30px;color:#ccc;font-size:.92rem}}
@media(max-width:700px){{.vids figure video{{width:100%!important;height:auto!important}}.vids figure{{width:100%}}}}</style></head><body>
<h1>Solace Skin Lab · Video Ads Meta · Noviembre 2026</h1>
<p>5 anuncios en video (HyperFrames: motion + voz en inglés + música). Cada uno en <b>9:16</b> (Reels/Stories) y <b>4:5</b> (Feed). Pendiente de aprobación — nada está publicado.</p>
<ul class="n">{notes}</ul>
<button id="zip" onclick="dl()">⬇ Descargar todo (ZIP: 10 videos + copys)</button> <span id="st"></span>
{''.join(secs)}
<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
<script>
const FILES={json.dumps(files)};const COPY={json.dumps(copytxt)};
function cp(b){{navigator.clipboard.writeText(b.nextElementSibling.textContent);b.textContent='¡Copiado!';setTimeout(()=>b.textContent='Copiar',1200)}}
async function dl(){{const z=new JSZip(),s=document.getElementById('st');let n=0;
for(const [u,name] of FILES){{s.textContent='Descargando '+(++n)+'/'+FILES.length+'…';z.file(name,await (await fetch(u)).blob())}}
z.file('00_COPYS_Solace_Video_Ads_Nov2026.txt',COPY);s.textContent='Comprimiendo…';
const b=await z.generateAsync({{type:'blob'}});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='Solace_Video_Ads_Nov2026.zip';a.click();s.textContent='Listo ✓'}}
</script></body></html>"""
open(f'{SRC}/index.html', 'w').write(page)
print('page ok', len(files))
