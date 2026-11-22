# Un alza de +100 % en el precio del arroz se asocia con 0,22 a 0,34 desviaciones estándar menos de talla para la edad entre 1997 y 2000 (1,1 a 1,7 cm), más que el −0,135 de Elmira y Qaim pero con intervalos que se traslapan

- **Estado:** vigente
- **Etapa / alcance:** A; contraste entre comunidades con mayor y menor alza
- **Script de origen:** `02_Scripts/06_ate.R`
- **Hipótesis relacionada:** ninguna de H1-H8 (es la pregunta 1, el efecto promedio)
- **Última verificación:** 2026-11-22, con `02_Scripts/06_ate.R` (P2.1)

## Evidencia

`03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.{png,csv}`

MCO del cambio en el HAZ (OMS) 1997→2000 sobre la dosis: cambio proporcional del
precio nominal del arroz en la comunidad de 1997 (1 = +100 %). 2.421 niños de 0-5
años en 1997, 294 comunidades, en las cuatro columnas.

| | (1) | (2) | (3) | (4) |
|---|---:|---:|---:|---:|
| β (HAZ por +100 %) | −0,217 | −0,238 | −0,339 | −0,329 |
| EE agrupado por comunidad | 0,119 | 0,109 | 0,112 | 0,139 |
| EE robusto sin agrupar (como E-Q) | 0,091 | 0,094 | 0,100 | 0,127 |
| p (EE agrupado) | 0,070 | 0,029 | 0,003 | 0,018 |
| Equivalente aproximado en cm | −1,09 | −1,20 | −1,71 | −1,66 |
| Controles de 1997 | No | Sí | Sí | Sí |
| Efectos fijos de provincia | No | No | Sí | Sí |
| Log del precio de 1997 | No | No | No | Sí |

- **Bosque causal** (mismas X y niños que (4), agrupado por comunidad): pendiente
  promedio −0,260 (EE 0,132). Pondera distinto que MCO; no es el mismo estimando.
- **Intervalos al 95 % (EE agrupado):** (2) de −0,452 a −0,024; (4) de −0,601 a
  −0,057. El de E-Q (−0,135, EE robusto 0,041) va de −0,216 a −0,054.
- **cm:** β multiplicado por 5,03 cm, la desviación estándar media de la talla de
  referencia OMS en 2000 a la edad y el sexo de cada niño. Es una aproximación.
- **Escala ilustrativa** (cálculo a partir de esta tabla y de
  `05_Notas/02_precio_arroz/D_distribucion_precio_arroz.md`): con el alza de la
  comunidad típica (+70 %), la columna (4) implica unos −0,23 HAZ (≈ −1,2 cm).
- Los indicadores de faltante del productor de arroz y del tamaño del hogar
  salen por colinealidad (repiten a otro indicador); no afecta a β.

## Qué dice, en lenguaje intuitivo

- Los niños de las comunidades donde el arroz subió más crecieron menos entre
  1997 y 2000 que los de comunidades donde subió menos. Si el precio se doblaba,
  el niño quedaba en promedio entre 1 y 1,7 cm más bajo de lo esperado para su
  edad, según la especificación.
- El resultado se mantiene al tener en cuenta las características de los hogares
  y las comunidades en 1997, y se hace más grande al comparar solo comunidades de
  la misma provincia.
- El bosque causal, que estima el efecto de otra manera, da una cifra parecida
  (−0,26).
- Es un **contraste entre comunidades** con más y menos alza, no el efecto total
  de la crisis: todas las comunidades vivieron la crisis.

## Por qué importa en el estudio

- **Responde la pregunta 1 (¿dolió?):** sí, en la escala del precio del arroz de
  la comunidad. Es la base para preguntar después a quién le dolió más (H3).
- **Difiere de Elmira y Qaim (2026) en magnitud, misma dirección.** Nuestro β es
  1,6 a 2,5 veces su −0,135, con la misma escala (cambio proporcional nominal),
  la misma cohorte y el mismo periodo. Los intervalos se traslapan. Explicaciones
  posibles, **por verificar**:
  1. **Medida del precio.** Ellos combinan fuentes distintas en 1997 y 2000
     (incluyen el PKK en 1997); su alza tiene mucha más dispersión (media +83 %,
     DE 0,67) que la nuestra (+20 % a +153 % tras winsorizar). Si su medida tiene
     más ruido, su β estaría atenuado hacia cero.
  2. **Efectos fijos de provincia.** Ellos no los usan; aquí β pasa de −0,24 a
     −0,34 al agregarlos.
  Con la información disponible es una diferencia atribuible al diseño, no una
  contradicción. La robustez sin winsorizar y con la dosis solo en kg (P2.3)
  ayuda a probar el punto 1.
- **Frankenberg y Thomas (2017)** no encuentran daño en talla comparando por zona
  (urbano frente a rural). Aquí la exposición es el alza del precio, que varía
  sobre todo dentro de cada provincia. La diferencia es la que el proyecto busca
  reconciliar.
- **Consistente** con `05_Notas/05_base/D_desgaste_segun_alza.md`: esa nota
  anticipaba que los efectos fijos de provincia podían mover el resultado, porque
  la menor cobertura del HAZ de 1997 en las comunidades de mayor alza es sobre
  todo entre provincias.

## Límites e incertidumbre

- La incertidumbre es grande: con 294 comunidades, el intervalo de la columna
  (4) va de −0,60 a −0,06. El orden de magnitud está menos claro que la dirección.
- Sin controles, el resultado no es distinto de cero al 5 % (p = 0,070).
- El salto al agregar los efectos fijos de provincia indica que las provincias
  con más alza difieren en algo que afecta el crecimiento. Dentro de provincia
  la comparación es más limpia, pero no se pueden descartar choques
  simultáneos dentro de cada provincia.
- Los cm son aproximados: usan la desviación estándar media de la referencia, no
  la de cada niño.
- Falta la validación de P2.3: placebo con 1993→1997, sin las comunidades
  entrevistadas en 1998, con pesos, sin winsorizar y sin la cola del cambio en el
  HAZ.

## Historial

- 2026-11-22: creación (P2.1).
