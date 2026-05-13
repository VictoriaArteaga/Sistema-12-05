# ui/screens/jobs_screen.py
import customtkinter as ctk
from ui.components.cards import JobCard
from ui.styles.theme import Theme
from services.job_service import JobService

class JobsScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.job_service = JobService()
        
        # Título y Buscador (Header más intuitivo)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.header, text="🔍 Explorar Vacantes", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(side="left")

        # Barra de búsqueda integrada
        self.search_entry = ctk.CTkEntry(
            self.header, placeholder_text="Buscar por cargo o empresa...",
            width=300, height=40, corner_radius=10
        )
        self.search_entry.pack(side="right", padx=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_jobs(self.search_entry.get()))

        # Contenedor de vacantes
        self.scroll_container = ctk.CTkScrollableFrame(
            self, fg_color="transparent", 
            label_text="Resultados de búsqueda",
            label_font=ctk.CTkFont(size=14, weight="bold")
        )
        self.scroll_container.pack(fill="both", expand=True)

        self.load_jobs()

    def load_jobs(self, query=""):
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        try:
            if query:
                jobs = self.job_service.search_jobs(query)
            else:
                jobs = self.job_service.get_all_jobs()

            if not jobs:
                label = ctk.CTkLabel(self.scroll_container, text="No se encontraron vacantes.", pady=20)
                label.pack()
                return

            for job in jobs:
                card = JobCard(
                    self.scroll_container, 
                    title=f"🚀 {job.title}", 
                    company="Empresa Verificada", 
                    salary=f"${job.salary}" if job.salary else "A convenir", 
                    status=job.status.upper()
                )
                card.pack(fill="x", pady=8, padx=5)
        except Exception as e:
            print(f"Error: {e}")
