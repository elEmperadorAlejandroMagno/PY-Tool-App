from src.config.translations import get_translations as translations
from googletrans import Translator
from typing import List, Dict, Any, Optional, Union
import os

class TranslatorApp:
    def __init__(self, lang: str = "en") -> None:
        self.translator: Translator = Translator()
        self.languages: List[str] = ["es", "fr", "ru", "en", "zh"]
        self.lang: str = lang
        self.t: Dict[str, Any] = translations.get(lang, translations["en"])["translator"]
        self._entry_lang: str = "detect"
        self._output_lang: str = lang

    def _translate_text(self, text: str) -> str:
        try:
            src_lang: str = self._entry_lang
            dest_lang: str = self._output_lang
            if src_lang == "detect":
                detected_lang: str = self.translator.detect(text).lang
                src_lang = detected_lang
            if src_lang == dest_lang:
                return text
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
            return str(translated.text)
        except Exception:
            return "Error: unable to translate text. Try again later."

    @property
    def entry_language(self) -> str:
        return self._entry_lang

    @entry_language.setter
    def entry_language(self, lang: str) -> None:
        self._entry_lang = lang

    @property
    def output_language(self) -> str:
        return self._output_lang

    @output_language.setter
    def output_language(self, lang: str) -> None:
        self._output_lang = lang

def main(lang: str = "en") -> None:
    from src.gui.translator_gui import TranslatorGUI
    gui = TranslatorGUI(lang)
    gui.run()

if __name__ == '__main__':
    main()
