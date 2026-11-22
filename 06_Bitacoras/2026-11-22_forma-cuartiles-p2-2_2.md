# Bitácora — 2026-11-22 (2): forma del efecto por cuartiles (P2.2)

## Resumen

Objetivo: cerrar P2.2, la forma del efecto del alza del precio del arroz sobre
el cambio en el HAZ, con los cuartiles del alza. Mateo Olmos, con plan previo
aprobado por él y Claude en el chat de Claude; Mateo hizo los cambios en su
copia local.

Desarrollo:

1. **Plan** con una decisión de Mateo: la figura usa la especificación (4),
   la más completa y la que más se aleja de E-Q en P2.1.
2. **Script `07_cuartiles.R`**, probado primero con datos simulados y luego
   con los reales dentro de `00_main.R` (siete scripts sin errores).
3. **Mudanza del proyecto local:** iCloud Drive estaba lleno y RStudio no podía
   guardar `00_main.R` («generic error 2»). El proyecto se copió con `ditto` a
   `~/proyecto_final`; se verificó la rama `MateoOlmosB`, el commit de P2.1
   (`0e5cca6`) y las cinco olas en `01_Datos/01_Crudos/`. La copia de iCloud se
   borra cuando se confirme que todo corre desde la nueva carpeta.
4. **Nota del hallazgo** contrastada con P2.1 y con E-Q.

**Siguientes objetivos que traía `HANDOFF.md`:**

- (1) P2.2: **cumplido**.
- (2) P2.3 y (3) P3.1: no se trabajaron.

## Archivos

- **Creados:**
  - `02_Scripts/07_cuartiles.R`;
  - `03_Resultados/Tablas/07_cuartiles/ninos_cuartiles_especificaciones.{png,csv}`;
  - `03_Resultados/Figuras/07_cuartiles/ninos_cuartiles_coeficientes.png`;
  - `05_Notas/07_cuartiles/A_forma_cuartiles.md`;
  - esta bitácora.
- **Modificados:**
  - `00_main.R`: `07_cuartiles.R` en la lista de scripts y sus dos carpetas de
    salida;
  - `05_Notas/README.md`, `README.md`, `PLAN.md` y `HANDOFF.md`.
- **Bases:** ninguna nueva. `07_cuartiles.R` lee `base_estimacion.rds`.

## Detalle por archivo

### `02_Scripts/07_cuartiles.R`

- **Tratamiento:** los cuartiles del alza que construye `02_precio_arroz`
  (cuartiles de la dosis entre comunidades). Entran como tres indicadoras (Q2,
  Q3, Q4), con Q1 como referencia. La intuición: en vez de imponer una recta,
  se deja que cada tramo del alza tenga su propio efecto.
- **Especificaciones:** las mismas cuatro de `06_ate.R`, con los mismos
  controles, efectos fijos y errores agrupados por comunidad. La lista de
  controles está copiada de `06_ate.R` (con un comentario que lo advierte) para
  no tocar ese script, que ya estaba en el commit de P2.1.
- **Alza media de cada cuartil:** promedio de la dosis entre los niños de la
  base. Sirve para ubicar los puntos en el eje x de la figura y para anclar las
  rectas.
- **Figura (especificación 4):** coeficiente de cada cuartil con su intervalo
  al 95 %, Q1 en cero, y dos rectas que parten del alza media de Q1: la de E-Q
  (−0,135 por +100 %) y la del efecto promedio de la misma especificación,
  re-estimado dentro del script (−0,329, igual que en `06_ate`).
- **Chequeo mínimo:** cuatro cuartiles con alza media creciente, ningún modelo
  con más niños que la base y coeficientes finitos.

## Resultados nuevos (tablas, figuras, bases)

Contraste entre comunidades con mayor y menor alza (pregunta 1, forma del ATE).
La interpretación está en la nota
[A_forma_cuartiles.md](../05_Notas/07_cuartiles/A_forma_cuartiles.md)
(vigente). Cifras clave, con 2.421 niños en 294 comunidades:

- Alza media por cuartil: +42 %, +61 %, +82 % y +118 % (75, 72, 74 y 73
  comunidades).
- Especificación (4), frente a Q1: Q2 −0,189 (EE 0,093), Q3 −0,116 (0,094), Q4
  −0,295 (0,104).
- Q4 es distinto de cero en las cuatro especificaciones; Q3 en ninguna. Q2 está
  por debajo de Q3 en las cuatro.
- Los puntos quedan dentro de su incertidumbre alrededor de la recta de P2.1.

## Pendientes

- **P2.3:** validación (placebo y robustez), incluida la prueba de si la
  diferencia con E-Q viene de la medida del precio.
- **Subir los commits:** la cuenta de GitHub de Mateo (`Mateo10o`) no tiene
  permiso de escritura en el repositorio. Pedir acceso a Santiago o subir por
  un fork.
- Borrar la copia del proyecto en iCloud cuando se confirme que todo corre
  desde `~/proyecto_final`.
