import os, json, tkinter as tk
from tkinter import messagebox
from iqoptionapi.stable_api import IQ_Option
from core.state import SESSION_FILE
from core.logger import log_line

class LoginFrame(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, bg="#0e0e10")
        self.master=master; self.on_success=on_success; self.api=None
        self.pack(fill="both", expand=True)
        self.build()

    def build(self):
        tk.Label(self,text="Inicia sesión en IQ Option",bg="#0e0e10",fg="#e5e5e5",font=("Segoe UI",16,"bold")).pack(pady=(26,10))
        card=tk.Frame(self,bg="#151518",highlightthickness=1,highlightbackground="#222228"); card.pack(padx=22,pady=10,fill="x")
        inner=tk.Frame(card,bg="#151518"); inner.pack(padx=16,pady=16,fill="x")
        lbl=dict(bg="#151518",fg="#e5e5e5",font=("Segoe UI",11),width=18,anchor="e")
        ent=dict(bg="#1c1c21",fg="#e5e5e5",insertbackground="#e5e5e5",relief="flat",highlightthickness=1,highlightbackground="#2a2a31",font=("Segoe UI",11),width=28)
        tk.Label(inner,text="Usuario (email):",**lbl).grid(row=0,column=0,padx=(0,10),pady=6,sticky="e")
        self.user_entry=tk.Entry(inner,**ent); self.user_entry.grid(row=0,column=1,pady=6,sticky="w")
        tk.Label(inner,text="Contraseña:",**lbl).grid(row=1,column=0,padx=(0,10),pady=6,sticky="e")
        self.pass_entry=tk.Entry(inner,show="*",**ent); self.pass_entry.grid(row=1,column=1,pady=6,sticky="w")
        self.btn=tk.Button(self,text="Conectar",command=self.conectar,bg="#FFD86B",fg="#1b1b1b",activebackground="#F2C85B",
                           relief="flat",font=("Segoe UI",12,"bold"),padx=16,pady=8,cursor="hand2"); self.btn.pack(pady=12)
        if os.path.exists(SESSION_FILE):
            try:
                d=json.load(open(SESSION_FILE,"r",encoding="utf-8"))
                self.user_entry.insert(0,d.get("usuario","")); self.pass_entry.insert(0,d.get("password",""))
            except: pass

    def conectar(self):
        u=self.user_entry.get().strip(); p=self.pass_entry.get().strip()
        if not u or not p:
            messagebox.showwarning("Datos incompletos","Ingresa usuario y contraseña"); return
        self.btn.config(state="disabled",text="Conectando…"); self.update_idletasks()
        try:
            self.api=IQ_Option(u,p); ok,msg=self.api.connect()
        except Exception as e:
            ok, msg = False, str(e)
        if ok and self.api.check_connect():
            try: json.dump({"usuario":u,"password":p},open(SESSION_FILE,"w",encoding="utf-8"))
            except: pass
            log_line("status","Login","Conectado"); self.on_success(self.api); self.destroy()
        else:
            self.btn.config(state="normal",text="Conectar"); log_line("error","Login",msg)
            messagebox.showerror("Error", f"No se pudo conectar: {msg}")
