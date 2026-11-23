# HANDOFF

Resumen accionable del proyecto final para retomar el trabajo. El detalle de cada
sesión está en `06_Bitacoras/`; aquí solo va lo necesario para saber dónde
estamos y qué sigue. Las reglas para mantener este archivo están en `CLAUDE.md`
(§7).

**Asesoría: semana 15 (por agendar). Presentación y entrega: semana 16,
miércoles 11:59 pm (fechas exactas por confirmar).**

## Siguientes objetivos

<!-- Dos a tres tareas concretas, en orden de prioridad, cada una con el
     archivo que debe producirse, un criterio de terminado verificable y, si
     aplica, el integrante a cargo. Se derivan de las primeras casillas sin
     marcar de PLAN.md. Se reescribe al cerrar cada sesión. -->

Objetivos derivados de [`PLAN.md`](PLAN.md). Lo confirmado está en
[`registro_decisiones.md`](registro_decisiones.md). **H2, H3 y H4 están
completos** (22-nov). Insumos de la presentación:
`04_Presentaciones/hallazgos_principales.txt` (todo el proyecto, con rutas) y
`04_Presentaciones/estructura_presentacion.md` (15 láminas, apéndice y
preguntas).

1. **P6.1-P6.2: guion y láminas** a partir de `estructura_presentacion.md`:
   poner los nombres de los presentadores 1-4 y armar las láminas con los
   `.png` exportados.
   - *Terminado cuando:* `04_Presentaciones/guion.md` y las láminas existen y
     cada lámina usa la ruta indicada.
2. **Decidir lo marcado [REVISIÓN HUMANA]** (urbano frente a E-Q) y, si se
   quiere, producir la figura de la lámina 11 (potencia).
3. **P7.1-P7.3: entrega** (`00_main.R` desde cero ya corre con 14 scripts;
   falta README final y `.zip`).

**Bloqueos / preguntas abiertas:**

- **Contar al equipo el resultado de H4:** el bosque no prioriza mejor que
  pobre, urbano ni comprador neto (AUTOC del bosque 0,116, EE 0,116; menor p
  Holm de las diferencias 0,492). Con la calibración nula y los GATE, la
  pregunta 3 es un nulo.
- **Contar al equipo el resultado de H3** (`05_Notas/09_*` a `13_*`): ninguna
  de las cinco interacciones de E-Q ni de los seis GATE pasa Holm (menores p
  Holm 1,000 y 0,764); la calibración del bosque no rechaza (p 0,438). El
  resultado urbano de E-Q (−0,270) no se replica (−0,009, EE 0,223).
- **Rama de Samuel:** la sesión del 22-nov (4) trabajó en un worktree y empujó
  a `origin/SamuelEscandonC`; la rama local `SamuelEscandonC` (otro worktree)
  necesita `git pull`.
- **Contar al equipo el resultado de H2** antes de armar la lámina de la
  pregunta 1 (`05_Notas/06_ate/`, `07_cuartiles/` y `08_validacion/`):
  - el efecto es negativo en todas las variantes, pero su tamaño va de −0,20 a
    −0,50 HAZ por +100 % (principal −0,329, 1,6 a 2,5 veces el −0,135 de E-Q);
  - el placebo 1993-1997 no es significativo, pero con controles es −0,19
    (p = 0,10), cerca del 60 % del efecto: **inconcluso**, no se puede descartar
    una tendencia previa;
  - sin los 110 niños con |ΔHAZ| > 3 el efecto baja a −0,197 (p = 0,064); se
    mantienen en lo principal por la decisión previa de P1.6.
  Mensaje propuesto: la dirección es robusta, el tamaño no.
- **Acceso de Mateo al repositorio:** la cuenta `Mateo10o` no tiene permiso de
  escritura; los commits de H2 están en su rama local `MateoOlmosB` hasta que
  se le dé acceso (o se suban por un fork).
- **Contar al equipo** las decisiones del 20-nov (4): litros a kg, 38
  comunidades de 1998, terciles dentro de provincia, línea de Widyanti et al.
  (2009) y la base fuera de GitHub (cada uno la regenera con `00_main.R`).
- **Muestra frente a E-Q:** nuestros 2.421 niños frente a los 2.112 de su cuadro
  1, cuyos filtros no se conocen.
- **Por verificar antes de usar:** cómo trata `grf` los empates en el RATE;
  que la «edad crítica» de E-Q sea 0-2 años.
- Fechas exactas de las semanas 15 y 16.

## Estado actual

- **Repositorio:** `talleres-ECON3785/proyecto_final` (público). Santiago
  trabaja en `SantiagoMunozM` y Mateo en `MateoOlmosB`.
- **Datos:** las cinco olas de la IFLS en local (`01_Datos/01_Crudos/`, sin
  versionar). Reglas en `01_Datos/CLAUDE.md`.
- **Pipeline:** `00_main.R` corre de principio a fin ocho scripts:
  `01_tracks`, `02_precio_arroz`, `03_x_1997`, `04_haz`, `05_base`, `06_ate`,
  `07_cuartiles` y `08_validacion`, y desde el 22-nov (4) `09_interacciones_eq`,
  `10_bosque`, `11_gate`, `12_calibracion`, `13_perfil` y `14_rate` (14 scripts). Las ampliaciones `anthro` y `anthroplus` están registradas.
- **Bases** (locales, ignoradas por git):
  - `02_Procesados/`: `tracks`, `precio_arroz` (297 comunidades), `x_1997` y
    `haz`;
  - `03_Listos/base_estimacion.rds`: **2.421 niños en 294 comunidades**, un niño
    por fila, con ΔHAZ, dosis, cuartiles, terciles y X de 1997;
  - no se comparten por GitHub: se regeneran con `00_main.R`.
- **Resultados** (`03_Resultados/`): desgaste por ola, distribución del alza y
  resumen del precio, resumen del HAZ, desgaste según el alza y la revisión de
  P1.6 (motivos del HAZ faltante en 1997, balance y cola del ΔHAZ), todos
  descriptivos. **ATE (P2.1):** `06_ate/ninos_ate_especificaciones`, cuatro
  especificaciones con `feols` y la pendiente del bosque. **Forma (P2.2):**
  tabla y figura de `07_cuartiles`. **Validación (P2.3):** placebo y robustez
  de `08_validacion`. **H3:** interacciones de E-Q (`09`), bosque con
  terciles y traslape (`10`), GATE y BLP (`11`); **P4.1/P4.3:** calibración
  (`12`) y perfil por cuartil de τ̂ (`13`); **P4.2:** RATE con AUTOC (`14`).
- **Notas** (`05_Notas/`): cohortes y desgaste, distribución del precio,
  desgaste según el alza (con la revisión de P1.6), el efecto promedio (P2.1,
  matizado), la forma por cuartiles (P2.2), la validación (P2.3), y de H3 en
  adelante: interacciones de E-Q, bosque, GATE, calibración (nulo) y perfil.
- **Decisiones:** `registro_decisiones.md`, al día con lo de H1. Pre-registro en
  `10_Propuesta/07_preregistro_heterogeneidad.md`.

## Registro de sesiones

<!-- La más reciente primero. Tres a cinco líneas por entrada; las anteriores
     no se editan. -->

### 2026-11-22 (6): correcciones de la presentación final

- Samuel Escandón (worktree, empujado a `SamuelEscandonC`), sesión autónoma.
  - `04_Presentaciones/_fuente/construir_presentacion.py` corrige la
    presentación (10 láminas, mismas cifras) y deja
    `08_Entregables/presentacion_final.{pptx,pdf}`; la revisión del PDF no
    encuentra textos montados ni cortados. Bigotes de ±1,96 EE en la lámina 3.
  - La base, el `.pptx` y el `.pdf` no se versionan (portada de TIME).
- Bitácora: [2026-11-22_rate-y-presentacion_5.md](06_Bitacoras/2026-11-22_rate-y-presentacion_5.md)
- **Siguientes objetivos:** (1) ensayar con el PDF; (2) confirmar la fecha de
  la portada; (3) P7: entrega.

### 2026-11-22 (5): RATE (P4.2) e insumos de la presentación

- Samuel Escandón (worktree, empujado a `SamuelEscandonC`), sesión autónoma.
  - `14_rate.R`: AUTOC en escala de daño, 834 niños en 98 comunidades; bosque
    0,116 (EE 0,116); diferencias bosque − regla de 0,070 a 0,208, ninguna pasa
    Holm (F3). **Cierra P4.2 y H4.**
  - `hallazgos_principales.txt` y `estructura_presentacion.md` (15 láminas,
    apéndice, 10 preguntas). `00_main.R` corre desde cero con 14 scripts.
- Bitácora: [2026-11-22_rate-y-presentacion_5.md](06_Bitacoras/2026-11-22_rate-y-presentacion_5.md)
- **Siguientes objetivos:** (1) P6.1-P6.2: guion y láminas; (2) decidir lo
  marcado [REVISIÓN HUMANA]; (3) P7: entrega.

### 2026-11-22 (4): ¿a quién? (H3), calibración y perfil

- Samuel Escandón (worktree, empujado a `SamuelEscandonC`), sesión autónoma.
  - P3.1: ninguna de las cinco interacciones de E-Q pasa Holm (β2 de −0,096 a
    0,127, EE 0,18-0,26). P3.2: bosque con terciles, ATE −0,184 (EE 0,065),
    1.602 niños en 195 comunidades, traslape dentro de la regla. P3.3: ningún
    GATE pasa Holm (edad, el más alejado: 0-2 años −0,313 frente a 3-5 −0,083).
  - P4.1: la calibración no rechaza (diferencial 0,124, p 0,438). P4.3: el
    bosque ordena sobre todo por edad. **Cierra H3, P4.1 y P4.3.**
- Bitácora: [2026-11-22_heterogeneidad-h3_4.md](06_Bitacoras/2026-11-22_heterogeneidad-h3_4.md)
- **Siguientes objetivos:** (1) P6.1-P6.2: guion y láminas; (2) P4.2: RATE;
  (3) revisar lo marcado [REVISIÓN HUMANA].

### 2026-11-22 (3): placebo y robustez (P2.3)

- Mateo Olmos (`MateoOlmosB`).
  - `08_validacion.R`: placebo 1993-1997 entre −0,097 y −0,194 (p de 0,10 a
    0,43), inconcluso; robustez de −0,197 (sin |ΔHAZ| > 3) a −0,504 (con pesos
    de la evaluación de salud de 2000). La dirección se sostiene, el tamaño no.
    **Cierra P2.3 y H2.**
  - Pesos de la robustez: del longitudinal (932 niños) al de la evaluación de
    salud de 2000 (2.421), registrado en §5. La nota de P2.1 pasa a matizada.
- Bitácora: [2026-11-22_validacion-p2-3_3.md](06_Bitacoras/2026-11-22_validacion-p2-3_3.md)
- **Siguientes objetivos:** (1) P3.1: interacciones de E-Q; (2) P3.2: bosque
  principal; (3) P3.3: GATE.

### 2026-11-22 (2): forma del efecto por cuartiles (P2.2)

- Mateo Olmos (`MateoOlmosB`).
  - `07_cuartiles.R`: frente al cuartil 1 (+42 %), especificación 4: cuartil 2
    −0,189 (EE 0,093), cuartil 3 −0,116 (0,094), cuartil 4 −0,295 (0,104). Los
    puntos quedan dentro de su incertidumbre alrededor de la recta de P2.1.
    **Cierra P2.2.**
  - El proyecto local se movió de iCloud a `~/proyecto_final` (iCloud lleno no
    dejaba guardar).
- Bitácora: [2026-11-22_forma-cuartiles-p2-2_2.md](06_Bitacoras/2026-11-22_forma-cuartiles-p2-2_2.md)
- **Siguientes objetivos:** (1) P2.3: validación; (2) P3.1: réplica de las
  interacciones de E-Q; (3) P3.2: bosque principal.

### 2026-11-22: efecto promedio del alza del arroz en la talla (P2.1)

- Mateo Olmos (`MateoOlmosB`), primera sesión.
  - Clonó el repositorio, ubicó los datos y reprodujo la base: 2.421 niños en
    294 comunidades.
  - `06_ate.R`: β entre −0,217 y −0,339 HAZ por +100 % (EE agrupado 0,109 a
    0,139), −1,1 a −1,7 cm aproximados; pendiente del bosque −0,260 (0,132).
    Mayor que el −0,135 de E-Q, con intervalos que se traslapan. **Cierra
    P2.1.**
- Bitácora: [2026-11-22_ate-promedio-p2-1.md](06_Bitacoras/2026-11-22_ate-promedio-p2-1.md)
- **Siguientes objetivos:** (1) P2.2: forma con cuartiles; (2) P2.3:
  validación; (3) P3.1: réplica de las interacciones de E-Q.

### 2026-11-20 (5): revisión de la base antes de H2 (P1.6)

- Santiago Muñoz (`SantiagoMunozM`).
  - Hay menos HAZ de 1997 en el cuartil de mayor alza porque faltan
    evaluaciones de salud, y la brecha es sobre todo entre provincias: con
    efectos fijos de provincia, la pendiente pasa de −0,090 a −0,045 (EE 0,033).
  - La composición de los medidos no cambia con el alza.
  - La cola del ΔHAZ (110 niños) se mantiene, con robustez sin |ΔHAZ| > 3 en
    P2.3, decidido antes de ver el ATE. **Cierra P1.6.**
- Bitácora: [2026-11-20_revision-base-p1-6_5.md](06_Bitacoras/2026-11-20_revision-base-p1-6_5.md)
- **Siguientes objetivos:** (1) P2.1: ATE con `feols`; (2) P2.2: forma con
  cuartiles; (3) P2.3: validación (placebo y robustez).

### 2026-11-20 (4): las bases del hito H1

- Santiago Muñoz (`SantiagoMunozM`).
  - Se escribieron y corrieron `01_tracks`, `02_precio_arroz`, `03_x_1997`,
    `04_haz` y `05_base`. **Cierra H1 (P1.1-P1.5).**
  - La base lista tiene 2.421 niños en 294 comunidades.
  - Decisiones: litros a kg, 38 comunidades de 1998, terciles dentro de
    provincia, línea de Widyanti et al. (2009) verificada en el PDF y la base
    fuera de GitHub (repositorio público).
  - El seguimiento 1997-2000 no depende del alza, pero la cobertura del HAZ de
    1997 sí (P1.6).
- Bitácora: [2026-11-20_bases-h1_4.md](06_Bitacoras/2026-11-20_bases-h1_4.md)
- **Siguientes objetivos:** (1) P1.6: revisar la base (HAZ de 1997 faltante y
  cola del ΔHAZ); (2) P2.1: ATE con `feols`; (3) P2.2: forma con cuartiles.

### 2026-11-20 (3): registro de decisiones, pre-registro y plan nuevo

- Santiago Muñoz (`SantiagoMunozM`).
  - Se revisó volver a incluir 2014 y el logro educativo (escolaridad y pruebas
    EK de 2000) con conteos exploratorios. Santiago lo descartó: la prueba de
    2000 no es comparable con la de 1997. Se mantiene solo estatura.
  - Pre-registro de las cinco interacciones de E-Q, seis GATE, Holm (F1-F3) y
    AUTOC. R para todo. T1 descartada.
  - Nuevo `registro_decisiones.md` (solo lo confirmado, manda), `PLAN.md`
    rehecho desde cero y `10_Propuesta/` histórica. Ninguna estimación.
- Bitácora: [2026-11-20_registro-decisiones-y-plan_3.md](06_Bitacoras/2026-11-20_registro-decisiones-y-plan_3.md)
- **Siguientes objetivos:** (1) P0.1-P0.3: equipo en el repositorio y
  conocimiento del registro; (2) P1.1: `01_tracks.R`; (3) P1.2:
  `02_precio_arroz.R` con la decisión de los terciles.

### 2026-11-20 (2): el precio de 2000 y el suplemento de E-Q

- Santiago Muñoz (`SantiagoMunozM`).
  - Se diagnosticó el problema del precio de 2000: el libro PKK no trae precios,
    así que promediar todas las fuentes de cada año mezcla el alza con el
    cambio de fuentes.
  - Se leyó completo el suplemento de E-Q (cierra PL.2). No dice qué fuente usan
    en 2000, y sus errores son robustos sin agrupar por comunidad.
  - Santiago decidió el precio principal: fuentes comunes (posyandu +
    `bk2_hpj`) y cambio proporcional nominal; T1 queda como réplica aproximada.
  - Se corrigió `CLAUDE.md` §5.6 con el cuadro A4. Ninguna estimación.
- Bitácora: [2026-11-20_precio-2000-y-suplemento-eq_2.md](06_Bitacoras/2026-11-20_precio-2000-y-suplemento-eq_2.md)
- **Siguientes objetivos:** (1) P0.3 y P1.1, P1.3-P1.5: equipo en el
  repositorio y confirmación de las decisiones, incluido el precio; (2) P2.1:
  `01_tracks.R`; (3) P2.2: `02_precio_arroz.R` con T1-T4, la prueba 1 y el
  diagnóstico PKK frente a posyandu.

### 2026-11-20: identificación del tratamiento y alcance

- Santiago Muñoz (`SantiagoMunozM`).
  - Se revisó contra el PDF cómo asignan E-Q el tratamiento: dosis continua y
    cambio proporcional, sin grupo de control.
  - Se discutieron las alternativas (continuo, terciles, otros cortes,
    cuartiles) y se verificaron en `grf` 2.6.1 el bosque continuo, RATE y
    `lm_forest`.
  - El equipo dejó solo estatura. La propuesta se evaluó con un consejo de cinco
    asesores, y la recomendación quedó en `PLAN.md`, `CLAUDE.md` y el resumen
    v5: réplica y no linealidad con `feols`, el bosque para los GATE y RATE.
  - Cierra P1.2. Ninguna estimación.
- Bitácora: [2026-11-20_identificacion-tratamiento-y-alcance.md](06_Bitacoras/2026-11-20_identificacion-tratamiento-y-alcance.md)
- **Siguientes objetivos:** (1) P0.3 y P1.1, P1.3-P1.5: equipo en el
  repositorio y confirmación de las decisiones; (2) P2.1: `01_tracks.R`; (3)
  P2.2: `02_precio_arroz.R` con T1-T4 y la prueba 1.

### 2026-11-18: configuración del repositorio

- Santiago Muñoz (`main`, commit inicial). Se reorganizó la carpeta del proyecto
  con la estructura de los talleres, se escribieron `CLAUDE.md`,
  `01_Datos/CLAUDE.md`, `HANDOFF.md`, `PLAN.md`, README, `.gitignore` (datos
  fuera) y `00_main.R`, y se adaptaron las skills `bitacora-sesion`,
  `cerrar-sesion` y `registrar-hallazgo`. Cierra P0.1 y P0.2.
- Bitácora: [2026-11-18_configuracion-repositorio.md](06_Bitacoras/2026-11-18_configuracion-repositorio.md)
- **Siguientes objetivos:** (1) P0.3 y P1.1-P1.6: equipo en el repositorio y
  decisiones previas; (2) P2.1: `01_tracks.R`; (3) P2.2: `02_precio_arroz.R`.

### 2026-11-10 a 2026-11-17: propuesta y revisión de datos (antes del repositorio)

- Sesiones previas, fuera de git: propuesta v2 → v4, revisión de las cinco olas
  de la IFLS y cotejo de los cinco artículos centrales con los PDF. La nota de
  traspaso del 13-nov está en
  [2026-11-13_handoff-revision-datos-ronda5.md](06_Bitacoras/2026-11-13_handoff-revision-datos-ronda5.md);
  el `CLAUDE.md` de esa etapa, en `10_Propuesta/_obsoleto/CLAUDE_2026-11-17.md`.
