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

    def save_customers(self, customers):
        """Save customer data to Excel, appending new customers to existing data."""
        if not os.path.exists(self.file_name):
            # If the file doesn't exist, create it with the headers
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Customers"
            ws.append(["First Name", "Last Name", "Email", "Phone", "City", "Description", "Address", "Sensors (Code, Description)"])  # Header
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
        ws.append(["First Name", "Last Name", "Email", "Phone", "City", "Description", "Address", "Sensors (Code, Description)"])  # Header

        for customer in existing_customers:
            sensors = "; ".join([f"{s['code']} - {s['description']}" for s in customer['sensors']])
            ws.append([customer['first_name'], customer['last_name'], customer['email'], customer['phone'], customer['city'], customer['description'], customer['address'], sensors])
        
        wb.save(self.file_name)
        wb.close()

    def load_customers(self):
        """Load customer data from Excel."""
        wb = openpyxl.load_workbook(self.file_name)
        ws = wb['Customers']
        customers = []

        for row in ws.iter_rows(min_row=2, values_only=True):
            first_name, last_name, email, phone, city, description, address, sensors_data = row
            sensors = []
            if sensors_data:
                for sensor_info in sensors_data.split("; "):
                    code, desc = sensor_info.split(" - ")
                    sensors.append({"code": code, "description": desc})
            customers.append({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "city": city,
                "description": description,
                "address": address,
                "sensors": sensors
            })

        return customers
