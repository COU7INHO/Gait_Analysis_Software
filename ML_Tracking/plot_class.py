
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class RealTimePlot:
    def __init__(self, angle):
        self.angle = angle
        self.fig, self.ax = plt.subplots()

    def updateAngle(self, ang):
        new_value = get_ankle_angle_value()
        ankle_angle_values.append(new_value)
        self.ax.clear()
        self.ax.plot(self.angle)

    def showPlot(self):
        self.ani = FuncAnimation(self.fig, update, frames=range(0, 100), repeat=True)
        plt.show()


