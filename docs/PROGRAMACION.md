# Programación vigente R3 · Ajuste por reunión LPS

## Confirmaciones del usuario

- Las cuatro semanas fotografiadas son de noviembre de 2026 y sus tarjetas son compromisos planificados, sin cumplimiento confirmado.
- El 09/11/2026 se considera no laborable y el usuario pidió reprogramar las tareas afectadas.
- El fin previsto de ET1 hasta P8 es 10/11/2026: se corrige la referencia 10/10 de R2. No se da por realizada una actividad por corregir la fecha de una promesa.
- SH+T refiere a sala de máquinas y tanques; la tarjeta H. SH+T se transcribe como hormigón de sala de máquinas y tanques.
- SAN-02 del 18/11 es inspección ocular de instalación de gas. Se mantiene el código original y se aclara su clasificación de alcance; no se atribuye un responsable personal ni cumplimiento.
- RDC y otras lecturas parciales permanecen señaladas para revisión. No se expanden por inferencia.

## Resultado de reprogramación

**Programación remanente: 10/11/2026–14/10/2027.** La fecha de inicio no es una declaración del inicio histórico de obra. El cierre se mueve un día laborable respecto de R2.

Se mantienen las 395 actividades/hitos activos, las duraciones y todos los vínculos FS/SS del modelo R2, incluido el lag SS+2. El 09/11 se agrega como exclusión del calendario, junto a vacaciones 24/12/2026–10/01/2027 inclusive; otros feriados no se descuentan.

Antes de aplicar el cambio, el motor reproduce exactamente los seis campos calculados de cada una de las 395 filas de R2: índices de inicio y fin, fechas de inicio y fin, inicio tardío y holgura. Luego realiza pase hacia delante y hacia atrás con el nuevo calendario. Cambian las fechas de **372 actividades**; las independientes y ancladas no se desplazan indiscriminadamente. Permanecen **58 actividades con HT cero** en la red recalculada. Criticidad de red no equivale a atraso real ni estado rojo de ejecución.

| Referencia | Fin R2 | Fin R3 |
|---|---|---|
| ET2 P1 | 13/11/2026 | 16/11/2026 |
| ET2 P8 | 19/01/2027 | 20/01/2027 |
| Contrapiso P5 | 27/11/2026 | 27/11/2026 |
| Contrapiso P6 | 27/11/2026 | 27/11/2026 |
| Medianera Norte | 19/02/2027 | 19/02/2027 |
| Hormigón sala máquinas / azotea | 16/11/2026 | 16/11/2026 |
| Liberación P9 | 30/11/2026 | 30/11/2026 |
| Entrega general | 13/10/2027 | 14/10/2027 |

El hito H16 y la liberación LIB mantienen sus fechas; la liberación P9 continúa siendo un supuesto a verificar con Dirección de Obra y no un plazo técnico de curado. Las fechas mínimas del resto de hitos de liberación se conservan según la red R2. El modelo no incorpora nuevas dependencias a partir de lecturas parciales de tarjetas LPS.

Los contrapisos obligatorios P5/P6 siguen el **27/11/2026**. Medianera Norte conserva fin **19/02/2027**, dentro del límite 20/02. La holgura global no autoriza a incumplir estos compromisos. Las cadencias y solapes siguen exigiendo la capacidad de cuadrillas prevista en R2; no se inventan recursos ni se comprimen duraciones.

## Vista LPS

Se incorpora una vista separada con **20 compromisos**, distribuidos en cuatro semanas (3, 9, 4 y 4 tarjetas), con fecha, código de origen, rubro, piso y observaciones. Son datos compartidos de planificación: no se insertan como partes reales privados ni completan tareas del semáforo. Los colores de origen identifican rubros/actores, no atrasos o restricciones.

**PPC pendiente:** no hay cumplimiento individual confirmado. El panel de completadas vacío en la foto no demuestra 0% de cumplimiento. No se calcula ni muestra PPC cero. Las tarjetas “Fin” son compromisos de fin, no evidencia de haber terminado.

Las fotografías originales no se publican. Se usa una transcripción con referencias “Foto 1”, etc. Las lecturas dudosas siguen marcadas, incluidas RDC, parte de la compra de caños y los alcances de ladrillos/vistos/Med. PB-Este. Las metas LPS del 14/11 y 28/11 caen en sábado: se conservan sus fechas, sin habilitar automáticamente sábados en la red L-V del Gantt; el trabajo efectivo en esos días queda por confirmar. Los códigos LPS no se equiparan automáticamente con las etapas del Gantt. La tarjeta de premarcos, por ejemplo, no certifica toda ET2.

## Conservación de avances e históricos

Se mantienen 501 registros internos, con los mismos IDs activos y archivados que R2. La clave local `jujuy-control-v1`, el proyecto interno `jujuy-a0`, los partes, sus fechas y las restricciones privadas no cambian. Los compromisos LPS no se transfieren a porcentajes de ejecución. Los respaldos anteriores siguen siendo compatibles.

- A0 y R1 originales, sin cambios, en sus archivos históricos.
- R2: `data/schedule-r2.json`, `docs/programacion-r2.csv`, `docs/PROGRAMACION-R2.md` y su PDF original de 40 páginas.
- R3: `data/schedule.json`, `docs/programacion.csv` y `docs/Jujuy_Programacion_R3_LPS.pdf`.
- Transcripción confirmada LPS: `data/lps-noviembre-2026.json`, también incluida en el JSON del plan para uso offline; CSV descargable en `docs/compromisos-lps-noviembre-2026.csv`.

Cada tarea activa conserva `r2Plan`, las holguras originales del PDF y el vínculo a la página de R2. Las fechas R3 y su holgura recalculada se distinguen de esos datos de origen. Los antecedentes de bombeo P3/P4 del 30/10 permanecen como en R2, sin completar automáticamente el nuevo alcance de contrapiso terminado.

## Regeneración y validación

Desde el repositorio, `python3 scripts/replan_lps.py` reconstruye R3 desde `data/schedule-r2.json` y la transcripción LPS, verifica el modelo base y produce los archivos vigentes. No acumula desplazamientos. Para generar el PDF usa ReportLab y la fuente DejaVu Sans; no son dependencias de ejecución de la aplicación estática. El CSV de compromisos contiene la transcripción, sin datos privados de partes.

El script verifica ausencia de ciclos, existencia de predecesoras, lags FS/SS, duraciones, holguras no negativas y preservación de anclas obligatorias. Los datos, el CSV y el PDF generado son reproducibles byte por byte.

La aplicación mantiene su semáforo por avance real frente al esperado según el calendario R3. La actualización se probó desde una instalación antigua, preservando partes de actividades archivadas, y en uso offline. Abrir con conexión y pulsar “Actualizar app” después de guardar formularios; no borrar datos del sitio. Los PDF no se precargan y deben descargarse previamente para consulta offline. No hay sincronización con monday ni entre dispositivos.
