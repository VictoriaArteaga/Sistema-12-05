# ui/screens/main_window.py
import customtkinter as ctk
from ui.styles.theme import Theme
from ui.components.navbar import Navbar
from ui.screens.candidate_screen import CandidateScreen
from ui.screens.recruiter_screen import RecruiterScreen
from ui.screens.jobs_screen import JobsScreen
from ui.screens.applications_screen import ApplicationsScreen

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.title("JobConnect - Sistema de Gestión de Reclutamiento")
        self.geometry(f"{Theme.WINDOW_WIDTH}x{Theme.WINDOW_HEIGHT}")
        
        # Configuración del grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra de Navegación Lateral (Componente)
        self.navigation_frame = Navbar(
            self, 
            width=Theme.NAVBAR_WIDTH, 
            corner_radius=0,
            callbacks={
                'home': self.show_home,
                'candidate': self.show_candidates,
                'recruiter': self.show_recruiters,
                'jobs': self.show_jobs,
                'apps': self.show_applications
            }
        )
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        # Contenedor Principal
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.show_home()

    def show_home(self):
        self.clear_main_container()
        label = ctk.CTkLabel(
            self.main_container, 
            text="Bienvenido a JobConnect", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        label.pack(pady=40)
        
        info = ctk.CTkLabel(
            self.main_container, 
            text="Selecciona una opción en el menú lateral para comenzar.",
            font=ctk.CTkFont(size=16)
        )
        info.pack()

    def show_candidates(self):
        self.clear_main_container()
        screen = CandidateScreen(self.main_container)
        screen.pack(fill="both", expand=True)

    def show_recruiters(self):
        self.clear_main_container()
        screen = RecruiterScreen(self.main_container)
        screen.pack(fill="both", expand=True)

    def show_jobs(self):
        self.clear_main_container()
        screen = JobsScreen(self.main_container)
        screen.pack(fill="both", expand=True)

    def show_applications(self):
        self.clear_main_container()
        screen = ApplicationsScreen(self.main_container)
        screen.pack(fill="both", expand=True)

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
