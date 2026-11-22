# =============================================================================
# 07_cuartiles: P2.2, forma del efecto del alza del precio del arroz
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Pregunta 1 (¿dolio?), forma: MCO del cambio en el HAZ 1997->2000 sobre los
# cuartiles del alza (Q2, Q3 y Q4 frente a Q1, cuartiles entre comunidades de
# 02_precio_arroz), en las mismas cuatro especificaciones de 06_ate. Errores
# agrupados por commid97. La figura usa la especificacion (4) y pone encima la
# recta de Elmira y Qaim (-0,135 por +100 %) y la recta de 06_ate con la misma
# especificacion, ambas ancladas en el alza media de Q1.
#
# Entradas: 01_Datos/03_Listos/base_estimacion.rds
# Salidas:  03_Resultados/Tablas/07_cuartiles/ninos_cuartiles_especificaciones.{png,csv}
#           03_Resultados/Figuras/07_cuartiles/ninos_cuartiles_coeficientes.png
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R") # tambien carga el formato de graficas
carpeta_salida <- "07_cuartiles"

base <- readRDS("01_Datos/03_Listos/base_estimacion.rds") |>
  mutate(edad_meses97_3 = edad_meses97^3, log_p97 = log(p97),
         q2 = cuartil == 2, q3 = cuartil == 3, q4 = cuartil == 4)

# MISMA lista que 06_ate.R: si cambia alla, hay que cambiarla aqui
controles <- c("mujer", "edad_meses97", "edad_meses97_3", "educ_padre",
               "educ_madre", "fumador_padre", "musulman_padre",
               "musulman_madre", "urbano97", "productor_arroz", "tam_hogar",
               "quintil_gasto", "centro_salud", "agua_entubada",
               "via_vehiculos", "via_asfaltada", "parada_bus",
               "sequia_incendio_97", "mercado", "telefono", "correo", "banco",
               "entrevista_1998", grep("^falta_", names(base), value = TRUE))

# -----------------------------------------------------------------------------
# 1. Las cuatro especificaciones con cuartiles (EE agrupado por comunidad)
# -----------------------------------------------------------------------------

modelos <- list(
  feols(dhaz ~ q2 + q3 + q4, base, cluster = ~commid97),
  feols(dhaz ~ q2 + q3 + q4 + .[controles], base, cluster = ~commid97),
  feols(dhaz ~ q2 + q3 + q4 + .[controles] | provincia, base,
        cluster = ~commid97),
  feols(dhaz ~ q2 + q3 + q4 + log_p97 + .[controles] | provincia, base,
        cluster = ~commid97)
)
# la recta de 06_ate con la especificacion (4), para la figura
beta_lineal <- coef(feols(dhaz ~ dosis + log_p97 + .[controles] | provincia,
                          base, cluster = ~commid97))[["dosis"]]

# alza media de cada cuartil entre los ninos de la base
alza <- base |>
  group_by(cuartil) |>
  summarise(alza_media = mean(dosis), comunidades_q = n_distinct(commid97),
            ninos_q = n(), .groups = "drop")
stopifnot(nrow(alza) == 4, all(diff(alza$alza_media) > 0))

resultados <- imap_dfr(modelos, \(m, i) tibble(
  especificacion = i,
  cuartil = 2:4,
  coef = coef(m)[c("q2TRUE", "q3TRUE", "q4TRUE")],
  ee = se(m)[c("q2TRUE", "q3TRUE", "q4TRUE")],
  p = pvalue(m)[c("q2TRUE", "q3TRUE", "q4TRUE")],
  ninos = nobs(m),
  comunidades = n_distinct(base$commid97[obs(m)])
)) |>
  left_join(alza, by = "cuartil")
print(resultados, n = Inf, width = Inf)
print(alza)

# chequeo: ningun nino de mas, estimaciones finitas
stopifnot(all(resultados$ninos <= nrow(base)), all(is.finite(resultados$coef)))

# -----------------------------------------------------------------------------
# 2. Tabla
# -----------------------------------------------------------------------------

num <- function(x, d) formatC(x, format = "f", digits = d)
si_no <- function(...) if_else(c(...), "Sí", "No")
etiqueta_q <- \(k) sprintf("Cuartil %d frente a 1 (alza media %+.0f %%)", k,
                           100 * alza$alza_media[k])
vista <- tibble(
  fila = c(etiqueta_q(2:4), "Alza media del cuartil 1",
           "Controles de 1997", "Efectos fijos de provincia",
           "Log del precio de 1997", "Niños", "Comunidades"),
  !!!set_names(map(1:4, \(i) {
    r <- filter(resultados, especificacion == i)
    c(paste0(num(r$coef, decimales$z), " (", num(r$ee, decimales$z), ")"),
      sprintf("%+.0f %%", 100 * alza$alza_media[1]),
      si_no(i >= 2), si_no(i >= 3), si_no(i >= 4),
      num(r$ninos[1], decimales$conteo), num(r$comunidades[1], decimales$conteo))
  }), paste0("e", 1:4))
)

tabla <- vista |>
  gt(rowname_col = "fila") |>
  cols_label(e1 = "(1)", e2 = "(2)", e3 = "(3)", e4 = "(4)") |>
  estilo_tabla(
    titulo = "¿El daño crece con el alza? Efecto por cuartil del alza del precio del arroz",
    subtitulo = "Cambio en la talla para la edad (HAZ) 1997-2000, frente al cuartil de menor alza",
    nota = nota_tabla(
      muestra = "base lista", alcance = "contraste",
      extra = c(
        paste("MCO del cambio en el HAZ (OMS) sobre los cuartiles del alza",
              "del precio del arroz entre comunidades (cambio proporcional",
              "nominal 1997-2000). Entre paréntesis, EE agrupado por comunidad.",
              "Mismos controles que la tabla del efecto promedio."),
        sprintf(paste("Comunidades por cuartil: %s. Niños por cuartil: %s."),
                paste(alza$comunidades_q, collapse = ", "),
                paste(alza$ninos_q, collapse = ", "))
      )))
guardar_tabla("ninos_cuartiles_especificaciones", tabla, resultados,
              carpeta_salida)

# -----------------------------------------------------------------------------
# 3. Figura: especificacion (4) con las rectas de E-Q y de 06_ate
# -----------------------------------------------------------------------------

puntos <- resultados |>
  filter(especificacion == 4) |>
  select(alza_media, coef, ee) |>
  add_row(alza_media = alza$alza_media[1], coef = 0, ee = NA, .before = 1)
puntos_n <- filter(resultados, especificacion == 4) |> slice(1)
x_rectas <- range(alza$alza_media)
rectas <- tibble(
  alza_media = rep(x_rectas, 2),
  recta = rep(c(sprintf("Elmira y Qaim (2026): %.3f por +100 %%", -0.135),
                sprintf("Efecto promedio, misma especificación: %.3f por +100 %%",
                        beta_lineal)), each = 2),
  efecto = c(-0.135, -0.135, beta_lineal, beta_lineal) *
    (rep(x_rectas, 2) - alza$alza_media[1])
)

figura <- ggplot(puntos, aes(alza_media, coef)) +
  geom_hline(yintercept = 0, color = gris_secundario, linewidth = 0.4) +
  geom_line(data = rectas, aes(alza_media, efecto, linetype = recta),
            color = gris_secundario, linewidth = 0.6) +
  geom_errorbar(aes(ymin = coef - 1.96 * ee, ymax = coef + 1.96 * ee),
                width = 0.03, color = paleta_categorica[1], na.rm = TRUE) +
  geom_point(size = 3, color = paleta_categorica[1]) +
  scale_x_continuous(labels = scales::label_percent()) +
  scale_linetype_manual(values = set_names(c("dashed", "solid"),
                                            unique(rectas$recta)), name = NULL) +
  labs(title = "El daño en la talla según el tamaño del alza del arroz",
       subtitle = paste0(subtitulo_contraste,
                         "\nEfecto frente al cuartil de menor alza."),
       x = "Alza media del precio del arroz en el cuartil",
       y = "Cambio en el HAZ frente al cuartil 1",
       caption = str_wrap(paste0(
         "MCO con controles de 1997, efectos fijos de provincia y log del ",
         "precio de 1997; intervalos al 95 % con EE agrupado por comunidad. ",
         "Las rectas parten del alza media del cuartil 1. ",
         puntos_n$ninos, " niños, ",
         puntos_n$comunidades, " comunidades."), 130)) +
  tema_presentacion +
  theme(legend.position = "bottom", legend.direction = "vertical")
guardar_figura("ninos_cuartiles_coeficientes.png", figura, carpeta_salida)
