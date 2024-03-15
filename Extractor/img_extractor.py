from PIL import Image
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = Image.open('E:\Helloworld\Extractor\W2.jpg')

ocr_text = pytesseract.image_to_string(image)

def extract_w2_info(text):
    employee_match = re.search(r"2\. Employee Name and Address\.\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n", text, re.DOTALL)
    wages_match  = re.search(r'Pay\s+(\d+,\d+\.\d+)', text)
    employer_match  = re.search(r"© Employer's name, address, and ZIP code\n(.*?)\n(.*?)\n(.*?)\n", text, re.DOTALL)

    if employee_match:
        employee_name = employee_match.group(2).strip()
        employee_address = f"{employee_match.group(3).strip()}, {employee_match.group(4).strip()}"
    else:
        employee_name = None
        employee_address = None

    if employer_match:
        employer_name = employer_match.group(1).strip()
        employer_address = f"{employer_match.group(2).strip()}, {employer_match.group(3).strip()}"
    else:
        employer_name = None
        employer_address = None

    if wages_match:
        wages = wages_match.group(1)
    else:
        wages = None

    return {"name": employee_name, "address": employee_address, "wages": wages, "work_name": employer_name, "work_address": employer_address}


info = extract_w2_info(ocr_text)

print(f"Name: {info['name']}")
print(f"Address: {info['address']}")
print(f"Wages: {info['wages']}")
print(f"Company name: {info['work_name']}")
print(f"Company address: {info['work_address']}")