# IFLS5 (2014-2015) · Catálogo, contenido y manejo de los datos

*Guía de la ronda 5 para el proyecto final de Ciencia de Datos. Escrita el 14-nov-2026 a partir de la documentación de RAND en `01_Datos/01_Crudos/IFLS5/Documentation` (guía de usuario vol. 1 y 2, codebooks `.txt` y cuestionarios en PDF en inglés e indonesio) y de una revisión directa de los 152 archivos `.dta` de `Household Data` y los 150 de `Community Data`. Los conteos y las pruebas de llaves salen de los archivos (Python + `pyreadstat` 1.3.7); lo demás, de la documentación citada. Los scripts de la revisión están en `01_Datos/01_Crudos/IFLS5/_revision/`.*

*La guía es **descriptiva**: documenta qué hay, cómo está codificado y qué problemas tiene. No decide qué variables serán resultado, control o muestra; las opciones quedan en §12 («Preguntas abiertas»).*

## 1. Qué es esta ronda

- **IFLS5.** Quinta ola completa: hogares de 1993 y todos sus *split-off* de 1997, 1998, 2000 y 2007, más nuevos *split-off* de 2014. Primera ola levantada con entrevista asistida por computador (CAPI; guía vol. 1, §2.2).
- **Trabajo de campo.** Primera visita del libro K (`bk_time`): **septiembre de 2014 a septiembre de 2015** (§8). El codebook dice «entre noviembre de 2014 y julio de 2015» y la guía vol. 1 «finales de 2014 y comienzos de 2015»; los datos muestran un periodo más largo.
- **Tamaño (archivos):** `htrack` tiene 19.401 filas (todo hogar que aparece en alguna ola). **15.921 hogares tienen el libro K hecho en 2014** (`res14bk` = 1, igual a `result14` = 1 y a las filas de `bk_cov`): 6.044 de origen y 9.877 *split-off* (sexto dígito del `hhid14`: 607 de 1997, 207 de 1998, 1.787 de 2000, 3.273 de 2007 y **4.003 nuevos de 2014**). `ptrack` tiene 83.780 filas; 58.549 son miembros de un hogar en 2014 (`member14` = 1).
  - La guía vol. 1 habla de 16.204 hogares y 50.148 personas entrevistadas; la vol. 2, de 13.536 registros en HTRACK y 50.579 en PTRACK. **Ninguna cifra coincide con los archivos.** Las de la vol. 2 son casi iguales a las de 2007 (13.536 hogares con libro K en 2007; 50.582 miembros en 2007, según `IFLS4/00_guia_IFLS4.md`): parece texto heredado.
- **Panel:** 5.564 hogares tienen `result` = 1 en 1993, 1997, 2000, 2007 y 2014. 17.309 personas son miembros de un hogar en las cinco olas.
- **Comunidades:** las mismas EA de la IFLS (320 filas en `bk1`, 311 códigos `commid14`) más hogares fuera de ellas con `commid14` con letras (§6.1, §10).
- **Contenido nuevo o cambiado frente a 2007:**
  - **CES-D de 10 ítems con una sola pregunta de frecuencia** (`kp02`); en 2007 había un filtro sí/no (`kp01`) (§9.2);
  - antropometría y salud física en **un solo archivo** (`bus_us`) (§9.1);
  - pruebas EK con **indicadores de respuesta correcta ya calculados** (`ekN_ans`) (§9.4);
  - el módulo de desastres (`b2_nd*`) **incluye ahora choques económicos del hogar** (muerte, enfermedad, pérdida de empleo, cosecha, caída de precios) (§9.6);
  - módulos nuevos: personalidad (`b3b_psn`), afecto positivo/negativo (`b3a_pna*`), sueño (`b3b_tdr`), serie numérica adaptativa (`b3b_cob`), gotas de sangre seca (`dbs_*`);
  - **no hay archivos de libro proxy** (`bp_*`), aunque el cuestionario proxy existe (§6.3).

## 2. Qué archivos hay

- `Household Data/`: 152 archivos `.dta`; `Community Data/`: 150. **Todos en formato `.dta` 111** (Stata 7 SE). El codebook dice «STATA (8.0)» y el mapa automático de la guía decía Stata 13; ninguno es correcto. No hay `.zip` pendientes. La carpeta pesa 2,0 GB.
- **Cotejo con los codebooks** (`ifls2014_hhd_*.txt`, `ifls2014_cf_*.txt`): 298 archivos aparecen en las listas de módulos, todos con el mismo número de filas, **salvo `schl` (2.668 en el archivo, 2.567 en el codebook)**.
  - `dbs_ifls4_public_use` y `dbs_ifls5_public_use` (7.579 filas cada uno) no están en los codebooks; los documenta `IFLS5-DBS-PubUse-Jan31.pdf`.
- **El apéndice A de la guía vol. 2 no coincide del todo con los archivos.** Usa nombres que no existen (`BK_AR2` por `bk_ar1`, `BEF_*` por `fe_*`, `B3A_KW2`/`KW33` por `b3a_kw1`/`kw3`) y omite archivos que sí están (`b5_rja0`-`rja2`, `bt_time`, `bus_time`, `ek_time1`/`2`, `mkd_*`, `pkk_lk`, `pkk_time`, `sch*_cov`/`_time`). Sus conteos de EK no coinciden con los archivos (§9.4).
- **Sin problemas de lectura** con `pyreadstat`: ningún valor con |x| > 1e90 (el problema de 1997) y casi ninguna columna numérica leída como texto (el problema de 2000). Las pocas columnas de texto con contenido numérico son de control: `idrtk`, `stemid`, `idrtfe`, `ea`, `idw`, `eabk1`, `eabk2`, `fascode`, `bxar00`, `ep06`, `baatype`, `prptype`.
- Hay un duplicado de nombre en `Documentation/IFLS5_BPS_2014_codes/` («`kec_9899000714.dta 2`»).

## 3. Mapa de la documentación

| Archivo | Qué es | Cuándo usarlo |
|---|---|---|
| `IFLS5_User_Guide_Vol_1.pdf` | Diseño, recontacto, CAPI, contenido de los cuestionarios | Sección de datos del informe |
| `IFLS5_User_Guide_Vol_2.pdf` | Ids, `commid14`/`mkid14`, códigos especiales, pesos, `htrack`/`ptrack`, apéndices A-C. **Conteos de HTRACK/PTRACK y del apéndice A desactualizados** (§1, §2) | Leer primero, con cuidado |
| `IFLS5_hh_codebooks/ifls2014_hhd_*.txt` | Codebooks de hogar (14 libros, incluidos `BUS`, `EK`, `BEK`, `FE`, `HTRACK`, `PTRACK`) con frecuencias | Códigos y frecuencias |
| `IFLS5_cf_codebooks/ifls2014_cf_*.txt` | Codebooks comunitarios (15 libros, incluidos `HPS`, `HTW`, `HIN`, `MKD`) | Datos comunitarios |
| `IFLS5_HH_PQX_Public_Eng/`, `IFLS5_HH_PQX_Public_Ind/` | Cuestionarios de hogar en inglés e indonesio, incluidos EK tipo 1 (7-14) y tipo 2 (15+) y el libro proxy | Redacción exacta |
| `IFLS5_CF_PQX_Public_Eng/`, `IFLS5_CF_PQX_Public_Ind/` | Cuestionarios comunitarios (incluidos precios de mercado y *warung* y mini-CFS) | Datos comunitarios |
| `IFLS5_hh_formats/`, `IFLS5_cf_formats/` | Formatos SAS (`.inc`) con etiquetas de valores | Etiquetas que faltan en los `.dta` |
| `IFLS5_BPS_2014_codes/` | Códigos BPS de provincia, kabupaten y kecamatan de 2014 | Unir con fuentes externas |
| `IFLS5-DBS-PubUse-Jan31.pdf` | Gotas de sangre seca (CRP, HbA1c) | Solo si se usan biomarcadores |
| `Prindle_McArdle_Numeracy_Results.pdf` | Resultados de la prueba de numeracidad | Módulo `b3b_cob` |
| `interviewers_data/` | Datos de los entrevistadores de IFLS4 e IFLS5 | Efectos de entrevistador |

## 4. Libros y quién responde

Reglas: las mismas de 2007 (guía vol. 1). En hogares de origen se entrevista o se hace proxy a todos; en *split-off*, a los miembros de 1993, sus cónyuges e hijos. Por diseño de la IFLS, los libros 3A/3B son para personas de 15 años o más; el libro 5, para menores de 15; el libro 4, para mujeres alguna vez casadas (no se buscó la regla en la guía de 2014). En los datos no se cruzan (ninguna persona está en `b3a_dl1` y `b5_dla1` a la vez), pero con `ptrack$age_14` hay 323 personas de `b3a_dl1` con menos de 15 años (mínimo 7) y 10 de `b5_dla1` con 15 o más (máximo 41).

Resultado por persona en `ptrack` (personas distintas por `pidlink`):

| Libro | Completo | Parcial | No completado |
|---|---:|---:|---:|
| 3A | 34.394 | 69 | 1.930 |
| 3B | 34.201 | 69 | 2.118 |
| 4 | 12.473 | 3 | 586 |
| 5 | 3.231 | **12.447** | 454 |
| US (medición) | 48.137 | — | 4.444 |
| EK (`res14bek`) | 39.081 | — | 5.465 |

- En el libro 5 casi todo figura como «parcialmente completo»; no se sabe por qué.
- `res14bek` dice «Book EK1 completed», pero sus 39.081 completos no corresponden a ningún archivo: `ek_ek1` tiene 13.469 con `result` = 1 y `ek_ek2` 29.642.

## 5. Catálogo de archivos

«Llave única» es la combinación de variables que identifica cada fila, **comprobada en los archivos** (primera combinación de 1 a 3 variables entre los ids y las variables `…type`); «no determinada» significa que ninguna combinación estándar resultó única. En los libros individuales la llave aparece como `pidlink`; **`hhid14` + `pid14` también es única** en `b3a_cov`, `b3a_dl1`, `b3b_cov`, `b4_cov`, `b5_cov`, `b5_dla1`, `bus_us`, `ek_ek1` y `ek_ek2` (verificado). Las descripciones de cada archivo están en las listas de módulos de los codebooks y en el apéndice A de la guía vol. 2.

<<CATALOGO>>

## 6. Cómo manejar los datos

### 6.1 Identificadores

| Variable | Qué es | Notas (verificadas) |
|---|---|---|
| `hhid14` (texto, 7) | EA + hogar + origen/*split-off* | Sexto dígito: `0` origen, `1` *split-off* de 1997, `2` de 1998, `3` de 2000, `4` de 2007, `5` nuevo en 2014. Único entre los 15.921 hogares de 2014; vacío en `htrack` para 3.480 hogares no entrevistados |
| `hhid14_9` (texto, 9) | Versión de 9 caracteres | En casi todos los archivos de hogar. **No es `hhid14` con dos dígitos más**: p. ej., `hhid14` = `0010651` tiene `hhid14_9` = `001060004` |
| `pid14` | Línea en el roster de 2014 | |
| `pidlink` (texto, 9) | Persona, constante entre olas | Único dentro de cada libro individual. En `ptrack` se repite 3 veces (§6.1, más abajo). **3 personas tienen `pidlink` de 8 caracteres** (`14103003`, `14103007`, `14103008`, hogar `1410341`) |
| `commid14` (texto, 4) | Comunidad | En los 15.921 hogares de 2014: 9.106 con código numérico (312 códigos) y **6.815 con letras** (fuera de las EA de la IFLS). 3 hogares tienen el código `3249`, que no está en `bk1` |
| `ea` (texto, 3) | EA de la IFLS (001-320) | **Llave de los archivos comunitarios** (`bk1`, `bk2`, `pkk`, `hin`, `bk1a_cov`…): 320 EA para 311 códigos `commid14` (§10). No está en `htrack` |
| `mkid14` (texto, 5) | Llave del mini-CFS (`mkd_*`) | 4.339 valores en `htrack`, 261 vacíos (`mkdstatus` = 2). De los 6.815 hogares con letras, 6.551 tienen un `mkid14` que está en `mkd_cov` |
| `fascode`, `fcode14` | Establecimiento | Precios: `fascode` (p. ej., `001P501` mercado, `001W501` *warung*). Escuelas y posyandu: `fcode14` |

**`htrack` es acumulativo.** Una fila por hogar que aparece en cualquier ola (19.401), con la historia de ids `hhid93`, `hhid97`, `hhid98`, `hhid00`, `hhid07`, `hhid14`. Esa combinación de seis variables es única; ninguna sola lo es (cada *split-off* repite el `hhid93` de su hogar de origen). Las columnas `pidlink` y `pid14` existen en `htrack` pero están vacías.

**`ptrack` tiene filas repetidas.** `pidlink` se repite en 3 casos: una fila duplicada exacta (`017132102`) y dos personas que aparecen en dos hogares de 2014 (`168284105`, `274090007`). `ar01a_14` = 6 («duplicado») marca 246 filas.

**El roster (`bk_ar1`) acumula a todos los que vivieron en el hogar.** `pidlink` se repite 13.702 veces. La guía vol. 2 dice que basta con quitar `ar01a = 3`; **no basta**: quedan 292 repetidos; quitando además muertos (`ar01a = 0`) quedan 14, y quitando también duplicados (`ar01a = 6`), 8.

Códigos de `ar01a` (codebook `PTRACK`, `ar01a_14`): 0 muerto, 1 sigue en el hogar, 2 estaba en otro hogar IFLS en la ronda anterior, 3 ya no vive ahí, 5 nuevo miembro, 6 duplicado, 11 regresó en la misma ronda.

**Archivos sin llave única** con las combinaciones estándar (§5): `b2_nd2` (12 pares `hhid14` + `ndtype` repetidos), historia educativa (`b3a_dl2`, `dl3`), padres fuera del hogar (`b3b_ba0`), hijos fuera del hogar (`b4_bx6`), formulario de salida (`fe_34`), archivos de tiempo (`bt_time`, `ek_time1`, `ek_time2`) y, entre los comunitarios, `hps`, `sar` y casi todos los de establecimientos de salud y escuelas. No se buscó la llave correcta de cada uno.

### 6.2 Códigos especiales

Codebook (todos los libros): 5/95/995 (texto V) fuera de rango, 6/96/996 (W) no aplica, 7/97/997 (X) rechazo, 8/98/998 (Y) no sabe, 9/99/999 (Z) faltante. Variables X (`…x`) indican si hay respuesta. Sí/no = 1/3; sexo = 1 hombre / 3 mujer. Años con 4 dígitos. Intervalos (*unfolding brackets*) con punto de entrada aleatorio (guía vol. 2).

- **Talla y peso (`bus_us`) no usan códigos especiales**: el no medido es faltante (§9.1).
- **Precios del informante (`hin_h`) sí traen 999998** (§10).

### 6.3 Proxy y formato largo

- **No hay archivos del libro proxy** en la descarga (en 2007 eran `bp_*`), aunque `17. PQX Buku Proxy.pdf` y `15 IFLS5 HH BOOK PROXY.pdf` existen. No se sabe si las entrevistas proxy quedaron dentro de los libros 3A/3B.
- Muchos archivos están en formato largo con variables `…type` (§5).

### 6.4 Pesos

Etiquetas de los codebooks `HTRACK` y `PTRACK`:

| Archivo | Variables | Qué son |
|---|---|---|
| `htrack` | `hwt14xa`, `hwt14x_` | Transversales de hogar con y sin ajuste por desgaste |
| `htrack` | `hwt14la`, `hwt14l_` | Longitudinales de hogar con y sin corrección por desgaste |
| `htrack` | `hwt_5_waves_l` | Longitudinal de hogar para el panel 1993-1997-2000-2007-2014 |
| `htrack` | `hh14attr_adjust`, `hh9397000714attr_adjust` | Sumas de ajustes de desgaste individuales |
| `ptrack` | `pwt14xa`, `pwt14x_` | Transversales de persona con y sin corrección |
| `ptrack` | `pwt14la` | Longitudinal para miembros de 1993 encontrados en 2014 |
| `ptrack` | `pwt_5_waves_l`, `pwt_5_waves_lr`, `pwt_5_waves_usl` | Longitudinales 1993-2014: entrevistado, en el roster, medido |
| `ptrack` | `pwt14usxa`, `pwt14usx_` | Transversales de medición de salud |
| `ptrack` | `pwt14dbsxa`, `pwt14dbsx_`, `pwt14dbsla`, `pwt07dbsxa`, `pwt07dbsx_` | Gotas de sangre seca |

`htrack` y `ptrack` de 2014 traen también los pesos de 1993, 1997, 2000 y 2007 (p. ej., `pwt97ekx`, `pwt07usxa`).

## 7. Seguimiento

**Hogares** (`htrack$result14`, etiquetas del codebook): 15.921 entrevistados (1), 199 rechazos (2), 485 unidos a otro hogar IFLS (3), 386 todos muertos (4), 1.069 no encontrados (5), 88 «aún no entrevistados» (6), 129 «confirmación de mudanza» (8) y 1.124 sin dato.

- **Los códigos 2-4 del codebook no coinciden con la guía vol. 2**, que dice 2 = unido a otro hogar, 3 = todos muertos, 4 = rechazo. Los códigos 6 y 8 no están en la guía.
- De los 7.224 hogares de 1993: 5.917 con `result14` = 1, 532 no encontrados, 302 con código 4, 133 con código 2, 47 con código 3, 47 con 6, 26 con 8 y 220 sin dato.
- `mover14` (entre 2007 y 2014; 15.902 hogares con dato): 8.509 no se movieron; 1.740 dentro de la desa; 1.895 dentro del kecamatan; 1.126 dentro del kabupaten; 1.361 dentro de la provincia; 1.059 a otra provincia IFLS; 212 a otra provincia. En esta ronda **no aparecen los códigos raros de 2007** (6 y 98 sin documentar): aquí el 6 sí tiene etiqueta.
- De los 8.509 que no se movieron, 8.297 tienen el mismo `commid14` que `commid07`. 2.362 hogares que no se movieron tienen `commid14` con letras (estaban fuera de las EA ya en 2007).

**Personas del roster de 1993** (33.081; `ptrack$ar01a_14`): 16.276 siguen en el mismo hogar (1), 4.355 estaban en otro hogar IFLS (2), 6.656 ya no están (3), 5.733 murieron (0), 30 duplicados (6) y 31 regresaron (11); **20.692 son miembros de un hogar en 2014**.

**Niños de 0 a 5 años en 1997** (`ptrack$age_97` ≤ 5 y `member97` = 1): **3.851**, de 15 a 25 años en 2014 (mediana 19; 319 sin `age_14`).

| Qué tienen en 2014 | Personas |
|---|---:|
| Miembros de un hogar (`member14` = 1) | 2.846 |
| Muertos (`ar01a_14` = 0) | 97 |
| Talla medida (`bus_us$us04` no faltante) | 2.586 |
| Libro 3A, educación (`b3a_dl1`) | 2.690 (2.682 con `dl06`) |
| CES-D (`b3b_kp`) | 2.578 |
| EK1 con `result` = 1 | 2.225 |
| EK2 con `result` = 1 | 2.522 |
| EK1 o EK2 con `result` = 1 | 2.535 |

**Personas de 5 a 21 años en 1997** (`member97` = 1): 12.632; 8.423 miembros en 2014; 401 muertos; 7.993 con `b3a_dl1` (7.925 con `dl06`); 7.650 con talla; 7.250 con EK1 o EK2 completos.

**Coherencia de edades.** Para quienes eran miembros en 1997, `age_14` − `age_97` tiene mediana 17, pero 3.160 de 30.104 caen fuera de 16-19 (mínimo −99, máximo 75). En la cohorte de 5-21 años en 1997, `age_14` va de 9 a 95. `ptrack$bth_year` falta en 12.141 filas y va de 1895 a 2014. `age_14` falta para 1.712 de las 48.139 personas de `bus_us`.

## 8. Fechas de entrevista

Primera visita del libro K (`bk_time`, `time_occ` mínimo), por ubicación del hogar (`commid14` con o sin letras):

| Año-mes | 2014-09 | 2014-10 | 2014-11 | 2014-12 | 2015-01 | 2015-02 | 2015-03 | 2015-04 | 2015-05 | 2015-06 | 2015-07 | 2015-08 | 2015-09 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| En comunidades IFLS | 727 | 1.323 | 1.529 | 1.628 | 1.299 | 979 | 635 | 433 | 146 | 88 | 39 | 183 | 97 |
| Fuera de comunidades IFLS | 185 | 486 | 576 | 472 | 624 | 504 | 658 | 699 | 812 | 657 | 252 | 665 | 225 |

- `bk_time` tiene hasta 21 visitas por hogar (`time_occ`); 2.243 hogares tuvieron al menos una segunda visita.
- **Libros individuales y medición:** de septiembre de 2014 a diciembre de 2015 (`b3a_time`, `bus_time`). `bus_time` tiene 1 caso con fecha de 2009-01.
- **Pruebas cognitivas** (`ek_time1`, `ek_time2`): de septiembre de 2014 a diciembre de 2015. En `ek_ek1`, 6.595 en 2014 y 8.348 en 2015; en `ek_ek2`, 16.471 y 19.909.
- **Encuesta comunitaria y de precios** (`bk1a_time`, `pkk_time`, `hps_time`, `htw_time`, `hin_time`): **de marzo a agosto de 2015**, casi todo de marzo a junio. Es decir, buena parte de los hogares se entrevistó entre 3 y 6 meses antes que su comunidad.

## 9. Contenido por tema

### 9.1 Antropometría y salud física (`bus_us`)

- **Un solo archivo** con 48.139 personas y 143 variables: presión arterial (3 medidas), **peso** (`us06`), **talla** (`us04`), método de medición (`us05`), altura de rodilla (40+), largo del brazo, cintura y cadera, sentarse y pararse, fuerza de agarre, balance, velocidad de marcha, capacidad pulmonar, hemoglobina, toma de gotas de sangre seca, medicamentos, ayuno, embarazo, discapacidad. `bus_cov` (52.580) es la portada.
- **Talla:** `us04x` = 1 en 47.859, 3 en 189, 7 en 91. Rango de 42,0 a 198,0 cm (p1 62,6; mediana 151,4; p99 174,3). Sin códigos especiales ni ceros. De pie (`us05` = 1) 45.856; acostado (3) 2.003; sin dato 280.
- **Peso:** `us06x` = 1 en 47.929. Rango de 1,5 a 142,3 kg (mediana 49,4).
- Fecha de nacimiento: no está en `bus_us`. Fuentes de edad: `bk_ar1`, `ptrack` (`age_14`, `bth_year`, `bth_month`, `bth_day`, `bg_dob`) y la fecha de medición en `bus_time`.
- Gotas de sangre seca: `dbs_ifls5_public_use` (y `dbs_ifls4_public_use`), 7.579 personas, con su propia documentación.

### 9.2 Salud mental (`b3b_kp`)

- **CES-D de 10 ítems**, semana anterior. Formato largo: una fila por persona e ítem (`kptype` A-J; **31.447 personas × 10**, sin faltantes). **Una sola pregunta:** `kp02` (frecuencia: 1 raramente o nunca, ≤ 1 día; 2 algunos días, 1-2; 3 ocasionalmente, 3-4; 4 la mayor parte del tiempo, 5-7). **No hay `kp01`** (el filtro sí/no de 2007).
- **Las etiquetas de `kptype` del codebook sí coinciden con el cuestionario** (`08 IFLS5 HH BOOK 3B.pdf`, sección KP), a diferencia de 2007. El orden de los ítems es el mismo del cuestionario de 2007.

| `kptype` | Ítem | ≤ 1 día | 1-2 días | 3-4 días | 5-7 días |
|---|---|---:|---:|---:|---:|
| A | Me molestaron cosas que usualmente no me molestan | 20.144 | 5.563 | 4.444 | 1.296 |
| B | Tuve problemas para concentrarme | 19.413 | 5.965 | 4.685 | 1.384 |
| C | Me sentí deprimido | 22.903 | 4.254 | 3.095 | 1.195 |
| D | Sentí que todo lo que hacía era un esfuerzo | 17.047 | 5.477 | 4.888 | 4.035 |
| E | Me sentí con esperanza en el futuro (positivo) | 3.600 | 5.367 | 6.781 | 15.699 |
| F | Sentí miedo | 21.311 | 4.827 | 3.697 | 1.612 |
| G | Dormí mal | 19.034 | 4.231 | 4.762 | 3.420 |
| H | Estuve feliz (positivo) | 2.582 | 5.599 | 8.782 | 14.484 |
| I | Me sentí solo | 25.318 | 2.684 | 2.464 | 981 |
| J | No podía ponerme en marcha | 23.045 | 3.557 | 3.661 | 1.184 |

- **No es igual al formato de 2007:** allí la categoría «no» (`kp01` = 3) estaba separada de «≤ 1 día»; aquí ambas caen en `kp02` = 1.
- Otros módulos cercanos, nuevos: afecto positivo/negativo (`b3a_pna1`, `pna2`), personalidad BFI (`b3b_psn`), sueño PROMIS (`b3b_tdr`), bienestar subjetivo (`b3a_sw`). No se revisaron.

### 9.3 Educación

- **Adultos (`b3a_dl1`, 34.464, 15 años o más):** alguna vez asistió (`dl04`: 32.677 sí, 1.741 no, 44 no sabe); nivel más alto (`dl06`: 2 primaria, 3-4 secundaria baja, 5-6 secundaria alta, 11/12/15 educación de adultos A/B/C, 13 universidad abierta, 14 pesantren, 17 escuela especial, 60 diploma D1-D3, 61-63 universidad S1-S3, 72-74 madrasah, 90 kínder, 95 otro, 98 no sabe; 1.787 faltantes); grado más alto en ese nivel (`dl07`: 0 no completó el primero, 1-6 grado, **7 graduado**, 98 no sabe). El codebook etiqueta los grados 1-6 de `dl07` como «missing» por error de formato. Historia en `b3a_dl2`-`dl5`; asistencia actual `dl07a`; año en que dejó la escuela `dl07byr`.
- **Niños (`b5_dla1`, 15.742, menores de 15):** 8.591 asistieron alguna vez (`dla01`); nivel (`dla08`) y grado (`dla09`); sigue en la escuela (`dla07`). Historia en `b5_dla2`, `dla3`, `dla6`.
- **Roster (`bk_ar1`):** nivel y grado para todos (no revisado en esta ronda).

### 9.4 Pruebas cognitivas (`ek_ek1`, `ek_ek2`)

- **Dos archivos**, una fila por persona en cada uno: `ek_ek1` (tipo 1, 14.943 personas de 7 a 44 años) y `ek_ek2` (tipo 2, 36.380 personas de 7 a 99 años; solo 1 menor de 15). **6.779 personas están en los dos**: en `ek_ek1`, `resptype` = 2 marca a 6.777 de 15 años o más (5.178 de 15-24 y 1.599 de 25-44) que también tomaron el tipo 1, seguramente el panel de niños de 2007.

| Archivo | Ítems con respuesta | `result` (1 / 2 / 3) | Edad (mín.-mediana-máx.) |
|---|---|---|---|
| `ek_ek1` | `ek1`-`ek12` (12) y `ek13`-`ek17` (5) | 13.469 / 526 / 948 | 7-14-44 |
| `ek_ek2` | `ek1`-`ek12` (12) y `ek18`-`ek22` (5) | 29.642 / 1.697 / 5.041 | 7-35-99 |

- **Respuestas como letras** (A-F; Y no sabe, X rechazo, Z faltante). **Indicador de acierto ya calculado:** `ekN_ans` (codebook: 0 incorrecto, 1 correcto). **Trampa: `ekN_ans` = 0 también cuando no hubo respuesta**: en `ek_ek1`, `ek1_ans` = 0 en 1.924 filas, de las cuales 948 no tienen respuesta. Los ítems que no aplican a la versión vienen con `_ans` = 0 en todas las filas (p. ej., `ek18_ans` en `ek_ek1`).
- En el tipo 2, los ítems de matemáticas (`ek18`-`ek22`) faltan para todos los mayores de 59 años (4.219) y para 3.747 personas de 15-59.
- **Diferencias con 2007:** el tipo 2 tiene ahora 12 ítems cognitivos (en 2007 eran 8: `ek1`-`ek6`, `ek11`, `ek12`) y se aplica a todas las edades de 15 en adelante (en 2007, 15-24). No se verificó en los cuestionarios que los ítems sean idénticos a los de 2000 y 2007.
- La guía vol. 2 da para EK 66.283 y 87.725 registros, y una descripción contradictoria del tipo 2 («8 cognitivas + 5 matemáticas» y «las últimas 10 son matemáticas»); los archivos tienen 14.943 y 36.380 filas con la estructura de la tabla.
- Pruebas cognitivas de adultos aparte: `b3b_co1` (31.471; recuerdo de palabras, fecha, etc.) y `b3b_cob` (31.409; serie numérica adaptativa, nueva). No se revisaron.

### 9.5 Arroz: consumo, precio pagado y Raskin

- `b1_ks1` (arroz, `ks1type` = A; 15.144 hogares): `ks02` = valor comprado la última semana (Rp; 7.008 con 0), `ks03` = valor de producción propia (mediana 0; p99 140.000; máximo 750.000).
- `b1_ks4` (arroz, `ks4type` = A; 15.135 hogares): 10.720 compraron el último mes (`ks13a` = 1). Unidad (`ks14`): kg 9.675, litro 935, bolsa 64, otra 43, no sabe 3. Precio implícito (`ks15`/`ks13`, solo kg, sin limpiar): **mediana Rp 9.500/kg**; p1 1.600; p5 4.741; p95 12.500; p99 16.667; mínimo 10. Hay compras con `ks13` = 0.
- **Raskin** (`b1_ksr2`, `ksr24a`): 6.692 hogares compraron arroz Raskin en el último año (A), 47 recibieron dinero (B), 19 ambas (AB), 8.105 no (C) y 270 no saben o no hay programa (W). Cantidades, precios y fechas en `ksr25`-`ksr36`.
- `b1_ksr3` (compras en mercado subsidiado, `ksr2type` B arroz, D azúcar, J aceite, K kerosene): solo 189 hogares compraron arroz así.
- `b1_ksr1`: transferencias en efectivo (`ksr3type` A compensación por subsidio, B condicionada, C BLT). No revisado en detalle.

### 9.6 Agricultura y choques

- **El módulo ND (`b2_nd1`, `b2_nd2`) cubre ahora también choques económicos del hogar** en los últimos 5 años. `nd01` registra desastres en el área (letras combinadas; 11.992 hogares con W = ninguno); `nd02a`, choques económicos. `b2_nd2` tiene una fila por hogar y tipo (`ndtype`; 3.435 filas):

| `ndtype` | Tipo (codebook) | Filas |
|---|---|---:|
| A | Inundación | 331 |
| B | Deslizamiento | 21 |
| D | Terremoto (según el codebook) | 112 |
| E | Erupción volcánica (según el codebook) | 69 |
| G | Vendaval | 95 |
| H | Incendio forestal | 8 |
| I | Incendio | 27 |
| J | Conflicto civil | 10 |
| K | Muerte del jefe o principal perceptor | 161 |
| L | Muerte de otro miembro | 151 |
| M | Enfermedad grave del jefe o principal perceptor | 370 |
| N | Enfermedad grave de otro miembro | 568 |
| O | Pérdida de empleo o quiebra | 457 |
| Q | Cosecha fallida | 470 |
| R | Caída del ingreso por caída de precios | 514 |
| S | Sequía | 71 |

  - **Trampa: D y E están invertidos entre el codebook y los cuestionarios.** Los cuestionarios en inglés y en indonesio dicen D = erupción volcánica (*Gunung Meletus*) y E = terremoto (*Gempa Bumi*); el codebook dice lo contrario.
  - Las letras C (lodo) y F (tsunami) existen en el cuestionario pero no aparecen en `ndtype`.
  - 12 pares `hhid14` + `ndtype` repetidos.
- Agricultura: `b2_ut1` (tierra, ingreso), `b2_ut2` (cosechas de arroz, 2.443 filas), `b2_ut3` (problemas de cosecha), `b2_ut4` (activos).

### 9.7 Otros módulos nuevos o ampliados

Personalidad (`b3b_psn`), afecto positivo/negativo (`b3a_pna*`), sueño (`b3b_tdr`), serie numérica adaptativa (`b3b_cob`), preferencias de riesgo y tiempo (`b3a_si`), confianza (`b3a_tr`), toma de decisiones del hogar (`b3a_pk*`), nivel socioeconómico en la niñez (`b3b_sa`), salud temprana (`b3b_eh`), expectativas sobre los hijos (`b3b_ep*`, `b4_ep*`), seguro de salud (`b3b_ak*`), formulario de salida de fallecidos (`fe_*`). Descripciones a partir de las etiquetas de variables y del apéndice A; no se revisaron en detalle.

## 10. Datos comunitarios de 2014-2015

**Unidad: la EA, no el `commid14`.** `bk1`, `bk2`, `pkk`, `hin`, `bk1a_cov`-`bk1c_cov` y `sar_cov` tienen **320 filas, una por EA** (`ea` = 001-320, igual a `idw`), para **311 códigos `commid14`**. Nueve códigos tienen dos EA: `3109`, `3113`, `3114`, `3134`, `3233`, `3331`, `3403`, `3409`, `3415`; son los mismos 9 que en 2007 tenían dos filas. `bk1_pap0` tiene 311 filas (una por `commid14`) y `pkk_lk` 309. El código `9999` de 2007 no aparece.

**Precios del arroz: tres libros**, levantados de marzo a agosto de 2015 (§8). Calidades (`htype`, cuestionario `11 IFLS5 CF PRICES - MARKET.pdf`): 1 alta (Rojolele, Mentik), 2 media (Cisadane), 3 baja (IR64).

| Libro | Archivo | Calidades | Comunidades con precio en kg | Unidad (filas de arroz) | Rp/kg, mediana (p1-p99), sin limpiar |
|---|---|---|---|---|---|
| Mercado (`HPS`) | `hps_h` | alta, media, baja | 224 / 224 / 217 | kg 682, litro 166, otra 26, faltante 86 | alta 10.750 (8.000-17.710); media 9.000 (7.000-12.855); baja 8.000 (5.000-11.000) |
| *Warung* / tienda (`HTW`) | `htw_h` | solo media | 198 | kg 319, litro 113, otra 14, faltante 194 | media 9.000 (7.000-14.820); máximo 55.000 |
| Informante (`HIN`) | `hin_h` | alta, media, baja | 225 / 219 / 199 | kg 655, litro 201, otra 32, faltante 72 | alta 11.000 (7.000-20.720); media 9.000; baja 8.000. **Incluye 999998** (no sabe), que llega al p99 en media |

- Llave de los archivos de precios: `fascode` + `htype` (verificada). `hps` (portada del mercado) tiene 675 filas para 320 `fascode`: repite el mercado 2 o 3 veces con distinto `cov02market` (tipo de mercado), y 58 filas son idénticas.
- **`h03a` mezcla dos cosas:** la variedad (1 Rojolele o Cisadane o IR64, 2 Mentik, 5 otra) y la disponibilidad (6 o 7 sin existencias, 8 no se vende). El cuestionario usa códigos distintos de «sin existencias» según la calidad (6 en alta, 7 en media, 8 en baja, donde 8 es también «no se vende»).
- Mini-CFS de quienes viven fuera de las EA: `mkd_km5` (`mkid14` + `hpj3type`, 28.154 filas) trae precios de alimentos; `mkd_cov` tiene 4.032 áreas. No revisado en detalle.
- Otros: `bk1*` (jefe de comunidad, incluidos programas de protección social `bk1_pap*`, eventos `bk1_e2`, desastres `bk1_f*`), `bk2*`, `pkk*`, `inf*` (informantes), salud (`pusk*`, `pra*`, `pos*`, `pls*`, `tra`), escuelas (`sch*`), `sar*`.

## 11. Enlace con olas anteriores

- `htrack` de 2014 trae `hhid93`, `hhid97`, `hhid98`, `hhid00`, `hhid07`, `commid93`, `commid97`, `commid00`, `commid07`, `mkid00`, `mkid07`, códigos de ubicación de cada ola, `mover97`/`00`/`07`/`14` y los resultados de cada ola.
- `ptrack` de 2014 trae ids, `member`, edades (`age_93`-`age_14`) y resultados por libro de todas las olas (incluidos `res97ekm`, `res97ekb`, `res07bek1`, `res07bek2`), y los pesos de todas las olas.
- Para unir personas entre olas se usa `pidlink` (atención a los 3 repetidos de `ptrack` y a los 3 de 8 caracteres, §6.1).
- No se comprobó que `commid07` de `htrack` 2014 coincida con el `htrack` de 2007.

## 12. Preguntas abiertas (se deciden con todas las olas revisadas)

- **Unidad de comunidad:** EA (`ea`, 320) o `commid14` (311); cómo unir hogares con comunidades si `htrack` no trae `ea` (§10).
- **Hogares fuera de las EA:** 6.815 con `commid14` con letras; unión con el mini-CFS por `mkid14` (§6.1).
- **Roster:** qué códigos de `ar01a` quitar para que `pidlink` sea único (§6.1).
- **Códigos de `result14`:** codebook o guía (§7).
- **Precio del arroz en 2014-2015:** tres libros, calidades, unidades kg/litro, el 999998 de `hin_h` y la diferencia de fechas entre hogar y comunidad (§8, §10).
- **Salud mental:** CES-D-10 con una sola escala de frecuencia, distinta de 2007 (con filtro sí/no) y de 1993/2000 (otros ítems) (§9.2).
- **Pruebas cognitivas:** cómo puntuar; `_ans` mezcla incorrecto y sin respuesta; quién tomó qué versión en la cohorte de 0-5 años en 1997 (§9.4).
- **Choques:** el módulo ND de 2014 incluye choques económicos que no estaban en 2007; códigos D/E invertidos (§9.6).
- **Edad:** `age_14`, `bth_*` o `bk_ar1`; casos con diferencias de edad imposibles entre olas (§7).
- **Pesos:** con o sin ajuste por desgaste; transversales, longitudinales o de 5 olas (§6.4).

## 13. Lo que no está verificado

- Por qué los conteos de la guía de usuario (vol. 1: 16.204 hogares, 50.148 personas; vol. 2: 13.536 y 50.579) no coinciden con los archivos.
- La diferencia de filas de `schl` entre el archivo y el codebook.
- Qué códigos de `result14` son los correctos (codebook frente a guía) y qué significan 6 y 8.
- Por qué casi todos los libros 5 figuran como «parcialmente completos» y a qué archivo corresponde `res14bek`.
- Si las entrevistas proxy están en algún archivo.
- El significado de `resptype` en `ek_ek1` (se infirió de la edad) y que los ítems EK sean idénticos a los de 2000 y 2007.
- Si los códigos D/E de `ndtype` en los datos siguen al codebook o al cuestionario (solo se comparó la documentación).
- La relación entre `hhid14` y `hhid14_9`, y los 3 `pidlink` de 8 caracteres.
- Las llaves de los archivos marcados «no determinada», los valores extremos de talla, edad y precios, y las edades incoherentes entre olas.
- Que `commid07` en `htrack` 2014 coincida con `htrack` 2007; el código `3249` de 3 hogares.
- Los módulos marcados «no revisado».
