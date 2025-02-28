# reads netCDF files and plots chromatograms using Plotly.
print("plotly in browser")

import subprocess
import sys

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

install_and_import('tkinter')
install_and_import('netCDF4')
install_and_import('pandas')
install_and_import('plotly')
install_and_import('webbrowser')

import tkinter as tk
from tkinter import filedialog
import netCDF4 as nc
import pandas as pd
import webbrowser
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import locale



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
    print(df.head())
    return rt, intensity

def plot_chromatogram(data_list):
    traces = []
    for data, file_name in data_list:
        rt, intensity = data
        trace = go.Scatter(x=rt, y=intensity, mode='lines', name=file_name)
        traces.append(trace)
    
    # Create subplots with 2 rows and 1 column
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=("Chromatogram 1", "Chromatogram 2"))

    # Add traces to the first plot
    for trace in traces:
        fig.add_trace(trace, row=1, col=1)

    # Add the same traces to the second plot
    # for trace in traces:
    #     fig.add_trace(trace, row=2, col=1)
    
    fig.update_layout(title='Chromatogram', xaxis=dict(title='RT'), yaxis=dict(title='Intensity'))
    file_path = 'chromatogram.html'
    pyo.plot(fig, filename=file_path, auto_open=False)
    webbrowser.open(file_path)

if __name__ == "__main__":
    file_paths = select_files()
    data_list = []
    if file_paths:
        for file_path in file_paths:
            rt, intensity = read_netcdf(file_path)
            file_name = file_path.split('/')[-1]  # Extract the file name from the file path
            data_list.append(((rt, intensity), file_name))
        plot_chromatogram(data_list)
    else:
        print("No files selected.")