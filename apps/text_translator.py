from apps.translator import TranslatorApp

class TextTranslator(TranslatorApp):
    def translate_line(self, text):
        return self._translate_text(text)