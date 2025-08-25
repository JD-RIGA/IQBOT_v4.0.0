
import tkinter as tk
import threading, queue, time, random

from core.state import (state, stats, PAYOUT, STAKE_BASE, INTERVALO,
                        VELAS_BUFFER, BASES, symbol_from_state)
from core.logger import log_line, log_snapshot
from core.recovery import calcular_stake_recuperacion
from core.indicators import analisis_decision
from core.iq_helpers import obtener_cierres, both_balances
from core.clicks import click_call, click_put, click_new
from core.persistence import load_coords, save_coords, save_config

# Frame con scroll integrado
class ScrollableFrame(tk.Frame):
    def __init__(self, master, bg="#0e0e10"):
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.vbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.inner = tk.Frame(self.canvas, bg=bg)

        self.win = self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vbar.pack(side="right", fill="y")

        self.inner.bind("<Configure>", self._on_inner_config)
        self.canvas.bind("<Configure>", self._on_canvas_config)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_inner_config(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_config(self, event):
        self.canvas.itemconfig(self.win, width=event.width)

    def _on_mousewheel(self, event):
        delta = int(-1*(event.delta/120))
        self.canvas.yview_scroll(delta, "units")


class PanelFrame(tk.Frame):
    def __init__(self, master, api=None, tool_manager=None, **kwargs):
        super().__init__(master, bg="#0e0e10", **kwargs)
        self.master=master; self.api=api; self.tools=tool_manager
        self.q=queue.Queue(); self.stop_evt=threading.Event(); self.pause_evt=threading.Event(); self.worker=None

        # Contenedor con scroll
        self.scroller = ScrollableFrame(self, bg="#0e0e10"); self.scroller.pack(fill="both", expand=True)
        self.root = self.scroller.inner

        # Tk vars
        self.var_mode=tk.StringVar(value="")
        self.var_ext=tk.BooleanVar(value=state["external_clicks"])
        self.var_auto_new=tk.BooleanVar(value=state["auto_new_option"])
        self.var_stake=tk.StringVar(value="—"); self.var_ema9=tk.StringVar(value="—")
        self.var_ema26=tk.StringVar(value="—"); self.var_rsi=tk.StringVar(value="—")
        self.var_real=tk.StringVar(value="—"); self.var_prac=tk.StringVar(value="—")
        self.var_base=tk.StringVar(value=state["asset_base"])
        self.var_otc=tk.BooleanVar(value=state["asset_otc"])
        self.var_manual=tk.StringVar(value="")
        self.var_act_symbol=tk.StringVar(value=symbol_from_state())
        self.var_analysis=tk.StringVar(value="(aún sin análisis)")
        self.var_reco=tk.StringVar(value="—")
        self.var_call_x=tk.StringVar(value=str(state["coords"]["call"]["x"]))
        self.var_call_y=tk.StringVar(value=str(state["coords"]["call"]["y"]))
        self.var_put_x=tk.StringVar(value=str(state["coords"]["put"]["x"]))
        self.var_put_y=tk.StringVar(value=str(state["coords"]["put"]["y"]))
        self.var_new_x=tk.StringVar(value=str(state["coords"]["new"]["x"]))
        self.var_new_y=tk.StringVar(value=str(state["coords"]["new"]["y"]))
        self.var_status=tk.StringVar(value="Conectado. Iniciando…")

        # Recuperación
        self.var_recovery=tk.StringVar(value="Pool=0.00 · +5% · StakeSug=1.00")
        self.var_margin = tk.DoubleVar(value=state["recovery_margin"]*100.0)
        self.var_show_margin = tk.BooleanVar(value=state["show_margin"])  # <- TOGGLE

        self.pending = {"stake": None, "mode": None}

        self.pack(fill="both", expand=True)
        self.build()

        # Lanzar worker
        self.worker=threading.Thread(target=self.bot_worker,daemon=True); self.worker.start()
        self.after(100,self.drain_queue)

    def card(self,parent,pad=(16,16)):
        f=tk.Frame(parent,bg="#151518",highlightthickness=1,highlightbackground="#222228")
        f.pack(fill="x",padx=22,pady=10); f._padx,f._pady=pad; return f
    def row(self,parent,title,var):
        r=tk.Frame(parent,bg="#151518"); r.pack(fill="x",padx=parent._padx,pady=6)
        tk.Label(r,text=title,width=18,anchor="e",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left")
        tk.Label(r,textvariable=var,anchor="w",bg="#151518",fg="#FFD86B",font=("Segoe UI",12,"bold")).pack(side="left")

    def build(self):
        # Header
        hdr=self.card(self.root)
        tk.Label(hdr,text="Panel de Trading",bg="#151518",fg="#e5e5e5",font=("Segoe UI",16,"bold"))\
            .pack(padx=hdr._padx,pady=(hdr._pady,6),anchor="w")
        top=tk.Frame(hdr,bg="#151518"); top.pack(fill="x",padx=hdr._padx,pady=(0,8))
        tk.Label(top,text="Modo:",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left",padx=(0,8))
        tk.Label(top,textvariable=self.var_mode,bg="#151518",fg="#FFD86B",font=("Segoe UI",12,"bold")).pack(side="left")
        tk.Checkbutton(top,text="Hacer clic externo",variable=self.var_ext,command=self.toggle_external,
                       bg="#151518",fg="#FFD86B",activebackground="#151518",selectcolor="#151518",
                       font=("Segoe UI",10,"bold")).pack(side="right")

        # Activo
        card_act=self.card(self.root)
        tk.Label(card_act,text="Activo",bg="#151518",fg="#bdbdbd",font=("Segoe UI",11,"bold"),padx=card_act._padx)\
            .pack(anchor="w",pady=(card_act._pady-6,0))
        r1=tk.Frame(card_act,bg="#151518"); r1.pack(fill="x",padx=card_act._padx,pady=6)
        tk.Label(r1,text="Base:",width=18,anchor="e",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left")
        om=tk.OptionMenu(r1,self.var_base,*BASES); om.config(bg="#2a2a31",fg="#fff",activebackground="#3a3a45",relief="flat"); om.pack(side="left")
        tk.Checkbutton(r1,text="OTC",variable=self.var_otc,bg="#151518",fg="#FFD86B",activebackground="#151518",selectcolor="#151518").pack(side="left",padx=12)
        r2=tk.Frame(card_act,bg="#151518"); r2.pack(fill="x",padx=card_act._padx,pady=6)
        tk.Label(r2,text="Manual:",width=18,anchor="e",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left")
        tk.Entry(r2,textvariable=self.var_manual,width=18,bg="#1c1c21",fg="#e5e5e5",relief="flat").pack(side="left",padx=(0,10))
        tk.Button(r2,text="Aplicar",command=self.apply_asset,bg="#3a3a45",fg="#fff",relief="flat",padx=12,cursor="hand2").pack(side="left")
        r3=tk.Frame(card_act,bg="#151518"); r3.pack(fill="x",padx=card_act._padx,pady=6)
        tk.Label(r3,text="Actual:",width=18,anchor="e",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left")
        tk.Label(r3,textvariable=self.var_act_symbol,bg="#151518",fg="#FFD86B",font=("Consolas",12,"bold")).pack(side="left")

        # Indicadores
        card_ind=self.card(self.root)
        tk.Label(card_ind,text="Indicadores",bg="#151518",fg="#bdbdbd",font=("Segoe UI",11,"bold"),padx=card_ind._padx)\
            .pack(anchor="w",pady=(card_ind._pady-6,0))
        self.row(card_ind,"💰 Stake:",self.var_stake)
        self.row(card_ind,"📈 EMA9:",self.var_ema9)
        self.row(card_ind,"EMA26:",self.var_ema26)
        self.row(card_ind,"🧪 RSI:",self.var_rsi)

        # Análisis
        card_an=self.card(self.root)
        tk.Label(card_an,text="Análisis de decisión",bg="#151518",fg="#bdbdbd",font=("Segoe UI",11,"bold"),padx=card_an._padx)\
            .pack(anchor="w",pady=(card_an._pady-6,0))
        tk.Label(card_an,textvariable=self.var_analysis,bg="#151518",fg="#e5e5e5",font=("Consolas",10),justify="left",wraplength=780)\
            .pack(anchor="w",padx=card_an._padx)
        rowr=tk.Frame(card_an,bg="#151518"); rowr.pack(fill="x",padx=card_an._padx,pady=6)
        tk.Label(rowr,text="Recomendación:",width=18,anchor="e",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left")
        tk.Label(rowr,textvariable=self.var_reco,bg="#151518",fg="#FFD86B",font=("Segoe UI",12,"bold")).pack(side="left")

        # Recuperación (siempre visible)
        rowrec=tk.Frame(card_an,bg="#151518"); rowrec.pack(fill="x",padx=card_an._padx,pady=0)
        tk.Label(rowrec,text="Recuperación:",width=18,anchor="e",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left")
        tk.Label(rowrec,textvariable=self.var_recovery,bg="#151518",fg="#FFD86B",font=("Consolas",11)).pack(side="left")

        # Toggle de slider
        ctrlm=tk.Frame(card_an,bg="#151518"); ctrlm.pack(fill="x",padx=card_an._padx,pady=(4,0))
        tk.Checkbutton(ctrlm,text="Mostrar ajuste de margen",variable=self.var_show_margin,
                       command=self.toggle_margin_ui,bg="#151518",fg="#e5e5e5",
                       activebackground="#151518",selectcolor="#151518").pack(side="left")

        # Slider margen
        self.rowm=tk.Frame(card_an,bg="#151518")
        tk.Label(self.rowm,text="Margen (%):",width=18,anchor="e",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left")
        self.scale = tk.Scale(self.rowm, variable=self.var_margin, from_=0, to=30, orient="horizontal",
                              showvalue=True, resolution=1, length=260,
                              command=lambda v: self.update_margin())
        self.scale.config(bg="#151518", fg="#e5e5e5", highlightthickness=0, troughcolor="#2a2a31", sliderlength=16)
        self.scale.pack(side="left",padx=(6,0))
        if state['show_margin']:
            self.rowm.pack(fill="x",padx=card_an._padx,pady=(4,6))

        # Cuentas
        card_acc=self.card(self.root)
        tk.Label(card_acc,text="Cuentas",bg="#151518",fg="#bdbdbd",font=("Segoe UI",11,"bold"),padx=card_acc._padx)\
            .pack(anchor="w",pady=(card_acc._pady-6,0))
        self.row(card_acc,"💵 Total REAL:",self.var_real)
        self.row(card_acc,"🪙 Total PRÁCTICA:",self.var_prac)

        # Coordenadas + pruebas
        card_xy=self.card(self.root)
        tk.Label(card_xy,text="Coordenadas (captura y guarda)",bg="#151518",fg="#bdbdbd",font=("Segoe UI",11,"bold"),padx=card_xy._padx)\
            .pack(anchor="w",pady=(card_xy._pady-6,0))
        def xy_row(p,title,varx,vary,on_take):
            r=tk.Frame(p,bg="#151518"); r.pack(fill="x",padx=p._padx,pady=6)
            tk.Label(r,text=title,width=18,anchor="e",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11)).pack(side="left")
            tk.Entry(r,textvariable=varx,width=7,bg="#1c1c21",fg="#e5e5e5",relief="flat").pack(side="left")
            tk.Label(r,text=",",bg="#151518",fg="#e5e5e5").pack(side="left",padx=2)
            tk.Entry(r,textvariable=vary,width=7,bg="#1c1c21",fg="#e5e5e5",relief="flat").pack(side="left")
            tk.Button(r,text="Tomar",command=on_take,bg="#2a2a31",fg="#fff",relief="flat",padx=10,cursor="hand2").pack(side="left",padx=10)
        xy_row(card_xy,"CALL (x,y):",self.var_call_x,self.var_call_y,lambda: self.capture_xy("call"))
        xy_row(card_xy,"PUT  (x,y):",self.var_put_x,self.var_put_y,lambda: self.capture_xy("put"))
        xy_row(card_xy,"NUEVA OPCIÓN (x,y):",self.var_new_x,self.var_new_y,lambda: self.capture_xy("new"))
        tools=tk.Frame(card_xy,bg="#151518"); tools.pack(fill="x",padx=card_xy._padx,pady=6)
        tk.Button(tools,text="Guardar",command=self.save_xy,bg="#3a3a45",fg="#fff",relief="flat",padx=12,cursor="hand2").pack(side="left",padx=4)
        tk.Button(tools,text="Cargar",command=self.load_xy,bg="#3a3a45",fg="#fff",relief="flat",padx=12,cursor="hand2").pack(side="left",padx=4)
        tk.Button(tools,text="Probar CALL",command=self.test_call,bg="#3c6e47",fg="#fff",relief="flat",padx=12,cursor="hand2").pack(side="left",padx=14)
        tk.Button(tools,text="Probar PUT",command=self.test_put,bg="#6e3c3c",fg="#fff",relief="flat",padx=12,cursor="hand2").pack(side="left",padx=4)
        tk.Button(tools,text="Probar NUEVA OPCIÓN",command=self.test_new,bg="#6e553c",fg="#fff",relief="flat",padx=12,cursor="hand2").pack(side="left",padx=14)
        tk.Checkbutton(tools,text="Auto ‘Nueva opción’",variable=self.var_auto_new,command=self.toggle_auto_new,
                       bg="#151518",fg="#FFD86B",activebackground="#151518",selectcolor="#151518",
                       font=("Segoe UI",10,"bold")).pack(side="right",padx=8)

        # Estado y controles
        card_st=self.card(self.root)
        tk.Label(card_st,text="Estado:",bg="#151518",fg="#e5e5e5",font=("Segoe UI",11),padx=card_st._padx).pack(anchor="w")
        tk.Label(card_st,textvariable=self.var_status,bg="#151518",fg="#9CDCFE",font=("Consolas",11),padx=card_st._padx,justify="left")\
            .pack(anchor="w",pady=(2,card_st._pady-6))
        bar=self.card(self.root,pad=(12,12))
        def btn(t,cmd,color="#2a2a31"):
            return tk.Button(bar,text=t,command=cmd,bg=color,fg="#fff",activebackground="#3a3a45",relief="flat",
                             font=("Segoe UI",10,"bold"),padx=14,pady=8,cursor="hand2")
        btn("Marcar WIN",self.mark_win,color="#3c6e47").pack(side="left",padx=6)
        btn("Marcar LOSS",self.mark_loss,color="#6e3c3c").pack(side="left",padx=6)
        btn("PRACTICE",self.to_practice).pack(side="left",padx=6)
        btn("REAL",self.to_real,color="#a03a3a").pack(side="left",padx=6)
        btn("Pausar/Reanudar",self.toggle_pause,color="#314a7a").pack(side="left",padx=6)
        btn("Salir",self.exit_all,color="#7a2e2e").pack(side="right",padx=6)

    # ===== WORKER =====
    def bot_worker(self):
        try:
            self.api.change_balance("PRACTICE"); self.q.put(("mode","PRACTICE")); log_line("mode","Cuenta","PRACTICE")
        except Exception as e:
            self.q.put(("status",f"No se pudo forzar PRACTICE: {e}")); log_line("error","Forzar PRACTICE",str(e))

        last_bal=0
        while not self.stop_evt.is_set():
            try:
                if self.pause_evt.is_set():
                    self.q.put(("status","⏸ Pausado")); time.sleep(0.25); continue

                if time.time()-last_bal>30:
                    real_,prac_=both_balances(self.api)
                    state["balance_real"],state["balance_practice"]=real_,prac_
                    self.q.put(("balance_real",real_)); self.q.put(("balance_practice",prac_))
                    last_bal=time.time()
                    log_line("status","Balances",f"REAL={real_} | PRACTICE={prac_}")

                symbol = symbol_from_state()
                cierres = obtener_cierres(self.api, symbol, INTERVALO, VELAS_BUFFER)
                if len(cierres)<30:
                    self.q.put(("status",f"Esperando velas de {symbol}…")); log_line("status","Mercado",f"Esperando velas de {symbol}…")
                    time.sleep(1); continue

                a = analisis_decision(cierres)

                # Stake con recuperación
                cur_mode = (self.var_mode.get() or "PRACTICE")
                pool = stats[cur_mode]["loss_pool"]
                bal_cap = (state["balance_real"] if cur_mode=="REAL" else state["balance_practice"]) or float("inf")
                margin = state["recovery_margin"]
                stake_suggest = calcular_stake_recuperacion(pool, PAYOUT, STAKE_BASE, margin, bal_cap)
                a["stake"] = stake_suggest
                a["bal_real"]=state["balance_real"]; a["bal_prac"]=state["balance_practice"]

                # Plugins (si existen)
                if hasattr(self, "tools") and self.tools:
                    try: self.tools.on_tick(a)
                    except Exception as e: log_line("error","Plugin on_tick", str(e))
                    decision = a["recommend"]
                    try:
                        decision, stake_suggest = self.tools.before_order(decision, stake_suggest, a, None)
                    except Exception as e:
                        log_line("error","Plugin before_order", str(e))
                    a["stake"] = stake_suggest
                else:
                    decision = a["recommend"]

                # UI + log
                self.q.put(("stake", a["stake"]))
                self.q.put(("ema9", a["ema9"])); self.q.put(("ema26", a["ema26"])); self.q.put(("rsi", a["rsi"]))

                delta_s  = "—" if a["delta_ema"] is None else f"{a['delta_ema']:+.6f}"
                rsi_s    = "—" if a["rsi"] is None else f"{a['rsi']:.2f}"
                slope9_s = "—" if a["slope9"] is None else f"{a['slope9']:+.6f}"
                rules_line = " | ".join([("✓ " if ok else "✗ ") + name
                                         for name, ok in a["rules"]
                                         if name in ['EMA9>EMA26','EMA9<EMA26','RSI>50','RSI<50','Slope9>0','Slope9<0']]) or "—"
                analysis_text = (
                    f"Tendencia EMA: {a.get('trend','—')} (Δ={delta_s})\n"
                    f"RSI: {rsi_s}  | Zona: {a.get('rsi_zone','—')}\n"
                    f"Momentum EMA9: {a.get('momentum','—')} ({slope9_s})\n"
                    f"Reglas: {rules_line}"
                )
                self.q.put(("analysis", analysis_text))
                self.q.put(("reco", decision))
                rec_line = f"💊 Recuperación → Pool={pool:.2f} · +{int(margin*100)}% · StakeSug={stake_suggest:.2f}"
                self.q.put(("recovery", f"Pool={pool:.2f} · +{int(margin*100)}% · StakeSug={stake_suggest:.2f}"))
                log_snapshot(symbol, a, rec_line)

                if decision == "ESPERAR":
                    self.countdown("Mercado lateral. Esperando…", 8); continue

                if state["external_clicks"]:
                    self.pending["stake"] = stake_suggest
                    self.pending["mode"]  = cur_mode

                    self.q.put(("status", f"Entrada: {decision} (clic externo)")); log_line("status","Entrada",decision)
                    self.countdown(f"{decision} — clic en", 1)
                    if decision=="CALL": click_call(); log_line("click","CALL",str(state["coords"]["call"]))
                    else: click_put(); log_line("click","PUT",str(state["coords"]["put"]))
                    self.q.put(("status","⏳ Esperando resultado…")); self.countdown("Resultado en", 60 + 2)
                    if state["auto_new_option"]:
                        self.q.put(("status","Recuperando botones… ‘Nueva opción’")); time.sleep(0.4); click_new(); log_line("click","NUEVA OPCIÓN",str(state["coords"]["new"]))
                    self.q.put(("status","Marca WIN/LOSS para actualizar el pool."))
                else:
                    win = random.random() < 0.55
                    self.q.put(("status", f"{decision} — simulando…")); self.countdown("Resultado en", 60 + 2)
                    if win:
                        self._apply_win(stake_suggest, cur_mode)
                        if hasattr(self, "tools") and self.tools:
                            try: self.tools.after_result("WIN", stake_suggest, cur_mode)
                            except Exception as e: log_line("error","Plugin after_result", str(e))
                    else:
                        self._apply_loss(stake_suggest, cur_mode)
                        if hasattr(self, "tools") and self.tools:
                            try: self.tools.after_result("LOSS", stake_suggest, cur_mode)
                            except Exception as e: log_line("error","Plugin after_result", str(e))
                    self.q.put(("status","Simulación terminada."))

                time.sleep(1)

            except Exception as e:
                self.q.put(("status", f"⚠️ Error: {e}")); log_line("error","Loop",str(e)); time.sleep(1)

        self.q.put(("status","🛑 Bot detenido por usuario.")); log_line("status","Bot","Detenido")

    # ===== Helpers =====
    def countdown(self, title_prefix, seconds_total):
        for s in range(seconds_total,0,-1):
            msg=f"{title_prefix} {s}s…"
            self.q.put(("status", msg)); log_line("count","Cuenta regresiva",msg)
            time.sleep(1)

    def drain_queue(self):
        try:
            while True:
                k,v=self.q.get_nowait()
                if   k=="stake": self.var_stake.set(f"{v:.2f}")
                elif k=="ema9":  self.var_ema9.set("—" if v is None else f"{v:.6f}")
                elif k=="ema26": self.var_ema26.set("—" if v is None else f"{v:.6f}")
                elif k=="rsi":   self.var_rsi.set("—" if v is None else f"{v:.2f}")
                elif k=="analysis": self.var_analysis.set(v)
                elif k=="reco":     self.var_reco.set(v)
                elif k=="recovery": self.var_recovery.set(v)
                elif k=="balance_real": self.var_real.set("—" if v is None else f"{v:.2f}")
                elif k=="balance_practice": self.var_prac.set("—" if v is None else f"{v:.2f}")
                elif k=="status": self.var_status.set(v)
                elif k=="mode":   self.var_mode.set(v)
        except queue.Empty:
            pass
        self.after(100,self.drain_queue)

    # ===== Toggle slider =====
    def toggle_margin_ui(self):
        state["show_margin"] = bool(self.var_show_margin.get())
        save_config()
        try:
            if state["show_margin"]:
                parent = self.rowm.master
                self.rowm.pack(fill="x",padx=parent._padx,pady=(4,6))
            else:
                self.rowm.pack_forget()
        except Exception:
            pass

    # ===== Acciones =====
    def apply_asset(self):
        manual=self.var_manual.get().strip().upper()
        if manual:
            if manual.endswith("-OTC"):
                state["asset_base"] = manual[:-4]; state["asset_otc"]  = True
            else:
                state["asset_base"] = manual;       state["asset_otc"]  = False
            symbol = f"{state['asset_base']}{'-OTC' if state['asset_otc'] else ''}"
        else:
            base=self.var_base.get().strip().upper(); state["asset_base"]=base
            state["asset_otc"]=bool(self.var_otc.get()); symbol = f"{base}{'-OTC' if state['asset_otc'] else ''}"
        self.var_act_symbol.set(symbol); save_config()
        self.var_status.set(f"Activo cambiado a {symbol}. Ábrelo también en IQ Option."); log_line("status","Activo",symbol)

    def toggle_external(self):
        state["external_clicks"]=self.var_ext.get(); save_config()
        self.var_status.set("⚠ MODO CLIC EXTERNO ACTIVADO." if state["external_clicks"] else "Modo simulación (sin clic real).")
        log_line("status","External Clicks",str(state["external_clicks"]))

    def toggle_auto_new(self):
        state["auto_new_option"]=self.var_auto_new.get(); save_config()
        log_line("status","Auto ‘Nueva opción’",str(state["auto_new_option"]))

    def update_margin(self):
        try:
            m = float(self.var_margin.get())/100.0
            state["recovery_margin"] = max(0.0, min(0.30, m))
            save_config()
            cur_mode = (self.var_mode.get() or "PRACTICE")
            pool = stats[cur_mode]["loss_pool"]
            self.var_recovery.set(f"Pool={pool:.2f} · +{int(state['recovery_margin']*100)}% · StakeSug=…")
            self.var_status.set(f"Margen de recuperación: {int(state['recovery_margin']*100)}%")
        except Exception as e:
            self.var_status.set(f"Error ajustando margen: {e}")

    # Coordenadas
    def capture_xy(self,which):
        self.var_status.set(f"Coloca el mouse sobre {which.upper()}… Captura en 3s"); log_line("status","Captura",f"{which} en 3s")
        def cap():
            for s in (2,1):
                self.var_status.set(f"Capturando {which.upper()} en {s}s…"); time.sleep(1)
            import pyautogui
            pos=pyautogui.position()
            if which=="call":
                self.var_call_x.set(str(pos.x)); self.var_call_y.set(str(pos.y)); state["coords"]["call"]={"x":pos.x,"y":pos.y}
            elif which=="put":
                self.var_put_x.set(str(pos.x)); self.var_put_y.set(str(pos.y)); state["coords"]["put"]={"x":pos.x,"y":pos.y}
            else:
                self.var_new_x.set(str(pos.x)); self.var_new_y.set(str(pos.y)); state["coords"]["new"]={"x":pos.x,"y":pos.y}
            save_coords(); self.var_status.set(f"Capturado {which.upper()}: ({pos.x},{pos.y})"); log_line("status","Coord",f"{which}={pos.x},{pos.y}")
        threading.Thread(target=cap,daemon=True).start()

    def save_xy(self):
        try:
            state["coords"]["call"]={"x":int(self.var_call_x.get()),"y":int(self.var_call_y.get())}
            state["coords"]["put"] ={"x":int(self.var_put_x.get()), "y":int(self.var_put_y.get())}
            state["coords"]["new"] ={"x":int(self.var_new_x.get()), "y":int(self.var_new_y.get())}
            save_coords(); self.var_status.set("Coordenadas guardadas.")
        except Exception as e:
            self.var_status.set(f"Error guardando coords: {e}"); log_line("error","Guardar coords",str(e))

    def load_xy(self):
        load_coords()
        self.var_call_x.set(str(state["coords"]["call"]["x"])); self.var_call_y.set(str(state["coords"]["call"]["y"]))
        self.var_put_x.set(str(state["coords"]["put"]["x"]));   self.var_put_y.set(str(state["coords"]["put"]["y"]))
        self.var_new_x.set(str(state["coords"]["new"]["x"]));   self.var_new_y.set(str(state["coords"]["new"]["y"]))
        self.var_status.set("Coordenadas cargadas.")

    # Probar clics
    def test_call(self):
        if not state["external_clicks"]:
            self.var_status.set("Activa ‘Hacer clic externo’ para probar."); return
        self.var_status.set("Probando CALL en 0.6s…")
        self.after(600, lambda:(click_call(), self.var_status.set("CALL OK"), log_line("test","CALL",str(state["coords"]["call"]))))

    def test_put(self):
        if not state["external_clicks"]:
            self.var_status.set("Activa ‘Hacer clic externo’ para probar."); return
        self.var_status.set("Probando PUT en 0.6s…")
        self.after(600, lambda:(click_put(), self.var_status.set("PUT OK"), log_line("test","PUT",str(state["coords"]["put"]))))

    def test_new(self):
        if not state["external_clicks"]:
            self.var_status.set("Activa ‘Hacer clic externo’ para probar."); return
        self.var_status.set("Probando NUEVA OPCIÓN en 0.6s…")
        self.after(600, lambda:(click_new(), self.var_status.set("NUEVA OPCIÓN OK"), log_line("test","NUEVA OPCIÓN",str(state["coords"]["new"]))))

    # Modos / pausa / salir
    def to_practice(self):
        try:
            self.api.change_balance("PRACTICE")
            self.q.put(("mode","PRACTICE"))
            self.var_status.set("✅ Cambiado a PRACTICE"); log_line("mode","Cuenta","PRACTICE")
        except Exception as e:
            self.var_status.set(f"⚠ No se pudo cambiar: {e}"); log_line("error","Cambiar a PRACTICE",str(e))

    def to_real(self):
        try:
            self.api.change_balance("REAL")
            self.q.put(("mode","REAL"))
            self.var_status.set("✅ Cambiado a REAL"); log_line("mode","Cuenta","REAL")
        except Exception as e:
            self.var_status.set(f"⚠ No se pudo cambiar: {e}"); log_line("error","Cambiar a REAL",str(e))

    def toggle_pause(self):
        if self.pause_evt.is_set():
            self.pause_evt.clear(); self.var_status.set("▶ Reanudado"); log_line("status","Pausa","OFF")
        else:
            self.pause_evt.set(); self.var_status.set("⏸ Pausado"); log_line("status","Pausa","ON")

    def exit_all(self):
        self.stop_evt.set(); self.after(300,self.master.destroy)

    # ===== Resultado manual =====
    def mark_win(self):
        if self.pending["stake"] is None:
            self.var_status.set("No hay operación pendiente (clic externo)."); return
        self._apply_win(self.pending["stake"], self.pending["mode"])
        if hasattr(self, "tools") and self.tools:
            try: self.tools.after_result("WIN", self.pending["stake"], self.pending["mode"])
            except Exception as e: log_line("error","Plugin after_result", str(e))
        self.pending["stake"]=None; self.pending["mode"]=None

    def mark_loss(self):
        if self.pending["stake"] is None:
            self.var_status.set("No hay operación pendiente (clic externo)."); return
        self._apply_loss(self.pending["stake"], self.pending["mode"])
        if hasattr(self, "tools") and self.tools:
            try: self.tools.after_result("LOSS", self.pending["stake"], self.pending["mode"])
            except Exception as e: log_line("error","Plugin after_result", str(e))
        self.pending["stake"]=None; self.pending["mode"]=None

    def _apply_win(self, stake, mode):
        prof = stake * PAYOUT
        stats[mode]["won"] += prof
        stats[mode]["loss_pool"] = max(0.0, stats[mode]["loss_pool"] - prof)
        self.var_status.set(f"✅ WIN +{prof:.2f} — Pool {stats[mode]['loss_pool']:.2f}")
        log_line("win","Resultado",f"{mode} +{prof:.2f} | Pool {stats[mode]['loss_pool']:.2f}")

    def _apply_loss(self, stake, mode):
        stats[mode]["lost"] += stake
        stats[mode]["loss_pool"] += stake
        self.var_status.set(f"❌ LOSS -{stake:.2f} — Pool {stats[mode]['loss_pool']:.2f}")
        log_line("loss","Resultado",f"{mode} -{stake:.2f} | Pool {stats[mode]['loss_pool']:.2f}")
