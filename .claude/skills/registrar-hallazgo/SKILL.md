---
name: registrar-hallazgo
description: Crea o actualiza una nota de hallazgo en 05_Notas/ (un .md por hallazgo principal, con referencia a tablas/figuras, explicación intuitiva e importancia para el cliente) y contrasta la evidencia nueva con las notas existentes y con la literatura de referencia (Elmira y Qaim 2026; Frankenberg y Thomas 2017), alertando de inmediato si algo es contradictorio. Usar cuando se genere o cambie un resultado (tabla, figura, estimación, base de tratamiento), cuando el usuario pida "registrar un hallazgo", "escribir la nota", "actualizar las notas" o "contrastar con lo anterior", y antes de dar por cerrado un análisis.
---

# Registrar hallazgo y contrastar evidencia

Mantiene `05_Notas/` como memoria analítica del proyecto. Las reglas de fondo
están en `CLAUDE.md` §8; esta skill es el procedimiento. Se invoca cuando se
genera o cambia un resultado, no solo al cerrar la sesión.

Básate solo en resultados que existan en `03_Resultados/` y en lo ocurrido en la
conversación. Si algo no es inferible con certeza (la escala de una cifra, la
muestra, cuántas comunidades hay detrás, si dos números son comparables),
pregunta en vez de adivinar.

## Paso 1: identificar el hallazgo y su evidencia

1. Qué tablas o figuras de `03_Resultados/` contienen el resultado y qué script
   de `02_Scripts/` las genera. Confirma que existen (`ls`); una cifra sin
   archivo no entra a una nota.
2. Lee `05_Notas/README.md`: si ya hay nota sobre el mismo hallazgo, se
   actualiza; si no, se crea.
3. Un hallazgo es un resultado que sostiene, matiza o contradice una conclusión
   del proyecto o una hipótesis H1-H9. Un resultado intermedio sin esa
   implicación queda solo en la bitácora. Los resultados de datos y tratamiento
   (distribución del precio, desgaste, balance) sí son hallazgos: sostienen la
   identificación.

## Paso 2: contrastar antes de escribir

Contrasta con:

- las notas de `05_Notas/` de la misma etapa y las transversales (`X_`);
- la literatura de `CLAUDE.md` §5 (Elmira y Qaim 2026: −0,135 HAZ por +100 % de
  precio nominal; Frankenberg y Thomas 2017: sin daño en talla y −1,95 años en la
  cohorte urbana pobre de 8 años) y `10_Propuesta/01` y `04`;
- las hipótesis pre-declaradas H1-H9 (`10_Propuesta/04` §4) y "Decisiones
  tomadas" de `CLAUDE.md`.

Compara dirección, orden de magnitud, **escala** (precio nominal o real; Δlog o
terciles; z, años o cm), muestra (cohorte, olas, exclusiones) y unidad de
inferencia (número de comunidades, agrupamiento).

| Clasificación | Qué significa | Qué se hace |
|---|---|---|
| **Consistente** | Coincide con lo registrado o con la literatura. | Actualizar "Última verificación" e historial. |
| **Difiere (atribuible)** | Difiere de la literatura y se explica por la exposición (precio frente a zona), la muestra, las olas o el diseño. | Es parte del aporte (reconciliar E-Q y F-T): se registra como "difiere" con la atribución. No es alerta. |
| **Contradictorio** | Choca con otra nota del proyecto, o con la literatura sin explicación atribuible. | Alertar (Paso 3). |

Si no puedes distinguir "difiere (atribuible)" de "contradictorio", trátalo como
contradictorio.

Contra las hipótesis H1-H9: registra si el resultado la apoya, no la apoya o es
inconcluso, **sin reformular la hipótesis** después de ver el resultado. Si el
resultado sugiere una dimensión nueva, se marca como exploratoria.

## Paso 3: alertar si hay contradicción

Detén el registro y avisa al usuario en ese momento, sin resolverlo en silencio:

1. Qué se contradice: ruta de la nota o fuente previa y del resultado nuevo.
2. Las cifras de ambos lados con escala, muestra, n de personas y de comunidades.
3. Hipótesis de la causa: construcción del tratamiento, muestra o desgaste,
   unidad o agrupamiento, semilla o hilos de `grf`, error de código o de unión de
   datos (llaves duplicadas), o diferencia en el estimando.
4. Qué verificar para resolverlo (chequeo concreto, con el script o la tabla).

Mientras el usuario no decida: no sobrescribas la nota anterior ni cambies su
estado; deja la evidencia nueva en el historial o en una nota marcada como
pendiente de conciliar. Con la decisión: marca la nota previa como `matizado` o
`reemplazado` (con enlace) y, si cambió una conclusión, regístralo en "Decisiones
tomadas" de `CLAUDE.md`.

## Paso 4: escribir o actualizar la nota

Ruta: `05_Notas/<script>/<etapa>_<slug>.md`, en la subcarpeta del script de
origen, con `<etapa>` = `D` (datos y tratamiento), `A` (ATE y validación), `H`
(heterogeneidad y focalización) o `X` (transversal); slug en minúsculas con guion
bajo (p. ej. `D_distribucion_precio_arroz.md`, `H_calibracion_bosque.md`).

```markdown
# <Hallazgo, enunciado como conclusión>

- **Estado:** vigente | matizado | reemplazado (con enlace a la nota que lo reemplaza)
- **Etapa / alcance:** D, A, H o X; descriptivo, contraste entre comunidades o placebo
- **Script de origen:** `02_Scripts/<script>.R`
- **Hipótesis relacionada:** H1-H9 o "ninguna" (y si la apoya, no la apoya o es inconcluso)
- **Última verificación:** YYYY-MM-DD, con el script que lo genera

## Evidencia
Rutas exactas de las tablas/figuras en `03_Resultados/`. Cifras clave con escala,
n de personas, n de comunidades e intervalo o error estándar agrupado.

## Qué dice, en lenguaje intuitivo
Qué muestra y cómo leerlo, para alguien sin formación técnica (la agencia
cliente). Distingue estimando, estimador y estimación; separa lo descriptivo del
contraste causal.

## Por qué importa en el estudio
Qué pregunta del cliente responde (a quién proteger primero), con qué hallazgo
de la literatura se conecta (se replica, difiere o lo contradice) y qué implica
para la regla de focalización.

## Límites e incertidumbre
Qué no permite afirmar (es un contraste entre comunidades con más y menos alza,
no el efecto de la crisis; choques simultáneos; desgaste), potencia (cuántas
comunidades) y qué evidencia adicional haría falta.

## Historial
- YYYY-MM-DD: qué cambió y por qué.
```

Reglas de redacción (de `CLAUDE.md`):

- Sin juicios de "bueno" o "malo" y sin entusiasmo por coeficientes o
  significancia. Magnitud e incertidumbre.
- Sin código. Sin nombres de variables en la explicación intuitiva (di "precio
  del arroz de la comunidad", "años de escolaridad", no `commid97`, `dl06`).
- Los CATE son estimaciones con incertidumbre; que el bosque encuentre grupos no
  prueba heterogeneidad (eso lo dice `test_calibration`); `variable_importance`
  no es un efecto.
- Nunca cifras de memoria: toda cifra viene de `03_Resultados/` o de un artículo
  con página.

## Paso 5: actualizar el índice

Actualiza la tabla de `05_Notas/README.md`: una fila por nota con archivo,
estado, etapa/alcance y la pregunta que responde. No edites las filas de otras
notas salvo para cambiar un estado decidido por el usuario.

## Cierre

Reporte corto: notas creadas o actualizadas (rutas), la clasificación de cada
contraste (consistente, difiere, contradictorio) y, si hubo alertas, qué quedó
pendiente de decisión. Esta skill no hace commit: los cambios se versionan con
`cerrar-sesion` (en la rama del integrante, nunca en `main`).
