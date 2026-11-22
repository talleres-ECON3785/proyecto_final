# =============================================================================
# 10_bosque: P3.2, bosque causal principal con los terciles del alza
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Pregunta 2 (¿a quien?), insumo de los GATE (P3.3) y de la calibracion (P4.1).
# Tratamiento binario: comunidad en el tercil alto del alza dentro de su
# provincia (W = 1) frente al tercil bajo (W = 0); el tercil medio no entra
# (registro §3). Resultado: cambio en el HAZ 1997->2000. Solo X de 1997; el HAZ
# de 1997 no entra (regresion a la media, CLAUDE.md §6).
# causal_forest con clusters = commid97, seed = 2026, num.threads = 1.
# Revisa el traslape (W.hat) y reporta el ATE del bosque (AIPW) junto al MCO
# con el mismo tratamiento binario. Escala: HAZ del tercil alto frente al bajo,
# no por +100 % del precio.
#
# Entradas: 01_Datos/03_Listos/base_estimacion.rds
# Salidas:  01_Datos/03_Listos/bosque_terciles.rds (local: bosque, X y base)
#           03_Resultados/Figuras/10_bosque/ninos_bosque_traslape.png
#           03_Resultados/Tablas/10_bosque/ninos_bosque_ate.{png,csv}
# =============================================================================

# los paquetes los carga 00_main.R con pacman
source("02_Scripts/00_formato_tablas.R")
carpeta_salida <- "10_bosque"

base <- readRDS("01_Datos/03_Listos/base_estimacion.rds") |>
  mutate(log_p97 = log(p97), edad_meses97_3 = edad_meses97^3)

# -----------------------------------------------------------------------------
# 1. Muestra: tercil alto (W = 1) y bajo (W = 0) dentro de provincia
# -----------------------------------------------------------------------------

d <- base |>
  filter(tercil_prov %in% c(1, 3)) |>
  mutate(w = as.numeric(tercil_prov == 3))
message("Bosque: ", nrow(d), " niños en ", n_distinct(d$commid97),
        " comunidades (se quedan fuera ", nrow(base) - nrow(d),
        " niños del tercil medio en ",
        n_distinct(base$commid97) - n_distinct(d$commid97), " comunidades)")
print(count(d, w, name = "ninos") |>
        left_join(summarise(d, comunidades = n_distinct(commid97), .by = w),
                  by = "w"))

# -----------------------------------------------------------------------------
# 2. X de 1997
# -----------------------------------------------------------------------------

# controles de 06_ate (sin el cubo de la edad: el bosque no lo necesita) y
# provincia; ninguno tiene NA (05_base los completo con indicadores)
controles <- c("mujer", "edad_meses97", "educ_padre", "educ_madre",
               "fumador_padre", "musulman_padre", "musulman_madre", "urbano97",
               "productor_arroz", "tam_hogar", "quintil_gasto", "centro_salud",
               "agua_entubada", "via_vehiculos", "via_asfaltada", "parada_bus",
               "sequia_incendio_97", "mercado", "telefono", "correo", "banco",
               "entrevista_1998", grep("^falta_", names(base), value = TRUE))
x_controles <- model.matrix(
  reformulate(c(controles, "log_p97", "factor(provincia)")), d)[, -1]
stopifnot(nrow(x_controles) == nrow(d))
# moderadores pre-registrados que no estan en los controles, con sus NA (grf
# los trata como informacion: "missing incorporated in attributes")
x <- cbind(x_controles,
           madre_mas_primaria = as.numeric(d$madre_mas_primaria),
           pobre = as.numeric(d$pobre),
           comprador_neto = as.numeric(d$comprador_neto))
stopifnot(!"haz97" %in% colnames(x))

# -----------------------------------------------------------------------------
# 3. Bosque principal
# -----------------------------------------------------------------------------

bosque <- causal_forest(x, d$dhaz, d$w, clusters = factor(d$commid97),
                        num.trees = 4000, seed = 2026, num.threads = 1)
ate_bosque <- average_treatment_effect(bosque)
print(ate_bosque)

# -----------------------------------------------------------------------------
# 4. Traslape
# -----------------------------------------------------------------------------

d <- mutate(d, w_hat = bosque$W.hat,
            fuera = w_hat < 0.05 | w_hat > 0.95)
share_fuera <- mean(d$fuera)
message("W.hat: min ", round(min(d$w_hat), 3), ", max ", round(max(d$w_hat), 3),
        "; fuera de [0,05; 0,95]: ", sum(d$fuera), " niños (",
        round(100 * share_fuera, 1), " %) en ",
        n_distinct(d$commid97[d$fuera]), " comunidades")

# regla de la sesion del 22-nov (4): si mas del 5 % de los ninos queda fuera,
# el bosque principal se mantiene y se agrega uno de robustez sin ellos
robustez <- NULL
if (share_fuera > 0.05) {
  dentro <- !d$fuera
  bosque_r <- causal_forest(x[dentro, ], d$dhaz[dentro], d$w[dentro],
                            clusters = factor(d$commid97[dentro]),
                            num.trees = 4000, seed = 2026, num.threads = 1)
  robustez <- list(ate = average_treatment_effect(bosque_r),
                   ninos = sum(dentro),
                   comunidades = n_distinct(d$commid97[dentro]))
  print(robustez$ate)
}

etiquetas_w <- c("0" = "Tercil bajo del alza (W = 0)",
                 "1" = "Tercil alto del alza (W = 1)")
fig <- ggplot(d, aes(w_hat, fill = factor(w))) +
  geom_histogram(binwidth = 0.025, boundary = 0, alpha = 0.85,
                 position = "identity") +
  geom_vline(xintercept = c(0.05, 0.95), linetype = "dashed",
             color = gris_secundario) +
  scale_fill_manual(values = paleta_categorica[1:2], labels = etiquetas_w,
                    name = NULL) +
  scale_x_continuous(limits = c(0, 1), breaks = seq(0, 1, 0.1)) +
  labs(title = "Traslape del bosque: probabilidad estimada de estar en el tercil alto",
       subtitle = paste0(subtitulo_descriptivo, " ", nrow(d), " niños en ",
                         n_distinct(d$commid97), " comunidades."),
       x = "Probabilidad estimada de estar en el tercil alto (W.hat, fuera de la bolsa)",
       y = "Niños",
       caption = sprintf(paste(
         "Bosque causal (grf), X de 1997, agrupado por comunidad. Líneas: 0,05",
         "y 0,95. Fuera de ese rango: %d niños (%.1f %%) en %d comunidades.",
         "\nTerciles del alza dentro de provincia; el tercil medio no entra."),
         sum(d$fuera), 100 * share_fuera, n_distinct(d$commid97[d$fuera]))) +
  tema_presentacion +
  theme(legend.position = "top")
guardar_figura("ninos_bosque_traslape.png", fig, carpeta_salida)

# -----------------------------------------------------------------------------
# 5. ATE del bosque y MCO con el mismo tratamiento
# -----------------------------------------------------------------------------

# referencia: especificacion (4) de 06_ate con W binario en lugar de la dosis
mco <- feols(dhaz ~ w + log_p97 + edad_meses97_3 + .[controles] | provincia, d,
             cluster = ~commid97)

resultados <- tibble(
  estimador = c("Bosque causal (AIPW)", "MCO, especificación (4)",
                if (!is.null(robustez)) "Bosque sin niños con W.hat fuera de [0,05; 0,95]"),
  estimacion = c(ate_bosque[["estimate"]], coef(mco)[["w"]],
                 robustez$ate[["estimate"]]),
  ee = c(ate_bosque[["std.err"]], se(mco)[["w"]], robustez$ate[["std.err"]]),
  ninos = c(nrow(d), nobs(mco), robustez$ninos),
  comunidades = c(n_distinct(d$commid97), n_distinct(d$commid97[obs(mco)]),
                  robustez$comunidades)
) |>
  mutate(p = 2 * pnorm(-abs(estimacion / ee)),
         ic_inf = estimacion - qnorm(0.975) * ee,
         ic_sup = estimacion + qnorm(0.975) * ee,
         ninos_fuera_traslape = sum(d$fuera),
         # alza media (1 = +100 %) de cada tercil, entre comunidades, para
         # comparar con la escala de la dosis
         dosis_media_alto = mean(distinct(filter(d, w == 1), commid97, dosis)$dosis),
         dosis_media_bajo = mean(distinct(filter(d, w == 0), commid97, dosis)$dosis),
         w_hat_min = min(d$w_hat), w_hat_max = max(d$w_hat))
print(resultados, width = Inf)
stopifnot(all(is.finite(resultados$estimacion)))

num <- function(x, k) formatC(x, format = "f", digits = k)
tabla <- resultados |>
  transmute(estimador,
            efecto = paste0(num(estimacion, decimales$z), " (",
                            num(ee, decimales$z), ")"),
            ic = paste0(num(ic_inf, decimales$z), " a ", num(ic_sup, decimales$z)),
            p = num(p, decimales$estadistico),
            ninos = num(ninos, 0), comunidades = num(comunidades, 0)) |>
  gt(rowname_col = "estimador") |>
  cols_label(efecto = "Efecto en HAZ (EE)", ic = "IC 95 %", p = "p",
             ninos = "Niños", comunidades = "Comunidades") |>
  estilo_tabla(
    titulo = "Bosque causal: efecto promedio del tercil alto frente al bajo",
    subtitulo = "Cambio en la talla para la edad (HAZ) 1997-2000",
    nota = nota_tabla(
      muestra = "base lista, terciles alto y bajo del alza", alcance = "contraste",
      extra = c(
        paste("Tratamiento: la comunidad de 1997 está en el tercil alto del",
              "alza del precio del arroz dentro de su provincia (frente al",
              "tercil bajo; el medio no entra). Es otro estimando que el de la",
              "dosis: no es HAZ por +100 %."),
        paste("Bosque: grf, 4.000 árboles, agrupado por comunidad, semilla",
              "2026, X de 1997 (controles de E-Q sin programas, log del precio",
              "de 1997, provincia, madre con más que primaria, pobre y",
              "comprador neto); el HAZ de 1997 no entra. ATE por AIPW, EE",
              "agrupado. MCO: especificación (4) del efecto promedio con el",
              "tratamiento binario, EE agrupado.")
      )))
guardar_tabla("ninos_bosque_ate", tabla, resultados, carpeta_salida)

# -----------------------------------------------------------------------------
# 6. Guardar el bosque para P3.3 y P4 (local, no se versiona)
# -----------------------------------------------------------------------------

saveRDS(list(bosque = bosque, x = x, datos = d),
        "01_Datos/03_Listos/bosque_terciles.rds")
