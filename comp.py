import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Generate a noisy signal
t = np.linspace(0, 10, 1000)
x = np.sin(2*np.pi*5*t) + np.sin(2*np.pi*20*t) + np.random.randn(len(t))

# Define the Butterworth filter parameters
order = 4
cutoff_freq = 10

# Create the Butterworth filter
b, a = butter(order, cutoff_freq/(120/2), btype='low')

# Apply the filter to the signal
filtered_x = filtfilt(b, a, x)

# Plot the original and filtered signals
plt.figure()
plt.plot(t, x, label='Original signal')
plt.plot(t, filtered_x, label='Filtered signal')
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()
