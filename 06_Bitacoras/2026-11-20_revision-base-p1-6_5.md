# Bitácora — 2026-11-20 (5): revisión de la base antes de H2 (P1.6)

## Resumen

Objetivo: cerrar P1.6, la revisión de la base lista antes de estimar el ATE.
Había dos preguntas: (a) por qué en las comunidades de mayor alza hay menos
niños con HAZ válido en 1997, y (b) qué hacer con la cola del ΔHAZ. Se planeó
en modo plan, primero con una exploración de solo lectura y después con los
cambios.

Desarrollo:

1. La exploración mostró que la brecha del cuartil 4 viene de niños sin
   evaluación de salud y de evaluados sin talla, y que se concentra entre
   provincias.
2. Santiago decidió la cola del ΔHAZ **antes de ver el ATE**: se mantiene en la
   estimación principal y va una columna de robustez sin |ΔHAZ| > 3 en P2.3.
3. Se amplió `05_base.R` con tres tablas nuevas y con las pendientes con y sin
   efectos fijos de provincia. Las cifras exportadas coinciden con las de la
   exploración.

**Siguientes objetivos que traía `HANDOFF.md`:**

- (1) P1.6: **cumplido**.
- (2) P2.1 y (3) P2.2: no se trabajaron.

## Archivos

- **Creados:**
  - `03_Resultados/Tablas/05_base/ninos_haz1997_motivos.{png,csv}`;
  - `03_Resultados/Tablas/05_base/ninos_haz1997_balance.{png,csv}`;
  - `03_Resultados/Tablas/05_base/ninos_dhaz_cola.{png,csv}`;
  - `03_Resultados/Tablas/05_base/ninos_dhaz_cola_perfil.csv`.
- **Modificados:**
  - `02_Scripts/05_base.R`;
  - `03_Resultados/Tablas/05_base/ninos_desgaste_alza.png` y
    `ninos_desgaste_alza_pendientes.csv`, con pendientes nuevas;
  - `05_Notas/05_base/D_desgaste_segun_alza.md` y `05_Notas/README.md`;
  - `registro_decisiones.md`, `PLAN.md`, `README.md` y `HANDOFF.md`.
- **Base local, sin versionar:** `01_Datos/03_Listos/base_estimacion.rds`, con
  una columna nueva (`dhaz_mayor_3`).

## Detalle por archivo

### `02_Scripts/05_base.R`

- **Población de partida:** toma también `res97us` (evaluación de salud de 1997)
  de `tracks.rds` y `talla97` de `haz.rds`, para separar los motivos.
- **Base lista:** gana `dhaz_mayor_3` (|ΔHAZ| > 3), que P2.3 usará para la
  robustez sin la cola.
- **Pendientes de retención sobre la dosis:** cada paso se estima sin y con
  efectos fijos de provincia, y se agrega el paso «evaluación de salud en
  1997». La intuición: si la brecha es entre provincias, los efectos fijos de
  provincia la absorben.
- **Motivo del HAZ faltante:** es excluyente y sigue el orden en que se pierde
  al niño: sin evaluación, evaluado sin talla, sin fecha de nacimiento o de
  medición, HAZ fuera de ±6.
- **Balance:** MCO de cinco moderadores pre-registrados (pobre, urbano, madre
  con más que primaria, comprador neto, mujer) sobre «con HAZ en 1997 × dosis»,
  con efectos fijos de provincia y EE agrupado por comunidad. Si la interacción
  fuera distinta de cero, la composición de los medidos cambiaría con el alza.
- **Cola:** por cuartil, niños con |ΔHAZ| > 2 y > 3, y el perfil (edad y HAZ de
  1997 y 2000) dentro y fuera de la cola.

### `registro_decisiones.md`, `PLAN.md`, `README.md`

- **Registro §5:** la cola del ΔHAZ se mantiene y va una robustez sin
  |ΔHAZ| > 3. Decisión de Santiago, anotada en el historial.
- **`PLAN.md`:** P1.6 marcada. P2.3 agrega la columna sin |ΔHAZ| > 3.
- **README:** las salidas nuevas en la fila de `05_base.R`.

## Resultados nuevos (tablas, figuras, bases)

Todos son descriptivos (validación de la pregunta 1). La interpretación está en
la nota [D_desgaste_segun_alza.md](../05_Notas/05_base/D_desgaste_segun_alza.md)
(vigente, reescrita). Cifras clave, sobre 3.191 niños en 297 comunidades con
precio:

- **Pendientes por +100 % de alza** (`ninos_desgaste_alza_pendientes.csv`):
  - HAZ válido en 1997: −0,090 (EE 0,038) sin efectos fijos de provincia;
    −0,045 (EE 0,033; p = 0,165) con ellos;
  - evaluación de salud en 1997: −0,062 sin efectos fijos; −0,023 (EE 0,027)
    con ellos;
  - HAZ en 2000, de los medidos en 1997: −0,003 sin efectos fijos; −0,004 con
    ellos.
- **Motivos** (`ninos_haz1997_motivos.csv`): sin evaluación de salud, 16,0 % en
  el cuartil 4 frente a 10,2-11,6 % en los demás; evaluado sin talla, 4,4 %
  frente a 1,5-1,7 %.
- **Balance** (`ninos_haz1997_balance.csv`): interacciones entre −0,073 y
  +0,085, con p entre 0,211 y 0,744.
- **Cola** (`ninos_dhaz_cola.csv`, `ninos_dhaz_cola_perfil.csv`):
  - 110 niños (4,5 %) con |ΔHAZ| > 3, entre 3,8 % y 6,2 % por cuartil;
  - edad media en 1997 de 21,6 meses (frente a 39,9);
  - HAZ medio de −0,425 en 1997 (frente a −1,827).
- **Base lista:** sin cambios en filas (2.421 niños, 294 comunidades) y una
  columna más.

## Pendientes

- **Pendiente residual:** dentro de provincia queda −0,045 en la cobertura de
  1997. No se distingue de cero, pero tampoco se puede descartar. Hay que
  leerlo junto con la especificación 3 de P2.1.
- **Fuera de `03_Resultados/`:** la cobertura por provincia y el cruce con las
  34 comunidades con precio de 1998 (23 en el cuartil 1, según la exploración)
  solo salieron en la consola.
- **Siguiente:** P2.1, el ATE con `feols`.
