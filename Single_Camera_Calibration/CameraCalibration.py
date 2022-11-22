'''Os objpoints são os mesmos para as duas câmaras
Fazer algum ciclo for que criar objpoints para cada uma das câmaras '''

import cv2 as cv 
import os
import glob
import numpy as np


class CalibrateCamera():

    def __init__(self, cam1_index, cam2_index):
        self.cam1_index = cam1_index
        self.cam2_index = cam2_index
        self.indices = [self.cam1_index, self.cam2_index]
        self.cameras = []
        for index in self.indices:
            camera = cv.VideoCapture(index)
            self.cameras.append(camera)

    def getCalibrationImages(self):
        self.paths = []
        for index in self.indices:
            path = f"./Single_Camera_calibration/CalibrationImages/Camera{index}/"
            self.paths.append(path)

        if not os.path.exists(self.paths[0]):
            os.makedirs(self.paths[0])
        if not os.path.exists(self.paths[1]):
            os.makedirs(self.paths[1])

        new_images = input("Do you want to get new calibration images? Y -> Yes\n >> ").upper()
        
        if new_images == 'Y':
            if os.path.exists(self.paths[0]):
                for file1 in os.scandir(self.paths[0]):
                    if file1.name.endswith(".png"):
                        os.unlink(file1)
            if os.path.exists(self.paths[1]):
                for file2 in os.scandir(self.paths[1]):
                    if file2.name.endswith(".png"):
                        os.unlink(file2)

            for camera, index in zip(self.cameras, self.indices):
                n_images = 0

                while camera.isOpened():
                    success, frame = camera.read()

                    k = cv.waitKey(1)

                    if k == ord('q'):
                        break
                    elif k == ord('s'):
                        cv.imwrite(self.paths[index] + "Cam" + str(index) + '_' + str(n_images) + ".png", frame)
                        print(f"Camera{index}, images saved -> {n_images}")
                        n_images += 1
                    
                    cv.imshow("Get New Calibration Images", frame)

                camera.release()
                cv.destroyAllWindows()

    def findChessboardCorners(self,squareSize=25, chessboardRows=9, chessboardCols=6, imshow=False):

        self.squareSize = squareSize
        self.chessboardRows = chessboardRows
        self.chessboardCols = chessboardCols
        self.imshow = imshow
        chessboardSize = (self.chessboardRows, self.chessboardCols)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        objp = np.zeros((self.chessboardCols*self.chessboardRows,3), np.float32)
        objp[:,:2] = np.mgrid[0:self.chessboardRows,0:self.chessboardCols].T.reshape(-1,2)
        objp = objp * self.squareSize
        
        self.objpoints = [] 
        self.imgpoints = [] 
        
        path = 0
        index = 0
        for camera in self.cameras:
            images = glob.glob(self.paths[path] + "*.png")

            for img in images:
                self.frame = cv.imread(img)
                self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
                self.ret, corners = cv.findChessboardCorners(self.gray, chessboardSize, None)

                if self.ret == True:
                    self.objpoints.append(objp)
                    corners2 = cv.cornerSubPix(self.gray,corners, (11,11), (-1,-1), criteria)
                    self.imgpoints.append(corners2)
                    cv.drawChessboardCorners(self.frame, chessboardSize, corners2, self.ret)
                    
                    if self.imshow == True:
                        cv.imshow(f"Calibrated images, Camera{index}", self.frame)
                        k = cv.waitKey(0)

                        if k == ord('q'):
                            break
                        
                        cv.destroyAllWindows()
                    
                if self.ret == False:
                    print("No pattern detected")
                    break
                
            path += 1
            index += 1



            
                          