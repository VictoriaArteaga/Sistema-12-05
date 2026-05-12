# ui/screens/applications_screen.py
import customtkinter as ctk
from ui.styles.theme import Theme

class ApplicationsScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.label = ctk.CTkLabel(
            self, text="Mis Postulaciones", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.label.pack(pady=(0, 20), anchor="w")

        # Tabla simple simulada
        self.table_container = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12)
        self.table_container.pack(fill="both", expand=True, padx=2, pady=2)

        # Encabezados
        self.create_row("Puesto", "Empresa", "Fecha", "Estado", is_header=True)
        
        # Datos simulados
        self.create_row("Senior Python Developer", "TechNova", "12/05/2026", "En Revisión")
        self.create_row("UI/UX Designer", "Creative Studio", "10/05/2026", "Entrevista")
        self.create_row("Data Analyst", "Global Insight", "05/05/2026", "Rechazado")

    def create_row(self, pos, comp, date, status, is_header=False):
        font_style = ctk.CTkFont(size=13, weight="bold" if is_header else "normal")
        color = Theme.PRIMARY if is_header else Theme.TEXT_MAIN
        
        row_frame = ctk.CTkFrame(self.table_container, fg_color="transparent")
        row_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(row_frame, text=pos, font=font_style, text_color=color, width=200, anchor="w").pack(side="left")
        ctk.CTkLabel(row_frame, text=comp, font=font_style, text_color=color, width=150, anchor="w").pack(side="left")
        ctk.CTkLabel(row_frame, text=date, font=font_style, text_color=color, width=100, anchor="w").pack(side="left")
        
        status_label = ctk.CTkLabel(row_frame, text=status, font=font_style, text_color=color, width=100, anchor="w")
        status_label.pack(side="left")
        
        # Línea divisoria
        line = ctk.CTkFrame(self.table_container, height=1, fg_color=Theme.SECONDARY)
        line.pack(fill="x", padx=10)
