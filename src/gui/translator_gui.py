import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Any
from src.core.factories.translator_factory import create_translator_app

class TranslatorGUI:
    def __init__(self, lang: str = "en") -> None:
        self.app = create_translator_app(lang)
        self.t: dict[str, Any] = self.app.t
        self.file_path: str | None = None
        self.app.languages.append("detect")

        self.root: tk.Tk = tk.Tk()
        self.root.title(self.t["title"])
        
        self.translate_text_btn: tk.Button = tk.Button(self.root, text=self.t["translate"], command=self.translate_text_gui)
        self.translate_text_btn.pack(pady=10)
        
        self.translate_file_btn: tk.Button = tk.Button(self.root, text=self.t["translate_file"], command=self.file_translate_gui)
        self.translate_file_btn.pack(pady=10)

    def set_entry_language_menu(self) -> None:
        self.entry_language_var: tk.StringVar = tk.StringVar(value="detect")
        self.entry_language_menu: tk.OptionMenu = tk.OptionMenu(
            self.root,
            self.entry_language_var,
            *self.app.languages,
            command=lambda value: self.set_entry_language(str(value))
        )
        self.entry_language_menu.pack(pady=10)

    def set_output_language_menu(self) -> None:
        self.output_language_var: tk.StringVar = tk.StringVar(value=self.app.lang)
        self.output_language_menu: tk.OptionMenu = tk.OptionMenu(
            self.root,
            self.output_language_var,
            *self.app.languages,
            command=lambda value: self.set_output_language(str(value))
        )
        self.output_language_menu.pack(pady=10)

    def draw_language_menus(self) -> None:
        self.entry_label = tk.Label(self.root, text=self.t["select_language_from"])
        self.entry_label.pack()
        self.set_entry_language_menu() 
        self.output_label = tk.Label(self.root, text=self.t["select_language_to"])
        self.output_label.pack()
        self.set_output_language_menu()

    def translate_text_gui(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        self.draw_language_menus()
        
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=10)
        
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.btn_translate = tk.Button(self.root, text=self.t["translate"], command=self.translate_text)
        self.btn_translate.pack(pady=10)

    def file_translate_gui(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        self.draw_language_menus()

        self.btn_file = tk.Button(self.root, text=self.t["select_file"], command=self.get_file_path)
        self.btn_file.pack(pady=10)

        self.file_path = None
        self.btn_translate_file = tk.Button(self.root, text=self.t["translate_file"], state=tk.DISABLED, command=self.translate_file)
        self.btn_translate_file.pack(pady=10)

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

    def translate_text(self) -> None:
        self.disable_translate_btn(self.btn_translate)
        text: str = self.entry.get()
        result: str = self.app.translate_text(text)
        self.result_label.config(text=result)
        self.enable_translate_btn(self.btn_translate)

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

    def set_lang(self, lang: str) -> None:
        self.app.output_language = lang

    def set_entry_language(self, lang: str) -> None:
        self.app.entry_language = lang

    def set_output_language(self, lang: str) -> None:
        self.app.output_language = lang

    def run(self) -> None:
        self.root.mainloop()
