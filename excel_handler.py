import openpyxl
import os, sys

class ExcelHandler:
    def __init__(self, file_name):
        self.file_name = file_name

        if not os.path.exists(self.file_name):
            self.create_excel_file()
        else:
            self.load_excel_file()

    def create_excel_file(self):
        """Creates a new Excel file with necessary headers."""
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Customers"
        # Add headers for customer data
        sheet.append(["First Name", "Last Name", "Email", "Phone Number", "City", "Description"])
        workbook.save(self.file_name)
        print(f"New Excel file '{self.file_name}' created.")

    def load_excel_file(self):
        """Loads the existing Excel file."""
        self.workbook = openpyxl.load_workbook(self.file_name)
        self.sheet = self.workbook.active
        print(f"Excel file '{self.file_name}' loaded.")

    def save_customers(self, customers):
        """Save customer data to Excel."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Customers"
        ws.append(["First Name", "Last Name", "Email", "Phone", "City", "Description", "Address", "Sensors (Code, Description)"])  # Header

        for customer in customers:
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
