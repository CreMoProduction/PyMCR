# mass spectra at a given retention time (RT) with the top N peaks labeled.

import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import os

def read_cdf_files(file_paths, target_rt):
    results = []
    for file_path in file_paths:
        with Dataset(file_path, 'r') as nc_file:
            rt = nc_file.variables['scan_acquisition_time'][:]
            scan_index = np.argmin(np.abs(rt - target_rt))
            print(f"Selected scan at RT: {rt[scan_index]} seconds for file {file_path}")

            scan_indices = nc_file.variables['scan_index'][:]
            start_idx = scan_indices[scan_index] + 1
            end_idx = scan_indices[scan_index + 1] if scan_index < len(scan_indices) - 1 else len(nc_file.variables['mass_values'][:])

            mz = nc_file.variables['mass_values'][start_idx:end_idx]
            intensity = nc_file.variables['intensity_values'][start_idx:end_idx]

            max_intensity = np.max(intensity) if intensity.size > 0 else 0 # Handle empty intensity arrays
            threshold = 0.002 * max_intensity
            intensity[intensity < threshold] = 0

            results.append((file_path, rt[scan_index], scan_index, mz, intensity)) 

    return results

def plot_mass_specs(data, target_rt, top_n):
    plt.figure(figsize=(10, 6))

    file_colors = {}
    for file_path, _, _, _, _ in data:
        line, = plt.plot([], [], label=os.path.basename(file_path), alpha=0.4)
        file_colors[file_path] = line.get_color()

    for file_path, rt, scan_index, mz, intensity in data:  
        plt.plot(mz, intensity, label=os.path.basename(file_path), alpha=0.4, color=file_colors[file_path])

        if len(intensity) > 0:
            top_n_indices = np.argsort(intensity)[-min(top_n, len(intensity)):]
            top_n_mz = mz[top_n_indices]
            top_n_intensities = intensity[top_n_indices]

            for mz_val, peak_intensity in zip(top_n_mz, top_n_intensities):
                plt.text(mz_val, peak_intensity, f'{mz_val:.2f}', ha='center', va='bottom', fontsize=8, color=file_colors[file_path])


    plt.title(f'Mass Spec Line Plot at RT: {target_rt}, scan: {scan_index}')
    plt.xlabel('Mass/Charge (m/z)')
    plt.ylabel('Intensity')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    plt.show()

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("CDF files", "*.cdf")])
    target_rt = float(input("Enter the target retention time (RT): "))
    top_n = int(input("Enter the number of top peaks to label: "))

    data = read_cdf_files(file_paths, target_rt) # No need for all_intensities, all_mz anymore

    if data: # Check if data is not empty
        plot_mass_specs(data, target_rt, top_n)
    else:
        print("No data found for the selected retention time in the chosen files or no files selected.")

root = tk.Tk()
root.withdraw()
select_files()