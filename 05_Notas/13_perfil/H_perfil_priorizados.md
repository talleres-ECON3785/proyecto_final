# El bosque ordena primero a los niños más pequeños: el cuartil de más daño predicho tiene 22 meses de edad media frente a 52 en el de menos, pero ese orden no está validado (la calibración no rechaza)

- **Estado:** vigente
- **Etapa / alcance:** H; descriptivo
- **Script de origen:** `02_Scripts/13_perfil.R`
- **Hipótesis relacionada:** pregunta 3, perfil de los priorizados (P4.3). Describe el orden del bosque; no prueba diferencias
- **Última verificación:** 2026-11-22, con `02_Scripts/13_perfil.R` (P4.3)

## Evidencia

`03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.{png,csv}`

Efecto predicho por el bosque de `10_bosque` (τ̂ fuera de la bolsa, tercil alto
frente a bajo del alza) para 1.602 niños en 195 comunidades, en cuartiles entre
niños (unos 400 por cuartil, 132 a 150 comunidades cada uno).

| | Cuartil 1 (más daño predicho) | 2 | 3 | Cuartil 4 (menos daño predicho) |
|---|---:|---:|---:|---:|
| Efecto predicho medio (HAZ) | −0,342 | −0,180 | −0,086 | 0,000 |
| Edad en 1997 (meses) | 22,5 | 36,7 | 44,9 | 51,7 |
| 3-5 años | 25,2 % | 45,9 % | 72,0 % | 82,0 % |
| Urbano | 44,1 % | 41,1 % | 38,8 % | 39,5 % |
| Madre con más que primaria | 41,5 % | 37,2 % | 42,5 % | 24,9 % |
| Mujer | 57,9 % | 48,1 % | 52,0 % | 41,2 % |
| Comprador neto | 73,3 % | 72,2 % | 65,2 % | 69,5 % |
| Pobre | 26,9 % | 23,0 % | 20,1 % | 29,8 % |
| Tamaño del hogar | 6,4 | 6,0 | 5,5 | 5,3 |

## Qué dice, en lenguaje intuitivo

- Si se usara el bosque para escoger a quién atender primero, escogería sobre
  todo a los niños más pequeños (menores de dos años en 1997) y, en menor
  medida, a niñas, hijos de hogares más grandes y compradores netos de arroz.
- Su variable principal es la edad, lo mismo que sugerían, sin precisión
  suficiente, la réplica de E-Q y los GATE (0-2 años con algo más de daño).
- Pero la prueba de calibración no encuentra que ese orden capte diferencias
  reales (`05_Notas/12_calibracion/H_calibracion_nulo.md`). Así que este perfil
  dice **a quién ordenaría el bosque**, no a quién dañó más el alza.

## Por qué importa en el estudio

- **Para el cliente:** es el perfil, en variables que una agencia observa (edad,
  sexo, tamaño del hogar, educación de la madre), de lo que priorizaría el
  bosque. Con la calibración nula, la recomendación es no usarlo para
  focalizar; si se quiere una regla, la edad es la candidata a probar, y su
  diferencia no pasó Holm (`05_Notas/11_gate/H_gate_preregistrados.md`).
- Pobreza y zona urbana casi no cambian entre cuartiles: el bosque no ordena por
  las reglas que el cliente usaría por defecto.

## Límites e incertidumbre

- Descriptivo: las diferencias entre cuartiles no tienen prueba ni EE.
- Que el bosque divida por la edad no hace a la edad la causa de la
  heterogeneidad; la importancia de variables no es un efecto.
- Los cuartiles son entre niños; una comunidad puede aportar niños a varios.

## Historial

- 2026-11-22: creación (P4.3).
