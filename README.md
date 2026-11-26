# Proyecto final: ¿a quién golpeó más el arroz caro?

Ciencia de Datos y Econometría Aplicada (ECON-3785, 2026-2), Universidad de los
Andes.

## Objetivo

Indonesia vivió en 1997-98 una crisis financiera en la que el precio del arroz
se disparó, con alzas muy distintas entre comunidades. Con la Indonesia Family
Life Survey (IFLS, RAND) y la estatura de los niños de 0 a 5 años en 1997
(cambio del puntaje z de talla para la edad, ΔHAZ, entre 1997 y 2000), el
proyecto responde tres preguntas:

1. **¿Dolió?** Replica con `feols` el efecto promedio del alza del precio del
   arroz sobre el ΔHAZ (Elmira y Qaim 2026: −0,135 HAZ por +100 % del precio) y
   estudia su forma por cuartiles del alza, con un placebo 1993-1997.
2. **¿A quién?** Réplica de las cinco interacciones de Elmira y Qaim y seis
   efectos por grupo (GATE) pre-declarados con los puntajes AIPW de un bosque
   causal agrupado por comunidad, con corrección de Holm.
3. **¿El bosque supera a las reglas simples?** Calibración del bosque y RATE
   (AUTOC) del bosque frente a focalizar en pobres, urbanos o compradores netos
   de arroz.

**Cliente propuesto:** una agencia que focaliza ayuda ante choques de precios de
alimentos (tipo Programa Mundial de Alimentos). La pregunta del cliente es a qué
hogares proteger primero.

**Estrategia:** se compara a los niños de comunidades con mayor alza del precio
del arroz entre 1997 y 2000 con los de comunidades con menor alza. Se identifica
ese contraste, no el efecto total de la crisis. Las definiciones (tratamiento,
muestra, subgrupos y familias de Holm) están en
[`registro_decisiones.md`](registro_decisiones.md) y en el pre-registro de la
heterogeneidad,
[`10_Propuesta/07_preregistro_heterogeneidad.md`](10_Propuesta/07_preregistro_heterogeneidad.md).
Los hallazgos, uno por nota, están en [`05_Notas/`](05_Notas/README.md), y la
presentación final, en
[`08_Entregables/presentacion_final.pdf`](08_Entregables/presentacion_final.pdf).

## Cómo reproducir

### Requisitos

- **R** 4.6.1 (versión con la que se verificó). Los paquetes los instala
  `00_main.R` con `pacman`; las versiones verificadas fueron `tidyverse` 2.0.0,
  `haven` 2.5.5, `anthro` 1.1.0, `anthroplus` 1.1.0, `gt` 1.4.0,
  `modelsummary` 2.6.0, `fixest` 0.14.2 y `grf` 2.6.1.
- **Google Chrome o Chromium**, para exportar las tablas a `.png`
  (`guardar_tabla()` en `02_Scripts/00_formato_tablas.R`). Se busca en las rutas
  habituales de macOS, Linux y Windows; si está en otra, defina la variable de
  entorno `CHROME_PATH`.
- **Datos de la IFLS** (RAND), que no vienen en el repositorio (ver abajo).

### Pasos

1. **Datos:** la licencia de RAND no permite redistribuir la IFLS, así que
   cada quien la descarga con su propia cuenta (gratis):
   1. Regístrese y acepte las condiciones de uso en
      <https://www.rand.org/health/surveys/FLS/IFLS/access.html>
      («Register to Download Data»). La página general de la IFLS es
      <https://www.rand.org/well-being/social-and-behavioral-policy/data/FLS/IFLS.html>.
   2. Descargue, en formato Stata (`.dta`), los **datos de hogar** y los
      **datos comunitarios** de **IFLS1 (1993), IFLS2 (1997) e IFLS3 (2000)**,
      y descomprímalos. IFLS4 e IFLS5 no hacen falta.
   3. Póngalos en `01_Datos/01_Crudos/` con estos nombres de carpeta:

      ```
      01_Datos/01_Crudos/
      ├── IFLS1/  Household Data/   Community Data/
      ├── IFLS2/  Household Data/   Community Data/
      └── IFLS3/  Household Data/   Community Data/
      ```

   `00_main.R` se detiene con un mensaje si falta alguna carpeta
   `Household Data`. El detalle (módulos que vienen aparte, cuántos `.dta` debe
   haber en cada carpeta para comprobar la descarga y cómo citar cada ola) está
   en [`01_Datos/README.md`](01_Datos/README.md).
2. Abra `proyecto_final.Rproj` en RStudio (o fije el directorio de trabajo en la
   raíz del repositorio).
3. Corra `00_main.R`. Instala y carga los paquetes, verifica que los datos estén
   en su lugar, crea las carpetas de salida y ejecuta los 15 scripts de
   `02_Scripts/` en orden. No hace falta instalar nada a mano.

`00_main.R` regenera, desde los datos crudos, las bases de `01_Datos/02_Procesados/`
y `01_Datos/03_Listos/` y todo `03_Resultados/`. Se comprobó el 25-nov-2026
borrando esas tres carpetas y corriéndolo de principio a fin: terminó sin
errores en unos 3 minutos (macOS 27, Apple silicon, un hilo).

### Reproducibilidad de las cifras

- Todo paso aleatorio usa la semilla 2026 (`set.seed(2026)`; en `grf`,
  `seed = 2026` y `num.threads = 1`). En un mismo computador, dos corridas dan
  los mismos `.csv`, idénticos bit a bit.
- Las estimaciones con `feols` (scripts 06 a 09) son iguales en cualquier
  computador, salvo ruido de punto flotante en el decimal 15.
- Las del bosque causal (scripts 10 a 14) **pueden cambiar en el tercer decimal
  de un computador a otro**, aun con la misma semilla, porque `grf` no garantiza
  los mismos números entre plataformas. Las versionadas en `03_Resultados/` (y
  las de la presentación y las notas) salieron de la corrida completa del
  25-nov-2026 descrita arriba. Entre dos computadores del equipo, el AUTOC del
  bosque fue 0,115 y 0,116, y la menor p de Holm de la familia F3, 0,503 y
  0,492; ninguna conclusión cambia. Ningún script exige que una cifra coincida
  con un valor fijo.

### Cómo obtener la base lista para estimar

La base final (`01_Datos/03_Listos/base_estimacion.rds`: un niño por fila, con
ΔHAZ, tratamiento, características de 1997, `commid97` y provincia) **no está
en GitHub**: el repositorio es público y la licencia de RAND prohíbe
redistribuir los microdatos y sus derivados. La genera `00_main.R` (scripts 01 a
05) a partir de los datos de RAND en `01_Datos/01_Crudos/`.

### La presentación

`08_Entregables/presentacion_final.pdf` está versionado. Lo construye
`04_Presentaciones/_fuente/construir_presentacion.py` (Python, fuera de
`00_main.R`) con las figuras de `15_figuras_presentacion` y tablas leídas de los
`.csv` de `03_Resultados/`. Para reconstruirlo hacen falta `python-pptx`,
`pandas`, `pymupdf`, `pillow` y LibreOffice, además de la imagen de portada,
que no se versiona porque tiene derechos de terceros. Uso, desde la raíz:
`python 04_Presentaciones/_fuente/construir_presentacion.py`.

## Estructura

| Carpeta | Contenido |
|---|---|
| `00_main.R` | Script maestro: único punto de entrada |
| `01_Datos/` | `01_Crudos/` (IFLS de RAND, solo local; guías `.md` por ola), `02_Procesados/` y `03_Listos/` (solo local), síntesis de las cinco olas |
| `02_Scripts/` | Scripts numerados; `00_formato_*.R` (formato de figuras y tablas); `_exploratorio/` (fuera del pipeline) |
| `03_Resultados/` | `Tablas/` y `Figuras/`, una subcarpeta por script |
| `04_Presentaciones/` | Guion, notas del orador, estructura y fuente de la presentación |
| `05_Notas/` | Una nota por hallazgo, con la evidencia que la sostiene |
| `06_Bitacoras/` | Una bitácora por sesión de trabajo |
| `07_Recursos/` | Enunciado, catálogo de herramientas del curso, artículos (solo local) |
| `08_Entregables/` | Presentación final (`presentacion_final.pdf`) |
| `10_Propuesta/` | Propuesta histórica (no se consulta); vigente solo `07_preregistro_heterogeneidad.md` |

`registro_decisiones.md` reúne lo confirmado; `PLAN.md`, el plan por hitos;
`HANDOFF.md`, el estado; `CLAUDE.md` y `01_Datos/CLAUDE.md`, las reglas de
trabajo.

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
| `02_Scripts/12_calibracion.R` | P4.1: `test_calibration` del bosque de `10_bosque` (predicción media y diferencial); distribución descriptiva de los efectos predichos τ̂(x) | `03_Resultados/Tablas/12_calibracion/ninos_calibracion.{png,csv}`; `03_Resultados/Figuras/12_calibracion/ninos_cate_distribucion.png` |
| `02_Scripts/13_perfil.R` | P4.3: perfil de los niños por cuartil del efecto predicho por el bosque (X de 1997 que el cliente observa); descriptivo | `03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.{png,csv}` |
| `02_Scripts/14_rate.R` | P4.2: RATE con AUTOC en dos mitades de comunidades (escala de daño): bosque (−τ̂) frente a pobre, urbano y comprador neto; diferencias con bootstrap emparejado y Holm (F3); mitades invertidas como robustez; curvas TOC | `03_Resultados/Tablas/14_rate/ninos_rate.{png,csv}`; `03_Resultados/Figuras/14_rate/ninos_rate_toc.png` |
| `02_Scripts/15_figuras_presentacion.R` | Siete figuras para proyectar (12 × 5,6 in, sin título): alza por comunidad, efecto principal frente a E-Q, robustez y placebo, efecto por grupo, potencia, focalización y distribución de los efectos predichos. No estima nada nuevo: lee los `.csv` de `03_Resultados/` (y, para la primera, la base de precios y, para la última, el bosque guardado por `10_bosque`) | `03_Resultados/Figuras/15_figuras_presentacion/f1_alza.png` … `f7_cate_distribucion.png` |
| `04_Presentaciones/_fuente/construir_presentacion.py` | Construye la presentación final (Python, fuera de `00_main.R`) con las figuras de `15_figuras_presentacion` y tablas nativas desde los `.csv`; exporta el PDF y verifica tamaños de letra, contraste y textos montados | `08_Entregables/presentacion_final.pdf` (versionado) y `.pptx` (local) |
| `02_Scripts/_exploratorio/01_salud_mental_1993.py` | Índice de síntomas de 1993 (Python, fuera del pipeline) | `01_Datos/02_Procesados/salud_mental_1993.*` (local) |
| `02_Scripts/_exploratorio/mde_potencia.R` | Diferencia mínima detectable aproximada (≈ 2,8 × EE) a partir de los EE ya exportados (fuera del pipeline) | Salida en consola |

## Paquetes

Del curso: `tidyverse`, `gt`, `modelsummary`, `fixest` y `grf` (incluidos
`causal_forest`, `test_calibration` y `rank_average_treatment_effect`).
**Ampliaciones** frente al curso, registradas en `registro_decisiones.md` antes
de usarlas: `haven` (lectura de los `.dta`), `anthro` y `anthroplus` (HAZ con
los estándares de la OMS) y, de `grf`, `get_scores`, `best_linear_projection` y
`average_treatment_effect(subset = …)`. La lista única está en el
`pacman::p_load()` de `00_main.R`.

## Datos y licencia

Los datos son de la Indonesia Family Life Survey (RAND). Se usan bajo sus
condiciones: no se redistribuyen ni se intenta identificar a personas, hogares o
comunidades. Las tablas y figuras de `03_Resultados/` solo contienen agregados.

Citas de los datos, según la guía de usuario de cada ola:

- IFLS1: Frankenberg, E. y L. Karoly (1995). «The 1993 Indonesian Family Life
  Survey: Overview and Field Report». RAND, DRU-1195/1-NICHD/AID.
- IFLS2: Frankenberg, E. y D. Thomas (2000). «The Indonesia Family Life Survey
  (IFLS): Study Design and Results from Waves 1 and 2». RAND,
  DRU-2238/1-NIA/NICHD.
- IFLS3: Strauss, J., K. Beegle, B. Sikoki, A. Dwiyanto, Y. Herawati y F.
  Witoelar (2004). «The Third Wave of the Indonesia Family Life Survey (IFLS3):
  Overview and Field Report». RAND, WR-144/1-NIA/NICHD.
