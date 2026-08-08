# SOLACE SKIN LAB — Manual de Montaje en Ads Manager (Paso a Paso)
**8 anuncios · META-01 → META-08 · El Paso, TX · Tel (915) 995-9524**

> Sigue este manual en orden. Cada anuncio incluye: ad set (audiencia + presupuesto) y el anuncio
> (imagen + copy A/B + titular + CTA + destino). Textos listos para copiar/pegar.

---

## FASE 0 — Preparación (haz esto UNA vez)

1. Entra a **business.facebook.com → Ads Manager**.
2. **Píxel:** menú *Events Manager → Data sources → Pixel* → confirma que el píxel esté *Active*.
   - Si no existe: *Connect data source → Web → Facebook Pixel* → instala el código en la página
     (o usa la integración con Shopify/WordPress si aplica).
3. **Página:** confirma que la página de Facebook "Solace Skin Lab" esté vinculada al Business Manager
   (Configuración → Páginas).
4. **Sube los 8 creativos** (imágenes 1:1) a la biblioteca:
   - `images/august-2026-v2/day01.png` · `day04.png` · `day05.png` · `day10.png` · `day13.png` · `day21.png` · `day28.png` · `day30.png`
   - (Además day06/12/14/18/19/20/22/25/26/27 como variantes alternas — ver por anuncio.)
5. **Crea las audiencias guardadas** (menú Audiences → Create → Saved Audience):

| Audiencia | Nombre sugerido | Ubicación | Edad | Género | Intereses |
|---|---|---|---|---|---|
| A1 Broad El Paso | `SOL_AUG_PROS_BROAD` | El Paso TX + 25 mi | 25–54 | Todos | Sin intereses |
| A2 Beauty | `SOL_AUG_PROS_BEAUTY` | El Paso TX + 15 mi | 25–54 | Mujeres | Skincare, Beauty & Cosmetics, Spas, Wellness |
| A3 Hombres 30-55 | `SOL_AUG_PROS_MEN` | El Paso TX + 25 mi | 30–55 | Hombres | Skincare, Grooming, Fitness |
| A4 21+ Ofertas | `SOL_AUG_OFFER_21` | El Paso TX + 15 mi | 21–54 | Todos | Skincare, Beauty |
| A5 Consulta 30+ | `SOL_AUG_PROS_30` | El Paso TX + 25 mi | 30–55 | Todos | Skincare, Wellness |
| A6 Juvéderm 25-45 | `SOL_AUG_PROS_25` | El Paso TX + 25 mi | 25–45 | Todos | Beauty, Makeup, Skincare |
| A7 Retargeting | `SOL_AUG_RET_ENGAGE` | El Paso TX + 25 mi | 25–55 | Todos | **Custom:** Engagers FB/IG 30 días + Video viewers 90 días + Visitantes web 180 días |

6. **Estructura que vas a crear (3 campañas):**

| Campaña | Objetivo | Presupuesto | Anuncios dentro |
|---|---|---|---|
| `SOL_AUG_01_PROSPECTING` | Awareness (o Traffic) | $15/día CBO | META-01, META-02 |
| `SOL_AUG_02_OFFERS` | Leads | $9/día CBO | META-03, META-04, META-05 |
| `SOL_AUG_03_RETARGET` | Leads | $6/día CBO | META-06, META-07, META-08 |

> *Presupuesto de ejemplo ($900/mes). Ajusta los $/día al real. Usa CBO (Advantage campaign budget): activa
> "Campaign budget optimization" y pon el total de la campaña.*

---

## ANUNCIO 1 — META-01 "Real Skin — Local Awareness"
**Campaña:** `SOL_AUG_01_PROSPECTING` · **Objetivo:** Awareness · **Ad set:** A1 `SOL_AUG_PROS_BROAD`

### Ad Set
- **Name:** `AS-META-01-BROAD`
- **Audiencia:** A1 (Broad, El Paso +25 mi, 25–54, todos)
- **Placements:** Advantage (quita Audience Network y Marketplace)
- **Presupuesto:** CBO de campaña (no pongas aquí)

### Anuncio
- **Formato:** Imagen única · **Imagen:** `day09.png` (Your August Skin Reset — Real skin. Smart care.)
- **Primary text A:**
  > Real skin deserves thoughtful care—not a one-size-fits-all promise. Solace Skin Lab begins with your goals and a conversation about the next step that may fit. Call (915) 995-9524 to learn more.
- **Primary text B:**
  > Smart skincare starts with clarity. Explore personalized facials, LED Light Therapy and consultation-led aesthetic care at Solace Skin Lab in El Paso. Call (915) 995-9524.
- **Headline A:** `Real Skin. Smart Care.`
- **Headline B:** `Personalized Care in El Paso`
- **Description:** `Cielo Vista Mall • Consultation-first care`
- **CTA:** `Learn More` (destino: página de reservas aprobada)
- **Optimización:** Alcance / participación
- **UTM:** `utm_source=meta&utm_medium=cpc&utm_campaign=solace_aug&utm_content=META-01`

---

## ANUNCIO 2 — META-02 "Facial + LED Experience"
**Campaña:** `SOL_AUG_01_PROSPECTING` · **Objetivo:** Traffic/Inquiries · **Ad set:** A2 `SOL_AUG_PROS_BEAUTY`

### Ad Set
- **Name:** `AS-META-02-BEAUTY`
- **Audiencia:** A2 (El Paso +15 mi, 25–54, mujeres, intereses beauty)
- **Placements:** Advantage − Audience Network − Marketplace

### Anuncio
- **Imagen:** `day28.png`
- **Primary text A:**
  > A personalized facial plan may include LED Light Therapy when appropriate and available. Discover a calm, consultation-led experience at Solace Skin Lab. Call (915) 995-9524 to ask about availability.
- **Primary text B:**
  > Modern skincare can still feel personal. Ask how a facial and LED Light Therapy may fit into a thoughtful care plan. Availability and individual experiences vary. Call (915) 995-9524.
- **Headline A:** `Complete Facial + LED`
- **Headline B:** `Ask About Facial + LED`
- **Description:** `Availability and suitability vary.`
- **CTA:** `Call Now` → teléfono **(915) 995-9524**
- **Optimización:** Llamadas calificadas
- **UTM:** `utm_content=META-02`

---

## ANUNCIO 3 — META-03 "Luxury Skincare + Free Facial"
**Campaña:** `SOL_AUG_02_OFFERS` · **Objetivo:** Leads · **Ad set:** A4 `SOL_AUG_OFFER_21`

### Ad Set
- **Name:** `AS-META-03-OFFER`
- **Audiencia:** A4 (El Paso +15 mi, 21–54, intereses beauty)
- **Fechas:** Semanas 2 y 4 del mes
- **Exclusión:** personas que ya canjearon la oferta (si hay lista)

### Anuncio
- **Imagen:** `day04.png` (alterna 1: `day25.png` en semana 4 · alterna 2: `day01.png`)
- **Primary text A:**
  > GET A FREE FACIAL. WITH THE PURCHASE OF ANY LUXURY SKINCARE PRODUCT • ONLY $64.99. Call Solace Skin Lab at (915) 995-9524 to confirm eligible products, availability and complete offer terms.
- **Primary text B:**
  > Bring your skincare routine and in-spa care together. GET A FREE FACIAL. WITH THE PURCHASE OF ANY LUXURY SKINCARE PRODUCT • ONLY $64.99. Call (915) 995-9524 for eligible products and complete terms.
- **Headline A:** `Get a Free Facial • Only $64.99`
- **Headline B:** `Luxury Skincare + Free Facial`
- **Description:** `Eligible products, availability and complete terms must be confirmed.`
- **CTA:** `Call Now` → (915) 995-9524
- **Optimización:** Llamadas calificadas / canjes confirmados
- **UTM:** `utm_content=META-03`
- **⚠️ No activar** hasta que el cliente confirme por escrito qué cubre $64.99, productos elegibles, fechas y límites.

---

## ANUNCIO 4 — META-04 "Tuesday 2×1 Rotation"
**Campaña:** `SOL_AUG_02_OFFERS` · **Objetivo:** Leads · **Ad set:** A4 + **edad 21+ obligatoria**

### Ad Set
- **Name:** `AS-META-04-TUESDAY`
- **Audiencia:** A4 (21–54) — el ad set DEBE tener edad mínima 21+ (vino)
- **Programación:** martes + 1–2 días previos (domingo/lunes a martes)
- **Frecuencia:** rota imagen cada martes

### Anuncio
- **Imagenes:** `day05.png` (sem 1) → `day12.png` (sem 2) → `day19.png` (sem 3) → `day26.png` (sem 4)
- **Primary text A:**
  > TUESDAY 2×1 + WINE + 2 FREE FACIALS. Call Solace Skin Lab at (915) 995-9524 for complete offer terms, eligibility, restrictions and availability. Wine available only to guests age 21+.
- **Primary text B:**
  > Make Tuesday the self-care plan. TUESDAY 2×1 + WINE + 2 FREE FACIALS. Call (915) 995-9524 to verify eligibility, restrictions, availability and complete terms. Wine available only to guests age 21+.
- **Headline A:** `Tuesday 2×1 Facials`
- **Headline B:** `Wine + 2 Free Facials`
- **Description:** `Restrictions apply • Availability varies • Wine 21+ only`
- **CTA:** `Call Now` → (915) 995-9524
- **Optimización:** Llamadas calificadas / reservas verificadas
- **UTM:** `utm_content=META-04`
- **⚠️ No activar** hasta confirmar reglas del 2×1 (qué incluye, límites, términos del vino).

---

## ANUNCIO 5 — META-05 "BOTOX® Cosmetic Consultation"
**Campaña:** `SOL_AUG_02_OFFERS` · **Objetivo:** Leads · **Ad set:** A5 `SOL_AUG_PROS_30`

### Ad Set
- **Name:** `AS-META-05-BOTOX`
- **Audiencia:** A5 (El Paso +25 mi, 30–55, todos)
- **Fechas:** semanas 2–4 (después de aprobación regulatoria)

### Anuncio
- **Imagen:** `day06.png` (BOTOX® consultation first — limpia, sin badge de oferta)
- **Alternas:** `day14.png` (Real Treatment. Real Care.) · `day10.png` (Ask Before BOTOX®) · `day22.png` (Questions Deserve Answers)
- **Primary text A:**
  > Considering BOTOX® Cosmetic starts with an informed consultation. Discuss suitability, potential risks, natural movement and realistic expectations before deciding whether treatment is appropriate. Individual results vary. Call (915) 995-9524.
- **Primary text B:**
  > Questions should come before treatment. A Solace consultation can cover BOTOX® Cosmetic suitability, potential risks and realistic expectations. Individual results vary. Call (915) 995-9524.
- **Headline A:** `BOTOX® Cosmetic Consultation`
- **Headline B:** `Questions Come First`
- **Description:** `Suitability and individual results vary.`
- **CTA:** `Call Now` → (915) 995-9524 (o formulario de consulta aprobado)
- **Optimización:** Consultas calificadas (no clics)
- **UTM:** `utm_content=META-05`
- **⚠️ Requiere** revisión del cliente + información de seguridad del fabricante (ISI) antes de publicar.

---

## ANUNCIO 6 — META-06 "Microneedling Consultation"
**Campaña:** `SOL_AUG_03_RETARGET` · **Objetivo:** Leads · **Ad set:** A3 `SOL_AUG_PROS_MEN`

### Ad Set
- **Name:** `AS-META-06-MEN`
- **Audiencia:** A3 (El Paso +25 mi, 30–55, **hombres**, grooming/skincare)
- **Nota:** si el píxel muestra que mujeres convierten en textura/fine lines, crea espejo femenino con A5 en semana 3.

### Anuncio
- **Imagen:** `day13.png` (alternas: `day18.png`, `day20.png`, `day27.png`)
- **Primary text A:**
  > Microneedling may be considered as part of a personalized approach to the appearance of certain acne scars, healed scar texture, fine lines or scalp concerns. Suitability and individual results vary. Call (915) 995-9524 to request an evaluation.
- **Primary text B:**
  > A microneedling plan should begin with an individual evaluation—not a promise. Ask whether the service may be appropriate for specific texture, fine-line or scalp goals. Individual results vary. Call (915) 995-9524.
- **Headline A:** `Request a Microneedling Evaluation`
- **Headline B:** `A Personalized Microneedling Plan`
- **Description:** `Suitability, treatment needs and results vary.`
- **CTA:** `Learn More` → página de consulta aprobada
- **Optimización:** Solicitudes de evaluación calificadas
- **UTM:** `utm_content=META-06`
- **⚠️** Sin promesa de mejora, diagnóstico ni antes/después.

---

## ANUNCIO 7 — META-07 "JUVÉDERM® Consultation"
**Campaña:** `SOL_AUG_03_RETARGET` · **Objetivo:** Leads · **Ad set:** A6 `SOL_AUG_PROS_25`

### Ad Set
- **Name:** `AS-META-07-JUVE`
- **Audiencia:** A6 (El Paso +25 mi, 25–45, todos)
- **Fechas:** semanas 3–4 (después de aprobación regulatoria)

### Anuncio
- **Imagen:** `day21.png`
- **Primary text A:**
  > A JUVÉDERM® lip filler conversation should begin with your goals, suitability, potential risks and realistic expectations. Individual results vary. Call Solace Skin Lab at (915) 995-9524 to request a consultation.
- **Primary text B:**
  > Interested in learning about JUVÉDERM® for lip filler? Start with an informed consultation covering suitability, potential risks and expectations. Individual results vary. Call (915) 995-9524.
- **Headline A:** `JUVÉDERM® Lip Filler Consultation`
- **Headline B:** `Start With an Informed Consultation`
- **Description:** `Suitability and individual results vary.`
- **CTA:** `Call Now` → (915) 995-9524
- **Optimización:** Consultas calificadas
- **UTM:** `utm_content=META-07`
- **⚠️ Requiere** revisión del cliente + ISI del fabricante antes de publicar.

---

## ANUNCIO 8 — META-08 "Warm Audience — Choose Your Next Step"
**Campaña:** `SOL_AUG_03_RETARGET` · **Objetivo:** Leads · **Ad set:** A7 `SOL_AUG_RET_ENGAGE`

### Ad Set
- **Name:** `AS-META-08-RET`
- **Audiencia:** A7 (custom: engagers 30d + video viewers 90d + web visitors 180d)
- **Exclusión:** clientes recientes / reservas confirmadas (cuando exista lista)
- **Fechas:** semanas 2–4

### Anuncio
- **Imagen:** `day30.png`
- **Primary text A:**
  > Still exploring the right next step? Solace Skin Lab can help organize the questions around your goals, suitability and available services. Call (915) 995-9524 to request a consultation.
- **Primary text B:**
  > Clear information comes before a confident decision. Reconnect with Solace Skin Lab to discuss the service that may fit your goals. Call (915) 995-9524.
- **Headline A:** `Your Next Step Starts Here`
- **Headline B:** `Request a Personalized Consultation`
- **Description:** `Cielo Vista Mall • El Paso, TX`
- **CTA:** `Call Now` → (915) 995-9524 (o página de reservas)
- **Optimización:** Llamadas calificadas y reservas confirmadas
- **UTM:** `utm_content=META-08`

---

## FASE FINAL — Después de publicar

1. **Verifica que las 3 campañas estén en "Active"** (vista Campaigns).
2. **Prueba el píxel:** Events Manager → Test events → navega a la página de reservas.
3. **Día 2:** revisa entrega, NO toques nada.
4. **Día 5:** primer corte — CTR, costo/llamada, frecuencia.
5. **Día 7:** pausa ad sets por debajo del umbral; escala ganadores +20–30%.
6. **Frecuencia > 3.0** → rota creativo alterno.
7. **Comentarios:** responde en < 24h todos los días.
8. **Reporte semanal al cliente:** alcance, llamadas, costo/llamada, reservas.
