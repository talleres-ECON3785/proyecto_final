# 05 · Salud mental y texto como datos

## El problema de entrada

La idea de "evaluar dimensiones cualitativas de salud mental con texto" choca con un hecho: **en la documentación que revisé, la IFLS mide salud mental con ítems cerrados, no con respuestas abiertas.** No encontré evidencia de texto libre de los encuestados en los archivos públicos. No pude abrir los microdatos, así que esto hay que confirmarlo (ver "Verificación" abajo), pero no conviene que el proyecto dependa de que ese texto exista.

## Qué sí hay sobre salud mental en la IFLS

| Ola | Instrumento | Quién |
|---|---|---|
| 1993 | Ítems adaptados del GHQ: tristeza, ansiedad, insomnio, fatiga, irritabilidad, dolores ("últimas 4 semanas"; a menudo/a veces/nunca) | Adultos |
| 1998 (IFLS2+) | Los mismos | Submuestra 25 %; no pública |
| 2000 | Solo tristeza, ansiedad, insomnio | Adultos |
| 2007 | CES-D de 10 ítems (sección KP, libro 3B) | 15+ |
| 2014 | CES-D-10, más personalidad (Big Five), afecto positivo/negativo, calidad del sueño | 15+ |

Consecuencias:

- Los niños de 0-5 en 1997 tienen CES-D en 2014 (17-23 años) → **resultado de largo plazo válido** para los árboles causales. No tienen línea base de salud mental (eran bebés); se puede controlar por la de la madre en 1993.
- Para adultos, GHQ (1993/2000) y CES-D (2007/2014) no son la misma escala. Estandarizar dentro de ola y hablar de "síntomas", no de niveles comparables.
- Punto de corte usual CES-D-10 ≥ 10; reportar también el puntaje continuo. La escala tiene ítems de baja calidad psicométrica en Indonesia según un estudio IRT con IFLS5, aunque la confiabilidad global es aceptable.

## Verificación rápida de si hay texto en la IFLS

```r
library(haven); library(purrr)
archivos <- list.files("IFLS5/hh", pattern = "\\.dta$", full.names = TRUE)
texto <- map_dfr(archivos, \(f) {
  d <- read_dta(f, n_max = 2000)
  chr <- names(d)[map_lgl(d, is.character)]
  tibble(archivo = basename(f), var = chr,
         largo_medio = map_dbl(chr, \(v) mean(nchar(d[[v]]), na.rm = TRUE)))
})
dplyr::filter(texto, largo_medio > 15)   # candidatos a texto libre
```

Candidatos posibles: respuestas "otro, especifique", notas del entrevistador (libro CP) y descripciones de ocupación. Si aparecen, serán frases cortas en **bahasa indonesia**.

## Tres formas de incorporar texto, de más a menos recomendada

### Opción A · Texto externo para medir la intensidad "narrativa" de la crisis por región (recomendada)
- **Corpus:** prensa y reportes de 1997-1999 con referencia geográfica (archivos de prensa indonesia en inglés o bahasa; reportes de situación de FAO/PMA/OCHA en ReliefWeb; informes de SMERU y del Banco Mundial sobre la crisis).
- **Método del curso:** limpieza y tokenización → modelo de tópicos (LDA) → proporción de tópicos "escasez/precio de alimentos", "desempleo", "disturbios", "sequía/incendios" por provincia y trimestre.
- **Uso:** (i) validar el tratamiento (¿las comunidades con mayor Δprecio están en provincias donde la prensa habla más de escasez de arroz?); (ii) **separar el choque del arroz de los choques simultáneos** (disturbios, sequía), que es la principal amenaza del archivo 03; (iii) covariable de heterogeneidad en el árbol.
- **Costo:** conseguir el corpus es lo incierto. Definir en 2-3 días si es factible; si no, pasar a C.

### Opción B · Texto libre de la IFLS, si existe
- Solo si la verificación de arriba encuentra campos con contenido relevante.
- Método: tokenización en bahasa (lista de *stopwords* indonesia; *stemming* con Sastrawi), frecuencias y tópicos.
- Riesgo alto de que sean pocas palabras por registro; LDA funciona mal con textos tan cortos.

### Opción C · "Dimensiones cualitativas" sin texto: estructura de los ítems
- Tratar los 10 ítems del CES-D (más afecto positivo/negativo y sueño en 2014) como un perfil y extraer dimensiones con análisis factorial o *clustering* (afecto depresivo, síntomas somáticos, afecto positivo).
- Estimar CATEs por dimensión: ¿el choque deja huella en síntomas somáticos más que en ánimo?
- No es texto como datos, pero responde la pregunta sustantiva del equipo y es totalmente factible con lo que hay.

## Recomendación

Plan base: **Opción C** garantizada + **Opción A** como componente de texto si el corpus se consigue esta semana. Presentar la B solo si aparece texto útil. Decirle al profesor en la asesoría, de frente, que la IFLS no trae narrativas de salud mental y preguntarle si A cumple con lo que él espera del bloque de texto.

## Cautelas

- Salud mental a los 17-23 años depende de muchas cosas ocurridas entre 1998 y 2014. El efecto esperado es pequeño y la potencia baja; tratarlo como resultado **exploratorio**.
- Sesgo de reporte: Friedman y Thomas controlan por religión porque afecta cómo se reportan síntomas.
- No presentar puntajes de tamizaje como diagnósticos.
