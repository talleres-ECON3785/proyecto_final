# =============================================================================
# 05_base: base lista para estimar (un nino por fila) y desgaste segun el alza
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Une las bases de 01-04 para la cohorte principal: DHAZ 1997->2000,
# tratamiento (dosis, cuartiles, terciles), X de 1997, commid97 y provincia.
# Los controles con faltantes se completan con un indicador para que feols no
# descarte ninos; los moderadores pre-registrados quedan con sus NA.
# La base NO se versiona (licencia de RAND, repositorio publico): cada
# integrante la regenera con 00_main.R.
#
# Entradas: 01_Datos/02_Procesados/{tracks,precio_arroz,x_1997,haz}.rds
# Salidas:  01_Datos/03_Listos/base_estimacion.rds
#           03_Resultados/Tablas/05_base/ninos_desgaste_alza.{png,csv} y
#           ninos_desgaste_alza_pendientes.csv
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "05_base"

procesados <- "01_Datos/02_Procesados"
tracks <- readRDS(file.path(procesados, "tracks.rds"))
precio <- readRDS(file.path(procesados, "precio_arroz.rds"))
x_1997 <- readRDS(file.path(procesados, "x_1997.rds"))
haz <- readRDS(file.path(procesados, "haz.rds"))
stopifnot(!anyDuplicated(precio$commid97), !anyDuplicated(x_1997$pidlink),
          !anyDuplicated(haz$pidlink))

# -----------------------------------------------------------------------------
# 1. Poblacion de partida y perdidas en orden
# -----------------------------------------------------------------------------

partida <- tracks |>
  filter(cohorte_97, !is.na(commid97)) |>
  select(pidlink) |>
  inner_join(x_1997, by = "pidlink") |>
  left_join(select(haz, pidlink, haz97, haz00, edad_meses97, medido_1998),
            by = "pidlink") |>
  left_join(select(precio, commid97, provincia, p97, dosis, dosis_cruda,
                   dosis_kg, cuartil, tercil_prov, tercil_nac, precio_1998),
            by = "commid97") |>
  mutate(con_precio = !is.na(dosis),
         retenido = con_precio & !is.na(haz97) & !is.na(haz00))
stopifnot(nrow(partida) == nrow(x_1997))

perdidas <- tibble(
  paso = c("Cohorte principal con comunidad IFLS", "Con precio en la comunidad",
           "Con HAZ válido en 1997", "Con HAZ válido en 2000 (base lista)"),
  ninos = c(nrow(partida), sum(partida$con_precio),
            sum(partida$con_precio & !is.na(partida$haz97)), sum(partida$retenido)),
  comunidades = c(n_distinct(partida$commid97),
                  n_distinct(partida$commid97[partida$con_precio]),
                  n_distinct(partida$commid97[partida$con_precio & !is.na(partida$haz97)]),
                  n_distinct(partida$commid97[partida$retenido])))
print(perdidas)

# -----------------------------------------------------------------------------
# 2. Base lista: faltantes de los controles con indicador
# -----------------------------------------------------------------------------

# controles del cuadro A1 de E-Q (sin los programas) que tienen faltantes; los
# moderadores (urbano, madre con mas que primaria, mujer, comprador neto,
# pobre) no se completan
controles_logicos <- c("fumador_padre", "musulman_padre", "musulman_madre",
                       "productor_arroz", "agua_entubada", "via_vehiculos",
                       "via_asfaltada", "parada_bus", "mercado", "telefono",
                       "correo", "banco", "centro_salud", "sequia_incendio_97")

base <- partida |>
  filter(retenido) |>
  mutate(dhaz = haz00 - haz97,
         across(all_of(controles_logicos), is.na, .names = "falta_{.col}"),
         across(all_of(controles_logicos), \(v) coalesce(v, FALSE)),
         falta_tam_hogar = is.na(tam_hogar),
         tam_hogar = coalesce(tam_hogar, median(tam_hogar, na.rm = TRUE)),
         across(c(educ_madre, educ_padre), \(v) coalesce(v, "falta")),
         quintil_gasto = coalesce(as.character(quintil_gasto), "falta")) |>
  select(-retenido, -con_precio, -fumador_madre) |>
  # los indicadores sin ningun faltante no aportan nada
  select(-(starts_with("falta_") & where(\(v) is.logical(v) && !any(v, na.rm = TRUE))))

message("Ninos con algun control completado, por variable:")
print(colSums(select(base, starts_with("falta_"))))

message("Distribucion del cambio en el HAZ:")
print(quantile(base$dhaz, c(0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1)))
message("Ninos con |DHAZ| > 3: ", sum(abs(base$dhaz) > 3))

saveRDS(base, "01_Datos/03_Listos/base_estimacion.rds")

# -----------------------------------------------------------------------------
# 3. Desgaste segun el alza, entre los ninos con precio, separado en dos pasos:
#    tener HAZ en 1997 (antes del alza) y, de esos, tenerlo en 2000
# -----------------------------------------------------------------------------

con_precio <- filter(partida, con_precio) |>
  mutate(haz_1997 = !is.na(haz97), haz_2000 = retenido)
medidos_97 <- filter(con_precio, haz_1997)

pendientes <- list(
  "Retenido (HAZ en 1997 y 2000)" = feols(as.numeric(retenido) ~ dosis,
                                          con_precio, cluster = ~commid97),
  "HAZ en 1997" = feols(as.numeric(haz_1997) ~ dosis, con_precio,
                        cluster = ~commid97),
  "HAZ en 2000, de los medidos en 1997" = feols(as.numeric(haz_2000) ~ dosis,
                                                medidos_97, cluster = ~commid97)
) |>
  imap_dfr(\(m, paso) tibble(paso, pendiente = coef(m)[["dosis"]],
                             ee_agrupado = se(m)[["dosis"]],
                             p_valor = pvalue(m)[["dosis"]]))
print(pendientes)

por_cuartil <- function(d) {
  summarise(d, ninos_1997 = n(), comunidades = n_distinct(commid97),
            en_la_base = sum(retenido),
            retenido_pct = round(100 * mean(retenido), 1),
            haz_1997_pct = round(100 * mean(haz_1997), 1),
            haz_2000_dado_1997_pct = round(100 * mean(haz_2000[haz_1997]), 1),
            .groups = "drop")
}
desgaste <- bind_rows(
  con_precio |> group_by(cuartil = paste("Cuartil", cuartil)) |> por_cuartil(),
  con_precio |> mutate(cuartil = "Todos") |> group_by(cuartil) |> por_cuartil()
)
print(desgaste, width = Inf)

texto_pendientes <- pendientes |>
  mutate(texto = sprintf("%s: %.3f (EE %.3f; p = %.3f)", paso, pendiente,
                         ee_agrupado, p_valor)) |>
  pull(texto)

tabla <- desgaste |>
  gt() |>
  cols_label(cuartil = "Alza del precio", ninos_1997 = "Niños en 1997",
             comunidades = "Comunidades", en_la_base = "En la base",
             retenido_pct = "Retenidos (%)", haz_1997_pct = "Con HAZ en 1997 (%)",
             haz_2000_dado_1997_pct = "Con HAZ en 2000, de los medidos en 1997 (%)") |>
  fmt_number(c(ninos_1997, comunidades, en_la_base), decimals = decimales$conteo) |>
  fmt_number(ends_with("_pct"), decimals = decimales$porcentaje) |>
  estilo_tabla(
    titulo = "Desgaste según el alza del precio del arroz",
    subtitulo = "Niños de 0-5 años en 1997 con precio en su comunidad",
    nota = nota_tabla(
      muestra = "cohorte principal", alcance = "descriptivo",
      extra = c("Retenido = HAZ válido en 1997 y 2000. Pendientes sobre la dosis (MCO, EE agrupado por comunidad):",
                texto_pendientes)))
guardar_tabla("ninos_desgaste_alza", tabla, desgaste, carpeta_salida)
write_csv(pendientes, file.path("03_Resultados/Tablas", carpeta_salida,
                                "ninos_desgaste_alza_pendientes.csv"))
