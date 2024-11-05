from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from excel_handler import ExcelHandler
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

class CustomerSetupScreen(Screen):
    #Registration Form Objects
    first_name_input = ObjectProperty(None)
    last_name_input = ObjectProperty(None)
    email_input = ObjectProperty(None)
    phone_input = ObjectProperty(None)
    city_input = ObjectProperty(None)
    address_input = ObjectProperty(None)
    description_input = ObjectProperty(None)
    #Customer List Objects
    customer_list = ObjectProperty(None)
    #Sensor side Objects
    sensor_code_input = ObjectProperty(None)
    sensor_description_input = ObjectProperty(None)
    sensor_type=''

#----------------------------------------Screen Entery Functions --------------------------#
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customers = []  # Will hold customer data
        self.excel_handler = ExcelHandler("customers_data.xlsx")  # Initialize ExcelHandler
        self.load_customers()

    def on_enter(self):
        """Load customer data from Excel when the screen is opened."""
        self.load_customers()

#----------------------------------------- Register or Delete a new Customer ------------------------#
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
            }
            self.customers.clear()
            self.customers.append(new_customer)
            self.update_customer_list()
            self.save_customer_to_excel()
            self.clear_form()
            self.load_customers()

    def delete_customer(self):
        if self.selected_customer is None:
            print("No Customer Selected for the Operation!")
            return
        else:
            App.get_running_app().excel_handler.delete_customer(self.selected_customer)

#------------------------------------------Sensors Operations------------------------------#
    def save_sensor(self):
        sensor_code = self.sensor_code_input.text
        sensor_description = self.sensor_description_input.text
        print(f"Selected Customer: {self.selected_customer}")

        if len(sensor_code) >= 3 and self.selected_customer != None:
            self.clear_form()
            App.get_running_app().excel_handler.save_sensor(self.selected_customer, sensor_code, self.sensor_type, sensor_description)

    def sensors_type(self, instance, value, sensor):
        self.sensor_type = sensor
        return self.sensor_type
    
#------------------------------------------Excel Operations---------------------------------#
    def save_customer_to_excel(self):
        """Save customer data to Excel."""
        App.get_running_app().excel_handler.save_customers(self.customers)

    def load_customers(self):
        """Load customer data from Excel and update the customer list."""
        self.customers = App.get_running_app().excel_handler.load_customers()
        #print("Loaded customers:", self.customers)
        self.update_customer_list()

#------------------------------------ Screen Tools Functions -------------------------------#
    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()
        self.selected_customer = None
        # Sort customers by last name
        if self.customers != None:
            sorted_customers = sorted(self.customers, key=lambda customer: customer['last_name'].lower())
            for customer in sorted_customers:
                # Create a layout to hold the toggle button and label
                layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=40,
                    padding=(10, 0, 60, 0)
                )
                # Create a label for the customer's name
                customer_label = Label(
                    text=f"{customer['last_name']}",
                    color=(0, 0, 0),
                    size_hint_y=None,
                    height=40,
                    halign="left",
                    font_size=16,
                )
                # Create a ToggleButton for selection
                toggle_button = ToggleButton(
                group='customer_selection',
                size_hint_x=None,
                width=40,  
                # Use a lambda function to capture the current customer and state
                on_press=lambda instance, cust=customer: self.on_customer_selected(cust)
                )
                # Add the toggle button and label to the layout
                layout.add_widget(customer_label)
                layout.add_widget(toggle_button)
                # Dynamically update padding based on the label width
                def update_padding(instance, value):
                    padding = instance.width * 0.4
                    instance.text_size = (instance.width - padding, None)

                # Bind the width change to the padding adjustment
                customer_label.bind(size=update_padding)
                self.customer_list.add_widget(layout)

    def on_customer_selected(self, customer):
        self.selected_customer = f"{customer['last_name']};{customer['first_name']}"

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
        self.sensor_code_input.text= ''
        self.sensor_description_input.text = ''

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
