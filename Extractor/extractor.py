from PIL import Image
import pytesseract

image = Image.open('E:\Helloworld\Extractor\W2.jpg')

text = pytesseract.image_to_string(image)

print(text)