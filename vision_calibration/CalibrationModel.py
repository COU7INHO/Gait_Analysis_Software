import cv2
import numpy as np 
import glob
from GetBothCamsImgs import GetCalibrationImages

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
CRITERIA_STEREO = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


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
    
    def find_chessboard_corners(self):
        objp = np.zeros((self.chessboardrows * self.chessboardcols, 3), np.float32)
        objp[:,:2] = np.mgrid[0:self.chessboardrows,0:self.chessboardcols].T.reshape(-1,2)
        objp = objp * self.squaresize
        objpoints = [] 
        imgpointsL = []
        imgpointsR = [] 

        imagesLeft = sorted(glob.glob(self.path1 + "*.png"))
        imagesRight = sorted(glob.glob(self.path2 + "*.png"))

        for imgLeft, imgRight in zip(imagesLeft, imagesRight):

            imgL = cv2.imread(imgLeft)
            imgR = cv2.imread(imgRight)
            grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
            grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

            retL, cornersL = cv2.findChessboardCorners(grayL, self.chessboardsize, None)
            retR, cornersR = cv2.findChessboardCorners(grayR, self.chessboardsize, None)

            if retL and retR == True:  #! ret = False

                objpoints.append(objp)

                cornersL = cv2.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), CRITERIA)
                imgpointsL.append(cornersL)

                cornersR = cv2.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), CRITERIA)
                imgpointsR.append(cornersR)

                cv2.drawChessboardCorners(imgL, self.chessboardsize, cornersL, retL)
                cv2.drawChessboardCorners(imgR, self.chessboardsize, cornersR, retR)
                cv2.imshow('abc', imgL)
                cv2.imshow('abc', imgR)
                cv2.waitKey(2000)

        cv2.destroyAllWindows()

#* Calibration
        retL, cameraMatrixL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, self.framesize, None, None)
        heightL, widthL, channelsL = imgL.shape
        newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

        retR, cameraMatrixR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, self.framesize, None, None)
        heightR, widthR, channelsR = cv2.shape
        newCameraMatrixR, roi_R = cv2.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

#* Stereo vision calibration
        flags = 0
        flags |= cv2.CALIB_FIX_INTRINSIC

        criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#* Transformation between the two cameras and calculate Essential and Fundamental matrix
        retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(objpoints, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags)

#* Stereo Rectification
        rectifyScale= 1
        rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv2.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale,(0,0))

        stereoMapL = cv2.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv2.CV_16SC2)
        stereoMapR = cv2.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv2.CV_16SC2)

        print("Saving parameters!")
        cv_file = cv2.FileStorage('stereoMap.xml', cv2.FILE_STORAGE_WRITE)

        cv_file.write('stereoMapL_x',stereoMapL[0])
        cv_file.write('stereoMapL_y',stereoMapL[1])
        cv_file.write('stereoMapR_x',stereoMapR[0])
        cv_file.write('stereoMapR_y',stereoMapR[1])

        cv_file.release()