from apps import tictactoe, timer, translator
import argparse
import tkinter as tk
from translations.translations import get_translations as translations

def main():
    parser = argparse.ArgumentParser(description="Selecciona qué aplicación iniciar")
    parser.add_argument("--lang", type=str, default="en", help="Idioma general de la aplicación")
    args = parser.parse_args()
    lang = args.lang if  args.lang in translations else "en"
    title = translations[lang]["launcher"]

    # Launcher con Tkinter
    def launch_timer():
        root.destroy()
        timer.main(lang)

    def launch_translator():
        root.destroy()
        translator.main(lang)

    def launch_tictactoe():
        root.destroy()
        tictactoe.main(lang)

    global root
    root = tk.Tk()
    root.title("Launcher")

    tk.Label(root, text=title["select_app"], font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text=title["timer"], width=20, command=launch_timer).pack(pady=5)
    tk.Button(root, text=title["translator"], width=20, command=launch_translator).pack(pady=5)
    tk.Button(root, text=title["tictactoe"], width=20, command=launch_tictactoe).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
