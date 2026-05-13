# ui/components/cards.py
import customtkinter as ctk
from ui.styles.theme import Theme
from ui.components.forms import PrimaryButton

class JobCard(ctk.CTkFrame):
    def __init__(self, master, title, company, salary, status, **kwargs):
        super().__init__(master, fg_color=Theme.BG_CARD, corner_radius=12, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        # Título del Puesto
        self.title_label = ctk.CTkLabel(
            self, text=title, 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=Theme.PRIMARY
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")
        
        # Empresa
        self.company_label = ctk.CTkLabel(
            self, text=company, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Theme.TEXT_MAIN
        )
        self.company_label.grid(row=1, column=0, padx=20, pady=0, sticky="w")
        
        # Detalles (Salario y Estado)
        self.details_label = ctk.CTkLabel(
            self, text=f"💰 {salary}  •  Status: {status}", 
            font=ctk.CTkFont(size=12),
            text_color=Theme.TEXT_MUTED
        )
        self.details_label.grid(row=2, column=0, padx=20, pady=(5, 15), sticky="w")
        
        # Botón de Aplicar
        self.apply_btn = PrimaryButton(
            self, text="Aplicar Ahora", 
            command=self.on_apply,
            height=32, width=120
        )
        self.apply_btn.grid(row=0, column=1, rowspan=3, padx=20, pady=20)

    def on_apply(self):
        self.apply_btn.configure(text="Aplicando...", state="disabled", fg_color=Theme.SECONDARY)
        # Feedback simulado
        self.after(1500, lambda: self.apply_btn.configure(text="¡Postulado!", fg_color=Theme.SUCCESS))
