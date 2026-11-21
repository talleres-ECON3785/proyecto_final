# =============================================================================
# 04_haz: talla para la edad (HAZ, OMS) en 1993, 1997 y 2000
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# HAZ de las dos cohortes de 01_tracks con las reglas de registro_decisiones.md,
# seccion 5: estandares OMS (anthro hasta 60 meses, anthroplus desde 61), edad
# = fecha de medicion - fecha de nacimiento, acostado o de pie segun la
# medicion, y HAZ fuera de +-6 excluidos. La fecha de nacimiento es la
# construida en el ptrack de 2000, la misma para todas las olas.
#
# Entradas: 01_Datos/02_Procesados/tracks.rds; IFLS1 bukcca2, IFLS2 bus_1,
#           IFLS3 bus2_1
# Salidas:  01_Datos/02_Procesados/haz.rds (una fila por pidlink)
#           03_Resultados/Tablas/04_haz/cohortes_haz_resumen.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "04_haz"

# los .dta de 1997 traen los faltantes como 1,75e+100 tambien con haven
na100 <- function(x) if (is.numeric(x)) replace(x, x > 1e99, NA) else x
leer <- function(archivo) {
  read_dta(file.path("01_Datos/01_Crudos", archivo)) |>
    zap_labels() |>
    mutate(across(everything(), na100))
}

# fecha con dia faltante (codigos > 31) en el 15 del mes; sin mes, NA
fecha <- function(anio, mes, dia) {
  make_date(anio, if_else(mes %in% 1:12, mes, NA), if_else(dia %in% 1:31, dia, 15))
}

tracks <- readRDS("01_Datos/02_Procesados/tracks.rds") |>
  mutate(nacimiento = fecha(if_else(bth_year < 3000, bth_year, NA), bthmonth, bth_day),
         sexo_oms = if_else(sex == 1, 1, 2))
message("Sin fecha de nacimiento: ", sum(is.na(tracks$nacimiento) & tracks$cohorte_97),
        " de la cohorte principal y ",
        sum(is.na(tracks$nacimiento) & tracks$cohorte_93), " de la placebo")

# -----------------------------------------------------------------------------
# 1. Mediciones por ola, en un mismo formato: talla, acostado, fecha
#    Ojo: el codigo del metodo esta invertido entre olas. 1993 (ca11): 1
#    acostado, 3 de pie. 1997 y 2000 (us05): 1 de pie, 3 acostado
# -----------------------------------------------------------------------------

# person = 96: medidos fuera del roster, sin pidlink propio (guia de 1993)
med93 <- leer("IFLS1/Household Data/bukcca2.dta") |>
  filter(person != 96) |>
  transmute(hhid93, pid93,
            talla = if_else(ca10 > 0 & ca10 < 999, ca10, NA),
            acostado = case_when(ca11 == 1 ~ TRUE, ca11 == 3 ~ FALSE),
            medicion = fecha(1900 + ca09yr, ca09mth, ca09day))

med97 <- leer("IFLS2/Household Data/bus_1.dta") |>
  transmute(hhid97, pid97,
            talla = if_else(us04x %in% 1 & us04 > 0, us04, NA),
            acostado = case_when(us05 == 3 ~ TRUE, us05 == 1 ~ FALSE),
            medicion = fecha(us17yr, us17mth, us17day))

med00 <- leer("IFLS3/Household Data/bus2_1.dta") |>
  transmute(hhid00, pid00,
            talla = if_else(us04x %in% 1 & us04 > 0, us04, NA),
            acostado = case_when(us05 == 3 ~ TRUE, us05 == 1 ~ FALSE),
            medicion = fecha(us17byrb, us17bmtb, us17bdyb))

stopifnot(!anyDuplicated(med93[c("hhid93", "pid93")]),
          !anyDuplicated(med97[c("hhid97", "pid97")]),
          !anyDuplicated(med00[c("hhid00", "pid00")]))

# -----------------------------------------------------------------------------
# 2. HAZ: anthro hasta 1.856 dias (60 meses, con el ajuste de 0,7 cm entre
#    acostado y de pie); anthroplus desde ahi (hasta 228 meses)
# -----------------------------------------------------------------------------

calcular_haz <- function(datos) {
  datos <- mutate(datos,
                  edad_dias = as.numeric(medicion - nacimiento),
                  edad_dias = if_else(edad_dias >= 0, edad_dias, NA),
                  edad_meses = edad_dias / (365.25 / 12))
  menor <- !is.na(datos$edad_dias) & datos$edad_dias <= 1856
  z_menor <- anthro_zscores(sex = datos$sexo_oms, age = datos$edad_dias,
                            lenhei = datos$talla,
                            measure = if_else(datos$acostado, "l", "h"))$zlen
  z_mayor <- anthroplus_zscores(sex = datos$sexo_oms,
                                age_in_months = datos$edad_meses,
                                height_in_cm = datos$talla)$zhfa
  mutate(datos, haz_crudo = if_else(menor, z_menor, z_mayor),
         haz = if_else(abs(haz_crudo) <= 6, haz_crudo, NA))
}

unir <- function(med, llaves) {
  n <- nrow(tracks)
  datos <- left_join(select(tracks, pidlink, all_of(llaves), nacimiento, sexo_oms),
                     med, by = llaves)
  stopifnot(nrow(datos) == n)
  calcular_haz(datos)
}

ola93 <- unir(med93, c("hhid93", "pid93"))
ola97 <- unir(med97, c("hhid97", "pid97"))
ola00 <- unir(med00, c("hhid00", "pid00"))

haz <- tracks |>
  select(pidlink, cohorte_97, cohorte_93, commid93, commid97) |>
  mutate(haz93 = ola93$haz, haz97 = ola97$haz, haz00 = ola00$haz,
         talla93 = ola93$talla, talla97 = ola97$talla, talla00 = ola00$talla,
         edad_meses93 = ola93$edad_meses, edad_meses97 = ola97$edad_meses,
         edad_meses00 = ola00$edad_meses,
         medido_1998 = year(ola97$medicion) %in% 1998)

saveRDS(select(haz, -cohorte_97, -cohorte_93, -commid93, -commid97),
        "01_Datos/02_Procesados/haz.rds")

# -----------------------------------------------------------------------------
# 3. Resumen por cohorte y ola
# -----------------------------------------------------------------------------

# comunidades: de 1997 en la principal y de 1993 en la placebo
resumir <- function(ola, en_cohorte, cohorte, anio, commid) {
  d <- ola[en_cohorte, ]
  tibble(cohorte, anio = as.character(anio),
         con_talla = sum(!is.na(d$talla)),
         con_talla_y_edad = sum(!is.na(d$talla) & !is.na(d$edad_dias)),
         fuera_de_6 = sum(!is.na(d$haz_crudo) & is.na(d$haz)),
         haz_valido = sum(!is.na(d$haz)),
         comunidades = n_distinct(na.omit(commid[en_cohorte][!is.na(d$haz)])),
         edad_media_meses = round(mean(d$edad_meses[!is.na(d$haz)]), 1),
         haz_media = round(mean(d$haz, na.rm = TRUE), 3),
         haz_de = round(sd(d$haz, na.rm = TRUE), 3))
}

principal <- "0-5 años en 1997 (principal)"
placebo <- "0-5 años en 1993 (placebo)"
# las dos olas a la vez, con comunidad IFLS: lo que puede entrar al DHAZ
ambas <- function(en_cohorte, h1, h2, commid, cohorte, anio) {
  ok <- en_cohorte & !is.na(h1) & !is.na(h2) & !is.na(commid)
  tibble(cohorte, anio, haz_valido = sum(ok), comunidades = n_distinct(commid[ok]),
         haz_media = round(mean(h2[ok] - h1[ok]), 3),
         haz_de = round(sd(h2[ok] - h1[ok]), 3))
}
resumen <- bind_rows(
  resumir(ola97, haz$cohorte_97, principal, 1997, haz$commid97),
  resumir(ola00, haz$cohorte_97, principal, 2000, haz$commid97),
  ambas(haz$cohorte_97, haz$haz97, haz$haz00, haz$commid97, principal,
        "1997 y 2000 (cambio)"),
  resumir(ola93, haz$cohorte_93, placebo, 1993, haz$commid93),
  resumir(ola97, haz$cohorte_93, placebo, 1997, haz$commid93),
  ambas(haz$cohorte_93, haz$haz93, haz$haz97, haz$commid93, placebo,
        "1993 y 1997 (cambio)")
)
print(resumen, width = Inf)

tabla <- resumen |>
  gt(groupname_col = "cohorte") |>
  cols_label(anio = "Año", con_talla = "Con talla",
             con_talla_y_edad = "Con talla y edad", fuera_de_6 = "HAZ fuera de ±6",
             haz_valido = "HAZ válido", comunidades = "Comunidades",
             edad_media_meses = "Edad media (meses)",
             haz_media = "HAZ medio", haz_de = "DE del HAZ") |>
  fmt_number(c(con_talla, con_talla_y_edad, fuera_de_6, haz_valido, comunidades),
             decimals = decimales$conteo) |>
  sub_missing(missing_text = "") |>
  fmt_number(c(haz_media, haz_de), decimals = decimales$z) |>
  estilo_tabla(
    titulo = "Talla para la edad de las dos cohortes",
    subtitulo = "Puntaje z de la OMS (anthro hasta 60 meses, anthroplus desde 61)",
    nota = nota_tabla(muestra = "miembros de cada cohorte", alcance = "descriptivo",
                      extra = paste("Edad = fecha de medición menos fecha de",
                                    "nacimiento del ptrack de 2000. Las filas",
                                    "de cada año no exigen comunidad IFLS; las",
                                    "de cambio sí, y su media y DE son las del",
                                    "cambio en el HAZ.")))
guardar_tabla("cohortes_haz_resumen", tabla, resumen, carpeta_salida)
