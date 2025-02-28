# app/gui/callbacks.py

import os
import tkinter as tk
from .widgets import Plotter
from app.file_services.file_handler import (
   open_files,
   read_netcdf,
   )

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk
from tkinter import Menu
import matplotlib
import numpy as np
import gc


# def on_open_click(main_window):
#    # Clear the previous plot
   
#    for widget in main_window.upper_right_frame.winfo_children(): # Destroy all widgets in the upper_right_frame
#       widget.destroy()
#    plt.close('all')
#    gc.collect() # Force garbage collection
   
#    file_paths = []
#    file_paths = open_files()
#    data_list = []
#    datasets = []
#    if file_paths:
#       for file_path in file_paths:
#          dataset = read_netcdf(file_path)
#          rt = dataset.variables['scan_acquisition_time'][:]
#          intensity = dataset.variables['total_intensity'][:]
#          file_name = file_path.split('/')[-1]  # Extract the file name from the file path
#          data_list.append(((rt, intensity), file_name))
#          datasets.append(dataset)
#       main_window.plotter_upper = Plotter(main_window, placer= "upper_right_frame")
#       main_window.after(0, lambda: main_window.plotter_upper.plot_data(data_list,  
#                                                                  plot_type="line", 
#                                                                  title="Chromatogram", 
#                                                                  xlabel="RT, sec", 
#                                                                  ylabel="Total Ion Counts", 
#                                                                  x_data="rt", 
#                                                                  y_data="intensity",
#                                                                  )) # Plot immediately (0 ms delay)
#       main_window.plotter_lower = Plotter(main_window, placer= "lower_right_frame")
#       main_window.after(0, lambda: main_window.plotter_lower.plot_data(data_list,  
#                                                                  plot_type="line", 
#                                                                  title="Mass Spectrum", 
#                                                                  xlabel="RT, sec", 
#                                                                  ylabel="Total Ion Counts", 
#                                                                  x_data="rt", 
#                                                                  y_data="intensity", 
#                                                                  )) # Plot immediately (0 ms delay)
#          #main_window.plotter.plot_data(main_window, data_list,  title="Plot", x_data = "rt", y_data = "intensity", xlabel="X", ylabel="Y")
#          #plot_chromatogram(main_window, data_list)
         
#    else:
#       print("No files selected.")



def plot_chromatogram(main_window, checked_files, datasets):
   print(checked_files)
   # Clear the previous plot
   for widget in main_window.upper_right_frame.winfo_children():  # Destroy all widgets in the upper_right_frame
      widget.destroy()
   plt.close('all')
   gc.collect()  # Force garbage collection

   selected_datasets = {
      fp: datasets[fp] for fp in checked_files if fp in datasets
   }

   data_list = []  # List to store data for plotting

   for file_path, dataset in selected_datasets.items():
      rt = dataset.variables['scan_acquisition_time'][:]
      intensity = dataset.variables['total_intensity'][:]
      file_name = file_path.split('/')[-1]  # Extract the file name
      data_list.append(((rt, intensity), file_name))  # Store data and filename

   #===========plot arguments================
   placer="upper_right_frame"
   plot_type="line"
   title_type="Total Ion Chromatogram"
   title_full = title_type 
   xlabel="RT, sec"
   ylabel="Total Ion Counts"
   x_data="rt"
   y_data="intensity"
   #=========================================
   main_window.plotter_upper = Plotter(main_window, 
                                       placer, 
                                       title_type)

    # Ensure the plot is updated
   if data_list:  # Only plot if there is data
      #print("Data list contents:", data_list)
      main_window.plotter_upper.plot_data(
         data_list,
         plot_type,
         title_type,
         title_full,
         xlabel,
         ylabel,
         x_data,
         y_data,

      )
   else:
      print("No data to plot.")  # Debug print





def plot_mass_spectrum(main_window, checked_files, datasets, target_rt=200):
   #print(checked_files)
   # Clear the previous plot
   for widget in main_window.lower_right_frame.winfo_children():  # Destroy all widgets in the lower_right_frame
      widget.destroy()
   plt.close('all')
   gc.collect()  # Force garbage collection

   selected_datasets = {
      fp: datasets[fp] for fp in checked_files if fp in datasets
   }

   data_list = []  # List to store data for plotting

   for file_path, dataset in selected_datasets.items():
      rt = dataset.variables['scan_acquisition_time'][:]
      scan_index = np.argmin(np.abs(rt - target_rt))
      file_name = file_path.split('/')[-1]  # Extract the file name
      print(f"Selected scan at RT: {rt[scan_index]} seconds for file {file_path}")
      scan_indices = dataset.variables['scan_index'][:]
      start_idx = scan_indices[scan_index] + 1
      end_idx = scan_indices[scan_index + 1] if scan_index < len(scan_indices) - 1 else len(dataset.variables['mass_values'][:])
      
      mz = dataset.variables['mass_values'][start_idx:end_idx]
      intensity = dataset.variables['intensity_values'][start_idx:end_idx]

      max_intensity = np.max(intensity) if intensity.size > 0 else 0 # Handle empty intensity arrays
      threshold = 0.008 * max_intensity #убрать все пики ниже порога 0.8% от максимального значения
      intensity[intensity < threshold] = 0

      data_list.append(((mz, intensity), file_name))

   #===========plot arguments================
   placer="lower_right_frame"
   plot_type="bar"
   title_type="Mass Spectrum"
   title_full = f'Mass Spectrum at RT: {round(target_rt,2)} sec, scan id: {scan_index}' 
   xlabel="m/z"
   ylabel="Intensity"
   x_data="mz"
   y_data="intensity"
   #=========================================
   main_window.plotter_lower = Plotter(main_window, 
                                       placer,
                                       title_type,
                                       )

    # Ensure the plot is updated
   if data_list:  # Only plot if there is data
      #print("Data list contents:", data_list)
      main_window.plotter_lower.plot_data(
         data_list,
         plot_type,
         title_type,
         title_full,
         xlabel,
         ylabel,
         x_data,
         y_data,
      )
   else:
      print("No data to plot.")  # Debug print

def plot_rt_vs_mz(main_window, checked_files, datasets):
   #print(checked_files)
   # Clear the previous plot
   for widget in main_window.upper_right_frame.winfo_children():  # Destroy all widgets in the upper_right_frame
      widget.destroy()
   plt.close('all')
   gc.collect()  # Force garbage collection

   selected_datasets = {
      fp: datasets[fp] for fp in checked_files if fp in datasets
   }

   data_list = []  # List to store data for plotting

   for file_path, dataset in selected_datasets.items():
      rt = dataset.variables['scan_acquisition_time'][:]
      intensity = dataset.variables['total_intensity'][:]
      file_name = file_path.split('/')[-1]  # Extract the file name
      data_list.append(((rt, intensity), file_name))  # Store data and filename

   #===========plot arguments================
   placer="upper_right_frame"
   plot_type="line"
   title_type="Total Ion Chromatogram"
   title_full = title_type 
   xlabel="RT, sec"
   ylabel="Total Ion Counts"
   x_data="rt"
   y_data="intensity"
   #=========================================
   main_window.plotter_upper = Plotter(main_window, 
                                       placer, 
                                       title_type)

    # Ensure the plot is updated
   if data_list:  # Only plot if there is data
      #print("Data list contents:", data_list)
      main_window.plotter_upper.plot_data(
         data_list,
         plot_type,
         title_type,
         title_full,
         xlabel,
         ylabel,
         x_data,
         y_data,

      )
   else:
      print("No data to plot.")  # Debug print



#================================================================================================
def clear_frames(parent, *frame_names): # удалить все графики
   """
   Clears the specified frames or all child widgets within a parent widget.

   Args:
      parent: The parent widget (e.g., self.main_window).  This is where the 
               search for frames/widgets will start.
      *frame_names: Variable number of frame names (strings) to clear. 
                     If no frame names are provided, *all* child widgets 
                     of the parent will be destroyed.
   """

   if frame_names:  # If specific frame names are given
      for frame_name in frame_names:
         if frame_name == "*": # Wildcard to clear all descendants
               for child in parent.winfo_children():
                  clear_frames(child,"*") # Recursive call to clear all children of the child
                  child.destroy()
               return # Stop after clearing all descendants. No need to continue the loop
         try:
               frame = getattr(parent, frame_name) # Get the frame object. Important!
               for widget in frame.winfo_children():
                  widget.destroy()
         except AttributeError:
               print(f"Frame '{frame_name}' not found within parent.")
   else:  # If no frame names are given, clear all children of the parent
      for widget in parent.winfo_children():
         widget.destroy()