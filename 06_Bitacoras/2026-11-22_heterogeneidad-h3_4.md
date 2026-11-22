# Bitácora — 2026-11-22 (4): pregunta 2, ¿a quién? (H3) y calibración (P4.1, P4.3)

Samuel Escandón, sesión autónoma (el integrante pidió correr todo de corrido,
sin confirmaciones; los planes de cada tarea se escriben aquí antes de
implementarla).

## Planes por tarea (escritos antes de implementar)

### Preparación

- Rama: la rama `SamuelEscandonC` está abierta en otro worktree
  (`.claude/worktrees/ifls-raw-data-setup-8aa5ba`), así que git no deja
  cambiarse a ella aquí. Las dos ramas están en el mismo commit que
  `origin/main` (`c39dd34`). Se trabaja en el worktree
  `claude/hito-3-estimaciones-4919ca` y al cerrar se empuja a
  `origin/SamuelEscandonC` (`git push origin HEAD:SamuelEscandonC`).
  **[REVISIÓN HUMANA]**: la rama local `SamuelEscandonC` del otro worktree queda
  atrás del remoto; hay que hacer `git pull` en ella.
- Datos enlazados con `enlazar_datos_ifls.ps1` (17 uniones, sin problemas).

### P3.1: réplica de las cinco interacciones de E-Q (`09_interacciones_eq.R`)

- **Qué hará.** Para cada E1-E5 (pre-registro §1), una regresión
  `dhaz ~ dosis + dosis:X + X + controles + log_p97 | provincia`, es decir, la
  especificación (4) de `06_ate.R` con la interacción. β1 = efecto en X = 0,
  β2 = diferencia, β1 + β2 = efecto en X = 1 (con su EE por la combinación
  lineal de la matriz de varianzas). EE agrupados por `commid97` y robustos
  (HC1) lado a lado; p sin ajustar de ambos y Holm (m = 5) sobre los p de β2
  agrupados.
- **Variables X = 1:** E1 0-2 años en 1997 (`edad_meses97 < 36`; inferencia
  nuestra a partir de la fig. 5 de E-Q), E2 mujer, E3 madre con más que
  primaria (`madre_mas_primaria`), E4 pobre (línea de Widyanti), E5 urbano
  (`urbano97`).
- **Decisiones.** (a) Especificación (4) de 06_ate (la más completa) como
  principal, porque así lo pide la tarea («la especificación y los controles de
  06_ate»). E-Q no usan EF de provincia; por eso se agrega, como columna de
  comparación, la especificación (2) (sin EF ni log del precio) en el `.csv`,
  sin familia de Holm aparte. (b) El efecto principal de X entra solo (es
  constante en el tiempo, pero en primeras diferencias equivale a dejar que el
  ΔHAZ difiera por grupo, lo que hace E-Q con su interacción con T). Cuando X ya
  está en los controles (mujer, urbano97) no se duplica. (c) Los NA de los
  moderadores (madre, pobre) se pierden en esa regresión; se reporta el n de
  cada una.
- **Riesgos.** El moderador de edad está en los controles como edad continua;
  se mantiene. Los n difieren por interacción (NA del moderador).
- **Archivos.** `02_Scripts/09_interacciones_eq.R`, tabla en
  `03_Resultados/Tablas/09_interacciones_eq/`, nota en
  `05_Notas/09_interacciones_eq/`, `00_main.R`, README, PLAN.

**P3.1 hecho** (ver Resumen): ninguna β2 pasa Holm. Nota en
`05_Notas/09_interacciones_eq/H_interacciones_eq.md`.

### P3.2: bosque principal con terciles (`10_bosque.R`)

- **Qué hará.** Muestra: niños de la base en comunidades del tercil alto o bajo
  del alza dentro de provincia (`tercil_prov` 3 = 1, 1 = 0; sin el medio).
  `causal_forest(X, ΔHAZ, W, clusters = commid97, seed = 2026,
  num.threads = 1, num.trees = 4000)`. Guarda el bosque y la matriz X en
  `01_Datos/03_Listos/` (local, ignorado por git) para P3.3 y P4.
- **X (solo de 1997):** los controles de `06_ate` (cuadro A1 de E-Q sin
  programas; edad en meses, sin el cubo porque el bosque no lo necesita),
  log del precio de 1997, indicadores de provincia y los moderadores que no
  están en los controles: madre con más que primaria, pobre y comprador neto
  (con sus NA; `grf` los maneja). El HAZ de 1997 **no** entra.
- **Salidas.** Figura del traslape (`W.hat` por grupo) y tabla con el ATE del
  bosque (AIPW, agrupado) y, como referencia, MCO con el mismo tratamiento
  binario y la especificación (4). Escala: HAZ, tercil alto frente a bajo (no
  por +100 %).
- **Regla de traslape:** si más del 5 % de los niños tiene `W.hat` fuera de
  [0,05; 0,95], se mantiene el bosque principal y se agrega un bosque de
  robustez sin esos niños, con [REVISIÓN HUMANA]. No se usa
  `target.sample = "overlap"`.
- **Riesgos.** Provincias con una sola comunidad quedan enteras en un tercil
  (ntile dentro de provincia): su `W.hat` se pega a 0 o 1. Se reporta.

**P3.2 hecho:** ATE del bosque −0,184 (EE 0,065), 1.602 niños en 195
comunidades; `W.hat` entre 0,101 y 0,933, nadie fuera de [0,05; 0,95] (no hizo
falta la robustez). Nota en `05_Notas/10_bosque/H_bosque_ate_traslape.md`.

### P3.3: seis GATE con puntajes AIPW (`11_gate.R`)

- **Qué hará.** Carga el bosque de `10_bosque`. Γ = `get_scores(bosque)`. Para
  G1-G6: GATE de cada grupo con `average_treatment_effect(bosque, subset = …)`
  y Δ = GATE(X = 1) − GATE(X = 0) con `feols(Γ ~ X, cluster = ~commid97)`.
  Holm sobre los seis p de Δ (F1, m = 6). BLP conjunta con
  `best_linear_projection(bosque, A)` con las seis variables, solo
  descriptiva (sin p para conclusiones).
- **Grupos (X = 1):** G1 3-5 años (`edad_meses97` ≥ 36, al revés que E1);
  G2 urbano; G3 madre con más que primaria; G4 mujer; G5 comprador neto;
  G6 pobre. Los NA de G3, G5 y G6 se excluyen de esa comparación.
- **Salidas.** Tabla de GATE con qué grupo es X = 1 y figura de los GATE por
  grupo con IC 95 %; tabla de la BLP.
- **Riesgos.** El EE del GATE de `average_treatment_effect(subset)` y el de
  `feols` pueden diferir un poco (son estimadores de varianza distintos); se
  reportan los dos tal cual.

**P3.3 hecho:** ningún Δ pasa Holm (menor p Holm 0,764, edad). Nota en
`05_Notas/11_gate/H_gate_preregistrados.md`. H3 completo sin bloqueos graves;
se sigue con P4.1 y P4.3 (P4.2 no, por instrucción del integrante).

### P4.1: calibración del bosque (`12_calibracion.R`)

- **Qué hará.** `test_calibration(bosque)` del bosque de `10_bosque`: coeficiente
  de la predicción media (≈ 1 si el ATE está bien) y de la predicción
  diferencial (> 0 y significativo si el bosque capta heterogeneidad real). grf
  reporta un p unilateral para la diferencial; se reporta tal cual. Fuera de las
  familias de Holm (pre-registro §3).
- **Lectura pre-fijada:** si la diferencial no rechaza al 5 %, la nota dice «no
  hay evidencia de heterogeneidad más allá de los GATE pre-declarados».
- **Salidas.** `03_Resultados/Tablas/12_calibracion/ninos_calibracion.{png,csv}`.

### P4.3: perfil de los niños por cuartil de τ̂ (`13_perfil.R`)

- **Qué hará.** τ̂ fuera de la bolsa del bosque (`predict(bosque)`), cuartiles
  entre niños (Q1 = τ̂ más negativo = más daño predicho). Tabla de medias de las
  X de 1997 por cuartil: los seis moderadores, edad en meses, tamaño del hogar,
  gasto per cápita, productor de arroz, con n de niños y de comunidades y el τ̂
  medio. Descriptiva: es a quién **prioriza** el bosque, no a quién daña más.
- **Riesgo.** Si la calibración no rechaza, el perfil describe un orden que puede
  ser ruido; la nota lo dice.
- **Salidas.** `03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.{png,csv}`.

**P4.1 y P4.3 hechos:** la calibración no rechaza (diferencial 0,124, EE
0,799, p unilateral 0,438); el bosque ordena sobre todo por edad. Notas en
`05_Notas/12_calibracion/` y `05_Notas/13_perfil/`. P4.2 no se hizo.

## Resumen

Sesión autónoma de Samuel Escandón para el hito H3 (pregunta 2: ¿a quién?).
De los «Siguientes objetivos» de `HANDOFF.md` se cumplieron los tres: **P3.1**
(réplica de las interacciones de E-Q), **P3.2** (bosque con terciles) y
**P3.3** (seis GATE). Además se hicieron **P4.1** (calibración) y **P4.3**
(perfil por cuartil de τ̂). **P4.2** (RATE) no se trabajó, por instrucción.

Resultado de conjunto: el alza del arroz se asocia con menos talla en todos los
grupos, pero ninguna diferencia entre grupos pasa Holm (F2: ninguna de las cinco
interacciones; F1: ninguno de los seis GATE) y la calibración del bosque no
encuentra heterogeneidad. Es el escenario del nulo que `CLAUDE.md` §5.6
anticipaba. El pre-registro no tuvo desviaciones en esta sesión.

Antes de empezar se corrió `00_main.R` completo (8 scripts sin errores) y se
restauraron los resultados de 01-08 (`git restore 03_Resultados/`: solo
cambiaban por fin de línea y ruido numérico). Al final se corrió desde cero
(borrando `03_Resultados/`, `02_Procesados/` y `03_Listos/`).

## Archivos

- Creados: `02_Scripts/09_interacciones_eq.R`, `10_bosque.R`, `11_gate.R`,
  `12_calibracion.R`, `13_perfil.R`; tablas y figuras en
  `03_Resultados/{Tablas,Figuras}/09_interacciones_eq` a `13_perfil`; notas
  `05_Notas/09_interacciones_eq/H_interacciones_eq.md`,
  `10_bosque/H_bosque_ate_traslape.md`, `11_gate/H_gate_preregistrados.md`,
  `12_calibracion/H_calibracion_nulo.md`, `13_perfil/H_perfil_priorizados.md`;
  `04_Presentaciones/resumen_H3_para_laminas.md`; esta bitácora.
- Modificados: `00_main.R` (scripts y carpetas), `README.md` (mapa),
  `PLAN.md` (P3.1-P3.3, P4.1, P4.3), `05_Notas/README.md` (índice),
  `registro_decisiones.md` (§6), `HANDOFF.md`.
- Local, sin versionar: `01_Datos/03_Listos/bosque_terciles.rds` (bosque, X y
  datos de la muestra del bosque).

## Detalle por archivo

### `02_Scripts/09_interacciones_eq.R` (P3.1)

- **Estimando:** β2 = diferencia del efecto de +100 % del precio entre X = 1 y
  X = 0. **Estimador:** MCO con la especificación (4) de `06_ate` más dosis × X
  y X; una interacción a la vez. β1 + β2 con su EE por la combinación lineal de
  la matriz de varianzas (t con los grados de libertad de `fixest`).
- X = 1: E1 0-2 años (`edad_meses97` < 36; inferencia nuestra sobre la «edad
  crítica» de E-Q, fig. 5), E2 mujer, E3 madre con más que primaria, E4 pobre
  (Widyanti), E5 urbano. Si X ya era control (mujer, urbano) entra una sola vez.
- Pérdidas: E3, 93 niños sin dato de la madre (2.328); E4, 2 sin gasto (2.419).
- Holm (F2, m = 5) sobre los p agrupados de β2 de la especificación (4). La
  especificación (2) va en el `.csv` como comparación, sin familia.

### `02_Scripts/10_bosque.R` (P3.2)

- **Tratamiento W:** `tercil_prov` 3 = 1, 1 = 0 (registro §3); fuera el tercil
  medio (819 niños, 99 comunidades). Quedan 1.602 niños en 195 comunidades
  (731 en 93 comunidades tratadas; 871 en 102 de control). El registro dice
  197 comunidades en la comparación por terciles: son las del precio (297); en
  la base con HAZ (294) quedan 195.
- **X:** controles de `06_ate` sin el cubo de la edad, log del precio de 1997,
  indicadores de provincia, y madre con más que primaria, pobre y comprador
  neto con sus NA. Sin HAZ de 1997.
- `causal_forest(..., clusters = commid97, num.trees = 4000, seed = 2026,
  num.threads = 1)`. ATE por AIPW. Referencia: MCO de la especificación (4)
  con W.
- Traslape dentro de la regla (0 % fuera de [0,05; 0,95]); no hizo falta el
  bosque de robustez.

### `02_Scripts/11_gate.R` (P3.3)

- Γ = `get_scores(bosque)` (puntajes AIPW, ampliación registrada). GATE con
  `average_treatment_effect(subset = …)`; Δ con `feols(Γ ~ X, cluster =
  ~commid97)`; Holm (F1, m = 6). G1: X = 1 es 3-5 años (al revés que E1).
- BLP conjunta (`best_linear_projection`, ampliación registrada) en los 1.538
  niños sin faltantes en las seis variables; descriptiva.

### `02_Scripts/12_calibracion.R` (P4.1) y `13_perfil.R` (P4.3)

- `test_calibration(bosque)`; p unilateral como lo da `grf`.
- τ̂ = `predict(bosque)` (fuera de la bolsa); cuartiles entre niños; medias de
  X de 1997 por cuartil. Descriptivo.

## Resultados nuevos

Ver las notas (cifras con escala, n y comunidades) y el resumen
`04_Presentaciones/resumen_H3_para_laminas.md`. Todos son de la etapa 4-5 de
`CLAUDE.md` §6: contrastes entre comunidades con más y menos alza, salvo el
traslape y el perfil (descriptivos).

## Pendientes

- **P4.2** (RATE con AUTOC frente a pobre, urbano y comprador neto, Holm F3):
  sin hacer. Antes, verificar cómo trata `grf` los empates de una regla binaria.
- **[REVISIÓN HUMANA]** Presentación del resultado urbano frente a E-Q (nota
  de P3.1) y si `test_calibration` agrupa los EE (nota de P4.1).
- Contar al equipo que H3 dio un nulo en las dos familias de Holm y que la
  lámina del nulo es la de la pregunta 3.

## Corrida final desde cero

- La primera corrida desde cero falló en `07_cuartiles` («Chrome no generó el
  .png de ninos_cuartiles_especificaciones»): `carpetas_salida` de `00_main.R`
  no incluía `03_Resultados/Tablas/07_cuartiles` (error previo de P2.2, oculto
  porque la carpeta venía versionada). Se agregó la carpeta en `00_main.R`; el
  script 07 no se tocó. Así se cumple la regla de `CLAUDE.md` §4.1 (borrar
  `03_Resultados/` y regenerar todo).
- Antes del commit se restauraron con `git restore` los `.gitkeep` y los
  resultados de 01-08 que solo cambian por fin de línea o ruido numérico.
