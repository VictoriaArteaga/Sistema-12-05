# main.py
import customtkinter as ctk
from ui.screens.main_window import MainWindow

def main():
    # Configuración de apariencia global
    ctk.set_appearance_mode("dark")  # Modos: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Temas: "blue" (standard), "green", "dark-blue"

    # Inicialización de la ventana principal
    app = MainWindow()
    
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\nAplicación cerrada por el usuario.")

if __name__ == "__main__":
    main()
