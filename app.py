import argparse
import tkinter as tk
from translations.translations import get_translations as translations

def main():
    parser = argparse.ArgumentParser(description="Selecciona qué aplicación iniciar")
    parser.add_argument("--lang", type=str, default="en", help="Idioma general de la aplicación")
    args = parser.parse_args()
    lang = args.lang if  args.lang in translations else "en"
    title = "My own translator"

    global root
    root = tk.Tk()
    root.title("Launcher")

    tk.Label(root, text=title, font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Translate text", width=20, command=launch_text_translator).pack(pady=5)
    tk.Button(root, text="Translate file", width=20, command=launch_file_translator).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
