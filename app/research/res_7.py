# EXamples of baseline correction and data alignment
#---------------------------------------------------------------------
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.signal import savgol_filter

# # Example data: Replace this with your actual chromatogram data
# x = np.linspace(0, 100, 500)
# y = np.sin(x) + np.random.normal(0, 0.1, x.size) + 0.5 * x

# # Fit a polynomial to the baseline
# degree = 3  # Degree of the polynomial
# baseline = np.polyfit(x, y, degree)
# baseline_func = np.poly1d(baseline)

# # Subtract the baseline
# corrected_y = y - baseline_func(x)

# # Optional: Smooth the corrected signal using Savitzky-Golay filter
# smoothed_y = savgol_filter(corrected_y, window_length=51, polyorder=3)

# # Plot the results
# plt.figure(figsize=(10, 6))
# plt.plot(x, y, label='Original Signal')
# plt.plot(x, baseline_func(x), label='Baseline', linestyle='--')
# plt.plot(x, corrected_y, label='Baseline Corrected Signal')
# plt.plot(x, smoothed_y, label='Smoothed Signal', linestyle='-.')
# plt.legend()
# plt.xlabel('Time')
# plt.ylabel('Intensity')
# plt.title('Baseline Correction')
# plt.show()

#================================================================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Example GC-MS data (replace with your actual data)
time1 = np.linspace(0, 10, 100)
intensity1 = np.sin(time1) + np.random.normal(0, 0.1, time1.size)

time2 = np.linspace(0, 10, 100)
intensity2 = np.sin(time2 + 0.5) + np.random.normal(0, 0.1, time2.size)

# Find peaks in both datasets
peaks1, _ = find_peaks(intensity1, height=0)
peaks2, _ = find_peaks(intensity2, height=0)

# Align the datasets by shifting time2 to match the peaks of time1
shift = time1[peaks1[0]] - time2[peaks2[0]]
time2_aligned = time2 + shift

# Plot the original and aligned data
plt.figure(figsize=(10, 6))
plt.plot(time1, intensity1, label='Dataset 1')
plt.plot(time2, intensity2, label='Dataset 2')
plt.plot(time2_aligned, intensity2, label='Aligned Dataset 2', linestyle='--')
plt.xlabel('Time (min)')
plt.ylabel('Intensity')
plt.legend()
plt.title('GC-MS Data Alignment')
plt.show()