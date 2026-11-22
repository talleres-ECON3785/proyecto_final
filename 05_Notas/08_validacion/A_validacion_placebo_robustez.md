# El efecto del alza del arroz es negativo en todas las variantes, pero su tamaño va de −0,20 a −0,50 HAZ y el placebo no permite descartar una tendencia previa: la dirección es robusta, el tamaño no

- **Estado:** vigente
- **Etapa / alcance:** A; placebo y contraste entre comunidades con mayor y menor alza
- **Script de origen:** `02_Scripts/08_validacion.R`
- **Hipótesis relacionada:** ninguna de H1-H8 (validación de la pregunta 1). Placebo: **inconcluso**
- **Última verificación:** 2026-11-22, con `02_Scripts/08_validacion.R` (P2.3)

## Evidencia

### Placebo

`03_Resultados/Tablas/08_validacion/ninos_placebo.{png,csv}`

Cohorte de 0-5 años en 1993 con HAZ válido en 1993 y 1997. MCO del cambio en el
HAZ 1993→1997 (antes del alza) sobre la dosis principal (alza proporcional del
precio nominal 1997→2000, winsorizada) de su comunidad. EE agrupado por la
comunidad asignada.

| Comunidad asignada | Controles | β (EE) | p | Niños | Comunidades |
|---|---|---:|---:|---:|---:|
| 1997 | ninguno | −0,097 (0,123) | 0,432 | 2.221 | 285 |
| 1997 | edad, sexo y EF de provincia | −0,192 (0,117) | 0,102 | 2.221 | 285 |
| 1993 | ninguno | −0,120 (0,126) | 0,342 | 2.343 | 286 |
| 1993 | edad, sexo y EF de provincia | −0,194 (0,117) | 0,097 | 2.343 | 286 |

### Robustez

`03_Resultados/Tablas/08_validacion/ninos_robustez.{png,csv}`

Especificación (4) del efecto promedio (controles de 1997, EF de provincia y log
del precio de 1997), cambiando una cosa a la vez. EE agrupado por comunidad.

| Variante | β (EE) | p | Niños | Comunidades |
|---|---:|---:|---:|---:|
| Principal | −0,329 (0,139) | 0,018 | 2.421 | 294 |
| Sin comunidades con precio de 1998 ni niños medidos en 1998 | −0,378 (0,156) | 0,016 | 2.178 | 259 |
| Con pesos de la evaluación de salud de 2000 (versión a) | −0,504 (0,161) | 0,002 | 2.421 | 294 |
| Alza sin winsorizar | −0,207 (0,165) | 0,211 | 2.421 | 294 |
| Alza con precios solo en kg | −0,317 (0,127) | 0,013 | 2.101 | 251 |
| Sin los niños con \|ΔHAZ\| > 3 | −0,197 (0,106) | 0,064 | 2.311 | 294 |

- **Pesos:** primero se probó el peso longitudinal de persona de 2000 (versión
  a), pero solo era positivo para 932 de los 2.421 niños (probablemente
  porque es un peso para quienes ya estaban en 1993, y la mayoría de la
  cohorte nació después). Se
  cambió al peso transversal de la evaluación de salud de 2000, positivo para
  los 2.421.
- El desgaste según el alza no se repite aquí: está en
  `05_Notas/05_base/D_desgaste_segun_alza.md` (no depende del alza entre 1997 y
  2000).

## Qué dice, en lenguaje intuitivo

- **Placebo.** Se tomaron niños que eran pequeños en 1993 y se miró cuánto
  crecieron entre 1993 y 1997, antes de que subiera el arroz. Si las
  comunidades con más alza después no tenían nada distinto antes, ese
  crecimiento no debería tener relación con el alza. Sin controles la relación
  es pequeña y no se distingue de cero. Con controles tampoco se distingue de
  cero, pero es cerca del 60 % del efecto principal. Es decir: no hay
  prueba de una tendencia previa, pero tampoco se puede descartar.
- **Robustez.** En todas las variantes, los niños de comunidades con más alza
  crecieron menos. Lo que cambia es cuánto: desde −0,20 (sin los niños con
  cambios extremos de talla, o con el alza sin recortar los extremos) hasta
  −0,50 (con pesos).
- **Mensaje honesto para el cliente:** el alza del arroz se asocia con menos
  crecimiento de forma consistente, pero el tamaño exacto del daño es incierto
  y una parte podría venir de diferencias previas entre comunidades.

## Por qué importa en el estudio

- **Matiza la nota de P2.1** (`05_Notas/06_ate/A_ate_promedio.md`): la dirección
  se sostiene, pero el −0,329 no debe presentarse como una cifra precisa.
- **Frente a E-Q (−0,135):** sin winsorizar, el efecto baja a −0,207, más cerca
  de su cifra. Es consistente con la explicación de P2.1 (una medida del precio
  con más extremos o más ruido acerca el efecto a cero), aunque no lo prueba:
  no es su medida del precio.
- **Cola del ΔHAZ:** sin esos 110 niños el efecto baja 40 % (de −0,329 a
  −0,197). La nota de desgaste esperaba que la cola moviera sobre todo la
  precisión, no el estimando, porque su proporción no depende del alza; aquí
  también mueve el tamaño. Por decisión tomada **antes de ver el efecto**
  (registro §5, P1.6) la cola se mantiene en lo principal y se reportan las dos
  cifras. Cambiarla ahora sería escoger la especificación por el resultado.
- **Pesos:** el efecto ponderado (−0,504) es mayor que el sin ponderar. La
  muestra de la IFLS sobrerrepresenta zonas urbanas y provincias pequeñas; un
  efecto mayor con pesos sugiere que el daño podría ser distinto en los grupos
  que la muestra sub- o sobrerrepresenta. Es un indicio para la pregunta 2 (a
  quién), no un resultado.
- **Para la presentación:** el placebo es la pregunta que más probablemente
  haga un evaluador. Conviene mostrarlo tal cual, como inconcluso, junto con la
  tabla de robustez.

## Límites e incertidumbre

- El placebo no tiene los mismos controles que la especificación (4): para la
  cohorte de 1993 no se construyeron las características de 1997. La comparación
  de magnitudes es aproximada.
- Las variantes no son independientes (misma base) y no hay corrección por
  comparaciones múltiples; se leen como sensibilidad, no como pruebas.
- Con 251 a 294 comunidades, los errores de cada variante son de 0,11 a 0,17
  HAZ: las diferencias entre variantes caben, en buena parte, dentro de esa
  incertidumbre.
- Ninguna variante corrige una tendencia previa; para eso haría falta otro
  diseño (por ejemplo, comparar con la cohorte de 1993 en la misma regresión).

## Historial

- 2026-11-22: creación (P2.3).
