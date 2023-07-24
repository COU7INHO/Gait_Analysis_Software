
import cv2
import numpy as np
from time import time
from detection_class import MarkerDetection


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
        self.init_angle_ang = None
        self.filtered_ankle_angles = []
        self.direction = "left_to_right"
        self.showLines = True
        self.showLabels= True
        self.showbbox = True

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
        self.sorted_centers = []
        self.centers = []

        for i, newbox in enumerate(self.boxes):
            x = int(newbox[0])
            y = int(newbox[1])
            w = int(newbox[2])
            h = int(newbox[3])

            center = (x + w//2, y + h//2)
            self.x_coord, self.y_coord = center[0], center[1]
            self.sorted_centers.append(((self.x_coord, self.y_coord), i))
            self.centers.append((center, i))
            if self.showbbox:
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
            cv2.circle(self.frame, center, 6, (255, 0, 0), -1)

    def getDirection(self):

        x_coords = [center[0] for center, _ in self.sorted_centers]
        mean_x_coord = np.mean(x_coords)
        self.direction= ""
        if hasattr(self, 'prev_mean_x_coord'):
            if mean_x_coord > self.prev_mean_x_coord:
                self.direction = "left_to_right"
                print(self.direction)
            else:
                self.direction = "right_to_left"
                print(self.direction)

        self.prev_mean_x_coord = mean_x_coord

    def calcAngles(self):
        self.gt_center = []
        self.sorted_centers = sorted(self.sorted_centers, key=lambda x: x[0][1])

        prev_x = 0
        prev_y = 0

        for i, (_, _) in enumerate(self.sorted_centers):

            distance = 160  #! Colocar uma parte na GUI para inserir este valor em centímetros 
            if prev_x != 0 and prev_y != 0:
                x_gt = self.centers[1][0][0]
                y_gt = self.centers[1][0][1]
                x_le = self.centers[2][0][0]
                y_le = self.centers[2][0][1]
                alpha = np.arctan((x_gt - x_le)/(y_gt - y_le))
                new_x = int(-distance * np.sin(alpha) + x_gt)
                new_y = int(-distance * np.cos(alpha) + y_gt)
                self.gt_center.append((new_x, new_y))

                #* trunk_angle
                trunk_angle = np.degrees(np.arctan((new_x - self.centers[0][0][0])/(new_y - self.centers[0][0][1])))
                
                #* thigh_angle
                if self.centers[2][0][0] - self.centers[1][0][0] == 0:
                    thigh_angle = 0
                else:
                    thigh_angle = np.degrees(np.arctan((self.centers[2][0][1] - self.centers[1][0][1])/(self.centers[2][0][0] - self.centers[1][0][0])))

                #* shank_angle
                if self.centers[3][0][0] - self.centers[2][0][0] == 0:
                    shank_angle = 0
                else:
                    shank_angle = np.degrees(np.arctan((self.centers[3][0][1] - self.centers[2][0][1])/(self.centers[3][0][0] - self.centers[2][0][0])))
                
                #* foot_angle
                foot_angle = np.degrees(np.arctan((self.centers[4][0][1] - self.centers[3][0][1])/(self.centers[4][0][0] - self.centers[3][0][0])))

                #* hip_ang
                hip_ang = trunk_angle - thigh_angle 
                
                if hip_ang > 0:
                    hip_ang -= 90
                elif hip_ang <= 0:
                    hip_ang += 90
                if abs(hip_ang) <= 40:
                    self.hip_angles.append(hip_ang)
    
                #cv2.putText(self.frame, f"Hip angle = {str(round(hip_ang, 2))}", (10, 160), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)
                
                #* knee_ang
                knee_ang = thigh_angle - shank_angle
  
                if knee_ang > 100:
                    knee_ang = 180 - knee_ang
                elif knee_ang < 0:
                    knee_ang = abs(knee_ang)
                else:
                    continue

                self.knee_angles.append(knee_ang)
                
                #cv2.putText(self.frame, f"Knee angle = {str(round(knee_ang, 2))}", (10, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)

                #* ankle_ang
                ankle_ang = foot_angle - shank_angle 
                if self.init_angle_ang is None:
                    self.init_angle_ang = ankle_ang
                if ankle_ang < 0:
                    ankle_ang -= self.init_angle_ang
                elif ankle_ang > 0:
                    ankle_ang = 180 - ankle_ang + self.init_angle_ang

                self.ankle_angles.append(ankle_ang)

                #cv2.putText(self.frame, f"Ankle angle = {str(round(ankle_ang, 2))}", (10, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)
                cv2.circle(self.frame, (new_x, new_y), 10, (0, 0, 255), -1)

            prev_x = self.centers[i][0][0]
            prev_y = self.centers[i][0][1]

        self.counting += 1

    def lines(self):
        if self.showLines:
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

            for i in range(1, len(points)):
                cv2.line(self.frame, points[i], points[i-1], (0, 255, 0), 3)

    def labels(self):
        if self.showLabels:
            for idx, point in enumerate(self.unique_points_list):
                if idx < len(self.names):
                    name = self.names[idx]

                x = point[0]
                y = point[1]
                cv2.putText(self.frame, f"{name}", (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

    def timeStop(self):
        self.fps = 1/(time() - self.loop_time)
        self.loop_time = time()
        cv2.putText(self.frame, f"FPS: {str(round(self.fps, 2))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)

    def displayWindow(self):
        #cv2.putText(self.frame, f"FPS: {str(round(self.fps, 2))}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
        #cv2.putText(self.frame, f"Markers: {str(len(self.boxes))}", (10, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
        if self.frame.shape[0] > 0 and self.frame.shape[1] > 0:
            cv2.imshow('Gait analysis', self.frame)
        #cv2.waitKey(int(1000/120))
        cv2.waitKey(0)

    def closeWindow(self):
        self.camera.release()
        cv2.destroyAllWindows()
