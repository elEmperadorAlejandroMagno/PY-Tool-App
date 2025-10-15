"""
Pestaña de transcripción fonética IPA.

Maneja la funcionalidad de transcribir texto en inglés a notación IPA 
(tanto RP como American).
"""

import re
from typing import Any, Dict
import customtkinter as ctk
from tkinter import messagebox
from .tab_interface import TabInterface
from src.core.implements.phonetic_transcription_implements import PhoneticTranscriptionImplements


class IpaTranscriptionTab(TabInterface):
    """Pestaña para transcripción fonética IPA."""
    
    def __init__(self, parent_frame: ctk.CTkFrame, app: Any, t: Dict[str, Any]) -> None:
        """
        Inicializa la pestaña de transcripción IPA.
        
        Args:
            parent_frame: Frame padre donde se renderizará
            app: Instancia de la aplicación principal
            t: Diccionario de traducciones
        """
        super().__init__(parent_frame, app, t)
        
        # Inicializar el servicio de transcripción fonética
        self.phonetic_transcriptor = PhoneticTranscriptionImplements()
        
        # Variables de interfaz
        self.tool_var: ctk.StringVar = None
        self.use_weak_forms_var: ctk.BooleanVar = None
        
        # Widgets
        self.tool_menu: ctk.CTkOptionMenu = None
        self.tools_input: ctk.CTkTextbox = None
        self.tools_output: ctk.CTkTextbox = None
        self.btn_process: ctk.CTkButton = None
        self.btn_clear_all: ctk.CTkButton = None
        
    def render(self) -> None:
        """Renderiza el contenido de la pestaña de transcripción IPA."""
        self.content_frame = self.create_content_frame()
        
        self._create_tool_selection()
        self._create_input_section()
        self._create_process_button()
        self._create_output_section()
        self._create_clear_button()
        
    def _create_tool_selection(self) -> None:
        """Crea la sección de selección de tipo IPA."""
        tool_label = self.create_label(
            self.content_frame,
            "Select IPA Type:"
        )
        tool_label.pack(pady=(10, 5))
        
        self.tool_var = ctk.StringVar(value="RP IPA")
        tool_options = ["RP IPA", "AMERICAN IPA"]
        self.tool_menu = self.create_language_menu(
            self.content_frame,
            tool_options,
            self.tool_var,
            self.update_tool_selection
        )
        self.tool_menu.pack(pady=5)
        
        # Checkbox para formas strong/weak
        self.use_weak_forms_var = ctk.BooleanVar(value=True)
        weak_forms_checkbox = ctk.CTkCheckBox(
            self.content_frame,
            text="Use weak forms (unstressed)",
            variable=self.use_weak_forms_var,
            font=ctk.CTkFont(size=12)
        )
        weak_forms_checkbox.pack(pady=(15, 10))
        
    def _create_input_section(self) -> None:
        """Crea la sección de entrada de texto."""
        input_label = self.create_label(
            self.content_frame,
            "English Text:"
        )
        input_label.pack(pady=(20, 5))
        
        self.tools_input = self.create_textbox(self.content_frame)
        self.tools_input.pack(pady=5)
        
    def _create_process_button(self) -> None:
        """Crea el botón de procesar."""
        self.btn_process = self.create_button(
            self.content_frame,
            "Transcribe",
            self.process_text_tool
        )
        self.btn_process.pack(pady=15)
        
    def _create_output_section(self) -> None:
        """Crea la sección de salida."""
        output_label = self.create_label(
            self.content_frame,
            "IPA Transcription:"
        )
        output_label.pack(pady=(10, 5))
        
        self.tools_output = self.create_textbox(
            self.content_frame,
            font_family="Arial Unicode MS"
        )
        self.tools_output.pack(pady=5)
        
    def _create_clear_button(self) -> None:
        """Crea el botón de limpiar todo."""
        # Frame para el botón inferior en la esquina
        bottom_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(15, 0))
        
        # Botón en la esquina inferior derecha
        self.btn_clear_all = ctk.CTkButton(
            bottom_frame,
            text="Clear All",
            command=self.clear_all_tools,
            width=120,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        self.btn_clear_all.pack(side="right")
        
    def update_tool_selection(self, tool: str) -> None:
        """
        Actualiza la herramienta seleccionada.
        
        Args:
            tool: Tipo de IPA seleccionado
        """
        self.selected_tool = tool
        
    def process_text_tool(self) -> None:
        """Procesa el texto con la herramienta seleccionada."""
        # Obtener texto sin .strip() para preservar saltos de línea al final
        raw_input_text = self.tools_input.get("1.0", "end")
        # Solo eliminar el \n final que CustomTkinter agrega automáticamente
        if raw_input_text.endswith('\n'):
            raw_input_text = raw_input_text[:-1]
        
        # Limpiar y normalizar el texto de entrada
        input_text = self._clean_input_text(raw_input_text)
        
        if not input_text.strip():
            messagebox.showwarning(
                "Warning", 
                "Please enter some English text to transcribe."
            )
            return
        
        # Deshabilitar botón mientras procesa
        self.btn_process.configure(state="disabled", text="Transcribing...")
        self.parent_frame.master.update_idletasks()
        
        try:
            tool = self.tool_var.get()
            use_weak_forms = self.use_weak_forms_var.get()
            result = self._apply_text_tool(input_text, tool, use_weak_forms)
            
            # Mostrar resultado
            self.tools_output.delete("1.0", "end")
            self.tools_output.insert("1.0", result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing text: {str(e)}")
        finally:
            # Rehabilitar botón
            self.btn_process.configure(state="normal", text="Transcribe")
            self.parent_frame.master.update_idletasks()
            
    def _apply_text_tool(self, text: str, tool: str, use_weak_forms: bool = True) -> str:
        """
        Aplica la transcripción IPA según el tipo seleccionado preservando saltos de línea.
        
        Args:
            text: Texto a transcribir
            tool: Tipo de IPA a usar
            use_weak_forms: Si aplicar formas débiles
            
        Returns:
            Texto transcrito a IPA
        """
        if tool == "RP IPA":
            try:
                result = self.phonetic_transcriptor.transcribe_to_ipa(text, "rp", use_weak_forms)
                if result:
                    # Limpiar el resultado antes de devolverlo
                    cleaned_result = self._clean_output_text(result)
                    return cleaned_result
                else:
                    return "Error: Could not transcribe text to RP IPA"
            except Exception as e:
                return f"Error in RP IPA transcription: {str(e)}"
                
        elif tool == "AMERICAN IPA":
            try:
                result = self.phonetic_transcriptor.transcribe_to_ipa(text, "american", use_weak_forms)
                if result:
                    # Limpiar el resultado antes de devolverlo
                    cleaned_result = self._clean_output_text(result)
                    return f"/{cleaned_result}/"
                else:
                    return "Error: Could not transcribe text to American IPA"
            except Exception as e:
                return f"Error in American IPA transcription: {str(e)}"
        else:
            return "Unknown IPA type selected"
            
    def clear_all_tools(self) -> None:
        """Limpia todos los campos de la pestaña de herramientas."""
        self.tools_input.delete("1.0", "end")
        self.tools_output.delete("1.0", "end")
        self.tool_var.set("RP IPA")  # Reset to default
        
    def _clean_input_text(self, text: str) -> str:
        """
        Limpia y normaliza el texto de entrada.
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio y normalizado
        """
        if not text:
            return ""
        
        # Normalizar diferentes tipos de comillas y apostrofes
        text = text.replace('\u201c', '"').replace('\u201d', '"')  # comillas dobles
        text = text.replace('\u2018', "'").replace('\u2019', "'")  # comillas simples
        
        # Normalizar espacios múltiples pero preservar saltos de línea
        # Solo reemplazar espacios múltiples en la misma línea
        lines = text.splitlines()
        cleaned_lines = []
        for line in lines:
            # Limpiar espacios múltiples y tabs en cada línea
            cleaned_line = re.sub(r'[ \t]+', ' ', line.strip())
            cleaned_lines.append(cleaned_line)
        
        # Reunir las líneas preservando estructura
        result = '\n'.join(cleaned_lines)
        
        # Remover líneas vacías múltiples (más de 2 seguidas)
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        return result
        
    def _clean_output_text(self, text: str) -> str:
        """
        Limpia y normaliza el texto de salida de transcripción.
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio y normalizado
        """
        if not text:
            return ""
        
        # Reemplazar todas las ɐ con ə (schwa estándar)
        text = text.replace('ɐ', 'ə')
        
        # Limpiar espacios extra alrededor de puntuación
        text = re.sub(r'\s+([.,!?;:\'-])', r'\1', text)
        
        # Normalizar espacios múltiples pero preservar saltos de línea
        lines = text.splitlines()
        cleaned_lines = []
        for line in lines:
            # Solo limpiar espacios múltiples en cada línea
            cleaned_line = re.sub(r' {2,}', ' ', line.strip())
            cleaned_lines.append(cleaned_line)
        
        result = '\n'.join(cleaned_lines)
        
        # Remover líneas vacías múltiples innecesarias
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        return result.strip()