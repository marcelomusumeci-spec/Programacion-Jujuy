# Oddino Arquitectura · Control de obra Jujuy

Aplicación web adaptable a celular, tableta y escritorio, con identidad de Oddino Arquitectura. Portada visual con semáforos grandes, atención priorizada, cobertura de partes y tarjetas de rubros. Los filtros y las referencias del plan se despliegan bajo “Filtros y referencia del plan”. Semáforo por rubro, carga manual de avances por actividad/nivel, seguimiento histórico de restricciones y programación documental trazable a los nueve PDF.

## Programación vigente R2

Leer [la programación y sus criterios](docs/PROGRAMACION.md). El PDF `Jujuy_Programacion_completa_revisada.pdf` es la fuente vigente: 395 actividades e hitos, desde el 09/11/2026 al 13/10/2027. El calendario excluye vacaciones del 24/12/2026 al 10/01/2027 inclusive, con reinicio el 11/01. Otros feriados no se descuentan.

Se conservan A0 y R1 por separado. Los 491 IDs originales permanecen y se agregan diez IDs nuevos para H16, LIB y L1–L8. Las 106 filas no activas se conservan con su trazabilidad; las actividades productivas anteriores se consultan desde Programación → Historial fuera de R2. Los partes y restricciones locales no se borran ni se transfieren automáticamente a los nuevos hitos agregados.

El antecedente de bombeo P3/P4 del 30/10/2026 se conserva por separado: no completa automáticamente los hitos de contrapiso terminado que R2 programa para 27/11 y 04/12. Las condiciones y supuestos del PDF continúan visibles. [CSV vigente](docs/programacion.csv).

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

Trece pruebas del cálculo, históricos, calendario R2, integridad del plan y conservación de partes. Las pruebas de navegador están en `tests/browser_smoke.py`, `tests/home_smoke.py` (portada visual) y `tests/update_smoke.py` (actualización conservando partes): requieren Python Playwright y Chromium ya instalados, servidor activo y permiso de acceso a loopback. Ejecutar `python3 tests/browser_smoke.py`; opcionalmente indicar `JUJUY_TEST_URL`, `CHROMIUM_PATH` y `JUJUY_TEST_ARTIFACTS`. Usan perfiles temporales y no modifican partes de usuarios reales.

## Usar el tablero

1. Seleccionar fecha de corte, nivel, rubro y, opcionalmente, próximas tres semanas.
2. En Programación, abrir una actividad. Registrar porcentaje acumulado, fecha, responsable y observación. Un parte por fecha; editar la misma fecha pide confirmar el reemplazo.
3. Registrar restricciones con causa, categoría, responsable y fecha compromiso. Resolver con su fecha real; el historial sigue disponible.
4. Exportar un respaldo JSON periódicamente. Restaurarlo permite trasladar el seguimiento a otro dispositivo, reemplazando la información local con confirmación. El CSV de corte sirve para informes, no para restauración.

**Verde:** parte al nivel del plan. **Rojo:** avance menor al esperado. **Ámbar:** restricción vigente. **Gris:** sin parte o programado. Sin parte no equivale a cero avance. Las vacaciones de R2 no generan avance esperado. La prioridad por rubro es restricción, atraso, sin parte, en plan, programado. El promedio se pondera por duración, no por costo ni cantidades físicas.

## Celular y tableta

La interfaz se verificó con Chromium en anchos de 320, 390, 768 y 1440 px. Para abrirla desde un teléfono físico e instalarla en pantalla de inicio, es necesario alojar los archivos estáticos en un sitio **HTTPS** accesible al dispositivo. La aplicación se aloja en https://marcelomusumeci-spec.github.io/Programacion-Jujuy/ con autorización del usuario.

Una vez alojada, abrir el sitio desde el dispositivo y usar «Instalar aplicación» o «Añadir a pantalla de inicio». Después de la primera carga completa, la aplicación y el plan quedan disponibles offline mediante service worker. Los PDF originales no se precargan: descargarlos antes si se necesitan sin conexión. Una actualización que modifique archivos de la aplicación debe cambiar el identificador `CACHE` de `sw.js`.

## Almacenamiento y límites

Los partes y restricciones permanecen en el navegador/dispositivo, mediante `localStorage`. No hay cuentas ni sincronización entre celular y tableta. Borrar los datos del sitio o usar navegación privada puede perder el seguimiento. La copia JSON es el mecanismo de resguardo y traslado; no se deben mezclar dos copias como si hubiera sincronización.

No se calculan automáticamente predecesoras, ruta crítica, feriados, productividad ni impacto de restricciones en fechas. Las fichas son referencia de aceptación y no equivalen automáticamente a los números de etapa del cronograma. Revisar las observaciones de `docs/PROGRAMACION.md` con la jefatura antes de adoptar el plan.

## Archivos

- `index.html`, `app.js`, `styles.css`: interfaz.
- `assets/oddino-logo.svg`: logo original de la web oficial; fuente documentada en `assets/README.md`.
- `model.js`: calendario, cortes históricos, semáforo, validación y exportación.
- `data/schedule.json`: plan R2, calendario, IDs activos y archivados, vínculos y páginas de fuente.
- `data/schedule-r1.json`: histórico R1 inalterado.
- `scripts/import_r2.py`: importación repetible del PDF R2, con cotejo y validación de duraciones.
- `data/schedule-a0.json`: plan A0 inalterado.
- `scripts/reprogram.py`: generador histórico de R1; no usar para actualizar R2.
- `docs/`: PDF originales, programación y CSV.
- `manifest.webmanifest`, `sw.js`, `icon-*`: aplicación instalable y caché offline.

Los procesos en ejecución no sobreviven necesariamente a una nueva tarea. Usar el checkout existente: cada tarea cloud ya está aislada; no crear un worktree salvo pedido explícito.
