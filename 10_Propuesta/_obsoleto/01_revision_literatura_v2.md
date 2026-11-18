# 01 · Revisión de literatura (versión 2)

> Versión 2, 10-nov-2026. Cambios frente a la v1: (i) se abandona el componente de texto, así que la revisión se reorienta a resultados de largo plazo y a salud mental medida con las escalas de la encuesta; (ii) **todas las referencias fueron verificadas en línea** (revista, volumen, páginas y contenido); ya no hay citas de memoria; (iii) se agrega literatura específica de identificación, que se desarrolla en el archivo 03.

## Qué cambió en el diagnóstico

1. El antecedente directo sigue siendo Elmira y Qaim (2025): variación comunitaria del precio del arroz en la IFLS → talla infantil y adulta.
2. **Hay evidencia de largo plazo que apunta en dirección contraria.** Frankenberg y Thomas (2017) siguen a los niños de 1997 hasta 2014 y casi no encuentran daño duradero en educación, y hasta 2008 no ven efecto en estatura. Strauss et al. (2004) muestran que para 2000 los niveles de vida ya se habían recuperado. El ATE que vamos a replicar está, entonces, **en disputa**: eso hace más valiosa la replicación y obliga a no dar por hecho que hay un efecto.
3. Para salud mental no hay ningún estudio de largo plazo de este choque. Lo más cercano es Friedman y Thomas (2009), que llega hasta 2000, y Adhvaryu, Fenske y Nyshadham (2019), que muestran en Ghana que los precios en la primera infancia dejan huella en la salud mental adulta. Ese es el vacío más claro.

## Los 5 artículos más relevantes sobre el fenómeno

### 1. Elmira y Qaim (2025) — antecedente directo y ATE de referencia
Elmira, E. S. y Qaim, M. (2025). Macroeconomic shocks and long-term nutritional outcomes: Insights from the Asian financial crisis. *Global Food Security*, 48, 100900. <https://www.sciencedirect.com/science/article/pii/S2211912425000756>

- **Diseño:** IFLS 1997, 2000 y 2014; ≈ 2.100 niños de 0-5 años en 1997. Tratamiento = cambio 1997→2000 del precio del arroz en 312 comunidades. Panel con efectos fijos individuales para el corto plazo; MCO de corte transversal para 2014.
- **Resultado:** +100 % de precio nominal ⇒ −0,135 HAZ y +3,5 pp de retraso en talla (−0,251 HAZ con precio real); ≈ −0,65 cm de estatura adulta; más obesidad en la cohorte de 3-5 años.
- **Heterogeneidad (subgrupos predefinidos):** mayor en zona urbana, madres con primaria o menos y niños varones.
- **Límites:** precio de 2000 como proxy del pico; largo plazo descrito por los autores como asociación; no separan productores netos; solo antropometría.

### 2. Frankenberg y Thomas (2017) — el contrapeso: poco daño de largo plazo
Frankenberg, E. y Thomas, D. (2017). Human Capital and Shocks: Evidence on Education, Health and Nutrition. NBER Working Paper 23347. <https://www.nber.org/papers/w23347>

- **Diseño:** niños de 5-21 años en IFLS2 (1997) seguidos a IFLS5 (2014). Comparan años de educación completados por cohorte contra la tendencia lineal de las cohortes vecinas, separando urbano/rural y cuartil pobre vs. resto (una diferencia en diferencias por cohorte y pobreza).
- **Resultado:** sin desviación de tendencia para los pobres de 7-12 ni de 13-16 años. La excepción es una sola cohorte (8 años en 1997, hogares pobres), que pierde cerca de 2 años de escolaridad; con efectos fijos de hogar el efecto cae ≈ 40 %. Talla-para-edad sin efecto adverso de largo plazo hasta 2008.
- **Por qué importa:** (i) fija la expectativa: un nulo en educación es plausible; (ii) usa zona urbana como proxy de intensidad, no precios; (iii) insiste en que las respuestas de los hogares (venta de oro, migración, reagrupación de hogares, becas temporales) amortiguan el efecto, que es justo lo que un CATE debería capturar; (iv) señala que los consumidores netos de alimentos fueron los golpeados y los productores netos quedaron protegidos o ganaron.

### 3. Friedman y Thomas (2009) — salud mental con las métricas de la IFLS
Friedman, J. y Thomas, D. (2009). Psychological Health Before, During, and After an Economic Crisis: Results from Indonesia, 1993–2000. *World Bank Economic Review*, 23(1), 57-76. WP abierto: <https://openknowledge.worldbank.org/entities/publication/c07de537-45c7-5287-ae1c-95f1d5160f11>

- **Diseño:** los mismos adultos en 1993, 1998 y 2000; ítems adaptados del General Health Questionnaire (tristeza, ansiedad, insomnio en las tres olas). Logit y logit multinomial de transiciones con covariables de 1993.
- **Resultado:** tristeza y ansiedad se duplican aproximadamente entre 1993 y 1998 y apenas bajan en 2000. Más afectados: baja educación, rurales sin tierra, urbanos, provincias más golpeadas.
- **Límites que podemos mejorar:** intensidad medida con 13 promedios provinciales de gasto (endógeno); horizonte hasta 2000. Nosotros podemos usar el precio comunitario (312 unidades) y extender a CES-D 2007 y 2014.

### 4. Friedman y Levinsohn (2002) — quién pierde con el alza de precios
Friedman, J. y Levinsohn, J. (2002). The Distributional Impacts of Indonesia's Financial Crisis on Household Welfare: A "Rapid Response" Methodology. *World Bank Economic Review*, 16(3), 397-423. WP: <https://www.nber.org/papers/w8564>

- **Diseño:** canastas pre-crisis (SUSENAS 1996) × cambios de precio provinciales (ene-1997 a oct-1998, precios de ciudades BPS) ⇒ variación compensatoria por hogar.
- **Resultado:** pierden casi todos; más los pobres urbanos; la producción propia de alimentos protege a los pobres rurales; la geografía importa aun dentro de zona e ingreso; hogares con niños pequeños pierden más.
- **Por qué importa:** es el origen de la idea de exposición = precio local × dependencia del hogar, que proponemos como diseño de respaldo.

### 5. Frankenberg, Smith y Thomas (2003) — heterogeneidad y mecanismos de suavización
Frankenberg, E., Smith, J. P. y Thomas, D. (2003). Economic Shocks, Wealth, and Welfare. *Journal of Human Resources*, 38(2), 280-321. WP: <https://escholarship.org/uc/item/2nt453d4>

- **Resultado:** enorme diversidad en el efecto del choque: devastador para unos hogares, oportunidad para otros. Los hogares se reagrupan, aumentan oferta laboral, recortan semidurables y protegen alimentos; los hogares rurales usan riqueza, sobre todo **oro**, para suavizar consumo.
- **Por qué importa:** es la justificación económica más directa para estimar CATEs y da covariables de heterogeneidad concretas (tenencia de oro, composición del hogar, sector).

## Segunda línea: contexto del choque

| Referencia | Aporte |
|---|---|
| Thomas, D. y Frankenberg, E. (2007). Household Responses to the Financial Crisis in Indonesia. En A. Harrison (ed.), *Globalization and Poverty*, NBER/U. Chicago Press. <https://www.nber.org/system/files/chapters/c0116/c0116.pdf> | Magnitudes 1997-98 y la advertencia de que todo depende de cómo se mida la inflación (precios IFLS ≈ 15 % por encima de BPS; ciudades BPS entre ≈ 50 % y ≈ 90 %). |
| Thomas, D., Beegle, K., Frankenberg, E., Sikoki, B., Strauss, J. y Teruel, G. (2004). Education in a crisis. *Journal of Development Economics*, 74(1), 53-85. | Los hogares pobres protegen la educación de los hijos mayores a costa de los menores. |
| Smith, J. P., Thomas, D., Frankenberg, E., Beegle, K. y Teruel, G. (2002). Wages, employment and economic shocks: Evidence from Indonesia. *Journal of Population Economics*, 15(1), 161-193. | Salarios reales ≈ −40 % con empleo agregado estable. |
| Strauss, J., Beegle, K., Dwiyanto, A., Herawati, Y., Pattinasarany, D., Satriawan, E., Sikoki, B., Sukamdi y Witoelar, F. (2004). *Indonesian Living Standards Before and After the Financial Crisis*. ISEAS/RAND. | A finales de 2000 los niveles de vida habían vuelto a los de 1997 en casi todas las dimensiones. Contexto para esperar efectos de largo plazo pequeños. |
| Levinsohn, J., Berry, S. y Friedman, J. (2003). Impacts of the Indonesian Economic Crisis: Price Changes and the Poor. En Dooley y Frankel (eds.), *Managing Currency Crises in Emerging Markets*, NBER. <https://www.nber.org/papers/w7194> | Los cambios de precio varían mucho por lugar; advierten que sequía e incendios pudieron mover precios de forma independiente. |
| Block, S. A., Kiess, L., Webb, P., Kosen, S., Moench-Pfanner, R., Bloem, M. W. y Timmer, C. P. (2004). Macro shocks and micro outcomes: child nutrition during Indonesia's crisis. *Economics & Human Biology*, 2(1), 21-44. | Corrección frente a la v1: **no usa la IFLS**, sino una encuesta de vigilancia nutricional en Java rural. Peso-para-edad infantil estable; las madres amortiguan (aumenta su delgadez); sube la anemia; peor para cohortes concebidas o destetadas en la crisis. |

## Tercera línea: fuentes de identificación (detalle en el archivo 03)

| Referencia | Qué nos presta |
|---|---|
| Yamauchi, F. y Larson, D. F. (2019). Long-term impacts of an unanticipated spike in food prices on child growth in Indonesia. *World Development*, 113, 330-343. | Mismo país, crisis de precios de 2007/08: el alza daña el crecimiento solo en hogares **no productores**; verifican que el cambio de precio local no se correlaciona con la proporción de productores ni con la nutrición inicial. Plantilla para nuestro diseño de respaldo. |
| Maccini, S. y Yang, D. (2009). Under the Weather: Health, Schooling, and Economic Consequences of Early-Life Rainfall. *American Economic Review*, 99(3), 1006-1026. | IFLS; choque local en el año y lugar de nacimiento → resultados adultos. Diseño cohorte × lugar. Efectos solo en mujeres. |
| Adhvaryu, A., Fenske, J. y Nyshadham, A. (2019). Early Life Circumstance and Adult Mental Health. *Journal of Political Economy*, 127(4), 1516-1549. | Precio de un producto básico en la primera infancia × región → angustia mental severa en la adultez (Ghana). El precedente metodológico para salud mental. |
| Callaway, B., Goodman-Bacon, A. y Sant'Anna, P. (2021-2025). Difference-in-Differences with a Continuous Treatment. arXiv:2107.02637. | Con tratamiento continuo, comparar dosis exige un supuesto más fuerte que tendencias paralelas. |
| Athey, S. y Wager, S. (2019). Estimating Treatment Effects with Causal Forests: An Application. *Observational Studies*, 5, 36-51. | Bosque causal en datos observacionales y con conglomerados. |
| Jayachandran, S. (2009). Air Quality and Early-Life Mortality: Evidence from Indonesia's Wildfires. *Journal of Human Resources*, 44(4), 916-954. | El humo de los incendios de fines de 1997 tuvo efectos propios en la primera infancia, mayores en zonas pobres: es un confusor real y medible. |
| Rukumnuaykit, P. (2003). *Economic Crises and Demographic Outcomes: Evidence from Indonesia*. Tesis doctoral, Michigan State University. | Con IFLS separa la crisis financiera de la crisis de sequía/humo: ambas afectan mortalidad infantil, con patrones urbano/rural distintos. |
| Ferreira, F. y Schady, N. (2009). Aggregate Economic Shocks, Child Schooling, and Child Health. *World Bank Research Observer*, 24(2), 147-181. | Marco teórico: efecto ingreso vs. sustitución; en países pobres salud y educación infantil son procíclicas. |
| "Educational mobility across multiple generations in Indonesia" (2026). *Journal of Development Economics*. <https://www.sciencedirect.com/science/article/pii/S0304387826001513> | Mide la exposición a la crisis con el cambio de **luces nocturnas** 1996-1998 por kabupaten de residencia pre-crisis, con la IFLS. Medida alternativa de intensidad. |
| Christian, C., Hensel, L. y Roth, C. (2019). Income Shocks and Suicides: Causal Evidence from Indonesia. *Review of Economics and Statistics*, 101(5), 905-920. | Choques de lluvia afectan los puntajes de depresión de la IFLS: el CES-D responde a choques económicos. |

## Métodos

- Athey, S. e Imbens, G. (2016). Recursive partitioning for heterogeneous causal effects. *PNAS*, 113(27), 7353-7360. (Base del Laboratorio 09.)
- Wager, S. y Athey, S. (2018). Estimation and Inference of Heterogeneous Treatment Effects using Random Forests. *JASA*, 113(523), 1228-1242. (Base del Laboratorio 10.)
- Kreif, N. et al. (2021). Estimating heterogeneous policy impacts using causal machine learning: a case study of health insurance reform in Indonesia. *Health Services and Outcomes Research Methodology*. <https://doi.org/10.1007/s10742-021-00259-3> (Bosques causales con la IFLS.)

## Vacíos que el proyecto puede llenar

1. **Reconciliar** Elmira-Qaim (efecto) con Frankenberg-Thomas (casi nulo): ¿la diferencia viene de la medida de exposición (precio comunitario vs. zona urbana) o de quiénes cargan el efecto?
2. **CATE basados en datos** para este choque; no encontré ninguno.
3. **Salud mental de largo plazo** (CES-D 2007 y 2014) con exposición por precio comunitario.
4. **Productor neto vs. comprador neto** como modificador, verificado para 2007/08 por Yamauchi y Larson pero no para 1998.

## Resultado de la verificación de las citas de memoria de la v1

| Cita | Estado | Corrección |
|---|---|---|
| Frankenberg, Smith y Thomas (2003), JHR 38(2) | Confirmada: pp. 280-321 | Sube al grupo de los 5 por su relevancia para heterogeneidad |
| Thomas et al. (2004), JDE 74(1), 53-85 | Confirmada | Ninguna |
| Strauss et al. (2004) | Confirmada: ISEAS/RAND/UGM, 402 pp. | Se completa la lista de autores |
| Block et al. (2004) | Confirmada: EHB 2(1), 21-44 | No usa IFLS; es Java rural. Sirve como contexto, no como precedente de diseño |
| Athey e Imbens (2016) | Confirmada: PNAS 113(27), 7353-7360 | Ninguna |
| Wager y Athey (2018) | Confirmada: JASA 113(523), 1228-1242 | Ninguna |
