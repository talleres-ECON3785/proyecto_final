# Proyecto final: ¿a quién golpeó más el arroz caro?

Ciencia de Datos y Econometría Aplicada (ECON-3785, 2026-2), Universidad de los
Andes.

## Objetivo

Indonesia vivió en 1997-98 una crisis financiera en la que el precio del arroz
se disparó, con alzas muy distintas entre comunidades. Con la Indonesia Family
Life Survey (IFLS, RAND), el proyecto:

1. **Replica** el efecto promedio del alza del precio del arroz sobre la
   estatura de los niños de 0 a 5 años (Elmira y Qaim 2026).
2. **Lo extiende** a la escolaridad completada en 2014 (resultado primario
   recomendado) y a la cognición.
3. **Estima para quién fue peor** con bosques causales honestos agrupados por
   comunidad, y compara una regla de focalización basada en el bosque con
   «focalizar en pobres».

**Cliente propuesto:** una agencia que focaliza ayuda ante choques de precios de
alimentos (tipo Programa Mundial de Alimentos). La pregunta del cliente es a qué
hogares proteger primero.

**Estrategia:** se compara a los niños de comunidades con mayor alza del precio
del arroz entre 1997 y 2000 con los de comunidades con menor alza, dentro de un
diseño de cohortes. Se identifica ese contraste, no el efecto total de la
crisis. El diseño completo está en [`10_Propuesta/`](10_Propuesta/) (documento
central: `04_heterogeneidad_bosques_honestos.md`).

## Cómo reproducir

1. **Datos:** la licencia de RAND no permite redistribuir la IFLS, así que este
   repositorio no la trae. Siga [`01_Datos/README.md`](01_Datos/README.md) para
   registrarse, descargar las cinco olas y ponerlas en `01_Datos/01_Crudos/`.
2. Abra `proyecto_final.Rproj` en RStudio (o fije el directorio de trabajo en la
   raíz del repositorio).
3. Corra `00_main.R`. Instala y carga los paquetes con `pacman`, verifica que los
   datos estén en su lugar, crea las carpetas de salida y ejecuta los scripts de
   `02_Scripts/` en orden. No hace falta instalar nada a mano.

Semilla: 2026 en todo paso aleatorio.

## Estructura

| Carpeta | Contenido |
|---|---|
| `00_main.R` | Script maestro: único punto de entrada |
| `01_Datos/` | `01_Crudos/` (IFLS de RAND, solo local; guías `.md` por ola), `02_Procesados/`, `03_Listos/` (solo local), síntesis de las cinco olas |
| `02_Scripts/` | Scripts numerados; `00_formato_*.R` (formato de figuras y tablas); `_exploratorio/` |
| `03_Resultados/` | `Tablas/` y `Figuras/`, una subcarpeta por script |
| `04_Presentaciones/` | Borradores de la asesoría y la sustentación |
| `05_Notas/` | Una nota por hallazgo, con la evidencia que la sostiene |
| `06_Bitacoras/` | Una bitácora por sesión de trabajo |
| `07_Recursos/` | Enunciado, catálogo de herramientas del curso, artículos (solo local) |
| `08_Entregables/` | Presentación final y `.zip` de entrega |
| `10_Propuesta/` | Propuesta v4: literatura, datos, identificación, heterogeneidad |

`HANDOFF.md` resume el estado y lo que sigue; `PLAN.md` es el plan por hitos;
`CLAUDE.md` y `01_Datos/CLAUDE.md` son las reglas de trabajo.

## Mapa script → resultados

### Scripts existentes

| Script | Qué hace | Salidas |
|---|---|---|
| `02_Scripts/00_formato_graficas.R` | Paleta, tema y `guardar_figura()` | — |
| `02_Scripts/00_formato_tablas.R` | Estilo `gt` y `guardar_tabla()` | — |
| `02_Scripts/_exploratorio/01_salud_mental_1993.py` | Índice de síntomas de 1993 (Python, fuera del pipeline) | `01_Datos/02_Procesados/salud_mental_1993.*` (local) |

### Scripts previstos (por llenar)

`01_tracks`, `02_precio_arroz`, `03_x_1997`, `04_haz_9700`,
`05_escolaridad_2014`, `06_cognicion`, `10_validacion`, `20_bosques`,
`40_focalizacion` (`10_Propuesta/02` §6).

## Paquetes

`tidyverse`, `gt`, `modelsummary`, `fixest`, `glmnet` y `grf` son los del curso.
**Ampliaciones** frente al curso: `haven` (lectura de `.dta`) y, de `grf`,
`get_scores`, `best_linear_projection` y `average_treatment_effect(subset = …)`;
`fwildclusterboot` si se usa. Cualquier otra se registra en `CLAUDE.md`
("Decisiones tomadas") antes de usarla.

## Datos y licencia

Los datos son de la Indonesia Family Life Survey (RAND). Se usan bajo sus
condiciones: no se redistribuyen ni se intenta identificar a personas, hogares o
comunidades. Las tablas y figuras de `03_Resultados/` solo contienen agregados.
