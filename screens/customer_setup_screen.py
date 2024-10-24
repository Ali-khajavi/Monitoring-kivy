from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App

class CustomerSetupScreen(Screen):
    first_name_input = ObjectProperty(None)
    last_name_input = ObjectProperty(None)
    email_input = ObjectProperty(None)
    phone_input = ObjectProperty(None)
    city_input = ObjectProperty(None)
    address_input = ObjectProperty(None)
    description_input = ObjectProperty(None)
    customer_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customers = []  # Will hold customer data

    def register_customer(self):
        """Register a new customer."""
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text
        email = self.email_input.text
        phone = self.phone_input.text
        city = self.city_input.text
        description = self.description_input.text
        address = self.address_input.text

        if first_name and last_name and email:
            new_customer = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "city": city,
                "description": description,
                "address": address,
                "sensors": []
            }
            self.customers.append(new_customer)
            self.update_customer_list()
            self.save_customers()
            self.clear_form()

    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()   #  remove all children from a widget (Customers)
        for customer in self.customers:
            customer_widget = App.get_running_app().customer_list_item_class(customer=customer)
            #customer_widget.size_hint_y = None
            #customer_widget.height = 40
            self.customer_list.add_widget(customer_widget)
        #self.customer_list.height = self.customer_list.minimum_height

    def clear_form(self):
        """Clear the registration form."""
        self.first_name_input.text = ""
        self.last_name_input.text = ""
        self.email_input.text = ""
        self.phone_input.text = ""
        self.city_input.text = ""
        self.address_input.text = ""
        self.description_input.text = ""

    def save_customers(self):
        """Save customer data to Excel."""
        App.get_running_app().excel_handler.save_customers(self.customers)

    def load_customers(self):
        """Load customer data from Excel and update the customer list."""
        self.customers = App.get_running_app().excel_handler.load_customers()
        print("Loaded customers:", self.customers)
        self.update_customer_list()

    def on_customer_selected(self, customer):
        """Update the sensor form when a customer is selected."""
        self.ids.sensor_label.text = f"Implementing sensor for {customer['first_name']} {customer['last_name']}"
        self.selected_customer = customer
        self.ids.sensor_code_input.text = ""
        self.ids.sensor_description_input.text = ""

    def show_customer_info(self, customer):
        """Show customer information in a popup."""
        info = (
            f"Name: {customer['first_name']} {customer['last_name']}\n"
            f"Email: {customer['email']}\n"
            f"Phone: {customer['phone']}\n"
            f"City: {customer['city']}\n"
            f"Address: {customer['address']}\n"
            f"Description: {customer['description']}"
        )
        popup = Popup(title="Customer Information", content=Label(text=info), size_hint=(0.6, 0.6))
        popup.open()
