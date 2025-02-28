import tkinter as tk
from tkinter import ttk

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

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Closable Tabs Example")

    notebook = ClosableTabNotebook(root)
    notebook.pack(expand=True, fill="both")

    # Add some tabs
    for i in range(1, 4):
        tab = ttk.Frame(notebook)
        label = tk.Label(tab, text=f"Content of Tab {i}")
        label.pack(padx=20, pady=20)
        notebook.add(tab, text=f"Tab {i}")

    root.mainloop()