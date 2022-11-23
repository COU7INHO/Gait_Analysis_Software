'''Os objpoints são os mesmos para as duas câmaras
Fazer algum ciclo for que criar objpoints para cada uma das câmaras '''

import cv2 as cv 
import os
import glob
import numpy as np

CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

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
        self.chessboardSize = (self.chessboardRows, self.chessboardCols)
        
        self.objp = np.zeros((self.chessboardCols*self.chessboardRows,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:self.chessboardRows,0:self.chessboardCols].T.reshape(-1,2)
        self.objp = self.objp * self.squareSize

        self.objpoints = [] 
        self.imgpoints = [] 
        
        path = 0
        index = 0

        for index in range(len(self.indices)):
            images = glob.glob(self.paths[path] + "*.png")

            for img in images:
                self.frame = cv.imread(img)
                self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
                self.ret, corners = cv.findChessboardCorners(self.gray, self.chessboardSize, None)

                if self.ret == True:
                    self.objpoints.append(self.objp)
                    corners2 = cv.cornerSubPix(self.gray,corners, (11,11), (-1,-1), CRITERIA)
                    self.imgpoints.append(corners2)
                    
                    if self.imshow == True:
                        cv.drawChessboardCorners(self.frame, self.chessboardSize, corners2, self.ret)
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

    def calibrateCamera(self):

        path = 0
        index = 0
   
        for index in range(len(self.indices)):
            images = glob.glob(self.paths[path] + "*.png")

            for img in images:
                self.frame = cv.imread(img)
                self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
                self.ret, corners = cv.findChessboardCorners(self.gray, self.chessboardSize, None)

                if self.ret == True:
                    self.objpoints.append(self.objp)
                    corners2 = cv.cornerSubPix(self.gray,corners, (11,11), (-1,-1), CRITERIA)
                    self.imgpoints.append(corners2)
            
                    self.ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.objpoints, self.imgpoints, self.gray.shape[::-1], None, None)
                    h, w = self.frame.shape[:2]
                    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
                    mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
                    
                    cv_file = cv.FileStorage(f"./Single_Camera_Calibration/map{index}.xml", cv.FILE_STORAGE_WRITE)
                    cv_file.write(f"map{index}_x",mapx)
                    cv_file.write(f"map{index}_y",mapy)
                    cv_file.release()

                    mean_error = 0
                    for i in range(len(self.objpoints)):
                        imgpoints2, _ = cv.projectPoints(self.objpoints[i], rvecs[i], tvecs[i], mtx, dist)
                        error = cv.norm(self.imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
                        mean_error += error
                    print( f"Cam{index} error: {mean_error/len(self.objpoints)}")

            path += 1
            index += 1

    def display(self):
        index = 0

        for index, camera in zip(self.indices, self.cameras):
            cv_file = cv.FileStorage()
            cv_file.open(f"./Single_Camera_Calibration/map{index}.xml", cv.FileStorage_READ)

            map_x = cv_file.getNode(f"map{index}_x").mat()
            map_y = cv_file.getNode(f"map{index}_y").mat()

            while camera.isOpened():
                success, frame = camera.read()
                frame = cv.remap(frame, map_x, map_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
                cv.imshow("Calibrated video", frame)
                if cv.waitKey(1) == ord('q'):
                    break

            camera.release()
            cv.destroyAllWindows()
                
            index += 1              