# El seguimiento de 1997 a 2000 no depende del alza del precio, pero en las comunidades de mayor alza hay menos niños con talla válida en 1997 (76 % frente a 82-84 %)

- **Estado:** vigente
- **Etapa / alcance:** D; descriptivo
- **Script de origen:** `02_Scripts/05_base.R`
- **Hipótesis relacionada:** ninguna (validez de la pregunta 1: desgaste según el alza)
- **Última verificación:** 2026-11-20, con `02_Scripts/05_base.R`

## Evidencia

- `03_Resultados/Tablas/05_base/ninos_desgaste_alza.{png,csv}`
- `03_Resultados/Tablas/05_base/ninos_desgaste_alza_pendientes.csv`

Población: niños de 0-5 años en 1997 con comunidad IFLS y precio del arroz en
ella (3.191 niños, 297 comunidades). Cuartiles de la dosis (cambio proporcional
del precio nominal 1997→2000) entre comunidades.

| Alza | Niños en 1997 | Con HAZ en 1997 | Con HAZ en 2000, de los medidos en 1997 | En la base |
|---|---:|---:|---:|---:|
| Cuartil 1 | 843 | 82,3 % | 94,1 % | 653 (77,5 %) |
| Cuartil 2 | 752 | 84,3 % | 92,3 % | 585 (77,8 %) |
| Cuartil 3 | 839 | 82,7 % | 92,8 % | 644 (76,8 %) |
| Cuartil 4 | 757 | 75,8 % | 93,9 % | 539 (71,2 %) |
| Todos | 3.191 | 81,4 % | 93,3 % | 2.421 (75,9 %), 294 comunidades |

Pendientes sobre la dosis (MCO, escala: probabilidad por +100 % de alza; EE
agrupado por comunidad):

| Paso | Pendiente | EE | p |
|---|---:|---:|---:|
| Quedar en la base | −0,087 | 0,037 | 0,019 |
| Tener HAZ válido en 1997 | −0,090 | 0,038 | 0,018 |
| Tener HAZ en 2000, de los medidos en 1997 | −0,003 | 0,017 | 0,857 |

## Qué dice, en lenguaje intuitivo

De los niños que se midieron bien en 1997, alrededor del 93 % se vuelve a medir
en 2000, y esa proporción es casi la misma en las comunidades donde el arroz
subió poco y en las que subió mucho. El alza no hizo que se perdiera más a unos
niños que a otros entre 1997 y 2000.

La diferencia está antes: en las comunidades del cuartil de mayor alza, menos
niños tienen una talla válida en 1997 (76 % frente a 82-84 % en los demás). Eso
pasó antes de que el precio subiera, así que no puede ser un efecto del alza.
Pero hace que la muestra de esas comunidades sea algo más pequeña y quizá
distinta.

## Por qué importa en el estudio

- **Sostiene la pregunta 1** en su punto más débil: si el alza hubiera hecho
  perder más niños entre 1997 y 2000 (por muerte, migración o falta de medición),
  el ATE estaría sesgado. Con esta población no se ve: la pendiente es −0,003
  (EE 0,017).
- **Consistente** con `05_Notas/01_tracks/D_cohortes_desgaste.md` (desgaste
  1997-2000 pequeño), que dejaba esta prueba para P1.5.
- **Matiza** esa nota: la selección que importa ocurre en la medición de 1997, y
  se concentra en las comunidades de mayor alza. Si los niños sin talla válida en
  1997 son distintos (más pobres, más rurales), la base sobrerrepresentaría en el
  cuartil 4 a los niños medidos con éxito. La pregunta es si esto sesga el
  contraste, no si el alza causó la pérdida.

## Límites e incertidumbre

- No se sabe todavía **por qué** el cuartil 4 tiene menos talla válida en 1997:
  medición no hecha, fecha de nacimiento faltante o HAZ fuera de ±6. Tampoco si
  coincide con las comunidades con campo en 1998 (34 con precio levantado en
  1998). Hay que verificarlo antes de H2: descomponer «sin HAZ en 1997» por
  motivo y por cuartil, y comparar las características de 1997 de los niños con
  y sin HAZ en ese año, según el alza.
- La pendiente para quedar en la base (−0,087) se suma a lo que P2.3 ya prevé
  (desgaste según el alza, con pesos, sin las comunidades de 1998).
- Son pendientes descriptivas con 297 comunidades; un p de 0,018 en una de
  varias pruebas de validación no se corrige por comparaciones múltiples.

## Historial

- 2026-11-20: creación (P1.5).
