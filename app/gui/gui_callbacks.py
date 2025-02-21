import os
import tkinter as tk
from .widgets import Plotter
from app.utils.file_utils import (
    select_files,
    read_netcdf,
    )

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk
from tkinter import Menu
import matplotlib
import gc


def on_open_click(main_window):
   # Clear the previous plot
   
   for widget in main_window.upper_right_frame.winfo_children(): # Destroy all widgets in the upper_right_frame
      widget.destroy()
   plt.close('all')
   gc.collect() # Force garbage collection
   
   file_paths = []
   file_paths = select_files()
   data_list = []
   datasets = []
   if file_paths:
      for file_path in file_paths:
         dataset = read_netcdf(file_path)
         rt = dataset.variables['scan_acquisition_time'][:]
         intensity = dataset.variables['total_intensity'][:]
         file_name = file_path.split('/')[-1]  # Extract the file name from the file path
         data_list.append(((rt, intensity), file_name))
         datasets.append(dataset)
      main_window.plotter_upper = Plotter(main_window, placer= "upper_right_frame")
      main_window.after(0, lambda: main_window.plotter_upper.plot_data(data_list,  
                                                                 plot_type="line", 
                                                                 title="Chromatogram", 
                                                                 xlabel="RT, sec", 
                                                                 ylabel="Total Ion Counts", 
                                                                 x_data="rt", 
                                                                 y_data="intensity",
                                                                 )) # Plot immediately (0 ms delay)
      main_window.plotter_lower = Plotter(main_window, placer= "lower_right_frame")
      main_window.after(0, lambda: main_window.plotter_lower.plot_data(data_list,  
                                                                 plot_type="line", 
                                                                 title="Mass Spectrum", 
                                                                 xlabel="RT, sec", 
                                                                 ylabel="Total Ion Counts", 
                                                                 x_data="rt", 
                                                                 y_data="intensity", 
                                                                 )) # Plot immediately (0 ms delay)
         #main_window.plotter.plot_data(main_window, data_list,  title="Plot", x_data = "rt", y_data = "intensity", xlabel="X", ylabel="Y")
         #plot_chromatogram(main_window, data_list)
         
   else:
      print("No files selected.")

