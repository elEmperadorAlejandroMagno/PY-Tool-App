from googletrans import Translator
from translations.translations import get_translations as translations

class TranslatorApp:
    def __init__(self, lang="en"):
        self.lang = lang
        self.t = translations.get(lang, translations["en"])["translator"]
        self.translator = Translator()

    def _translate_text(self, text):
        # Siempre detecta el idioma de origen y traduce al español
        try:
            detected_lang = self.translator.detect(text).lang
            if detected_lang == "es":
                return text
            translated = self.translator.translate(text, src=detected_lang, dest='es')
        except Exception:
            return f"Error: unable to translate text. Try again later."
        return translated.text

    def translate_line(self, text):
        return self._translate_text(text)

    def translate_file(self, file_path):
        try:
            print("Translating file, wait a moment...")
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            return f"Error: file not found {file_path}"
        
        output_path = file_path.replace('.txt', '_translated.txt')
        try:
            with open(output_path, 'w', encoding='utf-8') as out_file:
                for line in lines:
                    translated_line = self.translate_line(line.strip())
                    out_file.write(translated_line + '\n')
        except Exception:
            return f"Error writing to file"
        return f"{self.t['output_path']}: {output_path}"

# Funciones auxiliares separadas para la interacción con el usuario

def main(lang="en"):
    app = TranslatorApp(lang)
    tipo = input("¿Traducir una línea (1) o un archivo (2)?: ")
    if tipo == "1":
        text = input("Introduce el texto: ")
        print("Traducción:", app.translate_line(text))
    elif tipo == "2":
        file_path = input("Introduce el path del archivo: ")
        print(app.translate_file(file_path))
    else:
        print("Opción no válida.")

if __name__ == '__main__':
    main()
