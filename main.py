from kivy.config import Config

# Set the desired window size before importing other Kivy modules
Config.set('graphics', 'width', '1200')  # Set the width to 1200
Config.set('graphics', 'height', '700')  # Set the height to 700

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from utils.excel_handler import ExcelHandler
from screens import FirstMenuScreen, SettingsScreen, MonitoringScreen, CustomerSetupScreen
from kivy.core.window import Window

# Load the kv files
Builder.load_file('kv/first_menu.kv')
Builder.load_file('kv/settings.kv')
Builder.load_file('kv/monitoring.kv')
Builder.load_file('kv/customer_setup.kv')


class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        # Initialize ExcelHandler (creates new file if it doesn't exist)
        self.excel_handler = ExcelHandler('customers.xlsx')  # Ensure the file name matches
        
        # Window.fullscreen = True  # Ensure this line is commented out or removed

        # Set up the screen manager
        sm = MyScreenManager()
        sm.add_widget(FirstMenuScreen(name='first_menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        # Initialize MonitoringScreen with the excel_handler instance
        monitoring_screen = MonitoringScreen(name='monitoring')
        monitoring_screen.excel_handler = self.excel_handler  # Pass the excel handler to the screen
        sm.add_widget(monitoring_screen)

        sm.add_widget(CustomerSetupScreen(name='customer_setup'))

        return sm

if __name__ == '__main__':
    MyApp().run()
