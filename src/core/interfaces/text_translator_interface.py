from abc import ABC, abstractmethod

class TextTranslatorInterface(ABC):
    @abstractmethod
    def translate_text(self, text: str, entry_lang: str, output_lang: str) -> str:
        """Translate a text from entry_lang to output_lang and return the translated string."""
        raise NotImplementedError
