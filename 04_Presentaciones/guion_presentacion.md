# Guion de la presentación final (20 min + 5 de preguntas)

Versión del 22-nov-2026 para presentar el 23-nov. Presentación:
`08_Entregables/presentacion_final.pdf` (presentar desde el PDF: lleva las
fuentes incrustadas). Se construye con
`04_Presentaciones/_fuente/construir_presentacion.py`; el texto completo de
cada lámina está en sus notas del orador. Las cifras salen de
`04_Presentaciones/hallazgos_principales.txt` y de los `.csv` de
`03_Resultados/`.

## Tiempos

| Presentador | Láminas | Segundos |
|---|---|---:|
| Presentador 1 | 1 Portada (45) · 2 Situación (75) · 3 Lo que se sabe (90) · 4 Cómo lo medimos (90) | 300 |
| Presentador 2 | 5 Respuesta 1 (150) · 6 Qué tan sólido (150) | 300 |
| Presentador 3 | 7 El bosque replica el ATE (60) · 8 Respuesta 2 (100) · 9 La única pista (100) · 10 Respuesta 3 (100) | 360 |
| Presentador 4 | 11 Recomendación (110) · 12 Aporte y límites (110) · 13 Cierre (80) | 300 |
| **Total** | | **1.260** (21 min: falta recortar 60 s) |

Fuera de los 20 min: 14 Referencias (APA 7) · 15 separador «Respaldo» · 16 traslape
del bosque causal · 17 forma por cuartiles · 18 especificaciones (con la ecuación
estimada) · 19 interacciones de Elmira y Qaim · 20 calibración · 21 perfil de los
priorizados · 22 edad sin valores extremos · 23 curvas de priorización.

## Las 13 láminas

| # | Título | Figura o elemento |
|---|---|---|
| 1 | ¿A quién golpeó más el arroz caro? | Portada de TIME (19-ene-1998) |
| 2 | El arroz subió un 70 % entre 1997 y 2000, y en unas comunidades mucho más | F1 `f1_alza.png` |
| 3 | Dos estudios con estos datos no coinciden, y nadie ha probado a quién proteger primero | Dos tarjetas + las tres preguntas |
| 4 | Seguimos a 2.421 niños de la IFLS y comparamos comunidades con más y menos alza | Esquema 1997 → alza → 2000 |
| 5 | Replicamos a Elmira y Qaim: donde el arroz subió más, los niños crecieron menos | F2 `f2_efecto_principal.png` |
| 6 | El signo del efecto resiste cinco pruebas de robustez, pero su tamaño cambia | F3 `f3_robustez.png` |
| 7 | Un bosque causal logra replicar el ATE de las especificaciones lineales | F7 `f7_cate_distribucion.png` |
| 8 | Un bosque causal no reproduce la heterogeneidad de las interacciones identificadas por Elmira y Qaim | F4 `f4_grupos.png` |
| 9 | Los menores de 3 años quizá sufrieron más, pero los datos no alcanzan para afirmarlo | F5 `f5_potencia.png` + dos cifras |
| 10 | Un bosque causal no encuentra a los más afectados mejor que una regla simple | F6 `f6_focalizacion.png` |
| 11 | Focalice por comunidad, no por hogar | Hacer / No hacer / Por confirmar |
| 12 | Qué añadimos y qué no podemos afirmar | Dos columnas |
| 13 | Tres preguntas, tres respuestas | Preguntas y respuestas + cierre |

Figuras en `03_Resultados/Figuras/15_figuras_presentacion/` (script
`02_Scripts/15_figuras_presentacion.R`).

## Diez preguntas probables

1. **¿Por qué una regresión y no el bosque causal para el efecto promedio?** La
   regresión da el mismo número que replicamos de Elmira y Qaim (efecto por
   cada duplicación del precio). La pendiente del bosque pondera distinto
   (−0,260 frente a −0,329) y supone un efecto lineal en el alza; el bosque lo
   usamos para buscar diferencias entre niños. *Respaldo: 18.*
2. **¿Es el efecto de la crisis?** No. Todas las comunidades vivieron la crisis;
   medimos el efecto de más alza frente a menos alza, suponiendo que sin esa
   diferencia el cambio en la estatura habría sido igual, dadas las
   características de 1997. *Respaldo: 4 y 5.*
3. **¿Por qué errores agrupados por comunidad?** El alza se asigna por
   comunidad y los niños de una comunidad comparten choques. Agrupados, los
   márgenes de error son 9 a 31 % mayores que los robustos sin agrupar que usan
   Elmira y Qaim. La unidad efectiva son 294 comunidades. *Respaldo: 18.*
4. **¿Y el placebo?** Inconcluso: −0,192 (margen de error 0,117) con
   controles, cerca del 60 % del efecto. No prueba una tendencia previa, pero
   no la descarta; por eso decimos que la dirección es sólida y el tamaño no.
   *Respaldo: 6.*
5. **¿El desgaste es selectivo?** El seguimiento 1997-2000 no depende del alza
   (pendiente −0,003, margen de error 0,017). En 1997 se midió a menos niños
   en el cuartil de más alza, sobre todo entre provincias, sin cambiar la
   composición. *Respaldo: 12; nota `05_Notas/05_base/D_desgaste_segun_alza.md`.*
6. **¿Por qué su efecto es mayor que el de Elmira y Qaim?** Hipótesis no
   probadas: su precio mezcla fuentes distintas en cada año (más ruido, efecto
   atenuado; sin recortar extremos el nuestro baja a −0,207) y no comparan
   dentro de provincia (con efectos fijos de provincia el nuestro pasa de
   −0,24 a −0,34). Los rangos se traslapan. *Respaldo: 5, 6 y 18.*
7. **¿Cómo se concilia con Frankenberg y Thomas (2017)?** Ellos comparan zonas
   urbanas y rurales; nosotros, el alza del precio, que varía sobre todo dentro
   de provincia. Y en nuestros datos tampoco hay diferencia clara entre urbano
   y rural. *Respaldo: 2, 8 y 19.*
8. **¿Por qué terciles dentro de provincia para el bosque causal?** La provincia
   explica el 14,6 % de la variación del alza; con terciles nacionales,
   provincias enteras caerían en un extremo y la comparación no tendría niños
   parecidos en los dos grupos. Así, la probabilidad estimada va de 0,10 a
   0,93. *Respaldo: 16.*
9. **¿Qué significa que la calibración no rechace?** Que no hay evidencia de
   que el orden del bosque causal capte diferencias reales entre niños (0,124,
   margen de error 0,799; p de una cola 0,438). No prueba que el efecto sea
   igual para todos: con 195 comunidades solo veríamos diferencias grandes.
   *Respaldo: 9 y 20.*
10. **¿Qué le recomiendan al cliente?** Vigilar el alza por comunidad y cubrir
    a todos los niños pequeños donde más sube; no usar el bosque causal ni excluir
    por pobreza o zona con esta evidencia. La edad (menores de 3) es una pista
    a confirmar. *Respaldo: 11, 21 y 22.*

## Qué no está verificado

- La fecha de la portada de TIME («19 de enero de 1998») se leyó en la propia
  imagen, de baja resolución.
- «El arroz es el alimento básico de Indonesia» (lámina 2) no tiene cita en
  el proyecto; es conocimiento general.
- La diferencia mínima detectable (lámina 9) es una aproximación normal
  (≈ 2,8 × margen de error), no una simulación de potencia.
