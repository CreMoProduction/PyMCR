# embed a Plotly plot in a Tkinter window using PyWebView.
print("plotly in tkinter")

import tkinter as tk
import webview
import plotly.graph_objects as go
import numpy as np
import os

# Create the Tkinter window
root = tk.Tk()
root.title("Embed Plotly in Tkinter with PyWebView")
root.geometry("800x600")

# Create a paned window
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=1)

# Create two frames
frame1 = tk.Frame(paned_window, bg='lightgrey')
frame2 = tk.Frame(paned_window, bg='white')

# Add the frames to the paned window
paned_window.add(frame1, minsize=200)
paned_window.add(frame2, minsize=200)

# Generate test data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a Plotly plot
fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name='sin(x)'))
fig.update_layout(title="Interactive Plotly Plot", xaxis_title="X-axis", yaxis_title="Y-axis")

# Save the Plotly plot as an HTML file
html_file = "plotly_plot.html"
fig.write_html(html_file)

# Get the full path to the HTML file
html_path = os.path.abspath(html_file)

# Embed the browser in Tkinter using pywebview
def embed_browser():
    webview.create_window("Plotly Plot", url=f"file://{html_path}", width=400, height=600)
    webview.start()

# Embed the browser in the second frame
frame1.after(100, embed_browser)

# Run the Tkinter event loop
root.mainloop()