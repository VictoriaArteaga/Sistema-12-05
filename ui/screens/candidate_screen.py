# ui/screens/candidate_screen.py
import customtkinter as ctk
from ui.components.forms import FormInput, PrimaryButton
from ui.styles.theme import Theme
from services.user_service import UserService

class CandidateScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_service = UserService()
        
        # Título
        self.label = ctk.CTkLabel(
            self, text="Perfil del Candidato", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.label.pack(pady=(0, 20), anchor="w")

        # Formulario de Registro/Edición
        self.form_container = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, padx=30, pady=30)
        self.form_container.pack(fill="x", pady=10)

        self.name_input = FormInput(self.form_container, "Nombre Completo", "Ej. Juan Pérez")
        self.name_input.pack(fill="x", pady=10)

        self.email_input = FormInput(self.form_container, "Correo Electrónico", "juan@ejemplo.com")
        self.email_input.pack(fill="x", pady=10)

        self.skills_input = FormInput(self.form_container, "Habilidades (separadas por coma)", "Python, SQL, AWS")
        self.skills_input.pack(fill="x", pady=10)

        self.save_btn = PrimaryButton(self.form_container, "Guardar Perfil", self.save_profile)
        self.save_btn.pack(pady=(20, 0))

    def save_profile(self):
        name = self.name_input.get_value()
        email = self.email_input.get_value()
        skills = [s.strip() for s in self.skills_input.get_value().split(",")]

        if not name or not email:
            self.save_btn.configure(text="Faltan datos", fg_color=Theme.DANGER)
            self.after(2000, lambda: self.save_btn.configure(text="Guardar Perfil", fg_color=Theme.PRIMARY))
            return

        try:
            self.user_service.register_user(name, email, skills)
            print(f"Perfil guardado en JSON: {name}")
            self.save_btn.configure(text="¡Perfil Guardado!", fg_color=Theme.SUCCESS)
        except Exception as e:
            self.save_btn.configure(text="Error al guardar", fg_color=Theme.DANGER)
            print(f"Error: {e}")

        self.after(2000, lambda: self.save_btn.configure(text="Guardar Perfil", fg_color=Theme.PRIMARY))
