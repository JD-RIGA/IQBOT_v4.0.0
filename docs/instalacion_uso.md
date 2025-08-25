# Instalación y uso (Windows)

## Requisitos
- Python 3.10+
- Windows 10/11
- Cuenta en IQ Option (credenciales válidas)
- Permisos para automatización de GUI (evitar superposiciones)

## Pasos rápidos
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Scripts útiles
- `install_and_run.bat` — instala dependencias y ejecuta.
- `run_app.bat` — ejecuta la app directamente.
- `build_exe_windows.bat` — empaqueta con PyInstaller usando `iqbot.spec`.

## Flujo básico
1. Inicia la app y realiza **login** (puedes alternar demo/real desde el panel).
2. Configura las **coordenadas** de CALL/PUT y prueba los clics.
3. Ajusta parámetros de **recuperación** y **margen** si aplica.
4. Observa logs y marca manualmente **WIN/LOSS** para entrenamiento.
