# Arquitectura

```
app.py  -> Crea Tk/App, monta LoginFrame y PanelFrame, conecta con core/ui_bridge
  ui/   -> login_frame.py, panel_frame.py, widgets.py (Scroll, Cards, etc.)
  core/ -> clicks.py, indicators.py, iq_helpers.py, logger.py, persistence.py,
           plugins.py, recovery.py, state.py, ui_bridge.py
  data/ -> config.json, session.json
  tools/-> scripts auxiliares y plugins de ejemplo
```
Comunicación:
- **UI ↔ core/ui_bridge.py**: Eventos y mensajes (logs, señales, errores).
- **core/iq_helpers.py ↔ IQ Option**: Conexión, velas, compra, balance, demo/real.
- **core/recovery.py**: Cálculo de stake de recuperación y aplicación de resultados.
- **core/clicks.py**: Clics externos en coordenadas configurables (CALL/PUT).
- **core/indicators.py**: EMA/RSI/MACD/ATR/SMA/Stochastic/Bollinger.
- **core/persistence.py**: Guardar/cargar configuración y sesión.
- **core/plugins.py**: Descubrir/cargar/ejecutar plugins.

Estados:
- `core/state.py` define constantes, flags (pausa, modo demo/real), y parámetros globales.
