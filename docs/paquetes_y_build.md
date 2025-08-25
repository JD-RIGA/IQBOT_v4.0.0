# Empaquetado y distribución

## PyInstaller
- Archivo de spec: `iqbot.spec`
- Script: `build_exe_windows.bat`

### Construcción
```bat
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller iqbot.spec
```
Salida en `dist/` con ejecutable.

## Portable
- Incluir `data/` por defecto con `config.json` mínimo.
- Asegurar permisos de escritura en carpeta del usuario para logs y session.
