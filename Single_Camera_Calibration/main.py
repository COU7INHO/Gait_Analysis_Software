from CameraCalibration import CalibrateCamera
from DisplayCalibratedVideo import DisplayVideo

cam1_index = 0
cam2_index = 1

new_calibration = input("\nNew camera to calibrate? Y -> Yes\n>> ").upper()

cameras = CalibrateCamera(cam1_index, cam2_index)

if new_calibration == 'Y':
    cameras.getCalibrationImages()
    cameras.findChessboardCorners(imshow=False)
    cameras.calibrateCamera()

video = DisplayVideo(cam1_index, cam2_index)
video.display()
