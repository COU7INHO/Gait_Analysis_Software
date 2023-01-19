import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

class CreatePlot:
    def __init__(self):
        
        # Create a figure and axes for the plot
        self.fig, self.ax = plt.subplots()

        # Create a list to store the data
        self.data = []

    # Define a function to update the plot
    def update(self, num):
        # Add a new random data point to the list
        self.data.append(random.randint(0, 80))

        # Clear the previous plot
        self.ax.clear()

        # Plot the data
        self.ax.plot(self.data)

    def animation(self):
        # Create an animation object to update the plot every 100ms
        self.ani = FuncAnimation(self.fig, self.update, interval=100)

        # Show the plot
        plt.show()


plot = CreatePlot()
plot.animation()
