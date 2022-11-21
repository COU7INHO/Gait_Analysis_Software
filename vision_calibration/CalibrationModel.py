
#* This class is used to calibrate both cameras using a chessboard 

import cv2
import numpy as np 
import glob
from vision_calibration.GetBothCamsImgs import GetCalibrationImages

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
CRITERIA_STEREO = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
FLAGS = 0
FLAGS |= cv2.CALIB_FIX_INTRINSIC

class CalibrationModel(GetCalibrationImages):

    def __init__(self, cam1_index, cam2_index, squaresize, chessboardrows=9, chessboardcols=6, framewidth=1200, frameheight=720):
        super().__init__(cam1_index, cam2_index)
        self.chessboardrows = chessboardrows
        self.chessboardcols = chessboardcols
        self.chessboardsize = (self.chessboardrows, chessboardcols)
        self.squaresize = squaresize
        self.framewidth = framewidth
        self.frameheight = frameheight
        self.framesize = (self.framewidth, self.frameheight)
    
    def findChessboardCorners(self, imshow=False):
        objp = np.zeros((self.chessboardrows * self.chessboardcols, 3), np.float32)
        objp[:,:2] = np.mgrid[0:self.chessboardrows,0:self.chessboardcols].T.reshape(-1,2)
        objp = objp * self.squaresize
        self.objpoints = [] 
        self.imgpointsL = []
        self.imgpointsR = [] 

        imagesLeft = sorted(glob.glob(self.path1 + "*.png"))
        imagesRight = sorted(glob.glob(self.path2 + "*.png"))
        cv2.waitKey(2000)

        for imgLeft, imgRight in zip(imagesLeft, imagesRight):

            self.imgL = cv2.imread(imgLeft)
            self.imgR = cv2.imread(imgRight)
            self.grayL = cv2.cvtColor(self.imgL, cv2.COLOR_BGR2GRAY)
            self.grayR = cv2.cvtColor(self.imgR, cv2.COLOR_BGR2GRAY)

            self.retL, cornersL = cv2.findChessboardCorners(self.grayL, self.chessboardsize, None)
            self.retR, cornersR = cv2.findChessboardCorners(self.grayR, self.chessboardsize, None)

            if self.retL and self.retR == True:

                self.objpoints.append(objp)

                cornersL = cv2.cornerSubPix(self.grayL, cornersL, (11,11), (-1,-1), CRITERIA)
                self.imgpointsL.append(cornersL)

                cornersR = cv2.cornerSubPix(self.grayR, cornersR, (11,11), (-1,-1), CRITERIA)
                self.imgpointsR.append(cornersR)

                cv2.drawChessboardCorners(self.imgL, self.chessboardsize, cornersL, self.retL)
                cv2.drawChessboardCorners(self.imgR, self.chessboardsize, cornersR, self.retR)
                
                if imshow == True:

                    imgRL = np.hstack((self.imgL, self.imgR))
                    cv2.imshow("Chessboard corners", imgRL)
                    cv2.waitKey(2000)

        cv2.destroyAllWindows()

    def calibration(self):

        self.retL, cameraMatrixL, self.distL, self.rvecsL, self.tvecsL = cv2.calibrateCamera(self.objpoints, self.imgpointsL, self.framesize, None, None)
        heightL, widthL, self.channelsL = self.imgL.shape
        self.newCameraMatrixL, self.roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, self.distL, (widthL, heightL), 1, (widthL, heightL))

        self.retR, cameraMatrixR, self.distR, self.rvecsR, self.tvecsR = cv2.calibrateCamera(self.objpoints, self.imgpointsR, self.framesize, None, None)
        heightR, widthR, self.channelsR = self.imgR.shape
        self.newCameraMatrixR, self.roi_R = cv2.getOptimalNewCameraMatrix(cameraMatrixR, self.distR, (widthR, heightR), 1, (widthR, heightR))
    
    def stereoCalculation(self):
        self.retStereo, self.newCameraMatrixL, self.distL, self.newCameraMatrixR, self.distR, self.rot, self.trans, self.essentialMatrix, self.fundamentalMatrix = cv2.stereoCalibrate(self.objpoints, self.imgpointsL, self.imgpointsR, self.newCameraMatrixL, self.distL, self.newCameraMatrixR, self.distR, self.grayL.shape[::-1], CRITERIA_STEREO, FLAGS)
        
    def newMatrix(self):
        rectifyScale = 1
        rectL, rectR, projMatrixL, projMatrixR, Q, self.roi_L, self.roi_R = cv2.stereoRectify(self.newCameraMatrixL, self.distL, self.newCameraMatrixR, self.distR, self.grayL.shape[::-1], self.rot, self.trans, rectifyScale,(0,0))

        stereoMapL = cv2.initUndistortRectifyMap(self.newCameraMatrixL, self.distL, rectL, projMatrixL, self.grayL.shape[::-1], cv2.CV_16SC2)
        stereoMapR = cv2.initUndistortRectifyMap(self.newCameraMatrixR, self.distR, rectR, projMatrixR, self.grayR.shape[::-1], cv2.CV_16SC2)

        cv_file = cv2.FileStorage("./vision_calibration/stereoMap.xml", cv2.FILE_STORAGE_WRITE)

    
        cv_file.write('stereoMapL_x',stereoMapL[0])
        cv_file.write('stereoMapL_y',stereoMapL[1])
        cv_file.write('stereoMapR_x',stereoMapR[0])
        cv_file.write('stereoMapR_y',stereoMapR[1])

        cv_file.release()