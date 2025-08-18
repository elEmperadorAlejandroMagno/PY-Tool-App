import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Dict, Any
from src.core.factories.translator_factory import create_translator_app

class TranslatorGUI:
    def __init__(self, lang: str = "en") -> None:
        self.app = create_translator_app(lang)
        self.t: Dict[str, Any] = self.app.t
        self.file_path: Optional[str] = None
        self.entry_languages = [lang for lang in self.app.languages] + ["detect"]
        self.output_languages = [lang for lang in self.app.languages]

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

        # Renderizar cada apartado
        self.render_text_tab()
        self.render_file_tab()

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

    def run(self) -> None:
        self.root.mainloop()
