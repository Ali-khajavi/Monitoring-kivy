from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from excel_handler import ExcelHandler
from customer_setup_screen import CustomerSetupScreen
from first_menu_screen import FirstMenuScreen
from monitoring_screen import MonitoringScreen 
from settings_screen import SettingsScreen

import os, sys
from kivy.resources import resource_add_path

def resource_path(relative_path):
        """Get absolute path to resource, works for dev and PyInstaller"""
        try:
            # PyInstaller temporary folder
            base_path = sys._MEIPASS
        except AttributeError:
            # Development environment
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

# Load the kv files
Builder.load_file(resource_path('kv/first_menu.kv'))
Builder.load_file(resource_path('kv/settings.kv'))
Builder.load_file(resource_path('kv/monitoring.kv'))
Builder.load_file(resource_path('kv/customer_setup.kv'))


class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        # Initialize ExcelHandler with error handling
        try:
            excel_file_path = self.resource_path('customers_data.xlsx')
            self.excel_handler = ExcelHandler(excel_file_path)
        except Exception as e:
            print(f"Error initializing ExcelHandler: {e}")
            return None

        # Set up the screen manager
        sm = MyScreenManager()
        sm.add_widget(FirstMenuScreen(name='first_menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        # Initialize MonitoringScreen with the excel_handler instance
        monitoring_screen = MonitoringScreen(name='monitoring')
        monitoring_screen.excel_handler = self.excel_handler
        sm.add_widget(monitoring_screen)

        # Initialize CustomerSetupScreen with the excel_handler if needed
        customer_setup_screen = CustomerSetupScreen(name='customer_setup')
        customer_setup_screen.excel_handler = self.excel_handler
        sm.add_widget(customer_setup_screen)

        # Optional: set default screen
        sm.current = 'first_menu'

        return sm

    @staticmethod
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and PyInstaller"""
        try:
            # PyInstaller temporary folder
            base_path = sys._MEIPASS
        except AttributeError:
            # Development environment
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    # Add MEIPASS path for packaged resources
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    MyApp().run()
