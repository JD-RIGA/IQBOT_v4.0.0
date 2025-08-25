import tkinter as tk
import platform

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

        self._bind_mousewheel(self.canvas)

    def _on_inner_config(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_config(self, event):
        self.canvas.itemconfig(self.win, width=event.width)

    def _bind_mousewheel(self, widget):
        osname = platform.system()
        if osname in ("Windows", "Darwin"):
            widget.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            widget.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
            widget.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll( 1, "units"))

    def _on_mousewheel(self, event):
        delta = int(-1*(event.delta/120))
        self.canvas.yview_scroll(delta, "units")
