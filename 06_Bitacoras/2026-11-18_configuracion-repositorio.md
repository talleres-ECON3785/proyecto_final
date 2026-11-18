# Bitácora — 2026-11-18: configuración del repositorio

## Resumen

Objetivo: convertir la carpeta local del proyecto en el repositorio
`talleres-ECON3785/proyecto_final` (recién creado y vacío), con la estructura y
el flujo de trabajo de los Talleres 1 y 2: carpetas numeradas, `CLAUDE.md`,
`HANDOFF.md`, `PLAN.md`, `00_main.R` y las skills `bitacora-sesion`,
`cerrar-sesion` y `registrar-hallazgo`. Se pidió además un `CLAUDE.md` dedicado
a los datos y conservar las guías `.md` de cada ola.

Desarrollo:

1. Se tomaron como referencia los repositorios `taller_01` y `taller_02` en
   GitHub (la carpeta local de los talleres no estaba conectada a la sesión).
   El modelo principal es el Taller 2, que ya tenía `HANDOFF.md`, `PLAN.md`,
   notas por script y las tres skills.
2. Se reorganizó la carpeta «Proyecto Final» en el lugar, **solo con
   movimientos** (nada se borró): ver "Archivos".
3. Se escribieron los documentos de configuración y se adaptaron las skills al
   proyecto (IFLS, comunidades, hipótesis H1-H9, literatura de referencia en
   lugar del Taller 1).
4. Commit inicial en `main` y push a GitHub.

**Datos en el repositorio.** El repositorio es público y la licencia de RAND
prohíbe redistribuir la IFLS; además los datos pesan 4,3 GB y GitHub rechaza
archivos de más de 100 MB. Por eso los datos quedaron **dentro de la carpeta del
repositorio** (`01_Datos/01_Crudos/`), pero el `.gitignore` los excluye junto con
las bases derivadas. En GitHub quedan las guías, la síntesis, las reglas
(`01_Datos/CLAUDE.md`) y las instrucciones de descarga (`01_Datos/README.md`),
que es lo que pide la entrega ("datos o instrucciones para obtenerlos").

No había "Siguientes objetivos" previos (primera sesión del repositorio).

## Archivos

- **Movidos** (de la estructura anterior a la nueva):
  - `Datos/IFLS1…IFLS5/` → `01_Datos/01_Crudos/IFLS1…IFLS5/` (datos,
    documentación de RAND, guías `00_guia_IFLSx.md`, `_obsoleto/`, `_revision/`)
  - `Datos/00_sintesis_revision_IFLS.md` → `01_Datos/00_sintesis_revision_IFLS.md`
  - `Datos/derivados/salud_mental_1993.{csv,dta}` → `01_Datos/02_Procesados/`
  - `codigo/01_salud_mental_1993.py` → `02_Scripts/_exploratorio/`
  - `ProyectoFinal.pdf`, `herramientas_R_del_curso.md` → `07_Recursos/`
  - `Artículos/` → `07_Recursos/Articulos/` (sin tilde, para evitar problemas de
    rutas en R y Windows)
  - `Insumos/` → `07_Recursos/Insumos/`
  - `propuesta_ifls/*` → `10_Propuesta/` (salvo `propuesta_presentacion.pdf` →
    `04_Presentaciones/`)
  - `handoff_revision_datos_ronda5.md` →
    `06_Bitacoras/2026-11-13_handoff-revision-datos-ronda5.md`
  - `CLAUDE.md` (17-nov) → `10_Propuesta/_obsoleto/CLAUDE_2026-11-17.md`
- **Creados:** `CLAUDE.md`, `01_Datos/CLAUDE.md`, `01_Datos/README.md`,
  `HANDOFF.md`, `PLAN.md`, `README.md`, `.gitignore`, `00_main.R`,
  `proyecto_final.Rproj`, `02_Scripts/00_formato_graficas.R`,
  `02_Scripts/00_formato_tablas.R`, `05_Notas/README.md`,
  `07_Recursos/Articulos/README.md`, `07_Recursos/Insumos/README.md`,
  `.claude/skills/{bitacora-sesion,cerrar-sesion,registrar-hallazgo}/SKILL.md`,
  `.gitkeep` en las carpetas vacías y esta bitácora.
- **Modificados (solo rutas):** `02_Scripts/_exploratorio/01_salud_mental_1993.py`,
  `01_Datos/01_Crudos/IFLS5/_revision/{inv,llaves,cot}.py`, las guías y la
  síntesis de `01_Datos/`, y `10_Propuesta/00`-`06` (referencias a `Datos/`,
  `codigo/`, `Artículos/` y `herramientas_R_del_curso.md`; la fila "Carpeta" de
  `00_resumen.md` pasa a "hecho").
- **Eliminados:** las carpetas vacías `Datos/`, `codigo/` y `propuesta_ifls/`.

## Detalle por archivo

### `CLAUDE.md`
Une el contenido del `CLAUDE.md` del 17-nov (proyecto, exigencias del curso,
conclusiones sustantivas, diseño, literatura, decisiones) con las reglas de
trabajo del Taller 2 (reproducibilidad, `00_main.R` como único punto de
entrada, una carpeta de resultados por script, ramas por integrante, bitácoras,
handoff, notas, skills). Lo que cambia frente al Taller 2: las notas se agrupan
por etapa (`D`, `A`, `H`, `X`) en lugar de Parte A/B; el contraste se hace con
la literatura (E-Q, F-T) y no con el Taller 1; el control de datos antes de cada
commit es obligatorio. Las reglas de manejo de la IFLS (antes §7) pasan a
`01_Datos/CLAUDE.md`, y los pendientes (antes §10) a `PLAN.md`. Se registra la
decisión del 18-nov de retirar el árbol causal (estaba en `10_Propuesta/00` y
`04`, pero no en el `CLAUDE.md` del 17-nov). La tabla de integrantes y ramas se
copió del Taller 2 y queda por confirmar.

### `01_Datos/CLAUDE.md`
Reglas para manejar la IFLS: mapa de carpetas y guías, licencia, flujo
Crudos → Procesados → Listos, problemas de lectura, llaves, códigos, particulares
de cada ola, tratamiento y muestras, y una tabla vacía de decisiones de uso de
los datos (las recomendaciones de `10_Propuesta/02` §5 siguen sin aprobar).
Todo sale del `CLAUDE.md` del 17-nov y de la síntesis; no se agregó ninguna
cifra nueva. Claude Code lo carga al trabajar dentro de `01_Datos/`; el
`CLAUDE.md` raíz pide leerlo también antes de escribir scripts que lean datos.

### `01_Datos/README.md`
Instrucciones de descarga (registro en RAND), nombres de carpeta que esperan los
scripts y qué se versiona. Las citas de los informes de campo de IFLS2-4 quedan
pendientes (no se copiaron sin verificar).

### `.gitignore`
Excluye todo `01_Datos/01_Crudos/` menos `*.md` y `_revision/*.py|*.tsv`;
excluye `02_Procesados/` y `03_Listos/` (salvo `.gitkeep`), cualquier `.dta` o
`.rds` del repositorio, los PDF de artículos e insumos de terceros y
`09_Conversaciones/`.

### `00_main.R`
Estructura del Taller 2 con un paso nuevo: verifica que las cinco carpetas
`Household Data` estén en `01_Datos/01_Crudos/` y se detiene con un mensaje que
remite al README si faltan. Paquetes: los del curso más `haven` (marcado como
ampliación, todavía sin aprobar). La lista `scripts` está vacía; el orden
previsto queda en un comentario.

### `02_Scripts/00_formato_graficas.R` y `00_formato_tablas.R`
Copiados del Taller 2 (misma paleta, tema y exportación). Se cambiaron los
subtítulos por base (experimento/observacional) por subtítulos por alcance
(`descriptivo`, `contraste`, `placebo`), los decimales por tipo de cifra (z,
años, cm, log, rupias) y `nota_tabla()`, que ahora declara el n de personas y el
de comunidades.

### Skills
Mismo procedimiento que en el Taller 2, adaptado: `bitacora-sesion` también
marca `PLAN.md` y verifica que las bases nuevas queden ignoradas;
`cerrar-sesion` tiene un control de datos obligatorio antes del commit y crea la
rama del integrante si no existe; `registrar-hallazgo` contrasta con E-Q, F-T y
las hipótesis H1-H9, sin reformularlas después de ver resultados.

### Rutas en scripts y documentos
El script de salud mental de 1993 calcula la raíz subiendo tres niveles y lee y
escribe en `01_Datos/`. Los scripts de revisión de IFLS5 tenían rutas absolutas
de la máquina virtual (`~/mnt/Proyecto Final/...`); se actualizó la carpeta pero
siguen siendo absolutas y escriben en `~/w5/`: son registro de la revisión, no
parte del pipeline. No se volvió a correr ningún script.

## Pendientes

- Confirmar integrantes y ramas (tabla copiada del Taller 2).
- Cada integrante: clonar, poner los datos en `01_Datos/01_Crudos/` y crear su
  rama (P0.3); verificar el registro en RAND (P0.4).
- Decisiones previas del equipo (P1.1-P1.6), sobre todo el lenguaje del
  pipeline y las recomendaciones de datos.
- Completar las citas de los informes de campo de IFLS2-4 (PL.6).
- Siguiente paso técnico: `01_tracks.R` (P2.1) y `02_precio_arroz.R` (P2.2).
