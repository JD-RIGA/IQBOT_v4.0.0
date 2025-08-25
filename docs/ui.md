# Interfaz de usuario (UI)

## Login
- Campo de email/contraseña y botón de acceso.
- Valida credenciales vía `core/iq_helpers.connect()`.
- En caso de error, muestra mensaje y permite reintentar.

## Panel
- **Modo**: alterna DEMO/REAL.
- **Coordenadas**: botones para capturar x,y de CALL y PUT; pruebas de clic.
- **Trading rápido**: botones de CALL/PUT (si aplica), temporizador, etc.
- **Gestión**: pausa/reanuda, salida segura.
- **Resultados**: marcar WIN/LOSS para el módulo de recuperación.
- **Logs**: visor con scroll, severidad y timestamps.
