import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional, Dict, Any
import re
from src.core.factories.translator_factory import create_translator_app
from src.core.implements.phonetic_transcription_implements import PhoneticTranscriptionImplements

class TranslatorGUI:
    def __init__(self, lang: str = "en") -> None:
        self.app = create_translator_app(lang)
        self.t: Dict[str, Any] = self.app.t
        self.file_path: Optional[str] = None
        self.entry_languages = [lang.upper() for lang in self.app.languages] + ["DETECT"]
        self.output_languages = [lang.upper() for lang in self.app.languages]
        
        # Inicializar el servicio de transcripción fonética
        self.phonetic_transcriptor = PhoneticTranscriptionImplements()

        # Configurar apariencia de CustomTkinter
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        self.root: ctk.CTk = ctk.CTk()
        self.root.title(self.t["title"])
        self.root.geometry("900x700")

        # Crear sistema de pestañas con CustomTkinter
        self.notebook = ctk.CTkTabview(self.root, width=850, height=650)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Agregar pestañas
        self.notebook.add(self.t["translate"])
        self.notebook.add(self.t["translate_file"])
        self.notebook.add("IPA Transcription")
        
        # Obtener referencias a los frames de las pestañas
        self.text_tab = self.notebook.tab(self.t["translate"])
        self.file_tab = self.notebook.tab(self.t["translate_file"])
        self.tools_tab = self.notebook.tab("IPA Transcription")

        # Renderizar cada apartado
        self.render_text_tab()
        self.render_file_tab()
        self.render_tools_tab()

    def render_text_tab(self):
        # frame interno con padding
        content_frame = ctk.CTkFrame(self.text_tab)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Menús de idioma
        entry_label = ctk.CTkLabel(content_frame, text=self.t["select_language_from"], font=ctk.CTkFont(size=14, weight="bold"))
        entry_label.pack(pady=(10, 5))
        
        self.entry_language_var = ctk.StringVar(value="DETECT")
        self.entry_menu = ctk.CTkOptionMenu(
            content_frame,
            values=self.entry_languages,
            variable=self.entry_language_var,
            command=self.set_entry_language,
            width=200,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.entry_menu.pack(pady=5)

        output_label = ctk.CTkLabel(content_frame, text=self.t["select_language_to"], font=ctk.CTkFont(size=14, weight="bold"))
        output_label.pack(pady=(15, 5))
        
        self.output_language_var = ctk.StringVar(value=self.app.lang.upper())
        self.output_menu = ctk.CTkOptionMenu(
            content_frame,
            values=self.output_languages,
            variable=self.output_language_var,
            command=self.set_output_language,
            width=200,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.output_menu.pack(pady=5)

        # Entrada de texto
        input_label = ctk.CTkLabel(content_frame, text="Text to translate:", font=ctk.CTkFont(size=14, weight="bold"))
        input_label.pack(pady=(20, 5))
        
        self.entry = ctk.CTkTextbox(content_frame, width=700, height=120, font=ctk.CTkFont(size=16))
        self.entry.pack(pady=5)
        
        # Botón de traducir
        self.btn_translate = ctk.CTkButton(
            content_frame, 
            text=self.t["translate"], 
            command=self.translate_text,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_translate.pack(pady=15)
        
        # Resultado
        result_label = ctk.CTkLabel(content_frame, text="Translation result:", font=ctk.CTkFont(size=14, weight="bold"))
        result_label.pack(pady=(10, 5))
        
        self.result_textbox = ctk.CTkTextbox(content_frame, width=700, height=120, font=ctk.CTkFont(size=16))
        self.result_textbox.pack(pady=5)

    def render_file_tab(self):
        # frame interno con padding
        content_frame = ctk.CTkFrame(self.file_tab)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Menús de idioma
        entry_label = ctk.CTkLabel(content_frame, text=self.t["select_language_from"], font=ctk.CTkFont(size=14, weight="bold"))
        entry_label.pack(pady=(10, 5))
        
        self.entry_language_var_file = ctk.StringVar(value="DETECT")
        self.entry_menu_file = ctk.CTkOptionMenu(
            content_frame,
            values=self.entry_languages,
            variable=self.entry_language_var_file,
            command=self.set_entry_language_file,
            width=200,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.entry_menu_file.pack(pady=5)

        output_label = ctk.CTkLabel(content_frame, text=self.t["select_language_to"], font=ctk.CTkFont(size=14, weight="bold"))
        output_label.pack(pady=(15, 5))
        
        self.output_language_var_file = ctk.StringVar(value=self.app.lang.upper())
        self.output_menu_file = ctk.CTkOptionMenu(
            content_frame,
            values=self.output_languages,
            variable=self.output_language_var_file,
            command=self.set_output_language_file,
            width=200,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.output_menu_file.pack(pady=5)

        # Selección de archivo
        file_label = ctk.CTkLabel(content_frame, text="File Selection:", font=ctk.CTkFont(size=14, weight="bold"))
        file_label.pack(pady=(30, 10))
        
        self.btn_file = ctk.CTkButton(
            content_frame, 
            text=self.t["select_file"], 
            command=self.get_file_path,
            width=250,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_file.pack(pady=10)
        
        self.btn_translate_file = ctk.CTkButton(
            content_frame, 
            text=self.t["translate_file"], 
            state="disabled", 
            command=self.translate_file,
            width=250,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_translate_file.pack(pady=10)
    
    def render_tools_tab(self):
        """Renderiza la pestaña de herramientas"""
        # Frame principal con padding
        content_frame = ctk.CTkFrame(self.tools_tab)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Select/Dropdown para elegir tipo de IPA
        tool_label = ctk.CTkLabel(content_frame, text="Select IPA Type:", font=ctk.CTkFont(size=14, weight="bold"))
        tool_label.pack(pady=(10, 5))
        
        self.tool_var = ctk.StringVar(value="RP IPA")
        tool_options = ["RP IPA", "AMERICAN IPA"]
        self.tool_menu = ctk.CTkOptionMenu(
            content_frame,
            values=tool_options,
            variable=self.tool_var,
            command=self.update_tool_selection,
            width=200,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.tool_menu.pack(pady=5)
        
        # Checkbox para formas strong/weak
        self.use_weak_forms_var = ctk.BooleanVar(value=True)  # Por defecto usa formas weak
        weak_forms_checkbox = ctk.CTkCheckBox(
            content_frame,
            text="Use weak forms (unstressed)",
            variable=self.use_weak_forms_var,
            font=ctk.CTkFont(size=12)
        )
        weak_forms_checkbox.pack(pady=(15, 10))
        
        # Input Text
        input_label = ctk.CTkLabel(content_frame, text="English Text:", font=ctk.CTkFont(size=14, weight="bold"))
        input_label.pack(pady=(20, 5))
        
        self.tools_input = ctk.CTkTextbox(content_frame, width=700, height=120, font=ctk.CTkFont(size=16))
        self.tools_input.pack(pady=5)
        
        # Botón central (entre los inputs)
        self.btn_process = ctk.CTkButton(
            content_frame,
            text="Transcribe",
            command=self.process_text_tool,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_process.pack(pady=15)
        
        # Output Text
        output_label = ctk.CTkLabel(content_frame, text="IPA Transcription:", font=ctk.CTkFont(size=14, weight="bold"))
        output_label.pack(pady=(10, 5))
        
        self.tools_output = ctk.CTkTextbox(
            content_frame,
            width=700,
            height=120,
            font=ctk.CTkFont(family="Arial Unicode MS", size=16)  # Fuente que soporta bien caracteres IPA
        )
        self.tools_output.pack(pady=5)
        
        # Frame para el botón inferior en la esquina
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
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

    # Métodos para pestaña de texto
    def translate_text(self) -> None:
        self.disable_translate_btn(self.btn_translate)
        text: str = self.entry.get("1.0", "end").strip()
        result: str = self.app.translate_text(text)
        
        # Limpiar y mostrar resultado
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", result.text)
        
        self.enable_translate_btn(self.btn_translate)

    # Métodos para pestaña de archivo
    def get_file_path(self) -> None:
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
            self.enable_file_button()
        else:
            messagebox.showwarning("No file selected", "Please select a file to translate.")

    def enable_file_button(self) -> None:
        if self.file_path:
            self.btn_translate_file.configure(state="normal")
            self.btn_file.configure(text=self.file_path.split("/")[-1])

    def disable_translate_btn(self, button: ctk.CTkButton) -> None:
        button.configure(state="disabled", text="Translating...")
        self.root.update_idletasks()

    def enable_translate_btn(self, button: ctk.CTkButton) -> None:
        button.configure(state="normal", text=self.t["translate"])
        self.root.update_idletasks()
        
    def translate_file(self) -> None:
        self.disable_translate_btn(self.btn_translate_file)
        if not self.file_path:
            messagebox.showwarning("No file selected", "Please select a file to translate.")
            self.enable_translate_btn(self.btn_translate_file)
            return
        try:
            result: str = self.app.translate_file(self.file_path)
        except Exception as e:
            result = f"Error translating file: {e}"
        self.enable_translate_btn(self.btn_translate_file)
        messagebox.showinfo(self.t["translation"], result)

    # Métodos para actualizar idioma en cada pestaña
    def set_entry_language(self, lang: str) -> None:
        self.app.entry_language = lang.lower()

    def set_output_language(self, lang: str) -> None:
        self.app.output_language = lang.lower()

    def set_entry_language_file(self, lang: str) -> None:
        self.app.entry_language = lang.lower()

    def set_output_language_file(self, lang: str) -> None:
        self.app.output_language = lang.lower()
    
    # Métodos para herramientas de texto
    def update_tool_selection(self, tool: str) -> None:
        """Actualizar la herramienta seleccionada"""
        self.selected_tool = tool
    
    def process_text_tool(self) -> None:
        """Procesar el texto con la herramienta seleccionada"""
        # Obtener texto sin .strip() para preservar saltos de línea al final
        raw_input_text = self.tools_input.get("1.0", "end")
        # Solo eliminar el \n final que CustomTkinter agrega automáticamente
        if raw_input_text.endswith('\n'):
            raw_input_text = raw_input_text[:-1]
        
        # Limpiar y normalizar el texto de entrada
        input_text = self.clean_input_text(raw_input_text)
        
        if not input_text.strip():
            messagebox.showwarning("Warning", "Please enter some English text to transcribe.")
            return
        
        # Deshabilitar botón mientras procesa
        self.btn_process.configure(state="disabled", text="Transcribing...")
        self.root.update_idletasks()
        
        try:
            tool = self.tool_var.get()
            result = self.apply_text_tool(input_text, tool)
            
            # Mostrar resultado
            self.tools_output.delete("1.0", "end")
            self.tools_output.insert("1.0", result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing text: {str(e)}")
        finally:
            # Rehabilitar botón
            self.btn_process.configure(state="normal", text="Transcribe")
            self.root.update_idletasks()
    
    def apply_text_tool(self, text: str, tool: str) -> str:
        """Aplicar la transcripción IPA según el tipo seleccionado preservando saltos de línea"""
        if tool == "RP IPA":
            try:
                result = self.phonetic_transcriptor.transcribe_to_ipa(text, "rp")
                if result:
                    # Limpiar el resultado antes de devolverlo
                    cleaned_result = self.clean_output_text(result)
                    return cleaned_result
                else:
                    return "Error: Could not transcribe text to RP IPA"
            except Exception as e:
                return f"Error in RP IPA transcription: {str(e)}"
                
        elif tool == "American IPA":
            try:
                result = self.phonetic_transcriptor.transcribe_to_ipa(text, "american")
                if result:
                    # Limpiar el resultado antes de devolverlo
                    cleaned_result = self.clean_output_text(result)
                    return f"/{cleaned_result}/"
                else:
                    return "Error: Could not transcribe text to American IPA"
            except Exception as e:
                return f"Error in American IPA transcription: {str(e)}"
        else:
            return "Unknown IPA type selected"
    
    def clear_all_tools(self) -> None:
        """Limpiar todos los campos de la pestaña de herramientas"""
        self.tools_input.delete("1.0", "end")
        self.tools_output.delete("1.0", "end")
        self.tool_var.set("RP IPA")  # Reset to default
        
    def clean_input_text(self, text: str) -> str:
        """Limpia y normaliza el texto de entrada"""
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
    
    def clean_output_text(self, text: str) -> str:
        """Limpia y normaliza el texto de salida de transcripción"""
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

    def run(self) -> None:
        self.root.mainloop()
