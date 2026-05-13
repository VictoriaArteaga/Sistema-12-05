# ui/screens/jobs_screen.py
import customtkinter as ctk
from ui.components.cards import JobCard
from ui.styles.theme import Theme
from services.job_service import JobService

class JobsScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.job_service = JobService()
        
        # Título y Buscador
        self.header_container = ctk.CTkFrame(self, fg_color="transparent")
        self.header_container.pack(fill="x", pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.header_container, text="Explorar Vacantes", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(side="left")

        # Scrollable Frame para las vacantes
        self.scroll_container = ctk.CTkScrollableFrame(
            self, fg_color="transparent", 
            label_text="Vacantes Disponibles en tiempo real",
            label_font=ctk.CTkFont(size=14, weight="bold")
        )
        self.scroll_container.pack(fill="both", expand=True)

        self.load_jobs()

    def load_jobs(self):
        # Limpiar contenedor
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        try:
            jobs = self.job_service.get_all_jobs()
            if not jobs:
                label = ctk.CTkLabel(self.scroll_container, text="No hay vacantes disponibles aún.")
                label.pack(pady=20)
                return

            for job in jobs:
                card = JobCard(
                    self.scroll_container, 
                    title=job.title, 
                    company="Empresa Colaboradora", # Esto se podría expandir con el nombre real
                    salary=f"${job.salary}" if job.salary else "N/A", 
                    status=job.status
                )
                card.pack(fill="x", pady=10, padx=5)
        except Exception as e:
            print(f"Error al cargar vacantes: {e}")
