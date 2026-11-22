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

### Cómo obtener la base lista para estimar

La base final (`01_Datos/03_Listos/base_estimacion.rds`: un niño por fila, con
ΔHAZ, tratamiento, características de 1997, `commid97` y provincia) **no está
en GitHub**: el repositorio es público y la licencia de RAND prohíbe
redistribuir los microdatos y sus derivados. Para tenerla basta con
`git pull` y correr `00_main.R` con los datos de RAND en `01_Datos/01_Crudos/`;
sale idéntica en la máquina de cada integrante.

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
| `02_Scripts/01_tracks.R` | Cohortes de 0-5 años en 1997 (principal) y en 1993 (placebo) desde el `ptrack`/`htrack` de 2000; `commid97`, `commid93`, provincia y urbano de 1997; desgaste por ola | `01_Datos/02_Procesados/tracks.rds` (local); `03_Resultados/Tablas/01_tracks/cohortes_desgaste.{png,csv}` |
| `02_Scripts/02_precio_arroz.R` | Precio del arroz por comunidad en 1997 y 2000 (posyandu y tiendas, Rp/kg, litros convertidos); dosis, cuartiles, terciles dentro de provincia y nacionales; marca de precio levantado en 1998 | `01_Datos/02_Procesados/precio_arroz.rds` (local); `03_Resultados/Figuras/02_precio_arroz/comunidades_distribucion_alza.png`; `03_Resultados/Tablas/02_precio_arroz/comunidades_resumen_precio.{png,csv}` |
| `02_Scripts/03_x_1997.R` | Características de 1997 de la cohorte principal: controles de E-Q sin los programas, moderadores pre-registrados (pobre con la línea de Widyanti et al. 2009), entrevista en 1998 | `01_Datos/02_Procesados/x_1997.rds` (local) |
| `02_Scripts/04_haz.R` | HAZ (OMS) de la cohorte principal en 1997 y 2000 y de la placebo en 1993 y 1997; edad en meses y medición en 1998 | `01_Datos/02_Procesados/haz.rds` (local); `03_Resultados/Tablas/04_haz/cohortes_haz_resumen.{png,csv}` |
| `02_Scripts/05_base.R` | Base lista para estimar (cohorte principal con precio y HAZ válido en 1997 y 2000) y desgaste según el alza | `01_Datos/03_Listos/base_estimacion.rds` (local); `03_Resultados/Tablas/05_base/ninos_desgaste_alza.{png,csv}`, `ninos_desgaste_alza_pendientes.csv` y, de la revisión P1.6, `ninos_haz1997_motivos`, `ninos_haz1997_balance`, `ninos_dhaz_cola` (`.png` y `.csv`) y `ninos_dhaz_cola_perfil.csv` |
| `02_Scripts/06_ate.R` | P2.1: efecto promedio del alza en el ΔHAZ (cuatro especificaciones con `feols`, EE agrupados y robustos, pendiente promedio del bosque, equivalente aproximado en cm) | `03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.{png,csv}` |
| `02_Scripts/07_cuartiles.R` | P2.2: forma del efecto con los cuartiles del alza (Q2-Q4 frente a Q1) en las cuatro especificaciones de `06_ate`; figura de la especificación 4 con las rectas de E-Q y del efecto promedio | `03_Resultados/Tablas/07_cuartiles/ninos_cuartiles_especificaciones.{png,csv}`; `03_Resultados/Figuras/07_cuartiles/ninos_cuartiles_coeficientes.png` |
| `02_Scripts/08_validacion.R` | P2.3: placebo (ΔHAZ 1993-1997 de la cohorte de 1993 sobre el alza 1997-2000, por comunidad de 1997 y de 1993) y robustez de la especificación 4 (sin precio de 1998, con pesos de la evaluación de salud de 2000, sin winsorizar, solo kg, sin \|ΔHAZ\| > 3) | `03_Resultados/Tablas/08_validacion/ninos_placebo.{png,csv}` y `ninos_robustez.{png,csv}` |
| `02_Scripts/09_interacciones_eq.R` | P3.1: réplica de las cinco interacciones de E-Q (edad 0-2, mujer, madre con más que primaria, pobre, urbano), una a la vez, con la dosis y la especificación 4; EE agrupados y robustos; Holm (F2) | `03_Resultados/Tablas/09_interacciones_eq/ninos_interacciones_eq.{png,csv}` |
| `02_Scripts/10_bosque.R` | P3.2: bosque causal (`grf`) con el tercil alto frente al bajo del alza dentro de provincia, X de 1997, agrupado por comunidad; traslape (`W.hat`) y ATE (AIPW) junto al MCO con el mismo tratamiento | `01_Datos/03_Listos/bosque_terciles.rds` (local); `03_Resultados/Figuras/10_bosque/ninos_bosque_traslape.png`; `03_Resultados/Tablas/10_bosque/ninos_bosque_ate.{png,csv}` |
| `02_Scripts/11_gate.R` | P3.3: seis GATE pre-declarados (edad 3-5, urbano, madre con más que primaria, mujer, comprador neto, pobre) con los puntajes AIPW del bosque de `10_bosque`; contrastes con `feols` agrupado y Holm (F1); BLP conjunta descriptiva | `03_Resultados/Tablas/11_gate/ninos_gate.{png,csv}`, `ninos_blp.{png,csv}` y, exploratorio, `ninos_edad_sin_cola_exploratorio.{png,csv}`; `03_Resultados/Figuras/11_gate/ninos_gate.png` |
| `02_Scripts/12_calibracion.R` | P4.1: `test_calibration` del bosque de `10_bosque` (predicción media y diferencial) | `03_Resultados/Tablas/12_calibracion/ninos_calibracion.{png,csv}` |
| `02_Scripts/13_perfil.R` | P4.3: perfil de los niños por cuartil del efecto predicho por el bosque (X de 1997 que el cliente observa); descriptivo | `03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.{png,csv}` |
| `02_Scripts/_exploratorio/01_salud_mental_1993.py` | Índice de síntomas de 1993 (Python, fuera del pipeline) | `01_Datos/02_Procesados/salud_mental_1993.*` (local) |

### Scripts previstos (por llenar)

El RATE con AUTOC de P4.2 (`PLAN.md`).

## Paquetes

`tidyverse`, `gt`, `modelsummary`, `fixest`, `glmnet` y `grf` son los del curso.
**Ampliaciones** frente al curso: `haven` (lectura de `.dta`), `anthro` y
`anthroplus` (HAZ con los estándares de la OMS) y, de `grf`,
`get_scores`, `best_linear_projection` y `average_treatment_effect(subset = …)`;
`fwildclusterboot` si se usa. Cualquier otra se registra en `CLAUDE.md`
("Decisiones tomadas") antes de usarla.

## Datos y licencia

Los datos son de la Indonesia Family Life Survey (RAND). Se usan bajo sus
condiciones: no se redistribuyen ni se intenta identificar a personas, hogares o
comunidades. Las tablas y figuras de `03_Resultados/` solo contienen agregados.
