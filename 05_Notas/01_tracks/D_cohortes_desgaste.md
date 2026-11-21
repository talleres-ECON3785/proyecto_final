# Dos de cada tres niños de 0-5 años en 1997 (2.526 en 307 comunidades) llegan a 2000 con su comunidad de 1997 y un HAZ válido en los dos años; la pérdida mayor es estar fuera de las comunidades IFLS en 1997

- **Estado:** vigente
- **Etapa / alcance:** D; descriptivo
- **Script de origen:** `02_Scripts/01_tracks.R` (seguimiento) y `02_Scripts/04_haz.R` (HAZ)
- **Hipótesis relacionada:** ninguna (sostiene la muestra de la pregunta 1 y la placebo)
- **Última verificación:** 2026-11-20, con `02_Scripts/01_tracks.R` y `02_Scripts/04_haz.R`

## Evidencia

`03_Resultados/Tablas/01_tracks/cohortes_desgaste.{png,csv}`. Cada paso exige el
anterior.

| Cohorte principal (0-5 años en 1997) | Niños | Comunidades |
|---|---:|---:|
| Miembros del hogar en 1997 | 3.851 | 312 |
| En una comunidad IFLS en 1997 | 3.369 | 312 |
| Evaluación de salud en 1997 | 2.940 | 310 |
| Miembros del hogar en 2000 | 2.843 | 309 |
| Evaluación de salud en 2000 | 2.832 | 308 |
| Muertos en 2000 (de los 3.851) | 33 | 26 |

| Cohorte placebo (0-5 años en 1993) | Niños | Comunidades |
|---|---:|---:|
| Miembros del hogar en 1993 | 4.268 | 311 |
| Evaluación de salud en 1993 | 3.902 | 308 |
| Miembros del hogar en 1997 | 3.546 | 308 |
| Evaluación de salud en 1997 | 3.228 | 306 |

«Evaluación de salud» quiere decir que se hizo el módulo de medición.

**HAZ válido** (`03_Resultados/Tablas/04_haz/cohortes_haz_resumen.{png,csv}`;
puntaje z de la OMS, edad desde la fecha de nacimiento del `ptrack` de 2000,
HAZ fuera de ±6 excluidos):

| Cohorte · año | Con talla | HAZ válido | Comunidades | HAZ medio (DE) |
|---|---:|---:|---:|---:|
| Principal · 1997 | 3.217 | 3.043 | 308 | −1,755 (1,575) |
| Principal · 2000 | 3.422 | 3.359 | 311 | −1,729 (1,140) |
| Principal · los dos años, con comunidad IFLS (cambio) | — | **2.526** | **307** | +0,026 (1,333) |
| Placebo · 1993 | 3.261 | 2.970 | 303 | −1,704 (1,605) |
| Placebo · 1997 | 3.530 | 3.429 | 306 | −1,816 (1,133) |
| Placebo · los dos años, con comunidad IFLS (cambio) | — | **2.504** | **301** | −0,072 (1,434) |

Las filas de cada año no exigen comunidad IFLS. Entre la talla y el HAZ válido
se pierden los niños sin fecha de nacimiento o de medición (de 3.217 con talla
a 3.168 con talla y edad en 1997) y los HAZ fuera de ±6 (64 en 1997, 15 en
2000).

## Qué dice, en lenguaje intuitivo

De los 3.851 niños pequeños de 1997, 2.526 (66 %) tienen todo lo necesario
para entrar al análisis: vivían en una de las comunidades de la encuesta (donde
se mide el precio del arroz) y tienen una talla para la edad válida en 1997 y en
2000. Por el lado del seguimiento llegan 2.832 (74 %): vivían en una de las
comunidades de la encuesta, donde se mide el precio del arroz, se midieron en
1997 y se volvieron a medir en 2000. La pérdida más grande (482 niños, 13 %)
está al principio: vivían en hogares fuera de las comunidades de la encuesta,
casi siempre porque la familia se había mudado, y para ellos no hay precio
comunitario. Entre 1997 y 2000 se pierden pocos: 97 de los medidos en 1997 dejan de
ser miembros de su hogar y 11 no se midieron en 2000; en toda la cohorte
murieron 33 niños antes de 2000. Casi todas las comunidades
(307 de 312) siguen representadas. En promedio, estos niños miden unas 1,7
desviaciones estándar menos que la referencia de la OMS en los dos años; el
cambio promedio entre 1997 y 2000 es casi cero, pero varía mucho de niño a niño.

## Por qué importa en el estudio

- Sostiene la pregunta 1: el contraste entre comunidades descansa en unas 308
  comunidades, no en miles de niños. Esa es la unidad de inferencia.
- El desgaste entre 1997 y 2000 es pequeño (108 de 2.940, ≈ 4 %, de quienes se
  midieron en 1997). Si dependiera del alza del precio sesgaría el ATE; eso se prueba en
  P1.5 (desgaste según el alza) y P2.3.
- **Consistente** con la síntesis de datos (`01_Datos/00_sintesis_revision_IFLS.md`
  §4.3: 3.851 miembros, 3.217 con talla en 1997 y 3.422 en 2000, iguales a los
  de la tabla de HAZ).
- **Difiere (atribuible)** del conteo exploratorio de `PLAN.md` (2.668 niños en
  307 comunidades con talla en los dos años): con HAZ válido quedan 2.526, por
  la fecha de nacimiento y los HAZ fuera de ±6.
- **Difiere (causa no verificada)** de la muestra de Elmira y Qaim (2026): 2.112
  niños en su cuadro 1 y 3.338 observaciones en su cuadro A1 (≈ 1.669 niños si
  el panel es balanceado; `07_Recursos/Articulos/00_hallazgos_articulos.md`).
  Nuestra muestra es mayor. Ellos no detallan sus filtros (y su propia cifra
  entre el cuadro 1 y el A1 no cuadra), así que la diferencia es de construcción
  de la muestra, no de resultados. Se revisa en P1.5.
- La cohorte placebo deja 2.504 niños con HAZ válido en 1993 y 1997, en 301
  comunidades (de 1993), para la prueba de tendencias previas.

## Límites e incertidumbre

- Los 482 niños fuera de las comunidades IFLS en 1997 no son una muestra al azar
  (hogares que migraron entre 1993 y 1997). La conclusión vale para los niños
  que vivían en las comunidades de la encuesta.
- El cambio en el HAZ es muy disperso (DE de 1,333 en tres años), lo que sugiere
  errores de medición o de fecha en parte de los niños. El registro no prevé
  recortar la cola; se revisa su distribución en P1.5.
- 85 niños sin fecha de nacimiento quedan fuera; no se usaron otras fuentes de
  fecha para no mezclar edades entre olas.
- Para la placebo se guardan la comunidad de 1993 y la de 1997; cuál asigna el
  alza se decide en P2.3.

## Historial

- 2026-11-20: creación (P1.1).
- 2026-11-20: se agrega el HAZ válido (P1.4); el título pasa de 2.832 niños con evaluación de salud a 2.526 con HAZ válido.
