# ui/screens/candidate_screen.py
import customtkinter as ctk
from ui.components.forms import FormInput, PrimaryButton
from ui.styles.theme import Theme

class CandidateScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 30))
        self.label = ctk.CTkLabel(self.header, text="Mi Perfil Profesional 🚀", font=ctk.CTkFont(size=32, weight="bold"))
        self.label.pack(side="left")
        self.form_card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=20)
        self.form_card.pack(fill="x", pady=10, padx=2)
        self.inner_form = ctk.CTkFrame(self.form_card, fg_color="transparent", padx=40, pady=40)
        self.inner_form.pack(fill="x")
        self.name_input = FormInput(self.inner_form, "Nombre Completo", "Tu nombre...")
        self.name_input.pack(fill="x", pady=15)
        self.email_input = FormInput(self.inner_form, "Correo Personal", "usuario@correo.com")
        self.email_input.pack(fill="x", pady=15)
        self.skills_input = FormInput(self.inner_form, "Habilidades Clave", "Ej. Python, Design, Management")
        self.skills_input.pack(fill="x", pady=15)
        self.save_btn = PrimaryButton(self.inner_form, "Actualizar Mi Perfil ✨", self.save_profile)
        self.save_btn.pack(pady=(30, 0), fill="x")

    def save_profile(self):
        self.save_btn.configure(text="Procesando...", state="disabled")
        self.after(1000, self._show_success)

    def _show_success(self):
        self.save_btn.configure(text="¡Perfil Optimizado! ✅", fg_color=Theme.SUCCESS, state="normal")
        self.after(2000, lambda: self.save_btn.configure(text="Actualizar Mi Perfil ✨", fg_color=Theme.PRIMARY))
