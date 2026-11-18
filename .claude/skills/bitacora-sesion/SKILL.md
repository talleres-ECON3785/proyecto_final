---
name: bitacora-sesion
description: Registra el trabajo de una sesión del proyecto final (IFLS) — escribe la bitácora en 06_Bitacoras/ con el formato de CLAUDE.md, verifica las notas de hallazgos de 05_Notas/ y actualiza HANDOFF.md (estado actual, dos a tres siguientes objetivos y registro de sesiones) y las casillas de PLAN.md. No hace commit ni push ni copia la conversación: eso lo hace después la skill cerrar-sesion. Usar cuando el usuario pida "registrar la sesión", "escribir la bitácora" o "actualizar el handoff".
---

# Bitácora de la sesión

Al terminar una sesión de trabajo en el proyecto, hace dos cosas en este orden:

1. Escribir la bitácora de la sesión en `06_Bitacoras/`.
2. Actualizar `HANDOFF.md` (raíz) y `PLAN.md` a partir de esa bitácora.

El commit, el push y la copia del `.jsonl` **no** son de esta skill: los hace
`cerrar-sesion` después.

Básate solo en lo que ocurrió en la conversación. Confirma los archivos
afectados con `git status` / `git diff --stat` (y `git log` si hubo commits).
Si algo no es inferible con certeza (un supuesto, un resultado ambiguo, quién
del equipo trabajó, cuáles deben ser los siguientes objetivos), pregunta al
usuario en vez de adivinar. Si el usuario pide solo una de las partes, haz solo
esa.

## Paso 1: bitácora

Antes de escribir, lee `HANDOFF.md` y **solo la última bitácora** de
`06_Bitacoras/` (la más reciente por nombre). Abre otras únicamente si la sesión
retoma una decisión o un resultado que el handoff no explica.

Nombre: `YYYY-MM-DD_slug-descriptivo.md` (minúsculas, guiones), con la fecha real
de la sesión. Si ya hay una del mismo día, agrega un sufijo (`_2`) o pregunta.

Estructura (la de `CLAUDE.md` §7):

```markdown
# Bitácora — YYYY-MM-DD: <descripción corta>

## Resumen
Objetivo de la sesión y desarrollo, en pocos párrafos. Indica cuáles de los
"Siguientes objetivos" que traía HANDOFF.md se cumplieron, cuáles avanzaron y
cuáles no se trabajaron, con su número de PLAN.md (P*k.n*).

## Archivos
- Creados: ...
- Modificados: ...
- Movidos o eliminados: ...

## Detalle por archivo
### `ruta/relativa/archivo`
Qué cambió, decisiones de implementación, supuestos usados y la intuición en
lenguaje natural de cada decisión.

## Resultados nuevos (tablas, figuras, bases)
Por cada uno: qué busca comunicar, cómo se generan los datos que lo alimentan y
qué rol cumple en el proyecto (etapa 1-6 de CLAUDE.md §6). Para las bases de
01_Datos/: filas, llave única y observaciones perdidas en cada filtro. Omitir si
no hubo.

## Pendientes
Lo que quedó sin hacer, supuestos sin confirmar y el siguiente paso. Alimenta los
"Siguientes objetivos" de HANDOFF.md.
```

Reglas de contenido (de `CLAUDE.md` y `01_Datos/CLAUDE.md`):

- **Datos:** reporta cuántas personas, hogares y comunidades se pierden en cada
  limpieza, filtro o unión, y con qué llave se unió. Si se tomó una decisión de
  uso de los datos (unidad de comunidad, construcción del precio, cohortes,
  pesos…), cítala con su pregunta de la síntesis (S §11) y regístrala también en
  `01_Datos/CLAUDE.md` §9.
- **Nunca cifras inventadas:** toda cifra de la bitácora viene de la salida de un
  script de la sesión o de un archivo de `03_Resultados/`, con su ruta.
- No juicios de "bueno" o "malo" sobre resultados ni entusiasmo por coeficientes
  o significancia.
- Distingue estimando, estimador y estimación, y la escala de cada número (z de
  HAZ, años de escolaridad, cm, Δlog del precio). Di si es un contraste entre
  comunidades (causal bajo el diseño), un placebo o una descripción.
- Los CATE y los subgrupos son estimaciones con incertidumbre; que el bosque
  divida por una covariable no la hace la causa de la heterogeneidad. Menciona
  el número de comunidades detrás de cada grupo.
- Para las variables que construyen un estimador (tratamiento, cohorte no
  expuesta, puntajes AIPW, prioridad del RATE…), explica cada una por aparte:
  fuente (página del artículo, sección de `10_Propuesta/` o de la guía de datos),
  cómo se calcula y qué rol cumple en la fórmula.
- Las decisiones metodológicas relevantes se registran también en "Decisiones
  tomadas" de `CLAUDE.md` (o en "Análisis descartados").
- Sin código salvo que aporte a entender una decisión. Español en todo.

### Verificación de notas de hallazgos

Antes de dar por escrita la bitácora, revisa que cada tabla o figura nueva o
modificada en la sesión (`git status` sobre `03_Resultados/`) tenga su nota en
`05_Notas/` y que `05_Notas/README.md` la liste.

- Si falta alguna, invoca la skill `registrar-hallazgo`.
- Si hay contradicciones sin conciliar, menciónalas en "Pendientes" y como
  bloqueo en `HANDOFF.md`.
- En "Resultados nuevos", enlaza la nota en lugar de repetir su explicación.
- Si la sesión no generó ni cambió resultados, omite esta verificación.

### Verificación de datos

Si la sesión tocó `01_Datos/`, confirma con `git status --ignored 01_Datos` que
las bases nuevas quedaron ignoradas (no deben aparecer como archivos por
agregar). Si alguna aparece, avisa al usuario antes de seguir: es un problema
de licencia, no de orden.

## Paso 2: actualizar `HANDOFF.md` y `PLAN.md`

- **`PLAN.md`:** marca `[x]` las casillas que la sesión terminó. Si surgió una
  tarea nueva, agrégala en el hito que corresponda con el siguiente número.
- **Siguientes objetivos:** reescríbela con **dos a tres** tareas, tomadas de las
  primeras casillas sin marcar de `PLAN.md`, en su orden, citando el número
  (P*k.n*). Cada una con el archivo a producir, un criterio de terminado
  verificable y, si aplica, el integrante a cargo. Un objetivo no terminado se
  mantiene. Actualiza los bloqueos y preguntas abiertas: quita los resueltos y
  agrega los nuevos. Si hay varias opciones razonables, pregunta.
- **Estado actual:** reescríbelo para reflejar qué existe y funciona hoy (datos
  locales, bases derivadas, scripts, resultados, notas). No es un historial.
- **Registro de sesiones:** agrega una entrada arriba (la más reciente primero):

  ```markdown
  ### YYYY-MM-DD: <descripción corta>

  - <Integrante> (`<rama>`). Qué se hizo, en tres a cinco líneas, y qué pasos del
    plan avanzó o cerró. Si un objetivo no se terminó, qué avanzó y qué lo
    impidió.
  - Bitácora: [<archivo>.md](06_Bitacoras/<archivo>.md)
  - **Siguientes objetivos:** (1) ...; (2) ...; (3) ...
  ```

  No edites las entradas anteriores.

## Cierre

Termina con un reporte corto: ruta de la bitácora, notas de `05_Notas/` creadas
o actualizadas, casillas de `PLAN.md` marcadas y los dos a tres siguientes
objetivos. Después, **indica que el siguiente paso es la skill `cerrar-sesion`**
(commit y push a la rama del integrante, y copia del `.jsonl`) y pregunta si
quiere correrla ahora. No hagas commit ni push desde aquí.
