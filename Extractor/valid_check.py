import os
import PyPDF2
import re

file_path = 'Extractor/PaySlip1.pdf'

file_name, file_ext = os.path.splitext(file_path.split("/")[-1])
file_ext = file_ext.strip('.')

print(file_name, file_ext)
    
invalid_chars = ['#', '@', '%', '&','$', '{', '}', '\\', '<', '>']

invalid_chars_pattern = r'[' + r''.join(invalid_chars) + r']'

if re.search(invalid_chars_pattern, file_name):
    raise Exception("Error: Uploaded document name contains invalid file name")

max_size = 20 * 1024 * 1024 #20 MB

if os.path.getsize(file_path) > max_size:
    raise Exception("Error: Uploaded document max size is 20 MB")

allowed_ext = ['pdf', 'jpg', 'jpeg', 'png', 'tif']

is_allowed = False

for ext in allowed_ext:
    if file_ext.lower() == ext:
        is_allowed = True
        break
    
if not is_allowed:           
    raise Exception('Error: Uploaded document contains invalid file extension')

if file_ext.lower() == "pdf":
    with open(file_path, "rb") as file:

        pdf_reader = PyPDF2.PdfReader(file)

        if pdf_reader.is_encrypted:
            raise Exception("Error: Uploaded document cannot be encrypted or password protected.")