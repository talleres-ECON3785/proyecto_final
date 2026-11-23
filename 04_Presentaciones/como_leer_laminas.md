# Cómo leer cada figura

Textos que se quitaron de las láminas: «Cómo leer» de cada figura y aclaraciones para el orador. Los genera `04_Presentaciones/_fuente/construir_presentacion.py`; no se editan a mano.

## Lámina 2

- Crisis financiera de fin de siglo afecta a Indonesia particularmente fuerte frente a la región.
- El arroz, alimento pilar de la canasta básica, tuvo fuertes incrementos en su precio y de forma desigual en el territorio
- Incremento mediano de 70%.
- Cada barra cuenta comunidades según cuánto subió allí el precio del arroz (297 comunidades).
- En Colombia, el 74% de los hogares consume arroz y los hogares de ingresos bajos dedican el 2.51% de su gasto a este frente a 0.21% de los hogares ricos (más de 10 veces más). Por ende, en la coyuntura actual donde esperamos un fenómeno del niño muy fuerte, es importante entender los posibles efectos de un encarecimiento repentino del arroz sobre la altura de los niños, prestando especial atención a efectos diferenciales para los individuos más vulnerables.

## Lámina 3

- La literatura ha evaluado los efectos de la crisis sobre la estatura, pero las conclusiones entran en conflicto
- No se ha estudiado a quién se debería proteger primero.

## Lámina 4

- Usamos la Indonesia Family Life Survey como nuestra fuente de datos. Es un panel longitudinal que sigue a las mismas personas a través de varias rondas.
- Todo lo de la slide
- Finalmente, fijamos los grupos y las pruebas estadísticas antes de ver los resultados, para evitar reportar un resultado significativo por azar.

## Lámina 5

- Gráfica da el ATE identificado por Elmira y Qaim y nuestra replicación con la ecuación de la slide.
- Diferimos en magnitud pero los intervalos se cruzan, coincidimos en dirección y significancia (es distinto de 0)

Cómo leer: cada punto es el efecto promedio; la línea, su rango plausible al 95 %. Más a la izquierda = más daño. 2.421 niños en 294 comunidades.

## Lámina 6

Cómo leer: todas las estimaciones quedan a la izquierda de cero

- el placebo debería estar en cero.
- El placebo no se distingue de 0, pero por el intervalo no descarta tendencia previa.

Solo por si preguntan:


- Principal: misma de la pasada
- 1998: hubo mediciones hechas en 1998, estimación si las quitamos de la muestra porque ya había empezado la crisis.
- Pesos: pesos de la encuesta para representación nacional
- Sin recortar alzas: sin quitar los cambios más extremos de precios
- Solo precio por kilo: se quitan mediciones en litros que se convirtieron
- Sin cambios extremos: quita niños con cambios de HAZ outliers
- Placebo: Diferencia entre 1993 y 97 para la cohorte con la misma edad en el 93, debería ser 0.

## Lámina 7

Cómo leer: cada barra cuenta niños según el efecto que el bosque predice para ellos; la línea punteada es el promedio. La dispersión mezcla diferencias reales y ruido de estimación: la prueba de calibración no los distingue.

- Nos interesa expandir la investigación usando bosques causales para identificar y corroborar heterogeneidades.
- Cambiamos la identificación del tratamiento a comparar individuos en comunidades en el decil de mayor incremento con aquellos en el de menor incremento - necesario tener un tratamiento binario o categórico para usar focalización en bosques causales.
- Distribución de CATEs segun un bosque causal - recupera bien el resultado de un MCO equivalente.
- Algunas observaciones presentan valores inferiores a -0.4 que nos dan indicios de la posibilidad de focalizar.

## Lámina 8

Cómo leer: punto = daño en cada grupo; línea = rango plausible. Todos los grupos quedan a la izquierda de cero; tampoco confirmamos un daño mayor en zonas urbanas.

- Revisamos si el bosque causal replica las interacciones que Elmira y Qaim habían identificado: edad, sexo, zona, si es comprador o vendedor de arroz, educación de la madre y pobreza.
- Solo la edad parece sugerir diferencias entre mayores de 3 años y menores de dos años

## Lámina 9

Cómo leer: la barra naranja es la menor diferencia entre dos grupos que estos datos detectarían (aproximada). La parte oscura llega al contraste más fácil de detectar (0,36) y la clara, al más difícil (0,44): es un rango entre los seis contrastes, no un intervalo de confianza. Es el doble del daño promedio.

- Como análisis exploratorio de ese resultado de bosques causales, revisamos los efectos heterogéneos por edad.
- Los menores de 2 años parecen tener mayor afectación a su estatura, pero no tenemos poder estadístico, dado el tamaño de muestra y la agrupación por comunidades, para concluir que la diferencia con respecto a los niños entre 3 y 5 años sea significativa.

## Lámina 10

Cómo leer: si la agencia atiende primero a quien señala cada regla, ¿esos niños sufrieron más que el promedio? La calibración del bosque tampoco encuentra diferencias entre niños.

- Finalmente, probamos la utilidad del bosque causal como herramienta de focalización, y encontramos que no tiene mejor desempeño que otros criterio o incluso, que el azar

## Lámina 11

- En conclusión, no podemos concluir que se deba focalizar un grupo específico, más allá de priorizar a quienes más les aumenta el precio.

## Resto

12 y 13 se dice lo que está
