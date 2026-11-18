# 05 · Salud mental como extensión opcional (versión 4)

> Versión 4, 17-nov-2026. Se mantiene la recomendación de la v3 (11-nov): **salud mental es extensión opcional, sin CATEs**. Falta que el equipo la confirme. Cambios: (i) la tabla de medidas se corrige con la revisión de las cinco olas (S = `01_Datos/00_sintesis_revision_IFLS.md`); (ii) Friedman y Thomas (2009) se cita con página, verificado contra el PDF; (iii) se corrige la descripción de 1993 como «GHQ» (pendiente de `CLAUDE.md` §10).
>
> Se mantiene la decisión del 10-nov: no se procesa texto. La IFLS mide salud mental con ítems cerrados.

## 1. Por qué no entra al núcleo

- **La referencia es descriptiva.** Friedman y Thomas (2009) documentan un aumento grande y persistente de la angustia. La tristeza pasa de cerca de 12 % a casi 30 % en hombres y de 16 % a 41 % en mujeres entre 1993 y 1998 (p. 61), y sigue alta en 2000 (p. 62). Pero la exposición es el cambio del gasto medio en 13 provincias por zona: significativa en lo urbano (R² = 0,34) y no en lo rural (p. 72-74). No hay un efecto con precio comunitario que replicar.
- **La medida armonizable es pobre.** Solo 3 ítems son comunes a 1993 y 2000: insomnio, tristeza y ansiedad (S §7.2).
- **No hay ventana de 1997.** La ola de 1997 no trae ítems psicológicos (F-T 2009, p. 60; S §7.2), y la de 1998 no es pública.
- **El cambio de formato confunde.** En 1993 los ítems van en una grilla de síntomas físicos; en 2000, como preguntas sueltas. La prevalencia de tristeza pasa de 15 % a 33 %, y los datos no permiten separar el cambio real del cambio de instrumento (S §7.2).
- **Es ruidosa para un bosque.** Resultado binario o de pocos valores, con ~312 comunidades.

A favor: el índice de 1993 ya existe (`02_Scripts/_exploratorio/01_salud_mental_1993.py` → `01_Datos/02_Procesados/salud_mental_1993.*`: `sm3_93`, `sm6_93`, `triste_93`, `ansioso_93`).

## 2. Qué mide la IFLS (verificado en los datos; S §7.2)

| Ola | Archivo | Instrumento | Escala | Quién |
|---|---|---|---|---|
| 1993 | `buk3kk2` | **6 síntomas** de la sección KK (insomnio, fatiga, irritabilidad, dolores, tristeza, ansiedad). F-T 2009 los describen como «adaptados del GHQ» (p. 60); **no es el GHQ completo** | 1 a menudo / 3 a veces / 5 nunca; 4 semanas | Submuestra del libro III (12.985 respondientes) |
| 1997 | — | **Sin ítems** | — | — |
| 2000 | `b3b_kk` (`kk04`-`kk11`) | **8 ítems**; 3 comunes con 1993 | 1/3/5; 4 semanas | Todos los adultos del libro 3B (25.470) |
| 2007 | `b3b_kp` | CES-D-10 (`kptype` A-J), `kp01` sí/no + `kp02` frecuencia. **Etiquetas del codebook erradas: usar el cuestionario** | Semana anterior | 29.029 |
| 2014 | `b3b_kp` | CES-D-10, **solo `kp02`** («no» y «≤ 1 día» en la misma categoría) | Semana anterior | 31.447 |

El CES-D de 2007 y el de 2014 tienen estructuras de respuesta distintas. Se estandariza dentro de cada ola y no se comparan niveles.

## 3. Dos preguntas posibles (exploratorias)

**P1 · Adultos, 1993-2000 (prioritaria dentro de la extensión).** Panel de dos periodos con EF individuales (diseño B de `03`). Resultado: índice de los 3 ítems comunes, o cada ítem por separado. Exposición: Δlog del precio del arroz de la comunidad de 1997.
- **Aporte:** pasar de 13 provincias a ~312 comunidades.
- **Modificadores pre-declarados** (de F-T 2009, sin bosque): rurales sin tierra (+19 % tristeza y +18 % ansiedad frente a los rurales con tierra después de la crisis, p. 71); baja educación (más ansiedad, p. 70); mujeres; 60+ (p. 69); urbanos.
- **Placebo:** salud general autorreportada, que casi no cambió (F-T 2009, p. 62).

**P2 · Niños de la crisis, CES-D 2014.** Cohorte 0-5 en 1997 (2.578 con CES-D; S §4.3) frente a las cohortes mayores de la misma comunidad (diseño C). Precedente de magnitud: Adhvaryu, Fenske y Nyshadham (2019, Ghana; sin PDF local). Solo como apéndice.

## 4. Cautelas

Potencia baja. Mortalidad y migración selectivas. Sesgo de reporte por educación. Las comparaciones múltiples entre ítems se corrigen. Son tamizajes de síntomas, no diagnósticos (F-T 2009, nota 5, p. 60).

## 5. Qué no está verificado

- Que los 3 ítems «comunes» midan lo mismo con formatos distintos.
- Christian, Hensel y Roth (2019) y los estudios descriptivos del CES-D con IFLS5: sin PDF local.
- Los módulos vecinos de 2014 (afecto, personalidad, sueño) no se revisaron.
