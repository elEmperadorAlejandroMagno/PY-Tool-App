from translator import TranslatorApp
from src.services.spacy_text_process import cargar_modelo

class TextTranslator(TranslatorApp):

    def __init__(self, lang: str = "en") -> None:
        super().__init__(lang)
        self.original_text_object = cargar_modelo(self.text, lang)
        self.text = ""
        self.translated_text = ""

    def preprocess_text(self) -> str:
        self.text = self._preprocess_text(self.text, self.text_object)
        return self.text

    def translate_line(self, text):
        self.translated_text = self._translate_text(text)
        return self.translated_text
    
    def postprocess_text(self):
        self.text = self._postprocess_text(self.original_text_object, self.text)
        return self.text