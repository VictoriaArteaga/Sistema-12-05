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
            self, text="Panel de Reclutamiento", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.label.pack(pady=(0, 20), anchor="w")

        # Layout de dos columnas para hacerlo más intuitivo
        self.content_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.content_grid.pack(fill="both", expand=True)
        self.content_grid.grid_columnconfigure((0, 1), weight=1)

        # Columna 1: Registro de Empresa
        self.col_left = self._create_section(self.content_grid, "🏢 Registro de Empresa", 0)
        self.comp_name = FormInput(self.col_left, "Nombre de la Empresa", "Ej. Google")
        self.comp_name.pack(fill="x", pady=5)
        self.comp_email = FormInput(self.col_left, "Email de contacto", "hr@empresa.com")
        self.comp_email.pack(fill="x", pady=5)
        self.reg_btn = PrimaryButton(self.col_left, "Crear Perfil Empresa", self.register_company)
        self.reg_btn.pack(pady=(20, 0), fill="x")

        # Columna 2: Publicar Vacante
        self.col_right = self._create_section(self.content_grid, "📝 Publicar Nueva Vacante", 1)
        self.job_title = FormInput(self.col_right, "Título del Puesto", "Ej. Senior Python Dev")
        self.job_title.pack(fill="x", pady=5)
        self.job_salary = FormInput(self.col_right, "Salario (opcional)", "Ej. 5000")
        self.job_salary.pack(fill="x", pady=5)
        self.pub_btn = PrimaryButton(self.col_right, "Publicar Vacante Ahora", self.publish_job)
        self.pub_btn.pack(pady=(20, 0), fill="x")

    def _create_section(self, master, title, col):
        frame = ctk.CTkFrame(master, fg_color=Theme.BG_CARD, corner_radius=15, padx=20, pady=20)
        frame.grid(row=0, column=col, padx=10, sticky="nsew")
        
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=18, weight="bold"), text_color=Theme.PRIMARY).pack(pady=(0, 15), anchor="w")
        return frame

    def register_company(self):
        name = self.comp_name.get_value()
        email = self.comp_email.get_value()
        if not name or not email: return
        try:
            self.recruiter_service.create_recruiter(name, email)
            self.reg_btn.configure(text="✅ Empresa Registrada", fg_color=Theme.SUCCESS)
        except Exception as e:
            self.reg_btn.configure(text="❌ Error", fg_color=Theme.DANGER)
        self.after(2000, lambda: self.reg_btn.configure(text="Crear Perfil Empresa", fg_color=Theme.PRIMARY))

    def publish_job(self):
        # Simulación de publicación (requeriría un ID de reclutador real)
        title = self.job_title.get_value()
        if not title: return
        self.pub_btn.configure(text="🚀 Vacante Publicada", fg_color=Theme.SUCCESS)
        self.after(2000, lambda: self.pub_btn.configure(text="Publicar Vacante Ahora", fg_color=Theme.PRIMARY))
