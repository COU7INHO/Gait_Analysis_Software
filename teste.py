import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Create figure and axes
fig, ax = plt.subplots()

# Set x-axis limits
ax.set_xlim(0, 10)
ax.set_ylim(-1, 10)

# Create line object
line, = ax.plot([], [], lw=2)

# Define initialization function
def init():
    line.set_data([], [])
    return line,

# Define animation function
def animate(i):
    x = np.linspace(0, 10, 1000)
    y = np.sin(x + i) + x
    line.set_data(x, y)
    return line,

# Create animation object
ani = FuncAnimation(fig, animate, frames=5000, interval=100, init_func=init, blit=True)

# Show the plot
plt.show()


