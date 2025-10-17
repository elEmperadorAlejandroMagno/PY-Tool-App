import customtkinter as ctk
from typing import Dict, Any
from src.core.factories.translator_factory import create_translator_app
from src.gui.tabs import TextTranslatorTab, FileTranslatorTab

class TranslatorGUI:
    """Interfaz gráfica principal del traductor."""
    
    def __init__(self, lang: str = "en") -> None:
        """Inicializa la interfaz gráfica del traductor."""
        self.app = create_translator_app(lang)
        self.t: Dict[str, Any] = self.app.t
        self.entry_languages = [lang.upper() for lang in self.app.languages] + ["DETECT"]
        self.output_languages = [lang.upper() for lang in self.app.languages]
        
        # Configurar apariencia de CustomTkinter
        self._setup_appearance()
        
        # Crear ventana principal
        self._create_main_window()
        
        # Crear sistema de pestañas
        self._create_notebook()
        
        # Inicializar las pestañas
        self._setup_tabs()

    def _setup_appearance(self) -> None:
        """Configura la apariencia de CustomTkinter."""
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
    def _create_main_window(self) -> None:
        """Crea la ventana principal."""
        self.root: ctk.CTk = ctk.CTk()
        self.root.title(self.t["title"])
        self.root.geometry("900x700")
        
    def _create_notebook(self) -> None:
        """Crea el sistema de pestañas."""
        self.notebook = ctk.CTkTabview(self.root, width=850, height=650)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Agregar pestañas
        self.notebook.add(self.t["translate"])
        self.notebook.add(self.t["translate_file"])
        
    def _setup_tabs(self) -> None:
        """Inicializa y configura todas las pestañas."""
        # Obtener referencias a los frames de las pestañas
        text_tab_frame = self.notebook.tab(self.t["translate"])
        file_tab_frame = self.notebook.tab(self.t["translate_file"])
        
        # Crear e inicializar las pestañas
        self.text_tab = TextTranslatorTab(
            text_tab_frame, 
            self.app, 
            self.t, 
            self.entry_languages, 
            self.output_languages
        )
        self.text_tab.render()
        
        self.file_tab = FileTranslatorTab(
            file_tab_frame, 
            self.app, 
            self.t, 
            self.entry_languages, 
            self.output_languages
        )
        self.file_tab.render()

    def run(self) -> None:
        self.root.mainloop()
