---
name: cerrar-sesion
description: Cierra una sesión del proyecto final a nivel de repositorio — revisa que no entre ningún dato de la IFLS, hace commit y push a la rama del integrante (nunca a main) y copia el registro crudo (.jsonl) de la conversación a 09_Conversaciones/ (ignorada por git). Es mecánica; la bitácora y el handoff los escribe antes bitacora-sesion. Usar cuando el usuario pida "cerrar sesión", "hacer el commit", "subir los cambios", "push" o "guardar la conversación".
model: haiku
---

# Cerrar sesión de trabajo

Último paso de una sesión: versiona lo hecho y guarda la conversación. Va
**después** de `bitacora-sesion`, para que el commit incluya la bitácora y el
handoff. Hace dos cosas en este orden:

1. Commit y push a la rama del integrante (nunca a `main`), sin datos.
2. Copiar el `.jsonl` de la conversación a `09_Conversaciones/`.

Antes de empezar, confirma que existe la bitácora de hoy en `06_Bitacoras/` y que
`HANDOFF.md` aparece modificado en `git status`. Si falta alguno, avisa y sugiere
correr primero `bitacora-sesion`; no la escribas aquí. Si algo no es inferible
con certeza (quién trabajó, qué archivos son de la sesión), pregunta. Si el
usuario pide solo una de las partes, haz solo esa.

## Paso 1: commit y push a la rama del integrante

La tabla integrante → rama está en `CLAUDE.md` §4.2.

1. **Identificar la rama.** Compara `git branch --show-current` y
   `git config user.name` con la tabla.
   - Rama del integrante: continúa.
   - `main`: **no hagas commit**. Si los cambios están sin commitear, cambia con
     `git switch <rama>` (o `git switch -c <rama>` si no existe todavía; los
     cambios se trasladan). Si hay commits locales en `main` que no están en
     `origin/main`, detente y pregunta cómo moverlos.
   - Rama de otro integrante, o no se sabe quién trabajó: pregunta.
2. **Control de datos (obligatorio, el repositorio es público).**
   - Corre `git status --short` y `git diff --stat`.
   - Ningún archivo de `01_Datos/` puede entrar salvo `.md`, `.gitkeep` y
     `01_Crudos/**/_revision/*.py|*.tsv`. Ningún `.dta`, `.rds`, `.Rds`,
     `.sav` ni `.csv` con microdatos en ninguna carpeta. Ningún PDF de
     `07_Recursos/Articulos/` ni de `07_Recursos/Insumos/`.
   - Si aparece alguno (por ejemplo porque alguien cambió el `.gitignore` o usó
     `git add -f`), **detente y avisa**; no lo agregues. Nunca uses `git add -f`.
   - Revisa que los `.csv` de `03_Resultados/` sean tablas agregadas (no una fila
     por persona u hogar). Si dudas, pregunta.
3. **Agregar por nombre** (no `git add -A` a ciegas):
   - Sí se versionan: la bitácora, `HANDOFF.md`, `PLAN.md`, `CLAUDE.md`,
     `01_Datos/CLAUDE.md`, los README, los scripts de `02_Scripts/`, las tablas y
     figuras de `03_Resultados/`, las notas de `05_Notas/`, los borradores de
     `04_Presentaciones/` y los documentos de `10_Propuesta/`.
   - No se versionan: `09_Conversaciones/`, archivos temporales de RStudio o de
     Office (`~$*`), `.DS_Store`.
   - Si aparecen archivos modificados que no son de esta sesión, o archivos
     pesados, pregunta antes de incluirlos.
4. **Commit.** Mensaje en español, en imperativo, que resuma la sesión (p. ej.
   "Construir el precio del arroz por comunidad 1997-2000"), con el cuerpo
   `Bitácora: 06_Bitacoras/<archivo>.md`.
5. **Push a la rama del integrante:** `git push origin <rama>`
   (`git push -u origin <rama>` la primera vez).
   - Si se rechaza porque la remota avanzó: `git pull --no-rebase origin <rama>`,
     resolver conflictos con el usuario y reintentar. Nunca `--force`.
   - **Nunca** `git push origin main`, ni `<rama>:main`, ni merge a `main`.
     Llevar cambios a `main` es decisión del integrante, con un pull request.
6. Si el usuario pidió explícitamente no versionar, omite este paso y dilo.

## Paso 2: copiar el `.jsonl` de la conversación

Claude Code guarda cada sesión como un `.jsonl` en `~/.claude/projects/<slug>/`,
donde `<slug>` es la ruta del directorio de trabajo con todo carácter no
alfanumérico cambiado por `-`. Esta skill se invoca sin argumentos.

```bash
# Raíz del directorio de trabajo actual (repo principal o worktree)
TOPLEVEL=$(git rev-parse --show-toplevel)

# Carpeta de proyecto de Claude: la ruta con lo no alfanumérico cambiado por "-"
CARPETA="$HOME/.claude/projects/$(printf '%s' "$TOPLEVEL" | sed -E 's/[^A-Za-z0-9]/-/g')"

# Sesión actual = .jsonl modificado más recientemente en esa carpeta
SESSION_FILE=$(ls -t "$CARPETA"/*.jsonl 2>/dev/null | head -1)

if [ -z "$SESSION_FILE" ]; then
  echo "No se encontró ningún .jsonl en: $CARPETA"; exit 1
fi

mkdir -p "$TOPLEVEL/09_Conversaciones"
DEST="$TOPLEVEL/09_Conversaciones/$(date +%Y-%m-%d)_$(basename "$SESSION_FILE")"
cp "$SESSION_FILE" "$DEST"
echo "Copiado: $SESSION_FILE -> $DEST"
```

Reglas:

- Es una copia: el original no se toca.
- Antes de copiar, muestra qué archivo se eligió (nombre y fecha). Si hay varios
  con fechas cercanas y hay duda, pregunta.
- `09_Conversaciones/` está en `.gitignore`: no se versiona. No uses `git add -f`.
- La ruta del proyecto tiene espacios y acentos si vive en «Proyecto Final»; el
  `sed` los convierte en `-`. Si no aparece la carpeta, lista
  `~/.claude/projects/` y pregunta cuál es, en vez de improvisar.
- Si la sesión no corrió en Claude Code (p. ej. en claude.ai), no hay `.jsonl`
  local: dilo y sigue.

## Cierre

Reporte corto: resultado del control de datos, hash y mensaje del commit, rama
del push (o por qué no se hizo), ruta del `.jsonl` copiado y los siguientes
objetivos de `HANDOFF.md`. Si el integrante quiere llevar los cambios a `main`,
recuérdale que se hace aparte, con un pull request desde su rama.
