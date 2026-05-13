# ui/components/navbar.py
import customtkinter as ctk

class Navbar(ctk.CTkFrame):
    def __init__(self, master, callbacks, **kwargs):
        super().__init__(master, **kwargs)
        
        self.callbacks = callbacks
        self.grid_rowconfigure(4, weight=1)

        self.label = ctk.CTkLabel(
            self, text="JobConnect", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.btn_home = self._create_button("Inicio", 1, self.callbacks['home'])
        self.btn_candidate = self._create_button("Perfil Candidato", 2, self.callbacks['candidate'])
        self.btn_recruiter = self._create_button("Panel Reclutador", 3, self.callbacks['recruiter'])
        self.btn_jobs = self._create_button("Explorar Vacantes", 4, self.callbacks['jobs'])
        self.btn_apps = self._create_button("Mis Postulaciones", 5, self.callbacks['apps'])

    def _create_button(self, text, row, command):
        btn = ctk.CTkButton(
            self, corner_radius=0, height=40, border_spacing=10, 
            text=text, fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"), anchor="w", command=command
        )
        btn.grid(row=row, column=0, sticky="ew")
        return btn
