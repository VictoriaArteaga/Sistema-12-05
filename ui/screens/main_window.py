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
        self.title("JobConnect Pro | Ecosystem")
        self.geometry(f"{Theme.WINDOW_WIDTH}x{Theme.WINDOW_HEIGHT}")
        self.configure(fg_color=Theme.BG_DARK)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.navigation_frame = Navbar(self, width=Theme.NAVBAR_WIDTH, fg_color=Theme.BG_NAV,
            callbacks={
                'home': lambda: self.navigate('home'),
                'candidate': lambda: self.navigate('candidate'),
                'recruiter': lambda: self.navigate('recruiter'),
                'jobs': lambda: self.navigate('jobs'),
                'apps': lambda: self.navigate('apps')
            }
        )
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.main_container = ctk.CTkFrame(self, corner_radius=25, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.navigate('home')

    def navigate(self, screen_name):
        self.clear_main_container()
        self.navigation_frame.set_active(screen_name)
        if screen_name == 'home': self.show_home()
        elif screen_name == 'candidate': CandidateScreen(self.main_container).pack(fill="both", expand=True)
        elif screen_name == 'recruiter': RecruiterScreen(self.main_container).pack(fill="both", expand=True)
        elif screen_name == 'jobs': JobsScreen(self.main_container).pack(fill="both", expand=True)
        elif screen_name == 'apps': ApplicationsScreen(self.main_container).pack(fill="both", expand=True)

    def show_home(self):
        home_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        home_frame.pack(fill="both", expand=True)
        ctk.CTkLabel(home_frame, text="El futuro del trabajo está aquí ⚡", 
            font=ctk.CTkFont(size=48, weight="bold"), text_color=Theme.PRIMARY).pack(pady=(80, 10), anchor="w")
        ctk.CTkLabel(home_frame, text="Gestiona tu carrera profesional con la plataforma más avanzada.",
            font=ctk.CTkFont(size=20), text_color=Theme.TEXT_MUTED).pack(anchor="w", pady=(0, 60))
        stats_frame = ctk.CTkFrame(home_frame, fg_color="transparent")
        stats_frame.pack(fill="x")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self._create_stat_card(stats_frame, "Oportunidades", "2,412", 0, "🎯", Theme.PRIMARY)
        self._create_stat_card(stats_frame, "Postulaciones", "14", 1, "📩", Theme.SECONDARY)
        self._create_stat_card(stats_frame, "Impacto", "+85%", 2, "📈", Theme.ACCENT)

    def _create_stat_card(self, master, title, value, col, icon, color):
        card = ctk.CTkFrame(master, fg_color=Theme.BG_CARD, corner_radius=25, height=220)
        card.grid(row=0, column=col, padx=15, sticky="nsew")
        card.grid_propagate(False)
        ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=40)).pack(pady=(35, 10))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=38, weight="bold"), text_color=color).pack()
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16), text_color=Theme.TEXT_MUTED).pack(pady=5)

    def clear_main_container(self):
        for widget in self.main_container.winfo_children(): widget.destroy()
        self.update_idletasks()
