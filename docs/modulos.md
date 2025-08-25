# Módulos principales

## app.py
- Clase `App`: inicializa la UI, muestra Login y Panel.
- Métodos: `show_login`, `on_login_success`.

## core/clicks.py
- `click_call(x, y)`, `click_put(x, y)`, `click_new(...)`: clics externos confiables.

## core/indicators.py
- `ema`, `rsi`, `macd`, `atr`, `sma`, `stochastic`, `bbands`.

## core/iq_helpers.py
- `connect(email, password)`
- `get_candles(asset, interval, count)`
- `buy(asset, direction, amount, duration)`
- `get_balance()`, `switch_to_demo()`, `switch_to_real()`, `is_demo()`
- `ensure_asset_open(asset)`

## core/logger.py
- `get_logger(name)`, `setup_file_logging(path)`

## core/persistence.py
- `load_json(path)`, `save_json(path, data)`
- `load_session()`, `save_session()`
- `load_config()`, `save_config()`

## core/plugins.py
- `discover_plugins(folder)`, `load_plugin(path)`, `run_plugins(context)`

## core/recovery.py
- `calc_stake_recovery(pool, payout, base, margin, balance_cap=inf)`
- `reset_recovery()`, `apply_result(win/loss)`

## core/state.py
- Constantes y flags globales: límites, modo, pausa, etc.

## core/ui_bridge.py
- `send_log`, `send_signal`, `send_error`, `bind_ui`, `unbind_ui`

## ui/login_frame.py
- Clase `LoginFrame` con `do_login()`.

## ui/panel_frame.py
- Clase `PanelFrame`: alternar demo/real, configurar coordenadas, probar clics,
  pausar/reanudar, marcar WIN/LOSS.

## ui/widgets.py
- `ScrollableFrame`: soporte de scroll para paneles largos.
