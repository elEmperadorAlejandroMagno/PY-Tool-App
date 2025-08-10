from src.core.translator import TranslatorApp
from src.core.implements.text_translator_implements import TextTranslatorImplements
from src.core.implements.file_translator_implements import FileTranslatorImplements


def create_translator_app(lang: str = "en") -> TranslatorApp:
    """Factory that wires default implementations to the app using interfaces."""
    text_impl = TextTranslatorImplements()
    file_impl = FileTranslatorImplements()
    return TranslatorApp(lang=lang, text_translator=text_impl, file_translator=file_impl)

