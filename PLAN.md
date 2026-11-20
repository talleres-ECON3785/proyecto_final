# PLAN: plan de implementación del proyecto final

Hoja de ruta desde la infraestructura hasta la entrega. Cada tarea es una
casilla `Pk.n`: se marca `[x]` en la misma sesión en que se termina.
`HANDOFF.md` deriva sus "Siguientes objetivos" de las primeras casillas sin
marcar y las cita por número. El cómo de cada paso está en `10_Propuesta/`
(sobre todo `02` §5-6, `03` y `04`) y en `01_Datos/CLAUDE.md`; este plan los cita,
no los repite. Armado el 18-nov-2026; **reorganizado el 20-nov-2026** con los
objetivos del equipo, la discusión sobre la identificación y la evaluación de la
propuesta de trabajo con un consejo de cinco asesores y revisión cruzada.

**Fechas:** asesoría en la semana 15 (agendar; documento por correo la noche
anterior) y presentación y entrega en la semana 16 (miércoles, 11:59 pm).
Fechas exactas por confirmar.

## Alcance y arco de la presentación (20-nov-2026)

**Solo estatura:** ΔHAZ 1997→2000 de los niños de 0-5 años en 1997. El equipo
descartó por ahora la escolaridad (y con ella la celda de 8 años de F-T), la
cognición, la salud mental y la estatura adulta. Frankenberg y Thomas (2017)
siguen siendo el contrapunto: con la zona urbana como exposición, no encuentran
daño en la talla.

La presentación responde tres preguntas, cada una con su herramienta:

| # | Pregunta | Herramienta principal | Papel del bosque causal |
|---|---|---|---|
| 1 | **¿Dolió?** Replicar el ATE de E-Q (−0,135 HAZ por +100 %) y ver su forma | `feols` (dosis continua y cuartiles) | Solo una fila de robustez |
| 2 | **¿A quién?** Subgrupos pre-declarados: edad, urbano, educación de la madre, sexo, comprador neto, pobreza | GATE con puntajes AIPW del bosque y Holm; BLP | Central |
| 3 | **¿El bosque supera a las reglas simples?** | Bosque con terciles: calibración, RATE/TOC frente a pobre, urbano y comprador neto; perfil de los priorizados | Central (entregable al cliente) |

**Recorte si falta tiempo:** se conservan las preguntas 1 y 2; la 3 queda como
exploratoria. Se prepara desde el principio la lámina del nulo: "no hay
evidencia de heterogeneidad más allá de las reglas simples". Para el cliente
es un resultado útil.

**Lo que no se usa y por qué:**

- **El bosque para replicar el ATE.** Estima la pendiente promedio, que pondera
  distinto que el MCO de E-Q. Si no da −0,135, no se sabría si la diferencia
  viene del estimador, del precio o de la muestra.
- **El bosque para la no linealidad.** `causal_forest` supone un efecto lineal en
  W dado x, así que no puede mostrar la forma de la dosis-respuesta.
- **El árbol causal individual.** Lo retiró el equipo el 18-nov (`CLAUDE.md` §11).
  Un `rpart` descriptivo sobre los τ̂ no se recomienda; el perfil de los
  priorizados va en una tabla.

| Hito | Contenido | Resp. |
|---|---|---|
| H0 | Infraestructura del repositorio | Santiago |
| H1 | Identificación y decisiones previas | Equipo |
| H2 | Construcción de las bases | |
| H3 | Asesoría de la semana 15 | |
| H4 | Pregunta 1: ¿dolió? (ATE y no linealidad) | |
| H5 | Pregunta 2: ¿a quién? (GATE pre-declarados) | |
| H6 | Pregunta 3: ¿el bosque supera a las reglas simples? | |
| H7 | Presentación | |
| H8 | Entrega reproducible | |
| HL | Literatura y verificación (en paralelo) | |

---

## H0. Infraestructura

- [x] **P0.1** Estructura de carpetas de los talleres, `CLAUDE.md` raíz,
  `01_Datos/CLAUDE.md`, `HANDOFF.md`, `PLAN.md`, README, `.gitignore` que excluye
  los datos, `00_main.R` y skills (18-nov).
- [x] **P0.2** Commit inicial en `main` y push a GitHub (18-nov).
- [ ] **P0.3** Cada integrante clona el repositorio, copia o descarga los datos de
  RAND en `01_Datos/01_Crudos/` (`01_Datos/README.md`), crea su rama y confirma
  que `00_main.R` pasa la verificación de datos. Confirmar el equipo y las ramas
  de `CLAUDE.md` §4.2 y §10.
- [ ] **P0.4** Verificar que cada integrante que toque los datos esté registrado
  en RAND.

## H1. Identificación y decisiones previas

### Cómo asignan E-Q tratados y controles (cotejado con el PDF el 20-nov)

- **No hay grupo de control:** el tratamiento es una dosis continua por
  comunidad, `C_j` = cambio **proporcional** del precio del arroz 1997→2000
  (1 = +100 %; p. 5), no Δlog. Media 0,83, DE 0,67, mín −0,17, **máx 7,29**, sin
  indicios de recorte (cuadro 1, p. 4; 2.112 niños).
- **Precio:** promedio por comunidad de todas las calidades y fuentes (mercados,
  tiendas y grupos comunitarios de mujeres), en Rp/kg (p. 3). Hay una versión
  nominal (la principal) y una real (IPC Laspeyres sin arroz; apéndice A1, que no
  tenemos).
- **Ecuación 1** (p. 3): `HAZ_it = β1 (C_j × T_t) + γ (X'_1997 × T_t) + λ_i + T_t`.
  Con dos olas equivale a regresar ΔHAZ sobre `C_j` y X de 1997. HAZ con
  estándares OMS (p. 2).
- **Para replicar:** en 2000 el libro PKK no trae precios, así que el promedio de
  E-Q cambia de fuentes entre años. Ni el artículo ni el suplemento dicen qué
  usaron en 2000 (PL.3 abierta). La cola de +729 % puede mover β.
- **Del suplemento** (leído el 20-nov; detalle en
  `07_Recursos/Articulos/00_hallazgos_articulos.md` §1):
  - errores robustos, **sin agrupar por comunidad**;
  - lista completa de controles del cuadro A1, que incluye cinco programas de la
    red de seguridad social (desde 1998), probablemente posteriores al
    tratamiento;
  - 3.338 observaciones de HAZ, frente a los 2.112 niños del cuadro 1 (sin
    explicar);
  - deflactor por hogar con el IPC mensual del BPS, que no viene en la IFLS.

### Construcción del precio (registrada el 20-nov)

- **Fuentes:** el tratamiento principal usa solo las fuentes presentes en 1997 y
  en 2000, el posyandu (`pos_h`) y tiendas y mercados (`bk2_hpj`). Así el cambio
  no mezcla el alza con el cambio de fuentes. El PKK de 1997 entra solo en T1.
- **Escala:** cambio proporcional `(P2000 − P1997) / P1997` (1 = +100 %), como
  E-Q (p. 5); no Δlog ni diferencia en Rp.
- **Nominal:** con un deflactor común, el cambio real es una transformación
  lineal del nominal (β_real ≈ β_nominal × D), así que no cambia la variación
  entre comunidades que identifica β. El deflactor de E-Q queda como extensión
  opcional (exige conseguir el IPC del BPS).
- **Diagnóstico** dentro de `02_precio_arroz`: en 1997, comparar PKK y posyandu
  en las mismas comunidades (nivel y correlación). No decide la construcción;
  sirve para explicar en la sustentación una eventual diferencia entre T1 y T2.

### Tratamiento: cuatro versiones

Todas se asignan por la comunidad de 1997 (`commid97`). La unidad de
observación es el niño y los errores se agrupan por comunidad.

| Versión | Definición | Uso |
|---|---|---|
| **T1. Réplica E-Q (aproximada)** | Cambio proporcional nominal, promedio de todas las fuentes y calidades de cada año (PKK + posyandu + `bk2_hpj` en 1997; posyandu + `bk2_hpj` en 2000) | Comparar con −0,135; se declara aproximada |
| **T2. Dosis limpia (principal)** | Cambio proporcional nominal, solo con fuentes presentes en 1997 y 2000 (posyandu + `bk2_hpj`), calidad media, kg, mediana por comunidad, winsorizado en p1/p99 (`02` §5.3) | β sin el artefacto de fuentes ni la cola |
| **T3. Cuartiles de T2** | Q2, Q3 y Q4 frente a Q1 | Forma de la respuesta: lineal, umbral o saturación |
| **T4. Terciles de T2** | Tercil alto = 1, bajo = 0, sin el medio (~208 comunidades) | Bosque: calibración, GATE, RATE |

**Pendiente de los datos:** que los terciles de T4 sean nacionales o dentro de
provincia lo decide la prueba 1 (varianza del alza dentro y entre provincias).
Con terciles nacionales, poner la provincia en X puede pegar `W.hat` a 0 o 1, y
quitarla deja la confusión regional sin controlar. Si hay variación suficiente
dentro de provincia, esos terciles son los principales.

**Otras versiones discutidas y descartadas como principales:**

- **Otros cortes (40/40, 50/50, 75/25):** quedan solo para robustez.
- **Exposición del hogar** (alza × proporción comprada): queda como modificador
  (comprador neto).
- **Zona urbana como exposición** (la de F-T): queda como modificador.
- **Choque autorreportado:** endógeno.

### Supuesto de identificación y amenazas

Se compara a cada niño consigo mismo (ΔHAZ) entre comunidades con más alza y con
menos. El supuesto es que, sin esa diferencia de alza y dadas sus X de 1997,
ambos grupos habrían cambiado igual. Con la dosis continua (T1, T2) se necesita
además la versión fuerte del supuesto (Callaway, Goodman-Bacon y Sant'Anna); con
T3 y T4 no. **Lo que se identifica es el efecto de más alza frente a menos alza,
no el de la crisis frente a no tener crisis.**

| Amenaza | Defensa |
|---|---|
| Choques regionales (sequía de El Niño, humo) | EF de provincia o terciles dentro de provincia; sin Sumatra ni Kalimantan; errores agrupados por provincia como robustez |
| Alza confundida con lo urbano | Controlar la zona; lo urbano además es un GATE |
| El HAZ cambia solo con la edad (cae entre 0 y 24 meses) | Edad en 1997 flexible (dummies por año o spline en meses) |
| Regresión a la media | El HAZ de 1997 **no** se usa como modificador; como control, solo en robustez |
| Reversión a la media del precio | Controlar el log del precio de 1997 |
| Desgaste y mortalidad 1997→2000 | Tabla de desgaste según el alza; el tratamiento sigue la residencia de 1997 |
| Línea base contaminada | Indicador y robustez sin las 27 comunidades con precio de 1998 ni los niños medidos en 1998 |
| Medición del HAZ (estándar OMS 2006 hasta los 60 meses y referencia 2007 después; longitud acostado y talla de pie) | `anthro` y `anthroplus`, con la convención declarada e igual a la de E-Q |

### Hechos verificados en `grf` 2.6.1 (código y documentación, 20-nov)

- **`causal_forest` con W continuo** estima τ(x) = Cov[Y,W|X=x]/Var[W|X=x], una
  pendiente local lineal en W. `average_treatment_effect` da la pendiente
  promedio (solo `target.sample = "all"` u `"overlap"`). `test_calibration`,
  `best_linear_projection` y `get_scores` funcionan con W continuo.
- **RATE:** `rank_average_treatment_effect(forest, …)` solo acepta W binario.
  `rank_average_treatment_effect.fit(DR.scores, priorities, clusters)` acepta
  cualquier puntaje AIPW, por ejemplo de `multi_arm_causal_forest`, con un RATE
  por contraste. Con puntajes de pendiente continua corre, pero su validez no
  está documentada.
- **`lm_forest`** solo tiene `predict` con varianza: no trae ATE, `get_scores`,
  RATE, BLP ni calibración. Ni `lm_forest` ni `multi_arm_causal_forest` están en
  el catálogo del curso.
- **`clusters = commid97`** entrena y evalúa con comunidades completas.
  `equalize.cluster.weights = FALSE` (cada niño pesa igual) en lo principal y
  `TRUE` como robustez.
- **Simulación con datos inventados** (3.000 niños, 250 comunidades,
  heterogeneidad grande): los GATE pre-declarados y la BLP recuperaron el patrón,
  pero `test_calibration` no lo detectó (p = 0,48) y el orden por τ̂ no fue
  monótono. Con este número de comunidades, preguntar por grupos definidos de
  antemano tiene mucha más potencia que pedirle al bosque que los encuentre.

### Tareas

- [ ] **P1.1** Registrar en "Decisiones tomadas" de `CLAUDE.md` las versiones
  T1-T4 y el tercil (33/33) para el bosque. La elección entre terciles
  nacionales y dentro de provincia se cierra con la prueba 1 (P2.2).
- [x] **P1.2** Registrar el nuevo alcance (solo estatura, arco de tres
  preguntas, sin escolaridad, cognición ni salud mental) en `CLAUDE.md` §1, §5,
  §6 y §11-12 y en `10_Propuesta/00_resumen.md` (v5); mover lo reemplazado a
  `_obsoleto/` (20-nov). Falta actualizar `10_Propuesta/03` y `04` (P1.6).
- [ ] **P1.3** Pre-registrar por escrito, con fecha, los GATE de la pregunta 2,
  con la edad en 1997 primero (H5: más daño a los 3-5 años), y después urbano,
  educación de la madre, sexo, comprador neto y pobreza. Fijar también la
  familia de Holm y la métrica de RATE (AUTOC o QINI) antes de correr el bosque.
  Registrar como ampliaciones `get_scores`, `best_linear_projection` y, si se
  usa, `fwildclusterboot`.
- [ ] **P1.4** Decidir el lenguaje del pipeline (R para todo con `haven`, o
  Python solo para construir bases) y registrar `haven` como ampliación.
- [ ] **P1.5** Aprobar las recomendaciones de datos de `10_Propuesta/02` §5 y
  registrarlas en `01_Datos/CLAUDE.md` §9.
- [ ] **P1.6** Actualizar `10_Propuesta/03` y `04` al alcance de solo estatura
  (hoy tratan la escolaridad como resultado primario).

## H2. Construcción de las bases

Cada script deja su base en `01_Datos/02_Procesados/` o `03_Listos/`, reporta
las observaciones perdidas y se agrega a `00_main.R`. **P2.2 bloquea todo lo
demás:** dos integrantes en la semana 1.

- [ ] **P2.1** `01_tracks`: `htrack`/`ptrack` 1993-2000, `commid97`, cohortes (0-5
  años en 1997; 0-5 en 1993 para el placebo) y desgaste por ola.
- [ ] **P2.2** `02_precio_arroz`: precios de 1997 y 2000 por comunidad (y de 1993
  para el placebo), unidades y calidades, y **T1-T4** (construcción en H1).
  Marcar las 27 comunidades levantadas en 1998. Prueba 1 (varianza dentro y
  entre provincias), diagnóstico PKK frente a posyandu en 1997 y figura de la
  distribución del alza.
- [ ] **P2.3** `03_x_1997`: roster, educación de los padres, línea de pobreza de
  los noventa (Widyanti et al. 2009, según E-Q p. 4), posición neta en arroz
  (`b1_ks1`), gasto per cápita, oro y tierra, composición del hogar e indicadores
  de humo y sequía de 1997.
- [ ] **P2.4** `04_haz`: antropometría y HAZ OMS de 1997 y 2000 (cohorte 0-5) y de
  1993 y 1997 (cohorte del placebo), con edad en meses. Tabla de desgaste según
  el alza.
- [ ] **P2.5** (Opcional) `05_simulacion_potencia`: con los N reales y la
  distribución real del alza, pero con **resultados simulados**, ver qué
  heterogeneidad detectan los GATE, la calibración y RATE. Sirve como argumento
  ante el profesor.

**En paralelo a P2.2:** un integrante escribe los scripts de `feols` (H4) y otro
el del bosque (H5-H6) sobre datos simulados, para que solo haya que cambiar la
base cuando exista el precio.

## H3. Asesoría de la semana 15

- [ ] **P3.1** Agendar el turno de la asesoría.
- [ ] **P3.2** Llevar la réplica (P4.1-P4.2), la figura de cuartiles (P4.3), la
  prueba 1 y el balance y desgaste por tercil.
- [ ] **P3.3** Documento o presentación preliminar (pregunta y cliente; datos;
  avances; dudas) en `04_Presentaciones/`, enviado por correo la noche anterior.
  **Acordar con el profesor si el bosque (pregunta 3) es núcleo o exploratorio.**

## H4. Pregunta 1: ¿dolió? (ATE y no linealidad)

- [ ] **P4.1** Réplica con `feols` en las dos formas, para mostrar que son
  equivalentes: el panel `haz ~ alza:post + x97:post | pidlink + post` y las
  primeras diferencias `d_haz ~ alza + x97`, con `cluster = ~commid97`. Con T1 y
  con T2.
- [ ] **P4.2** Tabla de especificaciones (T1 y T2 lado a lado): (1) sin controles;
  (2a) controles completos de E-Q (cuadro A1 del suplemento, con los programas
  de la red de seguridad social), solo como réplica; (2b) controles de E-Q sin
  esos programas (principal, sin controles posteriores al tratamiento); (3) más
  EF de provincia o provincia × zona; (4) más el log del precio de 1997; (5)
  Lasso de doble selección (`glmnet`); (6) pendiente promedio de
  `causal_forest` continuo como robustez. β con su escala (HAZ por +100 %),
  traducido a cm, con n de niños y de comunidades. En la columna de réplica,
  errores robustos (los de E-Q) y agrupados por `commid97`, uno al lado del otro.
- [ ] **P4.3** No linealidad: `feols` con `i(cuartil_alza, ref = 1)` (T3) y un
  spline de la dosis como robustez. Figura de los coeficientes contra el alza
  media de cada cuartil, con la recta de E-Q encima.
- [ ] **P4.4** Puente hacia el bosque: el mismo `feols` con T4 (alto frente a
  bajo).
- [ ] **P4.5** Validación:
  - placebo de tendencias previas: ΔHAZ 1993→1997 de la cohorte de 0-5 años en
    1993, sobre el alza 1997→2000 (debe dar ≈ 0);
  - balance de Yamauchi-Larson;
  - desgaste según el alza;
  - robusteces: sin Sumatra ni Kalimantan, sin las comunidades de 1998, con y sin
    winsorizar, y con errores agrupados por provincia (13, con bootstrap salvaje;
    `fwildclusterboot` sería una ampliación).

## H5. Pregunta 2: ¿a quién? (GATE pre-declarados)

- [ ] **P5.1** Bosque principal con T4, `clusters = commid97`, `seed = 2026` y
  `num.threads` fijo. Revisar el traslape (`W.hat`) y el ATE, y compararlo con
  P4.4.
- [ ] **P5.2** GATE de P1.3 con `get_scores` y `average_treatment_effect(subset =
  …)`, con Holm, empezando por la edad. Comparar en signo y orden con la fig. 5
  de E-Q (urbano, madre con primaria o menos, varones, pobres). BLP sobre las
  mismas variables.

## H6. Pregunta 3: ¿el bosque supera a las reglas simples?

- [ ] **P6.1** `test_calibration` del bosque principal. Si no rechaza, decir que
  no hay evidencia de heterogeneidad más allá de los GATE y quedarse con ellos.
- [ ] **P6.2** Dos mitades de comunidades (Lab 10): RATE/TOC del τ̂ del bosque
  frente a pobre, urbano y comprador neto (H9), con errores emparejados. Las
  prioridades son −τ̂ (τ < 0 = daño). La TOC se reporta como ganancia relativa
  entre reglas, no como casos evitados (no hay comunidades sin tratar).
- [ ] **P6.3** Perfil de los niños que prioriza el bosque: tabla de las X de 1997
  por cuartil de τ̂, con variables que observa el cliente.

## H7. Presentación

- [ ] **P7.1** Guion en `04_Presentaciones/guion.md` siguiendo el arco: (1)
  ¿dolió?, con la tabla de especificaciones, la figura de cuartiles y la lámina de
  validación; (2) ¿a quién?, con los GATE; (3) ¿el bosque supera a las reglas
  simples?, con calibración, RATE y perfil, o la lámina del nulo. Cada lámina
  responde una pregunta en lenguaje llano y lleva la figura o tabla de
  `03_Resultados/` y quién la expone (20 min + 5 de preguntas).
- [ ] **P7.2** Láminas con los archivos exportados, sin retoques, y preparación de
  preguntas: por qué `feols` y no el bosque para el ATE, contraste frente a
  crisis, `clusters`, desgaste y diferencia con F-T.

## H8. Entrega reproducible

- [ ] **P8.1** Corrida completa de `00_main.R` desde cero (borrando
  `03_Resultados/` y `01_Datos/02_Procesados/`, `03_Listos/`) sin errores.
- [ ] **P8.2** README con el mapa completo script → tablas/figuras, instrucciones
  de descarga y registro de ampliaciones.
- [ ] **P8.3** `.zip` sin datos (código, README, instrucciones) y presentación en
  `08_Entregables/`; conversaciones unidas por aparte.

## HL. Literatura y verificación (en paralelo)

- [ ] **PL.1** Buscar en Google Scholar si ya existen CATEs con bosques causales
  para este choque.
- [x] **PL.2** Revisar el apéndice en línea de E-Q
  (`07_Recursos/Articulos/1-s2.0-S2211912425000756-mmc1.docx`, 20-nov). Trae
  los controles, el deflactor, el cuadro A4 y errores robustos sin agrupar. No
  trae las fuentes del precio de 2000 ni la convención de HAZ. Resumen en
  `07_Recursos/Articulos/00_hallazgos_articulos.md` §1.
- [ ] **PL.3** Confirmar qué fuente es el "grupo comunitario de mujeres" de E-Q
  en 2000, año en que el PKK no trae precios (¿el posyandu?). El suplemento no lo
  dice. Ya no bloquea: T2 no depende de esto y T1 se declara aproximada.
- [ ] **PL.7** Confirmar en qué ola miden E-Q los programas de la red de
  seguridad social que usan como controles, y qué definen como "edad crítica" y
  "pobre" en el cuadro A4 (texto principal).
- [ ] **PL.4** Confirmar los códigos 51 y 52 de `ar10`/`ar11` (IFLS1, Libro K).
- [ ] **PL.5** Insertar en `01_Datos/01_Crudos/IFLS5/00_guia_IFLS5.md` §5 el
  catálogo de `IFLS5/_revision/_cat.md` (marcador `<<CATALOGO>>`).
- [ ] **PL.6** Completar en `01_Datos/README.md` las citas de los informes de
  campo de IFLS2, IFLS3 e IFLS4.

## Qué no está verificado

- Ninguna versión de W se ha construido. La variación del alza dentro de
  provincia (prueba 1), que decide el tipo de terciles, es el supuesto más
  importante sin comprobar.
- No sabemos si E-Q recortan la cola de `C_j` ni qué fuente de precio usan en
  2000. Tampoco por qué el cuadro A1 tiene 3.338 observaciones si el cuadro 1
  describe 2.112 niños.
- Que el cociente −0,251 / −0,135 ≈ 1,86 sea la inflación acumulada 1997-2000
  es una inferencia nuestra, no de E-Q.
- La simulación que sugiere poca potencia para la heterogeneidad usa datos
  inventados y una sola semilla; no es un cálculo de potencia.
- Que exista suficiente cohorte de 0-5 años en 1993 con talla en 1993 y 1997
  para el placebo no se ha comprobado en los datos.
- Que MCO pondere los efectos heterogéneos según la varianza condicional del
  tratamiento se cita de memoria; hay que verificarlo antes de usarlo en la
  presentación.
