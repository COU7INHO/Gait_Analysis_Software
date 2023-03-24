
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from motionAnalysis_class import MotionAnalysis


class RealTimePlot(MotionAnalysis):
    def __init__(self, cameraID, window_name, plotInterval=100):
        super().__init__(cameraID, window_name)
        self.frame = 0
        self.plotInterval = plotInterval
    
    def getHipAngle(self):
        self.fig, self.ax = plt.subplots()

        for hip_angle in self.hip_angles:
            self.ax.plot(hip_angle)
    
    def animateHip(self):
        self.ani = FuncAnimation(fig=self.fig, func=self.getHipAngle, interval=self.plotInterval)
        plt.show()
    
    def p(self):
        for angle in self.hip_angles:
            print(round(angle, 2))

