import time
from core.state import LOG_FILE

LOG_TO_FILE = True

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
    C = {
        "OK":   Fore.GREEN + Style.BRIGHT, "BAD":  Fore.RED + Style.BRIGHT,
        "WARN": Fore.YELLOW + Style.BRIGHT, "INFO": Fore.CYAN + Style.NORMAL,
        "HEAD": Fore.MAGENTA + Style.BRIGHT, "KEY":  Fore.WHITE + Style.BRIGHT,
        "DIM":  Style.DIM, "RST":  Style.RESET_ALL,
    }
except Exception:
    C = {k: "" for k in ["OK","BAD","WARN","INFO","HEAD","KEY","DIM","RST"]}

EMOJI = {"status":"🔔","snap":"📊","mode":"🧭","click":"🖱️","test":"🧪","win":"✅","loss":"❌","count":"⏳","error":"⚠️",
         "rule":"─","sep":"─","box_t":"┏","box_b":"┗","box_s":"┠","box_s2":"┨"}

def _ts(): return time.strftime("%Y-%m-%d %H:%M:%S")

def _log_file(s):
    if not LOG_TO_FILE: return
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(s + "\n")
    except: pass

def log_line(kind, title, body=""):
    color = {"status":C["INFO"],"snap":C["HEAD"],"mode":C["KEY"],"click":C["KEY"],"test":C["KEY"],
             "win":C["OK"],"loss":C["BAD"],"count":C["DIM"],"error":C["BAD"]}.get(kind, C["INFO"])
    icon = EMOJI.get(kind,"•")
    line = f"{C['DIM']}{_ts()}{C['RST']} {color}{icon} {title}{C['RST']}" + (f" — {body}" if body else "")
    print(line); _log_file(f"{_ts()} [{kind}] {title} | {body}")

def log_snapshot_box(title_lines, body_lines, tail_lines=None):
    w=88
    top = EMOJI["box_t"] + ("━"*(w-2)) + "┓"
    print(C["DIM"] + top + C["RST"])
    for t in title_lines: print(C["HEAD"] + f"┃ {t}" + C["RST"])
    print(C["DIM"] + "┠" + ("─"*(w-4)) + "┨" + C["RST"])
    for b in body_lines: print(f"┃ {b}")
    if tail_lines:
        print(C["DIM"] + "┠" + ("─"*(w-4)) + "┨" + C["RST"])
        for t in tail_lines: print(f"┃ {t}")
    print(C["DIM"] + "┗" + ("━"*(w-2)) + "┛" + C["RST"])

def log_snapshot(symbol, a, rec_line):
    ema9_s  = "—" if a["ema9"]   is None else f"{a['ema9']:.6f}"
    ema26_s = "—" if a["ema26"]  is None else f"{a['ema26']:.6f}"
    rsi_s   = "—" if a["rsi"]    is None else f"{a['rsi']:.2f}"
    real_s  = "—" if a.get("bal_real") is None else f"{a['bal_real']:.2f}"
    prac_s  = "—" if a.get("bal_prac") is None else f"{a['bal_prac']:.2f}"
    delta_s = "—" if a["delta_ema"] is None else f"{a['delta_ema']:+.6f}"
    slope_s = "—" if a["slope9"] is None else f"{a['slope9']:+.6f}"
    trend_s = a.get("trend","—")
    zone_s  = a.get("rsi_zone","—")
    mom_s   = a.get("momentum","—")
    title = [f"{EMOJI['snap']} SNAPSHOT — {_ts()}"]
    body = [
        f"{C['KEY']}🧭 Activo:{C['RST']} {symbol}   {C['KEY']}💰 Stake:{C['RST']} {a['stake']:.2f}",
        f"{C['KEY']}📈 EMA9:{C['RST']} {ema9_s}   {C['KEY']}EMA26:{C['RST']} {ema26_s}   {C['KEY']}🧪 RSI:{C['RST']} {rsi_s}",
        f"🔍 Tendencia: {trend_s} (Δ={delta_s}) | Zona RSI: {zone_s} | Momentum EMA9: {mom_s} ({slope_s})",
        rec_line,
    ]
    tail = [f"💼 Totales → REAL: {real_s} | PRÁCTICA: {prac_s}"]
    log_snapshot_box(title, body, tail)
