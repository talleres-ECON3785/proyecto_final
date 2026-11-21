# Bitácora — 2026-11-20 (2): el precio de 2000 y el suplemento de E-Q

## Resumen

Objetivo: entender el problema de los datos del precio del arroz en la ronda de
2000 antes de escribir `02_precio_arroz.R`, y decidir cómo construirlo.

Desarrollo:

1. **Diagnóstico del problema** con la síntesis de datos (S §7.6), la guía de
   IFLS3 (§9.5, §10) y `PLAN.md` H1. En 1997 hay tres fuentes de precio
   comunitario (PKK, posyandu, tiendas y mercados); en 2000 el libro PKK no
   trae precios. E-Q (p. 3) promedian "mercados, tiendas y grupos comunitarios
   de mujeres" sin decir qué usan en 2000. Si se promedian todas las fuentes de
   cada año, el cambio del precio mezcla el alza con el cambio de fuentes y
   calidades, de forma distinta en cada comunidad.
2. **Lectura completa del suplemento en línea de E-Q**
   (`07_Recursos/Articulos/1-s2.0-S2211912425000756-mmc1.docx`), convertido a
   texto con `markitdown` y `pandoc` (para las fórmulas) en el directorio
   temporal de la sesión, y con la figura A1 extraída del `.docx`. No dice qué
   fuente usan en 2000. Sí trae el deflactor, la lista completa de controles,
   los errores (robustos, sin agrupar por comunidad) y las interacciones del
   cuadro A4.
3. **Decisión sobre el precio** (Santiago, en la sesión): el tratamiento
   principal usa solo las fuentes presentes en ambos años, con cambio
   proporcional nominal. Registrada en `CLAUDE.md` §11, `PLAN.md` H1,
   `01_Datos/CLAUDE.md` §9 y `10_Propuesta/00_resumen.md`.
4. **Corrección de `CLAUDE.md` §5.6:** los subgrupos de E-Q para la talla,
   con las cifras del cuadro A4.

**Siguientes objetivos que traía `HANDOFF.md`:**

- (1) P0.3 y P1.1, P1.3-P1.5: no se trabajó la puesta del equipo en el
  repositorio. Avanzó la parte de decisiones del tratamiento (construcción del
  precio), pendiente de informar al equipo.
- (2) P2.1: no se trabajó.
- (3) P2.2: no se escribió el script, pero queda definida la construcción del
  precio, que era su primer paso.
- Se cerró PL.2 (suplemento de E-Q).

## Archivos

- **Creados:** `06_Bitacoras/2026-11-20_precio-2000-y-suplemento-eq_2.md`.
- **Modificados:** `PLAN.md`, `CLAUDE.md`, `01_Datos/CLAUDE.md`,
  `10_Propuesta/00_resumen.md`, `HANDOFF.md` y
  `07_Recursos/Articulos/00_hallazgos_articulos.md` (este último estaba sin
  seguimiento desde antes de la sesión; se le agregó la subsección del
  suplemento).
- **Fuera de la sesión, sin tocar:** `07_Recursos/Articulos/README.md`
  (modificado antes) y `Claude outputs/` (sin seguimiento desde antes).

## Detalle por archivo

### `07_Recursos/Articulos/00_hallazgos_articulos.md`

Nueva subsección "Suplemento en línea" dentro de §1 (E-Q), con nivel de
verificación "texto del archivo". Recoge:

- **Precio:** el suplemento no menciona fuentes ni calidades. PL.3 sigue
  abierta.
- **Deflactor (A1):** `P^h(t) = W_F^h · P_F(t) + (1 − W_F^h) · P_NF(t)`. El peso
  de alimentos de cada hogar sale de una regresión con datos de 1997, y los
  índices son el IPC mensual de alimentos y de otros bienes del BPS (base
  diciembre de 2000), emparejado con el mes de entrevista. El IPC no viene en la
  IFLS.
- **Errores:** "robust standard errors" en todos los cuadros, sin agrupar por
  comunidad.
- **Cuadro A1:** −0,135 (0,0412) nominal y −0,251 (0,0796) real, en z de HAZ
  por +100 % del precio; 3.338 observaciones, frente a 2.112 niños en el
  cuadro 1 del artículo (sin explicar).
- **Controles completos,** incluidos cinco programas de la red de seguridad
  social (desde 1998), probablemente posteriores al tratamiento.
- **Cuadro A4 (HAZ):** urbano −0,270* (0,153), madre con educación alta
  +0,129* (0,075), mujer +0,099 (0,073), pobre +0,216 (0,180), edad crítica
  0,005 (0,066).
- **Cuadros A6-A7 (2014)** y la figura A1 (sin HAZ).
- **Inferencia propia,** marcada como tal: −0,251 / −0,135 ≈ 1,86. Con un
  deflactor común, β real ≈ β nominal × D.

### `PLAN.md`

- **H1, "Para replicar":** se agregan los hallazgos del suplemento.
- **Nueva subsección "Construcción del precio"** (fuentes, escala, nominal y
  diagnóstico).
- **Tabla de tratamientos:**
  - T1 queda como réplica aproximada (todas las fuentes de cada año, nominal);
  - T2 precisa fuentes comunes, nominal y mediana por comunidad.
- **P2.2:** incluye el diagnóstico PKK frente a posyandu de 1997.
- **P4.2:**
  - separa la columna (2a), controles completos de E-Q, solo como réplica, de
    la (2b), sin los programas posteriores a 1997, que es la principal;
  - pide errores robustos y agrupados, uno al lado del otro, en la réplica.
- **PL.2** marcada; PL.3 deja de bloquear; nueva **PL.7** (ola de los programas;
  definiciones de "edad crítica" y "pobre").
- **"Qué no está verificado"** actualizado.

### `CLAUDE.md`

- **§11:** nueva fila del 20-nov sobre el precio. Dice "decisión de Santiago en
  la sesión; informar al equipo", porque las decisiones del tratamiento
  requieren al equipo (§4).
- **§5.6:** se reemplaza "urbano, madre con primaria o menos, varones" por las
  cifras del cuadro A4. Solo urbano y madre con educación alta son
  significativos, y al 10 %; varones y pobres no.

### `01_Datos/CLAUDE.md`

§9, recomendaciones vigentes: "Δlog winsorizado" contradecía la decisión de
usar el cambio proporcional. Queda "cambio proporcional nominal winsorizado
p1/p99, no Δlog", con posyandu + `bk2_hpj`. No se agregó fila a la tabla de
decisiones aprobadas, porque el equipo no lo ha aprobado.

### `10_Propuesta/00_resumen.md`

Fila "Precio" en la tabla "Qué cambió en la versión 5". En "Qué no está
verificado", la línea del apéndice sin revisar se reemplaza por lo que sigue
abierto: la fuente de 2000 y la ola de los programas.

### Variable que construye el estimador: el tratamiento (precio)

- **Estimando:** efecto sobre ΔHAZ (z) 1997→2000 de un alza del precio
  comunitario del arroz de +100 % frente a no tener alza adicional, en
  comunidades con más alza frente a menos (contraste, no el efecto de la
  crisis).
- **T2, principal:**
  - **Fuentes:** posyandu (`pos_h`, calidad media) y tiendas y mercados
    (`bk2_hpj`, `hpj3type` = 1), en 1997 y 2000 (S §7.6; guía IFLS3 §10).
  - **Construcción:** mediana por comunidad (`commid97`) de los precios en kg;
    después `(P2000 − P1997) / P1997`, winsorizado en p1/p99.
  - **Rol:** es la dosis `C_j` de la ecuación 1 de E-Q (p. 3).
  - **Por qué estas fuentes:** con las mismas fuentes en los dos años, la
    variación de `C_j` entre comunidades no depende de qué fuente o calidad
    había en cada una.
- **T1, réplica aproximada:** el promedio de todas las fuentes y calidades de
  cada año, como E-Q (p. 3). Es aproximada porque no sabemos qué reemplazó al
  PKK en 2000.
- **Nominal y no real:** si el deflactor D es común, el cambio real es
  `(1 + C) / D − 1`, lineal en C. β solo se reescala y no cambia la variación
  que lo identifica. El de E-Q varía por hogar y por mes, así que la
  equivalencia es aproximada.

## Resultados nuevos (tablas, figuras, bases)

Ninguno. No se corrieron scripts del pipeline ni se tocaron datos de
`01_Datos/`.

## Pendientes

- Informar al equipo la construcción del precio, que figura en `CLAUDE.md` §11
  como decisión de Santiago.
- **PL.3:** qué fuente usan E-Q en 2000. Ya no bloquea.
- **PL.7:** en qué ola miden E-Q los programas de la red de seguridad social, y
  cómo definen "edad crítica" y "pobre".
- La diferencia entre las 3.338 observaciones del cuadro A1 y los 2.112 niños
  del cuadro 1.
- Siguiente paso: P2.1 (`01_tracks.R`) y P2.2 (`02_precio_arroz.R`), con T1-T4,
  la prueba 1 y el diagnóstico PKK frente a posyandu.
