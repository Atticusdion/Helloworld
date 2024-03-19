import pdfplumber
import pandas as pd
import re

with pdfplumber.open('Extractor/PaySlip1.pdf') as pdf:
    text = pdf.pages[0].extract_text()

def extract_payslip_info(payslip_text):

    lines = payslip_text.split('\n')
    
    employee_name = None
    basic_pay = None
    net_pay = None
    house_rent_allowance = None
    address = None
    
    for line in lines:
        if 'Employee Name :' in line:
            employee_name = line.split('Employee Name :')[1].strip()
        
        elif 'Basic Pay' in line:
            basic_pay = float(re.findall(r'\d+', line)[0])
        
        elif 'Net Pay' in line:
            net_pay = float(line.split()[2])
        
        elif 'House Rent Allowance' in line:
            house_rent_allowance = float(re.findall(r'\d+', line)[0])
        
        elif 'Zoonodle Inc' in line:
            address = line.strip()
    
    return {
        'employee_name': employee_name,
        'basic_pay': basic_pay,
        'net_pay': net_pay,
        'house_rent_allowance': house_rent_allowance,
        'address': address
    }

print(extract_payslip_info(text))