# IFLS3 (2000) · Catálogo, contenido y manejo de los datos

*Guía de la ronda 3 para el proyecto final de Ciencia de Datos. Escrita el 12-nov-2026 a partir de la documentación de RAND en `01_Datos/01_Crudos/IFLS3/Household Documentation` y `Community Documentation` (sobre todo `IFLS2000_UsersGuide_vol1.pdf` y `vol2.pdf`, y los codebooks `.cbk`), y de una revisión directa de los 139 archivos `.dta` de `Household Data` y los 91 de `Community Data`. Los conteos y las pruebas de llaves salen de los archivos (Python + `pyreadstat`); lo demás, de la documentación citada.*

*La guía es **descriptiva**: documenta qué hay, cómo está codificado y qué problemas tiene. No decide qué variables serán resultado, control o muestra; las opciones quedan en §12 («Preguntas abiertas»).*

## 1. Qué es esta ronda

- **IFLS3.** Tercera ola completa. Recontacta los hogares de 1993, los *split-off* de 1997 y los de IFLS2+ (1998), y agrega nuevos *split-off*.
- **Trabajo de campo.** Según la guía de usuario (vol. 1), el campo principal fue de **junio a noviembre de 2000**; la portada de los codebooks dice «agosto de 2000 a febrero de 2001». En los datos, la primera visita del libro K (`bk_cov$ivwmth1`) va de **junio a diciembre** (288 en junio, 1.508 en julio, 2.375 en agosto, 2.634 en septiembre, 2.127 en octubre, 1.194 en noviembre, 309 en diciembre). `bk_cov` **no trae año**; las fechas de medición del libro US dicen 2000 en todos los casos.
- **Tamaño (archivos):** `htrack` lista 11.112 hogares, de los cuales **10.435 fueron entrevistados** en 2000: 6.758 de origen (1993) y 3.677 *split-off* (751 de 1997, 280 de 1998 y 2.646 nuevos de 2000). `ptrack` lista 51.142 personas; 43.649 son miembros de un hogar en 2000.
- **Panel:** 6.564 hogares tienen entrevista en 1993, 1997 y 2000 (`htrack`). RAND reporta un recontacto del 95,3 % de los hogares de 1993 (vol. 1, §2.1.4).
- **Comunidades:** las mismas 312 (`commid00` numérico). A diferencia de 1997, los hogares que se mudaron fuera de las comunidades IFLS **sí tienen `commid00`**, con letras (ver §6.1 y §7).
- **Contenido nuevo frente a 1997:** vuelven los síntomas de salud mental (8 ítems, §9.2); nuevas pruebas cognitivas (§9.4); precios de arroz pagados por el hogar (`b1_ks4`, §9.5); programas de la red de seguridad social (arroz subsidiado OPK, ayudas; `b1_ksr*`, `pkk_ksr*`, `jps*`); libro de seguimiento (`bt_cov`); y una encuesta comunitaria corta (**mini-CFS**) para hogares que se mudaron fuera de las comunidades IFLS.

## 2. Qué archivos hay

- `Household Data/`: 139 archivos `.dta`, todos en la raíz (sin subcarpetas). `Community Data/`: 91. Todos en formato `.dta` 113 (Stata 8). **No hay `.zip` pendientes.**
- **Comparado con el apéndice A de la guía de usuario (vol. 2):** coinciden todos los archivos salvo nombres: el apéndice llama `MINI_SN1GRD` y `MINI_SN2GRD` a lo que en disco es `mini_sn1` y `mini_sn2`, y no lista `bk1_ls` ni `bus2_1` (este último por una errata: lista `BUS1_1` dos veces). No falta ningún archivo.
- **Conteos distintos del apéndice en 19 archivos**, casi todos comunitarios (p. ej., `pusk_a1`: 103.954 en el apéndice frente a 10.406 en disco; `sar`: 25.408 frente a 24.653). En los de hogar: `htrack` (11.109 frente a 11.112), `ptrack` (51.244 frente a 51.142), `bt_cov` y `b3b_ma1`. El texto de la guía da además otras cifras para `htrack` (11.183) y `ptrack` (51.263). No se investigó más.
- **Etiquetas:** los `.dta` no traen etiqueta de archivo; las descripciones están en el apéndice A y en los `.cbk`.
- **Documentación:** codebooks en texto (`ifls2000_hhd_*.cbk`, `ifls2000_cf_*.cbk`), cuestionarios en PDF (hogar) y `.doc` (comunidad), y las dos pruebas cognitivas (`7-14_EK1.pdf`, `15-24_EK2.pdf`). **Sí hay codebook de los libros US y EK** (a diferencia de 1997).

## 3. Mapa de la documentación

| Archivo | Qué es | Cuándo usarlo |
|---|---|---|
| `IFLS2000_UsersGuide_vol1.pdf` | Diseño, muestra, reglas de recontacto y seguimiento, contenido de los cuestionarios | Sección de datos del informe |
| `IFLS2000_UsersGuide_vol2.pdf` | **Guía de usuario**: ids, `commid00` y `mkid00`, códigos especiales, pesos, `htrack`/`ptrack`, apéndice A (archivos) y C (notas por módulo) | **Leer primero** |
| `ifls2000_hhd_*.cbk` | Codebooks de hogar por libro (incluidos `BUS`, `BEK`, `BT`, `HTRACK`, `PTRACK`) | Códigos y frecuencias |
| `_01_` … `_13_ … .pdf` | Cuestionarios de hogar (libros T, K, 1, 2, 3A, 3B, 4, 5, US-I, US-II, proxy y formularios de seguimiento T1, T2) | Redacción exacta y saltos |
| `7-14_EK1.pdf`, `15-24_EK2.pdf` | Pruebas cognitivas de 2000 | Contenido de los ítems |
| `ifls2000_cf_*.cbk`, `(01)…(13) … (CF).doc` | Codebooks y cuestionarios comunitarios y de establecimientos (incluidos JPS y mini-CFS) | Datos comunitarios |

## 4. Libros y quién responde

Reglas según la guía de usuario (vol. 1, §2.1.4):

- **Hogares de origen:** se entrevista (o se hace proxy) a todos los miembros actuales, hayan estado o no en 1993.
- **Hogares *split-off*:** se entrevista a los miembros de 1993, sus cónyuges y sus hijos biológicos; de los demás solo hay datos de roster.
- **Seguimiento ampliado:** además de los «objetivo» de 1997 (respondientes principales de 1993 y nacidos antes de 1968), se siguió a los nacidos desde 1993 en hogares de origen, a los nacidos después de 1988 que vivían en un hogar de origen en 1993, a los nacidos entre 1968 y 1988 entrevistados en 1997, y a una muestra aleatoria del 20 % de los nacidos entre 1968 y 1988 no entrevistados en 1997.

Resultado por persona en `ptrack` (códigos del codebook `PTRACK`):

| Libro | Completo | Parcial | No completado |
|---|---:|---:|---:|
| 3A (adultos) | 25.473 | 17 | 339 |
| 3B (adultos) | 25.459 | 11 | 359 |
| 3P (proxy) | 1.273 | 3 | 2 |
| 4 (mujeres alguna vez casadas) | 8.267 | 3 | 82 |
| 5 (niños) | 2.480 | 9.206 | 53 |
| US (salud) | 21.798 | — | 26.990 |
| EK (pruebas cognitivas) | 13.340 | — | 798 |

En el libro 5, «parcial» es la categoría con más casos; el codebook no explica si corresponde a respuestas de un adulto por el niño, como en 1997. En US, «no completado» incluye a personas listadas que ya no viven en el hogar; ver §9.1.

## 5. Catálogo de archivos

«Llave única» es la combinación de variables que identifica cada fila, **comprobada en los archivos**; «no determinada» significa que ninguna combinación estándar resultó única. Las descripciones de cada archivo están en el apéndice A de la guía de usuario (vol. 2).

**Hogar (`Household Data/`)**

| Archivo | Llave única (verificada) | N | Variables |
|---|---|---:|---:|
| `b1_cov` | `pidlink` | 10.291 | 41 |
| `b1_ks0` | `hhid00` | 10.259 | 21 |
| `b1_ks1` | `hhid00` + `ks1type` | 379.583 | 8 |
| `b1_ks2` | `hhid00` + `ks2type` | 92.331 | 6 |
| `b1_ks3` | `hhid00` + `ks3type` | 71.813 | 8 |
| `b1_ks4` | `hhid00` + `ks4type` | 71.813 | 14 |
| `b1_ksr1` | `hhid00` | 10.259 | 5 |
| `b1_ksr3` | `hhid00` + `ksr1type` | 1.516 | 14 |
| `b1_ksr4` | `hhid00` + `ksr2type` | 14.244 | 18 |
| `b1_pp` | `hhid00` + `pptype` | 123.108 | 12 |
| `b2_cov` | `pidlink` | 10.292 | 40 |
| `b2_ge` | `hhid00` + `getype` | 82.152 | 14 |
| `b2_hi` | `hhid00` + `hitype` | 51.337 | 6 |
| `b2_hr1` | `hhid00` + `hrtype` | 102.576 | 18 |
| `b2_hr2` | `hhid00` + `hr2type` | 30.807 | 8 |
| `b2_kr` | `hhid00` | 10.269 | 74 |
| `b2_nt1` | `hhid00` | 10.269 | 5 |
| `b2_nt2` | no determinada | 5.461 | 55 |
| `b2_ut1` | `hhid00` | 10.269 | 27 |
| `b2_ut2` | `hhid00` + `uttype` | 43.651 | 13 |
| `b3a_br` | `pidlink` | 21.736 | 25 |
| `b3a_cov` | `pidlink` | 25.829 | 48 |
| `b3a_dl1` | `pidlink` | 25.490 | 34 |
| `b3a_dl2` | `pidlink` + `dl2type` | 23.081 | 19 |
| `b3a_dl3` | `pidlink` + `dl3type` | 23.081 | 72 |
| `b3a_dl4` | `pidlink` | 9.433 | 69 |
| `b3a_hi` | `pidlink` + `hitype` | 127.440 | 9 |
| `b3a_hr0` | `pidlink` | 25.490 | 8 |
| `b3a_hr1` | `pidlink` + `hrtype` | 98.419 | 20 |
| `b3a_hr2` | `pidlink` + `hr2type` | 26.862 | 11 |
| `b3a_kw1` | `pidlink` | 25.490 | 8 |
| `b3a_kw2` | `pidlink` | 10.568 | 54 |
| `b3a_kw3` | `pidlink` + `kwn` | 11.282 | 23 |
| `b3a_mg1` | `pidlink` | 25.490 | 77 |
| `b3a_mg2` | `pidlink` + `movenum` | 17.475 | 44 |
| `b3a_pk1` | `pidlink` | 21.736 | 37 |
| `b3a_pk2` | `pidlink` + `pk2type` | 369.512 | 8 |
| `b3a_pk3` | `pidlink` + `pk3type` | 42.808 | 16 |
| `b3a_sr1` | `pidlink` | 25.490 | 12 |
| `b3a_sr2` | no determinada | 4.399 | 35 |
| `b3a_sw` | `pidlink` | 25.490 | 28 |
| `b3a_tk1` | `pidlink` | 25.490 | 19 |
| `b3a_tk2` | `pidlink` | 17.333 | 84 |
| `b3a_tk3` | `pidlink` + `tk28yr` | 76.488 | 43 |
| `b3a_tk4` | `pidlink` | 20.433 | 26 |
| `b3b_ak` | `pidlink` + `aktype` | 39.004 | 18 |
| `b3b_ba0` | `pidlink` | 25.470 | 52 |
| `b3b_ba1` | `pidlink` | 11.894 | 53 |
| `b3b_ba2` | `pidlink` | 25.470 | 18 |
| `b3b_ba3` | no determinada | 72.689 | 21 |
| `b3b_ba4` | `pidlink` | 25.470 | 20 |
| `b3b_ba5` | `pidlink` | 25.470 | 15 |
| `b3b_ba6` | no determinada | 12.397 | 43 |
| `b3b_bh1` | `pidlink` | 25.470 | 15 |
| `b3b_bh2` | no determinada | 3.335 | 27 |
| `b3b_cov` | `pidlink` | 25.829 | 48 |
| `b3b_kk` | `pidlink` | 25.470 | 50 |
| `b3b_km` | `pidlink` | 25.470 | 36 |
| `b3b_ma1` | `pidlink` + `matype` | 369.397 | 8 |
| `b3b_ma2` | `pidlink` | 25.470 | 13 |
| `b3b_pm1` | no determinada | 40.688 | 17 |
| `b3b_pm3` | `pidlink` + `pm3type` | 219.582 | 16 |
| `b3b_pm4` | `pidlink` | 25.470 | 11 |
| `b3b_ps` | `pidlink` + `pstype` | 127.242 | 10 |
| `b3b_rj1` | no determinada | 65.762 | 13 |
| `b3b_rj2` | `pidlink` + `rj2type` | 5.503 | 43 |
| `b3b_rj3` | `pidlink` | 25.470 | 17 |
| `b3b_rj4` | `pidlink` | 25.470 | 27 |
| `b3b_rn1` | `pidlink` + `rn1type` | 27.950 | 11 |
| `b3b_rn2` | `pidlink` + `rn2type` | 673 | 29 |
| `b3b_tf` | `pidlink` + `tftype` | 76.410 | 27 |
| `b3p_ba0` | `pidlink` | 1.277 | 52 |
| `b3p_ba1` | `pidlink` | 368 | 66 |
| `b3p_ba2` | `pidlink` | 1.277 | 16 |
| `b3p_ba3` | no determinada | 2.526 | 21 |
| `b3p_ba4` | `pidlink` | 1.277 | 35 |
| `b3p_ba5` | `pidlink` | 1.277 | 29 |
| `b3p_ba6` | no determinada | 1.110 | 50 |
| `b3p_bh` | `pidlink` | 1.277 | 14 |
| `b3p_br` | `pidlink` | 1.277 | 24 |
| `b3p_ch0` | `pidlink` | 527 | 9 |
| `b3p_ch1` | `pidlink` + `ch05` | 50 | 25 |
| `b3p_cov` | `pidlink` | 1.279 | 52 |
| `b3p_cx` | `pidlink` | 527 | 9 |
| `b3p_dl1` | `pidlink` | 1.277 | 22 |
| `b3p_dl3` | `pidlink` + `dl3type` | 960 | 54 |
| `b3p_dl4` | `pidlink` | 874 | 100 |
| `b3p_kk` | `pidlink` | 1.277 | 41 |
| `b3p_km` | `pidlink` | 1.277 | 16 |
| `b3p_kw` | `pidlink` | 1.277 | 34 |
| `b3p_ma` | `pidlink` + `matype` | 18.592 | 9 |
| `b3p_mg` | `pidlink` | 1.277 | 71 |
| `b3p_pm1` | no determinada | 1.463 | 18 |
| `b3p_pm3` | `pidlink` + `pm3type` | 12.770 | 15 |
| `b3p_rj` | `pidlink` + `rj1type` | 2.670 | 10 |
| `b3p_rn` | `pidlink` + `rn1type` | 1.513 | 10 |
| `b3p_tk1` | `pidlink` | 1.277 | 18 |
| `b3p_tk2` | `pidlink` | 994 | 80 |
| `b4_ba6` | no determinada | 14.007 | 46 |
| `b4_bf` | `pidlink` | 4.272 | 17 |
| `b4_br` | `pidlink` | 8.270 | 27 |
| `b4_bx6` | `pidlink` + `bx63a` | 329 | 40 |
| `b4_ch0` | `pidlink` | 8.270 | 23 |
| `b4_ch1` | `pidlink` + `ch05` | 7.170 | 130 |
| `b4_cov` | `pidlink` | 8.352 | 45 |
| `b4_cx1` | `pidlink` + `cx1type` | 66.160 | 12 |
| `b4_cx2` | `pidlink` | 8.270 | 23 |
| `b4_kl1` | `pidlink` | 8.270 | 33 |
| `b4_kl2` | `pidlink` + `year` + `month` | 463.120 | 19 |
| `b4_kw2` | `pidlink` | 8.270 | 54 |
| `b4_kw3` | `pidlink` + `kwn` | 8.729 | 21 |
| `b5_baa` | `pidlink` + `baatype` | 23.372 | 15 |
| `b5_cov` | `pidlink` | 11.739 | 47 |
| `b5_dla1` | `pidlink` | 11.686 | 66 |
| `b5_dla3` | `pidlink` + `dla3type` | 10.320 | 93 |
| `b5_dla4` | `pidlink` | 11.686 | 29 |
| `b5_maa0` | `pidlink` | 11.686 | 17 |
| `b5_maa1` | `pidlink` + `maatype` | 157.979 | 8 |
| `b5_psa` | `pidlink` + `psatype` | 58.390 | 10 |
| `b5_rja0` | `pidlink` | 11.686 | 28 |
| `b5_rja1` | `pidlink` + `rja1type` | 16.520 | 9 |
| `b5_rja2` | `pidlink` + `rja2type` | 2.687 | 43 |
| `b5_rja3` | `pidlink` | 11.686 | 62 |
| `b5_rja4` | `pidlink` + `rja4type` | 116.860 | 9 |
| `b5_rna1` | `pidlink` + `rna1type` | 12.466 | 11 |
| `b5_rna2` | `pidlink` + `rna2type` | 171 | 29 |
| `bek` | `pidlink` | 14.145 | 67 |
| `bk_ar0` | `hhid00` | 10.435 | 9 |
| `bk_ar1` | `hhid00` + `pid00` | 54.991 | 48 |
| `bk_cov` | `pidlink` | 10.435 | 39 |
| `bk_krk` | `hhid00` | 10.435 | 18 |
| `bk_sc` | `hhid00` | 10.435 | 10 |
| `bt_cov` | no determinada | 11.105 | 36 |
| `bus1_0` | `hhid00` | 10.294 | 38 |
| `bus1_1` | `hhid00` + `pid00` | 53.488 | 39 |
| `bus2_0` | `hhid00` | 10.294 | 38 |
| `bus2_1` | `hhid00` + `pid00` | 53.488 | 36 |
| `htrack` | no determinada | 11.112 | 63 |
| `ptrack` | `pidlink` | 51.142 | 69 |

**Comunidad y establecimientos (`Community Data/`)**

| Archivo | Llave única (verificada) | N | Variables |
|---|---|---:|---:|
| `bk1` | `commid00` | 311 | 328 |
| `bk1_a` | `commid00` + `atype` | 2.488 | 10 |
| `bk1_b` | no determinada | 924 | 10 |
| `bk1_cp` | `commid00` | 311 | 3 |
| `bk1_d1` | `commid00` + `d1type` | 872 | 6 |
| `bk1_d2` | `commid00` + `d2type` | 391 | 11 |
| `bk1_d3` | `commid00` + `d19type` + `d3type` | 2.092 | 24 |
| `bk1_d4` | no determinada | 235 | 13 |
| `bk1_d5` | `commid00` + `d5type` | 542 | 4 |
| `bk1_e1` | no determinada | 933 | 12 |
| `bk1_e2` | `commid00` + `e2type` | 442 | 8 |
| `bk1_g` | `commid00` + `gtype` | 2.177 | 8 |
| `bk1_ge` | `commid00` + `getype` | 1.866 | 8 |
| `bk1_i` | `commid00` + `itype` | 933 | 9 |
| `bk1_j` | `commid00` + `jtype` | 1.555 | 3 |
| `bk1_jp1` | `commid00` + `jps1type` | 608 | 7 |
| `bk1_jp2` | `commid00` + `jps2type` | 3.648 | 6 |
| `bk1_jp3` | `commid00` + `jps3type` | 507 | 16 |
| `bk1_jp4` | `commid00` + `jps4type` | 681 | 15 |
| `bk1_k0` | `commid00` | 311 | 2 |
| `bk1_k1` | `commid00` + `ktype` | 884 | 14 |
| `bk1_ls` | no determinada | 372 | 6 |
| `bk1_pmkd` | `commid00` + `pmkdtype` | 3.110 | 10 |
| `bk2` | `commid00` | 312 | 213 |
| `bk2_cp` | `commid00` | 312 | 2 |
| `bk2_hpj` | `commid00` + `hpj3type` | 4.056 | 28 |
| `bk2_ka1` | `commid00` + `ka1type` | 154 | 8 |
| `bk2_ka2` | `commid00` + `ka2type` | 3.432 | 7 |
| `bk2_kd` | `commid00` + `kdyear` | 936 | 41 |
| `jps` | `commid00` | 303 | 206 |
| `jps_cp` | `commid00` | 303 | 2 |
| `jps_jps1` | `commid00` + `jps1type` | 1.475 | 24 |
| `jps_jps2` | `commid00` + `jps2type` | 717 | 14 |
| `mini` | `mkid00` | 1.660 | 120 |
| `mini_sn1` | no determinada | 16.600 | 6 |
| `mini_sn2` | no determinada | 4.980 | 9 |
| `pkk` | `commid00` | 311 | 83 |
| `pkk_cp` | `commid00` | 311 | 2 |
| `pkk_i` | `commid00` + `itype` | 933 | 9 |
| `pkk_j` | no determinada | 1.555 | 5 |
| `pkk_kr` | `commid00` + `krtype` | 379 | 10 |
| `pkk_ksr1` | `commid00` + `ksr1type` | 1.244 | 7 |
| `pkk_ksr2` | `commid00` + `ksr2type` | 1.244 | 8 |
| `pkk_pm` | `commid00` + `pmtype` | 2.799 | 10 |
| `pm` | `commid00` | 304 | 225 |
| `pm_cp` | no determinada | 307 | 2 |
| `pm_k` | no determinada | 337 | 13 |
| `pos` | `fcode00` | 630 | 159 |
| `pos_b1` | `fcode00` + `b1type` | 5.670 | 16 |
| `pos_b2` | `commid00` + `b2type` + `fascode` | 3.150 | 11 |
| `pos_c` | `commid00` + `ctype` + `fascode` | 2.919 | 16 |
| `pos_cp` | no determinada | 631 | 4 |
| `pos_d` | `commid00` + `dtype` + `fascode` | 8.190 | 10 |
| `pos_h` | `commid00` + `htype` + `fascode` | 26.460 | 10 |
| `pos_prp` | `commid00` + `prptype` + `fascode` | 918 | 14 |
| `pra` | no determinada | 1.907 | 255 |
| `pra_a` | `commid00` + `atype` + `fascode` | 20.944 | 8 |
| `pra_b1` | `fcode00` + `b1type` | 13.328 | 20 |
| `pra_b2` | `commid00` + `b2type` + `fascode` | 78.064 | 8 |
| `pra_b3` | `commid00` + `b3type` + `fascode` | 7.616 | 25 |
| `pra_b4` | `commid00` + `b4type` + `fascode` | 15.232 | 10 |
| `pra_c1` | `commid00` + `c1type` + `fascode` | 39.984 | 8 |
| `pra_c2` | `commid00` + `c2type` + `fascode` | 41.888 | 7 |
| `pra_cp` | `fcode00` | 1.904 | 4 |
| `pra_d1` | `commid00` + `d1type` + `fascode` | 61.982 | 22 |
| `pra_f` | `commid00` + `ftype` + `fascode` | 24.752 | 11 |
| `pusk` | `fcode00` | 943 | 501 |
| `pusk_a1` | `commid00` + `atype` + `fascode` | 10.406 | 8 |
| `pusk_b1` | `commid00` + `btype` + `fascode` | 5.676 | 19 |
| `pusk_c1` | `commid00` + `c1type` + `fascode` | 36.894 | 8 |
| `pusk_c2` | `commid00` + `c2type` + `fascode` | 3.784 | 14 |
| `pusk_c3` | `commid00` + `c3type` + `fascode` | 7.568 | 11 |
| `pusk_cp` | `commid00` + `fcode00` | 946 | 4 |
| `pusk_d` | no determinada | 8.360 | 11 |
| `pusk_dm` | `commid00` + `dmtype` + `fascode` | 7.560 | 11 |
| `pusk_e1` | `commid00` + `e1type` + `fascode` | 20.812 | 10 |
| `pusk_e2` | `commid00` + `e2type` + `fascode` | 15.136 | 7 |
| `pusk_f` | `commid00` + `ftype` + `fascode` | 32.164 | 21 |
| `pusk_g` | `commid00` + `gtype` + `fascode` | 12.298 | 10 |
| `pusk_jps` | `commid00` + `jps1type` + `fascode` | 11.352 | 11 |
| `sar` | no determinada | 24.653 | 33 |
| `sar_cov` | no determinada | 322 | 26 |
| `sar_cp` | no determinada | 322 | 1 |
| `schl` | `fcode00` | 2.529 | 469 |
| `schl_b2` | `commid00` + `b2type` + `fascode` | 1.668 | 10 |
| `schl_b3` | `commid00` + `b3type` + `fascode` | 2.784 | 10 |
| `schl_b5` | no determinada | 22.797 | 18 |
| `schl_b6` | `commid00` + `b6type` + `fascode` | 6.135 | 21 |
| `schl_c` | no determinada | 5.053 | 82 |
| `schl_cp` | no determinada | 2.533 | 4 |
| `schl_e` | no determinada | 50.660 | 9 |

## 6. Cómo manejar los datos

### 6.1 Identificadores

| Variable | Tipo | Qué es | Notas (verificadas en los archivos salvo que se indique) |
|---|---|---|---|
| `hhid00` | texto, 7 | EA (3) + hogar (2) + origen/*split-off* (2) | `00` = origen; sexto dígito `1` = *split-off* de 1997, `2` = de 1998, `3` = nuevo en 2000 (vol. 2). En `htrack` está vacío solo para 97 hogares con `result00` = 9 (todos muertos antes de 2000) |
| `hhid00_9` | texto, 9 | Versión de 9 caracteres de `hhid00` (`htrack`, `ptrack`) | |
| `pid00` | número | Línea en el roster de 2000 | Puede diferir del `pid93`/`pid97` de la misma persona |
| `pidlink` | texto, 9 | Persona, constante entre olas | Único en `ptrack` y en `bek`. **Repetido en `bus1_1`/`bus2_1`** (5.160) porque el roster acumula a quienes se fueron (`ar01a` = 3). RAND: quitar los registros con `ar01a` = 3 o usar `hhid00` + `pid00` |
| `commid00` | texto, 4 | Provincia (2) + secuencia (2) | En los hogares entrevistados: 7.494 con código numérico (las 312 comunidades IFLS) y **2.941 con letras** (hogares fuera de las comunidades IFLS; según RAND, definido al nivel del subdistrito). Ninguno vacío |
| `mkid00` | texto, 5 | `commid00` + un carácter de área local | Llave del **mini-CFS** (`mini`, 1.660 áreas). De los 2.941 hogares entrevistados fuera de comunidades IFLS, 2.296 tienen un `mkid00` que está en `mini`; 645 tienen `mkid00` vacío |
| `fcode00` | texto, 8 | `commid00` (4) + tipo (1) + secuencia (3) | Según vol. 2, la secuencia indica la ola en que apareció el establecimiento (< 70: 1993; 70-99: 1997; > 100: 2000). Los establecimientos que sirven a cada comunidad están en `sar` |
| `hhid93`, `hhid97`, `hhid98`, `pid93`, `pid97`, `pid98` | | Ids de olas anteriores en `htrack` y `ptrack` | |

**`commid97` en el `htrack` de 2000** es idéntico al del `htrack` de 1997 y sigue vacío para los 894 hogares de 1997 que vivían fuera de comunidades IFLS. La guía de usuario dice que todos los hogares encontrados en una ola tienen `commid` de esa ola; en los datos, eso se cumple para 2000 pero no para 1997.

**Archivos sin llave única** con las combinaciones estándar: los de hermanos e hijos fuera del hogar (`b3b_ba3`, `b3b_ba6`, `b4_ba6` y proxy), uso de servicios (`b3b_rj1`), negocios no agrícolas (`b2_nt2`), migración circular (`b3a_sr2`), participación comunitaria (`b3b_pm1`), `bt_cov` (669 `hhid00` repetidos y 670 vacíos: el libro de seguimiento tiene una fila por visita de rastreo) y varios archivos de establecimientos y del mini-CFS. Las llaves que propone el apéndice A no se probaron una por una.

### 6.2 Códigos especiales

- Igual que en 1997: variables X (`…x`) que indican si hubo respuesta válida; último dígito 5 fuera de rango, 6 no aplica, 7 rechazó, 8 no sabe, 9 faltante (en texto: V, W, X, Y, Z). Algunos montos usan 99998 (p. ej., precios de `pos_h`).
- Sí / no = 1 / 3; sexo = 1 / 3. Años con cuatro dígitos.
- `ptrack$age_00` (y `age_93`, `age_97`) vienen como texto.

### 6.3 Trampa: enteros leídos como texto con `pyreadstat`

En 201 de los 230 archivos hay columnas enteras con faltantes que `pyreadstat` devuelve como tipo objeto (4.102 columnas; p. ej., precios de `bk2_hpj`, ítems de `bek`). `pandas.read_stata` las lee como números. Hay que convertirlas (`pd.to_numeric`) antes de calcular. El mismo fenómeno aparece en `bek` de 1997. No hay valores 1,75e+100 como en los comunitarios de 1997.

### 6.4 Proxy y formato largo

Como en 1997: el libro 3P se anexa a 3A/3B/4, y muchos archivos están en formato largo con variables `…type`. El libro 3P **no** trae los ítems de salud mental (`b3p_kk` no tiene `kk04`-`kk11`).

### 6.5 Pesos

| Archivo | Variables | Qué son (según vol. 2) |
|---|---|---|
| `htrack` | `hwt00la`, `hwt00lb` | Longitudinales de hogar 2000 (sin y con «encontrado en 1997» en el modelo de desgaste) |
| `htrack` | `hw93700l` | Longitudinal para hogares en 1993, 1997 y 2000 |
| `htrack` | `hwt00xa`, `hwt00xb` | Transversales de hogar 2000 |
| `htrack` | `hwt93`, `hwt93smp`, `hwt97l`, `hwt97x` | Pesos de olas anteriores |
| `ptrack` | `pwt00la`, `pwt00lb`, `p939700l` | Longitudinales de persona |
| `ptrack` | `pwt00xa`, `pwt00xb`, `pw00usxa`, `pw00usxb` | Transversales de persona y de evaluación de salud |
| `ptrack` | `p939700u` | Longitudinal de evaluación de salud |
| `ptrack` | `pwt97usl`, `pwt97usx`, **`pwt97ekx`** | Pesos de 1997 de salud y de pruebas cognitivas, que **no estaban en el `ptrack` de 1997** |

RAND reporta dos versiones (a y b) porque usar o no «encontrado en 1997» en el modelo de desgaste cambia el peso; no recomienda una sola.

## 7. Seguimiento

**Hogares** (`htrack$result00`; códigos de vol. 2): 10.435 entrevistados, 105 se unieron a otro hogar IFLS, 34 todos muertos, 67 rechazos, 374 no encontrados y 97 con código 9 (todos muertos antes de 2000).

- De los 7.224 hogares de 1993: 6.758 entrevistados en 2000, 292 no encontrados, 72 con código 9, 60 rechazos, 32 todos muertos y 10 unidos a otro hogar.
- `mover00` (movimiento desde la última entrevista): 7.634 no se movieron; 683 dentro de la desa; 360 dentro del kecamatan; 483 dentro del kabupaten; 708 dentro de la provincia; 496 a otra provincia IFLS; **71 con código 6**, que no está en la documentación.

**Personas del roster de 1993** (33.081; `ptrack`): 26.067 siguen en el mismo hogar (`ar01a_00` = 1), 1.464 son miembros de otro hogar IFLS en 2000 (`ar01a_00` = 5), 1.363 murieron, 2.784 dejaron el hogar sin ser ubicados y 1.403 no tienen información de 2000.

**Niños de 0 a 5 años en 1997** (`ptrack$age_97` ≤ 5 y `member97` = 1): 3.851; 3.646 son miembros de un hogar en 2000, y 3.422 tienen talla medida en 2000.

## 8. Fechas de entrevista

| Mes (sin año en `bk_cov`) | Jun | Jul | Ago | Sep | Oct | Nov | Dic |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hogares en comunidades IFLS | 261 | 1.285 | 2.038 | 2.105 | 1.328 | 444 | 33 |
| Hogares fuera de comunidades IFLS | 27 | 223 | 337 | 625 | 799 | 750 | 276 |

- Libro 1 de la comunidad (`bk1`): julio a diciembre, más 4 en enero. Libro 2 (`bk2`, incluye precios de mercado): igual, 3 en enero. Posyandu: julio a enero, 3 con mes 99.
- Pruebas cognitivas (`bek$ekmth`): junio a diciembre, más 5 en enero o febrero.
- Medición de talla (`bus2_1$us17bmtb`): sobre todo de junio a diciembre; hay 9 casos con meses de enero a mayo y 4 con 99.

## 9. Contenido por tema

### 9.1 Antropometría y salud física (`bus1_1`, `bus2_1`)

- En 2000 la evaluación de salud tiene dos libros: **US-I** (`bus1_1`: fecha de nacimiento, edad, presión, pulso, capacidad pulmonar, hemoglobina, embarazo/lactancia) y **US-II** (`bus2_1`: talla, peso, circunferencias de cintura, cadera y **cabeza**, prueba de sentarse y pararse). Ambos tienen 53.488 filas, con las mismas personas (`hhid00` + `pid00`).
- Las filas incluyen a todos los listados en el roster: 31.976 miembros que siguen (`ar01a` = 1), 10.606 nuevos (5), 9.413 que ya no viven en el hogar (3) y 1.493 muertos (0).
- **Talla válida** (`us04x` = 1): 36.482. Peso válido (`us06x` = 1): 36.207. De pie 34.833 / acostado 1.619 (`us05`). Rango de talla observado: 10,4 a 191,7 cm (el mínimo es claramente un error).
- `us00` (¿se midió?) toma, entre otros, 1 (36.402), 6 (10.474), 9 (4.231) y 0 (1.497); los significados están en `ifls2000_hhd_BUS.cbk` y no se revisaron uno por uno.
- **Fecha de nacimiento en US-I** (`us02yr`): incluye 1.000 casos con 9998 y 559 con 9999. Otras fuentes de edad: `bk_ar1` y `ptrack` (`age_00`, `bth_year`, `bthmonth`, `bth_day`).
- **Niños:** 4.893 miembros de 0 a 5 años en 2000 (`ptrack$age_00`). Seguimiento de la cohorte de 0-5 en 1997: ver §7.

### 9.2 Salud mental de adultos (`b3b_kk`)

- **Vuelven los síntomas psicológicos.** Ocho ítems sobre las últimas 4 semanas, escala 1 = a menudo, 3 = a veces, 5 = nunca, sin faltantes en los 25.470 respondientes de 3B:

| Ítem | Contenido | A menudo | A veces | Nunca |
|---|---|---:|---:|---:|
| `kk04` | Dificultad para dormir | 2.254 | 5.406 | 17.810 |
| `kk05` | Molesto por cosas | 721 | 3.615 | 21.134 |
| `kk06` | Soledad | 525 | 2.547 | 22.398 |
| `kk07` | Tristeza | 1.674 | 6.651 | 17.145 |
| `kk08` | Ansiedad o miedo | 851 | 4.821 | 19.798 |
| `kk09` | Dificultad para concentrarse | 808 | 4.484 | 20.178 |
| `kk10` | Dificultad con las tareas | 609 | 3.234 | 21.627 |
| `kk11` | Dificultad para recordar | 2.204 | 6.014 | 17.252 |

- Correspondencia con 1993 (verificada en la ronda 1): solo `kk04` (insomnio), `kk07` (tristeza) y `kk08` (ansiedad) coinciden con ítems de 1993. En 1997 no hubo ítems psicológicos.
- **Población:** en 2000 el libro 3B se aplicó a todos los adultos de los hogares de origen y a los miembros de 1993 (y familia cercana) en los *split-off*; en 1993 fue una submuestra. No hay ítems en el libro proxy.
- También en `b3b_kk`: salud autorreportada, comparación con hace 12 meses, expectativa de salud, actividades de la vida diaria (`kk03*`).

### 9.3 Educación

- **Adultos (`b3a_dl1`, 25.490):** a diferencia de 1997, el nivel más alto (`dl06`) y el grado se preguntan a **todos** los que asistieron alguna vez (22.464), no solo a los de 50+. `dl07a` (asiste hoy) tiene respuesta para 18.979. La historia por nivel está en `b3a_dl2`/`dl3` y gastos en `dl4`.
- **Niños (`b5_dla1`, 11.686):** 7.195 asistieron alguna vez y 6.832 siguen asistiendo. Historia escolar en `b5_dla3` y `b5_dla4`.
- **Roster (`bk_ar1`):** nivel y grado para todos los miembros.

### 9.4 Pruebas cognitivas (`bek`)

- **14.145 personas**, una fila por persona (`hhid00` + `pid00` y `pidlink` únicos). Formato distinto al de 1997: una columna por ítem (`ek0`-`ek22`, respuesta; `ek0x`-`ek22x`, 1 correcta / 3 incorrecta / 9 faltante). **No hay puntaje total**: hay que construirlo.
- **Dos versiones según la edad** (`ekage`): 7-14 años (6.182) y 15-24 años (7.963). Según el codebook, la primera tiene 12 preguntas «cognitivas» y 5 de matemáticas; la segunda, 8 cognitivas y 5 de matemáticas más difíciles; los números de pregunta son comunes, así que el ítem 6 es el mismo en ambas. En los datos:

| Versión | Ítems con respuesta | |
|---|---|---|
| 7-14 | `ek0`-`ek12` (13 ítems) y `ek13`-`ek17` (5) | Respuestas en `ek13`-`ek17` bajan de ≈5.500 a ≈4.700 |
| 15-24 | `ek0`-`ek6`, `ek11`, `ek12` (9 ítems) y `ek18`-`ek22` (5) | |

  El codebook habla de 12 y 8 preguntas cognitivas; los datos tienen 13 y 9 con respuesta (`ek0` incluido). No se revisó en el cuestionario si `ek0` es un ejemplo.
- **Resultado** (`ekc3`): 12.095 terminaron, 1.246 no completaron, 804 no respondieron (motivos en `ekc33`: rechazo 265, proxy 179, analfabetismo 81…).
- **Edad:** según `ptrack`, la mediana es 11 años en la versión de 7-14 y 20 en la de 15-24, pero hay valores de 1 a 57 años; no se revisaron.
- **Cohorte de 1997:** 1.240 de los evaluados en 2000 tenían 5 años o menos en 1997 (casi todos 4 o 5 años), según `ptrack$age_97`.
- **Las pruebas de 2000 no son las de 1997** (el codebook dice que se rediseñaron): en 1997 eran pruebas de matemáticas e indonesio por nivel; en 2000, ítems cognitivos comunes más matemáticas.
- **Nota para 1997:** `ptrack` de 2000 trae `res97ekm` (matemáticas) y `res97ekb` (bahasa) de 1997. Cruzados con `bek` de 1997, el resultado de las pruebas con número (`1`-`4`) coincide con `res97ekm` en el 99,8-100 % de los casos en los cuatro niveles, y el de las letras (`A`-`D`) con `res97ekb`. Esto confirma también para los niveles 3 y 4 que los números son matemáticas y las letras bahasa (actualizado en la guía de 1997).

### 9.5 Arroz: consumo, precio pagado y arroz subsidiado

- **`b1_ks1`** (consumo de la última semana por tipo de alimento, en rupias): compras (`ks02`) y producción propia (`ks03`), como en 1997.
- **`b1_ks4` ahora incluye arroz** (`ks4type` = A): ¿compró el último mes? (7.359 sí, 2.897 no), cantidad (`ks13`), unidad (`ks14`: kg 5.620, litro 1.609, otras 130) y precio pagado (`ks15`). Precio implícito (`ks15`/`ks13`, solo en kg, sin limpiar): mediana Rp 2.000 por kg; p1 970; p99 5.000; con atípicos de 1 a 350.000.
- **Arroz subsidiado (OPK) y ayudas** (`b1_ksr1`, `b1_ksr3`, `b1_ksr4`): 3.560 hogares compraron en un mercado subsidiado en los últimos 12 meses (`ksr11a`); 3.403 de ellos compraron arroz (`b1_ksr4`, `ksr2type` = B), con fecha de primera compra, frecuencia, costo y precio en el mercado privado (`ksr16`). `b1_ksr3`: ayudas recibidas (dinero, arroz, otros alimentos).

### 9.6 Agricultura y choques

- `b2_ut1`/`b2_ut2`: tierra, ingreso y activos agrícolas.
- **`b2_ge`: choques de los últimos 12 meses** (en 1997 eran 5 años), 8 tipos (muerte, enfermedad, pérdida de cosecha, desastre, pérdida de empleo o negocio, caída de ingresos y dos «otros»): 4.048 respuestas «sí» en 82.152 filas.

### 9.7 Otros módulos nuevos o ampliados

Libro de seguimiento (`bt_cov`), transferencias y arisan (`b3b_tf`), historia de préstamos (`b3b_bh*`), bienestar subjetivo (`b3a_sw`), migración circular (`b3a_sr*`), uso de servicios y seguro (`b3b_rj*`, `b3b_ak`), lactancia y embarazos (`b4_*`), vacunas y uso de servicios de los niños (`b5_rja*`).

## 10. Datos comunitarios de 2000

**Precios del arroz:**

| Fuente | Archivo | Qué mide | Cobertura | Respuestas | Unidad / valores (Rp por kg, sin limpiar) |
|---|---|---|---|---|---|
| Informante PKK | — | **El libro PKK de 2000 no tiene módulo de precios** (en 1993 y 1997 sí) | — | — | — |
| Posyandu | `pos_h`, `htype` 1-3 (calidad alta, media, baja) | Precio por unidad | 630 puestos en 310 comunidades | 1.890 filas; `h01x` casi siempre vacío, `h01` con valor en todas (incluye 99998) | kg 1.320, litro 488, otras 82. Medianas: alta 2.400, media 2.000, baja 1.800 |
| Tiendas y mercados | `bk2_hpj`, `hpj3type` = 1 (calidad media), en formato **ancho**: comerciante 1 (`hpj5`), 2 (`hpj13`), 3 (`hpj21`) | Precio por kg | 312 comunidades | 685 precios válidos en 250 comunidades | Mediana 2.000; p1 1.500; p99 3.200; máximo 25.000 |
| Hogares | `b1_ks4` | Precio pagado (§9.5) | Hogares que compraron | 5.612 en kg | Mediana 2.000 |

- En `bk2_hpj` el formato cambió frente a 1997 (antes una fila por comerciante; ahora tres columnas por comunidad y producto). Los tres comerciantes tienden a ser de tipos distintos: el 1 casi siempre un *warung* (puesto pequeño), el 2 una tienda y el 3 un mercado (`hpj2`, `hpj10`, `hpj18`; códigos de `hpj2` en el codebook `BK2`, asumidos iguales para los otros dos).
- **Programas sociales** (nuevos): `pkk_ksr1` (ayudas en la comunidad: dinero, arroz…), `pkk_ksr2` (venta de arroz, azúcar y aceite por debajo del precio de mercado en los últimos 12 meses, con ahorro aproximado por unidad), `jps*` (red de seguridad social en salud), `bk1_jp*`.
- **Mini-CFS** (`mini`, `mini_sn1`, `mini_sn2`): cuestionario corto de comunidad para 1.660 áreas donde viven hogares que se mudaron (§6.1).
- Otros: `bk1*` (jefe de comunidad), `bk2*` (estadísticas y finanzas de la comunidad, `bk2_kd`), `pm*`, `sar*`, salud (`pusk*`, `pra*`, `pos*`) y escuelas (`schl*`).

## 11. Enlace con 1993 y 1997 (verificado)

- `htrack` de 2000 trae `hhid93`, `hhid97`, `hhid98` y `commid93`/`commid97`; los `commid97` coinciden con el `htrack` de 1997.
- 6.564 hogares tienen entrevista en las tres olas completas.
- `ptrack` de 2000 trae `member93`, `member97`, `member98`, `member00`, ids de cada ola, edades (`age_93`, `age_97`, `age_00`) y los pesos de todas las olas. Según la guía de usuario, las edades de cada ola se calcularon por separado y no tienen por qué ser consistentes entre sí.
- Para unir personas entre olas se usa `pidlink`; `hhid00` + `pid00` no corresponde a `hhid93` + `pid93` (vol. 2, §4).

## 12. Preguntas abiertas (se deciden con todas las olas revisadas)

- **Comunidad de residencia:** `commid00` con letras para 2.941 hogares (subdistrito, no comunidad IFLS) y `mkid00` para unir con el mini-CFS (§6.1).
- **Precio del arroz en 2000:** fuente (posyandu, mercado, hogares), calidad, unidades y atípicos; no hay precio PKK como en 1993 y 1997 (§10).
- **Edad en meses para HAZ:** `bus1_1` (fecha de nacimiento, con códigos 9998/9999), `bk_ar1` y `ptrack` (§9.1).
- **Pruebas cognitivas:** cómo construir puntajes con ítems comunes y específicos por versión; comparabilidad nula con 1997 (§9.4).
- **Síntomas de salud mental:** qué ítems y escala usar; solo 3 se comparan con 1993 (§9.2).
- **Pesos:** versión a o b; longitudinales o transversales (§6.5).
- **Programas sociales (OPK, ayudas):** si se usan y cómo (§9.5, §10).

## 13. Lo que no está verificado

- Por qué `bk_cov` no tiene año ni si todas las entrevistas son de 2000 (la portada del codebook dice que el campo llegó a febrero de 2001).
- El código 6 de `mover00` (71 hogares) y el significado de la categoría «parcial» del libro 5.
- Si `ek0` es un ítem de ejemplo y por qué los datos tienen un ítem cognitivo más que lo que dice el codebook.
- Los conteos distintos del apéndice A (19 archivos) y las cifras de `htrack`/`ptrack` en el texto de la guía.
- Las llaves de los archivos marcados «no determinada».
- Los códigos de `us00` y los valores extremos de talla, edad y precios.
- La comparabilidad de las preguntas de consumo y precio entre 1997 y 2000.
