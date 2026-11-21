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
#           03_Resultados/Tablas/05_base/ninos_desgaste_alza.{png,csv},
#           ninos_desgaste_alza_pendientes.csv, ninos_haz1997_motivos,
#           ninos_haz1997_balance y ninos_dhaz_cola (.png y .csv; P1.6)
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
  select(pidlink, res97us) |>
  inner_join(x_1997, by = "pidlink") |>
  left_join(select(haz, pidlink, haz97, haz00, talla97, edad_meses97, medido_1998),
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
         # para la robustez de P2.3 sin la cola (decision del 20-nov)
         dhaz_mayor_3 = abs(dhaz) > 3,
         across(all_of(controles_logicos), is.na, .names = "falta_{.col}"),
         across(all_of(controles_logicos), \(v) coalesce(v, FALSE)),
         falta_tam_hogar = is.na(tam_hogar),
         tam_hogar = coalesce(tam_hogar, median(tam_hogar, na.rm = TRUE)),
         across(c(educ_madre, educ_padre), \(v) coalesce(v, "falta")),
         quintil_gasto = coalesce(as.character(quintil_gasto), "falta")) |>
  select(-retenido, -con_precio, -fumador_madre, -res97us, -talla97) |>
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
  mutate(evaluado_1997 = res97us %in% 1, haz_1997 = !is.na(haz97),
         haz_2000 = retenido)
medidos_97 <- filter(con_precio, haz_1997)

# cada paso, sin y con efectos fijos de provincia (P1.6: la brecha es sobre
# todo entre provincias)
pasos <- tribble(
  ~paso, ~variable, ~datos,
  "Retenido (HAZ en 1997 y 2000)", "retenido", list(con_precio),
  "Evaluación de salud en 1997", "evaluado_1997", list(con_precio),
  "HAZ en 1997", "haz_1997", list(con_precio),
  "HAZ en 2000, de los medidos en 1997", "haz_2000", list(medidos_97)
)
pendientes <- expand_grid(pasos, efectos_provincia = c(FALSE, TRUE)) |>
  pmap_dfr(\(paso, variable, datos, efectos_provincia) {
    formula <- paste0("as.numeric(", variable, ") ~ dosis",
                      if (efectos_provincia) " | provincia" else "")
    m <- feols(as.formula(formula), datos[[1]], cluster = ~commid97)
    tibble(paso, efectos_provincia, pendiente = coef(m)[["dosis"]],
           ee_agrupado = se(m)[["dosis"]], p_valor = pvalue(m)[["dosis"]])
  })
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
  mutate(texto = sprintf("%s%s: %.3f (EE %.3f; p = %.3f)", paso,
                         if_else(efectos_provincia, ", con EF de provincia", ""),
                         pendiente, ee_agrupado, p_valor)) |>
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

# -----------------------------------------------------------------------------
# 4. P1.6: por que falta el HAZ de 1997, balance de los que faltan y cola del
#    cambio en el HAZ
# -----------------------------------------------------------------------------

# motivo excluyente, en el orden en que se pierde al nino
motivos <- con_precio |>
  mutate(motivo = case_when(haz_1997 ~ "con_haz",
                            !evaluado_1997 ~ "sin_evaluacion",
                            is.na(talla97) ~ "evaluado_sin_talla",
                            is.na(edad_meses97) ~ "sin_fecha",
                            TRUE ~ "fuera_de_6"))
tabla_motivos <- bind_rows(motivos, mutate(motivos, cuartil = 5)) |>
  mutate(cuartil = if_else(cuartil == 5, "Todos", paste("Cuartil", cuartil))) |>
  count(cuartil, motivo) |>
  group_by(cuartil) |>
  mutate(ninos = sum(n), pct = round(100 * n / ninos, 1)) |>
  select(-n) |>
  pivot_wider(names_from = motivo, values_from = pct, values_fill = 0) |>
  ungroup() |>
  select(cuartil, ninos, con_haz, sin_evaluacion, evaluado_sin_talla, sin_fecha,
         fuera_de_6)
print(tabla_motivos)

tabla <- tabla_motivos |>
  gt() |>
  cols_label(cuartil = "Alza del precio", ninos = "Niños", con_haz = "Con HAZ",
             sin_evaluacion = "Sin evaluación de salud",
             evaluado_sin_talla = "Evaluado sin talla",
             sin_fecha = "Sin fecha de nacimiento o de medición",
             fuera_de_6 = "HAZ fuera de ±6") |>
  fmt_number(ninos, decimals = decimales$conteo) |>
  fmt_number(-c(cuartil, ninos), decimals = decimales$porcentaje) |>
  estilo_tabla(
    titulo = "Por qué falta el HAZ de 1997, según el alza",
    subtitulo = "Porcentaje de niños por motivo excluyente, en el orden en que se pierden",
    nota = nota_tabla(muestra = "cohorte principal con precio en su comunidad",
                      alcance = "descriptivo"))
guardar_tabla("ninos_haz1997_motivos", tabla, tabla_motivos, carpeta_salida)

# las X de 1997 de quienes tienen y no tienen HAZ en 1997: si su diferencia
# cambia con el alza (interaccion), la seleccion depende del tratamiento
balance <- c(pobre = "Pobre", urbano97 = "Urbano",
             madre_mas_primaria = "Madre con más que primaria",
             comprador_neto = "Comprador neto de arroz", mujer = "Mujer") |>
  imap_dfr(\(etiqueta, v) {
    m <- feols(as.formula(paste0("as.numeric(", v, ") ~ haz_1997 * dosis | provincia")),
               con_precio, cluster = ~commid97)
    tibble(variable = etiqueta,
           con_haz = mean(con_precio[[v]][con_precio$haz_1997], na.rm = TRUE),
           sin_haz = mean(con_precio[[v]][!con_precio$haz_1997], na.rm = TRUE),
           interaccion = coef(m)[["haz_1997TRUE:dosis"]],
           ee_agrupado = se(m)[["haz_1997TRUE:dosis"]],
           p_valor = pvalue(m)[["haz_1997TRUE:dosis"]])
  })
print(balance)

tabla <- balance |>
  gt() |>
  cols_label(variable = "", con_haz = "Con HAZ en 1997", sin_haz = "Sin HAZ en 1997",
             interaccion = "Con HAZ × dosis", ee_agrupado = "EE agrupado",
             p_valor = "p") |>
  fmt_percent(c(con_haz, sin_haz), decimals = decimales$porcentaje) |>
  fmt_number(c(interaccion, ee_agrupado, p_valor), decimals = decimales$estadistico) |>
  estilo_tabla(
    titulo = "Características de 1997 de los niños con y sin HAZ en 1997",
    subtitulo = "¿La diferencia cambia con el alza del precio?",
    nota = nota_tabla(
      muestra = "cohorte principal con precio en su comunidad",
      alcance = "descriptivo",
      extra = paste("Interacción: MCO de la característica sobre «con HAZ en",
                    "1997» × dosis, con efectos fijos de provincia y EE",
                    "agrupado por comunidad.")))
guardar_tabla("ninos_haz1997_balance", tabla, balance, carpeta_salida)

# cola del cambio en el HAZ, por cuartil, y perfil de quienes caen en ella
cola <- bind_rows(base, mutate(base, cuartil = 5)) |>
  group_by(cuartil = if_else(cuartil == 5, "Todos", paste("Cuartil", cuartil))) |>
  summarise(ninos = n(), mayor_2 = sum(abs(dhaz) > 2),
            mayor_2_pct = round(100 * mean(abs(dhaz) > 2), 1),
            mayor_3 = sum(dhaz_mayor_3), mayor_3_pct = round(100 * mean(dhaz_mayor_3), 1))
perfil_cola <- base |>
  group_by(grupo = if_else(dhaz_mayor_3, "|ΔHAZ| > 3", "|ΔHAZ| ≤ 3")) |>
  summarise(ninos = n(), edad_meses_1997 = round(mean(edad_meses97), 1),
            haz_1997 = round(mean(haz97), 3), haz_2000 = round(mean(haz00), 3))
print(cola)
print(perfil_cola)

texto_perfil <- with(perfil_cola, sprintf(
  "%s: %d niños, edad media en 1997 de %.1f meses, HAZ medio de %.3f en 1997 y %.3f en 2000.",
  grupo, ninos, edad_meses_1997, haz_1997, haz_2000))
tabla <- cola |>
  gt() |>
  cols_label(cuartil = "Alza del precio", ninos = "Niños en la base",
             mayor_2 = "|ΔHAZ| > 2", mayor_2_pct = "(%)",
             mayor_3 = "|ΔHAZ| > 3", mayor_3_pct = "(%)") |>
  fmt_number(c(ninos, mayor_2, mayor_3), decimals = decimales$conteo) |>
  fmt_number(ends_with("_pct"), decimals = decimales$porcentaje) |>
  estilo_tabla(
    titulo = "La cola del cambio en el HAZ, 1997-2000",
    subtitulo = "Niños con cambios grandes en la talla para la edad, según el alza",
    nota = nota_tabla(muestra = "base lista", alcance = "descriptivo",
                      extra = c(texto_perfil,
                                "Decisión del 20-nov: se mantienen en la estimación principal; robustez sin |ΔHAZ| > 3.")))
guardar_tabla("ninos_dhaz_cola", tabla, cola, carpeta_salida)
write_csv(perfil_cola, file.path("03_Resultados/Tablas", carpeta_salida,
                                 "ninos_dhaz_cola_perfil.csv"))
