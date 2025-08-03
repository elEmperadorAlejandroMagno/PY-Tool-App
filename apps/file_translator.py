from help.write_files import read_pdf_file, read_docx_file, read_txt_file
from help.read_files import write_pdf_file, write_docx_file, write_txt_file
import os
from typing import Dict, List, Callable, Any
from apps.translator import TranslatorApp

class FileTranslator(TranslatorApp):
    def __init__(self, lang: str = "en") -> None:
        super().__init__(lang)
        self.suffixes_enable: Dict[str, Callable[[str], str]] = {
            '.pdf': self.translate_pdf_file,
            '.docx': self.translate_docx_file,
            '.txt': self.translate_txt_file,
            # Add more file types as needed
        }

    def translate_file(self, file_path: str) -> str:
        file_extension: str = os.path.splitext(file_path)[1].lower()
        if file_extension in self.suffixes_enable:
            # run the appropriate translation function based on the file type
            translation_function: Callable[[str], str] = self.suffixes_enable[file_extension]
            return translation_function(file_path)
        else:
            return "Unsupported file format. Please use .pdf, .docx, or .txt files."
            
    def translate_pdf_file(self, file_path: str) -> str:
        text: List[str] = read_pdf_file(file_path)
        translated: List[str] = [self._translate_text(line.strip()) for line in text if line.strip()]
        output_path: str = file_path.replace('.pdf', '_translated.pdf')
        write_pdf_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"

    def translate_docx_file(self, file_path: str) -> str:
        text: List[str] = read_docx_file(file_path)
        translated: List[str] = [self._translate_text(line.strip()) for line in text if line.strip()]
        output_path: str = file_path.replace('.docx', '_translated.docx')
        write_docx_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"

    def translate_txt_file(self, file_path: str) -> str:
        text: List[str] = read_txt_file(file_path)
        translated: List[str] = [self._translate_text(line.strip()) for line in text if line.strip()]
        output_path: str = file_path.replace('.txt', '_translated.txt')
        write_txt_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"
