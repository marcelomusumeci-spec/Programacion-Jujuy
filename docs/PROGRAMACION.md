# Programación vigente R2 · Obra Jujuy

## Fuente definitiva para las fechas del tablero

Archivo entregado por el usuario: **Jujuy_Programacion_completa_revisada.pdf**, 40 páginas, versión PDF de su Excel R2. La app adopta las fechas explícitas de **Inicio y Fin de la sección 2**; no las desplaza desde R1 ni las calcula a partir de los índices internos o de Disponibilidad mínima.

Se transcribieron las **395 actividades e hitos**, incluidos los nuevos IDs H16, LIB y L1–L8. Los 385 IDs numéricos se cotejaron contra las fechas de revisión de la sección 4, que conserva 491 registros de trazabilidad. Todas las duraciones de actividades coinciden con el calendario de vacaciones R2. La fuente, su SHA-256 y la página de cada actividad quedan registrados en `data/schedule.json`.

**Inicio de las actividades del modelo: 09/11/2026. Cierre general: 13/10/2027.** El inicio del modelo no se presenta como fecha histórica real de inicio de obra. Se mantienen visibles las condiciones y supuestos que el propio documento señala; la incorporación de fechas no acredita ejecución ni habilitación de uso.

## Fechas de control

| Frente | Fin ET2 | Contrapiso terminado | Inicio ET3 | Fin ET3 | Inicio yesería | Entrega |
|---|---|---|---|---|---|---|
| P1 | 13/11/2026 | 13/11/2026 | 16/11/2026 | 27/11/2026 | 30/11/2026 | 10/03/2027 |
| P2 | 20/11/2026 | 20/11/2026 | 23/11/2026 | 04/12/2026 | 07/12/2026 | 17/03/2027 |
| P3 | 27/11/2026 | 27/11/2026 | 30/11/2026 | 11/12/2026 | 14/12/2026 | 24/03/2027 |
| P4 | 04/12/2026 | 04/12/2026 | 07/12/2026 | 18/12/2026 | 21/12/2026 | 31/03/2027 |
| P5 | 11/12/2026 | **27/11/2026** | 14/12/2026 | 12/01/2027 | 13/01/2027 | 07/04/2027 |
| P6 | 18/12/2026 | **27/11/2026** | 21/12/2026 | 19/01/2027 | 20/01/2027 | 14/04/2027 |
| P7 | 12/01/2027 | 11/12/2026 | 13/01/2027 | 26/01/2027 | 27/01/2027 | 21/04/2027 |
| P8 | 19/01/2027 | 18/12/2026 | 20/01/2027 | 02/02/2027 | 03/02/2027 | 28/04/2027 |

- P9 / quincho y azotea: 30/11/2026–29/06/2027; inicio sujeto a liberación de Dirección de Obra.
- Medianeras: 02/12/2026–19/02/2027; compromiso al 20/02/2027 (sábado).
- PB: ejecución y puesta a punto 10/02/2027–01/07/2027; entrega ligada al cierre general del 13/10/2027.
- Comunes y ascensor: 18/06/2027–13/10/2027.
- Hormigonado de azotea y sala de máquinas: 16/11/2026; no equivale a liberación del frente.

Las fechas de contrapiso son hitos de liberación de duración cero, no la duración física del bombeo. El PDF marca los de P5/P6 como obligatorios, y otros como propuestos; ambas condiciones se conservan en las observaciones de la app.

## Calendario

Lunes a viernes, con **cierre del 24/12/2026 al 10/01/2027 inclusive**. Reinicio el **11/01/2027**. Se excluyen 12 días laborables; otros feriados no se descuentan.

El avance esperado se interpola sobre los días efectivos de cada actividad. Durante el cierre permanece constante; no penaliza el período de vacaciones como atraso por sí mismo. Los hitos se exigen desde su fecha. Las actividades archivadas de R1 conservan su calendario original y no intervienen en los indicadores activos.

## Vínculos, holguras y supuestos

La app muestra las predecesoras FS/SS, la HT y la criticidad **tal como aparecen en el PDF**, sin recalcularlas. Los vínculos del documento son reconstruidos, no extraídos de un archivo MS Project nativo. Sus 58 actividades “Crítica modelo” no se convierten automáticamente en semáforo rojo: el atraso se calcula con avances reales.

La HT es holgura hasta el cierre general y no autoriza a incumplir contrapisos del 27/11 ni medianeras del 20/02. ET3 dura 10 días y empieza un piso cada 5, por lo que exige dos frentes o capacidad equivalente. Se conservan las condiciones de liberación, pruebas, suministros y ascensor; la entrega de un sector no acredita habilitación. No se inventan duraciones para trámites o conexiones no informadas.

## Conservación de registros y alcance

La actualización mantiene **501 registros internos**: 491 IDs originales y 10 nuevos. De ellos, **395 integran el plan activo** y **106 quedan fuera del alcance activo R2**, con el tratamiento indicado en la sección de trazabilidad del PDF. Las actividades productivas anteriores se pueden abrir desde **Programación → Historial fuera de R2**. Los 106 incluyen también resúmenes y contrataciones que no formaban parte de los indicadores de producción.

Los IDs internos anteriores se mantienen. H16, LIB y L1–L8 usan IDs internos numéricos nuevos, separados de los originales, y muestran el ID del PDF en pantalla. La clave local `jujuy-control-v1` y el identificador interno de proyecto `jujuy-a0` se conservan para compatibilidad. La restauración valida tanto IDs activos como archivados.

**No se borran, desplazan ni transfieren partes o restricciones privados.** Los de tareas archivadas se conservan para consulta/edición y respaldo, pero se excluyen del semáforo activo. Los hitos L1–L8 agrupan instalaciones iniciales P1–P8 sin saldo real informado; no reciben automáticamente porcentajes de sus tareas antiguas. ET1 ejecutada hasta P8 al 10/10/2026 figura como observación del documento, sin inventar fechas reales por piso.

### Antecedente de bombeos P3/P4

R1 incluía bombeos confirmados el 30/10/2026. El PDF R2 programa **“Contrapiso terminado” P3 el 27/11/2026 y P4 el 04/12/2026**. El antecedente del bombeo se conserva en `previousConfirmedReport` y en el detalle de actividad, sin usarlo para completar automáticamente el alcance revisado de R2. Los partes manuales de cualquier fecha, incluidos los de esos IDs, permanecen intactos y siguen siendo editables por su propietario. No se modifica un parte real por un cambio de programación.

## Históricos y reproducción

- A0: `data/schedule-a0.json`, `docs/programacion-a0.csv`, `docs/PROGRAMACION-A0.md` y los nueve PDF originales.
- R1: `data/schedule-r1.json`, `docs/programacion-r1.csv`, `docs/PROGRAMACION-R1.md`.
- R2 vigente: `data/schedule.json`, `docs/programacion.csv` y el PDF revisado.
- `scripts/import_r2.py` importa el PDF y realiza las comprobaciones de integridad. Ejecutarlo nuevamente produce exactamente el mismo resultado y no vuelve a desplazar fechas. No ejecutar el generador R1 para actualizar un plan R2.

## Actualización y uso

Abrir la app con conexión y aceptar “Actualizar app” después de guardar formularios abiertos. No borrar datos del sitio para actualizar. La caché R2 permite consultar y editar partes offline tras la primera carga completa; los PDF no se precargan, por lo que deben descargarse previamente si se necesitan sin conexión. No hay sincronización con monday ni entre dispositivos; el respaldo JSON sigue siendo el mecanismo de traslado de datos.
