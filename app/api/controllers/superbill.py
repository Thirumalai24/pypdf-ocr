import io
import json
import re
from pypdf import PdfReader

class PdfExtraction:
    def __init__(self, pdf_content):
        try:
            read_pdf_file = self.extract_text(pdf_content)
            # print(read_pdf_file,"Raw data")
            
            # Parse and convert to JSON
            self.json_output = self.parse_to_json(read_pdf_file)
            
        except Exception as e:
            print(f'Exception encountered while executing operation: {e}')
            self.json_output = None

    # Extract text from pdf
    def extract_text(self,pdf_content):
        try:
            pdf_file = io.BytesIO(pdf_content)
            reader = PdfReader(pdf_file)
            page = reader.pages[0]
            text = page.extract_text()
            return text
            
        except Exception as e:
            print(f'Exception encountered while extracting Text from pdf: {e}')
            return None

    # Function to parse the text to JSON format
    def parse_to_json(self, text):
        try:
            json_data = {
                "client": self.extract_client(text),
                "insured": self.extract_insured(text),
                "responsibleparty": self.extract_responsible_party(text),
                "provider": self.extract_provider(text),
                "practice": self.extract_practice(text),
                "diagnosisCodes": self.extract_diagnosis_codes(text),
                "services": self.extract_services(text),
                "totalFees": self.extract_total_fees(text),
                "totalPaid": self.extract_total_paid(text)
            }
            return json_data
            
        except Exception as e:
            print(f'Exception encountered while parsing JSON Data: {e}')
            return None

    # Client
    def extract_client(self, text):
        try:
            start = text.find("Client") + len("Client")
            if "Insured" in text:
                end = text.find("Insured")
            elif "Responsible party" in text:
                end = text.find("Responsible party")
            elif "Provider" in text:
                end = text.find("Provider")
            else:
                end = text.find("\n", start)
                for _ in range(3):
                    next_line = text.find("\n", end + 1)
                    if next_line == -1:
                        break
                    end = next_line

            client_data = text[start:end].strip().replace("\n", ", ")
            
            # Check for the "Statement" word and trim the "Statement"
            if "Statement" in client_data:
                client_data = client_data.split("Statement")[0].strip()  
                          
             # Split by comma and trim spaces
            client_parts = [part.strip() for part in client_data.split(',')]
            
            # Initialize client information
            client_info = {
                "rawData": client_data,
                "name": None,
                "dob": None,
                "mob": None,
                "email": None
            }
            
            # Iterate through parts and assign to corresponding keys
            for part in client_parts:
                if "DOB:" in part:
                    client_info["dob"] = part.split(":")[1].strip() if len(part.split(":")) > 1 else None
                elif "(" in part and ")" in part:
                    client_info["mob"] = part.strip()
                elif "@" in part:
                    client_info["email"] = part.strip()
                else:
                    client_info["name"] = part.strip()
            
            return client_info

        except Exception as e:
            print(f'Exception encountered while extracting Client from text: {e}')
            return None

    # Insured   
    def extract_insured(self, text):
        try:
            start = text.find("Insured") + len("Insured")
            if start == -1 + len("Insured"):
                return None  # 'Insured' section not found

            end = text.find("Provider", start)
            insured_data = text[start:end].strip().replace("\n", ", ")

            # Check for the "Statement" word and trim if necessary
            if "Statement" in insured_data:
                insured_data = insured_data.split("Statement")[0].strip()

            # Initialize insured information
            insured_info = {
                "rawData": insured_data,
                "name": None,
                "company": None,
                "member": None,
                "plan": None,
                "group": None
            }

            # Split by comma and trim spaces
            insured_parts = [part.strip() for part in insured_data.split(',')]

            # Assign parts to insured_info
            for part in insured_parts:
                if "Company:" in part:
                    insured_info["company"] = part.split(":")[1].strip() if len(part.split(":")) > 1 else None
                elif "Member:" in part:
                    insured_info["member"] = part.split(":")[1].strip() if len(part.split(":")) > 1 else None
                elif "Plan:" in part:
                    insured_info["plan"] = part.split(":")[1].strip() if len(part.split(":")) > 1 else None
                elif "Group:" in part:
                    insured_info["group"] = part.split(":")[1].strip() if len(part.split(":")) > 1 else None
                else:
                    insured_info["name"] = part.strip()

            return insured_info
        except Exception as e:
            print(f'Exception encountered while extracting Insured from text: {e}')
            return None
        
       #responsible party   
    def extract_responsible_party(self, text):
        try:
            start = text.find("Responsible party") + len("Responsible party")
            if start == -1 + len("Responsible party"):
                return None  # 'Responsible party' section not found

            end = text.find("Provider", start)
            responsible_data = text[start:end].strip().replace("\n", ", ")

            # Check for the "Statement" word and trim if necessary
            if "Statement" in responsible_data:
                responsible_data = responsible_data.split("Statement")[0].strip()

            responsible_parts = [part.strip() for part in responsible_data.split(',')]

            # Initialize responsible party information
            responsible_info = {
                "rawData":responsible_data,
                "name": None,
                "mob": None,
                "email": None
            }

             # Iterate through parts and assign to corresponding keys
            for part in responsible_parts:
                if "(" in part and ")" in part:
                    responsible_info["mob"] = part.strip()
                elif "@" in part:
                    responsible_info["email"] = part.strip()
                else:
                    responsible_info["name"] = part.strip()

            return responsible_info
            
        except Exception as e:
            print(f'Exception encountered while extracting Insured from text: {e}')
            return None

    # Provider
    def extract_provider(self, text):
        try:
            start = text.find("Provider") + len("Provider")
            end = text.find("Practice")
            # license_data = None
            # Check for Licenses or License
            # if(text.find("Licenses") != -1 or text.find("License") != -1):
            #     if(text.find("Licenses") != -1):
            #         license_data = text[text.find("Licenses"):text.find("Practice")].strip().replace("\n","")
            #         license_data = license_data.replace("Licenses: ","")
            #         end = text.find("Licenses")
            #     else:
            #         license_data = text[text.find("License"):text.find("Practice")].strip().replace("\n", "")
            #         license_data = license_data.replace("License: ","")
            #         end = text.find("License")

            provider_data = text[start:end].strip().replace("\n", ",")
            
            # Split by comma and trim spaces
            provider_parts = [part.strip() for part in provider_data.split(',')]

            # Initialize provider information
            provider_info = {
                "rawData": provider_data,
                "name": None,
                "npi": None,
                "mob": None,
                "email": None,
                # "License": license_data
            }

            # Iterate through parts and assign to corresponding keys
            for i, part in enumerate(provider_parts):
                if i == 0:
                    provider_info["name"] = part.strip()
                elif "NPI:" in part:
                    provider_info["npi"] = part.split(":")[1].strip() if len(part.split(":")) > 1 else None
                elif "(" in part and ")" in part:
                    provider_info["mob"] = part.strip()
                elif "@" in part:
                    provider_info["email"] = part.strip()
                
            return provider_info

        except Exception as e:
            print(f'Exception encountered while extracting Provider from text: {e}')
            return None

    # Practice
    def extract_practice(self, text):
        try:
            start = text.find("Practice") + len("Practice")
            end = text.find("DX Diagnosis Code")
            practice_data = text[start:end].strip().replace("\n",",")

            # Check for the "Date" word and trim if necessary
            if "Date" in practice_data:
                practice_data = practice_data.split("Date")[0].strip()
                
            # Split practice_data by comma and trim spaces
            practice_parts = [part.strip() for part in practice_data.split(',')]
            
            # Initialize provider information
            practice_info = {
                "rawData": practice_data,
                "taxId": None,
                "npi": None   
            }
            #Iterate through parts and assign to corresponding keys
            for part in practice_parts:
                if "Tax ID:" in part:
                    practice_info["taxId"] = part.split(":")[1].strip() if len(part.split(":")) > 1 else None
                elif "NPI:" in part:
                    practice_info["npi"] = part.split(":")[1].strip() if len(part.split(":")) > 1 else None

            return practice_info 
        except Exception as e:
            print(f'Exception encountered while extracting Practice from text: {e}')
            return None

    # Diagnosis Codes(Dx, Diagnosis code)
    def extract_diagnosis_codes(self, text):
        try:
            start = text.find("DX Diagnosis Code") + len("DX Diagnosis Code")
            if start == -1 + len("DX Diagnosis Code"):
                return None  # 'DX Diagnosis Code' section not found

            end = text.find("Date POS Service DX Description Units Fee Paid")
            diagnosis_data = text[start:end].strip()
            diagnosis_codes = []
            for line in diagnosis_data.split('\n'):
                if line:
                    parts = line.split(' ', 1)  # Split only at the first space
                    dx = parts[0].strip()
                    diagnosis_code, diagnosis_name = parts[1].split(' - ', 1) if ' - ' in parts[1] else (parts[1], "")

                     # Handle null DX case
                    if dx.lower() == "null":
                        diagnosis_codes.append({
                            "rawData": line,
                            "dx": None,
                            "diagnosisCode": diagnosis_code.strip(),
                            "description": diagnosis_name.strip() if diagnosis_name else None
                        })
                    else:
                        diagnosis_codes.append({
                            "rawData": line,
                            "dx": dx,
                            "diagnosisCode": diagnosis_code.strip(),
                            "description": diagnosis_name.strip() if diagnosis_name else None
                        })

            return diagnosis_codes
        except Exception as e:
            print(f'Exception encountered while extracting diagnosis codes from text: {e}')
            return None
        
    #Process the Service Table 
    def process_service_text(self, text):
        service_text = ""  # Variable to store the processed service text
        start = text.find("Date POS Service DX Description Units Fee Paid") + len("Date POS Service DX Description Units Fee Paid")
        end = text.find("Total Fees")
        services_data = text[start:end].strip()
        
        date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
        lines = services_data.split('\n')
        i = 0
        while i < len(lines):
            current_line = lines[i].strip()
            if date_pattern.match(current_line):
                # Check if the next line is also a part of the current service entry
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    
                    #check the current line end - and append the second 
                    if current_line.endswith(' -'):
                        current_line = current_line.rstrip(' -') + '-' + next_line
                        i += 1  # Skip the next line since it's already included
                        
                    elif not date_pattern.match(next_line):
                        current_line += ' ' + next_line
                        i += 1  # Skip the next line since it's already included
                        
                    # Split the service code and dx value
                    parts = current_line.split(' ')
                    service_code = parts[2]
                    if '-' in service_code:
                        service_code_parts = service_code.split('-')
                        parts[2] = service_code_parts[0] + '-' + service_code_parts[1][:2] 
                        parts.insert(3, service_code_parts[1][2:]) 
                    current_line = ' '.join(parts)
                        
                    service_text += current_line + "\n"
                else:
                    service_text += current_line + "\n"
            i += 1 
        return service_text
            
    # Processed service text 
    def extract_services(self, text):
        try:
            service_text = self.process_service_text(text)
            services = []

            lines = service_text.split('\n')
            for line in lines:
                if line.strip():  # Ensure the line is not empty
                    parts = line.split()
                    try:
                        date = parts[0]
                        
                        # Handle POS null value
                        if parts[1].isdigit() and len(parts[1]) == 2:
                            pos = parts[1]
                            service_code_start_index = 2
                        else:
                            pos = None
                            service_code_start_index = 1

                        # Extract Service Code and Modifiers
                        service_code = parts[service_code_start_index]
                        modifiers = None
                        if '-' in service_code:
                            service_code, modifiers = service_code.split('-')
                        elif '.' in service_code:
                            service_code, modifiers = service_code.split('.')
                        
                        # Extract DX values
                        dx = []
                        dx_found = False
                        for i in range(service_code_start_index + 1, len(parts)):
                            if any(c.isalpha() for c in parts[i]):
                                dx_found = True
                                break
                            dx.append(parts[i].replace(',', ''))
                        dx = ','.join(dx) if dx_found else None
                        
                        # handle empty dx and service code if wrong value comes eg: MNT - 1
                        if dx and '-' in dx:
                            dx_parts = dx.split(',')
                            dx = None
                            service_code = service_code.split('-')[0]  # Only take the first part before '-'
                            processed_service_code = []
                            for part in dx_parts:
                                if part.isdigit():
                                    modifiers = part if modifiers is None else modifiers
                                else:
                                    processed_service_code.append(part)

                        # Remove string values from units   
                        units = ''.join(filter(str.isdigit, parts[-3]))
                        fee = parts[-2].replace('$', '').replace(',', '')
                        paid = parts[-1].replace('$', '').replace(',', '')

                        service = {
                            "rawData": line,
                            "date": date,
                            "pos": pos,
                            "serviceCode": service_code[:5] or None,
                            "modifiers": modifiers or None,
                            "dx": dx or None,
                            "units": units,
                            "fee": fee,
                            "paid": paid
                        }
                        services.append(service)
                    except IndexError:
                        print("Not enough parts in line:", line)

            # If no services were extracted, check if there are any lines at all
            if not services and lines:
                print("No valid services found in the processed text.")
            return services

        except Exception as e:
            print(f'Exception encountered while extracting Services from text: {e}')
            return []
        
    # Total Fees
    def extract_total_fees(self, text):
        try:
            start = text.find("Total Fees") + len("Total Fees")
            end = text.find("Total Paid")
            total_fees = text[start:end].strip()
            return total_fees
        except Exception as e:
            print(f'Exception encountered while extracting Total Fees from text: {e}')
            return None

    # Total Paid
    def extract_total_paid(self, text):
        try:
            start = text.find("Total Paid") + len("Total Paid")
            end = text.find("Make Payments")
            total_paid = text[start:end].strip()
            
            # Check for the "Page" word and trim if necessary
            if "Page" in total_paid:
                total_paid = total_paid.split("Page")[0].strip()  
            return total_paid
        except Exception as e:
            print(f'Exception encountered while extracting Total Paid from text: {e}')
            return None

