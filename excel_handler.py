import openpyxl

class ExcelHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def save_customers(self, customers):
        """Save customer data to Excel, including sensors."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Customers"
        ws.append(["Name", "Email", "Sensors (Code, Description)"])  # Header

        for customer in customers:
            sensors = "; ".join([f"{s['code']} - {s['description']}" for s in customer['sensors']])
            ws.append([customer['name'], customer['email'], sensors])
        
        wb.save(self.filepath)

    def load_customers(self):
        """Load customer data from Excel."""
        wb = openpyxl.load_workbook(self.filepath)
        ws = wb['Customers']
        customers = []

        for row in ws.iter_rows(min_row=2, values_only=True):
            name, email, sensors_data = row
            sensors = []
            if sensors_data:
                for sensor_info in sensors_data.split("; "):
                    code, description = sensor_info.split(" - ")
                    sensors.append({"code": code, "description": description})
            customers.append({"name": name, "email": email, "sensors": sensors})

        return customers
