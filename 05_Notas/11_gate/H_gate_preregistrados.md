# Ninguno de los seis contrastes GATE pre-declarados pasa Holm: con 195 comunidades no hay evidencia de que el daño del tercil alto del alza difiera entre grupos

- **Estado:** vigente
- **Etapa / alcance:** H; contraste entre comunidades del tercil alto y bajo del alza
- **Script de origen:** `02_Scripts/11_gate.R`
- **Hipótesis relacionada:** G1-G6 del pre-registro (familia F1). Ninguna se apoya; G1 (más daño a los 3-5 años) va en el sentido **contrario** en la estimación puntual, sin distinguirse de cero
- **Última verificación:** 2026-11-22, con `02_Scripts/11_gate.R` (P3.3)

## Evidencia

- `03_Resultados/Tablas/11_gate/ninos_gate.{png,csv}`
- `03_Resultados/Figuras/11_gate/ninos_gate.png`
- `03_Resultados/Tablas/11_gate/ninos_blp.{png,csv}` (descriptiva)

Bosque de `10_bosque` (tercil alto frente a bajo del alza dentro de provincia;
1.602 niños en 195 comunidades). GATE = promedio de los puntajes AIPW en el
grupo (EE agrupado); Δ = GATE(X = 1) − GATE(X = 0) por MCO de los puntajes
sobre el indicador, EE agrupado por comunidad. Escala: HAZ entre terciles. Δ < 0
= más daño en X = 1.

| | X = 1 frente a X = 0 | GATE X = 1 | GATE X = 0 | Δ (EE) | p | p Holm (F1) | Comunidades (X1 / X0) |
|---|---|---:|---:|---:|---:|---:|---:|
| G1 | 3-5 años frente a 0-2 | −0,083 (0,055) | −0,313 (0,136) | 0,229 (0,150) | 0,128 | 0,765 | 190 / 182 |
| G2 | urbano frente a rural | −0,185 (0,095) | −0,183 (0,089) | −0,003 (0,130) | 0,983 | 1,000 | 111 / 84 |
| G3 | madre con más que primaria frente a primaria o menos | −0,206 (0,096) | −0,177 (0,098) | −0,029 (0,138) | 0,831 | 1,000 | 162 / 169 |
| G4 | mujer frente a varón | −0,197 (0,095) | −0,171 (0,096) | −0,026 (0,139) | 0,850 | 1,000 | 184 / 184 |
| G5 | comprador neto frente a no comprador neto | −0,221 (0,085) | −0,093 (0,121) | −0,127 (0,158) | 0,420 | 1,000 | 186 / 142 |
| G6 | pobre frente a no pobre | −0,103 (0,129) | −0,209 (0,075) | 0,106 (0,148) | 0,474 | 1,000 | 118 / 190 |

- **BLP conjunta** (1.538 niños sin faltantes, 195 comunidades; descriptiva,
  fuera de Holm): coeficientes entre −0,168 (comprador neto, EE 0,171) y
  +0,211 (3-5 años, EE 0,166); ninguno mayor que 1,3 veces su EE.
- **Exploratorio (fuera de PLAN.md y de Holm), edad sin los 70 niños del bosque con |ΔHAZ| > 3:**
  G1 Δ pasa de 0,229 (EE 0,150; p 0,128) a 0,283 (0,119; p 0,018 sin ajustar) y E1 β2 de −0,096 (0,207) a −0,213 (0,146; p 0,146); `03_Resultados/Tablas/11_gate/ninos_edad_sin_cola_exploratorio.{png,csv}`. La cola se mantiene en lo principal (decisión previa de P1.6).

## Qué dice, en lenguaje intuitivo

- En los doce grupos, los niños del tercio de comunidades con más alza crecieron
  menos que los del tercio con menos alza (todas las estimaciones son
  negativas, entre −0,08 y −0,31).
- Las diferencias entre grupos son pequeñas frente a su margen de error. Después
  de corregir por mirar seis comparaciones a la vez, ninguna es distinguible de
  cero. Es un resultado válido: con estos datos no hay base para decir que un
  grupo sufrió más que otro.
- Lo que más se aleja es la edad: los menores de 3 años en 1997 muestran más
  daño (−0,31) que los de 3-5 (−0,08), lo contrario de lo pre-declarado. Con su
  incertidumbre, no basta para afirmarlo.
- Los compradores netos de arroz muestran algo más de daño que los demás
  (−0,22 frente a −0,09), en el sentido esperado, pero tampoco se distingue de
  cero.

## Por qué importa en el estudio

- **Pregunta 2 (¿a quién?):** la respuesta honesta es que no se detectan
  diferencias entre los grupos pre-declarados. Para el cliente, ninguno de estos
  seis criterios tiene, con esta evidencia, respaldo para priorizar dentro de
  los niños expuestos.
- **Consistente con P3.1** (`05_Notas/09_interacciones_eq/H_interacciones_eq.md`):
  la réplica con la dosis tampoco encontró diferencias, y la edad apunta en la
  misma dirección (0-2 años algo más de daño: β2 = −0,096 allí, Δ = +0,229 aquí
  con el signo al revés porque X = 1 es 3-5 años). Dos estimadores y dos
  tratamientos distintos coinciden en dirección para la edad, ninguno con
  precisión suficiente.
- **Frente a E-Q:** su único resultado destacado (más daño urbano) no aparece
  (G2 Δ = −0,003). Su menor daño con madre educada tampoco (G3 Δ = −0,029, signo
  opuesto). Difiere, atribuible al tratamiento (terciles dentro de provincia
  frente a la dosis con otra medida del precio), al agrupamiento por comunidad
  y a la corrección por comparaciones múltiples; E-Q reportan esas diferencias
  al 10 % sin agrupar ni corregir.
- **Pre-registro G1** («más daño a los 3-5», tomado de la estatura adulta de
  E-Q): la estimación puntual va en sentido contrario, no significativa. Se
  registra como **no apoyada**, sin reformular la hipótesis.

## Límites e incertidumbre

- 195 comunidades: los EE de Δ son de 0,13 a 0,16 HAZ, comparables al ATE
  (−0,18). Solo diferencias del tamaño del efecto promedio serían detectables.
- Los grupos urbano (111 comunidades) y rural (84), y pobre (118), tienen menos
  comunidades; sus GATE son más imprecisos.
- La BLP es descriptiva y sus coeficientes están condicionados a las demás
  variables; no se usa para afirmar nada.
- Hereda los límites del bosque (`05_Notas/10_bosque/H_bosque_ate_traslape.md`):
  las X predicen bien el tercil y el placebo del ATE es inconcluso.

## Historial

- 2026-11-22: creación (P3.3).
- 2026-11-22: línea exploratoria de la edad sin la cola del ΔHAZ (pedida por Samuel; no cambia el estado).
