import tkinter as tk
import tkinter.ttk as ttk

class ClosableTabNotebook(ttk.Notebook):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-3>", self.show_context_menu)  # Bind right-click event

    def show_context_menu(self, event):
        """Display the context menu on right-click."""
        tab_index = self.index(f"@{event.x},{event.y}")
        if tab_index != -1:  # Check if a tab was clicked
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Close Tab", command=lambda: self.close_tab(tab_index))
            menu.post(event.x_root, event.y_root)

    def close_tab(self, tab_index):
        """Close the tab at the specified index."""
        self.forget(tab_index)
    
        