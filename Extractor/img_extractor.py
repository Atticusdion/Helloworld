from PIL import Image
import pytesseract
from modules import extract_w2_info

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = Image.open('E:\Helloworld\Extractor\W2.jpg')

ocr_text = pytesseract.image_to_string(image)

folder = 'Extractor\Extractions\Image'
extract_w2_info(ocr_text, folder)