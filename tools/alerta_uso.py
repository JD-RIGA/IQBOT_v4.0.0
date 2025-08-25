import time
from core.plugins import BaseTool
from core.logger import log_line
from core import clicks as clicks_mod
from core import ui_bridge

COURTESY_SECONDS = 15
IDLE_REQUIRED    = 2
MAX_WAIT_SECONDS = 45

def _safe_beep(times=3):
    try:
        import winsound
        for _ in range(times):
            winsound.Beep(950, 160)
            time.sleep(0.08)
    except Exception:
        for _ in range(times):
            print('\a', end='', flush=True)
            time.sleep(0.12)

def _wait_for_idle_with_popup():
    log_line("status","AlertaUso","INICIO espera (popup + beep)")
    try:
        import pyautogui
    except Exception as e:
        log_line("status","AlertaUso",f"pyautogui no disponible: {e}. Espera fija {COURTESY_SECONDS}s.")
        _safe_beep(3)
        time.sleep(COURTESY_SECONDS)
        return

    try:
        ui_bridge.alert_open(title="Alerta de uso del mouse",
                             message=f"⚠ El bot usará el mouse en {COURTESY_SECONDS}s…")
        log_line("status","AlertaUso","Popup abierto (ui_bridge)")
    except Exception as e:
        log_line("error","AlertaUso",f"No se pudo abrir popup: {e}")

    _safe_beep(3)
    log_line("status","AlertaUso","Beep x3 enviado")

    end_courtesy = time.time() + COURTESY_SECONDS
    while time.time() < end_courtesy:
        ui_bridge.alert_set(seconds_left=end_courtesy - time.time())
        time.sleep(0.1)

    ui_bridge.alert_set(message="Esperando que el mouse quede quieto…")

    start_wait = time.time()
    idle_start = None
    last_pos = pyautogui.position()

    while True:
        time.sleep(0.15)
        pos = pyautogui.position()
        if pos != last_pos:
            idle_start = None
            last_pos = pos
            log_line("status","AlertaUso","Mouse en uso; esperando reposo…")
        else:
            if idle_start is None:
                idle_start = time.time()
            elif time.time() - idle_start >= IDLE_REQUIRED:
                log_line("status","AlertaUso",f"Reposo detectado ({IDLE_REQUIRED}s). Continuando.")
                break

        if time.time() - start_wait > MAX_WAIT_SECONDS:
            log_line("warn","AlertaUso",f"Tiempo máx. espera agotado ({MAX_WAIT_SECONDS}s). Continuando.")
            break

    try:
        ui_bridge.alert_close()
        log_line("status","AlertaUso","Popup cerrado")
    except Exception as e:
        log_line("error","AlertaUso",f"No se pudo cerrar popup: {e}")

def _wrap_click(fn, name):
    def wrapper(*args, **kwargs):
        log_line("status","AlertaUso",f"WRAPPER INVOCADO → {name}")
        try:
            _wait_for_idle_with_popup()
        except Exception as e:
            log_line("error","AlertaUso",f"Error en espera: {e}")
        log_line("status","AlertaUso",f"Ejecutando clic real: {name}")
        return fn(*args, **kwargs)
    return wrapper

class Tool(BaseTool):
    NAME = "alerta_uso"

    def __init__(self):
        log_line("status","AlertaUso","Inicializando plugin...")
        try:
            if not getattr(clicks_mod, "_alerta_uso_patched", False):
                clicks_mod.click_call = _wrap_click(clicks_mod.click_call, "CALL")
                clicks_mod.click_put  = _wrap_click(clicks_mod.click_put,  "PUT")
                clicks_mod.click_new  = _wrap_click(clicks_mod.click_new,  "NUEVA OPCIÓN")
                clicks_mod._alerta_uso_patched = True
                log_line("status","AlertaUso","Parche aplicado a funciones de clic ✅")
            else:
                log_line("warn","AlertaUso","Ya estaba parcheado (evitando duplicado).")
        except Exception as e:
            log_line("error","AlertaUso",f"No se pudieron parchear los clics: {e}")

    def on_tick(self, market, ctx): return
    def before_order(self, decision, stake, market, ctx): return decision, stake
    def after_result(self, result, stake, mode, ctx): return
