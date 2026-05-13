# ui/components/navbar.py
import customtkinter as ctk
from ui.styles.theme import Theme

class Navbar(ctk.CTkFrame):
    def __init__(self, master, callbacks, **kwargs):
        super().__init__(master, **kwargs)
        self.callbacks = callbacks
        self.buttons = {}
        self.grid_rowconfigure(6, weight=1)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, padx=20, pady=40, sticky="ew")
        self.icon = ctk.CTkLabel(self.header, text="💠", font=ctk.CTkFont(size=30))
        self.icon.pack(side="left", padx=(0, 10))
        self.label = ctk.CTkLabel(self.header, text="JOBCONNECT", font=ctk.CTkFont(size=22, weight="bold"), text_color=Theme.PRIMARY)
        self.label.pack(side="left")
        self.buttons['home'] = self._create_btn("  Dashboard 🏠", 1, self.callbacks['home'])
        self.buttons['candidate'] = self._create_btn("  Mi Carrera 👤", 2, self.callbacks['candidate'])
        self.buttons['recruiter'] = self._create_btn("  Reclutamiento 🏢", 3, self.callbacks['recruiter'])
        self.buttons['jobs'] = self._create_btn("  Buscador 🔍", 4, self.callbacks['jobs'])
        self.buttons['apps'] = self._create_btn("  Historial 📑", 5, self.callbacks['apps'])

    def _create_btn(self, text, row, command):
        btn = ctk.CTkButton(self, corner_radius=15, height=55, border_spacing=10, text=text, fg_color="transparent", 
            text_color=Theme.TEXT_MUTED, hover_color=Theme.BG_CARD, anchor="w", font=ctk.CTkFont(size=16, weight="bold"), command=command)
        btn.grid(row=row, column=0, sticky="ew", padx=15, pady=8)
        return btn

    def set_active(self, key):
        for k, b in self.buttons.items(): b.configure(fg_color="transparent", text_color=Theme.TEXT_MUTED)
        if key in self.buttons: self.buttons[key].configure(fg_color=Theme.PRIMARY, text_color="white")
