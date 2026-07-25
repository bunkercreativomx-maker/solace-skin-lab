# Auditoría bloqueante de cumplimiento — Calendario V2

**Archivos revisados**

- `calendar_v2_2026-07-24_to_2026-08-22.json`
- `calendar_v2_2026-07-24_to_2026-08-22.md`

**Decisión:** **FAIL — PUBLICACIÓN BLOQUEADA** hasta aplicar y volver a revisar los cambios indicados abajo.

> Revisión editorial/comercial preventiva; no sustituye revisión legal, regulatoria ni la información de seguridad exigible por fabricante, jurisdicción o plataforma.

## Resumen por categoría

| Categoría | Resultado | Hallazgo principal |
|---|---|---|
| Claims médicos y credenciales | **FAIL** | Hay claims fisiológicos no sustentados, resultados formulados de manera demasiado directa y cuatro menciones de “trained provider” sin credencial confirmada. |
| BOTOX® Cosmetic | **FAIL** | El día 10 usa el nombre incompleto en imagen; el día 30 menciona BOTOX® Cosmetic sin suitability, potential risks ni variabilidad; el día 6 sugiere resultado en copy/imagen. |
| JUVÉDERM® | **PASS condicional** | El día 21 incluye consulta, suitability, potential risks, expectativas realistas e individual results vary. Publicación sigue condicionada a confirmar ISI/revisión regulatoria aplicable. |
| Microneedling: acne scars/scars/fine lines/scalp | **FAIL** | No hay garantía explícita, pero días 13 y 18 incorporan un claim fisiológico (“supports … natural renewal”) no documentado. Días 20 y 27 están correctamente limitados. |
| Alcohol 21+ | **PASS** | Los cuatro martes (días 5, 12, 19 y 26) incluyen restricción 21+ en el copy y no muestran consumo durante tratamiento. |
| Promociones, términos y precios | **FAIL** | No se mezclan $64.99/$149.99, pero la promoción Tuesday no se conserva literalmente en todos los copys y “bring your favorite person” interpreta el 2×1 antes de confirmar términos. |
| Teléfono oficial | **PASS** | Las 23 apariciones detectadas usan exclusivamente **(915) 995-9524**; no se encontró otro teléfono. |
| AIDA completo | **PASS** | Los 30 registros tienen `hook`, `body`, `desire` y `cta` no vacíos. |
| Duplicación de hooks | **PASS** | No hay hooks exactos duplicados ni pares con similitud alta en la revisión automatizada. |
| Duplicación de CTAs | **FAIL** | Días 19 y 26 repiten exactamente el CTA; días 5/12 son casi idénticos (similitud 0.92). |
| Coherencia JSON ↔ Markdown | **FAIL** | La arquitectura de 30 días coincide en lo sustancial, pero el Markdown conserva un gate ya superado, clasifica el día 24 como BOTOX® y no refleja exactamente el CTA del día 28. |

## Cambios bloqueantes exactos

### 1. Claims médicos y credenciales

Aplicar estas sustituciones en el JSON y en cualquier texto visible que se genere a partir de él:

1. **Día 2 — `body`**  
   Sustituir:
   > “LED Light Therapy can be discussed as a gentle, technology-forward complement…”

   por:
   > **“LED Light Therapy may be discussed as a technology-forward complement to a personalized facial experience. The right option depends on your skin, goals, and the services available at Solace.”**

   Motivo: “gentle” puede leerse como claim de tolerabilidad/seguridad no sustentado.

2. **Día 8 — `desire`**  
   Sustituir:
   > “Leave with refreshed skin and a clearer understanding of what to do next.”

   por:
   > **“A personalized facial may support a refreshed-looking complexion and a clearer understanding of what to do next; individual experiences vary.”**

3. **Día 11 — `desire`**  
   Sustituir:
   > “Enjoy skin that feels polished, soft, and ready for your next step in care.”

   por:
   > **“Ask whether dermaplaning may help your skin look and feel smoother as part of your next step in care; individual results vary.”**

4. **Días 8, 11, 13 y 20 — `imageScene`**  
   Eliminar la palabra **“trained”** de “trained provider”/“trained gloved provider”, salvo que el cliente documente esa credencial y autorice expresamente su uso. Mantener la dirección de técnica segura sin atribuir credenciales inventadas.

5. **Día 16 — `hook` y `body`**  
   Sustituir el hook por:
   > **“A technology-forward facial experience can be approached thoughtfully.”**

   Sustituir el body por:
   > **“LED Light Therapy may be considered as a complement to a personalized facial plan. Availability, suitability, and individual experiences vary.”**

   Motivo: retirar “gentle” y evitar presentar beneficios/tolerabilidad como hechos no documentados.

### 2. Microneedling

1. **Día 13 — `body`**  
   Sustituir por:
   > **“Microneedling may be considered as part of a personalized approach to improve the appearance of certain acne scars and uneven texture. Suitability, treatment needs, and individual results vary.”**

2. **Día 18 — `body`**  
   Sustituir por:
   > **“Microneedling may help improve the appearance of fine lines, wrinkles, and uneven texture as part of a customized approach. Suitability, treatment needs, and individual results vary.”**

Motivo: eliminar el claim fisiológico no documentado **“supports the skin’s natural renewal response/process”**. Los días 20 y 27 ya evitan garantías de crecimiento capilar o corrección de cicatrices y pueden mantenerse.

### 3. BOTOX® Cosmetic

1. **Día 10 — `imageTitle`**  
   Sustituir:
   > `BEFORE BOTOX®`

   por:
   > **`BEFORE BOTOX® COSMETIC`**

2. **Día 6 — `desire`**  
   Sustituir por:
   > **“Discuss whether a measured approach may align with your goals; suitability and individual results vary.”**

3. **Día 6 — `imageScript`**  
   Sustituir:
   > `Refreshed, still you`

   por una formulación no orientada a resultado, por ejemplo:
   > **`Consultation first`**

4. **Día 30 — `body`**  
   Al mencionar BOTOX® Cosmetic en una pieza de conversión, añadir el gate completo. Sustituir por:
   > **“Choose one goal, ask one honest question, and take one clear next step. From personalized facials and LED therapy to microneedling, BOTOX® Cosmetic, lip filler, and thoughtful skincare, a consultation can address suitability, potential risks, realistic expectations, and available options. Individual results vary.”**

5. **Antes de publicación comercial:** obtener confirmación escrita del cliente sobre las indicaciones, contraindicaciones, Important Safety Information, enlaces y aprobaciones de fabricante/regulatorias que deban acompañar BOTOX® Cosmetic. No inventar ese contenido en la campaña.

### 4. JUVÉDERM®

El día 21 pasa la revisión de lenguaje: distingue JUVÉDERM® lip filler, presenta consulta, suitability, potential risks, realistic expectations e individual results vary.

**Gate externo obligatorio antes de publicar:** confirmar por escrito con el cliente si se requiere Important Safety Information, indicaciones, contraindicaciones, enlaces o aprobación de fabricante/regulatoria. Si se requiere, incorporarlo literalmente y volver a auditar; no inventarlo.

### 5. Promociones y alcohol

#### Tuesday

1. En los cuerpos de los días **5, 12, 19 y 26**, conservar literalmente y como una sola unidad factual:
   > **TUESDAY 2×1 + WINE + 2 FREE FACIALS**

   Las variantes actuales “Tuesday 2x1 + wine…”, “with WINE…” y “LAST TUESDAY TO GLOW 2×1 with…” no preservan literalmente la oferta confirmada.

2. **Días 5 y 12:** retirar:
   > “Bring your favorite person…”

   hasta confirmar por escrito qué significa el 2×1, quién es elegible y cómo se relaciona con “2 FREE FACIALS”. No sustituirlo por “one for you and one for a friend” ni otra interpretación.

3. Mantener en los cuatro copys:
   > **“Wine available only to guests age 21+.”**

   Para uniformidad, usar esa frase exacta también en días 19 y 26, además del llamado a consultar términos.

4. Antes de publicar, el cliente debe confirmar por escrito: servicio/producto elegible, alcance exacto del 2×1, relación con las dos faciales gratuitas, fechas, límites, disponibilidad, exclusiones, restricciones, reglas de canje y elegibilidad del alcohol. Hasta entonces, mantener el calificador de llamada para términos completos.

#### Luxury skincare

- Días 4 y 25 conservan la oferta aprobada y no mezclan `$64.99` con `$149.99`.
- Mantener literalmente:
  > **GET A FREE FACIAL / WITH THE PURCHASE OF ANY LUXURY SKINCARE PRODUCT / ONLY $64.99**
- Mantener el llamado para productos elegibles y términos completos hasta que el cliente confirme por escrito qué cubre exactamente `$64.99`, disponibilidad, fechas, límites y exclusiones.

### 6. CTAs duplicados

Reescribir, como mínimo, estos CTAs sin cambiar la oferta factual:

- **Día 12:**
  > **“Share this post, then call (915) 995-9524 to verify eligibility, availability, and complete offer terms.”**

- **Día 19:**
  > **“Save the date and call (915) 995-9524 to ask about restrictions, 21+ wine eligibility, and availability.”**

- **Día 26:**
  > **“For final-Tuesday availability and complete offer terms, call (915) 995-9524.”**

Esto elimina el duplicado exacto 19/26 y reduce el solapamiento 5/12 sin alterar precio ni términos.

### 7. Coherencia con el Markdown

Corregir el Markdown de planificación para que vuelva a ser una referencia fiable, sin alterar los 30 temas aprobados:

1. **Líneas 71–77 / Gate de aprobación:** ya no debe decir “Redactar los 30 copys AIDA completos” como tarea futura; el JSON ya contiene esos 30 copys. Cambiar el estado a “copy redactado, pendiente de correcciones bloqueantes y aprobación”.
2. **Distribución final:** la frase “BOTOX® con fotos reales: días 6, 10, 14, 22 y 24” es imprecisa. El día 24 es una pieza de Trust/Prepared with Care basada en materiales, no una pieza BOTOX® Cosmetic. Separar así:
   - **BOTOX® Cosmetic: días 6, 10, 14 y 22.**
   - **Trust/preparación con activo real de materiales: día 24.**
3. **Día 28:** el Markdown dice “Consultar precio/disponibilidad”, pero el JSON únicamente pregunta por disponibilidad. Elegir una sola versión; no añadir “precio” sin confirmación del cliente. Recomendación: cambiar el Markdown a **“Consultar disponibilidad”** para coincidir con el JSON.
4. Actualizar en el Markdown cualquier texto BOTOX® visible incompleto para usar siempre **BOTOX® Cosmetic**.

## Controles que sí pasaron

- 30 registros consecutivos, días 1–30; fechas mostradas coherentes con `scheduledAt`.
- AIDA estructural completo en todos los registros.
- Teléfono oficial correcto en todas las apariciones.
- No se encontró `$149.99` ni mezcla de ese precio con la oferta de `$64.99`.
- Los cuatro martes incluyen 21+ en el copy.
- No hay hooks exactos duplicados.
- Microneedling de cuero cabelludo no garantiza crecimiento; cicatrices se limitan a ciertas cicatrices totalmente curadas y evaluación individual.

## Gate de reauditoría

Después de aplicar cambios, volver a revisar **JSON, Markdown y todo texto visible en las imágenes**. La campaña no debe publicarse hasta comprobar: marcas completas, disclaimers aplicables, oferta literal, 21+, teléfono, ausencia de claims obsoletos y confirmación escrita de términos/regulación por el cliente.
