import argparse
import tkinter as tk
import sys
from typing import List
from src.config.i18n import get_available_languages
from src.gui.translator_gui import TranslatorGUI

languages_available: List[str] = get_available_languages()

def show_usage() -> None:
    """Muestra el uso correcto del programa"""
    print("\n=== TRANSLATOR APP ===")
    print("Uso correcto:")
    print("  python app.py                 # Usa inglés por defecto")
    print("  python app.py --lang es       # Español")
    print("  python app.py --lang fr       # Francés")
    print("  python app.py --lang ru       # Ruso")
    print(f"\nIdiomas disponibles: {', '.join(languages_available)}")
    print("======================\n")

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aplicación de Traducción - Translator App",
        epilog="Ejemplos:\n  python app.py              # Inglés por defecto",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--lang", 
        type=str, 
        default="en", 
        choices=languages_available,
        help="Idioma de la interfaz (por defecto: en)"
    )
    return parser

def validate_language(language: str) -> bool:
    if language not in languages_available:
        print(f"❌ Error: Idioma '{language}' no disponible")
        show_usage()
        return False
    return True

def start_application(language: str) -> None:
    print(f"🚀 Iniciando traductor en idioma: {language}")
    gui = TranslatorGUI(language)
    gui.run()

def handle_keyboard_interrupt() -> None:
    """Maneja la interrupción por teclado (Ctrl+C)"""
    print("\n👋 Aplicación cerrada por el usuario")
    sys.exit(0)

def handle_application_error(error) -> None:
    """Maneja errores generales de la aplicación"""
    print(f"❌ Error al iniciar la aplicación: {error}")
    show_usage()
    sys.exit(1)

def configure_arguments() -> argparse.Namespace:
    parser = create_argument_parser()
    args = parser.parse_args()
    return args

def main() -> None:
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
