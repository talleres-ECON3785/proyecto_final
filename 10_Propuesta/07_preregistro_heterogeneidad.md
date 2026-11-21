# 07 · Pre-registro de la heterogeneidad (pregunta 2) y de la focalización (pregunta 3)

> **Fijado el 20-nov-2026, antes de construir el tratamiento y de correr cualquier
> estimación** (tarea P1.3 de `PLAN.md`). Este documento no se edita después de
> ver resultados: si algo cambia, se agrega una sección "Desviaciones" al final,
> con fecha y razón, y el texto original se conserva.
> Resultado: ΔHAZ 1997→2000 de los niños de 0-5 años en 1997. Convención:
> τ < 0 = daño (menos HAZ). «Más daño» = τ más negativo.

## 1. Las interacciones de Elmira y Qaim (2026) que replicamos

E-Q estiman una interacción binaria a la vez (ec. 2, p. 4):
`N_ihjt = β1 (C_j × T_t) + β2 (C_j × T_t × X_ih) + γ1 X'_ihj + λ_i + T_t + ε`.
β1 es el efecto en el grupo de referencia (X = 0), β2 la diferencia entre
grupos y β1 + β2 el efecto en el grupo X = 1 (p. 4). Cinco variables binarias
(p. 4; fig. 5, p. 6), todas con precio nominal:

| # | Interacción (cuadro A4) | Grupos de la fig. 5 | Definición en E-Q | HAZ, cuadro A4: β2 (EE) | Retraso en talla, cuadro A5: β2 (EE) |
|---|---|---|---|---|---|
| E1 | × edad crítica | 0-2 frente a 3-5 años en 1997 | Edad en 1997. **Qué grupo es "crítico" no se dice**; por el color de la fig. 5 (el primer grupo de cada par es X = 1) sería 0-2 años: inferencia nuestra | 0,005 (0,066) | −0,053 (0,036) |
| E2 | × mujer | mujer frente a varón | Sexo del niño | 0,099 (0,073) | −0,026 (0,032) |
| E3 | × madre con educación alta | más que primaria frente a primaria o menos | "lower education (primary school or less)" (p. 5) | 0,129* (0,075) | −0,028 (0,032) |
| E4 | × pobre | pobre frente a no pobre | Línea oficial de pobreza de Indonesia de fines de los 90 (Widyanti et al. 2009; nota 3, p. 4) | 0,216 (0,180) | −0,085 (0,079) |
| E5 | × urbano | urbano frente a rural | Residencia | −0,270* (0,153) | 0,051 (0,058) |

\* p < 0,10. Errores robustos sin agrupar por comunidad; sin corrección por
comparaciones múltiples (notas de los cuadros A4 y A5 del suplemento). Lo que
E-Q leen en el texto (p. 5): más daño urbano (lo único que llaman
significativo), con madres de primaria o menos y en varones; los no pobres algo
más que los pobres, no significativo. En retraso en talla ninguna interacción
es significativa. Las cifras se cotejaron con el PDF y el suplemento el 20-nov
(nivel: texto del archivo; fig. 5, leída de la imagen).

**Fuera de este pre-registro:** las interacciones de WHZ, BMIZ, emaciación,
sobrepeso y obesidad (otros resultados) y las de 2014 (estatura adulta; cohorte
in utero o recién nacida, 0-2 y 3-5 años, cuadro A7): no están en el alcance.

**Cómo se replican (P4.x, `feols`):** la misma ecuación con T1 y con T2, en
primeras diferencias, con los controles de 1997 de E-Q, una interacción a la
vez, con errores robustos (para comparar con E-Q) y agrupados por `commid97`
(los que se interpretan), lado a lado. Se reporta el p sin ajustar y el
ajustado por Holm (familia F2, §3). Escala: β2 en HAZ por +100 % del precio.

## 2. Los GATE pre-declarados (bosque con T4)

Seis dimensiones, todas medidas en 1997. El orden es el de presentación y
empieza por la edad (H5); la corrección de Holm no depende del orden.

| # | Dimensión (H de `04` §4) | X = 1 | X = 0 | Predicción | Variable (a verificar en H2) |
|---|---|---|---|---|---|
| G1 | Edad en 1997 (H5) | 3-5 años (36-71 meses) | 0-2 años (0-35 meses) | Más daño a los 3-5 (E-Q p. 6, para la estatura adulta) | Fechas de nacimiento y de medición de 1997; `ptrack$age_97` solo para revisar |
| G2 | Urbano (H1) | Urbano | Rural | Más daño urbano (E-Q p. 5) | Ubicación urbana de 1997 (`bk_sc`/`htrack`) |
| G3 | Educación de la madre (H4) | Más que primaria | Primaria o menos | Menos daño con educación alta (E-Q p. 5) | Línea de la madre (`ar11`) + `ar16`/`ar17` del roster de 1997 |
| G4 | Sexo (H6) | Mujer | Varón | Sin predicción (E-Q: varones algo más, n.s.) | `ptrack$sex` |
| G5 | Comprador neto de arroz (H2) | Comprador neto | No comprador neto (productor o autosuficiente) | Más daño en compradores netos | `b1_ks1` 1997, ítem del arroz: comprador neto si el valor comprado supera el de la producción propia |
| G6 | Pobreza (H3) | Pobre | No pobre | Ambigua (E-Q: no pobres algo más, n.s.) | Gasto per cápita de 1997 bajo la línea oficial de Widyanti et al. (2009), como E-Q. Si no se consigue la línea, el cuartil inferior nacional del gasto per cápita; se decide en H2, antes de ver resultados |

G1-G4 y G6 son las dimensiones de E-Q (E1-E5); G5 es nuestra (E-Q lo invocan
para explicar lo urbano, pero no lo estiman, p. 5 y 7).

**Estimando:** GATE_g = E[τ(X) | G = g], con τ el efecto de vivir en una
comunidad del tercil alto del alza frente al tercil bajo (T4). Contraste de la
dimensión: Δ = GATE(X = 1) − GATE(X = 0).
**Estimador:** puntajes AIPW Γ_i de `get_scores(cf)` del bosque principal
(`clusters = commid97`, `seed = 2026`, `num.threads` fijo). GATE por grupo con
`average_treatment_effect(cf, subset = …)`; Δ con `feols(Γ ~ X, cluster =
~commid97)`, el mismo cálculo que una BLP con una sola variable.
**Escala:** HAZ entre terciles, no por +100 % del precio. Con E-Q se compara el
signo y el orden, no la magnitud.

## 3. Comparaciones múltiples: las familias de Holm

**Qué hace Holm.** Con m pruebas en una familia, se ordenan los p de menor a
mayor, p(1) ≤ … ≤ p(m). Se rechaza H(1) si p(1) ≤ α/m; si se rechaza, se pasa a
H(2) con α/(m − 1); y así, con α/(m − k + 1) para la k-ésima, hasta la primera
que no se rechaza (de ahí en adelante, ninguna). Equivale a reportar
p_Holm(k) = max_{j ≤ k} min{1, (m − j + 1) · p(j)} (`p.adjust(p, "holm")`). Controla
la **tasa de error por familia**: la probabilidad de declarar al menos un
efecto falso dentro de la familia es ≤ α, con cualquier dependencia entre las
pruebas. Es uniformemente más potente que Bonferroni (α/m para todas) y no
exige independencia.

**Qué es una familia.** El conjunto de pruebas sobre el que se haría una
afirmación conjunta («alguno de estos grupos sufrió más»). Se fija antes de ver
resultados, porque agrandarla o achicarla después cambia los umbrales.

| Familia | Pruebas | m | α | Qué se reporta |
|---|---|---|---|---|
| **F1 (principal, pregunta 2)** | Los seis contrastes Δ de G1-G6 (bilaterales) | 6 | 0,05 | Δ, EE agrupado, p sin ajustar y p Holm. Solo los que pasan Holm se llaman «diferencia entre grupos» |
| **F2 (réplica de E-Q)** | Las cinco β2 de E1-E5 con T1 y errores agrupados (bilaterales) | 5 | 0,05 | p sin ajustar (comparable con E-Q) y p Holm. Con T2 se repite como robustez, sin familia aparte |
| **F3 (pregunta 3)** | Las tres diferencias de RATE bosque − regla (pobre, urbano, comprador neto) | 3 | 0,05 | Diferencia, EE emparejado, p sin ajustar y p Holm |

**Fuera de toda familia** (una sola prueba pre-especificada cada una, o
descriptivas): el ATE de la pregunta 1 (resultado primario único);
`test_calibration`; el RATE del bosque solo (¿AUTOC > 0?); la BLP conjunta
(descriptiva); los cuartiles de la dosis, el placebo y las robusteces.

**Por qué Holm simple y no una secuencia con la edad primero.** Una prueba en
secuencia fija (la edad a α completo y las demás solo si la edad rechaza) daría
más potencia a la edad, pero si la edad no rechaza ya no se puede afirmar nada de
las otras cinco. La predicción para la edad viene de la estatura adulta de E-Q
(una asociación), no del HAZ de 2000. No es lo bastante firme para apostarle
toda la familia.

## 4. Focalización: la métrica de RATE es AUTOC

**Fijado:** `rank_average_treatment_effect(…, target = "AUTOC")`. QINI no se
reporta.

- **Qué mide.** La curva TOC compara, para cada fracción q de niños priorizados,
  el efecto medio en ese q superior con el efecto medio de todos. AUTOC es el área
  bajo esa curva con igual peso para cada q. Como el q superior entra en todas
  las fracciones mayores, el resultado pesa más la cabeza del orden. QINI pondera
  cada q por q, así que pesa más la cola y gana potencia cuando la heterogeneidad
  es difusa.
- **Por qué AUTOC.**
  1. La pregunta del cliente es a quién atender primero con un presupuesto
     limitado: importa la cabeza del orden.
  2. Es la métrica del Lab 10 (`07_Recursos/herramientas_R_del_curso.md` §5), así
     que no requiere ampliación.
- **Prioridades.** Bosque: −τ̂ (τ < 0 = daño), predicho por un bosque entrenado
  en una mitad de las comunidades y evaluado con otro bosque en la otra mitad
  (partición por `commid97` completo, `set.seed(2026)` antes de partir y antes
  del bootstrap). Reglas simples: 1{pobre}, 1{urbano} y 1{comprador neto}, con
  las definiciones de G6, G2 y G5.
- **Lectura.** Con W binario por terciles y sin comunidades sin tratar, la TOC se
  lee como ganancia relativa entre reglas, no como casos de desnutrición evitados.

## 5. Ampliaciones que esto requiere

Registradas en `CLAUDE.md` §11 el 20-nov: `get_scores`, `best_linear_projection`,
`average_treatment_effect(subset = …)` (ya registrada en el Taller 2) y, si se
usa, `fwildclusterboot` (bootstrap salvaje por conglomerados como robustez de los
EE con pocas comunidades por grupo).

## Desviaciones

- **20-nov-2026, antes de construir el tratamiento** (Santiago): se descarta T1
  (réplica con fuentes distintas en cada año). La familia F2 y la réplica de las
  interacciones de §1 usan la dosis con fuentes comunes (antes T2), y no T1 y T2.
  Ver `registro_decisiones.md`.

## Qué no está verificado

- Que la "edad crítica" de E-Q sea 0-2 años: se infiere del color de la fig. 5.
- El valor de la línea de pobreza de Widyanti et al. (2009) y si se puede
  aplicar al gasto que construimos para 1997 (E-Q no dicen qué agregado de gasto
  usan).
- Los nombres, códigos y unidades de `b1_ks1` para definir al comprador neto, y
  la línea de la madre en el roster de 1997: se verifican en H2.
- Cómo trata `rank_average_treatment_effect` los empates de una regla binaria y
  si acepta dos prioridades para la diferencia con EE emparejado: se verifica en
  la documentación de `grf` 2.6.1 antes de P6.2.
- La afirmación de que AUTOC pesa la cabeza y QINI la cola viene de Yadlowsky et
  al. (2025), citada de memoria; hay que verificar la página.
