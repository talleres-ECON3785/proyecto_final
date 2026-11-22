# =============================================================================
# 12_calibracion: P4.1, prueba de calibracion del bosque principal
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Pregunta 3 (¿el bosque supera a las reglas simples?), primer paso.
# test_calibration() del bosque de 10_bosque (tercil alto frente a bajo):
# regresion del resultado centrado sobre la prediccion media y la prediccion
# diferencial del bosque (fuera de la bolsa).
#   - prediccion media: coeficiente cercano a 1 si el ATE esta bien calibrado;
#   - prediccion diferencial: coeficiente > 0 y significativo si el bosque
#     capta heterogeneidad real (p unilateral, como lo reporta grf).
# Una sola prueba pre-especificada: fuera de las familias de Holm.
#
# Entradas: 01_Datos/03_Listos/bosque_terciles.rds
# Salidas:  03_Resultados/Tablas/12_calibracion/ninos_calibracion.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "12_calibracion"

guardado <- readRDS("01_Datos/03_Listos/bosque_terciles.rds")
bosque <- guardado$bosque
d <- guardado$datos

calibracion <- test_calibration(bosque)
print(calibracion)

resultados <- tibble(
  termino = rownames(calibracion),
  coeficiente = calibracion[, 1], ee = calibracion[, 2],
  t = calibracion[, 3], p_unilateral = calibracion[, 4],
  ninos = nrow(d), comunidades = n_distinct(d$commid97)
)
stopifnot(nrow(resultados) == 2, all(is.finite(resultados$coeficiente)))
message("¿La prediccion diferencial rechaza al 5 %? ",
        resultados$p_unilateral[2] < 0.05)

num <- function(x, k) formatC(x, format = "f", digits = k)
tabla <- resultados |>
  transmute(
    termino = c("Predicción media (≈ 1: ATE calibrado)",
                "Predicción diferencial (> 0: heterogeneidad que el bosque capta)"),
    coef = num(coeficiente, decimales$z), ee = num(ee, decimales$z),
    p = num(p_unilateral, decimales$estadistico)) |>
  gt(rowname_col = "termino") |>
  cols_label(coef = "Coeficiente", ee = "EE", p = "p (unilateral)") |>
  estilo_tabla(
    titulo = "¿Capta el bosque heterogeneidad? Prueba de calibración",
    subtitulo = paste("Bosque causal del tercil alto frente al bajo del alza;",
                      "cambio en el HAZ 1997-2000"),
    nota = nota_tabla(
      n = nrow(d), comunidades = n_distinct(d$commid97),
      muestra = "terciles alto y bajo del alza", alcance = "contraste",
      extra = c(
        paste("test_calibration de grf: regresión del resultado centrado sobre",
              "la predicción media y la diferencial del bosque, fuera de la",
              "bolsa. p unilateral, como lo reporta grf."),
        paste("Una sola prueba pre-especificada, fuera de las familias de Holm.",
              "Si la predicción diferencial no rechaza, no hay evidencia de",
              "heterogeneidad más allá de los GATE pre-declarados.")
      )))
guardar_tabla("ninos_calibracion", tabla, resultados, carpeta_salida)
