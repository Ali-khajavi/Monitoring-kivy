from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App


class FirstMenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class MonitoringScreen(Screen):
    pass

class CustomerListItem(Button):
    """Custom button to represent a customer in the list."""
    def __init__(self, customer, **kwargs):
        super().__init__(**kwargs)
        self.customer = customer
        self.bind(on_press=self.on_click)

    def on_click(self, instance):
        """When clicked, show customer info."""
        App.get_running_app().root.get_screen('customer_setup').show_customer_info(self.customer)

class CustomerSetupScreen(Screen):
    # Reference to form inputs in .kv
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
                "sensors": []  # Empty sensors list for now
            }
            self.customers.append(new_customer)
            self.update_customer_list()
            self.save_customers()
            self.clear_form()

    def clear_form(self):
        """Clear the registration form."""
        self.first_name_input.text = ""
        self.last_name_input.text = ""
        self.email_input.text = ""
        self.phone_input.text = ""
        self.city_input.text = ""
        self.address_input.text = ""
        self.description_input.text = ""


    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()  # Clear the existing list first

        # Ensure the customer_list height adjusts to the content
        self.customer_list.height = 0

        for customer in self.customers:
            customer_str = f"{customer['first_name']} {customer['last_name']} ({customer['email']})"
            customer_widget = CustomerListItem(text=customer_str, customer=customer)
            
            # Set the size hint and height for each customer widget
            customer_widget.size_hint_y = None
            customer_widget.height = 40  # Set a fixed height (adjust as needed)
            
            self.customer_list.add_widget(customer_widget)
        
        # Adjust the customer_list height to fit all children
        self.customer_list.height = self.customer_list.minimum_height

        print(self.customers)


    def show_customer_info(self, customer):
        """Show customer information in a popup window."""
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

    def save_customers(self):
        """Save customer data to Excel."""
        App.get_running_app().excel_handler.save_customers(self.customers)

    def load_customers(self):
        """Load customer data from Excel."""
        self.customers = App.get_running_app().excel_handler.load_customers()
        self.update_customer_list()