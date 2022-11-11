
#? Function to open both cameras and take pictures of the chessboard in 
#? different positions 
#! Only works with two cameras - one camera 

import cv2
import os
import numpy as np

class GetCalibrationImages:

    def __init__(self, cam1_index, cam2_index):
        self.cam1_index = cam1_index
        self.cam2_index = cam2_index
        self.path1 = f"./vision_calibration/images_to_calibrate/Camera{self.cam1_index}/"
        self.path2 = f"./vision_calibration/images_to_calibrate/Camera{self.cam2_index}/"


    def get_images(self):
        if not os.path.exists(self.path1):
            os.makedirs(self.path1)
        if not os.path.exists(self.path2):
            os.makedirs(self.path2)
            
        cam1 = cv2.VideoCapture(self.cam1_index)
        cam2 = cv2.VideoCapture(self.cam2_index)

        n_images = 0
        while cam1.isOpened():
            _, img1 = cam1.read()
            _, img2 = cam2.read()

            k = cv2.waitKey(5)

            if k == 27:
                break
            elif k == ord('s'):
                cv2.imwrite(self.path1 + "Cam" + str(self.cam1_index) + '_' + str(n_images) + ".png", img1)
                cv2.imwrite(self.path2 + "Cam" + str(self.cam1_index) + '_' + str(n_images) + ".png", img2)
                print(f"images saved -> {n_images}")
                n_images += 1

            frames = np.hstack((img1, img2))
            cv2.imshow("Cameras", frames)

        cam1.release()
        cam2.release()
        cv2.destroyAllWindows()

