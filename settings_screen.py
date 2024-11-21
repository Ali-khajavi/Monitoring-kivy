from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import secrets_server
from kivy.properties import StringProperty
import os, sys

def resource_path(relative_path):
        """Get absolute path to resource, works for dev and PyInstaller"""
        try:
            # PyInstaller temporary folder
            base_path = sys._MEIPASS
        except AttributeError:
            # Development environment
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

class SettingsScreen(Screen):
    background_image = StringProperty(resource_path('assets/back0.jpg'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change_server_settings(self, server_address, token, organization, bucket):
        from main import MyScreenManager
        secrets_server.save_settings(token, organization, bucket, server_address)
        secrets_server.print_settings() # Debugg

        secrets_server.BUCKET = bucket
        secrets_server.INFLUXDB_TOKEN = token
        secrets_server.ORGANIZATION = organization
        secrets_server.SERVER_ADDRESS = server_address
        secrets_server.save_settings(token, organization, bucket, server_address)

        secrets_server.print_settings() # Debugg

        MyScreenManager.show_popup(
            title='Server Setting',
            message1=f"Server Settings Successfully changed to...\n"
                    f"Account IP: {server_address}\n"
                    f"Account Email: {organization}\n"
                    f"API Token: {token}\n"
                    f"Account Username: {bucket}\n"
                    f"Please restart the Software!",
                    message2="If still has no account now it is possible to register from the link below:"
        )

    def reset_settings(self):
        # Reset to default settings
        from main import MyScreenManager
        secrets_server.reset_to_defaults()
        MyScreenManager.show_popup(
            title='Settings', 
            message1=f"Server setting turned to base test softwar."
                    f"\n please restart the Monitoring software!"
        )