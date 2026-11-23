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
#           03_Resultados/Figuras/12_calibracion/ninos_cate_distribucion.png
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
source("02_Scripts/00_formato_graficas.R")
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

# --- Distribucion de los efectos predichos (CATE) ----------------------------
# tau_hat fuera de la bolsa de cada nino. Descriptivo: su dispersion mezcla
# heterogeneidad y ruido de estimacion; la calibracion dice si hay de la primera
d <- mutate(d, tau = predict(bosque)$predictions)
ate <- average_treatment_effect(bosque)
message("tau_hat: mediana ", round(median(d$tau), 3), ", p5 ",
        round(quantile(d$tau, 0.05), 3), ", p95 ", round(quantile(d$tau, 0.95), 3),
        "; negativos ", round(100 * mean(d$tau < 0), 1), " %")

fig <- ggplot(d, aes(tau)) +
  geom_histogram(binwidth = 0.02, fill = paleta_categorica[1], alpha = 0.85) +
  geom_vline(xintercept = 0, color = gris_secundario) +
  geom_vline(xintercept = ate[["estimate"]], linetype = "dashed",
             color = paleta_categorica[2], linewidth = 0.9) +
  annotate("text", x = ate[["estimate"]], y = Inf, vjust = 1.5, hjust = 1.05,
           color = paleta_categorica[2], size = 3.8,
           label = sprintf("ATE (AIPW): %s (EE %s)",
                           num(ate[["estimate"]], decimales$z),
                           num(ate[["std.err"]], decimales$z))) +
  labs(title = "Efecto predicho por el bosque para cada niño",
       subtitle = paste0(subtitulo_contraste, " ", nrow(d), " niños en ",
                         n_distinct(d$commid97), " comunidades."),
       x = "Efecto predicho del tercil alto frente al bajo (cambio en HAZ, fuera de la bolsa)",
       y = "Niños",
       caption = sprintf(paste(
         "Bosque causal (grf), X de 1997, agrupado por comunidad. La dispersión",
         "mezcla heterogeneidad y ruido de estimación: la calibración no la",
         "distingue\ndel ruido (predicción diferencial %s, p unilateral %s).",
         "Ningún efecto individual tiene intervalo propio aquí; no se lee",
         "niño por niño.\nTerciles del alza dentro de provincia; el tercil",
         "medio no entra."),
         num(resultados$coeficiente[2], decimales$z),
         num(resultados$p_unilateral[2], decimales$estadistico))) +
  tema_presentacion
guardar_figura("ninos_cate_distribucion.png", fig, carpeta_salida)
