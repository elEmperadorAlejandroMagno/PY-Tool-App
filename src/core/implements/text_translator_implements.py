from src.core.interfaces.text_translator_interface import TextTranslatorInterface
from src.services.googletrans_services import translate_text_delegate

class TextTranslatorImplements(TextTranslatorInterface):
    def translate_text(self, text: str, entry_lang: str, output_lang: str) -> str:
        try:
            src_input = (text, entry_lang, output_lang)
            text_translated = translate_text_delegate(src_input)
            return text_translated
        except Exception as e:
            return f"Error: unable to translate text. Try again later. ({str(e)})"
