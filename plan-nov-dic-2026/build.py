#!/usr/bin/env python3
"""Plan 14-nov → 13-dic 2026 de Solace Skin Lab (bilingüe EN/ES, sin Rx). Genera index.html."""
import json, html, pathlib
OUT = pathlib.Path(__file__).parent / 'index.html'

# day, fecha, idioma, servicio, audiencia, gancho (pantalla), ángulo, promo
P = [
 (1, 'Sáb 14 nov', 'EN', 'Luxury Facial', 'Mujeres', 'One hour that\'s just yours.', 'Cómo se siente: tiempo para ella', 'Producto $74.99 + facial GRATIS'),
 (2, 'Dom 15 nov', 'ES', 'Facial (manchas)', 'Mujeres hispanas', 'Tu piel, sin filtro.', 'Confianza sin maquillaje', ''),
 (3, 'Lun 16 nov', 'EN', 'Microneedling (hombres)', 'Hombres', 'Smoother skin. Same you.', 'Cómo se ve: textura y cicatrices', ''),
 (4, 'Mar 17 nov', 'ES', 'Martes de amigas', 'Amigas / mamá e hija', 'Martes de amigas: 2 faciales gratis.', 'Plan para dos', 'Producto $74.99 + 2 faciales GRATIS (vino solo en el texto)'),
 (5, 'Mié 18 nov', 'EN', 'Mapa de líneas finas', 'Mujeres 30+', 'Smooth fine lines. No needles.', 'Alternativa sin agujas', ''),
 (6, 'Jue 19 nov', 'ES', 'Facial + Dermaplaning', 'Mujeres', 'Que el maquillaje se vea como piel.', 'Resultado el mismo día', ''),
 (7, 'Vie 20 nov', 'EN', 'Salmon DNA', 'Mujeres', 'Hydration you can actually see.', 'Beneficios (sin precio)', ''),
 (8, 'Sáb 21 nov', 'ES', 'DpSCAN', 'Todos', 'Conoce tu piel por dentro.', 'Diagnóstico con datos', ''),
 (9, 'Dom 22 nov', 'EN', 'Lip enhancement', 'Mujeres 18+', 'Soft, natural lips. Still you.', 'Natural, no exagerado', ''),
 (10, 'Lun 23 nov', 'ES', 'Evaluación de cicatrices (hombres)', 'Hombres hispanos', 'Hombres: las cicatrices de acné tienen solución.', 'Cómo se ve + privado', ''),
 (11, 'Mar 24 nov', 'EN', 'Tuesday besties', 'Amigas', 'Thankful for my bestie.', 'Plan para dos, semana de Thanksgiving', 'Producto $74.99 + 2 facials FREE'),
 (12, 'Mié 25 nov', 'ES', 'Luxury Facial', 'Mujeres hispanas', 'Lista para la foto familiar.', 'Llegar radiante a la cena', 'Producto $74.99 + facial GRATIS'),
 (13, 'Jue 26 nov', 'EN', 'Saludo Thanksgiving', 'Comunidad', 'Grateful for you, El Paso.', 'Gratitud, sin venta', ''),
 (14, 'Vie 27 nov', 'ES', 'Black Friday', 'Mujeres', 'Este Black Friday, regálate a ti primero.', 'Darse un gusto', 'Producto $74.99 + facial GRATIS'),
 (15, 'Sáb 28 nov', 'EN', 'Small Business Saturday', 'Comunidad', 'Shop local. Glow local.', 'Negocio local de El Paso', ''),
 (16, 'Dom 29 nov', 'ES', 'Derma Jade Eye', 'Mujeres', 'Mirada descansada, aunque no duermas.', 'Ojeras y cansancio', ''),
 (17, 'Lun 30 nov', 'EN', 'LED Light Therapy', 'Todos', 'Red light. Real glow.', 'Cómo funciona la luz roja/azul', ''),
 (18, 'Mar 1 dic', 'ES', 'Martes de amigas', 'Amigas', 'Diciembre empieza de a dos.', 'Plan para dos', 'Producto $74.99 + 2 faciales GRATIS*'),
 (19, 'Mié 2 dic', 'EN', 'D\'OR24K Neck & Décolleté', 'Mujeres 35+', 'Your neck deserves a facial too.', 'La zona que todas olvidan', ''),
 (20, 'Jue 3 dic', 'ES', 'Mapa de líneas finas', 'Mujeres 30+', 'Suaviza líneas finas. Sin agujas.', 'Alternativa sin agujas', ''),
 (21, 'Vie 4 dic', 'EN', 'Scalp Care (hombres)', 'Hombres', 'Your hairline, looked after.', 'Cómo se ve: cabello y cuero cabelludo', ''),
 (22, 'Sáb 5 dic', 'ES', 'Luxury Facial en 3 pasos', 'Mujeres', 'Una hora solo para ti, en 3 pasos.', 'Qué incluye (análisis + facial + LED)', 'Producto $74.99 + facial GRATIS*'),
 (23, 'Dom 6 dic', 'EN', 'Mito vs realidad', 'Todos', '"Facials are just pampering." Think again.', 'Educación', ''),
 (24, 'Lun 7 dic', 'ES', 'Microneedling (hombres)', 'Hombres hispanos', 'Piel más pareja, sin que nadie lo note.', 'Cómo se ve + discreto', ''),
 (25, 'Mar 8 dic', 'EN', 'Tuesday besties', 'Amigas', 'Holiday party prep, for two.', 'Plan para dos antes de las fiestas', 'Producto $74.99 + 2 facials FREE*'),
 (26, 'Mié 9 dic', 'ES', 'Labios naturales', 'Mujeres 18+', 'Labios suaves y naturales.', 'Natural, no exagerado', ''),
 (27, 'Jue 10 dic', 'EN', 'Facial + LED cara y cuello', 'Mujeres', 'Camera-ready for every holiday photo.', 'Fotos de temporada', ''),
 (28, 'Vie 11 dic', 'ES', 'Salmon DNA', 'Mujeres', 'Hidratación que se nota.', 'Beneficios (sin precio)', ''),
 (29, 'Sáb 12 dic', 'EN', 'Interacción', 'Todos', 'What\'s your skin goal for 2027? 👇', 'Comentarios', ''),
 (30, 'Dom 13 dic', 'ES', 'Posadas', 'Mujeres hispanas', 'Brilla en todas tus posadas.', 'Temporada hispana', 'Producto $74.99 + facial GRATIS*'),
]

ok = [
 ('Faciales', 'Luxury Facial, Facial (limpieza, acné, anti-edad, manchas), Facial + Dermaplaning, Salmon DNA (solo beneficios, sin precio)'),
 ('Luz LED', 'LED Light Therapy (roja/azul), Facial + LED cara y cuello (D\'OR24K)'),
 ('Piel y ojos', 'DpSCAN, Derma Jade Eye Solution, D\'OR24K Neck & Décolleté'),
 ('Hombres', 'Evaluación de cicatrices de acné, Scalp Care, Microneedling'),
 ('Promo', 'Producto luxury $74.99 + facial GRATIS · Martes: 2 faciales GRATIS (tú + amiga)'),
]
care = [
 ('Lip enhancement', 'Sí, Meta lo permite (dermal fillers) con anuncios para 18+. Siempre "lip filler / lip enhancement" genérico: sin marcas, sin agujas ni jeringas, foto del resultado. Máximo 2 al mes.'),
 ('Microneedling', 'Sí, Meta lo menciona como permitido para 18+. Mostrar el aparato y la piel después, nunca agujas en primer plano ni piel con sangre. Decir "collagen induction" / "inducción de colágeno".'),
]
no = 'Botox, Xeomin, Dysport, "wrinkle relaxers", "injectables", Juvéderm/Belotero (marcas), GLP-1/semaglutide, péptidos, NAD+, IV/B12, agujas/jeringas/💉, "exosomes", PRP en anuncios.'

def e(s): return html.escape(s)
rows = ''.join(f'''<tr data-d="{d}"><td class="n">{d}</td><td class="date">{e(f)}</td><td><span class="lang {l.lower()}">{l}</span></td>
<td><b>{e(s)}</b><div class="aud">{e(a)}</div></td><td class="hook">{e(h)}</td><td class="ang">{e(an)}</td><td class="promo">{e(pr) if pr else '—'}</td>
<td class="act"><button class="ch" onclick="tog({d})">Cambiar</button><textarea id="n{d}" placeholder="¿Qué cambiarías?" hidden></textarea></td></tr>''' for d, f, l, s, a, h, an, pr in P)
okh = ''.join(f'<li><b>{e(a)}:</b> {e(b)}</li>' for a, b in ok)
careh = ''.join(f'<li><b>{e(a)}:</b> {e(b)}</li>' for a, b in care)
en = sum(1 for p in P if p[2] == 'EN'); es = len(P) - en; promos = sum(1 for p in P if p[7])

page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Solace Skin Lab · Plan 14 nov – 13 dic 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#141110;--card:#1e1a17;--line:#3a322b;--gold:#c9a45c;--cream:#f3ead9;--mut:#b3a690;--ok:#7fb48a;--warn:#e0b45a;--no:#d9776a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--cream);font:15px/1.55 Inter,system-ui,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:32px 20px 80px}}
h1,h2{{font-family:"Cormorant Garamond",serif;font-weight:600;color:var(--gold);margin:0 0 6px}}h1{{font-size:40px}}h2{{font-size:28px;margin-top:40px}}
.sub{{color:var(--mut);margin:0 0 24px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px}}.card h3{{margin:0 0 8px;font-size:15px;letter-spacing:.06em;text-transform:uppercase}}
.card ul{{margin:0;padding-left:18px}}.card li{{margin:6px 0}}.g h3{{color:var(--ok)}}.y h3{{color:var(--warn)}}.r h3{{color:var(--no)}}
.kpis{{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}}.kpi{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px}}.kpi b{{display:block;font-size:24px;color:var(--gold)}}
table{{width:100%;border-collapse:collapse;background:var(--card);border-radius:14px;overflow:hidden}}th,td{{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}}
th{{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);background:#191512}}td.n{{color:var(--gold);font-weight:600}}td.date{{white-space:nowrap;color:var(--mut)}}
.lang{{font-size:12px;font-weight:600;padding:2px 8px;border-radius:99px}}.lang.en{{background:#2c3a4a;color:#bcd6f2}}.lang.es{{background:#4a2f2c;color:#f2c9bc}}
.aud{{color:var(--mut);font-size:13px}}.hook{{font-family:"Cormorant Garamond",serif;font-size:19px}}.promo{{color:var(--gold);font-size:13px}}.ang{{font-size:13px;color:var(--mut)}}
.act button,.big{{background:transparent;border:1px solid var(--line);color:var(--cream);border-radius:8px;padding:6px 10px;cursor:pointer;font:inherit;font-size:13px}}
.act textarea{{width:100%;min-width:160px;margin-top:6px;background:#141110;color:var(--cream);border:1px solid var(--gold);border-radius:8px;padding:6px;font:inherit;font-size:13px}}
tr.flag td{{background:#2a2118}}.big{{font-size:16px;padding:12px 20px;border-radius:10px}}.big.pri{{background:var(--gold);color:#1a1410;border-color:var(--gold);font-weight:600}}
.map{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}.map div{{background:#191512;border:1px solid var(--line);border-radius:10px;padding:12px}}.map b{{color:var(--gold);display:block}}
.foot{{color:var(--mut);font-size:13px;margin-top:10px}}#msg{{margin-left:12px;color:var(--ok)}}
@media(max-width:820px){{table,thead,tbody,tr,td{{display:block}}thead{{display:none}}tr{{border-bottom:1px solid var(--line);padding:8px 0}}td{{border:0;padding:4px 14px}}.map{{grid-template-columns:1fr 1fr}}}}
</style></head><body><div class="wrap">
<h1>Solace Skin Lab · Plan de contenido</h1>
<p class="sub">14 de noviembre – 13 de diciembre 2026 · Facebook + Instagram · Inglés y español</p>

<h2>Sí podemos publicar y anunciar</h2>
<p class="sub">El castigo de octubre fue por 3 posts de medicamentos con receta (Botox / inyectables). Todo lo demás del spa se puede publicar y anunciar con normalidad. Antes de empezar los anuncios, revisar en Meta Business Suite → <b>Calidad de la cuenta</b> que no haya restricciones activas.</p>
<div class="grid">
<div class="card g"><h3>✅ Sí, sin problema</h3><ul>{okh}</ul></div>
<div class="card y"><h3>⚠️ Sí, con cuidado</h3><ul>{careh}</ul></div>
<div class="card r"><h3>❌ Nunca en Facebook / Instagram</h3><ul><li>{e(no)}</li></ul></div>
</div>

<h2>Estrategia</h2>
<div class="kpis"><div class="kpi"><b>30</b>videos animados con voz</div><div class="kpi"><b>{en} / {es}</b>inglés / español</div><div class="kpi"><b>{promos}</b>con la promo</div><div class="kpi"><b>Reel + historia</b>cada publicación</div></div>
<div class="grid">
<div class="card"><h3>Público hispano</h3><ul><li>La mitad del calendario va en <b>español</b>, con voz en español, para la clientela hispana de El Paso y Juárez.</li><li>En anuncios: un conjunto en inglés y otro en español (segmentación por idioma: español), ambos para mayores de 18.</li><li>El texto en español no es traducción: habla de posadas, foto familiar y "martes de amigas".</li></ul></div>
<div class="card"><h3>A quién le hablamos</h3><ul><li><b>Mujeres:</b> cómo se siente (confianza, una hora para ella).</li><li><b>Hombres:</b> cómo se ve (textura, cicatrices, cabello) y que sea discreto.</li><li><b>Clientas con poco tiempo:</b> resultado el mismo día.</li></ul></div>
<div class="card"><h3>Formato</h3><ul><li>Videos de 10–15 s, fotos estilo tratamiento real, tipografía serif dorada.</li><li>Cada pieza sale como reel y como historia a la misma hora.</li><li>Teléfono (915) 209-2060 · Cielo Vista Mall.</li></ul></div>
</div>

<h2>"Smooth fine lines. No needles."</h2>
<p class="sub">En lugar del diagrama de zonas de Botox, el mismo concepto con tratamientos sin receta (días 5 y 20):</p>
<div class="map"><div><b>Frente y entrecejo</b>Luxury Facial + LED luz roja</div><div><b>Patas de gallo</b>Derma Jade Eye Solution</div><div><b>Cuello y escote</b>D'OR24K Neck &amp; Décolleté</div><div><b>Textura y brillo</b>Facial + Dermaplaning</div></div>

<h2>Calendario</h2>
<p class="sub">Toca "Cambiar" en cualquier día para dejar un comentario.</p>
<table><thead><tr><th>#</th><th>Fecha</th><th>Idioma</th><th>Servicio</th><th>Gancho en pantalla</th><th>Ángulo</th><th>Promo</th><th></th></tr></thead><tbody>{rows}</tbody></table>
<p class="foot">* Si la promo cambia en diciembre, se ajusta solo ese día. Salmon DNA siempre sin precio. Sin vino en imágenes (solo en el texto del martes).</p>

<h2>Aprobación</h2>
<textarea id="gen" placeholder="Comentarios generales (opcional)" style="width:100%;min-height:80px;background:var(--card);color:var(--cream);border:1px solid var(--line);border-radius:10px;padding:10px;font:inherit"></textarea>
<p><button class="big pri" onclick="send('approved')">Aprobar plan</button> <button class="big" onclick="send('changes')">Enviar cambios</button><span id="msg"></span></p>
</div>
<script>
const PB='https://aprovaciones.bunkeragent.cloud',CLIENT='solace',CAMPAIGN='plan-nov-dic-2026';
function tog(d){{const t=document.getElementById('n'+d);t.hidden=!t.hidden;t.closest('tr').classList.toggle('flag',!t.hidden);if(!t.hidden)t.focus()}}
async function send(status){{const days=[...document.querySelectorAll('textarea[id^=n]')].filter(t=>t.value.trim()).map(t=>({{id:+t.id.slice(1),status:'changes',notes:t.value.trim()}}));
const review={{plan:status,notes:document.getElementById('gen').value.trim(),posts:days,sent_at:new Date().toISOString()}};
const m=document.getElementById('msg');m.textContent='Enviando…';
try{{const r=await fetch(PB+'/api/collections/approvals/records',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{client:CLIENT,campaign:CAMPAIGN,client_name:'Solace Client',review}})}});
m.textContent=r.ok?(status==='approved'?'¡Plan aprobado! Gracias.':'Cambios enviados. Gracias.'):'No se pudo enviar ('+r.status+').'}}catch(e){{m.textContent='No se pudo enviar. Revisa tu conexión.'}}}}
</script></body></html>'''
OUT.write_text(page)
json.dump([dict(zip(['day', 'date', 'lang', 'service', 'audience', 'hook', 'angle', 'promo'], p)) for p in P], open(OUT.parent / 'plan.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(P), en, es, promos)
