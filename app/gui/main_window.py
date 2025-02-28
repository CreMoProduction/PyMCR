# gui/gui.py
import tkinter as tk
from tkinter import Menu, PanedWindow
from app.gui.gui_callbacks import (
    clear_frames,
)
from app.gui.widgets.file_explorer import (
    FileExplorerTab,
    ButtonFrame,
)
from app.gui.widgets.tabs import (
    ClosableTabNotebook,
    )
from app.gui.widgets.file_explorer import FileExplorerTab, ButtonFrame

class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack()
        self.raw_data_overview_var = tk.BooleanVar(value=True)
        self.raw_data_tab = None
        # self.root.title("My First App")
        # self.root.geometry("400x300")
        self.create_widgets()
        self.file_explorer_tabs = []  # Store FileExplorerTab instances here
        self.file_explorer_state = None  # Store the state of the File Explorer


    def create_widgets(self): 
        self.create_menu()
        self.create_toolbar()
        self.create_panned_window()
        self.create_sidebar_tabs()
        self.create_plot_tabs()
        self.create_statusbar()

        
    def open_cdf_files(self):
        if self.file_explorer_tabs:  # Check if any tabs exist
            # Option 1: Open in the first tab (simplest if you only have one)
            # self.file_explorer_tabs[0].select_files()

            # Option 2: Let the user choose which tab to open in (more flexible)
            if len(self.file_explorer_tabs) == 1:
                selected_tab = self.file_explorer_tabs[0]
            else:
                # Create a dialog or other way to select the tab
                # For simplicity, I'll just use the first one for now. You should improve this!
                selected_tab = self.file_explorer_tabs[0]
                print("More than one tab exists, opening in the first one. Please add tab selection.")

            if selected_tab:
                selected_tab.select_files()

        else:
            print("No File Explorer Tabs exist. Please create one.")

    

    def create_menu(self):
        # Create the menu bar
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        # Create the File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open CDF", command= self.open_cdf)
        #self.file_menu.add_command(label="Open CDF", command=lambda: on_open_click(self))
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        # Create the Options menu
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(label="Settings", command=self.open_settings)
        # Create the Window menu
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Window", menu=self.options_menu)
        self.options_menu.add_command(label="File Explorer", command=lambda: self.reopen_tab(self.sidebar_tab, self.create_file_explorer, tab="File Explorer"))
        self.options_menu.add_command(label="Raw data overview", command=lambda: self.reopen_tab(self.plot_tab, self.create_raw_data_overview_tab, tab="Raw data overview"))
        self.options_menu.add_command(label="Retention Time vs. m/z", command=lambda: self.reopen_tab(self.plot_tab, self.create_raw_data_overview_tab, tab="Retention Time vs. m/z"))
        # Create the Help menu
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.options_menu)
        self.options_menu.add_command(label="Documentation", command=self.open_settings)
        self.options_menu.add_command(label="About", command=self.open_settings)
        

        

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, background="#e8e8e8", height=15)
        self.statusbar = tk.Frame(self.root, background="#e8e8e8", height=15)
        self.main = tk.PanedWindow(self.root, background="#ffffff")
        self.toolbar.pack(side="top", fill="x")
        self.statusbar.pack(side="bottom", fill="x")
        self.main.pack(side="top", fill="both", expand=True)
        # add a label to the toolbar
        self.toolbar_label = tk.Label(self.toolbar, text="toolbar", font=("Arial", 8))
        self.toolbar_label.pack(side="left", padx=1, pady=1)
        

    def create_statusbar(self):
        self.statusbar = tk.Label(self.statusbar, text="statusbar", font=("Arial", 8))
        self.statusbar.pack(side="left", padx=1, pady=1)


    def create_panned_window(self):
        # Create the PanedWindow
        self.left_paned_window = PanedWindow(self.main, orient=tk.HORIZONTAL)
        self.left_paned_window.pack(side="left", fill="both", expand=True)
        # Create the left and right frames
        self.left_frame = tk.Frame(self.left_paned_window, bg="lightgray")
        self.right_frame = tk.Frame(self.left_paned_window, bg="white")
        # Add the frames to the PanedWindow
        self.left_paned_window.add(self.left_frame, minsize=200)
        self.left_paned_window.add(self.right_frame, minsize=200)
        # Create vertical PanedWindow in the right frame
        self.right_paned_window = PanedWindow(self.right_frame, orient=tk.VERTICAL)
        self.right_paned_window.pack(fill="both", expand=True)



    def create_plot_tabs(self):
        self.plot_tab = ClosableTabNotebook(self.right_paned_window)
        self.plot_tab.pack(fill="both", expand=True)

        frame1 = tk.Frame(self.plot_tab)
        label1 = tk.Label(frame1)
        #label1.pack(padx=1, pady=1)
        self.create_raw_data_overview_tab(frame1)
        self.plot_tab.add(frame1, text="Raw data overview")

        frame1 = tk.Frame(self.plot_tab)
        label1 = tk.Label(frame1, text="Content of Retention Time vs. m/z")
        label1.pack(padx=10, pady=10)
        self.plot_tab.add(frame1, text="Retention Time vs. m/z")
        
    def create_sidebar_tabs(self):
        self.sidebar_tab = ClosableTabNotebook(self.left_frame)  # Place it in left_frame directly
        self.sidebar_tab.pack(fill="both", expand=True)
        
        frame1 = tk.Frame(self.sidebar_tab)
        self.create_file_explorer(frame1)
        # Add the combined_frame to the sidebar_tab
        self.sidebar_tab.add(frame1, text="File Explorer")

        frame1 = tk.Frame(self.sidebar_tab)
        label1 = tk.Label(frame1, text="Content of Retention Time vs. m/z")
        label1.pack(padx=10, pady=10)
        self.sidebar_tab.add(frame1, text="Retention Time vs. m/z")

    def create_file_explorer(self, parent_frame):
        # Create the FileExplorerTab
        self.file_explorer_tab = FileExplorerTab(parent_frame, self.sidebar_tab, self)  # Pass the combined_frame as parent and main_window
        self.file_explorer_tab.pack(fill="both", expand=True)  # Pack it inside the combined_frame
        
        

        
        # Create the ButtonFrame and pass the FileExplorerTab instance
        # self.button_frame = ButtonFrame(parent_frame, self.file_explorer_tab)
        # self.button_frame.pack(fill="x")  # Pack it inside the combined_frame
        return self.file_explorer_tab
        
        


        # self.button_frame = ButtonFrame(self.sidebar_tab, self.file_explorer_tab) # Pass the instance
        # self.sidebar_tab.add(frame1)


        
        # file_explorer_label = tk.Label(frame1, text="File Explorer Content (Placeholder)")
        # file_explorer_label.pack(padx=10, pady=10)
        # self.sidebar_tab.add(frame1, text="File Explorer")



    def create_raw_data_overview_tab(self, parent_frame):
        # Create a vertical PanedWindow inside the parent_frame
        self.chromatogram_paned_window = PanedWindow(parent_frame, orient=tk.VERTICAL)
        self.chromatogram_paned_window.pack(fill="both", expand=True)
        # Create upper and lower frames within the provided parent_frame
        self.upper_right_frame = tk.Frame(self.chromatogram_paned_window, bg="white")
        self.lower_right_frame = tk.Frame(self.chromatogram_paned_window, bg="white")

        # Add the frames to the PanedWindow
        self.chromatogram_paned_window.add(self.upper_right_frame, minsize=100)  # Upper frame (chromatogram)
        self.chromatogram_paned_window.add(self.lower_right_frame, minsize=100)  # Lower frame (mass spectrum)
        
        # Add some example content to the frames
        upper_label = tk.Label(self.upper_right_frame, 
                               #text="Chromatogram Display", 
                               bg="white")
        upper_label.pack(padx=1, pady=1)

        lower_label = tk.Label(self.lower_right_frame, 
                               #text="Mass Spectrum Display", 
                               bg="white")
        lower_label.pack(padx=1, pady=1)

        # Configure frame ratios and bind resize event
        self.upper_frame_ratio = 1.5
        self.lower_frame_ratio = 1.0
        self.set_sash_position()  # Initial placement
        parent_frame.bind("<Configure>", self.on_resize)  # Bind to resize event

    #TODO:
    def create_rt_vs_mz_tab(self, parent_frame):
        print("Creating Raw Data Overview Tab")

    def set_sash_position(self): # set the sash position based on the desired ratio
        total_height = self.chromatogram_paned_window.winfo_height()
        if total_height <= 1: # Window not fully initialized yet
            self.chromatogram_paned_window.after(50, self.set_sash_position)
            return
        ratio = self.upper_frame_ratio / (self.upper_frame_ratio + self.lower_frame_ratio)
        sash_position = int(total_height * ratio)
        sash_position = max(0, min(sash_position, total_height)) # Clamp
        self.chromatogram_paned_window.sash_place(0, 0, sash_position)


    def on_resize(self, event):
        self.set_sash_position()

    
        # Add widgets here
        #self.label.pack(pady=20)

        # self.button = tk.Button(root, text="Click Me", command=self.on_button_click)
        # self.button.pack()
        
        # self.plot_frame = tk.Frame(root)
        # self.plot_frame.pack(fill=tk.BOTH, expand=True)
    # def open_raw_data_overview(self, tab_container, tab="Raw data overview"):
    #     # Check if tab with the name exists
    #     for tab_id in tab_container.tabs():
    #         if tab_container.tab(tab_id, "text") == tab:
    #             tab_container.select(tab_id)  # Select the tab to make it visible
    #             return  # Exit to prevent creating another tab
    #     # Tab doesn't exist, create it
    #     raw_data_tab = tk.Frame(tab_container)  # Create the frame
    #     self.create_chromatogram_tab(raw_data_tab)  # Add content to the frame
    #     tab_container.add(raw_data_tab, text=tab)  # Add the tab
    #     tab_container.select(raw_data_tab)  # Select the new tab

    def reopen_tab(self, tab_container, create_tab_func, tab="Raw data overview"):
        # Check if tab with the name exists
        for tab_id in tab_container.tabs():
            if tab_container.tab(tab_id, "text") == tab:
                tab_container.select(tab_id)  # Select the tab to make it visible
                return  # Exit to prevent creating another tab
        # Tab doesn't exist, create it
        raw_data_tab = tk.Frame(tab_container)  # Create the frame
        create_tab_func(raw_data_tab)  # Call the passed function to add content to the frame
        tab_container.add(raw_data_tab, text=tab)  # Add the tab
        tab_container.select(raw_data_tab)  # Select the new tab

    def create_file_explorer(self, parent_frame):
        # Create the FileExplorerTab
        self.file_explorer_tab = FileExplorerTab(parent_frame, self.sidebar_tab, self)  # Pass the combined_frame as parent and main_window
        self.file_explorer_tab.pack(fill="both", expand=True)  # Pack it inside the combined_frame
        return self.file_explorer_tab

    def close_file_explorer_tab(self):
        # Save the state of the File Explorer before closing the tab
        if self.file_explorer_tab:
            self.file_explorer_state = self.file_explorer_tab.save_state()
            self.file_explorer_tab.destroy()
            #clear_frames(self, "upper_right_frame", "lower_right_frame")
            self.file_explorer_tab = None


    def open_cdf(self):
        if self.file_explorer_tab:  # Check if file explorer is created
            self.file_explorer_tab.select_files()
        else:
            print("File Explorer not yet initialized!")


    def new_file(self):
        print("New File")

    def save_file(self):
        print("Save File")

    def open_settings(self):
        print("Open Settings")

    def on_button_click(self):
        self.label.config(text="Button Clicked!")

    
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)


    def option1(self):
        print("Option 1 selected")

    def option2(self):
        print("Option 2 selected")

    def option3(self):
        print("Option 3 selected")










