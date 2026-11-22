# Ninguna de las cinco interacciones de Elmira y Qaim se distingue de cero: el alza del arroz se asocia con menos talla en todos los grupos, sin diferencias detectables entre ellos (ninguna pasa Holm)

- **Estado:** vigente
- **Etapa / alcance:** H; contraste entre comunidades con mayor y menor alza
- **Script de origen:** `02_Scripts/09_interacciones_eq.R`
- **Hipótesis relacionada:** réplica de E1-E5 del pre-registro (familia F2). Ninguna diferencia entre grupos: **no se replica** la de urbano ni la de educación de la madre de E-Q (que ellos reportan al 10 %, sin agrupar y sin Holm)
- **Última verificación:** 2026-11-22, con `02_Scripts/09_interacciones_eq.R` (P3.1)

## Evidencia

`03_Resultados/Tablas/09_interacciones_eq/ninos_interacciones_eq.{png,csv}`

MCO del cambio en el HAZ (OMS) 1997→2000 sobre la dosis (cambio proporcional
del precio nominal del arroz en la comunidad de 1997; 1 = +100 %), la dosis × X
y X, con la especificación (4) de `06_ate` (controles de 1997, EF de provincia y
log del precio de 1997). Una interacción a la vez. 294 comunidades en todas.
HAZ por +100 %; EE agrupado por comunidad entre paréntesis, robusto entre
corchetes.

| | X = 1 frente a X = 0 | β1: X = 0 | β2: diferencia | p agrupado | p Holm (F2) | β1 + β2: X = 1 | E-Q β2 (EE robusto) | Niños (X = 1) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| E1 | 0-2 años frente a 3-5 | −0,293 (0,124) | −0,096 (0,207) [0,194] | 0,644 | 1,000 | −0,388 (0,218) | 0,005 (0,066) | 2.421 (1.054) |
| E2 | mujer frente a varón | −0,343 (0,158) | 0,028 (0,183) [0,177] | 0,878 | 1,000 | −0,315 (0,173) | 0,099 (0,073) | 2.421 (1.199) |
| E3 | madre con más que primaria frente a primaria o menos | −0,380 (0,164) | 0,109 (0,232) [0,204] | 0,639 | 1,000 | −0,271 (0,212) | 0,129 (0,075) | 2.328 (824) |
| E4 | pobre frente a no pobre | −0,354 (0,146) | 0,127 (0,261) [0,202] | 0,628 | 1,000 | −0,227 (0,255) | 0,216 (0,180) | 2.419 (584) |
| E5 | urbano frente a rural | −0,324 (0,177) | −0,009 (0,223) [0,194] | 0,968 | 1,000 | −0,333 (0,178) | −0,270 (0,153) | 2.421 (1.012) |

- En la especificación (4), ningún β2 tiene p sin ajustar menor que 0,5 (ni agrupado ni robusto); con Holm
  todos quedan en 1,000.
- Los niños pobres están en 177 comunidades y los urbanos en 170; los demás
  grupos X = 1, en 246 a 278 (`.csv`, columna `comunidades_x1`).
- **Especificación (2)** (sin EF de provincia ni log del precio, más cercana a
  la de E-Q; en el `.csv`, sin familia de Holm): β2 entre −0,093 y 0,135, todos
  con p agrupado ≥ 0,61.
- **E1:** E-Q no dicen qué grupo es la «edad crítica»; X = 1 = 0-2 años es
  **inferencia nuestra** a partir del orden de su fig. 5.

## Qué dice, en lenguaje intuitivo

- En todos los grupos, los niños de comunidades con más alza del arroz crecieron
  menos: el efecto estimado va de −0,23 a −0,39 desviaciones estándar por cada
  vez que el precio se dobla, parecido al promedio (−0,329).
- Pero las diferencias entre grupos (urbanos frente a rurales, niñas frente a
  niños, etc.) son pequeñas frente a su margen de error, que es de unas 0,2
  desviaciones estándar. Con estos datos no se puede decir que el daño fue
  mayor en un grupo que en otro.
- No es lo mismo que «el daño fue igual en todos»: es que no hay precisión para
  distinguirlo.

## Por qué importa en el estudio

- **Pregunta 2 (¿a quién?), réplica:** los dos resultados que E-Q reportan al
  10 % no aparecen aquí.
  - **Urbano:** E-Q −0,270 (EE robusto 0,153); aquí −0,009 (0,223), casi cero. Los
    intervalos se traslapan (el nuestro va de −0,45 a 0,43 y contiene
    su cifra). Difiere, atribuible a la medida del precio (ellos combinan
    fuentes distintas en 1997 y 2000), a los EF de provincia (que absorben la
    diferencia urbano-rural entre provincias) y a la muestra (2.421 frente a
    2.112 niños). Con EE robusto, como E-Q, tampoco aparece (p = 0,963).
    **[REVISIÓN HUMANA]**: es el único resultado de heterogeneidad que E-Q
    destacan en el texto (p. 5); conviene decidir cómo presentarlo.
  - **Madre con educación alta:** mismo signo (menos daño) que E-Q (+0,109
    frente a +0,129), sin distinguirse de cero.
  - Mujer y pobre: mismo signo que E-Q, ninguno significativo, como en E-Q.
  - Edad: E-Q 0,005, aquí −0,096 (0-2 años algo más de daño), ninguno distinto
    de cero.
- **Con el ATE** (`05_Notas/06_ate/A_ate_promedio.md`): consistente. Los β1 y
  β1 + β2 rodean al −0,329 del promedio.
- **Para el cliente:** con una regresión de una variable a la vez no hay base
  para priorizar a ninguno de estos cinco grupos sobre su complemento. Los GATE
  del bosque (P3.3) son la segunda mirada, con otro tratamiento (terciles).

## Límites e incertidumbre

- La potencia es baja: los EE de β2 son de 0,18 a 0,26 HAZ, del orden del efecto
  promedio. Una diferencia del tamaño de la de urbano de E-Q (−0,27) tendría
  p ≈ 0,2 con este EE.
- Una interacción a la vez: cada β2 puede recoger otras diferencias
  correlacionadas con X (por ejemplo, urbano y pobre).
- E3 pierde 93 niños sin dato de la madre y E4, 2 sin gasto.
- Hereda los límites del ATE: placebo inconcluso y tamaño sensible a la cola del
  ΔHAZ (`05_Notas/08_validacion/A_validacion_placebo_robustez.md`).

## Historial

- 2026-11-22: creación (P3.1).
