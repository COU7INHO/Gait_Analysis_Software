from CameraCalibration import CalibrateCamera


cameras = CalibrateCamera(0, 1)
cameras.getCalibrationImages()
cameras.calibrateCamera(imshow=True)
