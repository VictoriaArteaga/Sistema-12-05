# ui/screens/jobs_screen.py
import customtkinter as ctk
from ui.components.cards import JobCard
from ui.styles.theme import Theme

class JobsScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 30))
        self.title = ctk.CTkLabel(self.header, text="Explorador de Talento 🔍", font=ctk.CTkFont(size=32, weight="bold"))
        self.title.pack(side="left")
        self.search = ctk.CTkEntry(self.header, placeholder_text="Filtrar por tecnología...", width=350, height=50, corner_radius=15, border_width=2, border_color=Theme.BG_CARD)
        self.search.pack(side="right")
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text="OPORTUNIDADES DESTACADAS", label_font=ctk.CTkFont(size=14, weight="bold"), label_text_color=Theme.ACCENT)
        self.scroll.pack(fill="both", expand=True)
        self._add_mock_jobs()

    def _add_mock_jobs(self):
        jobs = [("Creative Director", "Design Hub", "120k", "URGENTE"), ("Senior Fullstack", "TechFlow", "95k", "DESTACADO"), ("AI Engineer", "NeuralLab", "150k", "NUEVO")]
        for t, c, s, st in jobs:
            card = JobCard(self.scroll, title=t, company=c, salary=s, status=st)
            card.pack(fill="x", pady=10, padx=10)
