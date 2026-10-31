# Jujuy · Control de obra

Aplicación web adaptable a celular, tableta y escritorio. Semáforo por rubro, carga manual de avances por actividad/nivel, seguimiento histórico de restricciones y programación documental trazable a los nueve PDF.

## Programación primero

Leer [la programación y sus supuestos](docs/PROGRAMACION.md). Se transcribieron 491 registros de Niveles A0, con 453 actividades/hitos de producción. Inicio 24/08/2026, fin 27/01/2028. Se cotejaron 473 registros con Curva A0. La diferencia de fechas del ID 391 y las diferencias de etapas entre fichas están documentadas. [CSV completo](docs/programacion.csv).

No se inventaron partes reales, responsables, restricciones ni fechas de reprogramación. El usuario eligió cargar el seguimiento manualmente.

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

Ocho pruebas del cálculo y la integridad del plan. Las pruebas de navegador están en `tests/browser_smoke.py`: requieren Python Playwright y Chromium ya instalados, servidor activo y permiso de acceso a loopback. Ejecutar `python3 tests/browser_smoke.py`; opcionalmente indicar `JUJUY_TEST_URL`, `CHROMIUM_PATH` y `JUJUY_TEST_ARTIFACTS`. Usan perfiles temporales y no modifican partes de usuarios reales.

## Usar el tablero

1. Seleccionar fecha de corte, nivel, rubro y, opcionalmente, próximas tres semanas.
2. En Programación, abrir una actividad. Registrar porcentaje acumulado, fecha, responsable y observación. Un parte por fecha; editar la misma fecha pide confirmar el reemplazo.
3. Registrar restricciones con causa, categoría, responsable y fecha compromiso. Resolver con su fecha real; el historial sigue disponible.
4. Exportar un respaldo JSON periódicamente. Restaurarlo permite trasladar el seguimiento a otro dispositivo, reemplazando la información local con confirmación. El CSV de corte sirve para informes, no para restauración.

**Verde:** parte al nivel del plan. **Rojo:** avance menor al esperado. **Ámbar:** restricción vigente. **Gris:** sin parte o programado. Sin parte no equivale a cero avance. La prioridad por rubro es restricción, atraso, sin parte, en plan, programado. El promedio se pondera por duración, no por costo ni cantidades físicas.

## Celular y tableta

La interfaz se verificó con Chromium en anchos de 320, 390, 768 y 1440 px. Para abrirla desde un teléfono físico e instalarla en pantalla de inicio, es necesario alojar los archivos estáticos en un sitio **HTTPS** accesible al dispositivo. Este trabajo no despliega, publica ni hace push a GitHub.

Una vez alojada, abrir el sitio desde el dispositivo y usar «Instalar aplicación» o «Añadir a pantalla de inicio». Después de la primera carga completa, la aplicación y el plan quedan disponibles offline mediante service worker. Los PDF originales no se precargan: descargarlos antes si se necesitan sin conexión. Una actualización que modifique archivos de la aplicación debe cambiar el identificador `CACHE` de `sw.js`.

## Almacenamiento y límites

Los partes y restricciones permanecen en el navegador/dispositivo, mediante `localStorage`. No hay cuentas ni sincronización entre celular y tableta. Borrar los datos del sitio o usar navegación privada puede perder el seguimiento. La copia JSON es el mecanismo de resguardo y traslado; no se deben mezclar dos copias como si hubiera sincronización.

No se calculan automáticamente predecesoras, ruta crítica, feriados, productividad ni impacto de restricciones en fechas. Las fichas son referencia de aceptación y no equivalen automáticamente a los números de etapa del cronograma. Revisar las observaciones de `docs/PROGRAMACION.md` con la jefatura antes de adoptar el plan.

## Archivos

- `index.html`, `app.js`, `styles.css`: interfaz.
- `model.js`: calendario, cortes históricos, semáforo, validación y exportación.
- `data/schedule.json`: plan, fuente/página por ID, discrepancias, textos de fichas y huellas de originales.
- `docs/`: PDF originales, programación y CSV.
- `manifest.webmanifest`, `sw.js`, `icon-*`: aplicación instalable y caché offline.

Los procesos en ejecución no sobreviven necesariamente a una nueva tarea. Usar el checkout existente: cada tarea cloud ya está aislada; no crear un worktree salvo pedido explícito.
