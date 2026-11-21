# Bitácora — 2026-11-20 (3): registro de decisiones, pre-registro y plan nuevo

## Resumen

Objetivo: cerrar las decisiones previas antes de construir las bases y dejar
el proyecto con una fuente única de lo confirmado.

Desarrollo:

1. **Alcance revisado y confirmado.** Se discutió volver a incluir resultados de
   2014 y, después, el logro educativo: primero la escolaridad en 2000 y luego
   el rendimiento en pruebas (EK de 2000). Para comparar se hicieron conteos
   exploratorios con los microdatos (ver "Resultados nuevos"). Santiago descartó
   el rendimiento porque la prueba de 2000 no es comparable con la de 1997, y el
   efecto dependería de cómo se construyera el resultado. Se mantiene solo
   estatura.
2. **Pre-registro de la heterogeneidad** (P1.3 del plan anterior). Se cotejaron
   con el PDF y el suplemento de E-Q las cinco interacciones (cuadros A4-A5),
   sus definiciones (pobre = línea oficial de Widyanti et al. 2009, nota 3, p. 4;
   madre con educación baja = primaria o menos, p. 5) y los grupos de edad de la
   fig. 5 (0-2 y 3-5 años). Se fijaron seis GATE, tres familias de Holm y AUTOC.
3. **R para todo el pipeline** (P1.4 del plan anterior).
4. **`registro_decisiones.md`.** Santiago pidió un archivo conciso solo con lo
   confirmado, porque la propuesta se escribió antes de conocer las
   limitaciones de los datos. Se descartó T1 (fuentes distintas entre años) y se
   tomaron, con preguntas cerradas, las decisiones de datos que faltaban.
5. **`PLAN.md` rehecho desde cero** con lo que falta, a partir solo del registro
   y de la conversación. **`10_Propuesta/` queda histórica** y ya no se
   consulta, salvo el pre-registro.

**Siguientes objetivos que traía `HANDOFF.md`:**

- (1) Equipo en el repositorio y decisiones previas: las decisiones quedaron
  tomadas (por Santiago; falta contarlas al equipo, ahora P0.3). La puesta del
  equipo en el repositorio no se trabajó.
- (2) `01_tracks.R`: no se trabajó (ahora P1.1).
- (3) `02_precio_arroz.R`: no se escribió. Quedó cerrada su construcción
  (fuentes, mediana de todas las calidades, winsorizado) salvo el tipo de
  terciles, que deciden los datos (ahora P1.2).

## Archivos

- Creados: `registro_decisiones.md`,
  `10_Propuesta/07_preregistro_heterogeneidad.md`, esta bitácora.
- Modificados: `PLAN.md` (reescrito), `CLAUDE.md`, `README.md`,
  `01_Datos/CLAUDE.md`, `07_Recursos/Articulos/00_hallazgos_articulos.md`,
  `HANDOFF.md`.
- Movidos o eliminados: ninguno.

## Detalle por archivo

### `registro_decisiones.md`

Fuente única de lo confirmado; manda sobre `CLAUDE.md`, `PLAN.md` y la
propuesta. Solo lleva lo decidido, sin lo descartado. Una tarea del plan pasa
al registro cuando se completa. Secciones:

1. **Administrativas:** R para todo; ampliaciones `haven`, `get_scores`,
   `best_linear_projection`, `average_treatment_effect(subset = …)` y
   `fwildclusterboot` si se usa.
2. **Las tres preguntas**, con ΔHAZ 1997→2000 de la cohorte de 0-5 años en 1997
   como resultado único.
3. **Identificación y tratamiento:** contraste de más alza frente a menos alza,
   asignado por `commid97`; tres versiones (abajo).
4. **Precio:** fuentes presentes en 1997 y 2000 (posyandu `pos_h` + tiendas y
   mercados `bk2_hpj`), mediana de **todas las calidades** por comunidad y año,
   cambio proporcional nominal, winsorizado en p1/p99. La opción de todas las
   calidades la eligió Santiago frente a la recomendada (solo calidad media):
   da más reportes por comunidad, a costa de que la composición de calidades
   pueda cambiar entre años.
5. **Muestra y variables:**
   - HAZ OMS (`anthro`/`anthroplus`), edad en meses por fechas, fuera |z| > 6;
   - entrevistas de 1998 con un indicador y una robustez sin ellas;
   - sin pesos (ponderado como robustez);
   - controles del cuadro A1 de E-Q sin los cinco programas de la red de
     seguridad social;
   - comprador neto binario (valor comprado > producción propia, `b1_ks1` 1997);
   - pobre = bajo la línea de Widyanti o, si no se consigue, el cuartil
     inferior.
6. **Holm y AUTOC.**

Variables que construyen los estimadores:

- **Dosis** (registro §3-4): cambio proporcional `(P2000 − P1997) / P1997` de la
  mediana comunitaria del precio, en la escala de E-Q (1 = +100 %, p. 5). Es el
  regresor de la pregunta 1 y de la réplica de las interacciones.
- **Cuartiles:** Q2-Q4 de la dosis frente a Q1. Muestran la forma de la
  respuesta sin suponerla lineal.
- **Terciles:** tercil alto = 1 y bajo = 0, sin el medio. Es el W binario del
  bosque, porque `rank_average_treatment_effect` lo exige.
- **Puntajes AIPW** (pre-registro §2): Γ_i de `get_scores` del bosque con
  terciles. Su promedio en un subgrupo es el GATE, y su regresión sobre una
  dummy da el contraste entre grupos con errores agrupados.
- **Prioridad del RATE** (registro §6): −τ̂ del bosque, estimada en una mitad de
  las comunidades y evaluada en la otra. τ < 0 es daño, así que el signo menos
  pone primero a los más afectados.

### `10_Propuesta/07_preregistro_heterogeneidad.md`

Pre-registro con fecha, que no se edita después de ver resultados. Los cambios
van en una sección "Desviaciones".

- **§1:** las cinco interacciones de E-Q con β2 (EE) para HAZ y para retraso en
  talla. La "edad crítica" no está definida en el artículo; por el color de la
  fig. 5 sería 0-2 años (inferencia nuestra, marcada así).
- **§2:** los seis GATE con X = 1 y X = 0, la predicción y la variable de la
  IFLS (a verificar en H1).
- **§3:** Holm y sus tres familias. Se eligió Holm simple y no una secuencia con
  la edad primero, porque la predicción para la edad viene de una asociación
  de E-Q en 2014.
- **§4:** AUTOC, por la pregunta del cliente (a quién atender primero) y porque
  es la métrica del Lab 10.
- **Desviación del mismo día:** T1 se descartó, así que F2 usa la dosis.

### `PLAN.md`

Reescrito desde cero con un resumen de lo hecho y lo pendiente:

- H0 equipo; H1 bases (P1.1 tracks, P1.2 precio, P1.3 X de 1997, P1.4 HAZ, P1.5
  base lista); H2-H4 las tres preguntas; H5 asesoría; H6 presentación; H7
  entrega; "Por verificar antes de usar".
- No se heredó lo que no se habló en la sesión: Lasso, spline, Yamauchi-Larson,
  la exclusión de Sumatra y Kalimantan, y las tareas de literatura salvo las
  citas de los informes de campo.
- La asesoría figuraba como hecha en el archivo anterior. Se dejó pendiente,
  porque llevaba resultados que no existen.

### `CLAUDE.md`

- El encabezado y §1 remiten al registro y al plan.
- §3: el registro en la estructura; `10_Propuesta/` histórica.
- §4: la regla del registro y el plan, y el lenguaje R.
- §5.6 y §6 alineados con el pre-registro y el plan nuevo.
- §11 marcada como histórica.
- §12: se descartó el rendimiento escolar en 2000.
- Las referencias a la propuesta pasan al archivo de hallazgos de los
  artículos.

### `01_Datos/CLAUDE.md`

§9: aprobadas las preguntas S §11 que aplican a la estatura (1-6, 10-13, 15,
17), con remisión al registro. Ajustes frente a la recomendación de
`10_Propuesta/02` §5: mediana de todas las calidades y cambio proporcional (no
Δlog), y comprador neto binario (no tres categorías).

### `07_Recursos/Articulos/00_hallazgos_articulos.md`

Se agregaron el cuadro A5 (retraso en talla) y las definiciones de E-Q.

### `README.md`

Se agregaron las ampliaciones de `grf`.

## Resultados nuevos

No hay tablas ni figuras en `03_Resultados/`. Hubo dos conteos exploratorios con
los microdatos, fuera del pipeline: scripts en el directorio temporal de la
sesión, `conteo_2000.R` y `conteo_ek.R`, no versionados. Muestra común:
miembros del hogar en 1997 (`ptrack$member97 = 1`) con `commid97` válido,
unidos por `pidlink` y `hhid97`.

- **Estatura:** 3.851 niños de 0-5 años en 1997 → 3.369 con `commid97` → 3.219
  en un hogar en 2000 → **2.668 con talla válida (`us04x = 1`) en 1997 y
  2000, en 307 comunidades**. Descriptivo; es la muestra potencial de ΔHAZ, antes
  de limpiar el HAZ.
- **Rendimiento (descartado):** de la cohorte de 7-11 años en 1997, 2.904
  completaron la prueba EK de 2000 (casi todos en la versión de 7-14) en 308
  comunidades, y 2.112 tienen además las pruebas de 1997. Los conteos de nivel
  educativo con `ar16`/`ar18c` usaron códigos sin cotejar con el codebook.

## Pendientes

- **Contar al equipo** las decisiones del 20-nov, tomadas por Santiago (P0.3).
- **P1.1** `01_tracks` y **P1.2** `02_precio_arroz`, con la decisión de los
  terciles.
- **Verificar:** el valor de la línea de Widyanti; las variables de `b1_ks1`;
  cómo trata `grf` los empates en el RATE; la página de Yadlowsky et al. (2025);
  la "edad crítica" de E-Q.
- `Claude outputs/` sigue sin versionar desde antes de esta sesión. No se tocó.
