# File Explorer Tab
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os


class FileExplorerTab(tk.Frame):
    def __init__(self, parent, tab_control):
        super().__init__(parent)
        self.tab_control = tab_control

        self.filenames = []
        self.after_id = None
        self.selected_indices = []
        self.filename_map = {}
        self.selected_filenames = set()  # Use a set for efficient checking
        self.filtering = False

        self.selected_files_variable = []  # Initialize as an empty list

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=5, pady=5)

        # Create a Canvas to hold the Listbox
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add a Scrollbar to the Canvas
        self.scrollbar_y = tk.Scrollbar(self.canvas, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the Listbox and link it to the Scrollbar
        self.file_listbox = tk.Listbox(self.canvas, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar_y.set)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)  # Pack WITHIN the Canvas

        self.scrollbar_y.config(command=self.file_listbox.yview)  # Connect scrollbar to listbox

        self.file_listbox.config(selectbackground="lightblue")


        

        self.search_var.trace_add("write", self.filter_files)
        self.file_listbox.bind("<Delete>", self.remove_files_event)


        self.context_menu = tk.Menu(self, tearoff=0)
        
        self.context_menu.add_command(label="Select All              Ctrl+A", command=self.select_all)
        self.context_menu.add_command(label="Unselect All", command=self.unselect_all)
        self.context_menu.add_command(label="Invert Selection", command=self.invert_selection)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Clear All ", command=self.clear_all_files)
        self.context_menu.add_command(label="Clear Selected    Delete", command=self.remove_files)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Open Files", command= self.select_files)

        self.file_listbox.bind("<Double-Button-1>", self.handle_double_click)
        self.file_listbox.bind("<Button-1>", self.handle_click)
        self.file_listbox.bind("<Button-3>", self.show_context_menu)
        self.file_listbox.bind("<<ListboxSelect>>", self.selection_changed)

    def filter_files(self, *args):
        search_term = self.search_var.get().lower()
        self.selected_filenames = set(self.get_checked_files_filenames())

        self.file_listbox.delete(0, tk.END)
        self.filename_map.clear()

        filtered_filenames = [] # Temporary list to hold filtered filenames

        for filename in self.filenames:
            basename = os.path.basename(filename)
            if search_term in basename.lower():
                filtered_filenames.append(filename) # Add the full path to the temporary list

        filtered_filenames.sort(key=os.path.basename) # Sort the filtered filenames A-Z

        for filename in filtered_filenames: # Now, insert the sorted filenames
            basename = os.path.basename(filename)
            self.file_listbox.insert(tk.END, basename)
            self.filename_map[basename] = filename

        self.reselect_filtered_files()

    def reselect_filtered_files(self):
        self.file_listbox.select_clear(0, tk.END)  # Clear selections

        for i in range(self.file_listbox.size()):
            displayed_filename = self.file_listbox.get(i)
            full_path = self.filename_map.get(displayed_filename)

            if full_path in self.selected_filenames:
                self.file_listbox.select_set(i)  # Select by matching filenames


    def get_checked_files_filenames(self):
        selected_indices = self.file_listbox.curselection()
        selected_filenames = []
        for i in selected_indices:
            displayed_filename = self.file_listbox.get(i)
            full_path = self.filename_map.get(displayed_filename)
            if full_path:  # Check if full_path exists
                selected_filenames.append(full_path)
        return selected_filenames

    def reselect_all_files(self):
        self.file_listbox.select_clear(0, tk.END)  # Clear existing selections

        for i in range(self.file_listbox.size()):
            displayed_filename = self.file_listbox.get(i)
            full_path = self.filename_map.get(displayed_filename)

            if full_path in self.selected_filenames:
                self.file_listbox.select_set(i)  # Restore selection based on display names


    def add_file(self, filename):
        if filename not in self.filenames:
            self.filenames.append(filename)
            self.filenames.sort(key=os.path.basename)  # Sort filenames after adding

            self.file_listbox.delete(0, tk.END)  # Clear listbox
            self.filename_map.clear()  # Clear filename map

            for fn in self.filenames:  # Re-populate listbox in sorted order
                basename = os.path.basename(fn)
                self.file_listbox.insert(tk.END, basename)
                self.filename_map[basename] = fn

            self.reselect_filtered_files()  # Maintain selection after adding files
        else:
            print(f"File '{filename}' already in the list.")  # Inform user if file exists




    def get_checked_files(self):
        """Get the full paths of selected files after filtering."""
        selected_indices = self.file_listbox.curselection()
        selected_filenames = []
        
        for i in selected_indices:
            displayed_filename = self.file_listbox.get(i)
            full_path = self.filename_map.get(displayed_filename)
            if full_path:
                selected_filenames.append(full_path)

        return selected_filenames
    
    def show_context_menu(self, event):
        """Show the context menu on right-click."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)  # Popup at mouse position
        finally:
            self.context_menu.grab_release() # Release grab so other events can be processed

    def select_all(self, event=None):
        self.file_listbox.select_set(0, tk.END)
        self.selected_filenames = set(self.get_checked_files_filenames())  # Update IMMEDIATELY
        self.selected_files_variable = list(self.selected_filenames) # Update Variable
        self._get_checked_files()  # Call the function to print the selected files
        self.update_selection_color()  # Update the selection color
        print("Select All Called")

    def unselect_all(self):
        self.file_listbox.select_clear(0, tk.END)
        self.selected_filenames = set()  # Update IMMEDIATELY
        self.selected_files_variable = []  # Update Variable
        self._get_checked_files()  # Call the function to print the selected files
        self.update_selection_color()  # Update the selection color
        print("Unselect All Called")

    def invert_selection(self):
        selected_indices = self.file_listbox.curselection()
        self.file_listbox.select_clear(0, tk.END)

        for i in range(self.file_listbox.size()):
            if i not in selected_indices:
                self.file_listbox.select_set(i)

        self.selected_filenames = set(self.get_checked_files_filenames())  # Update IMMEDIATELY
        self.selected_files_variable = list(self.selected_filenames)  # Update Variable
        self._get_checked_files()  # Call the function to print the selected files
        self.update_selection_color()  # Update the selection color
        print("Invert Selection Called")

    def remove_files_event(self, event):
        """Handle remove_files when Delete key is pressed."""
        self.remove_files()  # Call the existing remove_files function


    def remove_files(self):
        """Remove selected files from the listbox and filenames list."""
        selected_indices = sorted(self.file_listbox.curselection(), reverse=True)

        if selected_indices:
            filenames_to_remove = []  # Store filenames to remove *before* modifying lists
            for index in selected_indices:
                filenames_to_remove.append(self.filenames[index])

            for filename_to_remove in filenames_to_remove: #Iterate through the copy of the list
                basename = os.path.basename(filename_to_remove)
                try:
                    index_to_delete = self.filenames.index(filename_to_remove) #Get index based on filename
                    self.file_listbox.delete(index_to_delete)
                    del self.filenames[index_to_delete]
                    print(f"Removed: {basename}")
                except ValueError:
                    print(f"Error: Filename {basename} not found in list.") #Handle potential errors
                    continue

            self.filter_files()  # Refresh the list AFTER removing items

    def clear_all_files(self):
        """Clear all files from the listbox and the filenames list."""
        self.file_listbox.delete(0, tk.END)  # Clear the listbox
        self.filenames = []  # Clear the filenames list
        self.filename_map.clear() #Clear the filename map
        self.selected_filenames = set() #Clear the set
        self.selected_files_variable = [] #Clear the Variable
        print("All files cleared.")




    #========================================
    def selection_changed(self, event=None):
        if self.filtering:  # Ignore the event if we're filtering
            return

        self.selected_filenames = set(self.get_checked_files_filenames())
        self.get_checked_files_delayed()
    
    def get_checked_files_delayed(self):
        """Get checked files after a delay."""
        if self.after_id is not None:  # Cancel any existing delayed call
            self.after_cancel(self.after_id)

        self.after_id = self.after(2500, self._get_checked_files)  # 2500ms delay (adjust as needed)

    def _get_checked_files(self):  # The actual function to get the files
        """Internal function to get checked files (called after delay)."""
        checked_files = self.get_checked_files()
        self.after_id = None  # Reset after_id
        if checked_files:  # Check if any files are actually selected
            print("Selected files (full paths) after delay:")
            for file_path in checked_files:
                print(file_path)  # Print each file on a new line
        else:
            print("")

    def get_checked_files(self):
        """Get the full paths of selected files (no delay)."""
        selected_indices = self.file_listbox.curselection()
        selected_filenames = []
        for i in selected_indices:
            displayed_filename = self.file_listbox.get(i)
            full_path = self.filename_map.get(displayed_filename)
            if full_path:
                selected_filenames.append(full_path)
        return selected_filenames

    def handle_click(self, event):
        """Handle mouse clicks for selection (including Ctrl and Shift)."""
        if self.filtering:  # Don't handle clicks during filtering
            return

        index = self.file_listbox.nearest(event.y)  # Get the index of the clicked item

        if event.state & 0x4:  # Check if Ctrl key is pressed (state & 0x4)
            if index in self.file_listbox.curselection():
                self.file_listbox.select_clear(index)  # Toggle selection
            else:
                self.file_listbox.select_set(index)  # Add to selection
            self.last_clicked = index

        elif event.state & 0x1:  # Check if Shift key is pressed (state & 0x1)
            if self.last_clicked is not None:  # Check if we have a previous click
                start = min(self.last_clicked, index)
                end = max(self.last_clicked, index)
                self.file_listbox.select_clear(0, tk.END)  # Clear previous selections
                self.file_listbox.select_set(start, end)  # Select range
            self.last_clicked = index  # Update last_clicked even with Shift

        else:  # Normal click (no Ctrl or Shift)
            if index in self.file_listbox.curselection() and len(self.file_listbox.curselection()) == 1:
                # If the item is already selected and only one item is selected, clear the selection
                self.file_listbox.select_clear(index)
                self.last_clicked = None
            else:
                # If the item is not selected or multiple items are selected, clear all selections and select the clicked item
                self.file_listbox.select_clear(0, tk.END)
                self.file_listbox.select_set(index)
                self.last_clicked = index

            # Print filename of the clicked file
            # displayed_filename = self.file_listbox.get(index)
            # full_path = self.filename_map.get(displayed_filename)
            # if full_path:
            #     self.after(2500, lambda: print(f"Clicked file: {full_path}"))  # Print the full path after delay

        # Force the Listbox to update its display
        self.file_listbox.update_idletasks()

        # Update the set and variable with the current selection
        self.selected_filenames = set(self.get_checked_files_filenames())
        self.selected_files_variable = list(self.selected_filenames)
        self.get_checked_files_delayed()  # Call the function to print the selected files after delay

        # Update the background color of selected items
        self.update_selection_color()


    def handle_double_click(self, event):
        if self.filtering:  # Don't handle clicks during filtering
            return

        index = self.file_listbox.nearest(event.y)  # Get the index of the clicked item
        if index in self.file_listbox.curselection() and len(self.file_listbox.curselection()) == 1:
            # If the item is already selected and only one item is selected, clear the selection
            self.file_listbox.select_clear(index)
            self.last_clicked = None
        else:
            # If the item is not selected or multiple items are selected, clear all selections and select the clicked item
            self.file_listbox.select_clear(0, tk.END)
            self.file_listbox.select_set(index)
            self.last_clicked = index

        # Print filename of the clicked file
        displayed_filename = self.file_listbox.get(index)
        full_path = self.filename_map.get(displayed_filename)
        # if full_path:
        #     self.after(2500, lambda: print(f"Clicked file: {full_path}"))  # Print the full path after delay


    def update_selection_color(self):
        """Update the background color of selected items."""
        for i in range(self.file_listbox.size()):
            if i in self.file_listbox.curselection():
                self.file_listbox.itemconfig(i, {'bg': 'lightblue'})
            else:
                self.file_listbox.itemconfig(i, {'bg': 'white'})








#=====================================================
    def select_files(self):
        filenames = MainApplication.open_files(self)
        if filenames:
            for filename in filenames:
                self.add_file(filename)




class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Explorer Example")
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.paned_window = ttk.Panedwindow(self.frame, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.paned_window)
        self.paned_window.add(self.notebook, weight=1)

        # Create a FileExplorerTab instance
        self.file_explorer_tab = FileExplorerTab(self.notebook, self.notebook)
        self.notebook.add(self.file_explorer_tab, text="File Explorer")

        self.button_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.button_frame, weight=0)

        self.select_button = tk.Button(self.button_frame, text="Select", command=self.on_select)
        self.select_button.pack(pady=10)

        self.open_files_button = tk.Button(self.frame, text="Open Files", command=self.open_files)
        self.open_files_button.pack(pady=5)

    # def open_files(self):
    #     """Open files and add them to the file explorer tab."""
    #     filenames = filedialog.askopenfilenames(title="Open Files")
    #     return filenames
    #     # if filenames:
    #     #     for filename in filenames:
    #     #         self.file_explorer_tab.add_file(filename)

    def open_files(self):
        """Open files and add them to the file explorer tab."""
        filenames = filedialog.askopenfilenames(title="Open Files")
        if filenames:
            for filename in filenames:
                self.file_explorer_tab.add_file(filename)

    def on_select(self):
        """Handle the selection of files."""
        checked_files = self.file_explorer_tab.get_checked_files()
        print("Selected files (full paths):", checked_files)
        # Process the selected files here

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

