from GetBothCamsImgs import GetCalibrationImages
from CalibrationModel import CalibrationModel

images = GetCalibrationImages(0, 1)
images.get_images()
model = CalibrationModel(0, 1, 25)
model.find_chessboard_corners()
model.calibration()
model.matrixcalculation()
model.newmatrix()
