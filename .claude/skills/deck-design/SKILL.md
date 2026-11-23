---
name: deck-design
description: Buenas prácticas, errores corregidos y ajustes de diseño de la presentación final del proyecto (IFLS, precio del arroz). Usar al crear o editar láminas con `04_Presentaciones/_fuente/construir_presentacion.py`, al pedir cambios de títulos, subtítulos, cajas, figuras, ecuaciones o referencias, y antes de reconstruir `08_Entregables/presentacion_final.pdf`. También sirve como lista de revisión antes de entregar cualquier deck 16:9 con figuras y ecuaciones.
---

# Diseño de la presentación (deck-design)

Recoge lo que se decidió y corrigió en la sesión del 23-nov-2026 sobre
`04_Presentaciones/_fuente/construir_presentacion.py`. Aplica a toda lámina
nueva o editada. Si algo de aquí contradice a `CLAUDE.md` o a
`registro_decisiones.md`, mandan ellos.

## 0. Cómo se trabaja

- La presentación **se construye con el script**, nunca a mano en PowerPoint:
  `python 04_Presentaciones/_fuente/construir_presentacion.py` genera
  `08_Entregables/presentacion_final.{pptx,pdf}`, un PNG por lámina en
  `04_Presentaciones/_fuente/_render/` y `04_Presentaciones/como_leer_laminas.md`.
- Requisitos: `python-pptx`, `pymupdf`, `pandas`, `pillow`, `numpy`, LibreOffice
  (`soffice`) y `pdflatex`. En macOS conviene un venv fuera del repo.
- El script **falla** si: algún texto < 12 pt, contraste < 4,5:1, número de
  láminas principales ≠ `N_PRINCIPALES` esperado, textos montados o fuera de la
  página en el PDF. Si cambia el número de láminas principales, actualizar el
  `assert` y `N_PRINCIPALES + 2` (pie sin portada ni separador).
- **Después de cada cambio: reconstruir y mirar el PNG de la lámina**
  (`_render/laminaNN.png`). Las comprobaciones automáticas no ven si algo se
  ve mal; las medidas sobre el PDF (ver §7) sí ven si algo está desparejo.
- Una cosa a la vez: el usuario pide ajustes finos y los revisa lámina por
  lámina. Cambia lo pedido, reconstruye, verifica, y no toques lo demás.
- No inventes cifras: salen de los `.csv` de `03_Resultados/` (el script las
  lee) o de un artículo citado. Si cambias un número, que venga de un `.csv`.
- Idioma: español. Sin juicios de «bueno/malo» ni entusiasmo por significancia.

## 1. Contenido de las láminas

- **Título = afirmación clara**, de ≤ 15 palabras (el script lo verifica), sin
  «;». No usar títulos-etiqueta en láminas de resultados. Ejemplos vigentes:
  «Replicamos a Elmira y Qaim: donde el arroz subió más, los niños crecieron
  menos»; «El signo del efecto resiste cinco pruebas de robustez, pero su
  tamaño cambia»; «Un bosque causal no reproduce la heterogeneidad de las
  interacciones identificadas por Elmira y Qaim».
- **Decir el método, sin ambigüedad.** Nada de «algoritmo»: es **bosque causal**
  (o MCO, RATE, GATE…). Nada de «medimos la estatura»: **calculamos el HAZ**
  (estatura para la edad, referencia OMS) a partir de lo que trae la **IFLS**
  (declarar la fuente en la lámina de datos).
- **Subtítulo de método** en las láminas de resultados: *estimador* (MCO,
  bosque causal, RATE) + *estrategia de identificación* (dosis continua,
  terciles del alza dentro de provincia, mitades de comunidades). En ocre
  `#8F6219`, negrilla, 20 pt (el título va a 32 pt). **No repetir** en el
  subtítulo lo que el título ya dice (si el título dice «bosque causal», el
  subtítulo habla de terciles/GATE, no del bosque).
- **Nota de método** (14 pt, gris, bajo la figura): solo detalles — efectos
  fijos, controles, cifras puntuales, Holm, errores agrupados. Si una ecuación
  ya resume la especificación, se quita la nota.
- **«Cómo leer» y aclaraciones del orador no van en la lámina**: se registran
  con `como_leer(s, texto)` y salen en `04_Presentaciones/como_leer_laminas.md`
  (archivo generado; no se edita a mano). También las notas del orador del
  `.pptx` (tiempos por presentador; total objetivo 1.200 s).
- **Referencias en APA 7** al final del cuerpo principal (lámina «Referencias»,
  orden alfabético, sangría francesa, cursivas en revistas/volúmenes/títulos de
  informes). Cada referencia se verifica contra el PDF del proyecto o la página
  del editor; lo escrito de memoria se declara como no verificado.
- Distinguir siempre estimando/estimador/estimación y la escala (z de HAZ, cm,
  Δlog). No presentar un rango entre contrastes como intervalo de confianza.

## 2. Esquema de una lámina de resultados

De arriba abajo (pulgadas, lámina 13,333 × 7,5):

| Elemento | Posición |
|---|---|
| Título | caja 0,32–1,47, 32 pt, `Radio Canada Big` negrilla |
| Subtítulo (ocre) | `Y_SUB = 1,45`, alto 0,4 |
| Figura | `Y_FIG = 2,01` (tras ecuación o subtítulo), ancho 9,0 (7,3–7,9 si comparte fila) |
| Nota de método | figura + `GAP − 0,1`, 14 pt gris |
| Pie | 7,05: «Proyecto Final - ECON-3785», sección actual al centro, n.º a la derecha |

- **`GAP = 0,2 in` igual entre subtítulo→figura y figura→nota.** Verificar
  midiendo, no a ojo.
- Más aire entre el título y el contenido: nada de cajas o figuras pegadas al
  título (0,2–0,5 in desde la tinta del título).
- Figuras algo más angostas (≈ 9 in) antes que apretadas; las exporta
  `02_Scripts/15_figuras_presentacion.R` (12 × 5,6 in, 300 dpi, **sin título**,
  rótulos directos). Una figura que comparte lámina con un panel se regenera
  más alta (F2: 12 × 6,6) en vez de dejar espacio vacío.
- **Pie:** «Proyecto Final - ECON-3785». El indicador de sección es **solo el
  nombre de la sección actual** (Contexto, Método, Resultados, Recomendación,
  Referencias, Respaldo), en verde y centrado; no la lista completa.
- **Sin puntos medios (·) como separadores**: usar comas o guiones.

## 3. Cajas de texto: relleno parejo

- **El relleno interior debe ser igual a los cuatro lados.** `caja_texto()`
  centra el texto en vertical por defecto y registra la caja; el relleno se
  mide sobre el PDF (≈ 0,3 in en cajas grandes, 0,25 en tarjetas).
- Ajustar la **altura de la caja al texto** (alto de la tinta + 2 × margen), no
  al revés. Si el usuario pide texto más chico «sin reducir la caja», el
  relleno sobrante queda: avisarlo.
- Cajas en la misma fila comparten alto; la de menos texto queda con más aire
  abajo (decirlo). Alinear encabezados con anclaje arriba
  (`MSO_ANCHOR.TOP`, margen superior = margen − 0,07 por el interlineado).
- «Centrar entre A y B» = distancias iguales a la **tinta** de A y B (en el
  título, hasta los descendentes), no a los bordes de caja. Ej.: ítems de la
  lámina 13 entre el título (1,16) y el banner (6,0): 0,39 y 0,40 in.
- Para alinear el segundo bloque de varias columnas sin importar el largo del
  primero, dar a cada columna **dos cuadros de texto con posición fija**
  (`OFF2`), no un solo cuadro con texto corrido.
- Centrar verticalmente cajas en la lámina: `y = (H − alto) / 2`.
- Usar el tamaño de letra que deje respirar: reducir 2 pt antes que agrandar la
  caja contra el título.

## 4. Viñetas, cursiva y símbolos

- Viñetas con sangría francesa (0,25 in). `texto()` recibe un 8.º elemento por
  párrafo: `True` = viñeta automática; `"texto"` = «•» escrito como texto + tab.
- **Si en una línea hay un símbolo de otro tamaño (p. ej., μ más grande), usar
  `"texto"`:** la viñeta automática de LibreOffice se ubica según la altura de
  toda la línea y se descuadra; ni `buSzPts` ni interlineado fijo lo arreglaron.
- Estilos por trozo: `"i"` cursiva (variables *i*, *c*, *p*), `"b"` negrilla
  (**X**), `"grande"` cursiva ×1,3 (μ: Radio Canada no trae griegas y la
  tipografía de respaldo sale chica).
- Definiciones de variables: «i - niño» con guion, una viñeta por definición.

## 5. Ecuaciones y fórmulas

- Siempre en **LaTeX** compilado con `pdflatex` (`ecuacion_png()`); se pegan
  como PNG transparente con el color del texto. No escribirlas con Unicode.
- La instalación de TeX no trae `standalone` ni `preview`: se usa `article` con
  página grande y se recorta por la tinta.
- Especificación **sin resultados** en la lámina de método/resultado inicial
  (ΔHAZ = β·Dosis + γ·ln P₁₉₉₇ + **X**′**δ** + μ_p + ε); la ecuación **estimada**
  (coeficiente y EE agrupado desde el `.csv`) va en respaldo.
- Ecuación centrada arriba de figura + cuadro, con `GAP` igual arriba y abajo.
- Ponerla como una línea horizontal; el panel lateral con la especificación en
  3 líneas se descartó.

## 6. Figuras (R, `15_figuras_presentacion.R`)

- Estilo: verde `#2E6B4F`, ocre `#B8863B`, gris `#757575`, `texto #222222`,
  comas decimales, signo menos «−», sin título ni caja de fuente.
- Rótulos con el nombre del método («Bosque causal»), no «Algoritmo».
- **Cuidado con los intervalos.** La figura de potencia mostraba un «bigote» que
  parecía un IC y era el rango de la diferencia mínima detectable entre los seis
  contrastes (0,36 a 0,44). Se redibujó como barra oscura hasta el mínimo y
  clara hasta el máximo, rotulada «según el contraste». Un rango no es un IC:
  cada elemento visual debe leerse como lo que es.
- Al regenerar figuras, **revertir las que no cambiaron**
  (`git checkout -- ruta/figura.png`) para no ensuciar el diff, pero **no
  revertir las que sí cambiaste** (error cometido: se perdieron f5 y f6 una vez
  y hubo que regenerarlas).

## 7. Verificar midiendo (no a ojo)

Medir sobre el PDF a 200–300 dpi con `pymupdf` + `numpy`:

- Relleno de una caja: recortar el rectángulo de la caja, restar su color de
  fondo y tomar el recuadro de tinta; comparar izquierda/derecha/arriba/abajo.
- Separaciones entre elementos: filas de píxeles con el color de cada elemento
  (ocre del subtítulo, blanco de la figura, gris de la nota).
- Portada: detectar el marco rojo de TIME (la portada empieza en 0,32 in y
  termina en 7,20 in) y repartir bloques con la misma separación entre sus
  tintas (`Y_PORT` se calcula midiendo cada bloque).
- Ver el PNG de la lámina después de cada reconstrucción; ampliar (250 dpi) para
  alineaciones finas como viñetas y símbolos.

## 8. Portada

- Título alineado con el **borde superior de la portada de TIME** (no con el
  borde de la lámina); de ahí hacia abajo bloques con **separación igual**
  (título, subtítulo, «Para: …», autores y materia, crédito de la portada); el
  crédito termina en el borde inferior de la portada.
- Subtítulo vigente: «Análisis de los efectos promedio y heterogéneos de la
  crisis financiera de Indonesia de 1997-98 sobre la estatura de los niños».
- Autores separados por comas; materia y fecha con coma, no con «·».
- La imagen de TIME es de terceros: `portada_time.png` es local y está en
  `.gitignore` (el PDF final sí se versiona por decisión del equipo).

## 9. Errores que ya corregimos (no repetir)

1. Títulos con «;» o que describen en vez de afirmar.
2. «Algoritmo» (ambiguo) y «medimos la estatura» (imprecisa).
3. Falta de la fuente (IFLS) y del método en las láminas de resultados.
4. «Cómo leer» y aclaraciones ocupando espacio en la lámina.
5. Cajas con más relleno abajo que arriba; cajas pegadas al título.
6. Fuentes que sustituye LibreOffice (se ve «FrankRuhl»/«Linux Libertine»):
   las Radio Canada hay que copiarlas al perfil temporal
   (`user/fonts`), no basta instalarlas.
7. Ocre `#B8863B` como color de texto: contraste < 4,5:1 → el script falla; usar
   `#8F6219`.
8. Tabla de respaldo desbordada al añadir la ecuación: `alto_fila` explícito
   (0,36 con 14 pt).
9. Viñeta automática descuadrada con la μ grande (ver §4).
10. Barra con «bigote» que parecía IC (ver §6).
11. Último ítem de la lámina 13 más lejos del banner que el primero del título.
12. Referencias de memoria sin verificar: DOI, volumen y páginas se confirman;
    lo no confirmado se anota en la bitácora (p. ej., título completo de
    Chernozhukov et al., título y fecha de la página de RAND).
13. Archivos de depuración dentro del repo (`_cajas.json`): irían a
    `.gitignore`; las carpetas de vistas previas se borran al decidir.
14. Cambiar el número de láminas sin actualizar el guion, las referencias de
    respaldo («Respaldo: N») ni el README.

## 10. Lista de revisión antes de dar por buena una lámina

- [ ] Título = afirmación ≤ 15 palabras, sin «;»; método dicho una sola vez.
- [ ] Subtítulo de método en ocre (si es de resultados); nota solo con detalles.
- [ ] Cifras desde `.csv`; escala y alcance claros; ningún rango pasa por IC.
- [ ] Relleno de cajas parejo (medido); alineaciones y centrados medidos.
- [ ] ≥ 12 pt, contraste ≥ 4,5:1, sin solapes (lo verifica el script).
- [ ] Pie correcto y sección actual; sin «·» como separador.
- [ ] «Cómo leer»/aclaraciones en `como_leer_laminas.md`; notas del orador al día.
- [ ] Tiempo total de las láminas principales = 1.200 s; guion al día.
- [ ] Si hubo figuras nuevas/cambiadas: regeneradas con
  `15_figuras_presentacion.R` y solo se versionan las que cambiaron.
- [ ] Al cerrar: `bitacora-sesion` y `cerrar-sesion` (en la rama del integrante
  salvo instrucción expresa del usuario).

## 11. Mapa de archivos

- `04_Presentaciones/_fuente/construir_presentacion.py`: construye todo (piezas:
  `lamina`, `titulo`, `subtitulo`, `figura_metodo`, `nota_metodo`, `caja_texto`,
  `texto`, `tabla`, `ecuacion_png`, `pie`; constantes `Y_SUB`, `Y_FIG`, `GAP`,
  `Y_PIE`, `Y_PORT`, `OCRE_T`, `REFS`).
- `02_Scripts/15_figuras_presentacion.R`: figuras f1–f7 para proyectar.
- `04_Presentaciones/guion_presentacion.md`: tiempos, títulos, preguntas.
- `04_Presentaciones/como_leer_laminas.md`: generado; textos quitados.
- `08_Entregables/presentacion_final.pdf`: entregable (se presenta desde el PDF).
