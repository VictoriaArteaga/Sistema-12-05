# ui/screens/jobs_screen.py
import customtkinter as ctk
from ui.components.cards import JobCard
from ui.styles.theme import Theme

class JobsScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Título y Buscador
        self.header_container = ctk.CTkFrame(self, fg_color="transparent")
        self.header_container.pack(fill="x", pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.header_container, text="Explorar Vacantes", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(side="left")

        self.search_entry = ctk.CTkEntry(
            self.header_container, placeholder_text="Buscar por cargo o empresa...",
            width=300, height=35
        )
        self.search_entry.pack(side="right", padx=10)

        # Scrollable Frame para las vacantes
        self.scroll_container = ctk.CTkScrollableFrame(
            self, fg_color="transparent", 
            label_text="Vacantes Disponibles",
            label_font=ctk.CTkFont(size=14, weight="bold")
        )
        self.scroll_container.pack(fill="both", expand=True)

        # Ejemplo de vacantes (Mock data)
        self.mock_jobs = [
            {"title": "Senior Python Developer", "company": "TechNova Solutions", "salary": "$4,500", "status": "Abierta"},
            {"title": "Data Analyst", "company": "Global Insight", "salary": "$3,200", "status": "Abierta"},
            {"title": "UI/UX Designer", "company": "Creative Studio", "salary": "$3,800", "status": "Urgente"},
            {"title": "DevOps Engineer", "company": "Cloud Systems", "salary": "$5,000", "status": "Abierta"},
        ]

        for job in self.mock_jobs:
            card = JobCard(
                self.scroll_container, 
                title=job["title"], 
                company=job["company"], 
                salary=job["salary"], 
                status=job["status"]
            )
            card.pack(fill="x", pady=10, padx=5)
