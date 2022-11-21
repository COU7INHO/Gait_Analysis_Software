from vision_calibration.GetBothCamsImgs import GetCalibrationImages
from vision_calibration.CalibrationModel import CalibrationModel
from vision_calibration.CalibratedImages import CalibratedImages
from camera_pose_estimation.Measure import Measure


cam1 = 0
cam2 = 1
square_size = 25
new_images = input("Do you want to get new calibration images? \n 'Y' -> Yes \n >> ").upper()

if new_images == 'Y':
    images = GetCalibrationImages(cam1, cam2)
    images.clearPath()
    images.getImages()

output = CalibrationModel(cam1, cam2, square_size, framewidth=640, frameheight=480)
output.findChessboardCorners(imshow=False)
output.calibration()
output.stereoCalculation()
output.newMatrix()
output = CalibratedImages(cam1, cam2)
img1, img2 = output.calibratedImages(imshow=False)
model = Measure(cam1, cam2, img1, img2)
model.calibrated_env()