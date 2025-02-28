import os
import tkinter as tk
from app.utils.file_handler import (
    open_files,
    read_netcdf,
    get_scan_data,
    save_plot_as_image,
    )
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk
from tkinter import Menu
from PIL import Image, ImageTk
import matplotlib
import gc

fig = None
def on_open_click(main_window):
   # Clear the previous plot
   
   for widget in main_window.upper_right_frame.winfo_children(): # Destroy all widgets in the upper_right_frame
      widget.destroy()
      plt.close('all')
      gc.collect() # Force garbage collection
   
   file_paths = []
   file_paths = open_files()
   data_list = []
   datasets = []
   if file_paths:
      for file_path in file_paths:
         dataset = read_netcdf(file_path)
         rt = dataset.variables['scan_acquisition_time'][:]
         intensity = dataset.variables['total_intensity'][:]
         file_name = file_path.split('/')[-1]  # Extract the file name from the file path
         data_list.append(((rt, intensity), file_name))
         plot_chromatogram(main_window, data_list)
         datasets.append(dataset)
   else:
      print("No files selected.")

def plot_chromatogram(main_window, data_list):
    
   class CustomToolbar(NavigationToolbar2Tk):
      def _init_toolbar(self):
         self.basedir = os.path.join(matplotlib.rcParams['datapath'], 'images')
         self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
         )
         
         for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
               self.add_separator()
            else:
               image = Image.open(os.path.join(self.basedir, f'{image_file}.png'))
               image = image.resize((10, 10), Image.ANTIALIAS)  # Resize the icon
               photo = ImageTk.PhotoImage(image)
               button = self._Button(self, text=text, image=photo, command=getattr(self, callback))
               button._ntimage = photo
               button.pack(side=tk.LEFT)
               if tooltip_text is not None:
                  self._add_tooltip(button, tooltip_text)

   fig, ax = plt.subplots()
   fig.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.12)  # Adjust margins for each side
   lines = []
   for (rt, intensity), file_name in data_list:
      line, = ax.plot(rt, intensity, label=file_name)
      lines.append(line)
   ax.set_title("Chromatogram", fontsize=10)
   ax.set_xlabel("RT", fontsize=8)
   ax.set_ylabel("Total Ion Intensity", fontsize=8)
   ax.tick_params(axis='both', which='major', labelsize=8)
   for line in lines:
      line.set_linewidth(1.2)  # line width
      line.set_alpha(0.5)  # line opacity

   for widget in main_window.upper_right_frame.winfo_children():
      widget.destroy()

   canvas = FigureCanvasTkAgg(fig, master=main_window.upper_right_frame)
   canvas.draw()
   
   
   
   toolbar = NavigationToolbar2Tk(canvas, main_window.upper_right_frame)
   toolbar.pack_forget() # Hide the default matplotlib toolbar
   # toolbar = CustomToolbar(canvas, main_window.upper_right_frame)
   # toolbar.update()
   # toolbar.pack(side=tk.TOP, fill=tk.X)
   canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

   cursor_x, cursor_y = None, None
   
   annot = ax.annotate("", xy=(0,0), xytext=(20,20),
                  textcoords="offset points",
                  bbox=dict(boxstyle="round", fc="w"),
                  arrowprops=dict(arrowstyle="->"))
   annot.set_visible(False)

   def update_annot(ind, line):
      x, y = line.get_data()
      annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
      text = f"rt: {x[ind['ind'][0]]:.2f}\ntic: {y[ind['ind'][0]]:.2e}\n{line.get_label()}"
      annot.set_text(text)
      annot.set_fontsize(8)
      annot.get_bbox_patch().set_alpha(0.2)
      annot.get_bbox_patch().set_facecolor(line.get_color())
      annot.get_bbox_patch().set_edgecolor(line.get_color())
      annot.set_color(line.get_color())
      annot.arrow_patch.set_color(line.get_color())
      return x[ind["ind"][0]], y[ind["ind"][0]]

   def hover(event):
      vis = annot.get_visible()
      if event.inaxes == ax:
         for line in lines:
            cont, ind = line.contains(event)
            if cont:
               update_annot(ind, line)
               annot.set_visible(True)
               fig.canvas.draw_idle()
               return
      if vis:
         annot.set_visible(False)
         fig.canvas.draw_idle()
   
   def on_click(event):
      if event.inaxes == ax and event.button in [1, 3] :  # Left mouse button
         nonlocal cursor_x, cursor_y
         cursor_x, cursor_y = event.xdata, event.ydata
         # TODO: Implement get_scan_data
         # Do I need to plot mass spec for one file or multiple files?
         # get_scan_data(file_path, cursor_x)
         print(f"Clicked at x={cursor_x:.2f}, y={cursor_y:.2f}")

   def on_key(event):
      if event.inaxes == ax and event.key == 'enter': # Enter key
         nonlocal cursor_x, cursor_y
         cursor_x, cursor_y = event.xdata, event.ydata
         print(f"Pressed at x={cursor_x:.2f}, y={cursor_y:.2f}")

   

   def zoom(event):
      base_scale = 1.1
      cur_xlim = ax.get_xlim()
      cur_ylim = ax.get_ylim()
      xdata = event.xdata
      ydata = event.ydata
      if event.button == 'up':
         scale_factor = 1 / base_scale
      elif event.button == 'down':
         scale_factor = base_scale
      else:
         scale_factor = 1
         print(event.button)
      new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
      new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
      relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
      rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
      ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
      ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
      fig.canvas.draw_idle()

   def pan(event):
        if event.button == 2:  # Middle mouse button or left mouse button when zoom mode is not enabled
         if event.name == 'button_press_event':
               pan.press(event)
         elif event.name == 'motion_notify_event' and pan.pressed:
               dx = event.xdata - pan.x
               dy = event.ydata - pan.y
               cur_xlim = ax.get_xlim()
               cur_ylim = ax.get_ylim()
               ax.set_xlim(cur_xlim[0] - dx, cur_xlim[1] - dx)
               ax.set_ylim(cur_ylim[0] - dy, cur_ylim[1] - dy)
               fig.canvas.draw_idle()
         elif event.name == 'button_release_event':
               pan.pressed = False

   pan.pressed = False
   pan.x = None
   pan.y = None

   def pan_press(event):
        if event.button == 2:  # Middle mouse button or left mouse button when zoom mode is not enabled
         pan.pressed = True
         pan.x = event.xdata
         pan.y = event.ydata

   def pan_release(event):
      if event.button in [2]: 
         pan.pressed = False

   def reset_zoom():
      print("Resetting zoom")
      ax.autoscale()
      fig.canvas.draw_idle()

   def zoom_to_rectangle(event=None):
      toolbar.zoom()
   # Variable to track zoom mode
   zoom_mode = tk.BooleanVar()
   # Function to toggle zoom mode
   def toggle_zoom_mode():
      if zoom_mode.get():
         zoom_to_rectangle()
      else:
         zoom_to_rectangle()

   def show_context_menu(event):
      if event.button == 3 and event.name == 'button_release_event':  # Check BOTH button and event name
         context_menu = tk.Menu(main_window, tearoff=0)
         context_menu.add_command(label="Reset Zoom", command=reset_zoom)
         context_menu.add_checkbutton(label="Zoom to Rectangle",  variable= zoom_mode, command= toggle_zoom_mode)
         context_menu.add_separator()
         context_menu.add_command(label="Plot m/z at current RT", command=lambda: save_plot_as_image(fig))
         context_menu.add_separator()
         context_menu.add_command(label="Save as Image", command=lambda: save_plot_as_image(fig))
         context_menu.post(event.guiEvent.x_root, event.guiEvent.y_root)
         # Check if the right mouse button was *released*
      

   fig.canvas.mpl_connect("button_release_event", show_context_menu) 
   # Connect the hover, click, and key press events to the functions
   fig.canvas.mpl_connect("motion_notify_event", hover)
   fig.canvas.mpl_connect("button_press_event", on_click)
   fig.canvas.mpl_connect("key_press_event", on_key)
   fig.canvas.mpl_connect("scroll_event", zoom)
   fig.canvas.mpl_connect("button_press_event", pan_press)
   fig.canvas.mpl_connect("motion_notify_event", pan)
   fig.canvas.mpl_connect("button_release_event", pan_release)
   
   fig.canvas.mpl_connect("button_press_event", lambda event: reset_zoom() if event.dblclick and event.button == 1 else None)

   plt.close(fig)
   return fig # needed for def save plot as image



