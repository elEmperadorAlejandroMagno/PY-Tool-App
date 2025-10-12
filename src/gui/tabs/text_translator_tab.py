"""
Pestaña de traducción de texto.

Maneja la funcionalidad de traducir texto directo introducido por el usuario.
"""

from typing import Any, Dict
import customtkinter as ctk
from .tab_interface import TabInterface


class TextTranslatorTab(TabInterface):
    """Pestaña para traducir texto directo."""
    
    def __init__(self, parent_frame: ctk.CTkFrame, app: Any, t: Dict[str, Any], 
                 entry_languages: list, output_languages: list) -> None:
        """
        Inicializa la pestaña de traducción de texto.
        
        Args:
            parent_frame: Frame padre donde se renderizará
            app: Instancia de la aplicación principal
            t: Diccionario de traducciones
            entry_languages: Lista de idiomas de entrada
            output_languages: Lista de idiomas de salida
        """
        super().__init__(parent_frame, app, t)
        self.entry_languages = entry_languages
        self.output_languages = output_languages
        
        # Variables de interfaz
        self.entry_language_var: ctk.StringVar = None
        self.output_language_var: ctk.StringVar = None
        
        # Widgets
        self.entry_menu: ctk.CTkOptionMenu = None
        self.output_menu: ctk.CTkOptionMenu = None
        self.entry: ctk.CTkTextbox = None
        self.result_textbox: ctk.CTkTextbox = None
        self.btn_translate: ctk.CTkButton = None
        
    def render(self) -> None:
        """Renderiza el contenido de la pestaña de traducción de texto."""
        self.content_frame = self.create_content_frame()
        
        self._create_language_selection()
        self._create_input_section()
        self._create_translate_button()
        self._create_result_section()
        
    def _create_language_selection(self) -> None:
        """Crea la sección de selección de idiomas."""
        # Idioma de entrada
        entry_label = self.create_label(
            self.content_frame, 
            self.t["select_language_from"]
        )
        entry_label.pack(pady=(10, 5))
        
        self.entry_language_var = ctk.StringVar(value="DETECT")
        self.entry_menu = self.create_language_menu(
            self.content_frame,
            self.entry_languages,
            self.entry_language_var,
            self.set_entry_language
        )
        self.entry_menu.pack(pady=5)
        
        # Idioma de salida
        output_label = self.create_label(
            self.content_frame,
            self.t["select_language_to"]
        )
        output_label.pack(pady=(15, 5))
        
        self.output_language_var = ctk.StringVar(value=self.app.lang.upper())
        self.output_menu = self.create_language_menu(
            self.content_frame,
            self.output_languages,
            self.output_language_var,
            self.set_output_language
        )
        self.output_menu.pack(pady=5)
        
    def _create_input_section(self) -> None:
        """Crea la sección de entrada de texto."""
        input_label = self.create_label(
            self.content_frame,
            "Text to translate:"
        )
        input_label.pack(pady=(20, 5))
        
        self.entry = self.create_textbox(self.content_frame)
        self.entry.pack(pady=5)
        
    def _create_translate_button(self) -> None:
        """Crea el botón de traducir."""
        self.btn_translate = self.create_button(
            self.content_frame,
            self.t["translate"],
            self.translate_text
        )
        self.btn_translate.pack(pady=15)
        
    def _create_result_section(self) -> None:
        """Crea la sección de resultados."""
        result_label = self.create_label(
            self.content_frame,
            "Translation result:"
        )
        result_label.pack(pady=(10, 5))
        
        self.result_textbox = self.create_textbox(self.content_frame)
        self.result_textbox.pack(pady=5)
        
    def translate_text(self) -> None:
        """Traduce el texto introducido por el usuario."""
        self._disable_translate_btn()
        
        try:
            text: str = self.entry.get("1.0", "end").strip()
            if not text:
                return
                
            result = self.app.translate_text(text)
            
            # Limpiar y mostrar resultado
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("1.0", result.text)
            
        except Exception as e:
            # Manejar errores si es necesario
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("1.0", f"Error: {str(e)}")
        finally:
            self._enable_translate_btn()
            
    def set_entry_language(self, lang: str) -> None:
        """
        Establece el idioma de entrada.
        
        Args:
            lang: Código del idioma en mayúsculas
        """
        self.app.entry_language = lang.lower()
        
    def set_output_language(self, lang: str) -> None:
        """
        Establece el idioma de salida.
        
        Args:
            lang: Código del idioma en mayúsculas
        """
        self.app.output_language = lang.lower()
        
    def _disable_translate_btn(self) -> None:
        """Deshabilita el botón de traducir durante el proceso."""
        self.btn_translate.configure(state="disabled", text="Translating...")
        self.parent_frame.master.update_idletasks()
        
    def _enable_translate_btn(self) -> None:
        """Rehabilita el botón de traducir."""
        self.btn_translate.configure(state="normal", text=self.t["translate"])
        self.parent_frame.master.update_idletasks()