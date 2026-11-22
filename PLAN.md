# PLAN: lo que falta por ejecutar

Rehecho el 20-nov-2026 a partir de `registro_decisiones.md`. Cada tarea es una
casilla `Pk.n` que se marca `[x]` en la sesión en que se termina. Cuando una
tarea fija algo (una definición, un corte, una variable), eso pasa a
`registro_decisiones.md` **al completarse**, no antes. `HANDOFF.md` toma sus
"Siguientes objetivos" de las primeras casillas sin marcar. `10_Propuesta/` es
histórica y ya no se consulta.

**Fechas:** asesoría en la semana 15 (documento por correo la noche anterior);
presentación y entrega en la semana 16 (miércoles, 11:59 pm). Por confirmar.

## Lo hecho hasta el 20-nov

- **Repositorio** con la estructura de los talleres, `00_main.R`, skills y una
  rama por integrante (18-nov).
- **Datos:** las cinco olas de la IFLS revisadas, con una guía por ola y una
  síntesis (`01_Datos/`).
- **Artículo de referencia:** Elmira y Qaim (2026) y su suplemento, cotejados
  con el PDF: la ecuación, los controles del cuadro A1, las cinco interacciones
  (cuadros A4-A5) y errores sin agrupar.
- **Decisiones** en `registro_decisiones.md`: lenguaje, tres preguntas,
  identificación, precio, muestra, controles, modificadores, Holm y AUTOC.
- **Pre-registro** de subgrupos y familias de Holm en
  `10_Propuesta/07_preregistro_heterogeneidad.md` (fijado antes de construir
  nada).
- **Conteo exploratorio** (fuera del pipeline): 2.668 niños de 0-5 años en 1997
  con `commid97` y talla en 1997 y 2000, en 307 comunidades.
- **Aún no se ha construido el precio ni se ha corrido ninguna estimación.**

## H0. Equipo

- [X] **P0.1** Cada integrante clona el repositorio, pone los datos de RAND en
  `01_Datos/01_Crudos/`, crea su rama y confirma que `00_main.R` pasa la
  verificación de datos.
- [X] **P0.2** Confirmar que quien toque los datos esté registrado en RAND.
- [X] **P0.3** Contar al equipo lo registrado el 20-nov y recoger objeciones
  antes de H2.

## H1. Bases

Cada script deja su base en `01_Datos/02_Procesados/` o `03_Listos/`, imprime las
observaciones que pierde y se agrega a `00_main.R` y al README.

- [x] **P1.1** `01_tracks`: seguimiento 1993-2000 desde `htrack`/`ptrack`,
  `commid97`, cohorte de 0-5 años en 1997 y cohorte de 0-5 en 1993 (placebo).
  Desgaste por ola.
- [x] **P1.2** `02_precio_arroz`: precio por comunidad en 1997 y 2000 con el
  registro §4. Dosis, cuartiles y terciles. Marcar las 38 comunidades con precio
  levantado en 1998. Figura de la distribución del alza.
  - **Decidir con los datos:** terciles nacionales o dentro de provincia, según
    cuánta variación del alza hay dentro de provincia. Luego, al registro.
- [x] **P1.3** `03_x_1997`: controles de E-Q sin los programas, comprador neto,
  gasto per cápita y pobreza, educación de la madre, urbano, sexo, edad e
  indicador de entrevista en 1998.
  - **Decidir:** el valor de la línea de Widyanti et al. (2009) o, si no se
    consigue, el cuartil inferior. Luego, al registro.
- [x] **P1.4** `04_haz`: HAZ de 1997 y 2000 (cohorte principal) y de 1993 y 1997
  (placebo) con el registro §5. Registrar `anthro`/`anthroplus` como
  ampliaciones al crear el script.
- [x] **P1.5** Base lista para estimar (un niño por fila: ΔHAZ, tratamiento, X de
  1997, `commid97`, provincia) y tabla de desgaste según el alza.
- [x] **P1.6** Antes de H2, revisar la base (de la sesión del 20-nov (4)):
  (a) por qué falta más el HAZ de 1997 en el cuartil de mayor alza (no medido,
  sin fecha de nacimiento o fuera de ±6; relación con las comunidades con campo
  en 1998; X de 1997 de los niños con y sin HAZ, según el alza), con una tabla en
  `03_Resultados/Tablas/05_base/`; (b) la cola del ΔHAZ (110 niños con
  |ΔHAZ| > 3), para que el equipo decida si se deja o se recorta, y registrarlo.

**En paralelo a P1.2:** escribir los scripts de H2-H4 sobre datos simulados, para
que solo haya que cambiar la base.

## H2. Pregunta 1: ¿dolió?

- [x] **P2.1** ATE con `feols`, dosis, primeras diferencias y
  `cluster = ~commid97`. Tabla de especificaciones:

  1. sin controles;
  2. con los controles del registro;
  3. más EF de provincia;
  4. más el log del precio de 1997.

  Al lado, errores robustos sin agrupar (los de E-Q) y la pendiente promedio del
  bosque causal como fila de robustez. β en HAZ por +100 % y en cm, con n de
  niños y de comunidades.
- [x] **P2.2** Forma: `feols` con cuartiles (Q2-Q4 frente a Q1). Figura de los
  coeficientes con la recta de E-Q encima.
- [x] **P2.3** Validación: placebo (ΔHAZ 1993→1997 de la cohorte de 1993 sobre el
  alza 1997→2000, debe dar ≈ 0), desgaste según el alza, sin las comunidades de
  1998, con pesos, sin winsorizar y sin los niños con |ΔHAZ| > 3 (`dhaz_mayor_3`).

## H3. Pregunta 2: ¿a quién?

- [x] **P3.1** Réplica de las cinco interacciones de E-Q con `feols` y la dosis,
  una a la vez, con errores robustos y agrupados; p sin ajustar y Holm (F2).
- [x] **P3.2** Bosque principal con terciles: `clusters = commid97`,
  `seed = 2026`, `num.threads` fijo. Revisar el traslape (`W.hat`) y el ATE.
- [x] **P3.3** Seis GATE con `get_scores`; contrastes con
  `feols(Γ ~ X, cluster = ~commid97)` y Holm (F1). BLP descriptiva con las seis
  variables.

## H4. Pregunta 3: ¿el bosque supera a las reglas simples?

- [x] **P4.1** `test_calibration` del bosque.
- [x] **P4.2** RATE con AUTOC en dos mitades de comunidades: bosque (−τ̂) frente a
  pobre, urbano y comprador neto; diferencias con Holm (F3).
- [x] **P4.3** Perfil de los niños que prioriza el bosque (X de 1997 por cuartil
  de τ̂). Si el bosque no supera a las reglas, preparar la lámina del nulo.

## H5. Asesoría (semana 15)

- [ ] **P5.1** Agendar el turno.
- [ ] **P5.2** Documento preliminar en `04_Presentaciones/`: pregunta y cliente,
  datos, avances (idealmente H2) y dudas. Enviarlo la noche anterior.

## H6. Presentación (semana 16)

- [ ] **P6.1** Guion en `04_Presentaciones/guion.md` con el arco de las tres
  preguntas (20 min + 5 de preguntas) y quién expone cada parte.
- [ ] **P6.2** Láminas con las figuras y tablas exportadas, sin retoques.
  Preparar preguntas: por qué `feols` y no el bosque para el ATE, contraste
  frente a crisis, errores agrupados, desgaste, diferencia con Frankenberg y
  Thomas (2017).

## H7. Entrega

- [ ] **P7.1** `00_main.R` corre desde cero (borrando `03_Resultados/`,
  `02_Procesados/` y `03_Listos/`) sin errores.
- [ ] **P7.2** README con el mapa script → resultados, instrucciones de descarga,
  citas de los informes de campo de la IFLS y ampliaciones.
- [ ] **P7.3** `.zip` sin datos y presentación en `08_Entregables/`.

## Por verificar antes de usar

- ~~Cómo trata `rank_average_treatment_effect` los empates de una regla binaria y
  si da la diferencia entre dos prioridades con EE emparejado (P4.2).~~
  **Resuelto (22-nov, Samuel, en el código de `grf` 2.6.1):** solo acepta W
  binario; los empates se promedian dentro de cada grupo (las reglas binarias
  son válidas); con dos prioridades devuelve las dos RATE y su diferencia con
  bootstrap emparejado y agrupado por los clusters del bosque.
- Que la "edad crítica" de E-Q sea 0-2 años (se infiere de su fig. 5).
- La página de Yadlowsky et al. (2025) sobre AUTOC frente a QINI.
