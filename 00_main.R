# =============================================================================
# Script maestro: ejecuta todo el pipeline del proyecto final en una corrida
# Proyecto final - ECON-3785 (2026-2): IFLS y precio del arroz 1997-98
#
# Corre los scripts de 02_Scripts/ en el orden de su numeracion. Antes de
# ejecutarlos, (1) verifica que el directorio de trabajo es la raiz del
# proyecto, (2) instala y carga con pacman todos los paquetes del proyecto,
# (3) verifica que los datos crudos de RAND esten en 01_Datos/01_Crudos/ y
# (4) crea las carpetas de salida que falten. Los scripts individuales NO
# cargan paquetes ni crean carpetas: asumen que este script ya lo hizo.
#
# Los datos crudos NO vienen en el repositorio (licencia de RAND): ver
# 01_Datos/README.md para descargarlos y ubicarlos.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. Verificar que el directorio de trabajo es la raiz del proyecto
# -----------------------------------------------------------------------------

# la raiz es la carpeta que tiene un archivo .Rproj (con cualquier nombre) y
# la carpeta 02_Scripts/
if (length(list.files(pattern = "\\.Rproj$")) == 0 || !dir.exists("02_Scripts")) {
  stop("Ejecuta este script desde la raiz del proyecto (donde esta el .Rproj). ",
       "Directorio actual: ", getwd())
}

# -----------------------------------------------------------------------------
# 2. Paquetes: pacman los instala si no estan y luego los carga
# -----------------------------------------------------------------------------

# lista unica de paquetes del proyecto: si un script nuevo necesita otro
# paquete, se agrega aqui con un comentario de para que se usa (no dentro del
# script). Los que no se vieron en el curso son ampliaciones y se registran
# antes en 07_Recursos/herramientas_R_del_curso.md y en CLAUDE.md
if (!require("pacman")) install.packages("pacman")
pacman::p_load(
  tidyverse,    # limpieza, manipulacion y graficas (incluye ggplot2)
  haven,        # AMPLIACION: lectura de los .dta de la IFLS (read_dta)
  gt,           # formato de las tablas de la presentacion
  modelsummary, # tablas de regresion (output = "gt")
  fixest,       # feols(): efectos fijos y errores agrupados por commid97
  glmnet,       # Lasso de doble seleccion de controles (ATE de referencia)
  grf           # bosque causal con clusters, calibracion, RATE/TOC
)

# -----------------------------------------------------------------------------
# 3. Verificar que los datos crudos esten en su lugar
# -----------------------------------------------------------------------------

# 01_Datos/01_Crudos/ no se versiona: cada integrante descarga los datos de
# RAND (01_Datos/README.md). Aqui solo se comprueba que las cinco olas esten
olas <- paste0("01_Datos/01_Crudos/IFLS", 1:5, "/Household Data")
faltan <- olas[!dir.exists(olas)]
if (length(faltan) > 0) {
  stop("Faltan los datos crudos de RAND en:\n  ", paste(faltan, collapse = "\n  "),
       "\nVer 01_Datos/README.md para descargarlos.")
}

# -----------------------------------------------------------------------------
# 4. Verificar las carpetas de salida (una sola vez, antes de todo)
# -----------------------------------------------------------------------------

# si un script nuevo escribe en otra carpeta, se agrega a esta lista.
# 01_Datos/01_Crudos/ no va aqui: no es una salida y nunca se escribe en ella
carpetas_salida <- c(
  "01_Datos/02_Procesados", "01_Datos/03_Listos",
  "03_Resultados/Tablas", "03_Resultados/Figuras"
  # una subcarpeta por script que genera tablas o figuras (nombre del script),
  # p. ej. "03_Resultados/Tablas/02_precio_arroz"
)
for (carpeta in carpetas_salida) {
  if (!dir.exists(carpeta)) dir.create(carpeta, recursive = TRUE)
}

# -----------------------------------------------------------------------------
# 5. Orden de ejecucion de los scripts (segun su numeracion)
# -----------------------------------------------------------------------------

# cada script nuevo se agrega aqui en la misma sesion en que se crea. Orden
# previsto (10_Propuesta/02_datos_ifls_acceso_y_manejo.md, seccion 6):
#   01_tracks, 02_precio_arroz, 03_x_1997, 04_haz_9700, 05_escolaridad_2014,
#   06_cognicion, 10_validacion, 20_bosques, 40_focalizacion
scripts <- c(
)

# nota: los '00_formato_*.R' no aparecen en esta lista porque no producen
# resultados; los cargan con source() los scripts que generan figuras o tablas.
# Los scripts de 02_Scripts/_exploratorio/ tampoco: no alimentan resultados.

# -----------------------------------------------------------------------------
# 6. Ejecutar cada script en su propio entorno, en orden
# -----------------------------------------------------------------------------

for (script in scripts) {
  mensaje <- paste0("Ejecutando: ", script)
  message(strrep("=", nchar(mensaje)))
  message(mensaje)
  message(strrep("=", nchar(mensaje)))

  source(script, local = new.env(), encoding = "UTF-8")
}

message("Pipeline completo: ", length(scripts),
        " scripts se ejecutaron sin errores.")
