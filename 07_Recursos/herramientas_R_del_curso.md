# Herramientas de R usadas en el curso (Laboratorios y Talleres)

Recopilación de los paquetes de R que aparecen en los scripts de `Laboratorios/` y `Talleres/` (ECON-3785, 2026-2). Para cada uno: para qué sirve, cómo se usó y qué consideraciones dejaron los propios scripts, comentarios y catálogos de métodos.

**Fuentes revisadas:** los scripts `.R`/`.qmd` de los Laboratorios 1, 2, 4-13 y de los Talleres 1 y 2; `CLAUDE.md`/`AGENTS.md`/`README.md` de varios laboratorios; y los `07_Recursos/catalogo_metodos.md` de los Talleres 2 y 3. No incluí las copias de `Laboratorio 9/.claude/worktrees/` (duplican los scripts) ni los entornos de Python.

**Alcance y huecos:** el Laboratorio 3 no tiene carpeta propia (su reporte, `10_reporte_laboratorio_03.R`, vive dentro del Lab 2). El Taller 3 todavía no tiene scripts en `02_Scripts/`; solo tiene su catálogo de métodos de texto, así que lo que figura de texto sale de los Labs 11-13 y de ese catálogo. Los "usos" son los que vi en el código; no ejecuté nada.

---

## 1. Mapa rápido

| Paquete | Para qué sirve | Dónde se usó |
|---|---|---|
| `pacman` | Instalar y cargar paquetes con `p_load()` | Labs 7-13; Talleres 2 y 3 (en `00_main.R`) |
| `tidyverse` (`dplyr`, `ggplot2`, `tidyr`, `readr`, `stringr`, `purrr`) | Leer, limpiar, transformar y graficar | Casi todos |
| `janitor` | Estandarizar nombres de columnas | Labs 6, 7, 8 |
| `caret` | Validación cruzada y particiones | Lab 5; Taller 2 |
| `glmnet` | LASSO | Lab 6; Taller 2 |
| `rpart`, `rpart.plot` | Árboles de regresión (CART) y su gráfica | Lab 7, Lab 8 (a mano); Taller 2 |
| `ranger` | Bagging y bosques aleatorios | Lab 8; Taller 2 |
| `grf` | Bosque causal (ATE, CATE, calibración, TOC) | Lab 10; Taller 2 |
| `fixest` | Regresión con errores robustos o agrupados (`feols`, `etable`, `wald`) | Lab 10; Taller 2 |
| `sandwich` | Matrices de varianza robusta (`vcovHC`) | Lab 2; Taller 2 |
| `modelsummary` | Tablas de regresión y de balance | Lab 2; Taller 1; Taller 2 |
| `broom` | Resultados de modelos como tablas (`tidy`, `glance`) | Lab 2; Taller 1 |
| `flextable`, `officer` | Tablas y reporte en Word | Lab 2 |
| `skimr`, `writexl` | Descriptivas rápidas; exportar a Excel | Taller 1 |
| `gt` | Tablas con formato final | Taller 2 |
| `knitr` | `kable()` para tablas | Labs 5 y 12 |
| `tidytext` | Texto en formato ordenado: tokens, TF-IDF, DTM | Labs 11-13 |
| `stopwords`, `stringi`, `SnowballC` | Palabras vacías, quitar tildes, raíces | Labs 11-13 |
| `tm` | Matriz documento-término | Labs 11 y 12 |
| `widyr`, `igraph`, `ggraph` | Correlación entre palabras; redes | Lab 11 |
| `udpipe` | Lematización y categoría gramatical | Lab 12 |
| `topicmodels` | LDA (modelos de tópicos) | Lab 12 |
| `word2vec`, `text2vec`, `Matrix` | Embeddings (skip-gram, GloVe) y matrices ralas | Lab 13 |
| `plotly` | Gráfica 3D interactiva | Lab 13 |
| `parallel` (base) | Cómputo en paralelo | Lab 9 |
| `hash` | Diccionarios en R | Solo en un script de prueba del Lab 7 |

Fuera de los paquetes: **Quarto** (`resultados.qmd`, formato `revealjs`) en el Lab 5.

---

## 2. Infraestructura y datos

### `pacman`
- **Sirve para:** cargar (e instalar si falta) varios paquetes de una vez con `p_load()`.
- **Cómo se usó:** en los laboratorios cada script carga lo suyo con `library(pacman); p_load("tidyverse", ...)`. En el Lab 9, el `00_main.R` solo asegura que `pacman` esté instalado y cada script hace `pacman::p_load()`.
- **Consideraciones:** en los Talleres 2 y 3 la regla es distinta: **todos los paquetes se cargan solo en el `p_load()` de `00_main.R`**, cada uno con un comentario de para qué se usa; los scripts de análisis no cargan librerías. Un paquete nuevo se agrega a esa lista en la misma sesión en que se crea el primer script que lo usa.

### `tidyverse`
- **Sirve para:** `readr` (`read_csv`, `parse_number`), `dplyr` (`mutate`, `filter`, `group_by`, `summarise`, `left_join`), `tidyr` (`pivot_longer`, `pivot_wider`), `stringr`, `purrr` (`map_dbl`) y `ggplot2`.
- **Cómo se usó:** limpieza y construcción de variables en todos los labs y talleres; `pivot_*` en tablas de resultados; `map_dbl` para calcular el RMSE por pliegue (Taller 2).
- **Consideraciones:** los datos crudos nunca se editan; el flujo es Crudos → Listos y los scripts reportan cuántas observaciones se pierden al limpiar (Lab 2, Lab 9). Se usan `stopifnot()` para verificar que las uniones y las filas coincidan (Lab 9, Taller 2).

### `janitor`
- **Sirve para:** `clean_names()` pasa los nombres de columnas a minúscula y sin espacios.
- **Cómo se usó:** `read_csv(URL) %>% clean_names()` al leer la base de carros (Labs 6, 7 y 8).
- **Consideraciones:** cambia los nombres; el resto del script ya usa los nombres limpios (`price` → `precio` se crea después con `parse_number`).

### `parallel` (R base)
- **Sirve para:** `mclapply()` y `detectCores()`.
- **Cómo se usó:** en el Lab 9 (`09_sensibilidad.R`) para el bootstrap de colegios (999 réplicas) y las simulaciones (1000), con `n_nucleos = min(7, detectCores() - 1)`.
- **Consideraciones:** se deja al menos un núcleo libre. `mclapply` no funciona en paralelo en Windows (no lo verifiqué en tu máquina).

---

## 3. Regresión, errores estándar y tablas

### `fixest`
- **Sirve para:** regresión lineal rápida con varianza robusta o agrupada (`feols`), tablas (`etable`) y pruebas conjuntas (`wald`).
- **Cómo se usó:**
  - Lab 10: `feols(puntaje ~ tratamiento, vcov = "hc1")`, con `cluster = ~colegio`, y con controles `+ .[X]` (`.[X]` expande un vector de nombres). `etable(..., keep = "tratamiento", se.below = TRUE, tex = TRUE, file = ...)`.
  - Taller 2: ITT con `vcov = "hc1"`; `fixest::wald(..., keep = ...)` para la prueba conjunta de balance y de representatividad.
- **Consideraciones:** **el nivel de los errores estándar sigue el nivel de la asignación.** En el Lab 10 el tratamiento se asignó por colegio, así que se reporta el error agrupado; en CheMarket (Taller 2) la asignación es individual, así que `"hc1"` sin agrupar. Si el coeficiente casi no cambia al agregar controles, es buena señal del diseño; los controles bajan el error estándar por reducir la variabilidad residual (conclusión de los comentarios del Lab 10). Ojo con los argumentos de `keep` de `wald`: es una expresión regular sobre los nombres de los coeficientes.

### `sandwich`
- **Sirve para:** matrices de varianza robusta; `vcovHC(modelo, type = "HC1")`.
- **Cómo se usó:** Lab 2 (`07_varianza_robusta.R`) compara clásico vs. robusto, sin y con controles; Taller 2 para la regresión lineal.
- **Consideraciones:** `HC1` es la que coincide con `vce(robust)` de Stata. Se le pasa a `modelsummary(..., vcov = "HC1")` para que la tabla salga con los errores robustos.

### `modelsummary`
- **Sirve para:** tablas de regresión (`modelsummary`) y de balance de covariables (`datasummary_balance`).
- **Cómo se usó:**
  - Balance: `datasummary_balance(~easier_signup, data = ..., dinm_statistic = "p.value")` (Taller 1); en el Lab 2 las variables se renombraron con etiquetas legibles (con comillas invertidas) para que la tabla salga con nombres claros.
  - Regresión: `modelsummary(list("nombre" = modelo), gof_map = c("nobs", "r.squared"), add_rows = ..., output = "data.frame")`; en el Taller 2, `output = "gt"`.
- **Consideraciones:** `modelsummary` **reserva los nombres `statistic` y `p.value`**: si se pasan por `gof_map`, descarta la fila. Por eso el F-test global se arma a mano con `broom::glance()` y se agrega con `add_rows` (comentario del Taller 1). `output = "data.frame"` sirve para exportar la tabla a Excel.

### `broom`
- **Sirve para:** `tidy()` (coeficientes como tabla) y `glance()` (estadísticos del modelo).
- **Cómo se usó:** `tidy()` en el Lab 2 (`10_reporte_laboratorio_03.R`, coeficientes de los modelos sin y con controles y de la intensidad del match); `broom::glance(modelo_balance)` en el Taller 1 para el F global.

### `flextable` y `officer`
- **Sirven para:** tablas con formato y un `.docx`.
- **Cómo se usó:** Lab 2 (`10_reporte_laboratorio_03.R`): `flextable(df) %>% theme_booktabs() %>% autofit()`, y `read_docx() %>% body_add_par(...) %>% body_add_flextable(...) %>% body_add_img(...)`.
- **Consideraciones:** las cifras del texto del reporte están escritas dentro de los párrafos del script; si cambian los datos hay que actualizarlas a mano.

### `skimr` y `writexl`
- **Sirven para:** `skim()` (descriptivas de variables numéricas) y `write_xlsx()` (Excel).
- **Cómo se usó:** Taller 1: `skim()` sobre `Revenue`, `time_spent`, `past_sessions`; `write_xlsx(lista_de_tablas, ...)` guarda **un libro con una hoja por tabla**, insumo de la presentación (que no debe incluir código).

### `gt`
- **Sirve para:** tablas con formato final (`tab_header`, `gtsave`).
- **Cómo se usó:** Taller 2, con `guardar_tabla()` en `02_Scripts/00_formato_tablas.R`.
- **Consideraciones:** el `.png` se genera con Chrome o Chromium en modo *headless*, **sin `webshot2`** (registro de ampliaciones del catálogo del Taller 2).

### `knitr`
- `kable()` para tablas en consola/reportes (Lab 5, Lab 12).

---

## 4. Predicción y validación (Labs 4-8; Taller 2 Parte A)

### Regresión lineal base (`lm`, `predict`, `poly`)
- **Cómo se usó:** Lab 4 (sesgo-varianza con modelos de distinta complejidad, partición train/test, RMSE fuera de muestra); Taller 2 como *benchmark*.
- **Consideraciones:** si una categoría aparece solo en `test`, `predict()` falla. El RMSE de `ln(Revenue)` está en logaritmos: para compararlo con el Taller 1 hay que llevar las predicciones a dólares. `lm()` toma como referencia la primera categoría del factor (se cambia con `relevel()`).

### `caret`
- **Sirve para:** validación cruzada (`train()` + `trainControl()`) y particiones (`createFolds()`).
- **Cómo se usó:** Lab 5: `train(formula, method = "lm", trControl = trainControl(method = "LOOCV"))` y `method = "cv", number = 5/10`, para comparar siete modelos. Taller 2: `caret::createFolds(train$Revenue, k = 5)` para tener **los mismos 5 pliegues** en lineal, LASSO, árboles y bosque.
- **Consideraciones:** la regla del Lab 5 era hacer **toda** la CV con `caret`, sin `boot`, `rsample`, `tidymodels` ni ciclos propios. `set.seed(2026)` va justo antes de cada `train()` para que todos los modelos usen las mismas particiones. LOOCV es mucho más costoso (se midió el tiempo con `system.time()`).

### `glmnet`
- **Sirve para:** LASSO (`alpha = 1`; `alpha = 0` sería Ridge).
- **Cómo se usó:** `X <- model.matrix(formula, train)[, -1]`; `glmnet(X, y, alpha = 1)` para la trayectoria; `cv.glmnet()` para elegir λ; `coef(cv, s = "lambda.min")`; `predict(cv, newx = X_test)`. En el Taller 2 se pasa `foldid` (construido con `createFolds`) y `keep = TRUE`.
- **Consideraciones:** `glmnet` **no recibe fórmulas**, solo una matriz numérica y un vector; se quita el intercepto con `[, -1]` y para `test` se usa la **misma fórmula**. Estandariza por defecto y se deja así. Dos reglas para λ: `lambda.min` (mínimo error de CV) o `lambda.1se` (más regularizado). **LASSO solo elige entre lo que se le ofrece:** el diccionario de regresores (potencias, logaritmos, interacciones) lo propone el equipo con criterio económico. La CV es aleatoria: `set.seed()` antes de `cv.glmnet`.

### `rpart` y `rpart.plot`
- **Sirven para:** árbol de regresión (CART) y su gráfica.
- **Cómo se usó:** `rpart(y ~ x, method = "anova", control = rpart.control(cp = 0, minbucket = 7, xval = 10))` → se deja crecer un árbol grande, `printcp()`/`cptable`, y se poda con `prune()` por la regla del mínimo o la regla 1-ES. `rpart.plot(arbol, type = 2, extra = 101, ...)`.
- **Consideraciones:** la CV interna es aleatoria (semilla antes de la llamada). Las categóricas van como factores. `cp` = α / SSR de la raíz (0,01 por defecto). El conjunto de prueba no se toca hasta el final. En el Lab 7, el árbol se construyó primero **a mano** (`03_arbol_a_mano.R`: un ciclo que prueba cada punto de corte de `edad` y compara la suma de cuadrados residual, SSR, de las dos regiones) y después con `rpart`. En el Taller 2 la paleta del árbol sale de `00_formato_graficas.R`.

### `ranger`
- **Sirve para:** bagging y bosque aleatorio, rápido.
- **Cómo se usó:** `ranger(y ~ ., data = train, num.trees = 500, mtry = 8, min.node.size = 5, max.depth = NULL, replace = TRUE, sample.fraction = 1, seed = 2026)`. `predict(bosque, data = test)$predictions`. En el Lab 8 también se armó **un bosque a mano** con `rpart` (muestras bootstrap).
- **Consideraciones:** `ranger` tiene su propia semilla (`seed`); `set.seed()` no basta. `predict()` usa `data =`, no `newdata =`. `bosque$prediction.error` es el **MSE fuera de bolsa**: el RMSE es su raíz. `mtry` por defecto (⌊√p⌋) puede ser malo: se elige con el error OOB sobre una rejilla `mtry × min.node.size`. Más árboles no sobreajustan (se fija grande, no se optimiza); árboles profundos funcionan mejor dentro de un bosque. El Lab 8 **no** calcula importancia de variables; en el Taller 2 se registró como ampliación (`importance = "permutation"`, `$variable.importance`) y se lee como uso del modelo, no como efecto.

---

## 5. Inferencia causal y heterogeneidad (Labs 9-10; Taller 2 Parte B)

### Árbol causal honesto (Lab 9, sin paquete)
- Implementación **desde cero** del estimador CT-H de Athey e Imbens (2016) en R base y `tidyverse`; en ese lab los paquetes de árboles o bosques (`rpart`, `grf`, `causalTree`, `party`) estaban **prohibidos**.
- **Consideraciones:** partición de muestras y folds de CV **por colegio** (la unidad que recibió el tratamiento), errores agrupados por colegio, criterio que premia diferencias de efecto con penalización de varianza, estimación honesta (una submuestra construye, otra estima), poda por CV y elección conjunta de `alpha` y `min_colegios`. Hay un contraste formal de H0 (efecto igual en todas las hojas) con Wald y bootstrap de colegios. En el Taller 2 el equipo decidió **no** usar el árbol causal individual y estimar la heterogeneidad solo con el bosque causal.

### `grf`
- **Sirve para:** `causal_forest()` y sus herramientas.
- **Cómo se usó (Lab 10):**
  ```r
  cf <- causal_forest(X_mat, Y, W, W.hat = 0.5, clusters = dta$colegio,
                      num.trees = 2000, seed = 2026)
  average_treatment_effect(cf)            # ATE
  predict(cf)$predictions                 # CATE, fuera de bolsa
  get_forest_weights(cf)                  # pesos α_i(x)
  test_calibration(cf)                    # prueba formal de heterogeneidad
  variable_importance(cf)                 # dónde corta el bosque
  rank_average_treatment_effect(cf_eva, priorities, target = "AUTOC")  # TOC
  ```
- **Consideraciones:**
  - `grf` exige **matriz numérica** (`as.matrix` o `model.matrix`).
  - `W.hat = 0.5` porque el Lab 10 era un experimento con probabilidad conocida. En el Taller 2 los scripts 12 y 13 usan `W.hat = mean(W)` (proporción tratada, asignación aleatoria con probabilidad común).
  - `clusters = colegio` cuando la asignación fue por colegio; **sin `clusters`** cuando fue individual (CheMarket).
  - `seed` propio, `num.trees ≥ 2000`; honestidad activada por defecto. En el Taller 2 se fija `num.threads = 4` para reproducir las cifras entre máquinas.
  - **La dispersión de τ̂ por sí sola no prueba heterogeneidad.** En `test_calibration`: `mean.forest.prediction ≈ 1` indica ATE bien calibrado; `differential.forest.prediction` es la prueba de heterogeneidad (H0: β ≤ 0); β cercano a 1 es bien calibrado y 0 < β < 1 sugiere que se exagera la heterogeneidad. Si no se rechaza, no hay evidencia de heterogeneidad.
  - `variable_importance` dice dónde mira el bosque; **no** es un efecto ni el porcentaje de heterogeneidad explicado.
  - Para la **focalización** (TOC/AUTOC) se parten los datos en dos mitades (en el Lab 10, por colegio): un bosque de entrenamiento define las prioridades y otro, independiente, evalúa. El error estándar sale de un bootstrap, así que se fija la semilla antes de `rank_average_treatment_effect`.
  - Ampliaciones registradas en el Taller 2: `predict(cf, estimate.variance = TRUE)` (intervalos por CATE) y `average_treatment_effect(cf, subset = ...)` (ATE por subgrupo).

---

## 6. Texto como datos (Labs 11-13; Taller 3)

### `tidytext`
- **Sirve para:** pasar texto a formato ordenado y trabajar con frecuencias.
- **Cómo se usó:** `unnest_tokens(word, texto)`; `count()` + `slice_max()` por grupo con `reorder_within()`/`scale_y_reordered()`; `bind_tf_idf(word, grupo, n)`; `cast_dtm(id, word, n)`; `tidy()` sobre la DTM y sobre el modelo LDA; bigramas con `unnest_tokens(..., token = "ngrams", n = 2)`.
- **Consideraciones:** en TF-IDF el "documento" es el **grupo** (la década en el lab), no el artículo; una palabra presente en todos los grupos tiene `idf = 0`. Sin filtro dominan palabras rarísimas, por eso el lab exige un mínimo de apariciones (`n >= 8`) antes de graficar.

### `stopwords`, `stringi`, `SnowballC`
- **Cómo se usó:** `stopwords("es", source = "snowball")` + `stopwords("en")`, `anti_join()`; `stringi::stri_trans_general(x, "Latin-ASCII")` para quitar tildes; `SnowballC::wordStem(word, language = "spanish")` para raíces.
- **Consideraciones:** las palabras vacías se normalizan igual que el texto (sin tildes). Los labs eliminan todo token con dígitos; si las cifras son contenido (tasas, inflación) hay que decirlo. Las raíces son exploratorias; el Lab 12 las reemplaza por **lemas**. Las listas propias de palabras genéricas cambian los resultados y se documentan.

### `tm`
- **Sirve para:** el objeto `DocumentTermMatrix` que recibe LDA (se arma con `cast_dtm`).
- **Consideraciones:** el Lab 12 recorta el vocabulario a palabras en **≥ 5 documentos y ≤ 25 %** de ellos; esos umbrales son del corpus CEPAL y hay que revisarlos con corpus más pequeños.

### `widyr`, `igraph`, `ggraph`
- **Cómo se usó:** `pairwise_cor(word, id)` (correlación phi entre palabras, con un mínimo de documentos por palabra, `n >= 30`). El script 06 del Lab 11 carga `igraph` y `ggraph` pero, según el catálogo del Taller 3, **no llega a dibujar la red de co-ocurrencias**.

### `udpipe`
- **Sirve para:** lematizar y etiquetar categoría gramatical (modelo `spanish-gsd`, ≈ 28 MB).
- **Cómo se usó:** `udpipe_download_model()`, `udpipe_load_model()`, `udpipe_annotate(..., parser = "none")`, y se conservan `NOUN`, `ADJ`, `VERB`, `PROPN`.
- **Consideraciones:** `options(timeout = 600)` antes de descargar el modelo (con 60 s puede quedar incompleto). **Primero se lematiza y después se quitan las tildes**: `udpipe` necesita el texto original. Los términos compuestos (diccionario de la expresión más larga a la más corta, con `str_replace_all` y patrones `\\b...\\b` tolerantes a tildes) se unen con guion bajo **antes** y no se lematizan.

### `topicmodels`
- **Sirve para:** LDA.
- **Cómo se usó:** `LDA(dtm, k = 4, control = list(seed = 2026))` (VEM) y la versión final `LDA(dtm, k = 12, method = "Gibbs", control = list(alpha = 0.1, delta = 1, iter = 1000, burnin = 200, seed = ...))`; `posterior(lda)$topics`; `tidy(lda, matrix = "beta" / "gamma")`. Hiperparámetros por perplejidad con *document completion* en 3 pliegues (rejilla K × α × δ = 162 ajustes) y coherencia UMass; "lift" = `beta / frecuencia` para nombrar tópicos.
- **Consideraciones:** en `topicmodels`, `set.seed()` **no basta**: la semilla va en `control = list(seed = ...)`. La rejilla completa es costosa. El lab fija K = 12 por balance entre perplejidad, coherencia e interpretabilidad, no por el mínimo de perplejidad. Para nombrar un tópico se leen los documentos más representativos y se contrasta con etiquetas externas.

### `word2vec`, `text2vec` y `Matrix`
- **Cómo se usó:** `word2vec(x, type = "skip-gram", dim = 50, window = 5, iter = 20, negative = 5, min_count = 5, threads = 1)` (con `set.seed`); GloVe con `itoken`, `create_vocabulary() %>% prune_vocabulary(term_count_min = 5)`, `create_tcm(..., skip_grams_window = 5)`, `GlobalVectors$new(rank = 50, x_max = 10)$fit_transform(X, n_iter = 50)` y se suma `W + t(glove$components)`; vecinos y analogías con `sim2(..., method = "cosine", norm = "l2")`; vectores fastText en español recortados al vocabulario.
- **Consideraciones:** la matriz de coocurrencia es muy rala (`Matrix::nnzero` mide el porcentaje de ceros). El lab fija `set.seed(123)` y `threads = 1` en `word2vec` (no verifiqué si esto se hizo por reproducibilidad). El token `</s>` se quita de la matriz. Según el catálogo del Taller 3, los embeddings están **fuera del catálogo** de ese taller salvo que se registren como ampliación.

### `plotly`
- Gráfica 3D interactiva de los vectores (`plot_ly` + `add_markers`), con las palabras de interés coloreadas por campo temático y el resto en gris.

---

## 7. Gráficas

- **`ggplot2`:** los laboratorios usan `theme_classic()` y el color `#5D878E`; los talleres usan el formato propio de `02_Scripts/00_formato_graficas.R` (de los labs se toma la construcción de cada figura, no el estilo). Se guarda con `ggsave()`.
- **Suavizado `geom_smooth(method = "loess")`:** registrado como ampliación en el Taller 2, solo para figuras; con ~85.000 observaciones por lado `loess` agota la memoria si se piden errores estándar.
- **Paquetes de escalas:** `scales::label_comma`, `label_dollar`, `percent_format`, `pseudo_log_trans`, llamados con `::`.

---

## 8. Convenciones transversales

- **Estructura:** `01_Datos / 02_Scripts / 03_Resultados`, scripts numerados y un `00_main.R`; rutas relativas; comentarios en español.
- **Semilla:** `set.seed(2026)` antes de cualquier paso aleatorio. Paquetes con semilla propia (`ranger`, `grf`, `topicmodels`) la reciben por argumento. Los labs de texto usaban `20261028` y el Lab 5 pedía `set.seed(2026)` inmediatamente antes de cada `train()`.
- **Partición:** el Taller 2 usa la del Taller 1 (80/20, `set.seed(2026)`, `sample(seq_len(n), size = round(0.8 * n))`), no la de los Labs 7 y 8 (70/30, semilla 123).
- **Hiperparámetros:** se eligen solo con `train` (CV interna, `xval`, `cv.glmnet` o error OOB); la prueba se usa una sola vez.
- **Reproducibilidad:** ningún número se escribe a mano; todo sale de una corrida, y los scripts verifican con `stopifnot()`.
- **Catálogo cerrado (Talleres 2 y 3):** solo se usan los métodos y funciones del catálogo; lo que se agregue se registra antes en el "Registro de ampliaciones" y en "Decisiones tomadas" de `CLAUDE.md`.

---

## 9. Para el proyecto final

Los métodos de `CLAUDE.md` §6 y su correspondencia con el curso:

| Método del proyecto | Paquete | ¿Visto en el curso? |
|---|---|---|
| Efectos fijos, errores agrupados por comunidad | `fixest::feols` | Sí (Lab 10, Taller 2); en el curso se agrupó por colegio |
| Lasso para controles | `glmnet` | Sí (Lab 6, Taller 2) |
| Árbol interpretable | `rpart` | Sí (Lab 7, Taller 2) |
| Bosque | `ranger` | Sí (Lab 8, Taller 2) |
| Bosque causal con `clusters`, calibración, TOC | `grf` | Sí (Lab 10; en el Taller 2 sin `clusters`) |
| Árbol honesto sobre puntajes AIPW (`get_scores`) | `grf::get_scores` | **`get_scores` no apareció** en los scripts que revisé; el árbol honesto del Lab 9 se escribió a mano |
| Sensibilidad (`sensemakr`) | `sensemakr` | **No apareció** en ningún script de labs ni talleres |
| Lectura de `.dta` | `haven` / `pyreadstat` | **No apareció** `haven` en R; el proyecto ya usa Python con `pyreadstat` |

Por lo tanto, `get_scores`, `sensemakr` y `haven` serían ampliaciones frente al curso. Conviene justificarlas en el README y en la sustentación, como hicieron los talleres con su "Registro de ampliaciones".

---

## Qué no está verificado

- No ejecuté ningún script; todo viene de leer el código, sus comentarios y los catálogos.
- Revisé con detalle los scripts clave de cada unidad, pero no leí línea por línea los ~110 archivos; puede haber funciones secundarias que no aparecen.
- Los parámetros de LDA, `word2vec` y GloVe son los de los scripts de los labs; los del Taller 3 todavía no existen.
- El comportamiento de `mclapply` en tu sistema operativo no se probó.
- Las afirmaciones sobre `get_scores`, `sensemakr` y `haven` se basan en una búsqueda de texto en los `.R`/`.qmd` (sin los directorios `.claude`, `renv` y `.venv`); una búsqueda en otros formatos (por ejemplo `.Rmd` o PDF) podría encontrar más.
