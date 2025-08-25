import time

def obtener_cierres(api, symbol, intervalo, n):
    velas = api.get_candles(symbol, intervalo, n, time.time())
    if not velas: return []
    velas.sort(key=lambda x: x['from'])
    return [v['close'] for v in velas]

def both_balances(api):
    try:
        api.change_balance("REAL"); time.sleep(0.25); real_ = api.get_balance()
        api.change_balance("PRACTICE"); time.sleep(0.25); prac_ = api.get_balance()
        api.change_balance("PRACTICE"); time.sleep(0.15)
        return real_, prac_
    except:
        return None, None
