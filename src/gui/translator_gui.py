import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, Dict, Any
from src.core.translator import TranslatorApp

class TranslatorGUI:
    def __init__(self, lang: str = "en") -> None:
        self.app: TranslatorApp = TranslatorApp(lang)
        self.t: Dict[str, Any] = self.app.t
        self.file_path: Optional[str] = None

        self.root: tk.Tk = tk.Tk()
        self.root.title(self.t["title"])

        self.language_var: tk.StringVar = tk.StringVar(value=self.app.lang)
        self.language_menu: tk.OptionMenu = tk.OptionMenu(
            self.root,
            self.language_var,
            *self.app.languages,
            command=lambda value: self.set_lang(str(value))
        )
        self.language_menu.pack(pad=10)
        
        self.translate_text_btn: tk.Button = tk.Button(self.root, text=self.t["translate"], command=self.translate_text_gui)
        self.translate_text_btn.pack(pad=10)
        
        self.translate_file_btn: tk.Button = tk.Button(self.root, text=self.t["translate_file"], command=self.file_translate_gui)
        self.translate_file_btn.pack(pad=10)

    def translate_text_gui(self) -> None:
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pad=10)
        
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pad=10)

        self.btn_translate = tk.Button(self.root, text=self.t["translate"], command=self.translate_text)
        self.btn_translate.pack(pad=10)

        self.btn_file = tk.Button(self.root, text=self.t["select_file"], command=self.get_file_path)
        self.btn_file.pack(pad=10)

        self.file_path = None
        self.btn_translate_file = tk.Button(self.root, text=self.t["translate_file"], state=tk.DISABLED, command=self.translate_file)
        self.btn_translate_file.pack(pad=10)

    def file_translate_gui(self) -> None:
        self.btn_file = tk.Button(self.root, text=self.t["select_file"], command=self.get_file_path)
        self.btn_file.pack(pad=10)

        self.file_path = None
        self.btn_translate_file = tk.Button(self.root, text=self.t["translate_file"], state=tk.DISABLED, command=self.translate_file)
        self.btn_translate_file.pack(pad=10)

    def get_file_path(self) -> None:
        self.file_path = filedialog.askopenfilename(
            title="Selecciona un archivo de texto",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
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

    def translate_text(self) -> None:
        self.disable_translate_btn(self.btn_translate)
        text: str = self.entry.get()
        result: str = self.app._translate_text(text)
        self.result_label.config(text=result)
        self.enable_translate_btn(self.btn_translate)

    def translate_file(self) -> None:
        self.disable_translate_btn(self.btn_translate_file)
        # TODO: Implementar traducción de archivos
        result: str = "File translation not implemented yet"
        self.enable_translate_btn(self.btn_translate_file)
        messagebox.showinfo(self.t["translation"], result)

    def set_lang(self, lang: str) -> None:
        self.app.output_language = lang

    def set_entry_language(self, lang: str) -> None:
        self.app.entry_language = lang

    def set_output_language(self, lang: str) -> None:
        self.app.output_language = lang

    def run(self) -> None:
        self.root.mainloop()
