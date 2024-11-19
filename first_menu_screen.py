from kivy.uix.screenmanager import Screen
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

class FirstMenuScreen(Screen):
    background_image = StringProperty(resource_path('assets/Backgroundimage.png'))
    button_b3 = StringProperty(resource_path('assets/PNG/Button_1/b3.png'))
    button_b4 = StringProperty(resource_path('assets/PNG/Button_1/b4.png'))
    button_b1 = StringProperty(resource_path('assets/PNG/Button_1/b1.png'))
    button_b2 = StringProperty(resource_path('assets/PNG/Button_1/b2.png'))

    pass
