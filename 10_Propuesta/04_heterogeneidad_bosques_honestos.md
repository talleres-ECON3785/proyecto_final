# 04 · Heterogeneidad con bosques y árboles causales honestos (versión 4)

> Versión 4, 17-nov-2026 (ajuste del 18-nov: se retira el árbol causal). Reemplaza `04_arboles_causales_honestos.md` (v2). Es ahora el **documento central** de la propuesta: qué se sabe sobre quién cargó con el choque, qué no se sabe y cómo lo estimamos con las herramientas del curso (`07_Recursos/herramientas_R_del_curso.md`). Las citas con página se verificaron contra los PDF de `07_Recursos/Articulos/` (ver `01`, §6). Las cifras de datos vienen de `01_Datos/00_sintesis_revision_IFLS.md` (S §x) y de las guías de ola.

## 1. La idea en un párrafo

La literatura coincide en que la crisis de 1998 golpeó de forma **muy desigual**: «devastadora para unos, una oportunidad para otros» (Frankenberg, Smith y Thomas 2003, p. 280). Sin embargo, quién cargó con el daño se ha estudiado siempre con **subgrupos elegidos a mano, una dimensión a la vez**, con medidas de exposición distintas en cada estudio (zona, provincia, gasto, precio) y sin una prueba global de heterogeneidad. Proponemos usar **una sola exposición** (el cambio del precio comunitario del arroz) y un **bosque causal honesto con conglomerados por comunidad** para responder tres preguntas: (1) ¿hay heterogeneidad real o solo ruido?; (2) ¿el bosque recupera, sin buscarlos, los subgrupos que la literatura encontró a mano?; (3) ¿una regla de focalización basada en el bosque supera a las reglas simples que usaría el cliente, como «focalizar en pobres»?

## 2. Qué encontró la literatura, con qué método y qué quedó abierto

| Estudio | Exposición | Método de heterogeneidad | Hallazgo | Qué deja abierto |
|---|---|---|---|---|
| Elmira y Qaim (2026) | Δ precio del arroz por comunidad, 1997→2000 | Una interacción binaria a la vez: sexo, edad, educación materna, pobreza, zona (ec. 2, p. 4) | HAZ: urbano > rural (signif.); madres de primaria o menos y niños varones, más daño; **no pobres ≥ pobres (n.s.)** (p. 5) | Sin posición neta en arroz, activos ni composición del hogar; sin interacciones entre dimensiones; sin prueba global; sin corrección múltiple |
| Frankenberg y Thomas (2017) | Zona urbana como proxy (p. 12); cohorte | Celdas edad × zona × cuartil de gasto frente a tendencia lineal (fig. 7, cuadro 3) | Escolaridad: **solo la cohorte de 8 años urbana pobre**, −1,95 (0,63), −1,24 (0,69) con EF de hogar. HAZ: sin daño, ni urbano ni rural (p. 12) | Una celda entre ~68 (17 edades × 4 grupos): ¿hallazgo robusto o comparación múltiple? Sin precio |
| Frankenberg, Smith y Thomas (2003) | Choque de gasto del kecamatan | Interacciones choque × riqueza, educación, tamaño; urbano y rural por separado (cuadros 8-9) | Rural: oro y tierra suavizan (p. 316-317); jefe educado suaviza (p. 313); urbano: mujeres mayores (p. 313); ~⅓ de hogares mejoró (p. 295) | Resultado = consumo 1997-98, no capital humano de los niños |
| Friedman y Levinsohn (2002) | Δ precios por provincia × canasta de 1996 | Regresión no paramétrica por gasto y zona; provincias; composición (p. 408-419) | Pobres urbanos 109 % frente a rurales 70 % (p. 408-409); la producción propia invierte el orden rural (p. 414); niños pequeños, más exposición (p. 419) | Es exposición *ex ante* (simulación), no efecto realizado sobre resultados |
| Friedman y Thomas (2009) | Δ gasto medio por provincia × zona | Logits con interacciones; 13 provincias (p. 69-74) | Rurales sin tierra +19 % tristeza, +18 % ansiedad (p. 71); baja educación, más ansiedad (p. 70) | Salud mental adulta; exposición provincial con 13 puntos |

**Contradicciones que un mismo método puede ordenar:**

1. **Pobreza.** Los pobres urbanos pierden más en variación compensatoria (F-L) y en escolaridad (F-T 2017), pero los mejor situados caen más en gasto (FST p. 295; F-T 2017 p. 8) y algo más en HAZ (E-Q, n.s.). Hipótesis: el gradiente por gasto **cambia de signo según el resultado y la zona**.
2. **Urbano en estatura.** E-Q encuentran más daño urbano en HAZ; F-T 2017, con IFLS2+ y sin precios, no encuentran daño ni urbano ni rural.
3. **Edad.** Las ventanas críticas difieren: 3-5 años y en gestación para la estatura adulta (E-Q, asociación); ninguna para ≤ 30 meses (F-T 2017); 8 años para la escolaridad (F-T 2017).

## 3. Cinco vacíos concretos (dónde podemos aportar)

| # | Vacío | Por qué importa | Cómo lo atacamos |
|---|---|---|---|
| V1 | **Nadie ha hecho una prueba global de heterogeneidad** para este choque | Sin ella, los subgrupos reportados pueden ser ruido (F-T 2017 miran ~68 celdas) | `test_calibration` del bosque; si no rechaza, lo decimos |
| V2 | **La posición neta en arroz nunca se ha probado como modificador del efecto sobre los niños** con el precio comunitario | Es el canal económico más claro (F-L p. 414; FST p. 295; F-T 2017 p. 6-7) y explica el resultado urbano (E-Q p. 5) | Covariable del bosque + GATE por categoría + diseño D dentro de comunidad (`03`) |
| V3 | **Los mecanismos de suavización** (oro, tierra, mujeres mayores, hermanos) se estudiaron sobre el consumo, no como modificadores del daño a los niños | Si suavizaron el consumo, deberían reducir el CATE | Covariables de 1997 en el bosque; GATE pre-declarados |
| V4 | **La cohorte urbana pobre de 8 años** es un resultado hallado a mano | Si un bosque honesto la recupera con otra exposición (precio), gana mucho crédito; si no, es evidencia de que era ruido | Prueba de recuperación (§6.5) y placebo con cohortes no expuestas |
| V5 | **Nadie compara reglas de focalización** para este tipo de choque | E-Q sugieren que «focalizar solo en pobres puede no bastar» (p. 5 y 7), pero no lo prueban | RATE/TOC (Yadlowsky et al. 2025) entre la regla del bosque y las reglas simples |

## 4. Hipótesis declaradas antes de ver resultados

Convención: τ(x) < 0 = daño (menos HAZ, menos años de escolaridad o menos puntaje). «Más daño» = τ más negativo.

| H | Modificador (medido en 1997) | Predicción | Fuente | Dónde está en la IFLS |
|---|---|---|---|---|
| H1 | Urbano | Más daño urbano | E-Q p. 5; F-L p. 408-409; FST p. 295; F-T 2017 cuadro 3. En contra para HAZ: F-T 2017 p. 12 | `htrack`/`bk_sc` 1997 (S §5.2) |
| H2 | Comprador neto de arroz (frente a productor) | Más daño en compradores; productores ≈ 0 o efecto positivo | F-L p. 414; FST p. 295; F-T 2017 p. 6-7 | No hay variable directa (S §7.5). Construir con `b1_ks1` 1997, ítem A: compra frente a producción propia (5.075 hogares compran, 1.511 producen, 193 ambas) |
| H3 | Gasto per cápita 1997 (percentil) | Ambiguo; **interacción con zona**: daño concentrado en pobres urbanos para escolaridad; plano o inverso en HAZ | F-L; FST p. 295; E-Q p. 5; F-T 2017 cuadro 3 | Agregado propio desde `b1_ks*` (no hay agregado oficial de 1997; S §7.8) |
| H4 | Educación de la madre (primaria o menos) | Más daño con baja educación | E-Q p. 5, 7-8; FST p. 313 (jefe) | Roster: línea de la madre (`ar11`) + educación (`ar16`/`ar17`) |
| H5 | Edad en 1997 | Escolaridad: daño concentrado cerca de 8 años; HAZ/estatura: 3-5 años | F-T 2017 cuadro 3; E-Q p. 6 | `ptrack` (`age_97`, como texto; S §4.5) y fechas de nacimiento |
| H6 | Sexo | Sin predicción (niños más afectados en HAZ según E-Q p. 5; sin diferencia en matrícula según F-T 2017 p. 9) | — | `ptrack` |
| H7 | Oro y tierra del hogar | Menos daño si el hogar tenía oro o tierra, sobre todo en lo rural | FST p. 305, 316-317; F-T 2017 p. 11 | Activos del hogar (`hr`, libro 2); tierra (`hr`/`ut`) |
| H8 | Composición: hermanos mayores en edad escolar; mujeres de 50+; niños menores de 5 | Más daño escolar en el menor con hermanos mayores; menos daño con mujeres mayores; más exposición con más niños pequeños | Thomas et al. (2004) vía F-T 2017 p. 9; FST p. 313; F-T 2017 p. 10; F-L p. 419 | Roster 1997 |
| H9 | Regla de focalización | Priorizar por el CATE del bosque supera a «pobre» y a «urbano» (RATE mayor) | E-Q p. 5, 7 (sugerido, no probado) | — |

H1-H8 son las dimensiones de `X` que el bosque debe recibir obligatoriamente. A ellas se añaden controles de confusión de 1997 (§5.3). Las hipótesis se fijan por escrito antes de correr el bosque (pendiente de `CLAUDE.md` §10).

## 5. Diseño: cómo poner cada resultado en un bosque

### 5.1 Tratamiento, unidad y conglomerado

- **W (principal):** comunidad de 1997 en el tercil alto de Δlog(precio del arroz) 1997→2000 = 1; tercil bajo = 0; el tercil medio se excluye. Es binario porque así lo exigen el árbol honesto y `get_scores` (ver §6.4), y porque el supuesto de identificación es más débil que con dosis continua (Callaway, Goodman-Bacon y Sant'Anna).
- **W (complemento):** Δlog continuo con las 312 comunidades. `grf` acepta W continuo. Así se usan todas las comunidades y se compara con el β de E-Q.
- **Unidad de asignación y conglomerado:** `commid97` (312). Siempre `clusters = commid97`. El N efectivo para la heterogeneidad es de cientos de comunidades, no de miles de personas: **~208 comunidades** en la comparación por terciles.
- Quedan fuera los **894 hogares sin `commid97`** en 1997 (fuera de comunidades IFLS; S §5.1): sin precio no hay tratamiento.

### 5.2 El resultado: hacer que el bosque respete el diseño

Un bosque causal compara personas tratadas y no tratadas con X parecidas, en corte transversal. Para que herede la identificación de los diseños de `03`, **transformamos el resultado** en lugar de forzar efectos fijos dentro del bosque:

| Resultado | Muestra (S §4.3-4.4) | Y que entra al bosque | Equivale a… |
|---|---|---|---|
| **Escolaridad completada 2014** (primario recomendado) | Cohortes de 5-21 años en 1997: 12.632 miembros en 1997; 7.925 con `dl06` en 2014 | Y = años en 2014 − media de años de la **cohorte no expuesta** (22-30 años en 1997) de la misma comunidad y sexo | Diseño C (cohorte × intensidad) |
| **ΔHAZ 1997→2000** (ancla de replicación) | Niños de 0-5 años en 1997: 3.217 con talla en 1997 y 3.422 en 2000 | Y = HAZ₂₀₀₀ − HAZ₁₉₉₇ (primera diferencia individual) | Diseño B (EF individuales, como E-Q) |
| Estatura adulta 2014 | Cohorte 0-5: 2.586 con talla en 2014 | Y = talla₂₀₁₄ − media de la cohorte mayor ya adulta en 1997, por comunidad y sexo | Diseño C |
| Cognición 2014 (secundario) | Cohorte 0-5: 2.535 con EK completo | Y = puntaje EK2 estandarizado por edad; cohorte no expuesta como X | Corte transversal + controles; exploratorio |

La cohorte no expuesta también entra en X: como media comunitaria, actúa como resultado rezagado y deja que el bosque ajuste más allá de la diferencia uno a uno. **Bosque placebo:** el mismo bosque corrido solo sobre la cohorte no expuesta (Y en niveles) debe dar un ATE ≈ 0 y no rechazar `test_calibration`.

### 5.3 Covariables X (todas de 1997 o antes; nada posterior al tratamiento)

1. **Modificadores pre-declarados (H1-H8):** urbano, posición en arroz (categoría y proporción de producción propia), percentil de gasto per cápita, educación de la madre y del padre, edad en meses, sexo, oro (sí/no y valor), tierra, número de hermanos mayores de 7-15 años, mujeres de 50+ en el hogar, niños menores de 5.
2. **Confusores de la comunidad:** log del precio del arroz en 1997 (reversión a la media), provincia (indicadoras), distancia o acceso a mercado, infraestructura, proporción de hogares productores de la comunidad, choques reportados en 1997 (pérdida de cosecha «demasiado seco» en `b2_ge`; S §7.7), indicador de Sumatra/Kalimantan (humo).
3. **Resultados previos:** HAZ de 1997 (solo para escolaridad y cognición; en ΔHAZ ya está diferenciado), media de la cohorte no expuesta, tendencia 1993-97 de la comunidad cuando exista.
4. **Indicadores de calidad de datos:** entrevista de hogar en 1998 (627 hogares; S §6) y comunidad con precio levantado en 1998 (27 comunidades; S §7.6).

**Se excluyen de X:** OPK/Raskin, migración posterior, salud o estatura posteriores a 1997. Son resultados o mediadores.

## 6. Inferencia: del bosque a afirmaciones defendibles

### 6.1 Secuencia (todo con semilla 2026, `num.trees` ≥ 4000, `num.threads` fijo)

| Paso | Pregunta | Herramienta | ¿En el curso? |
|---|---|---|---|
| 1 | ¿Hay traslape? | `cf$W.hat`; recortar si < 0,05 o > 0,95 | Lab 10 |
| 2 | ¿Cuál es el efecto promedio? | `average_treatment_effect(cf, target.sample = "overlap")` | Lab 10 (sin `overlap`) |
| 3 | **¿Hay heterogeneidad real?** (V1) | `test_calibration(cf)`: coeficiente `differential.forest.prediction` > 0 | Lab 10 |
| 4 | ¿Qué variables la explican? | `best_linear_projection(cf, X[, H1:H8])` (Semenova y Chernozhukov 2021) | **Ampliación** |
| 5 | **Hipótesis pre-declaradas** (H1-H8) | GATE: promedio de los puntajes AIPW (`get_scores`) por subgrupo, con errores por comunidad; Holm sobre los 8 contrastes | **Ampliación** (`get_scores`); Taller 2 registró `average_treatment_effect(cf, subset = …)` |
| 6 | ¿Dónde mira el bosque? | `variable_importance(cf)`, descriptivo, no es un efecto | Lab 10 |
| 7 | **Focalización** (V5, H9) | Bosques en dos mitades de comunidades; `rank_average_treatment_effect` con prioridades: −τ̂ del bosque frente a «pobre», «urbano» y «comprador neto» | Lab 10 (TOC/AUTOC) |
| 9 | Estabilidad | Primer corte del árbol en 200 particiones de comunidades; ATE y calibración con 10 semillas | Lab 09 (estabilidad) |

### 6.2 Cómo leer la prueba de calibración

- `mean.forest.prediction` ≈ 1: el ATE está bien calibrado.
- `differential.forest.prediction`: si es significativamente > 0, hay heterogeneidad que el bosque captura. Si está entre 0 y 1, el bosque exagera la dispersión. Si no rechaza, el resultado honesto es **«no hay evidencia de heterogeneidad»**. Entonces la presentación se apoya en el ATE y en los GATE pre-declarados, con corrección.
- La dispersión de τ̂ por sí sola no prueba nada (Lab 10).

### 6.3 Prueba de recuperación (V4)

¿El bosque encuentra, sin que se lo pidamos, la celda de F-T 2017?

1. En la muestra de escolaridad, comparar el CATE promedio de los urbanos del cuartil inferior con 7-9 años en 1997 frente al resto, con puntajes AIPW y error por comunidad. **Es la única prueba que se declara con la celda exacta de la literatura.**
2. Graficar τ̂ promedio por edad en 1997, separado por urbano × cuartil de gasto: ¿hay un valle cerca de los 8 años?
3. Repetirlo en el bosque placebo (cohorte no expuesta), donde no debe aparecer.

Con la exposición por precio, un efecto concentrado ahí refuerza a F-T 2017. Un nulo junto a una calibración que no rechaza sugiere que su celda pudo ser una comparación múltiple. Las dos lecturas son aportes.

### 6.4 Árbol honesto (retirado el 18-nov)

Decisión del equipo del 18-nov: no se estima árbol causal; por robustez, toda la heterogeneidad se estima con el bosque causal. El entregable al cliente es la comparación de reglas de §6.5 y el perfil de los hogares que el bosque prioriza, descrito con variables observables.

### 6.5 Regla de focalización y comparación (H9)

- Bosque de entrenamiento en la mitad A → prioridad = −τ̂(x) en B. Bosque de evaluación en B → `rank_average_treatment_effect(cf_B, cbind(prioridad_bosque, pobre))`. Si `grf` acepta dos columnas, reporta la diferencia de RATE (verificar en la documentación de la versión instalada).
- Reglas a comparar: (a) bosque; (b) pobre (cuartil inferior de gasto); (c) urbano; (d) comprador neto; (e) árbol de §6.4.
- Mensaje al cliente: «Si solo puede proteger al 20 %, ¿cuánto daño evita cada regla?» (curva TOC).

## 7. Esqueleto de código (R; nombres ilustrativos, no ejecutado)

```r
# 00_main.R: todos los paquetes aquí (convención de los talleres)
pacman::p_load(tidyverse, haven, fixest, grf, rpart, rpart.plot, glmnet, modelsummary)
set.seed(2026)

# --- Bosque principal: escolaridad 2014, W = tercil alto vs. bajo ---------
d  <- read_rds("01_Datos/03_Listos/panel_escolaridad.rds") |> filter(tercil != 2)
X  <- model.matrix(~ urbano + comprador_neto + prop_arroz_propio + pctl_pce97 +
                     educ_madre + educ_padre + edad_meses97 + mujer + oro97 +
                     tierra97 + n_herm_mayores + mujeres50 + n_menores5 +
                     log_p_arroz97 + factor(provincia) + humo + sequia97 +
                     y_cohorte_no_expuesta + entrevista_1998, d)[, -1]
cf <- causal_forest(X, Y = d$y_dif_cohorte, W = d$W, clusters = d$commid97,
                    num.trees = 4000, seed = 2026, num.threads = 4)

summary(cf$W.hat)                                        # traslape
average_treatment_effect(cf, target.sample = "overlap")  # ATE
test_calibration(cf)                                     # V1
best_linear_projection(cf, X[, c("urbano", "comprador_neto", "pctl_pce97",
                                 "educ_madre", "oro97", "n_herm_mayores")])

# --- GATE pre-declarados con puntajes AIPW ------------------------------
d$score <- get_scores(cf)
gate <- feols(score ~ 0 + i(urbano), data = d, cluster = ~commid97)
# … uno por H1-H8; p-valores con p.adjust(method = "holm")

# --- Focalización: dos mitades de comunidades (Lab 10) --------------------
com <- unique(d$commid97); A <- d$commid97 %in% sample(com, length(com) %/% 2)
cf_A <- causal_forest(X[A, ], d$y_dif_cohorte[A], d$W[A], clusters = d$commid97[A], seed = 2026)
cf_B <- causal_forest(X[!A, ], d$y_dif_cohorte[!A], d$W[!A], clusters = d$commid97[!A], seed = 2026)
prior_bosque <- -predict(cf_A, X[!A, ])$predictions     # más daño = más prioridad
rank_average_treatment_effect(cf_B, cbind(prior_bosque, d$pobre[!A]), target = "AUTOC")

# --- Árbol honesto sobre puntajes (mitad A elige, mitad B estima) ----------
arbol <- rpart(score ~ urbano + educ_madre + comprador_neto + edad_meses97 + n_menores5,
               data = d[A, ], control = rpart.control(maxdepth = 3, minbucket = 150, cp = 0))
# poda por CV con folds por comunidad; luego:
d$hoja <- predict(partykit::as.party(arbol), newdata = d, type = "node")
feols(score ~ 0 + factor(hoja), data = d[!A, ], cluster = ~commid97)
```

## 8. Qué viene del curso y qué es ampliación

| Herramienta | Curso | Nota para la sustentación |
|---|---|---|
| `causal_forest` con `clusters`, `test_calibration`, `variable_importance`, RATE/TOC con dos mitades | Lab 10 | En el Lab 10 `W.hat = 0.5` (experimento); aquí se estima, porque no hay aleatorización |
| `rpart`, poda por CV, árbol honesto con partición por conglomerado | Labs 07 y 09 | El Lab 09 compara medias; aquí, puntajes AIPW |
| `feols` con errores agrupados | Lab 10, Taller 2 | Agrupado por comunidad porque la asignación es por comunidad |
| `glmnet` (doble selección para el ATE de referencia) | Lab 06 | — |
| `get_scores`, `best_linear_projection`, `target.sample = "overlap"` | **Ampliación** | Registrar en el README (como el «Registro de ampliaciones» del Taller 2) |
| `haven::read_dta` | **Ampliación** | O construir las bases en Python (`pyreadstat`) y estimar en R (decisión pendiente) |
| `sensemakr` | **Ampliación** | Opcional (`03`, prueba 10) |
| `partykit` (hojas del árbol) | **Ampliación** menor | Alternativa: `rpart` con `$where` en la muestra A y una función propia para B |

## 9. Potencia y riesgos

- **La heterogeneidad cuesta muestra.** Con ~208 comunidades en la comparación por terciles, detectar diferencias entre CATEs exige efectos grandes. Mitigaciones: la escolaridad es el resultado primario (la muestra más grande), el W continuo usa las 312 comunidades y los GATE pre-declarados no dependen de que el bosque «encuentre» nada.
- **Los CATE heredan el sesgo del ATE.** El bosque no corrige un confusor omitido. Por eso las pruebas de `03` (tendencias previas, Yamauchi-Larson, placebo) van antes que los CATE.
- **Comparaciones múltiples.** Un solo resultado primario; Holm sobre H1-H8; los resultados secundarios se reportan como exploratorios.
- **Muestras pequeñas por celda.** La celda de F-T (urbano × cuartil pobre × 7-9 años) puede tener pocas decenas de niños: reportar N y comunidades por celda antes de interpretarla.

## 10. Qué no está verificado

- Ninguna estimación se ha corrido; el código es un esqueleto con nombres ilustrativos.
- Que `rank_average_treatment_effect` de la versión instalada de `grf` acepte dos prioridades y reporte su diferencia; que `get_scores` acepte W continuo; si en `grf` la partición honesta respeta los conglomerados (el submuestreo sí es por conglomerado).
- La construcción de la posición neta en arroz con `b1_ks1` (consumo comprado frente a propio) no mide ventas; falta revisar si `ut` de 1997 trae producción y venta de arroz.
- El agregado de gasto per cápita de 1997 no existe y hay que construirlo; su costo de tiempo no está estimado.
- Los tamaños de celda para H5 y para la prueba de recuperación no se han calculado.
- El apéndice de E-Q (cuadro A4: pruebas de diferencias entre subgrupos) no se revisó.
