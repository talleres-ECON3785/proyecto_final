# =============================================================================
# 06_ate: P2.1, efecto promedio del alza del precio del arroz sobre el ΔHAZ
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Pregunta 1 (¿dolió?): MCO del cambio en el HAZ 1997->2000 sobre la dosis
# (cambio proporcional del precio en la comunidad de 1997; 1 = +100 %), en
# cuatro especificaciones: (1) sin controles, (2) controles de 1997, (3) mas EF
# de provincia y (4) mas el log del precio de 1997. Errores agrupados por
# commid97 y, al lado, robustos sin agrupar (los de Elmira y Qaim). Fila de
# robustez: pendiente promedio del bosque causal con las X de (4). El efecto
# tambien se pasa a cm de forma aproximada.
#
# Entradas: 01_Datos/03_Listos/base_estimacion.rds
#           01_Datos/02_Procesados/haz.rds (talla y edad en 2000, para los cm)
# Salidas:  03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "06_ate"

base <- readRDS("01_Datos/03_Listos/base_estimacion.rds") |>
  mutate(edad_meses97_3 = edad_meses97^3, log_p97 = log(p97))

# controles del cuadro A1 de E-Q medidos en 1997, sin los cinco programas
# (registro §5); edad en meses y al cubo, sin termino cuadratico, como E-Q.
# Los indicadores falta_* los crea 05_base solo si hubo faltantes
controles <- c("mujer", "edad_meses97", "edad_meses97_3", "educ_padre",
               "educ_madre", "fumador_padre", "musulman_padre",
               "musulman_madre", "urbano97", "productor_arroz", "tam_hogar",
               "quintil_gasto", "centro_salud", "agua_entubada",
               "via_vehiculos", "via_asfaltada", "parada_bus",
               "sequia_incendio_97", "mercado", "telefono", "correo", "banco",
               "entrevista_1998", grep("^falta_", names(base), value = TRUE))

# -----------------------------------------------------------------------------
# 1. Las cuatro especificaciones (MCO, EE agrupado por comunidad)
# -----------------------------------------------------------------------------

modelos <- list(
  feols(dhaz ~ dosis, base, cluster = ~commid97),
  feols(dhaz ~ dosis + .[controles], base, cluster = ~commid97),
  feols(dhaz ~ dosis + .[controles] | provincia, base, cluster = ~commid97),
  feols(dhaz ~ dosis + log_p97 + .[controles] | provincia, base,
        cluster = ~commid97)
)

# -----------------------------------------------------------------------------
# 2. Bosque causal con W continuo y las mismas X y ninos que (4)
# -----------------------------------------------------------------------------

d4 <- base[obs(modelos[[4]]), ]
x4 <- model.matrix(reformulate(c(controles, "log_p97", "factor(provincia)")),
                   d4)[, -1]
stopifnot(nrow(x4) == nrow(d4))
bosque <- causal_forest(x4, d4$dhaz, d4$dosis, clusters = factor(d4$commid97),
                        seed = 2026, num.threads = 1)
# con W continuo, average_treatment_effect da la pendiente promedio (pondera
# distinto que MCO: no es el mismo estimando que el beta de feols)
pendiente_bosque <- average_treatment_effect(bosque)

# -----------------------------------------------------------------------------
# 3. Paso a cm (aproximado)
# -----------------------------------------------------------------------------

# el HAZ es lineal en la talla (L = 1 en el metodo LMS de la OMS), asi que
# 1 / (z(talla + 1) - z(talla)) es la DE de la referencia en cm a esa edad y
# sexo. Mismas funciones y corte de edad que 04_haz
z_talla <- function(talla, edad_meses, sexo) {
  edad_dias <- edad_meses * 365.25 / 12
  if_else(edad_dias <= 1856,
          anthro_zscores(sex = sexo, age = edad_dias, lenhei = talla,
                         measure = "h")$zlen,
          anthroplus_zscores(sex = sexo, age_in_months = edad_meses,
                             height_in_cm = talla)$zhfa)
}
de_cm <- base |>
  select(pidlink, mujer) |>
  inner_join(select(readRDS("01_Datos/02_Procesados/haz.rds"),
                    pidlink, talla00, edad_meses00), by = "pidlink") |>
  mutate(sexo = if_else(mujer, 2, 1),
         cm_por_de = 1 / (z_talla(talla00 + 1, edad_meses00, sexo) -
                            z_talla(talla00, edad_meses00, sexo)))
cm_por_de <- mean(de_cm$cm_por_de, na.rm = TRUE)
message("DE media de la talla de referencia en 2000: ", round(cm_por_de, 2),
        " cm (", sum(!is.na(de_cm$cm_por_de)), " niños)")

# -----------------------------------------------------------------------------
# 4. Tabla
# -----------------------------------------------------------------------------

resultados <- imap_dfr(modelos, \(m, i) tibble(
  especificacion = i,
  beta = coef(m)[["dosis"]],
  ee_agrupado = se(m)[["dosis"]],
  p_agrupado = pvalue(m)[["dosis"]],
  ee_robusto = se(summary(m, vcov = "hc1"))[["dosis"]],
  beta_cm = beta * cm_por_de,
  ninos = nobs(m),
  comunidades = n_distinct(base$commid97[obs(m)])
)) |>
  mutate(bosque = c(NA, NA, NA, pendiente_bosque[["estimate"]]),
         ee_bosque = c(NA, NA, NA, pendiente_bosque[["std.err"]]))
print(resultados, width = Inf)
message("Referencia de Elmira y Qaim (2026): -0,135 HAZ por +100 % (EE robusto 0,041)")

# chequeo: ningun nino de mas, estimaciones finitas
stopifnot(all(resultados$ninos <= nrow(base)), all(is.finite(resultados$beta)),
          is.finite(pendiente_bosque[["estimate"]]))

num <- function(x, d) if_else(is.na(x), "", formatC(x, format = "f", digits = d))
si_no <- function(...) if_else(c(...), "Sí", "No")
vista <- tibble(
  fila = c("Alza de +100 % en el precio del arroz", "EE agrupado por comunidad",
           "EE robusto sin agrupar (como E-Q)", "p (EE agrupado)",
           "Equivalente aproximado en cm", "Pendiente promedio del bosque causal",
           "Controles de 1997", "Efectos fijos de provincia",
           "Log del precio de 1997", "Niños", "Comunidades"),
  !!!set_names(map(1:4, \(i) with(resultados[i, ], c(
    num(beta, decimales$z),
    paste0("(", num(ee_agrupado, decimales$z), ")"),
    paste0("[", num(ee_robusto, decimales$z), "]"),
    num(p_agrupado, decimales$estadistico),
    num(beta_cm, decimales$cm),
    if (is.na(bosque)) "" else paste0(num(bosque, decimales$z), " (",
                                      num(ee_bosque, decimales$z), ")"),
    si_no(i >= 2), si_no(i >= 3), si_no(i >= 4),
    num(ninos, decimales$conteo), num(comunidades, decimales$conteo)
  ))), paste0("e", 1:4))
)

tabla <- vista |>
  gt(rowname_col = "fila") |>
  cols_label(e1 = "(1)", e2 = "(2)", e3 = "(3)", e4 = "(4)") |>
  estilo_tabla(
    titulo = "¿Dolió? Efecto promedio del alza del precio del arroz en la talla",
    subtitulo = "Cambio en la talla para la edad (HAZ) 1997-2000 por un alza de +100 %",
    nota = nota_tabla(
      muestra = "base lista", alcance = "contraste",
      extra = c(
        paste("MCO del cambio en el HAZ (OMS) sobre la dosis: cambio",
              "proporcional del precio del arroz en la comunidad de 1997",
              "(1 = +100 %). Controles de 1997: los del cuadro A1 de Elmira y",
              "Qaim sin los programas sociales, más el indicador de entrevista",
              "en 1998 y los de datos faltantes."),
        paste("Referencia: Elmira y Qaim (2026) estiman −0,135 (EE robusto",
              "0,041) con otra medida del precio; la comparación es aproximada."),
        sprintf(paste("cm: aproximación; el efecto en HAZ multiplicado por la",
                      "desviación estándar media de la talla de referencia OMS",
                      "en 2000 (%.2f cm), a la edad y el sexo de cada niño."),
                cm_por_de),
        paste("Bosque causal (grf, tratamiento continuo, agrupado por",
              "comunidad, mismas X y niños que (4)): pendiente promedio con su",
              "EE; pondera distinto que MCO, así que no es el mismo estimando.")
      )))
guardar_tabla("ninos_ate_especificaciones", tabla, resultados, carpeta_salida)
