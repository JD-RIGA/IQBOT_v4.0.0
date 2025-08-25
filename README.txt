IQBOT — INSTALACIÓN FÁCIL (SIN PROGRAMAR)

OPCIÓN A) USARLO YA MISMO (Windows)
1. Haz doble clic en:  install_and_run.bat
   - Crea una carpeta interna (venv), instala lo necesario y abre la app.
2. La próxima vez, solo usa:  run_app.bat

Requisitos: Windows 10/11 y conexión a internet. (Python NO es obligatorio para la opción B de EXE)

OPCIÓN B) CREAR UN .EXE (Windows, sin programar)
1. Haz doble clic en:  build_exe_windows.bat
   - Descarga PyInstaller y empaqueta la app.
2. Al terminar, el ejecutable quedará en:  dist\app\app.exe
3. Puedes copiar esa carpeta a otro PC y abrir el .exe sin instalar nada.

CONFIGURACIÓN RÁPIDA
- Abre el archivo:  data\config.json  (haz doble clic y edítalo con el Bloc de notas)
  - "asset_base": "EURUSD"         → Activo base
  - "asset_otc": true/false         → Usar mercado OTC
  - "external_clicks": true/false   → Activar clic REAL en IQ Option (si está en pantalla)
  - "recovery_margin": 0.05         → 5% para recuperación
  - "enabled_tools": ["example_tool"] → Lista de plugins activos (en carpeta tools)

PLUGINS (HERRAMIENTAS EXTERNAS)
- Carpeta: tools\
- Cada archivo es un plugin. Ejemplo: tools\example_tool.py
- Para activarlo, añade su nombre en "enabled_tools" del config.
- Plantilla rápida (crea tools\mi_tool.py):
    from core.plugins import BaseTool
    from core.logger import log_line
    class Tool(BaseTool):
        NAME = "mi_tool"
        def before_order(self, decision, stake, market, ctx):
            # ... modifica o bloquea entrada ...
            return decision, stake

PREGUNTAS COMUNES
- ¿Necesito cuenta de IQ Option? Sí, e iniciar sesión desde la app.
- ¿Es seguro? No guarda tu contraseña en servidores; queda local en data\session.json
- ¿No se abren los clics? Activa “Hacer clic externo” en el panel y ten IQ Option en primer plano.
- ¿Errores de módulos? Ejecuta install_and_run.bat de nuevo.

Soporte: edita config y prueba en modo PRÁCTICA antes de REAL.
