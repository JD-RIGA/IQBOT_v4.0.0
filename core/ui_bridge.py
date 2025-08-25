_root = None
_popup = None
_timer_var = None
_msg_var = None

def set_root(tk_root):
    global _root
    _root = tk_root

def _ensure_root():
    if _root is None:
        raise RuntimeError("ui_bridge: root de Tk no registrado. Llama a ui_bridge.set_root(root) al iniciar la app.")

def run_ui(fn, *args, **kwargs):
    _ensure_root()
    _root.after(0, lambda: fn(*args, **kwargs))

def alert_open(title="Alerta", message=""):
    from tkinter import Toplevel, Frame, Label, StringVar, Button
    global _popup, _timer_var, _msg_var
    if _popup is not None:
        return
    _ensure_root()
    def _create():
        from tkinter import Toplevel, Frame, Label, StringVar, Button
        global _popup, _timer_var, _msg_var
        _popup = Toplevel(_root)
        _popup.title(title)
        try:
            _popup.attributes("-topmost", True)
        except Exception:
            pass
        _popup.configure(bg="#151518")
        try:
            _popup.withdraw(); _popup.update_idletasks()
            w, h = 460, 160
            sw = _popup.winfo_screenwidth(); sh = _popup.winfo_screenheight()
            x = int((sw - w) / 2); y = int((sh - h) / 3)
            _popup.geometry(f"{w}x{h}+{x}+{y}"); _popup.deiconify()
        except Exception:
            pass
        frm = Frame(_popup, bg="#151518"); frm.pack(fill="both", expand=True, padx=16, pady=16)
        _msg_var = StringVar(value=message)
        Label(frm, textvariable=_msg_var, bg="#151518", fg="#FFD86B", font=("Segoe UI", 12, "bold"), wraplength=410, justify="center").pack(pady=(4,8))
        Label(frm, text="Cuenta atrás:", bg="#151518", fg="#e5e5e5", font=("Segoe UI", 10)).pack()
        _timer_var = StringVar(value="")
        Label(frm, textvariable=_timer_var, bg="#151518", fg="#9CDCFE", font=("Consolas", 20, "bold")).pack()
        Label(frm, text="No muevas el mouse durante la cuenta atrás.", bg="#151518", fg="#bdbdbd", font=("Segoe UI", 9)).pack(pady=(8,0))
        Button(frm, text="Cerrar aviso", command=alert_close, bg="#2a2a31", fg="#fff").pack(pady=(10,2))
    run_ui(_create)

def alert_set(message=None, seconds_left=None):
    def _update():
        global _popup, _timer_var, _msg_var
        if _popup is None: return
        if message is not None and _msg_var is not None: _msg_var.set(message)
        if seconds_left is not None and _timer_var is not None:
            try: _timer_var.set(str(int(seconds_left)))
            except Exception: _timer_var.set("")
    run_ui(_update)

def alert_close():
    def _destroy():
        global _popup, _timer_var, _msg_var
        if _popup is not None:
            try: _popup.destroy()
            except Exception: pass
        _popup = None; _timer_var = None; _msg_var = None
    run_ui(_destroy)
