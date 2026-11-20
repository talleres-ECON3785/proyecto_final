# 00 · Resumen (versión 5): Proyecto final ECON-3785 · ¿A quién golpeó más el arroz caro?

Fecha: 20-nov-2026 · Estado: plan para el equipo y para la asesoría de la semana 15. Reemplaza la v4 (17-nov, en `_obsoleto/00_resumen_v4.md`). El detalle operativo está en `PLAN.md`; los documentos `01`-`06` siguen en v4 y se leen con los cambios de esta tabla.

## En una frase

Con la IFLS, replicar el efecto promedio del alza del precio del arroz de 1997-98 sobre la **estatura infantil** (ΔHAZ 1997→2000, niños de 0-5 años en 1997; Elmira y Qaim 2026), ver su forma, estimar **a quién golpeó más** con subgrupos pre-declarados y probar si una priorización con bosques causales supera a reglas simples de focalización.

## Qué cambió en la versión 5

| Punto | Cambio |
|---|---|
| Alcance | **Solo estatura.** Fuera, por ahora, la escolaridad 2014 (antes resultado primario), la cognición, la estatura adulta y la salud mental. Decisión del equipo |
| Arco | Tres preguntas: ¿dolió? (`feols`), ¿a quién? (GATE pre-declarados con puntajes AIPW del bosque y Holm), ¿el bosque supera a las reglas simples? (calibración y RATE) |
| Tratamiento | Cuatro versiones: T1 réplica E-Q (cambio **proporcional**, no Δlog; todas las fuentes), T2 dosis limpia (principal), T3 cuartiles, T4 terciles para el bosque (`PLAN.md` H1) |
| Réplica | Con `feols` (panel con EF individuales ≡ primeras diferencias). La pendiente promedio de `grf` continuo es otro estimando: solo una fila de robustez |
| No linealidad | Nueva: cuartiles del alza y spline con `feols`. No con bosques (suponen un efecto lineal en W dado x) |
| Validación | Placebo de tendencias previas con la cohorte de 0-5 años en 1993; desgaste según el alza; errores agrupados por provincia como robustez |
| `grf` | Verificado en 2.6.1: RATE nativo solo con W binario; `lm_forest` sin herramientas de inferencia |

## Conclusiones que siguen vigentes

1. **El efecto promedio en talla está en disputa.** E-Q: −0,135 HAZ por +100 % de precio nominal (p. 1, 5). F-T 2017: sin daño en estatura, con la zona urbana como exposición (p. 12). Un nulo bien documentado es un resultado válido.
2. **Se identifica un contraste (más alza frente a menos alza), no el efecto de la crisis.** La amenaza principal son los choques simultáneos (sequía, humo).
3. **La heterogeneidad es difícil de detectar con unos cientos de comunidades.** Los GATE pre-declarados son el núcleo; si la calibración no rechaza, se dice «no hay evidencia de heterogeneidad más allá de las reglas simples», que también le sirve al cliente.
4. **El cliente necesita saber a quién proteger primero** con variables que observa.

## Decisiones del equipo (con recomendación)

| Decisión | Estado |
|---|---|
| Cliente | Agencia tipo PMA (recomendación) |
| Alcance: solo estatura | Decidido por el equipo (20-nov) |
| Tratamiento T1-T4 y réplica con `feols` | Recomendado el 20-nov; falta confirmación del equipo |
| Terciles nacionales o dentro de provincia | Lo decide la prueba 1 |
| GATE pre-declarados (edad primero) | Por fijar por escrito antes de correr el bosque |
| Lenguaje | R para todo con `haven`, o Python solo para construir bases |

## Riesgos

- **Tiempo.** No se ha corrido nada y el precio no existe: bloquea todo.
- **Potencia** para la heterogeneidad (~208 comunidades con terciles).
- **Medición** del tratamiento (sin PKK en 2000; 27 comunidades levantadas en 1998) y del HAZ (estándar OMS hasta los 60 meses y referencia después).
- **Desgaste** entre 1997 y 2000 posiblemente relacionado con el alza.

## Qué no está verificado

- Ningún número sale de estimaciones propias.
- El apéndice de E-Q (controles, deflactor, agrupamiento de errores) no se ha revisado.
- La simulación sobre la potencia usa datos inventados y una sola semilla.
- Que haya suficiente cohorte de 0-5 años en 1993 con talla en 1993 y 1997 para el placebo.
