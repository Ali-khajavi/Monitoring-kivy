from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class CustomerSetupScreen(Screen):
    # Reference to widgets in .kv
    name_input = ObjectProperty(None)
    email_input = ObjectProperty(None)
    sensor_code_input = ObjectProperty(None)
    sensor_desc_input = ObjectProperty(None)
    customer_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customers = []  # Will hold customer data

    def register_customer(self):
        """Register a new customer."""
        name = self.name_input.text
        email = self.email_input.text

        if name and email:
            new_customer = {"name": name, "email": email, "sensors": []}
            self.customers.append(new_customer)
            self.update_customer_list()
            self.name_input.text = ""
            self.email_input.text = ""

    def add_sensor_to_customer(self, customer_name):
        """Add a sensor to the selected customer."""
        code = self.sensor_code_input.text
        description = self.sensor_desc_input.text

        for customer in self.customers:
            if customer['name'] == customer_name:
                customer['sensors'].append({"code": code, "description": description})
                break

        self.update_customer_list()

    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()
        for customer in self.customers:
            customer_str = f"{customer['name']} ({customer['email']})"
            self.customer_list.add_widget(CustomerListItem(text=customer_str))

    def save_customers(self):
        """Save customer data to Excel."""
        App.get_running_app().excel_handler.save_customers(self.customers)

    def load_customers(self):
        """Load customer data from Excel."""
        self.customers = App.get_running_app().excel_handler.load_customers()
        self.update_customer_list()
