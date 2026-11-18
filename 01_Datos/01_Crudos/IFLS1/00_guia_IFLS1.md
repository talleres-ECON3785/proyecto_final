# IFLS1 (1993) · Catálogo, contenido y manejo de los datos

*Guía de la ronda 1 para el proyecto final de Ciencia de Datos. Escrita el 10-nov-2026 a partir de la documentación de RAND en `01_Datos/01_Crudos/IFLS1/Documentation` y de una revisión directa de los 109 archivos `.dta` de `01_Datos/01_Crudos/IFLS1/Household Data`. Los conteos y las pruebas de llaves de esta guía salen de los archivos; lo demás, de la documentación citada.*

*Versión 2 (12-nov-2026): se reescribió para que sea **descriptiva**. La guía documenta qué hay en la ola, cómo está codificado y qué problemas tiene; **no** decide qué variables serán resultado, control o muestra. Esas decisiones se toman cuando estén revisadas todas las olas. La versión 1 está en `_obsoleto/`.*

## 1. Qué es esta ronda

- **IFLS1, también llamada SAKERTI 93.** Trabajo de campo de **agosto de 1993 a enero de 1994** (mes de la primera visita en `bukksc1`: 159 hogares en agosto, 640 en septiembre, 1.598 en octubre, 2.026 en noviembre, 2.257 en diciembre y 881 en enero).
- **Muestra:** 13 provincias (≈ 83 % de la población), 321 áreas de enumeración (EA) que corresponden a **312 comunidades** (`commid93`). 7.730 hogares en la muestra del libro K, **7.224 con roster** y 33.081 personas en el roster.
- **Diseño:** sobremuestra urbana y de provincias pequeñas, por lo que la muestra no es autoponderada (ver §6.5).
- **Ubicación en el tiempo:** es la primera ola del panel, unos cuatro años antes de la crisis de 1997-98. Contiene, entre otros, módulos de hogar, consumo, activos, educación, salud de adultos (incluidos síntomas de malestar psicológico), antropometría y precios comunitarios (§7-§8).

## 2. Qué versión tienes: IFLS1-RR

Los archivos son el **IFLS1-RR** (*revised and restructured*), la reedición del año 2000 preparada para enlazar con IFLS2. Se reconoce porque todos tienen `hhid93`, `pid93`, `pidlink` y `commid93`, y porque traen variables con sufijo `_`.

Diferencias con el IFLS1 original de 1995 que importan al trabajar:

1. **Correcciones incorporadas.** Los archivos `.fix` ya están aplicados. El valor original se conserva en `VAR_` (p. ej., `ca06yr_`, `ar09yr_`). Las observaciones con `VAR != VAR_` son las corregidas; `VAR` es el valor corregido por RAND.
2. **Archivos fusionados.** Doce pares de subarchivos con la misma unidad se unieron. Por ejemplo, `bukcca2` ya trae la talla y el peso del antiguo `bukcca3`, y `bukkar2` ya trae la educación del antiguo `bukkar3`. Si un codebook menciona `bukcca3`, `bukkar3`, `buk1ksa`, `buk3t2b`, `buk3tk4`, `buk3ba2`, `buk3ba6`, `buk3baa`, `buk3tf2`, `buk3tf4`, `buk4ch2`, `buk4ch3` o `buk4kl3`, sus variables están en el archivo «padre».
3. **Nombres de variables iguales a los del codebook original**, salvo los ingresos laborales de `buk3tk2`, que quedan en mensuales (`tk25a_m`) y anuales (`tk25a_y`). El cuadro 3.2 de `iflsrr1.pdf` tiene la lista completa.
4. **Stata versión 6**: `haven::read_dta()` lo lee sin problema. Las etiquetas de valores casi no vienen en los `.dta`, así que los códigos hay que mirarlos en el codebook.

## 3. Mapa de la documentación

| Archivo en `Documentation/` | Qué es | Cuándo usarlo |
|---|---|---|
| `iflsrr1.pdf` (DRU-1195/7) | Documentación del IFLS1-RR: correcciones, fusiones, identificadores nuevos, enlace con IFLS2. El apéndice A lista los archivos y el B los mapea a IFLS2. | **Leer primero.** Es lo único que describe la versión que tienes. |
| `DRU1195_6.pdf` (DRU-1195/6) | Guía de usuario: estructura de archivos y cómo identificar madres, padres, cónyuges e hijos y enlazar libros. | Al construir el archivo de análisis. |
| `DRU1195_1.pdf` (DRU-1195/1) | Visión general e informe de campo: muestreo, tasas de respuesta, contenido de cada libro, pesos. | Para la sección de datos del informe. |
| `DRU1195_4/` (DRU-1195/4, apéndice C) | **Codebook del hogar**: un PDF por libro (`Book1` … `Book5`, `BookK`, `CA`) más la introducción (`intro`) y apéndices. | Para cada variable: códigos, rangos y notas sobre anomalías. |
| `DRU1195_2/` (apéndice A) | Cuestionarios del hogar en inglés y manual del entrevistador. | Para ver la redacción exacta y los saltos. |
| `DRU1195_3/` (apéndice B) | Cuestionarios comunitarios y de establecimientos. | Solo si se descargan los datos comunitarios (ver §8). |
| `DRU1195_5/` (apéndice D) | Codebook comunitario y de establecimientos. | Igual. |

## 4. Estructura de la encuesta: libros y quién responde

| Libro | Quién responde | Unidad | N |
|---|---|---|---:|
| K · Control | Entrevistador e informante | Hogar (muestra completa) | 7.730 |
| K · Roster (`bukkar2`) | Informante del hogar | Persona | 33.081 |
| I · Hogar | Informante del hogar | Hogar | 7.216 |
| II · Economía del hogar | Informante del hogar | Hogar | 7.185 |
| III · Adultos | **Solo una submuestra de adultos** (ver abajo) | Persona | 14.418 |
| IV · Mujeres | Todas las mujeres alguna vez casadas de 15 a 49 años | Persona | 4.981 |
| V · Niños | Madre o cuidadora, **por proxy**, para hasta dos hijos menores de 15 del jefe o su cónyuge | Persona | 7.751 |
| CA · Antropometría | Medición directa a todos los miembros presentes | Persona | 24.515 (en 7.164 hogares) |

**Selección dentro del hogar (libro III):** se entrevista al jefe y su cónyuge; a una persona de 50 años o más elegida al azar y su cónyuge; y, **solo en uno de cada cuatro hogares**, a una persona de 15 a 49 elegida al azar y su cónyuge. Por eso los módulos del libro III (incluidos los síntomas de la sección KK) **no cubren a todos los adultos**: sobrerrepresentan a jefes, cónyuges y mayores. El grupo de muestreo de cada persona está en `indivwt$smpgrp` (1 = jefe o cónyuge, 2 = 50+, 3 = 15-49, 4 = niños).

## 5. Catálogo de archivos

Las 108 tablas de hogar coinciden una a una con el cuadro A.1 de `iflsrr1.pdf`, con el mismo número de registros. En `Household Data` no hay archivos comunitarios ni de establecimientos; los comunitarios están en `Community Data` (§8). La descripción es la etiqueta oficial de RAND. «Llave adicional» es lo que identifica la fila, además del hogar o la persona.

**Libro K (control, muestreo)**

| Archivo | Contenido | Unidad | Llave adicional | N |
|---|---|---|---|---:|
| `bukkar1` | Book I Cover Page | hogar | — | 7.224 |
| `bukkar2` | HH Roster (AR01-AR22) | miembro del hogar | `ar001a` | 33.081 |
| `bukkfp1` | Survey Disposition (FP1-FP9) | hogar | — | 7.730 |
| `bukkpsk` | Respondent Selection | hogar | — | 33.157 |
| `bukksc1` | Visit Record (IK1-IK2, SC01-SC20) | hogar | — | 7.730 |

**Libro I (hogar: roster, características, consumo)**

| Archivo | Contenido | Unidad | Llave adicional | N |
|---|---|---|---|---:|
| `buk1cp1` | Interview Evalualtion (CPI1-CPI3) | hogar | — | 7.216 |
| `buk1kr1` | Household Characteristics (KR02-KR22) | hogar | — | 7.216 |
| `buk1ks1` | Food Item Consumption & Own Production (KS01-KS03) | ítem de alimento | `item` | 106.090 |
| `buk1ks2a` | Transfer of Food Items (KS04-KS05) | hogar | — | 7.216 |
| `buk1ks2b` | Non-food Items in Past Month (KS06-KS07) | ítem no alimentario | `nf_item1` | 50.512 |
| `buk1ks3a` | Non-food Items in Past Year (KS08-KS09) | ítem no alimentario | `nf_item2` | 43.296 |
| `buk1ks3b` | Education Expenditures (KS10-KS12) | hogar | — | 7.216 |
| `buk1ks4` | Purchases in Last Month (KS13-KS15) | tipo de compra | `item_m` | 108.240 |
| `buk1pp1` | Health Provider Knowledge (PP1-PP7) | establecimiento | `factype` | 50.512 |

**Libro II (economía del hogar)**

| Archivo | Contenido | Unidad | Llave adicional | N |
|---|---|---|---|---:|
| `buk2ak1` | Employer-provided Health Insurance: Who is covered | persona cubierta | `ak04` | 9.072 |
| `buk2ak2` | Employer-provided Health Insurance: Companies | empresa | `ak06` | 1.000 |
| `buk2ak3` | Individual Health Insurance: Who is covered (AK12-AK16) | persona cubierta | `ak15` | 7.256 |
| `buk2ak4` | Individual Health Insurance: Companies (AK17-AK21) | empresa | `ak17` | 77 |
| `buk2ak5` | Employer-provided Medical Benefits: Who is covered | persona cubierta | `ak25` | 7.863 |
| `buk2ak6` | Employer-provided Medical Benefits: Type of Benefit | beneficio | `ak27` | 524 |
| `buk2ak7` | Care at Company Clinic: Who is covered (AK33-AK37) | persona cubierta | `ak36` | 7.991 |
| `buk2ak8` | Care at Company Clinic: Clinics (AK38-AK43) | clínica | `ak38` | 524 |
| `buk2cp2` | Interview Evaluation (CPII1-CPII3) | hogar | — | 7.184 |
| `buk2ge1` | Economic Hardships (GE01-GE04) | tipo de choque | `typehard` | 43.110 |
| `buk2hr1` | Household Assets (HR01-HR12) | activo | `assettyp` | 79.035 |
| `buk2hr2` | Household Data (HR13-HR15) | hogar | — | 7.185 |
| `buk2nt1` | Non-Farm Business (NT01-NT09) | hogar | — | 7.185 |
| `buk2nt2` | Non-Farm Business Assets (NT10-NT14) | activo | `nfrmasst` | 22.005 |
| `buk2ph1` | Individual Income (PH01-PH07) | miembro del hogar | `ph00` | 10.211 |
| `buk2ph2` | Other Income Sources (PH08-PH11) | fuente de ingreso | `incsourc` | 43.110 |
| `buk2ut1` | Book II Cover. Farm Business (UT01-UT09) | hogar | — | 7.185 |
| `buk2ut2` | Farm Business Assets (UT10-UT14) | activo | `farmasst` | 25.272 |

**Libro III (adultos)**

| Archivo | Contenido | Unidad | Llave adicional | N |
|---|---|---|---|---:|
| `buk3aw1` | Time Allocation (AW1-AW3) | respondiente | — | 14.418 |
| `buk3ba1` | Noncoresident Parents (BA01-BA26) | padre/madre | `parent` | 25.970 |
| `buk3ba3` | Non-Householders: Siblings (BA28-BA29) | respondiente | — | 12.459 |
| `buk3ba4` | Noncoresident Sibling Roster (BA30A-BA30G, BA33B, BA34-BA51) | hermano | `ba30a` | 44.995 |
| `buk3ba5` | Sibling Summary Counts (BA30H. BA31-BA32) | respondiente | — | 11.241 |
| `buk3ba7a` | Help from/to Siblings Not Mentioned (BA53-BA57) | respondiente | — | 12.459 |
| `buk3ba7b` | Trigger Questions: Non-coresident children BA58-BA63) | respondiente | — | 12.459 |
| `buk3ba8` | Noncoresident Children Roster (BA63A-BA71. BA74-BA90) | hijo | `ba63a` | 10.100 |
| `buk3ba9` | Non-CoResid Kids Age 15+-Counts (BA72-BA73) | respondiente | — | 3.776 |
| `buk3bab` | Help From/To Non-cores. Kids Not Selected (BA92-BA96) | respondiente | — | 3.432 |
| `buk3br1` | Pregnancy Summary (BR01-BR16) | mujer sin libro IV | — | 2.664 |
| `buk3cp3` | Interview Evaluation (CP1-CP3) | respondiente | — | 14.405 |
| `buk3dl1` | Education Summary (DL01-DL07) | respondiente | — | 14.418 |
| `buk3dl2` | Levels of Schooling (DL08-DL15) | nivel escolar | `dl08` | 13.355 |
| `buk3dl3` | Last School Attended (DL17-DL31) | respondiente | — | 7.778 |
| `buk3hi1` | Individual Assets (HI01-HI13) | tipo de activo | `assettyp` | 73.993 |
| `buk3hi2` | Other Income In Past Year (HI14) | tipo de ingreso | `incomtyp` | 30.570 |
| `buk3kk1` | Current Health & Activities of Daily Living (KK01-KK04) | respondiente | — | 12.985 |
| `buk3kk2` | Health Conditions During Past 4 Weeks (KK05-KK07) | respondiente | — | 12.985 |
| `buk3km1` | Smoking Habits (KM01-KM09) | respondiente | — | 14.406 |
| `buk3kw1` | Marriage Summary (KW01-KW08) | respondiente | — | 14.418 |
| `buk3kw2` | Marital History (KW09-KW22) | matrimonio | `marrnum` | 10.516 |
| `buk3kw3` | Husband's Desire For More Kids (KW23-KW27) | hombre casado | — | 7.572 |
| `buk3ma1` | Acute Morbidity (MA01-MA03) | síntoma | `symptom` | 172.872 |
| `buk3mg1` | Migration History:Birth, Age 12, 1st Marr (MG01-MG21) | respondiente | — | 12.996 |
| `buk3mg2` | Migration History (MG21-MG40) | mudanza | `movenum` | 15.376 |
| `buk3mg3` | Last Move to Current Residence (MG41-MG52) | respondiente | — | 6.945 |
| `buk3ps1` | Self-Treatment (PS01-PS02) | respondiente | — | 12.989 |
| `buk3rj1` | Outpatient Medical Facilities (RJ01-RJ04) | respondiente | — | 14.406 |
| `buk3rj2` | Outpatient Visits (RJ05-RJ24) | visita | `rj05` | 4.685 |
| `buk3rn1` | Inpatient Medical Facilities (RN01-RN04) | respondiente | — | 14.406 |
| `buk3rn2` | Inpatient Visits (RN05-RN20) | visita | `rn05` | 410 |
| `buk3s3a` | Book III Cover Page | respondiente | — | 14.418 |
| `buk3sr1` | Circular Migration: Trigger Questions (SR01-SR02) | respondiente | — | 14.418 |
| `buk3sr2` | Circular Migration History (SR03-SR18) | migración circular | `tripnum` | 1.788 |
| `buk3tf1` | Transfers To/From: Parents, Sibs, Children (TF01-TF05) | tipo de transferente | `reltype` | 38.955 |
| `buk3tf3` | Transfers To/From: Relatives, Friends, Employer, Org. (TF06-TF09) | tipo de transferente | `whohelp` | 51.940 |
| `buk3tk1` | Work Experience (TK01-TK17) | respondiente | — | 14.418 |
| `buk3tk2` | Current Job (Primary & Secondary) (TK18-TK27, monthly & annual earnings) | respondiente | — | 9.762 |
| `buk3tk3` | Primary & Secondary Jobs During Past 5 Years (TK28-TK46) | año (1988-92) | `year` | 52.934 |
| `buk3tk5` | Employment History: 1st, 1983, 1973 job (TK47-TK59) | momento laboral | `jobrec` | 19.551 |

**Libro IV (mujeres alguna vez casadas 15-49)**

| Archivo | Contenido | Unidad | Llave adicional | N |
|---|---|---|---|---:|
| `buk4br1` | Pregnancy Summary (BR1-BR16) | respondiente | — | 4.980 |
| `buk4ch1` | Pregnancy Roster (CH01-CH54) | embarazo | `prgid` | 17.962 |
| `buk4cp4` | Interview Evaluation (CP1-CP3) | respondiente | — | 4.981 |
| `buk4cx1` | Contraceptive Knowledge/Use: Efficient (CX1-CX11) | método | `method` | 39.120 |
| `buk4cx2` | Contraceptive Knowledge/Use: Less efficient (CX12-CX13) | método | `method` | 24.450 |
| `buk4cx3` | Contraceptive Use (CX14-CX29) | persona | — | 4.890 |
| `buk4kl1` | Cont. Calender: Marriage/calendar start/end dates | matrimonio | — | 4.966 |
| `buk4kl2` | Cont. Calendar (1/84-12/88) (KAL)(1/89-2/94) (KAL1) | tipo de evento | `event` | 44.007 |
| `buk4kl4a` | Cont. Facility Visit Cost, last 30 months of calendar | mes | `evntmth` | 16.353 |
| `buk4kl4b` | Cont. Facility Info (KL1-KL6) | respondiente | — | 4.890 |
| `buk4kw1` | Marriage Summary (KW01-KW03) | respondiente | — | 4.981 |
| `buk4kw2` | Marital History (KW04-KW17) | matrimonio | `marrnum` | 5.776 |
| `buk4kw3` | Menstrual History/Desire for Kids (KW18-KW25) | respondiente | — | 4.889 |
| `buk4siv` | Book IV Cover | respondiente | — | 4.981 |

**Libro V (niños <15, por proxy)**

| Archivo | Contenido | Unidad | Llave adicional | N |
|---|---|---|---|---:|
| `buk5cp5` | Interview Evaluation (CP5A-CP5C) | respondiente | — | 7.751 |
| `buk5dl1` | Levels of Schooling (DLA01-DLA22) | nivel cursado | `dla05` | 8.563 |
| `buk5dl2` | School Expenses (DLA24-DLA25) | respondiente | — | 4.668 |
| `buk5ma1` | Acute Morbidity (MAA01-MAA03) | síntoma | `symptom` | 116.265 |
| `buk5psa` | Self-Treatment (PSA01-PSA02) | respondiente | — | 7.751 |
| `buk5rj1` | Outpatient Medical Facilities (RJA01-RJA04) | respondiente | — | 7.751 |
| `buk5rj2` | Outpatient Visits (RJA05-RJA24) | visita | `rja05` | 2.259 |
| `buk5rn1` | Inpatient Medical Facilities (RNA01-RNA04) | respondiente | — | 7.751 |
| `buk5rn2` | Inpatient Visits (RNA05-RNA20) | visita | `rna05` | 100 |
| `buk5se5` | Book V Cover Page | respondiente | — | 7.751 |

**Libro CA (antropometría)**

| Archivo | Contenido | Unidad | Llave adicional | N |
|---|---|---|---|---:|
| `bukcca1` | Cover Page- Anthropometry | hogar | — | 7.164 |
| `bukcca2` | Anthropometry Roster (CA01-CA15) | persona | `line_ca` | 24.515 |

**Archivos auxiliares**

| Archivo | Contenido | N |
|---|---|---:|
| `hhldwt` | Pesos de hogar (`hhwt730`. `hhwt224`) | 7.730 |
| `indivwt` | Pesos individuales (respondiente. roster. antropometría) y edad imputada | 33.081 |
| `expend2` | Gasto mensual del hogar nominal y real. total y per cápita (RAND no lo soporta) | 7.216 |
| `priceidx` | Índice de precios de alimentos 1993 por provincia y urbano/rural (Jakarta = 1) | 27 |
| `ba_chkid` | Cruce entre hijos no corresidentes (BUK3BA8) y su registro de embarazo (BUK4CH1) | 1.730 |
| `othtrans` | Traducción al inglés de las respuestas "Otro. especifique" | 96.497 |
| `prov` | Códigos y nombres de provincia | 27 |
| `kab` | Códigos y nombres de kabupaten (regencia/municipio) | 301 |
| `kec` | Códigos y nombres de kecamatan (subdistrito) | 3.809 |
| `rnd2_eas` | 32 áreas de enumeración entrevistadas antes del reentrenamiento de la 2.ª ronda de campo | 32 |
## 6. Cómo manejar los datos

### 6.1 Identificadores (todos verificados en los archivos)

| Variable | Tipo | Qué es | Uso |
|---|---|---|---|
| `hhid93` | texto, 7 | EA (3) + número de hogar (2) + `"00"`. P. ej., `"0010600"` | Llave de hogar. Enlaza con `hhid97` de IFLS2 (hogares de origen). |
| `pid93` | número | Línea de la persona en el roster de 1993 (= `person`) | Junto con `hhid93` |
| `pidlink` | texto, 9 | `hhid93` + `pid93` con dos dígitos. P. ej., `"001060001"` | Llave de persona, constante en todas las olas; identifica a la persona sin necesidad del hogar. |
| `commid93` | texto, 4 | Comunidad (provincia + kabupaten…). P. ej., `"1202"` | Llave de comunidad. Hay 312 valores. |
| `case`, `hhid` | número / texto, 9 | Identificador original: prov(2)+kab(2)+EA(3)+hogar(2) | Solo para cruzar con documentación vieja |
| `person`, `pid` | número | = `pid93` | Ídem |
| `fcode` | texto, 7 | Establecimiento (escuela, puskesmas…). El quinto dígito es el tipo. | Enlace con datos de establecimientos |

Unicidad comprobada:

- `bukkar2`, `indivwt`, `buk3s3a` y `buk3kk2`: `pidlink` es único.
- `bukksc1`, `bukkar1` y `buk1kr1`: `hhid93` es único.
- `buk3tk3`: `pidlink` + `year` es único. `buk4ch1`: `pidlink` + `prgid` es único.
- `bukcca2`: `pidlink` **no** es único. Hay 4 filas con `person = 96`: personas medidas que no estaban en el roster, sin `pidlink` propio. Una unión por `pidlink` las duplica si no se tratan antes.
- `buk1ks1`: `hhid93` + `item` **no** es único. Hay 56 filas duplicadas, en general con valores de compra distintos (no son copias exactas). Hay que resolverlas (p. ej., sumar o investigar) antes de pivotar a una fila por hogar.

**Trampas de los identificadores:**

- `hhid93`, `pidlink` y `commid93` son **texto con ceros a la izquierda**. Nunca los conviertas a número: `"0010600"` y `"10600"` no se unen.
- **EA (`sc07`) y comunidad no son lo mismo.** Hay 321 EA y 312 `commid93`: 9 pares de EA «gemelas» en el mismo pueblo comparten `commid93` (75-76, 80-81, 82-83, 103-104, 139-140, 188-189, 198-199, 204-205, 212-213).
- **Ubicación de 1993:** está en `bukksc1` (`sc01` provincia, `sc02` kabupaten, `sc03` kecamatan, `sc05` urbano/rural), donde RAND corrigió los códigos de 15 EA. El historial de migración (`buk3mg2`) también trae lugares, pero sin esa corrección.

### 6.2 Códigos especiales (cuadro 1.6 del codebook)

Los faltantes **no vienen como `NA`**. Son valores numéricos que dependen del ancho de la variable:

| Ancho | Fuera de rango | No aplica | Rechazó | No sabe | Faltante |
|---|---:|---:|---:|---:|---:|
| 1 dígito | 5 | 6 | 7 | 8 | 9 |
| 2 dígitos | 95 | 96 | 97 | 98 | 99 |
| 3 dígitos | 995 | 996 | 997 | 998 | 999 |
| decimal 5.1 (p. ej., talla) | 999,5 | 999,6 | 999,7 | 999,8 | 999,9 |
| texto | V | W | X | Y | Z |

**Ojo:** en variables de un dígito, **5 puede ser una respuesta válida**. Por ejemplo, `kk05_*`: 1 = a menudo, 3 = a veces, **5 = nunca**. Hay que limpiar **variable por variable** mirando el rango válido del codebook, nunca con una regla global del tipo «≥ 5 → NA».

Convenciones de respuesta de la IFLS:

- **Sí / no = 1 / 3** (no 1/0 ni 1/2).
- **Sexo = 1 hombre / 3 mujer**. En `bukkar2`: 16.077 hombres, 17.002 mujeres, 2 inválidos.
- **Años con dos dígitos**: `93` = 1993. Fechas de medición con `ca09yr` = 94 son de enero de 1994. Valores 96-99 en años o meses son códigos de faltante, no años.
- Hay casos con **0 = no medido**: 188 tallas en `ca10` y 157 pesos en `ca13`.
- **El peso no sigue la regla del ancho:** `ca13` usa 9996-9999 como faltantes (1.983 casos), más 4 casos con 999,9.

### 6.3 Rupias

- Ya vienen convertidas a número, en rupias **nominales de 1993**. Para comparar con 1997-2000 hay que deflactar (la inflación de 1998 fue muy alta).
- Algunos montos se pidieron **en miles de rupias** (gastos de educación en los libros III y V, empleo y transferencias del libro III), y a veces el entrevistador anotó el monto completo. Hay que **revisar atípicos de un factor 1.000**.
- Las variables `...r1`, `...rp` son los montos numéricos; las letras (`a`, `b`) son indicadores de cómo se respondió (monto exacto, rango, no sabe).

### 6.4 Formato largo vs. ancho

Muchos archivos tienen **varias filas por hogar o persona**: ítems de consumo (`buk1ks1`), activos (`buk2hr1`), choques (`buk2ge1`), síntomas (`buk3ma1`), embarazos (`buk4ch1`), años de empleo (`buk3tk3`). Antes de unirlos a la base de personas hay que **resumirlos o pivotarlos a una fila por llave**, o la unión multiplica observaciones.

### 6.5 Pesos

- **`hhldwt`**: `hhwt224` es el peso de los 7.224 hogares con roster y `hhwt730` el de los 7.730 de la muestra K. Corrigen la sobremuestra urbana y de provincias pequeñas.
- **`indivwt`**: `rosterwt` para personas del roster; `respwt` para respondientes de los libros III/IV/V (incluye el ¼ de hogares con respondiente de 15-49); `ca_wt` para antropometría. `zerowt` marca a los respondientes elegidos por error (peso 0). `impage` es la edad con imputación y `ageimp` la marca de imputación.
- Según la documentación, los pesos de 1993 son de corte transversal para 1993. Las olas posteriores traen sus propios pesos (los longitudinales de IFLS3 se revisan en esa ronda).

### 6.6 Gasto del hogar (`expend2`)

Trae el gasto mensual total y per cápita, nominal y real (`exppc_r`, deflactado con `priceidx`, Jakarta = 1), y quintiles. **RAND no lo soporta**: lo armó otro proyecto, y cuando un hogar declaró una compra sin valor imputó la **mediana de la EA o del kabupaten** según tamaño del hogar. El archivo **no marca** qué hogares tuvieron imputación. La mediana del gasto nominal per cápita es Rp 41.542 al mes. Hay 12 hogares sin valor, 3 con gasto 0 y 1 máximo de Rp 4,4 millones que conviene revisar.

## 7. Contenido por tema

### 7.1 Antropometría (`bukcca2`)

- **Variables:** `ca10` talla en cm, con un decimal; `ca11` método (de pie o acostado); `ca12` motivo de no medición; `ca13` peso en kg.
- **Edad y fecha de nacimiento:** `ca06yr` y `ca06mth` dan la edad; `ca07day`/`mth`/`yr` la fecha de nacimiento; `ca08` la fuente de esa información; `ca09*` la fecha de medición.
- **Cobertura:** de 24.515 personas, 22.284 tienen talla (sin contar los códigos 999,x); 188 tienen 0 (no medido) y 2.231 un código 999,x.
- **Niños menores de 5 en 1993:** 3.230 personas, de las cuales 2.670 tienen talla válida. **185 no tienen año de nacimiento** (`ca07yr` = 98) y 342 no tienen el mes. La puntuación HAZ (OMS) requiere la edad en meses; las fuentes disponibles son la fecha de nacimiento (`ca07*`) con la de medición (`ca09*`), la edad declarada (`ca06yr`, `ca06mth`) y la edad del roster. Cómo combinarlas queda abierto (§10).
- **Solapamiento con cohortes posteriores:** de los niños que tendrían 0-5 años en 1997 (nacidos en 1992-97), solo los nacidos en 1992-93 pueden aparecer medidos en 1993 (unos 1.100 tienen año de nacimiento 92 o 93). Los menores de 5 en 1993 son, en su mayoría, una cohorte distinta de la de 0-5 en 1997.
- El codebook advierte errores de transcripción de la fecha y la edad desde el roster, en parte corregidos (variables `_`). La consistencia entre `ca06yr` y la edad del roster (`bukkar2$ar09yr`) **no se ha revisado**.

### 7.2 Síntomas de salud de adultos (`buk3kk2`)

En 1993 **no hay un GHQ** como tal. Hay **6 síntomas** de las últimas 4 semanas en la sección KK del libro III: `kk05_a` insomnio, `kk05_b` fatiga, `kk05_c` irritabilidad, `kk05_d` dolores corporales, `kk05_e` tristeza, `kk05_f` ansiedad. Son los ítems que usan Friedman y Thomas (2009). (`02_datos` y `05_salud_mental.md` los describen como «GHQ»; está en pendientes corregirlos.)

- **Escala:** 1 = a menudo, 3 = a veces, 5 = nunca. Faltantes: 6 = no aplica, 8 = no sabe, 9 = faltante (entre 5 y 20 casos por ítem).
- **Frecuencias** (12.985 respondientes):

| Ítem | A menudo | A veces | Nunca |
|---|---:|---:|---:|
| Insomnio | 889 | 2.007 | 10.075 |
| Fatiga | 1.162 | 2.521 | 9.284 |
| Irritabilidad | 647 | 1.427 | 10.897 |
| Dolores | 802 | 1.881 | 10.281 |
| Tristeza | 579 | 1.411 | 10.983 |
| Ansiedad | 222 | 719 | 12.031 |

- La distribución está muy concentrada en «nunca» (entre 70 % y 93 % según el ítem). Para cada ítem hay además cuándo fue el último episodio (`kk06*`) y cuántos días sin síntomas (`kk07*`).
- **Cobertura:** 12.985 de los 14.418 respondientes del libro III. La diferencia es casi exactamente la de los respondientes con proxy: de 1.386 entrevistas con proxy, solo 5 tienen KK, frente a 12.980 de 13.032 sin proxy.
- **Otros indicadores de salud en el mismo libro:**
  - `buk3kk1`: salud autorreportada (`kk01`) y 9 actividades de la vida diaria (`kk03_a`-`i`).
  - `buk3ma1`: morbilidad aguda por síntoma (formato largo).
  - `buk3km1`: tabaquismo.
- **Comparabilidad con 2000 (IFLS3, `b3b_kk`), verificada:** en 2000 hay 8 ítems con la misma escala 1/3/5 (`kk04`-`kk11`). **Solo 3 coinciden con 1993:**
  - insomnio (`kk05_a` ↔ `kk04`);
  - tristeza (`kk05_e` ↔ `kk07`);
  - ansiedad o miedo (`kk05_f` ↔ `kk08`).

  Fatiga, irritabilidad y dolores existen solo en 1993. Molestia por cosas, soledad, concentración, tareas y memoria existen solo en 2000.
- **Cambio de formato:** en 1993 los ítems iban en una grilla de síntomas, junto a «dolores» y «fatiga»; en 2000 son preguntas sueltas. La prevalencia sube mucho (tristeza «a menudo o a veces»: 15 % en 1993 frente a 33 % en 2000). Con estos datos no se puede separar qué parte del salto es cambio real y qué parte es cambio de instrumento.

**Variables derivadas ya construidas** (`02_Scripts/_exploratorio/01_salud_mental_1993.py` → `01_Datos/02_Procesados/salud_mental_1993.csv` y `.dta`, 12.985 personas, una fila por `pidlink`). Se construyeron en la sesión del 10-nov; su uso en el análisis no está decidido.

| Variable | Definición | Media | NA |
|---|---|---:|---:|
| `sm3_93` | insomnio + tristeza + ansiedad (los 3 ítems que se repiten en 2000), cada uno 0/1/2 → 0-6 | 0,58 | 20 |
| `sm6_93` | los 6 ítems → 0-12 | 1,43 | 46 |
| `triste_93`, `ansioso_93` | 1 si «a menudo» o «a veces» (dicotomización de Friedman y Thomas) | 0,15 / 0,07 | 12-13 |

Recodificación: 1 → 2, 3 → 1, 5 → 0; 6/8/9 → NA; si falta un ítem, el índice es NA. El 69 % tiene `sm3_93` = 0, y la correlación entre `sm3_93` y `sm6_93` es 0,86. El archivo trae también `hhid93`, `commid93`, `smpgrp`, `respwt`, `edad_93`, `mujer` y `parentesco_93`.

### 7.3 Otras características de hogares y personas en 1993

| Dimensión | Archivo · variables |
|---|---|
| Demografía | `bukkar2`: edad, sexo, parentesco, estado civil, religión (`ar15`), educación (`ar16`, `ar17`) |
| Vivienda y servicios | `buk1kr1`: piso, agua, sanitario, electricidad |
| Gasto | `expend2`: `exppc_r`, quintiles |
| Activos y tierra | `buk2hr1` (formato largo, por tipo de activo); `buk2ut1` y `buk2ut2` (finca) |
| Producción y consumo de arroz | `buk2ut*` (producción agrícola) y `buk1ks1` (consumo de producción propia, `ks03rp`). No hay una variable directa de posición neta; habría que construirla. |
| Choques previos | `buk2ge1`: choques económicos de los últimos 5 años, por tipo |
| Ubicación | `bukksc1`: provincia, kabupaten, urbano/rural |
| Madre | `bukkar2$ar11` da la línea de la madre en el roster, lo que permite enlazar sus características (educación, libro III si fue entrevistada) |

## 8. Datos comunitarios de 1993 (`Community Data/`, descargados el 10-nov-2026)

53 archivos del IFLS1-RR comunitario. Entre ellos:

| Archivo | Contenido | N |
|---|---|---:|
| `bukph01` | Libro PKK: **precio promedio por unidad** (`dh1r1`) de arroz de calidad buena, media y baja (`dhtype` 1-3) y otros alimentos; escasez (`dh2`, `dh3`) | 5.616 (18 ítems × 312) |
| `bkppkh01` | Posyandu: módulo equivalente de precios de alimentos | 16.182 |
| `buki_cf`, `bkii_cf` | Jefe de comunidad y estadísticas del pueblo: transporte, electricidad, agricultura, uso del suelo, observación directa | 312 |
| `commwt` | Pesos de comunidad (a nivel de EA: 321 filas, con `commid93`) | 321 |

El contenido de estos archivos (cobertura por `commid93`, unidades, calidades, coherencia entre PKK y posyandu) **no se ha revisado todavía**; queda para cuando se revisen los precios de 1997.

## 9. Esqueleto de lectura en R

*No ejecutado (no hay R en la máquina donde se hizo la revisión); los nombres y códigos sí están verificados contra los archivos.*

```r
library(haven); library(dplyr)
d1 <- "Datos/IFLS1/Household Data"
rd <- function(f) read_dta(file.path(d1, paste0(f, ".dta"))) |> zap_labels()

# Personas (roster) + ubicación + pesos
roster <- rd("bukkar2") |>
  transmute(pidlink, hhid93, commid93, pid93,
            edad93 = if_else(ar09yr >= 95, NA_real_, ar09yr),   # 95-99 = códigos
            mujer  = case_when(ar07 == 3 ~ 1, ar07 == 1 ~ 0),
            linea_madre = if_else(ar11 >= 51, NA_real_, ar11))   # 51/52 = madre fuera del hogar o fallecida (ver codebook); 96-99 faltantes
ubic <- rd("bukksc1") |> select(hhid93, prov = sc01, kab = sc02, kec = sc03, urbano = sc05)

# Antropometría: excluir personas fuera del roster y limpiar códigos
ca <- rd("bukcca2") |>
  filter(person != 96) |>
  mutate(talla = if_else(ca10 == 0 | ca10 >= 999, NA_real_, ca10),
         peso  = if_else(ca13 == 0 | ca13 >= 999, NA_real_, ca13))   # ca13 usa 9996-9999

# Síntomas KK 1993: 1 a menudo, 3 a veces, 5 nunca; 6/8/9 -> NA
kk <- rd("buk3kk2") |>
  mutate(across(starts_with("kk05_"), ~ if_else(.x %in% c(1, 3, 5), .x, NA_real_)))

base93 <- roster |> left_join(ubic, by = "hhid93") |>
  left_join(select(ca, pidlink, talla, peso), by = "pidlink") |>
  left_join(select(kk, pidlink, starts_with("kk05_")), by = "pidlink")
stopifnot(nrow(base93) == 33081)   # la unión no debe duplicar personas
```

## 10. Preguntas abiertas (se deciden con todas las olas revisadas)

Esta guía no toma posición sobre ellas; solo registra qué información de 1993 es pertinente a cada una.

- **Unidad de comunidad:** `commid93` (312) o EA (321). Ver §6.1.
- **Síntomas de adultos:** si se usan, y cómo (6 ítems de 1993, los 3 que se repiten en 2000, ítems por separado, dicotomizados o en escala). Ver §7.2. Las variables de `01_salud_mental_1993.py` son una opción ya construida, no una decisión.
- **Muestra de adultos:** cómo tratar la selección del libro III (`smpgrp`) y las entrevistas por proxy. Ver §4 y §7.2.
- **Pesos:** con o sin pesos, y cuáles. Ver §6.5.
- **Gasto pre-crisis:** `expend2` (imputado sin marca) o un agregado propio desde los módulos de consumo. Ver §6.6.
- **Edad para HAZ:** cómo combinar fecha de nacimiento, edad declarada y edad del roster. Ver §7.1.
- **Posición neta en arroz:** si se construye y con qué módulos. Ver §7.3.

## 11. Lo que no está verificado

- El significado exacto de los códigos 51 y 52 de `ar10`/`ar11` (en los datos hay 8.494 y 7.811 casos): confirmar en `DRU1195.4.BookK.pdf`.
- El contenido y la calidad de los precios comunitarios de 1993 (PKK y posyandu): los archivos están descargados pero no revisados.
- La consistencia entre la edad de antropometría (`ca06yr`) y la del roster (`ar09yr`).
- El esqueleto de R (§9) no se ha ejecutado.
