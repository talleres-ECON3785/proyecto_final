# 04 · Árboles y bosques causales (versión 2, alineada con los laboratorios)

## Qué han trabajado en el curso (revisado en la carpeta `Ciencia de Datos`)

| Material | Tema | Herramientas | Uso en el proyecto |
|---|---|---|---|
| Lab 02-03 | Identificación por diseño, balance, efecto con y sin controles, varianza robusta | regresión, auditoría con agente | Balance por tercil; ATE de referencia |
| Lab 04-05 | Sesgo-varianza, muestra de validación, validación cruzada | partición de muestra | Elección de hiperparámetros |
| Lab 06 | Lasso | `glmnet` | Selección de controles para el ATE |
| Lab 07 | Árboles de regresión, poda por costo-complejidad | `rpart`, `rpart.plot` | Árbol interpretable final |
| Lab 08 | Bagging y bosques, error OOB | `ranger` | Modelos auxiliares |
| Lab 09 | **Árbol causal honesto escrito desde cero** (Athey e Imbens 2016), experimento por colegios | R base | Adaptar su propio código |
| Lab 10 | **Bosque causal**: ATE y CATE, `clusters`, prueba de calibración, importancia de variables, curva TOC | `grf`, `fixest` | Método central |
| Lab 11-12, Taller 3 | Texto como datos, LDA | `tidytext`, `topicmodels` | No se usa (decisión del equipo) |
| Taller 2 | ATE con balance, Lasso de referencia, bosque causal de heterogeneidad | — | Plantilla de flujo de trabajo |

Correcciones frente a la v1: el programa público que consulté incluía econometría espacial, pero no aparece en sus laboratorios, así que la retiro. Y como en el curso el árbol causal se construyó a mano y el bosque con `grf`, descarto el paquete `causalTree` que había sugerido.

Convenciones del curso que conviene mantener: estructura `01_Datos / 02_Scripts / 03_Resultados`, paquetes con `pacman::p_load()`, `CLAUDE.md` en la raíz, presentación tipo "conclusión primero, una idea por lámina".

## La diferencia clave con los laboratorios

En los Labs 09 y 10 el tratamiento era **aleatorio** (experimento por colegios). Aquí es **observacional**: el alza del arroz no se sorteó. Tres consecuencias:

1. El árbol del Lab 09 compara medias de tratados y controles dentro de cada hoja. Eso solo es válido con asignación aleatoria. No se puede reutilizar tal cual.
2. `grf` sí está pensado para este caso: estima primero E[Y|X] y E[W|X] y trabaja con los residuos (ortogonalización, tema 9 del Quiz 2). Athey y Wager (2019) lo aplican a un estudio que tratan como observacional y con conglomerados.
3. La validez depende del supuesto de independencia condicional (archivo 03), no del método.

## Paso 1 · ATE de referencia

- Replicar Elmira y Qaim con `feols()`: panel 1997-2000, efectos fijos individuales, error agrupado por comunidad. Meta: β ≈ −0,135.
- Versión con Lasso (Lab 06): elegir controles con `glmnet` por doble selección (Lasso de Y sobre X, Lasso de W sobre X, MCO con la unión).
- Versión por terciles, que es la que entra al árbol.

## Paso 2 · Bosque causal (método central)

```r
pacman::p_load(grf, fixest, tidyverse)

X <- d |> select(mujer, edad_meses98, urbano97, educ_madre, educ_padre, log_pce97,
                 oro97, tierra97, comprador_neto97, tam_hogar97, haz97,
                 log_precio97, resultado_cohorte_mayor) |> as.matrix()

cf <- causal_forest(X, Y = d$haz_2014, W = d$W,          # W: tercil alto = 1, bajo = 0
                    clusters = d$commid97,                # el tratamiento varia por comunidad
                    num.trees = 4000, seed = 2026)

average_treatment_effect(cf, target.sample = "overlap")   # ATE doblemente robusto
test_calibration(cf)                                      # ¿hay heterogeneidad real?
variable_importance(cf)
rate <- rank_average_treatment_effect(cf, predict(cf)$predictions)  # curva TOC
```

Decisiones específicas para estos datos:

- **`clusters = commid97` es obligatorio.** El tratamiento es constante dentro de comunidad; sin agrupar, los errores estándar salen demasiado pequeños y la honestidad se rompe.
- **`target.sample = "overlap"`** para el ATE: pondera hacia donde hay tratados y controles comparables.
- **Revisar el propensity estimado** (`cf$W.hat`): si se pega a 0 o 1, no hay traslape y hay que recortar.
- **Tratamiento continuo como robustez:** `grf` acepta W continuo y entrega un efecto parcial promedio comparable con el β de Elmira y Qaim. Recordar que comparar dosis exige el supuesto fuerte (archivo 03).
- **Covariable `resultado_cohorte_mayor`:** promedio del resultado en la cohorte no expuesta de la misma comunidad. Acerca el bosque al diseño de cohortes.

## Paso 3 · Árbol honesto interpretable

El árbol es lo que el cliente entiende. Dos rutas, de más a menos recomendada:

**Ruta A · Árbol sobre puntajes doblemente robustos.** Obtener del bosque el puntaje AIPW de cada individuo (`get_scores(cf)`), que bajo el supuesto de identificación promedia al efecto del tratamiento. Partir las comunidades en dos mitades; ajustar un `rpart` (Lab 07) de los puntajes sobre X con la primera; estimar el promedio de puntajes por hoja con la segunda. Usa herramientas del curso, respeta la honestidad y hereda la corrección por confusión.

```r
d$score <- get_scores(cf)
com <- unique(d$commid97); set.seed(2026)
A <- d$commid97 %in% sample(com, length(com) / 2)
arbol <- rpart(score ~ ., data = d[A, c("score", vars_x)], minbucket = 80, cp = 0.005)
d$hoja <- treeClust::rpart.predict.leaves(arbol, d)      # o partykit::as.party + predict(type = "node")
feols(score ~ 0 + factor(hoja), data = d[!A, ], cluster = ~commid97)   # efecto e IC por hoja, mitad B
```

**Ruta B · Adaptar el árbol del Lab 09.** Reemplazar la diferencia de medias por hoja por una diferencia ponderada por el inverso del propensity (o usar Y y W residualizados). Más trabajo y más riesgo de error; solo si el profesor pide ver el algoritmo propio.

Reglas para ambos:

- Partición por **comunidad completa**.
- Mínimo por hoja en individuos y en comunidades (≥ 15 comunidades), no solo en individuos.
- Esperar 3-6 hojas. Mostrar estabilidad: frecuencia del primer corte en 200 semillas.

## Paso 4 · De la heterogeneidad a la recomendación

Igual que el "policy brief" del Lab 09: ¿a quién priorizar? Usar la curva TOC para mostrar cuánto mayor es el daño en el 20 % con CATE más negativo, y describir a ese grupo con variables observables por el cliente (zona, educación de la madre, si el hogar compra arroz).

## Hipótesis de heterogeneidad (declararlas antes de mirar)

| Dimensión | Efecto más negativo esperado en… | Fuente |
|---|---|---|
| Posición en arroz | compradores netos; posible signo contrario en productores | Friedman y Levinsohn; Yamauchi y Larson; Frankenberg y Thomas |
| Zona | urbano | Elmira y Qaim; Friedman y Levinsohn |
| Educación materna | primaria o menos | Elmira y Qaim |
| Sexo | niños en talla (Elmira y Qaim); niñas en otro choque temprano (Maccini y Yang) | Ambiguo: dejar que los datos hablen |
| Activos líquidos | hogares sin oro | Frankenberg, Smith y Thomas |
| Edad en 1998 | los más pequeños para talla; ≈ 8 años para educación | Elmira y Qaim; Frankenberg y Thomas |

## Riesgos

- **Potencia.** Detectar diferencias entre CATEs exige mucha más muestra que el ATE. Si `test_calibration` no rechaza, el resultado honesto es "no hay evidencia de heterogeneidad" y la presentación se apoya en el ATE y en los subgrupos predeclarados.
- **Los CATE heredan el sesgo del ATE.** Ningún método de ML arregla un confusor omitido.
- **Hipótesis múltiples** (tema 10 del Quiz 2): comparar solo las hojas extremas o corregir.
