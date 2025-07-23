from helpers.file_reader import read_pdf_file, read_docx_file, read_txt_file
from helpers.file_writer import write_pdf_file, write_docx_file, write_txt_file
import os
from apps.translator import TranslatorApp

class FileTranslator(TranslatorApp):
    def __init__(self, lang="en"):
        super().__init__(lang)
        self.suffixes_enable = {
            '.pdf': self.tramslate_pdf_file,
            '.docx': self.translate_docx_file,
            '.txt': self.translate_txt_file,
            # Add more file types as needed
        }

    def translate_file(self, file_path):
            text = []
            output_path = ""
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in self.suffixes_enable:
                # run the appropriate translation function based on the file type
                translation_function = self.suffixes_enable[file_extension]
                return translation_function(file_path)
            else:
                return "Unsupported file format. Please use .pdf, .docx, or .txt files."
            
    def tramslate_pdf_file(self, file_path):
        text = read_pdf_file(file_path)
        translated = [self.translate_line(line.strip()) for line in text]
        output_path = file_path.replace('.pdf', '_translated.pdf')
        write_pdf_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"

    def translate_docx_file(self, file_path):
        text = read_docx_file(file_path)
        translated = [self.translate_line(line.strip()) for line in text]
        output_path = file_path.replace('.docx', '_translated.docx')
        write_docx_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"

    def translate_txt_file(self, file_path):
        text = read_txt_file(file_path)
        translated = [self.translate_line(line.strip()) for line in text]
        output_path = file_path.replace('.txt', '_translated.txt')
        write_txt_file(translated, output_path)
        return f"File translated successfully and saved as {output_path.split('/')[-1]}"
