#!/usr/bin/env python3
"""Plan + pilot page for Solace November 2026 (GH Pages)."""
import html, json, sys, datetime
sys.path.insert(0, '/opt/data/solace-skin-lab/november-2026')
from spec import POSTS
E = html.escape
rows = []
for p in POSTS:
    dt = datetime.date.fromisoformat(p['date']).strftime('%a %b %d')
    fmt = '4:5' if p['fmt'] == '4x5' else '1:1'
    rows.append(f"<tr><td>{p['d']}</td><td>{dt}</td><td><span class='f f{p['fmt']}'>{fmt}</span></td><td>{E(p['service'])}</td>"
                f"<td><b>{E(p['title'])}</b> <i>{E(p['script'])}</i><br><small>{E(p['eyebrow'])} · {E(p['support'])}</small></td>"
                f"<td>{E(p['price'] or '—')}</td><td>{E(p['cta'])}</td>"
                f"<td><details><summary>ver</summary><p><b>Voz:</b> {E(' '.join(p['vo']))}</p><p><b>Caption:</b><br>{E(p['caption']).replace(chr(10),'<br>')}</p><p>{E(p['tags'])}</p></details></td></tr>")
pil = ''
for d, lab, voice in ((1, 'Día 1 · 4:5 · Microneedling', 'Victoria Reynolds'), (2, 'Día 2 · 1:1 · Martes 2×1 $74.99', 'Camila Navarro')):
    pil += f"""<div class="pil"><h3>{lab}</h3><video controls playsinline preload="metadata" poster="pilot/d{d:02d}.png?v=2" src="pilot/d{d:02d}.mp4?v=2"></video>
<p>Voz CloneVoice: <b>{voice}</b> · <a href="pilot/d{d:02d}.mp4?v=2" download>MP4</a> · <a href="pilot/d{d:02d}.png?v=2">PNG fijo</a></p></div>"""
page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Solace · Noviembre 2026 · Plan + piloto</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#0f0b08;color:#f3ece1;font:15px/1.5 Jost,sans-serif}}main{{max-width:1240px;margin:auto;padding:32px 20px}}
h1{{font:600 44px/1.1 'Cormorant Garamond',serif;margin:0 0 6px}}h2{{font:600 30px 'Cormorant Garamond',serif;color:#e2c88f;margin:36px 0 12px}}
.sub{{color:#bfb3a2}}.pils{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:24px}}.pil video{{width:100%;border-radius:10px;background:#000}}
.pil h3{{font:500 18px Jost;margin:0 0 8px}}a{{color:#e2c88f}}table{{width:100%;border-collapse:collapse;font-size:14px}}td,th{{border-bottom:1px solid #2c241c;padding:8px 6px;vertical-align:top;text-align:left}}
th{{color:#e2c88f;font-weight:500}}i{{font-family:'Cormorant Garamond',serif;color:#e2c88f;font-size:17px}}small{{color:#a99c89}}.f{{padding:2px 8px;border-radius:99px;font-size:12px}}.f4x5{{background:#3a2c1c}}.f1x1{{background:#1f2a26}}
details p{{margin:6px 0;color:#d8cdbd}}ul{{color:#d8cdbd}}</style></head><body><main>
<h1>Solace Skin Lab · Noviembre 2026</h1><p class="sub">30 posts animados para Facebook · 2 nov – 1 dic · 15 en 4:5 (días impares) + 15 en 1:1 (días pares) · Foto Artistly + voz CloneVoice (inglés) + animación HyperFrames · Interno, no compartir con el cliente.</p>
<h2>Piloto (2 de 30)</h2><div class="pils">{pil}</div>
<h2>Reglas del mes</h2><ul>
<li>Promos usadas tal cual están en el CRM: Martes 2×1 faciales $74.99 + copa de vino · Producto de lujo $74.99 + facial GRATIS · Salmon DNA 2×1 · LED desde $79.99 · Facial $74.99.</li>
<li>Black Friday (27 nov) usa la promo vigente de producto + facial gratis. <b>CONFIRMAR</b> si el cliente quiere otra promo especial.</li>
<li>Fechas: Veterans Day 11 nov, Thanksgiving 26 nov, Small Business Saturday 28 nov. 5 martes de 2×1 con parejas diferentes cada semana.</li>
<li>Inyectables: BOTOX® Cosmetic, Xeomin®, Juvéderm®, Belotero® con ® + "Individual results vary". Cero 'exosomes'. Sin antes/después ni testimonios inventados.</li>
<li>Fotos sin manos y sin texto generado; la tipografía la pone HyperFrames (texto exacto, sin errores).</li></ul>
<h2>Calendario</h2><table><tr><th>#</th><th>Fecha</th><th>Formato</th><th>Servicio</th><th>Pieza</th><th>Precio</th><th>CTA</th><th>Voz / caption</th></tr>{''.join(rows)}</table>
</main></body></html>"""
open('/opt/data/solace-skin-lab/november-2026/index.html', 'w').write(page)
print('ok')
