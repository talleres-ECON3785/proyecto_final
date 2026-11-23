# Bitácora — 2026-11-22 (5): RATE (P4.2) e insumos de la presentación

Samuel Escandón, sesión autónoma (sin confirmaciones; cada plan se escribe aquí
antes de implementarlo).

## Planes por tarea (escritos antes de implementar)

### Preparación

- Datos enlazados (17 uniones ya existían). Se sigue en el worktree
  `claude/hito-3-estimaciones-4919ca`, que avanzó por *fast-forward* a
  `origin/main` (`881bc78`, el PR #3 que llevó H3 a `main`); se empuja a
  `origin/SamuelEscandonC` al cerrar, como en la sesión (4).

### Parte A. P4.2: RATE del bosque frente a reglas simples (`14_rate.R`)

- **Qué hará.** Con la muestra, la X y el tratamiento de `10_bosque` (tercil
  alto = 1, bajo = 0 dentro de provincia):
  1. `set.seed(2026)` y partición de las 195 comunidades en dos mitades al azar
     (comunidad completa).
  2. Bosque A en la mitad 1 (`clusters = commid97`, `seed = 2026`,
     `num.threads = 1`, 4.000 árboles como `10_bosque`) → τ̂ en la mitad 2.
  3. Bosque de evaluación en la mitad 2 con **Y = −ΔHAZ** (escala de daño),
     mismas opciones.
  4. Muestra común: niños de la mitad 2 sin NA en pobre, urbano y comprador
     neto (`subset`); se reporta cuántos se pierden.
  5. `rank_average_treatment_effect(target = "AUTOC", R = 500)` con
     `set.seed(2026)` antes de cada llamada: una por prioridad sola (bosque
     = −τ̂, 1{pobre}, 1{urbano}, 1{comprador neto}; curvas TOC) y una por cada
     par bosque − regla (diferencia con bootstrap emparejado y agrupado).
     Holm (F3, m = 3) sobre los tres p de las diferencias (bilateral, normal).
  6. Robustez secundaria: los papeles invertidos (bosque en la mitad 2,
     evaluación en la 1); se reporta aparte y el promedio de las estimaciones
     puntuales, sin EE. Lo principal es la versión pre-registrada.
- **Signo (escala de daño).** grf mide si los priorizados tienen τ mayor que el
  promedio. Con Y = −ΔHAZ el τ del bosque de evaluación es daño (positivo =
  menos talla), así que AUTOC > 0 = la regla encuentra a los más dañados. La
  prioridad del bosque es −τ̂ con τ̂ del bosque A entrenado con ΔHAZ (= daño
  predicho). **Chequeo numérico:** un bosque de evaluación con Y = +ΔHAZ debe
  dar AUTOC del bosque igual al de escala de daño con el signo cambiado; se
  imprime y se exige con `stopifnot` (tolerancia pequeña).
- **Riesgos.** Unas 100 comunidades por mitad: se espera un nulo. Si `W.hat`
  de la mitad de evaluación queda fuera de [0,05; 0,95], grf avisa; se
  documenta con [REVISIÓN HUMANA] y se sigue.
- **Salidas.** `03_Resultados/Tablas/14_rate/ninos_rate.{png,csv}` y
  `03_Resultados/Figuras/14_rate/ninos_rate_toc.png`.

**Parte A hecha:** AUTOC del bosque 0,116 (EE 0,116; p 0,313); diferencias
bosque − regla entre 0,070 y 0,208, ninguna pasa Holm (menor p Holm 0,492).
834 niños en 98 comunidades; 0 perdidos por NA. Chequeo de signo superado
(−0,116 con Y = +ΔHAZ). Propensiones de 0,136 a 0,841: sin avisos de grf.
Nota en `05_Notas/14_rate/H_rate_reglas.md`.

### Parte B. `04_Presentaciones/hallazgos_principales.txt`

- **Qué hará.** Texto plano en ocho secciones (las del pedido), con cada cifra
  seguida de la ruta del `.csv`/`.png` de `03_Resultados/` o de la nota que la
  cita, y las de la literatura solo de `CLAUDE.md` §5 y las notas (ya
  cotejadas con los PDF).
- **Potencia.** Diferencia mínima detectable ≈ (1,96 + 0,84) × EE ≈ 2,8 × EE,
  calculada en R con `02_Scripts/_exploratorio/mde_potencia.R` sobre los EE de
  los `.csv` (fuera del pipeline, porque no produce tablas para láminas;
  marcada como aproximada).
- **Calibración.** Se incorpora lo que verificó Samuel en el código de grf
  2.6.1 (`sandwich::vcovCL` con los clusters del bosque, tipo HC3; p
  unilateral). Eso resuelve el [REVISIÓN HUMANA] de la nota de P4.1, que se
  actualiza en su historial (sin cambiar la conclusión).
- **Riesgo.** Lenguaje: solo el contraste identificado; «no se distingue de
  cero»; urbano de E-Q «ni lo confirmamos ni lo descartamos».

### Parte C. `04_Presentaciones/estructura_presentacion.md`

- **Qué hará.** 13 láminas principales en el arco ¿dolió? → ¿a quién? → ¿el
  bosque supera a las reglas? → qué hacer, con título-conclusión, mensaje,
  ruta exacta del `.png`, cifras con `.csv`, tiempo y presentador (1-4,
  ~5 min cada uno); tabla resumen; apéndice; 10 preguntas con respuesta.
- **Verificación.** Un `ls` de cada ruta citada; las figuras que falten se
  listan, no se inventan.

**Partes B y C hechas.** Todas las rutas citadas se verificaron con `ls`
(la única que no existe, `02_Scripts/15_potencia.R`, aparece a propósito en
«Figuras que faltarían»).

## Resumen

Sesión autónoma de Samuel Escandón. Cierra **H4** (P4.2; P4.1 y P4.3 ya
estaban) y deja los insumos de la presentación. De los «Siguientes objetivos»
de `HANDOFF.md`: (2) P4.2 se cumplió; (3) los [REVISIÓN HUMANA] de H3 se
resolvieron en parte (calibración, ver abajo); (1) P6.1-P6.2 avanzó con la
estructura de la presentación, pero no hay guion ni láminas.

- **P4.2:** el bosque no prioriza mejor que pobre, urbano ni comprador neto:
  AUTOC del bosque 0,116 (EE 0,116); diferencias de 0,070 a 0,208, menor p Holm
  0,492. Coherente con la calibración nula y los GATE.
- **Insumos:** `04_Presentaciones/hallazgos_principales.txt` (todo el proyecto
  en texto plano con rutas) y `04_Presentaciones/estructura_presentacion.md`
  (15 láminas, apéndice, 10 preguntas, figuras que faltarían).
- **Potencia:** MDE ≈ 2,8 × EE, calculada con
  `02_Scripts/_exploratorio/mde_potencia.R` (fuera del pipeline).

## Archivos

- Creados: `02_Scripts/14_rate.R`; `02_Scripts/_exploratorio/mde_potencia.R`;
  `03_Resultados/Tablas/14_rate/ninos_rate.{png,csv}`;
  `03_Resultados/Figuras/14_rate/ninos_rate_toc.png`;
  `05_Notas/14_rate/H_rate_reglas.md`;
  `04_Presentaciones/hallazgos_principales.txt`;
  `04_Presentaciones/estructura_presentacion.md`; esta bitácora.
- Modificados: `00_main.R`, `README.md`, `PLAN.md` (P4.2 y «Por verificar»),
  `registro_decisiones.md` (§6, RATE), `05_Notas/README.md`,
  `05_Notas/12_calibracion/H_calibracion_nulo.md` (EE de la calibración
  resuelto), `HANDOFF.md`.

## Detalle por archivo

### `02_Scripts/14_rate.R`

- **Estimando:** AUTOC de cada prioridad = área bajo la curva TOC, en escala de
  daño (efecto del tercil alto frente al bajo, con signo cambiado), y la
  diferencia bosque − regla. **Estimador:** `rank_average_treatment_effect`
  sobre los puntajes doblemente robustos de un bosque de evaluación; bootstrap
  agrupado por comunidad, emparejado en las diferencias.
- **Partición:** `set.seed(2026)`, 97 comunidades en la mitad 1 y 98 en la 2
  (de 195). Mitad de evaluación: 834 niños, 98 comunidades, 0 perdidos por NA
  en las reglas. Invertida: 766 niños, 97 comunidades, 2 perdidos.
- **Prioridad del bosque:** −τ̂ con τ̂ de un bosque entrenado con ΔHAZ en la
  otra mitad (mismas X y opciones que `10_bosque`).
- **Signo:** bosque de evaluación con Y = −ΔHAZ; chequeo con Y = +ΔHAZ: AUTOC
  del bosque −0,116 frente a +0,116 (exigido con `stopifnot`).
- **R = 500**, `set.seed(2026)` antes de cada llamada; Holm sobre las tres
  diferencias de la versión pre-registrada.
- Propensiones de la mitad de evaluación entre 0,136 y 0,841 (invertida, 0,136
  a 0,886): grf no avisó de valores extremos.

### `04_Presentaciones/hallazgos_principales.txt` y `estructura_presentacion.md`

- Cifras copiadas de los `.csv` y notas; la literatura, solo de `CLAUDE.md` §5
  y del pre-registro. Lenguaje: «no se distingue de cero», contraste y no
  efecto de la crisis, urbano de E-Q «ni lo confirmamos ni lo descartamos»,
  lo exploratorio dicho como exploratorio.
- Tiempos: 1.200 s; presentadores con 285 a 310 s.

### `05_Notas/12_calibracion/H_calibracion_nulo.md`

- El [REVISIÓN HUMANA] sobre los EE de `test_calibration` queda resuelto con lo
  que Samuel verificó en el código de grf 2.6.1 (`sandwich::vcovCL` con los
  clusters del bosque, HC3; p unilateral). La conclusión no cambia.

## Resultados nuevos

- `ninos_rate` y `ninos_rate_toc` (etapa 5 de `CLAUDE.md` §6; contraste):
  responden la pregunta 3 y sostienen la lámina del nulo.

## Pendientes

- **P6.1-P6.2:** guion (`04_Presentaciones/guion.md`) y láminas con los
  nombres de los presentadores; la lámina 11 (potencia) no tiene figura.
- **[REVISIÓN HUMANA]** (siguen abiertos de la sesión (4)): presentación del
  resultado urbano frente a E-Q (`05_Notas/09_interacciones_eq/H_interacciones_eq.md`)
  y `git pull` de la rama local `SamuelEscandonC` en el otro worktree.
- P7.1-P7.3 (entrega).

## Sesión posterior: correcciones de `presentacion_final.pptx` (pedido de Samuel)

### Plan (escrito antes de implementar)

- **Punto de partida.** El script `04_Presentaciones/_fuente/construir_presentacion.py`
  no existía en ninguna rama; la única copia de la presentación estaba en
  `04_Presentaciones/presentacion_final.pptx` del checkout principal (sin
  versionar). Se copia como `04_Presentaciones/_fuente/presentacion_base.pptx`
  y se escribe el script, que la toma como base, aplica las correcciones con
  `python-pptx` y deja `08_Entregables/presentacion_final.{pptx,pdf}`, más un
  PNG por lámina y una revisión automática de textos montados o fuera de la
  página (con PyMuPDF sobre el PDF).
- **Cambios** (los del pedido): lámina 3 (pie, notas del Presentador 1, bigotes
  de ±1,96 EE calculados desde `06_ate/ninos_ate_especificaciones.csv`),
  lámina 1 (portada sin solapes y crédito de TIME), lámina 5 (tabla, fuente y
  título), lámina 10 (cuadrícula 2 × 3), lámina 9 (cuadros a la misma altura),
  consistencia (rectángulos en lugar de ondas en 2, 6 y 8; títulos a la
  izquierda; cuadro verde del pie), lámina 7 (figura de GATE más grande, sin
  deformar). Además, lo que la revisión muestre montado (p. ej., la tabla y el
  texto del panel de la lámina 4, los títulos que invaden la figura en 2 y 6).
- **Decisiones.** Ninguna cifra cambia; el número de láminas sigue en 10. Las
  figuras se insertan sin recortar ni deformar (CLAUDE.md §4.1). La escala de
  las barras de la lámina 3 se recalcula para que quepan los bigotes.
- **Riesgos.** (1) La fuente «Radio Canada» no está instalada ni incrustada:
  LibreOffice la sustituye al exportar el PDF, y PowerPoint en otro equipo
  también lo hará. Se dimensiona con márgenes. (2) La portada de TIME tiene
  derechos de autor y el repositorio es público: el `.pptx`, el `.pdf` y la base
  no se versionan (`.gitignore`); solo el script. **[REVISIÓN HUMANA]**

### Resultado

- `04_Presentaciones/_fuente/construir_presentacion.py` deja
  `08_Entregables/presentacion_final.{pptx,pdf}` (10 láminas, sin cambiar
  cifras) y un PNG por lámina en `04_Presentaciones/_fuente/_render/`. La
  revisión automática del PDF (textos montados, sobre imágenes o fuera de la
  página) da 0 problemas, y se revisaron a ojo las 10 láminas.
- Cambios: lámina 1 (encabezado en una línea, título a la izquierda, pregunta
  con mayúscula, portada de TIME más chica sin tapar texto, crédito «Portada:
  TIME, 19 de enero de 1998» a 10 pt, nombres completos dentro del panel);
  lámina 3 (sin «Opción B», bigotes de ±1,96 EE calculados desde el `.csv`
  de 06_ate, escala de las barras recalculada, EE «agrupado» y «robusto sin
  agrupar» en las etiquetas, notas nuevas del Presentador 1 de ~100 s);
  lámina 5 (título nuevo, tabla más ancha con «−0,270 (0,153)» en una línea,
  fuente debajo de la tabla); lámina 7 (panel de 3,15 M EMU, figura de GATE a
  toda la altura disponible, sin deformar; pie visible); lámina 9 (tres
  cuadros a la misma altura); lámina 10 (cuadrícula 2 × 3); láminas 2, 6 y 8
  (rectángulos con el texto dentro en lugar de ondas); láminas 2, 4, 6 y 8
  (títulos de 24 pt para que no invadan la figura; tabla y textos del panel
  de la lámina 4 sin montarse); todos los títulos a la izquierda; cuadro
  verde del pie en las láminas 2-10.
- **La fecha de la portada** se leyó en la propia imagen («JANUARY 19, 1998»,
  baja resolución). **[REVISIÓN HUMANA]**: confirmarla.
- **Fuente:** «Radio Canada» no está instalada ni incrustada; el PDF usa la
  sustitución de LibreOffice. Recomendación: presentar desde el PDF.
- No se versionan la base, el `.pptx`, el `.pdf` ni los PNG (`.gitignore`):
  la portada de TIME tiene derechos de terceros y el repositorio es público.
  **[REVISIÓN HUMANA]**: para la entrega, subir la presentación a Bloque Neón
  directamente.
