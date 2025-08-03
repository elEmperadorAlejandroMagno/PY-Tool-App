import argparse
import tkinter as tk
import sys
from src.config.translations import get_translations as translations
from src.gui.translator_gui import TranslatorGUI

def show_usage():
    """Muestra el uso correcto del programa"""
    print("\n=== TRANSLATOR APP ===")
    print("Uso correcto:")
    print("  python app.py                 # Usa inglés por defecto")
    print("  python app.py --lang es       # Español")
    print("  python app.py --lang fr       # Francés")
    print("  python app.py --lang ru       # Ruso")
    print("  python app.py --lang zh       # Chino")
    print("\nIdiomas disponibles: en, es, fr, ru, zh")
    print("======================\n")

def create_argument_parser():
    parser = argparse.ArgumentParser(
        description="Aplicación de Traducción - Translator App",
        epilog="Ejemplos:\n  python app.py              # Inglés por defecto\n  python app.py --lang es    # Español\n  python app.py --lang fr    # Francés",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--lang", 
        type=str, 
        default="en", 
        choices=["en", "es", "fr", "ru", "zh"],
        help="Idioma de la interfaz (por defecto: en)"
    )
    return parser

def validate_language(language):
    if language not in translations:
        print(f"❌ Error: Idioma '{language}' no disponible")
        show_usage()
        return False
    return True

def start_application(language):
    print(f"🚀 Iniciando traductor en idioma: {language}")
    gui = TranslatorGUI(lang=language)
    tk.mainloop()

def handle_keyboard_interrupt():
    """Maneja la interrupción por teclado (Ctrl+C)"""
    print("\n👋 Aplicación cerrada por el usuario")
    sys.exit(0)

def handle_application_error(error):
    """Maneja errores generales de la aplicación"""
    print(f"❌ Error al iniciar la aplicación: {error}")
    show_usage()
    sys.exit(1)

def configure_arguments():
    parser = create_argument_parser()
    args = parser.parse_args()
    return args

def main():
    """Función principal que orquesta la ejecución de la aplicación"""
    try:
        args = configure_arguments()
        
        if not validate_language(args.lang):
            sys.exit(1)
        
        start_application(args.lang)
        
    except KeyboardInterrupt:
        handle_keyboard_interrupt()
    except Exception as e:
        handle_application_error(e)

if __name__ == '__main__':
    main()
