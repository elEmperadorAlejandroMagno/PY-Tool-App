"""
Pestaña de traducción de archivos.

Maneja la funcionalidad de traducir archivos (txt, pdf, docx) seleccionados por el usuario.
"""

from typing import Any, Dict, Optional
import customtkinter as ctk
from tkinter import filedialog, messagebox
from .tab_interface import TabInterface


class FileTranslatorTab(TabInterface):
    """Pestaña para traducir archivos."""
    
    def __init__(self, parent_frame: ctk.CTkFrame, app: Any, t: Dict[str, Any], 
                 entry_languages: list, output_languages: list) -> None:
        """
        Inicializa la pestaña de traducción de archivos.
        
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
        self.file_path: Optional[str] = None
        
        # Variables de interfaz
        self.entry_language_var_file: ctk.StringVar = None
        self.output_language_var_file: ctk.StringVar = None
        
        # Widgets
        self.entry_menu_file: ctk.CTkOptionMenu = None
        self.output_menu_file: ctk.CTkOptionMenu = None
        self.btn_file: ctk.CTkButton = None
        self.btn_translate_file: ctk.CTkButton = None
        
    def render(self) -> None:
        """Renderiza el contenido de la pestaña de traducción de archivos."""
        self.content_frame = self.create_content_frame()
        
        self._create_language_selection()
        self._create_file_selection()
        
    def _create_language_selection(self) -> None:
        """Crea la sección de selección de idiomas."""
        # Idioma de entrada
        entry_label = self.create_label(
            self.content_frame, 
            self.t["select_language_from"]
        )
        entry_label.pack(pady=(10, 5))
        
        self.entry_language_var_file = ctk.StringVar(value="DETECT")
        self.entry_menu_file = self.create_language_menu(
            self.content_frame,
            self.entry_languages,
            self.entry_language_var_file,
            self.set_entry_language_file
        )
        self.entry_menu_file.pack(pady=5)
        
        # Idioma de salida
        output_label = self.create_label(
            self.content_frame,
            self.t["select_language_to"]
        )
        output_label.pack(pady=(15, 5))
        
        self.output_language_var_file = ctk.StringVar(value=self.app.lang.upper())
        self.output_menu_file = self.create_language_menu(
            self.content_frame,
            self.output_languages,
            self.output_language_var_file,
            self.set_output_language_file
        )
        self.output_menu_file.pack(pady=5)
        
    def _create_file_selection(self) -> None:
        """Crea la sección de selección de archivos."""
        file_label = self.create_label(
            self.content_frame,
            "File Selection:"
        )
        file_label.pack(pady=(30, 10))
        
        # Botón para seleccionar archivo
        self.btn_file = self.create_button(
            self.content_frame,
            self.t["select_file"],
            self.get_file_path,
            width=250
        )
        self.btn_file.pack(pady=10)
        
        # Botón para traducir archivo
        self.btn_translate_file = self.create_button(
            self.content_frame,
            self.t["translate_file"],
            self.translate_file,
            width=250
        )
        self.btn_translate_file.configure(state="disabled")
        self.btn_translate_file.pack(pady=10)
        
    def get_file_path(self) -> None:
        """Abre el diálogo para seleccionar un archivo."""
        self.file_path = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=[
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("Word files", "*.docx"),
                ("All files", "*.*")
            ]
        )
        
        if self.file_path:
            self._enable_file_button()
        else:
            messagebox.showwarning(
                "No file selected", 
                "Please select a file to translate."
            )
            
    def translate_file(self) -> None:
        """Traduce el archivo seleccionado."""
        if not self.file_path:
            messagebox.showwarning(
                "No file selected", 
                "Please select a file to translate."
            )
            return
            
        self._disable_translate_btn()
        
        try:
            result: str = self.app.translate_file(self.file_path)
            messagebox.showinfo(self.t["translation"], result)
        except Exception as e:
            error_msg = f"Error translating file: {e}"
            messagebox.showerror("Error", error_msg)
        finally:
            self._enable_translate_btn()
            
    def set_entry_language_file(self, lang: str) -> None:
        """
        Establece el idioma de entrada para archivos.
        
        Args:
            lang: Código del idioma en mayúsculas
        """
        self.app.entry_language = lang.lower()
        
    def set_output_language_file(self, lang: str) -> None:
        """
        Establece el idioma de salida para archivos.
        
        Args:
            lang: Código del idioma en mayúsculas
        """
        self.app.output_language = lang.lower()
        
    def _enable_file_button(self) -> None:
        """Habilita el botón de traducir archivo cuando se selecciona un archivo."""
        if self.file_path:
            self.btn_translate_file.configure(state="normal")
            # Mostrar solo el nombre del archivo en el botón
            filename = self.file_path.split("/")[-1]
            self.btn_file.configure(text=filename)
            
    def _disable_translate_btn(self) -> None:
        """Deshabilita el botón de traducir durante el proceso."""
        self.btn_translate_file.configure(state="disabled", text="Translating...")
        self.parent_frame.master.update_idletasks()
        
    def _enable_translate_btn(self) -> None:
        """Rehabilita el botón de traducir."""
        self.btn_translate_file.configure(state="normal", text=self.t["translate_file"])
        self.parent_frame.master.update_idletasks()