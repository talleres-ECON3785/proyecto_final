# 00 · Resumen (versión 3) — Proyecto final ECON-3785: efectos heterogéneos de largo plazo de la crisis de 1998 en Indonesia (IFLS)

> Copia archivada el 17-nov-2026 desde el Project de claude.ai (`claude/resumen-propuesta-ifls.md`), reemplazada por la v4.

Fecha: 11-nov-2026 · Estado: borrador para discusión del equipo y para la asesoría de semana 15.

## En una frase

Replicar con la IFLS el efecto promedio del alza del precio del arroz de 1997-98 sobre estatura, y extenderlo a **escolaridad completada y cognición**, para estimar **para quién fue peor** con bosques y árboles causales. La salud mental pasa a extensión opcional.

## Qué cambió en la versión 3

| Punto | Cambio |
|---|---|
| Resultados | Núcleo = estatura (ancla) + escolaridad completada 2014 + cognición 2007/2014. Salud mental baja a extensión exploratoria (ver `06_literatura_escolaridad_cognicion.md`, sección 4). |
| Frankenberg y Thomas | **Corrección.** Sí encuentran un déficit de educación: −1,95 años (EE 0,63) en la cohorte de 8 años de hogares urbanos pobres, que baja a −1,24 con efectos fijos de hogar y es significativo solo al 10 %. Para las cohortes de 7-12 y 13-16 años no hay efecto. En estatura no hallan daño. |
| Literatura nueva | Revisión de escolaridad y cognición en `06_literatura_escolaridad_cognicion.md` (Thomas et al. 2004; Tsaneva 2017; Irhamni 2017; Rini y Kurniawati 2026; Wediawaty 2014; Menéndez y Gignoux 2012). |
| Hueco identificado | No encontré un ATE del precio del arroz sobre escolaridad o cognición, ni CATEs con bosques causales sobre estos resultados. **Falta confirmarlo en Google Scholar** antes de presentarlo como aporte. |
| Fecha de Elmira y Qaim | Aparece como 2026 en *Global Food Security* 48, 100900 (en línea en 2025). |

Se mantiene de la v2: texto como datos eliminado; métodos del curso (Lasso, `rpart`, `ranger`, árbol honesto del Lab 09, `grf` con `clusters` del Lab 10); seis citas de memoria verificadas, con la corrección de Block et al. (2004), que usa datos de Java rural y no la IFLS.

## Seis conclusiones

1. **Hay un ATE publicado para replicar, pero no hay consenso.** Elmira y Qaim (2026) encuentran −0,135 en talla-para-edad por +100 % en el precio nominal del arroz (−0,251 con precio real) y −0,65 cm de estatura adulta; los resultados de 2014 son asociaciones, no efectos causales. Frankenberg y Thomas (2017) no hallan daño en estatura y casi no lo hallan en educación, salvo en la cohorte urbana pobre de 8 años. Reconciliar ambos es parte del aporte.
2. **El tratamiento "más alza vs. menos alza" identifica un contraste, no el efecto de la crisis.** No hay comunidades sin tratar. Con tratamiento continuo se necesita un supuesto más fuerte que con terciles (Callaway, Goodman-Bacon y Sant'Anna).
3. **La principal amenaza son choques simultáneos** (sequía, humo de incendios, disturbios) correlacionados con el precio. Hay evidencia de que tuvieron efectos propios (Jayachandran; Rukumnuaykit).
4. **Los mejores respaldos están dentro de la IFLS:** cohortes mayores de la misma comunidad, hermanos de distinta edad, y productores netos de arroz como grupo de comparación (Yamauchi y Larson lo validan para 2007/08; Adhvaryu et al. usan la misma lógica en Ghana).
5. **Datos de otros países: no como respaldo de identificación.** Responden otra pregunta, dan un solo país tratado, los resultados no son comparables y suman 1-2 semanas. Sirven como referentes de magnitud y como extensión futura.
6. **Escolaridad y cognición tienen más muestra y una pregunta de heterogeneidad concreta.** Frankenberg y Thomas hallaron a mano un déficit de ~2 años en la cohorte urbana pobre de 8 años; Elmira y Qaim hallan más daño en lo urbano y con madres de baja educación; Irhamni halla más daño en cognición con exposición en el útero. La pregunta es si el bosque causal recupera esos subgrupos sin escogerlos de antemano. Salud mental tiene una referencia descriptiva (Friedman y Thomas, 2009), pero solo tres síntomas binarios comparables entre olas y ningún ítem en 1997.

## Diseño propuesto

| Etapa | Qué | Método (curso) |
|---|---|---|
| 1 | Replicar el ATE: niños 0-5 en 1997, HAZ 1997-2000 | `feols` con efectos fijos; Lasso para controles |
| 2 | Largo plazo: estatura 2014 y **escolaridad completada 2014** (cohortes 5-21 años en 1997); cohorte expuesta vs. mayores × intensidad, efectos fijos de comunidad | `feols` |
| 3 | **Cognición** (Raven y matemáticas, 2007/2014) en cohortes de 0-5 años en 1997 | `feols` |
| 4 | Heterogeneidad con hipótesis declaradas de antemano: urbano, edad en 1997, educación materna, sexo, pobreza, productor/comprador neto de arroz | `grf::causal_forest` con `clusters`; `test_calibration`; TOC |
| 5 | Árbol honesto interpretable sobre puntajes doblemente robustos | `rpart` + partición por comunidad |
| 6 | Validación: tendencias previas 1993-97, placebos, hermanos, productores netos | `feols` |
| Extensión | Salud mental de adultos, GHQ 1993-2000, descriptiva y sin CATEs | `feols` |

## Decisiones pendientes del equipo

| Decisión | Recomendación |
|---|---|
| Cliente | Agencia que focaliza ayuda ante choques de precios de alimentos (p. ej., Programa Mundial de Alimentos) |
| Resultado principal | Declarar uno solo antes de ver resultados: años de escolaridad en 2014 o HAZ, según los datos disponibles. El resto como secundarios, para limitar las comparaciones múltiples. |
| Alcance mínimo | Etapas 1, 2, 4, 5 y las pruebas de tendencias previas y balance |
| Qué se recorta primero | CES-D 2014 de los niños; luego salud mental de adultos; cognición antes que escolaridad si el tiempo aprieta |
| ¿Mantener salud mental como núcleo? | Recomendación: no. Pasa a extensión. Decisión del equipo. |

## Riesgos principales

- **Tiempo:** armar el panel toma ≈ 2 semanas. Registrarse y descargar hoy.
- **Potencia:** ≈ 312 comunidades. La heterogeneidad puede no ser detectable; un nulo bien documentado es un resultado válido y coherente con Frankenberg y Thomas. La estatura de corto plazo tiene ~2.100 niños; escolaridad y cognición tienen más muestra.
- **Identificación:** si las tendencias previas no dan cero, el diseño principal pasa a ser productores vs. compradores netos dentro de comunidad.
- **Cognición:** no he confirmado qué pruebas se aplicaron a qué edades en 2007 y 2014. Esto define si la cohorte de 0-5 años en 1997 tiene puntajes comparables.
- **Comparaciones múltiples:** tres resultados y varias dimensiones de heterogeneidad aumentan el riesgo de falsos positivos. Pre-especificar hipótesis.

## Archivos

| Archivo | Contenido |
|---|---|
| `01_revision_literatura.md` | 5 artículos clave, contexto, fuentes de identificación, tabla de verificación de citas |
| `02_datos_ifls_acceso_y_manejo.md` | Acceso, estructura, variables y trampas de manejo |
| `03_estrategia_identificacion.md` | Estimandos, menú de diseños, amenazas, pruebas, evaluación de otros países |
| `04_arboles_causales_honestos.md` | Métodos del curso, bosque causal, árbol honesto, código base |
| `05_salud_mental.md` | Métricas, dos diseños, cautelas (ahora extensión opcional) |
| `06_literatura_escolaridad_cognicion.md` | **Nuevo.** Tabla de estudios, hipótesis de heterogeneidad, evaluación de salud mental y recomendación de alcance |
| `propuesta_borrador.pdf` | Borrador de propuesta con diagramas (v2; no refleja aún los cambios de la v3) |

## Qué no está verificado

- Ningún número sale de los microdatos; todos vienen de los artículos citados.
- La ubicación de variables en los libros de la IFLS es la esperada según la documentación; confirmar en codebooks.
- Los fragmentos de código son esqueletos con nombres de variables ilustrativos; no se han ejecutado.
- Tsaneva (2017), Irhamni (2017) y Wediawaty (2014) se conocen solo por resúmenes y presentaciones; no se leyeron los textos completos.
- Las cifras de Frankenberg y Thomas y de Elmira y Qaim vienen de resúmenes automáticos de los PDF; contrastarlas con el original antes de citarlas.
- Que no existan estudios previos de ATE o CATE del precio del arroz sobre escolaridad o cognición es una conclusión de una búsqueda acotada, no una garantía.
- `propuesta_borrador.pdf` y los archivos `01`-`05` no se han actualizado con la v3.
