# ui/screens/recruiter_screen.py
import customtkinter as ctk
from ui.components.forms import FormInput, PrimaryButton
from ui.styles.theme import Theme

class RecruiterScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.label = ctk.CTkLabel(self, text="Recruitment Ecosystem 💠", font=ctk.CTkFont(size=32, weight="bold"))
        self.label.pack(pady=(0, 40), anchor="w")
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True)
        self.content.grid_columnconfigure((0, 1), weight=1)
        self.left = self._create_box(self.content, "🏢 Corporación", 0)
        FormInput(self.left, "Razón Social", "Ej. Horizon Tech").pack(fill="x", pady=10)
        FormInput(self.left, "Sede Central", "Ej. Madrid, ES").pack(fill="x", pady=10)
        PrimaryButton(self.left, "Registrar Entidad", lambda: None).pack(pady=(30, 0), fill="x")
        self.right = self._create_box(self.content, "⚡ Nueva Oferta", 1)
        FormInput(self.right, "Posición", "Ej. Lead Designer").pack(fill="x", pady=10)
        FormInput(self.right, "Compensación", "Ej. 80k - 100k").pack(fill="x", pady=10)
        PrimaryButton(self.right, "Lanzar al Mercado", lambda: None, fg_color=Theme.ACCENT).pack(pady=(30, 0), fill="x")

    def _create_box(self, master, title, col):
        frame = ctk.CTkFrame(master, fg_color=Theme.BG_CARD, corner_radius=25, padx=35, pady=35)
        frame.grid(row=0, column=col, padx=15, sticky="nsew")
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=20, weight="bold"), text_color=Theme.PRIMARY).pack(pady=(0, 20), anchor="w")
        return frame
