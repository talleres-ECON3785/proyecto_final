# 02 · Datos: acceso, lo que encontramos en las cinco olas y recomendaciones de uso (versión 4)

> Versión 4, 17-nov-2026. La v2 describía los datos según la documentación de RAND, sin haberlos abierto. Desde el 14-nov las cinco olas están revisadas: `01_Datos/01_Crudos/IFLS1/` a `IFLS5/00_guia_IFLSx.md` y la síntesis `01_Datos/00_sintesis_revision_IFLS.md` (citada como S §x). Las guías son descriptivas; **este documento sí recomienda** cómo usar los datos, porque `CLAUDE.md` (§4, decisión del 12-nov) fijó que las decisiones se tomarían con todas las olas revisadas. Son recomendaciones: decide el equipo.

## 1. Acceso y licencia (sin cambios)

- Registro gratuito en RAND; cada integrante que toque los datos debe estar registrado (pendiente de verificar, `CLAUDE.md` §10).
- **No redistribuir.** El `.zip` de entrega lleva `README.md` con instrucciones de descarga y scripts que construyen todo desde los crudos. Citar el informe de campo de cada ola.
- IFLS2+ (1998) **no está en la descarga pública** (S §1, §10).

## 2. Lo que hay, en una tabla

| | 1993 | 1997 | 2000 | 2007-08 | 2014-15 |
|---|---|---|---|---|---|
| Papel en el proyecto | Tendencias previas | **Línea base y X** | Corto plazo; precio post | Cognición (secundaria) | **Largo plazo** |
| Campo (hogares) | ago-93 a ene-94 | ago-97 a **abr-98** | jun-dic 2000 | nov-07 a jul-08 | sep-14 a sep-15 |
| Comunidades IFLS | 312 `commid93` (321 EA) | 312 | 312 | 312 | 311 `commid14` (320 EA) |
| Formato / lectura | Stata 6 | Comunitarios: faltantes = 1,75e+100 con `pyreadstat` | Enteros con faltantes leídos como texto | Sin problemas | Sin problemas |

Fuente: S §1. El `htrack` de 2014 es acumulativo (19.401 filas) y sus conteos no coinciden con la guía de usuario (S §9).

## 3. Tamaños de muestra que ya conocemos (S §4.3-4.4)

| Muestra | 1997 | 2000 | 2007 | 2014 |
|---|---:|---:|---:|---:|
| Cohorte 0-5 en 1997 (`age_97` ≤ 5, `member97` = 1): miembros | 3.851 | 3.646 | 3.451 | 2.846 |
| … con talla | 3.217 | 3.422 | 3.284 | 2.586 |
| … con pruebas cognitivas | — | 1.240 | EK1 3.361 / EK2 727 | 2.535 (EK completo) |
| … con educación (`dl06`) / CES-D | — | — | — | 2.682 / 2.578 |
| Cohorte 5-21 en 1997: miembros | 12.632 | — | — | 8.423 |
| … con escolaridad 2014 (`dl06`) / talla / EK | — | — | — | 7.925 / 7.650 / 7.250 |

La escolaridad de 2014 tiene **tres veces más observaciones** que la talla de la cohorte 0-5. Es un argumento para que sea el resultado primario (`00`, decisiones).

## 4. Variables por constructo (verificadas en las guías)

| Constructo | Dónde | Notas de manejo |
|---|---|---|
| Comunidad de 1997 | `commid97`, **solo en `htrack`** | Falta para 894 hogares fuera de comunidades IFLS (S §5.1) |
| Precio comunitario del arroz 1997 | `pkk_h` (PKK, 310 comunidades), `pos_h` (posyandu, 308), `bk2_hpj` (tiendas y mercados, 265, solo calidad media) | Unidades kg, litro y «otra»; códigos 6-8 de unidad sin etiqueta en `pkk_h` (S §7.6) |
| Precio comunitario del arroz 2000 | `pos_h` (310), `bk2_hpj` (250, formato ancho) | **El libro PKK de 2000 no tiene precios**; `h01x` casi vacío y 99998 en `pos_h` |
| Medianas sin limpiar (Rp/kg, calidad media) | 1997: PKK 1.200, mercado 1.200 · 2000: posyandu 2.000, mercado 2.000 | Solo orientativas (S §7.6) |
| Antropometría | 1997 `bus_1` (`us04`, `us04x`); 2000 `bus2_1`; 2014 `bus_us` | Archivos con el roster acumulado (`pidlink` repetido); en 2014 no hay fecha de nacimiento en `bus_us` (S §7.1) |
| Escolaridad 2014 | `b3a_dl1`: `dl04`, `dl06` (nivel), `dl07` (grado; 7 = graduado) | El codebook etiqueta 1-6 de `dl07` como «missing» por error (S §7.3) |
| Cognición | 2014: `ek_ek1` (7-14), `ek_ek2` (15+: `ek1`-`ek12` + `ek18`-`ek22`) | `ekN_ans` = 0 también sin respuesta; la de 1997 no es comparable (S §7.4) |
| Consumo de arroz 1997 | `b1_ks1`, ítem A: compra y producción propia | 5.075 hogares compran, 1.511 producen y 193 ambas; `b1_ks4` de 1997 **no** incluye arroz (S §7.5) |
| Choques 1997 | `b2_ge` (5 años): pérdida de cosecha 891 hogares; «demasiado seco» en 431 de 960 menciones | Comunitario: `bk1_e2` (S §7.7) |
| Programas de arroz | 2000: OPK (3.403 hogares, `b1_ksr4`); 2007/2014: Raskin | Posteriores al tratamiento: no van como control |
| Pesos | `pwt97l`, `pwt97x`… (S §7.9) | La muestra de 1993 no es autoponderada |

## 5. Recomendaciones sobre las 17 preguntas abiertas de la síntesis (S §11)

| # | Pregunta | Recomendación | Alternativa / robustez |
|---|---|---|---|
| 1 | Unidad de comunidad | **`commid97` (312)** como unidad de tratamiento y conglomerado. Las 9 EA gemelas de 1993 comparten `commid93` y se tratan como una comunidad | EA solo si se usan los comunitarios de 2014 (no hace falta para el tratamiento) |
| 2 | Comunidad de quienes se mudaron | Tratamiento por residencia de 1997. Los 894 hogares sin `commid97` quedan fuera; reportar cuántos niños se pierden | — |
| 3 | Precio del arroz | **Dos construcciones.** (a) **Principal:** mediana por comunidad de las fuentes presentes en 1997 y 2000 (posyandu + `bk2_hpj`), calidad media, solo kg; Δlog winsorizado en p1/p99. (b) **Réplica E-Q:** promedio de todas las calidades y fuentes disponibles en cada año (E-Q p. 3) | Con PKK en 1997; calidad baja (la que compran los pobres); deflactado |
| 4 | Entrevistas de 1998 | Indicador en X; robustez excluyendo los 627 hogares, las 27 comunidades con precio levantado en 1998 y las mediciones de 1998 | — |
| 5 | Edad | Edad en meses = fecha de medición − fecha de nacimiento (`ptrack`/roster); comparar con `age_97` y marcar incoherencias > 12 meses | — |
| 6 | Antropometría | HAZ con estándares OMS (`anthro` para 0-5 y `anthroplus` para 5-19 en R); quitar códigos de no medido y z fuera de ±6 | — |
| 7 | Salud mental | Extensión opcional (`05`): `sm3_93` y los 3 ítems comunes de 2000 | — |
| 8 | Escolaridad | Años completados en 2014 desde `dl06` × `dl07` con una tabla de equivalencias nivel → años (por construir con los códigos de G5 §9.3) | Nivel máximo (categórico) |
| 9 | Cognición | 2014: proporción de aciertos en EK2 (17 ítems), estandarizada por año de edad; respuesta faltante ≠ 0 | 2007 como secundaria |
| 10 | Posición neta en arroz | **Construirla** desde `b1_ks1` 1997: proporción del valor del arroz consumido que es de producción propia; tres categorías (solo compra, mixto, solo propio) | Revisar si `ut` 1997 trae venta de arroz |
| 11 | Choques | X de la comunidad: proporción de hogares con pérdida de cosecha por sequía en `b2_ge` 1997 | Excluir Sumatra/Kalimantan |
| 12 | OPK/Raskin | No controlar (son posteriores); describir como canal | — |
| 13 | Pesos | **Sin pesos** en lo principal (efectos causales con X ricas); versión ponderada con pesos longitudinales como robustez | — |
| 14 | `result07`/`result14` | Solo para el desgaste; documentar | — |
| 15 | Roster | Quitar `ar01a` = 3 (y 0, 6 en 2014) antes de unir; `stopifnot` de unicidad | — |
| 16 | Proxy | No hay salud mental por proxy; para educación y talla no afecta | — |
| 17 | Gasto del hogar | Agregado propio de 1997 (alimentos semanales × 52/12 + no alimentos mensuales + anuales/12), per cápita, deflactado por comunidad | Índice de activos si el agregado no alcanza a estar a tiempo |

## 6. Orden de construcción (scripts numerados)

1. `01_tracks`: `htrack`/`ptrack` 1997-2014; `commid97`; cohortes; desgaste.
2. `02_precio_arroz`: precios 1997 y 2000, unidades, medianas, terciles, las dos construcciones.
3. `03_x_1997`: roster, educación de los padres, consumo de arroz, gasto, activos, choques.
4. `04_haz_9700`: antropometría y HAZ (replicación).
5. `05_escolaridad_2014`: años completados y la cohorte no expuesta.
6. `06_cognicion` (si hay tiempo).
7. `10_validacion`, `20_bosques`, `30_arbol_honesto`, `40_focalizacion`.

Lenguaje: decisión pendiente (`CLAUDE.md` §10). Recomendación: R para todo con `haven` (ampliación frente al curso), o Python (`pyreadstat`) solo para los pasos 1-3 y R para estimar. En cualquier caso se documenta en el README.

## 7. Tiempo estimado

Pasos 1-2: 2-3 días. Pasos 3-5: 4-6 días. Validación y bosques: 3-4 días. **Antes de la asesoría:** pasos 1-2 y las pruebas 1-5 de `03`, aunque no haya resultados.

## 8. Qué no está verificado

- Las cifras de esta nota vienen de la síntesis y de las guías; no se volvieron a correr.
- Que `haven::read_dta()` lea bien los comunitarios de 1997 (formato 104).
- La conversión kg/litro y los atípicos de precio; los precios de 1993.
- Que la construcción «réplica E-Q» coincida con la de los autores: no sabemos qué fuentes usaron en 2000, porque el libro PKK de ese año no tiene precios (S §7.6) y E-Q dicen haber usado los de los grupos de mujeres (p. 3).
- La tabla de equivalencias nivel → años de 2014 y el agregado de gasto de 1997 no existen todavía.
