# =============================================================================
# 14_rate: P4.2, RATE (AUTOC) del bosque frente a reglas simples
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Pregunta 3 (¿el bosque supera a las reglas simples?), pre-registro §4.
# Misma muestra, X y tratamiento que 10_bosque (tercil alto = 1 frente a bajo
# = 0 del alza dentro de provincia). Particion de las comunidades en dos
# mitades (set.seed(2026)): un bosque entrenado en la mitad 1 predice tau-hat
# en la mitad 2, y un bosque de evaluacion en la mitad 2 da los puntajes
# doblemente robustos con que grf calcula el RATE.
#
# Escala de dano: el bosque de evaluacion usa Y = -dHAZ, asi que su tau es
# dano (positivo = menos talla) y AUTOC > 0 = la regla encuentra a los ninos
# mas danados. Prioridades: bosque = -tau-hat (tau-hat del bosque de la mitad 1,
# entrenado con dHAZ) y reglas 1{pobre}, 1{urbano}, 1{comprador neto}.
# Muestra comun: ninos de la mitad de evaluacion sin NA en las tres reglas.
# Bootstrap de grf (R = 500) agrupado por comunidad y emparejado en las
# diferencias. Holm (familia F3, m = 3) sobre las tres diferencias.
#
# Entradas: 01_Datos/03_Listos/bosque_terciles.rds
# Salidas:  03_Resultados/Tablas/14_rate/ninos_rate.{png,csv}
#           03_Resultados/Figuras/14_rate/ninos_rate_toc.png
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "14_rate"

guardado <- readRDS("01_Datos/03_Listos/bosque_terciles.rds")
x <- guardado$x
d <- guardado$datos

# -----------------------------------------------------------------------------
# 1. Particion por comunidad completa
# -----------------------------------------------------------------------------

set.seed(2026)
comunidades <- sort(unique(d$commid97))
mitad_1 <- sample(comunidades, floor(length(comunidades) / 2))
d$mitad <- if_else(d$commid97 %in% mitad_1, 1L, 2L)
print(summarise(d, ninos = n(), comunidades = n_distinct(commid97), .by = mitad))

bosque_en <- function(filas, y) {
  causal_forest(x[filas, ], y, d$w[filas], clusters = factor(d$commid97[filas]),
                num.trees = 4000, seed = 2026, num.threads = 1)
}

reglas <- c(bosque = "Bosque (−τ̂)", pobre = "Pobre", urbano97 = "Urbano",
            comprador_neto = "Comprador neto")

# -----------------------------------------------------------------------------
# 2. RATE en una mitad de evaluacion, con tau-hat de la otra
# -----------------------------------------------------------------------------

rate_en <- function(entrena, evalua) {
  fe <- d$mitad == entrena
  fv <- d$mitad == evalua
  tau_hat <- predict(bosque_en(fe, d$dhaz[fe]), x[fv, ])$predictions
  eval_dano <- bosque_en(fv, -d$dhaz[fv])
  dv <- d[fv, ]
  comun <- complete.cases(dv[, c("pobre", "urbano97", "comprador_neto")])
  w_hat <- range(eval_dano$W.hat[comun])
  prioridades <- tibble(bosque = -tau_hat,
                        pobre = as.numeric(dv$pobre),
                        urbano97 = as.numeric(dv$urbano97),
                        comprador_neto = as.numeric(dv$comprador_neto))[comun, ]
  rate <- function(p, bosque = eval_dano) {
    set.seed(2026)
    rank_average_treatment_effect(bosque, p, target = "AUTOC", R = 500,
                                  subset = which(comun))
  }
  solas <- map(names(reglas), \(r) rate(prioridades[[r]])) |>
    set_names(names(reglas))
  pares <- map(names(reglas)[-1], \(r) rate(prioridades[, c("bosque", r)])) |>
    set_names(names(reglas)[-1])

  # chequeo de la convencion: con Y = +dHAZ el AUTOC del bosque cambia de signo
  eval_talla <- bosque_en(fv, d$dhaz[fv])
  autoc_talla <- rate(prioridades$bosque, eval_talla)$estimate
  message("Mitad de evaluacion ", evalua, ": AUTOC del bosque, escala de daño ",
          round(solas$bosque$estimate, 4), "; con Y = +dHAZ ",
          round(autoc_talla, 4))
  stopifnot(abs(solas$bosque$estimate + autoc_talla) < 0.02)

  autoc <- imap_dfr(solas, \(s, r) tibble(
    prioridad = r, tipo = "AUTOC", estimacion = s$estimate, ee = s$std.err))
  difs <- imap_dfr(pares, \(p, r) tibble(
    prioridad = paste0("bosque - ", r), tipo = "Diferencia",
    estimacion = p$estimate[3], ee = p$std.err[3]))
  list(
    tabla = bind_rows(autoc, difs) |>
      mutate(p = 2 * pnorm(-abs(estimacion / ee)),
             evaluacion = evalua, ninos = sum(comun),
             comunidades = n_distinct(dv$commid97[comun]),
             ninos_perdidos_na = sum(!comun),
             w_hat_min = w_hat[1], w_hat_max = w_hat[2],
             autoc_bosque_y_talla = autoc_talla),
    toc = imap_dfr(solas, \(s, r) mutate(s$TOC, prioridad = r))
  )
}

principal <- rate_en(entrena = 1, evalua = 2) # pre-registrada
invertida <- rate_en(entrena = 2, evalua = 1) # robustez secundaria

resultados <- bind_rows(principal = principal$tabla,
                        invertida = invertida$tabla, .id = "version") |>
  group_by(version, tipo) |>
  mutate(p_holm = if_else(tipo == "Diferencia" & version == "principal",
                          p.adjust(p, "holm"), NA_real_)) |>
  ungroup() |>
  group_by(prioridad) |>
  mutate(promedio_dos_mitades = mean(estimacion)) |>
  ungroup()
print(resultados, width = Inf)
stopifnot(nrow(resultados) == 14, all(is.finite(resultados$estimacion)))
message("Diferencias que pasan Holm (F3): ",
        sum(resultados$p_holm < 0.05, na.rm = TRUE))

# -----------------------------------------------------------------------------
# 3. Tabla (version pre-registrada; la invertida, al lado)
# -----------------------------------------------------------------------------

num <- function(v, k) if_else(is.na(v), "—", formatC(v, format = "f", digits = k))
z <- decimales$z
etiqueta <- c(reglas, `bosque - pobre` = "Bosque − pobre",
              `bosque - urbano97` = "Bosque − urbano",
              `bosque - comprador_neto` = "Bosque − comprador neto")
pr <- filter(resultados, version == "principal")
inv <- filter(resultados, version == "invertida")
tabla <- pr |>
  left_join(select(inv, prioridad, est_inv = estimacion, ee_inv = ee),
            by = "prioridad") |>
  transmute(prioridad = etiqueta[prioridad], tipo,
            est = paste0(num(estimacion, z), " (", num(ee, z), ")"),
            p = num(p, decimales$estadistico),
            p_holm = num(p_holm, decimales$estadistico),
            inv = paste0(num(est_inv, z), " (", num(ee_inv, z), ")")) |>
  gt(rowname_col = "prioridad", groupname_col = "tipo") |>
  cols_label(est = "Estimación (EE)", p = "p", p_holm = "p Holm (F3)",
             inv = "Mitades invertidas (EE)") |>
  estilo_tabla(
    titulo = "¿El bosque supera a las reglas simples? RATE con AUTOC",
    subtitulo = paste("Escala de daño: AUTOC > 0 = la regla encuentra a niños",
                      "con más pérdida de HAZ 1997-2000 que el promedio"),
    nota = nota_tabla(
      n = pr$ninos[1], comunidades = pr$comunidades[1],
      muestra = "mitad de evaluación, terciles alto y bajo, sin NA en las tres reglas",
      alcance = "contraste",
      extra = c(
        paste("Pre-registro §4: τ̂ de un bosque entrenado en la otra mitad de",
              "las comunidades; puntajes doblemente robustos de un bosque de",
              "evaluación con Y = −ΔHAZ (daño). Tercil alto frente a bajo del",
              "alza dentro de provincia. AUTOC de grf, bootstrap agrupado por",
              "comunidad (R = 500), emparejado en las diferencias."),
        sprintf(paste("Se pierden %d niños por NA en las reglas. Holm: familia",
                      "F3 (m = 3), sobre las tres diferencias; los AUTOC solos",
                      "van sin ajuste. Mitades invertidas: robustez, sin Holm."),
                pr$ninos_perdidos_na[1])
      )))
guardar_tabla("ninos_rate", tabla, resultados, carpeta_salida)

# -----------------------------------------------------------------------------
# 4. Curvas TOC (version pre-registrada)
# -----------------------------------------------------------------------------

toc <- principal$toc |>
  mutate(prioridad = factor(reglas[prioridad], levels = reglas))
fig <- ggplot(toc, aes(q, estimate, color = prioridad, fill = prioridad)) +
  geom_hline(yintercept = 0, color = gris_secundario) +
  geom_ribbon(aes(ymin = estimate - 1.96 * std.err,
                  ymax = estimate + 1.96 * std.err), alpha = 0.12, color = NA) +
  geom_line(linewidth = 0.9) +
  geom_point(size = 1.8) +
  facet_wrap(~prioridad, nrow = 1) +
  scale_color_manual(values = c(paleta_categorica, gris_secundario), guide = "none") +
  scale_fill_manual(values = c(paleta_categorica, gris_secundario), guide = "none") +
  scale_x_continuous(breaks = c(0.25, 0.5, 0.75, 1)) +
  labs(title = "Curvas TOC: ¿la prioridad encuentra a los niños con más daño?",
       subtitle = paste0(subtitulo_contraste, "\n", pr$ninos[1], " niños en ",
                         pr$comunidades[1], " comunidades (mitad de evaluación)."),
       x = "Fracción q de niños priorizados",
       y = "Daño medio en el q priorizado − daño medio\n(HAZ, tercil alto frente a bajo)",
       caption = paste(
         "TOC de grf con puntajes doblemente robustos; bandas: ±1,96 EE",
         "(bootstrap agrupado por comunidad, R = 500). Escala de daño: > 0 =",
         "más daño que el promedio.\nReglas binarias: los empates se promedian,",
         "así que la curva es plana en el grupo priorizado.")) +
  tema_presentacion + tema_paneles +
  theme(plot.title.position = "plot", plot.caption.position = "plot",
        axis.text.x = element_text(size = 10))
guardar_figura("ninos_rate_toc.png", fig, carpeta_salida)
