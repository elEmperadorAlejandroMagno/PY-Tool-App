from translator import TranslatorApp
from src.services.spacy_text_process import cargar_modelo

class TextTranslator(TranslatorApp):

    def __init__(self, _entry_lang, _output_lang) -> None:
        super().__init__(from_lang=_entry_lang, to_lang=_output_lang)
        self.original_text_object = cargar_modelo(self.text, self.from_lang)
        self.text = ""
        self.translated_text = ""

    def translate_text(self) -> str:
        pass