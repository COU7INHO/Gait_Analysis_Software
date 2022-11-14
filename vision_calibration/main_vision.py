from GetBothCamsImgs import GetCalibrationImages
from CalibrationModel import CalibrationModel
from CalibratedImages import calibrated_images

cam1 = 0
cam2 = 1
square_size = 25
new_images = input("Do you want to get new calibration images? \n 'Y' -> Yes \n >> ").upper()

if new_images == 'Y':
    images = GetCalibrationImages(cam1, cam2)
    images.get_images()

model = CalibrationModel(cam1, cam2, square_size)
model.find_chessboard_corners()
model.calibration()
model.matrixcalculation()
model.newmatrix()
calibrated_images(cam1, cam2)
