# Resumen de H3 (¿a quién?) y de la calibración, para las láminas

Sesión del 22-nov-2026 (4), Samuel Escandón. Todas las cifras salen de los
archivos citados; las notas con el detalle están en `05_Notas/09_*` a `13_*`.
Escala: HAZ (desviaciones estándar de talla para la edad, OMS), cambio
1997→2000, niños de 0-5 años en 1997. EE agrupados por comunidad.

## Pregunta 2a: ¿se replican las interacciones de Elmira y Qaim? (P3.1, F2)

- Con la dosis (+100 % del precio) y la especificación (4) de la pregunta 1,
  **ninguna de las cinco diferencias entre grupos se distingue de cero**: β2
  entre −0,096 y +0,127, EE agrupados de 0,18 a 0,26, p sin ajustar ≥ 0,63 y
  p Holm = 1,000 en las cinco. 2.328 a 2.421 niños, 294 comunidades.
  → `03_Resultados/Tablas/09_interacciones_eq/ninos_interacciones_eq.png`
- El efecto es negativo en todos los grupos: β1 (X = 0) entre −0,29 y −0,38 y
  β1 + β2 (X = 1) entre −0,23 y −0,39 HAZ por +100 %. (misma tabla)
- **Urbano**, el único resultado que E-Q destacan (−0,270, EE robusto 0,153, al
  10 %), aquí es −0,009 (EE agrupado 0,223; robusto 0,194). Los intervalos se
  traslapan. (misma tabla)
- Madre educada, mujer y pobre: mismo signo que E-Q, ninguno significativo.
  Edad: X = 1 = 0-2 años (inferencia nuestra sobre la «edad crítica» de E-Q).

## Pregunta 2b: GATE pre-declarados con el bosque (P3.2-P3.3, F1)

- **Bosque** (tercil alto frente a bajo del alza dentro de provincia; 1.602
  niños, 195 comunidades): ATE −0,184 (EE 0,065), casi igual al MCO con el
  mismo tratamiento (−0,188, EE 0,079). Otro estimando: tercil alto (+107 %
  de alza media) frente a bajo (+48 %), no por +100 %.
  → `03_Resultados/Tablas/10_bosque/ninos_bosque_ate.png`
- **Traslape:** `W.hat` entre 0,10 y 0,93; ningún niño fuera de [0,05; 0,95].
  Las X de 1997 predicen bien el tercil (mediana de `W.hat` 0,155 en el bajo y
  0,719 en el alto).
  → `03_Resultados/Figuras/10_bosque/ninos_bosque_traslape.png`
- **Ninguno de los seis contrastes GATE pasa Holm** (menor p Holm 0,764). Los
  doce GATE son negativos (−0,08 a −0,31).
  → `03_Resultados/Figuras/11_gate/ninos_gate.png` y
  `03_Resultados/Tablas/11_gate/ninos_gate.png`
- Lo que más se aleja es la **edad**: 0-2 años −0,313 (0,136) frente a 3-5
  años −0,083 (0,055); Δ = 0,229 (0,150), p = 0,127, Holm 0,764. Contrario a
  lo pre-declarado (más daño a los 3-5), en la misma dirección que la réplica
  de E-Q; ninguno con precisión suficiente.
- Comprador neto −0,221 frente a −0,093 (Δ −0,128, EE 0,158); urbano y rural
  iguales (Δ −0,003). BLP conjunta solo descriptiva.
  → `03_Resultados/Tablas/11_gate/ninos_blp.png`

**Mensaje para la lámina:** el alza dañó a todos los grupos; con 195-294
comunidades no se detecta que haya dañado más a unos que a otros.

## Pregunta 3 (parcial): ¿capta el bosque heterogeneidad? (P4.1, P4.3)

- **Calibración:** predicción media 0,974 (EE 0,589, p unilateral 0,049);
  predicción diferencial 0,124 (EE 0,799, p 0,438). **No hay evidencia de
  heterogeneidad más allá de los GATE pre-declarados.** 1.602 niños, 195
  comunidades.
  → `03_Resultados/Tablas/12_calibracion/ninos_calibracion.png`
- **Perfil** (descriptivo): el bosque ordena sobre todo por edad. Cuartil de
  más daño predicho (−0,342): 22,5 meses de edad media, 25 % de 3-5 años;
  cuartil de menos daño (0,000): 51,7 meses, 82 % de 3-5 años. Pobreza y zona
  urbana casi no cambian entre cuartiles.
  → `03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.png`
- **Mensaje para el cliente (lámina del nulo):** con esta evidencia el bosque no
  tiene respaldo para focalizar; ninguna de las reglas simples (pobre, urbano,
  comprador neto) se distingue tampoco. El RATE formal (P4.2) no se corrió.

## Marcado [REVISIÓN HUMANA]

- `06_Bitacoras/2026-11-22_heterogeneidad-h3_4.md`, línea 17: la rama local
  `SamuelEscandonC` está en otro worktree; se empujó desde este worktree a
  `origin/SamuelEscandonC` y la rama local queda atrás (hacer `git pull` en
  ella).
- `05_Notas/09_interacciones_eq/H_interacciones_eq.md`, línea 60: urbano no se
  replica (E-Q −0,270 frente a −0,009); decidir cómo presentarlo.
- `05_Notas/12_calibracion/H_calibracion_nulo.md`, línea 55: no se verificó si
  `test_calibration` usa EE agrupados con un bosque agrupado (la salida dice
  HC3); la conclusión no cambia.
