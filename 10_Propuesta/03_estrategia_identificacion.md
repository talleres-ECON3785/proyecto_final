# 03 · Estrategia de identificación (versión 4)

> Versión 4, 17-nov-2026. Cambios frente a la v2: (i) se conecta cada diseño con la forma en que entra al bosque causal (`04`, §5.2); (ii) se incorporan los hallazgos de la revisión de las cinco olas (fechas de 1998, fuentes de precio que cambian entre olas, `commid97` faltante); (iii) los precedentes se citan con página, verificada contra el PDF cuando lo hay; (iv) la evaluación de otros países se resume (la decisión del 10-nov se mantiene).

## 1. Estimando

- **Tratados:** personas que en 1997 vivían en comunidades del tercil alto del cambio del precio del arroz 1997→2000. **Controles:** las del tercil bajo. El tratamiento se asigna por `commid97`.
- **No hay comunidades sin tratar.** El precio nominal subió en casi todas: media +83 %, mínimo −17 % (Elmira y Qaim 2026, cuadro 1). Se identifica el efecto de **más alza frente a menos alza**, no el de la crisis.

| Versión del tratamiento | Estimando | Supuesto |
|---|---|---|
| Terciles (alto frente a bajo) | Efecto de vivir en una comunidad de alza alta frente a una de alza baja | Independencia condicional en X de 1997 (o tendencias paralelas con pre-período) |
| Continuo: Δlog(precio) | Respuesta causal promedio por unidad de alza | Más fuerte: «tendencias paralelas fuertes» (Callaway, Goodman-Bacon y Sant'Anna; NBER WP 32117, arXiv v8 de dic-2025) |

El coeficiente de E-Q (−0,135 por +100 %) es de dosis continua. Reportamos ambos y decimos qué supuesto usa cada uno.

## 2. Por qué no basta con «eran parecidos ex ante»

1. **Choques simultáneos.** La sequía de El Niño y los incendios golpearon la agricultura justo antes: la producción de arroz cayó 4 % en 1997, con incendios en Sumatra, Kalimantan y Sulawesi (Frankenberg, Smith y Thomas 2003, p. 281 y 283, nota 1). Jayachandran (2009) muestra efectos propios del humo en la primera infancia. En los datos, 431 de 960 menciones de pérdida de cosecha en 1997 dicen «demasiado seco» (`b2_ge`; síntesis §7.7).
2. **La exposición se confunde con lo urbano.** La crisis fue más urbana (FST p. 295; F-L p. 408-409) y el arroz pesa más en el gasto de los pobres (más de 25 % en el decil inferior; F-L p. 402).
3. **El signo depende de la posición en el mercado de arroz.** Los productores ganaron (FST p. 295; F-T 2017 p. 6-7; F-L p. 414).
4. **Respuestas de los hogares y de la política.** Migración urbano→rural, venta de oro (F-T 2017 p. 10-11), becas escolares desde 1999 (p. 10) y alimentación complementaria focalizada (Giles y Satriawan 2015, según E-Q p. 5). Lo estimado es neto de estas respuestas, y algunas son modificadores.
5. **Medición del tratamiento.** El precio de 2000 no es el pico (no hay precios de 1998-99 en la descarga pública). Las fuentes cambian entre olas: en 2000 el libro PKK no trae precios y en 2007 desaparecen posyandu y `bk2_hpj` (síntesis §7.6). Además, 27 comunidades tienen el libro PKK de 1997 levantado en enero o febrero de 1998, ya en crisis.

## 3. Diseños y cómo entran al bosque

| # | Diseño | Precedente (verificación) | Qué elimina | Qué no elimina | Uso | Forma en el bosque (`04` §5.2) |
|---|---|---|---|---|---|---|
| B | Intensidad × panel de dos periodos con EF individuales | E-Q, ec. 1 (PDF) | Lo fijo de la persona y la comunidad | Choques locales simultáneos al alza | Replicar el ATE (ΔHAZ 1997-2000) | Y = primera diferencia |
| C | Cohorte × intensidad, EF de comunidad y cohorte | F-T 2017 (tendencia por cohorte, PDF); Maccini y Yang 2009; Adhvaryu et al. 2019 (resumen) | Lo fijo de la comunidad; tendencias comunes entre cohortes | Choques locales que afecten solo a los jóvenes; migración selectiva | **Escolaridad 2014 (primario)**, estatura adulta | Y = resultado − media de la cohorte no expuesta de la comunidad |
| D | Precio local × posición neta, dentro de comunidad | F-L (exposición *ex ante*, PDF); Yamauchi y Larson 2019 (resumen) | **Todo choque común a la comunidad** (sequía, humo, disturbios) | Diferencias no observadas entre compradores y productores | Respaldo principal y modificador H2 | GATE por posición neta + `feols` con EF de comunidad |
| E | Choque autorreportado | Robustez de E-Q (p. 5) | — | Endógeno | Solo robustez | — |
| F | Medidas alternas de intensidad | F-L (precios BPS); JDE 2026 (luces nocturnas) | Error de medición | Miden otras cosas | Robustez opcional | Cambiar W |

### Lecciones de cada precedente

- **E-Q (2026).** Su ecuación 1 es exactamente el diseño B. Replicarla primero valida el pipeline de precios y antropometría. Diferencias que debemos documentar: ellos promedian todas las calidades y fuentes de precio (p. 3); su largo plazo es MCO de corte transversal (asociación, p. 5).
- **F-T (2017).** El contrafactual de cada cohorte es la tendencia de las vecinas. Con EF de hogar (hermanos), el efecto de la cohorte de 8 años cae ~40 % y queda significativo solo al 10 % (p. 14; cuadro 3). Lección: reportar la versión con hermanos (prueba 8).
- **FST (2003) y F-L (2002).** La zona urbana y la producción de alimentos dominan el efecto. Lección: estimar dentro de zona y tratar la posición neta como modificador, no como ruido.
- **Yamauchi y Larson (2019).** El cambio de precio local no debe correlacionarse con la proporción de productores ni con la nutrición inicial. Es la prueba 5.

## 4. Amenazas, ordenadas por gravedad

| # | Amenaza | Evidencia | Mitigación |
|---|---|---|---|
| 1 | Choques simultáneos (sequía, humo, disturbios) | FST p. 283; Jayachandran 2009; `b2_ge` 1997 | Diseño D; controles de sequía (`b2_ge`) y de humo (isla); excluir Sumatra y Kalimantan |
| 2 | Urbano/rural | FST p. 295; F-L p. 408 | Estimar dentro de zona; traslape por zona |
| 3 | Posición neta en arroz | F-L p. 414 | Modificador H2; diseño D |
| 4 | Reversión a la media del precio | — | Controlar log del precio de 1997 |
| 5 | Error de medición del tratamiento | Sin pico 1998-99; fuentes cambiantes; 27 comunidades levantadas en 1998 | Fuentes comunes 1997-2000 (`02` §5); indicador de levantamiento en 1998; versión «réplica E-Q» |
| 6 | Línea base contaminada | 627 hogares entrevistados en 1998; 2.123 mediciones antropométricas de 1997 hechas en 1998 (síntesis §6) | Indicador en X; robustez excluyéndolos |
| 7 | Respuesta de política focalizada | Giles y Satriawan 2015; OPK en 2000 (3.403 hogares; síntesis §7.5) | No controlar por OPK (es posterior); discutir como canal |
| 8 | Migración y desgaste selectivos | Cohorte 0-5: 3.851 en 1997 → 2.846 miembros en 2014, 97 muertos (síntesis §4.3) | Tratamiento por residencia de 1997; desgaste por tercil (prueba 11) |
| 9 | Pocas unidades independientes | 312 comunidades; ~208 en la comparación por terciles | Inferencia por comunidad; árboles pequeños |

## 5. Pruebas contra los datos

| # | Prueba | Debe dar | Esfuerzo | ¿Para la asesoría? |
|---|---|---|---|---|
| 1 | Distribución de Δlog(precio) y su varianza dentro y entre provincias y zonas | Variación útil dentro de provincia | Bajo | Sí |
| 2 | Balance de X de 1997 por tercil (diferencias estandarizadas) | Diferencias pequeñas o ajustables | Bajo | Sí |
| 3 | Traslape (`W.hat`) | Soporte común | Bajo | Sí |
| 4 | **Tendencias previas:** cambio 1993→1997 de HAZ y escolaridad (cohortes mayores) sobre Δprecio 1997→2000 | ≈ 0 | Medio | Sí |
| 5 | **Yamauchi-Larson:** Δprecio sobre la proporción de productores y la HAZ media de 1997 | ≈ 0 | Bajo | Sí |
| 6 | Placebo de resultado: estatura de quienes tenían > 25 años en 1997 | ≈ 0 | Bajo | — |
| 7 | **Bosque placebo** en la cohorte no expuesta (`04` §5.2) | ATE ≈ 0; calibración no rechaza | Medio | — |
| 8 | Hermanos: EF de hogar, edad en 1997 × intensidad | Efecto estable | Medio | — |
| 9 | Robustez de medida: precio real, fuentes alternas, W continuo, sin Sumatra/Kalimantan, sin entrevistas de 1998 | Estabilidad | Medio | — |
| 10 | Sensibilidad (`sensemakr`, ampliación) | Robustez a confusores moderados | Bajo | — |
| 11 | Desgaste: características de 1997 de quienes llegan a 2014, por tercil | Sin diferencias por tercil | Bajo | Sí |

```r
# 4. Tendencias previas (comunidad): debe ser ~0
feols(d_haz_9397 ~ dlog_arroz_9700 + log_p_arroz97 | provincia^urbano,
      data = panel_com, cluster = ~commid97)
# 5. Yamauchi-Larson
feols(dlog_arroz_9700 ~ prop_productores97 + haz_media97 | provincia^urbano,
      data = panel_com, vcov = "hc1")
# B. Replicación de E-Q
feols(haz ~ dlog_arroz_9700:post + controles97:post | pidlink + post,
      data = panel_ninos, cluster = ~commid97)
# C. Cohorte x intensidad
feols(anios_2014 ~ i(expuesto, dlog_arroz_9700) + mujer | commid97 + cohorte,
      data = esc14, cluster = ~commid97)
# D. Comprador vs. productor dentro de la comunidad
feols(anios_2014 ~ comprador_neto97 * expuesto + educ_madre + pctl_pce97 | commid97,
      data = esc14, cluster = ~commid97)
```

## 6. Diseño recomendado (recomendación; decisión del equipo)

1. **Replicación (B):** ΔHAZ 1997-2000 con EF individuales, como E-Q. Meta β ≈ −0,135, con la construcción de precio «réplica E-Q».
2. **Resultado primario (C):** escolaridad completada en 2014, cohortes de 5-21 años en 1997, frente a la cohorte no expuesta de la misma comunidad.
3. **Heterogeneidad:** bosque causal sobre el resultado transformado (`04`).
4. **Respaldo (D):** comprador frente a productor dentro de la comunidad.

## 7. Otros países (decisión del 10-nov, se mantiene)

No sirven como respaldo de identificación: responden otra pregunta (el efecto total frente a un mundo sin crisis), dejan un solo país tratado, los resultados no son comparables (solo la antropometría es armonizable) y cuestan 1-2 semanas. Quedan como **referentes de magnitud** (Adhvaryu et al. 2019; Maccini y Yang 2009) y como extensión futura. El análisis completo está en `_obsoleto/03_estrategia_identificacion_v2.md`, §7.

## 8. Qué no está verificado

- Ninguna prueba se ha corrido.
- La variación del precio dentro de provincia (prueba 1) es el supuesto más importante sin comprobar.
- Yamauchi y Larson (2019), Maccini y Yang (2009), Adhvaryu et al. (2019), Jayachandran (2009) y Giles y Satriawan (2015) se citan sin PDF local.
- No se ha decidido qué cohorte cuenta como «no expuesta» para la escolaridad; 22-30 años en 1997 es una propuesta. Algunos de esa cohorte aún estudiaban en 1998.
