# 00 · Resumen (versión 2) — Proyecto final ECON-3785: efectos heterogéneos de largo plazo de la crisis de 1998 en Indonesia (IFLS)

Fecha: 10-nov-2026 · Estado: borrador para discusión del equipo y para la asesoría de semana 15.

## En una frase

Replicar con la IFLS el efecto promedio del alza del precio del arroz de 1997-98 sobre resultados de largo plazo y estimar **para quién fue peor** con bosques y árboles causales, incluyendo salud mental medida con las escalas de la encuesta.

## Qué cambió en la versión 2

| Punto | Cambio |
|---|---|
| Texto como datos | **Eliminado.** La IFLS no trae texto de salud mental. La salud mental entra como resultado cuantitativo (ítems GHQ 1993/2000, CES-D-10 2007/2014). |
| Métodos del curso | Revisados en la carpeta: Lasso (`glmnet`), árboles (`rpart`), bosques (`ranger`), árbol causal honesto escrito a mano (Lab 09), bosque causal con `grf` y `clusters` (Lab 10). Se retira lo espacial y el paquete `causalTree`. |
| Citas de memoria | Las seis verificadas. Una corrección: Block et al. (2004) no usa la IFLS sino datos de Java rural. |
| Literatura | Entra Frankenberg y Thomas (2017), que casi no encuentra efectos de largo plazo: el ATE a replicar está en disputa. |
| Identificación | Ampliada con seis precedentes de diseño y una evaluación de usar otros países. |

## Seis conclusiones

1. **Hay un ATE publicado para replicar, pero no hay consenso.** Elmira y Qaim (2025) encuentran −0,135 en talla-para-edad por +100 % en el precio del arroz y menor estatura adulta. Frankenberg y Thomas (2017), con un diseño de cohortes hasta 2014, casi no encuentran daño duradero en educación ni en estatura. Reconciliar ambos es parte del aporte.
2. **El tratamiento "más alza vs. menos alza" identifica un contraste, no el efecto de la crisis.** No hay comunidades sin tratar. Con tratamiento continuo se necesita un supuesto más fuerte que con terciles (Callaway, Goodman-Bacon y Sant'Anna).
3. **La principal amenaza son choques simultáneos** (sequía, humo de incendios, disturbios) correlacionados con el precio. Hay evidencia de que tuvieron efectos propios (Jayachandran; Rukumnuaykit).
4. **Los mejores respaldos están dentro de la IFLS:** cohortes mayores de la misma comunidad, hermanos de distinta edad, y productores netos de arroz como grupo de comparación (Yamauchi y Larson lo validan para 2007/08; Adhvaryu et al. usan la misma lógica en Ghana).
5. **Datos de otros países: no como respaldo de identificación.** Responden otra pregunta, dan un solo país tratado, los resultados no son comparables y suman 1-2 semanas. Sirven como referentes de magnitud y como extensión futura.
6. **Salud mental: dos preguntas.** (i) Adultos, panel 1993-2000 con ítems GHQ y exposición por precio comunitario, que mejora la medida provincial de Friedman y Thomas; (ii) niños de la crisis, CES-D en 2014, exploratoria.

## Diseño propuesto

| Etapa | Qué | Método (curso) |
|---|---|---|
| 1 | Replicar el ATE: niños 0-5 en 1997, HAZ 1997-2000 | `feols` con efectos fijos; Lasso para controles |
| 2 | Largo plazo: cohorte expuesta vs. mayores × intensidad, efectos fijos de comunidad | `feols` |
| 3 | Heterogeneidad: terciles de alza, X de 1997 | `grf::causal_forest` con `clusters`; `test_calibration`; TOC |
| 4 | Árbol honesto interpretable sobre puntajes doblemente robustos | `rpart` + partición por comunidad |
| 5 | Salud mental: GHQ 1993-2000 en adultos; CES-D 2014 | mismos métodos |
| 6 | Validación: tendencias previas 1993-97, placebos, hermanos, productores netos | `feols` |

## Decisiones pendientes del equipo

| Decisión | Recomendación |
|---|---|
| Cliente | Agencia que focaliza ayuda ante choques de precios de alimentos (p. ej., Programa Mundial de Alimentos) |
| Resultado principal | Estatura (replicación) + uno nuevo: salud mental de adultos 1993-2000 |
| Alcance mínimo | Etapas 1, 3, 4 y las pruebas de tendencias previas y balance |
| Qué se recorta primero | CES-D 2014 de los niños; educación y cognición |

## Riesgos principales

- **Tiempo:** armar el panel toma ≈ 2 semanas. Registrarse y descargar hoy.
- **Potencia:** ≈ 312 comunidades. La heterogeneidad puede no ser detectable; un nulo bien documentado es un resultado válido y coherente con Frankenberg y Thomas.
- **Identificación:** si las tendencias previas no dan cero, el diseño principal pasa a ser productores vs. compradores netos dentro de comunidad.

## Archivos

| Archivo | Contenido |
|---|---|
| `01_revision_literatura.md` | 5 artículos clave, contexto, fuentes de identificación, tabla de verificación de citas |
| `02_datos_ifls_acceso_y_manejo.md` | Acceso, estructura, variables y trampas de manejo |
| `03_estrategia_identificacion.md` | Estimandos, menú de diseños, amenazas, pruebas, evaluación de otros países |
| `04_arboles_causales_honestos.md` | Métodos del curso, bosque causal, árbol honesto, código base |
| `05_salud_mental.md` | Métricas, dos diseños, cautelas |
| `propuesta_borrador.pdf` | Borrador de propuesta con diagramas (v2) |

## Qué no está verificado

- Ningún número sale de los microdatos; todos vienen de los artículos citados.
- La ubicación de variables en los libros de la IFLS es la esperada según la documentación; confirmar en codebooks.
- Los fragmentos de código son esqueletos con nombres de variables ilustrativos; no se han ejecutado.
