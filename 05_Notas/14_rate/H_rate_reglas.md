# El bosque no prioriza mejor que las reglas simples: ninguna de las tres diferencias de AUTOC (bosque − pobre, − urbano, − comprador neto) pasa Holm, y el AUTOC del bosque solo no se distingue de cero

- **Estado:** vigente
- **Etapa / alcance:** H; contraste entre comunidades del tercil alto y bajo del alza
- **Script de origen:** `02_Scripts/14_rate.R`
- **Hipótesis relacionada:** pregunta 3 (familia F3, m = 3). Ninguna diferencia pasa Holm
- **Última verificación:** 2026-11-22, con `02_Scripts/14_rate.R` (P4.2)

## Evidencia

- `03_Resultados/Tablas/14_rate/ninos_rate.{png,csv}`
- `03_Resultados/Figuras/14_rate/ninos_rate_toc.png`

Versión pre-registrada (pre-registro §4): τ̂ de un bosque entrenado en la mitad
1 de las comunidades; RATE con AUTOC sobre los puntajes doblemente robustos de
un bosque de evaluación en la mitad 2 (834 niños en 98 comunidades; ningún niño
perdido por NA en las reglas). Tercil alto frente a bajo del alza dentro de
provincia. Bootstrap de grf agrupado por comunidad, R = 500.

**Escala de daño:** el bosque de evaluación usa Y = −ΔHAZ, así que AUTOC > 0 =
la regla encuentra a niños con más pérdida de HAZ que el promedio. Chequeo
numérico: con Y = +ΔHAZ el AUTOC del bosque es −0,116, el mismo número con el
signo cambiado (columna `autoc_bosque_y_talla` del `.csv`).

| Prioridad | AUTOC (EE) | p | p Holm (F3) | Mitades invertidas (EE) |
|---|---:|---:|---:|---:|
| Bosque (−τ̂) | 0,116 (0,116) | 0,313 | — | 0,196 (0,100) |
| Pobre | −0,092 (0,082) | 0,263 | — | 0,029 (0,078) |
| Urbano | 0,039 (0,059) | 0,504 | — | −0,010 (0,067) |
| Comprador neto | 0,046 (0,052) | 0,376 | — | 0,021 (0,047) |
| Bosque − pobre | 0,208 (0,150) | 0,164 | 0,492 | 0,167 (0,131) |
| Bosque − urbano | 0,077 (0,119) | 0,515 | 1,000 | 0,206 (0,111) |
| Bosque − comprador neto | 0,070 (0,117) | 0,548 | 1,000 | 0,176 (0,100) |

- **Mitades invertidas** (robustez, sin Holm; 766 niños en 97 comunidades, 2
  perdidos por NA): todas las diferencias positivas; las de menor p son
  bosque − urbano (p 0,064) y bosque − comprador neto (p 0,078); el
  AUTOC del bosque solo, 0,196 (p 0,050). Promedio de las dos versiones
  (columna `promedio_dos_mitades`): AUTOC del bosque 0,156.
- **Propensiones** de la mitad de evaluación entre 0,136 y 0,841 (0,136 a
  0,886 en la invertida): sin valores extremos.

## Qué dice, en lenguaje intuitivo

- La prueba simula a la agencia escogiendo a quién atender primero según una
  regla, y mira si los escogidos de verdad sufrieron más daño que el promedio.
- Priorizar con el bosque da, en la estimación puntual, algo de ventaja sobre
  las tres reglas simples, pero esa ventaja es pequeña frente a su margen de
  error y no se distingue de cero después de corregir por mirar tres
  comparaciones. Tampoco se distingue de cero que el bosque encuentre a los más
  dañados (AUTOC 0,116, EE 0,116).
- Priorizar por pobreza da, si acaso, lo contrario (los pobres con algo menos
  daño que el promedio), también sin distinguirse de cero.
- Al invertir las mitades, el bosque sale algo mejor, pero eso no es la prueba
  pre-registrada y tampoco pasa un umbral corregido.

## Por qué importa en el estudio

- **Pregunta 3:** con esta evidencia el bosque no supera a las reglas simples.
  Es coherente con la calibración (`05_Notas/12_calibracion/H_calibracion_nulo.md`:
  la predicción diferencial no rechaza) y con los GATE (`05_Notas/11_gate/`:
  ningún grupo difiere tras Holm).
- **Para el cliente:** no hay respaldo para preferir un algoritmo sobre una
  regla simple, ni una regla simple sobre otra, para focalizar dentro de los
  niños expuestos. Es la lámina del nulo.
- Con unas 98 comunidades por mitad, se esperaba poca potencia (`CLAUDE.md`
  §5.6). El signo de la diferencia bosque − regla es positivo en las seis
  estimaciones (dos versiones × tres reglas); se dice como estimación puntual,
  no como evidencia.

## Límites e incertidumbre

- Cada mitad tiene unas 100 comunidades: los EE del AUTOC son del orden del
  ATE del bosque (−0,184 en escala de talla).
- El resultado depende de la partición al azar: las dos versiones dan cifras
  distintas (0,116 frente a 0,196 para el bosque). No se promedió sobre muchas
  particiones (no estaba pre-registrado).
- En escala de daño y con tratamiento por terciles, la TOC se lee como ganancia
  relativa entre reglas, no como casos de desnutrición evitados (pre-registro
  §4).
- El p de la diferencia usa la aproximación normal con el EE del bootstrap.

## Historial

- 2026-11-22: creación (P4.2).
