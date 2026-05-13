# ui/components/navbar.py
import customtkinter as ctk
from ui.styles.theme import Theme

class Navbar(ctk.CTkFrame):
    def __init__(self, master, callbacks, **kwargs):
        super().__init__(master, **kwargs)
        
        self.callbacks = callbacks
        self.buttons = {}
        self.grid_rowconfigure(6, weight=1)

        # Header con "Icono"
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=30, sticky="ew")
        
        self.logo_label = ctk.CTkLabel(
            self.header_frame, text="💼", font=ctk.CTkFont(size=28)
        )
        self.logo_label.pack(side="left", padx=(0, 10))
        
        self.label = ctk.CTkLabel(
            self.header_frame, text="JobConnect", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.label.pack(side="left")

        # Botones con identificadores
        self.buttons['home'] = self._create_button("🏠  Inicio", 1, self.callbacks['home'])
        self.buttons['candidate'] = self._create_button("👤  Mi Perfil", 2, self.callbacks['candidate'])
        self.buttons['recruiter'] = self._create_button("🏢  Panel Empresa", 3, self.callbacks['recruiter'])
        self.buttons['jobs'] = self._create_button("🔍  Buscar Empleo", 4, self.callbacks['jobs'])
        self.buttons['apps'] = self._create_button("📑  Mis Postulaciones", 5, self.callbacks['apps'])

        self.set_active('home')

    def _create_button(self, text, row, command):
        btn = ctk.CTkButton(
            self, corner_radius=8, height=45, border_spacing=10, 
            text=text, fg_color="transparent", text_color=Theme.TEXT_MUTED,
            hover_color=Theme.BG_CARD, anchor="w", 
            font=ctk.CTkFont(size=14, weight="medium"),
            command=command
        )
        btn.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        return btn

    def set_active(self, button_key):
        # Resetear todos
        for key, btn in self.buttons.items():
            btn.configure(
                fg_color="transparent", 
                text_color=Theme.TEXT_MUTED,
                font=ctk.CTkFont(size=14, weight="medium")
            )
        
        # Activar el seleccionado
        if button_key in self.buttons:
            self.buttons[button_key].configure(
                fg_color=Theme.PRIMARY, 
                text_color="white",
                font=ctk.CTkFont(size=14, weight="bold")
            )
