# 05 · Salud mental como resultado, con las métricas de la encuesta (versión 2)

> Decisión del equipo (10-nov-2026): **se abandona el procesamiento de texto**. La IFLS mide salud mental con ítems cerrados; se integra como resultado cuantitativo dentro del mismo diseño de identificación y los mismos métodos.

## Qué mide la IFLS

| Ola | Instrumento | Población | Uso |
|---|---|---|---|
| 1993 | Ítems adaptados del General Health Questionnaire: tristeza, ansiedad, insomnio, fatiga, irritabilidad, dolores ("últimas 4 semanas"; a menudo / a veces / nunca) | Adultos | Línea base pre-crisis |
| 2000 | Tristeza, ansiedad, insomnio (los tres comunes) | Adultos | Corto plazo |
| 2007 | CES-D de 10 ítems (sección KP, libro 3B) | 15+ | Mediano plazo |
| 2014 | CES-D-10; además personalidad (Big Five), afecto positivo y negativo, calidad del sueño | 15+ | Largo plazo |

La ola de 1998, que también tenía los ítems GHQ, no está en la descarga pública.

Notas de medición:

- CES-D-10: puntaje 0-30; punto de corte habitual ≥ 10. Usar el puntaje continuo como resultado principal y el binario como secundario.
- La escala no está validada contra diagnóstico clínico en Indonesia. Un análisis IRT con IFLS5 encuentra algunos ítems débiles pero confiabilidad global aceptable e información concentrada en síntomas medios y severos.
- GHQ (1993/2000) y CES-D (2007/2014) no son la misma escala: estandarizar dentro de ola y no comparar niveles entre instrumentos.
- Son tamizajes de síntomas, no diagnósticos.

## Dos preguntas, dos diseños

### Pregunta 1 · Adultos: ¿el alza del arroz explica el aumento de angustia 1993-2000?
- **Muestra:** adultos con ítems GHQ en 1993 y 2000 (Friedman y Thomas trabajan con ≈ 10.500).
- **Diseño B (archivo 03):** panel de dos períodos con efectos fijos individuales; exposición = Δlog(precio del arroz) de la comunidad de 1997.
- **Aporte:** Friedman y Thomas miden la intensidad con el cambio del gasto en 13 provincias, que es endógeno y da una pendiente rural no significativa. El precio comunitario da 312 unidades y es más exógeno al hogar.
- **Extensión:** los mismos adultos tienen CES-D en 2007 y 2014 → persistencia a 9 y 16 años.
- **Ventaja:** hay pre-período, así que se puede hacer la prueba de tendencias previas con el propio resultado solo de forma limitada (una ola previa); complementar con placebo sobre salud general autorreportada, que según Friedman y Thomas casi no cambió.

### Pregunta 2 · Niños de la crisis: ¿mayor exposición temprana ⇒ más síntomas depresivos de adultos jóvenes?
- **Muestra:** cohorte de 0-5 años en 1997, CES-D en 2014 (17-23 años).
- **Diseño C:** cohorte expuesta vs. cohortes mayores de la misma comunidad × intensidad del alza, con efectos fijos de comunidad y cohorte. Sin línea base propia de salud mental; controlar por la angustia de la madre en 1993.
- **Precedente:** Adhvaryu, Fenske y Nyshadham (2019): en Ghana, un precio más alto del cacao en la primera infancia reduce la angustia mental severa en la adultez en regiones cacaoteras frente a las demás, con la nutrición materna y las inversiones en la niñez como canales.
- **Canal propio:** Elmira y Qaim documentan menor estatura adulta; la salud física es un mediador plausible. No controlar por ella en la especificación principal (es resultado del tratamiento).

## Cómo entra a los árboles y bosques causales

- Mismo código del archivo 04, cambiando `Y` por el CES-D estandarizado.
- Covariables de heterogeneidad adicionales: religión (Friedman y Thomas la incluyen porque afecta el reporte de síntomas), angustia de la madre o del propio individuo en 1993, tenencia de tierra.
- Hipótesis a declarar: más efecto en baja educación, rurales sin tierra y urbanos (Friedman y Thomas); en mujeres, que reportan más síntomas y transitan más.

## "Dimensiones" de salud mental sin texto

El interés original era mirar la salud mental en más de una dimensión. Con las métricas disponibles:

1. **Subescalas del CES-D-10.** Suele tener dos factores: afecto depresivo/síntomas somáticos (8 ítems) y afecto positivo (2 ítems). Estimar el efecto por subescala.
2. **Ítem por ítem** para el panel GHQ: tristeza, ansiedad e insomnio por separado, como Friedman y Thomas.
3. **Resultados vecinos de 2014:** afecto positivo y negativo, problemas de sueño, rasgos de personalidad (neuroticismo). Tratarlos como familia de resultados y corregir por pruebas múltiples.

## Qué sabemos que responde el CES-D en Indonesia

- Christian, Hensel y Roth (2019) usan los puntajes de depresión de la IFLS para mostrar que los choques de productividad agrícola (lluvia) afectan la depresión: la escala es sensible a choques económicos.
- Estudios descriptivos con IFLS5 encuentran ≈ 22 % de adultos sobre el punto de corte y asociación con adversidad en la niñez, incluido haber pasado hambre, y con bajo nivel socioeconómico infantil. Son correlaciones, pero muestran que la relación infancia-depresión adulta existe en estos datos.

## Cautelas

- **Potencia baja en la pregunta 2.** La cohorte es de ≈ 2.000 personas, el resultado es ruidoso y han pasado 17 años. Declararlo exploratorio.
- **Mortalidad y migración selectivas** afectan quién llega a 2014.
- **Sesgo de reporte** diferencial por educación y religión.
- **Edad al medir:** 17-23 años es un tramo de alta prevalencia de síntomas; controlar edad flexiblemente.

## Prioridad sugerida

La pregunta 1 es más factible (muestra grande, pre-período, antecedente directo que mejorar). Si el tiempo alcanza para un solo resultado de salud mental, que sea ese; la pregunta 2 queda como extensión.
