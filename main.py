from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from excel_handler import ExcelHandler
from screens import FirstMenuScreen, SettingsScreen, MonitoringScreen, CustomerSetupScreen

# Load the kv file
Builder.load_file('kv/main.kv')

class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        # Initialize ExcelHandler (creates new file if it doesn't exist)
        self.excel_handler = ExcelHandler('customer_data.xlsx')

        # Set up the screen manager
        sm = MyScreenManager()

        # Add screens first
        sm.add_widget(FirstMenuScreen(name='first_menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(MonitoringScreen(name='monitoring'))
        sm.add_widget(CustomerSetupScreen(name='customer_setup'))

        # Now you can access the customer_setup screen and load customers
        sm.get_screen('customer_setup').load_customers()  # No need to pass excel_handler here



        return sm

if __name__ == '__main__':
    MyApp().run()
