# IFLS 1993-2015 · Síntesis de la revisión de datos de las cinco olas

*Documento de síntesis escrito el 14-nov-2026 para el proyecto final de Ciencia de Datos (ECON-3785). Junta los hallazgos de las cinco guías de ola (`IFLS1/00_guia_IFLS1.md` a `IFLS5/00_guia_IFLS5.md`). **No es una revisión nueva de los archivos**: todas las cifras vienen de esas guías, que a su vez salen de los `.dta` (Python + `pyreadstat`) o de la documentación de RAND citada en cada una. Para el detalle, la fuente y el script de cada cifra, ir a la guía de la ola (se indica la sección entre paréntesis, p. ej., «G2 §9.4» = guía de IFLS2, sección 9.4).*

*Igual que las guías, este documento es **descriptivo**: dice qué hay, cómo está codificado, qué falta y qué problemas tiene. No asigna variables a resultado, control o muestra ni recomienda cómo usar los datos. Las opciones quedan en §11 («Preguntas abiertas»), sin recomendación.*

---

## 1. Panorama de las cinco olas

| | IFLS1 | IFLS2 | IFLS3 | IFLS4 | IFLS5 |
|---|---|---|---|---|---|
| Año de referencia | 1993 | 1997 | 2000 | 2007 | 2014 |
| Campo según los datos (primera visita, libro K) | ago-1993 a ene-1994 | ago-1997 a abr-1998 | jun a dic (sin año en `bk_cov`) | nov-2007 a jul-2008 | sep-2014 a sep-2015 |
| Filas en `htrack` | — (no hay) | 8.116 | 11.112 | 15.146 | 19.401 (acumulativo) |
| Hogares entrevistados | 7.224 con roster (7.730 en la muestra K) | 7.620 | 10.435 | 13.536 (`res07bk` = 1) | 15.921 |
| … de ellos *split-off* | — | 878 | 3.677 | 7.107 | 9.877 |
| Filas en `ptrack` | — (roster: 33.081) | 39.785 | 51.142 | 66.784 | 83.780 |
| Miembros de un hogar en la ola | 33.081 | 33.937 | 43.649 | 50.582 | 58.549 |
| Comunidades IFLS | 312 `commid93` (321 EA) | 312 | 312 | 312 (+ códigos raros) | 311 `commid14` (320 EA) |
| Hogares fuera de comunidades IFLS | — | 894 sin `commid97` | 2.941 (`commid00` con letras) | 5.039 | 6.815 |
| Archivos `.dta` (hogar / comunidad) | 109 / 53 | 126 / 69 | 139 / 91 | 171 / 119 | 152 / 150 |
| Formato `.dta` | Stata 6 | 108 (hogar), 104 (comunidad) | 113 | 111 (uno en 113) | 111 |
| Problemas de lectura con `pyreadstat` | ninguno señalado | comunitarios: faltantes leídos como 1,75e+100 | enteros con faltantes leídos como texto | ninguno | ninguno |

Fuentes: G1 §1, §5; G2 §1, §2; G3 §1, §2; G4 §1, §2; G5 §1, §2.

**Panel de hogares.** 6.564 hogares con entrevista en 1993, 1997 y 2000 (G3 §1); 6.010 en las cuatro primeras olas (G4 §1); 5.564 en las cinco (G5 §1). 17.309 personas son miembros de un hogar en las cinco olas (G5 §1).

**Versión de 1993.** Los archivos son el **IFLS1-RR** (reedición de 2000): correcciones aplicadas, valor original en `VAR_`, doce pares de subarchivos fusionados (G1 §2).

**Lo que no está en la descarga.** La submuestra IFLS2+ (1998, 25 % de los hogares en 7 provincias) no es pública; sus ids (`hhid98`, `member98`) sí aparecen en los `htrack`/`ptrack` posteriores (G2 §8, G3 §6.1).

## 2. Estructura común de la encuesta

### 2.1 Libros

| Libro | Contenido | Cambios entre olas |
|---|---|---|
| K | Control, roster (`ar*`), ubicación | En 1993, `bukk*`; desde 1997, `bk_*` |
| 1 | Consumo, precios pagados, programas de alimentos | Precio del arroz pagado por el hogar solo desde 2000 (§7.5) |
| 2 | Economía del hogar: activos, negocio, agricultura, choques | Módulo de choques cambia de forma y desaparece en 2007 (§7.7) |
| 3A / 3B | Adultos: educación, empleo, migración, salud, salud mental | **1993: submuestra** (jefe y cónyuge, una persona de 50+ y, en ¼ de los hogares, una de 15-49). **Desde 1997: todos los adultos** de hogares de origen y, en *split-off*, los miembros de 1993 con cónyuge e hijos (G1 §4, G2 §4) |
| Proxy | Adulto que no pudo responder | 1993: sin libro aparte; 1997-2000 `b3p_*`; 2007 `bp_*`; **2014: sin archivos** (G5 §6.3) |
| 4 | Mujeres alguna vez casadas de 15-49 | — |
| 5 | Niños menores de 15 | 1993: hasta dos hijos del jefe o cónyuge, por proxy. Desde 1997: todos los menores de 15 |
| CA / US | Antropometría y salud física | 1993 `bukcca*`; 1997 `bus_*`; 2000 dos libros (`bus1_1`, `bus2_1`); 2007 siete archivos; 2014 un archivo (`bus_us`) |
| EK | Pruebas cognitivas | No existe en 1993; diseño distinto en 1997; mismo diseño 2000-2014 con cambios (§7.4) |
| Comunidad | Jefe de comunidad, PKK, establecimientos, precios | Las fuentes de precios del arroz cambian en cada ola (§7.6) |

### 2.2 Convenciones de codificación (iguales en todas las olas)

- **Sí / no = 1 / 3. Sexo = 1 hombre / 3 mujer.**
- **Códigos especiales por el último dígito** según el ancho: 5 fuera de rango, 6 no aplica, 7 rechazo, 8 no sabe, 9 faltante (95-99, 995-999…; en texto V-Z). En variables de un dígito, **5 puede ser una respuesta válida** (p. ej., `kk05_*` de 1993: 5 = nunca) (G1 §6.2).
- **Variables X** (`…x`) desde 1997: indican si hubo respuesta válida (y a veces la unidad); el valor está en la variable sin `x` (G2 §6.2).
- **Años con dos dígitos en 1993** (93 = 1993) y con cuatro desde 1997.
- **Formato largo** en muchos módulos (consumo, activos, choques, síntomas, CES-D, calendario anticonceptivo), con una variable `…type` (desde 1997) o con nombres propios en 1993 (`item`, `assettyp`, `typehard`…).
- **Etiquetas de valores**: casi no vienen en los `.dta`; están en los codebooks (y en IFLS5, también en formatos SAS `.inc`).
- **Rupias nominales** de cada ola; algunos montos se pidieron en miles (riesgo de atípicos de factor 1.000; revisado solo en 1993) (G1 §6.3).

## 3. Identificadores

### 3.1 Llaves por ola

| Nivel | 1993 | 1997 | 2000 | 2007 | 2014 |
|---|---|---|---|---|---|
| Hogar | `hhid93` (7) | `hhid97` (7) | `hhid00` (7; `hhid00_9`) | `hhid07` (7; `hhid07_9`) | `hhid14` (7; `hhid14_9`) |
| Persona en la ola | `hhid93` + `pid93` | `hhid97` + `pid97` | `hhid00` + `pid00` | `hhid07` + `pid07` | `hhid14` + `pid14` |
| Persona entre olas | `pidlink` (9) | `pidlink` | `pidlink` | `pidlink` | `pidlink` |
| Comunidad | `commid93` (312); EA `sc07` (321) | `commid97` (solo en `htrack`) | `commid00`; `mkid00` (mini-CFS) | `commid07`; `mkid07` | `commid14`; **`ea`** en los comunitarios; `mkid14` |
| Establecimiento | `fcode` (7) | `fcode` (7) | `fcode00` (8) | `fcode07`; `fascode` en precios | `fcode14`; `fascode` en precios |

- **Todos los ids son texto con ceros a la izquierda** (G1 §6.1).
- **Sexto dígito del `hhid`**: 0 hogar de origen; 1 *split-off* de 1997; 2 de 1998; 3 de 2000; 4 de 2007; 5 de 2014 (G3 §6.1, G4 §6.1, G5 §6.1).
- **`pidXX` puede cambiar entre olas** para la misma persona; RAND indica unir entre olas con `pidlink` (G3 §11).
- **`hhid14_9` no es `hhid14` con dos dígitos más** (ejemplo en G5 §6.1). La relación entre `hhidXX` y `hhidXX_9` solo se revisó en 2014.

### 3.2 Dónde `pidlink` no es único

| Ola | Archivo | Qué pasa |
|---|---|---|
| 1993 | `bukcca2` | 4 filas con `person = 96` (medidos fuera del roster, sin `pidlink` propio) (G1 §6.1) |
| 1997 | `bk_ar1`, `bus_1` | 1.464 y 1.245 repetidos: quien se mudó aparece en el hogar de origen (`ar01a` = 3) y en el *split-off* (G2 §6.1) |
| 2000 | `bus1_1`, `bus2_1` | 5.160 repetidos: el roster acumula a quienes se fueron (G3 §6.1) |
| 2007 | `bus1_*` | 9.161 repetidos (G4 §6.1) |
| 2014 | `bk_ar1` | 13.702 repetidos. Quitar `ar01a = 3` deja 292; quitando también `ar01a = 0` quedan 14; quitando además `ar01a = 6`, 8 (G5 §6.1) |
| 2014 | `ptrack` | 3 repetidos (una fila duplicada exacta y dos personas en dos hogares); 246 filas con `ar01a_14` = 6 «duplicado» (G5 §6.1) |
| 2014 | varios | 3 `pidlink` de 8 caracteres (hogar `1410341`) (G5 §6.1) |

Otros no únicos conocidos: `buk1ks1` de 1993 tiene 56 pares `hhid93` + `item` duplicados, con valores distintos (G1 §6.1); en 1997, filas duplicadas exactas en `b3b_rj1`, `b3b_rn1`, `b5_rna1` y un `fcode` repetido por tipo de establecimiento (G2 §6.1); en 2014, 12 pares `hhid14` + `ndtype` repetidos en `b2_nd2` (G5 §9.6). Cada guía lista además los archivos con llave «no determinada».

### 3.3 Códigos de `ar01a` (estado de la persona en el roster)

Según el codebook `PTRACK` de 2014: 0 muerto, 1 sigue en el hogar, 2 estaba en otro hogar IFLS en la ronda anterior, 3 ya no vive ahí, 5 nuevo miembro, 6 duplicado, 11 regresó en la misma ronda (G5 §6.1). En 1997 aparecen 3 y 4 para quien se mudó a un *split-off* (G2 §6.1); en 2007, el 2 figura como «*ART comeback*» (G4 §7).

## 4. Seguimiento y desgaste

### 4.1 Hogares de 1993 (7.224) en cada ola

| | 1997 | 2000 | 2007 | 2014 |
|---|---:|---:|---:|---:|
| Entrevistados | 6.742 de origen (RAND: ≥ 1 miembro en el 93,5 %) | 6.758 | 6.234 (`result07` = 1) | 5.917 |
| No encontrados | — | 292 | 489 | 532 |

Fuentes: G2 §1, §7; G3 §7; G4 §7; G5 §7. Los códigos de resultado no son iguales entre olas: en 2014 los códigos 2-4 del codebook (2 rechazo, 3 unido, 4 muertos) no coinciden con la guía de usuario (2 unido, 3 muertos, 4 rechazo), y 6 y 8 no están en la guía (G5 §7). En 2007, `result07` = 1 en 13.270 hogares y `res07bk` = 1 en 13.536 (G4 §6.1).

### 4.2 Personas del roster de 1993 (33.081)

| | 1997 | 2000 | 2007 | 2014 |
|---|---:|---:|---:|---:|
| Siguen en el mismo hogar | 25.769 | 26.067 | 18.868 | 16.276 |
| Muertos | 857 | 1.363 | 4.093 | 5.733 |
| Miembros de un hogar en la ola | — | — | 23.902 | 20.692 |

Fuentes: G2 §7; G3 §7; G4 §7; G5 §7. Las cifras de seguimiento de las guías de usuario de RAND no coinciden exactamente con `ptrack` en 2007 ni en 2014.

### 4.3 Cohorte de 0 a 5 años en 1997

Definición usada en las guías: `ptrack$age_97` ≤ 5 y `member97` = 1. Son **3.851** (G3 §7; la guía de 1997 cuenta 3.852 miembros de 0-5 años, G2 §9.1).

| Ola | Edad | Miembros del hogar | Talla medida | Pruebas cognitivas | Otros |
|---|---|---:|---:|---|---|
| 1993 | −4 a 1 | — | — | — | Solo los nacidos en 1992-93 pueden aparecer medidos en 1993 (≈ 1.100 con año de nacimiento 92 o 93) (G1 §7.1) |
| 1997 | 0-5 | 3.852 | 3.217 | — (EK es para 7-24; 43 menores de 7 en el nivel 1) | 1.273 ya estaban en el roster de 1993 (G2 §9.1) |
| 2000 | 3-8 | 3.646 | 3.422 | 1.240 evaluados (casi todos de 4-5 años en 1997) | (G3 §7, §9.4) |
| 2007 | 9-19 (mediana 13) | 3.451 | 3.284 | EK1 3.361; EK2 727 | Libro 5: 2.643; libro 3A: 700 (G4 §7) |
| 2014 | 15-25 (mediana 19) | 2.846 | 2.586 | EK1 o EK2 completos: 2.535 | Educación (`dl06`) 2.682; CES-D 2.578; muertos 97 (G5 §7) |

### 4.4 Cohorte de 5 a 21 años en 1997 (en 2014)

12.632 miembros en 1997; en 2014: 8.423 miembros, 401 muertos, 7.993 con `b3a_dl1` (7.925 con `dl06`), 7.650 con talla y 7.250 con EK1 o EK2 completos (G5 §7).

### 4.5 Edades entre olas

- RAND calculó las edades de cada ola por separado; no tienen por qué ser consistentes (G3 §11).
- En 2014, para los miembros de 1997, `age_14` − `age_97` tiene mediana 17, pero 3.160 de 30.104 caen fuera de 16-19 (mínimo −99, máximo 75). `bth_year` falta en 12.141 filas de `ptrack` y va de 1895 a 2014 (G5 §7).
- Tipo de dato: `age_93`, `age_97` y `age_00` vienen como texto en los `ptrack` de 1997 y 2000 (con el código `998`); `age_07` viene como número (G2 §6.2, G3 §6.2, G4 §6.2).

## 5. Comunidad

### 5.1 Unidad de comunidad por ola

| Ola | Qué hay |
|---|---|
| 1993 | 321 EA (`sc07`) y 312 `commid93`: 9 pares de EA «gemelas» comparten `commid93` (75-76, 80-81, 82-83, 103-104, 139-140, 188-189, 198-199, 204-205, 212-213). `commwt` está a nivel de EA (321 filas) (G1 §6.1, §8) |
| 1997 | 312 `commid97`. Está solo en `htrack`, no en los archivos de hogar. Falta para 894 hogares entrevistados fuera de comunidades IFLS (388 de origen, 506 *split-off*); 45 hogares cambiaron de una comunidad IFLS a otra (G2 §6.1, §7) |
| 2000 | `commid00` existe para todos: 7.494 hogares con código numérico y 2.941 con letras (fuera de comunidades IFLS, a nivel de subdistrito). `mkid00` une con el mini-CFS (1.660 áreas); 2.296 de los 2.941 tienen un `mkid00` que está en `mini` y 645 lo tienen vacío. El `commid97` del `htrack` de 2000 sigue vacío para los 894 de 1997 (G3 §6.1) |
| 2007 | 8.497 hogares con código numérico y 5.039 con letras; 17 con códigos numéricos que no son de las 312 (`1227`, `5115`). Los comunitarios tienen **322 filas** para 313 códigos: las 312, el código `9999` y 9 comunidades con dos filas (`3109`, `3113`, `3114`, `3134`, `3233`, `3331`, `3403`, `3409`, `3415`). Mini-CFS `mkd_*` (3.122 áreas) (G4 §6.1, §10) |
| 2014 | Los comunitarios son **por EA** (`ea` = 001-320; 320 filas) para 311 `commid14`. Los 9 códigos con dos EA son los mismos 9 de 2007. **`htrack` no trae `ea`.** 9.106 hogares con código numérico y 6.815 con letras; 3 hogares con `3249`, que no está en `bk1`. Mini-CFS `mkd_cov` (4.032 áreas); 6.551 de los 6.815 tienen un `mkid14` que está en `mkd_cov` (G5 §6.1, §10) |

No se verificó que las 9 comunidades con dos filas en 2007 y dos EA en 2014 sean los 9 pares de EA gemelas de 1993 (G4 §6.1, G5 §10).

### 5.2 Ubicación geográfica

- 1993: `bukksc1` (`sc01` provincia, `sc02` kabupaten, `sc03` kecamatan, `sc05` urbano/rural), con códigos corregidos por RAND para 15 EA; el historial de migración `buk3mg2` trae lugares sin esa corrección (G1 §6.1).
- Desde 1997: `bk_sc` y `htrack` traen ubicación y `moverXX` (movimiento desde la última entrevista). Códigos no documentados de `mover`: 71 hogares con 6 en 2000; 174 con 6 y 1.671 con 98 en 2007; en 2014 el 6 sí tiene etiqueta (G3 §7, G4 §7, G5 §7).
- IFLS5 trae códigos BPS de 2014 para unir con fuentes externas (G5 §3).

## 6. Fechas

| Ola | Hogares | Comunidad y precios | Desfase |
|---|---|---|---|
| 1993 | ago-1993 a ene-1994 | No revisado | — |
| 1997 | ago-1997 a abr-1998; **627 hogares en 1998** (160 en comunidades IFLS); 96 de 312 comunidades con algún hogar en 1998 | PKK y libro 2 en 1998 en 27 comunidades (ene-feb) | Medición US: 2.123 en 1998; EK: 764 personas en 1998 (G2 §8) |
| 2000 | jun a dic (`bk_cov` sin año) | `bk1`, `bk2` jul a dic (+ algunos en enero); posyandu jul a ene | La portada de los codebooks dice ago-2000 a feb-2001 (G3 §8) |
| 2007 | nov-2007 a jul-2008 | Precios (`hin`, `hps`, `htw`): feb a jun de 2008 | Medición: 57 casos con años 2000-2006 o 2009 (G4 §8) |
| 2014 | sep-2014 a sep-2015 | Comunidad y precios: **mar a ago de 2015**, casi todo mar-jun | Buena parte de los hogares se entrevistó 3-6 meses antes que su comunidad (G5 §8) |

Los hogares fuera de comunidades IFLS se entrevistan, en promedio, más tarde en cada ola (tablas por mes en G2 §8, G3 §8, G4 §8, G5 §8).

## 7. Contenido por tema a través de las olas

### 7.1 Antropometría

| Ola | Archivo · variable | Talla válida | Codificación del no medido | Fuentes de edad |
|---|---|---:|---|---|
| 1993 | `bukcca2` · `ca10` | 22.284 de 24.515 | 0 (188) y 999,x (2.231); peso `ca13` con 9996-9999 | `ca06yr/mth`, `ca07*` (nacimiento), `ca09*` (medición), roster `ar09yr`. Menores de 5: 185 sin año de nacimiento |
| 1997 | `bus_1` · `us04` (+ `us04x`) | 28.816 | `us04x` ≠ 1; sin codebook de US | `us02*`, `us03`, `bk_ar1`, `ptrack` |
| 2000 | `bus2_1` · `us04` | 36.482 | `us04x`; mínimo 10,4 cm (error) | `bus1_1$us02yr` (1.000 con 9998, 559 con 9999), `bk_ar1`, `ptrack` |
| 2007 | `bus1_2` · `us04` | 42.310 | `us04x`; mínimo 10,7 cm (error) | `bus1_1$us02yr` (384 con 9998, 5 con 9999), `bk_ar1`, `ptrack` |
| 2014 | `bus_us` · `us04` | 47.859 (`us04x` = 1) | **Faltante, sin códigos ni ceros**; rango 42,0-198,0 | No hay fecha de nacimiento en `bus_us`: `bk_ar1`, `ptrack`, fecha de medición en `bus_time` |

- Todas las olas registran método (de pie / acostado, `ca11` o `us05`) y peso. Desde 1997 hay mediciones adicionales (presión, hemoglobina, capacidad pulmonar…); en 2007 se añaden fuerza de agarre y colesterol; en 2014, velocidad de marcha, balance y gotas de sangre seca (`dbs_*`, 7.579 personas) (G4 §9.1, G5 §9.1).
- Los archivos de medición incluyen filas de todo el roster acumulado (personas que se fueron o murieron) desde 1997 (G2 §9.1, G3 §9.1, G4 §9.1).
- `us00` (¿se midió?) tiene valores no documentados en 1997 (0 y 4) y no revisados en 2000 (G2 §9.1, G3 §9.1).
- Las fechas de medición y nacimiento permiten calcular la edad en meses en todas las olas; la consistencia entre fuentes de edad no se ha revisado en ninguna.

### 7.2 Salud mental de adultos

| Ola | Archivo | Instrumento | Periodo | Escala | Quién |
|---|---|---|---|---|---|
| 1993 | `buk3kk2` | **6 síntomas** de la sección KK: insomnio, fatiga, irritabilidad, dolores, tristeza, ansiedad. **No es el GHQ** | 4 semanas | 1 a menudo / 3 a veces / 5 nunca | Submuestra del libro III; 12.985 respondientes; casi ninguno por proxy |
| 1997 | — | **Sin ítems psicológicos** (ni en 3B ni en proxy) | — | — | — |
| 2000 | `b3b_kk` · `kk04`-`kk11` | **8 ítems**: dormir, molesto, soledad, tristeza, ansiedad, concentración, tareas, memoria | 4 semanas | 1 / 3 / 5 | Todos los adultos de 3B (25.470); no en proxy |
| 2007 | `b3b_kp` | **CES-D-10**, formato largo (`kptype` A-J); `kp01` sí/no y `kp02` frecuencia 1-4 | Semana anterior | ≤ 1 día, 1-2, 3-4, 5-7 días (con «no» aparte) | 29.029 personas; no en proxy |
| 2014 | `b3b_kp` | **CES-D-10**, mismo orden de ítems; **solo `kp02`** (sin `kp01`) | Semana anterior | 1-4; «no» y «≤ 1 día» en la misma categoría | 31.447 personas |

- **Ítems comunes entre 1993 y 2000:** solo 3 (insomnio `kk05_a` ↔ `kk04`; tristeza `kk05_e` ↔ `kk07`; ansiedad `kk05_f` ↔ `kk08`). En 1993 iban en una grilla de síntomas físicos y en 2000 como preguntas sueltas; la prevalencia de tristeza («a menudo o a veces») pasa de 15 % a 33 %, y los datos no permiten separar cambio real de cambio de instrumento (G1 §7.2).
- **CES-D de 2007 frente a 2014:** mismos 10 ítems, distinta estructura de respuesta (G5 §9.2). En 2007, **las etiquetas de `kptype` del codebook no coinciden con el cuestionario** (los datos siguen al cuestionario); en 2014 sí coinciden (G4 §9.2, G5 §9.2).
- **CES-D frente a 1993/2000:** cambian ítems, periodo de referencia y escala; hay ítems de contenido parecido (deprimido/triste, miedo/ansiedad, dormir mal/insomnio) con otra redacción (G4 §9.2).
- Derivados ya construidos para 1993 (`01_Datos/02_Procesados/salud_mental_1993.*`): `sm3_93`, `sm6_93`, `triste_93`, `ansioso_93`; su uso no está decidido (G1 §7.2).
- Módulos cercanos solo en 2014 (no revisados): afecto positivo/negativo (`b3a_pna*`), personalidad BFI (`b3b_psn`), sueño PROMIS (`b3b_tdr`). Bienestar subjetivo (`b3a_sw`) desde 2000.

### 7.3 Educación

| Ola | Adultos | Niños | Roster |
|---|---|---|---|
| 1993 | `buk3dl1`-`dl3` (submuestra del libro III) | `buk5dl1` (niveles cursados) | `ar16`, `ar17` |
| 1997 | `b3a_dl1` (19.910). **Nivel máximo (`dl06`, `dl07`) solo para 50+** (2.793); para menores de 50, grillas `dl2`/`dl3`, y en el panel solo lo ocurrido desde 1993 | `b5_dla1` (10.356); puntajes EBTANAS (989 los mostraron) | `ar16`, `ar17`, `ar18c` |
| 2000 | `b3a_dl1` (25.490); nivel máximo para **todos** los que asistieron (22.464) | `b5_dla1` (11.686) | Nivel y grado |
| 2007 | `b3a_dl1` (29.059); nivel máximo para todos | `b5_dla1` (13.511) | Nivel y grado |
| 2014 | `b3a_dl1` (34.464): `dl04`, `dl06` (códigos de nivel en G5 §9.3; 1.787 faltantes), `dl07` (7 = graduado; el codebook etiqueta 1-6 como «missing» por error de formato), `dl07byr` | `b5_dla1` (15.742) | Nivel y grado (no revisado en 2014) |

- En los módulos retrospectivos, quienes ya respondieron en una ola anterior solo actualizan; la historia completa requiere unir olas (G2 §4).
- Interrupciones escolares registradas en 1997 (`b3a_dlr2`, 145; `b5_dla2`, 115) (G2 §9.3).
- En 2014, 323 personas de `b3a_dl1` tienen menos de 15 años según `age_14` y 10 de `b5_dla1` tienen 15 o más (G5 §4).

### 7.4 Pruebas cognitivas (libro EK)

| Ola | Archivo(s) | Diseño | Puntaje | Cobertura |
|---|---|---|---|---|
| 1993 | — | No hay | — | — |
| 1997 | `bek` (formato largo: persona × prueba) | Matemáticas y bahasa Indonesia por nivel de edad (7-9, 10-12, 13-15, 16-24); ítems del EBTANAS, hasta 40 por prueba. Desde las primeras semanas, los de 13-24 hicieron el nivel 13-15. `ektype` sin etiquetas: **números = matemáticas, letras = bahasa** (verificado con claves en inglés para niveles 1-2 y con `res97ekm`/`res97ekb` del `ptrack` de 2000 para los cuatro) | `ekscore` (total) y `ekanswer` (texto ítem a ítem). Las claves en inglés tienen 30 ítems y no bastan para recalificar | 12.143 personas; 7.565 intentaron las dos pruebas, 4.296 ninguna |
| 2000 | `bek` (una fila por persona) | **Rediseñado**: versión 7-14 (`ek0`-`ek12` cognitivos + `ek13`-`ek17` matemáticas) y 15-24 (`ek0`-`ek6`, `ek11`, `ek12` + `ek18`-`ek22`). Ítem `ek0` adicional a lo que dice el codebook | **Sin total**: `ekNx` 1 correcto / 3 incorrecto / 9 faltante | 14.145 personas; 12.095 terminaron |
| 2007 | `bek_ek1`, `bek_ek2` | Mismo diseño que 2000, **sin `ek0`**; versión 15-24 con 8 cognitivos + 5 matemáticas | Sin total; `ekNx` | 11.202 y 11.824 personas |
| 2014 | `ek_ek1`, `ek_ek2` | Tipo 1 igual; **tipo 2 con 12 ítems cognitivos** (`ek1`-`ek12`) + `ek18`-`ek22`, y aplicado a **todas las edades de 15+**. 6.779 personas tomaron ambos (`resptype` = 2 en `ek_ek1`) | **`ekN_ans` ya calculado**, pero vale 0 también cuando no hubo respuesta | 14.943 y 36.380 personas; matemáticas faltan para los mayores de 59 |

- **1997 no es comparable ítem a ítem con 2000-2014** (instrumento distinto) (G3 §9.4).
- Entre 2000, 2007 y 2014, los ítems con el mismo número se describen como comunes; **no se verificó en los cuestionarios que sean idénticos** (G4 §9.4, G5 §9.4).
- Pesos de EK: `pwt97ekx` (1997) está en los `ptrack` de 2000 en adelante, no en el de 1997 (G2 §6.6).
- Otras medidas cognitivas de adultos (no revisadas): `b3b_co*` en 2007 y 2014 (recuerdo de palabras, fecha…) y `b3b_cob` (serie numérica adaptativa, nueva en 2014).

### 7.5 Arroz en el hogar: consumo, precio pagado y programas

| Ola | Consumo (`ks1`, última semana, Rp) | Precio pagado (`ks4`, último mes) | Programas |
|---|---|---|---|
| 1993 | `buk1ks1`: compra y producción propia (`ks03rp`); 56 duplicados `hhid93` + `item` | No revisado si `buk1ks4` incluye arroz | — |
| 1997 | `b1_ks1`, ítem A: 5.075 hogares con compra > 0, 1.511 con producción propia > 0, 193 ambas | **`b1_ks4` no incluye arroz** | — |
| 2000 | `b1_ks1` | `b1_ks4` (A): 7.359 compraron; kg 5.620, litro 1.609. **Mediana Rp 2.000/kg** (p1 970; p99 5.000) | **OPK** (arroz subsidiado): 3.403 hogares compraron arroz (`b1_ksr4`); ayudas en `b1_ksr3` |
| 2007 | `b1_ks1` | 9.554 compraron; kg 7.827, litro 1.546. **Mediana Rp 5.000/kg** (p1 1.200; p99 10.576) | **Raskin**: 5.662 hogares (`b1_ksr2`); operación de mercado 114 |
| 2014 | `b1_ks1` (A): 15.144 hogares; 7.008 con compra 0 | 10.720 compraron; kg 9.675, litro 935. **Mediana Rp 9.500/kg** (p1 1.600; p99 16.667); compras con cantidad 0 | **Raskin**: 6.692 hogares (`b1_ksr2`); mercado subsidiado de arroz 189 (`b1_ksr3`); transferencias en efectivo `b1_ksr1` |

- Precios implícitos sin limpiar, solo en kg, con atípicos extremos en todas las olas (G3 §9.5, G4 §9.5, G5 §9.5).
- Las cantidades consumidas no se registran en `ks1` (solo valores en rupias); hay cantidades solo en `ks4` para quienes compraron (G2 §9.5).
- En ninguna ola hay una variable directa de **posición neta en arroz**; los insumos disponibles son consumo comprado y propio (`ks1`), precio pagado (`ks4`, desde 2000) y módulos agrícolas (`ut*`; cosechas de arroz en `b2_ut2` de 2014) (G1 §7.3, G2 §9.5-9.6).

### 7.6 Precios comunitarios del arroz

| Ola | Fuentes | Calidades | Cobertura y unidades | Rp/kg, mediana (sin limpiar) |
|---|---|---|---|---|
| 1993 | PKK (`bukph01`, `dhtype` 1-3) y posyandu (`bkppkh01`) | alta, media, baja | **No revisado** | — |
| 1997 | PKK (`pkk_h`), posyandu (`pos_h`), tiendas y mercados (`bk2_hpj`, hasta 3 puntos, solo calidad media) | 1-3 (PKK, posyandu); media (`bk2_hpj`) | PKK 310 comunidades (kg 650, litro 165); posyandu 618 puestos en 308 (kg 1.273, litro 406); `bk2_hpj` 633 precios en kg en 265 | PKK alta 1.300, media 1.200, baja 1.000; mercado media 1.200 |
| 2000 | Posyandu (`pos_h`) y tiendas/mercados (`bk2_hpj`, formato **ancho**: tres comerciantes en columnas). **PKK sin módulo de precios** | 1-3 (posyandu); media | Posyandu 630 en 310 (kg 1.320, litro 488; `h01x` casi siempre vacío, 99998); `bk2_hpj` 685 precios en 250 | Posyandu alta 2.400, media 2.000, baja 1.800; mercado 2.000 |
| 2007 | **Tres libros nuevos**: informante (`hin_h`), mercado (`hps_h`), *warung*/tienda (`htw_h`, solo media). **Ya no hay `pos_h` ni `bk2_hpj`**; PKK sin precios | 1-3; media en `htw_h` | ≈ 311-313 códigos; en las tres, una parte en litros (≈ 200 filas en `hin_h` y `hps_h`) | Media 5.000 en las tres |
| 2014 | Mismos tres libros | 1 alta (Rojolele, Mentik), 2 media (Cisadane), 3 baja (IR64) | Mercado 224/224/217 comunidades con precio en kg; *warung* 198; informante 225/219/199. Llave `fascode` + `htype` | Mercado media 9.000; *warung* 9.000; informante media 9.000 (**incluye 999998**) |

- Hay unidades en kg, litro y «otra» en todas las fuentes revisadas; la conversión no se ha hecho (G2 §10, G3 §10, G4 §10, G5 §10).
- Los códigos 6-8 de la unidad de precio en `pkk_h` (1997) no tienen etiqueta (G2 §13). En 2007, `h03a` tiene muchos 5 y 8 sin etiquetas claras; en 2014, `h03a` mezcla variedad y disponibilidad, con códigos distintos por calidad (G4 §10, G5 §10).
- En 1997, 27 comunidades tienen el libro PKK y el libro 2 levantados en enero o febrero de 1998 (G2 §10).
- No hay precios comunitarios de 1998 ni de 1999 en la descarga pública.
- Mini-CFS de 2014 (`mkd_km5`) trae precios de alimentos para áreas fuera de las EA; no revisado (G5 §10).

### 7.7 Choques del hogar

| Ola | Archivo | Periodo | Contenido |
|---|---|---|---|
| 1993 | `buk2ge1` | 5 años | Choques económicos por tipo (`typehard`, formato largo) |
| 1997 | `b2_ge` | 5 años | 6 tipos (muerte 1.115 hogares; enfermedad 1.212; pérdida de cosecha 891; desastre 175; desempleo 335; caída de ingreso 639); 1.688 choques fechados en 1997; razón de la pérdida de cosecha («demasiado seco» en 431 de 960 menciones) |
| 2000 | `b2_ge` | **12 meses** | 8 tipos; 4.048 «sí» en 82.152 filas |
| 2007 | — | — | **No hay módulo general.** Sí hay pérdida de cosecha por causa (`b2_ut3`, 601 hogares), desastres en el área en 5 años (`b2_nd1`/`nd2`) y victimización (`b1_cr*`) |
| 2014 | `b2_nd1`, `b2_nd2` | 5 años | Desastres **y choques económicos** (muerte, enfermedad, pérdida de empleo, cosecha fallida, caída de precios, sequía…), 3.435 filas. **Códigos D y E invertidos** entre codebook (D terremoto, E erupción) y cuestionarios (D erupción, E terremoto); C y F del cuestionario no aparecen |

A nivel de comunidad, `bk1_e2` (1997 en adelante) registra eventos importantes con su año, desde 1965 en 1997 (incendios 92, inundaciones 60, sequía 28; no aclara si «incendios» incluye incendios forestales) (G2 §10); desde 2007 hay además `bk1_f*` (desastres) (G4 §5, G5 §10).

### 7.8 Otras características disponibles en varias olas

Demografía y parentesco (roster; línea de la madre en `ar11` desde 1993, con códigos 51/52 sin confirmar), vivienda (`kr`), activos del hogar y de la persona (`hr`), negocios no agrícolas (`nt`), agricultura (`ut`), ingresos no laborales (`hi`), transferencias (`ba`, `tf`), migración (`mg`), historia laboral (`tk`), embarazos y anticoncepción (libro 4), uso de servicios y seguro de salud (`rj`, `rn`, `ak`), tabaquismo (`km`), salud autorreportada y actividades de la vida diaria (`kk`). Módulos que aparecen en una sola ola o pocas: decisiones del hogar (`pk`, desde 1997), participación comunitaria (`pm`), préstamos (`bh`, 2000), preferencias de riesgo (`si`, 2007-2014), confianza (`tr`), condiciones crónicas (`cd`), salud temprana y nivel socioeconómico en la niñez (`eh`, `sa`, 2014), formulario de salida de fallecidos (`fe_*`, 2014).

**Gasto del hogar:** solo en 1993 hay un agregado ya construido (`expend2`), imputado por otro proyecto sin marcar qué hogares, y RAND no lo soporta; mediana Rp 41.542 per cápita al mes (G1 §6.6). Para las demás olas no se revisó si existe un agregado equivalente.

### 7.9 Pesos

| Ola | Hogar | Persona | Específicos |
|---|---|---|---|
| 1993 | `hhwt224`, `hhwt730` (`hhldwt`) | `rosterwt`, `respwt` (`indivwt`; `zerowt` marca elegidos por error) | `ca_wt` (antropometría) |
| 1997 | `hwt97l` (longitudinal), `hwt97x` (transversal) | `pwt97l`, `pwt97inl`, `pwt97x` | `pwt97usl`, `pwt97usx`, `pwt97ekx`: **solo en `ptrack` de 2000 en adelante** |
| 2000 | `hwt00la`/`lb`, `hwt00xa`/`xb`, `hw93700l` | `pwt00la`/`lb`, `pwt00xa`/`xb`, `p939700l` | `pw00usxa`/`xb`, `p939700u`. Versiones a y b según el modelo de desgaste; RAND no recomienda una |
| 2007 | `hwt07la`/`l_`, `hwt07xa`/`x_`, `hwt9307l` | `pwt07la`, `pw9307l`, `pw9307lr`, `pwt07xa`/`x_` | `pw9307ul`, `pw07usxa`/`usx` |
| 2014 | `hwt14xa`/`x_`, `hwt14la`/`l_`, `hwt_5_waves_l` | `pwt14xa`/`x_`, `pwt14la`, `pwt_5_waves_l`/`lr` | `pwt_5_waves_usl`, `pwt14usxa`/`usx_`, pesos de DBS |

Los `htrack`/`ptrack` de cada ola traen también los pesos de las olas anteriores. La muestra de 1993 no es autoponderada (sobremuestra urbana y de provincias pequeñas) (G1 §1, §6.5).

## 8. Problemas técnicos de lectura y codificación (resumen)

| Problema | Dónde | Detalle |
|---|---|---|
| Faltantes leídos como 1,7498 × 10¹⁰⁰ | 68 de 69 comunitarios de 1997 (formato 104) | 2.504.420 celdas; no comprobado con `haven` (G2 §6.3) |
| Enteros con faltantes leídos como texto | 201 de 230 archivos de 2000 (4.102 columnas); también `bek` de 1997 | `pandas.read_stata` los lee como números (G3 §6.3) |
| `VAR` frente a `VAR_` | 1993 | `VAR_` es el valor original sin corregir (G1 §2) |
| Faltantes por ancho; 5 válido en algunas variables | Todas | Limpiar variable por variable con el codebook (G1 §6.2) |
| Talla/peso = 0 como no medido; peso con 9996-9999 | 1993 | 188 tallas y 157 pesos con 0 (G1 §6.2) |
| Precios con 99998/99999 o 999998 | 2000 (`pos_h`), 2007, 2014 (`hin_h`) | (G3 §10, G4 §6.2, G5 §10) |
| Etiquetas de `kptype` erradas en el codebook | 2007 | Usar las del cuestionario (G4 §9.2) |
| `ndtype` D/E invertidos | 2014 | Codebook frente a cuestionario (G5 §9.6) |
| `ekN_ans` = 0 sin respuesta | 2014 | (G5 §9.4) |
| `dl07` con etiquetas «missing» en 1-6 | 2014 | Error de formato del codebook (G5 §9.3) |
| Roster y archivos de medición acumulativos | 1997-2014 | `pidlink` repetido (§3.2) |
| `htrack` acumulativo | 2014 | Llave = los seis `hhidXX` (G5 §6.1) |
| `commid97` solo en `htrack` | 1997 | Pegar antes de unir con comunitarios (G2 §6.1) |
| `ea` no está en `htrack` | 2014 | Comunitarios por EA (G5 §10) |
| Formato ancho de `bk2_hpj` | 2000 | En 1997 era largo (G3 §10) |
| Copia duplicada de archivos | 1997 (`hh97usdta/` = `bus_0`/`bus_1`); 2014 (`kec_9899000714.dta 2`) | (G2 §2, G5 §2) |

## 9. Discrepancias de la documentación de RAND (resumen)

- **1997:** el apéndice A de la guía de usuario difiere en 20 conteos de los archivos (parece una versión anterior); no hay codebook de US ni de EK; la guía dice campo hasta febrero de 1998 y los datos llegan a abril (G2 §1-2).
- **2000:** 19 conteos distintos del apéndice A; `htrack`/`ptrack` con tres cifras distintas entre apéndice, texto y archivos; fechas de campo distintas entre guía y codebooks; `ek0` no descrito (G3 §2, §9.4).
- **2007:** el apéndice A es copia del de IFLS3; dos fechas de campo distintas en la guía (2007-08 y 2008-09); cifras de seguimiento distintas de `ptrack` (G4 §2, §7).
- **2014:** conteos de HTRACK/PTRACK de la vol. 2 iguales a los de 2007; vol. 1 con otras cifras (16.204 hogares, 50.148 personas); apéndice A con nombres que no existen y sin varios archivos; conteos EK de la guía (66.283 y 87.725) distintos de los archivos (14.943 y 36.380); formato declarado Stata 8 y real 111; `result14` con códigos distintos entre codebook y guía; `schl` con 2.668 filas frente a 2.567 en el codebook (G5 §1-2, §7, §9.4).
- **Todas:** etiquetas de valores casi ausentes en los `.dta`.

## 10. Lo que no traen los datos

- **IFLS2+ (1998)**: no está en la descarga pública.
- **Ítems de salud mental en 1997**: no hay. En 1993 solo cubren la submuestra del libro III y no hay ítems en los libros proxy de ninguna ola.
- **Escala de salud mental común a todas las olas**: no hay; 3 ítems comunes entre 1993 y 2000, y CES-D-10 en 2007 y 2014 con estructuras de respuesta distintas.
- **Pruebas cognitivas en 1993**: no hay. Las de 1997 no son comparables con las de 2000-2014. En 2000 y 2007 no hay puntaje total.
- **Precio del arroz pagado por el hogar en 1997**: `b1_ks4` no incluye arroz.
- **Precio PKK en 2000**: el libro PKK de 2000 no tiene módulo de precios. **Posyandu y `bk2_hpj` en 2007-2014**: ya no existen.
- **Precios comunitarios de 1998 y 1999**.
- **Módulo general de choques del hogar en 2007**.
- **Archivos del libro proxy en 2014**, aunque el cuestionario existe.
- **`commid97` para hogares fuera de comunidades IFLS** (894 hogares en 1997).
- **EA en el `htrack` de 2014**; **fecha de nacimiento en `bus_us` de 2014**; **año en `bk_cov` de 2000**.
- **Codebooks de US y EK de 1997**; **etiquetas de `ektype` en 1997**.
- **Posición neta en arroz** como variable directa, en ninguna ola.
- **`b3p_tk4` de 1997** (primer empleo por proxy): falta en la descarga.

## 11. Preguntas abiertas (consolidadas de las cinco guías, sin recomendación)

Cada una reúne las «Preguntas abiertas» de las guías (G1 §10, G2-G5 §12). Este documento no toma posición.

1. **Unidad de comunidad:** `commid` (312/311) o EA (321/320); EA gemelas de 1993 y las 9 comunidades con dos filas o dos EA en 2007 y 2014; cómo unir hogares con comunitarios de 2014 si `htrack` no trae `ea`.
2. **Comunidad de quienes se mudaron:** `commid97` faltante (894), `commid` con letras (2000-2014) y unión con el mini-CFS por `mkid`.
3. **Precio del arroz:** qué fuente por ola (PKK, posyandu, mercado, *warung*, informante, hogares), calidad, conversión de unidades, atípicos y códigos 99998/999998; cambio de fuentes entre olas; comunidades encuestadas en 1998; desfase entre hogar y comunidad en 2014-15.
4. **Entrevistas de 1998** en IFLS2: 627 hogares, 27 comunidades, mediciones y pruebas EK de 1998.
5. **Edad:** fuentes por ola (antropometría, roster, `ptrack`), edad en meses para HAZ, edades incoherentes entre olas.
6. **Antropometría:** códigos de no medido por ola, valores extremos, `us00` sin documentar.
7. **Salud mental:** si se usa, qué ítems, qué escala; derivados de 1993 ya construidos; submuestra y proxy de 1993; CES-D 2007 frente a 2014.
8. **Educación:** cómo armar el nivel máximo en 1997 (solo 50+ en `dl1`), en el panel (solo actualizaciones) y en 2014 (`dl06`, `dl07`).
9. **Pruebas cognitivas:** cómo puntuar en cada ola; nivel 4 y edades fuera de rango en 1997; `ek0` en 2000; `_ans` en 2014; quién tomó qué versión en cada cohorte.
10. **Posición neta en arroz:** si se construye y con qué módulos.
11. **Choques:** comparabilidad de los módulos (5 años, 12 meses, ausencia en 2007, ND ampliado en 2014).
12. **Programas de arroz subsidiado** (OPK, Raskin): si se usan y cómo.
13. **Pesos:** con o sin pesos; transversales, longitudinales, de panel; versión a/b o con/sin ajuste por desgaste.
14. **Indicadores de entrevista y de resultado:** `result07` frente a `res07bk`; códigos de `result14`.
15. **Roster:** qué códigos de `ar01a` quitar en cada ola para que `pidlink` sea único.
16. **Proxy:** cómo tratar los libros proxy (1997-2007) y su ausencia en 2014.
17. **Gasto del hogar:** `expend2` de 1993 (imputado sin marca) o agregados propios.

## 12. Qué no está verificado

- **Este documento no se cotejó contra los `.dta`**: todas las cifras se copiaron de las guías de ola. Si una cifra de aquí y una guía difieren, manda la guía.
- Lo que cada guía marca como no verificado sigue sin verificar. Entre lo más transversal:
  - la consistencia entre fuentes de edad en todas las olas;
  - que los ítems EK con el mismo número sean idénticos entre 2000, 2007 y 2014;
  - que las 9 comunidades con dos filas (2007) o dos EA (2014) correspondan a las EA gemelas de 1993;
  - los precios comunitarios de 1993 (descargados, no revisados);
  - la conversión de unidades de precio (kg/litro) y los atípicos de todas las olas;
  - los montos en rupias (atípicos de factor 1.000) fuera de 1993;
  - las llaves de los archivos marcados «no determinada» en cada guía;
  - si `haven::read_dta()` lee bien los comunitarios de 1997;
  - si los datos de `ndtype` de 2014 siguen al codebook o al cuestionario;
  - los códigos 51/52 de `ar10`/`ar11` de 1993, 6 y 98 de `mover07`, `9999`, `1227`, `5115` y `3249` de comunidad;
  - los módulos marcados «no revisado» en cada guía.
- La guía de IFLS5 (`IFLS5/00_guia_IFLS5.md`, §5) tiene el marcador `<<CATALOGO>>` sin reemplazar: el catálogo de archivos de esa ola está en `IFLS5/_revision/_cat.md` y no se insertó en la guía. Las llaves de IFLS5 citadas aquí salen del resto de la guía.
