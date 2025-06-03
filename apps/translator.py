from googletrans import Translator
from translations.translations import get_translations as translations
import asyncio

class TranslatorApp:
    def __init__(self, lang="en"):
        self.lang = lang
        self.t = translations.get(lang, translations["en"])["translator"]
        self.translator = Translator()

    async def _translate_text(self, text, lang=None):
        lang = lang or self.lang
        if not lang:
            detected_lang = await self.translator.detect(text)
            lang = detected_lang.lang
        translated = await self.translator.translate(text, src=lang, dest='es')
        return translated.text.lower()

    def translate_line(self, text, lang=None):
        return asyncio.run(self._translate_text(text, lang))

    def translate_file(self, file_path, lang=None):
        lang = lang or self.lang
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        output_path = file_path.replace('.txt', '_translated.txt')
        with open(output_path, 'w', encoding='utf-8') as out_file:
            for line in lines:
                translated_line = self.translate_line(line.strip(), lang)
                out_file.write(translated_line + '\n')
        return f"{self.t['output_path']}: {output_path}"

# Funciones auxiliares separadas para la interacción con el usuario

def main():
    app = TranslatorApp()
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
