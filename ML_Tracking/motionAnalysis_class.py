
import cv2
import numpy as np
from time import time
from detection_class import MarkerDetection

class MotionAnalysis:
    def __init__(self, cameraID, window_name, n_markers=5, labels = True, draw_lines = True):
        self.cameraID = cameraID
        self.window_name = window_name
        self.names = ["Shoulder", "Trochanter", "Knee", "Ankle", "V_Metatarsal"]
        self.n_markers = n_markers
        self.labels = labels
        self.draw_lines = draw_lines
        self.ankle_angles = []
        self.first_ankle_angle = None
        self.angle_stored = False

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

        for i, newbox in enumerate(self.boxes):
            x = int(newbox[0])
            y = int(newbox[1])
            w = int(newbox[2])
            h = int(newbox[3])
            
            center = (x + w//2, y + h//2)
            self.y_coord = center[1]

            self.sorted_yCoord.append((self.y_coord, i))

            self.centers.append((center, i))

            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
            cv2.circle(self.frame, center, 6, (255, 0, 0), -1)

            if self.draw_lines:
                if prev_center is not None:
                    cv2.line(self.frame, center, prev_center, (255, 255, 0), 2)
            
            prev_center = center

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
                if i > 0 and i <= 1:
                    if (self.centers[i][0][1] - prev_y) != 0:
                        trunk_angle = np.degrees(np.arctan((self.centers[i][0][0] - prev_x)/(self.centers[i][0][1] - prev_y)))
                        trunk_angles.append(trunk_angle)

                if i > 1 and i <= 2:
                    if (self.centers[i][0][1] - prev_y) != 0:
                        thigh_angle = np.degrees(np.arctan((self.centers[i][0][0] - prev_x)/(self.centers[i][0][1] - prev_y)))
                        thigh_angles.append(thigh_angle)

                if i > 2 and i <= 3:
                    if (self.centers[i][0][1] - prev_y) != 0:
                        shank_angle = np.degrees(np.arctan((self.centers[i][0][0] - prev_x)/(self.centers[i][0][1] - prev_y)))
                        shank_angles.append(shank_angle)

                if i > 3 and i <= 4:
                    if (self.centers[i][0][1] - prev_y) != 0:
                        foot_angle = np.degrees(np.arctan((self.centers[i][0][0] - prev_x)/(self.centers[i][0][1] - prev_y)))
                        if foot_angle >= -180:
                            foot_angle = 180 - foot_angle
                        foot_angles.append(foot_angle)
    
            prev_x = self.centers[i][0][0]
            prev_y = self.centers[i][0][1]

            for trunk_ang, thigh_ang, shank_ang, foot_ang in zip(trunk_angles, thigh_angles, shank_angles, foot_angles):
                hip_ang = thigh_ang - trunk_ang
                knee_angle = thigh_ang - shank_ang
                ankle_angle = foot_ang - shank_ang - 90

                if ankle_angle > 90 and ankle_angle < 180:
                    ankle_angle = ankle_angle - 180

                if len(self.boxes) == self.n_markers and self.angle_stored == False:
                    self.ankle_angles.append(ankle_angle)
                    self.first_ankle_angle = self.ankle_angles[0]
                    self.angle_stored = True

                if self.first_ankle_angle is not None:
                    ankle_angle = ankle_angle - self.first_ankle_angle

                cv2.putText(self.frame, f"Hip Angle: {round(hip_ang, 2)}", (10, 240),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)
                cv2.putText(self.frame, f"Knee Angle: {round(knee_angle, 2)}", (10, 280),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)
                cv2.putText(self.frame, f"Ankle Angle: {round(ankle_angle, 2)}", (10, 320),cv2.FONT_HERSHEY_COMPLEX, 1, (20, 255, 217), 2)

            if self.labels:
                for j, newbox in enumerate(self.boxes):
                    if j == marker_id:
                        x = int(newbox[0])
                        y = int(newbox[1])
                        w = int(newbox[2])
                        h = int(newbox[3])
                        cv2.putText(self.frame, f"{name}", (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 128), 1)

    def timeStop(self):
        self.fps = 1/(time() - self.loop_time)
        self.loop_time = time()

    def displayWindow(self):
        cv2.putText(self.frame, f"FPS: {str(round(self.fps, 2))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
        cv2.putText(self.frame, f"Markers: {str(len(self.boxes))}", (10, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
        cv2.imshow('Gait analysis', self.frame)

    def closeWindow(self):
        self.camera.release()
        cv2.destroyAllWindows()
