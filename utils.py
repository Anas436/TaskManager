# Source - https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file

import os
import sys

# Call 'resource_path' function everywhere in the code during use the 'icons' & 'assests' folder.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

