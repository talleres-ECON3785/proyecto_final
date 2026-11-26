# =============================================================================
# 15_figuras_presentacion: figuras para proyectar en la sustentación
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Siete figuras grandes y simples (12 x 5,6 in, 200 dpi), SIN titulo ni notas
# (eso lo dice la lamina), con rotulos directos. No estima nada nuevo: lee los
# .csv de 03_Resultados/ (y, solo para F1, el alza por comunidad de la base de
# precios, que no esta en ningun .csv). Intervalos = estimacion +/- 1,96 x EE.
#   F1 alza del precio por comunidad      F4 efecto por grupo (6 dimensiones)
#   F2 efecto principal frente a E-Q      F5 potencia para comparar grupos
#   F3 robustez y placebo                 F6 focalizacion (RATE, escala de dano)
#   F7 distribucion de los efectos predichos del bosque (CATE)
#
# Entradas: 01_Datos/02_Procesados/precio_arroz.rds (F1), 01_Datos/03_Listos/bosque_terciles.rds
#           (F7, solo predict) y los .csv de 06_ate, 08_validacion, 10_bosque, 11_gate y 14_rate
# Salidas:  03_Resultados/Figuras/15_figuras_presentacion/f1_alza.png ... f7_cate_distribucion.png
# =============================================================================

# los paquetes los carga 00_main.R con pacman
carpeta_salida <- "15_figuras_presentacion"
leer <- function(f) read_csv(file.path("03_Resultados/Tablas", f), show_col_types = FALSE)

verde <- "#2E6B4F"
gris <- "#757575"
ocre <- "#B8863B"
texto <- "#222222"
z <- qnorm(0.975)
coma <- function(x, d = 2) sub("-", "−", formatC(x, format = "f", digits = d, decimal.mark = ","), fixed = TRUE)
eje_coma <- scales::label_number(decimal.mark = ",", accuracy = 0.1, style_negative = "minus")
tam_rotulo <- 7.5 # mm; ~21 pt

tema <- theme_minimal(base_size = 24) +
  theme(text = element_text(color = texto),
        axis.text = element_text(color = texto),
        panel.grid.minor = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.major.x = element_line(color = "#E3E3E3", linewidth = 0.5),
        plot.margin = margin(10, 30, 10, 10),
        legend.position = "none")
guardar <- function(nombre, g, width = 12, height = 5.6) {
  ggsave(file.path("03_Resultados/Figuras", carpeta_salida, nombre), g,
         width = width, height = height, dpi = 200, bg = "white")
}

# -----------------------------------------------------------------------------
# F1: alza del precio del arroz por comunidad (base de precios: no hay .csv)
# -----------------------------------------------------------------------------

alza <- readRDS("01_Datos/02_Procesados/precio_arroz.rds") |> filter(!is.na(dosis))
mediana <- median(alza$dosis)
f1 <- ggplot(alza, aes(100 * dosis)) +
  geom_histogram(binwidth = 10, boundary = 0, fill = verde, color = "white") +
  geom_vline(xintercept = 100 * mediana, color = ocre, linewidth = 1.4) +
  annotate("label", x = 100 * mediana + 3, y = Inf, vjust = 1.3, hjust = 0,
           label = "La mitad de las comunidades\nsubió más de +70 %",
           size = tam_rotulo, color = texto, fill = "white", linewidth = 0) +
  scale_x_continuous(labels = \(x) paste0("+", x, " %"), breaks = seq(0, 160, 40)) +
  labs(x = "Alza del precio del arroz en la comunidad, 1997-2000",
       y = "Comunidades") +
  tema + theme(panel.grid.major.y = element_line(color = "#E3E3E3"),
               panel.grid.major.x = element_blank())
guardar("f1_alza.png", f1)

# -----------------------------------------------------------------------------
# F2: efecto principal frente a Elmira y Qaim (2026)
# -----------------------------------------------------------------------------

ate <- leer("06_ate/ninos_ate_especificaciones.csv") |> filter(especificacion == 4)
f2_datos <- tibble(
  estudio = factor(c("Elmira y Qaim (2026)", "Nuestro estudio"),
                   levels = c("Elmira y Qaim (2026)", "Nuestro estudio")),
  # E-Q: cuadro A1, -0,135 (EE robusto 0,0412); 07_Recursos/Articulos/00_hallazgos_articulos.md
  b = c(-0.135, ate$beta), ee = c(0.041, ate$ee_agrupado),
  color = c(gris, verde))
f2 <- ggplot(f2_datos, aes(b, estudio, color = color)) +
  geom_vline(xintercept = 0, color = texto, linewidth = 0.6) +
  geom_errorbar(aes(xmin = b - z * ee, xmax = b + z * ee), width = 0.18,
                linewidth = 1.6, orientation = "y") +
  geom_point(size = 7) +
  geom_text(aes(label = if_else(estudio == "Nuestro estudio",
                                paste0(coma(b, 2), " (≈ ", coma(ate$beta_cm, 1), " cm)"),
                                coma(b, 3))),
            nudge_y = 0.32, size = tam_rotulo, fontface = "bold") +
  annotate("text", x = -0.64, y = 1.5, hjust = 0, size = tam_rotulo, color = texto,
           label = "Más que Elmira y Qaim,\npero los rangos se traslapan", lineheight = 0.9) +
  scale_color_identity() +
  scale_x_continuous(labels = eje_coma, limits = c(-0.65, 0.05), breaks = seq(-0.6, 0, 0.1)) +
  scale_y_discrete(expand = expansion(add = c(0.5, 0.9))) +
  labs(x = "Desviaciones estándar por cada duplicación del precio", y = NULL) +
  tema
guardar("f2_efecto_principal.png", f2, height = 6.6)  # más alta: comparte lámina con el panel de la ecuación

# -----------------------------------------------------------------------------
# F3: robustez y placebo
# -----------------------------------------------------------------------------

nombres <- c(
  "Principal (especificación 4 del efecto promedio)" = "Principal",
  "Sin comunidades con precio de 1998 ni niños medidos en 1998" = "Sin medidas de 1998",
  "Con pesos de la evaluación de salud de 2000 (versión a)" = "Con pesos",
  "Alza sin winsorizar" = "Sin recortar alzas",
  "Alza con precios solo en kg" = "Solo precio por kilo",
  "Sin los niños con |ΔHAZ| > 3" = "Sin cambios extremos")
rob <- leer("08_validacion/ninos_robustez.csv") |>
  transmute(nombre = nombres[variante], b = beta, ee,
            color = if_else(nombre == "Principal", verde, gris))
stopifnot(!anyNA(rob$nombre))
plac <- leer("08_validacion/ninos_placebo.csv") |>
  filter(comunidad_asignada == 1997, especificacion == 2) |>
  transmute(nombre = "Placebo (antes del alza)", b = beta, ee, color = ocre)
f3_datos <- bind_rows(rob, plac) |>
  mutate(nombre = factor(nombre, levels = rev(c(rob$nombre, plac$nombre))))
f3 <- ggplot(f3_datos, aes(b, nombre, color = color)) +
  geom_vline(xintercept = 0, color = texto, linewidth = 0.6) +
  geom_hline(yintercept = 1.5, color = "#CFCFCF", linetype = "dashed") +
  geom_errorbar(aes(xmin = b - z * ee, xmax = b + z * ee), width = 0.3,
                linewidth = 1.3, orientation = "y") +
  geom_point(size = 5) +
  scale_color_identity() +
  scale_x_continuous(labels = eje_coma, breaks = seq(-0.8, 0.2, 0.2), limits = c(-0.85, 0.25)) +
  labs(x = "Desviaciones estándar por cada duplicación del precio", y = NULL) +
  tema
guardar("f3_robustez.png", f3)

# -----------------------------------------------------------------------------
# F4: efecto por grupo (los dos lados de las seis dimensiones)
# -----------------------------------------------------------------------------

gate <- leer("11_gate/ninos_gate.csv")
etiq <- c(G1 = "Edad", G2 = "Zona", G3 = "Educación de la madre", G4 = "Sexo",
          G5 = "Compra de arroz", G6 = "Pobreza")
lado <- c("3-5 años en 1997" = "3-5 años", "0-2 años" = "0-2 años",
          "Urbano" = "Urbano", "Rural" = "Rural",
          "Madre con más que primaria" = "Más que primaria",
          "Primaria o menos" = "Primaria o menos", "Mujer" = "Niña", "Varón" = "Niño",
          "Comprador neto de arroz" = "Compra arroz",
          "No comprador neto" = "Produce su arroz",
          "Pobre" = "Pobre", "No pobre" = "No pobre")
f4_datos <- bind_rows(
  transmute(gate, id, grupo = grupo_0, b = gate_0, ee = ee_gate_0),
  transmute(gate, id, grupo = grupo_1, b = gate_1, ee = ee_gate_1)) |>
  mutate(dimension = factor(etiq[id], levels = etiq),
         grupo = factor(lado[grupo], levels = rev(lado)),
         color = if_else(id == "G1", ocre, verde))
stopifnot(nrow(f4_datos) == 12, !anyNA(f4_datos$grupo))
f4 <- ggplot(f4_datos, aes(b, grupo, color = color)) +
  geom_vline(xintercept = 0, color = texto, linewidth = 0.6) +
  geom_errorbar(aes(xmin = b - z * ee, xmax = b + z * ee), width = 0.35,
                linewidth = 1.1, orientation = "y") +
  geom_point(size = 4) +
  geom_text(data = tibble(dimension = factor("Edad", levels = etiq), b = 0.06, grupo = "3-5 años"),
            aes(b, grupo), label = "← la única\ndiferencia\nvisible", hjust = 0, vjust = 0.75,
            size = 7, color = texto, lineheight = 0.85, inherit.aes = FALSE) +
  facet_wrap(~dimension, ncol = 2, scales = "free_y", dir = "v") +
  scale_color_identity() +
  scale_x_continuous(labels = eje_coma, breaks = c(-0.4, 0, 0.4), limits = c(-0.62, 0.62)) +
  labs(x = "Desviaciones estándar (más alza frente a menos alza)", y = NULL) +
  tema + theme(strip.text = element_text(face = "bold", size = 20, hjust = 0),
               axis.text.y = element_text(size = 20), axis.text.x = element_text(size = 19),
               panel.spacing.x = unit(2.5, "lines"), panel.spacing.y = unit(0.4, "lines"))
guardar("f4_grupos.png", f4)

# -----------------------------------------------------------------------------
# F5: potencia. Efecto promedio del bosque frente a la menor diferencia
#     entre grupos que los datos detectarian (MDE ~ 2,8 x EE, aproximada)
# -----------------------------------------------------------------------------

bosque <- leer("10_bosque/ninos_bosque_ate.csv") |> filter(estimador == "Bosque causal (AIPW)")
mde <- (qnorm(0.975) + qnorm(0.80)) * gate$ee_delta
f5_datos <- tibble(
  que = factor(c("Daño promedio\ndel alza", "Menor diferencia\ndetectable\nentre grupos"),
               levels = rev(c("Daño promedio\ndel alza", "Menor diferencia\ndetectable\nentre grupos"))),
  desde = c(abs(bosque$estimacion), min(mde)), hasta = c(NA, max(mde)),
  color = c(verde, ocre),
  rotulo = c(coma(abs(bosque$estimacion)),
             paste0(coma(min(mde)), " a ", coma(max(mde)), "\nsegún el contraste")))
f5 <- ggplot(f5_datos, aes(y = que)) +
  # la parte clara va de la menor a la mayor diferencia detectable entre los seis contrastes
  # (es un rango entre contrastes, no un intervalo de confianza)
  geom_col(aes(x = coalesce(hasta, desde), fill = color), width = 0.55, alpha = 0.35) +
  geom_col(aes(x = desde, fill = color), width = 0.55) +
  geom_text(aes(x = coalesce(hasta, desde) + 0.02, label = rotulo), hjust = 0, size = tam_rotulo,
            fontface = "bold", color = texto, lineheight = 0.9) +
  scale_fill_identity() +
  scale_x_continuous(labels = eje_coma, limits = c(0, 0.95), breaks = seq(0, 0.6, 0.2),
                     expand = expansion(mult = c(0, 0))) +
  labs(x = "Desviaciones estándar", y = NULL) +
  tema + theme(axis.text.y = element_text(size = 20))
guardar("f5_potencia.png", f5, width = 8.4, height = 4.8)

# -----------------------------------------------------------------------------
# F6: focalizacion. Que tan bien prioriza cada regla a los mas afectados
# -----------------------------------------------------------------------------

reglas <- c(bosque = "Bosque causal", pobre = "Pobre", urbano97 = "Urbano",
            comprador_neto = "Compra más arroz\nde lo que produce")
f6_datos <- leer("14_rate/ninos_rate.csv") |>
  filter(version == "principal", tipo == "AUTOC") |>
  transmute(regla = factor(reglas[prioridad], levels = rev(reglas)), b = estimacion, ee,
            color = if_else(prioridad == "bosque", verde, gris))
stopifnot(nrow(f6_datos) == 4)
f6 <- ggplot(f6_datos, aes(b, regla, color = color)) +
  geom_vline(xintercept = 0, color = texto, linewidth = 0.8) +
  annotate("text", x = 0, y = 4.45, label = "No mejor que escoger al azar",
           hjust = -0.03, size = tam_rotulo, color = texto) +
  geom_errorbar(aes(xmin = b - z * ee, xmax = b + z * ee), width = 0.25,
                linewidth = 1.4, orientation = "y") +
  geom_point(size = 6) +
  scale_color_identity() +
  scale_x_continuous(labels = eje_coma, breaks = seq(-0.4, 0.4, 0.2)) +
  scale_y_discrete(expand = expansion(add = c(0.6, 0.9))) +
  labs(x = "Qué tan bien prioriza a los más afectados (desviaciones estándar)", y = NULL) +
  tema
guardar("f6_focalizacion.png", f6)

# -----------------------------------------------------------------------------
# F7: distribucion de los efectos predichos por el bosque (CATE), con su promedio
#     (ATE AIPW) y el MCO de la especificacion (4) con el mismo contraste.
#     Solo predice con el bosque ya guardado por 10_bosque; no reestima nada
# -----------------------------------------------------------------------------

ate_bosque <- leer("10_bosque/ninos_bosque_ate.csv")
f7_datos <- tibble(tau = predict(readRDS("01_Datos/03_Listos/bosque_terciles.rds")$bosque)$predictions)
b_bosque <- ate_bosque$estimacion[ate_bosque$estimador == "Bosque causal (AIPW)"]
b_mco <- ate_bosque$estimacion[startsWith(ate_bosque$estimador, "MCO")]
stopifnot(length(b_bosque) == 1, length(b_mco) == 1, nrow(f7_datos) == ate_bosque$ninos[1])
f7 <- ggplot(f7_datos, aes(tau)) +
  geom_histogram(binwidth = 0.02, fill = verde, color = "white", linewidth = 0.3) +
  geom_vline(xintercept = 0, color = texto, linewidth = 0.8) +
  geom_vline(xintercept = b_bosque, color = ocre, linewidth = 1.3, linetype = "dashed") +
  annotate("text", x = b_bosque - 0.015, y = Inf, vjust = 1.6, hjust = 1, size = tam_rotulo,
           color = ocre, fontface = "bold", lineheight = 0.9,
           label = paste0("Promedio del bosque: ", coma(b_bosque), "\nMCO: ", coma(b_mco))) +
  scale_x_continuous(labels = eje_coma, breaks = seq(-0.6, 0, 0.2)) +
  labs(x = "Efecto predicho para cada niño (cambio en el HAZ)", y = "Niños") +
  tema + theme(panel.grid.major.y = element_line(color = "#E3E3E3", linewidth = 0.5),
               panel.grid.major.x = element_blank(), axis.title.y = element_text(size = 20))
guardar("f7_cate_distribucion.png", f7)
