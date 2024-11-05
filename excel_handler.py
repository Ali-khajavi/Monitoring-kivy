import openpyxl
import os

class ExcelHandler:
    def __init__(self, file_name):
        self.file_name = file_name

        if os.path.exists(self.file_name):
            self.load_excel_file()
        else:
            print(f"Excel file '{self.file_name}' does not exist.")

    def load_excel_file(self):
        """Loads the existing Excel file."""
        try:
            self.workbook = openpyxl.load_workbook(self.file_name)
            self.sheet = self.workbook.active
            print(f"Excel file '{self.file_name}' loaded.")
        except Exception as e:
            print(f"Error loading Excel file: {e}")

#----------------------------------Customers Operations---------------------#
    def load_customers(self):
        """Load customer data from Excel."""
        wb = openpyxl.load_workbook(self.file_name)
        ws = wb['Customers']
        customers = []
        # take 
        for row in ws.iter_rows(min_row=2, values_only=True):
            first_name, last_name, email, phone, city, description, address, sensors_code, sensors_type, sensors_description = row

            customers.append({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "city": city,
                "description": description,
                "address": address,
                "sensors_code": sensors_code,
                "sensors_type": sensors_type,
                "sensor_description": sensors_description
            })
        return customers

    def save_customers(self, customers):
        """Save customer data to Excel, appending new customers to existing data."""
        if not os.path.exists(self.file_name):
            # If the file doesn't exist, create it with the headers
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Customers"
            ws.append(["First Name", "Last Name", "Email", "Phone", "City", "Description", "Address", "Sensors Code", "Sensors Type", "Sensor Description"])  # Header
            wb.save(self.file_name)
            wb.close()
        
        # Load existing customers from the Excel file
        existing_customers = self.load_customers()
        
        # Append new customers to the existing list
        existing_customers.extend(customers)

        # Write back all customers to the Excel file
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Customers"
        # Header
        ws.append(["First Name", 
                   "Last Name", 
                   "Email", 
                   "Phone", 
                   "City", 
                   "Description",         
                   "Address", 
                   "Sensors Code",
                   "Sensors Type", 
                   "Sensor Description"]) 

        for customer in existing_customers:
            ws.append([customer['first_name'], 
                        customer['last_name'], 
                        customer['email'], 
                        customer['phone'], 
                        customer['city'], 
                        customer['description'], 
                        customer['address'],
                        ])
            
        wb.save(self.file_name)
        wb.close()

    def delete_customer(self, customer):
        print(customer)
        pass


#-----------------------------------Sensors Operations---------------------#
    def save_sensor(self, customer, sensor_code, type, description):
        wb = openpyxl.load_workbook(self.file_name)
        ws = wb['Customers']
        customer_row = self.return_customers_row(customer)
        current_sensor_codes = ws[f"H{customer_row}"].value 
        current_sensor_types = ws[f"I{customer_row}"].value 
        current_sensor_descriptions = ws[f"J{customer_row}"].value
        # Write the new Value of Sensor Code and Sensor Type and Sensor Description
        if current_sensor_codes is not None:
            ws[f"H{customer_row}"] = f"{current_sensor_codes};{sensor_code}"
        else:
            ws[f"H{customer_row}"] = sensor_code 

        if current_sensor_types is not None:
            ws[f"I{customer_row}"] = f"{current_sensor_types};{type}"
        else:
            ws[f"I{customer_row}"] = type 

        if current_sensor_descriptions is not None:
            ws[f"J{customer_row}"] = f"{current_sensor_descriptions};{description}"
        else:
            ws[f"J{customer_row}"] = description 
               
        wb.save(self.file_name)
        wb.close()

    def load_sensors(self, customer):
        self.return_customers_row(customer)

    
    def return_customers_row(self, customer):
        wb = openpyxl.load_workbook("customers_data.xlsx")
        ws = wb["Customers"]

        last_name, first_name = customer.split(";")
        customer_row = None
        
        for index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):  # Start index from 2
            if row[0] == first_name and row[1] == last_name:  # Check columns 1 and 2
                customer_row = index  # Get the row number
                print(f"Customer {first_name} {last_name} found in row {customer_row}.")
                break
        if customer_row is None:
            print(f"Customer with the name {first_name} {last_name} is not registered in the list!")    
            return
        else:
            return customer_row

        