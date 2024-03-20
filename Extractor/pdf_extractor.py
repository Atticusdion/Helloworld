import pdfplumber
from modules_set1 import extract_pdf_info

with pdfplumber.open('Extractor/PaySlip1.pdf') as pdf:
    pdf_text = pdf.pages[0].extract_text()

folder = 'Extractor/Extractions/PDF'

extract_pdf_info(pdf_text, folder)