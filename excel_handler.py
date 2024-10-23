import openpyxl

class ExcelHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def save_customers(self, customers):
        """Save customer data to Excel."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Customers"
        ws.append(["First Name", "Last Name", "Email", "Phone", "City", "Description", "Address", "Sensors (Code, Description)"])  # Header

        for customer in customers:
            sensors = "; ".join([f"{s['code']} - {s['description']}" for s in customer['sensors']])
            ws.append([customer['first_name'], customer['last_name'], customer['email'], customer['phone'], customer['city'], customer['description'], customer['address'], sensors])
        
        wb.save(self.filepath)
        wb.close()

    def load_customers(self):
        """Load customer data from Excel."""
        wb = openpyxl.load_workbook(self.filepath)
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
