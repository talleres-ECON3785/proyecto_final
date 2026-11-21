# El seguimiento de 1997 a 2000 no depende del alza; la menor cobertura del HAZ de 1997 en las comunidades de mayor alza viene sobre todo de diferencias entre provincias y no cambia la composición de la muestra según el alza

- **Estado:** vigente
- **Etapa / alcance:** D; descriptivo
- **Script de origen:** `02_Scripts/05_base.R`
- **Hipótesis relacionada:** ninguna (validez de la pregunta 1: desgaste según el alza)
- **Última verificación:** 2026-11-20, con `02_Scripts/05_base.R` (revisión P1.6)

## Evidencia

Población: niños de 0-5 años en 1997 con comunidad IFLS y precio del arroz en
ella (3.191 niños, 297 comunidades). Cuartiles de la dosis (cambio proporcional
del precio nominal 1997→2000) entre comunidades.

**Retención por cuartil** (`03_Resultados/Tablas/05_base/ninos_desgaste_alza.{png,csv}`):

| Alza | Niños en 1997 | Con HAZ en 1997 | Con HAZ en 2000, de los medidos en 1997 | En la base |
|---|---:|---:|---:|---:|
| Cuartil 1 | 843 | 82,3 % | 94,1 % | 653 (77,5 %) |
| Cuartil 2 | 752 | 84,3 % | 92,3 % | 585 (77,8 %) |
| Cuartil 3 | 839 | 82,7 % | 92,8 % | 644 (76,8 %) |
| Cuartil 4 | 757 | 75,8 % | 93,9 % | 539 (71,2 %) |
| Todos | 3.191 | 81,4 % | 93,3 % | 2.421 (75,9 %), 294 comunidades |

**Pendientes sobre la dosis** (`ninos_desgaste_alza_pendientes.csv`; MCO,
probabilidad por +100 % de alza, EE agrupado por comunidad):

| Paso | Sin EF de provincia | Con EF de provincia |
|---|---:|---:|
| Quedar en la base | −0,087 (0,037; p = 0,019) | −0,045 (0,032; p = 0,161) |
| Evaluación de salud en 1997 | −0,062 (0,032; p = 0,051) | −0,023 (0,027; p = 0,398) |
| HAZ válido en 1997 | −0,090 (0,038; p = 0,018) | −0,045 (0,033; p = 0,165) |
| HAZ en 2000, de los medidos en 1997 | −0,003 (0,017; p = 0,857) | −0,004 (0,018; p = 0,821) |

**Motivo del HAZ faltante en 1997** (`ninos_haz1997_motivos.{png,csv}`; % de los
niños de cada cuartil, motivos excluyentes):

| Alza | Sin evaluación de salud | Evaluado sin talla | Sin fecha | Fuera de ±6 |
|---|---:|---:|---:|---:|
| Cuartiles 1-3 | 10,2-11,6 | 1,5-1,7 | 0,6-1,4 | 3,1-3,6 |
| Cuartil 4 | 16,0 | 4,4 | 0,8 | 3,0 |

**Balance** (`ninos_haz1997_balance.{png,csv}`): la diferencia entre niños con
y sin HAZ en 1997 en pobre, urbano, madre con más que primaria, comprador neto y
mujer **no cambia con el alza** dentro de provincia. Las interacciones van de
−0,073 a +0,085, con p entre 0,211 y 0,744. Los niños sin HAZ en 1997 son algo
más urbanos (47,2 % frente a 41,6 %) y algo más pobres (28,9 % frente a 25,2 %),
en todos los niveles de alza.

**Cola del cambio en el HAZ** (`ninos_dhaz_cola.{png,csv}` y
`ninos_dhaz_cola_perfil.csv`): 110 de 2.421 niños (4,5 %) con |ΔHAZ| > 3, y 272
(11,2 %) con |ΔHAZ| > 2. Por cuartil, la cola de más de 3 va de 3,8 % a 6,2 %,
sin orden con el alza. Quienes están en ella tenían 21,6 meses en 1997 (frente a
39,9) y un HAZ medio de −0,425 en 1997 (frente a −1,827), que pasa a −1,351 en
2000.

## Qué dice, en lenguaje intuitivo

- **El seguimiento no depende del alza.** De los niños medidos bien en 1997,
  alrededor del 93 % se vuelve a medir en 2000, igual donde el arroz subió poco
  y donde subió mucho.
- **La medición de 1997 sí cubrió menos niños en las comunidades de mayor
  alza.** Sobre todo porque a más niños no se les hizo la evaluación de salud
  (16 % frente a 10-12 %). Esto pasó antes del alza, así que no es un efecto del
  precio.
- **Esa diferencia viene sobre todo de las provincias.** Las provincias con
  menos cobertura de medición son también las que tuvieron más alza. Al comparar
  comunidades de la misma provincia, la brecha se reduce a la mitad y deja de
  distinguirse de cero.
- **Los niños que faltan no son distintos según el alza.** Son algo más urbanos
  y algo más pobres que los medidos, pero esa diferencia es la misma en todos los
  niveles de alza. La muestra se achica en las comunidades de mayor alza, pero no
  cambia de composición.
- **La cola del cambio en el HAZ parece error de medición.** Unos pocos bebés
  tienen cambios enormes en tres años, que se explican mejor por una talla o
  una edad mal registradas en 1997. Ese ruido no se concentra en ningún nivel de
  alza.

## Por qué importa en el estudio

- **Sostiene la pregunta 1:** el alza no hizo perder más niños entre 1997 y 2000
  (pendiente −0,003, EE 0,017).
- **Implicación para H2:** la columna con efectos fijos de provincia (P2.1,
  especificación 3) y los terciles dentro de provincia del bosque absorben la
  mayor parte de la selección en la medición de 1997. Si el ATE cambia mucho al
  agregar efectos fijos de provincia, esta es una de las explicaciones que hay
  que considerar.
- **Cola:** por decisión del 20-nov (registro §5) se mantiene en la estimación
  principal, con robustez sin |ΔHAZ| > 3 en P2.3. Como no depende del alza,
  debería mover sobre todo la precisión, no el estimando.
- **Consistente** con `05_Notas/01_tracks/D_cohortes_desgaste.md` (desgaste
  1997-2000 pequeño).

## Límites e incertidumbre

- **Lo que sigue fuera del alcance de esta revisión:**
  - Dentro de provincia queda una pendiente de −0,045 en la cobertura de 1997
    que no es distinta de cero con 297 comunidades, pero tampoco se puede
    descartar.
  - El balance mira solo cinco características, y no se pueden revisar las no
    observadas.
- Son pruebas de validación sin corrección por comparaciones múltiples.
- No se exportó la cobertura por provincia ni el cruce con las 34 comunidades
  con precio de 1998; sale de una exploración en consola, no de
  `03_Resultados/`.

## Historial

- 2026-11-20: creación (P1.5).
- 2026-11-20: revisión P1.6. Se agregan las pendientes con efectos fijos de
  provincia, los motivos del HAZ faltante, el balance y la cola del ΔHAZ. El
  título pasa a decir que la brecha de 1997 es sobre todo entre provincias.
