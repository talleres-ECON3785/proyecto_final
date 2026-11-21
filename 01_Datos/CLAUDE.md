# 01_Datos/CLAUDE.md · Reglas para manejar la IFLS

> Complementa el `CLAUDE.md` de la raíz. Claude Code lo carga al trabajar dentro
> de `01_Datos/`; **léalo también antes de escribir o modificar cualquier script
> que lea o una datos** (en `02_Scripts/`), aunque el trabajo no ocurra aquí.
> Recoge lo aprendido en las cinco rondas de revisión de datos (10 al 14 de
> noviembre de 2026). Si algo de aquí contradice una guía de ola, manda la guía
> más reciente y se corrige este archivo en el mismo cambio.

## 1. Qué hay y dónde

```
01_Datos/
├── CLAUDE.md                       # este archivo
├── README.md                       # cómo descargar los datos de RAND y dónde ponerlos
├── 00_sintesis_revision_IFLS.md    # síntesis de las cinco olas (citada como «S §x»)
├── 01_Crudos/                      # NO se versiona (salvo .md y _revision/)
│   ├── IFLS1/  00_guia_IFLS1.md (G1) · Household Data · Community Data · Documentation · _obsoleto/
│   ├── IFLS2/  00_guia_IFLS2.md (G2) · Household Data · Community Data · Documentation
│   ├── IFLS3/  00_guia_IFLS3.md (G3) · Household Data · Community Data · Household/Community Documentation
│   ├── IFLS4/  00_guia_IFLS4.md (G4) · Household Data · Community Data · Household/Community Documentation
│   └── IFLS5/  00_guia_IFLS5.md (G5) · Household Data · Community Data · Documentation · _revision/
├── 02_Procesados/                  # NO se versiona: bases intermedias que salen de los scripts
└── 03_Listos/                      # NO se versiona: bases finales que entran a la estimación
```

| Ola | Año de campo | Formato `.dta` | Peso | Guía |
|---|---|---|---|---|
| IFLS1 | 1993 | versión RR | 229 MB | `01_Crudos/IFLS1/00_guia_IFLS1.md` (v2) |
| IFLS2 | 1997 (hasta abr-1998) | 104 (comunitarios) | 399 MB | `01_Crudos/IFLS2/00_guia_IFLS2.md` |
| IFLS3 | 2000 | — | 346 MB | `01_Crudos/IFLS3/00_guia_IFLS3.md` |
| IFLS4 | 2007-08 | — | 1,4 GB | `01_Crudos/IFLS4/00_guia_IFLS4.md` |
| IFLS5 | 2014-15 | 111 | 2,0 GB | `01_Crudos/IFLS5/00_guia_IFLS5.md` |

**Cómo leer la documentación.** Empiece por `00_sintesis_revision_IFLS.md`: está
organizada por tema (llaves, seguimiento, comunidad, fechas, antropometría,
educación, cognición, arroz, precios, choques, pesos) y remite a la sección de
cada guía (G1-G5 §x). Abra la guía de una ola solo para el detalle. La
documentación original de RAND (codebooks, cuestionarios, guías de usuario) está
en las carpetas `Documentation` de cada ola, solo en la copia local.

**Las guías y la síntesis son descriptivas:** qué hay, cómo está codificado, qué
problemas tiene. No asignan variables a resultado, control o muestra. Las
recomendaciones de uso están en `10_Propuesta/02_datos_ifls_acceso_y_manejo.md`
§5 y se vuelven decisiones solo cuando el equipo las aprueba (ver §9).

## 2. Licencia de RAND (no negociable)

- El repositorio es **público**. Los microdatos de la IFLS y todo lo derivado a
  nivel de persona, hogar o comunidad (`02_Procesados/`, `03_Listos/`) **nunca**
  se suben. El `.gitignore` lo impide; no use `git add -f` sobre nada de
  `01_Datos/` que no sea `.md`, `.gitkeep` o `_revision/`.
- Las tablas y figuras de `03_Resultados/` sí se versionan, pero solo con
  agregados: nada de listados de personas u hogares, ni celdas que permitan
  identificar una comunidad (p. ej. medias de una sola comunidad con su código).
  Si una tabla necesita celdas pequeñas, reporte el número de observaciones y
  pregunte antes de versionarla.
- No intentar identificar personas, hogares ni comunidades.
- Cada integrante que toque los datos debe estar registrado en RAND (pendiente
  de verificar; ver `HANDOFF.md`).
- Citar el informe de campo de cada ola (lista en `README.md`).

## 3. Flujo de los datos

- **Crudos → Procesados → Listos, nunca al revés.** Los `.dta` crudos no se
  editan, no se renombran y no se mueven.
- Todo derivado sale de un script numerado de `02_Scripts/` (rutas relativas a
  la raíz, semilla 2026) que lo deja en `02_Procesados/` o `03_Listos/`. No hay
  bases construidas a mano.
- Reportar en cada paso cuántas observaciones (personas, hogares, comunidades)
  se pierden y por qué; el script lo imprime y la bitácora lo registra.
- Antes de cada unión: (i) resumir o pivotar a una fila por llave los archivos en
  formato largo; (ii) verificar unicidad de la llave con `stopifnot()`; (iii)
  después de unir, `stopifnot(nrow(despues) == nrow(antes))` salvo que la unión
  deba cambiar filas, y entonces se dice cuántas.
- **Verificar contra los datos antes de afirmar** la ubicación, el nombre o la
  codificación de una variable. Los esqueletos de `10_Propuesta/` usan nombres
  ilustrativos y nunca se han ejecutado.
- Ninguna cifra se escribe a mano en un documento: sale de un script o de una
  guía que cite el script que la produjo.

## 4. Lectura de los archivos

| Problema | Dónde | Qué hacer |
|---|---|---|
| Faltantes leídos como 1,75e+100 con `pyreadstat` | 68 de 69 comunitarios de IFLS2 (formato 104) | Convertir a NA antes de calcular. No comprobado con `haven::read_dta()`: verificarlo la primera vez |
| Enteros con faltantes leídos como texto | 201 de 230 archivos de IFLS3 (4.102 columnas); también `bek` de 1997 | `pd.to_numeric`; en R, revisar el tipo de cada columna tras leer |
| `VAR` frente a `VAR_` | IFLS1 (versión RR) | Usar `VAR`; `VAR_` es el valor original sin corregir |
| Etiquetas de valores casi ausentes | Todas | Codificar con el codebook o el cuestionario |
| Copias duplicadas | `Household Data/hh97usdta/` (= `bus_0`/`bus_1`); `kec_9899000714.dta 2` en 2014 | No usar las dos |
| `.zip` dentro de `Documentation` | IFLS2 `volume4/` | Son documentación; no hace falta extraerlos para los datos |

## 5. Llaves

- **Persona:** `pidlink` (texto, 9 caracteres, constante entre olas). Dentro de
  una ola, `hhidXX` + `pidXX`.
- **Hogar:** `hhid93/97/00/07/14` (cambian por divisiones del hogar; el 6.º
  dígito marca la ola del *split-off*).
- **Comunidad:** `commid93/97/00/07/14`. En 2014 los comunitarios son por EA
  (`ea`, 320), no por `commid14` (311), y `htrack` no trae `ea`.
- **Todos los ids son texto con ceros a la izquierda: nunca convertirlos a
  número.**
- Para cualquier unión entre olas, partir de `htrack`/`ptrack`.
- `pidlink` **no es único** en varios archivos (rosters y archivos de medición
  acumulativos; S §3.2). Quitar `ar01a = 3` (y 0, 6 en 2014) antes de unir; aun
  así en `bk_ar1` de 2014 quedan 292 repetidos (G5 §6.1).
- Ubicación de 1993: `bukksc1` (`sc01` provincia, `sc02` kabupaten, `sc05`
  urbano). No usar la migración de `buk3mg2` para ubicar.

## 6. Códigos y unidades

- Faltantes según el ancho del campo: 1 dígito 5/6/7/8/9; 2 dígitos 95-99;
  3 dígitos 995-999; talla 999,5-999,9; peso `ca13` 9996-9999. **Limpiar
  variable por variable con el codebook**: en variables de 1 dígito, 5 puede ser
  válido (`kk05_*`: 1 a menudo, 3 a veces, 5 nunca).
- Sí/no = 1/3. Sexo = 1 hombre / 3 mujer. Años con dos dígitos. Talla y peso
  = 0 significa no medido.
- Precios con 99998/99999 o 999998 son códigos, no precios (2000 `pos_h`,
  2007, 2014 `hin_h`).
- **Rupias:** nominales por ola; deflactar para comparar (inflación de 1998 muy
  alta). Revisar atípicos de factor 1.000 (montos pedidos en miles).
- `expend2` (gasto de 1993) lo imputó otro proyecto sin marcar qué hogares; RAND
  no lo soporta.
- HAZ con estándares OMS; edad en meses desde fecha de nacimiento y de medición;
  contrastar `ca06yr` con la edad del roster.

## 7. Particularidades por ola

**IFLS1 (1993).** `bukcca2` tiene 4 filas `person = 96` (descartar); `buk1ks1`
tiene 56 duplicados `hhid93 + item` (sumar). Salud mental del libro III: jefe o
cónyuge, una persona de 50+ y, solo en 1/4 de los hogares, una de 15-49
(`indivwt$smpgrp`). Los ítems son 6 síntomas de la sección KK «adaptados del
GHQ», no el GHQ. Los códigos 51 y 52 de `ar10`/`ar11` están sin confirmar.

**IFLS2 (1997).** Dentro de la ola, persona = `hhid97` + `pid97`; `pidlink` se
repite en `bk_ar1` y `bus_1` (quien se mudó aparece en el hogar de origen y en
el *split-off*). `commid97` está solo en `htrack` y falta en 894 hogares fuera
de comunidades IFLS. Parte del campo es de inicios de 1998 (627 hogares, 27
comunidades): revisar la fecha de entrevista. `bek` (cognición) se descargó
aparte; en `ektype`, números = matemáticas y letras = bahasa (niveles 1-4
confirmados). Falta `b3p_tk4` (menor). IFLS2+ (1998) no es pública.

**IFLS3 (2000).** `commid00` con letras = hogar fuera de comunidades IFLS (unir
con el mini-CFS por `mkid00`). El libro PKK de 2000 no tiene precios.
`bk2_hpj` está en formato ancho (en 1997 era largo).

**IFLS4 (2007-08).** Las etiquetas de `kptype` (CES-D, `b3b_kp`) del codebook
**no coinciden con el cuestionario**: usar las del cuestionario. El apéndice A
de la guía de usuario es copia del de IFLS3. Precios del arroz en `hin_h`,
`hps_h`, `htw_h` (no hay `pos_h` ni `bk2_hpj`). No hay módulo general de choques
del hogar. Sin aclarar: códigos 6 y 98 de `mover07`, comunidad `9999` y 9
comunidades con dos filas en los comunitarios.

**IFLS5 (2014-15).** `htrack` es acumulativo (19.401 filas; llave = los seis
`hhidXX`; `hhid14` vacío en 3.480). `ptrack` repite `pidlink` 3 veces y tiene 3
`pidlink` de 8 caracteres. `result14`: códigos 2-4 del codebook no coinciden con
la guía de usuario. CES-D (`b3b_kp`): etiquetas del codebook correctas, una sola
pregunta `kp02`. EK: `ekN_ans` = 0 también si no hubo respuesta. `b2_nd2`
incluye choques económicos; `ndtype` D/E invertidos entre codebook y
cuestionario. Precios del arroz en `hps_h`, `htw_h`, `hin_h` (llave `fascode` +
`htype`; `hin_h` trae 999998). La encuesta comunitaria es de mar-ago 2015,
después de buena parte de las entrevistas de hogar (sep 2014-sep 2015). No hay
archivos del libro proxy. 6.815 de 15.921 hogares viven fuera de las EA de la
IFLS. El catálogo de archivos está en `IFLS5/_revision/_cat.md` (la guía §5
conserva el marcador `<<CATALOGO>>`).

## 8. Tratamiento, muestras y selección

- **Precio del arroz:** hasta seis fuentes por comunidad (PKK, mercado,
  posyandu, tiendas, informante). Revisar unidades (kg frente a litro) y calidad
  (`dhtype` 1-3). Cómo combinarlas está por aprobar (§9). Que las informantes
  PKK/posyandu sobre-reporten **no** está verificado en estos datos.
- El precio de 2000 no es el pico de 1998: mide el alza persistente, con error
  (sesga hacia cero). No hay precios comunitarios de 1998 ni 1999.
- **Tratamiento por residencia en 1997** (`commid97`); la migración posterior es
  resultado, no control.
- **Desgaste y mortalidad selectiva:** comparar las características de 1997 de
  quienes llegan a 2014 por nivel de tratamiento.
- Cohorte de 0-5 años en 1997 (`ptrack`, `age_97` ≤ 5 y `member97` = 1): 3.851
  niños; en 2014, 2.586 con talla, 2.682 con nivel educativo, 2.535 con alguna
  prueba EK completa y 2.578 con CES-D (S §4.3).
- El salto de prevalencia de salud mental 1993→2000 mezcla cambio real y cambio
  de formato: solo interpretar el contraste entre comunidades.
- No controlar por variables posteriores al tratamiento (OPK/Raskin, migración,
  salud o estatura posteriores a 1997).

## 9. Decisiones de uso de los datos

Hasta que el equipo apruebe las recomendaciones de
`10_Propuesta/02_datos_ifls_acceso_y_manejo.md` §5 (17 preguntas abiertas de
S §11), ninguna es definitiva. Cuando se aprueben, se registran aquí y en
"Decisiones tomadas" del `CLAUDE.md` raíz, con fecha.

| Fecha | Pregunta (S §11) | Decisión | Razón |
|---|---|---|---|
| 2026-11-20 | 1-6, 10-13, 15, 17 | Aprobadas, con ajustes, en `registro_decisiones.md` §4-5 (raíz): precio con mediana de todas las calidades y cambio proporcional; comprador neto binario | Decisión de Santiago; el registro manda sobre las recomendaciones de abajo |

Recomendaciones vigentes (pendientes de aprobación): unidad `commid97` (312);
tratamiento por residencia en 1997 (fuera los 894 hogares sin `commid97`); dos
construcciones del precio (principal: mediana de fuentes comunes 1997-2000,
posyandu + `bk2_hpj`, calidad media, kg, cambio proporcional nominal
winsorizado p1/p99, no Δlog; réplica E-Q aproximada con todas las fuentes de
cada año; registrado el 20-nov en `CLAUDE.md` §11 y `PLAN.md` H1); indicador de
entrevista en 1998; sin pesos en lo principal; posición neta en arroz desde
`b1_ks1` 1997; agregado de gasto propio de 1997; cohorte no expuesta de 22-30
años en 1997.

## 10. Derivados existentes

| Archivo | Script | Contenido | Estado |
|---|---|---|---|
| `02_Procesados/salud_mental_1993.{csv,dta}` | `02_Scripts/_exploratorio/01_salud_mental_1993.py` (Python + `pyreadstat`) | `sm3_93`, `sm6_93`, `triste_93`, `ansioso_93`; 12.985 personas, una fila por `pidlink` | Exploratorio; uso no decidido (salud mental es extensión opcional) |

## Qué no está verificado

- Que `haven::read_dta()` lea bien los comunitarios de 1997 (formato 104) y los
  enteros con faltantes de 2000.
- Lo que cada guía marca como no verificado (sección final de cada una y S §12).
