from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from excel_handler import ExcelHandler  # Ensure correct import based on your tree


class MonitoringScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.excel_handler = ExcelHandler("customers_data.xlsx")  # Initialize ExcelHandler
        self.load_customers()

    def load_customers(self):
        """Load customers from the Excel file and populate the list."""
        customers = self.excel_handler.load_customers()
        customer_list = self.ids.customer_list  # Get the ScrollView's child container
        customer_list.clear_widgets()  # Clear existing items

