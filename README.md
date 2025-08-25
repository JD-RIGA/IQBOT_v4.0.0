# IQBOT

Bot/GUI para **IQ Option** con interfaz en Tkinter, sistema modular y **soporte de plugins**.

> Repositorio organizado para GitHub (limpio de `venv/`, `__pycache__/`, archivos binarios y zips de releases).  
> La configuración sensible se mueve a `data/config.example.json` y se ignoran los datos locales en `data/`.

## 🚀 Características
- Interfaz gráfica (Tkinter) con **Login** y **Panel**.
- Módulos en `core/` para indicadores, persistencia, logs, recuperación y puente UI ⇄ lógica.
- Soporte de **plugins** en `tools/` (ejemplos incluidos).
- Scripts para **instalación/ejecución** en Windows y empaquetado con **PyInstaller**.

## 📦 Estructura (resumen)
- `README.txt`
- `app.py`
- `build_exe_windows.bat`
- `core/__init__.py`
- `core/clicks.py`
- `core/indicators.py`
- `core/iq_helpers.py`
- `core/logger.py`
- `core/persistence.py`
- `core/plugins.py`
- `core/recovery.py`
- `core/state.py`
- `core/ui_bridge.py`
- `data/config.example.json`
- `docs/README.md`
- `docs/arquitectura.md`
- `docs/configuracion.md`
- `docs/contribuir.md`
- `docs/faq.md`
- `docs/instalacion_uso.md`
- `docs/modulos.md`
- `docs/paquetes_y_build.md`
- `docs/plantilla_changelog.md`
- `docs/solucion_problemas.md`
- `docs/ui.md`
- `install_and_run.bat`
- `iqbot.spec`
- `requirements.txt`
- `run_app.bat`
- `tools/alerta_uso.py`
- `tools/example_tool.py`
- `ui/__init__.py`
- `ui/login_frame.py`
- `ui/panel_frame.py`
- `ui/widgets.py`

## 🖥️ Requisitos
- Python 3.10+ (para desarrollo/ejecución con `pip`)
- Windows 10/11 (para scripts `.bat` y empaquetado con PyInstaller)

## ⬇️ Instalación rápida (desarrollo)
```bash
python -m venv .venv
. .venv/Scripts/activate    # Windows (PowerShell)
pip install -r requirements.txt
python app.py
```

## 🧩 Configuración
Copia `data/config.example.json` a `data/config.json` y ajusta tus preferencias. Ejemplo:

```json
{
  "asset_base": "EURUSD",
  "asset_otc": true,
  "auto_new_option": true,
  "recovery_margin": 0.06,
  "show_margin": true,
  "external_clicks": false,
  "enabled_tools": [
    "alerta_uso",
    "example_tool"
  ]
}
```

> **Nota:** El directorio `data/` (incluyendo `session.json` y `coords.json`) está **ignorado en Git** para evitar publicar datos locales.

## 🔌 Plugins
- Coloca tus plugins en `tools/` (ver ejemplos).
- Actívalos en `data/config.json` dentro de `enabled_tools`.
- Interfaz base disponible en `core/plugins.py`.

## 🏗️ Build (Windows → EXE)
- `build_exe_windows.bat` usa **PyInstaller** y genera `dist/app/app.exe`.
- Alternativas y detalles en `docs/paquetes_y_build.md`.

## 📚 Documentación
Consulta la carpeta [`docs/`](docs/), que incluye:
- arquitectura, módulos, UI, instalación y uso, configuración, empaquetado, troubleshooting y FAQ.

## 🤝 Contribuir
Lee [`CONTRIBUTING.md`](CONTRIBUTING.md) y el **Código de Conducta**.

## 📄 Licencia
Este proyecto usa la licencia **MIT** (ver `LICENSE`).

---

> _Organizado automáticamente el 2025-08-25 02:03._
