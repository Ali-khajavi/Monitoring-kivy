from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from excel_handler import ExcelHandler  # Ensure correct import based on your tree
from screens.customer_list_item import CustomListItem  # Import your CustomListItem here

class MonitoringScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.excel_handler = ExcelHandler("customers.xlsx")  # Initialize ExcelHandler
        self.load_customers()

    def load_customers(self):
        """Load customers from the Excel file and populate the list."""
        customers = self.excel_handler.load_customers()
        customer_list = self.ids.customer_list  # Get the ScrollView's child container
        customer_list.clear_widgets()  # Clear existing items

        # Add each customer to the ScrollView
        for customer in customers:
            full_name = f"{customer['first_name']} {customer['last_name']}"
            customer_item = CustomListItem(customer_name=full_name)  # Use your custom list item
            customer_list.add_widget(customer_item)
