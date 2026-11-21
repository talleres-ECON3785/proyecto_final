# =============================================================================
# 03_x_1997: caracteristicas de 1997 (X) de la cohorte principal
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Controles del cuadro A1 de Elmira y Qaim (2026) sin los cinco programas de la
# red de seguridad social, moderadores pre-registrados (urbano, educacion de la
# madre, sexo, comprador neto, pobre) e indicador de entrevista en 1998. Todo
# medido en 1997. La edad en meses la calcula 04_haz (fecha de medicion).
# Las definiciones operativas estan en registro_decisiones.md, seccion 5.
#
# Entradas: 01_Datos/02_Procesados/tracks.rds; IFLS2 bk_ar1, bk_cov, b1_ks0-3,
#           b2_kr, b3b_km, b3p_km, bk1, bk1_a, bk1_e2, bk1_j; ptrack de IFLS3
# Salida:   01_Datos/02_Procesados/x_1997.rds (una fila por nino de cohorte_97
#           con commid97)
# =============================================================================

# los paquetes los carga 00_main.R con pacman

# los .dta de 1997 traen los faltantes como 1,75e+100 tambien con haven
na100 <- function(x) if (is.numeric(x)) replace(x, x > 1e99, NA) else x
leer <- function(archivo) {
  read_dta(file.path("01_Datos/01_Crudos", archivo)) |>
    zap_labels() |>
    mutate(across(everything(), na100))
}
hogar97 <- "IFLS2/Household Data"
comunidad97 <- "IFLS2/Community Data"

ninos <- readRDS("01_Datos/02_Procesados/tracks.rds") |>
  filter(cohorte_97, !is.na(commid97)) |>
  select(pidlink, hhid97, pid97, sex, commid97, prov97, urbano97)

# -----------------------------------------------------------------------------
# 1. Padres (roster de 1997): ar10/ar11 = pid97 del padre/madre si vive en el
#    hogar; 51 y 52 = no vive en el hogar o murio
# -----------------------------------------------------------------------------

# ar16: 1 ninguna, 90 kinder, 2 primaria, 3-6 secundaria, 7-9 superior; el
# resto (otra, educacion de adultos, escuela islamica, no sabe) queda NA
nivel_educ <- function(ar16) {
  case_when(ar16 %in% c(1, 90) ~ "ninguna", ar16 == 2 ~ "primaria",
            ar16 %in% 3:6 ~ "secundaria", ar16 %in% 7:9 ~ "superior")
}

roster <- leer(file.path(hogar97, "hh97bk/bk_ar1.dta")) |>
  select(hhid97, pid97, pidlink, ar10, ar11, ar15, ar16)
stopifnot(!anyDuplicated(roster[c("hhid97", "pid97")]))

# fumador hoy: alguna vez tuvo el habito de tabaco y no lo ha dejado
tabaco <- bind_rows(leer(file.path(hogar97, "hh97b3/b3b_km.dta")),
                    leer(file.path(hogar97, "hh97b3/b3p_km.dta"))) |>
  distinct(pidlink, .keep_all = TRUE) |>
  transmute(pidlink, fumador = km01a == 1 & km04 %in% 1)

padres <- roster |>
  left_join(tabaco, by = "pidlink") |>
  transmute(hhid97, pid_padre = pid97, educ = nivel_educ(ar16),
            musulman = ar15 == 1, fumador)

n_antes <- nrow(ninos)
ninos <- ninos |>
  left_join(select(roster, hhid97, pid97, ar10, ar11), by = c("hhid97", "pid97")) |>
  left_join(rename_with(padres, \(v) paste0(v, "_madre"), -c(hhid97, pid_padre)),
            by = c("hhid97", "ar11" = "pid_padre")) |>
  left_join(rename_with(padres, \(v) paste0(v, "_padre"), -c(hhid97, pid_padre)),
            by = c("hhid97", "ar10" = "pid_padre")) |>
  mutate(madre_ausente = !ar11 %in% 1:50, padre_ausente = !ar10 %in% 1:50)
stopifnot(nrow(ninos) == n_antes)

# -----------------------------------------------------------------------------
# 2. Hogar: tamano, arroz, gasto per capita, pobreza y fecha de entrevista
# -----------------------------------------------------------------------------

tam <- leer("IFLS3/Household Data/ptrack.dta") |>
  filter(member97 == 1) |>
  count(hhid97, name = "tam_hogar")

# x == 1: valor reportado; 7/8 (rechazo, no sabe) cuentan como 0 en el gasto
valor <- function(monto, x) if_else(x %in% 1, monto, 0)
ks1 <- leer(file.path(hogar97, "hh97b1/b1_ks1.dta"))
ks2 <- leer(file.path(hogar97, "hh97b1/b1_ks2.dta"))
ks3 <- leer(file.path(hogar97, "hh97b1/b1_ks3.dta"))
ks0 <- leer(file.path(hogar97, "hh97b1/b1_ks0.dta"))
kr <- leer(file.path(hogar97, "hh97b2/b2_kr.dta"))

gasto <- list(
  # alimentos de la ultima semana, comprados y de produccion propia
  ks1 |> group_by(hhid97) |>
    summarise(alimentos = sum(valor(ks02, ks02x) + valor(ks03, ks03x)) * 30 / 7,
              faltante = any(!ks02x %in% 1 | !ks03x %in% 1)),
  # no alimentos del ultimo mes, sin rifas (F1) ni arisan (F2): no son consumo
  ks2 |> filter(!ks2type %in% c("F1", "F2")) |> group_by(hhid97) |>
    summarise(no_alim_mes = sum(valor(ks06, ks06x)),
              faltante = any(!ks06x %in% 1)),
  ks3 |> group_by(hhid97) |>
    summarise(no_alim_anio = sum(valor(ks08, ks08x) + valor(ks09a, ks09ax)) / 12,
              faltante = any(!ks08x %in% 1)),
  ks0 |> transmute(hhid97,
                   educacion = (valor(ks10aa, ks10aax) + valor(ks11aa, ks11aax) +
                                  valor(ks12aa, ks12aax)) / 12,
                   faltante = FALSE),
  # vivienda: arriendo pagado o, si no arrienda, el que pagaria (kr05)
  kr |> transmute(hhid97,
                  vivienda = if_else(kr04x %in% 1, kr04, valor(kr05, kr05x)),
                  faltante = !(kr04x %in% 1 | kr05x %in% 1))
) |>
  bind_rows() |>
  group_by(hhid97) |>
  summarise(gasto_mes = sum(alimentos, no_alim_mes, no_alim_anio, educacion,
                            vivienda, na.rm = TRUE),
            faltante = any(faltante), .groups = "drop") |>
  # solo hogares con el modulo de consumo: sin el, el gasto seria solo vivienda
  filter(hhid97 %in% ks1$hhid97) |>
  inner_join(tam, by = "hhid97") |>
  mutate(gasto_pc = gasto_mes / tam_hogar,
         quintil_gasto = ntile(gasto_pc, 5),
         pobre_q1 = ntile(gasto_pc, 4) == 1)
stopifnot(!anyDuplicated(gasto$hhid97))
message("Hogares con gasto per capita: ", nrow(gasto), " (", sum(gasto$faltante),
        " con algun rubro sin valor, contado como 0)")

# arroz de la ultima semana: comprado (ks02) y de produccion propia (ks03)
arroz <- ks1 |>
  filter(ks1type == "A") |>
  transmute(hhid97,
            productor_arroz = if_else(ks03x %in% 1, ks03 > 0, NA),
            comprador_neto = if_else(ks02x %in% 1 & ks03x %in% 1, ks02 > ks03, NA))
stopifnot(!anyDuplicated(arroz$hhid97))

# lineas regionales de pobreza de diciembre de 1997 (Rp por persona al mes),
# apendice 1, p. 18 (metodo en la seccion IV, p. 5) de: Widyanti, W.,
# Suryahadi, A., Sumarto, S. y Yumna, A. (2009). The Relationship between
# Chronic Poverty and Household Dynamics: Evidence from Indonesia. SMERU
# Working Paper. https://smeru.or.id/sites/default/files/publication/chronicpovertyhouseholddynamics.pdf
# (resumen en 07_Recursos/Articulos/00_hallazgos_articulos.md, seccion 7).
# Provincia con el codigo BPS de los 2 primeros digitos de commid97; Jakarta no
# tiene linea rural (es toda urbana)
lineas <- tribble(
  ~prov97, ~linea_urbana, ~linea_rural,
  12, 39496, 38260,  # Sumatra del Norte
  13, 36275, 32811,  # Sumatra Occidental
  16, 40381, 37911,  # Sumatra del Sur
  18, 41837, 36881,  # Lampung
  31, 54280, 54280,  # Jakarta
  32, 45892, 40974,  # Java Occidental
  33, 42165, 37329,  # Java Central
  34, 46839, 39213,  # Yogyakarta
  35, 41571, 39737,  # Java Oriental
  51, 46962, 43734,  # Bali
  52, 38909, 40072,  # Nusa Tenggara Occidental
  63, 42768, 37026,  # Kalimantan del Sur
  73, 40949, 38557   # Sulawesi del Sur
)

cobertura <- leer(file.path(hogar97, "hh97bk/bk_cov.dta")) |>
  transmute(hhid97, entrevista_1998 = ivwyr1 %in% 1998)
stopifnot(!anyDuplicated(cobertura$hhid97))

ninos <- ninos |>
  left_join(select(gasto, -faltante, -gasto_mes), by = "hhid97") |>
  left_join(arroz, by = "hhid97") |>
  left_join(cobertura, by = "hhid97") |>
  left_join(lineas, by = "prov97") |>
  mutate(pobre = gasto_pc < if_else(urbano97, linea_urbana, linea_rural)) |>
  select(-linea_urbana, -linea_rural)
stopifnot(nrow(ninos) == n_antes, all(ninos$prov97 %in% lineas$prov97))

# -----------------------------------------------------------------------------
# 3. Comunidad (libro 1 de la comunidad, 1997)
# -----------------------------------------------------------------------------

bk1 <- leer(file.path(comunidad97, "bk1.dta")) |>
  transmute(commid97,
            agua_entubada = c1_1a %in% 1 | c1_1b %in% 1,
            via_vehiculos = a8a == 1,
            via_asfaltada = a8 == 1)

# a0 == 1: el lugar esta dentro de la aldea
lugares <- leer(file.path(comunidad97, "bk1_a.dta")) |>
  filter(atype %in% c("A", "B", "C", "D", "E")) |>
  mutate(lugar = c(A = "parada_bus", B = "mercado", C = "telefono",
                   D = "correo", E = "banco")[atype]) |>
  select(commid97, lugar, en_aldea = a0) |>
  pivot_wider(names_from = lugar, values_from = en_aldea,
              values_fn = \(a0) any(a0 == 1))

salud <- leer(file.path(comunidad97, "bk1_j.dta")) |>
  filter(jtype == "A") |>
  transmute(commid97, centro_salud = j26 > 0)

# incendio (1) o sequia (5) registrados como evento de 1997
eventos <- leer(file.path(comunidad97, "bk1_e2.dta")) |>
  group_by(commid97) |>
  summarise(sequia_incendio_97 = any(e10evt %in% c(1, 5) & e10a %in% 1997))

comunidad <- bk1 |>
  left_join(lugares, by = "commid97") |>
  left_join(salud, by = "commid97") |>
  left_join(eventos, by = "commid97") |>
  mutate(sequia_incendio_97 = coalesce(sequia_incendio_97, FALSE))
stopifnot(!anyDuplicated(comunidad$commid97))

x_1997 <- ninos |>
  left_join(comunidad, by = "commid97") |>
  mutate(mujer = sex == 3,
         madre_mas_primaria = if_else(is.na(educ_madre), NA,
                                      educ_madre %in% c("secundaria", "superior"))) |>
  select(-sex, -ar10, -ar11)
stopifnot(nrow(x_1997) == n_antes)

saveRDS(x_1997, "01_Datos/02_Procesados/x_1997.rds")

# -----------------------------------------------------------------------------
# 4. Resumen para la bitacora: faltantes y proporciones de los moderadores
# -----------------------------------------------------------------------------

message("Ninos: ", nrow(x_1997), " en ", n_distinct(x_1997$commid97), " comunidades")
message("Faltantes por variable:")
print(sort(colSums(is.na(x_1997))[colSums(is.na(x_1997)) > 0], decreasing = TRUE))
message("Proporcion de cada moderador (entre los ninos con dato):")
x_1997 |>
  summarise(across(c(urbano97, madre_mas_primaria, mujer, comprador_neto,
                     productor_arroz, pobre, pobre_q1, entrevista_1998,
                     madre_ausente),
                   \(v) round(mean(v, na.rm = TRUE), 3))) |>
  pivot_longer(everything(), names_to = "variable", values_to = "proporcion") |>
  print()
