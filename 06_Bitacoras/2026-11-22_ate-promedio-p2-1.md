# Bitácora — 2026-11-22: efecto promedio del alza del arroz en la talla (P2.1)

## Resumen

Objetivo: cerrar P2.1, el efecto promedio del alza del precio del arroz sobre el
cambio en el HAZ entre 1997 y 2000, con `feols`. Es la primera sesión de Mateo
Olmos en el proyecto. Se trabajó con plan previo aprobado por Mateo y Claude en
el chat de Claude (no en Claude Code), con Mateo haciendo todos los cambios en
su copia local.

Desarrollo:

1. **Puesta en marcha.** Mateo clonó el repositorio, creó la rama
   `MateoOlmosB` y ubicó las cinco olas de la IFLS en `01_Datos/01_Crudos/`.
   `00_main.R` corrió los cinco scripts de H1 sin errores y reprodujo la base de
   Santiago: 2.421 niños en 294 comunidades.
2. **Plan de P2.1** y tres decisiones de Mateo antes de ver resultados (ver
   «Detalle por archivo»): edad como en E-Q, pendiente del bosque dentro de P2.1
   como dice `PLAN.md`, y el efecto también en cm, como aproximación.
3. **Script `06_ate.R`.** Se probó primero con datos simulados con las mismas
   columnas de la base (recuperó el efecto verdadero dentro de su EE) y luego
   corrió con los datos reales dentro de `00_main.R`.
4. **Nota del hallazgo** contrastada con E-Q, con Frankenberg y Thomas (2017) y
   con la nota de desgaste.

**Siguientes objetivos que traía `HANDOFF.md`:**

- (1) P2.1: **cumplido**.
- (2) P2.2 y (3) P2.3: no se trabajaron.

## Archivos

- **Creados:**
  - `02_Scripts/06_ate.R`;
  - `03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.{png,csv}`;
  - `05_Notas/06_ate/A_ate_promedio.md`;
  - esta bitácora.
- **Modificados:**
  - `00_main.R`: `06_ate.R` en la lista de scripts y
    `03_Resultados/Tablas/06_ate` en las carpetas de salida;
  - `05_Notas/README.md`, `README.md`, `PLAN.md` y `HANDOFF.md`.
- **Bases:** ninguna nueva. `06_ate.R` lee `base_estimacion.rds` y `haz.rds`.

## Detalle por archivo

### `02_Scripts/06_ate.R`

- **Variable dependiente:** cambio en el HAZ (OMS) entre 1997 y 2000. Con dos
  periodos, las primeras diferencias equivalen al panel con efectos fijos
  individuales de E-Q (`CLAUDE.md`, decisión del 20-nov).
- **Tratamiento:** la dosis principal, cambio proporcional del precio nominal del
  arroz en la comunidad de 1997, winsorizada en p1/p99 (registro §4). 1 = +100 %.
- **Cuatro especificaciones** (`PLAN.md` P2.1): (1) sin controles; (2) controles
  de 1997 del cuadro A1 de E-Q sin los programas sociales (registro §5), más el
  indicador de entrevista en 1998 y los indicadores de faltante; (3) más efectos
  fijos de provincia; (4) más el log del precio de 1997, para comparar
  comunidades que partían del mismo nivel de precio.
- **Edad (decisión de Mateo):** edad en meses en 1997 y su cubo, sin término
  cuadrático, como E-Q. Es una réplica, así que se copia su forma funcional.
- **Errores:** agrupados por comunidad de 1997 (el tratamiento varía por
  comunidad) y, al lado, robustos sin agrupar, que son los que reporta E-Q.
- **Bosque causal (decisión de Mateo: dentro de P2.1, como dice el plan):** `grf`
  con tratamiento continuo, las mismas X y niños que la especificación (4),
  efectos de provincia como indicadoras, `clusters` por comunidad,
  `seed = 2026` y `num.threads = 1`. `average_treatment_effect()` con W continuo
  da la pendiente promedio, que pondera distinto que MCO: es una fila de
  robustez, no el mismo estimando (`CLAUDE.md`, decisión del 20-nov).
- **cm (decisión de Mateo: aproximado, con salvedad):** el HAZ es lineal en la
  talla (L = 1 en el método LMS de la OMS), así que la desviación estándar de la
  referencia en cm a la edad y el sexo de cada niño en 2000 es
  1 / (z(talla + 1) − z(talla)), con `anthro` hasta 1.856 días y `anthroplus`
  después, igual que `04_haz`. β se multiplica por la media de esa desviación
  (5,03 cm, 2.421 niños).
- **Chequeo mínimo:** ningún modelo usa más niños que la base y las estimaciones
  son finitas.
- **Colinealidad:** `fixest` saca los indicadores de faltante del productor de
  arroz y del tamaño del hogar, porque repiten a otro indicador. No afecta a β.

## Resultados nuevos (tablas, figuras, bases)

`03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.{png,csv}`: contraste
entre comunidades con mayor y menor alza (pregunta 1, etapa del ATE). La
interpretación está en la nota
[A_ate_promedio.md](../05_Notas/06_ate/A_ate_promedio.md) (vigente). Cifras
clave, con 2.421 niños en 294 comunidades en las cuatro columnas:

- β en HAZ por +100 %: −0,217 (EE agrupado 0,119), −0,238 (0,109), −0,339
  (0,112) y −0,329 (0,139). En cm: −1,09 a −1,71.
- Pendiente promedio del bosque: −0,260 (EE 0,132).
- Frente a E-Q (−0,135, EE robusto 0,041): misma dirección, 1,6 a 2,5 veces más
  grande, intervalos que se traslapan. Clasificado como «difiere (atribuible)»,
  por verificar: la medida del precio de E-Q mezcla fuentes y tiene más ruido, y
  no usa efectos fijos de provincia.

## Pendientes

- **P2.2:** forma con cuartiles y figura con la recta de E-Q.
- **P2.3:** validación. La robustez sin winsorizar y con la dosis solo en kg
  sirve también para probar si la diferencia con E-Q viene de la medida del
  precio.
- **Contar al equipo** el salto de β al agregar efectos fijos de provincia y la
  diferencia de magnitud con E-Q, porque ambos van a la presentación.
