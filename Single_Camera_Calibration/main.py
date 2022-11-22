from CameraCalibration import CalibrateCamera


cameras = CalibrateCamera(0, 1)
cameras.getCalibrationImages()
cameras.findChessboardCorners(imshow=False)
cameras.calibrateCamera()
cameras.display()