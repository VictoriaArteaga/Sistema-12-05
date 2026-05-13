# ui/components/forms.py
import customtkinter as ctk
from ui.styles.theme import Theme

class FormInput(ctk.CTkFrame):
    def __init__(self, master, label_text, placeholder="", is_password=False, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.label = ctk.CTkLabel(
            self, text=label_text, 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Theme.TEXT_MUTED
        )
        self.label.pack(anchor="w", pady=(0, 5))
        
        self.entry = ctk.CTkEntry(
            self, placeholder_text=placeholder,
            height=40, corner_radius=8,
            border_color=Theme.SECONDARY,
            show="*" if is_password else ""
        )
        self.entry.pack(fill="x", expand=True)

    def get_value(self):
        return self.entry.get()

class PrimaryButton(ctk.CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(
            master, text=text, command=command,
            fg_color=Theme.PRIMARY, hover_color=Theme.PRIMARY_HOVER,
            height=45, corner_radius=8,
            font=ctk.CTkFont(size=15, weight="bold"),
            **kwargs
        )
