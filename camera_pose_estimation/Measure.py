import cv2
import numpy as np
from camera_pose_estimation.object_detector import HomogeneousBgDetector
from vision_calibration.CalibratedImages import CalibratedImages


PARAMETERS = cv2.aruco.DetectorParameters_create()
ARUCO_DICT = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
DETECTOR = HomogeneousBgDetector()

class Measure(CalibratedImages):

    def __init__(self, cam_index1, cam_index2, img1, img2):
        super().__init__(cam_index1, cam_index2)
        self.img1 = img1
        self.img2 = img2

    def calibrated_env(self):

        while (self.cam1.isOpened() and self.cam2.isOpened()):
            
            corners1, _, _ = cv2.aruco.detectMarkers(self.img1, ARUCO_DICT, parameters=PARAMETERS)
            corners2, _, _ = cv2.aruco.detectMarkers(self.img2, ARUCO_DICT, parameters=PARAMETERS)

            if corners1:
                # Draw polygon around the marker
                int_corners1 = np.int0(corners1)
                cv2.polylines(self.img1, int_corners1, True, (0, 255, 0), 5)

                # Aruco Perimeter
                aruco_perimeter = cv2.arcLength(corners1[0], True)

                # Pixel to cm ratio
                pixel_cm_ratio = aruco_perimeter / 20

                contours = DETECTOR.detect_objects(self.img1)

                # Draw objects boundaries
                for cnt in contours:
                    # Get rect
                    rect = cv2.minAreaRect(cnt)
                    (x, y), (w, h), angle = rect

                    # Get Width and Height of the Objects by applying the Ratio pixel to cm
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio

                    # Display rectangle
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    cv2.circle(self.img1, (int(x), int(y)), 5, (0, 0, 255), -1)
                    cv2.polylines(self.img1, [box], True, (255, 0, 0), 2)
                    cv2.putText(self.img1, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (50, 255, 0), 2)
                    cv2.putText(self.img1, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

            if corners2:
                # Draw polygon around the marker
                int_corners2 = np.int0(corners2)
                cv2.polylines(self.img2, int_corners2, True, (0, 255, 0), 5)

                # Aruco Perimeter
                aruco_perimeter2 = cv2.arcLength(corners2[0], True)

                # Pixel to cm ratio
                pixel_cm_ratio2 = aruco_perimeter2 / 20

                contours2 = DETECTOR.detect_objects(self.img2)

                # Draw objects boundaries
                for cnt2 in contours2:
                    # Get rect
                    rect2 = cv2.minAreaRect(cnt2)
                    (x2, y2), (w2, h2), angle2 = rect2

                    # Get Width and Height of the Objects by applying the Ratio pixel to cm
                    object_width2 = w2 / pixel_cm_ratio2
                    object_height2 = h2 / pixel_cm_ratio2

                    # Display rectangle
                    box2 = cv2.boxPoints(rect2)
                    box2 = np.int0(box2)

                    cv2.circle(self.img2, (int(x2), int(y2)), 5, (0, 0, 255), -1)
                    cv2.polylines(self.img2, [box2], True, (255, 0, 0), 2)
                    cv2.putText(self.img2, "Width {} cm".format(round(object_width2, 1)), (int(x2 - 100), int(y2 - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (50, 255, 0), 2)
                    cv2.putText(self.img2, "Height {} cm".format(round(object_height2, 1)), (int(x2 - 100), int(y2 + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

            frames = np.hstack((self.img1, self.img2))
            cv2.imshow("Frames", frames)
            key = cv2.waitKey(1)
            if key == 27:
                break
        
        self.cam1.release()
        self.cam2.release()
        cv2.destroyAllWindows()

     

