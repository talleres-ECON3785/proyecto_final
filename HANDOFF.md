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

Objetivos derivados de [`PLAN.md`](PLAN.md). El alcance cambió el 20-nov: solo
estatura, en tres preguntas (¿dolió?, ¿a quién?, ¿el bosque supera a las reglas
simples?).

1. **P0.3 y P1.1, P1.3-P1.5: equipo en el repositorio y decisiones previas**
   (todo el equipo).
   - Cada integrante clona, pone los datos de RAND en `01_Datos/01_Crudos/` y
     crea su rama.
   - Reunión corta para confirmar:
     - el tratamiento T1-T4 y la réplica con `feols` (`PLAN.md` H1; en
       `CLAUDE.md` §11 figuran como recomendación por confirmar), y la
       construcción del precio decidida por Santiago el 20-nov (fuentes
       comunes, cambio proporcional nominal);
     - los GATE pre-declarados, con la edad primero, la familia de Holm y la
       métrica de RATE;
     - el lenguaje del pipeline;
     - las recomendaciones de datos de `10_Propuesta/02` §5.
   - *Terminado cuando:* las decisiones están en "Decisiones tomadas" de
     `CLAUDE.md` y en `01_Datos/CLAUDE.md` §9, con fecha, y los GATE quedan
     escritos.
2. **P2.1: `02_Scripts/01_tracks.R`.**
   - `htrack`/`ptrack` 1993-2000, `commid97`, cohortes (0-5 años en 1997; 0-5 en
     1993 para el placebo) y desgaste por ola, en `01_Datos/02_Procesados/`.
   - *Terminado cuando:* corre desde `00_main.R`, verifica la unicidad de las
     llaves con `stopifnot()` y reproduce los conteos de la síntesis (p. ej.
     3.851 niños de 0-5 años en 1997; 894 hogares sin `commid97`).
3. **P2.2: `02_Scripts/02_precio_arroz.R`.** Bloquea todo lo demás; dos
   integrantes en la semana 1.
   - Precio por comunidad en 1997 y 2000 con la construcción de `PLAN.md` H1:
     T2 con posyandu + `bk2_hpj`, calidad media, kg, mediana, cambio
     proporcional nominal winsorizado; T1 como réplica aproximada.
   - T1-T4, prueba 1 (variación del alza dentro y entre provincias),
     diagnóstico PKK frente a posyandu en 1997 y figura de la distribución.
   - *Terminado cuando:* hay una base de comunidades en `01_Datos/03_Listos/`,
     una figura en `03_Resultados/Figuras/02_precio_arroz/`, su nota en
     `05_Notas/` y una decisión entre terciles nacionales y dentro de provincia.

**Bloqueos / preguntas abiertas:**

- Confirmar que el equipo del proyecto es el mismo del Taller 2 (la tabla de
  ramas de `CLAUDE.md` se copió de ahí).
- Lenguaje del pipeline sin decidir (P1.4): bloquea el estilo de los scripts de
  construcción.
- La réplica de E-Q será aproximada: ni el artículo ni el suplemento dicen qué
  fuente de precio usan en 2000 (PL.3). Tampoco se sabe en qué ola miden los
  programas que usan como controles (PL.7) ni por qué el cuadro A1 tiene 3.338
  observaciones frente a los 2.112 niños del cuadro 1.
- `10_Propuesta/03` y `04` siguen en v4, con la escolaridad como resultado
  primario (P1.6).
- Fechas exactas de las semanas 15 y 16.

## Estado actual

- **Repositorio:** `talleres-ECON3785/proyecto_final` (público), con la
  estructura de los talleres. `main` tiene el commit inicial; Santiago trabaja en
  `SantiagoMunozM`.
- **Datos:** las cinco olas de la IFLS (4,3 GB) están en la copia local de
  Santiago, en `01_Datos/01_Crudos/IFLS1…5/`, y no se versionan. Las cinco están
  revisadas, con guías descriptivas `00_guia_IFLSx.md` y la síntesis
  `01_Datos/00_sintesis_revision_IFLS.md`. Reglas en `01_Datos/CLAUDE.md`.
- **Derivados:** solo `01_Datos/02_Procesados/salud_mental_1993.{csv,dta}`, de
  `02_Scripts/_exploratorio/01_salud_mental_1993.py`. Queda fuera del alcance
  actual.
- **Scripts del pipeline:** ninguno. `00_main.R` tiene paquetes, verificación de
  datos y de carpetas, y la lista `scripts` vacía. Formatos de figuras y tablas
  en `02_Scripts/00_formato_*.R`.
- **Resultados y notas:** ninguno.
- **Plan y alcance:** `PLAN.md` reorganizado el 20-nov. Solo estatura (ΔHAZ
  1997-2000, cohorte 0-5) y tratamiento en cuatro versiones: T1 réplica E-Q, T2
  dosis limpia (principal), T3 cuartiles, T4 terciles para el bosque. La
  réplica y la no linealidad van con `feols`; el bosque causal se usa para los
  GATE pre-declarados, la calibración y RATE.
- **Precio (sin construir):** construcción definida el 20-nov (`PLAN.md` H1,
  `CLAUDE.md` §11). Fuentes comunes 1997-2000 (posyandu + `bk2_hpj`) y cambio
  proporcional nominal; T1 es una réplica aproximada.
- **Suplemento de E-Q revisado** (PL.2): controles, deflactor, errores robustos
  sin agrupar por comunidad y cuadro A4, en
  `07_Recursos/Articulos/00_hallazgos_articulos.md` §1.
- **Propuesta:** resumen v5 en `10_Propuesta/00_resumen.md`; los documentos
  `01`-`06` siguen en v4 (central: `04`). PDF en
  `10_Propuesta/Propuesta Proyecto Final.pdf` y presentación en
  `04_Presentaciones/propuesta_presentacion.pdf`.
- **`grf` 2.6.1 instalado:** verificado que RATE nativo solo acepta W binario y
  que `lm_forest` solo tiene `predict`.

## Registro de sesiones

<!-- La más reciente primero. Tres a cinco líneas por entrada; las anteriores
     no se editan. -->

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
