# Oddino Arquitectura · Control de obra Jujuy

Aplicación web adaptable a celular, tableta y escritorio, con identidad de Oddino Arquitectura. Portada visual con semáforos grandes, atención priorizada, cobertura de partes y tarjetas de rubros. Los filtros y las referencias del plan se despliegan bajo “Filtros y referencia del plan”. Semáforo por rubro, carga manual de avances por actividad/nivel, seguimiento histórico de restricciones y programación documental trazable a los nueve PDF.

## Programación vigente R3 y compromisos LPS

Leer [criterios y resultados](docs/PROGRAMACION.md). R3 recalcula la red de 395 actividades de R2 por el **09/11/2026 no laborable**, confirmado por el usuario. Antes del ajuste el motor reproduce exactamente todas las fechas, índices y holguras R2. Plan remanente **10/11/2026–14/10/2027**, conservando duraciones, vínculos FS/SS, lag SS+2 y compromisos fijos. Se mantienen vacaciones 24/12/2026–10/01/2027. Contrapisos P5/P6: 27/11/2026; medianeras: 19/02/2027.

La vista **LPS** muestra 20 compromisos de noviembre, todavía sin cumplimiento ni PPC calculable. Correcciones confirmadas: ET1 hasta P8 fin previsto 10/11; SH+T sala de máquinas y tanques; SAN-02 inspección ocular de gas. Las lecturas pendientes se señalan y las fotos originales no se publican.

A0, R1 y R2 se conservan aparte. Los 501 IDs internos y los partes/restricciones locales permanecen compatibles. Las 106 filas no activas incluyen 68 actividades productivas anteriores consultables desde Programación → Historial fuera del plan. No se transfieren porcentajes a los hitos nuevos ni se toman promesas LPS como ejecución. [CSV vigente](docs/programacion.csv) · [Gantt R3 PDF](docs/Jujuy_Programacion_R3_LPS.pdf).

## Iniciar en el entorno

Requiere Python 3.10+; Node.js 20+ sólo para las pruebas. No hay paquetes externos ni instalación de dependencias para ejecutar la aplicación.

```sh
cd /workspace/Programacion-Jujuy
python3 scripts/serve.py
```

El servidor de desarrollo escucha sólo dentro del equipo, en 127.0.0.1, puerto 8000 (o `PORT`). Mantener el proceso activo para la sesión de pruebas. No ejecutar abriendo `index.html` directamente, porque el navegador necesita cargar módulos y JSON por HTTP.

```sh
cd /workspace/Programacion-Jujuy
npm test
```

Dieciséis pruebas del cálculo, históricos, calendarios R2/R3, red de dependencias, compromisos LPS y conservación de partes. Las pruebas de navegador están en `tests/browser_smoke.py`, `tests/home_smoke.py` (portada visual), `tests/lps_smoke.py` (promesas y filtros semanales) y `tests/update_smoke.py` (actualización conservando partes): requieren Python Playwright y Chromium ya instalados, servidor activo y permiso de acceso a loopback. Ejecutar `python3 tests/browser_smoke.py`; opcionalmente indicar `JUJUY_TEST_URL`, `CHROMIUM_PATH` y `JUJUY_TEST_ARTIFACTS`. Usan perfiles temporales y no modifican partes de usuarios reales.

## Usar el tablero

1. Seleccionar fecha de corte, nivel, rubro y, opcionalmente, próximas tres semanas.
2. En Programación, abrir una actividad. Registrar porcentaje acumulado, fecha, responsable y observación. Un parte por fecha; editar la misma fecha pide confirmar el reemplazo.
3. Registrar restricciones con causa, categoría, responsable y fecha compromiso. Resolver con su fecha real; el historial sigue disponible.
4. Exportar un respaldo JSON periódicamente. Restaurarlo permite trasladar el seguimiento a otro dispositivo, reemplazando la información local con confirmación. El CSV de corte sirve para informes, no para restauración.

**Verde:** parte al nivel del plan. **Rojo:** avance menor al esperado. **Ámbar:** restricción vigente. **Gris:** sin parte o programado. Sin parte no equivale a cero avance. El 9/11 no laborable y las vacaciones no generan avance esperado. La prioridad por rubro es restricción, atraso, sin parte, en plan, programado. El promedio se pondera por duración, no por costo ni cantidades físicas.

## Celular y tableta

La interfaz se verificó con Chromium en anchos de 320, 390, 768 y 1440 px. Para abrirla desde un teléfono físico e instalarla en pantalla de inicio, es necesario alojar los archivos estáticos en un sitio **HTTPS** accesible al dispositivo. La aplicación se aloja en https://marcelomusumeci-spec.github.io/Programacion-Jujuy/ con autorización del usuario.

Una vez alojada, abrir el sitio desde el dispositivo y usar «Instalar aplicación» o «Añadir a pantalla de inicio». Después de la primera carga completa, la aplicación y el plan quedan disponibles offline mediante service worker. Los PDF originales no se precargan: descargarlos antes si se necesitan sin conexión. Una actualización que modifique archivos de la aplicación debe cambiar el identificador `CACHE` de `sw.js`.

## Almacenamiento y límites

Los partes y restricciones permanecen en el navegador/dispositivo, mediante `localStorage`. No hay cuentas ni sincronización entre celular y tableta. Borrar los datos del sitio o usar navegación privada puede perder el seguimiento. La copia JSON es el mecanismo de resguardo y traslado; no se deben mezclar dos copias como si hubiera sincronización.

Agregar restricciones en la interfaz no recalcula automáticamente la red. R3 se generó mediante un cálculo explícito de los vínculos del PDF R2 y de las exclusiones confirmadas; no se inventan productividad ni feriados adicionales. Las fichas son referencia de aceptación y no equivalen automáticamente a los números de etapa del cronograma. Revisar las observaciones de `docs/PROGRAMACION.md` con la jefatura antes de adoptar el plan.

## Archivos

- `index.html`, `app.js`, `styles.css`: interfaz.
- `assets/oddino-logo.svg`: logo original de la web oficial; fuente documentada en `assets/README.md`.
- `model.js`: calendario, cortes históricos, semáforo, validación y exportación.
- `data/schedule.json`: plan R3, calendario, IDs activos/archivados, red, fechas R2 de comparación y compromisos LPS.
- `data/schedule-r2.json`: base R2 intacta.
- `data/lps-noviembre-2026.json`: transcripción LPS confirmada y lecturas pendientes.
- `scripts/replan_lps.py`: motor R3 y generación del PDF (ReportLab + DejaVu Sans, sólo para regenerar).
- `data/schedule-r1.json`: histórico R1 inalterado.
- `scripts/import_r2.py`: importador histórico R2; no usar para actualizar directamente R3.
- `data/schedule-a0.json`: plan A0 inalterado.
- `scripts/reprogram.py`: generador histórico de R1; no usar para actualizar R2.
- `docs/`: PDF originales, programación y CSV.
- `manifest.webmanifest`, `sw.js`, `icon-*`: aplicación instalable y caché offline.

Los procesos en ejecución no sobreviven necesariamente a una nueva tarea. Usar el checkout existente: cada tarea cloud ya está aislada; no crear un worktree salvo pedido explícito.
