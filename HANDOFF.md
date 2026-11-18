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

Objetivos derivados de [`PLAN.md`](PLAN.md).

1. **P0.3 y P1.1-P1.6: poner al equipo en el repositorio y tomar las
   decisiones previas** (todo el equipo).
   - Cada integrante clona, pone los datos de RAND en `01_Datos/01_Crudos/`
     (`01_Datos/README.md`) y crea su rama.
   - Reunión corta para cerrar cliente, resultado primario, lenguaje del
     pipeline, recomendaciones de datos de `10_Propuesta/02` §5 e hipótesis
     H1-H9.
   - *Terminado cuando:* las decisiones están en "Decisiones tomadas" de
     `CLAUDE.md` y en `01_Datos/CLAUDE.md` §9, con fecha, y las H1-H9 quedan
     fijadas por escrito.
2. **P2.1: `02_Scripts/01_tracks.R`.**
   - `htrack`/`ptrack` 1997-2014, `commid97`, cohortes y desgaste por ola, en
     `01_Datos/02_Procesados/`.
   - *Terminado cuando:* corre desde `00_main.R`, verifica la unicidad de las
     llaves con `stopifnot()` y reproduce los conteos de la síntesis (p. ej.
     3.851 niños de 0-5 años en 1997; 894 hogares sin `commid97`).
3. **P2.2: `02_Scripts/02_precio_arroz.R`** (es lo primero que pide la
   asesoría).
   - Precio por comunidad en 1997 y 2000 con las dos construcciones, Δlog y
     terciles, y la figura de su distribución.
   - *Terminado cuando:* hay una base de comunidades en `01_Datos/03_Listos/`,
     una figura en `03_Resultados/Figuras/02_precio_arroz/` y su nota en
     `05_Notas/`.

**Bloqueos / preguntas abiertas:**

- Confirmar que el equipo del proyecto es el mismo del Taller 2 (la tabla de
  ramas de `CLAUDE.md` se copió de ahí).
- Lenguaje del pipeline sin decidir (P1.4): bloquea el estilo de los scripts de
  construcción.
- Fechas exactas de las semanas 15 y 16.

## Estado actual

- **Repositorio:** `talleres-ECON3785/proyecto_final` (público), con la
  estructura de los talleres. `main` tiene el commit inicial; todavía no hay
  ramas de integrantes.
- **Datos:** las cinco olas de la IFLS (4,3 GB) están en la copia local de
  Santiago, en `01_Datos/01_Crudos/IFLS1…5/`, y no se versionan. Revisadas las
  cinco; guías descriptivas `00_guia_IFLSx.md` y síntesis
  `01_Datos/00_sintesis_revision_IFLS.md`. Reglas en `01_Datos/CLAUDE.md`.
- **Derivados:** solo `01_Datos/02_Procesados/salud_mental_1993.{csv,dta}`, de
  `02_Scripts/_exploratorio/01_salud_mental_1993.py` (uso no decidido).
- **Scripts del pipeline:** ninguno. `00_main.R` tiene paquetes, verificación de
  datos y de carpetas, y la lista `scripts` vacía. Formatos de figuras y tablas
  copiados del Taller 2 y adaptados (`02_Scripts/00_formato_*.R`).
- **Resultados y notas:** ninguno.
- **Propuesta:** v4 en `10_Propuesta/` (documento central `04`); desde el 18-nov
  sin árbol causal. PDF en `10_Propuesta/Propuesta Proyecto Final.pdf` y
  presentación en `04_Presentaciones/propuesta_presentacion.pdf`.

## Registro de sesiones

<!-- La más reciente primero. Tres a cinco líneas por entrada; las anteriores
     no se editan. -->

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
