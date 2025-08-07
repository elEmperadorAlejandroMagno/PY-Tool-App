from core.interfaces.text_translator_interface import TextTranslatorInterface
from src.services.googletrans_services import translate_text_delegate
from src.services.spacy_text_process import preprocess_text, postprocess_text
from typing import List, Dict, Any, Optional, Union

class TextTranslatorImplements(TextTranslatorInterface):
    def __init__(self, lang: str = "en") -> None:
        super().__init__(lang)

    def _preprocess_text(self, text_object: object) -> str:
        try:
            text_processed = preprocess_text(text_object)
            return text_processed
        except Exception as e:
            return f"Error: unable to preprocess text. Try again later. ({str(e)})"
        
    def _postprocess_text(self, original_text: object, processed_text) -> str:
        try:
            text_processed = postprocess_text(original_text, processed_text)
            return text_processed
        except Exception as e:
            return f"Error: unable to postprocess text. Try again later. ({str(e)})"

    def _translate_text(self, text: str) -> str:
        try:
            src_input = (text, self._entry_lang, self._output_lang)
            text_translated = translate_text_delegate(src_input)
            return text_translated
        except Exception as e:
            return f"Error: unable to translate text. Try again later. ({str(e)})"