from apps.help.read_files import read_pdf_file, read_docx_file, read_txt_file
from apps.help.write_files import write_pdf_file, write_docx_file, write_txt_file
from apps.translator import TranslatorApp

class FileTranslator(TranslatorApp):
    def translate_file(self, file_path):
            text = []
            output_path = ""
            if file_path.endswith('.pdf'):
                text = read_pdf_file(file_path)
                translated = [self.translate_line(line.strip()) for line in text]
                output_path = file_path.replace('.pdf', '_translated.pdf')
                write_pdf_file(translated, output_path)
                return f"File translated successfully and saved as {output_path.split('/')[-1]}"
            elif file_path.endswith('.docx'):
                text = read_docx_file(file_path)
                translated = [self.translate_line(line.strip()) for line in text]
                output_path = file_path.replace('.docx', '_translated.docx')
                write_docx_file(translated, output_path)
                return f"File translated successfully and saved as {output_path.split('/')[-1]}"
            elif file_path.endswith('.txt'):
                text = read_txt_file(file_path)
                translated = [self.translate_line(line.strip()) for line in text]
                output_path = file_path.replace('.txt', '_translated.txt')
                write_txt_file(translated, output_path)
                return f"File translated successfully and saved as {output_path.split('/')[-1]}"
            else:
                return "Unsupported file format. Please use .pdf, .docx, or .txt files."
