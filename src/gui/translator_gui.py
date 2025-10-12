import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Dict, Any
import re
from src.core.factories.translator_factory import create_translator_app
from src.core.implements.phonetic_transcription_implements import PhoneticTranscriptionImplements

class TranslatorGUI:
    def __init__(self, lang: str = "en") -> None:
        self.app = create_translator_app(lang)
        self.t: Dict[str, Any] = self.app.t
        self.file_path: Optional[str] = None
        self.entry_languages = [lang for lang in self.app.languages] + ["detect"]
        self.output_languages = [lang for lang in self.app.languages]
        
        # Inicializar el servicio de transcripción fonética
        self.phonetic_transcriptor = PhoneticTranscriptionImplements()

        self.root: tk.Tk = tk.Tk()
        self.root.title(self.t["title"])

        # Crear Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para traducir texto
        self.text_tab = tk.Frame(self.notebook)
        self.notebook.add(self.text_tab, text=self.t["translate"])

        # Frame para traducir archivo
        self.file_tab = tk.Frame(self.notebook)
        self.notebook.add(self.file_tab, text=self.t["translate_file"])
        
        # Frame para herramientas
        self.tools_tab = tk.Frame(self.notebook)
        self.notebook.add(self.tools_tab, text="IPA Transcription")

        # Renderizar cada apartado
        self.render_text_tab()
        self.render_file_tab()
        self.render_tools_tab()

    def render_text_tab(self):
        # frame interno con padding
        content_frame = tk.Frame(self.text_tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        # Menús de idioma
        entry_label = tk.Label(content_frame, text=self.t["select_language_from"])
        entry_label.pack()
        self.entry_language_var = tk.StringVar(value="detect")
        entry_menu = tk.OptionMenu(
            content_frame,
            self.entry_language_var,
            *self.entry_languages,
            command=lambda value: self.set_entry_language(str(value))
        )
        entry_menu.pack(pady=5)
        entry_menu.config(width=5)

        output_label = tk.Label(content_frame, text=self.t["select_language_to"])
        output_label.pack()
        self.output_language_var = tk.StringVar(value=self.app.lang)
        output_menu = tk.OptionMenu(
            content_frame,
            self.output_language_var,
            *self.output_languages,
            command=lambda value: self.set_output_language(str(value))
        )
        output_menu.pack(pady=5)
        output_menu.config(width=5)

        # Entrada de texto y botón
        self.entry = tk.Text(content_frame, width=50, height=5)
        self.entry.pack(pady=10)
        self.result_label = tk.Label(content_frame, text="")
        self.result_label.pack(pady=10)
        self.btn_translate = tk.Button(content_frame, text=self.t["translate"], command=self.translate_text)
        self.btn_translate.pack(pady=10)

    def render_file_tab(self):
        # frame interno con padding
        content_frame = tk.Frame(self.file_tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        # Menús de idioma
        entry_label = tk.Label(content_frame, text=self.t["select_language_from"])
        entry_label.pack()
        self.entry_language_var_file = tk.StringVar(value="detect")
        entry_menu = tk.OptionMenu(
            content_frame,
            self.entry_language_var_file,
            *self.entry_languages,
            command=lambda value: self.set_entry_language_file(str(value))
        )
        entry_menu.pack(pady=5)
        entry_menu.config(width=5)

        output_label = tk.Label(content_frame, text=self.t["select_language_to"])
        output_label.pack()
        self.output_language_var_file = tk.StringVar(value=self.app.lang)
        output_menu = tk.OptionMenu(
            content_frame,
            self.output_language_var_file,
            *self.output_languages,
            command=lambda value: self.set_output_language_file(str(value))
        )
        output_menu.pack(pady=5)
        output_menu.config(width=5)

        # Selección de archivo y botón
        self.btn_file = tk.Button(content_frame, text=self.t["select_file"], command=self.get_file_path)
        self.btn_file.pack(pady=10)
        self.btn_translate_file = tk.Button(content_frame, text=self.t["translate_file"], state=tk.DISABLED, command=self.translate_file)
        self.btn_translate_file.pack(pady=10)
    
    def render_tools_tab(self):
        """Renderiza la pestaña de herramientas"""
        # Frame principal con padding
        content_frame = tk.Frame(self.tools_tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Select/Dropdown para elegir tipo de IPA
        tool_label = tk.Label(content_frame, text="Select IPA Type:")
        tool_label.pack(pady=(0, 5))
        
        self.tool_var = tk.StringVar(value="RP IPA")
        tool_options = ["RP IPA", "American IPA"]
        tool_menu = tk.OptionMenu(
            content_frame,
            self.tool_var,
            *tool_options,
            command=lambda value: self.update_tool_selection(str(value))
        )
        tool_menu.pack(pady=5)
        tool_menu.config(width=15)
        
        # Checkbox para formas strong/weak
        self.use_weak_forms_var = tk.BooleanVar(value=True)  # Por defecto usa formas weak
        weak_forms_checkbox = tk.Checkbutton(
            content_frame,
            text="Use weak forms (unstressed)",
            variable=self.use_weak_forms_var,
            font=("Arial", 9)
        )
        weak_forms_checkbox.pack(pady=(10, 0))
        
        # Input Text
        input_label = tk.Label(content_frame, text="English Text:")
        input_label.pack(pady=(15, 5))
        
        self.tools_input = tk.Text(content_frame, width=60, height=6)
        self.tools_input.pack(pady=5)
        
        # Botón central (entre los inputs)
        self.btn_process = tk.Button(
            content_frame,
            text="Transcribe",
            command=self.process_text_tool,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_process.pack(pady=10)
        
        # Output Text
        output_label = tk.Label(content_frame, text="IPA Transcription:")
        output_label.pack(pady=(5, 5))
        
        self.tools_output = tk.Text(
            content_frame,
            width=60,
            height=6,
            state=tk.DISABLED,
            bg="#f0f0f0",
            font=("Arial Unicode MS", 12)  # Fuente que soporta bien caracteres IPA
        )
        self.tools_output.pack(pady=5)
        
        # Frame para el botón inferior en la esquina
        bottom_frame = tk.Frame(content_frame)
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        # Botón en la esquina inferior derecha
        self.btn_clear_all = tk.Button(
            bottom_frame,
            text="Clear All",
            command=self.clear_all_tools,
            bg="#f44336",
            fg="white",
            font=("Arial", 9)
        )
        self.btn_clear_all.pack(side="right")

    # Métodos para pestaña de texto
    def translate_text(self) -> None:
        self.disable_translate_btn(self.btn_translate)
        text: str = self.entry.get("1.0", tk.END).strip()
        result: str = self.app.translate_text(text)
        self.result_label.config(text=result.text)
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
            self.btn_translate_file.config(state=tk.NORMAL)
            self.btn_file.config(text=self.file_path.split("/")[-1])

    def disable_translate_btn(self, button: tk.Button) -> None:
        button.config(state=tk.DISABLED, text="Translating...")
        self.root.update_idletasks()

    def enable_translate_btn(self, button: tk.Button) -> None:
        button.config(state=tk.NORMAL, text=self.t["translate"])
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
        self.app.entry_language = lang

    def set_output_language(self, lang: str) -> None:
        self.app.output_language = lang

    def set_entry_language_file(self, lang: str) -> None:
        self.app.entry_language = lang

    def set_output_language_file(self, lang: str) -> None:
        self.app.output_language = lang
    
    # Métodos para herramientas de texto
    def update_tool_selection(self, tool: str) -> None:
        """Actualizar la herramienta seleccionada"""
        self.selected_tool = tool
    
    def process_text_tool(self) -> None:
        """Procesar el texto con la herramienta seleccionada"""
        # Obtener texto sin .strip() para preservar saltos de línea al final
        raw_input_text = self.tools_input.get("1.0", tk.END)
        # Solo eliminar el \n final que tkinter agrega automáticamente
        if raw_input_text.endswith('\n'):
            raw_input_text = raw_input_text[:-1]
        
        # Limpiar y normalizar el texto de entrada
        input_text = self.clean_input_text(raw_input_text)
        
        if not input_text.strip():
            messagebox.showwarning("Warning", "Please enter some English text to transcribe.")
            return
        
        # Deshabilitar botón mientras procesa
        self.btn_process.config(state=tk.DISABLED, text="Transcribing...")
        self.root.update_idletasks()
        
        try:
            tool = self.tool_var.get()
            result = self.apply_text_tool(input_text, tool)
            
            # Mostrar resultado
            self.tools_output.config(state=tk.NORMAL)
            self.tools_output.delete("1.0", tk.END)
            self.tools_output.insert("1.0", result)
            self.tools_output.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing text: {str(e)}")
        finally:
            # Rehabilitar botón
            self.btn_process.config(state=tk.NORMAL, text="Transcribe")
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
        self.tools_input.delete("1.0", tk.END)
        self.tools_output.config(state=tk.NORMAL)
        self.tools_output.delete("1.0", tk.END)
        self.tools_output.config(state=tk.DISABLED)
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
