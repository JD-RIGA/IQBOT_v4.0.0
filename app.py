import tkinter as tk
from core.state import load_coords, load_config
from ui.login_frame import LoginFrame
from ui.panel_frame import PanelFrame
from core.plugins import ToolManager
from core import ui_bridge

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IQ Option Bot — Clic Externo (Modular & Plugins)")
        self.configure(bg="#0e0e10")
        self.geometry("980x860")
        self.minsize(820, 640)

        load_coords()
        load_config()

        # REGISTRA el root ANTES de cargar plugins
        ui_bridge.set_root(self)

        # Cargar plugins (alerta_uso debe parchear core.clicks.*)
        self.tool_manager = ToolManager()
        self.tool_manager.load_from_config()

        self.current_frame = None
        self.show_login()

    def show_login(self):
        self.current_frame = LoginFrame(self, self.on_login_success)

    def on_login_success(self, api):
        self.current_frame.pack_forget()
        self.current_frame.destroy()
        self.current_frame = PanelFrame(self, api, self.tool_manager)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
