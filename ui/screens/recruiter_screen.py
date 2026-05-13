# ui/screens/recruiter_screen.py
import customtkinter as ctk
from ui.components.forms import FormInput, PrimaryButton
from ui.styles.theme import Theme

class RecruiterScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Título
        self.label = ctk.CTkLabel(
            self, text="Panel del Reclutador", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.label.pack(pady=(0, 20), anchor="w")

        # Contenedor de Acciones Rápidas
        self.actions_container = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_container.pack(fill="x", pady=10)

        # Formulario para Nueva Vacante
        self.form_label = ctk.CTkLabel(
            self.actions_container, text="Publicar Nueva Vacante", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=Theme.PRIMARY
        )
        self.form_label.pack(pady=(10, 5), anchor="w")

        self.form_card = ctk.CTkFrame(self.actions_container, fg_color=Theme.BG_CARD, corner_radius=12, padx=30, pady=30)
        self.form_card.pack(fill="x")

        self.job_title = FormInput(self.form_card, "Título de la Vacante", "Ej. Desarrollador Senior Python")
        self.job_title.pack(fill="x", pady=10)

        self.salary = FormInput(self.form_card, "Rango Salarial", "Ej. $3000 - $5000")
        self.salary.pack(fill="x", pady=10)

        self.publish_btn = PrimaryButton(self.form_card, "Publicar Vacante", self.publish_job)
        self.publish_btn.pack(pady=(20, 0))

    def publish_job(self):
        print(f"Publicando vacante: {self.job_title.get_value()}")
        self.publish_btn.configure(text="¡Publicada!", fg_color=Theme.SUCCESS)
        self.after(2000, lambda: self.publish_btn.configure(text="Publicar Vacante", fg_color=Theme.PRIMARY))
