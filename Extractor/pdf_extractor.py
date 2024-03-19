import pdfplumber
from modules import extract_payslip_info

with pdfplumber.open('Extractor/PaySlip1.pdf') as pdf:
    pdf_text = pdf.pages[0].extract_text()

folder = 'Extractions/PDF'
extract_payslip_info(pdf_text, folder)