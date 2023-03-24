
import numpy as np


class CalcAngles:
    def __init__(self, i, minMarkers, maxMarkers, angList, centers, prev_x, prev_y):
        self.i = i
        self.minMarkers = minMarkers
        self.maxMarkers = maxMarkers
        self.angList = angList
        self.centers = centers
        self.prev_x = prev_x
        self.prev_y = prev_y

    def getAngle(self):
        if self.i > self.minMarkers and self.i <= self.maxMarkers:
            if (self.centers[self.i][0][1] - self.prev_y) != 0:
                angle = np.degrees(np.arctan((self.centers[self.i][0][0] - self.prev_x)/(self.centers[self.i][0][1] - self.prev_y)))
                self.angList.append(angle)