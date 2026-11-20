# Bitácora — 2026-11-20: identificación del tratamiento y alcance

## Resumen

Objetivo: definir los objetivos del proyecto y la estrategia de identificación
antes de trabajar con los datos. El equipo había fijado tres objetivos: replicar
el ATE de Elmira y Qaim sobre la estatura, aplicar bosques causales a estatura y
escolaridad para ver si recuperan las interacciones de E-Q y F-T, y buscar CATEs
nuevos con implicaciones de focalización. La sesión empezó por cómo separan E-Q
tratados de controles y qué alternativas permiten los datos.

Desarrollo:

1. **Revisión de E-Q contra el PDF.** No tienen grupo de control: usan una dosis
   continua por comunidad, el cambio **proporcional** del precio 1997→2000 (no
   Δlog), promediando todas las fuentes y calidades.
2. **Alternativas de tratamiento discutidas:**
   - dosis continua y cómo se identifica;
   - terciles, nacionales o dentro de provincia, y otros cortes (40/40, 50/50,
     75/25);
   - cuartiles para estudiar no linealidad;
   - exposición del hogar (posición neta en arroz).
3. **Verificación en el código y la documentación de `grf` 2.6.1,** con
   simulaciones de datos inventados en el directorio temporal de la sesión (no
   entran al pipeline): qué hacen `causal_forest` continuo, `lm_forest`, RATE,
   `multi_arm_causal_forest` y `clusters`.
4. **El equipo descartó la escolaridad;** queda solo estatura.
5. **Evaluación de la propuesta con un consejo** (`llm-council`): cinco asesores
   con perspectivas distintas, revisión cruzada anónima y síntesis. La
   propuesta del usuario tenía tres puntos: (1) ATE de E-Q con bosque continuo;
   (2) bosque binario por terciles para RATE y TOC; (3) no linealidad con
   bosques y después `feols`.
6. **Recomendación consolidada,** registrada en `PLAN.md`, `CLAUDE.md` y
   `10_Propuesta/00_resumen.md` (v5).

**Siguientes objetivos que traía `HANDOFF.md`:**

- (1) P0.3 y P1.1-P1.6: avanzó la parte de decisiones previas. Quedó escrita la
  recomendación de tratamiento y alcance, y se cerró el registro del alcance
  (nueva P1.2). La puesta del equipo en el repositorio (P0.3) no se trabajó.
- (2) P2.1 y (3) P2.2: no se trabajaron.

## Archivos

- **Creados:**
  - `06_Bitacoras/2026-11-20_identificacion-tratamiento-y-alcance.md`
  - `10_Propuesta/00_resumen.md` (v5)
- **Modificados:** `PLAN.md` (reescrito), `CLAUDE.md`, `HANDOFF.md`,
  `.gitignore`.
- **Movidos:** `10_Propuesta/00_resumen.md` (v4) →
  `10_Propuesta/_obsoleto/00_resumen_v4.md`.
- **Fuera de la sesión, sin tocar:**
  - `07_Recursos/Articulos/README.md` (modificado antes);
  - `07_Recursos/Articulos/00_hallazgos_articulos.md` y `Claude outputs/` (sin
    seguimiento desde antes);
  - un archivo nuevo, `07_Recursos/Articulos/1-s2.0-S2211912425000756-mmc1.docx`.
    Por el nombre parece el material suplementario de E-Q, pero no se abrió.

## Detalle por archivo

### `PLAN.md`

Se reorganizó alrededor del alcance y del arco de tres preguntas. Contenido
principal:

- **H1** registra:
  - el método de E-Q (cotejado con el PDF);
  - las cuatro versiones del tratamiento;
  - el supuesto de identificación con su tabla de amenazas y defensas;
  - los hechos verificados de `grf`.
- **Hitos de análisis:** H4 (¿dolió?), H5 (¿a quién?), H6 (¿el bosque supera
  a las reglas simples?).
- **Lo descartado,** con su razón:
  - el bosque para el ATE;
  - el bosque para la no linealidad;
  - el árbol individual (retirado el 18-nov).

Las variables que construyen los estimadores son las siguientes.

**Tratamiento T1, réplica E-Q.**

- *Fuente:* E-Q p. 3 (promedio de calidades y fuentes) y p. 5 (escala
  proporcional, 1 = +100 %); cuadro 1, p. 4 (media 0,83, DE 0,67, mín −0,17,
  máx 7,29).
- *Cálculo:* (precio 2000 − precio 1997) / precio 1997 por `commid97`, nominal.
- *Rol:* el regresor de la ecuación 1 cuyo coeficiente se compara con −0,135.

**Tratamiento T2, dosis limpia (principal).**

- *Fuente:* `10_Propuesta/02` §5.3 y síntesis §7.6 (el PKK no trae precios en
  2000).
- *Cálculo:* lo mismo que T1, pero solo con posyandu + `bk2_hpj`, calidad media,
  kg, winsorizado en p1/p99.
- *Rol:* comprobar que β no depende del cambio de fuentes ni de la cola.

**Tratamiento T3, cuartiles de T2.**

- *Cálculo:* Q2, Q3 y Q4 como indicadores frente a Q1, que es la referencia.
- *Rol:* distinguir una respuesta lineal, con umbral o con saturación (P4.3).

**Tratamiento T4, terciles de T2.**

- *Cálculo:* tercil alto = 1, tercil bajo = 0, sin el tercil medio (~208
  comunidades, `10_Propuesta/04` §5.1).
- *Rol:* el W binario del bosque. Es el único que admite el RATE nativo de
  `grf`.
- *Pendiente:* que los terciles sean nacionales o dentro de provincia lo decide
  la prueba 1.

**Puntajes AIPW** (`get_scores`).

- *Rol:* estimar los GATE pre-declarados y la RATE en una mitad de comunidades
  distinta de la que fija las prioridades. Las prioridades son −τ̂, porque
  τ < 0 es daño.

### `CLAUDE.md`

Actualizado con el nuevo alcance:

- **§1:** nuevo resumen del proyecto en tres preguntas y el tratamiento en
  cuatro versiones.
- **§5:** dos matices.
  - La pendiente promedio del bosque continuo no es el β MCO de E-Q.
  - La potencia para la heterogeneidad es baja.
- **§6:** tabla de etapas rediseñada y reglas nuevas.
  - `W.hat` con terciles nacionales.
  - El bosque continuo supone un efecto lineal en W.
  - RATE nativo solo con W binario.
  - El HAZ de 1997 no se usa como modificador.
- **§11:** tres decisiones.
  - El alcance, que es decisión del equipo.
  - El tratamiento T1-T4.
  - La réplica y la no linealidad con `feols`.

  Las dos últimas quedan marcadas como recomendación por confirmar con el equipo.
- **§12:** lo descartado, con su razón.
  - La escolaridad (con la celda de F-T y el bosque placebo), la cognición, la
    estatura adulta y la salud mental.
  - El bosque para el ATE y para la no linealidad.
  - `lm_forest` y `multi_arm_causal_forest`.

### `10_Propuesta/00_resumen.md` (v5)

Resumen corto con la tabla "qué cambió en la v5", como pide `CLAUDE.md` §4. Los
documentos `01`-`06` siguen en v4: el resumen avisa que se leen con estos
cambios. **No se reescribieron `03` ni `04`.**

### `.gitignore`

Se agregó `07_Recursos/Articulos/*.docx`. El archivo `.docx` nuevo (al parecer,
el suplemento de E-Q) es material con derechos de terceros, en la misma lógica
que la decisión del 18-nov sobre los PDF. Se confirmó con `git check-ignore`
que queda ignorado.

### Hallazgos técnicos de la sesión (verificados, sin resultados del proyecto)

**`grf` 2.6.1** (código y documentación):

- **`causal_forest` con W continuo:**
  - estima τ(x) = Cov[Y,W|X=x]/Var[W|X=x];
  - `average_treatment_effect` da la pendiente promedio (solo
    `target.sample = "all"` u `"overlap"`);
  - `test_calibration`, `best_linear_projection` y `get_scores` funcionan.
- **RATE:**
  - `rank_average_treatment_effect(forest)` rechaza todo W que no sea binario;
  - `rank_average_treatment_effect.fit` acepta puntajes AIPW de cualquier
    origen.
- **`lm_forest`** solo tiene `predict`.

**Simulaciones con datos inventados** (`seed = 2026`, en el directorio temporal
de la sesión):

- `lm_forest` con un solo W y `causal_forest` continuo dieron predicciones con
  correlación de 0,93.
- Con 3.000 niños, 250 comunidades y heterogeneidad grande:
  - los GATE pre-declarados y la BLP recuperaron el patrón;
  - `test_calibration` no lo detectó (p = 0,48);
  - los puntajes por cuartil de τ̂ no fueron monótonos.

Son ilustraciones, no resultados del proyecto ni un cálculo de potencia.

### Evaluación con el consejo

Las cinco revisiones eligieron como respuesta más fuerte la que señalaba errores
técnicos comprobables:

- la pendiente promedio del bosque no es el β MCO;
- el bosque no sirve para estudiar la no linealidad;
- `W.hat` se puede pegar con terciles nacionales;
- el cambio de referencia OMS;
- las tendencias previas no se pueden probar en estos niños.

Como mayor punto ciego, las cinco eligieron la idea de reconciliar E-Q y F-T con
cuartiles de precio, porque F-T miden la exposición por zona urbana. Los puntos
ciegos que detectaron se incorporaron al plan: desgaste selectivo, dinámica del
HAZ por edad, regresión a la media, agrupamiento por provincia y el placebo con
la cohorte de 1993.

**Matices propios sobre el veredicto:**

- Las recomendaciones de sacar la provincia de X y de controlar la confusión
  regional chocan entre sí; la prueba 1 decide.
- La edad (H5) y el placebo con cohortes mayores ya estaban en la propuesta.
- El precio real no es claramente más limpio, y no tenemos el deflactor.
- El cruce de referencias OMS se resuelve declarando la convención.

## Resultados nuevos (tablas, figuras, bases)

No hubo: ninguna estimación ni base derivada.

## Pendientes

- **Confirmar con el equipo** el tratamiento T1-T4 y la réplica con `feols`
  (P1.1), y fijar por escrito los GATE, la familia de Holm y la métrica de RATE
  (P1.3).
- **Registrar como ampliaciones antes de usarlas:** `get_scores`,
  `best_linear_projection` y, si se usa, `fwildclusterboot`.
- **Revisar el `.docx`** que parece el suplemento de E-Q (PL.2): controles,
  deflactor, agrupamiento de errores y convención de HAZ.
- **Actualizar los documentos de la propuesta:** `10_Propuesta/03` y `04` siguen
  hablando de escolaridad como resultado primario.
- **Siguiente paso técnico:** `01_tracks` (P2.1) y `02_precio_arroz` con T1-T4 y
  la prueba 1 (P2.2), que bloquea todo lo demás.
- **Sin confirmar:** el equipo y las ramas (heredado), y que haya suficiente
  cohorte de 1993 para el placebo.
