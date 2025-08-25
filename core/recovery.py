import math
from core.state import STAKE_MAX_FACTOR

def calcular_stake_recuperacion(pool, payout, base, margin, balance_cap=float("inf")):
    if pool <= 0:
        return base
    objetivo = pool * (1.0 + margin)
    s = math.ceil((objetivo / payout) * 100) / 100.0
    s = min(s, balance_cap, base * STAKE_MAX_FACTOR)
    return max(base, s)
