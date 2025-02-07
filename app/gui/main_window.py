# gui/gui.py
import tkinter as tk
from tkinter import Menu, PanedWindow
#from tkinter import filedialog
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
from utils.file_utils import (
    read_netcdf
    )
from app.gui.gui_callbacks import (
    on_open_click,
    #save_plot_as_image
)
import webbrowser
from tkinterweb import HtmlFrame
import plotly.io as pio


from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk

class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack()
        # self.root.title("My First App")
        # self.root.geometry("400x300")

        # Create the menu bar
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Create the File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open CDF", command=lambda: on_open_click(self))
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        # Create the Options menu
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(label="Settings", command=self.open_settings)
        
        #=====================================
        self.toolbar = tk.Frame(self.root, background="#e8e8e8", height=15)
        self.statusbar = tk.Frame(self.root, background="#e8e8e8", height=15)
        self.main = tk.PanedWindow(self.root, background="#ffffff")

        self.toolbar.pack(side="top", fill="x")
        self.statusbar.pack(side="bottom", fill="x")
        self.main.pack(side="top", fill="both", expand=True)
        #=====================================
        
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
        # Create upper and lower frames
        self.upper_right_frame = tk.Frame(self.right_paned_window, bg="white")
        self.lower_right_frame = tk.Frame(self.right_paned_window, bg="white")
        # Add the frames to the PanedWindow
        self.right_paned_window.add(self.upper_right_frame, minsize=200) # chromatogram plotly
        self.right_paned_window.add(self.lower_right_frame, minsize=200) # mass spectrum plotly
        # Set the sash position to make the frames equal height 50% each
        self.right_frame.after(100, lambda: self.right_paned_window.sash_place(0, 0, self.right_frame.winfo_height() // 2))


 


        # Add a label to the toolbar and statusbar
        self.toolbar_label = tk.Label(self.toolbar, text="toolbar", font=("Arial", 8))
        self.toolbar_label.pack(side="left", padx=1, pady=1)
        self.statusbar = tk.Label(self.statusbar, text="statusbar", font=("Arial", 8))
        self.statusbar.pack(side="left", padx=1, pady=1)

        # Add widgets here
        #self.label.pack(pady=20)

        # self.button = tk.Button(root, text="Click Me", command=self.on_button_click)
        # self.button.pack()
        
        # self.plot_frame = tk.Frame(root)
        # self.plot_frame.pack(fill=tk.BOTH, expand=True)
    


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










