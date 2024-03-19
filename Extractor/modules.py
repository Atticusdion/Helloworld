import re
import json
import os
import string

def sanitize_name(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in name if c in valid_chars)
    sanitized = sanitized.replace(' ', '_')
    return sanitized

def directory(destination, details, name):

    filename = f"{sanitize_name(name)}_extractions.json"
    destination_path = os.path.join(destination, filename)
    with open(destination_path, 'w') as file:
        json.dump(details, file, indent=4)

def extract_payslip_info(text, destination):

    lines = text.split('\n')
    
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
    
    payslip_details = {
        'employee_name': employee_name,
        'basic_pay': basic_pay,
        'net_pay': net_pay,
        'house_rent_allowance': house_rent_allowance,
        'address': address
    }

    directory(destination, payslip_details, employee_name)

    return payslip_details

def extract_w2_info(text, destination):
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

    w2_details = {
        'name': employee_name, 
        'address': employee_address, 
        'wages': wages, 
        'work_name': employer_name, 
        'work_address': employer_address
    }

    directory(destination, w2_details, employee_name)

    return w2_details