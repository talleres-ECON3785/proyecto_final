# =============================================================================
# Exploratorio (fuera del pipeline): diferencia minima detectable (MDE)
# aproximada a partir de los EE ya exportados en 03_Resultados/.
# MDE ~ (z_{0,975} + z_{0,80}) x EE = (1,96 + 0,84) x EE ~ 2,8 x EE
# (prueba bilateral al 5 %, potencia del 80 %, aproximacion normal; ignora la
# incertidumbre del propio EE y la correccion de Holm, que la haria mayor).
# Uso: Rscript 02_Scripts/_exploratorio/mde_potencia.R (desde la raiz)
# =============================================================================
suppressMessages(library(tidyverse))
k <- qnorm(0.975) + qnorm(0.80)
leer <- function(f) read_csv(file.path("03_Resultados/Tablas", f), show_col_types = FALSE)
ee <- bind_rows(
  leer("06_ate/ninos_ate_especificaciones.csv") |>
    transmute(estimacion = paste("ATE, especificación", especificacion), ee = ee_agrupado),
  leer("09_interacciones_eq/ninos_interacciones_eq.csv") |>
    filter(ee == "agrupado", especificacion == 4) |>
    transmute(estimacion = paste("Interacción", id, "(β2)"), ee = ee_b2),
  leer("10_bosque/ninos_bosque_ate.csv") |>
    transmute(estimacion = paste("Terciles:", estimador), ee),
  leer("11_gate/ninos_gate.csv") |>
    transmute(estimacion = paste("GATE", id, "(Δ)"), ee = ee_delta),
  leer("14_rate/ninos_rate.csv") |>
    filter(version == "principal") |>
    transmute(estimacion = paste("RATE:", prioridad), ee)
) |>
  mutate(mde = k * ee)
cat(sprintf("Factor: %.3f\n", k))
print(ee, n = Inf)
