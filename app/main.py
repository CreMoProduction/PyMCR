import sys
import os

# Add the parent directory to the sys.path (app)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from app import ( # Import the package-level variables including __version__
    __version__,
    __author__
    ) 
from app.config.config import (
    version,
    author,
    date,
    APP_TITLE, 
    APP_GEOMETRY)
from app.gui.main_window import MainWindow
from app.config.config import (
    APP_TITLE, 
    APP_GEOMETRY
    )


def main():
    root = tk.Tk()
    root.title(f"{APP_TITLE} v{version}")
    root.geometry(APP_GEOMETRY)

    main_window = MainWindow(root)  # Use a different variable name
    root.mainloop()                 # Start the Tkinter event loop

if __name__ == "__main__":
    main()


