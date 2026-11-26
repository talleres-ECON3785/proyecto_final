# 01_Datos · Cómo obtener los datos de la IFLS

Este repositorio es público y **no trae los datos**: la licencia de RAND prohíbe
redistribuir la Indonesia Family Life Survey (IFLS). Cada persona que quiera
reproducir el proyecto debe descargarlos con su propia cuenta y ponerlos en
`01_Crudos/`, con la estructura de abajo. Después basta con correr `00_main.R`
desde la raíz.

Las reglas para manejar los datos (llaves, códigos, problemas de lectura) están
en [`CLAUDE.md`](CLAUDE.md); la descripción de cada ola, en las guías
`01_Crudos/IFLSx/00_guia_IFLSx.md` y en la síntesis
[`00_sintesis_revision_IFLS.md`](00_sintesis_revision_IFLS.md).

## 1. Registro y descarga

1. Página de la IFLS en RAND:
   <https://www.rand.org/well-being/social-and-behavioral-policy/data/FLS/IFLS.html>.
2. Registrarse en «Register to Download Data»
   (<https://www.rand.org/health/surveys/FLS/IFLS/access.html>) y aceptar las
   condiciones de uso.
3. Descargar, para cada ola, los **datos de hogar** y los **datos comunitarios**
   en formato Stata (`.dta`), y la documentación (guía de usuario, codebooks y
   cuestionarios).
   - Para reproducir el pipeline bastan IFLS1 (1993), IFLS2 (1997) e IFLS3
     (2000). IFLS4 (2007-08) e IFLS5 (2014-15) solo se usaron en la revisión de
     datos (guías de cada ola) y no hacen falta.
   - IFLS2: el módulo de pruebas cognitivas (`bek`) puede venir aparte; hace
     falta (guía IFLS2 §2 y §9.4).
   - IFLS2+ (1998) no está en la descarga pública y el proyecto no la usa.
4. Descomprimir los `.zip` de datos.

## 2. Dónde poner cada cosa

Los scripts esperan exactamente estos nombres de carpeta (los de la descarga que
usó el equipo en noviembre de 2026):

```
01_Datos/01_Crudos/
├── IFLS1/  Household Data/   Community Data/   Documentation/
├── IFLS2/  Household Data/   Community Data/   Documentation/
├── IFLS3/  Household Data/   Community Data/   Household Documentation/   Community Documentation/
├── IFLS4/  Household Data/   Community Data/   Household Documentation/   Community Documentation/
└── IFLS5/  Household Data/   Community Data/   Documentation/
```

Las guías (`00_guia_IFLSx.md`) ya están en cada carpeta porque sí se versionan.
El número de archivos `.dta` que debe haber en cada carpeta está en la sección 2
de cada guía; sirve para comprobar que la descarga quedó completa.

`00_main.R` se detiene con un mensaje si falta la carpeta `Household Data` de
IFLS1, IFLS2 o IFLS3.

## 3. Qué se versiona y qué no

| Ruta | ¿En GitHub? | Por qué |
|---|---|---|
| `01_Crudos/**/*.md`, `01_Crudos/IFLS5/_revision/` | Sí | Guías y scripts de revisión: descripción, sin microdatos |
| `01_Crudos/**` (datos y documentación de RAND) | No | Licencia de RAND y tamaño (4,3 GB) |
| `02_Procesados/`, `03_Listos/` | No | Microdatos derivados: misma licencia |
| `00_sintesis_revision_IFLS.md`, `CLAUDE.md`, `README.md` | Sí | Documentación propia |

## 4. Cómo citar

Citar la IFLS con el informe de campo de cada ola, como recomienda la guía de
usuario de RAND (verificado en `IFLS2/Documentation/volume1.pdf` e
`IFLS3/Household Documentation/IFLS2000_UsersGuide_vol1.pdf`):

- IFLS1: Frankenberg, E. y L. Karoly (1995). «The 1993 Indonesian Family Life
  Survey: Overview and Field Report». RAND, DRU-1195/1-NICHD/AID.
- IFLS2: Frankenberg, E. y D. Thomas (2000). «The Indonesia Family Life Survey
  (IFLS): Study Design and Results from Waves 1 and 2». RAND,
  DRU-2238/1-NIA/NICHD.
- IFLS3: Strauss, J., K. Beegle, B. Sikoki, A. Dwiyanto, Y. Herawati y F.
  Witoelar (2004). «The Third Wave of the Indonesia Family Life Survey (IFLS3):
  Overview and Field Report». RAND, WR-144/1-NIA/NICHD.
- IFLS4 (revisión de datos): Strauss, J., F. Witoelar, B. Sikoki y A. M. Wattie
  (2009). «The Fourth Wave of the Indonesia Family Life Survey: Overview and
  Field Report», vol. 1. RAND, WR-675/1-NIA/NICHD.
- IFLS5 (revisión de datos): Strauss, J., F. Witoelar y B. Sikoki (2016). RAND,
  WR-1143/1.
