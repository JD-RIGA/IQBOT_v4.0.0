# iqbot — Documentación

Este repositorio contiene un bot/GUI para IQ Option con:
- Interfaz gráfica para **login**, panel de control, y acciones rápidas.
- Módulos `core/` para clics externos, indicadores, conexión a IQ, recuperación de pérdidas, logs, persistencia y plugins.
- Datos persistentes en `data/`.
- Scripts de instalación y empaquetado para Windows.

## Puntos clave
- **app.py**: arranque de la app (clase `App`), encola frames de `ui/` y puentea con `core/`.
- **ui/**: ventanas (`LoginFrame`, `PanelFrame`) y widgets.
- **core/**: lógica de negocio (indicadores, IQ helpers, recuperación, etc.).
- **tools/**: utilidades y ejemplo de plugin/herramienta.
- **requirements.txt**: dependencias.
- **.bat**: scripts para instalar y ejecutar en Windows.

Consulta los archivos de `docs/` para guías detalladas:
- [`docs/arquitectura.md`](arquitectura.md)
- [`docs/instalacion_uso.md`](instalacion_uso.md)
- [`docs/configuracion.md`](configuracion.md)
- [`docs/modulos.md`](modulos.md)
- [`docs/ui.md`](ui.md)
- [`docs/paquetes_y_build.md`](paquetes_y_build.md)
- [`docs/solucion_problemas.md`](solucion_problemas.md)
- [`docs/faq.md`](faq.md)
- [`docs/plantilla_changelog.md`](plantilla_changelog.md)
- [`docs/contribuir.md`](contribuir.md)
