# This script demonstrates how to create a zoomable plot with a context menu and a checkbutton to toggle zoom mode.
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# Create the main window
root = tk.Tk()
root.title("Zoom Rectangle with Context Menu and Checkbutton")

# Create a figure
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

# Create a canvas and add the figure to it
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create a toolbar and add it to the window
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.pack_forget()
#toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to reset zoom
def reset_zoom():
    toolbar.home()

# Function to zoom to rectangle
def zoom_to_rectangle(event=None):
    toolbar.zoom()

# Function to save plot as image
def save_plot_as_image(fig):
    fig.savefig("plot.png")

# Variable to track zoom mode
zoom_mode = tk.BooleanVar()

# Function to toggle zoom mode
def toggle_zoom_mode():
    if zoom_mode.get():
        zoom_to_rectangle()
    else:
        zoom_to_rectangle()

# Function to show context menu
def show_context_menu(event):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Reset Zoom", command=reset_zoom)
    context_menu.add_checkbutton(label="Zoom to Rectangle", variable=zoom_mode, command=toggle_zoom_mode)
    context_menu.add_command(label="Save as Image", command=lambda: save_plot_as_image(fig))
    context_menu.post(event.x_root, event.y_root)

# Bind right-click to show context menu
canvas.get_tk_widget().bind("<Button-3>", show_context_menu)

# Start the Tkinter main loop
tk.mainloop()