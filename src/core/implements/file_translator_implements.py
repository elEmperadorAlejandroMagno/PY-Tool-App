from core.interfaces.file_translator_interface import FileTranslatorInterface
from help.read_files import read_pdf_file, read_docx_file, read_txt_file
from help.write_files import write_pdf_file, write_docx_file, write_txt_file
from help.text_process import preprocess_text, postprocess_text
from typing import List, Dict, Any, Optional, Union, Callable
import os

class FileTranslatorImplements(FileTranslatorInterface):
    def __init__(self, suffixes_enable) -> None:
        super().__init__(suffixes_enable)

    def translate_file(self, _file_path) -> str:
        file_extension: str = os.path.splitext(_file_path)[1].lower()
        if file_extension in self.suffixes_enable:
            # run the appropriate translation function based on the file type
            translation_function: Callable[[str], str] = self.suffixes_enable[file_extension]
            return translation_function(_file_path)
        else:
            return "Unsupported file format. Please use .pdf, .docx, or .txt files."
            
    def translate_pdf_file(self, _file_path: str) -> str:
        text: List[str] = read_pdf_file(_file_path)
        translated: List[str] = [self._translate_text(line.strip()) for line in text if line.strip()]
        output_path: str = _file_path.replace('.pdf', '_translated.pdf')
        write_pdf_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"

    def translate_docx_file(self, _file_path: str) -> str:
        text: List[str] = read_docx_file(_file_path)
        translated: List[str] = [self._translate_text(line.strip()) for line in text if line.strip()]
        output_path: str = _file_path.replace('.docx', '_translated.docx')
        write_docx_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"

    def translate_txt_file(self, _file_path: str) -> str:
        text: List[str] = read_txt_file(_file_path)
        translated: List[str] = [self._translate_text(line.strip()) for line in text if line.strip()]
        output_path: str = _file_path.replace('.txt', '_translated.txt')
        write_txt_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"