import cv2
import imutils
import numpy as np


built_in_camera = cv2.VideoCapture(0)
external_cam1 = cv2.VideoCapture(1)
external_cam2 = cv2.VideoCapture(2)


WIDTH = 500

while True:
    _, frame1 = built_in_camera.read()
    _, frame2 = external_cam1.read()
    _, frame3 = external_cam2.read()

    frame1 = imutils.resize(frame1, width=WIDTH)
    frame3 = imutils.resize(frame3, width=WIDTH)

    if built_in_camera.isOpened():

        w, h = frame1.shape[:2]
        
    
    frame2 = cv2.resize(frame2, (h, w))

    frames = np.hstack([frame1, frame2, frame3])

    cv2.imshow("imagem", frames)

    if cv2.waitKey(1) == ord('q'):
        break


built_in_camera.release()
external_cam1.release()
cv2.destroyAllWindows()