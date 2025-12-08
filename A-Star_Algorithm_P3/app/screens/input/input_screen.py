from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
import sys, os
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

class InputScreen(Screen):
    repoPath = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.repoPath = find_folder("test_manifests")
        except FileNotFoundError:
            # Default to system root directory
            self.repoPath = os.path.abspath(os.sep)

    def selected(self, filename):
        print("Selected file: ", filename)

class InputLayout(Widget):
    filepath = ObjectProperty(None)

def find_folder(target_folder="p3_tests"):
    import sys, os
    
    # Resolve starting directory
    if getattr(sys, "frozen", False):
        path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        path = os.path.dirname(os.path.abspath(__file__))

    # Climb upward until folder is found
    while True:
        candidate = os.path.join(path, target_folder)

        if os.path.isdir(candidate):
            return candidate 

        parent = os.path.dirname(path)
        if parent == path:
            raise FileNotFoundError(
                f"Could not find '{target_folder}' starting from {path}"
            )

        path = parent
