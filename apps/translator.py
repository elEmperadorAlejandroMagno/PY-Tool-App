from translations.translations import get_translations as translations
from googletrans import Translator
import os

class TranslatorApp:
    def __init__(self, lang="en"):
        self.translator = Translator()
        self.lang = lang
        self.t = translations.get(lang, translations["en"])["translator"]
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
    from app_gui.translator_gui import TranslatorGUI
    gui = TranslatorGUI(lang)
    gui.run()

if __name__ == '__main__':
    main()