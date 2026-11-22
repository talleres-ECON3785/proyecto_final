# =============================================================================
# 08_validacion: P2.3, placebo y robustez del efecto promedio
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# 1. Placebo: cohorte de 0-5 anios en 1993. Cambio en el HAZ 1993->1997 (antes
#    del alza) sobre el alza del precio del arroz 1997->2000 de su comunidad.
#    Si el diseno funciona, debe dar cerca de cero. Se asigna el alza por la
#    comunidad de 1997 (principal, la misma regla del analisis) y por la de
#    1993 (decision de Mateo, 22-nov). Dos columnas de controles: ninguno; y
#    edad en meses en 1993 y su cubo, sexo y EF de provincia.
# 2. Robustez de la especificacion (4) de 06_ate, cambiando una cosa a la vez:
#    sin las comunidades con precio de 1998 ni los ninos medidos en 1998, con
#    pesos de la evaluacion de salud de 2000 (version a, pw00usxa; el
#    longitudinal pwt00la solo cubria a 932 ninos), sin winsorizar la
#    dosis, con la dosis solo en kg y sin los ninos con |dHAZ| > 3.
# El desgaste segun el alza ya esta en 05_base (P1.5 y P1.6).
#
# Entradas: 01_Datos/03_Listos/base_estimacion.rds
#           01_Datos/02_Procesados/{tracks,haz,precio_arroz}.rds
#           01_Datos/01_Crudos/IFLS3/Household Data/ptrack.dta (solo pw00usxa)
# Salidas:  03_Resultados/Tablas/08_validacion/ninos_placebo.{png,csv}
#           03_Resultados/Tablas/08_validacion/ninos_robustez.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "08_validacion"
procesados <- "01_Datos/02_Procesados"

num <- function(x, d) if_else(is.na(x), "", formatC(x, format = "f", digits = d))
coef_ee <- function(m, v) paste0(num(coef(m)[[v]], decimales$z), " (",
                                 num(se(m)[[v]], decimales$z), ")")

# -----------------------------------------------------------------------------
# 1. Placebo: cohorte de 1993, cambio en el HAZ 1993->1997
# -----------------------------------------------------------------------------

precio <- readRDS(file.path(procesados, "precio_arroz.rds"))
placebo <- readRDS(file.path(procesados, "tracks.rds")) |>
  filter(cohorte_93) |>
  select(pidlink, sex, commid93, commid97) |>
  inner_join(select(readRDS(file.path(procesados, "haz.rds")),
                    pidlink, haz93, haz97, edad_meses93), by = "pidlink") |>
  filter(!is.na(haz93), !is.na(haz97)) |>
  mutate(dhaz = haz97 - haz93, mujer = sex == 3,
         edad_meses93_3 = edad_meses93^3)
stopifnot(!anyDuplicated(placebo$pidlink), nrow(placebo) > 0)

message("Placebo: ", nrow(placebo), " niños con HAZ válido en 1993 y 1997; ",
        sum(is.na(placebo$commid97)), " sin comunidad IFLS en 1997; ",
        sum(placebo$commid93 != placebo$commid97, na.rm = TRUE),
        " con comunidad distinta en 1993 y 1997")

# asigna el alza (dosis principal) por la comunidad indicada; los codigos de
# 1993 se cruzan con los de 1997 del precio
asignar <- function(comunidad) {
  placebo |>
    mutate(comunidad = .data[[comunidad]]) |>
    inner_join(select(precio, comunidad = commid97, provincia, dosis),
               by = "comunidad")
}
placebos <- list(`1997` = asignar("commid97"), `1993` = asignar("commid93"))
modelos_placebo <- imap(placebos, \(d, a) list(
  feols(dhaz ~ dosis, d, cluster = ~comunidad),
  feols(dhaz ~ dosis + mujer + edad_meses93 + edad_meses93_3 | provincia, d,
        cluster = ~comunidad)
))

resultados_placebo <- imap_dfr(modelos_placebo, \(ms, a) imap_dfr(ms, \(m, i)
  tibble(comunidad_asignada = a, especificacion = i,
         beta = coef(m)[["dosis"]], ee = se(m)[["dosis"]],
         p = pvalue(m)[["dosis"]], ninos = nobs(m),
         comunidades = n_distinct(placebos[[a]]$comunidad[obs(m)]))))
print(resultados_placebo, width = Inf)
stopifnot(all(is.finite(resultados_placebo$beta)))

columnas <- list(modelos_placebo$`1997`[[1]], modelos_placebo$`1997`[[2]],
                 modelos_placebo$`1993`[[1]], modelos_placebo$`1993`[[2]])
vista_placebo <- tibble(
  fila = c("Alza de +100 % en el precio del arroz 1997-2000", "p (EE agrupado)",
           "Edad, sexo y efectos fijos de provincia", "Niños", "Comunidades"),
  !!!set_names(map(1:4, \(j) with(resultados_placebo[j, ], c(
    coef_ee(columnas[[j]], "dosis"), num(p, decimales$estadistico),
    if_else(especificacion == 2, "Sí", "No"),
    num(ninos, decimales$conteo), num(comunidades, decimales$conteo)
  ))), paste0("e", 1:4))
)
tabla_placebo <- vista_placebo |>
  gt(rowname_col = "fila") |>
  tab_spanner("Comunidad de 1997", c(e1, e2)) |>
  tab_spanner("Comunidad de 1993", c(e3, e4)) |>
  cols_label(e1 = "(1)", e2 = "(2)", e3 = "(1)", e4 = "(2)") |>
  estilo_tabla(
    titulo = "Placebo: el alza de 1997-2000 no debería explicar el crecimiento de 1993-1997",
    subtitulo = "Cambio en la talla para la edad (HAZ) 1993-1997 de los niños de 0-5 años en 1993",
    nota = nota_tabla(
      muestra = "cohorte de 0-5 años en 1993 con HAZ válido en 1993 y 1997",
      alcance = "placebo",
      extra = c(
        paste("MCO del cambio en el HAZ (OMS) 1993-1997 sobre la dosis",
              "principal (cambio proporcional del precio nominal del arroz",
              "1997-2000, winsorizado). Entre paréntesis, EE agrupado por",
              "comunidad asignada."),
        paste("El alza se asigna por la comunidad del niño en 1997 (la regla",
              "del análisis principal) o en 1993; solo difieren para quienes",
              "se mudaron. Edad en meses en 1993 y su cubo.")
      )))
guardar_tabla("ninos_placebo", tabla_placebo, resultados_placebo,
              carpeta_salida)

# -----------------------------------------------------------------------------
# 2. Robustez de la especificacion (4) de 06_ate
# -----------------------------------------------------------------------------

pesos <- read_dta("01_Datos/01_Crudos/IFLS3/Household Data/ptrack.dta",
                  col_select = c(pidlink, pw00usxa)) |>
  zap_labels()
stopifnot(!anyDuplicated(pesos$pidlink))

base <- readRDS("01_Datos/03_Listos/base_estimacion.rds") |>
  mutate(edad_meses97_3 = edad_meses97^3, log_p97 = log(p97))
n_base <- nrow(base)
base <- left_join(base, pesos, by = "pidlink")
stopifnot(nrow(base) == n_base)
message("Niños de la base con peso de la evaluación de salud de 2000 positivo: ",
        sum(base$pw00usxa > 0, na.rm = TRUE), " de ", n_base)

# MISMA lista que 06_ate.R: si cambia alla, hay que cambiarla aqui
controles <- c("mujer", "edad_meses97", "edad_meses97_3", "educ_padre",
               "educ_madre", "fumador_padre", "musulman_padre",
               "musulman_madre", "urbano97", "productor_arroz", "tam_hogar",
               "quintil_gasto", "centro_salud", "agua_entubada",
               "via_vehiculos", "via_asfaltada", "parada_bus",
               "sequia_incendio_97", "mercado", "telefono", "correo", "banco",
               "entrevista_1998", grep("^falta_", names(base), value = TRUE))

# especificacion (4) con la dosis que se indique (columna `d`)
estimar <- function(datos, dosis = "dosis", pesos = NULL) {
  feols(dhaz ~ d + log_p97 + .[controles] | provincia,
        mutate(datos, d = .data[[dosis]]), cluster = ~commid97,
        weights = pesos)
}
variantes <- list(
  "Principal (especificación 4 del efecto promedio)" = estimar(base),
  "Sin comunidades con precio de 1998 ni niños medidos en 1998" =
    estimar(filter(base, !precio_1998, !medido_1998)),
  "Con pesos de la evaluación de salud de 2000 (versión a)" =
    estimar(filter(base, pw00usxa > 0), pesos = ~pw00usxa),
  "Alza sin winsorizar" = estimar(base, "dosis_cruda"),
  "Alza con precios solo en kg" =
    estimar(filter(base, !is.na(dosis_kg)), "dosis_kg"),
  "Sin los niños con |ΔHAZ| > 3" = estimar(filter(base, !dhaz_mayor_3))
)
datos_variante <- list(base, filter(base, !precio_1998, !medido_1998),
                       filter(base, pw00usxa > 0), base,
                       filter(base, !is.na(dosis_kg)),
                       filter(base, !dhaz_mayor_3))

resultados_robustez <- imap_dfr(variantes, \(m, v) tibble(
  variante = v, beta = coef(m)[["d"]], ee = se(m)[["d"]], p = pvalue(m)[["d"]],
  ninos = nobs(m)
)) |>
  mutate(comunidades = map2_int(variantes, datos_variante,
                                \(m, d) n_distinct(d$commid97[obs(m)])))
print(resultados_robustez, width = Inf)
message("Referencia de Elmira y Qaim (2026): -0,135 HAZ por +100 % (EE robusto 0,041)")

# chequeo: ninguna variante usa mas ninos que la principal, estimaciones finitas
stopifnot(all(is.finite(resultados_robustez$beta)),
          all(resultados_robustez$ninos <= resultados_robustez$ninos[1]))

tabla_robustez <- resultados_robustez |>
  transmute(variante,
            beta = paste0(num(beta, decimales$z), " (", num(ee, decimales$z), ")"),
            p = num(p, decimales$estadistico),
            ninos = num(ninos, decimales$conteo),
            comunidades = num(comunidades, decimales$conteo)) |>
  gt(rowname_col = "variante") |>
  cols_label(beta = "Alza de +100 % (EE)", p = "p", ninos = "Niños",
             comunidades = "Comunidades") |>
  estilo_tabla(
    titulo = "El efecto del alza del arroz con distintas decisiones de medición y muestra",
    subtitulo = "Cambio en la talla para la edad (HAZ) 1997-2000; cada fila cambia una sola cosa",
    nota = nota_tabla(
      muestra = "base lista", alcance = "contraste",
      extra = c(
        paste("Especificación (4) del efecto promedio: controles de 1997,",
              "efectos fijos de provincia y log del precio de 1997; EE",
              "agrupado por comunidad entre paréntesis."),
        paste("Precio de 1998: comunidades cuyo precio de 1997 se levantó en",
              "1998. Pesos: transversales de la evaluación de salud de la IFLS",
              "2000 (versión a; RAND publica también la b y no recomienda una).",
              "Solo en kg: comunidades con reportes en kg en los dos años."),
        paste("Referencia: Elmira y Qaim (2026) estiman −0,135 (EE robusto",
              "0,041) con otra medida del precio.")
      )))
guardar_tabla("ninos_robustez", tabla_robustez, resultados_robustez,
              carpeta_salida)
