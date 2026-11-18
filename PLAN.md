# PLAN: plan de implementación del proyecto final

Hoja de ruta desde la infraestructura hasta la entrega. Cada tarea es una
casilla `Pk.n`: se marca `[x]` en la misma sesión en que se termina.
`HANDOFF.md` deriva sus "Siguientes objetivos" de las primeras casillas sin
marcar y las cita por número. El cómo de cada paso está en `10_Propuesta/`
(sobre todo `02` §5-6, `03` y `04`) y en `01_Datos/CLAUDE.md`; este plan los cita,
no los repite. Armado el 18-nov-2026 con los pendientes del `CLAUDE.md` del 17-nov.

**Fechas:** asesoría en la semana 15 (agendar; documento por correo la noche
anterior) y presentación y entrega en la semana 16 (miércoles, 11:59 pm).
Fechas exactas por confirmar.

**Responsables:** el equipo llena la columna "Resp." de cada hito.

| Hito | Contenido | Resp. |
|---|---|---|
| H0 | Infraestructura del repositorio | Santiago |
| H1 | Decisiones del equipo antes de construir | Equipo |
| H2 | Construcción de las bases (scripts 01-05) | |
| H3 | Asesoría de la semana 15 | |
| H4 | ATE y validación (etapas 1-3) | |
| H5 | Heterogeneidad y focalización (etapas 4-6) | |
| H6 | Presentación | |
| H7 | Entrega reproducible | |
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

## H1. Decisiones del equipo (antes de construir)

- [ ] **P1.1** Confirmar el cliente (recomendación: agencia tipo PMA).
- [ ] **P1.2** Declarar el resultado primario antes de ver resultados
  (recomendación: escolaridad 2014; ancla ΔHAZ 1997-2000).
- [ ] **P1.3** Confirmar que salud mental es extensión, el alcance mínimo y el
  orden de recorte.
- [ ] **P1.4** Decidir el lenguaje del pipeline (R para todo con `haven`, o
  Python solo para construir bases) y registrar `haven` como ampliación.
- [ ] **P1.5** Aprobar las recomendaciones de datos de `10_Propuesta/02` §5
  (unidad `commid97`, dos construcciones del precio, sin pesos, posición neta
  desde `b1_ks1`, cohorte no expuesta 22-30) y registrarlas en
  `01_Datos/CLAUDE.md` §9.
- [ ] **P1.6** Pre-registrar por escrito las hipótesis H1-H9
  (`10_Propuesta/04` §4) con fecha, antes de correr el bosque.

## H2. Construcción de las bases

Orden de `10_Propuesta/02` §6. Cada script deja su base en `01_Datos/02_Procesados/`
o `03_Listos/`, reporta observaciones perdidas y se agrega a `00_main.R`.

- [ ] **P2.1** `01_tracks`: `htrack`/`ptrack` 1997-2014, `commid97`, cohortes
  (0-5 y 5-21 en 1997; no expuesta 22-30) y desgaste por ola.
- [ ] **P2.2** `02_precio_arroz`: precios de 1993, 1997 y 2000 por comunidad
  (PKK, mercado, posyandu), unidades y calidades, las dos construcciones, Δlog y
  terciles; marcar las comunidades levantadas en 1998. Figura de la distribución
  del tratamiento.
- [ ] **P2.3** `03_x_1997`: roster, educación de los padres, posición neta en
  arroz (`b1_ks1`), gasto per cápita de 1997, oro y tierra, composición del hogar,
  choques; indicadores de humo y sequía de 1997.
- [ ] **P2.4** `04_haz_9700`: antropometría y HAZ OMS 1997 y 2000 (cohorte 0-5).
- [ ] **P2.5** `05_escolaridad_2014`: años completados en 2014 (tabla nivel →
  años) y media de la cohorte no expuesta por comunidad y sexo.
- [ ] **P2.6** (Si hay tiempo) `06_cognicion`: confirmar en el libro EK qué
  pruebas tomó cada edad en 2007 y 2014 y construir el puntaje EK2 de 2014.

## H3. Asesoría de la semana 15

- [ ] **P3.1** Agendar el turno de la asesoría.
- [ ] **P3.2** Pruebas 1-5 de `10_Propuesta/03`: varianza del precio dentro de
  provincia, balance por tercil, traslape, tendencias previas 1993-97,
  Yamauchi-Larson.
- [ ] **P3.3** Documento o presentación preliminar (pregunta y cliente; datos;
  avances; dudas) en `04_Presentaciones/`, enviado por correo la noche anterior.

## H4. ATE y validación (etapas 1-3)

- [ ] **P4.1** Replicación: ΔHAZ 1997-2000 con EF individuales, cluster
  `commid97`, Lasso de doble selección; comparar con β ≈ −0,135 de E-Q.
- [ ] **P4.2** Resultado primario: escolaridad 2014, diseño C (cohorte expuesta
  vs. no expuesta × intensidad), con terciles y Δlog continuo.
- [ ] **P4.3** Validación: placebos (cohortes > 25 años; 12-17), hermanos (EF de
  hogar), desgaste por tratamiento, robustez sin Sumatra y Kalimantan.

## H5. Heterogeneidad y focalización (etapas 4-6)

- [ ] **P5.1** Verificar en la versión instalada de `grf`: RATE con dos
  prioridades, `get_scores` con W continuo, honestidad por conglomerado. Registrar
  las ampliaciones.
- [ ] **P5.2** Bosque causal principal (escolaridad, terciles): traslape, ATE,
  `test_calibration`, BLP, GATE de H1-H8 con Holm.
- [ ] **P5.3** Prueba de recuperación de la celda de F-T y bosque placebo en la
  cohorte no expuesta.
- [ ] **P5.4** Focalización: dos mitades de comunidades, RATE/TOC del bosque
  frente a pobre, urbano y comprador neto; perfil de los hogares priorizados.
- [ ] **P5.5** (Secundario) Mismo flujo para ΔHAZ, estatura adulta y cognición.

## H6. Presentación

- [ ] **P6.1** Guion "conclusión primero, una idea por lámina" en
  `04_Presentaciones/guion.md`, con la figura o tabla de `03_Resultados/` de cada
  lámina y quién la expone (20 min + 5 de preguntas).
- [ ] **P6.2** Láminas con los archivos exportados, sin retoques; preparación de
  preguntas sobre identificación, `clusters` y limitaciones.

## H7. Entrega reproducible

- [ ] **P7.1** Corrida completa de `00_main.R` desde cero (borrando
  `03_Resultados/` y `01_Datos/02_Procesados/`, `03_Listos/`) sin errores.
- [ ] **P7.2** README con el mapa completo script → tablas/figuras e
  instrucciones de descarga; registro de ampliaciones.
- [ ] **P7.3** `.zip` sin datos (código, README, instrucciones) y presentación en
  `08_Entregables/`; conversaciones unidas por aparte.

## HL. Literatura y verificación (en paralelo)

- [ ] **PL.1** Buscar en Google Scholar si ya existe un ATE del precio del arroz
  sobre escolaridad o cognición, o CATEs con bosques causales para este choque.
- [ ] **PL.2** Revisar el apéndice en línea de Elmira y Qaim (cuadros A1-A7).
- [ ] **PL.3** Leer el texto completo de Tsaneva (2017), Irhamni (2017),
  Wediawaty (2014) y Menéndez y Gignoux (2012).
- [ ] **PL.4** Confirmar los códigos 51 y 52 de `ar10`/`ar11` (IFLS1, Libro K).
- [ ] **PL.5** Insertar en `01_Datos/01_Crudos/IFLS5/00_guia_IFLS5.md` §5 el
  catálogo de `IFLS5/_revision/_cat.md` (marcador `<<CATALOGO>>`).
- [ ] **PL.6** Completar en `01_Datos/README.md` las citas de los informes de
  campo de IFLS2, IFLS3 e IFLS4.
