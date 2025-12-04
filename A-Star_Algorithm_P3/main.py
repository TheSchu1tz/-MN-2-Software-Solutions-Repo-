import kivy
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
kivy.require('2.3.1')
import os, sys
from app.screens.input.input_screen import InputScreen
from app.screens.ship.ship_screen import ShipScreen
from app.screens.error.error_screen import ErrorScreen
from app.screens.log.log_screen import LogScreen
from app.utils.logger import Logger

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

class MainApp(App):
    logger:Logger

    def build(self):
        Builder.load_file(resource_path("main.kv"))
        Builder.load_file(resource_path("app/screens/input/input_screen.kv"))
        Builder.load_file(resource_path("app/screens/ship/ship_screen.kv"))
        Builder.load_file(resource_path("app/screens/error/error_screen.kv"))
        Builder.load_file(resource_path("app/screens/log/log_screen.kv"))

        self.logger = Logger()
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input_screen'))
        shipScreen = ShipScreen(name='ship_screen')
        shipScreen.SetLogger(self.logger)
        sm.add_widget(shipScreen)
        sm.add_widget(ErrorScreen(name='error_screen'))
        sm.add_widget(LogScreen(name='log_screen'))
        return sm
    
    def on_start(self):
        Window.maximize()

    def on_stop(self):
        self.logger.WriteSessionLog()

    def show_error(self, exception):
        root = self.root
        error_screen = root.get_screen("error_screen")
        error_screen.error_details = str(exception)
        root.current = "error_screen"

def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()