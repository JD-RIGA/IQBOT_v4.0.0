def ema(vals, length):
    if not vals or len(vals) < length: return None
    k = 2/(length+1); e = sum(vals[:length])/length
    for v in vals[length:]:
        e = v*k + e*(1-k)
    return e

def rsi(vals, length=14):
    if len(vals) < length+1: return None
    g=l=0
    for i in range(1,length+1):
        d=vals[i]-vals[i-1]; g+=max(d,0); l+=abs(min(d,0))
    g/=length; l/=length
    for i in range(length+1,len(vals)):
        d=vals[i]-vals[i-1]
        g=(g*(length-1)+max(d,0))/length
        l=(l*(length-1)+abs(min(d,0)))/length
    if l==0: return 100.0
    rs=g/l; return 100 - (100/(1+rs))

def analisis_decision(cierres):
    a = {"ema9":None,"ema26":None,"rsi":None,"slope9":None,"delta_ema":None,
         "trend":None,"rsi_zone":None,"momentum":None,"recommend":"ESPERAR","rules":[], "explain":[]}
    if len(cierres) < 30: return a

    e9  = ema(cierres, 9);  e26 = ema(cierres, 26); r = rsi(cierres,14)
    e9p = ema(cierres[:-1],9) if len(cierres)>=10 else None
    slope9 = (e9 - e9p) if (e9 is not None and e9p is not None) else None
    delta  = (e9 - e26) if (e9 is not None and e26 is not None) else None

    a.update({"ema9":e9,"ema26":e26,"rsi":r,"slope9":slope9,"delta_ema":delta})

    if delta is not None:
        if delta > 0: a["trend"]="alcista"
        elif delta < 0: a["trend"]="bajista"
        else: a["trend"]="plana"
        a["explain"].append(f"Tendencia EMA: {a['trend']} (Δ={delta:+.6f})")

    if r is not None:
        if r >= 60: zone="fuerte alcista"
        elif r >= 50: zone="ligera alcista"
        elif r > 40: zone="ligera bajista"
        else: zone="fuerte bajista"
        a["rsi_zone"]=zone
        a["explain"].append(f"RSI {r:.2f} → {zone}")

    if slope9 is not None:
        mom = "subiendo" if slope9>0 else ("bajando" if slope9<0 else "plano")
        a["momentum"]=mom
        a["explain"].append(f"Momentum EMA9: {mom} ({slope9:+.6f})")

    rule_call = (delta is not None and delta>0) and (r is not None and r>50) and (slope9 is not None and slope9>0)
    rule_put  = (delta is not None and delta<0) and (r is not None and r<50) and (slope9 is not None and slope9<0)

    a["rules"] = [("EMA9>EMA26", delta is not None and delta>0),
                  ("EMA9<EMA26", delta is not None and delta<0),
                  ("RSI>50", r is not None and r>50),
                  ("RSI<50", r is not None and r<50),
                  ("Slope9>0", slope9 is not None and slope9>0),
                  ("Slope9<0", slope9 is not None and slope9<0)]
    if rule_call: a["recommend"]="CALL"
    elif rule_put: a["recommend"]="PUT"
    else: a["recommend"]="ESPERAR"
    return a
