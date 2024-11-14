from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import DictProperty

class FirstMenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class MonitoringScreen(Screen):
    pass

class CustomerListItem(BoxLayout):
    customer = DictProperty({})

    def __init__(self, customer, **kwargs):
        super().__init__(**kwargs)

        self.customer = customer  # Store the passed customer data

        # This ensures the label text is set correctly based on customer data
        self.bind(customer=self.update_display)

        # Initialize display
        self.update_display()

        self.is_selected = False

    def update_display(self, *args):
        """Update the label text based on the customer data."""
        self.ids.customer_label.text = f"{self.customer.get('first_name', 'Unknown')} {self.customer.get('last_name', 'Unknown')}"

    def on_select(self, is_active):
        """Triggered when the checkbox is selected or deselected."""
        self.is_selected = is_active
        if is_active:
            # Update the sensor form on the right side of the screen for sensor implementation
            App.get_running_app().root.get_screen('customer_setup').on_customer_selected(self.customer)
        print(f"Displaying details for {self.customer['first_name']} {self.customer['last_name']}")

    def on_name_click(self):
        """Triggered when the customer's name is clicked, showing the popup."""
        App.get_running_app().root.get_screen('customer_setup').show_customer_info(self.customer)
        if self.is_selected:
            print(f"Selected {self.customer['first_name']} {self.customer['last_name']} for sensor setup")

class CustomerSetupScreen(Screen):
    # Reference to form inputs in .kv
    first_name_input = ObjectProperty(None)
    last_name_input = ObjectProperty(None)
    email_input = ObjectProperty(None)
    phone_input = ObjectProperty(None)
    city_input = ObjectProperty(None)
    address_input = ObjectProperty(None)
    description_input = ObjectProperty(None)
    customer_list = ObjectProperty(None)  # The layout inside ScrollView

    
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

    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()  # Clear the existing list first

        for customer in self.customers:
            customer_widget = CustomerListItem(customer=customer)  # Correctly instantiate with customer data
            
            # Set the size hint and height for each customer widget
            customer_widget.size_hint_y = None
            customer_widget.height = 40
            
            # Add the widget to the customer list
            self.customer_list.add_widget(customer_widget)

        # Ensure the list is scrollable
        self.customer_list.height = self.customer_list.minimum_height

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
        print("Loaded customers:", self.customers)  # Add this line for debugging
        self.update_customer_list()

    def on_customer_selected(self, customer):
        """Update the sensor form when a customer is selected via checkbox."""
        self.ids.sensor_label.text = f"Implementing sensor for {customer['first_name']} {customer['last_name']}"
        self.selected_customer = customer  # Save the selected customer for sensor setup

        # Clear any previous inputs for sensor setup
        self.ids.sensor_code_input.text = ""
        self.ids.sensor_description_input.text = ""

    def show_customer_info(self, customer):
        """Show customer information in a popup window when their name is clicked."""
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
