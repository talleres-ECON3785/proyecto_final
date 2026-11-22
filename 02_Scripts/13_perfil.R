# =============================================================================
# 13_perfil: P4.3, perfil de los ninos que prioriza el bosque
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Pregunta 3, entregable para el cliente: con el bosque de 10_bosque, efecto
# predicho para cada nino (tau-hat fuera de la bolsa; tercil alto frente a
# bajo del alza). Cuartiles de tau-hat entre ninos: cuartil 1 = tau-hat mas
# negativo = mas dano predicho = los que el bosque priorizaria primero. Tabla
# de las X de 1997 por cuartil, con variables que el cliente observa.
# Descriptivo: describe a quien ordena primero el bosque, no prueba que ellos
# sufrieron mas (eso lo dirian la calibracion y el RATE).
#
# Entradas: 01_Datos/03_Listos/bosque_terciles.rds
# Salidas:  03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "13_perfil"

guardado <- readRDS("01_Datos/03_Listos/bosque_terciles.rds")
bosque <- guardado$bosque
d <- guardado$datos |>
  mutate(tau = predict(bosque)$predictions,
         cuartil_tau = ntile(tau, 4))

# medias por cuartil (los NA de los moderadores no cuentan en su media)
perfil <- d |>
  group_by(cuartil_tau) |>
  summarise(
    tau_medio = mean(tau), tau_min = min(tau), tau_max = max(tau),
    ninos = n(), comunidades = n_distinct(commid97),
    tercil_alto = mean(w),
    edad_meses = mean(edad_meses97),
    edad_3_5 = mean(edad_meses97 >= 36),
    urbano = mean(urbano97),
    madre_mas_primaria = mean(madre_mas_primaria, na.rm = TRUE),
    mujer = mean(mujer),
    comprador_neto = mean(comprador_neto, na.rm = TRUE),
    pobre = mean(pobre, na.rm = TRUE),
    productor_arroz = mean(productor_arroz),
    tam_hogar = mean(tam_hogar),
    gasto_pc_mediana = median(gasto_pc, na.rm = TRUE),
    .groups = "drop"
  )
print(perfil, width = Inf)
stopifnot(sum(perfil$ninos) == nrow(d))

# tabla: filas = caracteristicas, columnas = cuartiles
num <- function(x, k) formatC(x, format = "f", digits = k, big.mark = ".",
                              decimal.mark = ",")
pct <- function(x) paste0(num(100 * x, decimales$porcentaje), " %")
filas <- list(
  "Efecto predicho medio (HAZ)" = \(p) num(p$tau_medio, decimales$z),
  "Rango del efecto predicho" = \(p) paste0(num(p$tau_min, 2), " a ",
                                            num(p$tau_max, 2)),
  "Edad en 1997 (meses)" = \(p) num(p$edad_meses, 1),
  "3-5 años en 1997" = \(p) pct(p$edad_3_5),
  "Urbano" = \(p) pct(p$urbano),
  "Madre con más que primaria" = \(p) pct(p$madre_mas_primaria),
  "Mujer" = \(p) pct(p$mujer),
  "Comprador neto de arroz" = \(p) pct(p$comprador_neto),
  "Pobre" = \(p) pct(p$pobre),
  "Productor de arroz" = \(p) pct(p$productor_arroz),
  "Tamaño del hogar" = \(p) num(p$tam_hogar, 1),
  "Gasto per cápita mensual, mediana (Rp nominales de 1997)" =
    \(p) num(p$gasto_pc_mediana, decimales$rupias),
  "En comunidad del tercil alto del alza" = \(p) pct(p$tercil_alto),
  "Niños" = \(p) num(p$ninos, 0),
  "Comunidades" = \(p) num(p$comunidades, 0)
)
vista <- tibble(fila = names(filas),
                !!!set_names(map(1:4, \(q) map_chr(filas, \(f) f(perfil[q, ]))),
                             paste0("q", 1:4)))

tabla <- vista |>
  gt(rowname_col = "fila") |>
  cols_label(q1 = "Cuartil 1 (más daño predicho)", q2 = "Cuartil 2",
             q3 = "Cuartil 3", q4 = "Cuartil 4 (menos daño predicho)") |>
  cols_width(everything() ~ px(150)) |>
  estilo_tabla(
    titulo = "¿A quién prioriza el bosque? Perfil por cuartil del efecto predicho",
    subtitulo = "Características de 1997 de los niños, según el efecto predicho por el bosque",
    nota = nota_tabla(
      n = nrow(d), comunidades = n_distinct(d$commid97),
      muestra = "terciles alto y bajo del alza", alcance = "descriptivo",
      extra = c(
        paste("Efecto predicho: τ̂ del bosque causal (tercil alto frente a",
              "bajo del alza), fuera de la bolsa. Cuartiles entre niños;",
              "una comunidad puede tener niños en varios cuartiles."),
        paste("Describe a quién ordenaría primero el bosque, no prueba que",
              "esos niños sufrieran más: la prueba de calibración no encuentra",
              "heterogeneidad (12_calibracion). Porcentajes sin los niños sin",
              "dato de esa variable.")
      )))
guardar_tabla("ninos_perfil_cuartil_tau", tabla, perfil, carpeta_salida)
