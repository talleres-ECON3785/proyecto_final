# 06 · Literatura sobre escolaridad y cognición tras la crisis de 1998 (IFLS) y recomendación de alcance

Fecha: 10-nov-2026 (ajustado 11-nov-2026) · Complementa `00_resumen.md` (v3) y `01_revision_literatura.md`.

## Resumen en cinco puntos

1. **Escolaridad tiene antecedentes sólidos; cognición tiene antecedentes débiles.** Thomas et al. (2004) y Frankenberg y Thomas (2017) son trabajos de primer nivel sobre escolaridad. Para cognición solo hay un artículo con diseño causal explícito (Tsaneva, 2017) y varios trabajos menores (tesis, working papers, una revista regional).
2. **Casi todo mide la exposición como pobreza u hogar, no como precio del arroz.** La excepción es Rini y Kurniawati (2026), que usa el precio comunitario de alimentos como instrumento del gasto. Un ATE con el cambio del precio comunitario del arroz sobre escolaridad y cognición **no aparece en lo que pude revisar**. Esto no prueba que no exista; revisar Google Scholar antes de afirmarlo en la propuesta.
3. **Ninguno estima CATEs con métodos de bosques causales.** La heterogeneidad se explora con subgrupos escogidos a mano (urbano/rural, cuartil de gasto, edad, educación materna).
4. **Matiz importante sobre Frankenberg y Thomas.** El resumen v2 decía que "casi no encuentran daño duradero en educación". Eso es cierto para las cohortes de 7-12 y 13-16 años, pero **sí encuentran un déficit grande en la cohorte de 8 años de hogares urbanos pobres** (ver tabla). Es un resultado de heterogeneidad hallado a mano, que un bosque causal puede poner a prueba de forma sistemática.
5. **Recomendación:** núcleo = estatura (ancla) + escolaridad completada + cognición, con CATEs pre-especificados. Salud mental pasa a extensión opcional (sección 4).

## 1. Tabla de estudios

Nivel de verificación: **Texto** = leí el documento completo o la sección relevante; **Resumen** = solo abstract o página descriptiva; **Prensa** = solo notas de prensa o presentación. Las cifras con Texto vienen de mi lectura del documento; las demás son menos seguras.

| Estudio | Datos y exposición | Resultado | Hallazgo principal | Matices y limitaciones | Verificación |
|---|---|---|---|---|---|
| **Thomas, Beegle, Frankenberg, Sikoki, Strauss y Teruel (2004)**, *J. Dev. Econ.* 74(1) | IFLS2 (1997) e IFLS2+ (1998, submuestra 25%, 7 provincias); ~1.934 hogares; SUSENAS 1993-98. Exposición = cuartil de gasto per cápita 1997 y urbano/rural. Primeras diferencias | Matrícula, horas en la escuela, trabajo infantil, gasto educativo | La no matrícula de los menores subió; los hogares pobres protegieron a los mayores. En el panel IFLS, la brecha de matrícula por gasto creció en lo urbano (≈10 pp entre cuartiles). Horas diarias en la escuela −0,9; escolares que trabajan 3 % → 6 % | Verificado sobre la versión de trabajo (2001), no la de la revista. No hay horizonte largo. De 108 coeficientes de composición del hogar, 6 son significativos al 5 %, cifra compatible con el azar. Hay una posible inconsistencia entre texto y Tabla 3a en 16-19 años | Texto (WP 2001) |
| **Frankenberg y Thomas (2017/2019)**, NBER WP 23347; cap. en *Economics of Poverty Traps* | IFLS2, 2+, 3, 4, 5 (2014/15). Cohortes: 7-12 y 13-16 años en 1997 para matrícula; 5-21 años en 1997 para educación completada en 2014. "Expuesta" = 8 años en 1997, cuartil inferior urbano. Tendencia lineal por cohorte + indicador | Matrícula, educación completada, HAZ, peso | **Matrícula** 7-12 años: 3,1 % → 5,9 % (+90 %); pobres 4,9 % → 10,7 %. **Educación 2014:** cohortes 7-12 y 13-16 sin diferencia frente a la tendencia (+0,002 años, EE 0,17). **Cohorte urbana pobre de 8 años: −1,95 años (EE 0,63); −2,09 con controles; −1,24 (EE 0,69) con efectos fijos de hogar, significativo solo al 10 %.** Diferencia en diferencias urbano-rural: 1,97 años (EE 0,87). Estatura: sin efecto negativo en HAZ; los menores de 30 meses eran más altos en 2000 | La significancia del déficit depende de la especificación (baja ~40 % con efectos fijos). La muestra de menores de 30 meses es muy pequeña. El texto menciona "8 year olds in poor, rural households", pero la tabla apunta al grupo **urbano**; parece un error del texto. El resumen de prensa del HCEO dice solo "sin evidencia de menor educación"; es parcial. Una beca desde 1999 pudo mitigar el efecto | Texto (versión NBER) |
| **Tsaneva (2017)**, *World Dev. Perspectives* 6 | "Datos alrededor de la crisis" (la página no precisa la encuesta; presumiblemente IFLS). Value-added con puntajes antes/después del abandono + IV con restricciones de recursos de la crisis | Matemáticas y Raven | Efecto negativo "económica y estadísticamente significativo" del abandono sobre matemáticas; efecto menor sobre Raven | **No pude ver coeficientes ni tamaño de muestra** (texto de pago). Mide el efecto del abandono, no de la exposición a la crisis. Los instrumentos no pude evaluarlos | Resumen |
| **Irhamni (2017)**, tesis UMN, ensayo 2; presentación FKP/AMINEF 2018 | IFLS 2007 y 2014; ~8.159 niños de 0-5 años en 1997; 17 preguntas (12 cognitivas básicas, 5 de matemáticas). Compara hermanos del mismo hogar y hogares distintos con la misma brecha de edad entre hermanos | Cognición | Mayor efecto negativo en niños **urbanos expuestos en el útero**; en lo rural, en hogares **no agrícolas** | **No leí la tesis** (el enlace no cargó). No hay magnitudes ni errores estándar. Las ventanas de exposición más allá del útero no se mencionan en la fuente. La exposición no es el precio del arroz; es la crisis por cohorte de nacimiento | Prensa |
| **Wediawaty (2014)**, WoPEDS 201413, Unpad | IFLS; corte transversal agrupado; niños pobres | Salud infantil y cognición | En general no hay efectos negativos en pobres; en lo urbano, efecto negativo en ciertos grupos de edad; las ventanas críticas estarían en los primeros dos años. Gasto y educación materna predicen fuerte | **El PDF no cargó.** Sin cifras. Un documento de trabajo de universidad regional; el diseño es de corte transversal agrupado | Resumen |
| **Rini y Kurniawati (2026)**, *Jurnal Ekonomi Malaysia* 60(1) | IFLS2-IFLS3 (1997-2000); 4.204 niños; exposición = cambio del gasto del hogar; instrumento principal = **precio comunitario de alimentos** | Raven/matemáticas (17 preguntas, fracción correcta; media 0,62) | MCO ≈ 0 (no signif.); PSM entre −0,005 y −0,023 (no signif.); **IV: −0,0158, significativo al 10 %** (F primera etapa 17,3) | Doble definición del instrumento (precio de alimentos vs. caídas de gasto en varios rubros); revista regional; ventana corta (hasta 2000); datos de 2007/2014 solo descriptivos; el diseño es de panel aunque lo llaman corte transversal | Texto |
| **Ayanian (2014)**, tesis Colby | IFLS hasta 2007; niños nacidos antes/durante la crisis | Salud, cognición, educación | Cognición y educación sin efectos negativos de largo plazo; sí efectos en indicadores de salud | Tesis de pregrado, acceso restringido; sin detalles | Resumen |
| **Menéndez y Gignoux (2012)**, comunicación HAL | IFLS 1993, 1997, 2000, 2007; panel de hermanos; **choques de hogar** (desastres, cosechas, empleo, muertes) | Educación | En lo urbano, desastres, muertes y choques de mercado reducen la educación; en lo rural, la pérdida de cosecha. **Poca evidencia de que los choques tempranos duren más** | Resultados preliminares. **No es sobre la crisis ni el arroz** (corrijo mi mención previa). Útil como referente de diseño por hermanos | Resumen |
| **Elmira y Qaim (2026)**, *Global Food Security* 48, 100900 | IFLS 1993, 97, 00, 07, 14; ~2.100 niños de 0-5 años en 1997; precios comunitarios del arroz en **312 comunidades** (1997 y 2000); media nominal +83 %, real ≈ 0. Panel con efectos fijos individuales; controles de 1997 × año | HAZ, stunting, sobrepeso, estatura adulta, IMC | **HAZ −0,135 por +100 % nominal (−0,251 con precio real); stunting +3,5 pp; sobrepeso +3 pp.** 2014: **−0,65 cm** de estatura adulta; IMC y obesidad solo en el grupo de 3-5 años. Más fuerte en lo **urbano** y con **madres de primaria o menos**; **los niños más afectados que las niñas** | Los resultados de 2014 son **asociaciones, no causales** (OLS). Sin precios de 1999 (se usa 2000). Exogeneidad del precio es un supuesto. Los autores no pueden compartir los datos. Heterogeneidad por pobreza: no significativa | Texto |
| **Friedman y Thomas (2009)**, *World Bank Econ. Rev.* (versión PMC) | IFLS 1993, 1998 (submuestra 25 %), 2000; N≈10.500 adultos de 20+ en 1993. GHQ adaptado. Exposición = provincia, urbano/rural, tenencia de tierra, educación (1993) | Tristeza, ansiedad, insomnio, etc. | La tristeza pasó de ~12 % a ~29 % (hombres) y de ~16 % a ~41 % (mujeres) entre 1993 y 1998; casi no bajó en 2000 aunque el consumo ya se había recuperado | Solo 3 síntomas se repiten en las tres olas; síntomas dicotomizados; **sin preguntas psicológicas en 1997**; **la ola de 1998 que usan no está en la descarga pública**; el análisis provincial tiene pocas observaciones; no son diagnósticos clínicos; último dato 2000 | Texto |

Otros trabajos cercanos, sin lectura completa: Webb (2019, tesis PSE): choques climáticos en Indonesia, periodo crítico a los 2 años para cognición (solo rural, no es la crisis). RISE WP 026: perfiles de aprendizaje con las preguntas de numeracidad de la IFLS (útil para confirmar qué pruebas de matemáticas existen en qué ola).

## 2. Lo que sugiere la literatura sobre dónde buscar heterogeneidad

| Dimensión | Evidencia previa | Dirección esperada del efecto |
|---|---|---|
| Urbano vs. rural | Elmira y Qaim (HAZ), F&T (educación), Irhamni (cognición), Wediawaty | Mayor daño urbano |
| Edad en 1997 | F&T (8 años), Irhamni (útero), Elmira y Qaim (3-5 años), Wediawaty (0-2 años) | Ventanas distintas según el resultado: **no hay consenso** |
| Pobreza / gasto | Thomas et al. y F&T: concentrado en pobres. Elmira y Qaim: algo mayor en no pobres, no significativo | Ambigua |
| Educación materna | Elmira y Qaim; Wediawaty | Mayor daño con menor educación materna |
| Sexo | Elmira y Qaim: niños más afectados; F&T: sin diferencias | Ambigua |
| Hogar agrícola / productor neto | Irhamni (rural no agrícola); Elmira y Qaim (autoconsumo de arroz) | Mayor daño en compradores netos |
| Hermanos mayores en el hogar | Thomas et al. (los menores pagan el costo) | Mayor daño en menores con hermanos mayores |

Estas son las hipótesis que el bosque causal debería poder confirmar o desmentir.

## 3. Qué podría ser nuevo con la IFLS y los métodos del curso

1. **ATE con exposición común.** Un solo diseño (cambio del precio comunitario del arroz o terciles) aplicado a HAZ, años de escolaridad y cognición. Hoy cada resultado usa una exposición distinta (pobreza, cohorte, gasto, precio).
2. **CATEs sistemáticos.** `grf::causal_forest` con `clusters` por comunidad, `test_calibration` y TOC, más un árbol honesto interpretable. Pregunta concreta: ¿recupera el bosque la cohorte urbana pobre de 8 años de F&T y la heterogeneidad urbana/educación materna de Elmira y Qaim, sin escogerlas a mano?
3. **Reconciliar Elmira–Qaim con F&T.** Elmira y Qaim hallan daño en estatura; F&T no. Aplicar la misma exposición a estatura y educación, en las mismas cohortes, ayuda a ver si la diferencia viene del diseño o de la población.
4. **Cognición de largo plazo con una exposición continua.** Irhamni usa 2007 y 2014 con una exposición por cohorte; Rini y Kurniawati usan 1997-2000.

## 4. Salud mental: ¿conviene mantenerla?

**Aclaración sobre "no hay referencia".** Sí hay una: Friedman y Thomas (2009) documentan un aumento grande y persistente de la angustia en adultos. Pero es descriptivo, con exposición provincial, y no entrega un efecto promedio que replicar ni un contraste con precio comunitario.

| Criterio | Estatura (HAZ) | Escolaridad completada | Cognición | Salud mental (adultos, GHQ) | Salud mental (niños, CES-D 2014) |
|---|---|---|---|---|---|
| Ancla de ATE publicada | Sí (Elmira y Qaim) | Parcial (F&T, por cohorte) | Débil (Rini y Kurniawati, 10 %) | No (solo descriptivo) | No |
| Tamaño de muestra aproximado | ~2.100 (corto plazo) | miles (F&T: ~5.900 urbano y ~6.644 rural obs.) | ~4.200 a ~8.200 | ~10.500 | No verificado |
| Calidad de la medida | Buena (antropometría) | Buena | Media (17 ítems) | **Baja:** 3 síntomas binarios comunes a todas las olas | Por verificar en codebook |
| Pre-tendencia disponible | Sí (1993, 1997) | Sí (cohortes mayores) | Parcial | **Solo 1993** (sin ítems en 1997) | No |
| Riesgo de ruido en CATEs | Medio | Medio-bajo | Medio | **Alto** (resultado binario ruidoso; la ola de 1998 no está en la descarga pública) | Alto |
| Novedad | Replicación | Media | Alta | Media-alta | Alta |

**Mi lectura:**

- **A favor de mantenerla:** es el componente más original, y tiene sentido de política (la angustia persistió aunque el consumo se recuperó). Además, el índice de 1993 ya está construido en `codigo/01_salud_mental_1993.py`.
- **En contra, para este proyecto:** (i) sin ATE de referencia no podrá saber si un resultado nulo viene de la exposición, la medida o el método; (ii) la medida armonizable son tres ítems, con una ola base de 1993 (cuatro años antes de la crisis) y ninguna de 1997; (iii) la ventana 1993-2000 mezcla la crisis con la transición política; (iv) un bosque causal necesita un resultado con señal, y un resultado ruidoso con ~312 comunidades es el caso menos favorable; (v) construir el panel de adultos suma tiempo, y el resumen estima ≈2 semanas.
- **Evaluar lo ya hecho tiene más sentido** si el objetivo es una contribución metodológica clara (CATEs honestos) y entregable a tiempo. Escolaridad y cognición tienen más muestra, ancla parcial y una pregunta de heterogeneidad concreta (la cohorte de 8 años).

## 5. Recomendación de alcance

**Núcleo (incluir):**
1. **Replicar el ATE de estatura** (Elmira y Qaim): ancla de validación del pipeline.
2. **Escolaridad completada en 2014** (IFLS5) para cohortes de 5-21 años en 1997, con la misma exposición. Permite comparar con F&T y probar si el déficit de la cohorte urbana pobre de 8 años aparece de forma sistemática.
3. **Cognición** (Raven/matemáticas, 2007 y 2014) para las cohortes de 0-5 años en 1997, como el resultado nuevo. Confirmar en los codebooks qué ítems existen por ola y por edad.
4. **CATEs:** bosque causal con `clusters`, calibración, TOC y un árbol honesto, con las hipótesis de la sección 2 declaradas **antes** de ver los resultados.
5. **Pruebas de validación:** tendencias previas, placebos, hermanos y productores netos (ya en el plan).

**Extensión (solo si sobra tiempo):** salud mental de adultos con GHQ 1993-2000, como análisis descriptivo y de efectos promedio, sin CATEs y con las cautelas de la sección 4. CES-D 2014 de los niños solo como apéndice exploratorio.

**Resultado primario:** declarar uno (sugiero años de escolaridad en 2014 o HAZ, según los datos disponibles) y tratar el resto como secundarios, para limitar las comparaciones múltiples.

## 6. Qué no está verificado

- Ninguna cifra sale de los microdatos de la IFLS.
- Tsaneva (2017), Irhamni (2017) y Wediawaty (2014): no pude leer el texto completo; las descripciones vienen de resúmenes y presentaciones.
- Thomas et al. (2004) está verificado sobre el documento de trabajo de 2001.
- Menéndez y Gignoux: solo el resumen; el PDF estaba bloqueado.
- No he confirmado qué pruebas cognitivas se aplicaron a qué edades en 2007 y 2014; esto determina si la cohorte de 0-5 años en 1997 tiene puntajes comparables.
- Revisar en Google Scholar si ya existe un ATE del precio del arroz sobre escolaridad o cognición antes de presentar el aporte como novedoso.
- Los resúmenes de documentos largos los generó una herramienta de lectura automática; las cifras clave de F&T y Elmira y Qaim conviene contrastarlas con el PDF antes de citarlas.

## Fuentes

- Thomas et al. (2004), versión de trabajo: https://escholarship.org/content/qt1gh9r6rr/qt1gh9r6rr.pdf
- Frankenberg y Thomas (2017): https://www.nber.org/papers/w23347.pdf
- Elmira y Qaim (2026): https://www.sciencedirect.com/science/article/pii/S2211912425000756
- Tsaneva (2017): https://ideas.repec.org/a/eee/wodepe/v6y2017icp1-10.html
- Irhamni, presentación: https://www.fkpindonesia.org/?p=1607 · Tesis: https://hdl.handle.net/11299/195395
- Wediawaty (2014): https://econpapers.repec.org/RePEc:unp:wpaper:201413
- Rini y Kurniawati (2026): https://www.ukm.my/jem/wp-content/uploads/2026/01/jeko_601-2.pdf
- Ayanian (2014): https://digitalcommons.colby.edu/honorstheses/870
- Menéndez y Gignoux: https://ideas.repec.org/p/hal/journl/hal-01617427.html
- Friedman y Thomas: https://pmc.ncbi.nlm.nih.gov/articles/PMC4399497
- RISE WP 026: https://assets.publishing.service.gov.uk/media/5c335332ed915d730928e408/RISE_WP-026_Indonesia.pdf
- Webb (2019): https://dumas.ccsd.cnrs.fr/dumas-02407565/document
