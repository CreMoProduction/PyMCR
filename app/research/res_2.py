# code for adaptive data reduction

import matplotlib.pyplot as plt
import numpy as np

def reduce_scatter_data(x, y, visible_range):
    """Reduces scatter plot data based on visible range."""
    x_min, x_max = visible_range
    mask = (x >= x_min) & (x <= x_max)
    x_visible = x[mask]
    y_visible = y[mask]

    if len(x_visible) > 1000:  # Adjust threshold
        step = len(x_visible) // 1000  # Adjust division factor
        x_reduced = x_visible[::step]
        y_reduced = y_visible[::step]
        return x_reduced, y_reduced
    else:
        return x_visible, y_visible

def update_scatter_plot(event):
    """Updates the scatter plot when the x-axis limits change."""
    x_min, x_max = ax.get_xlim()
    x_reduced, y_reduced = reduce_scatter_data(x_scatter, y_scatter, (x_min, x_max))
    scatter.set_offsets(np.c_[x_reduced, y_reduced]) # update scatter plot data
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

# Generate sample scatter data
n_points = 10000
x_scatter = np.random.rand(n_points) * 10
y_scatter = np.random.rand(n_points)

# Create the scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(x_scatter, y_scatter, s=5)  # s controls point size

# Connect the event handler
ax.callbacks.connect('xlim_changed', update_scatter_plot)

plt.show()