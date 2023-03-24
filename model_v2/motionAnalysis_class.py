
import cv2
import numpy as np
from time import time
from detection_class import MarkerDetection
from calc_angles import CalcAngles
import matplotlib.pyplot as plt

class MotionAnalysis:
    def __init__(self, cameraID, window_name, n_markers=5, labels = True, draw_lines = True):
        self.cameraID = cameraID
        self.window_name = window_name
        self.names = ["Shoulder", "Trochanter", "Knee", "Ankle", "V_Metatarsal"]
        self.n_markers = n_markers
        self.labels = labels
        self.draw_lines = draw_lines
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
        prev_center = None
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

            if self.draw_lines:
                if prev_center is not None:
                    cv2.line(self.frame, center, prev_center, (255, 255, 0), 2)

            prev_center = center
            
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
        self.sorted_yCoord = sorted(self.sorted_yCoord, key=lambda x: x[0])

        prev_x = 0
        prev_y = 0

        trunk_angles = []
        thigh_angles = []
        shank_angles = []
        foot_angles = []

        for i, (self.y_coord, marker_id) in enumerate(self.sorted_yCoord):
            if i < len(self.names):
                name = self.names[i]
            else:
                name = f"Marker {i}"

            if prev_x != 0 and prev_y != 0:
                trunk_angle = CalcAngles(i, 0, 1, trunk_angles, self.centers, prev_x, prev_y)
                trunk_angle.getAngle()

                thigh_angle = CalcAngles(i, 1, 2, thigh_angles, self.centers, prev_x, prev_y)
                thigh_angle.getAngle()
                
                shank_angle = CalcAngles(i, 2, 3, shank_angles, self.centers, prev_x, prev_y)
                shank_angle.getAngle()

                if i > 3 and i <= 4:
                    if (self.centers[i][0][1] - prev_y) != 0:
                        foot_angle = np.degrees(np.arctan((self.centers[i][0][0] - prev_x)/(self.centers[i][0][1] - prev_y)))
                        if foot_angle >= -180:
                            foot_angle = 180 - foot_angle
                        foot_angles.append(foot_angle)
    
            prev_x = self.centers[i][0][0]
            prev_y = self.centers[i][0][1]

            for trunk_ang, thigh_ang, shank_ang, foot_ang in zip(trunk_angles, thigh_angles, shank_angles, foot_angles):
                self.hip_angle = thigh_ang - trunk_ang
                self.knee_angle = thigh_ang - shank_ang
                self.ankle_angle = foot_ang - shank_ang - 90

                if self.ankle_angle > 90 and self.ankle_angle < 180:
                    self.ankle_angle -= 180

                if len(self.boxes) == self.n_markers and self.angle_stored == False:
                    self.first_ankle_angle.append(self.ankle_angle)
                    self.angle_stored = True

                if len(self.first_ankle_angle) > 0:
                    self.ankle_angle -= self.first_ankle_angle[0]

                cv2.putText(self.frame, f"Hip Angle: {round(self.hip_angle, 2)}", (10, 240),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)
                cv2.putText(self.frame, f"Knee Angle: {round(self.knee_angle, 2)}", (10, 280),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)
                cv2.putText(self.frame, f"Ankle Angle: {round(self.ankle_angle, 2)}", (10, 320),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)
                
                self.hip_angles.append(self.hip_angle)
                self.knee_angles.append(self.knee_angle)
                self.ankle_angles.append(self.ankle_angle)

            if self.labels:
                for j, newbox in enumerate(self.boxes):
                    if j == marker_id:
                        x = int(newbox[0])
                        y = int(newbox[1])
                        w = int(newbox[2])
                        h = int(newbox[3])
                        cv2.putText(self.frame, f"{name}", (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 128), 1)
        
        self.counting += 1


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
