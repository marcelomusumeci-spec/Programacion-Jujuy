# Programación de control · Obra Jujuy

Programación documental para revisión de la jefatura de obra. Se conserva el plan de los PDF; no constituye una reprogramación aprobada ni acredita avance real.

## Base y alcance

Se transcribieron las **491 filas (ID 0–490)** de «260831_112_JUJUY_PG - LB - Niveles A0.pdf»: 453 actividades/hitos de obra, 21 hitos de contratación y 17 resúmenes. Los 473 registros fechados extraídos de «Curva A0» se cotejaron por ID, inicio, fin y duración. Los siete documentos de instancias productivas se incorporan para consulta de alcance y aceptación. Los originales están en esta carpeta, con sus huellas SHA-256 en `data/schedule.json`.

El plan de control usa las columnas **Comienzo y Fin del documento Niveles**, sin desplazar fechas al día actual. Se retienen por separado duración, duración de línea base y variación de fin del PDF. No se reconstruyen fechas originales de línea base a partir de esas duraciones. La variación negativa del PDF representa una diferencia entre planes, no un atraso real de obra.

Inicio general: **24/08/2026**. Fin general: **27/01/2028**. Estructura hasta **19/05/2027**. Arranque de albañilería N1: **04/03/2027** (hito previo 03/03/2027). Contrataciones: 24/08/2026–30/04/2027, consultables por separado y excluidas de los indicadores de producción.

## Frentes y entregas documentales

| Frente | Inicio | Entrega/fin |
|---|---|---|
| N1 | 04/03/2027 | 05/08/2027 |
| N2 | 11/03/2027 | 12/08/2027 |
| N3 | 18/03/2027 | 19/08/2027 |
| N4 | 25/03/2027 | 30/09/2027 |
| N5 | 01/04/2027 | 02/09/2027 |
| N6 | 08/04/2027 | 09/09/2027 |
| N7 | 15/04/2027 | 25/11/2027 |
| N8 | 22/04/2027 | 23/09/2027 |
| Azotea | 29/04/2027 | 13/10/2027 |
| Medianeras | 10/06/2027 | 12/08/2027 |
| Planta baja | 10/06/2027 | 27/01/2028 |
| Palier y escaleras | 04/10/2027 | 27/01/2028 |

El escalonamiento inicial de N1–N8 es de cinco días laborables, pero el resto del plan **no se obtiene desplazando una semana cada piso**: N4 y N7 tienen interrupciones significativas. Se conservan sus fechas particulares. Las tareas y todos sus hitos se entregan en `programacion.csv` y en la vista Programación de la aplicación.

## Secuencia de coordinación propuesta (validar en obra)

1. Estructura y liberación del frente; coordinación de cañerías eléctricas embebidas.
2. Albañilería ET1 y ET2; recepción del piso por Dirección de Obra antes del ingreso de instalaciones (ficha ALB).
3. Gas, sanitaria, electricidad, agua, climatización y radiadores según las fechas de cada ID. Pruebas y aprobaciones antes de tapados.
4. Albañilería ET3, contrapisos, yesería y armados; verificar instalaciones antes del cierre.
5. Impermeabilización y prueba hidráulica; revestimientos, aberturas, pintura y equipamiento.
6. Pruebas finales, limpieza, checklist, correcciones y entrega con conformidad y documentación.

Esta secuencia es una guía de liberación. Los PDF no aportan una tabla de predecesoras ni recursos; **no se calculan ruta crítica, holguras, capacidad de cuadrillas ni nuevas fechas comprometidas**. Un bloqueo registrado no desplaza automáticamente tareas dependientes: la jefatura debe evaluar el impacto.

## Puntos a resolver antes de aprobar

- **ID 391, contrapiso de pendiente con carpeta de azotea:** Niveles indica 14–16/06/2027, 3 días; Curva indica 16–17/06/2027, 2 días. Se adopta provisionalmente Niveles y se muestra la discrepancia.
- Los números de etapa no son equivalentes entre documentos: electricidad de UF Terminaciones ubica cableado en ET3, mientras la ficha ELEC lo ubica en ET4. Gas ET3 de la ficha refiere reguladores; no se asimila automáticamente a colocación de artefactos. EC-SANIT_ET3, EC-ALB_ET6 y EC-ELEC_ET6 no tienen equivalente directo en las fichas específicas (SANIT llega a ET2, ALB a ET5, ELEC a ET5). Consultar ficha y descripción antes de certificar.
- Algunos checklist ocurren antes de la limpieza y de las últimas terminaciones (por ejemplo N1 checklist 22/07/2027 y limpieza 03–05/08/2027). Se requiere una verificación final de conformidad previa a entrega, según UF ENTREGA.
- Planta baja: puesta a punto termina 29/10/2027 y entrega está fijada para 27/01/2028. Se conserva el intervalo sin atribuirle causa.
- Azotea ID 395 exige desarrollar la programación según proyecto. No se considera que el alcance esté definido.
- No hay calendario de feriados, partes reales, ponderaciones económicas, cantidades, responsables ni restricciones vigentes. Deben validarse en obra. No se inventan.

## Método de seguimiento

Fecha de corte seleccionable. Avance esperado de una tarea = proporción de días lunes–viernes transcurridos entre inicio y fin, inclusivos (sin feriados); hitos = 100% desde su fecha. Antes de inicio = 0%. La interpolación es un supuesto operativo y no una curva certificable. El promedio general se pondera por la duración documental (hitos con peso 1), excluyendo resúmenes y contrataciones; no es avance físico/económico certificado.

Cada parte registra fecha, avance real 0–100%, responsable y nota. El corte utiliza el último parte con fecha menor o igual al corte; sin parte elegible se muestra **Sin parte**. No se interpreta falta de información como 0% ni como atraso. Se advierte cuando la fecha del último parte es anterior al corte. El progreso real global sólo se muestra cuando todas las tareas exigibles tienen parte; la cobertura se informa aparte. Las tareas futuras sin parte figuran como Programadas.

- **Verde · En plan:** parte disponible y avance real mayor o igual al esperado; una tarea al 100% figura Completada.
- **Rojo · Atrasado:** parte disponible y avance real menor al esperado (tolerancia de redondeo 0,5 puntos porcentuales).
- **Ámbar · Restringido:** existe una restricción vigente para la fecha de corte; prima sobre el atraso. Conserva visible el desvío.
- **Gris · Sin parte / Programado:** información insuficiente o trabajo futuro.

Un rubro se resume con prioridad Restringido → Atrasado → Sin parte → En plan → Programado; la falta de datos siempre aparece en su cobertura. Las restricciones tienen causa, categoría, responsable, fecha de alta, compromiso y resolución. Resolver no borra el historial. El filtro de próximas tres semanas incluye tareas en curso y las que comienzan dentro de 21 días.

## Uso y resguardo

Carga manual, confirmada por el usuario. Los datos se guardan en el navegador de cada dispositivo; no hay sincronización automática ni cuentas. Exportar una copia JSON y restaurarla permite trasladar el seguimiento. La restauración valida el formato y reemplaza los datos sólo con confirmación. Se incluye exportación CSV del corte y CSV documental completo. Instalable/offline mediante PWA al servir por HTTPS; no se ha desplegado ni publicado.
