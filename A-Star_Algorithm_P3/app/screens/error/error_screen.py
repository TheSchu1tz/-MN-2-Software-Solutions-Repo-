from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class ErrorScreen(Screen):
    error_message = "An unexpected error occurred"
    error_details = StringProperty("")
