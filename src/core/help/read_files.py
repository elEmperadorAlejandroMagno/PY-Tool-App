import pdfplumber as PDF
import docx
import os
from typing import List

def read_pdf_file(file_path: str) -> List[str]:
        text: List[str] = []
        try:
            with PDF.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        paragraphs = page_text.split('\n')
                        for para in paragraphs:
                            para = para.strip()
                            if para:
                                text.append(para)
        except Exception:
            return f"Error: unable to read file {file_path}"
        return text


def read_docx_file(file_path: str) -> List[str]:
        text = []
        try:
            doc = docx.Document(file_path)
            text = [para.text for para in doc.paragraphs if para.text.strip()]
        except Exception:
            return f"Error: unable to read file {file_path}"
        return text

def read_txt_file(file_path: str) -> List[str]:
        text = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.readlines()
        except FileNotFoundError:
            return f"Error: file not found {os.path.basename(file_path)}"
        return text
