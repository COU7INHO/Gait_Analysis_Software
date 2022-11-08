import cv2 
import numpy as np
import imutils
from object_detector import HomogeneousBgDetector

parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

detector = HomogeneousBgDetector()
    
cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)

while True:

    _, frame1 = cam1.read()
    _, frame2 = cam2.read()

    # Get Aruco marker
    corners1, _, _ = cv2.aruco.detectMarkers(frame1, aruco_dict, parameters=parameters)
    corners2, _, _ = cv2.aruco.detectMarkers(frame2, aruco_dict, parameters=parameters)
   
    if corners1:

        # Draw polygon around the marker
        int_corners = np.int0(corners1)
        cv2.polylines(frame1, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners1[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20

        contours = detector.detect_objects(frame1)

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

            cv2.circle(frame1, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(frame2, [box], True, (255, 0, 0), 2)
            cv2.putText(frame1, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (50, 255, 0), 2)
            cv2.putText(frame1, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)



    if corners2:

        # Draw polygon around the marker
        int_corners = np.int0(corners2)
        cv2.polylines(frame2, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners2[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20

        contours = detector.detect_objects(frame2)

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

            cv2.circle(frame2, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(frame2, [box], True, (255, 0, 0), 2)
            cv2.putText(frame2, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (50, 255, 0), 2)
            cv2.putText(frame2, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)


    frames = np.hstack([frame1, frame2])
    cv2.imshow("Image", frames)
    if cv2.waitKey(1) == ord('q'):
        break

cam1.release()
cv2.destroyAllWindows()