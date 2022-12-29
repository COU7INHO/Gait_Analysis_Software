
import numpy as np

def calcAngle(center_points, sorted_yCoord):
    shoulder_x = center_points[sorted_yCoord[0][1]][0]
    shoulder_y = center_points[sorted_yCoord[0][1]][1]

    trochanter_x = center_points[sorted_yCoord[1][1]][0]
    trochanter_y = center_points[sorted_yCoord[1][1]][1]

    knee_x = center_points[sorted_yCoord[2][1]][0]
    knee_y = center_points[sorted_yCoord[2][1]][1]

    angle = np.degrees(np.atan2(knee_y - trochanter_y, knee_x - trochanter_x) - np.atan2(shoulder_y - trochanter_y, shoulder_x - trochanter_x))
    
    return angle