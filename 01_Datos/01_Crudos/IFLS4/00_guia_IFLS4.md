# IFLS4 (2007-2008) · Catálogo, contenido y manejo de los datos

*Guía de la ronda 4 para el proyecto final de Ciencia de Datos. Escrita el 12-nov-2026 a partir de la documentación de RAND en `01_Datos/01_Crudos/IFLS4/Household Documentation` y `Community Documentation` (guía de usuario vol. 1 y 2, codebooks `.txt` y cuestionarios en PDF), y de una revisión directa de los 171 archivos `.dta` de `Household Data` y los 119 de `Community Data`. Los conteos y las pruebas de llaves salen de los archivos (Python + `pyreadstat`); lo demás, de la documentación citada.*

*La guía es **descriptiva**: documenta qué hay, cómo está codificado y qué problemas tiene. No decide qué variables serán resultado, control o muestra; las opciones quedan en §12 («Preguntas abiertas»).*

## 1. Qué es esta ronda

- **IFLS4.** Cuarta ola completa: hogares de 1993 con miembros vivos, todos los *split-off* de 1997, 1998 y 2000, y nuevos *split-off*.
- **Trabajo de campo.** Primera visita del libro K (`bk_cov`): **noviembre de 2007 a julio de 2008** (1.975 hogares en 2007 y 11.561 en 2008; 1 caso en octubre de 2007). La guía de usuario dice en un lugar «finales de noviembre de 2007 a finales de abril de 2008» y en otro «finales de noviembre de 2008 a mayo de 2009»; los datos confirman 2007-2008.
- **Tamaño (archivos):** `htrack` lista 15.146 hogares. **13.536 tienen el libro K hecho** (`res07bk` = 1; la guía de usuario habla de 13.535 entrevistados), de los cuales 6.429 son de origen y 7.107 *split-off* (704 de 1997, 261 de 1998, 2.109 de 2000 y 4.033 nuevos de 2007). `ptrack` lista 66.784 personas; 50.582 son miembros de un hogar en 2007.
- **Panel:** 6.010 hogares tienen `result` = 1 en 1993, 1997, 2000 y 2007.
- **Comunidades:** las mismas 312 más hogares fuera de ellas con `commid07` con letras, como en 2000 (§6.1).
- **Contenido nuevo o cambiado frente a 2000:**
  - salud mental con la **escala CES-D de 10 ítems** (§9.2), distinta de los ítems de 2000;
  - antropometría repartida en 7 archivos, con fuerza de agarre y colesterol (§9.1);
  - pruebas cognitivas con el mismo diseño de 2000, en dos archivos (§9.4);
  - **tres encuestas de precios** por comunidad: informante, mercado y *warung*/tienda (§10);
  - arroz subsidiado **Raskin** (§9.5);
  - **no hay** módulo general de choques económicos del hogar (§9.6);
  - libro proxy renombrado `bp_*` (antes `b3p_*`).

## 2. Qué archivos hay

- `Household Data/`: 171 archivos `.dta` en la raíz; `Community Data/`: 119. Formato `.dta` 111 (uno, `b3b_co2`, en 113). No hay `.zip` pendientes.
- **Los 290 archivos coinciden uno a uno, con el mismo número de registros, con las listas de módulos de los codebooks** (`ifls2007_hhd_*.txt`, `ifls2007_cf_*.txt`). No falta nada.
- **El apéndice A de la guía de usuario (vol. 2) no sirve para esta ola:** reproduce la lista y los conteos de IFLS3 (p. ej., `htrack` con 11.109 registros), no los de IFLS4.
- Sin etiquetas de archivo en los `.dta`; usar los codebooks.
- **Sin problemas de lectura** detectados: no hay valores 1,75e+100 ni enteros leídos como texto con `pyreadstat` (a diferencia de 1997 y 2000).

## 3. Mapa de la documentación

| Archivo | Qué es | Cuándo usarlo |
|---|---|---|
| `IFLS2007_UsersGuide_vol1-6-23-09.pdf` | Diseño, recontacto, seguimiento, contenido de los cuestionarios | Sección de datos del informe |
| `IFLS2007_UsersGuide_vol2.pdf` | Ids, `commid07`/`mkid07`, códigos, pesos, `htrack`/`ptrack`. **Su apéndice A es de IFLS3** | **Leer primero** (salvo el apéndice) |
| `ifls2007_hhd_*.txt` | Codebooks de hogar (incluidos `BUS`, `BEK`, `BP`, `BT`, `HTRACK`, `PTRACK`) | Códigos y frecuencias |
| `hh07_english_pqx/`, `hh07_bahasa_indonesia_pqx/` | Cuestionarios de hogar en inglés e indonesio, incluidas las pruebas EK1 (7-14) y EK2 (15-24) | Redacción exacta |
| `ifls2007_cf_*.txt`, `cf07_*_pqx/`, `IFLS4 MINIKAMADES.pdf` | Codebooks y cuestionarios comunitarios, de precios y del mini-CFS | Datos comunitarios |

## 4. Libros y quién responde

Reglas (vol. 1, §2.1.5): casi iguales a 2000. En hogares de origen se entrevista o se hace proxy a todos; en *split-off*, a los miembros de 1993, sus cónyuges e hijos. Los entrevistadores intentan entrevistar a toda persona de 11 años o más; por los menores de 11 responde un padre o cuidador. El seguimiento de personas que se mudaron usa las reglas de 2000, con una ampliación para niños nacidos desde 1997 aunque ya no vivan en el hogar.

Resultado por persona en `ptrack` (codebook `PTRACK`):

| Libro | Completo | Parcial | No completado |
|---|---:|---:|---:|
| 3A | 29.045 | 13 | 908 |
| 3B | 29.014 | 16 | 936 |
| Proxy (`bp`) | 1.531 | — | 1 |
| 4 | 10.663 | 1 | 217 |
| 5 | 13.509 | — | 141 |
| EK1 (7-14) | 9.221 | 1.481 | 500 |
| EK2 (15-24) | 9.253 | 1.830 | 742 |

`res07us` (libro US) marca 59.140 «completos», más que los miembros del hogar; para saber quién fue medido es más directo `msrd07` (42.510 sí, 11.873 no) o los propios archivos `bus*`.

## 5. Catálogo de archivos

«Llave única» es la combinación de variables que identifica cada fila, **comprobada en los archivos**; «no determinada» significa que ninguna combinación estándar resultó única. Las descripciones de cada archivo están en las listas de módulos de los codebooks.

**Hogar (`Household Data/`)**

| Archivo | Llave única (verificada) | N | Variables |
|---|---|---:|---:|
| `b1_cov` | `hhid07` | 13.056 | 43 |
| `b1_cr1` | `hhid07` + `crtype` | 77.856 | 25 |
| `b1_cr2` | `hhid07` | 12.976 | 9 |
| `b1_ks0` | `hhid07` | 12.977 | 24 |
| `b1_ks1` | `hhid07` + `ks1type` | 480.149 | 8 |
| `b1_ks2` | `hhid07` + `ks2type` | 155.724 | 6 |
| `b1_ks3` | `hhid07` + `ks3type` | 90.839 | 8 |
| `b1_ks4` | `hhid07` + `ks4type` | 116.793 | 14 |
| `b1_ksr1` | `hhid07` + `ksr3type` | 25.951 | 16 |
| `b1_ksr2` | `hhid07` + `ksr4type` | 25.953 | 27 |
| `b1_ksr3` | `hhid07` + `ksr2type` | 38.928 | 18 |
| `b1_ksr4` | `hhid07` + `ksr5type` | 25.952 | 11 |
| `b1_pp` | `hhid07` + `pptype` | 155.712 | 16 |
| `b2_bh` | `hhid07` | 12.987 | 36 |
| `b2_cov` | `hhid07` | 13.056 | 43 |
| `b2_hi` | `hhid07` + `hitype` | 51.948 | 6 |
| `b2_hr1` | `hhid07` + `hrtype` | 168.831 | 19 |
| `b2_hr2` | `hhid07` + `hr2type` | 77.922 | 8 |
| `b2_kr` | `hhid07` | 12.987 | 43 |
| `b2_nd1` | `hhid07` | 12.987 | 6 |
| `b2_nd2` | `hhid07` + `ndtype` | 821 | 32 |
| `b2_nt1` | `hhid07` | 12.987 | 6 |
| `b2_nt2` | no determinada | 6.197 | 82 |
| `b2_ut1` | `hhid07` | 12.987 | 56 |
| `b2_ut2` | `hhid07` + `ut2type` | 3.859 | 36 |
| `b2_ut3` | `hhid07` + `ut3type` | 3.005 | 10 |
| `b2_ut4` | `hhid07` + `uttype` | 58.740 | 15 |
| `b2_vu` | `hhid07` + `vutype` | 90.909 | 25 |
| `b3a_br1` | `pidlink` | 22.193 | 23 |
| `b3a_cov` | `pidlink` | 29.967 | 51 |
| `b3a_dl1` | `pidlink` | 29.059 | 55 |
| `b3a_dl2` | no determinada | 29.774 | 25 |
| `b3a_dl3` | no determinada | 24.788 | 47 |
| `b3a_dl4` | `pidlink` + `dl4type` | 50.792 | 48 |
| `b3a_dl5` | `pidlink` | 3.054 | 47 |
| `b3a_hi` | `pidlink` + `hitype` | 116.236 | 8 |
| `b3a_hr0` | `pidlink` | 29.059 | 8 |
| `b3a_hr1` | `pidlink` + `hr1type` | 136.201 | 22 |
| `b3a_hr2` | `pidlink` + `hr2type` | 62.862 | 10 |
| `b3a_kw1` | `pidlink` | 29.059 | 65 |
| `b3a_kw3` | `pidlink` + `kwn` | 12.903 | 22 |
| `b3a_mg1` | `pidlink` | 29.057 | 98 |
| `b3a_mg2` | `pidlink` + `movenum` | 17.215 | 42 |
| `b3a_pk1` | `pidlink` | 22.193 | 15 |
| `b3a_pk2` | `pidlink` + `pk2type` | 344.736 | 7 |
| `b3a_pk3` | `pidlink` + `pk3type` | 76.731 | 11 |
| `b3a_re` | `pidlink` | 24.255 | 59 |
| `b3a_si` | `pidlink` | 29.054 | 25 |
| `b3a_sw` | `pidlink` | 29.059 | 19 |
| `b3a_tk1` | `pidlink` | 29.055 | 43 |
| `b3a_tk2` | `pidlink` | 29.055 | 142 |
| `b3a_tk3` | no determinada | 209.205 | 18 |
| `b3a_tk4` | `pidlink` | 24.255 | 55 |
| `b3a_tr` | `pidlink` | 29.054 | 39 |
| `b3b_ak1` | `pidlink` + `aktype` | 73.861 | 12 |
| `b3b_ak2` | `hhid07` + `pid07` + `ak2type` | 40.699 | 11 |
| `b3b_ba0` | `pidlink` | 29.027 | 54 |
| `b3b_ba1` | `pidlink` | 14.992 | 63 |
| `b3b_ba4` | `pidlink` | 29.027 | 32 |
| `b3b_ba5` | `pidlink` | 29.027 | 11 |
| `b3b_ba6` | no determinada | 11.020 | 56 |
| `b3b_cd1` | `pidlink` | 29.030 | 6 |
| `b3b_cd2` | no determinada | 261.270 | 8 |
| `b3b_cd3` | `pidlink` + `cdtype` | 129.804 | 15 |
| `b3b_co1` | `pidlink` | 29.029 | 28 |
| `b3b_co2` | `pidlink` | 28.391 | 23 |
| `b3b_co3` | `pidlink` | 28.394 | 19 |
| `b3b_cov` | `pidlink` | 29.967 | 54 |
| `b3b_ep1` | `pidlink` | 29.026 | 7 |
| `b3b_ep2` | no determinada | 15.132 | 22 |
| `b3b_fm` | `pidlink` + `fmtype` | 290.280 | 14 |
| `b3b_kk1` | `pidlink` | 29.032 | 14 |
| `b3b_kk2` | `pidlink` + `kktype` | 116.128 | 10 |
| `b3b_kk3` | `pidlink` + `kk3type` | 194.778 | 7 |
| `b3b_kk4` | `pidlink` | 29.032 | 21 |
| `b3b_km` | `pidlink` | 29.032 | 32 |
| `b3b_kp` | `pidlink` + `kptype` | 290.290 | 8 |
| `b3b_ma1` | `pidlink` | 29.029 | 22 |
| `b3b_ma2` | no determinada | 609.609 | 7 |
| `b3b_ma3` | `pidlink` + `ma2type` | 261.261 | 15 |
| `b3b_pm1` | `pidlink` | 29.028 | 40 |
| `b3b_pm2` | no determinada | 9.189 | 20 |
| `b3b_pm3` | `pidlink` + `pm3type` | 406.392 | 15 |
| `b3b_ps` | `pidlink` + `pstype` | 145.145 | 9 |
| `b3b_rj0` | `pidlink` | 29.029 | 32 |
| `b3b_rj1` | `pidlink` + `rjtype` | 30.548 | 10 |
| `b3b_rj3` | `pidlink` | 29.029 | 65 |
| `b3b_rn1` | `pidlink` | 29.028 | 29 |
| `b3b_rn2` | `pidlink` + `rn1type` | 4.930 | 9 |
| `b3b_tf` | `pidlink` + `tftype` | 116.104 | 36 |
| `b3b_vg` | `pidlink` | 29.031 | 30 |
| `b4_ba6` | no determinada | 21.377 | 56 |
| `b4_bf` | `pidlink` | 10.665 | 19 |
| `b4_br` | `pidlink` | 10.666 | 24 |
| `b4_bx6` | `pidlink` + `bx63a` | 1.568 | 14 |
| `b4_ch0` | `pidlink` | 10.663 | 22 |
| `b4_ch1` | no determinada | 11.228 | 128 |
| `b4_cov` | `pidlink` | 10.884 | 49 |
| `b4_cx1` | `pidlink` + `cxtype` | 93.230 | 11 |
| `b4_cx2` | `pidlink` | 10.660 | 53 |
| `b4_ep1` | `pidlink` | 10.660 | 7 |
| `b4_ep2` | no determinada | 18.634 | 23 |
| `b4_kw2` | `pidlink` + `kwn` | 11.167 | 66 |
| `b4_kw3` | `pidlink` | 10.666 | 19 |
| `b5_baa` | `pidlink` + `baatype` | 27.022 | 15 |
| `b5_cov` | `pidlink` | 13.652 | 50 |
| `b5_dla1` | `pidlink` | 13.511 | 21 |
| `b5_dla2` | `pidlink` + `dlatype` | 8.627 | 106 |
| `b5_dla3` | `pidlink` | 13.511 | 61 |
| `b5_dla6` | `pidlink` + `dla2type` | 33.672 | 18 |
| `b5_fma` | `pidlink` + `fmatype` | 129.503 | 14 |
| `b5_maa1` | `pidlink` | 13.511 | 15 |
| `b5_maa2` | no determinada | 270.220 | 7 |
| `b5_psa` | `pidlink` + `psatype` | 67.555 | 9 |
| `b5_rja0` | `pidlink` | 13.511 | 25 |
| `b5_rja1` | `hhid07` + `pid07` + `rja1type` | 20.784 | 9 |
| `b5_rja2` | `hhid07` + `pid07` | 13.511 | 42 |
| `b5_rja3` | `pidlink` | 13.511 | 57 |
| `b5_rna1` | `pidlink` + `rna1type` | 15.206 | 11 |
| `b5_rna2` | `pidlink` | 13.511 | 28 |
| `bek_ek1` | `pidlink` | 11.202 | 64 |
| `bek_ek2` | `pidlink` | 11.824 | 64 |
| `bk_ar0` | `hhid07` | 13.536 | 9 |
| `bk_ar1` | `hhid07` + `pid07` | 73.016 | 53 |
| `bk_cov` | `hhid07` | 13.536 | 45 |
| `bk_krk` | `hhid07` | 13.535 | 18 |
| `bk_sc` | `hhid07` | 13.536 | 17 |
| `bp_ak1` | `pidlink` + `aktype` | 3.446 | 13 |
| `bp_ak2` | `pidlink` + `ak2type` | 455 | 10 |
| `bp_ba0` | `pidlink` | 1.532 | 75 |
| `bp_ba1` | `pidlink` + `ba2type` + `bap3type` | 1.056 | 28 |
| `bp_ba5` | `pidlink` | 1.532 | 32 |
| `bp_ba6` | no determinada | 1.756 | 55 |
| `bp_br` | `pidlink` | 1.532 | 22 |
| `bp_cd1` | `pidlink` | 1.532 | 6 |
| `bp_cd2` | `pidlink` + `cd01type` | 13.788 | 8 |
| `bp_cd3` | `pidlink` + `cdtype` | 10.548 | 15 |
| `bp_ch0` | `pidlink` | 671 | 7 |
| `bp_ch1` | `pidlink` + `ch05` | 74 | 25 |
| `bp_cov` | `pidlink` | 1.533 | 54 |
| `bp_cx` | `pidlink` | 671 | 7 |
| `bp_dl1` | `pidlink` | 1.532 | 38 |
| `bp_dl3` | no determinada | 681 | 43 |
| `bp_dl4` | `pidlink` + `dl4type` | 1.562 | 50 |
| `bp_dl5` | `pidlink` | 50 | 65 |
| `bp_kk1` | `pidlink` | 1.532 | 26 |
| `bp_kk2` | `pidlink` + `kktype` | 15.822 | 7 |
| `bp_km` | `pidlink` | 1.532 | 22 |
| `bp_kw` | `pidlink` | 1.532 | 36 |
| `bp_ma1` | no determinada | 32.172 | 7 |
| `bp_ma2` | `pidlink` + `ma2type` | 13.788 | 15 |
| `bp_ma3` | `pidlink` | 1.532 | 16 |
| `bp_mg` | `pidlink` | 1.532 | 72 |
| `bp_pm` | `pidlink` | 1.532 | 12 |
| `bp_rj` | `pidlink` + `rjtype` | 3.676 | 9 |
| `bp_rn` | `pidlink` + `rntype` | 1.876 | 9 |
| `bp_tf` | `pidlink` + `tftype` | 3.062 | 33 |
| `bp_tk1` | `pidlink` | 1.532 | 83 |
| `bp_tk2` | `pidlink` | 1.208 | 64 |
| `bt_cov` | `hhid07` | 13.537 | 37 |
| `bus1_0` | `hhid07` | 13.056 | 38 |
| `bus1_1` | `hhid07` + `pid07` | 68.484 | 23 |
| `bus1_2` | `hhid07` + `pid07` | 68.484 | 23 |
| `bus1_3` | `hhid07` + `pid07` | 68.484 | 31 |
| `bus1_4` | `hhid07` + `pid07` | 68.484 | 10 |
| `bus2_0` | `hhid07` | 13.055 | 40 |
| `bus2_1` | `hhid07` + `pid07` | 68.459 | 19 |
| `bus2_2` | `hhid07` + `pid07` | 68.454 | 16 |
| `bus2_3` | `hhid07` + `pid07` | 68.454 | 21 |
| `htrack` | no determinada | 15.146 | 86 |
| `ptrack` | `pidlink` | 66.784 | 101 |

**Comunidad y establecimientos (`Community Data/`)**

| Archivo | Llave única (verificada) | N | Variables |
|---|---|---:|---:|
| `adt` | no determinada | 340 | 190 |
| `adt_ap1` | no determinada | 660 | 8 |
| `adt_dg1` | no determinada | 660 | 14 |
| `bk1` | `commid07` + `bk1type` | 322 | 351 |
| `bk1_a` | `commid07` + `atype` | 2.504 | 9 |
| `bk1_b` | `commid07` + `btype` | 1.872 | 11 |
| `bk1_d1` | `commid07` + `d1type` | 564 | 6 |
| `bk1_d1a` | `commid07` + `d8atype` | 426 | 6 |
| `bk1_d2` | `commid07` + `d2type` | 980 | 10 |
| `bk1_d3` | `commid07` + `d3type` | 605 | 10 |
| `bk1_d4` | no determinada | 563 | 16 |
| `bk1_e1` | no determinada | 68 | 13 |
| `bk1_e2` | no determinada | 512 | 7 |
| `bk1_f1` | `commid07` + `f1type` | 2.504 | 9 |
| `bk1_f2` | no determinada | 2.052 | 8 |
| `bk1_g` | `commid07` + `gtype` | 2.191 | 7 |
| `bk1_i` | `commid07` + `itype` | 939 | 5 |
| `bk1_ir` | `commid07` + `irtype` | 1.235 | 14 |
| `bk1_j` | `commid07` + `jtype` | 1.878 | 5 |
| `bk1_pap0` | `commid07` | 313 | 90 |
| `bk1_pap1` | `commid07` + `pap1type` | 2.808 | 20 |
| `bk1_pap2` | no determinada | 66 | 6 |
| `bk1_pap3` | no determinada | 936 | 6 |
| `bk1_pap4` | no determinada | 936 | 6 |
| `bk1_pmkd` | `commid07` + `pmkdtype` | 5.634 | 9 |
| `bk1_tr` | `commid07` + `trtype` | 1.878 | 7 |
| `bk2` | no determinada | 322 | 168 |
| `bk2_ka3` | no determinada | 622 | 9 |
| `bk2_ka4` | no determinada | 967 | 8 |
| `bk2_lu1` | `commid07` + `s38type` | 3.139 | 4 |
| `bk2_pl` | `commid07` + `ka1type` | 1.261 | 8 |
| `bk2_pr2` | no determinada | 392 | 5 |
| `bk2_st` | `commid07` + `s1type` | 3.452 | 4 |
| `hin` | no determinada | 322 | 59 |
| `hin_h` | no determinada | 13.202 | 8 |
| `hps` | no determinada | 328 | 34 |
| `hps_h` | no determinada | 12.480 | 8 |
| `hps_hour` | `commid07` | 311 | 30 |
| `htw` | no determinada | 645 | 38 |
| `htw_h` | no determinada | 16.075 | 8 |
| `htw_hour` | `commid07` | 313 | 30 |
| `inf` | no determinada | 644 | 139 |
| `inf_pap0` | no determinada | 628 | 67 |
| `inf_pap1` | no determinada | 5.652 | 22 |
| `inf_pap2` | no determinada | 128 | 7 |
| `inf_pap5` | no determinada | 3.768 | 7 |
| `inf_tr1` | no determinada | 3.768 | 10 |
| `mkd_cov` | no determinada | 3.122 | 50 |
| `mkd_km1` | no determinada | 3.067 | 109 |
| `mkd_km2` | no determinada | 30.670 | 5 |
| `mkd_km3` | no determinada | 18.402 | 6 |
| `mkd_km4` | no determinada | 24.536 | 8 |
| `mkd_km5` | no determinada | 18.402 | 9 |
| `pkk` | no determinada | 322 | 133 |
| `pkk_i` | `commid07` + `itype` | 948 | 6 |
| `pkk_j` | `commid07` + `j26type` | 1.887 | 6 |
| `pkk_j1` | `commid07` + `year` + `fascode` | 2.310 | 7 |
| `pkk_kr` | `commid07` + `krtype` | 432 | 10 |
| `pkk_ksr` | `commid07` + `ksr2type` | 946 | 13 |
| `pkk_pap2` | no determinada | 364 | 6 |
| `pkk_pm` | `commid07` + `pmtype` | 5.627 | 10 |
| `pls` | `fcode07` | 307 | 121 |
| `pls_b1` | `commid07` + `b1type` + `fascode` | 4.605 | 6 |
| `pls_d1` | `fcode07` + `dtype` | 3.070 | 7 |
| `pls_sdp1` | no determinada | 811 | 10 |
| `pos` | `fcode07` | 636 | 152 |
| `pos_b1` | `commid07` + `b1type` + `fascode` | 6.360 | 15 |
| `pos_b2` | `commid07` + `b2type` + `fascode` | 3.180 | 10 |
| `pos_c0` | no determinada | 3.512 | 18 |
| `pos_c2` | no determinada | 3.816 | 8 |
| `pos_d1` | no determinada | 11.448 | 10 |
| `pos_prp1` | `commid07` + `prptype` + `fascode` | 1.064 | 8 |
| `pos_sdp1` | no determinada | 1.776 | 10 |
| `pra` | `commid07` + `fcode07` | 1.595 | 474 |
| `pra_a1` | `commid07` + `atype` + `fascode` | 17.545 | 7 |
| `pra_b1` | `commid07` + `b1type` + `fascode` | 11.165 | 13 |
| `pra_b2` | `commid07` + `b2type` + `fascode` | 78.114 | 12 |
| `pra_b3` | `commid07` + `b3type` + `fascode` | 4.782 | 23 |
| `pra_b4` | `commid07` + `b4type` + `fascode` | 19.128 | 10 |
| `pra_b5` | `commid07` + `b5type` + `fascode` | 3.708 | 7 |
| `pra_b6` | no determinada | 11.074 | 7 |
| `pra_c1` | `commid07` + `c1type` + `fascode` | 47.820 | 8 |
| `pra_c2` | `commid07` + `c2type` + `fascode` | 30.286 | 7 |
| `pra_ph1` | `commid07` + `phtype` + `fascode` | 4.879 | 12 |
| `pusk` | `fcode07` | 952 | 673 |
| `pusk_a1` | `commid07` + `atype` + `fascode` | 10.472 | 7 |
| `pusk_b1` | `commid07` + `btype` + `fascode` | 1.904 | 22 |
| `pusk_c0` | no determinada | 5.712 | 9 |
| `pusk_c1` | `commid07` + `c1type` + `fascode` | 84.728 | 12 |
| `pusk_c2` | `commid07` + `c2type` + `fascode` | 2.856 | 20 |
| `pusk_c3` | `commid07` + `c3type` + `fascode` | 12.376 | 11 |
| `pusk_c4` | `commid07` + `c4type` + `fascode` | 5.706 | 11 |
| `pusk_d1` | `commid07` + `d1type` + `fascode` | 13.328 | 7 |
| `pusk_d2` | `commid07` + `d2type` + `fascode` | 4.249 | 7 |
| `pusk_d3` | no determinada | 12.257 | 18 |
| `pusk_dm1` | `commid07` + `dm1type` + `fascode` | 7.616 | 9 |
| `pusk_dm2` | `commid07` + `dm2type` + `fascode` | 7.616 | 7 |
| `pusk_e1` | `commid07` + `e1type` + `fascode` | 26.656 | 8 |
| `pusk_e2` | `commid07` + `e2type` + `fascode` | 15.232 | 7 |
| `pusk_g1` | `commid07` + `g1type` + `fascode` | 5.562 | 8 |
| `puskakm1` | `commid07` + `akmtype` + `fascode` | 6.447 | 7 |
| `sar` | no determinada | 39.348 | 38 |
| `sar_cov` | no determinada | 322 | 37 |
| `schl` | `fcode07` + `b2type` | 2.621 | 403 |
| `schl_a1` | `commid07` + `a1type` + `fascode` | 7.680 | 13 |
| `schl_a2` | `fcode07` + `a2type` | 558 | 6 |
| `schl_b3` | `commid07` + `b3type` + `fascode` | 43.520 | 6 |
| `schl_b5` | `fcode07` + `b5type` | 10.240 | 13 |
| `schl_b6` | `fcode07` + `b10type` | 38.400 | 6 |
| `schl_c1` | `commid07` + `c1type` + `fascode` | 7.680 | 13 |
| `schl_d1` | `commid07` + `d1type` + `fascode` | 5.790 | 8 |
| `schl_d2` | `commid07` + `d2type` + `fascode` | 4.785 | 8 |
| `schl_e` | `commid07` + `etype` + `fascode` | 53.760 | 7 |
| `schl_f` | no determinada | 63.775 | 15 |
| `schl_g1` | no determinada | 5.790 | 8 |
| `schl_g2` | no determinada | 4.785 | 8 |
| `schl_g3` | `commid07` + `g3type` + `fascode` | 15.360 | 10 |
| `schl_kr` | `commid07` + `krtype` + `fascode` | 10.921 | 18 |
| `tra` | `commid07` + `b1type` + `fascode` | 4.373 | 230 |

## 6. Cómo manejar los datos

### 6.1 Identificadores

| Variable | Qué es | Notas (verificadas) |
|---|---|---|
| `hhid07` (texto, 7) | EA + hogar + origen/*split-off* | Sexto dígito: `0` origen, `1` *split-off* de 1997, `2` de 1998, `3` de 2000, `4` nuevo en 2007. Vacío en `htrack` para 1.328 hogares no entrevistados |
| `hhid07_9` | Versión de 9 caracteres | En `htrack` y en algunos archivos (`bus*`, `b2_vu`, `b3b_kk4`) |
| `pid07` | Línea en el roster de 2007 | |
| `pidlink` | Persona, constante entre olas | Único en `ptrack` y en `bek_ek1`/`bek_ek2`. Repetido en `bus1_*` (9.161), porque el roster acumula a quienes se fueron o murieron |
| `commid07` | Comunidad | En los 13.536 hogares con libro K: 8.497 con código numérico y **5.039 con letras** (fuera de las comunidades IFLS). 17 hogares tienen códigos numéricos que no son de las 312 comunidades (`1227`, `5115`) |
| `mkid07` | Llave del mini-CFS (`mkd_*`) | De los hogares con `commid07` con letras (`result07` = 1), 3.152 de 4.967 tienen un `mkid07` que está en `mkd_cov`; 278 lo tienen vacío |
| `fcode07` | Establecimiento | Igual lógica que en 2000 |

**Archivos comunitarios con 322 filas para 313 códigos.** `bk1`, `bk2`, `pkk`, `hin`, `sar_cov` tienen 322 filas: 312 comunidades, más el código `9999`, y 9 comunidades con dos filas (`3109`, `3113`, `3114`, `3134`, `3233`, `3331`, `3403`, `3409`, `3415`). Puede tratarse de las EA gemelas, pero no se verificó. En los archivos de precios, la llave incluye además el código del libro (`hincode`, `hpscode`, `htwcode`).

**Dos indicadores de entrevista que no coinciden.** En `htrack`, `result07` = 1 en 13.270 hogares, pero `res07bk` = 1 en 13.536: 266 hogares tienen el libro K hecho y `result07` distinto de 1 (14 «se unió a otro hogar», 106 «rechazo», 146 «no encontrado»). `bk_cov` tiene 13.536 filas.

**Archivos sin llave única** con las combinaciones estándar: entre los de hogar, la historia educativa (`b3a_dl2`, `dl3`) y laboral (`b3a_tk3`), hijos fuera del hogar (`b3b_ba6`, `b4_ba6`, `bp_ba6`), embarazos (`b4_ch1`), negocios (`b2_nt2`), morbilidad (`b3b_ma2`, `b5_maa2`, `bp_ma1`), episodios (`b3b_ep2`, `b4_ep2`), participación (`b3b_pm2`), `b3b_cd2`, `bp_dl3` y `htrack` (por los `hhid07` vacíos). Entre los comunitarios, los de precios, mini-CFS, informantes y varios de establecimientos. No se buscó la llave correcta de cada uno.

### 6.2 Códigos especiales

Igual que en 2000: variables X, último dígito 5-9 para códigos especiales (en texto V-Z), sí/no = 1/3, sexo = 1/3, años con 4 dígitos. Algunos precios usan 99998/99999. `ptrack$age_07` viene como número (en 2000 y 1997 venía como texto).

### 6.3 Proxy y formato largo

El libro proxy se llama ahora `bp_*` (1.532 personas) y no trae la escala CES-D (`bp_kk1` no tiene variables `kp`). Muchos archivos están en formato largo con variables `…type`.

### 6.4 Pesos

| Archivo | Variables | Qué son (codebooks y vol. 2) |
|---|---|---|
| `htrack` | `hwt07la`, `hwt07l_` | Longitudinales de hogar con y sin ajuste por desgaste |
| `htrack` | `hwt07xa`, `hwt07x_` | Transversales de hogar con y sin ajuste por desgaste |
| `htrack` | `hwt9307l` | Longitudinal de hogar para el panel 1993-1997-2000-2007 |
| `htrack` | `hh07ataj`, `hh9307aj` | Sumas de ajustes de desgaste individuales |
| `ptrack` | `pwt07la`, `pw9307l`, `pw9307lr`, `pw9307ul` | Longitudinales de persona (2007; panel 1993-2007 de entrevista, de roster y de medición) |
| `ptrack` | `pwt07xa`, `pwt07x_`, `pw07usxa`, `pw07usx` | Transversales de persona y de evaluación de salud |
| `ptrack` | `mrsp9307`, `msrd9307` | Indicadores de entrevistado y medido en las cuatro olas |

`htrack` y `ptrack` de 2007 traen también los pesos de 1993, 1997 (incluidos `pwt97usl`, `pwt97usx`, `pwt97ekx`) y 2000.

## 7. Seguimiento

**Hogares** (`htrack$result07`): 13.270 con resultado 1, 301 unidos a otro hogar, 167 todos muertos, 300 rechazos, 973 no encontrados y 135 sin dato. Ver §6.1 sobre `res07bk`.

- De los 7.224 hogares de 1993: 6.234 con `result07` = 1, 489 no encontrados, 227 rechazos, 143 todos muertos, 35 unidos a otro hogar y 96 sin dato.
- `mover07` (desde la última entrevista): 7.703 no se movieron; 788 dentro de la desa; 1.936 dentro del kecamatan; 978 dentro del kabupaten; 1.164 dentro de la provincia; 732 a otra provincia IFLS; **174 con código 6 y 1.671 con 98**, códigos que no describe la documentación.

**Personas del roster de 1993** (33.081; `ptrack$ar01a_07`): 18.868 siguen en el mismo hogar (1), 4.958 «regresaron» (2, *ART comeback*), 5.086 ya no están (3), 4.093 murieron (0) y 76 con otros códigos; 23.902 son miembros de un hogar en 2007. La guía de usuario reporta 16.559 en su hogar original, 7.340 en otro y 3.116 muertos (vol. 1, §2.1.5); las cifras no coinciden exactamente con `ptrack`.

**Niños de 0 a 5 años en 1997** (`ptrack`): 3.851, de 9 a 19 años en 2007 (mediana 13). 3.451 son miembros de un hogar en 2007; 3.284 tienen talla medida; 3.361 tienen prueba EK1 y 727 EK2; 2.643 respondieron el libro 5 y 700 el 3A.

## 8. Fechas de entrevista

| Año-mes | 2007-11 | 2007-12 | 2008-01 | 2008-02 | 2008-03 | 2008-04 | 2008-05 | 2008-06 | 2008-07 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| En comunidades IFLS | 260 | 1.240 | 1.965 | 1.726 | 1.584 | 1.030 | 509 | 174 | 9 |
| Fuera de comunidades IFLS | 49 | 425 | 659 | 572 | 684 | 961 | 1.220 | 384 | 84 |

- **Encuestas de precios** (`hin`, `hps`, `htw`): todas en **2008, de febrero a junio**.
- **Pruebas cognitivas:** EK1 1.658 en 2007 y 9.543 en 2008; EK2 1.800 y 10.024.
- **Medición de salud** (`bus1_3$us17year`): 6.387 en 2007 y 36.031 en 2008, más 57 casos con años de 2000 a 2006 (52) o 2009 (5) y 2 con 9999.

## 9. Contenido por tema

### 9.1 Antropometría y salud física (`bus1_*`, `bus2_*`)

- **Siete archivos por persona**, todos con 68.484 filas en US-1 (`bus1_1`-`bus1_4`) y 68.459/68.454 en US-2 (`bus2_1`-`bus2_3`):
  - `bus1_1`: fecha de nacimiento, edad, peso (`us06`), presión (dos medidas);
  - `bus1_2`: **talla** (`us04`), tipo de medición (`us05`), altura sentado (40+), tercera presión, prueba de sentarse y pararse, cintura y cadera;
  - `bus1_3`: **fuerza de agarre**, fecha de medición;
  - `bus1_4`: medicamentos;
  - `bus2_1`: capacidad pulmonar; `bus2_2`: hemoglobina, **colesterol total y HDL (40+)**; `bus2_3`: embarazo, ayuno, discapacidad, fecha.
- Las filas incluyen a todo el roster acumulado (`usar01a`: 26.810 siguen, 14.933 nuevos, 6.187 «regresaron», 16.821 ya no viven ahí, 3.657 muertos, 76 otro).
- **Talla válida** (`us04x` = 1): 42.310; peso válido: 42.337. De pie 40.508 / acostado 1.795. Rango de talla: 10,7 a 197,4 cm (el mínimo es un error evidente).
- Fecha de nacimiento (`us02yr`): 384 con 9998 y 5 con 9999. Otras fuentes de edad: `bk_ar1` y `ptrack` (`age_07`, `bth_year`, `bth_mnth`, `bth_day`).

### 9.2 Salud mental (`b3b_kp`)

- **Escala CES-D de 10 ítems**, semana anterior. Formato largo: una fila por persona e ítem (`kptype` A-J; 29.029 personas × 10). Dos preguntas: `kp01` (¿se sintió así? 1 sí / 3 no) y, si sí, `kp02` (frecuencia: 1 ≤ 1 día, 2 = 1-2 días, 3 = 3-4 días, 4 = 5-7 días).
- **Trampa: las etiquetas de `kptype` en el codebook no coinciden con el cuestionario.** El codebook dice, por ejemplo, B = «no tenía apetito», D = «me sentí tan bueno como los demás» y H = «sentí miedo»; el cuestionario (`HH BOOK 3B FINAL.pdf`, sección KP) dice B = «problemas para concentrarme», D = «todo lo que hacía era un esfuerzo» y H = «estuve feliz». Los datos siguen al cuestionario: los ítems con más respuestas «sí» frecuentes son E y H, que en el cuestionario son los dos ítems positivos («esperanza en el futuro» y «feliz»).

| `kptype` | Ítem según el cuestionario | No | ≤ 1 día | 1-2 días | 3-4 días | 5-7 días |
|---|---|---:|---:|---:|---:|---:|
| A | Me molestaron cosas que usualmente no me molestan | 25.299 | 946 | 860 | 1.174 | 747 |
| B | Tuve problemas para concentrarme | 23.580 | 1.347 | 1.281 | 1.925 | 892 |
| C | Me sentí deprimido | 24.895 | 1.121 | 1.019 | 1.224 | 767 |
| D | Sentí que todo lo que hacía era un esfuerzo | 18.855 | 1.532 | 2.053 | 3.644 | 2.941 |
| E | Me sentí con esperanza en el futuro (positivo) | 3.158 | 1.708 | 2.790 | 8.841 | 12.526 |
| F | Sentí miedo | 24.482 | 1.292 | 936 | 1.503 | 812 |
| G | Dormí mal | 20.962 | 1.575 | 1.648 | 2.643 | 2.196 |
| H | Estuve feliz (positivo) | 2.530 | 1.534 | 2.480 | 9.198 | 13.282 |
| I | Me sentí solo | 27.193 | 467 | 348 | 635 | 382 |
| J | No podía ponerme en marcha | 26.732 | 545 | 471 | 891 | 385 |

  Faltantes: 3 a 6 por ítem.
- **No es comparable directamente con 1993 ni con 2000**: cambian los ítems, el periodo de referencia (semana anterior frente a 4 semanas) y la escala de respuesta. Hay ítems de contenido parecido (deprimido/triste, miedo/ansiedad, dormir mal/insomnio), pero con otra redacción y otra escala.
- El libro proxy no trae la escala.

### 9.3 Educación

- **Adultos (`b3a_dl1`, 29.059):** nivel más alto (`dl06`) y grado para todos los que asistieron; historia en `b3a_dl2`-`dl5`.
- **Niños (`b5_dla1`, 13.511):** 7.058 asistieron alguna vez. Historia escolar en `b5_dla2`, `dla3`, `dla6`.
- **Roster (`bk_ar1`):** nivel y grado para todos.

### 9.4 Pruebas cognitivas (`bek_ek1`, `bek_ek2`)

- **Mismo diseño que en 2000** (el codebook repite el texto de IFLS3): ítems cognitivos comunes más ítems de matemáticas por versión; respuesta correcta `ekNx` = 1, incorrecta 3, faltante 9; sin puntaje total.
- **Dos archivos**: `bek_ek1` (versión 7-14; 11.202 personas) y `bek_ek2` (versión 15-24; 11.824). Una fila por persona en cada uno.

| Archivo | Ítems con respuesta | Resultado (`result`: completo / parcial / no) | Edad (mín.-mediana-máx.) |
|---|---|---|---|
| `bek_ek1` | `ek1`-`ek12` (12) y `ek13`-`ek17` (5) | 9.221 / 1.481 / 500 | 7-13-27 |
| `bek_ek2` | `ek1`-`ek6`, `ek11`, `ek12` (8) y `ek18`-`ek22` (5) | 9.252 / 1.830 / 742 | 9-23-35 |

- **Diferencia con 2000:** no hay ítem `ek0`. En 2007 los conteos de ítems coinciden con el codebook (12 + 5 y 8 + 5); en 2000 había un ítem `ek0` adicional en ambas versiones.
- Con los ítems comunes (`ek1`-`ek6`, `ek11`, `ek12`) y los mismos números de pregunta que en 2000, hay base para comparar ítem por ítem entre 2000 y 2007; no se verificó en los cuestionarios que sean idénticos.

### 9.5 Arroz: consumo, precio pagado y Raskin

- `b1_ks1`: consumo semanal por tipo de alimento (compras y producción propia, en rupias).
- `b1_ks4` (arroz, `ks4type` = A): 9.554 hogares compraron el último mes; unidad kg 7.827, litro 1.546, otras 187. Precio implícito (`ks15`/`ks13`, solo kg, sin limpiar): mediana **Rp 5.000/kg**; p1 1.200; p99 10.576; atípicos de 4 a 520.000.
- **Raskin** (`b1_ksr2`, `ksr4type` A = Raskin, B = operación de mercado): 5.662 hogares compraron arroz Raskin en el último año y 114 en operación de mercado; incluye cantidades, precio pagado, precio de mercado, calidad y si rechazaron comprar. `b1_ksr1`, `b1_ksr3`, `b1_ksr4`: otros programas (en esta ronda no se revisaron uno por uno).

### 9.6 Agricultura y choques

- **No hay módulo general de choques del hogar** (muerte, enfermedad, desempleo…) como `b2_ge` en 1997 y 2000. El codebook del libro 2 menciona «choques económicos» en su introducción, pero ni su lista de módulos ni los datos tienen un archivo así.
- Lo que hay:
  - `b2_ut3`: pérdida de cosecha en los últimos 12 meses para hogares agrícolas, por causa (sequía, inundación, plagas, enfermedad, otra): 3.005 filas = 601 hogares × 5 causas; `ut09r` = 1 en 621 filas.
  - `b2_nd1`/`b2_nd2`: desastres en el área en los últimos 5 años y si el hogar fue gravemente afectado.
  - `b1_cr1`/`b1_cr2`: victimización por delitos en los últimos 12 meses.
- `b2_ut1`/`b2_ut2`/`b2_ut4`: tierra, ingreso y activos agrícolas; `b2_vu`: animales y pérdidas por enfermedad.

### 9.7 Otros módulos nuevos

Preferencias de riesgo con elecciones de dinero (`b3a_si`), retiro (`b3a_re`), confianza (`b3a_tr`), condiciones crónicas y discapacidad (`b3b_cd*`), pruebas cognitivas de adultos (fecha, memoria; `b3b_co*`), viñetas de salud (`b3b_vg`), alimentación de niños (`b3b_fm`, `b5_fma`), módulo EP (`b3b_ep*`, `b4_ep*`; no revisado), acceso a crédito (`b2_bh`), seguro de salud (`b3b_ak*`). Descripciones a partir de las etiquetas de variables; no se revisaron en detalle.

## 10. Datos comunitarios de 2007-2008

**Precios del arroz: tres libros de precios nuevos** (todos levantados de febrero a junio de 2008):

| Libro | Archivo | Calidades | Cobertura | Unidad (filas de arroz) | Rp/kg, mediana (p1-p99) |
|---|---|---|---|---|---|
| Informante (`HIN`) | `hin_h` | alta, media, baja | 313 códigos de comunidad | kg 664, litro 202, otra 38, faltante 62 | alta 6.000 (4.500-8.910); media 5.000 (3.526-7.000); baja 4.500 (2.150-6.000) |
| Mercado (`HPS`) | `hps_h` | alta, media, baja | 311 | kg 674, litro 203, otra 20, faltante 63 | alta 5.500 (4.228-10.860); media 5.000 (3.920-8.000); baja 4.400 (3.074-7.000) |
| *Warung* / tienda (`HTW`) | `htw_h` | solo media | 313; casi siempre 2 puntos de venta por comunidad | kg 333, litro 110, otra 21, faltante 179 | media 5.000 (4.000-6.500) |

- Valores sin limpiar, solo respuestas en kg; hay atípicos (máximo 45.000 en mercado, calidad alta).
- `h03a` (¿se vende?) tiene muchos códigos 5 («otros») y 8 («no se vende»); los códigos 1-4 no tienen etiqueta en el codebook de `HTW`.
- **Ya no hay precios en `pos_h` ni en `bk2_hpj`** (no existen en 2007), y el libro PKK no tiene precios. El informante de `HIN` puede ser de la PKK (`hin` registra el tipo y cargo del informante), pero no es el mismo instrumento.
- Otros: `bk1*` (jefe de comunidad, incluidos programas y transporte), `bk2*`, `pkk*` (incluido `pkk_ksr`: programas), `inf*` (informante sobre percepción pública), `tra` (práctica tradicional), `pls` (posyandu para adultos mayores), salud (`pusk*`, `pra*`, `pos*`), escuelas (`schl*`), mini-CFS (`mkd_*`, 3.122 áreas), `sar*`, `adt*`.

## 11. Enlace con olas anteriores

- `htrack` de 2007 trae `hhid93`, `hhid97`, `hhid98`, `hhid00`, `commid93`, `commid97`, `commid00` y resultados de cada ola; `commid00` coincide con el `htrack` de 2000 en todos los casos.
- `ptrack` de 2007 trae ids, `member` y edades de todas las olas, y los pesos de todas las olas.
- Para unir personas entre olas se usa `pidlink`.

## 12. Preguntas abiertas (se deciden con todas las olas revisadas)

- **Comunidad de residencia:** 5.039 hogares con `commid07` con letras; unión con el mini-CFS por `mkid07` (§6.1).
- **Qué indicador de entrevista usar:** `result07` o `res07bk` (§6.1).
- **Precio del arroz en 2007-2008:** tres libros nuevos, distintos de las fuentes de 1993-2000 (§10).
- **Salud mental:** CES-D-10 con otra escala y otro periodo que 1993 y 2000; corregir las etiquetas de `kptype` según el cuestionario (§9.2).
- **Pruebas cognitivas:** cómo puntuar; comparación ítem por ítem con 2000 (§9.4).
- **Choques del hogar:** no hay módulo general en 2007 (§9.6).
- **Edad en meses para HAZ:** `bus1_1`, `bk_ar1`, `ptrack` (§9.1).
- **Pesos:** con o sin ajuste por desgaste (§6.4).

## 13. Lo que no está verificado

- La contradicción de fechas en la guía de usuario (2007-2008 frente a 2008-2009); los datos dicen 2007-2008.
- Por qué 266 hogares tienen libro K hecho y `result07` ≠ 1.
- Los códigos 6 y 98 de `mover07`, el código `9999` y las 9 comunidades con dos filas en los archivos comunitarios, y los códigos `1227` y `5115` de `commid07`.
- Si las etiquetas correctas de `kptype` son las del cuestionario para los 10 ítems: se verificó con el cuestionario en inglés y con el patrón de respuestas, no con una nota de RAND.
- Que los ítems `ek1`-`ek22` sean idénticos a los de 2000.
- La diferencia entre las cifras de seguimiento de la guía de usuario y las de `ptrack`.
- Las llaves de los archivos marcados «no determinada» y los valores extremos de talla, edad y precios.
