import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

kivy.require('2.3.1')
from screens.input.input_screen import InputScreen
from screens.ship.ship_screen import ShipScreen

class MainApp(App):
    def build(self):
        Builder.load_file("main.kv")
        Builder.load_file("screens/input/input_screen.kv")
        Builder.load_file("screens/ship/ship_screen.kv")

        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input_screen'))
        sm.add_widget(ShipScreen(name='ship_screen'))

        return sm
    def on_start(self):
        Window.maximize()

def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()