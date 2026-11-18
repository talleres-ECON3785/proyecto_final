# 03 · Estrategia de identificación (versión 2, ampliada)

> No corrí nada sobre los microdatos (la descarga requiere el registro de ustedes en RAND). Este archivo contrasta la hipótesis con la literatura, ordena los diseños posibles y deja las pruebas listas.

## 1. La propuesta y su estimando

- **Tratados:** individuos que en 1997 vivían en comunidades donde el precio del arroz subió más. **Controles:** donde subió menos, parecidos *ex ante*.
- **Supuesto:** condicional en X de 1997, la intensidad del alza es independiente de los resultados potenciales.

Antes de discutir amenazas hay que fijar **qué se estima**, porque cambia según el diseño:

| Versión del tratamiento | Estimando | Supuesto necesario |
|---|---|---|
| Binario: tercil alto vs. bajo | Efecto promedio de estar en una comunidad de alza alta frente a una de alza baja | Independencia condicional (o tendencias paralelas si hay pre-período) |
| Continuo: Δlog(precio) | Respuesta causal promedio a un punto adicional de alza | **Más fuerte.** Callaway, Goodman-Bacon y Sant'Anna muestran que, con dosis continua, las tendencias paralelas estándar identifican el efecto de cada dosis frente a no tratamiento, pero comparar dosis entre sí mezcla efecto causal con sesgo de selección, salvo que se asuman "tendencias paralelas fuertes", que restringen la heterogeneidad del efecto |

Dos consecuencias prácticas:

1. Aquí **no hay grupo sin tratar**: el arroz subió en todas partes. Solo se identifica el efecto de más alza frente a menos alza, nunca el efecto total de la crisis.
2. El coeficiente continuo de Elmira y Qaim (−0,135 por +100 %) descansa en el supuesto fuerte. La versión por terciles es más defendible y es la que pide un árbol causal. Reportar las dos y decir cuál supuesto usa cada una.

## 2. Veredicto

La hipótesis **es viable y tiene precedente directo**, pero "eran parecidos ex ante" no basta. La literatura da tres motivos para ser exigentes:

- Los precios se movieron junto con otros choques. Levinsohn, Berry y Friedman advierten que sequía e incendios pudieron subir precios por su cuenta. Jayachandran muestra que el humo de fines de 1997 tuvo efectos propios sobre la primera infancia, mayores en zonas pobres. Rukumnuaykit, con la IFLS, encuentra que la crisis financiera y la crisis de sequía/humo afectan la mortalidad infantil con patrones urbano/rural distintos.
- El efecto de largo plazo está en disputa: Frankenberg y Thomas casi no encuentran daño duradero con un diseño de cohortes; Elmira y Qaim sí, con precios.
- El signo del efecto depende de la posición del hogar en el mercado de arroz (Friedman y Levinsohn; Yamauchi y Larson).

## 3. Menú de diseños usados en la literatura

| # | Diseño | Quién | Qué elimina | Qué no elimina | Uso para nosotros |
|---|---|---|---|---|---|
| A | Antes-después con panel individual | Frankenberg, Smith y Thomas; Thomas et al.; Smith et al. | Heterogeneidad fija individual | Tendencia y todo choque simultáneo; no hay control | Solo descriptivo |
| B | Intensidad geográfica × panel de dos períodos (efectos fijos individuales) | Elmira y Qaim (precio comunitario); Friedman y Thomas (gasto provincial) | Diferencias fijas entre individuos y comunidades | Choques locales que coinciden con el alza; requiere resultado medido antes y después | **Replicación del ATE** (HAZ 1997-2000) y **salud mental de adultos** (ítems GHQ 1993-2000) |
| C | Cohorte × intensidad geográfica | Maccini y Yang (lluvia al nacer, IFLS); Adhvaryu, Fenske y Nyshadham (precio del cacao al nacer × región productora); Frankenberg y Thomas (cohorte × pobreza × zona) | Diferencias fijas entre comunidades (efecto fijo de comunidad) y entre cohortes | Choques locales que afecten distinto a las cohortes jóvenes; migración selectiva | **Diseño principal recomendado para resultados que solo se miden de adulto** (educación, cognición, CES-D 2014) |
| D | Exposición del hogar = precio local × posición neta en el bien | Friedman y Levinsohn (variación compensatoria); Yamauchi y Larson (alza 2007/08 × hogar productor o no) | Con efectos fijos de comunidad: **todo** choque común a la comunidad (sequía, humo, disturbios, política local) | Diferencias no observadas entre compradores y productores que interactúen con la crisis | **Respaldo principal** y fuente del modificador clave |
| E | Choque autorreportado | Robustez de Elmira y Qaim | — | Endógeno, sesgo de recuerdo | Solo robustez |
| F | Medidas alternativas de intensidad | Precios BPS por ciudad (Friedman y Levinsohn); luces nocturnas 1996-98 por kabupaten (JDE 2026) | Error de medición del precio IFLS | Miden cosas distintas: precio vs. actividad económica | Robustez; las luces capturan el choque de ingreso, no el de precio |

### Qué nos enseña cada precedente

- **Maccini y Yang (2009).** Enlazan lluvia del año y lugar de nacimiento con resultados adultos en la IFLS 2000. La variación es desviación respecto a la norma local, así que el lugar se controla solo. Encuentran efectos en mujeres y no en hombres. Lección: usar la **desviación local** (cambio de precio, no nivel) y abrir por sexo.
- **Adhvaryu, Fenske y Nyshadham (2019).** Precio real del cacao en la primera infancia × nacer en región cacaotera. Las regiones no cacaoteras funcionan como grupo de comparación porque el precio no les mueve el ingreso. Lección directa: **los productores netos de arroz pueden ser nuestro grupo de comparación interno** (o incluso un grupo con signo contrario).
- **Yamauchi y Larson (2019).** En Indonesia, el alza de 2007/08 frena el crecimiento solo en hogares que no producen alimentos. Su prueba de validez es replicable: el cambio de precio local no se correlaciona con la proporción de hogares productores ni con la nutrición promedio inicial de la aldea. Lección: correr exactamente esa prueba para 1997-2000.
- **Frankenberg y Thomas (2017).** Construyen el contrafactual de cada cohorte con la tendencia de las cohortes vecinas. Con efectos fijos de hogar (hermanos) el efecto cae 40 %. Lección: comparar **hermanos** de distinta edad en 1998 es un control potente y disponible.
- **Rukumnuaykit (2003) y Jayachandran (2009).** La sequía y el humo son medibles y tienen geografía propia. Lección: no basta con "controlar por provincia"; incluir indicadores de exposición a humo y sequía o excluir las islas más afectadas por los incendios como robustez.

## 4. Amenazas, ordenadas por gravedad

1. **Choques simultáneos correlacionados con el precio** (sequía, humo, disturbios, salario formal). Solución: diseño D con efectos fijos de comunidad; controles de sequía y humo; excluir Sumatra y Kalimantan.
2. **Urbano/rural.** La crisis fue más urbana. Solución: estimar dentro de zona; verificar traslape.
3. **Posición neta en arroz.** Mezcla signos opuestos. Solución: tratarla como modificador, no como ruido.
4. **Reversión a la media del precio base.** Solución: controlar por precio de 1997; cambio en logaritmos.
5. **Error de medición.** Precio de 2000 en vez del pico; informantes sobre-reportan. Sesga a cero. Solución: mediana de fuentes; contraste con BPS.
6. **Respuesta de política.** BULOG y arroz subsidiado dirigidos a zonas golpeadas. Atenúa el efecto: lo estimado es neto de política.
7. **Migración y desgaste selectivos.** Frankenberg y Thomas documentan migración urbano-rural como respuesta. Solución: tratamiento por residencia de 1997; comparar desgaste por tercil.
8. **Pocas unidades independientes** (≈ 312 comunidades, 13 provincias). Solución: inferencia por comunidad; árboles pequeños.

## 5. Plan de verificación contra los datos

| # | Prueba | Qué muestra | Esfuerzo |
|---|---|---|---|
| 1 | Distribución de Δlog(precio) y descomposición de varianza entre/dentro de provincia y zona | Si hay variación utilizable dentro de provincia | Bajo |
| 2 | Balance de X de 1997 por tercil (diferencias estandarizadas) | Qué tan distintos son tratados y controles | Bajo |
| 3 | Traslape del propensity score | Dónde hay soporte común | Bajo |
| 4 | **Tendencias previas:** cambio 1993→1997 del resultado sobre Δprecio 1997→2000 | Debe ser cero. La más convincente | Medio |
| 5 | **Prueba de Yamauchi-Larson:** Δprecio sobre proporción de hogares productores y nutrición promedio de 1997 | Debe ser cero | Bajo |
| 6 | Placebo de resultado: estatura de quienes tenían > 25 años en 1997 | Debe ser cero | Bajo |
| 7 | Placebo de cohorte: adolescentes de 12-17 en 1997 para estatura | Debe ser menor que para 0-5 | Medio |
| 8 | Hermanos: efecto fijo de hogar, edad en 1998 × intensidad | Elimina todo lo fijo del hogar | Medio |
| 9 | Robustez de medida: precio real, BPS, luces nocturnas; excluir Sumatra/Kalimantan | Estabilidad | Medio |
| 10 | Sensibilidad a no observables (`sensemakr`) | Qué tan fuerte tendría que ser un confusor omitido | Bajo |

Las pruebas 1-5 se pueden llevar a la asesoría de semana 15. En el Laboratorio 10 ya usaron `fixest::feols()` con errores agrupados; las pruebas 4, 5, 6 y 8 son regresiones de ese tipo (nombres de variables ilustrativos):

```r
# 4. Tendencias previas (comunidad): debe ser ~0
feols(d_resultado_9397 ~ dlog_arroz_9700 + log_precio97 | provincia^urbano,
      data = panel_com, cluster = ~commid97)

# 5. Prueba tipo Yamauchi-Larson
feols(dlog_arroz_9700 ~ share_productores97 + haz_medio97 | provincia^urbano,
      data = panel_com, vcov = "hc1")

# C. Cohorte x intensidad con efectos fijos de comunidad y de cohorte
feols(cesd_2014 ~ i(expuesto_0a5, dlog_arroz_9700) + mujer | commid97 + cohorte,
      data = adultos14, cluster = ~commid97)

# D. Comprador neto vs. productor dentro de comunidad
feols(haz_2014 ~ comprador_neto97 + educ_madre + log_pce97 | commid97,
      data = ninos, cluster = ~commid97)
```

## 6. Diseño recomendado

1. **Replicación (diseño B):** panel 1997-2000 con efectos fijos individuales, tal como Elmira y Qaim. Meta: β ≈ −0,135.
2. **Largo plazo (diseño C):** cohortes expuestas a 0-5 años vs. cohortes mayores, por intensidad del alza, con efectos fijos de comunidad y cohorte. Es más creíble que el corte transversal de Elmira y Qaim para 2014 porque absorbe todo lo fijo de la comunidad.
3. **Heterogeneidad (árbol y bosque causal):** tratamiento binario por terciles sobre la cohorte expuesta, con X de 1997. Para acercarlo al diseño C, incluir como covariable el **promedio del resultado de la cohorte mayor en la misma comunidad** (hace el papel de resultado rezagado).
4. **Respaldo (diseño D):** comprador neto vs. productor neto dentro de comunidad.

## 7. ¿Usar datos de otros países como respaldo de identificación?

### Qué podría significar

| Variante | Idea | Datos candidatos |
|---|---|---|
| (a) País de control | Comparar cohortes indonesias con las mismas cohortes de un país poco afectado: diferencias en diferencias entre países, o control sintético | China: CHNS (1989, 1991, 1993, 1997, 2000, 2004…), panel público y gratuito con antropometría en todas las olas |
| (b) Réplica externa | Repetir el diseño (precio local × cohorte) en otro país golpeado | Tailandia: Townsend Thai, línea base de mayo de 1997 y re-encuesta anual en 4 provincias |
| (c) Contraste de mecanismo | Donde los hogares venden arroz, el alza debería tener signo contrario | Tailandia, misma fuente |

### Evaluación crítica

**Lo que ganaría la identificación**

- (a) Responde algo que el diseño interno no puede: el efecto *total* de la crisis frente a un mundo sin crisis, porque dentro de Indonesia no hay grupo sin tratar.
- (c) Sería una prueba elegante del canal de precios.

**Por qué no lo recomiendo como respaldo**

1. **Responde otra pregunta.** La amenaza central es que, *dentro* de Indonesia, el alza del arroz coincide con otros choques locales. Un país de control no dice nada sobre eso. No respalda la hipótesis del equipo; la reemplaza por una comparación entre países.
2. **Un solo tratado.** Con Indonesia frente a China hay dos conglomerados. No hay inferencia estadística válida; el control sintético necesita varios donantes y una serie larga pre-choque, y aquí hay tres o cuatro olas.
3. **Confusores a nivel país peores que los locales.** En 1998 Indonesia vivió además la caída de Suharto, la sequía y los incendios; China estaba en plena transición nutricional y de crecimiento. Las tendencias paralelas entre países son menos creíbles que entre comunidades indonesias.
4. **Tailandia tampoco es control:** también sufrió la crisis. Sirve para (b) o (c), no para (a).
5. **Los resultados no son comparables.** El CES-D de la IFLS no tiene equivalente directo en esas encuestas para las mismas cohortes y años; las pruebas cognitivas difieren. Solo la antropometría es armonizable, y la CHNS no tiene pesos muestrales ni es representativa a nivel nacional. La encuesta tailandesa se centra en finanzas del hogar y cubre cuatro provincias.
6. **Costo.** Segundo registro y descarga, otra estructura de archivos, armonizar cohortes, edades y z-scores. Estimo 1-2 semanas adicionales sobre las 2 que ya toma la IFLS. No cabe antes de la semana 16 y duplica el `README` reproducible.
7. **Riesgo en la sustentación.** El enunciado evalúa el dominio técnico bajo preguntas. Un segundo país mal armonizado abre más flancos de los que cierra.

**Qué sí hacer con otros países, a costo casi cero**

- **Referentes de magnitud:** citar Adhvaryu et al. (Ghana), Maccini y Yang, y la revisión de Ferreira y Schady para decir si nuestros efectos son plausibles.
- **Una lámina descriptiva** con series agregadas (PIB per cápita, inflación de alimentos) de Indonesia frente a sus vecinos, solo para ubicar al cliente.
- Mencionar (a) y (c) como **extensión futura**, con las razones de arriba.

**Respaldos mejores y más baratos, todos dentro de la IFLS**

| Respaldo | Qué controla | Costo adicional |
|---|---|---|
| Cohortes mayores de la misma comunidad (diseño C) | Todo lo fijo de la comunidad | Bajo |
| Hermanos de distinta edad (efecto fijo de hogar) | Todo lo fijo del hogar | Bajo |
| Productores netos como comparación interna (diseño D) | Todo choque común a la comunidad | Medio |
| Tendencias previas 1993-1997 | Selección sobre trayectorias | Medio |
| Medidas alternas: precios BPS, luces nocturnas | Error de medición | Medio |

**Conclusión:** otros países, no como identificación. La variación que identifica debe seguir siendo interna; el respaldo debe venir de cohortes, hermanos y productores netos.
