# Ejemplo de herramienta (plugin): aplica filtro simple para evitar sobreoperar
# y aumenta ligeramente el stake si el RSI es muy extremo.
from core.plugins import BaseTool
from core.logger import log_line

class Tool(BaseTool):
    NAME = "example_tool"

    def on_tick(self, market, ctx):
        # Solo log de muestra
        # market contiene claves: ema9, ema26, rsi, slope9, delta_ema, recommend, stake, etc.
        pass

    def before_order(self, decision, stake, market, ctx):
        rsi = market.get("rsi")
        # Filtro: si RSI está en zona media (47-53), evita entradas (esperar)
        if rsi is not None and 47 <= rsi <= 53:
            log_line("status","Plugin example_tool","RSI neutro, forzando ESPERAR")
            return "ESPERAR", stake
        # Aumenta 10% stake si RSI extremo (<=25 o >=75)
        if rsi is not None and (rsi <= 25 or rsi >= 75):
            ns = round(stake * 1.10, 2)
            log_line("status","Plugin example_tool",f"RSI extremo ({rsi:.2f}), stake {stake} → {ns}")
            return decision, ns
        return decision, stake

    def after_result(self, result, stake, mode, ctx):
        log_line("status","Plugin example_tool",f"Resultado {result} en {mode} con stake {stake}")
