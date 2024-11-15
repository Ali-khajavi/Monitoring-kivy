from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from excel_handler import ExcelHandler
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.image import Image

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
    floatlayout = ObjectProperty(None)
    #Customer Sensors Menu
    sensor_chart = ObjectProperty(None)
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
        self.create_back_delete_btn()



#------------------------------------------Customer Operations-----------------------------#
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
                "sensor_code": '',
                "sensor_type": '',
                "sensor_description": ''
            }
            #self.customers.clear()
            self.customers.append(new_customer)
            self.update_customer_list()
            self.save_customer_to_excel(new_customer)
            self.clear_form()
            self.load_customers()

    def delete_a_customer(self, instance):
        if self.selected_customer is None:
            print("No Customer Selected for the Operation!")
            return
        else:
            App.get_running_app().excel_handler.delete_customer(self.selected_customer)
            self.load_customers()

    def update_customer_list(self):
        """Refresh the customer list display."""
        self.customer_list.clear_widgets()
        self.selected_customer = None
        # Sort customers by last name
        if self.customers is not None:
            sorted_customers = sorted(self.customers, key=lambda customer: customer['last_name'].lower())
            for customer in sorted_customers:
                # Create a layout to hold the toggle button and label
                layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=40,  # Fixed height for the row
                    padding=(10, 0, 9 + self.width * .07 , 0)
                )
                # Create a label for the customer's name
                customer_label = Label(
                    text=f"{customer['last_name']} , {customer['first_name']}",
                    color=(0, 0, 0),
                    size_hint_y=None,
                    height=40,  # Fixed height for the label
                    halign="left",
                    font_size=16,
                    text_size=(self.width * 0.7, None) # Dynamic text size based on screen width
                )
                
                customer_label.bind(on_touch_down=lambda instance, touch, cust=customer: self.on_customer_label_touch(instance, touch, cust))
        
                # Create a ToggleButton for selection
                toggle_button = ToggleButton(
                    group='customer_selection',
                    size_hint_y=self.height * 0.001,  # Make the button height fill the BoxLayout and width adjustable
                    size_hint_x=self.width * 0.00007,  # Set the width relative to the screen width
                    on_press=lambda instance, cust=customer: self.on_customer_selected(cust)  # Pass 'customer' explicitly
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
        self.create_back_delete_btn()
        self.update_customer_sensors()

    def on_customer_label_touch(self, instance, touch, customer):
        """Handle touch event on a customer label."""
        if instance.collide_point(*touch.pos):
            self.show_customer_info(customer)

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
        popup = Popup(title="Customer Information",title_size=28, content=Label(text=info), size_hint=(0.6, 0.6))

        popup.open()



#------------------------------------------Sensors Operations------------------------------#
    def save_sensor(self):
        sensor_code = self.sensor_code_input.text
        sensor_description = self.sensor_description_input.text
        print(f"Selected Customer: {self.selected_customer}")
        if len(sensor_code) >= 3 and self.selected_customer != None:
            self.clear_form()
            App.get_running_app().excel_handler.save_sensor(self.selected_customer, sensor_code, self.sensor_type, sensor_description)
        self.load_customers()
        self.update_customer_sensors()

    def sensors_type(self, instance, value, sensor):
        self.sensor_type = sensor
        return self.sensor_type
    
    def update_customer_sensors(self):
        self.sensor_chart.clear_widgets()
        if self.selected_customer is not None:
            sensors_type, sensors_code, sensors_description  = App.get_running_app().excel_handler.load_sensors(self.selected_customer)
            #sensors_type = sensors_type.split(';')
            #sensors_code = sensors_code.split(';')
            #sensors_description = sensors_description.spli(';')
            print(f"print from update customer sensor : {sensors_description}")
        else:
            return
        if sensors_type is not None:
            # Set dynamic button size hints
            button_width_hint = 0.22 
            button_height_hint = 0.15  
            layout = GridLayout(
                cols=4,
                size_hint_y=None,
                spacing=10,
                row_default_height = Window.height * button_height_hint *.6, # Use screen height to set row height
                col_default_width = Window.width * button_width_hint * .2
            )
            layout.bind(minimum_height=layout.setter('height'))

            buttons = []
            buttons.clear()

            for i , sensor in enumerate(sensors_type):
                image_path = self.sensor_image_address(str(sensor))
                button = Button(
                    size_hint=(button_width_hint, button_height_hint),
                    background_normal=image_path,
                )
                # Store the current sensor type, code, and description in local variables
                current_sensor_type = str(sensor)
                current_sensor_code = str(sensors_code[i])
                current_sensor_description = str(sensors_description[i])

                button.bind(on_release=lambda btn, s_type=current_sensor_type, s_code=current_sensor_code, s_desc=current_sensor_description: self.open_sensor_popup_edite(s_type, s_code, s_desc, self.selected_customer))
                buttons.append(button)

            for button in reversed(buttons):
                layout.add_widget(button)

            self.sensor_chart.add_widget(layout)

        Window.bind(on_resize=self.on_window_resize)

    def sensor_image_address(self, sensor):
        add = {'voltmeter': 'assets/sensor1.png',
               'flowmeter': 'assets/sensor2.png',
               'temperature': 'assets/sensor3.png',
               'ampermeter': 'assets/sensor4.png',
               }
        return add[sensor]
    
    def open_sensor_popup_edite(self, sensors_type, sensors_code, sensors_description, customer):
        # Create a popup window layout
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        sensor_layout = BoxLayout(orientation='horizontal', padding=10)

        image_path = self.sensor_image_address(sensors_type)
        sensor_image = Image(source=image_path, size_hint=(1, 1))
        labels_layout = BoxLayout(orientation='vertical', padding=10)
        code_label = Label(
        text="Sensor Uniqe Code:",
        size_hint=(1, 0.3),
        halign="left", 
        valign="top"    
        )
        description_label = Label(
        text="Description:",
        size_hint=(1, 1),
        halign="left", 
        valign="top"    
        )
        labels_layout.add_widget(code_label)
        labels_layout.add_widget(description_label)

        inputs_layut = BoxLayout(orientation='vertical',  padding=10)
    
        Code_input = TextInput(text=sensors_code, multiline=False, size_hint=(1, 0.3))
        description_input = TextInput(text=sensors_description, multiline=False, size_hint=(1, 1))
        inputs_layut.add_widget(Code_input)
        inputs_layut.add_widget(description_input)

        sensor_layout.add_widget(sensor_image)
        sensor_layout.add_widget(labels_layout)
        sensor_layout.add_widget(inputs_layut)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        save_button = Button(text="Save", size_hint=(0.5, 1))
        save_button.bind(
            on_release=lambda x: (
                App.get_running_app().excel_handler.save_sensor_edit(customer, sensors_code, Code_input.text, description_input.text),
                self.load_customers(),
                self.update_customer_sensors(),
                self.current_popup.dismiss()
            )
        )

        remove_button = Button(text="Remove", size_hint=(0.5, 1)) 
        remove_button.bind(
            on_release=lambda x: (
                App.get_running_app().excel_handler.delete_sensor(customer, sensors_code),
                self.load_customers(),
                self.update_customer_sensors(),
                self.current_popup.dismiss()
            )
        )

        button_layout.add_widget(save_button)
        button_layout.add_widget(remove_button)
        popup_layout.add_widget(sensor_layout)
        popup_layout.add_widget(button_layout)

        # Create and open the popup
        popup = Popup(title=f"Edit Sensor : {sensors_type}", content=popup_layout, size_hint=(0.6, 0.6))
        popup.open()

        # Add a reference to close the popup after actions
        self.current_popup = popup


#------------------------------------------Excel Operations---------------------------------#
    def save_customer_to_excel(self, new_customer):
        """Save customer data to Excel."""
        App.get_running_app().excel_handler.save_customers(new_customer)

    def load_customers(self):
        """Load customer data from Excel and update the customer list."""
        self.customers = App.get_running_app().excel_handler.load_customers()
        #print("Loaded customers:", self.customers)
        self.update_customer_list()



#------------------------------------------Tools Functions----------------------------------#
    def on_window_resize(self, *args):
        self.update_customer_sensors()  # Re-run the function to adjust button size

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

    def update_font_size(self, instance, value):
        """Update the font size dynamically based on the width of the button"""
        instance.font_size = instance.width / 12

    def create_back_delete_btn(self):
        self.floatlayout.clear_widgets()
        self.back_button = Button(
            text="Back to Main Menu",
            background_normal='assets/PNG/Button_1/b2.png',
            background_down='assets/PNG/Button_1/b4.png',
            size_hint=(0.6, 0.25),
            pos_hint={'top': 0.47},  
            on_release= self.back_to_main_menu
        )
        self.back_button.bind(size=self.update_font_size)
        self.floatlayout.add_widget(self.back_button)
        if self.selected_customer is not None:
            self.delete_custome_btn = Button(
                text = "Delete Customer",
                background_normal='assets/PNG/Button_1/b1.png',
                background_down='assets/PNG/Button_1/b4.png',
                size_hint=(0.6, 0.25),
                pos_hint = {'center_x': 0.8,'center_y': 0.85},
                on_release= self.delete_a_customer
            )
            self.delete_custome_btn.bind(size=self.update_font_size)
            self.floatlayout.add_widget(self.delete_custome_btn)

    def back_to_main_menu(self, instance):
        """Function to handle screen transition"""
        self.manager.current = 'first_menu'
