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

Objetivos derivados de [`PLAN.md`](PLAN.md) (rehecho el 20-nov). Lo confirmado
está en [`registro_decisiones.md`](registro_decisiones.md); `10_Propuesta/` ya no
se consulta, salvo el pre-registro.

1. **P0.1-P0.3: equipo en el repositorio** (todo el equipo).
   - Cada integrante clona, pone los datos de RAND en `01_Datos/01_Crudos/`,
     crea su rama y corre la verificación de datos de `00_main.R`.
   - Santiago cuenta al equipo lo decidido el 20-nov: `registro_decisiones.md` y
     `10_Propuesta/07_preregistro_heterogeneidad.md`.
   - *Terminado cuando:* las cuatro ramas existen y las objeciones al registro,
     si las hay, quedan resueltas en el registro (con su historial).
2. **P1.1: `02_Scripts/01_tracks.R`.**
   - Seguimiento 1993-2000 desde `htrack`/`ptrack`, `commid97`, cohorte de 0-5
     años en 1997 y de 0-5 en 1993 (placebo), y desgaste por ola, en
     `01_Datos/02_Procesados/`.
   - *Terminado cuando:* corre desde `00_main.R`, verifica la unicidad de las
     llaves con `stopifnot()` y reproduce los conteos de la sesión del 20-nov
     (3.851 niños de 0-5 años en 1997; 3.369 con `commid97`).
3. **P1.2: `02_Scripts/02_precio_arroz.R`.**
   - Precio por comunidad con el registro §4. Dosis, cuartiles y terciles.
     Marcar las 27 comunidades de 1998. Figura de la distribución del alza.
   - *Terminado cuando:* hay una base de comunidades en `01_Datos/03_Listos/`,
     la figura en `03_Resultados/Figuras/02_precio_arroz/` con su nota en
     `05_Notas/`, y la decisión entre terciles nacionales y dentro de provincia
     está en el registro.

**Bloqueos / preguntas abiertas:**

- Las decisiones del 20-nov las tomó Santiago; falta que el equipo las conozca
  (P0.3).
- Confirmar que el equipo y las ramas de `CLAUDE.md` §4.2 son los correctos.
- Por verificar antes de usar: el valor de la línea de pobreza de Widyanti et
  al. (2009); las variables de `b1_ks1` para el comprador neto; cómo trata `grf`
  los empates en el RATE.
- Fechas exactas de las semanas 15 y 16.

## Estado actual

- **Repositorio:** `talleres-ECON3785/proyecto_final` (público). Santiago
  trabaja en `SantiagoMunozM`.
- **Datos:** las cinco olas de la IFLS en la copia local de Santiago
  (`01_Datos/01_Crudos/`, sin versionar), revisadas, con guías y síntesis.
  Reglas en `01_Datos/CLAUDE.md`; §9 tiene las decisiones de datos aprobadas.
- **Decisiones:** `registro_decisiones.md` (lenguaje R, tres preguntas,
  tratamiento en tres versiones: dosis, cuartiles y terciles, precio, muestra,
  controles, modificadores, Holm y AUTOC). Pre-registro de subgrupos en
  `10_Propuesta/07_preregistro_heterogeneidad.md`.
- **Plan:** `PLAN.md` rehecho el 20-nov con lo que falta (H0-H7).
- **Scripts del pipeline:** ninguno. `00_main.R` tiene paquetes, verificaciones y
  la lista `scripts` vacía. Formatos en `02_Scripts/00_formato_*.R`.
- **Derivados:** solo `salud_mental_1993` (exploratorio, fuera de alcance).
- **Resultados y notas:** ninguno. Hay un conteo exploratorio de la muestra
  potencial de estatura (2.668 niños con talla en 1997 y 2000, 307 comunidades;
  bitácora del 20-nov (3)), fuera del pipeline.
- **Propuesta (`10_Propuesta/`):** histórica.

## Registro de sesiones

<!-- La más reciente primero. Tres a cinco líneas por entrada; las anteriores
     no se editan. -->

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
