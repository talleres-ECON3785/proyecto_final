# Los niños de los tres cuartiles de mayor alza crecieron menos que los del cuartil de menor alza; el daño más grande está en el cuartil 4 (−0,30 HAZ) y los cuartiles no se alejan de una recta más de lo que permite su incertidumbre

- **Estado:** vigente
- **Etapa / alcance:** A; contraste entre comunidades con mayor y menor alza
- **Script de origen:** `02_Scripts/07_cuartiles.R`
- **Hipótesis relacionada:** ninguna de H1-H8 (es la pregunta 1, forma del efecto promedio)
- **Última verificación:** 2026-11-22, con `02_Scripts/07_cuartiles.R` (P2.2)

## Evidencia

- `03_Resultados/Tablas/07_cuartiles/ninos_cuartiles_especificaciones.{png,csv}`
- `03_Resultados/Figuras/07_cuartiles/ninos_cuartiles_coeficientes.png`
  (especificación 4)

MCO del cambio en el HAZ (OMS) 1997→2000 sobre los cuartiles del alza del
precio nominal del arroz entre comunidades, frente al cuartil 1. Mismas cuatro
especificaciones y controles que `06_ate.R`. 2.421 niños en 294 comunidades.

| Cuartil | Alza media | Comunidades | Niños |
|---|---:|---:|---:|
| 1 | +42 % | 75 | 653 |
| 2 | +61 % | 72 | 585 |
| 3 | +82 % | 74 | 644 |
| 4 | +118 % | 73 | 539 |

Coeficientes frente al cuartil 1 (EE agrupado por comunidad):

| | (1) | (2) | (3) | (4) |
|---|---:|---:|---:|---:|
| Cuartil 2 | −0,224 (0,079) | −0,239 (0,090) | −0,197 (0,090) | −0,189 (0,093) |
| Cuartil 3 | −0,062 (0,083) | −0,084 (0,083) | −0,129 (0,085) | −0,116 (0,094) |
| Cuartil 4 | −0,226 (0,091) | −0,262 (0,089) | −0,315 (0,092) | −0,295 (0,104) |

**Especificación (4)** (la de la figura), con intervalos al 95 % y lo que
predicen las rectas desde el alza media del cuartil 1 (cálculo a partir de esta
tabla y de la de `06_ate`):

| Cuartil | Coeficiente | p | Intervalo al 95 % | Recta de 06_ate (−0,329) | Recta de E-Q (−0,135) |
|---|---:|---:|---|---:|---:|
| 2 | −0,189 | 0,043 | −0,371 a −0,007 | −0,063 | −0,026 |
| 3 | −0,116 | 0,219 | −0,300 a 0,068 | −0,131 | −0,054 |
| 4 | −0,295 | 0,005 | −0,499 a −0,091 | −0,250 | −0,103 |

## Qué dice, en lenguaje intuitivo

- Comparados con los niños de las comunidades donde el arroz subió menos (en
  promedio +42 %), los de los otros tres grupos crecieron menos entre 1997 y
  2000.
- El daño más grande y más claro está en el grupo de mayor alza (+118 % en
  promedio): unas 0,3 desviaciones estándar menos de talla para su edad.
- El orden no es perfecto: el segundo grupo muestra más daño que el tercero.
  Pero cada grupo tiene unas 73 comunidades y los márgenes de error son
  amplios, así que esa inversión puede ser ruido.
- Los tres puntos caen cerca de la recta del efecto promedio, dentro de su
  margen de error. Con esta precisión no se puede distinguir un daño que crece
  de forma pareja con el alza de uno que aparece en cuanto el alza supera la del
  grupo más bajo.

## Por qué importa en el estudio

- **Complementa la pregunta 1:** el efecto promedio de P2.1 no viene de unas
  pocas comunidades con alzas extremas. Los tres cuartiles por encima del más
  bajo muestran menos crecimiento, y el cuartil 4 es distinto de cero en las
  cuatro especificaciones.
- **Sostiene usar la dosis lineal** como medida principal (y en la réplica de
  las interacciones de E-Q, P3.1): los cuartiles no la contradicen.
- **Frente a E-Q:** en el cuartil 4, su recta predice −0,103, en el límite del
  intervalo del coeficiente (−0,499 a −0,091). Es consistente con la nota de
  P2.1 (`05_Notas/06_ate/A_ate_promedio.md`): nuestro efecto es mayor que el
  suyo, con incertidumbre que se traslapa. Difiere de forma atribuible a la
  medida del precio y a los efectos fijos de provincia, por verificar en P2.3.
- **Para el bosque (H3):** el tratamiento binario del bosque compara el tercil
  alto con el bajo. Que el daño esté presente en los cuartiles de arriba hace
  razonable esa comparación.

## Límites e incertidumbre

- Cada cuartil tiene 72 a 75 comunidades: los intervalos son amplios y el
  cuartil 3 no es distinto de cero en ninguna especificación.
- No se hizo una prueba formal de linealidad; la comparación con la recta es
  visual y con los intervalos de cada punto.
- La inversión entre los cuartiles 2 y 3 aparece en las cuatro
  especificaciones, así que no es un efecto de los controles. Puede ser ruido o
  alguna diferencia entre esas comunidades que no se mide aquí.
- Es un contraste entre comunidades con más y menos alza; todas vivieron la
  crisis.

## Historial

- 2026-11-22: creación (P2.2).
