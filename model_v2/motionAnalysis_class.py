
import cv2
import numpy as np
from time import time
from detection_class import MarkerDetection
import matplotlib.pyplot as plt

class MotionAnalysis:
    def __init__(self, cameraID, window_name, n_markers=5):
        self.cameraID = cameraID
        self.window_name = window_name
        self.names = ["Shoulder", "Trochanter", "Knee", "Ankle", "V_Metatarsal"]
        self.n_markers = n_markers
        self.first_ankle_angle = []
        self.angle_stored = False
        self.hip_angles = []
        self.knee_angles = []
        self.ankle_angles = []
        self.counting = 0


    def openCamera(self):
        self.camera = cv2.VideoCapture(self.cameraID)
    
    def timeInit(self):
        self.loop_time = time()

    def getFrame(self):
        self.success, self.frame = self.camera.read()

    def trackerInit(self):
        markerDDetection = MarkerDetection(self.frame)
        self.frame, self.boxes, self.indexes = markerDDetection.detect()

        self.multiTracker = cv2.legacy.MultiTracker_create()

        for box in self.boxes:
            self.multiTracker.add(cv2.legacy.TrackerCSRT_create(), self.frame, box)

    def removeEmptyBoxes(self):
        self.boxes = [box for box in self.boxes if np.any(box != [0, 0, 0, 0])]

    def checkMarkers(self):
        if len(self.boxes) != self.n_markers :
            if self.n_markers - len(self.boxes) == 1:
                cv2.putText(self.frame, "1 marker missing", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            elif self.n_markers - len(self.boxes) == -1:
                cv2.putText(self.frame, "1 marker in excess", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            elif self.n_markers - len(self.boxes) > 1:
                cv2.putText(self.frame, f"{int(self.n_markers - len(self.boxes))} markers missing", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            elif self.n_markers - len(self.boxes) < -1:
                cv2.putText(self.frame, f"{abs(int(self.n_markers - len(self.boxes)))} markers in excess", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

            markerDDetection = MarkerDetection(self.frame)
            self.frame, self.boxes, self.indexes = markerDDetection.detect()

            self.multiTracker = cv2.legacy.MultiTracker_create()

            for box in self.boxes:
                self.multiTracker.add(cv2.legacy.TrackerCSRT_create(), self.frame, box)
        else:
            cv2.putText(self.frame, "Tracking", (10, 110), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)
        
            self.tracking, self.boxes = self.multiTracker.update(self.frame)
    
    
    def getCenters(self):
        self.sorted_yCoord = []
        self.centers = []
        prev_x = None  
        first_marker_x = None

        for i, newbox in enumerate(self.boxes):
            x = int(newbox[0])
            y = int(newbox[1])
            w = int(newbox[2])
            h = int(newbox[3])

            center = (x + w//2, y + h//2)
            self.x_coord, self.y_coord = center[0], center[1]
            self.sorted_yCoord.append((self.y_coord, i))
            self.centers.append((center, i))
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
            cv2.circle(self.frame, center, 6, (255, 0, 0), -1)

            if i == 0:  
                first_marker_x = x
            prev_x = x
        
        direction = ""
        if first_marker_x is not None and prev_x is not None:
            if first_marker_x < prev_x:
                direction = "Left -> Right"
            elif first_marker_x > prev_x:
                direction = "Right -> Left"
        cv2.putText(self.frame, direction, (10, 370),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


    def calcAngles(self):
        self.gt_center = []
        self.sorted_yCoord = sorted(self.sorted_yCoord, key=lambda x: x[0])

        prev_x = 0
        prev_y = 0

        for i, (self.y_coord, _) in enumerate(self.sorted_yCoord):
  
            distance = 160
            if prev_x != 0 and prev_y != 0:
                x_gt = self.centers[1][0][0]
                y_gt = self.centers[1][0][1]
                x_le = self.centers[2][0][0]
                y_le = self.centers[2][0][1]
                alpha = np.arctan((x_gt - x_le)/(y_gt - y_le))
                new_x = int(-distance * np.sin(alpha) + x_gt)
                new_y = int(-distance * np.cos(alpha) + y_gt)
                self.gt_center.append((new_x, new_y))

                cv2.circle(self.frame, (new_x, new_y), 10, (0, 0, 255), -1)
            
            prev_x = self.centers[i][0][0]
            prev_y = self.centers[i][0][1]

        self.counting += 1

    def lines(self, showLines=True):

        if showLines:
            points = []
            for i in range(len(self.centers)):
                if i == 1:
                    continue
                x, y = self.centers[i][0][0], self.centers[i][0][1]
                points.append((x, y))
                
            for center in self.gt_center:
                points.append((center[0], center[1]))

            points.sort(key=lambda point: point[1])
            unique_points = {}
            for point in points:
                if point not in unique_points:
                    unique_points[point] = point

            self.unique_points_list = list(unique_points.values())
            print(self.unique_points_list)

            for i in range(1, len(points)):
                cv2.line(self.frame, points[i], points[i-1], (0, 255, 0), 3)


    def writeLabels(self, showLabels=True):

        if showLabels:
            for idx, point in enumerate(self.unique_points_list):
                if idx < len(self.names):
                    name = self.names[idx]
                else:
                    name = f"Marker {idx}"

                x = point[0]
                y = point[1]
                cv2.putText(self.frame, f"{name}", (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
        

    def timeStop(self):
        self.fps = 1/(time() - self.loop_time)
        self.loop_time = time()


    def plotAngles(self):
        if len(self.boxes) == self.n_markers :
            plt.ion()
            fig, ax = plt.subplots()
            for angle in self.hip_angles:
                y = self.counting
                x = angle
                ax.plot(x, y, '-')
                ax.set_title("Hip angle")
                plt.draw()
                print(angle)
            plt.ioff()


    def displayWindow(self):
        cv2.putText(self.frame, f"FPS: {str(round(self.fps, 2))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
        cv2.putText(self.frame, f"Markers: {str(len(self.boxes))}", (10, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)

        cv2.imshow('Gait analysis', self.frame)
        cv2.waitKey(1)


    def closeWindow(self):
        self.camera.release()
        cv2.destroyAllWindows()
