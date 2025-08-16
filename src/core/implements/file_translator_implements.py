from collections.abc import Callable
import os
from src.core.interfaces.file_translator_interface import FileTranslatorInterface
from src.core.help.read_files import read_pdf_file, read_docx_file, read_txt_file
from src.core.help.write_files import write_pdf_file, write_docx_file, write_txt_file
from src.services.googletrans_services import translate_text_delegate

class FileTranslatorImplements(FileTranslatorInterface):
    def __init__(self) -> None:
        super().__init__()
        self.suffixes_enable = {
            '.pdf': self.translate_pdf_file,
            '.docx': self.translate_docx_file,
            '.txt': self.translate_txt_file,
        }

    def translate_file(self, file_path: str, entry_lang: str, output_lang: str) -> str:
        self.validate_path(file_path)
        file_extension: str = os.path.splitext(file_path)[1].lower()
        if file_extension in self.suffixes_enable:
            translation_function: Callable[[str, str, str], str] = self.suffixes_enable[file_extension]
            return translation_function(file_path, entry_lang, output_lang)
        else:
            return "Unsupported file format. Please use .pdf, .docx, or .txt files."

    def translate_pdf_file(self, file_path: str, entry_lang: str, output_lang: str) -> str:
        text: list[str] = read_pdf_file(file_path)
        translated: list[str] = [translate_text_delegate((line.strip(), entry_lang, output_lang)) for line in text if line.strip()]
        output_path: str = file_path.replace('.pdf', '_translated.pdf')
        write_pdf_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"

    def translate_docx_file(self, file_path: str, entry_lang: str, output_lang: str) -> str:
        text: list[str] = read_docx_file(file_path)
        translated: list[str] = [translate_text_delegate((line.strip(), entry_lang, output_lang)) for line in text if line.strip()]
        output_path: str = file_path.replace('.docx', '_translated.docx')
        write_docx_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"

    def translate_txt_file(self, file_path: str, entry_lang: str, output_lang: str) -> str:
        text: list[str] = read_txt_file(file_path)
        translated: list[str] = [translate_text_delegate((line.strip(), entry_lang, output_lang)) for line in text if line.strip()]
        output_path: str = file_path.replace('.txt', '_translated.txt')
        write_txt_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"
