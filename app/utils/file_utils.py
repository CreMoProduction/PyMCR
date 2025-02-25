# utils/file_utils.py

import tkinter as tk
from tkinter import filedialog
import netCDF4 as nc
import pandas as pd
import locale
import numpy as np

import matplotlib.pyplot as plt 
from IPython.display import display # For displaying df

def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    locale.setlocale(locale.LC_CTYPE, "sv_SE.UTF-8")  # Set the locale to Swedish
    file_paths = filedialog.askopenfilenames(title="Select netCDF files", filetypes=[("netCDF files", "*.cdf")])
    print(file_paths)
    return file_paths


def read_netcdf(file_path):
    dataset = nc.Dataset(file_path)
    rt = dataset.variables['scan_acquisition_time'][:]
    intensity = dataset.variables['total_intensity'][:]
    df = pd.DataFrame({'RT': rt, 'Intensity': intensity})
    # NOTE: Display every second row
    df = df.iloc[::2]  # Remove every second row
    display(df)
    #print(df.head())
    return dataset
    #, rt, intensity

# TODO:
# def get_scan_data(file_path, target_rt):
#     # Get retention times
#     rt = nc.Dataset(file_path).variables['scan_acquisition_time'][:]

#     # Find the closest scan to the target retention time
#     scan_index = np.argmin(np.abs(rt - target_rt))

#     # Print the selected retention time
#     print(f"Selected scan at RT: {rt[scan_index]} seconds")

#     # Extract scan index mapping
#     scan_indices = dataset.variables['scan_index'][:]

#     # Define start and end positions for the selected scan
#     start_idx = scan_indices[scan_index] + 1
#     end_idx = scan_indices[scan_index + 1] if scan_index < len(scan_indices) - 1 else len(dataset.variables['mass_values'][:])

#     # Extract m/z and intensity values for the selected scan
#     mz = dataset.variables['mass_values'][start_idx:end_idx]
#     intensity = dataset.variables['intensity_values'][start_idx:end_idx]
    
#     print("m/z values:", mz)
#     print("Intensity values:", intensity)

#     return mz, intensity

    





def save_plot_as_image(fig, default_filename="plot.png"):
    """Saves a matplotlib figure as a PNG image, with a file dialog.
    Args:
        fig: The matplotlib figure object to save.
        default_filename: The default filename to suggest in the dialog.
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        initialfile=default_filename  # Suggest a default filename
    )
    if file_path:
        try:
            fig.savefig(file_path, dpi=300)  # Add dpi for better resolution
            print(f"Plot saved as {file_path}")
            return True  # Indicate success
        except Exception as e:
            print(f"Error saving plot: {e}")
            return False # Indicate failure
    return False # Return False if the user cancels the dialog.

# target_rt = 200
# mz, intensity = get_scan_data(dataset, target_rt)



