# 02 · Datos: cómo acceder a la IFLS y qué tener en cuenta al manejarla

## Qué es

La Indonesia Family Life Survey (IFLS) es un panel de hogares, individuos, comunidades y establecimientos (RAND, con Lembaga Demografi-UI, UCLA y SurveyMETER). La muestra de 1993 cubre 13 de las 26 provincias de entonces y representa cerca del 83 % de la población; son 7.224 hogares en 321 áreas de enumeración.

| Ola | Año | Relevancia para el proyecto |
|---|---|---|
| IFLS1 | 1993-94 | Pre-crisis lejana. Sirve para **tendencias previas** (placebo 1993→1997). |
| IFLS2 | 1997 (ago-1997 a inicios de 1998) | **Línea base**: justo antes del colapso de la rupia de enero de 1998. |
| IFLS2+ | 1998 | Submuestra del 25 % en plena crisis. **No aparece en la página pública de descarga**; no contar con ella. |
| IFLS3 | 2000 | Corto/mediano plazo. Precio del arroz post-crisis. |
| IFLS4 | 2007-08 | Mediano plazo. Primer CES-D (10 ítems). |
| IFLS5 | 2014-15 | **Largo plazo**: 16.204 hogares, 50.148 individuos; CES-D, personalidad (Big Five), cognición, bienestar subjetivo. |

IFLS East (2012) cubre provincias orientales que no estaban en 1993; no sirve para este diseño porque no tiene línea base de 1997.

## Cómo acceder

1. Registrarse en la página de RAND ("Register to Download Data") y descargar desde **IFLS Data and Documentation**: <https://www.rand.org/health/surveys/FLS/IFLS/download.html>. Es gratis. Cada integrante que toque los datos debe registrarse.
2. Bajar, por ola: datos del hogar (HH), datos comunitarios y de establecimientos (CF), cuestionarios, codebooks y User's Guide (vol. 1 y 2).
3. Formatos: Stata (v6 para IFLS1-RR e IFLS2, v7 para IFLS3, v9 para IFLS4 y 5) y SAS. En R se leen con `haven::read_dta()`.
4. Los agregados de consumo (PCE) existen para IFLS1-4; RAND los publica pero no los soporta.

**Restricciones:** no redistribuir los datos y no intentar identificar personas, hogares ni comunidades. Para la entrega del curso esto significa: **el `.zip` final no puede incluir los datos**; el `README.md` debe dar las instrucciones de descarga y un script que construya la base desde los archivos crudos (el enunciado del proyecto lo permite: "el código y los datos, o las instrucciones para obtenerlos"). Citar el informe de campo de cada ola usada.

## Estructura y llaves

- Los datos vienen en "libros" (B1, B2, B3A, B3B, B4, B5, US, EK…) y, dentro, módulos; hay un archivo por módulo. No hay una base plana.
- **Individuo:** `pidlink` (constante entre olas). **Hogar:** `hhid93`, `hhid97`, `hhid00`, `hhid07`, `hhid14` (los hogares se dividen, así que el id cambia). **Comunidad:** `commid93/97/00/…`.
- `ptrack` y `htrack` dicen en qué olas aparece cada persona/hogar y dónde. Son el punto de partida de cualquier merge.
- RAND advierte que aun trabajando una sola ola hay que traer información de olas previas, porque las historias retrospectivas no se repiten.

## Variables que necesitamos y dónde están (a confirmar en codebooks)

| Constructo | Fuente probable | Nota |
|---|---|---|
| Precio del arroz por comunidad, 1997 y 2000 | Encuesta comunitaria: libro PKK (módulo de precios, jefa del grupo de mujeres), libro de precios de mercado (visita a hasta 3 puntos de venta), informante de posyandu | Hasta **seis fuentes de precio por comunidad**; la guía sugiere usar media o mediana. |
| Antropometría (talla, peso) | Libro US, todas las olas | Convertir a z-scores con estándares OMS (`anthro`/`zscorer` en R). |
| Educación, trabajo, ingresos | B3A (DL, TK), B5 para niños | |
| Cognición | Libro EK | Pruebas distintas por edad y ola; estandarizar dentro de ola-edad. |
| Salud mental | B3B: ítems tipo GHQ en 1993 y 2000; sección KP con CES-D-10 en 2007 y 2014 | No comparables entre sí directamente (ver archivo 05). |
| Producción de arroz / tierra | B2 (UT, negocio agrícola), B1 (consumo: arroz comprado vs. autoproducido en KS) | Para clasificar productor neto vs. comprador neto en 1997. |
| Riqueza y activos (oro) | B2 (HR), B3A (HR) | |
| Características de la comunidad | Libro 1 y 2 comunitarios | Urbano/rural, distancia a mercado, infraestructura, actividad principal. |

## Consideraciones de manejo (las que más pueden dañar el resultado)

1. **El tratamiento varía a nivel de comunidad, no de individuo.** Hay ≈ 312 comunidades con precios. El tamaño efectivo de muestra para identificar el efecto es del orden de 312, no de miles. Errores estándar y partición de muestras siempre **por comunidad**.
2. **Asignar el tratamiento por la residencia de 1997** (`commid97`), no por la residencia actual. Quien migró después sigue "tratado" según donde vivía cuando llegó el choque. La migración es un resultado, no un control.
3. **El precio de 2000 no es el pico de 1998.** El cambio 1997→2000 mide el aumento persistente, con ruido respecto a la intensidad real de la crisis. Contrastar con precios BPS por ciudad/provincia (ene-1997 a oct-1998, como Friedman y Levinsohn).
4. **Ruido y sesgo en precios comunitarios.** La documentación de RAND reporta que las informantes PKK y de posyandu tienden a sobre-reportar frente al precio de mercado. Preferir el libro de mercado; usar mediana; revisar unidades (Rp/kg vs. Rp/litro) y calidad del arroz; winsorizar.
5. **Fecha de entrevista.** Una parte de IFLS2 se recogió a inicios de 1998, ya con la rupia en caída. Verificar fecha de entrevista comunitaria y de hogar; excluir o marcar las de 1998.
6. **Desgaste y selección.** El recontacto es muy alto (94 % de hogares en IFLS2; > 90 % en IFLS5), pero no aleatorio. Además, hay selección por mortalidad infantil. Comparar características de 1997 de quienes se observan en 2014 vs. quienes no, por nivel de tratamiento.
7. **Pesos.** Hay pesos transversales y longitudinales por ola. Para efectos causales con controles ricos se suele trabajar sin pesos y reportar la versión ponderada como robustez.
8. **Códigos especiales.** Valores 8/9/98/99 y variables `x` ("no sabe", "rehúsa", "falta") están por todas partes; limpiar antes de promediar.
9. **Comparabilidad entre olas.** Cuestionarios cambian (p. ej., la salud mental). No asumir que la misma etiqueta mide lo mismo.
10. **Volumen.** IFLS5 sola son cientos de archivos. Fijar desde ya una lista corta de módulos y un script `01_build.R` reproducible.

## Datos auxiliares para la identificación (v2)

| Dato | Para qué | Fuente y precedente |
|---|---|---|
| Precios al consumidor por ciudad (BPS), ene-1997 a oct-1998 | Medida alterna del alza, con el pico de 1998 | Usados por Friedman y Levinsohn; hay que conseguir la serie histórica de BPS |
| Luces nocturnas DMSP-OLS 1996-1998 por kabupaten | Intensidad del choque de actividad económica | Usadas con la IFLS en un artículo de 2026 del *Journal of Development Economics* |
| Lluvia 1997 por estación/distrito | Controlar la sequía de El Niño | Maccini y Yang enlazan lluvia histórica con la IFLS |
| Exposición al humo de 1997 | Controlar incendios | Jayachandran usa mediciones satelitales de aerosoles; como mínimo, indicador de Sumatra y Kalimantan |

Solo las dos últimas son baratas (un indicador por isla basta para la robustez). Las dos primeras son opcionales.

## Tiempo estimado realista

- Registro y descarga: 1 día.
- Construir panel niño 1997-2000-2014 con antropometría y controles: 4-6 días de una persona que no conoce la IFLS.
- Construir precio del arroz por comunidad en 1997 y 2000 y validarlo: 2-3 días.
- Total antes de estimar nada: **≈ 2 semanas**. Con la asesoría en semana 15, conviene llegar con el panel mínimo y la distribución del tratamiento, aunque no haya resultados.
