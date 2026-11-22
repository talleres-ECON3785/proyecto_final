# =============================================================================
# 09_interacciones_eq: P3.1, replica de las cinco interacciones de Elmira y Qaim
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Pregunta 2 (¿a quien?), parte de replica. Una interaccion binaria a la vez
# (pre-registro §1, ec. 2 de E-Q, p. 4), con la dosis y la especificacion (4)
# de 06_ate (controles de 1997, EF de provincia y log del precio de 1997):
#   dhaz = b1 dosis + b2 dosis x X + g X + controles + log_p97 | provincia
# b1 = efecto en X = 0, b2 = diferencia, b1 + b2 = efecto en X = 1.
# EE agrupados por commid97 (los que se interpretan) y robustos HC1 (los de
# E-Q) lado a lado; p sin ajustar y Holm (familia F2, m = 5) sobre los p
# agrupados de b2. Como comparacion sin familia, el .csv trae tambien la
# especificacion (2) de 06_ate (sin EF de provincia ni log del precio), mas
# parecida a la de E-Q.
#
# Entradas: 01_Datos/03_Listos/base_estimacion.rds
# Salidas:  03_Resultados/Tablas/09_interacciones_eq/ninos_interacciones_eq.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "09_interacciones_eq"

base <- readRDS("01_Datos/03_Listos/base_estimacion.rds") |>
  mutate(edad_meses97_3 = edad_meses97^3, log_p97 = log(p97),
         # E1: X = 1 es 0-2 anios en 1997. E-Q no dicen que grupo es la "edad
         # critica"; se infiere del orden de su fig. 5 (pre-registro §1)
         edad_0_2 = edad_meses97 < 36)

# mismos controles que 06_ate (cuadro A1 de E-Q en 1997, sin los programas)
controles <- c("mujer", "edad_meses97", "edad_meses97_3", "educ_padre",
               "educ_madre", "fumador_padre", "musulman_padre",
               "musulman_madre", "urbano97", "productor_arroz", "tam_hogar",
               "quintil_gasto", "centro_salud", "agua_entubada",
               "via_vehiculos", "via_asfaltada", "parada_bus",
               "sequia_incendio_97", "mercado", "telefono", "correo", "banco",
               "entrevista_1998", grep("^falta_", names(base), value = TRUE))

# las cinco interacciones del cuadro A4 de E-Q, con su beta2 en HAZ (EE robusto
# sin agrupar), cotejado con el suplemento el 20-nov (pre-registro §1)
interacciones <- tribble(
  ~id,  ~variable,            ~grupo_1,                     ~grupo_0,               ~eq_b2, ~eq_ee,
  "E1", "edad_0_2",           "0-2 años en 1997",           "3-5 años",              0.005, 0.066,
  "E2", "mujer",              "Mujer",                      "Varón",                 0.099, 0.073,
  "E3", "madre_mas_primaria", "Madre con más que primaria", "Primaria o menos",      0.129, 0.075,
  "E4", "pobre",              "Pobre",                      "No pobre",              0.216, 0.180,
  "E5", "urbano97",           "Urbano",                     "Rural",                -0.270, 0.153
)

# -----------------------------------------------------------------------------
# 1. Una regresion por interaccion y especificacion
# -----------------------------------------------------------------------------

# b1, b2 y b1 + b2 con su EE (combinacion lineal de la matriz de varianzas)
extraer <- function(m, vcov_tipo) {
  s <- if (vcov_tipo == "agrupado") m else summary(m, vcov = "hc1")
  b <- coef(s)[c("dosis", "dosis_x")]
  v <- vcov(s)[c("dosis", "dosis_x"), c("dosis", "dosis_x")]
  gl <- degrees_freedom(s, "t") # grados de libertad que usa fixest en sus p
  ee_suma <- sqrt(sum(v))
  tibble(b1 = b[[1]], ee_b1 = sqrt(v[1, 1]),
         b2 = b[[2]], ee_b2 = sqrt(v[2, 2]),
         p_b2 = pvalue(s)[["dosis_x"]],
         suma = sum(b), ee_suma = ee_suma,
         p_suma = 2 * pt(abs(sum(b) / ee_suma), gl, lower.tail = FALSE))
}

estimar <- function(id, variable, especificacion) {
  d <- base |>
    filter(!is.na(.data[[variable]])) |>
    mutate(x = as.numeric(.data[[variable]]), dosis_x = dosis * x)
  # si X ya es un control (mujer, urbano97), entra una sola vez, como x
  ctrl <- setdiff(controles, variable)
  f <- if (especificacion == 4) {
    dhaz ~ dosis + dosis_x + x + log_p97 + .[ctrl] | provincia
  } else {
    dhaz ~ dosis + dosis_x + x + .[ctrl]
  }
  m <- feols(f, d, cluster = ~commid97)
  bind_rows(agrupado = extraer(m, "agrupado"), robusto = extraer(m, "robusto"),
            .id = "ee") |>
    mutate(id = id, especificacion = especificacion, ninos = nobs(m),
           comunidades = n_distinct(d$commid97[obs(m)]),
           ninos_x1 = sum(d$x[obs(m)] == 1),
           comunidades_x1 = n_distinct(d$commid97[obs(m)][d$x[obs(m)] == 1]),
           .before = 1)
}

resultados <- expand_grid(select(interacciones, id, variable),
                          especificacion = c(4, 2)) |>
  pmap_dfr(estimar) |>
  left_join(select(interacciones, -variable), by = "id")

# Holm (familia F2, m = 5): solo los p agrupados de b2 de la especificacion 4
resultados <- resultados |>
  group_by(ee, especificacion) |>
  mutate(p_b2_holm = if_else(ee == "agrupado" & especificacion == 4,
                             p.adjust(p_b2, "holm"), NA_real_)) |>
  ungroup()
print(resultados, width = Inf)

stopifnot(nrow(resultados) == 20, all(is.finite(resultados$b2)),
          all(resultados$ninos <= nrow(base)))

# -----------------------------------------------------------------------------
# 2. Tabla (especificacion 4)
# -----------------------------------------------------------------------------

num <- function(x, d) formatC(x, format = "f", digits = d)
z <- decimales$z
p <- decimales$estadistico
agr <- filter(resultados, ee == "agrupado", especificacion == 4)
rob <- filter(resultados, ee == "robusto", especificacion == 4)
vista <- agr |>
  left_join(select(rob, id, rb_b1 = ee_b1, rb_b2 = ee_b2, rb_p = p_b2,
                   rb_suma = ee_suma), by = "id") |>
  transmute(
    id, grupos = paste0(grupo_1, " (X = 1) frente a ", grupo_0),
    b1 = paste0(num(b1, z), " (", num(ee_b1, z), ") [", num(rb_b1, z), "]"),
    b2 = paste0(num(b2, z), " (", num(ee_b2, z), ") [", num(rb_b2, z), "]"),
    p_agr = num(p_b2, p), p_holm = num(p_b2_holm, p), p_rob = num(rb_p, p),
    suma = paste0(num(suma, z), " (", num(ee_suma, z), ")"),
    eq = paste0(num(eq_b2, z), " (", num(eq_ee, z), ")"),
    n = paste0(num(ninos, 0), " / ", num(ninos_x1, 0)),
    comunidades = num(comunidades, 0)
  )

tabla <- vista |>
  gt(rowname_col = "id") |>
  cols_label(grupos = "Interacción", b1 = "β1: efecto en X = 0",
             b2 = "β2: diferencia", p_agr = "p (agrupado)",
             p_holm = "p Holm (F2)", p_rob = "p (robusto)",
             suma = "β1 + β2: efecto en X = 1", eq = "E-Q: β2 (EE robusto)",
             n = "Niños (total / X = 1)", comunidades = "Comunidades") |>
  cols_width(grupos ~ px(230), c(b1, b2) ~ px(170), c(suma, eq) ~ px(130),
             c(n, comunidades) ~ px(125), everything() ~ px(95)) |>
  estilo_tabla(
    titulo = "¿A quién? Réplica de las cinco interacciones de Elmira y Qaim",
    subtitulo = paste("Cambio en el HAZ 1997-2000 por un alza de +100 % del",
                      "precio del arroz, una interacción a la vez"),
    nota = nota_tabla(
      muestra = "base lista", alcance = "contraste",
      extra = c(
        paste("MCO del cambio en el HAZ (OMS) sobre la dosis, la dosis por X y",
              "X, con la especificación (4) del efecto promedio: controles de",
              "1997, efectos fijos de provincia y log del precio de 1997.",
              "Entre paréntesis, EE agrupado por comunidad (el que se",
              "interpreta); entre corchetes, EE robusto sin agrupar (el de E-Q)."),
        paste("p Holm: familia F2 del pre-registro (m = 5), sobre los p",
              "agrupados de β2. α = 0,05, bilateral."),
        paste("E1: E-Q no dicen qué grupo es la «edad crítica»; X = 1 = 0-2",
              "años es una inferencia nuestra a partir de su fig. 5. E-Q",
              "(cuadro A4 del suplemento) usan otra medida del precio y no",
              "usan efectos fijos de provincia: la comparación es de signo y",
              "orden, aproximada."),
        paste("E3 y E4 pierden a los niños sin dato de la madre o del gasto.",
              "Pobre: línea regional de dic. 1997 (Widyanti et al. 2009).")
      )))
guardar_tabla("ninos_interacciones_eq", tabla, resultados, carpeta_salida)
