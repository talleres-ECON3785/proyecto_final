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
[`registro_decisiones.md`](registro_decisiones.md). P2.1 (ATE) quedó el 22-nov.

1. **P2.2: forma con cuartiles** (Q2-Q4 frente a Q1), con `feols`, las mismas
   especificaciones y errores de `06_ate.R`.
   - *Terminado cuando:* la figura de los coeficientes, con la recta de E-Q
     encima, está exportada en `03_Resultados/Figuras/<script>/` y tiene nota.
2. **P2.3: validación.**
   - Placebo 1993→1997 (decidir antes si se asigna por `commid93` o `commid97`),
     desgaste según el alza, sin las comunidades de 1998, con pesos, sin
     winsorizar, con la dosis solo en kg y sin |ΔHAZ| > 3.
   - *Terminado cuando:* la tabla de robustez está exportada y tiene nota. Usar
     la robustez sin winsorizar y solo en kg para probar si la diferencia con
     E-Q viene de la medida del precio.
3. **P3.1: réplica de las cinco interacciones de E-Q** con `feols` y la dosis,
   una a la vez, con errores robustos y agrupados; p sin ajustar y Holm (F2).
   - *Terminado cuando:* la tabla está exportada y tiene nota.

**Bloqueos / preguntas abiertas:**

- **Contar al equipo el resultado de P2.1:** β entre −0,22 y −0,34 HAZ por
  +100 %, 1,6 a 2,5 veces el −0,135 de E-Q (intervalos que se traslapan), y el
  salto de −0,24 a −0,34 al agregar efectos fijos de provincia. Ver
  `05_Notas/06_ate/A_ate_promedio.md`.
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
- **Pipeline:** `00_main.R` corre de principio a fin seis scripts:
  `01_tracks`, `02_precio_arroz`, `03_x_1997`, `04_haz`, `05_base` y `06_ate`. Las
  ampliaciones `anthro` y `anthroplus` están registradas.
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
  especificaciones con `feols` y la pendiente del bosque.
- **Notas** (`05_Notas/`): cohortes y desgaste, distribución del precio,
  desgaste según el alza (con la revisión de P1.6) y el efecto promedio (P2.1).
- **Decisiones:** `registro_decisiones.md`, al día con lo de H1. Pre-registro en
  `10_Propuesta/07_preregistro_heterogeneidad.md`.

## Registro de sesiones

<!-- La más reciente primero. Tres a cinco líneas por entrada; las anteriores
     no se editan. -->

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
