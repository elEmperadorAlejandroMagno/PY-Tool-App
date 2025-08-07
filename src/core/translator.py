from src.config.i18n import get_text, get_available_languages
from typing import List, Dict, Any, Optional, Union
import os

class TranslatorApp:
    def __init__(self, lang: str = "en") -> None:
        self.languages: List[str] = get_available_languages()
        self.lang: str = lang
        self.t: Dict[str, Any] = get_text(self.lang)
        self._entry_lang: str = "detect"
        self._output_lang: str = lang

    def translate_text(self, text: str) -> str:
        pass

    def translate_file(self, file_path: str) -> str:
        pass

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
