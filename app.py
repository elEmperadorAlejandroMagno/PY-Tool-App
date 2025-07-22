import argparse
import tkinter as tk
from translations.translations import get_translations as translations
from app_gui.translator_gui import TranslatorGUI

def main():
    parser = argparse.ArgumentParser(description="Selecciona qué aplicación iniciar")
    parser.add_argument("--lang", type=str, default="en", help="Idioma general de la aplicación")
    args = parser.parse_args()
    title = "Translator"
    
    TranslatorGUI(lang=args.lang)
    tk.mainloop()

if __name__ == '__main__':
    main()
