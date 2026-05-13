# ui/screens/applications_screen.py
import customtkinter as ctk
from ui.styles.theme import Theme
from services.application_service import ApplicationService

class ApplicationsScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app_service = ApplicationService()
        
        self.label = ctk.CTkLabel(
            self, text="Mis Postulaciones", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.label.pack(pady=(0, 20), anchor="w")

        # Tabla simple simulada
        self.table_container = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12)
        self.table_container.pack(fill="both", expand=True, padx=2, pady=2)

        # Encabezados
        self.create_row("Puesto (ID)", "Candidato (ID)", "Estado", is_header=True)
        
        self.load_applications()

    def load_applications(self):
        try:
            apps = self.app_service.get_all_applications()
            if not apps:
                ctk.CTkLabel(self.table_container, text="No has aplicado a ninguna vacante aún.", pady=20).pack()
                return

            for app in apps:
                # Usamos IDs ya que no tenemos nombres vinculados directamente en el JSON sin más lógica
                self.create_row(app.job_id[:8], app.candidate_id[:8], app.status)
        except Exception as e:
            print(f"Error al cargar aplicaciones: {e}")

    def create_row(self, col1, col2, status, is_header=False):
        font_style = ctk.CTkFont(size=13, weight="bold" if is_header else "normal")
        color = Theme.PRIMARY if is_header else Theme.TEXT_MAIN
        
        row_frame = ctk.CTkFrame(self.table_container, fg_color="transparent")
        row_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(row_frame, text=col1, font=font_style, text_color=color, width=200, anchor="w").pack(side="left")
        ctk.CTkLabel(row_frame, text=col2, font=font_style, text_color=color, width=150, anchor="w").pack(side="left")
        
        status_label = ctk.CTkLabel(row_frame, text=status, font=font_style, text_color=color, width=100, anchor="w")
        status_label.pack(side="left")
        
        # Línea divisoria
        line = ctk.CTkFrame(self.table_container, height=1, fg_color=Theme.SECONDARY)
        line.pack(fill="x", padx=10)
