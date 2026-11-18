# IFLS2 (1997) · Catálogo, contenido y manejo de los datos

*Guía de la ronda 2 para el proyecto final de Ciencia de Datos. Escrita el 12-nov-2026 a partir de la documentación de RAND en `01_Datos/01_Crudos/IFLS2/Documentation` (sobre todo `volume2.pdf`, guía de usuario, y los codebooks de `volume5/` y `volume6/`) y de una revisión directa de los 126 archivos `.dta` de `Household Data` (incluidos `bek` y la carpeta `hh97usdta`, añadidos el 12-nov) y los 69 de `Community Data`. Los conteos y las pruebas de llaves salen de los archivos (Python + `pyreadstat`); lo demás, de la documentación citada.*

*La guía es **descriptiva**: documenta qué hay, cómo está codificado y qué problemas tiene. No decide qué variables serán resultado, control o muestra; las opciones quedan en §12 («Preguntas abiertas»).*

## 1. Qué es esta ronda

- **IFLS2.** Segunda ola del panel, reentrevista de los hogares de 1993 más los hogares nuevos formados por personas que se fueron de ellos (*split-off*).
- **Trabajo de campo.** Primera visita del libro K entre **agosto de 1997 y abril de 1998** (`bk_cov`, hogares entrevistados): 6.993 hogares en 1997 (277 en agosto, 1.175 en septiembre, 2.246 en octubre, 1.945 en noviembre, 1.350 en diciembre) y **627 en 1998** (415 en enero, 153 en febrero, 58 en marzo, 1 en abril). La guía de usuario habla de «agosto de 1997 a febrero de 1998»; los datos traen además marzo y abril.
- **Recontacto según RAND:** se entrevistó al menos a un miembro del 93,5 % de los hogares de 1993; en el 0,9 % todos habían muerto (`volume2.pdf`, sección de pesos).
- **Tamaño (archivos):** `htrack` lista 8.116 hogares, de los cuales **7.620 fueron entrevistados** (6.742 de origen y 878 *split-off*). `ptrack` lista 39.785 personas; 33.937 son miembros de un hogar en 1997.
- **Comunidades:** las mismas **312** de 1993 (`commid97`, 13 provincias).
- **Contenido nuevo frente a 1993:** evaluación de salud por enfermera para todos los miembros (libro US), pruebas cognitivas para personas de 7 a 24 años (libro EK, §9.4), libro proxy (3P) y precios de arroz en tiendas y mercados de cada comunidad (`bk2_hpj`).

## 2. Qué archivos hay y qué falta

- `Household Data/` tiene **seis subcarpetas** (`hh97bk`, `hh97b1` … `hh97b5`) y **14 archivos sueltos en la raíz** (`b3a_mg1`, `b3a_mg2`, `b3a_tk1`-`tk4`, `b3p_mg`, `b3p_tk1`, `b3p_tk2`, `b4_kl1`, `b4_kl2`, `bus_0`, `bus_1` y `bek`). Los sueltos pertenecen a los libros 3A, 3P, 4, US y EK. Además está la subcarpeta `hh97usdta/` (descargada el 12-nov) con `bus_0` y `bus_1`, **idénticos byte a byte** (mismo MD5) a los de la raíz: es una copia, no datos nuevos. Total: 128 archivos, 126 distintos. **Ya están descomprimidos** (no quedan `.zip` de datos).
- **Comparado con el apéndice A de `volume2.pdf` (127 archivos de hogar), faltaban dos:**
  - `BEK` (pruebas cognitivas): faltaba en la descarga inicial; **se descargó de RAND el 12-nov-2026** y está en la raíz de `Household Data/` (`bek.dta`, 24.288 filas, igual que el catálogo del Banco Mundial; el apéndice dice 22.081). No hay codebook de EK en `volume5/`, solo el cuestionario (`volume3/hh97bek.pdf`).
  - `B3P_TK4`: primer empleo, respuestas por proxy (1.217 registros según el apéndice).
- **Conteos distintos del apéndice en 20 archivos** (p. ej., `b3a_dl3`: 33.284 en el apéndice frente a 11.792 en disco; `b5_dla2`: 51.778 frente a 115; `b3b_ma1`: 437.624 frente a 537.084). Los conteos en disco coinciden con los del codebook (`volume5/`, fechado 28-may-2000) y con el catálogo del Banco Mundial; el apéndice parece describir una versión anterior. No se investigó más.
- **No hay codebook del libro US** (antropometría y salud) en `volume5/`: solo el cuestionario (`volume3/hh97bus.pdf`). Los códigos de US en esta guía salen del cuestionario y de los datos.
- **Formatos `.dta`:** los de hogar son versión 108 (Stata 6); los comunitarios son **versión 104, más antigua**. Ver la trampa de faltantes en §6.3.

## 3. Mapa de la documentación

| Archivo en `Documentation/` | Qué es | Cuándo usarlo |
|---|---|---|
| `volume1.pdf` | Diseño y resultados principales: muestra, recontacto, contenido de cada libro | Para la sección de datos del informe |
| `volume2.pdf` | **Guía de usuario**: ids, estructura de archivos, códigos especiales, pesos, `htrack`/`ptrack`, enlace con IFLS1. Apéndice C: notas por módulo; apéndice D: casos especiales | **Leer primero** |
| `volume3/` | Cuestionarios de hogar (un PDF por libro, incluidos US y EK) | Redacción exacta y saltos |
| `volume4/` | Cuestionarios comunitarios y de establecimientos (**en `.zip` sin extraer**) | Si se usan datos comunitarios |
| `volume5/` | **Codebook de hogar** (un PDF por libro + `hh97trk.pdf` para `htrack`/`ptrack`). Sin US ni EK | Códigos y frecuencias de cada variable |
| `volume6/` | Codebook comunitario y de establecimientos | Ídem para `Community Data` |
| `volume7.pdf` | **Crosswalk IFLS1-IFLS2**: correspondencia de preguntas entre olas | Al comparar variables con 1993 |
| `BEK_*_Indonesian/` (descargado el 12-nov) | Cuadernillos de las pruebas EK en indonés (matemáticas y bahasa), uno por nivel (7-9, 10-12, 13-15, 16-24). Son escaneos sin texto; no traen clave de respuestas | Para ver el contenido de las pruebas |
| `BEK_7-12_English/` (descargado el 12-nov) | Traducción al inglés de las pruebas de 7-9 y 10-12 (matemáticas y bahasa), 30 ítems cada una, **con clave de respuestas**. No hay versión en inglés de 13-15 ni de 16-24 | Para identificar las pruebas en `bek` (§9.4) |

## 4. Libros y quién responde (según `volume2.pdf`, sección 2)

| Libro | Quién responde | N en datos |
|---|---|---:|
| K · Control y roster (`bk_ar1`) | Informante del hogar; roster preimpreso con los miembros de 1993 en hogares de origen | 39.714 filas de roster |
| 1 · Consumo | Miembro de 18+ conocedor del hogar (en general, la mujer jefa) | 7.566 hogares |
| 2 · Economía del hogar | Ídem (en general, el hombre jefe) | 7.600 hogares |
| 3A y 3B · Adultos | **Todos los miembros actuales de 15+ en hogares de origen**; en *split-off*, la persona seguida, su cónyuge y sus hijos biológicos | 19.910 (3A) y 19.892 (3B) |
| 3P · Proxy | Otra persona responde por un adulto que no pudo; trae menos información que 3A/3B/4 (cuadro 2.1 de `volume2.pdf`) | 1.653 |
| 4 · Mujeres | Mujeres alguna vez casadas de 15-49, más las que respondieron el libro 4 en 1993 aunque hoy tengan 50+ | 6.160 |
| 5 · Niños | Todos los menores de 15. De 11 a 14 años responden ellos; menores de 11, un adulto (en general la madre) | 10.356 |
| US · Evaluación de salud | Enfermera o enfermero mide a todos los miembros; RAND reporta ≈85 % de cobertura | 37.980 filas (ver §9.1) |
| EK · Pruebas cognitivas | Personas de 7 a 24 años (dos pruebas por persona) | 24.288 filas, 12.143 personas |

Resultado por persona en `ptrack`:

| Libro | Hecho por la persona | Hecho por proxy / adulto | No hecho |
|---|---:|---:|---:|
| 3A | 19.910 | 1.652 | 1.633 |
| 3B | 19.892 | 1.653 | 1.650 |
| 4 | 6.160 | 154 | 369 |
| 5 | 2.893 (el niño) | 7.492 (un adulto) | 374 |

**Diferencia con 1993:** en 1993 el libro III se aplicó a una submuestra de adultos (jefe y cónyuge, una persona de 50+ y, en ¼ de los hogares, una de 15-49). En 1997 se buscó a **todos** los adultos de los hogares de origen.

**Panel y nuevos.** En los módulos retrospectivos (educación, matrimonio, migración, empleo, embarazos, anticoncepción), quienes respondieron en 1993 solo actualizan lo ocurrido desde entonces; los nuevos dan la historia completa. Para tener la historia completa de un respondiente de panel hay que unir 1993 y 1997 (`volume2.pdf`, cuadro 2.2).

## 5. Catálogo de archivos

La etiqueta es la oficial de RAND. «Llave única» es la combinación de variables que identifica cada fila, **comprobada en los archivos**; «no determinada» significa que ninguna combinación estándar resultó única (ver §6.1).

**Libro K y seguimiento**

| Archivo | Etiqueta RAND | Llave única (verificada) | N |
|---|---|---|---:|
| `bk_ar0` | Bk K Household size | `hhid97` | 7.620 |
| `bk_ar1` | Bk K Household roster | `hhid97` + `pid97` | 39.714 |
| `bk_cov` | Bk K Cover (Control Book) | `hhid97` | 8.116 |
| `bk_krk` | Bk K Household characteristics | `hhid97` | 7.620 |
| `bk_sc` | Bk K Location and sampling | `hhid97` | 7.637 |
| `htrack` | HH-level tracking across waves | `hhid97` | 8.116 |
| `ptrack` | Person-level tracking across waves | `pidlink` | 39.785 |

**Libro 1 (consumo)**

| Archivo | Etiqueta RAND | Llave única (verificada) | N |
|---|---|---|---:|
| `b1_cov` | Bk 1 Cover (HH Economy) | `hhid97` | 7.608 |
| `b1_ks0` | Bk 1 Consumption (1)-Misc. | `hhid97` | 7.566 |
| `b1_ks1` | Bk 1 Consumption (2)-Food | `hhid97` + `ks1type` | 279.942 |
| `b1_ks2` | Bk 1 Consumption (3)-Non food mthly | `hhid97` + `ks2type` | 68.094 |
| `b1_ks3` | Bk 1 Consumption (4)-Non food ann | `hhid97` + `ks3type` | 52.962 |
| `b1_ks4` | Bk 1 Consumption (5)-Prices | `hhid97` + `ks4type` | 37.830 |
| `b1_pp1` | Bk 1 Health facilities | `hhid97` + `pptype` | 83.226 |

**Libro 2 (economía del hogar)**

| Archivo | Etiqueta RAND | Llave única (verificada) | N |
|---|---|---|---:|
| `b2_cov` | Bk 2 Cover (HH Bus. wealth) | `hhid97` | 7.616 |
| `b2_ge` | Bk 2 HH econ hardships | `hhid97` + `getype` | 45.600 |
| `b2_hi` | Bk 2 HH Non labor income | `hhid97` + `hitype` | 68.400 |
| `b2_hr1` | Bk 2 HH Assets (1)-grid | `hhid97` + `hrtype` | 83.600 |
| `b2_hr2` | Bk 2 HH Assets (2)-debts | `hhid97` | 7.600 |
| `b2_kr` | Bk 2 Housing characs | `hhid97` | 7.600 |
| `b2_nt1` | Bk 2 Non farm business (1)-income | `hhid97` | 7.600 |
| `b2_nt2` | Bk 2 Non farm business (2)-assets | `hhid97` + `nttype` | 23.625 |
| `b2_ut1` | Bk 2 Farm business (1)-income | `hhid97` | 7.600 |
| `b2_ut2` | Bk 2 Farm business (2)-assets | `hhid97` + `uttype` | 23.310 |

**Libros 3A, 3B y 3P (adultos y proxy)**

| Archivo | Etiqueta RAND | Llave única (verificada) | N |
|---|---|---|---:|
| `b3a_br` | Bk 3A Pregnancy summary | `pidlink` | 2.187 |
| `b3a_cov` | Bk 3A Cover (Individ Adult) | `pidlink` | 20.529 |
| `b3a_dl1` | Bk 3A Education (1) | `pidlink` | 19.910 |
| `b3a_dl2` | Bk 3A Education (2) | `pidlink` + `dl2type` | 17.598 |
| `b3a_dl3` | Bk 3A Education (3)-grid | `pidlink` + `dl3type` | 11.792 |
| `b3a_dl4` | Bk 3A Education (4)-expenses | `pidlink` | 8.321 |
| `b3a_dlr1` | Bk 3A Youth educ/emp (1)-summary | `pidlink` | 5.333 |
| `b3a_dlr2` | Bk 3A Youth educ/emp (2)-disruptions | `pidlink` + `dlr04x` | 145 |
| `b3a_hi` | Bk 3A Individ non labor inc | `pidlink` + `hitype` | 179.190 |
| `b3a_hr0` | Bk 3A Individ assets (1)-screen | `pidlink` | 19.910 |
| `b3a_hr1` | Bk 3A Individ assets (2)-grid | `pidlink` + `hrtype` | 75.977 |
| `b3a_hr2` | Bk 3A Individ assets (3)-debts | `pidlink` | 6.907 |
| `b3a_kw1` | Bk 3A Marriage (1)-screen | `pidlink` | 19.910 |
| `b3a_kw2` | Bk 3A Marriage (2)-current | `pidlink` | 8.503 |
| `b3a_kw3` | Bk 3A Marriage (3)-history | `pidlink` + `kwn` | 9.831 |
| `b3a_pk1` | Bk 3A HH decision making (1) | `pidlink` | 16.994 |
| `b3a_pk2` | Bk 3A HH decision making (2) | `pidlink` + `pk2type` | 211.021 |
| `b3a_pk3` | Bk 3A HH decision making (3) | `pidlink` + `pk3type` | 99.304 |
| `b3b_ak` | Bk 3B Health insurance | `pidlink` + `aktype` | 119.352 |
| `b3b_ba0` | Bk 3B Non-HH mems (1)-parents | `pidlink` | 19.892 |
| `b3b_ba1` | Bk 3B Non-HH mems (2)-transfers | `pidlink` | 9.144 |
| `b3b_ba2` | Bk 3B Non-HH mems (3)-sibs (summary) | `pidlink` | 19.892 |
| `b3b_ba3` | Bk 3B Non-HH mems (4)-sibs (roster) | no determinada (§6.1) | 53.457 |
| `b3b_ba4` | Bk 3B Non-HH mems (5)-sibs (transfers) | `pidlink` | 19.892 |
| `b3b_ba5` | Bk 3B Non-HH mems (6)-kids (summary) | `pidlink` | 19.892 |
| `b3b_ba6` | Bk 3B Non-HH mems (7)-kids (roster) | no determinada (§6.1) | 10.713 |
| `b3b_cov` | Bk 3B Cover (Individ Adult) | `pidlink` | 20.521 |
| `b3b_kk` | Bk 3B Self assessed health | `pidlink` | 19.892 |
| `b3b_km` | Bk 3B Smoking | `pidlink` | 19.892 |
| `b3b_ma1` | Bk 3B Acute morbidity | `pidlink` + `matype` | 537.084 |
| `b3b_ma2` | Bk 3B Morbidity-symptoms | `pidlink` | 19.892 |
| `b3b_pm1` | Bk 3B Community participation (1) | `pidlink` + `pm1type` | 159.136 |
| `b3b_pm2` | Bk 3B Community participation (2) | `pidlink` | 19.892 |
| `b3b_pm3` | Bk 3B Community participation (3) | `pidlink` + `pm3type` | 238.704 |
| `b3b_ps` | Bk 3B Self-treatment | `pidlink` + `pstype` | 139.244 |
| `b3b_rj1` | Bk 3B Outpatient care (1)-use | no determinada (§6.1) | 159.136 |
| `b3b_rj2` | Bk 3B Outpatient care (2)-events | `pidlink` + `rj2type` | 4.597 |
| `b3b_rn1` | Bk 3B Hospitalization (1)-use | no determinada (§6.1) | 99.907 |
| `b3b_rn2` | Bk 3B Hospitalization (2)-events | `pidlink` + `rn2type` | 476 |
| `b3p_ba0` | Bk 3P(roxy) Non HHM (1)-parents | `pidlink` | 1.653 |
| `b3p_ba1` | Bk 3P(roxy) Non HHM (2)-transfers | `pidlink` | 549 |
| `b3p_ba2` | Bk 3P(roxy) Non HHM (3)-sibs (summary) | `pidlink` | 1.653 |
| `b3p_ba3` | Bk 3P(roxy) Non HHM (4)-sibs (roster) | no determinada (§6.1) | 3.349 |
| `b3p_ba4` | Bk 3P(roxy) Non HHM (5)-sibs (transfrs) | `pidlink` | 1.653 |
| `b3p_ba5` | Bk 3P(roxy) Non HHM (6)-kids (summary) | `pidlink` | 1.653 |
| `b3p_ba6` | Bk 3P(roxy) Non HHM (7)-kids (roster) | no determinada (§6.1) | 1.413 |
| `b3p_br` | Bk 3P(roxy) Pregnancy summary | `pidlink` | 1.653 |
| `b3p_ch0` | Bk 3P(roxy) Pregnancy history (1) | `pidlink` | 606 |
| `b3p_ch1` | Bk 3P(roxy) Pregnancy history (2) | `pidlink` + `ch05` | 83 |
| `b3p_cov` | Bk 3P(roxy) Cover (Individ Adult) | `pidlink` | 1.655 |
| `b3p_cx` | Bk 3P(roxy) Contraception | `pidlink` | 606 |
| `b3p_dl1` | Bk 3P(roxy) Education (1) | `pidlink` | 1.653 |
| `b3p_dl3` | Bk 3P(roxy) Education (3)-grid | `pidlink` + `dl3type` | 830 |
| `b3p_dl4` | Bk 3P(roxy) Education (4)-expenses | `pidlink` | 1.205 |
| `b3p_kk` | Bk 3P(roxy) Health status | `pidlink` | 1.653 |
| `b3p_km` | Bk 3P(roxy) Smoking | `pidlink` | 1.653 |
| `b3p_kw1` | Bk 3P(roxy) Marriage | `pidlink` | 1.653 |
| `b3p_ma` | Bk 3P(roxy) Acute morbidity | `pidlink` + `matype` | 44.631 |
| `b3p_pm1` | Bk 3P(roxy) Commun partic (1) | `pidlink` | 1.653 |
| `b3p_pm2` | Bk 3P(roxy) Commun partic (2)activities | `pidlink` + `pm2type` | 19.836 |
| `b3p_rj1` | Bk 3P(roxy) Outpatient care (1)-use | no determinada (§6.1) | 13.224 |
| `b3p_rj2` | Bk 3P(roxy) Outpatient care (2)-events | `pidlink` + `rj2type` | 406 |
| `b3p_rn1` | Bk 3P(roxy) Hospitalization (1)-use | no determinada (§6.1) | 8.315 |
| `b3p_rn2` | Bk 3P(roxy) Hospitalization (2)-events | `pidlink` + `rn2type` | 56 |

**Libro 4 (mujeres alguna vez casadas)**

| Archivo | Etiqueta RAND | Llave única (verificada) | N |
|---|---|---|---:|
| `b4_ba6` | Bk 4 Non-HH members-children | no determinada (§6.1) | 13.322 |
| `b4_bf` | Bk 4 Breastfeeding (Panel resp.) | `pidlink` | 3.984 |
| `b4_br` | Bk 4 Pregnancy summary | `pidlink` | 6.160 |
| `b4_bx6` | Bk 4 Non-HH members-children | `pidlink` + `bx63a` | 295 |
| `b4_ch0` | Bk 4 Pregnancy history (1) | `pidlink` | 6.160 |
| `b4_ch1` | Bk 4 Pregnancy history (2) | `pidlink` + `ch05` | 5.702 |
| `b4_cov` | Bk 4 Cover (Ever marr female) | `pidlink` | 6.269 |
| `b4_cx1` | Bk 4 Contraception (1) | `pidlink` + `cx1type` | 49.280 |
| `b4_cx2` | Bk 4 Contraception (2) | `pidlink` | 6.160 |
| `b4_kw1` | Bk 4 Marriage | `pidlink` | 6.160 |
| `b4_kw2` | Bk 4 Marital history | `pidlink` + `kwn` | 6.785 |

**Libro 5 (niños)**

| Archivo | Etiqueta RAND | Llave única (verificada) | N |
|---|---|---|---:|
| `b5_cov` | Bk 5 Cover (Child) | `pidlink` | 10.415 |
| `b5_dla1` | Bk 5 Child's education (1) | `pidlink` | 10.356 |
| `b5_dla2` | Bk 5 Child's education (2)-disruptions | `pidlink` + `dla2type` | 115 |
| `b5_dla3` | Bk 5 Child's education (3)-history | `pidlink` + `dla3type` | 7.295 |
| `b5_maa0` | Bk 5 Child's health status | `pidlink` | 10.356 |
| `b5_maa1` | Bk 5 Child's acute morbidity | `pidlink` + `maatype` | 279.612 |
| `b5_psa` | Bk 5 Self-treatment | `pidlink` + `psatype` | 72.492 |
| `b5_rja0` | Bk 5 Out patient care-(1) use | `pidlink` | 10.356 |
| `b5_rja1` | Bk 5 Out patient care-(2) services | `pidlink` + `rja1type` | 12.880 |
| `b5_rja2` | Bk 5 Out patient care-(3) events | `pidlink` + `rja2type` | 2.104 |
| `b5_rja3` | Bk 5 Out patient care-(4) vaccin | `pidlink` | 10.356 |
| `b5_rna1` | Bk 5 Hospitalization - (1) use | no determinada (§6.1) | 51.780 |
| `b5_rna2` | Bk 5 Hospitalization - (2) events | `pidlink` + `rna2type` | 146 |

**Sueltos en la raíz de `Household Data/` (libros 3A, 3P, 4 y US)**

| Archivo | Etiqueta RAND | Llave única (verificada) | N |
|---|---|---|---:|
| `b3a_mg1` | Bk 3A Migration (1)-birthplace | `pidlink` | 19.910 |
| `b3a_mg2` | Bk 3A Migration (2)-history | `pidlink` + `movenum` | 16.250 |
| `b3a_tk1` | Bk 3A Work history (1)-screen | `pidlink` | 19.910 |
| `b3a_tk2` | Bk 3A Work history (2)-current job | `pidlink` | 11.964 |
| `b3a_tk3` | Bk 3A Work history (3)-history | `pidlink` + `tk28yr` | 100.453 |
| `b3a_tk4` | Bk 3A Work history (4)-first job | `pidlink` | 14.293 |
| `b3p_mg` | Bk 3P(roxy) Migration | `pidlink` | 1.653 |
| `b3p_tk1` | Bk 3P(roxy) Work (1)-screen | `pidlink` | 1.653 |
| `b3p_tk2` | Bk 3P(roxy) Work (2)-current job | `pidlink` | 916 |
| `b4_kl1` | Bk 4 Contraceptive calendar (1) | `pidlink` | 6.160 |
| `b4_kl2` | Bk 4 Contraceptive calendar (2) | `pidlink` + `year` + `month` | 634.169 |
| `bus_0` | Bk US Health Assess (0)-HH summary | no determinada (§6.1) | 7.485 |
| `bek` | Bk EK Math/Bah Indonesia assessments | no determinada (§6.1) | 24.288 |
| `bus_1` | Bk US Health Assess (1)-Individ msr | `hhid97` + `pid97` | 37.980 |

**Comunidad y establecimientos (`Community Data/`)**

| Archivo | Etiqueta RAND | Llave única (verificada) | N |
|---|---|---|---:|
| `adat1` | (sin etiqueta) | `commid97` | 304 |
| `adat2` | (sin etiqueta) | `commid97` + `adattype` | 608 |
| `adat_ap1` | (sin etiqueta) | `commid97` + `ap1type` | 1.216 |
| `bk1` | (sin etiqueta) | `commid97` | 313 |
| `bk1_a` | (sin etiqueta) | `commid97` + `atype` | 2.817 |
| `bk1_b` | (sin etiqueta) | `commid97` + `btype` | 1.818 |
| `bk1_d1` | (sin etiqueta) | `commid97` + `d1type` | 1.565 |
| `bk1_d2` | (sin etiqueta) | `commid97` + `d2type` | 284 |
| `bk1_d3` | (sin etiqueta) | `commid97` + `d3type` | 939 |
| `bk1_d4` | (sin etiqueta) | `commid97` + `d4type` | 1.565 |
| `bk1_d5` | (sin etiqueta) | `commid97` + `d5type` | 1.565 |
| `bk1_e1` | (sin etiqueta) | `commid97` | 13 |
| `bk1_e2` | (sin etiqueta) | `commid97` + `e2type` | 3.443 |
| `bk1_g` | (sin etiqueta) | `commid97` + `gtype` | 2.191 |
| `bk1_i` | (sin etiqueta) | `commid97` + `itype` | 939 |
| `bk1_j` | (sin etiqueta) | `commid97` + `jtype` | 1.252 |
| `bk1_k` | (sin etiqueta) | `commid97` + `ktype` | 576 |
| `bk1_pmkd` | (sin etiqueta) | `commid97` + `pmkdtype` | 5.008 |
| `bk1_rw` | (sin etiqueta) | `commid97` + `rwtype` | 689 |
| `bk2` | (sin etiqueta) | `commid97` | 312 |
| `bk2_hpj` | (sin etiqueta) | `commid97` + `hpj1type` + `hpj3type` | 9.360 |
| `bk2_ka1` | (sin etiqueta) | `commid97` + `ka1type` | 1.248 |
| `bk2_ka2` | (sin etiqueta) | `commid97` + `ka2type` | 3.432 |
| `pkk` | (sin etiqueta) | `commid97` | 310 |
| `pkk_h` | (sin etiqueta) | `commid97` + `htype` | 12.090 |
| `pkk_i` | (sin etiqueta) | `commid97` + `itype` | 930 |
| `pkk_j` | (sin etiqueta) | `commid97` + `jtype` | 1.240 |
| `pkk_kr` | (sin etiqueta) | `commid97` + `krtype` | 390 |
| `pkk_pm` | (sin etiqueta) | `commid97` + `pmtype` | 3.410 |
| `pm` | (sin etiqueta) | `commid97` | 303 |
| `pos` | (sin etiqueta) | no determinada (§6.1) | 619 |
| `pos_b1` | (sin etiqueta) | no determinada (§6.1) | 6.190 |
| `pos_b2` | (sin etiqueta) | no determinada (§6.1) | 7.428 |
| `pos_c` | (sin etiqueta) | no determinada (§6.1) | 4.333 |
| `pos_d` | (sin etiqueta) | no determinada (§6.1) | 8.047 |
| `pos_h` | (sin etiqueta) | no determinada (§6.1) | 24.141 |
| `pra` | (sin etiqueta) | no determinada (§6.1) | 1.832 |
| `pra_b1` | (sin etiqueta) | no determinada (§6.1) | 12.824 |
| `pra_b2` | (sin etiqueta) | no determinada (§6.1) | 73.280 |
| `pra_b3` | (sin etiqueta) | no determinada (§6.1) | 7.295 |
| `pra_b4` | (sin etiqueta) | no determinada (§6.1) | 14.656 |
| `pra_c1` | (sin etiqueta) | no determinada (§6.1) | 36.640 |
| `pra_c2` | (sin etiqueta) | no determinada (§6.1) | 36.640 |
| `pra_d1` | (sin etiqueta) | no determinada (§6.1) | 49.464 |
| `pusk` | (sin etiqueta) | no determinada (§6.1) | 922 |
| `pusk_b1` | (sin etiqueta) | `fcode` | 921 |
| `pusk_c1` | (sin etiqueta) | `fcode` + `c1type` | 35.919 |
| `pusk_c2` | (sin etiqueta) | `fcode` + `c2type` | 4.605 |
| `pusk_c3` | (sin etiqueta) | `fcode` + `c3type` | 10.131 |
| `pusk_d` | (sin etiqueta) | `fcode` + `dtype` | 6.559 |
| `pusk_e1` | (sin etiqueta) | `fcode` + `e1type` | 20.262 |
| `pusk_e2` | (sin etiqueta) | `fcode` + `e2type` | 11.973 |
| `pusk_f` | (sin etiqueta) | `fcode` + `ftype` | 25.788 |
| `sar` | (sin etiqueta) | `commid97` + `fcode` | 15.260 |
| `sd` | (sin etiqueta) | no determinada (§6.1) | 964 |
| `sd_b2` | (sin etiqueta) | no determinada (§6.1) | 5.784 |
| `sd_b3` | (sin etiqueta) | `fcode` + `b3type` | 2.250 |
| `sd_b4` | (sin etiqueta) | no determinada (§6.1) | 8.676 |
| `sd_c` | (sin etiqueta) | no determinada (§6.1) | 1.927 |
| `smp` | (sin etiqueta) | `fcode` | 945 |
| `smp_b2` | (sin etiqueta) | `fcode` + `b2type` | 5.670 |
| `smp_b3` | (sin etiqueta) | `fcode` + `b3type` | 1.152 |
| `smp_b4` | (sin etiqueta) | `fcode` + `b4type` | 8.505 |
| `smp_c` | (sin etiqueta) | `fcode` + `ctype` | 1.890 |
| `smu` | (sin etiqueta) | `fcode` | 618 |
| `smu_b2` | (sin etiqueta) | `fcode` + `b2type` | 3.708 |
| `smu_b3` | (sin etiqueta) | `fcode` + `b3type` | 900 |
| `smu_b4` | (sin etiqueta) | `fcode` + `b4type` | 5.562 |
| `smu_c` | (sin etiqueta) | `fcode` + `ctype` | 1.235 |

## 6. Cómo manejar los datos

### 6.1 Identificadores (verificados en los archivos)

| Variable | Tipo | Qué es | Notas |
|---|---|---|---|
| `hhid97` | texto, 7 | EA (3) + hogar (2) + origen/*split-off* (2) | `00` = hogar de origen; `1x` = *split-off* (en los entrevistados: 792 con `11`, 81 con `12` y 5 con `13`) |
| `pid97` | número | Línea de la persona en el roster de 1997 (`bk_ar1`) | |
| `pidlink` | texto, 9 | Persona, constante entre olas | Único en `ptrack`. **No es único** en `bk_ar1` (1.464 repetidos) ni en `bus_1` (1.245 personas en dos filas) |
| `hhid93`, `pid93` | texto / número | Ids de 1993 | En `htrack`, `hhid93` está vacío para los 878 *split-off* entrevistados; su origen se rastrea con `ptrack` |
| `commid97` | texto, 4 | Provincia (2) + secuencia (2) | Está en `htrack`, no en los archivos de hogar: hay que pegarlo antes de unir con datos comunitarios |
| `fcode` | texto, 7 | Establecimiento: `commid97` (4) + tipo (1) + secuencia (2) | Según RAND, la comunidad incluida en `fcode` no es necesariamente donde está el establecimiento; los establecimientos que sirven a cada comunidad están en `sar` |

**Por qué se repite `pidlink`.** Una persona que dejó su hogar de 1993 aparece en el roster del hogar de origen (como «ya no vive aquí», `ar01a` = 3) y en el de su *split-off* (`ar01a` = 4). La guía de usuario indica identificar personas dentro de IFLS2 con `hhid97` + `pid97`. En `bus_1` pasa lo mismo: entre las filas con talla medida no hay `pidlink` repetidos.

**Archivos sin llave única** con las combinaciones estándar (ver catálogo):

- `b3b_rj1`, `b3b_rn1`, `b5_rna1` y sus versiones proxy (uso de servicios de salud): tienen **filas duplicadas exactas** (135.040, 97.225 y 51.070 filas involucradas en los de libro 3B y 5).
- `b3b_ba3`, `b3b_ba6`, `b4_ba6` y proxy (hermanos e hijos fuera del hogar): `hhid97` + `pid97` + `ppsib`/`ppchild` no basta; la llave no se determinó.
- Establecimientos (`pos*`, `pra*`, `pusk`, `sd*`): en cada tipo hay **un `fcode` repetido** (`3114470` en posyandu, `3406276` en práctica privada, `3251141` en puskesmas, `3331611` en primaria), lo que duplica sus filas en los archivos de detalle (p. ej., 78 filas en `pos_h`).
- `bus_0`: el hogar `2400900` aparece dos veces (una visita con resultado 2 y otra con resultado 1).
- `bek`: `hhid97` + `pid97` + `ektype` casi es única. Hay 3 excepciones: dos personas con dos filas de la prueba `3` y puntajes distintos (`1801100`-3 con 5 y 18; `2210100`-3 con 9 y 12), y una fila duplicada exacta (`3011900`-5, prueba `2`, no intentada).

### 6.2 Códigos especiales y variables X (`volume2.pdf`, sección 3)

- **Variables X.** Muchas preguntas numéricas tienen una variable `…x` que dice si hubo respuesta válida (casi siempre 1 = dio valor, 8 = no sabe) y, a veces, la unidad. El valor numérico está en la variable sin `x`. Ejemplo: `us04x` (¿se midió la talla?) y `us04` (talla).
- **Último dígito del código especial:** 5 fuera de rango, 6 no aplica, 7 rechazó, 8 no sabe, 9 faltante. Faltantes numéricos: 9 o «.»; de texto: «z» o vacío.
- **Sí / no = 1 / 3; sexo = 1 hombre / 3 mujer**, como en 1993.
- **Años con cuatro dígitos** (`1997`, `1998`), a diferencia de 1993 (dos dígitos).
- `ptrack$age_97` y `age_93` vienen **como texto**, con el código `998` (8 miembros de 1997).

### 6.3 Trampa: faltantes de los archivos comunitarios

Los 69 archivos de `Community Data` están en el formato `.dta` 104. Leídos con `pyreadstat`, **68 de ellos traen valores 1,7498 × 10¹⁰⁰** en lugar de faltantes (2.504.420 celdas en total). Los archivos de hogar (formato 108) no tienen este problema. Hay que convertir esos valores a `NA` antes de calcular nada. **No se comprobó** si `haven::read_dta()` en R los lee bien.

### 6.4 Proxy

RAND recomienda **anexar** los archivos del libro 3P a los correspondientes de 3A, 3B y 4 para cubrir a todos los adultos (`volume2.pdf`, sección 3 y cuadro 3.1). Los módulos proxy tienen menos variables y más opciones de «no sabe». En el libro 5, el 72 % de las entrevistas las respondió un adulto por el niño.

### 6.5 Formato largo

Igual que en 1993, muchos archivos tienen varias filas por hogar o persona, identificadas por una variable `…type` (consumo `b1_ks1`, activos `b2_hr1`, choques `b2_ge`, síntomas `b3b_ma1`, historia laboral `b3a_tk3`, calendario anticonceptivo `b4_kl2`). Hay que resumirlos o pivotarlos antes de unir.

### 6.6 Pesos

| Archivo | Variable | Qué es (según `volume2.pdf`) |
|---|---|---|
| `htrack` | `hwt93` | Peso de hogar de 1993 (= `hhwt224` de IFLS1) |
| `htrack` | `hwt93smp` | Peso de hogar 1993 para la muestra objetivo |
| `htrack` | `hwt97l` | Longitudinal de hogar: representa la población de 1993, corrige desgaste |
| `htrack` | `hwt97x` | Transversal de hogar: representa 1997 (ajustado a SUSENAS 1997) |
| `ptrack` | `pwt93`, `pwt93in`, `pwt93us` | Pesos de persona de 1993 (roster, respondiente principal, antropometría) |
| `ptrack` | `pwt97l`, `pwt97inl` | Longitudinales de persona (0 para quienes entraron en 1997) |
| `ptrack` | `pwt97x` | Transversal de persona 1997 |

La guía de usuario menciona además `PWT97USL`, `PWT97USX` (evaluación de salud) y `PWT97EKX` (pruebas cognitivas). **No están en el `ptrack` de 1997, pero sí en el `ptrack` de IFLS3** (`pwt97usl`, `pwt97usx`, `pwt97ekx`). RAND advierte que el ajuste por desgaste incorpora supuestos de modelo y que se puede usar `hwt93` o un ajuste propio.

## 7. Seguimiento entre 1993 y 1997

**Hogares** (`htrack`, `result97`; códigos del codebook `hh97trk.pdf`):

| Resultado | N |
|---|---:|
| Entrevista hecha | 7.620 |
| Se unió a otro hogar IFLS | 10 |
| Todos los miembros objetivo muertos | 69 |
| Rechazo | 88 |
| Se mudó (misma provincia / otra provincia IFLS / provincia no IFLS / otro país / lugar desconocido) | 87 / 69 / 47 / 6 / 79 |
| No se pudo contactar / vivienda vacía / demolida / no encontrada | 7 / 3 / 3 / 28 |
| **Total** | **8.116** |

**Personas del roster de 1993** (33.081; `ptrack$ar01a_97`): 25.769 siguen en el mismo hogar, 1.464 están en un hogar *split-off*, 857 murieron, 3.456 dejaron el hogar y no se les ubicó en un hogar IFLS, y 1.535 no tienen información porque su hogar no se entrevistó. Solo se siguió a los «objetivo» (respondientes principales de 1993 y nacidos antes de 1968) cuando se mudaban.

**Comunidad de residencia en 1997.** `commid97` solo existe si el hogar vive en una de las 312 comunidades IFLS:

| Hogares entrevistados | Con `commid97` | Sin `commid97` |
|---|---:|---:|
| De origen | 6.354 | 388 |
| *Split-off* | 372 | 506 |

- 45 hogares tienen `commid97` distinto de `commid93`: se mudaron de una comunidad IFLS a otra.
- `mover97` (`htrack` y `bk_sc`): 6.125 no se movieron; 556 se movieron dentro de la misma desa, 202 dentro del kecamatan, 253 dentro del kabupaten, 324 dentro de la provincia y 160 a otra provincia IFLS. Definido solo para quienes se entrevistaron en ambas olas.
- `bk_sc` tiene 7.637 hogares: los 7.620 entrevistados y 17 con otros resultados.

## 8. Fechas de entrevista

| | 1997 | 1998 |
|---|---:|---:|
| Hogares entrevistados en una comunidad IFLS | 6.566 | 160 |
| Hogares entrevistados fuera de comunidades IFLS | 427 | 467 |

- **96 de las 312 comunidades** tienen al menos un hogar entrevistado en 1998; en ninguna supera la mitad de sus hogares.
- **Mediciones de salud (libro US):** 2.123 en 1998 (`us17yr`).
- **Pruebas cognitivas (libro EK):** 1.522 filas (764 personas) de 1998; 17 filas sin fecha.
- **Encuesta comunitaria:** el libro PKK se hizo en 1998 en 27 comunidades (21 en enero y 6 en febrero; 2 sin fecha); el libro 2 de la comunidad, también en 27. Los precios del arroz de esas comunidades (§10) son de enero o febrero de 1998.
- La submuestra de 1998 (IFLS2+) no forma parte de estos archivos.

## 9. Contenido por tema

### 9.1 Antropometría y salud física (`bus_1`)

- **Cobertura:** `bus_1` tiene 37.980 filas (el roster `bk_ar1` tiene 39.714), con una por persona listada, incluidas las que murieron o ya no viven en el hogar (`ar01a` 0 o 3). Talla válida (`us04x` = 1) en **28.816**; peso válido (`us06x` = 1) en 28.894. 15 filas tienen valor en `us04` sin `us04x` = 1.
- **Variables:** `us04` talla (cm, un decimal; 40,6 a 185,0); `us05` de pie (27.775) o acostado (1.041); `us06` peso (kg); presión arterial, pulso, capacidad pulmonar, prueba de sentarse y pararse, hemoglobina (`us13`) y salud general según la enfermera (`us14`).
- **Fechas:** nacimiento declarado en la medición (`us02day/mth/yr`, con variables X: año válido en 27.262, mes en 20.661, día en 15.802); edad (`us03`); fecha de medición (`us17day/mth/yr`).
- **`us00`** (¿se pudo medir?) trae los valores 0 (741) y 4 (576), que no figuran en el cuestionario; sin codebook no se sabe qué significan.
- **Niños:** según `ptrack`, hay 3.852 miembros de 0 a 5 años en 1997; 3.217 tienen talla medida y 1.273 ya estaban en el roster de 1993. Entre quienes tienen edad < 5 en `us03` (2.652), 8 declaran años de nacimiento entre 1977 y 1991, inconsistentes con esa edad.
- **Otras fuentes de edad:** `bk_ar1` (`ar08mth`, `ar08yr`, `ar09`) y `ptrack` (`bth_day/mth/yr`, `age_97`). No se ha revisado su consistencia con `us02`/`us03`.

### 9.2 Salud de adultos (`b3b_kk`, `b3b_ma1`)

- `b3b_kk` trae salud autorreportada (`kk01`), días de actividad perdidos y en cama, salud frente a hace 4 años (`kk02c`), enfermedades serias en los últimos 4 años y 9 actividades de la vida diaria (`kk03a`-`i`).
- **No hay ítems de síntomas psicológicos.** Los 6 síntomas de la sección KK de 1993 (insomnio, fatiga, irritabilidad, dolores, tristeza, ansiedad) no aparecen en 1997, ni en 3B ni en el proxy. Esto coincide con lo que reportan Friedman y Thomas (2009).
- `b3b_ma1`: 27 síntomas físicos de las últimas 4 semanas (dolor de cabeza, tos, fiebre, diarrea…), uno de ellos «cansado/resfriado» (`matype` P).

### 9.3 Educación

- **Adultos de 15+ (`b3a_dl1`, 19.910):** alfabetismo, si asistió alguna vez, si asiste hoy (`dl07a`, solo menores de 50) y fechas. **El nivel máximo y el grado (`dl06`, `dl07`) en `dl1` solo se preguntan a personas de 50+ (2.793).** Para los menores de 50, la historia está por nivel en `b3a_dl2` y `b3a_dl3` (grilla por escuela), y para los de panel solo se actualiza desde 1993.
- **Roster (`bk_ar1`):** `ar16` (nivel más alto) y `ar17` (grado) para todos los miembros, más `ar18c` (¿sigue estudiando?) tras un filtro de edad < 25 (`ar18a`).
- **Niños de menos de 15 (`b5_dla1`, 10.356):** 6.326 fueron alguna vez a la escuela y 5.971 siguen asistiendo. Puntajes EBTANAS (`dla23a`-`e`, `dla24`): 1.513 presentaron la prueba y 989 mostraron los puntajes.
- **Interrupciones escolares:** `b3a_dlr2` (145 episodios) y `b5_dla2` (115).

### 9.4 Cognición (libro EK)

- **Diseño (`volume1.pdf`):** personas de 7 a 24 años, pruebas de matemáticas e indonesio con ítems del EBTANAS, en cuatro niveles por edad (7-9, 10-12, 13-15, 16-24). En las primeras semanas el nivel más alto resultó demasiado difícil, y desde entonces todos los de 13-24 años hicieron la prueba de 13-15. El cuestionario (`hh97bek.pdf`) trae hojas de respuesta de 40 ítems de opción múltiple (A-D), 60 minutos por prueba.
- **Archivo (`bek.dta`, formato 108):** una fila por persona y prueba. Variables: `ektype` (qué prueba), `ek1` (1 intentó / 3 no intentó), `ek2` (motivo), `ekanswer` (respuestas ítem por ítem, como texto), `ekscore` (puntaje total), horas de inicio y fin, fecha, entrevistador.
- **`ektype` no tiene etiquetas** ni en el `.dta`, ni en `volume5/`, ni en el catálogo del Banco Mundial. Toma los valores `1`-`4` y `A`-`D`. Cada persona tiene exactamente un número y una letra del mismo nivel (`1`+`A`, `2`+`B`, `3`+`C`, `4`+`D`), y el nivel sigue la edad (cuadro).
- **Identificación con las claves en inglés (verificada para los niveles 1 y 2).** Se calcularon los aciertos de cada persona contra las claves de `BEK_7-12_English/`, probando desplazamientos de 0 a 10 posiciones en `ekanswer`, y se correlacionaron con `ekscore`:

| `ektype` | Mejor clave | Desplazamiento | Correlación con `ekscore` | Segunda mejor clave |
|---|---|---:|---:|---|
| `1` | Matemáticas 7-9 | 5 | 0,93 | Bahasa 7-9 (0,81) |
| `2` | Matemáticas 10-12 | 5 | 0,97 | Matemáticas 7-9 (0,64) |
| `A` | Bahasa 7-9 | 0 | 0,97 | Matemáticas 10-12 (0,77) |
| `B` | Bahasa 10-12 | 5 | 0,98 | Matemáticas 10-12 (0,76) |

  Es decir, **los números son matemáticas y las letras son bahasa Indonesia** en los niveles 1 y 2.
- **Confirmación para los cuatro niveles con IFLS3.** El `ptrack` de 2000 trae `res97ekm` (matemáticas) y `res97ekb` (bahasa) de 1997. El resultado de las pruebas con número coincide con `res97ekm` en el 99,8-100 % de los casos en cada nivel (frente a 95,6-97,9 % con `res97ekb`), y el de las letras con `res97ekb`. **Números = matemáticas y letras = bahasa también en los niveles 3 y 4.** La versión en inglés tiene 30 ítems, y las respuestas en `bek` tienen hasta 35 o 40: la versión aplicada tenía ítems que la traducción no trae (el desplazamiento de 5 sugiere 5 ítems adicionales al inicio en tres de las cuatro pruebas). Por eso las claves en inglés no bastan para recalificar las pruebas.
- **Contenido de los niveles 3 y 4.** El cuadernillo escaneado de matemáticas 13-15 tiene 40 ítems, algunos con 5 opciones (A-E). En `bek` aparecen respuestas «E» en los niveles 3 y 4 de ambos juegos (24-34 % de las pruebas de nivel 3, 83-92 % de las de nivel 4) y nunca en los niveles 1 y 2.

| `ektype` | Filas | Intentadas | Edad en 1997 (mediana; mín-máx) | Puntaje máx. observado | Largo más común de `ekanswer` |
|---|---:|---:|---|---:|---:|
| `1` / `A` | 2.108 / 2.108 | 1.405 / 1.410 | 8 (5-15) | 40 / 34 | 40 / 35 |
| `2` / `B` | 2.213 / 2.211 | 1.736 / 1.768 | 11 (7-21) | 39 / 38 | 40 / 40 |
| `3` / `C` | 7.073 / 7.071 | 4.106 / 4.169 | 17 (7-33) | 33 / 34 | 40 / 40 |
| `4` / `D` | 752 / 752 | 398 / 421 | 19 (15-25) | 23 / 27 | 33 / 35 |

- **Cobertura:** 12.143 personas. Edad en 1997 según `ptrack`: 12.079 de 7 a 24 años, 43 menores de 7 (todos en el nivel 1) y 20 mayores de 24. Hay 14.971 personas de 7 a 24 en `ptrack`; 12.079 tienen fila en `bek`. Una persona (2 filas) no se encuentra en `ptrack`.
- **Nivel 4** (el de 16-24, abandonado al inicio del campo): 752 personas, casi todas de 16 a 24 años. Los demás de 16-24 (4.500) hicieron el nivel 3.
- **Participación:** 7.565 personas intentaron las dos pruebas, 281 solo una y 4.296 ninguna. Motivos de no intentar (`ek2`, filas): rechazo 3.565, no se le pudo contactar 3.067, poca capacidad 1.305, no sabe leer ni escribir 920, otro 18. El código 5 («respondió un adulto por proxy») del cuestionario no aparece.
- `ek1` = 1 siempre tiene puntaje y `ek1` = 3 nunca lo tiene.
- **Tipos de dato:** `ekscore`, `ek2`, las horas y la fecha se leen como columnas de tipo objeto (enteros mezclados con faltantes); hay que convertirlas a número.
- **Peso:** `pwt97ekx` no está en el `ptrack` de 1997, pero sí en el `ptrack` de IFLS3 (7.837 personas con peso > 0).

### 9.5 Consumo de arroz (`b1_ks1`, ítem A)

- **Valor en rupias de la última semana**, sin cantidades: comprado (`ks02`) y de producción propia (`ks03`). De 7.566 hogares, 5.075 reportan compra positiva, 1.511 producción propia positiva y 193 ambas.
- `b1_ks4` (cantidades y precio pagado) **no incluye arroz**: solo aceite, azúcar, kangkung, carne de res y pollo.

### 9.6 Agricultura, activos y choques

- `b2_ut1`: 2.590 de 7.600 hogares tienen algún miembro agricultor en el último año. Hay ingreso, gasto y ganancia agrícola (`ut07`-`ut09`); activos agrícolas en `b2_ut2`.
- `b2_hr1`/`b3a_hr1`: activos del hogar y de la persona, en formato largo por tipo de activo.
- **`b2_ge`: choques de los últimos 5 años**, 6 tipos (muerte 1.115 hogares; enfermedad 1.212; pérdida de cosecha 891; desastre natural 175; desempleo 335; caída de ingreso 639). Año del choque: 1.688 casos en 1997. Razón de la pérdida de cosecha (`ge_c_rsn`, respuesta múltiple): «demasiado seco» en 431 de 960 menciones.

### 9.7 Otros módulos

Decisiones dentro del hogar (`b3a_pk*`), participación comunitaria (`b3b_pm*`), transferencias con familiares fuera del hogar (`b3b_ba*`), migración (`b3a_mg*`), historia laboral (`b3a_tk*`), seguros de salud (`b3b_ak`), uso de servicios de salud (`b3b_rj*`, `b3b_rn*`), embarazos y lactancia (`b4_*`), vacunas (`b5_rja3`).

## 10. Datos comunitarios de 1997

**Precios del arroz: tres fuentes.**

| Fuente | Archivo | Qué mide | Cobertura | Respuestas válidas | Unidad |
|---|---|---|---|---|---|
| Informante PKK | `pkk_h`, `htype` 1-3 | Precio por unidad, arroz de calidad alta, media y baja | 310 comunidades | 891 de 930 | kg 650, litro 165, otra 65, faltante 50 |
| Posyandu | `pos_h`, `htype` 1-3 | Ídem | 618 puestos en 308 comunidades (284 con 2 puestos) | 1.782 de 1.857 | kg 1.273, litro 406, otra 78, faltante 100 |
| Tiendas y mercados (visita del encuestador) | `bk2_hpj`, `hpj3type` = 1 | Arroz de calidad media en hasta 3 puntos de venta por comunidad | 312 comunidades | 633 precios por kg en 265 comunidades; 126 casos con precio en otra unidad (`hpj6`-`hpj8`) | kg |

Valores observados, en Rp por kg (solo respuestas válidas en kg; sin limpiar):

| Fuente | N | Mediana | p1 | p99 | Máximo |
|---|---:|---:|---:|---:|---:|
| PKK, calidad alta | 221 | 1.300 | 1.000 | 2.500 | 7.500 |
| PKK, calidad media | 221 | 1.200 | 800 | 1.740 | 1.800 |
| PKK, calidad baja | 208 | 1.000 | 600 | 1.500 | 9.000 |
| Tiendas/mercados, calidad media | 633 | 1.200 | 800 | 2.772 | 22.000 |

- Tipo de punto de venta en `bk2_hpj` (`hpj2`, filas de arroz): 508 puestos pequeños, 201 tiendas, 148 mercados y 79 faltantes.
- El posyandu se une a la comunidad por los 4 primeros dígitos de `fcode`.
- 27 comunidades tienen el libro PKK y el libro 2 levantados en enero o febrero de 1998 (§8).

**Otros archivos comunitarios.** `bk1` (jefe de comunidad: transporte, electricidad, agua, agricultura, programas) con sus anexos; `bk1_e2` registra eventos importantes de la comunidad, con años desde 1965 (incluye incendios, 92; inundaciones, 60; sequía, 28; el codebook no aclara si «incendios» incluye incendios forestales); `bk2` (estadísticas de la comunidad, uso del suelo); `adat*` (costumbres); `sar` (establecimientos disponibles por comunidad); `pusk*`, `pra*`, `pos*` (salud); `sd*`, `smp*`, `smu*` (escuelas).

## 11. Enlace con 1993 (verificado)

- Las 33.081 personas del roster de 1993 en `ptrack` (`member93` = 1) son exactamente los `pidlink` de `IFLS1/bukkar2`.
- Los 7.224 `hhid93` entrevistados en 1993 (`htrack$result93` = 1) son exactamente los de `IFLS1/bukkar1`.
- `htrack$commid93` coincide con el `commid93` de IFLS1 en todos los hogares.
- RAND hizo la versión IFLS1-RR para que las dos olas se unan directamente (`volume2.pdf`, sección 6). Para comparar preguntas entre olas está el crosswalk (`volume7.pdf`).

## 12. Preguntas abiertas (se deciden con todas las olas revisadas)

Esta guía no toma posición; solo indica qué información de 1997 sirve para cada una.

- **Comunidad de 1997 de quien se mudó:** `commid97` falta en 894 hogares entrevistados y 45 cambiaron de comunidad IFLS (§7).
- **Precio del arroz:** fuente (PKK, posyandu, mercado), calidad, unidades (kg o litro), valores extremos y comunidades con encuesta en 1998 (§8, §10).
- **Entrevistas de 1998:** 627 hogares y 27 comunidades (§8).
- **Respuestas por proxy:** libro 3P y libro 5 respondido por adultos (§4, §6.4).
- **Edad en meses para HAZ:** `us02`/`us03`, `bk_ar1` y `ptrack` (§9.1).
- **Pesos:** longitudinales o transversales; los pesos de US y EK de 1997 están en el `ptrack` de IFLS3 (§6.6).
- **Pruebas EK:** cómo tratar el nivel 4 y las personas fuera de 7-24, y cómo resumir los puntajes de niveles distintos (§9.4).
- **Escolaridad de 1997:** cómo armar el nivel máximo con `dl1` (solo 50+), las grillas `dl2`/`dl3`, el roster y la historia de 1993 (§9.3).
- **Producción y compra de arroz:** solo hay valores en rupias (§9.5) y datos agrícolas (§9.6).

## 13. Lo que no está verificado

- El número exacto de ítems de cada prueba aplicada en 1997 y qué ítems no están en la traducción al inglés.
- El significado de los valores 0 y 4 de `us00` (no hay codebook de US).
- Si `haven::read_dta()` lee bien los faltantes del formato 104 (§6.3).
- La llave de `b3b_ba3`, `b3b_ba6` y `b4_ba6`, y el origen de las filas duplicadas exactas de `rj1`/`rn1`/`rna1`.
- Por qué el apéndice A de `volume2.pdf` difiere en 20 conteos; parece una versión anterior.
- Los códigos 6-8 de la unidad de precio (`pkk_h$h02`) no tienen etiqueta en el codebook.
- Los montos en rupias no se han revisado (atípicos, montos en miles).
- La comparabilidad de las preguntas de precio y de consumo entre 1993 y 1997 no se ha revisado con el crosswalk.
- Las cifras de precio de §10 son sin limpiar: no se han convertido unidades ni revisado atípicos.
