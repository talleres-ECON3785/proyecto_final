# Registro de decisiones

> Lo confirmado para el trabajo, en corto. Si contradice a `10_Propuesta/`,
> `PLAN.md` o `CLAUDE.md`, manda este archivo. Cada decisión lleva fecha y quién
> la tomó; si se cambia, se edita aquí y se anota en el historial del final.

## 1. Administrativas

| Decisión | Fecha | Quién |
|---|---|---|
| **R para todo el pipeline**, incluida la construcción de bases (`haven::read_dta()` + `tidyverse`). `00_main.R` es el único punto de entrada | 20-nov | Santiago |
| Ampliaciones frente al curso: `haven`, `get_scores`, `best_linear_projection`, `average_treatment_effect(subset = …)`; `fwildclusterboot` si se usa | 20-nov | Santiago |
| Ampliaciones: `anthro` (HAZ OMS hasta 60 meses) y `anthroplus` (desde 61 meses), para `04_haz` | 20-nov | Santiago |

## 2. Las tres preguntas

Resultado único: **ΔHAZ 1997→2000** de los niños de 0-5 años en 1997 (cohorte de
Elmira y Qaim 2026).

1. **¿Dolió?** Efecto del alza del precio del arroz sobre el HAZ, comparado con
   el −0,135 HAZ por +100 % de E-Q, y su forma (cuartiles). Con `feols`.
2. **¿A quién?** Seis GATE pre-declarados (edad, urbano, educación de la madre,
   sexo, comprador neto, pobreza) con puntajes AIPW del bosque causal, y réplica
   de las cinco interacciones de E-Q con `feols`.
3. **¿El bosque supera a las reglas simples?** RATE del bosque frente a priorizar
   por pobre, urbano o comprador neto.

Detalle de los subgrupos: `10_Propuesta/07_preregistro_heterogeneidad.md`.

## 3. Identificación y tratamiento

- **Contraste:** cada niño contra sí mismo (ΔHAZ), entre comunidades con más y
  menos alza. Se identifica el efecto de más alza frente a menos alza, no el de la
  crisis.
- **Supuesto:** sin la diferencia de alza, y dadas las X de 1997, el ΔHAZ habría
  sido igual. Con la dosis continua hace falta la versión fuerte (Callaway,
  Goodman-Bacon y Sant'Anna); con cuartiles y terciles, no.
- **Asignación:** por la comunidad de residencia en 1997 (`commid97`). Errores
  agrupados por `commid97`; `clusters = commid97` en `grf`.

| Versión | Definición | Uso |
|---|---|---|
| **Dosis** (principal) | Cambio proporcional del precio 1997→2000 por comunidad (§4) | Pregunta 1 y réplica de las interacciones de E-Q |
| **Cuartiles** | Q2, Q3 y Q4 de la dosis frente a Q1 | Forma de la respuesta |
| **Terciles** | Terciles de la dosis **dentro de cada provincia**; tercil alto = 1, bajo = 0, sin el medio (197 comunidades). Los terciles nacionales, como robustez | Bosque: GATE, calibración, RATE |

La comparación con el −0,135 de E-Q es aproximada: ellos combinan fuentes
distintas en cada año (en 1997 incluyen el PKK, que en 2000 no trae precios).

## 4. Precio del arroz

- **Fuentes:** solo las que existen en 1997 **y** en 2000: posyandu (`pos_h`) y
  tiendas y mercados (`bk2_hpj`). El mismo conjunto en los dos años.
- **Escala:** cambio proporcional `(P2000 − P1997) / P1997` (1 = +100 %), como
  E-Q (p. 5).
- **Nominal.** Con un deflactor común a todas las comunidades, el real solo
  reescala β.
- **Resumen por comunidad y año:** mediana de los reportes de todas las
  calidades (Rp/kg).
- **Cola:** el cambio proporcional se winsoriza en p1/p99.
- **Reglas operativas** (`02_Scripts/02_precio_arroz.R`): arroz = `htype` 1-3 en
  `pos_h` y `hpj3type` = 1 en `bk2_hpj`; solo respuestas válidas; el posyandu de
  1997 se asigna por los 4 primeros dígitos de `fcode`. **Los reportes por litro
  se pasan a kg** con un factor estimado en los datos (0,833: mediana, en 142
  comunidades-año con las dos unidades, del precio por litro sobre el precio por
  kg), el mismo en los dos años. Así quedan 297 comunidades con precio en 1997 y
  en 2000; solo con kg, 254, lo que dejaría fuera de forma selectiva a las que
  venden por litro. La dosis solo con kg (`dosis_kg`) es una robustez.
- Cuartiles y terciles se cortan **entre comunidades** (la unidad del
  tratamiento), no entre niños.
- **Terciles dentro de provincia:** la provincia explica el 14,6 % de la varianza
  de la dosis; con terciles nacionales, algunas provincias quedan casi enteras en
  un extremo y el traslape se pega a 0 o 1 si la provincia entra en X.

## 5. Muestra, medición, controles y modificadores

- **Cohortes** (`02_Scripts/01_tracks.R`, solo el `ptrack`/`htrack` de 2000,
  que ya trae 1993-2000): principal = `age_97` ≤ 5 y `member97` = 1 (3.851
  niños); placebo = `age_93` ≤ 5 y `member93` = 1 (4.268). La placebo guarda
  `commid93` y `commid97`; cuál asigna el alza se decide en P2.3.
- **HAZ:** estándares OMS (`anthro` hasta 60 meses, `anthroplus` desde 61);
  edad en meses = fecha de medición − fecha de nacimiento; acostado o de pie
  según `us05`; se excluyen los HAZ fuera de ±6.
  - Fecha de nacimiento: la construida en el `ptrack` de 2000, la misma para
    todas las olas (sin día → 15). Sin ella no hay HAZ (85 niños de la
    cohorte principal). Medición: `bukcca2` (1993, sin las filas
    `person = 96`), `bus_1` (1997), `bus2_1` (2000).
  - El método va **al revés entre olas**: en 1993 (`ca11`) 1 = acostado y
    3 = de pie; en 1997 y 2000 (`us05`) 1 = de pie y 3 = acostado.
- **Muestra analítica** (`05_base.R`): niños de 0-5 años en 1997 con
  comunidad IFLS, precio en su comunidad y HAZ válido en 1997 y 2000: 2.421
  niños en 294 comunidades. La base vive en `01_Datos/03_Listos/` y **no se
  comparte por GitHub** (repositorio público, licencia de RAND): cada integrante
  la regenera con `00_main.R`.
- **Faltantes en los controles:** en los controles lógicos el NA pasa a `FALSE`
  con un indicador `falta_<variable>`; en el tamaño del hogar, a la mediana con
  indicador; en la educación de los padres y el quintil de gasto, a la categoría
  «falta». Los moderadores pre-registrados conservan sus NA.
- **Cola del ΔHAZ** (P1.6): los 110 niños con |ΔHAZ| > 3 (4,5 % de la base)
  **se mantienen** en la estimación principal; en P2.3 va una columna de
  robustez sin ellos (`dhaz_mayor_3`). Su perfil apunta a error de medición
  (bebés con HAZ casi normal en 1997) y su proporción no cambia con el alza
  (`03_Resultados/Tablas/05_base/ninos_dhaz_cola.csv`). Decidido antes de ver el
  ATE.
- **Entrevistas de 1997 hechas en 1998:** entran con un indicador en X; una
  robustez excluye las 38 comunidades con precio levantado en 1998 (libro 2 o
  algún posyandu entrevistado en 1998; 34 de ellas tienen precio en los dos años) y a los niños
  medidos en 1998.
- **Sin pesos muestrales** en lo principal; versión con pesos como robustez:
  los transversales de la evaluación de salud de 2000 (`pw00usxa`, versión a).
  El longitudinal de persona (`pwt00la`) solo es positivo para 932 de los 2.421
  niños de la base (P2.3).
- **Controles de la pregunta 1** (todos de 1997): la lista del cuadro A1 de E-Q medida en 1997,
  sin los cinco programas de la red de seguridad social (tarjeta de salud, arroz
  gratis, arroz subsidiado, programa de empleo, transferencia a la aldea).
- **Comprador neto:** hogar cuyo valor de arroz comprado la última semana
  (`b1_ks1`, ítem A, `ks02`) supera el de su producción propia (`ks03`).
  Binaria. **Productor de arroz** (control de E-Q): producción propia > 0.
- **Gasto per cápita** (agregado propio, mensual, nominal; `03_x_1997.R`):
  alimentos de la última semana (comprados y propios) × 30/7, más no alimentos
  del mes (sin rifas ni arisan), más no alimentos del año / 12, más educación
  de los miembros / 12, más vivienda (arriendo pagado o el que pagaría), todo
  dividido por los miembros de 1997. Los rubros sin valor (rechazo o no sabe)
  cuentan como 0. Quintiles entre los 7.565 hogares de 1997, sin pesos.
- **Pobre:** gasto per cápita bajo la línea regional de diciembre de 1997, por
  provincia y zona urbana o rural (Widyanti, Suryahadi, Sumarto y Yumna 2009,
  *The Relationship between Chronic Poverty and Household Dynamics: Evidence
  from Indonesia*, SMERU Working Paper; apéndice 1, p. 18; método en la sección
  IV, p. 5; nivel de verificación: PDF). Es la misma edición que citan E-Q; no
  hay versión en revista. Detalle en `07_Recursos/Articulos/00_hallazgos_articulos.md` §7. El cuartil inferior del gasto
  per cápita (`pobre_q1`) queda como robustez.
- **Educación de la madre:** nivel más alto del roster de 1997 (`ar16`) de la
  madre si vive en el hogar; «más que primaria» = secundaria o superior.
- **Controles de comunidad** (libro 1 de la comunidad de 1997; E-Q no definen
  cada uno): puskesmas, agua para beber por tubería, vía transitable por
  vehículos, vía asfaltada, parada de bus, mercado, teléfono, correo y banco en
  la aldea, e incendio o sequía registrados en 1997.

Fecha: 20-nov. Quién: Santiago.

## 6. Comparaciones múltiples y focalización

- **Holm** (α = 0,05, bilateral), por familia:
  - F1: los seis contrastes GATE (m = 6);
  - F2: las cinco interacciones de E-Q con la dosis y errores agrupados (m = 5);
  - F3: las tres diferencias de RATE bosque − regla (m = 3).

  El ATE, `test_calibration`, el AUTOC del bosque y la BLP van sin ajuste (una
  prueba cada uno o descriptivos).
- **RATE con AUTOC** (`target = "AUTOC"`). Prioridad del bosque: −τ̂, estimada en
  una mitad de las comunidades y evaluada en la otra.

Fecha: 20-nov. Quién: Santiago.

- **Heterogeneidad, operativo** (al completar P3.1-P3.3 y P4.1):
  - Réplica de E-Q (F2): especificación (4) de la pregunta 1 más dosis × X y X;
    en E1, X = 1 = 0-2 años (inferencia sobre la fig. 5 de E-Q).
  - Bosque: `tercil_prov` alto = 1, bajo = 0; 1.602 niños en 195 comunidades;
    X = controles de la pregunta 1 (sin el cubo de la edad), log del precio de
    1997, provincia, madre con más que primaria, pobre y comprador neto (con
    NA); sin HAZ de 1997; 4.000 árboles, `seed = 2026`, `num.threads = 1`.
  - GATE (F1): en G1, X = 1 = 3-5 años.
  - RATE (F3, al completar P4.2): partición al azar de las 195 comunidades con
    `set.seed(2026)`; bosque de la mitad 1 → τ̂ en la mitad 2; bosque de
    evaluación en la mitad 2 con Y = −ΔHAZ (escala de daño: AUTOC > 0 = la
    regla encuentra a los más dañados); R = 500; muestra común sin NA en las
    tres reglas; las mitades invertidas, solo como robustez.
  Fecha: 22-nov. Quién: Samuel (sesión autónoma; confirmar con el equipo).

## Historial

- 20-nov-2026: creación (Santiago).
- 20-nov-2026: §5, definición de las cohortes al completar P1.1 (Santiago).
- 20-nov-2026: §5, al completar P1.6: la cola del ΔHAZ se mantiene, con
  robustez sin |ΔHAZ| > 3 (Santiago).
- 20-nov-2026: §5, al completar P1.5: muestra analítica, faltantes de los
  controles y la base fuera de GitHub (Santiago).
- 20-nov-2026: §1 y §5, al completar P1.4: `anthro` y `anthroplus` como
  ampliaciones; fuente de la fecha de nacimiento y códigos del método (Santiago).
- 20-nov-2026: §5, al completar P1.3: definiciones operativas de comprador
  neto, gasto per cápita, pobre (línea de Widyanti et al. verificada en el PDF),
  educación de la madre y controles de comunidad (Santiago).
- 20-nov-2026: §3-4, al completar P1.2: litros pasados a kg, cortes entre
  comunidades y terciles dentro de provincia; §5, las comunidades con precio de
  1998 pasan de 27 a 38, porque también cuenta el posyandu (Santiago).
- 22-nov-2026: §5, al completar P2.3: los pesos de la robustez pasan del
  longitudinal de persona (cubre 932 niños) al de la evaluación de salud de 2000
  (cubre los 2.421) (Mateo).
- 22-nov-2026: §6, definiciones operativas de la réplica de E-Q, el bosque
  y los GATE al completar P3.1-P3.3 (Samuel).
- 22-nov-2026: §6, definiciones operativas del RATE al completar P4.2 (Samuel).
