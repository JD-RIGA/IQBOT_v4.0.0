import json, os
from core.state import state, COORDS_FILE, CONFIG_FILE, DEFAULT_CONFIG
from core.logger import log_line

def load_coords():
    try:
        with open(COORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        state["coords"].update(data.get("coords", {}))
        log_line("status","Coordenadas","Cargadas")
    except FileNotFoundError:
        pass
    except Exception as e:
        log_line("error","Cargar coords",str(e))

def save_coords():
    try:
        with open(COORDS_FILE, "w", encoding="utf-8") as f:
            json.dump({"coords": state["coords"]}, f, indent=2)
        log_line("status","Coordenadas","Guardadas")
    except Exception as e:
        log_line("error","Guardar coords",str(e))

def load_config():
    try:
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        state["asset_base"]      = d.get("asset_base", state["asset_base"])
        state["asset_otc"]       = bool(d.get("asset_otc", state["asset_otc"]))
        state["auto_new_option"] = bool(d.get("auto_new_option", state["auto_new_option"]))
        state["recovery_margin"] = float(d.get("recovery_margin", state["recovery_margin"]))
        state["show_margin"]     = bool(d.get("show_margin", state["show_margin"]))
        state["external_clicks"] = bool(d.get("external_clicks", state["external_clicks"]))
        state["enabled_tools"]   = list(d.get("enabled_tools", state.get("enabled_tools", [])))
        log_line("status","Config",
                 f"{state['asset_base']} | OTC={state['asset_otc']} | AutoNueva={state['auto_new_option']} "
                 f"| Margin={int(state['recovery_margin']*100)}% | ShowMargin={state['show_margin']} "
                 f"| ExternalClicks={state['external_clicks']} | Tools={state['enabled_tools']}")
    except Exception as e:
        log_line("error","Cargar config",str(e))

def save_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        d = {}
    d.update({
        "asset_base": state["asset_base"],
        "asset_otc": state["asset_otc"],
        "auto_new_option": state["auto_new_option"],
        "recovery_margin": state["recovery_margin"],
        "show_margin": state["show_margin"],
        "external_clicks": state["external_clicks"],
        "enabled_tools": state["enabled_tools"],
    })
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
        log_line("status","Config","Guardada")
    except Exception as e:
        log_line("error","Guardar config",str(e))
