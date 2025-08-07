import os
from typing import Dict, List, Callable, Any
from translator import TranslatorApp

class FileTranslator(TranslatorApp):
    def __init__(self, _entry_lang, _output_lang) -> None:
        super().__init__(from_lang=_entry_lang, to_lang=_output_lang)
        self.suffixes_enable: Dict[str, Callable[[str], str]] = {
            '.pdf': self.translate_pdf_file,
            '.docx': self.translate_docx_file,
            '.txt': self.translate_txt_file,
            # Add more file types as needed
        }
        self._file_path: str = ""

    def translate_file(self, _file_path) -> str:
        pass

    @property
    def file_path(self) -> str:
        return self._file_path
    
    @file_path.setter
    def file_path(self, path: str) -> None:
        if os.path.isfile(path):
            self._file_path = path
        else:
            raise ValueError("Invalid file path provided.")

