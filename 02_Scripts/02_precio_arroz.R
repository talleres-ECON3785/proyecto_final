# =============================================================================
# 02_precio_arroz: precio del arroz por comunidad, 1997 y 2000, y el alza
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Reglas de registro_decisiones.md, seccion 4: solo las fuentes presentes en
# 1997 y 2000 (posyandu y tiendas/mercados), reportes en Rp/kg de todas las
# calidades, mediana por comunidad y anio, cambio proporcional nominal
# winsorizado p1/p99 entre comunidades. Los reportes por litro del posyandu se
# pasan a kg con un factor estimado en los mismos datos (decision del 20-nov);
# dosis_kg repite el calculo solo con reportes en kg, para la robustez. Cuartiles y terciles tambien entre
# comunidades (la comunidad es la unidad del tratamiento).
#
# Entradas: 01_Datos/01_Crudos/IFLS{2,3}/Community Data/{pos_h,bk2_hpj}.dta
#           y las portadas IFLS2 bk2.dta y pos.dta (fechas de 1997-98)
# Salidas:  01_Datos/02_Procesados/precio_arroz.rds
#           03_Resultados/Figuras/02_precio_arroz/comunidades_distribucion_alza.png
#           03_Resultados/Tablas/02_precio_arroz/comunidades_resumen_precio.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R") # carga tambien el de graficas
carpeta_salida <- "02_precio_arroz"

# los comunitarios de 1997 traen los faltantes como 1,75e+100 tambien con haven
na100 <- function(x) if (is.numeric(x)) replace(x, x > 1e99, NA) else x
leer <- function(ola, archivo) {
  read_dta(file.path("01_Datos/01_Crudos", ola, "Community Data", archivo)) |>
    zap_labels() |>
    mutate(across(everything(), na100))
}

# las 312 comunidades IFLS de 1997 (una fila por comunidad en el libro 2)
bk2_97 <- leer("IFLS2", "bk2.dta")
stopifnot(!anyDuplicated(bk2_97$commid97), nrow(bk2_97) == 312)

# -----------------------------------------------------------------------------
# 1. Reportes de precio (htype 1-3 = arroz de calidad alta, media y baja;
#    hpj3type 1 = arroz de calidad media; unidad 1 = kg, 2 = litro; x == 1 =
#    respuesta valida). Tiendas y mercados siempre reportan por kg
# -----------------------------------------------------------------------------

# el posyandu se une a la comunidad por los 4 primeros digitos de fcode; un
# fcode repetido duplica filas exactas, de ahi el distinct()
pos97 <- leer("IFLS2", "pos_h.dta") |>
  distinct() |>
  filter(htype %in% 1:3, h01x %in% 1, h02 %in% 1:2) |>
  transmute(commid97 = substr(fcode, 1, 4), anio = 1997, unidad = h02,
            precio = h01)

mer97 <- leer("IFLS2", "bk2_hpj.dta") |>
  filter(hpj3type == 1, hpj5x %in% 1) |>
  transmute(commid97, anio = 1997, unidad = 1, precio = hpj5)

# en 2000 h01x viene vacio: solo se descartan los codigos 99998/99999
pos00 <- leer("IFLS3", "pos_h.dta") |>
  filter(htype %in% c("1", "2", "3"), h02 %in% 1:2, h01 < 99998) |>
  transmute(commid97 = commid00, anio = 2000, unidad = h02, precio = h01)

# en 2000 bk2_hpj es ancho: un bloque de columnas por comerciante
arroz00 <- leer("IFLS3", "bk2_hpj.dta") |> filter(hpj3type == 1)
mer00 <- bind_rows(
  transmute(arroz00, commid97 = commid00, valido = hpj5x,  precio = hpj5),
  transmute(arroz00, commid97 = commid00, valido = hpj13x, precio = hpj13),
  transmute(arroz00, commid97 = commid00, valido = hpj21x, precio = hpj21)
) |>
  filter(valido %in% 1) |>
  transmute(commid97, anio = 2000, unidad = 1, precio)

reportes <- bind_rows(pos97, mer97, pos00, mer00) |>
  filter(precio > 0, commid97 %in% bk2_97$commid97)
stopifnot(all(reportes$precio < 99998))
reportes |> count(anio, unidad) |> print()

# factor litro -> kg: mediana, entre las comunidades-anio con reportes en las
# dos unidades, de (mediana Rp/litro) / (mediana Rp/kg). El mismo en los dos
# anios: como la dosis es un cociente, solo pesa si la comunidad cambia de unidad
pares <- reportes |>
  group_by(commid97, anio, unidad) |>
  summarise(p = median(precio), .groups = "drop") |>
  pivot_wider(names_from = unidad, values_from = p, names_prefix = "u") |>
  filter(!is.na(u1), !is.na(u2))
factor_litro <- median(pares$u2 / pares$u1)
message("Factor litro -> kg: ", round(factor_litro, 3), " (", nrow(pares),
        " comunidades-anio con las dos unidades)")
reportes <- mutate(reportes, precio_kg = if_else(unidad == 2,
                                                 precio / factor_litro, precio))

# -----------------------------------------------------------------------------
# 2. Mediana por comunidad y anio; solo comunidades con precio en los dos
# -----------------------------------------------------------------------------

resumir <- function(datos) {
  datos |>
    group_by(commid97, anio) |>
    summarise(p = median(precio_kg), n = n(), .groups = "drop") |>
    pivot_wider(names_from = anio, values_from = c(p, n)) |>
    rename(p97 = p_1997, p00 = p_2000, n97 = n_1997, n00 = n_2000)
}
winsorizar <- function(x) {
  pmin(pmax(x, quantile(x, 0.01, na.rm = TRUE)), quantile(x, 0.99, na.rm = TRUE))
}

por_comunidad <- resumir(reportes)
stopifnot(!anyDuplicated(por_comunidad$commid97))

# robustez: solo reportes en kg (NA en las comunidades sin kg en los dos anios)
solo_kg <- resumir(filter(reportes, unidad == 1)) |>
  filter(!is.na(p97), !is.na(p00)) |>
  transmute(commid97, dosis_kg = winsorizar((p00 - p97) / p97))

sin_precio <- tibble(commid97 = bk2_97$commid97) |>
  left_join(por_comunidad, by = "commid97") |>
  summarise(sin_1997 = sum(is.na(p97) & !is.na(p00)),
            sin_2000 = sum(!is.na(p97) & is.na(p00)),
            sin_ambos = sum(is.na(p97) & is.na(p00)))
message("Comunidades perdidas de las 312 por falta de precio:")
print(sin_precio)

# -----------------------------------------------------------------------------
# 3. Tratamiento: dosis, cuartiles y terciles
# -----------------------------------------------------------------------------

# precio levantado en 1998: libro 2 (tiendas y mercados) o algun posyandu
# (decision del 20-nov: la union de las dos fuentes)
pos_cov <- leer("IFLS2", "pos.dta")
comunidades_1998 <- union(bk2_97$commid97[bk2_97$ivwyr1 %in% 1998],
                          substr(pos_cov$fcode[pos_cov$ivwyr1 %in% 1998], 1, 4))
stopifnot(length(comunidades_1998) == 38)

precio <- por_comunidad |>
  filter(!is.na(p97), !is.na(p00)) |>
  mutate(provincia = substr(commid97, 1, 2),
         dosis_cruda = (p00 - p97) / p97,
         dosis = winsorizar(dosis_cruda),
         cuartil = ntile(dosis, 4),
         tercil_nac = ntile(dosis, 3),
         precio_1998 = commid97 %in% comunidades_1998) |>
  group_by(provincia) |>
  mutate(tercil_prov = ntile(dosis, 3)) |>
  ungroup() |>
  left_join(solo_kg, by = "commid97") |>
  relocate(commid97, provincia)
stopifnot(!anyNA(precio$dosis), !anyDuplicated(precio$commid97))

message("Comunidades con precio en 1997 y 2000: ", nrow(precio),
        " (", sum(precio$precio_1998), " con precio de 1997 levantado en 1998; ",
        sum(!is.na(precio$dosis_kg)), " con precio en kg en los dos anios)")
message("Correlacion entre dosis y dosis solo kg: ",
        round(cor(precio$dosis, precio$dosis_kg, use = "complete.obs"), 3))
message("Mediana nacional del precio (Rp/kg): 1997 = ", median(precio$p97),
        "; 2000 = ", median(precio$p00))
message("Cambio proporcional sin winsorizar:")
print(summary(precio$dosis_cruda))
message("Cortes de la winsorizacion (p1, p99): ",
        paste(round(range(precio$dosis), 3), collapse = ", "))

# con esto se decidio (20-nov) usar los terciles dentro de provincia en el
# bosque; los nacionales quedan como robustez
message("R2 de la dosis sobre la provincia: ",
        round(summary(lm(dosis ~ provincia, precio))$r.squared, 3))
message("Comunidades con tercil distinto (nacional frente a provincia): ",
        sum(precio$tercil_nac != precio$tercil_prov))
print(count(precio, provincia, tercil_nac) |>
        pivot_wider(names_from = tercil_nac, values_from = n,
                    names_prefix = "tercil_", values_fill = 0))

saveRDS(precio, "01_Datos/02_Procesados/precio_arroz.rds")

# -----------------------------------------------------------------------------
# 4. Figura: distribucion del alza entre comunidades
# -----------------------------------------------------------------------------

figura <- ggplot(precio, aes(dosis)) +
  geom_histogram(binwidth = 0.1, boundary = 0,
                 fill = paleta_categorica[1], color = "white") +
  scale_x_continuous(labels = scales::label_percent()) +
  labs(title = "Alza del precio del arroz por comunidad, 1997-2000",
       subtitle = paste0(subtitulo_descriptivo, " ", nrow(precio),
                         " comunidades."),
       x = "Cambio proporcional del precio nominal (winsorizado p1/p99)",
       y = "Comunidades",
       caption = paste("Mediana por comunidad de los precios por kg del",
                       "posyandu y de tiendas y mercados (litros pasados a kg).")) +
  tema_presentacion
guardar_figura("comunidades_distribucion_alza.png", figura, carpeta_salida)

# -----------------------------------------------------------------------------
# 5. Tabla resumen de la construccion (las cifras que cita la nota de hallazgo)
# -----------------------------------------------------------------------------

resumen <- tribble(
  ~indicador, ~valor,
  "Comunidades IFLS de 1997", 312,
  "Sin precio en 1997 (sí en 2000)", sin_precio$sin_1997,
  "Sin precio en 2000 (sí en 1997)", sin_precio$sin_2000,
  "Sin precio en ninguno de los dos años", sin_precio$sin_ambos,
  "Con precio en 1997 y 2000", nrow(precio),
  "  de ellas, solo con reportes en kg en los dos años", sum(!is.na(precio$dosis_kg)),
  "  de ellas, con precio de 1997 levantado en 1998", sum(precio$precio_1998),
  "Factor litro a kg (precio por litro / precio por kg)", round(factor_litro, 3),
  "Comunidades-año usadas para el factor", nrow(pares),
  "Mediana del precio en 1997 (Rp/kg, nominal)", median(precio$p97),
  "Mediana del precio en 2000 (Rp/kg, nominal)", median(precio$p00),
  "Mediana del alza (cambio proporcional)", round(median(precio$dosis), 3),
  "Corte p1 de la winsorización", round(min(precio$dosis), 3),
  "Corte p99 de la winsorización", round(max(precio$dosis), 3),
  "Máximo del alza sin winsorizar", round(max(precio$dosis_cruda), 3),
  "Correlación entre la dosis y la dosis solo kg",
  round(cor(precio$dosis, precio$dosis_kg, use = "complete.obs"), 3),
  "R² de la dosis sobre la provincia",
  round(summary(lm(dosis ~ provincia, precio))$r.squared, 3),
  "Comunidades en los terciles alto o bajo (dentro de provincia)",
  sum(precio$tercil_prov != 2),
  "Comunidades con tercil distinto (nacional frente a provincia)",
  sum(precio$tercil_nac != precio$tercil_prov)
)

tabla <- resumen |>
  gt() |>
  cols_label(indicador = "", valor = "") |>
  fmt_number(valor, decimals = 3, drop_trailing_zeros = TRUE) |>
  estilo_tabla(
    titulo = "Construcción del precio del arroz por comunidad",
    subtitulo = "Posyandu y tiendas y mercados, 1997 y 2000",
    nota = nota_tabla(comunidades = nrow(precio), muestra = "comunidades IFLS",
                      alcance = "descriptivo"))
guardar_tabla("comunidades_resumen_precio", tabla, resumen, carpeta_salida)
