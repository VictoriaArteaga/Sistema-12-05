# ui/screens/candidate_screen.py
import customtkinter as ctk
from ui.components.forms import FormInput, PrimaryButton
from ui.styles.theme import Theme

class CandidateScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
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
        # Aquí se llamaría al servicio (Persona 2) en el futuro
        print(f"Guardando perfil: {self.name_input.get_value()}")
        # Por ahora solo feedback visual
        self.save_btn.configure(text="¡Guardado!", fg_color=Theme.SUCCESS)
        self.after(2000, lambda: self.save_btn.configure(text="Guardar Perfil", fg_color=Theme.PRIMARY))
