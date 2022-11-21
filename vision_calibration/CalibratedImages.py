import cv2
import imutils
import numpy as np


class CalibratedImages:

    def __init__(self, cam_index1, cam_index2):
        self.cam_index1 = cam_index1
        self.cam_index2 = cam_index2
        self.cam1 = cv2.VideoCapture(self.cam_index1)                    
        self.cam2 =  cv2.VideoCapture(self.cam_index2)

    def calibratedImages(self, imshow=False):
        cv_file = cv2.FileStorage()
        cv_file.open("./vision_calibration/stereoMap.xml", cv2.FileStorage_READ)

        stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
        stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
        stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
        stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

        while (self.cam1.isOpened() and self.cam2.isOpened()):
            _, self.img1 = self.cam1.read()
            _, self.img2 = self.cam2.read()
            self.img1 = cv2.remap(self.img1, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
            self.img2 = cv2.remap(self.img2, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
            
            if imshow == True:
                #self.img1 = imutils.resize(self.img1, width=750)
                #self.img2 = imutils.resize(self.img2, width=750)
                #cv2.imshow("Camera 1 calibrated", self.img1) 
                #cv2.imshow("Camera 2 calibrated", self.img2)

                frames = np.hstack((self.img1, self.img2))
                cv2.imshow("Frames", frames)

                k = cv2.waitKey(1)
                if k == 27:
                    break
            else:
                break

        self.cam1.release()
        self.cam2.release()

        cv2.destroyAllWindows()

        return self.img1, self.img2