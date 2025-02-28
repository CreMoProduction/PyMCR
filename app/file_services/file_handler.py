# utils/file_utils.py

import tkinter as tk
from tkinter import filedialog
import netCDF4 as nc
import pandas as pd
import locale
import numpy as np

import matplotlib.pyplot as plt 
from IPython.display import display # For displaying df

from app.file_services.settings_handler import (
   get_user_settings,
   save_user_settings,
   get_user_setting_value,
   save_user_setting_value
)

def open_files(file_explorer_tab):
    """Open files and add them to the file explorer tab."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    locale.setlocale(locale.LC_CTYPE, "sv_SE.UTF-8")  # Set the locale to Swedish
    file_paths = filedialog.askopenfilenames(title="Select netCDF files", filetypes=[("netCDF files", "*.cdf")])
    filenames = file_paths
    datasets = {} # Dictionary to store datasets, keyed by file path
    for file_path in file_paths:
        datasets.update(read_netcdf(file_path)) # Update datasets with the new dataset
    return (
        filenames, 
        datasets 
        )

    
def read_netcdf(file_path):
    dataset = nc.Dataset(file_path)
    return {file_path: dataset}  # Return a dictionary containing the dataset



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

    





def save_plot_as_image(fig, default_filename=None, format="png"):
    """Saves a matplotlib figure as an image, with a file dialog.
    Args:
        fig: The matplotlib figure object to save.
        default_filename: The default filename to suggest in the dialog.
        format: The format to save the image in (e.g., 'png', 'jpg', 'pdf', 'svg').
    """
    if default_filename is None:
        default_filename = f"plot.{format}"
    
    filetypes = {
        "png": [("PNG files", "*.png")],
        "jpg": [("JPEG files", "*.jpg"), ("JPEG files", "*.jpeg")],
        "pdf": [("PDF files", "*.pdf")],
        "svg": [("SVG files", "*.svg")]
    }
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=f".{format}",
        filetypes=filetypes.get(format, [("All files", "*.*")]),
        initialfile=default_filename  # Suggest a default filename
    )
    if file_path:
        try:
            fig.savefig(file_path, format=format, dpi=300)  # Add dpi for better resolution
            print(f"Plot saved as {file_path}")
            return True  # Indicate success
        except Exception as e:
            print(f"Error saving plot: {e}")
            return False  # Indicate failure
    return False  # Return False if the user cancels the dialog.



def save_plot_data_to_csv(fig, default_filename=None):
    """
    Saves the data from a matplotlib plot to a CSV file.

    Handles different plot types (lines, scatter, images, etc.) and 
    extracts data accordingly. It attempts to get labels from the plot 
    elements to use as column names, falling back to generic names if 
    labels aren't available.

    Args:
        fig: The matplotlib Figure object.
        default_filename: The default filename to suggest in the dialog.
    """
    if default_filename is None:
        default_filename = "plot_data.csv"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=default_filename  # Suggest a default filename
    )
    if not file_path:
        print("Save operation cancelled.")
        return

    data = []
    labels = []

    for ax in fig.get_axes():  # Iterate through subplots if any
        for line in ax.lines:
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            label = line.get_label() or "y"  # Get label or default to "y" for the first data series
            
            if not labels:  # Add 'x' label for the x-axis if no label exists
                labels.append("x")
            if label not in labels:  # Append the new label if it doesn't already exist
                labels.append(label)

            # Handle cases where xdata and ydata are single points (e.g., scatter plots)
            if np.isscalar(xdata):
                xdata = [xdata]
            if np.isscalar(ydata):
                ydata = [ydata]

            if len(data) == 0:  # Initialize the data list on the first line
                data.append(xdata)
                data.append(ydata)  # Add the initial y-data
            else:
                if len(xdata) != len(data[0]):  # Check if x-data has the same length as the first data series
                    max_len = max(len(xdata), len(data[0]))
                    xdata = np.pad(xdata, (0, max_len - len(xdata)), constant_values=np.nan)
                    ydata = np.pad(ydata, (0, max_len - len(ydata)), constant_values=np.nan)
                    data = [np.pad(d, (0, max_len - len(d)), constant_values=np.nan) for d in data]
                data.append(ydata)  # Append subsequent y-data

        # Handle images (e.g., imshow)
        for image in ax.images:
            im_data = image.get_array()
            # For images, we will assume x and y are indices.
            x_indices = np.arange(im_data.shape[1])  # Column indices
            y_indices = np.arange(im_data.shape[0])  # Row indices

            if not labels:
                labels.extend(["x", "y"])
            if "image_data" not in labels:
                labels.append("image_data")

            data.append(x_indices)
            data.append(y_indices)
            data.append(im_data.flatten())  # Flatten the image data

    # Create a Pandas DataFrame and save to CSV
    try:
        df = pd.DataFrame(np.array(data).T, columns=labels)  # Transpose to have correct orientation
    except ValueError as e:  # Handle different lengths of data
        print(f"Error creating dataframe: {e}")
        print("Data shapes:", [len(d) for d in data])
        return

    df.to_csv(file_path, index=False)
    print(f"Plot data saved to {file_path}")


# target_rt = 200
# mz, intensity = get_scan_data(dataset, target_rt)



