# CLAUDE.md · Proyecto final ECON-3785 (Ciencia de Datos y Econometría Aplicada, 2026-2)

> Reglas del proyecto para los agentes y el equipo. Reúne lo decidido hasta el
> 20-nov-2026 (el `CLAUDE.md` anterior, del 17-nov, está archivado en
> `10_Propuesta/_obsoleto/CLAUDE_2026-11-17.md`) y adapta el flujo de trabajo de
> los Talleres 1 y 2 (repositorios `talleres-ECON3785/taller_01` y `taller_02`).
> **Las reglas para manejar los datos están en [`01_Datos/CLAUDE.md`](01_Datos/CLAUDE.md):
> léalo antes de escribir cualquier script que lea o una datos.**
> **Lo confirmado está en [`registro_decisiones.md`](registro_decisiones.md) y lo
> que falta, en [`PLAN.md`](PLAN.md).** Si algo de aquí los contradice, mandan
> ellos y se corrige este archivo en el mismo cambio. `10_Propuesta/` es
> histórica desde el 20-nov y ya no se consulta, salvo
> `07_preregistro_heterogeneidad.md` (vigente).

## 1. El proyecto en una frase

¿A quién afectó más el arroz caro? Con la Indonesia Family Life Survey (IFLS),
**solo estatura** (ΔHAZ 1997→2000 de los niños de 0-5 años en 1997; alcance del
20-nov). La presentación responde tres preguntas:

1. **¿Dolió?** Replicar con `feols` el ATE de Elmira y Qaim (2026), −0,135 HAZ
   por +100 % del precio, y ver su forma (cuartiles).
2. **¿A quién?** GATE pre-declarados (edad, urbano, educación de la madre,
   sexo, comprador neto, pobreza) con puntajes AIPW del bosque causal y Holm.
3. **¿El bosque supera a las reglas simples?** Bosque con terciles, calibración
   y RATE/TOC frente a pobre, urbano y comprador neto.

Escolaridad, cognición y salud mental quedan fuera por ahora.

- **Cliente propuesto:** agencia que focaliza ayuda ante choques de precios de
  alimentos (p. ej., Programa Mundial de Alimentos). Entregable para el cliente:
  la comparación del bosque con reglas simples, el perfil de los niños que
  prioriza con variables que el cliente observa y, si el bosque no las supera,
  la evidencia de que basta una regla simple.
- **Tratamiento:** cambio proporcional del precio comunitario del arroz
  1997→2000 (fuentes presentes en ambos años), asignado por la comunidad de
  residencia en 1997 (`commid97`), en tres versiones: dosis (principal),
  cuartiles y terciles (bosque). Definiciones en `registro_decisiones.md` §3-4.
- **Documentos:** `registro_decisiones.md` (lo confirmado), `PLAN.md` (lo que
  falta) y `10_Propuesta/07_preregistro_heterogeneidad.md` (subgrupos y Holm).
- **Estado al 20-nov:** decisiones previas tomadas y las cinco olas de la IFLS
  revisadas (guías en `01_Datos/01_Crudos/IFLSx/`); **ninguna estimación
  corrida y el precio sin construir**. El avance y lo que sigue están en
  `HANDOFF.md`.

## 2. Lo que exige el curso (`07_Recursos/ProyectoFinal.pdf`)

- Emular una consultoría: definir cliente y problema; usar al menos un método
  del curso.
- **Semana 15:** asesoría obligatoria con el profesor (agendar turno). La
  **noche anterior** se envía por correo una presentación preliminar o un
  documento. Se revisa: pregunta y cliente; datos (qué hay, cómo se obtuvieron,
  qué falta); avances; dudas.
- **Semana 16:** presentación presencial de 20 min + 5 min de preguntas.
- **Entrega** (Bloque Neón, 11:59 pm del miércoles de la semana 16): la
  presentación + un `.zip` con el código, los datos **o las instrucciones para
  obtenerlos**, y un `README.md` que permita reproducir todo.
- Se evalúa: creatividad, corrección del análisis, dominio técnico bajo
  preguntas, claridad, comunicación, reproducibilidad y reflexión crítica sobre
  limitaciones.

Las fechas exactas de las semanas 15 y 16 van en `HANDOFF.md` cuando se
confirmen.

## 3. Estructura del repositorio

- `00_main.R`                (raíz) script maestro: corre todo el pipeline
- `proyecto_final.Rproj`     proyecto de RStudio (raíz)
- `CLAUDE.md`                este archivo
- `HANDOFF.md`               estado actual, siguientes objetivos y registro de sesiones
- `registro_decisiones.md`   lo confirmado para el trabajo (manda sobre todo lo demás)
- `PLAN.md`                  lo que falta por ejecutar, por hitos (P*k.n*)
- `README.md`                objetivo, instrucciones de ejecución y mapa script → resultados
- `01_Datos/`                ver [`01_Datos/CLAUDE.md`](01_Datos/CLAUDE.md) y [`01_Datos/README.md`](01_Datos/README.md)
  - `01_Crudos/IFLS1…IFLS5/` datos de RAND (**no se versionan**) + guía `00_guia_IFLSx.md` (sí)
  - `02_Procesados/`, `03_Listos/` bases derivadas (**no se versionan**)
  - `00_sintesis_revision_IFLS.md` síntesis de las cinco olas
- `02_Scripts/`              scripts numerados; `00_formato_graficas.R` y
  `00_formato_tablas.R` (formato, sin resultados); `_exploratorio/` (scripts
  que no entran al pipeline, p. ej. el índice de salud mental de 1993 en Python)
- `03_Resultados/`           `Tablas/` y `Figuras/`, una subcarpeta por script
- `04_Presentaciones/`       borradores (asesoría, sustentación); hoy, `propuesta_presentacion.pdf`
- `05_Notas/`                notas de hallazgos, una por hallazgo (ver §8)
- `06_Bitacoras/`            una bitácora por sesión de trabajo
- `07_Recursos/`             enunciado (`ProyectoFinal.pdf`), catálogo de
  herramientas del curso (`herramientas_R_del_curso.md`), artículos
  (`Articulos/`, PDF solo en local) e insumos de referencia (`Insumos/`, solo en local)
- `08_Entregables/`          presentación final y `.zip` de entrega
- `09_Conversaciones/`       registro crudo (`.jsonl`) de las conversaciones; en `.gitignore`
- `10_Propuesta/`            histórica (propuesta v4, no se consulta); vigente solo `07_preregistro_heterogeneidad.md`
- `.claude/skills/`          `bitacora-sesion`, `cerrar-sesion`, `registrar-hallazgo`

## 4. Reglas de trabajo

- **Idioma:** español en todo (documentos, comentarios del código, láminas).
- **Lenguaje:** R para todo el pipeline, incluida la construcción de bases
  (`haven::read_dta()` + `tidyverse`; decisión del 20-nov). Python
  (`pyreadstat`) queda solo en `02_Scripts/_exploratorio/` y en los scripts de
  revisión de datos, fuera del pipeline.
- Explique lo que va a hacer ANTES de editar o crear archivos.
- Rutas relativas a la raíz del repositorio. Nunca rutas absolutas.
- **Semilla:** `set.seed(2026)` en todo paso aleatorio; `grf` recibe
  `seed = 2026` y `num.threads` fijo (solo así reproduce las cifras).
- **Nunca inventar cifras ni citas.** Toda cifra sale de un script (con la ruta
  del archivo que la produce) o de un artículo citado con página y nivel de
  verificación (PDF / texto / resumen / prensa). Las citas de memoria se
  verifican antes de usarlas.
- Cada documento de análisis o de propuesta cierra con una sección "Qué no está
  verificado".
- Las decisiones del equipo (cliente, resultado primario, alcance, hipótesis) se
  **recomiendan**; las toma el equipo. Se registran en `registro_decisiones.md`
  con fecha y quién las tomó.
- Pensar siempre en la sustentación: preferir lo que el equipo pueda defender
  bajo preguntas sobre lo más sofisticado.
- **Registro y plan:** lo pendiente vive en `PLAN.md`; pasa a
  `registro_decisiones.md` solo cuando la tarea se completa. El registro es
  conciso: solo lo confirmado, sin lo descartado ni lo que no se hará. Al cambiar
  una decisión, se edita el registro y se anota en su historial.
- Al cerrar una sesión: `bitacora-sesion` y después `cerrar-sesion` (§7).

### 4.1 Reproducibilidad y salidas (heredado del Taller 2)

- **`00_main.R` es el único punto de entrada.** (1) Verifica que el directorio
  de trabajo es la raíz (un `.Rproj` y `02_Scripts/`); (2) carga los paquetes
  con `pacman`; (3) verifica que los datos crudos de RAND estén en
  `01_Datos/01_Crudos/`; (4) crea las carpetas de salida que falten; (5) corre
  cada script de la lista `scripts` con `source(script, local = new.env(),
  encoding = "UTF-8")`. Cada script nuevo se agrega a esa lista en la misma
  sesión en que se crea.
- **Paquetes:** la lista única vive en el `pacman::p_load()` de `00_main.R`. Los
  scripts no cargan paquetes; llevan el comentario
  `# los paquetes los carga 00_main.R con pacman`. Para correr un script suelto,
  primero se ejecutan las secciones 1 a 4 de `00_main.R`.
- **Carpetas de salida:** se verifican solo en `00_main.R` (`carpetas_salida`).
  Ni los scripts ni `guardar_figura()`/`guardar_tabla()` llaman a
  `dir.create()`. Borrar `03_Resultados/` y correr `00_main.R` debe regenerarlo
  todo.
- **Una carpeta de resultados por script:** `03_Resultados/Figuras/<script>/` y
  `03_Resultados/Tablas/<script>/`; el script define
  `carpeta_salida <- "<nombre_del_script>"`. Si se renombra un script, se
  renombran sus carpetas (`git mv`) y se actualizan `00_main.R`, README y notas.
- **Tablas y figuras en formato final:** salen de `02_Scripts/00_formato_tablas.R`
  (`gt`, `guardar_tabla()`: `.png` + `.csv`) y `02_Scripts/00_formato_graficas.R`
  (paleta azul `#2B5FA3`, ocre `#B8863B`, verde-azulado `#0E8A6C`;
  `tema_presentacion`; `guardar_figura()` 9×6 in, 300 dpi). La figura o tabla que
  entra a la lámina es la exportada, sin retoques. Subtítulo y nota declaran el
  alcance (`descriptivo`, `contraste` o `placebo`), el n de personas y el de
  comunidades.
- **Nombres de archivo:** `03_Resultados/{Tablas,Figuras}/<script>/<muestra>_<contenido>.<ext>`
  (p. ej. `comunidades_balance_tercil.png`, `escolaridad_gate_h1_h8.png`).
- **Datos:** el flujo Crudos → Procesados → Listos y las reglas de uniones y
  llaves están en `01_Datos/CLAUDE.md`. Ningún microdato se versiona.
- **README:** objetivo, estructura, instrucciones (descargar RAND → correr
  `00_main.R`) y mapa completo script → tablas/figuras. Se actualiza en la misma
  sesión en que se agrega o renombra un script o un resultado.

### 4.2 Flujo de versiones: una rama por integrante (obligatorio para los agentes)

Repositorio: `https://github.com/talleres-ECON3785/proyecto_final` (**público**).
Cada integrante trabaja en su rama, creada desde `main`, con la convención de
los talleres (nombre + primer apellido + inicial del segundo):

| Integrante | Rama |
|---|---|
| Samuel Escandón | `SamuelEscandonC` |
| Douglas Plazas Guzmán | `DouglasPlazasG` |
| Mateo Olmos Becerra | `MateoOlmosB` |
| Santiago Muñoz Martínez | `SantiagoMunozM` |

<!-- Equipo copiado del Taller 2: confirmar que es el mismo para el proyecto final. -->

1. **Al empezar la sesión, ubicarse en la rama del integrante**
   (`git branch --show-current`, `git config user.name`). Si se está en `main`
   o en la rama de otro, cambiar (`git switch <rama>`; si no existe,
   `git switch -c <rama>` desde `main` actualizado). Si no es inferible quién
   trabaja, preguntar.
2. **Sincronizar con `main` al empezar:** `git fetch origin` y
   `git merge origin/main` si avanzó. Conflictos: se muestran y se resuelven con
   el usuario.
3. Todo se commitea y se empuja en la rama del integrante (lo hace
   `cerrar-sesion`).
4. **Nunca commitear ni hacer push directo a `main`.** Llevar cambios a `main`
   es decisión del integrante, con un pull request (`gh pr create --base main
   --head <rama>`), después de sincronizar y de comprobar que `00_main.R` corre.
   La única excepción fue el commit inicial del 18-nov que creó el repositorio.
5. No crear ramas por tarea ni trabajar en la rama de otro sin que el usuario lo
   pida.
6. **Antes de cada commit, revisar que no entre ningún dato** (`git status`,
   `git diff --cached --stat`): nada de `.dta`, `.csv` o `.rds` de `01_Datos/`.

## 5. Conclusiones sustantivas que guían el análisis

1. **El ATE a replicar está en disputa.** Elmira y Qaim (2026, *Global Food
   Security* 48, 100900): +100 % de precio nominal ⇒ −0,135 HAZ (−0,251 real),
   +3,5 pp de retraso en talla; −0,65 cm de estatura adulta en 2014
   (asociación). Frankenberg y Thomas (2017, NBER WP 23347): sin daño en
   estatura; en escolaridad, nada para las cohortes de 7-12 y 13-16, **salvo
   −1,95 años (EE 0,63) en la cohorte urbana pobre de 8 años en 1997**, que cae
   a −1,24 (EE 0,69, al 10 %) con EF de hogar (cuadro 3; −2,09 (0,66) con
   controles; −1,82 (0,73) frente a urbanos no pobres; DiD urbano-rural 1,97
   (0,87)). Cifras cotejadas con los PDF el 17-nov (`07_Recursos/Articulos/00_hallazgos_articulos.md`). Un
   nulo bien documentado es un resultado válido.
2. **Se identifica un contraste, no el efecto de la crisis.** No hay comunidades
   sin tratar. Con tratamiento continuo hace falta "tendencias paralelas
   fuertes" (Callaway, Goodman-Bacon y Sant'Anna); los terciles son más
   defendibles. Reportar ambos y decir qué supuesto usa cada uno. La pendiente
   promedio de `causal_forest` con W continuo no es el β MCO de E-Q (pondera
   distinto): la réplica se hace con `feols`.
3. **Amenaza principal: choques simultáneos** correlacionados con el precio
   (sequía de El Niño, humo de 1997, disturbios). Mitigar con EF de comunidad,
   diseño productor/comprador neto, controles de humo/sequía y excluir Sumatra y
   Kalimantan como robustez.
4. **El signo depende de la posición neta en arroz** (Friedman y Levinsohn;
   Yamauchi y Larson): es un modificador, no ruido.
5. **Hueco aparente** (sin confirmar en Google Scholar): no encontramos un ATE
   del precio del arroz sobre escolaridad o cognición, ni CATEs con bosques
   causales para este choque. Decir «hasta donde revisamos».
6. **Heterogeneidad pre-registrada** (`10_Propuesta/07_preregistro_heterogeneidad.md`,
   20-nov). Pregunta concreta: ¿el bosque recupera,
   sin escogerlos a mano, los subgrupos de E-Q para la talla? En su cuadro A4
   (suplemento; EE robustos sin agrupar, sin corregir por comparaciones
   múltiples) solo dos interacciones son significativas, y al 10 %: urbano
   −0,270 (0,153) y madre con educación alta +0,129 (0,075). Varones y pobres no
   lo son: mujer +0,099 (0,073), pobre +0,216 (0,180). Con unos cientos de comunidades, los GATE
   pre-declarados tienen mucha más potencia que la búsqueda del bosque (una
   simulación con datos inventados del 20-nov no pasó `test_calibration` aun con
   heterogeneidad grande); hay que preparar la lámina del nulo.

## 6. Diseño y métodos

Rehecho el 20-nov. Detalle de cada paso en `PLAN.md` (H2-H4).

| Etapa | Qué | Método |
|---|---|---|
| 1 | **¿Dolió?** ΔHAZ 1997-2000, cohorte 0-5, con la dosis; tabla de especificaciones (sin controles → controles → EF de provincia → log precio 1997; EE robustos al lado; pendiente promedio del bosque como fila de robustez) | `feols`, cluster `commid97` |
| 2 | Forma: cuartiles de la dosis (Q2-Q4 frente a Q1), figura contra la recta de E-Q | `feols` con `i(cuartil, ref = 1)` |
| 3 | Validación: placebo ΔHAZ 1993-97 de la cohorte 0-5 de 1993, desgaste según el alza, sin comunidades de 1998, con pesos, sin winsorizar | `feols` |
| 4 | **¿A quién?** Réplica de las cinco interacciones de E-Q (Holm F2); bosque con terciles, traslape, seis GATE (Holm F1), BLP | `feols`; `grf` + puntajes AIPW |
| 5 | **¿El bosque supera a las reglas simples?** Calibración; RATE con AUTOC en dos mitades de comunidades frente a pobre, urbano y comprador neto (Holm F3); perfil de los priorizados | `test_calibration`, `rank_average_treatment_effect` |

**Alcance mínimo:** etapas 1-4. Si falta tiempo, la etapa 5 queda como
exploratoria.

Reglas de los métodos:

- **Catálogo:** los métodos y funciones de `07_Recursos/herramientas_R_del_curso.md`
  (`fixest`, `glmnet`, `rpart`, `ranger`, `grf`). `haven`, `get_scores`,
  `best_linear_projection`, `target.sample = "overlap"` y `sensemakr` son
  **ampliaciones**: se registran en "Decisiones tomadas" (y en el README)
  **antes** de usarlas.
- `clusters = commid97` siempre en `grf`; errores agrupados por comunidad en
  `feols`. El N efectivo es de cientos de comunidades (197 en la comparación por
  terciles), no de miles de personas.
- Partición de muestras **por comunidad completa** (focalización en dos mitades).
- Revisar `cf$W.hat` (traslape); recortar si se pega a 0 o 1. Los terciles son
  dentro de provincia (registro §3), así que poner la provincia en X no lo pega.
- `causal_forest` con W continuo supone un efecto lineal en W dado x: no sirve
  para estudiar la no linealidad de la dosis (va con `feols`).
  `rank_average_treatment_effect(forest)` solo acepta W binario (`grf` 2.6.1).
- El HAZ de 1997 no se usa como modificador (regresión a la media); la edad en
  1997 entra de forma flexible.
- Si `test_calibration` no rechaza: reportar "no hay evidencia de
  heterogeneidad" y apoyarse en el ATE y los GATE pre-declarados.
- No controlar por variables posteriores al tratamiento.
- Corregir comparaciones múltiples con Holm en las familias F1-F3 del
  registro; un solo resultado primario (el ATE); lo demás no pre-registrado es
  exploratorio.
- Distinguir siempre **estimando**, **estimador** y **estimación**, y la escala
  (z de HAZ, años, cm, Δlog del precio).
- No emitir juicios de "bueno" o "malo" sobre resultados ni entusiasmo por
  métricas o significancia; reportar magnitud e incertidumbre. Que el bosque
  encuentre grupos no prueba heterogeneidad; `variable_importance` no es un
  efecto.

## 7. Bitácoras, `HANDOFF.md` y skills

- **Bitácora por sesión** en `06_Bitacoras/YYYY-MM-DD_slug.md` con: Resumen;
  Archivos (creados, modificados, movidos, eliminados); Detalle por archivo
  (decisiones, supuestos, intuición); Resultados nuevos (qué comunican, cómo se
  generan, rol en el proyecto); Pendientes. Para las variables que construyen un
  estimador (p. ej. el tratamiento, la cohorte no expuesta, los puntajes AIPW),
  explicar cada una por aparte con su fuente (página del artículo, sección de la
  guía de datos o de la propuesta), cómo se calcula y qué rol cumple. Reportar
  observaciones perdidas.
- **`HANDOFF.md`** (raíz): se lee primero al iniciar una sesión (después de
  ubicarse en la rama) y se propone trabajar en el primer "Siguiente objetivo"
  no asignado a otro integrante. Al cerrar se reescriben "Siguientes objetivos"
  (dos a tres, derivados de las primeras casillas sin marcar de `PLAN.md`, con
  archivo a producir, criterio de terminado y responsable) y "Estado actual", y
  se agrega una entrada arriba en "Registro de sesiones" (tres a cinco líneas,
  enlace a la bitácora y los siguientes objetivos). Las entradas anteriores no
  se editan. Conflictos entre ramas: conservar todas las entradas por fecha.
- **`PLAN.md`**: hitos y tareas `Pk.n` con casillas; se marcan `[x]` en la
  sesión en que se terminan.
- **Skills** (`.claude/skills/`):
  1. `registrar-hallazgo`: al generar o cambiar un resultado. Crea o actualiza la
     nota de `05_Notas/` y contrasta con las notas previas y con la literatura.
  2. `bitacora-sesion`: al terminar la sesión. Escribe la bitácora, verifica las
     notas y actualiza `HANDOFF.md` y `PLAN.md`. No hace commit.
  3. `cerrar-sesion` (`model: haiku`): commit y push a la rama del integrante
     (nunca a `main`), revisando que no entren datos, y copia del `.jsonl` a
     `09_Conversaciones/` (que no se versiona; al final el equipo une las
     conversaciones por aparte).

## 8. Notas de hallazgos (`05_Notas/`)

Memoria analítica del proyecto: qué se encontró y por qué importa (las bitácoras
dicen qué se hizo). Quien arme la presentación debe poder leer solo las notas.

- Una nota por hallazgo principal, en la subcarpeta del script de origen:
  `05_Notas/<script>/<etapa>_<slug>.md`, con `<etapa>` = `D` (datos y
  tratamiento: precio, muestras, desgaste), `A` (ATE y validación: etapas 1-3),
  `H` (heterogeneidad y focalización: etapas 4-6) o `X` (transversal).
- Se crea o actualiza en la misma sesión en que se genera o cambia el resultado.
- Estructura: título-conclusión; Estado (vigente | matizado | reemplazado);
  Etapa / alcance (descriptivo, contraste, placebo); Script de origen; Última
  verificación; Evidencia (rutas exactas en `03_Resultados/`, cifras con escala,
  n de personas y de comunidades); Qué dice en lenguaje intuitivo; Por qué
  importa (pregunta del cliente, subgrupos pre-registrados, relación con E-Q y F-T);
  Límites e incertidumbre; Historial.
- Solo se cita lo que está en `03_Resultados/`. `05_Notas/README.md` es el índice.
- **Contraste con lo registrado:** ante cada resultado nuevo se compara con las
  notas previas y con la literatura de referencia (§5). Si algo es
  contradictorio (dentro del proyecto, o con la literatura sin una explicación
  atribuible a la exposición, la muestra o el diseño), se **alerta al usuario de
  inmediato** con las cifras de ambos lados y no se sobrescribe la nota previa
  sin su decisión. Una diferencia con la literatura atribuible no es una
  contradicción: es parte del aporte (reconciliar E-Q y F-T).

## 9. Literatura clave (detalle en `07_Recursos/Articulos/00_hallazgos_articulos.md`)

Elmira y Qaim (2026) · Frankenberg y Thomas (2017) · Frankenberg, Smith y Thomas
(2003) · Friedman y Levinsohn (2002) · Friedman y Thomas (2009) · Thomas et al.
(2004) · Yamauchi y Larson (2019) · Giles y Satriawan (2015) · Callaway,
Goodman-Bacon y Sant'Anna · Wager y Athey (2018) · Athey, Tibshirani y Wager
(2019) · Athey y Wager (2019) · Yadlowsky et al. (2025, RATE) · Semenova y
Chernozhukov (2021, BLP) · Chernozhukov et al. (2025, GATES). PDF de los cinco
centrales en `07_Recursos/Articulos/` (solo local). Corrección registrada: Block
et al. (2004) usa datos de Java rural, no la IFLS.

## 10. Integrantes

| Nombre | Rol / responsabilidad | Contacto |
|---|---|---|
| Samuel Escandón | Por definir | s.escandoc@uniandes.edu.co |
| Douglas Plazas Guzmán | Por definir | d.plazasg@uniandes.edu.co |
| Mateo Olmos Becerra | Por definir | m.olmosb@uniandes.edu.co |
| Santiago Muñoz Martínez | Por definir | s.munozm234@uniandes.edu.co |

<!-- Copiado del Taller 2; confirmar integrantes y roles del proyecto final. -->

## 11. Decisiones tomadas

> **Histórica.** Desde el 20-nov las decisiones vigentes están en
> `registro_decisiones.md`, que manda sobre esta tabla (por ejemplo, T1 está
> descartada y las versiones se llaman dosis, cuartiles y terciles). No se
> agregan filas nuevas aquí.

| Fecha | Decisión | Justificación |
|---|---|---|
| 2026-11-09 | Tema IFLS / crisis de 1998 en lugar de tweets de Petro y la bolsa | — |
| 2026-11-10 | Se elimina texto como datos | La IFLS no trae texto de salud mental; solo ítems cerrados |
| 2026-11-10 | Métodos = los del curso: Lasso, `rpart`, `ranger`, `grf::causal_forest` con `clusters`, `fixest::feols`. Se descartan `causalTree` y la econometría espacial | Son los de los labs; lo espacial no aparece en el curso |
| 2026-11-10 | Otros países no se usan como respaldo de identificación; solo como referentes de magnitud | Responden otra pregunta, un solo país tratado, +1-2 semanas |
| 2026-11-10 | Respaldos de identificación dentro de la IFLS: cohortes mayores de la misma comunidad, hermanos (EF de hogar), productores vs. compradores netos, tendencias previas 1993-97 | Controlan choques comunes a la comunidad y lo fijo del hogar |
| 2026-11-11 | Núcleo = estatura (ancla) + escolaridad 2014 + cognición; salud mental pasa a extensión opcional (recomendación; falta confirmación del equipo) | Más muestra, ancla parcial; salud mental es ruidosa, sin ATE de referencia ni ola 1997/98 pública |
| 2026-11-12 | Las guías de datos son descriptivas; las decisiones de uso se toman con todas las olas revisadas | Decidir con el panorama completo |
| 2026-11-18 | Se retira el árbol causal; toda la heterogeneidad se estima con el bosque causal. El entregable al cliente es la comparación de reglas (RATE) y el perfil de los hogares que prioriza el bosque | Decisión del equipo, por robustez (`10_Propuesta/04` §6.4) |
| 2026-11-18 | Repositorio `talleres-ECON3785/proyecto_final` con la estructura de los talleres (`01_Datos`…`10_Propuesta`), `HANDOFF.md`, `PLAN.md` y las skills de bitácora, cierre y hallazgos | Mismo flujo que dio buenos resultados en los Talleres 1 y 2 |
| 2026-11-18 | Los datos de la IFLS viven dentro del repositorio local (`01_Datos/01_Crudos/`) pero **no se versionan**, ni sus derivados (`02_Procesados/`, `03_Listos/`). Sí se versionan las guías `.md`, la síntesis y los scripts de revisión. Reglas de datos en `01_Datos/CLAUDE.md` | La licencia de RAND prohíbe redistribuir y el repositorio es público; además pesan 4,3 GB (GitHub rechaza archivos de más de 100 MB). La entrega pide "datos o instrucciones": van las instrucciones (`01_Datos/README.md`) |
| 2026-11-18 | Los PDF de artículos (`07_Recursos/Articulos/`) e insumos de terceros (`07_Recursos/Insumos/`) se guardan solo en local | Derechos de autor en un repositorio público |
| 2026-11-20 | **Alcance: solo estatura** (ΔHAZ 1997-2000, cohorte 0-5). Se descartan por ahora la escolaridad 2014, la cognición y la salud mental. Presentación en tres preguntas: ¿dolió?, ¿a quién?, ¿el bosque supera a las reglas simples? | Decisión del equipo: 20 minutos que deben quedar pulidos y defendibles sin abarcar de más |
| 2026-11-20 | Tratamiento en cuatro versiones: T1 réplica E-Q (cambio proporcional, todas las fuentes, nominal); T2 dosis limpia, principal (fuentes comunes 1997-2000, calidad media, kg, winsorizada p1/p99); T3 cuartiles de T2; T4 terciles de T2, alto frente a bajo sin el medio, para el bosque. Terciles nacionales o dentro de provincia según la prueba 1 (pendiente) | E-Q usan cambio proporcional, no Δlog (p. 5); el PKK no trae precios en 2000; cola de +729 %; RATE nativo exige W binario. Recomendación de la sesión de Santiago tras evaluarla con un consejo de cinco asesores; **confirmar con el equipo** |
| 2026-11-20 | **Precio:** el tratamiento principal usa solo las fuentes presentes en 1997 y 2000 (posyandu + `bk2_hpj`), con cambio proporcional **nominal**. El PKK de 1997 entra solo en T1 (réplica aproximada). El deflactor de E-Q queda como extensión opcional. Errores robustos y agrupados, uno al lado del otro, en la réplica; los programas de la red de seguridad social, solo en la columna de réplica | El suplemento de E-Q no dice qué fuente usaron en 2000 ni agrupa por comunidad. Con un deflactor común, el cambio real solo reescala β. Decisión de Santiago en la sesión del 20-nov (`PLAN.md` H1); informar al equipo |
| 2026-11-20 | El ATE se replica con `feols` (panel con EF individuales ≡ primeras diferencias); la pendiente promedio del bosque solo como fila de robustez. La no linealidad se estudia con `feols` (cuartiles y spline), no con bosques | El estimando de `grf` continuo no es el β MCO de E-Q, y el bosque supone efecto lineal en W dado x. Recomendación; **confirmar con el equipo** |
| 2026-11-20 | **R para todo el pipeline**, también para construir las bases (`haven::read_dta()`, ampliación). Python solo en lo exploratorio | Un solo lenguaje para la entrega reproducible y un solo punto de entrada (`00_main.R`). Decisión de Santiago (P1.4) |
| 2026-11-20 | **Pre-registro de la heterogeneidad** (`10_Propuesta/07_preregistro_heterogeneidad.md`): réplica de las cinco interacciones de E-Q (edad crítica, mujer, madre con educación alta, pobre, urbano; cuadros A4-A5) con `feols`; seis GATE con el bosque T4 (edad 3-5 frente a 0-2, urbano, madre con más que primaria, mujer, comprador neto, pobre) | Fijar subgrupos antes de ver resultados (§5.6). Decisión de Santiago (P1.3) |
| 2026-11-20 | **Familias de Holm** (α = 0,05, bilateral): F1 = los seis contrastes GATE (m = 6); F2 = las cinco interacciones de E-Q con T1 y EE agrupados (m = 5); F3 = las tres diferencias de RATE bosque − regla (m = 3). El ATE, `test_calibration`, el AUTOC del bosque y la BLP quedan fuera de toda familia. Holm simple, sin secuencia con la edad primero | Controla la probabilidad de algún falso positivo por familia con cualquier dependencia; la predicción para la edad viene de una asociación de 2014, demasiado débil para una secuencia fija. Decisión de Santiago (P1.3) |
| 2026-11-20 | **Métrica de RATE: AUTOC** (`target = "AUTOC"`); QINI no se reporta | El cliente atiende primero a quien más sufre (pesa la cabeza del orden) y es la métrica del Lab 10. Decisión de Santiago (P1.3) |
| 2026-11-20 | **Ampliaciones registradas:** `haven`, `get_scores`, `best_linear_projection`, `average_treatment_effect(subset = …)` (ya registrada en el Taller 2) y, si se usa, `fwildclusterboot` | Requisito de §6 (registrar antes de usar). `anthro`/`anthroplus` (HAZ OMS) se registran cuando se cree `04_haz` |

## 12. Análisis descartados

| Fecha | Análisis | Razón |
|---|---|---|
| 2026-11-10 | Texto como datos (salud mental) | Ver "Decisiones tomadas" |
| 2026-11-10 | `causalTree` y econometría espacial | Fuera del curso |
| 2026-11-18 | Árbol causal honesto sobre puntajes AIPW (antes etapa 7) | Decisión del equipo; ver "Decisiones tomadas" |
| 2026-11-20 | Escolaridad 2014 (con la recuperación de la celda de 8 años de F-T y el bosque placebo en la cohorte no expuesta), cognición, estatura adulta y salud mental | Alcance; ver "Decisiones tomadas" |
| 2026-11-20 | Bosque causal para replicar el ATE y para la no linealidad; `lm_forest` y `multi_arm_causal_forest` | Estimando distinto o sin herramientas de inferencia (`lm_forest` solo tiene `predict`); fuera del catálogo del curso |
| 2026-11-20 | Rendimiento escolar en 2000 (prueba EK de 2000, cohorte de 7-11 años en 1997; ~2.904 niños en 308 comunidades según un conteo exploratorio) | Decisión de Santiago: la prueba de 2000 no es comparable con la de 1997 (instrumento rediseñado, sin puntaje total, 18 ítems) y el efecto dependería de cómo se construya el resultado (corte transversal, valor agregado o cambio en z). El EBTANAS reportado solo lo tienen 989 niños en 1997 |
