from kivy.clock import Clock
from kivy.app import App

def safe_raise(exception):
    """
    Safely triggers your app's error handler without crashing
    regardless of Kivy thread or lifecycle.
    """
    def do_error(dt):
        app = App.get_running_app()
        if not app:
            raise exception  # fallback
        app.show_error(exception)

    Clock.schedule_once(do_error, 0)