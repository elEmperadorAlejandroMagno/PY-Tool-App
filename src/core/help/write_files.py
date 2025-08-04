import docx
from fpdf import FPDF
import re

def clean_text(text):
    return re.sub(r'[^\x00-\xff]', '*', text)

def write_docx_file(paragraphs, output_path):
    try:
      doc = docx.Document()
      for para in paragraphs:
          doc.add_paragraph(para)
      doc.save(output_path)
    except Exception as e:
        return "Error writing to file"

def write_txt_file(text, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            for line in text:
                out_file.write(line + '\n')
    except Exception:
        return "Error writing to file"
    
def write_pdf_file(paragraphs, output_path):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for para in paragraphs:
            pdf.multi_cell(0, 10, clean_text(para))
        print(pdf.output(output_path))
    except Exception as e:
        print(f"Error writing PDF: {e}")  # <-- Esto te da información útil
        return "Error writing to file"