from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.resources import resource_add_path
from excel_handler import ExcelHandler
from customer_setup_screen import CustomerSetupScreen
from first_menu_screen import FirstMenuScreen
from monitoring_screen import MonitoringScreen
from settings_screen import SettingsScreen
import os, sys

def resource_path(relative_path):
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
    def show_popup(title, message1, message2=None, button_text=None, image_text=None):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Create a label with wrapped text
        label = Label(
            text=message1, 
            halign="left", 
            valign="top",
            size_hint=(1, 1),
            #text_size=(400, None)  # Adjust width for text wrapping
        )
        label.bind(size=lambda *args: label.setter('text_size')(label, (label.width, None)))

        if message2:
            label2 = Label(
                text=message2, 
                halign="left", 
                valign="bottom",
                size_hint=(1, 1),
                #text_size=(400, None)  # Adjust width for text wrapping
            )
            label2.bind(size=lambda *args: label2.setter('text_size')(label2, (label2.width, None)))


        # Add a close button
        close_button = Button(text="Close", halign='center', size_hint=(0.5, None), height=40)
        layout.add_widget(label)
        if message2:
            layout.add_widget(label2)
            popup = Popup(title=title, content=layout, size_hint=(0.8, 0.5))
        else:
            popup = Popup(title=title, content=layout, size_hint=(0.5, 0.3))

              
        layout.add_widget(close_button)
        
        # Create the popup
        
        close_button.bind(on_release=popup.dismiss)
        popup.open()
 
      
    def close_app(self, instance):
        from kivy.app import App
        App.get_running_app().stop()  # Properly stops the app
        sys.exit(0)  # Exits the program

class MyApp(App):
    def build(self):
        try:
            # Initialize ExcelHandler with the Excel file path
            excel_file_path = resource_path('customers_data.xlsx')
            self.excel_handler = ExcelHandler(excel_file_path)
        except Exception as e:
            # Handle errors in initializing the ExcelHandler
            MyScreenManager.show_popup('Loading Database', f'Error: {e}')
            return None

        # Set up the screen manager
        sm = MyScreenManager()

        # List of screens to add to the manager with their respective names
        screens = [
            (FirstMenuScreen, 'first_menu'),
            (SettingsScreen, 'settings'),
            (MonitoringScreen, 'monitoring'),
            (CustomerSetupScreen, 'customer_setup')
        ]

        # Add screens to the manager
        for ScreenClass, screen_name in screens:
            screen = ScreenClass(name=screen_name)
            if hasattr(screen, 'excel_handler'):
                screen.excel_handler = self.excel_handler
            sm.add_widget(screen)

        # Set the default screen to 'first_menu'
        sm.current = 'first_menu'
        return sm
    
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    # Add MEIPASS path for packaged resources (required for PyInstaller)
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    # Run the app
    MyApp().run()