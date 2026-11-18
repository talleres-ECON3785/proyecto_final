# Traspaso · Revisión de datos IFLS: dónde seguir (13-nov-2026)

Nota para la próxima sesión. La sesión anterior no pudo seguir porque se perdió la conexión con el computador de Santiago. Por eso esta nota está en el Project y no en la carpeta local.

## Dónde estamos

- **Rondas 1 a 4 revisadas**, cada una con su guía descriptiva en la carpeta local `Proyecto Final/Datos/`:
  - `IFLS1/00_guia_IFLS1.md`: 1993. Versión 2, reescrita para que sea neutral; la v1 está en `IFLS1/_obsoleto/`.
  - `IFLS2/00_guia_IFLS2.md`: 1997, incluido `bek` (pruebas cognitivas), descargado aparte el 12-nov.
  - `IFLS3/00_guia_IFLS3.md`: 2000.
  - `IFLS4/00_guia_IFLS4.md`: 2007-08.
- **Siguiente paso: ronda 5 (IFLS5, 2014-15).** Santiago dice que ya está descargada en `Datos/` (seguramente en `Datos/IFLS5/`). No se ha abierto.
- `CLAUDE.md` (raíz del proyecto local) ya está actualizado con el estado, las reglas de manejo de cada ola y los pendientes. **Leerlo primero.**

## Regla clave del usuario

Las guías son **descriptivas**: qué hay, cómo está codificado, qué problemas tiene. **No** asignan variables a resultado, control o muestra, y no dicen para qué sirve cada módulo. Las opciones van en una sección «Preguntas abiertas», sin recomendación. Las decisiones de uso se toman cuando estén revisadas todas las olas. Esto también está en `CLAUDE.md`, §4 (fila del 12-nov) y §8.

## Cómo se hizo cada ronda (repetir para IFLS5)

1. **Inventario.** Listar los `.dta`, filas, columnas y versión del formato (primer byte). Buscar `.zip` sin extraer. Revisar la documentación disponible: guía de usuario, codebooks y cuestionarios.
2. **Cotejo con la documentación.** Comparar los archivos y conteos con la lista de módulos de los codebooks y con el apéndice A de la guía de usuario. Ojo: el apéndice A de IFLS4 era copia del de IFLS3.
3. **Problemas de lectura con `pyreadstat`.**
   - Valores 1,75e+100 en lugar de faltantes (pasó en los comunitarios de 1997).
   - Enteros con faltantes leídos como objeto (pasó en IFLS3).
4. **Llaves.** Probar la unicidad de `hhidXX`, `hhidXX`+`pidXX`, `pidlink`, `commidXX`, `fcodeXX`, `mkidXX`, sumando las variables `…type`. Marcar como «no determinada» la que no salga.
5. **Seguimiento con `htrack`/`ptrack`.**
   - Hogares: códigos `resultXX`, sexto dígito del `hhid` (tipo de *split-off*), `moverXX`.
   - Personas del roster de 1993: códigos `ar01a`.
   - `commid` de quienes se mudaron: con letras desde 2000. Unión con el mini-CFS por `mkid`.
   - Panel completo.
6. **Fechas.** Año y mes de entrevista del hogar, la comunidad, la antropometría y las pruebas cognitivas. Contrastar con lo que dice la documentación.
7. **Temas.**
   - Antropometría: talla válida, rango, fuentes de edad.
   - Salud mental: qué ítems, escala, frecuencias. Comparar etiquetas del codebook con el cuestionario, porque en IFLS4 no coincidían.
   - Educación.
   - Pruebas cognitivas: archivos, ítems con respuesta por versión, si hay puntaje total.
   - Arroz: consumo, precio pagado por el hogar, programas como Raskin.
   - Choques: el módulo general no existe en 2007.
   - Precios comunitarios del arroz: fuentes, calidades, unidades kg/litro, medianas y p1/p99 sin limpiar.
8. **Seguimiento de la cohorte de 0-5 años en 1997** (`ptrack$age_97` ≤ 5 y `member97` = 1; son 3.851 niños). Contar cuántos son miembros del hogar en la ola, cuántos tienen talla y cuántos pruebas cognitivas.
9. **Escribir `IFLS5/00_guia_IFLS5.md`** con la misma estructura que las anteriores:
   1. Qué es la ronda.
   2. Archivos.
   3. Mapa de la documentación.
   4. Libros y quién responde.
   5. Catálogo con llaves verificadas.
   6. Manejo.
   7. Seguimiento.
   8. Fechas.
   9. Temas.
   10. Comunidad.
   11. Enlace con olas anteriores.
   12. Preguntas abiertas.
   13. Lo que no está verificado.
10. **Actualizar `CLAUDE.md`:** estado (§1), árbol de carpetas (§3), reglas de manejo de IFLS5 (§7) y pendientes (§10).

Herramientas que se usaron: Python con `pyreadstat` y `pandas` (en la VM local puede hacer falta `pip install --break-system-packages pyreadstat pandas`) y `pdftotext` para la documentación. Español en todo. Nunca inventar cifras: todo sale de los archivos o de la documentación citada.

## Para tener a mano en IFLS5 (lo que importa al proyecto)

- **Escolaridad completada en 2014** de las cohortes de 5 a 21 años en 1997: es uno de los resultados núcleo de la propuesta.
- **Estatura adulta en 2014** de la cohorte de 0-5 años en 1997.
- **Pruebas cognitivas 2014** (EK): ¿mismo diseño que en 2000 y 2007? ¿Ítems comunes?
- **Salud mental 2014** (CES-D de adultos y quizás de niños; la propuesta menciona «CES-D 2014 de niños»).
- **Precios del arroz y programas** (Raskin) en 2014-15.
- Comparabilidad de `commid14`/`mkid14` y de los pesos.

## Pendientes abiertos que no dependen de IFLS5

- Preguntas abiertas de cada guía (§12 de IFLS2, IFLS3 e IFLS4; §10 de IFLS1).
- IFLS2: falta el archivo `b3p_tk4`, que no es importante.
- IFLS4: aclarar los códigos 6 y 98 de `mover07`, el código de comunidad `9999` y las 9 comunidades con dos filas en los archivos comunitarios.
- Resto de pendientes del equipo y de la literatura: ver `CLAUDE.md` §10.
