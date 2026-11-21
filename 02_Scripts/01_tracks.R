# =============================================================================
# 01_tracks: cohortes, comunidad de 1997 y desgaste 1993-2000
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Marca las dos cohortes del analisis y les asigna su comunidad:
#   - cohorte_97 (principal, DHAZ 1997->2000): 0-5 anios y miembro en 1997
#   - cohorte_93 (placebo, DHAZ 1993->1997):   0-5 anios y miembro en 1993
# Usa solo el ptrack/htrack de IFLS3 (2000), que ya trae 1993, 1997 y 2000.
# Guarda la base con todos los miembros de cada cohorte (tambien los que se
# pierden despues): la muestra analitica se arma en P1.5.
#
# Entrada: 01_Datos/01_Crudos/IFLS3/Household Data/{ptrack,htrack}.dta
# Salidas: 01_Datos/02_Procesados/tracks.rds
#          03_Resultados/Tablas/01_tracks/cohortes_desgaste.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "01_tracks"

crudos <- "01_Datos/01_Crudos/IFLS3/Household Data"
ptrack <- zap_labels(read_dta(file.path(crudos, "ptrack.dta")))
htrack <- zap_labels(read_dta(file.path(crudos, "htrack.dta")))
stopifnot(!anyDuplicated(ptrack$pidlink))

# -----------------------------------------------------------------------------
# 1. Comunidad por hogar: htrack tiene una fila por hogar de 2000, asi que un
#    hogar de 1997 que se dividio aparece varias veces; se deja una por llave
# -----------------------------------------------------------------------------

hogar97 <- htrack |>
  filter(hhid97 != "") |>
  distinct(hhid97, commid97, prov97 = sc01_97, urbano97 = sc05_97 == 1)
stopifnot(!anyDuplicated(hogar97$hhid97))

hogar93 <- htrack |>
  filter(hhid93 != "") |>
  distinct(hhid93, commid93)
stopifnot(!anyDuplicated(hogar93$hhid93))

# -----------------------------------------------------------------------------
# 2. Cohortes (definicion de la sintesis de datos, S 4.3)
# -----------------------------------------------------------------------------

tracks <- ptrack |>
  mutate(cohorte_97 = coalesce(age_97 <= 5 & member97 == 1, FALSE),
         cohorte_93 = coalesce(age_93 <= 5 & member93 == 1, FALSE)) |>
  filter(cohorte_97 | cohorte_93) |>
  select(pidlink, sex, bth_year, bthmonth, bth_day, age_93, age_97,
         hhid93, pid93, hhid97, pid97, hhid00, pid00,
         member93, member97, member00, ar01a_00, res93us, res97us, res00us,
         cohorte_97, cohorte_93)

n_antes <- nrow(tracks)
tracks <- tracks |>
  left_join(hogar97, by = "hhid97") |>
  left_join(hogar93, by = "hhid93") |>
  # vacio = hogar fuera de las comunidades IFLS
  mutate(across(c(commid93, commid97), \(x) na_if(x, "")))
stopifnot(nrow(tracks) == n_antes)
# si cambia, la cohorte ya no coincide con S 4.3: revisar antes de seguir
stopifnot(sum(tracks$cohorte_97) == 3851)

saveRDS(tracks, "01_Datos/02_Procesados/tracks.rds")

# -----------------------------------------------------------------------------
# 3. Desgaste por ola: cada paso exige el anterior. "Evaluacion de salud" es
#    que se hizo el modulo US; la talla valida se revisa en 04_haz (P1.4)
# -----------------------------------------------------------------------------

contar <- function(datos, commid, paso) {
  tibble(paso = paso, ninos = nrow(datos),
         comunidades = n_distinct(na.omit(datos[[commid]])))
}

p1 <- filter(tracks, cohorte_97)
p2 <- filter(p1, !is.na(commid97))
p3 <- filter(p2, res97us %in% 1)
p4 <- filter(p3, member00 %in% 1)
p5 <- filter(p4, res00us %in% 1)

q1 <- filter(tracks, cohorte_93)
q2 <- filter(q1, res93us %in% 1)
q3 <- filter(q2, member97 %in% 1)
q4 <- filter(q3, res97us %in% 1)

desgaste <- bind_rows(
  bind_rows(
    contar(p1, "commid97", "Miembros del hogar en 1997"),
    contar(p2, "commid97", "En una comunidad IFLS en 1997"),
    contar(p3, "commid97", "Evaluación de salud en 1997"),
    contar(p4, "commid97", "Miembros del hogar en 2000"),
    contar(p5, "commid97", "Evaluación de salud en 2000"),
    contar(filter(p1, ar01a_00 %in% 0), "commid97",
           "Muertos en 2000 (de los miembros de 1997)")
  ) |> mutate(cohorte = "0-5 años en 1997 (principal)", .before = 1),
  bind_rows(
    contar(q1, "commid93", "Miembros del hogar en 1993"),
    contar(q2, "commid93", "Evaluación de salud en 1993"),
    contar(q3, "commid93", "Miembros del hogar en 1997"),
    contar(q4, "commid93", "Evaluación de salud en 1997")
  ) |> mutate(cohorte = "0-5 años en 1993 (placebo)", .before = 1)
)
print(desgaste, n = Inf)

tabla <- desgaste |>
  gt(groupname_col = "cohorte") |>
  cols_label(paso = "", ninos = "Niños", comunidades = "Comunidades") |>
  fmt_number(c(ninos, comunidades), decimals = decimales$conteo) |>
  estilo_tabla(
    titulo = "Seguimiento de las dos cohortes",
    subtitulo = "Cada fila exige la anterior; comunidad de 1997 (principal) o de 1993 (placebo)",
    nota = nota_tabla(
      muestra = "ptrack y htrack de 2000", alcance = "descriptivo",
      extra = paste("Evaluación de salud = se hizo el módulo de medición (US);",
                    "la validez de la talla se revisa en 04_haz.")))
guardar_tabla("cohortes_desgaste", tabla, desgaste, carpeta_salida)
