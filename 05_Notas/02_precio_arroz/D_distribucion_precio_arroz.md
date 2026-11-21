# El precio nominal del arroz subió una mediana de 70 % entre 1997 y 2000, con alzas de +20 % a +153 % entre comunidades; el 85 % de esa variación ocurre dentro de cada provincia

- **Estado:** vigente
- **Etapa / alcance:** D; descriptivo
- **Script de origen:** `02_Scripts/02_precio_arroz.R`
- **Hipótesis relacionada:** ninguna (construye el tratamiento de las tres preguntas)
- **Última verificación:** 2026-11-20, con `02_Scripts/02_precio_arroz.R`

## Evidencia

- `03_Resultados/Tablas/02_precio_arroz/comunidades_resumen_precio.{png,csv}`
- `03_Resultados/Figuras/02_precio_arroz/comunidades_distribucion_alza.png`

Escala: cambio proporcional del precio nominal por kg, en la comunidad de
residencia de 1997 (1 = +100 %). Precio = mediana de los reportes del posyandu y
de tiendas y mercados, de todas las calidades.

| Cifra | Valor |
|---|---:|
| Comunidades con precio en 1997 y 2000 | 297 de 312 |
| Solo con reportes en kg en los dos años | 254 |
| Mediana del precio, 1997 → 2000 (Rp/kg) | 1.200 → 2.100 |
| Mediana del alza | 0,700 |
| Cortes de la winsorización p1 / p99 | 0,198 / 1,530 |
| Máximo sin winsorizar | 3,125 |
| Factor litro a kg | 0,833 (142 comunidades-año) |
| Correlación de la dosis con la dosis solo kg | 0,835 |
| R² de la dosis sobre la provincia | 0,146 |
| Comunidades en los terciles alto o bajo (dentro de provincia) | 197 |
| Comunidades con tercil distinto, nacional frente a provincia | 88 |
| Con precio de 1997 levantado en 1998 | 34 |

## Qué dice, en lenguaje intuitivo

Entre 1997 y 2000 el precio del arroz subió en todas partes, pero no lo mismo en
todas: en la comunidad típica subió un 70 %, y entre la comunidad con menos alza
y la de más (sin contar los extremos) va de +20 % a +153 %. Esa diferencia
entre comunidades es la que usa el estudio: compara a los niños de comunidades
donde el arroz subió más con los de comunidades donde subió menos. Casi toda la
diferencia está entre comunidades de la misma provincia, no entre provincias.
Por eso el bosque compara el tercio de más alza con el tercio de menos alza
dentro de cada provincia.

## Por qué importa en el estudio

- Es el tratamiento de las tres preguntas: la dosis (pregunta 1), los cuartiles
  (forma) y los terciles (bosque).
- Que el 85 % de la variación esté dentro de provincia permite descontar los
  choques regionales (sequía de El Niño, humo de 1997), que son la amenaza
  principal (`CLAUDE.md` §5.3), sin quedarse sin variación.
- Las medianas coinciden con la revisión de datos (síntesis §7.6: 1.200 Rp/kg en
  1997 en tiendas y PKK; 2.000 en 2000 en posyandu y tiendas). La de 2000 da
  2.100 porque ahora entran los litros convertidos.
- **Difiere (atribuible)** de la cola de +729 % que anotó la sesión del 20-nov
  (`CLAUDE.md` §11), con otra construcción que no quedó en un script.
  Aquí el máximo por comunidad es +312 %: la mediana de varios reportes amortigua
  los atípicos. Que esa sea la causa no está verificado, pero no cambia nada
  porque la cola se winsoriza.
- La comparación con el −0,135 HAZ por +100 % de Elmira y Qaim (2026) usa esta
  misma escala (cambio proporcional nominal), pero sus fuentes de 1997 incluyen
  el PKK: la réplica es aproximada (registro §3).

## Límites e incertidumbre

- Los reportes por litro (24 % de los reportes del posyandu en 1997 y 27 % en 2000) se convierten con un
  solo factor para todo el país. Si la densidad del arroz varía entre regiones,
  hay error de medición. La correlación con la dosis solo kg es 0,835: la
  robustez con kg (254 comunidades) es necesaria.
- El precio de 2000 no es el pico de 1998: mide el alza persistente, con error,
  lo que sesga hacia cero.
- 15 comunidades no tienen precio en algún año y salen del análisis.
- Los terciles dentro de provincia se cortan con 11 a 51 comunidades por
  provincia: en las provincias chicas los cortes son ruidosos, y el «alto» de
  una provincia puede tener menos alza que el «bajo» de otra.
- En 34 comunidades el precio de 1997 es de enero o febrero de 1998, ya con la
  crisis encima. Hay una robustez que las excluye.

## Historial

- 2026-11-20: creación (P1.2). Decisiones de Santiago en la sesión: litros
  convertidos a kg, unión de 38 comunidades con precio de 1998, terciles dentro
  de provincia.
