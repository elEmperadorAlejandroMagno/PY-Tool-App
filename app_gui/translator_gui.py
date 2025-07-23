import tkinter as tk
from tkinter import filedialog, messagebox
from apps.translator import TranslatorApp

class TranslatorGUI:
    def __init__(self, lang="en"):
        self.app = TranslatorApp(lang)
        self.t = self.app.t

        self.root = tk.Tk()
        self.root.title(self.t["title"])

        self.language_var = tk.StringVar(value=self.app.lang)
        self.language_menu = tk.OptionMenu(
            self.root,
            self.language_var,
            *self.app.languages,
            command=self.set_lang
        )
        self.language_menu.pack(pady=10)
        
        self.translate_text= tk.Button(self.root, text=self.t["translate"], command=self.translate_text)
        self.translate_text.pack(pady=10)
        
        self.translate_file = tk.Button(self.root, text=self.t["translate_file"], command=self.translate_file)
        self.translate_file.pack(pady=10)

    def translate_text_gui(self):
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=10)
        
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.btn_translate = tk.Button(self.root, text=self.t["translate"], command=self.translate_text)
        self.btn_translate.pack(pady=10)

        self.btn_file = tk.Button(self.root, text=self.t["select_file"], command=self.get_file_path)
        self.btn_file.pack(pady=10)

        self.file_path = None
        self.btn_translate_file = tk.Button(self.root, text=self.t["translate_file"], state=tk.DISABLED, command=self.translate_file)
        self.btn_translate_file.pack(pady=10)

    def file_translate_gui(self):
        self.btn_file = tk.Button(self.root, text=self.t["select_file"], command=self.get_file_path)
        self.btn_file.pack(pady=10)

        self.file_path = None
        self.btn_translate_file = tk.Button(self.root, text=self.t["translate_file"], state=tk.DISABLED, command=self.translate_file)
        self.btn_translate_file.pack(pady=10)

    def get_file_path(self):
        self.file_path = filedialog.askopenfilename(
            title="Selecciona un archivo de texto",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.file_path != None:
            self.enable_file_button()
        else:
            messagebox.showwarning("No file selected", "Please select a file to translate.")

    def enable_file_button(self):
        self.btn_translate_file.config(state=tk.NORMAL)
        self.btn_file.config(text=self.file_path.split("/")[-1])

    def disable_translate_btn(self, button):
        button.config(state=tk.DISABLED, text="Translating...")
        self.root.update_idletasks()

    def enable_translate_btn(self, button):
        button.config(state=tk.NORMAL, text=self.t["translate"])
        self.root.update_idletasks()

    def translate_text(self):
        self.disable_translate_btn(self.btn_translate)
        text = self.entry.get()
        result = self.app.translate_line(text)
        self.result_label.config(text=result)
        self.enable_translate_btn(self.btn_translate)

    def translate_file(self):
        self.disable_translate_btn(self.btn_translate_file)
        result = self.app.translate_file(self.file_path)
        self.enable_translate_btn(self.btn_translate_file)
        messagebox.showinfo(self.t["translation"], result)


    def set_entry_language(self, lang):
        self.app.entry_language = lang

    def set_output_language(self, lang):
        self.app.output_language = lang

    def run(self):
        self.root.mainloop()