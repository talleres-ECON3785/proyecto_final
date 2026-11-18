# 00 · Resumen (versión 4): Proyecto final ECON-3785 · ¿A quién golpeó más el arroz caro?

Fecha: 17-nov-2026 · Estado: borrador para el equipo y para la asesoría de la semana 15. Reemplaza la v3 (Project, 11-nov) y la v2 (copia local, 10-nov).

## En una frase

Con la IFLS, replicar el efecto promedio del alza del precio del arroz de 1997-98 sobre la estatura (Elmira y Qaim 2026), llevar la misma exposición a la **escolaridad completada en 2014** y estimar **para quién fue peor** con bosques y árboles causales honestos. Probamos además si el bosque recupera, sin buscarlos, los subgrupos que la literatura encontró a mano, y si una regla de focalización basada en el bosque supera a «focalizar en pobres».

## Qué cambió en la versión 4

| Punto | Cambio |
|---|---|
| Foco | La **heterogeneidad** pasa a ser el aporte central. Nuevo `04_heterogeneidad_bosques_honestos.md` (reemplaza `04_arboles_causales_honestos.md`): matriz de hallazgos previos, cinco vacíos, nueve hipótesis pre-declaradas y el flujo de inferencia |
| Citas | Los cinco artículos centrales se cotejaron contra los PDF de `07_Recursos/Articulos/`, con página y cuadro (`01` §6). Correcciones: E-Q usa 1997, 2000 y 2014 (no 1993/2007); el oro suaviza el consumo **solo en lo rural** (FST); las preguntas de 1993 son «adaptadas del GHQ» |
| Datos | Las cinco olas ya están revisadas. `02` trae **recomendaciones** para las 17 preguntas abiertas de la síntesis (unidad `commid97`, dos construcciones del precio, sin pesos, posición neta desde `b1_ks1`…) |
| Resultado primario | Recomendado: **escolaridad 2014** (7.925 obs.). ΔHAZ 1997-2000 queda como ancla de replicación |
| Diseño en el bosque | El resultado se transforma para que el bosque herede el diseño: primera diferencia (HAZ) o diferencia frente a la cohorte no expuesta de la misma comunidad (escolaridad). **Bosque placebo** en la cohorte no expuesta |
| Focalización | Comparación formal de reglas (bosque frente a pobre, urbano o comprador neto) con RATE/TOC (Yadlowsky et al. 2025) |

## Seis conclusiones

1. **El efecto promedio está en disputa.** E-Q: −0,135 HAZ por +100 % de precio nominal y −0,65 cm de estatura adulta (asociación) (p. 1, 5, 6). F-T 2017: sin daño en estatura (p. 12); en escolaridad, solo la cohorte urbana pobre de 8 años: −1,95 (0,63), −1,24 (0,69) con EF de hogar (cuadro 3). Un nulo bien documentado es un resultado válido.
2. **Todos encontraron la heterogeneidad a mano.** Una interacción a la vez (E-Q), celdas edad × zona × cuartil (F-T) o interacciones por zona (FST). Nadie probó si hay heterogeneidad en conjunto ni corrigió por lo que miró.
3. **Hay modificadores con buena teoría que nunca se probaron sobre los niños:** posición neta en arroz (F-L p. 414; FST p. 295), oro y tierra (FST p. 316-317), hermanos mayores y mujeres mayores (F-T 2017 p. 9-10; FST p. 313).
4. **La literatura se contradice en pobreza y edad.** Los pobres urbanos pierden más (F-L), pero los mejor situados caen más en gasto (FST, F-T) y algo más en HAZ (E-Q, n.s.). Un mismo método con una sola exposición puede ordenarlo.
5. **Se identifica un contraste (más alza frente a menos alza), no el efecto de la crisis.** La amenaza principal son los choques simultáneos (sequía, humo). La defensa son las tres capas (comunidades, cohortes, compradores frente a productores) y las pruebas de `03`.
6. **El cliente necesita saber a quién proteger primero.** El entregable es la priorización del bosque, el perfil de los hogares priorizados con variables observables y la evidencia de cuánto daño evita frente a focalizar por pobreza.

## Diseño

| Etapa | Qué | Método |
|---|---|---|
| 1 | Replicar el ATE: ΔHAZ 1997-2000, cohorte 0-5 (diseño B) | `feols`, cluster `commid97`; Lasso de doble selección |
| 2 | **Primario:** escolaridad 2014, cohortes de 5-21 años frente a la cohorte no expuesta (diseño C) | `feols` |
| 3 | Pruebas: tendencias previas, Yamauchi-Larson, balance, traslape, desgaste | `feols` |
| 4 | Heterogeneidad: bosque con `clusters`, calibración, BLP, GATE de H1-H8 (Holm) | `grf` |
| 5 | Recuperación de la celda de F-T y bosque placebo | `grf` + puntajes AIPW |
| 6 | Focalización: RATE del bosque frente a reglas simples | `rank_average_treatment_effect` |
| Sec. | Estatura adulta y cognición 2014 | Mismo flujo, exploratorio |
| Ext. | Salud mental adultos 1993-2000 | `feols`, sin CATEs |

**Alcance mínimo:** etapas 1-4 y 6 con el resultado primario. (18-nov: se retira el árbol causal; solo bosque causal.)

## Decisiones del equipo (con recomendación)

| Decisión | Recomendación |
|---|---|
| Cliente | Agencia que focaliza ayuda ante choques de precios de alimentos (tipo PMA) |
| Resultado primario | **Escolaridad completada en 2014** |
| Salud mental | Extensión opcional |
| Hipótesis H1-H9 | Aprobar y fijar por escrito antes de correr el bosque (`04` §4) |
| Construcción del precio | Principal (fuentes comunes 1997-2000, calidad media, kg) + réplica E-Q (`02` §5) |
| Cohorte no expuesta | 22-30 años en 1997 |
| Lenguaje | R para todo con `haven`, o Python solo para construir bases |
| Carpeta | Hecho el 18-nov: repositorio `talleres-ECON3785/proyecto_final` con la estructura de los talleres |

## Riesgos

- **Tiempo.** No se ha corrido ninguna estimación. Para la asesoría: precio por comunidad + pruebas 1-5 de `03`.
- **Potencia.** ~208 comunidades en la comparación por terciles. Si la calibración no rechaza, se reporta «sin evidencia de heterogeneidad» y se usan los GATE pre-declarados.
- **Medición del tratamiento.** Las fuentes de precio cambian entre olas (sin PKK en 2000); 27 comunidades se levantaron en 1998.
- **Construcción de X.** No hay agregado de gasto ni variable de posición neta en 1997: hay que construirlos.

## Archivos

| Archivo | Versión | Contenido |
|---|---|---|
| `01_revision_literatura.md` | v4 | Cinco artículos cotejados con PDF; heterogeneidad; tabla de verificación |
| `02_datos_ifls_acceso_y_manejo.md` | v4 | Tamaños de muestra reales; recomendaciones para las 17 preguntas abiertas |
| `03_estrategia_identificacion.md` | v4 | Diseños B/C/D y cómo entran al bosque; amenazas; 11 pruebas |
| `04_heterogeneidad_bosques_honestos.md` | v4 (nuevo) | Documento central |
| `05_salud_mental.md` | v4 | Extensión opcional, medidas corregidas |
| `06_literatura_escolaridad_cognicion.md` | v4 | Escolaridad y cognición; alcance |
| `propuesta_borrador.pdf` | v4 | Borrador con figuras |
| `_obsoleto/` | — | v2/v3 reemplazadas |

## Qué no está verificado

- Ningún número sale de estimaciones propias. Las cifras de datos vienen de las guías de ola (scripts de revisión); las de la literatura, de los PDF con página.
- Los apéndices de E-Q; los artículos sin PDF local (ver `01` §7 y `06` §6).
- El hueco de la literatura: dos búsquedas web, sin Google Scholar.
- Las funciones de `grf` marcadas en `04` §10.
