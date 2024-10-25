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

    def on_enter(self):
        """Load customer data from Excel when the screen is opened."""
        self.load_customers()

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
            self.customers.clear()
            self.customers.append(new_customer)
            self.update_customer_list()
            self.save_customers()
            self.clear_form()
            self.load_customers()

    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()  # Remove all children from the customer list

        # Sort customers by last name and print them to verify sorting
        sorted_customers = sorted(self.customers, key=lambda customer: customer['last_name'].lower())
        print("Sorted customers:", sorted_customers)  # Debugging line

        for customer in sorted_customers:
            customer_label = Label(text=f"{customer['first_name']} {customer['last_name']}", size_hint_y=None, height=40)

            # Adjust lambda function to capture customer correctly
            customer_label.bind(on_touch_down=lambda instance, touch, cust=customer: self.on_customer_label_touch(instance, touch, cust))
            
            self.customer_list.add_widget(customer_label)



    def on_customer_label_touch(self, instance, touch, customer):
        """Handle touch event on a customer label."""
        if instance.collide_point(*touch.pos):
            self.show_customer_info(customer)

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
