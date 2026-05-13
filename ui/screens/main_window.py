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

        self.title("JobConnect - Sistema de Gestión de Reclutamiento")
        self.geometry(f"{Theme.WINDOW_WIDTH}x{Theme.WINDOW_HEIGHT}")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigation_frame = Navbar(
            self, 
            width=Theme.NAVBAR_WIDTH, 
            corner_radius=0,
            callbacks={
                'home': lambda: self.navigate('home'),
                'candidate': lambda: self.navigate('candidate'),
                'recruiter': lambda: self.navigate('recruiter'),
                'jobs': lambda: self.navigate('jobs'),
                'apps': lambda: self.navigate('apps')
            }
        )
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        self.navigate('home')

    def navigate(self, screen_name):
        self.clear_main_container()
        self.navigation_frame.set_active(screen_name)
        
        if screen_name == 'home':
            self.show_home()
        elif screen_name == 'candidate':
            CandidateScreen(self.main_container).pack(fill="both", expand=True)
        elif screen_name == 'recruiter':
            RecruiterScreen(self.main_container).pack(fill="both", expand=True)
        elif screen_name == 'jobs':
            JobsScreen(self.main_container).pack(fill="both", expand=True)
        elif screen_name == 'apps':
            ApplicationsScreen(self.main_container).pack(fill="both", expand=True)

    def show_home(self):
        home_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        home_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            home_frame, text="Bienvenido de nuevo 👋", 
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(pady=(40, 10), anchor="w")
        
        ctk.CTkLabel(
            home_frame, text="Este es tu resumen de hoy en JobConnect.",
            font=ctk.CTkFont(size=16), text_color=Theme.TEXT_MUTED
        ).pack(anchor="w", pady=(0, 40))

        # Grid de "Cards" de Resumen (Dashboard intuitivo)
        stats_frame = ctk.CTkFrame(home_frame, fg_color="transparent")
        stats_frame.pack(fill="x")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self._create_stat_card(stats_frame, "Vacantes Activas", "12", 0)
        self._create_stat_card(stats_frame, "Mis Postulaciones", "5", 1)
        self._create_stat_card(stats_frame, "Mensajes", "3", 2)

    def _create_stat_card(self, master, title, value, col):
        card = ctk.CTkFrame(master, fg_color=Theme.BG_CARD, corner_radius=15, height=150)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        card.grid_propagate(False)
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color=Theme.TEXT_MUTED).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=36, weight="bold")).pack()

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
        self.update_idletasks()
