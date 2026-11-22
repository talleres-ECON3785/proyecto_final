# =============================================================================
# 11_gate: P3.3, seis GATE pre-declarados con puntajes AIPW del bosque
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Pregunta 2 (¿a quien?). Con el bosque principal de 10_bosque (tercil alto
# frente a bajo del alza dentro de provincia), para cada dimension G1-G6 del
# pre-registro §2:
#   - GATE de cada grupo: average_treatment_effect(bosque, subset = ...);
#   - contraste D = GATE(X = 1) - GATE(X = 0): feols(Gamma ~ X,
#     cluster = ~commid97), con Gamma = get_scores(bosque);
#   - Holm sobre los seis p de D (familia F1, m = 6).
# BLP conjunta con las seis variables: solo descriptiva.
# Escala: HAZ del tercil alto frente al bajo (no por +100 % del precio).
# Convencion: tau < 0 = dano; "mas dano" = tau mas negativo.
#
# Entradas: 01_Datos/03_Listos/bosque_terciles.rds
# Salidas:  03_Resultados/Tablas/11_gate/ninos_gate.{png,csv}
#           03_Resultados/Tablas/11_gate/ninos_blp.{png,csv}
#           03_Resultados/Figuras/11_gate/ninos_gate.png
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "11_gate"

guardado <- readRDS("01_Datos/03_Listos/bosque_terciles.rds")
bosque <- guardado$bosque
d <- guardado$datos |>
  mutate(gamma = get_scores(bosque),
         # G1: X = 1 es 3-5 anios (36-71 meses), al reves que E1 de 09
         edad_3_5 = edad_meses97 >= 36)

dimensiones <- tribble(
  ~id,  ~variable,            ~grupo_1,                     ~grupo_0,
  "G1", "edad_3_5",           "3-5 años en 1997",           "0-2 años",
  "G2", "urbano97",           "Urbano",                     "Rural",
  "G3", "madre_mas_primaria", "Madre con más que primaria", "Primaria o menos",
  "G4", "mujer",              "Mujer",                      "Varón",
  "G5", "comprador_neto",     "Comprador neto de arroz",    "No comprador neto",
  "G6", "pobre",              "Pobre",                      "No pobre"
)

# -----------------------------------------------------------------------------
# 1. GATE por grupo y contraste con los puntajes AIPW
# -----------------------------------------------------------------------------

gate <- pmap_dfr(dimensiones, \(id, variable, grupo_1, grupo_0) {
  x <- d[[variable]]
  ok <- !is.na(x)
  g1 <- average_treatment_effect(bosque, subset = ok & x)
  g0 <- average_treatment_effect(bosque, subset = ok & !x)
  m <- feols(gamma ~ x_1, data = mutate(d[ok, ], x_1 = as.numeric(x[ok])),
             cluster = ~commid97)
  tibble(id, grupo_1, grupo_0,
         gate_1 = g1[["estimate"]], ee_gate_1 = g1[["std.err"]],
         gate_0 = g0[["estimate"]], ee_gate_0 = g0[["std.err"]],
         delta = coef(m)[["x_1"]], ee_delta = se(m)[["x_1"]],
         p_delta = pvalue(m)[["x_1"]],
         ninos_1 = sum(x[ok]), ninos_0 = sum(!x[ok]),
         comunidades_1 = n_distinct(d$commid97[ok & x]),
         comunidades_0 = n_distinct(d$commid97[ok & !x]),
         ninos = sum(ok), comunidades = n_distinct(d$commid97[ok]))
}) |>
  mutate(p_delta_holm = p.adjust(p_delta, "holm"))
print(gate, width = Inf)
stopifnot(nrow(gate) == 6, all(is.finite(gate$delta)))
message("Contrastes que pasan Holm (F1) al 5 %: ", sum(gate$p_delta_holm < 0.05))

# -----------------------------------------------------------------------------
# 2. Tabla de GATE
# -----------------------------------------------------------------------------

num <- function(x, k) formatC(x, format = "f", digits = k)
z <- decimales$z
con_ee <- function(b, e) paste0(num(b, z), " (", num(e, z), ")")
tabla <- gate |>
  transmute(
    id, grupo_1, grupo_0,
    gate_1 = con_ee(gate_1, ee_gate_1), gate_0 = con_ee(gate_0, ee_gate_0),
    delta = con_ee(delta, ee_delta), p = num(p_delta, decimales$estadistico),
    p_holm = num(p_delta_holm, decimales$estadistico),
    n = paste0(num(ninos_1, 0), " / ", num(ninos_0, 0)),
    com = paste0(num(comunidades_1, 0), " / ", num(comunidades_0, 0))
  ) |>
  gt(rowname_col = "id") |>
  cols_label(grupo_1 = "Grupo X = 1", grupo_0 = "Grupo X = 0",
             gate_1 = "GATE X = 1", gate_0 = "GATE X = 0",
             delta = "Δ = X1 − X0", p = "p", p_holm = "p Holm (F1)",
             n = "Niños (X1 / X0)", com = "Comunidades (X1 / X0)") |>
  cols_width(c(grupo_1, grupo_0) ~ px(190), c(gate_1, gate_0, delta) ~ px(140),
             c(n, com) ~ px(130), everything() ~ px(85)) |>
  estilo_tabla(
    titulo = "¿A quién? Efecto del tercil alto del alza por grupo (GATE)",
    subtitulo = paste("Cambio en el HAZ 1997-2000, tercil alto frente a bajo",
                      "del alza; seis grupos pre-declarados"),
    nota = nota_tabla(
      muestra = "terciles alto y bajo del alza", alcance = "contraste",
      extra = c(
        paste("GATE: promedio de los puntajes AIPW del bosque causal (grf,",
              "agrupado por comunidad) en cada grupo, con EE agrupado.",
              "Δ: MCO de los puntajes sobre el indicador del grupo X = 1, EE",
              "agrupado por comunidad. Δ < 0: más daño en el grupo X = 1."),
        paste("p Holm: familia F1 del pre-registro (m = 6), α = 0,05",
              "bilateral. Solo un Δ que pase Holm se lee como diferencia entre",
              "grupos."),
        paste("G1 compara 3-5 años (X = 1) con 0-2 (al revés que la",
              "interacción E1 de la réplica de E-Q). G3, G5 y G6 excluyen a",
              "los niños sin dato de esa variable. Escala: HAZ entre terciles,",
              "no por +100 % del precio.")
      )))
guardar_tabla("ninos_gate", tabla, gate, carpeta_salida)

# -----------------------------------------------------------------------------
# 3. Figura de los GATE
# -----------------------------------------------------------------------------

puntos <- bind_rows(
  transmute(gate, id, grupo = grupo_1, x = "X = 1", gate = gate_1, ee = ee_gate_1),
  transmute(gate, id, grupo = grupo_0, x = "X = 0", gate = gate_0, ee = ee_gate_0)
) |>
  left_join(select(gate, id, p_delta_holm), by = "id") |>
  mutate(panel = paste0(id, " · Holm p = ", num(p_delta_holm, 2)),
         grupo = fct_inorder(grupo))
ate <- average_treatment_effect(bosque)[["estimate"]]

fig <- ggplot(puntos, aes(gate, fct_rev(grupo), color = x)) +
  geom_vline(xintercept = 0, color = gris_secundario) +
  geom_vline(xintercept = ate, linetype = "dashed", color = gris_nota) +
  geom_errorbar(aes(xmin = gate - 1.96 * ee, xmax = gate + 1.96 * ee),
                width = 0.2, orientation = "y") +
  geom_point(size = 2.6) +
  facet_wrap(~panel, ncol = 2, scales = "free_y") +
  scale_color_manual(values = paleta_categorica[1:2], name = NULL) +
  labs(title = "¿A quién? GATE del tercil alto frente al bajo del alza",
       subtitle = paste0(subtitulo_contraste, "\n", nrow(d), " niños en ",
                         n_distinct(d$commid97), " comunidades."),
       x = "Efecto en el cambio del HAZ 1997-2000 (IC 95 %, EE agrupado)",
       y = NULL,
       caption = paste0(
         "Puntajes AIPW del bosque causal (grf). Línea discontinua: ATE del",
         " bosque (", num(ate, z), ").\nHolm: familia F1 (m = 6), sobre Δ =",
         " GATE(X = 1) − GATE(X = 0). Ningún contraste es una diferencia",
         " entre grupos salvo que su p de Holm sea < 0,05.")) +
  tema_presentacion + tema_paneles +
  theme(legend.position = "top", plot.title.position = "plot",
        plot.caption.position = "plot", axis.text.x = element_text(size = 10),
        panel.grid.major.x = element_line(color = gris_grilla, linewidth = 0.3))
guardar_figura("ninos_gate.png", fig, carpeta_salida, height = 7)

# -----------------------------------------------------------------------------
# 4. BLP conjunta (descriptiva)
# -----------------------------------------------------------------------------

a <- d |>
  transmute(edad_3_5, urbano97, madre_mas_primaria, mujer, comprador_neto,
            pobre) |>
  mutate(across(everything(), as.numeric))
completos <- complete.cases(a)
blp <- best_linear_projection(bosque, as.matrix(a[completos, ]),
                              subset = completos)
blp_df <- tibble(termino = rownames(blp), coef = blp[, 1], ee = blp[, 2],
                 ninos = sum(completos),
                 comunidades = n_distinct(d$commid97[completos]))
print(blp_df)
etiquetas <- c("(Intercept)" = "Constante (todos en X = 0)",
               edad_3_5 = "3-5 años en 1997", urbano97 = "Urbano",
               madre_mas_primaria = "Madre con más que primaria",
               mujer = "Mujer", comprador_neto = "Comprador neto de arroz",
               pobre = "Pobre")
tabla_blp <- blp_df |>
  transmute(termino = etiquetas[termino],
            coef = con_ee(coef, ee)) |>
  gt(rowname_col = "termino") |>
  cols_label(coef = "Coeficiente (EE agrupado)") |>
  estilo_tabla(
    titulo = "Mejor proyección lineal del efecto en los seis grupos (descriptiva)",
    subtitulo = "Cambio en el HAZ 1997-2000, tercil alto frente a bajo del alza",
    nota = nota_tabla(
      n = sum(completos), comunidades = n_distinct(d$commid97[completos]),
      muestra = "terciles alto y bajo, sin faltantes en las seis variables",
      alcance = "descriptivo",
      extra = paste("best_linear_projection del bosque causal sobre las seis",
                    "variables a la vez. Descriptiva: fuera de las familias de",
                    "Holm; no se usa para afirmar diferencias entre grupos.")))
guardar_tabla("ninos_blp", tabla_blp, blp_df, carpeta_salida)
