
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import MaxNLocator

from app.file_services.file_handler import (
   save_plot_as_image,
   save_plot_data_to_csv
   )
from app.file_services.settings_handler import (
   get_user_settings,
   save_user_settings,
   get_user_setting_value,
   save_user_setting_value
)

global_cursor_x = None
global_cursor_y = None

class Plotter:
   def __init__(self, 
               main_window, 
               placer,
               title="Plot"
               ):
      
      self.title = title
      self.fig = None
      self.main_window = main_window
      self.fig, self.ax = plt.subplots()
      self.fig.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.12)
      self.canvas = FigureCanvasTkAgg(self.fig, master=getattr(self.main_window, placer))
      self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Pack canvas FIRST
      self.toolbar = NavigationToolbar2Tk(self.canvas, getattr(self.main_window, placer))
      self.toolbar.pack_forget()  # Hide the default matplotlib toolbar
      self.lines = []
      self.cursor_x, self.cursor_y = None, None
      self.annot = self.ax.annotate("", xy=(0, 0), xytext=(20, 20),
                                 textcoords="offset points",
                                 bbox=dict(boxstyle="round", fc="w"),
                                 arrowprops=dict(arrowstyle="->"))
      self.annot.set_visible(False)

      self.panning = False  # Initialize a panning flag
      self.pan_x = None
      self.pan_y = None

      self.zoom_mode = tk.BooleanVar(value=False)
      #self.zoom_mode = tk.BooleanVar(value=get_user_setting_value("plotter.zoom_mode", default_value=False)) 
      self.show_legend = tk.BooleanVar(value=get_user_setting_value(f"{self.title}.plotter.show_legend", default_value=False))
      

      # Use Matplotlib's built-in pan and zoom, but don't activate them initially
      # self.toolbar.pan()  # Don't activate pan initially
      # self.toolbar.zoom()  # Don't activate zoom initially 

      self._connect_events()  # Connect event handlers

   
   
   #=========================================
   def plot_data(self, 
                 data_list, 
                 plot_type="line", 
                 title_type="Plot", 
                 title_full = "Plot", 
                 xlabel="X", 
                 ylabel="Y",
                 x_data = "rt", 
                 y_data = "intensity",
                 **kwargs
                 ):
      """
      Plots data with specified type.

      Args:
         data_list: List of data tuples (same format as before).
         plot_type: Type of plot ("line", "scatter", "bar", etc.).
         title: Plot title.
         xlabel: X-axis label.
         ylabel: Y-axis label.
         **kwargs: Additional keyword arguments to pass to the plotting function
                     (e.g., marker style for scatter plots, bar width for bar plots).
      """
      self.ax.clear()  # Clear axes ONCE, before the loop
      self.lines = []

      for (x_data, y_data), file_name in data_list:
         if plot_type == "line":
               line, = self.ax.plot(x_data, y_data, label=file_name, linewidth=1.2, alpha=0.7,  **kwargs)
         elif plot_type == "scatter":
               line = self.ax.scatter(x_data, y_data, label=file_name, s=50, alpha=0.5, **kwargs)
               self.lines.append(line)  # For scatter, append the PathCollection
         elif plot_type == "bar":
               line = self.ax.bar(x_data, y_data, label=file_name, alpha=0.7, **kwargs)
               self.lines.append(line)  # For bar, append the BarContainer
         else:
               raise ValueError(f"Invalid plot_type: {plot_type}")

         if plot_type != "scatter":  # Only for line plots
               self.lines.append(line)  # For annotations, etc. (line plots)

      self.ax.set_title(title_full, fontsize=9)
      self.ax.set_xlabel(xlabel, fontsize=7)
      self.ax.set_ylabel(ylabel, fontsize=7)
      self.ax.tick_params(axis='both', which='major', labelsize=7)
      self.ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0)) #for setting scientific notation.
      self.ax.xaxis.set_major_locator(MaxNLocator(10)) # Set the number of ticks on the x-axis
      self.ax.yaxis.set_major_locator(MaxNLocator(8)) # Set the number of ticks on the y-axis
      self.ax.set_facecolor('white') # Set background color to gray
      self.ax.grid(True, linestyle='--', color='gray', alpha=0.3, linewidth=0.4) # Add dashed grid


      #self.ax.legend()  # Show the legend (now all lines will be there)
      self.toolbar.pack_forget()  # Hide the default matplotlib toolbar
      # Update annotations to handle scatter plots correctly:
      self.annot = self.ax.annotate("", xy=(0, 0), xytext=(20, 20),
                                    textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="w"),
                                    arrowprops=dict(arrowstyle="->"))
      self.annot.set_visible(False)

      self._toggle_legend()
      #self._toggle_zoom_mode() #FIXME:
   #===============End of plot_data========================



   #=================Legend========================
   def _toggle_legend(self):  #добаяляем метод для отображения легенды
         if self.show_legend.get():
               self.ax.legend().set_visible(True)
               self.ax.legend(prop={'size': 7})
               #TODO:
               save_user_setting_value(f"{self.title}.plotter.show_legend", "True")
         else:
               self.ax.legend().set_visible(False)
               save_user_setting_value(f"{self.title}.plotter.show_legend", "False")
         self.fig.canvas.draw_idle()

   #=================Events========================
   def _connect_events(self):
      self.fig.canvas.mpl_connect("motion_notify_event", self._hover)
      self.fig.canvas.mpl_connect("button_press_event", self._on_click)
      self.fig.canvas.mpl_connect("key_press_event", self._on_key)
      self.fig.canvas.mpl_connect("scroll_event", self._zoom)
      self.fig.canvas.mpl_connect("button_press_event", self._pan_press)
      self.fig.canvas.mpl_connect("motion_notify_event", self._pan_move)
      self.fig.canvas.mpl_connect("button_release_event", self._pan_release)
      self.fig.canvas.mpl_connect("button_press_event", lambda event: self._reset_zoom() if event.dblclick and event.button == 1 else None)
      self.fig.canvas.mpl_connect("button_release_event", self._show_context_menu)


   def _update_annot(self, ind, line):
      if isinstance(line, matplotlib.collections.PathCollection): # For scatter plot
         x, y = line.get_offsets()[ind["ind"][0]]
      elif isinstance(line, matplotlib.container.BarContainer): # For bar plot
         x = line[ind["ind"][0]].get_x() + line[ind["ind"][0]].get_width()/2
         y = line[ind["ind"][0]].get_height()
      else: # For line plot
         x, y = line.get_data()
         x = x[ind["ind"][0]]
         y = y[ind["ind"][0]]

      self.annot.xy = (x, y)
      if isinstance(line, matplotlib.collections.PathCollection): # For scatter plot
         text = f"x: {x:.2f}\ny: {y:.2e}\n{line.get_label()}"
      elif isinstance(line, matplotlib.container.BarContainer): # For bar plot
         text = f"x: {x:.2f}\ny: {y:.2e}\n{line.get_label()}"
      else: # For line plot
         text = f"x: {x:.2f}\ny: {y:.2e}\n{line.get_label()}"
      self.annot.set_text(text)
      self.annot.set_fontsize(8)
      self.annot.get_bbox_patch().set_alpha(0.2)
      if isinstance(line, matplotlib.collections.PathCollection): # For scatter plot
         color = line.get_facecolors()[0]
      elif isinstance(line, matplotlib.container.BarContainer): # For bar plot
         color = line.patches[0].get_facecolor()
      else: # For line plot
         color = line.get_color()
      self.annot.get_bbox_patch().set_facecolor(color)
      self.annot.get_bbox_patch().set_edgecolor(color)
      self.annot.set_color(color)
      self.annot.arrow_patch.set_color(color)
      return x, y

   def _hover(self, event):
      vis = self.annot.get_visible()
      if event.inaxes == self.ax:
         for line in self.lines:
               if isinstance(line, matplotlib.container.BarContainer):
                  for patch in line.get_children():
                     cont, _ = patch.contains(event)
                     if cont:
                        ind = {"ind": [line.get_children().index(patch)]}
                        self._update_annot(ind, line)
                        self.annot.set_visible(True)
                        self.fig.canvas.draw_idle()
                        return
               else:
                  cont, ind = line.contains(event)
                  if cont:
                     self._update_annot(ind, line)
                     self.annot.set_visible(True)
                     self.fig.canvas.draw_idle()
                     return
      if vis:
         self.annot.set_visible(False)
         self.fig.canvas.draw_idle()

   #=========================================
   def _on_click(self, event):
      if event.inaxes == self.ax and event.button in [1, 3]:
         global global_cursor_x, global_cursor_y
         global_cursor_x, global_cursor_y = event.xdata, event.ydata
         print(f"Pressed at x={global_cursor_x:.2f}, y={global_cursor_x:.2f}")

   def _on_key(self, event):
      if event.inaxes == self.ax and event.key == 'enter':
         global global_cursor_x, global_cursor_y
         global_cursor_x, global_cursor_y = event.xdata, event.ydata
         print(f"Pressed at x={global_cursor_x:.2f}, y={global_cursor_x:.2f}")
   #=========================================

   def _zoom(self, event):
      base_scale = 1.1
      cur_xlim = self.ax.get_xlim()
      cur_ylim = self.ax.get_ylim()
      xdata = event.xdata
      ydata = event.ydata
      if event.button == 'up':
         scale_factor = 1 / base_scale
      elif event.button == 'down':
         scale_factor = base_scale
      else:
         scale_factor = 1

      new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
      new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
      relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
      rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
      self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
      self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
      self.fig.canvas.draw_idle()

   def _pan_move(self, event):
      if event.button == 2 and self.panning:
         dx = event.xdata - self.pan_x
         dy = event.ydata - self.pan_y
         cur_xlim = self.ax.get_xlim()
         cur_ylim = self.ax.get_ylim()
         self.ax.set_xlim(cur_xlim[0] - dx, cur_xlim[1] - dx)
         self.ax.set_ylim(cur_ylim[0] - dy, cur_ylim[1] - dy)
         self.fig.canvas.draw_idle()

   _pan_move.pressed = False
   _pan_move.x = None
   _pan_move.y = None

   def _pan_press(self, event):
      if event.button == 2:  # Middle mouse button
         self.panning = True
         self.pan_x = event.xdata
         self.pan_y = event.ydata

   def _pan_release(self, event):
      if event.button == 2:
         self.panning = False

   def _reset_zoom(self):
      print("Resetting zoom")
      self.ax.autoscale()
      self.fig.canvas.draw_idle()
   #=========================================
   def _zoom_to_rectangle(self, event=None):
      self.toolbar.zoom()
   
   # Function to toggle zoom mode
   def _toggle_zoom_mode(self):
      if  self.zoom_mode.get():
         self._zoom_to_rectangle()
         #save_user_setting_value("plotter.zoom_mode", "True") 
      else:
         self._zoom_to_rectangle()
         #save_user_setting_value("plotter.zoom_mode", "False") 


   def _show_context_menu(self, event):
      from app.gui.gui_callbacks import (
         plot_mass_spectrum,
      )
      from app.gui.widgets.file_explorer import (
      global_selected_filenames,
      global_datasets,
      )
      #selected_filenames = FileExplorerTab.get_checked_files_filenames(self)
      selected_filenames = global_selected_filenames
      if event.button == 3 and event.name == 'button_release_event':  # Check BOTH button and event name
         self.context_menu = tk.Menu(self.main_window, tearoff=0)
         self.context_menu.add_command(label="Reset Zoom", command= self._reset_zoom)
         self.context_menu.add_checkbutton(label="Zoom to Rectangle",  variable= self.zoom_mode, command= self._toggle_zoom_mode)
         self.context_menu.add_checkbutton(label="Show Legend", variable=self.show_legend, command=self._toggle_legend)
         self.context_menu.add_separator()
         #NOTE:
         self.context_menu.add_command(label="Plot m/z at current RT", command=lambda: plot_mass_spectrum(
               self.main_window, 
               global_selected_filenames, 
               global_datasets,
               target_rt=global_cursor_x,
               )
            )
         self.context_menu.add_separator()
         save_menu = tk.Menu(self.context_menu, tearoff=0)
         self.context_menu.add_cascade(label="Save", menu=save_menu)
         save_menu.add_command(label="Save as PNG", command=lambda: save_plot_as_image(self.fig, default_filename= "TIC", format='png'))
         save_menu.add_command(label="Save as JPG", command=lambda: save_plot_as_image(self.fig, default_filename= "TIC", format='jpg'))
         save_menu.add_command(label="Save as PDF", command=lambda: save_plot_as_image(self.fig, default_filename= "TIC", format='pdf'))
         save_menu.add_command(label="Save as SVG", command=lambda: save_plot_as_image(self.fig, default_filename= "TIC", format='svg'))
         save_menu.add_separator()
         save_menu.add_command(label="Export plot as CSV", command=lambda: save_plot_data_to_csv(self.fig, default_filename= "TIC"))
         self.context_menu.post(event.guiEvent.x_root, event.guiEvent.y_root)


