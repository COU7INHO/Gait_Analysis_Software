import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class RealTimePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.xdata = []
        self.ydata = []
        self.ln, = plt.plot([], [], 'ro')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Knee angle')
        self.ax.set_ylim([-10, 80])
        self.ax.grid()
        
    def update(self, knee_angle):
        self.xdata.append(time.time())
        self.ydata.append(knee_angle)
        self.ln.set_data(self.xdata, self.ydata)
        self.ax.relim()
        self.ax.autoscale_view()
        
    def animation(self):
        ani = FuncAnimation(self.fig, self.update, interval=100)
        plt.show()
        
# Create an instance of the RealTimePlot class
plot = RealTimePlot()

# Start the animation
plot.animation()

# Add new angle
while True:
    knee_angle = calculate_knee_angle() # replace with your function to calculate the knee angle
    plot.update(knee_angle)
