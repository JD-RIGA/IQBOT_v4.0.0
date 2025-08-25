import importlib
import pkgutil
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List
from core.state import state
from core.logger import log_line

@dataclass
class Context:
    state: Dict[str, Any]
    def symbol(self) -> str:
        base = self.state['asset_base']
        return f"{base}{'-OTC' if self.state['asset_otc'] else ''}"

class BaseTool:
    NAME = "base"

    def on_tick(self, market: Dict[str, Any], ctx: Context) -> None:
        """Se llama en cada iteración tras calcular indicadores."""
        return

    def before_order(self, decision: str, stake: float, market: Dict[str, Any], ctx: Context) -> Tuple[str, float]:
        """Permite modificar (decision, stake) antes de entrar."""
        return decision, stake

    def after_result(self, result: str, stake: float, mode: str, ctx: Context) -> None:
        """Notificación de resultado ('WIN' o 'LOSS')."""
        return

class ToolManager:
    def __init__(self):
        self.tools: List[BaseTool] = []

    def load_from_config(self):
        enabled = state.get("enabled_tools", [])
        self.tools.clear()
        for name in enabled:
            try:
                mod = importlib.import_module(f"tools.{name}")
                tool_cls = getattr(mod, "Tool", None)
                if tool_cls is None:
                    log_line("error","Plugin","No encontró clase Tool en " + name); continue
                tool = tool_cls()
                self.tools.append(tool)
                log_line("status","Plugin cargado", tool.NAME)
            except Exception as e:
                log_line("error","Cargar plugin", f"{name}: {e}")

    def on_tick(self, market: Dict[str, Any]):
        ctx = Context(state)
        for t in self.tools:
            try: t.on_tick(market, ctx)
            except Exception as e: log_line("error","Plugin on_tick", f"{t.NAME}: {e}")

    def before_order(self, decision: str, stake: float, market: Dict[str, Any]):
        ctx = Context(state)
        for t in self.tools:
            try:
                decision, stake = t.before_order(decision, stake, market, ctx)
            except Exception as e:
                log_line("error","Plugin before_order", f"{t.NAME}: {e}")
        return decision, stake

    def after_result(self, result: str, stake: float, mode: str):
        ctx = Context(state)
        for t in self.tools:
            try: t.after_result(result, stake, mode, ctx)
            except Exception as e: log_line("error","Plugin after_result", f"{t.NAME}: {e}")
