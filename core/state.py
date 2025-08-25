import os
import pyautogui

DEFAULT_BASE = "EURUSD"
TIEMPO_EXP = 1           # min
INTERVALO = 60           # seg
VELAS_BUFFER = 300
STAKE_BASE = 1.0
PAYOUT = 0.80
STAKE_MAX_FACTOR = 10
RECOVERY_MARGIN_DEFAULT = 0.05  # 5%

BASES = ["EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCHF","NZDUSD","USDCAD","EURGBP","GBPJPY"]

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

SESSION_FILE = os.path.join(DATA_DIR, "session.json")
COORDS_FILE  = os.path.join(DATA_DIR, "coords.json")
CONFIG_FILE  = os.path.join(DATA_DIR, "config.json")
LOG_FILE     = os.path.join(ROOT_DIR, "bot_log.txt")

# Defaults si no hay config previa
DEFAULT_CONFIG = {
    "asset_base": DEFAULT_BASE,
    "asset_otc": True,
    "auto_new_option": True,
    "recovery_margin": RECOVERY_MARGIN_DEFAULT,
    "show_margin": True,
    "external_clicks": False,
    "enabled_tools": ["example_tool"]
}

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.03

state = {
    "mode": "", "external_clicks": DEFAULT_CONFIG["external_clicks"], "auto_new_option": True,
    "balance_real": None, "balance_practice": None,
    "asset_base": DEFAULT_BASE, "asset_otc": True,
    "coords": {"call":{"x":1848,"y":522}, "put":{"x":1842,"y":656}, "new":{"x":1550,"y":600}},
    "recovery_margin": RECOVERY_MARGIN_DEFAULT,
    "show_margin": True,
    "enabled_tools": DEFAULT_CONFIG["enabled_tools"],
}

stats = {
    "REAL":     {"loss_pool": 0.0, "won": 0.0, "lost": 0.0},
    "PRACTICE": {"loss_pool": 0.0, "won": 0.0, "lost": 0.0},
}

def symbol_from_state():
    return f"{state['asset_base']}{'-OTC' if state['asset_otc'] else ''}"

# Re-export helpers de persistencia
from core.persistence import load_coords, save_coords, load_config, save_config  # noqa
