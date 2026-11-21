# Hallazgos principales de los artículos de referencia

> 18-nov-2026; §2 (F-T 2017) revisada el 20-nov-2026 contra la versión final de
> noviembre de 2017 (`c13829.rev1.pdf`). Resumen de los cinco PDF de
> `07_Recursos/Articulos/` (solo en local). Para cada estudio: qué hace, qué encuentra y cómo se relaciona con el
> proyecto. Las cifras llevan página o cuadro del PDF (páginas impresas). El
> detalle completo y la tabla de verificación están en
> `10_Propuesta/01_revision_literatura.md`; la matriz de heterogeneidad, en
> `10_Propuesta/04_heterogeneidad_bosques_honestos.md`.
>
> Siglas: **E-Q** = Elmira y Qaim (2026); **F-T 2017** = Frankenberg y Thomas
> (2017); **FST** = Frankenberg, Smith y Thomas (2003); **F-L** = Friedman y
> Levinsohn (2002); **F-T 2009** = Friedman y Thomas (2009). La §7 (Widyanti
> et al. 2009, línea de pobreza) se agregó el 20-nov-2026.

---

## 1. Elmira y Qaim (2026): el ATE que replicamos

*Macroeconomic shocks and long-term nutritional outcomes: Insights from the Asian
financial crisis.* *Global Food Security*, 48, 100900.

**Qué hacen**

- IFLS 1997, 2000 y 2014 (p. 2). Niños de 0-5 años en 1997, medidos de nuevo en
  2000 (3-8 años) y en 2014 (17-23 años).
- Exposición: cambio del precio comunitario del arroz 1997→2000 en las 312
  comunidades. El precio es un promedio de calidades, vendedores y grupos de
  mujeres (p. 3). Usan 2000 porque la IFLS no tiene precios de 1999, el pico.
- Corto plazo: panel con efectos fijos individuales y controles de 1997
  interactuados con el año (ec. 1, p. 3). Largo plazo: corte transversal en 2014
  con HAZ inicial y EF regionales, que **ellos mismos llaman asociación** (ec. 3,
  p. 4-5).
- Robustez: un indicador alternativo de crisis (pérdida de ingreso o empleo
  reportada en 2000), que da −0,22 HAZ (p. 5; cuadro A1).

**Qué encuentran**

- +100 % de precio nominal ⇒ **−0,135 HAZ** y **+3,5 pp de retraso en talla**;
  −0,251 HAZ con precio real (p. 1 y 5; figs. 3-4).
- Sin efecto significativo en WHZ ni BMIZ; sí +3 pp de sobrepeso infantil (p. 5).
- Cambio medio del precio: +83 % nominal (DE 0,67), −0,06 real (cuadro 1, p. 4).
  En el 30 % de las comunidades el precio real de 2000 seguía por encima del de
  1997 (p. 3).
- Heterogeneidad, **una interacción binaria a la vez** (ec. 2, p. 4): más daño
  urbano (diferencia significativa), con madres de primaria o menos y en niños
  varones; los **no pobres algo más que los pobres, no significativo**. Lo
  atribuyen a programas focalizados (Giles y Satriawan 2015) y concluyen que
  focalizar solo en pobres «puede no bastar» (p. 5 y 7).
- 2014: −0,65 cm de estatura adulta por +100 % (p. 6, fig. 6). Más fuerte en
  quienes tenían 3-5 años y en los nacidos o gestados en 1998-99; en el grupo de
  3-5 años, más IMC y obesidad (p. 6).

**Relación con el proyecto**

- Es la **etapa 1** (ancla de replicación): mismo tratamiento (Δ precio comunitario
  1997→2000), misma cohorte y diseño B. Meta: β ≈ −0,135.
- Sus vacíos son nuestro aporte: no usan la posición neta en arroz aunque la
  invocan para explicar el resultado urbano (p. 5, 7); no combinan dimensiones;
  no hacen prueba global de heterogeneidad ni corrigen por comparaciones
  múltiples (→ H1-H8, `test_calibration`, Holm).
- Su frase sobre focalizar en pobres es literalmente la hipótesis **H9**: la
  sugieren, no la prueban. El RATE de la etapa 6 la pone a prueba.
- Su resultado de 2014 es asociación; nuestra estatura adulta (secundaria) usa el
  diseño C con la cohorte no expuesta para mejorar sobre eso.

**Suplemento en línea** (`1-s2.0-S2211912425000756-mmc1.docx`, solo en local;
leído completo el 20-nov-2026, nivel de verificación: texto del archivo)

- **Precio:** no dice qué fuentes usan en 2000 ni cómo reemplazan el PKK, que ese
  año no trae precios. Lo único sobre precios es el deflactor. La pregunta PL.3
  de `PLAN.md` sigue abierta.
- **Deflactor (apéndice A1):**
  `P^h(t) = W_F^h · P_F(t) + (1 − W_F^h) · P_NF(t)`, donde `W_F^h` es la
  participación de los alimentos sin arroz que predice una regresión con datos
  de 1997 sobre el log del gasto per cápita sin arroz y el tamaño del hogar.
  `P_F` y `P_NF` son el IPC mensual de alimentos y de otros bienes de
  Statistics Indonesia, base diciembre de 2000, emparejado con el mes de
  entrevista de cada comunidad. El IPC no viene en la IFLS.
- **Errores estándar:** todas las notas dicen "robust standard errors", **sin
  agrupar por comunidad** (cuadros A1-A7). En un panel con EF individuales, el
  robusto de Stata agrupa por individuo. Como el tratamiento varía por
  comunidad, los errores agrupados por `commid97` deberían ser más grandes.
- **Cuadro A1 (HAZ), columna 1:** Δ precio nominal −0,135 (EE 0,0412); real
  −0,251 (0,0796); pérdida de ingreso o empleo 1998-99 −0,218 (0,130).
  **3.338 observaciones** (columna 3: 3.596), R² 0,756, con EF individuales y de
  año. Unos 1.669 niños si el panel está balanceado, frente a los 2.112 del
  cuadro 1 del artículo: diferencia sin explicar.
- **Lista completa de controles (cuadro A1):**
  - niño: mujer, edad en meses, edad al cubo (sin término cuadrático);
  - hogar: educación del padre y de la madre, padre fumador, padre musulmán,
    madre musulmana, urbano, productor de arroz, tamaño, quintiles de gasto
    (el 5 omitido);
  - comunidad: centro de salud, agua limpia, vía para vehículos, vía asfaltada,
    parada de bus, sequía o incendio en 1997, mercado, oficina de teléfono,
    correo, banco, tarjeta de salud, arroz gratis, arroz subsidiado, programa de
    empleo y transferencia a la aldea.
  - Los programas (tarjeta de salud, arroz gratis o subsidiado, empleo,
    transferencia) son de la red de seguridad social que empezó en 1998:
    **probablemente posteriores al tratamiento**. No se dice en qué ola se miden.
- **Cuadro A4 (interacciones con Δ precio, HAZ, EE robustos):** edad crítica
  0,005 (0,066); mujer 0,099 (0,073); madre con educación alta 0,129* (0,075);
  pobre 0,216 (0,180); urbano −0,270* (0,153). Solo al 10 %, sin agrupar y sin
  corregir por comparaciones múltiples. Lo de "más daño en varones" no es
  significativo.
- **Cuadro A5 (las mismas interacciones, retraso en talla):** edad crítica
  −0,053 (0,036); mujer −0,026 (0,032); madre con educación alta −0,028
  (0,032); pobre −0,085 (0,079); urbano 0,051 (0,058). Ninguna significativa.
- **Definiciones (texto principal, cotejado el 20-nov):** pobre = línea oficial
  de pobreza de Indonesia de fines de los 90 (Widyanti et al. 2009; nota 3,
  p. 4); educación baja de la madre = primaria o menos (p. 5); la fig. 5 parte
  la edad en 0-2 y 3-5 años en 1997. No dicen cuál es la "edad crítica"; por el
  color de la fig. 5 sería 0-2 años (inferencia nuestra). Todo esto queda
  pre-registrado en `10_Propuesta/07_preregistro_heterogeneidad.md`.
- **Figura A1:** subgrupos para retraso en talla, emaciación, sobrepeso y
  obesidad (no para HAZ). La emaciación (WHZ) solo se estima para los niños de
  0-31 meses en 1997.
- **Cuadros A6 y A7 (2014):** estatura adulta −0,645 cm (0,232) nominal y −1,200
  (0,450) real; MCO con controles de 1997 y EF regionales; 2.349 observaciones.
- **Cociente real/nominal:** −0,251 / −0,135 ≈ 1,86. Si el deflactor fuera común
  a todas las comunidades, el cambio real sería (1 + C) / D − 1 y
  β_real ≈ β_nominal × D, es decir, solo un reescalamiento. Es una inferencia
  nuestra; E-Q no lo dicen.

---

## 2. Frankenberg y Thomas (2017): la tesis de la resiliencia

*Human Capital and Shocks: Evidence on Education, Health and Nutrition.* NBER WP
23347 (abril de 2017). **Versión revisada:** `c13829.rev1.pdf`, fechada en
**noviembre de 2017** (41 páginas; el identificador `c13829` parece de un
capítulo NBER y su texto remite a «the model laid out in the introduction» de un
volumen sobre trampas de pobreza; la referencia bibliográfica exacta de esa
versión no está verificada). Las páginas de esta sección son las **impresas en la
versión de noviembre**; desde la p. 7 van una más que en el WP de abril.

**Qué hacen**

- Ensayo con evidencia de dos choques: la crisis de 1998 (IFLS2, IFLS2+ y olas
  posteriores) y el tsunami de 2004 en Aceh (estudio STAR).
- Aclaran que los resultados son sobre **los niños**, no los adultos, que sí
  sufrieron en salud física y mental y en cognición (p. 2).
- No usan precios: la **zona urbana es el proxy de intensidad** del choque
  (p. 13). En escolaridad comparan cada cohorte contra una tendencia lineal por
  cohorte, separando urbano/rural × cuartil de gasto de 1997 (fig. 7, cuadro 3).

**Qué encuentran (crisis de 1998)**

- El precio de los alimentos subió 120 %, ~50 % más que el índice general,
  arrastrado por el arroz; la inflación general pasó a 80 %. Los consumidores
  netos perdieron; los productores netos quedaron protegidos o ganaron (p. 7).
- Salarios reales −40 %, ingreso del hogar −30 %, gasto per cápita −23 %; la caída
  fue mayor en los hogares que estaban mejor (−30 % en el p75 frente a −15 % en
  el p25 de 1993) (p. 8).
- **Estatura: sin daño**, ni urbano ni rural. Corto plazo, sin diferencias
  significativas por edad (p. 9); mediano plazo, los menores de 30 meses eran en
  2000 más altos que los de su edad en 1997 y su talla en 2007/8 se mantiene
  (p. 13, fig. 5).
- Matrícula 1997→1998: no matrícula a los 7-12 años de 3,1 % a 5,9 % (+90 %); en
  el cuartil más pobre, de 4,9 % a 10,7 % (+118 %); sin cambio a los 13-16
  (25,6 % a 25,1 %) (cuadro 1, p. 9 y p. 37). En hogares pobres, el hermano mayor
  matriculado se asocia con que el menor no lo esté (p. 9-10). Sin diferencias por
  zona ni sexo en matrícula (p. 10).
- **Escolaridad 2014** (5-21 años en 1997; n = 5.900 urbanos y 6.644 rurales):
  nada para las cohortes de 7-12 (+0,002, EE 0,17, pobres; +0,04, EE 0,14, no
  pobres; nota 1, p. 14) y 13-16 (+0,06, EE 0,18; +0,16, EE 0,12; nota 2, p. 15).
  **Única excepción: la cohorte urbana pobre de 8 años**, −1,95 años (EE 0,63);
  −2,09 (0,66) con controles; **−1,24 (0,69) con EF de hogar**, solo al 10 %
  (cuadro 3, p. 39). Brecha frente a urbanos no pobres: −1,82 (0,73); −1,86 (0,77)
  con controles; −1,34 (0,78) con EF de hogar. Diferencia en diferencias
  urbano-rural: 1,97 (0,87) (p. 15). La misma celda en lo rural: −0,08 (0,31).
- **Novedad de la versión final: comparaciones múltiples (nota 3, p. 16).** Dicen
  que «ninguna de estas inferencias» cambia al corregir con Hochberg (1988) o
  Hommel (1988). No dicen sobre qué familia de pruebas ni dan los p ajustados.
- Mecanismos de suavización (p. 10-12): migración urbano→rural y hogares que se
  juntan (4,33 → 4,53 personas, cuadro 2); recorte de gasto diferible (−35 %) y de
  salud y educación (−37 %), con la comida protegida (−9 %); venta de oro (que más
  que duplicó su valor; la salud y la educación son lo más protegido por tenerlo,
  según FST); las mujeres de 60+ perdieron ~15 % de peso, probablemente a favor
  de los nietos (p. 10).
- **Novedad de la versión final: cuarto mecanismo, las redes de protección
  (p. 12).** Raskin (arroz subsidiado para hogares pobres, 1998, hoy el mayor
  programa de asistencia) y una beca en efectivo para escolares pobres. Ninguno
  existía durante el campo de IFLS2+ (agosto-diciembre de 1998), así que no
  contaminan el corto plazo, pero «probablemente mitigaron» los efectos de largo
  plazo. La beca desde 1999 sustituye a las matrículas (p. 10 y 16).
- Matiz de redacción: «at most, muted» (antes «very muted») para el efecto en el
  capital humano de los niños (p. 16).

**Qué encuentran (tsunami, §4, p. 16-23)**

- Niños en gestación durante el tsunami, comparados con la cohorte de 2002 del
  mismo trimestre de nacimiento, con controles de sexo, mes de entrevista y orden
  de nacimiento. A los ~18 meses (2006-07), HAZ −0,70 (0,20) para los nacidos en
  el 2.º trimestre de 2005 (−0,18 y +0,05 en el 1.º y el 3.º). Cinco años después
  (2009-10) los tres grupos quedan por encima de la referencia (+0,41, +0,31,
  +0,34) y el crecimiento relativo de los del 2.º trimestre fue de 1,09 DE (0,20)
  (cuadro 4, p. 40). Los autores lo atribuyen en parte a la reconstrucción y a la
  inversión de los padres en los sobrevivientes. La moraleja sigue siendo la
  misma: juzgar el largo plazo por el daño de corto plazo puede engañar.

**Relación con el proyecto**

- Es el **contrapeso** de E-Q: mismo choque y mismos datos, conclusión opuesta en
  estatura. Reconciliarlos es parte del aporte; la diferencia es atribuible a la
  exposición (precio frente a zona) y al diseño, así que no es una contradicción.
- Su diseño de escolaridad es el antecedente directo de nuestro **resultado
  primario** (etapa 2, diseño C): misma cohorte de 5-21 años en 1997, mismo año de
  medición.
- La celda de 8 años es el objetivo de la **prueba de recuperación** (etapa 5,
  vacío V4): es una celda entre ~68 (17 edades × 2 zonas × 2 grupos de gasto,
  conteo nuestro de la fig. 7), y cae 40 % con EF de hogar. **Matiz respecto de
  la versión anterior de estas notas:** ya no se puede decir que F-T no corrigen
  por comparaciones múltiples; dicen que lo hicieron (nota 3), pero sin detallar la
  familia. Nuestro argumento de V4 pasa a ser que la corrección no es verificable
  desde el artículo, no que no exista. Si el bosque encuentra la celda con otra
  exposición, gana crédito; si no, no se puede descartar que sea ruido.
- Sus mecanismos (oro, hermanos mayores, mujeres mayores) son modificadores
  pre-declarados (**H7, H8**). Su advertencia sobre choques simultáneos y
  respuestas de los hogares respalda la §5.3 del `CLAUDE.md`.
- **Raskin y la beca (nuevo):** son respuestas de política posteriores al
  tratamiento y Raskin es un programa de **arroz** focalizado en pobres. Pueden
  mediar o confundir el efecto del precio del arroz sobre la escolaridad de 2014 y
  tocan a H3 (pobreza) y H9 (focalización). No son controles (variables
  posteriores al tratamiento), pero hay que discutirlos como mecanismo y buscar si
  la IFLS3-5 trae su cobertura. Es una idea para el equipo, no una decisión.
- Erratas a tener presentes (siguen en la versión final): la p. 16 dice «poor,
  **rural** households» para la cohorte de 8 años; el cuadro y el resto del texto
  dicen urbano. En la p. 9, «10.7% were not enrolled in 1997» debería decir 1998.

---

## 3. Frankenberg, Smith y Thomas (2003): diversidad del choque y el oro

*Economic Shocks, Wealth, and Welfare.* *Journal of Human Resources*, 38(2),
280-321.

**Qué hacen**

- IFLS2 (1997) e IFLS2+ (1998). Miden el choque como el cambio del gasto per
  cápita del hogar e interactúan el choque local (cambio del gasto en el
  kecamatan) con características de 1997, por separado en lo urbano y lo rural
  (cuadros 8-9).

**Qué encuentran**

- El gasto per cápita cayó cerca de 20 % en un año, con **enorme diversidad**:
  devastador para unos, oportunidad para otros. Cerca de **un tercio de los
  hogares** reportó más gasto en 1998 que en 1997 (p. 282, 295).
- Productores netos de alimentos, sobre todo de arroz, y del sector exportador se
  beneficiaron (p. 295).
- Urbano: caídas 5-15 pp mayores que en lo rural y mayores en los hogares que
  estaban mejor. Rural: la caída casi no depende del nivel inicial (p. 295).
- Mecanismos: hogares que se juntan (tamaño 4,33 → 4,53), más oferta laboral pese
  al colapso salarial, recorte de semidurables y protección del gasto en
  alimentos.
- **Oro y tierra suavizan el consumo solo en lo rural** (p. 316-317). La tenencia
  de oro rural cayó de 50,9 % a 34,5 % entre 1997 y 1998 (cuadro 4, p. 305). La
  educación del jefe suaviza; en lo urbano, también las mujeres mayores (p. 313).
- Advierten que la sequía de El Niño y los incendios golpearon la agricultura
  justo antes de la crisis (nota 1, p. 283).

**Relación con el proyecto**

- Sustenta la premisa de que el choque fue **muy heterogéneo**: justifica buscar
  CATEs en lugar de quedarse con el ATE.
- Su método (choque × características de 1997, por zona) es la versión
  paramétrica de lo que hace el bosque. Sus modificadores entran como **H7**
  (oro, tierra; esperamos menos daño sobre todo en lo rural) y **H8** (mujeres
  mayores).
- Pero su resultado es el consumo del hogar, no el capital humano de los niños:
  **nadie ha probado si esos amortiguadores protegieron a los niños** (vacío V3).
- La nota sobre sequía e incendios es la amenaza principal de identificación
  (choques simultáneos): controles de humo y sequía y exclusión de Sumatra y
  Kalimantan como robustez.

---

## 4. Friedman y Levinsohn (2002): quién perdía *ex ante* por los precios

*The Distributional Impacts of Indonesia's Financial Crisis on Household Welfare:
A "Rapid Response" Methodology.* *World Bank Economic Review*, 16(3), 397-423.

**Qué hacen**

- Simulación con datos previos a la crisis: canastas de SUSENAS 1996 × cambios de
  precios por provincia (44 ciudades, ene-1997 a oct-1998) ⇒ variación
  compensatoria de cada hogar; análisis no paramétrico por gasto y zona
  (p. 399-401).

**Qué encuentran**

- Prácticamente todos los hogares salieron muy afectados, pero **los pobres
  urbanos fueron los peores**: necesitaban en promedio el 109 % de su gasto previo
  para recuperar su bienestar, frente a 70 % de los pobres rurales (cuadro 2,
  p. 408-409).
- El arroz pesa más de un cuarto del gasto del decil más pobre; su precio subió
  casi 200 % en promedio, con mucha variación geográfica (cuadro 1, p. 402).
- **La producción propia protege**: sin ella, la compensación de los pobres
  rurales sube a ~130 % y el orden rural se invierte (p. 414). Lo mismo con la
  vivienda propia.
- La ubicación importa aun dentro de zona y nivel de gasto (p. 416). Los hogares
  con **niños pequeños** sufren más; los que tienen más mujeres mayores, menos
  (p. 419).
- Limitaciones que ellos mismos señalan: sequía e incendios también movieron los
  precios; el análisis es nominal y no mide el lado del ingreso (p. 420).

**Relación con el proyecto**

- Da la **lógica económica del tratamiento**: la exposición del hogar es el cambio
  del precio local × (consumo − producción propia). Por eso la posición neta en
  arroz es el modificador central (**H2**, vacío V2) y no ruido.
- Respalda H1 (urbano), H3 (pobreza que interactúa con zona) y H8 (niños
  pequeños, mujeres mayores).
- Su ejercicio es justo lo que haría un cliente tipo PMA con información *ex
  ante*. Nuestro aporte es pasar de exposición simulada a **daño realizado** en
  capital humano y comparar reglas de focalización (H9).
- Su advertencia sobre la sequía y los incendios refuerza la de FST.

---

## 5. Friedman y Thomas (2009): salud mental (extensión opcional)

*Psychological Health Before, During, and After an Economic Crisis: Results From
Indonesia, 1993-2000.* *World Bank Economic Review*, 23(1), 57-76.

**Qué hacen**

- Panel de 10.524 adultos de 20+ años en 1993 (cuadro 2), con ítems «adaptados del
  GHQ» (tristeza, ansiedad, sueño, entre otros; p. 60) en 1993, 1998 (IFLS2+) y
  2000. No hay ítems psicológicos en 1997.
- Exposición: cambio del gasto real medio 1997-2000 por provincia × zona (13
  puntos) y características de antes de la crisis (edad, sexo, educación, zona,
  tierra).

**Qué encuentran**

- La tristeza pasó de ~12 % a casi 30 % en hombres y de 16 % a 41 % en mujeres
  entre 1993 y 1998; la ansiedad se multiplicó por tres o cuatro (p. 61).
- **La angustia persiste en 2000**, cuando el consumo ya se había recuperado
  (p. 62, 75): la salud mental tarda más que las medidas económicas.
- Más daño en grupos vulnerables: rurales sin tierra (+19 % tristeza, +18 %
  ansiedad frente a rurales con tierra; p. 71), baja educación (p. 70), urbanos y
  provincias más golpeadas. En 2000, los de 60+ son 38 % más propensos a la
  tristeza (p. 69).
- La pendiente con la exposición provincial es significativa en lo urbano
  (R² = 0,34) y no significativa en lo rural (p. 72-74).

**Relación con el proyecto**

- Es la referencia de la **extensión opcional** (salud mental de adultos
  1993-2000), primera en la lista de recortes. Muestra por qué es la opción menos
  favorable para el bosque: pocos ítems ordinales, sin ola de 1997 y la de 1998 no
  es pública.
- Aporta evidencia indirecta para H2 y H7: «sin tierra» se parece a «comprador
  neto», y la tierra vuelve a aparecer como amortiguador.
- Su decisión de condicionar solo en características previas a la crisis es la
  misma regla que seguimos (no controlar por variables posteriores al
  tratamiento).

---

## 6. Lo que dicen juntos, en una tabla

| Dimensión | E-Q | F-T 2017 | FST | F-L | F-T 2009 | En el proyecto |
|---|---|---|---|---|---|---|
| Urbano | Más daño en HAZ | Más daño escolar (cohorte de 8 años); sin diferencia en HAZ | Más caída de gasto | Pobres urbanos, los peores | Más angustia | H1 |
| Posición neta en arroz | No la usan (la invocan) | Productores protegidos (p. 7) | Productores ganan | La producción propia protege | Sin tierra, peor | H2 (nunca probada en niños) |
| Pobreza | No pobres ≥ pobres (n.s.) | Daño solo en pobres urbanos | Los mejor situados caen más en % | Pobres urbanos, peores | — | H3 (ambigua) |
| Educación materna o del jefe | Baja educación, más daño | — | Jefe educado suaviza | — | Baja educación, más angustia | H4 |
| Edad | 3-5 años y gestación (largo plazo) | 8 años (escolaridad); ninguna en HAZ | — | Niños pequeños más expuestos | 60+ en 2000 | H5 |
| Activos (oro, tierra) | — | Oro protege salud y educación | Suavizan solo en lo rural | — | Tierra protege | H7 |
| Composición del hogar | — | Hermano mayor desplaza al menor; abuelas se sacrifican | Mujeres mayores suavizan (urbano) | Niños pequeños (+), mujeres mayores (−) | — | H8 |
| Método | Una interacción a la vez | Celdas a mano | Interacciones por zona | No paramétrico, *ex ante* | Logits con interacciones | Bosque causal + GATE con Holm + RATE |

**Mensaje para la sustentación:** los cinco coinciden en que el choque fue muy
desigual, pero cada uno lo midió con una exposición distinta (precio, zona, gasto,
simulación) y encontró los subgrupos a mano, una dimensión a la vez. Nosotros
usamos una sola exposición, pre-declaramos las dimensiones y dejamos que una
prueba global diga si la heterogeneidad es real.

---

## 7. Widyanti et al. (2009): la línea de pobreza de 1997

Widyanti, W., Suryahadi, A., Sumarto, S. y Yumna, A. (2009). *The Relationship between Chronic Poverty and Household Dynamics: Evidence from Indonesia*. SMERU Working Paper, enero de 2009. Jakarta: The SMERU Research Institute. https://smeru.or.id/sites/default/files/publication/chronicpovertyhouseholddynamics.pdf

Nivel de verificación: PDF (descargado y leído el 20-nov-2026; páginas
impresas). Es el trabajo que citan E-Q para definir «pobre» («official poverty
line in Indonesia for the late-1990s», p. 4), en la misma edición de SMERU.
También circula como CPRC Working Paper 132 y EABER Microeconomics WP 22554.
**No encontramos versión en revista** (búsqueda del 20-nov-2026 en SMERU,
IDEAS/RePEc, EABER y GOV.UK): la versión citable es el working paper.

- **Método (sección IV, p. 5):** la línea de cada región (provincia × urbano o
  rural) parte de las de diciembre de 2000 que calcularon Strauss et al. (2004,
  *Indonesian Living Standards Before and After the Financial Crisis*, RAND)
  para IFLS3. Esas, a su vez, inflan las de febrero de 1999 de Pradhan et al.
  (2001). Widyanti et al. las deflactan a diciembre de 1997 (IFLS2) y de 1993
  (IFLS1) con un IPC reponderado a 80 % de alimentos (Suryahadi et al. 2003),
  con el mismo deflactor para lo urbano y lo rural de cada provincia. La canasta
  de alimentos es nacional; el componente no alimentario sale de curvas de
  Engel.
- **Valores de diciembre de 1997 (apéndice 1, p. 18; Rp por persona al mes):**

| Provincia | Urbano | Rural |
|---|---:|---:|
| Sumatra del Norte | 39.496 | 38.260 |
| Sumatra Occidental | 36.275 | 32.811 |
| Sumatra del Sur | 40.381 | 37.911 |
| Lampung | 41.837 | 36.881 |
| Yakarta | 54.280 | — |
| Java Occidental | 45.892 | 40.974 |
| Java Central | 42.165 | 37.329 |
| Yogyakarta | 46.839 | 39.213 |
| Java Oriental | 41.571 | 39.737 |
| Bali | 46.962 | 43.734 |
| Nusa Tenggara Occidental | 38.909 | 40.072 |
| Kalimantan del Sur | 42.768 | 37.026 |
| Sulawesi del Sur | 40.949 | 38.557 |

- **Uso en el proyecto:** `pobre` = gasto per cápita del hogar de 1997 por
  debajo de la línea de su provincia y zona (`02_Scripts/03_x_1997.R`;
  `registro_decisiones.md` §5).
- **Diferencia con nuestro uso:** ellos comparan la línea con el gasto per
  cápita de los hogares de origen del panel, pero el texto no detalla cómo
  arman el agregado. Nosotros usamos un agregado propio, que puede no ser el
  mismo.

---

## Qué no está verificado

- De FST, F-L y F-T 2009 se releyeron hoy el resumen, las conclusiones y pasajes
  puntuales; las demás cifras con página vienen del cotejo con los PDF del 17-nov
  (`10_Propuesta/01` §6). E-Q y la parte de la crisis de F-T 2017 se releyeron
  completas. La §2 (F-T 2017) se cotejó el 20-nov contra la versión final de
  nov-2017 y contra el WP de abril (diferencias en la §2).
- Widyanti et al. (2009): no se cotejaron las ediciones de CPRC y EABER con la
  de SMERU, ni las fuentes originales de la línea (Strauss et al. 2004; Pradhan
  et al. 2001).
- Los apéndices de E-Q (cuadros A1-A7) no están en la carpeta: las pruebas de
  diferencias entre subgrupos (A4, A5, A7) no se han revisado.
- Tsunami de F-T 2017: se extrajeron las cifras del cuadro 4 y las del texto de la
  p. 20, pero no se revisaron las referencias que cita (Frankenberg et al. 2017,
  inédito) ni los resultados por sexo y por dosis de exposición (p. 21).
- F-T 2017: la referencia bibliográfica de la versión final (¿capítulo NBER
  c13829 en un volumen sobre trampas de pobreza?) no está verificada; hasta
  confirmarla, la cita del proyecto sigue siendo NBER WP 23347. Los números de
  página de `10_Propuesta/` y `CLAUDE.md` son los del WP de abril y están
  desfasados una página desde la p. 7 (ver reporte de la sesión del 20-nov).
- Nota 3 de F-T 2017 (Hochberg y Hommel): no se sabe qué familia de pruebas
  corrigieron.
- Las cifras de inflación de alimentos difieren entre artículos (120 % en F-T 2017,
  160 % en F-T 2009, casi 200 % para el arroz en F-L) porque miden índices y
  periodos distintos; no se reconciliaron.
