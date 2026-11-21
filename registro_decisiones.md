# Registro de decisiones

> Lo confirmado para el trabajo, en corto. Si contradice a `10_Propuesta/`,
> `PLAN.md` o `CLAUDE.md`, manda este archivo. Cada decisión lleva fecha y quién
> la tomó; si se cambia, se edita aquí y se anota en el historial del final.

## 1. Administrativas

| Decisión | Fecha | Quién |
|---|---|---|
| **R para todo el pipeline**, incluida la construcción de bases (`haven::read_dta()` + `tidyverse`). `00_main.R` es el único punto de entrada | 20-nov | Santiago |
| Ampliaciones frente al curso: `haven`, `get_scores`, `best_linear_projection`, `average_treatment_effect(subset = …)`; `fwildclusterboot` si se usa | 20-nov | Santiago |

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
| **Terciles** | Tercil alto = 1, bajo = 0, sin el medio | Bosque: GATE, calibración, RATE |

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

## 5. Muestra, medición, controles y modificadores

- **HAZ:** estándares OMS (`anthro` hasta 60 meses, `anthroplus` desde 61);
  edad en meses = fecha de medición − fecha de nacimiento; acostado o de pie
  según `us05`; se excluyen los HAZ fuera de ±6.
- **Entrevistas de 1997 hechas en 1998:** entran con un indicador en X; una
  robustez excluye las 27 comunidades con precio levantado en 1998 y a los niños
  medidos en 1998.
- **Sin pesos muestrales** en lo principal; versión con pesos longitudinales de
  la IFLS como robustez.
- **Controles de la pregunta 1** (todos de 1997): la lista del cuadro A1 de E-Q medida en 1997,
  sin los cinco programas de la red de seguridad social (tarjeta de salud, arroz
  gratis, arroz subsidiado, programa de empleo, transferencia a la aldea).
- **Comprador neto:** hogar cuyo valor de arroz comprado supera el de su
  producción propia (`b1_ks1` 1997). Binaria.
- **Pobre:** gasto per cápita de 1997 bajo la línea oficial de pobreza de fines
  de los 90 (Widyanti et al. 2009), como E-Q. Si no se consigue el valor de la
  línea, el cuartil inferior nacional del gasto per cápita. Se fija en H2, antes
  de ver resultados.

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

## Historial

- 20-nov-2026: creación (Santiago).
