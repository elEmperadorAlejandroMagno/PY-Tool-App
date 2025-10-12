from src.config.i18n import get_text, get_available_languages
from typing import Any, Optional
from src.core.interfaces.text_translator_interface import TextTranslatorInterface
from src.core.interfaces.file_translator_interface import FileTranslatorInterface
from src.core.interfaces.phonetic_transcription_interface import PhoneticTranscriptionInterface

class TranslatorApp:
    def __init__(self, lang: str, text_translator: TextTranslatorInterface, file_translator: FileTranslatorInterface, phonetic_transcriber: Optional[PhoneticTranscriptionInterface] = None) -> None:
        self.languages: list[str] = get_available_languages()
        self.lang: str = lang
        self.t: dict[str, Any] = get_text(self.lang)
        self._entry_lang: str = "detect"
        self._output_lang: str = lang
        self._accent: str = "rp"  # Acento por defecto para transcripción fonética
        # dependencies (interfaces)
        self._text_interface = text_translator
        self._file_interface = file_translator
        self._phonetic_interface = phonetic_transcriber

    def translate_text(self, text: str) -> str:
        return self._text_interface.translate_text(text, self._entry_lang, self._output_lang)

    def translate_file(self, file_path: str) -> str:
        return self._file_interface.translate_file(file_path, self._entry_lang, self._output_lang)
    
    def transcribe_to_ipa(self, text: str) -> str:
        """Transcribe text to IPA phonetic notation."""
        if not self._phonetic_interface:
            raise RuntimeError("Phonetic transcription service not available")
        return self._phonetic_interface.transcribe_to_ipa(text, self._accent)
    
    def get_supported_accents(self) -> list[str]:
        """Get list of supported phonetic accents."""
        if not self._phonetic_interface:
            return []
        return self._phonetic_interface.get_supported_accents()
    
    def is_phonetic_transcription_available(self) -> bool:
        """Check if phonetic transcription is available."""
        return self._phonetic_interface is not None

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
    
    @property
    def accent(self) -> str:
        return self._accent
    
    @accent.setter
    def accent(self, accent: str) -> None:
        if self._phonetic_interface and self._phonetic_interface.is_accent_supported(accent):
            self._accent = accent
        else:
            raise ValueError(f"Accent '{accent}' is not supported")


def main(lang: str = "en") -> None:
    from src.gui.translator_gui import TranslatorGUI
    gui = TranslatorGUI(lang)
    gui.run()

if __name__ == '__main__':
    main()
