# Vivir en una comunidad del tercil alto del alza (frente al bajo) se asocia con −0,18 HAZ entre 1997 y 2000, según el bosque causal y MCO por igual; el traslape cumple la regla, pero las X de 1997 predicen bien el tercil

- **Estado:** vigente
- **Etapa / alcance:** H (insumo de los GATE); contraste entre comunidades del tercil alto y bajo del alza; la figura del traslape es descriptiva
- **Script de origen:** `02_Scripts/10_bosque.R`
- **Hipótesis relacionada:** ninguna de E1-E5 ni G1-G6 (es el bosque sobre el que se calculan los GATE de P3.3)
- **Última verificación:** 2026-11-22, con `02_Scripts/10_bosque.R` (P3.2)

## Evidencia

- `03_Resultados/Tablas/10_bosque/ninos_bosque_ate.{png,csv}`
- `03_Resultados/Figuras/10_bosque/ninos_bosque_traslape.png`

Muestra: 1.602 niños en 195 comunidades (tercil alto: 731 niños en 93
comunidades; bajo: 871 en 102). Quedan fuera 819 niños del tercil medio en 99
comunidades. Terciles del alza dentro de provincia.

| Estimador | Efecto en HAZ (EE agrupado) | IC 95 % | p |
|---|---:|---|---:|
| Bosque causal (AIPW, 4.000 árboles, agrupado por comunidad) | −0,184 (0,065) | −0,312 a −0,056 | 0,005 |
| MCO, especificación (4) con el tratamiento binario | −0,188 (0,079) | −0,343 a −0,033 | 0,018 |

- **Traslape:** `W.hat` (probabilidad estimada de estar en el tercil alto) va de
  0,101 a 0,933. Ningún niño queda fuera de [0,05; 0,95], así que no hizo falta
  el bosque de robustez.
- Pero las X de 1997 **predicen bien** el tercil: mediana de `W.hat` 0,155 en el
  tercil bajo y 0,719 en el alto (salida de consola de `10_bosque.R`). En la
  figura, buena parte del tercil bajo se concentra entre 0,10 y 0,17, donde hay
  pocos niños del tercil alto.

## Qué dice, en lenguaje intuitivo

- Los niños de las comunidades donde el arroz subió más (el tercio de mayor alza
  dentro de su provincia) crecieron en promedio 0,18 desviaciones estándar menos
  que los del tercio de menor alza. El bosque causal y una regresión lineal dan
  casi la misma cifra.
- Es otra forma de medir el mismo contraste de la pregunta 1: en lugar de «por
  cada vez que el precio se dobla», compara a los extremos.
- La figura del traslape muestra que las características de 1997 de los hogares
  y las comunidades ya anticipaban bastante en qué tercio iba a caer cada
  comunidad. Hay niños comparables en los dos grupos, pero no en todas las
  zonas de la distribución por igual.

## Por qué importa en el estudio

- **Consistente con la pregunta 1:** el alza media entre comunidades es +107 %
  en el tercil alto y +48 % en el bajo (columnas `dosis_media_*` del `.csv`),
  una diferencia de 0,59 en la escala de la dosis. Con el −0,329 por +100 % de
  `05_Notas/06_ate/A_ate_promedio.md`, la recta predice 0,59 × −0,329 ≈ −0,19,
  muy cerca del −0,18 de aquí (cálculo a partir de las dos tablas).
- **Frente a E-Q:** no es comparable en magnitud (otro estimando, sin dosis).
- **Para la pregunta 2:** este bosque es la base de los seis GATE (P3.3). Que
  su ATE coincida con el MCO sugiere que el ajuste por X no está dominado por
  pocas observaciones extremas.

## Límites e incertidumbre

- 195 comunidades: el N efectivo es ese, no 1.602.
- La separación de `W.hat` indica que el tercil depende de cosas observables de
  1997 (en la importancia de variables del bosque, que no es un efecto,
  aparecen la edad, la educación de la madre, el tamaño del hogar, una
  provincia y el log del precio de 1997). El supuesto de que, dadas esas X, el
  tercil es como asignado al azar pesa más donde hay menos traslape.
- Hereda los límites del ATE (placebo inconcluso; tamaño sensible a la cola del
  ΔHAZ), `05_Notas/08_validacion/A_validacion_placebo_robustez.md`.

## Historial

- 2026-11-22: creación (P3.2).
