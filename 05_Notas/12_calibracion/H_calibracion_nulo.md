# No hay evidencia de heterogeneidad más allá de los GATE pre-declarados: la prueba de calibración del bosque no rechaza (predicción diferencial 0,12, p unilateral 0,44)

- **Estado:** vigente
- **Etapa / alcance:** H; contraste entre comunidades del tercil alto y bajo del alza
- **Script de origen:** `02_Scripts/12_calibracion.R`
- **Hipótesis relacionada:** pregunta 3 (¿el bosque supera a las reglas simples?), primer paso. Prueba única fuera de Holm (pre-registro §3)
- **Última verificación:** 2026-11-22, con `02_Scripts/12_calibracion.R` (P4.1)

## Evidencia

`03_Resultados/Tablas/12_calibracion/ninos_calibracion.{png,csv}`

`test_calibration` del bosque de `10_bosque` (tercil alto frente a bajo del alza
dentro de provincia; 1.602 niños en 195 comunidades):

| Término | Coeficiente | EE | p (unilateral) |
|---|---:|---:|---:|
| Predicción media | 0,974 | 0,589 | 0,049 |
| Predicción diferencial | 0,124 | 0,799 | 0,438 |

## Qué dice, en lenguaje intuitivo

- La prueba pregunta dos cosas. Primero, si el efecto promedio que estima el
  bosque es correcto en promedio: el coeficiente es 0,97 (cerca de 1, como
  debería), aunque con mucha incertidumbre.
- Segundo, si las diferencias entre niños que predice el bosque son reales: si
  lo fueran, los niños a los que el bosque les predice más daño deberían, de
  hecho, mostrar más daño. El coeficiente es 0,12, lejos de 1, con un error de
  0,80: no hay evidencia de que el orden del bosque capte diferencias reales.
- **Mensaje:** no hay evidencia de heterogeneidad más allá de los GATE
  pre-declarados (que tampoco la mostraron). Es un resultado válido: el daño
  del alza del arroz se ve parejo dentro de lo que estos datos permiten
  distinguir.

## Por qué importa en el estudio

- **Pregunta 3 y cliente:** sin calibración, el orden del bosque no tiene
  respaldo para focalizar. Lo esperable es que el RATE frente a las reglas
  simples (P4.2, no hecho en esta sesión) tampoco muestre ventaja; la lámina
  del nulo dice que, con esta evidencia, una regla simple (o ninguna dentro de
  los expuestos) es tan defendible como el bosque.
- **Consistente** con P3.1 y P3.3 (`05_Notas/09_interacciones_eq/`,
  `05_Notas/11_gate/`): ninguna diferencia entre grupos pasa Holm, y el bosque
  tampoco encuentra heterogeneidad por su cuenta.
- **Consistente con lo anticipado** en `CLAUDE.md` §5.6: con unos cientos de
  comunidades, la búsqueda del bosque tiene poca potencia (una simulación del
  20-nov no pasó la calibración aun con heterogeneidad grande).
- La predicción media (p = 0,049) concuerda con que el ATE del bosque (−0,184)
  es distinto de cero (`05_Notas/10_bosque/H_bosque_ate_traslape.md`).

## Límites e incertidumbre

- No rechazar no prueba que el efecto sea igual para todos: con 195
  comunidades, la prueba solo detectaría heterogeneidad grande.
- **[REVISIÓN HUMANA]** La salida de `grf` 2.6.1 dice «HC3»; no se verificó en
  la documentación si, con un bosque agrupado, `test_calibration` usa errores
  agrupados por comunidad. Si no los usa, el EE estaría subestimado y la
  conclusión (no rechaza) no cambiaría.
- Hereda los límites del bosque y del ATE (traslape con `W.hat` muy
  predecible; placebo inconcluso).

## Historial

- 2026-11-22: creación (P4.1).
