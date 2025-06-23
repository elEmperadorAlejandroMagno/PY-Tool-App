import tkinter as tk
from tkinter import filedialog, messagebox
from apps.translator import TranslatorApp

class TranslatorGUI:
    def __init__(self, lang="en"):
        self.app = TranslatorApp(lang)
        self.t = self.app.t

        self.root = tk.Tk()
        self.root.title(self.t["title"])

        # Entrada de texto
        self.label = tk.Label(self.root, text=self.t["insert_text"])
        self.label.pack(pady=5)

        self.entry_lang_options = ["detect", "ES", "EN", "RU"]
        self.entry_lang = tk.OptionMenu(self.root, tk.StringVar(value="detect"), *self.entry_lang_options, command=self.set_entry_language)
        self.entry_lang.pack(pady=5)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=5)

        self.btn_translate = tk.Button(self.root, text=self.t["translate"], command=self.translate_text)
        self.btn_translate.pack(pady=5)

        self.output_lang_options = ["ES", "EN", "RU"]
        self.outro_lang = tk.OptionMenu(self.root, tk.StringVar(value=lang), *self.output_lang_options, command=self.set_output_language)
        self.outro_lang.pack(pady=5)

        self.result_label = tk.Label(self.root, text=self.t["translation"])
        self.result_label.pack(pady=10)

        self.btn_file = tk.Button(self.root, text="Seleccionar archivo", command=self.translate_file)
        self.btn_file.pack(pady=5)

    def translate_text(self):
        text = self.entry.get()
        result = self.app.translate_line(text)
        self.result_label.config(text=result)

    def translate_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo de texto",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            result = self.app.translate_file(file_path)
            messagebox.showinfo(self.t["translation"], result)

    def set_entry_language(self, lang):
        self.app.entry_language = lang

    def set_output_language(self, lang):
        self.app.output_language = lang

    def run(self):
        self.root.mainloop()