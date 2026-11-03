# Reprogramación R1 · Obra Jujuy

## Referencia real confirmada

El comitente confirmó expresamente que **los bombeos de contrapisos de los pisos 3 y 4 se realizaron ambos el 30/10/2026**. Los hitos ID 135 (N3-BOMBEO_) y 181 (N4-BOMBEO_) quedan en esa fecha y con 100% de ejecución confirmado. No se certifican otras tareas ni el resto de sus tandas.

## Método y alcance

Se conservan las 491 filas, sus IDs, niveles, rubros, alcances, duraciones y fuentes. La A0 no se altera: `data/schedule-a0.json`, `programacion-a0.csv`, `PROGRAMACION-A0.md` y los nueve PDF conservan los valores originales.

- **Referencia general N3:** del 26/05/2027 al 30/10/2026. Todas las fechas anteriores y posteriores se adelantan **148 días laborables**, salvo la secuencia N4 indicada abajo.
- **Secuencia propia N4:** su bombeo original era el 07/07/2027. Para llevarlo también al 30/10/2026 se adelanta su secuencia de albañilería, instalaciones y terminaciones (IDs 173–213, más resumen ID 172) **178 días laborables**. Así se mantienen los intervalos de esa secuencia anteriores y posteriores al bombeo sin comprimir duraciones. La estructura N4 conserva el desplazamiento general para mantener el orden constructivo N1 → N8; queda finalizada el 26/06/2026, antes del inicio del frente N4 el 20/07/2026.
- Calendario lunes–viernes, sin feriados, igual al supuesto de control de la aplicación. Las fechas se desplazan en días laborables y no en días corridos, para evitar colocar trabajos en fines de semana y alterar su duración laborable.
- Los hitos de contratación, estructura, espacios comunes, medianeras y otros niveles reciben el desplazamiento general. No se afirma que esos hitos ya se hayan cumplido.
- Hito de coordinación ID 170 «Bombeos N4-5-6»: se alinea a N4 (30/10/2026), como referencia de arranque de esa tanda; **no acredita que N5 y N6 estén bombeados**. El hito ID 169 mantiene su relación con el arranque N1 de su tanda. Los hitos por nivel conservan sus propias fechas.
- El resumen de bombeos ID 168 abarca desde el primer hasta el último bombeo individual reprogramado. Su duración original se conserva como dato documental; no se interpreta como suma de jornadas productivas.

Esta es una reprogramación por desplazamiento con dos anclas, **no un cálculo de red CPM**: los PDF no contienen la tabla de predecesoras, holguras, cuadrillas ni recursos. La coherencia interna de cada frente se conserva, pero la jefatura debe validar las relaciones entre frentes y la disponibilidad de cuadrillas. Por ejemplo, para conservar su secuencia y coincidir en el bombeo, N4 comienza sus actividades antes que N3; no se ha supuesto una cuadrilla compartida.

## Fechas resultantes

**Inicio del plan desplazado: 28/01/2026. Fin del plan desplazado: 05/07/2027.** Son fechas resultantes del desplazamiento solicitado, no fechas reales acreditadas ni un nuevo compromiso contractual.

| Frente | Inicio R1 | Fin/entrega R1 |
|---|---|---|
| NIVEL 1 | 10/08/2026 | 11/01/2027 |
| NIVEL 2 | 17/08/2026 | 18/01/2027 |
| NIVEL 3 | 24/08/2026 | 25/01/2027 |
| NIVEL 4 | 20/07/2026 | 25/01/2027 |
| NIVEL 5 | 07/09/2026 | 08/02/2027 |
| NIVEL 6 | 14/09/2026 | 15/02/2027 |
| NIVEL 7 | 21/09/2026 | 03/05/2027 |
| NIVEL 8 | 28/09/2026 | 01/03/2027 |
| AZOTEA | 05/10/2026 | 19/03/2027 |
| PALIER & ESCALERAS | 10/03/2027 | 05/07/2027 |
| MEDIANERAS | 16/11/2026 | 18/01/2027 |
| PLANTA BAJA | 16/11/2026 | 05/07/2027 |

El CSV `programacion.csv` incluye por ID inicio/fin R1, inicio/fin A0, desplazamiento laborable y duración documental. `scripts/reprogram.py` regenera R1 siempre desde la A0 original: ejecutarlo nuevamente no vuelve a adelantar fechas.

## Conservación del seguimiento

Los partes y restricciones guardados por cada usuario permanecen intactos, con sus fechas reales, responsables y notas. No se desplazan fechas de partes, altas, compromisos ni resoluciones de restricciones. Al conservar el identificador de tarea y la clave de almacenamiento, los respaldos anteriores siguen siendo compatibles.

Los dos hitos confirmados se incorporan como referencia de ejecución al plan compartido, no escribiendo ni reemplazando partes privados. Sólo aparecen al consultar cortes desde el 30/10/2026. Un parte local para la misma actividad y fecha tiene prioridad; un parte posterior también se respeta. Los detalles indican su confirmación por separado del historial local.

El resto de tareas sin parte seguirá figurando **Sin parte** aunque su nueva fecha de fin sea anterior al corte. No se presume un 100% de ejecución de las precedentes por haberse ejecutado el bombeo.

## Criterios del semáforo

Avance esperado interpolado por días lunes–viernes inclusivos entre inicio y fin R1, sin feriados; hitos al 100% desde su fecha. El promedio se pondera por duración documental (hitos con peso 1); no es avance económico certificado. Se usa el último parte con fecha menor o igual al corte.

- Verde: avance conocido igual o superior al esperado; al 100%, Completado.
- Rojo: avance conocido menor al esperado, con tolerancia de 0,5 puntos por redondeo.
- Ámbar: restricción vigente al corte, con prioridad sobre el atraso.
- Gris: sin parte o programado para el futuro. La ausencia de información no equivale a cero avance.

## Observaciones originales que permanecen

- ID 391: Niveles A0 indica 14–16/06/2027, 3 días, y Curva A0 16–17/06/2027, 2 días. R1 adopta las fechas de Niveles y las desplaza. La discrepancia original se conserva, sin mezclarla con el cambio R1.
- Las etapas no tienen equivalencias automáticas entre fichas y cronograma, especialmente electricidad, gas y espacios comunes.
- Los checklist anteriores a limpieza y terminaciones requieren verificación final antes de entrega; la separación temporal de PB entre puesta a punto y entrega se mantiene.
- ID 395 de azotea sigue requiriendo desarrollar su alcance según proyecto.

Ver `PROGRAMACION-A0.md` para la revisión documental completa y las fichas de origen. No se editan los PDF para hacerlos pasar por documentos R1.

## Actualización de la aplicación

R1 actualiza las fechas visibles, el CSV de programación, el plan esperado y la caché offline. Al recibir una actualización aparece la opción «Actualizar R1»; guardar los partes abiertos antes de pulsarla. Si se mantiene una pestaña antigua, cerrar y volver a abrir la aplicación con conexión para recibir la revisión. Nunca borrar datos del sitio para actualizar: eso eliminaría los partes locales.
