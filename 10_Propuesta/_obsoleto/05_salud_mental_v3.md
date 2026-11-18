# 05 · Salud mental como extensión opcional (versión 3)

> **Cambio de alcance (11-nov-2026, recomendación pendiente de confirmación del equipo).** Salud mental deja de ser parte del núcleo y pasa a **extensión opcional**. El núcleo es estatura + escolaridad completada + cognición (ver `06_literatura_escolaridad_cognicion.md`). Lo que sigue se conserva para cuando el núcleo esté terminado.
>
> Se mantiene la decisión del 10-nov: **no se procesa texto**. La IFLS mide salud mental con ítems cerrados.

## Por qué baja de prioridad

- **Hay referencia, pero descriptiva.** Friedman y Thomas (2009) documentan un aumento grande y persistente de la angustia en adultos (tristeza ≈ 12 % → 29 % en hombres y 16 % → 41 % en mujeres entre 1993 y 1998; casi sin descenso en 2000). No entregan un efecto promedio con precio comunitario que replicar.
- **Medida armonizable pobre.** Solo tres síntomas (insomnio, tristeza, ansiedad) se repiten entre 1993 y 2000, y se dicotomizan o se suman en un índice de 0 a 6.
- **Ventana de identificación débil.** La ola de 1998 (IFLS2+), usada por Friedman y Thomas, **no está en la descarga pública**; la 1997 no tiene ítems psicológicos. Con los datos públicos queda un panel de dos puntos (1993 y 2000) y una sola ola previa a la crisis, cuatro años antes.
- **Confusión con otros eventos** entre 1993 y 2000 (transición política, disturbios, sequía).
- **Ruido para CATEs.** Un resultado binario o de 7 valores, con ~312 comunidades, es el caso menos favorable para un bosque causal.
- **Sin ancla para el pipeline.** Si el resultado es nulo, no se puede distinguir entre exposición, medida y método.

Ventaja que sí tiene: el índice de 1993 ya está construido (`codigo/01_salud_mental_1993.py`, salida en `Datos/derivados/salud_mental_1993.{csv,dta}`), con `sm3_93` (insomnio + tristeza + ansiedad, 0-6) y `sm6_93` (los seis ítems de 1993, solo línea base). Eso baja el costo de la extensión.

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

## Dos preguntas posibles (ambas exploratorias)

### Pregunta 1 · Adultos: ¿el alza del arroz se asocia con el aumento de angustia 1993-2000?

Es la prioritaria dentro de la extensión.

- **Muestra:** adultos con ítems GHQ en 1993 y 2000 (Friedman y Thomas trabajan con ≈ 10.500).
- **Diseño B (archivo 03):** panel de dos períodos con efectos fijos individuales; exposición = Δlog(precio del arroz) de la comunidad de 1997.
- **Aporte posible:** Friedman y Thomas miden la intensidad con el cambio del gasto en 13 provincias, que es endógeno y da una pendiente rural no significativa. El precio comunitario da ~312 unidades y es más exógeno al hogar.
- **Persistencia:** los mismos adultos tienen CES-D en 2007 y 2014, pero con otra escala; solo se puede comparar el cambio estandarizado.
- **Validación:** con una sola ola previa, la prueba de tendencias previas con el propio resultado es limitada. Complementar con un placebo sobre salud general autorreportada, que según Friedman y Thomas casi no cambió.
- **Sin CATEs.** Análisis descriptivo y de efectos promedio, con la heterogeneidad declarada de antemano (baja educación, rurales sin tierra, urbanos, mujeres).

### Pregunta 2 · Niños de la crisis: ¿mayor exposición temprana ⇒ más síntomas depresivos de adultos jóvenes?

Solo si sobra tiempo; la más débil.

- **Muestra:** cohorte de 0-5 años en 1997, CES-D en 2014 (17-23 años).
- **Diseño C:** cohorte expuesta vs. cohortes mayores de la misma comunidad × intensidad del alza, con efectos fijos de comunidad y cohorte. Sin línea base propia de salud mental; controlar por la angustia de la madre en 1993.
- **Precedente:** Adhvaryu, Fenske y Nyshadham (2019): en Ghana, un precio más alto del cacao en la primera infancia reduce la angustia mental severa en la adultez en regiones cacaoteras frente a las demás, con la nutrición materna y las inversiones en la niñez como canales.
- **Canal propio:** Elmira y Qaim documentan menor estatura adulta; la salud física es un mediador plausible. No controlar por ella en la especificación principal (es resultado del tratamiento).
- **Potencia baja:** cohorte de ≈ 2.000 personas, resultado ruidoso y 17 años de distancia. Si se incluye, declararla exploratoria.

## Cómo entra a los árboles y bosques causales

Solo si el equipo decide extender los CATEs a este resultado (no es la recomendación):

- Mismo código del archivo 04, cambiando `Y` por el CES-D estandarizado (pregunta 2) o por el cambio del índice GHQ (pregunta 1).
- Covariables de heterogeneidad adicionales: religión (Friedman y Thomas la incluyen porque afecta el reporte de síntomas), angustia de la madre o del propio individuo en 1993, tenencia de tierra.
- Antes de interpretar, pasar la prueba de calibración. Con poca señal, reportar el nulo.

## "Dimensiones" de salud mental sin texto

1. **Subescalas del CES-D-10.** Suele tener dos factores: afecto depresivo/síntomas somáticos (8 ítems) y afecto positivo (2 ítems). Estimar el efecto por subescala.
2. **Ítem por ítem** para el panel GHQ: tristeza, ansiedad e insomnio por separado, como Friedman y Thomas.
3. **Resultados vecinos de 2014:** afecto positivo y negativo, problemas de sueño, rasgos de personalidad (neuroticismo). Tratarlos como familia de resultados y corregir por pruebas múltiples.

## Qué sabemos que responde el CES-D en Indonesia

- Christian, Hensel y Roth (2019) usan los puntajes de depresión de la IFLS para mostrar que los choques de productividad agrícola (lluvia) afectan la depresión: la escala es sensible a choques económicos.
- Estudios descriptivos con IFLS5 encuentran ≈ 22 % de adultos sobre el punto de corte y asociación con adversidad en la niñez, incluido haber pasado hambre, y con bajo nivel socioeconómico infantil. Son correlaciones, pero muestran que la relación infancia-depresión adulta existe en estos datos.

## Cautelas

- **Potencia baja**, sobre todo en la pregunta 2.
- **Mortalidad y migración selectivas** afectan quién llega a 2014.
- **Sesgo de reporte** diferencial por educación y religión.
- **Edad al medir:** 17-23 años es un tramo de alta prevalencia de síntomas; controlar edad flexiblemente.
- **Comparaciones múltiples** si se estiman varias subescalas e ítems.

## Prioridad sugerida

1. Terminar el núcleo (estatura, escolaridad, cognición y CATEs).
2. Con tiempo sobrante, la pregunta 1 como análisis descriptivo y de efectos promedio.
3. La pregunta 2 solo como apéndice exploratorio.
