# Estructura de la presentación (20 min + 5 de preguntas)

Versión del 22-nov-2026 (Samuel Escandón). Arco: **¿dolió? → ¿a quién? → ¿el
bosque supera a las reglas simples? → qué hacer**. 15 láminas principales,
1.200 s en total, cuatro presentadores con 285 a 310 s cada uno. Las cifras y
rutas salen de `03_Resultados/`; el texto completo con las fuentes está en
`04_Presentaciones/hallazgos_principales.txt`. Todas las rutas se verificaron
con `ls` el 22-nov. Las figuras y tablas entran tal como se exportaron, sin
retoques.

Escala: HAZ = talla para la edad en desviaciones estándar OMS; EE agrupados
por comunidad.

---

## Láminas principales

### 1. El arroz subió en toda Indonesia, pero mucho más en unas comunidades que en otras: ¿a qué niños protege primero una agencia?
- **Mensaje:** pregunta y cliente.
- **Visual:** sin figura (título, cliente y las tres preguntas).
- **Cifras:** ninguna.
- **Tiempo / presentador:** 45 s · Presentador 1.
- **Notas del orador:** Somos consultores de una agencia que focaliza ayuda
  ante choques de precios de alimentos. La crisis de 1997-98 subió el arroz en
  todo el país, pero de forma desigual. Respondemos tres preguntas: ¿dolió?,
  ¿a quién?, y ¿un bosque causal escoge mejor que una regla simple?

### 2. El alza fue de +20 % a +153 % entre comunidades, y casi toda esa diferencia está dentro de cada provincia
- **Mensaje:** comparamos comunidades con más y menos alza, no «con y sin crisis».
- **Visual:** `03_Resultados/Figuras/02_precio_arroz/comunidades_distribucion_alza.png`
- **Cifras:** mediana +70 %; +20 % a +153 % tras winsorizar; la provincia
  explica el 14,6 % de la varianza (`03_Resultados/Tablas/02_precio_arroz/comunidades_resumen_precio.csv`).
- **Tiempo / presentador:** 75 s · Presentador 1.
- **Notas del orador:** El tratamiento es el cambio proporcional del precio
  nominal del arroz en la comunidad de 1997, entre 1997 y 2000. No hay
  comunidades sin alza: identificamos el contraste de más alza frente a menos
  alza. Como el 85 % de la variación está dentro de provincia, podemos comparar
  comunidades vecinas y descontar choques regionales.

### 3. Seguimos a 2.421 niños en 294 comunidades, y el seguimiento 1997-2000 no depende del alza
- **Mensaje:** la muestra es válida para el contraste; la unidad de inferencia son las comunidades.
- **Visual:** `03_Resultados/Tablas/05_base/ninos_desgaste_alza.png`
- **Cifras:** 2.421 niños, 294 comunidades; llega a la base el 77,5 % en el
  cuartil 1 y el 71,2 % en el 4; pendiente del seguimiento −0,003 (EE 0,017)
  (`03_Resultados/Tablas/05_base/ninos_desgaste_alza.csv` y `ninos_desgaste_alza_pendientes.csv`).
- **Tiempo / presentador:** 75 s · Presentador 1.
- **Notas del orador:** Niños de 0-5 años en 1997, medidos en 1997 y 2000 en la
  IFLS. De los medidos en 1997, cerca del 93 % se vuelve a medir en 2000 sin
  importar el alza. Donde más subió el arroz se midió a menos niños en 1997,
  pero esa brecha es sobre todo entre provincias y no cambia quiénes quedan.

### 4. Donde el arroz subió más, los niños crecieron menos: −0,33 HAZ por +100 % de alza (≈ −1,7 cm)
- **Mensaje:** sí dolió, en la escala del contraste; más que lo que reportan E-Q.
- **Visual:** `03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.png`
- **Cifras:** −0,217 a −0,339 según la especificación; principal (4) −0,329
  (EE 0,139; p 0,018), ≈ −1,66 cm; E-Q −0,135 (EE robusto 0,041)
  (`03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.csv`).
- **Tiempo / presentador:** 100 s · Presentador 1.
- **Notas del orador:** Regresamos el cambio en la talla del mismo niño sobre
  el alza de su comunidad, con errores agrupados por comunidad. El efecto se
  mantiene con controles de 1997 y crece al comparar dentro de provincia. Es
  1,6 a 2,5 veces el de Elmira y Qaim, con intervalos que se traslapan; ellos
  miden el precio distinto y no usan efectos fijos de provincia.

### 5. El daño aparece en los tres cuartiles de mayor alza y es mayor en el de más alza (−0,30 HAZ)
- **Mensaje:** el efecto no viene de unas pocas comunidades extremas; cabe en una recta.
- **Visual:** `03_Resultados/Figuras/07_cuartiles/ninos_cuartiles_coeficientes.png`
- **Cifras:** frente al cuartil 1 (+42 %): Q2 −0,189 (EE 0,093), Q3 −0,116
  (EE 0,094), Q4 −0,295 (EE 0,104) (`03_Resultados/Tablas/07_cuartiles/ninos_cuartiles_especificaciones.csv`).
- **Tiempo / presentador:** 70 s · Presentador 2.
- **Notas del orador:** Partimos el alza en cuartiles. Los tres de arriba
  crecen menos que el de abajo; el de más alza, unas 0,3 desviaciones estándar
  menos. Con unas 73 comunidades por cuartil, la inversión entre Q2 y Q3 cabe
  en el ruido. Por eso usamos la dosis lineal como medida principal.

### 6. El placebo no se distingue de cero, pero tampoco lo descarta: es inconcluso
- **Mensaje:** no hay prueba de tendencia previa, pero no podemos excluirla.
- **Visual:** `03_Resultados/Tablas/08_validacion/ninos_placebo.png`
- **Cifras:** −0,097 (EE 0,123; p 0,432) sin controles; −0,192 (EE 0,117;
  p 0,102) con controles; 2.221 niños, 285 comunidades
  (`03_Resultados/Tablas/08_validacion/ninos_placebo.csv`).
- **Tiempo / presentador:** 80 s · Presentador 2.
- **Notas del orador:** Tomamos niños pequeños en 1993 y medimos cuánto
  crecieron entre 1993 y 1997, antes del alza. Si nada era distinto antes, no
  debería haber relación con el alza posterior. No se distingue de cero, pero
  con controles es cerca del 60 % del efecto principal. Lo decimos tal cual.

### 7. La dirección se sostiene en todas las variantes; el tamaño va de −0,20 a −0,50
- **Mensaje:** confiamos en el signo, no en el número exacto.
- **Visual:** `03_Resultados/Tablas/08_validacion/ninos_robustez.png`
- **Cifras:** sin la cola |ΔHAZ| > 3 −0,197 (EE 0,106); sin winsorizar −0,207
  (EE 0,165); con pesos −0,504 (EE 0,161) (`03_Resultados/Tablas/08_validacion/ninos_robustez.csv`).
- **Tiempo / presentador:** 70 s · Presentador 2.
- **Notas del orador:** Cambiamos una cosa a la vez: sin las comunidades con
  precio levantado en 1998, con pesos, sin recortar extremos del alza, solo
  kg, sin los cambios de talla extremos. Siempre negativo; el tamaño cambia.
  Para el cliente: el alza se asocia con menos crecimiento, la magnitud es
  incierta.

### 8. No replicamos las diferencias entre grupos de Elmira y Qaim: ninguna de las cinco interacciones se distingue de cero
- **Mensaje:** con la dosis, el daño es parecido en todos los grupos que miran E-Q.
- **Visual:** `03_Resultados/Tablas/09_interacciones_eq/ninos_interacciones_eq.png`
- **Cifras:** β2 de −0,096 a 0,127 (EE 0,18 a 0,26); p Holm = 1,000 en las
  cinco; urbano −0,009 (EE 0,223) frente a −0,270 de E-Q
  (`03_Resultados/Tablas/09_interacciones_eq/ninos_interacciones_eq.csv`).
- **Tiempo / presentador:** 90 s · Presentador 2.
- **Notas del orador:** Repetimos sus cinco interacciones, una a la vez, con
  errores agrupados y corrección de Holm. El efecto es negativo en todos los
  grupos. Lo urbano, que ellos destacan, no lo confirmamos ni lo descartamos:
  nuestro intervalo (−0,45 a 0,43) contiene su cifra. Ellos reportan al 10 %,
  sin agrupar ni corregir.

### 9. El bosque causal da el mismo efecto promedio que la regresión: −0,18 HAZ del tercil alto frente al bajo
- **Mensaje:** el bosque está bien parado para buscar heterogeneidad; hay traslape.
- **Visual:** `03_Resultados/Figuras/10_bosque/ninos_bosque_traslape.png`
- **Cifras:** ATE bosque −0,184 (EE 0,065); MCO −0,188 (EE 0,079); 1.602
  niños, 195 comunidades; W.hat de 0,101 a 0,933
  (`03_Resultados/Tablas/10_bosque/ninos_bosque_ate.csv`).
- **Tiempo / presentador:** 70 s · Presentador 3.
- **Notas del orador:** Para el bosque usamos un tratamiento binario: tercil
  alto frente a bajo del alza dentro de cada provincia. Es otro estimando que
  la dosis, pero coincide con la recta (≈ −0,19). Ningún niño tiene propensión
  fuera de 5-95 %, aunque las características de 1997 anticipan bastante el
  tercil.

### 10. Ninguno de los seis grupos pre-declarados sufrió más que su complemento después de corregir por comparaciones múltiples
- **Mensaje:** el daño se ve en todos los grupos; no detectamos diferencias entre ellos.
- **Visual:** `03_Resultados/Figuras/11_gate/ninos_gate.png`
- **Cifras:** menor p Holm 0,765 (edad); los doce GATE entre −0,08 y −0,31;
  0-2 años −0,313 (EE 0,136) frente a 3-5 años −0,083 (EE 0,055)
  (`03_Resultados/Tablas/11_gate/ninos_gate.csv`).
- **Tiempo / presentador:** 110 s · Presentador 3.
- **Notas del orador:** Fijamos seis grupos antes de ver datos: edad, urbano,
  educación de la madre, sexo, comprador neto y pobreza. Con los puntajes AIPW
  del bosque, ningún contraste pasa Holm. La edad es la que más se aleja: los
  menores de 3 años con más daño, al revés de lo que esperábamos. Sin la cola
  de cambios extremos esa señal crece, pero es exploratoria.

### 11. Con 195-294 comunidades, solo veríamos diferencias entre grupos del tamaño del efecto promedio
- **Mensaje:** «no se distingue de cero» no es «igual para todos».
- **Visual:** sin figura: texto con tres cifras (ver «Figuras que faltarían»).
- **Cifras (aproximadas, MDE ≈ 2,8 × EE):** ATE 0,39 por +100 %; contrastes
  GATE 0,36 a 0,44 HAZ; interacciones de E-Q 0,51 a 0,73 (EE de
  `03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.csv`,
  `11_gate/ninos_gate.csv` y `09_interacciones_eq/ninos_interacciones_eq.csv`;
  cálculo en `02_Scripts/_exploratorio/mde_potencia.R`).
- **Tiempo / presentador:** 60 s · Presentador 3.
- **Notas del orador:** ¿Qué tan grande tendría que ser una diferencia para
  verla? Con 5 % y 80 % de potencia, unas 2,8 veces su error estándar: más de
  0,36 desviaciones estándar entre grupos, el doble del efecto del bosque. Es
  una aproximación; nos dice que el nulo es poco informativo sobre diferencias
  pequeñas.

### 12. El bosque no encuentra heterogeneidad por su cuenta: la prueba de calibración no rechaza
- **Mensaje:** no hay evidencia de heterogeneidad más allá de los GATE pre-declarados.
- **Visual:** `03_Resultados/Tablas/12_calibracion/ninos_calibracion.png`
- **Cifras:** predicción media 0,974 (EE 0,589); predicción diferencial 0,124
  (EE 0,799; p unilateral 0,438) (`03_Resultados/Tablas/12_calibracion/ninos_calibracion.csv`).
- **Tiempo / presentador:** 70 s · Presentador 3.
- **Notas del orador:** La prueba pregunta si los niños a los que el bosque
  les predice más daño de verdad sufren más. El coeficiente debería acercarse
  a 1 si capta diferencias reales; da 0,12 con un error de 0,80. El promedio
  sí está calibrado (0,97). Los errores agrupan por comunidad y el p es
  unilateral.

### 13. Priorizar con el bosque no encuentra a los más dañados mejor que priorizar por pobreza, zona urbana o compra neta de arroz
- **Mensaje:** el algoritmo no supera a las reglas simples (ni las reglas entre sí).
- **Visual:** `03_Resultados/Figuras/14_rate/ninos_rate_toc.png`
- **Cifras:** AUTOC bosque 0,115 (EE 0,116); diferencias bosque − regla 0,068
  a 0,207, menor p Holm 0,503; 834 niños, 98 comunidades
  (`03_Resultados/Tablas/14_rate/ninos_rate.csv`).
- **Tiempo / presentador:** 110 s · Presentador 4.
- **Notas del orador:** Simulamos a la agencia escogiendo a quién atender
  primero. Entrenamos el bosque en la mitad de las comunidades y lo evaluamos
  en la otra. En escala de daño, mayor que cero significa que la regla
  encuentra a los más afectados. Ni el bosque ni las reglas se distinguen de
  cero, y ninguna diferencia pasa Holm.

### 14. El bosque priorizaría sobre todo a los más pequeños, pero ese orden no está validado
- **Mensaje:** perfil descriptivo, en variables que el cliente observa.
- **Visual:** `03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.png`
- **Cifras:** edad media 22,4 meses en el cuartil de más daño predicho frente a
  51,7 en el de menos; 3-5 años: 24,9 % frente a 82,0 %
  (`03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.csv`).
- **Tiempo / presentador:** 65 s · Presentador 4.
- **Notas del orador:** Si alguien usara el bosque, escogería a los menores de
  tres años. Pobreza y zona urbana casi no cambian entre cuartiles. Como la
  calibración y el RATE no lo respaldan, esto describe al algoritmo, no a
  quién le dolió más.

### 15. Qué hacer: focalizar por el alza en la comunidad y cubrir a todos los niños pequeños; no usar un algoritmo para escoger dentro
- **Mensaje:** recomendación y límites.
- **Visual:** sin figura: texto (qué hacer / qué no / límites).
- **Cifras:** −0,33 HAZ por +100 % (lámina 4); ninguna diferencia entre grupos
  pasa Holm (láminas 8, 10, 13).
- **Tiempo / presentador:** 110 s · Presentador 4.
- **Notas del orador:** El alza importa: donde más subió, menos crecieron los
  niños. No encontramos a quién le dolió más, ni un algoritmo que lo encuentre
  mejor que una regla. Recomendamos vigilar el alza por comunidad y cubrir a
  todos los niños pequeños; la edad es una pista a confirmar. Límites: placebo
  inconcluso, choques simultáneos y poca potencia.

**Tiempos:** Presentador 1: 295 s (1-4); Presentador 2: 310 s (5-8);
Presentador 3: 310 s (9-12); Presentador 4: 285 s (13-15). Total 1.200 s.

---

## Tabla resumen

| Lámina | Figura o tabla | Ruta | Script que la genera |
|---|---|---|---|
| 1 | — | sin figura | — |
| 2 | Distribución del alza | `03_Resultados/Figuras/02_precio_arroz/comunidades_distribucion_alza.png` | `02_Scripts/02_precio_arroz.R` |
| 3 | Desgaste según el alza | `03_Resultados/Tablas/05_base/ninos_desgaste_alza.png` | `02_Scripts/05_base.R` |
| 4 | ATE, cuatro especificaciones | `03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.png` | `02_Scripts/06_ate.R` |
| 5 | Coeficientes por cuartil | `03_Resultados/Figuras/07_cuartiles/ninos_cuartiles_coeficientes.png` | `02_Scripts/07_cuartiles.R` |
| 6 | Placebo | `03_Resultados/Tablas/08_validacion/ninos_placebo.png` | `02_Scripts/08_validacion.R` |
| 7 | Robustez | `03_Resultados/Tablas/08_validacion/ninos_robustez.png` | `02_Scripts/08_validacion.R` |
| 8 | Interacciones de E-Q | `03_Resultados/Tablas/09_interacciones_eq/ninos_interacciones_eq.png` | `02_Scripts/09_interacciones_eq.R` |
| 9 | Traslape del bosque | `03_Resultados/Figuras/10_bosque/ninos_bosque_traslape.png` | `02_Scripts/10_bosque.R` |
| 10 | GATE | `03_Resultados/Figuras/11_gate/ninos_gate.png` | `02_Scripts/11_gate.R` |
| 11 | — (MDE en texto) | sin figura | `02_Scripts/_exploratorio/mde_potencia.R` (cifras) |
| 12 | Calibración | `03_Resultados/Tablas/12_calibracion/ninos_calibracion.png` | `02_Scripts/12_calibracion.R` |
| 13 | Curvas TOC | `03_Resultados/Figuras/14_rate/ninos_rate_toc.png` | `02_Scripts/14_rate.R` |
| 14 | Perfil por cuartil de τ̂ | `03_Resultados/Tablas/13_perfil/ninos_perfil_cuartil_tau.png` | `02_Scripts/13_perfil.R` |
| 15 | — | sin figura | — |

---

## Apéndice (láminas de respaldo)

| # | Contenido | Ruta | Script |
|---|---|---|---|
| A1 | Cohortes y desgaste por ola | `03_Resultados/Tablas/01_tracks/cohortes_desgaste.png` | `01_tracks.R` |
| A2 | Resumen del precio | `03_Resultados/Tablas/02_precio_arroz/comunidades_resumen_precio.png` | `02_precio_arroz.R` |
| A3 | HAZ por cohorte y año | `03_Resultados/Tablas/04_haz/cohortes_haz_resumen.png` | `04_haz.R` |
| A4 | Motivos del HAZ faltante en 1997 | `03_Resultados/Tablas/05_base/ninos_haz1997_motivos.png` | `05_base.R` |
| A5 | Balance de los medidos según el alza | `03_Resultados/Tablas/05_base/ninos_haz1997_balance.png` | `05_base.R` |
| A6 | Cola del ΔHAZ | `03_Resultados/Tablas/05_base/ninos_dhaz_cola.png` | `05_base.R` |
| A7 | Cuartiles, cuatro especificaciones | `03_Resultados/Tablas/07_cuartiles/ninos_cuartiles_especificaciones.png` | `07_cuartiles.R` |
| A8 | ATE del bosque y MCO con terciles | `03_Resultados/Tablas/10_bosque/ninos_bosque_ate.png` | `10_bosque.R` |
| A9 | GATE en tabla | `03_Resultados/Tablas/11_gate/ninos_gate.png` | `11_gate.R` |
| A10 | BLP conjunta (descriptiva) | `03_Resultados/Tablas/11_gate/ninos_blp.png` | `11_gate.R` |
| A11 | Edad con y sin la cola (exploratorio) | `03_Resultados/Tablas/11_gate/ninos_edad_sin_cola_exploratorio.png` | `11_gate.R` |
| A12 | RATE en tabla, con mitades invertidas | `03_Resultados/Tablas/14_rate/ninos_rate.png` | `14_rate.R` |

(Las especificaciones completas del ATE están en la lámina 4; la robustez, en
la 7; el traslape, en la 9; el perfil, en la 14.)

---

## Preguntas probables del profesor

1. **¿Por qué `feols` y no el bosque para el ATE?** El β de MCO es el estimando
   de E-Q, el que replicamos. La pendiente promedio del bosque con tratamiento
   continuo pondera distinto (−0,260 frente a −0,329) y supone un efecto lineal
   en la dosis. El bosque lo usamos para heterogeneidad. *Respaldo: lámina 4.*
2. **¿Es el efecto de la crisis?** No. Todas las comunidades vivieron la
   crisis; identificamos el contraste de más alza frente a menos alza, bajo el
   supuesto de que sin esa diferencia el ΔHAZ habría sido igual dadas las X de
   1997. *Respaldo: láminas 2 y 4.*
3. **¿Por qué errores agrupados por comunidad?** El alza se asigna por
   comunidad y los niños de una comunidad comparten choques. Los EE agrupados
   son 9 a 31 % mayores que los robustos (los de E-Q) en el ATE. El N efectivo son 294
   comunidades. *Respaldo: lámina 4 (EE robustos entre corchetes).*
4. **¿Y el placebo?** Inconcluso: −0,192 (EE 0,117) con controles, p 0,102,
   cerca del 60 % del efecto. No prueba una tendencia previa, pero no la
   descarta; por eso decimos que la dirección es robusta y el tamaño no.
   *Respaldo: lámina 6.*
5. **¿El desgaste es selectivo?** El seguimiento 1997-2000 no depende del alza
   (−0,003, EE 0,017). La medición de 1997 cubrió menos en el cuartil de más
   alza, sobre todo entre provincias (con EF de provincia la pendiente baja a
   −0,045, EE 0,033), sin cambiar la composición. *Respaldo: lámina 3, A4, A5.*
6. **¿Por qué su efecto es mayor que el de E-Q?** Hipótesis no probadas: su
   medida del precio mezcla fuentes distintas en cada año (más ruido, efecto
   atenuado; sin winsorizar el nuestro baja a −0,207) y no usan EF de
   provincia (con ellos el nuestro pasa de −0,24 a −0,34). Los intervalos se
   traslapan. *Respaldo: láminas 4 y 7.*
7. **¿Cómo se concilia con Frankenberg y Thomas (2017), que no ven daño en
   talla?** Ellos comparan zonas (urbano frente a rural); nosotros, el alza del
   precio, que varía sobre todo dentro de provincia. Son contrastes distintos.
   Y en nuestros datos la diferencia urbano-rural tampoco se distingue de cero.
   *Respaldo: láminas 2, 8 y 10.*
8. **¿Por qué terciles dentro de provincia?** La provincia explica el 14,6 % de
   la varianza del alza; con terciles nacionales, provincias enteras caen en
   un extremo y la propensión se pega a 0 o 1 si la provincia está en X. Dentro
   de provincia el traslape queda entre 0,10 y 0,93. *Respaldo: láminas 2 y 9.*
9. **¿Qué significa que la calibración no rechace?** Que no hay evidencia de
   que el orden del bosque capte diferencias reales entre niños (0,124, EE
   0,799; p unilateral 0,438). No prueba que el efecto sea igual para todos:
   con 195 comunidades solo veríamos heterogeneidad grande. *Respaldo:
   láminas 11 y 12.*
10. **¿Qué le recomiendan al cliente?** Vigilar el alza por comunidad y cubrir
    a todos los niños pequeños de las comunidades con más alza; no usar el
    bosque ni excluir por pobreza o zona con esta evidencia. La edad (menores
    de 3) es una pista a confirmar. *Respaldo: láminas 13-15.*

---

## Figuras que faltarían

- **Lámina 11, diferencia mínima detectable:** una gráfica de barras con la MDE
  (≈ 2,8 × EE) de cada contraste (ATE, cinco interacciones, seis GATE, tres
  diferencias de RATE) frente a su estimación puntual. La produciría un script
  del pipeline (p. ej. `02_Scripts/15_potencia.R`) que lea los `.csv` de
  `06_ate`, `09_interacciones_eq`, `11_gate` y `14_rate`, como hoy hace
  `02_Scripts/_exploratorio/mde_potencia.R` en consola.
- **Lámina 1 o 15 (opcional), esquema del diseño:** un diagrama de la
  cohorte (0-5 años en 1997), las dos mediciones y el contraste por comunidad.
  No requiere datos; se puede hacer a mano en las láminas.
