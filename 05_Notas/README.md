# Notas de hallazgos

Cada nota recopila un hallazgo principal del proyecto: qué evidencia lo sostiene
(tablas y figuras de `03_Resultados/`), qué dice en lenguaje intuitivo y por qué
importa para el cliente. Las bitácoras (`06_Bitacoras/`) cuentan qué se hizo en
cada sesión; las notas cuentan qué se encontró. Quien arme la presentación debe
poder leer solo estas notas y reconstruir los mensajes principales.

Las reglas están en `CLAUDE.md` §8. Las notas se crean y actualizan con la skill
`registrar-hallazgo`, que también contrasta la evidencia nueva con lo registrado
aquí y con la literatura de referencia (Elmira y Qaim 2026; Frankenberg y Thomas
2017), y alerta si algo es contradictorio.

## Convenciones

- Una subcarpeta por script de origen, con el nombre del script sin `.R`
  (p. ej. `05_Notas/02_precio_arroz/`).
- Nombre: `<etapa>_<slug>.md`, con `<etapa>` = `D` (datos y tratamiento), `A`
  (ATE y validación), `H` (heterogeneidad y focalización) o `X` (transversal).
- Estado: `vigente`, `matizado` o `reemplazado` (con enlace a la nota que lo
  reemplaza).
- Toda cifra remite a un archivo de `03_Resultados/`.

## Índice

| Nota | Estado | Etapa / alcance | Pregunta que responde |
|---|---|---|---|
| [`01_tracks/D_cohortes_desgaste.md`](01_tracks/D_cohortes_desgaste.md) | vigente | D; descriptivo | ¿Cuántos niños y comunidades quedan tras el seguimiento 1993-2000 y con HAZ válido? |
| [`02_precio_arroz/D_distribucion_precio_arroz.md`](02_precio_arroz/D_distribucion_precio_arroz.md) | vigente | D; descriptivo | ¿Cuánto subió el arroz y cuánto varía el alza entre comunidades y dentro de provincia? |
| [`05_base/D_desgaste_segun_alza.md`](05_base/D_desgaste_segun_alza.md) | vigente | D; descriptivo | ¿El desgaste depende del alza del precio? ¿Qué hacer con la cola del ΔHAZ? |
| [`06_ate/A_ate_promedio.md`](06_ate/A_ate_promedio.md) | vigente | A; contraste | ¿Dolió? Efecto promedio del alza del arroz en la talla y comparación con E-Q |
| [`07_cuartiles/A_forma_cuartiles.md`](07_cuartiles/A_forma_cuartiles.md) | vigente | A; contraste | ¿El daño crece de forma pareja con el alza? Efecto por cuartiles frente a la recta |
