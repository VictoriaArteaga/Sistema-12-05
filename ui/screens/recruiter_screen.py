# ui/screens/recruiter_screen.py
import customtkinter as ctk
from ui.components.forms import FormInput, PrimaryButton
from ui.styles.theme import Theme
from services.recruiter_service import RecruiterService

class RecruiterScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.recruiter_service = RecruiterService()
        
        # Título
        self.label = ctk.CTkLabel(
            self, text="Panel del Reclutador", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.label.pack(pady=(0, 20), anchor="w")

        # Contenedor de Registro de Empresa
        self.company_label = ctk.CTkLabel(
            self, text="Registrar Empresa", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=Theme.PRIMARY
        )
        self.company_label.pack(pady=(10, 5), anchor="w")

        self.company_card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12)
        self.company_card.pack(fill="x", pady=(0, 20), padx=30)

        self.comp_name = FormInput(self.company_card, "Nombre de la Empresa", "Ej. Tech Corp")
        self.comp_name.pack(fill="x", pady=5)
        
        self.comp_email = FormInput(self.company_card, "Email Corporativo", "hr@techcorp.com")
        self.comp_email.pack(fill="x", pady=5)

        self.reg_btn = PrimaryButton(self.company_card, "Registrar Empresa", self.register_company)
        self.reg_btn.pack(pady=(10, 0))

    def register_company(self):
        name = self.comp_name.get_value()
        email = self.comp_email.get_value()
        
        if not name or not email:
            return

        try:
            self.recruiter_service.create_recruiter(name, email)
            self.reg_btn.configure(text="¡Registrada!", fg_color=Theme.SUCCESS)
        except Exception as e:
            print(f"Error: {e}")
            self.reg_btn.configure(text="Error", fg_color=Theme.DANGER)
            
        self.after(2000, lambda: self.reg_btn.configure(text="Registrar Empresa", fg_color=Theme.PRIMARY))
