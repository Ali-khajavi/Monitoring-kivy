from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
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
    from kivy.uix.widget import Widget  # Make sure Widget is imported
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.popup import Popup

    def show_popup(title, message, message2='None'):
        # Create the content of the popup
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[10, 50, 10, 10])  # Adjust padding
        font_size = 16  # You can adjust this value or calculate it dynamically

        # Create the first message label with wrapping enabled
        message_label = Label(
            text=message,
            halign="left",
            size_hint_y=None,
            font_size=font_size,
            width=200,  # Set a fixed width for the label to allow wrapping
            text_size=(200, None),  # Allow text to wrap based on the width
            height=30  # Set a minimum height for the label
        )
        message_label.bind(size=message_label.setter('text_size'))  # Adjust text wrapping
        message_label.height = message_label.texture_size[1]  # Adjust the height of the label based on the content

        # Optionally create the second message label
        message_label2 = None
        if message2 != 'None':
            message_label2 = Label(
                text=message2,
                halign="left",
                size_hint_y=None,
                font_size=font_size,
                height=30  # Set a minimum height for the second label
            )
            message_label2.bind(size=message_label2.setter('text_size'))
            message_label2.height = message_label2.texture_size[1]  # Adjust the height of message2

        # Create a close button
        close_button = Button(text="Close", size_hint_y=None, height=40)

        # Create the popup
        popup = Popup(
            title=title,
            content=layout,
            size_hint=(0.6, 0.4),  # Adjust popup size
            auto_dismiss=False
        )

        # Add widgets to the layout in the correct order
        layout.add_widget(message_label)  # Add the first message
        if message_label2:
            layout.add_widget(message_label2)  # Add the second message if it exists
        layout.add_widget(close_button)  # Add the close button

        # Close the popup when the button is pressed
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