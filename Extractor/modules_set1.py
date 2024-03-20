import re
import json
import os
import string
import pandas as pd
import pdfplumber

## File name sanitizer

def sanitize_name(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in name if c in valid_chars)
    sanitized = sanitized.replace(' ', '_')
    return sanitized

## Extractions dumper

def directory(destination, details, name):

    filename = f"{sanitize_name(name)}_extractions.json"
    destination_path = os.path.join(destination, filename)
    with open(destination_path, 'w') as file:
        json.dump(details, file, indent=4)

## PDF info extarctor

def extract_pdf_info(text, destination):

    lines = text.split('\n')

    address = None
    
    for index, line in enumerate(lines):
        if 'Employee Name :' in line:
            employee_name = line.split('Employee Name :')[1].strip()
        
        elif 'Total Earnings' in line:
            total_pay = float(re.findall(r'\d+', line)[0])
        
        elif 'Net Pay' in line:
            net_pay = float(line.split()[2])
        
        elif 'House Rent Allowance' in line:
            house_rent_allowance = float(re.findall(r'\d+', line)[0])
    
    pdf_details = {
        'employee_name': employee_name,
        'total_pay': total_pay,
        'net_pay': net_pay,
        'house_rent_allowance': house_rent_allowance
    }

    directory(destination, pdf_details, employee_name)

    return pdf_details

## Image info extractor

def extract_img_info(text, destination):
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
        wages = float(wages_match.group(1).replace(',', ''))
    else:
        wages = None

    img_details = {
        'name': employee_name, 
        'address': employee_address, 
        'wages': wages, 
        'work_name': employer_name, 
        'work_address': employer_address
    }

    directory(destination, img_details, employee_name)

    return img_details

## Table info from PDF -> CSV

def extract_csv(file_path):

    with pdfplumber.open(file_path) as pdf:
        table = pdf.pages[0].extract_table()

    rows = []

    for row in table[1:]:
        subrows = [[] for _ in range(max(len(cell.split('\n')) for cell in row))]
        for i, cell in enumerate(row):
            values =  cell.split('\n')
            for j, value in enumerate(values):
                subrows[j].append(value)
        
        rows.extend(subrows)

    df = pd.DataFrame(rows, columns = table[0])

    df.to_csv('PaySlip1_table.csv', index = False)

    return df

