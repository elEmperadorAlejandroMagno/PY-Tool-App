from googletrans import Translator
from apps.help.read_files import read_pdf_file, read_docx_file, read_txt_file
from translations.translations import get_translations as translations
import os

class TranslatorApp:
    def __init__(self, lang="en"):
        self.lang = lang
        self.t = translations.get(lang, translations["en"])["translator"]
        self.translator = Translator()
        self._entry_lang = "detect"
        self._output_lang = lang

    def _translate_text(self, text):
        try:
            src_lang = self._entry_lang
            dest_lang = self._output_lang
            if src_lang == "detect":
                detected_lang = self.translator.detect(text).lang
                src_lang = detected_lang
            if src_lang == dest_lang:
                return text
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
            return translated.text
        except Exception:
            return "Error: unable to translate text. Try again later."

    def translate_line(self, text):
        return self._translate_text(text)

    def translate_file(self, file_path):
        text = []
        output_path = ""
        if file_path.endswith('.pdf'):
            text = self.read_pdf_file(file_path)
            output_path = file_path.replace('.pdf', '_translated.txt')
        elif file_path.endswith('.docx'):
            text = self.read_docx_file(file_path)
            output_path = file_path.replace('.docx', '_translated.txt')
        elif file_path.endswith('.txt'):
            text = self.read_txt_file(file_path)
            output_path = file_path.replace('.txt', '_translated.txt')
        else:
            return "Unsupported file format. Please use .pdf, .docx, or .txt files."
        try:
            with open(output_path, 'w', encoding='utf-8') as out_file:
                for line in text:
                    translated_line = self.translate_line(line.strip())
                    out_file.write(translated_line + '\n')
        except Exception:
            return "Error writing to file"
        return f"{self.t['output_path']}: {os.path.basename(output_path)}"

    @property
    def entry_language(self):
        return self._entry_lang

    @entry_language.setter
    def entry_language(self, lang):
        self._entry_lang = lang

    @property
    def output_language(self):
        return self._output_lang

    @output_language.setter
    def output_language(self, lang):
        self._output_lang = lang

def main(lang="en"):
    from apps.guis.translator_gui import TranslatorGUI
    gui = TranslatorGUI(lang)
    gui.run()

if __name__ == '__main__':
    main()